"""'Diet Starts Tomorrow' - original, general-audience comedy short, ~22s.
Hook: ECU of Dad at midnight in the fridge glow, cheeks stuffed with cake: "IT'S NOT WHAT IT LOOKS LIKE!"
Morning: Dad with one lettuce leaf, "NEW ME!" - calendar says DAY 1.
Beat 1: the kid's pancake tower glows with an angel choir; Dad drools, chews his leaf: "I'M... FINE."
Beat 2: 11 PM, ninja tiptoe to the fridge; POV from INSIDE the fridge: "JUST ONE BITE..." - grabs the whole cake.
Beat 3: lights click on, kid catches him. Dad puts the lettuce leaf on the cake: "IT'S... SALAD."
Twist: whip pan - Mom is crouched at the freezer with a tub of ice cream, also on a diet. Family eats cake together:
"DIET STARTS TOMORROW!" Calendar flips to TOMORROW. Loops to the opening face."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
import scenes13
from scenes13 import card as _card13
import random

BOY = doodle.BOY
DAD = doodle.DAD
MOM = doodle.MOM_G
N = 660
FLOOR = 1460
RED = hx('ff3b5c')
BLUE = hx('1f8bff')
GREEN = hx('3ccf4e')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')

CAPS = {
    'p1': [[("WHEN DAD SAYS", OUT)], [("\"MY DIET STARTS TODAY\"", RED)]],
    'p2': [[("9 AM:", OUT)], [("THE PANCAKE TEST", BLUE)]],
    'p3': [[("11 PM:", OUT)], [("THE FRIDGE IS CALLING", ORANGE)]],
    'p4': [[("THEN THE", OUT)], [("LIGHTS COME ON", PURPLE)]],
    'p5': [[("PLOT TWIST:", OUT)], [("MOM IS ON A DIET TOO", RED)]],
}
scenes13.CAPS = CAPS
card = _card13


def label(ctx, s, x, y, size, col, ang=0, t=1.0):
    if t <= 0:
        return
    sc = 0.5 + 0.5 * eout(min(1, t * 2)) + 0.08 * math.sin(min(1, t) * math.pi)
    ctx.save(); ctx.translate(x, y); ctx.scale(sc, sc)
    text(ctx, s, 0, 0, size, col, ang=ang, ow=12, maxw=860)
    ctx.restore()


def cam(ctx, cx, cy, z, rot=0, shake=0, f=0, sx=W / 2, sy=H / 2):
    rnd = random.Random(f * 31 + 7)
    dx, dy = (rnd.uniform(-1, 1) * shake, rnd.uniform(-1, 1) * shake) if shake else (0, 0)
    ctx.translate(sx + dx, sy + dy); ctx.rotate(math.radians(rot)); ctx.scale(z, z); ctx.translate(-cx, -cy)


def rect_r(ctx, x, y, w, h, r):
    ctx.new_path(); ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); ctx.close_path()


def rays(ctx, x, y, r0, r1, t, col=(1, 0.97, 0.6), a=0.8, n=12):
    for k in range(n):
        ang = k * 2 * math.pi / n + t
        ctx.move_to(x + math.cos(ang) * r0, y + math.sin(ang) * r0)
        ctx.line_to(x + math.cos(ang - 0.09) * r1, y + math.sin(ang - 0.09) * r1)
        ctx.line_to(x + math.cos(ang + 0.09) * r1, y + math.sin(ang + 0.09) * r1); ctx.close_path()
    setc(ctx, col + (a,)); ctx.fill()


_SCR = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4))


def face(ctx, ch, p, cx, cy, Rt, rot=0.0, f_=1, head_only=False):
    b = draw_hip(_SCR, 0, 0, 1, f_, ch, p)
    hd, R = b['head'], b['R']
    s = Rt / R
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot)
    if head_only:
        ctx.rectangle(-4 * Rt, -4 * Rt, 8 * Rt, 4.9 * Rt); ctx.clip()
    ctx.scale(s, s); ctx.translate(-hd[0], -hd[1])
    draw_hip(ctx, 0, 0, 1, f_, ch, p)
    ctx.restore()


def talk(lf, a='open', b='scream', rate=4):
    return a if (lf // rate) % 2 == 0 else b


# ------------------------------------------------------------------ props
FROST = hx('fff4f8'); PINK = hx('ff7fb0'); SPONGE = hx('8a4a2a')


def stuffed(ctx, ch, cx, cy, Rt, lf=0, cream=True, f_=1):
    """hamster cheeks + cream moustache on a face() drawn at (cx, cy, Rt)"""
    wob = 1 + 0.04 * math.sin(lf * 0.9)
    for sx in (-1, 1):
        ellipse(ctx, cx + sx * Rt * 0.66 + f_ * Rt * 0.08, cy + Rt * 0.42, Rt * 0.36 * wob, Rt * 0.3 / wob); fl(ctx, ch['skin'], Rt * 0.03)
        ellipse(ctx, cx + sx * Rt * 0.62 + f_ * Rt * 0.08, cy + Rt * 0.44, Rt * 0.16, Rt * 0.08); setc(ctx, (1, 0.5, 0.58, 0.6)); ctx.fill()
    # tiny squished mouth
    mx = cx + f_ * Rt * 0.12; my = cy + Rt * 0.56
    ellipse(ctx, mx, my, Rt * 0.07, Rt * 0.05); fl(ctx, hx('8a1c2c'), Rt * 0.025)
    if cream:
        for k, (dx, dy, r) in enumerate(((-0.12, 0.42, 0.11), (0.0, 0.4, 0.13), (0.14, 0.43, 0.1), (0.24, 0.5, 0.07), (-0.02, 0.66, 0.06))):
            ellipse(ctx, mx + dx * Rt, cy + dy * Rt, r * Rt, r * Rt * 0.8); fl(ctx, FROST, Rt * 0.02)
        ellipse(ctx, mx + 0.05 * Rt, cy + 0.38 * Rt, 0.05 * Rt, 0.04 * Rt); setc(ctx, hx('e0263a')); ctx.fill()   # sprinkle


def crumbs(ctx, lf, x, y, seed=3, n=8, spread=260):
    rnd = random.Random(seed)
    for k in range(n):
        st = rnd.uniform(0, 30); ph = ((lf - st) % 30) / 30
        a = rnd.uniform(-math.pi, 0)
        cx_ = x + math.cos(a) * spread * ph; cy_ = y + math.sin(a) * spread * 0.5 * ph + 500 * ph * ph
        r = rnd.uniform(8, 16)
        poly(ctx, [(cx_, cy_ - r), (cx_ + r, cy_ + r * 0.4), (cx_ - r * 0.7, cy_ + r * 0.6)]); fl(ctx, SPONGE if k % 2 else FROST, 3)


def cake(ctx, x, y, s=1.0, cut=True, leaf=False):
    """round layer cake, base centre at (x, y)"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 6, 250, 50); fl(ctx, hx('dfe6f2'), 7)            # plate
    rect_r(ctx, -200, -230, 400, 230, 30); fl(ctx, SPONGE, 8)
    ctx.rectangle(-200, -140, 400, 30); setc(ctx, PINK); ctx.fill()   # jam layer
    rect_r(ctx, -206, -260, 412, 90, 40); fl(ctx, FROST, 8)
    for k in range(7):                                                 # drips
        dx = -170 + k * 56
        rect_r(ctx, dx, -200, 30, 40 + (k * 23) % 50, 15); setc(ctx, FROST); ctx.fill()
    for k in range(5):                                                 # strawberries
        sx = -150 + k * 75
        ctx.new_path(); ctx.move_to(sx - 26, -262); ctx.curve_to(sx - 26, -300, sx + 26, -300, sx + 26, -262); ctx.curve_to(sx + 14, -230, sx - 14, -230, sx - 26, -262)
        fl(ctx, hx('ff3b5c'), 5)
        poly(ctx, [(sx - 14, -292), (sx, -306), (sx + 14, -292), (sx, -286)]); fl(ctx, GREEN, 3)
    if cut:   # missing wedge, front-right
        poly(ctx, [(60, -270), (210, -250), (210, 0), (60, 0)]); setc(ctx, hx('dfe6f2')); ctx.fill()
        ctx.rectangle(56, -262, 10, 262); setc(ctx, SPONGE); ctx.fill()
        ctx.move_to(60, -265); ctx.line_to(60, 0); ink(ctx, 7); ctx.stroke()
    if leaf:
        lettuce(ctx, 0, -330, 1.2, 0.15)
    ctx.restore()


