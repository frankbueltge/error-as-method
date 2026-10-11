import json, heapq, math
D=json.load(open('comps.json'))
A={(x,y):v for x,y,v in D['ink']}
R=1.3; S=8; Q=4  # quarter-pixel grid
KC={}
def kern(ox4,oy4):
    # offsets within pixel in quarter steps (0..3), centre = i+ (ox4+.5)/4
    key=(ox4,oy4)
    if key in KC: return KC[key]
    ox=(ox4+.5)/Q; oy=(oy4+.5)/Q; K=[]
    for i in range(-2,3):
        for j in range(-2,3):
            n=0
            for a in range(S):
                for b in range(S):
                    px=i+(a+.5)/S; py=j+(b+.5)/S
                    if (px-ox)**2+(py-oy)**2<=R*R: n+=1
            if n: K.append((i,j,n/S/S))
    KC[key]=K; return K
T={}  # transmittance
def M(p): return 1-T.get(p,1.0)
def gain(c):
    x,y,ox4,oy4=c; g=0
    for i,j,k in kern(ox4,oy4):
        p=(x+i,y+j); a=A.get(p,0.0); t=T.get(p,1.0)
        m=1-t; m2=1-t*(1-k)
        g+=(a-m)**2-(a-m2)**2
    return g
cands=set()
for (x,y) in A:
    if A[(x,y)]>0.25:
        for ox4 in range(Q):
            for oy4 in range(Q): cands.add((x,y,ox4,oy4))
print('cands',len(cands))
heap=[(-gain(c),0,c) for c in cands]; heapq.heapify(heap)
ver={}
dots=[]
import sys
STOP=float(sys.argv[1])
while heap:
    ng,v,c=heapq.heappop(heap)
    if ver.get((c[0],c[1]),0)!=v: continue
    if -ng<STOP: break
    # verify fresh
    gnow=gain(c)
    if abs(gnow+ng)>1e-9:
        heapq.heappush(heap,(-gnow,v,c)); continue
    dots.append(c)
    x,y,ox4,oy4=c
    for i,j,k in kern(ox4,oy4):
        p=(x+i,y+j); T[p]=T.get(p,1.0)*(1-k)
    for xx in range(x-4,x+5):
        for yy in range(y-4,y+5):
            if A.get((xx,yy),0)>0.25:
                nv=ver.get((xx,yy),0)+1; ver[(xx,yy)]=nv
                for a4 in range(Q):
                    for b4 in range(Q):
                        cc=(xx,yy,a4,b4); heapq.heappush(heap,(-gain(cc),nv,cc))
print('dots',len(dots))
res=sum((A.get(p,0)-M(p))**2 for p in set(A)|set(T))
print('residual',res)
out=[[x+(a+.5)/Q, y+(b+.5)/Q] for x,y,a,b in dots]
json.dump(out,open(sys.argv[2],"w"))
