#!/usr/bin/env python3
"""Render the manuscript as a LaTeX source file for journal submission.

The markdown manuscript is the canonical artefact; this is a mechanical export
so the paper can be submitted to a venue that wants LaTeX. It converts the
headings, the inline [N] citations, the markdown tables and the emphasis, and
inserts figure environments at the points where the manuscript first references
each figure. It does not attempt to be a general markdown converter.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG = "attack-ontology-drift-cti-85bc51"
SRC = ROOT / "research" / "notes" / f"final_report_{TAG}.md"
OUT = ROOT / "paper" / "manuscript.tex"

FIGURES = {
    1: ("fig1_growth_churn", "Live technique count per Enterprise release, and per-release "
        "additions, retirements and description rewrites."),
    2: ("fig2_survival", "Identifier survival by source release, and the share recoverable "
        "through the published revocation graph at the newest release."),
    3: ("fig3_semantic_drift", "Silent semantic drift among techniques whose identifiers "
        "never changed."),
    4: ("fig4_growth_decomposition", "Per-transition decomposition of new group-technique "
        "edges for pre-existing groups."),
    5: ("fig5_attribution", "Attribution accuracy by condition, and the drift penalty with "
        "bootstrap confidence bands."),
    6: ("fig6_coverage", "Reported coverage under a frozen capability, and the "
        "random-portfolio sweep."),
    7: ("fig7_artifact_validity", "Label-validity curves for four deployed CTI corpora."),
    8: ("fig8_conclusion_flips", "Attribution verdict instability, and mitigation "
        "leaderboard reordering."),
    9: ("fig9_two_clocks", "The two clocks: the intensional clock at a common two-year "
        "horizon per cohort, and the five restructuring events across the three domains."),
    10: ("fig10_cwe_capec", "The two clocks in three MITRE vocabularies: identifier-set Jaccard across consecutive releases, and edited and substantially rewritten shares by cohort age, for ATT&CK Enterprise, CWE and CAPEC."),
}

PREAMBLE = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage[hidelinks]{hyperref}
\usepackage[margin=2.5cm]{geometry}
\usepackage{microtype}
\graphicspath{{figures/}}
\title{Ontology Drift in Cyber Threat Intelligence:\\
A Longitudinal Measurement of MITRE ATT\&CK and a Reporting Contract\\
for Reproducible CTI Analytics}
\date{}
\begin{document}
\maketitle
"""

ESCAPES = [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"),
           ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"), ("~", r"\textasciitilde{}"),
           ("^", r"\textasciicircum{}")]


def esc(s: str) -> str:
    for a, b in ESCAPES:
        s = s.replace(a, b)
    return s


def inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\\emph{\1}", s)
    s = re.sub(r"`([^`]+)`", r"\\texttt{\1}", s)
    return s


def table(rows: list[str]) -> str:
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [c for c in cells if not all(set(x) <= set("-: ") for x in c)]
    if not cells:
        return ""
    ncol = max(len(c) for c in cells)
    spec = "l" * ncol
    out = [r"\begin{center}\footnotesize", r"\begin{tabular}{" + spec + "}", r"\toprule"]
    head = cells[0] + [""] * (ncol - len(cells[0]))
    out.append(" & ".join(inline(h) for h in head) + r" \\")
    out.append(r"\midrule")
    for row in cells[1:]:
        row = row + [""] * (ncol - len(row))
        out.append(" & ".join(inline(c) for c in row) + r" \\")
    out += [r"\bottomrule", r"\end{tabular}", r"\end{center}"]
    return "\n".join(out)


def main() -> int:
    if not SRC.exists():
        print("manuscript not written yet", file=sys.stderr)
        return 2
    lines = SRC.read_text().splitlines()
    body, buf, seen_fig = [], [], set()
    for raw in lines:
        line = raw.rstrip()
        if line.startswith("|"):
            buf.append(line)
            continue
        if buf:
            body.append(table(buf))
            buf = []
        if line.startswith("# ") and not line.startswith("## "):
            # the manuscript's H1 is its title; the preamble already carries it
            continue
        if line.startswith("### "):
            body.append(r"\subsection{" + inline(line[4:]) + "}")
        elif line.startswith("## "):
            title = re.sub(r"^\d+\.\s*", "", line[3:])
            if title.strip().lower() == "abstract":
                body.append(r"\begin{abstract}")
                body.append("%ABSTRACT_OPEN%")
            elif "%ABSTRACT_OPEN%" in body:
                body.append(r"\end{abstract}")
                body.append(r"\section{" + inline(title) + "}")
            else:
                body.append(r"\section{" + inline(title) + "}")
        elif not line.strip():
            body.append("")
        else:
            body.append(inline(line))
            for n in sorted(int(x) for x in re.findall(r"Figure (\d+)", line)):
                if n in FIGURES and n not in seen_fig:
                    seen_fig.add(n)
                    f, cap = FIGURES[n]
                    body += ["", r"\begin{figure}[htbp]", r"\centering",
                             r"\includegraphics[width=\linewidth]{" + f + ".pdf}",
                             r"\caption{" + inline(cap) + "}",
                             r"\label{fig:" + str(n) + "}", r"\end{figure}", ""]
    if buf:
        body.append(table(buf))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(body).replace("%ABSTRACT_OPEN%", "")
    # close the abstract if the manuscript ended inside it
    if text.count(r"\begin{abstract}") > text.count(r"\end{abstract}"):
        text += "\n" + r"\end{abstract}"
    OUT.write_text(PREAMBLE + text + "\n\\end{document}\n")
    print(f"wrote {OUT} ({len(body)} lines, {len(seen_fig)} figures placed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
