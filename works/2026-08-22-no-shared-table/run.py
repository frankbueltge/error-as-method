#!/usr/bin/env python3
"""Session 67 driver — put the same questions to five runtimes and collect the answers.

Two passes, and the second is the one the night turns on.

  pass 1  each runtime answers every probe, runs its four internal-identity
          checks, and renders all 512 seed doubles with its DEFAULT string
          conversion.
  pass 2  each runtime is handed every other runtime's renderings and asked to
          parse them back. That gives a 5x5xN matrix of bit patterns and, with
          it, the only thing that can settle Session 66's falsifier: whether a
          failure exists that needs BOTH parties to be visible.

Writes answers.json (pass 1) and interop.json (pass 2). Nothing is fetched;
everything runs locally and deterministically.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

RUNTIMES = [
    ("python", ["python3", "probe_python.py"]),
    ("node",   ["node", "probe_node.js"]),
    ("ruby",   ["ruby", "probe_ruby.rb"]),
    ("php",    ["php", "probe_php.php"]),
    ("perl",   ["perl", "probe_perl.pl"]),
]


def call(cmd, mode, stdin_text=None):
    p = subprocess.run(cmd + [mode], cwd=HERE, input=stdin_text,
                       capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit("%s %s failed:\n%s" % (" ".join(cmd), mode, p.stderr[:2000]))
    return json.loads(p.stdout)


def main():
    seeds = json.load(open(os.path.join(HERE, "seeds.json")))
    names = [s["name"] for s in seeds]

    # ---- pass 1 ----
    answers = {}
    for name, cmd in RUNTIMES:
        answers[name] = call(cmd, "emit")
        print("emit  %-7s %s" % (name, answers[name]["version"]))
    json.dump(answers, open(os.path.join(HERE, "answers.json"), "w"), indent=1)

    # ---- pass 2 ----
    # One flat list per producer, in seed order, so the parser side needs no
    # knowledge of what it is being handed.
    produced = {p: [answers[p]["renderings"][n] for n in names] for p, _ in RUNTIMES}

    matrix = {}   # matrix[parser][producer] = [bits or null, ...] in seed order
    for parser, cmd in RUNTIMES:
        matrix[parser] = {}
        for producer, _ in RUNTIMES:
            payload = json.dumps(produced[producer])
            matrix[parser][producer] = call(cmd, "parse", payload)
        print("parse %-7s done" % parser)

    json.dump({"seed_order": names, "produced": produced, "matrix": matrix},
              open(os.path.join(HERE, "interop.json"), "w"), indent=1)
    print("seeds %d · cells %d" % (len(names), len(names) * 25))


if __name__ == "__main__":
    main()
