"""Is Black Friday Real? (bonus) - motion-graphics scene plan, Episode 1-2 house style."""
import os
LINES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out2/thecostnerd-bonus-bf2-main-lines.json")

CHAPTERS = {1: "The \"half price\" toothbrush", 11: "Are Black Friday deals real?", 21: "The evidence: years of price tracking",
            41: "Trick 1: the \"was\" price", 51: "Trick 2: the deal that never ends", 61: "Trick 3: the special model",
            71: "Is it legal?", 81: "Why it still works", 91: "The one number", 101: "What to do before you buy", 111: "Next: hidden fees"}

SRT = {
 1: "This electric toothbrush was on sale for Black Friday. \"Save £35\", the sign said. Was £70, now £35.",
 21: "The consumer group Which?, in the United Kingdom, has tracked the daily prices of Black Friday deals for years, at big retailers like Amazon, Argos, Currys and John Lewis.",
 23: "Start with Black Friday 2022. Which? followed 208 discounted products.",
 26: "One pair of wireless earbuds was cut from £139 to £119. But for much of the summer before, they had cost between £99 and £109.",
 28: "The next year, Which? checked 227 deals. 92% were the same price or cheaper at other times of the year.",
 29: "Then it checked the 2024 sale. 175 products, across 8 retailers. 83% were the same price or cheaper outside the sale.",
 31: "This isn't just a British thing. In New Zealand, the group Consumer NZ tracked prices for 14 weeks before last year's sales. For half the products, shoppers could have paid the same or less in the months before.",
 32: "One blender was $70 in September, and $100 during the sale.",
 33: "To be fair, some retailers disagree with these studies. Amazon pointed out that Which? looked at only a small number of its products. But the pattern keeps showing up, year after year, country after country.",
 42: "Trick 1 is the \"was\" price. A discount needs something to be discounted from, and that number, the \"was\" price, or the recommended retail price, is the anchor.",
 44: "That's how a toothbrush that sold at £70 for just 3 days can carry a £70 \"was\" price.",
 45: "The same store had a second toothbrush. \"Save £25\", it said, from a recommended price of £50. That £50 price applied for 13 days, in 6 months.",
 51: "Trick 2 is the deal that never ends. Some Black Friday prices aren't inflated at all. They're just not special.",
 54: "And sometimes, it's worse. One robot vacuum was £299 in May. Before the sale, its price climbed to £500. Then its Black Friday deal price was £350.",
 61: "Trick 3 is the special model, and it's one you'd never spot in a store.",
 63: "Back in 2015, electronics reviewers warned shoppers about Black Friday televisions like this. One 58-inch set had 10 dimming zones. A higher-end model from the same brand had 32.",
 72: "In the United States, the Federal Trade Commission has had guides on this for decades. A \"was\" price is only honest if the item was really offered at that price, regularly, for a reasonably substantial period.",
 73: "The guide even gives an example. A pen normally sells for $7.50. The store lists it at $10 for a few days, then advertises a bargain, from $10, down to $7.50. That, says the guide, is a fictitious former price.",
 81: "So why do retailers keep doing it? On Black Friday 2025, Americans spent a record $11.8 billion online, according to Adobe Analytics.",
 82: "And in the first four weeks of November, $8.2 billion of online spending went through buy now, pay later.",
 91: "So here's the number to remember. 2. Out of every 100 Black Friday deals that Which? tracked in 2022, only 2 were actually the lowest price of the year, on the day.",
 102: "1. Check the price history. Free trackers like Keepa and CamelCamelCamel show what an item on Amazon has cost for months, and other trackers cover other stores. If the deal price shows up all year, it's not a deal. It's just the price.",
 103: "2. Ignore the \"was\" price. Compare it with what the item actually sold for, not what the tag says it used to cost.",
 104: "3. Search the model number. If all you find are Black Friday ads, and no reviews, you might be looking at a special model.",
 105: "4. Decide your price now. Write down what you'd happily pay for the thing you want. If the sale hits it, buy. If it doesn't, walk away.",
 106: "And 5. Check the total before you pay, because the price on the sign is not always the price at the end.",
}

def art(f, x, y, s, at=0, d=0.15, **kw):
    e = {"t": "art", "f": f, "x": x, "y": y, "s": s, "at": at, "d": d}
    for k in ("anim", "rot", "bob", "out", "od"):
        if k in kw: e[k] = kw.pop(k)
    e["args"] = kw; return e

def pill(txt, x, y, at=0, d=0.15, style="card", size=30, **kw):
    return dict({"t": "pill", "txt": txt, "x": x, "y": y, "at": at, "d": d, "style": style, "size": size}, **kw)

