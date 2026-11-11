LINES = "./thecostnerd-bonus-bf-promo-lines.json"
def tag(txt, small=None, color=None, rot=-10, s=0.75, x=0.5, y=0.45):
    a = {"txt": txt, "rot": rot}
    if small: a["small"] = small
    if color: a["color"] = color
    return {"f": "price_tag", "s": s, "x": x, "y": y, "args": a}
def o(f, s=0.7, x=0.5, y=0.45, rot=0, **args):
    return {"f": f, "s": s, "x": x, "y": y, "rot": rot, "args": args}
LIGHT = [255, 252, 244, 255]

SCENES = [
 {"ids": [1, 1], "head": "Black Friday is tomorrow. Watch for…", "hl": ["tomorrow."], "bg": "red", "count": {"from": 0, "to": 3, "fmt": "{:.0f} TRICKS", "size": 200}},
 {"ids": [2, 2], "head": "1. The \"was\" price", "hl": ["\"was\""], "art": [tag("£50", "WAS", LIGHT, s=0.8)]},
 {"ids": [3, 3], "head": "\"Was £50\" lasted 13 days in 6 months", "hl": ["13", "days"], "bg": "cream", "art": [o("calendar", 0.65, top="DAYS AT £50", big="13")], "src": "Source: Which? (UK), 2024"},
 {"ids": [4, 4], "head": "2. The deal that never ends", "hl": ["never"], "art": [o("countdown", 0.85)]},
 {"ids": [5, 5], "head": "Same price on 70 days around the sale", "hl": ["70", "days"], "bg": "cream", "art": [o("stick_vacuum", 0.55, 0.3), o("calendar", 0.5, 0.72, top="SAME PRICE", big="70")]},
 {"ids": [6, 6], "head": "3. The special model", "hl": ["special"], "bg": "red", "art": [o("tv", 0.8, txt="BF")]},
 {"ids": [7, 7], "head": "New model number = no price history", "hl": ["no", "price", "history"], "art": [o("magnifier", 0.7, txt="???")]},
 {"ids": [8, 8], "head": "Full investigation on the channel now", "hl": ["now"], "bg": "yellow", "sub": "Tap the video link above", "art": [o("tv", 0.7, txt="▶")]},
]
END = {"end": ["THE COST NERD", "The price tag never tells the whole story", "@THECOSTNERD"], "hold": 1.5, "bg": "ink"}

SRT = {3: 'A sign said was £50, now £25. That £50 price lasted 13 days in 6 months.'}
