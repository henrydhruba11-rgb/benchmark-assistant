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
