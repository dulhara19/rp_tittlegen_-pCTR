# Chapter 2: Literature Review

---

## 2.1 Chapter Overview

This chapter situates the YouTube Title Optimizer (YTO) within the existing body of academic and applied knowledge across three intersecting domains: user engagement psychology, generative AI and prompt engineering, and NLP evaluation methods. It additionally surveys the landscape of existing systems — both tools and research prototypes — that address some subset of the problem, and identifies through systematic comparison the multi-dimensional gap that this research fills.

The review is organised according to a coverage structure prescribed by the project template: a domain overview (approximately 10% of coverage) establishes the macro-context; an existing systems analysis (approximately 30%) critically examines and compares prior approaches; and a technological analysis (approximately 60%) provides an algorithmic, design, and workflow-level review of the techniques, architectures, and datasets on which the proposed system is built. The chapter closes with a reflection that traces the research gap back through the literature, providing a grounded justification for the research question stated in Chapter 1.

---

## 2.2 Conceptual Map of the Literature

The literature that informs this research spans four distinct knowledge domains. Table 2.1 maps the primary theoretical and technical pillars to the system components they inform, and to the research questions (RQ1–RQ4) they address.

**Table 2.1 — Conceptual Map of the Literature**

| Domain | Key Works | System Component | RQ Addressed |
|---|---|---|---|
| **Engagement Psychology** | Loewenstein (1994) [1], Golman & Loewenstein (2016) [2], Kahneman & Tversky (1979) [3], Cialdini (1984) [4], Berger & Milkman (2012) [5] | Psychological Trigger Taxonomy (T1–T7); Generator Agent prompt templates | RQ1, RQ3 |
| **YouTube Algorithm & CTR** | Covington et al. (2016) [6], Kawata et al. (2025) [7], Zhang et al. (2024) [8] | System motivation; pCTR target variable; dataset strategy | RQ3 |
| **Generative AI & Prompt Engineering** | Vaswani et al. (2017) [9], Brown et al. (2020) [10], Wei et al. (2022) [11], Yang (2024) [12] | Generator Agent; Prompt Factory; Few-Shot Prompt Database | RQ1, RQ2 |
| **NLP Evaluation Methods** | Hutto & Gilbert (2014) [13], Zhang et al. (2020) [14], Laban et al. (2023) [15], Aslam et al. (2021) [16] | Critic Agent; VADER, BERTScore, NLI, pCTR model | RQ2, RQ4 |
| **Research Methodology** | Peffers et al. (2007) [17] | DSR strategy; DSRM six-phase process | — |

The three columns — psychological theory, AI/NLP technology, and existing systems — represent the three pillars that must be integrated. No prior work has performed this integration in the specific combination that YTO proposes. That is the gap this chapter establishes.

---

## 2.3 Domain Overview

### 2.3.1 The Video-First Internet and the Creator Economy

The consumption of digital content has undergone a structural reorientation over the past decade. Where textual media — articles, blog posts, and web pages — once constituted the primary vehicle for online information exchange, video has emerged as the dominant format through which billions of people learn, decide, and discover. YouTube, processing over 500 hours of new video content every minute [19], represents the largest video repository in existence and the world's second-largest search engine by query volume. Alongside it, short-form platforms including TikTok and Instagram Reels have further accelerated the shift toward video as the default communication medium.

This transformation has given rise to a significant creator economy. Individual content creators, educators, journalists, and organisations now depend on video platforms as primary channels for audience reach, brand building, and monetisation. In this economy, the ability to generate video content is no longer the limiting factor — production costs have collapsed with the democratisation of recording hardware and editing software. The limiting factor is *discovery*: the ability to surface content to relevant audiences in an environment of extraordinary supply.

### 2.3.2 Click-Through Rate as the Algorithmic Gatekeeper

YouTube's recommendation system, as documented by Covington, Adams, and Sargin (2016) in the foundational paper *Deep Neural Networks for YouTube Recommendations* [6], operates as a two-stage pipeline. The candidate generation stage narrows billions of videos to hundreds of candidates for each user session. The ranking stage orders those candidates according to predicted user satisfaction signals, of which Click-Through Rate (CTR) — the proportion of users who click a video after seeing its impression — is among the most immediate and influential.

For newly uploaded videos, the system faces a cold-start problem: no historical engagement data exists, and the recommendation engine must rely on the earliest available signal to decide whether to expand distribution. That signal is the click decision made in milliseconds by a viewer who reads a title and sees a thumbnail. If CTR during the initial test cohort is insufficient, the algorithm contracts distribution regardless of the video's intrinsic quality. YouTube's own documentation confirms that half of all channels and videos have impressions CTRs between 2% and 10% [20], and industry benchmarks indicate that CTRs above 7% on the home feed represent a strong outcome associated with meaningful algorithmic amplification [21].

This dynamic creates a disproportionate influence for video titles relative to every other variable in content production. A well-crafted title that achieves a 7% CTR versus a poorly crafted title achieving 3% can produce dramatically different long-term distribution outcomes — not because the content differs, but because the metadata packaging does.

### 2.3.3 Historical Evolution: From Manual Copywriting to AI-Assisted Generation

The craft of writing compelling headlines predates the internet. In traditional print and broadcast media, professional copywriters applied empirically developed heuristics to generate click, read, or view responses. The psychological mechanisms these professionals exploited intuitively — curiosity gaps [1], urgency framing [4], social proof signals [4], emotional arousal [5] — were formalised in academic literature beginning in the 1970s and 1980s.

