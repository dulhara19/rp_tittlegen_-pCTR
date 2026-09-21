# Chapter 3: Methodology

---

## 3.1 Research Paradigm

### Paradigm: Pragmatism

Every research project rests on a set of philosophical assumptions about the nature of knowledge and how it can be obtained. These assumptions, collectively the research paradigm, determine which methods are legitimate, what counts as evidence, and how findings are interpreted. The paradigm adopted for this research is **Pragmatism**.

Pragmatism, as a philosophical tradition originating with Peirce, James, and Dewey and later applied to social science research methodology, holds that knowledge should be evaluated by its practical consequences and its capacity to solve real-world problems rather than by adherence to a single ontological doctrine [1]. In pragmatist epistemology, there is no single "best" way to know something: the appropriate methods depend on the research question and what kinds of evidence are most useful for answering it. Truth, in the pragmatist formulation, is what works.

This stance has a direct bearing on research design. Because pragmatism is not committed to either the objective, value-free stance of positivism or the subjective, meaning-oriented stance of interpretivism, it permits the legitimate combination of quantitative and qualitative methods in the same study. This flexibility is essential for this research: the evaluation of the YTO system requires both quantitative measurement (F1-score, predicted CTR, BERTScore, VADER compound) to assess objective system performance, and qualitative human evaluation (preference surveys, LLM-as-a-Judge rubric scoring) to assess the subjective dimensions of title quality (curiosity, emotional impact, and trustworthiness) that quantitative proxies cannot fully capture.

**Why not Positivism:** A purely positivist paradigm would require tightly controlled laboratory conditions to isolate a single causal variable, a design incompatible with a system whose performance depends on the interaction of multiple AI components, a probabilistic ML model, and human evaluators with inherent variability. It would also favour deductive testing of pre-specified hypotheses over the discovery-oriented iteration that artefact construction requires.

**Why not Interpretivism:** An interpretivist paradigm would focus on the subjective meaning that creators and viewers attach to titles, appropriate for a study of creator experience or viewer psychology. This research is ultimately concerned with a software artefact and its measurable outputs, not with the lived experience of participants.

**Pragmatism is the fit:** It evaluates the artefact by whether it works, whether the titles it generates outperform baselines on measurable engagement predictors while satisfying human evaluators on perceptual quality criteria. Both types of evidence are gathered, because both matter.

---

## 3.2 Research Approach

### Approach: Abductive

Research approaches describe how the relationship between theory and data is structured. Three main approaches are distinguished in the literature: deductive (testing a pre-formed hypothesis derived from theory), inductive (generating theory from observed data), and abductive (moving iteratively between theory and observation to infer the best explanation) [2].

This research adopts an **abductive approach**.

The study does not begin with a null hypothesis to be tested under controlled conditions (deductive), nor does it begin with a blank-slate observation of the world from which theory is meant to emerge inductively. Instead, it begins with established theoretical constructs (Information Gap Theory [3], Prospect Theory [4], Social Proof [5], and the empirically validated principle that high-arousal emotional content drives viral spread [6]) and uses these to *design* a software artefact. It then evaluates the artefact empirically against measurable performance criteria.

This movement, from established theory to artefact design to empirical evaluation back to theoretical reflection, is precisely what abductive reasoning describes: reasoning from existing theoretical knowledge to a novel instantiation of that knowledge, and then evaluating whether the instantiation works as theorised. The abductive approach is consistent with the Design Science Research paradigm (Section 3.3), in which existing theories serve as the "kernel theories" that motivate and guide artefact design, and the artefact's evaluated performance contributes new knowledge back to the theoretical base.

---

## 3.3 Research Strategy

### Strategy: Design Science Research (DSR)

The research strategy adopted is **Design Science Research (DSR)**, as formalised by Peffers, Tuunanen, Rothenberger, and Chatterjee (2007) in the widely cited *Design Science Research Methodology for Information Systems Research* [7].

