#!/usr/bin/env python3
"""Render the manuscript as a single self-contained web page.

The markdown is the canonical artefact; this converts it faithfully rather than
re-writing it. ATT&CK identifiers and release numbers are set in the mono face
wherever they appear in running text, because the paper's subject is identifiers
as units of measurement.
"""
from __future__ import annotations

import html
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG = "attack-ontology-drift-cti-85bc51"
SRC = ROOT / "research" / "notes" / f"final_report_{TAG}.md"
OUT = Path(os.environ.get(
    "WEB_OUT",
    "/tmp/claude-0/-home-user-hyper-research-works/"
    "aa6e0fd0-b155-51a6-ad4a-ebbe528f3807/scratchpad/web/paper.html"))
FIG_PREFIX = os.environ.get("WEB_FIG_PREFIX", "")
RESULTS = ROOT / "data" / "results"

FIG_FILES = {
    1: "fig1_growth_churn.png", 2: "fig2_survival.png", 3: "fig3_semantic_drift.png",
    4: "fig4_growth_decomposition.png", 5: "fig5_attribution.png",
    6: "fig6_coverage.png", 7: "fig7_artifact_validity.png",
    8: "fig8_conclusion_flips.png", 9: "fig9_two_clocks.png", 10: "fig10_cwe_capec.png",
}

ATTACK_ID = re.compile(r"\b(T\d{4}(?:\.\d{3})?|TA\d{4}|MOB-T\d{4})\b")
VERSION = re.compile(r"\bv\d{1,2}\.\d{1,2}\b")
CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITAL = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
CITE = re.compile(r"\[(\d+(?:\s*,\s*\d+)*)\]")


def inline(text: str) -> str:
    """Markdown inline formatting, with code spans protected from the rest."""
    spans: list[str] = []

    def stash(m):
        spans.append(f'<code>{html.escape(m.group(1))}</code>')
        return f"\x00{len(spans) - 1}\x00"

    text = CODE.sub(stash, text)
    text = html.escape(text)
    text = BOLD.sub(r"<strong>\1</strong>", text)
    text = ITAL.sub(r"<em>\1</em>", text)
    text = ATTACK_ID.sub(r'<span class="id">\1</span>', text)
    text = VERSION.sub(r'<span class="ver">\g<0></span>', text)
    text = re.sub(r"[ ]+(?=\[\d)", "", text)
    text = CITE.sub(
        lambda m: "".join(
            f'<a class="cite" href="#ref-{n.strip()}">{n.strip()}</a>'
            for n in m.group(1).split(",")),
        text)
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], text)


