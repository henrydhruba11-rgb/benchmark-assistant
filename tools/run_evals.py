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
  python tools/run_evals.py --cmd "claude -p --dangerously-skip-permissions"  # 换 agent CLI
  python tools/run_evals.py --dry-run       # print the composed prompts, run nothing

Outputs evals/last-run/<id>.txt (raw responses) for manual review. Exit 1 if any
deterministic check fails.
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
    "先阅读 {skill}/SKILL.md 并严格遵循其中的全部指令(可按需阅读它引用的 "
    "playbooks/、references/、sources/ 文件)。你现在就是这个 skill。回应以下用户输入:"
)


def compose_prompt(scenario: dict) -> str:
    return PREAMBLE.format(skill=SKILL_DIR.as_posix()) + "\n\n" + scenario["prompt"]


def clean_output(text: str) -> str:
    """Strip CLI chrome (version banner, progress bullets, session footer) from print-mode output."""
    lines = text.split("\n")
    out = [ln for ln in lines
           if not ln.startswith("kimi version")
           and not ln.startswith("To resume this session:")
           and not ln.lstrip().startswith("• ")]
    return "\n".join(out).strip()


def run_one(cli: list[str], scenario: dict, timeout: int) -> tuple[str, str]:
    """Returns (response_text, error)."""
    prompt = compose_prompt(scenario)
    cmd = [prompt if part == "{prompt}" else part for part in cli]
    if "{prompt}" not in cli:
        cmd = cli + [prompt]
    try:
        proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired:
        return "", f"timeout after {timeout}s"
    except FileNotFoundError:
        return "", f"CLI not found: {cli[0]}"
    if proc.returncode != 0:
        return "", f"exit {proc.returncode}: {proc.stderr.strip()[:300]}"
    return clean_output(proc.stdout), ""


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
    failed = 0
    for s in suite:
        t0 = time.time()
        response, error = run_one(cli, s, args.timeout)
        (OUT_DIR / f"{s['id']}.txt").write_text(response or f"<{error}>", encoding="utf-8")
        elapsed = time.time() - t0
        if error:
            failed += 1
            print(f"[FAIL] {s['id']} {s['title']} ({elapsed:.0f}s) - {error}")
            continue
        failures = check(response, s["expect"])
        status = "PASS" if not failures else "FAIL"
        failed += bool(failures)
        print(f"[{status}] {s['id']} {s['title']} ({elapsed:.0f}s)")
        for f in failures:
            print(f"       {f}")
        for m in s["expect"].get("manual", []):
            print(f"       [manual review] {m}")

    print(f"\n{len(suite)} scenario(s), {failed} failed. Raw responses: evals/last-run/")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
