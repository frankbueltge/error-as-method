// Session 67 probe runner — Node / V8. Same two modes, same conventions as
// probe_python.py: every answer a string, nothing normalised across runtimes.
'use strict';
const fs = require('fs');
const SEEDS = JSON.parse(fs.readFileSync(__dirname + '/seeds.json', 'utf8'));

function bits(x) {
  const d = new DataView(new ArrayBuffer(8));
  d.setFloat64(0, x);
  return [...new Uint8Array(d.buffer)].map(v => v.toString(16).padStart(2, '0')).join('');
}
function unbits(h) {
  const d = new DataView(new ArrayBuffer(8));
  for (let i = 0; i < 8; i++) d.setUint8(i, parseInt(h.substr(i * 2, 2), 16));
  return d.getFloat64(0);
}
function cps(s) {
  return [...s].map(c => 'U+' + c.codePointAt(0).toString(16).toUpperCase().padStart(4, '0')).join(' ');
}
function numify(s) {
  const v = Number(s);
  return Number.isNaN(v) && s.trim() !== 'NaN' ? 'error' : bits(v);
}

// The scalar set for L2/L3 — this runtime's analogue of the classic set.
const SCALARS = [['0', 0], ["''", ''], ["'0'", '0'], ['false', false],
                 ['none', null], ["'abc'", 'abc'], ['[]', []]];

function emit() {
  const a = {};
  // ---- Family S: answers that descend from the Unicode Character Database ----
  a.S1 = cps('ß'.toUpperCase());
  a.S2 = cps('ﬁ'.toUpperCase());
  a.S3 = cps('İ'.toLowerCase());
  a.S4 = cps('ı'.toUpperCase());
  a.S5 = cps('ΟΔΟΣ'.toLowerCase());
  a.S6 = cps('ᏸ'.toUpperCase());
  a.S7 = cps('ჯ'.toUpperCase());
  a.S8 = cps('\u{10428}'.toUpperCase());
  a.S9 = cps('ǳ'.toUpperCase());
  a.S10 = cps('ẞ'.toLowerCase());

  // ---- Family I: answers written by hand, per runtime ----
  a.I1 = String(-7 % 3);
  a.I2 = String(7 % -3);
  a.I3 = String(Math.trunc(-7 / 3));   // no integer-division operator; this is the idiom
  a.I4 = String(0.1 + 0.2);
  a.I5 = String(1 / 3);
  a.I6 = String(1e21);
  a.I7 = String(-0.0);
  a.I8 = [0.5, 1.5, 2.5, -0.5].map(v => String(Math.round(v))).join(' ');
  a.I9 = ('10' < '9') ? 'true' : 'false';
  a.I10 = ('' == 0) ? 'true' : 'false';
  a.I11 = String('\u{1d11e}'.length);
  a.I12 = (0.1 + 0.2 === 0.3) ? 'true' : 'false';
  a.I13 = [10, 9, 1].sort().join(' ');
  a.I14 = String(2 ** 3 ** 2);
  a.I15 = ['0x10', '010', '1e2', ' 12 '].map(numify).join(' ');

  const renderings = {};
  for (const s of SEEDS) renderings[s.name] = String(unbits(s.bits));

  return {
    runtime: 'node', version: process.versions.node,
    unicode_version: process.versions.unicode,
    answers: a,
    checks: { L1_roundtrip: l1(), L2_loose_equality: l2(),
              L3_relational_coherence: l3(), L4_division_identity: l4() },
    renderings: renderings
  };
}

// L1 -- does this runtime parse back its own default rendering of a double?
function l1() {
  const detail = [];
  for (const s of SEEDS) {
    const x = unbits(s.bits), rendered = String(x), back = Number(rendered);
    const b = Number.isNaN(back) ? null : bits(back);
    if (b !== s.bits) detail.push({ seed: s.name, rendered: rendered, back: b });
  }
  return { tested: SEEDS.length, violations: detail.length, detail: detail };
}

// L2 -- is this runtime's own equality operator transitive over that set?
function l2() {
  const viol = [];
  for (const [na, x] of SCALARS) for (const [nb, y] of SCALARS) for (const [nc, z] of SCALARS)
    if ((x == y) && (y == z) && !(x == z)) viol.push([na, nb, nc]);
  return { operator: '==', set_size: SCALARS.length,
           transitivity_violations: viol.length, examples: viol.slice(0, 5) };
}

// L3 -- if a<=b and a>=b, does this runtime also say a==b?
function l3() {
  const viol = [];
  for (const [na, x] of SCALARS) for (const [nb, y] of SCALARS)
    if ((x <= y) && (x >= y) && !(x == y)) viol.push([na, nb]);
  return { pairs: SCALARS.length ** 2, incomparable: 0,
           violations: viol.length, examples: viol.slice(0, 5) };
}

// L4 -- does q*b + r == a hold, with this runtime's own division and % ?
function l4() {
  const viol = [];
  for (const a of [-13, -8, -7, -1, 0, 1, 7, 8, 13]) for (const b of [3, -3, 5, -5]) {
    const q = Math.trunc(a / b), r = a % b;
    if (q * b + r !== a) viol.push([a, b, q, r]);
  }
  return { pairs: 36, violations: viol.length, examples: viol.slice(0, 5) };
}

function parse() {
  const strings = JSON.parse(fs.readFileSync(0, 'utf8'));
  return strings.map(s => {
    const v = Number(s);
    return Number.isNaN(v) ? null : bits(v);
  });
}

const mode = process.argv[2] || 'emit';
process.stdout.write(JSON.stringify(mode === 'emit' ? emit() : parse()) + '\n');
