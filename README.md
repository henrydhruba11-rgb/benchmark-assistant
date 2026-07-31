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
| **Analyze others' benchmarks** | 5-part breakdown framework | Structured analysis notes |

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
      SKILL.md                    # entry: menu, audience inference, routing, grounding, boundaries
      references/
        knowledge-map.md          # topic -> source ID + section index
        design-principles.md      # 16 cross-source design principles
        benchmarks.md             # common benchmark quick-reference (LLM + agent)
      playbooks/
        build.md                  # build mode: 10-step walkthrough
        review.md                 # review mode: 9-dimension checklist
        analyze.md                # analyze mode: 5-part framework
      sources/                    # 5 normalized reference docs (read-only .md)
  docs/                           # design spec, implementation plan, verification record
```

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

The two surveys (`chang-survey`, `yehudai-survey`) were converted from PDF via pypdf as a fallback; their prose has space-joining artifacts (e.g. `a n dhow`) but section headings are intact and locatable. Section-level citations are unaffected; on-demand quotes are lightly cleaned.

## Acknowledgments & Licenses

This skill distills methodology from the following reference materials. Four are bundled under their **original licenses** (see [NOTICE.md](NOTICE.md)); the repo's MIT license covers only the skill's original files (`SKILL.md`, `references/`, `playbooks/`).

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
