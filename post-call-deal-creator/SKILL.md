---
name: post-call-deal-creator
description: >
  After sales calls, automatically check Fireflies transcripts for Miriam's completed calls, identify any companies that don't yet have a HubSpot deal, create those deals with correct fields pre-filled, and add a rich qualification note to every deal. Use this skill whenever the user says "create deals from today's calls", "log deals from my calls", "which calls didn't get deals", "add deals to HubSpot", "update HubSpot after my calls", "post-call deal sync", or "log that call". Also trigger automatically when invoked after daily-followup-drafts completes. If the user mentions they just finished a call and need to log it, or says "create a deal for [company]", use this skill. Do NOT wait for the user to explicitly say "skill" — whenever the context is post-call CRM logging, use this skill.
---

## What this skill does

After Miriam's sales calls, look up her Fireflies transcripts, check HubSpot for existing deals, create any that are missing, and add a rich qualification note to capture everything relevant from the call — so Miriam never has to open HubSpot manually after a call.

**Important: Only Miriam's calls**
Only process calls where miriam@virio.ai is listed as an attendee. Skip calls where only other Virio team members are present (david@virio.ai, jon@virio.ai, marghi@virio.ai, etc.) — those are teammates' calls and are not Miriam's responsibility to log.

**Default deal fields:**
- **Amount:** $8,667 (always; Miriam will update if it differs)
- **Close date:** Last day of the current quarter (Q1 = Mar 31, Q2 = Jun 30, Q3 = Sep 30, Q4 = Dec 31)
- **Deal name:** `[Company Name] - [Month Year]` (e.g., "Acme Corp - April 2026")
- **Stage:** First available deal stage in HubSpot pipeline (typically "Appointment Scheduled" or equivalent — check when you open HubSpot)
- **Note:** Full qualification capture from the transcript (see below)

---

## Step-by-step workflow

### Step 1: Get Miriam's completed calls today

Use `fireflies_get_transcripts` to fetch transcripts from today. Filter for:
1. **Miriam must be an attendee** — miriam@virio.ai must appear in the attendee list. Skip any calls she wasn't on.
2. **External calls only** — at least one attendee must have a non-virio.ai email address. Skip purely internal team calls.

If no date is specified, default to today. If the user asks about a different date or "most recent calls," adjust accordingly.

For each qualifying transcript, read the full content and extract the qualification information needed for the deal note (see Step 4).

### Step 2: Check for existing deals in HubSpot

For each company from Step 1, use `search_crm_objects` to search for existing deals associated with that company name. Check deals created in the last 60 days.

- **Deal already exists:** Do not create a new one. Add the qualification note from this call as a new note on the existing deal instead.
- **No deal exists:** Proceed to create one.

### Step 3: Create the deal via HubSpot UI

Open HubSpot in Chrome (`app.hubspot.com`) and navigate to CRM > Deals. For each company that needs a new deal, click "Create deal" and fill in:

- **Deal name:** `[Company Name] - [Month Year]`
- **Amount:** 8667
- **Close date:** Last day of current quarter
- **Deal stage:** First stage in the pipeline
- **Associate contact:** Search for the contact by email; create if not found

After saving the deal, add the qualification note (Step 4).

### Step 4: Write the qualification note

For every deal — whether newly created or existing — add a structured note that captures what happened on this call. Extract as much as you can from the transcript; use "not discussed" for fields where nothing was mentioned.

Use this exact template for the note:

```
[Date] Call with [Contact Name], [Title] at [Company]

**Deal source:** [how did this prospect come in — inbound, outbound, referral, event, LinkedIn, etc.]
**ICP fit:** [how well does this prospect match Virio's ideal customer profile — their role, company size, industry]
**ACV:** [annual contract value discussed or implied, or "not discussed"]
**Deal cycle:** [timeline to close mentioned, or expected cycle length based on context]
**Pain points:** [specific problems they're experiencing that Virio could solve]
**Gap:** [the gap between where they are and where they want to be]
**Objections:** [any hesitations, concerns, or pushback raised on the call]
**Stakeholders:** [who else needs to be involved in the buying decision]
**Budget:** [budget mentioned, implied, or "not discussed"]
**Sales motion today:** [what stage of the sale are we in — discovery, demo, proposal, negotiation, etc.]
**Outbound motion:** [are we running any outbound to this account — if yes, what]
**What's working:** [what resonated with the prospect — what got them excited or engaged]
**What's not working:** [what fell flat, what objections they raised, what needs to change]
**Content strategy today:** [what content are they currently doing, what's their LinkedIn/social presence like]
**Paid ads today:** [are they running paid ads, what channels, what's the budget]
**Agreed next step:** [the specific commitment made — who does what by when]
```

Not every field will have information — "not discussed" is fine. The goal is to create a reliable qualification record from each call so the deal history in HubSpot is actually useful.

### Step 5: Report back

After all deals are processed, summarize:

```
## Deals logged from today's calls

**✅ Created ([N] new deals)**
- [Company Name] — new deal created, stage: [stage]

**📝 Updated ([N] existing deals)**
- [Company Name] — deal exists (created [date]), qualification note added

**⏭️ Skipped**
- [Call title] — not Miriam's call (attendees: [names])

**⚠️ Needs attention**
- [Company Name] — [reason: couldn't determine company, duplicate ambiguity, etc.]
```

---

## Edge cases

**Multiple calls with the same company:** Create one deal and write the note combining insights from both calls.

**Call where Miriam is the only Virio attendee:** Still process it — what matters is that miriam@virio.ai is present, not how many team members joined.

**No transcript content available:** If a call has no transcript or is silent (e.g., a brief silent meeting), skip it and include it in ⚠️ Needs attention.

**No qualifying calls today:** Say so clearly and note the most recent date with Miriam's calls if you can find it: "No calls with miriam@virio.ai found for today. Most recent was [date] — want me to check those?"

**Duplicate deal ambiguity:** If the existing deal is closed-won and today's call looks like a new engagement (different contact, different topic), flag it in ⚠️ Needs attention and ask Miriam whether to create a new deal or update the existing account.

---

## Tools to use

- `fireflies_get_transcripts` — fetch today's call transcripts
- `fireflies_get_transcript` — read the full content of a specific transcript
- `search_crm_objects` — check HubSpot for existing deals by company name
- `mcp__Claude_in_Chrome__navigate` + Chrome tools — create deals in HubSpot UI
- `mcp__Claude_in_Chrome__form_input` — fill in deal fields
