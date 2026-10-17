from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m02/work/record.jpg').convert('L')
w,h=im.size;px=im.load()
# darkness profile on baseline rows
prof=[ (255-px[x,83])+(255-px[x,84]) for x in range(w)]
# horizontal extent of left & right end dot centroids
def cen(xs):
    s=sum(prof[x] for x in xs); return sum(x*prof[x] for x in xs)/s
# find gaps: local light regions between x=1..298
gaps=[]
x=5
while x<298:
    if prof[x]<200:
        st=x
        while x<298 and prof[x]<200: x+=1
        # weighted center of lightness
        xs=range(st-1,x+1)
        wts=[max(0,510-prof[i]) for i in xs]
        gaps.append(sum(i*wv for i,wv in zip(xs,wts))/sum(wts))
    x+=1
print(len(gaps))
print([round(g,2) for g in gaps])
n=len(gaps)
import statistics
xs=list(range(n))
mx=statistics.mean(xs);my=statistics.mean(gaps)
sl=sum((a-mx)*(b-my) for a,b in zip(xs,gaps))/sum((a-mx)**2 for a in xs)
print('slope',sl,'int',my-sl*mx, 'b=',sl/24)
print('resid',[round(g-(my-sl*mx+sl*i),2) for i,g in enumerate(gaps)])
# leftmost/rightmost ink
for x in range(0,8): print(x,[px[x,y] for y in range(80,86)])
for x in range(292,300): print(x,[px[x,y] for y in range(80,86)])
