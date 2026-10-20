s=open('work/draw.js').read()
ex=open('work/extract_page.js').read()
html='''<!doctype html>
<html><head><meta charset="utf-8"><title>The Selborne Year</title>
<style>html,body{margin:0;background:#f2ece0}canvas{display:block;width:1100px;height:800px}</style>
</head><body><canvas id="c"></canvas>
<script src="data/selborne.js"></script>
<script>
'''+ex+'\n'+s+'''
</script></body></html>'''
open('index.html','w').write(html)
