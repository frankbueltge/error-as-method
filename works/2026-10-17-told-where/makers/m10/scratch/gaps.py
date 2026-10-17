from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m10/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
base=[ 255-(p[x,83]+p[x,84])/2 for x in range(W)]
# light-weighted centers of gaps: find local minima regions
g=[]
x=0
while x<W:
    if base[x]<120:
        s=x
        while x<W and base[x]<120: x+=1
        e=x
        w=[255-base[i] for i in range(s,e)]
        g.append((sum(i*wi for i,wi in zip(range(s,e),w))/sum(w), e-s))
    x+=1
print(len(g)); print(g)
import statistics
cs=[c for c,_ in g if 2<c<295]
n=len(cs)
# linear fit index vs center
xs=list(range(n)); mx=sum(xs)/n; my=sum(cs)/n
b=sum((a-mx)*(c-my) for a,c in zip(xs,cs))/sum((a-mx)**2 for a in xs)
print('period',b,'intercept',my-b*mx)
print([round(c-(my-b*mx)-b*i,2) for i,c in enumerate(cs)])
