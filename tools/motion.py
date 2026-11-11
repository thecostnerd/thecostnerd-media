"""The Cost Nerd motion-graphics renderer (Episode 1-2 house style).
Dark charcoal stage, small red kicker, one hero graphic per beat, elements build in on narration cues.
Usage: python3 motion.py <episode.py> <voice_dir> <out_dir> [h|v]
Episode file: LINES, SCENES, optional CHAPTERS {first_id: title}, SRT {id: text}, BRAND_AFTER (scene index for logo sting), END.
Scene: {"ids":[a,b], "k":("KICKER","sub"), "src":"...", "ex":True (example prices), "els":[element,...]}
Element: {"t": type, "at": step (line index within scene, float ok), "d": delay s, "out": step to fade out, ...}
"""
import json, os, sys, math, subprocess, wave, importlib.util
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import art as A
import srtnum
from reel import music, write_wav

FPS = 30
BG = (19, 19, 20); GRIDC = (25, 25, 27); CREAM = (226, 221, 210); WHITE = (242, 238, 230); RED = (216, 38, 30); RED2 = (236, 74, 62)
CARD = (38, 38, 42); CARD2 = (54, 54, 59); GREY = (138, 135, 130); DIM = (70, 70, 74); YEL = (247, 196, 49)
FD = "/usr/share/fonts/opentype/inter/"
FONTS = {"black": FD + "InterDisplay-Black.otf", "xb": FD + "Inter-ExtraBold.otf", "bold": FD + "Inter-Bold.otf", "semi": FD + "Inter-SemiBold.otf",
         "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", "monob": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"}
_fc = {}


def F(name, size):
    k = (name, int(size))
    if k not in _fc: _fc[k] = ImageFont.truetype(FONTS[name], int(size))
    return _fc[k]


def C(name):
    return {"red": RED, "red2": RED2, "cream": CREAM, "white": WHITE, "grey": GREY, "dim": DIM, "card": CARD, "card2": CARD2, "yel": YEL, "bg": BG}.get(name, name) if isinstance(name, str) else tuple(name)


def mix(c, k):  # fade colour from background
    c = C(c); return tuple(int(BG[i] + (c[i] - BG[i]) * k) for i in range(3))


def eo(t): t = min(1, max(0, t)); return 1 - (1 - t) ** 3
def eob(t, s=1.6): t = min(1, max(0, t)); t -= 1; return t * t * ((s + 1) * t + s) + 1
def clamp(t): return min(1, max(0, t))


def spaced(d, xy, s, font, fill, sp=2, anchor="la"):
    """Letter-spaced text (for mono kickers)."""
    x, y = xy
    w = sum(d.textlength(ch, font=font) + sp for ch in s) - sp
    if anchor[0] == "m": x -= w / 2
    elif anchor[0] == "r": x -= w
    for ch in s:
        d.text((x, y), ch, font=font, fill=fill, anchor="l" + anchor[1]); x += d.textlength(ch, font=font) + sp
    return w


_bg = {}


def stage(W, H):
    if (W, H) not in _bg:
        im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
        for x in range(0, W, 48): d.line([(x, 0), (x, H)], fill=GRIDC, width=1)
        for y in range(0, H, 48): d.line([(0, y), (W, y)], fill=GRIDC, width=1)
        # vignette
        v = Image.new("L", (W, H), 0); dv = ImageDraw.Draw(v)
        for i in range(30):
            dv.rectangle([i * 6, i * 6, W - i * 6, H - i * 6], outline=int(60 - i * 2))
        im = Image.composite(Image.new("RGB", (W, H), (10, 10, 11)), im, v)
        _bg[(W, H)] = im
    return _bg[(W, H)]


_art = {}


def sprite(f, S, args):
    key = (f, S, json.dumps(args, sort_keys=True))
    if key not in _art:
        a = {k: (tuple(tuple(x) if isinstance(x, list) else x for x in v) if isinstance(v, list) else v) for k, v in args.items()}
        _art[key] = A.ART[f](S, **a)
    return _art[key]


def paste_alpha(img, spr, x, y, alpha=1.0):
    if alpha <= 0: return
    if alpha < 0.999:
        spr = spr.copy(); spr.putalpha(spr.getchannel("A").point(lambda v: int(v * alpha)))
    img.paste(spr, (int(x - spr.width / 2), int(y - spr.height / 2)), spr)


# ---------------- elements: draw(img, d, e, lt, fade) ; lt = seconds since appear ----------------

def el_text(img, d, e, lt, fa):
    k = eo(lt / 0.45) * fa
    if k <= 0: return
    y = e["y"] + 18 * (1 - eo(lt / 0.45))
    font = F(e.get("font", "bold"), e.get("size", 40))
    col = mix(e.get("color", "white"), k)
    if e.get("spaced"):
        spaced(d, (e["x"], y), e["txt"], font, col, e.get("sp", 3), e.get("anchor", "mm")); return
    if e.get("hl"):  # boxed highlight label
        bb = d.textbbox((e["x"], y), e["txt"], font=font, anchor=e.get("anchor", "mm"))
        pad = e.get("pad", 14)
        d.rounded_rectangle([bb[0] - pad, bb[1] - pad * 0.7, bb[2] + pad, bb[3] + pad * 0.7], radius=8, fill=mix(e["hl"], k))
    d.multiline_text((e["x"], y), e["txt"], font=font, fill=col, anchor=e.get("anchor", "mm"), align=e.get("align", "center"), spacing=e.get("spacing", 10))


def el_art(img, d, e, lt, fa):
    S = e.get("s", 400); spr = sprite(e["f"], S, e.get("args", {}))
    anim = e.get("anim", "pop"); x, y = e["x"], e["y"]; rot = e.get("rot", 0)
    k = clamp(lt / 0.5)
    if anim == "pop":
        sc = max(0.05, eob(k)); a = min(1, k * 3)
    elif anim == "rise":
        sc = 1; y += 60 * (1 - eo(k)); a = eo(k)
    elif anim == "drop":
        sc = 1; y -= 220 * (1 - eob(clamp(lt / 0.55), 1.2)); a = min(1, k * 4)
    elif anim == "slidel":
        sc = 1; x -= 300 * (1 - eo(k)); a = eo(k)
    elif anim == "slider":
        sc = 1; x += 300 * (1 - eo(k)); a = eo(k)
    elif anim == "swing":
        sc = 1; a = min(1, k * 4); rot += 28 * math.exp(-lt * 4.5) * math.cos(lt * 11)
    else:
        sc = 1; a = eo(k)
    if e.get("bob"): y += math.sin(lt * 2.2) * e["bob"]
    a *= fa
    s2 = spr
    if abs(sc - 1) > 0.01: s2 = s2.resize((max(1, int(S * sc)), max(1, int(S * sc))), Image.BILINEAR)
    if abs(rot) > 0.3: s2 = s2.rotate(rot, resample=Image.BICUBIC, expand=True)
    if e.get("xray") is not None:  # dim the sprite after xray step
        pass
    paste_alpha(img, s2, x, y, a)


def el_tag(img, d, e, lt, fa):
    """Price tag card (cream) that swings in: {x,y,txt,small,w}."""
    w = e.get("w", 220); h = int(w * 0.48)
    k = clamp(lt / 0.35)
    rot = e.get("rot", -8) + 30 * math.exp(-lt * 4) * math.cos(lt * 10)
    lay = Image.new("RGBA", (w + 60, h + 20), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    pts = [(30, 10), (w + 5, 10), (w + 5, h + 10), (30, h + 10), (5, h / 2 + 10)]
    ld.polygon(pts, fill=C(e.get("bg", "white")) + (255,))
    ld.ellipse([16, h / 2 + 4, 28, h / 2 + 16], fill=BG + (255,))
    big = F("black", h * (0.55 if not e.get("small") else 0.46))
    ld.text((w / 2 + 22, h / 2 + 10 - (h * 0.1 if e.get("small") else 0)), e["txt"], font=big, fill=C(e.get("fg", (24, 22, 20))) + (255,), anchor="mm")
    if e.get("small"): ld.text((w / 2 + 22, h * 0.82 + 10), e["small"], font=F("monob", h * 0.16), fill=(90, 86, 80, 255), anchor="mm")
    lay = lay.rotate(rot, resample=Image.BICUBIC, expand=True)
    paste_alpha(img, lay, e["x"], e["y"], min(1, k * 3) * fa)


def el_count(img, d, e, lt, fa):
    dur = e.get("dur", 1.1)
    k = eo((lt - 0.05) / dur)
    v = e["from"] + (e["to"] - e["from"]) * k
    a = clamp(lt / 0.25) * fa
    if a <= 0: return
    font = F(e.get("font", "black"), e.get("size", 200))
    d.text((e["x"], e["y"]), e["fmt"].format(v), font=font, fill=mix(e.get("color", "red2"), a), anchor=e.get("anchor", "mm"))
    if e.get("sub"):
        ks = clamp((lt - 0.4) / 0.4) * fa
        if ks > 0:
            fs = F(e.get("subfont", "semi"), e.get("subsize", 36))
            d.multiline_text((e["sx"] if "sx" in e else e["x"], e["y"] + e.get("size", 200) * 0.62), e["sub"], font=fs, fill=mix(e.get("subcolor", "white"), ks), anchor="ma" if e.get("anchor", "mm")[0] == "m" else e.get("anchor", "mm")[0] + "a", align="center" if e.get("anchor", "mm")[0] == "m" else "left", spacing=8)


def el_dots(img, d, e, lt, fa):
    n = e["n"]; cols = e.get("cols", 10); r = e.get("r", 12); gap = e.get("gap", 34)
    rows = math.ceil(n / cols)
    x0 = e["x"] - (cols - 1) * gap / 2; y0 = e["y"] - (rows - 1) * gap / 2
    hits = set(e.get("hit_idx", range(e.get("hit", 0))))
    special = {int(k): v for k, v in e.get("special", {}).items()}
    fill_dur = e.get("fill_dur", 1.2); base_dur = e.get("base_dur", 0.6)
    hit_order = sorted(hits)
    hit_rank = {h: i for i, h in enumerate(hit_order)}
    hit_delay = e.get("hit_delay", 0.6)
    shape = e.get("shape", "dot")
    for i in range(n):
        rr, cc = divmod(i, cols)
        cx, cy = x0 + cc * gap, y0 + rr * gap
        ka = clamp((lt - base_dur * i / n) / 0.25) * fa
        if ka <= 0: continue
        col = mix(DIM, ka)
        if i in hits:
            kh = clamp((lt - hit_delay - fill_dur * hit_rank[i] / max(1, len(hit_order))) / 0.2)
            if kh > 0: col = tuple(int(col[j] + (mix(e.get("hit_color", "red"), fa)[j] - col[j]) * kh) for j in range(3))
        if i in special:
            ks = clamp((lt - hit_delay - fill_dur) / 0.3)
            if ks > 0: col = mix(special[i], ks * fa)
        if shape == "sq":
            d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=max(2, r // 4), fill=col)
        else:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)


def el_bars(img, d, e, lt, fa):
    items = e["items"]; bw = e.get("bw", 170); gap = e.get("gap", 70); hmax = e.get("h", 420)
    vmax = e.get("vmax", max(it["v"] for it in items))
    total_w = len(items) * bw + (len(items) - 1) * gap
    x0 = e["x"] - total_w / 2; base = e["y"]
    ka = clamp(lt / 0.3) * fa
    d.line([(x0 - 40, base), (x0 + total_w + 40, base)], fill=mix(GREY, ka), width=3)
    tops = []
    for i, it in enumerate(items):
        st = e.get("stagger", 0.35) * i
        kb = eo((lt - 0.1 - st) / 0.7)
        h = hmax * it["v"] / vmax * kb
        bx = x0 + i * (bw + gap)
        col = C(it.get("color", "cream"))
        if kb > 0:
            d.rectangle([bx, base - h, bx + bw, base], fill=mix(col, fa))
        tops.append((bx, base - hmax * it["v"] / vmax))
        kl = clamp((lt - 0.1 - st) / 0.3) * fa
        if kl > 0:
            spaced(d, (bx + bw / 2, base + 24), it.get("label", ""), F("mono", 20), mix(it.get("lcolor", "grey"), kl), 2, "mt")
        kv = clamp((lt - 0.6 - st) / 0.3) * fa
        if kv > 0 and it.get("txt"):
            d.text((bx + bw / 2, base - hmax * it["v"] / vmax - 18), it["txt"], font=F("black", e.get("vsize", 56)), fill=mix(it.get("vcolor", "white" if it.get("color", "cream") != "red" else "red2"), kv), anchor="md")
    if e.get("delta"):
        dl = e["delta"]; kd = clamp((lt - dl.get("t", 1.6)) / 0.4) * fa
        if kd > 0:
            i0, i1 = dl.get("pair", (0, len(items) - 1))
            (ax, ay), (bx2, by) = tops[i0], tops[i1]
            xr = bx2 + bw + 30
            # dashed line from top of first to right
            xx = ax + bw
            while xx < xr:
                d.line([(xx, ay), (min(xx + 10, xr), ay)], fill=mix(GREY, kd), width=2); xx += 18
            d.line([(xr, by), (xr + 16, by), (xr + 16, ay), (xr, ay)], fill=mix(RED, kd), width=4)
            d.text((xr + 40, (ay + by) / 2 - 10), dl["txt"], font=F("black", dl.get("size", 84)), fill=mix(RED2, kd), anchor="lm")
            if dl.get("sub"): spaced(d, (xr + 44, (ay + by) / 2 + 42), dl["sub"], F("mono", 20), mix(WHITE, kd), 2, "lt")


def el_rows(img, d, e, lt, fa):
    x, y, w = e["x"], e["y"], e.get("w", 640); rh = e.get("rh", 56); pad = 26
    rows = e["rows"]; th = 60 if e.get("title") else 20
    H = th + len(rows) * (rh + 10) + pad
    if e.get("total"): H += rh + 30
    ka = eo(lt / 0.35) * fa
    if ka <= 0: return
    yo = 20 * (1 - eo(lt / 0.35))
    card = C(e.get("card", "card"))
    d.rounded_rectangle([x, y + yo, x + w, y + H + yo], radius=14, fill=mix(card, ka))
    if e.get("title"): spaced(d, (x + pad, y + 32 + yo), e["title"], F("mono", 19), mix(GREY, ka), 2, "lm")
    ry = y + th + yo
    for i, row in enumerate(rows):
        l, r = row[0], row[1]; flag = row[2] if len(row) > 2 else ""
        st = e.get("stagger", 0.22) * i + e.get("rows_delay", 0.25)
        kr = eo((lt - st) / 0.35) * fa
        if kr > 0:
            dx = -40 * (1 - kr)
            fill = mix(CARD2 if card == CARD else (214, 208, 196), kr)
            outline = mix(RED, kr) if flag == "red" else None
            d.rounded_rectangle([x + 16 + dx, ry, x + w - 16 + dx, ry + rh], radius=6, fill=fill, outline=outline, width=3 if outline else 0)
            tc = mix("white" if card == CARD else (24, 22, 20), kr)
            d.text((x + 36 + dx, ry + rh / 2), l, font=F("semi", e.get("fs", 26)), fill=mix(RED2, kr) if flag == "red" else tc, anchor="lm")
            d.text((x + w - 36 + dx, ry + rh / 2), r, font=F("monob", e.get("fs", 26)), fill=mix(RED2, kr) if flag in ("red", "redval") else tc, anchor="rm")
            if flag == "strike" or (row[3:] and row[3] is not None and lt > row[3]):
                ks = eo((lt - (row[3] if row[3:] and row[3] is not None else st + 0.4)) / 0.4)
                if ks > 0: d.line([(x + 30, ry + rh / 2), (x + 30 + (w - 60) * ks, ry + rh / 2)], fill=RED, width=4)
        ry += rh + 10
    if e.get("total"):
        kt = eo((lt - e.get("total_t", e.get("stagger", 0.22) * len(rows) + 0.5)) / 0.4) * fa
        if kt > 0:
            d.line([(x + 30, ry + 6), (x + w - 30, ry + 6)], fill=mix(GREY, kt), width=2)
            tl, tr = e["total"]
            tc = mix("white" if card == CARD else (24, 22, 20), kt)
            d.text((x + 36, ry + 20 + rh / 2), tl, font=F("xb", 32), fill=tc, anchor="lm")
            d.text((x + w - 36, ry + 20 + rh / 2), tr, font=F("black", 44), fill=mix(RED2, kt), anchor="rm")


def el_days(img, d, e, lt, fa):
    items = e["items"]; bw = e.get("w", 112); bh = e.get("h", 128); gap = e.get("gap", 18)
    tw = len(items) * bw + (len(items) - 1) * gap; x0 = e["x"] - tw / 2; y = e["y"] - bh / 2
    for i, it in enumerate(items):
        top, mid = it[0], it[1]; state = it[2] if len(it) > 2 else ""
        k = eo((lt - e.get("stagger", 0.12) * i) / 0.3) * fa
        if k <= 0: continue
        bx = x0 + i * (bw + gap); yo = 16 * (1 - k)
        hot = state == "red" and lt > e.get("stagger", 0.12) * i + e.get("hot_delay", 0.3)
        fill = mix(RED if hot else CARD2, k)
        d.rounded_rectangle([bx, y + yo, bx + bw, y + bh + yo], radius=10, fill=fill)
        spaced(d, (bx + bw / 2, y + 28 + yo), top, F("mono", 17), mix(WHITE if hot else GREY, k), 1, "mm")
        d.text((bx + bw / 2, y + bh * 0.62 + yo), mid, font=F("xb", e.get("fs", 30)), fill=mix(WHITE, k), anchor="mm")


def el_line(img, d, e, lt, fa):
    x, y, w, h = e["x"], e["y"], e["w"], e["h"]; pts = e["pts"]; labels = e.get("labels", [""] * len(pts))
    lo = e.get("lo", min(pts) * 0.8); hi = e.get("hi", max(pts) * 1.1); cur = e.get("cur", "£")
    X = lambda i: x + 60 + i * (w - 120) / max(1, len(pts) - 1); Y = lambda v: y + h - (v - lo) / (hi - lo) * h
    ka = clamp(lt / 0.3) * fa
    d.line([(x, y + h + 20), (x + w, y + h + 20)], fill=mix(GREY, ka), width=2)
    if e.get("ref"):
        rv = e["ref"]; kr = clamp((lt - e.get("ref_t", 0.2)) / 0.4) * fa
        if kr > 0:
            yy = Y(rv["v"]); xx = x
            while xx < x + w: d.line([(xx, yy), (min(xx + 12, x + w), yy)], fill=mix(GREY, kr), width=2); xx += 22
            spaced(d, (x + w + 14, yy), rv["txt"], F("mono", 18), mix(GREY, kr), 2, "lm")
    dur = e.get("dur", 1.6); kk = eo((lt - 0.2) / dur) * (len(pts) - 1)
    prev = None
    for i, v in enumerate(pts):
        if i > kk + 1e-6:
            if prev is not None and i - 1 < kk:
                f = kk - (i - 1); px, py = prev
                d.line([(px, py), (px + (X(i) - px) * f, py + (Y(v) - py) * f)], fill=mix(RED, fa), width=8)
            break
        if prev: d.line([prev, (X(i), Y(v))], fill=mix(RED, fa), width=8)
        prev = (X(i), Y(v))
    for i, v in enumerate(pts):
        kp = clamp((lt - 0.2 - dur * i / max(1, len(pts) - 1)) / 0.25) * fa
        if kp <= 0: continue
        r = 13; mk = e.get("mark") == i
        d.ellipse([X(i) - r, Y(v) - r, X(i) + r, Y(v) + r], fill=mix(YEL if mk else WHITE, kp), outline=mix(BG, kp), width=3)
        if not e.get("novals"): d.text((X(i), Y(v) - 30), f"{cur}{v}", font=F("black", e.get("vsize", 46)), fill=mix(RED2 if mk else WHITE, kp), anchor="md")
        if labels[i]: spaced(d, (X(i), y + h + 48), labels[i], F("mono", 20), mix(GREY, kp), 2, "mt")
    if e.get("mark") is not None:
        km = clamp((lt - 0.4 - dur) / 0.4) * fa
        if km > 0:
            i = e["mark"]; r = 34 + 6 * math.sin(lt * 4)
            d.ellipse([X(i) - r, Y(pts[i]) - r, X(i) + r, Y(pts[i]) + r], outline=mix(RED2, km), width=4)


def el_check(img, d, e, lt, fa):
    x, y, w = e["x"], e["y"], e.get("w", 520); items = e["items"]; rh = 54
    H = 100 + len(items) * rh
    ka = eo(lt / 0.35) * fa
    if ka <= 0: return
    yo = 20 * (1 - eo(lt / 0.35))
    cardc = (238, 233, 222) if e.get("light", True) else CARD
    ink = (24, 22, 20) if e.get("light", True) else WHITE
    d.rounded_rectangle([x, y + yo, x + w, y + H + yo], radius=8, fill=mix(cardc, ka))
    d.text((x + w / 2, y + 50 + yo), e["title"], font=F("xb", 36), fill=mix(ink, ka), anchor="mm")
    d.line([(x + 30, y + 80 + yo), (x + w - 30, y + 80 + yo)], fill=mix(ink, ka), width=3)
    for i, (mk, txt) in enumerate(items):
        k = eo((lt - e.get("items_delay", 0.4) - e.get("stagger", 0.35) * i) / 0.3) * fa
        if k <= 0: continue
        yy = y + 110 + i * rh + yo + 10
        col = RED if mk == "x" else (46, 150, 92)
        if mk == "x":
            d.line([(x + 34, yy - 10), (x + 54, yy + 10)], fill=mix(col, k), width=5); d.line([(x + 54, yy - 10), (x + 34, yy + 10)], fill=mix(col, k), width=5)
        else:
            d.line([(x + 32, yy), (x + 42, yy + 10), (x + 58, yy - 12)], fill=mix(col, k), width=5)
        d.text((x + 76, yy), txt, font=F("bold", 28), fill=mix(ink, k), anchor="lm")


def el_stamp(img, d, e, lt, fa):
    k = clamp(lt / 0.22)
    sc = 2.0 - 1.0 * eo(k)
    size = e.get("size", 64); txt = e["txt"]; col = C(e.get("color", "red"))
    f = F("black", int(size * sc))
    tw = d.textlength(txt, font=f); th = size * sc
    lay = Image.new("RGBA", (int(tw + 60 * sc), int(th + 50 * sc)), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([6, 6, lay.width - 6, lay.height - 6], radius=int(10 * sc), outline=col + (255,), width=max(3, int(6 * sc)))
    ld.text((lay.width / 2, lay.height / 2), txt, font=f, fill=col + (255,), anchor="mm")
    lay = lay.rotate(e.get("rot", 10), resample=Image.BICUBIC, expand=True)
    sx = (math.sin(lt * 60) * 6 * (1 - clamp((lt - 0.22) / 0.2))) if lt > 0.22 else 0
    paste_alpha(img, lay, e["x"] + sx, e["y"], min(1, k * 2) * fa)


def el_pill(img, d, e, lt, fa):
    k = eob(clamp(lt / 0.35)); a = clamp(lt / 0.2) * fa
    if a <= 0: return
    f = F(e.get("font", "bold"), e.get("size", 30)); tw = d.textlength(e["txt"], font=f)
    padx, pady = e.get("padx", 26), e.get("pady", 14)
    w2, h2 = (tw / 2 + padx) * k, (e.get("size", 30) / 2 + pady) * k
    st = e.get("style", "card")
    fill = {"card": CARD2, "red": RED, "cream": CREAM, "outline": None}[st]
    tcol = (24, 22, 20) if st == "cream" else WHITE
    d.rounded_rectangle([e["x"] - w2, e["y"] - h2, e["x"] + w2, e["y"] + h2], radius=int(min(h2, 30)) if e.get("round", True) else 8,
                        fill=mix(fill, a) if fill else None, outline=mix(GREY, a) if st == "outline" else None, width=2)
    if k > 0.6: d.text((e["x"], e["y"]), e["txt"], font=f, fill=mix(tcol, a), anchor="mm")


def el_cards(img, d, e, lt, fa):
    items = e["items"]; w = e.get("w", 200); h = e.get("h", 230); gap = e.get("gap", 22)
    tw = len(items) * w + (len(items) - 1) * gap; x0 = e["x"] - tw / 2; y = e["y"] - h / 2
    hl = e.get("hl")
    for i, (num, lab) in enumerate(items):
        k = eo((lt - e.get("stagger", 0.15) * i) / 0.35) * fa
        if k <= 0: continue
        bx = x0 + i * (w + gap); yo = 24 * (1 - k)
        dim = hl is not None and i != hl and lt > e.get("hl_t", 0.9)
        fill = RED if (hl == i and lt > e.get("hl_t", 0.9)) else CARD2
        kk = k * (0.45 if dim else 1)
        d.rounded_rectangle([bx, y + yo, bx + w, y + h + yo], radius=10, fill=mix(fill, k))
        d.text((bx + w / 2, y + h * 0.36 + yo), str(num), font=F("black", h * 0.34), fill=mix(WHITE if fill == RED else RED2, kk), anchor="mm")
        d.multiline_text((bx + w / 2, y + h * 0.72 + yo), lab, font=F("bold", e.get("fs", 24)), fill=mix(WHITE, kk), anchor="mm", align="center", spacing=6)


def el_title(img, d, e, lt, fa):
    y = e.get("y", 470); x = e.get("x", 960)
    k1 = eo(lt / 0.45) * fa
    if k1 > 0: d.text((x, y + 20 * (1 - eo(lt / 0.45))), e["txt"], font=F("xb", e.get("size", 80)), fill=mix(WHITE, k1), anchor="mm")
    if e.get("sub"):
        k2 = eo((lt - e.get("sub_t", 0.6)) / 0.4) * fa
        if k2 > 0: d.text((x, y + e.get("size", 80) * 0.95), e["sub"], font=F("bold", 42), fill=mix(RED2, k2), anchor="mm")
    if e.get("sub2"):
        k3 = eo((lt - e.get("sub2_t", 1.2)) / 0.4) * fa
        if k3 > 0: d.text((x, y + e.get("size", 80) * 0.95 + 64), e["sub2"], font=F("semi", 32), fill=mix(GREY, k3), anchor="mm")


def specs(d, cx, cy, r, k=1):
    if r < 6: return
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=mix(RED, k))
    rr = r * 0.36
    for dx in (-rr - r * 0.07, rr + r * 0.07):
        d.ellipse([cx + dx - rr, cy - rr, cx + dx + rr, cy + rr], fill=mix((244, 238, 226), k), outline=mix((24, 22, 20), k), width=max(2, int(r * 0.06)))
        d.text((cx + dx, cy + 2), "¢", font=F("black", int(rr * 1.25)), fill=mix((24, 22, 20), k), anchor="mm")
    d.rectangle([cx - r * 0.08, cy - r * 0.03, cx + r * 0.08, cy + r * 0.03], fill=mix((24, 22, 20), k))


def el_logo(img, d, e, lt, fa):
    k = eob(clamp(lt / 0.5)); a = clamp(lt / 0.3) * fa
    x, y, r = e.get("x", 760), e.get("y", 540), e.get("r", 150)
    if a <= 0: return
    # dashed ring
    rr = r * 1.35; ang = lt * 20
    for i in range(36):
        a0 = ang + i * 10
        d.arc([x - rr, y - rr, x + rr, y + rr], a0, a0 + 5, fill=mix(RED, a * 0.8), width=3)
    specs(d, x, y, r * k, a)
    k2 = eo((lt - 0.35) / 0.4) * fa
    if k2 > 0 and e.get("vertical"):
        spaced(d, (x, y + r * 1.75), "THE", F("monob", 26), mix(RED2, k2), 6, "mm")
        d.text((x, y + r * 1.75 + 70), "COST NERD", font=F("black", 110), fill=mix(WHITE, k2), anchor="mm")
        return
    if k2 > 0:
        tx = x + r * 1.8
        spaced(d, (tx, y - 70), "THE", F("monob", 26), mix(RED2, k2), 6, "lm")
        d.text((tx - 4, y), "COST NERD", font=F("black", 120), fill=mix(WHITE, k2), anchor="lm")
        if e.get("tag"): d.text((tx, y + 82), e["tag"], font=F("semi", 30), fill=mix(GREY, k2), anchor="lm")


def el_box(img, d, e, lt, fa):
    k = eo(lt / 0.4) * fa
    if k > 0: d.rounded_rectangle([e["x0"], e["y0"], e["x1"], e["y1"]], radius=14, outline=mix(DIM, k), width=3)


def el_strike(img, d, e, lt, fa):
    k = eo(lt / 0.3)
    if k > 0: d.line([(e["x0"], e["y0"]), (e["x0"] + (e["x1"] - e["x0"]) * k, e["y0"] + (e["y1"] - e["y0"]) * k)], fill=mix(e.get("color", "red"), fa), width=e.get("w", 10))


def el_arrow(img, d, e, lt, fa):
    k = eo(lt / 0.45) * 1
    if k <= 0: return
    x0, y0, x1, y1 = e["x0"], e["y0"], e["x0"] + (e["x1"] - e["x0"]) * k, e["y0"] + (e["y1"] - e["y0"]) * k
    col = mix(e.get("color", "red"), fa)
    d.line([(x0, y0), (x1, y1)], fill=col, width=e.get("w", 8))
    if k > 0.95:
        ang = math.atan2(y1 - y0, x1 - x0); L = 26
        for s in (-0.5, 0.5):
            d.line([(x1, y1), (x1 - L * math.cos(ang + s), y1 - L * math.sin(ang + s))], fill=col, width=e.get("w", 8))


def el_meter(img, d, e, lt, fa):
    """Horizontal bar: {x,y,w,h,frac,label,txt}"""
    x, y, w, h = e["x"], e["y"], e["w"], e.get("h", 46)
    ka = clamp(lt / 0.3) * fa
    if ka <= 0: return
    d.rectangle([x, y, x + w, y + h], fill=mix(CARD2, ka))
    kf = eo((lt - 0.2) / e.get("dur", 1.0))
    d.rectangle([x, y, x + w * e["frac"] * kf, y + h], fill=mix(e.get("color", "red"), fa))
    if e.get("label"): spaced(d, (x, y - 30), e["label"], F("mono", 19), mix(GREY, ka), 2, "lm")
    if e.get("txt"):
        kt = clamp((lt - 0.5) / 0.3) * fa
        if kt > 0: d.text((x + 18, y + h / 2), e["txt"], font=F("xb", 28), fill=mix(WHITE, kt), anchor="lm")


EL = {"text": el_text, "art": el_art, "tag": el_tag, "count": el_count, "dots": el_dots, "bars": el_bars, "rows": el_rows, "days": el_days,
      "line": el_line, "check": el_check, "stamp": el_stamp, "pill": el_pill, "cards": el_cards, "title": el_title, "logo": el_logo,
      "box": el_box, "strike": el_strike, "arrow": el_arrow, "meter": el_meter}
ANIM_LEN = {"count": 1.4, "dots": 3.2, "bars": 2.4, "rows": 2.8, "days": 2.2, "line": 2.6, "check": 2.4, "cards": 1.8, "title": 1.8, "logo": 99, "tag": 1.3, "stamp": 0.6}


def frame(sc, W, H, lt_scene, step_times):
    img = stage(W, H).copy(); d = ImageDraw.Draw(img)
    busy = False
    if sc.get("k"):
        k = eo(lt_scene / 0.4)
        ky, ks = (58, 20) if W > H else (250, 26)
        spaced(d, (64, ky), sc["k"][0], F("monob", ks), mix(RED2, k), 3, "lm")
        if len(sc["k"]) > 1 and sc["k"][1]: d.text((64, ky + ks * 1.5), sc["k"][1], font=F("mono", ks - 1), fill=mix(GREY, k), anchor="lm")
        busy |= lt_scene < 0.5
    if sc.get("src"):
        spaced(d, (64, H - (52 if W > H else 400)), "SOURCE · " + sc["src"].upper(), F("mono", 15), (96, 94, 90), 1, "lm")
    if sc.get("ex"):
        spaced(d, (W - 64, H - (52 if W > H else 400)), "EXAMPLE PRICES" if sc["ex"] is True else sc["ex"].upper(), F("mono", 15), (96, 94, 90), 1, "rm")
    els = sc.get("els", [])
    t0s = [step_times(e.get("at", 0)) + e.get("d", 0.15) for e in els]
    first = min(t0s) if t0s else 0
    for e, t0 in zip(els, t0s):
        if first > 0.5 and t0 - first < 0.05: t0 = 0.5  # never leave the stage empty for long
        lt = lt_scene - t0
        if lt < 0: continue
        fa = 1.0
        if e.get("out") is not None:
            to = step_times(e["out"]) + e.get("od", 0.0)
            if lt_scene >= to: fa = 1 - eo((lt_scene - to) / 0.35)
            if fa <= 0: continue
            if lt_scene - to < 0.4: busy = True
        if any(k.endswith("_at") for k in e):
            e = dict(e)
            for k, v in list(e.items()):
                if not k.endswith("_at"): continue
                sec = step_times(v) - t0
                if k == "dur_at": e["dur"] = max(0.4, sec - 0.2)
                elif k == "delta_at": e["delta"] = dict(e["delta"], t=sec)
                else: e[{"hit_at": "hit_delay", "sub_at": "sub_t", "sub2_at": "sub2_t", "hl_at": "hl_t", "total_at": "total_t", "ref_at": "ref_t"}[k]] = sec
        L = ANIM_LEN.get(e["t"], 1.0) + (e.get("dur", 0) if e["t"] in ("count", "line") else 0) + (len(e.get("rows", [])) * 0.25 if e["t"] == "rows" else 0)
        if e["t"] == "line" and e.get("mark") is not None: L = 99
        if e["t"] == "dots": L = max(L, e.get("hit_delay", 0.6) + e.get("fill_dur", 1.2) + 0.6)
        if e["t"] in ("title",): L = max(L, e.get("sub2_t", e.get("sub_t", 0.6)) + 0.6)
        if e["t"] == "rows": L = max(L, e.get("total_t", 0) + 0.6, e.get("stagger", 0.22) * len(e["rows"]) + e.get("rows_delay", 0.25) + 0.6)
        if e["t"] == "check": L = max(L, e.get("items_delay", 0.4) + e.get("stagger", 0.35) * len(e["items"]) + 0.4)
        if e["t"] == "cards": L = max(L, e.get("hl_t", 0) + 0.4, e.get("stagger", 0.15) * len(e["items"]) + 0.5)
        if e["t"] == "count" and e.get("sub"): L = max(L, 1.0)
        if e["t"] == "bars" and e.get("delta"): L = max(L, e["delta"].get("t", 1.6) + 0.6)
        if e.get("bob") or e.get("anim") == "swing": L = max(L, 99 if e.get("bob") else 1.4)
        if lt < L: busy = True
        EL[e["t"]](img, d, e, lt, fa)
    return img, busy


def load(path):
    spec = importlib.util.spec_from_file_location("ep", path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def read_wav(p):
    with wave.open(p) as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
    if ch == 2: a = a.reshape(-1, 2).mean(1)
    if sr != 48000:
        a = np.interp(np.arange(0, len(a), sr / 48000), np.arange(len(a)), a).astype(np.float32)
    nz = np.where(np.abs(a) > 0.008)[0]
    if len(nz): a = a[max(0, nz[0] - 960): nz[-1] + 3360]
    return a


def build(ep, voice_dir, out_dir, name, mode="h"):
    W, H = (1920, 1080) if mode == "h" else (1080, 1920)
    SR = 48000; os.makedirs(out_dir, exist_ok=True)
    texts = {l["id"]: l["text"] for l in json.load(open(ep.LINES))}
    chapters = getattr(ep, "CHAPTERS", {})
    GAP = getattr(ep, "GAP", 0.30); SCENE_GAP = getattr(ep, "SCENE_GAP", 0.25); CHAP_GAP = getattr(ep, "CHAP_GAP", 0.45)
    voice = [np.zeros(int(0.35 * SR))]; t = 0.35
    timeline = []; cues = []; chap_marks = []
    for si, sc in enumerate(ep.SCENES):
        if sc.get("brand"):  # silent logo sting
            dur = sc.get("dur", 2.2); voice.append(np.zeros(int(dur * SR)))
            timeline.append((t, t + dur, sc, [t])); t += dur; continue
        a, b = sc["ids"]; ids = [i for i in sorted(texts) if a <= i <= b]
        if ids[0] in chapters:
            if si > 0:
                voice.append(np.zeros(int(CHAP_GAP * SR))); t += CHAP_GAP
            chap_marks.append((t if si > 0 else 0.0, chapters[ids[0]]))
        s0 = t; starts = []
        for j, i in enumerate(ids):
            w = read_wav(os.path.join(voice_dir, f"line-{i:02d}.wav"))
            starts.append((t, len(w) / SR))
            cues.append((t, t + len(w) / SR, getattr(ep, "SRT", {}).get(i, srtnum.convert(texts[i])).replace("E U", "EU").replace("N Z", "NZ")))
            voice.append(w); t += len(w) / SR
            g = GAP if j < len(ids) - 1 else SCENE_GAP
            voice.append(np.zeros(int(g * SR))); t += g
        hold = sc.get("hold", 0)
        if hold: voice.append(np.zeros(int(hold * SR))); t += hold
        timeline.append((s0, t, sc, starts))
    end = getattr(ep, "END", None)
    if end:
        hold = end.get("hold", 14); voice.append(np.zeros(int(hold * SR)))
        timeline.append((t, t + hold, end, [(t, hold)])); t += hold
    total = t
    vo = np.concatenate(voice); vo = vo / max(1e-6, np.max(np.abs(vo))) * 0.9
    SRT_ONLY = bool(os.environ.get("SRT_ONLY"))
    if not SRT_ONLY:
        vpath = os.path.join(out_dir, f"{name}-voice.wav")
        with wave.open(vpath, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((vo * 32767).astype(np.int16).tobytes())
        mpath = os.path.join(out_dir, f"{name}-music.wav")
        write_wav(mpath, music(total, [0.0], seed=7, key=0))
        vid = os.path.join(out_dir, f"{name}-v.mp4")
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
        n = int(math.ceil(total * FPS)); ti = 0; cache = None; ckey = None
        for fi in range(n):
            tt = fi / FPS
            while ti < len(timeline) - 1 and tt >= timeline[ti][1]: ti += 1
            s0, s1, sc, starts = timeline[ti]
            def step_times(at, starts=starts, s0=s0):
                if not isinstance(starts[0], tuple): return 0
                i = int(math.floor(at)); f = at - i
                i = min(i, len(starts) - 1)
                return starts[i][0] - s0 + f * starts[i][1]
            lt = tt - s0
            if ti == 0 and mode == "v": lt += 2.5
            if ckey == ti and cache is not None and not _next_event_due(sc, lt, step_times):
                im = cache
            else:
                im, busy = frame(sc, W, H, lt, step_times)
                if not busy: cache, ckey = im, ti
                else: cache, ckey = None, None
            p.stdin.write(im.tobytes())
        p.stdin.close(); p.wait()
        final = os.path.join(out_dir, f"{name}.mp4")
        mvol = getattr(ep, "MUSIC_VOL", 0.09)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", vpath, "-i", mpath, "-filter_complex",
                        f"[2:a]aresample=48000,volume={mvol}[m];[1:a][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", final], check=True)
        for x in (vid, vpath, mpath): os.remove(x)
    def ts(x):
        h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
        return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)) % 1000:03d}"
    out = []; k = 1
    for a0, a1, txt in cues:
        # split into sentences / ~84-char chunks, timed by characters
        import re
        sents = re.split(r"(?<=[.?!])\s+", txt); parts = []
        for s in sents:
            while len(s) > 84:
                cut = s.rfind(", ", 0, 84); cut = cut + 1 if cut > 30 else s.rfind(" ", 0, 84)
                parts.append(s[:cut].strip()); s = s[cut:].strip()
            if s: parts.append(s)
        tot = sum(len(pp) for pp in parts); c0 = a0
        for pp in parts:
            c1 = c0 + (a1 - a0) * len(pp) / tot
            out.append(f"{k}\n{ts(c0)} --> {ts(c1)}\n{pp}\n"); k += 1; c0 = c1
    open(os.path.join(out_dir, f"{name}.srt"), "w").write("\n".join(out))
    mm = lambda x: f"{int(x // 60)}:{int(x % 60):02d}"
    json.dump({"total": total, "chapters": [(mm(a), b) for a, b in chap_marks]}, open(os.path.join(out_dir, f"{name}-meta.json"), "w"), indent=1)
    return total, chap_marks


def _next_event_due(sc, lt, step_times):
    """True if any element starts or fades out within this frame window (so the cache must be dropped)."""
    els = sc.get("els", [])
    t0s = [step_times(e.get("at", 0)) + e.get("d", 0.15) for e in els]
    first = min(t0s) if t0s else 0
    for e, t0 in zip(els, t0s):
        if first > 0.5 and t0 - first < 0.05: t0 = 0.5
        if t0 - 1 / FPS <= lt <= t0 + 1 / FPS or (lt >= t0 and lt - t0 < 0.05): return True
        if e.get("out") is not None:
            to = step_times(e["out"]) + e.get("od", 0.0)
            if to - 1 / FPS <= lt <= to + 0.45: return True
    return False


if __name__ == "__main__":
    ep = load(sys.argv[1]); mode = sys.argv[4] if len(sys.argv) > 4 else "h"
    name = os.path.splitext(os.path.basename(sys.argv[1]))[0]
    tot, ch = build(ep, sys.argv[2], sys.argv[3], name, mode)
    print(name, f"{tot:.1f}s", [(round(a, 1), b) for a, b in ch])
