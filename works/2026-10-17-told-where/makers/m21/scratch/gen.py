import json
d=json.load(open('dots2.json'))
X0=3.0; PXH=4.8225/24; Y0=83.8; YT=5.5
lit=[]
for x,y,w in d:
    if y>=81.6: continue
    if w<0.18: continue
    h=(x-X0)/PXH
    v=max(0,min(1,(Y0-y)/(Y0-YT)))
    lit.append([round(h,1),round(v,3),round(min(1,w*1.6),2)])
print(len(lit))
json.dump(lit,open('lit.json','w'),separators=(',',':'))
