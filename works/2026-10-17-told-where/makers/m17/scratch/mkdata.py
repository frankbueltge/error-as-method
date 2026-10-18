import json,math,statistics as st
B=json.load(open('blobs.json'))
P=4.821653; step=P/24; base=83.5; top=5.3
pts=[]
for b in B:
  if b['ymax']>=82 or b['mass']<150: continue
  k=max(1,round(b['mass']/330))
  pts.append((b['x'],(base-b['y'])/(base-top),k))
# phase via circular mean
sx=sum(v*k*math.cos(2*math.pi*x/P) for x,v,k in pts); sy=sum(v*k*math.sin(2*math.pi*x/P) for x,v,k in pts)
ph=(math.atan2(sy,sx)/(2*math.pi)*P)%P
print('noon phase px',ph)
days=[[] for _ in range(62)]
for x,v,k in pts:
  d=round((x-ph)/P); h=12+(x-ph-d*P)/step
  if 0<=d<62: days[d].append([round(h,2),round(v,3),k])
for L in days: L.sort()
spans=[];tots=[];mxs=[]
for d,L in enumerate(days):
  hs=[h for h,v,k in L]; tots.append(sum(v*k for h,v,k in L)); mxs.append(max(v for h,v,k in L))
  lo=min(hs);hi=max(hs);spans.append(hi-lo)
  print(d,round(lo,1),round(hi,1),round(tots[-1],2),round(mxs[-1],2))
for a,b in((0,20),(20,40),(40,61)):
  print(a,b,'span med',round(st.median(spans[a:b]),2),'tot',round(st.mean(tots[a:b]),2),'max top5',[round(m,2) for m in sorted(mxs[a:b])[-5:]])
json.dump(days,open('data.json','w'),separators=(',',':'))
days=[[p for p in L if 3.5<=p[0]<=20.5] for L in days]
json.dump(days,open('data.json','w'),separators=(',',':'))
