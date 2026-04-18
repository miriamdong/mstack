---
name: linkedin-content-analyzer
description: >
  Analyze a company's LinkedIn content strategy — including posting cadence, content themes,
  executive voices, engagement patterns, and strategic gaps. Use this skill whenever the user
  asks to "look at [company]'s LinkedIn", "analyze how [company] uses LinkedIn", "study
  [company]'s content strategy on LinkedIn", "what does [company] post on LinkedIn", or any
  request to understand a company's LinkedIn presence. Also trigger proactively when prepping
  for sales calls and the user mentions wanting to understand a prospect's content, when doing
  account research, or when the user says "look at their LinkedIn" without specifying what they
  want. Outputs a structured analysis with actionable intelligence including content themes,
  cadence, executive voices, engagement signals, and strategic gaps.
---

# LinkedIn Content Strategy Analyzer

You're analyzing a company's LinkedIn presence to surface strategic intelligence: what they post, how often, who drives their content, what's working, and where the gaps are. This is most useful for sales prep, account research, and competitive intelligence.

## The Core Challenge

LinkedIn is heavily JavaScript-rendered. Navigating to `linkedin.com/company/X/posts/` often returns near-empty page text. Your primary research strategy is **web search**, not browser scraping. Use Claude in Chrome as a supplement for profile verification, but don't depend on it for post content.

---

## Step 1: Identify the Company

Before searching, make sure you know:
- The company's exact LinkedIn URL slug (e.g., `fireflies-inc`, `jellyfish-co`)
- Their main founders/CEO (these are often the primary content voices)
- Their industry and approximate size

If the user didn't specify the LinkedIn slug, navigate to `https://www.linkedin.com/company/[company-name]/` to confirm the right page, then read the company overview text.

---

## Step 2: Gather Data via Web Search (Primary Method)

Run these searches in parallel to gather post content and engagement signals:

1. **Recent company posts:**
   `"[company name]" linkedin post 2025 OR 2026 site:linkedin.com`

2. **Founder/exec recent activity:**
   `"[CEO name]" OR "[co-founder name]" linkedin post "[company name]" 2025 OR 2026`

3. **Viral or high-engagement moments:**
   `"[company name]" linkedin viral OR "went viral" OR "most liked" OR engagement 2025`

4. **Content themes in the wild:**
   `"[company name]" linkedin content strategy OR thought leadership OR posts`

5. **ABM signals:**
   `"[company name]" linkedin "account-based" OR ABM OR "target accounts" OR "named accounts" OR "ICP"`
   Also look for: Are they posting content tailored to specific verticals or company sizes? Do they mention target account lists, intent data, or 1:1 / 1:few marketing? Is their paid content (thought leadership ads) mapped to specific buyer personas or account segments?

The web search results will give you post titles, snippets, and engagement signals that LinkedIn's own interface hides behind a login wall.

---

## Step 3: Navigate to LinkedIn (Supplementary)

Use Claude in Chrome to gather what web search can't provide — profile metadata and any visible posts:

1. **Company page overview:** `https://www.linkedin.com/company/[slug]/`
   - Capture: follower count, employee count, tagline, about section

2. **CEO/founder recent activity:** `https://www.linkedin.com/in/[founder-slug]/recent-activity/all/`
   - The page may render as near-empty text — that's normal. Capture whatever is visible.

3. **Try a direct post URL** if you found one via web search — post pages sometimes render better than feed pages.

Don't spend more than 2-3 browser navigations on this step. If LinkedIn isn't rendering content, move on — web search is more reliable.

---

## Step 4: Synthesize the Analysis

Compile everything into the structured output below. Focus on insights that are actually useful for sales, account research, or understanding the company — not just a list of facts.

---

## Step 5: Produce Virio-Branded One-Pager (Default)

