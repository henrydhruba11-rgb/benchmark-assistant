#!/usr/bin/env python3
"""check_citations.py - verify every citation in the skill resolves against sources/.

The skill's core promise is traceable citations (source ID + section). This script makes
that promise continuously verifiable instead of relying on one-time manual checks.

Checks (ERROR fails CI, WARN is reported only):
  1. `<id> §<section>` refs resolve to actual text in sources/<id>.md. Matching strips all
     whitespace, unifies quotes/dashes/colons and is case-insensitive, so pypdf space-joining
     artifacts in the two surveys (e.g. `3 WHAT TO EV ALUATE`) still match.
  2. Primary line anchors (`<id> §<section>（line N`): the section must appear at line N.
     A citation pointing anywhere inside the section's heading span also passes.
     On mismatch the actual line(s) are reported - use them to re-anchor.
  3. Content line refs (`<phrase>，line N`): phrase must appear at the cited line(s). WARN only.
  4. `原则 N` refs must exist in references/design-principles.md; its numbering must stay 1..16.
  5. Structure counts: build.md = Step 1-10, review.md = R1-R9, analyze.md = F1-F5 + F4.5.
  6. Path refs in SKILL.md (`playbooks/...`, `references/...`, `sources/...`, `scripts/...`) exist.
  7. `knowledge-map §X` internal refs must be ## headings in references/knowledge-map.md.

Source IDs are loaded from tools/sources-registry.json (adding a source = registry entry).
Per-source `aliases` in the registry map conventional short names (e.g. chapter6 引言)
to the actual text in the source. Skip a citing line with: lint:allow
Exit code 1 if any ERROR.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "benchmark-assistant"
REGISTRY = REPO_ROOT / "tools" / "sources-registry.json"

# § ref: optional source id directly before §, lazy title terminated by a bracket,
# punctuation mark, a `line N` ref, another §, or end of line.
CIT_RE = re.compile(
    r"(?:(?P<id>[A-Za-z][\w.-]*)\s*)?§\s*(?P<title>.+?)(?=[（(\[）)\]；;。，、：:\n「」]|\s+line\s*\d|§|$)"
)
LINE_REF_RE = re.compile(r"line\s*(?P<n>\d+)(?:\s*-\s*(?P<m>\d+))?")
PRINCIPLE_RE = re.compile(r"原则\s*(\d+)")
PATH_REF_RE = re.compile(r"`((?:playbooks|references|sources|scripts)/[^`\s]+)`")

INTERNAL_IDS = {"knowledge-map": "references/knowledge-map.md"}  # id -> file under the skill dir
ID_SKIP = {"spec"}  # 'spec §...' refers to docs/superpowers design specs, not sources/
# annotation glue stripped from content-ref phrases before matching; prefix/suffix only,
# longest first (本章导读 before 章首), single chars last
DESCRIPTORS = [
    "为加粗小标题", "加粗小标题", "列四组", "等下游领域", "等子节", "本章导读", "代码示例",
    "采样指标", "后者含", "定义", "说明", "开篇", "章首", "摘要", "亦提", "略提",
    "含", "属", "内", "见", "即",
]

errors: list[str] = []
warns: list[str] = []
checked = 0


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warns.append(msg)


def norm(s: str) -> str:
    """Normalize for matching: tolerant of pypdf garbling, quote/dash variants, mojibake."""
    s = s.replace("�", "")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("：", ":").replace("—", "-").replace("–", "-").replace("`", "")
    s = s.replace("-", "")  # hyphen variants in citation vs source (Final-response vs Final Response)
    return re.sub(r"\s+", "", s).lower()


def load_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")


def has_cjk(s: str) -> bool:
    return any("一" <= ch <= "鿿" for ch in s)


def key_ok(key: str) -> bool:
    return len(key) >= (2 if has_cjk(key) else 3)


class Source:
    def __init__(self, sid: str, path: Path, aliases: dict[str, str]):
        self.sid = sid
        self.lines = load_lines(path)
        self.normed = [norm(line) for line in self.lines]
        self.aliases = aliases  # normalized cited title -> normalized actual text

    def find(self, key: str) -> list[int]:
        return [i for i, line in enumerate(self.normed, 1) if key in line]

    def resolve(self, title: str) -> tuple[str, list[int]] | None:
        """Match ladder: alias -> full title -> progressive trim -> section-number prefix."""
        segments = [s.strip() for s in title.split(">") if s.strip()]
        leaf = (segments[-1] if segments else "").rstrip("/").strip()
        alias = self.aliases.get(norm(leaf)) or self.aliases.get(norm(title.strip()))
        if alias:
            hits = self.find(alias)
            if hits:
                return alias, hits
        cand = leaf
        for attempt in (leaf, re.sub(r"^\d+(?:\.\d+)*\s+", "", leaf)):  # retry without section number
            cand = attempt
            while cand:
                key = norm(cand)
                if key_ok(key):
                    hits = self.find(key)
                    if hits:
                        return key, hits
                new = re.sub(r"\s+\S+$", "", cand)  # drop trailing space-separated token
                if new == cand:
                    new = cand[:-1]  # no spaces left: drop last char
                cand = new.strip()
        m = re.match(r"(\d+(?:\.\d+)*)", leaf)  # section-number prefix fallback
        if m:
            num = m.group(1)
            pat = re.compile(r"^\s*#*\s*\*{0,2}\s*" + re.escape(num) + r"[\s.、*]")
            hits = [i for i, line in enumerate(self.lines, 1) if pat.match(line)]
            if hits:
                return num, hits
        return None

    def heading_spans(self, hits: list[int]) -> list[tuple[int, int]]:
        """For hits that are markdown headings, return [heading_line, next_same_level_heading) spans."""
        spans = []
        for h in hits:
            m = re.match(r"^\s{0,3}(#{1,6})\s", self.lines[h - 1])
            if not m:
                continue
            level = len(m.group(1))
            end = len(self.lines) + 1
            for i in range(h, len(self.lines)):
                m2 = re.match(r"^\s{0,3}(#{1,6})\s", self.lines[i])
                if m2 and len(m2.group(1)) <= level:
                    end = i + 1  # 1-based line of the next heading; span is [h, end)
                    break
            spans.append((h, end))
        return spans


def clean_phrase(raw: str) -> str:
    """Extract the matchable key from the text preceding a `line N` ref."""
    raw = LINE_REF_RE.sub("", raw)  # drop earlier `line N` refs in `... line 625 / X line 632` chains
    frags = [f.strip() for f in re.split(r"[，,、：:；;（）()\[\]/]|\s+vs\s+", raw) if f.strip()]
    frag = frags[-1] if frags else ""
    changed = True  # strip annotation glue, prefix/suffix only (global replace would eat 内容->容)
    while changed and frag:
        changed = False
        for d in DESCRIPTORS:
            if frag.startswith(d) or frag.endswith(d):
                frag = frag.removeprefix(d).removesuffix(d).strip()
                changed = True
    return frag.strip(" -—–\"'“”‘’")


def check_ref(src: Source, title: str, segment: str, cite: str) -> None:
    global checked
    checked += 1
    resolved = src.resolve(title)
    if not resolved:
        err(f"{cite}: {src.sid} §{title.strip()} -> NOT FOUND in sources/{src.sid}.md")
        return
    key, hits = resolved
    spans = src.heading_spans(hits)
    # titles ending in a locator word (§X 开篇/章首/摘要) point at the section's opening
    # text, not its heading line - skip exact anchor check for them
    locator = any(title.strip().endswith(d) for d in ("开篇", "章首", "摘要"))
    prev_end = 0
    for ref in LINE_REF_RE.finditer(segment):
        n = int(ref.group("n"))
        m = int(ref.group("m") or n)
        raw = segment[prev_end:ref.start()]
        prev_end = ref.end()
        if n < 1 or m > len(src.lines):
            err(f"{cite}: {src.sid} §{title.strip()} line {ref.group(0)} out of range "
                f"(file has {len(src.lines)} lines)")
            continue
        if re.fullmatch(r"[\s（(\[：:]*", raw):  # primary anchor: `§title（line N` / `§title line N`
            if locator:
                continue
            exact = any(n <= h <= m for h in hits)
            in_span = any(h <= n < e for h, e in spans)
            if not exact and not in_span:
                err(f"{cite}: {src.sid} §{title.strip()} cited at line {ref.group(0)[5:]} "
                    f"but '{key}' found at line(s) {hits[:8]}"
                    + (f" (total {len(hits)})" if len(hits) > 8 else ""))
        else:
            phrase = clean_phrase(raw)
            pkey = norm(phrase)
            if len(pkey) < 2:
                continue
            if not any(pkey in src.normed[i] for i in range(n - 1, m)):
                warn(f"{cite}: {src.sid} §{title.strip()}: '{phrase}' not found at "
                     f"line {n}" + (f"-{m}" if m != n else ""))


def scan_file(path: Path, sources: dict[str, Source], internal: dict[str, Path]) -> None:
    global checked
    rel = path.relative_to(REPO_ROOT)
    for lineno, line in enumerate(load_lines(path), 1):
        if "lint:allow" in line or "§" not in line:
            continue
        cite = f"{rel}:{lineno}"
        matches = list(CIT_RE.finditer(line))
        last_id: str | None = None
        for idx, match in enumerate(matches):
            sid = match.group("id") or last_id
            if match.group("id"):
                last_id = match.group("id")
            title = match.group("title")
            seg_end = matches[idx + 1].start() if idx + 1 < len(matches) else len(line)
            segment = line[match.end():seg_end]
            if not sid:
                warn(f"{cite}: §{title.strip()} has no source id and none to inherit")
                continue
            if sid in ID_SKIP:
                continue
            if sid in internal:
                target = load_lines(internal[sid])
                heading = re.compile(r"^##\s*" + re.escape(title.strip()) + r"(?:[.\s（(]|$)")
                checked += 1
                if not any(heading.match(t) for t in target):
                    err(f"{cite}: knowledge-map §{title.strip()} -> no '## {title.strip()}' "
                        f"heading in {internal[sid].relative_to(REPO_ROOT)}")
                continue
            if sid.endswith(".md"):
                continue  # plain file mention, not a source citation
            src = sources.get(sid)
            if not src:
                warn(f"{cite}: unknown source id '{sid}' (not in tools/sources-registry.json)")
                continue
            check_ref(src, title, segment, cite)


def check_principles(files: list[Path]) -> None:
    global checked
    dp = SKILL_DIR / "references" / "design-principles.md"
    defined = [int(m.group(1)) for m in
               map(re.compile(r"^### (\d+)\.").match, load_lines(dp)) if m]
    if defined != list(range(1, 17)):
        err(f"references/design-principles.md: principle numbering must stay 1..16, "
            f"got {defined}")
    for path in files:
        rel = path.relative_to(REPO_ROOT)
        for lineno, line in enumerate(load_lines(path), 1):
            for ref in PRINCIPLE_RE.finditer(line):
                checked += 1
                if int(ref.group(1)) not in defined:
                    err(f"{rel}:{lineno}: 原则 {ref.group(1)} not defined in design-principles.md")


def check_structure() -> None:
    global checked

    def headings(path: Path, pat: str) -> list[str]:
        rx = re.compile(pat)
        return [m.group(1) for m in map(rx.match, load_lines(path)) if m]

    steps = headings(SKILL_DIR / "playbooks" / "build.md", r"^## Step (\d+)\.")
    if steps != [str(i) for i in range(1, 11)]:
        err(f"playbooks/build.md: expected Step 1..10, got {steps}")
    rs = headings(SKILL_DIR / "playbooks" / "review.md", r"^### R(\d)\.")
    if rs != [str(i) for i in range(1, 10)]:
        err(f"playbooks/review.md: expected R1..R9, got {rs}")
    fs = headings(SKILL_DIR / "playbooks" / "analyze.md", r"^### F(\d)\.(?!\d)")
    f45 = headings(SKILL_DIR / "playbooks" / "analyze.md", r"^### F(4\.5)")
    if fs != [str(i) for i in range(1, 6)] or not f45:
        err(f"playbooks/analyze.md: expected F1..F5 + F4.5, got F{fs} F4.5={bool(f45)}")
    checked += 3


def check_skill_paths() -> None:
    global checked
    skill_md = SKILL_DIR / "SKILL.md"
    for lineno, line in enumerate(load_lines(skill_md), 1):
        for ref in PATH_REF_RE.finditer(line):
            p = ref.group(1)
            if "<" in p or "*" in p:
                continue
            checked += 1
            if not (SKILL_DIR / p).exists():
                err(f"SKILL.md:{lineno}: referenced path '{p}' does not exist")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows GBK console
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    sources: dict[str, Source] = {}
    for entry in registry["sources"]:
        snap = REPO_ROOT / entry["snapshot"]
        if not snap.exists():
            err(f"registry: snapshot missing: {entry['snapshot']}")
            continue
        aliases = {norm(k): norm(v) for k, v in entry.get("aliases", {}).items()}
        sources[entry["id"]] = Source(entry["id"], snap, aliases)
    internal = {k: SKILL_DIR / v for k, v in INTERNAL_IDS.items()}

    files = [SKILL_DIR / "SKILL.md"]
    files += sorted((SKILL_DIR / "playbooks").glob("*.md"))
    files += sorted((SKILL_DIR / "references").glob("*.md"))
    for path in files:
        scan_file(path, sources, internal)
    check_principles(files)
    check_structure()
    check_skill_paths()

    for msg in errors:
        print(f"[ERROR] {msg}")
    for msg in warns:
        print(f"[WARN]  {msg}")
    print(f"\n{checked} citations/checks, {len(errors)} error(s), {len(warns)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
