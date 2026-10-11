import pickle, math
W=1100
C,comps=pickle.load(open('cc.pkl','rb'))
A1=5.2624
for R in (2,3,4,6):
    tot=0; up=0
    for y in range(10,449):
        for x in range(81,1080):
            c=C[y*W+x]
            if c<=0: continue
            s=0;n=0
            for yy in range(max(10,y-R),min(449,y+R+1)):
                for xx in range(max(81,x-R),min(1080,x+R+1)):
                    s+=C[yy*W+xx]; n+=1
            cb=min(0.97,s/n)
            f=-math.log(1-cb)/cb if cb>1e-6 else 1
            m=c*f/A1; tot+=m
            if y<263: up+=m
    print(R,round(tot),round(up),round(tot-up))
