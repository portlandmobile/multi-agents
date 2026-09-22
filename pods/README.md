# Pods: persona teams for Claude Code and Claude Cowork

A **pod** is a small team of role personas that share one format. Each pod ships two ways from the same source files, with no plugin or install step:

| | Claude Code (real subagents) | Simulated (Cowork or Code) |
|---|---|---|
| How it runs | Copy `agents/<role>.md` (repo root) into `.claude/agents/` or `~/.claude/agents/` | Point Claude at a pod's `skills/pod/` folder and tell it to read and follow `SKILL.md` |
| Best for | Independent review, parallel work | Team conversations where isolation doesn't matter |
| Continuity | A memory file per role | A memory file per role, same mechanism |

The simulation is not the same as independent agents. The roles share one conversation and run one after another, so one role's view is not a second opinion. See the root [`README.md`](../README.md) for the quick start.

## Pods in this repo

| Pod | Roles | Use it for |
|---|---|---|
| [`pods/dev`](dev/README.md) | Tech Lead, Product | Software planning: feasibility vs. scope, PRDs, architecture trade-offs |
| [`pods/family`](family/README.md) | Family Assistant, Family Meal Plan | School calendars, breaks and time-off planning, coverage for the kids, weekly meal planning around a busy schedule |

## Layout

```
agents/<role>.md                    GENERATED Claude Code subagents (repo root, shared across pods, do not edit)
pods/<pod>/
  skills/pod/SKILL.md               the router: roster, how to run a request, simulated mode
  skills/pod/personas/<role>.md     SOURCE OF TRUTH for each role
scripts/build_agents.py             generates agents/ from every pod's personas/
```

## Edit or add a role

1. Edit or add `pods/<pod>/skills/pod/personas/<role>.md`. Frontmatter needs `name` (lowercase letters and hyphens, matching the filename), `description`, and `tools`.
2. Add a row to the roster table in `pods/<pod>/skills/pod/SKILL.md`, including the role's memory-file path (see below).
3. If the role should track its own continuity across sessions, give it a "Memory and session continuity" section — see any existing persona for the pattern (a memory file in the *user's* working folder, read before acting, updated when something changes).
4. Run `python3 scripts/build_agents.py` from the repo root. Use `--check` in CI to catch stale, orphaned, or unlisted files. Role names must be unique across every pod, since all pods generate into the same `agents/` folder.

## Add a pod

Copy an existing pod folder, rename it, and replace the personas, the router, and the README.

## Design rules

- **Personas are generic. Your data is not in the repo.** A pod reads your facts (for example `family/profile.md`) and keeps its memory files in *your* working folder, never inside the pod's own files.
- **Propose, don't act.** Personas draft and recommend. The user decides, and nothing is sent, booked, or changed without confirmation.
- **Explicit boundaries and handoffs.** Each role names what it does not decide and who to hand off to.
- **Each role remembers on its own.** A role's memory file is what carries continuity across sessions, real subagent or simulated, since neither one has memory of its own beyond the current run.
- **Verify, then report.** Roles cite sources, compute rather than guess, and proofread files they write.

## Privacy

Don't put account numbers, SSNs, passwords, or logins in any file a persona reads. The family pod tells its personas not to ask for them. Anything you share is processed by Claude under your plan's terms.

If you're using a pod's folder as a mounted Cowork project folder from inside a git clone, copy that folder out to your own location first, so your profile, memory files, and drafts never end up inside the git repository.
