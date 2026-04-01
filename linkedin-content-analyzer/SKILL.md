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

## Output Format

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
