"""Flat, bold-outline illustrations for The Cost Nerd. No brand logos.
Every function draws on a square RGBA canvas of size S (supersampled 2x then downscaled)."""
import math
from PIL import Image, ImageDraw, ImageFont

INK = (24, 22, 20, 255); CREAM = (244, 238, 226, 255); RED = (216, 38, 30, 255)
YEL = (247, 196, 49, 255); MUST = (232, 168, 36, 255); BUN = (226, 160, 92, 255); SAUS = (178, 62, 44, 255)
BLUE = (64, 110, 214, 255); GREEN = (46, 150, 92, 255); KRAFT = (196, 142, 84, 255); KRAFT2 = (170, 116, 62, 255)
GREY = (120, 116, 108, 255); LIGHT = (255, 252, 244, 255); BROWN = (92, 52, 30, 255); SILVER = (200, 200, 196, 255)
FD = "/usr/share/fonts/opentype/inter/"
BLACK = FD + "InterDisplay-Black.otf"; XB = FD + "Inter-ExtraBold.otf"; SB = FD + "Inter-SemiBold.otf"
MONOB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
K = 2  # supersample


def F(p, s): return ImageFont.truetype(p, int(s))


class C:
    """Canvas helper in a 0..1000 coordinate space."""
    def __init__(self, S=700):
        self.S = S; self.n = S * K
        self.im = Image.new("RGBA", (self.n, self.n), (0, 0, 0, 0)); self.d = ImageDraw.Draw(self.im)
        self.u = self.n / 1000

    def p(self, *xy): return [v * self.u for v in xy]
    def w(self, v): return max(1, int(v * self.u))

    def rect(self, x0, y0, x1, y1, fill, r=0, ow=12, outline=INK, shadow=True):
        if shadow:
            self.d.rounded_rectangle(self.p(x0 + 14, y0 + 14, x1 + 14, y1 + 14), radius=self.w(r), fill=INK)
        self.d.rounded_rectangle(self.p(x0, y0, x1, y1), radius=self.w(r), fill=fill, outline=outline, width=self.w(ow))

    def ell(self, x0, y0, x1, y1, fill, ow=12, shadow=True):
        if shadow: self.d.ellipse(self.p(x0 + 14, y0 + 14, x1 + 14, y1 + 14), fill=INK)
        self.d.ellipse(self.p(x0, y0, x1, y1), fill=fill, outline=INK, width=self.w(ow))

    def poly(self, pts, fill, ow=12, shadow=True):
        if shadow: self.d.polygon([(x * self.u + 14 * self.u, y * self.u + 14 * self.u) for x, y in pts], fill=INK)
        self.d.polygon([(x * self.u, y * self.u) for x, y in pts], fill=fill, outline=INK, width=self.w(ow))

    def line(self, pts, fill=INK, w=12):
        self.d.line([(x * self.u, y * self.u) for x, y in pts], fill=fill, width=self.w(w), joint="curve")

    def text(self, x, y, s, size, fill=INK, font=BLACK, anchor="mm"):
        self.d.text((x * self.u, y * self.u), s, font=F(font, size * self.u), fill=fill, anchor=anchor)

    def done(self):
        return self.im.resize((self.S, self.S), Image.LANCZOS)


# ---------------- objects ----------------

def hotdog(S=700):
    c = C(S)
    c.ell(110, 420, 890, 700, BUN)                     # bottom bun
    c.rect(80, 380, 920, 520, SAUS, r=70)               # sausage
    c.line([(150, 440), (230, 470), (310, 430), (390, 470), (470, 430), (550, 470), (630, 430), (710, 470), (790, 435), (850, 460)], MUST, 26)
    c.poly([(140, 470), (860, 470), (820, 600), (180, 600)], BUN, shadow=False)
    c.line([(180, 600), (820, 600)], INK, 12)
    return c.done()


