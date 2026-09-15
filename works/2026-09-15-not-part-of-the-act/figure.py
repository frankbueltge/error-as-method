#!/usr/bin/env python3
"""figure.py -- the fourth corpus is not a point.

Session 89 drew two line panels because its finding was a comparison between two curves.  Tonight's
finding has a different shape and gets a different form: a dot-and-interval chart.  Three traditions
enter `S89.WORDUNIT` as single values at word window 36.  The fourth enters as an INTERVAL, because
three party-term lists declared in advance by the same author on the same night put it at 0.76 %,
34.24 % and 50.91 % -- and the row's acceptance region, the union of 20 points either side of each
prior value, is narrower than the interval that crosses it.

Beneath it, the reason: how far the 26 borrowed party terms reach into 63 Acts of Parliament.

Every number is read out of reach.json, bounds.json and adjudication.json.  Nothing is drawn that is
not in one of those files.

Run last.  Writes figure.svg.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

W, H = 1020, 600
PAD_L, PAD_R = 208, 34
TOP, MAIN_H = 96, 232
STRIP_T = 404

INK = "#22201c"
MUTED = "#6b655a"
GRID = "#d8d2c6"
PAPER = "#f7f5f0"
BAND = "#e7e1d4"
COLOUR = {"whatwg": "#1d3557", "eu": "#a2391c", "rfc": "#2a6b5f", "uk": "#6b3fa0"}
SERIF = "Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif"
MONO = "SFMono-Regular,Menlo,DejaVu Sans Mono,Consolas,monospace"

XMAX = 56.0


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    rch = json.load(open(HERE / "reach.json"))
    bnd = json.load(open(HERE / "bounds.json"))
    adj = json.load(open(HERE / "adjudication.json"))

    prior = rch["prior_word_window_36"]
    byl = rch["the_interval"]["word_window_36_by_list"]
    arm = rch["row_arm"]
    bv = bnd["borrowed_vocabulary"]

    lo = min(min(prior.values()) - 20, 0)
    hi = max(prior.values()) + 20

    def px(v):
        return PAD_L + (W - PAD_L - PAD_R) * (v / XMAX)

    rows = [("rfc", "63 RFCs, capitals", prior["rfc"]),
            ("whatwg", "22 WHATWG living standards", prior["whatwg"]),
            ("eu", "63 EU acts, articles", prior["eu"])]
    step = MAIN_H / 4.0
    o = []

    o.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="100%%" role="img" '
             'aria-label="Three drafting traditions enter a falsifier as single values at word '
             'window 36. The fourth enters as an interval from 0.76 to 50.91 per cent, wider than '
             'the falsifier\'s whole acceptance region, because three party-term lists declared in '
             'advance disagree by 50 points.">' % (W, H))
    o.append("""<style>
 .bg{fill:%s}
 .grid{stroke:%s;stroke-width:1}
 .band{fill:%s}
 .iv{stroke:%s;stroke-width:9;stroke-linecap:butt;opacity:.30}
 .cap{stroke:%s;stroke-width:1.6}
 .hd{font:600 17px %s;fill:%s}
 .sub{font:13px %s;fill:%s}
 .lab{font:12.5px %s;fill:%s;text-anchor:end}
 .labk{font:600 12.5px %s;fill:%s;text-anchor:end}
 .ax{font:11px %s;fill:%s}
 .ac{text-anchor:middle}
 .num{font:600 12px %s}
 .note{font:11.5px %s;fill:%s}
 .tick{font:10.5px %s;fill:%s;text-anchor:middle}
