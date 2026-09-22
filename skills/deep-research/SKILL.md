---
name: deep-research
description: >
  Multi-stage evaluation research framework for thorough, review-driven analysis.
  Use when research tasks involve web_search + synthesis and need expert review,
  critical adversarial review, or revision loops. Triggers on: deep research,
  expert review, critical review, research with adversarial analysis,
  multi-stage research, research requiring domain expert feedback,
  research with review and revision loops. Use the web-research skill for
  the gathering phase (search + chunking) before entering this pipeline.
---

# Deep Research Skill

Multi-stage research pipeline that adds **critical review**, **expert review**, and
**revision loops** on top of the web-research gathering phase. Use when a research
task needs rigor beyond basic web search — expert validation, adversarial review, or
multi-pass iteration.

## Relationship to web-research

| Skill | Role |
|---|---|
| **deep-research** | Information reasoning — evaluation, review, revision loops |

## Pipeline — 6 Stages

```
Phase 1: Gather          → web_search + web_fetch + your experience → files (web-research)
Phase 2: Critical Review → spawn reviewer (adversarial lens)
Phase 3: Revision        → incorporate findings → update artifacts
Phase 4: Expert Review   → send to expert (KermitExpert default. Make sure this is not the Kermit.)
Phase 5: Revise + Review → incorporate feedback → second expert pass
Phase 6: Final Output    → clean deliverable + summary for human review
```

### Phase 1: Gather

Use the `web-research` skill. Run all web_search + web_fetch, write results to files
(never hold raw results in context), then synthesize into a findings document:
```
~/MyVault/Projects/{project}/{project}-{role}-{topic}-findings-{date}.md
```

The findings doc should contain: sources, key data, claims, and initial conclusions.
Once Phase 1 is complete, proceed to Phase 2.

### Phase 2: Critical Review

Spawn a reviewer sub-agent with an adversarial lens. The reviewer's job is not to
be wrong — it is to find real weaknesses.

**Spawn with:** `sessions_spawn(task="<task>", runtime="subagent", mode="run",
runTimeoutSeconds=2400)`

Include this in the task:
```
You are a critical reviewer. Your job: find genuine weaknesses, missing evidence,
weak reasoning, and unstated assumptions in the following research.

Rules:
- Do NOT be contrarian for its own sake. Only flag real issues.
- For each issue found, provide: (a) what it is, (b) why it matters, (c) what
  evidence would resolve it.
- Be specific. "This feels wrong" is not useful. "Claim X needs source Y" is.
- Maximum 3 review passes (same cap as expert review, see Phase 4).
- Write review to: ~/MyVault/Projects/{project}/{project}-review-critical-{date}.md
- Use the deep-research skill: ~/.openclaw/skills/deep-research/SKILL.md
```

**Acceptance criteria for a review:** Each issue must have (a) description,
(b) significance, (c) resolving evidence. Vague feedback is rejected.

### Phase 3: Revision

Read the critical review. Incorporate each identified issue into the findings:
- Add missing evidence if available
- Qualify weak claims
- Note unresolved gaps explicitly
- Update the findings document in place

Then proceed to Phase 4.
### Phase 4: Expert Review

Send the revised findings to an expert. Default: `KermitExpert` (KermitExpert
agent ID). For domain-specific work (legal, engineering, etc.), swap in the
appropriate expert agent or model.

**Spawn with:** `sessions_spawn(task="<task>", runtime="subagent",
runTimeoutSeconds=2400)`

Include this in the task:
```
You are a domain expert reviewing research findings. Provide a structured
review focused on: accuracy, completeness, reasoning quality, and practical
utility.

Output format:
### GO / NO-GO
{explicit GO or NO-GO}

### Issues
{numbered list: each with severity [critical/major/minor], description, and fix}

### Recommendation
{one-line summary of the assessment}

DO NOT be vague. "Feels good" is not review. Provide specific, actionable
feedback. Write to: ~/MyVault/Projects/{project}/{project}-review-expert-{date}.md
```

**Hard cap: maximum 2 expert review passes.** After the second pass, GO/NO-GO
is the stopping criterion.

### Phase 5: Revise + Expert Re-Review

If the expert review returned NO-GO issues, revise and request a second pass.
On the second pass, the expert provides a final GO/NO-GO.

### Phase 6: Final Output

Write the final deliverable and a human-readable summary.

**Deliverable:**
```
~/MyVault/Projects/{project}/{project}-{role}-{topic}-final-{date}.md
```

**Summary (for stakeholder):**
- What was researched
- Key findings (3-5 bullets)
- Confidence level (high/medium/low) and why
- Any unresolved gaps

**Never auto-notify the stakeholder.** Output the summary file and let the pod
lead decide when to escalate. The summary is a checkpoint, not a notification.

## Safety Constraints

1. **Max 2 expert review passes.** Not "as many as needed." Two passes gives
   (1) initial expert review, (2) post-revision re-review. Then we ship.
2. **Hard timeout per stage.** Use `runTimeoutSeconds=2400` for review spawns.
   Longer tasks get 900s.
3. **All artifacts to files.** Never dump multi-stage work into chat context.
4. **GO/NO-GO required.** Expert must explicitly say "GO" or "NO-GO — fix X."
   Vague feedback is rejected; the expert must provide specific, actionable items.
5. **Fixed pipeline, not a loop.** Phases flow forward. Each stage is a sequential
   step, not a cycle. Review → revise → next stage → done.
6. **Stakeholder checkpoint at Phase 6 only.** The summary is written to file.
   The human or pod lead decides when to escalate.

## Artifact Naming

All artifacts follow the existing convention:

```
{project}-{role}-{topic}-{stage}-{date}.md
```

| Stage | Naming |
|---|---|
| Findings | `{project}-{role}-{topic}-findings-{date}.md` |
| Critical review | `{project}-review-critical-{date}.md` |
| Expert review | `{project}-review-expert-{date}.md` |
| Final deliverable | `{project}-{role}-{topic}-final-{date}.md` |

Use `memory_search` to verify artifacts exist before referencing them in later
stages.
## When to Use This Skill

- Research tasks with **3+ search queries** that need expert validation
- Any research where the stakes are high enough that adversarial review
  would improve the output
- Tasks where you'd naturally say "I should have someone double-check this"
- Freemium/readiness/payment research (the proven use case)

## When NOT to Use This Skill

- Simple lookups (1-2 web searches)
- Internal memos or notes that don't need validation
- Quick fact-checks (use web-research alone)
- The task is already done and the human asked for a rewrite
                                                                                                                                            189,1         Bot