The default output is a **true single-page Virio-branded one-pager** rendered to PDF. The reference for "good" is `https://viriopricing.netlify.app/` — calm, generous whitespace, alternating dark/light blocks, mono kickers, and big confident numerals carrying the page. Match that energy. Markdown output is the explicit-opt-in fallback only.

### 5a. Brand source of truth

Read the `virio-brand` skill SKILL.md for the full color/type/layout system. If the Virio Figma brand book is connected (Figma MCP) and the user asks for a Figma-true output, pull live tokens from there. Otherwise the `virio-brand` skill is the canonical fallback.

### 5a-bis. Logos — USE REAL FILES, NEVER TEXT

**This is the single most important rule in this skill.** Logos are image assets, not text. Always render from SVG files. Never type company names as styled text to fake a wordmark.

**Audience vs. author logos:** The analysis is prepared *by* Virio *for* the subject company. Both logos should appear, with distinct roles:

- **Header — client logo (large, prominent).** The company being analyzed. This is the subject of the document. Upload their official SVG or request one if not provided.
- **Footer — Virio logo (small, "Prepared by" attribution).** The author/deliverer. Render as `Prepared by [virio logo]` at ~16–18px height.

If the analysis is internal (not being delivered to the company), the header can use the Virio logo instead and the footer can simplify. Default to the external-delivery pattern unless the user explicitly says otherwise.

**Virio logo rules:**
- `assets/virio_black.svg` on light backgrounds; `assets/virio_white.svg` on dark backgrounds.
- Never type `virio`, `virio.ai`, or construct a fake wordmark from text + styled dot. That is not the logo.
- The Virio logo includes a hexagon inside the "o" and a red dot at the upper-right of the "o". Do not crop, recolor, or modify.
- Red #CF5E32 is reserved for the dot in the Virio wordmark. Use it elsewhere only sparingly as a single accent (e.g., the 8px dot on the takeaway card). Never as a button, highlight, or paragraph color.

**Client logo rules:**
- Use the official SVG the client provides. If the user uploads a file, save it to `assets/` and reference it.
- Preserve the client's brand colors in their logo. Don't restyle to match Virio's palette.
- If the SVG isn't provided, ask for one — don't substitute a text wordmark.

Copy all SVG files into the output folder's `assets/` subdirectory at the start of every run. Render the PDF with `base_url='.'` so relative paths resolve. If a required SVG can't be located, stop and ask — do not substitute text.

### 5b. This is analysis delivered to the client — not a pitch

The deliverable is an **analysis document prepared for the company being analyzed**. Write it as if handing it to their CMO. That means:

- **No sales framing.** No "Opening Hook" quote, no "Pitch Angle" panel, no "how to sell them" language. The reader is the subject.
- **No accusatory language.** Reframe deficits as observations and opportunities. Don't say "they're missing X" — say "X is the clearest whitespace" or "the next layer of content would address X". Same insight, respectful frame.
- **The takeaway punchlines are observations, not indictments.** E.g., "The rebrand narrative carried 2025. LinkedIn is ready for a second chapter" — not "they never moved past the rebrand."
- **The final section is Strategic Opportunities, not Strategic Gaps.** Same content, forward-looking frame — what to build next, not what's broken. Use labels like "Whitespace" on absent themes rather than "Absent".

**Required sections (in order):**

