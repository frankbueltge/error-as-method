import json
d=json.load(open('ink.json'));cols=d['cols'];dot=d['dot']
H=len(cols[0]);N=len(cols)
val=[17000-(i+21-19.5)*12000/430 for i in range(H)]
def wq(pairs,q):
    pairs=sorted(pairs);t=sum(w for _,w in pairs);a=0
    for v,w in pairs:
        a+=w
        if a>=q*t: return v
    return pairs[-1][0]
def km2(pairs):
    a,b=min(v for v,_ in pairs),max(v for v,_ in pairs)
    for _ in range(30):
        A=[(v,w) for v,w in pairs if abs(v-a)<=abs(v-b)];B=[(v,w) for v,w in pairs if abs(v-a)>abs(v-b)]
        if not A or not B: break
        a=sum(v*w for v,w in A)/sum(w for _,w in A);b=sum(v*w for v,w in B)/sum(w for _,w in B)
    return a,b,sum(w for _,w in A),sum(w for _,w in B)
R=4
out=[]
for x in range(N):
    up=[];lo=[]
    for xx in range(max(0,x-R),min(N,x+R+1)):
        for i in range(H):
            w=cols[xx][i]
            if w<=0.02: continue
            (up if val[i]>10100 else lo).append((val[i],w))
    sun,sat,ws,wsa=km2(lo)
    out.append(dict(x=x,wd=wq(up,.5),wd25=wq(up,.25),wd75=wq(up,.75),sat=sat,sun=sun,ws=ws,wsa=wsa))
json.dump(out,open('tiers.json','w'))
for o in out[::25]:
    print('%4d %6.0f %6.0f %6.0f  gap %5.0f  mass sun/sat %.2f'%(o['x'],o['wd'],o['sat'],o['sun'],o['sat']-o['sun'],o['ws']/o['wsa']))