def render_table(rows: list[str]) -> str:
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [c for c in cells if not all(set(x) <= set("-: ") for x in c)]
    if not cells:
        return ""
    head, body = cells[0], cells[1:]
    out = ['<div class="scroll"><table>', "<thead><tr>"]
    out += [f"<th>{inline(c)}</th>" for c in head]
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def build_body(md: str) -> tuple[str, list[tuple[str, str, str]]]:
    blocks = md.split("\n\n")
    out, toc = [], []
    i, open_section = 0, False
    in_sources = False
    pending_caption: str | None = None
    while i < len(blocks):
        b = blocks[i].strip()
        i += 1
        if not b:
            continue

        if b.startswith("# ") and not b.startswith("## "):
            continue

        if b.startswith("## "):
            title = b[3:].strip()
            if open_section:
                out.append("</section>")
            m = re.match(r"^(\d+)\.\s+(.*)$", title)
            num, label = (m.group(1), m.group(2)) if m else ("", title)
            slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
            toc.append((num, label, slug))
            in_sources = label.lower() == "sources"
            out.append(f'<section id="{slug}">')
            out.append('<div class="sec-head">'
                       + (f'<span class="sec-num">{num}</span>' if num else "")
                       + f"<h2>{inline(label)}</h2></div>")
            open_section = True
            continue

        if b.startswith("### "):
            title = b[4:].strip()
            m = re.match(r"^(\d+\.\d+)\s+(.*)$", title)
            num, label = (m.group(1), m.group(2)) if m else ("", title)
            out.append(f'<h3><span class="sub-num">{num}</span>{inline(label)}</h3>')
            continue

        if b.startswith("|"):
            out.append(render_table([l for l in b.split("\n") if l.startswith("|")]))
            if pending_caption:
                out.append(f'<figcaption class="tbl-cap">{pending_caption}</figcaption>')
                out.append("</figure>")
                pending_caption = None
            continue

        fig = re.match(r"^\*\*Figure (\d+)\.\*\*\s*(.*)$", b, re.S)
        if fig:
            n = int(fig.group(1))
            cap = inline(" ".join(fig.group(2).split()))
            src = FIG_PREFIX + FIG_FILES.get(n, "")
            out.append(
                f'<figure class="fig" id="fig-{n}">'
                f'<img src="{src}" alt="Figure {n}" loading="lazy" width="1920" height="760">'
                f'<figcaption><span class="fig-num">Figure {n}</span>{cap}</figcaption>'
                f"</figure>")
            continue

        tbl = re.match(r"^\*\*Table (\d+)\.\*\*\s*(.*)$", b, re.S)
        if tbl:
            n = int(tbl.group(1))
            cap = inline(" ".join(tbl.group(2).split()))
            out.append(f'<figure class="tbl" id="tbl-{n}">')
            pending_caption = f'<span class="fig-num">Table {n}</span>{cap}'
            continue

        if b.startswith("- "):
            items = [inline(l[2:].strip()) for l in b.split("\n") if l.startswith("- ")]
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>")
            continue

        if in_sources and re.match(r"^\d+\.\s", b):
            out.append('<ol class="refs">')
            for line in b.split("\n"):
                m = re.match(r"^(\d+)\.\s+(.*)$", line.strip())
                if not m:
                    continue
                n, rest = m.group(1), m.group(2)
                url_m = re.search(r"(https?://\S+)$", rest)
                url = url_m.group(1) if url_m else ""
                title = rest[: url_m.start()].strip() if url_m else rest
                link = (f'<a href="{html.escape(url)}" rel="noopener" '
                        f'target="_blank">{html.escape(url)}</a>') if url else ""
                out.append(f'<li id="ref-{n}"><span class="ref-n">{n}</span>'
                           f'<span class="ref-t">{inline(title)}</span>{link}</li>')
            out.append("</ol>")
            continue

        out.append(f"<p>{inline(' '.join(b.split()))}</p>")

    if open_section:
        out.append("</section>")
    return "\n".join(out), toc


def timeline_svg() -> str:
    """The five restructuring events at their real dates and Jaccard values."""
    e12 = json.loads((RESULTS / "e12_temporal_structure.json").read_text())
    events = sorted(e12["recurrence"]["events"], key=lambda e: e["date"])
    start, end = 2018.0, 2026.6
    w, h = 1000, 118
    pad_l, pad_r = 54, 54
    span = w - pad_l - pad_r

    def x(date: str) -> float:
        y, m, _ = date.split("-")
        t = int(y) + (int(m) - 1) / 12
        return pad_l + span * (t - start) / (end - start)

    parts = [f'<svg viewBox="0 0 {w} {h}" role="img" '
             f'aria-label="Five ATT&amp;CK restructuring events between 2018 and 2026" '
             f'class="timeline">']
    axis_y = 78
    parts.append(f'<line x1="{pad_l}" y1="{axis_y}" x2="{w-pad_r}" y2="{axis_y}" '
                 f'class="tl-axis"/>')
    for yr in range(2018, 2027):
        xx = pad_l + span * (yr - start) / (end - start)
        parts.append(f'<line x1="{xx:.1f}" y1="{axis_y-4}" x2="{xx:.1f}" '
                     f'y2="{axis_y+4}" class="tl-tick"/>')
        parts.append(f'<text x="{xx:.1f}" y="{axis_y+22}" class="tl-year">{yr}</text>')
    for k, e in enumerate(events):
        xx = x(e["date"])
        dom = e["domain"].replace("-attack", "")
        top = 22 if k % 2 == 0 else 44
        parts.append(f'<line x1="{xx:.1f}" y1="{top+6}" x2="{xx:.1f}" y2="{axis_y}" '
                     f'class="tl-stem"/>')
        parts.append(f'<circle cx="{xx:.1f}" cy="{axis_y}" r="4.5" class="tl-dot"/>')
        parts.append(f'<text x="{xx:.1f}" y="{top}" class="tl-label">'
                     f'{dom} <tspan class="tl-j">J={e["jaccard"]:.3f}</tspan></text>')
    parts.append("</svg>")
    return "".join(parts)


