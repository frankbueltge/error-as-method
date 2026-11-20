"""Word rules for names, fixed before any maker ran.

content(name): lowercase, letters only, words split on anything else, stopwords dropped, a trailing 's' dropped from
words longer than three letters ('swans' -> 'swan', 'bus' stays). The people's shelf: the content words of the 50
most frequent whole names people gave KILOGRAM's figures (full.json, after the same lowercasing and stripping).

Usage: python3 words.py FULL_JSON -> shelf.json
"""
import json
import re
import sys
from collections import Counter

STOP = {"a", "an", "the", "of", "with", "on", "in", "and", "or", "its", "it", "to", "at", "is", "his", "her", "their",
        "from", "for", "up", "down", "out", "some", "something", "like", "looking", "shape", "shaped", "figure"}


def content(name):
    words = [w for w in re.split(r"[^a-z]+", name.lower()) if w and w not in STOP]
    return {w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w for w in words}


def main(full_json):
    full = json.load(open(full_json))
    c = Counter()
    for v in full.values():
        for a in v["annotations"]:
            c[" ".join(re.split(r"[^a-z]+", a["whole"]["wholeAnnotation"].lower())).strip()] += 1
    top = c.most_common(50)
    shelf = set()
    for name, _ in top:
        shelf |= content(name)
    json.dump({"rule": __doc__.strip().split("\n\n")[1], "top50": top, "shelf": sorted(shelf),
               "n_names": sum(c.values())}, open("shelf.json", "w"), indent=1)
    print(len(shelf), sorted(shelf))


if __name__ == "__main__":
    main(sys.argv[1])
