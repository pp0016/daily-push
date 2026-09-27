# YouTube Channel Niche Audit & RPM Strategy Session

## Overview
This folder contains the complete backup of our deep-dive session into YouTube channel analytics, specifically exposing the flaws in AI-driven demographic models (NexLev) and creating a definitive, bulletproof system for estimating YouTube channel revenue.

## Key Discoveries
1. **NexLev's Geography Hallucination:** We proved that NexLev applies a default Western demographic template (~40% US) to unauthenticated channels. This causes it to wildly inflate the RPM and Revenue for Hindi/regional channels (like FactTechz and NeonMan).
2. **vidIQ AI Coach Flaws:** We discovered that while vidIQ is great at assigning category-specific RPMs, its AI Chatbot hallucinates 30-day view counts (e.g., claiming 55K views for a dead channel getting 5K).
3. **The Hybrid Methodology (The Truth):** The only way to get accurate revenue estimates is to combine tools:
   - Use **NexLev API** to get the exact 30-Day Long-Form Views.
   - Use **vidIQ Category RPMs** (The 'RPM Oracle' prompt).
   - Manually calculate: True Views × Mid RPM = True Revenue.

## Artifacts Included
- **Channel Audits (.md):** Detailed audits for Brain Station Advanced, PsychToonsHQ, Cosmic Explainer, FactTechz, NeonMan.
- **Niche Ease Comparison:** A master document comparing 10 niches based on replication difficulty, cost, and true revenue potential.
- **Skill Created:** youtube-revenue-truth.md — The custom skill we built, containing the exact rules of when to trust which tool, and the "MASTER PROMPT: YouTube RPM Oracle" to feed into vidIQ.
- **Full Transcripts:** The raw JSONL logs of the entire conversation.
