#!/usr/bin/env python3
"""page.py -- index.html, self-contained: inline styles and one inline script, no outside fetches,
no assets beside it but figure.svg.

The page hands the reader the one choice this night could not avoid making for them.  S91.RULEBOUND
is decided by the R3b fire rate under "that corpus's own declared party vocabulary", and the
vocabulary is declared by whoever runs the check.  Tonight declared three per corpus and fixed the
decision on one, in advance.  Here the reader can move the declaration and watch the verdict move.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R3B = "R3b_active_governor_own_block"
RULES = [("R1_adjacent_subject", "R1 adjacent subject"),
         ("R2_no_competing_nominal", "R2 no competing nominal"),
         ("R3_active_governor", "R3 active governor"),
         (R3B, "R3b active governor, own block")]


def main():
    res = json.load(open(HERE / "results.json"))
    ins = json.load(open(HERE / "inspection.json"))
    adj = json.load(open(HERE / "adjudication.json"))

    data = {"band": [21.42, 41.42], "uk_value": 31.42, "corpora": [], "rules": RULES,
            "verdict": adj["S91.RULEBOUND"]["verdict"],
            "decided_on": "narrow",
            "subjecthood": {r["corpus"].replace(" (calibration)", ""): r["subjecthood_rate_pct"]
                            for r in ins["rows"]}}

    def pack(name, entry, lists, tested):
        return {"name": name, "tested": tested, "population": entry.get("population"),
                "binding_register": entry.get("binding_register"),
                "own_terms": entry.get("own_terms", []),
                "wide_adds": entry.get("wide_adds", []),
                "lists": {l: {"reach_pct": lists[l]["reach_pct"],
                              "in_reach": lists[l]["rows_in_reach_at_word_36"],
                              "terms": lists[l]["terms_in_list"],
                              "same_block_pct": lists[l]["carrier_in_own_block_pct"],
                              "median_block": lists[l]["median_carrier_block_words"],
                              "fires": {k: lists[l]["by_rule"][k]["fire_pct"] for k, _ in RULES},
                              "carriers": lists[l]["carriers_in_reach"]}
                          for l in ("base", "narrow", "wide")}}

    for name, entry in res["corpora"].items():
        data["corpora"].append(pack(name, entry, entry["lists"], True))
    cal = res["calibration_UK_statute"]
    data["corpora"].append(pack("UK Acts", {"population": None,
                                            "binding_register": cal["binding_register"],
                                            "own_terms": [], "wide_adds": ["person", "persons"]},
                                cal["lists"], False))

    html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Three Other Offices &mdash; the vocabulary that decides a falsifier</title>
<style>
  :root { --ink:#1b1b1b; --muted:#6f6f6f; --paper:#faf8f4; --band:#d8d2c4; --hit:#a33; --rule:#ddd8cc; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--paper); color:var(--ink);
         font:16px/1.55 Georgia,'Times New Roman',serif; }
  main { max-width:960px; margin:0 auto; padding:34px 20px 80px; }
  h1 { font-size:1.6rem; line-height:1.25; margin:0 0 .4rem; font-weight:normal; }
  h2 { font-size:1.05rem; margin:2.4rem 0 .6rem; font-weight:normal;
       border-bottom:1px solid var(--rule); padding-bottom:.3rem; }
  p.lede { color:var(--muted); margin:0 0 1.6rem; }
  fieldset { border:1px solid var(--rule); padding:.8rem 1rem 1rem; margin:0 0 1.4rem; }
  legend { font-size:.82rem; color:var(--muted); letter-spacing:.04em; text-transform:uppercase; }
  .opts { display:flex; flex-wrap:wrap; gap:.4rem 1.4rem; }
  label.opt { cursor:pointer; display:flex; gap:.45rem; align-items:baseline; }
  .note { font-size:.86rem; color:var(--muted); margin:.6rem 0 0; }
  .verdict { border-left:3px solid var(--hit); padding:.7rem .9rem; background:#fff;
             margin:1.2rem 0; }
  .verdict b { color:var(--hit); }
  table { border-collapse:collapse; width:100%; font-size:.92rem; }
  th,td { text-align:left; padding:.36rem .5rem; border-bottom:1px solid var(--rule);
          vertical-align:top; }
  th { font-weight:normal; color:var(--muted); font-size:.82rem; }
  td.n { text-align:right; font-variant-numeric:tabular-nums; }
  td.in { color:var(--hit); font-weight:bold; }
  svg, img { width:100%; max-width:100%; height:auto; display:block; }
  .chips { display:flex; flex-wrap:wrap; gap:.3rem; margin:.5rem 0 0; }
  .chip { border:1px solid var(--rule); background:#fff; padding:.12rem .45rem;
          font-size:.84rem; white-space:nowrap; }
  .chip span { color:var(--muted); }
  figure { margin:1.6rem 0; }
  figcaption { font-size:.86rem; color:var(--muted); margin-top:.5rem; }
  footer { margin-top:3rem; font-size:.84rem; color:var(--muted); }
  a { color:inherit; }
  @media (max-width:560px){ body{font-size:15px;} main{padding:22px 16px 60px;} }
</style>
</head>
<body>
<main>
<h1>Three Other Offices</h1>
<p class="lede">A decision rule written to find who bears an obligation in UK statute, taken
unchanged to European law, the RFC series and the WHATWG standards. Its falsifier asks for the
rule&rsquo;s fire rate &ldquo;under that corpus&rsquo;s own declared party vocabulary&rdquo;.
Somebody has to declare it. Move the declaration below and watch the verdict move.</p>

<fieldset>
  <legend>the declared vocabulary</legend>
  <div class="opts" id="lists"></div>
  <p class="note" id="listnote"></p>
</fieldset>

<div id="chart"></div>
<div class="verdict" id="verdict"></div>

<h2>What the list put in reach</h2>
<table id="tbl"><thead><tr>
  <th>corpus</th><th class="n">rows in reach</th><th class="n">reach&nbsp;%</th>
  <th class="n">R1</th><th class="n">R2</th><th class="n">R3</th><th class="n">R3b&nbsp;%</th>
  <th class="n">carrier in own block&nbsp;%</th></tr></thead><tbody></tbody></table>
<p class="note">R1, R2, R3 and R3b are Session 91&rsquo;s three declared rules and its one repair,
imported unchanged. R3b is the one the falsifier is written on.</p>

<h2>The words the rule was actually looking at</h2>
<p class="note">The twelve commonest carriers in reach, per corpus, under the selected list. This is
where a declared vocabulary stops being a technicality.</p>
<div id="carriers"></div>

<figure>
  <img src="figure.svg" alt="Four traditions plotted by how often they put their party terms in
  subject position against what the rule returns, with the falsifying band drawn as a stripe; and
  the same decision taken twelve times, once per corpus and vocabulary.">
  <figcaption>The static figure. Only subjecthood orders the four traditions as the rule does;
  block length and term density do not.</figcaption>
</figure>

<footer>
<p>Session 94 &middot; 2026-09-21 &middot; Error as Method. Every number on this page comes from
<code>results.json</code>, <code>inspection.json</code> and <code>adjudication.json</code> in this
work&rsquo;s directory, which are recomputable from committed corpora by <code>port.py</code>,
<code>inspect.py</code> and <code>score.py</code>. The rules come from
<code>works/2026-09-17-the-second-instrument/validate.py</code> and are not reimplemented here.</p>
<p>UK Acts are drawn for comparison and are not one of the three corpora put to the test: the band
was drawn around their value, so they fall inside it by construction.</p>
</footer>
</main>
<script type="application/json" id="data">__DATA__</script>
<script>
(function () {
  var D = JSON.parse(document.getElementById('data').textContent);
  var LISTS = ['base','narrow','wide'];
  var NOTE = {
    base: 'The 26 terms Session 88 derived from the WHATWG standards, used unchanged by Sessions 90 and 91. It is one tradition’s vocabulary applied to all four.',
    narrow: 'The 26 plus each tradition’s own named offices, bodies and roles, authored before the run and published in PREDICTIONS.md §4. This is the list the check was fixed on, in advance.',
    wide: 'The narrow list plus that tradition’s single most general noun for a party — person, or party — mirroring Session 90’s own wide clause.'
  };
  var sel = 'narrow';

  var opts = document.getElementById('lists');
  LISTS.forEach(function (l) {
    var lab = document.createElement('label');
    lab.className = 'opt';
    var r = document.createElement('input');
    r.type = 'radio'; r.name = 'list'; r.value = l; r.checked = (l === sel);
    r.addEventListener('change', function () { sel = l; render(); });
    lab.appendChild(r);
    var s = document.createElement('span');
    s.textContent = l;
    lab.appendChild(s);
    opts.appendChild(lab);
  });

  function el(tag, attrs, text) {
    var e = document.createElementNS('http://www.w3.org/2000/svg', tag);
    for (var k in attrs) { e.setAttribute(k, attrs[k]); }
    if (text !== undefined) { e.textContent = text; }
    return e;
  }

  function render() {
    document.getElementById('listnote').textContent = NOTE[sel];

    // ---- chart
    var W = 900, H = 330, L = 150, T = 24, PW = W - L - 90, PH = H - T - 54;
    var max = 72;
    var svg = el('svg', {viewBox: '0 0 ' + W + ' ' + H, role: 'img'});
    svg.appendChild(el('title', {}, 'R3b fire rate by corpus under the ' + sel + ' vocabulary'));
    var y = function (v) { return T + PH - PH * v / max; };
    var band = D.band;
    svg.appendChild(el('rect', {x: L, y: y(band[1]), width: PW, height: y(band[0]) - y(band[1]),
                                fill: 'var(--band)', 'fill-opacity': '0.55'}));
    svg.appendChild(el('line', {x1: L, y1: y(D.uk_value), x2: L + PW, y2: y(D.uk_value),
                                stroke: 'var(--hit)', 'stroke-dasharray': '5 4'}));
    svg.appendChild(el('text', {x: L + PW + 6, y: y(D.uk_value) + 4, 'font-size': '11',
                                fill: 'var(--hit)'}, '31.42'));
    svg.appendChild(el('line', {x1: L, y1: T + PH, x2: L + PW, y2: T + PH, stroke: 'var(--ink)'}));
    [0, 20, 40, 60].forEach(function (v) {
      svg.appendChild(el('text', {x: L - 8, y: y(v) + 4, 'font-size': '11', 'text-anchor': 'end',
                                  fill: 'var(--muted)'}, String(v)));
    });
    var n = D.corpora.length, bw = PW / n * 0.46;
    D.corpora.forEach(function (c, i) {
      var v = c.lists[sel].fires['R3b_active_governor_own_block'];
      var cx = L + PW * (i + 0.5) / n;
      var hit = v >= band[0] && v <= band[1];
      svg.appendChild(el('rect', {x: cx - bw / 2, y: y(v), width: bw, height: (T + PH) - y(v),
                                  fill: hit ? 'var(--hit)' : 'var(--ink)',
                                  'fill-opacity': c.tested ? '1' : '0.25'}));
      svg.appendChild(el('text', {x: cx, y: y(v) - 7, 'font-size': '13', 'text-anchor': 'middle',
                                  fill: hit ? 'var(--hit)' : 'var(--ink)'}, v.toFixed(2)));
      svg.appendChild(el('text', {x: cx, y: T + PH + 20, 'font-size': '12',
                                  'text-anchor': 'middle'}, c.name));
      svg.appendChild(el('text', {x: cx, y: T + PH + 38, 'font-size': '10.5',
                                  'text-anchor': 'middle', fill: 'var(--muted)'},
                          c.tested ? (c.lists[sel].in_reach + ' rows in reach')
                                   : 'calibration, in the band by construction'));
    });
    var host = document.getElementById('chart');
    host.textContent = '';
    host.appendChild(svg);

    // ---- verdict
    var inside = D.corpora.filter(function (c) {
      var v = c.lists[sel].fires['R3b_active_governor_own_block'];
      return c.tested && v >= band[0] && v <= band[1];
    }).map(function (c) { return c.name; });
    var v = document.getElementById('verdict');
    v.textContent = '';
    var b = document.createElement('b');
    b.textContent = inside.length ? 'S91.RULEBOUND would be FALSIFIED'
                                  : 'S91.RULEBOUND would survive';
    v.appendChild(b);
    var p = document.createElement('span');
    p.textContent = inside.length
      ? ' on the ' + sel + ' vocabulary, by ' + inside.join(' and ') + '.'
      : ' on the ' + sel + ' vocabulary: no corpus lands in the band.';
    v.appendChild(p);
    var q = document.createElement('p');
    q.className = 'note';
    q.textContent = sel === D.decided_on
      ? 'This is the list the check was fixed on before the run, so this is the verdict of record: '
        + D.verdict + '.'
      : 'This is not the list the check was fixed on. The verdict of record is the one under '
        + D.decided_on + ': ' + D.verdict + '. Shown here because the row’s own wording leaves '
        + 'the vocabulary to whoever runs it.';
    v.appendChild(q);

    // ---- table
    var tb = document.querySelector('#tbl tbody');
    tb.textContent = '';
    D.corpora.forEach(function (c) {
      var L2 = c.lists[sel], tr = document.createElement('tr');
      function td(t, cls) {
        var d = document.createElement('td');
        if (cls) { d.className = cls; }
        d.textContent = t;
        tr.appendChild(d);
      }
      td(c.name + (c.tested ? '' : ' (calibration)'));
      td(String(L2.in_reach), 'n');
      td(L2.reach_pct.toFixed(2), 'n');
      td(L2.fires['R1_adjacent_subject'].toFixed(2), 'n');
      td(L2.fires['R2_no_competing_nominal'].toFixed(2), 'n');
      td(L2.fires['R3_active_governor'].toFixed(2), 'n');
      var r3b = L2.fires['R3b_active_governor_own_block'];
      td(r3b.toFixed(2), (c.tested && r3b >= band[0] && r3b <= band[1]) ? 'n in' : 'n');
      td(L2.same_block_pct.toFixed(2), 'n');
      tb.appendChild(tr);
    });

    // ---- carriers
    var host2 = document.getElementById('carriers');
    host2.textContent = '';
    D.corpora.forEach(function (c) {
      var h = document.createElement('p');
      h.style.margin = '1rem 0 .1rem';
      h.textContent = c.name;
      host2.appendChild(h);
      var box = document.createElement('div');
      box.className = 'chips';
      var carriers = c.lists[sel].carriers;
      var keys = Object.keys(carriers);
      if (!keys.length) {
        var none = document.createElement('span');
        none.className = 'note';
        none.textContent = 'nothing in reach under this list';
        box.appendChild(none);
      }
      keys.forEach(function (k) {
        var s = document.createElement('span');
        s.className = 'chip';
        s.textContent = k + ' ';
        var c2 = document.createElement('span');
        c2.textContent = carriers[k];
        s.appendChild(c2);
        box.appendChild(s);
      });
      host2.appendChild(box);
    });
  }

  render();
})();
</script>
</body>
</html>
"""
    html = html.replace("__DATA__", json.dumps(data, separators=(",", ":")))
    (HERE / "index.html").write_text(html)
    print("wrote index.html (%d bytes)" % (HERE / "index.html").stat().st_size)


if __name__ == "__main__":
    main()
