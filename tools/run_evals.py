#!/usr/bin/env python3
"""run_evals.py - run the golden-scenario suite against the skill.

For each scenario in evals/scenarios.json, spawns a fresh agent CLI session that reads
SKILL.md and responds to the scenario prompt, then applies the deterministic checks
(must_contain_all / must_contain_any / must_not_contain). `manual` items are printed for
human review - they never fail the run, but the release protocol (evals/README.md)
requires eyeballing them.

Usage:
  python tools/run_evals.py                 # full suite
  python tools/run_evals.py --core          # 5-scenario smoke set (S01,S03,S05,S08,S09)
  python tools/run_evals.py --only S03,S09  # subset
  python tools/run_evals.py --cmd "claude -p --dangerously-skip-permissions"  # other agent CLI
  python tools/run_evals.py --dry-run       # print the composed prompts, run nothing

Outputs evals/last-run/<id>.txt (RAW responses, exactly as the CLI printed them) for
manual review; deterministic checks run on a lightly cleaned copy (CLI banner/progress
lines stripped). After the suite, the working tree is diffed for files the sub-agent
may have written despite the no-write instruction. Exit 1 if any deterministic check fails.

Note for --cmd on Windows: npm-installed CLIs are often `*.cmd` shims, which list-form
subprocess cannot execute - use the real .exe path or `{prompt}` placeholder form.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "benchmark-assistant"
SCENARIOS = REPO_ROOT / "evals" / "scenarios.json"
OUT_DIR = REPO_ROOT / "evals" / "last-run"
CORE = ["S01", "S03", "S05", "S08", "S09"]

PREAMBLE = (
    '先阅读 "{skill}/SKILL.md" 并严格遵循其中的全部指令(可按需阅读它引用的 '
    "playbooks/、references/、sources/ 文件)。你现在就是这个 skill。"
    "直接把回应打印出来,不要创建或修改任何文件。回应以下用户输入:"
)


def compose_prompt(scenario: dict) -> str:
    return PREAMBLE.format(skill=SKILL_DIR.as_posix()) + "\n\n" + scenario["prompt"]


def clean_output(text: str, cli_name: str) -> str:
    """Strip CLI chrome for judging. kimi print mode adds a version banner, `• ` progress
    bullets and a session footer; the `• ` rule is kimi-only so other CLIs' legitimate
    bullet lines survive."""
    out = []
    for ln in text.split("\n"):
        if ln.startswith("kimi version") or ln.startswith("To resume this session:"):
            continue
        if cli_name == "kimi" and ln.lstrip().startswith("• "):
            continue
        out.append(ln)
    return "\n".join(out).strip()


def run_one(cli: list[str], scenario: dict, timeout: int) -> tuple[str, str, str]:
    """Returns (raw_response, cleaned_response, error)."""
    prompt = compose_prompt(scenario)
    cmd = [prompt if part == "{prompt}" else part for part in cli]
    if "{prompt}" not in cli:
        cmd = cli + [prompt]
    try:
        proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired:
        return "", "", f"timeout after {timeout}s"
    except FileNotFoundError:
        return "", "", f"CLI not found: {cli[0]} (on Windows, npm *.cmd shims need the real .exe path)"
    if proc.returncode != 0:
        return "", "", f"exit {proc.returncode}: {proc.stderr.strip()[:300]}"
    raw = proc.stdout.strip()
    return raw, clean_output(raw, Path(cli[0]).stem.lower()), ""


def check(response: str, expect: dict) -> list[str]:
    failures = []
    for s in expect.get("must_contain_all", []):
        if s not in response:
            failures.append(f"missing (all): {s!r}")
    for group in expect.get("must_contain_any", []):
        if not any(s in response for s in group):
            failures.append(f"missing (any of): {group}")
    for s in expect.get("must_not_contain", []):
        if s in response:
            failures.append(f"forbidden present: {s!r}")
    return failures


def git_porcelain() -> str:
    return subprocess.run(["git", "status", "--porcelain"], cwd=REPO_ROOT,
                          capture_output=True, text=True).stdout


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--core", action="store_true", help="run only the 5-scenario smoke set")
    ap.add_argument("--only", help="comma-separated scenario ids")
    ap.add_argument("--cmd", default="kimi -p",
                    help="agent CLI; the prompt is appended at the end, or inserted at a "
                         "{prompt} placeholder (default: kimi -p; alternative: "
                         "claude -p --dangerously-skip-permissions)")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    suite = json.loads(SCENARIOS.read_text(encoding="utf-8"))["scenarios"]
    if args.only:
        wanted = {s.strip() for s in args.only.split(",")}
        suite = [s for s in suite if s["id"] in wanted]
    elif args.core:
        suite = [s for s in suite if s["id"] in CORE]
    if not suite:
        print("no scenarios selected")
        return 2

    if args.dry_run:
        for s in suite:
            print(f"===== {s['id']} {s['title']} =====\n{compose_prompt(s)}\n")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cli = args.cmd.split()
    tree_before = git_porcelain()
    failed = 0
    for s in suite:
        t0 = time.time()
        raw, cleaned, error = run_one(cli, s, args.timeout)
        (OUT_DIR / f"{s['id']}.txt").write_text(raw or f"<{error}>", encoding="utf-8")
        elapsed = time.time() - t0
        if error:
            failed += 1
            print(f"[FAIL] {s['id']} {s['title']} ({elapsed:.0f}s) - {error}")
            continue
        failures = check(cleaned, s["expect"])
        status = "PASS" if not failures else "FAIL"
        failed += bool(failures)
        print(f"[{status}] {s['id']} {s['title']} ({elapsed:.0f}s)")
        for f in failures:
            print(f"       {f}")
        for m in s["expect"].get("manual", []):
            print(f"       [manual review] {m}")

    pollution = git_porcelain()
    if pollution != tree_before:
        new = [ln for ln in pollution.splitlines() if ln not in tree_before.splitlines()]
        print(f"\n[WARN] working tree changed during the run (sub-agent wrote files?):")
        for ln in new:
            print(f"       {ln}")

    print(f"\n{len(suite)} scenario(s), {failed} failed. Raw responses: evals/last-run/")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