def slice_(ctx, x, y, s=1.0, a=0.0, bite=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-90, 0), (90, 0), (90, -150), (-90, -60)]); fl(ctx, SPONGE, 7)
    poly(ctx, [(-90, -42), (90, -100), (90, -80), (-90, -24)]); setc(ctx, PINK); ctx.fill()
    poly(ctx, [(-96, -60), (96, -160), (96, -128), (-96, -40)]); fl(ctx, FROST, 6)
    if bite > 0:
        for k in range(3):
            ellipse(ctx, 90, -150 + k * 45, 40 * bite, 34); setc(ctx, hx('241a4a')); ctx.fill()
    ctx.restore()


def lettuce(ctx, x, y, s=1.0, a=0.0, wilt=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a + wilt * 0.9); ctx.scale(s, s * (1 - 0.3 * wilt))
    ctx.new_path(); ctx.move_to(0, 60)
    ctx.curve_to(-90 - 20 * wilt, 40, -80, -60 + 60 * wilt, 0, -80 + 70 * wilt)
    ctx.curve_to(80, -60 + 60 * wilt, 90 + 20 * wilt, 40, 0, 60); ctx.close_path()
    fl(ctx, lerp_c(hx('7fe05a'), hx('9aa060'), wilt), 6)
    ctx.move_to(0, 55); ctx.line_to(0, -60 + 60 * wilt); setc(ctx, hx('d8ffb0')); ctx.set_line_width(8); ctx.stroke()
    for k in (-1, 1):
        ctx.move_to(0, 10); ctx.line_to(k * 50, -20 + 30 * wilt); ctx.stroke()
    ctx.restore()


