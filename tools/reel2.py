"""Visual, illustration-led Reels and carousels for The Cost Nerd."""
import json, os, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import art as A
from reel import music, write_wav, BEAT

FPS = 30
FD = "/usr/share/fonts/opentype/inter/"
BLACK = FD + "InterDisplay-Black.otf"; XB = FD + "Inter-ExtraBold.otf"; SB = FD + "Inter-SemiBold.otf"
PAL = {
    "ink": {"bg": (22, 21, 20), "fg": (244, 238, 226), "hl": (247, 196, 49), "sub": (170, 164, 154), "grid": (36, 35, 33)},
    "red": {"bg": (216, 38, 30), "fg": (255, 250, 240), "hl": (24, 22, 20), "sub": (255, 214, 205), "grid": (200, 32, 26)},
    "cream": {"bg": (244, 238, 226), "fg": (24, 22, 20), "hl": (216, 38, 30), "sub": (108, 100, 90), "grid": (232, 224, 210)},
    "yellow": {"bg": (247, 196, 49), "fg": (24, 22, 20), "hl": (216, 38, 30), "sub": (90, 70, 20), "grid": (236, 184, 40)},
}
_d = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def F(p, s): return ImageFont.truetype(p, int(s))


def wrap(text, font, maxw):
    out, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if _d.textlength(t, font=font) <= maxw: cur = t
        else:
            if cur: out.append(cur)
            cur = w
    out.append(cur); return out


def fit(text, path, maxw, maxh, start, mn=36, lh=1.04):
    s = start
    while s > mn:
        f = F(path, s); ls = wrap(text, f, maxw)
        if all(_d.textlength(l, font=f) <= maxw for l in ls) and len(ls) * s * lh <= maxh: return f, ls, s
        s -= 4
    f = F(path, mn); return f, wrap(text, f, maxw), mn


def draw_rich(img, x, y, lines, font, size, fg, hl, hlwords, lh=1.04, center=False, W=1080, marker=True):
    d = ImageDraw.Draw(img)
    for line in lines:
        words = line.split(" ")
        lw = d.textlength(line, font=font)
        cx = (W - lw) / 2 if center else x
        for i, w in enumerate(words):
            tok = w + (" " if i < len(words) - 1 else "")
            clean = w.strip(".,!?:;“”\"'()…")
            is_hl = any(clean.lower() == h.strip(".,!?…").lower() for h in hlwords)
            ww = d.textlength(w, font=font)
            if is_hl and marker:
                d.rectangle([cx - 8, y + size * 0.12, cx + ww + 8, y + size * 1.02], fill=hl)
                col = fg if hl != fg else fg
                # text on marker: use bg-contrasting colour
                col = (24, 22, 20) if hl in [(247, 196, 49)] else (255, 250, 240)
                d.text((cx, y), w, font=font, fill=col)
            else:
                d.text((cx, y), w, font=font, fill=hl if is_hl else fg)
            cx += d.textlength(tok, font=font)
        y += size * lh
    return y


def ease_out_back(t, s=1.70158):
    t -= 1; return t * t * ((s + 1) * t + s) + 1


def ease(t): return 1 - (1 - t) ** 3


_art_cache = {}


def get_art(spec, W):
    key = json.dumps(spec, sort_keys=True) + str(W)
    if key not in _art_cache:
        S = int(spec.get("s", 0.6) * W)
        args = {a: (tuple(v) if isinstance(v, list) and a != "rows" else v) for a, v in spec.get("args", {}).items()}
        _art_cache[key] = A.ART[spec["f"]](S, **args)
    return _art_cache[key]


def grid_bg(W, H, pal, off=0):
    im = Image.new("RGB", (W, H), pal["bg"]); d = ImageDraw.Draw(im)
    step = 60
    for gx in range(-step + off % step, W, step): d.line([(gx, 0), (gx, H)], fill=pal["grid"], width=2)
    for gy in range(-step + off % step, H, step): d.line([(0, gy), (W, gy)], fill=pal["grid"], width=2)
    return im


def specs_mark(d, cx, cy, r, ink=(24, 22, 20), cream=(244, 238, 226)):
    for dx in (-r - 14, r + 14):
        d.ellipse([cx + dx - r, cy - r, cx + dx + r, cy + r], fill=cream, outline=ink, width=14)
        d.text((cx + dx, cy + 4), "¢", font=F(BLACK, int(r * 1.15)), fill=ink, anchor="mm")
    d.rectangle([cx - 20, cy - 8, cx + 20, cy + 8], fill=ink)


