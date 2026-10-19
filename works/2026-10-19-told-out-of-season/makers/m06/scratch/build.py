from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m06/work/record.jpg').convert('L');px=im.load()
pts=[]
for x in range(300):
    for y in range(90):
        d=255-px[x,y]
        if d>=48: pts+= [x,y,min(9,d//26)]
# daily range from the cols analysis
ranges=[]
for d in range(61):
    a=int(round(d*300/61)); b=int(round((d+1)*300/61))
    ys=[y for x in range(a,b) for y in range(90) if 255-px[x,y]>60]
    ranges.append(max(ys)-min(ys) if ys else 0)
html=open('template.html').read().replace('__PTS__',','.join(map(str,pts))).replace('__RNG__',','.join(map(str,ranges)))
open('/tmp/claude-0/s137/mk/m06/work/index.html','w').write(html)
print(len(pts)//3, ranges)
