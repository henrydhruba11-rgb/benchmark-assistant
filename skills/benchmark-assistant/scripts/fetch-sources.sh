#!/usr/bin/env bash
# fetch-sources.sh - OPTIONAL: re-fetch chang-survey.md from arXiv.
# chang-survey.md is already bundled (arXiv author preprint, CC-BY 4.0). This script is only
# needed if you want to regenerate it. The other 4 sources are bundled under their original
# licenses (see NOTICE.md). NOTE: the repo-root Zotero PDF is the ACM published version and
# must NOT be bundled - always convert from the arXiv preprint (tools/sources-registry.json).
#
# This script only works inside the full repo (it needs tools/). If you installed the skill
# standalone (copied skills/benchmark-assistant/), the bundled chang-survey.md works out of
# the box and there is nothing to re-fetch - new conversions happen in the repo.
#
# Run: bash scripts/fetch-sources.sh [--force]   (paths resolve relative to this script)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/../sources"
TOOLS="$HERE/../../../tools"
PDF="$TOOLS/_conv/chang-arxiv.pdf"
OUT_TMP="$SRC/chang-survey.md.tmp"

if [ ! -d "$TOOLS" ]; then
  printf 'Nothing to do: this script only works inside the full benchmark-assistant repo\n'
  printf '(tools/ not found at %s). The bundled sources/ work out of the box.\n' "$TOOLS"
  exit 0
fi

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

PY=python
for cand in "$TOOLS/.venv/Scripts/python.exe" "$TOOLS/.venv/bin/python"; do
  [ -x "$cand" ] && PY="$cand" && break
done

if "$PY" -c "import pymupdf4llm" 2>/dev/null; then
  "$PY" "$TOOLS/reconvert_surveys.py" --only chang-survey --apply
elif "$PY" -c "import pypdf" 2>/dev/null; then
  printf '[chang-survey] pymupdf4llm not found; using pypdf fallback (space-joining artifacts).\n'
  printf '             For clean output: python -m venv tools/.venv && tools/.venv/Scripts/pip install pymupdf4llm\n'
  "$PY" -c "from pypdf import PdfReader; import pathlib; r=PdfReader(open(r'$PDF','rb')); pathlib.Path(r'$OUT_TMP').write_text(''.join('\n\n<!-- page %d -->\n'%i+(p.extract_text() or '') for i,p in enumerate(r.pages,1)),encoding='utf-8')"
  if [ -s "$OUT_TMP" ]; then
    mv "$OUT_TMP" "$SRC/chang-survey.md"
    printf 'OK: chang-survey.md (%s lines, pypdf fallback).\n' "$(wc -l < "$SRC/chang-survey.md")"
  else
    rm -f "$OUT_TMP"
    printf 'FAIL: conversion produced empty file; existing chang-survey.md left untouched.\n'
    exit 1
  fi
else
  printf 'FAIL: no converter available. Set one up first:\n'
  printf '  python -m venv tools/.venv && tools/.venv/Scripts/pip install pymupdf4llm\n'
  printf '(existing chang-survey.md left untouched)\n'
  exit 1
fi

printf 'Next: python tools/check_citations.py   # re-anchor any shifted line refs\n'
printf 'Then: python tools/check_snapshot_sync.py --update   # re-record snapshot hash\n'
