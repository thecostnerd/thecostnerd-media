"""Community post images (1080x1080), house style: dark grid, 2-line headline with one yellow word, one visual, red footer + Cent Specs."""
import sys
sys.path.insert(0, '.')
import motion as M
import art as A
from PIL import Image, ImageDraw
W = H = 1080
YEL = (255, 210, 60); CREAM = (240, 236, 226); RED = (212, 36, 28); INK = (20, 20, 20)

def base(l1, l2, hl_line=2, size=170):
    im = M.stage(W, H).copy(); d = ImageDraw.Draw(im)
    for i, (t, y) in enumerate(((l1, 150), (l2, 285)), 1):
        s = size; f = M.F("black", s)
        while d.textlength(t, font=f) > W - 120: s -= 6; f = M.F("black", s)
        d.text((W / 2, y), t, font=f, fill=YEL if i == hl_line else CREAM, anchor="mm")
    return im, d

def footer(im, d, a, b):
    d.rectangle([0, 900, W, H], fill=RED)
    d.text((60, 965), a, font=M.F("xb", 48), fill=CREAM, anchor="lm")
    d.text((60, 1030), b, font=M.F("bold", 40), fill=(255, 222, 214), anchor="lm")
    cx, cy, r = 985, 990, 78
    d.ellipse([cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12], fill=INK)
    M.specs(d, cx, cy, r)

def tag(im, x, y, txt, small, w=230, rot=-6):
    d = ImageDraw.Draw(im)
    M.el_tag(im, d, {"txt": txt, "small": small, "x": x, "y": y, "w": w, "rot": rot}, 9, 1)

def post1():
    im, d = base("SPOT THE", "REAL DEAL")
    for x, lab, price, small in ((290, "A", "£299", "MAY"), (790, "B", "£350", "BLACK FRIDAY")):
        v = A.robot_vacuum(380); im.paste(v, (x - 190, 420), v)
        tag(im, x + 120, 450, price, small, rot=-6 if lab == "A" else 6)
        d.text((x, 840), lab, font=M.F("monob", 52), fill=CREAM, anchor="mm")
    s = A.sale_sign(170); im.paste(s, (870, 610), s)
    M.spaced(d, (W / 2, 880), "SOURCE · WHICH? (UK) PRICE TRACKING, 2024 SALE", M.F("mono", 14), (110, 108, 104), 1, "mm")
    footer(im, d, "Same vacuum. Two prices.", "Which one is the real deal?")
    return im

def post2():
    im, d = base("ONLY 5 OF 208", "WERE REAL", hl_line=1, size=150)
    hits = [17, 64, 103, 150, 190]; cols, gap, r = 26, 34, 12
    x0 = W / 2 - (cols - 1) * gap / 2; y0 = 440
    for i in range(208):
        rr, cc = divmod(i, cols); cx, cy = x0 + cc * gap, y0 + rr * gap
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED if i in hits else (70, 70, 74))
    M.spaced(d, (W / 2, 745), "208 BLACK FRIDAY DEALS · ● CHEAPEST ON THE DAY", M.F("monob", 20), (200, 196, 188), 2, "mm")
    d.text((W / 2, 810), "Poll answer: A. It was £299 in May.", font=M.F("bold", 38), fill=CREAM, anchor="mm")
    M.spaced(d, (W / 2, 875), "SOURCE · WHICH? (UK), BLACK FRIDAY 2022", M.F("mono", 14), (110, 108, 104), 1, "mm")
    footer(im, d, "About 2 in every 100.", "Your best deal: real or fake?")
    return im

if __name__ == "__main__":
    out = sys.argv[1]
    post1().save(f"{out}/community1.png"); post2().save(f"{out}/community2.png")
    a = Image.open(f"{out}/community1.png"); b = Image.open(f"{out}/community2.png")
    s = Image.new("RGB", (2160, 1080)); s.paste(a, (0, 0)); s.paste(b, (1080, 0)); s.resize((1440, 720)).save(f"{out}/community-both.png")
