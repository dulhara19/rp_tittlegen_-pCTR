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
- [x] Download Kaggle YouTube Trending Dataset (`rsrishav/youtube-trending-video-dataset`)
- [x] Download Kaggle Classic Dataset (`datasnaek/youtube-new`)
- [ ] Set up YouTube Data API v3 credentials *(deferred to Sprint 3 — not required for pCTR training)*
- [ ] Scrape top 500 titles from: MrBeast, Veritasium, Mark Rober, Kurzgesagt *(deferred to Sprint 3)*
- [ ] Download Webis Clickbait Corpus (for validation layer negative examples) *(deferred to Sprint 3)*

### 1.2 Data Cleaning
*(Reference: SOT §15.4)*
- [x] De-duplicate trending entries (collapse per-day rows to single entry with peak metrics)
- [x] Remove videos with < 1,000 views
- [x] Remove non-English titles *(ASCII-ratio heuristic used instead of `langdetect` for runtime reasons — documented as a limitation, SOT §20)*
- [x] Remove pure SEO keyword strings (no natural language)
- [ ] Normalize subscriber count to upload date (not current) *(not applicable — neither Kaggle source ships subscriber_count; category-median proxy used instead, see 1.4)*
- [x] Apply toxicity filter (`unitary/toxic-bert`) to sanitize few-shot candidate titles
- [x] Handle emojis: preserve and tokenize (do not strip)

### 1.3 Feature Engineering
*(Reference: SOT §15.2)*
- [x] `title_length_chars` — `len(title)`
- [x] `title_word_count` — `len(title.split())`
- [x] `has_number` — regex `\d+`
- [x] `number_value` — extract and parse numeric value
- [x] `vader_compound`, `vader_positive` — VADER scoring
- [x] `first_word_type` — POS tag via spaCy/NLTK
- [x] `has_question` — `?` in title
- [x] `has_exclamation` — `!` in title
- [x] `all_caps_ratio` — word-level caps check
- [x] `has_emoji` — boolean emoji detection
- [x] `category_id` — from metadata
- [x] `channel_subscriber_tier` — binned (0–10K, 10K–100K, 100K–1M, 1M+) *(defaults to "0-10K" for all rows — no subscriber_count in source data, see 1.4)*
- [ ] `trigger_type` — manual annotation (T1–T7) for 500–1,000 titles *(not started — manual labeling task, not part of `data_exploration.ipynb`)*

### 1.4 Target Variable Construction
*(Reference: SOT §15.3)*
- [x] Compute `Virality_Score = Views / Subscriber_Count` *(fallback proxy used: `Views / category-median Views`, since neither Kaggle source includes subscriber_count — documented limitation, SOT §20)*
- [x] Create binary label: Class 0 (below median) / Class 1 (above median)
- [x] Log the distribution and threshold used *(printed in notebook EDA cell; not yet copied into standalone documentation)*

### 1.5 ML Model Training
*(Reference: SOT §16)*
- [x] Split: 70% train / 15% validation / 15% test (hold test set until final evaluation)
- [x] Train Random Forest: tune `n_estimators` (100–500), `max_depth` (10–30)
- [x] Train XGBoost: tune `learning_rate` (0.01–0.1), `n_estimators`, `max_depth` (3–8), L1+L2 reg
- [x] Hyperparameter tuning: `RandomizedSearchCV` or Optuna
- [x] Evaluate on validation set: F1-score (primary), ROC-AUC, Precision, Recall
- [ ] Run RMSE if regression variant is trained *(not applicable — classification variant only)*
- [x] Plot feature importance for top 10 features
- [x] Save best model as `pctr_model.pkl` (joblib)

