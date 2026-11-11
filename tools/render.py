"""Render The Cost Nerd Instagram slides (1080x1350 JPEG)."""
import os, sys, json
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
BG = (20, 20, 20)
GRID = (32, 32, 32)
CREAM = (244, 238, 226)
RED = (216, 38, 30)
GREY = (150, 146, 138)
INK = (24, 22, 20)
FD = "/usr/share/fonts/opentype/inter/"
BLACK = FD + "InterDisplay-Black.otf"
XB = FD + "Inter-ExtraBold.otf"
SB = FD + "Inter-SemiBold.otf"
MED = FD + "Inter-Medium.otf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONOB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
M = 84  # side margin


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, maxw):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(" "), ""
        for w in words:
            t = (cur + " " + w).strip()
            if draw.textlength(t, font=font) <= maxw:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def fit(draw, text, path, maxw, maxh, start, minsize=30, lh=1.08):
    s = start
    while s > minsize:
        f = F(path, s)
        lines = wrap(draw, text, f, maxw)
        if all(draw.textlength(l, font=f) <= maxw for l in lines) and len(lines) * s * lh <= maxh:
            return f, lines, s
        s -= 4
    f = F(path, minsize)
    return f, wrap(draw, text, f, maxw), minsize


def draw_lines(draw, xy, lines, font, size, fill, lh=1.08, hl=None, anchor_center=False):
    """hl: list of words/phrases to paint red."""
    x, y = xy
    for line in lines:
        if anchor_center:
            lx = (W - draw.textlength(line, font=font)) / 2
        else:
            lx = x
        if hl:
            # paint word by word, red if token matches any highlight token
            cx = lx
            for i, word in enumerate(line.split(" ")):
                token = word + (" " if i < len(line.split(" ")) - 1 else "")
                clean = word.strip(".,!?:;\"'()")
                col = RED if any(clean.upper() == h.upper() or word.upper() == h.upper() for h in hl) else fill
                draw.text((cx, y), token, font=font, fill=col)
                cx += draw.textlength(token, font=font)
        else:
            draw.text((lx, y), line, font=font, fill=fill)
        y += size * lh
    return y


def base(idx, total, last=False):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for gx in range(0, W, 54):
        d.line([(gx, 0), (gx, H)], fill=GRID, width=1)
    for gy in range(0, H, 54):
        d.line([(0, gy), (W, gy)], fill=GRID, width=1)
    # header
    d.rectangle([0, 0, W, 10], fill=RED)
    d.text((M, 50), "THE COST NERD", font=F(XB, 30), fill=CREAM)
    if total > 1:
        t = f"{idx}/{total}"
        f = F(XB, 30)
        d.text((W - M - d.textlength(t, font=f), 50), t, font=f, fill=RED)
    # footer
    d.text((M, H - 78), "@thecostnerd", font=F(SB, 28), fill=GREY)
    if total > 1 and not last:
        t = "SWIPE  →"
        f = F(XB, 28)
        d.text((W - M - d.textlength(t, font=f), H - 78), t, font=f, fill=CREAM)
    return img, d


def source(d, text):
    f = F(MED, 22)
    lines = wrap(d, (text if text.startswith("Example") else "Source: " + text), f, W - 2 * M)
    y = H - 130 - (len(lines) - 1) * 28
    for l in lines:
        d.text((M, y), l, font=f, fill=GREY)
        y += 28


def kicker(d, text, y=150):
    f = F(XB, 30)
    w = d.textlength(text, font=f)
    d.rectangle([M, y, M + w + 32, y + 52], fill=RED)
    d.text((M + 16, y + 9), text, font=f, fill=CREAM)
    return y + 52


