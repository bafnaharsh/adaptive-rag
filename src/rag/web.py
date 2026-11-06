"""
Tier 3: web search. Tavily when settings.TAVILY_API_KEY is set, otherwise DuckDuckGo (ddgs, no key).
"""

import hashlib
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup

from src.core.config import settings
from src.core.logger import logger
from src.models.evidence import Chunk
from src.rag import store

_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; adaptive-rag/1.0)"}
_FETCH = 4
_MAX_PAGE_CHARS = 20_000  # shortcut: only the start of long pages is reranked (CPU cost); raise if answers get cut


def _search(query: str) -> list[dict]:
    """[{"url", "title", "snippet"}] from Tavily or DuckDuckGo."""
    if settings.TAVILY_API_KEY:
        from tavily import TavilyClient

        hits = TavilyClient(api_key=settings.TAVILY_API_KEY).search(query, max_results=8)["results"]
        return [{"url": h["url"], "title": h.get("title", ""), "snippet": h.get("content", "")} for h in hits]
    from ddgs import DDGS
    from ddgs.exceptions import DDGSException

    for attempt in range(3):
        try:
            hits = DDGS().text(query, max_results=8)
            break
        except DDGSException:  # backends rate-limit bursts at random; a later "auto" pass usually lands on a working one
            if attempt == 2:
                raise
            time.sleep(1.5 * (attempt + 1))
    return [{"url": h["href"], "title": h.get("title", ""), "snippet": h.get("body", "")} for h in hits]


def _fetch(url: str) -> tuple[str, str]:
    """(page title, visible text) or ("", "") when the page is unreachable or not HTML."""
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=8)
        if not resp.ok or "html" not in resp.headers.get("content-type", ""):
            return "", ""
        soup = BeautifulSoup(resp.content, "html.parser")  # bytes, so bs4 honours the page's own charset
        for tag in soup(["script", "style", "noscript", "nav", "header", "footer", "aside", "form"]):
            tag.decompose()
        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        return title, soup.get_text("\n")[:_MAX_PAGE_CHARS]
    except Exception as e:  # one bad page must not sink the whole search
        logger.info("web fetch skipped %s: %s", url, e)
        return "", ""


def _passage(url: str, title: str, text: str) -> Chunk:
    return Chunk("web:" + hashlib.sha1((url + text).encode()).hexdigest()[:12], text, url, None, title)


def web_search(query: str, k: int = 5) -> list[Chunk]:
    """Search, fetch the top result pages' text, split into passages, rerank them against the query and return the
    best k as Chunks: id "web:<hex>", source = page URL, title = page title, page = None. The passages are saved with
    store.save_web_chunks so citations to them can be verified later. Returns [] (never raises) when offline."""
    try:
        hits = [h for h in _search(query) if h["url"].startswith("http")]
        with ThreadPoolExecutor(_FETCH) as pool:
            pages = list(pool.map(_fetch, [h["url"] for h in hits[:_FETCH]]))
        passages = {}
        for i, hit in enumerate(hits):
            title, text = pages[i] if i < len(pages) else ("", "")
            title = title or hit["title"]
            for piece in [" ".join(hit["snippet"].split()), *store._split(store._clean(text))]:
                if piece:
                    chunk = _passage(hit["url"], title, piece)
                    passages[chunk.id] = chunk
        best = store.rerank(query, list(passages.values()), k)
        store.save_web_chunks(best)
        return best
    except Exception as e:  # contract: the web tier degrades to "no evidence", never an error
        logger.warning("web search failed for %r: %s", query, e)
        return []
