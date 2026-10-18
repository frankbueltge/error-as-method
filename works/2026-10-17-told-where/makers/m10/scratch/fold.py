import json
dots=json.load(open('dots.json'))
xs=sorted(x for x,y,v in dots)
print('xmin',xs[:3],'xmax',xs[-3:])
P=4.82071; n0=6.29415; pxh=P/24
span=1463*pxh
a=(xs[0]+xs[-1]-span)/2
print('a',a,'end',a+span, 'start solar hour', 12+(a-(n0-P))/pxh, 'end solar hour', 12+(a+span-(n0+60*P))/pxh)
rows={}
for x,y,v in dots:
  k=round((x-n0)/P)
  h=12+(x-(n0+k*P))/pxh
  val=max(0.0,(83.5-y)/81.0) if y<81.5 else 0.0
  rows.setdefault(k,[]).append((h,val,x,y))
out=[]
for k in range(-1,61):
  ds=sorted(rows.get(k,[]))
  lit=[(h,v) for h,v,_,_ in ds if v>0]
  hours=[0.0]*24
  if lit:
    c=sum(h for h,_ in lit)/len(lit)
    n=len(lit)
    start=round(c-(n-1)/2)
    # for partial days, anchor to edge rather than centre
    if k==-1: start=round(lit[0][0])

    for i,(h,v) in enumerate(lit):
      hh=start+i
      if 0<=hh<24: hours[hh]=max(hours[hh],v)
  out.append({'k':k,'raw':[(round(h,2),round(v,3)) for h,v,_,_ in ds],'hours':[round(v,3) for v in hours]})
for o in out:
  print(o['k'],''.join(' ' if v==0 else ' .:-=+*#%@'[min(9,int(v*10))] for v in o['hours']), round(sum(o['hours']),2))
json.dump(out,open('fold.json','w'))
# compact raw strip for provenance
json.dump([[round(x,1),round(y,1)] for x,y,v in dots],open('strip.json','w'))
