"""
One prompt -> one answer, through whatever the user already has:

- cli:claude | cli:agy | cli:copilot: the harness CLI you are logged into, so no API key. Every CLI runs text-only
  (no tools, no auto-approved permissions). claude runs as a pool of long-lived stream-json sessions (~1 s per call
  after a ~4 s start, against 6-10 s for a fresh process).
- <provider>:<model> (BYOK): LangChain init_chat_model, e.g. openai:gpt-4o-mini with OPENAI_API_KEY set and
  langchain-openai installed.

settings.LLM_MODEL is a comma-separated fallback chain: "cli:claude,cli:agy" tries claude, then agy.
"""

import atexit
import json
import queue
import re
import subprocess
import threading
import time
from functools import lru_cache

from src.core.config import settings

CLI_DEFAULT_MODEL = {"claude": "haiku", "agy": "gemini-3.8-flash-medium", "copilot": "auto"}
ARGV_MAX = 28_000  # Windows command lines cap at 32767 chars and agy takes the prompt only as an argument
LEAN = ["--strict-mcp-config", "--no-session-persistence", "--tools", "", "--setting-sources", "",
        "--system-prompt", "You answer exactly what the user asks, in the format asked. You have no tools."]
RECYCLE = 4  # calls per claude session: every call adds its prompt to the session context, which slows later calls
CWD = settings.DATA_DIR / "llm"  # empty dir: no project instructions (CLAUDE.md, AGENTS.md) leak into the call


class LLMError(RuntimeError):
    pass


def parse_json(text: str):
    """The JSON value in a model reply: a ```json fence, else the outermost {...} or [...]."""
    if m := re.search(r"```(?:json)?\s*(.+?)```", text, re.S):
        text = m.group(1)
    starts = [i for i in (text.find("{"), text.find("[")) if i >= 0]
    if not starts:
        raise ValueError(f"no JSON in reply: {text[:200]}")
    start = min(starts)
    end = text.rfind("}" if text[start] == "{" else "]")
    return json.loads(text[start:end + 1])


class _Session:
    """One long-lived `claude -p` taking prompts as stream-json lines; a reader thread queues its output lines."""

    def __init__(self, model: str):
        CWD.mkdir(parents=True, exist_ok=True)
        self.proc = subprocess.Popen(
            ["claude", "-p", "--input-format", "stream-json", "--output-format", "stream-json", "--verbose", *LEAN,
             "--model", model], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, encoding="utf-8", bufsize=1, cwd=CWD)
        self.lines: queue.Queue = queue.Queue()
        self.calls = 0
        threading.Thread(target=lambda: [self.lines.put(line) for line in self.proc.stdout] + [self.lines.put(None)],
                         daemon=True).start()

    def ask(self, prompt: str, timeout: float) -> str:
        self.calls += 1
        msg = {"type": "user", "message": {"role": "user", "content": "Ignore earlier messages; this task stands "
                                                                       "alone.\n\n" + prompt}}
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()
        deadline = time.monotonic() + timeout
        while True:
            line = self.lines.get(timeout=max(0.1, deadline - time.monotonic()))  # queue.Empty on timeout
            if line is None:
                raise LLMError("claude session ended")
            out = json.loads(line)
            if out.get("type") == "result":
                if out.get("is_error"):
                    raise LLMError(out.get("result") or "claude failed")
                return (out.get("result") or "").strip()

    def close(self) -> None:
        self.proc.kill()


_pool: queue.Queue = queue.Queue()


@atexit.register
def _close_all() -> None:  # Windows keeps child processes alive after the parent exits
    while True:
        try:
            _pool.get_nowait().close()
        except queue.Empty:
            return


def _claude(model: str, prompt: str, timeout: float) -> str:
    try:
        sess = _pool.get_nowait()
    except queue.Empty:
        sess = _Session(model)
    try:
        text = sess.ask(prompt, timeout)
    except BaseException:
        sess.close()  # a broken or timed-out session is never reused
        raise
    if sess.calls >= RECYCLE:
        sess.close()
        _pool.put(_Session(model))  # started now, it is warm by the next call
    else:
        _pool.put(sess)
    return text


def _cli(name: str, model: str, prompt: str, timeout: float) -> str:
    if name == "claude":
        return _claude(model, prompt, timeout)
    if name == "agy":  # --sandbox and no auto-approve: a text-only call
        argv, stdin = ["agy", "-p", prompt[:ARGV_MAX], "--output-format", "json", "--sandbox", "--model", model], None
    elif name == "copilot":  # --available-tools= leaves the model no tools at all
        argv, stdin = ["copilot", "-s", "--available-tools=", "--disable-builtin-mcps", "--model", model], prompt
    else:
        raise LLMError(f"unknown CLI backend cli:{name}")
    CWD.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(argv, input=stdin, capture_output=True, text=True, encoding="utf-8", timeout=timeout, cwd=CWD)
    if r.returncode != 0:
        raise LLMError((r.stderr or r.stdout)[-500:])
    if name == "copilot":
        return r.stdout.strip()
    out = json.loads(r.stdout.strip().splitlines()[-1])
    if out.get("status") != "SUCCESS":
        raise LLMError(out.get("error") or "agy failed")
    return out["response"].strip()


@lru_cache(maxsize=None)
def _byok(model: str):
    from langchain.chat_models import init_chat_model
    return init_chat_model(model)


def _byok_ask(model: str, prompt: str) -> str:
    content = _byok(model).invoke(prompt).content
    if isinstance(content, list):  # Anthropic/Gemini may return content blocks
        content = "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in content)
    return content.strip()


def warm() -> None:
    """Start two claude sessions now (Popen returns at once): the first question skips the ~4 s start, and calls
    alternate between them, so a session recycled after RECYCLE calls has warmed up before it is used again."""
    if backends()[:1] == ["cli:claude"]:
        for _ in range(2):
            _pool.put(_Session(settings.CLI_MODEL or CLI_DEFAULT_MODEL["claude"]))


def backends() -> list[str]:
    return [b.strip() for b in settings.LLM_MODEL.split(",") if b.strip()]


def ask(prompt: str, timeout: float | None = None) -> str:
    """The first backend's answer. Raises LLMError when every backend in the chain fails."""
    errors = []
    for backend in backends():
        try:
            if backend.startswith("cli:"):
                name = backend[4:]
                return _cli(name, settings.CLI_MODEL or CLI_DEFAULT_MODEL.get(name, ""), prompt,
                            timeout or settings.LLM_TIMEOUT)
            return _byok_ask(backend, prompt)
        except Exception as e:  # any backend failure falls through to the next one in the chain
            errors.append(f"{backend}: {str(e)[:300]}")
    raise LLMError("; ".join(errors) or "LLM_MODEL is empty")


def ask_json(prompt: str, timeout: float | None = None, retries: int = 1):
    """ask() and parse the JSON in the reply; one retry with a reminder when the reply is not valid JSON."""
    for attempt in range(retries + 1):
        text = ask(prompt if attempt == 0 else prompt + "\n\nReturn ONLY valid JSON, nothing else.", timeout)
        try:
            return parse_json(text)
        except ValueError:
            if attempt == retries:
                raise
