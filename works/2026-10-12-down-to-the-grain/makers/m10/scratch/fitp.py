import sys, math, json, random
from PIL import Image
im=Image.open('../work/record.jpg').convert('L'); W,H=im.size; p=im.load()
D=[[max(0,255-p[x,y]-15)/240 for y in range(H)] for x in range(W)]
# smoothed darkness, subpixel sampler
def samp(x,y):
  x0=int(math.floor(x)); y0=int(math.floor(y)); fx=x-x0; fy=y-y0; s=0
  for dx,wx in ((0,1-fx),(1,fx)):
    for dy,wy in ((0,1-fy),(1,fy)):
      xx=x0+dx; yy=y0+dy
      if 0<=xx<W and 0<=yy<H: s+=wx*wy*D[xx][yy]
  return s
N=1464
X0=float(sys.argv[1]) if len(sys.argv)>1 else 2.6
X1=float(sys.argv[2]) if len(sys.argv)>2 else 296.3
xs=[X0+i*(X1-X0)/(N-1) for i in range(N)]
# blobs: dark pixel lists per column (y positions weighted)
PER={'M2':float(sys.argv[4]),'S2':12.0,'N2':12.65834751,'K2':11.96723606,'K1':23.93446966,'O1':25.81934171,'P1':24.06589,'M4':6.210300601,'MS4':6.103339,'M6':4.140200}
names=list(PER)
KN=12.0  # spline knot spacing hours
nk=int(math.ceil((N-1)/KN))+1
def basis(i):
  row=[]
  for n in names:
    w=2*math.pi*i/PER[n]; row+= [math.cos(w),math.sin(w)]
  # linear hat functions for slow level
  t=i/KN; k=int(t); f=t-k
  hb=[0.0]*nk; hb[k]+=1-f
  if k+1<nk: hb[k+1]+=f
  return row+hb
B=[basis(i) for i in range(N)]
P=len(B[0]); nh=2*len(names)
def solve(A,b):
  n=len(b); M=[A[r][:]+[b[r]] for r in range(n)]
  for c in range(n):
    piv=max(range(c,n),key=lambda r:abs(M[r][c])); M[c],M[piv]=M[piv],M[c]
    v=M[c][c]
    if abs(v)<1e-12: continue
    for r in range(n):
      if r!=c and M[r][c]!=0:
        f=M[r][c]/v; Mr=M[r]; Mc=M[c]
        for k in range(c,n+1): Mr[k]-=f*Mc[k]
  return [M[r][n]/M[r][r] if abs(M[r][r])>1e-12 else 0 for r in range(n)]
def lsq(targets,weights,lam_s=0.3,lam_h=1e-3):
  A=[[0.0]*P for _ in range(P)]; b=[0.0]*P
  for i in range(N):
    w=weights[i]
    if w<=0: continue
    r=B[i]; t=targets[i]
    nz=[j for j in range(P) if r[j]!=0]
    for j in nz:
      rj=r[j]*w; b[j]+=rj*t
      Aj=A[j]
      for k in nz: Aj[k]+=rj*r[k]
  for j in range(nh): A[j][j]+=lam_h
  # second-difference smoothness on level
  for k in range(1,nk-1):
    idx=[nh+k-1,nh+k,nh+k+1]; c=[1,-2,1]
    for a in range(3):
      for bb in range(3): A[idx[a]][idx[bb]]+=lam_s*c[a]*c[bb]
  for k in range(nk): A[nh+k][nh+k]+=1e-6
  return solve(A,b)
def pred(th): return [sum(a*b for a,b in zip(B[i],th)) for i in range(N)]
# column candidate y's: local maxima of darkness in column x (vertical), using the column pair
def cand(x):
  xi=int(round(x)); out=[]
  for xx in (xi-1,xi):
    if not 0<=xx<W: continue
    col=D[xx]
    for y in range(1,H-1):
      if col[y]>0.25 and col[y]>=col[y-1] and col[y]>=col[y+1]:
        # subpixel
        a,b_,c=col[y-1],col[y],col[y+1]; den=a-2*b_+c
        off=0.5*(a-c)/den if den<0 else 0
        out.append(y+off+0.5)
  return out
CAND=[cand(x) for x in xs]
def score(yp): return sum(samp(xs[i]-0.5,yp[i]-1.0) for i in range(N))/N
def em(th,iters=25,gate=8.0):
  for it in range(iters):
    yp=pred(th); tg=[];wt=[]
    for i in range(N):
      c=CAND[i]
      if not c: tg.append(yp[i]); wt.append(0); continue
      best=min(c,key=lambda v:abs(v-yp[i])); dd=abs(best-yp[i])
      tg.append(best); wt.append(1.0 if dd<gate else 0.2)
    th=lsq(tg,wt)
  return th
# initial: level from column means, then grid over M2 phase & amp
colmean=[]
for x in xs:
  xi=int(round(x)); col=D[xi]; tw=sum(col); colmean.append(sum(y*col[y] for y in range(H))/tw if tw else 64)
th0=lsq(colmean,[1]*N)
results=[]
random.seed(1)
trials=int(sys.argv[3]) if len(sys.argv)>3 else 24
for t in range(trials):
  th=th0[:]
  for j in range(nh): th[j]=0
  ph=2*math.pi*t/trials; th[0]=10*math.cos(ph); th[1]=10*math.sin(ph)
  # S2 in phase at springs near hour 734
  for n,a in (('S2',4),('N2',2)):
    j=2*names.index(n); w0=2*math.pi*734/PER['M2']; w1=2*math.pi*734/PER[n]
    phm=math.atan2(th[1],th[0])
    # want cos(w1-ph_s)=cos(w0-phm) => ph_s = phm + w1 - w0
    phs=phm+w1-w0; th[j]=a*math.cos(phs); th[j+1]=a*math.sin(phs)
  th=em(th,iters=12)
  s=score(pred(th)); results.append((s,t,th))
  print(t,round(s,4),file=sys.stderr)
results.sort(key=lambda r:-r[0])
best=results[0][2]; best=em(best,iters=30,gate=6)
yp=pred(best)
print('best score',score(yp),file=sys.stderr)
for k,n in enumerate(names):
  a=math.hypot(best[2*k],best[2*k+1]); print(n,round(a,2),round(math.degrees(math.atan2(best[2*k+1],best[2*k])),1),file=sys.stderr)