DSR is the dominant research paradigm in Information Systems and Software Engineering when the primary output of the study is a novel **artefact**, a construct, model, method, or instantiation, created to address a specific real-world problem. Hevner et al. (2004) articulate the core principle: design science creates and evaluates IT artefacts intended to solve identified organisational problems [8]. Unlike natural science research, which describes and explains existing phenomena, Design Science *creates new reality* through the act of building. The artefact itself is the primary research contribution, and its evaluation against defined performance criteria constitutes the empirical contribution.

DSR is characterised by two equally weighted requirements:
- **Rigor:** The artefact must be grounded in existing knowledge (theoretical constructs, prior research, established techniques) and evaluated using systematic, reproducible methods.
- **Relevance:** The artefact must address a real, identified problem and demonstrate practical value to an identifiable stakeholder community.

For this research, both requirements are met. The system is rigorously grounded in Information Gap Theory [3], Prospect Theory [4], Social Proof [5], and established NLP techniques (VADER [9], BERTScore [10], NLI [11], Few-Shot prompting [12], Chain-of-Thought reasoning [13]). Its relevance is established by the empirical evidence that metadata quality directly determines content visibility for millions of content creators [14][15].

### Alternative Strategies Considered and Rejected

| Strategy | Why Rejected |
|---|---|
| **Case Study** | Appropriate for studying existing phenomena in real-world context; this research creates a new artefact rather than studying an existing one |
| **Controlled Experiment** | Would require live YouTube channels with significant traffic for real CTR measurement, outside the ethical and practical scope of a research prototype |
| **Survey** | Captures perceptions and opinions; cannot evaluate software system performance or NLP metric behaviour |
| **Grounded Theory** | Generates theory inductively from data; this research has an established theoretical foundation and a defined artefact output |
| **Action Research** | Requires collaborative, iterative engagement with an organisational client; this is a solo academic project with no host organisation |

DSR is the methodologically sound choice because the research question, how to design and evaluate a multi-agent AI system for title optimisation, is fundamentally a design question, not a discovery question.

---

## 3.4 Fact Collection Mechanisms

This section specifies the data sources used across all phases of the project: model training, system evaluation, and the Prompt Database.

**Table 3.1: Data Collection Mechanisms**

| Data Type | Source | Collection Method | Purpose |
|---|---|---|---|
| YouTube trending video titles + engagement metrics | Kaggle YouTube Trending Dataset (rsrishav) [16] | Direct download via Kaggle CLI | pCTR ML model training; viral linguistic pattern analysis |
| Historical YouTube trending statistics | Kaggle YouTube Trending Video Statistics (datasnaek) [17] | Direct download via Kaggle CLI | ML model training; baseline viral pattern dataset |
| High-performing channel titles + metadata | YouTube Data API v3 | Targeted API scraping (MrBeast, Veritasium, Mark Rober, Kurzgesagt) | Few-Shot Prompt Database population; gold-standard positive examples |
| Annotated clickbait titles (negative examples) | Webis Clickbait Corpus (Potthast et al., 2016) [18] | Download from webis.de | NLI validation layer training; rejection boundary definition |
| Psychological trigger type labels (T1–T7) | Custom annotation | Manual labelling of 500–1,000 title samples by researcher | Trigger classification feature for pCTR model |
| Human title preference ratings | A/B preference survey (n ≥ 50 participants) | Online survey instrument (Google Forms) | Qualitative human evaluation; Curiosity, Emotional Impact, Clarity, Trustworthiness scoring |

### Data Ethical Considerations

All secondary data sources are publicly available. The Kaggle datasets are published under open licences for research use. YouTube Data API v3 usage complies with YouTube's Terms of Service for non-commercial research data collection, with rate limits observed and no personal user data collected [19]. The human preference survey collects no personally identifiable information beyond optional demographic data (age range, YouTube usage frequency); participation is voluntary and anonymised.

---

## 3.5 Research Methodology

### Methodology: Peffers' Design Science Research Methodology (DSRM)

The specific methodology adopted is the **six-phase Design Science Research Methodology (DSRM)** proposed by Peffers et al. (2007) [7]. DSRM provides a structured, phase-by-phase framework for conducting DSR in Information Systems and Software Engineering, ensuring that the artefact development process is both systematic and communicable.

