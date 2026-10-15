from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m07/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
s=''
for x in range(W):
    for y in range(H):
        d=max(0,232-px[x,y])/232
        q=min(15,int(round(d*15)))
        s+='0123456789abcdef'[q]
# run-length-ish: keep plain hex
open('ink.txt','w').write(s)
print(len(s), s.count('0'))
