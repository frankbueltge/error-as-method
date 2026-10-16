from PIL import Image
import json
im=Image.open('/tmp/claude-0/s130/mk/m17/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
ink=[[max(0,(235-px[x,y]))/235 for y in range(H)] for x in range(W)]
tot=sum(sum(c) for c in ink); per=tot/1464
cols=[]; carry=0.0; n_all=0
for x in range(2,298):
    p=ink[x]; S=sum(p)
    exact=S/per+carry; n=max(0,round(exact)); carry=exact-n
    ys=[]
    if n:
        cum=0; k=0; targets=[(i+0.5)*S/n for i in range(n)]
        for y in range(H):
            prev=cum; cum+=p[y]
            while k<n and cum>=targets[k]:
                frac=(targets[k]-prev)/p[y] if p[y]>0 else 0.5
                ys.append(round(y-0.5+frac,1)); k+=1
    n_all+=len(ys); cols.append(ys)
print('dots',n_all)
json.dump(cols,open('cols.json','w'),separators=(',',':'))
