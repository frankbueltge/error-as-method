from PIL import Image, ImageDraw
M=[[int(c) for c in r] for r in open('days.txt').read().split(',')]
D=61;K=18
im=Image.new('RGBA',(1100,800),(242,238,229,255)); dr=ImageDraw.Draw(im,'RGBA')
L,R,T,B=70,1030,66,650; px=(R-L)/D; py=(B-T)/(K-1); tw=px-3.2; th=13
for k in range(K):
    y=round(B-k*py); dr.line([(L-16,y),(R+16,y)],fill=(28,36,48,19))
for d in range(D+1):
    x=round(L+d*px-1.6); dr.rectangle([x,B+26,x,B+26+(8 if d%7==0 else 3)],fill=(28,36,48,77))
for d in range(D):
    x=L+d*px+1.6
    for k in range(K):
        v=M[d][k]
        if v<1: continue
        al=min(1,.12+.88*(v/7)**1.1)
        dr.rectangle([x,B-k*py-th/2,x+tw,B-k*py+th/2],fill=(28,36,48,int(al*255)))
dr.text((70,728),"Eighteen Steps Down",fill=(28,36,48))
im.save('preview2.png')
