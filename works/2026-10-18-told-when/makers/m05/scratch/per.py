import json,math
mean=json.load(open('mean.json'));W=300
def rm(x):
    v=[mean[k] for k in range(max(0,x-7),min(W,x+8)) if mean[k] is not None]; return sum(v)/len(v)
r=[(x,mean[x]-rm(x)) for x in range(W) if mean[x] is not None]
print('first/last col with data',r[0][0],r[-1][0])
for i in range(30):
    P=4.6+i*0.02
    c=sum(v*math.cos(2*math.pi*x/P) for x,v in r); s=sum(v*math.sin(2*math.pi*x/P) for x,v in r)
    print(round(P,2), round(math.hypot(c,s),1), round(math.degrees(math.atan2(s,c))))
