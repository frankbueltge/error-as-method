from PIL import Image
import math, json
im=Image.open('/tmp/claude-0/s130/mk/m03/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
N=1464; hp=N/W  # hours per px
# blob detection: local minima of gray below threshold
g=[[p[x,y] for x in range(W)] for y in range(H)]
pts=[]
for y in range(H):
  for x in range(W):
    v=g[y][x]
    if v>200: continue
    ok=True
    for dy in (-1,0,1):
      for dx in (-1,0,1):
        if (dx or dy) and 0<=y+dy<H and 0<=x+dx<W:
          u=g[y+dy][x+dx]
          if u<v or (u==v and (dy,dx)<(0,0)): ok=False
    if ok: pts.append((x,y,v))
print('blobs',len(pts))
# darkness mass total vs single dot mass estimate
mass=sum(max(0,230-g[y][x]) for y in range(H) for x in range(W))
print('mass',mass, 'mass/1464',mass/1464)
# subpixel centroid of each blob
cent=[]
for x,y,v in pts:
  sw=sx=sy=0
  for dy in (-1,0,1):
    for dx in (-1,0,1):
      X,Y=x+dx,y+dy
      if 0<=X<W and 0<=Y<H:
        w=max(0,230-g[Y][X]); sw+=w; sx+=X*w; sy+=Y*w
  cent.append((sx/sw,sy/sw,sw))
json.dump(cent,open('blobs.json','w'))
# least squares: y(x) ~ a + trend(spline by day) + diurnal harmonics; use blobs; hour t=(x+0.5)*hp
# Solve with normal equations: basis = day dummies (61) + cos/sin k=1..3
def basis(t):
  d=min(60,int(t//24)); b=[0.0]*61; b[d]=1.0
  for k in (1,2,3):
    b+= [math.cos(2*math.pi*k*t/24), math.sin(2*math.pi*k*t/24)]
  return b
rows=[(basis((cx+0.5)*hp), cy, w) for cx,cy,w in cent]
n=67
A=[[0.0]*n for _ in range(n)]; B=[0.0]*n
for b,yv,w in rows:
  for i in range(n):
    if b[i]==0: continue
    B[i]+=b[i]*yv
    for j in range(n): A[i][j]+=b[i]*b[j]
# gaussian elimination
M=[A[i]+[B[i]] for i in range(n)]
for i in range(n):
  piv=max(range(i,n),key=lambda r:abs(M[r][i])); M[i],M[piv]=M[piv],M[i]
  for r in range(n):
    if r!=i:
      f=M[r][i]/M[i][i]
      for c in range(i,n+1): M[r][c]-=f*M[i][c]
sol=[M[i][n]/M[i][i] for i in range(n)]
days=sol[:61]; harm=sol[61:]
prof=[sum(harm[2*(k-1)]*math.cos(2*math.pi*k*h/24)+harm[2*(k-1)+1]*math.sin(2*math.pi*k*h/24) for k in (1,2,3)) for h in range(24)]
print('diurnal profile (y px offset; negative=higher value), hour from record start:')
print([round(v,1) for v in prof])
print('daily level y:',[round(v,1) for v in days])
res=[yv-sum(bi*si for bi,si in zip(b,sol)) for b,yv,w in rows]
print('resid sd',(sum(r*r for r in res)/len(res))**.5)
# weekly check on daily levels
m=sum(days)/61; dd=[v-m for v in days]
for L in range(1,15): print(L, round(sum(dd[i]*dd[i+L] for i in range(61-L))/sum(v*v for v in dd),2), end='; ')
print()
# residual detrended daily levels weekly fold
sm=[sum(days[max(0,i-3):i+4])/len(days[max(0,i-3):i+4]) for i in range(61)]
wk=[[] for _ in range(7)]
for i in range(61): wk[i%7].append(days[i]-sm[i])
print('weekday fold',[round(sum(w)/len(w),2) for w in wk])
# amplitude of diurnal per day: fit per-day amplitude of fixed-shape profile
json.dump({'days':days,'prof':prof,'harm':harm},open('fit.json','w'))
