# SOURCE OF TRUTH — AI-Powered YouTube Title Optimizer
### Research Project by P.A.D.B. Pathiraja (29071) · BSc (Hons) Software Engineering · NSBM Green University

> **Purpose of this document:** Single authoritative reference feeding all design, development, and writing decisions for this research project. Every claim here is grounded in published research or verified empirical data. Update this document as the project evolves — never let code or writing contradict it.

---

## Table of Contents

1. [Project Identity](#1-project-identity)
2. [Problem Statement](#2-problem-statement)
3. [Research Questions](#3-research-questions)
4. [Research Methodology](#4-research-methodology)
5. [The Research Gap](#5-the-research-gap)
6. [Theoretical Foundation](#6-theoretical-foundation)
7. [YouTube Algorithm & CTR — Empirical Facts](#7-youtube-algorithm--ctr--empirical-facts)
8. [Title Engineering — Empirical Rules](#8-title-engineering--empirical-rules)
9. [Psychological Triggers Taxonomy](#9-psychological-triggers-taxonomy)
10. [Existing Solutions & Their Limits](#10-existing-solutions--their-limits)
11. [System Architecture](#11-system-architecture)
12. [Agent Design](#12-agent-design)
13. [Prompt Engineering Techniques](#13-prompt-engineering-techniques)
14. [Technology Stack — Justified](#14-technology-stack--justified)
15. [Dataset Strategy](#15-dataset-strategy)
16. [Machine Learning — Virality Score Model](#16-machine-learning--virality-score-model)
17. [Semantic Faithfulness & Anti-Deception Layer](#17-semantic-faithfulness--anti-deception-layer)
18. [Generative Ethics Framework](#18-generative-ethics-framework)
19. [Evaluation Metrics](#19-evaluation-metrics)
20. [Limitations & Future Work](#20-limitations--future-work)
21. [Key References](#21-key-references)

---

## 1. Project Identity

| Field | Value |
|---|---|
| **Project Title** | AI-Powered Proactive YouTube Title Optimizer |
| **Short Name** | YTO (YouTube Title Optimizer) |
| **Student** | P.A.D.B. Pathiraja |
| **Student ID** | 29071 |
| **Program** | BSc (Hons) Software Engineering |
| **Institution** | NSBM Green University |
| **Presented** | March 2026 |
| **Domain** | NLP · Generative AI · Recommender Systems · Behavioral Psychology |

### Core Thesis

A multi-agent generative AI system implemented as an **API Wrapper** that **proactively** analyzes a YouTube video's content and automatically produces psychologically optimized, virality-engineered titles — while an integrated ethical layer ensures the generated titles do not factually contradict the source video. This bridges the operationalized gap between psychological theory (Information Gap Theory, loss aversion, social proof) and algorithmic content generation.

---

## 2. Problem Statement

### 2.1 The Scale Problem

- **500 hours** of video are uploaded to YouTube every single minute (YouTube internal data, widely cited).
- This means discovery — not quality — is the primary determinant of a video's success.
- The first decision a viewer makes is based entirely on the **title and thumbnail**, a judgment made in milliseconds.

### 2.2 The CTR Cold-Start Death Loop

YouTube's recommendation algorithm runs a continuous **exploration-exploitation loop**:

1. A new video is shown to a **small test cohort** of users.
2. If CTR is strong in this test window, the algorithm expands distribution.
3. If CTR is weak, the algorithm stops recommending the video — regardless of its intrinsic quality.
4. A video that fails the cold-start test is effectively **dead on arrival**, even if the content itself is excellent.

This creates an asymmetric problem: *a single poorly written title can permanently bury high-quality content.*

### 2.3 The Skill Gap

Professional copywriters use heuristic mastery of psychological triggers — curiosity gaps, urgency framing, loss aversion, social proof — to craft high-CTR titles. This expertise is:
- **Unscalable**: can't be applied to every upload
- **Inaccessible**: most content creators lack this training
- **Inconsistent**: even experts produce flat titles under time pressure

### 2.4 The Metadata Bottleneck

A video's metadata (title, description, tags) is disproportionately influential relative to the video content itself. The algorithm uses metadata to initially categorize and surface a video before it has any watch-time signals.

---

## 3. Research Questions

### 3.1 Main Research Problem

Content creators and digital marketers face a critical efficiency and capability bottleneck: they struggle to consistently generate video metadata (specifically titles) that effectively leverage complex psychological triggers for high Click-Through Rates (CTR). This is due to the difficulty of scaling manual copywriting expertise and the "black box" nature of generic AI tools, which often produce mediocre or hallucinatory results. Consequently, high-quality content often underperforms in algorithmic recommendation systems due to suboptimal packaging.

### 3.2 Specific Research Questions

**RQ1:** How can specific linguistic patterns associated with "virality" (e.g., high-arousal sentiment, information gaps, negative superlatives) be systematically codified into Few-Shot and Chain-of-Thought prompt templates for Large Language Models?

**RQ2:** What is the optimal software architecture for an API Wrapper that integrates LLM generation with a validation layer to ensure titles are not only engaging (Predicted CTR) but also semantically faithful to the source content (hallucination-free)?

**RQ3:** To what extent do LLM-generated titles optimized with "viral" prompt strategies outperform baseline human-generated titles and generic zero-shot AI titles when evaluated against predicted virality metrics and human preference?

**RQ4:** How can "LLM-as-a-Judge" evaluation patterns be utilized to automatically score and filter generated titles based on their adherence to specific marketing rubrics (Curiosity, Urgency, Relevance)?

---

## 4. Research Methodology

### 4.1 Research Strategy: Design Science Research (DSR)

This project adopts a **Design Science Research (DSR)** strategy. DSR is a research paradigm used in Information Systems and Engineering that focuses on the creation and evaluation of innovative **artifacts** (constructs, models, methods, or instantiations) to solve identified practical problems. Unlike natural sciences that describe existing phenomena, Design Science creates new reality through the design of useful objects.

**Why DSR:** The primary output is a novel software system (the AI Title Generator API Wrapper) solving the practical problem of low video engagement. DSR allows an iterative "Build and Evaluate" cycle where theoretical knowledge (Information Gap Theory) is instantiated into the artifact, and the artifact's performance contributes back to the knowledge base. DSR emphasizes both **Rigor** (adherence to scientific theories and evaluation methods) and **Relevance** (solving a real-world business problem).

**Source:** Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). "A Design Science Research Methodology for Information Systems Research." *Journal of Management Information Systems*, 24(3), 45–77.

### 4.2 Peffers' DSRM Process — Six Activities

| Activity | Description | Where Addressed |
|---|---|---|
| 1. Problem Identification & Motivation | Define the CTR bottleneck; justify the value of a solution | §2 Problem Statement |
| 2. Define Objectives | API accepting transcripts/summaries → optimized titles; balance virality with integrity | §1 Core Thesis, §3 RQs |
| 3. Design & Development | Architecture, prompt engineering, algorithm implementation | §11–§13 |
| 4. Demonstration | Apply to diverse test cases (Educational, Entertainment, Tech) to prove feasibility | Prototype demo phase |
| 5. Evaluation | Quantitative (pCTR, BERTScore, Self-BLEU) + qualitative (human survey) | §19 |
| 6. Communication | Dissertation + potential academic publication | Final thesis |

---

## 5. The Research Gap

### 5.1 Proactive vs. Reactive

| Existing Tools | This System |
|---|---|
| Reactive — user asks for a title | Proactive — system automatically generates after analyzing content |
| Single-shot generation | Multi-agent pipeline with self-critique |
| No virality scoring | Predicted CTR (pCTR) score from ML model |
| No factual validation | NLI-based deception detection |
| No psychological grounding | Explicit operationalization of psychological theory |

### 5.2 Operationalizing Psychological Theory

There is a **documented gap in the academic literature**: psychological theories like Information Gap Theory are widely cited in clickbait research but are *rarely implemented as explicit algorithmic prompts in generative AI systems*. This project closes that gap by encoding each trigger as a specific LLM prompt instruction (see §13 Prompt Engineering Techniques).

### 5.3 The Ethics Gap

Most existing tools optimize either for:
- **Clicks** (marketing tools) — no truth constraint
- **Truth** (fact-checking tools) — no optimization for engagement

No existing tool occupies the middle space: **optimizing for virality while guaranteeing factual faithfulness**. This project defines that middle space as **Generative Ethics**.

### 5.4 The "Proactive Data Systems" Gap

Existing academic work treats LLMs as reactive entities — the user prompts, and the model answers. There is limited work on **Proactive Data Systems** in the context of video metadata: architectural frameworks that automatically decompose title generation into sub-agents (Analyzer → Generator → Critic) without user intervention. This project fills that gap by designing an API Wrapper that encapsulates this complex workflow.

---

## 6. Theoretical Foundation

### 6.1 Information Gap Theory (Loewenstein, 1994; Golman & Loewenstein, 2018)

**Core Claim:** Curiosity arises when a person perceives a gap between what they know and what they *want* to know. This gap creates psychological tension that motivates information-seeking behavior (clicking).

Golman & Loewenstein (2018) further refined this: the **salience of the gap** matters — we are most curious about things we already know a little about. Partial information increases curiosity more than zero information.

**How it applies to titles:**
- A title that reveals just enough to identify a topic but withholds the resolution creates a curiosity gap.
- Classic form: *"You Won't Believe What Happens When..."* — the gap is explicit.
- Sophisticated form: *"I Tried Every $1 Restaurant in Tokyo"* — the gap is "what happened?" + implied surprise.

**Academic support:**
- Loewenstein (1994) — original theoretical paper
- Golman & Loewenstein (2018) — salience refinement
- Peer-reviewed studies confirm that curiosity-gap headlines significantly increase click behavior (PMC 2022)
- *However*, research also shows **diminishing returns**: when curiosity-gap headlines became ubiquitous (e.g., Upworthy circa 2014), platforms (Facebook, YouTube) adjusted algorithms to penalize them (Nature, 2024)

**Design implication:** The system must generate curiosity gaps that are **specific** (not generic), **authentic** (grounded in actual video content), and **non-deceptive** (resolved by watching the video).

### 6.2 Prospect Theory & Loss Aversion (Kahneman & Tversky, 1979)

**Core Claim:** People respond more strongly to the potential for *loss* than equivalent *gain*. Losses loom approximately **2x larger** than gains in psychological weight.

**How it applies to titles:**
- "How I LOST $50,000" outperforms "How I Made $50,000" in CTR because loss framing activates stronger emotional arousal.
- "Don't Make This Mistake" activates avoidance motivation more powerfully than "Here's the Right Way."
- FOMO (Fear of Missing Out) is a direct application: 68% of millennials make decisions within 24 hours when experiencing FOMO (research cited by multiple marketing studies).

**Design implication:** The Generator agent should include a loss-framing variant in every title batch generated.

### 6.3 Social Proof (Cialdini, 1984)

**Core Claim:** People look to others' behavior and expert authority when uncertain. Social proof reduces perceived risk of a click.

**How it applies to titles:**
- Numbers imply research ("I Tested 47 Laptops")
- Authority signals ("What NASA Scientists Actually Eat")
- Scale signals ("10 Million People Got This Wrong")

**Design implication:** Title templates should include social proof injection points.

### 6.4 Emotional Arousal & Virality

Research on content virality (Berger & Milkman, 2012, Wharton) established that high-arousal emotions — both positive (awe, excitement) and negative (anger, anxiety) — drive sharing and clicking, while low-arousal emotions (sadness, contentment) suppress it.

Chen (2023) further found that sentiment **strength** in titles has a statistically significant impact on engagement metrics like likes and comments, and that **incongruence** between the title sentiment and other metadata signals can dampen performance even when individual elements are strong.

**Key finding:** Awe is the single highest-performing emotional trigger for viral spread. Anger is second. Contentment has near-zero viral effect.

**Design implication:** VADER sentiment scores should target high-arousal positive or high-arousal negative sentiment bands, not neutral or low-arousal scores.

---

## 7. YouTube Algorithm & CTR — Empirical Facts

### 7.1 How the Algorithm Uses CTR

The YouTube recommendation system evaluates CTR as a *signal*, not an absolute ranking factor. The algorithm:
1. Shows the video to a small test audience (cold-start cohort)
2. Measures CTR alongside **watch time** and **audience retention**
3. If CTR is strong AND watch time is sustained → expand distribution
4. High CTR + low watch time → algorithm penalizes (punishes misleading titles)

This is why the ethical layer (NLI faithfulness check) is not just a moral choice — it is an **algorithmic survival requirement**.

### 7.2 CTR Benchmarks

| Context | Good CTR | Average CTR |
|---|---|---|
| Browse / Home feed | 7–12% | 2–5% |
| Suggested videos | 7–12% | 4–6% |
| YouTube Search | 4–8% | 2–4% |
| Overall average | 4–6% | 2–3% |

Source: LenosTube industry data, Hootsuite 2025 analysis.

A video achieving >10% CTR on the home feed is a significant outlier and typically indicates a strong title + thumbnail combination.

### 7.3 The Compound Algorithm Effect

High CTR creates a self-reinforcing loop:
- High CTR → more impressions → more watch time data → higher ranking → more impressions
- This loop explains why optimizing the title has **disproportionate long-term impact** compared to any other single variable.

### 7.4 CTR Prediction Feasibility (ML Evidence)

Existing ML research demonstrates that CTR is predictable from title features alone:
- XGBoost regressor achieved **RMSE of 3.48%** on YouTube CTR from title + metadata features
- Random Forest achieved **70%+ accuracy** in classifying whether a video CTR would exceed 6%
- Adding full metadata (views, subscribers) pushed accuracy to **92.5%**

This validates the pCTR model component of this project.

---

## 8. Title Engineering — Empirical Rules

### 8.1 Optimal Title Length

| Metric | Optimal Range | Notes |
|---|---|---|
| Character count | 60–70 chars | Full display in YouTube search results |
| Character count (mobile) | 40–50 chars | Truncation begins at ~35 chars on mobile home feed |
| Word count | 7–12 words | Bell-curve peak (EAI study, 12,466 videos) |

**Academic evidence:** A peer-reviewed study (EAI, 2025) analyzing 12,466 Microsoft Excel YouTube tutorial videos found a **bell-shaped relationship** between title length/word count and view counts, with peaks at specific lengths, confirming both extremes underperform.

**Key display constraint:** YouTube truncates titles after ~60–70 characters in search results and as early as 35–50 characters on mobile browse. The most critical words must appear in the **first 30–50 characters**. Hard cap for mobile-first safety: <60 characters where possible (per platform best practice).

### 8.2 Numerical Triggers

- Titles containing numbers achieve **20–30% higher CTR** on average vs. non-numerical titles.
- Odd numbers outperform even numbers in headline research (general copywriting, widely replicated).
- Large numbers imply scale: "47 Tests", "1,000,000 Views" — social proof via quantity.

### 8.3 Front-Loading

- Front-loading the primary keyword in the first 30 characters improves **search rankings by up to 20%** (SEO research).
- The first 3–5 words function as the "hook" — they determine whether a viewer reads the rest.

### 8.4 The IMPACT Title Formula

Derived from synthesis of copywriting research and YouTube-specific studies:

| Component | What it is |
|---|---|
| **I** — Immediate Hook | First 3–5 words create the grab |
| **M** — Measurable Outcome | Numbers or specific results |
| **P** — Personal/Proof element | Credibility signal |
| **A** — Audience Clarification | Who the video is for |
| **C** — Curiosity or Controversy | The gap or the tension |
| **T** — Timeframe | When/urgency signal |

Not all components appear in every title — the formula is a *checklist*, not a template.

### 8.5 MrBeast Title Principles (Real-World Case Study)

MrBeast (world's most-subscribed YouTube channel) publicly shared his title philosophy. Key documented rules:

- Titles are **written before the video is produced** — if the title doesn't work, the concept is rethought.
- Titles stay **under 50 characters** where possible.
- Emotional intensity is maximized: "I Survive" instead of "I Spent" (more extreme = higher CTR).
- Superlatives and extremes dominate: avoid neutrality at all costs.
- A/B testing is systematic — every title is tested and CTR is measured.
- Titles must be **immediately comprehensible** — no ambiguity about the core premise.

---

## 9. Psychological Triggers Taxonomy

The following is the **operationalized trigger list** that the Generator agent must implement. Each trigger maps to specific linguistic patterns.

### T1 — Curiosity Gap
- **Theory base:** Loewenstein Information Gap Theory
- **Linguistic markers:** "Why I...", "What Happens When...", "The Real Reason...", "Nobody Talks About..."
- **Implementation:** Withhold the resolution. State the premise. Create a question the viewer can only answer by watching.
- **Example:** "I Tried Every $1 Restaurant in Tokyo" → gap: "what did he find?"

### T2 — Loss Aversion / FOMO
- **Theory base:** Kahneman & Tversky Prospect Theory
- **Linguistic markers:** "Don't Make This Mistake", "Before You Buy...", "You're Doing X Wrong", "Everyone Gets This Wrong"
- **Implementation:** Frame as avoidable loss. The click resolves the threat.
- **Example:** "Stop Wasting Money on This (I Did For 3 Years)"

### T3 — Social Proof / Authority
- **Theory base:** Cialdini Social Proof
- **Linguistic markers:** "Expert Says...", "10,000 People Tried This", "What Scientists Found...", numbered lists
- **Implementation:** Inject scale, expertise, or crowd behavior as signal.
- **Example:** "I Asked 50 Experts What They'd Do With $1000"

### T4 — Urgency / Scarcity
- **Theory base:** FOMO + Scarcity Marketing (Cialdini)
- **Linguistic markers:** "Before It's Too Late", "Last Chance", "This Changes Everything"
- **Implementation:** Time-bound or finite framing forces immediate action.
- **Warning:** Overuse leads to credibility erosion. Use sparingly.

### T5 — Extreme / Superlative
- **Theory base:** Emotional arousal research (Berger & Milkman)
- **Linguistic markers:** "The Worst", "Impossible", "Never Seen Before", "Most Expensive"
- **Implementation:** Push the framing to its extreme. Neutral statements do not click.
- **MrBeast validation:** "I Don't Like Bananas" → "Bananas Are The Worst Food On Earth"

### T6 — Personal Stakes / Vulnerability
- **Theory base:** Narrative transportation theory
- **Linguistic markers:** "I Lost...", "I Failed...", "My Biggest Mistake", "I Quit..."
- **Implementation:** First-person stakes create parasocial investment.
- **Example:** "I Quit My $200K Job to Do This"

### T7 — Number + Specificity
- **Theory base:** Cognitive ease; specificity implies credibility
- **Linguistic markers:** Exact numbers (not rounded), timeframes, percentages
- **Example:** "This $11 Meal Changed How I Cook Forever"

---

## 10. Existing Solutions & Their Limits

### 10.1 Manual Expert Copywriting

| Attribute | Assessment |
|---|---|
| Quality | High — experts understand psychological triggers |
| Scalability | Zero — cannot operate at creator volume |
| Accessibility | Low — requires expensive specialists |
| Speed | Slow |
| Consistency | Variable |

### 10.2 Generic LLM Prompts ("Write me a YouTube title")

| Attribute | Assessment |
|---|---|
| Quality | Low — produces descriptive, flat titles |
| Scalability | High |
| Psychological grounding | None — no trigger operationalization |
| CTR optimization | None |
| Hallucination risk | High — may generate titles unrelated to content |

Research on machine-generated titles (PLOS ONE, 2024) confirmed that standard LLM prompts lack the nuance to capture emotional appeal and cultural specificity that human experts apply.

### 10.3 YouTube Analytics Platforms (TubeBuddy, VidIQ, etc.)

| Attribute | Assessment |
|---|---|
| Data richness | High — show historical CTR, keyword data |
| Generative capability | None or minimal |
| Proactive | No — purely reactive, user-driven |
| Psychological optimization | None |

These tools show you *what happened* — they do not *generate what should happen next*.

### 10.4 Clickbait Detectors (ClickGuard, SemEval systems)

Built for detection and classification, not generation. They identify deceptive content but provide no optimization pathway.

---

## 11. System Architecture

### 11.1 Architectural Pattern: API Wrapper with Facade Pattern

The system follows the **API Facade Pattern**. This design pattern provides a simplified interface to a complex body of code (the LLM, its prompt strategies, and the validation pipeline). The client submits a simple request (video transcript/summary), and the Facade handles the complex orchestration internally:

- **Facade:** FastAPI endpoint — hides all internal complexity from the caller
- **Factory:** "Prompt Factory" module — constructs psychologically engineered prompts dynamically per request
- **Internal orchestration:** Multi-agent pipeline (Analyzer → Generator → Critic) managed by LangGraph

This pattern ensures the system is easy to consume externally (simple API) while being architecturally sophisticated internally (multi-agent, multi-model pipeline).

### 11.2 High-Level Flow

```
Video Content Input (transcript / description / summary)
          │
          ▼
  [Analyzer Agent]
  • Extract key themes, promises, emotional hooks
  • Identify what the video actually delivers (ground truth)
  • Score emotional arousal potential
          │
          ▼
  [Generator Agent]
  • Query Prompt Database via vector similarity → retrieve niche-specific few-shot examples
  • Apply Chain-of-Thought reasoning sequence
  • Produce N=5 candidate titles
  • Each title targets a different psychological trigger (T1–T7)
  • Apply IMPACT formula constraints
  • Apply length constraints (55–70 chars target, hard cap <100)
          │
          ▼
  [Critic Agent]
  • Score each title with pCTR model (predicted CTR)
  • Run VADER sentiment → ensure high-arousal score
  • Run BERTScore + NLI faithfulness check
  • Flag any title that contradicts video content
  • Rank surviving titles by composite score
          │
          ▼
  [Output]
  • Top-ranked title with virality score
  • Full ranked list with per-title analysis
  • Rejection log for deceptive candidates
```

### 11.3 Data Flow Detail

```
Input:
  - video_transcript: str
  - video_description: str (optional)
  - video_category: str
  - channel_stats: {subscribers, avg_views} (optional)

Analyzer Output:
  - core_promise: str          (what the video actually delivers)
  - key_entities: list[str]    (people, places, numbers, stakes)
  - emotional_potential: float (0–1, estimated arousal ceiling)
  - trigger_candidates: list[str]  (which triggers T1–T7 fit this content)

Generator Output:
  - candidates: list[TitleCandidate]
    Each TitleCandidate:
      - title: str
      - trigger_used: str
      - char_count: int
      - word_count: int

Critic Output:
  - scored_candidates: list[ScoredTitle]
    Each ScoredTitle:
      - title: str
      - pctr_score: float       (0–1, predicted CTR)
      - vader_compound: float   (-1 to +1, sentiment)
      - bert_similarity: float  (0–1, vs. video summary)
      - nli_label: str          ("entailment" | "neutral" | "contradiction")
      - composite_score: float
      - is_valid: bool          (False if nli_label == "contradiction")
  - top_title: str
  - rejection_log: list[str]
```

### 11.4 Composite Scoring Formula

```
composite_score = (
    w1 * pctr_score +
    w2 * abs(vader_compound) +       # arousal, not polarity direction
    w3 * bert_similarity
) * nli_validity_multiplier           # 0 if contradiction, 1 if entailment/neutral

Initial weights (to be tuned):
  w1 = 0.50  (virality is primary objective)
  w2 = 0.25  (emotional arousal)
  w3 = 0.25  (faithfulness)
```

---

## 12. Agent Design

### 12.1 Analyzer Agent

**Role:** Ground truth extractor. Reads the raw video content and builds the semantic envelope that all downstream generation must stay within.

**Responsibilities:**
- Extract the **core promise** of the video (what will the viewer learn/experience/see?)
- Identify **key entities** (proper nouns, numbers, stakes) that are real and usable in titles
- Estimate **emotional ceiling** — what is the strongest truthful emotional framing possible?
- Map content to applicable **psychological triggers** (T1–T7)
- Output a structured **video brief** consumed by the Generator

**Why separate from Generator:** Decoupling analysis from generation prevents hallucination. The Generator never reads the raw transcript — it only works from the Analyzer's structured brief. This hard constraint is the primary anti-hallucination mechanism.

### 12.2 Generator Agent

**Role:** Creative title factory. Produces diverse title candidates, each engineered around a different psychological trigger.

**Responsibilities:**
- Receive video brief from Analyzer
- Query Prompt Database for niche-relevant few-shot examples (see §13.1)
- Apply Chain-of-Thought reasoning sequence (see §13.2)
- Generate N=5 candidate titles (one per priority trigger)
- Apply IMPACT formula elements
- Respect length constraints (target 55–70 chars, hard cap at 100)
- Include numerical variants for all applicable titles
- Generate one loss-framing variant per batch (mandatory)
- Output structured candidates with trigger metadata

**Prompt engineering principle:** Each trigger maps to a specific system prompt instruction. The Generator does not receive a generic "write a title" instruction — it receives explicit operationalized rules per trigger type, using the techniques in §13.

### 12.3 Critic Agent

**Role:** Gatekeeper and ranker. Eliminates deceptive candidates and ranks the rest by composite virality-faithfulness score.

**Responsibilities:**
- Run pCTR regression model on each candidate (from Virality Score Model)
- Score VADER compound sentiment (arousal magnitude target: >0.5 absolute)
- Compute BERTScore between title and video summary (faithfulness proxy)
- Run NLI model: premise = title, hypothesis = core promise from Analyzer
  - "entailment" → title accurately represents content ✓
  - "neutral" → title does not contradict but doesn't entail ✓ (allowed)
  - "contradiction" → title contradicts content ✗ (rejected, logged)
- Compute composite score for valid candidates
- Return ranked list and top recommendation

---

## 13. Prompt Engineering Techniques

This section documents the formal prompt engineering techniques used to steer the LLM toward psychologically optimized outputs. These are **first-class technical contributions** of the system — not incidental implementation details. They are the primary mechanism for operationalizing psychological theory (§6) into algorithmic behavior.

### 13.1 Few-Shot Prompting

**What it is:** Providing the model with curated examples of the desired output format and quality within the prompt context, without updating model weights.

**Academic basis:** Brown, T. et al. (2020). "Language Models are Few-Shot Learners." *NeurIPS.*

**How it works in this system:**
1. The pre-processed "Prompt Database" stores high-performing YouTube titles, categorized by Hook Type (Curiosity Gap, Negative Surprise, Listicle, Question, Superlative)
2. At generation time, the system performs a **vector similarity search** to find 3–5 titles semantically closest to the user's input topic
3. Category-specific examples (Tech, Education, Entertainment) are retrieved — not generic cross-domain examples
4. These examples are injected into the Generator Agent's prompt:
   > *"Here are high-performing titles in this niche: [Example 1], [Example 2], [Example 3]. Learn from their structure and psychological trigger patterns."*

**Why this outperforms zero-shot:** Zero-shot prompts produce generic, flat titles. Few-shot examples anchor the model to the specific linguistic register and trigger structure that works for the content niche.

### 13.2 Chain-of-Thought (CoT) Reasoning

**What it is:** Instructing the LLM to reason step-by-step before producing the final output, rather than generating the answer directly.

**Academic basis:** Wei, J. et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *NeurIPS.*

**CoT sequence implemented in the Generator Agent:**
1. *"Analyze the video brief and identify the core Information Gap or Conflict that the viewer would want resolved."*
2. *"Determine the optimal emotional angle — what high-arousal emotion does this content authentically support?"*
3. *"Draft 10 potential titles targeting this angle, each using a different psychological trigger from the taxonomy."*
4. *"Refine the best 3 for brevity, mobile impact, and the 55–70 character constraint."*

**Why CoT:** Creative generation tasks benefit from explicit reasoning decomposition. Asking for the title directly produces a surface-level answer; asking for step-by-step analysis produces more considered, trigger-aligned output.

### 13.3 Persona Pattern

**What it is:** Assigning the LLM a specific expert role to align its output distribution with professional-level standards.

**Implementation:**
> *"You are a viral YouTube title copywriter with 10+ years of experience optimizing CTR for top creators. You have deep expertise in psychological triggers, curiosity gaps, and emotional arousal engineering. Your goal is to write titles that are compelling, honest, and click-worthy."*

**Why it works:** Role-assigned prompts shift the model's prior toward domain-specific vocabulary, tone, and heuristics — producing outputs that more closely resemble expert human practitioners than generic instruction-following.

### 13.4 Dynamic Prompt Database (Vector Retrieval)

The few-shot examples are not static — they are retrieved dynamically per request:

| Step | Detail |
|---|---|
| Indexing | High-performing titles embedded and stored in a vector store |
| Query | Input video brief is embedded at runtime |
| Retrieval | Nearest-neighbor search returns top-K most similar titles |
| Filtering | Category filter applied (e.g., only Education titles for educational videos) |
| Injection | Retrieved titles inserted as few-shot examples in the Generator prompt |

This ensures the few-shot context is always topically relevant — a cooking video gets cooking-niche examples, not generic examples from MrBeast's extreme challenge format.

---

## 14. Technology Stack — Justified

### 14.1 Backend: Python + FastAPI

**Why FastAPI:**
- ASGI-based (Asynchronous Server Gateway Interface) — native async/await support
- LLM calls are fundamentally I/O-bound; async handling allows a single process to serve thousands of concurrent requests efficiently
- Automatic request validation via Pydantic models — critical for structured agent I/O
- Native streaming response support (critical for LLM output streaming)
- Performance benchmarks comparable to Node.js and Go for I/O-bound workloads
- Production deployment: Gunicorn + Uvicorn workers for multi-process async

**Architecture pattern:**
- FastAPI handles routing and request lifecycle (Facade layer)
- LangChain agents run as async background tasks
- ML model inference (pCTR) runs in a separate ProcessPoolExecutor (CPU-bound)
- Heavy LLM inference optionally offloaded to vLLM or Triton Inference Server

### 14.2 Agent Orchestration: LangChain + LangGraph

**Why LangChain:**
- Provides the infrastructure layer for building, connecting, and managing agents
- Native support for the Supervisor pattern (Analyzer → Generator → Critic)
- Memory management across agent turns
- Tool binding for calling external services (YouTube API, NLI models)
- Well-documented multi-agent coordination with LangGraph for stateful, graph-based agent flow

**Agent coordination pattern:** Supervisor pattern
- A controller receives the input and sequentially delegates to Analyzer, then Generator, then Critic
- LangGraph manages the state transitions between agents
- Each agent has an **isolated context window** — the Generator does not see the raw transcript, only the Analyzer's structured output. This is an architectural deception-prevention mechanism.

### 14.3 LLM Layer: GPT-4o (primary) / Llama 3 (fallback/open-source)

**Why GPT-4o:**
- State-of-the-art instruction following for structured JSON output
- Strong performance on creative generation tasks with constraint satisfaction
- Fine-tuning available ($25/million tokens training, $3.75/$15 per million I/O tokens inference)
- Native function calling / structured output mode for agent pipelines

**Why Llama 3 as alternative:**
- Open-source — deployable on local hardware with no per-token cost
- Viable for fine-tuning on domain-specific YouTube title data
- Avoids vendor lock-in for production deployment

**Note on fine-tuning:** Both models support fine-tuning. A fine-tuned version on a curated dataset of high-CTR YouTube titles (sourced from the dataset pipeline) is a planned Phase 2 enhancement.

### 14.4 Sentiment Analysis: VADER

**Why VADER:**
- Specifically designed for **short, informal social media text** — exactly the domain of YouTube titles
- Combines a hand-curated lexicon with heuristic rules capturing:
  - Capitalization effects ("GREAT" vs "great")
  - Punctuation effects ("great!!!" > "great")
  - Negation handling
  - Degree modifiers ("very", "extremely")
- Returns both **polarity** (positive/negative) and **intensity** (compound score -1 to +1)
- Pre-trained, no GPU required, extremely fast inference
- Validated on social media corpora

**What VADER measures in this system:**
- The Critic agent uses the **absolute compound score** as an emotional arousal proxy
- High-arousal target: |compound| > 0.5
- Neutral titles (compound ≈ 0) are penalized because low arousal correlates with low CTR in viral content research

**VADER limitation acknowledged:** VADER does not model *type* of emotional arousal — it measures intensity. The system uses it as a necessary proxy, not a perfect arousal classifier. Future work: replace with a fine-tuned arousal classifier.

### 14.5 Semantic Faithfulness: BERTScore + NLI

**Why this two-layer approach:**

| Layer | Tool | What it measures | Limitation |
|---|---|---|---|
| Layer 1 | BERTScore | Token-level semantic similarity between title and video summary | Measures similarity, not truthfulness |
| Layer 2 | NLI model | Logical relationship: does title *contradict* the video content? | Definitive deception detection |

**BERTScore:**
- Computes cosine similarity between BERT embeddings of title tokens and summary tokens
- Scores range 0–1 (1 = semantically identical)
- Used as a **relevance filter** — very low BERTScore (< 0.3) indicates the title is off-topic
- *Cannot* detect factual contradiction — only semantic distance
- Implemented via `bert-score` Python library

**NLI (Natural Language Inference):**
- Models: `roberta-large-mnli` or `facebook/bart-large-mnli` (available on HuggingFace)
- Task: given [Title] as premise and [Video Core Promise] as hypothesis, classify as:
  - **Entailment:** Title logically implies the video content ✓
  - **Neutral:** Title is consistent but doesn't entail the content ✓ (acceptable)
  - **Contradiction:** Title logically contradicts the video content ✗ (rejected)
- Research shows NLI-based faithfulness correlates more strongly with human judgments than BERTScore alone (ACL 2025 findings)
- This is the **hard rejection gate** in the system

**Why BERTScore is kept despite limitations:** It catches off-topic titles (low similarity) before they reach the NLI model, reducing unnecessary NLI inference calls. The two models serve complementary roles.

---

## 15. Dataset Strategy

### 15.1 Primary Sources

**Source 1: Kaggle YouTube Trending Dataset**
- URL: `https://www.kaggle.com/datasets/rsrishav/youtube-trending-video-dataset`
- Updated daily; US trending videos
- Fields: video_id, title, channel_title, category_id, trending_date, tags, views, likes, dislikes, comment_count, description
- **Limitation:** Trending ≠ high CTR. Trending videos have accumulated views, but early CTR is not captured. Use as proxy for viral linguistic patterns.

**Source 2: Kaggle Trending YouTube Video Statistics (Classic)**
- URL: `https://www.kaggle.com/datasets/datasnaek/youtube-new`
- Historical US/CA/GB/IN data, 29,089 unique videos
- Widely used in academic ML research on YouTube virality

**Source 3: YouTube Data API v3 (Targeted Scraping)**
- Scrape top-performing videos from high-CTR channels (MrBeast, Veritasium, Mark Rober, Kurzgesagt)
- Collect: title, description, view_count, like_count, subscriber_count_at_upload
- Purpose: extract linguistic patterns from demonstrably high-performing titles

**Source 4: Custom Annotation**
- Manual labeling of title quality with psychological trigger type (T1–T7)
- Required for the pCTR model's trigger-type feature
- Target: 500–1,000 labeled examples minimum

**Source 5: Webis Clickbait Corpus (Negative Examples)**
- Academic dataset of annotated clickbait titles used in clickbait detection research
- Purpose: train the validation layer's rejection module on *what not to do* — linguistic patterns associated with deceptive or misleading metadata
- Provides ground-truth negative examples to complement the positive examples from Sources 1–3
- Also referenced in SemEval clickbait detection shared tasks

### 15.2 Feature Engineering for ML

From raw title text, extract:

| Feature | How | Why |
|---|---|---|
| title_length_chars | `len(title)` | Bell-curve optimal length |
| title_word_count | `len(title.split())` | Bell-curve optimal word count |
| has_number | regex `\d+` | +20–30% CTR signal |
| number_value | extract & parse | Large numbers = social proof |
| vader_compound | VADER | Emotional arousal |
| vader_positive | VADER | Positive valence |
| trigger_type | classification | Which T1–T7 |
| first_word_type | POS tag | Verb starts outperform nouns |
| has_question | `?` in title | Curiosity gap signal |
| has_exclamation | `!` in title | Arousal signal |
| all_caps_ratio | word-level | Intensity signal |
| has_emoji | boolean | Virality signal per Chen (2023) |
| category_id | from metadata | Category baseline CTR varies |
| channel_subscriber_tier | binned | Larger channels have higher baseline CTR |

### 15.3 Target Variable for pCTR Model

**Primary target: Virality Score (subscriber-normalized)**

Since raw CTR is not publicly available from YouTube, the target variable is a normalized proxy:

```
Virality_Score = Views / Subscriber_Count
```

(Or view velocity if time-series data is available.) This normalization is critical — a generic title on a large channel gets views purely from subscriber pull, not title quality. Normalizing by subscriber count isolates the title's contribution to discovery.

**Binary classification alternative:** CTR bucket
- Class 0: below-average performance (Virality_Score < threshold)
- Class 1: above-average performance (Virality_Score ≥ threshold)

**Caveat:** Both proxy methods are acknowledged limitations. Real CTR data requires YouTube Studio API access with creator consent. This is documented in §20 Limitations.

### 15.4 Data Cleaning Requirements

- Remove deleted/unavailable videos
- Remove videos with < 1,000 views (insufficient signal)
- Normalize subscriber counts to upload date (not current)
- Remove non-English titles (scope limitation)
- Remove titles that are purely SEO keyword strings (no natural language)
- **De-duplicate trending entries:** Trending datasets list the same video once per trending day — collapse to a single entry with peak metrics
- **Emoji handling:** Preserve and properly tokenize emojis; research (Chen, 2023) indicates emojis are significant carriers of sentiment and virality signals
- **Toxicity filtering:** Apply a toxicity classifier (e.g., `unitary/toxic-bert`) to sanitize few-shot training examples drawn from trending data, which may contain hate-watching or sensationalist content. This prevents the LLM from learning manipulative or harmful patterns as optimization targets.

---

## 16. Machine Learning — Virality Score Model

### 16.1 Model Choice: Random Forest + XGBoost

**Why tree-based ensemble methods (not deep learning):**
- Dataset size (tens of thousands) does not justify deep learning
- Features are tabular (engineered numerics + encoded text features), not raw sequences
- Tree methods are interpretable — can explain which features drive high CTR (research requirement)
- XGBoost is industry-validated: F1 = 0.741 on YouTube virality tasks (prior research)
- Random Forest achieved 80.1% accuracy using title + limited metadata in clickbait research, scaling to 92.5% with full metadata

### 16.2 Model Training Plan

```
Data split:
  - 70% training
  - 15% validation
  - 15% test (held out until final evaluation)

Model 1: Random Forest
  - n_estimators: 100–500 (tune)
  - max_depth: 10–30 (tune)
  - Feature importance analysis

Model 2: XGBoost
  - learning_rate: 0.01–0.1
  - n_estimators: 100–500
  - max_depth: 3–8
  - Regularization: L1 + L2

Hyperparameter tuning: RandomizedSearchCV or Optuna
```

### 16.3 Evaluation Metrics

- **Primary:** F1-score (accounts for class imbalance)
- **Secondary:** ROC-AUC, Precision, Recall
- **Regression variant:** RMSE

### 16.4 Feature Importance

Prior research found "Comments Per View" was disproportionately informative in tree models. For this system, the equivalent high-signal features are expected to be:
- VADER compound (emotional arousal)
- Presence of number
- Title length (bell curve sweet spot)
- Trigger type

The trained model serves as the **pCTR scorer** inside the Critic agent.

---

## 17. Semantic Faithfulness & Anti-Deception Layer

### 17.1 The Deception Problem in AI Title Generation

Standard LLM prompting for titles has two failure modes:
1. **Bland generation:** Title is accurate but boring ("How to Make Pasta")
2. **Hallucinated generation:** Title is clickable but factually wrong or misleading ("I Made $1M from Pasta" when the video is a basic recipe tutorial)

Mode 2 is the more dangerous failure — it produces titles that get initial clicks but devastate watch time, which destroys algorithmic standing. It also erodes creator trust and violates platform content policies.

### 17.2 The Two-Layer Defense

**Layer 1 (Architectural):** The Generator never reads the raw video — it reads only the Analyzer's structured brief. The Analyzer has already extracted the ground truth. This limits the space of hallucinations by design.

**Layer 2 (Computational):** The Critic runs NLI to detect if any generated title contradicts the core promise established by the Analyzer. Contradictions are hard-rejected and logged.

### 17.3 NLI Implementation Detail

```python
# Model recommendation
model_name = "facebook/bart-large-mnli"
# Alternative: "roberta-large-mnli"

# Input construction
premise = generated_title          # e.g., "I Made $1M Selling Pasta"
hypothesis = core_promise          # e.g., "This is a basic pasta recipe tutorial"

# Expected output
# "contradiction" → reject this title
# "neutral"       → allow (title is not deceptive, just not perfectly aligned)
# "entailment"    → ideal (title accurately represents content)
```

### 17.4 BERTScore Threshold

- BERTScore < 0.30 (vs. video summary): flag for manual review (potentially off-topic)
- BERTScore 0.30–0.60: normal range for creative titles (acceptable)
- BERTScore > 0.60: title is semantically very close to summary (risk of being boring/descriptive)

---

## 18. Generative Ethics Framework

### 18.1 Definition

**Generative Ethics** (as defined by this project): A framework for AI content generation that optimizes for engagement while enforcing factual faithfulness constraints. The system should be able to answer "yes" to both:

1. Would a viewer who clicked this title feel satisfied (not deceived) after watching?
2. Does this title perform better than a non-optimized descriptive title on the click-through metric?

### 18.2 The Click-Truth Spectrum

```
PURELY DECEPTIVE ←──────────────────────────────→ PURELY DESCRIPTIVE
"I Made $1M"          "Curiosity-Optimized,        "Basic Pasta Recipe"
(video: pasta recipe)  Factually Faithful"          (boring, low CTR)
                       TARGET ZONE ↑
```

The system must operate in the right-center of this spectrum — psychologically compelling but factually grounded.

### 18.3 Ethical Constraints Encoded in System

| Constraint | Implementation |
|---|---|
| No factual contradiction | NLI hard rejection |
| No fabricated numbers | Analyzer extracts real numbers only; Generator uses them |
| No false promise of outcome | Core promise validation before generation |
| No manipulative exaggeration | Extreme framing must be grounded in real extremes from the video |
| No toxic optimization | Toxicity filter on training examples (§15.4) |
| Title must match content delivered | Watch time signal (external feedback loop) |

### 18.4 Platform Policy Alignment

YouTube's Terms of Service (Section 4H) prohibit misleading metadata. Thumbnails and titles that "set up expectations the video doesn't deliver" violate policy and can lead to:
- Video demonetization
- Channel strikes
- Reduced algorithmic distribution

The NLI faithfulness layer is therefore both an ethical and a **legal/platform compliance** mechanism.

---

## 19. Evaluation Metrics

### 19.1 System-Level Evaluation

| Metric | Definition | Target |
|---|---|---|
| **Title Acceptance Rate** | % of generated titles passing NLI check | > 60% |
| **pCTR Score (avg)** | Average predicted CTR of top-ranked titles | > 6% |
| **VADER Arousal (avg)** | Average \|compound\| of generated titles | > 0.4 |
| **BERTScore (avg)** | Average title-to-summary semantic similarity | 0.35–0.60 |
| **Self-BLEU (diversity)** | Overlap between generated titles in a batch; lower = more diverse | < 0.4 |
| **Latency (P95)** | End-to-end pipeline time | < 10 seconds |

**Self-BLEU:** Computes BLEU score between each generated title and the rest of the batch. A low Self-BLEU score confirms the system produces diverse title variants (different triggers, structures) rather than minor paraphrases of a single pattern. High Self-BLEU indicates the API is over-fitting to a single trigger type.

### 19.2 Offline Evaluation (ML Model)

| Metric | Target |
|---|---|
| F1-score (pCTR classifier) | > 0.75 |
| ROC-AUC | > 0.80 |
| RMSE (if regression mode) | < 3.5% |

### 19.3 Human Evaluation (User Study)

A human evaluation study comparing:
- **Baseline A:** Descriptive title (ground truth from video)
- **Baseline B:** Generic LLM prompt output (zero-shot, no trigger engineering)
- **System output:** YTO top-ranked title

Evaluators rate on a standardized 4-dimension rubric (1–5 scale):
1. **Curiosity** — Does this title create an information gap? How curious does it make you?
2. **Emotional Impact** — How strong is the emotional response (arousal)?
3. **Clarity** — Is the core topic immediately understandable?
4. **Trustworthiness** — Does this title feel honest (not deceptive)?

Target: YTO significantly outperforms both baselines on Curiosity and Emotional Impact while maintaining comparable Clarity and Trustworthiness scores.

**Deviation (logged 2026-08-13, `PLAN_IMPLEMENTATION.md` §6.3):** the design above (10 videos, n=50+ participants → 120 rating questions per respondent) was descoped during Sprint 6 to a **3-video, n=15–20 pilot study** (3 videos × 3 titles × 4 dimensions = 36 rating questions, ~8–10 minutes), after a first-pass 5-video cut (60 questions) was also judged too long for realistic completion. The 3 retained videos (`video_id` 1, 3, 6 — Science & Technology, People & Blogs, Education) were chosen for category diversity from the same 20-video evaluation set used in §19.1, and kept their original IDs so responses join cleanly against `human_eval_answer_key.csv`. Baseline A ("ground truth from video") is instantiated as `video_description` rather than a real published title, since the evaluation set consists of synthetic transcripts with no real underlying YouTube upload. All tooling (stimulus generation, blinding, survey instrument, analysis script) was built and is ready; the target design above is retained here as the original research intent, while Chapter 6 (§6.6) reports actual results against this reduced pilot scope, not the full n=50+/10-video design.

**Actual results (2026-09-10):** the pilot survey was distributed and collected **n=29 real respondents** (exceeding the n=15–20 target), reshaped from the Google Forms wide export into the long format `human_eval_analysis.py` expects (`system/evaluation/reshape_human_eval_responses.py`), and analyzed. Mean scores (1–5 scale): System led on curiosity (3.52) and emotional impact (3.59) over both baselines; Baseline A led clarity (3.71 vs. System 3.55); trustworthiness tied between System and Baseline A (3.51). None of the System-vs-baseline Wilcoxon comparisons reached significance at α=0.05 (all p > 0.1) — unsurprising at n=29 paired ratings, and reported as a limited-evidence pilot result rather than a confirmed effect. The §19.4 inter-rater reliability check (Pearson r between human and LLM-judge curiosity scores) came back weak and non-significant (r = −0.14, p = 0.72, n=9 video/condition pairs), which Chapter 6 discusses honestly as a limitation rather than treating the LLM judge as validated ground truth. Full figures: `system/evaluation/outputs/human_eval_results.json`.

### 19.4 LLM-as-a-Judge Evaluation

A secondary automated evaluation method where a capable LLM (e.g., GPT-4o) is used as an evaluator to score generated titles against a structured marketing rubric. This addresses RQ4 directly.

**How it works:**
```
Prompt to Judge LLM:
"You are an expert YouTube growth strategist. 
Given the video summary below, evaluate this title on three dimensions (1–5):
- Curiosity (Information Gap created)
- Urgency (time/loss pressure felt)
- Relevance (how well it matches the content)

Video Summary: [summary]
Title: [generated_title]

Return JSON: {curiosity: X, urgency: X, relevance: X, overall: X, reasoning: "..."}"
```

**Why LLM-as-a-Judge:**
- Scales to hundreds of titles without human annotator cost
- Provides interpretable, rubric-grounded scores
- Cross-validated against human evaluation scores to assess reliability
- Complements quantitative metrics (pCTR, VADER) with qualitative marketing expertise simulation

**Limitation:** LLM judges can be biased toward verbose or confident-sounding outputs. Cross-validation with human evaluation is mandatory.

---

## 20. Limitations & Future Work

### 20.1 Known Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| CTR not directly available in public datasets | pCTR model trained on proxy signals (Views/Subscriber_Count) | Collect actual CTR data via YouTube Studio API with creator consent |
| VADER does not model arousal type | May rank high-anger titles equally with high-awe titles | Replace with fine-tuned arousal classifier |
| English-only scope | Cannot serve non-English creators | Language-specific model variants in Phase 2 |
| Thumbnail not included | Title-only optimization ignores title+thumbnail interaction | Add thumbnail analysis module (computer vision) |
| No personalization | Same title for all audiences | Add audience demographic modeling |
| Channel authority not modeled | A title that works for MrBeast may not work for a 1,000-subscriber channel | Add subscriber_tier as context variable |
| Model volatility | Underlying LLM updates may affect reproducibility | Pin model versions; document API version at evaluation time |
| Cultural context | Viral titles rely on cultural context/memes that LLMs may miss without fine-tuning | Niche-specific fine-tuning in Phase 2 |

### 20.2 Future Work

1. **Thumbnail integration:** Multimodal analysis (title + thumbnail) for joint CTR optimization
2. **Description optimization:** Extend the pipeline to generate SEO-optimized descriptions
3. **Fine-tuned LLM:** Train a domain-specific model on high-CTR YouTube titles
4. **Real-time A/B integration:** API hook into YouTube Studio for live CTR feedback loop
5. **Multi-language support:** Localized psychological trigger databases per language/culture
6. **Creator style matching:** Learn channel-specific voice and maintain stylistic consistency
7. **Audience modeling:** Incorporate viewer demographic and interest profile
8. **Arousal classifier:** Replace VADER with a fine-tuned high-arousal/low-arousal classifier

---

## 21. Key References

### Foundational Theory

- Loewenstein, G. (1994). "The psychology of curiosity: A review and reinterpretation." *Psychological Bulletin*, 116(1), 75–98. — **Information Gap Theory**
- Golman, R. & Loewenstein, G. (2018). "Information Gaps: A Theory of Preferences Regarding the Presence and Absence of Information." *Decision*, 5(3), 143–164. — **Information Gap — salience refinement**
- Kahneman, D. & Tversky, A. (1979). "Prospect Theory: An Analysis of Decision under Risk." *Econometrica*, 47(2). — **Loss Aversion**
- Cialdini, R. B. (1984). *Influence: The Psychology of Persuasion.* Harper Collins. — **Social Proof, Scarcity, Authority**
- Berger, J. & Milkman, K. (2012). "What Makes Online Content Viral?" *Journal of Marketing Research*, 49(2). — **Emotional Arousal & Virality**
- Chen, H. (2023). "Title Matters: Impacts of Titles on User Engagement in Short Video Platforms." Singapore Management University (PhD Dissertation). — **Title characteristics, sentiment, emoji signals**
- Cui, G., Chung, S.Y.-H., Peng, L., & Wang, Q. (2024). "Clicks for Money: Predicting Video Views Through a Sentiment Analysis of Titles and Thumbnails." *Journal of Business Research*, 183, 114849. — **Sentiment + thumbnail CTR prediction**

### Research Methodology

- Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). "A Design Science Research Methodology for Information Systems Research." *Journal of Management Information Systems*, 24(3), 45–77. — **DSR / DSRM framework**

### Prompt Engineering

- Brown, T., Mann, B., Ryder, N., et al. (2020). "Language Models are Few-Shot Learners." *Advances in Neural Information Processing Systems (NeurIPS).* — **Few-Shot Prompting**
- Wei, J., Wang, X., Schuurmans, D., et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *Advances in Neural Information Processing Systems (NeurIPS).* — **Chain-of-Thought (CoT)**

### Clickbait & Curiosity Research

- Rony, M.M.U. et al. (2017). "Diving Deep into Clickbaits: Who, What, and Why?" — Systematic literature review
- "You Won't Believe What's in this Paper: Clickbait, Relevance and the Curiosity Gap." *Journal of Pragmatics*, 2021. ScienceDirect.
- "When curiosity gaps backfire: effects of headline concreteness on information selection." *Scientific Reports / Nature*, 2024.
- "Did clickbait crack the code on virality?" *PMC*, 2022. [PMC8799425]
- Mihelich, J. (2020). "Curiosity, Clickbait and Their Impacts on Political Media Selection." Wake Forest University.
- "Beyond algorithms: The human touch in machine-generated titles." *PLOS ONE*, 2024. [DOI: 10.1371/journal.pone.0306639]

### YouTube Algorithm & CTR

- Covington, P., Adams, J., & Sargin, E. (2016). "Deep Neural Networks for YouTube Recommendations." *ACM RecSys.* — Foundational YouTube ranking paper
- "Effect of Title Length and Word Count on Views." *EAI Endorsed Transactions on Scalable Information Systems*, 2025. [ResearchGate: 387126034]
- Hootsuite. "How the YouTube Algorithm Works." (2025 edition.)

### Machine Learning & CTR Prediction

- "YouTube Videos Prediction: Will this video be popular?" *Stanford CS229 Project*, 2019.
- Paskalev, G. "Can You Predict a YouTube Video's CTR using Machine Learning?" Medium.
- "Clickbait Detection in YouTube Videos." *arXiv*, 2021. [arXiv:2107.12791]
- Kaggle. "Trending YouTube Video Dataset." `rsrishav/youtube-trending-video-dataset`
- Kaggle. "YouTube Trending Video Statistics." `datasnaek/youtube-new`

### NLP — Sentiment, Faithfulness, Hallucination

- Hutto, C.J. & Gilbert, E. (2014). "VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text." *ICWSM.* — **VADER original paper**
- Zhang, T. et al. (2020). "BERTScore: Evaluating Text Generation with BERT." *ICLR.* — **BERTScore original paper**
- "A hallucination detection and mitigation framework for faithful text summarization using LLMs." *Scientific Reports*, 2025. [Nature]
- "Re-evaluating Hallucination Detection in LLMs." *ACL EMNLP*, 2025.
- "A Comprehensive Survey of Hallucination in Large Language Models." *arXiv*, 2025. [arXiv:2510.06265]
- "Clickbait Detection via Large Language Models." *arXiv*, 2023. [arXiv:2306.09597]
- "An Interpretable Benchmark for Clickbait Detection." *arXiv*, 2025. [arXiv:2509.10937]

### Generative AI Ethics

- "Negotiating the ethical frontier: the double-edged role of generative AI in scientific research." *NCBI*, 2025.
- California AB-2655 — Defending Democracy from Deepfake Deception Act (2024)

### Technology

- FastAPI documentation. "Asynchronous Backend Architecture." Tiangolo.
- LangChain documentation. "Multi-Agent Systems." LangChain Inc.
- OpenAI. "GPT-4o Fine-Tuning." OpenAI Blog, 2024.
- "Architecting Scalable FastAPI Systems for LLM Applications." Medium, 2024.

---

*Last updated: June 2026 | Maintained by: P.A.D.B. Pathiraja (29071)*
*This document is the single source of truth for all project decisions. Any contradiction between this document and code/writing should be resolved in favor of this document unless a versioned update is made here first.*
