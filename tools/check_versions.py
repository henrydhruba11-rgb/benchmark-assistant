#!/usr/bin/env python3
"""check_versions.py - verify plugin manifest versions stay in sync.

.claude-plugin/plugin.json and .claude-plugin/marketplace.json each carry a version;
they must be equal so a release means the same thing everywhere.

Exit code 1 on mismatch.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    plugin = json.loads((REPO_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    marketplace = json.loads((REPO_ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))

    p_name, p_ver = plugin["name"], plugin["version"]
    entries = marketplace.get("plugins", [])
    failures = 0

    if len(entries) != 1:
        print(f"[FAIL] marketplace.json should list exactly 1 plugin, got {len(entries)}")
        failures += 1
    else:
        m_name, m_ver = entries[0]["name"], entries[0]["version"]
        if m_name != p_name:
            print(f"[FAIL] name mismatch: plugin.json '{p_name}' vs marketplace.json '{m_name}'")
            failures += 1
        if m_ver != p_ver:
            print(f"[FAIL] version mismatch: plugin.json {p_ver} vs marketplace.json {m_ver}")
            failures += 1

    if not failures:
        print(f"[OK]   {p_name} v{p_ver} (plugin.json == marketplace.json)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
