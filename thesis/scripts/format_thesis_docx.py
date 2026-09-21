"""Reformat the final thesis to the NSBM Green University Senate-Approved
Thesis Preparation and Formatting Guideline WITHOUT changing research content.

SOURCE is a read-only backup copy; OUTPUT is a different file. The script is
idempotent: re-run it top to bottom any time (python format_thesis_docx.py).
Page numbers for the TOC / List of Figures / List of Tables come from
page_map.json, produced by harvest_pages.py (regenerate after any change that
alters pagination).
"""

import copy
import json
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Emu, Pt, RGBColor
from docx.text.paragraph import Paragraph
from docx.text.run import Run

HERE = Path(__file__).resolve().parent
THESIS = HERE.parent
SOURCE = THESIS / "bckp" / "Pathiraja_29071_Final_Thesis.docx"
OUTPUT = THESIS / "Pathiraja_29071_Final_Thesis_NEW.docx"
PAGE_MAP = HERE / "page_map.json"
LOG = HERE / "format_log.txt"

FONT = "Times New Roman"
LEFT_CM, RIGHT_CM, TOP_CM, BOTTOM_CM = 3.175, 2.54, 2.54, 2.54  # 1.25", 1", 1", 1"
A4_W_CM, A4_H_CM = 21.0, 29.7
TEXT_W_CM = A4_W_CM - LEFT_CM - RIGHT_CM
TEXT_W_TW = int(TEXT_W_CM / 2.54 * 1440)  # twentieths of a point

# Thesis details (all taken from the existing thesis title block).
TITLE = "AI-Powered Proactive YouTube Title Optimizer"
SUBTITLE = ("A Multi-Agent System for Psychologically Optimised, "
            "Faithfulness-Constrained Video Title Generation")
AUTHOR = "P.A.D.B. Pathiraja"
STUDENT_ID = "29071"
DEGREE = "BSc (Hons) Software Engineering"
FACULTY = "Faculty of Computing"
SUBMITTED = "September 2026"
PLACEHOLDER_DEPT = "[to be confirmed]"
PLACEHOLDER_SUP = "[surname]"

# New chapter order. old chapter number -> (new number, new title)
NEW_CHAPTERS = {
    "Introduction": (1, "Introduction"),
    "Objectives": (2, "Objectives"),
    "Literature Review": (3, "Literature Review"),
    "Methodology": (4, "Methodology"),
    "System Requirements Specification": (5, "System Requirements Specification"),
    "Implementation": (6, "Implementation"),
    "Testing and Evaluation": (7, "Results"),
    "Concluding Remarks": (8, "Discussion and Conclusions"),
}

ABSTRACT = (
    "Video titles strongly influence whether a viewer clicks, yet writing titles that "
    "are both engaging and faithful to the video content is a skill most creators lack, "
    "and generic large language model (LLM) prompting rarely provides it. This research "
    "aimed to design, develop and evaluate a multi-agent AI system, implemented as a "
    "Facade-pattern API wrapper, that generates psychologically optimised YouTube titles "
    "while preserving semantic faithfulness to the source video. Following the Design "
    "Science Research Methodology of Peffers et al., the system was built as an "
    "Analyzer, Generator and Critic agent pipeline orchestrated with LangGraph and served "
    "through FastAPI. The Generator uses Few-Shot, Chain-of-Thought and Persona prompting, "
    "and the Critic combines a predicted click-through rate (pCTR) model with VADER, "
    "BERTScore and natural language inference (NLI) checks. The system was evaluated "
    "through functional and non-functional testing, offline model metrics, a system-level "
    "evaluation on 20 videos, an LLM-as-a-Judge evaluation (60 evaluations) and a human "
    "survey (n = 29). All eleven functional tests passed. The pCTR classifier reached an "
    "F1 score of 0.6901 and a ROC-AUC of 0.7613, below its targets of 0.75 and 0.80, and "
    "four of six system-level targets were met. The system significantly outperformed a "
    "purely descriptive baseline and held a significant advantage over a zero-shot GPT-4o "
    "baseline on relevance. The human survey was directionally consistent with these "
    "results but not statistically significant, and agreement between human and LLM "
    "ratings was weak (r = -0.14). The work shows that generative AI can be systematically "
    "constrained to produce faithful, engagement-oriented titles, while the moderate "
    "predictive performance and pilot-scale human evidence mark clear limits to the "
    "current validation."
)

ACK_PARAS = [
    "I would like to express my sincere gratitude to my supervisor, Ms. Nimesha, for her "
    "guidance, patience and encouragement throughout this research. Her constructive "
    "feedback and support at every stage shaped both the system and this thesis, and I am "
    "truly grateful for the time and care she invested in my work.",
    "I also thank the lecturers and staff of the Faculty of Computing at NSBM Green "
    "University for the knowledge and support I received during my degree, and the "
    "participants who took the time to complete the evaluation survey.",
    "Finally, I thank my family and friends for their constant support, understanding and "
    "motivation, which carried me through the demanding months of this project.",
]

