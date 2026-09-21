"""One-off script: builds the progress submission docx by copying the
Interim Submission 01 docx (Chapters 1-3) and appending a new Progress
Summary section covering Chapters 4-7 status. Ch1-3 content is carried
over with formatting-only cleanup (em dashes / checkmark icons -> plain
punctuation, matching the equivalent cleanup already applied to the
Ch1-3 markdown source files); no wording/meaning changes. The original
Interim_Submission_01.docx on disk is left untouched.
Not part of the runtime system; lives in thesis/ as a build artefact script.
"""
import re
import docx
from docx.enum.text import WD_BREAK

SRC = "thesis/Pathiraja_29071_Interim_Submission_01.docx"
OUT = "thesis/Pathiraja_29071_Progress_Submission_02.docx"

CLAUSE_STARTERS = {
    "it", "this", "that", "these", "those", "there", "which", "and", "but",
    "so", "however", "though", "while", "since", "he", "she", "we", "you",
    "they", "i", "each", "both", "either", "neither",
}


def fix_dash_run(text):
    """Convert a spaced em dash to comma/semicolon depending on what follows,
    same heuristic used on the Ch1-3 markdown source."""
    def repl(m):
        rest = text[m.end():m.end() + 20]
        fw = re.match(r"[A-Za-z']+", rest)
        w = fw.group(0).lower() if fw else ""
        return "; " if w in CLAUSE_STARTERS else ", "
    return re.sub(r'\s—\s', repl, text)


def fix_icons_run(text):
    text = text.replace("→", "->")
    text = text.replace("✅ ", "").replace(" ✅", "").replace("✅", "")
    text = text.replace("✓", "Yes").replace("✗", "No")
    return text


# Manual overrides: same sentence-level fixes already vetted on the Ch1-3
# markdown source, reapplied here. Applied at the paragraph level (via
# replace_across_runs) since docx splits text into multiple runs at
# bold/italic boundaries, so a phrase spanning a *italic* word won't appear
# intact within any single run's .text.
MANUAL_FIXES = [
    ("the content itself, the audio, the video stream, is largely opaque",
     "the content itself (the audio, the video stream) is largely opaque"),
    ("The majority of content creators, individual educators, small businesses, independent journalists, student filmmakers, do not have training",
     "The majority of content creators (individual educators, small businesses, independent journalists, student filmmakers) do not have training"),
    ("Where once the primary mode of online information exchange was text, articles, blog posts, search results, video has emerged",
     "Where once the primary mode of online information exchange was text (articles, blog posts, search results), video has emerged"),
    ("they do not operationalise the psychological theories, Information Gap Theory [4], Prospect Theory [5], Social Proof [6]; that the copywriting literature identifies",
     "they do not operationalise the psychological theories (Information Gap Theory [4], Prospect Theory [5], Social Proof [6]) that the copywriting literature identifies"),
    ("All internal complexity, agent orchestration, prompt construction, ML model inference, NLP validation, is hidden",
     "All internal complexity (agent orchestration, prompt construction, ML model inference, NLP validation) is hidden"),
    ("All internal complexity, agent orchestration, prompt construction, vector retrieval, ML inference, NLP evaluation, is invisible",
     "All internal complexity (agent orchestration, prompt construction, vector retrieval, ML inference, NLP evaluation) is invisible"),
    ("opened the possibility of AI-assisted title generation; though, as discussed in Section 2.4,",
     "opened the possibility of AI-assisted title generation, though, as discussed in Section 2.4,"),
    ("The core limitation of raw LLMs for title generation is that their output distribution reflects their training data, broad, general-purpose text, rather than",
     "The core limitation of raw LLMs for title generation is that their output distribution reflects their training data (broad, general-purpose text) rather than"),
    ("The technique causes the model to decompose the problem into explicit sub-problems, identifying the core tension, selecting the optimal emotional framing, drafting candidates, refining for constraint satisfaction, rather than",
     "The technique causes the model to decompose the problem into explicit sub-problems: identifying the core tension, selecting the optimal emotional framing, drafting candidates, and refining for constraint satisfaction, rather than"),
    ("Titles optimised for high CTR can legitimately employ psychological techniques, curiosity gaps, urgency framing, emotional arousal, when those techniques accurately represent",
     "Titles optimised for high CTR can legitimately employ psychological techniques (curiosity gaps, urgency framing, emotional arousal) when those techniques accurately represent"),
    ("YouTube trending data may contain titles that achieved high engagement through toxic, sensationalist, or harmful framing, hate-watching content, inflammatory news titles, or content that exploits tragedy",
     "YouTube trending data may contain titles that achieved high engagement through toxic, sensationalist, or harmful framing (hate-watching content, inflammatory news titles, or content that exploits tragedy)"),
]


