"""Offline tests for the document store (models load once from the real DATA_DIR/models; each test gets a tmp DB)."""

import sqlite3
import textwrap

import pytest
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from src.core.config import settings
from src.models.evidence import Chunk
from src.rag import store

RESTART = ("To force restart iPhone, press and quickly release the volume up button, press and quickly release the "
           "volume down button, then press and hold the side button. When the Apple logo appears, release the button.")
PLANTS = ("Photosynthesis is the process by which green plants use sunlight, water and carbon dioxide to produce "
          "glucose and oxygen. It takes place in the chloroplasts of leaf cells.")
TOWER = ("The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris. It was completed in 1889 "
         "for the World's Fair and is 330 metres tall.")


@pytest.fixture(scope="session", autouse=True)
def _models():
    store._embedder(), store._reranker()  # load into the real models cache before DATA_DIR moves to tmp


@pytest.fixture
def data(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "DATA_DIR", tmp_path)
    return tmp_path


def _txt(dir_, name, text):
    path = dir_ / name
    path.write_text(text, encoding="utf-8")
    return path


def _pdf(path, pages):
    """Minimal PDF with one Helvetica text block per page ('' makes a blank page)."""
    writer = PdfWriter()
    font = DictionaryObject({NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"),
                             NameObject("/BaseFont"): NameObject("/Helvetica")})
    for text in pages:
        page = writer.add_blank_page(612, 792)
        page[NameObject("/Resources")] = DictionaryObject(
            {NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})})
        lines = " ".join(f"({line}) Tj T*" for line in textwrap.wrap(text, 95))
        stream = DecodedStreamObject()
        stream.set_data(f"BT /F1 9 Tf 36 760 Td 11 TL {lines} ET".encode("latin-1"))
        page[NameObject("/Contents")] = writer._add_object(stream)
    writer.write(path)
    return path


def _corpus(dir_):
    return {name: store.add_document(_txt(dir_, f"{name}.txt", text))["doc_id"]
            for name, text in (("restart", RESTART), ("plants", PLANTS), ("tower", TOWER))}


def test_txt_ingest_is_idempotent(data):
    path = _txt(data, "notes.md", "# Notes\n\n" + RESTART)
    first = store.add_document(path, description="phone notes")
    assert first["status"] == "added" and first["name"] == "notes.md" and first["pages"] == 1 and first["chunks"] == 1
    again = store.add_document(_txt(data, "copy.md", "# Notes\n\n" + RESTART))
    assert again == {**first, "status": "exists"}
    assert store.list_documents() == [{k: first[k] for k in ("doc_id", "name", "description", "pages", "chunks")}]
    chunk = store.keyword_search("volume")[0]
    assert chunk.page is None and chunk.source == "notes.md" and chunk.title == "phone notes"


def test_rejects_unsupported_and_empty(data):
    with pytest.raises(ValueError):
        store.add_document(_txt(data, "x.csv", "a,b"))
    with pytest.raises(ValueError):
        store.add_document(_txt(data, "empty.txt", "  \n\n "))
    with pytest.raises(ValueError):
        store.add_document(_txt(data, "broken.pdf", "not a pdf"))
    assert store.list_documents() == [] and store.dense_search("x") == [] and store.hybrid_search("x") == []


def test_pdf_pages_are_one_based_and_chunks_never_span_pages(data):
    body = "This sentence pads the page so that it needs more than one chunk of text to hold it. " * 25
    pages = [f"Marker alphaword opens page one. {body}", "", f"Marker gammaword opens page three. {body}"]
    doc = store.add_document(_pdf(data / "manual.pdf", pages))
    assert doc["pages"] == 3 and doc["chunks"] >= 4
    with sqlite3.connect(data / "rag.sqlite") as con:
        rows = con.execute("SELECT page, text FROM chunks").fetchall()
    assert {page for page, _ in rows} == {1, 3}
    assert all(len(text) <= store.CHUNK_CHARS for _, text in rows)
    page_text = {1: " ".join(pages[0].split()), 3: " ".join(pages[2].split())}
    assert all(text in page_text[page] for page, text in rows)  # each chunk is a slice of exactly its own page
    hit = store.keyword_search("gammaword")[0]
    assert hit.page == 3 and hit.label() == "manual.pdf, p. 3"


def test_keyword_search(data):
    ids = _corpus(data)
    assert store.keyword_search("chloroplasts")[0].id.startswith("doc:")
    assert "chloroplasts" in store.keyword_search("chloroplasts")[0].text
    assert len(store.keyword_search('"foo" AND (bar* OR -')) == 3  # operators become plain words ("and" is in all)
    assert store.keyword_search('Eiffel" NEAR(*')[0].source == "tower.txt" and store.keyword_search("") == []
    assert store.keyword_search("_ ^ café 日本語") == []
    assert store.keyword_search("chloroplasts", doc_ids=[ids["tower"]]) == []


def test_dense_search(data):
    ids = _corpus(data)
    top = store.dense_search("how do plants make food from light", k=3)
    assert top[0].source == "plants.txt" and len(top) == 3 and top[0].score > top[1].score
    assert [c.source for c in store.dense_search("plants", doc_ids=[ids["tower"]])] == ["tower.txt"]


def test_hybrid_search(data):
    ids = _corpus(data)
    top = store.hybrid_search(["my phone is frozen", "how do I force restart my iPhone"])
    assert top[0].source == "restart.txt" and top[0].score >= store.RERANK_MIN
    assert store.hybrid_search("who won the 2018 football world cup") == []
    assert store.hybrid_search("force restart iPhone", doc_ids=[ids["plants"]]) == []


def test_web_chunks_round_trip(data):
    web = Chunk("web:abc123def456", "Passage text.", "https://example.com/a", title="Example")
    store.save_web_chunks([web])
    assert store.get_chunk("web:abc123def456") == web
    assert store.get_chunk("web:unknown") is None
    assert store.get_chunk("doc:999") is None and store.get_chunk("nonsense") is None
    doc_id = _corpus(data)["tower"]
    found = store.keyword_search("Eiffel", doc_ids=[doc_id])[0]
    assert store.get_chunk(found.id) == Chunk(found.id, found.text, "tower.txt", None, "", 0.0)