def lerp_c(a, b, t):
    return tuple(lerp(a[i], b[i], t) for i in range(3))


def bowl(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-70, -20); ctx.curve_to(-70, 40, 70, 40, 70, -20); ctx.close_path(); fl(ctx, hx('ffffff'), 6)
    ellipse(ctx, 0, -20, 70, 14); fl(ctx, hx('e8f0ff'), 5)
    ctx.restore()


def fork(ctx, x, y, a=0.0, s=1.0, col=hx('c8d0e0')):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -9, 0, 18, 150, 9); fl(ctx, col, 5)
    rect_r(ctx, -26, -26, 52, 34, 10); fl(ctx, col, 5)
    for k in range(4):
        ctx.rectangle(-24 + k * 14, -80, 8, 60); fl(ctx, col, 4)
    ctx.restore()


def spoon(ctx, x, y, a=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -9, 0, 18, 160, 9); fl(ctx, hx('c8d0e0'), 5)
    ellipse(ctx, 0, -30, 32, 44); fl(ctx, hx('c8d0e0'), 5)
    ctx.restore()


def tub(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    poly(ctx, [(-140, -170), (140, -170), (115, 60), (-115, 60)]); fl(ctx, hx('ffe9a8'), 8)
    poly(ctx, [(-132, -100), (132, -100), (126, -50), (-126, -50)]); setc(ctx, hx('ff8fb8')); ctx.fill()
    ellipse(ctx, 0, -175, 150, 34); fl(ctx, hx('fff6dc'), 7)
    for k, (dx, dy) in enumerate(((-60, -190), (10, -200), (70, -188))):
        ellipse(ctx, dx, dy, 52, 36); fl(ctx, hx('fffaf0'), 5)
    ellipse(ctx, 0, -20, 40, 40); setc(ctx, hx('ffffff')); ctx.fill()
    ctx.restore()


def pancakes(ctx, x, y, n=9, s=1.0, lf=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 10, 260, 46); fl(ctx, hx('ffffff'), 7)
    for k in range(n):
        yy = -k * 46
        wob = 6 * math.sin(k * 1.7)
        rect_r(ctx, -190 + wob, yy - 44, 380, 50, 24); fl(ctx, hx('f2b35a') if k % 2 else hx('e8a245'), 6)
        ctx.move_to(-160 + wob, yy - 30); ctx.line_to(160 + wob, yy - 30); setc(ctx, hx('ffd890')); ctx.set_line_width(6); ctx.stroke()
    top = -n * 46
    # syrup cascade
    pour = 0.5 + 0.5 * math.sin(lf * 0.15)
    ctx.new_path(); ctx.move_to(-180, top + 4); ctx.curve_to(-120, top - 30, 120, top - 30, 180, top + 4)
    for k in range(6):
        dx = 170 - k * 68
        ctx.line_to(dx, top + 40 + (k * 37) % 90 + 30 * pour); ctx.line_to(dx - 30, top + 10)
    ctx.close_path(); fl(ctx, hx('b5560f'), 5)
    rect_r(ctx, -50, top - 70, 100, 60, 10); fl(ctx, hx('fff07a'), 6)    # butter pat
    ctx.restore()


def calendar(ctx, x, y, txt, s=1.0, flip=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rect_r(ctx, -110, -90, 220, 200, 16); fl(ctx, (1, 1, 1), 6)
    ctx.rectangle(-110, -90, 220, 50); setc(ctx, RED); ctx.fill()
    rect_r(ctx, -110, -90, 220, 200, 16); ink(ctx, 6); ctx.stroke()
    for dx in (-60, 60):
        ellipse(ctx, dx, -90, 10, 16); fl(ctx, hx('c8d0e0'), 4)
    if flip > 0:   # page tearing off
        ctx.save(); ctx.translate(0, -40); ctx.rotate(-1.2 * flip); ctx.translate(120 * flip, -200 * flip)
        rect_r(ctx, -110, 0, 220, 150, 10); fl(ctx, (1, 1, 1, 1 - flip), 5); ctx.restore()
    text(ctx, txt, 0, 36, 44, (1, 1, 1) if False else hx('241a4a'), outline=(1, 1, 1), ow=2, shadow=False, maxw=190)
    ctx.restore()


# ------------------------------------------------------------------ sets
def kitchen(ctx, night=False, cal="DAY 1"):
    wall = hx('2b2f6e') if night else hx('ffe08a')
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, wall); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 120, -3000, 46, 6000); setc(ctx, dark(wall, 0.94)); ctx.fill()
    # upper cabinets
    for cx in (-200, 160):
        rect_r(ctx, cx, 520, 300, 220, 14); fl(ctx, hx('3a4a9a') if night else hx('ff9f5a'), 8)
        ellipse(ctx, cx + 150, 700, 12, 12); fl(ctx, hx('ffd23f'), 4)
    calendar(ctx, 830, 720, cal, 0.9)
    # counter
    ctx.rectangle(-3000, 1130, 7000, 40); fl(ctx, hx('4a5aa0') if night else hx('fff2c8'), 8)
    ctx.rectangle(-3000, 1170, 7000, FLOOR - 1170); setc(ctx, hx('3a4a9a') if night else hx('ff9f5a')); ctx.fill()
    for i in range(-10, 12):
        ctx.rectangle(i * 260 + 20, 1200, 220, FLOOR - 1230); ink(ctx, 6); ctx.stroke()
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('3a2f5a') if night else hx('c98a52')); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()


