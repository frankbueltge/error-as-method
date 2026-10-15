import json, math
cols=json.load(open('cols.json'))[1:299]; H=90
# use centroid-of-darkness mean height per col
mean=[]
for c in cols:
  c=[v if v>40 else 0 for v in c]; s=sum(c)
  mean.append(sum((H-1-y)*v for y,v in enumerate(c))/s)
n=len(mean); mu=sum(mean)/n; s=[v-mu for v in mean]
hpp=1464/n
best=[]
for i in range(400):
  P=20+i*0.02  # hours
  f=hpp/P
  re=sum(s[j]*math.cos(2*math.pi*f*j) for j in range(n)); im=sum(s[j]*math.sin(2*math.pi*f*j) for j in range(n))
  best.append((re*re+im*im,P))
best.sort(reverse=True); print('best periods (h)',[(round(P,2),round(p)) for p,P in best[:6]])
# phase per ~10-day block at 24h
for b in range(6):
  lo,hi=b*n//6,(b+1)*n//6
  f=hpp/24
  re=sum(s[j]*math.cos(2*math.pi*f*j) for j in range(lo,hi)); im=sum(s[j]*math.sin(2*math.pi*f*j) for j in range(lo,hi))
  ph=math.atan2(-im,re)  # s ~ A cos(2pi f j + ph)
  # hour of max = -ph/(2pi f)*hpp mod 24
  hmax=(-ph/(2*math.pi))*24%24
  print('block',b,'amp',round(math.hypot(re,im)*2/(hi-lo),1),'hour-of-day of max (rel. to first sample)',round(hmax,1),'min',round((hmax+12)%24,1))
json.dump(mean,open('mean.json','w'))