def replace_across_runs(paragraph, old, new):
    """Replace `old` with `new` across a paragraph's text even when `old`
    spans multiple runs (common at bold/italic boundaries). No-op if `old`
    isn't found."""
    runs = paragraph.runs
    full = "".join(r.text for r in runs)
    idx = full.find(old)
    if idx == -1:
        return False
    end = idx + len(old)
    pos = 0
    first_overlap = None
    for i, r in enumerate(runs):
        r_start, r_end = pos, pos + len(r.text)
        if r_end > idx and r_start < end:
            if first_overlap is None:
                first_overlap = i
                prefix = r.text[:max(0, idx - r_start)]
                r.text = prefix + new
            else:
                suffix_start = max(0, end - r_start)
                r.text = r.text[suffix_start:]
        pos = r_end
    return True


def clean_paragraph(p):
    for run in p.runs:
        if any(ch in run.text for ch in "—→✓✗✅"):
            t = fix_icons_run(fix_dash_run(run.text))
            run.text = t


def fix_boundary_dash(p):
    """Em dashes that fall at a run boundary (e.g. right after/before a
    bold/italic run) aren't caught by the whole-run regex in fix_dash_run,
    since the surrounding whitespace lives in a separate run. Handle those
    here, both the opening dash of a pair (starts a run) and the closing
    dash (ends a run)."""
    for i, run in enumerate(p.runs):
        t = run.text
        if t.startswith('—'):
            rest = t[1:]
            if rest.startswith(' '):
                rest = rest[1:]
            fw = re.match(r"[A-Za-z']+", rest)
            w = fw.group(0).lower() if fw else ""
            punct = "; " if w in CLAUSE_STARTERS else ", "
            run.text = punct + rest
            if i > 0:
                prev = p.runs[i - 1]
                if prev.text != '' and prev.text.strip() == '':
                    prev.text = ''
        elif t.endswith('—') or t.endswith(' —'):
            run.text = t.rstrip('— ').rstrip() + ','
            if i + 1 < len(p.runs):
                nxt = p.runs[i + 1]
                if nxt.text == ' ':
                    pass  # keep the single space before the next word/quote


d = docx.Document(SRC)

for p in d.paragraphs:
    clean_paragraph(p)
    fix_boundary_dash(p)
for t in d.tables:
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                clean_paragraph(p)
                fix_boundary_dash(p)

for p in d.paragraphs:
    for old, new in MANUAL_FIXES:
        replace_across_runs(p, old, new)
for t in d.tables:
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for old, new in MANUAL_FIXES:
                    replace_across_runs(p, old, new)

# Update title-page subtitle/date only; Ch1-3 body content otherwise untouched
# apart from the dash/icon formatting cleanup above.
d.paragraphs[1].runs[0].text = (
    "Chapters 1–3 (Resubmitted) "
    "+ Progress Summary: System Design through Evaluation (Chapters 4–7)"
)
d.paragraphs[3].runs[0].text = "19 August 2026"


def h1(text):
    d.add_paragraph(text, style="Heading 1")


def h2(text):
    d.add_paragraph(text, style="Heading 2")


def h3(text):
    d.add_paragraph(text, style="Heading 3")


def body(text):
    d.add_paragraph(text, style="Body Text")


def first(text):
    d.add_paragraph(text, style="First Paragraph")


def table(headers, rows):
    t = d.add_table(rows=1, cols=len(headers))
    t.style = "Table"
    for i, htext in enumerate(headers):
        t.rows[0].cells[i].text = htext
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = str(val)
    d.add_paragraph("", style="Normal")


# Page break before the new section
pb = d.add_paragraph()
run = pb.add_run()
run.add_break(WD_BREAK.PAGE)

h1("Progress Summary: System Design through Evaluation (Chapters 4–7)")
d.add_paragraph("", style="Normal")

