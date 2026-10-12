import json
# re-run assignment to keep x of each hour, then permit swaps between hours whose dots are < 1 px apart in x
exec(open('/tmp/claude-0/s122/mk/m02/scratch/assign.py').read().split("missing=[k")[0])
xs=[None]*m; j=m
# recover x for each assigned slot
j=m
for i in range(n,0,-1):
    while back[i-1][j]==0: j-=1
    xs[j-1]=d[i-1][0]; j-=1
S=json.load(open('/tmp/claude-0/s122/mk/m02/scratch/series.json')); v=S['v'][:]; miss=set(S['missing'])
def rough(a,b):
    return sum(abs(v[t-1]-2*v[t]+v[t+1]) for t in range(max(1,a),min(m-1,b)))
swaps=0
for it in range(12):
    ch=0
    for t in range(1,m-3):
      for u,lim in ((t+1,1.0),(t+2,1.7)):
        if t in miss or u in miss or u>=m-1: continue
        if abs(xs[u]-xs[t])<lim:
            r0=rough(t-1,u+2); v[t],v[u]=v[u],v[t]; r1=rough(t-1,u+2)
            if r1<r0-1e-9: ch+=1
            else: v[t],v[u]=v[u],v[t]
    swaps+=ch
    if not ch: break
print('swaps',swaps)
S['v']=v; json.dump(S,open('/tmp/claude-0/s122/mk/m02/scratch/series.json','w'))
