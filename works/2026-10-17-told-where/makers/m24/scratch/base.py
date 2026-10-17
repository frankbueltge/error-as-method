from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m24/work/record.jpg').convert('L')
w,h=im.size;p=im.load()
D=[[max(0,255-p[x,y])/255 for x in range(w)] for y in range(h)]
for y in range(78,88): print(y, ' '.join('%d'%int(D[y][x]*9) for x in range(0,60)))
base=[D[83][x]+D[84][x] for x in range(w)]
# cluster segmentation
cl=[];cur=None
for x in range(w):
    if base[x]>0.6:
        if cur is None: cur=[x,x]
        else: cur[1]=x
    else:
        if cur: cl.append(cur);cur=None
if cur: cl.append(cur)
print(len(cl))
cent=[]
for a,b in cl:
    s=sum(base[x] for x in range(a,b+1)); c=sum(x*base[x] for x in range(a,b+1))/s
    cent.append((c,b-a+1,s))
for i,c in enumerate(cent): print(i,'%.2f w=%d ink=%.2f'%c)
n=len(cent);xs=list(range(n));ys=[c[0] for c in cent]
mx=sum(xs)/n;my=sum(ys)/n
P=sum((a-mx)*(b-my) for a,b in zip(xs,ys))/sum((a-mx)**2 for a in xs)
print('period',P,'c0',my-P*mx)
print('resid',[round(ys[i]-(my-P*mx+P*i),2) for i in range(n)])
