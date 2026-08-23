// Node probe. Reads a job on stdin, answers on stdout, in its own words.
//
// Rendering:
//   default -- Date.prototype.toString(). ECMA-262 defines it; it is what a Date becomes in
//              any string context.
//   iso     -- Date.prototype.toISOString(), which ECMA-262 fixes as the Date Time String Format
//              and which always renders in UTC with a trailing Z.
// Parsing:
//   new Date(s). ECMA-262 21.4.3.2 gives implementation latitude for non-conforming strings;
//   for conforming date-time forms WITHOUT an offset it specifies LOCAL time, and for
//   date-only forms it specifies UTC. That asymmetry is the language's, not this harness's.
// Numbers:
//   Number(s), the language's own string-to-number coercion. NaN is recorded as NaN, not as an
//   error, because that is what the language returns.

let buf = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (d) => { buf += d; });
process.stdin.on('end', () => {
  const job = JSON.parse(buf);
  const out = { runtime: 'node', version: process.versions.node };

  if (job.instants) {
    out.render = job.instants.map((e) => {
      const r = { default: null, default_error: null, iso: null, iso_error: null };
      const d = new Date(e * 1000);
      if (Number.isNaN(d.getTime())) {
        r.default_error = 'Invalid Date';
        r.iso_error = 'Invalid Date';
        return r;
      }
      r.default = d.toString();
      try { r.iso = d.toISOString(); } catch (err) { r.iso_error = String(err); }
      return r;
    });
  }

  if (job.strings) {
    out.parse = job.strings.map((s) => {
      const d = new Date(s);
      const t = d.getTime();
      if (Number.isNaN(t)) return { status: 'refused', error: 'Invalid Date' };
      return { status: 'ok', epoch: t / 1000 };
    });
  }

  if (job.numbers) {
    out.numparse = job.numbers.map((s) => {
      const v = Number(s);
      // JSON cannot carry NaN or Infinity; report them by name so nothing is silently coerced.
      const enc = (x) => (Number.isFinite(x) ? x : String(x));
      return { strict: enc(v), lenient: enc(parseFloat(s)) };
    });
  }

  process.stdout.write(JSON.stringify(out));
});
