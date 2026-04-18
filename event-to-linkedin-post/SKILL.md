---
name: event-to-linkedin-post
description: Turn event recordings into LinkedIn posts. Scans Granola for conference, panel, summit, or meetup recordings, analyzes the transcript for post-worthy insights, proposes angle options, and drafts a ready-to-publish LinkedIn post using the linkedin-post-writer skill. Use this skill whenever the user says "turn my event recording into a post", "write a post from the conference", "create a LinkedIn post from my event", "make a post from the panel I attended", "post from my recording", "find my event transcript and write a post", or asks to scan transcripts for event content to post about. Also trigger proactively when the user mentions they attended a conference, summit, panel, or meetup and wants to create content from it, or when they ask to scan Granola for event recordings. If the user says something like "find the recording from the event and make a post", this is the skill to use.
---

# Event Recording to LinkedIn Post

This skill bridges the gap between attending events and turning those experiences into high-performing LinkedIn content. It automates what would otherwise be a tedious process: digging through transcript tools, finding the right recording, pulling out insights, and crafting a post.

## Why this skill exists

Miriam attends conferences, panels, and summits regularly. These events are goldmines for LinkedIn content because they contain fresh insights from named industry leaders, real quotes, and specific data points. But the gap between "I attended a great event" and "here's a post about it" is where content dies. This skill closes that gap.

## Workflow

### Step 1: Find the event recording in Granola

Search Granola for event recordings. The key challenge is distinguishing event recordings from regular sales calls and internal meetings.

**How to auto-detect events vs. regular calls:**

Event recordings typically have these signals (use a combination, not just one):
- Title contains words like "conference", "summit", "panel", "keynote", "live", "meetup", "workshop" (but NOT "content workshop" or "sales workshop" which are Virio client calls)
- Multiple speakers who are NOT Virio team members or prospects
- Content covers broad industry themes rather than Virio's specific service offering
- Speakers represent well-known companies, VC firms, or platforms
- The transcript reads more like a panel discussion or presentation than a two-way sales conversation

Regular sales calls typically have these signals:
- Title is "[Person] and Miriam Dong" or "[Company] Content Workshop" or "[Company] <> Virio"
- Two participants (Miriam + one prospect)
- Content focuses on Virio's pricing, onboarding, case studies, or ROI
- Action items involve sending case studies, scheduling follow-ups, or pilot discussions

**Search approach:**
1. Use `list_meetings` with the appropriate time range (default to last 30 days, narrow to "this_week" or "last_week" if the user specifies)
2. Scan titles for event signals
3. If ambiguous, use `get_meetings` to pull the summary and check content signals
4. If multiple event recordings exist, present the options and ask which one to use
5. If no event recording is found, tell the user and ask if they meant a different time range

### Step 2: Pull the full transcript

Once the event recording is identified:
1. Use `get_meeting_transcript` to pull the complete transcript
2. Also use `get_meetings` to get the summary if you haven't already

The full transcript is essential because the summary alone misses the best post material: specific quotes, surprising stats, memorable phrasing, and the back-and-forth dynamics between speakers.

### Step 3: Analyze for post-worthy angles

Read through the transcript and identify 3 to 4 distinct angles that would make strong LinkedIn posts. For each angle, consider:

**What makes a strong angle:**
- A surprising stat or data point that challenges assumptions
- A bold claim from a credible speaker that sparks debate
- A trend or shift that Miriam's audience (B2B founders, marketing leaders, sales executives) would care about
- Something that connects to Virio's thesis (executive content, LinkedIn as a pipeline channel, authenticity over automation) without being salesy
- A quote or moment that was genuinely memorable from the event

**For each angle, provide:**
- A one-line summary of the angle
- Which speaker(s) and company said or demonstrated it
- Why it matters for Miriam's audience
- How it connects to Miriam's work or perspective (if applicable)

**Present the angles and wait for the user's choice.** Do not proceed to drafting until the user picks an angle or asks you to combine angles. This step is important because Miriam knows her audience and current content strategy better than anyone.

### Step 4: Draft the post using linkedin-post-writer

Once the user picks an angle, invoke the `linkedin-post-writer` skill to draft the post. When calling the skill, you already have all the context it needs:

- **Topic**: The chosen angle with full transcript context
- **Goal**: Thought leadership, building credibility as someone who attends and synthesizes top industry events
- **Audience**: B2B founders, marketing leaders, sales executives (Miriam's 20K+ LinkedIn followers)
- **Tone**: Bold but grounded. Data-driven where possible. Personal (she was there)
- **Specific details**: Use real speaker names, their titles and companies, exact quotes or stats from the transcript, and the event name
- **Optimization target**: Default to steady engagement unless the user specifies moonshot

**Important details for the draft:**
- Always use the correct speaker names and titles. If a photo or slide from the event is shared, use those exact names and titles rather than what the transcript's speaker labels say (transcripts often use generic labels like "Speaker A")
- Include the event name to establish credibility and context
- Ground insights in what specific people said, not vague "experts say" framing
- Connect the event insight back to Miriam's own experience at Virio when it's natural and relevant, but don't force it
- Keep the Virio mention brief and towards the end. The post should lead with value, not promotion

### Step 5: Iterate based on feedback

After presenting the draft, the user may want to:
- Swap the hook (offer 1 to 2 alternatives with each draft)
- Add or correct speaker names and titles (especially if they share a photo from the event)
- Adjust tone or length
- Combine elements from multiple angles
- Generate a visual to accompany the post (use the `linkedin-visual-generator` skill if requested)

Stay responsive and iterate until the user is happy with the final version.

## Edge cases

- **No event recording found**: Tell the user clearly. Suggest broadening the time range or checking if the recording landed in Fireflies instead.
- **Multiple events in the time range**: List them with titles and dates, ask which one.
- **Very long transcript** (90+ minutes): Focus on the most quotable and insight-dense segments. Panel Q&A sections and lightning round segments often have the highest density of post-worthy material.
- **User shares a photo from the event**: Use it to verify and correct speaker names, titles, and company affiliations. The photo is the source of truth over transcript labels.
