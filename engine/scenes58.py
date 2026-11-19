"""'What Do You Want For Dinner?' - original, general-audience comedy short, 22s.
Hook: Mom ECU, twitching glare, spatula up: "WHAT DO YOU WANT FOR DINNER?!" -> Dad + kid on the sofa shrug in unison: "ANYTHING!"
Beat 1-3 (rapid fire, faster each time): "PASTA?" -> kid "Eww. NO." *BZZT* red X; "TACOS?" -> Dad "Had it LAST WEEK." X;
 "SOUP?" -> split screen both "Too... SOUPY." X.
Beat 4: Mom ECU "FINE." -> kitchen super-speed blur: she cooks EVERYTHING -> low angle food mountain "TA-DA!"
Twist: kid + Dad dwarfed by the mountain: "...can we just get PIZZA?" -> Mom's ears whistle steam like a kettle -> creepy calm "Sure, sweetie."
 -> Mom alone on the sofa with a whole pizza "Just for ME." -> "You said... ANYTHING." -> 1 HOUR LATER: stuffed round Dad + kid,
 Mom sweetly: "So... what do you want for BREAKFAST?" -> weak "...anything?" -> opening glare (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos, zigs, sofa_back, sofa_front, SEAT
from scenes48 import label1, label2
import scenes13
from scenes13 import card as _card13
import random

BOY = dict(doodle.BOY, hood=False, shirt=hx('ff5fa8'), pants=hx('3d5aff'))
MOM = dict(doodle.MOM_G, shirt=hx('22b45a'), pants=hx('3d5a9e'))
DAD = dict(doodle.DAD, shirt=hx('ffc93c'))
N = 660
FLOOR = 1460
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
GOLD = hx('ffc93c')
WHITE = (1, 1, 1)

CAPS = {
    'p1': [[("THE HARDEST QUESTION", OUT)], [("IN EVERY HOME", RED)]],
    'p2': [[("\"ANYTHING\" MEANS...", OUT)], [("NOT THAT.", BLUE)]],
    'p3': [[("MOM'S", OUT)], [("FINAL FORM", ORANGE)]],
    'p4': [[("THEN THEY SAID", OUT)], [("THE WORST THING", RED)]],
    'p5': [[("MOM'S", OUT)], [("SWEET REVENGE", PURPLE)]],
    'p6': [[("1 HOUR LATER...", PURPLE)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ food props
def plate(ctx, x, y, s=1.0, col=(1, 1, 1)):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 170, 60); fl(ctx, col, 7)
    ellipse(ctx, 0, -4, 120, 40); setc(ctx, dark(col, 0.92) if col != (1, 1, 1) else hx('e6ecf5')); ctx.fill()
    ctx.restore()


def pasta(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    plate(ctx, 0, 30)
    ctx.move_to(-120, 20); ctx.curve_to(-120, -110, 120, -110, 120, 20); ctx.close_path(); fl(ctx, hx('ffd86a'), 6)
    setc(ctx, hx('e0a92a')); ctx.set_line_width(5)
    for k in range(6):
        ctx.new_path(); ctx.arc(-70 + k * 28, -20 + (k % 2) * 16, 26, math.pi * 0.9, math.pi * 2.2); ctx.stroke()
    ctx.move_to(-80, -40); ctx.curve_to(-60, -100, 70, -100, 85, -40); ctx.curve_to(40, -20, -40, -20, -80, -40); fl(ctx, hx('e8342e'), 5)
    for mx, my in ((-30, -62), (30, -66)):
        ellipse(ctx, mx, my, 24, 22); fl(ctx, hx('8a4a2a'), 5)
    ctx.move_to(10, -90); ctx.line_to(20, -110); setc(ctx, GREEN); ctx.set_line_width(10); ctx.stroke()
    ctx.restore()


def taco(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    plate(ctx, 0, 40)
    for dx in (-60, 60):
        ctx.save(); ctx.translate(dx, 0)
        # fillings poke out the top
        for k, col in enumerate((hx('6fd84a'), hx('e8342e'), hx('ffd23f'), hx('6fd84a'))):
            ellipse(ctx, -50 + k * 33, -70 + (k % 2) * 8, 26, 20); fl(ctx, col, 4)
        ctx.new_path(); ctx.arc(0, -20, 90, math.pi * 0.05, math.pi * 0.95); ctx.close_path(); fl(ctx, hx('f5b83a'), 6)
        ctx.new_path(); ctx.arc(0, -20, 90, math.pi * 0.05, math.pi * 0.95); ctx.close_path()
        ctx.restore()
    ctx.restore()


def soup(ctx, x, y, s=1.0, a=0.0, lf=0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    plate(ctx, 0, 50)
    ctx.move_to(-140, -30); ctx.curve_to(-140, 70, 140, 70, 140, -30); ctx.close_path(); fl(ctx, hx('1f8bff'), 7)
    ellipse(ctx, 0, -30, 140, 34); fl(ctx, hx('ff9a3a'), 6)
    for cx_, cy_ in ((-60, -32), (10, -26), (60, -36)):
        ellipse(ctx, cx_, cy_, 14, 8); setc(ctx, hx('ffd23f')); ctx.fill()
    for k in range(3):
        ph = lf * 0.2 + k * 2
        ctx.move_to(-50 + k * 50, -70); ctx.curve_to(-70 + k * 50 + 20 * math.sin(ph), -120, -30 + k * 50, -150, -50 + k * 50 + 20 * math.sin(ph + 1), -200)
        setc(ctx, (1, 1, 1, 0.85)); ctx.set_line_width(12); ctx.stroke()
    ctx.restore()


def pizza(ctx, x, y, s=1.0, a=0.0, box=False, slices=8):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if box:
        rect_r(ctx, -230, -150, 460, 300, 16); fl(ctx, hx('e9c79a'), 8)
        rect_r(ctx, -205, -125, 410, 250, 10); setc(ctx, hx('d8b07e')); ctx.fill()
    ctx.save(); ctx.scale(1, 0.62)
    ellipse(ctx, 0, 0, 190, 190); fl(ctx, hx('f2a640'), 8)
    ellipse(ctx, 0, 0, 160, 160); fl(ctx, hx('ffd23f'), 5)
    rnd = random.Random(3)
    for k in range(10):
        ang = rnd.uniform(0, 6.28); d = rnd.uniform(30, 130)
        ellipse(ctx, math.cos(ang) * d, math.sin(ang) * d, 22, 22); fl(ctx, hx('e8342e'), 4)
    ink(ctx, 4)
    for k in range(4):
        ang = k * math.pi / 4
        ctx.move_to(math.cos(ang) * 160, math.sin(ang) * 160); ctx.line_to(-math.cos(ang) * 160, -math.sin(ang) * 160)
    ctx.stroke()
    ctx.restore()
    ctx.restore()


def salad(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    for dx, dy, col in ((-70, -40, hx('3aa52e')), (60, -50, hx('6fd84a')), (0, -80, hx('3aa52e')), (-20, -30, hx('6fd84a'))):
        ellipse(ctx, dx, dy, 60, 40); fl(ctx, col, 5)
    for dx, dy in ((-40, -70), (40, -40)):
        ellipse(ctx, dx, dy, 18, 18); fl(ctx, hx('e8342e'), 4)
    ctx.move_to(-130, -20); ctx.curve_to(-130, 80, 130, 80, 130, -20); ctx.close_path(); fl(ctx, hx('ff5fa8'), 7)
    ctx.restore()


def burger(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -110, 20, 220, 40, 18); fl(ctx, hx('f2b85a'), 6)
    rect_r(ctx, -115, -10, 230, 34, 14); fl(ctx, hx('8a4a2a'), 6)
    ctx.move_to(-120, -12)
    for i in range(7):
        ctx.line_to(-120 + i * 40 + 20, 10 if i % 2 else -24)
    ctx.line_to(125, -12); ctx.close_path(); fl(ctx, hx('6fd84a'), 5)
    poly(ctx, [(-100, -24), (100, -24), (80, 0), (60, -10), (40, 4), (-100, -10)]); fl(ctx, hx('ffd23f'), 4)
    ctx.move_to(-110, -24); ctx.curve_to(-110, -120, 110, -120, 110, -24); ctx.close_path(); fl(ctx, hx('f2b85a'), 6)
    for sx, sy in ((-50, -70), (0, -84), (50, -68)):
        ellipse(ctx, sx, sy, 8, 4); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.restore()


def drumstick(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(30, 0); ctx.line_to(120, 0); setc(ctx, INK); ctx.set_line_width(36); ctx.stroke()
    ctx.move_to(30, 0); ctx.line_to(120, 0); setc(ctx, hx('fff6e6')); ctx.set_line_width(22); ctx.stroke()
    for dy in (-16, 16):
        ellipse(ctx, 128, dy, 20, 18); fl(ctx, hx('fff6e6'), 5)
    ellipse(ctx, -20, 0, 90, 64); fl(ctx, hx('c8702a'), 7)
    ellipse(ctx, -40, -24, 30, 12); setc(ctx, hx('e8a050')); ctx.fill()
    ctx.restore()


def cake(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -130, -60, 260, 120, 20); fl(ctx, hx('ff9ac8'), 7)
    ctx.move_to(-130, -40)
    for i in range(7):
        ctx.curve_to(-130 + i * 37 + 10, 10, -130 + i * 37 + 27, 10, -130 + (i + 1) * 37, -40)
    ctx.line_to(130, -60); ctx.line_to(-130, -60); ctx.close_path(); fl(ctx, (1, 1, 1), 5)
    ellipse(ctx, 0, -84, 26, 26); fl(ctx, hx('e8342e'), 5)
    ctx.restore()


DISHES = (pasta, taco, soup, burger, salad, drumstick, cake, pizza)


def food_mountain(ctx, x, base, h=1.0, lf=0, rows=6, sp=1.0):
    """stack of plates of everything; grows with h (0..1)"""
    rnd = random.Random(21)
    rows_ = [(0, -190, 3), (1, -150, 3), (2, -110, 3), (3, -80, 2), (4, -40, 2), (5, 0, 1)]
    k = 0
    tot = sum(r[2] for r in rows_[:rows])
    for ri, spread, cnt in rows_[:rows]:
        for c in range(cnt):
            if k >= tot * h:
                return
            fx = x + (c - (cnt - 1) / 2) * 330 * sp * (1 - ri * 0.09)
            fy = base - ri * 190
            fn = DISHES[(k * 3 + ri) % len(DISHES)]
            a = rnd.uniform(-0.1, 0.1)
            if fn is soup:
                fn(ctx, fx, fy, 0.95, a, lf)
            else:
                fn(ctx, fx, fy, 0.95, a)
            k += 1


def x_stamp(ctx, x, y, t, s=1.0):
    if t <= 0:
        return
    sc = s * (2.2 - 1.2 * eout(min(1, t)))
    ctx.save(); ctx.translate(x, y); ctx.scale(sc, sc); ctx.rotate(0.08)
    for a in (math.pi / 4, -math.pi / 4):
        ctx.save(); ctx.rotate(a)
        rect_r(ctx, -190, -38, 380, 76, 30); fl(ctx, RED, 10)
        ctx.restore()
    ctx.restore()


def spatula(ctx, x, y, a=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(0, 0); ctx.line_to(0, 260); setc(ctx, INK); ctx.set_line_width(40); ctx.stroke()
    ctx.move_to(0, 0); ctx.line_to(0, 260); setc(ctx, hx('a8642e')); ctx.set_line_width(24); ctx.stroke()
    rect_r(ctx, -70, -150, 140, 150, 20); fl(ctx, hx('c0c6d6'), 8)
    for dx in (-30, 0, 30):
        rect_r(ctx, dx - 7, -125, 14, 90, 7); setc(ctx, hx('6a7088')); ctx.fill()
    ctx.restore()


def fork(ctx, x, y, a=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(0, 0); ctx.line_to(0, 200); setc(ctx, INK); ctx.set_line_width(28); ctx.stroke()
    ctx.move_to(0, 0); ctx.line_to(0, 200); setc(ctx, hx('dfe3ee')); ctx.set_line_width(14); ctx.stroke()
    for dx in (-24, -8, 8, 24):
        ctx.move_to(dx, 0); ctx.line_to(dx, -70); setc(ctx, INK); ctx.set_line_width(14); ctx.stroke()
        ctx.move_to(dx, 0); ctx.line_to(dx, -70); setc(ctx, hx('dfe3ee')); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def arm_to(ctx, x0, y0, x1, y1, col, skin, bend=80, w=80):
    mx, my = (x0 + x1) / 2 + bend, (y0 + y1) / 2 + bend * 0.4
    for c, ww in ((INK, w + 18), (col, w)):
        ctx.move_to(x0, y0); ctx.curve_to(mx, my, mx, my, x1, y1); setc(ctx, c); ctx.set_line_width(ww); ctx.stroke()
    ellipse(ctx, x1, y1, w * 0.5, w * 0.5); fl(ctx, skin, 7)


def steam_jets(ctx, cx, cy, R, lf, power=1.0):
    for sx in (-1, 1):
        ex = cx + sx * 1.0 * R
        for k in range(6):
            t = ((lf * 0.09 + k / 6.0) % 1.0)
            d = 80 + 520 * t
            x = ex + sx * d; y = cy + 0.1 * R - 160 * t
            r = (40 + 90 * t) * power
            ellipse(ctx, x, y, r, r * 0.8); setc(ctx, (1, 1, 1, 0.9 * (1 - t))); ctx.fill()
        poly(ctx, [(ex, cy + 0.02 * R), (ex + sx * 140, cy - 40), (ex + sx * 140, cy + 60)]); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()


def sweat(ctx, x, y, lf, s=1.0):
    y_ = y + ((lf * 3) % 120)
    ctx.move_to(x, y_ - 40 * s); ctx.curve_to(x + 26 * s, y_, x + 20 * s, y_ + 26 * s, x, y_ + 26 * s)
    ctx.curve_to(x - 20 * s, y_ + 26 * s, x - 26 * s, y_, x, y_ - 40 * s); fl(ctx, hx('5ac8ff'), 5)


def twitch(ctx, x, y, lf, s=1.0):
    if (lf // 3) % 2 == 0:
        for a in (-0.6, 0, 0.6):
            ctx.move_to(x + math.cos(a - 1.57) * 30 * s, y + math.sin(a - 1.57) * 30 * s)
            ctx.line_to(x + math.cos(a - 1.57) * 70 * s, y + math.sin(a - 1.57) * 70 * s)
        ink(ctx, 9); ctx.stroke()


# ------------------------------------------------------------------ sets
def dining(ctx, wall=hx('ffd9a8')):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, wall); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 130, -3000, 50, 6000); setc(ctx, dark(wall, 0.95)); ctx.fill()
    # window with evening sky
    rect_r(ctx, 640, 540, 320, 360, 12); fl(ctx, hx('ff9a5a'), 9)
    ellipse(ctx, 860, 640, 44, 44); setc(ctx, hx('fff2b0')); ctx.fill()
    ctx.move_to(800, 540); ctx.line_to(800, 900); ink(ctx, 7); ctx.stroke()
    ctx.move_to(640, 720); ctx.line_to(960, 720); ink(ctx, 7); ctx.stroke()
    # clock
    ellipse(ctx, 230, 680, 90, 90); fl(ctx, (1, 1, 1), 8)
    ctx.move_to(230, 680); ctx.line_to(230, 615); ink(ctx, 8); ctx.stroke()
    ctx.move_to(230, 680); ctx.line_to(275, 700); ink(ctx, 8); ctx.stroke()
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('b97a48')); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()


TABLE = 1180


def table_front(ctx, x0=60, x1=1020, y=TABLE):
    ctx.rectangle(x0, y, x1 - x0, 60); fl(ctx, hx('ffffff'), 8)
    # checker cloth band
    for i in range(int((x1 - x0) / 60)):
        if i % 2 == 0:
            ctx.rectangle(x0 + i * 60, y + 60, 60, 120); setc(ctx, RED); ctx.fill()
        else:
            ctx.rectangle(x0 + i * 60, y + 60, 60, 120); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.rectangle(x0, y + 60, x1 - x0, 120); ink(ctx, 8); ctx.stroke()
    for x in (x0 + 60, x1 - 100):
        ctx.rectangle(x, y + 180, 40, FLOOR - y - 180); fl(ctx, hx('8a4a2a'), 6)


def kitchen(ctx):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('c8f0e8')); ctx.fill()
    for j in range(10):
        ctx.move_to(-3000, 700 + j * 60); ctx.line_to(4000, 700 + j * 60)
    setc(ctx, hx('a8e0d6')); ctx.set_line_width(4); ctx.stroke()
    for x0 in (-200, 160, 720):
        rect_r(ctx, x0, 380, 320, 260, 12); fl(ctx, hx('ffb36b'), 7)
        ellipse(ctx, x0 + 160, 600, 12, 12); fl(ctx, GOLD, 3)
    # hood + stove
    poly(ctx, [(500, 380), (700, 380), (760, 560), (440, 560)]); fl(ctx, hx('c0c6d6'), 7)
    ctx.rectangle(-3000, 1240, 7000, 40); fl(ctx, (1, 1, 1), 7)
    ctx.rectangle(-3000, 1280, 7000, 300); setc(ctx, hx('1f8bff')); ctx.fill()
    for i in range(-10, 14):
        rect_r(ctx, i * 200 + 20, 1310, 160, 220, 10); fl(ctx, hx('4aa2ff'), 5)
    ctx.rectangle(-3000, 1580, 7000, 1500); setc(ctx, hx('f0e0c8')); ctx.fill()
    ctx.move_to(-3000, 1580); ctx.line_to(4000, 1580); ink(ctx, 7); ctx.stroke()


def pan(ctx, x, y, a=0.0, s=1.0, fire=0, lf=0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if fire:
        for k in range(5):
            fx = -80 + k * 40; fh = 60 + 30 * math.sin(lf * 1.3 + k)
            ctx.move_to(fx - 20, 60); ctx.curve_to(fx - 20, 60 - fh, fx + 20, 60 - fh, fx + 20, 60); ctx.close_path(); fl(ctx, ORANGE, 4)
    ctx.move_to(130, 0); ctx.line_to(300, -10); setc(ctx, INK); ctx.set_line_width(36); ctx.stroke()
    ctx.move_to(130, 0); ctx.line_to(300, -10); setc(ctx, hx('2a2a3a')); ctx.set_line_width(20); ctx.stroke()
    ctx.move_to(-140, -10); ctx.line_to(140, -10); ctx.line_to(110, 40); ctx.line_to(-110, 40); ctx.close_path(); fl(ctx, hx('3a3a4a'), 7)
    ctx.restore()


# ------------------------------------------------------------------ opening face
def opening_face(ctx, f, lf, lab=True):
    bob = 10 * math.sin(lf * 0.9)
    ctx.save(); cam(ctx, 540, 960, 1.04 + 0.05 * eout(pop(lf, 0, 40)), -3 + 1.5 * math.sin(lf * 0.6), 6, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8a5a')); ctx.fill()
    rays(ctx, 540, 960, 260, 1700, lf * 0.05, col=(1, 0.85, 0.5), a=0.55, n=18)
    cx, cy, R = 520, 980 + bob, 300
    # arm + spatula raised at right
    arm_to(ctx, cx + 230, cy + 420, 860, 820, MOM['shirt'], MOM['skin'], bend=60, w=90)
    spatula(ctx, 860, 770, 0.25 + 0.12 * math.sin(lf * 1.4), 1.1)
    face(ctx, MOM, P(eye='glare', mouth='scream', head=0), cx, cy, R, 0.03 * math.sin(lf * 1.2))
    twitch(ctx, cx + 0.42 * R, cy - 0.45 * R, lf, 1.3)
    ctx.restore()
    if lab:
        label2(ctx, "\"WHAT DO YOU WANT", "FOR DINNER?!\"", (1, 1, 1), 1.0, 104, col2=YEL, y=1400)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 45:
        opening_face(ctx, f, f)
    else:
        lf = f - 45
        # wide living room: Dad + kid on the sofa shrug in unison
        sh = eout(pop(lf, 4, 10)) * (1 - 0.6 * pop(lf, 30, 40))
        ctx.save(); cam(ctx, 510, 1140, 1.32, 0, shake_at(lf, [4], 8, 10), f)
        ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('8fe0d6')); ctx.fill()
        for i in range(-30, 40):
            ctx.rectangle(i * 120, -3000, 46, 6000); setc(ctx, hx('82d4ca')); ctx.fill()
        ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('c98a52')); ctx.fill()
        ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()
        sofa_back(ctx)
        arms = dict(lsh=-120 * sh, lel=-60 * sh - 15, rsh=-120 * sh, rel=-60 * sh - 15)
        draw(ctx, 330, SEAT - 186 * 1.3 + 60, 1.3, 1, DAD, P(eye='closed' if sh > 0.5 else 'normal', mouth='smile', lhip=-80, lkn=80, rhip=-80, rkn=80, **arms))
        draw(ctx, 680, SEAT - 186 * 1.05 + 50, 1.05, -1, BOY, P(eye='closed' if sh > 0.5 else 'normal', mouth='grin', lhip=-80, lkn=80, rhip=-80, rkn=80, **arms))
        sofa_front(ctx)
        ctx.restore()
        label1(ctx, "\"ANYTHING!\"", YEL, pop(lf, 4, 8), 150, -0.04, y=1420)
    card(ctx, 'p1', f, -6, 86)


OPTIONS = [
    ('"PASTA?"', pasta, 'boy', '"Eww. NO."'),
    ('"TACOS?"', taco, 'dad', '"Had it LAST WEEK."'),
    ('"SOUP?"', soup, 'both', '"Too... SOUPY."'),
]


def s2(ctx, f):
    lf = f - 90
    bi = min(2, lf // 36)
    ml = lf - bi * 36
    name, dish, who, reply = OPTIONS[bi]
    MS = 14 - bi * 2     # Mom's shot gets shorter each time (escalation)
    if ml < MS:
        # Mom presents the dish, smile cracking a little more each time
        bgc = (hx('ffd23f'), hx('ffb36b'), hx('ff8a5a'))[bi]
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * bi + 0.05 * eout(pop(ml, 0, MS)), (-4, 4, -6)[bi], shake_at(ml, [0], 6, 10), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bgc); ctx.fill()
        rays(ctx, 740, 1000, 200, 1700, lf * 0.05, col=(1, 1, 1), a=0.35, n=14)
        cx, cy, R = 360, 860, 230
        face(ctx, MOM, P(eye=('happy', 'normal', 'shock')[bi], mouth=('grin', 'smile', 'wavy')[bi], head=0), cx, cy, R, -0.06)
        if bi == 2:
            sweat(ctx, cx - 0.95 * R, cy - 0.7 * R, ml, 1.4)
        arm_to(ctx, cx + 120, cy + 420, 740, 1080, MOM['shirt'], MOM['skin'], bend=-40, w=80)
        if dish is soup:
            dish(ctx, 760, 1010, 1.25, 0, lf)
        else:
            dish(ctx, 760, 1010, 1.25, 0.05 * math.sin(ml))
        sparkle(ctx, 960, 820, 34); sparkle(ctx, 560, 1240, 26)
        ctx.restore()
        label1(ctx, name, (1, 1, 1), pop(ml, 0, 3), 140, -0.04, y=1420)
    else:
        rl = ml - MS
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eout(pop(rl, 0, 20)), (3, -3, 0)[bi], shake_at(rl, [8], 8, 16), f)
        if who == 'both':
            # split screen: left Dad, right kid
            ctx.rectangle(-500, -500, 1040, 3000); setc(ctx, hx('8fdcff')); ctx.fill()
            ctx.rectangle(540, -500, 1200, 3000); setc(ctx, hx('ffb3d9')); ctx.fill()
            face(ctx, DAD, P(eye='smug', mouth='frown', head=0), 290, 940, 210, 0.08)
            face(ctx, BOY, P(eye='smug', mouth='frown', head=0), 800, 960, 190, -0.08)
            ctx.move_to(540, -500); ctx.line_to(540, 2500); ink(ctx, 14); ctx.stroke()
        else:
            ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('8fdcff') if who == 'dad' else hx('ffb3d9')); ctx.fill()
            rays(ctx, 540, 900, 260, 1700, rl * 0.03, col=(1, 1, 1), a=0.3, n=14)
            ch = DAD if who == 'dad' else BOY
            face(ctx, ch, P(eye='smug' if who == 'dad' else 'closed', mouth='frown' if who == 'dad' else 'wavy', head=0), 420, 880, 260, 0.05)
            if who == 'boy':   # tongue out "eww"
                ellipse(ctx, 437, 1030, 36, 46); fl(ctx, hx('ff6f86'), 7)
        # the rejected dish in the corner gets the big red X
        dx_ = 540 if who == 'both' else 830
        if dish is soup:
            dish(ctx, dx_, 1220, 0.75, 0, lf)
        else:
            dish(ctx, dx_, 1220, 0.75, 0)
        x_stamp(ctx, dx_, 1190, pop(rl, 8, 12), 0.75)
        ctx.restore()
        label1(ctx, reply, (1, 1, 1), pop(rl, 1, 4), 112 if bi != 1 else 96, 0.02, y=1440)
        if rl >= 8:
            if who != 'both':
                label(ctx, "*BZZZT!*", 850, 1050, 80, RED, -0.12, pop(rl, 8, 11))
    card(ctx, 'p2', f, 92, 132)


def s3(ctx, f):
    lf = f - 200
    if lf < 32:
        # Mom ECU: "FINE." glare, low angle push-in, rolling up the sleeve
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.12 * eout(pop(lf, 0, 30)), 0, shake_at(lf, [4], 10, 18), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff3b5c')); ctx.fill()
        rays(ctx, 540, 1000, 260, 1700, lf * 0.08, col=(1, 0.8, 0.3), a=0.5, n=18)
        cx, cy, R = 540, 960, 290
        face(ctx, MOM, P(eye='glare', mouth='flat', head=0), cx, cy, R, 0)
        zigs(ctx, cx, cy - 1.1 * R, 120, lf)
        ctx.restore()
        label1(ctx, "\"FINE.\"", WHITE, pop(lf, 4, 7), 170, -0.04, y=1420)
        card(ctx, 'p3', f, 202, 232)
    elif lf < 95:
        il = lf - 32
        # kitchen, super-speed: Mom blurs between 3 spots, pans fly, dishes pile onto the counter
        ctx.save(); cam(ctx, 540, 1330, 1.12, 2 * math.sin(il * 0.7), 6, f)
        kitchen(ctx)
        # speed lines
        for k in range(16):
            y = 700 + k * 55; x0 = (il * 140 + k * 237) % 1600 - 300
            ctx.move_to(x0, y); ctx.line_to(x0 + 260, y); setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(8); ctx.stroke()
        spots = (220, 540, 860)
        cur = spots[(il // 3) % 3]
        for j, xs in enumerate(spots):
            a = 1.0 if xs == cur else 0.28
            ctx.push_group()
            ang = 40 * math.sin(il * 2 + j)
            draw(ctx, xs, 1580 - 186 * 1.25, 1.25, 1 if j % 2 == 0 else -1, MOM, P(eye='glare', mouth='grin', lsh=-90 + ang, lel=-40, rsh=-120 - ang, rel=-30, torso=10))
            ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
        # flying pans + ingredients
        for k in range(3):
            pan(ctx, 220 + k * 320, 930 + 60 * math.sin(il * 0.9 + k), 0.6 * math.sin(il * 0.8 + k * 2), 0.6, 1, il)
        # dishes appear one by one on the counter top
        cnt = int(pop(il, 4, 56) * 8)
        for k in range(cnt):
            fn = DISHES[k % 8]
            xx = 120 + (k % 4) * 280; yy = 1200 - (k // 4) * 140
            if fn is soup:
                fn(ctx, xx, yy, 0.55, 0, il)
            else:
                fn(ctx, xx, yy, 0.55, 0)
            if k == cnt - 1:
                sparkle(ctx, xx + 90, yy - 80, 26)
        ctx.restore()
        label2(ctx, "\"I'LL MAKE...", "EVERYTHING!\"", WHITE, pop(il, 2, 6), 120, col2=YEL, y=1440)
        label1(ctx, "*CLANG! SIZZLE! CHOP!*", ORANGE, pop(il, 8, 11), 82, 0.04 * math.sin(il), y=600)
    else:
        il = lf - 95
        # low angle: towering food mountain, Mom proud on top of a stool, TA-DA!
        ctx.save(); cam(ctx, 540, 1000 - 120 * eout(pop(il, 0, 30)), 0.78, 0, shake_at(il, [0], 10, 16), f)
        ctx.rectangle(-1000, -1000, 3200, 4000); setc(ctx, hx('ffd23f')); ctx.fill()
        rays(ctx, 540, 600, 200, 2200, il * 0.05, col=(1, 1, 1), a=0.55, n=18)
        table_front(ctx, -100, 1180, 1500)
        food_mountain(ctx, 540, 1460, 1.0, il)
        for k in range(6):
            sparkle(ctx, 60 + k * 190, 260 + 60 * math.sin(il * 0.5 + k), 40)
        ctx.restore()
        label1(ctx, "\"TA-DAAA!\"", WHITE, pop(il, 1, 4), 150, -0.04, y=1440)
        label1(ctx, "*DING!*", YEL, pop(il, 1, 3), 110, 0.05, y=600)


def table_scene(ctx, f, lf, zoom=1.0, cy=1080, boy_p=None, dad_p=None, mountain=True, mx=540, stuffed=0.0, plates=0):
    ctx.save(); cam(ctx, 540, cy, zoom, 0, 0, f)
    dining(ctx)
    belly = stuffed
    db = draw(ctx, 120, TABLE - 186 * 1.2 + 120, 1.2, 1, DAD, dad_p or P())
    bb = draw(ctx, 960, TABLE - 186 * 0.95 + 120, 0.95, -1, BOY, boy_p or P())
    if belly > 0:
        for (bx, by_), r in (((120, TABLE - 40), 230), ((960, TABLE - 20), 190)):
            ellipse(ctx, bx, by_, r * belly, r * 0.8 * belly); fl(ctx, DAD['shirt'] if bx < 500 else BOY['shirt'], 9)
            ellipse(ctx, bx - r * 0.25 * belly, by_ - r * 0.3 * belly, r * 0.25 * belly, r * 0.12 * belly); setc(ctx, (1, 1, 1, 0.4)); ctx.fill()
    if mountain:
        food_mountain(ctx, mx, TABLE + 10, 1.0, lf, sp=0.68)
    for k in range(plates):
        plate(ctx, 540, TABLE + 10 - k * 26, 1.0)
    table_front(ctx)
    ctx.restore()
    return db, bb


def s4(ctx, f):
    lf = f - 330
    if lf < 45:
        # wide: kid + Dad dwarfed by the mountain, look at each other... "can we just get PIZZA?"
        look = pop(lf, 6, 12)
        table_scene(ctx, f, lf, 0.72 + 0.04 * eout(pop(lf, 0, 45)), 900,
                    boy_p=P(eye='normal', mouth='flat', head=-12 * look, lsh=-40, rsh=40),
                    dad_p=P(eye='normal', mouth='flat', head=12 * look, lsh=-40, rsh=40))
        label2(ctx, "\"...can we just", "get PIZZA?\"", WHITE, pop(lf, 12, 16), 110, col2=YEL, y=1420)
        card(ctx, 'p4', f, 332, 370)
    elif lf < 90:
        il = lf - 45
        # Mom ECU: ears blow steam like a kettle
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.1 * eout(pop(il, 0, 40)), 0, 6 + shake_at(il, [2], 12, 20), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('e0263a')); ctx.fill()
        rays(ctx, 540, 960, 260, 1700, il * 0.12, col=(1, 0.6, 0.3), a=0.5, n=20)
        cx, cy, R = 540, 960, 270
        steam_jets(ctx, cx, cy, R, il, 0.6 + 0.4 * pop(il, 0, 15))
        face(ctx, MOM, P(eye='glare', mouth='wavy', head=0), cx, cy, R, 0.02 * math.sin(il * 3))
        twitch(ctx, cx + 0.42 * R, cy - 0.45 * R, il, 1.2)
        ctx.restore()
        label1(ctx, "*WHEEEEEEEE!*", WHITE, pop(il, 2, 5), 130, 0.03 * math.sin(il * 2), y=1440)
    else:
        il = lf - 90
        # instantly calm. too calm. creepy sweet smile
        ctx.save(); cam(ctx, 540, 960, 1.15 - 0.05 * eout(pop(il, 0, 40)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffc8e4')); ctx.fill()
        for k in range(5):
            ellipse(ctx, 540, 960, 380 + k * 160, 380 + k * 160); setc(ctx, (1, 1, 1, 0.18)); ctx.set_line_width(30); ctx.stroke()
        cx, cy, R = 540, 960, 270
        face(ctx, MOM, P(eye='happy', mouth='smile', head=0), cx, cy, R, -0.08)
        for k in range(3):
            sparkle(ctx, 220 + k * 320, 560 + 40 * math.sin(il * 0.4 + k), 30)
        ctx.restore()
        label2(ctx, "\"Sure,", "sweetie.\"", WHITE, pop(il, 3, 7), 120, col2=PINK, y=1420)


def s5(ctx, f):
    lf = f - 460
    if lf < 55:
        # Mom alone on the sofa, feet up, a whole pizza on her lap
        ctx.save(); cam(ctx, 540, 1100, 1.15 + 0.05 * eout(pop(lf, 0, 55)), 0, shake_at(lf, [0], 6, 8), f)
        ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('b39bff')); ctx.fill()
        for i in range(-30, 40):
            ctx.rectangle(i * 120, -3000, 46, 6000); setc(ctx, hx('a88ff6')); ctx.fill()
        ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('c98a52')); ctx.fill()
        ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()
        sofa_back(ctx)
        bite = pop(lf, 26, 30)
        draw(ctx, 470, SEAT - 186 * 1.3 + 60, 1.3, 1, MOM, P(eye='happy', mouth='grin' if lf < 26 else 'open', lhip=-80, lkn=80, rhip=-80, rkn=80,
                                                            lsh=-30, rsh=-110 - 30 * bite, rel=-60))
        sofa_front(ctx)
        pizza(ctx, 520, SEAT + 10, 0.9, 0.05, box=True)
        # her slice
        ctx.save(); ctx.translate(690, 1010 - 30 * bite); ctx.rotate(-0.6)
        poly(ctx, [(0, 0), (-50, -150), (50, -150)]); fl(ctx, hx('ffd23f'), 6)
        ctx.move_to(-56, -150); ctx.curve_to(-30, -175, 30, -175, 56, -150); setc(ctx, INK); ctx.set_line_width(26); ctx.stroke()
        ctx.move_to(-56, -150); ctx.curve_to(-30, -175, 30, -175, 56, -150); setc(ctx, hx('f2a640')); ctx.set_line_width(14); ctx.stroke()
        ellipse(ctx, 0, -90, 16, 16); fl(ctx, hx('e8342e'), 4)
        ctx.restore()
        for k in range(4):
            sparkle(ctx, 200 + k * 230, 760 + 30 * math.sin(lf * 0.5 + k), 28)
        ctx.restore()
        label2(ctx, "\"ONE pizza.", "Just for ME.\"", WHITE, pop(lf, 3, 7), 116, col2=YEL, y=1420)
        card(ctx, 'p5', f, 462, 500)
    elif lf < 118:
        il = lf - 55
        # low angle, kid + Dad with forks under the looming mountain; Mom's voice
        ctx.save(); cam(ctx, 540, 860, 0.8, 0, shake_at(il, [10], 8, 12), f)
        dining(ctx, hx('ffb36b'))
        food_mountain(ctx, 540, 1480, 1.0, il)
        ctx.restore()
        ctx.save(); cam(ctx, 540, 960, 1.0, 0, 0, f)
        face(ctx, DAD, P(eye='shock', mouth='open', head=0), 230, 1110, 200, 0.12)
        face(ctx, BOY, P(eye='shock', mouth='open', head=0), 850, 1120, 170, -0.12)
        fork(ctx, 420, 1000, 0.2, 1.0); fork(ctx, 670, 1010, -0.2, 0.9)
        sweat(ctx, 60, 860, il, 1.2); sweat(ctx, 1000, 890, il + 30, 1.0)
        ctx.restore()
        label2(ctx, "\"You said...", "ANYTHING.\"", WHITE, pop(il, 4, 8), 120, col2=RED, y=1440 - 0)
    elif lf < 165:
        il = lf - 118
        # 1 HOUR LATER: stuffed round Dad + kid, empty plates; Mom pops in sweetly
        table_scene(ctx, f, il, 0.78, 960,
                    boy_p=P(eye='closed', mouth='wavy', torso=-12, lsh=-20, rsh=20),
                    dad_p=P(eye='closed', mouth='wavy', torso=12, lsh=-20, rsh=20),
                    mountain=False, stuffed=1.0, plates=12)
        if il >= 16:
            ctx.save(); ctx.rectangle(0, 0, W, 860); ctx.clip()
            u = eout(pop(il, 16, 22))
            face(ctx, MOM, P(eye='happy', mouth='grin', head=0), 540, 300 + 340 * u, 170, 0.04 * math.sin(il * 0.5))
            ctx.restore()
            label2(ctx, "\"So... what do you", "want for BREAKFAST?\"", WHITE, pop(il, 18, 22), 92, col2=YEL, y=1420)
        else:
            label1(ctx, "*groooan*", WHITE, pop(il, 2, 5), 110, y=1430)
        card(ctx, 'p6', f, 580, 596)
    elif lf < 186:
        il = lf - 165
        # split: weak "...anything?"
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eout(pop(il, 0, 21)), 0, 0, f)
        ctx.rectangle(-500, -500, 1040, 3000); setc(ctx, hx('8fdcff')); ctx.fill()
        ctx.rectangle(540, -500, 1200, 3000); setc(ctx, hx('ffb3d9')); ctx.fill()
        face(ctx, DAD, P(eye='closed', mouth='wavy', head=0), 290, 940, 210, 0.1)
        face(ctx, BOY, P(eye='closed', mouth='wavy', head=0), 800, 960, 190, -0.1)
        sweat(ctx, 470, 760, il, 1.0); sweat(ctx, 960, 790, il + 20, 0.9)
        ctx.move_to(540, -500); ctx.line_to(540, 2500); ink(ctx, 14); ctx.stroke()
        ctx.restore()
        label1(ctx, "\"...anything?\"", WHITE, pop(il, 2, 5), 120, y=1430)
    else:
        il = lf - 186
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 646)


SHOTS = [(0, s1), (90, s2), (200, s3), (330, s4), (460, s5)]
CUTS = (45, 90, 104, 126, 138, 162, 172, 200, 232, 295, 330, 375, 420, 460, 515, 578, 625, 646)


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.25)
    ctx.set_source(g); ctx.paint()
    for c in CUTS:
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.5 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/v{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/dinner_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
