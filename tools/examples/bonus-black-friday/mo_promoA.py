import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mo_shorts import PROMO_A as SCENES
LINES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out2/thecostnerd-bonus-bf2-promoA-lines.json")
GAP = 0.25; SCENE_GAP = 0.2; MUSIC_VOL = 0.14
SRT = {1: "This robot vacuum was on sale for Black Friday, for £350.", 2: "Here's the problem. In May, the exact same vacuum cost £299. So the Black Friday deal was £50 more than in May.", 3: "How does that work? Before the sale, the price climbed to £500. Then it dropped to £350, and got a sale sign. A discount from the peak, not from the normal price."}
