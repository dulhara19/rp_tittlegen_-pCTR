# THESIS WRITING PLAN
### AI-Powered YouTube Title Optimizer — P.A.D.B. Pathiraja (29071)
### Template Authority: Dulanjali Wijesekara Chapter Breakdown v1.1
### SOT Authority: SOURCE_OF_TRUTH.md

> Every section below maps to a numbered section in the lecturer's template. Do not skip or rename sections. All content must be grounded in SOURCE_OF_TRUTH.md.

---

## PROGRESS TRACKER

| Chapter | Status | Completed | File |
|---|---|---|---|
| Ch 1 — Introduction | ✅ DONE | 28 Jun 2026 | `thesis/chapters/ch01_introduction/ch01_introduction.md` |
| Ch 2 — Literature Review | ✅ DONE | 28 Jun 2026 | `thesis/chapters/ch02_literature_review/ch02_literature_review.md` |
| Ch 3 — Methodology | ✅ DONE | 28 Jun 2026 | `thesis/chapters/ch03_methodology/ch03_methodology.md` |
| Ch 4 — System Design | ✅ DONE | 13 Aug 2026 | `thesis/chapters/ch04_system_design/ch04_system_design.md` |
| Ch 5 — Implementation | ✅ DONE | 14 Aug 2026 | `thesis/chapters/ch05_implementation/ch05_implementation.md` |
| Ch 6 — Evaluation | ✅ DONE | 10 Sep 2026 | `thesis/chapters/ch06_evaluation/ch06_evaluation.md` |
| Ch 7 — Conclusion | ✅ DONE | 10 Sep 2026 (revised) | `thesis/chapters/ch07_conclusion/ch07_conclusion.md` |

**Interim Submission 01** ✅ SUBMITTED — 28 June 2026
**Next milestone:** None outstanding for the thesis text itself — all 7 chapters are complete and grounded in real data, including the human evaluation survey (n=29, collected 2026-09-04, analyzed 2026-09-10). Remaining work is at the recommendation level only: Ch7 §7.6 recommends scaling the human survey toward its original n=50+ target for statistical power, not required for chapter completeness. Full document assembly/export (`thesis/build_progress_submission.py`, `.docx` outputs) should be re-run to pick up the Ch6/Ch7 edits before final submission.

---

## INTERIM SUBMISSION 01 — ✅ SUBMITTED: 28 June 2026

Covers: Chapter 1, Chapter 2, Chapter 3
DOCX: `thesis/Pathiraja_29071_Interim_Submission_01.docx` (393 KB — includes embedded Figure 1.1 PNG)
Diagram assets: `thesis/assets/rich_picture.png` (matplotlib, 180 DPI) | `thesis/assets/rich_picture.drawio` (editable source)

---

## CHAPTER 1 — Introduction ✅ DONE

### 1.1 Chapter Overview
- 1–2 paragraphs
- Briefly introduce the chapter's purpose and structure
- Mention the video-first digital landscape and the metadata optimization problem
- End by signposting what each section covers

### 1.2 Problem Background *(What has actually happened?)*
- The shift from text-based to video-first internet (YouTube, TikTok, Instagram Reels)
- 500 hours of video uploaded to YouTube every minute → discovery problem, not quality
- CTR as the algorithmic gatekeeper: the click is the fundamental unit of currency
- The cold-start loop: test cohort → CTR signal → expand or suppress distribution
- Manual copywriting expertise is unscalable and inaccessible to most creators
- Rise of LLMs (GPT-4, Llama, Claude) and their generic application gap
- Reference: Covington et al. (2016) YouTube Recommendations paper

### 1.3 Problem Statement
*(Must be focused and supported with recent citations, justified with latest statistics)*

#### 1.3.1 General Problem
- At a macro level: algorithmically-driven discovery punishes poor metadata regardless of content quality
- High-quality educational/creative content fails to reach audiences not because it's bad, but because its packaging is weak
- The economic implication: creator ROI, business reach, and learning outcomes all hinge on a title
- Cite: 500 hours/minute (YouTube), cold-start effect (Covington et al., 2016)