def headline_figures() -> list[tuple[str, str, str]]:
    e1 = json.loads((RESULTS / "e1_e2_e3.json").read_text())["enterprise-attack"]
    e4 = json.loads((RESULTS / "e4_growth.json").read_text())["enterprise-attack"]
    e11 = json.loads((RESULTS / "e11_version_metadata.json").read_text())["summary"]
    e16 = json.loads((RESULTS / "e16_layer_adoption.json").read_text())["summary"]
    c = e4["cumulative"]
    base = c["total_added"] - c["new_actor"]
    book = (c["ontology_refinement"] + c["revocation_remap"]) / base
    worst = min(e1["churn"], key=lambda x: x["jaccard_id"])
    return [
        (f"{book:.3f}", "of new adversary edges are bookkeeping",
         "not intelligence, for groups ATT&CK already tracked"),
        (f"{e11['precision_of_version_bump']:.3f}", "precision of ATT&CK's own change signal",
         f"recall {e11['recall_of_version_bump']:.3f}, as a detector of a rewritten technique"),
        (f"{worst['jaccard_id']:.3f}", "identifier overlap at the worst boundary",
         f"Enterprise v{worst['from']} to v{worst['to']}, one release"),
        (f"{e16['by_group']['third_party']['dead_share']:.3f}",
         "of published coverage annotations are dead",
         "across 57 third-party layers, none of which declares a release"),
    ]


def main() -> None:
    md = SRC.read_text()
    title_line = md.split("\n", 1)[0].lstrip("# ").strip()
    abstract = md.split("## Abstract", 1)[1].split("## 1.", 1)[0].strip()
    body_md = md.split("## Abstract", 1)[0] + "## Abstract\n\n" + md.split("## Abstract", 1)[1]
    body, toc = build_body(body_md)
    words = len(re.findall(r"\S+", md))

    tiles = "".join(
        f'<div class="tile"><span class="tile-n">{n}</span>'
        f'<span class="tile-l">{html.escape(l)}</span>'
        f'<span class="tile-s">{html.escape(s)}</span></div>'
        for n, l, s in headline_figures())
    nav = "".join(
        f'<li><a href="#{slug}">'
        f'{f"<span>{num}</span>" if num else "<span></span>"}{html.escape(label)}</a></li>'
        for num, label, slug in toc)

    page = TEMPLATE.format(
        title=html.escape(title_line.split(":")[0]),
        full_title=html.escape(title_line),
        subtitle=html.escape(title_line.split(":", 1)[1].strip() if ":" in title_line else ""),
        timeline=timeline_svg(), tiles=tiles, nav=nav, body=body, words=f"{words:,}",
        abstract_preview=(
            "MITRE ATT&amp;CK has been re-issued 109 times since January 2018, and no "
            "published CTI result records which issue it used. This paper measures what "
            "that omission costs, and finds the damage lands where the analytic was "
            "doing real work."),
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page)
    print(f"wrote {OUT} ({len(page)/1000:.0f} kB, {len(toc)} sections)")


