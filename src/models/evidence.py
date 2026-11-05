"""
One piece of evidence: a document chunk (always from a single PDF page) or a passage of a web page.
"""

from dataclasses import asdict, dataclass


@dataclass
class Chunk:
    id: str                  # "doc:<int>" for indexed document chunks, "web:<hex>" for web passages
    text: str
    source: str              # document file name, or the page URL for web
    page: int | None = None  # 1-based PDF page (as shown in a PDF viewer); None for web and plain text
    title: str = ""          # web page title, or the document description
    score: float = 0.0       # retrieval/rerank score, higher is better (only comparable within one result list)

    def to_dict(self) -> dict:
        return asdict(self)

    def label(self) -> str:
        """Human citation target: 'iphone_user_guide.pdf, p. 42' or the URL."""
        return f"{self.source}, p. {self.page}" if self.page else self.source
