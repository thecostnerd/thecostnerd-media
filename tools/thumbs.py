"""Colourway thumbnails: specs (dark ink grid), paper (white), red, yellow. Same composition rules: max 4 words, one highlight, one object, Cent Specs mark."""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import art as A
FD = "/usr/share/fonts/opentype/inter/"; BLACK = FD + "InterDisplay-Black.otf"
INK = (22, 20, 18); CREAM = (244, 238, 226); YEL = (255, 222, 60); RED = (216, 38, 30); PAPER = (243, 238, 227)
PALS = {
 "paper": dict(bg=PAPER, fg=INK, hl=YEL, hlfg=INK, rule=(236, 231, 220), strike=RED, grid=False),
 "specs": dict(bg=(22, 21, 20), fg=CREAM, hl=YEL, hlfg=INK, rule=(40, 38, 36), strike=RED, grid=True),
 "red": dict(bg=RED, fg=(255, 250, 240), hl=YEL, hlfg=INK, rule=(196, 30, 24), strike=INK, grid=True),
 "yellow": dict(bg=(247, 196, 49), fg=INK, hl=RED, hlfg=(255, 250, 240), rule=(232, 180, 40), strike=RED, grid=True),
}
def F(p, s): return ImageFont.truetype(p, s)

def bg(W, H, P, seed=1):
    im = Image.new("RGB", (W, H), P["bg"])
    noise = Image.effect_noise((W, H), 18).convert("L")
    im = Image.blend(im, Image.merge("RGB", (noise,) * 3), 0.05)
    d = ImageDraw.Draw(im)
    if P["grid"]:
        for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=P["rule"], width=2)
        for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=P["rule"], width=2)
    else:
        for y in range(60, H, 46): d.line([(0, y), (W, y)], fill=P["rule"], width=1)
    return im

def highlight(im, box, color, seed):
    rnd = random.Random(seed); x0, y0, x1, y1 = box
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    d.polygon([(x0 - 14, y0 + rnd.randint(0, 10)), (x1 + 18, y0 + rnd.randint(-4, 8)), (x1 + 10, y1 + rnd.randint(-6, 6)), (x0 - 8, y1 + rnd.randint(-2, 10))], fill=color + (240,))
    im.paste(layer.filter(ImageFilter.GaussianBlur(1.2)), (0, 0), layer.filter(ImageFilter.GaussianBlur(1.2)))

def txt(im, P, xy, s, font, hl=False, seed=3, anchor=None):
    d = ImageDraw.Draw(im); bb = d.textbbox(xy, s, font=font)
    if hl: highlight(im, (bb[0], bb[1] + 6, bb[2], bb[3] + 6), P["hl"], seed)
    ImageDraw.Draw(im).text(xy, s, font=font, fill=P["hlfg"] if hl else P["fg"]); return bb

def mark(im, cx, cy, r=46, ring=INK):
    d = ImageDraw.Draw(im)
    d.ellipse([cx - r - 18, cy - r - 18, cx + r + 18, cy + r + 18], fill=RED, outline=ring, width=5)
    rr = r // 2
    for dx in (-rr - 6, rr + 6):
        d.ellipse([cx + dx - rr, cy - rr, cx + dx + rr, cy + rr], fill=PAPER, outline=INK, width=5)
        d.text((cx + dx, cy + 2), "¢", font=F(BLACK, int(rr * 1.2)), fill=INK, anchor="mm")

def strike(im, box, color, w=14):
    d = ImageDraw.Draw(im); x0, y0, x1, y1 = box; ym = (y0 + y1) // 2 + 8
    d.line([(x0 - 10, ym + 10), (x1 + 10, ym - 10)], fill=color, width=w)

def never_full_price(P, W=1280, H=720):
    im = bg(W, H, P); f = F(BLACK, 150)
    txt(im, P, (60, 110), "NEVER", f, hl=True, seed=4); txt(im, P, (60, 270), "FULL", f); txt(im, P, (60, 430), "PRICE", f)
    tag = A.price_tag(560, txt="£35", color=(255, 252, 244, 255), small="NOW", rot=-10); im.paste(tag, (690, 150), tag)
    d = ImageDraw.Draw(im); fw = F(BLACK, 92); bb = d.textbbox((770, 70), "WAS £70", font=fw); d.text((770, 70), "WAS £70", font=fw, fill=P["fg"]); strike(im, bb, P["strike"])
    mark(im, W - 100, H - 100, 56 if P is PALS["specs"] else 46, ring=P["fg"] if P["bg"] != PAPER else INK)
    return im

def two_percent(P, W=1280, H=720):
    im = bg(W, H, P)
    txt(im, P, (60, 40), "2%", F(BLACK, 380), hl=True, seed=6); txt(im, P, (70, 480), "REAL DEALS", F(BLACK, 100))
    dark = P["bg"] in (PALS["specs"]["bg"],)
    bag = A.bag(520, color=(216, 38, 30, 255) if dark else (22, 20, 18, 255)); im.paste(bag, (760, 110), bag)
    d = ImageDraw.Draw(im)
    for y, s in ((470, "BLACK"), (545, "FRIDAY")): d.text((1020, y), s, font=F(BLACK, 74), fill=CREAM, anchor="mm")
    mark(im, W - 90, 90, ring=P["fg"] if P["bg"] != PAPER else INK)
    return im

def cheaper_in_may(P, W=1280, H=720):
    im = bg(W, H, P)
    txt(im, P, (60, 120), "CHEAPER", F(BLACK, 140), seed=8); txt(im, P, (60, 290), "IN MAY", F(BLACK, 170), hl=True, seed=9)
    rc = A.receipt(600, rows=(("MAY", "£299"), ("OCT", "£500")), total=("SALE", "£350"), title="PRICE LOG"); im.paste(rc, (680, 60), rc)
    mark(im, 110, H - 100, ring=P["fg"] if P["bg"] != PAPER else INK)
    return im

def short(P, lines, hl_idx, obj, W=1080, H=1920, seed=5):
    im = bg(W, H, P); y = 260
    for i, (s, size) in enumerate(lines):
        f = F(BLACK, size); w = ImageDraw.Draw(im).textlength(s, font=f)
        txt(im, P, ((W - w) / 2, y), s, f, hl=(i in hl_idx), seed=seed + i); y += int(size * 1.12)
    im.paste(obj, ((W - obj.width) // 2, y + 40), obj)
    mark(im, W // 2, H - 220, 60, ring=P["fg"] if P["bg"] != PAPER else INK)
    return im

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for name, fn in (("never", never_full_price), ("2pct", two_percent), ("may", cheaper_in_may)):
        for pk in ("specs", "paper", "red"):
            fn(PALS[pk]).save(f"{out}/{name}-{pk}.png")
    LT = (255, 252, 244, 255)
    short(PALS["specs"], [("WAS £70", 170), ("FOR 3 DAYS", 150), ("ONLY", 150)], {1}, A.price_tag(760, txt="£35", color=LT, small="NOW")).save(f"{out}/teaser-specs.png")
    short(PALS["yellow"], [("CHEAPER", 170), ("IN MAY", 190), ("THAN ON", 150), ("BLACK FRIDAY", 130)], {1}, A.receipt(560, rows=(("MAY", "£299"), ("OCT", "£500")), total=("SALE", "£350"), title="PRICE LOG"), seed=13).save(f"{out}/promoA-yellow.png")
    short(PALS["red"], [("3 BLACK", 170), ("FRIDAY", 170), ("TRICKS", 190)], {2}, A.sale_sign(720, txt="SALE").convert("RGBA"), seed=11).save(f"{out}/promoB-red.png")
    print("ok")