ABBREVIATIONS = [
    ("AAAI", "Association for the Advancement of Artificial Intelligence"),
    ("ACL", "Association for Computational Linguistics"),
    ("AI", "Artificial Intelligence"),
    ("ANEW", "Affective Norms for English Words"),
    ("API", "Application Programming Interface"),
    ("ASGI", "Asynchronous Server Gateway Interface"),
    ("AUC", "Area Under the Curve"),
    ("BERT", "Bidirectional Encoder Representations from Transformers"),
    ("BLEU", "Bilingual Evaluation Understudy"),
    ("CI/CD", "Continuous Integration and Continuous Delivery"),
    ("CLI", "Command-Line Interface"),
    ("CORS", "Cross-Origin Resource Sharing"),
    ("CPU", "Central Processing Unit"),
    ("CRUD", "Create, Read, Update, Delete"),
    ("CTR", "Click-Through Rate"),
    ("DSR", "Design Science Research"),
    ("DSRM", "Design Science Research Methodology"),
    ("FAISS", "Facebook AI Similarity Search"),
    ("FOMO", "Fear of Missing Out"),
    ("GB", "Gigabyte"),
    ("GIL", "Global Interpreter Lock"),
    ("GPT", "Generative Pre-trained Transformer"),
    ("GPU", "Graphics Processing Unit"),
    ("HTML", "HyperText Markup Language"),
    ("HTTP", "HyperText Transfer Protocol"),
    ("ID", "Identifier"),
    ("IEEE", "Institute of Electrical and Electronics Engineers"),
    ("IS", "Information Systems"),
    ("JSON", "JavaScript Object Notation"),
    ("LIWC", "Linguistic Inquiry and Word Count"),
    ("LLM", "Large Language Model"),
    ("LSTM", "Long Short-Term Memory"),
    ("METEOR", "Metric for Evaluation of Translation with Explicit Ordering"),
    ("ML", "Machine Learning"),
    ("NLI", "Natural Language Inference"),
    ("NLP", "Natural Language Processing"),
    ("NLTK", "Natural Language Toolkit"),
    ("ORM", "Object-Relational Mapping"),
    ("OS", "Operating System"),
    ("P50 / P95", "50th / 95th Percentile (latency)"),
    ("pCTR", "Predicted Click-Through Rate"),
    ("POS", "Part of Speech"),
    ("PRINCE2", "Projects IN Controlled Environments"),
    ("RAM", "Random Access Memory"),
    ("REST", "Representational State Transfer"),
    ("RMSE", "Root Mean Square Error"),
    ("RNN", "Recurrent Neural Network"),
    ("ROC", "Receiver Operating Characteristic"),
    ("ROUGE", "Recall-Oriented Understudy for Gisting Evaluation"),
    ("RQ", "Research Question"),
    ("SDK", "Software Development Kit"),
    ("SE", "Software Engineering"),
    ("SEO", "Search Engine Optimisation"),
    ("SOT", "Source of Truth"),
    ("SRS", "System Requirements Specification"),
    ("SSD", "Solid-State Drive"),
    ("TER", "Translation Edit Rate"),
    ("UI", "User Interface"),
    ("UML", "Unified Modelling Language"),
    ("VADER", "Valence Aware Dictionary and sEntiment Reasoner"),
    ("VRAM", "Video Random Access Memory"),
    ("XSS", "Cross-Site Scripting"),
    ("YTO", "YouTube Title Optimizer"),
]

log_lines = []


def log(*a):
    log_lines.append(" ".join(str(x) for x in a))


# --------------------------------------------------------------------------
# Safe text helpers (never touch image-bearing runs)
# --------------------------------------------------------------------------
def safe_run_sub(r, fn):
    """Apply fn(text)->text to a run only if it has text and the result differs."""
    if not r.text:
        return
    new = fn(r.text)
    if new != r.text:
        r.text = new


def all_runs(body):
    for r in body.iter(qn("w:r")):
        yield Run(r, None)


def para_text(p_el):
    return "".join(t.text or "" for t in p_el.iter(qn("w:t")))


# --------------------------------------------------------------------------
# Cross-reference remapping (single combined regex pass)
# --------------------------------------------------------------------------
NUM = r"\d+(?:\.\d+)+"
SEP = r"(?:\s*(?:–|-|/|,|and|through)\s*)"
RE_MAIN = re.compile(
    r"(?P<tl>Chapter 1 \(Introduction\), Chapter 2 \(Literature Review\), "
    r"Chapter 3 \(Methodology\))"
    r"|(?P<ch>\b(?:Chapters?|Ch\.)\s*\d+(?:\s*(?:–|-|and|through|to)\s*\d+)*)"
    r"|(?P<sec>(?:\bSections?\s+|§\s*)" + NUM + r"(?:" + SEP + NUM + r")*)"
    r"|(?P<tf>\b(?:Tables?|Figures?|Listings?)\s+\d+\.\d+[a-z]?)"
    r"|(?P<obj>\b1\.7\.\d\b)"
)
EXTERNAL_CTX = re.compile(r"SOT|PLAN_IMPLEMENTATION|SOURCE_OF_TRUTH")


def _map_chapter(n, before):
    if n == 1:
        return 2 if "objective" in before.lower() else 1
    if 2 <= n <= 7:
        return n + 1
    return n


def _map_sec_token(tok):
    parts = tok.split(".")
    c = int(parts[0])
    if c == 1 and len(parts) >= 2:
        s = int(parts[1])
        if s == 7 and len(parts) >= 3:
            return "2." + ".".join(parts[2:])
        if s >= 8:
            parts[1] = str(s - 1)
        return ".".join(parts)
    if 2 <= c <= 7:
        parts[0] = str(c + 1)
    return ".".join(parts)


