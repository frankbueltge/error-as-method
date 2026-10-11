t=open('tpl.html').read().replace('__DATA__',open('data.txt').read())
open('/tmp/claude-0/s121/mk/m01/work/index.html','w').write(t)
