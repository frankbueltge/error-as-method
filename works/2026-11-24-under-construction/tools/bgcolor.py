"""Descriptive only (for the face, not scoring): a page's declared body colour and whether it tiles an image.
Returns (hex or None, has_image)."""
import re
from features import INJECT
NAMED = {"black": "#000000", "white": "#ffffff", "navy": "#000080", "blue": "#0000ff", "red": "#ff0000",
         "purple": "#800080", "maroon": "#800000", "green": "#008000", "yellow": "#ffff00", "silver": "#c0c0c0",
         "gray": "#808080", "grey": "#808080", "teal": "#008080", "aqua": "#00ffff", "pink": "#ffc0cb",
         "darkblue": "#00008b", "midnightblue": "#191970", "lightblue": "#add8e6", "lavender": "#e6e6fa"}
def bg(html):
    low = INJECT.sub("", html).lower()
    b = re.search(r'<body([^>]*)>', low); a = b.group(1) if b else ""
    img = bool(re.search(r'background\s*=', a)) or bool(re.search(r'background(?:-image)?\s*:\s*url', low))
    c = re.search(r'bgcolor\s*=\s*["\']?#?([0-9a-f]{6}|[a-z]+)', a)
    if not c:
        c = re.search(r'body\s*{[^}]*background(?:-color)?\s*:\s*#?([0-9a-f]{6}|[a-z]+)', low)
    col = None
    if c:
        v = c.group(1)
        col = "#" + v if re.fullmatch(r'[0-9a-f]{6}', v) else NAMED.get(v)
    return col, img
