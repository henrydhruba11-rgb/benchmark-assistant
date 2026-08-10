#!/usr/bin/env python3
"""check_versions.py - verify ALL plugin manifests carry the same version.

Four manifests exist for different agent hosts:
  .claude-plugin/plugin.json        (.version)
  .claude-plugin/marketplace.json   (.plugins[0].version)
  .codex-plugin/plugin.json         (.version)
  gemini-extension.json             (.version)
A release means the same version everywhere; a manifest left behind ships a stale
package to that host's users (this exact blind spot shipped in v0.2.0).

Exit code 1 on any mismatch.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def load() -> dict[str, tuple[str, str]]:
    """manifest path -> (name, version)"""
    out = {}
    plugin = json.loads((REPO_ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    out[".claude-plugin/plugin.json"] = (plugin["name"], plugin["version"])
    marketplace = json.loads((REPO_ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    entries = marketplace.get("plugins", [])
    if len(entries) != 1:
        raise ValueError(f"marketplace.json should list exactly 1 plugin, got {len(entries)}")
    out[".claude-plugin/marketplace.json"] = (entries[0]["name"], entries[0]["version"])
    codex = json.loads((REPO_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    out[".codex-plugin/plugin.json"] = (codex["name"], codex["version"])
    gemini = json.loads((REPO_ROOT / "gemini-extension.json").read_text(encoding="utf-8"))
    out["gemini-extension.json"] = (gemini["name"], gemini["version"])
    return out


def main() -> int:
    manifests = load()
    names = {n for n, _ in manifests.values()}
    versions = {v for _, v in manifests.values()}
    for path, (name, version) in manifests.items():
        print(f"       {path}: {name} v{version}")
    failures = 0
    if len(names) != 1:
        print(f"[FAIL] name mismatch across manifests: {sorted(names)}")
        failures += 1
    if len(versions) != 1:
        print(f"[FAIL] version mismatch across manifests: {sorted(versions)}")
        failures += 1
    if not failures:
        print(f"[OK]   all 4 manifests agree: {names.pop()} v{versions.pop()}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
