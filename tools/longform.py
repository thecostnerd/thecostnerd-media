"""Narration-timed explainer renderer for The Cost Nerd.
Horizontal long-form (1920x1080) and vertical Shorts (1080x1920) from a scene list + Kokoro WAVs.
Usage: python3 longform.py <episode.py> <voice_dir> <out_dir> <h|v>
episode.py defines SCENES (list of dicts) and optionally CHAPTERS {first_line_id: title}, END (dict).
Scene keys: ids [a,b] inclusive line ids, head, hl [words], sub, bg (ink|cream|red|yellow), art [specs as in reel2], count {from,to,fmt}.
"""
import json, os, sys, math, subprocess, wave, importlib.util
import numpy as np
from PIL import Image, ImageDraw
import art as A
import srtnum
from reel2 import PAL, F, fit, draw_rich, ease, ease_out_back, grid_bg, specs_mark, BLACK, XB, SB
from reel import music, write_wav

FPS = 30
GAP = 0.30          # silence between lines
SCENE_GAP = 0.15    # extra at scene change
STING = 1.6         # chapter card length (h only)
YEL = (247, 196, 49); RED = (216, 38, 30); INK = (24, 22, 20); CREAM = (244, 238, 226)


def load(path):
    spec = importlib.util.spec_from_file_location("ep", path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def read_wav(p):
    with wave.open(p) as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
    if ch == 2: a = a.reshape(-1, 2).mean(1)
    assert sr == 48000, sr
    # trim leading/trailing silence
    nz = np.where(np.abs(a) > 0.01)[0]
    if len(nz): a = a[max(0, nz[0] - 1200): nz[-1] + 2400]
    return a


def layout(mode):
    if mode == "h":
        return dict(W=1920, H=1080, M=110)
    return dict(W=1080, H=1920, M=84)


_art_cache = {}


def art_img(spec, S):
    key = json.dumps(spec, sort_keys=True) + str(S)
    if key not in _art_cache:
        args = {a: (tuple(tuple(x) if isinstance(x, list) else x for x in v) if isinstance(v, list) else v) for a, v in spec.get("args", {}).items()}
        _art_cache[key] = A.ART[spec["f"]](S, **args)
    return _art_cache[key]


def draw_scene(sc, mode, lt, chapter_label=""):
    L = layout(mode); W, H, M = L["W"], L["H"], L["M"]
    static = lt >= 1.1
    pal = PAL[sc.get("bg", "ink")]
    img = grid_bg(W, H, pal).copy()
    d = ImageDraw.Draw(img)
    # header
    hy = 60 if mode == "h" else 230
    d.text((M, hy), "THE COST NERD", font=F(XB, 30 if mode == "h" else 32), fill=pal["fg"])
    if chapter_label and mode == "h":
        fs = F(XB, 26); tw = d.textlength(chapter_label, font=fs)
        x0 = M + d.textlength("THE COST NERD", font=F(XB, 30)) + 22
        tag_bg = YEL if sc.get("bg") != "yellow" else INK; tag_fg = INK if sc.get("bg") != "yellow" else YEL
        d.rectangle([x0, hy - 4, x0 + tw + 24, hy + 38], fill=tag_bg); d.text((x0 + 12, hy + 2), chapter_label, font=fs, fill=tag_fg)
    if sc.get("end"):
        return end_card(img, sc, mode, lt, pal)
    arts = sc.get("art", []); has_zone = bool(arts) or bool(sc.get("count"))
    if mode == "h":
        if sc.get("center") or not has_zone:
            tx, tw_, ty, hmax, hs = M, W - 2 * M, (300 if has_zone else 330), (260 if has_zone else 420), sc.get("hsize", 120 if has_zone else 150)
            zone = (M, 560, W - M, H - 90) if has_zone else None
        else:
            tx, tw_, ty, hmax, hs = M, 860, 250, 520, sc.get("hsize", 116)
            zone = (1020, 150, W - 70, H - 80)
    else:
        tx, tw_, ty, hmax, hs = M, W - 2 * M - 40, 340, 420, sc.get("hsize", 120)
        zone = (M, 0, W - M, 1500)
    f, ls, s = fit(sc["head"], BLACK, tw_, hmax, hs)
    k = min(1, lt / 0.3)
    yoff = int(36 * (1 - ease(k)))
    block_h = len(ls) * s * 1.04
    if mode == "h" and not (sc.get("center") or not has_zone):
        sub_h = 0
        if sc.get("sub"):
            f3, l3, s3 = fit(sc["sub"], SB, tw_, 200, 46); sub_h = 30 + len(l3) * s3 * 1.25
        ty = int((H - block_h - sub_h) / 2) + 20
    center = mode == "h" and (sc.get("center") or not has_zone)
    if k > 0:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw_rich(layer, tx, ty + yoff, ls, f, s, pal["fg"] + (255,), pal["hl"] + (255,), sc.get("hl", []), center=center, W=W)
        if k < 1:
            layer.putalpha(layer.getchannel("A").point(lambda v: int(v * ease(k))))
        img.paste(layer, (0, 0), layer)
    bottom = ty + block_h
    if sc.get("sub"):
        ks = min(1, max(0, (lt - 0.35) / 0.3))
        if ks > 0:
            f3, l3, s3 = fit(sc["sub"], SB, tw_, 200, 46 if mode == "h" else 50)
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(layer); y = bottom + 30
            for l in l3:
                if center: dl.text((W / 2, y), l, font=f3, fill=pal["sub"] + (int(255 * ks),), anchor="ma")
                else: dl.text((tx, y), l, font=f3, fill=pal["sub"] + (int(255 * ks),))
                y += s3 * 1.25
            img.paste(layer, (0, 0), layer); bottom = y
    if mode == "v": zone = (M, bottom + 40, W - M, 1500)
    if zone:
        zx0, zy0, zx1, zy1 = zone; zw, zh = zx1 - zx0, zy1 - zy0
        for i, spec in enumerate(arts):
            S = int(spec.get("s", 0.8) * min(zw, zh) if mode == "h" else spec.get("s", 0.6) * W)
            im = art_img(spec, S)
            delay = spec.get("delay", 0.12 + 0.14 * i)
            kk = (lt - delay) / 0.45
            if kk <= 0: continue
            kk = min(1, kk); sc_ = max(0.05, ease_out_back(kk))
            cx = zx0 + spec.get("x", 0.5) * zw; cy = zy0 + spec.get("y", 0.5) * zh
            a = im
            if abs(sc_ - 1) > 0.01: a = a.resize((max(1, int(a.width * sc_)), max(1, int(a.height * sc_))), Image.BILINEAR)
            if spec.get("rot"): a = a.rotate(spec["rot"], resample=Image.BICUBIC, expand=True)
            img.paste(a, (int(cx - a.width / 2), int(cy - a.height / 2)), a)
        if sc.get("count"):
            c = sc["count"]; kk = min(1, max(0, (lt - 0.15) / c.get("dur", 0.9)))
            v = c["from"] + (c["to"] - c["from"]) * ease(kk)
            col = pal["hl"] if sc.get("bg") != "yellow" else RED
            size = c.get("size", 300 if mode == "h" else 320)
            fc = F(BLACK, size); txt = c["fmt"].format(v)
            while d.textlength(c["fmt"].format(c["to"]), font=fc) > zw - 20: size -= 10; fc = F(BLACK, size)
            d.text((zx0 + zw * c.get("x", 0.5), zy0 + zh * c.get("y", 0.5)), txt, font=fc, fill=col, anchor="mm")
    if sc.get("src"):
        fs = F(SB, 24 if mode == "h" else 28)
        d.text((M, H - (54 if mode == "h" else 380)), sc["src"], font=fs, fill=pal["sub"])
    return img


def end_card(img, sc, mode, lt, pal):
    L = layout(mode); W, H = L["W"], L["H"]; d = ImageDraw.Draw(img)
    k = ease_out_back(min(1, lt / 0.45))
    if mode == "h":
        cx, cy = 360, 430
    else:
        cx, cy = W // 2, 720
    r = int(200 * max(0.05, k))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=INK, width=10)
    if k > 0.7: specs_mark(d, cx, cy + 8, int(70 * min(1, k)))
    lines = sc["end"]
    y = cy + 250
    for i, l in enumerate(lines):
        f = F(BLACK if i == 0 else SB, (86 if i == 0 else 42) if mode == "h" else (90 if i == 0 else 44))
        col = pal["fg"] if i != 1 else pal["sub"]
        if mode == "h": d.text((cx, y), l, font=f, fill=col, anchor="ma")
        else: d.text((W / 2, y), l, font=f, fill=col, anchor="ma")
        y += 100 if i == 0 else 60
    if mode == "h" and sc.get("watch_next"):
        # leave the right side clear for YouTube end-screen elements; label the slot
        d.text((1340, 230), sc["watch_next"], font=F(XB, 40), fill=pal["hl"], anchor="ma")
        d.rounded_rectangle([960, 300, 1720, 728], radius=18, outline=pal["sub"], width=4)
    return img


