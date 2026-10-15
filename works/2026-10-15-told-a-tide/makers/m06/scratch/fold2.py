import json,math
c=json.load(open('peaks.json'))['colmean'];W=len(c)
k=7; r=[c[i]-sum(c[max(0,i-k):i+k+1])/len(c[max(0,i-k):i+k+1]) for i in range(W)]
for P in [4.80,4.85,4.88,4.918,4.95]:
  f=2*math.pi/P
  a=sum(r[i]*math.cos(f*i) for i in range(W)); b=sum(r[i]*math.sin(f*i) for i in range(W))
  # amplitude in first vs second half
  h=W//2
  a1=sum(r[i]*math.cos(f*i) for i in range(h)); b1=sum(r[i]*math.sin(f*i) for i in range(h))
  a2=sum(r[i]*math.cos(f*i) for i in range(h,W)); b2=sum(r[i]*math.sin(f*i) for i in range(h,W))
  print(P, round(math.hypot(a,b)), round(math.degrees(math.atan2(b1,a1))), round(math.degrees(math.atan2(b2,a2))))
# local maxima of r (low values=large y) positions
mx=[i for i in range(1,W-1) if r[i]>r[i-1] and r[i]>=r[i+1] and r[i]>2]
print(mx); import statistics; d=[b-a for a,b in zip(mx,mx[1:])]; print(d, statistics.mean(d))
