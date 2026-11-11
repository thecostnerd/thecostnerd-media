"""Builds the three vertical Short scene files' content (imported by mo_teaser/mo_promoA/mo_promoB)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mo_main import art, pill, text, mono, spread3, spread13
D = os.path.dirname(os.path.abspath(__file__))
WHICH = "Which? (UK) Black Friday investigations"

def strike(x0, y0, x1, y1, at=0, d=0): return {"t": "strike", "x0": x0, "y0": y0, "x1": x1, "y1": y1, "at": at, "d": d}

OUTRO = lambda i, sub: {"ids": [i, i], "k": ("THE COST NERD", ""), "els": [
    {"t": "logo", "x": 540, "y": 520, "r": 120, "at": 0, "d": 0, "vertical": True},
    text("Full investigation\non the channel now", 540, 1060, at=0, d=0.3, size=76, font="xb"),
    pill(sub, 540, 1290, at=0.35, d=0, style="red", size=40)]}

TEASER = [
 {"ids": [1, 1], "k": ("BLACK FRIDAY", "An electric toothbrush, on sale"), "els": [
   text("\"SAVE £35\"", 540, 470, at=0, d=0, size=110, font="black", color="red2"),
   art("toothbrush", 420, 950, 620, d=0, anim="pop"),
   {"t": "tag", "txt": "£35", "small": "NOW", "x": 760, "y": 820, "w": 330, "at": 0, "d": 0.2},
   text("WAS £70", 760, 1100, at=0.55, d=0, size=80, font="black", color="grey"),
   strike(600, 1125, 920, 1080, at=0.6)]},
 {"ids": [2, 2], "k": ("THE 6 MONTHS BEFORE", "One square per day"), "src": WHICH, "els": [
   text("Full price, £70, on…", 540, 470, at=0, d=0, size=72, font="xb"),
   {"t": "dots", "n": 182, "cols": 14, "r": 15, "gap": 42, "x": 540, "y": 900, "shape": "sq", "hit_idx": spread3, "at": 0, "d": 0.1, "hit_at": 0.65, "fill_dur": 0.4, "base_dur": 0.8},
   pill("just 3 days", 540, 1330, at=0.7, d=0, style="red", size=48)]},
 {"ids": [3, 3], "k": ("BLACK FRIDAY 2022", "Which? tracked 208 deals"), "src": "Which? (UK), Nov 2023", "els": [
   {"t": "count", "from": 0, "to": 208, "fmt": "{:.0f} deals", "x": 540, "y": 470, "size": 110, "color": "white", "at": 0.2, "d": 0},
   {"t": "dots", "n": 208, "cols": 13, "r": 14, "gap": 40, "x": 540, "y": 920, "at": 0.25, "d": 0, "hit_idx": [17, 64, 103, 150, 190], "hit_at": 0.6, "fill_dur": 0.6, "base_dur": 0.9},
   pill("Only 5 were cheapest on the day", 540, 1300, at=0.65, d=0, style="red", size=40)]},
 {"ids": [4, 4], "k": ("THE QUESTION", ""), "els": [
   text("Are Black Friday\ndeals real?", 540, 760, at=0, d=0, size=110, font="xb"),
   pill("Full investigation: tomorrow", 540, 1100, at=0.45, d=0, style="red", size=42)]},
]

PROMO_A = [
 {"ids": [1, 1], "k": ("BLACK FRIDAY DEAL", "A robot vacuum"), "src": "Which? (UK), Nov 2025", "els": [
   text("CHEAPER IN MAY?", 540, 470, at=0, d=0, size=96, font="black", color="red2"),
   art("robot_vacuum", 480, 950, 600, d=0, anim="pop"),
   {"t": "tag", "txt": "£350", "small": "BLACK FRIDAY", "x": 760, "y": 760, "w": 340, "at": 0, "d": 0.2}]},
 {"ids": [2, 2], "k": ("BLACK FRIDAY DEAL", "Same vacuum, two prices"), "src": "Which? (UK), Nov 2025", "els": [
   {"t": "bars", "x": 470, "y": 1250, "h": 620, "vmax": 380, "bw": 220, "gap": 100, "at": 0, "d": 0.05, "stagger": 1.2, "vsize": 64,
    "items": [{"label": "MAY", "v": 299, "txt": "£299", "color": "cream"}, {"label": "BLACK FRIDAY", "v": 350, "txt": "£350", "color": "red"}],
    "delta": {"txt": "+£51", "size": 64, "pair": [0, 1]}, "delta_at": 0.6}]},
 {"ids": [3, 3], "k": ("HOW?", "The price before the sale"), "src": "Which? (UK), Nov 2025", "els": [
   {"t": "line", "x": 100, "y": 620, "w": 860, "h": 560, "pts": [299, 500, 350], "labels": ["MAY", "BEFORE", "BF"], "cur": "£", "lo": 200, "hi": 560, "mark": 2, "vsize": 56,
    "ref": {"v": 299, "txt": ""}, "at": 0, "d": 0.05, "dur_at": 0.6},
   pill("A discount from the peak", 540, 1400, at=0.7, d=0, style="red", size=44)]},
 {"ids": [4, 4], "k": ("BLACK FRIDAY 2024", "Which? tracked 175 deals"), "src": "Which? (UK), Nov 2025", "els": [
   {"t": "dots", "n": 175, "cols": 13, "r": 14, "gap": 40, "x": 540, "y": 880, "at": 0, "d": 0.05, "hit": 0, "base_dur": 1.0},
   text("Cheapest ONLY on\nBlack Friday:", 540, 470, at=0.55, d=0, size=70, font="xb"),
   {"t": "count", "from": 175, "to": 0, "fmt": "{:.0f}", "x": 540, "y": 1340, "size": 200, "at": 0.6, "d": 0}]},
 OUTRO(5, "Tap the link above"),
]

PROMO_B = [
 {"ids": [1, 1], "k": ("BLACK FRIDAY IS TOMORROW", ""), "els": [
   text("3 tricks\nto watch for", 540, 560, at=0, d=0, size=110, font="xb"),
   {"t": "cards", "items": [[1, "The \"was\"\nprice"], [2, "The deal\nthat never\nends"], [3, "The special\nmodel"]], "x": 540, "y": 1050, "w": 300, "h": 360, "fs": 30, "at": 0, "d": 0.2, "stagger": 0.2}]},
 {"ids": [2, 2], "k": ("TRICK 1 OF 3", "The \"was\" price"), "src": "Which? (UK), Nov 2025", "els": [
   {"t": "tag", "txt": "£50", "small": "WAS", "x": 540, "y": 560, "w": 420, "at": 0, "d": 0.1},
   {"t": "dots", "n": 182, "cols": 14, "r": 13, "gap": 36, "x": 540, "y": 1050, "shape": "sq", "hit_idx": spread13, "at": 0.3, "d": 0, "hit_at": 0.6, "fill_dur": 1.0, "base_dur": 0.8},
   pill("£50 on just 13 days in 6 months", 540, 1370, at=0.75, d=0, style="red", size=38)]},
 {"ids": [3, 3], "k": ("TRICK 2 OF 3", "The deal that never ends"), "src": "Which? (UK), Nov 2025", "els": [
   art("countdown", 540, 600, 640, d=0.05, anim="pop", txt="02:59:41", label="DEAL ENDS IN"),
   {"t": "dots", "n": 71, "cols": 12, "r": 15, "gap": 44, "x": 540, "y": 1050, "shape": "sq", "hit_idx": [i for i in range(71) if i != 29], "special": {"29": "yel"}, "at": 0.35, "d": 0, "hit_at": 0.55, "fill_dur": 1.2, "base_dur": 0.6},
   pill("Same price on 70 days", 540, 1370, at=0.75, d=0, style="red", size=42)]},
 {"ids": [4, 4], "k": ("TRICK 3 OF 3", "The special model"), "els": [
   art("tv", 330, 700, 400, d=0.05, anim="drop", txt="X100"),
   art("tv", 760, 700, 400, at=0.2, d=0, anim="drop", txt="X100B"),
   mono("THE FAMOUS ONE", 330, 920, at=0, d=0.4, size=24), mono("BLACK FRIDAY VERSION", 760, 920, at=0.2, d=0.3, size=24, color="red2"),
   {"t": "rows", "x": 160, "y": 1020, "w": 760, "title": "PRICE HISTORY · X100B", "rows": [["Last year", "—"], ["Last month", "—"]], "at": 0.6, "d": 0, "stagger": 0.3},
   {"t": "stamp", "txt": "NO HISTORY", "x": 600, "y": 1330, "size": 52, "rot": -8, "at": 0.8, "d": 0}]},
 OUTRO(5, "Tap the link above"),
]