def soda_cup(S=700, label="", color=RED):
    c = C(S)
    c.line([(560, 60), (520, 260)], INK, 30); c.line([(560, 60), (520, 260)], RED, 16)   # straw
    c.poly([(260, 240), (740, 240), (680, 930), (320, 930)], color)
    c.rect(220, 200, 780, 280, LIGHT, r=30)
    c.d.rectangle(c.p(300, 470, 700, 640), fill=LIGHT)
    if label: c.text(500, 555, label, 120, INK)
    return c.done()


def price_tag(S=700, txt="$1.50", color=YEL, tcol=INK, rot=-12, small=None):
    c = C(S)
    pts = [(130, 300), (650, 300), (880, 500), (650, 700), (130, 700)]
    c.poly(pts, color)
    c.ell(660, 465, 730, 535, LIGHT, ow=10, shadow=False)
    size = 230 if len(txt) <= 4 else (190 if len(txt) <= 5 else 150)
    c.text(390, 500 if not small else 470, txt, size, tcol)
    if small: c.text(390, 620, small, 60, tcol, XB)
    im = c.done()
    return im.rotate(rot, resample=Image.BICUBIC, expand=False)


def calendar(S=700, top="SINCE", big="1985", color=RED):
    c = C(S)
    c.rect(150, 180, 850, 860, LIGHT, r=40)
    c.d.rounded_rectangle(c.p(150, 180, 850, 380), radius=c.w(40), fill=color, outline=INK, width=c.w(12))
    c.d.rectangle(c.p(156, 330, 844, 380), fill=color)
    c.line([(150, 380), (850, 380)], INK, 12)
    for x in (320, 680):
        c.rect(x - 25, 120, x + 25, 250, GREY, r=20, shadow=False)
    c.text(500, 285, top, 90, LIGHT)
    c.text(500, 620, big, 230, INK)
    return c.done()


def member_card(S=700, color=BLUE):
    c = C(S)
    c.rect(90, 270, 910, 760, color, r=60)
    c.d.rectangle(c.p(96, 360, 904, 440), fill=INK)
    c.rect(160, 520, 320, 640, YEL, r=20, shadow=False)
    c.text(620, 560, "MEMBER", 90, LIGHT)
    c.line([(470, 650), (820, 650)], LIGHT, 18)
    return c.done()


def money_stack(S=700, label="$5.3B"):
    c = C(S)
    for i, y in enumerate((700, 610, 520, 430)):
        c.rect(150, y, 850, y + 110, GREEN, r=20, shadow=(i == 0))
        c.ell(440, y + 20, 560, y + 90, (120, 200, 150, 255), ow=8, shadow=False)
    c.rect(200, 200, 800, 380, YEL, r=40)
    c.text(500, 290, label, 150, INK)
    return c.done()


def pie(S=700, frac=0.66, label="⅔"):
    c = C(S)
    c.ell(130, 130, 870, 870, LIGHT)
    c.d.pieslice(c.p(130, 130, 870, 870), -90, -90 + 360 * frac, fill=RED, outline=INK, width=c.w(12))
    c.d.ellipse(c.p(130, 130, 870, 870), outline=INK, width=c.w(12))
    c.text(560, 600, label, 200, LIGHT)
    return c.done()


def box(S=700):
    c = C(S)
    c.poly([(150, 380), (500, 250), (850, 380), (500, 510)], KRAFT)
    c.poly([(150, 380), (500, 510), (500, 900), (150, 770)], KRAFT2)
    c.poly([(850, 380), (500, 510), (500, 900), (850, 770)], KRAFT)
    c.poly([(330, 315), (680, 445), (680, 560), (620, 540), (620, 470), (330, 360)], (230, 210, 170, 255), ow=8, shadow=False)
    return c.done()


