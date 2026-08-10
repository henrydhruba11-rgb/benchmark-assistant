# benchmark-assistant

**English** | [中文](README.zh.md)

> A Claude Code skill that guides building, reviewing, and analyzing LLM/agent benchmarks — grounded in 5 reference docs with traceable citations.

`benchmark-assistant` is a methodology advisor for LLM/agent benchmark (evaluation) work. Every answer is grounded in 5 reference documents under `sources/`; key claims cite 「source ID + section」 and original text can be quoted on demand. It does **not** write eval code, run evaluations, or call model APIs — it gives traceable methodology guidance and document deliverables.

## Three modes

On invocation it shows a menu; audience expertise is inferred once at startup and term depth adapts accordingly.

| Mode | What it does | Deliverable |
|---|---|---|
| **Build a benchmark** | 10-step walkthrough (eval-object decoupling → capability dims → dataset design → environment → metrics → scoring → stats/cost → QC) | Evaluation plan doc (with dataset spec & Rubric template) |
| **Review your project** | 9-dimension checklist diagnosis | Severity-sorted issue list (🔴🟠🟡) |
| **Analyze others' benchmarks** | 5-part breakdown framework (L0–L3 walkthrough, then methodology judgment) | Structured analysis notes (with plain-language "3-minute version" + ASCII architecture/pipeline diagrams) |

## Usage examples

**Build a benchmark**
```
You: I want to build a benchmark for my customer-service agent.
Skill: (mode 1) walks 10 decisions — what to evaluate (LLM vs agent vs harness),
       capability dimensions, dataset design (clarity vs openness, contamination,
       verifiability), environment, metrics (Pass@k vs Pass^k), scoring (Rubric),
       statistics & cost, quality control — and writes an evaluation-plan doc with
       a dataset spec and Rubric template.
```

**Review your project**
```
You: Review my agent eval: 20 cases, GPT as judge scoring 1-5, no calibration.
Skill: (mode 2) diagnoses 9 dimensions, flags "small sample", "judge uncalibrated",
       "Pass@k/Pass^k misuse", cites sources, outputs a severity-sorted issue list.
```
A real mode-2 output on exactly this scenario: [docs/examples/review-report-example.md](docs/examples/review-report-example.md).

**Analyze an existing benchmark**
```
You: Walk me through the GAIA benchmark.
Skill: (mode 3) looks up references/benchmarks.md, breaks GAIA into 5 parts
       (what it tests, how, design tradeoffs, limits, what to borrow), cites sources.
```

**Ask for evidence**
```
You: What's the basis for that?
Skill: Reads sources/<id>.md and quotes the original passage, cited as
       「source ID + section」.
```

**Out of scope**
```
You: Write me a Python script to run the eval.
Skill: Declines (no code / no eval execution / no API calls); instead offers
       methodology or pseudocode-level design.
```

## Installation

### As a Claude Code plugin (recommended)

```bash
/plugin marketplace add henrydhruba11-rgb/benchmark-assistant
/plugin install benchmark-assistant@benchmark-assistant-marketplace
```

### Manual copy (no plugin mechanism)

```bash
git clone https://github.com/henrydhruba11-rgb/benchmark-assistant
# User-level (global)
cp -r benchmark-assistant/skills/benchmark-assistant ~/.claude/skills/
# Or project-level
cp -r benchmark-assistant/skills/benchmark-assistant <project>/.claude/skills/
```

Restart Claude Code, then say “help me build / review / analyze a benchmark” to auto-trigger, or invoke `/benchmark-assistant` directly.

Works with **Codex**, **Gemini CLI**, and other agents too — adapter files (`.codex-plugin/`, `GEMINI.md`, `AGENTS.md`) are included; see [AGENTS.md](AGENTS.md).

## Structure

