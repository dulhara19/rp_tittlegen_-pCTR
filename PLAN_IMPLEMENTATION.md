# IMPLEMENTATION PLAN
### AI-Powered YouTube Title Optimizer — System Build
### P.A.D.B. Pathiraja (29071) | Dulhara (Developer)
### SOT Authority: SOURCE_OF_TRUTH.md

> Every component below maps to a section in SOURCE_OF_TRUTH.md. No implementation decision should contradict the SOT. If it must deviate, update the SOT first.

---

## Timeline Overview

| Sprint | Dates | Focus | SOT Sections |
|---|---|---|---|
| Sprint 1 | 29 Jun – 12 Jul | Dataset pipeline + pCTR ML model | §15, §16 |
| Sprint 2 | 13 Jul – 19 Jul | Analyzer Agent | §12.1 |
| Sprint 3 | 20 Jul – 26 Jul | Generator Agent + Prompt Engineering | §12.2, §13 |
| Sprint 4 | 27 Jul – 2 Aug | Critic Agent (VADER + BERTScore + NLI + pCTR scoring) | §12.3, §14.4, §14.5 |
| Sprint 5 | 3 Aug – 9 Aug | FastAPI backend + full pipeline integration | §14.1, §14.2, §11 |
| Sprint 6 | 10 Aug – 16 Aug | Evaluation — ML metrics, human survey, LLM-as-a-Judge | §19 |

---

## SPRINT 1 — Dataset Pipeline + pCTR ML Model
**Dates:** 29 June – 12 July 2026
**Goal:** Raw data → cleaned features → trained, evaluated pCTR classifier

### 1.1 Data Acquisition
- [ ] Download Kaggle YouTube Trending Dataset (`rsrishav/youtube-trending-video-dataset`)
- [ ] Download Kaggle Classic Dataset (`datasnaek/youtube-new`)
- [ ] Set up YouTube Data API v3 credentials
- [ ] Scrape top 500 titles from: MrBeast, Veritasium, Mark Rober, Kurzgesagt
- [ ] Download Webis Clickbait Corpus (for validation layer negative examples)

### 1.2 Data Cleaning
*(Reference: SOT §15.4)*
- [ ] De-duplicate trending entries (collapse per-day rows to single entry with peak metrics)
- [ ] Remove videos with < 1,000 views
- [ ] Remove non-English titles
- [ ] Remove pure SEO keyword strings (no natural language)
- [ ] Normalize subscriber count to upload date (not current)
- [ ] Apply toxicity filter (`unitary/toxic-bert`) to sanitize few-shot candidate titles
- [ ] Handle emojis: preserve and tokenize (do not strip)

### 1.3 Feature Engineering
*(Reference: SOT §15.2)*
- [ ] `title_length_chars` — `len(title)`
- [ ] `title_word_count` — `len(title.split())`
- [ ] `has_number` — regex `\d+`
- [ ] `number_value` — extract and parse numeric value
- [ ] `vader_compound`, `vader_positive` — VADER scoring
- [ ] `first_word_type` — POS tag via spaCy/NLTK
- [ ] `has_question` — `?` in title
- [ ] `has_exclamation` — `!` in title
- [ ] `all_caps_ratio` — word-level caps check
- [ ] `has_emoji` — boolean emoji detection
- [ ] `category_id` — from metadata
- [ ] `channel_subscriber_tier` — binned (0–10K, 10K–100K, 100K–1M, 1M+)
- [ ] `trigger_type` — manual annotation (T1–T7) for 500–1,000 titles

### 1.4 Target Variable Construction
*(Reference: SOT §15.3)*
- [ ] Compute `Virality_Score = Views / Subscriber_Count`
- [ ] Create binary label: Class 0 (below median) / Class 1 (above median)
- [ ] Log the distribution and threshold used; save to documentation

