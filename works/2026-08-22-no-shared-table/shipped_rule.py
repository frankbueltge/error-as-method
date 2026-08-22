#!/usr/bin/env python3
"""The one Family S disagreement, traced to the rule that ships and is not applied.

The five runtimes agree on nine of ten case-mapping probes and split on one:
lowercasing Greek ODOS. Python, Node and PHP end the word with U+03C2 FINAL
SIGMA; Ruby and Perl end it with U+03C3.

The obvious explanation is a Unicode version gap -- Session 66 found exactly
that shape when it swapped one implementation for another. This script tests it
and finds something else. Perl's installation carries the Unicode Character
Database file that states the rule, byte for byte as Unicode publishes it, and
Perl's lc does not apply it. Ruby's own documentation says why it does not.

Nothing is fetched at measuring time; the remote comparison is a separate,
optional step (--fetch) and its result is recorded in sources/MANIFEST.json.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UCD_URL = "https://www.unicode.org/Public/15.0.0/ucd/SpecialCasing.txt"


def perl_privlib():
    out = subprocess.run(["perl", "-MConfig", "-e", "print $Config{privlib}"],
                         capture_output=True, text=True, check=True)
    return out.stdout.strip()


def main():
    lib = perl_privlib()
    sc = os.path.join(lib, "unicore", "SpecialCasing.txt")
    ver = os.path.join(lib, "unicore", "version")

    res = {"perl_privlib": lib, "shipped_file": sc}

    res["perl_unicore_version"] = open(ver).read().strip() if os.path.exists(ver) else None

    if os.path.exists(sc):
        blob = open(sc, "rb").read()
        res["shipped_bytes"] = len(blob)
        res["shipped_sha256"] = hashlib.sha256(blob).hexdigest()
        # The rule itself, verbatim, with its line number in the shipped file.
        lines = blob.decode("utf-8").splitlines()
        res["final_sigma_lines"] = [
            {"line": i + 1, "text": t}
            for i, t in enumerate(lines) if "Final_Sigma" in t
        ]
    else:
        res["shipped_bytes"] = None

    # What each runtime actually does at the end of a word, and in the middle.
    words = {"ODOS_uppercase": "ΟΔΟΣ",     # ΟΔΟΣ
             "SIGMA_SIGMA": "ΣΣ",                     # ΣΣ
             "SIGMA_alone": "Σ"}                           # Σ  (no preceding cased letter)
    progs = {
        "python": ["python3", "-c",
                   "import sys,json;print(json.dumps({k:' '.join('U+%04X'%ord(c) for c in v.lower())"
                   " for k,v in json.load(sys.stdin).items()}))"],
        "node": ["node", "-e",
                 "let s='';process.stdin.on('data',d=>s+=d).on('end',()=>{const o={};"
                 "for(const[k,v]of Object.entries(JSON.parse(s)))o[k]=[...v.toLowerCase()]"
                 ".map(c=>'U+'+c.codePointAt(0).toString(16).toUpperCase().padStart(4,'0')).join(' ');"
                 "console.log(JSON.stringify(o))})"],
        "ruby": ["ruby", "-rjson", "-e",
                 "h=JSON.parse($stdin.read);puts JSON.generate(h.transform_values{|v|"
                 "v.downcase.codepoints.map{|c|format('U+%04X',c)}.join(' ')})"],
        "php": ["php", "-r",
                "$h=json_decode(stream_get_contents(STDIN),true);$o=[];"
                "foreach($h as $k=>$v){$p=[];foreach(mb_str_split(mb_strtolower($v,'UTF-8'),1,'UTF-8') as $c)"
                "$p[]=sprintf('U+%04X',mb_ord($c,'UTF-8'));$o[$k]=implode(' ',$p);}echo json_encode($o);"],
        "perl": ["perl", "-MJSON::PP", "-e",
                 "my $h=JSON::PP->new->decode(do{local $/;<STDIN>});"
                 "my %o=map{($_=>join' ',map{sprintf'U+%04X',ord}split//,lc($h->{$_}))}keys %$h;"
                 "print JSON::PP->new->canonical->encode(\\%o);"],
    }
    payload = json.dumps(words)
    res["lowercased"] = {}
    for name, cmd in progs.items():
        p = subprocess.run(cmd, input=payload, capture_output=True, text=True)
        res["lowercased"][name] = json.loads(p.stdout) if p.returncode == 0 else \
            {"error": p.stderr[:300]}

    res["applies_final_sigma"] = {
        n: (v.get("ODOS_uppercase", "").endswith("U+03C2") if isinstance(v, dict) else None)
        for n, v in res["lowercased"].items()}

    if "--fetch" in sys.argv:
        import urllib.request
        with urllib.request.urlopen(UCD_URL) as r:
            remote = r.read()
        res["remote"] = {"url": UCD_URL, "status": 200, "bytes": len(remote),
                         "sha256": hashlib.sha256(remote).hexdigest()}
        res["remote"]["identical_to_shipped"] = \
            res["remote"]["sha256"] == res.get("shipped_sha256")

    json.dump(res, open(os.path.join(HERE, "shipped_rule.json"), "w"), indent=1)
    print("perl unicore version   :", res["perl_unicore_version"])
    print("shipped SpecialCasing  :", res["shipped_bytes"], "bytes",
          res.get("shipped_sha256", "")[:16])
    for l in res.get("final_sigma_lines", []):
        print("  line %-4d %s" % (l["line"], l["text"]))
    print("applies Final_Sigma    :", res["applies_final_sigma"])
    if "remote" in res:
        print("remote UCD identical   :", res["remote"]["identical_to_shipped"])


if __name__ == "__main__":
    main()
