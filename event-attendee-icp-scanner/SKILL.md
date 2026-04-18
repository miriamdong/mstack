---
name: event-attendee-icp-scanner
description: >
  Given an upcoming event, pull the attendee list, score each person against Virio's ICP criteria, and produce a ranked Notion page showing who to prioritize — with LinkedIn context, a personalized conversation opener, and pre-event warm-up messages for top targets. Use this skill whenever the user says "prep me for [event]", "who should I talk to at [event]", "scan attendees for [event]", "score the [event] attendee list", "who's going to [event]", or shares a Luma URL and asks who to meet. Also use this skill proactively whenever an event URL appears in conversation context and Miriam seems to be attending — don't wait for an explicit request.
---

## What this skill does

Turns an event URL (or pasted attendee list) into a prioritized hit list: who to talk to, why they're a fit, how to open the conversation, and warm-up messages to send before the event — all in a Notion page Miriam can pull up on her phone at the event.

**Virio's ICP (for scoring):**
- **Tier 1 — Perfect fit:** Founder or CEO at a B2B SaaS company, especially pre-Series B. These people are making content decisions themselves and feel the pain directly.
- **Tier 2 — Strong fit:** Head of Marketing / CMO, Head of Sales / VP Sales, Head of Content / Brand Lead at a B2B SaaS company. The buying decision likely goes through them.
- **Tier 3 — Possible fit:** Marketing, sales, or content role at a non-SaaS B2B company. Worth a conversation but less likely to convert quickly.
- **Not a fit:** Engineers, developers, designers, investors, academics, government. Deprioritize unless they're also a founder.

**Critical ICP note:** Large enterprise brand CMOs (e.g., CMO at AB InBev, Diageo, Walmart) are NOT Tier 1 even though they are "marketing leaders." Virio serves B2B SaaS companies — consumer brands and Fortune 500 enterprises are out of ICP. Never place them above SaaS founders or SaaS marketing leaders.

Company signals that strengthen a fit: post-Series A (have budget), active on LinkedIn (understand content), US-based, <500 employees (still scrappy, not over-resourced on content).

---

## Step-by-step workflow

### Step 1: Get the attendee list

Navigate to the event page using Claude in Chrome. Most events use Luma (lu.ma) — look for the attendees/guests section.

- Extract every visible attendee: name, company, role/title (if shown), profile photo URL, and any other context on the page.
- If the list is paginated or requires scrolling, scroll through and capture all visible entries.
- If the attendee list is fully gated (login required and no public preview), tell Miriam: "The attendee list for [event] is private. If you can share a CSV or list of names, I can score and research them."
- If only partial attendees are visible (e.g., first 20 shown), note this and work with what's available.
- **If the user pastes a list of names directly:** work from that list — do NOT attempt to fetch a URL. Proceed directly to enrichment and scoring.

### Step 2: Enrich each attendee

For attendees where the role or company is unclear, use Clay to enrich:

```
find-and-enrich-list-of-contacts: pass names + companies, get back role, LinkedIn URL, company size, industry
```

If Clay can't find someone, use web search to find their LinkedIn or company page. The goal is to have enough context to score them — you don't need a full dossier, just role + company.

Also note **warm context signals** during enrichment:
- LinkedIn connections (if visible)
- Mutual connections
- Speaking/hosting at this event
- Recent post or article by this person you could reference
- Met previously (if Miriam mentions it)

These signals matter for the Warm Outreach Targets section.

### Step 3: Score and rank