def fridge(ctx, x, open_=0.0, glow=True):
    """fridge body left edge x, top 500, width 340, bottom FLOOR"""
    w, top = 340, 520
    if open_ > 0 and glow:
        # light beam spilling out to the left
        poly(ctx, [(x, top + 40), (x, FLOOR), (x - 900 * open_, FLOOR + 300), (x - 700 * open_, top - 200)]); setc(ctx, (0.85, 0.95, 1, 0.35 * open_)); ctx.fill()
    rect_r(ctx, x, top, w, FLOOR - top, 26); fl(ctx, hx('e8f0ff'), 9)
    if open_ > 0:
        rect_r(ctx, x + 20, top + 20, w - 40, FLOOR - top - 40, 16); fl(ctx, hx('fffbe0'), 6)
        for sy in (800, 1050, 1250):
            ctx.move_to(x + 20, sy); ctx.line_to(x + w - 20, sy); ink(ctx, 6); ctx.stroke()
        cake(ctx, x + w / 2, 1050, 0.55)
        # open door swings toward camera
        dw = w * open_ * 0.6
        poly(ctx, [(x + w, top), (x + w + dw, top - 40), (x + w + dw, FLOOR + 40), (x + w, FLOOR)]); fl(ctx, hx('d6e2fa'), 8)
    else:
        ctx.move_to(x, 860); ctx.line_to(x + w, 860); ink(ctx, 7); ctx.stroke()
        rect_r(ctx, x + w - 50, 620, 20, 160, 10); fl(ctx, hx('9aa6c4'), 5)
        rect_r(ctx, x + w - 50, 920, 20, 220, 10); fl(ctx, hx('9aa6c4'), 5)


