# Multi-Agents Pods

Ready-made teams of AI personas, written once and used two ways:

- **Claude Cowork:** one agent that reads the role profiles and plays each role in turn, with a memory file per role so each one keeps its own continuity.

## Pods
There are two pods:
 - Family - Family Assistant, Family Meal Plan | School calendars and breaks, time-off and coverage planning, weekly meal planning around a busy schedule | [`pods/family`](pods/family/README.md)
 - Dev -  Tech Lead, Product | Software planning: feasibility vs. scope, PRDs, architecture trade-offs | [`pods/dev`](pods/dev/README.md)

Each pod's guide has full setup steps, example prompts, and ground rules.

## Quick start
1. Download the zip files or direct "git pull" from here: https://github.com/portlandmobile/multi-agents
2. Place the files in a directory such as Projects/multi-agents
3. Create a "family-pod" under your ~/Documents folder
4. copy Projects/multi-agents/pods/family
5. After creating Cowork Projects, added new folders, put this text to the Instructions input field.
```
This project runs the Family Pod (Family Assistant + Family Meal Plan).
 
 For any request about school calendars, closures or breaks, time off, coverage for the kids, activities, reminders, weekly meal planning, grocery lists, or dietary restrictions: read skills/pod/SKILL.md in this project's folder and follow it exactly — pick the right role(s), speak in role, and hand off between them as it describes.
 
Read family/profile.md first if it exists; if it doesn't, offer the short setup interview from skills/pod/SKILL.md.
 
Propose, don't act. Each role keeps its own memory file (see the roster in SKILL.md) — never blend them. Never ask for account numbers, card numbers, SSNs, passwords, or logins.
```
## How it works

Every role is one Markdown file: a name, a description, the tools it may use, then its principles, boundaries, and handoff rules. A small script generates the subagent files from those, so there's one source of truth.

| | Native subagents | Simulated (Cowork or standalone) |
|---|---|---|
| Runs as | Separate, isolated subagents | One agent playing roles in turn |
| Context | Isolated per role | Shared across roles |
| Parallel work | Yes | No |
| Independent second opinion | Yes | No |
| Continuity | A memory file per role, either way | A memory file per role, either way |

The simulated mode is not the same as independent agents: the roles share a conversation, so one role's view of another's point is not an independent review.

