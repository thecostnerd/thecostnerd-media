LINES = "./thecostnerd-bonus-bf-main-lines.json"

CHAPTERS = {1: "The \"half price\" toothbrush", 21: "Are Black Friday deals real?", 31: "The evidence: years of price tracking",
            61: "Trick 1: the \"was\" price", 81: "Trick 2: the deal that never ends", 91: "Trick 3: the special model",
            111: "Is it legal?", 131: "Why it still works", 141: "The one number", 151: "What to do before you buy", 171: "Next: hidden fees"}

def tag(txt, small=None, color=None, rot=-10, s=0.8, x=0.5, y=0.5, delay=None):
    a = {"txt": txt, "rot": rot}
    if small: a["small"] = small
    if color: a["color"] = color
    d = {"f": "price_tag", "s": s, "x": x, "y": y, "args": a}
    if delay is not None: d["delay"] = delay
    return d

def o(f, s=0.8, x=0.5, y=0.5, rot=0, **args):
    return {"f": f, "s": s, "x": x, "y": y, "rot": rot, "args": args}

LIGHT = [255, 252, 244, 255]; GREEN = [46, 150, 92, 255]; BLUE = [64, 110, 214, 255]; RED = [216, 38, 30, 255]

SCENES = [
 # cold open
 {"ids": [1, 1], "head": "This toothbrush was on sale for Black Friday", "hl": ["sale"], "art": [o("toothbrush", 0.9, 0.38), o("sale_sign", 0.5, 0.74, 0.3)]},
 {"ids": [2, 3], "head": "\"Save £35.\" Was £70. Now £35.", "hl": ["£35."], "bg": "cream", "art": [tag("£35", "NOW", LIGHT, s=0.95)]},
 {"ids": [4, 4], "head": "Half price. Who says no?", "hl": ["Half"], "bg": "red", "art": [o("bag", 0.85, txt="50%")]},
 {"ids": [5, 7], "head": "Full price of £70 lasted…", "hl": ["£70"], "sub": "in the six months before the sale", "count": {"from": 0, "to": 3, "fmt": "{:.0f} DAYS", "size": 230}},
 {"ids": [8, 8], "head": "Every other day, it cost less", "hl": ["less"], "bg": "cream", "art": [o("toothbrush", 0.8, 0.35, rot=8), o("stamp", 0.6, 0.68, 0.45, txt="LESS")]},
 {"ids": [9, 9], "head": "So how much did you really save?", "hl": ["really"], "art": [o("question", 0.85)]},
 {"ids": [10, 10], "head": "A lot less than half", "hl": ["less"], "bg": "yellow", "center": True},
 # the question
 {"ids": [21, 22], "head": "Are Black Friday deals real?", "hl": ["real?"], "art": [o("sale_sign", 0.75, 0.4), o("question", 0.5, 0.78, 0.65)]},
 {"ids": [23, 23], "head": "Or a discount on a price that never existed?", "hl": ["never"], "bg": "cream", "art": [tag("£??", "WAS", s=0.9)]},
 {"ids": [24, 25], "head": "Not ads. Price histories.", "hl": ["Price", "histories."], "art": [o("receipt", 0.85, 0.4, title="PRICE LOG", rows=[["DAY 1", "✓"], ["DAY 2", "✓"]], total=["DAY 180", "✓"]), o("magnifier", 0.5, 0.75, 0.6, txt="£")]},
 # the evidence
 {"ids": [31, 31], "head": "Which? tracked the prices", "hl": ["tracked"], "sub": "UK consumer group", "art": [o("flag_card", 0.8, txt="UK", color=BLUE)], "src": "Source: Which? (UK) Black Friday investigations, 2022–2025"},
 {"ids": [32, 33], "head": "Every day. Six months before, six months after.", "hl": ["Every", "day."], "sub": "Amazon · Argos · Currys · John Lewis and more", "art": [o("calendar", 0.85, top="MONTHS", big="6+6")]},
 {"ids": [34, 35], "head": "Black Friday 2022: deals tracked", "hl": ["2022:"], "bg": "cream", "count": {"from": 0, "to": 208, "fmt": "{:.0f}", "dur": 1.2}},
 {"ids": [36, 36], "head": "Cheapest on Black Friday itself", "hl": ["Cheapest"], "count": {"from": 208, "to": 5, "fmt": "{:.0f}", "dur": 1.2}},
 {"ids": [37, 38], "head": "That's about 2 in every 100", "hl": ["2"], "bg": "yellow", "sub": "The other 98 were the same price or cheaper at some other point", "count": {"from": 0, "to": 2, "fmt": "{:.0f}%", "size": 380}},
 {"ids": [39, 39], "head": "Earbuds: £139 → £119 for Black Friday", "hl": ["£119"], "art": [o("earbuds", 0.75, 0.35), tag("£119", "BF DEAL", s=0.6, x=0.72, y=0.7, rot=8)]},
 {"ids": [40, 41], "head": "The summer price was the real deal", "hl": ["summer"], "bg": "cream", "art": [o("receipt", 0.95, title="EARBUDS", rows=[["SUMMER", "£99-109"], ["BEFORE BF", "£139"]], total=["BF DEAL", "£119"])]},
 {"ids": [42, 43], "head": "2023: same price or cheaper at other times", "hl": ["2023:"], "sub": "227 deals checked", "count": {"from": 0, "to": 92, "fmt": "{:.0f}%"}},
 {"ids": [44, 45], "head": "2024: same price or cheaper outside the sale", "hl": ["2024:"], "sub": "175 products · 8 retailers", "bg": "cream", "count": {"from": 0, "to": 83, "fmt": "{:.0f}%"}},
 {"ids": [46, 46], "head": "Lowest only on Black Friday: not one", "hl": ["not", "one"], "bg": "red", "art": [o("stamp", 0.9, txt="ZERO")]},
 {"ids": [47, 48], "head": "Not just Britain. New Zealand too.", "hl": ["New", "Zealand"], "sub": "Consumer NZ tracked prices for 14 weeks", "art": [o("flag_card", 0.6, 0.3, 0.4, txt="UK", color=BLUE), o("flag_card", 0.6, 0.7, 0.6, txt="NZ", color=GREEN)], "src": "Source: Consumer NZ, Nov 2025"},
 {"ids": [49, 49], "head": "Half could've been bought for the same or less, earlier", "hl": ["Half"], "bg": "cream", "art": [o("pie", 0.85, frac=0.5, label="½")]},
 {"ids": [50, 50], "head": "A blender: $70 in September. $100 in the sale.", "hl": ["$100"], "art": [o("blender", 0.7, 0.3), o("receipt", 0.7, 0.72, title="BLENDER", rows=[["SEPT", "$69.99"]], total=["SALE", "$99.99"])], "src": "Source: Consumer NZ, Nov 2025"},
 {"ids": [51, 52], "head": "Some retailers disagree. The pattern keeps showing up.", "hl": ["pattern"], "bg": "cream", "art": [o("calendar", 0.55, 0.3, 0.35, top="WHICH?", big="2022"), o("calendar", 0.55, 0.7, 0.65, top="CONSUMER NZ", big="2025")]},
 # trick 1
 {"ids": [61, 61], "head": "How a fake deal gets made", "hl": ["fake"], "bg": "yellow", "sub": "three main tricks", "count": {"from": 0, "to": 3, "fmt": "{:.0f}", "size": 420}},
 {"ids": [62, 64], "head": "Trick 1: the \"was\" price", "hl": ["\"was\""], "sub": "Every discount needs an anchor", "art": [tag("£70", "WAS", LIGHT, s=0.85)]},
 {"ids": [65, 66], "head": "Your brain compares the sale to the anchor", "hl": ["anchor"], "bg": "cream", "sub": "Not to what it usually sells for", "art": [o("brain", 0.8)]},
 {"ids": [67, 67], "head": "Full price for three days = a \"was\" price", "hl": ["three", "days"], "art": [o("toothbrush", 0.75, 0.3), o("calendar", 0.6, 0.72, top="DAYS AT £70", big="3")]},
 {"ids": [68, 68], "head": "Toothbrush #2: \"Save £25.\" RRP £50.", "hl": ["£25."], "bg": "cream", "art": [o("toothbrush", 0.75, 0.3, color=GREEN), tag("£25", "SAVE", s=0.6, x=0.72, y=0.6, rot=8)]},
 {"ids": [69, 70], "head": "13 days of full price buys a season of sale signs", "hl": ["13", "days"], "art": [o("calendar", 0.6, 0.3, 0.45, top="DAYS AT £50", big="13"), o("sale_sign", 0.55, 0.72, 0.6)]},
 # trick 2
 {"ids": [81, 82], "head": "Trick 2: the deal that never ends", "hl": ["never"], "bg": "red", "sub": "Not inflated. Just not special.", "art": [o("countdown", 0.95)]},
 {"ids": [83, 83], "head": "Cordless vacuum: £349 on Black Friday", "hl": ["£349"], "art": [o("stick_vacuum", 0.8, 0.35), tag("£349", s=0.55, x=0.72, y=0.6)]},
 {"ids": [84, 84], "head": "Same price, 70 days around the sale", "hl": ["Same", "price,"], "bg": "cream", "art": [o("calendar", 0.55, 0.28, top="DAYS BEFORE", big="29"), o("calendar", 0.55, 0.72, top="DAYS AFTER", big="41")]},
 {"ids": [85, 85], "head": "Nothing urgent. Except the clock.", "hl": ["clock."], "art": [o("countdown", 0.95)]},
 {"ids": [86, 86], "head": "A robot vacuum: £299 in May", "hl": ["£299"], "bg": "cream", "art": [o("robot_vacuum", 0.75, 0.35), tag("£299", "MAY", s=0.55, x=0.72, y=0.65)]},
 {"ids": [87, 88], "head": "Black Friday \"deal\": £350", "hl": ["£350"], "sub": "Before the sale, it climbed to £500", "art": [o("price_history", 0.95, pts=[[0, 299], [1, 500], [2, 350]], labels=["MAY", "BEFORE", "BF"], lo=200, mark=2)]},
 {"ids": [89, 89], "head": "A discount from the peak, not the normal price", "hl": ["peak,"], "bg": "yellow", "art": [o("price_history", 0.95, pts=[[0, 299], [1, 500], [2, 350]], labels=["MAY", "BEFORE", "BF"], lo=200, mark=1)]},
 # trick 3
 {"ids": [91, 92], "head": "Trick 3: the special model", "hl": ["special"], "bg": "red", "art": [o("tv", 0.9, txt="BF")]},
 {"ids": [93, 94], "head": "Made for Black Friday. A slightly different model number.", "hl": ["model", "number."], "art": [o("tv", 0.6, 0.3, 0.35, txt="X100"), o("tv", 0.6, 0.7, 0.65, txt="X100B")]},
 {"ids": [95, 96], "head": "Same product, new name. Or built cheaper.", "hl": ["cheaper."], "bg": "cream", "art": [o("stamp", 0.85, txt="CHEAP")]},
 {"ids": [97, 97], "head": "2015: reviewers warned about Black Friday TVs", "hl": ["2015:"], "art": [o("calendar", 0.85, top="REVIEWERS", big="2015")], "src": "Source: NBC News, 2015"},
 {"ids": [98, 98], "head": "58-inch: 10 dimming zones vs 32", "hl": ["10"], "bg": "cream", "art": [o("tv", 0.6, 0.3, 0.35, txt="10", sub="ZONES"), o("tv", 0.6, 0.7, 0.65, txt="32", sub="ZONES")]},
 {"ids": [99, 100], "head": "New model = no price history", "hl": ["no", "price", "history"], "sub": "Normally, it doesn't exist", "art": [o("magnifier", 0.85, txt="???")]},
 # legal
 {"ids": [111, 111], "head": "Is any of this legal?", "hl": ["legal?"], "bg": "yellow", "art": [o("gavel", 0.85)]},
 {"ids": [112, 113], "head": "US: a \"was\" price must be real and regular", "hl": ["real", "regular"], "sub": "Offered for a reasonably substantial period", "art": [o("scroll_paper", 0.85, title="FTC GUIDES")], "src": "Source: FTC Guides Against Deceptive Pricing, 16 CFR 233.1"},
 {"ids": [114, 115], "head": "The guide's own example", "hl": ["example"], "bg": "cream", "art": [o("receipt", 0.95, title="PEN", rows=[["NORMALLY", "$7.50"], ["A FEW DAYS", "$10"]], total=["SALE!", "$7.50"])]},
 {"ids": [116, 116], "head": "A fictitious former price", "hl": ["fictitious"], "bg": "red", "art": [o("stamp", 0.9, txt="FAKE")]},
 {"ids": [117, 118], "head": "EU: show the lowest price from the last 30 days", "hl": ["lowest"], "art": [o("flag_card", 0.55, 0.3, 0.4, txt="EU", color=BLUE), o("calendar", 0.55, 0.72, 0.6, top="LAST", big="30")], "src": "Source: Price Indication Directive, Art. 6a"},
 {"ids": [119, 119], "head": "2024: the % off must start from that lowest price", "hl": ["lowest"], "bg": "cream", "sub": "EU Court of Justice, case C-330/23", "art": [o("gavel", 0.85)]},
 {"ids": [120, 120], "head": "Canada: real sales, or a real length of time", "hl": ["real"], "art": [o("flag_card", 0.8, txt="CA", color=RED)], "src": "Source: Competition Act, ordinary selling price tests"},
 {"ids": [121, 121], "head": "The rules exist. Checking millions of tags is hard.", "hl": ["hard."], "bg": "cream", "art": [o("magnifier", 0.6, 0.35, 0.4, txt="£"), o("countdown", 0.6, 0.68, 0.7, txt="7 DAYS", label="SALE OVER IN")]},
 # why it works
 {"ids": [131, 132], "head": "Black Friday 2025, US online", "hl": ["2025,"], "sub": "A record, says Adobe Analytics", "count": {"from": 0, "to": 11.8, "fmt": "${:.1f}B", "dur": 1.2}, "src": "Source: Adobe Analytics via Nasdaq, Nov 2025"},
 {"ids": [133, 133], "head": "Through buy now, pay later in November", "hl": ["buy", "now,"], "bg": "cream", "sub": "Nov 1–28, US online", "count": {"from": 0, "to": 8.2, "fmt": "${:.1f}B", "dur": 1.2}},
 {"ids": [134, 135], "head": "The deal feels cheap. The plan feels cheaper.", "hl": ["cheaper."], "bg": "red", "art": [o("card_statement", 0.85)]},
 # one number
 {"ids": [141, 143], "head": "The number to remember", "hl": ["remember"], "bg": "yellow", "sub": "of every 100 deals were really the lowest price on the day (Which?, 2022)", "count": {"from": 0, "to": 2, "fmt": "{:.0f}", "size": 460}},
 {"ids": [144, 145], "head": "Real bargains exist. They're just rarer than the signs say.", "hl": ["rarer"], "art": [o("trophy", 0.8)]},
 # what to do
 {"ids": [151, 151], "head": "Before you buy anything this Black Friday", "hl": ["Before"], "bg": "yellow", "sub": "5 checks", "center": True},
 {"ids": [152, 154], "head": "1. Check the price history", "hl": ["price", "history"], "sub": "Free trackers: Keepa, CamelCamelCamel for Amazon", "art": [o("price_history", 0.95, pts=[[0, 99], [1, 99], [2, 99], [3, 99]], labels=["MAR", "JUN", "SEP", "BF"], cur="$", lo=0, hi=160, mark=3)], "src": "Example prices"},
 {"ids": [155, 156], "head": "2. Ignore the \"was\" price", "hl": ["Ignore"], "bg": "cream", "sub": "Compare with what it actually sold for", "art": [o("scissors_coupon", 0.85)]},
 {"ids": [157, 158], "head": "3. Search the model number", "hl": ["model", "number"], "sub": "Only Black Friday ads, no reviews? Could be a special model.", "art": [o("magnifier", 0.85, txt="#")]},
 {"ids": [159, 160], "head": "4. Decide your price now", "hl": ["now"], "bg": "cream", "sub": "The sale hits it: buy. It doesn't: walk away.", "art": [o("scroll_paper", 0.85, title="MY PRICE")]},
 {"ids": [161, 162], "head": "5. Check the total before you pay", "hl": ["total"], "art": [o("receipt", 0.95, title="CHECKOUT", rows=[["Item", "$99"], ["Fees", "+$19"]], total=["TOTAL", "$118"])], "src": "Example prices"},
 # next
 {"ids": [171, 173], "head": "Next: the price you see vs the price you pay", "hl": ["pay"], "bg": "red", "art": [o("hotel_bell", 0.55, 0.3, 0.35), o("receipt", 0.8, 0.68, 0.55, rows=[["Room", "$150"], ["Fees", "+$60"]], total=["TOTAL", "$210"])], "src": "Example prices"},
 {"ids": [174, 174], "head": "This Friday. On Black Friday itself.", "hl": ["Black", "Friday"], "bg": "yellow", "art": [o("calendar", 0.85, top="NOV · FRIDAY", big="27")]},
 {"ids": [175, 175], "head": "Best Black Friday deal you ever got? Was it real?", "hl": ["real?"], "sub": "Tell me in the comments", "art": [o("question", 0.85)]},
 {"ids": [176, 177], "head": "The price tag never tells the whole story", "hl": ["whole", "story"], "center": True},
]

END = {"end": ["THE COST NERD", "New investigation every Friday", "SUBSCRIBE"], "watch_next": "WATCH NEXT", "hold": 14, "bg": "ink"}

SRT = {3: 'Was £70. Now £35.', 39: 'One pair of wireless earbuds was cut from £139 to £119 for Black Friday.', 40: 'For much of the summer before, it had cost between £99 and £109.', 50: 'One blender was $70 in September, and $100 during the sale.', 68: 'The same store had a second toothbrush. Save £25, it said. Recommended price, £50.', 87: 'Its Black Friday deal price was £350.', 88: 'Before the sale, its price had climbed to £500.', 98: 'One 58-inch set had 10 dimming zones. A higher-end model from the same brand had 32.', 115: 'A pen normally sells for $7.50. The store lists it at $10 for a few days, then advertises a bargain, from $10 down to $7.50.', 132: 'On Black Friday 2025, Americans spent a record $11.8 billion online, according to Adobe Analytics.', 133: 'In the first four weeks of November, $8.2 billion of online spending went through buy now, pay later.', 143: 'Out of every 100 Black Friday deals Which? tracked in 2022, 2 were actually the lowest price of the year on the day.'}
