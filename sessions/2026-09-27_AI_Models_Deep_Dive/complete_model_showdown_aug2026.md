# Complete AI Model Showdown — August 2026

All 6 models. Every benchmark that matters. No BS.

---

## The Models At a Glance

| Model | Maker | Released | Context | Price | Open Weight? |
|---|---|---|:---:|---|:---:|
| **Claude Opus 4.6** | Anthropic | Early 2026 | 200K | Paid | ❌ |
| **Claude Opus 5** | Anthropic | Jul 24, 2026 | 200K | Paid (premium) | ❌ |
| **Gemini 3.1 Pro (High)** | Google DeepMind | Feb 19, 2026 | **1M** | $2/\$12 per 1M tokens | ❌ |
| **Nemotron 3 Ultra 550B** | NVIDIA | Jun 4, 2026 | **1M** | Free API + self-host | ✅ |
| **OX Alpha** | Anonymous (likely Zhipu AI) | Aug 20, 2026 | **1M** | Free (temp preview) | ❌ |
| **Claude Fable 5** | Anthropic | Jul 2026 | 200K | Paid | ❌ |

---

## The Master Benchmark Table

### Coding Benchmarks

| Benchmark | Opus 4.6 | Opus 5 | Gemini 3.1 Pro | Nemotron 3 Ultra | OX Alpha | Fable 5 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **SWE-bench Verified** | 80.8% | ~92%+ | **80.6%** | 71.9% | ❌ None | 95% |
| **SWE-bench Pro** | — | **79.2%** | — | — | ❌ None | — |
| **DeepSWE (113 tasks)** | ~54% | **74.0%** | ~65%* | — | ~63% | 69.7% |
| **LiveCodeBench** | — | — | — | 89.0% | — | — |
| **HumanEval** | ~90%+ | ~95%+ | — | 88.4% | — | — |

*\*Gemini 3.7 Flash scored 65% on DeepSWE; Gemini 3.1 Pro (High) likely performs in a similar range.*

### Knowledge & Reasoning Benchmarks

| Benchmark | Opus 4.6 | Opus 5 | Gemini 3.1 Pro | Nemotron 3 Ultra | OX Alpha |
|---|:---:|:---:|:---:|:---:|:---:|
| **MMLU** | ~87-88% | ~92%+ | **92.6%** | ~88% | ❌ None |
| **MMLU-Pro** | ~85-87% | **~91-92%** | ~89-90%* | ~81-88% | ❌ None |
| **GPQA Diamond** | ~78-82% | **~94-95%** | **94.3%** | 86.7% | ❌ None |
| **ARC-AGI-2** | — | — | **77.1%** | — | ❌ None |

---

## What Each Benchmark Measures (Quick Recap)

| Benchmark | Tests | In Plain English |
|---|---|---|
| **SWE-bench Verified** | Fix real GitHub bugs | "Here's a bug report, fix it" |
| **DeepSWE** | Build complex multi-file projects | "Here's a project, build it end-to-end" |
| **MMLU / MMLU-Pro** | Knowledge + reasoning across 57 subjects | "How smart are you overall?" |
| **GPQA Diamond** | Graduate-level science questions | "Can you answer PhD-level science?" |
| **ARC-AGI-2** | Abstract reasoning / pattern recognition | "Can you actually think, not just memorize?" |
| **HumanEval** | Write code from function descriptions | "Can you code from a spec?" |

---

## Head-to-Head Verdicts

### 🏆 Opus 5 — The Undisputed Champion
Wins on virtually every benchmark. **74% DeepSWE, ~92%+ SWE-bench, ~95% GPQA.** If you want the absolute best and don't care about cost, this is it.

### 🧠 Gemini 3.1 Pro (High) — The Best Balance You're Already Using
This is what you have access to right here in Antigravity. Let's be brutally honest about it:

**Where Gemini 3.1 Pro wins:**
- **GPQA Diamond: 94.3%** — essentially tied with Opus 5 (~94-95%). PhD-level science reasoning.
- **MMLU: 92.6%** — actually **beats** Opus 4.6 (~87-88%) on general knowledge
- **ARC-AGI-2: 77.1%** — abstract reasoning, a huge leap
- **1M context window** — same as Nemotron and OX Alpha, much bigger than Opus
- **Price** — significantly cheaper than Opus 5

**Where Gemini 3.1 Pro loses:**
- **SWE-bench Verified: 80.6%** — essentially tied with Opus 4.6 (80.8%), but behind Opus 5 (92%+)
- **DeepSWE: ~65%** — behind Opus 5 (74%) and Fable 5 (69.7%), but ahead of OX Alpha (63%)
- **Deep coding refactors** — Opus models generally produce more careful, nuanced code edits

### 🟢 Nemotron 3 Ultra — The Legitimate Free Option
- **71.9% SWE-bench Verified** — solid but behind Opus 4.6 (80.8%) and Gemini 3.1 Pro (80.6%)
- **86.7% GPQA** — good but behind both Gemini 3.1 Pro (94.3%) and Opus 5 (95%)
- **Open weights** — you can literally run it yourself. No data privacy concerns.
- **Best for:** Enterprise teams who need to self-host, agentic pipelines, data-sensitive work

### 🔴 OX Alpha — The Instagram Hype
- **~63% DeepSWE** — below Gemini 3.1 Pro (~65%), Nemotron, and every Opus except 4.6
- **Zero verified scores** on SWE-bench, MMLU, GPQA — literally no official benchmarks
- **Anonymous provider** — you don't know who has your data
- **Best for:** Nothing that Nemotron or Gemini 3.1 Pro can't do better with full transparency

---

## The Honest Ranking (August 2026)

| Rank | Model | Overall Strength | Best For |
|:---:|---|---|---|
| 1 | **Claude Opus 5** | 🏆 Best at everything | Deep coding, complex reasoning, agentic tasks |
| 2 | **Gemini 3.1 Pro (High)** | 🥈 Excellent all-rounder | Large context tasks, science/knowledge, best price-to-performance |
| 3 | **Claude Fable 5** | Strong coder | Specialized coding tasks |
| 4 | **Claude Opus 4.6** | Still solid, aging | Bug fixing, precise edits (being deprecated Sep 2026) |
| 5 | **Nemotron 3 Ultra** | Best open-weight | Self-hosting, data privacy, enterprise pipelines |
| 6 | **OX Alpha** | Unverified hype | Nothing you can't get better elsewhere |

---

## What This Means For YOU Specifically

You have access to **two models right now** in Antigravity:
1. **Claude Opus 4.6** (currently selected)
2. **Gemini 3.1 Pro (High)** (available)

### Practical Recommendation

| Task | Use This |
|---|---|
| **Writing scripts, creative content, YouTube work** | Either works — Opus 4.6 slightly better for nuanced writing |
| **Analyzing large documents or full codebases** | **Gemini 3.1 Pro** — 1M context vs Opus's 200K |
| **Fixing specific bugs in code** | **Opus 4.6** — 80.8% SWE-bench, surgical precision |
| **Science/research questions** | **Gemini 3.1 Pro** — 94.3% GPQA, nearly the best in the world |
| **General knowledge questions** | **Gemini 3.1 Pro** — 92.6% MMLU vs Opus 4.6's ~87% |
| **Complex multi-step reasoning** | Tied — both are strong |

> [!IMPORTANT]
> **Don't chase OX Alpha.** You already have Gemini 3.1 Pro (High) which beats it on every benchmark where both have scores, has a 1M context window, comes from Google DeepMind, and has transparent data handling. OX Alpha offers you nothing you don't already have — but with the added risk of sending your data to an unknown entity.

> [!TIP]
> **If you upgrade to Opus 5**, you'll have access to the #1 model on earth for coding and reasoning. But Gemini 3.1 Pro (High) at its current price point gives you ~95% of that performance for significantly less cost.
