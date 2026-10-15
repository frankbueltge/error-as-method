from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m03/work/record.jpg').convert('L');px=im.load()
pts=[]
for x in range(300):
    for y in range(90):
        d=255-px[x,y]
        if d>28: pts+= [x,y,d]
print(len(pts)//3,'pixels')
data=','.join(map(str,pts))
html=open('template.html').read().replace('/*DATA*/',data)
open('/tmp/claude-0/s128/mk/m03/work/index.html','w').write(html)
print(len(html),'bytes')
