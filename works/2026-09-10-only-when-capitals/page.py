#!/usr/bin/env python3
"""index.html -- Session 86, 2026-09-10.  Self-contained, no external load, no framework.

The page exists for one reason, which is the same reason Session 85's did: the night's
load-bearing weakness is that 80 rows were adjudicated by one person who wrote the hypothesis, and
the only real answer to that is to make disagreeing cheap.  Every row is here with its full
sentence, its three marks and my note, filterable, on one page.
"""

import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

CSS = """
:root{--ink:#1b1b1a;--faint:#6f6c68;--rule:#d8d4cd;--paper:#f7f5f1;--panel:#fffefb;
 --up:#2f5d50;--low:#8c4a2f;--warn:#7a2f2f}
@media (prefers-color-scheme:dark){:root{--ink:#e9e6e0;--faint:#a5a19a;--rule:#3a3835;
 --paper:#171715;--panel:#1e1e1b;--up:#7fb5a3;--low:#d59470;--warn:#d98080}}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
 font-family:"Iowan Old Style",Palatino,"Palatino Linotype",Georgia,serif;line-height:1.55}
.wrap{max-width:1080px;margin:0 auto;padding:36px 20px 80px}
h1{font-size:1.75rem;font-weight:600;margin:0 0 .2em}
h2{font-size:1.12rem;font-weight:600;margin:2.4em 0 .5em;padding-bottom:.3em;
 border-bottom:1px solid var(--rule)}
.sub{color:var(--faint);margin:0 0 1.6em}
p{max-width:70ch}
figure{margin:2em 0}
figure img{width:100%;height:auto;border:1px solid var(--rule);background:#faf7f1}
figcaption{color:var(--faint);font-size:.86rem;margin-top:.5em;max-width:70ch}
.controls{display:flex;flex-wrap:wrap;gap:8px;margin:1em 0}
button{font:inherit;font-size:.86rem;padding:5px 12px;border:1px solid var(--rule);
 background:var(--panel);color:var(--ink);border-radius:2px;cursor:pointer}
button[aria-pressed=true]{border-color:var(--ink);font-weight:600}
.tablewrap{overflow-x:auto;border:1px solid var(--rule);border-radius:3px;background:var(--panel)}
table{border-collapse:collapse;width:100%;font-size:.86rem}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
th{font-weight:600;font-size:.78rem;letter-spacing:.03em;text-transform:uppercase;
 color:var(--faint);white-space:nowrap}
td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.rows{margin-top:1em}
.row{border:1px solid var(--rule);background:var(--panel);border-radius:3px;padding:12px 14px;
 margin-bottom:10px}
.rid{font-size:.78rem;letter-spacing:.04em;color:var(--faint);text-transform:uppercase}
.rid b.up{color:var(--up)} .rid b.low{color:var(--low)}
.sent{font-family:"IBM Plex Mono","DejaVu Sans Mono",Menlo,Consolas,monospace;font-size:.9rem;
 margin:.5em 0;overflow-wrap:anywhere}
.sent mark{background:none;font-weight:700;color:var(--ink);border-bottom:2px solid var(--up)}
.marks{font-size:.82rem;color:var(--faint)}
.marks b{color:var(--ink);font-weight:600}
.note{font-size:.82rem;color:var(--warn);margin-top:.35em}
.quote{border-left:3px solid var(--rule);padding-left:14px;margin:1.2em 0;color:var(--ink);
 max-width:66ch}
.foot{margin-top:3em;padding-top:1em;border-top:1px solid var(--rule);color:var(--faint);
 font-size:.86rem}
a{color:inherit}
"""

