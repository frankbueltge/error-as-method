from PIL import Image, ImageDraw
import math
cols=[[int(c) for c in r] for r in open('occ.txt').read().split(',')]
N=len(cols);D=61;K=18
im=Image.new('RGBA',(1100,800),(242,238,229,255)); dr=ImageDraw.Draw(im,'RGBA')
L,R,T,B=70,1030,70,650; px=(R-L)/D; py=(B-T)/(K-1); tw=px-4; th=9
for k in range(K):
    y=round(B-k*py); dr.line([(L-14,y),(R+14,y)],fill=(28,36,48,23))
w=N/D
for d in range(D):
    a=d*w;b=a+w;x0=L+d*px+2
    for k in range(K):
        yc=B-k*py
        for x in range(int(a),math.ceil(b)):
            lo=max(a,x);hi=min(b,x+1)
            if hi<=lo: continue
            v=cols[x][k]
            if v<3: continue
            al=min(1,.18+.82*(v-3)/5)
            sx=x0+(lo-a)/w*tw; ex=x0+(hi-a)/w*tw
            dr.rectangle([sx,yc-th/2,ex,yc+th/2],fill=(28,36,48,int(al*255)))
im.save('preview.png')
