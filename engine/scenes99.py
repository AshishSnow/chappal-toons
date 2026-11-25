"""'The PILLOW FORT'. Original, general-audience comedy short, 22s.
Hook:   cosy living-room medium shot at night: a blanket fort over two chairs (fairy lights, a 'NO GROWN-UPS' sign);
        the kid sits in the doorway pointing out "NO GROWN-UPS ALLOWED!!", Dad kneels outside begging + caption "THE PILLOW FORT:".
Beat 1: Dad "Pleeease? I'm FUN!" -> kid "PASSWORD?" -> "...BANANA?" *BZZT!* "WRONG!" -> Dad pulls out a cookie
        "...COOKIE?" -> kid *NOM* "...ACCESS GRANTED." *DING!*
Beat 2: cut-away inside the fort (Dutch tilt): Dad crammed knees-to-ears, head bulging the blanket "...it's COZY." ->
        fluff on his nose "AH... AH..." -> *ACHOO!!* -> the fort explodes, cushions fly *FWOOMP!* -> blanket floats down.
Turn:   the one close-up: Dad's head pokes out of the blanket heap, grinning "BEST... FORT..." "...EVER!!"
Twist:  Mom walks in "Who took ALL the cushions?!" -> both heads duck under *fwip* "...not US." -> PLOT TWIST:
        MOM BUILT A BIGGER ONE. pan right to MOM'S CASTLE (sheets, cushion towers, flags) -> she pops out of the window
        "Members ONLY." -> Dad + kid "...PASSWORD?" -> "NOPE." *zip* -> the dog trots straight in *woof!* ->
        "...the DOG?!" -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r
from scenes58 import sweat, twitch
from scenes65 import dog
from scenes84 import eio
import scenes13
from scenes13 import card as _card13

RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
BLANK = hx('ff8fb8'); BLANK2 = hx('e8689a'); SHEET = hx('8fd0ff'); SHEET2 = hx('5fb0ef')
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ffc93c'), pants=hx('3d7bff'), shoes=hx('ff4d5e'))
MOM = dict(doodle.MOM_G, shirt=hx('9b4dff'))
DAD = dict(doodle.DAD, shirt=hx('3fd6a0'), pants=hx('3a4a8a'))
N = 660
FLOOR, GND = 1560, 1590
FX = 1080            # small fort centre
FL0, FR0 = 800, 1360  # fort edges
FTOP = 1230          # blanket top
KKID, KDAD, KMOM = 0.92, 1.0, 0.98
CX, CY, CZ = 1150, 1290, 1.28
CAST = 2140          # Mom's castle centre

CAPS = {'p1': [[("THE ", OUT), ("PILLOW FORT:", PINK)]],
        'p2': [[("PLOT TWIST:", RED)], [("MOM ", PURPLE), ("BUILT A BIGGER ONE.", OUT)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ set: cosy living room at night
def room(ctx, lf):
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, hx('e9e2ff')); ctx.fill()
    rnd = random.Random(99)
    for k in range(60):   # star wallpaper
        sparkle(ctx, rnd.uniform(300, 2700), rnd.uniform(500, 1500), 9, hx('c9b8ff'))
    # window (left) with night sky + moon
    x, y, w, h = 610, 880, 230, 270
    rect_r(ctx, x, y, w, h, 14); fl(ctx, hx('2c2f6e'), 8)
    ctx.save(); rect_r(ctx, x, y, w, h, 14); ctx.clip()
    ellipse(ctx, x + 160, y + 70, 34, 34); fl(ctx, hx('fff2a8'), 3)
    ellipse(ctx, x + 176, y + 62, 30, 30); setc(ctx, hx('2c2f6e')); ctx.fill()
    for k in range(7):
        sparkle(ctx, x + 20 + (k * 53) % 200, y + 40 + (k * 71) % 210, 7, YEL if (lf // 10 + k) % 3 else WHITE)
    ctx.restore()
    ctx.move_to(x + w / 2, y); ctx.line_to(x + w / 2, y + h); ctx.move_to(x, y + h / 2); ctx.line_to(x + w, y + h / 2); ink(ctx, 6); ctx.stroke()
    # picture frame + clock
    rect_r(ctx, 1150, 870, 150, 120, 8); fl(ctx, hx('ffb36a'), 6)
    rect_r(ctx, 1168, 888, 114, 84, 4); fl(ctx, hx('bfe9ff'), 3)
    poly(ctx, [(1178, 960), (1220, 905), (1262, 960)]); fl(ctx, hx('6fd37a'), 3)
    ellipse(ctx, 950, 920, 46, 46); fl(ctx, WHITE, 5)
    ctx.move_to(950, 920); ctx.line_to(950, 892); ctx.move_to(950, 920); ctx.line_to(972, 930); ink(ctx, 5); ctx.stroke()
    # bookshelf (right) + plant
    rect_r(ctx, 1440, 1120, 190, 440, 10); fl(ctx, hx('c98a52'), 6)
    for j in range(3):
        yy = 1170 + j * 130
        rect_r(ctx, 1452, yy + 92, 166, 14, 4); fl(ctx, hx('a46a3a'), 3)
        for b in range(5):
            cols = (PINK, MINT, GOLD, BLUE, PURPLE)
            rect_r(ctx, 1462 + b * 30, yy + 20 + (b % 2) * 12, 24, 72 - (b % 2) * 12, 4); fl(ctx, cols[(b + j) % 5], 3)
    rect_r(ctx, 1500, 1060, 70, 60, 10); fl(ctx, hx('ff8a5c'), 4)
    for a in (-0.7, -0.2, 0.3, 0.8):
        ellipse(ctx, 1535 + 44 * math.sin(a), 1020 - 30 * math.cos(a), 14, 34, a); fl(ctx, GREEN, 3)
    # far right: sofa (its cushions are gone!) + floor lamp
    rect_r(ctx, 2300, 1300, 420, 200, 40); fl(ctx, hx('5a7bff'), 6)
    rect_r(ctx, 1720, 1120, 12, 440, 4); fl(ctx, hx('8a5a3a'), 3)
    poly(ctx, [(1670, 1120), (1782, 1120), (1760, 1030), (1692, 1030)]); fl(ctx, hx('ffd36a'), 5)
    # skirting + wooden floor + rug
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('e8b98a')); ctx.fill()
    for k in range(-20, 60):
        ctx.move_to(k * 140, FLOOR); ctx.line_to(k * 140 - 60, FLOOR + 600); setc(ctx, (0.7, 0.5, 0.35, 0.35)); ctx.set_line_width(4); ctx.stroke()
    rect_r(ctx, -3000, FLOOR - 24, 9000, 24, 4); fl(ctx, WHITE, 4)
    ellipse(ctx, 1080, 1640, 470, 70); fl(ctx, hx('9fe7c8'), 5)
    ellipse(ctx, 1080, 1640, 380, 50); setc(ctx, hx('c8f4e0')); ctx.fill()


def fairy(ctx, lf, x0, x1, y0, sag, n=9):
    ctx.new_path(); ctx.move_to(x0, y0); ctx.curve_to(x0 + (x1 - x0) * 0.3, y0 + sag, x0 + (x1 - x0) * 0.7, y0 + sag, x1, y0)
    setc(ctx, INK); ctx.set_line_width(3); ctx.stroke()
    cols = (YEL, PINK, CYAN, MINT, ORANGE)
    for i in range(n):
        t = (i + 0.5) / n
        bx = (1 - t) ** 3 * x0 + 3 * (1 - t) ** 2 * t * (x0 + (x1 - x0) * 0.3) + 3 * (1 - t) * t * t * (x0 + (x1 - x0) * 0.7) + t ** 3 * x1
        by = y0 + 3 * (1 - t) ** 2 * t * sag + 3 * (1 - t) * t * t * sag + 6
        on = (lf // 6 + i) % 3 != 0
        c = cols[i % 5]
        if on:
            ellipse(ctx, bx, by + 6, 16, 16); setc(ctx, c[:3] + (0.35,)); ctx.fill()
        ellipse(ctx, bx, by + 6, 7, 9); fl(ctx, c if on else dark(c, 0.6), 2)


def cushion(ctx, x, y, col, a=0.0, w=150, h=60):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    rect_r(ctx, -w / 2, -h / 2, w, h, h * 0.4); fl(ctx, col, 4)
    ellipse(ctx, 0, 0, 7, 5); fl(ctx, dark(col, 0.75), 2)
    for sx in (-1, 1):
        for sy in (-1, 1):
            ctx.move_to(sx * w / 2 * 0.95, sy * h / 2 * 0.8); ctx.line_to(sx * (w / 2 + 10), sy * (h / 2 + 8)); ink(ctx, 3); ctx.stroke()
    ctx.restore()


def chair_top(ctx, x, a=0.0):
    ctx.save(); ctx.translate(x, FTOP + 30); ctx.rotate(a)
    rect_r(ctx, -16, -70, 32, 360, 10); fl(ctx, hx('b97a4a'), 4)
    ellipse(ctx, 0, -72, 22, 22); fl(ctx, hx('d99a5a'), 4)
    ctx.restore()


def blanket_path(ctx, top, sag, x0=FL0, x1=FR0, bump=None):
    """front-view draped blanket: rounded top between chair posts, sides flaring to the floor, scalloped hem"""
    ctx.new_path()
    ctx.move_to(x0, GND - 10)
    ctx.curve_to(x0 + 20, top + 160, x0 + 30, top + 20, x0 + 80, top)
    if bump:
        bx, bh = bump
        ctx.line_to(bx - 90, top + sag * 0.6)
        ctx.curve_to(bx - 50, top + sag * 0.6, bx - 50, top - bh, bx, top - bh)
        ctx.curve_to(bx + 50, top - bh, bx + 50, top + sag * 0.6, bx + 90, top + sag * 0.6)
    else:
        ctx.curve_to(x0 + (x1 - x0) * 0.35, top + sag, x0 + (x1 - x0) * 0.65, top + sag, x1 - 80, top)
    ctx.line_to(x1 - 80, top)
    ctx.curve_to(x1 - 30, top + 20, x1 - 20, top + 160, x1, GND - 10)
    n = 8
    for i in range(n):
        xa = x1 - (x1 - x0) * i / n; xb = x1 - (x1 - x0) * (i + 1) / n
        ctx.curve_to(xa - 10, GND + 14, xb + 10, GND + 14, xb, GND - 10)
    ctx.close_path()


def blanket_dots(ctx, top, x0=FL0, x1=FR0):
    rnd = random.Random(5)
    for k in range(18):
        x = rnd.uniform(x0 + 40, x1 - 40); y = rnd.uniform(top + 40, GND - 40)
        sparkle(ctx, x, y, 10, WHITE)


def sign(ctx, x, y, a, s1="NO", s2="GROWN-UPS", col=hx('f4d9a8')):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    poly(ctx, [(-95, -62), (95, -66), (92, 62), (-90, 66)]); fl(ctx, col, 5)
    text(ctx, s1, 0, -22, 40, RED, ow=4, shadow=False)
    text(ctx, s2, 0, 26, 34, RED, ow=4, shadow=False, maxw=170)
    for sx in (-1, 1):
        rect_r(ctx, sx * 80 - 14, -72, 28, 16, 3); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()
    ctx.restore()


def fort(ctx, lf, wob=0.0, door=True):
    """small blanket fort; returns nothing. door: dark open doorway in the middle"""
    for x in (FL0 + 70, FR0 - 70):
        chair_top(ctx, x, wob * 0.02)
    ctx.save(); ctx.translate(FX, GND); ctx.rotate(wob * 0.01); ctx.translate(-FX, -GND)
    blanket_path(ctx, FTOP, 50); fl(ctx, BLANK, 6)
    ctx.save(); blanket_path(ctx, FTOP, 50); ctx.clip(); blanket_dots(ctx, FTOP)
    for k in range(4):   # soft folds
        xx = FL0 + 120 + k * 110
        ctx.move_to(xx, FTOP + 80); ctx.curve_to(xx + 10, FTOP + 200, xx - 10, GND - 150, xx + 6, GND - 20)
        setc(ctx, BLANK2[:3] + (0.6,)); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()
    if door:
        doorway(ctx, lf)
    fairy(ctx, lf, FL0 + 70, FR0 - 70, FTOP - 6, 60)
    # pennant on the left chair
    ctx.move_to(FL0 + 70, FTOP - 40); ctx.line_to(FL0 + 70, FTOP - 170); ink(ctx, 5); ctx.stroke()
    fw = 6 * math.sin(lf * 0.3)
    poly(ctx, [(FL0 + 70, FTOP - 170), (FL0 + 150, FTOP - 145 + fw), (FL0 + 70, FTOP - 118)]); fl(ctx, GOLD, 4)
    ctx.restore()


DOOR_X0, DOOR_X1, DOOR_TOP = FX - 120, FX + 120, 1330


def door_path(ctx):
    ctx.new_path(); ctx.move_to(DOOR_X0, GND - 6)
    ctx.curve_to(DOOR_X0 + 10, DOOR_TOP + 40, FX - 40, DOOR_TOP, FX, DOOR_TOP)
    ctx.curve_to(FX + 40, DOOR_TOP, DOOR_X1 - 10, DOOR_TOP + 40, DOOR_X1, GND - 6); ctx.close_path()


def doorway(ctx, lf):
    door_path(ctx)
    g = cairo.RadialGradient(FX, GND - 80, 20, FX, GND - 80, 260)
    g.add_color_stop_rgb(0, 1, 0.85, 0.5); g.add_color_stop_rgb(1, 0.3, 0.2, 0.4)
    ctx.save(); ctx.set_source(g); ctx.fill_preserve(); ctx.restore(); ink(ctx, 5); ctx.stroke()


def door_flaps(ctx):
    for sd in (-1, 1):   # tied-back flaps
        xe = DOOR_X0 if sd < 0 else DOOR_X1
        ctx.new_path(); ctx.move_to(FX + sd * 20, DOOR_TOP)
        ctx.curve_to(xe + sd * 10, DOOR_TOP + 60, xe - sd * 30, DOOR_TOP + 150, xe + sd * 6, GND - 6)
        ctx.line_to(xe + sd * 50, GND - 6); ctx.curve_to(xe + sd * 40, DOOR_TOP + 120, xe + sd * 40, DOOR_TOP + 40, FX + sd * 40, DOOR_TOP - 10)
        ctx.close_path(); fl(ctx, BLANK2, 4)
        ellipse(ctx, xe + sd * 20, DOOR_TOP + 140, 14, 10); fl(ctx, GOLD, 3)


def stand(ctx, ch, x, k, p, f_=1, feet=GND):
    return draw(ctx, x, feet - 186 * k, k, f_, ch, p)


SIT = dict(lhip=86, lkn=-86, rhip=88, rkn=-88)
KNEEL = dict(lhip=6, lkn=95, rhip=-6, rkn=95)


def kneel(ctx, ch, x, k, p, f_=1, feet=GND):
    # kneeling: shins folded back, so drop the body by the shin length
    return draw(ctx, x, feet - 186 * k + 62 * k * 1.35, k, f_, ch, p)


def sit(ctx, ch, x, k, p, f_=1, feet=GND):
    return draw(ctx, x, feet - 186 * k + 70 * k * 1.35, k, f_, ch, p)


def cookie(ctx, x, y, r=26, bite=0.0):
    ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi); fl(ctx, hx('e0a35a'), 4)
    for dx, dy in ((-8, -6), (9, -2), (-2, 10), (10, 11)):
        ellipse(ctx, x + dx * r / 26, y + dy * r / 26, 4 * r / 26, 4 * r / 26); setc(ctx, hx('5a3420')); ctx.fill()
    if bite > 0:
        ellipse(ctx, x + r * 0.8, y - r * 0.5, r * 0.5 * bite, r * 0.5 * bite); setc(ctx, hx('fff0d6')); ctx.fill()


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = CZ + 0.04 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, CX, CY, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    room(ctx, lf)
    fort(ctx, lf)
    sit(ctx, KID, FX, KKID, P(eye='glare', mouth='scream', lsh=-90, lel=-10, rsh=40, rel=-110, head=-6, **SIT), 1)
    door_flaps(ctx)
    sign(ctx, FL0 + 110, 1440, -0.08)
    cushion(ctx, FL0 + 40, GND - 28, MINT, 0.05)
    beg = 6 * math.sin(lf * 0.5)
    d = kneel(ctx, DAD, 1420, KDAD, P(eye='happy', mouth='open', lsh=70 + beg, lel=-100, rsh=60 - beg, rel=-110, head=6 + beg * 0.5, **KNEEL), -1)
    dog(ctx, 620, GND - 6, 0.42, 1, lf, sleep=True)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"NO GROWN-UPS", 540, 1450, 92, YEL, -0.04, t)
    label(ctx, "ALLOWED!!\"", 540, 1555, 104, YEL, -0.04, t)


# ------------------------------------------------------------------ shot 2: the password
def beat1(ctx, f, il):
    # 0-34 "Pleeease? I'm FUN!" ; 34-60 "PASSWORD?" ; 60-88 "...BANANA?" BZZT WRONG ; 88-112 "...COOKIE?" ; 112-140 NOM ACCESS GRANTED
    pin = eio(pop(il, 0, 50))
    ctx.save(); cam(ctx, lerp(CX, 1250, pin), lerp(CY, 1320, pin), lerp(CZ, 1.45, pin), 0, shake_at(il, [74, 114], 9, 10), f)
    room(ctx, il); fort(ctx, il)
    # kid
    if il < 34:
        kp = P(eye='glare', mouth='flat', lsh=30, lel=-150, rsh=30, rel=-150)
    elif il < 60:
        kp = P(eye='smug', mouth='smile', lsh=-60, lel=-20, rsh=40, rel=-110, head=-8)
    elif il < 88:
        kp = P(eye='glare', mouth='scream', lsh=-120, lel=0, rsh=30, rel=-150, head=6)
    elif il < 112:
        kp = P(eye='shock', mouth='open', lsh=-50, lel=-40, rsh=40, rel=-100)
    else:
        kp = P(eye='happy', mouth='grin', lsh=-160, lel=-10, rsh=-60, rel=-80, head=-6 * math.sin(il * 0.5))
    kd = sit(ctx, KID, FX, KKID, dict(kp, **SIT), 1)
    door_flaps(ctx)
    sign(ctx, FL0 + 110, 1440, -0.08)
    # Dad
    if il < 34:
        beg = 8 * math.sin(il * 0.6)
        dp = P(eye='happy', mouth='grin', lsh=70 + beg, lel=-110, rsh=60 - beg, rel=-110, head=8)
    elif il < 60:
        dp = P(eye='normal', mouth='open', lsh=20, lel=-20, rsh=20, rel=-20, head=4)
    elif il < 88:
        sc = il >= 74
        dp = P(eye='shock' if sc else 'happy', mouth='wavy' if sc else 'smile', lsh=90, lel=-120, rsh=20, rel=-20, head=-8 if sc else 6)
    elif il < 112:
        dp = P(eye='smug', mouth='grin', lsh=80, lel=-40, rsh=20, rel=-20, head=6)
    else:
        dp = P(eye='happy', mouth='open', lsh=150, lel=-20, rsh=140, rel=-20, head=0)
    dd = kneel(ctx, DAD, 1440, KDAD, dict(dp, **KNEEL), -1)
    if 60 <= il < 74:   # banana in hand
        hx_, hy_ = dd['head'][0] - dd['R'] * 1.6, dd['head'][1] + dd['R'] * 0.2
        ctx.new_path(); ctx.arc(hx_, hy_, 34, 0.3, 2.6); ctx.arc_negative(hx_, hy_ - 14, 30, 2.5, 0.4); ctx.close_path(); fl(ctx, hx('ffe14a'), 4)
    if 88 <= il < 116:
        u = eio(pop(il, 108, 116))
        cookie(ctx, lerp(dd['front'][0] - 70, FX + 40, u), lerp(dd['head'][1] + 50, kd['head'][1] + 30, u), 24)
    if 74 <= il < 88:   # big red X
        a = max(0.01, pop(il, 74, 78))
        ctx.save(); ctx.translate(1250, 1120); ctx.scale(a, a)
        for s_ in (-1, 1):
            ctx.move_to(-60, -60 * s_); ctx.line_to(60, 60 * s_); setc(ctx, INK); ctx.set_line_width(36); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
            ctx.move_to(-60, -60 * s_); ctx.line_to(60, 60 * s_); setc(ctx, RED); ctx.set_line_width(24); ctx.stroke()
        ctx.restore()
    if il >= 120:
        for k in range(5):
            sparkle(ctx, FX - 160 + k * 80, 1300 - 30 * math.sin(il * 0.3 + k), 14, YEL)
    dog(ctx, 620, GND - 6, 0.42, 1, il, sleep=True)
    ctx.restore()
    if il < 34:
        label(ctx, "\"Pleeease? I'm FUN!\"", 540, 1520, 96, WHITE, -0.03, pop(il, 2, 6))
    elif il < 60:
        label(ctx, "\"What's the PASSWORD?\"", 540, 1520, 92, YEL, 0.03, pop(il, 36, 40))
    elif il < 74:
        label(ctx, "\"...BANANA?\"", 540, 1520, 110, WHITE, -0.03, pop(il, 62, 66))
    elif il < 88:
        label(ctx, "*BZZT!* \"WRONG!\"", 540, 1520, 110, RED, 0.04, pop(il, 74, 77))
    elif il < 112:
        label(ctx, "\"...COOKIE?\"", 540, 1520, 110, hx('ffb86a'), -0.03, pop(il, 90, 94))
    else:
        label(ctx, "*NOM*", 540, 760, 110, ORANGE, 0.05, pop(il, 114, 117))
        label(ctx, "\"...ACCESS GRANTED.\"", 540, 1520, 96, MINT, -0.03, pop(il, 120, 124))


def s2(ctx, f):
    beat1(ctx, f, f - 60)


# ------------------------------------------------------------------ shot 3: inside the fort -> ACHOO
FLY = [(FL0 + 40, MINT, -1), (FL0 + 200, GOLD, -1), (FR0 - 60, PURPLE, 1), (FR0 - 220, ORANGE, 1), (FX, BLUE, 1)]


def inside(ctx, f, il):
    # 0-40 crammed "...it's COZY." ; 40-70 fluff "AH... AH..." ; 70 ACHOO ; 70-100 explosion ; 100-130 blanket floats down
    zz = 1.45 + 0.25 * eio(pop(il, 40, 68)) - 0.35 * eio(pop(il, 70, 76))
    ctx.save(); cam(ctx, FX + 30, 1360 - 40 * pop(il, 40, 68), zz, -6 + 4 * pop(il, 70, 80), shake_at(il, [70, 76], 14, 26), f)
    room(ctx, il)
    boom = pop(il, 70, 96)
    if il < 70:
        # interior back wall of the tent (lit by a flashlight)
        blanket_path(ctx, FTOP, 50); fl(ctx, hx('ffc6dc'), 6)
        g = cairo.RadialGradient(FX - 160, 1450, 20, FX - 160, 1450, 380)
        g.add_color_stop_rgba(0, 1, 0.95, 0.6, 0.85); g.add_color_stop_rgba(1, 1, 0.9, 0.6, 0)
        ctx.save(); blanket_path(ctx, FTOP, 50); ctx.clip(); ctx.set_source(g); ctx.paint(); ctx.restore()
        for x in (FL0 + 70, FR0 - 70):
            chair_top(ctx, x)
        fairy(ctx, il, FL0 + 70, FR0 - 70, FTOP + 30, 40)
        cushion(ctx, FX - 260, GND - 26, MINT, 0, 180, 56)
        cushion(ctx, FX + 260, GND - 26, PURPLE, 0, 180, 56)
        # snacks + flashlight + teddy
        rect_r(ctx, FX - 60, GND - 60, 60, 50, 8); fl(ctx, hx('ff5f6f'), 3)
        for k in range(3):
            ellipse(ctx, FX - 40 + k * 14, GND - 66, 10, 8); fl(ctx, hx('fff4c8'), 2)
        # kid
        sit(ctx, KID, FX - 210, KKID, P(eye='happy', mouth='grin', lsh=40, lel=-80, rsh=-40, rel=-70, **SIT), 1)
        rect_r(ctx, FX - 120, GND - 150, 60, 26, 8); fl(ctx, hx('4a4f6a'), 3)
        # Dad crammed: knees to his ears
        sneez = pop(il, 40, 68)
        dp = P(eye='happy' if il < 40 else 'closed', mouth='grin' if il < 40 else 'open', lsh=50, lel=-150, rsh=-50, rel=-150,
               lhip=150, lkn=-150, rhip=150, rkn=-150, head=4 - 16 * sneez, torso=-8 * sneez)
        d = sit(ctx, DAD, FX + 130, KDAD, dp, -1, GND + 30)
        # front-edge band of the blanket roof, bulged by Dad's head
        top = d['head'][1] - d['R'] * 1.15
        ctx.new_path(); ctx.move_to(FL0 + 20, FTOP + 40); ctx.curve_to(FL0 + 40, FTOP - 20, FR0 - 40, FTOP - 20, FR0 - 20, FTOP + 40)
        bx = d['head'][0]
        ctx.line_to(bx + 140, FTOP + 40); ctx.curve_to(bx + 70, FTOP + 40, bx + 80, top, bx, top)
        ctx.curve_to(bx - 80, top, bx - 70, FTOP + 40, bx - 140, FTOP + 40)
        ctx.close_path(); fl(ctx, BLANK, 6)
        fairy(ctx, il, FL0 + 60, FR0 - 60, FTOP + 20, 20)
        if il >= 40:   # fluff drifting onto his nose
            u = pop(il, 40, 60)
            fx_, fy_ = lerp(bx - 30, d['head'][0] - d['R'] * 0.1, u), lerp(FTOP + 60, d['head'][1] + d['R'] * 0.25, u) + 8 * math.sin(il * 0.5)
            for k in range(6):
                a = k * math.pi / 3 + il * 0.1
                ctx.move_to(fx_, fy_); ctx.line_to(fx_ + 12 * math.cos(a), fy_ + 12 * math.sin(a)); setc(ctx, INK); ctx.set_line_width(2.5); ctx.stroke()
        dog(ctx, FX - 20, GND - 6, 0.36, 1, il)
    else:
        # the explosion: chairs tip out, cushions fly, blanket billows up then floats down
        for sd, x in ((-1, FL0 + 70), (1, FR0 - 70)):
            chair_top(ctx, x + sd * 120 * eio(boom), sd * 1.2 * eio(boom))
        fall = eio(pop(il, 96, 126))
        up_ = 150 * math.sin(math.pi * min(1, boom * 1.2)) * (1 - fall)
        # two lumps under the blanket
        sit(ctx, KID, FX - 210, KKID, P(eye='shock', mouth='scream', lsh=160, lel=-10, rsh=-160, rel=-10, **SIT), 1)
        sit(ctx, DAD, FX + 130, KDAD, P(eye='shock', mouth='scream', lsh=160, lel=-10, rsh=-160, rel=-10, **SIT), -1)
        top = lerp(FTOP - 80, 1400, fall) - up_ * 0.2
        ctx.new_path(); ctx.move_to(FL0 - 60 + 40 * fall, GND)
        ctx.curve_to(FL0 - 100, top - up_, FX - 200, top - up_ - 40 * (1 - fall), FX - 210, top + 40 * fall)
        ctx.curve_to(FX - 60, top + 90 * fall, FX + 20, top - 60 * fall - up_, FX + 130, top - 60 * fall - up_ * 0.6)
        ctx.curve_to(FX + 260, top - 40 * fall - up_, FR0 + 100, top - up_, FR0 + 60 - 40 * fall, GND)
        ctx.close_path(); fl(ctx, BLANK, 6)
        rnd = random.Random(4)
        for k in range(12):
            sparkle(ctx, rnd.uniform(FL0, FR0), rnd.uniform(top + 60, GND - 30), 10, WHITE)
        for j, (x, col, sd) in enumerate(FLY):
            u = boom
            cx_ = x + sd * (420 + j * 60) * u
            cy_ = GND - 40 - (520 + j * 60) * math.sin(math.pi * min(1, u * 0.9)) * (1 - 0.3 * j / 5)
            cushion(ctx, cx_, cy_, col, u * (5 + j) * sd)
        if il < 90:
            for k in range(12):   # fluff burst
                a = k * math.pi / 6; r = 500 * boom
                ellipse(ctx, FX + r * math.cos(a), 1380 + r * 0.8 * math.sin(a), 18, 12, a); fl(ctx, WHITE, 2)
    ctx.restore()
    if il < 40:
        label(ctx, "\"...it's COZY.\"", 540, 1520, 110, WHITE, -0.03, pop(il, 4, 8))
    elif il < 70:
        label(ctx, "\"AH... AH...\"", 540, 1520, 120, YEL, 0.03, pop(il, 46, 50))
    elif il < 100:
        label(ctx, "*ACHOOO!!*", 540, 760, 140, ORANGE, -0.05, pop(il, 70, 73))
        label(ctx, "*FWOOMP!*", 540, 1520, 120, PINK, 0.04, pop(il, 78, 81))
    else:
        label(ctx, "*flumpf.*", 540, 1520, 110, WHITE, -0.03, pop(il, 112, 116))


def s3(ctx, f):
    inside(ctx, f, f - 200)


# ------------------------------------------------------------------ the blanket heap (heads poke out)
def heap(ctx, lf, dad_up=1.0, kid_up=1.0, shiver=0.0, dp=None, kp=None):
    sh = shiver * 5 * math.sin(lf * 2.1)
    from scenes32 import _SCR
    _SCR.identity_matrix()
    k0 = sit(_SCR, KID, 0, KKID, P(**SIT), 1, GND + 30); d0 = sit(_SCR, DAD, 0, KDAD, P(**SIT), -1, GND + 30)
    kn = k0['head'][1] + k0['R'] * 0.95; dn_ = d0['head'][1] + d0['R'] * 0.95
    ctx.save(); ctx.rectangle(-3000, -3000, 9000, 3000 + GND); ctx.clip()
    kd = sit(ctx, KID, FX - 200 + sh, KKID, kp or P(eye='normal', mouth='flat', lsh=20, lel=-10, rsh=-20, rel=-10, **SIT), 1, GND + 150 * (1 - kid_up) + 30)
    dd = sit(ctx, DAD, FX + 120 - sh, KDAD, dp or P(eye='happy', mouth='grin', lsh=20, lel=-10, rsh=-20, rel=-10, **SIT), -1, GND + 170 * (1 - dad_up) + 30)
    ctx.restore()
    ctx.new_path(); ctx.move_to(FL0 - 120, GND + 10)
    ctx.curve_to(FL0 - 60, 1470, FX - 330, kn + 30, FX - 290, kn)
    ctx.curve_to(FX - 250, kn - 10, FX - 150, kn - 10, FX - 110, kn + 10)
    ctx.curve_to(FX - 60, kn + 70, FX - 20, dn_ + 40, FX + 10, dn_)
    ctx.curve_to(FX + 60, dn_ - 10, FX + 180, dn_ - 10, FX + 230, dn_ + 10)
    ctx.curve_to(FX + 300, dn_ + 40, FR0 + 60, 1470, FR0 + 120, GND + 10)
    ctx.close_path(); fl(ctx, BLANK, 6)
    ctx.new_path()
    rnd = random.Random(3)
    for k in range(10):
        x = rnd.uniform(FL0, FR0); y = rnd.uniform(max(kn, dn_) + 60, GND - 20)
        sparkle(ctx, x, y, 10, WHITE)
    return dd, kd


SCAT = [(FL0 - 260, MINT, 0.3), (FR0 + 260, PURPLE, -0.4), (FL0 - 60, GOLD, -0.2), (FR0 + 420, ORANGE, 0.5), (FX + 520, BLUE, 0.1)]


def scattered(ctx):
    for x, col, a in SCAT:
        cushion(ctx, x, GND - 20, col, a)
    for sd, x in ((-1, FL0 - 50), (1, FR0 + 50)):
        ctx.save(); ctx.translate(x, GND - 10); ctx.rotate(sd * 1.45)
        rect_r(ctx, -16, -300, 32, 300, 10); fl(ctx, hx('b97a4a'), 4)
        ctx.restore()


# ------------------------------------------------------------------ shot 4: the one close-up
def s4(ctx, f):
    il = f - 330
    ctx.save(); cam(ctx, FX + 100, 1330, 2.0 + 0.1 * eio(il / 70), 0, shake_at(il, [34], 6, 8) + 1.5, f)
    room(ctx, il); scattered(ctx)
    big = il >= 34
    heap(ctx, il, 1.0, 0.0, 0, dp=P(eye='happy' if not big else 'closed', mouth='grin' if not big else 'scream',
                                  lsh=20, lel=-10, rsh=-20, rel=-10, head=6 * math.sin(il * 0.4), **SIT))
    ctx.restore()
    if il < 34:
        label(ctx, "\"BEST... FORT...\"", 540, 1480, 115, WHITE, -0.03, pop(il, 3, 7))
    else:
        label(ctx, "\"...EVER!!\"", 540, 1480, 140, YEL, 0.03, pop(il, 34, 37))
        for k in range(6):
            sparkle(ctx, 200 + k * 140, 640 + 40 * math.sin(il * 0.4 + k), 20, YEL)


# ------------------------------------------------------------------ Mom's castle
def castle(ctx, lf, curtain=0.0, mom_win=None):
    x0, x1, top = CAST - 280, CAST + 280, 1180
    # cushion towers with flags
    for tx in (x0 - 10, x1 + 10):
        for j in range(5):
            cushion(ctx, tx, GND - 30 - j * 62, (PINK, MINT, GOLD, PURPLE, ORANGE)[(j + (tx > CAST)) % 5], 0.04 * (-1) ** j, 140, 58)
        ctx.move_to(tx, GND - 330); ctx.line_to(tx, GND - 500); ink(ctx, 5); ctx.stroke()
        fw = 8 * math.sin(lf * 0.3 + tx)
        poly(ctx, [(tx, GND - 500), (tx + 90, GND - 470 + fw), (tx, GND - 440)]); fl(ctx, RED, 4)
    # big sheet over the sofa
    blanket_path(ctx, top, 30, x0 + 40, x1 - 40); fl(ctx, SHEET, 6)
    ctx.save(); blanket_path(ctx, top, 30, x0 + 40, x1 - 40); ctx.clip()
    for k in range(5):   # stripes
        ctx.rectangle(x0 + 60 + k * 100, top - 20, 40, 600); setc(ctx, SHEET2[:3] + (0.5,)); ctx.fill()
    ctx.restore()
    # battlements
    for k in range(6):
        rect_r(ctx, x0 + 80 + k * 80, top - 46, 50, 56, 8); fl(ctx, SHEET2, 4)
    fairy(ctx, lf, x0 + 50, x1 - 50, top + 10, 50, 12)
    # door
    ctx.new_path(); ctx.move_to(CAST + 30, GND - 6); ctx.curve_to(CAST + 30, 1420, CAST + 200, 1420, CAST + 200, GND - 6); ctx.close_path()
    g = cairo.RadialGradient(CAST + 115, GND - 60, 10, CAST + 115, GND - 60, 160)
    g.add_color_stop_rgb(0, 1, 0.85, 0.5); g.add_color_stop_rgb(1, 0.3, 0.2, 0.4)
    ctx.save(); ctx.set_source(g); ctx.fill_preserve(); ctx.restore(); ink(ctx, 5); ctx.stroke()
    # window (Mom pops out here)
    wx, wy, ww, wh = CAST - 215, 1270, 180, 160
    rect_r(ctx, wx, wy, ww, wh, 20); setc(ctx, hx('ffe0a0')); ctx.fill()
    if mom_win is not None:
        ctx.save(); rect_r(ctx, wx, wy, ww, wh, 20); ctx.clip()
        stand(ctx, MOM, wx + ww / 2, KMOM, mom_win, 1, wy + wh + 210)
        ctx.restore()
    if curtain > 0:
        ctx.save(); rect_r(ctx, wx, wy, ww, wh, 20); ctx.clip()
        ctx.rectangle(wx, wy, ww, wh * curtain); setc(ctx, hx('ff7a9a')); ctx.fill()
        for k in range(4):
            ctx.move_to(wx + 25 + k * 50, wy); ctx.line_to(wx + 25 + k * 50, wy + wh * curtain); setc(ctx, (0.8, 0.3, 0.45, 0.7)); ctx.set_line_width(5); ctx.stroke()
        ctx.restore()
    rect_r(ctx, wx, wy, ww, wh, 20); ink(ctx, 6); ctx.stroke()
    sign(ctx, CAST + 120, 1300, 0.06, "MOM'S", "CASTLE", hx('fff4c8'))
    sign(ctx, CAST - 110, GND - 50, -0.05, "MEMBERS", "ONLY", hx('f4d9a8'))


# ------------------------------------------------------------------ shot 5: Mom -> the castle -> loop
def finale(ctx, f, il):
    # 0-40 Mom "Who took ALL the cushions?!" ; 40-70 heads duck *fwip* "...not US." ; 70 card + pan right ;
    # 110-140 Mom walks into the castle door ; 140-170 pops out of the window "Members ONLY." ;
    # 150-180 Dad + kid run over "...PASSWORD?" ; 180-200 "NOPE." *zip* ; 200-230 dog trots in *woof!* "...the DOG?!"
    pan = eio(pop(il, 72, 110))
    ccx = lerp(CX, 1990, pan)
    ctx.save(); cam(ctx, ccx, lerp(CY, 1250, pan), lerp(CZ, 0.97, pan), 0, shake_at(il, [40, 180], 8, 9), f)
    room(ctx, il)
    castle(ctx, il, curtain=eio(pop(il, 182, 192)),
           mom_win=(P(eye='smug', mouth='smile', lsh=150, lel=-30, rsh=30, rel=-40, head=-6) if il < 182 else
                    P(eye='closed', mouth='smug' if False else 'smile', lsh=150, lel=-30, rsh=30, rel=-40, head=-10)) if 138 <= il < 196 else None)
    scattered(ctx)
    # Dad + kid: in the heap, then run to the castle
    if il < 150:
        dup = 1 - eio(pop(il, 40, 46))
        dup = max(dup, eio(pop(il, 56, 62)) * 0.55)   # peek back up to the eyes
        dp = P(eye='shock', mouth='open', **SIT) if il < 40 else P(eye='shock', mouth='flat', **SIT)
        heap(ctx, il, dup, dup, 1.0 if 46 <= il < 70 else 0, dp=dp,
             kp=P(eye='shock', mouth='open' if il < 40 else 'flat', **SIT))
    else:
        u = eio(pop(il, 150, 168))
        kx = lerp(FX - 200, 1725, u); dx = lerp(FX + 120, 1565, u)
        hopy = -30 * abs(math.sin(math.pi * u * 3)) * (u < 1)
        if il < 200:
            kp = P(eye='happy' if il < 180 else 'shock', mouth='open' if il < 180 else 'wavy', lsh=60, lel=-100, rsh=50, rel=-100)
            dp = P(eye='happy' if il < 180 else 'shock', mouth='open' if il < 180 else 'wavy', lsh=70, lel=-110, rsh=60, rel=-110)
        else:
            kp = P(eye='shock', mouth='scream', lsh=150, lel=-20, rsh=40, rel=-60)
            dp = P(eye='shock', mouth='scream', lsh=30, lel=-150, rsh=30, rel=-150)
        stand(ctx, DAD, dx, KDAD, dp, 1, GND + hopy)
        stand(ctx, KID, kx, KKID, kp, 1, GND + hopy)
        heap_flat(ctx)
    # Mom
    if il < 140:
        if il < 72:
            mx = lerp(1900, 1490, eio(pop(il, 0, 16)))
            mp = P(eye='glare', mouth='open', lsh=150, lel=-30, rsh=-150, rel=-30) if il < 40 else P(eye='smug', mouth='flat', lsh=30, lel=-150, rsh=30, rel=-150, head=-6)
            fdir = -1
        else:
            u = pop(il, 76, 136)
            mx = lerp(1490, CAST + 115, eio(u)); fdir = 1
            mp = P(eye='happy', mouth='grin', lsh=20 + 20 * math.sin(il * 0.5), lel=-20, rsh=-20 - 20 * math.sin(il * 0.5), rel=-20, rot=3 * math.sin(il * 0.5))
        if il < 120:
            stand(ctx, MOM, mx, KMOM, mp, fdir, GND)
        else:   # duck into the door
            ctx.save(); ctx.new_path(); ctx.rectangle(mx - 300, 0, 600, GND - 220 * pop(il, 120, 138) + 30); ctx.clip()
            stand(ctx, MOM, mx, KMOM, mp, fdir, GND + 260 * eio(pop(il, 120, 138)))
            ctx.restore()
    # dog trots into the castle
    if il < 196:
        dog(ctx, FX - 420 + (il * 0.4 if il > 150 else 0), GND - 6, 0.42, 1, il, sleep=il < 150)
    else:
        u = pop(il, 196, 222)
        dx_ = lerp(1330, CAST + 115, eio(u))
        if u < 1:
            dog(ctx, dx_, GND - 6 - 14 * abs(math.sin(il * 0.6)), 0.42, 1, il)
        else:
            ctx.save(); ctx.translate(CAST + 115, GND - 10)
            ctx.rotate(0.3 * math.sin(il * 0.9))
            poly(ctx, [(-6, 0), (6, 0), (20, -40), (-4, -10)]); fl(ctx, hx('c98a52'), 3)   # wagging tail in the doorway
            ctx.restore()
    ctx.restore()
    if 72 <= il < 150:
        card(ctx, 'p2', il, 74)
    if il < 40:
        label(ctx, "\"Who took ALL", 540, 1450, 96, WHITE, -0.03, pop(il, 2, 6))
        label(ctx, "the CUSHIONS?!\"", 540, 1555, 100, PINK, -0.03, pop(il, 6, 10))
    elif il < 72:
        label(ctx, "*fwip*", 540, 1430, 90, WHITE, 0.04, pop(il, 40, 43))
        label(ctx, "\"...not US.\"", 540, 1540, 110, YEL, -0.03, pop(il, 52, 56))
    elif il < 150:
        if il >= 140:
            label(ctx, "\"Members ONLY.\"", 540, 1520, 110, PURPLE, -0.03, pop(il, 140, 144))
    elif il < 182:
        label(ctx, "\"...PASSWORD?\"", 540, 1520, 120, YEL, 0.03, pop(il, 160, 164))
    elif il < 200:
        label(ctx, "\"NOPE.\" *zip*", 540, 1520, 120, PINK, -0.04, pop(il, 182, 185))
    else:
        label(ctx, "*woof!*", 540, 1420, 100, GOLD, 0.05, pop(il, 216, 219))
        label(ctx, "\"...the DOG?!\"", 540, 1540, 120, YEL, -0.03, pop(il, 222, 226))


def heap_flat(ctx):
    ctx.new_path(); ctx.move_to(FL0 - 120, GND + 10)
    ctx.curve_to(FL0 - 40, 1500, FR0 + 40, 1500, FR0 + 120, GND + 10); ctx.close_path(); fl(ctx, BLANK, 6)


def s5(ctx, f):
    lf = f - 400
    if lf < 230:
        finale(ctx, f, lf)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (200, s3), (330, s4), (400, s5)]
CUTS = (60, 200, 270, 330, 400, 630)


def render(f):
    import sketch
    sketch.BOIL[0] = f // 4
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.1, 0.05, 0.15, 0.2)
    ctx.set_source(g); ctx.paint()
    for c in CUTS:
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.5 * (1 - (f - c) / 3))); ctx.fill()
    sketch.paper(s)
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/v{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/fort_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
