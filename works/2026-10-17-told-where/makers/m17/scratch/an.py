from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m17/work/record.jpg').convert('L');W,H=im.size
p=im.load()
# column darkness profile per row region
for y in range(80,90):
    print(y, ''.join('#' if p[x,y]<100 else ('+' if p[x,y]<180 else '.') for x in range(150,300)))
# bottom rows darkness sum per column
bot=[sum(255-p[x,y] for y in (84,85)) for x in range(W)]
print(bot)
# top-most dark pixel per column
top=[]
for x in range(W):
    t=None
    for y in range(H):
        if p[x,y]<140: t=y;break
    top.append(t)
print(top)
