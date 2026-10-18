import math
d=open('rec.raw','rb').read();W,H=300,90
X0,X1=3.0,297.0
cen=[]
for x in range(W):
  w=[(255-d[y*W+x])**2 for y in range(H)];s=sum(w)
  cen.append(sum(y*w[y] for y in range(H))/s if s else None)
for i in range(W):
  if cen[i] is None: cen[i]=cen[i-1]
k=15;det=[cen[i]-sum(cen[max(0,i-k):i+k+1])/len(cen[max(0,i-k):i+k+1]) for i in range(W)]
hr=lambda x:(x-X0)/(X1-X0)*1463
best=[]
for p100 in range(2300,2550,2):
  P=p100/100
  a=sum(det[i]*math.cos(2*math.pi*hr(i)/P) for i in range(5,295));b=sum(det[i]*math.sin(2*math.pi*hr(i)/P) for i in range(5,295))
  best.append((a*a+b*b,P))
best.sort(reverse=True);print(best[:4])
for s in range(5,295,58):
  a=sum(det[i]*math.cos(2*math.pi*hr(i)/24) for i in range(s,s+58));b=sum(det[i]*math.sin(2*math.pi*hr(i)/24) for i in range(s,s+58))
  # det ~ A cos(wt - phi); min y (high value) at phase phi+pi
  phi=math.atan2(b,a); print('cols',s,'peak-value hour of day %.1f'%(((phi+math.pi)/(2*math.pi)*24)%24),'amp',round(math.hypot(a,b)))
