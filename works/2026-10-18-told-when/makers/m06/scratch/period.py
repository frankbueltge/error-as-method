import math
d=open('rec.raw','rb').read();W,H=300,90
cen=[]
for x in range(W):
  w=[(255-d[y*W+x])**2 for y in range(H)]
  s=sum(w); cen.append(sum(y*w[y] for y in range(H))/s if s else None)
# fill none
for i in range(W):
  if cen[i] is None: cen[i]=cen[i-1]
# detrend with 15px running mean
k=15;det=[cen[i]-sum(cen[max(0,i-k):i+k+1])/len(cen[max(0,i-k):i+k+1]) for i in range(W)]
res=[]
for c10 in range(300,1000):
  cyc=c10/10  # cycles per record (61 days -> 1464h)
  f=cyc/W
  a=sum(det[i]*math.cos(2*math.pi*f*i) for i in range(W));b=sum(det[i]*math.sin(2*math.pi*f*i) for i in range(W))
  res.append((a*a+b*b,cyc))
res.sort(reverse=True)
for p,c in res[:8]: print('cycles %.1f period %.2f h power %.0f'%(c,1464/c,p))
# phase per 10-day window at 61 cycles
f=61/W
for s in range(0,300,50):
  a=sum(det[i]*math.cos(2*math.pi*f*i) for i in range(s,s+50));b=sum(det[i]*math.sin(2*math.pi*f*i) for i in range(s,s+50))
  ph=math.atan2(b,a)
  # centroid y small = high value; peak value time = phase of min y
  print('window',s, 'amp %.1f'%math.hypot(a,b),'high-value hour %.1f'%(((ph+math.pi)/(2*math.pi)*24)%24))
