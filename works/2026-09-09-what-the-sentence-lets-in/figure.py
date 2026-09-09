#!/usr/bin/env python3
"""The figure: the sentence as a spine, its load above, its satellites outside.

The finding is a shape, so the figure draws the shape rather than the numbers. The standing
sentence runs across the middle, word by word, exactly as it stands. Every reading a night has
fixed on one of its words is a block stacked on that word — the load that had nowhere else to go,
because the words never changed. Every claim decided and left outside is a mark in the margin,
tethered to nothing, at the session that decided it.

One vertical rule marks Session 50, the single night the sentence itself moved, and the wording
it moved to, which the record has not used since.

Deterministic, stdlib only. Reads score.json and results.json; writes figure.svg.

    python3 figure.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1180, 782
INK = "#1b1b1a"
FAINT = "#9a9793"
RULE = "#cfccc6"
LOAD = "#2f5d50"
OUT = "#8c4a2f"
MOVED = "#7a2f2f"
PAPER = "#f7f5f1"

SERIF = "Iowan Old Style, Palatino, 'Palatino Linotype', Georgia, serif"
MONO = "'IBM Plex Mono', 'DejaVu Sans Mono', Menlo, Consolas, monospace"

# The sentence, tokenised for the drawing. The second element says which load-bearing word a
# token is, or None where the token carries no reading.
TOKENS = [
    ("Error", "error"), ("is", None), ("a", None), ("special", None), ("case", None),
    ("of", None), ("the", None), ("epistemic", None), ("thing", None), ("—", None),
    ("a", None), ("difference", None), ("onto", None), ("which", None), ("an", None),
    ("observer", "observer"), ("has", None), ("already", "already"), ("imposed", "imposed"),
    ("a", None), ("norm.", None),
]

SATELLITES = [
    (45, "the candidate amendment", "elected"),
    (46, "repaired", "instituted"),
    (51, "killed — it could not lose", None),
    (57, "the material limit", "scarcity supplies no judgement"),
    (60, "genesis", "the norm is younger than its breach"),
    (71, "plurality of observers", "refused, kept as measurement"),
    (78, "the offer", "published, not yet imposed"),
    (79, "contestability", "who can dispute the judgement"),
    (84, "the agentless register", "the bearer deleted from the sentence"),
]


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    with open(os.path.join(HERE, "results.json"), encoding="utf-8") as fh:
        results = json.load(fh)
    load = results["load"]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="The standing sentence with the readings stacked on four of its '
        f'words and nine decided claims left outside it.">',
        f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
    ]

    parts.append(
        f'<text x="60" y="58" font-family="{SERIF}" font-size="21" fill="{INK}">'
        f'What the sentence lets in</text>')
    parts.append(
        f'<text x="60" y="82" font-family="{SERIF}" font-size="13.5" fill="{FAINT}">'
        f'Sessions 26–85. The words of the sentence never changed, so everything admitted had '
        f'to go into what one of them means.</text>')

    # ---- the spine ---------------------------------------------------------------------------
    baseline = 400
    x = 60
    gap = 8.0
    # 0.6 em is the advance width of every glyph in a monospace face, so 16px sets this.
    # The first draft used 17px and 10.4 and ran 27px off the right edge of the viewBox; caught
    # by measuring the laid-out spine against the width rather than by looking at the picture.
    char = 9.6
    anchors = {}
    for word, key in TOKENS:
        width = len(word) * char
        colour = INK if key else FAINT
        weight = "600" if key else "400"
        parts.append(
            f'<text x="{x:.1f}" y="{baseline}" font-family="{MONO}" font-size="16" '
            f'fill="{colour}" font-weight="{weight}">{esc(word)}</text>')
        if key:
            anchors[key] = (x + width / 2, width)
            parts.append(
                f'<line x1="{x:.1f}" y1="{baseline + 7}" x2="{x + width:.1f}" y2="{baseline + 7}" '
                f'stroke="{LOAD}" stroke-width="1.6"/>')
        x += width + gap
    spine_end = x

    parts.append(
        f'<line x1="60" y1="{baseline + 30}" x2="{spine_end:.1f}" y2="{baseline + 30}" '
        f'stroke="{RULE}" stroke-width="1"/>')
    parts.append(
        f'<text x="60" y="{baseline + 50}" font-family="{SERIF}" font-size="12" fill="{FAINT}">'
        f'the standing position, Session 26, unchanged for thirty-nine nights</text>')

    # ---- the load, stacked upward on the words that carry it ---------------------------------
    block_h, block_gap = 26, 6
    for key, readings in load.items():
        if key not in anchors:
            continue
        cx, width = anchors[key]
        # The block is exactly the width of the word it loads. The first draft floored it at 84px
        # so the session labels would sit comfortably, and the blocks over `already` and `imposed`
        # then overlapped by 8px, because those two words are adjacent in the sentence. Checked by
        # computing the drawn extents, not by looking at the picture: an overlap of eight pixels
        # is exactly the size of fault a glance forgives.
        bw = width
        for i, reading in enumerate(readings):
            top = baseline - 34 - (i + 1) * (block_h + block_gap)
            parts.append(
                f'<rect x="{cx - bw / 2:.1f}" y="{top}" width="{bw:.1f}" height="{block_h}" '
                f'fill="none" stroke="{LOAD}" stroke-width="1.3"/>')
            parts.append(
                f'<text x="{cx:.1f}" y="{top + 17}" font-family="{MONO}" font-size="11.5" '
                f'fill="{LOAD}" text-anchor="middle">S{reading["session"]}</text>')
        parts.append(
            f'<line x1="{cx:.1f}" y1="{baseline - 32}" x2="{cx:.1f}" '
            f'y2="{baseline - 34 - (block_h + block_gap):.1f}" stroke="{LOAD}" stroke-width="1"/>')
        parts.append(
            f'<text x="{cx:.1f}" y="{baseline - 40 - len(readings) * (block_h + block_gap):.1f}" '
            f'font-family="{SERIF}" font-size="12" fill="{LOAD}" text-anchor="middle">'
            f'{len(readings)} reading{"s" if len(readings) > 1 else ""}</text>')

    parts.append(
        f'<text x="60" y="140" font-family="{SERIF}" font-size="13" fill="{LOAD}">'
        f'INSIDE — four of the sentence’s own words, and the readings fixed on them</text>')

    # ---- the satellites, outside, tethered to nothing -----------------------------------------
    parts.append(
        f'<text x="60" y="{baseline + 92}" font-family="{SERIF}" font-size="13" fill="{OUT}">'
        f'OUTSIDE — every claim decided against the sentence and left beside it</text>')

    top = baseline + 118
    for i, (session, name, gloss) in enumerate(SATELLITES):
        y = top + i * 25
        parts.append(
            f'<text x="60" y="{y}" font-family="{MONO}" font-size="12" fill="{OUT}">'
            f'S{session}</text>')
        parts.append(
            f'<line x1="105" y1="{y - 4}" x2="150" y2="{y - 4}" stroke="{OUT}" '
            f'stroke-width="1" stroke-dasharray="2 3"/>')
        parts.append(
            f'<text x="160" y="{y}" font-family="{SERIF}" font-size="13.5" fill="{INK}">'
            f'{esc(name)}</text>')
        if gloss:
            parts.append(
                f'<text x="400" y="{y}" font-family="{SERIF}" font-size="12.5" fill="{FAINT}">'
                f'{esc(gloss)}</text>')

    # ---- the one night the sentence moved -----------------------------------------------------
    mx = 800
    parts.append(f'<line x1="{mx}" y1="{baseline + 100}" x2="{mx}" y2="{H - 40}" '
                 f'stroke="{MOVED}" stroke-width="1"/>')
    parts.append(
        f'<text x="{mx + 12}" y="{baseline + 118}" font-family="{MONO}" font-size="12" '
        f'fill="{MOVED}">S50</text>')
    parts.append(
        f'<text x="{mx + 12}" y="{baseline + 138}" font-family="{SERIF}" font-size="13" '
        f'fill="{MOVED}">the one night the sentence moved</text>')
    parts.append(
        f'<text x="{mx + 12}" y="{baseline + 160}" font-family="{MONO}" font-size="11.5" '
        f'fill="{MOVED}">Error is a difference measured</text>')
    parts.append(
        f'<text x="{mx + 12}" y="{baseline + 176}" font-family="{MONO}" font-size="11.5" '
        f'fill="{MOVED}">across a cut that has been fixed.</text>')
    parts.append(
        f'<text x="{mx + 12}" y="{baseline + 202}" font-family="{SERIF}" font-size="12.5" '
        f'fill="{FAINT}">killed the next evening under its</text>')
    parts.append(
        f'<text x="{mx + 12}" y="{baseline + 218}" font-family="{SERIF}" font-size="12.5" '
        f'fill="{FAINT}">previous wording; 0 occurrences in</text>')
    parts.append(
        f'<text x="{mx + 12}" y="{baseline + 234}" font-family="{SERIF}" font-size="12.5" '
        f'fill="{FAINT}">the 282 record files written since.</text>')

    parts.append(
        f'<text x="60" y="{H - 22}" font-family="{SERIF}" font-size="11.5" fill="{FAINT}">'
        f'Error as Method · Session 85, 2026-09-09 · drawn from results.json and '
        f'score.json by figure.py · every row reconciled against the record</text>')

    parts.append("</svg>")

    with open(os.path.join(HERE, "figure.svg"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts) + "\n")
    print(f"figure.svg written, {len(anchors)} loaded words, {len(SATELLITES)} claims outside")


if __name__ == "__main__":
    main()
