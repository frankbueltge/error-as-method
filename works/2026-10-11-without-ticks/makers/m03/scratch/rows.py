import json, math
dots=json.load(open('dots_px.json'))
rows={}
for x,y in dots:
    r=int(math.floor(y)); yr=min(14,max(0,int((x-80.0)/(1000/15))))
    rows.setdefault(r,[0]*15)[yr]+=1
lo,hi=min(rows),max(rows)
print(lo,hi,max(sum(v) for v in rows.values()))
data=[rows.get(r,[0]*15) for r in range(lo,hi+1)]
json.dump({'lo':lo,'hi':hi,'rows':data},open('rows.json','w'))
print(sum(map(sum,data)))
for r in range(lo,hi+1,8): print(r,sum(rows.get(r,[0])),rows.get(r))
