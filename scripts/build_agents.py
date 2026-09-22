#!/usr/bin/env python3
"""Generate Claude Code subagents from each pod's persona profiles.

Source of truth: pods/<pod>/skills/pod/personas/<name>.md (also read directly
by the `pod` skill for the Cowork simulation).

Generated output: agents/<name>.md, one shared top-level folder across every
pod. This is a plain folder, not a plugin: copy the file(s) you want into
.claude/agents/ (project) or ~/.claude/agents/ (personal) to use them as
native Claude Code subagents, or point any other harness at them directly.

Usage:
    python3 scripts/build_agents.py           # write agents/*.md
    python3 scripts/build_agents.py --check   # exit 1 if anything is stale, missing, or unlisted
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PODS = ROOT / "pods"
OUT = ROOT / "agents"

NAME_RE = re.compile(r"^[a-z][a-z-]*$")
REQUIRED = ("name", "description")
MARKER = "<!-- GENERATED from "

OVERLAY = """
## Running as a subagent

You run in an isolated context and cannot see the parent conversation, so work
only from the task you were given. Do not spawn other agents. If another role
should weigh in, say which one and why in your final report. End with a short
summary of what you decided or produced, including the full path of any file you
wrote.
"""


def rel(path):
    return path.relative_to(ROOT).as_posix()


def split_frontmatter(text, path):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        sys.exit(f"{rel(path)}: missing YAML frontmatter")
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return m.group(1), fm, m.group(2)


def build(path):
    raw, fm, body = split_frontmatter(path.read_text(encoding="utf-8"), path)
    for key in REQUIRED:
        if not fm.get(key):
            sys.exit(f"{rel(path)}: frontmatter is missing '{key}'")
    if not NAME_RE.match(fm["name"]):
        sys.exit(f"{rel(path)}: name '{fm['name']}' must be lowercase letters and hyphens")
    if fm["name"] != path.stem:
        sys.exit(f"{rel(path)}: name '{fm['name']}' must match the filename '{path.stem}'")
    note = f"{MARKER}{rel(path)}. Edit the source, then run scripts/build_agents.py. -->"
    return f"---\n{raw}\n---\n{note}\n{body.rstrip()}\n{OVERLAY}"


def main():
    check = "--check" in sys.argv
    problems = []
    seen = {}
    expected = set()
    pod_dirs = sorted(p for p in PODS.iterdir() if (p / "skills" / "pod" / "personas").is_dir())
    if not pod_dirs:
        sys.exit(f"no pods with personas found under {rel(PODS)}")

    for pod in pod_dirs:
        skill_dir = pod / "skills" / "pod"
        sources = sorted((skill_dir / "personas").glob("*.md"))
        roster = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

        for src in sources:
            content = build(src)
            name = src.stem
            if name in seen:
                sys.exit(f"duplicate persona name '{name}' in {rel(src)} and {seen[name]}")
            seen[name] = rel(src)
            if f"personas/{src.name}" not in roster:
                problems.append(f"{rel(skill_dir / 'SKILL.md')}: roster does not list personas/{src.name}")
            target = OUT / src.name
            expected.add(target.name)
            if check:
                if not target.exists() or target.read_text(encoding="utf-8") != content:
                    problems.append(f"stale or missing: {rel(target)}")
            else:
                OUT.mkdir(exist_ok=True)
                target.write_text(content, encoding="utf-8")
                print("wrote", rel(target))

    # Orphans: generated files whose persona was removed or renamed. Never touch
    # a hand-written file that doesn't carry the GENERATED marker.
    if OUT.is_dir():
        for f in sorted(OUT.glob("*.md")):
            if f.name not in expected and MARKER in f.read_text(encoding="utf-8"):
                if check:
                    problems.append(f"orphaned (persona removed): {rel(f)}")
                else:
                    f.unlink()
                    print("removed", rel(f))

    if check:
        if problems:
            sys.exit("\n".join(problems))
        print("up to date:", ", ".join(sorted(seen)))
    elif problems:
        print("warning:\n" + "\n".join(problems), file=sys.stderr)


if __name__ == "__main__":
    main()
