d=open('/tmp/claude-0/s130/mk/m17/scratch/cols.json').read()
t=open('/tmp/claude-0/s130/mk/m17/scratch/template.html').read().replace('__DATA__',d)
open('/tmp/claude-0/s130/mk/m17/work/index.html','w').write(t)