#### 1.3.2 Specific Problem *(Domain-specific shortcomings; end by highlighting the research gap)*
- Current LLM integrations are reactive and produce flat, descriptive, un-optimized titles
- Existing analytics tools (TubeBuddy, VidIQ) show historical data but cannot generate optimized titles
- Psychological theories (Information Gap, Prospect Theory) are documented but not operationalized into generative AI systems
- No existing tool sits in the middle ground: optimizing virality while ensuring factual faithfulness
- Research gap: absence of a proactive, psychologically-grounded, ethics-constrained AI title generation system
- Cite: PLOS ONE (2024), Nature (2024) on clickbait decline

### 1.4 Research Question *(Wh-form, one primary)*
> **How can a multi-agent AI system be designed and evaluated to automatically generate YouTube video titles that are psychologically optimized for high Click-Through Rates while maintaining semantic faithfulness to the source video content?**

Sub-questions (optional):
- RQ1: How can viral linguistic patterns be operationalized into Few-Shot and Chain-of-Thought prompt templates?
- RQ2: What architecture best integrates LLM generation with a validation layer for hallucination-free output?
- RQ3: To what extent do engineered AI titles outperform zero-shot and human-generated baselines?
- RQ4: How can LLM-as-a-Judge patterns automate title quality scoring?

### 1.5 Research Motivation
Three dimensions:
1. **Economic/Social:** Democratizing access to viral marketing strategies; leveling the playing field for small creators and educators; creator economy dependency on metadata
2. **Technical:** Moving from reactive ("write me a title") to proactive AI systems; building API wrappers that abstract prompt complexity from the user; investigating whether LLMs can be steered to optimize a specific measurable metric (pCTR)
3. **Ethical:** Addressing the proliferation of deceptive clickbait; providing a "white-hat" alternative that is engaging but honest; answering whether virality and truthfulness can coexist in AI-generated content

### 1.6 Research Aim
> To design, develop, and evaluate a multi-agent AI system implemented as an API Wrapper that automatically generates psychologically optimized YouTube video titles, demonstrating that generative AI can be systematically constrained to maximize predicted engagement while preserving semantic faithfulness to the source video content.

### 1.7 Research Objectives
*(Must be research-specific, not generic learning objectives)*

#### 1.7.1 To Identify
Viral linguistic features (sentiment polarity, arousal level, information gap structures, numerical triggers, and psychological trigger types T1–T7) that correlate with high view velocity in YouTube trending video datasets.

#### 1.7.2 To Analyze
The effectiveness of advanced prompt engineering techniques — specifically Few-Shot Prompting, Chain-of-Thought reasoning, and the Persona Pattern — in operationalizing psychological theories (Information Gap Theory, Prospect Theory, Social Proof) within a Large Language Model generation pipeline.

#### 1.7.3 To Design and Develop
A multi-agent AI system comprising an Analyzer Agent, Generator Agent, and Critic Agent, encapsulated as a RESTful API Wrapper using the Facade design pattern, with an integrated Predicted CTR (pCTR) machine learning model and NLP validation layer (VADER, BERTScore, NLI).

#### 1.7.4 To Evaluate
The performance of the system using quantitative metrics (pCTR score, BERTScore, VADER arousal magnitude, Self-BLEU diversity, NLI acceptance rate) and qualitative human evaluation (preference survey, LLM-as-a-Judge rubric scoring) against human-generated and zero-shot AI baselines.

### 1.8 Rich Picture of the Proposed Solution
✅ Diagram created and embedded — 28 June 2026
- PNG: `thesis/assets/rich_picture.png` (matplotlib, 180 DPI) — embedded in ch01 and in DOCX
- Editable source: `thesis/assets/rich_picture.drawio` (open in draw.io Desktop or drawio.com)
- Diagram shows: INPUT → Analyzer → Generator (← Prompt DB) → Critic (pCTR / VADER / BERTScore / NLI gate) → OUTPUT, wrapped in API Wrapper / Facade container

### 1.9 Resource Requirements

#### 1.9.1 Hardware
| Resource | Specification | Purpose |
|---|---|---|
| Development Machine | Minimum 16GB RAM, 8-core CPU | LLM inference, ML model training |
| GPU (optional) | NVIDIA GPU with 8GB+ VRAM | Faster NLI/BERTScore inference |
| Storage | 50GB+ SSD | Dataset storage, model weights |
| Internet | Stable broadband | OpenAI API, HuggingFace model downloads |

