"""
Single-page chat UI for the Adaptive RAG API. Run: streamlit run streamlit_app/home.py
"""

import os
import uuid

import requests
import streamlit as st

API_URL = os.getenv("RAG_API_URL", "http://127.0.0.1:8000").rstrip("/")
TIMEOUT = 300  # answers can take a minute (LLM CLI + retrieval)
TIER_BADGE = {"knowledge": ":blue[knowledge]", "rag": ":green[rag]", "hybrid": ":orange[hybrid]", "web": ":violet[web]"}

st.set_page_config(page_title="Adaptive RAG", page_icon="💬")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.turns = []  # [{"role": "user"|"assistant", "content": str, "result": dict | None}]
    st.session_state.uploaded = {}  # (name, size) -> upload response, so each file is indexed once


def call_api(method: str, path: str, **kwargs):
    """Returns (json, error); error is a readable string and json is None on failure."""
    try:
        r = requests.request(method, API_URL + path, timeout=TIMEOUT, **kwargs)
    except requests.RequestException as e:
        return None, f"Cannot reach the API at {API_URL}: {e}"
    if not r.ok:
        try:
            detail = r.json().get("detail", r.text)
        except ValueError:
            detail = r.text
        return None, f"API error {r.status_code}: {detail}"
    return r.json(), None


def render_sources(citations: list[dict]):
    for c in citations:
        mark = "✓" if c.get("verified") else "⚠"
        where = f"[{c.get('title') or c['url']}]({c['url']})" if c.get("url") else c.get("label", c.get("source", ""))
        st.markdown(f"**[{c['n']}]** {where} {mark}")
        st.caption(f"“{c.get('quote', '')}”" + ("" if c.get("verified") else f" — {c.get('reason', '')}"))


def render_assistant(turn: dict):
    st.markdown(turn["content"])
    r = turn["result"]
    if not r:
        return
    verified = ":green[✓ citations verified]" if r.get("verified") else ":red[⚠ unverified]"
    st.caption(f"{TIER_BADGE.get(r.get('tier'), r.get('tier'))} · {verified}")
    with st.expander("How I answered"):
        for step in r.get("trace", []):
            st.markdown(f"- {step}")
    if r.get("citations"):
        with st.expander("Sources", expanded=True):
            render_sources(r["citations"])


with st.sidebar:
    st.header("Adaptive RAG")
    if st.button("New chat", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.turns = []
        st.rerun()

    st.subheader("Add a document")
    file = st.file_uploader("PDF, TXT or Markdown", type=["pdf", "txt", "md"])
    description = st.text_input("Description (optional)")
    if file and st.button("Index document", use_container_width=True):
        key = (file.name, file.size)
        if key not in st.session_state.uploaded:
            with st.spinner("Indexing..."):
                data, err = call_api(
                    "POST", "/rag/documents/upload",
                    files={"file": (file.name, file.getvalue())}, headers={"X-Description": description},
                )
            if err:
                st.error(err)
            else:
                st.session_state.uploaded[key] = data["document"]
        if key in st.session_state.uploaded:
            doc = st.session_state.uploaded[key]
            st.success(f"{doc['name']}: {doc['status']} ({doc['pages']} pages, {doc['chunks']} chunks)")

    st.subheader("Indexed documents")
    docs, err = call_api("GET", "/rag/documents")
    if err:
        st.error(err)
    elif not docs:
        st.caption("No documents yet.")
    for d in docs or []:
        st.markdown(f"**{d['name']}** · {d['pages']} pages, {d['chunks']} chunks")
        if d.get("description"):
            st.caption(d["description"])

st.title("Adaptive RAG")
for turn in st.session_state.turns:
    with st.chat_message(turn["role"]):
        render_assistant(turn) if turn["role"] == "assistant" else st.markdown(turn["content"])

if query := st.chat_input("Ask a question"):
    st.session_state.turns.append({"role": "user", "content": query, "result": None})
    with st.chat_message("user"):
        st.markdown(query)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result, err = call_api("POST", "/rag/query", json={"query": query, "session_id": st.session_state.session_id})
        if err:
            st.error(err)
        else:
            turn = {"role": "assistant", "content": result["answer"], "result": result}
            st.session_state.turns.append(turn)
            render_assistant(turn)