def sting(title, mode, lt, num):
    L = layout(mode); W, H = L["W"], L["H"]
    pal = PAL["yellow"]; img = grid_bg(W, H, pal).copy(); d = ImageDraw.Draw(img)
    k = ease(min(1, lt / 0.35))
    d.text((W / 2, H / 2 - 120 - 30 * (1 - k)), f"PART {num}", font=F(XB, 44), fill=RED, anchor="mm")
    f, ls, s = fit(title.upper(), BLACK, W - 300, 330, 130)
    y = H / 2 - len(ls) * s * 1.04 / 2 + 40 + 30 * (1 - k)
    for l in ls:
        d.text((W / 2, y), l, font=f, fill=INK, anchor="ma"); y += s * 1.04
    return img


def build(ep, voice_dir, out_dir, mode, name):
    os.makedirs(out_dir, exist_ok=True)
    L = layout(mode); W, H = L["W"], L["H"]
    SR = 48000
    chapters = getattr(ep, "CHAPTERS", {}) if mode == "h" else {}
    texts = {l["id"]: l["text"] for l in json.load(open(ep.LINES))}
    timeline = []   # (kind, t0, t1, payload)
    voice = []; t = 0.0; cues = []; chap_marks = []
    lead = 0.4
    voice.append(np.zeros(int(lead * SR))); t += lead
    cur_chapter = ""; nchap = 0
    for si, sc in enumerate(ep.SCENES):
        a, b = sc["ids"]
        ids = [i for i in sorted(texts) if a <= i <= b]
        if ids[0] in chapters and ids[0] != min(texts):
            nchap += 1
            voice.append(np.zeros(int(STING * SR))); timeline.append(("sting", t, t + STING, (chapters[ids[0]], nchap))); chap_marks.append((t, chapters[ids[0]])); t += STING
            cur_chapter = chapters[ids[0]]
        elif ids[0] in chapters:
            chap_marks.append((0.0, chapters[ids[0]])); cur_chapter = chapters[ids[0]]
        s0 = t
        for i in ids:
            w = read_wav(os.path.join(voice_dir, f"line-{i:02d}.wav"))
            cues.append((t, t + len(w) / SR, getattr(ep, 'SRT', {}).get(i, srtnum.convert(texts[i])).replace('E U', 'EU').replace('N Z', 'NZ')))
            voice.append(w); t += len(w) / SR
            voice.append(np.zeros(int(GAP * SR))); t += GAP
        voice.append(np.zeros(int(SCENE_GAP * SR))); t += SCENE_GAP
        timeline.append(("scene", s0, t, (sc, cur_chapter if mode == "h" else "")))
    end = getattr(ep, "END", None)
    if end:
        hold = end.get("hold", 12 if mode == "h" else 3)
        voice.append(np.zeros(int(hold * SR))); timeline.append(("scene", t, t + hold, (end, ""))); t += hold
    total = t
    SRT_ONLY = bool(os.environ.get('SRT_ONLY'))
    if SRT_ONLY: chap_marks_ = chap_marks
    vo = np.concatenate(voice)
    vo = vo / max(1e-6, np.max(np.abs(vo))) * 0.9
    if not SRT_ONLY:
        vpath = os.path.join(out_dir, f"{name}-voice.wav")
        with wave.open(vpath, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((vo * 32767).astype(np.int16).tobytes())
        mpath = os.path.join(out_dir, f"{name}-music.wav")
        write_wav(mpath, music(total, [m[0] for m in chap_marks] if mode == "h" else [x[1] for x in timeline], seed=7, key=0))
        # video
        vid = os.path.join(out_dir, f"{name}-v.mp4")
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
        n = int(math.ceil(total * FPS)); ti = 0; cache = None; cache_key = None
        bar_y = H - 10
        for fi in range(n):
            tt = fi / FPS
            while ti < len(timeline) - 1 and tt >= timeline[ti][2]: ti += 1
            kind, t0, t1, pay = timeline[ti]; lt = tt - t0
            if ti == 0: lt += 1.6  # finished hook on frame 1
            if kind == "sting":
                im = sting(pay[0], mode, lt, pay[1]) if lt < 0.4 or cache_key != (ti, "s") else cache.copy()
                if lt >= 0.4 and cache_key != (ti, "s"): cache, cache_key = im.copy(), (ti, "s")
            else:
                sc, ch = pay
                settle = 1.1 + (sc.get('count', {}).get('dur', 0.9) + 0.2 if sc.get('count') else 0)
                if lt >= settle and cache_key == (ti, "c"): im = cache.copy()
                else:
                    im = draw_scene(sc, mode, lt, ch)
                    if lt >= settle: cache, cache_key = im.copy(), (ti, "c")
            d = ImageDraw.Draw(im)
            d.rectangle([0, bar_y, W, H], fill=(45, 43, 40)); d.rectangle([0, bar_y, int(W * tt / total), H], fill=YEL)
            p.stdin.write(im.tobytes())
        p.stdin.close(); p.wait()
        # mix: voice + music bed ~ -20 dB, loudness normalise
        final = os.path.join(out_dir, f"{name}.mp4")
        mvol = 0.10 if mode == "h" else 0.16
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", vpath, "-i", mpath, "-filter_complex",
                        f"[2:a]aresample=48000,volume={mvol}[m];[1:a][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", final], check=True)
        for x in (vid, vpath, mpath): os.remove(x)
    # SRT
    def ts(x):
        h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
        return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)) % 1000:03d}"
    out = []; k = 1
    for a0, a1, txt in cues:
        words = txt.split()
        parts = [txt] if len(txt) <= 84 else [" ".join(words[:len(words) // 2]), " ".join(words[len(words) // 2:])]
        tot = sum(len(pp) for pp in parts); c0 = a0
        for pp in parts:
            c1 = c0 + (a1 - a0) * len(pp) / tot
            out.append(f"{k}\n{ts(c0)} --> {ts(c1)}\n{pp}\n"); k += 1; c0 = c1
    open(os.path.join(out_dir, f"{name}.srt"), "w").write("\n".join(out))
    def mmss(x): return f"{int(x // 60)}:{int(x % 60):02d}"
    json.dump({"total": total, "chapters": [(mmss(a), b) for a, b in chap_marks]}, open(os.path.join(out_dir, f"{name}-meta.json"), "w"), indent=1)
    return total, chap_marks


if __name__ == "__main__":
    ep = load(sys.argv[1]); mode = sys.argv[4]; name = os.path.splitext(os.path.basename(sys.argv[1]))[0]
    tot, ch = build(ep, sys.argv[2], sys.argv[3], mode, name)
    print(name, f"{tot:.1f}s", ch)
