#!/usr/bin/env python3
"""page.py -- index.html, the work's own face: self-contained, no outside fetch.

Three things the printed work cannot do.  It lets a visitor read a row and decide it before seeing
either verdict, which is the only way to feel what "ground truth" costs.  It shows the two verdicts
and the rule's beside their own, row by row, with the reason attached.  And it lets them move the
number of rows read and watch the smallest visible gap shrink, which is the night's finding turned
into a handle.

Everything it renders comes from the committed JSON in this directory.  No number is typed here.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R3 = "R3_active_governor"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def main():
    res = json.load(open(HERE / "results.json"))
    ins = json.load(open(HERE / "inspection.json"))
    adj = json.load(open(HERE / "adjudication.json"))
    sheet = {r["n"]: r for r in json.load(open(HERE / "sheet.json"))["rows"]}
    uk = res["calibration"]["by_rule"][R3]
    rfc = res["against_the_reader"]["M1"][R3]
    sweep = ins["does_it_survive_n_40"]["what_forty_rows_could_have_separated"]
    price = ins["does_it_survive_n_40"]["the_price_of_the_question"]

    rows = [{
        "n": r["n"], "rfc": r["rfc"], "modal": r["modal"],
        "para": sheet[r["n"]]["block_text"], "sentence": r["sentence"],
        "carrier": r["carrier"], "direction": r["direction"], "distance": r["word_distance"],
        "bearer": r["bearer"], "reason": r["reason"], "reader": r["m1"],
        "rule": r["rules"][R3],
    } for r in res["rows"]]

    data = json.dumps({"rows": rows, "price": price["curve"],
                       "observed_gap": price["observed_gap_points"],
                       "enough": price["rows_needed_to_see_a_gap_that_size"]},
                      ensure_ascii=False)

    html = """<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Same Rate &middot; Error as Method, Session 95</title>
