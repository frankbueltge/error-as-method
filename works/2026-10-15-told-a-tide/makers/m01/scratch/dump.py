from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m01/work/record.jpg').convert('L')
W,H=im.size; print(W,H)
p=im.load()
chars=' .:-=+*#%@'
for y in range(H):
    print(''.join(chars[min(9,(255-p[x,y])*10//256)] for x in range(W)))
