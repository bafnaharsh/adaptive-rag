"""Offline tests for deterministic citation verification and rendering."""

import pytest

from src.models.evidence import Chunk
from src.rag import citations, store

PAGE = Chunk("doc:7", "Battery life: the iPhone 17 lasts up to 20 hours of video playback. The “Smart Stack” widget—new "
                      "in iOS 26—shows it’s   time\nto charge when the bat-\ntery drops below 20 percent.",
             "iphone_user_guide.pdf", page=42)
SITE = Chunk("web:ab12", "Apple released iOS 26 on September 15, 2026.", "https://example.com/ios26", title="iOS 26 release")
EVIDENCE = {c.id: c for c in (PAGE, SITE)}


@pytest.fixture(autouse=True)
def empty_store(monkeypatch):
    monkeypatch.setattr(store, "get_chunk", lambda chunk_id: None)


def check(quote, source_id="doc:7", evidence=EVIDENCE):
    return citations.verify([{"n": 1, "source_id": source_id, "quote": quote}], evidence)[0]


def test_exact_quote():
    c = check("the iPhone 17 lasts up to 20 hours of video playback")
    assert c["verified"] and c["reason"] == ""
    assert (c["n"], c["source_id"], c["source"], c["page"], c["url"], c["label"]) == (
        1, "doc:7", "iphone_user_guide.pdf", 42, None, "iphone_user_guide.pdf, p. 42")


@pytest.mark.parametrize("quote", [
    '"Smart Stack" widget–new in iOS 26–shows it\'s time to charge',  # straight quotes, en dashes, single spaces
    "“The iPhone 17 lasts up to 20 hours of video playback.”",  # surrounding curly quotes, case, final period
    "…the  iPhone 17 lasts\nup to 20 hours...",  # surrounding ellipses, odd whitespace
])
def test_normalized_variants(quote):
    assert check(quote)["verified"]


def test_ellipsis_segments_must_match_in_order():
    assert check("the iPhone 17 lasts ... of video playback")["verified"]
    assert not check("of video playback ... the iPhone 17 lasts")["verified"]


def test_fuzzy_match_tolerates_pdf_hyphenation():
    assert check("to charge when the battery drops below 20 percent")["verified"]


@pytest.mark.parametrize("quote", ["to charge when the battery drops below 25 percent",
                                   "lasts up to 20 hours of audio playback"])
def test_fuzzy_match_rejects_changed_words(quote):
    c = check(quote)
    assert not c["verified"] and c["reason"] == "quote not found in the source text"


def test_too_short_quote():
    c = check("20 hours")
    assert not c["verified"] and "too short" in c["reason"]


def test_unknown_source_id():
    c = check("the iPhone 17 lasts up to 20 hours", source_id="doc:99")
    assert not c["verified"] and c["reason"] == "unknown source id" and c["label"] == "doc:99"


def test_falls_back_to_store(monkeypatch):
    monkeypatch.setattr(store, "get_chunk", lambda chunk_id: PAGE if chunk_id == "doc:7" else None)
    assert check("the iPhone 17 lasts up to 20 hours", evidence=None)["verified"]


def test_render_with_page_url_and_warning():
    cits = citations.verify([
        {"n": 1, "source_id": "doc:7", "quote": "lasts up to 20 hours of video playback"},
        {"n": 2, "source_id": "web:ab12", "quote": "Apple released iOS 26 on September 15, 2026"},
        {"n": 3, "source_id": "doc:7", "quote": "the battery lasts three whole days"},
    ], EVIDENCE)
    assert cits[1]["url"] == "https://example.com/ios26"
    assert citations.render("Answer [1][2][3].", cits) == (
        "Answer [1][2][3].\n\n**Sources**\n"
        "- [1] iphone_user_guide.pdf, p. 42 ✓ — “lasts up to 20 hours of video playback”\n"
        "- [2] [iOS 26 release](https://example.com/ios26) ✓ — “Apple released iOS 26 on September 15, 2026”\n"
        "- [3] iphone_user_guide.pdf, p. 42 ⚠ quote not found in the source text — “the battery lasts three whole days”")


def test_render_without_citations_is_the_answer():
    assert citations.render("Hello!", []) == "Hello!"