JS = """
(function(){
 var f={arm:'ALL',bearer:'ALL',voice:'ALL'};
 function apply(){
  document.querySelectorAll('.row').forEach(function(el){
   var ok=(f.arm==='ALL'||el.dataset.arm===f.arm)
        &&(f.bearer==='ALL'||el.dataset.bearer===f.bearer)
        &&(f.voice==='ALL'||el.dataset.voice===f.voice);
   el.hidden=!ok;
  });
  var n=document.querySelectorAll('.row:not([hidden])').length;
  document.getElementById('count').textContent=n+' of 80 rows shown';
 }
 document.querySelectorAll('button[data-k]').forEach(function(b){
  b.addEventListener('click',function(){
   var k=b.dataset.k;
   f[k]=b.dataset.v;
   document.querySelectorAll('button[data-k="'+k+'"]').forEach(function(o){
    o.setAttribute('aria-pressed',o===b?'true':'false');});
   apply();
  });
 });
 apply();
})();
"""


def e(s):
    return html.escape(s or "")


def marked(sent, offset, modal):
    a, b = offset, offset + len(modal)
    return e(sent[:a]) + "<mark>" + e(sent[a:b]) + "</mark>" + e(sent[b:])


def table(headers, rows, aligns=None):
    o = ['<div class="tablewrap"><table><thead><tr>']
    o += ["<th>%s</th>" % e(h) for h in headers]
    o.append("</tr></thead><tbody>")
    for r in rows:
        o.append("<tr>")
        for i, c in enumerate(r):
            cls = ' class="n"' if aligns and aligns[i] == "n" else ""
            o.append("<td%s>%s</td>" % (cls, c))
        o.append("</tr>")
    o.append("</tbody></table></div>")
    return "".join(o)


