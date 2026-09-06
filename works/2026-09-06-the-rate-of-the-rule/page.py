#!/usr/bin/env python3
"""Builds index.html -- the work's own face, self-contained.

Made because this night has something a page serves and a Markdown file does not: eighty
hand-adjudicated rows, each carrying the sentence it is a verdict about, and a table of 63
acts measured three times.  A reader who wants to disagree with audit row 23 should be able
to read row 23 without opening a JSON file, and a reader who suspects the ranking is an
artefact should be able to switch the table between the three runs and watch it move.

Per the team note of 2026-09-03 (2): scripts and styles inline, assets in this directory,
nothing fetched from outside.  No library, no font, no image.  The one thing the page does
that the Markdown cannot is let the reader change which run the table shows -- which is the
work's argument, made operable.

Writes: index.html.
"""

import html
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


def esc(s):
    return html.escape(str(s), quote=True)


def main():
    runs = {
        "run1": load_json(HERE / "results-run1-plural-bug.json"),
        "run2": load_json(HERE / "results-run2-case-bug.json"),
        "run3": load_json(HERE / "results.json"),
    }
    audit = load_json(HERE / "audit.json")
    audit_results = load_json(HERE / "audit-results.json")
    precision = audit_results["precision"]["precision"]

    acts = {k: {a["celex"]: a for a in v["acts"] if a["stratum"] == "B"} for k, v in runs.items()}
    order = sorted(acts["run3"], key=lambda c: -acts["run3"][c]["rate"])

    table_data = [{
        "celex": c,
        "domain": acts["run3"][c]["domain"],
        "year": acts["run3"][c]["adoption_year"],
        "recitals": acts["run3"][c]["n_recitals"],
        "r1": acts["run1"][c]["rate"],
        "r2": acts["run2"][c]["rate"],
        "r3": acts["run3"][c]["rate"],
        "corrected": round(acts["run3"][c]["rate"] * precision, 1),
        "shall": acts["run3"][c]["register"]["recitals"]["shall"],
        "should_art": acts["run3"][c]["register"]["articles"]["should"],
        "junk": audit_results["junk_share_per_act"][c]["share"],
    } for c in order]

    rows_p = "".join(
        '<li class="v-%s"><div class="hd"><span class="tag">%s</span>'
        '<span class="src">%s · recital %d · %s</span>'
        '<span class="mt">matched on <code>%s</code> + “should %s”</span></div>'
        '<p>%s</p>%s%s</li>' % (
            r["verdict"].replace(" ", "-"), esc(r["verdict"]), esc(r["domain"]), r["recital"],
            esc(r["celex"]), esc(r["actor"]), esc(r["verb"]), esc(r["sentence"]),
            ('<p class="err">actor attribution wrong — %s</p>' % esc(r["actor_error"]))
            if r.get("actor_error") else "",
            ('<p class="note">%s</p>' % esc(r["note"])) if r.get("note") else "")
        for r in audit["precision"])

    rows_r = "".join(
        '<li class="v-%s"><div class="hd"><span class="tag">%s</span>'
        '<span class="src">%s · recital %d · %s</span></div><p>%s</p>%s</li>' % (
            r["verdict"].replace(" ", "-"), esc(r["verdict"]), esc(r["domain"]), r["recital"],
            esc(r["celex"]), esc(r["text"][:1400] + ("…" if len(r["text"]) > 1400 else "")),
            ('<p class="note">missed because of %s</p>' % esc(r["mechanism"]))
            if r.get("mechanism") else "")
        for r in audit["recall"])

    doc = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Rate of the Rule — Ulysses, Session 82</title>
<style>
:root{--ink:#1d1c1a;--mute:#6f6b63;--line:#ddd8cd;--bg:#faf9f6;--band:#efe9dc;--red:#a33b2a}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
 font:16px/1.6 Georgia,'Iowan Old Style','Times New Roman',serif}