# ------------------------------------------------------------------ shots
def opening_face(ctx, f, lf, lab=True):
    """ECU: Dad caught at midnight in the fridge glow, cheeks stuffed"""
    sh = shake_at(lf, [0], 12, 22) + 1.5
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 60)), 0, sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('1f2560')); ctx.fill()
    rays(ctx, 540, 1100, 260, 1500, lf * 0.02, col=(0.75, 0.9, 1), a=0.35, n=16)
    p = P(eye='shock', mouth='flat', head=0)
    face(ctx, DAD, p, 540 + 5 * math.sin(lf * 0.6), 1040, 340, 0.03)
    stuffed(ctx, DAD, 540 + 5 * math.sin(lf * 0.6), 1040, 340, lf)
    sweat(ctx, 880, 820 + (lf % 18) * 5, 2.0)
    # cake slice + fork in hand
    slice_(ctx, 830, 1330, 1.3, -0.25, 1.0)
    ellipse(ctx, 780, 1380, 70, 60); fl(ctx, DAD['skin'], 8)
    crumbs(ctx, lf, 600, 1260, seed=4)
    ctx.restore()
    if lab:
        label(ctx, "\"THIS IS NOT CAKE!\"", 540, 1470, 110, (1, 1, 1), -0.04, pop(lf, 0, 4) if lf > 0 else 1)


def s1(ctx, f):
    if f < 56:
        opening_face(ctx, f, f)
    else:
        lf = f - 56
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(lf, 0, 54)), 0, 2 + shake_at(lf, [0], 8, 12), f)
        kitchen(ctx)
        rays(ctx, 540, 900, 200, 1500, lf * 0.03, col=(1, 1, 1), a=0.25, n=14)
        dp = P(eye='happy', mouth='grin', rsh=170, rel=-10, lsh=-120, lel=-80, head=-4, torso=-3)
        b = draw_hip(ctx, 520, 1400, 1.7, 1, DAD, dp)
        hx_, hy_ = b['front']
        bowl(ctx, hx_, hy_ - 40, 1.4)
        lettuce(ctx, hx_, hy_ - 95, 0.5, 0.1)
        for k in range(4):
            sparkle(ctx, hx_ + 110 * math.cos(lf * 0.2 + k * 1.6), hy_ - 90 + 80 * math.sin(lf * 0.2 + k * 1.6), 22)
        ctx.restore()
        label(ctx, "THAT MORNING...", 540, 590, 60, hx('ffe14d'), 0.0, pop(lf, 0, 4))
        label(ctx, "\"NEW ME!\"", 540, 1480, 120, (1, 1, 1), -0.04, pop(lf, 8, 12))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 60:
        # low angle hero shot of the kid's pancake tower
        ctx.save(); cam(ctx, 540, 1100, 1.0 + 0.1 * eout(pop(lf, 0, 60)), -2 + 4 * pop(lf, 0, 60), 2, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb3d1')); ctx.fill()
        rays(ctx, 540, 820, 200, 1500, lf * 0.03, col=(1, 0.97, 0.7), a=0.6, n=18)
        ctx.rectangle(-500, 1360, 2200, 900); fl(ctx, hx('ff7fb0'), 8)    # table
        pancakes(ctx, 540, 1370, 9, 1.0, lf)
        for k in range(6):
            a = lf * 0.08 + k * 1.05
            sparkle(ctx, 540 + 330 * math.cos(a), 950 + 260 * math.sin(a), 26 + 8 * math.sin(lf * 0.3 + k))
        # the kid happily digging in at the right
        face(ctx, BOY, P(eye='happy', mouth=talk(lf, 'open', 'grin', 6), head=-6), 880, 1180, 130, 0.0, -1)
        fork(ctx, 760, 1200, -0.6, 0.8)
        ctx.restore()
        label(ctx, "*ANGELIC CHOIR*", 540, 1520 - 40, 84, hx('fff27a'), -0.03, pop(lf, 4, 8))
    else:
        il = lf - 60
        # Dad ECU: drooling at the pancakes, then sadly chewing his leaf
        late = il >= 32
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.12 * eout(pop(il, 0, 60)), 0, 2 + shake_at(il, [22], 10, 18), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('c8b6ff')); ctx.fill()
        rays(ctx, 540, 960, 300, 1500, il * 0.02, col=(1, 1, 1), a=0.35, n=18)
        face(ctx, DAD, P(eye='shock' if not late else 'closed', mouth='open' if not late else talk(il, 'flat', 'wavy', 5), head=4), 540, 1000, 340, 0.0)
        if not late:
            # drool waterfall
            d = eout(pop(il, 2, 20))
            ctx.new_path(); ctx.move_to(555, 1170); ctx.curve_to(560, 1170 + 200 * d, 545, 1300 * 1 + 0 * d, 550, 1170 + 420 * d)
            setc(ctx, hx('9fe0ff', 0.9)); ctx.set_line_width(26); ctx.stroke()
            ellipse(ctx, 550, 1170 + 420 * d, 22, 26); setc(ctx, hx('9fe0ff')); ctx.fill()
            # pancake reflected in the eyes
            for ex in (540 - 0.3 * 340 + 34, 540 + 0.32 * 340 + 34):
                ctx.save(); ctx.translate(ex, 1020); ctx.scale(0.12, 0.12); pancakes(ctx, 0, 300, 5, 1.0, il); ctx.restore()
        else:
            u = pop(il, 32, 60)
            lettuce(ctx, 560, 1240, 1.0, 0.0, u)
            ctx.save(); ctx.translate(560, 1240); ctx.restore()
            sweat(ctx, 860, 760 + (il % 18) * 6, 2.0)
        ctx.restore()
        if il >= 18 and not late:
            label(ctx, "*GRRRRWL*", 540, 1460, 110, ORANGE, 0.05, pop(il, 18, 22))
        if late:
            label(ctx, "\"I'M... FINE.\"", 540, 1480, 120, (1, 1, 1), -0.03, pop(il, 34, 38))
    card(ctx, 'p2', f, 114, 226)


