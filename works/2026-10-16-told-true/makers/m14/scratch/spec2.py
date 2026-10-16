import json, math
c=json.load(open('cent.json'))
hpp=1463/295.0
t=[(i+2-2.5)*hpp for i in range(len(c))]
def fit(P,idx):
  a=sum(c[i]*math.cos(2*math.pi*t[i]/P) for i in idx); b=sum(c[i]*math.sin(2*math.pi*t[i]/P) for i in idx)
  n=len(idx); return 2*math.hypot(a,b)/n, math.degrees(math.atan2(b,a))
allidx=range(len(c))
for P in [168,84,56,120,240,328,24*14.77,24*13.66,24*27.3]:
  print('P %.0fh amp %.2f px'%(P,fit(P,allidx)[0]))
print('sliding 4-day windows, 24h amplitude (px) and phase(deg):')
w=int(96/hpp)
for s in range(0,len(c)-w,w//2):
  idx=range(s,s+w)
  m=sum(c[i] for i in idx)/w
  a,p=fit(24.0,idx); print('day %5.1f  mean %+.1f  amp %.2f  phase %4.0f'%(t[s]/24,m,a,p))