#### 1.9.2 Software
| Software | Version/Type | Purpose |
|---|---|---|
| Python | 3.10+ | Core implementation language |
| FastAPI + Uvicorn | Latest stable | REST API backend |
| LangChain + LangGraph | Latest stable | Agent orchestration |
| OpenAI API (GPT-4o) | API access | LLM generation |
| HuggingFace Transformers | Latest stable | NLI models (BART-MNLI), BERTScore |
| NLTK / VADER | Latest stable | Sentiment analysis |
| Scikit-learn / XGBoost | Latest stable | pCTR ML model |
| Kaggle Datasets | Public | Training data |
| GitHub | Free tier | Version control |

### 1.10 Project Scope

| In Scope | Out of Scope |
|---|---|
| YouTube video title generation | Thumbnail generation or optimization |
| English-language titles only | Non-English or multilingual titles |
| Text-based input (transcript/description/summary) | Direct video file processing (audio/visual) |
| Predicted CTR as the optimization metric | Live CTR measurement from real channels |
| Multi-agent pipeline with NLI faithfulness check | Real-time YouTube Studio API integration |
| pCTR model trained on public Kaggle datasets | Proprietary CTR data collection |
| FastAPI REST backend | Frontend user interface / web app |
| Research prototype for academic evaluation | Production-ready commercial deployment |
| Comparison against zero-shot and human baselines | Large-scale A/B testing on live channels |

**In-scope elaboration:** The system accepts a video transcript or summary as input and returns a ranked list of 5 psychologically optimized title candidates with scores, via a REST API endpoint.

**Out-of-scope elaboration:** Thumbnail optimization, multilingual support, and real-time YouTube Studio integration are acknowledged as valuable extensions but are explicitly excluded from this research prototype to maintain a focused, evaluable scope.

### 1.11 Chapter Summary
- Summarize the problem (creator discovery bottleneck driven by metadata quality)
- Restate the research aim and four objectives
- Note the research question that guides the study
- Signal the structure of the rest of the thesis (Ch2 → Literature Review, Ch3 → Methodology, Ch4 → System Design, Ch5 → Implementation, Ch6 → Evaluation, Ch7 → Conclusion)

---

## CHAPTER 2 — Literature Review ✅ DONE

> Coverage ratios from template: Domain Overview 10% | Existing Systems 30% | Technological Analysis 60%

### Chapter Overview
- Purpose of the literature review and how it is organized
- Introduce the three domains: User Engagement Psychology, Generative AI & Prompt Engineering, Clickbait Ethics
- Signal the conceptual map

### Conceptual Map of the Literature
*(Create a diagram or table showing how the reviewed literature connects)*
- Three columns/nodes: Psychological Theories → AI/NLP Technologies → Ethical Frameworks
- Show how each connects to the research problem
- Reference key authors at each node

### Domain Overview *(10% coverage — surface-level but significant)*
- The video-first internet and creator economy context
- YouTube as a primary discovery platform; CTR as the algorithmic gatekeeper
- The metadata optimization problem: title and thumbnail as decision triggers
- Historical evolution: manual copywriting → SEO tools → AI-assisted generation
- Transition to the review of specific studies and systems

### Existing Systems, Frameworks, and Designs *(30% coverage — comparative + personal reflection)*

**System 1: Manual Expert Copywriting**
- Description: Human copywriters applying heuristic trigger knowledge
- Strengths: High quality, nuanced, culturally aware
- Weaknesses: Unscalable, expensive, inconsistent
- Personal reflection: Sufficient for individual creators but cannot address the scale of 500 hours/minute uploads

**System 2: YouTube Analytics Platforms (TubeBuddy, VidIQ)**
- Description: Data dashboards showing historical CTR, keyword suggestions, trend data
- Strengths: Rich empirical data, channel benchmarking
- Weaknesses: Reactive (user-driven), no generative capability, no psychological grounding
- Personal reflection: Useful for analysis but absent from the generation problem entirely

**System 3: Generic LLM Prompting ("Write me a YouTube title")**
- Description: Zero-shot or basic prompting of GPT-4/Claude/Llama
- Strengths: Scalable, accessible, no cost barrier
- Weaknesses: Flat/descriptive outputs, no psychological trigger operationalization, high hallucination risk (PLOS ONE, 2024)
- Personal reflection: The "black box" problem — user needs "prompt literacy" to extract useful results; most users don't have it

