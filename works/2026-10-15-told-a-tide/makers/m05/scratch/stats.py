import json,math
cols=json.load(open('cols.json'))
W=len(cols)
# group consecutive pixels into dots
def dots(r):
    g=[];cur=[]
    for y in r:
        if cur and y-cur[-1]>1: g.append(cur);cur=[]
        cur.append(y)
    if cur:g.append(cur)
    return g
top=[];bot=[];med=[];spread=[]
for r in cols:
    if not r: top.append(None);bot.append(None);med.append(None);continue
    top.append(min(r));bot.append(max(r));s=sorted(r);med.append(s[len(s)//2])
allys=[y for r in cols for y in r]
hist=[0]*90
for y in allys: hist[y]+=1
print('hist of y:'); 
for y in range(90): print(y,'#'*(hist[y]//3))
def pgram(series,name):
    xs=[(i,v) for i,v in enumerate(series) if v is not None]
    m=sum(v for _,v in xs)/len(xs)
    out=[]
    for P10 in range(20,1600):
        P=P10/10
        c=sum((v-m)*math.cos(2*math.pi*i/P) for i,v in xs);s=sum((v-m)*math.sin(2*math.pi*i/P) for i,v in xs)
        out.append((c*c+s*s,P))
    out.sort(reverse=True)
    print(name,[(round(p,1),round(a)) for a,p in out[:15]])
pgram(bot,'bottom');pgram(top,'top');pgram(med,'median')
pgram([b-t if b is not None else None for b,t in zip(bot,top)],'spread')
