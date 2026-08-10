#!/usr/bin/env python3
"""check_snapshot_sync.py - verify sources/ snapshots are in sync with their originals.

Two layers of protection:

1. Snapshot integrity (always runs, CI-safe): every snapshot's sha256 must match
   `snapshot_sha256` in tools/sources-registry.json. The originals at the repo root are
   gitignored (see .gitignore "原始资料"), so CI clones don't have them - this layer is
   what prevents hand-edited snapshots from drifting away from the registry there.

2. Drift detection (only where originals exist, i.e. the maintainer's machine): compare
   each snapshot against its original, per `sync_mode`:
     exact-modulo-crlf : texts must be identical after CR stripping.
     normalized        : difflib similarity after stripping CR + U+FFFD must stay
                         >= baseline_ratio (a one-time manual cleanup makes exact
                         match impossible; the baseline records the known diff level).
     derived           : snapshot was converted from a PDF; content can't be diffed,
                         so the original PDF's sha256 must match the recorded one
                         (a replaced PDF means the snapshot must be regenerated).

Usage:
  python tools/check_snapshot_sync.py           # check, exit 1 on any failure
  python tools/check_snapshot_sync.py --update  # after intentional re-normalization:
                                                # re-record snapshot hashes (and report
                                                # current similarity ratios for baseline
                                                # tuning), then run the checks
"""

from __future__ import annotations

import difflib
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "tools" / "sources-registry.json"


def read_norm(path: Path, strip_mojibake: bool = False) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return text.replace("�", "") if strip_mojibake else text


def snapshot_hash(path: Path) -> str:
    return hashlib.sha256(read_norm(path).encode("utf-8")).hexdigest()


def main() -> int:
    update = "--update" in sys.argv
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows GBK console
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    failures = 0

    if update:
        for entry in registry["sources"]:
            snap = REPO_ROOT / entry["snapshot"]
            if snap.exists():
                entry["snapshot_sha256"] = snapshot_hash(snap)
        REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
        print("registry snapshot hashes updated\n")

    for entry in registry["sources"]:
        sid = entry["id"]
        snap = REPO_ROOT / entry["snapshot"]
        orig = REPO_ROOT / entry["original"]
        mode = entry["sync_mode"]

        if not snap.exists():
            print(f"[FAIL] {sid}: snapshot missing: {entry['snapshot']}")
            failures += 1
            continue

        # layer 1: snapshot integrity (always)
        digest = snapshot_hash(snap)
        if digest != entry.get("snapshot_sha256"):
            print(f"[FAIL] {sid}: snapshot changed vs registry hash. If this was an "
                  f"intentional re-normalization, run: python tools/check_snapshot_sync.py --update")
            failures += 1
            continue

        # layer 2: drift vs original (only where the original exists)
        if not orig.exists():
            print(f"[OK]   {sid}: snapshot hash match (original not in repo - drift check skipped)")
            continue

        if mode == "exact-modulo-crlf":
            if read_norm(snap) == read_norm(orig):
                print(f"[OK]   {sid}: snapshot identical to original (modulo line endings)")
            else:
                snap_lines = read_norm(snap).split("\n")
                orig_lines = read_norm(orig).split("\n")
                diff = sum(1 for a, b in zip(snap_lines, orig_lines) if a != b)
                diff += abs(len(snap_lines) - len(orig_lines))
                print(f"[FAIL] {sid}: original changed ({diff} line(s) differ). "
                      f"Re-run the normalization step to refresh {entry['snapshot']}.")
                failures += 1

        elif mode == "normalized":
            ratio = difflib.SequenceMatcher(
                None, read_norm(orig, strip_mojibake=True),
                read_norm(snap, strip_mojibake=True)
            ).ratio()
            baseline = entry["baseline_ratio"]
            note = f"similarity {ratio:.4f} vs baseline {baseline}"
            if ratio >= baseline:
                print(f"[OK]   {sid}: {note}")
            else:
                print(f"[FAIL] {sid}: {note}. Original drifted beyond the known cleanup - "
                      f"re-normalize (and re-tune baseline_ratio if the new level is intended).")
                failures += 1

        elif mode == "derived":
            digest = hashlib.sha256(orig.read_bytes()).hexdigest()
            if digest != entry["original_sha256"]:
                print(f"[FAIL] {sid}: original PDF sha256 changed "
                      f"({digest[:12]}... != recorded {entry['original_sha256'][:12]}...). "
                      f"Re-convert to refresh {entry['snapshot']}.")
                failures += 1
            else:
                print(f"[OK]   {sid}: original PDF unchanged (sha256 match)")

        else:
            print(f"[FAIL] {sid}: unknown sync_mode '{mode}' in registry")
            failures += 1

    print(f"\n{len(registry['sources'])} source(s), {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