Peffers et al. identified that prior DSR work lacked a common process model that researchers and reviewers could use to evaluate whether a study followed DSR rigor. The DSRM fills this gap by prescribing a nominal sequence of six activities, while recognising that real research may begin at any activity and iterate between them. The six activities are:

1. **Problem Identification and Motivation**: Define the problem and justify the value of a solution
2. **Define Objectives of a Solution**: Specify what a successful artefact must accomplish
3. **Design and Development**: Create the artefact
4. **Demonstration**: Use the artefact to solve one or more instances of the problem
5. **Evaluation**: Observe and measure how well the artefact addresses the problem
6. **Communication**: Communicate the problem, artefact, and evaluation to relevant audiences

This process aligns naturally with the structure of this thesis and the academic calendar of the project, as shown in Section 3.6.

---

## 3.6 Execution Workflow

The following table maps each DSRM activity to its concrete project realisation, the chapter(s) in which it is documented, and its primary deliverable output.

**Table 3.2: DSRM Execution Workflow**

| DSRM Activity | Project Action | Chapter(s) | Output |
|---|---|---|---|
| **1. Problem Identification & Motivation** | Analysis of the creator CTR bottleneck; literature review of clickbait research, LLM generation limits, and psychological trigger theory | Ch1, Ch2 | Research problem statement; justification of value of a solution; research gap articulation |
| **2. Define Objectives** | Specification of four research objectives (§1.7.1–1.7.4); definition of success criteria (pCTR > 6%, F1 > 0.75, NLI acceptance > 60%, human preference significance) | Ch1, Ch3 | Research aim; four research objectives; system performance targets |
| **3. Design & Development** | Multi-agent pipeline architecture; Prompt Factory design; pCTR ML model training; FastAPI backend implementation; NLI and BERTScore integration | Ch4, Ch5 | Working system prototype; trained pCTR model; populated Prompt Database; REST API endpoint |
| **4. Demonstration** | Application of the system to 10+ diverse video topics across three content categories (Education, Entertainment, Technology) with outputs recorded | Ch5, Ch6 | Demonstration dataset: video transcripts -> generated title batches with per-title scores |
| **5. Evaluation** | Offline ML evaluation (F1, ROC-AUC, RMSE); system-level metrics (pCTR, VADER, BERTScore, Self-BLEU, acceptance rate); human A/B preference survey (n ≥ 50); LLM-as-a-Judge rubric scoring | Ch6 | Quantitative evaluation report; human preference results; LLM-judge scores; comparative analysis against Baseline A and Baseline B |
| **6. Communication** | Thesis dissertation write-up; GitHub repository publication; potential academic conference paper | All chapters | Thesis document; public code repository |

### Entry Point

Following Peffers et al.'s (2007) entry point taxonomy [7], this research begins at **Activity 1 (Problem-Centred Initiation)**: the research was motivated by the identification of a practical problem (the creator metadata optimisation bottleneck) rather than by an available technology seeking an application or a prior design in need of improvement.

---

## 3.7 Project Management Methodology

### Methodology: Agile (Scrum-Inspired)

The development and research process is managed using an **Agile, Scrum-inspired methodology**, adapted for a single-researcher academic project [20].

Agile is selected over traditional plan-driven methodologies for three reasons specific to this project.

Each component of the YTO system (the Analyzer Agent, Generator Agent, Critic Agent, pCTR model, and FastAPI backend) needs to be developed and tested as an independent increment before integration, which matches the Sprint model: each sprint delivers a testable, working component, and the output of each sprint informs the design decisions of the next. Prompt engineering is also inherently empirical — the optimal CoT sequence, the effective few-shot example count, and the BERTScore threshold for the relevance filter cannot all be fully specified in advance, but emerge through iterative testing and refinement, and Agile accommodates this by treating backlog refinement as an ongoing activity rather than requiring all requirements to be defined upfront. Finally, there's a question of scale: this is a solo project with a fixed timeline, and PRINCE2 and other heavyweight methodologies impose extensive documentation overhead designed for multi-stakeholder projects. Agile's minimal ceremony (sprint planning, a working product increment, and retrospective) fits the scale and pace of a single-researcher academic project.

