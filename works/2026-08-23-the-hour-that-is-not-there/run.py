#!/usr/bin/env python3
"""Run the matrix.

Pass 1 -- every runtime renders every instant under every zone, twice: with its own default
          string conversion and with its own explicit ISO-8601 form.
Pass 2 -- every PARSER, under every zone, reads every string any producer emitted under any
          zone, and reports the epoch seconds it recovered, in its own words.

A cell is therefore (form, producer, producer-zone, parser, parser-zone, instant). Cells where
the two zones agree are the matrix as first designed; cells where they differ are the repair.

THE REPAIR, recorded here because it was found mid-night and not by the matrix. The design as
first run used two zones and ran each producer and each parser under the SAME one. That made
every parser's local zone equal to every honest producer's local zone, so a divergence that
only appears when the two differ could not occur -- and one does: Ruby's Time.parse discards
the offset in Node's default `GMT+0200` rendering and falls back to its own local zone, which
under a shared zone lands on the right instant by coincidence. A hand-made single-observer
probe found it; the matrix could not. Correction C1 in adjudication.json.

Perl produces and does not parse; see probe_perl.pl for why.
"""
import json
import os
import subprocess
import sys

RUNTIMES = {
    "python": ["python3", "probe_python.py"],
    "node":   ["node", "probe_node.js"],
    "ruby":   ["ruby", "probe_ruby.rb"],
    "php":    ["php", "probe_php.php"],
    "perl":   ["perl", "probe_perl.pl"],
}
PRODUCERS = ["python", "node", "ruby", "php", "perl"]
PARSERS = ["python", "node", "ruby", "php"]          # perl: producer only

ZONES = ["UTC", "Europe/Berlin", "America/Los_Angeles"]

# Family N: hand-written numeric text. No producer -- these are strings nobody's default
# conversion emits. The family exists to ask what a comparison with only readers can do.
NUMBERS = [
    "1234.5",        # the plain case, as a control
    "1,234.5",       # en-GB / en-US thousands separator
    "1.234,5",       # de-DE thousands separator: the same quantity, the same glyphs, swapped
    "1 234,5",       # space as separator
    "1 234,5",  # NARROW NO-BREAK SPACE, which is what CLDR actually specifies for fr-FR
    "1_000",         # numeric literal separator (a literal form in several languages)
    "0x1A",          # hexadecimal
    "0o17",          # octal, modern prefix
    "017",           # octal, historical prefix
    "1e3",           # exponent
    "1E3",
    "  42  ",        # surrounding whitespace
    "42abc",         # a number with junk after it
    "abc42",         # junk first
    "",              # the empty string
    "+.5",           # leading plus, no integer part
    "-.5",
    ".",             # a lone decimal point
    "1,,2",          # a malformed separator run
    "Infinity",
    "inf",
    "NaN",
    "nan",
    "1e400",              # overflows a double
    "9007199254740993",   # 2**53+1: not representable as a binary64
    "١٢٣",  # ARABIC-INDIC DIGITS ONE TWO THREE
    "１２３",  # FULLWIDTH DIGITS ONE TWO THREE
]


def call(runtime, job, tz):
    env = dict(os.environ)
    env["TZ"] = tz
    env["LC_ALL"] = "C"
    env["LANG"] = "C"
    proc = subprocess.run(RUNTIMES[runtime], input=json.dumps(job), env=env,
                          capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"{runtime} exited {proc.returncode} under TZ={tz}\n{proc.stderr[:2000]}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        sys.exit(f"{runtime} emitted unparseable output under TZ={tz}:\n{proc.stdout[:2000]}")


def main():
    corpus = json.load(open("corpus.json"))
    instants = [c["epoch"] for c in corpus["chosen"]] + corpus["drawn"]
    labels = [c["label"] for c in corpus["chosen"]] + \
             [f"drawn-{i:03d}" for i in range(len(corpus["drawn"]))]

    # ---- pass 1: render, under every zone
    render, versions = {}, {}
    php_zone = {}
    for tz in ZONES:
        render[tz] = {}
        for rt in PRODUCERS:
            r = call(rt, {"instants": instants}, tz)
            render[tz][rt] = r["render"]
            versions[rt] = r.get("version")
        php_zone[tz] = call("php", {}, tz).get("default_timezone")
        print(f"  rendered under TZ={tz}", flush=True)

    # ---- the union of every string any producer emitted under any zone. A parser sees only
    #      the string: it is never told who produced it or where.
    strings, index = [], {}
    for tz in ZONES:
        for rt in PRODUCERS:
            for row in render[tz][rt]:
                for form in ("default", "iso"):
                    s = row[form]
                    if s is not None and s not in index:
                        index[s] = len(strings)
                        strings.append(s)

    # ---- pass 2: parse the whole union, under every zone
    parse, numparse = {}, {}
    for tz in ZONES:
        parse[tz] = {}
        for rt in PARSERS:
            r = call(rt, {"strings": strings, "numbers": NUMBERS}, tz)
            parse[tz][rt] = r["parse"]
            numparse.setdefault(tz, {})[rt] = r.get("numparse")
        numparse[tz]["perl"] = call("perl", {"numbers": NUMBERS}, tz).get("numparse")
        print(f"  parsed {len(strings)} strings under TZ={tz}", flush=True)

    # Store the parse block compactly: one entry per string, in the order of `strings`.
    # A number is the epoch seconds the parser recovered; a string is its refusal message.
    # 50,856 records written as {"status":"ok","epoch":...} cost several megabytes and say
    # nothing the two forms below do not. Nothing is dropped -- compare.py reads it back.
    packed = {tz: {rt: [(r["epoch"] if r["status"] == "ok" else r["error"])
                        for r in parse[tz][rt]]
                   for rt in PARSERS} for tz in ZONES}

    out = {
        "labels": labels, "n_chosen": len(corpus["chosen"]), "n_drawn": len(corpus["drawn"]),
        "zones": ZONES, "instants": instants, "versions": versions,
        "php_default_timezone_per_TZ": php_zone,
        "strings": strings, "string_index": index,
        "render": render,
        "parse_encoding": "parse[zone][parser][i] corresponds to strings[i]: a NUMBER is the "
                          "epoch seconds that parser recovered, a STRING is its refusal message.",
        "parse": packed,
        "numbers": NUMBERS, "numparse": numparse,
    }
    with open("matrix.json", "w") as fh:
        json.dump(out, fh, separators=(",", ":"))

    print(f"matrix.json: {len(instants)} instants x {len(PRODUCERS)} producers x "
          f"{len(ZONES)} producer-zones x {len(PARSERS)} parsers x {len(ZONES)} parser-zones "
          f"x 2 forms; {len(strings)} distinct strings")


if __name__ == "__main__":
    main()