### 1.5 ML Model Training
*(Reference: SOT §16)*
- [ ] Split: 70% train / 15% validation / 15% test (hold test set until final evaluation)
- [ ] Train Random Forest: tune `n_estimators` (100–500), `max_depth` (10–30)
- [ ] Train XGBoost: tune `learning_rate` (0.01–0.1), `n_estimators`, `max_depth` (3–8), L1+L2 reg
- [ ] Hyperparameter tuning: `RandomizedSearchCV` or Optuna
- [ ] Evaluate on validation set: F1-score (primary), ROC-AUC, Precision, Recall
- [ ] Run RMSE if regression variant is trained
- [ ] Plot feature importance for top 10 features
- [ ] Save best model as `pctr_model.pkl` (joblib)

### 1.6 Sprint 1 Exit Criteria
- Cleaned dataset with all features computed
- pCTR model achieving F1 > 0.70 on validation set (target F1 > 0.75 on test)
- Feature importance plot showing VADER, has_number, title_length as top signals
- `pctr_model.pkl` saved and callable via a `predict(title_features) → float` function

---

## SPRINT 2 — Analyzer Agent
**Dates:** 13 July – 19 July 2026
**Goal:** Working Analyzer Agent that converts raw video input into a structured video brief

### 2.1 Input Schema
*(Reference: SOT §11.3)*
```python
class VideoInput(BaseModel):
    video_transcript: str
    video_description: Optional[str]
    video_category: str
    channel_stats: Optional[dict]  # {subscribers, avg_views}
```

### 2.2 Analyzer Responsibilities
*(Reference: SOT §12.1)*
- [ ] Extract `core_promise` — one sentence: what the video actually delivers
- [ ] Extract `key_entities` — list of proper nouns, numbers, stakes from transcript
- [ ] Score `emotional_potential` (0–1) — ceiling of truthful emotional framing possible
- [ ] Identify `trigger_candidates` — which T1–T7 triggers are authentic for this content

### 2.3 Analyzer Output Schema
```python
class VideoBrief(BaseModel):
    core_promise: str
    key_entities: List[str]
    emotional_potential: float  # 0–1
    trigger_candidates: List[str]  # e.g., ["T1", "T3", "T6"]
```

### 2.4 Prompt Design for Analyzer
- System prompt: Persona pattern (analytical video content expert)
- Instruction: Extract factual elements only — no creative interpretation
- CoT step 1: "What does this video actually deliver to the viewer?"
- CoT step 2: "What real entities (numbers, names, stakes) are present?"
- CoT step 3: "What is the strongest truthful emotional angle possible?"
- CoT step 4: "Which psychological triggers authentically apply to this content?"
- Output: structured JSON matching `VideoBrief` schema

### 2.5 Anti-Hallucination Constraint
- Analyzer must ground every output in the raw transcript — no inference beyond what's stated
- If a fact is not in the transcript, it must not appear in `key_entities`
- This is the architectural deception-prevention mechanism (SOT §12.1)

### 2.6 Sprint 2 Exit Criteria
- Analyzer Agent runs on 10 test transcripts and produces valid `VideoBrief` JSON
- Manually verify core_promise is factually accurate for each test case
- Confirm no entities appear in output that weren't in the input transcript

---

## SPRINT 3 — Generator Agent + Prompt Engineering
**Dates:** 20 July – 26 July 2026
**Goal:** Generator Agent producing 5 psychologically diverse, length-constrained title candidates

### 3.1 Prompt Database Setup
*(Reference: SOT §13.4)*
- [ ] Select top 200 high-performing titles from Sprint 1 dataset (highest Virality_Score)
- [ ] Manually categorize each by Hook Type (Curiosity Gap, Loss Aversion, Social Proof, Urgency, Superlative, Personal Stakes, Number+Specificity)
- [ ] Embed titles using `text-embedding-3-small` (OpenAI) or sentence-transformers
- [ ] Store in vector store (ChromaDB or FAISS)
- [ ] Implement `retrieve_examples(topic: str, category: str, k: int = 5) → List[str]`