### 1.6 Sprint 1 Exit Criteria
- [x] Cleaned dataset with all features computed — `labeled_titles.csv`, 154,471 rows
- [ ] pCTR model achieving F1 > 0.70 on validation set (target F1 > 0.75 on test) — **NOT MET, DEFERRED**: val F1 = 0.6958 (best model: Random Forest), test F1 = 0.6901. Just under threshold. A wider hyperparameter search (RF/XGB/ExtraTrees/GradientBoosting, more iterations) was scoped but not completed — deliberately deferred (2026-08-10) to unblock Sprint 3 rather than block the pipeline on a ~1-4pt F1 gap. Revisit before Chapter 6 evaluation is written.
- [ ] Feature importance plot showing VADER, has_number, title_length as top signals — plot generated (`feature_importance.png`), ranking not yet manually verified against this claim
- [x] `pctr_model.pkl` saved — saved to `system/models/pctr_model.pkl`; callable via `predict(title_features)` not yet verified outside the notebook

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
- [x] Extract `core_promise` — one sentence: what the video actually delivers
- [x] Extract `key_entities` — list of proper nouns, numbers, stakes from transcript
- [x] Score `emotional_potential` (0–1) — ceiling of truthful emotional framing possible
- [x] Identify `trigger_candidates` — which T1–T7 triggers are authentic for this content

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
- [x] Analyzer Agent runs on 10 test transcripts and produces valid `VideoBrief` JSON — `system/agents/analyzer.py`, `pytest system/tests/test_analyzer.py` (10/10 passed)
- [x] Manually verify core_promise is factually accurate for each test case — reviewed via `system/tests/manual_check_analyzer.py`, all 10 accurate
- [x] Confirm no entities appear in output that weren't in the input transcript — 0/10 flagged by the unsupported-entity check; manual review confirms all entities are grounded in transcript text

---

## SPRINT 3 — Generator Agent + Prompt Engineering
**Dates:** 20 July – 26 July 2026
**Goal:** Generator Agent producing 5 psychologically diverse, length-constrained title candidates

### 3.1 Prompt Database Setup
*(Reference: SOT §13.4)*
- [x] Select high-performing titles from Sprint 1 dataset — `system/pipeline/prompt_db.py::build()`. Deviated from a flat top-200 by global Virality_Score: that concentrated almost entirely in a few viral-outlier categories (Music, Shorts, trailers), starving niches like Education/Travel of same-category examples. Switched to top-15 per category_id (~254 titles total) — verified this measurably improves per-category retrieval relevance (see manual spot-check below).
- [x] Categorize each by Hook Type — heuristic keyword/regex classifier (`classify_hook_type`) reusing the Analyzer's T1-T7 taxonomy, not manual annotation of 200 titles. Documented deviation, same pattern as Sprint 1's ASCII-heuristic language filter (SOT §20).
- [x] Embed titles using `text-embedding-3-small` (OpenAI)
- [x] Store in vector store (ChromaDB, persisted to `system/data/prompt_db/`)
- [x] Implement `retrieve_examples(topic: str, category: str, k: int = 5) → List[str]` — category-filtered nearest-neighbor query with unfiltered fallback if a category has fewer than `k` matches

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
- [x] At least one loss-framing variant per batch (mandatory — SOT §12.2) — instructed in prompt, with an explicit anti-hallucination carve-out: only if the brief authentically supports a loss/mistake framing, else substitute the next-strongest applicable trigger
- [x] At least one numerical variant per batch if key_entities contains numbers
- [x] No title may exceed 100 characters (hard cap) — enforced both in-prompt and post-hoc (`generator.run` raises `ValueError` if violated)
- [x] Target 55–70 characters
- [x] Generator receives only `VideoBrief` — never the raw transcript (anti-hallucination); `video_category` is also passed in for retrieval, since it's metadata, not transcript content

### 3.5 Sprint 3 Exit Criteria
- [x] Generator runs end-to-end with Analyzer output as input — `system/agents/generator.py`, `pytest system/tests/test_generator.py` (10/10 passed)
- [x] Produces 5 candidates per run, each with different trigger — first prompt draft failed this on 1/10 cases (all 5 candidates landed on T7 for a numbers-heavy brief); added an explicit "TRIGGER DIVERSITY IS MANDATORY" constraint to the prompt, then re-ran — 10/10 passed
- [x] Prompt Database retrieval returns topically relevant examples (verified manually for 10 test cases) — spot-checked 6+ topics across categories after the per-category rebuild (3.1); examples are now genuinely niche-relevant (e.g. Science & Technology retrieves iPhone/Vision Pro/Galaxy Unpacked titles, not generic viral shorts)
- [x] All candidates within length constraints — asserted in `test_generator.py` (`char_count <= 100` and matches `len(title)`)

---

## SPRINT 4 — Critic Agent
**Dates:** 27 July – 2 August 2026
**Goal:** Full scoring and rejection pipeline; composite score ranking; rejection log

