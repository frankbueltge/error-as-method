from PIL import Image
import json
im=Image.open('/tmp/claude-0/s130/mk/m12/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
D=[[255-px[x,y] for y in range(H)] for x in range(W)]
cols=[x for x in range(W) if max(D[x])>110]
rws=[y for y in range(H) if max(D[x][y] for x in range(W))>110]
print('x extent',cols[0],cols[-1],'y extent',rws[0],rws[-1])
x0,x1=cols[0],cols[-1]
# candidates per column: local maxima of darkness (smoothed with neighbor cols)
cand={}
for x in range(W):
    s=[D[x][y]+0.5*((D[x-1][y] if x>0 else 0)+(D[x+1][y] if x<W-1 else 0)) for y in range(H)]
    c=[]
    for y in range(1,H-1):
        if s[y]>=s[y-1] and s[y]>=s[y+1] and D[x][y]>70:
            # subpixel
            a,b,cc=s[y-1],s[y],s[y+1]; den=a-2*b+cc
            off=0.5*(a-cc)/den if den!=0 else 0
            c.append((y+off,D[x][y]))
    cand[x]=c
N=1464
xs=[x0+0.5+i*(x1-x0-1)/(N-1) for i in range(N)]
states=[]
for i in range(N):
    xc=xs[i]; st=[]
    for x in (int(xc-0.5),int(xc+0.5)):
        for (y,d) in cand.get(x,[]):
            st.append((y,d))
    if not st: st=[(None,0)]
    states.append(st)
INF=1e18
cost=[ [ (300-d) *0.05 for (y,d) in states[0]] ]
back=[]
for i in range(1,N):
    cur=[];bk=[]
    for (y,d) in states[i]:
        best=INF;bj=0
        for j,(py,pd) in enumerate(states[i-1]):
            t=0 if (y is None or py is None) else (y-py)**2*0.15+abs(y-py)
            v=cost[-1][j]+t
            if v<best: best=v;bj=j
        cur.append(best+(300-d)*0.05 + (25 if y is None else 0)); bk.append(bj)
    cost.append(cur); back.append(bk)
j=min(range(len(cost[-1])),key=lambda k:cost[-1][k])
path=[j]
for i in range(N-1,0,-1):
    j=back[i-1][j]; path.append(j)
path.reverse()
ys=[states[i][path[i]][0] for i in range(N)]
# fill None by interpolation
for i in range(N):
    if ys[i] is None:
        a=i
        while a>=0 and ys[a] is None: a-=1
        b=i
        while b<N and ys[b] is None: b+=1
        ys[i]= ys[a] if b>=N else (ys[b] if a<0 else ys[a]+(ys[b]-ys[a])*(i-a)/(b-a))
v=[round(H-1-y,2) for y in ys]
json.dump(v,open('series.json','w'))
print(len(v),min(v),max(v))
