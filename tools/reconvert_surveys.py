#!/usr/bin/env python3
"""reconvert_surveys.py - re-convert the two survey PDFs to markdown with pymupdf4llm.

The bundled chang-survey.md / yehudai-survey.md were converted with pypdf as a fallback
and have space-joining artifacts (e.g. `EV ALUATE`). pymupdf4llm produces proper markdown
(headings by font size, no garbling). Both surveys are CC-BY; originals live (gitignored)
at the repo root.

Usage (isolated env):
  python -m venv tools/.venv && tools/.venv/Scripts/pip install pymupdf4llm
  tools/.venv/Scripts/python tools/reconvert_surveys.py            # preview to tools/_conv/
  tools/.venv/Scripts/python tools/reconvert_surveys.py --apply    # overwrite sources/

After --apply: run `python tools/check_citations.py` to find line anchors that shifted,
re-anchor them in references/knowledge-map.md, then `python tools/check_snapshot_sync.py
--update` to re-record snapshot hashes.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "tools" / "_conv"

import pymupdf4llm  # noqa: E402


def main() -> int:
    apply = "--apply" in sys.argv
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    registry = json.loads((REPO_ROOT / "tools" / "sources-registry.json").read_text(encoding="utf-8"))

    for entry in registry["sources"]:
        if entry["sync_mode"] != "derived":
            continue
        sid = entry["id"]
        pdf = REPO_ROOT / entry["original"]
        if not pdf.exists() and entry.get("origin_url"):
            import urllib.request
            pdf.parent.mkdir(parents=True, exist_ok=True)
            print(f"[..]   {sid}: downloading {entry['origin_url']}")
            urllib.request.urlretrieve(entry["origin_url"], pdf)
        if not pdf.exists():
            print(f"[SKIP] {sid}: original PDF not found: {entry['original']}")
            continue
        md = pymupdf4llm.to_markdown(str(pdf))
        if not md.strip():
            print(f"[FAIL] {sid}: conversion produced empty output")
            continue
        dest = (REPO_ROOT / entry["snapshot"]) if apply else (OUT_DIR / f"{sid}.md")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(md, encoding="utf-8", newline="\n")
        headings = [ln for ln in md.split("\n") if ln.startswith("#")]
        print(f"[OK]   {sid}: {len(md.splitlines())} lines, {len(headings)} markdown headings "
              f"-> {dest.relative_to(REPO_ROOT)}" + (" (applied)" if apply else " (preview)"))
        for h in headings[:12]:
            print(f"       {h[:90]}")

    if not apply:
        print("\npreview only - inspect tools/_conv/*.md, then re-run with --apply to overwrite sources/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
