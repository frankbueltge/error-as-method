t=open('template.html').read()
r=open('render.js').read().split("if (typeof module")[0]
t=t.replace('__RENDER__',r).replace('__DATA__',open('ink.enc').read())
open('/tmp/claude-0/s121/mk/m07/work/index.html','w').write(t)
print(len(t))