h2("Purpose of This Update")
first(
    "Chapters 1–3 above are resubmitted unchanged from Interim Submission 01 "
    "(28 June 2026). This section is a short progress summary covering the work "
    "completed since then. Chapter 4 (System Requirements Specification), "
    "Chapter 5 (Implementation), Chapter 6 (Testing and Evaluation), and "
    "Chapter 7 (Concluding Remarks) are all complete, grounded in the working "
    "implementation and real evaluation data — including the human preference "
    "survey, which collected n = 29 real respondent ratings and is reported "
    "honestly as directionally consistent with, but not a statistically "
    "significant confirmation of, the automated evaluation findings."
)
d.add_paragraph("", style="Normal")

h2("Overall Status")
table(
    ["Chapter", "Status", "Completed"],
    [
        ["1. Introduction", "Done (resubmitted unchanged)", "28 Jun 2026"],
        ["2. Literature Review", "Done (resubmitted unchanged)", "28 Jun 2026"],
        ["3. Methodology", "Done (resubmitted unchanged)", "28 Jun 2026"],
        ["4. System Requirements Specification", "Done", "13 Aug 2026"],
        ["5. Implementation", "Done", "14 Aug 2026"],
        ["6. Testing and Evaluation", "Done", "10 Sep 2026"],
        ["7. Concluding Remarks", "Done (revised)", "10 Sep 2026"],
    ],
)

h2("Chapter 4: System Requirements Specification")
first(
    "The system was formally specified as a three-agent architecture "
    "(Analyzer, Generator, Critic) exposed behind a RESTful API using the "
    "Facade design pattern, with six supporting diagrams (use case, class, "
    "activity, two sequence diagrams, and system architecture), eleven "
    "functional requirements, and seven non-functional requirements. Because "
    "implementation was already underway by this point, the diagrams were "
    "built directly from the implemented code, not from a forward-looking "
    "design."
)

h2("Chapter 5: Implementation")
first(
    "All three agents, the Prompt Factory and Prompt Database (ChromaDB-backed "
    "few-shot retrieval), the pCTR machine learning model, the Critic's "
    "three-part validation layer (VADER, BERTScore, NLI faithfulness gate), "
    "the LangGraph orchestration layer, the FastAPI Facade, and a demonstration "
    "React frontend (a scope amendment added after Sprint 5) are all implemented "
    "and working. Seven implementation-level deviations from the original plan "
    "came up along the way, and each is documented in place rather than "
    "absorbed silently. The most significant was a real concurrency correctness "
    "bug found and fixed during Sprint 5: concurrent loading of two transformer "
    "models corrupted weight materialization, which was resolved by loading "
    "both models eagerly at import time instead."
)

h2("Chapter 6: Testing and Evaluation Results")
first(
    "Eleven automated functional tests cover the pipeline end-to-end and all "
    "pass. The offline pCTR classifier evaluation, the 20-video system-level "
    "evaluation, and the LLM-as-a-Judge evaluation are all complete, run "
    "against real held-out data and real model outputs. Table 2 summarises the "
    "headline results."
)
table(
    ["Evaluation area", "Result", "Target", "Met?"],
    [
        ["pCTR classifier F1-score", "0.6901", "> 0.75", "No (known, previously logged gap)"],
        ["pCTR classifier ROC-AUC", "0.7613", "> 0.80", "No (same gap)"],
        ["System-level: NLI acceptance rate", "0.94", "> 60%", "Yes"],
        ["System-level: avg. top-ranked pCTR", "0.6853", "well above range midpoint", "Yes"],
        ["System-level: avg. VADER arousal", "0.2647", "> 0.4", "No (VADER lexicon-coverage gap, discussed below)"],
        ["System-level: avg. BERTScore", "0.8717", "0.35–0.60", "No (too high; faithfulness/creativity trade-off)"],
        ["System-level: avg. Self-BLEU (diversity)", "0.0537", "< 0.4", "Yes"],
        ["System-level: latency P95", "9.95 s", "< 10 s", "Yes (narrowly)"],
        ["LLM-as-a-Judge: System vs. Baseline A (overall)", "3.95 vs. 3.30, p = 0.00079", "significant improvement", "Yes"],
        ["LLM-as-a-Judge: System vs. Baseline B (overall)", "3.95 vs. 3.85, p = 0.157", "significant improvement", "Not significant at n = 20"],
    ],
)

