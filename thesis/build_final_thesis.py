"""Assemble the 7 thesis chapters into one combined Markdown file (with a
title page and fixed image paths) and convert it to a single .docx via
pandoc.

Usage: python thesis/build_final_thesis.py
Requires: pandoc on PATH (verified present, v3.9.0.2).
"""

import re
import subprocess
from pathlib import Path

THESIS_DIR = Path(__file__).resolve().parent
CHAPTERS_DIR = THESIS_DIR / "chapters"
OUT_MD = THESIS_DIR / "_final_thesis_combined.md"
OUT_DOCX = THESIS_DIR / "Pathiraja_29071_Final_Thesis.docx"

CHAPTER_FILES = [
    "ch01_introduction/ch01_introduction.md",
    "ch02_literature_review/ch02_literature_review.md",
    "ch03_methodology/ch03_methodology.md",
    "ch04_system_design/ch04_system_design.md",
    "ch05_implementation/ch05_implementation.md",
    "ch06_evaluation/ch06_evaluation.md",
    "ch07_conclusion/ch07_conclusion.md",
]

TITLE_PAGE = """\
---
title: "AI-Powered Proactive YouTube Title Optimizer"
author: "P.A.D.B. Pathiraja (Student ID: 29071)"
date: "10 September 2026"
---

\\newpage

**AI-Powered Proactive YouTube Title Optimizer**

**A Multi-Agent System for Psychologically Optimised, Faithfulness-Constrained
Video Title Generation**

BSc (Hons) Software Engineering

P.A.D.B. Pathiraja (Student ID: 29071)

NSBM Green University, Faculty of Computing

Client: P.A.D.B. Pathiraja (29071)

\\newpage

"""


def fix_image_paths(text: str) -> str:
    # thesis/chapters/chXX_*/chXX.md -> ../../assets/X.png  becomes  assets/X.png
    text = text.replace("](../../assets/", "](assets/")
    # thesis/chapters/chXX_*/chXX.md -> ../../../system/evaluation/outputs/X.png
    # becomes ../system/evaluation/outputs/X.png (one level up from thesis/)
    text = text.replace(
        "](../../../system/evaluation/outputs/", "](../system/evaluation/outputs/"
    )
    return text


def strip_trailing_chapter_footer(text: str) -> str:
    # Drop the "*Chapter N ... | ... | NSBM Green University*" footer line;
    # it's redundant once chapters are combined into one document.
    return re.sub(
        r"\n\*Chapter \d+.*NSBM Green University\*\n*$", "\n", text.rstrip() + "\n"
    )


def main():
    parts = [TITLE_PAGE]
    for rel_path in CHAPTER_FILES:
        path = CHAPTERS_DIR / rel_path
        text = path.read_text(encoding="utf-8")
        text = fix_image_paths(text)
        text = strip_trailing_chapter_footer(text)
        parts.append(text.strip())
        parts.append("\n\n\\newpage\n\n")

    combined = "\n\n".join(parts)
    OUT_MD.write_text(combined, encoding="utf-8")
    print(f"Combined Markdown written -> {OUT_MD} ({len(combined)} chars)")

    cmd = [
        "pandoc",
        str(OUT_MD),
        "-o",
        str(OUT_DOCX),
        "--toc",
        "--toc-depth=3",
        "--resource-path",
        str(THESIS_DIR),
        "--metadata",
        "title=AI-Powered Proactive YouTube Title Optimizer",
    ]
    result = subprocess.run(cmd, cwd=str(THESIS_DIR), capture_output=True, text=True)
    if result.returncode != 0:
        print("PANDOC FAILED")
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(1)
    OUT_MD.unlink()
    print(f"Saved -> {OUT_DOCX}")


if __name__ == "__main__":
    main()
