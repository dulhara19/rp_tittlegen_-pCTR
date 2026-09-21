"""Prove the reformat changed presentation only: bag-of-text diff, image count,
caption/heading numbering, page setup, fonts."""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

THESIS = Path(__file__).resolve().parent.parent
OLD = THESIS / "bckp" / "Pathiraja_29071_Final_Thesis.docx"
NEW = THESIS / "Pathiraja_29071_Final_Thesis_NEW.docx"


def norm(s):
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"^\d+(\.\d+){0,3}\s+", "", s)
    s = re.sub(r"^chapter \d+:\s*", "", s)
    s = re.sub(r"chapters? \d+(\s*(–|-|and|through)\s*\d+)?", "chapter #", s)
    s = re.sub(r"ch\. ?\d+(–\d+)?", "ch #", s)
    s = re.sub(r"§\s*\d+(\.\d+)*([–-]\d+(\.\d+)*)?", "§#", s)
    s = re.sub(r"\bsections? \d+(\.\d+)*", "section #", s)
    s = re.sub(r"\b(table|figure|listing)s? \d+\.\d+[a-z]?\b", r"\1 #", s)
    s = re.sub(r"\b1\.7\.\d\b|\b2\.\d\b", "#", s)
    s = re.sub(r"\d+(\.\d+)+", "#", s)
    s = re.sub(r"\s", "", s)
    return s


def texts(path, is_new=False):
    d = Document(str(path))
    paras = list(d.paragraphs)
    i = next(k for k, p in enumerate(paras) if p.style.name == "Heading 1")
    paras = paras[i:]  # drop title block / generated front matter
    if is_new:
        paras = [p for p in paras if not p.text.startswith("References cited in Chapter")]
    out = [p.text for p in paras if not p.style.name.startswith("Heading")]
    d._heads = [p.text for p in paras if p.style.name.startswith("Heading")]
    for t in d.tables:
        for row in t.rows:
            seen = set()
            for c in row.cells:
                if id(c._tc) in seen:
                    continue
                seen.add(id(c._tc))
                out.extend(p.text for p in c.paragraphs)
    return d, [t for t in out if t.strip()]


od, old = texts(OLD)
nd, new = texts(NEW, True)
print("images old/new:", len(od.inline_shapes), len(nd.inline_shapes))
print("tables old/new:", len(od.tables), len(nd.tables))
ob, nb = Counter(norm(t) for t in old), Counter(norm(t) for t in new)
only_old, only_new = ob - nb, nb - ob
print("\n== only in OLD (%d) ==" % sum(only_old.values()))
oldmap = {norm(t): t for t in old}
for k, n in only_old.items():
    print("  -", oldmap.get(k, k)[:110], f"(x{n})")
print("\n== only in NEW (%d) ==" % sum(only_new.values()))
newmap = {norm(t): t for t in new}
for k, n in only_new.items():
    print("  +", newmap.get(k, k)[:110], f"(x{n})")

# caption sequences
print("\n== caption numbering ==")
caps = defaultdict(list)
for p in nd.paragraphs:
    m = re.match(r"^(Table|Figure) (\d+)\.(\d+)([a-z]?):", p.text)
    if m and p.style.name != "Captioned Figure":
        (caps[(m.group(1), int(m.group(2)))].append((int(m.group(3)), m.group(4))) if (int(m.group(3)), m.group(4)) not in caps[(m.group(1), int(m.group(2)))] else None)
ok = True
for k in sorted(caps):
    seq = [s for s, _ in caps[k]]
    good = seq == list(range(1, len(seq) + 1)) and not any(x for _, x in caps[k])
    ok &= good
    print(" ", k, seq, "OK" if good else "BAD")
print("caption numbering all OK:", ok)

# headings
print("\n== heading sequence ==")
bad = 0
cnt = [0, 0, 0, 0]
for p in nd.paragraphs:
    st = p.style.name
    if st in ("Heading 1", "Heading 2", "Heading 3", "Heading 4"):
        m = re.match(r"^(\d+(?:\.\d+)*)\s", p.text)
        if not m:
            print("  unnumbered:", p.text)
            continue
        parts = [int(x) for x in m.group(1).split(".")]
        lv = int(st[-1])
        if len(parts) != lv:
            bad += 1
            print("  level mismatch:", p.text)
        cnt = (cnt[:lv - 1] + [0] * 4)[:lv - 1] + [cnt[lv - 1] + 1 if len(cnt) >= lv else 1]
        cnt = cnt + [0] * (4 - len(cnt))
print("heading level mismatches:", bad)

# page setup / sections
print("\n== sections ==")
for i, s in enumerate(nd.sections):
    pg = s._sectPr.find(qn("w:pgNumType"))
    print(f"  S{i+1}: {s.page_width.cm:.2f}x{s.page_height.cm:.2f}cm  L{s.left_margin.inches:.2f} "
          f"R{s.right_margin.inches:.2f} T{s.top_margin.inches:.2f} B{s.bottom_margin.inches:.2f}  "
          f"pgNum={dict(pg.attrib) if pg is not None else None}")

# fonts
sizes = Counter()
for st in nd.styles:
    if st.type == 1 and st.name in ("Normal", "Body Text", "First Paragraph", "Compact",
                                    "Heading 1", "Heading 2", "Heading 3", "Heading 4",
                                    "Image Caption"):
        sizes[(st.name, st.font.name, st.font.size.pt if st.font.size else None,
               st.paragraph_format.line_spacing)] += 1
print("\n== style fonts ==")
for k in sizes:
    print(" ", k)
print("shd elements:", len(nd.element.body.findall(".//" + qn("w:shd"))))