**System 4: Clickbait Detection Systems (ClickGuard, SemEval shared tasks, Webis Corpus tools)**
- Description: Classification models trained to detect deceptive headlines
- Strengths: Strong NLI/NLP grounding, robust datasets available
- Weaknesses: Detection only — no optimization pathway, binary verdict with no constructive alternative
- Personal reflection: The inverse problem is unsolved: these systems know what bad looks like but cannot produce what good looks like

**Comparative Summary Table:**
| System | Proactive | Psychologically Grounded | Generative | Faithfulness Check | Scalable |
|---|---|---|---|---|---|
| Expert Copywriting | No | Yes | Yes (manual) | Yes (human) | No |
| TubeBuddy/VidIQ | No | No | No | N/A | Yes |
| Generic LLM | No | No | Yes | No | Yes |
| Clickbait Detectors | No | Partial | No | Yes (detection only) | Yes |
| **This System** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** |

**Research gap emerging from this comparison:** No existing system is simultaneously proactive, psychologically grounded, generative, and ethically constrained. This gap justifies the proposed system.

### Technological Analysis *(60% coverage — algorithmic, design, workflow analysis)*

#### Algorithmic Analysis

**A1: Large Language Models (Transformers)**
- Transformer architecture: self-attention for long-range context and nuance (Vaswani et al., 2017)
- GPT-4o: state-of-the-art instruction-following, structured JSON output, native function calling
- Llama 3: open-source alternative, local deployment, fine-tuning viable
- Why LLMs for title generation: ability to generate human-like creative text with constraint satisfaction
- Limitation of raw LLMs: generic outputs without specialized prompting (PLOS ONE, 2024)

**A2: Prompt Engineering Techniques**
- Few-Shot Prompting (Brown et al., 2020): in-context examples significantly improve output quality without weight updates
- Chain-of-Thought (CoT) Reasoning (Wei et al., 2022): step-by-step reasoning improves creative and analytical tasks
- Persona Pattern: role assignment aligns model output with expert professional standards
- Vector similarity retrieval for dynamic few-shot example selection

**A3: Sentiment Analysis — VADER**
- Hutto & Gilbert (2014): lexicon + heuristic rules for short informal social media text
- Returns compound score (−1 to +1): used as emotional arousal proxy in Critic Agent
- Captures capitalization, punctuation, negation, and degree modifiers
- Validated on social media corpora; pre-trained, no GPU required

**A4: Semantic Faithfulness — BERTScore**
- Zhang et al. (2020): cosine similarity between contextual BERT embeddings
- Measures semantic distance between generated title and video summary
- Used as relevance filter (BERTScore < 0.30 = off-topic)
- Limitation: measures similarity, not truthfulness

**A5: Natural Language Inference (NLI)**
- Models: `facebook/bart-large-mnli`, `roberta-large-mnli`
- Three-class classification: Entailment / Neutral / Contradiction
- Hard rejection gate: any title classified as "Contradiction" to the video's core promise is eliminated
- ACL 2025: NLI-based faithfulness correlates more strongly with human judgments than BERTScore alone
- Critical algorithmic component — addresses the deception problem directly

**A6: Predicted CTR (pCTR) — Machine Learning**
- Random Forest: ensemble of decision trees; 80.1% accuracy on title + metadata features (prior research)
- XGBoost: gradient boosting; F1 = 0.741 on YouTube virality tasks (prior research)
- Feature set: title length, word count, VADER compound, has_number, trigger_type, all_caps_ratio, category
- Target variable: Virality_Score = Views / Subscriber_Count (normalized proxy for CTR)
- RMSE benchmark: 3.48% on YouTube CTR prediction (prior XGBoost study)

#### Design Analysis

**D1: Multi-Agent Architecture**
- Supervisor pattern: Controller → Analyzer → Generator → Critic
- LangGraph for stateful graph-based agent transitions
- Each agent has an isolated context window — a deliberate anti-hallucination architectural decision
- Aligns with DSR artifact design principles: modular, evaluable, extensible

**D2: API Wrapper with Facade Pattern**
- Facade: FastAPI endpoint hides internal complexity from caller
- Factory: Prompt Factory constructs context-aware prompts dynamically per request
- Client submits simple payload (transcript/description); receives ranked titles with scores
- Enables scalability and ease of integration — any application can consume the API

