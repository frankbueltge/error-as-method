"""Code one home page's HTML for the vernacular's markers. Fixed before any maker ran.

The twelve ICONIC markers are the signs the web's critics and collectors name for the amateur page:
Nielsen's 'Original Top 10 Mistakes in Web Design' (1996: frames, scrolling text/marquees, blink,
non-standard link colours) and Lialina's 'A Vernacular Web' (2005: under construction, starry
night background, MIDI, frames, welcome to my homepage, mail me, free collections of web elements)
and 'Ruins and Templates of Geocities' (counters, guestbooks, awards, webrings).
The PLAIN markers describe the page without judging it.
The gallery's injected sound script (first line of every restored page) is removed before coding.
"""
import re

INJECT = re.compile(r'<script src="/_assets/midi/bg-sound\.min\.js"></script><script>BgSound\.enableCompatMode\([^)]*\)</script>', re.I)


def lum(hexcol):
    m = re.fullmatch(r'#?([0-9a-fA-F]{6})', hexcol.strip().strip('"\''))
    if not m:
        names = {"black": 0, "navy": .05, "darkblue": .05, "midnightblue": .08, "purple": .2,
                 "maroon": .1, "darkgreen": .15, "darkred": .1, "indigo": .1, "white": 1,
                 "silver": .75, "gray": .5, "grey": .5}
        return names.get(hexcol.strip().strip('"\'').lower())
    v = m.group(1)
    r, g, b = (int(v[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def code(html):
    h = INJECT.sub("", html)
    low = h.lower()
    text = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', low, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&nbsp;|&[a-z]+;', ' ', text)
    words = re.findall(r"[a-z0-9']+", text)
    srcs = re.findall(r'(?:src|background|href)\s*=\s*["\']?([^"\' >]+)', low)
    body = re.search(r'<body([^>]*)>', low)
    battr = body.group(1) if body else ""
    bgimg = bool(re.search(r'background\s*=', battr)) or bool(re.search(r'background(?:-image)?\s*:\s*url', low))
    bgc = re.search(r'bgcolor\s*=\s*["\']?([#a-z0-9]+)', battr)
    bgl = lum(bgc.group(1)) if bgc else None
    css_bg = re.search(r'body\s*{[^}]*background(?:-color)?\s*:\s*(#[0-9a-f]{6}|[a-z]+)', low)
    if bgl is None and css_bg:
        bgl = lum(css_bg.group(1))
    gifs = [s for s in srcs if s.endswith('.gif')]
    iconic = {
        "under_construction": bool(re.search(r'construct', low)),
        "marquee": '<marquee' in low,
        "blink": '<blink' in low or 'text-decoration: blink' in low or 'text-decoration:blink' in low,
        "music": bool(re.search(r'<bgsound|\.mid\b|\.midi\b|\.wav\b', low)),
        "counter": bool(re.search(r'counter|you are visitor|visitors? since|visitor number|hits since|\bvisitor #', low)),
        "guestbook": 'guestbook' in low or 'guest book' in low,
        "webring": 'webring' in low or 'web ring' in low or re.search(r'ring[ _-]?(home|next|prev|id)', low) is not None,
        "award": bool(re.search(r'\baward', text)),
        "welcome_to_my": bool(re.search(r'welcome to (my|the|our)', text)),
        "best_viewed": 'best viewed' in text,
        "frames": '<frameset' in low,
        "dark_or_image_bg": bgimg or (bgl is not None and bgl < 0.3),
    }
    plain = {
        "words": len(words),
        "images": len(re.findall(r'<img\b', low)),
        "gif_images": len(gifs),
        "links": len(re.findall(r'<a\s[^>]*href', low)),
        "mailto": 'mailto:' in low,
        "center": '<center' in low or 'align="center"' in low or 'align=center' in low,
        "table": '<table' in low,
        "font_tag": '<font' in low,
        "comic_sans": 'comic sans' in low,
        "hr": '<hr' in low,
        "script": '<script' in low,
        "css": '<style' in low or 'style=' in low,
        "default_bg": (not bgimg) and (bgl is None or bgl >= 0.7),
        "last_updated": bool(re.search(r'(last )?updated', text)),
    }
    return {"iconic": iconic, "n_iconic": sum(iconic.values()), "plain": plain}
