#!/usr/bin/env python3
"""Draws figure.svg: three answers from one instrument.

One row per act of Stratum B, ordered by the rate the repaired instrument gives.  On each
row, three dots joined by a line -- the same measurement taken with the plural bug (run 1),
with the case bug (run 2), and with both repaired (run 3) -- and a hollow diamond at the
run-3 rate multiplied by the hand-measured precision of 0.45, which is the most defensible
estimate this work can offer of the quantity it set out to measure.

The spread between the three dots on a row is not noise around a true value.  Each dot is
what a night that stopped there would have published.

Raw SVG, no external resources, no randomness.
"""

import gzip
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent


def load_json(path):
    """Read a JSON file, transparently accepting the gzipped form.

    corpus.json and the two superseded run files are committed gzipped: they are 12.7 MB
    of largely repeated legal text against an 11 MB repository, and the licence question
    is not the size question.  Gzip keeps every byte checkable offline at a proportionate
    cost, which is the same trade the raw HTML lost.
    """
    path = pathlib.Path(path)
    if path.exists():
        return json.loads(path.read_text())
    gz = path.with_suffix(path.suffix + ".gz")
    with gzip.open(gz, "rt") as fh:
        return json.load(fh)


def dump_json(path, payload, gzipped=False):
    path = pathlib.Path(path)
    text = json.dumps(payload, indent=1) + "\n"
    if gzipped:
        with gzip.open(str(path) + ".gz", "wt") as fh:
            fh.write(text)
        if path.exists():
            path.unlink()
    else:
        path.write_text(text)

W, ROW, TOP, LEFT, RIGHT = 940, 21, 108, 268, 96
XMAX = 75.0

