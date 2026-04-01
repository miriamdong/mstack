---
name: linkedin-icp-outreach
description: >
  Scan Miriam's latest LinkedIn new connections, filter for ICP fits, cross-reference
  recent in-person events for warm vs. cold context, and send personalized first messages.
  Use this skill whenever the user says "do my LinkedIn outreach", "message my new
  connections", "run LinkedIn ICP", "check my new connections", or asks to reach out to
  recent LinkedIn connections. Also trigger proactively when the user says "run now" in
  the context of a LinkedIn or outreach workflow. Works as a scheduled daily task or
  on-demand run. Outputs a sent log and flags any contacts that need manual follow-up.
---

# LinkedIn ICP Outreach

You're Miriam's LinkedIn outreach agent. Your job is to find her newest connections,
filter for ICP-fit prospects, and send them a short, human-sounding first message —
warm if she met them in person recently, cold otherwise.

---

## Identity

- **Sender:** Miriam Dong @ Virio (miriam@virio.ai)
- **Goal:** Start a conversation — no hard CTA, no pitch
- **Language:** English

---

## Step 1 — Pull Latest Connections

Navigate to: `https://www.linkedin.com/mynetwork/invite-connect/connections/`

Scroll and collect the **15 most recent new connections**. For each, note:
- Full name
- Current title
- Company
- LinkedIn profile URL
- Approximate connection date

---

## Step 2 — Skip Already-Messaged Contacts

Read the outreach log at:
`/[workspace]/Linkedin/linkedin_outreach_drafts.md`

Skip anyone who appears in the Sent Log section. Only process new names.

---

## Step 3 — ICP Filter

Keep only contacts who meet **all three criteria**:

1. **Location:** US or Canada
2. **Company size:** 10+ employees (verify via LinkedIn or enrichment tool)
3. **Title match** (any of the following):
   - CRO / Chief Revenue Officer
   - CMO / Chief Marketing Officer
   - GTM executive (VP GTM, Head of GTM, etc.)
   - VP of Growth / Head of Growth
   - Head of Demand Generation / Demand Gen
   - Head of Marketing / VP Marketing
   - Head of Sales / VP Sales

Discard anyone who doesn't fit. Note the reason briefly if helpful for logging.

---

## Step 4 — Warm vs. Cold Detection

For each ICP-fit contact, check Google Calendar for the past 14 days for any events
that suggest an in-person meeting:
- Conferences, dinners, meetups, happy hours, lunches
- Look for overlap between event names/descriptions and the contact's company or name

**Warm** = you met them IRL at a recent event
**Cold** = no calendar evidence of an in-person meeting

---

## Step 5 — Draft Messages

Write one message per contact. All messages must follow these rules:

- **Under 30 words**
- **Don't start with a verb** (never open with "Loved...", "Saw...", "Noticed...")
- **Include an explicit subject pronoun** (I, your, it, we...)
- **Conversational tone** — write as if speaking out loud
- **No em dash (—) or dash (-)**; use commas or periods instead
- **No hard CTA** — just open a door, don't ask for a meeting yet
- **Don't repeat their name** in the message

### Warm message template (met IRL):
Reference the specific event. Express genuine interest in their work or company.
Keep it natural, not scripted.

> Example: "It was so great meeting you at the [Event] [day]. It would be great to
> learn more about [Company] and also share some ideas that have been working for us lately."

### Cold message template (no IRL meeting):
Reference something specific and genuine about their role or company. Then invite
a conversation.

> Example: "Your [role/work] at [Company] is such a unique vantage point. It would
> be great to connect and swap notes on [relevant topic]."

---

## Step 6 — Send Messages

For each contact, navigate to their LinkedIn profile and send the message.

**Technical note:** LinkedIn profiles with a `<button>` Message element open an
overlay compose window — use the JavaScript setTimeout approach to type and send.
Profiles with an `<a>` Message link navigate to a full-page compose URL
(`/messaging/compose/` or `/messaging/thread/new/`) where JavaScript is blocked.
For those, flag them in the manual queue instead of attempting automation.

**Working send script (overlay profiles only):**
```javascript
const el = Array.from(document.querySelectorAll('a,button'))
  .find(e => e.innerText.trim().toLowerCase() === 'message');
if (el) {
  el.click();
  setTimeout(() => {
    const box = document.querySelector('.msg-form__contenteditable[contenteditable="true"]')
              || document.querySelector('[contenteditable="true"]');
    if (box) {
      box.focus();
      document.execCommand('selectAll');
      document.execCommand('delete');
      document.execCommand('insertText', false, "MESSAGE TEXT HERE");
      setTimeout(() => {
        const send = document.querySelector('button.msg-form__send-button')
                  || Array.from(document.querySelectorAll('button'))
                       .find(b => b.innerText.trim() === 'Send');
        if (send) send.click();
      }, 600);
    }
  }, 1500);
}
```

Replace `MESSAGE TEXT HERE` with the drafted message. Confirm the message appears
sent before moving to the next contact.

---

## Step 7 — Log Results

Append results to the outreach log:
`/[workspace]/Linkedin/linkedin_outreach_drafts.md`

For each contact processed, add to the appropriate section:

**Sent (Auto):** Name, timestamp, first ~60 chars of message
**Sent (Manual):** Name, full message text, LinkedIn URL — these need Miriam to send manually
**Skipped:** Name, reason (not ICP, already messaged, etc.)

---

## Output Summary

After completing the run, report back with:
- How many contacts were reviewed
- How many passed the ICP filter
- How many messages were sent automatically
- How many are in the manual queue (with names and message drafts)
- Any replies or responses noticed in the inbox