**Sprint structure:** Six two-week development sprints (Sprints 1–6) follow the Interim Submission 01 deadline. Each sprint is focused on a single deliverable component. Backlog items that cannot be completed within a sprint are carried forward rather than blocked.

**Tools:** GitHub for version control and sprint board; a GitHub Projects Kanban board tracks backlog, in-progress, and completed items per sprint.

### Alternative Considered: PRINCE2

PRINCE2 (Projects IN Controlled Environments) was considered and rejected. PRINCE2's stage-gate model, management product documentation requirements, and multi-role structure (Project Board, Project Manager, Team Manager) are designed for organisational projects with external stakeholders and formal governance requirements. For a solo academic research project with a supervisor rather than a client board, this overhead is unnecessary and counterproductive.

---

## 3.8 Project Timeline

**Table 3.3: Project Timeline**

| Phase | Deliverable | Target Date | Status |
|---|---|---|---|
| **Interim Submission 01** | Chapter 1 (Introduction), Chapter 2 (Literature Review), Chapter 3 (Methodology) | 28 June 2026 | In progress |
| **Sprint 1: Data & ML** | Kaggle dataset pipeline; feature engineering; pCTR model (Random Forest + XGBoost) trained and evaluated; F1 / ROC-AUC recorded | 12 July 2026 | Planned |
| **Sprint 2: Analyzer Agent** | Analyzer Agent fully implemented; video brief output (core promise, key entities, emotional ceiling, trigger candidates) validated on 5 test cases | 19 July 2026 | Planned |
| **Sprint 3: Generator Agent** | Generator Agent with Prompt Database (vector retrieval), CoT sequence, and Few-Shot injection; 5 candidate titles produced per run | 26 July 2026 | Planned |
| **Sprint 4: Critic Agent** | Full end-to-end pipeline: NLI, VADER, BERTScore, pCTR scoring integrated; composite score ranking working; rejection log operational | 2 August 2026 | Planned |
| **Sprint 5: FastAPI & Integration** | FastAPI REST endpoint live; full Analyzer->Generator->Critic pipeline accessible via HTTP POST; Pydantic request/response validation working | 9 August 2026 | Planned |
| **Sprint 6: Evaluation** | Demonstration dataset generated (10+ topics, 3 categories); human survey launched and n ≥ 50 responses collected; LLM-as-a-Judge scoring completed; all evaluation metrics compiled | 16 August 2026 | Planned |
| **Chapter 4: System Design** | SRS, diagrams (use case, class, activity, sequence), architecture documentation written | 19 August 2026 | Planned |
| **Chapter 5: Implementation** | Implementation chapter written with pseudocode, code snippets, and sample outputs | 21 August 2026 | Planned |
| **Chapter 6: Results & Evaluation** | Evaluation chapter written with result tables, graphs, and comparative analysis | 23 August 2026 | Planned |
| **Chapter 7: Conclusion** | Concluding chapter; objectives triangulated against results; future work articulated | 25 August 2026 | Planned |
| **Final Submission** | Complete thesis document + GitHub repository published | 28 August 2026 | Planned |

The timeline allocates six sprints (twelve weeks) to system development and evaluation, followed by four writing days for Chapters 4–7 once implementation and evaluation data are complete. This sequence reflects the DSR cycle: build first, then document and communicate.

---

## 3.9 Ethical Considerations

Research involving AI-generated content, human participant evaluation, and publicly collected datasets raises several ethical dimensions that must be addressed explicitly.

### 3.9.1 Deception versus Persuasion

The central ethical tension in this research is the boundary between legitimate persuasion and deceptive manipulation. Titles optimised for high CTR can legitimately employ psychological techniques (curiosity gaps, urgency framing, emotional arousal) when those techniques accurately represent the content the viewer will receive. They become ethically problematic when they create false expectations, fabricate claims, or misrepresent the video's content.

The YTO system is explicitly designed to operate on the legitimate side of this boundary. The NLI-based hard rejection gate eliminates any title classified as a factual "Contradiction" to the video's core promise before it is surfaced to the creator. The Analyzer Agent establishes the semantic envelope of permissible claims by extracting only what is truthfully present in the video transcript. The Generator Agent works only within that envelope. This architecture means the system structurally prohibits deceptive output; it is not an opt-in safety feature but a mandatory pipeline stage.