**D3: Psychological Trigger Operationalization**
- Information Gap Theory (Loewenstein, 1994; Golman & Loewenstein, 2018) → T1 Curiosity Gap prompt templates
- Prospect Theory (Kahneman & Tversky, 1979) → T2 Loss Aversion prompt templates
- Social Proof (Cialdini, 1984) → T3 Authority/Scale prompt templates
- Emotional Arousal (Berger & Milkman, 2012) → T5 Extreme/Superlative + VADER arousal targeting

#### Workflow Analysis

**W1: Dataset Pipeline**
- Kaggle YouTube Trending Dataset (rsrishav): daily US trending, proxy for viral patterns
- Kaggle Classic Dataset (datasnaek): 29,089 historical videos, widely used in academic ML
- YouTube Data API v3: targeted scraping from high-CTR channels (MrBeast, Veritasium)
- Webis Clickbait Corpus: negative examples for validation layer training
- Data cleaning: de-duplication, normalization, toxicity filtering, non-English removal

**W2: Evaluation Workflow**
- Offline ML evaluation: F1-score, ROC-AUC, RMSE on held-out test set (15%)
- System-level evaluation: pCTR score, VADER arousal, BERTScore, Self-BLEU, acceptance rate
- Human evaluation: A/B preference survey (n=50+), 4-dimension rubric (Curiosity, Emotional Impact, Clarity, Trustworthiness)
- LLM-as-a-Judge: automated rubric scoring by GPT-4o; cross-validated against human scores

### Reflection — Research Gap Justification
*(Link literature findings to the gap; cite sources from within the last 5 years where possible)*
- From the algorithmic analysis: LLMs can generate text but not systematically optimize it for CTR without specialized prompting infrastructure
- From the design analysis: no existing system operationalizes psychological trigger theory as explicit prompt engineering constraints
- From the existing systems comparison: the proactive + psychologically grounded + ethically constrained combination is unoccupied in the literature
- From the ethical dimension: the clickbait literature identifies deception as a problem but provides no constructive engineering solution
- Conclusion: this research addresses a real, documented, multi-dimensional gap at the intersection of generative AI, behavioral psychology, and digital marketing ethics

---

## CHAPTER 3 — Methodology ✅ DONE

### 3.1 Research Paradigm
- **Paradigm: Pragmatism**
- Pragmatism holds that knowledge is evaluated by its practical consequences — truth is what works
- Justification: This research does not seek to discover a fundamental scientific law; it seeks to build and evaluate a useful artifact. Pragmatism accommodates both qualitative insights (human evaluation, expert rubric) and quantitative measurement (pCTR, F1, BERTScore)
- Contrast with Positivism (pure measurement, lab isolation — unsuitable for a sociotechnical AI system) and Interpretivism (subjective meaning — unsuitable for a system measured by objective metrics)
- Pragmatism allows the mixing of methods: quantitative ML evaluation + qualitative human preference survey

### 3.2 Research Approach
- **Approach: Abductive (Pragmatic)**
- Not purely deductive (we are not testing a pre-existing hypothesis) and not purely inductive (we are not discovering patterns from scratch)
- Abductive: we reason from established psychological theories (Information Gap, Prospect Theory) to design an artifact, then evaluate it empirically
- This is consistent with DSR's "Build and Evaluate" cycle: theoretical grounding → artifact construction → empirical validation

### 3.3 Research Strategy
- **Strategy: Design Science Research (DSR)**
- DSR is the dominant research paradigm in IS/SE when the primary output is a novel artifact
- Peffers et al. (2007): DSR emphasizes Rigor (grounding in theory) and Relevance (solving a real problem)
- Alternative strategies considered and rejected:
  - Case Study: appropriate for studying existing phenomena, not creating new ones
  - Experiment: would require a live YouTube channel with significant traffic for real CTR — outside project scope
  - Survey: captures opinions, not system performance
- DSR is the most methodologically sound choice for a software artifact evaluated against defined performance objectives

### 3.4 Fact Collection Mechanisms
*(Data for training, evaluation, and few-shot prompting)*