</style>""" % (PAPER, GRID, BAND, COLOUR["uk"], INK, SERIF, INK, SERIF, MUTED, SERIF, INK,
                SERIF, INK, MONO, MUTED, MONO, SERIF, MUTED, MONO, MUTED))
    o.append('<rect class="bg" x="0" y="0" width="%d" height="%d"/>' % (W, H))

    o.append('<text class="hd" x="34" y="40">The fourth corpus is not a point</text>')
    o.append('<text class="sub" x="34" y="62">Reach at word window 36: the share of binding '
             'agentless obligations with a term for a party within 36 words behind them.</text>')
    o.append('<text class="sub" x="34" y="80">Shaded: where S89.WORDUNIT\'s <tspan '
             'font-style="italic">first</tspan> criterion accepts &#8212; within 20 points of a '
             'prior value. Its second is the median, which is what the base list fails.</text>')

    # the acceptance region
    o.append('<rect class="band" x="%.1f" y="%d" width="%.1f" height="%d"/>'
             % (px(max(lo, 0)), TOP - 8, px(hi) - px(max(lo, 0)), MAIN_H + 16))

    for v in (0, 10, 20, 30, 40, 50):
        o.append('<line class="grid" x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>'
                 % (px(v), TOP - 8, px(v), TOP + MAIN_H + 8))
        o.append('<text class="tick" x="%.1f" y="%d">%d%%</text>'
                 % (px(v), TOP + MAIN_H + 26, v))

    for i, (key, label, val) in enumerate(rows):
        y = TOP + step * i + 20
        o.append('<text class="lab" x="%d" y="%.1f">%s</text>' % (PAD_L - 18, y + 4, esc(label)))
        o.append('<circle cx="%.1f" cy="%.1f" r="6" fill="%s"/>' % (px(val), y, COLOUR[key]))
        o.append('<text class="num" x="%.1f" y="%.1f" fill="%s">%.2f</text>'
                 % (px(val) + 12, y + 4, COLOUR[key], val))

    # the fourth: an interval
    y = TOP + step * 3 + 20
    o.append('<text class="labk" x="%d" y="%.1f">63 UK Acts 2012&#8211;14, the Act</text>'
             % (PAD_L - 18, y - 2))
    o.append('<text class="lab" x="%d" y="%.1f">three lists, all declared in advance</text>'
             % (PAD_L - 18, y + 15))
    o.append('<line class="iv" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
             % (px(byl["base"]), y, px(byl["wide"]), y))
    for name, dy in (("base", -1), ("wide", -1)):
        o.append('<line class="cap" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                 % (px(byl[name]), y - 11, px(byl[name]), y + 11))
    o.append('<circle cx="%.1f" cy="%.1f" r="6" fill="%s"/>'
             % (px(byl["narrow"]), y, COLOUR["uk"]))
    o.append('<text class="num" x="%.1f" y="%.1f" fill="%s" text-anchor="middle">%.2f</text>'
             % (px(byl["base"]), y - 18, INK, byl["base"]))
    o.append('<text class="num" x="%.1f" y="%.1f" fill="%s" text-anchor="middle">%.2f</text>'
             % (px(byl["narrow"]), y - 18, COLOUR["uk"], byl["narrow"]))
    o.append('<text class="num" x="%.1f" y="%.1f" fill="%s" text-anchor="middle">%.2f</text>'
             % (px(byl["wide"]), y - 18, INK, byl["wide"]))
    o.append('<text class="ax" x="%.1f" y="%.1f" text-anchor="start">base 26</text>'
             % (px(byl["base"]) - 8, y + 30))
    o.append('<text class="ax" x="%.1f" y="%.1f" text-anchor="middle">+ 15 UK terms &#8212; '
             'the row\'s list</text>' % (px(byl["narrow"]), y + 30))
    o.append('<text class="ax" x="%.1f" y="%.1f" text-anchor="end">+ person</text>'
             % (px(byl["wide"]) + 8, y + 30))
    o.append('<text class="ax" x="%.1f" y="%.1f" text-anchor="start">median %s words &#8212; '
             'outside 60&#8211;500, which is how this list falsifies the row</text>'
             % (px(byl["base"]) - 8, y + 47,
                "{:,}".format(int(rch["lists"]["base"]["words"]["median_where_present"]))))

    o.append('<text class="note" x="34" y="%d">The interval is %.2f points. The whole '
             'falsification band is %d points wide. Two of these three lists falsify the row; '
             'one saves it.</text>'
             % (TOP + MAIN_H + 76, rch["the_interval"]["span_points"], 20))

    # ---------------------------------------------------------------------------- the strip below
    o.append('<line class="grid" x1="34" y1="%d" x2="%d" y2="%d"/>' % (STRIP_T - 18, W - 34,
                                                                      STRIP_T - 18))
    o.append('<text class="hd" x="34" y="%d">Why: the shared vocabulary does not reach this '
             'tradition</text>' % (STRIP_T + 8))
    occ = bv["occurrences_per_term"]
    present = sum(1 for n in occ.values() if n > 0)
    absent = bv["terms_that_never_occur_count"]
    box = 21
    for i in range(len(occ)):
        o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="2" fill="%s" '
                 'stroke="%s" stroke-width="1"/>'
                 % (34 + i * box, STRIP_T + 24, box - 5, box - 5,
                    COLOUR["uk"] if i < present else "none", GRID))
    o.append('<text class="sub" x="%d" y="%d">%d of the 26 party terms that make the four</text>'
             % (34 + 26 * box + 20, STRIP_T + 33, absent))
    o.append('<text class="sub" x="%d" y="%d">traditions comparable never occur at all</text>'
             % (34 + 26 * box + 20, STRIP_T + 51))
    o.append('<text class="note" x="34" y="%d">The seven that do occur stand %d times, in %s of '
             '71,762 blocks &#8212; %s %% &#8212; where <tspan font-style="italic">client</tspan> '
             'means a customer of a</text>'
             % (STRIP_T + 82, bv["total_occurrences"], bv["act_blocks_carrying_any_base_term"],
                bv["act_blocks_carrying_any_base_term_pct"]))
    o.append('<text class="note" x="34" y="%d">tax-avoidance promoter and <tspan '
             'font-style="italic">implementation</tspan> is a gerund.</text>' % (STRIP_T + 100))

    hand = json.load(open(HERE / "handreading.json"))
    o.append('<text class="note" x="34" y="%d">Forty window-0 rows read whole, one reader: the '
             'nearest party term is the bearer in %d &#8212; a precision of %.3f against %.3f in '
             'the corpus the list</text>'
             % (H - 40, hand["bearer"], hand["precision"],
                hand["session_88_precision_in_its_own_corpus"]))
    o.append('<text class="note" x="34" y="%d">was written for. %d of 6 predictions won, and '
             'S86.CONSTANT\'s register clause is checked at last, and survives.</text>'
             % (H - 22, adj["score"]["won"]))

    o.append("</svg>")
    (HERE / "figure.svg").write_text("\n".join(o) + "\n")
    print("figure.svg written: %d bytes" % (HERE / "figure.svg").stat().st_size)


if __name__ == "__main__":
    main()