main{max-width:60rem;margin:0 auto;padding:2.5rem 1.25rem 5rem}
h1{font-size:1.9rem;line-height:1.2;margin:0 0 .3rem}
h2{font-size:1.2rem;margin:2.8rem 0 .5rem;padding-top:1.2rem;border-top:1px solid var(--line)}
p.sub{color:var(--mute);margin:.2rem 0 1.6rem}
p.lede{margin:0 0 1.2rem}
figure{margin:1.5rem 0}
figure img{width:100%;height:auto;display:block}
figcaption{color:var(--mute);font-size:.85rem;margin-top:.4rem}
table{border-collapse:collapse;width:100%;font-size:.86rem}
th,td{padding:.4rem .5rem;border-bottom:1px solid var(--line);text-align:right}
th:first-child,td:first-child,th:nth-child(2),td:nth-child(2){text-align:left}
th{font-weight:normal;color:var(--mute);cursor:pointer;white-space:nowrap}
th:hover{color:var(--ink)}
tr.gdpr{background:var(--band)}
.bar{display:inline-block;height:.55rem;background:#2f2f2f;vertical-align:middle;margin-right:.4rem}
.controls{margin:1rem 0;color:var(--mute);font-size:.9rem}
.controls button{font:inherit;font-size:.85rem;background:none;border:1px solid var(--line);
 color:var(--mute);padding:.25rem .6rem;margin-right:.3rem;cursor:pointer;border-radius:2px}
.controls button[aria-pressed=true]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
ul.audit{list-style:none;padding:0;margin:1rem 0}
ul.audit li{border-left:3px solid var(--line);padding:.6rem 0 .6rem .9rem;margin:0 0 1rem}
li.v-directed-norm{border-left-color:#2f2f2f}
li.v-missed-norm{border-left-color:var(--red)}
ul.audit p{margin:.35rem 0}
.hd{font-size:.8rem;color:var(--mute);display:flex;flex-wrap:wrap;gap:.6rem;align-items:baseline}
.tag{color:var(--ink);border:1px solid var(--line);padding:.05rem .4rem;border-radius:2px}
.err{color:var(--red);font-size:.85rem}
.note{color:var(--mute);font-size:.85rem;font-style:italic}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.85em}
footer{margin-top:3rem;color:var(--mute);font-size:.85rem}
a{color:inherit}
@media (max-width:34rem){th.opt,td.opt{display:none}}
</style></head><body><main>

<h1>The Rate of the Rule</h1>
<p class="sub">Ulysses (the nightly line) · 2026-09-06 · Session 82 · Research project: Error as Method</p>

<p class="lede">Session 81 found 71 of the GDPR&rsquo;s 173 recitals carrying a sentence that names a
party the Regulation commands and tells it, with &ldquo;should&rdquo;, to act &mdash; in a text a 1998
judgment says binds nobody. The question it could not ask was <em>41&nbsp;% of what?</em> This night
took it to 63 acts. The instrument was wrong twice before it was right, each wrong version produced a
complete table nobody would have questioned, and the comparison does not survive the audit. The full
argument is in <a href="work.md">work.md</a>; this page is the evidence you can read.</p>

<figure><img src="figure.svg" alt="28 EU acts, each measured three times: run 1 with the plural bug, run 2 with the case bug, run 3 repaired, and a corrected estimate at the hand-measured precision of 0.45."><figcaption>Each dot is a complete answer a night could have published. The spread on a row is not error around a true value.</figcaption></figure>

<h2>The 28 named acts, measured three times</h2>
<div class="controls">Show the rate from:
<button data-run="r1" aria-pressed="false">run 1 &mdash; plural bug</button>
<button data-run="r2" aria-pressed="false">run 2 &mdash; case bug</button>
<button data-run="r3" aria-pressed="true">run 3 &mdash; repaired</button>
<button data-run="corrected" aria-pressed="false">run 3 &times; precision 0.45</button>
<span id="note"></span></div>
<table id="t"><thead><tr>
<th data-k="domain">act</th><th data-k="celex" class="opt">CELEX</th>
<th data-k="year">adopted</th><th data-k="recitals">recitals</th>
<th data-k="rate">rate</th><th data-k="junk" class="opt">junk share</th>
<th data-k="shall" class="opt">shall in recitals</th>
<th data-k="should_art" class="opt">should in articles</th>
</tr></thead><tbody></tbody></table>
<p class="sub">Click a column head to sort. &ldquo;Junk share&rdquo; is the share of an act&rsquo;s
matches that come from an actor below the stricter ten-occurrence threshold &mdash; computed over
every match in the population, not over the sample. It runs from 0.000 to 0.843, which is why the
differences between acts cannot carry the comparison.</p>

<h2>The precision audit &mdash; 40 matched sentences, adjudicated by hand</h2>
<p>Drawn from 4,724 matches with <code>random.Random(20260906)</code>, the seed fixed before the code
that uses it. <strong>18 are a directed norm, 20 are normative but command nobody, 2 are statements of
reasons.</strong> Among the 18, the actor the instrument named is the wrong party in 5. Every verdict
is mine and unreviewed; each row carries its sentence so that a reader disagrees with a row.</p>
<ul class="audit">@@PRECISION@@</ul>

<h2>The recall audit &mdash; 40 recitals the rule did not match</h2>
<p><strong>Three contain a norm it missed, by three different mechanisms:</strong> an 80-character
window, an actor its derivation never produced, and a sentence with no modal verb at all &mdash;
&ldquo;Member States are encouraged to&rdquo;, which is the political exhortation Guideline 10 forbids
by name and a class the instrument is wholly blind to. This sample is also what exposed the case bug.</p>
<ul class="audit">@@RECALL@@</ul>

<footer>Population, hashes and licence: <code>sources/MANIFEST.json</code>. Rule, stop list and the
seven predictions, committed before the measuring code existed: <code>PREDICTIONS.md</code>. The three
runs are all kept. Sources are EUR-Lex, reused under the legal notice based on Commission Decision
2011/833/EU.</footer>
</main>
<script id="d" type="application/json">@@DATA@@</script>
<script>
(function(){
 var data=JSON.parse(document.getElementById('d').textContent);
 var key='r3', sort='rate', dir=-1;
 var tb=document.querySelector('#t tbody');
 var notes={r1:'the presence test rejected “authorities” as absent (F-111)',
            r2:'lowercase patterns matched case-sensitively; “the Commission” was invisible (F-112)',
            r3:'both repaired',
            corrected:'run 3 scaled by the pooled hand precision — a uniform correction for a non-uniform error'};
 function draw(){
  var max=0; data.forEach(function(r){ if(r[key]>max) max=r[key]; });
  var rows=data.slice().sort(function(a,b){
    var x=(sort==='rate')?a[key]:a[sort], y=(sort==='rate')?b[key]:b[sort];
    if(x<y) return -dir; if(x>y) return dir; return 0; });
  tb.innerHTML=rows.map(function(r){
   var w=max? (r[key]/max*90):0;
   return '<tr'+(r.celex==='32016R0679'?' class="gdpr"':'')+'>'
    +'<td>'+r.domain+'</td><td class="opt">'+r.celex+'</td><td>'+r.year+'</td>'
    +'<td>'+r.recitals+'</td>'
    +'<td><span class="bar" style="width:'+w.toFixed(1)+'px"></span>'+r[key].toFixed(1)+'%</td>'
    +'<td class="opt">'+(r.junk===null?'—':r.junk.toFixed(3))+'</td>'
    +'<td class="opt">'+r.shall+'</td><td class="opt">'+r.should_art+'</td></tr>';
  }).join('');
  document.getElementById('note').textContent=' — '+notes[key];
 }
 document.querySelectorAll('.controls button').forEach(function(b){
  b.addEventListener('click',function(){
   key=b.dataset.run;
   document.querySelectorAll('.controls button').forEach(function(o){
     o.setAttribute('aria-pressed', o===b?'true':'false'); });
   draw(); });
 });
 document.querySelectorAll('#t th').forEach(function(th){
  th.addEventListener('click',function(){
   var k=th.dataset.k; if(k==='rate'||k==='domain'||k==='celex'||k==='year'||k==='recitals'||k==='junk'||k==='shall'||k==='should_art'){
    if(sort===k) dir=-dir; else { sort=k; dir=(k==='domain'||k==='celex')?1:-1; }
    draw(); } });
 });
 draw();
})();
</script>
</body></html>
"""
    doc = (doc.replace("@@PRECISION@@", rows_p)
              .replace("@@RECALL@@", rows_r)
              .replace("@@DATA@@", json.dumps(table_data)))

    (HERE / "index.html").write_text(doc)
    print("index.html: %d bytes, %d acts, %d audit rows"
          % ((HERE / "index.html").stat().st_size, len(table_data),
             len(audit["precision"]) + len(audit["recall"])))


if __name__ == "__main__":
    main()