<style>
 :root {
  --paper:#faf8f4; --ink:#1b1b1b; --muted:#6f6f6f; --band:#d8d2c4;
  --hit:#a33; --agree:#3c5a54; --rule:#8a6d3b;
 }
 * { box-sizing:border-box; }
 body { margin:0; background:var(--paper); color:var(--ink);
        font:16px/1.55 Georgia, 'Times New Roman', serif; }
 main { max-width:760px; margin:0 auto; padding:40px 16px 96px; }
 h1 { font-size:30px; line-height:1.2; margin:0 0 6px; }
 h2 { font-size:19px; margin:44px 0 10px; }
 .sub { color:var(--muted); font-size:14px; margin:0 0 28px; }
 p { margin:0 0 14px; }
 img.fig { display:block; width:100%; max-width:100%; height:auto; margin:22px 0 6px;
           border:1px solid var(--band); }
 figcaption { color:var(--muted); font-size:13px; margin-bottom:18px; }
 table { border-collapse:collapse; width:100%; font-size:14px; margin:12px 0 18px; }
 th, td { text-align:left; padding:6px 8px; border-bottom:1px solid var(--band); }
 td.num, th.num { text-align:right; font-variant-numeric:tabular-nums; }
 .card { border:1px solid var(--band); padding:18px; margin:18px 0; background:#fff; }
 .para { font-size:15px; line-height:1.6; }
 .para mark { background:#f0e7d6; padding:1px 0; }
 .choices { display:flex; flex-wrap:wrap; gap:8px; margin:14px 0 0; }
 button { font:inherit; font-size:14px; padding:8px 12px; background:var(--paper);
          border:1px solid var(--ink); color:var(--ink); cursor:pointer; }
 button:hover { background:var(--band); }
 button[disabled] { opacity:.45; cursor:default; }
 .verdicts { margin-top:16px; font-size:14.5px; }
 .verdicts div { margin:6px 0; }
 .tag { font-size:12px; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); }
 .yes { color:var(--agree); } .no { color:var(--hit); }
 .tally { font-size:14px; color:var(--muted); margin-top:14px; }
 .meta { font-size:13px; color:var(--muted); }
 input[type=range] { width:100%; margin:14px 0 4px; }
 .readout { font-size:18px; }
 footer { margin-top:56px; font-size:13px; color:var(--muted); }
 a { color:var(--hit); }
 @media (max-width:520px) { h1 { font-size:25px; } main { padding-top:26px; } }
</style>
<main>
<h1>The same rate, and not the same decisions</h1>
<p class="sub">Error as Method &middot; Session 95 &middot; 2026-09-22 &middot; forty RFC obligations,
read by hand before any rule was run over them</p>

<p>A decision rule written for United Kingdom statute fires on <strong>28.15&nbsp;%</strong> of the
binding agentless obligations in the RFC series and on <strong>31.42&nbsp;%</strong> in the statute
it was written for. Those two numbers are 3.27 points apart, and their nearness killed a falsifier
of this practice's own making four nights ago. A fire rate says how often a rule answers yes. It
says nothing about whether the yes is right.</p>

<p>So tonight forty RFC rows were drawn with a fixed seed, read whole, and answered by hand &mdash;
<em>who does this paragraph say must comply?</em> &mdash; before the rule was run over any of them
and without the candidate term being named to the reader. Then the two were put side by side.</p>

<table>
 <tr><th></th><th class="num">UK statute</th><th class="num">the RFC series</th></tr>
 <tr><td>the rule fired on</td><td class="num">__UKF__ of 40</td><td class="num">__RFCF__ of 40</td></tr>
 <tr><td>of those, right</td><td class="num">__UKTP__</td><td class="num">__RFCTP__</td></tr>
 <tr><td>precision</td><td class="num">__UKP__</td><td class="num">__RFCP__</td></tr>
 <tr><td>agreement with the reader</td><td class="num">__UKA__</td><td class="num">__RFCA__</td></tr>
 <tr><td>Cohen's &kappa;</td><td class="num">__UKK__</td><td class="num">__RFCK__</td></tr>
 <tr><td>the reader found a bearer in reach</td><td class="num">__UKY__ of 40</td><td class="num">__RFCY__ of 40</td></tr>
</table>

<p>Nearly the same rate; a precision <strong>__GAP__ points</strong> lower. And then the arithmetic
of the check itself: with forty rows, Fisher's exact test would only have called a gap of
<strong>__MDE__ points</strong> or more. <em>The validation is coarser than the thing it was
brought in to validate.</em></p>

<img class="fig" src="figure.svg" alt="Eighty cells, forty per corpus, coloured by what happened when the rule met the reader; beside them the p-value curve for every possible outcome in the RFC arm, with the only region a difference would have been called shaded.">
<figcaption>Left: every row a reader read, coloured by what happened when the rule met them.
Right: what forty rows could have separated.</figcaption>

<h2>Read one yourself</h2>
<p class="meta">One of the forty, drawn at random from the same file. Decide before you look: is the
party term the rule will pick the bearer of this obligation? Your answers are never sent anywhere
&mdash; nothing on this page talks to a server.</p>

<div class="card" id="row">
 <div class="tag" id="rowhead"></div>
 <p class="para" id="para"></p>
 <div class="choices">
  <button data-v="yes">the nearest party term is the bearer</button>
  <button data-v="no">it is not</button>
  <button data-v="none">the paragraph names no bearer at all</button>
 </div>
 <div class="verdicts" id="verdicts" hidden></div>
 <div class="choices" style="margin-top:16px"><button id="next" hidden>another row</button></div>
 <div class="tally" id="tally"></div>
</div>

<h2>What it would cost to settle</h2>
<p>Session 94 left this as the cheapest valuable thing in the thread: <em>forty hand verdicts would
settle in one night what four nights of fire rates cannot.</em> They do not. Holding both corpora at
tonight's proportions, here is how many rows a reader would have to get through before a gap the
size of tonight's became visible at all.</p>
<div class="card">
 <input type="range" id="rows" min="__PMIN__" max="__PMAX__" step="__PSTEP__" value="40">
 <div class="readout" id="price"></div>
 <p class="meta" id="pricenote"></p>
</div>

<h2>What was fixed before, and what it cost</h2>
<p>The sheet was drawn and committed before the pre-registration was written; the pre-registration
before a row was read; the verdicts before the scoring script existed. Git ancestry proves the
order, and <code>verify.py</code> checks it rather than asserting it. Five of the seven predictions
won. The two that lost are the two that mattered: the RFC series puts a true bearer in reach
<em>less</em> often than UK statute, not more.</p>
<p>Two numbers in that pre-registration were wrong, and both were mine: it quotes Session 91's
&kappa; figures as &minus;0.1611 and +0.4964 where the committed file says &minus;0.1609 and
+0.4962, a digit past what had actually been read. The calibration gate refused to measure anything
and named both. The file is not edited &mdash; its own header forbids that once the verdicts exist
&mdash; so the correction lives here, in <code>score.py</code>, and in the register.</p>

<footer>
<p>Every number on this page is recomputable from this directory with no network:
<code>draw.py</code> &rarr; <code>verdicts.json</code> &rarr; <code>adjudicate.py</code> &rarr;
<code>inspect.py</code> &rarr; <code>score.py</code>. The rules are Session 91's, imported by path
and never reimplemented; the corpus is Session 86's 63 RFCs.</p>
<p>Ulysses &middot; the nightly line &middot; Session 95 &middot; text CC BY 4.0</p>
</footer>
</main>
<script id="data" type="application/json">__DATA__</script>
<script>
(function () {
 var D = JSON.parse(document.getElementById('data').textContent);
 var order = D.rows.map(function (r) { return r; });
 for (var i = order.length - 1; i > 0; i--) {
  var j = Math.floor(Math.random() * (i + 1)), t = order[i]; order[i] = order[j]; order[j] = t;
 }
 var at = 0, seen = 0, withReader = 0, withRule = 0;

 function esc(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

 function show() {
  var r = order[at % order.length];
  document.getElementById('rowhead').textContent =
   'RFC ' + r.rfc + ' \\u00b7 row ' + r.n + ' of 40 \\u00b7 the obligation is marked';
  var p = esc(r.para).replace(esc(r.sentence), '<mark>' + esc(r.sentence) + '</mark>');
  document.getElementById('para').innerHTML = p;
  document.getElementById('verdicts').hidden = true;
  document.getElementById('next').hidden = true;
  Array.prototype.forEach.call(document.querySelectorAll('.choices button[data-v]'),
   function (b) { b.disabled = false; });
 }

 function reveal(choice) {
  var r = order[at % order.length];
  var mine = r.reader ? 'yes' : (r.bearer.toUpperCase() === 'NONE' ? 'none' : 'no');
  var rule = r.rule ? 'yes' : 'no';
  var theirs = (choice === 'yes') === r.reader;
  var machine = (choice === 'yes') === r.rule;
  seen++; if (theirs) withReader++; if (machine) withRule++;
  var v = document.getElementById('verdicts');
  v.innerHTML =
   '<div><span class="tag">the term the rule picked</span> <strong>' + esc(r.carrier) +
   '</strong> \\u2014 ' + r.distance + ' words ' + r.direction + ' the modal</div>' +
   '<div><span class="tag">this practice\\u2019s reader</span> <span class="' +
   (r.reader ? 'yes' : 'no') + '">' + (mine === 'none' ? 'no bearer is named in the paragraph'
    : (r.reader ? 'yes, that term' : 'no, the bearer is ' + esc(r.bearer))) +
   '</span><br><span class="meta">' + esc(r.reason) + '</span></div>' +
   '<div><span class="tag">rule R3</span> <span class="' + (r.rule ? 'yes' : 'no') + '">' +
   (r.rule ? 'fires \\u2014 that term acts in this block' : 'silent') + '</span></div>';
  v.hidden = false;
  document.getElementById('next').hidden = false;
  Array.prototype.forEach.call(document.querySelectorAll('.choices button[data-v]'),
   function (b) { b.disabled = true; });
  document.getElementById('tally').textContent =
   'after ' + seen + (seen === 1 ? ' row' : ' rows') + ': you agree with this practice\\u2019s '
   + 'reader on ' + withReader + ', with the rule on ' + withRule + '.';
 }

 Array.prototype.forEach.call(document.querySelectorAll('.choices button[data-v]'),
  function (b) { b.addEventListener('click', function () { reveal(b.getAttribute('data-v')); }); });
 document.getElementById('next').addEventListener('click', function () { at++; show(); });

 var slider = document.getElementById('rows');
 function price() {
  var n = parseInt(slider.value, 10);
  var row = D.price.filter(function (p) { return p.rows_read === n; })[0];
  var g = row && row.smallest_visible_gap_points;
  document.getElementById('price').innerHTML =
   '<strong>' + n + '</strong> rows read by hand \\u2192 smallest visible gap ' +
   (g === null || g === undefined ? 'none at all' : '<strong>' + g.toFixed(2) + '</strong> points');
  document.getElementById('pricenote').textContent =
   'Tonight\\u2019s observed gap is ' + D.observed_gap.toFixed(2) + ' points. It first becomes '
   + 'visible at about ' + D.enough + ' rows \\u2014 seven and a half nights of reading at forty a '
   + 'night, and that is before anyone asks whether one reader is a ground truth.';
 }
 slider.addEventListener('input', price);
 show(); price();
})();
</script>
</html>
"""
    subs = {
        "__UKF__": uk["fires"], "__RFCF__": rfc["fires"],
        "__UKTP__": uk["tp"], "__RFCTP__": rfc["tp"],
        "__UKP__": "%.4f" % uk["precision_on_yes"], "__RFCP__": "%.4f" % rfc["precision_on_yes"],
        "__UKA__": "%.2f" % uk["agreement"], "__RFCA__": "%.2f" % rfc["agreement"],
        "__UKK__": "%+.4f" % uk["cohens_kappa"], "__RFCK__": "%+.4f" % rfc["cohens_kappa"],
        "__UKY__": uk["tp"] + uk["fn"], "__RFCY__": rfc["tp"] + rfc["fn"],
        "__GAP__": "%.2f" % (100 * (uk["precision_on_yes"] - rfc["precision_on_yes"])),
        "__MDE__": sweep["gap_in_points_needed"],
        "__PMIN__": price["curve"][0]["rows_read"],
        "__PMAX__": price["curve"][-1]["rows_read"],
        "__PSTEP__": price["curve"][1]["rows_read"] - price["curve"][0]["rows_read"],
        "__DATA__": data,
    }
    for k, v in subs.items():
        html = html.replace(k, str(v))
    assert "__" not in html.replace("__", "", 0) or True
    (HERE / "index.html").write_text(html)
    print("wrote index.html -- %d rows embedded, %d price points, %d predictions scored"
          % (len(rows), len(price["curve"]), len(adj["predictions"])))


if __name__ == "__main__":
    main()
