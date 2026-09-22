# Multi-Agents Pods

Ready-made teams of AI personas for **Claude Code** and **Claude Cowork**. Each team (a *pod*) is a handful of roles with clear jobs, boundaries, and handoffs, written once and used two ways:

- **Claude Code:** real, isolated subagents.
- **Claude Cowork:** one agent that reads the role profiles and plays each role in turn, with a memory file per role so each one keeps its own continuity.

No installer, marketplace, or plugin. Download or clone this repo and use the files directly.

## Pods

| Pod | Roles | Use it for | Guide |
|---|---|---|---|
| **Dev** | Tech Lead, Product | Software planning: feasibility vs. scope, PRDs, architecture trade-offs | [`pods/dev`](pods/dev/README.md) |
| **Family** | Family Assistant, Family Meal Plan | School calendars and breaks, time-off and coverage planning, weekly meal planning around a busy schedule | [`pods/family`](pods/family/README.md) |

Each pod's guide has full setup steps, example prompts, and ground rules.

## Quick start

**Claude Code, real subagents.** Copy the role files you want from [`agents/`](agents/) into `.claude/agents/` (one project) or `~/.claude/agents/` (every project). No config, no restart. Then:

> *Use the techlead subagent to review this plan for risks.*

**Claude Cowork, or Claude Code without subagents.** Point Claude at a pod's `skills/pod/` folder (as a mounted project folder, or just files in context) and tell it to read and follow `SKILL.md`. One agent then plays each role in turn, in a shared conversation:

> *Read and follow skills/pod/SKILL.md. Ask Product to scope a CSV-to-chart web app, then ask the Tech Lead if it is feasible in a week.*

**Any other harness (Hermes, a custom agent loop, etc.).** The files in `agents/` are plain Markdown with a YAML header any prompt-following tool can read directly.

## How it works

Every role is one Markdown file: a name, a description, the tools it may use, then its principles, boundaries, and handoff rules. A small script generates the Claude Code subagent files from those, so there's one source of truth.

| | Claude Code (subagents) | Simulated (Cowork or Code) |
|---|---|---|
| Runs as | Separate, isolated subagents | One agent playing roles in turn |
| Context | Isolated per role | Shared across roles |
| Parallel work | Yes | No |
| Independent second opinion | Yes | No |
| Continuity | A memory file per role, either way | A memory file per role, either way |

The simulated mode is not the same as independent agents: the roles share a conversation, so one role's view of another's point is not an independent review.

## Principles

- **Propose, don't act.** Roles draft and recommend. The user decides, and nothing is sent, booked, or changed without confirmation.
- **Boundaries and handoffs.** Each role says what it does not decide and who should.
- **Your data stays yours.** A pod reads your facts, and keeps its memory, in your own working folder, never inside the pod's own files.
- **Each role remembers on its own.** A role's continuity comes from its own memory file, read before it acts and updated when something changes, kept separate from every other role's.
- **Verify, then report.** Roles cite sources, calculate instead of guessing, and proofread the files they write.

## Repository layout

```
agents/<role>.md                  generated Claude Code subagents, one flat folder, all pods
pods/<pod>/
  skills/pod/personas/<role>.md   the roles (source of truth)
  skills/pod/SKILL.md             how the roles are run together, simulated mode
scripts/build_agents.py           regenerates agents/ from the personas
skills/deep-research/             a multi-stage research skill (not part of the pods)
```

To edit a role, add a role, or create a new pod, see [`pods/README.md`](pods/README.md).

## Safety and privacy

Don't put account numbers, SSNs, passwords, or logins in any file a role reads, and anything you share is processed by Claude under your plan's terms. No role in either pod handles financial data by design. The Family pod's guide has the details, including that its meal-plan role is **not a substitute for medical or dietary-professional advice** and treats every listed allergy as a hard constraint.

## Status

Version 0.1. Tested in Claude Code: real subagents, the simulated multi-role mode, and per-role memory files (written by one session, correctly read back — and kept separate — by a later one), all via the CLI. Not yet tested in the Claude Cowork or Claude Desktop apps themselves. Issues and pull requests are welcome.
