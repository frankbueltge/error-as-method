"""verify.py: git order and reproducibility of The Balance. Run from this directory."""
import subprocess, json, os, sys
W = 'works/2026-10-07-the-balance/'
revs = subprocess.run(['git', 'rev-list', '--reverse', 'HEAD'], capture_output=True, text=True, cwd='../..').stdout.split()
def first(path):
    out = subprocess.run(['git', 'log', '--diff-filter=A', '--format=%H', '--', W + path], capture_output=True, text=True, cwd='../..').stdout.split()
    return revs.index(out[-1]) if out else None
ok = bad = 0
def check(name, cond):
    global ok, bad
    print(('PASS ' if cond else 'FAIL ') + name); ok += bool(cond); bad += (not cond)
Ls = ('P1', 'P2', 'B1', 'B2')
pre = {f: first(f) for f in ['PREDICTIONS.md', 'briefs/v0.md', 'briefs/plain.md', 'briefs/balance.md', 'order.py', 'prepare.py']}
check('pre-registration, briefs, order and preparation are committed together', None not in pre.values() and len(set(pre.values())) == 1)
check('... before the material', pre['PREDICTIONS.md'] < first('data/extent.js'))
for k in range(5):
    v = [first(f'lineages/{L}/v{k}/index.html') for L in Ls]; s = [first(f'shots/{L}-v{k}.png') for L in Ls]
    check(f'v{k}: all four versions in one commit, after the material', len(set(v)) == 1 and v[0] > first('data/extent.js'))
    check(f'v{k}: screenshots in one commit after the versions', len(set(s)) == 1 and s[0] > v[0])
    if k < 4:
        check(f'v{k+1} made after the screenshots of v{k}', first(f'lineages/P1/v{k+1}/NOTE.md') > s[0])
blind = first('coder/blind.json'); key = first('coder/KEY.json')
check('mask, key and coder prompt before the blind coding, after v4 screenshots', first('coder/PROMPT.md') == key < blind and key > first('shots/B2-v4.png'))
check('open coding after the blind coding', first('open.json') > blind)
check('control declared after the blind coding and before the control files', blind < first('CONTROL.md') < first('control/C1/index.html'))
check('order.py reproduces the key', json.load(open('coder/KEY.json'))['transitions'] == __import__('order').masks)
before = {f: open(f).read() for f in ['results.json', 'data.js', 'figure.svg']}
for s in ('score.py', 'build.py', 'figure.py'): subprocess.run([sys.executable, s], capture_output=True)
for f, t in before.items(): check(f'{f} reproduces', open(f).read() == t)
check('P1 v3 is byte-identical to v2 (the declined version)', open('lineages/P1/v3/index.html').read() == open('lineages/P1/v2/index.html').read())
print(f'{ok} passed, {bad} failed'); sys.exit(1 if bad else 0)