def text(txt, x, y, at=0, d=0.15, size=40, font="bold", color="white", **kw):
    return dict({"t": "text", "txt": txt, "x": x, "y": y, "at": at, "d": d, "size": size, "font": font, "color": color}, **kw)

def mono(txt, x, y, at=0, d=0.15, color="grey", size=20, anchor="mm"):
    return {"t": "text", "txt": txt, "x": x, "y": y, "at": at, "d": d, "size": size, "font": "mono", "color": color, "spaced": True, "anchor": anchor}

SIX_MONTHS = 182
spread3 = [37, 98, 151]
spread13 = [5, 19, 33, 41, 58, 72, 90, 104, 117, 131, 146, 160, 175]
WHICH = "Which? (UK) Black Friday investigations, 2022–2024"

SCENES = [
 # ---------------- cold open ----------------
 {"ids": [1, 1], "k": ("BLACK FRIDAY", "An electric toothbrush, on sale"), "els": [
   art("toothbrush", 760, 560, 560, d=0.1, anim="drop"),
   {"t": "tag", "txt": "£35", "small": "NOW", "x": 1080, "y": 430, "w": 300, "at": 0.35, "d": 0},
   text("WAS £70", 1150, 280, at=0.7, d=0, size=60, font="black", color="grey"),
   {"t": "strike", "x0": 1015, "y0": 300, "x1": 1290, "y1": 262, "at": 0.78, "d": 0},
 ]},
 {"ids": [2, 2], "k": ("BLACK FRIDAY", "An electric toothbrush, on sale"), "els": [
   {"t": "count", "from": 0, "to": 50, "fmt": "{:.0f}% OFF", "x": 960, "y": 470, "size": 230, "at": 0, "d": 0.05, "sub": "Who says no to that?", "subsize": 44},
 ]},
 {"ids": [3, 4], "k": ("THE PRICE HISTORY", "The 6 months before the sale, one square per day"), "src": WHICH, "els": [
   {"t": "dots", "n": SIX_MONTHS, "cols": 26, "r": 11, "gap": 32, "x": 960, "y": 470, "shape": "sq", "hit_idx": spread3, "at": 0, "hit_at": 0.75, "fill_dur": 0.5, "base_dur": 1.0},
   pill("Full price, £70: just 3 days", 960, 760, at=0.8, style="red"),
   {"t": "dots", "n": SIX_MONTHS, "cols": 26, "r": 11, "gap": 32, "x": 960, "y": 470, "shape": "sq", "hit_idx": [i for i in range(SIX_MONTHS) if i not in spread3], "hit_color": "cream", "base_dur": 0.01, "hit_delay": 0.1, "fill_dur": 1.4, "at": 1, "special": {str(i): "red" for i in spread3}},
   pill("Every other day: cheaper", 960, 850, at=1, d=0.3, style="cream"),
   text("Real saving? A lot less than half.", 960, 950, at=1.72, d=0, size=44, font="xb", color="red2"),
 ]},
 {"brand": True, "dur": 2.6, "els": [{"t": "logo", "x": 640, "y": 540, "r": 140, "tag": "The price tag never tells the whole story.", "at": 0, "d": 0.1}]},
 # ---------------- the question ----------------
 {"ids": [11, 11], "k": ("THE QUESTION", ""), "els": [
   {"t": "title", "txt": "Are Black Friday deals real?", "y": 470, "size": 88, "at": 0, "d": 0.2, "sub": "Or a discount on a price that never existed?", "sub_at": 0.62},
 ]},
 {"ids": [12, 12], "k": ("THE METHOD", "Receipts, not ads"), "els": [
   art("sale_sign", 560, 520, 360, d=0.1, anim="drop", out=0.28),
   {"t": "stamp", "txt": "NOT ADS", "x": 560, "y": 560, "size": 56, "rot": -10, "at": 0.15, "d": 0, "out": 0.3, "od": 0.4},
   {"t": "line", "x": 520, "y": 330, "w": 900, "h": 360, "pts": [6, 6, 7, 5, 8, 6, 6, 9, 4], "labels": ["JUN", "", "", "", "", "", "", "", "NOV"], "novals": True, "lo": 0, "hi": 10, "at": 0.35, "d": 0, "dur": 2.4},
   mono("PRICE HISTORIES", 970, 220, at=0.35, d=0, color="red2", size=22),
 ]},
 # ---------------- evidence ----------------
 {"ids": [21, 22], "k": ("THE EVIDENCE", "Which? · UK consumer group"), "src": WHICH, "els": [
   art("magnifier", 960, 470, 440, d=0.1, anim="pop", txt="£", out=1),
   {"t": "rows", "x": 1240, "y": 300, "w": 520, "title": "DAILY PRICE LOG", "rows": [["Day 1", "£"], ["Day 2", "£"], ["Day 3", "£"]], "at": 0, "d": 0.4, "stagger": 0.3, "out": 1},
   pill("Amazon", 600, 860, at=0.62, d=0, out=1), pill("Argos", 820, 860, at=0.66, d=0, out=1), pill("Currys", 1030, 860, at=0.71, d=0, out=1), pill("John Lewis", 1280, 860, at=0.76, d=0, out=1),
   {"t": "days", "items": [["MAY", ""], ["JUN", ""], ["JUL", ""], ["AUG", ""], ["SEP", ""], ["OCT", ""], ["NOV", "BF", "red"], ["DEC", ""], ["JAN", ""], ["FEB", ""], ["MAR", ""], ["APR", ""], ["MAY", ""]], "x": 960, "y": 560, "w": 110, "h": 120, "at": 1, "d": 0.1, "stagger": 0.1, "hot_delay": 0.0},
   mono("← 6 MONTHS BEFORE", 590, 680, at=1.4, d=0, color="grey"), mono("6 MONTHS AFTER →", 1330, 680, at=1.75, d=0, color="grey"),
 ]},
 {"ids": [23, 25], "k": ("BLACK FRIDAY 2022", "Which? tracked 208 discounted products"), "src": "Which? (UK), Nov 2023", "els": [
   {"t": "dots", "n": 208, "cols": 26, "r": 10, "gap": 30, "x": 640, "y": 500, "at": 0, "d": 0.1, "hit_idx": [17, 64, 103, 150, 190], "hit_at": 1.05, "fill_dur": 0.8, "base_dur": 1.2},
   {"t": "count", "from": 0, "to": 208, "fmt": "{:.0f}", "x": 1440, "y": 330, "size": 150, "color": "white", "sub": "DEALS TRACKED", "subfont": "mono", "subsize": 22, "subcolor": "grey", "at": 0.45, "d": 0},
   {"t": "count", "from": 0, "to": 5, "fmt": "{:.0f}", "x": 1440, "y": 640, "size": 150, "color": "red2", "sub": "CHEAPEST ON THE DAY", "subfont": "mono", "subsize": 22, "subcolor": "grey", "at": 1, "d": 0.1},
   pill("≈ 2 in every 100", 1440, 880, at=1.55, d=0, style="red", size=34),
   pill("The other 98: same price or cheaper at another time", 640, 960, at=2, d=0.1, size=26),
 ]},
 {"ids": [26, 27], "k": ("ONE EXAMPLE", "Wireless earbuds"), "src": "Which? (UK), Nov 2023", "els": [
   art("earbuds", 360, 540, 380, d=0.1, anim="drop"),
   {"t": "bars", "x": 1150, "y": 830, "h": 460, "vmax": 150, "bw": 200, "gap": 80, "at": 0, "d": 0.4, "stagger": 0.9,
    "items": [{"label": "BEFORE THE SALE", "v": 139, "txt": "£139", "color": "dim"}, {"label": "BLACK FRIDAY", "v": 119, "txt": "£119", "color": "red"}, {"label": "THE SUMMER BEFORE", "v": 109, "txt": "£99–109", "color": "cream", "vsize": 48}]},
   {"t": "pill", "txt": "The summer price was the real deal", "x": 1150, "y": 950, "at": 1, "d": 0.1, "style": "cream", "size": 30},
 ]},
 {"ids": [28, 28], "k": ("BLACK FRIDAY 2023", "Which? checked 227 deals"), "src": "Which? (UK), Nov 2024", "els": [
   {"t": "dots", "n": 100, "cols": 10, "r": 15, "gap": 42, "x": 600, "y": 540, "hit": 92, "at": 0, "d": 0.1, "hit_at": 0.55, "fill_dur": 1.5},
   {"t": "count", "from": 0, "to": 92, "fmt": "{:.0f}%", "x": 1360, "y": 470, "size": 230, "at": 0.55, "d": 0, "sub": "same price or cheaper\nat other times of the year", "subsize": 40},
 ]},
 {"ids": [29, 30], "k": ("BLACK FRIDAY 2024", "175 products · 8 retailers"), "src": "Which? (UK), Nov 2025", "els": [
   {"t": "dots", "n": 100, "cols": 10, "r": 15, "gap": 42, "x": 600, "y": 540, "hit": 83, "at": 0, "d": 0.1, "hit_at": 0.62, "fill_dur": 1.5},
   {"t": "count", "from": 0, "to": 83, "fmt": "{:.0f}%", "x": 1360, "y": 430, "size": 230, "at": 0.62, "d": 0, "sub": "same price or cheaper\noutside the sale", "subsize": 40},
   pill("Lowest only on Black Friday:  0", 1360, 830, at=1, d=0.2, style="red", size=36),
 ]},
 {"ids": [31, 32], "k": ("NEW ZEALAND", "Consumer NZ · 14 weeks of prices before the 2025 sales"), "src": "Consumer NZ, Nov 2025", "els": [
   {"t": "dots", "n": 100, "cols": 10, "r": 15, "gap": 42, "x": 600, "y": 540, "hit": 50, "at": 0, "d": 0.1, "hit_at": 0.6, "fill_dur": 1.2, "out": 1},
   {"t": "count", "from": 0, "to": 50, "fmt": "{:.0f}%", "x": 1360, "y": 430, "size": 230, "at": 0.6, "d": 0, "sub": "could have paid the same\nor less in the months before", "subsize": 40, "out": 1},
   art("blender", 470, 560, 400, at=1, d=0.35, anim="drop"),
   {"t": "bars", "x": 1250, "y": 820, "h": 440, "vmax": 110, "bw": 220, "gap": 120, "at": 1, "d": 0.45, "stagger": 0.8,
    "items": [{"label": "SEPTEMBER", "v": 70, "txt": "$70", "color": "cream"}, {"label": "THE SALE", "v": 100, "txt": "$100", "color": "red"}],
    "delta": {"txt": "+$30", "sub": "ON SALE", "pair": [0, 1]}, "delta_at": 1.6},
 ]},
 {"ids": [33, 33], "k": ("TO BE FAIR", "Retailers dispute some findings"), "src": "Which? (UK); Consumer NZ", "els": [
   pill("Amazon: Which? looked at only a small number of its products", 960, 330, at=0.1, d=0, size=30),
   {"t": "cards", "items": [["2022", "UK"], ["2023", "UK"], ["2024", "UK"], ["2025", "NZ"]], "x": 960, "y": 650, "w": 250, "h": 230, "at": 0.15, "d": 0, "stagger": 0.35},
 ]},
 # ---------------- trick 1 ----------------
 {"ids": [41, 41], "k": ("HOW A FAKE DEAL IS MADE", "Three main tricks"), "els": [
   {"t": "cards", "items": [[1, "The \"was\"\nprice"], [2, "The deal that\nnever ends"], [3, "The special\nmodel"]], "x": 960, "y": 540, "w": 340, "h": 340, "fs": 34, "at": 0, "d": 0, "stagger": 0.3},
 ]},
 {"ids": [42, 42], "k": ("TRICK 1 OF 3", "The \"was\" price"), "els": [
   {"t": "cards", "items": [[1, "The \"was\"\nprice"], [2, "The deal that\nnever ends"], [3, "The special\nmodel"]], "x": 960, "y": 540, "w": 300, "h": 300, "fs": 30, "at": 0, "d": 0, "stagger": 0.0, "hl": 0, "hl_t": 0.2, "out": 0.3},
   {"t": "tag", "txt": "£70", "small": "WAS · RRP", "x": 760, "y": 470, "w": 380, "at": 0.35, "d": 0},
   {"t": "arrow", "x0": 1180, "y0": 700, "x1": 920, "y1": 560, "at": 0.78, "d": 0},
   pill("THE ANCHOR", 1300, 720, at=0.78, d=0.2, style="red", size=38, font="xb"),
 ]},
 {"ids": [43, 43], "k": ("TRICK 1 OF 3", "What your brain compares"), "ex": True, "els": [
   {"t": "bars", "x": 860, "y": 820, "h": 480, "vmax": 75, "bw": 220, "gap": 140, "at": 0, "d": 0.2, "stagger": 0.6,
    "items": [{"label": "THE ANCHOR", "v": 70, "txt": "£70", "color": "dim"}, {"label": "SALE PRICE", "v": 35, "txt": "£35", "color": "red"}],
    "delta": {"txt": "−50%", "sub": "HOW IT FEELS", "pair": [0, 1]}, "delta_at": 0.3},
   pill("Higher anchor  →  better-feeling deal", 960, 960, at=0.62, d=0, style="cream"),
 ]},
 {"ids": [44, 44], "k": ("TRICK 1 OF 3", "6 months of toothbrush prices, one square per day"), "src": WHICH, "els": [
   art("toothbrush", 330, 540, 440, d=0.05, anim="drop"),
   {"t": "dots", "n": SIX_MONTHS, "cols": 26, "r": 10, "gap": 28, "x": 1160, "y": 500, "shape": "sq", "hit_idx": spread3, "at": 0, "d": 0.2, "hit_at": 0.4, "fill_dur": 0.4, "base_dur": 0.8},
   pill("3 days at £70  =  a £70 \"was\" price", 1160, 790, at=0.6, d=0, style="red"),
 ]},
 {"ids": [45, 46], "k": ("TRICK 1 OF 3", "A second toothbrush"), "src": WHICH, "els": [
   art("toothbrush", 330, 560, 440, d=0.05, anim="drop", color=[46, 150, 92, 255]),
   {"t": "tag", "txt": "£25", "small": "SAVE", "x": 520, "y": 330, "w": 220, "at": 0.15, "d": 0},
   text("RRP £50", 1160, 250, at=0.3, d=0, size=48, font="black", color="grey"),
   {"t": "dots", "n": SIX_MONTHS, "cols": 26, "r": 10, "gap": 28, "x": 1160, "y": 520, "shape": "sq", "hit_idx": spread13, "at": 0.4, "d": 0, "hit_at": 0.62, "fill_dur": 1.0, "base_dur": 0.8},
   pill("£50 on just 13 days in 6 months", 1160, 790, at=0.7, d=0, style="red"),
   art("sale_sign", 1640, 330, 220, at=1, d=0.2, anim="drop", bob=6),
   pill("= a whole season of sale signs", 1160, 880, at=1, d=0.4, style="cream"),
 ]},
 # ---------------- trick 2 ----------------
 {"ids": [51, 51], "k": ("TRICK 2 OF 3", "The deal that never ends"), "els": [
   art("countdown", 960, 470, 700, d=0.15, anim="pop", bob=5, txt="02:59:41", label="DEAL ENDS IN"),
   pill("Not inflated. Just not special.", 960, 860, at=0.55, d=0, style="cream", size=34),
 ]},
 {"ids": [52, 53], "k": ("TRICK 2 OF 3", "A cordless vacuum, one square per day"), "src": "Which? (UK), Nov 2025", "els": [
   art("stick_vacuum", 300, 560, 420, d=0.05, anim="drop"),
   {"t": "tag", "txt": "£349", "x": 470, "y": 330, "w": 240, "at": 0.15, "d": 0},
   {"t": "dots", "n": 71, "cols": 24, "r": 13, "gap": 36, "x": 1180, "y": 460, "shape": "sq", "hit_idx": [i for i in range(71) if i != 29], "special": {"29": "yel"}, "at": 0.4, "d": 0, "hit_at": 0.5, "fill_dur": 1.8, "base_dur": 0.6},
   mono("29 DAYS BEFORE · BLACK FRIDAY · 41 DAYS AFTER", 1180, 600, at=0.55, d=0.4),
   pill("Same £349 on all of them", 1180, 700, at=0.8, d=0, style="red"),
   art("countdown", 1180, 870, 330, at=1, d=0.1, anim="rise", txt="02:59:41", label="DEAL ENDS IN"),
   {"t": "stamp", "txt": "NOT URGENT", "x": 1500, "y": 880, "size": 44, "rot": -8, "at": 1, "d": 1.1},
 ]},
 {"ids": [54, 55], "k": ("TRICK 2 OF 3", "A robot vacuum's price"), "src": "Which? (UK), Nov 2025", "els": [
   art("robot_vacuum", 330, 580, 380, d=0.05, anim="slidel"),
   {"t": "line", "x": 760, "y": 300, "w": 1000, "h": 420, "pts": [299, 500, 350], "labels": ["MAY", "BEFORE THE SALE", "BLACK FRIDAY"], "cur": "£", "lo": 200, "hi": 560, "mark": 2,
    "ref": {"v": 299, "txt": "MAY"}, "at": 0.15, "d": 0, "dur_at": 0.9},
   pill("A discount from the peak, not the normal price", 1260, 960, at=1, d=0.1, style="red"),
 ]},
 # ---------------- trick 3 ----------------
 {"ids": [61, 62], "k": ("TRICK 3 OF 3", "The special model"), "src": "Illustration", "els": [
   art("tv", 560, 470, 480, d=0.2, anim="drop", txt="X100"),
   mono("THE FAMOUS MODEL", 560, 740, at=0, d=0.5),
   art("tv", 1360, 470, 480, at=1, d=1.5, anim="drop", txt="X100B"),
   mono("THE BLACK FRIDAY VERSION", 1360, 740, at=1, d=1.9, color="red2"),
   pill("Same product, new name?", 1360, 840, at=1.6, d=0, style="card"),
   pill("Built cheaper, to hit a price?", 1360, 930, at=1.78, d=0, style="red"),
 ]},
 {"ids": [63, 63], "k": ("BLACK FRIDAY TVs, 2015", "Two 58-inch sets, same brand"), "src": "NBC News, 2015", "els": [
   art("tv", 640, 520, 440, d=0.1, anim="drop", txt="58\"", out=0.5), art("tv", 1280, 520, 440, d=0.3, anim="drop", txt="58\"", out=0.5),
   mono("DIMMING ZONES", 960, 200, at=0.55, d=0, color="grey", size=24),
   {"t": "bars", "x": 960, "y": 820, "h": 480, "vmax": 34, "bw": 240, "gap": 200, "at": 0.55, "d": 0, "stagger": 0.9, "vsize": 80,
    "items": [{"label": "BLACK FRIDAY SET", "v": 10, "txt": "10", "color": "red"}, {"label": "HIGHER-END MODEL", "v": 32, "txt": "32", "color": "cream"}]},
 ]},
 {"ids": [64, 64], "k": ("TRICK 3 OF 3", "Searching a brand-new model number"), "src": "Illustration", "els": [
   {"t": "rows", "x": 560, "y": 300, "w": 800, "title": "PRICE HISTORY · MODEL X100B", "rows": [["One year ago", "—"], ["Six months ago", "—"], ["Last month", "—"]], "at": 0, "d": 0.2, "stagger": 0.35},
   {"t": "stamp", "txt": "NO HISTORY", "x": 1160, "y": 720, "size": 60, "rot": -8, "at": 0.45, "d": 0},
 ]},
 # ---------------- legal ----------------
 {"ids": [71, 71], "k": ("IS IT LEGAL?", "General information, not legal advice"), "els": [
   {"t": "title", "txt": "Is any of this legal?", "y": 470, "size": 92, "at": 0, "d": 0.15, "sub": "It depends where you shop.", "sub_t": 1.4},
 ]},
 {"ids": [72, 72], "k": ("UNITED STATES", "FTC Guides Against Deceptive Pricing"), "src": "16 CFR 233.1", "els": [
   {"t": "check", "x": 560, "y": 290, "w": 800, "title": "A \"WAS\" PRICE MUST BE...", "items": [["v", "A price it was really offered at"], ["v", "Offered regularly"], ["v", "For a reasonably substantial period"]], "at": 0.12, "d": 0, "items_delay": 5.6, "stagger": 1.6},
 ]},
 {"ids": [73, 73], "k": ("UNITED STATES", "The guide's own example"), "src": "16 CFR 233.1", "els": [
   {"t": "rows", "x": 360, "y": 300, "w": 900, "title": "FTC EXAMPLE · A PEN", "rows": [["Normally sells for", "$7.50"], ["Listed for a few days at", "$10.00"], ["Ad: \"Was $10, now only\"", "$7.50", "red"]], "at": 0.1, "d": 0, "stagger": 2.6, "rows_delay": 0.6},
   {"t": "stamp", "txt": "FICTITIOUS", "x": 1500, "y": 640, "size": 58, "rot": -10, "at": 0.8, "d": 0},
 ]},
 {"ids": [74, 75], "k": ("EUROPEAN UNION", "Price cuts must show the lowest price of the last 30 days"), "src": "EU Price Indication Directive, Art. 6a; CJEU case C-330/23", "els": [
   mono("THE 30 DAYS BEFORE A PRICE CUT", 960, 300, at=0, d=0.2, size=22),
   {"t": "dots", "n": 30, "cols": 30, "r": 18, "gap": 48, "x": 960, "y": 410, "shape": "sq", "hit_idx": [11], "at": 0, "d": 0.1, "hit_at": 0.75, "fill_dur": 0.2, "base_dur": 1.0},
   mono("LOWEST", 792, 470, at=0.75, d=0.2, color="red2"),
   pill("The % off must start from that lowest price", 960, 640, at=1, d=0.3, style="red", size=34),
   mono("EU COURT OF JUSTICE · 2024", 960, 720, at=1, d=0.6),
 ]},
 {"ids": [76, 76], "k": ("CANADA", "Competition Act · \"ordinary selling price\""), "src": "Competition Act (Canada), ordinary selling price tests", "els": [
   {"t": "check", "x": 510, "y": 320, "w": 900, "title": "A \"REGULAR\" PRICE ONLY COUNTS IF...", "items": [["v", "Enough units really sold at it"], ["v", "OR it was charged for a substantial time"]], "at": 0, "d": 0.1, "items_delay": 2.0, "stagger": 1.4},
 ]},
 {"ids": [77, 77], "k": ("THE CATCH", ""), "els": [
   art("magnifier", 640, 520, 400, d=0.2, anim="pop", txt="£"),
   art("countdown", 1280, 520, 520, at=0.6, d=0, anim="pop", txt="7 DAYS", label="SALE OVER IN"),
   pill("Rules exist. Checking millions of tags is hard.", 960, 900, at=0.3, d=0, style="cream"),
 ]},
 # ---------------- why it works ----------------
 {"ids": [81, 82], "k": ("WHY IT STILL WORKS", "US online spending"), "src": "Adobe Analytics via Nasdaq/RTTNews, Nov 2025", "els": [
   art("money_stack", 960, 470, 420, d=0.1, anim="pop", label="$", out=0.42),
   {"t": "count", "from": 0, "to": 11.8, "fmt": "${:.1f}B", "x": 960, "y": 420, "size": 230, "at": 0.45, "d": 0, "dur": 1.4, "sub": "Black Friday 2025, online. A record.", "subsize": 40, "out": 1},
   {"t": "count", "from": 0, "to": 8.2, "fmt": "${:.1f}B", "x": 960, "y": 420, "size": 230, "at": 1, "d": 0.5, "dur": 1.4, "sub": "through buy now, pay later · Nov 1–28", "subsize": 40},
 ]},
 {"ids": [83, 83], "k": ("WHY IT STILL WORKS", "Two ways to make a price feel smaller"), "ex": True, "els": [
   {"t": "tag", "txt": "£100", "small": "DEAL", "x": 560, "y": 500, "w": 380, "at": 0, "d": 0.2},
   {"t": "days", "items": [["1 OF 4", "£25"], ["2 OF 4", "£25"], ["3 OF 4", "£25"], ["4 OF 4", "£25"]], "x": 1300, "y": 500, "w": 140, "h": 150, "fs": 40, "at": 0.65, "d": 0, "stagger": 0.15},
   text("feels cheap", 560, 760, at=0.45, d=0.3, size=40, font="xb", color="grey"),
   text("feels cheaper", 1300, 760, at=0.7, d=0.3, size=40, font="xb", color="red2"),
 ]},
 # ---------------- one number ----------------
 {"ids": [91, 92], "k": ("THE ONE NUMBER", "Which?, Black Friday 2022"), "src": "Which? (UK), Nov 2023", "els": [
   {"t": "dots", "n": 100, "cols": 10, "r": 15, "gap": 42, "x": 600, "y": 520, "hit_idx": [33, 71], "at": 0, "d": 0.1, "hit_at": 0.3, "fill_dur": 0.4},
   {"t": "count", "from": 0, "to": 2, "fmt": "{:.0f}", "x": 1360, "y": 420, "size": 330, "at": 0.2, "d": 0, "sub": "in every 100 deals were really\nthe lowest price on the day", "subsize": 40},
   pill("Real bargains exist. They're just rare.", 960, 950, at=1, d=0.6, style="cream", size=34),
 ]},
 # ---------------- toolkit ----------------
 {"ids": [101, 101], "k": ("THE TOOLKIT", "5 checks before you buy"), "els": [
   {"t": "cards", "items": [[1, "Check the\nprice history"], [2, "Ignore the\n\"was\" price"], [3, "Search the\nmodel number"], [4, "Decide your\nprice now"], [5, "Check the\ntotal"]], "x": 960, "y": 540, "w": 300, "h": 330, "fs": 28, "at": 0, "d": 0.2, "stagger": 0.18},
 ]},
 {"ids": [102, 102], "k": ("CHECK 1 OF 5", "Check the price history"), "ex": True, "els": [
   pill("Keepa", 860, 220, at=0.15, d=0), pill("CamelCamelCamel", 1120, 220, at=0.2, d=0),
   {"t": "line", "x": 460, "y": 360, "w": 1000, "h": 360, "pts": [99, 99, 99, 99, 99, 99], "labels": ["MAY", "JUN", "JUL", "AUG", "OCT", "BF"], "cur": "$", "lo": 0, "hi": 160, "mark": 5, "at": 0, "d": 0.1, "dur_at": 0.75},
   pill("Same price all year? It's just the price.", 960, 950, at=0.8, d=0, style="red"),
 ]},
 {"ids": [103, 103], "k": ("CHECK 2 OF 5", "Ignore the \"was\" price"), "ex": True, "els": [
   {"t": "tag", "txt": "£70", "small": "WAS", "x": 620, "y": 480, "w": 380, "at": 0, "d": 0.2},
   {"t": "strike", "x0": 430, "y0": 560, "x1": 830, "y1": 400, "at": 0.25, "d": 0, "w": 14},
   {"t": "bars", "x": 1320, "y": 800, "h": 420, "vmax": 75, "bw": 170, "gap": 70, "at": 0.4, "d": 0, "stagger": 0.25,
    "items": [{"label": "JUL", "v": 39, "txt": "£39", "color": "cream"}, {"label": "SEP", "v": 39, "txt": "£39", "color": "cream"}, {"label": "BF", "v": 35, "txt": "£35", "color": "red"}]},
   mono("WHAT IT ACTUALLY SOLD FOR", 1320, 230, at=0.4, d=0.3, color="grey", size=22),
 ]},
 {"ids": [104, 104], "k": ("CHECK 3 OF 5", "Search the model number"), "ex": "Illustration", "els": [
   art("magnifier", 520, 520, 420, d=0.2, anim="pop", txt="#"),
   {"t": "rows", "x": 860, "y": 360, "w": 760, "title": "SEARCH RESULTS · MODEL X100B", "rows": [["Reviews", "0", "red"], ["Black Friday ads", "12"]], "at": 0.4, "d": 0, "stagger": 0.6},
   pill("Could be a special model", 1240, 760, at=0.75, d=0, style="red"),
 ]},
 {"ids": [105, 105], "k": ("CHECK 4 OF 5", "Decide your price now"), "ex": True, "els": [
   {"t": "rows", "x": 260, "y": 330, "w": 720, "title": "MY BLACK FRIDAY LIST", "rows": [["Headphones", "£80 max"], ["Air fryer", "£60 max"]], "at": 0, "d": 0, "stagger": 0.5},
   pill("Sale hits it  →  buy", 1380, 470, at=0.72, d=0, style="cream", size=34),
   pill("It doesn't  →  walk away", 1380, 600, at=0.86, d=0, style="red", size=34),
 ]},
 {"ids": [106, 106], "k": ("CHECK 5 OF 5", "Check the total before you pay"), "ex": True, "els": [
   {"t": "rows", "x": 600, "y": 240, "w": 720, "title": "CHECKOUT", "rows": [["Sale price", "$99.00"], ["Service fee", "+$12.00", "redval"], ["Shipping", "+$7.00", "redval"]], "total": ["TOTAL", "$118.00"], "at": 0.2, "d": 0, "stagger": 0.5},
 ]},
 # ---------------- next ----------------
 {"ids": [111, 111], "k": ("NEXT CASE", "This Friday · on Black Friday itself"), "ex": True, "els": [
   art("hotel_bell", 460, 520, 360, d=0.2, anim="drop"),
   {"t": "rows", "x": 820, "y": 260, "w": 760, "title": "ONE NIGHT · $150 ADVERTISED", "rows": [["Room", "$150"], ["Resort fee", "+$35", "redval"], ["Service fee", "+$25", "redval"]], "total": ["AT CHECKOUT", "$210"], "at": 0.1, "d": 0, "stagger": 0.45, "rows_delay": 0.5},
 ]},
 {"ids": [112, 112], "k": ("YOUR TURN", ""), "els": [
   {"t": "title", "txt": "Your best Black Friday deal?", "y": 450, "size": 86, "at": 0.2, "d": 0, "sub": "Was it real?", "sub_at": 0.75, "sub2": "Tell me in the comments", "sub2_at": 0.8},
 ]},
 {"ids": [113, 113], "els": [{"t": "logo", "x": 640, "y": 540, "r": 140, "tag": "The price tag never tells the whole story.", "at": 0, "d": 0.1}]},
]

END = {"hold": 14, "els": [
  {"t": "logo", "x": 190, "y": 250, "r": 80, "at": 0, "d": 0.1},
  mono("NEXT CASE", 110, 760, at=0, d=0.5, color="red2", size=22, anchor="lm"),
  text("Hidden fees: the price you see\nvs the price you pay", 110, 800, at=0, d=0.6, size=46, font="xb", anchor="la", align="left"),
  {"t": "box", "x0": 1040, "y0": 180, "x1": 1820, "y1": 620, "at": 0, "d": 0.3},
  {"t": "box", "x0": 1040, "y0": 680, "x1": 1820, "y1": 960, "at": 0, "d": 0.4},
]}
