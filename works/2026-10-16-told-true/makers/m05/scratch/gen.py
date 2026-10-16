import base64
from PIL import Image
src='/tmp/claude-0/s130/mk/m05/work/record.jpg'
im=Image.open(src).convert('L')
raw=base64.b64encode(im.tobytes()).decode()
jpg=base64.b64encode(open(src,'rb').read()).decode()
tpl=open('/tmp/claude-0/s130/mk/m05/scratch/template.html').read()
out=tpl.replace('__RAW__',raw).replace('__JPG__',jpg)
open('/tmp/claude-0/s130/mk/m05/work/index.html','w').write(out)
print(len(out))
