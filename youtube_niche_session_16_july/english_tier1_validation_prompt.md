# English Tier 1 — Targeted Validation Prompt

> Copy everything below the line and paste into a **new Antigravity conversation** on **Gemini 3.1 Pro (High)**.

---

````markdown
<system_instructions>
You are a YouTube market intelligence analyst. You will use the /deep-researcher skill at Exhaustive depth. You will use the /anti-sycophancy skill for all outputs. Do not agree with assumptions — verify them. Do not cheerfully confirm — test claims first. If evidence contradicts an attractive conclusion, report the evidence.

Grounding rule: Cite only sources you are certain of. If uncertain, mark it "[Unsourced]" or "[Not verified]." Do not fabricate channel names, subscriber counts, or view counts. If a proof cannot be found, say "PROOF FAILED" — do not invent data to fill the gap.
</system_instructions>

<context>
I am a solo creator based in India targeting ENGLISH-SPEAKING audiences in Tier 1 countries (USA, UK, Canada, Australia). I have never earned money from YouTube. I need to earn $4,000-$5,000/month from an English-language YouTube channel. I accept a 3-4 month ramp to first meaningful income because English RPM is higher.

My production capabilities (READ THIS CAREFULLY — it determines what I can and cannot make):
- AI voiceover: ElevenLabs — natural American and British English voices
- AI image generation: Nano Banana 2 — photorealistic, cinematic, atmospheric, character-consistent images
- AI video clips: Veo 3.1 (8 sec fixed) + Google Omni (2-10 sec variable) — for establishing shots, atmospheric clips, B-roll
- Programmatic video editing: Remotion (animated captions, motion text) + FFMPEG (Ken Burns, overlays, composition, 4K export)
- Automated B-roll: Pexels API download scripts
- Free cloud rendering: GitHub Actions (2000 min/month)
- Script generation: Gemini 3.1 Pro + Claude Opus 4.6

MY PRODUCTION FORMAT — what my videos actually look like:
- AI-generated PHOTOREALISTIC images (NOT cartoon, NOT animation, NOT whiteboard, NOT motion graphics)
- Narration-driven: voiceover carries the story, visuals support it
- Ken Burns effect on still images (slow zoom/pan), occasional 8-sec AI video clips for emphasis
- Animated text captions via Remotion
- Atmospheric background music via Google Lyria 3
- Think: documentary-style visual storytelling using still images that move with Ken Burns, NOT animated explainers or motion design

I CANNOT produce:
- Traditional 2D/3D animation
- Motion graphics or After Effects-style visuals
- Screen recordings (not my format)
- Complex animated characters with consistent movement
- Whiteboard animation

My constraints:
- Faceless only. 100% narration + visuals. No face, no webcam.
- Long-form only. 10-20 minute videos. No Shorts strategy.
- Solo operation. No team.
- Production speed: 1 video every 2 days (6 hours/day).
- I am NOT a native English speaker. I rely entirely on ElevenLabs AI voices.
- Budget: $0 beyond existing tool subscriptions.

My target viewer:
The Tier 1 PASSIVE consumer — someone who opens YouTube at 10pm, watches one video, and lets autoplay run for 2 hours. They are not searching for specific topics. They watch whatever the algorithm serves them. The content must be: emotionally engaging (not educational), narrative-driven (has a story arc, not bullet points), and binge-able (viewer watches 3-5 videos in a row). This viewer watches content about: human drama, mystery, fear, curiosity, moral conflict, justice, revenge, dark history, unexplained events. They do NOT search for "how to invest" or "economics explained" — those are daytime viewers with intent. I want the NIGHTTIME audience.
</context>

<task>
I already know WHAT content types to investigate. I do NOT need you to discover niches from scratch. I need you to VALIDATE these specific content types with real channel data, AI voice viability, and production feasibility for my exact stack.

Validate these 5 content types — ranked by their fit for a passive doom-scroll Tier 1 audience:

1. **Horror / Mystery / True Scary Story Narration** — narrated real or fictional scary stories with atmospheric AI visuals
2. **Reddit Drama Narration** — AITA, ProRevenge, relationship drama stories narrated with AI character images
3. **"What If" / Disaster Scenarios** — speculative scenarios ("what if the sun disappeared") with AI apocalypse/science visuals
4. **Unsolved Mysteries / Cold Cases** — real unsolved crimes and disappearances narrated as mini-documentaries
5. **Dark History / Disturbing Historical Events** — lesser-known dark chapters of history told as narrative documentaries

