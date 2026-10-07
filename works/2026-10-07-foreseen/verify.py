"""verify.py: git order, hashes and reproducibility of Foreseen. Run from this directory."""
import subprocess, json, hashlib, os, sys
W = 'works/2026-10-07-foreseen/'
def first_commit(path):
    out = subprocess.run(['git', 'log', '--diff-filter=A', '--format=%H', '--', W + path], capture_output=True, text=True, cwd='../..').stdout.split()
    return out[-1] if out else None
revs = subprocess.run(['git', 'rev-list', '--reverse', 'HEAD'], capture_output=True, text=True, cwd='../..').stdout.split()
order = lambda c: revs.index(c)
ok = bad = 0
def check(name, cond):
    global ok, bad
    print(('PASS ' if cond else 'FAIL ') + name); ok += bool(cond); bad += (not cond)
files = ['PREDICTIONS.md', 'forecast.json', 'home.py', 'render.py', 'readers/PROMPT.md', 'fetch.py',
         'sources/full-moon-2024-2025.json', 'home.json', 'renders/T1.png', 'renders/T5.txt', 'results.json', 'posthoc.json']
c = {p: first_commit(p) for p in files}
for k, v in c.items(): check(f'{k} is committed', v is not None)
o = {k: order(v) for k, v in c.items() if v}
check('forecast, rules, translations and prompt land together, before the material',
      o['PREDICTIONS.md'] == o['forecast.json'] == o['home.py'] == o['render.py'] == o['readers/PROMPT.md'] < o['sources/full-moon-2024-2025.json'])
check('home.json and renders after the material', o['sources/full-moon-2024-2025.json'] < o['home.json'] == o['renders/T1.png'] == o['renders/T5.txt'])
rd = sorted(f for f in os.listdir('readers') if f.startswith('F-'))
rc = {f: order(first_commit('readers/' + f)) for f in rd}
check('10 readings, two per translation', len(rd) == 10 and all(sum(f.startswith(f'F-T{i}') for f in rd) == 2 for i in range(1, 6)))
check('every reading after the renders', all(v > o['home.json'] for v in rc.values()))
check('every reading in a commit of its own', len(set(rc.values())) == 10)
check('scores after every reading', o['results.json'] > max(rc.values()))
check('forecast.json unchanged since the pre-registration',
      subprocess.run(['git', 'diff', '--quiet', c['forecast.json'], 'HEAD', '--', W + 'forecast.json'], cwd='../..').returncode == 0)
check('each reader opened only its own file', all(len(json.load(open('readers/' + f))['answer']['files_opened']) == 1 and
      json.load(open('readers/' + f))['answer']['files_opened'][0].endswith(f[2:4] + ('.txt' if f[2:4] == 'T5' else '.png')) for f in rd))
m = json.load(open('sources/MANIFEST.json'))
check('material hash matches the manifest', hashlib.sha256(open('sources/full-moon-2024-2025.json', 'rb').read()).hexdigest() == m['pageviews']['sha256'])
check('phase extract hash matches the manifest', hashlib.sha256(open('sources/moon-phases-2024-2025.txt', 'rb').read()).hexdigest() == m['moon_phases']['extract_sha256'])
before = {f: open(f).read() for f in ['home.json', 'results.json', 'posthoc.json', 'data.js', 'figure.svg']}
for s in ['home.py', 'score.py', 'posthoc.py', 'build.py', 'figure.py']: subprocess.run([sys.executable, s], capture_output=True)
for f, t in before.items(): check(f'{f} reproduces byte-identical', open(f).read() == t)
r = json.load(open('results.json')); p = json.load(open('posthoc.json')); h = json.load(open('home.json'))
check('P1 11 vs 10, P2 59, P3 fails, P4 9, P5 fails (as reported)',
      r['misses'] == {'regular': 10, 'singular': 11} and r['matches'] == 59 and not r['P3']['holds'] and r['P4']['moon_guesses'] == 9 and not r['P5']['holds'])
check('24 home events, all within 1.5 days of a full moon', h['n_events'] == 24 and p['events_within_1_day_of_full'] == 24)
check('47 marks, 28 outside every home event', r['S111']['marks'] == 47 and r['S111']['outside'] == 28)
check('18 of 21 misses: forecast blind, reader saw', sum(m['direction'].startswith('forecast blind') for m in p['misses']) == 18 and len(p['misses']) == 21)
print(f'{ok} pass, {bad} fail'); sys.exit(1 if bad else 0)