def _cb(m):
    s = m.group(0)
    before = m.string[max(0, m.start() - 45):m.start()]
    if m.group("tl"):
        return ("Chapter 1 (Introduction), Chapter 2 (Objectives), "
                "Chapter 3 (Literature Review), Chapter 4 (Methodology)")
    if m.group("ch"):
        return re.sub(r"\d+", lambda x: str(_map_chapter(int(x.group(0)), before)), s)
    if m.group("sec"):
        if s.startswith("§") and EXTERNAL_CTX.search(m.string[max(0, m.start() - 40):m.start()]):
            return s
        kw = re.match(r"(?:Sections?\s+|§\s*)", s).group(0)
        rest = s[len(kw):]
        if rest == "1.7":
            return "Chapter 2"
        return kw + re.sub(NUM, lambda x: _map_sec_token(x.group(0)), rest)
    if m.group("tf"):
        is_table = s.startswith("Table")

        def tf(x):
            c, q = int(x.group(1)), int(x.group(2))
            if is_table and c == 3:  # old Ch3 gains a new first table (uncaptioned one)
                q += 1
            if 2 <= c <= 7:
                c += 1
            return f"{c}.{q}"
        return re.sub(r"(\d+)\.(\d+)", tf, s)
    if m.group("obj"):
        return "2." + s.split(".")[2]
    return s


def remap_text(t):
    return RE_MAIN.sub(_cb, t)


def remap_paragraph(p_el):
    """Remap cross-refs using whole-paragraph text; write edits back into runs."""
    runs = [Run(r, None) for r in p_el.iter(qn("w:r"))]
    texts = [r.text for r in runs]
    full = "".join(texts)
    if not full:
        return
    edits = [(m.start(), m.end(), _cb(m)) for m in RE_MAIN.finditer(full)]
    edits = [e for e in edits if full[e[0]:e[1]] != e[2]]
    if not edits:
        return
    starts, pos = [], 0
    for t in texts:
        starts.append(pos)
        pos += len(t)
    new_texts = list(texts)
    for s_, e_, new in reversed(edits):
        first = True
        for i, (rs, rt) in enumerate(zip(starts, texts)):
            re_ = rs + len(rt)
            if re_ <= s_ or rs >= e_:
                continue
            ls, le = max(s_, rs) - rs, min(e_, re_) - rs
            if first:
                new_texts[i] = new_texts[i][:ls] + new + new_texts[i][le:]
                first = False
            else:
                new_texts[i] = new_texts[i][:ls] + new_texts[i][le:]
    for r, old, new in zip(runs, texts, new_texts):
        if new != old:  # never reassign unchanged runs (protects image-bearing runs)
            r.text = new


def remap_all_refs(doc):
    body = doc.element.body
    before_pt = {p: para_text(p) for p in body.iter(qn("w:p"))}
    for p in body.iter(qn("w:p")):
        remap_paragraph(p)
    bad = 0
    for p in body.iter(qn("w:p")):
        if remap_text(before_pt[p]) != para_text(p):
            bad += 1
            log("REF MISMATCH:", repr(before_pt[p][:100]), "=>", repr(para_text(p)[:100]))
    log("paragraphs whose cross-refs did not map cleanly:", bad)


# --------------------------------------------------------------------------
# Heading text helpers
# --------------------------------------------------------------------------
PROPER = {"Peffers", "Agile", "Scrum", "Kaggle", "Llama", "Pydantic"}
NUM_PREFIX = re.compile(r"^\d+(?:\.\d+){0,3}\s+")
CODE_RE = re.compile(r"^([A-Za-z]{1,4}\d*[a-z]?)([:;])\s*(.+)$")


def _case_part(pt):
    core = re.sub(r"^\W+|\W+$", "", pt)
    core_ns = core.rstrip("’'s") if core.endswith(("’s", "'s")) else core
    keep = (
        not core
        or any(c.isdigit() for c in core)
        or (core.isalpha() and core.isupper())
        or re.search(r"[a-z][A-Z]", core)
        or re.search(r"[A-Z]{2,}", core)
        or core in PROPER
        or core_ns.strip("’'") in PROPER
    )
    return pt if keep else pt.lower()


def sentence_case(title):
    words = title.split(" ")
    out = []
    for w in words:
        parts = re.split(r"([-–/])", w)
        out.append("".join(p if p in ("-", "–", "/") else _case_part(p) for p in parts))
    s = " ".join(out)
    for i, ch in enumerate(s):
        if ch.isalpha():
            s = s[:i] + ch.upper() + s[i + 1:]
            break
    return s


def heading_title(text):
    """Strip number prefix; return sentence-cased title, keeping short codes."""
    t = NUM_PREFIX.sub("", text.strip())
    m = CODE_RE.match(t)
    if m and not re.match(r"^(Objective|Note|Study)\b", t):
        return f"{m.group(1)}{m.group(2)} {sentence_case(m.group(3))}"
    return sentence_case(t)