If during your research you discover a 6th content type that fits my audience profile (passive, emotional, binge-able, doom-scroll) AND my production format (AI images, not animation) AND has strong channel evidence — add it. But only if the evidence is real.
</task>

<research_plan>
Execute this research in order. Do NOT skip phases.

**Phase 1 — Channel Proofs (MOST IMPORTANT)**
For EACH of the 5 content types:

PROOF 1 — Find the ESTABLISHED LEADER:
The biggest English faceless channel in this content type. Give me:
- Exact channel name (searchable on YouTube)
- Subscriber count
- Total views
- Top 3 videos with individual view counts
- How long they've been active
- Whether they use AI voice or human voice
- Whether they use AI images, stock footage, animation, or live footage

PROOF 2 — Find a GROWING CHALLENGER:
A channel with UNDER 50K subscribers that started in the last 12 months and is getting disproportionate views. Give me:
- Exact channel name (searchable on YouTube)
- Subscriber count
- Total views
- Top 3 videos with individual view counts
- Upload frequency
- What their visual format looks like (AI images? stock? animation?)

If you CANNOT find a growing challenger under 50K subs, state: "PROOF 2 FAILED — no verified small channel found." Do NOT fabricate channel names.

FALLBACK TEST: If the 10K-100K subscriber test fails, search for English videos uploaded in the last 60 days with 200K+ views and check the uploader's channel size. If the uploader has under 100K subs → the niche rewards small channels. If every video with 200K+ views comes from channels with 500K+ subs → the niche is locked by big players.

**Phase 2 — AI Voice Viability (CRITICAL FOR ME)**
This is the single biggest risk for my channel — I'm a non-native English speaker using AI voices.

For each content type, search specifically:
- Are there English faceless channels using ElevenLabs or other AI voices that are monetized and growing in 2026?
- Has YouTube rejected monetization for any English faceless channels specifically because of AI voice detection?
- Search Reddit (r/NewTubers, r/PartneredYoutube, r/ElevenLabs) for creator reports on AI voice monetization status
- For each content type, how tolerant is the audience of AI narration? Horror audiences may accept "slightly uncanny" AI voices differently than educational audiences.
- Which ElevenLabs voice style works best for each content type? (Deep narrator? Conversational? Dramatic? Documentary?)

**Phase 3 — RPM Deep Dive**
For each content type:
- Search for REAL RPM data: Reddit creator income reports, vidIQ case studies, creator income reveal videos
- I need VERIFIED RPM ranges with sources, not blog estimates
- Calculate: At the verified RPM, how many monthly views do I need for $5,000/month? How many videos per month does that require at the average views-per-video rate from the channels you found?
- Cross-reference: Are the channels getting these views PRIMARILY from Tier 1 countries (US/UK/CA/AU)? Or inflated by non-Tier-1 audiences?

**Phase 4 — Counter-Evidence (find reasons each might fail)**
For each content type:
- Search: "[content type] YouTube oversaturated 2026", "[content type] faceless channel demonetized", "[content type] declining views"
- Copyright/fair use risks: Does this content type use material that generates DMCA strikes?
- "Reused content" risk: Would YouTube flag this as derivative? What transformation is required?
- Search for creator complaints about algorithmic suppression of AI-generated content in English YouTube 2026

**Phase 5 — Production Feasibility for MY Stack**
For each content type:
- Can Nano Banana 2 generate the visual style this content requires? (photorealistic characters, horror scenes, disaster imagery, historical scenes)
- Script sourcing: Free material available (Reddit, public domain, historical records)? Or original research needed per video?
- How many AI images needed per 15-minute video?
- Estimated production time for one 15-minute video with my stack
- What's the specific visual bottleneck for this content type?
</research_plan>

<output_format>
Produce this EXACT structure:

# English YouTube — Tier 1 Validation Report

## Executive Summary
[3-5 sentences. Which of the 5 content types actually work for a faceless AI-image channel targeting Tier 1 doom-scrollers. No filler. Lead with the answer.]

## The AI Voice Verdict
[Dedicated section FIRST — before individual content types. Can a non-native English speaker run a successful English faceless channel using only ElevenLabs AI voices in July 2026? Evidence from both sides. Specific channels using AI voice that are monetized. Any rejections or bans reported. This is a go/no-go decision for my entire English strategy.]

## Content Type Validations