def maze(S=700):
    c = C(S)
    c.rect(100, 100, 900, 900, LIGHT, r=30)
    walls = [[(100, 250), (750, 250)], [(250, 250), (250, 750)], [(250, 750), (750, 750)], [(750, 400), (750, 900)],
             [(400, 400), (750, 400)], [(400, 400), (400, 600)], [(400, 600), (600, 600)], [(600, 520), (600, 600)],
             [(900, 250), (900, 250)]]
    for wl in walls: c.line(wl, INK, 26)
    c.line([(160, 180), (850, 180), (850, 320), (330, 320), (330, 680), (680, 680), (680, 470), (500, 470), (500, 530)], RED, 18)
    c.ell(470, 500, 530, 560, RED, ow=6, shadow=False)
    c.rect(780, 800, 900, 900, GREEN, r=0, ow=0, outline=None, shadow=False)
    c.text(840, 850, "?", 80, LIGHT)
    return c.done()


def cancel_button(S=700):
    c = C(S)
    c.rect(100, 330, 900, 590, LIGHT, r=60)
    c.text(500, 460, "CANCEL", 150, GREY)
    c.poly([(640, 520), (640, 860), (720, 780), (780, 900), (830, 875), (770, 755), (880, 750)], LIGHT)
    return c.done()


def gavel(S=700):
    c = C(S)
    c.rect(150, 760, 850, 860, KRAFT2, r=20)
    hd = C(S)
    hd.rect(300, 150, 760, 330, BROWN, r=40)
    hd.rect(250, 140, 330, 340, KRAFT, r=20, shadow=False); hd.rect(730, 140, 810, 340, KRAFT, r=20, shadow=False)
    hd.rect(500, 320, 560, 720, KRAFT, r=20)
    h = hd.done().rotate(28, resample=Image.BICUBIC, center=(S * 0.55, S * 0.4))
    out = c.done(); out.alpha_composite(h); return out


def scroll_paper(S=700, title="CONTRACT", lines=4):
    c = C(S)
    c.rect(200, 120, 800, 880, LIGHT, r=30)
    c.text(500, 230, title, 80, INK)
    for i in range(lines):
        c.line([(280, 340 + i * 90), (720, 340 + i * 90)], GREY, 16)
    c.line([(520, 760), (560, 720), (600, 780), (660, 720), (720, 770)], BLUE, 12)
    c.text(400, 770, "∞", 140, RED)
    return c.done()


def brain(S=700):
    c = C(S)
    c.ell(170, 230, 830, 800, (240, 160, 170, 255))
    c.line([(500, 250), (480, 400), (520, 520), (490, 650), (500, 790)], INK, 12)
    for pts in ([(300, 380), (380, 330), (440, 400)], [(250, 560), (340, 500), (420, 560)], [(580, 360), (660, 320), (740, 400)],
                [(570, 560), (660, 500), (760, 570)], [(320, 700), (420, 650)], [(600, 690), (700, 660)]):
        c.line(pts, INK, 10)
    return c.done()


def sale_sign(S=700, txt="SALE"):
    c = C(S)
    c.line([(500, 80), (300, 300)], INK, 10); c.line([(500, 80), (700, 300)], INK, 10)
    c.ell(470, 60, 530, 120, GREY, ow=6, shadow=False)
    c.rect(150, 290, 850, 760, RED, r=30)
    c.text(500, 525, txt, 230, LIGHT)
    return c.done()


def hotel_bell(S=700):
    c = C(S)
    c.rect(130, 720, 870, 800, INK, r=20)
    c.d.pieslice(c.p(180, 320, 820, 1120), 180, 360, fill=YEL, outline=INK, width=c.w(12))
    c.line([(180, 720), (820, 720)], INK, 12)
    c.rect(470, 240, 530, 330, SILVER, r=10)
    c.ell(430, 200, 570, 270, SILVER, ow=10)
    c.line([(300, 560), (360, 470)], LIGHT, 24)
    return c.done()