### 3.2 Generator Prompt Architecture
*(Reference: SOT §13.1, §13.2, §13.3)*

**Layer 1 — Persona:**
```
You are a viral YouTube title copywriter with 10+ years of experience optimizing CTR for 
top creators. You have deep expertise in psychological triggers, curiosity gaps, and emotional 
arousal engineering. Your goal is to write titles that are compelling, honest, and click-worthy.
```

**Layer 2 — Few-Shot Examples (dynamic, retrieved per request):**
```
Here are high-performing titles in this niche:
[Retrieved Example 1]
[Retrieved Example 2]
[Retrieved Example 3]
Learn from their structure and psychological trigger patterns.
```

**Layer 3 — CoT Instructions:**
```
Step 1: Analyze the video brief. Identify the core Information Gap a viewer would want resolved.
Step 2: Determine the strongest high-arousal emotional angle this content authentically supports.
Step 3: Draft one title for each of these triggers: {trigger_candidates from video brief}
Step 4: Refine each title for mobile impact — target 55–70 characters, hard cap 100.
Step 5: Return exactly 5 titles as structured JSON with trigger_used and char_count.
```

### 3.3 Generator Output Schema
```python
class TitleCandidate(BaseModel):
    title: str
    trigger_used: str  # e.g., "T1 - Curiosity Gap"
    char_count: int
    word_count: int

class GeneratorOutput(BaseModel):
    candidates: List[TitleCandidate]  # exactly 5
```

### 3.4 Generator Constraints
- [ ] At least one loss-framing variant per batch (mandatory — SOT §12.2)
- [ ] At least one numerical variant per batch if key_entities contains numbers
- [ ] No title may exceed 100 characters (hard cap)
- [ ] Target 55–70 characters
- [ ] Generator receives only `VideoBrief` — never the raw transcript (anti-hallucination)

### 3.5 Sprint 3 Exit Criteria
- Generator runs end-to-end with Analyzer output as input
- Produces 5 candidates per run, each with different trigger
- Prompt Database retrieval returns topically relevant examples (verified manually for 10 test cases)
- All candidates within length constraints

---

## SPRINT 4 — Critic Agent
**Dates:** 27 July – 2 August 2026
**Goal:** Full scoring and rejection pipeline; composite score ranking; rejection log

### 4.1 pCTR Scoring
*(Reference: SOT §16.4, §12.3)*
- [ ] Extract title features from each candidate (same feature pipeline as Sprint 1)
- [ ] Call `pctr_model.predict(features) → float` for each candidate
- [ ] Store as `pctr_score` (0–1)

### 4.2 VADER Arousal Scoring
*(Reference: SOT §14.4)*
- [ ] Run VADER on each candidate title
- [ ] Store `vader_compound` (−1 to +1)
- [ ] Compute arousal: `abs(vader_compound)`
- [ ] Titles with `abs(vader_compound) < 0.5` are penalized (not rejected, but lower composite score)

### 4.3 BERTScore Relevance Check
*(Reference: SOT §14.5, §17.4)*
- [ ] Compute BERTScore between `title` and `core_promise` from `VideoBrief`
- [ ] Store `bert_similarity` (0–1)
- [ ] If `bert_similarity < 0.30`: flag for manual review (potentially off-topic)
- [ ] If `bert_similarity > 0.60`: note as potentially boring/descriptive (acceptable but low bonus)

### 4.4 NLI Faithfulness Gate
*(Reference: SOT §14.5, §17.3)*
- [ ] Load `facebook/bart-large-mnli` from HuggingFace
- [ ] For each candidate:
  ```
  premise   = generated_title
  hypothesis = core_promise (from VideoBrief)
  ```
- [ ] Classify: `entailment` / `neutral` / `contradiction`
- [ ] **If `contradiction`: hard reject — add to `rejection_log`, set `is_valid = False`**
- [ ] `entailment` or `neutral`: `is_valid = True`