def set_heading_text(p, text, bold, caps=False):
    assert not p._p.findall(".//" + qn("w:drawing")), "heading contains a drawing"
    for r in list(p._p.iter(qn("w:r"))):
        r.getparent().remove(r)
    for h in list(p._p.findall(qn("w:hyperlink"))):
        p._p.remove(h)
    run = p.add_run(text)
    run.bold = bold
    run.italic = False
    run.font.all_caps = caps
    run.font.name = FONT
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0, 0, 0)


# --------------------------------------------------------------------------
# Restructuring
# --------------------------------------------------------------------------
def is_style(p_el, pmap, *names):
    p = pmap.get(p_el)
    return p is not None and p.style.name in names


def restructure(doc):
    body = doc.element.body
    pmap = {p._p: p for p in doc.paragraphs}
    kids = list(body)

    # 0. delete old title block (3 metadata paras, TOC sdt, cover paragraphs) up to first H1
    first_h1 = next(k for k in kids if is_style(k, pmap, "Heading 1"))
    for k in kids[:kids.index(first_h1)]:
        body.remove(k)
    log("removed old title block / TOC elements up to first Heading 1")

    kids = list(body)

    # 1. extract per-chapter References blocks
    groups = []  # (old_chapter_title, [elements])
    cur_chapter = None
    i = 0
    while i < len(kids):
        k = kids[i]
        p = pmap.get(k)
        if p is not None and p.style.name == "Heading 1":
            cur_chapter = re.sub(r"^Chapter \d+:\s*", "", p.text.strip())
        if p is not None and p.style.name == "Heading 2" and p.text.strip() == "References":
            j = i + 1
            block = [k]
            while j < len(kids):
                kj = kids[j]
                pj = pmap.get(kj)
                if kj.tag != qn("w:p") and kj.tag != qn("w:tbl"):
                    break
                if pj is not None and pj.style.name == "Heading 1":
                    break
                block.append(kj)
                j += 1
            entries = [e for e in block[1:]]
            while entries and not para_text(entries[-1]).strip():
                entries.pop()
            groups.append((cur_chapter, entries))
            for e in block:
                body.remove(e)
            i = j
            continue
        i += 1
    log("reference groups extracted:", [(g[0], len(g[1])) for g in groups])

    # 2. move '1.7 Research Objectives' block into its own chapter before Literature Review
    kids = list(body)
    start = next(k for k in kids if is_style(k, pmap, "Heading 2")
                 and pmap[k].text.startswith("1.7 Research Objectives"))
    end = next(k for k in kids[kids.index(start) + 1:]
               if is_style(k, pmap, "Heading 2"))
    block = kids[kids.index(start):kids.index(end)]
    assert not any(b.tag == qn("w:tbl") for b in block), "table inside objectives block"
    assert not any(b.findall(".//" + qn("w:drawing")) for b in block)
    lit = next(k for k in kids if is_style(k, pmap, "Heading 1")
               and pmap[k].text.strip().endswith("Literature Review"))
    for b in block:
        body.remove(b)
        lit.addprevious(b)
    # old H2 -> new H1 ; its H3 children -> H2
    hp = pmap[start]
    hp.style = doc.styles["Heading 1"]
    hp.text = "Chapter 2: Objectives"  # heading paragraph: no image possible (asserted)
    for b in block[1:]:
        pb = pmap.get(b)
        if pb is not None and pb.style.name == "Heading 3":
            pb.style = doc.styles["Heading 2"]
    log("objectives block moved:", len(block), "elements")
    return groups


def renumber_headings(doc):
    """Normalise every heading: number, case, bold. Returns [(level, num, text)]."""
    body = doc.element.body
    pmap = {p._p: p for p in doc.paragraphs}
    heads = []
    n = [0, 0, 0, 0]
    chapter_titles = {}
    for k in list(body):
        p = pmap.get(k)
        if p is None:
            continue
        st = p.style.name
        if st == "Heading 1":
            old = re.sub(r"^Chapter \d+:\s*", "", p.text.strip())
            new_num, title = NEW_CHAPTERS[old]
            n = [new_num, 0, 0, 0]
            set_heading_text(p, f"{new_num} {title}", True, caps=True)
            heads.append((1, str(new_num), title))
        elif st == "Heading 2":
            n[1] += 1
            n[2] = n[3] = 0
            title = heading_title(p.text)
            num = f"{n[0]}.{n[1]}"
            set_heading_text(p, f"{num} {title}", True)
            heads.append((2, num, title))
        elif st == "Heading 3":
            n[2] += 1
            n[3] = 0
            title = heading_title(p.text)
            num = f"{n[0]}.{n[1]}.{n[2]}"
            set_heading_text(p, f"{num} {title}", False)
            heads.append((3, num, title))
        elif st == "Heading 4":
            assert n[2] > 0, "Heading 4 without Heading 3 parent: " + p.text
            n[3] += 1
            title = heading_title(p.text)
            num = f"{n[0]}.{n[1]}.{n[2]}.{n[3]}"
            set_heading_text(p, f"{num} {title}", False)
            heads.append((4, num, title))
    for lv, num, t in heads:
        log("HEAD", lv, num, t)
    return heads


# --------------------------------------------------------------------------
# Styles, fonts, spacing
# --------------------------------------------------------------------------
def _fix_rfonts(rpr, name):
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.insert(0, rf)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        rf.attrib.pop(qn(a), None)
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(a), name)


