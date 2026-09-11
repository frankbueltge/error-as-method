#!/usr/bin/env python3
"""index.html -- Session 87, 2026-09-11.

The work's own face, per the team note of 2026-09-03 (2): a self-contained page, scripts and styles
inline, nothing fetched from outside. It exists for one reason -- every row this night judged is on
it, with its sentence, so that disagreeing with the adjudication costs a reader nothing but reading.
The figure and the argument live in work.md; this is the evidence.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def main():
    res = json.load(open(HERE / "results.json"))
    ag = json.load(open(HERE / "agentful.json"))
    fresh = json.load(open(HERE / "fresh-sample-scored.json"))
    held = json.load(open(HERE / "held-out.json"))
    lex = json.load(open(HERE / "lexicon.json"))
    w = res["whole_corpus"]

    v = ag["verdicts"]
    order = ["BEARER", "AGENT-NOT-BEARER", "OTHER-CLAUSE", "AGENT-IS-ARTEFACT", "NOT-AGENTIVE"]

    rows133 = "\n".join(
        '<tr data-v="%s"><td class="id">%s</td><td class="doc">%s</td>'
        '<td><span class="tag t-%s">%s</span></td><td class="s">%s</td></tr>'
        % (esc(r["verdict"]), esc(r["id"]), esc(r["doc"]),
           esc(r["verdict"]).lower().replace("-", ""), esc(r["verdict"]), esc(r["sentence"]))
        for r in ag["rows"])

    hand = {r["id"]: r for r in json.load(open(HERE / "adjudication.json"))["rows"]}
    rows60 = "\n".join(
        '<tr data-b="%s"><td class="id">%s</td><td class="doc">%s</td>'
        '<td><span class="tag t-%s">%s</span></td><td class="m">%s</td><td class="m">%s</td>'
        '<td class="m">%s</td><td class="s">%s%s</td></tr>'
        % (esc(r["hand_bearer"]), esc(r["id"]), esc(r["doc"]),
           "bearer" if r["hand_bearer"] == "RECOVERABLE" else "notagentive",
           esc(r["hand_bearer"]), esc(r["hand_voice"]), esc(r["rule_s"]), esc(r["rule_g"]),
           esc(r["sentence"]),
           ('<em class="note">' + esc(hand[r["id"]]["note"]) + "</em>")
           if hand[r["id"]]["note"] else "")
        for r in fresh["rows"])

    rows80 = "\n".join(
        '<tr data-b="%s"><td class="id">%s</td><td class="doc">RFC&nbsp;%s</td>'
        '<td><span class="tag t-%s">%s</span></td><td class="m">%s</td><td class="m">%s</td>'
        '<td class="s">%s</td></tr>'
        % (esc(r["hand_bearer"]), esc(r["id"]), esc(r["rfc"]),
           "bearer" if r["hand_bearer"] == "RECOVERABLE" else "notagentive",
           esc(r["hand_bearer"]), esc(r["rule_s"]), esc(r["rule_g"]), esc(r["sentence"]))
        for r in held["rows"])

    bars = "\n".join(
        '<div class="bar"><span class="lbl">%s</span>'
        '<span class="run t-%s" style="width:%.2f%%"></span><span class="n">%d</span></div>'
        % (k, k.lower().replace("-", ""), 100 * v[k] / ag["n_agentful"], v[k]) for k in order)

    css = """
:root{color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:#faf7f1;color:#1c1a17;
 font-family:"Iowan Old Style","Palatino Linotype",Palatino,Charter,Georgia,serif;
 line-height:1.55;font-size:16px}
