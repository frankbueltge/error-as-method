import json, math
d=json.load(open('/tmp/claude-0/s122/mk/m09/scratch/series.json')); v=d['v']; N=len(v)
m=sum(v)/N; x=[a-m for a in v]
def amp(P):
  c=sum(x[i]*math.cos(2*math.pi*i/P) for i in range(N)); s=sum(x[i]*math.sin(2*math.pi*i/P) for i in range(N))
  return 2*math.hypot(c,s)/N
best=[]
P=6.0
while P<30:
  best.append((amp(P),P)); P+=0.01
best.sort(reverse=True)
print(best[:10])
for P in (12.0,12.42,12.66,12.0,23.93,24.0,25.82,24.84,6.21,8.0):
  print(P,round(amp(P),2))
# daily mean (25h running)
dm=[sum(v[i:i+25])/25 for i in range(0,N-25,24)]
print([round(a) for a in dm])
# daily range
print([round(max(v[d*24:d*24+25])-min(v[d*24:d*24+25])) for d in range(60)])
