"""verify.py: git order, hashes and reproducibility of Unknowing. Run from this directory."""
import subprocess, json, hashlib, os, sys
W = 'works/2026-10-07-unknowing/'
def first_commit(path):
    out = subprocess.run(['git', 'log', '--diff-filter=A', '--format=%H %ct', '--', W + path], capture_output=True, text=True, cwd='../..').stdout.split()
    return out[-2] if out else None
def order(c):  # position in first-parent history (older = smaller)
    revs = subprocess.run(['git', 'rev-list', '--reverse', 'HEAD'], capture_output=True, text=True, cwd='../..').stdout.split()
    return revs.index(c)
ok = 0; bad = 0
def check(name, cond):
    global ok, bad
    print(('PASS ' if cond else 'FAIL ') + name); ok += cond; bad += (not cond)
c = {p: first_commit(p) for p in ['PREDICTIONS.md', 'home.py', 'render.py', 'readers/PROMPT.md', 'sources/kp-2025.txt', 'home.json', 'renders/T1.png', 'FORECAST.md', 'forecast.json']}
for k, v in c.items(): check(f'{k} is committed', v is not None)
o = {k: order(v) for k, v in c.items() if v}
check('pre-registration, home.py, render.py and the prompt land together, before the material',
      o['PREDICTIONS.md'] == o['home.py'] == o['render.py'] == o['readers/PROMPT.md'] < o['sources/kp-2025.txt'])
check('home.json and the renders after the material', o['sources/kp-2025.txt'] < o['home.json'] == o['renders/T1.png'])
check('forecast after home.json', o['home.json'] < o['FORECAST.md'] == o['forecast.json'])
readers = sorted(f for f in os.listdir('readers') if f.endswith('.json'))
rc = {f: order(first_commit('readers/' + f)) for f in readers}
check('16 readings committed', len(readers) == 16)
check('every reading after the forecast', all(v > o['FORECAST.md'] for v in rc.values()))
check('every reading in a commit of its own', len(set(rc.values())) == 16)
for s in ('S1', 'S2'):
    st = sorted(f for f in readers if f.startswith(s))
    check(f'{s} steps committed in reading order', [rc[f] for f in st] == sorted(rc[f] for f in st))
m = json.load(open('sources/MANIFEST.json'))
check('window hash matches the manifest', hashlib.sha256(open('sources/kp-2025.txt', 'rb').read()).hexdigest() == m['window_sha256'])
check('window has 2,920 lines', sum(1 for _ in open('sources/kp-2025.txt')) == 2920)
before = {f: open(f).read() for f in ['home.json', 'results.json', 'posthoc.json', 'data.js']}
for s in ['home.py', 'score.py', 'posthoc.py', 'build.py']: subprocess.run([sys.executable, s], capture_output=True)
for f, t in before.items(): check(f'{f} reproduces byte-identical', open(f).read() == t)
r = json.load(open('results.json'))
check('P5 holds, P1-P4 fail (as reported)', r['P5']['holds'] and not any(r[k]['holds'] for k in ['P1', 'P2', 'P3', 'P4']))
h = json.load(open('home.json'))
check('21 events, 7 of them at 6-', h['n_events'] == 21 and sum(abs(e['peak_kp'] - 5.667) < 1e-3 for e in h['events']) == 7)
check('no fresh reading found a 6- event', not any(e['id'] in x['found'] for x in r['readers'].values() if x['condition'] == 'fresh' for e in h['events'] if abs(e['peak_kp'] - 5.667) < 1e-3))
p = json.load(open('posthoc.json'))
check('no item outside every event window', p['items_outside_every_event_window'] == 0 and p['items_total'] == 115)
check('carry: 12 beyond both fresh, 7 named earlier', p['carry_totals'] == {'beyond_both_fresh': 12, 'named_earlier': 7})
print(f'{ok} pass, {bad} fail'); sys.exit(1 if bad else 0)
