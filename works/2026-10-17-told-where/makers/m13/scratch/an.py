from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m13/work/record.jpg').convert('L')
p=im.load()
floor=[255-min(p[x,83],p[x,84]) for x in range(300)]
print(''.join('#' if v>128 else ('+' if v>60 else '.') for v in floor))
# light (gap) columns in floor
gaps=[x for x in range(300) if floor[x]<100]
print(gaps)
# top dark pixel per col
top=[]
for x in range(300):
    t=None
    for y in range(0,83):
        if 255-p[x,y]>110: t=y;break
    top.append(t)
print(top)