def style_setup(doc):
    styles = doc.styles.element
    dd = styles.find(qn("w:docDefaults"))
    if dd is not None:
        rpr = dd.find(qn("w:rPrDefault") + "/" + qn("w:rPr"))
        if rpr is not None:
            _fix_rfonts(rpr, FONT)
    mono = {"Source Code"}
    for st in doc.styles:
        if st.type != WD_STYLE_TYPE.PARAGRAPH:
            continue
        name = st.name
        f = st.font
        if name in mono:
            f.size = Pt(10)
            st.paragraph_format.line_spacing = 1.0
            st.paragraph_format.space_after = Pt(0)
            continue
        f.name = FONT
        _fix_rfonts(st.element.get_or_add_rPr(), FONT)
        f.size = Pt(12)
        f.color.rgb = RGBColor(0, 0, 0)
        pf = st.paragraph_format
        pf.line_spacing = 1.5
        if name.startswith("Heading"):
            f.italic = False
            f.bold = name in ("Heading 1", "Heading 2")
            pf.space_before = Pt(12)
            pf.space_after = Pt(6)
            pf.keep_with_next = True
            if name == "Heading 1":
                pf.page_break_before = True
        elif name in ("Body Text", "First Paragraph"):
            pf.space_before = Pt(0)
            pf.space_after = Pt(6)
            pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        elif name in ("Image Caption", "Table Caption"):
            f.italic = False
            f.bold = False
    # Captioned Figure paragraph centred, keep with caption
    for nm in ("Captioned Figure", "Image Caption"):
        try:
            doc.styles[nm].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        except KeyError:
            pass
    try:
        doc.styles["Captioned Figure"].paragraph_format.keep_with_next = True
    except KeyError:
        pass
    # remove explicit run-level font/size overrides left over from generation
    for r in doc.element.body.iter(qn("w:r")):
        rpr = r.find(qn("w:rPr"))
        if rpr is None:
            continue
        rs = rpr.find(qn("w:rStyle"))
        if rs is not None and rs.get(qn("w:val")) in ("VerbatimChar", "Verbatim Char"):
            continue
        for tag in ("w:sz", "w:szCs"):
            e = rpr.find(qn(tag))
            if e is not None:
                rpr.remove(e)
        rf = rpr.find(qn("w:rFonts"))
        if rf is not None:
            rpr.remove(rf)


def page_setup(doc):
    for s in doc.sections:
        s.page_width, s.page_height = Cm(A4_W_CM), Cm(A4_H_CM)
        s.left_margin, s.right_margin = Cm(LEFT_CM), Cm(RIGHT_CM)
        s.top_margin, s.bottom_margin = Cm(TOP_CM), Cm(BOTTOM_CM)
        s.header_distance = s.footer_distance = Cm(1.25)
        # drop pandoc header/footer references
        for tag in ("w:headerReference", "w:footerReference"):
            for e in s._sectPr.findall(qn(tag)):
                s._sectPr.remove(e)


# --------------------------------------------------------------------------
# Tables, figures, captions
# --------------------------------------------------------------------------
def fix_tables(doc):
    n_scaled = 0
    for tbl in doc.tables:
        t = tbl._tbl
        # shading off
        for shd in t.iter(qn("w:shd")):
            shd.getparent().remove(shd)
        grid = t.find(qn("w:tblGrid"))
        cols = grid.findall(qn("w:gridCol")) if grid is not None else []
        widths = [int(c.get(qn("w:w"), 0)) for c in cols]
        total = sum(widths)
        if cols and total > 0:
            factor = TEXT_W_TW / total
            new = [int(w * factor) for w in widths]
            for c, w in zip(cols, new):
                c.set(qn("w:w"), str(w))
            for tr in t.findall(qn("w:tr")):
                tcs = tr.findall(qn("w:tc"))
                for idx, tc in enumerate(tcs):
                    tcpr = tc.find(qn("w:tcPr"))
                    if tcpr is None:
                        continue
                    tcw = tcpr.find(qn("w:tcW"))
                    if tcw is not None and idx < len(new):
                        span = tcpr.find(qn("w:gridSpan"))
                        sp = int(span.get(qn("w:val"))) if span is not None else 1
                        tcw.set(qn("w:type"), "dxa")
                        tcw.set(qn("w:w"), str(sum(new[idx:idx + sp])))
            n_scaled += 1
        tblPr = t.tblPr
        tw = tblPr.find(qn("w:tblW"))
        if tw is None:
            tw = OxmlElement("w:tblW")
            tblPr.append(tw)
        tw.set(qn("w:type"), "dxa")
        tw.set(qn("w:w"), str(TEXT_W_TW))
        # paragraphs inside cells: single spaced, no left-over sizes
        for p in t.iter(qn("w:p")):
            pp = p.find(qn("w:pPr"))
    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.line_spacing = 1.0
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        # repeat header row across pages
        first = tbl.rows[0]._tr
        trpr = first.get_or_add_trPr()
        if trpr.find(qn("w:tblHeader")) is None:
            trpr.append(OxmlElement("w:tblHeader"))
    log("tables scaled to text width:", n_scaled, "of", len(doc.tables))


