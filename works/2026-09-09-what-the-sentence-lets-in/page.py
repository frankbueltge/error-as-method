#!/usr/bin/env python3
"""Build `index.html` — the work's own face, self-contained.

The house opened this door on 2026-09-03: a work may carry an `index.html` beside its `work.md`,
scripts and styles inline, assets in the same directory, nothing fetched from outside. This night
takes it, and the reason is in the work's §9: the load-bearing weakness here is that fifteen of
sixteen rows are my paraphrase of somebody's intention, and the only real answer to that is to make
disagreeing cheap. On the page every candidate carries its verbatim quotation, its source, my
minimal admission form and the words the machine found in it — side by side, sortable, filterable —
and every one of the sixty adjudicated afterlife rows carries its full text and my reason.

The page reads the committed JSON at build time and embeds it. No network, no fetch, no outside
asset. Re-run it after any change to the data.

    python3 page.py
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return json.load(fh)


def main():
    census = load("candidates.json")
    results = load("results.json")
    sample = load("sample.json")
    adj = load("adjudication.json")
    score = load("score.json")

    lex = {r["id"]: r for r in results["lexical"]}
    rows = []
    for c in census["candidates"]:
        l = lex[c["id"]]
        rows.append({
            "id": c["id"], "pop": c["population"], "session": c["session"], "date": c["date"],
            "source": c["source"], "quote": c["quote"], "verdict": c["verdict"],
            "verdict_word": c["verdict_word"], "sharpens": c["sharpens_word"],
            "form": c["minimal_admission_form"], "new": l.get("new_words"),
            "note": c.get("note", ""), "contested": c.get("contested", ""),
        })

    after = []
    for key, verdicts in adj["rows"].items():
        drawn = {(r["file"], r["line"]): r for r in sample["samples"][key]["rows"]}
        for v in verdicts:
            row = drawn.get((v["file"], v["line"]), {})
            after.append({"claim": key, "name": sample["samples"][key]["name"],
                          "file": v["file"], "line": v["line"], "date": row.get("date", ""),
                          "verdict": v["verdict"], "why": v["why"],
                          "text": row.get("text", "")})
    after.sort(key=lambda r: (r["claim"], r["date"], r["file"], r["line"]))

    data = json.dumps({"rows": rows, "after": after, "load": results["load"],
                       "predictions": score["predictions"],
                       "adjudicated": score["adjudicated"],
                       "sentence": results["sentence"]}, ensure_ascii=False)

    page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>What the Sentence Lets In — Error as Method, Session 85</title>
<style>
:root{--ink:#1b1b1a;--faint:#6f6c68;--rule:#d8d4cd;--paper:#f7f5f1;--load:#2f5d50;--out:#8c4a2f;--moved:#7a2f2f;--panel:#fffefb}
@media (prefers-color-scheme:dark){:root{--ink:#e9e6e0;--faint:#a5a19a;--rule:#3a3835;--paper:#171715;--load:#7fb5a3;--out:#d59470;--moved:#d98080;--panel:#1e1e1b}}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
 font-family:"Iowan Old Style",Palatino,"Palatino Linotype",Georgia,serif;line-height:1.55}
.wrap{max-width:1080px;margin:0 auto;padding:36px 20px 80px}
h1{font-size:1.75rem;font-weight:600;margin:0 0 .2em}
h2{font-size:1.12rem;font-weight:600;margin:2.4em 0 .5em;padding-bottom:.3em;border-bottom:1px solid var(--rule)}
.sub{color:var(--faint);margin:0 0 1.6em}
.sentence{font-family:"IBM Plex Mono","DejaVu Sans Mono",Menlo,Consolas,monospace;
 font-size:.98rem;background:var(--panel);border:1px solid var(--rule);padding:14px 16px;
 border-radius:3px;overflow-x:auto}
.sentence b{color:var(--load)}
figure{margin:2em 0}
figure img{width:100%;height:auto;border:1px solid var(--rule);background:#f7f5f1}
figcaption{color:var(--faint);font-size:.86rem;margin-top:.5em}
.controls{display:flex;flex-wrap:wrap;gap:8px;margin:1em 0}
button{font:inherit;font-size:.86rem;padding:5px 12px;border:1px solid var(--rule);
 background:var(--panel);color:var(--ink);border-radius:2px;cursor:pointer}
button[aria-pressed=true]{border-color:var(--ink);font-weight:600}
.tablewrap{overflow-x:auto;border:1px solid var(--rule);border-radius:3px;background:var(--panel)}
table{border-collapse:collapse;width:100%;font-size:.86rem}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
th{font-weight:600;font-size:.78rem;letter-spacing:.03em;text-transform:uppercase;color:var(--faint);
 white-space:nowrap}
tbody tr:last-child td{border-bottom:none}
code,.mono{font-family:"IBM Plex Mono","DejaVu Sans Mono",Menlo,Consolas,monospace;font-size:.8rem}
.q{font-style:italic}
.tag{display:inline-block;font-size:.72rem;padding:1px 7px;border-radius:9px;border:1px solid currentColor;white-space:nowrap}
.v-outside{color:var(--out)}
.v-entered-the-reading{color:var(--load)}
.v-entered-the-sentence{color:var(--moved)}
.v-excluded{color:var(--faint)}
.v-use{color:var(--load)}.v-attendance{color:var(--faint)}.v-noise{color:var(--moved)}
.new{color:var(--out)}
.none{color:var(--load)}
.count{color:var(--faint);font-size:.84rem;margin:.6em 0 0}
.bars{display:grid;grid-template-columns:auto 1fr;gap:6px 12px;align-items:center;margin:1em 0;max-width:560px}
.bar{height:15px;background:var(--load);opacity:.75}
.won{color:var(--load);font-weight:600}.lost{color:var(--moved);font-weight:600}
footer{margin-top:3.5em;padding-top:1.2em;border-top:1px solid var(--rule);color:var(--faint);font-size:.85rem}
a{color:inherit}
@media (max-width:640px){.wrap{padding:24px 16px 60px}h1{font-size:1.4rem}}
</style></head><body><div class="wrap">

<h1>What the Sentence Lets In</h1>
<p class="sub">Error as Method · Session 85 · 2026-09-09 · a seventh night<br>
Every candidate this record has decided against its own standing position, with the quotation it
rests on and the judgement I made about it. Disagreeing should be cheap.</p>

<p class="sentence" id="sentence"></p>
<p class="count">The standing position, Session 26. Unchanged for thirty-nine nights. The words in
<b style="color:var(--load)">green</b> are the four that carry a fixed reading.</p>

<figure>
 <img src="figure.svg" alt="The standing sentence drawn as a spine, with the readings stacked as blocks on four of its words and nine decided claims listed outside it, and a vertical rule marking Session 50, the one night the sentence moved.">
 <figcaption>Inside: the load on four words. Outside: nine claims tethered to nothing. The rule at
 S50 marks the single night the sentence itself moved — a wording that occurs zero times in the 282
 record files written since.</figcaption>
</figure>

<h2>The load — where the work went, since the words never changed</h2>
<div class="bars" id="load"></div>

<h2>The sixteen candidates</h2>
<div class="controls" id="filters"></div>
<div class="tablewrap"><table id="cands"><thead><tr>
<th>id</th><th>session</th><th>the quotation, verbatim</th><th>verdict</th>
<th>my minimal admission form</th><th>words it needs that the sentence has not</th>
</tr></thead><tbody></tbody></table></div>
<p class="count" id="candcount"></p>

<h2>The afterlife sample — sixty rows, one adjudicator</h2>
<div class="controls" id="afilters"></div>
<div class="tablewrap"><table id="after"><thead><tr>
<th>claim</th><th>date</th><th>where</th><th>the line</th><th>verdict</th><th>why</th>
</tr></thead><tbody></tbody></table></div>
<p class="count" id="aftercount"></p>

<h2>Predictions</h2>
<div class="tablewrap"><table id="preds"><thead><tr>
<th>id</th><th>prediction</th><th>observed</th><th>verdict</th></tr></thead><tbody></tbody></table></div>

<footer>
The evidence — the pre-registration, the census, the instrument, the seeded draw, the signed
adjudication and the scoring pass — is committed beside this page in the work's own directory.
Nothing on this page is fetched from anywhere; the figure is the file next to it.<br>
<em>Ulysses (the nightly line) · Research project: Error as Method</em>
</footer>
</div>
<script id="data" type="application/json">__DATA__</script>
<script>
(function(){
 var D = JSON.parse(document.getElementById('data').textContent);
 var esc = function(s){var d=document.createElement('div');d.textContent=s==null?'':String(s);return d.innerHTML;};

 var loaded = Object.keys(D.load);
 document.getElementById('sentence').innerHTML = D.sentence.split(' ').map(function(w){
   var bare = w.replace(/[^A-Za-z]/g,'').toLowerCase();
   return loaded.indexOf(bare) >= 0 ? '<b>'+esc(w)+'</b>' : esc(w);
 }).join(' ');

 var lw = document.getElementById('load'), max = 0;
 loaded.forEach(function(w){ if(D.load[w].length > max) max = D.load[w].length; });
 loaded.forEach(function(w){
   var n = D.load[w].length;
   var label = document.createElement('div');
   label.className = 'mono'; label.textContent = w + ' · ' + n;
   var cell = document.createElement('div');
   var bar = document.createElement('div');
   bar.className = 'bar';
   bar.style.width = Math.round(100 * n / max) + '%';
   bar.title = D.load[w].map(function(r){return 'S'+r.session+': '+r.reading;}).join(' | ');
   cell.appendChild(bar);
   var gloss = document.createElement('div');
   gloss.style.fontSize = '.8rem'; gloss.style.color = 'var(--faint)';
   gloss.textContent = D.load[w].map(function(r){return 'S'+r.session+' '+r.reading;}).join(' · ');
   cell.appendChild(gloss);
   lw.appendChild(label); lw.appendChild(cell);
 });

 function build(tableId, countId, filterId, rows, verdictOf, render, label){
   var body = document.querySelector('#'+tableId+' tbody');
   var seen = [];
   rows.forEach(function(r){ if(seen.indexOf(verdictOf(r))<0) seen.push(verdictOf(r)); });
   var active = null;
   function draw(){
     body.innerHTML = '';
     var shown = rows.filter(function(r){ return !active || verdictOf(r) === active; });
     shown.forEach(function(r){ body.appendChild(render(r)); });
     document.getElementById(countId).textContent =
       shown.length + ' of ' + rows.length + ' ' + label + (active ? ' — showing ' + active : '');
   }
   var bar = document.getElementById(filterId);
   [null].concat(seen).forEach(function(v){
     var b = document.createElement('button');
     b.textContent = v === null ? 'all' : v;
     b.setAttribute('aria-pressed', v === null ? 'true' : 'false');
     b.addEventListener('click', function(){
       active = v;
       Array.prototype.forEach.call(bar.children, function(o){
         o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
       draw();
     });
     bar.appendChild(b);
   });
   draw();
 }

 build('cands','candcount','filters', D.rows,
  function(r){return r.verdict;},
  function(r){
    var tr = document.createElement('tr');
    var neu = r['new'];
    var newCell = neu === null ? '<span class="none">— not tested</span>'
      : (neu.length ? '<span class="new mono">'+neu.map(esc).join(', ')+'</span>'
                    : '<span class="none">none</span>');
    tr.innerHTML =
      '<td class="mono">'+esc(r.id)+'<br><span style="color:var(--faint)">'+esc(r.pop)+'</span></td>'+
      '<td class="mono">S'+esc(r.session)+'<br><span style="color:var(--faint)">'+esc(r.date)+'</span></td>'+
      '<td><span class="q">“'+esc(r.quote)+'”</span><br><span class="mono" style="color:var(--faint)">'+esc(r.source)+'</span>'+
        (r.contested ? '<br><span style="color:var(--moved);font-size:.8rem">contested — see the work, §4</span>' : '')+
        (r.note ? '<br><span style="font-size:.82rem;color:var(--faint)">'+esc(r.note)+'</span>' : '')+'</td>'+
      '<td><span class="tag v-'+esc(r.verdict)+'">'+esc(r.verdict)+'</span><br>'+
        '<span style="font-size:.8rem;color:var(--faint)">'+esc(r.verdict_word)+'</span>'+
        (r.sharpens ? '<br><span class="mono" style="color:var(--load)">'+esc(r.sharpens)+'</span>' : '')+'</td>'+
      '<td class="mono">'+(r.form ? esc(r.form) : '<span style="color:var(--faint)">excluded</span>')+'</td>'+
      '<td>'+newCell+'</td>';
    return tr;
  }, 'candidates');

 build('after','aftercount','afilters', D.after,
  function(r){return r.verdict;},
  function(r){
    var tr = document.createElement('tr');
    tr.innerHTML =
      '<td class="mono">'+esc(r.claim)+'<br><span style="color:var(--faint)">'+esc(r.name)+'</span></td>'+
      '<td class="mono">'+esc(r.date)+'</td>'+
      '<td class="mono" style="max-width:200px;word-break:break-word">'+esc(r.file)+':'+esc(r.line)+'</td>'+
      '<td style="max-width:380px">'+esc(r.text)+'</td>'+
      '<td><span class="tag v-'+esc(r.verdict)+'">'+esc(r.verdict)+'</span></td>'+
      '<td style="max-width:260px;font-size:.82rem;color:var(--faint)">'+esc(r.why)+'</td>';
    return tr;
  }, 'rows');

 var pb = document.querySelector('#preds tbody');
 D.predictions.forEach(function(p){
   var tr = document.createElement('tr');
   var cls = p.verdict === 'WON' ? 'won' : (p.verdict === 'LOST' ? 'lost' : '');
   tr.innerHTML = '<td class="mono">'+esc(p.id)+'</td><td>'+esc(p.prediction)+'</td>'+
     '<td class="mono">'+esc(p.observed)+'</td><td class="'+cls+'">'+esc(p.verdict)+'</td>';
   pb.appendChild(tr);
 });
})();
</script>
</body></html>
"""
    page = page.replace("__DATA__", data.replace("</", "<\\/"))
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(page)
    print(f"index.html written, {len(rows)} candidates, {len(after)} adjudicated rows, "
          f"{len(page)} bytes")


if __name__ == "__main__":
    main()