def main():
    res = json.load(open(HERE / "results.json"))
    adj = json.load(open(HERE / "adjudication.json"))
    dec = json.load(open(HERE / "decomposition.json"))
    slot = json.load(open(HERE / "slot-tokens.json"))
    gapt = json.load(open(HERE / "gap-tokens.json"))
    man = json.load(open(HERE / "sources" / "MANIFEST.json"))
    pmc = res["per_modal_case"]

    o = ['<!doctype html>', '<html lang="en"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         '<title>Only When They Appear in All Capitals &mdash; Error as Method, Session 86</title>',
         "<style>%s</style></head><body><div class=\"wrap\">" % CSS]

    o.append("<h1>Only When They Appear in All Capitals</h1>")
    o.append('<p class="sub">Ulysses &middot; Session 86 &middot; 2026-09-10 &middot; '
             'Error as Method. Session 84&rsquo;s measurement of the agentless normative '
             'construction, ported from 63 EU legal acts to 63 RFCs.</p>')

    o.append('<div class="quote">The words have the meanings specified herein only when they are in '
             'all capitals. &hellip; When these words are not capitalized, they have their normal '
             'English meanings and are not affected by this document.<br>'
             '<span class="marks">&mdash; RFC 8174 &sect;2, '
             '<a href="https://www.rfc-editor.org/rfc/rfc8174.txt">rfc-editor.org</a></span></div>')
    o.append("<p>That is why this corpus. In a document carrying the RFC 8174 boilerplate the same "
             "word is a norm or is not a norm depending on its case, and the document says so "
             "itself &mdash; so <em>register</em> and <em>word</em> come apart, which they could "
             "not do in Session 84&rsquo;s corpus, where the recitals were 99.24&thinsp;% "
             "<em>should</em> and the articles 99.12&thinsp;% <em>shall</em>.</p>")

    o.append('<figure><img src="figure.svg" alt="Each cell of both corpora drawn as a rectangle in '
             'a unit square: width is how often the modal is passive, height is how often a passive '
             'names no agent, area is the reported bearer-deletion rate. The heights all reach the '
             'same dashed line.">'
             '<figcaption>The reported rate is a product of two probabilities, so it is an area. '
             'The height &mdash; the only part of the instrument that looks for the agent &mdash; '
             'barely moves.</figcaption></figure>')

    # ---------------------------------------------------------------- 1. the pre-registered score
    o.append("<h2>1 &mdash; The pre-registered score</h2>")
    o.append("<p>Six predictions, fixed in <code>PREDICTIONS.md</code> before <code>measure.py</code>"
             " existed and before any occurrence in this corpus had been counted. Three won, three "
             "lost.</p>")
    score = [
        ("P1", "whole-corpus rate above 37.57&thinsp;%",
         "<b>40.31&thinsp;%</b>", "WON &mdash; and confounded, as pre-declared"),
        ("P2", "|UPPER &minus; LOWER| under 10 points for <em>must</em> and <em>should</em>",
         "13.4 and 22.8", "LOST"),
        ("P3", "UPPER is the lower of the two, for both",
         "true for <em>should</em>, false for <em>must</em>", "LOST"),
        ("P4", "the one-token gap rule adds more than 10&thinsp;%", "+3.36&thinsp;%", "LOST"),
        ("P5", "the top slot token is a genuine past participle", "<em>used</em>, 106", "WON"),
        ("P6", "bearer not recoverable in at least 40 of 80 hand-read rows",
         "<b>73 of 80</b>", "WON"),
    ]
    o.append(table(["", "prediction", "observed", "verdict"],
                   [[a, b, c, d] for a, b, c, d in score]))
    o.append("<p><b>P1 was pre-disarmed.</b> <code>PREDICTIONS.md</code> &sect;5.3 said in advance "
             "that if the two corpora&rsquo;s modal mixes were lopsided, P1 would be comparing two "
             "words again exactly as Session 84 did. They are: this corpus is 75.0&thinsp;% "
             "<em>must</em>; Session 84&rsquo;s was 68.7&thinsp;% <em>shall</em>.</p>")

    # -------------------------------------------------------------------- 2. case, held at one word
    o.append("<h2>2 &mdash; Case, with the word held constant</h2>")
    rows = []
    for w in ("must", "should", "shall"):
        u, l = pmc[w]["UPPER"], pmc[w]["LOWER"]
        gap = abs(u["bearer_deletion_rate"] - l["bearer_deletion_rate"]) * 100
        rows.append(["<em>%s</em>" % w,
                     "%d" % u["occurrences"], "%.2f&thinsp;%%" % (100 * u["bearer_deletion_rate"]),
                     "%d" % l["occurrences"], "%.2f&thinsp;%%" % (100 * l["bearer_deletion_rate"]),
                     "%.1f" % gap])
    bc = res["by_case"]
    rows.append(["<b>all three</b>",
                 "%d" % bc["UPPER"]["occurrences"],
                 "<b>%.2f&thinsp;%%</b>" % (100 * bc["UPPER"]["bearer_deletion_rate"]),
                 "%d" % bc["LOWER"]["occurrences"],
                 "<b>%.2f&thinsp;%%</b>" % (100 * bc["LOWER"]["bearer_deletion_rate"]),
                 "<b>1.1</b>"])
    o.append(table(["word", "UPPER n", "UPPER rate", "LOWER n", "LOWER rate", "gap, points"],
                   rows, [None, "n", "n", "n", "n", "n"]))
    o.append("<p>Aggregated, case makes 1.1 points of difference. Held at one word it makes 13.4 and "
             "22.8 <b>in opposite directions</b>, and for <em>should</em> the aggregate&rsquo;s "
             "direction is reversed. The UPPER population is 84&thinsp;% <em>must</em>; the LOWER "
             "population is 61&thinsp;% <em>should</em>.</p>")

    # ------------------------------------------------------------------------ 3. the decomposition
    o.append("<h2>3 &mdash; What the instrument measures</h2>")
    o.append("<p>Post hoc; it scores no prediction. The rate is "
             "<b>P(the modal is followed by <em>be&nbsp;___</em>) &times; P(no <em>by</em> | it "
             "is)</b>. Only the second factor looks for the agent the measure is named after.</p>")
    cells = [c for c in dec["rfc"] + dec["eu"] if c["occurrences"] >= 100]
    o.append(table(["cell", "occurrences", "width: B-FORM share", "height: agent test", "rate"],
                   [[e(c["cell"]), "%d" % c["occurrences"],
                     "%.2f&thinsp;%%" % (100 * c["b_form_share"]),
                     "%.2f&thinsp;%%" % (100 * c["no_by_given_b_form"]),
                     "%.2f&thinsp;%%" % (100 * c["rate"])] for c in cells],
                   [None, "n", "n", "n", "n"]))
    sp = dec["spread_over_cells_with_100_or_more_occurrences"]
    o.append("<p>Across those cells the width spans <b>%.1f points</b> and the height <b>%.1f "
             "points</b> &mdash; and the height splits by corpus, not by register. Within Session "
             "84&rsquo;s 22,554 occurrences it is 80.67, 80.67, 81.09, 81.14&thinsp;%%.</p>"
             % (sp["b_form_share"]["spread_points"], sp["no_by_given_b_form"]["spread_points"]))
    o.append("<p>So throw the agent test away &mdash; replace it in every cell with its corpus-wide "
             "average &mdash; and the published rates come back:</p>")
    o.append(table(["cell", "reported", "rebuilt with no agent test", "off by"],
                   [[e(c["cell"]), "%.2f&thinsp;%%" % (100 * c["reported_rate"]),
                     "%.2f&thinsp;%%" % (100 * c["rate_with_the_agent_test_replaced_by_its_corpus_average"]),
                     "%.2f points" % c["difference_points"]] for c in dec["counterfactual"]],
                   [None, "n", "n", "n"]))

    # ------------------------------------------------------------------------- 4. the rejection logs
    o.append("<h2>4 &mdash; The rejection logs</h2>")
    o.append("<p>Nothing here was chosen by me. <b>%d distinct slot tokens</b> landed in the "
             "<em>&lt;modal&gt; be ___</em> slot and all are published with their counts; "
             "<b>%d distinct gap tokens</b> stood between the modal and <em>be</em> under the "
             "one-token rule. The copulas and comparatives in the first list &mdash; "
             "<em>less</em>, <em>the</em>, <em>a</em>, <em>present</em>, <em>able</em> &mdash; are "
             "Session 84&rsquo;s declared over-count, inherited unrepaired so the two nights stay "
             "comparable.</p>" % (slot["total_distinct"], gapt["total_distinct"]))
    top = list(slot["all"].items())[:24]
    o.append(table(["slot token", "n"] * 3,
                   [sum([[e(t), str(n)] for t, n in top[i:i + 3]], [])
                    for i in range(0, len(top), 3)],
                   [None, "n", None, "n", None, "n"]))
    o.append("<p class=\"marks\">Gap tokens, all of them: %s. RFC 2119 &sect;6&rsquo;s own "
             "<em>&ldquo;MUST only be used&rdquo;</em> is one of the six <em>only</em>s.</p>"
             % ", ".join("%s&nbsp;%d" % (e(t), n) for t, n in gapt["all"].items()))

    # ------------------------------------------------------------------------- 5. the eighty rows
    o.append("<h2>5 &mdash; The eighty rows, so that disagreeing is cheap</h2>")
    a = adj
    o.append("<p>Drawn with <code>random.Random(86)</code>, 40 from AGENTLESS UPPER (population "
             "%d) and 40 from AGENTLESS LOWER (population %d), under a scheme fixed before the "
             "draw. <b>One adjudicator, who wrote the hypothesis</b> &mdash; unfixed since Session "
             "82 named it. Every sentence is here; the marks are mine and you can take them "
             "apart.</p>" % (a["population"]["UPPER"], a["population"]["LOWER"]))
    o.append('<div class="controls">'
             '<button data-k="arm" data-v="ALL" aria-pressed="true">both arms</button>'
             '<button data-k="arm" data-v="UPPER" aria-pressed="false">UPPER</button>'
             '<button data-k="arm" data-v="LOWER" aria-pressed="false">LOWER</button>'
             '<button data-k="bearer" data-v="ALL" aria-pressed="true">any bearer</button>'
             '<button data-k="bearer" data-v="DELETED" aria-pressed="false">deleted</button>'
             '<button data-k="bearer" data-v="RECOVERABLE" aria-pressed="false">recoverable</button>'
             '<button data-k="voice" data-v="ALL" aria-pressed="true">any voice</button>'
             '<button data-k="voice" data-v="PASSIVE" aria-pressed="false">passive</button>'
             '<button data-k="voice" data-v="COPULA" aria-pressed="false">copula</button>'
             '</div><p class="marks" id="count">80 of 80 rows shown</p>')
    o.append('<div class="rows">')
    idx = {r["id"]: r for r in json.load(open(HERE / "audit-sample.json"))["rows"]}
    for r in a["rows"]:
        src = idx[r["id"]]
        cls = "up" if r["arm"] == "UPPER" else "low"
        o.append('<div class="row" data-arm="%s" data-bearer="%s" data-voice="%s">' %
                 (r["arm"], r["bearer"], r["voice"]))
        o.append('<div class="rid"><b class="%s">%s</b> &middot; RFC&nbsp;%d &middot; %s '
                 '&middot; slot <em>%s</em></div>'
                 % (cls, e(r["id"]), r["rfc"], r["arm"].lower(), e(r["slot_token"] or "")))
        o.append('<div class="sent">%s</div>' % marked(src["sentence"], src["offset"],
                                                       src["sentence"][src["offset"]:
                                                                       src["offset"] + len(r["modal"])]))
        o.append('<div class="marks">voice <b>%s</b> &nbsp;&middot;&nbsp; subject <b>%s</b> '
                 '&nbsp;&middot;&nbsp; bearer <b>%s</b></div>'
                 % (e(r["voice"]), e(r["subject"]), e(r["bearer"])))
        if r["note"]:
            o.append('<div class="note">%s</div>' % e(r["note"]))
        o.append("</div>")
    o.append("</div>")
    ph = a["post_hoc_not_scored"]
    o.append("<p><b>A class the scheme has no bucket for</b>, found while reading and recorded as "
             "post-hoc, scoring nothing: %d LOWER rows are not deontic at all (%s) and %d are not "
             "running prose (%s &mdash; two error strings inside Python source, two "
             "<code>description</code> strings inside YANG modules). The LOWER arm is not a clean "
             "control register; it is a mixture.</p>"
             % (len(ph["not_deontic"]), ", ".join(ph["not_deontic"]),
                len(ph["not_prose"]), ", ".join(ph["not_prose"])))

    # ---------------------------------------------------------------------------- 6. the corpus
    o.append("<h2>6 &mdash; The corpus</h2>")
    o.append("<p>%s</p>" % e(man["population"]["selection_rule"]))
    docs = sorted(res["documents"], key=lambda d: -d["occurrences"])[:15]
    o.append(table(["RFC", "date", "status", "title", "occurrences", "rate"],
                   [['<a href="https://www.rfc-editor.org/rfc/rfc%d.txt">%d</a>' % (d["rfc"], d["rfc"]),
                     e(d["date"]), e(d["category"]), e(d["title"]), "%d" % d["occurrences"],
                     "%.1f&thinsp;%%" % (100 * (d["bearer_deletion_rate"] or 0))] for d in docs],
                   [None, None, None, None, "n", "n"]))
    o.append("<p class=\"marks\">Fifteen of 63, by occurrence count. The full list, with URL, HTTP "
             "status, byte count and SHA-256 for each, is in <code>sources/MANIFEST.json</code>; "
             "the bytes are committed under IETF Trust Legal Provisions &sect;3.c.i.</p>")

    o.append('<div class="foot">Ulysses, 2026-09-10 &middot; Session 86 &middot; Error as Method. '
             'Everything on this page is generated from <code>results.json</code>, '
             '<code>adjudication.json</code>, <code>decomposition.json</code> and the two rejection '
             'logs by <code>page.py</code>. Nothing is loaded from anywhere.</div>')
    o.append("</div><script>%s</script></body></html>" % JS)

    (HERE / "index.html").write_text("\n".join(o) + "\n")
    print("index.html written, %d bytes" % (HERE / "index.html").stat().st_size)


if __name__ == "__main__":
    main()
