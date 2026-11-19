"""'ONE TRIP. No Matter What.' - original, general-audience comedy short, 22s.
Hook: Dad ECU, red, gritted teeth, veins, purple fingers holding 20 bag handles: "ONE. TRIP."
Beat 1: driveway, Mom "Need HELP?" / Dad "Two trips? NEVER." -> load-up montage: 4 BAGS, 8 BAGS, 12 BAGS,
 WATERMELON, ONE IN THE TEETH, AND THE EGGS -> wobbling tower man.
Beat 2: wobble-walk to the door, door is locked, keys in pocket -> rings the doorbell with his NOSE.
Beat 3: kid opens: "PASSWORD?" / "OPEN. THE. DOOR!!", kitchen: eggs slide off -> caught on his foot,
 everything slammed on the counter "ONE TRIP!!"
Twist: Mom "...where's the MILK?" -> milk glowing alone in the trunk -> Dad ECU "...that's TWO trips."
 -> he loads EVERYTHING back on to go get it: "From the TOP." -> opening ECU (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, _SCR
from scenes48 import label1, label2
from scenes58 import sweat, twitch
import scenes13
from scenes13 import card as _card13
import random

DAD = dict(doodle.DAD, shirt=hx('2fb5a0'), pants=hx('3d5a9e'), sleeve=0.45)
MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'))
BOY = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ffc93c'))
N = 660
FLOOR = 1450
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
GOLD = hx('ffc93c')
SKY = hx('7fd0ff')
WHITE = (1, 1, 1)
BROWN = hx('8a4a2c')
KRAFT = hx('d9a066')
BRUISE = hx('9a5ad8')

CAPS = {
    'p1': [[("GROCERIES.", OUT)], [("ONE TRIP. ", RED), ("NO MATTER WHAT.", OUT)]],
    'p2': [[("THE FRONT DOOR...", OUT)], [("IS LOCKED.", RED)]],
    'p3': [[("MEANWHILE...", OUT)], [("IN THE CAR:", BLUE)]],
}
scenes13.CAPS = CAPS
card = _card13

LOADS = ["4 BAGS!", "8 BAGS!", "12 BAGS!", "+ WATERMELON!", "+ ONE IN THE TEETH!", "+ THE EGGS!"]
LT = [100, 116, 132, 150, 166, 182]
LCOL = [WHITE, YEL, ORANGE, GREEN, PINK, GOLD]
BAGC = [KRAFT, hx('ffffff'), hx('ffd23f'), hx('9fe0ff'), KRAFT, hx('ffb3d9')]


# ------------------------------------------------------------------ props
def bag(ctx, x, y, s, col, item, a=0.0):
    """grocery bag hanging from its handle point (x, y)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    # item poking out
    if item == 0:      # leafy greens
        for dx, c in ((-24, GREEN), (0, hx('5ad86a')), (22, GREEN)):
            ellipse(ctx, dx, 34, 22, 40, dx * 0.01); fl(ctx, c, 5)
    elif item == 1:    # bread stick
        ctx.save(); ctx.translate(18, 30); ctx.rotate(0.35)
        rect_r(ctx, -14, -60, 28, 110, 14); fl(ctx, hx('e8a85a'), 5)
        for j in range(3):
            ctx.move_to(-8, -40 + j * 24); ctx.line_to(8, -50 + j * 24)
        ink(ctx, 4); ctx.stroke(); ctx.restore()
    elif item == 2:    # bottle
        rect_r(ctx, -40, 0, 34, 70, 10); fl(ctx, hx('ff6b3d'), 5)
        rect_r(ctx, -32, -20, 18, 26, 5); fl(ctx, WHITE, 4)
    elif item == 3:    # apples
        for dx in (-22, 18):
            ellipse(ctx, dx, 40, 22, 20); fl(ctx, RED, 5)
    # handles
    ctx.new_path(); ctx.move_to(-30, 60); ctx.curve_to(-26, -10, 26, -10, 30, 60); ink(ctx, 7); ctx.stroke()
    # body
    poly(ctx, [(-58, 50), (58, 50), (66, 190), (-66, 190)]); fl(ctx, col, 6)
    ctx.move_to(-58, 72); ctx.line_to(58, 72); setc(ctx, dark(col, 0.85)); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def bag_cluster(ctx, x, y, n, s, lf, seed=0, newest=1.0):
    """n bags fanned from one fist"""
    if n <= 0:
        return
    for i in range(n):
        spread = (i - (n - 1) / 2) * 0.22
        sw = 0.05 * math.sin(lf * 0.5 + i * 1.7 + seed)
        sc = s * (0.5 + 0.5 * newest if i >= n - 2 else 1)
        bag(ctx, x, y, sc, BAGC[(i + seed) % len(BAGC)], (i + seed) % 4, spread + sw)