### 4.1 pCTR Scoring
*(Reference: SOT §16.4, §12.3)*
- [x] Extract title features from each candidate (same feature pipeline as Sprint 1) — `system/pipeline/pctr_scorer.py` reuses `build_features_single` from `features.py` directly, so live scoring can't silently diverge from the training-time transform
- [x] Call `pctr_model.predict(features) → float` for each candidate — uses `predict_proba` class-1 probability
- [x] Store as `pctr_score` (0–1)

### 4.2 VADER Arousal Scoring
*(Reference: SOT §14.4)*
- [x] Run VADER on each candidate title — reused from the same feature row computed for pCTR scoring rather than a second NLTK call
- [x] Store `vader_compound` (−1 to +1)
- [x] Compute arousal: `abs(vader_compound)` — used directly in the composite score formula
- [x] Titles with `abs(vader_compound) < 0.5` are penalized (not rejected, but lower composite score) — implicit in the weighted composite formula (4.5), no separate penalty step needed

### 4.3 BERTScore Relevance Check
*(Reference: SOT §14.5, §17.4)*
- [x] Compute BERTScore between `title` and `core_promise` from `VideoBrief` — `system/pipeline/bertscore_scorer.py`, default roberta-large model
- [x] Store `bert_similarity` (0–1) — F1 score
- [ ] If `bert_similarity < 0.30`: flag for manual review (potentially off-topic) — not implemented as a separate flag; composite score already suppresses low-relevance titles via the 0.25 weight. Revisit if Sprint 6 evaluation shows off-topic titles slipping through.
- [ ] If `bert_similarity > 0.60`: note as potentially boring/descriptive — not implemented, same reasoning as above

### 4.4 NLI Faithfulness Gate
*(Reference: SOT §14.5, §17.3)*
- [x] Load `facebook/bart-large-mnli` from HuggingFace — `system/pipeline/nli_scorer.py`, lazy-loaded on first use
- [x] For each candidate:
  ```
  premise   = generated_title
  hypothesis = core_promise (from VideoBrief)
  ```