Score each attendee against the ICP framework above and assign them a tier (1, 2, 3, or Skip). Within each tier, rank by:
- How well their company size and stage fits (smaller = more likely to need Virio's help)
- How active their company appears to be on LinkedIn content
- Any event-specific context that makes them warmer (speaking, hosting, mutual connections)

Keep the top 15–20 targets. Skip everyone else unless the total attendee list is small (<30 people), in which case include all.

### Step 4: Write conversation openers

For each Tier 1 and Tier 2 target, write a short, specific opener (2–3 sentences max) that:
- References something real about their company or role (not generic)
- Connects naturally to what Virio does (content strategy, LinkedIn presence, AI-powered content)
- Feels like something you'd actually say at a networking event — casual and genuine, not a pitch

Good opener: *"I saw Tray.io has been really active on LinkedIn lately — are you driving that personally? We work with a lot of SaaS founders helping them turn their sales insights into content."*

Bad opener: *"Hi, I'm Miriam from Virio. We help B2B SaaS companies with AI-powered content strategy."*

The opener should give Miriam a conversation starter, not a sales script.

### Step 5: Draft pre-event warm-up messages

For Tier 1 targets (and top Tier 2 targets) that have a warm signal — speaking at the event, recent LinkedIn post, mutual connection, or notable company milestone — draft a brief pre-event message Miriam can send via LinkedIn DM or email before the event.

The warm-up message should:
- Be 2–3 sentences max
- Give a genuine reason for reaching out (the event, their content, their company news)
- Not pitch Virio — the goal is to make the in-person conversation warmer, not close a deal
- Feel personal and natural, like a message from a peer

Good warm-up: *"Hey Lin — saw you're speaking at HumanX next week! Really looking forward to hearing your take on inference optimization. I'll be there too — hope we get a chance to connect."*

Bad warm-up: *"Hi, I'm Miriam from Virio. We help companies like Fireworks AI with content strategy. Would love to chat at HumanX."*

After drafting, ask Miriam: "Want me to send any of these via LinkedIn? I can do it now or you can review them first."

### Step 6: Create the Notion page

Search Notion for an existing "Events" or "Event Prep" page to place this under. If none exists, create it at the root level.

Create a new page titled: `[Event Name] — [Date] Attendee Targets`

Structure the page as:

```
# [Event Name] — [Date] Attendee Targets

**Event:** [name]
**Date:** [date]
**Location:** [location if known]
**Total visible attendees:** [N]
**Top targets identified:** [N Tier 1 + N Tier 2]

---

## 📌 Bottom Line Recommendation

[2–4 sentences. Is this event worth heavy investment of time? What's the quality of the audience overall — mostly Tier 1/2 fits, or mostly Tier 3/skip? Who are the 2–3 must-meet people and why? Any red flags (e.g., mostly enterprise companies, mostly engineers, speaker list is all out-of-ICP)?]

Example: "This is a high-value event for Miriam — 8 Tier 1 targets in a 250-person event is a great ratio. The AI infrastructure angle means most founders are actively thinking about content. Priority must-meets: Lin Qiao (Fireworks AI), May Habib (WRITER), Aidan Gomez (Cohere). Avoid spending time on the enterprise track — Diageo and Walmart reps are present but firmly out of ICP."

---

## 📊 Attendee Prioritization Matrix

A quick-scan overview of all scored attendees:

| Name | Company | Role | Tier | Warm Signal | Priority |
|------|---------|------|------|-------------|---------|
| Lin Qiao | Fireworks AI | CEO | 1 | Speaking | 🔴 Must-meet |
| May Habib | WRITER | CEO | 1 | Active on LinkedIn | 🔴 Must-meet |
| ... | ... | ... | ... | ... | ... |

Priority legend: 🔴 Must-meet (Tier 1 + warm signal) · 🟠 High (Tier 1) · 🟡 Good (Tier 2) · ⚪ Low (Tier 3/Skip)

---

## 🎯 Tier 1 — Perfect Fit

| Name | Company | Role | Why | Opener |
|------|---------|------|-----|--------|
| ... | ... | ... | ... | ... |

## 💛 Tier 2 — Strong Fit

| Name | Company | Role | Why | Opener |
|------|---------|------|-----|--------|
| ... | ... | ... | ... | ... |

---

## 🔥 Warm Outreach Targets

People with a warm signal — reach out before the event to make the in-person conversation easier.

| Name | Company | Warm Signal | Pre-Event Message |
|------|---------|-------------|------------------|
| ... | ... | Speaking at event | "Hey [Name] — saw you're speaking at [event]..." |

---

## 📬 Recommended Outreach Strategy

[Tactical plan for the event. How should Miriam approach the day?]

Example:
- **Before the event:** Send LinkedIn DMs to speakers (list names) — they're easier to approach post-talk if they already know who you are.
- **Opening reception:** Target Tier 1 founders who don't have a packed schedule — they're often more available at evening events.
- **During sessions:** Sit near [specific person] in the [session name] track.
- **Post-event:** Follow up within 24 hours using the openers as a conversation reference point.

---

## 🔵 Tier 3 — Possible Fit (no openers needed)

| Name | Company | Role | Notes |
|------|---------|------|-------|
| ... | ... | ... | ... |

---

*Scanned [date] · [N] attendees visible · [N] enriched via Clay*
```

Add each target's LinkedIn URL as a link on their name in the table so Miriam can tap through at the event.

### Step 7: Report back

After creating the Notion page, share the link and give a quick summary:
- How many attendees were visible
- How many Tier 1 and Tier 2 targets were found
- The top 3 most promising names with a one-line reason why
- Whether warm-up messages were drafted and which ones are ready to send

---

## Edge cases

**URL resolves to an organizer profile, not a specific event (e.g., lu.ma/cerebralvalley):** Do NOT fabricate attendee lists. Instead, produce a brief output that explains what happened and gives Miriam a clear path forward:

```
## ⚠️ Organizer Profile Detected

The URL you shared ([URL]) resolves to the [Organizer Name] profile page on Luma, not a specific event. I can see they host events, but I can't get an attendee list from the organizer page.

To proceed, please share one of:
1. The URL for a specific [Organizer Name] event (e.g., lu.ma/[event-slug])
2. The date of the event you're attending (I'll try to find the right event page)
3. A list of attendees you already have — paste names and I'll score them
```

**Event is on a platform other than Luma (Eventbrite, Splash, etc.):** Navigate to the event page and adapt — the pattern is the same. Extract names, enrich, score.

**Very large events (500+ attendees):** Don't try to score everyone. Focus on the attendee list's first 50–100 visible entries, note the limitation, and ask if Miriam wants to filter by company type or role first.

**Speaker list only (no general attendee list):** Speakers are almost always worth meeting. Score them as a special category and note they'll be easy to approach post-talk. Use the speaker list as your dataset and flag that general attendees aren't visible.

**Event is tomorrow or very soon:** Prioritize speed over depth. Skip deep enrichment, do quick tier scoring from name + company alone, and get the Notion page created fast. Still write openers for top 3 Tier 1 targets.
