# AGENTS.md

This repository packages **benchmark-assistant**, a methodology-advisor skill for LLM/agent benchmark (evaluation) work. It is primarily a Claude Code plugin but is also usable by other coding agents (Codex, Gemini CLI, opencode, etc.).

## What it does

Guides building, reviewing, and analyzing benchmarks, grounded in 5 reference docs under `sources/` with traceable citations (source ID + section). It does **not** write eval code, run evaluations, or call model APIs - only methodology guidance and document deliverables.

## How to use it (any agent)

The skill content lives at `skills/benchmark-assistant/`. When the user asks to build, review, or analyze a benchmark (评估 / benchmark / eval):

1. Read `skills/benchmark-assistant/SKILL.md` and follow its instructions.
2. It shows a 3-mode menu (build / review / analyze) and infers audience expertise once at startup.
3. As directed, read `references/` (knowledge-map, design-principles, benchmarks, glossary), `playbooks/` (build / review / analyze), and `sources/` (5 reference docs) - all paths relative to the skill directory.
4. Cite key claims as 「source ID + section」; quote original text from `sources/<id>.md` on demand. If a topic is outside `sources/`, say so rather than fabricating.

## Agent-specific entry points

- **Claude Code**: plugin at `.claude-plugin/` (auto-discovers `skills/`); invoke `/benchmark-assistant`.
- **Codex**: plugin manifest at `.codex-plugin/plugin.json` (points to `./skills/`).
- **Gemini CLI**: `GEMINI.md` imports `skills/benchmark-assistant/SKILL.md` via `@`; see `gemini-extension.json`.
- **Others**: follow "How to use it" above; this AGENTS.md is the generic entry.

## Development (repo tooling)

`tools/` (stdlib-only Python, run from repo root) — all three run in CI on every push/PR:

- `python tools/check_citations.py` — every 「source ID + §section + line」 reference in `SKILL.md` / `playbooks/` / `references/` must resolve against `sources/`; also guards principle numbering (1-16) and playbook structures. **Run this after any edit to those files.** Re-anchor mismatched line refs it reports.
- `python tools/check_snapshot_sync.py` — snapshots must match `tools/sources-registry.json` hashes; locally also compares against the gitignored originals. After an intentional re-normalization: `--update`.
- `python tools/check_versions.py` — `plugin.json` / `marketplace.json` version parity.
- `tools/reconvert_surveys.py` — re-converts the two survey PDFs via pymupdf4llm (venv at `tools/.venv/`). chang-survey derives ONLY from the arXiv preprint (CC-BY); the repo-root Zotero PDF is the ACM version and must not be bundled.

`evals/` holds the golden-scenario self-eval suite (12 scenarios, each mapped to a spec section). After changing `SKILL.md` / `playbooks/` behavior, run `python tools/run_evals.py --core` (needs a local agent CLI); run the full suite before releases. Protocol: `evals/README.md`.

`tools/sources-registry.json` is the machine-readable source of truth for the knowledge base (IDs, snapshot paths/hashes, originals, licenses, citation aliases). Adding a new reference doc = registry entry + snapshot file.