def ninja_pose(lf):
    ph = lf * 0.35
    return P(eye='smug', mouth='grin', torso=14, head=-8, rsh=70 + 20 * math.sin(ph), rel=-90, lsh=-50, lel=-70,
             lhip=-30 + 20 * math.sin(ph), lkn=40, rhip=24 - 20 * math.sin(ph), rkn=-10)


def s3(ctx, f):
    lf = f - 230
    if lf < 66:
        # night kitchen: ninja tiptoe to the fridge
        op = eout(pop(lf, 40, 50))
        ctx.save(); cam(ctx, 560, 1050, 1.0 + 0.08 * eout(pop(lf, 40, 66)), 0, shake_at(lf, [40], 8, 12), f)
        kitchen(ctx, night=True)
        fridge(ctx, 640, op)
        ellipse(ctx, 160, 640, 50, 50); setc(ctx, hx('fff6c8', 0.0)); ctx.fill()
        tip = abs(math.sin(lf * 0.35)) * 26
        dx = lerp(-150, 430, eout(pop(lf, 0, 40)))
        draw_hip(ctx, dx, FLOOR - 120 - tip, 1.45, 1, DAD, ninja_pose(lf) if lf < 44 else P(eye='shock', mouth='grin', torso=6, rsh=150, rel=-30, lsh=-140, lel=-30))
        if lf >= 44:
            for k in range(5):
                sparkle(ctx, 810 + 140 * math.cos(lf * 0.2 + k * 1.3), 1000 + 200 * math.sin(lf * 0.2 + k * 1.3), 24)
        ctx.restore()
        if lf < 40:
            label(ctx, "*TIPTOE TIPTOE*", 540, 1480, 90, hx('c8b6ff'), -0.04, pop(lf, 4, 8))
        else:
            label(ctx, "*CREEEAK*", 540, 1480, 110, hx('ffe14d'), 0.04, pop(lf, 40, 44))
    else:
        il = lf - 66
        # POV from INSIDE the fridge
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.1 * eout(pop(il, 0, 70)), 0, 1.5 + shake_at(il, [44], 10, 18), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('1f2560')); ctx.fill()
        rays(ctx, 540, 950, 260, 1500, il * 0.02, col=(0.85, 0.95, 1), a=0.3, n=16)
        face(ctx, DAD, P(eye='glare' if il < 44 else 'shock', mouth='grin' if il < 44 else 'open', head=-4), 540, 880, 330, 0.0)
        # fork raised
        fy = 980 - 30 * math.sin(il * 0.3)
        fork(ctx, 920, fy, 0.2, 1.4)
        ellipse(ctx, 905, fy + 210, 60, 52); fl(ctx, DAD['skin'], 8)
        # fridge interior frame (foreground)
        ctx.new_path(); ctx.rectangle(-500, -500, 2200, 3000); ctx.rectangle(120, 260, 840, 1260)
        ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); setc(ctx, hx('eef4ff')); ctx.fill(); ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
        ctx.rectangle(120, 260, 840, 1260); ink(ctx, 10); ctx.stroke()
        # jars on the side shelves
        for jx, jy, col in ((40, 600, hx('ff8a1f')), (40, 980, GREEN), (1030, 700, hx('ff3b5c')), (1030, 1060, hx('ffe14d'))):
            rect_r(ctx, jx - 50, jy - 80, 100, 160, 18); fl(ctx, col, 6)
            rect_r(ctx, jx - 54, jy - 100, 108, 34, 8); fl(ctx, hx('ffffff'), 5)
        # glass shelf + cake in the foreground
        grab = eout(pop(il, 44, 56))
        ctx.rectangle(120, 1430, 840, 24); setc(ctx, (0.8, 0.95, 1, 0.8)); ctx.fill(); ink(ctx, 6); ctx.stroke()
        cake(ctx, 540, 1430 - 560 * grab * 0 , 1.1, cut=False) if grab == 0 else cake(ctx, 540 + 40 * grab, 1430 - 900 * grab, 1.1, cut=False)
        ctx.restore()
        if il < 44:
            label(ctx, "\"JUST ONE BITE...\"", 540, 1480, 100, (1, 1, 1), -0.03, pop(il, 4, 8))
        else:
            label(ctx, "*YOINK*", 540, 1480, 120, hx('ffe14d'), 0.05, pop(il, 44, 48))
    card(ctx, 'p3', f, 234, 366)


