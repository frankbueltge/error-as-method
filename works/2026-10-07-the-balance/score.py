"""score.py: scores P1-P7 and the control from blind.json, open.json, the key, the sizes and the notes -> results.json"""
import json, os, statistics as st
key = json.load(open('coder/KEY.json')); b = json.load(open('coder/blind.json')); o = json.load(open('open.json'))
Ls = ('P1', 'P2', 'B1', 'B2'); T = [f'{L}-{k}' for L in Ls for k in range(1, 5)]
blind = {t: b['pairs'][key['transitions'][t]]['code'] for t in T}; opn = {t: o[t][0] for t in T}
folded = {s: b['singles'][m]['folded'] for s, m in key['singles'].items()}
size = {f'{L}-v{k}': os.path.getsize(f'lineages/{L}/v{k}/index.html') for L in Ls for k in range(5)}
notes = {L: open(f'lineages/{L}/v4/NOTE.md').read() for L in Ls}
def n(codes, arm, which): return sum(codes[t] in which for t in T if t[0] == arm)
growth = {L: size[f'{L}-v4'] - size[f'{L}-v0'] for L in Ls}
declined = [t for t in T if blind[t] == 'SAME' and opn[t] == 'SAME' and open(f'lineages/{t[:2]}/v{t[3]}/index.html').read() == open(f'lineages/{t[:2]}/v{int(t[3])-1}/index.html').read()]
r = {'blind': blind, 'open': opn, 'folded': folded, 'bytes': size, 'growth_v0_v4': growth, 'declined': declined,
     'balance_in_v0_note': {L: 'balance' in notes[L].split('## v1')[0].lower() or 'scale' in notes[L].split('## v1')[0].lower() for L in Ls}}
mould_v0 = [L for L in Ls if folded[f'{L}-v0'] == 'yes']
r['P1'] = {'in_mould_v0': mould_v0, 'held': len(mould_v0) >= 3}
pADD = n(blind, 'P', {'ADD'})
r['P2'] = {'plain_growth': [growth['P1'], growth['P2']], 'plain_ADD_blind': pADD, 'held': growth['P1'] > 0 and growth['P2'] > 0 and pADD >= 5}
ss = {'SCHEMA', 'STRIKE'}
r['P3'] = {'blind': [n(blind, 'B', ss), n(blind, 'P', ss)], 'open': [n(opn, 'B', ss), n(opn, 'P', ss)],
           'held': n(blind, 'B', ss) > n(blind, 'P', ss) and n(opn, 'B', ss) > n(opn, 'P', ss)}
mb, mp = st.median([growth['B1'], growth['B2']]), st.median([growth['P1'], growth['P2']])
r['P4'] = {'median_growth_balance': mb, 'median_growth_plain': mp, 'held': mb < mp}
r['P5'] = {'note': 'no lineage was in the mould at v0, so the prediction has no case', 'held': None,
           'posthoc_entered_mould': [L for L in Ls if folded[f'{L}-v0'] == 'no' and folded[f'{L}-v4'] == 'yes']}
claims = 8  # every balance-arm heading v1-v4 answers (a) and (b) with a named convergence and obstacle; none declined (read in NOTE.md)
bs = sum(blind[t] == 'SCHEMA' for t in T if t[0] == 'B')
r['P6'] = {'claims': claims, 'blind_SCHEMA_of_those': bs, 'held': claims >= 6 and bs <= 3}
r['P7'] = {'declined': declined, 'held': not declined}
json.dump(r, open('results.json', 'w'), indent=1)
for p in ('P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7'): print(p, r[p])
print(r['balance_in_v0_note'])
