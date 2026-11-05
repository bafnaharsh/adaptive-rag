"""
End-to-end eval on the iPhone manuals: ingest data/manuals/*.pdf (idempotent), run every question in
eval/iphone_questions.yaml through the full pipeline (graph_builder.answer) with the configured LLM backend, and
score routing, grounding and citations. Writes eval/REPORT.md and eval/results.json.

    .venv/Scripts/python.exe scripts/run_eval.py [--only id1,id2]
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.config import settings  # noqa: E402
from src.rag import store  # noqa: E402
from src.rag.graph_builder import answer  # noqa: E402


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower())


def score(q: dict, r: dict) -> dict:
    cites = r["citations"]
    ok_cites = [c for c in cites if c.get("verified")]
    checks = {"tier": r["tier"] in q["expected_tiers"]}
    if q["category"] in ("doc", "hybrid"):
        pages = set(q["pages"])
        on_doc = [c for c in ok_cites if c.get("source") == q["doc"]]
        checks["verified"] = r["verified"]
        checks["page_exact"] = any(c.get("page") in pages for c in on_doc)
        checks["page_pm1"] = any(c.get("page") and min(abs(c["page"] - p) for p in pages) <= 1 for c in on_doc)
        checks["keywords"] = sum(norm(k) in norm(r["answer"]) for k in q["keywords"]) / len(q["keywords"])
    elif q["category"] == "web":
        checks["verified"] = r["verified"]
        checks["url_cited"] = any((c.get("url") or "").startswith("http") for c in ok_cites)
    passed = all(v is True or (isinstance(v, float) and v >= 0.5) for k, v in checks.items() if k != "page_exact")
    return {"checks": checks, "passed": passed}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252, which has no ✓/⚠

    for pdf in sorted((ROOT / "data" / "manuals").glob("*.pdf")):
        t = time.time()
        d = store.add_document(pdf, description=pdf.stem.replace("_", " "))
        print(f"{d['status']}: {d['name']} {d['pages']} pages, {d['chunks']} chunks ({time.time() - t:.0f}s)")

    questions = yaml.safe_load((ROOT / "eval" / "iphone_questions.yaml").read_text(encoding="utf-8"))
    if args.only:
        questions = [q for q in questions if q["id"] in args.only.split(",")]

    rows = []
    for q in questions:
        t = time.time()
        r = answer(q["question"])
        took = time.time() - t
        s = score(q, r)
        rows.append({**q, "result": r, **s, "seconds": round(took, 1)})
        cited = ", ".join(f"{c['label']}{'✓' if c.get('verified') else '⚠'}" for c in r["citations"]) or "-"
        print(f"[{'PASS' if s['passed'] else 'FAIL'}] {q['id']} tier={r['tier']} {took:.0f}s cites={cited} {s['checks']}")

    (ROOT / "eval" / "results.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    passed = sum(r["passed"] for r in rows)
    lines = [
        "# iPhone manuals: end-to-end eval",
        "",
        f"LLM backend: `{settings.LLM_MODEL}` (model `{settings.CLI_MODEL or 'CLI default'}`). "
        f"Passed **{passed}/{len(rows)}**. Median latency {sorted(r['seconds'] for r in rows)[len(rows) // 2]} s.",
        "",
        "| id | category | expected | tier | verified citations | page hit | keywords | s | result |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        c, res = r["checks"], r["result"]
        nv = sum(x.get("verified", False) for x in res["citations"])
        page = "exact" if c.get("page_exact") else ("±1" if c.get("page_pm1") else ("miss" if "page_pm1" in c else "-"))
        kw = f"{c['keywords']:.0%}" if "keywords" in c else "-"
        lines.append(f"| {r['id']} | {r['category']} | {'/'.join(r['expected_tiers'])} | {res['tier']} | "
                     f"{nv}/{len(res['citations'])} | {page} | {kw} | {r['seconds']} | "
                     f"{'PASS' if r['passed'] else 'FAIL'} |")
    lines += ["", "## Answers", ""]
    for r in rows:
        lines += [f"### {r['id']}: {r['question']}", "", f"Tier: {r['result']['tier']}", "",
                  r["result"]["rendered"], "", "<details><summary>Trace</summary>", "",
                  *[f"- {t}" for t in r["result"]["trace"]], "", "</details>", ""]
    (ROOT / "eval" / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\n{passed}/{len(rows)} passed -> eval/REPORT.md")


if __name__ == "__main__":
    main()