def slide_hook(s, idx, total):
    img, d = base(idx, total)
    y = 190
    if s.get("kicker"):
        y = kicker(d, s["kicker"], 170) + 50
    f, lines, size = fit(d, s["title"], BLACK, W - 2 * M, 700, 132)
    y = draw_lines(d, (M, y), lines, f, size, CREAM, lh=1.04, hl=s.get("hl"))
    if s.get("sub"):
        y += 40
        d.rectangle([M, y, M + 120, y + 8], fill=RED)
        y += 40
        f2, l2, s2 = fit(d, s["sub"], SB, W - 2 * M, 260, 46)
        draw_lines(d, (M, y), l2, f2, s2, GREY, lh=1.25)
    return img, d


def slide_stat(s, idx, total):
    img, d = base(idx, total)
    y = 200
    if s.get("kicker"):
        y = kicker(d, s["kicker"], 170) + 60
    for st in s["stats"]:
        f, lines, size = fit(d, st["n"], BLACK, W - 2 * M, 300, st.get("size", 230))
        y = draw_lines(d, (M, y), lines, f, size, tuple(st.get("color_rgb", RED)), lh=1.0)
        y += 10
        f2, l2, s2 = fit(d, st["label"], SB, W - 2 * M, 200, 46)
        y = draw_lines(d, (M, y), l2, f2, s2, CREAM, lh=1.22)
        y += 60
    if s.get("body"):
        f3, l3, s3 = fit(d, s["body"], MED, W - 2 * M, H - 260 - y, 40)
        draw_lines(d, (M, y), l3, f3, s3, GREY, lh=1.3)
    if s.get("src"):
        source(d, s["src"])
    return img, d


def slide_text(s, idx, total, last=False):
    img, d = base(idx, total, last)
    y = 190
    if s.get("kicker"):
        y = kicker(d, s["kicker"], 170) + 60
    f, lines, size = fit(d, s["title"], BLACK, W - 2 * M, 430, 96)
    y = draw_lines(d, (M, y), lines, f, size, CREAM, lh=1.06, hl=s.get("hl"))
    y += 50
    if s.get("quote"):
        d.rectangle([M, y, M + 10, y + 10], fill=RED)
        fq, lq, sq = fit(d, s["quote"], XB, W - 2 * M - 40, 300, 54)
        d.rectangle([M, y, M + 10, y + len(lq) * sq * 1.2], fill=RED)
        y = draw_lines(d, (M + 40, y), lq, fq, sq, CREAM, lh=1.2)
        y += 20
        d.text((M + 40, y), s.get("attr", ""), font=F(SB, 30), fill=GREY)
        y += 80
    if s.get("bullets"):
        fb = F(SB, 40)
        for b in s["bullets"]:
            lb = wrap(d, b, fb, W - 2 * M - 60)
            d.rectangle([M, y + 14, M + 22, y + 36], fill=RED)
            y = draw_lines(d, (M + 50, y), lb, fb, 40, CREAM, lh=1.25)
            y += 28
    if s.get("body"):
        f3, l3, s3 = fit(d, s["body"], MED, W - 2 * M, H - 230 - y, 44)
        draw_lines(d, (M, y), l3, f3, s3, GREY, lh=1.32)
    if s.get("src"):
        source(d, s["src"])
    return img, d