def s4(ctx, f):
    lf = f - 370
    if lf < 62:
        # lights on: wide, Dad frozen mid-bite with the whole cake, kid at the switch
        on = lf >= 6
        ctx.save(); cam(ctx, 560, 1000, 1.0 + 0.1 * eout(pop(lf, 6, 30)), 0, shake_at(lf, [6], 12, 24), f)
        kitchen(ctx, night=not on)
        fridge(ctx, 700, 1.0, glow=not on)
        # Dad, cheeks stuffed, cake in arms
        dp = P(eye='shock', mouth='flat', rsh=100, rel=-60, lsh=-100, lel=-60, torso=-4, lhip=10, rhip=-14)
        b = draw_hip(ctx, 430, FLOOR - 120, 1.55, 1, DAD, dp)
        hd = b['head']
        stuffed(ctx, DAD, hd[0] - 4, hd[1] - 0, b['R'] * 1.0, lf)
        cake(ctx, (b['front'][0] + b['back'][0]) / 2, b['front'][1] + 40, 0.62, cut=True)
        # kid in the doorway at right with hand on the switch
        kp = P(eye='shock' if on else 'normal', mouth='open' if on else 'flat', rsh=150, rel=-30, lsh=-10)
        draw_hip(ctx, 880, FLOOR - 70, 1.0, -1, BOY, kp)
        rect_r(ctx, 930, 960, 50, 80, 8); fl(ctx, (1, 1, 1), 5)
        if not on:
            ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, (0.05, 0.05, 0.2, 0.35)); ctx.fill()
        ctx.restore()
        if lf < 6:
            pass
        elif lf < 24:
            label(ctx, "*CLICK*", 540, 1480, 110, hx('ffe14d'), 0.05, pop(lf, 6, 10))
        else:
            label(ctx, "\"DAD?!\"", 540, 1480, 130, (1, 1, 1), -0.04, pop(lf, 24, 28))
        if 6 <= lf < 9:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.7 * (1 - (lf - 6) / 3))); ctx.fill()
    else:
        il = lf - 62
        # Dad ECU: places the lettuce leaf on the cake
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.1 * eout(pop(il, 0, 60)), 0, shake_at(il, [20], 8, 14), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('b6f0a0')); ctx.fill()
        rays(ctx, 540, 960, 300, 1500, il * 0.02, col=(1, 1, 1), a=0.35, n=18)
        face(ctx, DAD, P(eye='smug' if il > 14 else 'normal', mouth='grin', head=-6), 540, 860, 300, 0.0)
        stuffed(ctx, DAD, 540, 860, 300, il) if il < 10 else None
        u = eout(pop(il, 12, 20))
        cake(ctx, 540, 1430, 0.95, cut=True)
        lettuce(ctx, lerp(900, 540, u), lerp(900, 1100, u), 1.1, 0.15 + (1 - u) * 1.2)
        if il >= 20:
            sparkle(ctx, 640, 1060, 30); sparkle(ctx, 440, 1120, 24)
        ctx.restore()
        label(ctx, "\"IT'S... SALAD.\"", 540, 1480, 120, (1, 1, 1), -0.03, pop(il, 22, 26))
    card(ctx, 'p4', f, 374, 496)