h2("Discussion Highlights")
first(
    "Two of the six system-level targets are missed, and both have "
    "identifiable causes. VADER's rule-based sentiment lexicon was validated "
    "on short informal social-media text carrying explicit sentiment words, so "
    "it under-detects the implicit arousal created by curiosity-gap and "
    "loss-framing titles, which happens to be exactly the register this "
    "system's trigger taxonomy relies on. That looks more like a gap between "
    "what VADER can measure and what the titles are actually doing than "
    "evidence that the titles themselves are flat. The BERTScore result sits "
    "above its target band, and that fits the Generator's anti-hallucination "
    "grounding constraint, which keeps titles close to each video's core "
    "promise. Read together, the two misses point to a real design tension "
    "between faithfulness and marketing punch, and the system currently sits "
    "on the faithful side of it."
)
body(
    "Against Baseline A (a plain descriptive title), the system's improvement "
    "is statistically significant on curiosity, urgency, and overall score "
    "(p < 0.002 throughout). Against Baseline B (a zero-shot GPT-4o prompt "
    "with no trigger engineering), the system wins significantly only on "
    "relevance (p = 0.0047). Its numerical lead on curiosity, urgency, and "
    "overall score is not statistically significant at this sample size "
    "(n = 20, p ≈ 0.16–0.32). So the honest summary is a clear win over an "
    "unoptimized baseline, and a narrower, partly significant edge over a "
    "strong zero-shot baseline."
)

h2("What Remains Open: The Human Evaluation Survey")
first(
    "SOT §19.3 specifies a blinded preference survey (Curiosity, Emotional "
    "Impact, Clarity, Trustworthiness; 1–5 scale) comparing the system's "
    "output against both baselines. All tooling for this study was built and "
    "piloted during Sprint 6: stimulus selection, condition blinding with a "
    "participant-invisible answer key, a survey instrument already drafted "
    "and ready to paste into a Google Form, and an analysis script that "
    "computes mean scores, a Wilcoxon significance test, and a Pearson "
    "correlation against the LLM judge's scores for inter-rater reliability. "
    "The study's scope was reduced from the original 10-video, n=50+ design "
    "to a 3-video, n=15–20 pilot (36 rating questions, roughly 8 to 10 "
    "minutes), after the original 120-question design was judged impractical "
    "for realistic completion. This deviation is logged in both the "
    "implementation plan and the Source of Truth document. Distribution to "
    "real participants and collection of responses had not yet happened at "
    "the time of writing. This project's data-integrity position does not "
    "allow fabricating or simulating that data under any circumstance, so it "
    "is left open here rather than filled in. It is also the single "
    "outstanding item before Chapter 6 can be considered fully complete: no "
    "further design or tooling work is needed, only distribution, collection, "
    "and running the existing analysis script."
)

h2("Chapter 7: Concluding Remarks (Done)")
first(
    "Chapter 7 evaluates the four research objectives from Chapter 1 against "
    "the Chapter 6 evidence. Objective 1.7.3 (design and develop the system) "
    "is fully met. Objectives 1.7.1 (identify viral linguistic features), "
    "1.7.2 (analyse prompting technique effectiveness), and 1.7.4 (evaluate "
    "system performance) are all met too, though each comes with a "
    "qualification worth stating plainly: the pCTR model's predictive power "
    "is moderate, not strong; the prompting advantage over the strongest "
    "baseline is real but statistically bounded, not sweeping; and the human "
    "preference survey (n = 29, exceeding the n = 15–20 pilot target) is "
    "directionally consistent with the automated findings but did not reach "
    "statistical significance at this sample size. Chapter 7 also covers "
    "problems encountered (data-availability limits on the pCTR model, the "
    "Sprint 5 concurrency bug, the two-stage human-study descoping), "
    "self-reflection on the research process, real-world application "
    "possibilities, and future recommendations. The recommendations now lead "
    "with scaling the human survey toward its original n = 50+ target for "
    "statistical power, ahead of any longer-term extension work."
)

h2("Next Steps")
body(
    "1. Re-run this build script and the equivalent export for Chapters 4–7 "
    "to produce a final assembled thesis document reflecting the completed "
    "Chapter 6/7 text (this progress summary was regenerated 10 Sep 2026, "
    "after the human survey's collection and analysis)."
)
body(
    "2. Optionally, scale the human evaluation survey toward the original "
    "n = 50+ target (Chapter 7, Section 7.6, recommendation 1) to strengthen "
    "the statistical power of its results before final submission."
)

d.add_paragraph("", style="Normal")
footer = d.add_paragraph(
    "Progress Summary | P.A.D.B. Pathiraja (29071) | BSc (Hons) Software "
    "Engineering | NSBM Green University",
    style="First Paragraph",
)

d.save(OUT)
print("Saved:", OUT)