```
benchmark-assistant/              # repo root = plugin
  .claude-plugin/
    plugin.json                   # plugin manifest
    marketplace.json              # marketplace listing
  skills/
    benchmark-assistant/          # the skill
      SKILL.md                    # entry: menu, audience inference + teaching protocol, routing, grounding, boundaries
      references/
        knowledge-map.md          # topic -> source ID + section index
        design-principles.md      # 16 cross-source design principles
        benchmarks.md             # common benchmark quick-reference (LLM + agent)
        glossary.md               # plain-language term definitions for novice/intermediate audiences
      playbooks/
        build.md                  # build mode: 10-step walkthrough
        review.md                 # review mode: 9-dimension checklist
        analyze.md                # analyze mode: 5-part framework
      scripts/
        fetch-sources.sh          # optional re-fetch of chang-survey from arXiv
      sources/                    # 5 normalized reference docs (read-only .md) + README.md (licenses & snapshot-sync note)
  tools/                          # repo maintenance (CI): citation-graph lint, snapshot-sync check,
                                  # manifest-version check, survey re-conversion, sources-registry.json
  evals/                          # golden-scenario self-eval suite (scenarios.json + run protocol)
  docs/                           # design spec, implementation plan, verification record
```

## Quality gates (CI)

Every push/PR runs three checks (`tools/`, stdlib-only Python):

- `check_citations.py` — every 「source ID + §section + line」 reference in `SKILL.md` / `playbooks/` / `references/` must resolve against `sources/` (hundreds of checks; tolerant of conversion artifacts; also guards the principle numbering 1-16 and playbook structures).
- `check_snapshot_sync.py` — `sources/` snapshots must match the registry's recorded hashes, and (on the maintainer's machine, where the gitignored originals live) must not drift from the originals.
- `check_versions.py` — `plugin.json` and `marketplace.json` versions must agree.

The skill's behavior is covered by a golden-scenario suite (`evals/`, 12 scenarios each mapped to a spec section): run `python tools/run_evals.py --core` for a 5-scenario smoke set — needs a local agent CLI, so it gates releases rather than CI. See `evals/README.md`.

## Knowledge sources

All knowledge comes from 5 docs normalized to `.md` under `sources/`:

| Source ID | Content |
|---|---|
| `chapter6` | Agent evaluation (Chinese textbook chapter) |
| `chapter12` | Agent evaluation (Chinese textbook chapter) |
| `guidebook` | The LLM Evaluation Guidebook (Hugging Face) |
| `chang-survey` | A Survey on Evaluation of Large Language Models (Chang et al., 2024) |
| `yehudai-survey` | A Survey on Evaluation of LLM-based Agents (Yehudai et al., 2026) |

Citations always use source ID + section, never filenames or author names.

## Boundaries

- No eval code, no evaluation execution, no model API calls.
- Declines code/eval requests; offers methodology or pseudocode-level design instead.
- Says “not covered by references” (rather than fabricating) for topics outside `sources/`.

## Known limitations

The two surveys (`chang-survey`, `yehudai-survey`) are converted from PDF via `pymupdf4llm` (clean headings, no space-joining artifacts). Table regions are still lossy (row text may be flattened); section-level citations are verified by `tools/check_citations.py` in CI.

## Acknowledgments & Licenses

This skill distills methodology from the following reference materials. All five are bundled under their **original licenses** (see [NOTICE.md](NOTICE.md)); the repo's MIT license covers only the skill's original files (`SKILL.md`, `references/`, `playbooks/`).

| ID | Work | License | Bundled? |
|---|---|---|---|
| `chapter6` | Agent evaluation chapter ([bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book)) | Apache-2.0 | ✅ |
| `chapter12` | Agent performance evaluation, HelloAgents ([datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)) | CC BY-NC-SA 4.0 | ✅ |
| `guidebook` | The LLM Evaluation Guidebook, Fourrier et al. (Hugging Face) | CC BY-NC-SA 4.0 | ✅ |
| `yehudai-survey` | A Survey on Evaluation of LLM-based Agents, Yehudai et al. (ACL 2026) | CC-BY 4.0 | ✅ |
| `chang-survey` | A Survey on Evaluation of Large Language Models, Chang et al. (2024) | CC-BY 4.0 (arXiv preprint) | ✅ |

Credit for the underlying methodology belongs to the original authors.

## License

[MIT](LICENSE)
