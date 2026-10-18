import json
d=json.load(open('grid.json')); G=d['G']
X0,X1=2.5,297.5   # dot extent -> hours 0..1464
S=10              # samples per day
def val(x,l):
    i=int(x); f=x-i
    a=G[i][l] if 0<=i<300 else 0; b=G[i+1][l] if 0<=i+1<300 else 0
    return a*(1-f)+b*f
out=[]
for day in range(61):
    rows=[]
    for l in range(18):
        s=''
        for k in range(S):
            h=day*24+(k+0.5)*24/S
            x=X0+h/1464*(X1-X0)
            v=val(x,l)
            q=max(0,min(9,round((v-50)/150*9)))
            s+=str(q)
        rows.append(s)
    out.append(''.join(rows))
json.dump(out,open('days.json','w'))
for day in (0,20,45,60):
    print(day); [print(out[day][l*S:(l+1)*S]) for l in range(18)]