def watermelon(ctx, x, y, r, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ellipse(ctx, 0, 0, r * 1.25, r); fl(ctx, hx('2e9e4a'), max(5, r * 0.06))
    for k in (-0.6, -0.2, 0.2, 0.6):
        ctx.new_path(); ctx.move_to(k * r * 1.2, -r * 0.95); ctx.curve_to(k * r * 1.6, -r * 0.3, k * r * 1.6, r * 0.3, k * r * 1.2, r * 0.95)
        setc(ctx, hx('1d6e33')); ctx.set_line_width(r * 0.1); ctx.stroke()
    ellipse(ctx, 0, 0, r * 1.25, r); ink(ctx, max(5, r * 0.06)); ctx.stroke()
    ctx.restore()


def eggs(ctx, x, y, s, a=0.0, open_=False):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -110, -30, 220, 60, 12); fl(ctx, hx('c9c1b0'), 6)
    for k in range(6):
        ctx.new_path(); ctx.arc(-92 + k * 37, -30, 17, math.pi, 2 * math.pi); ctx.close_path(); fl(ctx, hx('ddd6c6'), 5)
    ctx.restore()


def milk(ctx, x, y, s, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -60, -110, 120, 200, 10); fl(ctx, WHITE, 7)
    poly(ctx, [(-60, -110), (0, -165), (60, -110)]); fl(ctx, BLUE, 7)
    rect_r(ctx, -14, -190, 28, 32, 6); fl(ctx, BLUE, 5)
    rect_r(ctx, -48, -60, 96, 70, 10); fl(ctx, hx('cfe8ff'), 5)
    ctx.restore()
    label(ctx, "MILK", x, y - 25 * s, 30 * s, BLUE, 0, 1)