def slide_receipt(s, idx, total):
    img, d = base(idx, total, last=(idx == total))
    y0 = 150
    if s.get("kicker"):
        y0 = kicker(d, s["kicker"], 150) + 40
    px0, px1 = 150, W - 150
    rows = s["rows"]
    rh = 66
    ph = 200 + len(rows) * rh + 210
    py1 = y0 + ph
    d.rectangle([px0, y0, px1, py1], fill=CREAM)
    # zigzag bottom edge
    zz = 24
    pts = []
    for x in range(px0, px1 + 1, zz):
        pts += [(x, py1), (x + zz / 2, py1 + 18)]
    d.polygon([(px0, py1)] + pts + [(px1, py1)], fill=CREAM)
    ft = F(MONOB, 40)
    t = s["title"]
    tl = wrap(d, t, ft, px1 - px0 - 80)
    y = y0 + 50
    for l in tl:
        d.text(((W - d.textlength(l, font=ft)) / 2, y), l, font=ft, fill=INK)
        y += 50
    y += 10
    d.text((px0 + 40, y), "-" * 34, font=F(MONO, 30), fill=GREY)
    y += 50
    fr = F(MONO, 32)
    frb = F(MONOB, 34)
    for r in rows:
        bold = r.get("bold")
        f = frb if bold else fr
        col = RED if r.get("red") else INK
        if r.get("rule"):
            d.text((px0 + 40, y), "-" * 34, font=F(MONO, 30), fill=GREY)
            y += rh
            continue
        d.text((px0 + 40, y), r["l"], font=f, fill=col)
        rv = r.get("r", "")
        d.text((px1 - 40 - d.textlength(rv, font=f), y), rv, font=f, fill=col)
        y += rh
    y += 20
    if s.get("foot"):
        ff = F(MONO, 26)
        for l in wrap(d, s["foot"], ff, px1 - px0 - 80):
            d.text(((W - d.textlength(l, font=ff)) / 2, y), l, font=ff, fill=GREY)
            y += 34
    if s.get("caption"):
        fc, lc, sc = fit(d, s["caption"], XB, W - 2 * M, 160, 44)
        draw_lines(d, (M, py1 + 60), lc, fc, sc, CREAM, lh=1.2, hl=s.get("hl"))
    if s.get("src"):
        source(d, s["src"])
    return img, d


def specs(d, cx, cy, r):
    """Simple 'Cent Specs' mark: two lenses with a cent sign."""
    for dx in (-r - 14, r + 14):
        d.ellipse([cx + dx - r, cy - r, cx + dx + r, cy + r], fill=CREAM, outline=INK, width=14)
        f = F(BLACK, int(r * 1.15))
        d.text((cx + dx, cy + 4), "¢", font=f, fill=INK, anchor="mm")
    d.rectangle([cx - 20, cy - 8, cx + 20, cy + 8], fill=INK)
    d.rectangle([cx - 14, cy - 18, cx + 14, cy + 18], fill=CREAM, outline=INK, width=4)


def slide_cta(s, idx, total):
    img, d = base(idx, total, last=True)
    cx, cy = W // 2, 400
    d.ellipse([cx - 230, cy - 230, cx + 230, cy + 230], fill=RED)
    specs(d, cx, cy + 10, 82)
    y = 700
    f = F(BLACK, 92)
    for l in ["FOLLOW", "@THECOSTNERD"]:
        d.text(((W - d.textlength(l, font=f)) / 2, y), l, font=f, fill=CREAM if l == "FOLLOW" else RED)
        y += 100
    y += 30
    f2 = F(SB, 40)
    t = "The price tag never tells the whole story."
    d.text(((W - d.textlength(t, font=f2)) / 2, y), t, font=f2, fill=GREY)
    y += 90
    if s.get("line"):
        f3, l3, s3 = fit(d, s["line"], XB, W - 2 * M, 140, 40)
        draw_lines(d, (M, y), l3, f3, s3, CREAM, lh=1.25, anchor_center=True)
    return img, d