def s5(ctx, f):
    lf = f - 500
    if lf < 72:
        # whip pan to Mom at the freezer, caught with a tub of ice cream
        pan = eout(pop(lf, 0, 10))
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(lf, 10, 70)), 0, shake_at(lf, [10], 12, 22) + 1.5, f, sx=W / 2 + (1 - pan) * 1400)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('1d4a6a')); ctx.fill()
        rays(ctx, 540, 1100, 260, 1500, lf * 0.02, col=(0.75, 1, 0.95), a=0.35, n=16)
        face(ctx, MOM, P(eye='shock', mouth='flat', head=0), 540 + 4 * math.sin(lf * 0.7), 960, 320, -0.04)
        stuffed(ctx, MOM, 540 + 4 * math.sin(lf * 0.7), 960, 320, lf, cream=False)
        tub(ctx, 330, 1420, 1.2)
        spoon(ctx, 620, 1120, 0.5, 1.2)
        ellipse(ctx, 330, 1460, 90, 60); fl(ctx, MOM['skin'], 8)
        ctx.restore()
        if lf < 10:
            hlines(ctx, lf, 0.7)
        label(ctx, "\"...I CAN EXPLAIN.\"", 540, 1480, 110, (1, 1, 1), -0.03, pop(lf, 16, 20))
        card(ctx, 'p5', f, 504, 616)
    elif lf < 120:
        il = lf - 72
        # the whole family eats the cake together at midnight
        ctx.save(); cam(ctx, 540, 1060, 1.06 - 0.06 * eout(pop(il, 0, 48)), 0, shake_at(il, [0], 8, 14), f)
        kitchen(ctx, night=True, cal="TOMORROW" if il >= 20 else "DAY 1")
        if 14 <= il < 24:
            calendar(ctx, 830, 720, "DAY 1", 0.9, pop(il, 14, 24))
        rays(ctx, 540, 1150, 200, 1500, il * 0.03, col=(1, 0.95, 0.6), a=0.25, n=16)
        chew = (il // 5) % 2
        for x, ch, k, f_ in ((250, DAD, 1.35, 1), (820, MOM, 1.25, -1), (540, BOY, 1.0, 1)):
            hy = 1180 if ch is BOY else 1330
            p = P(eye='happy', mouth='open' if chew else 'grin', rsh=120, rel=-70, lsh=-10, head=4 * math.sin(il * 0.4 + x))
            b = draw_hip(ctx, x, hy, k, f_, ch, p)
            fork(ctx, b['front'][0], b['front'][1] - 20, (0.3 if f_ > 0 else -0.3), 0.6)
        rect_r(ctx, 40, 1250, 1000, 70, 20); fl(ctx, hx('ff9f5a'), 8)   # table top
        ctx.rectangle(100, 1320, 50, 200); fl(ctx, hx('c96a2a'), 6); ctx.rectangle(930, 1320, 50, 200); fl(ctx, hx('c96a2a'), 6)
        cake(ctx, 540, 1260, 0.6, cut=True)
        crumbs(ctx, il, 540, 1080, seed=8, n=10, spread=320)
        ctx.restore()
        label(ctx, "\"DIET STARTS TOMORROW!\"", 540, 1480, 96, hx('ffe14d'), -0.03, pop(il, 4, 8))
        card(ctx, 'p5', f, 504, 616)
    else:
        il = lf - 120
        opening_face(ctx, f, il, True)
        card(ctx, 'p1', f, 620)


SHOTS = [(0, s1), (110, s2), (230, s3), (370, s4), (500, s5)]
CUTS = (56, 110, 170, 230, 296, 370, 432, 500, 572, 620)


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
                              "-i", "out/diet_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