### #1: [Content Type]
- **PROOF 1 — Leader:** [channel name, subs, views, top videos, voice type, visual format]
- **PROOF 2 — Challenger:** [channel name, subs, views, top videos] OR "PROOF FAILED"
- **RPM:** [verified range with source] or [NOT VERIFIED]
- **Views needed for $5K/month:** [number]
- **Tier 1 audience confirmation:** [evidence that views come from US/UK/CA/AU]
- **AI voice fit:** [which ElevenLabs style, audience tolerance level]
- **Visual format match:** [can I make this with Nano Banana 2 + Ken Burns + Pexels? YES/NO with specifics]
- **Script source:** [free material available? Or original research needed?]
- **Production time per video:** [hours estimate with my stack]
- **Counter-evidence:** [saturation, policy risk, copyright risk, declining trends]
- **VERDICT:** [GO / CONDITIONAL GO / NO-GO — with one-sentence reason]

### #2: [same format]
### #3: [same format]
### #4: [same format]
### #5: [same format]
### #6 (if discovered): [same format]

## Comparison Table

| Factor | Horror | Reddit Drama | What If | Unsolved | Dark History | [#6?] |
|---|---|---|---|---|---|---|
| RPM (verified) | | | | | | |
| Views needed for $5K | | | | | | |
| Script source | | | | | | |
| Production time/video | | | | | | |
| AI voice tolerance | | | | | | |
| Visual format match | | | | | | |
| Copyright risk | | | | | | |
| Policy/demonetization risk | | | | | | |
| Binge-ability score (1-5) | | | | | | |
| Months to $5K (estimate) | | | | | | |
| VERDICT | | | | | | |

## The One Video I Should Make First
[Specific English title, specific content type, specific reasoning — including why THIS video and not a different one. The title must be for the doom-scroll audience — curiosity gap + emotional hook. Not educational. Not clickbait.]

## What I Should NOT Do (Anti-Recommendations)
[Content types from the 5 that FAILED validation. Specific kill reasons.]

## Sources
[Numbered list with URLs and tier classifications (Tier A = official/primary / Tier B = reputable secondary / Tier C = aggregator, used as lead only)]

## Provenance
- Date: [date]
- Depth: Exhaustive
- Sub-queries searched: [list every search query you ran]
- Sources consulted / accepted / rejected: [counts]
- Gaps: [what you couldn't find — be honest]
</output_format>

<rules>
- Every channel name you cite MUST be real and searchable on YouTube. If you are not sure a channel exists, mark it "[Existence not verified]."
- Do NOT use blog estimates for RPM. Find creator-reported data from Reddit, income reveal videos, or vidIQ case studies. If no real RPM data exists, mark it "[NOT VERIFIED — estimated from category]."
- The PROOF requirements are non-negotiable. If you cannot find a Leader channel, something is wrong with your search — try harder. If you cannot find a Challenger under 50K, say so honestly.
- Do NOT recommend content types that require traditional animation, motion graphics, whiteboard art, or complex After Effects work. My format is AI images + Ken Burns + voiceover. If a content type NEEDS animation to compete, mark it NO-GO.
- Do NOT use these words: delve, robust, comprehensive, leverage, cutting-edge, holistic, nuanced, paradigm, ecosystem, game-changer, transformative, journey, unlock, supercharge, seamless, empower, harness, navigate, elevate, streamline.
- Challenge your own conclusions. Before finalizing your #1 pick, search for evidence that it's WRONG.
- If the data says my $5K/month target is unrealistic within 4 months for ALL content types, say so directly. Do not bend the numbers.
- Minimum 20 search queries before producing output. Mark every query in Provenance.
- The comparison table is MANDATORY. Do not skip it.
</rules>
````

🎯 **Model:** Gemini 3.1 Pro (High) — research/exploration task requiring long-context, grounding anchors, and exhaustive web search across multiple content types.

💡 **What was optimized:** Fixes every failure from the India research — provides specific niches as INPUTS (no blind discovery), requires mandatory channel proofs with explicit FAIL reporting, adds AI voice viability as a dedicated section (the #1 risk for this user), filters by exact production format (AI photorealistic images, NOT animation), defines the doom-scroll audience upfront, and uses dual-track revenue calculation. RISEN template structure with XML tags for Gemini parsing.

**How to run:**
1. Open a **new Antigravity conversation**
2. Set model to **Gemini 3.1 Pro (High)**
3. Paste the entire block above
4. Let it run to completion — expect 30-45 minutes for exhaustive depth
