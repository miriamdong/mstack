---
name: linkedin-visual-generator
description: >
  Generate a 1080x1080 LinkedIn post visual in Virio's brand style.
  Use this skill whenever the user asks to "make a visual for a post",
  "create a LinkedIn image", "generate a card for this post", "make a graphic
  for LinkedIn", "turn this into a visual", or any request to produce a
  shareable image to accompany a LinkedIn post. Also trigger proactively when
  the user shares LinkedIn post content and hasn't yet made a visual — offer
  to generate one. Outputs a PNG saved to the workspace. Currently supports the
  list/framework card format (Charlie Hills-style save-worthy reference card),
  which is the highest-performing format for thought leadership and hot takes.
---

# LinkedIn Visual Generator

## What this skill does

Takes a LinkedIn post's content and renders a **1080×1080 PNG** visual in
**Virio's brand style** — warm sand-to-mist gradient background, subtle grain
texture, dark near-black type, rounded cards with soft alpha fills, and the
Virio wordmark at the bottom.

The output is a save-worthy **list/framework card** — structured, scannable,
and valuable enough that someone would screenshot it. Think Charlie Hills-style
reference content: numbered items, bold titles, concise descriptions.

---

## Workflow

### Step 1 — Extract the content spec from the post

Read the user's post and extract the key elements. You're identifying:

- **Headline** — the bold contrarian claim or hook (e.g. "GitHub stars ≠ pipeline.")
- **Section label** — the post's category in caps (e.g. "HOT TAKE", "FRAMEWORK", "PLAYBOOK")
- **Topic label** — short context tag (e.g. "Open-Source GTM", "Enterprise Sales")
- **Subhead** — one sentence that expands the headline or sets up the list
- **Items** — 3–6 numbered points. Each has:
  - `num`: "001", "002", etc.
  - `title`: bold 3–6 word label
  - `desc`: 1–2 sentence explanation (keep under ~120 chars for clean rendering)
- **Footnote** — optional one-liner at the bottom (e.g. "Works until Series B. Then it doesn't.")
- **Examples** — optional named companies or tools (e.g. "Teleport · Skyflow")

**3–4 items render best.** 5–6 is fine for dense frameworks. Avoid 7+ — they get cramped.

If the post doesn't have clean numbered items yet, infer them from the post's
key arguments. Your job is to distill the post into the clearest possible
save-worthy visual, not just transcribe it.

### Step 2 — Write the spec JSON

Write the spec to a temp file at `/tmp/virio_card_spec.json`:

```json
{
  "type": "list",
  "section_label": "HOT TAKE",
  "topic_label": "Open-Source GTM",
  "headline": "GitHub stars ≠ pipeline.",
  "subhead": "Here's what breaks after Series B — and what you need instead.",
  "items": [
    {
      "num": "001",
      "title": "Social proof signal",
      "desc": "Stars tell VCs and early buyers you're real. They open doors through your first two rounds."
    },
    {
      "num": "002",
      "title": "Dev-first credibility",
      "desc": "Engineers trust what engineers use. Stars mean the community has vetted you."
    },
    {
      "num": "003",
      "title": "Inbound surface area",
      "desc": "High repo activity pulls devs into your orbit. A free top-of-funnel that compounds."
    }
  ],
  "footnote": "Works until Series B. Then it doesn't.",
  "examples": "Teleport · Skyflow"
}
```

### Step 3 — Run the render script

```bash
python3 /path/to/linkedin-visual-generator/scripts/render_card.py \
  --spec /tmp/virio_card_spec.json \
  --output /sessions/bold-laughing-bardeen/mnt/Linkedin/post_visual.png
```

The script path is relative to where this skill is installed. Use the actual
absolute path to `scripts/render_card.py` in the skill's directory.

Name the output file descriptively, e.g. `post4_visual.png`, `series_b_visual.png`.
Always save to `/sessions/bold-laughing-bardeen/mnt/Linkedin/` so the user can access it.

### Step 4 — Show the user

Read the output PNG and show it inline. Then share the file link:

```
[View your visual](computer:///sessions/bold-laughing-bardeen/mnt/Linkedin/post_visual.png)
```

Ask if they want any tweaks — headline wording, number of items, footnote copy, etc.

---

## Design principles to keep in mind

These aren't arbitrary rules — they're what makes the output look like Virio
and perform on LinkedIn:

**Headline first.** The headline is the biggest element. It should be the
sharpest, most quotable version of the post's central claim. If it's weak,
the whole visual is weak. Punch it up.

**Items should be save-worthy.** Each item should teach something. Not bullet
points of the post — distilled, named concepts someone would write down.

**Keep descriptions tight.** The card gets cramped fast. Each description should
be 1 sentence ideally, 2 at most. If it needs more, the concept needs simplifying.

**Footnote is the kicker.** Used sparingly, the footnote lands the emotional
payoff — the "then it doesn't" moment. Not every card needs one.

**Don't over-brand.** The "Virio" wordmark in the bottom right is sufficient.
No taglines, no URLs, no social handles — these look desperate.

---

## Virio brand reference

| Element        | Value                          |
|----------------|--------------------------------|
| Background     | Warm sand → cool mist gradient |
| BG Left        | rgb(216, 205, 184)             |
| BG Right       | rgb(196, 202, 194)             |
| Primary text   | rgb(26, 23, 20)                |
| Mid text       | rgb(90, 80, 68)                |
| Muted text     | rgb(122, 112, 98)              |
| Card fill      | rgba(26, 23, 20, 20–50)        |
| Font (Bold)    | LiberationSans-Bold            |
| Font (Regular) | LiberationSans-Regular         |
| Canvas size    | 1080 × 1080 px                 |
| Grain seed     | 42 (fixed for consistency)     |

---

## Common issues

**Text overflows a card**: Shorten the description. Aim for under 100 chars per item desc.

**Too many items**: 3–4 is the sweet spot. 5 is OK. 6+ starts to feel cramped.

**Headline too long**: If it wraps to 3 lines it loses impact. Try to keep it to 1–2 bold lines.

**The visual looks too generic**: Make sure the headline is a real claim, not a topic title.
"Why OSS GTM fails after Series B" is a topic. "GitHub stars ≠ pipeline." is a claim.