def receipt(S=700, rows=(("Room", "$89"), ("Resort fee", "+$35")), total=("TOTAL", "$124"), title="RECEIPT"):
    c = C(S)
    top, bot = 80, 880
    c.rect(220, top, 780, bot, LIGHT, r=0)
    for x in range(220, 781, 56):
        c.d.polygon(c.p(x, bot, x + 28, bot + 34, x + 56, bot), fill=LIGHT)
    c.text(500, top + 80, title, 60, INK, MONOB)
    y = top + 190
    for l, r in rows:
        c.text(270, y, l, 50, INK, MONOB, anchor="lm"); c.text(730, y, r, 50, RED if r.startswith("+") else INK, MONOB, anchor="rm"); y += 90
    c.line([(270, y), (730, y)], GREY, 8); y += 80
    c.text(270, y, total[0], 64, INK, MONOB, anchor="lm"); c.text(730, y, total[1], 64, RED, MONOB, anchor="rm")
    return c.done()


def ticket(S=700, txt="$10M"):
    c = C(S)
    c.rect(100, 300, 900, 700, YEL, r=30)
    c.ell(60, 450, 160, 550, (0, 0, 0, 0), shadow=False)
    c.d.ellipse(c.p(60, 450, 160, 550), fill=(0, 0, 0, 0))
    c.line([(320, 320), (320, 680)], INK, 8)
    c.text(210, 500, "ADMIT", 50, INK, XB) if False else None
    c.text(610, 500, txt, 210, RED)
    c.text(210, 500, "★", 140, INK)
    return c.done()


def stamp(S=700, txt="FINED", color=RED):
    c = C(S)
    c.d.rounded_rectangle(c.p(100, 330, 900, 670), radius=c.w(30), outline=color, width=c.w(36))
    c.text(500, 500, txt, 220, color)
    return c.done().rotate(-14, resample=Image.BICUBIC)


def bag(S=700, color=RED, txt=""):
    c = C(S)
    c.d.arc(c.p(330, 120, 670, 480), 180, 360, fill=INK, width=c.w(30))
    c.poly([(200, 300), (800, 300), (850, 880), (150, 880)], color)
    if txt: c.text(500, 600, txt, 150, LIGHT)
    return c.done()


def scissors_coupon(S=700):
    c = C(S)
    c.d.rectangle(c.p(120, 260, 880, 740), outline=INK, width=c.w(12), fill=LIGHT)
    for x in range(120, 880, 60): c.line([(x, 250), (x + 30, 250)], INK, 10)
    c.text(500, 430, "COUPON", 120, INK)
    c.text(500, 600, "20% OFF", 110, RED)
    c.line([(140, 170), (860, 830)], RED, 50); c.line([(860, 170), (140, 830)], RED, 50)
    return c.done()


def chart_down(S=700, a="$17.3B", b="$13.0B"):
    c = C(S)
    c.rect(80, 80, 920, 920, LIGHT, r=30)
    c.rect(200, 300, 420, 820, BLUE, r=10, shadow=False)
    c.rect(580, 470, 800, 820, RED, r=10, shadow=False)
    c.line([(140, 820), (860, 820)], INK, 14)
    c.text(310, 240, a, 70, INK); c.text(690, 410, b, 70, RED)
    c.text(310, 875, "2011", 50, GREY, XB); c.text(690, 875, "2012", 50, GREY, XB)
    return c.done()


def exit_door(S=700):
    c = C(S)
    c.rect(260, 150, 740, 900, KRAFT, r=10)
    c.ell(640, 520, 690, 570, YEL, ow=8, shadow=False)
    c.rect(300, 40, 700, 130, GREEN, r=10)
    c.text(500, 85, "EXIT", 70, LIGHT)
    return c.done()


def trophy(S=700):
    c = C(S)
    c.rect(330, 780, 670, 880, BROWN, r=10)
    c.rect(450, 600, 550, 790, YEL, r=0)
    c.d.arc(c.p(150, 220, 380, 500), 90, 270, fill=INK, width=c.w(24))
    c.d.arc(c.p(620, 220, 850, 500), 270, 90, fill=INK, width=c.w(24))
    c.d.chord(c.p(250, 50, 750, 700), 0, 180, fill=YEL, outline=INK, width=c.w(12))
    c.d.rectangle(c.p(250, 180, 750, 380), fill=YEL); c.line([(250, 180), (250, 380)], INK, 12); c.line([(750, 180), (750, 380)], INK, 12)
    c.line([(250, 180), (750, 180)], INK, 12)
    c.text(500, 360, "★", 160, LIGHT)
    return c.done()