def fix_images(doc):
    max_w = Cm(TEXT_W_CM)
    max_h = Cm(19)
    n = 0
    for shp in doc.inline_shapes:
        w, h = shp.width, shp.height
        ratio = min(1.0, max_w / w, max_h / h)
        if ratio < 1.0:
            shp.width, shp.height = int(w * ratio), int(h * ratio)
            n += 1
    log("images scaled to fit:", n, "of", len(doc.inline_shapes))


NEW_TABLE_CAPTIONS = [
    "Table 1.1: Hardware resource requirements",
    "Table 1.2: Software resource requirements",
    "Table 1.3: In-scope items",
    "Table 1.4: Out-of-scope items",
    "Table 4.1: Alternative research strategies considered and rejected",
]


def fix_captions(doc):
    body = doc.element.body
    pmap = {p._p: p for p in doc.paragraphs}
    kids = list(body)
    missing = []
    for idx, k in enumerate(kids):
        if k.tag == qn("w:tbl"):
            pp = pmap.get(kids[idx - 1])
            if pp is None or not re.match(r"^Table \d+\.\d+", pp.text):
                missing.append(k)
            else:
                pp.paragraph_format.keep_with_next = True
                pp.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for idx, k in enumerate(kids):
        if k.tag == qn("w:tbl") and idx + 1 < len(kids) and kids[idx + 1] in pmap:
            pmap[kids[idx + 1]].paragraph_format.space_before = Pt(10)
    assert len(missing) == len(NEW_TABLE_CAPTIONS), f"{len(missing)} uncaptioned tables"
    for tbl_el, cap in zip(missing, NEW_TABLE_CAPTIONS):
        p = doc.add_paragraph(cap, style="Body Text")
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        tbl_el.addprevious(p._p)
        log("ADDED CAPTION:", cap)


# --------------------------------------------------------------------------
# Front matter construction
# --------------------------------------------------------------------------
def mk(doc, text="", *, bold=False, size=12, align=None, caps=False, before=0, after=0,
       line=1.5, keep_next=False, page_break=False, italic=False, highlight=False):
    p = doc.add_paragraph(style="Normal")
    pf = p.paragraph_format
    pf.space_before, pf.space_after, pf.line_spacing = Pt(before), Pt(after), line
    pf.keep_with_next = keep_next
    pf.page_break_before = page_break
    if align is not None:
        pf.alignment = align
    if text:
        add_text(p, text, bold=bold, size=size, caps=caps, italic=italic, highlight=highlight)
    return p


def add_text(p, text, *, bold=False, size=12, caps=False, italic=False, highlight=False):
    """Add text; segments in [[...]] are highlighted placeholders."""
    for seg in re.split(r"(\[\[.*?\]\])", text):
        if not seg:
            continue
        hl = seg.startswith("[[")
        r = p.add_run(seg[2:-2] if hl else seg)
        r.bold, r.italic, r.font.size = bold, italic, Pt(size)
        r.font.all_caps = caps
        r.font.name = FONT
        if hl or highlight:
            rpr = r._r.get_or_add_rPr()
            h = OxmlElement("w:highlight")
            h.set(qn("w:val"), "yellow")
            rpr.append(h)


def sect_break_par(doc, sectpr_tpl):
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.space_after = Pt(0)
    sp = copy.deepcopy(sectpr_tpl)
    for tag in ("w:headerReference", "w:footerReference", "w:pgNumType", "w:titlePg", "w:type"):
        for e in sp.findall(qn(tag)):
            sp.remove(e)
    p._p.get_or_add_pPr().append(sp)
    return p


