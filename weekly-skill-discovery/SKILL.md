---
name: weekly-skill-discovery
description: >
  Scan Cowork session history, Slack, Notion, and HubSpot to find repeatable manual workflows that should be turned into skills or scheduled tasks. Use this skill whenever the user asks things like "what should be a skill", "find what I keep doing manually", "what workflows should I automate", "skill discovery", "what am I repeating", "find automation opportunities", "what processes should I systematize", or "what's taking up my time that Claude could do". Also trigger proactively when the user says "turn this into a skill" or "can you help me find things to automate" — the discovery phase should always run before building. The output is a prioritized report of skill candidates with evidence from the user's actual tool usage.
---

# Weekly Skill Discovery

Your job is to act as a thoughtful automation consultant. Scan the user's connected tools to find manual work that's being repeated — work that follows a consistent enough pattern that it could be captured in a skill and run automatically.

The goal is to surface the highest-leverage opportunities: where Claude could save the most time per week with the least complexity to build. Each candidate should feel like a clear, concrete pitch — the reader should immediately see themselves using it.

## Important: What counts as manual work (and what doesn't)

**Slack messages are communication, not evidence of manual overhead.** Miriam posts in Slack to coordinate with teammates — this is just how she communicates. Do NOT identify "posting X to Slack" as a skill candidate unless there is clear evidence that she is laboriously bridging data between two tools by hand (e.g., manually pulling a HubSpot report and typing its contents into Slack field by field). Simply sharing a link, summary, or update in Slack is normal communication behavior.

**Real manual work looks like:**
- Multi-step tool sequences done the same way repeatedly (open Fireflies → find transcript → copy context → open HubSpot → create deal → fill in same fields each time)
- Research tasks that follow a template (look up LinkedIn profile → analyze posting cadence → summarize gaps → write notes)
- Post-call action sequences that always require the same data entry
- Content that gets created on a repeating cadence using the same structure each time
- Tracking tasks done by hand that could be monitored automatically (deal stages, action items, engagement signals)

**High-value candidate types to actively look for:**
- **Post-call workflow automation** — deal creation, materials sending, action item logging after discovery calls
- **Content research and generation** — LinkedIn analysis, pain point research, content calendar building
- **Deal and pipeline monitoring** — stage updates, action item tracking, risk flag notifications
- **Event preparation** — attendee research and ICP scoring before conferences/networking events
- **LinkedIn engagement** — drafting replies to comments, tracking engagement patterns
- **Prospect research** — generating content examples tailored to a prospect's industry for calls

## What to scan

Work through these in parallel using multiple tool calls in the same turn:

### 1. Cowork session history

Call `list_sessions` with `limit: 50`. Look at **titles** first — repeated patterns are a strong signal. Then use `read_transcript` on sessions that appear to be manual one-off workflows (not already-scheduled tasks).

Look for:
- Tasks that follow similar patterns across multiple sessions
- Multi-step workflows with 5+ tool calls done more than once this week
- Research or preparation workflows repeated daily or weekly
- Post-call sequences (deal creation, follow-up, materials sending) done manually each time

Skip sessions whose titles match scheduled task names (e.g., "Apr N – [task name]").

### 2. Slack

Search `from:miriam` to understand what she's working on. But read Slack critically — the goal is to find patterns in the *work behind the messages*, not to flag the messages themselves as manual overhead.

Look for:
- References to manual steps she mentions doing ("I just created the deal", "I sent over the case studies")
- Requests for things that could be automated ("can someone check if...", recurring questions she's fielding)
- Evidence of repeated research or data-gathering that precedes the messages

### 3. Notion

Search for recently updated pages. Look for:
- Content calendars, templates, or trackers updated on a regular cadence
- Pages that get duplicated and filled in (same structure, different data)
- Action item logs or tracking sheets maintained manually

### 4. HubSpot CRM

Search contacts and deals. Look for:
- Batch deal creation with identical fields (same amount, same close date, same stage → suggests a manual template workflow)
- Deals missing next steps or action items (a monitoring/tracking skill could help)
- Patterns in what gets entered after calls vs. what gets skipped

### 5. Existing skills and scheduled tasks

Always check `list_scheduled_tasks` **before** writing any candidates. It's a critical failure to recommend automating something that's already automated. Cross-reference the installed skills list too.

## How to evaluate candidates

A good skill candidate has three things:
1. **Recurrence** — happens more than once (ideally daily or weekly)
2. **Pattern** — each instance follows roughly the same steps
3. **Tools** — uses connected tools Claude already has access to

The strongest candidates are repetitive multi-step sequences: the same tools, the same data, the same output shape, repeated regularly. One-off tasks or highly variable workflows are weak candidates.

## Output format

Save the report as `skill-discovery-[YYYY-MM-DD].md` in the outputs folder.

```markdown
# Skill Discovery Report
**Date:** [today]
**Period scanned:** [date range]

## Current Automation Baseline — What's Working
[Describe what each active task covers and why it's working — not just a bare list.
Help the reader understand what is genuinely handled.]

| Scheduled Task | Frequency | What It Covers |
|---|---|---|

## Skill Candidates

### 1. `skill-name-in-kebab-case` ⭐ [Top Priority / Quick Win / Strategic]

**What it would do:** [1-2 sentences]

**Current manual steps:** [Describe the actual manual workflow as it happens today —
tools involved, how many steps, rough time. Be specific and concrete.]

**Evidence:** [Cite specific session names, Slack context, Notion pages, or HubSpot
patterns you actually observed. No candidate without real evidence.]

**Ideal workflow (automated):**
1. [Trigger or data source]
2. [Processing step]
3. [Output or delivery]

**Time saved:** [X min/day or X hours/week]
**Complexity:** Low / Medium / High

[Repeat for each main candidate — max 6]

## Secondary Opportunities
[Real but lower-priority patterns — 2-4 bullet points, 1-2 sentences each]

## Existing Skills — Gap Analysis
| Skill/Task | Gap Observed | Suggested Enhancement |
|---|---|---|

## Priority Ranking
| Rank | Skill | Time Saved/Week | Complexity | Priority |
|---|---|---|---|---|

**Total weekly time recoverable if top candidates are built:** [X hours]
```

### Priority labels
- ⭐ **Top Priority** — high frequency + high time saved + medium or lower complexity
- **Quick Win** — low complexity, fast to build
- **Strategic** — lower frequency but high value per run

### Quality bar
Max 6 main candidates. A short, evidence-backed list beats a long vague one. Move borderline candidates to Secondary Opportunities. The **Current Manual Steps** and **Ideal Workflow** sections are what make candidates feel actionable — spend time on these.

## Running autonomously

- If a tool errors, note it briefly and continue
- Never recommend automating something already in `list_scheduled_tasks`
- Include a "Total weekly time recoverable" figure at the bottom of the priority table
- Make the report self-contained — the reader should understand each candidate without needing additional context