- [x] Classify: `entailment` / `neutral` / `contradiction`
- [x] **If `contradiction`: hard reject — add to `rejection_log`, set `is_valid = False`** — verified with a deliberately injected contradictory title (`test_nli_hard_rejects_deliberate_contradiction`), correctly classified as `contradiction`
- [x] `entailment` or `neutral`: `is_valid = True`

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
- [x] End-to-end pipeline: `VideoInput` → `VideoBrief` → `List[TitleCandidate]` → `CriticOutput` — `system/agents/critic.py`, `pytest system/tests/test_critic.py` (3/3 end-to-end cases passed; ran on 3 of the 10 fixtures rather than all 10, since each case now loads/runs two heavy local models — bart-large-mnli and BERTScore's roberta-large — on top of the LLM calls, making a full 10-case run materially slower than Sprints 2-3)
- [x] NLI correctly rejects at least 1 out of 5 candidates when a deliberately deceptive title is injected (manual test) — `test_nli_hard_rejects_deliberate_contradiction`: injected a title claiming the opposite of a synthetic core_promise, NLI correctly classified it `contradiction`
- [x] Composite score ranking produces meaningful differentiation across 5 candidates — asserted in `test_critic_produces_valid_output` (`len(set(scores)) > 1`); a sample real run showed composite scores from 0.354 to 0.454 with the correct top_title selected

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
- [x] All agent calls (`await analyzer.run()`, `await generator.run()`, `await critic.run()`) are async — `critic.run()` was converted from sync to async so it can fan its own scoring out concurrently (see below) rather than being wrapped wholesale in a single `asyncio.to_thread`
- [x] pCTR model inference (CPU-bound) runs concurrently — **deviated from `ProcessPoolExecutor`**: each candidate's pCTR/BERTScore/NLI scoring runs via `asyncio.to_thread`, and all 5 candidates are scored concurrently via `asyncio.gather` (`system/agents/critic.py::_score_candidate`). A `ProcessPoolExecutor` would require re-loading the pCTR/BERTScore/NLI models in every worker process — expensive and awkward to pickle for the torch/transformers models on Windows. sklearn/torch inference release the GIL for most of their work, so a thread pool buys real concurrency without that cost.
- [x] NLI/BERTScore inference concurrent with pCTR — same `asyncio.gather` per candidate covers all three scorers. **Found and fixed a real bug getting here**: concurrently *loading* bart-large-mnli (NLI) and roberta-large (BERTScore) for the first time on two different threads corrupted transformers/accelerate's meta-device weight materialization (`RuntimeError: Tensor on device cpu is not on the expected device meta!`) — reproduced reliably via the full API test suite, and a lock around each module's lazy-load didn't fix it (a single isolated load succeeded; two *different* models loading concurrently on two threads still crashed). Fixed by loading both models eagerly at module import instead of lazily on first request, plus a `threading.Lock` around each model's forward pass as cheap insurance. See docstrings in `system/pipeline/nli_scorer.py` / `bertscore_scorer.py`.
- [x] Gunicorn + Uvicorn for multi-worker production setup — not deployed in this dev environment; recommended prod command documented: `gunicorn system.api.main:app -k uvicorn.workers.UvicornWorker -w 4`

### 5.3 LangGraph State Machine
*(Reference: SOT §14.2)*
- [x] Define state graph: `START → Analyzer → Generator → Critic → END` — `system/pipeline/graph.py`
- [x] Each agent node receives only the state slice it needs (no raw transcript in Generator) — Generator/Critic nodes read `video_brief` and `video_category`, never `video_input.video_transcript`
- [x] Error handling: if any agent fails, return structured error response (no silent failures) — each node catches its own exceptions into `state["error"]`; downstream nodes short-circuit once `error` is set; the API returns HTTP 502 with the error detail. Verified with a monkeypatched Generator failure (`test_pipeline_error_surfaces_as_502`).

### 5.4 Input Validation
- [x] Pydantic models validate all inputs at API boundary — `GenerateTitlesRequest` in `system/api/main.py`
- [x] Reject transcripts < 50 words (insufficient signal) — `field_validator` raises, FastAPI returns 422; verified in `test_rejects_short_transcript` / `test_rejects_empty_transcript`
- [x] Sanitize input text (strip HTML, normalize whitespace) — `_sanitize()`; strips HTML tags (not tag contents — this is strip_tags semantics, not an XSS filter, since the text is only ever fed to an LLM prompt, never rendered as HTML) and collapses whitespace

### 5.5 Sprint 5 Exit Criteria
- [x] API responds to `POST /generate-titles` within P95 < 10 seconds — **MET after fix**: originally measured ~29.5s average (Critic scored candidates sequentially). Parallelizing Critic's per-candidate scoring (5.2) brought this down to 6.3–9.0s across 10 real end-to-end calls (avg ~7.7s), `test_generate_titles_end_to_end`.
- [x] End-to-end test: 10 real video transcripts → valid JSON responses for all — `test_generate_titles_end_to_end`, 10/10 passed (plus an 11th case testing the category-fallback path)
- [x] Error handling tested: empty transcript, invalid category, LLM timeout — empty/short transcript → 422 (`test_rejects_empty_transcript`, `test_rejects_short_transcript`); invalid/unrecognized category → falls back to a default category_id rather than rejecting, locked in by `test_accepts_unrecognized_category_via_fallback`; simulated agent failure (stand-in for an LLM timeout) → 502 with error detail (`test_pipeline_error_surfaces_as_502`)

---

## SPRINT 6 — Evaluation
**Dates:** 10 August – 16 August 2026
**Goal:** Complete all evaluation data required for Chapter 6

### 6.1 Offline ML Evaluation (pCTR Model)
*(Reference: SOT §19.2)*
- [x] Run held-out test set (15%) through trained model — `system/evaluation/ml_eval.py` reconstructs the exact 70/15/15 split from `model_training.ipynb` (same `random_state=42`, same stratify), confirmed correct: reproduced test F1 = 0.6901, identical to Sprint 1's original number
- [x] Compute: F1-score, ROC-AUC, Precision, Recall, Confusion Matrix — F1=0.6901, ROC-AUC=0.7613, Precision=0.6907, Recall=0.6895; confusion matrix plotted (`confusion_matrix.png`)
- [ ] If regression variant: RMSE — not applicable, classification variant only (same as Sprint 1)
- [x] Plot: ROC curve, feature importance bar chart, confusion matrix heatmap — all three saved to `system/evaluation/outputs/` (`roc_curve.png`, `feature_importance.png`, `confusion_matrix.png`)
- [ ] Target: F1 > 0.75, ROC-AUC > 0.80 — **NOT MET**, consistent with Sprint 1's deferred gap (§1.6). This re-confirms the existing model's numbers with proper plots rather than closing the gap — the earlier decision to defer hyperparameter re-tuning (2026-08-10) still stands; write up F1=0.69/ROC-AUC=0.76 as the actual result in Chapter 6, not the unmet target.

### 6.2 System-Level Evaluation
*(Reference: SOT §19.1)*
- [x] Run 20 diverse video transcripts through full pipeline — `system/evaluation/system_eval.py`, reused the 10 Sprint 2/3 fixtures + 10 new ones covering every remaining `category_map.py` category (`system/evaluation/eval_video_inputs.py`); 20/20 ran with 0 errors through the real HTTP-equivalent pipeline (`graph.run_pipeline`)
- [x] Record for each run: pCTR score, VADER arousal, BERTScore, is_valid count, Self-BLEU — all recorded in `system/evaluation/outputs/system_eval_results.json` (`per_run`), Self-BLEU implemented in `system_eval.py::self_bleu` via NLTK
- [x] Compute averages across all runs — see `aggregate` in the same file
- [x] Latency measurement: P50 and P95 end-to-end response time — P50=7.38s, P95=9.95s (consistent with the Sprint 5 latency fix)
- [x] Target checks (SOT §19.1's actual targets, which are more granular than this line's summary — acceptance rate > 60%, pCTR avg > 6%, VADER arousal avg > 0.4, BERTScore avg 0.35–0.60, Self-BLEU < 0.4, latency P95 < 10s):
  - Acceptance rate = 0.94 — **MET**
  - Avg top pCTR = 0.685 — **MET**
  - Avg Self-BLEU = 0.054 — **MET** (titles are highly diverse within a batch)
  - Latency P95 = 9.95s — **MET** (barely; see Sprint 5 latency work)
  - Avg VADER arousal = 0.265 — **NOT MET** (target > 0.4). Many candidates score `vader_compound = 0.0` — titles lean on curiosity/numeric framing (T1/T7) rather than emotionally-loaded lexicon VADER can detect, even when successfully evocative.
  - Avg BERTScore = 0.872 — **NOT MET** (target range 0.35–0.60, meaning too high, not too low). Critic's own comment (§4.3) already predicted this: `bert_similarity > 0.60` flags "potentially boring/descriptive." Titles track `core_promise` very closely — a plausible side effect of the anti-hallucination grounding constraint being effective at faithfulness but conservative on creative divergence. Worth writing up as a real design tension (faithfulness vs. marketing punch) in Chapter 6, not silently patched.
  - Bar chart comparing all 6 metrics against targets: `system/evaluation/outputs/system_eval_bar_chart.png` (`system/evaluation/plot_system_eval.py`)

### 6.3 Human Evaluation Survey
*(Reference: SOT §19.3)*
**Cannot be fully automated: n=50+ real participants are required, and no response data may ever be fabricated for a thesis.** Built all the tooling so this is a fast manual step once you're ready to distribute it, rather than doing the data collection itself.
- [x] Prepare 10 video descriptions as test stimuli (mix of Education, Tech, Entertainment) — `system/evaluation/human_eval_stimulus.py`, selects 10 of the 20 System-2 eval videos (spans the categories, not narrowed to just Education/Tech/Entertainment — the fuller diversity from 6.2 carries over). Script run 2026-08-13, output saved to `system/evaluation/outputs/human_eval_stimulus.csv` + `human_eval_answer_key.csv`.
- [x] For each: generate 3 title variants — Baseline A (descriptive), Baseline B (zero-shot GPT-4o), System Output (YTO top-ranked) — reuses `llm_judge_eval.py`'s output (6.4) rather than regenerating, avoiding duplicate LLM cost; `baseline_a_descriptive`/`baseline_b_zero_shot` in `system/evaluation/baselines.py`. Baseline A deviation documented: SOT specifies "ground truth from video," but these are synthetic transcripts with no real underlying video — `video_description` used as a documented stand-in.
- [x] Blinding: `human_eval_stimulus.py` independently shuffles the 3 conditions' on-screen order per video (`title_1`/`title_2`/`title_3`) and writes a separate, participant-invisible `human_eval_answer_key.csv` mapping label → real condition
- [x] **Deviation (2026-08-13, time constraint):** full n=50+ / 10-video study descoped to a **3-video, n=15–20 pilot study** — 120 rating questions (10 videos × 3 titles × 4 dims) was judged too long for realistic participant completion; even the first-pass 5-video cut (60 questions) was judged still too long. Further trimmed to 3 videos × 3 titles × 4 dims = 36 rating questions (~8-10 min). Videos selected for category diversity (Science & Technology, People & Blogs, Education), keeping their original `video_id`s (1, 3, 6) unchanged so responses still join cleanly against `human_eval_answer_key.csv`. Google Form content fully drafted and ready to paste in: `system/evaluation/outputs/human_eval_survey_questions.md`. To be reported in Ch6/§20 as a limited-sample pilot, not the full SOT-spec study — SOT §19.3 not updated to reflect this yet, should be before Ch6 is written.
- [x] Distribute blinded survey to n=15–20 participants (creators, marketing students, general users; reduced from n=50+, see deviation above) — **done 2026-09-04**: Google Form distributed, **n=29 real responses** collected (exceeds the n=15–20 pilot target), exported to `research/YouTube Title Preference Study .csv/YouTube Title Preference Study .csv`
- [x] 4-dimension rubric per title: Curiosity, Emotional Impact, Clarity, Trustworthiness (1–5) — columns pre-built into the stimulus CSV, question wording finalized in `human_eval_survey_questions.md`, ready for the survey tool
- [x] Compute mean scores per condition per dimension — **done 2026-09-10**. Wide Google Forms export reshaped to the script's expected long format (`participant_id, video_id, blinded_label, dimension, rating`) via new `system/evaluation/reshape_human_eval_responses.py` (1041 long rows, 3 blank cells skipped), then `human_eval_analysis.py` run on the reshaped file → `system/evaluation/outputs/human_eval_results.json`. Means (n=29): System leads on curiosity (3.52) and emotional impact (3.59) vs. Baseline A (3.47/3.53) and Baseline B (3.39/3.37); Baseline A leads clarity (3.71 vs. System 3.55); trustworthiness ties System/Baseline A (3.51).
- [x] Run Wilcoxon signed-rank test or t-test to check statistical significance — same script, run 2026-09-10. **No comparison reaches significance at α=0.05** (all p > 0.1, most p > 0.3) — expected at this pilot sample size (n=29, ~86–87 paired ratings per dimension), reported honestly in Ch6 §6.6 rather than overstated. Also computes Pearson r between human "curiosity" ratings and the LLM judge's curiosity scores (6.4) as the inter-rater reliability check SOT §19.4 asks for: r = −0.14, p = 0.72, n=9 (video, condition) pairs — weak, non-significant, written up as a genuine limitation in §6.6/§6.7.

### 6.4 LLM-as-a-Judge Evaluation
*(Reference: SOT §19.4)*
- [x] Design judge prompt (GPT-4o as evaluator): Curiosity / Urgency / Relevance rubric (1–5 per dimension) — `system/evaluation/judge.py`, matches SOT §19.4's prompt structure exactly, temperature=0.0 for deterministic scoring
- [x] Run judge on all 20 demonstration outputs × 3 conditions = 60 evaluations — `system/evaluation/llm_judge_eval.py`, run 2026-08-13, 60/60 completed with 0 errors, results saved to `system/evaluation/outputs/llm_judge_results.json`. Mean scores: Baseline A (descriptive) = 3.30 overall, Baseline B (zero-shot GPT-4o) = 3.85 overall, System = 3.95 overall (curiosity 4.00, urgency 2.95, relevance 4.55). Wilcoxon signed-rank: System significantly beats Baseline A on curiosity/urgency/overall (p<0.002); vs. Baseline B, System wins significantly on relevance only (p=0.0047) — curiosity/urgency/overall gaps not significant at n=20 (p≈0.16–0.32), worth writing up honestly in Ch6 rather than overstated.
- [x] Compute inter-rater reliability between LLM judge scores and human survey scores (Cohen's Kappa or Pearson r) — **done 2026-09-10**; `human_eval_analysis.py` computed Pearson r on the curiosity dimension: r = −0.14, p = 0.72, n=9 (video, condition) pairs
- [x] Document reliability and discuss limitations — weak, non-significant correlation reported and discussed honestly as a limitation in Ch6 §6.6/§6.7 (small n=9 pairing, single-dimension comparison, no claim of strong LLM-human agreement made)

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
