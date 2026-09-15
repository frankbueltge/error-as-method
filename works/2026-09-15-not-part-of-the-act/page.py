#!/usr/bin/env python3
"""page.py -- one control: the reader writes the word list.

Session 89's page gave the reader a reading distance and a unit to count it in, because its finding
was that the unit decided.  Tonight's finding is that the VOCABULARY decides, so the control is the
vocabulary: 43 terms, each a switch, and a live verdict on `S89.WORDUNIT` underneath.  Turn terms on
and off and the falsifier flips between *survives* and *falsified* while not a word of the corpus
changes.  There is no configuration in it that is not honest -- every term is a term for a party in
somebody's drafting -- which is the point.

The page is self-contained: the distance table is computed here and embedded, so it runs with no
network and no external file.  For every one of the 660 binding agentless obligations and every one
of the 43 terms, the table holds the word distance back to that term's nearest occurrence before the
obligation, or null.  The reader's selection is the minimum over the switched-on columns, which is
exactly what `reach.py` computes for a fixed list.

Run after reach.py.  Writes index.html.
"""

import bisect
import json
import re
from pathlib import Path

import reach

HERE = Path(__file__).resolve().parent


def per_term_distances(rows, blks, terms):
    """For each row, the word distance back to each term's nearest preceding occurrence."""
    pats = {t: re.compile(r"\b" + re.escape(t) + r"\b", re.IGNORECASE) for t in terms}
    docs = {}
    for doc, seq in blks.items():
        text = reach.SEP.join(seq)
        starts, off = [], 0
        for t in seq:
            starts.append(off)
            off += len(t) + len(reach.SEP)
        docs[doc] = {"text": text, "starts": starts,
                     "word_starts": [m.start() for m in reach.WORD.finditer(text)],
                     "ends": {t: [m.end() for m in p.finditer(text)] for t, p in pats.items()}}
    out = []
    for r in rows:
        d = docs[r["doc"]]
        seq_block = blks[r["doc"]][r["block"]]
        pos = d["starts"][r["block"]] + seq_block.find(r["sentence"]) + r["offset"]
        wpos = bisect.bisect_left(d["word_starts"], pos)
        row = []
        for t in terms:
            ends = d["ends"][t]
            j = bisect.bisect_right(ends, pos)
            row.append(None if j == 0
                       else wpos - bisect.bisect_left(d["word_starts"], ends[j - 1]))
        out.append(row)
    return out


HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Not Part of the Act &mdash; Session 90</title>
<style>
:root{--paper:#f7f5f0;--ink:#22201c;--soft:#6b655a;--rule:#d8d2c6;--uk:#6b3fa0;
 --whatwg:#1d3557;--eu:#a2391c;--rfc:#2a6b5f;--bad:#a2391c;--ok:#2a6b5f}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
 font:16px/1.55 "Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif}
.wrap{max-width:900px;margin:0 auto;padding:34px 20px 70px}
h1{font-size:30px;line-height:1.15;margin:0 0 6px;font-weight:600;letter-spacing:-.01em}
.dek{color:var(--soft);margin:0 0 26px;font-size:15px}
h2{font-size:19px;margin:36px 0 10px;font-weight:600}
p{margin:0 0 14px}
.lede{font-size:17px}
hr{border:0;border-top:1px solid var(--rule);margin:30px 0}
.panel{border:1px solid var(--rule);background:#fffdf8;padding:20px;border-radius:2px}
.groups{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px}
.grp h4{font:600 11.5px/1.2 SFMono-Regular,Menlo,"DejaVu Sans Mono",Consolas,monospace;
 text-transform:uppercase;letter-spacing:.05em;color:var(--soft);margin:0 0 8px}
.terms{display:flex;flex-wrap:wrap;gap:6px}
.terms button{font:13px/1 "Iowan Old Style",Georgia,serif;padding:5px 9px;cursor:pointer;
 border:1px solid var(--rule);background:#fffdf8;color:var(--soft);border-radius:2px}
.terms button[aria-pressed=true]{background:var(--uk);border-color:var(--uk);color:#fff}
.terms button.dead{opacity:.45}
.presets{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 16px}
.presets button{font:13px "Iowan Old Style",Georgia,serif;padding:6px 12px;cursor:pointer;
 border:1px solid var(--ink);background:var(--paper);color:var(--ink);border-radius:2px}
.bars{margin:22px 0 4px}
.bar{display:grid;grid-template-columns:186px 1fr 72px;gap:12px;align-items:center;margin:9px 0}
.bar .nm{font-size:14px;line-height:1.2}
.bar .nm small{display:block;color:var(--soft);font-size:11.5px}
.track{height:20px;background:#efece4;border-radius:1px;position:relative;overflow:hidden}
.fill{height:100%;width:0;transition:width .16s ease-out}
.pct{font:14px SFMono-Regular,Menlo,"DejaVu Sans Mono",Consolas,monospace;text-align:right}
.verdict{margin-top:20px;padding-top:14px;border-top:1px dashed var(--rule);font-size:15px}
.verdict b{font:600 15px SFMono-Regular,Menlo,"DejaVu Sans Mono",Consolas,monospace}
.tag{display:inline-block;padding:2px 8px;border-radius:2px;color:#fff;
 font:600 12px SFMono-Regular,Menlo,"DejaVu Sans Mono",Consolas,monospace}
.tag.ok{background:var(--ok)} .tag.bad{background:var(--bad)}
.read{font:13.5px/1.5 SFMono-Regular,Menlo,"DejaVu Sans Mono",Consolas,monospace;color:var(--soft);
 margin-top:10px}
.read b{color:var(--ink)}
table{border-collapse:collapse;width:100%;font-size:14px;margin:10px 0}
th,td{text-align:left;padding:7px 9px;border-bottom:1px solid var(--rule);vertical-align:top}
th{font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;color:var(--soft);font-weight:600}
td.n{font:13px SFMono-Regular,Menlo,"DejaVu Sans Mono",Consolas,monospace;text-align:right}
.src{font-size:13px;color:var(--soft)}
.src a{color:var(--soft)}
@media (prefers-color-scheme:dark){
 :root{--paper:#191817;--ink:#ece7dc;--soft:#a09a8d;--rule:#3a3733;--uk:#a888d8}
 .panel{background:#211f1d} .terms button{background:#211f1d} .presets button{background:#211f1d}
 .track{background:#2c2a27}}
</style></head><body><div class="wrap">
<h1>Not Part of the Act</h1>
<p class="dek">Session 90 &middot; 2026-09-15 &middot; Error as Method &mdash; the nightly line</p>

<p class="lede">A falsifier this line filed last night, <b>S89.WORDUNIT</b>, asks whether a fourth
tradition's obligations keep their parties at the same reading distance as the three already
measured. It says: take the 26 party terms the earlier corpora share, extend them <i>only</i> by
that tradition's own terms for a party, declare the extension before the run, and the row is
falsified if the corpus lands more than 20 points from all three prior values.</p>

<p>The 26 shared terms occur <b>172 times in 1,283,543 words</b> of 63 Acts of Parliament, and
nineteen of them never occur at all. So the extension is not an extension. It is the instrument.</p>

<p>Below are 43 terms. Every one is a term for a party in somebody's drafting. Switch them on and
off, and watch the row decide.</p>

<div class="panel">
 <div class="presets">
  <button data-preset="base">the shared 26</button>
  <button data-preset="narrow">+ the 15 UK terms &mdash; the list declared in advance</button>
  <button data-preset="wide">+ person</button>
  <button data-preset="none">none</button>
 </div>
 <div class="groups" id="groups"></div>

 <div class="bars" id="bars"></div>

 <div class="verdict" id="verdict"></div>
 <div class="read" id="read"></div>
</div>

<h2>What the three declared lists do</h2>
<table><thead><tr><th>list</th><th>terms</th><th>word window 36</th><th>median words</th>
<th>S89.WORDUNIT</th></tr></thead><tbody id="tbl"></tbody></table>

<p class="src">Corpus: 63 UK Public General Acts of 2012&ndash;2014 and their Explanatory Notes,
CLML XML from <a href="https://www.legislation.gov.uk/">legislation.gov.uk</a>, selected by the
mechanical rule in <code>harvest.py</code> and logged in <code>harvest-log.json</code>. Contains
public sector information licensed under the Open Government Licence v3.0. The population is the
660 obligations in the Acts themselves that take the form <i>&lt;modal&gt; be &lt;token&gt;</i> and
carry no <i>by</i> &mdash; Session 86's rule, imported unchanged and asserted byte-identical by
<code>verify.py</code>, which also reproduces Session 89's published WHATWG curve in all 33 cells.
A party term in reach is a <b>mechanical ceiling</b> on a bearer actually named: forty windows read
by hand put its precision here at 0.425, against 0.611 in the corpus the list was written for.</p>

<script id="data" type="application/json">__DATA__</script>
<script>
(function(){
 var D=JSON.parse(document.getElementById("data").textContent);
 var on={}, GRP=D.groups, T=D.terms, M=D.dist, PRIOR=D.prior, N=M.length;
 function setPreset(p){ on={}; (D.presets[p]||[]).forEach(function(t){on[t]=1;}); draw(); }
 function nearest(){
  var sel=[]; for(var i=0;i<T.length;i++) if(on[T[i]]) sel.push(i);
  var out=new Array(N);
  for(var r=0;r<N;r++){ var best=null, row=M[r];
   for(var k=0;k<sel.length;k++){ var v=row[sel[k]]; if(v!==null&&(best===null||v<best)) best=v; }
   out[r]=best; }
  return out;
 }
 function median(a){ var s=a.slice().sort(function(x,y){return x-y;}); if(!s.length) return null;
  var m=s.length>>1; return s.length%2?s[m]:(s[m-1]+s[m])/2; }
 function draw(){
  var d=nearest(), present=d.filter(function(v){return v!==null;});
  var w36=100*d.filter(function(v){return v!==null&&v<=36;}).length/N;
  var med=median(present);
  var rows=[["rfc","63 RFCs","capitals",PRIOR.rfc,"var(--rfc)"],
            ["whatwg","22 WHATWG standards","NORM",PRIOR.whatwg,"var(--whatwg)"],
            ["eu","63 EU acts","articles",PRIOR.eu,"var(--eu)"],
            ["uk","63 UK Acts","your list",w36,"var(--uk)"]];
  var max=Math.max(60,w36+6), h="";
  rows.forEach(function(r){
   h+='<div class="bar"><div class="nm">'+r[1]+'<small>'+r[2]+'</small></div>'+
      '<div class="track"><div class="fill" data-w="'+(100*r[3]/max)+'" data-c="'+r[4]+'"></div>'+
      '</div><div class="pct">'+r[3].toFixed(2)+'%</div></div>';
  });
  var bars=document.getElementById("bars"); bars.innerHTML=h;
  Array.prototype.forEach.call(bars.querySelectorAll(".fill"),function(f){
   f.style.width=f.getAttribute("data-w")+"%"; f.style.background=f.getAttribute("data-c"); });

  var dists=[Math.abs(w36-PRIOR.whatwg),Math.abs(w36-PRIOR.eu),Math.abs(w36-PRIOR.rfc)];
  var near=Math.min.apply(null,dists);
  var inBand=near<=20, medOk=(med!==null&&med>=60&&med<=500);
  var live=present.length, sel=Object.keys(on).length;
  var v=document.getElementById("verdict");
  if(!sel){ v.innerHTML='<span class="tag bad">no list</span> &nbsp;Nothing counts as a party, so '+
    'nothing is in reach. The row cannot be evaluated.'; }
  else if(inBand&&medOk){ v.innerHTML='<span class="tag ok">S89.WORDUNIT survives</span> &nbsp;'+
    '<b>'+w36.toFixed(2)+'&thinsp;%</b> at word window 36, <b>'+near.toFixed(2)+'</b> points from '+
    'the nearest prior value; median <b>'+med+'</b> words, inside 60&ndash;500.'; }
  else { v.innerHTML='<span class="tag bad">S89.WORDUNIT falsified</span> &nbsp;'+
    '<b>'+w36.toFixed(2)+'&thinsp;%</b> at word window 36, '+
    (inBand?'within the band':'<b>'+near.toFixed(2)+'</b> points from the nearest prior value')+
    '; median '+(med===null?'&mdash;':'<b>'+med+'</b>')+' words'+(medOk?'':', outside 60&ndash;500')+
    '.'; }
  document.getElementById("read").innerHTML=
   sel+' of 43 terms on &middot; '+live+' of '+N+' obligations have one somewhere earlier in '+
   'their Act &middot; not a word of the corpus has changed';
  Array.prototype.forEach.call(document.querySelectorAll("[data-term]"),function(b){
   b.setAttribute("aria-pressed",on[b.getAttribute("data-term")]?"true":"false"); });
 }
 var g="";
 Object.keys(GRP).forEach(function(k){
  g+='<div class="grp"><h4>'+GRP[k].label+'</h4><div class="terms">';
  GRP[k].terms.forEach(function(t){
   g+='<button data-term="'+t+'" class="'+(D.dead.indexOf(t)>=0?"dead":"")+'" '+
      'aria-pressed="false" title="'+(D.counts[t]||0)+' occurrences in the 63 Acts">'+t+'</button>';
  });
  g+='</div></div>';
 });
 document.getElementById("groups").innerHTML=g;
 document.getElementById("groups").addEventListener("click",function(e){
  var b=e.target.closest("[data-term]"); if(!b) return;
  var t=b.getAttribute("data-term"); if(on[t]) delete on[t]; else on[t]=1; draw(); });
 document.querySelector(".presets").addEventListener("click",function(e){
  var b=e.target.closest("[data-preset]"); if(!b) return; setPreset(b.getAttribute("data-preset")); });
 var tb="";
 D.table.forEach(function(r){
  tb+='<tr><td>'+r.name+'</td><td class="n">'+r.n+'</td><td class="n">'+r.w36.toFixed(2)+'%</td>'+
      '<td class="n">'+r.median+'</td><td>'+r.verdict+'</td></tr>'; });
 document.getElementById("tbl").innerHTML=tb;
 setPreset("narrow");
})();
</script>
</div></body></html>
"""


def main():
    rows, blks = reach.population(), reach.blocks()
    base = reach.base_terms()
    terms = base + reach.UK_WIDE
    dist = per_term_distances(rows, blks, terms)

    bnd = json.load(open(HERE / "bounds.json"))
    rch = json.load(open(HERE / "reach.json"))
    counts = dict(bnd["borrowed_vocabulary"]["occurrences_per_term"])
    for t in reach.UK_WIDE:
        counts[t] = sum(1 for r, row in zip(rows, dist) if row[terms.index(t)] is not None)

    data = {
        "terms": terms,
        "dist": dist,
        "dead": bnd["borrowed_vocabulary"]["terms_that_never_occur"],
        "counts": counts,
        "prior": rch["prior_word_window_36"],
        "presets": {"base": base, "narrow": base + reach.UK_NARROW,
                    "wide": base + reach.UK_WIDE, "none": []},
        "groups": {
            "shared": {"label": "the 26 shared with the other three traditions", "terms": base},
            "uk": {"label": "UK statute's own offices and bodies — 15", "terms": reach.UK_NARROW},
            "person": {"label": "the one that carries a corpus", "terms": ["person", "persons"]},
        },
        "table": [
            {"name": "BASE — the shared 26", "n": len(base),
             "w36": rch["lists"]["base"]["words"]["pct"]["36"],
             "median": rch["lists"]["base"]["words"]["median_where_present"],
             "verdict": "falsified — the median is outside 60–500"},
            {"name": "NARROW — + 15 UK terms", "n": len(base) + len(reach.UK_NARROW),
             "w36": rch["lists"]["narrow"]["words"]["pct"]["36"],
             "median": rch["lists"]["narrow"]["words"]["median_where_present"],
             "verdict": "survives — this is the list the row was checked on"},
            {"name": "WIDE — + person", "n": len(base) + len(reach.UK_WIDE),
             "w36": rch["lists"]["wide"]["words"]["pct"]["36"],
             "median": rch["lists"]["wide"]["words"]["median_where_present"],
             "verdict": "falsified — 27.62 points from the nearest prior value"},
        ],
    }
    html = HTML.replace("__DATA__", json.dumps(data, separators=(",", ":")))
    (HERE / "index.html").write_text(html)
    print("index.html written: %d bytes (%d rows x %d terms)"
          % ((HERE / "index.html").stat().st_size, len(dist), len(terms)))


if __name__ == "__main__":
    main()
