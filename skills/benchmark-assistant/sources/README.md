# Sources

The skill reads 5 reference docs from this directory as `sources/<id>.md`.

## Bundled (4 of 5)

Four sources are bundled with this repo under their **original licenses** (see repo-root [NOTICE.md](../../NOTICE.md)):

| ID | File | License |
|---|---|---|
| `chapter6` | `chapter6.md` | Apache-2.0 |
| `chapter12` | `chapter12.md` | CC BY-NC-SA 4.0 |
| `guidebook` | `guidebook.md` | CC BY-NC-SA 4.0 |
| `yehudai-survey` | `yehudai-survey.md` | CC-BY 4.0 |

## User-fetched (1 of 5)

`chang-survey` is **not bundled** (ACM-copyrighted; cannot be redistributed). Fetch the arXiv open-access preprint:

```bash
bash scripts/fetch-sources.sh
```

This downloads arXiv:2307.03109 (Chang et al., *A Survey on Evaluation of Large Language Models*) and converts it to `chang-survey.md` via `pypdf` (fallback; prose has space-joining artifacts but section headings are locatable). For higher fidelity, convert the PDF with a dedicated tool.

## Note on citations

`references/knowledge-map.md` cites sources by **section heading** and **line number**. Section headings resolve regardless of version; line numbers assume these specific files. The `chang-survey` line numbers were verified against the pypdf conversion - if you re-convert with a different tool, headings still match but line numbers may shift.
