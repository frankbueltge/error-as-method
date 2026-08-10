#!/usr/bin/env python3
"""Eight Misprints — the measurement.

Runs the Simkin–Roychowdhury misprint test on today's citation record for one
paper: K. G. Wilson, *Confinement of quarks*, Phys. Rev. D 10, 2445 (1974).

    Simkin & Roychowdhury, "Read before you cite!", arXiv:cond-mat/0212043
    Simkin & Roychowdhury, "Theory of citing",      arXiv:1109.2272

Their test: a citation whose digits deviate from the true ones is a misprint;
a misprint that appears *identically* in several citing papers was copied, not
typed from the paper itself. R = D/T (distinct misprints over all misprints) is
their estimate of the fraction of citers who read what they cite.

Input : citations.json — 1,708 reference strings exactly as they stand in the
        citing manuscripts, harvested from INSPIRE-HEP on 2026-08-10.
Output: measure.json, figure.svg.

Deterministic: no network, no randomness. Same input, same output.
"""
import json
import os
import re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TRUE_VOL, TRUE_PAGE, TRUE_YEAR = 10, 2445, 1974

DOI_RE = re.compile(r"10\.\d{4,9}\s*/\s*\S+", re.I)
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.I)
ARX_RE = re.compile(r"arxiv[:\s]*[\w./-]+", re.I)
TOK = re.compile(r"\d+")
YEARISH = re.compile(r"\b(19[5-9]\d|20[0-2]\d)\b")

# ---------------------------------------------------------------------------
# The adjudication. The automatic pass below only FLAGS a reference whose digits
# do not carry the true coordinates; it cannot tell a misprint from an omission,
# from the pagination of a reprint edition (pp. 45-59), or from a
# reference string that lost its content on ingestion. Every flagged record was
# read by hand and given one of the verdicts below. This table is the observer's
# judgement, and it is written down here so that it can be disputed line by line.
#
# It is not a judgement about people. Mistyping a volume number is the most
# ordinary act in scientific writing; what is under study is the machinery that
# does or does not preserve the trace of a copy.
# ---------------------------------------------------------------------------
VERDICTS = {
    # recid: (verdict, slot, value_given, author_group)
    # The signature of a misprint is (slot, value): two records carry the SAME
    # misprint when they give the same wrong digits in the same place. The last
    # column marks records that share an author group — a repeat inside one
    # author group is a writer repeating themselves, not one paper copying
    # another (Simkin & Roychowdhury raise exactly this case, §II.4).
    2173044: ("misprint", "year", "1975", "-"),
    144427:  ("misprint", "year", "1975", "-"),
    2767189: ("misprint", "year", "1975", "-"),
    1835048: ("misprint", "volume", "IO", "-"),      # 'DIO' for 'D10'; probably digitisation, see work.md
    1765257: ("misprint", "volume", "46", "-"),
    1980647: ("misprint", "volume", "19", "-"),
    3064036: ("misprint", "volume", "80", "panella-pacetti-immirzi"),
    2939843: ("misprint", "volume", "80", "panella-pacetti-immirzi"),
    2904628: ("misprint-outside-triple", "issue", "9", "-"),   # true issue is 8
    267754:  ("ambiguous", "-", "Doering 1985", "-"),          # matched to Wilson; the string names another work
    1830982: ("degenerate", "-", "", "-"),
    1881127: ("degenerate", "-", "", "-"),
    2690092: ("degenerate", "-", "", "-"),
    2695397: ("degenerate", "-", "", "-"),
    1817336: ("degenerate", "-", "", "-"),
    1799832: ("reprint-pagination", "-", "45-59", "-"),
    1989722: ("reprint-pagination", "-", "45", "-"),
    1811497: ("reprint-pagination", "-", "45-59", "-"),
    1841274: ("reprint-pagination", "-", "45-59", "-"),
    2015258: ("reprint-pagination", "-", "45-59", "-"),
    3096768: ("reprint-pagination", "-", "45-59", "-"),
    1850374: ("omission", "page", "", "-"),
    2746042: ("omission", "page", "", "-"),
    1841346: ("omission", "volume+page", "", "-"),
    2691839: ("omission", "page", "", "-"),
    2971685: ("omission", "page", "", "-"),
    2871020: ("omission", "volume+page", "", "-"),
    3188399: ("omission", "page", "", "-"),
}

