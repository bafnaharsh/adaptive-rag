"""Verify every doc/hybrid question's keywords appear on its listed PDF pages."""
import re
import sys
from pathlib import Path

import pypdf
import yaml

ROOT = Path(__file__).resolve().parent.parent
norm = lambda s: re.sub(r"\s+", " ", s).lower()
questions = yaml.safe_load((ROOT / "eval" / "iphone_questions.yaml").read_text(encoding="utf-8"))
readers, bad, n = {}, 0, 0
for q in questions:
    if q["category"] not in ("doc", "hybrid"):
        continue
    n += 1
    try:
        r = readers.setdefault(q["doc"], pypdf.PdfReader(ROOT / "data" / "manuals" / q["doc"]))
        text = norm(" ".join(r.pages[p - 1].extract_text() or "" for p in q["pages"]))
        missing = [k for k in q["keywords"] if norm(k) not in text]
    except Exception as e:  # missing file, bad page number...
        missing = [f"error: {e!r}"]
    if not q["pages"] or missing:
        bad += 1
        print(f"FAIL {q['id']}: pages={q['pages']} missing={missing}")
if bad:
    sys.exit(1)
print(f"all {n} doc questions verified")
