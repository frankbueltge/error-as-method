from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m05/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
for x in range(W):
    ys=[y for y in range(H) if p[x,y]<140]
    print(x,len(ys),min(ys) if ys else -1,max(ys) if ys else -1, ''.join('#' if p[x,y]<140 else ('+' if p[x,y]<200 else '.') for y in range(H)))
