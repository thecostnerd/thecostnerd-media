"""Render bite-size kinetic-text Reels for The Cost Nerd (1080x1920, 30fps, original music bed)."""
import json, os, sys, subprocess, math, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
BPM = 100
BEAT = 60 / BPM  # 0.6s
BG = (20, 20, 20); GRID = (34, 34, 34); CREAM = (244, 238, 226); RED = (216, 38, 30)
GREY = (150, 146, 138); INK = (24, 22, 20)
FD = "/usr/share/fonts/opentype/inter/"
BLACK = FD + "InterDisplay-Black.otf"; XB = FD + "Inter-ExtraBold.otf"; SB = FD + "Inter-SemiBold.otf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"; MONOB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
X0 = 90; MAXW = 860  # keep clear of IG right-side buttons
TOP_SAFE, BOT_SAFE = 420, 1460


def F(p, s): return ImageFont.truetype(p, s)


_d = ImageDraw.Draw(Image.new("RGB", (10, 10)))


def wrap(text, font, maxw):
    lines, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if _d.textlength(t, font=font) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def fit(text, path, maxw, maxh, start, minsize=40, lh=1.08):
    s = start
    while s > minsize:
        f = F(path, s); ls = wrap(text, f, maxw)
        if all(_d.textlength(l, font=f) <= maxw for l in ls) and len(ls) * s * lh <= maxh:
            return f, ls, s
        s -= 4
    f = F(path, minsize); return f, wrap(text, f, maxw), minsize


