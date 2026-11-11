LINES = "./thecostnerd-bonus-bf-teaser-lines.json"
def tag(txt, small=None, color=None, rot=-10, s=0.75, x=0.5, y=0.45):
    a = {"txt": txt, "rot": rot}
    if small: a["small"] = small
    if color: a["color"] = color
    return {"f": "price_tag", "s": s, "x": x, "y": y, "args": a}
def o(f, s=0.7, x=0.5, y=0.45, rot=0, **args):
    return {"f": f, "s": s, "x": x, "y": y, "rot": rot, "args": args}
LIGHT = [255, 252, 244, 255]

SCENES = [
 {"ids": [1, 1], "head": "This said \"save £35\"", "hl": ["£35\""], "art": [o("toothbrush", 0.55, 0.3), tag("£35", "SAVE", LIGHT, s=0.5, x=0.7, y=0.55)]},
 {"ids": [2, 2], "head": "Was £70. Now £35.", "hl": ["£35."], "bg": "cream", "art": [tag("£35", "NOW", LIGHT, s=0.8)]},
 {"ids": [3, 3], "head": "In 6 months, it was £70 for…", "hl": ["£70"], "count": {"from": 0, "to": 3, "fmt": "{:.0f} DAYS", "size": 220}},
 {"ids": [4, 4], "head": "And it's not alone", "hl": ["not", "alone"], "bg": "red", "art": [o("sale_sign", 0.75)]},
 {"ids": [5, 5], "head": "Black Friday deals tracked", "hl": ["tracked"], "bg": "cream", "count": {"from": 0, "to": 208, "fmt": "{:.0f}", "dur": 1.1}},
 {"ids": [6, 6], "head": "Lowest price on the day", "hl": ["Lowest"], "count": {"from": 208, "to": 5, "fmt": "{:.0f}", "dur": 1.1}, "src": "Source: Which? (UK), 2022"},
 {"ids": [7, 7], "head": "So are Black Friday deals real?", "hl": ["real?"], "bg": "yellow", "art": [o("question", 0.7)]},
 {"ids": [8, 8], "end": ["FULL STORY", "Tomorrow on The Cost Nerd", "@THECOSTNERD"]},
]
END = None

SRT = {2: 'Was £70. Now £35.'}