This design implements the distinction between *persuasion* (legitimate influence through accurate emotional framing) and *manipulation* (influence through false or misleading claims). The system targets persuasion while architecturally blocking manipulation.

### 3.9.2 Data Privacy

No personal user data is collected at any stage of this research. All training datasets are publicly available: the Kaggle YouTube Trending Datasets contain only publicly accessible video metadata (titles, view counts, like counts, channel names) that YouTube makes available through its public interface. The YouTube Data API v3 is used in compliance with YouTube's Terms of Service for non-commercial academic research [19], with API rate limits respected. The human preference survey collects no personally identifiable information; responses are recorded anonymously and used solely for aggregate comparative analysis.

### 3.9.3 Bias and Toxicity in Training Data

YouTube trending data may contain titles that achieved high engagement through toxic, sensationalist, or harmful framing (hate-watching content, inflammatory news titles, or content that exploits tragedy). If such examples are included in the Prompt Database unfiltered, the system could learn to optimise for engagement patterns that are harmful.

To mitigate this, a toxicity filtering stage is applied to the Prompt Database using the `unitary/toxic-bert` classifier. Titles scoring above the toxicity threshold are excluded from the few-shot example pool regardless of their historical engagement performance. This ensures the system optimises for psychological engagement mechanisms (curiosity, emotional arousal, social proof) without learning harmful framing as a positive engagement signal.

### 3.9.4 Transparency and Human Oversight

The YTO system is positioned as a *co-pilot for creators*, not an autonomous replacement for human editorial judgment. The API returns a ranked list of five candidates with per-title scoring, the creator sees the options and the scores, and makes the final selection. No title is published automatically. This design preserves human agency in the content creation workflow and makes the system's reasoning interpretable (the creator can see why a title scored highly on pCTR or was flagged by NLI).

The "black box" nature of the underlying LLM (GPT-4o) is acknowledged explicitly. The system does not claim to fully explain why any specific title was generated; it provides interpretable *evaluation scores* for each output, not a mechanistic explanation of the generation process.

### 3.9.5 Academic Integrity

All sources are cited in IEEE format. The research prototype is developed independently. Any use of AI tools during the writing or implementation process is acknowledged in accordance with NSBM Green University's academic integrity policy. The artefact is a research prototype intended for academic evaluation; commercial deployment would require additional ethical review, a point explicitly noted in the limitations.

### 3.9.6 Platform Policy Compliance

YouTube's Terms of Service (Section 4H) explicitly prohibit video metadata that "sets up viewer expectations the content doesn't deliver" [19]. Violations can result in video demonetisation, channel strikes, and algorithmic suppression. The NLI faithfulness layer is therefore not only an ethical safeguard but also a **platform compliance mechanism**: every title produced by the system has passed a computational check confirming it does not contradict the video's content, protecting the creator from inadvertent ToS violations.

---

## 3.10 Chapter Summary

This chapter has established the philosophical and procedural framework that governs this research. The philosophical layer rests on a **Pragmatist paradigm**, which licenses the combination of quantitative and qualitative evaluation methods appropriate for assessing both system performance and human preference. The **abductive approach** reflects the research's movement from established psychological and NLP theory to artefact design to empirical validation. The **Design Science Research strategy** positions this project within the IS/SE tradition of artefact-oriented scholarship, in which building and evaluating a novel system constitutes a genuine research contribution. The **Peffers DSRM** provides the six-phase process model that structures the project from problem identification through final communication.

The methodological choices made in this chapter are not procedural formalities. They directly shape what the research can and cannot claim. DSR under a pragmatist paradigm allows this research to claim that the YTO system *works*, meaning it outperforms defined baselines on defined metrics, without requiring the experimental isolation that would be necessary to claim universal causal laws about AI-generated content. That is the appropriate claim scope for a software engineering research prototype evaluated over a bounded set of test cases.

Chapter 4 proceeds to operationalise these methodological decisions into a full system requirements specification, including stakeholder analysis, use case diagrams, class diagrams, activity diagrams, sequence diagrams, and formal functional and non-functional requirements.

---

## References