### 4.5 Composite Scoring
*(Reference: SOT §11.4)*
```python
nli_multiplier = 1 if is_valid else 0
composite_score = (
    0.50 * pctr_score +
    0.25 * abs(vader_compound) +
    0.25 * bert_similarity
) * nli_multiplier
```

### 4.6 Critic Output Schema
```python
class ScoredTitle(BaseModel):
    title: str
    trigger_used: str
    pctr_score: float
    vader_compound: float
    bert_similarity: float
    nli_label: str
    composite_score: float
    is_valid: bool

class CriticOutput(BaseModel):
    scored_candidates: List[ScoredTitle]
    top_title: str
    rejection_log: List[str]
```

### 4.7 Sprint 4 Exit Criteria
- End-to-end pipeline: `VideoInput` → `VideoBrief` → `List[TitleCandidate]` → `CriticOutput`
- NLI correctly rejects at least 1 out of 5 candidates when a deliberately deceptive title is injected (manual test)
- Composite score ranking produces meaningful differentiation across 5 candidates

---

## SPRINT 5 — FastAPI Backend + Full Integration
**Dates:** 3 August – 9 August 2026
**Goal:** REST API exposing the full pipeline; production-ready Facade layer

### 5.1 API Architecture
*(Reference: SOT §11.1, §14.1)*
```
POST /generate-titles
  Request: VideoInput (transcript, description, category, channel_stats)
  Response: CriticOutput (scored candidates, top title, rejection log)

GET /health
  Response: {status: "ok", model_versions: {...}}
```

### 5.2 Async Implementation
- [ ] All agent calls (`await analyzer.run()`, `await generator.run()`, `await critic.run()`) are async
- [ ] pCTR model inference (CPU-bound) runs in `ProcessPoolExecutor`
- [ ] NLI/BERTScore inference (GPU-bound if available) in separate thread pool
- [ ] Gunicorn + Uvicorn for multi-worker production setup

### 5.3 LangGraph State Machine
*(Reference: SOT §14.2)*
- [ ] Define state graph: `START → Analyzer → Generator → Critic → END`
- [ ] Each agent node receives only the state slice it needs (no raw transcript in Generator)
- [ ] Error handling: if any agent fails, return structured error response (no silent failures)

### 5.4 Input Validation
- [ ] Pydantic models validate all inputs at API boundary
- [ ] Reject transcripts < 50 words (insufficient signal)
- [ ] Sanitize input text (strip HTML, normalize whitespace)

### 5.5 Sprint 5 Exit Criteria
- API responds to `POST /generate-titles` within P95 < 10 seconds (measure with Postman/locust)
- End-to-end test: 10 real video transcripts → valid JSON responses for all
- Error handling tested: empty transcript, invalid category, LLM timeout

---

## SPRINT 6 — Evaluation
**Dates:** 10 August – 16 August 2026
**Goal:** Complete all evaluation data required for Chapter 6

### 6.1 Offline ML Evaluation (pCTR Model)
*(Reference: SOT §19.2)*
- [ ] Run held-out test set (15%) through trained model
- [ ] Compute: F1-score, ROC-AUC, Precision, Recall, Confusion Matrix
- [ ] If regression variant: RMSE
- [ ] Plot: ROC curve, feature importance bar chart, confusion matrix heatmap
- [ ] Target: F1 > 0.75, ROC-AUC > 0.80

### 6.2 System-Level Evaluation
*(Reference: SOT §19.1)*
- [ ] Run 20 diverse video transcripts through full pipeline
- [ ] Record for each run: pCTR score, VADER arousal, BERTScore, is_valid count, Self-BLEU
- [ ] Compute averages across all runs
- [ ] Latency measurement: P50 and P95 end-to-end response time
- [ ] Target: acceptance rate > 60%, avg pCTR > 0.6, Self-BLEU < 0.4

