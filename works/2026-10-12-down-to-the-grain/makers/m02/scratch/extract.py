from PIL import Image
import json
im=Image.open('/tmp/claude-0/s122/mk/m02/work/record.jpg').convert('L')
W,H=im.size; px=im.load(); T=200
seen=set(); dots=[]
def kmeans(pts,w,k):
    pts_sorted=sorted(range(len(pts)),key=lambda i:(pts[i][0],pts[i][1]))
    cs=[pts[pts_sorted[int((j+.5)*len(pts)/k)]] for j in range(k)]
    cs=[(float(a),float(b)) for a,b in cs]
    for _ in range(20):
        g=[[] for _ in cs]
        for i,p in enumerate(pts):
            j=min(range(k),key=lambda j:(p[0]-cs[j][0])**2+(p[1]-cs[j][1])**2); g[j].append(i)
        cs=[(sum(pts[i][0]*w[i] for i in gi)/sum(w[i] for i in gi), sum(pts[i][1]*w[i] for i in gi)/sum(w[i] for i in gi)) if gi else cs[j] for j,gi in enumerate(g)]
    return cs
mass=[]
for x in range(W):
    for y in range(H):
        if px[x,y]<T and (x,y) not in seen:
            st=[(x,y)]; seen.add((x,y)); pts=[]
            while st:
                a,b=st.pop(); pts.append((a,b))
                for da in (-1,0,1):
                    for db in (-1,0,1):
                        c,d=a+da,b+db
                        if 0<=c<W and 0<=d<H and (c,d) not in seen and px[c,d]<T:
                            seen.add((c,d)); st.append((c,d))
            # include soft halo weights from neighbourhood for mass
            w=[255-px[a,b] for a,b in pts]
            mass.append(sum(w))
            k=max(1,round(len(pts)/4.0))
            if k==1:
                s=sum(w); dots.append((sum(a*q for (a,b),q in zip(pts,w))/s, sum(b*q for (a,b),q in zip(pts,w))/s))
            else:
                dots+=kmeans(pts,w,k)
dots.sort()
print(len(dots), dots[0], dots[-1])
xs=[d[0] for d in dots]; ys=[d[1] for d in dots]
print('y range',min(ys),max(ys))
json.dump(dots,open('/tmp/claude-0/s122/mk/m02/scratch/dots.json','w'))
