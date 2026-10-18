import json
d=open('rec.raw','rb').read();W,H=300,90
T=[[min(1.0,max(0.0,(255-d[y*W+x]-20)/190)) for x in range(W)] for y in range(H)]
C=[5.5,10.1,14.5,19.3,23.8,28.4,33,37.5,42.4,46.8,51.5,56,60.6,65.4,69.7,74.5,78.9,83.5]
N=1464; X0=3.0; X1=297.0
xc=[X0+i*(X1-X0)/(N-1) for i in range(N)]
def foot(i,L):
    cx=xc[i]; cy=C[L]+0.5; out=[]
    for x in range(int(cx-1)-1,int(cx+1)+1):
        ox=max(0,min(x+1,cx+1)-max(x,cx-1))
        if ox<=0 or x<0 or x>=W: continue
        for y in range(int(cy-1)-1,int(cy+1)+1):
            oy=max(0,min(y+1,cy+1)-max(y,cy-1))
            if oy>0: out.append((y,x,ox*oy))
    return out
S=[[0.0]*W for _ in range(H)]
def R(s): return min(1.0,s)
v=[]
for i in range(N):
    x=int(xc[i]); best=max(range(18),key=lambda L:sum(T[y][x] for y in (int(C[L]),int(C[L])+1)))
    v.append(best)
for i in range(N):
    for y,x,a in foot(i,v[i]): S[y][x]+=a
for sweep in range(8):
    changed=0
    for i in range(N):
        cur=v[i]
        for y,x,a in foot(i,cur): S[y][x]-=a
        bestL=None;bestE=None
        for L in range(max(0,cur-5),min(18,cur+6)):
            f=foot(i,L)
            # delta error from adding this dot
            e=0
            for y,x,a in f:
                e+=(R(S[y][x]+a)-T[y][x])**2-(R(S[y][x])-T[y][x])**2
            e+=0.02*(abs(L-v[i-1]) if i>0 else 0)+0.02*(abs(L-v[i+1]) if i<N-1 else 0)
            if bestE is None or e<bestE: bestE=e;bestL=L
        v[i]=bestL; changed+=bestL!=cur
        for y,x,a in foot(i,bestL): S[y][x]+=a
    err=sum((R(S[y][x])-T[y][x])**2 for y in range(H) for x in range(W))
    print('sweep',sweep,'changed',changed,'err',round(err,1))
lv=[17-L for L in v]
json.dump(lv,open('series.json','w'))
# write rendered image for comparison
open('render.pgm','wb').write(b'P5 300 90 255\n'+bytes(int(255-255*R(S[y][x])) for y in range(H) for x in range(W)))
