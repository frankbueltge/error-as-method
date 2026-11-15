"""Post hoc, after score.py: NOT a committed prediction.

score.py showed song A's makers far in pitch (0.30) though they hardly moved a note. The cause
is in melody.distance: pitch is taken relative to the final note, and every maker changed the
final note. This file (1) counts the endings, and (2) recomputes distance with pitch relative
to the tonic (the tonic pitch class just at or below the final), so one changed ending no
longer shifts the whole melody. All four songs are in G major (MTC features 'tonic', 'mode').

Run: python3 -I posthoc.py -> posthoc.json
"""
import gzip, json, os, sys, statistics, collections, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import melody
from melody import parse_text
from briefs import parse_answer, SONGS

HERE = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(HERE, 'plan.json')))
rows = {}
for l in gzip.open(os.path.join(HERE, 'sources/ann.jsonl.gz'), 'rt'):
    r = json.loads(l)
    rows[r['id']] = r
class _PC(dict):
    # Humdrum tonic names: a letter, then '#' (sharp) or '-' (flat), possibly repeated
    def __missing__(self, k):
        base = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}[k[0].upper()]
        return (base + k.count('#') - k.count('-')) % 12


PC = _PC()


def notes_of(r):
    f = r['features']
    return [(p, d, bool(e)) for p, d, e in zip(f['midipitch'], f['duration'], f['phrase_end'])]


def make_norm(tonic_pc):
    def norm_t(notes):
        fin = notes[-1][0]
        ref = fin - ((fin - tonic_pc) % 12)
        med = statistics.median(d for _, d, _ in notes) or 1.0
        return [(p - ref, d / med) for p, d, _ in notes]
    return norm_t


face_patch = {}
out = {'note': 'post hoc; tonic-relative distance; endings counted', 'songs': []}
for k, fam in zip(SONGS, plan['families']):
    src_r = rows[fam['source']]
    tpc = PC[src_r['features']['tonic'][0]]
    src = notes_of(src_r)
    people = [(x['id'], notes_of(rows[x['id']])) for x in fam['people']]
    par = [parse_text(parse_answer(os.path.join(HERE, f'makings/parallel-{i}.txt'))[k][1]) for i in range(1, 6)]
    chain = [parse_text(parse_answer(os.path.join(HERE, f'makings/chain-{i}.txt'))[k][1]) for i in range(1, 6)]
    deg = lambda p: (p - tpc) % 12
    endings = {
        'source': deg(src[-1][0]),
        'people': dict(collections.Counter((m[-1][0] - PC[rows[i]['features']['tonic'][0]]) % 12 for i, m in people)),  # each variant's own tonic
        'parallel': [deg(m[-1][0]) for m in par],
        'chain': [deg(m[-1][0]) for m in chain],
    }
    tonic_of = lambda i: PC[rows[i]['features']['tonic'][0]]
    dd = {
        'people': [melody.distance_tonic(src, tpc, m, tonic_of(i)) for i, m in people],
        'parallel': [melody.distance_tonic(src, tpc, m, tpc) for m in par],
        'chain': [melody.distance_tonic(src, tpc, m, tpc) for m in chain],
    }
    null = sorted(melody.distance_tonic(src, tpc, notes_of(r), PC[r['features']['tonic'][0]])
                  for r in rows.values() if r['tunefamily'] != fam['family'])
    dd_null = {'median': statistics.median(null), 'p10': null[len(null) // 10]}
    face_patch[k] = {'people': dd['people'], 'parallel': dd['parallel'], 'chain': dd['chain'],
                     'null_median': dd_null['median'], 'null_p10': dd_null['p10']}
    out['songs'].append({
        'song': k, 'endings_semitones_above_tonic': endings,
        'tonic_rel': {nm: [round(x, 3) for x in v] for nm, v in dd.items()},
        'tonic_rel_median': {nm: round(statistics.median(v), 3) for nm, v in dd.items()},
        'tonic_rel_null': {k2: round(v2, 3) for k2, v2 in dd_null.items()},
        'tonic_rel_pairwise_people_median': round(statistics.median(melody.distance_tonic(a, tonic_of(i), b, tonic_of(j)) for (i, a), (j, b) in itertools.combinations(people, 2)), 3),
        'tonic_rel_pairwise_parallel_median': round(statistics.median(melody.distance_tonic(a, tpc, b, tpc) for a, b in itertools.combinations(par, 2)), 3),
    })
    print(k, endings, {nm: round(statistics.median(v), 3) for nm, v in dd.items()}, 'chain', [round(x, 3) for x in dd['chain']])
json.dump(out, open(os.path.join(HERE, 'posthoc.json'), 'w'), indent=1)

# the face draws the tonic-relative distances (the predictions were scored on the final-relative ones, score.py)
fd = os.path.join(HERE, 'face-data.js')
txt = open(fd).read()
face = json.loads(txt[len('window.CARRIED='):-2])
for s_ in face['songs']:
    p = face_patch[s_['key']]
    for nm in ('people', 'parallel', 'chain'):
        for v, d in zip(s_[nm], p[nm]):
            v['d_final'] = v['d']
            v['d'] = d
    s_['null_median'], s_['null_p10'] = p['null_median'], p['null_p10']
open(fd, 'w').write('window.CARRIED=' + json.dumps(face, separators=(',', ':')) + ';\n')
