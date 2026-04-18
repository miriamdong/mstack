---
name: post-call-action-item-sync
description: "Extract action items from completed sales calls and sync them to Notion as tasks with owners, deadlines, and call context. Pulls transcripts from Fireflies and Granola, identifies commitments from both sides (Virio and prospect), and creates structured tasks in the My Tasks database. Use this skill whenever the user says 'sync action items from my calls', 'what did I commit to on my calls today', 'pull action items from my call with [company]', 'log the action items from [company]', 'what needs to happen after my calls', or 'action items from today'. Also trigger when the user mentions needing to track follow-ups, commitments, or next steps from sales calls — even if they don't say 'action items' explicitly. This is different from daily-followup-drafts (which sends thank-you emails) and post-call-deal-creator (which creates HubSpot deals). This skill captures the specific things both sides agreed to do and makes sure nothing falls through the cracks."
---

# Post-Call Action Item Sync

You extract action items from Miriam's completed sales calls and create structured tasks in Notion so nothing gets dropped. After every discovery call, demo, or follow-up, there are things both Virio and the prospect committed to doing — this skill captures all of them.

## Why This Matters

The gap between a great sales call and a closed deal is execution. When Miriam finishes 3-4 calls in a day, the specific commitments blur together: "Send the case study to Jess," "Follow up with the CTO intro by Thursday," "Prospect will share their target account list by Monday." If even one of these slips, trust erodes and deals stall. This skill makes sure every commitment lands in Notion with the right context, owner, and deadline.

## Modes

**Targeted mode**: The user names a specific company or person — e.g., "sync action items from my call with ClearVector" or "what did I commit to with Jess?" Find the matching transcript and extract action items from that call.

**Batch mode**: The user says something like "sync action items from today's calls" or "what needs to happen after my calls today." Scan all of today's completed external calls and extract action items from each.

## Step 1: Find the Call Transcript(s)

Use a multi-source approach — check Fireflies first, then Granola as fallback. Some calls are recorded in one system, some in the other.

### Targeted mode

1. Search Fireflies: `fireflies_search` with the company or person name, filtered to the last 7 days, `mine:true`
2. If no Fireflies result, check Granola: `query_granola_meetings` with the company or person name
3. **Critical: pick the RIGHT transcript.** When a company name returns multiple results, you must read the summary of each and select the correct one. Virio sells LinkedIn executive content services, so the correct transcript is the one where Miriam is selling Virio's services TO the prospect.

**Correct transcript (Miriam selling Virio services) — USE THIS ONE:**
- Summary mentions: LinkedIn content, executive voice, thought leadership, social selling, content strategy, posting cadence, profile optimization, ICP targeting, demand generation through content
- Action items include: content workshop, scoping document, pricing proposal, sample content
- Miriam is explaining Virio's approach, methodology, or pricing

**Wrong transcript (prospect pitching their product to Miriam) — SKIP THIS:**
- Summary focuses on the prospect's product features, technical architecture, or pricing model
- Action items are about Miriam evaluating the prospect's tool or scheduling an internal review
- Miriam is asking questions about the prospect's product, not presenting Virio's services

For example: A company called "ClearVector" might have two Fireflies entries — one where ClearVector demos their security product TO Miriam, and one where Miriam pitches Virio's LinkedIn content services TO ClearVector's marketing team. You want the second one. If the summary mentions "cloud security", "threat detection", or "identity-based" anything, that's the vendor demo — skip it and look for the one about LinkedIn content and executive voice.

### Batch mode

1. Check today's completed calendar events: `gcal_list_events` for today (timeMin = today 00:00, timeMax = now)
2. Filter to external meetings (attendees with non-virio.ai email domains) that have already ended
3. For each meeting, search Fireflies first (`fireflies_search` with attendee name or company), then Granola (`query_granola_meetings`)
4. Skip internal meetings and calls shorter than 10 minutes

Once you have the transcript(s), use `fireflies_get_summary` (for Fireflies) or `get_meeting_transcript` (for Granola) to get the structured data — attendees, action items, key discussion points, and any dates/deadlines mentioned.

## Step 2: Extract Action Items

Go through the transcript summary and full content to identify every commitment made by either side. Don't just rely on whatever the transcript tool labeled as "action items" — those often miss things. Read the actual discussion for commitments that were stated conversationally.

For each action item, extract:

| Field | Description |
|---|---|
| **Task** | Clear, specific description of what needs to happen. Use active voice: "Send ClearVector the case study about Luminary Health" not "Case study to be sent" |
| **Owner** | Who committed to doing this — "Miriam" / "Virio team" for our side, or the prospect's name for their side |
| **Deadline** | If a specific date was mentioned ("by Friday", "next Tuesday", "end of week"), convert to an actual date. If urgency was implied but no date given ("soon", "this week"), set a reasonable default. If no timeline was discussed, leave blank. |
| **Company** | The prospect's company name |
| **Call date** | When the call happened |
| **Context** | One sentence of context — why this matters or what it's connected to (e.g., "Needed before content workshop on April 22" or "Blocker for CEO approval") |
| **Side** | "virio" or "prospect" — whose responsibility this is |