The digital era introduced new layers of optimisation. Search engine optimisation (SEO) research established rules for keyword placement and title length to maximise search ranking visibility. The rise of social media platforms shifted focus toward emotional triggers and shareability. YouTube-specific tools such as TubeBuddy and VidIQ emerged to provide creators with data on which titles performed historically, without providing generative capability. Most recently, the public availability of large language models (LLMs) beginning with GPT-3 (Brown et al., 2020 [10]) opened the possibility of AI-assisted title generation — though, as discussed in Section 2.4, the unstructured application of these models does not automatically produce high-quality results [12].

---

## 2.4 Existing Systems, Frameworks, and Designs

This section critically examines four categories of existing approaches to the title optimisation problem, followed by a comparative analysis and identification of the research gap.

### 2.4.1 System 1: Manual Expert Copywriting

**Description:** Professional copywriters with expertise in marketing psychology apply their knowledge of psychological triggers, platform-specific conventions, and audience psychology to craft titles manually. This represents the highest quality baseline in the existing landscape.

**Strengths:** Manual expert copywriting produces titles grounded in nuanced understanding of cultural context, brand voice, and audience psychology. An experienced practitioner can apply information gap theory [1], loss aversion framing [3], and social proof construction [4] intuitively, adjusting for niche, audience, and content type. The approach has been validated by the measurable performance of channels whose creators invest in this expertise — MrBeast's publicly documented title philosophy, for instance, explicitly prioritises emotional intensity, brevity, and comprehensibility over descriptive accuracy.

**Weaknesses:** The approach is characterised by three structural limitations. First, it is *unscalable*: at 500 hours of video uploaded per minute [19], no human workforce can apply expert-level review at the required throughput. Second, it is *inaccessible*: professional copywriting services are expensive, creating an economic barrier that disadvantages individual creators, non-profit educators, and small organisations. Third, it is *inconsistent*: even expert practitioners produce suboptimal titles under time pressure or outside their domain of familiarity.

**Reflection:** Manual expert copywriting establishes the quality ceiling that an automated system must aspire to approach. Its unscalability and inaccessibility are precisely the structural problems this research addresses. The question is whether systematic prompt engineering can transfer the heuristic knowledge of expert copywriters into an algorithmic pipeline that is accessible to any creator with a video transcript.

---

### 2.4.2 System 2: YouTube Analytics Platforms (TubeBuddy, VidIQ)

**Description:** Dedicated YouTube optimisation tools such as TubeBuddy and VidIQ provide creators with data dashboards offering historical CTR analysis, keyword suggestion engines, competitor benchmarking, trend identification, and tag recommendation features.

**Strengths:** These platforms offer genuine empirical value. Creators with access to historical performance data can identify which topics and formats have generated high CTR in their niche, and keyword tools can surface search demand signals that inform title structure. The platforms serve a large, active user base and are integrated into YouTube Studio workflows, lowering the barrier to data-informed decision-making.

**Weaknesses:** Both platforms are fundamentally *reactive and generative-free*. They show creators what has already happened — historical CTR trends, past keyword performance, competitor data — but they do not generate titles from video content. The creator remains responsible for synthesising analytical insights into a new title, which requires the same expert judgment that most creators lack. Neither platform operationalises psychological trigger theory, applies sentiment analysis, or enforces faithfulness constraints. They answer the question "what worked before?" without answering "what should I write now?"

**Reflection:** TubeBuddy and VidIQ are valuable data tools but do not address the generative component of the problem. Their existence confirms market demand for title optimisation assistance, but their purely analytical orientation leaves the synthesis gap — the jump from insight to actual title copy — entirely to the creator.

---

### 2.4.3 System 3: Generic LLM Prompting (Zero-Shot)

**Description:** The public availability of capable LLMs — including GPT-4o (OpenAI), Claude (Anthropic), and Llama 3 (Meta) — has made it possible for creators to prompt these models directly for title suggestions: "Write me a YouTube title for a video about cooking pasta."

**Strengths:** LLM-based title generation is highly scalable, requires no technical expertise from the user, is available at low or zero marginal cost, and can produce grammatically fluent, topically accurate suggestions within seconds.

**Weaknesses:** The evidence that zero-shot LLM prompting fails to match expert copywriting quality is well-documented. Yang (2024), in a study published in *PLOS ONE*, evaluated AI-assisted title generation on the RED social media platform and found that standard machine-generated titles "lack the emotional sophistication and cultural proficiency" that human experts apply, producing output that is accurate but psychologically flat [12]. The study, which tested the "POP Title AI Five-Step Optimization Method," found that human refinement of AI-generated drafts was necessary to achieve performance gains.

More directly, Zhang et al. (2024), in a large-scale randomised field experiment involving over two million content producers, found that when videos already had human-generated titles, replacing them with pure AI-generated alternatives *decreased* valid watch counts by 37.9% — a finding that strongly suggests naive AI generation falls below the quality threshold that experienced human creators achieve [8].

The root cause of this limitation is architectural: a zero-shot prompt provides the model with no psychological framework, no niche-specific exemplars, no trigger operationalisation, and no quality evaluation mechanism. The model generates based on its training distribution, which produces descriptive competence but not engagement engineering.

**Reflection:** Generic LLM prompting does not solve the problem — it reframes it. The question is no longer whether LLMs *can* generate titles, but whether they can be *systematically directed* to generate titles that operationalise psychological trigger theory, are constrained against hallucination, and are ranked by a predicted virality metric. This is precisely the contribution of the proposed system.

---

### 2.4.4 System 4: Clickbait Detection Systems

**Description:** A substantial body of academic research addresses the detection and classification of clickbait. The Webis Clickbait Corpus (Potthast et al., 2016) provides annotated datasets for training detection models. SemEval shared tasks have produced multiple high-performing NLP classifiers. Research published in 2021 demonstrated the application of multi-modal ML to detect clickbait specifically in YouTube videos using title, description, and thumbnail features [22].