# Simkin & Roychowdhury, "Theory of citing" (arXiv:1109.2272), Table I.2, row 4 —
# the same Wilson paper, ISI data of late 2002 / early 2003.
SIMKIN_2002 = {"N": 2578, "T": 263, "D": 32, "R_eq1": 0.12, "R_eq8": 0.11}

# Author groups behind the deviations that are NOT digits — checked by hand against
# the INSPIRE record of each citing paper on 2026-08-10 (fields: authors).
AUTHOR_GROUP = {
    1974492: "zhang", 2031220: "zhang", 2860162: "zhang", 3082145: "zhang",
    2900045: "bairathi", 2933573: "bairathi", 2834350: "zhang-ruifeng-liang",
}


def strip(raw):
    s = ARX_RE.sub(" ", DOI_RE.sub(" ", URL_RE.sub(" ", raw)))
    s = s.replace("–", "-").replace("—", "-").replace("−", "-")
    return re.sub(r"\s+", " ", s)


def window(raw):
    """The span of the string that carries the Wilson reference."""
    s = strip(raw)
    m = re.search(r"[Ww]ilson|[Cc]on.?finement", s)
    return s if not m else s[max(0, m.start() - 40):m.start() + 240]


def flag(raw):
    w = window(raw)
    toks = {int(t) for t in TOK.findall(w)}
    years = {int(y) for y in YEARISH.findall(w)}
    bad = []
    if years and TRUE_YEAR not in years:
        bad.append("year")
    if TRUE_PAGE not in toks:
        bad.append("page")
    if TRUE_VOL not in toks:
        bad.append("volume")
    return bad


