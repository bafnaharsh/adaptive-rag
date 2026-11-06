# Harness integration (no API key)

`src/mcp_server.py` is an MCP server (`adaptive-rag`, stdio) exposing retrieval, web search and citation checking.
The harness's own model does the reasoning, following the research protocol the server sends at initialize
(also available as the MCP prompt `adaptive_research`).

Tools: `list_documents`, `ingest_document(path, description)`, `search_documents(query, mode, k, extra_queries, doc_ids)`,
`web_search(query, k)`, `verify_citations(citations)`, `research(question)` (server-side pipeline, slower).

Protocol: Tier 0 own knowledge only if not about the documents, not time-sensitive and reliably known (labelled
"model knowledge, not verified"); Tier 1 `search_documents(mode="dense")`; Tier 2 `mode="hybrid"` with 2-3 rewritten or
decomposed `extra_queries`; Tier 3 `web_search`. Answer only from evidence with `[n]` markers, check them with
`verify_citations` (verbatim quotes), end with a Sources list, and state which tier answered.

## Claude Code

`.mcp.json` at the repo root is picked up when you start `claude` in the repo (approve the project server once).
Check: `claude mcp list`. One-off: `claude -p "..." --mcp-config .mcp.json --strict-mcp-config`.
Run the protocol with `/mcp__adaptive-rag__adaptive_research <question>`.

## Antigravity (agy) CLI

User scope, registered with (agy has no cwd option, so `PYTHONPATH` points at the repo):

    agy mcp add -e "PYTHONPATH=C:/Users/HARSH BAFNA/B.E/project/adapt rag/Adaptive-Rag" adaptive-rag "C:/Users/HARSH BAFNA/B.E/project/adapt rag/Adaptive-Rag/.venv/Scripts/python.exe" -m src.mcp_server

Check: `agy mcp list`. Undo: `agy mcp remove adaptive-rag`.

## GitHub Copilot

- VS Code agent mode: `.vscode/mcp.json` is picked up when the repo is the workspace (Start it from the file's CodeLens
  or the MCP: List Servers command).
- Copilot CLI, user scope (`~/.copilot/mcp-config.json`):

      copilot mcp add --env "PYTHONPATH=C:/Users/HARSH BAFNA/B.E/project/adapt rag/Adaptive-Rag" adaptive-rag -- "C:/Users/HARSH BAFNA/B.E/project/adapt rag/Adaptive-Rag/.venv/Scripts/python.exe" -m src.mcp_server

  Check: `copilot mcp list` / `copilot mcp get adaptive-rag`. Undo: `copilot mcp remove adaptive-rag`.

## LLM backend for the server-side pipeline (`research` tool, API, web UI)

Set `LLM_MODEL` (env or `.env`); a comma-separated list is a fallback chain (see `src/llms/llm.py`):

- `cli:claude` (default), `cli:agy`, `cli:copilot`: run a CLI you are already logged into, no key.
- BYOK via LangChain: `openai:gpt-4o-mini`, `anthropic:claude-sonnet-4-5`, `google_genai:gemini-2.5-flash`, `ollama:llama3.1`
  (needs the provider's key env var, e.g. `OPENAI_API_KEY`).

`CLI_MODEL` picks the model flag for `cli:*`. The harness protocol above never uses this: it needs no LLM backend.

## Troubleshooting

Logs go to stderr (the harness shows them in its MCP log). Never print to stdout in code the server imports: stdout is
the JSON-RPC channel. `tests/test_mcp_server.py` starts the real server over stdio to catch that.