**Strengths:** Clickbait detection research has produced robust, well-validated NLP methods, rich annotated datasets, and a clear theoretical framing of what constitutes deceptive metadata. The NLI-based approach to hallucination detection that has emerged from summarisation faithfulness research (Laban et al., 2023 [15]) traces its lineage directly to this body of work.

**Weaknesses:** Detection systems solve the inverse of the generative problem. They identify what bad titles look like without providing a pathway to what good titles look like. They are binary (clickbait / not clickbait) or multi-class (degree of clickbait), but they do not generate alternatives, do not score engagement potential, and do not assist creators in producing improved metadata. They are diagnostic instruments without therapeutic capability.

**Reflection:** The clickbait detection literature is directly useful to this project as the source of negative examples (the Webis Clickbait Corpus serves as negative training data for the pCTR model's validation layer), and as the origin of the NLI faithfulness methodology adopted in the Critic Agent. However, the detection systems themselves do not occupy the generative space that YTO targets.

---

### 2.4.5 Comparative Summary

**Table 2.2 — Comparative Analysis of Existing Approaches**

| Criterion | Manual Copywriting | Analytics Platforms | Generic LLM | Clickbait Detection | **YTO (Proposed)** |
|---|:---:|:---:|:---:|:---:|:---:|
| Proactive (auto-generates from content) | ✗ | ✗ | Partial | ✗ | **✓** |
| Psychologically grounded (trigger theory) | ✓ | ✗ | ✗ | Partial | **✓** |
| Generative capability | ✓ | ✗ | ✓ | ✗ | **✓** |
| Faithfulness / deception enforcement | ✓ (human) | N/A | ✗ | ✓ (detect only) | **✓** |
| Scalable | ✗ | ✓ | ✓ | ✓ | **✓** |
| Virality scoring (pCTR) | ✗ | Partial | ✗ | ✗ | **✓** |
| Accessible (no expertise required) | ✗ | Partial | ✓ | ✓ | **✓** |

The comparative analysis reveals a consistent pattern: each existing approach satisfies some criteria while failing others. No existing system simultaneously provides proactive, psychologically-grounded, generative, and faithfulness-enforced title optimisation at scale. This intersection is the research gap that YTO addresses.

---

## 2.5 Technological Analysis

### 2.5.1 Algorithmic Analysis

#### A1: Large Language Models — The Transformer Architecture

The architectural foundation of all major LLMs is the Transformer, introduced by Vaswani et al. (2017) in *Attention Is All You Need* [9]. The Transformer replaced recurrent architectures (RNN, LSTM) with a self-attention mechanism that computes relationships between all tokens in a sequence simultaneously, enabling parallel training and capturing long-range dependencies that sequential models could not efficiently model. This architecture underpins every model considered for use in YTO — GPT-4o, Llama 3, and the encoder-based models (BERT, RoBERTa) used in the evaluation layer.

GPT-4o (OpenAI, 2024) is selected as the primary generation model on the basis of its state-of-the-art instruction-following capability, native support for structured JSON output (critical for agent pipelines where downstream components consume structured data), and strong performance on creative generation tasks with constraint satisfaction requirements [23]. It supports fine-tuning, offers a native function-calling interface, and provides a documented pricing structure that enables cost modelling within the research prototype scope.

Llama 3 (Meta AI, 2024) is included as the open-source alternative. Its deployability on local hardware without per-token API costs makes it attractive for production deployment scenarios, and its support for fine-tuning on domain-specific data (high-CTR YouTube titles) positions it as the preferred model for the planned Phase 2 fine-tuning extension. The existence of a capable open-source alternative also mitigates vendor lock-in risk.

The core limitation of raw LLMs for title generation is that their output distribution reflects their training data — broad, general-purpose text — rather than the narrow, psychologically engineered register of high-performing YouTube titles. Bridging this gap is the function of the prompt engineering techniques reviewed in A2.

#### A2: Prompt Engineering Techniques

**Few-Shot Prompting.** Introduced by Brown et al. (2020) in *Language Models are Few-Shot Learners* [10], few-shot prompting involves providing a small number of curated input-output examples (typically 3–8) within the prompt context to steer the model's output toward the desired format, register, and quality standard. Crucially, this technique requires *no updates to model weights* — the steering occurs entirely through the context window. Brown et al. demonstrated that scaled LLMs can approach fine-tuned model performance on many NLP benchmarks using only a handful of in-context examples, establishing in-context learning as a first-class capability distinct from gradient-based fine-tuning.

In the YTO Generator Agent, few-shot prompting is implemented through a dynamic Prompt Database: high-performing YouTube titles are embedded as vectors and stored in a vector store. At generation time, the video brief is embedded and a nearest-neighbour similarity search retrieves the 3–5 topically closest high-performing titles in the same content niche. These titles are injected into the Generator's prompt as examples, anchoring the model's output to the specific linguistic register, emotional register, and trigger structure that has historically performed well in that niche. This niche-specific retrieval is critical: a cooking video should receive cooking-niche exemplars, not the extreme-challenge format titles that characterise MrBeast's channel.

**Chain-of-Thought (CoT) Reasoning.** Wei et al. (2022), in *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* [11], demonstrated that instructing LLMs to articulate intermediate reasoning steps before producing a final answer significantly improves performance on complex multi-step tasks. The technique causes the model to decompose the problem into explicit sub-problems — identifying the core tension, selecting the optimal emotional framing, drafting candidates, refining for constraint satisfaction — rather than mapping input directly to output in a single step.

In the YTO Generator Agent, a four-step CoT sequence is applied: (1) identify the core information gap or conflict in the video brief; (2) determine the optimal high-arousal emotional angle authentically supported by the content; (3) draft 10 candidate titles across different psychological triggers; (4) refine the three strongest candidates for brevity, mobile display constraints, and the target character count. This decomposition prevents the Generator from short-circuiting to a generic answer and enforces deliberate trigger-type selection.

**Persona Pattern.** Assigning the LLM an expert role prior to the generation task — "You are a viral YouTube title copywriter with 10+ years of experience optimising CTR for top creators" — has been demonstrated to shift the model's prior toward domain-specific vocabulary, heuristics, and tone, producing outputs that more closely resemble professional practitioner work than instruction-following alone. White et al. (2023) systematised this and related techniques in the Prompt Pattern Catalog, establishing the Persona Pattern as a reproducible prompting strategy that modifies the LLM's assumed role and therefore its output distribution [34]. The persona pattern is applied in the Generator Agent's system prompt and functions as a baseline distributional alignment before few-shot examples and CoT instructions are applied.

**Dynamic Prompt Database via Vector Retrieval.** The integration of semantic vector search with few-shot prompting enables context-aware example selection at runtime. The Prompt Database indexes high-performing titles as dense vector embeddings using Sentence-Transformers. At generation time, the incoming video brief is embedded in the same semantic space, and a nearest-neighbour search retrieves the most topically relevant examples. A content category filter (Education, Entertainment, Technology) is applied to further constrain retrieval to niche-appropriate exemplars. This architecture ensures that the few-shot context is always maximally relevant to the current generation task — a significant improvement over static, hardcoded example sets.

#### A3: Sentiment Analysis — VADER

Hutto and Gilbert (2014) introduced VADER (Valence Aware Dictionary and sEntiment Reasoner) in *A Parsimonious Rule-Based Model for Sentiment Analysis of Social Media Text* [13], published at the AAAI International Conference on Weblogs and Social Media (ICWSM). The model was designed specifically for the characteristics of short, informal social media text — the precise domain of YouTube titles.

VADER combines a manually curated sentiment lexicon (approximately 7,500 items) with five heuristic rules that capture linguistic features distinctive to informal digital text: capitalisation effects ("GREAT" > "great"), punctuation intensity ("great!!!" > "great"), negation handling, degree modifiers, and contrastive conjunction effects. It returns four scores: positive, negative, neutral (normalised proportions summing to 1.0) and compound (a single normalised summary score ranging from −1 to +1). VADER was benchmarked against eleven standard methods including LIWC, ANEW, SentiWordNet, and a Human Rater baseline, outperforming all on social media corpora.

In the YTO Critic Agent, the absolute value of the compound score (|compound|) is used as a proxy for *emotional arousal magnitude*, independent of valence direction. This decision is grounded in Berger and Milkman's (2012) finding [5] that arousal — not valence — is the primary driver of viral spread: high-arousal positive content (awe, excitement) and high-arousal negative content (anger, anxiety) both outperform low-arousal content regardless of whether they are positive or negative. A target of |compound| > 0.5 is applied, penalising emotionally flat titles that may be descriptively accurate but psychologically inert.

A key limitation of VADER is that it does not model arousal *type*: a title evoking awe and a title evoking anxiety may receive identical compound scores despite their different psychological mechanisms and viral performance profiles. Berger and Milkman (2012) identified awe as the single highest-performing emotional trigger for viral spread and anger as the second-highest [5]. VADER cannot distinguish between these — it measures intensity, not category. This limitation is acknowledged and documented in Section 2.5.3 (Workflow Analysis — Evaluation) and in Chapter 7 (Limitations) as a direction for future work via a fine-tuned arousal classifier.

#### A4: Semantic Faithfulness — BERTScore

Zhang et al. (2020) introduced BERTScore in *BERTScore: Evaluating Text Generation with BERT* [14], published at ICLR 2020. Unlike traditional text similarity metrics such as BLEU or ROUGE, which compute n-gram overlap between candidate and reference texts, BERTScore computes token-level similarity using contextual BERT embeddings. For each token in the candidate text, BERTScore finds the maximum cosine similarity against all tokens in the reference text, aggregating these scores into precision, recall, and F1 measures. The result is a metric that captures semantic similarity across paraphrase and stylistic variation — a property that n-gram metrics cannot provide and that is essential when the candidate (a creative title) is stylistically very different from the reference (a factual video summary).

Zhang et al. demonstrated that BERTScore correlates more strongly with human quality judgements than BLEU, METEOR, and TER across 363 machine translation and image captioning systems.

In the YTO Critic Agent, BERTScore (specifically, the F1 score between the generated title and the video summary extracted by the Analyzer Agent) is used as a **semantic relevance filter**. A BERTScore below 0.30 indicates that the title is likely off-topic — semantically distant from the content the video actually delivers — and is flagged for rejection or manual review. Scores in the range 0.30–0.60 represent the expected zone for creative, psychologically optimised titles that are related to but not verbatim repetitions of the content. Scores above 0.60 indicate that the title is so closely paraphrastic of the summary that it is likely to be descriptively accurate but psychologically flat.

It is critical to note that BERTScore measures semantic *distance*, not factual *consistency*. A title can be semantically similar to a video summary while still making a factual claim that contradicts the content. This is why BERTScore is used as Layer 1 (relevance filter) rather than as the faithfulness gate, which is handled by the NLI model in Layer 2.

#### A5: Natural Language Inference for Faithfulness Verification

Natural Language Inference (NLI) is the task of classifying the logical relationship between two texts — a *premise* and a *hypothesis* — as one of three categories: *Entailment* (the premise logically implies the hypothesis), *Neutral* (the premise is consistent with but does not entail the hypothesis), or *Contradiction* (the premise is inconsistent with or negates the hypothesis).

The application of NLI models to faithfulness evaluation in text generation tasks has been validated by Laban et al. (2023) in *With a Little Push, NLI Models can Robustly and Efficiently Predict Faithfulness* [15], published at ACL 2023. Laban et al. demonstrated that NLI-based faithfulness scoring correlates more strongly with human faithfulness judgements than token-overlap metrics and, with appropriate calibration, can robustly identify generated text that contradicts source documents.

In the YTO Critic Agent, the NLI model is deployed with the generated title as the *premise* and the core promise extracted by the Analyzer Agent as the *hypothesis*. A "Contradiction" classification results in hard rejection of the title — it is eliminated from the output and added to the rejection log regardless of its predicted CTR score or VADER arousal magnitude. "Entailment" and "Neutral" classifications allow the title to proceed to composite scoring. Two candidate models are specified: `facebook/bart-large-mnli` and `roberta-large-mnli`, both available on Hugging Face, with the former preferred due to its encoder-decoder architecture's demonstrated strength on inference tasks.

This two-layer approach (BERTScore + NLI) is deliberately complementary. BERTScore filters off-topic titles efficiently before they consume expensive NLI inference calls. NLI provides the definitive factual consistency check that BERTScore cannot perform.

#### A6: Predicted CTR (pCTR) — Machine Learning Model

The prediction of video virality from title and metadata features using machine learning has been demonstrated as a viable approach in multiple prior studies. Aslam et al. (2021) achieved 86% accuracy classifying popular versus unpopular YouTube videos using XGBoost on features combining title characteristics, engagement metadata, and content category [16]. Paskalev (n.d.) reported an RMSE of 3.48% on YouTube CTR prediction using a Random Forest model trained on title and metadata features [24]. Merrell (n.d.) replicated this approach with XGBoost on approximately 2,000 videos, using the *views per subscriber* normalisation to isolate title quality from channel authority — the same normalisation strategy adopted as the pCTR target variable in YTO [25].

Both Random Forest and XGBoost are selected over deep learning approaches on principled grounds. The available dataset size (tens of thousands of labelled examples) does not justify the data requirements of deep sequence models. The features are tabular — engineered numerics and encoded categorical variables — rather than raw sequences, making tree-based ensemble methods the natural fit. Critically, both methods provide *feature importance* scores, enabling the system to explain which title characteristics most strongly predict virality — a research requirement for interpretability and for validating the psychological trigger taxonomy.

The pCTR model is trained on the subscriber-normalised virality score (Views / Subscriber_Count at upload time) computed from the Kaggle YouTube Trending Dataset [26] and the Kaggle Classic YouTube Statistics Dataset [27], supplemented by targeted scraping of high-performing channels via the YouTube Data API v3. This normalisation is essential: a title on a 10-million subscriber channel receives views from passive subscriber consumption regardless of title quality, masking the title's independent contribution to discovery. Normalisation by subscriber count isolates the discovery component.

---

### 2.5.2 Design Analysis

#### D1: Multi-Agent Architecture — Supervisor Pattern

Multi-agent systems decompose complex tasks into specialised agents, each with a focused role and isolated context, coordinated by a supervisory controller. LangGraph, the stateful graph-based extension to LangChain, implements this pattern through a directed graph of agent nodes with explicit state transitions, enabling deterministic control flow between agents alongside the flexibility of LLM-based reasoning within each node [28].

The Supervisor pattern — in which a controller agent receives input, delegates sequentially to specialised workers, and receives structured outputs from each — is the architectural pattern adopted for YTO. This pattern is preferred over the Network pattern (any agent can call any other) because the YTO pipeline has a strict sequential dependency: the Analyzer must complete before the Generator can proceed, and the Generator must complete before the Critic can evaluate. The sequential constraint is a design choice, not a technical limitation, and is motivated by the anti-hallucination architecture described in D2.

#### D2: API Wrapper with Facade Pattern

The system is implemented as an **API Wrapper using the Facade design pattern**. The Facade pattern (Gamma et al., 1994 [35]) provides a simplified interface to a complex subsystem, hiding its internal structure from external clients. In YTO, the Facade is a FastAPI REST endpoint that accepts a simple HTTP POST request (containing the video transcript and optional metadata) and returns a ranked list of scored title candidates. All internal complexity — agent orchestration, prompt construction, vector retrieval, ML inference, NLP evaluation — is invisible to the consuming application.

FastAPI is selected as the backend framework on the basis of its ASGI (Asynchronous Server Gateway Interface) architecture, which provides native async/await support for I/O-bound LLM API calls. This is a significant practical consideration: LLM inference calls are high-latency I/O operations (typically 1–5 seconds per call), and synchronous handling would block a process for each active request. ASGI-based handling allows a single FastAPI process to manage hundreds of concurrent requests efficiently, with each request awaiting its LLM response without blocking others. The framework additionally provides automatic Pydantic-based request validation — critical for structured agent I/O — and native streaming response support for real-time token output.

#### D3: Psychological Trigger Operationalisation

The core technical novelty of the Generator Agent is not the LLM it uses but the prompt infrastructure through which psychological theory is translated into algorithmic instructions. Each psychological trigger in the T1–T7 taxonomy maps to a set of explicit linguistic markers that the Generator is instructed to employ:

**Table 2.3 — Psychological Trigger Taxonomy and Linguistic Operationalisation**

| Trigger | Theoretical Basis | Linguistic Markers | Example |
|---|---|---|---|
| T1: Curiosity Gap | Loewenstein (1994) [1], Golman & Loewenstein (2016) [2] | "Why I...", "The Real Reason...", "What Happens When..." | "Why I Quit My Job After Discovering This" |
| T2: Loss Aversion / FOMO | Kahneman & Tversky (1979) [3] | "Don't Make This Mistake", "Before You Buy...", "You're Doing X Wrong" | "Stop Wasting Money on This (I Did For 3 Years)" |
| T3: Social Proof / Authority | Cialdini (1984) [4] | "Expert Says...", "10,000 People Tried This", "What Scientists Found", numbered lists | "I Asked 50 Experts What They'd Do With $1,000" |
| T4: Urgency / Scarcity | Cialdini (1984) [4] | "Before It's Too Late", "This Changes Everything", "Last Chance" | "Watch This Before YouTube Changes Everything" |
| T5: Extreme / Superlative | Berger & Milkman (2012) [5] | "The Worst", "Impossible", "Never Seen Before", "Most Expensive" | "I Tried the World's Most Expensive Pizza" |
| T6: Personal Stakes / Vulnerability | Parasocial Relationship Theory (Horton & Wohl, 1956) [32] | "I Lost...", "I Failed...", "My Biggest Mistake", "I Quit..." | "I Quit My $200K Job to Do This" |
| T7: Number + Specificity | Cognitive Ease (Kahneman, 2011 [33]); Specificity implies credibility | Exact numbers, percentages, timeframes | "This $11 Meal Changed How I Cook Forever" |

This operationalisation is a primary research contribution. As noted in the gap analysis in Section 2.4.5, no existing generative system encodes psychological trigger theory as explicit prompt engineering instructions. The trigger taxonomy bridges a documented gap between the academic literature on persuasion psychology and the practical implementation of LLM-based content generation.

The relationship between specificity and credibility (T7) is particularly notable. Kawata et al. (2025), in a study of 12,466 Microsoft Excel YouTube tutorial videos, found a bell-shaped relationship between title length/word count and view counts, with a performance peak at 7–12 words and 60–70 characters [7]. This empirical finding provides the length constraint that the Generator Agent enforces as a hard output requirement.

---

### 2.5.3 Workflow Analysis

#### W1: Dataset Pipeline

The pCTR model's training pipeline draws on four primary data sources:

**Kaggle YouTube Trending Dataset (rsrishav)** [26]: Daily snapshots of US trending videos, including title, view count, like count, comment count, category, and channel metadata. This dataset provides the primary source of viral linguistic patterns and the raw material for the subscriber-normalised virality score target variable. Its principal limitation is that trending status reflects accumulation over time rather than early CTR — it is used as a proxy for viral linguistic patterns rather than as a direct CTR dataset.

**Kaggle YouTube Trending Statistics (datasnaek)** [27]: A historical dataset of 29,089 unique videos across US, UK, Canadian, and Indian trending data, widely used in academic ML research on YouTube virality. This dataset provides cross-national variation and a larger historical baseline.

**YouTube Data API v3 (targeted scraping)**: Directed collection from demonstrably high-performing channels (MrBeast, Veritasium, Mark Rober, Kurzgesagt) provides gold-standard positive examples from channels where title engineering is known to be deliberate and effective. This targeted scraping supplements the trending datasets with examples where title quality can be more confidently attributed to intentional design rather than channel authority alone.

**Webis Clickbait Corpus** [29]: Annotated clickbait titles from academic detection research provide the negative example set — titles characterised by deceptive or misleading metadata — used to train the NLI validation layer's rejection boundary.

Data cleaning requirements include: deduplication of trending entries (each video appears multiple times in the trending dataset as it trends over multiple days); subscriber count normalisation to the upload date rather than current count; removal of non-English titles; removal of titles that are purely SEO keyword strings without natural language structure; emoji preservation and proper tokenisation (Chen, 2023 [18] found emoji carry significant sentiment and virality signals); and toxicity filtering via `unitary/toxic-bert` to prevent the Prompt Database from including examples that optimise for harmful engagement patterns.

#### W2: Evaluation Workflow

The evaluation methodology operates across three levels:

**Offline ML Evaluation:** The pCTR model is trained on a 70/15/15 train/validation/test split, with the test set held out until final evaluation to prevent data leakage. Primary metric: F1-score (chosen to account for class imbalance in the binary classification variant). Secondary metrics: ROC-AUC and RMSE for the regression variant. Target: F1 > 0.75, ROC-AUC > 0.80.

**System-Level Evaluation:** The end-to-end pipeline is evaluated on a demonstration dataset of 10+ diverse video topics across three content categories (Education, Entertainment, Technology). Six metrics are recorded for each run: pCTR score (target mean > 0.06), VADER arousal magnitude (target mean |compound| > 0.40), BERTScore F1 (target range 0.35–0.60), Self-BLEU (target < 0.40, indicating inter-title diversity within each batch), NLI acceptance rate (target > 60%), and P95 end-to-end latency (target < 10 seconds).

Self-BLEU warrants particular explanation. Originally introduced by Zhu et al. (2018) in the Texygen benchmarking platform for text generation [36], Self-BLEU computes the BLEU score between each generated title and the other titles in the same batch. A high Self-BLEU score indicates that the generated titles are minor paraphrases of a single pattern — that the Generator has collapsed to a single trigger type despite instructions to produce diverse variants. A low Self-BLEU score confirms that the five candidates represent genuinely distinct psychological framings.

**Human Evaluation:** A preference survey with a minimum of 50 participants evaluates generated titles on a four-dimension rubric (1–5 Likert scale): Curiosity (information gap created), Emotional Impact (arousal strength), Clarity (topic comprehensibility), and Trustworthiness (perceived honesty). Each participant evaluates three title variants for the same video: Baseline A (the original human-generated title), Baseline B (a zero-shot LLM title), and System Output (YTO's top-ranked candidate). The primary hypothesis is that YTO significantly outperforms both baselines on Curiosity and Emotional Impact while maintaining comparable Clarity and Trustworthiness scores.

**LLM-as-a-Judge Evaluation:** A secondary automated evaluation method — directly addressing RQ4 — uses GPT-4o as a rubric-based evaluator to score generated titles on three dimensions (Curiosity, Urgency, Relevance) via a structured prompt. This approach, supported by the LLM-RUBRIC framework (ACL 2024) which demonstrated that calibrated LLM judges combining multiple rubric dimensions can achieve reliable correlation with human raters [30], scales to large title sets without the cost of human annotation. All LLM-as-a-Judge scores are cross-validated against the human evaluation scores on the overlapping subset to assess their reliability.

---

## 2.6 Reflection — Research Gap Justification

The systematic review conducted in this chapter converges on a consistent finding: the research gap that motivates YTO is real, multi-dimensional, and not addressed by any single prior work or commercial tool.

**From the psychological theory literature**, the mechanisms by which titles generate clicks are well-documented. Loewenstein's Information Gap Theory [1], Kahneman and Tversky's Prospect Theory [3], Cialdini's Social Proof framework [4], and Berger and Milkman's emotional arousal research [5] collectively provide a rigorous theoretical basis for what makes a title effective. However, these theories are documented in the literature as descriptive accounts of human behaviour — they are not implemented as algorithmic instructions in any generative AI system. The operationalisation of psychological theory as explicit LLM prompt engineering is the first dimension of the gap.

**From the existing systems analysis**, each prior approach addresses at most two or three of the five criteria identified in Table 2.2. Manual copywriting achieves psychological grounding and generative quality but fails on scalability. Analytics platforms achieve scalability and data richness but have no generative capability. Generic LLM prompting achieves scalability but fails on psychological grounding and faithfulness enforcement. Clickbait detection achieves faithfulness checking but has no generative pathway. The five-way intersection — proactive, psychologically grounded, generative, faithfulness-enforced, and scalable — is unoccupied. That is the second dimension of the gap.

**From the technological analysis**, the component-level evidence confirms that the individual technologies required to close these gaps exist and have been individually validated. LLMs can generate creative text with constraint satisfaction (Brown et al., 2020 [10]; Wei et al., 2022 [11]). VADER can measure emotional arousal in short text (Hutto & Gilbert, 2014 [13]). BERTScore can measure semantic relevance (Zhang et al., 2020 [14]). NLI models can detect factual contradiction between generated and source text (Laban et al., 2023 [15]). Tree-based ML can predict video virality from title features (Aslam et al., 2021 [16]). Multi-agent architectures can coordinate specialised LLM pipelines (LangChain/LangGraph, 2024 [28]). The gap is not a component-level gap — it is an *integration and operationalisation* gap. No prior work has combined these components into a coherent system designed specifically to engineer psychologically optimised, faithfulness-verified, virality-ranked YouTube titles.

**From the empirical literature**, the most recent evidence further validates both the problem and the direction. Zhang et al. (2024) demonstrated in a 2-million-user field experiment that AI-generated metadata significantly boosts content consumption when human-AI co-creation is applied, but pure AI generation *underperforms* existing human-written titles [8]. Yang (2024) confirmed that generic AI title generation lacks the emotional sophistication of expert human copywriting [12]. Both findings point to the same conclusion: the research need is not for more AI generation, but for *more intelligently engineered* AI generation — precisely the contribution of this project.

---

## 2.7 Chapter Summary

This chapter has reviewed the literature across the domains of engagement psychology, generative AI and prompt engineering, NLP evaluation, ML-based virality prediction, and existing tools and systems. The domain overview established that CTR-driven algorithmic discovery creates a structural problem in which video metadata quality — and title quality specifically — exerts disproportionate influence over content visibility. The existing systems analysis demonstrated that manual copywriting, analytics platforms, generic LLM prompting, and clickbait detection each satisfy some requirements of an ideal solution while failing others, with no system occupying the intersection of all five. The technological analysis confirmed that the required component technologies have each been individually validated in the literature, and that the integration gap — the absence of a system that combines them under a psychologically grounded, ethically constrained generative architecture — is the specific contribution of this research.

Chapter 3 presents the research methodology, establishing the philosophical and strategic framework — Design Science Research under a Pragmatist paradigm — that governs how the system will be built and evaluated, and mapping the DSRM six-phase process to the specific activities of this project.

---

## References

[1] G. Loewenstein, "The psychology of curiosity: A review and reinterpretation," *Psychological Bulletin*, vol. 116, no. 1, pp. 75–98, 1994. DOI: 10.1037/0033-2909.116.1.75

[2] R. Golman and G. Loewenstein, "Information Gaps: A Theory of Preferences Regarding the Presence and Absence of Information," *Decision*, 2016. DOI: 10.1037/dec0000068

[3] D. Kahneman and A. Tversky, "Prospect Theory: An Analysis of Decision under Risk," *Econometrica*, vol. 47, no. 2, pp. 263–291, 1979. DOI: 10.2307/1914185

[4] R. B. Cialdini, *Influence: The Psychology of Persuasion.* New York: Harper & Row, 1984.

[5] J. Berger and K. L. Milkman, "What Makes Online Content Viral?" *Journal of Marketing Research*, vol. 49, no. 2, pp. 192–205, 2012. DOI: 10.1509/jmr.10.0353

[6] P. Covington, J. Adams, and E. Sargin, "Deep Neural Networks for YouTube Recommendations," in *Proc. 10th ACM Conf. Recommender Systems (RecSys '16)*, pp. 191–198, 2016. DOI: 10.1145/2959100.2959190

[7] T. Kawata, T. Kato, and K. Tsuda, "Effect of Title Length and Word Count on Views: Evidence from Microsoft Excel Videos on YouTube," *EAI Endorsed Trans. Scalable Information Systems*, vol. 12, no. 1, 2025. DOI: 10.4108/eetsis.7779

[8] X. Zhang, C. Sun, R. Zhang, and K.-Y. Goh, "The Value of AI-Generated Metadata for UGC Platforms: Evidence from a Large-scale Field Experiment," arXiv:2412.18337, Dec. 2024.

[9] A. Vaswani et al., "Attention Is All You Need," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2017. arXiv:1706.03762

[10] T. B. Brown et al., "Language Models are Few-Shot Learners," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2020. arXiv:2005.14165

[11] J. Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2022. DOI: 10.5555/3600270.3602070

[12] W. Yang, "Beyond algorithms: The human touch machine-generated titles for enhancing click-through rates on social media," *PLOS ONE*, vol. 19, no. 7, e0306639, Jul. 2024. DOI: 10.1371/journal.pone.0306639

[13] C. J. Hutto and E. Gilbert, "VADER: A Parsimonious Rule-Based Model for Sentiment Analysis of Social Media Text," in *Proc. 8th Int. AAAI Conf. Weblogs and Social Media (ICWSM)*, 2014.

[14] T. Zhang, V. Kishore, F. Wu, K. Q. Weinberger, and Y. Artzi, "BERTScore: Evaluating Text Generation with BERT," in *Int. Conf. Learning Representations (ICLR)*, 2020. arXiv:1904.09675

[15] P. Laban et al., "With a Little Push, NLI Models can Robustly and Efficiently Predict Faithfulness," in *Proc. 61st Annual Meeting of the ACL (Short Papers)*, 2023. DOI: 10.18653/v1/2023.acl-short.79

[16] M. Aslam et al., "Optimizing Prediction of YouTube Video Popularity Using XGBoost," *Electronics*, vol. 10, no. 23, p. 2962, 2021. DOI: 10.3390/electronics10232962

[17] K. Peffers, T. Tuunanen, M. A. Rothenberger, and S. Chatterjee, "A Design Science Research Methodology for Information Systems Research," *J. Management Information Systems*, vol. 24, no. 3, pp. 45–77, 2007. DOI: 10.2753/MIS0742-1222240302

[18] H. Chen, "Title Matters: Impacts of Titles on User Engagement in Short Video Platforms," PhD Dissertation, Singapore Management University, 2023.

[19] YouTube. (2024). *YouTube for Press — Statistics.* https://blog.youtube/press/

[20] YouTube Help. (2024). *Impressions and how they lead to watch time.* https://support.google.com/youtube/answer/9314486

[21] ThumbMentor. (2026). *YouTube CTR Benchmarks 2026: What Is a Good Click-Through Rate by Niche.* https://thumbmentor.com/en/blog/youtube-ctr-benchmarks

[22] A. Davoudi Monfared and K. Murthy, "Clickbait Detection in YouTube Videos," arXiv:2107.12791, Jul. 2021. https://arxiv.org/abs/2107.12791

[23] OpenAI. (2024). *GPT-4o System Card and Model Documentation.* https://openai.com/index/gpt-4o-system-card/

[24] G. Paskalev, "Can You Predict a YouTube Video's CTR using Machine Learning?" *Medium*, n.d. https://georgepaskalev.medium.com/can-you-predict-a-youtube-videos-ctr-using-machine-learning-bc20bb142a47

[25] J. Merrell, "YouTube Views with XGBoost," personal project, n.d. https://jmmerrell.github.io/YouTube_Views_XGBoost/

[26] R. Shav, "YouTube Trending Video Dataset," Kaggle, 2023. https://www.kaggle.com/datasets/rsrishav/youtube-trending-video-dataset

[27] datasnaek, "YouTube Trending Video Statistics," Kaggle, n.d. https://www.kaggle.com/datasets/datasnaek/youtube-new

[28] LangChain. (2024). *Multi-Agent Systems — Supervisor Pattern.* LangChain Documentation. https://docs.langchain.com/oss/python/langchain/multi-agent

[29] M. Potthast, S. Köpsel, B. Stein, and M. Hagen, "Clickbait Detection," in *Proc. 38th European Conf. Information Retrieval (ECIR)*, 2016. https://webis.de/data/webis-clickbait-17.html

[30] "LLM-RUBRIC: A Multidimensional, Calibrated Approach to Automated Evaluation of Natural Language Texts," in *Proc. 62nd Annual Meeting of the ACL*, 2024. https://aclanthology.org/2024.acl-long.745.pdf

[31] — (reserved)

[32] D. Horton and R. R. Wohl, "Mass Communication and Para-Social Interaction: Observations on Intimacy at a Distance," *Psychiatry*, vol. 19, no. 3, pp. 215–229, 1956.

[33] D. Kahneman, *Thinking, Fast and Slow.* New York: Farrar, Straus and Giroux, 2011.

[34] J. White et al., "A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT," arXiv:2302.11382, Feb. 2023. https://arxiv.org/abs/2302.11382

[35] E. Gamma, R. Helm, R. Johnson, and J. Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software.* Reading, MA: Addison-Wesley, 1994.

[36] Y. Zhu et al., "Texygen: A Benchmarking Platform for Text Generation Models," in *Proc. 41st Int. ACM SIGIR Conf. on Research and Development in Information Retrieval*, 2018. DOI: 10.1145/3209978.3210080

---

*Chapter 2 — Literature Review | P.A.D.B. Pathiraja (29071) | BSc (Hons) Software Engineering | NSBM Green University*