def tab_line(doc, level_indent_cm, left_text, page, *, hanging=None, bold=False):
    p = doc.add_paragraph(style="Normal")
    pf = p.paragraph_format
    pf.line_spacing = 1.15
    pf.space_after = Pt(2)
    pf.left_indent = Cm(level_indent_cm + (hanging or 0))
    if hanging:
        pf.first_line_indent = Cm(-hanging)
        pf.tab_stops.add_tab_stop(Cm(level_indent_cm + hanging), WD_TAB_ALIGNMENT.LEFT)
    pf.tab_stops.add_tab_stop(Cm(TEXT_W_CM), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    r = p.add_run(left_text + "\t" + (page or ""))
    r.bold = bold
    r.font.name = FONT
    r.font.size = Pt(12)
    return p


def build_front_matter(doc, heads, pages):
    """Returns list of body elements in order (already created at end of body)."""
    pg = pages
    els = []
    add = lambda p: els.append(p._p) or p
    C = WD_ALIGN_PARAGRAPH.CENTER

    # ---- Cover (Appendix I) ----
    add(mk(doc, TITLE, bold=True, size=16, align=C, caps=True, before=90))
    add(mk(doc, SUBTITLE, size=14, align=C, before=6))
    add(mk(doc, AUTHOR, bold=True, size=14, align=C, caps=True, before=150))
    add(mk(doc, f"Student ID: {STUDENT_ID}", size=14, align=C))
    add(mk(doc, DEGREE, size=14, align=C, before=12))
    add(mk(doc, f"Department of [[{PLACEHOLDER_DEPT[1:-1]}]]", size=14, align=C, before=110))
    add(mk(doc, FACULTY, size=14, align=C))
    add(mk(doc, "NSBM Green University", size=14, align=C))
    add(mk(doc, "Sri Lanka", size=14, align=C))
    add(mk(doc, SUBMITTED, size=14, align=C, before=18))
    tpl_sectpr = doc.element.body.find(qn("w:sectPr"))
    add(sect_break_par(doc, tpl_sectpr))  # end of section 1 (cover)

    # ---- Inner title page (Appendix II): page i, number hidden ----
    add(mk(doc, TITLE, bold=True, size=16, align=C, caps=True, before=90))
    add(mk(doc, SUBTITLE, size=14, align=C, before=6))
    add(mk(doc, "A thesis submitted to NSBM Green University for the degree of",
           size=14, align=C, before=60))
    add(mk(doc, DEGREE, size=14, align=C))
    add(mk(doc, "By", size=14, align=C, before=30))
    add(mk(doc, AUTHOR, bold=True, size=14, align=C, caps=True, before=6))
    add(mk(doc, f"Student ID: {STUDENT_ID}", size=14, align=C))
    add(mk(doc, f"Department of [[{PLACEHOLDER_DEPT[1:-1]}]]", size=14, align=C, before=90))
    add(mk(doc, FACULTY, size=14, align=C))
    add(mk(doc, "NSBM Green University", size=14, align=C))
    add(mk(doc, "Sri Lanka", size=14, align=C))
    add(mk(doc, SUBMITTED, size=14, align=C, before=18))

    # ---- Declaration (Appendix III) ----
    add(mk(doc, "DECLARATION", bold=True, align=C, page_break=True, after=12))
    add(mk(doc, f"I declare that the content of this undergraduate thesis titled "
                f"“{TITLE}” is my own work and this dissertation does not "
                f"incorporate without acknowledgement any material previously submitted "
                f"for any other degree in any university or institution of higher "
                f"learning.", align=WD_ALIGN_PARAGRAPH.JUSTIFY))
    add(mk(doc, "Signature: …………………………"
                "………………………………",
           before=24))
    add(mk(doc, f"Name: {AUTHOR} (Student ID: {STUDENT_ID})"))
    add(mk(doc, "Date: ……………………………"
                "………"))
    add(mk(doc, "Signature of the Supervisors", bold=True, before=30, keep_next=True))
    add(mk(doc, "……………………………"
                "………………………", before=18,
           keep_next=True))
    add(mk(doc, f"Ms. Nimesha [[{PLACEHOLDER_SUP[1:-1]}]]", keep_next=True))
    add(mk(doc, "Principal Supervisor", keep_next=True))
    add(mk(doc, "[[Senior Lecturer / Lecturer]]", keep_next=True))
    add(mk(doc, f"Department of [[{PLACEHOLDER_DEPT[1:-1]}]],", keep_next=True))
    add(mk(doc, "NSBM Green University", keep_next=True))
    add(mk(doc, "Date: ………………………………",
           before=12))

    # ---- Acknowledgement ----
    add(mk(doc, "ACKNOWLEDGEMENT", bold=True, align=C, page_break=True, after=12))
    for para in ACK_PARAS:
        add(mk(doc, para, align=WD_ALIGN_PARAGRAPH.JUSTIFY, after=6))

    # ---- Abstract ----
    add(mk(doc, "ABSTRACT", bold=True, align=C, page_break=True, after=12))
    add(mk(doc, ABSTRACT, align=WD_ALIGN_PARAGRAPH.JUSTIFY))

    # ---- Table of Contents ----
    add(mk(doc, "TABLE OF CONTENTS", bold=True, align=C, page_break=True, after=12))
    fm = pg.get("front", {})
    for name in ("Declaration", "Acknowledgement", "Abstract", "Table of Contents",
                 "List of Figures", "List of Tables", "List of Abbreviations"):
        add(tab_line(doc, 0, name, fm.get(name, "")))
    hp = pg.get("head", {})
    for lv, num, title in heads:
        indent = {1: 0, 2: 0.6, 3: 1.4, 4: 2.4}[lv]
        hang = {1: 0.9, 2: 1.0, 3: 1.4, 4: 1.6}[lv]
        add(tab_line(doc, indent, f"{num}\t{title}", hp.get(num, ""), hanging=hang,
                     bold=(lv == 1)))
    add(tab_line(doc, 0, "References", hp.get("References", ""), bold=True))

    # ---- List of Figures / Tables ----
    caps = collect_captions(doc)
    add(mk(doc, "LIST OF FIGURES", bold=True, align=C, page_break=True, after=12))
    add(mk(doc, "Page", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True))
    for label, text in caps["Figure"]:
        add(tab_line(doc, 0, f"{label}\t{text}", pg.get("cap", {}).get(label, ""),
                     hanging=2.6))
    add(mk(doc, "LIST OF TABLES", bold=True, align=C, page_break=True, after=12))
    add(mk(doc, "Page", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True))
    for label, text in caps["Table"]:
        add(tab_line(doc, 0, f"{label}\t{text}", pg.get("cap", {}).get(label, ""),
                     hanging=2.4))

    # ---- List of Abbreviations ----
    add(mk(doc, "LIST OF ABBREVIATIONS", bold=True, align=C, page_break=True, after=12))
    for ab, meaning in sorted(ABBREVIATIONS, key=lambda x: x[0].lower()):
        p = mk(doc, "", line=1.15, after=3)
        p.paragraph_format.left_indent = Cm(3.0)
        p.paragraph_format.first_line_indent = Cm(-3.0)
        p.paragraph_format.tab_stops.add_tab_stop(Cm(3.0), WD_TAB_ALIGNMENT.LEFT)
        add_text(p, ab, bold=True)
        add_text(p, "\t" + meaning)
        add(p)
    add(sect_break_par(doc, tpl_sectpr))  # end of section 2 (roman front matter)
    return els


def collect_captions(doc):
    """Captions in document order: Table caption paragraphs / Figure image captions."""
    tables, figures, seen = [], [], set()
    for p in doc.paragraphs:
        m = re.match(r"^(Table \d+\.\d+):\s*(.+)$", p.text)
        if m and p.style.name != "Captioned Figure" and m.group(1) not in seen:
            seen.add(m.group(1))
            tables.append((m.group(1), m.group(2).strip()))
            continue
        m = re.match(r"^(Figure \d+\.\d+):\s*(.+)$", p.text)
        if m and p.style.name == "Image Caption" and m.group(1) not in seen:
            seen.add(m.group(1))
            figures.append((m.group(1), m.group(2).strip()))
    return {"Table": tables, "Figure": figures}


# --------------------------------------------------------------------------
# References section
# --------------------------------------------------------------------------
def build_references(doc, groups):
    body = doc.element.body
    sect = body.find(qn("w:sectPr"))

    def put(el):
        sect.addprevious(el)

    h = doc.add_paragraph(style="Heading 1")
    set_heading_text(h, "References", True, caps=True)
    put(h._p)
    for old_title, entries in groups:
        new_num, new_title = NEW_CHAPTERS[old_title]
        lab = mk(doc, f"References cited in Chapter {new_num}: {new_title}", bold=True,
                 before=12, keep_next=True)
        put(lab._p)
        for e in entries:
            put(e)
        for e in entries:
            if e.tag == qn("w:p"):
                pf = Paragraph(e, doc._body).paragraph_format
                pf.left_indent = Cm(1.0)
                pf.first_line_indent = Cm(-1.0)


# --------------------------------------------------------------------------
# Section / pagination
# --------------------------------------------------------------------------
def add_page_field(footer):
    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in list(p.runs):
        r._r.getparent().remove(r._r)

    def fld(kind, text=None):
        r = p.add_run()
        r.font.name, r.font.size = FONT, Pt(12)
        if kind:
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), kind)
            r._r.append(fc)
        else:
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = text
            r._r.append(it)

    fld("begin")
    fld(None, " PAGE ")
    fld("separate")
    r = p.add_run("1")
    r.font.name, r.font.size = FONT, Pt(12)
    fld("end")


