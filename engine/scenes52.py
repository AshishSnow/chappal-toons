"""'Bath Time Battle' - original, general-audience comedy short, 22s.
Hook: ECU kid mid-scream, tears flying sideways: "NOOO! NOT THE BATH!!"
Beat 1: kid clings to the bathroom door frame like a flag in the wind, Mom pulling his ankles: "I'm ALLERGIC to water!"
Beat 2: hides under a laundry basket, feet poking out: "She'll NEVER find me." -> basket lifted.
Beat 3: overhead cam: dropped into the tub *SPLOOSH*, arms crossed: "WORST. DAY. EVER."
Turn: minute 5 - bubble beard, foam mohawk, duck fleet: "BEST. DAY. EVER!!"
 Split: Mom "Time to get OUT!" / kid "FIVE MORE MINUTES!!"
Hour 2: raisin fingers, "I live here now." Mom pulls the plug -> whirlpool spin "NOOOO!"
Twist: towel burrito, sparkling clean, Mom "SO CLEAN!" -> kid spots a mud puddle, cannonball SPLAT on the lens,
 Mom eye twitch "...BATH. TIME." -> opening scream (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos, zigs
from scenes48 import label1, label2
import scenes13
from scenes13 import card as _card13
import random

BOY = dict(doodle.BOY, hood=False)
MOM = doodle.MOM_G
WET = dict(BOY, hair=hx('1c1a2e'))
RAISIN = dict(BOY, skin=hx('d9a3c8'))
MUDDY = dict(BOY, skin=hx('9a6a3e'), shirt=hx('7a5230'), pants=hx('6a4424'))
N = 660
FLOOR = 1460
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
WATER = hx('7fd8ff')
DEEP = hx('3aa8f0')
MUD = hx('7a4f2a')
DUCKY = hx('ffd23f')

CAPS = {
    'p1': [[("BATH TIME:", OUT)], [("MINUTE 1", RED)]],
    'p2': [[("MINUTE 2:", OUT)], [("THE ESCAPE", BLUE)]],
    'p2b': [[("MINUTE 3:", OUT)], [("SPLASHDOWN", ORANGE)]],
    'p3': [[("MINUTE 5:", OUT)], [("BUBBLES", PURPLE)]],
    'p4': [[("HOUR 2...", PURPLE)]],
    'p5': [[("FINALLY", OUT)], [("CLEAN!", GREEN)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def tiles(ctx, col=hx('8fe3ff'), line=None):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, col); ctx.fill()
    lc = line or light(col, 0.35)
    for i in range(-30, 40):
        ctx.rectangle(i * 110, -3000, 5, 7000); setc(ctx, lc); ctx.fill()
        ctx.rectangle(-3000, i * 110, 7000, 5); setc(ctx, lc); ctx.fill()


def bubble(ctx, x, y, r, a=0.9):
    ellipse(ctx, x, y, r, r); setc(ctx, (1, 1, 1, a * 0.55)); ctx.fill_preserve()
    setc(ctx, (1, 1, 1, a)); ctx.set_line_width(max(2, r * 0.12)); ctx.stroke()
    ellipse(ctx, x - r * 0.35, y - r * 0.35, r * 0.2, r * 0.14, -0.6); setc(ctx, (1, 1, 1, a)); ctx.fill()


def foam(ctx, x, y, w, h, seed=1, n=18):
    rnd = random.Random(seed)
    for k in range(n):
        px = x + rnd.uniform(-w / 2, w / 2); py = y + rnd.uniform(-h / 2, h / 2); r = rnd.uniform(0.18, 0.32) * min(w, h)
        ellipse(ctx, px, py, r, r); fl(ctx, (1, 1, 1), 5)
    for k in range(n):
        px = x + rnd.uniform(-w / 2, w / 2); py = y + rnd.uniform(-h / 2, h / 2); r = rnd.uniform(0.15, 0.28) * min(w, h)
        ellipse(ctx, px, py, r, r); setc(ctx, (1, 1, 1)); ctx.fill()


def duck(ctx, x, y, s=1.0, a=0.0, f_=1):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s * f_, s)
    ctx.move_to(-70, 0); ctx.curve_to(-80, -60, 40, -60, 60, -10); ctx.curve_to(70, 30, -40, 40, -70, 0); ctx.close_path()
    fl(ctx, DUCKY, 6)
    ellipse(ctx, 30, -60, 34, 32); fl(ctx, DUCKY, 6)
    ctx.move_to(58, -62); ctx.line_to(92, -54); ctx.line_to(60, -44); ctx.close_path(); fl(ctx, ORANGE, 5)
    ellipse(ctx, 40, -68, 6, 7); setc(ctx, INK); ctx.fill()
    ctx.move_to(-40, -10); ctx.curve_to(-20, -30, 10, -20, 10, 0); ink(ctx, 5); ctx.stroke()
    ctx.restore()


def tub_side(ctx, x0, x1, top, water=0.6, lf=0):
    """side-view tub; front wall drawn by tub_front"""
    rect_r(ctx, x0, top, x1 - x0, FLOOR - 60 - top, 60); fl(ctx, (1, 1, 1), 8)


def tub_front(ctx, x0, x1, top):
    rect_r(ctx, x0, top, x1 - x0, FLOOR - 60 - top, 60); fl(ctx, (1, 1, 1), 8)
    for xf in (x0 + 80, x1 - 80):
        ellipse(ctx, xf, FLOOR - 40, 40, 30); fl(ctx, hx('ffcf3d'), 6)
    ctx.move_to(x0 + 40, top + 50); ctx.line_to(x1 - 40, top + 50); setc(ctx, hx('dff4ff')); ctx.set_line_width(12); ctx.stroke()


def tub_top(ctx, cx, cy, w, h, lvl=1.0, swirl=0.0, lf=0):
    """overhead tub: rim + water (lvl 0..1)"""
    rect_r(ctx, cx - w / 2 - 50, cy - h / 2 - 50, w + 100, h + 100, 160); fl(ctx, (1, 1, 1), 9)
    rect_r(ctx, cx - w / 2, cy - h / 2, w, h, 130); fl(ctx, hx('eaf6ff'), 6)
    ctx.save(); rect_r(ctx, cx - w / 2, cy - h / 2, w, h, 130); ctx.clip()
    if lvl > 0:
        sc = 0.35 + 0.65 * lvl
        rect_r(ctx, cx - w / 2 * sc, cy - h / 2 * sc, w * sc, h * sc, 130 * sc); setc(ctx, WATER); ctx.fill()
        for k in range(6):
            yy = cy - h / 2 + (k * 170 + lf * 3) % h
            ctx.move_to(cx - 150, yy); ctx.curve_to(cx - 80, yy - 20, cx - 20, yy + 20, cx + 50, yy)
            setc(ctx, (1, 1, 1, 0.45)); ctx.set_line_width(10); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    if swirl > 0:
        for k in range(5):
            a0 = lf * 0.35 + k * 1.25
            ctx.new_path(); ctx.arc(cx, cy + h * 0.32, 60 + k * 70, a0, a0 + 2.0)
            setc(ctx, (1, 1, 1, 0.75 * swirl)); ctx.set_line_width(16); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.restore()
    # faucet at the top end
    rect_r(ctx, cx - 50, cy - h / 2 - 100, 100, 110, 30); fl(ctx, hx('c8ccd8'), 7)
    ellipse(ctx, cx, cy + h * 0.32, 30, 30); fl(ctx, hx('9aa4b8'), 6)


def basket(ctx, x, y, s=1.0, lift=0.0):
    """upturned laundry basket, bottom-centre at x,y"""
    ctx.save(); ctx.translate(x, y - lift); ctx.scale(s, s)
    poly(ctx, [(-230, 0), (230, 0), (190, -330), (-190, -330)]); fl(ctx, hx('2fd0a0'), 8)
    ctx.save(); poly(ctx, [(-230, 0), (230, 0), (190, -330), (-190, -330)]); ctx.clip()
    for j in range(4):
        for i in range(-5, 6):
            rect_r(ctx, i * 80 - 26, -300 + j * 76, 52, 40, 14); setc(ctx, hx('0f8f6a')); ctx.fill()
    ctx.restore()
    rect_r(ctx, -240, -30, 480, 34, 12); fl(ctx, hx('22b48a'), 6)
    ctx.restore()


def towel_burrito(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rect_r(ctx, -140, -260, 280, 300, 110); fl(ctx, hx('ff8fc4'), 8)
    for k in range(3):
        ctx.move_to(-140, -180 + k * 70); ctx.curve_to(-40, -150 + k * 70, 60, -210 + k * 70, 140, -170 + k * 70)
    setc(ctx, (1, 1, 1)); ctx.set_line_width(12); ctx.stroke()
    ctx.restore()


def splats(ctx, x, y, s=1.0, seed=1, col=MUD):
    rnd = random.Random(seed)
    for k in range(5):
        ellipse(ctx, x + rnd.uniform(-40, 40) * s, y + rnd.uniform(-30, 30) * s, rnd.uniform(14, 30) * s, rnd.uniform(12, 24) * s); setc(ctx, col); ctx.fill()


def tears(ctx, cx, cy, R, lf):
    """cartoon sideways tear streams"""
    for side in (-1, 1):
        ex = cx + side * R * 0.42; ey = cy + R * 0.1
        for k in range(5):
            t = ((lf * 0.09 + k * 0.2) % 1)
            px = ex + side * (60 + 520 * t); py = ey - 60 * math.sin(t * math.pi) + 260 * t * t
            ellipse(ctx, px, py, 26 * (1 - 0.4 * t), 20 * (1 - 0.4 * t)); fl(ctx, hx('8fd8ff'), 4)


def bathroom(ctx, wall=hx('8fe3ff')):
    tiles(ctx, wall)
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('e8eef5')); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 140, FLOOR, 4, 1500); setc(ctx, hx('c7d2e0')); ctx.fill()
    ctx.rectangle(-3000, FLOOR - 6, 7000, 12); setc(ctx, OUT); ctx.fill()


def hallway(ctx):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('ffd166')); ctx.fill()
    for i in range(-20, 30):
        ctx.rectangle(i * 160, -3000, 50, 7000); setc(ctx, hx('ffdb85')); ctx.fill()
    rect_r(ctx, 680, 520, 240, 300, 10); fl(ctx, hx('ff9f6b'), 7)          # picture frame
    ellipse(ctx, 800, 640, 60, 60); setc(ctx, YEL); ctx.fill()
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('c98a52')); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 200, FLOOR, 5, 1500); setc(ctx, hx('a86e3c')); ctx.fill()
    ctx.rectangle(-3000, FLOOR - 6, 7000, 12); setc(ctx, OUT); ctx.fill()


def yard(ctx):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('7fd0ff')); ctx.fill()
    for (x, y, r) in ((200, 560, 80), (300, 540, 100), (820, 640, 90), (920, 620, 70)):
        ellipse(ctx, x, y, r * 1.3, r); setc(ctx, (1, 1, 1)); ctx.fill()
    ellipse(ctx, 540, 1700, 1800, 700); setc(ctx, hx('6fd16a')); ctx.fill()
    ctx.rectangle(-3000, 1300, 7000, 2000); setc(ctx, hx('6fd16a')); ctx.fill()
    for i in range(-10, 30):
        ctx.move_to(i * 70, 1320); ctx.line_to(i * 70 + 12, 1280); ctx.line_to(i * 70 + 24, 1320); setc(ctx, hx('4fb84c')); ctx.fill()
    # fence
    for i in range(-2, 14):
        poly(ctx, [(i * 100, 1300), (i * 100, 1000), (i * 100 + 40, 960), (i * 100 + 80, 1000), (i * 100 + 80, 1300)]); fl(ctx, (1, 1, 1), 6)


def puddle(ctx, x, y, w, h, splash=0.0):
    ellipse(ctx, x, y, w, h); fl(ctx, MUD, 8)
    ellipse(ctx, x - w * 0.3, y - h * 0.2, w * 0.25, h * 0.2); setc(ctx, light(MUD, 0.2)); ctx.fill()


# ------------------------------------------------------------------ opening
def opening_face(ctx, f, lf, lab=True):
    """ECU: kid mid-scream, tears flying sideways"""
    sh = shake_at(lf, [0], 12, 20) + 7
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eout(pop(lf, 0, 40)), 0, sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff5a7a')); ctx.fill()
    rays(ctx, 540, 860, 260, 1700, lf * 0.06, col=(1, 0.9, 0.4), a=0.4, n=18)
    cx, cy, R = 540 + 6 * math.sin(lf * 2.1), 860, 300
    tears(ctx, cx, cy, R, lf)
    face(ctx, BOY, P(eye='closed', mouth='scream', head=0), cx, cy, R, 0.03 * math.sin(lf * 1.5))
    # rubber duck sneaking in from the bottom (the threat)
    duck(ctx, 860, 1250 - 30 * abs(math.sin(lf * 0.3)), 1.2, 0.1, -1)
    ctx.restore()
    if lab:
        label2(ctx, "\"NOOO! NOT", "THE BATH!!\"", (1, 1, 1), 1.0 if f < 60 else pop(lf, 0, 3), 116, col2=YEL)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 60:
        opening_face(ctx, f, f)
    else:
        lf = f - 60
        # bathroom doorway: kid horizontal like a flag, gripping the door frame, Mom pulls his ankles
        flap = 6 * math.sin(lf * 1.2)
        ctx.save(); cam(ctx, 560, 1060, 1.0 + 0.04 * eout(pop(lf, 0, 50)), 0, 4, f)
        hallway(ctx)
        # door frame (left)
        ctx.rectangle(-400, 380, 560, FLOOR - 380); setc(ctx, hx('8fe3ff')); ctx.fill()
        ctx.rectangle(130, 380, 90, FLOOR - 380); fl(ctx, hx('fff3d6'), 7)
        # kid, rotated 90deg: arms reach left to the frame
        for hy_ in (930, 1110):   # arms gripping the frame
            ctx.move_to(360, 1020); ctx.line_to(178, hy_ + flap * 2)
            setc(ctx, INK); ctx.set_line_width(56); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke_preserve()
            setc(ctx, BOY['skin']); ctx.set_line_width(42); ctx.stroke()
            ellipse(ctx, 175, hy_ + flap * 2, 34, 34); fl(ctx, BOY['skin'], 6)
        ctx.save(); ctx.translate(760, 1030); ctx.rotate(math.radians(-90 + flap)); ctx.translate(-760, -1030)
        pk = P(torso=0, lhip=-6 + flap, lkn=0, rhip=6 - flap, rkn=0, lsh=-150, lel=-10, rsh=-205, rel=10, eye="closed", mouth="scream", head=0)
        draw(ctx, 760, 1030 - 186 * 1.2, 1.2, 1, BOY, pk)
        ctx.restore()
        for k in range(3):    # speed lines
            ctx.move_to(560, 1040 + k * 70); ctx.line_to(760, 1040 + k * 70 + 10 * math.sin(lf + k))
        setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(10); ctx.stroke()
        pm = P(torso=-14, lhip=-20, lkn=10, rhip=20, rkn=0, lsh=100, lel=-10, rsh=95, rel=-10, eye='glare', mouth='flat', head=8)
        draw(ctx, 960, FLOOR - 186 * 1.3, 1.3, -1, MOM, pm)
        ctx.restore()
        label2(ctx, "\"I'm ALLERGIC", "to WATER!\"", (1, 1, 1), pop(lf, 2, 6), 104, col2=YEL)
    card(ctx, 'p1', f, -6, 110)


def s2(ctx, f):
    lf = f - 110
    if lf < 60:
        # laundry basket hide-out
        lifted = lf >= 34
        ctx.save(); cam(ctx, 540, 1150, 1.15 + 0.04 * eout(pop(lf, 0, 60)), 0, shake_at(lf, [34], 6, 10), f)
        hallway(ctx)
        if lifted:
            pk = P(torso=0, lhip=-10, lkn=0, rhip=10, rkn=0, lsh=20, lel=-140, rsh=20, rel=-140, eye='shock', mouth='open', head=0)
            draw(ctx, 540, FLOOR - 186 * 0.9, 0.9, 1, BOY, pk)
            pm = P(torso=0, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=-160, lel=-10, rsh=-165, rel=-10, eye='smug', mouth='smile', head=0)
            bm = draw(ctx, 820, FLOOR - 186 * 1.25, 1.25, -1, MOM, pm)
            basket(ctx, 540, FLOOR + 10, 1.0, 360 * eout(pop(lf, 34, 40)))
        else:
            # feet poking out + eyes peeking through gaps
            for sx in (-1, 1):
                ellipse(ctx, 540 + sx * 70, FLOOR - 10, 44, 22); fl(ctx, BOY['shoes'], 6)
            basket(ctx, 540, FLOOR + 10, 1.0)
            ex = 540 + 8 * math.sin(lf * 0.4)
            for k in (-1, 1):
                ellipse(ctx, ex + k * 40, FLOOR - 196, 22, 22); fl(ctx, (1, 1, 1), 4)
                ellipse(ctx, ex + k * 40 + 6 * math.sin(lf * 0.4), FLOOR - 194, 9, 9); setc(ctx, INK); ctx.fill()
            # Mom's shadow creeping in
            ctx.save(); ctx.translate(lerp(1300, 900, eout(pop(lf, 12, 30))), 0)
            pm = P(torso=0, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=20, lel=-20, rsh=20, rel=-20, eye='smug', mouth='smile', head=0)
            draw(ctx, 0, FLOOR - 186 * 1.25, 1.25, -1, MOM, pm)
            ctx.restore()
        ctx.restore()
        if not lifted:
            label2(ctx, "\"She'll NEVER", "find me.\"", (1, 1, 1), pop(lf, 2, 6), 104, col2=YEL)
        else:
            label1(ctx, "\"FOUND YOU.\"", PINK, pop(lf, 36, 40), 120)
        card(ctx, 'p2', f, 112, 170)
    else:
        il = lf - 60
        # overhead tub: kid dropped in, SPLOOSH, then grumpy arms crossed
        drop = eout(pop(il, 0, 14))
        ctx.save(); cam(ctx, 540, 980, 1.0 + 0.05 * eout(pop(il, 14, 80)), 4, shake_at(il, [14], 16, 28), f)
        tiles(ctx, hx('ffd0e8'))
        tub_top(ctx, 540, 1000, 700, 1080, 1.0, 0, il)
        if il < 14:
            s_ = lerp(1.9, 1.0, drop)
            face(ctx, BOY, P(eye='shock', mouth='scream', head=0), 540, 920, 210 * s_, 0.0)
        else:
            # splash ring
            g = pop(il, 14, 30)
            if g < 1:
                rnd = random.Random(3)
                for k in range(24):
                    a = rnd.uniform(0, 2 * math.pi); d = rnd.uniform(200, 700) * eout(g)
                    ellipse(ctx, 540 + math.cos(a) * d, 920 + math.sin(a) * d, 40 * (1 - g) + 6, 40 * (1 - g) + 6); fl(ctx, WATER, 4)
            # arms crossed in front
            face(ctx, WET, P(eye='glare', mouth='frown', head=0), 540, 900, 210, 0.0)
            ctx.rectangle(200, 1060, 680, 400); setc(ctx, WATER + (0.9,)); ctx.fill()
            rect_r(ctx, 330, 1070, 420, 90, 45); fl(ctx, BOY['skin'], 7)
            rect_r(ctx, 360, 1110, 360, 80, 40); fl(ctx, BOY['skin'], 7)
            for k in range(3):
                bubble(ctx, 380 + k * 160, 1240 + 20 * math.sin(il * 0.2 + k), 40)
            duck(ctx, 720, 1330, 0.9, 0.0, -1)
        ctx.restore()
        if il < 14:
            pass
        elif il < 30:
            label1(ctx, "*SPLOOSH!*", (1, 1, 1), pop(il, 14, 17), 150, 0.04)
        else:
            label2(ctx, "\"WORST. DAY.", "EVER.\"", (1, 1, 1), pop(il, 30, 34), 116, col2=RED)
        card(ctx, 'p2b', f, 172, 250)


def s3(ctx, f):
    lf = f - 250
    if lf < 90:
        # bubble party: foam mohawk, bubble beard, duck fleet
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eout(pop(lf, 0, 90)), -6 + 4 * math.sin(lf * 0.12), shake_at(lf, [0, 40], 6, 10), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('b98cff')); ctx.fill()
        rays(ctx, 540, 820, 220, 1600, lf * 0.04, col=(1, 1, 1), a=0.28, n=18)
        rnd = random.Random(11)
        for k in range(26):                 # rising bubbles
            x = rnd.uniform(0, 1080); sp = rnd.uniform(4, 10); r = rnd.uniform(20, 60)
            y = 1800 - ((lf * sp + rnd.uniform(0, 1700)) % 1900)
            bubble(ctx, x + 20 * math.sin(lf * 0.1 + k), y, r)
        cx, cy, R = 540, 860, 250
        face(ctx, WET, P(eye='happy', mouth='grin', head=0), cx, cy, R, 0.05 * math.sin(lf * 0.3))
        ctx.rectangle(-500, 1180, 2200, 1000); setc(ctx, WATER + (0.97,)); ctx.fill()
        foam(ctx, cx, cy - R * 1.25, R * 0.9, R * 0.9, 4, 14)       # foam mohawk
        if lf >= 40:
            foam(ctx, cx + 10, cy + R * 0.95, R * 1.3 * eout(pop(lf, 40, 48)) + 1, R * 0.7, 7, 16)  # bubble beard
        foam(ctx, 540, 1190, 1300, 120, 9, 30)
        for k in range(4):
            duck(ctx, 160 + k * 250 + 20 * math.sin(lf * 0.2 + k), 1300 + 14 * math.sin(lf * 0.3 + k), 0.8 - 0.08 * k, 0.1 * math.sin(lf * 0.2 + k), 1)
        ctx.restore()
        if lf < 40:
            label1(ctx, "\"...oh. BUBBLES?\"", (1, 1, 1), pop(lf, 2, 6), 104, y=1520)
        else:
            label2(ctx, "\"BEST. DAY.", "EVER!!\"", (1, 1, 1), pop(lf, 40, 44), 124, col2=YEL, y=1460)
        card(ctx, 'p3', f, 252, 340)
    else:
        il = lf - 90
        # split: Mom at the door (top) vs kid in the bubbles (bottom)
        ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
        ctx.rectangle(0, 0, W, 960); setc(ctx, hx('ffd166')); ctx.fill()
        rays(ctx, 540, 700, 150, 1300, il * 0.03, col=(1, 1, 1), a=0.3, n=16)
        face(ctx, MOM, P(eye='normal', mouth='open', head=0), 540, 640, 200, -0.04)
        ctx.restore()
        ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
        ctx.rectangle(0, 960, W, 960); setc(ctx, hx('b98cff')); ctx.fill()
        sh = 8 if il >= 18 else 0
        face(ctx, WET, P(eye='glare' if il >= 18 else 'happy', mouth='scream' if il >= 18 else 'grin', head=0),
             540 + random.Random(il).uniform(-sh, sh), 1250, 200, 0.0)
        ctx.rectangle(0, 1330, W, 600); setc(ctx, WATER + (0.97,)); ctx.fill()
        foam(ctx, 540, 1250 - 250, 180, 180, 4, 12)
        foam(ctx, 540, 1350, 1200, 100, 9, 26)
        ctx.restore()
        ctx.rectangle(0, 952, W, 16); setc(ctx, (1, 1, 1)); ctx.fill()
        label(ctx, "\"Time to get OUT!\"", 540, 360, 92, (1, 1, 1), -0.03, pop(il, 2, 6))
        if il >= 18:
            label2(ctx, "\"FIVE MORE", "MINUTES!!\"", (1, 1, 1), pop(il, 18, 22), 104, col2=YEL, y=1430)


def s4(ctx, f):
    lf = f - 400
    if lf < 50:
        # raisin kid: wrinkly purple, big prune hand in the foreground
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eout(pop(lf, 0, 50)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('5b3fa8')); ctx.fill()
        rays(ctx, 540, 800, 200, 1600, lf * 0.02, col=(1, 1, 1), a=0.15, n=16)
        cx, cy, R = 520, 820, 250
        face(ctx, RAISIN, P(eye='smug', mouth='smile', head=0), cx, cy, R, -0.05)
        ctx.rectangle(-500, 1120, 2200, 1000); setc(ctx, hx('6fc0e8') + (0.93,)); ctx.fill()
        foam(ctx, 540, 1130, 1300, 80, 5, 24)
        for k in range(5):       # wrinkles
            ctx.move_to(cx - R * 0.6 + k * R * 0.3, cy - R * 0.62); ctx.curve_to(cx - R * 0.5 + k * R * 0.3, cy - R * 0.7, cx - R * 0.45 + k * R * 0.3, cy - R * 0.55, cx - R * 0.4 + k * R * 0.3, cy - R * 0.65)
        ink(ctx, 6); ctx.stroke()
        # giant pruney hand waving
        hy = 1180 + 20 * math.sin(lf * 0.3)
        ctx.save(); ctx.translate(830, hy); ctx.rotate(0.15 * math.sin(lf * 0.3))
        rect_r(ctx, -110, -80, 220, 170, 70); fl(ctx, RAISIN['skin'], 8)
        for j in range(4):
            rect_r(ctx, -100 + j * 52, -230, 44, 170, 22); fl(ctx, RAISIN['skin'], 6)
            for w in range(4):
                ctx.move_to(-92 + j * 52, -200 + w * 32); ctx.curve_to(-84 + j * 52, -206 + w * 32, -72 + j * 52, -194 + w * 32, -62 + j * 52, -200 + w * 32)
            ink(ctx, 4); ctx.stroke()
        ctx.restore()
        ctx.restore()
        label2(ctx, "\"I live", "here now.\"", (1, 1, 1), pop(lf, 4, 8), 112, col2=YEL, y=1470)
        card(ctx, 'p4', f, 402, 450)
    else:
        il = lf - 50
        # Mom pulls the plug: overhead whirlpool, kid spinning, clinging to a duck
        lvl = 1 - 0.7 * ein(pop(il, 8, 50))
        ctx.save(); cam(ctx, 540, 1000, 1.0, il * 3.0, shake_at(il, [8], 10, 14) + 3, f)
        tiles(ctx, hx('ffd0e8'))
        tub_top(ctx, 540, 1000, 700, 1080, lvl, pop(il, 8, 20), il)
        # plug chain flying out
        if il >= 6:
            u = eout(pop(il, 6, 14))
            ctx.move_to(540, 1345); ctx.line_to(540 + 300 * u, 1345 + 500 * u); ink(ctx, 8); ctx.stroke()
            ellipse(ctx, 540 + 300 * u, 1345 + 500 * u, 40, 40); fl(ctx, hx('2a2a3a'), 6)
        ang = il * 0.25 if il >= 10 else 0
        rr = 120 if il >= 10 else 0
        kx = 540 + math.cos(ang) * rr; ky = 1000 + math.sin(ang) * rr
        face(ctx, RAISIN, P(eye='shock', mouth='scream', head=0), kx, ky, 190, ang)
        duck(ctx, 540 + math.cos(ang + 2.4) * 260, 1050 + math.sin(ang + 2.4) * 260, 0.9, ang * 1.5, 1)
        ctx.restore()
        if il < 8:
            label1(ctx, "*PLINK*", YEL, pop(il, 4, 7), 120, y=1440)
        else:
            label2(ctx, "\"NOOOOO!", "*GLUG GLUG*\"", (1, 1, 1), pop(il, 8, 12), 112, col2=YEL)


def s5(ctx, f):
    lf = f - 500
    if lf < 50:
        # towel burrito, sparkling clean; eyes drift to the window
        ctx.save(); cam(ctx, 540, 1100, 1.1, 0, 0, f)
        bathroom(ctx, hx('9ff0b0'))
        # window with a puddle outside
        rect_r(ctx, 690, 520, 300, 300, 12); fl(ctx, hx('7fd0ff'), 8)
        ctx.rectangle(690, 720, 300, 100); setc(ctx, hx('6fd16a')); ctx.fill()
        ellipse(ctx, 840, 770, 90, 26); setc(ctx, MUD); ctx.fill()
        ctx.move_to(840, 520); ctx.line_to(840, 820); ctx.move_to(690, 670); ctx.line_to(990, 670); ink(ctx, 8); ctx.stroke()
        rect_r(ctx, 690, 520, 300, 300, 12); ink(ctx, 8); ctx.stroke()
        pm = P(torso=0, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=-20, lel=-20, rsh=-150, rel=-10, eye='happy', mouth='grin', head=0)
        draw(ctx, 220, FLOOR - 186 * 1.3, 1.3, 1, MOM, pm)
        look = lf >= 26
        towel_burrito(ctx, 560, FLOOR - 40, 1.05)
        face(ctx, BOY, P(eye='smug' if look else 'happy', mouth='smile' if look else 'grin', head=0), 560 + (14 if look else 0), FLOOR - 340, 120, 0.0)
        for k in range(4):
            a = lf * 0.15 + k * math.pi / 2
            sparkle(ctx, 560 + math.cos(a) * 200, FLOOR - 300 + math.sin(a) * 160, 26 + 8 * math.sin(lf * 0.5 + k))
        if look:
            ctx.move_to(640, FLOOR - 380); ctx.line_to(760, 780); setc(ctx, (1, 1, 1, 0.6)); ctx.set_dash([20, 18]); ctx.set_line_width(8); ctx.stroke(); ctx.set_dash([])
        ctx.restore()
        if not look:
            label2(ctx, "\"SO CLEAN!", "*DING!*\"", (1, 1, 1), pop(lf, 2, 6), 112, col2=YEL)
        else:
            label1(ctx, "\"...ooh. MUD.\"", YEL, pop(lf, 26, 30), 112)
        card(ctx, 'p5', f, 502, 548)
    elif lf < 110:
        il = lf - 50
        # yard: cannonball into the mud puddle, mud SPLAT on the lens
        ctx.save(); cam(ctx, 540, 1100, 1.05, 0, shake_at(il, [20], 18, 30), f)
        yard(ctx)
        puddle(ctx, 540, 1420, 360, 90)
        if il < 20:
            u = il / 20
            x = lerp(-100, 540, u); y = lerp(1100, 1340, u) - 500 * math.sin(u * math.pi)
            ctx.save(); ctx.translate(x, y); ctx.rotate(u * 6)
            ellipse(ctx, 0, 0, 120, 120); fl(ctx, hx('ff8fc4'), 8)                 # balled-up kid in the towel
            face(ctx, BOY, P(eye='happy', mouth='grin', head=0), 0, -10, 90, 0.0)
            ctx.restore()
            label(ctx, "CANNONBALL!!", 540, 700, 110, YEL, -0.05, pop(il, 0, 4))
        else:
            g = pop(il, 20, 34)
            rnd = random.Random(6)
            for k in range(30):
                a = -math.pi / 2 + rnd.uniform(-1.3, 1.3); sp = rnd.uniform(400, 1100)
                ellipse(ctx, 540 + math.cos(a) * sp * g, 1380 + math.sin(a) * sp * g + 800 * g * g, 30 * (1 + g), 26 * (1 + g)); setc(ctx, MUD); ctx.fill()
            pk = P(torso=0, lhip=-10, lkn=0, rhip=10, rkn=0, lsh=-150, lel=-10, rsh=-150, rel=-10, eye='happy', mouth='grin', head=0)
            draw(ctx, 540, 1400 - 186 * 1.1, 1.1, 1, MUDDY, pk)
        ctx.restore()
        if il >= 24:
            v = max(0.03, eout(pop(il, 24, 28)))
            rnd = random.Random(12)
            for k in range(12):
                x, y = rnd.uniform(-50, 1130), rnd.uniform(200, 1800); r_ = rnd.uniform(90, 220) * v
                ellipse(ctx, x, y, r_, r_ * 0.9); setc(ctx, MUD + (0.93,)); ctx.fill()
                d = (il - 28) * 8 * rnd.uniform(0.5, 1.2)
                if d > 0:
                    rect_r(ctx, x - 16, y, 32, r_ * 0.6 + d, 16); setc(ctx, MUD + (0.93,)); ctx.fill()
            label1(ctx, "*SPLAT!*", (1, 1, 1), pop(il, 24, 27), 150, -0.04, y=900)
        elif il >= 20:
            label1(ctx, "*SPLOOSH!*", YEL, pop(il, 20, 23), 140)
    elif lf < 135:
        il = lf - 110
        # Mom ECU: eye twitch, "...BATH. TIME."
        ctx.save(); cam(ctx, 540, 900, 1.15 + 0.15 * eout(pop(il, 0, 25)), 0, 4 if (il // 3) % 2 else 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('3a2a6a')); ctx.fill()
        rays(ctx, 540, 860, 200, 1500, il * 0.05, col=(1, 0.4, 0.5), a=0.3, n=16)
        face(ctx, MOM, P(eye='glare', mouth='flat', head=0), 540, 860, 280, 0.0)
        splats(ctx, 420, 700, 2.0, 3); splats(ctx, 690, 980, 1.6, 8)
        ctx.restore()
        label2(ctx, "\"...BATH.", "TIME.\"", (1, 1, 1), pop(il, 3, 7), 124, col2=RED)
    else:
        il = lf - 135
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 635)


SHOTS = [(0, s1), (110, s2), (250, s3), (400, s4), (500, s5)]
CUTS = (60, 110, 170, 250, 340, 400, 450, 500, 550, 610, 635)


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
                              "-i", "out/bath_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
