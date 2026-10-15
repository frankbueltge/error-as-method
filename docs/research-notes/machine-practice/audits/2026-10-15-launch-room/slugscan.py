import os,re,sys,json
root=sys.argv[1]
exps=[('the-balance',['balance']),('not-addressed',['addressed','unaddressed']),('customary-lines',['customary']),
('who-looks',['who looks','who-looks']),('order-words',['order-word','order word']),('prepared-clay',['clay']),
('without-ticks',['without ticks','tickless','no ticks']),('down-to-the-grain',['grain']),('told-the-hour',['told the hour','told-the-hour']),
('the-same-swing',['swing']),('told-a-tide',['told a tide','told-a-tide'])]
dirs={s:[d for d in os.listdir(root+'/works') if d.endswith(s) and d.startswith('2026-10')][0] for s,_ in exps}
def files(s):
    w=os.path.join(root,'works',dirs[s]); out=[]
    for sub in ('makers','reports','lineages'):
        for dp,_,fs in os.walk(os.path.join(w,sub)):
            for f in fs:
                if f.endswith(('.md','.html','.js','.txt')): out.append(os.path.join(dp,f))
    return out
# unit: maker = top-level folder under makers/ or lineage version; report files counted with their maker id
def units(s):
    u={}
    w=os.path.join(root,'works',dirs[s])
    for p in files(s):
        rel=os.path.relpath(p,w).split(os.sep)
        if rel[0]=='reports': key=os.path.splitext(rel[1])[0]
        elif rel[0]=='lineages': key='/'.join(rel[1:3])
        else: key=rel[1]
        if 'scratch' in rel: continue
        u.setdefault(key,'')
        try: u[key]+=open(p,errors='ignore').read().lower()+'\n'
        except: pass
    return u
U={s:units(s) for s,_ in exps}
res={}
print('experiment'.ljust(18),'n ',' '.join(s[:9].rjust(9) for s,_ in exps))
for s,_ in exps:
    row=[]
    for t,words in exps:
        k=sum(1 for txt in U[s].values() if any(re.search(r'\b'+re.escape(w)+r'\b',txt) for w in words))
        row.append(k)
    res[s]=row
    print(s[:18].ljust(18),str(len(U[s])).ljust(3),' '.join(str(x).rjust(9) for x in row))
json.dump({'units':{s:len(U[s]) for s in U},'matrix':res,'words':dict(exps),'dirs':dirs},open(sys.argv[2],'w'),indent=1)