[1] J. W. Creswell and J. D. Creswell, *Research Design: Qualitative, Quantitative, and Mixed Methods Approaches*, 5th ed. London: SAGE Publications, 2018.

[2] R. K. Kovács and C. Spens, "Abductive reasoning in logistics research," *International Journal of Physical Distribution & Logistics Management*, vol. 35, no. 2, pp. 132–144, 2005.

[3] G. Loewenstein, "The psychology of curiosity: A review and reinterpretation," *Psychological Bulletin*, vol. 116, no. 1, pp. 75–98, 1994. DOI: 10.1037/0033-2909.116.1.75

[4] D. Kahneman and A. Tversky, "Prospect Theory: An Analysis of Decision under Risk," *Econometrica*, vol. 47, no. 2, pp. 263–291, 1979. DOI: 10.2307/1914185

[5] R. B. Cialdini, *Influence: The Psychology of Persuasion.* New York: Harper & Row, 1984.

[6] J. Berger and K. L. Milkman, "What Makes Online Content Viral?" *Journal of Marketing Research*, vol. 49, no. 2, pp. 192–205, 2012. DOI: 10.1509/jmr.10.0353

[7] K. Peffers, T. Tuunanen, M. A. Rothenberger, and S. Chatterjee, "A Design Science Research Methodology for Information Systems Research," *Journal of Management Information Systems*, vol. 24, no. 3, pp. 45–77, 2007. DOI: 10.2753/MIS0742-1222240302

[8] A. R. Hevner, S. T. March, J. Park, and S. Ram, "Design Science in Information Systems Research," *MIS Quarterly*, vol. 28, no. 1, pp. 75–105, 2004. DOI: 10.2307/25148625

[9] C. J. Hutto and E. Gilbert, "VADER: A Parsimonious Rule-Based Model for Sentiment Analysis of Social Media Text," in *Proc. 8th Int. AAAI Conf. Weblogs and Social Media (ICWSM)*, 2014.

[10] T. Zhang, V. Kishore, F. Wu, K. Q. Weinberger, and Y. Artzi, "BERTScore: Evaluating Text Generation with BERT," in *Int. Conf. Learning Representations (ICLR)*, 2020. arXiv:1904.09675

[11] P. Laban et al., "With a Little Push, NLI Models can Robustly and Efficiently Predict Faithfulness," in *Proc. 61st Annual Meeting of the ACL (Short Papers)*, 2023. DOI: 10.18653/v1/2023.acl-short.79

[12] T. B. Brown et al., "Language Models are Few-Shot Learners," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2020. arXiv:2005.14165

[13] J. Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2022. DOI: 10.5555/3600270.3602070

[14] P. Covington, J. Adams, and E. Sargin, "Deep Neural Networks for YouTube Recommendations," in *Proc. 10th ACM Conf. Recommender Systems (RecSys '16)*, pp. 191–198, 2016. DOI: 10.1145/2959100.2959190

[15] X. Zhang, C. Sun, R. Zhang, and K.-Y. Goh, "The Value of AI-Generated Metadata for UGC Platforms: Evidence from a Large-scale Field Experiment," arXiv:2412.18337, Dec. 2024.

[16] R. Shav, "YouTube Trending Video Dataset," Kaggle, 2023. https://www.kaggle.com/datasets/rsrishav/youtube-trending-video-dataset

[17] datasnaek, "YouTube Trending Video Statistics," Kaggle, n.d. https://www.kaggle.com/datasets/datasnaek/youtube-new

[18] M. Potthast, S. Köpsel, B. Stein, and M. Hagen, "Clickbait Detection," in *Proc. 38th European Conf. Information Retrieval (ECIR)*, 2016. https://webis.de/data/webis-clickbait-17.html

[19] YouTube. (2024). *Terms of Service.* https://www.youtube.com/t/terms

[20] K. Schwaber and J. Sutherland, *The Scrum Guide: The Definitive Guide to Scrum: The Rules of the Game.* Scrum.org, 2020. https://scrumguides.org/scrum-guide.html

---

*Chapter 3, Methodology | P.A.D.B. Pathiraja (29071) | BSc (Hons) Software Engineering | NSBM Green University*