def frame(beat, W, H, lt, dur, mode="reel", prev_bg=None, page=None, total_pages=None):
    """Render one frame of a beat at local time lt (static final state if lt is None)."""
    static = lt is None
    if static: lt = 99
    pal = PAL[beat.get("bg", "ink")]
    img = grid_bg(W, H, pal, off=0 if static else int(lt * 20))
    # entry wipe from previous colour
    if not static and prev_bg and prev_bg != beat.get("bg") and lt < 0.22:
        k = ease(lt / 0.22)
        old = grid_bg(W, H, PAL[prev_bg])
        cut = int(W * k)
        img.paste(old.crop((cut, 0, W, H)), (cut, 0))
    d = ImageDraw.Draw(img)
    M = 84
    top = (440 if beat.get("is_cover") else 340) if mode == "reel" else 150
    # header
    if mode == "reel":
        d.text((M, 230), "THE COST NERD", font=F(XB, 32), fill=pal["fg"])
        if beat.get("series"):
            fs = F(XB, 28); tw = d.textlength(beat["series"], font=fs)
            x0 = M + d.textlength("THE COST NERD", font=F(XB, 32)) + 24
            d.rectangle([x0, 226, x0 + tw + 24, 270], fill=(247, 196, 49) if beat.get("bg") != "yellow" else (24, 22, 20))
            d.text((x0 + 12, 233), beat["series"], font=fs, fill=(24, 22, 20) if beat.get("bg") != "yellow" else (247, 196, 49))
    else:
        d.text((M, 56), "THE COST NERD", font=F(XB, 30), fill=pal["fg"])
        if total_pages and total_pages > 1:
            t = f"{page}/{total_pages}"; f = F(XB, 30)
            d.text((W - M - d.textlength(t, font=f), 56), t, font=f, fill=pal["fg"])
    if beat.get("end"):
        return end_frame(img, beat, W, H, lt, mode, pal)
    # headline
    maxw = W - 2 * M - (60 if mode == "reel" else 0)
    hmax = beat.get("hmax", 330 if mode == "reel" else 300)
    f, ls, s = fit(beat["head"], BLACK, maxw, hmax, beat.get("hsize", 132 if mode == "reel" else 112))
    k = min(1, max(0, lt / 0.3))
    hy = top + int(40 * (1 - ease(k)))
    if k > 0:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw_rich(layer, M, hy, ls, f, s, pal["fg"] + (255,), pal["hl"] + (255,), beat.get("hl", []))
        if k < 1:
            a = layer.getchannel("A").point(lambda v: int(v * ease(k))); layer.putalpha(a)
        img.paste(layer, (0, 0), layer)
    head_bottom = top + len(ls) * s * 1.04
    # art zone
    zone_top = head_bottom + 30
    zone_bot = ((1600 if beat.get("is_cover") else 1520) if mode == "reel" else H - 230) - (110 if beat.get("sub") else 0)
    zh = zone_bot - zone_top
    for i, spec in enumerate(beat.get("art", [])):
        im = get_art(spec, W)
        delay = spec.get("delay", 0.15 + 0.12 * i)
        kk = (lt - delay) / 0.45
        if kk <= 0: continue
        kk = min(1, kk)
        sc = max(0.05, ease_out_back(kk)) if spec.get("anim", "pop") == "pop" else 1
        bob = 0 if static else math.sin((lt + i) * 2.4) * 10
        rot = spec.get("rot", 0) + (0 if static else math.sin((lt + i * 0.7) * 1.8) * 2.0)
        cx = spec.get("x", 0.5) * W
        cy = zone_top + spec.get("y", 0.5) * zh + bob
        if spec.get("anim") == "slide":
            cx += (1 - ease(kk)) * W * spec.get("from", 0.6)
            sc = 1
        a = im
        if abs(sc - 1) > 0.01:
            a = a.resize((max(1, int(a.width * sc)), max(1, int(a.height * sc))), Image.BILINEAR)
        if abs(rot) > 0.2:
            a = a.rotate(rot, resample=Image.BILINEAR, expand=True)
        img.paste(a, (int(cx - a.width / 2), int(cy - a.height / 2)), a)
    # counter
    if beat.get("count"):
        c = beat["count"]
        kk = min(1, max(0, (lt - 0.2) / c.get("dur", 1.4)))
        v = c["from"] + (c["to"] - c["from"]) * ease(kk)
        txt = c["fmt"].format(v)
        f2 = F(BLACK, c.get("size", 300))
        cy = zone_top + c.get("y", 0.5) * zh
        col = pal["hl"] if beat.get("bg") != "yellow" else (216, 38, 30)
        d.text((W / 2, cy), txt, font=f2, fill=col, anchor="mm")
    # sub
    if beat.get("sub"):
        ks = min(1, max(0, (lt - 0.45) / 0.3))
        if ks > 0:
            f3, l3, s3 = fit(beat["sub"], SB, W - 2 * M, 130, 50 if mode == "reel" else 44)
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(layer)
            y = zone_bot + 30
            for l in l3:
                dl.text((W / 2, y), l, font=f3, fill=pal["sub"] + (int(255 * ks),), anchor="ma"); y += s3 * 1.25
            img.paste(layer, (0, 0), layer)
    if beat.get("sticker") and lt > 0.5:
        st = beat["sticker"]; kk = min(1, (lt - 0.5) / 0.3); sc = ease_out_back(kk)
        r = int(110 * sc)
        cx, cy = W - M - 90, int(zone_top + 90) + (0 if static else int(math.sin(lt * 5) * 8))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(247, 196, 49), outline=(24, 22, 20), width=8)
        if sc > 0.6:
            d.text((cx, cy), st, font=F(BLACK, int(64 * sc)), fill=(24, 22, 20), anchor="mm")
    if mode == "carousel" and beat.get("src"):
        d.text((M, H - 120), beat["src"], font=F(SB, 24), fill=pal["sub"])
    if mode == "carousel":
        d.text((M, H - 76), "@thecostnerd", font=F(SB, 28), fill=pal["sub"])
        if page and total_pages and page < total_pages:
            t = "SWIPE →"; f = F(XB, 30)
            d.text((W - M - d.textlength(t, font=f), H - 78), t, font=f, fill=pal["fg"])
    return img


