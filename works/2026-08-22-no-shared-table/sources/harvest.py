#!/usr/bin/env python3
"""Record every source this night leaned on, without committing anyone's bytes.

Per the protocol note of 2026-08-18: commit a source's bytes only where the
licence permits redistribution; otherwise commit the manifest and quote within
citation length. Nothing under this directory is a copy of a third-party file.
The manifest is the warrant -- a stranger re-fetches and compares the hash.

Writes MANIFEST.json next to this script.
"""
import hashlib
import json
import os
import subprocess
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))

REMOTE = [
    ("https://www.unicode.org/Public/15.0.0/ucd/SpecialCasing.txt",
     "The conditional case mappings, Unicode 15.0.0. Line 211 states the Final_Sigma "
     "rule this night found shipped and unapplied. Compared by hash against the copy "
     "inside Perl 5.38.2's installation.",
     "Unicode licence permits redistribution; not committed here regardless, because "
     "the manifest hash is the better warrant and the file is one fetch away."),
    ("https://docs.python.org/3/whatsnew/3.1.html",
     "States verbatim that Python uses David Gay's algorithm for the shortest "
     "floating-point representation. The primary source for correction C2.",
     "Documentation page, cited by URL and short quotation only."),
    ("https://docs.ruby-lang.org/en/3.3/case_mapping_rdoc.html",
     "States verbatim that context-dependent case mapping per Table 3-17 is not "
     "supported. Settles why Ruby does not produce a final sigma.",
     "Documentation page, cited by URL and short quotation only."),
    ("https://www.php.net/manual/en/function.mb-strtoupper.php",
     "States that mbstring determines 'alphabetic' by Unicode character properties. "
     "Part of the Family S lineage evidence.",
     "Documentation page, cited by URL and short quotation only."),
    ("https://perldoc.perl.org/perlunicode",
     "States that case translation operators use the Unicode case translation tables.",
     "Documentation page, cited by URL and short quotation only."),
    ("https://tc39.es/ecma262/multipage/text-processing.html",
     "String.prototype.toLowerCase: the result must be derived from the locale-"
     "insensitive case mappings in the Unicode Character Database, naming "
     "UnicodeData.txt and SpecialCasing.txt.",
     "Specification, cited by section and short quotation only."),
    ("https://tc39.es/ecma262/multipage/ecmascript-data-types-and-values.html",
     "Number::toString, section 6.1.6.1.20: 'k is as small as possible', ties to "
     "nearest then even. The norm that makes the shortest round-tripping decimal "
     "unique, and therefore makes section 7 of the work possible.",
     "Specification, cited by section and short quotation only."),
]

LOCAL = [
    ("perl unicore/SpecialCasing.txt",
     "read at run time by shipped_rule.py from this environment's Perl installation; "
     "the file whose line 211 Perl's lc does not apply"),
    ("perl unicore/version",
     "the Unicode version Perl's tables were generated from: 15.0.0"),
]

CITED_NOT_FETCHED = [
    {"citation": "Steele, G. L., Lea, D., Flood, C. H. (2014). Fast splittable pseudorandom "
                 "number generators. OOPSLA '14.",
     "doi": "10.1145/2660193.2660195",
     "why": "SplitMix64, whose constants seeds.py uses to draw the 500 doubles.",
     "read": "not read in full this session; the algorithm and its constants are used, and "
             "the attribution is to the published paper. Title, authors, venue and DOI "
             "verified against the ACM Digital Library entry and the OOPSLA 2014 programme."}
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "error-as-method/session-67"})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            body = r.read()
            return {"http_status": r.status, "bytes": len(body),
                    "sha256": hashlib.sha256(body).hexdigest()}
    except Exception as e:
        return {"http_status": None, "bytes": None, "sha256": None,
                "error": "%s: %s" % (type(e).__name__, e)}


def main():
    privlib = subprocess.run(["perl", "-MConfig", "-e", "print $Config{privlib}"],
                             capture_output=True, text=True).stdout.strip()
    out = {
     "session": 67, "date": "2026-08-22",
     "policy": "No third-party source file is committed. URL, HTTP status, byte count and "
               "SHA-256 are recorded so the reading is reproducible without this repository "
               "republishing anyone's text. (PROTOCOL.md, architect's note 2026-08-18.)",
     "remote": [], "local_read_at_run_time": [], "cited_not_fetched": CITED_NOT_FETCHED}

    for url, what, rights in REMOTE:
        rec = {"url": url, "what": what, "rights": rights, "fetched": "2026-08-22"}
        rec.update(fetch(url))
        out["remote"].append(rec)
        print("%-3s %-9s %s" % (rec.get("http_status"), rec.get("bytes"), url))

    for name, why in LOCAL:
        path = os.path.join(privlib, "unicore", name.split("/")[-1])
        rec = {"name": name, "path": path, "why": why, "committed": False}
        if os.path.exists(path):
            blob = open(path, "rb").read()
            rec.update({"bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
        out["local_read_at_run_time"].append(rec)
        print("local  %-9s %s" % (rec.get("bytes"), path))

    json.dump(out, open(os.path.join(HERE, "MANIFEST.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
