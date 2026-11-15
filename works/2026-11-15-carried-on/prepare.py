"""Choose the four songs and their sources, and compute the people's baseline.

Run: python3 -I prepare.py   (from this directory; reads sources/ann.jsonl.gz)
Writes plan.json: per family the source melody (the medoid of the family's sung and
printed variants under melody.distance), its text, and every variant's distance to it;
plus the null: the source's distance to every melody of every other family.
"""
import gzip, json, os, sys, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from melody import to_text, distance

HERE = os.path.dirname(os.path.abspath(__file__))
rows = [json.loads(l) for l in gzip.open(os.path.join(HERE, 'sources/ann.jsonl.gz'), 'rt')]


def notes_of(r):
    f = r['features']
    return [(p, d, bool(e)) for p, d, e in zip(f['midipitch'], f['duration'], f['phrase_end'])]


mel = {r['id']: notes_of(r) for r in rows}
fam = {}
for r in rows:
    fam.setdefault(r['tunefamily'], []).append(r['id'])
meter = {r['id']: r['features']['timesignature'][0] for r in rows}

# Choose: families with at least 15 variants, sources of 25-60 notes, and four
# different meters/characters where possible; the rule is fixed, not hand-picked.
cands = []
for f, ids in fam.items():
    if len(ids) < 15:
        continue
    sums = {i: sum(distance(mel[i], mel[j]) for j in ids if j != i) for i in ids}
    src = min(sums, key=sums.get)
    if 25 <= len(mel[src]) <= 60:
        cands.append((f, src, len(ids)))
cands.sort(key=lambda x: (-x[2], x[0]))
chosen = cands[:4]

plan = {'families': []}
for f, src, n in chosen:
    within = [{'id': j, 'd': distance(mel[src], mel[j])} for j in fam[f] if j != src]
    others = [distance(mel[src], mel[j]) for g, ids in fam.items() if g != f for j in ids]
    plan['families'].append({
        'family': f, 'source': src, 'meter': meter[src], 'n_variants': n,
        'notes': len(mel[src]), 'text': to_text(mel[src], meter[src]),
        'people': within,
        'people_median': statistics.median(x['d'] for x in within),
        'null_median': statistics.median(others),
        'null_p10': sorted(others)[len(others) // 10],
    })
    print(f, src, n, len(mel[src]), round(plan['families'][-1]['people_median'], 3),
          round(plan['families'][-1]['null_median'], 3), round(plan['families'][-1]['null_p10'], 3))
print('candidates', [(c[0], c[2]) for c in cands])
json.dump(plan, open(os.path.join(HERE, 'plan.json'), 'w'), indent=1)