def main():
    data = json.load(open(os.path.join(HERE, "citations.json")))
    recs = data["records"]
    N = len(recs)

    flagged = []
    for r in recs:
        bad = flag(r["raw"])
        if bad:
            v = VERDICTS.get(r["recid"], ("UNADJUDICATED", "-", "", "-"))
            flagged.append({"recid": r["recid"], "year": r["year"], "slots": bad,
                            "verdict": v[0], "slot": v[1], "given": v[2],
                            "signature": f"{v[1]}={v[2]}" if v[0].startswith("misprint") else "-",
                            "author_group": v[3], "raw": r["raw"]})
    assert not [f for f in flagged if f["verdict"] == "UNADJUDICATED"], \
        "a flagged record has no hand verdict — adjudicate it before reporting"

    misprints = [f for f in flagged if f["verdict"] == "misprint"]
    T = len(misprints)
    sigs = Counter(f["signature"] for f in misprints)
    D = len(sigs)
    repeats = {}
    for s, n in sigs.items():
        if n < 2:
            continue
        who = {f["author_group"] for f in misprints if f["signature"] == s}
        repeats[s] = {"records": n,
                      "across_author_groups": not (len(who) == 1 and "-" not in who)}

    # Simkin & Roychowdhury Eq. (I.1) and Eq. (I.8), arXiv:1109.2272.
    r_eq1 = D / T
    r_eq8 = (D / T) * (N - T) / (N - D)

    by_verdict = Counter(f["verdict"] for f in flagged)
    era = Counter((r["year"] or 0) // 10 * 10 for r in recs)
    beyond = beyond_the_digits(recs)

    result = {
        "target": data["target"]["citation"],
        "corpus": data["corpus"],
        "N_reference_strings": N,
        "flagged_by_the_automatic_pass": len(flagged),
        "verdicts": dict(sorted(by_verdict.items())),
        "T_misprints": T,
        "D_distinct_misprints": D,
        "repeated_misprints": repeats,
        "misprint_rate_T_over_N": round(T / N, 5),
        "R_eq1_distinct_over_total": round(r_eq1, 3),
        "R_eq8_finite_size_corrected": round(r_eq8, 3),
        "comparison_simkin_2002_same_paper": SIMKIN_2002,
        "misprint_rate_2002": round(SIMKIN_2002["T"] / SIMKIN_2002["N"], 5),
        "citing_year_decades": dict(sorted(era.items())),
        "beyond_the_digits": beyond,
        "adjudication": sorted(flagged, key=lambda f: (f["year"] or 0, f["recid"])),
    }
    json.dump(result, open(os.path.join(HERE, "measure.json"), "w"),
              indent=1, ensure_ascii=False)

    svg(recs, flagged, result)
    for k in ("N_reference_strings", "T_misprints", "D_distinct_misprints",
              "misprint_rate_T_over_N", "R_eq1_distinct_over_total",
              "R_eq8_finite_size_corrected", "repeated_misprints"):
        print(f"{k:34} {result[k]}")


def beyond_the_digits(recs):
    """Deviations in the slots the digit test does not read: the author's surname
    and the word 'quarks' in the title. Simkin & Roychowdhury count only the
    volume/page/year sequence; these two slots are outside their instrument and
    outside the one above."""
    out = {}
    for label, rx, true in (("surname", r"\b[Ww][a-zA-Z]{2,7}on\b", "wilson"),
                            ("title-word", r"\bq[a-zA-Z]{3,5}s\b", "quarks")):
        hits = defaultdict(list)
        for r in recs:
            w = window(r["raw"])
            for t in {m.group(0) for m in re.finditer(rx, w)}:
                if t.lower() != true:
                    hits[t].append(r["recid"])
        out[label] = {
            t: {"records": sorted(ids),
                "author_groups": sorted({AUTHOR_GROUP.get(i, f"unchecked:{i}") for i in ids})}
            for t, ids in sorted(hits.items(), key=lambda kv: -len(kv[1]))}
    return out


# ---------------------------------------------------------------------------
# figure.svg — the field of 1,708 citations, and the eight that deviate.
# ---------------------------------------------------------------------------
def svg(recs, flagged, res):
    W, H = 980, 700
    L, R = 60, 40
    order = sorted(recs, key=lambda r: (r["year"] or 0, r["recid"]))
    pos = {r["recid"]: i for i, r in enumerate(order)}
    n = len(order)
    x0, x1 = L, W - R
    top, bot = 250, 320          # the strip

    def x(i):
        return x0 + (x1 - x0) * i / (n - 1)

    mis = {f["recid"]: f for f in flagged if f["verdict"] == "misprint"}
    bygroup = defaultdict(list)
    for f in mis.values():
        bygroup[f["signature"]].append(pos[f["recid"]])

    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
             f'width="{W}" height="{H}" font-family="Georgia, \'Times New Roman\', serif">')
    p.append(f'<rect width="{W}" height="{H}" fill="#f4f1ea"/>')
    p.append(f'<text x="{L}" y="46" font-size="21" fill="#1b1b1b">Eight misprints in 1,708 citations</text>')
    p.append(f'<text x="{L}" y="70" font-size="13" fill="#4a4a4a">'
             'Reference strings citing K. G. Wilson, Phys. Rev. D <tspan font-style="italic">10</tspan>, '
             '2445 (1974), as they stand in the citing manuscripts. INSPIRE-HEP, 10 August 2026.</text>')
    p.append(f'<text x="{L}" y="90" font-size="13" fill="#4a4a4a">'
             'Each hair is one citation, in rank order by the year of the citing record — the record is dominated by recent papers. '
             'Tall marks deviate.</text>')

    # the field
    for r in order:
        i = pos[r["recid"]]
        if r["recid"] in mis:
            continue
        p.append(f'<line x1="{x(i):.2f}" y1="{top}" x2="{x(i):.2f}" y2="{bot}" '
                 f'stroke="#8d8778" stroke-width="0.35" opacity="0.5"/>')
    # a year scale under the strip (rank order, not time order)
    marks, seen_y, lastx = [], set(), -1e9
    for r in order:
        y = r["year"] or 0
        if y and y % 10 == 0 and y not in seen_y and y >= 1980:
            seen_y.add(y)
            if x(pos[r["recid"]]) - lastx < 46:      # too close to the previous decade to label
                continue
            lastx = x(pos[r["recid"]])
            marks.append((y, pos[r["recid"]]))
    for y, i in marks:
        p.append(f'<line x1="{x(i):.2f}" y1="{bot}" x2="{x(i):.2f}" y2="{bot+6}" stroke="#8d8778"/>')
        p.append(f'<text x="{x(i):.2f}" y="{bot+19}" font-size="10.5" fill="#6a6357" '
                 f'text-anchor="middle">{y}</text>')

    # the deviations, numbered; labels pushed apart so none overlaps
    ordered = sorted(mis.values(), key=lambda f: pos[f["recid"]])
    xs = [x(pos[f["recid"]]) for f in ordered]
    lab_x, last = [], -1e9
    for xi in xs:
        xi = max(xi, last + 26)
        lab_x.append(xi)
        last = xi
    for k, f in enumerate(ordered):
        xi = x(pos[f["recid"]])
        p.append(f'<line x1="{xi:.2f}" y1="{top-34}" x2="{xi:.2f}" y2="{bot+2}" '
                 f'stroke="#8a2b1e" stroke-width="1.5"/>')
        p.append(f'<line x1="{xi:.2f}" y1="{top-34}" x2="{lab_x[k]:.2f}" y2="{top-46}" '
                 f'stroke="#8a2b1e" stroke-width="0.6"/>')
        p.append(f'<text x="{lab_x[k]:.1f}" y="{top-52}" font-size="11" fill="#8a2b1e" '
                 f'text-anchor="middle">{k+1}</text>')
    # arcs joining identical misprints (the copying signature)
    for g, idxs in bygroup.items():
        if len(idxs) < 2:
            continue
        same_authors = not res["repeated_misprints"][g]["across_author_groups"]
        col, dash = ("#8d8778", "1 4") if same_authors else ("#8a2b1e", "3 3")
        idxs.sort()
        for a, b in zip(idxs, idxs[1:]):
            xa, xb = x(a), x(b)
            p.append(f'<path d="M {xa:.2f} {top-34} C {xa:.2f} {top-104}, {xb:.2f} {top-104}, '
                     f'{xb:.2f} {top-34}" fill="none" stroke="{col}" '
                     f'stroke-width="1.1" stroke-dasharray="{dash}"/>')
    p.append(f'<text x="{L}" y="{top-118}" font-size="11.5" fill="#4a4a4a">'
             'An arc joins two papers that print the same wrong digits — the trace of a copy. '
             'Red: different authors. Grey: one author group repeating itself.</text>')

    # the roll of the eight
    ry = bot + 46
    p.append(f'<text x="{L}" y="{ry}" font-size="12.5" fill="#1b1b1b">The eight</text>')
    for k, f in enumerate(ordered):
        col = L + (k % 2) * 440
        row = ry + 20 + (k // 2) * 17
        rep = "  — repeated" if bygroup[f["signature"]].__len__() > 1 else ""
        p.append(f'<text x="{col}" y="{row}" font-size="11.5" fill="#3a3a3a">'
                 f'{k+1}. citing record of {f["year"]} · gives {f["slot"]} '
                 f'“{f["given"]}” · INSPIRE {f["recid"]}{rep}</text>')

    # the two rates
    base = bot + 46 + 20 + 4 * 17 + 34
    p.append(f'<text x="{L}" y="{base}" font-size="13" fill="#1b1b1b">'
             'Share of citations to this paper carrying a misprint</text>')
    rows = [("2002 · 2,578 citations, ISI (Simkin &amp; Roychowdhury, Table I.2, row 4)",
             SIMKIN_2002["T"] / SIMKIN_2002["N"], "#8a2b1e"),
            ("2026 · 1,708 reference strings, INSPIRE-HEP (this measurement)",
             res["misprint_rate_T_over_N"], "#2f4858")]
    for k, (lab, val, col) in enumerate(rows):
        y = base + 30 + k * 46
        w = (x1 - L) * val / 0.12
        p.append(f'<rect x="{L}" y="{y}" width="{max(w,1.2):.2f}" height="16" fill="{col}"/>')
        p.append(f'<text x="{L + max(w,1.2) + 8:.1f}" y="{y+13}" font-size="12.5" '
                 f'fill="#1b1b1b">{val*100:.2f}%</text>')
        p.append(f'<text x="{L}" y="{y+32}" font-size="11.5" fill="#4a4a4a">{lab}</text>')

    p.append(f'<text x="{L}" y="{H-46}" font-size="11.5" fill="#4a4a4a">'
             'The two bars are not the same corpus and not the same instrument: the 2002 row counts every '
             'indexed citation, this one counts only</text>')
    p.append(f'<text x="{L}" y="{H-30}" font-size="11.5" fill="#4a4a4a">'
             'the references whose original text survives in the database. What the comparison can carry is '
             'argued in work.md, not here.</text>')
    p.append(f'<text x="{L}" y="{H-12}" font-size="11" fill="#6a6357">'
             'Data CC0 (INSPIRE-HEP metadata) · figure generated by measure.py, no randomness</text>')
    p.append("</svg>")
    open(os.path.join(HERE, "figure.svg"), "w").write("\n".join(p))


if __name__ == "__main__":
    main()
