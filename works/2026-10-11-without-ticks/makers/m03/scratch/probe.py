W,H=1100,500
d=open('img.raw','rb').read()
px=lambda x,y:d[y*W+x]
# rows: count of non-white pixels in x 85..1075
for y in range(H):
    c=sum(1 for x in range(85,1075) if px(x,y)<250)
    m=min(px(x,y) for x in range(85,1075))
    if c>500: print('row',y,c,m)
for x in range(W):
    c=sum(1 for y in range(10,460) if px(x,y)<250)
    if c>300: print('col',x,c)
# tick marks below axis
for y in range(445,470):
    print(y,''.join('#' if px(x,y)<200 else ('+' if px(x,y)<250 else '.') for x in range(60,200)))
