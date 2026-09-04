# CLAUDE.md — Project Context for AI Assistance
## AI-Powered YouTube Title Optimizer
### Client: P.A.D.B. Pathiraja (29071) | Developer: Dulhara | Institution: NSBM Green University

---

## What This Project Is

A BSc (Hons) Software Engineering final year research project. Dulhara is building both the **system** and the **thesis** for the client. The deliverable is a multi-agent AI system that automatically generates psychologically optimized YouTube video titles, implemented as an API Wrapper.

---

## Authority Files — Always Check These First

| File | Purpose |
|---|---|
| `SOURCE_OF_TRUTH.md` | Single source of truth for all content, technical decisions, and references. Never contradict it. |
| `PLAN_THESIS.md` | Section-by-section thesis writing plan. Mapped to lecturer's template. |
| `PLAN_IMPLEMENTATION.md` | Sprint-by-sprint system build plan. Mapped to SOURCE_OF_TRUTH.md sections. |

---

## Folder Structure

```
dasharatha/
│
├── CLAUDE.md                        ← this file
├── SOURCE_OF_TRUTH.md               ← single source of truth
├── PLAN_THESIS.md                   ← thesis writing plan
├── PLAN_IMPLEMENTATION.md           ← system implementation plan
│
├── client_info/                     ← original client documents (read-only reference)
│   ├── 29071 22.2 (1).pptx          ← original presentation (used to build SOT)
│   ├── Pathiraja P.A.D.B 29071 FYRP - Proposal.docx  ← research proposal
│   └── proposal.html                ← project quotation
│
├── thesis/                          ← all thesis writing
│   ├── chapters/
│   │   ├── ch01_introduction/       ← Chapter 1 drafts
│   │   ├── ch02_literature_review/  ← Chapter 2 drafts
│   │   ├── ch03_methodology/        ← Chapter 3 drafts
│   │   ├── ch04_system_design/      ← Chapter 4 drafts
│   │   ├── ch05_implementation/     ← Chapter 5 drafts
│   │   ├── ch06_evaluation/         ← Chapter 6 drafts
│   │   └── ch07_conclusion/         ← Chapter 7 drafts
│   ├── assets/                      ← diagrams, figures, tables for thesis
│   └── references/                  ← downloaded PDFs of cited papers
│
├── system/                          ← implementation code
│   ├── data/
│   │   ├── raw/                     ← Kaggle downloads, YouTube API scrapes
│   │   ├── processed/               ← cleaned, feature-engineered datasets
│   │   └── prompt_db/               ← vector store for few-shot examples
│   ├── models/                      ← saved pctr_model.pkl etc.
│   ├── agents/                      ← analyzer.py, generator.py, critic.py
│   ├── pipeline/                    ← LangGraph state machine, prompt_factory.py
│   ├── api/                         ← FastAPI main.py
│   ├── evaluation/                  ← ml_eval.py, system_eval.py, judge.py
│   ├── notebooks/                   ← Jupyter notebooks (exploration, training)
│   └── tests/                       ← test cases
│
└── research/
    └── papers/                      ← PDFs of cited academic papers
```

---

## Key Project Facts

| Field | Value |
|---|---|
| Client | P.A.D.B. Pathiraja (Student ID: 29071) |
| Program | BSc (Hons) Software Engineering |
| Institution | NSBM Green University |
| Research Methodology | Design Science Research (DSR) — Peffers' DSRM |
| System Architecture | Multi-agent API Wrapper (Facade Pattern): Analyzer → Generator → Critic |
| LLM | GPT-4o (primary), Llama 3 (fallback) |
| Agent Framework | LangChain + LangGraph |
| Backend | Python + FastAPI |
| ML Model | Random Forest + XGBoost (pCTR classifier) |
| NLP Layer | VADER + BERTScore + NLI (facebook/bart-large-mnli) |
| Prompt Engineering | Few-Shot, Chain-of-Thought (CoT), Persona Pattern |

---

## Thesis Structure & Deadlines

| Chapter | Title | Deadline |
|---|---|---|
| Ch 1 | Introduction | **28 June 2026 (Interim 01)** |
| Ch 2 | Literature Review | **28 June 2026 (Interim 01)** |
| Ch 3 | Methodology | **28 June 2026 (Interim 01)** |
| Ch 4 | System Requirements Specification | ~19 Aug 2026 |
| Ch 5 | Implementation | ~21 Aug 2026 |
| Ch 6 | Testing and Evaluation | ~23 Aug 2026 |
| Ch 7 | Concluding Remarks | ~25 Aug 2026 |
| Final | Complete thesis + system | **28 Aug 2026** |

---

## Lecturer Template Requirements

Template author: Dulanjali Wijesekara (v1.1, 23 June 2025)
File: `client_info/` — not in repo but structure is captured in `PLAN_THESIS.md`

Critical rules from the template:
- Chapter 1: sections 1.1–1.11 must all be present with exact numbering
- Chapter 2: Domain Overview 10% | Existing Systems 30% | Technological Analysis 60%
- Chapter 3: must include DSR paradigm, Peffers DSRM table, timeline, ethical considerations
- Research objectives must use verbs: To Identify / To Analyze / To Design & Develop / To Evaluate
- Personal reflection must accompany every comparative assessment in Ch2
- Citations must not be older than 5 years unless tied to a foundational theorem

---

## Implementation Sprint Schedule

| Sprint | Dates | Deliverable |
|---|---|---|
| Sprint 1 | 29 Jun – 12 Jul | Dataset pipeline + pCTR ML model |
| Sprint 2 | 13 Jul – 19 Jul | Analyzer Agent |
| Sprint 3 | 20 Jul – 26 Jul | Generator Agent + Prompt Engineering |
| Sprint 4 | 27 Jul – 2 Aug | Critic Agent (full scoring + NLI rejection) |
| Sprint 5 | 3 Aug – 9 Aug | FastAPI backend + full pipeline integration |
| Sprint 6 | 10 Aug – 16 Aug | Evaluation (ML metrics, human survey, LLM-as-a-Judge) |

---

## Rules for AI Assistance in This Project

1. **Always ground content in `SOURCE_OF_TRUTH.md`** — do not invent technical details, metrics, or references not already documented there.
2. **Follow the lecturer's template section numbering exactly** — do not add or remove sections without checking `PLAN_THESIS.md`.
3. **Thesis writing goes in `thesis/chapters/chXX_*/`** — one file per chapter.
4. **Implementation code goes in `system/`** — follow the folder structure above.
5. **Client documents in `client_info/` are read-only reference material** — do not modify them.
6. **Citations must be from `SOURCE_OF_TRUTH.md §21`** — do not cite sources not already verified in the SOT.
7. **Research methodology is DSR / Peffers DSRM** — do not suggest alternative methodologies.
