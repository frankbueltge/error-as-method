import json, math
occ=json.load(open('occ.json'))
x0,x1=2.0,298.0; D=61; w=(x1-x0)/D
TH=0.9
M=[]
for d in range(D):
    a=x0+d*w; b=a+w
    row=[]
    for k in range(18):
        cov=0;tot=0
        for x in range(int(a),int(math.ceil(b))):
            f=min(b,x+1)-max(a,x)
            if f<=0: continue
            tot+=f
            if occ[x][k]>TH: cov+=f*min(1,occ[x][k]/2.0)
        row.append(round(cov/tot,2))
    M.append(row)
json.dump(M,open('days.json','w'))
for k in range(17,-1,-1):
    print('%2d '%k+''.join(' ' if M[d][k]<0.05 else ('.' if M[d][k]<0.3 else ('o' if M[d][k]<0.6 else '#')) for d in range(D)))
# diurnal amplitude in thirds via f=62 per window