TEMPLATE = r"""<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root {{
  --ground:#f6f7f9; --surface:#ffffff; --ink:#161a21; --ink-soft:#5a6370;
  --accent:#12637c; --accent-soft:#e3eef2; --drift:#a9662b; --retired:#6c5a7b;
  --rule:#d5dbe2; --rule-soft:#e7ebf0;
  --serif:"Source Serif 4",Georgia,"Times New Roman",serif;
  --sans:Archivo,"Helvetica Neue",Arial,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,"SF Mono",Menlo,monospace;
  --measure:68ch;
}}
@media (prefers-color-scheme:dark) {{
  :root:not([data-theme="light"]) {{
    --ground:#101419; --surface:#171c23; --ink:#e6eaf0; --ink-soft:#97a2b0;
    --accent:#58b6d2; --accent-soft:#17313b; --drift:#d99553; --retired:#a791b8;
    --rule:#262e39; --rule-soft:#1e242c;
  }}
}}
:root[data-theme="dark"] {{
  --ground:#101419; --surface:#171c23; --ink:#e6eaf0; --ink-soft:#97a2b0;
  --accent:#58b6d2; --accent-soft:#17313b; --drift:#d99553; --retired:#a791b8;
  --rule:#262e39; --rule-soft:#1e242c;
}}
* {{ box-sizing:border-box; }}
body {{
  background:var(--ground); color:var(--ink); font-family:var(--serif);
  font-size:17px; line-height:1.62; margin:0;
  padding-inline:20px; padding-block:0 72px;
  -webkit-font-smoothing:antialiased;
}}
.wrap {{ max-width:1180px; margin-inline:auto; }}
h1,h2,h3 {{ font-family:var(--sans); text-wrap:balance; }}
a {{ color:var(--accent); }}

/* ---------- masthead ---------- */
header.paper {{ padding-block:56px 30px; border-bottom:1px solid var(--rule); }}
.eyebrow {{
  font-family:var(--sans); font-size:11.5px; font-weight:600; letter-spacing:.16em;
  text-transform:uppercase; color:var(--ink-soft); margin:0 0 18px;
  display:flex; gap:14px; flex-wrap:wrap; align-items:baseline;
}}
.eyebrow .dot {{ color:var(--rule); }}
h1 {{ font-size:clamp(28px,4.4vw,46px); line-height:1.1; font-weight:700; margin:0; letter-spacing:-.018em; }}
h1 .sub {{ display:block; font-weight:500; font-size:.56em; line-height:1.28; color:var(--ink-soft); margin-top:14px; letter-spacing:-.005em; }}
.lede {{ max-width:var(--measure); margin:26px 0 0; color:var(--ink-soft); font-size:17.5px; }}

/* ---------- timeline ---------- */
.tl-wrap {{ margin:34px 0 4px; }}
.tl-title {{
  font-family:var(--sans); font-size:11.5px; font-weight:600; letter-spacing:.14em;
  text-transform:uppercase; color:var(--ink-soft); margin-bottom:6px;
}}
svg.timeline {{ width:100%; height:auto; display:block; overflow:visible; }}
.tl-axis, .tl-tick {{ stroke:var(--rule); stroke-width:1; }}
.tl-stem {{ stroke:var(--drift); stroke-width:1; stroke-dasharray:2 2; }}
.tl-dot {{ fill:var(--drift); }}
.tl-year {{ fill:var(--ink-soft); font-family:var(--mono); font-size:10.5px; text-anchor:middle; }}
.tl-label {{ fill:var(--ink); font-family:var(--sans); font-size:11.5px; font-weight:600; text-anchor:middle; }}
.tl-j {{ fill:var(--drift); font-family:var(--mono); font-weight:400; }}

/* ---------- headline figures ---------- */
.tiles {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:1px;
  background:var(--rule); border:1px solid var(--rule); margin:38px 0 0; }}
.tile {{ background:var(--surface); padding:18px 18px 20px; display:flex; flex-direction:column; gap:5px; }}
.tile-n {{ font-family:var(--mono); font-size:30px; font-weight:500; color:var(--accent); font-variant-numeric:tabular-nums; line-height:1; }}
.tile-l {{ font-family:var(--sans); font-size:13px; font-weight:600; line-height:1.32; }}
.tile-s {{ font-size:13.5px; color:var(--ink-soft); line-height:1.4; }}

/* ---------- layout ---------- */
.cols {{ display:grid; grid-template-columns:1fr; gap:40px; margin-top:44px; }}
@media (min-width:1080px) {{ .cols {{ grid-template-columns:210px minmax(0,1fr); gap:56px; align-items:start; }} }}
nav.toc {{ position:sticky; top:22px; font-family:var(--sans); font-size:13px; }}
nav.toc h2 {{ font-size:11.5px; letter-spacing:.14em; text-transform:uppercase; color:var(--ink-soft); margin:0 0 10px; font-weight:600; }}
nav.toc ol {{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:1px; }}
nav.toc a {{ display:grid; grid-template-columns:22px 1fr; gap:6px; padding:3.5px 0; color:var(--ink-soft); text-decoration:none; line-height:1.3; }}
nav.toc a span:first-child {{ font-family:var(--mono); font-size:11px; color:var(--rule); }}
nav.toc a:hover {{ color:var(--accent); }}
@media (max-width:1079px) {{ nav.toc {{ position:static; border:1px solid var(--rule); padding:16px 18px; background:var(--surface); }} }}

article {{ max-width:var(--measure); }}
section {{ margin-bottom:8px; }}
.sec-head {{ display:flex; gap:14px; align-items:baseline; margin:46px 0 14px; padding-top:20px; border-top:1px solid var(--rule); }}
#abstract .sec-head {{ border-top:0; padding-top:0; margin-top:10px; }}
.sec-num {{ font-family:var(--mono); font-size:14px; color:var(--accent); font-weight:500; }}
h2 {{ font-size:25px; font-weight:600; margin:0; letter-spacing:-.012em; }}
h3 {{ font-size:17px; font-weight:600; margin:34px 0 10px; display:flex; gap:10px; align-items:baseline; }}
.sub-num {{ font-family:var(--mono); font-size:13px; color:var(--ink-soft); font-weight:400; }}
p {{ margin:0 0 16px; }}
ul {{ margin:0 0 18px; padding-left:20px; }}
li {{ margin-bottom:7px; }}
strong {{ font-weight:600; }}
code {{ font-family:var(--mono); font-size:.87em; background:var(--rule-soft); padding:1px 5px; border-radius:2px; }}
.id, .ver {{ font-family:var(--mono); font-size:.9em; font-variant-numeric:tabular-nums; }}
.id {{ color:var(--retired); }}
.ver {{ color:var(--ink-soft); }}
a.cite {{
  font-family:var(--mono); font-size:11px; font-weight:500; text-decoration:none;
  color:var(--accent); background:var(--accent-soft); padding:1px 4px; border-radius:2px;
  vertical-align:.18em; margin-inline:1px;
}}
a.cite:hover {{ text-decoration:underline; }}

/* ---------- figures and tables ---------- */
figure {{ margin:30px 0; }}
@media (min-width:1080px) {{ figure {{ width:min(124%,calc(100vw - 300px)); }} }}
.fig img {{ width:100%; height:auto; display:block; background:#fff; border:1px solid var(--rule); }}
figcaption {{ font-family:var(--sans); font-size:13px; line-height:1.45; color:var(--ink-soft); margin-top:9px; }}
.fig-num {{ color:var(--ink); font-weight:600; margin-right:7px; }}
.tbl-cap {{ margin-top:9px; }}
.scroll {{ overflow-x:auto; border:1px solid var(--rule); background:var(--surface); }}
table {{ border-collapse:collapse; width:100%; font-family:var(--mono); font-size:12px; font-variant-numeric:tabular-nums; }}
th {{ text-align:left; font-weight:500; color:var(--ink-soft); font-family:var(--sans); font-size:11px;
  letter-spacing:.03em; padding:9px 11px; border-bottom:1px solid var(--rule); white-space:nowrap; }}
td {{ padding:7px 11px; border-bottom:1px solid var(--rule-soft); white-space:nowrap; }}
tbody tr:last-child td {{ border-bottom:0; }}
tbody tr:hover td {{ background:var(--rule-soft); }}
td .id, td .ver, td code {{ font-size:1em; background:none; padding:0; }}

/* ---------- references ---------- */
ol.refs {{ list-style:none; margin:0; padding:0; font-size:14px; }}
ol.refs li {{ display:grid; grid-template-columns:32px 1fr; gap:4px 10px; padding:9px 0; border-bottom:1px solid var(--rule-soft); margin:0; }}
ol.refs li:target {{ background:var(--accent-soft); }}
.ref-n {{ font-family:var(--mono); font-size:12px; color:var(--accent); }}
.ref-t {{ font-family:var(--sans); font-size:13.5px; line-height:1.4; }}
ol.refs a {{ grid-column:2; font-family:var(--mono); font-size:11.5px; word-break:break-all; color:var(--ink-soft); }}
ol.refs a:hover {{ color:var(--accent); }}

footer {{ margin-top:56px; padding-top:22px; border-top:1px solid var(--rule);
  font-family:var(--sans); font-size:13px; color:var(--ink-soft); max-width:var(--measure); }}
@media (prefers-reduced-motion:reduce) {{ * {{ animation:none !important; transition:none !important; }} }}
:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
</style>

<div class="wrap">
<header class="paper">
  <p class="eyebrow"><span>Measurement study</span><span class="dot">/</span><span>Cyber threat intelligence</span><span class="dot">/</span><span>{words} words</span></p>
  <h1>{title}<span class="sub">{subtitle}</span></h1>
  <p class="lede">{abstract_preview}</p>

  <div class="tl-wrap">
    <p class="tl-title">Restructuring events, all three ATT&amp;CK domains</p>
    {timeline}
  </div>

  <div class="tiles">{tiles}</div>
</header>

<div class="cols">
  <nav class="toc" aria-label="Contents">
    <h2>Contents</h2>
    <ol>{nav}</ol>
  </nav>
  <article>
{body}
  <footer>
    Every figure in this paper is computed from public MITRE ATT&amp;CK STIX releases and public
    CTI label files by the scripts in the reproduction package, which runs end to end from one
    shell script and produces byte-identical output across runs.
  </footer>
  </article>
</div>
</div>
"""

if __name__ == "__main__":
    main()
