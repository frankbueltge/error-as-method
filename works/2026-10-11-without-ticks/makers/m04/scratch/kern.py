import json
D=json.load(open('comps.json'))
ink={(x,y):v for x,y,v in D['ink']}
iso=[c for c in D['comps'] if 6<=len(c)<=12]
iso=[c for c in iso if 4.6<sum(ink[tuple(p)] for p in c)<6.0][:300]
def kernel(r,ox,oy,S=8):
    # dot centred at (ox,oy) in pixel coords where pixel (i,j) spans [i,i+1)
    K={}
    for i in range(int(ox-r)-1,int(ox+r)+2):
        for j in range(int(oy-r)-1,int(oy+r)+2):
            n=0
            for a in range(S):
                for b in range(S):
                    px=i+(a+.5)/S; py=j+(b+.5)/S
                    if (px-ox)**2+(py-oy)**2<=r*r: n+=1
            if n: K[(i,j)]=n/S/S
    return K
best=None
for r in [1.1,1.2,1.3,1.4,1.5,1.6]:
    err=0
    for c in iso[:120]:
        sx=sum(p[0]*ink[tuple(p)] for p in c);sy=sum(p[1]*ink[tuple(p)] for p in c);m=sum(ink[tuple(p)] for p in c)
        cx=sx/m+.5;cy=sy/m+.5
        K=kernel(r,cx,cy)
        keys=set(K)|set(tuple(p) for p in c)
        err+=sum((K.get(k,0)-ink.get(k,0))**2 for k in keys)
    print(r,err/120)
