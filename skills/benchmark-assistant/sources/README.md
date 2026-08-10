# Sources

The skill reads 5 reference docs from this directory as `sources/<id>.md`. **All 5 are bundled** under their original licenses (see repo-root [NOTICE.md](../../NOTICE.md)):

| ID | File | License |
|---|---|---|
| `chapter6` | `chapter6.md` | Apache-2.0 |
| `chapter12` | `chapter12.md` | CC BY-NC-SA 4.0 |
| `guidebook` | `guidebook.md` | CC BY-NC-SA 4.0 |
| `yehudai-survey` | `yehudai-survey.md` | CC-BY 4.0 |
| `chang-survey` | `chang-survey.md` | CC-BY 4.0 (arXiv author preprint, arXiv:2307.03109) |

`chang-survey.md` is the **arXiv author preprint** (CC-BY 4.0), not the ACM journal version (ACM-copyrighted, not redistributable - do not convert from the repo-root Zotero PDF). Both surveys were converted with `pymupdf4llm` (clean markdown headings, no space-joining artifacts).

## Re-fetching / re-converting (optional)

Not required for normal use - the bundled copies work out of the box. To regenerate:

```bash
bash scripts/fetch-sources.sh --force                 # re-download arXiv PDF + convert chang-survey
tools/.venv/Scripts/python tools/reconvert_surveys.py # re-convert both surveys from their PDFs
```

## Note on citations

`references/knowledge-map.md` cites sources by **section heading** and **line number**. Both are continuously verified against the bundled files by `tools/check_citations.py` (CI). If you re-fetch/re-convert a source, re-run that script to find shifted line anchors, update `knowledge-map.md`, then `python tools/check_snapshot_sync.py --update` to re-record snapshot hashes.

## Keeping snapshots in sync

The files here are **snapshots**. The originals at the repo root (`chapter6.md`, `第十二章 智能体性能评估.md`, the guidebook copy, etc.) are living documents — after they are updated, re-run the normalization step (implementation plan Task 2 in `docs/superpowers/plans/`) to refresh this directory, otherwise citations and line numbers will silently drift out of date.