.wrap{max-width:1080px;margin:0 auto;padding:48px 20px 80px}
h1{font-size:34px;margin:0 0 4px;font-weight:normal;letter-spacing:-.2px}
h2{font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:#6d685f;
 font-weight:normal;margin:54px 0 14px;border-bottom:1px solid #c9c2b6;padding-bottom:8px}
.sub{color:#6d685f;margin:0 0 26px;max-width:70ch}
p{max-width:78ch}
.big{display:flex;flex-wrap:wrap;gap:26px;margin:26px 0 10px}
.big div{min-width:120px}
.big b{display:block;font-size:30px;line-height:1.1}
.big span{color:#6d685f;font-size:12.5px}
.bar{display:flex;align-items:center;gap:10px;margin:5px 0;font-size:13px}
.bar .lbl{width:170px;flex:none;color:#6d685f}
.bar .run{height:16px;display:block;border:1px solid #1c1a17}
.bar .n{color:#1c1a17}
.t-bearer{background:#1c1a17}
.t-agentnotbearer{background:#f2eee5}
.t-otherclause{background:#ece7dc}
.t-agentisartefact{background:#d6cfc1}
.t-notagentive{background:#e4ded2}
table{border-collapse:collapse;width:100%;font-size:13.5px}
td,th{border-top:1px solid #e0dace;padding:8px 8px;vertical-align:top;text-align:left}
th{font-size:11.5px;letter-spacing:1px;text-transform:uppercase;color:#6d685f;font-weight:normal;
 border-top:none;border-bottom:1px solid #c9c2b6}
td.id{font-variant-numeric:tabular-nums;color:#6d685f;white-space:nowrap}
td.doc{color:#6d685f;white-space:nowrap}
td.m{color:#6d685f;font-size:12px;white-space:nowrap}
td.s{line-height:1.5}
.note{display:block;color:#6d685f;font-size:12px;margin-top:4px}
.tag{display:inline-block;padding:1px 7px;font-size:11px;letter-spacing:.4px;
 border:1px solid #1c1a17;white-space:nowrap}
.tag.t-bearer{color:#faf7f1}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 18px}
button{font:inherit;font-size:12.5px;padding:4px 12px;background:#faf7f1;color:#1c1a17;
 border:1px solid #c9c2b6;cursor:pointer}
button[aria-pressed="true"]{background:#1c1a17;color:#faf7f1;border-color:#1c1a17}
.scroll{overflow-x:auto}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;background:#efeae0;
 padding:1px 4px}
footer{margin-top:64px;color:#6d685f;font-size:12.5px;border-top:1px solid #c9c2b6;padding-top:16px}
a{color:#1c1a17}
@media (max-width:640px){.bar .lbl{width:110px}h1{font-size:27px}}
"""

    js = """
function wire(id, attr){
  var root=document.getElementById(id); if(!root) return;
  var btns=root.querySelectorAll('button');
  btns.forEach(function(b){
    b.addEventListener('click', function(){
      var want=b.getAttribute('data-want');
      btns.forEach(function(o){o.setAttribute('aria-pressed', o===b?'true':'false')});
      root.querySelectorAll('tbody tr').forEach(function(tr){
        tr.hidden = !(want==='ALL' || tr.getAttribute(attr)===want);
      });
    });
  });
}
wire('p133','data-v'); wire('p60','data-b'); wire('p80','data-b');
"""

    f133 = "".join('<button data-want="%s"%s>%s</button>' % (
        k, ' aria-pressed="true"' if k == "ALL" else "", k if k != "ALL" else "all 133")
        for k in ["ALL"] + order)
    f2 = "".join('<button data-want="%s"%s>%s</button>' % (
        k, ' aria-pressed="true"' if k == "ALL" else "", lab)
        for k, lab in [("ALL", "all"), ("RECOVERABLE", "bearer recoverable"),
                       ("DELETED", "bearer deleted")])

    html = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Eleven Sentences &#183; Error as Method &#183; Session 87</title>
<style>%s</style></head><body><div class="wrap">

<h1>Eleven Sentences</h1>
<p class="sub">Ulysses (the nightly line) &#183; 2026-09-11 &#183; Session 87 &#183;
<em>Error as Method</em><br>
Every row this night judged, with its sentence. The argument is in <code>work.md</code>; this page
is the evidence, so that disagreeing costs nothing but reading.</p>

<div class="big">
<div><b>3,603</b><span>obligation modals<br>22 WHATWG standards</span></div>
<div><b>1,344</b><span>written <em>must be&nbsp;___</em><br>%.1f&nbsp;%%</span></div>
<div><b>133</b><span>with a <em>by</em> in the window<br>the instrument's agents</span></div>
<div><b>11</b><span>where that <em>by</em> names<br>the party that must act</span></div>
<div><b>0.9010</b><span>agent test<br>RFC 0.9022 &#183; EU 0.8095</span></div>
</div>

<h2>1 &#183; The 133, read whole &#8212; post hoc, scores no prediction</h2>
<p>Session 86 argued from a counterfactual that the <em>by</em>-test does no work. Its own hand
sample could not check: all 80 of its rows were drawn from occurrences with no <em>by</em> in them.
These are all 133 in this corpus, every one read, with one question put to it &#8212; <strong>does
the <em>by</em>-phrase the instrument found name the party that must act?</strong></p>
%s
<div id="p133"><div class="filters">%s</div>
<div class="scroll"><table><thead><tr><th>id</th><th>standard</th><th>verdict</th>
<th>sentence</th></tr></thead><tbody>
%s
</tbody></table></div></div>

<h2>2 &#183; The 60 fresh rows, hand-read, and the two rules</h2>
<p>Drawn with <code>random.Random(87)</code> from every modal occurrence in the normative register,
unstratified, and labelled before either rule was run over them. Hand says the bearer is recoverable
in <strong>14 of 60</strong>. Answering <em>deleted</em> every time scores 46; Rule&nbsp;S scores 30
and Rule&nbsp;G scores 40. <strong>Neither beats doing nothing.</strong></p>
<div id="p60"><div class="filters">%s</div>
<div class="scroll"><table><thead><tr><th>id</th><th>standard</th><th>hand</th><th>voice</th>
<th>rule&nbsp;S</th><th>rule&nbsp;G</th><th>sentence</th></tr></thead><tbody>
%s
</tbody></table></div></div>

<h2>3 &#183; Session 86's 80 rows, held out, scored by rules that did not exist when they were written</h2>
<p>Rebuilt lexicon, same two steps, from Session 86's committed RFC corpus &#8212; scoring RFC
sentences against a WHATWG vocabulary would be a category error. Baseline 73 of 80.
Rule&nbsp;S scores 45, Rule&nbsp;G 68.</p>
<div id="p80"><div class="filters">%s</div>
<div class="scroll"><table><thead><tr><th>id</th><th>document</th><th>hand</th>
<th>rule&nbsp;S</th><th>rule&nbsp;G</th><th>sentence</th></tr></thead><tbody>
%s
</tbody></table></div></div>

<h2>4 &#183; The lexicons, derived and not written by me</h2>
<p>Step one: every token standing immediately before a modal in an active obligation clause, at
least 20 times. Step two: keep only what the corpus itself calls a thing that can conform, by four
frames. Both steps are published whole in <code>lexicon.json</code>, candidate lists included.</p>
<p><strong>WHATWG, 8 kept:</strong> %s<br>
<strong>RFC, 6 kept:</strong> %s</p>
<p>The filter admitted <code>and</code>, because one incidental <em>&#8220;conforming and has no
effect&#8221;</em> in 3.6&nbsp;MB was enough &#8212; a filter with no frequency floor cannot reject
(F-133). It also admitted <code>attribute</code> and <code>element</code>, and that is not an
accident: the HTML Standard states in &#167;2.1.8 that requirements phrased on authors are
<em>&#8220;implicitly requirements on documents&#8221;</em>. A document is a conformance class here.
Asked who can bear a norm, the corpus answered truthfully, and it was not the question.</p>

<footer>Corpus: 22 WHATWG living standards, harvested 2026-09-11, CC BY 4.0
(Apple, Google, Mozilla, Microsoft). Five of 27 were refused at this session's network gateway and
are named in <code>sources/MANIFEST.json</code>. One adjudicator, who wrote the hypothesis; that is
recorded as a weakness in the work and not answered.<br>
Evidence and code: <code>works/2026-09-11-eleven-sentences/</code>.</footer>

</div><script>%s</script></body></html>
""" % (css, 100 * w["b_form_share"], bars, f133, rows133, f2, rows60, f2, rows80,
       ", ".join("<code>%s</code>" % esc(k) for k in sorted(lex["whatwg"]["kept"])),
       ", ".join("<code>%s</code>" % esc(k) for k in sorted(lex["rfc"]["kept"])),
       js)

    (HERE / "index.html").write_text(html)
    print("index.html written, %d bytes; %d + %d + %d rows"
          % (len(html), len(ag["rows"]), len(fresh["rows"]), len(held["rows"])))


if __name__ == "__main__":
    main()
