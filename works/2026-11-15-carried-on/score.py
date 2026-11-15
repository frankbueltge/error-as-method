"""Score the makings against the people and the null; check P1-P6 as committed.

Run: python3 -I score.py  -> results.json, face-data.js
"""
import gzip, json, math, os, sys, statistics, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from melody import parse_text, distance, dist3, norm, to_text
from briefs import parse_answer, SONGS

HERE = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(HERE, 'plan.json')))
rows = {json.loads(l)['id']: json.loads(l) for l in gzip.open(os.path.join(HERE, 'sources/ann.jsonl.gz'), 'rt')}


def notes_of(r):
    f = r['features']
    return [(p, d, bool(e)) for p, d, e in zip(f['midipitch'], f['duration'], f['phrase_end'])]


def entropy(m):
    c = collections.Counter(p for p, _ in norm(m))
    n = sum(c.values())
    return -sum(v / n * math.log2(v / n) for v in c.values())


def med(xs):
    return statistics.median(xs)


res = {'songs': []}
face = {'songs': []}
for k, fam in zip(SONGS, plan['families']):
    src = notes_of(rows[fam['source']])
    people = [notes_of(rows[x['id']]) for x in fam['people']]
    par = [parse_text(parse_answer(os.path.join(HERE, f'makings/parallel-{i}.txt'))[k][1]) for i in range(1, 6)]
    chain = [parse_text(parse_answer(os.path.join(HERE, f'makings/chain-{i}.txt'))[k][1]) for i in range(1, 6)]
    d_people = [distance(src, m) for m in people]
    d_par = [distance(src, m) for m in par]
    d_chain = [distance(src, m) for m in chain]
    pw_people = [distance(a, b) for a, b in itertools.combinations(people, 2)]
    pw_par = [distance(a, b) for a, b in itertools.combinations(par, 2)]
    dl = lambda ms: [abs(len(m) - len(src)) / len(src) for m in ms]
    # pitch-in-place: share of aligned changes that are pitch, approximated by pitch vs rhythm distance
    d3_people = [dist3(src, m) for m in people]
    d3_par = [dist3(src, m) for m in par]
    exact = sum(1 for m in par if [(p, d) for p, d, _ in m] == [(p, d) for p, d, _ in src])
    s = {
        'song': k, 'family': fam['family'], 'source': fam['source'], 'n_people': len(people),
        'people_median': med(d_people), 'people_min': min(d_people), 'people_max': max(d_people),
        'null_median': fam['null_median'], 'null_p10': fam['null_p10'],
        'parallel': d_par, 'parallel_median': med(d_par), 'parallel_exact_copies': exact,
        'chain': d_chain,
        'pairwise_people_median': med(pw_people), 'pairwise_parallel_median': med(pw_par),
        'len_change_people_median': med(dl(people)), 'len_change_parallel_median': med(dl(par)),
        'pitch_people_median': med(x['pitch'] for x in d3_people), 'rhythm_people_median': med(x['rhythm'] for x in d3_people),
        'pitch_parallel_median': med(x['pitch'] for x in d3_par), 'rhythm_parallel_median': med(x['rhythm'] for x in d3_par),
        'entropy_source': entropy(src), 'entropy_chain5': entropy(chain[-1]),
        'people_closer_than_parallel_median': sum(1 for x in d_people if x < med(d_par)),
    }
    res['songs'].append(s)
    face['songs'].append({
        'key': k, 'family': fam['family'].replace('_', ' '), 'meter': fam['meter'],
        'source': {'id': fam['source'], 'notes': src},
        'people': [{'id': x['id'], 'year': rows[x['id']].get('year'), 'tonic': rows[x['id']]['features']['tonic'][0], 'd': d, 'notes': m}
                   for x, d, m in zip(fam['people'], d_people, people)],
        'parallel': [{'id': f'parallel-{i+1}', 'd': d, 'notes': m} for i, (d, m) in enumerate(zip(d_par, par))],
        'chain': [{'id': f'chain-{i+1}', 'd': d, 'notes': m} for i, (d, m) in enumerate(zip(d_chain, chain))],
        'null_median': fam['null_median'], 'null_p10': fam['null_p10'],
    })

S = res['songs']
P = {}
P['P1'] = sum(s['parallel_median'] < s['people_median'] for s in S)
P['P2'] = sum(s['pairwise_parallel_median'] < s['pairwise_people_median'] for s in S)
P['P3'] = sum(s['len_change_parallel_median'] > s['len_change_people_median'] for s in S)
P['P4a'] = sum(s['chain'][-1] > s['parallel_median'] for s in S)
P['P4b'] = sum(s['chain'][-1] < s['null_p10'] for s in S)
P['P5'] = sum(s['entropy_chain5'] <= s['entropy_source'] for s in S)
P['P6'] = sum(1 for s in S for d in s['parallel'] if d >= s['null_p10'])
res['verdicts'] = {
    'P1': ('holds' if P['P1'] >= 3 else 'falsified', P['P1']),
    'P2': ('holds' if P['P2'] >= 3 else 'falsified', P['P2']),
    'P3': ('holds' if P['P3'] >= 3 else 'falsified', P['P3']),
    'P4': ('holds' if P['P4a'] >= 3 and P['P4b'] == 4 else 'falsified', [P['P4a'], P['P4b']]),
    'P5': ('holds' if P['P5'] >= 3 else 'falsified', P['P5']),
    'P6': ('holds' if P['P6'] == 0 else 'falsified', P['P6']),
}
json.dump(res, open(os.path.join(HERE, 'results.json'), 'w'), indent=1)
open(os.path.join(HERE, 'face-data.js'), 'w').write('window.CARRIED=' + json.dumps(face, separators=(',', ':')) + ';\n')
for s in S:
    print(s['song'], {k: (round(v, 3) if isinstance(v, float) else ([round(x, 3) for x in v] if isinstance(v, list) else v))
                      for k, v in s.items() if k not in ('family', 'source')})
print(res['verdicts'])
