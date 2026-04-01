---
name: pipeline-gap-check
description: >
  Scans HubSpot CRM deals, Gmail inbox, and Google Calendar to surface open deals
  that are missing next steps and flags urgent follow-ups the rep needs to take action on.
  Use this skill whenever the user asks to check their pipeline, scan their deals, find
  missing next steps, or get a daily/morning pipeline briefing. Trigger phrases include:
  "check my pipeline", "what deals need attention", "scan my CRM", "pipeline gap check",
  "which deals don't have next steps", "what am I missing in my deals", "morning pipeline
  check", "what should I follow up on today", or any request that combines CRM + inbox
  scanning to prioritize sales actions. Also trigger proactively when the user asks what
  they should work on today from a sales perspective.
---

# Pipeline Gap Check

Your job is to scan the user's HubSpot CRM, Gmail inbox, and Google Calendar, then deliver a concise, prioritized action list that surfaces deals with no next steps and flags anything that needs immediate attention.

## Why this matters

Deals die not from bad pitches but from dropped follow-ups. Your job here isn't just to list deals — it's to cross-reference the CRM with what's actually happening in email and calendar, so the rep walks away knowing exactly what to do next and in what order.

## Step 1: Identify the user and pull their open deals

Call `get_user_details` on HubSpot to get the user's `userId` (which is their `hubspot_owner_id`).

Then call `search_crm_objects` on objectType `deals` with:
- Filter: `hubspot_owner_id = {userId}` AND `pipeline = default`
- Exclude: `dealstage = closedwon` and `dealstage = closedlost`
- Properties to request: `dealname`, `dealstage`, `closedate`, `amount`, `hs_next_step`, `notes_last_updated`, `hs_lastmodifieddate`, `hs_deal_stage_probability`
- Sort by `hs_deal_stage_probability` descending so the most advanced deals come first

## Step 2: Scan Gmail for deal signals (last 48 hours)

Call `gmail_search_messages` with query `is:inbox newer_than:2d` (optionally filtering out obvious noise like `-category:promotions`). Scan for:

- **Prospects asking to reschedule** — these need a same-day reply
- **Meeting recaps** (Fireflies, Granola, WingRep, Fathom) — a recap means a call happened; check if the deal exists and has a logged next step
- **Calendly booking notifications** — a new discovery call that likely has no CRM record yet
- **Replies from known deal contacts** — any domain matching a deal name in your CRM is a signal

## Step 3: Check upcoming calendar for prospect meetings (next 7 days)

Call `gcal_list_events` with `timeMin` = today 00:00 and `timeMax` = 7 days out. Look for meetings whose titles or attendees match a deal name or company in the CRM. Cross-reference: if there's a meeting with a prospect but no next step logged on that deal, flag it — there's a clear next step waiting to be written down.

## Step 4: Cross-reference and identify gaps

Combine the three signals into a unified gap list. Flag a deal as needing attention if any of these are true:
- `hs_next_step` is empty or missing
- `notes_last_updated` is more than 5 days ago
- A contact from that deal emailed in the last 48 hours
- A meeting with that prospect is on the calendar but no next step is logged
- A meeting recap arrived but no deal record exists (new opportunity)

## Step 5: Produce the prioritized action list

Structure the output in this exact order — the rep should be able to read top-to-bottom and take action without re-sorting:

---

**🔴 Urgent — Act Today**
Contacts who emailed asking to reschedule or follow up, and new Calendly bookings not yet in CRM. These cost the rep nothing to handle and lose deals if ignored.

**🟠 High Priority — No Next Step, Stale Notes (>5 days)**
List each deal with: name, stage, days since last note, and a one-line recommended action. Leads with the most advanced deal stage (highest probability).

**🟡 Moderate — Recent Activity, Next Step Not Logged**
Recent meetings or notes exist, but no formal next step. One-line recommendation per deal.

**📥 New Opportunities — Create CRM Records**
Meeting recaps or Calendly bookings with no matching deal. List prospect name, signal source (e.g., "Fireflies recap"), and the meeting date.

---

## Formatting guidance

- Include a direct HubSpot link for every deal: `https://app.hubspot.com/contacts/{accountId}/record/0-3/{dealId}` (get `accountId` from `get_user_details`)
- Keep each deal to 2–3 lines max — this is a morning action list, not a report
- If a deal has an upcoming calendar meeting, mention it inline (e.g., "GraphIQ Sync on Monday 9:30 AM — log this as the next step now")
- End with a one-line summary: total open deals, how many are missing next steps, and how many new opportunities were found
- Don't mention closed deals, internal meetings, newsletters, or event registrations
