"""'FREE SAMPLES'. Original, general-audience comedy short, 22s.
Hook:   grocery-store medium shot: kid at the free-sample stand, cheeks STUFFED, toothpick in hand; the sample lady
        (paper hat) glaring and pointing "ONE PER CUSTOMER!" + caption 'FREE SAMPLES:'.
Beat 1: disguise #1 - kid slides back in sunglasses + fake moustache "Hello. I am... NEW." -> lady glare -> NOPE!
Beat 2: disguise #2 - top hat, giant white beard, cane, on tiptoe "Good day, madam." -> NOPE!
Beat 3: disguise #3 - Dutch tilt: a cardboard box creeps up *creep creep*, a hand sneaks out -> lady lifts the box
        -> sheepish kid "...hi." NICE TRY.
Close-up (the one face shot): lady's glare + twitch "I NEVER FORGET... A FACE."
Twist:  Dad strolls in wearing the kid's sunglasses "Hi! New customer." -> lady melts, hearts "WELL, HELLO!" hands him
        the WHOLE TRAY -> PLOT TWIST: DAD JUST WORE SUNGLASSES. -> low-angle kid "...HOW?!" -> Dad shares, kid stuffs
        his cheeks *GULP* -> lady "HEY!!" -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face, rays
from scenes58 import sweat, twitch
from scenes84 import eio
import scenes13
from scenes13 import card as _card13

RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
CHEESE = hx('ffd23f')
DAD = dict(doodle.DAD, shirt=hx('ff8a5c'), pants=hx('3a4a6a'), shoes=hx('7a4a2c'))
DADS = dict(DAD, shades=True)
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('5ad06a'), pants=hx('3d7bff'), shoes=hx('ff4d5e'))
KID_D1 = dict(KID, shades=True, moustache=hx('2a1a14'))
LADY = dict(doodle.NMOM, shirt=hx('ff6b9a'), glasses=None)
N = 660
FLOOR, GND = 1560, 1595
TX, TTOP = 1170, 1385          # sample stand centre x, top surface y
LX, KX = 1350, 880             # lady x, kid x
CX, CY, CZ = 1080, 1270, 1.17

CAPS = {'p1': [[("FREE ", OUT), ("SAMPLES:", RED)]],
        'p2': [[("PLOT TWIST:", RED)], [("DAD JUST WORE ", OUT), ("SUNGLASSES.", PURPLE)]]}
scenes13.CAPS = CAPS
card = _card13


def stand(ctx, ch, x, k, p, f_=1, feet=GND):
    return draw(ctx, x, feet - 186 * k, k, f_, ch, p)


# ------------------------------------------------------------------ props
def cube(ctx, x, y, s=1.0, pick=True):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rect_r(ctx, -15, -15, 30, 30, 5); fl(ctx, CHEESE, 3)
    ellipse(ctx, -5, -3, 3, 3); setc(ctx, hx('e0a820')); ctx.fill()
    if pick:
        ctx.move_to(4, -10); ctx.line_to(10, -42); setc(ctx, hx('c98a52')); ctx.set_line_width(4); ctx.stroke()
        ellipse(ctx, 10, -44, 5, 5); setc(ctx, RED); ctx.fill()
    ctx.restore()


def tray(ctx, x, y, s=1.0, n=7, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ellipse(ctx, 0, 6, 120, 26); setc(ctx, (0, 0, 0, 0.15)); ctx.fill()
    ellipse(ctx, 0, 0, 120, 26); fl(ctx, hx('e8eef5'), 4)
    ellipse(ctx, 0, -2, 98, 18); setc(ctx, WHITE); ctx.fill()
    spots = [(-70, -6), (-35, -10), (0, -8), (35, -10), (70, -6), (-50, 4), (20, 4), (55, 6), (-15, 6)]
    for (px, py) in spots[:n]:
        cube(ctx, px, py - 8, 0.8)
    ctx.restore()


def toothpick(ctx, x, y, s=1.0, a=0.0, cheese=False):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(0, 0); ctx.line_to(0, -60); setc(ctx, hx('c98a52')); ctx.set_line_width(5); ctx.stroke()
    ellipse(ctx, 0, -62, 6, 6); setc(ctx, RED); ctx.fill()
    if cheese:
        rect_r(ctx, -14, -40, 28, 28, 5); fl(ctx, CHEESE, 3)
    ctx.restore()


def stuffed(ctx, d, ch, amt=1.0):
    """big puffed hamster cheeks over the face"""
    hx_, hy_ = d['head']; R = d['R']
    for sx in (-1, 1):
        ellipse(ctx, hx_ + sx * R * 0.62, hy_ + R * 0.42, R * 0.36 * amt, R * 0.3 * amt); fl(ctx, ch['skin'], 4)
        ellipse(ctx, hx_ + sx * R * 0.66, hy_ + R * 0.42, R * 0.16, R * 0.1); setc(ctx, (1, 0.45, 0.55, 0.7)); ctx.fill()
    ctx.new_path(); ctx.move_to(hx_ - R * 0.14, hy_ + R * 0.6); ctx.curve_to(hx_ - R * 0.05, hy_ + R * 0.54, hx_ + R * 0.05, hy_ + R * 0.66, hx_ + R * 0.16, hy_ + R * 0.58)
    ink(ctx, 4); ctx.stroke()


def paper_hat(ctx, d, f_=-1):
    hx_, hy_ = d['head']; R = d['R']
    ctx.save(); ctx.translate(hx_, hy_ - R * 0.92); ctx.rotate(0.08 * f_)
    poly(ctx, [(-R * 0.62, R * 0.1), (R * 0.62, R * 0.1), (R * 0.46, -R * 0.36), (-R * 0.46, -R * 0.36)]); fl(ctx, WHITE, 4)
    rect_r(ctx, -R * 0.64, -R * 0.04, R * 1.28, R * 0.16, 4); fl(ctx, RED, 3)
    ctx.restore()


def top_hat(ctx, d):
    hx_, hy_ = d['head']; R = d['R']
    ctx.save(); ctx.translate(hx_, hy_ - R * 0.78)
    rect_r(ctx, -R * 0.95, -R * 0.08, R * 1.9, R * 0.2, 8); fl(ctx, hx('2a2a3a'), 4)
    rect_r(ctx, -R * 0.6, -R * 1.25, R * 1.2, R * 1.22, 8); fl(ctx, hx('2a2a3a'), 4)
    ctx.rectangle(-R * 0.6, -R * 0.36, R * 1.2, R * 0.2); setc(ctx, PURPLE); ctx.fill()
    ctx.restore()


def beard(ctx, d, sway=0.0):
    hx_, hy_ = d['head']; R = d['R']
    ctx.save(); ctx.translate(hx_ + R * 0.08, hy_ + R * 0.3)
    ctx.new_path(); ctx.move_to(-R * 0.85, -R * 0.1)
    ctx.curve_to(-R * 0.9, R * 0.9, -R * 0.3 + sway, R * 1.6, 0 + sway * 1.5, R * 1.75)
    ctx.curve_to(R * 0.3 + sway, R * 1.6, R * 0.9, R * 0.9, R * 0.85, -R * 0.1)
    ctx.curve_to(R * 0.4, R * 0.2, -R * 0.4, R * 0.2, -R * 0.85, -R * 0.1); ctx.close_path()
    fl(ctx, hx('f4f4f8'), 4)
    for k in range(5):
        x = -R * 0.5 + k * R * 0.25
        ctx.move_to(x, R * 0.4); ctx.curve_to(x + 8, R * 0.8, x - 8, R * 1.0, x + sway * 0.4, R * 1.25)
    setc(ctx, hx('c8c8d4')); ctx.set_line_width(4); ctx.stroke()
    ellipse(ctx, 0, R * 0.12, R * 0.2, R * 0.1); setc(ctx, hx('8a2a3a')); ctx.fill()
    ctx.restore()


def cane(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(0, 0); ctx.line_to(0, 300); ctx.move_to(0, 0); ctx.arc_negative(-26, 0, 26, 0, math.pi)
    ink(ctx, 18); ctx.stroke_preserve(); setc(ctx, hx('a46a3a')); ctx.set_line_width(10); ctx.stroke()
    ctx.restore()


def cbox(ctx, x, y, s=1.0, lf=0, eyes=True, hand=0.0, lift=0.0, rot=0.0):
    """cardboard box disguise, (x,y) = bottom centre"""
    ctx.save(); ctx.translate(x, y - lift); ctx.rotate(rot); ctx.scale(s, s)
    rect_r(ctx, -150, -260, 300, 260, 8); fl(ctx, hx('d8a065'), 6)
    ctx.move_to(-150, -130); ctx.line_to(150, -130); setc(ctx, hx('b07a45')); ctx.set_line_width(4); ctx.stroke()
    for sx in (-1, 1):   # flaps
        poly(ctx, [(sx * 4, -260), (sx * 150, -260), (sx * 170, -310), (sx * 30, -300)]); fl(ctx, hx('e8b478'), 5)
    rect_r(ctx, -20, -262, 40, 120, 2); setc(ctx, (1, 1, 1, 0.35)); ctx.fill()     # tape
    for k, ax in enumerate((-90, 90)):  # 'this side up' arrows
        poly(ctx, [(ax, -100), (ax - 22, -70), (ax - 8, -70), (ax - 8, -40), (ax + 8, -40), (ax + 8, -70), (ax + 22, -70)])
        setc(ctx, hx('8a5a2a')); ctx.fill()
    if eyes:
        for ex in (-40, 40):
            rect_r(ctx, ex - 26, -205, 52, 34, 10); setc(ctx, INK); ctx.fill()
            ellipse(ctx, ex + 6 + 6 * math.sin(lf * 0.2), -188, 10, 10); setc(ctx, WHITE); ctx.fill()
    ctx.restore()
    if hand > 0:   # sneaky hand out of the side
        hx0, hy0 = x + 150 * s, y - lift - 120 * s
        hx1 = hx0 + 120 * hand
        ctx.new_path(); ctx.move_to(hx0 - 10, hy0); ctx.line_to(hx1, hy0 - 40 * hand); ink(ctx, 34); ctx.stroke_preserve()
        setc(ctx, KID['shirt']); ctx.set_line_width(22); ctx.stroke()
        ellipse(ctx, hx1 + 12, hy0 - 40 * hand, 20, 16); fl(ctx, KID['skin'], 4)


def heart(ctx, x, y, s, col=PINK):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(0, 12)
    ctx.curve_to(-30, -8, -18, -34, 0, -16); ctx.curve_to(18, -34, 30, -8, 0, 12); ctx.close_path()
    fl(ctx, col, 3)
    ctx.restore()


def stamp(ctx, s, x, y, t, ang=-0.15, col=RED):
    if t <= 0:
        return
    sc = 1.6 - 0.6 * eout(min(1, t * 2))
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(sc, sc)
    rect_r(ctx, -200, -70, 400, 140, 16); setc(ctx, (1, 1, 1, 0.85)); ctx.fill_preserve()
    setc(ctx, col); ctx.set_line_width(12); ctx.stroke()
    text(ctx, s, 0, 0, 96, col, outline=WHITE, ow=8, shadow=False)
    ctx.restore()


# ------------------------------------------------------------------ set: grocery store aisle
PROD = (hx('ff8a5c'), hx('5aa8ff'), hx('ffd23f'), hx('3fd6a0'), hx('ff5fa8'), hx('b88aff'), hx('ffffff'), hx('ff3b5c'))


def store(ctx, lf):
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, hx('dff3ea')); ctx.fill()
    rnd = random.Random(104)
    for k in range(60):   # tiny star wallpaper
        x, y = rnd.uniform(-200, 2400), rnd.uniform(400, 820)
        ctx.save(); ctx.translate(x, y); ctx.rotate(rnd.uniform(0, 1))
        poly(ctx, [(0, -9), (3, -3), (9, -3), (4, 2), (6, 9), (0, 5), (-6, 9), (-4, 2), (-9, -3), (-3, -3)])
        setc(ctx, hx('bfe8d6')); ctx.fill(); ctx.restore()
    # ceiling lights
    for x in (500, 1100, 1700):
        rect_r(ctx, x - 120, 640, 240, 26, 12); fl(ctx, WHITE, 4)
    # back shelves
    for (x0, x1) in ((-300, 1000), (1000, 2300)):
        rect_r(ctx, x0, 860, x1 - x0, 680, 10); fl(ctx, hx('f7f1e6'), 6)
        for j in range(4):
            yy = 880 + j * 165
            rect_r(ctx, x0 + 10, yy + 140, x1 - x0 - 20, 18, 4); fl(ctx, hx('c9d2dc'), 3)
            x = x0 + 30; m = 0
            while x < x1 - 70:
                c = PROD[(m * 3 + j * 5 + (x0 > 0)) % len(PROD)]
                kind = (m + j) % 3
                if kind == 0:     # box
                    w_, h_ = 70, 110
                    rect_r(ctx, x, yy + 140 - h_, w_, h_, 6); fl(ctx, c, 3)
                    rect_r(ctx, x + 12, yy + 140 - h_ + 20, w_ - 24, 36, 6); setc(ctx, (1, 1, 1, 0.6)); ctx.fill()
                elif kind == 1:   # can
                    w_, h_ = 54, 80
                    rect_r(ctx, x, yy + 140 - h_, w_, h_, 8); fl(ctx, c, 3)
                    ctx.rectangle(x + 3, yy + 140 - h_ + 28, w_ - 6, 20); setc(ctx, (1, 1, 1, 0.55)); ctx.fill()
                else:             # jar
                    w_, h_ = 58, 90
                    rect_r(ctx, x + 4, yy + 140 - h_, w_ - 8, 16, 4); fl(ctx, hx('ff3b5c') if c != RED else GOLD, 3)
                    rect_r(ctx, x, yy + 140 - h_ + 14, w_, h_ - 14, 14); fl(ctx, c, 3)
                    ellipse(ctx, x + w_ / 2, yy + 140 - h_ / 2 + 8, 16, 12); setc(ctx, (1, 1, 1, 0.6)); ctx.fill()
                x += w_ + 14; m += 1
            # price tags
            for t in range(int(x0 + 80), int(x1 - 60), 220):
                rect_r(ctx, t, yy + 142, 46, 18, 3); setc(ctx, YEL); ctx.fill()
    # hanging aisle sign
    ctx.move_to(760, 600); ctx.line_to(760, 730); ctx.move_to(1000, 600); ctx.line_to(1000, 730); ink(ctx, 4); ctx.stroke()
    rect_r(ctx, 720, 720, 320, 96, 14); fl(ctx, hx('3fa8ff'), 5)
    text(ctx, "AISLE 4", 880, 768, 46, WHITE, ow=6, shadow=False)
    # floor: checker tiles
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('f5f0ff')); ctx.fill()
    for i in range(-20, 40):
        for jj in range(0, 8):
            if (i + jj) % 2 == 0:
                ctx.rectangle(i * 90, FLOOR + jj * 60, 90, 60); setc(ctx, hx('d8d0f2')); ctx.fill()
    rect_r(ctx, -3000, FLOOR - 22, 9000, 22, 4); fl(ctx, hx('c9d2dc'), 4)
    # potted plant (right)
    rect_r(ctx, 1640, 1460, 100, 110, 14); fl(ctx, hx('ff8a5c'), 5)
    for a in (-0.9, -0.4, 0.1, 0.6, 1.0):
        ellipse(ctx, 1690 + 70 * math.sin(a), 1420 - 50 * math.cos(a), 20, 48, a); fl(ctx, GREEN, 3)
    # shopping cart (left)
    cart(ctx, 520, GND)


def cart(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    poly(ctx, [(-150, -250), (140, -250), (110, -90), (-120, -90)]); setc(ctx, (0.85, 0.9, 1, 0.45)); ctx.fill_preserve(); ink(ctx, 7); ctx.stroke()
    for k in range(1, 6):
        ctx.move_to(-150 + k * 48, -250); ctx.line_to(-120 + k * 38, -90)
    for k in range(1, 3):
        ctx.move_to(-150 + k * 10, -250 + k * 53); ctx.line_to(140 - k * 10, -250 + k * 53)
    ink(ctx, 3); ctx.stroke()
    # groceries poking out
    rect_r(ctx, -110, -320, 60, 90, 6); fl(ctx, PROD[1], 3)
    ellipse(ctx, 0, -270, 46, 34); fl(ctx, PROD[2], 3)
    ctx.move_to(60, -250); ctx.line_to(90, -340); ink(ctx, 14); ctx.stroke_preserve(); setc(ctx, hx('f2d090')); ctx.set_line_width(8); ctx.stroke()
    ctx.move_to(140, -250); ctx.line_to(190, -280); ink(ctx, 8); ctx.stroke()
    ctx.move_to(-110, -90); ctx.line_to(-110, -30); ctx.line_to(110, -30); ctx.line_to(110, -90); ink(ctx, 6); ctx.stroke()
    for wx in (-100, 100):
        ellipse(ctx, wx, -14, 16, 16); fl(ctx, hx('3a3a4a'), 3)
    ctx.restore()


def stand_table(ctx, n=7, tray_on=True):
    rect_r(ctx, TX - 220, TTOP, 440, GND - TTOP, 10); fl(ctx, WHITE, 6)
    ctx.save(); rect_r(ctx, TX - 220, TTOP, 440, GND - TTOP, 10); ctx.clip()
    for i in range(12):
        ctx.rectangle(TX - 220 + i * 40, TTOP, 20, 300); setc(ctx, (1, 0.25, 0.35, 0.35)); ctx.fill()
    for j in range(8):
        ctx.rectangle(TX - 220, TTOP + j * 40, 440, 20); setc(ctx, (1, 0.25, 0.35, 0.3)); ctx.fill()
    ctx.restore()
    rect_r(ctx, TX - 220, TTOP, 440, GND - TTOP, 10); ink(ctx, 6); ctx.stroke()
    # sign
    rect_r(ctx, TX - 160, TTOP + 50, 320, 100, 14); fl(ctx, YEL, 5)
    text(ctx, "FREE", TX, TTOP + 82, 40, RED, ow=5, shadow=False)
    text(ctx, "SAMPLES", TX, TTOP + 124, 40, RED, ow=5, shadow=False)
    if tray_on:
        tray(ctx, TX - 10, TTOP - 4, 1.0, n)


def lady(ctx, lf, p, x=LX, k=1.12, hearts=0.0):
    d = stand(ctx, LADY, x, k, p, -1)
    paper_hat(ctx, d)
    if hearts > 0:
        for i in range(4):
            a = i * 1.6 + lf * 0.12
            u = ((lf * 0.03 + i * 0.25) % 1.0)
            heart(ctx, d['head'][0] + 110 * math.cos(a), d['head'][1] - 60 - 160 * u, 1.1 * hearts * (1 - 0.4 * u))
    return d


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = CZ + 0.04 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, CX, CY, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    store(ctx, lf)
    w = math.sin(lf * 1.3)
    lp = P(eye='glare', mouth='open', lsh=95 + 5 * w, lel=0, rsh=20, rel=-40, head=4)
    lady(ctx, lf, lp)
    stand_table(ctx, 6)
    kp = P(eye='shock', mouth='flat', lsh=20, lel=-120, rsh=30, rel=-125, head=-4 + 3 * w)
    kd = stand(ctx, KID, KX, 0.95, kp, 1)
    stuffed(ctx, kd, KID, 1.0 + 0.05 * w)
    toothpick(ctx, kd['front'][0], kd['front'][1] + 10, 1.0, 0.2)
    sweat(ctx, kd['head'][0] - kd['R'] * 1.0, kd['head'][1] - kd['R'] * 0.5, lf, 0.8)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"ONE PER", 540, 1400, 104, YEL, -0.04, t)
    label(ctx, "CUSTOMER!\"", 540, 1505, 118, WHITE, 0.03, t)


# ------------------------------------------------------------------ shot 2: disguises #1 and #2
def disguise(ctx, f, il):
    sub = 0 if il < 70 else 1
    j = il - (0, 70)[sub]
    ctx.save()
    zz = 1.28 if j < 44 else 1.36
    cam(ctx, 1080, 1250, zz, (-3, 3)[sub], shake_at(j, [44], 10, 14), f)
    store(ctx, il)
    lp = P(eye='glare', mouth='flat' if j < 44 else 'open', lsh=20 if j < 44 else 95, lel=-40 if j < 44 else 0, rsh=20, rel=-40, head=4)
    ld = lady(ctx, il, lp)
    stand_table(ctx, 6)
    slide = eout(pop(j, 0, 12))
    x = lerp(560, KX + 20, slide)
    if sub == 0:
        p = P(eye='normal', mouth='smile', shades=1, lsh=-30, lel=-20, rsh=40, rel=-110, head=6, torso=-6 + 6 * (1 - slide))
        d = stand(ctx, KID_D1, x, 0.95, p, 1)
        if j >= 44:
            sweat(ctx, d['head'][0] - d['R'], d['head'][1] - d['R'] * 0.4, j, 0.8)
    else:
        bob = abs(math.sin(j * 0.5)) * 14
        p = P(eye='closed' if j < 44 else 'shock', mouth='smile', lsh=60, lel=-30, rsh=-20, rel=-20, head=-4, lhip=-4, rhip=4)
        d = stand(ctx, KID, x, 0.95, p, 1, GND - 30 - bob)
        beard(ctx, d, 6 * math.sin(j * 0.3))
        top_hat(ctx, d)
        cane(ctx, d['front'][0], d['front'][1] - 6, 0.9)
    ctx.restore()
    if j < 6:
        speed_lines(ctx, 540, 960, il, 0.45 * (1 - j / 6), 50, 500)
    label(ctx, ("DISGUISE #1", "DISGUISE #2")[sub], 540, 470, 80, CYAN, 0.03, pop(j, 2, 5))
    if j < 44:
        if sub == 0:
            label(ctx, "\"Hello. I am...", 540, 1390, 92, WHITE, -0.03, pop(j, 10, 14))
            if j >= 24:
                label(ctx, "NEW.\"", 540, 1495, 130, YEL, 0.03, pop(j, 24, 27))
        else:
            label(ctx, "\"Good day,", 540, 1390, 96, WHITE, -0.03, pop(j, 10, 14))
            if j >= 24:
                label(ctx, "MADAM.\"", 540, 1495, 120, YEL, 0.03, pop(j, 24, 27))
    else:
        stamp(ctx, "NOPE!", 540, 1450, pop(j, 44, 48), (-0.14, 0.12)[sub])


def s2(ctx, f):
    disguise(ctx, f, f - 60)


# ------------------------------------------------------------------ shot 3: the box
def boxshot(ctx, f, il):
    # 0-50 box creeps in *creep creep*, hand sneaks out ; 50-70 lady SLAPS the hand away? lifts the box ; 70-100 sheepish kid
    tilt = -7 if il < 50 else 0
    zz = 1.35 if il < 50 else 1.3
    ctx.save(); cam(ctx, 1060, 1290, zz, tilt, shake_at(il, [50], 12, 16), f)
    store(ctx, il)
    if il < 50:
        lp = P(eye='closed', mouth='smile', lsh=20, lel=-40, rsh=20, rel=-40, head=6)
    elif il < 70:
        lp = P(eye='glare', mouth='open', lsh=165, lel=0, rsh=160, rel=0, head=-4)
    else:
        lp = P(eye='glare', mouth='grin', lsh=150, lel=0, rsh=150, rel=0, head=4)
    ld = lady(ctx, il, lp, LX - (0 if il < 50 else 130))
    stand_table(ctx, 6)
    creep = lerp(600, KX + 40, eio(pop(il, 0, 36)))
    if il < 50:
        shuffle = 6 * math.sin(il * 0.9)
        cbox(ctx, creep, GND, 0.82, il, True, hand=pop(il, 34, 46), rot=math.radians(shuffle * 0.3))
        for sx in (-50, 50):
            ellipse(ctx, creep + sx + shuffle * (1 if sx > 0 else -1), GND - 6, 26, 12); fl(ctx, KID['shoes'], 3)
    else:
        lift = 600 * eout(pop(il, 50, 60))
        kp = P(eye='happy', mouth='grin', lsh=20, lel=-30, rsh=150, rel=-30, head=8, lhip=40, lkn=-80, rhip=40, rkn=-80) if il >= 56 else \
            P(eye='shock', mouth='open', lsh=40, lel=-120, rsh=40, rel=-120, lhip=40, lkn=-80, rhip=40, rkn=-80)
        kd = stand(ctx, KID, KX + 40, 0.95, kp, 1, GND + 40)
        if il >= 56:
            cube(ctx, kd['front'][0] + 6, kd['front'][1] - 16, 1.0)
        cbox(ctx, KX + 40 + 150 * eout(pop(il, 50, 60)), GND, 0.82, il, False, lift=lift)
    ctx.restore()
    if il < 50:
        label(ctx, "DISGUISE #3", 540, 470, 80, CYAN, 0.03, pop(il, 2, 5))
        label(ctx, "*creep... creep...*", 540, 1420, 88, ORANGE, -0.03, pop(il, 6, 10))
    elif il < 70:
        label(ctx, "*FWOOP!*", 540, 470, 110, WHITE, 0.04, pop(il, 50, 53))
    else:
        label(ctx, "\"...hi.\"", 540, 1380, 110, MINT, -0.03, pop(il, 70, 73))
        stamp(ctx, "NICE TRY.", 540, 1520, pop(il, 80, 84), -0.1)


def s3(ctx, f):
    boxshot(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: the one close-up
def closeup(ctx, f, il):
    z = 1 + 0.06 * eio(il / 70)
    ctx.save(); cam(ctx, 540, 960, z, 2 * math.sin(il * 0.2), shake_at(il, [36], 10, 16) + 2, f)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('ffb3d0')), (1, hx('ff7aa8'))])); ctx.paint()
    rays(ctx, 540, 900, 150, 1400, il * 0.01, (1, 1, 1), 0.25, 18)
    p = P(eye='glare', mouth='flat' if il < 36 else 'open', lsh=-20, lel=-100, rsh=110, rel=-60, head=-3)
    face(ctx, LADY, p, 540, 900, 200, 0, -1)
    # paper hat on the big face
    paper_hat(ctx, {'head': (540, 900), 'R': 200})
    for sx in (-1, 1):   # pointing at her own eyes ('I'm watching you') - two fingers
        pass
    if il >= 36:
        twitch(ctx, 540 + 200, 900 - 200, il, 1.5)
    ctx.restore()
    label(ctx, "\"I NEVER FORGET...", 540, 1370, 92, WHITE, -0.03, pop(il, 4, 8))
    if il >= 36:
        label(ctx, "A FACE.\"", 540, 1500, 150, RED, 0.04, pop(il, 36, 39))


def s4(ctx, f):
    closeup(ctx, f, f - 300)


# ------------------------------------------------------------------ shot 5: twist
def finale(ctx, f, il):
    # 0-40 Dad strolls in with shades "Hi! New customer." ; 40-80 lady melts, hearts "WELL, HELLO!" ;
    # 80-130 she hands him the WHOLE tray + PLOT TWIST card ; 130-170 low-angle kid "...HOW?!" ;
    # 170-220 Dad shares, kid stuffs cheeks *GULP* ; 220-260 lady "HEY!!"
    if 130 <= il < 170:   # low angle on the kid
        j = il - 130
        ctx.save(); cam(ctx, 900, 1380, 1.75, 4, shake_at(j, [8], 12, 16), f)
        store(ctx, il)
        kp = P(eye='shock', mouth='scream', lsh=150, lel=-20, rsh=150, rel=-20, head=-8)
        kd = stand(ctx, KID, KX, 0.95, kp, 1)
        sweat(ctx, kd['head'][0] + kd['R'] * 1.0, kd['head'][1] - kd['R'] * 0.4, j, 0.8)
        ctx.restore()
        speed_lines(ctx, 540, 900, il, 0.4, 50, 420)
        label(ctx, "\"...HOW?!\"", 540, 1470, 160, RED, -0.04, pop(j, 8, 11))
        return
    if il < 40:
        cx_, cy_, z = 1080, 1270, 1.17
    elif il < 130:
        u = eio(pop(il, 40, 52)); cx_, cy_, z = lerp(1080, 1180, u), lerp(1270, 1200, u), lerp(1.17, 1.45, u)
    else:
        cx_, cy_, z = 1080, 1270, 1.2
    ctx.save(); cam(ctx, cx_, cy_, z, 0, shake_at(il, [222], 14, 22), f)
    store(ctx, il)
    # lady
    if il < 40:
        lp = P(eye='glare', mouth='flat', lsh=20, lel=-40, rsh=20, rel=-40, head=4)
        ld = lady(ctx, il, lp)
    elif il < 80:
        lp = P(eye='happy', mouth='grin', lsh=40, lel=-130, rsh=40, rel=-130, head=-8 + 4 * math.sin(il * 0.3))
        ld = lady(ctx, il, lp, hearts=pop(il, 40, 46))
    elif il < 220:
        lp = P(eye='happy', mouth='smile', lsh=95, lel=-10, rsh=90, rel=-10, head=-6)
        ld = lady(ctx, il, lp, hearts=1.0 if il < 130 else 0.5)
    else:
        lp = P(eye='glare', mouth='scream', lsh=95, lel=0, rsh=160, rel=0, head=4)
        ld = lady(ctx, il, lp)
    stand_table(ctx, 6, tray_on=il < 80)
    # Dad
    walk = eout(pop(il, 0, 22))
    dx_ = lerp(560, 940, walk) + 80 * eio(pop(il, 160, 172))
    if il < 40:
        sw = math.sin(il * 0.7) * (1 - walk * 0.8)
        dp = P(eye='normal', mouth='smile', shades=1, lsh=20 + 20 * sw, lel=-20, rsh=-140 if il > 22 else -20 * sw, rel=-30, lhip=15 * sw, rhip=-15 * sw, head=4)
    elif il < 80:
        dp = P(eye='normal', mouth='grin', shades=1, lsh=20, lel=-20, rsh=-140, rel=-30, head=6)
    elif il < 170:
        dp = P(eye='normal', mouth='grin', shades=1, lsh=90, lel=-60, rsh=95, rel=-60, head=-4)
    else:
        dp = P(eye='normal', mouth='grin', shades=1, lsh=70, lel=-40, rsh=80, rel=-40, head=-8)
    dd = stand(ctx, DADS, dx_, 1.12, dp, 1)
    if il >= 80:
        u = eio(pop(il, 80, 96))
        tx_ = lerp(TX - 10, dd['front'][0] + 40, u); ty_ = lerp(TTOP - 4, dd['front'][1] - 20, u) - 60 * math.sin(u * math.pi)
        ncube = 6 if il < 170 else max(0, 6 - (il - 170) // 7)
        tray(ctx, tx_, ty_, 0.9, ncube)
        if u >= 1:
            for k in range(4):
                a = k * 1.57 + il * 0.2
                sparkle(ctx, tx_ + 140 * math.cos(a), ty_ - 40 + 50 * math.sin(a), 14, YEL)
    # kid
    if il < 80:
        kp = P(eye='normal', mouth='frown', lsh=20, lel=-20, rsh=30, rel=-20, head=-6)
        kd = stand(ctx, KID, 700, 0.95, kp, 1)
    elif il < 170:
        kp = P(eye='shock', mouth='open', lsh=40, lel=-120, rsh=40, rel=-120)
        kd = stand(ctx, KID, 700, 0.95, kp, 1)
    else:
        w = math.sin(il * 1.6)
        kp = P(eye='happy' if il < 220 else 'shock', mouth='flat', lsh=150 + 10 * w, lel=-100, rsh=140 - 10 * w, rel=-110, head=4 * w)
        kd = stand(ctx, KID, 760, 0.95, kp, 1)
        stuffed(ctx, kd, KID, min(1.25, 0.6 + 0.02 * (il - 170)))
    ctx.restore()
    if 96 <= il < 130:
        card(ctx, 'p2', il, 96, 130)
    if il < 40:
        if il >= 20:
            label(ctx, "\"Hi! New", 540, 1400, 100, WHITE, -0.03, pop(il, 20, 24))
            label(ctx, "customer.\"", 540, 1500, 110, YEL, 0.03, pop(il, 26, 29))
        else:
            label(ctx, "*strut strut*", 540, 470, 80, CYAN, 0.03, pop(il, 2, 5))
    elif il < 80:
        label(ctx, "\"WELL, HELLO!\"", 540, 1470, 130, PINK, -0.04, pop(il, 42, 46))
    elif il < 96:
        label(ctx, "\"Take the TRAY!\"", 540, 1470, 110, YEL, 0.03, pop(il, 82, 86))
    elif 170 <= il < 220:
        label(ctx, "*GULP! GULP!*", 540, 470, 100, ORANGE, -0.03, pop(il, 172, 175))
    elif il >= 220:
        label(ctx, "\"HEY!!\"", 540, 1470, 170, RED, 0.04, pop(il, 222, 225))


def s5(ctx, f):
    lf = f - 370
    if lf < 260:
        finale(ctx, f, lf)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (200, s3), (300, s4), (370, s5)]
CUTS = (60, 130, 200, 300, 370, 500, 540, 630)


def render(f):
    import sketch
    sketch.BOIL[0] = f // 4
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.1, 0.05, 0.15, 0.16)
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
                              "-i", "out/samples_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