| Data Type | Source | Purpose |
|---|---|---|
| YouTube trending titles + engagement metrics | Kaggle (rsrishav, datasnaek) | ML model training, feature extraction |
| High-performing titles from top channels | YouTube Data API v3 | Few-shot Prompt Database population |
| Annotated clickbait titles | Webis Clickbait Corpus | Validation layer training (negative examples) |
| Manual trigger-type labels | Custom annotation (500–1,000 titles) | Trigger classification feature for pCTR model |
| Human preference ratings | A/B survey (n=50+) | Qualitative evaluation |

All secondary data is publicly available or ethically collected via API with no personal data involved.

### 3.5 Research Methodology
- **Methodology: Peffers' Design Science Research Methodology (DSRM)**
- Selected because it provides a structured, phase-by-phase framework for artifact-oriented research in IS/SE
- Six-phase process maps directly onto this project's workflow

### 3.6 Execution Workflow *(Tabular — maps each DSRM activity to this project)*

| DSRM Activity | Project Action | Output |
|---|---|---|
| 1. Problem Identification & Motivation | Analyze creator CTR bottleneck; literature review of clickbait and LLM research | Research problem statement; justification of value |
| 2. Define Objectives | Specify system requirements: proactive, psychologically grounded, ethically constrained title generation | Four research objectives (1.7.1–1.7.4); system specification |
| 3. Design & Development | Architect multi-agent pipeline; engineer prompts; implement pCTR ML model; build FastAPI backend | Working system prototype; Prompt Database; trained ML model |
| 4. Demonstration | Apply system to 10+ diverse video topics across 3 categories (Education, Entertainment, Tech) | Demonstration dataset with generated title outputs and scores |
| 5. Evaluation | Offline ML metrics; system-level scoring; human A/B survey; LLM-as-a-Judge rubric | Quantitative and qualitative evaluation report; comparison against baselines |
| 6. Communication | Dissertation write-up; potential academic paper formatting | Thesis document; GitHub repository |

### 3.7 Project Management Methodology
- **Methodology: Agile (Scrum-inspired)**
- Justification: The system involves iterative development where each agent (Analyzer, Generator, Critic) and each evaluation layer (VADER, BERTScore, NLI, pCTR) is built and tested incrementally. Agile accommodates the discovery of new requirements during development (e.g., prompt template refinement based on output quality)
- Alternative considered: PRINCE2 — too heavyweight and documentation-focused for a single-researcher academic project
- Sprint structure: 2-week sprints; each sprint delivers a testable component
- Tools: GitHub for version control; task tracking via project board

### 3.8 Project Timeline

| Phase | Deliverable | Target Date |
|---|---|---|
| Interim Submission 01 | Chapter 1, 2, 3 | 28 June 2026 |
| Sprint 1 — Data & ML | Dataset pipeline + pCTR model trained | 12 July 2026 |
| Sprint 2 — Analyzer Agent | Analyzer Agent working; video brief output validated | 19 July 2026 |
| Sprint 3 — Generator Agent | Generator with Prompt DB + CoT + Few-Shot; 5 candidates per run | 26 July 2026 |
| Sprint 4 — Critic Agent | Full pipeline end-to-end; NLI, VADER, BERTScore integrated | 2 August 2026 |
| Sprint 5 — FastAPI & Integration | REST API live; full pipeline accessible via endpoint | 9 August 2026 |
| Sprint 6 — Evaluation | Human survey completed; LLM-as-a-Judge scoring done; results compiled | 16 August 2026 |
| Chapter 4 — System Design | SRS, diagrams, architecture chapter written | 19 August 2026 |
| Chapter 5 — Implementation | Implementation chapter written with code snippets/pseudocode | 21 August 2026 |
| Chapter 6 — Results | Evaluation chapter written with tables, graphs, analysis | 23 August 2026 |
| Chapter 7 — Conclusion | Concluding chapter; final thesis assembled | 25 August 2026 |
| Final Submission | Complete thesis + system repository | 28 August 2026 |

