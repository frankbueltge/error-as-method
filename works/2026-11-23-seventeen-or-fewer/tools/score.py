"""Score experiment 59 from the committed makings/ and people/counts.json.

usage: python3 -I tools/score.py <experiment dir> <cmudict.dict>
Writes results.json and face-data.js in the experiment dir.
"""
import json, os, re, sys, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import syl

W = sys.argv[1]
syl.load(sys.argv[2])
SUBJ = ['laundromat', 'frost', 'waiting']
ARMS = ['W', 'F', 'J']
override = {}
op = os.path.join(W, 'counts_by_eye.json')
if os.path.exists(op):
    override = json.load(open(op))

def read_poem(p):
    lines = [l.rstrip() for l in open(p, encoding='utf-8').read().split('\n')]
    lines = [l.strip() for l in lines if l.strip()]
    return lines

def count(key, lines):
    if key in override:
        return override[key]['counts'], 'eye'
    c, ok = syl.poem(lines)
    return c, 'dict' if ok else 'guess'

makers, poems = [], []
for a in ARMS:
    for i in range(1, 5):
        m = f'{a}{i}'
        d = os.path.join(W, 'makings', m)
        notes = open(os.path.join(d, 'notes.md'), encoding='utf-8').read()
        low = notes.lower()
        mk = dict(maker=m, arm=a, mentions_count=bool(re.search(r'syllab|5-7-5|5/7/5|five-seven-five|seventeen|\b17\b|count', low)),
                  mentions_575=bool(re.search(r'5-7-5|5/7/5|five-seven-five|seventeen syllab|17 syllab|17-syllab', low)))
        makers.append(mk)
        for s in SUBJ:
            vs = sorted([f for f in os.listdir(d) if re.fullmatch(rf'{s}-v\d+\.txt', f)], key=lambda f: int(re.search(r'v(\d+)', f).group(1)))
            vers = []
            for f in vs + [f'{s}-final.txt']:
                lines = read_poem(os.path.join(d, f))
                key = f'{m}/{f}'
                c, how = count(key, lines)
                vers.append(dict(file=f, lines=lines, counts=c, how=how, total=sum(c), is575=c == [5, 7, 5]))
            first, final = vers[0], vers[-1]
            poems.append(dict(maker=m, arm=a, subject=s, versions=len(vs), first=first, final=final,
                              type_first='575' if first['is575'] else 'other',
                              type_final='575' if final['is575'] else 'other'))

def arm(a): return [p for p in poems if p['arm'] == a]
res = {}
for a in ARMS:
    ps = arm(a)
    res[a] = dict(finals=len(ps), final_575=sum(p['final']['is575'] for p in ps),
                  first_575=sum(p['first']['is575'] for p in ps),
                  median_total=statistics.median(p['final']['total'] for p in ps),
                  three_lines=sum(len(p['final']['counts']) == 3 for p in ps),
                  versions=sum(p['versions'] for p in ps))
kept = sum(p['type_first'] == p['type_final'] for p in poems)
P = {}
P['P1'] = dict(rule='W: >=9 of 12 finals 5-7-5', value=res['W']['final_575'], held=res['W']['final_575'] >= 9)
diffs = {f'{x}-{y}': abs(res[x]['final_575'] - res[y]['final_575']) for x, y in [('W', 'F'), ('W', 'J'), ('F', 'J')]}
P['P2'] = dict(rule='any two arms differ by <=3 of 12 in 5-7-5 finals', value=diffs, held=max(diffs.values()) <= 3,
               falsifier_fired={k: v >= 6 for k, v in diffs.items() if k.startswith('W')})
P['P4'] = dict(rule='>=30 of 36 keep type v1 -> final', value=kept, held=kept >= 30)
nc = sum(m['mentions_count'] for m in makers)
P['P5'] = dict(rule='>=9 of 12 makers mention syllables or counting', value=nc, held=nc >= 9)
P['P6'] = dict(rule="J median final total within 3 of the journal sheet's 11", value=res['J']['median_total'],
               held=abs(res['J']['median_total'] - 11) <= 3)
IMAGES = {  # post hoc: read after the run, not predicted
    'a garment waving through the dryer glass': r'(sleeve|shirt).*wav|wav.*(sleeve|shirt)',
    'a stranger': r'stranger',
    'the garden hose keeping its shape or coil': r'hose',
    'a name called, heads lifting': r'name|look up|head',
    'all-night laundromat': r'all-night',
    'the green shape where something slept': r'green shape',
}
post_hoc = {k: {a: [p['maker'] for p in poems if p['arm'] == a and re.search(v, ' '.join(p['final']['lines']).lower())]
                for a in ARMS} for k, v in IMAGES.items()}
out = dict(arms=res, predictions=P, makers=makers, poems=poems, post_hoc_images=post_hoc,
           P3_by_reading=dict(rule='forum arm: >=3 of 4 name the sheet majority form; >=3 of 4 depart or divide',
                              names_majority=['F1', 'F2', 'F3', 'F4'], divides=['F1', 'F2', 'F3', 'F4'], held=True,
                              note='read from notes.md, section "What I see in the fifty"; all four name the same three forum poems as the ones that hold up'))
json.dump(out, open(os.path.join(W, 'results.json'), 'w'), indent=1, ensure_ascii=False)

people = json.load(open(os.path.join(W, 'people', 'counts.json')))
face = dict(forum=[x['counts'] for x in people['forum_all_100'][:50]],
            journal=[x['counts'] for x in people['journal_all_105'][:50]],
            makers=[dict(m=p['maker'], arm=p['arm'], s=p['subject'], lines=p['final']['lines'], c=p['final']['counts'],
                         v1=p['first']['lines'], v1c=p['first']['counts'], n=p['versions']) for p in poems],
            results=dict(arms=res, predictions={k: dict(rule=v['rule'], held=v['held']) for k, v in P.items()}))
open(os.path.join(W, 'face-data.js'), 'w').write('window.FACE=' + json.dumps(face, ensure_ascii=False) + ';\n')
print(json.dumps(dict(arms=res, predictions=P), indent=1))