def end_frame(img, beat, W, H, lt, mode, pal):
    d = ImageDraw.Draw(img)
    k = ease_out_back(min(1, lt / 0.45))
    cx, cy = W // 2, int(H * (0.36 if mode == "reel" else 0.30))
    r = int(230 * max(0.05, k))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(216, 38, 30), outline=(24, 22, 20), width=10)
    if k > 0.7: specs_mark(d, cx, cy + 10, int(82 * min(1, k)))
    y = cy + 290
    for l, c in (("FOLLOW", pal["fg"]), ("@THECOSTNERD", (216, 38, 30) if beat.get("bg") != "red" else (247, 196, 49))):
        f = F(BLACK, 100); d.text(((W - d.textlength(l, font=f)) / 2, y), l, font=f, fill=c); y += 110
    t = "The price tag never tells the whole story."
    f2 = F(SB, 40); d.text(((W - d.textlength(t, font=f2)) / 2, y + 10), t, font=f2, fill=pal["sub"]); y += 100
    f3, ls, s3 = fit(beat["end"], XB, W - 200, 130, 46)
    for l in ls:
        d.text(((W - d.textlength(l, font=f3)) / 2, y), l, font=f3, fill=pal["fg"]); y += s3 * 1.25
    if beat.get("src"):
        f4 = F(SB, 26); d.text(((W - d.textlength(beat["src"], font=f4)) / 2, H - (430 if mode == "reel" else 110)), beat["src"], font=f4, fill=pal["sub"])
    return img


def beat_len(b):
    if b.get("dur"): return b["dur"] * BEAT
    if b.get("end"): return 5 * BEAT
    words = len(b.get("head", "").split()) + 0.6 * len(b.get("sub", "").split())
    n = max(4, math.ceil((words * 0.26 + 1.0) / BEAT))
    return n * BEAT


def render_reel(reel, root, k):
    out = os.path.join(root, f"ig/{reel['date']}/{reel['slug']}"); os.makedirs(out, exist_ok=True)
    W, H = 1080, 1920
    beats = reel["beats"]
    lens = [beat_len(b) for b in beats]; starts = np.cumsum([0] + lens[:-1]); total = sum(lens)
    vid = os.path.join(out, "v.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
    n = int(round(total * FPS))
    for fi in range(n):
        t = fi / FPS
        bi = int(np.searchsorted(starts, t, side="right") - 1); lt = t - starts[bi]
        prev = beats[bi - 1].get("bg") if bi > 0 else None
        im = frame(beats[bi], W, H, lt + (0.9 if bi == 0 else 0), lens[bi], "reel", prev)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W, 12], fill=(45, 43, 40)); d.rectangle([0, 0, int(W * t / total), 12], fill=(247, 196, 49))
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    # cover: designed thumbnail
    cov = frame(dict(reel["cover"], is_cover=True), W, H, None, 3, "reel")
    cov.save(os.path.join(out, "cover.jpg"), "JPEG", quality=90)
    wav = os.path.join(out, "m.wav")
    write_wav(wav, music(total, list(starts), seed=k + 11, key=[0, 2, -2, 3, -3][k % 5]))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest",
                    "-movflags", "+faststart", os.path.join(out, "reel.mp4")], check=True)
    os.remove(vid); os.remove(wav)
    return total


def render_carousel(car, root):
    out = os.path.join(root, f"ig/{car['date']}/{car['slug']}"); os.makedirs(out, exist_ok=True)
    W, H = 1080, 1350
    for i, b in enumerate(car["slides"], 1):
        im = frame(b, W, H, None, 3, "carousel", page=i, total_pages=len(car["slides"]))
        im.save(os.path.join(out, f"slide-{i:02d}.jpg"), "JPEG", quality=90, optimize=True)


if __name__ == "__main__":
    data = json.load(open(sys.argv[1])); root = sys.argv[2]; only = sys.argv[3] if len(sys.argv) > 3 else None
    for k, r in enumerate(data):
        if only and r["slug"] != only: continue
        if r.get("slides"): render_carousel(r, root); print(r["slug"], "slides", len(r["slides"]))
        else: print(r["slug"], round(render_reel(r, root, k), 1), "s")
