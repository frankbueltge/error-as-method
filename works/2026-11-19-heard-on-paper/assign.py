"""Seeded assignment of the ten spectrograms to eight makers (seed 20261119).
Per arm: two shuffles of a..j; the first shuffle's halves go to makers 1 and 2, the second's to 3 and 4,
so every image is made twice in each arm by two different makers."""
import json, random
rng = random.Random(20261119)
keys = list("abcdefghij")
out = {}
for arm in ("U", "N"):
    s1 = keys[:]; rng.shuffle(s1); s2 = keys[:]; rng.shuffle(s2)
    for i, part in enumerate([s1[:5], s1[5:], s2[:5], s2[5:]], 1):
        out[f"{arm}{i}"] = sorted(part)
json.dump(out, open("briefs/assignment.json", "w"), indent=1)
print(out)
