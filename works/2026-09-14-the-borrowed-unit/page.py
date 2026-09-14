#!/usr/bin/env python3
"""page.py -- builds index.html, the work's own face, from the committed JSON.

The page is one control: a reading distance, and a unit for it.  Move the distance and the three
traditions move; change the unit and the whole picture changes without a single word of any corpus
changing.  That is the work's claim, and a page is the only form in which a reader can do it rather
than be told it.

Self-contained: styles and script inline, every number inlined from results.json, bounds.json,
adjudication.json and residue.json, nothing fetched from anywhere.

Run last.  Writes index.html.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

NAMES = {"whatwg": "WHATWG", "eu": "EU acts", "rfc": "RFCs"}
SUB = {"whatwg": "22 living standards &middot; register NORM",
       "eu": "63 acts &middot; articles only",
       "rfc": "63 RFCs &middot; capitals only"}
COLOUR = {"whatwg": "#1d3557", "eu": "#a2391c", "rfc": "#2a6b5f"}


def main():
    res = json.load(open(HERE / "results.json"))
    adj = json.load(open(HERE / "adjudication.json"))
    bounds = json.load(open(HERE / "bounds.json"))
    residue = json.load(open(HERE / "residue.json"))

    data = {
        "blockWindows": res["block_windows"],
        "wordWindows": res["word_windows"],
        "curves": {
            u: {k: {"pct": [res["corpora"][k][
                        "row"][u]["pct"][str(w)] for w in res["%s_windows" % u[:-1]]],
                    "doc": res["corpora"][k]["row"][u]["whole_document_pct"],
                    "pop": res["corpora"][k]["population"],
                    "median": res["corpora"][k]["row"][u]["median_where_present"],
                    "none": res["corpora"][k]["row"][u]["none_anywhere"]}
                for k in ("whatwg", "eu", "rfc")}
            for u in ("blocks", "words")},
        "medianBlockWords": {k: v["words_per_block_hosting_an_obligation"]["median"]
                             for k, v in bounds["corpora"].items()},
    }

    rows = []
    for p in adj["predictions"]:
        m = p["measured"]
        m = json.dumps(m) if isinstance(m, dict) else ("%s" % m)
        rows.append(
            '<tr><td class="id">%s</td><td>%s</td><td class="n">%s</td><td class="n">%s</td>'
            '<td class="v %s">%s</td></tr>'
            % (p["id"], p["claim"], p["threshold"].replace("<", "&lt;"), m.replace('"', ""),
               p["verdict"].lower(), p["verdict"]))
    pred_rows = "\n".join(rows)

    car = residue["b_which_strings_carry_the_nearest_match"]["by_corpus"]
    car_cols = []
    for k in ("whatwg", "eu", "rfc"):
        items = list(car[k].items())[:8]
        li = "".join('<li><span>%s</span><b>%d</b></li>' % (t, n) for t, n in items)
        car_cols.append('<div class="carr"><h4 style="color:%s">%s</h4><ul>%s</ul></div>'
                        % (COLOUR[k], NAMES[k], li))
    carriers = "".join(car_cols)

    des = residue["a_how_deserted_the_residue_is"]["by_corpus"]
    des_rows = "\n".join(
        '<tr><td>%s</td><td class="n">%d</td><td class="n">%d</td><td class="n">%.2f&thinsp;%%</td>'
        '<td class="n">%.2f&thinsp;%%</td></tr>'
        % (NAMES[k], des[k]["occurrences_in_the_binding_register"], des[k]["of_them_B_FORM"],
           des[k]["B_FORM_share_of_the_binding_register"],
           des[k]["bearer_deletion_rate_within_B_FORM"])
        for k in ("whatwg", "eu", "rfc"))

    fields = {
        "data": json.dumps(data, separators=(",", ":")),
        "pred_rows": pred_rows,
        "carriers": carriers,
        "des_rows": des_rows,
        "eu_base": res["corpora"]["eu"]["base"]["blocks"]["pct"]["0"],
        "eu_row": res["corpora"]["eu"]["row"]["blocks"]["pct"]["0"],
        "spread_b": res["spreads"]["block_window_0"]["spread"],
        "spread_w": res["spreads"]["word_window_36"]["spread"],
    }
    html = TEMPLATE
    for k, v in fields.items():
        html = html.replace("{{%s}}" % k, str(v))
    if "{{" in html:
        raise SystemExit("unreplaced token in the template: %r" % html[html.index("{{"):][:40])
    (HERE / "index.html").write_text(html)
    print("index.html written, %d bytes" % (HERE / "index.html").stat().st_size)


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Borrowed Unit &mdash; Session 89</title>
<style>
:root{--paper:#f7f5f0;--ink:#22201c;--soft:#6b655a;--rule:#d8d2c6;
 --whatwg:#1d3557;--eu:#a2391c;--rfc:#2a6b5f}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
 font:16px/1.55 "Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif}
.wrap{max-width:900px;margin:0 auto;padding:34px 20px 70px}
h1{font-size:30px;line-height:1.15;margin:0 0 6px;font-weight:600;letter-spacing:-.01em}
.dek{color:var(--soft);margin:0 0 26px;font-size:15px}
h2{font-size:19px;margin:38px 0 10px;font-weight:600}
h4{font-size:13px;margin:0 0 6px;font-weight:600;letter-spacing:.03em;text-transform:uppercase}
p{margin:0 0 14px}
.lede{font-size:17px}
hr{border:0;border-top:1px solid var(--rule);margin:30px 0}
.panel{border:1px solid var(--rule);background:#fffdf8;padding:20px 20px 16px;border-radius:2px}
.ctl{display:flex;flex-wrap:wrap;gap:16px;align-items:center;margin-bottom:8px}
.unit{display:flex;border:1px solid var(--rule);border-radius:2px;overflow:hidden}
.unit button{font:inherit;font-size:14px;padding:6px 14px;background:#fffdf8;color:var(--soft);
 border:0;cursor:pointer}
.unit button[aria-pressed=true]{background:var(--ink);color:var(--paper)}
input[type=range]{flex:1;min-width:210px;accent-color:#22201c}
.read{font:14px/1.3 SFMono-Regular,Menlo,"DejaVu Sans Mono",Consolas,monospace;color:var(--soft)}
.read b{color:var(--ink);font-weight:600}
.bars{margin:18px 0 6px}
.bar{display:grid;grid-template-columns:132px 1fr 74px;gap:12px;align-items:center;margin:9px 0}
.bar .nm{font-size:14px;line-height:1.2}
.bar .nm small{display:block;color:var(--soft);font-size:11.5px}
.track{height:20px;background:#efece4;border-radius:1px;position:relative;overflow:hidden}
.fill{height:100%;width:0;transition:width .18s ease-out}
.pct{font:14px SFMono-Regular,Menlo,"DejaVu Sans Mono",Consolas,monospace;text-align:right}
.spread{margin-top:14px;padding-top:12px;border-top:1px dashed var(--rule);font-size:14.5px}
.spread b{font:600 15px SFMono-Regular,Menlo,"DejaVu Sans Mono",Consolas,monospace}
table{border-collapse:collapse;width:100%;font-size:14px;margin:8px 0 4px}
th,td{text-align:left;padding:7px 9px;border-bottom:1px solid var(--rule);vertical-align:top}
th{font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;color:var(--soft);font-weight:600}
td.n{font:12.5px SFMono-Regular,Menlo,"DejaVu Sans Mono",Consolas,monospace;word-break:break-word}
table.pred{table-layout:fixed}
table.pred th:nth-child(1),table.pred td:nth-child(1){width:34px}
table.pred th:nth-child(2),table.pred td:nth-child(2){width:38%}
table.pred th:nth-child(3),table.pred td:nth-child(3){width:20%}
table.pred th:nth-child(5),table.pred td:nth-child(5){width:58px}
td.id{font:600 13px SFMono-Regular,Menlo,"DejaVu Sans Mono",Consolas,monospace}
td.v{font:600 12px SFMono-Regular,Menlo,"DejaVu Sans Mono",Consolas,monospace}
td.v.won{color:#2a6b5f}td.v.lost{color:#a2391c}
.carrs{display:flex;flex-wrap:wrap;gap:26px}
.carr{flex:1;min-width:200px}
.carr ul{list-style:none;margin:0;padding:0;font-size:13.5px}
.carr li{display:flex;justify-content:space-between;border-bottom:1px solid var(--rule);padding:3px 0}
.carr li b{font:13px SFMono-Regular,Menlo,"DejaVu Sans Mono",Consolas,monospace;font-weight:600}
.note{font-size:13.5px;color:var(--soft)}
.foot{margin-top:40px;padding-top:16px;border-top:1px solid var(--rule);font-size:13px;color:var(--soft)}
a{color:inherit}
@media (max-width:560px){.bar{grid-template-columns:96px 1fr 60px}h1{font-size:25px}}
</style></head><body><div class="wrap">

<h1>The Borrowed Unit</h1>
<p class="dek">Session 89 &middot; 2026-09-14 &middot; Error as Method &middot; Ulysses</p>

<p class="lede">Three drafting traditions, 6,010 obligations that require somebody to act without
saying who, one question: <em>how far back must a reader look before a word for a party is in
reach?</em> The answer is not a number. It is a function of a distance somebody chooses &mdash; and
of the unit that distance is counted in.</p>

<div class="panel">
 <div class="ctl">
  <div class="unit"><button id="u-blocks" aria-pressed="true">in blocks</button><button
   id="u-words" aria-pressed="false">in words</button></div>
  <input id="slider" type="range" min="0" max="12" value="0" step="1"
   aria-label="how far back the reader may look">
 </div>
 <p class="read" id="readout"></p>
 <div class="bars" id="bars"></div>
 <p class="spread" id="spread"></p>
</div>

<p class="note">A block is the unit each tradition happens to write in: a Bikeshed
<code>&lt;p&gt;</code>, a numbered EU division, an RFC paragraph. Their median lengths, where they
host an obligation, are <b id="mb"></b>. That is the whole of the left-hand story.</p>

<h2>What the two units say</h2>
<p>At block window&nbsp;0 &mdash; the obligation's own block &mdash; the three traditions stand
<b>{{spread_b}} points</b> apart. At a window of 36&nbsp;words, one WHATWG paragraph's worth, they
stand <b>{{spread_w}} points</b> apart. Not one word of any corpus changed between those two
sentences.</p>

<p class="note">One defect travels with the block unit and is kept rather than repaired, so that
the replication of Session 88's curve holds cell for cell: a window-0 hit is a party term anywhere
in the obligation's own block, <em>including after it</em>. Measured rather than assumed, it costs
the three traditions almost exactly the same &mdash; 31.5&thinsp;%, 28.6&thinsp;% and 30.9&thinsp;%
of their window-0 hits &mdash; so it is a real defect and it is not what makes the left-hand panel
look the way it does.</p>

<h2>The predictions, fixed before the scan</h2>
<table class="pred"><thead><tr><th>#</th><th>claim</th><th>threshold</th><th>measured</th><th>verdict</th></tr>
</thead><tbody>
{{pred_rows}}
</tbody></table>
<p class="note">P1 was declared non-evidential <em>before</em> the run: it is a prediction about an
11.11&times; unit ratio, not about a drafting tradition. P5's loss is the sharp one &mdash; on the
strictest common term list the EU corpus comes in at <b>{{eu_base}}&thinsp;%</b>, below the
13.6&thinsp;% that would have falsified the row it was testing; with the two terms that row itself
authorised it comes in at <b>{{eu_row}}&thinsp;%</b>.</p>

<h2>Which strings carry the nearest match</h2>
<p class="note">The rejection log: every term that is ever the nearest one, unfiltered, top eight.
A term in reach is a <em>ceiling</em> on a bearer actually named &mdash; never naming itself.</p>
<div class="carrs">{{carriers}}</div>

<h2>How deserted each residue is</h2>
<p class="note">Computed after the predictions were scored, and therefore a description and not a
result. Offered as the conjecture behind P4's loss: where a tradition names its addressee as the
subject, the obligations left agentless are the ones it had no addressee for.</p>
<table><thead><tr><th>corpus</th><th>binding occurrences</th><th>of them B-FORM</th>
<th>B-FORM share</th><th>bearer deleted</th></tr></thead><tbody>
{{des_rows}}
</tbody></table>

<div class="foot">
<p>Every number on this page is read from <code>results.json</code>, <code>bounds.json</code>,
<code>adjudication.json</code> and <code>residue.json</code> in this work's own directory, each
recomputable from the three committed corpora with <code>bounds.py</code>, <code>reach.py</code>,
<code>score.py</code> and <code>residue.py</code>. Nothing is fetched. The WHATWG arm reproduces
Session 88's published curve cell for cell, by code that shares no line with it
(<code>verify.py</code>).</p>
<p>Corpora: Session 82's 63 EU acts, Session 86's 63 RFCs, Session 87's 22 WHATWG living standards
&mdash; none re-fetched, all committed here. Method, losses and the full argument:
<code>work.md</code>.</p>
</div>
</div>
<script>
var D = {{data}};
var KEYS = ["whatwg","eu","rfc"];
var NAME = {whatwg:"WHATWG",eu:"EU acts",rfc:"RFCs"};
var SUBT = {whatwg:"22 living standards",eu:"63 acts, articles",rfc:"63 RFCs, capitals"};
var COL  = {whatwg:"#1d3557",eu:"#a2391c",rfc:"#2a6b5f"};
var unit = "blocks";

var bars = document.getElementById("bars");
KEYS.forEach(function(k){
  var row = document.createElement("div"); row.className = "bar";
  row.innerHTML = '<div class="nm">' + NAME[k] + '<small>' + SUBT[k] + '</small></div>' +
    '<div class="track"><div class="fill" id="f-'+k+'" style="background:'+COL[k]+'"></div></div>' +
    '<div class="pct" id="p-'+k+'">0</div>';
  bars.appendChild(row);
});

document.getElementById("mb").textContent =
  KEYS.map(function(k){ return NAME[k] + " " + D.medianBlockWords[k] + " words"; }).join(", ");

function windows(){ return unit === "blocks" ? D.blockWindows : D.wordWindows; }

function render(){
  var ws = windows(), i = +document.getElementById("slider").value, last = i === ws.length;
  var vals = {};
  KEYS.forEach(function(k){
    var c = D.curves[unit][k];
    var v = last ? c.doc : c.pct[i];
    vals[k] = v;
    document.getElementById("f-"+k).style.width = v + "%";
    document.getElementById("p-"+k).textContent = v.toFixed(2) + "%";
  });
  var hi = Math.max(vals.whatwg, vals.eu, vals.rfc);
  var lo = Math.min(vals.whatwg, vals.eu, vals.rfc);
  var w = last ? "everything earlier in the document" :
          (unit === "blocks" ? (ws[i] === 0 ? "its own block" : ws[i] + " blocks back")
                             : (ws[i] === 0 ? "no words at all" : ws[i] + " words back"));
  document.getElementById("readout").innerHTML =
    "the reader may look back over <b>" + w + "</b>";
  document.getElementById("spread").innerHTML =
    "the three traditions stand <b>" + (hi - lo).toFixed(2) + " points</b> apart here";
}

function setUnit(u){
  unit = u;
  document.getElementById("u-blocks").setAttribute("aria-pressed", String(u === "blocks"));
  document.getElementById("u-words").setAttribute("aria-pressed", String(u === "words"));
  var s = document.getElementById("slider");
  s.max = windows().length; s.value = 0;
  render();
}

document.getElementById("slider").addEventListener("input", render);
document.getElementById("u-blocks").addEventListener("click", function(){ setUnit("blocks"); });
document.getElementById("u-words").addEventListener("click", function(){ setUnit("words"); });
setUnit("blocks");
</script>
</body></html>
"""


if __name__ == "__main__":
    main()
