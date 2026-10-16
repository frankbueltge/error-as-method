from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m02/work/record.jpg').convert('L')
W,H=im.size; print(W,H, im.mode)
p=im.load()
chars=" .:-=+*#%@"
for y in range(H):
    print(''.join(chars[min(9,(255-p[x,y])//26)] for x in range(W)))
