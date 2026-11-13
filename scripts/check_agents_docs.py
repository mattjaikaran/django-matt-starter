#!/usr/bin/env python3
"""Validate agent instructions: AGENTS.md, its links, its adapter ban, and skills."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
CLAUDE = ROOT / "CLAUDE.md"
SKILLS = ROOT / ".claude" / "skills"
MAX_AGENT_LINES = 200

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def link_targets(text: str) -> list[str]:
    """Return the raw targets of Markdown links and images."""
    targets: list[str] = []
    for raw in LINK_RE.findall(text):
        target = raw.strip()
        if target.startswith("<"):
            target = target[1:].split(">", 1)[0]
        else:
            target = target.split()[0]
        targets.append(target)
    return targets


def relative_path(target: str) -> str | None:
    """Return a repository path for a relative target, or None to skip it."""
    if target.startswith(("#", "mailto:", "tel:")):
        return None
    if "://" in target:
        return None
    path = unquote(target.split("#", 1)[0].split("?", 1)[0])
    return path or None


def check_agents() -> list[str]:
    if not AGENTS.is_file():
        return ["AGENTS.md is missing at the repository root"]

    text = AGENTS.read_text(encoding="utf-8")
    problems: list[str] = []
    line_count = len(text.splitlines())
    if line_count > MAX_AGENT_LINES:
        problems.append(f"AGENTS.md has {line_count} lines; the limit is {MAX_AGENT_LINES}")
    for target in link_targets(text):
        path = relative_path(target)
        if path is None:
            continue
        if not (ROOT / path.lstrip("/")).exists():
            problems.append(f"AGENTS.md links to a missing path: {target}")
    return problems


def check_claude() -> list[str]:
    """AGENTS.md is the only agent file; a harness adapter must not duplicate it."""
    if CLAUDE.is_file():
        return ["CLAUDE.md must not exist; AGENTS.md is the only agent file"]
    return []


def frontmatter(path: Path) -> dict[str, str] | None:
    match = FRONTMATTER_RE.match(path.read_text(encoding="utf-8"))
    if match is None:
        return None
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator and key.strip() and not key.startswith((" ", "\t")):
            fields[key.strip()] = value.strip().strip("\"'")
    return fields


def check_skills() -> list[str]:
    if not SKILLS.is_dir():
        return []

    problems: list[str] = []
    for skill in sorted(SKILLS.glob("*/SKILL.md")):
        relative = skill.relative_to(ROOT)
        fields = frontmatter(skill)
        if fields is None:
            problems.append(f"{relative} has no frontmatter block")
            continue
        for field in ("name", "description"):
            if not fields.get(field):
                problems.append(f"{relative} is missing frontmatter field: {field}")
        if fields.get("name") and fields["name"] != skill.parent.name:
            problems.append(
                f"{relative} name {fields['name']!r} does not match directory {skill.parent.name!r}"
            )
    return problems


def main() -> int:
    problems = check_agents() + check_claude() + check_skills()
    if problems:
        print("Agent docs checks failed:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print("Agent docs checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
