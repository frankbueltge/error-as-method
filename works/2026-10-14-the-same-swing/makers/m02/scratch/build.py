from PIL import Image
im=Image.open('/tmp/claude-0/s124/mk/m02/work/record.jpg').convert('L');px=im.load()
pts=[(x,y,255-px[x,y]) for x in range(300) for y in range(90) if 255-px[x,y]>45]
flat=[]
for x,y,d in pts: flat+= [x,y,d]
data=','.join(map(str,flat))
html=open('template.html').read().replace('/*DATA*/',data)
open('/tmp/claude-0/s124/mk/m02/work/index.html','w').write(html)
print(len(html))