### 3.9 Ethical Considerations
1. **Deception vs. Persuasion:** The system is explicitly designed to reject titles that factually contradict the source video (NLI hard rejection). The artifact promotes "engaging but honest" output — not clickbait.
2. **Data Privacy:** All datasets used are publicly available (Kaggle, YouTube Data API v3 in compliance with YouTube ToS). No personal user data is collected.
3. **Bias and Toxicity:** Trending data may contain hate-watching or toxic engagement patterns. A toxicity filter (`unitary/toxic-bert`) sanitizes the few-shot Prompt Database to prevent the LLM from optimizing for harmful engagement signals.
4. **Transparency:** The system is presented as a co-pilot for creators, not a replacement for human editorial judgment. The "black box" nature of the underlying LLM is acknowledged and reported transparently.
5. **Academic Integrity:** All sources are cited per IEEE format. The artifact is a research prototype and is not intended for commercial deployment without further ethical review.
6. **Platform Compliance:** The NLI faithfulness layer directly supports YouTube's Terms of Service (Section 4H) prohibiting misleading metadata.

### 3.10 Chapter Summary
- Recap: Pragmatist paradigm, abductive approach, DSR strategy, Peffers DSRM methodology
- Explain that the design decisions made in this chapter (agent architecture, dataset selection, evaluation metrics) are grounded in both theoretical rigor and practical relevance
- Signal that Chapter 4 proceeds to operationalize these methodological decisions into a full system requirements specification and design

---

## REMAINING CHAPTERS — Next Up After Implementation Sprints 1–4

### Chapter 4 — System Requirements Specification ✅ DONE (13 Aug 2026)
*(Target: ~19 August 2026 — completed early)*
- [x] 4.1 Chapter Overview
- [x] 4.2 Stakeholder Analysis (content creators, researchers, platform algorithms)
- [x] 4.3 Operationalization Process (mapping research objectives to system components)
- [x] 4.4 Use Case Diagrams with specifications (all 3 in body — Generate Titles, Review Scores, Health Check)
- [x] 4.5 Class Diagram
- [x] 4.6 Activity Diagram
- [x] 4.7 Sequence Diagrams (2 — happy path, Critic rejection logic)
- [x] 4.8 Proposed System Architecture Diagram (includes the new frontend layer)
- [x] 4.9 Functional Requirements (11 FRs)
- [x] 4.10 Non-Functional Requirements (7 NFRs — performance, reliability, scalability, security, maintainability, interpretability, reproducibility)
- [x] 4.11 Chapter Summary

All 6 diagrams built as Mermaid source (`thesis/assets/ch4_*.mmd`) and rendered to PNG via `mermaid-cli` (`thesis/assets/ch4_*.png`). Grounded directly in the actual implemented code (agents, schemas, API, LangGraph pipeline) rather than a forward-looking plan, since implementation was already complete. References: Gamma et al. (Facade pattern), Sommerville (FR/NFR distinction), Jacobson et al. (use case methodology), OMG UML spec, LangChain docs — all cited in-text.

### Chapter 5 — Implementation ✅ DONE (14 Aug 2026)
*(Target: ~21 August 2026 — completed early)*
- [x] Tech stack justification table (Python, FastAPI, LangChain, GPT-4o, etc.)
- [x] Analyzer Agent implementation (code snippet + discussion)
- [x] Prompt Factory + Prompt Database (vector retrieval implementation)
- [x] Generator Agent CoT sequence (code snippet + output example)
- [x] pCTR ML Model (training pipeline, shared feature module, live scoring)
- [x] Critic Agent (VADER + BERTScore + NLI integration, concurrency fix documented)
- [x] FastAPI endpoint (request/response schema, code snippet)
- [x] Sample end-to-end output with scores (Section 5.11, real Sprint 6 eval run)
- [x] Chapter Summary
- [x] Diagrams (added 15 Aug 2026, not in original checklist): Figure 5.1 Module Dependency Structure (§5.3), Figure 5.2 Critic Agent Parallel Scoring (§5.8), Figure 5.3 Deployment and Component View (§5.10) — built as Mermaid source (`thesis/assets/ch5_*.mmd`) and rendered to PNG via `mermaid-cli`, same settings as Chapter 4's diagrams (white background, 2352px width)

All listings are drawn directly from the working repository code (agents, pipeline, api, frontend) rather than pseudocode. A consolidated deviations table (Section 5.12) cross-references every implementation-level deviation already logged in this file's own sprint checklists, so Chapter 6 can be written without re-deriving them. Frontend (`system/frontend/`, added post-Sprint-5 as a scope amendment) is documented in a new Section 5.10, not originally in this checklist.

