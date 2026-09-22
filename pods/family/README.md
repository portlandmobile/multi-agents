# Family Pod

A two-role support team for a busy household, for **Claude Code** and **Claude Cowork**: a **Family Assistant** who keeps schedules and time off coherent, and a **Family Meal Plan** planner who turns that into a week of dinners. It helps the adults plan. The adults decide.

No installer, marketplace, or plugin. Download or clone the repo and use the files directly. No role in this pod handles money or financial data — that's a deliberate design choice, not a gap.

## The roles

| Role | Does | Does not do | Memory file |
|---|---|---|---|
| 🗓️ **Family Assistant** | School calendars, closures, half days and breaks. The adults' work schedules and time off. Activities and backup care. Conflict checks, coverage plans, time-off options, reminders. | Parenting or child-development advice. Money decisions. Meal planning. Book, send, or import anything on its own. | `family/memory/family-assistant.md` |
| 🍽️ **Family Meal Plan** | Weekly menus, grocery lists by store section, dietary restrictions and allergies, quick options for busy nights, batch cooking, leftovers. | Prices, budgets, or cost comparisons. Medical or nutrition-therapy advice. The shopping or the cooking itself. | `family/memory/family-meal-plan.md` |

They hand off to each other. A typical case: the Assistant flags which nights are busy, and Meal Plan builds the week's dinners around that, with quick options on the busy nights. Each keeps its own memory file, so their notes never blend.

## Before you start: keep your data out of git

If you cloned this repo with git, **copy the `pods/family` folder to a location outside the clone** before you use it — for example your Documents folder, or a fresh folder you point Cowork at. Your family profile, calendars, and memory files get written next to this folder, and if that folder is still inside the git repo, they could end up committed by mistake.

## Use it: Claude Code, real subagents

Copy the files from [`../../agents/`](../../agents/) (repo root) into `.claude/agents/` (one project) or `~/.claude/agents/` (every project):
```
cp ../../agents/family-assistant.md ../../agents/family-meal-plan.md ~/.claude/agents/
```
Then:

> *Use the family-assistant subagent to check the next month for school-closure conflicts.*

> *Use the family-meal-plan subagent to plan five weeknight dinners and build a grocery list.*

Each role runs isolated and can work in parallel. Its continuity across separate spawns comes from its memory file (above), not from conversation history.

## Use it: simulated (Cowork, or Claude Code without subagents)

Point Claude at this pod's `skills/pod/` folder — mount it as a Cowork project folder, or just make sure the files are in context — and tell it to read and follow `SKILL.md`:

> *Read and follow skills/pod/SKILL.md. Plan next week's dinners using my profile, and flag anything that clashes with our dietary restrictions or the busy nights on our calendar.*

In **Claude Code**, you can instead copy `skills/pod/` to `.claude/skills/pod/` in your project so it's picked up as a project skill.

In **Cowork**, add a standing project instruction once, so you don't have to repeat "read and follow SKILL.md" every time:
> *For scheduling, coverage, time-off, or meal-planning help, read `skills/pod/SKILL.md` in this project's folder and follow it exactly. Read `family/profile.md` first; if it's missing, offer the setup interview. Propose, don't act — nothing is booked, sent, or added to a calendar without me. Each role keeps its own memory file, per SKILL.md — don't blend them.*

This is a **simulation**: the roles share one conversation and run one after another, so Meal Plan's view of the Assistant's schedule is not an independent review. Each role still keeps its own memory file, so its notes don't blend with the other's.

## First run: your family profile

The roles work from a short profile: who is in the household, schools and their calendars, dietary needs and allergies, work schedules and time-off balances, recurring activities, backup care, and non-negotiables.

The first time you ask for help, the pod offers a short interview (a few questions at a time, and you can skip anything) and saves the result to **`family/profile.md` in your own working folder**. Dietary needs and allergies are asked early and treated as a hard constraint on every meal, not a preference. Prefer to fill it in yourself? Copy [`skills/pod/templates/family-profile.md`](skills/pod/templates/family-profile.md) to `family/profile.md`.

Give the pod your school calendars as PDFs, text, or ICS files in the same folder.

## What you get

- A **conflict report**: double-booked adults and days with no coverage.
- A **coverage plan**, day by day: school status, each adult's status, who covers, and gaps marked with two or three ways to close each.
- **Time-off options** with the number of days each uses.
- **Deadlines** worked out from your notice rules.
- A **weekly menu** matched to your busy nights, with quick options where the schedule needs them.
- A **grocery list** organized by store section, plus easy swaps for each meal.
- Every meal checked against your **dietary restrictions and allergies** before it's presented — not after.
- **Open questions** where the sources are ambiguous (no school vs. early dismissal, an optional holiday, whether working from home counts as coverage).
- **Continuity across sessions**: each role remembers what it already found out or decided, in its own memory file, so you don't re-explain the same thing next time.

Files go to `family/` in your folder, named `{family}-{role}-{topic}-{stage}-{date}.md`, and the roles always state the path.

## Ground rules

- **Propose, don't act.** Drafts only. Nothing is booked, sent, or added to a calendar without you.
- **Dates come from your sources**, cited, with weekdays computed by a script rather than guessed.
- **Ambiguity is flagged**, not resolved silently.
- **Allergies and restrictions are hard constraints.** Every recipe and every ingredient in it is checked against them before a plan is presented.
- **The adults decide.** You get options, trade-offs, and a recommendation.
- **Each role remembers on its own.** No shared memory between the two roles.

## Safety and privacy

- Family Meal Plan gives cooking and planning help, not medical or nutrition-therapy advice. For a diagnosed condition or a severe allergy, it works only within what you or your clinician have told it — it doesn't invent guidance, and it says so if asked for it. It can't see product labels, so it tells you to check store-bought items yourself.
- **This pod has no financial role and doesn't need financial data.** Don't put account numbers, card numbers, SSNs, passwords, or logins in your profile, memory files, or any file a role reads.
- Your profile, memory files, and drafts live in your own folder, never inside this pod's own files.
- Anything you share is processed by Claude under your plan's terms.

## Customize

Edit the roles in `skills/pod/personas/`, then regenerate (`python3 scripts/build_agents.py` from the repo root, writes to the shared `agents/` folder). See [`../README.md`](../README.md) for adding a role.

## Status

Version 0.1. Tested via the Claude Code CLI with fictional data: break-coverage planning, the first-run interview, a meal plan built against a profile with a listed severe allergy (the requested dish was swapped out and the substitution explained, unprompted), and the memory-file mechanism — both roles wrote to separate memory files in one run, and a later, separate invocation read each one back correctly and only its own. Not yet tested: the Claude Cowork or Claude Desktop apps themselves, and `.ics` calendar output. Calendar and email connectors are not used yet; everything works from files you provide.