def set_pgnum(section, fmt, start):
    sp = section._sectPr
    for e in sp.findall(qn("w:pgNumType")):
        sp.remove(e)
    pn = OxmlElement("w:pgNumType")
    pn.set(qn("w:fmt"), fmt)
    pn.set(qn("w:start"), str(start))
    cols = sp.find(qn("w:cols"))
    if cols is not None:
        cols.addprevious(pn)
    else:
        sp.find(qn("w:pgMar")).addnext(pn)


def paginate(path):
    doc = Document(str(path))
    secs = doc.sections
    assert len(secs) == 3, f"expected 3 sections, got {len(secs)}"
    # S1: cover, nothing. S2: roman, first page (inner title) hidden. S3: arabic from 1.
    s2, s3 = secs[1], secs[2]
    for e in list(s2._sectPr.findall(qn("w:titlePg"))):
        s2._sectPr.remove(e)
    s2.different_first_page_header_footer = True
    s2.footer.is_linked_to_previous = False
    add_page_field(s2.footer)
    s2.first_page_footer.is_linked_to_previous = False
    set_pgnum(s2, "lowerRoman", 1)
    s3.different_first_page_header_footer = False
    s3.footer.is_linked_to_previous = False
    add_page_field(s3.footer)
    set_pgnum(s3, "decimal", 1)
    doc.save(str(path))


# --------------------------------------------------------------------------
def main():
    pages = json.loads(PAGE_MAP.read_text()) if PAGE_MAP.exists() else {}
    doc = Document(str(SOURCE))
    n_img_before = len(doc.inline_shapes)

    remap_all_refs(doc)
    groups = restructure(doc)
    heads = renumber_headings(doc)
    style_setup(doc)
    page_setup(doc)
    fix_tables(doc)
    fix_images(doc)
    fix_captions(doc)

    build_references(doc, groups)
    # front matter must be built after all captions exist (lists), then inserted
    els = build_front_matter(doc, heads, pages)
    first_h1 = next(p for p in doc.paragraphs if p.style.name == "Heading 1")._p
    for el in els:
        el.getparent().remove(el)
        first_h1.addprevious(el)

    assert len(doc.inline_shapes) == n_img_before, "image count changed"
    doc.core_properties.title = TITLE
    doc.core_properties.author = AUTHOR
    doc.save(str(OUTPUT))
    paginate(OUTPUT)
    LOG.write_text("\n".join(log_lines), encoding="utf-8")
    print("saved", OUTPUT, "| images:", len(Document(str(OUTPUT)).inline_shapes),
          "(source", n_img_before, ")")


if __name__ == "__main__":
    main()