### 6.3 Human Evaluation Survey
*(Reference: SOT §19.3)*
- [ ] Prepare 10 video descriptions as test stimuli (mix of Education, Tech, Entertainment)
- [ ] For each: generate 3 title variants — Baseline A (descriptive), Baseline B (zero-shot GPT-4o), System Output (YTO top-ranked)
- [ ] Distribute blinded survey to n=50+ participants (creators, marketing students, general users)
- [ ] 4-dimension rubric per title: Curiosity, Emotional Impact, Clarity, Trustworthiness (1–5)
- [ ] Compute mean scores per condition per dimension
- [ ] Run Wilcoxon signed-rank test or t-test to check statistical significance

### 6.4 LLM-as-a-Judge Evaluation
*(Reference: SOT §19.4)*
- [ ] Design judge prompt (GPT-4o as evaluator): Curiosity / Urgency / Relevance rubric (1–5 per dimension)
- [ ] Run judge on all 20 demonstration outputs × 3 conditions = 60 evaluations
- [ ] Compute inter-rater reliability between LLM judge scores and human survey scores (Cohen's Kappa or Pearson r)
- [ ] Document reliability and discuss limitations

### 6.5 Sprint 6 Exit Criteria
- All evaluation data collected and tabulated
- At least 3 charts/graphs ready for Chapter 6 (ROC curve, system metric bar chart, human survey grouped bar chart)
- Statistical comparison between YTO and baselines documented with significance values

---

## Repository Structure (Target)

```
youtube-title-optimizer/
├── data/
│   ├── raw/                    # Kaggle datasets, YouTube API data
│   ├── processed/              # Cleaned, feature-engineered datasets
│   └── prompt_db/              # Vector store for few-shot examples
├── models/
│   └── pctr_model.pkl          # Trained pCTR model
├── agents/
│   ├── analyzer.py             # Analyzer Agent
│   ├── generator.py            # Generator Agent
│   └── critic.py               # Critic Agent
├── pipeline/
│   ├── graph.py                # LangGraph state machine
│   └── prompt_factory.py       # Dynamic prompt construction
├── api/
│   └── main.py                 # FastAPI app + endpoints
├── evaluation/
│   ├── ml_eval.py              # pCTR model evaluation scripts
│   ├── system_eval.py          # System-level evaluation
│   └── judge.py                # LLM-as-a-Judge evaluation
├── notebooks/
│   ├── data_exploration.ipynb
│   └── model_training.ipynb
├── tests/
│   └── test_pipeline.py        # End-to-end test cases
├── requirements.txt
└── README.md
```

---

## Technology Quick Reference

| Component | Technology | Justification (SOT ref) |
|---|---|---|
| LLM | GPT-4o (primary), Llama 3 (fallback) | §14.3 |
| Agent Orchestration | LangChain + LangGraph | §14.2 |
| Backend | Python + FastAPI | §14.1 |
| Sentiment | VADER (NLTK) | §14.4 |
| Faithfulness | BERTScore + `facebook/bart-large-mnli` | §14.5 |
| pCTR Model | Random Forest + XGBoost (scikit-learn) | §16.1 |
| Vector Store | ChromaDB or FAISS | §13.4 |
| Embeddings | `text-embedding-3-small` or sentence-transformers | §13.4 |
| Toxicity Filter | `unitary/toxic-bert` | §15.4 |
| Feature Engineering | pandas + spaCy + NLTK | §15.2 |

---

## Sync Points with Thesis Plan

| Implementation Milestone | Thesis Chapter Unlocked |
|---|---|
| Architecture finalized (end Sprint 1 setup) | Chapter 4 — System Design can be written |
| All agents working (end Sprint 4) | Chapter 5 — Implementation can be written |
| Evaluation complete (end Sprint 6) | Chapter 6 — Results can be written |
| Full system + evaluation done | Chapter 7 — Conclusion can be written |

---

*Plan maintained by: Dulhara | SOT: SOURCE_OF_TRUTH.md | Thesis Plan: PLAN_THESIS.md*
