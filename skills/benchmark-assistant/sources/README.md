# Sources

The skill reads 5 reference docs from this directory as `sources/<id>.md`. **All 5 are bundled** under their original licenses (see repo-root [NOTICE.md](../../NOTICE.md)):

| ID | File | License |
|---|---|---|
| `chapter6` | `chapter6.md` | Apache-2.0 |
| `chapter12` | `chapter12.md` | CC BY-NC-SA 4.0 |
| `guidebook` | `guidebook.md` | CC BY-NC-SA 4.0 |
| `yehudai-survey` | `yehudai-survey.md` | CC-BY 4.0 |
| `chang-survey` | `chang-survey.md` | CC-BY 4.0 (arXiv author preprint, arXiv:2307.03109) |

`chang-survey.md` is the **arXiv author preprint** (CC-BY 4.0), not the ACM journal version (ACM-copyrighted, not redistributable). It was converted from the arXiv PDF via `pypdf` as a fallback, so prose has space-joining artifacts (e.g. `EV ALUATE`) but section headings are locatable.

## Re-fetching (optional)

`scripts/fetch-sources.sh` can re-fetch `chang-survey.md` from arXiv if you want to regenerate it (e.g. with a better PDF-to-markdown tool). Not required for normal use - the bundled copy works out of the box.

```bash
bash scripts/fetch-sources.sh --force
```

## Note on citations

`references/knowledge-map.md` cites sources by **section heading** and **line number** (verified against the bundled files). Section headings resolve regardless of conversion; line numbers assume the bundled versions. If you re-fetch/re-convert `chang-survey` with a different tool, headings still match but line numbers may shift.