def slide_quiz(s, idx, total):
    img, d = base(idx, total)
    y = 180
    f, tl, ts = fit(d, s["title"], BLACK, W - 2 * M, 140, 120)
    d.text((M, y), tl[0], font=f, fill=CREAM)
    y += 190
    bw = (W - 2 * M - 40) // 2
    for i, opt in enumerate(s["options"]):
        x0 = M + i * (bw + 40)
        d.rectangle([x0, y, x0 + bw, y + 620], fill=CREAM)
        d.rectangle([x0, y, x0 + bw, y + 110], fill=RED if i == 0 else INK)
        fl = F(BLACK, 76)
        d.text((x0 + bw / 2, y + 58), opt["k"], font=fl, fill=CREAM, anchor="mm")
        fn = F(XB, 44)
        yy = y + 170
        for l in wrap(d, opt["name"], fn, bw - 50):
            d.text((x0 + bw / 2, yy), l, font=fn, fill=INK, anchor="mm")
            yy += 54
        d.text((x0 + bw / 2, y + 380), opt["size"], font=F(BLACK, 80), fill=INK, anchor="mm")
        d.text((x0 + bw / 2, y + 520), opt["price"], font=F(BLACK, 110), fill=RED, anchor="mm")
    y += 680
    f2, l2, s2 = fit(d, s["sub"], XB, W - 2 * M, 120, 44)
    draw_lines(d, (M, y), l2, f2, s2, CREAM, lh=1.2)
    if s.get("src"):
        source(d, s["src"])
    return img, d


def slide_tag(s, idx, total):
    """Single cheat-card image: shelf tag anatomy."""
    img, d = base(idx, total, last=True)
    y = 150
    f, lines, size = fit(d, s["title"], BLACK, W - 2 * M, 300, 104)
    y = draw_lines(d, (M, y), lines, f, size, CREAM, lh=1.04, hl=s.get("hl"))
    y += 50
    tx0, tx1, ty0, ty1 = M, W - M, y, y + 380
    d.rectangle([tx0, ty0, tx1, ty1], fill=(250, 214, 60))
    d.text((tx0 + 40, ty0 + 30), "CORNFLAKES FAMILY SIZE 18 OZ", font=F(XB, 34), fill=INK)
    d.text((tx0 + 40, ty0 + 90), "$5.99", font=F(BLACK, 180), fill=INK)
    # unit price box
    ux0 = tx1 - 330
    d.rectangle([ux0, ty0 + 110, tx1 - 30, ty0 + 330], outline=RED, width=8)
    d.text((ux0 + 25, ty0 + 130), "UNIT PRICE", font=F(XB, 28), fill=INK)
    d.text((ux0 + 25, ty0 + 175), "33.3¢", font=F(BLACK, 84), fill=INK)
    d.text((ux0 + 25, ty0 + 275), "per ounce", font=F(SB, 30), fill=INK)
    y = ty1 + 40
    fl = F(XB, 36)
    d.text((tx0 + 40, y), "↑ BIG NUMBER: what you pay", font=fl, fill=GREY)
    t = "SMALL NUMBER: what it costs ↑"
    y2 = y + 50
    d.text((tx1 - d.textlength(t, font=fl), y2), t, font=fl, fill=RED)
    y = y2 + 90
    for b in s["bullets"]:
        fb = F(SB, 38)
        lb = wrap(d, b, fb, W - 2 * M - 50)
        d.rectangle([M, y + 14, M + 22, y + 36], fill=RED)
        y = draw_lines(d, (M + 50, y), lb, fb, 38, CREAM, lh=1.25)
        y += 22
    return img, d


R = {"hook": slide_hook, "stat": slide_stat, "text": slide_text, "receipt": slide_receipt,
     "cta": slide_cta, "quiz": slide_quiz, "tag": slide_tag}


def render(post, outdir):
    os.makedirs(outdir, exist_ok=True)
    slides = post["slides"]
    total = len(slides)
    paths = []
    for i, s in enumerate(slides, 1):
        fn = R[s["type"]]
        if s["type"] == "text":
            img, _ = fn(s, i, total, last=(i == total))
        else:
            img, _ = fn(s, i, total)
        name = "image.jpg" if total == 1 else f"slide-{i:02d}.jpg"
        p = os.path.join(outdir, name)
        img.save(p, "JPEG", quality=90, optimize=True)
        paths.append(p)
    return paths


if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))
    root = sys.argv[2]
    for post in data:
        out = os.path.join(root, post["path"])
        ps = render(post, out)
        print(post["path"], len(ps))
