#!/usr/bin/env bash
# fetch-sources.sh - OPTIONAL: re-fetch chang-survey.md from arXiv.
# chang-survey.md is already bundled (arXiv author preprint, CC-BY 4.0). This script is only
# needed if you want to regenerate it. The other 4 sources are bundled under their original
# licenses (see NOTICE.md). NOTE: the repo-root Zotero PDF is the ACM published version and
# must NOT be bundled - always convert from the arXiv preprint (tools/sources-registry.json).
# Run: bash scripts/fetch-sources.sh [--force]   (paths resolve relative to this script)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/../sources"
TOOLS="$HERE/../../../tools"
PDF="$TOOLS/_conv/chang-arxiv.pdf"

if [ -s "$SRC/chang-survey.md" ]; then
  printf 'chang-survey.md already present (%s lines). Re-run with --force to re-fetch.\n' "$(wc -l < "$SRC/chang-survey.md")"
  [ "${1:-}" = "--force" ] || exit 0
fi

mkdir -p "$TOOLS/_conv"
printf '[chang-survey] downloading arXiv:2307.03109 ...\n'
if ! curl -fsSL -o "$PDF" https://arxiv.org/pdf/2307.03109 2>/dev/null; then
  printf 'FAIL: could not download from arXiv (network?). Download manually from https://arxiv.org/abs/2307.03109\n'
  printf 'and place the PDF at tools/_conv/chang-arxiv.pdf, then re-run.\n'
  exit 1
fi

# prefer the repo venv with pymupdf4llm (clean markdown); fall back to pypdf (space-joining artifacts)
PY=python
for cand in "$TOOLS/.venv/Scripts/python.exe" "$TOOLS/.venv/bin/python"; do
  [ -x "$cand" ] && PY="$cand" && break
done
if "$PY" -c "import pymupdf4llm" 2>/dev/null; then
  "$PY" "$TOOLS/reconvert_surveys.py" --apply
else
  printf '[chang-survey] pymupdf4llm not found (python -m venv tools/.venv && pip install pymupdf4llm); using pypdf fallback.\n'
  "$PY" -c "import pypdf" 2>/dev/null || "$PY" -m pip install -q pypdf 2>/dev/null
  "$PY" -c "from pypdf import PdfReader; import pathlib; r=PdfReader(open(r'$PDF','rb')); pathlib.Path(r'$SRC/chang-survey.md').write_text(''.join('\n\n<!-- page %d -->\n'%i+(p.extract_text() or '') for i,p in enumerate(r.pages,1)),encoding='utf-8')"
  [ -s "$SRC/chang-survey.md" ] && printf 'OK: chang-survey.md (%s lines, pypdf fallback - has space-joining artifacts).\n' "$(wc -l < "$SRC/chang-survey.md")" || { printf 'FAIL: conversion produced empty file.\n'; exit 1; }
fi

printf 'Next: python tools/check_citations.py   # re-anchor any shifted line refs\n'
printf 'Then: python tools/check_snapshot_sync.py --update   # re-record snapshot hash\n'
