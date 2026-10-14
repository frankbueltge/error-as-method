from PIL import Image
import math, json, random, sys
im=Image.open('/tmp/claude-0/s124/mk/m08/work/record.jpg').convert('L'); p=im.load()
W,H=im.size
N=1464; X0=2.5; X1=297.3; DX=(X1-X0)/(N-1)
obs=[[max(0.0,(255-p[x,y])/255.0) for x in range(W)] for y in range(H)]
SIG=float(sys.argv[1]) if len(sys.argv)>1 else 0.7; PEAK=0.85; LAM=float(sys.argv[2]) if len(sys.argv)>2 else 0.02
xs=[X0+i*DX for i in range(N)]
# column stats
cm=[];lo=[];hi=[]
for x in range(W):
  w=[obs[y][x] for y in range(H)]; s=sum(w)
  cm.append(sum(y*v for y,v in enumerate(w))/s if s>0.5 else None)
  d=[y for y in range(H) if obs[y][x]>0.35]
  lo.append(min(d) if d else None); hi.append(max(d) if d else None)
def interp(arr,x):
  a=int(math.floor(x)); b=a+1; f=x-a
  va=arr[a] if 0<=a<W and arr[a] is not None else None
  vb=arr[b] if 0<=b<W and arr[b] is not None else None
  if va is None: return vb
  if vb is None: return va
  return va*(1-f)+vb*f
def smooth(arr,r):
  out=[]
  for x in range(W):
    v=[arr[k] for k in range(max(0,x-r),min(W,x+r+1)) if arr[k] is not None]
    out.append(sum(v)/len(v) if v else None)
  return out
sm=smooth(cm,3)
y=[]
for i in range(N):
  c=interp(sm,xs[i]); m=interp(cm,xs[i]); l=interp(smooth(lo,0),xs[i]) if False else None
  y.append(c+2.0*(m-c))
# model as accumulated "absorbance": ink = 1-prod(1-a)
R=3
def kern(xc,yc):
  out=[]
  for yy in range(max(0,int(yc)-R),min(H,int(yc)+R+1)):
    for xx in range(max(0,int(xc)-R),min(W,int(xc)+R+1)):
      a=PEAK*math.exp(-((xx-xc)**2+(yy-yc)**2)/(2*SIG*SIG))
      if a>1e-3: out.append((yy,xx,a))
  return out
T=[[0.0]*W for _ in range(H)]  # sum of -log(1-a)
def add(i,sgn):
  for yy,xx,a in kern(xs[i],y[i]): T[yy][xx]+=sgn*(-math.log(1-a))
for i in range(N): add(i,1)
def model(yy,xx): return 1-math.exp(-T[yy][xx])
def local_err(i,yc):
  # error in neighborhood of sample i
  e=0.0
  xc=xs[i]
  for yy in range(max(0,int(min(yc,y[i]))-R-1),min(H,int(max(yc,y[i]))+R+2)):
    for xx in range(max(0,int(xc)-R),min(W,int(xc)+R+1)):
      e+=(obs[yy][xx]-model(yy,xx))**2
  return e
def smoothpen(i,v):
  s=0.0
  for j in (i-1,i,i+1):
    if 1<=j<N-1:
      a=y[j-1] if j-1!=i else v; b=y[j] if j!=i else v; c=y[j+1] if j+1!=i else v
      s+=(a-2*b+c)**2
  return LAM*s
def total():
  e=sum((obs[yy][xx]-model(yy,xx))**2 for yy in range(H) for xx in range(W))
  s=sum((y[j-1]-2*y[j]+y[j+1])**2 for j in range(1,N-1))
  return e, s
print('init',total())
for it in range(int(sys.argv[3]) if len(sys.argv)>3 else 12):
  order=list(range(N)); random.shuffle(order); moved=0
  for i in order:
    cur=y[i]
    # evaluate candidates over full column range coarse in early its, local later
    if it<4: cands=[v*0.5 for v in range(14,160)]
    else: cands=[cur+d*0.25 for d in range(-12,13)]
    best=None
    add(i,-1)
    for v in cands:
      if v<4 or v>82: continue
      y[i]=v; add(i,1)
      # error only over union region - approximate by computing region around both cur and v
      e=0.0
      for yy in range(max(0,int(v)-R),min(H,int(v)+R+2)):
        for xx in range(max(0,int(xs[i])-R),min(W,int(xs[i])+R+2)):
          e+=(obs[yy][xx]-model(yy,xx))**2-(obs[yy][xx]-(1-math.exp(-(T[yy][xx]-sum0(yy,xx)))) )**2 if False else 0
      add(i,-1)
    # simpler exact: compute delta error = err_with - err_without over the dot footprint
    bestv=cur; beste=1e18
    for v in cands:
      if v<4 or v>82: continue
      ks=kern(xs[i],v); d=0.0
      for yy,xx,a in ks:
        t0=T[yy][xx]; m0=1-math.exp(-t0); m1=1-math.exp(-(t0-math.log(1-a)))
        d+=(obs[yy][xx]-m1)**2-(obs[yy][xx]-m0)**2
      d+=smoothpen(i,v)
      if d<beste: beste=d; bestv=v
    y[i]=bestv; add(i,1)
    if abs(bestv-cur)>0.1: moved+=1
  print(it,moved,total(),flush=True)
json.dump(y,open('y_fit.json','w'))
