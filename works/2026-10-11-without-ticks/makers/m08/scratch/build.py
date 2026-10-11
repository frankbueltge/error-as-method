data=open('data.txt').read().strip()
tpl=open('template.html').read()
open('/tmp/claude-0/s121/mk/m08/work/index.html','w').write(tpl.replace('__DATA__',data))
