#!/usr/bin/env bash
# fetch-sources.sh - obtain chang-survey (the only non-bundled source) into sources/chang-survey.md
# The other 4 sources are bundled in the repo under their original licenses (see NOTICE.md).
# chang-survey is ACM-copyrighted in its published form, so we fetch the arXiv open-access preprint.
# Run: bash scripts/fetch-sources.sh   (paths resolve relative to this script)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/../sources"

if [ -s "$SRC/chang-survey.md" ]; then
  printf 'chang-survey.md already present (%s lines). Re-run with --force to re-fetch.\n' "$(wc -l < "$SRC/chang-survey.md")"
  [ "${1:-}" = "--force" ] || exit 0
fi

python -c "import pypdf" 2>/dev/null || pip install -q pypdf 2>/dev/null

TMP="$(mktemp -d)"
printf '[chang-survey] downloading arXiv:2307.03109 ...\n'
if curl -fsSL -o "$TMP/chang.pdf" https://arxiv.org/pdf/2307.03109 2>/dev/null; then
  python -c "from pypdf import PdfReader; import pathlib; r=PdfReader(open(r'$TMP/chang.pdf','rb')); pathlib.Path(r'$SRC/chang-survey.md').write_text(''.join('\n\n<!-- page %d -->\n'%i+(p.extract_text() or '') for i,p in enumerate(r.pages,1)),encoding='utf-8')"
  [ -s "$SRC/chang-survey.md" ] && printf 'OK: chang-survey.md (%s lines, pypdf fallback - has space-joining artifacts).\n' "$(wc -l < "$SRC/chang-survey.md")" || printf 'FAIL: conversion produced empty file.\n'
else
  printf 'FAIL: could not download from arXiv (network?). Download manually from https://arxiv.org/abs/2307.03109\n'
  printf 'and convert to sources/chang-survey.md (see sources/README.md).\n'
fi
rm -rf "$TMP"