INK = "#1a1a1a"
MUTE = "#8a8a8a"
RUN1 = "#c9c2b6"
RUN2 = "#9a8f7d"
RUN3 = "#2f2f2f"
MARK = "#a33b2a"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    runs = {
        "run1": load_json(HERE / "results-run1-plural-bug.json"),
        "run2": load_json(HERE / "results-run2-case-bug.json"),
        "run3": load_json(HERE / "results.json"),
    }
    audit = load_json(HERE / "audit-results.json")
    precision = audit["precision"]["precision"]

    rate = {k: {a["celex"]: a["rate"] for a in v["acts"] if a["stratum"] == "B"}
            for k, v in runs.items()}
    acts = [a for a in runs["run3"]["acts"] if a["stratum"] == "B"]
    acts.sort(key=lambda a: -rate["run3"][a["celex"]])

    plot = W - LEFT - RIGHT
    H = TOP + len(acts) * ROW + 114

    def x(v):
        return LEFT + plot * v / XMAX

    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" '
           'height="%d" font-family="Georgia, \'Iowan Old Style\', serif">' % (W, H, W, H),
           '<rect width="%d" height="%d" fill="#faf9f6"/>' % (W, H)]

    out.append('<text x="%d" y="34" font-size="19" fill="%s">Three answers from one '
               'instrument</text>' % (LEFT - 200, INK))
    out.append('<text x="%d" y="55" font-size="12.5" fill="%s">Share of an act’s recitals '
               'carrying a sentence that names a party the act commands and tells it, with '
               '“should”, to act.</text>' % (LEFT - 200, MUTE))
    out.append('<text x="%d" y="72" font-size="12.5" fill="%s">28 acts of the European '
               'Parliament and of the Council, 2,888 recitals. The same code, measured three '
               'times: twice wrong, once repaired.</text>' % (LEFT - 200, MUTE))

    # axis
    for v in range(0, int(XMAX) + 1, 15):
        out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#e2ded4" '
                   'stroke-width="1"/>' % (x(v), TOP - 12, x(v), TOP + len(acts) * ROW))
        out.append('<text x="%.1f" y="%d" font-size="10.5" fill="%s" text-anchor="middle">'
                   '%d%%</text>' % (x(v), TOP - 18, MUTE, v))

    for i, act in enumerate(acts):
        y = TOP + i * ROW + 12
        celex = act["celex"]
        r1, r2, r3 = rate["run1"][celex], rate["run2"][celex], rate["run3"][celex]
        corrected = r3 * precision
        is_gdpr = celex == "32016R0679"

        if is_gdpr:
            out.append('<rect x="%d" y="%.1f" width="%d" height="%d" fill="#efe9dc"/>'
                       % (LEFT - 262, y - 10, W - 100, ROW - 2))
        label = "%s  %d" % (act["domain"], act["adoption_year"])
        out.append('<text x="%d" y="%.1f" font-size="11.5" text-anchor="end" fill="%s"%s>%s'
                   '</text>' % (LEFT - 14, y + 4, INK if is_gdpr else "#4a4a4a",
                                ' font-weight="bold"' if is_gdpr else "", esc(label)))

        lo, hi = min(r1, r2, r3, corrected), max(r1, r2, r3, corrected)
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#cfc8ba" '
                   'stroke-width="1.4"/>' % (x(lo), y, x(hi), y))
        out.append('<circle cx="%.1f" cy="%.1f" r="3.6" fill="%s"/>' % (x(r1), y, RUN1))
        out.append('<circle cx="%.1f" cy="%.1f" r="3.6" fill="%s"/>' % (x(r2), y, RUN2))
        out.append('<circle cx="%.1f" cy="%.1f" r="4.4" fill="%s"/>' % (x(r3), y, RUN3))
        d = 4.0
        out.append('<path d="M %.1f %.1f l %.1f %.1f l %.1f %.1f l %.1f %.1f Z" fill="none" '
                   'stroke="%s" stroke-width="1.6"/>'
                   % (x(corrected) - d, y, d, -d, d, d, -d, d, MARK))
        out.append('<text x="%d" y="%.1f" font-size="10.5" fill="%s" text-anchor="end">%.1f'
                   '</text>' % (W - 30, y + 4, MUTE, r3))

    base = TOP + len(acts) * ROW + 26
    items = [(RUN1, "circle", "run 1 — plural bug (F-111)"),
             (RUN2, "circle", "run 2 — case bug (F-112)"),
             (RUN3, "circle", "run 3 — repaired"),
             (MARK, "diamond", "run 3 × hand precision 0.45")]
    cx = LEFT - 200
    for colour, shape, text in items:
        if shape == "circle":
            out.append('<circle cx="%.1f" cy="%.1f" r="4" fill="%s"/>' % (cx, base - 4, colour))
        else:
            d = 4.0
            out.append('<path d="M %.1f %.1f l %.1f %.1f l %.1f %.1f l %.1f %.1f Z" fill="none"'
                       ' stroke="%s" stroke-width="1.6"/>'
                       % (cx - d, base - 4, d, -d, d, d, -d, d, colour))
        out.append('<text x="%.1f" y="%.1f" font-size="11" fill="%s">%s</text>'
                   % (cx + 10, base, MUTE, esc(text)))
        cx += 8 * len(text) + 34

    out.append('<text x="%d" y="%d" font-size="11" fill="%s">Each dot is a complete table a '
               'night could have published. The two wrong runs raised no error and dropped no '
               'act.</text>' % (LEFT - 200, base + 26, MUTE))
    out.append('<text x="%d" y="%d" font-size="11" fill="%s">Sources: EUR-Lex, CELEX ids in '
               'sources/MANIFEST.json. Rule and stop list: PREDICTIONS.md.</text>'
               % (LEFT - 200, base + 44, MUTE))
    out.append('<text x="%d" y="%d" font-size="11" fill="%s">Precision: 40 seeded sentences '
               'adjudicated by hand in audit.json — 18 of 40 were a directed norm.</text>'
               % (LEFT - 200, base + 62, MUTE))
    out.append("</svg>")

    (HERE / "figure.svg").write_text("\n".join(out) + "\n")
    print("figure.svg: %d acts, %d bytes" % (len(acts), (HERE / "figure.svg").stat().st_size))


if __name__ == "__main__":
    main()
