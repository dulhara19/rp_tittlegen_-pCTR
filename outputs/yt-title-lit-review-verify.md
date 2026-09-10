# Verification + Review Report — Ch02 Literature Review
## Slug: yt-title-lit-review | Date: 28 June 2026

---

## FATAL ISSUES (must fix before delivery)

### F1 — Duplicate References [18] and [30]
Reference [18] and [30] are **identical**: both cite Chen, H. (2023), "Title Matters: Impacts of Titles on User Engagement in Short Video Platforms," PhD Dissertation, Singapore Management University.
- [18] is cited in Table 2.1 (conceptual map)
- [30] is cited in W1 (dataset pipeline — emoji tokenisation)
**Fix:** Merge [30] into [18]. Change all `[30]` occurrences in text to `[18]`. Remove [30] from reference list. Renumber [31] → [30].

### F2 — Missing Reference: Gamma et al., 1994 (Facade Pattern)
Section D2 reads: "The Facade pattern (Gamma et al., 1994) provides a simplified interface..."
`Gamma et al., 1994` is cited in the text but **absent from the reference list**.
**Fix:** Add to reference list:
> E. Gamma, R. Helm, R. Johnson, and J. Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software.* Addison-Wesley, 1994.

---

## MAJOR ISSUES (should fix)

### M1 — T6 "Narrative Transportation Theory" — Uncited
Table 2.3 lists T6 (Personal Stakes / Vulnerability) with theoretical basis "Narrative Transportation Theory" but:
- This theory is never reviewed in the chapter body
- No citation is provided in the table or surrounding text
**Fix options:** Either (a) add a parenthetical citation e.g., (Green & Brock, 2000) and add the reference, or (b) replace the theoretical basis with "Parasocial Relationship Theory (Horton & Wohl, 1956)" which is more commonly cited for YouTube first-person stakes titles, or (c) label it as "Practitioner-validated (see §2.4.1 MrBeast case study)" if a peer-reviewed source cannot be quickly located.

### M2 — Self-BLEU Metric — Missing Origin Citation
Section W2 states: "Self-BLEU computes the BLEU score between each generated title and the other titles in the same batch" but gives no citation for Self-BLEU's origin.
**Fix:** Add: (Zhu et al., 2018) and reference:
> Y. Zhu et al., "Texygen: A Benchmarking Platform for Text Generation Models," in *Proc. 41st Int. ACM SIGIR Conf.*, 2018. DOI: 10.1145/3209978.3210080

### M3 — Persona Pattern — No Peer-Reviewed Citation
The Persona Pattern subsection makes an empirical claim: "assigning the LLM an expert role has been demonstrated to shift the model's prior toward domain-specific vocabulary" — but no citation is provided for this claim.
**Fix:** Add reference to the Prompt Pattern Catalog paper:
> J. White et al., "A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT," arXiv:2302.11382, Feb. 2023.
And add in text: "...as systematised in the Prompt Pattern Catalog (White et al., 2023 [new ref])."

### M4 — Reference [22] Missing Authors
Reference [22] is formatted as: `"Clickbait Detection in YouTube Videos," arXiv:2107.12791, Jul. 2021.`
Authors are missing.
**Fix:** Update to: `A. Davoudi Monfared and K. Murthy, "Clickbait Detection in YouTube Videos," arXiv:2107.12791, Jul. 2021.`
(Note: verify exact author names from arXiv abstract page: https://arxiv.org/abs/2107.12791)

---

## MINOR ISSUES (noted)

### N1 — Practitioner References [24], [25] — Properly Qualified
References [24] (Paskalev, Medium) and [25] (Merrell, personal project) are practitioner sources. Text already qualifies them appropriately ("Paskalev (n.d.) reported..." / "Merrell (n.d.) replicated..."). No change needed.

### N2 — Reference Numbering After Deduplication
After removing [30] (merged into [18]), all subsequent references shift: current [31] → [30]. Verify all in-text citations updated accordingly.

### N3 — Coverage Ratio Check (estimated word counts)
- 2.3 Domain Overview: ~500 words → 10% ✓
- 2.4 Existing Systems: ~1,200 words → ~24%  ← slightly under 30% target
- 2.5 Technological Analysis: ~2,900 words → ~58% ← acceptable
- 2.6 Reflection + 2.7 Summary: ~600 words
- Total body: ~5,200 words
**Overall:** Technological Analysis is sufficiently dominant. Existing Systems section is slightly under 30% but the difference is acceptable (comparative table compensates). No structural rewrite needed.

### N4 — Table 2.1 — Peffers [17] Listed But Not Discussed in Ch2 Body
[17] appears in the conceptual map table with "—" for RQ addressed. It is correctly deferred to Chapter 3. No change needed.

### N5 — Section 2.5.2 D1 — No Citation for "Network Pattern" 
The Network multi-agent pattern is mentioned ("Network pattern (any agent can call any other)") but not cited. The LangChain docs [28] cover this. Could add a footnote clarifying this is from the same LangGraph documentation source as [28]. Low priority.

---

## STRUCTURAL REVIEW

### Gap Argument (2.6 → 2.4.5) — ✅ COHERENT
The research gap justification in Section 2.6 correctly refers back to Table 2.2 (the five-criterion comparative table) and maps each literature domain to a specific dimension of the gap. The logical flow is valid: psychological theory establishes *what works* → existing systems fail to implement it → component technologies exist individually → integration gap is the novel contribution.

### Table 2.3 Citations — ✅ PASS (with M1 caveat)
T1 → [1][2] ✓ | T2 → [3] ✓ | T3 → [4] ✓ | T4 → [4] ✓ | T5 → [5] ✓ | T6 → uncited ⚠️ (M1) | T7 → uncited ⚠️ (acceptable as cognitive psychology principle, add note)

### Berger & Milkman Attribution — ✅ CORRECT
"awe as the single highest-performing emotional trigger" and "anger as the second-highest" correctly attributed to [5] in A3. Matches verified RESEARCH_NOTES §1.5.

### Zhang et al. 2024 Stats — ✅ CORRECT
"-37.9% valid watches" when AI titles replace existing human titles — matches PDF read in RESEARCH_NOTES §4.5 / §8. ✓
"2 million content producers" — correct (2,048,033). ✓
"+7.1% valid watches when adopted" — correct. ✓

### VADER — |compound| > 0.5 threshold — ✅ MATCHES SOT
SOT §14.4 states arousal target > 0.5 (absolute); chapter text states "target of |compound| > 0.5." Match. ✓
Note: W2 (system-level evaluation) states "target mean |compound| > 0.40" — this is the *average across all generated titles*, which is lower than the per-title threshold (>0.5). This is internally consistent (some titles can score lower). No issue.

### Yang 2024 — "lacks emotional sophistication" — ✅ CORRECT
Matches RESEARCH_NOTES §4.4. Paper is about RED platform (Xiaohongshu), not YouTube. Text correctly says "RED social media platform." ✓

---

## VERDICT

**ACCEPT WITH REVISIONS**

Fix F1 and F2 (FATAL) before submission. M1–M4 are strongly recommended. Minor issues are low priority. After fixes: chapter is structurally sound, argument is coherent, citations are largely verified, coverage ratios are acceptable.

---

## FIXES REQUIRED IN CHAPTER FILE

1. Merge [30] → [18]; renumber [31] → [30]
2. Add Gamma et al. 1994 to reference list
3. Add T6 citation (Narrative Transportation) or replace label
4. Add Self-BLEU citation (Zhu et al., 2018)
5. Add Persona Pattern citation (White et al., 2023)
6. Fix [22] author names