### Chapter 6 — Testing and Evaluation ✅ DONE (10 Sep 2026)
*(Target: ~23 August 2026 — closed out late, after the human survey's distribution and collection)*
- [x] Test plan (11 functional test cases in body — all pass; PLAN_THESIS originally said "10", the actual suite has 11, none redundant, so none deferred to an appendix)
- [x] Offline ML evaluation (F1=0.6901, ROC-AUC=0.7613 — neither target met, previously-logged deferred gap; confusion matrix, ROC curve, feature importance all plotted)
- [x] System-level evaluation (4/6 targets met — acceptance rate 0.94, avg pCTR 0.685, Self-BLEU 0.054, latency P95 9.95s all met; VADER arousal 0.265 and BERTScore 0.872 both missed, both explained as metric/design-tension gaps not silent failures)
- [x] Human evaluation A/B survey results — **collected 2026-09-04, analyzed 2026-09-10**: n=29 respondents (exceeded the n=15–20 pilot target), reshaped and run through `human_eval_analysis.py`. System leads both baselines on raw-mean curiosity/emotional impact, but no Wilcoxon comparison reaches significance at α=0.05 (all p > 0.1); human/LLM-judge inter-rater reliability on curiosity is weak and non-significant (r=−0.14, p=0.72, n=9 pairs). Written up honestly in §6.6 as directionally consistent but statistically inconclusive at this pilot scale, not oversold as confirmation.
- [x] LLM-as-a-Judge evaluation results (60/60 complete; system beats Baseline A significantly on curiosity/urgency/overall, beats Baseline B significantly only on relevance)
- [x] Comparison against Baseline A (descriptive) and Baseline B (zero-shot LLM) — written up honestly as a bounded claim, not overstated (§6.8, now includes real human-survey rows)
- [x] Non-functional testing (latency P95 = 9.95s, met narrowly; 0 errors across 20 system-eval runs + 11 functional tests)
- [x] Review on test strategies and their suitability (VADER/BERTScore flagged as possibly the wrong instruments, not just missed targets; §6.9 now also discusses the LLM-judge/human-survey agreement gap)

Backfill completed 2026-09-10: `system/evaluation/reshape_human_eval_responses.py` (new) reshapes the Google Forms wide export into the long format `human_eval_analysis.py` expects; ran analysis → `system/evaluation/outputs/human_eval_results.json`; Tables 6.5–6.9 renumbered and rewritten with real figures across §6.6/6.8/6.9/6.10. `PLAN_IMPLEMENTATION.md` §6.3/§6.4 and `SOURCE_OF_TRUTH.md` §19.3 updated in step.

### Chapter 7 — Concluding Remarks ✅ DONE (10 Sep 2026)
*(Target: ~25 August 2026 — revised 10 Sep 2026 once Ch6's human survey data landed)*
- [x] Accomplishment of objectives 1.7.1–1.7.4 (triangulate with evaluation results) — 1.7.3 fully met; 1.7.1, 1.7.2, and 1.7.4 all met with honest qualifications (moderate ML power; statistically bounded prompting advantage; pilot-scale human survey directionally consistent but not statistically significant)
- [x] Problems encountered during research and development — data availability constraints on the pCTR model, the Sprint 5 concurrency/correctness bug, the two-stage human-study descoping, the Baseline A definition compromise
- [x] Self-reflection on the research process — benefit/risk of self-implementation-and-evaluation, value of the running sprint deviation log, one concrete process change (parallelize survey distribution earlier, which would have freed time to recruit toward the original n=50+ target)
- [x] Real-world application possibilities — independent creators/educators, small-org marketing teams, A/B testing tooling integration
- [x] Future recommendations (now led by scaling the human survey to statistical power, since collection itself is done; then: arousal classifier, pCTR data/hyperparameter work, thumbnail integration, multilingual, real-time A/B/YouTube Studio hook, fine-tuned domain LLM)

**Note:** Ch7 was originally written against Ch6 with the human survey pending; both chapters were revised together on 2026-09-10 once real n=29 response data existed, so Ch7's Objective 1.7.4 assessment, Table 7.1, and Section 7.6's recommendation 1 now reflect the actual (statistically inconclusive but directionally consistent) result rather than a pending-data placeholder.

---

*Plan maintained by: Dulhara | SOT: SOURCE_OF_TRUTH.md | Template: Dulanjali Wijesekara Chapter Breakdown v1.1*
