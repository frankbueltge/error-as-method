import sys,csv; sys.path.insert(0,'/tmp/claude-0/s146root/packets/V/scratch'); from cells import cells
from collections import Counter,defaultdict
from itertools import combinations
d=list(csv.DictReader(open('/tmp/claude-0/s146root/packets/V/data/dogs.csv')))
def check(path,key,**kw):
    groups=sorted(set(r[key] for r in d),key=lambda g:(float(g) if g.replace('.','').isdigit() else g))
    s=cells(path,**kw)
    cnt=Counter(r[key] for r in d); i=0; sigvec=defaultdict(lambda:[0]*len(groups))
    for gi,g in enumerate(groups):
        for k in range(cnt[g]): sigvec[s[i]][gi]+=1; i+=1
    namevec=defaultdict(lambda:[0]*len(groups))
    for r in d: namevec[r['HundefarbeText']][groups.index(r[key])]+=1
    names=dict((k,tuple(v)) for k,v in namevec.items()); sigs=dict((k,tuple(v)) for k,v in sigvec.items())
    unmatched_sig=[]; left=dict(names)
    for sg,v in sorted(sigs.items(),key=lambda kv:-sum(kv[1])):
        ex=[n for n,nv in left.items() if nv==v]
        if ex: del left[ex[0]]; continue
        unmatched_sig.append((sg,v))
    # try combos
    still=[]
    for sg,v in unmatched_sig:
        cand=[n for n,nv in left.items() if all(a<=b for a,b in zip(nv,v))]
        found=None
        for k in (2,3,4):
            for cb in combinations(cand,k):
                if tuple(map(sum,zip(*[left[n] for n in cb])))==v: found=cb;break
            if found: break
        if found:
            for n in found: del left[n]
        else: still.append((Counter(sg).most_common(2),v,sum(v)))
    return groups,still,left
if __name__=='__main__':
    g,still,left=check(sys.argv[1],sys.argv[2])
    print(g); print('unmatched sigs',len(still))
    for x in still: print(x)
    print('unused names',left)