def text_layer(lines, font, size, color, hl=None, lh=1.08):
    """Return list of (RGBA image, height) per line."""
    out = []
    for line in lines:
        w = int(_d.textlength(line, font=font)) + 10
        h = int(size * lh) + 10
        im = Image.new("RGBA", (max(w, 1), h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        x = 0
        words = line.split(" ")
        for i, wd in enumerate(words):
            tok = wd + (" " if i < len(words) - 1 else "")
            clean = wd.strip(".,!?:;“”\"'()")
            col = RED if hl and any(clean.lower() == h.strip(".,!?").lower() or wd.lower() == h.lower() for h in hl) else color
            d.text((x, 0), tok, font=font, fill=col)
            x += _d.textlength(tok, font=font)
        out.append(im)
    return out


def build_beat(b):
    """Return list of elements: dict(img, x, y, delay, pop). Vertically centred in safe band."""
    els = []  # (img, x, delay, pop)
    gap_after = []
    def add(lines_imgs, delay0, pop=False, gap=0, step=0.07):
        for i, im in enumerate(lines_imgs):
            els.append({"img": im, "delay": delay0 + i * step, "pop": pop})
            gap_after.append(0)
        if gap_after: gap_after[-1] = gap
    t = 0.0
    if b.get("end"):
        return None
    if b.get("top"):
        f, ls, s = fit(b["top"], SB, MAXW, 200, 58)
        add(text_layer(ls, f, s, GREY, lh=1.2), t, gap=24); t += 0.12
    if b.get("big"):
        f, ls, s = fit(b["big"], BLACK, MAXW, 420, 300)
        add(text_layer(ls, f, s, RED, lh=1.0), t, pop=True, gap=24); t += 0.15
    if b.get("quote"):
        f, ls, s = fit(b["quote"], XB, MAXW, 600, 84)
        add(text_layer(ls, f, s, CREAM, lh=1.15), t, gap=10); t += 0.1
    if b.get("text"):
        f, ls, s = fit(b["text"], BLACK, MAXW, 700, 118)
        add(text_layer(ls, f, s, CREAM, hl=b.get("hl"), lh=1.06), t, gap=10, step=0.16)
        for e in els[-len(ls):]: e["wipe"] = True
    if b.get("text2"):
        f, ls, s = fit(b["text2"], BLACK, MAXW, 620, 96)
        add(text_layer(ls, f, s, CREAM, lh=1.08), t)
    if b.get("bottom"):
        f, ls, s = fit(b["bottom"], SB, MAXW, 260, 54)
        add(text_layer(ls, f, s, CREAM, lh=1.25), t + 0.2)
    if b.get("tiles"):
        tw, th, gp = 270, 300, 25
        for i, lab in enumerate(b["tiles"]):
            im = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            win = b.get("win")
            fill = RED if win == i else (CREAM if win is None else (60, 58, 55))
            tcol = CREAM if win == i else INK
            d.rectangle([0, 0, tw, th], fill=fill)
            d.text((tw / 2, th / 2), lab, font=F(BLACK, 110), fill=tcol, anchor="mm")
            els.append({"img": im, "delay": t + 0.1 * i, "pop": win == i, "row": "tiles", "col": i, "tw": tw, "gp": gp})
            gap_after.append(0)
    if b.get("rows"):
        rw = MAXW; rh = 120
        for i, (l, r) in enumerate(b["rows"]):
            im = Image.new("RGBA", (rw, rh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            last = i == len(b["rows"]) - 1
            if last: d.rectangle([0, 0, rw, 6], fill=GREY)
            col = RED if r.startswith("+") or last else CREAM
            fnt = F(BLACK if last else XB, 84 if last else 72)
            d.text((0, 20), l, font=fnt, fill=CREAM)
            d.text((rw - _d.textlength(r, font=fnt), 20), r, font=fnt, fill=col)
            els.append({"img": im, "delay": t + 0.45 * i, "pop": last})
            gap_after.append(0)
        els[-1]["after"] = 0
    # layout: stack vertically (tiles share a row)
    rows = []
    i = 0
    while i < len(els):
        e = els[i]
        if e.get("row") == "tiles":
            grp = [x for x in els[i:] if x.get("row") == "tiles"]
            rows.append(("tiles", grp)); i += len(grp)
        else:
            rows.append(("line", [e])); i += 1
    heights = []
    for k, (kind, grp) in enumerate(rows):
        heights.append(grp[0]["img"].height)
    # gaps
    gaps = []
    idx = 0
    for kind, grp in rows:
        g = gap_after[idx + len(grp) - 1] if idx + len(grp) - 1 < len(gap_after) else 0
        gaps.append(g); idx += len(grp)
    total = sum(heights) + sum(gaps[:-1])
    y = TOP_SAFE + max(0, (BOT_SAFE - TOP_SAFE - total) // 2)
    for (kind, grp), h, g in zip(rows, heights, gaps):
        if kind == "tiles":
            for e in grp:
                e["x"] = X0 + e["col"] * (e["tw"] + e["gp"]); e["y"] = y
        else:
            grp[0]["x"] = X0; grp[0]["y"] = y
        y += h + g
    return els


def ease(t): return 1 - (1 - t) ** 3


def specs(d, cx, cy, r):
    for dx in (-r - 14, r + 14):
        d.ellipse([cx + dx - r, cy - r, cx + dx + r, cy + r], fill=CREAM, outline=INK, width=14)
        d.text((cx + dx, cy + 4), "¢", font=F(BLACK, int(r * 1.15)), fill=INK, anchor="mm")
    d.rectangle([cx - 20, cy - 8, cx + 20, cy + 8], fill=INK)
    d.rectangle([cx - 14, cy - 18, cx + 14, cy + 18], fill=CREAM, outline=INK, width=4)


def end_card(line, src):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, cy = W // 2, 720
    d.ellipse([cx - 230, cy - 230, cx + 230, cy + 230], fill=RED)
    specs(d, cx, cy + 10, 82)
    y = 1010
    for l, c in (("FOLLOW", CREAM), ("@THECOSTNERD", RED)):
        f = F(BLACK, 100); d.text(((W - d.textlength(l, font=f)) / 2, y), l, font=f, fill=c); y += 110
    y += 20
    t = "The price tag never tells the whole story."
    f2 = F(SB, 42); d.text(((W - d.textlength(t, font=f2)) / 2, y), t, font=f2, fill=GREY); y += 90
    f3, ls, s3 = fit(line, XB, 860, 140, 46)
    for l in ls:
        d.text(((W - d.textlength(l, font=f3)) / 2, y), l, font=f3, fill=CREAM); y += s3 * 1.25
    f4 = F(SB, 28)
    d.text(((W - d.textlength(src, font=f4)) / 2, 1500), src, font=f4, fill=GREY)
    return im


def make_bg():
    big = Image.new("RGB", (W + 60, H + 60), BG); d = ImageDraw.Draw(big)
    for gx in range(0, W + 60, 60): d.line([(gx, 0), (gx, H + 60)], fill=GRID, width=1)
    for gy in range(0, H + 60, 60): d.line([(0, gy), (W + 60, gy)], fill=GRID, width=1)
    return big


def header(img):
    d = ImageDraw.Draw(img)
    d.text((X0, 250), "THE COST NERD", font=F(XB, 34), fill=CREAM)


def beat_len(b):
    if b.get("end"): return 4 * BEAT
    words = sum(len(str(b.get(k, "")).split()) for k in ("top", "big", "text", "text2", "bottom", "quote"))
    if b.get("rows"): words += 8
    if b.get("tiles"): words += 3
    secs = words * 0.25 + 0.7
    n = max(3, math.ceil(secs / BEAT))
    return n * BEAT


def render(reel, outdir):
    os.makedirs(outdir, exist_ok=True)
    beats = reel["beats"]
    lens = [beat_len(b) for b in beats]
    starts = np.cumsum([0] + lens[:-1])
    total = sum(lens)
    nframes = int(round(total * FPS))
    built = [build_beat(b) if not b.get("end") else end_card(b["end"], reel["src"]) for b in beats]
    bg = make_bg()
    vid = os.path.join(outdir, "video_only.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
    cover = None
    for fi in range(nframes):
        t = fi / FPS
        bi = int(np.searchsorted(starts, t, side="right") - 1)
        lt = t - starts[bi]
        off = int((t * 12) % 60)
        frame = bg.crop((off, off, off + W, off + H)).copy()
        header(frame)
        b = beats[bi]
        if b.get("end"):
            a = min(1, lt / 0.3)
            layer = built[bi]
            if a < 1:
                layer = layer.copy(); layer.putalpha(Image.eval(layer.getchannel("A"), lambda v: int(v * a)))
            frame.paste(layer, (0, 0), layer)
        else:
            for e in built[bi]:
                k = (lt - e["delay"]) / (0.42 if e.get("wipe") else 0.32)
                if k <= 0: continue
                k = min(1, k); ek = ease(k)
                im = e["img"]
                if e.get("pop"):
                    sc = 0.86 + 0.14 * ek + (0.04 * math.sin(math.pi * k) if k < 1 else 0)
                    if abs(sc - 1) > 0.005:
                        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))))
                    dx = (e["img"].width - im.width) // 2 if not e.get("row") else (e["img"].width - im.width) // 2
                    dy = (e["img"].height - im.height) // 2
                    x, y = e["x"] + (0 if not e.get("row") else dx), e["y"] + dy
                elif e.get("wipe"):
                    x, y = e["x"], e["y"] + int(20 * (1 - ek))
                    cw = max(1, int(im.width * min(1, k * 1.15)))
                    im = im.crop((0, 0, cw, im.height))
                else:
                    x, y = e["x"], e["y"] + int(50 * (1 - ek))
                if ek < 1:
                    im = im.copy(); al = im.getchannel("A").point(lambda v: int(v * ek)); im.putalpha(al)
                frame.paste(im, (int(x), int(y)), im)
        # progress bar
        d = ImageDraw.Draw(frame)
        d.rectangle([0, 0, W, 12], fill=(45, 43, 40))
        d.rectangle([0, 0, int(W * (t / total)), 12], fill=RED)
        if bi == 0 and cover is None and lt >= lens[0] - 0.05:
            cover = frame.copy()
        p.stdin.write(frame.tobytes())
    p.stdin.close(); p.wait()
    if cover is None: cover = frame
    cover.save(os.path.join(outdir, "cover.jpg"), "JPEG", quality=90)
    return vid, total, list(starts)


# ---------------- music ----------------
SR = 44100


def env(n, a, r):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    e *= np.exp(-np.arange(n) / (r * SR)); return e


def music(total, cuts, seed=1, key=0):
    rng = np.random.default_rng(seed)
    n = int((total + 0.5) * SR); out = np.zeros(n)
    def put(sig, t):
        i = int(t * SR); j = min(n, i + len(sig))
        if i < n: out[i:j] += sig[: j - i]
    # chords: Am F C G (semitone offsets from A)
    prog = [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)]
    roots = [45, 41, 48, 43]
    hz = lambda m: 440 * 2 ** ((m + key - 69) / 12)
    bar = 4 * BEAT
    nb = int(math.ceil(total / bar)) + 1
    for bi in range(nb):
        t0 = bi * bar; ch = prog[bi % 4]
        L = int(bar * SR); tt = np.arange(L) / SR
        pad = sum(np.sin(2 * np.pi * hz(m) * tt) + 0.5 * np.sin(2 * np.pi * hz(m) * 1.003 * tt) for m in ch)
        pe = np.minimum(1, tt / 0.4) * np.minimum(1, (bar - tt) / 0.3)
        put(0.035 * pad * pe, t0)
        for half in (0, 2):
            Lb = int(1.1 * SR); tb = np.arange(Lb) / SR
            put(0.16 * np.sin(2 * np.pi * hz(roots[bi % 4]) * tb) * env(Lb, 0.01, 0.35), t0 + half * BEAT)
        for s in range(4):
            tb = t0 + s * BEAT
            if s in (0, 2):
                Lk = int(0.35 * SR); tk = np.arange(Lk) / SR
                f = 45 + 75 * np.exp(-tk * 25); ph = 2 * np.pi * np.cumsum(f) / SR
                put(0.55 * np.sin(ph) * env(Lk, 0.002, 0.12), tb)
            else:
                Ls = int(0.2 * SR); nz = rng.standard_normal(Ls)
                nz = np.diff(np.concatenate([[0], nz]))
                put(0.16 * nz * env(Ls, 0.001, 0.05), tb)
            for h in (0, 0.5):
                Lh = int(0.05 * SR); hz_ = np.diff(np.concatenate([[0], rng.standard_normal(Lh)]))
                put(0.05 * hz_ * env(Lh, 0.0005, 0.012), tb + h * BEAT)
    for c in cuts[1:]:
        Lw = int(0.3 * SR); tw = np.arange(Lw) / SR
        nz = rng.standard_normal(Lw)
        sw = np.convolve(nz, np.ones(6) / 6, mode="same")
        put(0.10 * sw * (tw / 0.3) ** 2, max(0, c - 0.3))
    # fade out
    fo = int(1.2 * SR); end = int(total * SR)
    out[end - fo:end] *= np.linspace(1, 0, fo); out[end:] = 0
    out = out[: end]
    out = np.tanh(out * 1.2)
    out /= np.max(np.abs(out)) / 0.89
    return (out * 32767).astype(np.int16)


def write_wav(path, data):
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())


if __name__ == "__main__":
    reels = json.load(open(sys.argv[1])); root = sys.argv[2]
    only = sys.argv[3] if len(sys.argv) > 3 else None
    for k, r in enumerate(reels):
        if only and r["slug"] != only: continue
        out = os.path.join(root, f"ig/{r['date']}/{r['slug']}")
        vid, total, starts = render(r, out)
        wav = os.path.join(out, "music.wav")
        write_wav(wav, music(total, starts, seed=k + 3, key=[0, 2, -2, 3, -3][k % 5]))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                        "-shortest", "-movflags", "+faststart", os.path.join(out, "reel.mp4")], check=True)
        os.remove(vid); os.remove(wav)
        print(r["slug"], round(total, 1), "s")
