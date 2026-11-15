"""Sun Nov 15, 2026 one-off: Starbucks' hidden Short size. IG Reel (hook A), IG trial Reel (hook B), TikTok (hook C)."""
import json, copy, re
def A(f, s=0.6, x=0.5, y=0.5, delay=None, **kw):
    d = dict(f=f, s=s, x=x, y=y)
    if kw: d["args"] = kw
    if delay is not None: d["delay"] = delay
    return d

SRC = "Sources: Harford/Slate 2006 · Starbucks 2025 · Business Insider · Reader's Digest"
HOOK_A = dict(bg="cream", head="Starbucks HIDES this size.", hl=["HIDES"], hsize=130,
    art=[A("coffee_cups", 0.7, 0.5, 0.5)],
    sub="8 oz. Not on the menu board.", dur=5,
    say="Starbucks has a size it won't show you.")
HOOK_B = dict(bg="ink", head="Ordered a Tall? Not the SMALL.", hl=["SMALL."], hsize=130,
    art=[A("coffee_cups", 0.7, 0.5, 0.5, hit=1)],
    sub="Starbucks' real small cup isn't on the board.", dur=5,
    say="Ordering a tall? That's not the small.")
HOOK_C = dict(bg="yellow", head="The smallest cup? NOT on the menu.", hl=["NOT"], hsize=124,
    art=[A("menu_board", 0.8, 0.5, 0.55, ghost="SHORT")],
    sub="Starbucks' 8 oz Short. You have to ask.", dur=5,
    say="Starbucks' smallest cup? It's not on the menu.")

BODY = [
 dict(bg="ink", head="Your 'small' is 12 OZ.", hl=["OZ."],
      art=[A("coffee_cups", 0.7, 0.5, 0.5, hidden=None, hit=1)],
      sub="Starbucks started with two sizes: an 8 oz Short and a 12 oz Tall.", dur=6,
      say="Tall is twelve ounces. The original small was an eight-ounce Short."),
 dict(bg="yellow", head="The Short still EXISTS.", hl=["EXISTS."],
      art=[A("coffee_cups", 0.7, 0.5, 0.5, hidden=None, hit=0)],
      sub="Starbucks even launched its 2025 cortado in Short (8 oz) only.", dur=5,
      say="It still exists. It's just not on the board."),
 dict(bg="red", head="Official reason: 'no ROOM.'", hl=["ROOM."],
      art=[A("menu_board", 0.8, 0.5, 0.55, ghost="SHORT")],
      sub="What Starbucks told economist Tim Harford (Slate, 2006).", dur=5,
      say="Starbucks' line? No room on the menu."),
 dict(bg="cream", head="Hide the CHEAP cup.", hl=["CHEAP"],
      art=[A("magnifier", 0.58, txt="8 oz")],
      sub="Harford: only price-hunters ask for it. Everyone else pays more.", dur=6,
      say="Economist Tim Harford's take: hide the cheap cup, and only price-hunters ask."),
 dict(bg="ink", head="Now GRANDE feels 'normal'.", hl=["GRANDE"],
      art=[A("menu_board", 0.8, 0.5, 0.55)],
      sub="With no small in sight, 16 oz looks like the safe middle.", dur=6,
      say="With no small in sight, the grande feels like the normal middle."),
 dict(bg="yellow", head="Twist: SAME shot as a Tall.", hl=["SAME"],
      art=[A("shots_compare", 0.7)],
      sub="Short and Tall lattes both get one espresso shot. The Tall just adds milk.", dur=7,
      say="Twist: a short latte gets the same espresso shot as a tall. The tall just adds milk."),
 dict(bg="red", head="Next time, say: 'SHORT, please.'", hl=["SHORT,"],
      art=[A("big_button", 0.62, txt="SHORT")],
      sub="Same coffee. Less milk. Lower price.", dur=5,
      say="Next coffee run, just say: short, please."),
 dict(bg="ink", cta=True, end="Save this + send it to the friend who always orders a Tall.", src=SRC,
      tt_end="Follow for Part 2: the Starbucks size that vanished.",
      say="Save this, and send it to the friend who always orders a tall.", tt_say="Follow for part two: the Starbucks size that vanished."),
]

def cut(slug, hook, tiktok=False):
    beats = [copy.deepcopy(hook)] + copy.deepcopy(BODY)
    cover = {k: v for k, v in hook.items() if k in ("bg", "head", "hl", "hsize", "art", "sub", "sticker")}
    r = dict(date="2026-11-15", slug=slug, cover=copy.deepcopy(cover), beats=beats)
    if tiktok:
        s = "STARBUCKS · PART 1"; r["cover"]["series"] = s
        for b in r["beats"]:
            b["series"] = s
            for a in b.get("art", []):
                a["x"] = round(min(a.get("x", 0.5), 0.62) * 0.94, 3); a["s"] = round(a["s"] * 0.9, 3)
            if b.get("end"): b["end"] = b["tt_end"]
        for a in r["cover"]["art"]: a["x"] = round(min(a.get("x", 0.5), 0.62) * 0.94, 3); a["s"] = round(a["s"] * 0.9, 3)
    for b in r["beats"]:
        for k in ("say", "tt_say", "tt_end"): b.pop(k, None)
    return r

cuts = [cut("starbucks-short-reel", HOOK_A), cut("starbucks-short-trial-hook-b", HOOK_B), cut("starbucks-short-tiktok", HOOK_C, True)]
json.dump(cuts, open("cuts.json", "w"), indent=1, ensure_ascii=False)
lines = [dict(id=10, chapter="hook-a-reel", text=HOOK_A["say"]), dict(id=20, chapter="hook-b-trial", text=HOOK_B["say"]),
         dict(id=30, chapter="hook-c-tiktok", text=HOOK_C["say"])]
for i, b in enumerate(BODY): lines.append(dict(id=100 + i * 10, chapter="body", text=b["say"]))
lines.append(dict(id=200, chapter="tiktok-end", text=BODY[-1]["tt_say"]))
json.dump(lines, open("thecostnerd-ig-starbucks-short-lines.json", "w"), indent=1, ensure_ascii=False)
for nm, h in (("A", HOOK_A), ("B", HOOK_B), ("C", HOOK_C)):
    print(nm, len(re.findall(r"[A-Za-z'-]+", h["say"] + " " + " ".join(b["say"] for b in BODY))), "words")
