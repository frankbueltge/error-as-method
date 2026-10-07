"""verify.py: git order, hashes and reproducibility of Other Trainings. Run from this directory."""
import subprocess, json, hashlib, os, sys
W = 'works/2026-10-07-other-trainings/'
revs = subprocess.run(['git', 'rev-list', '--reverse', 'HEAD'], capture_output=True, text=True, cwd='../..').stdout.split()
def first(path):
    out = subprocess.run(['git', 'log', '--diff-filter=A', '--format=%H', '--', W + path], capture_output=True, text=True, cwd='../..').stdout.split()
    return revs.index(out[-1]) if out else None
ok = bad = 0
def check(name, cond):
    global ok, bad
    print(('PASS ' if cond else 'FAIL ') + name); ok += bool(cond); bad += (not cond)
o = {p: first(p) for p in ['PREDICTIONS.md', 'forecast.json', 'home.py', 'render.py', 'load.py', 'readers/PROMPT.md',
                           'sources/hourly-2025.json', 'sources/daily-2025.json', 'home.json', 'renders/T1.png', 'renders/T3.txt']}
for k, v in o.items(): check(f'{k} is committed', v is not None)
check('pre-registration, forecast, home tool, renderer, loader and prompt land together',
      len({o[k] for k in ['PREDICTIONS.md', 'forecast.json', 'home.py', 'render.py', 'load.py', 'readers/PROMPT.md']}) == 1)
check('... before the material', o['PREDICTIONS.md'] < o['sources/hourly-2025.json'] == o['sources/daily-2025.json'])
check('home.json and the renders after the material', o['sources/hourly-2025.json'] < o['home.json'] == o['renders/T1.png'] == o['renders/T3.txt'])
readers = sorted(f for f in os.listdir('readers') if f.endswith('.json'))
rc = {f[:-5]: first('readers/' + f) for f in readers}
check('12 readings committed', len(readers) == 12)
check('every reading after the renders', all(v > o['renders/T1.png'] for v in rc.values()))
check('every reading in a commit of its own', len(set(rc.values())) == 12)
seq = 'K1-T3a K2-T1a K0-T1a K0-T3a K0-T1b K1-T1b K0-T3b K2-T3b K1-T1a K2-T1b K2-T3a K1-T3b'.split()
check('readings committed in the drawn order (order.py, seed 112)', [rc[n] for n in seq] == sorted(rc.values()))
check('order.py prints the drawn order', subprocess.run([sys.executable, 'order.py'], capture_output=True, text=True).stdout.split() == seq)
m = json.load(open('sources/MANIFEST.json'))
for n in ('hourly', 'daily'):
    check(f'{n} hash matches the manifest', hashlib.sha256(open(f'sources/{n}-2025.json', 'rb').read()).hexdigest() == m[n]['sha256'])
before = {f: open(f).read() for f in ['home.json', 'results.json', 'posthoc.json', 'data.js', 'figure.svg', 'renders/T3.txt']}
for s in ['home.py', 'render.py', 'score.py', 'posthoc.py', 'build.py', 'figure.py']: subprocess.run([sys.executable, s], capture_output=True)
for f, t in before.items(): check(f'{f} reproduces byte-identical', open(f).read() == t)
r = json.load(open('results.json')); h = json.load(open('home.json')); p = json.load(open('posthoc.json'))
check('2 events, 5 days over 50', h['n_events'] == 2 and h['n_exceedance_days'] == 5)
check('P1-P5 all fail (as reported)', not any(r[k]['holds'] for k in ['P1', 'P2', 'P3', 'P4', 'P5']))
check('forecast misses: 14 regular, 12 singular', (r['P1']['regular_misses'], r['P1']['singular_misses']) == (14, 12))
check('89 of 104 items outside every event', (r['P3']['outside'], r['P3']['items']) == (89, 104))
check('7 spike days; 10 of 12 readings name 6 or 7 of them', len(p['spike_days']) == 7 and sum(len(v) >= 6 for v in p['named_by_reader_tol1'].values()) == 10)
check('only K0 names the quantity in 2 or more readings', {k: len(v) for k, v in r['P4']['named_by_kind'].items()} == {'K0': 4, 'K1': 1, 'K2': 0})
print(f'{ok} pass, {bad} fail'); sys.exit(1 if bad else 0)
