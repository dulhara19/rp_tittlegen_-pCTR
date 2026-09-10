# Provenance Record — Chapter 2 Literature Review
## Slug: yt-title-lit-review
## Date: 28 June 2026
## Author: P.A.D.B. Pathiraja (29071) | Feynman research session

---

## Artifact Locations

| File | Path | Status |
|---|---|---|
| Final chapter (canonical) | `outputs/yt-title-lit-review.md` | ✅ exists |
| Thesis copy | `thesis/chapters/ch02_literature_review/ch02_literature_review.md` | ✅ exists |
| Verification + review report | `outputs/yt-title-lit-review-verify.md` | ✅ exists |
| Research notes (source) | `research/papers/RESEARCH_NOTES.md` | ✅ exists (47 KB) |
| Plan file | `outputs/.plans/yt-title-lit-review.md` | ✅ exists |

---

## Sources Consulted

| # | Source | Type | Status |
|---|---|---|---|
| Loewenstein (1994) | Psychological Bulletin 116(1):75–98 | Peer-reviewed paper | ✅ accepted — DOI verified |
| Golman & Loewenstein (2016) | Decision journal | Peer-reviewed paper | ✅ accepted — DOI verified |
| Kahneman & Tversky (1979) | Econometrica 47(2):263–291 | Peer-reviewed paper | ✅ accepted — DOI verified |
| Cialdini (1984) | Influence: Psychology of Persuasion | Book | ✅ accepted — widely cited |
| Berger & Milkman (2012) | J. Marketing Research 49(2) | Peer-reviewed paper | ✅ accepted — DOI + Wharton PDF |
| Covington et al. (2016) | ACM RecSys '16 pp. 191–198 | Peer-reviewed paper | ✅ accepted — DOI verified |
| Kawata et al. (2025) | EAI Trans. Scalable Info Systems | Peer-reviewed paper | ✅ accepted — DOI verified |
| Zhang et al. (2024) | arXiv:2412.18337 | Preprint (not yet peer-reviewed) | ✅ accepted (with caveat) — PDF read in full |
| Vaswani et al. (2017) | NeurIPS 2017 | Peer-reviewed paper | ✅ accepted — arXiv + NeurIPS |
| Brown et al. (2020) | NeurIPS 2020 | Peer-reviewed paper | ✅ accepted — arXiv:2005.14165 |
| Wei et al. (2022) | NeurIPS 2022 | Peer-reviewed paper | ✅ accepted — ACM DL DOI verified |
| Yang (2024) | PLOS ONE 19(7):e0306639 | Peer-reviewed paper | ✅ accepted — DOI + PubMed |
| Hutto & Gilbert (2014) | AAAI ICWSM | Peer-reviewed paper | ✅ accepted — AAAI OJS verified |
| Zhang et al. (2020) | ICLR 2020 | Peer-reviewed paper | ✅ accepted — OpenReview verified |
| Laban et al. (2023) | ACL 2023 Short Papers | Peer-reviewed paper | ✅ accepted — DOI verified |
| Aslam et al. (2021) | Electronics 10(23):2962 | Peer-reviewed paper | ✅ accepted — MDPI DOI verified |
| Peffers et al. (2007) | JMIS 24(3):45–77 | Peer-reviewed paper | ✅ accepted — DOI verified |
| Chen (2023) | PhD Dissertation, SMU | Doctoral thesis | ✅ accepted (secondary source) |
| YouTube Help (2024) | YouTube official documentation | Official documentation | ✅ accepted |
| ThumbMentor (2026) | Industry benchmark report | Industry source | ✅ accepted with qualification |
| arXiv:2107.12791 (2021) | arXiv preprint | Preprint | ✅ accepted — arXiv verified |
| Paskalev (n.d.) | Medium practitioner blog | Practitioner | ⚠️ accepted with qualification |
| Merrell (n.d.) | Personal project page | Practitioner | ⚠️ accepted with qualification |
| Kaggle datasets (rsrishav, datasnaek) | Public datasets | Dataset | ✅ accepted |
| LangChain Documentation (2024) | Official docs | Official documentation | ✅ accepted |
| Potthast et al. (2016) | ECIR 2016 | Peer-reviewed paper | ✅ accepted |
| Gamma et al. (1994) | Design Patterns book | Book | ✅ accepted — added in fix pass |
| Horton & Wohl (1956) | Psychiatry journal | Peer-reviewed paper | ✅ accepted (T6 theory basis) |
| Kahneman (2011) | Thinking, Fast and Slow | Book | ✅ accepted (T7 cognitive ease) |
| White et al. (2023) | arXiv:2302.11382 | Preprint | ✅ accepted — Persona Pattern |
| Zhu et al. (2018) | ACM SIGIR 2018 | Peer-reviewed paper | ✅ accepted — Self-BLEU origin |
| LLM-RUBRIC (2024) | ACL 2024 | Peer-reviewed paper | ✅ accepted — ACL Anthology |

---

## Accepted vs. Rejected

**Sources accepted:** 32
**Sources with caveats (practitioner/preprint):** 4 (Zhang 2024 arXiv, Paskalev blog, Merrell personal, ThumbMentor industry)
**Sources rejected:** 0
**Claims downgraded from RESEARCH_NOTES:** 2
  - "ACL 2025 NLI > BERTScore" → replaced with Laban et al. 2023 (ACL 2023)
  - "RF 80.1% accuracy" exact source → replaced with Aslam et al. 2021 (86% XGBoost)

---

## Verification Status

| Check | Result |
|---|---|
| All in-text citations have reference list entry | ✅ after fixes |
| Duplicate reference removed ([30] merged into [18]) | ✅ fixed |
| Gamma et al. 1994 added to reference list | ✅ fixed |
| T6 theoretical basis cited (Horton & Wohl 1956) | ✅ fixed |
| Self-BLEU origin cited (Zhu et al. 2018) | ✅ fixed |
| Persona Pattern cited (White et al. 2023) | ✅ fixed |
| T7 Cognitive Ease cited (Kahneman 2011) | ✅ fixed |
| Reference [22] author names added | ✅ fixed |
| Coverage ratio acceptable (10/~25/~60) | ✅ verified |
| Research gap argument coherent (2.6 → 2.4.5) | ✅ verified |
| Key stats from Zhang et al. 2024 match PDF | ✅ verified |
| VADER |compound| > 0.5 matches SOT §14.4 | ✅ verified |

---

## Intermediate Research Files

- `research/papers/RESEARCH_NOTES.md` — 47 KB primary source verification document
  - Contains verified DOIs, key findings, and corrections for all major citations
  - Used as primary input for all technological analysis sections

---

## Known Residual Risks

| Risk | Severity | Notes |
|---|---|---|
| Zhang et al. (2024) is an arXiv preprint | Low | Large-scale field experiment, methodologically robust; flag to supervisor |
| Paskalev (n.d.) RMSE 3.48% claim | Low | Medium/blog source; stated with qualification in text |
| arXiv:2107.12791 author names | Low | Authors listed as "Davoudi Monfared and Murthy" — verify against arXiv abstract page before submission |
| Horton & Wohl (1956) — T6 basis | Low | Classic media studies paper; appropriate but parasocial theory may not be the original YTO intent; acceptable substitution |

---

*Provenance record compiled by Feynman | 28 June 2026*