def bottle(S=700, label="5¢"):
    c = C(S)
    pts = [(440, 80), (560, 80), (560, 260), (650, 420), (650, 900), (350, 900), (350, 420), (440, 260)]
    c.poly(pts, (74, 40, 30, 255))
    c.rect(420, 50, 580, 110, SILVER, r=10)
    c.rect(350, 500, 650, 700, RED, r=0)
    c.text(500, 600, label, 120, LIGHT)
    c.line([(400, 760), (400, 860)], (255, 255, 255, 120), 18)
    return c.done()


def coin(S=700, txt="5¢"):
    c = C(S)
    c.ell(150, 150, 850, 850, SILVER)
    c.ell(220, 220, 780, 780, (225, 225, 220, 255), ow=8, shadow=False)
    c.text(500, 510, txt, 260, INK)
    return c.done()


def billboard(S=700, l1="DRINK", l2="5 CENTS"):
    c = C(S)
    c.rect(300, 640, 360, 920, GREY, r=0); c.rect(640, 640, 700, 920, GREY, r=0)
    c.rect(80, 200, 920, 660, RED, r=20)
    c.text(500, 340, l1, 120, LIGHT)
    c.text(500, 510, l2, 150, YEL)
    return c.done()


def vending(S=700):
    c = C(S)
    c.rect(220, 70, 780, 930, RED, r=30)
    c.rect(280, 140, 580, 700, (40, 40, 44, 255), r=10)
    for i in range(3):
        for j in range(2):
            c.rect(310 + j * 130, 180 + i * 170, 410 + j * 130, 300 + i * 170, (74, 40, 30, 255), r=10, ow=6, shadow=False)
    c.rect(620, 220, 730, 300, LIGHT, r=10, ow=8)
    c.line([(650, 260), (700, 260)], INK, 14)
    c.text(675, 380, "5¢", 80, LIGHT)
    c.rect(300, 760, 700, 860, (40, 40, 44, 255), r=10)
    return c.done()


def chips_bag(S=700, scale=1.0, txt="CHIPS", color=YEL):
    c = C(S)
    s = scale
    cx = 500; w = 300 * s; h = 400 * s; cy = 520
    pts = [(cx - w, cy - h), (cx + w, cy - h), (cx + w * 0.92, cy + h), (cx - w * 0.92, cy + h)]
    c.poly(pts, color)
    for x in range(int(cx - w), int(cx + w), 40):
        c.line([(x, cy - h - 10), (x + 20, cy - h + 20)], INK, 8)
    c.text(cx, cy - 40 * s, txt, 120 * s, RED)
    c.text(cx, cy + 180 * s, "NET WT", 50 * s, INK, XB)
    return c.done()


def magnifier(S=700, txt="10 oz"):
    c = C(S)
    c.line([(640, 640), (880, 880)], INK, 70); c.line([(640, 640), (880, 880)], BROWN, 46)
    c.ell(140, 140, 700, 700, (220, 236, 245, 255), ow=26)
    c.text(420, 420, txt, 130, RED)
    return c.done()


def toilet_roll(S=700):
    c = C(S)
    c.rect(220, 200, 700, 820, LIGHT, r=10)
    c.ell(600, 200, 800, 820, LIGHT)
    c.ell(660, 440, 740, 580, GREY, ow=8, shadow=False)
    c.line([(300, 820), (300, 920), (420, 900)], INK, 10)
    return c.done()


def arrow(S=700, color=RED, direction="right"):
    c = C(S)
    pts = [(120, 400), (580, 400), (580, 250), (880, 500), (580, 750), (580, 600), (120, 600)]
    c.poly(pts, color)
    im = c.done()
    return im.rotate({"right": 0, "down": -90, "up": 90}[direction], resample=Image.BICUBIC)