### What counts as an action item

Look for these patterns in the conversation:

**Explicit commitments:** "I'll send you...", "We'll put together...", "Let me get you...", "I'll have my team..."
**Requests accepted:** "Can you send us...?" followed by agreement, "We'll need your..." followed by acknowledgment
**Scheduled events:** "Let's do the workshop on the 22nd", "I'll set up a call with the CTO"
**Conditional next steps:** "Once you send the logos list, we'll...", "After the board meeting, let's..."
**Implicit commitments:** "We should probably..." or "It would be good to..." followed by agreement — these are softer but still worth tracking

### What does NOT count

- General discussion points or observations ("LinkedIn is important for B2B")
- Wishes without commitment ("It would be nice to have...")
- Things already completed on the call itself
- Vague intentions with no specificity ("We should stay in touch")

## Step 3: Check for Duplicates in Notion

Before creating tasks, search the existing "My Tasks" database to avoid duplicates:

1. Use `notion-search` to look for recent tasks mentioning the company name
2. If a matching task already exists (same action, same company, created in the last 7 days), skip it
3. If a similar task exists but with different details, note it in the summary so Miriam can decide whether to merge or keep both

## Step 4: Create Tasks in Notion

For each action item, create a task in the **My Tasks** database (ID: `077843e9-faf8-4a7b-88cb-f5d703b79fd6`).

Use `notion-create-pages` to create the tasks. Each task should include:

**Title format:** `[Company] — [Action item description]`
- Example: `ClearVector — Send Luminary Health case study to Jess`
- Example: `TwelveGrow — Schedule content workshop for April 22`
- Example: `⏳ ClearVector (prospect) — Share target account list by Monday`

For prospect-owned action items, prefix with ⏳ and add "(prospect)" so it's immediately clear this is something Miriam needs to follow up on, not do herself.

**Task properties:**
- Status: "To Do"
- Due date: The extracted deadline (if any)

**Task body content:** Include a brief context block:
```
📞 From call with [Contact Name] at [Company] on [Date]
Context: [One-line context about why this matters]
Owner: [Miriam / Prospect name]
```

### Grouping

If a single call produces 5+ action items, also create a parent task that links them:
- Title: `[Company] — Post-call action items ([Date])`
- Body: Checklist of all the individual items for quick scanning
- This gives Miriam one task to check that encompasses the whole call's follow-through

## Step 5: Output Summary

After syncing, present a clear summary grouped by call:

---
### Action Items Synced — [Date]

**[Company Name]** (call with [Contact], [duration])
📋 [X] action items created in Notion

**Virio's commitments:**
- [ ] [Action item] — due [date or "no deadline"]
- [ ] [Action item] — due [date or "no deadline"]

**Prospect's commitments (follow up if not received):**
- [ ] ⏳ [Action item] — [Prospect name] committed to [date or "no deadline"]

**Already in Notion (skipped):**
- [Any duplicates that were found and skipped]

---

Repeat for each call if batch mode.

End with a total count: "**Total: [X] action items synced from [Y] calls.** [Z] prospect commitments to follow up on."

## Output Files

Always produce a **summary.md** file alongside any Notion tasks created. This file is the primary deliverable — it's what Miriam reads to review what was synced. Save it to the current working outputs directory. The summary.md should contain the full output summary from Step 5 above, including every action item, owner, deadline, and Notion task link.

Even if no external calls are found (e.g., all meetings were internal), write a summary.md explaining what was checked and why nothing was synced. An empty result is still a result worth documenting.

## Important Notes

- **Don't duplicate other skills' work.** This skill creates Notion tasks. It doesn't send follow-up emails (that's daily-followup-drafts) or create HubSpot deals (that's post-call-deal-creator). If those haven't been run yet, mention it in the summary: "Tip: Run daily-followup-drafts to send thank-you emails for these calls."
- **Prospect action items are follow-up triggers.** When the prospect committed to something, the Notion task is really a reminder for Miriam to chase it if it doesn't arrive. Frame these as "Follow up with [person] re: [thing they committed to]" with the deadline being 1-2 days after the promised date.
- **Be specific over complete.** Five specific, actionable tasks are better than ten vague ones. If something from the call is too fuzzy to be a real task, skip it.
- **Deadlines should be real dates.** Convert relative references ("next Tuesday", "by end of week", "after the board meeting next month") to actual calendar dates based on the call date. If you can't determine a specific date, omit the deadline rather than guess wrong.