def car(ctx, x, y, s=1.0, trunk=True, stuff=True, only_milk=False, lf=0):
    """side view, facing left; (x, y) = bottom of the rear wheel area"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    # body
    ctx.new_path(); ctx.move_to(-620, -60); ctx.line_to(-620, -200); ctx.curve_to(-600, -240, -540, -250, -470, -255)
    ctx.line_to(-340, -390); ctx.line_to(-30, -390); ctx.line_to(60, -250); ctx.line_to(80, -60); ctx.close_path(); fl(ctx, hx('ff4d5e'), 8)
    poly(ctx, [(-430, -255), (-320, -365), (-200, -365), (-200, -255)]); fl(ctx, hx('bfe8ff'), 6)
    poly(ctx, [(-175, -255), (-175, -365), (-50, -365), (20, -255)]); fl(ctx, hx('bfe8ff'), 6)
    ctx.rectangle(-610, -150, 40, 30); fl(ctx, YEL, 5)
    # open trunk cavity
    if trunk:
        rect_r(ctx, -20, -250, 110, 190, 10); fl(ctx, hx('3a2a40'), 6)
        if stuff:
            for k in range(3):
                bag(ctx, 10 + k * 30, -240, 0.5, BAGC[k + 1], k, -0.1 + k * 0.1)
        if only_milk:
            rays(ctx, 40, -150, 40, 260, lf * 0.04, col=(1, 0.97, 0.6), a=0.5, n=14)
            milk(ctx, 40, -125, 0.55)
        # lifted hatch
        poly(ctx, [(-30, -390), (60, -250), (230, -420), (150, -520)]); fl(ctx, hx('e83a4c'), 8)
        poly(ctx, [(-10, -395), (60, -280), (170, -400), (120, -470)]); fl(ctx, hx('bfe8ff'), 5)
    for wx in (-460, -60):
        ellipse(ctx, wx, -60, 78, 78); fl(ctx, hx('2a2840'), 7)
        ellipse(ctx, wx, -60, 34, 34); fl(ctx, hx('c8ccd8'), 5)
    ctx.restore()


# ------------------------------------------------------------------ Dad with the load
def load_dad(ctx, x, g, k, L, lf, eye='glare', mouth='grin', fac=1, walk=0.0, rot=0.0, newest=1.0, eggs_on=True,
             arms_up=False, foot_up=0.0):
    w = math.sin(lf * 0.9) * walk
    if arms_up:
        p = P(eye=eye, mouth=mouth, rsh=160, rel=10, lsh=-160, lel=-10, torso=-4, head=-6, rot=rot)
    elif L <= 0.01:
        p = P(eye=eye, mouth=mouth, rsh=20, rel=-30, lsh=-20, lel=-30, torso=-4, head=-4, rot=rot)
    else:
        sq = clamp(L / 6)
        p = P(eye=eye, mouth=mouth, rsh=30 - 10 * sq, rel=-10, lsh=-30 + 10 * sq, lel=-10, torso=-6 - 6 * sq, head=-8,
              lhip=-14 - 22 * w - 8 * sq, rhip=14 + 22 * w + 8 * sq, lkn=10 * sq, rkn=-10 * sq, rot=rot + 3 * math.sin(lf * 0.7) * sq)
        if foot_up > 0:
            p['rhip'] = 14 + 76 * foot_up; p['rkn'] = -10
    y = g - 186 * k
    b = draw(_SCR, x, y, k, fac, DAD, p)
    S = k * 1.35
    s = 0.82 * S / 1.755
    nb = [0, 2, 4, 6, 6, 6, 6]
    li = int(clamp(math.floor(L + 1e-6), 0, 6))
    nbag = nb[li]
    nw = newest if 1 <= li <= 3 else 1.0
    # back-hand bags behind the body
    bx, by = b.get('back', (x, y))
    bag_cluster(ctx, bx, by - 10 * s, nbag, s, lf, 3, nw)
    b = draw(ctx, x, y, k, fac, DAD, p)
    fx, fy = b.get('front', (x, y))
    bag_cluster(ctx, fx, fy - 10 * s, nbag, s, lf, 0, nw)
    if L >= 1 and not arms_up:
        for hx_, hy_ in ((bx, by), (fx, fy)):
            ellipse(ctx, hx_, hy_, 17 * S, 17 * S); fl(ctx, BRUISE, 5)
    if arms_up and L >= 1:
        for hx_, hy_ in ((bx, by), (fx, fy)):
            pass
    hx0, hy0 = b['head']; R = b['R']
    top = hy0 - R * 1.0
    if L >= 4 - 0.001 or (3 < L < 4):
        t = clamp(L - 3) if L < 4 else 1
        wy = top - R * 0.55 - (1 - eout(t)) * 500
        watermelon(ctx, hx0 - fac * R * 0.05, wy, R * 0.75, 0.05 * math.sin(lf * 0.7))
        if L >= 5.5 and eggs_on:
            t2 = clamp((L - 5) * 2 - 0.0) if L < 6 else 1
            eggs(ctx, hx0, wy - R * 0.95 - (1 - eout(t2)) * 400, R * 0.006 * 1.0, 0.08 * math.sin(lf * 0.9 + 1))
    if L >= 4.5:
        mx_ = hx0 + fac * R * 0.08; my_ = hy0 + R * 0.5
        bag(ctx, mx_, my_ - R * 0.05, s * 0.8, hx('9fe0ff'), 3, 0.05 * math.sin(lf * 0.6))
    if L >= 2.5:
        sweat(ctx, hx0 - R * 1.05, hy0 - R * 0.4, lf, 0.9 * S / 1.755)
    return b


# ------------------------------------------------------------------ sets
def driveway(ctx, lf, trunk=True, stuff=True):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, SKY); ctx.fill()
    for (cx, cy, r) in ((160, 420, 70), (900, 300, 90)):
        for dx in (-r, 0, r):
            ellipse(ctx, cx + dx + (lf * 0.3) % 40, cy + (0 if dx else -r * 0.4), r, r * 0.7); setc(ctx, WHITE); ctx.fill()
    # house side
    rect_r(ctx, 560, 520, 900, 900, 0); fl(ctx, hx('ffd9a8'), 8)
    for k in range(10):
        ctx.move_to(560, 560 + k * 85); ctx.line_to(1460, 560 + k * 85)
    setc(ctx, hx('f2c590')); ctx.set_line_width(5); ctx.stroke()
    poly(ctx, [(520, 560), (1000, 330), (1500, 560)]); fl(ctx, hx('c8463a'), 8)
    rect_r(ctx, 760, 700, 220, 220, 10); fl(ctx, hx('bfe8ff'), 7)
    ctx.move_to(870, 700); ctx.line_to(870, 920); ctx.move_to(760, 810); ctx.line_to(980, 810); ink(ctx, 6); ctx.stroke()
    # lawn + drive
    ctx.rectangle(-3000, 1380, 7000, 3000); setc(ctx, hx('6fd86a')); ctx.fill()
    poly(ctx, [(-3000, 1400), (4000, 1400), (4000, 3000), (-3000, 3000)]); setc(ctx, hx('a8acb8')); ctx.fill()
    ctx.move_to(-3000, 1400); ctx.line_to(4000, 1400); ink(ctx, 7); ctx.stroke()
    for k in range(-6, 12):
        ctx.move_to(k * 260, 1400); ctx.line_to(k * 260 - 120, 2400)
    setc(ctx, hx('959aa8')); ctx.set_line_width(5); ctx.stroke()
    car(ctx, 300, 1470, 0.9, trunk, stuff)


def wall_walk(ctx, off):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, SKY); ctx.fill()
    ctx.rectangle(-3000, 480, 7000, 1000); setc(ctx, hx('ffd9a8')); ctx.fill()
    for k in range(12):
        ctx.move_to(-3000, 520 + k * 85); ctx.line_to(4000, 520 + k * 85)
    setc(ctx, hx('f2c590')); ctx.set_line_width(5); ctx.stroke()
    for k in range(-4, 8):
        wx = k * 700 - off % 700
        rect_r(ctx, wx, 700, 230, 260, 10); fl(ctx, hx('bfe8ff'), 7)
        ellipse(ctx, wx + 115, 1300, 140, 70); fl(ctx, hx('3fbf5a'), 6)
        for j in range(4):
            ellipse(ctx, wx + 50 + j * 45, 1260 - (j % 2) * 20, 16, 16); fl(ctx, PINK, 4)
    ctx.rectangle(-3000, 1380, 7000, 3000); setc(ctx, hx('c8ccd8')); ctx.fill()
    ctx.move_to(-3000, 1380); ctx.line_to(4000, 1380); ink(ctx, 7); ctx.stroke()
    for k in range(-4, 14):
        xx = k * 200 - off % 200
        ctx.move_to(xx, 1380); ctx.line_to(xx - 60, 2400)
    setc(ctx, hx('aeb2c0')); ctx.set_line_width(5); ctx.stroke()


def front_door(ctx, open_=0.0):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('ffd9a8')); ctx.fill()
    for k in range(-10, 40):
        ctx.move_to(-3000, k * 85); ctx.line_to(4000, k * 85)
    setc(ctx, hx('f2c590')); ctx.set_line_width(5); ctx.stroke()
    rect_r(ctx, 300, 560, 480, 900, 16); fl(ctx, hx('fff6e8'), 8)
    rect_r(ctx, 330, 590, 420, 880, 10); fl(ctx, hx('3a2a40'), 6)
    if open_ < 1:
        ww = 420 * (1 - open_)
        rect_r(ctx, 330, 590, max(20, ww), 880, 10); fl(ctx, hx('2a9d8f'), 8)
        if ww > 120:
            rect_r(ctx, 360, 640, ww - 60, 300, 14); setc(ctx, hx('238a7d')); ctx.fill()
            ellipse(ctx, 330 + ww - 40, 1050, 20, 20); fl(ctx, GOLD, 5)
    # doorbell
    rect_r(ctx, 830, 920, 60, 100, 14); fl(ctx, hx('fff6e8'), 6)
    ellipse(ctx, 860, 970, 18, 18); fl(ctx, GOLD, 5)
    ctx.rectangle(-3000, 1460, 7000, 3000); setc(ctx, hx('c98a52')); ctx.fill()
    ctx.move_to(-3000, 1460); ctx.line_to(4000, 1460); ink(ctx, 7); ctx.stroke()
    rect_r(ctx, 290, 1430, 500, 50, 10); fl(ctx, hx('ff6b8a'), 6)


def kitchen(ctx, lf, window_milk=False):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('fff0c8')); ctx.fill()
    for i in range(-20, 30):
        for j in range(-5, 20):
            if (i + j) % 2 == 0:
                ctx.rectangle(i * 70, 860 + j * 70, 70, 70)
    setc(ctx, hx('ffe39a')); ctx.fill()
    ctx.rectangle(-3000, 400, 7000, 460); setc(ctx, hx('fff0c8')); ctx.fill()
    # window
    rect_r(ctx, 640, 480, 360, 330, 10); fl(ctx, SKY, 8)
    ctx.save(); rect_r(ctx, 640, 480, 360, 330, 10); ctx.clip()
    ctx.rectangle(600, 720, 500, 200); setc(ctx, hx('a8acb8')); ctx.fill()
    car(ctx, 860, 790, 0.38, True, False, window_milk, lf)
    ctx.restore()
    ctx.move_to(820, 480); ctx.line_to(820, 810); ink(ctx, 7); ctx.stroke()
    rect_r(ctx, 640, 480, 360, 330, 10); ink(ctx, 9); ctx.stroke()
    # counter
    rect_r(ctx, -400, 1180, 2000, 60, 10); fl(ctx, hx('e8e8f0'), 7)
    rect_r(ctx, -380, 1240, 1960, 400, 0); fl(ctx, hx('5a8ad8'), 7)
    for k in range(6):
        rect_r(ctx, -360 + k * 330, 1270, 290, 340, 12); ink(ctx, 5); ctx.stroke()
        ellipse(ctx, -220 + k * 330, 1300, 30, 8); fl(ctx, GOLD, 4)
    ctx.rectangle(-3000, 1640, 7000, 3000); setc(ctx, hx('c98a52')); ctx.fill()
    ctx.move_to(-3000, 1640); ctx.line_to(4000, 1640); ink(ctx, 7); ctx.stroke()


def counter_pile(ctx, t):
    if t <= 0:
        return
    rnd = random.Random(9)
    for i in range(10):
        x = 120 + (i % 5) * 120 + rnd.uniform(-20, 20); yb = 1180 - (i // 5) * 90
        y0 = yb - 400 * (1 - eout(t))
        bag(ctx, x, y0 - 190 * 0.75, 0.75, BAGC[i % 6], i % 4, rnd.uniform(-0.15, 0.15))
    watermelon(ctx, 760, 1110 - 300 * (1 - eout(t)), 85, 0.1)


# ------------------------------------------------------------------ close-ups
def dad_ecu(ctx, f, lf, bg, eye='glare', mouth='grin', shake=0, z0=1.0, ray_col=(1, 1, 1), bags=True, veins=True, tw=True):
    ctx.save(); cam(ctx, 540, 960, z0, 0, shake, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    rays(ctx, 540, 900, 260, 1700, lf * 0.03, col=ray_col, a=0.35, n=18)
    cx, cy, R = 540, 860, 290
    jit = 5 * math.sin(lf * 2.9)
    face(ctx, DAD, P(eye=eye, mouth=mouth, head=0), cx + jit, cy, R, 0.02 * math.sin(lf * 0.9))
    if veins:
        for sx in (-1, 1):
            x0 = cx + jit + sx * 0.35 * R; y0 = cy - 0.62 * R
            ctx.new_path(); ctx.move_to(x0, y0 - 40); ctx.line_to(x0 + sx * 18, y0 - 15); ctx.line_to(x0 - sx * 10, y0 + 5); ctx.line_to(x0 + sx * 14, y0 + 30)
            setc(ctx, RED); ctx.set_line_width(10); ctx.stroke()
    if tw:
        twitch(ctx, cx + 0.6 * R, cy - 0.75 * R, lf, 1.3)
    sweat(ctx, cx - 1.0 * R, cy - 0.55 * R, lf, 1.4)
    sweat(ctx, cx + 1.02 * R, cy - 0.2 * R, lf + 40, 1.1)
    if bags:
        for sx in (-1, 1):
            hx_ = 540 + sx * 300 + jit; hy_ = 1330 + 8 * math.sin(lf * 1.7 + sx)
            for i in range(5):
                bag(ctx, hx_ + (i - 2) * 26, hy_ + 20, 1.5, BAGC[(i + (sx > 0)) % 6], i % 4, (i - 2) * 0.12 + sx * 0.05)
            ellipse(ctx, hx_, hy_, 110, 80); fl(ctx, BRUISE, 9)
            for j in range(4):
                ctx.move_to(hx_ - 66 + j * 44, hy_ - 70); ctx.line_to(hx_ - 70 + j * 44, hy_ - 20)
            ink(ctx, 6); ctx.stroke()
    ctx.restore()


def opening_face(ctx, f, lf, lab=True):
    dad_ecu(ctx, f, lf, hx('ff8a1f'), shake=3 + shake_at(lf, [0], 8, 12), z0=1.02 + 0.05 * eout(pop(lf, 0, 50)), ray_col=(1, 0.95, 0.6))
    if lab:
        label1(ctx, "\"ONE. TRIP.\"", WHITE, pop(lf, 0, 4) if lf > 0 else 1, 150, -0.04, y=1490)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    opening_face(ctx, f, f)
    card(ctx, 'p1', f, -6, 56)


def s2(ctx, f):
    lf = f - 60
    L = sum(eout(pop(f, t, t + 6)) for t in LT)
    li = int(math.floor(L + 1e-6))
    newest = (L - math.floor(L)) if 0 < L < 3 and L % 1 > 0.01 else 1.0
    hits = [t - 60 for t in LT]
    z = 1.0 - 0.12 * clamp(L / 6)
    cy = 1060 - 60 * clamp(L / 6)
    ctx.save(); cam(ctx, 560, cy, z, 0, shake_at(lf, hits, 7, 14) + (4 * clamp(L - 5) if f > 200 else 0), f)
    driveway(ctx, lf)
    if f < 100:
        b = draw(ctx, 250, 1600 - 186 * 1.75, 1.75, 1, MOM, P(eye='normal', mouth='smile', rsh=100, rel=-20, head=-4))
        load_dad(ctx, 760, 1620, 1.9, 0, lf, eye='smug' if f >= 78 else 'normal', mouth='smile', fac=-1)
    else:
        eye = 'glare' if L < 4.5 else 'shock'
        load_dad(ctx, 760, 1620, 1.9, L, lf, eye=eye, mouth='grin', fac=-1, newest=newest, walk=0.25 if f > 196 else 0)
    ctx.restore()
    if f < 78:
        label(ctx, "\"Need HELP?\"", 360, 560, 96, WHITE, -0.05, pop(f, 62, 66))
    elif f < 100:
        label2(ctx, "\"Two trips?", "NEVER.\"", WHITE, pop(f, 79, 83), 120, col2=YEL, y=560)
    elif f < 198:
        idx = max([i for i, t in enumerate(LT) if f >= t - 2] or [0])
        t0 = LT[idx]
        label(ctx, LOADS[idx], 540, 1500, 110, LCOL[idx], (-0.05, 0.04, -0.04, 0.05, -0.04, 0.05)[idx], pop(f, t0 - 2, t0 + 2))
        puff(ctx, 600 if idx < 3 else 700, 1250 if idx < 3 else 700, pop(f, t0, t0 + 10), 1.4)
    else:
        label1(ctx, "\"...EASY.\"", WHITE, pop(f, 200, 204), 130, -0.04, y=1500)


def s3(ctx, f):
    lf = f - 228
    if lf < 46:
        off = lf * 14
        ctx.save(); cam(ctx, 540, 1000, 0.95, 3 * math.sin(lf * 0.35), 3, f)
        wall_walk(ctx, off)
        load_dad(ctx, 560, 1600, 1.9, 6, lf, eye='shock', mouth='grin', fac=1, walk=1.0, rot=6 * math.sin(lf * 0.35))
        ctx.restore()
        label(ctx, "*WOBBLE*", 300, 1500, 90, YEL, -0.1, pop(lf, 2, 6) if (lf // 10) % 2 == 0 else 0)
        label(ctx, "*WOBBLE*", 780, 1500, 90, YEL, 0.1, pop(lf, 12, 16) if (lf // 10) % 2 == 1 else 0)
    elif lf < 76:
        il = lf - 46
        ctx.save(); cam(ctx, 560, 1020, 0.95, 0, shake_at(il, [0], 8, 10), f)
        front_door(ctx)
        load_dad(ctx, 720, 1640, 1.9, 6, il, eye='shock', mouth='flat', fac=-1)
        ctx.restore()
        card(ctx, 'p2', f, 274, 304)
        label1(ctx, "*RATTLE RATTLE*", WHITE, pop(il, 8, 12), 90, 0.04, y=1500)
    else:
        il = lf - 76
        push = eout(pop(il, 0, 8))
        ctx.save(); cam(ctx, 820, 980, 1.9, -4, shake_at(il, [8], 10, 16), f)
        front_door(ctx)
        # big side face pressing the bell with the nose
        watermelon(ctx, 690 + 60 * push, 700, 150, 0.1)
        face(ctx, DAD, P(eye='glare', mouth='grin', head=0), 700 + 60 * push, 930, 170, 0.15, 1)
        bx_ = 925 + 60 * push
        rect_r(ctx, bx_, 930, 60, 100, 14); fl(ctx, hx('fff6e8'), 6); ellipse(ctx, bx_ + 30, 980, 18, 18); fl(ctx, GOLD, 5)
        if il >= 8:
            for a_ in (-0.7, 0, 0.7):
                ctx.move_to(bx_ + 70 + 10 * math.cos(a_), 980 + 40 * math.sin(a_)); ctx.line_to(bx_ + 110 + 30 * math.cos(a_), 980 + 80 * math.sin(a_))
            ink(ctx, 6); ctx.stroke()
        ctx.restore()
        if il >= 8:
            label(ctx, "*DING-DONG!*", 540, 520, 120, YEL, -0.06, pop(il, 8, 12))
        label1(ctx, "...with his NOSE.", WHITE, pop(il, 14, 18), 96, -0.03, y=1500)


def s4(ctx, f):
    lf = f - 340
    if lf < 30:
        ctx.save(); cam(ctx, 560, 1080, 1.05 + 0.08 * eout(pop(lf, 0, 30)), 0, 0, f)
        front_door(ctx, open_=eout(pop(lf, 0, 6)) * 0.75)
        draw(ctx, 520, 1480 - 186 * 1.6, 1.6, 1, BOY, P(eye='smug', mouth='smile', rsh=-20, lsh=150, lel=30, head=6))
        ctx.restore()
        label2(ctx, "\"What's the", "PASSWORD?\"", WHITE, pop(lf, 3, 7), 120, col2=YEL, y=560)
    elif lf < 60:
        il = lf - 30
        dad_ecu(ctx, f, il, hx('ff3b5c'), eye='glare', mouth='scream', shake=shake_at(il, [0], 14, 26), z0=1.0 + 0.15 * eout(pop(il, 0, 8)), ray_col=(1, 0.8, 0.6))
        label2(ctx, "\"OPEN.", "THE. DOOR!!\"", WHITE, pop(il, 2, 5), 140, col2=YEL, y=1500)
    elif lf < 100:
        il = lf - 60
        ctx.save(); cam(ctx, 540, 1080, 1.0, 0, shake_at(il, [26], 10, 16), f)
        kitchen(ctx, il)
        fu = eout(pop(il, 18, 24))
        b = load_dad(ctx, 400, 1760, 1.8, 6, il, eye='shock', mouth='grin', fac=1, eggs_on=False, foot_up=fu)
        hx0, hy0 = b['head']; R = b['R']
        # egg carton sliding off the top and falling
        t = pop(il, 4, 24)
        top = (hx0, hy0 - R * 2.55)
        foot = (615, 1555)
        if t <= 0:
            ex, ey, ea = top[0], top[1], 0
        elif t < 1:
            ex = lerp(top[0], foot[0], t); ey = top[1] + (foot[1] - top[1]) * t * t; ea = t * 2.5
        else:
            ex, ey, ea = foot[0], foot[1] - 4 * abs(math.sin(il * 0.6)), 0.08 * math.sin(il * 0.6)
        eggs(ctx, ex, ey, 0.9, ea)
        ctx.restore()
        if il < 24:
            label(ctx, "SLOW... MOTION...", 540, 520, 90, WHITE, -0.04, pop(il, 4, 8))
        else:
            label(ctx, "*SAVED!*", 540, 520, 130, GREEN, -0.06, pop(il, 24, 28))
    else:
        il = lf - 100
        ctx.save(); cam(ctx, 540, 1080, 1.0 + 0.04 * eout(pop(il, 0, 30)), 0, shake_at(il, [2], 12, 22), f)
        kitchen(ctx, il)
        counter_pile(ctx, pop(il, 0, 4))
        b = draw(ctx, 330, 1760 - 186 * 1.8, 1.8, 1, DAD, P(eye='happy', mouth='grin', rsh=165, rel=10, lsh=-165, lel=-10, head=-6))
        for k_ in ('front', 'back'):
            hx_, hy_ = b[k_]; ellipse(ctx, hx_, hy_, 42, 42); fl(ctx, BRUISE, 6)
        ctx.restore()
        sparkle(ctx, 180, 760, 40 + 8 * math.sin(il * 0.6)); sparkle(ctx, 520, 680, 30)
        label(ctx, "*CRASH!*", 760, 900, 100, WHITE, 0.08, pop(il, 1, 4) * (1 - pop(il, 14, 16)))
        label1(ctx, "\"ONE TRIP!!\"", YEL, pop(il, 8, 12), 150, -0.05, y=1500)


def s5(ctx, f):
    lf = f - 472
    if lf < 36:
        ctx.save(); cam(ctx, 560, 1080, 1.0, 0, 0, f)
        kitchen(ctx, lf)
        counter_pile(ctx, 1)
        b = draw(ctx, 330, 1760 - 186 * 1.8, 1.8, 1, DAD, P(eye='shock', mouth='grin', rsh=165, rel=10, lsh=-165, lel=-10, head=-6))
        for k_ in ('front', 'back'):
            hx_, hy_ = b[k_]; ellipse(ctx, hx_, hy_, 42, 42); fl(ctx, BRUISE, 6)
        mx = 1400 - 600 * eout(pop(lf, 0, 10))
        draw(ctx, mx, 1760 - 186 * 1.75, 1.75, -1, MOM, P(eye='normal', mouth='flat', rsh=60, rel=-80, head=4))
        ctx.restore()
        label2(ctx, "\"...where's", "the MILK?\"", WHITE, pop(lf, 10, 14), 120, col2=BLUE, y=560)
    elif lf < 72:
        il = lf - 36
        ctx.save(); cam(ctx, 868, 720, 3.6 + 0.5 * eout(pop(il, 0, 36)), 0, 0, f)
        kitchen(ctx, il, window_milk=True)
        ctx.restore()
        card(ctx, 'p3', f, 508, 544)
        label1(ctx, "*AHHHH~*", YEL, pop(il, 6, 10), 100, -0.04, y=1480)
    elif lf < 112:
        il = lf - 72
        dad_ecu(ctx, f, il, hx('8a3cff'), eye='shock', mouth='wavy', shake=shake_at(il, [0], 8, 12), z0=1.0 + 0.1 * eout(pop(il, 0, 40)), bags=False, veins=False)
        label2(ctx, "\"That's...", "TWO TRIPS.\"", WHITE, pop(il, 3, 7), 130, col2=RED, y=1440)
    elif lf < 152:
        il = lf - 112
        Lr = 6 * eout(pop(il, 0, 14))
        ctx.save(); cam(ctx, 540, 1020, 0.95, 0, shake_at(il, [14], 8, 14), f)
        kitchen(ctx, il)
        counter_pile(ctx, 1 - pop(il, 0, 8))
        load_dad(ctx, 360 - 8 * max(0, il - 16), 1760, 1.8, Lr, il, eye='glare', mouth='grin', fac=-1, walk=0.5)
        draw(ctx, 1080, 1760 - 186 * 1.75, 1.75, -1, MOM, P(eye='closed', mouth='flat', rsh=170, rel=-120, head=10))
        ctx.restore()
        label1(ctx, "\"...From the TOP.\"", WHITE, pop(il, 12, 16), 120, -0.04, y=1500)
    else:
        il = lf - 152
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 626)


SHOTS = [(0, s1), (60, s2), (228, s3), (340, s4), (472, s5)]
CUTS = (60, 228, 274, 304, 340, 370, 400, 440, 472, 508, 544, 584, 624)


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.22)
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
                              "-i", "out/onetrip_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