def question(S=700):
    c = C(S)
    c.ell(120, 120, 880, 880, YEL)
    c.text(500, 520, "?", 520, INK)
    return c.done()


def card_statement(S=700):
    c = C(S)
    c.rect(170, 80, 830, 920, LIGHT, r=20)
    c.text(500, 170, "STATEMENT", 64, INK, MONOB)
    items = [("STREAMING", "$15.49"), ("MUSIC", "$11.99"), ("PRIME", "$14.99"), ("GYM", "$29.99"), ("??? APP", "$9.99")]
    y = 300
    for i, (a, b) in enumerate(items):
        col = RED if i == 4 else INK
        c.text(230, y, a, 46, col, MONOB, anchor="lm"); c.text(770, y, b, 46, col, MONOB, anchor="rm"); y += 110
    c.d.ellipse(c.p(200, 690, 800, 790), outline=RED, width=c.w(12))
    return c.done()


ART = {k: v for k, v in globals().items() if callable(v) and k not in ("F", "C") and not k.startswith("_")}


if __name__ == "__main__":
    names = ["hotdog", "soda_cup", "price_tag", "calendar", "member_card", "money_stack", "pie", "box", "maze", "cancel_button",
             "gavel", "scroll_paper", "brain", "sale_sign", "hotel_bell", "receipt", "ticket", "stamp", "bag", "scissors_coupon",
             "chart_down", "exit_door", "trophy", "bottle", "coin", "billboard", "vending", "chips_bag", "magnifier", "toilet_roll",
             "arrow", "question", "card_statement"]
    cols = 7; S = 300
    sheet = Image.new("RGBA", (cols * S, math.ceil(len(names) / cols) * S), (40, 40, 40, 255))
    for i, n in enumerate(names):
        im = ART[n](S)
        sheet.alpha_composite(im, ((i % cols) * S, (i // cols) * S))
    sheet.convert("RGB").save("artsheet.png")
    print("ok")


def gas_sign(S=700, price="3.49", frac="9/10"):
    c = C(S)
    c.rect(440, 700, 560, 960, GREY, r=0)
    c.rect(150, 90, 850, 720, (30, 30, 34, 255), r=30)
    c.rect(150, 90, 850, 230, RED, r=30)
    c.d.rectangle(c.p(156, 190, 844, 230), fill=RED)
    c.text(500, 160, "GAS", 100, LIGHT)
    c.text(440, 440, "$" + price, 165, YEL)
    c.text(755, 370, frac, 70, YEL)
    c.text(500, 620, "REGULAR", 60, SILVER, XB)
    return c.done()


def catalog(S=700):
    c = C(S)
    c.rect(210, 90, 790, 910, LIGHT, r=10)
    c.d.rectangle(c.p(216, 96, 784, 230), fill=RED)
    c.text(500, 165, "CATALOG", 90, LIGHT)
    # dress silhouette
    c.poly([(440, 300), (560, 300), (590, 420), (680, 760), (320, 760), (410, 420)], BLUE)
    c.line([(440, 300), (420, 260)], INK, 10); c.line([(560, 300), (580, 260)], INK, 10)
    c.rect(560, 640, 760, 760, YEL, r=10, ow=8)
    c.text(660, 700, "$??", 70, INK)
    c.text(500, 840, "Same item, 3 versions", 44, GREY, XB)
    return c.done()


def left_digit(S=700, a=("$4", "9"), b=("$5", "0")):
    c = C(S)
    for i, (big, rest) in enumerate((a, b)):
        y0 = 160 + i * 380
        c.rect(120, y0, 880, y0 + 290, LIGHT if i else YEL, r=30)
        sz = 230 if len(big) <= 2 else 170
        split = 600 if len(big) <= 2 else 660
        c.text(split, y0 + 145, big, sz, RED if i == 0 else INK, anchor="rm")
        c.text(split + 10, y0 + 145, rest, sz, (160, 150, 130, 255), anchor="lm")
    return c.done()


ART.update({"gas_sign": gas_sign, "catalog": catalog, "left_digit": left_digit})
