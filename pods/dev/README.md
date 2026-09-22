# Dev Pod

A two-role software product team for **Claude Code** and **Claude Cowork**: a **Tech Lead** who keeps plans buildable, and a **Product** manager who keeps them worth building. They disagree productively, and you make the call.

No installer, marketplace, or plugin. Download or clone the repo and use the files directly.

## The roles

| Role | Does | Does not decide | Memory file |
|---|---|---|---|
| 🔧 **Tech Lead** | Architecture, implementation specs, code review, feasibility checks. Verifies assumptions against docs, batches API calls, checks new work against its own memory, and expects docs with every change. | Feature scope (Product) and UI (Design) | `pod/memory/techlead.md` |
| 📋 **Product** | Feature scoping, PRDs, user stories, acceptance criteria. Challenges assumptions and asks what problem a feature solves. | Technical implementation (Tech Lead) and interface design (Design) | `pod/memory/product.md` |

When a question belongs to the other role, a role says so and hands off instead of answering for them. A Design role is referenced for handoffs but is not included yet.

## Use it: Claude Code, real subagents

Copy the files from [`../../agents/`](../../agents/) (repo root) into `.claude/agents/` (one project) or `~/.claude/agents/` (every project):
```
cp ../../agents/techlead.md ../../agents/product.md ~/.claude/agents/
```
Then:

> *Use the techlead subagent to list the main risks of storing uploaded CSVs on local disk.*

Each role runs isolated and can work in parallel. Its continuity across separate spawns comes from its memory file (above), not from conversation history.

## Use it: simulated (Cowork, or Claude Code without subagents)

Point Claude at this pod's `skills/pod/` folder — mount it as a Cowork project folder, or just make sure the files are in context — and tell it to read and follow `SKILL.md`:

> *Read and follow skills/pod/SKILL.md. Ask Product to scope a CSV-to-chart web app in three bullets, then ask the Tech Lead if it is feasible in a week.*

> *Read and follow skills/pod/SKILL.md. Have the Tech Lead review this plan for risks, then have Product tell me which risks are worth the scope trade-off.*

In **Claude Code**, you can instead copy `skills/pod/` to `.claude/skills/pod/` in your project so it's picked up as a project skill.

In **Cowork**, add a standing project instruction once, so you don't have to repeat "read and follow SKILL.md" every time:
> *For software planning, feasibility, or PRD help, read `skills/pod/SKILL.md` in this project's folder and follow it exactly. Each role keeps its own memory file, per SKILL.md — don't blend them.*

This is a **simulation**: the roles share one conversation and run one after another, so Product's view of a Tech Lead point is not an independent review. Each role still keeps its own memory file, so its notes don't blend with the other's.

## How a request runs

1. The pod picks the role you name, or the closest match, and says which.
2. It reads only that role's profile and memory file, not every profile.
3. Each turn is labeled (`**Product:**`, `**Tech Lead:**`), with a 2-3 line summary at each handoff.
4. It brings in at most two roles per request unless you say otherwise.
5. When the roles disagree, it lays out both positions and the trade-off, and you decide.

## Files it writes

Roles follow your project's existing layout for where code and docs live, and ask if there isn't one. The default doc filename is `{project}-{role}-{topic}-{stage}-{date}.md`, for example `acme-tech-auth-refactor-draft-2026-05-04.md`. A role always states the full path of any file it writes, including its memory file.

## Customize

Edit `skills/pod/personas/techlead.md` or `product.md`, then regenerate (`python3 scripts/build_agents.py` from the repo root, writes to the shared `agents/` folder). See [`../README.md`](../README.md) for adding a role.

## Status

Version 0.1. Tested via the Claude Code CLI: the real `techlead` subagent, the simulated skill running both roles with labeled handoffs, and the memory-file mechanism — a subagent wrote a decision to its memory file, and a separate later invocation read it back correctly. Not yet tested in the Claude Cowork or Claude Desktop apps themselves.