1. Header (client logo left, doc label right, hairline below)
2. Title + lede (firm context in 2–3 sentences, neutral tone)
3. **Headline Observations** — hero dark card, 3 punchlines (renamed from "The Takeaway" to signal neutrality)
4. **Who Drives the Content** — voices with cadence and style, plus company-page note
5. **Content Themes & Pillars** — row list with Primary / Secondary / Occasional / Whitespace markers (use "Whitespace" not "Absent")
6. **Engagement Signals** — key-value grid (what's working, post-rebrand pattern, earned-to-owned gap, audience composition)
7. **ABM Signals** — key-value grid (current approach, ICP targeting, named-account signals, paid+organic, funnel alignment, scale consideration)
8. **Strategic Opportunities** — numbered list framed as forward-looking moves, not missing items
9. Footer (Prepared by Virio + date)

Do not compress analytical depth to fit a page count — this is a long-form analysis, not a brochure. A full analysis runs 5–6 pages after reasonable trimming. Consolidate trailing pages if the last one holds only 1–2 items + footer.

### 5c. Fonts — embed proper ones, don't fall through to Inter

The previous default (Inter fallback) reads as generic web. Embed Geist (closest Google Font to Haffer's geometric flat-terminal character) and Geist Mono via Google Fonts at the top of the HTML:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
```

Stacks (use these — do not fall back to Inter as the primary):

```css
--font-sans: 'Haffer', 'Geist', 'Söhne', 'Helvetica Neue', sans-serif;
--font-mono: 'Haffer XH Semimono', 'Geist Mono', 'JetBrains Mono', monospace;
```

If the user has actual Haffer files licensed and reachable, embed them via `@font-face` and they take precedence — that's always preferred. Geist is the production fallback.

### 5d. Layout system — minimal, hairlines over cards

The reference is **viriopricing.netlify.app**. Study it. The dominant visual language is typography + thin horizontal rules on Off White, with exactly one or two dark cards per document. No gradients, no colored accent bars, no left-border quote treatments, no card-on-card stacking. The design is mostly negative space.

- **Page background:** Off White #FFF9ED. Plain. No vignette, no grain overlay unless specifically requested.
- **Header row:** Real SVG logo top-left (see 5a-bis), mono doc-label top-right. Thin hairline divider beneath (1px, 10% black). Generous space below (60–80px) before the title.
- **Title block:** Big H1 (36–40pt, weight 500, tight letter-spacing), single lede paragraph (14pt, muted color), generous space (60–80px) before the next block.
- **Hero takeaway:** The ONE dark card per page. Black #1B1B1B, Off White text, border-radius 10px (not 16–20), padding 44×48px. Three columns separated by thin vertical hairlines at 18% offwhite — not gaps, hairlines. Mono `01` `02` `03` markers in Mustard #D5B473. A single 8px Red dot in the upper-right corner as the only accent. Don't overload this block with a headline inside the card — kicker + three columns of prose is enough.
- **Sections below the takeaway:** Plain. Off White background, no card, no border. Structure is just: mono kicker (uppercase, 9pt, muted color, letter-spacing 0.16em) → H2 (20pt, weight 500) → content.
- **Row lists:** When listing gaps, themes, or discount tiers, use the pricing page's row pattern:
  - Hairline above the list
  - Each row: left column title + optional small description, right column mono value/number
  - 18px vertical padding, hairline below
  - No numbered gutters, no colored bars, no filled boxes
- **Voices, themes, stats:** Two-column hairline lists — not tiled cards. Top hairline, bottom hairline on each row.
- **Hook quotes:** Large prose (17pt, regular weight) with curly quotation marks as punctuation. No left border, no red accent, no italic.
- **Closing pitch:** Plain prose paragraph with a top hairline and a kicker. Do NOT use a second dark card for the pitch — the takeaway is the only hero.
- **Color budget:** Black, Off White, and one muted Dark Green / 55% black for secondary text. Blue #476D73 sparingly for one or two accent moments if needed. Mustard only inside the dark card. Red ONLY as the logo dot and the single 8px dot on the takeaway card.
- **Borders and radii:** 1px hairlines at 10% black. Dark card radius 10px. No other rounded corners anywhere.

### 5e. Page sizing — a long, breathing one-pager

The target is a "long one-pager" that naturally runs 2–3 Letter pages when printed. Breathing room is a brand principle — the Virio pricing page (viriopricing.netlify.app) is the reference for how much whitespace is appropriate. Crowding is worse than length.

Concrete rules:

- Body 10.5pt, line-height 1.5. Never smaller than 10pt.
- H1 30–36pt, H2 17–20pt. Only one H1 per page (the company name). Use mono kickers (9pt, letter-spacing 0.2em) as the primary section marker instead of stacking H-levels.
- Section vertical rhythm 28–38px between sections. Never less than 24px.
- The takeaway card is the only hero element above the fold. It gets generous internal padding (32–40px) and stands alone — don't crowd it with a stat grid or other dark blocks on the same page.
- Max one dark card per page spread. The takeaway is dark; the optional closing pitch is dark; everything else is off-white with hairline dividers.
- Max 6 gap-items, max 4 voices, max 8 theme rows. Cut content before cutting spacing.

**Page-count discipline:**
- A full analysis with all six analytical sections will naturally run 5–8 pages. That is the correct length.
- Do NOT compress analytical depth to hit a lower page count. This is a long-form analysis, not a one-page summary.
- Only cut content when it's genuinely thin or redundant — never to fit a target page count.
- Never shrink body below 10pt or delete the takeaway block to save pages.

Allow sections to flow across pages naturally. Only set `page-break-inside: avoid` on atomic blocks (`.takeaway`, `.closing`, `.hook-quote`, `.gap-item`, `.voice`, `.theme-row`) — not on `section` itself, or pages will have awkward empty gaps.

### 5f. Print CSS (required)

**Critical:** page margins go on `@page`, not on a `.page` container div. Otherwise pages 2, 3, 4+ start right at the top edge with no whitespace — an instant tell that the document was built for screen only.

```css
@page {
  size: Letter;
  margin: 0.55in 0.7in;
  background: #FFF9ED;
}
@media print {
  body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .takeaway { page-break-inside: avoid; break-inside: avoid; }
  .row, .voice, .kv, .gap { page-break-inside: avoid; break-inside: avoid; }
  h1, h2 { page-break-after: avoid; break-after: avoid; }
  p, li { orphans: 3; widows: 3; }
}
```

Do NOT set `@page { margin: 0 }` with a padded `.page` wrapper. Every page of a multi-page analysis needs the same top/bottom margins, which only `@page` provides.

### 5g. Render HTML to PDF

Copy the logo SVGs into `outputs/assets/` first, then render with `base_url='.'` so the logo paths resolve:

```bash
# Copy logo assets (adjust source path as needed)
mkdir -p outputs/assets
cp path/to/virio_black.svg outputs/assets/
cp path/to/virio_white.svg outputs/assets/

# Render
pip install weasyprint --break-system-packages --quiet
python3 -c "
from weasyprint import HTML
HTML('[company-slug]-linkedin-analysis.html', base_url='.').write_pdf('[company-slug]-linkedin-analysis.pdf')
"
```

After rendering, verify page count with `pypdf`. If it's >3 pages, cut copy (not type size) before re-rendering.

Share both files via `computer://` links. Lead with the PDF, offer the HTML for edits. Chat summary stays short — restate the 3 takeaways, link the file, list sources. The document carries the rest.

---

## Output Format (Markdown fallback only)

Use this only when the user explicitly opts out of the branded PDF deliverable.

```markdown
## 🔍 [Company Name] — LinkedIn Content Strategy Analysis

**Company Page:** [LinkedIn URL] — [X] followers · [size] employees

---

### Company Overview on LinkedIn
[2-3 sentences: What they say about themselves on LinkedIn, their tagline, positioning]

---

### Who Drives Their Content

List the primary voices in order of activity:

**[Name] ([Title])** — [LinkedIn URL]
- Posting cadence: [e.g., "2-3x/week", "irregular", "monthly"]
- Style: [e.g., "storytelling, personal vulnerability", "data-heavy, authoritative"]
- Best-performing content: [specific example with engagement if known]

[Repeat for each major voice — typically CEO, co-founders, VPs of Marketing/Sales]

**Company Page:** [active/moderate/quiet]
- What it posts: [e.g., "echoes exec posts, product launches, hiring"]

---

### Content Themes & Pillars

What topics do they consistently cover? Rate each by frequency (🔥 primary / ⚡ secondary / 💤 occasional):

| Theme | Frequency | Example |
|-------|-----------|---------|
| [Theme 1] | 🔥 | [Specific post example] |
| [Theme 2] | ⚡ | [Example] |
| [Theme 3] | 💤 | [Example] |

---

### Content Types & Format Mix

- **Text-only posts:** [% or description]
- **Images/carousels:** [description]
- **Videos:** [description]
- **Articles/newsletters:** [description]
- **Reposts/amplification:** [description]

---

### Engagement Signals

What's actually getting traction?

- **Highest-engagement post type:** [e.g., "founder vulnerability stories"]
- **Notable viral moment:** [specific post with context if known]
- **Typical engagement range:** [e.g., "50-200 reactions on exec posts, <20 on company page"]
- **Audience response pattern:** [e.g., "strong from practitioners, limited from buyers"]

---

### Posting Cadence Summary

| Voice | Cadence | Consistency |
|-------|---------|-------------|
| [CEO name] | [X/week or X/month] | [consistent / irregular / declining] |
| [Other exec] | [cadence] | [consistency] |
| Company page | [cadence] | [consistency] |

---

### ABM Signals

Is their LinkedIn content part of a deliberate Account-Based Marketing strategy, or is it broad awareness play?

- **ABM approach:** [Yes / No / Partial — and evidence for your answer]
- **ICP targeting in content:** [Are posts clearly aimed at specific buyer personas, verticals, or company sizes? Or is it generic?]
- **Named account signals:** [Any evidence of 1:1 or 1:few content — posts that reference specific companies, industries, or roles by name?]
- **Paid + organic coordination:** [Are they boosting exec posts as thought leadership ads to target account lists? Any mention of intent data or ABM tools?]
- **Funnel alignment:** [Is their LinkedIn content mapped to funnel stages — or is it all top-of-funnel awareness?]
- **ABM gap or opportunity:** [What's missing from their ABM approach that would make LinkedIn more effective for them?]

---

### Strategic Gaps

This is the most valuable section — what are they *not* doing that represents an opportunity?

- **[Gap 1]:** [Specific description of what's missing and why it matters]
- **[Gap 2]:** [Description]
- **[Gap 3]:** [Description]

---

### Sales / Outreach Angles

How to use this analysis in a conversation with this company:

- **The opening hook:** [One sentence that references something specific from their LinkedIn that opens a conversation]
- **The pain point to surface:** [What their content pattern reveals about what they're struggling with]
- **The proof point:** [What's already working for them that you can build on]
- **The pitch angle:** [How their specific gaps map to what you offer]

---

### Raw Intel

Any specific posts, quotes, or data points worth preserving:

- [Direct quote or post snippet — cite the URL if available]
- [Another data point]
```

---

## Quality Standards

**Be specific.** "They post about AI" is useless. "Their CTO posts 2x/week about developer productivity benchmarks, targeting engineering leaders at Series B+ companies, and gets 300-500 reactions per post" is useful.

**Surface the gap.** The most actionable part of this analysis is always what they're *not* doing. A company posting great top-of-funnel thought leadership but zero ICP-targeted middle-funnel content has a clear, articulable gap. The ABM section is especially important — whether a company is already running ABM (and doing it poorly on LinkedIn) or hasn't started is a key signal for how to pitch them.

**Use evidence.** If you cite an engagement number, explain where it came from. If you're estimating cadence, say so.

**Acknowledge when data is thin.** If LinkedIn's rendering blocked post content and web search came up dry, say so honestly rather than fabricating details. Note what you *do* know (follower count, company size, exec names) and what remains unknown.

**Keep the sales angles sharp.** The "Sales / Outreach Angles" section should feel like something a salesperson could actually say on a call — not generic, but rooted in specific observations from this company's actual LinkedIn behavior.
