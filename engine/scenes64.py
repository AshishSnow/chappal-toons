"""'HICCUPS: Everyone Has a Cure' - original, general-audience comedy short, 22s.
Hook: kid ECU mid-hiccup jolt "*HIC!*" + caption "HICCUPS. / EVERYONE HAS A CURE."
Beat 1: Dad "HOLD YOUR BREATH!" -> push-in on the kid's face inflating red -> purple ("5 SECONDS... 30!!")
 -> *HIC!* -> kid zips around the room like a let-go balloon *PFFFFT!*
Beat 2: Mom "Drink water UPSIDE DOWN!" -> camera rolls 180 so the room flips -> *GULP GULP* -> *HIC!*
 -> water fountain *SPLOOSH* all over Mom.
Beat 3: Dad sneaks up "I'll SCARE them out..." -> "BOO!!!" ECU -> kid, flat: "...hi Dad." -> *HIC* -> Dad faints.
Twist: "...wait. They're GONE!!" confetti cheer -> Dad ECU "*HIC!*" -> Mom + kid evil grins, low angle:
 "HOLD YOUR BREATH, DAD." -> kid ECU "*HIC!*" again (loop)."""
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


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))

DAD = dict(doodle.DAD, shirt=hx('2fb5a0'), pants=hx('3d5a9e'), sleeve=0.45)
MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'))
BOY = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ffc93c'))
N = 660
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
GOLD = hx('ffc93c')
TEAL = hx('19b5a5')
WATER = hx('6fd0ff')
WHITE = (1, 1, 1)

CAPS = {
    'p1': [[("HICCUPS.", OUT)], [("EVERYONE ", OUT), ("HAS A CURE.", PURPLE)]],
    'p2': [[("CURE #2:", BLUE)]],
    'p3': [[("CURE #3:", RED)]],
}
scenes13.CAPS = CAPS
card = _card13

HICS0 = (0, 22, 44)          # hook hiccups
HIC_BALLOON = 168
HIC_WATER = 300
HIC_CALM = 432
HIC_DAD = 540
HIC_LOOP = 628


def hic_jolt(lf, hits, h=60):
    """upward jolt offset for hiccup at hits"""
    o = 0
    for t in hits:
        if t <= lf < t + 10:
            u = (lf - t) / 10
            o = max(o, h * math.sin(math.pi * u) * (1 - u * 0.3))
    return o


# ------------------------------------------------------------------ sets / props
def room(ctx, lf):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('ffe2b8')); ctx.fill()
    for k in range(-30, 40):
        ctx.rectangle(k * 120, -3000, 60, 4450)
    setc(ctx, hx('ffd6a0')); ctx.fill()
    # window
    rect_r(ctx, 640, 560, 330, 380, 12); fl(ctx, hx('9fe0ff'), 8)
    ellipse(ctx, 720, 660, 50, 30); setc(ctx, WHITE); ctx.fill()
    ctx.move_to(805, 560); ctx.line_to(805, 940); ctx.move_to(640, 750); ctx.line_to(970, 750); ink(ctx, 6); ctx.stroke()
    # picture
    rect_r(ctx, 150, 620, 230, 180, 8); fl(ctx, GOLD, 7)
    rect_r(ctx, 170, 640, 190, 140, 4); fl(ctx, hx('7fd0ff'), 4)
    poly(ctx, [(180, 770), (240, 690), (290, 750), (320, 715), (350, 770)]); fl(ctx, GREEN, 4)
    # lamp
    rect_r(ctx, 1010, 980, 18, 470, 6); fl(ctx, hx('3a2a40'), 4)
    poly(ctx, [(950, 990), (1090, 990), (1060, 880), (980, 880)]); fl(ctx, ORANGE, 6)
    # sofa
    rect_r(ctx, 170, 1090, 760, 200, 40); fl(ctx, TEAL, 8)
    rect_r(ctx, 120, 1200, 110, 220, 30); fl(ctx, hx('15998c'), 8)
    rect_r(ctx, 870, 1200, 110, 220, 30); fl(ctx, hx('15998c'), 8)
    rect_r(ctx, 210, 1260, 680, 160, 24); fl(ctx, hx('1fc8b6'), 8)
    ctx.move_to(550, 1270); ctx.line_to(550, 1410); ink(ctx, 5); ctx.stroke()
    # floor + rug
    ctx.rectangle(-3000, 1450, 7000, 3000); setc(ctx, hx('c98a52')); ctx.fill()
    ctx.move_to(-3000, 1450); ctx.line_to(4000, 1450); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 540, 1640, 520, 110); fl(ctx, hx('ff6b8a'), 6)
    ellipse(ctx, 540, 1640, 400, 75); ink(ctx, 4); ctx.stroke()


def glass(ctx, x, y, s=1.0, a=0.0, full=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-34, -60), (34, -60), (26, 60), (-26, 60)]); fl(ctx, (0.85, 0.95, 1.0), 5)
    if full > 0:
        top = 60 - 110 * full
        poly(ctx, [(-26 - 8 * (top + 60) / 120 + 8, top), (26 + 8 * (top + 60) / 120 - 8, top), (26, 60), (-26, 60)])
        setc(ctx, WATER); ctx.fill()
    poly(ctx, [(-34, -60), (34, -60), (26, 60), (-26, 60)]); ink(ctx, 5); ctx.stroke()
    ctx.restore()


def drops(ctx, x, y, t, n=26, spread=1.0, seed=3, up=1.0):
    """fountain of water drops from (x, y), t = 0..1"""
    if t <= 0:
        return
    rnd = random.Random(seed)
    for i in range(n):
        vx = rnd.uniform(-1, 1) * 900 * spread; vy = -rnd.uniform(900, 1700) * up
        tt = t * rnd.uniform(0.7, 1.0)
        px = x + vx * tt; py = y + vy * tt + 2600 * tt * tt
        r = rnd.uniform(14, 30)
        ellipse(ctx, px, py, r * 0.8, r); fl(ctx, WATER, 4)


def drips(ctx, x, y, w, lf, seed=5):
    rnd = random.Random(seed)
    for i in range(9):
        dx = rnd.uniform(-w, w); ph = (lf * 6 + i * 37) % 160
        ellipse(ctx, x + dx, y + ph, 10, 16); fl(ctx, WATER, 3)


def confetti(ctx, lf, seed=11):
    rnd = random.Random(seed)
    cols = [RED, YEL, BLUE, GREEN, PINK, ORANGE, PURPLE]
    for i in range(70):
        x = rnd.uniform(-60, 1140); y0 = rnd.uniform(-900, 0); v = rnd.uniform(14, 26)
        y = y0 + lf * v
        if y > 1950:
            continue
        ctx.save(); ctx.translate(x + 30 * math.sin(lf * 0.2 + i), y); ctx.rotate(lf * 0.2 + i)
        ctx.rectangle(-14, -8, 28, 16); fl(ctx, cols[i % 7], 3); ctx.restore()


def hic_burst(ctx, x, y, t, s=1.0):
    """little star burst around the mouth on a hiccup"""
    if not 0 < t < 1:
        return
    for i in range(8):
        a = i * math.pi / 4
        r0 = 40 * s + 120 * s * t; r1 = r0 + 60 * s * (1 - t)
        ctx.move_to(x + math.cos(a) * r0, y + math.sin(a) * r0); ctx.line_to(x + math.cos(a) * r1, y + math.sin(a) * r1)
    ink(ctx, 8 * s); ctx.stroke()


def puffed(ctx, cx, cy, R, amt, tint):
    """inflated cheeks + colour tint over a face drawn at (cx, cy, R)"""
    if amt <= 0:
        return
    ctx.save()
    ctx.new_path(); ctx.arc(cx, cy + R * 0.3, R * 0.8, 0, 2 * math.pi)
    setc(ctx, tint + (0.3 * amt,)); ctx.fill()
    for sx in (-1, 1):
        ellipse(ctx, cx + sx * R * (0.55 + 0.25 * amt), cy + R * 0.38, R * (0.28 + 0.22 * amt), R * (0.24 + 0.18 * amt))
        setc(ctx, mix_(BOY['skin'], tint, 0.45 * amt)); ctx.fill_preserve(); ink(ctx, 7); ctx.stroke()
    # pursed lips
    ellipse(ctx, cx, cy + R * 0.5, R * 0.1, R * 0.07); fl(ctx, hx('d0505a'), 6)
    ctx.restore()


def mix_(a, b, t):
    return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))


# ------------------------------------------------------------------ close-ups
def kid_ecu(ctx, f, lf, bg, hits, eye_hic='shock', eye_rest='normal', mouth_rest='flat', z0=1.0, lab=True, ray_col=(1, 1, 1)):
    j = hic_jolt(lf, hits, 90)
    hic_now = any(t <= lf < t + 10 for t in hits)
    ctx.save(); cam(ctx, 540, 960, z0, 0, shake_at(lf, list(hits), 8, 16), f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    rays(ctx, 540, 900, 260, 1700, lf * 0.03, col=ray_col, a=0.35, n=18)
    cx, cy, R = 540, 900 - j, 300
    face(ctx, BOY, P(eye=eye_hic if hic_now else eye_rest, mouth='open' if hic_now else mouth_rest, head=0), cx, cy, R,
         0.04 * math.sin(lf * 0.5))
    for t in hits:
        hic_burst(ctx, cx, cy + R * 0.55, pop(lf, t, t + 9), 1.2)
    sweat(ctx, cx + 1.02 * R, cy - 0.35 * R, lf, 1.3)
    ctx.restore()
    if lab:
        for t in hits:
            if t - 1 <= lf < t + 18:
                label(ctx, "*HIC!*", 540 + (90 if (t // 2) % 2 else -90), 1480, 170, YEL, (-0.08 if (t // 2) % 2 else 0.08), pop(lf, t - 1, t + 3))


def dad_ecu(ctx, f, lf, bg, eye, mouth, shake=0, z0=1.0, jolt=0, ray_col=(1, 1, 1)):
    ctx.save(); cam(ctx, 540, 960, z0, 0, shake, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    rays(ctx, 540, 900, 260, 1700, lf * 0.03, col=ray_col, a=0.35, n=18)
    cx, cy, R = 540, 900 - jolt, 310
    face(ctx, DAD, P(eye=eye, mouth=mouth, head=0), cx + 4 * math.sin(lf * 2.7), cy, R, 0.02 * math.sin(lf * 0.9))
    ctx.restore()
    return cx, cy, R


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    kid_ecu(ctx, f, f, hx('8a3cff'), HICS0, z0=1.02 + 0.06 * eout(pop(f, 0, 60)), ray_col=(1, 0.9, 1))
    card(ctx, 'p1', f, -6, 56)


def s2(ctx, f):
    lf = f - 60
    if lf < 30:
        ctx.save(); cam(ctx, 540, 1100, 1.0, 0, 0, f)
        room(ctx, lf)
        draw(ctx, 300, 1640 - 186 * 1.8, 1.8, 1, DAD, P(eye='happy', mouth='grin', rsh=-110, rel=-10, lsh=20, head=-4))
        j = hic_jolt(lf, [14], 50)
        draw(ctx, 790, 1640 - 186 * 1.5 - j, 1.5, -1, BOY, P(eye='shock' if 14 <= lf < 24 else 'normal', mouth='open' if 14 <= lf < 24 else 'flat'))
        ctx.restore()
        label2(ctx, "\"HOLD YOUR", "BREATH!\"", WHITE, pop(lf, 1, 5), 120, col2=YEL, y=600)
        if 14 <= lf < 28:
            label(ctx, "*HIC!*", 800, 900, 100, YEL, 0.08, pop(lf, 14, 17))
    elif lf < 108:
        il = lf - 30
        amt = eout(pop(il, 0, 70))
        tint = mix_(RED, PURPLE, clamp((il - 30) / 40))
        R = 260 + 70 * amt
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.12 * amt, 0, 6 * clamp((il - 50) / 28), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, mix_(hx('ff8a1f'), PURPLE, amt * 0.6)); ctx.fill()
        rays(ctx, 540, 900, 260, 1700, il * 0.03, col=(1, 1, 1), a=0.3, n=18)
        face(ctx, BOY, P(eye='shock' if il > 40 else 'glare', mouth='flat', head=0), 540, 900, R, 0.03 * math.sin(il * 0.4))
        puffed(ctx, 540, 900, R, amt, tint)
        if il > 20:
            sweat(ctx, 540 + R * 1.02, 900 - R * 0.4, il, 1.4); sweat(ctx, 540 - R * 1.0, 900 - R * 0.2, il + 30, 1.2)
        ctx.restore()
        if il < 26:
            label1(ctx, "5 SECONDS...", WHITE, pop(il, 2, 6), 110, -0.04, y=1500)
        elif il < 52:
            label1(ctx, "15 SECONDS...", YEL, pop(il, 26, 30), 120, 0.04, y=1500)
        else:
            label1(ctx, "30 SECONDS!!", RED, pop(il, 52, 56), 140, -0.05, y=1500)
    else:
        # *HIC* -> balloon zip around the room
        il = lf - 108
        ctx.save(); cam(ctx, 540, 1060, 0.95, 0, shake_at(il, [0], 8, 18), f)
        room(ctx, il)
        t = clamp(il / 34)
        if t < 1:
            ang = t * 4.2 * math.pi
            px = 540 + 330 * math.sin(ang) * (1 - 0.3 * t); py = 1080 - 200 * math.sin(ang * 0.5 + 0.4) + 220 * t * t
            rot = math.degrees(ang) * 1.2
            pb = draw(ctx, px, py - 186 * 1.3, 1.3, 1, BOY, P(eye='shock', mouth='scream', rsh=160, lsh=-160, lhip=-30, rhip=30, rot=rot))
            # puff trail
            for k in range(6):
                tk = t - k * 0.04
                if tk > 0:
                    ak = tk * 4.2 * math.pi
                    qx = 540 + 330 * math.sin(ak) * (1 - 0.3 * tk); qy = 1080 - 200 * math.sin(ak * 0.5 + 0.4) + 220 * tk * tk
                    ellipse(ctx, qx, qy + 60, 40 - 5 * k, 40 - 5 * k); setc(ctx, (1, 1, 1, 0.8 - 0.12 * k)); ctx.fill()
        else:
            j = hic_jolt(il, [40], 40)
            draw(ctx, 560, 1300 - 186 * 1.5 - j, 1.5, 1, BOY, P(eye='closed' if il < 40 else 'shock', mouth='wavy', rsh=40, lsh=-40, rot=-12))
            puff(ctx, 560, 1250, pop(il, 34, 44), 1.6)
        ctx.restore()
        if il < 34:
            label(ctx, "*PFFFFFFT!*", 540, 560, 130, WHITE, -0.06, pop(il, 0, 4))
        else:
            label(ctx, "*FLOMP*", 540, 560, 110, WHITE, 0.05, pop(il, 34, 38))
            if il >= 40:
                label1(ctx, "*HIC!*", YEL, pop(il, 40, 43), 130, 0.06, y=1500)


def s3(ctx, f):
    lf = f - 210
    if lf < 30:
        ctx.save(); cam(ctx, 600, 1000, 1.25, 0, 0, f)
        room(ctx, lf)
        b = draw(ctx, 330, 1640 - 186 * 1.8, 1.8, 1, MOM, P(eye='smug', mouth='smile', rsh=-150, rel=-20, lsh=20, head=-4))
        draw(ctx, 820, 1640 - 186 * 1.5, 1.5, -1, BOY, P(eye='normal', mouth='flat', rsh=20, lsh=-20))
        ctx.restore()
        hx_, hy_ = b['front']
        glass(ctx, hx_, hy_ - 50, 1.6, 0.1)
        card(ctx, 'p2', f, 210, 238)
        label2(ctx, "\"Drink water", "UPSIDE DOWN!\"", WHITE, pop(lf, 3, 7), 115, col2=BLUE, y=1460)
    elif lf < 90:
        il = lf - 30
        roll = 180 * eio(pop(il, 0, 18))
        ctx.save(); cam(ctx, 560, 1420 + 600 * eio(pop(il, 0, 18)), 1.25, roll, 0, f)
        room(ctx, il)
        # kid doing a handstand to drink upside down
        gul = math.sin(il * 0.9) * 6 if il > 20 else 0
        bk = draw(ctx, 560, 1640 - 186 * 1.5 + gul, 1.5, 1, BOY, P(eye='closed', mouth='flat', rot=180, rsh=170, lsh=-170, rel=0, lel=0, lhip=-12, rhip=12))
        hx_, hy_ = bk['head']
        glass(ctx, 560 + 70, 1640 - 186 * 1.5 + 186 * 1.5 * 0.95, 1.2, 2.6, 1 - 0.8 * clamp((il - 20) / 40))
        ctx.restore()
        if il < 18:
            label(ctx, "*FLIP*", 540, 560, 120, WHITE, -0.05, pop(il, 0, 4))
        else:
            k = 0 if il < 38 else 1
            label(ctx, "*GULP GULP*", 540 + (-60 if k else 60), 540 + k * 40, 115, WATER, (-0.05, 0.05)[k], pop(il, 20 + 18 * k, 24 + 18 * k))
    else:
        il = lf - 90
        ctx.save(); cam(ctx, 540, 1060, 1.0, 0, shake_at(il, [0], 8, 20), f)
        room(ctx, il)
        wet = pop(il, 8, 14)
        b = draw(ctx, 320, 1640 - 186 * 1.8, 1.8, 1, MOM, P(eye='shock' if il < 14 else 'glare', mouth='scream' if il < 14 else 'flat', rsh=20, lsh=-20, head=-4))
        j = hic_jolt(il, [0], 60)
        kb = draw(ctx, 780, 1640 - 186 * 1.5 - j, 1.5, -1, BOY, P(eye='shock', mouth='open' if il < 14 else 'grin', rsh=30, lsh=-30))
        ctx.restore()
        mx_, my_ = b['head']; kx_, ky_ = kb['head']
        drops(ctx, kx_ - 60, ky_ + 40, pop(il, 0, 16), n=34, spread=0.5, up=1.0)
        if wet > 0:
            # soaked: wet hair drip + puddle
            ellipse(ctx, mx_, 1650, 240 * wet, 40 * wet); setc(ctx, WATER + (0.8,)); ctx.fill()
            drips(ctx, mx_, my_ - 40, 150, il)
        label(ctx, "*HIC!* *SPLOOSH!*", 540, 560, 120, WATER, -0.05, pop(il, 0, 4))
        if il >= 18:
            label1(ctx, "\"...thanks.\"", WHITE, pop(il, 18, 22), 110, 0.03, y=1500)


def s4(ctx, f):
    lf = f - 340
    if lf < 32:
        ctx.save(); cam(ctx, 540, 1100, 1.05, 0, 0, f)
        room(ctx, lf)
        draw(ctx, 790, 1640 - 186 * 1.5, 1.5, -1, BOY, P(eye='normal', mouth='flat', rsh=20, lsh=-20))
        tip = math.sin(lf * 0.5)
        draw(ctx, 170 + lf * 3, 1640 - 186 * 1.7 + 20, 1.7, 1, DAD,
             P(eye='smug', mouth='grin', rsh=120, rel=-60, lsh=-120, lel=60, torso=14, head=8, lhip=-10 + 18 * tip, rhip=10 - 18 * tip, lkn=20, rkn=20))
        ctx.restore()
        card(ctx, 'p3', f, 340, 370)
        label1(ctx, "*tiptoe tiptoe*", WHITE, pop(lf, 4, 8), 95, 0.04, y=1500)
    elif lf < 60:
        il = lf - 32
        dad_ecu(ctx, f, il, RED, 'glare', 'scream', shake=shake_at(il, [0], 16, 30), z0=1.0 + 0.2 * eout(pop(il, 0, 6)), ray_col=(1, 0.85, 0.5))
        label(ctx, "\"BOO!!!\"", 540, 1480, 220, YEL, -0.06, pop(il, 0, 3))
    elif lf < 92:
        il = lf - 60
        ctx.save(); cam(ctx, 600, 1260, 1.6 + 0.1 * eout(pop(il, 0, 32)), 0, 0, f)
        room(ctx, il)
        draw(ctx, 600, 1640 - 186 * 1.5, 1.5, -1, BOY, P(eye='normal', mouth='flat', rsh=20, lsh=-20, head=-4))
        ctx.restore()
        label2(ctx, "\"...hi,", "Dad.\"", WHITE, pop(il, 6, 10), 130, y=1440)
        cricket = (il // 4) % 2
        label(ctx, "*cricket*", 820, 600, 80, WHITE, 0.05, 1 if il > 14 and cricket else 0)
    else:
        il = lf - 92
        ctx.save(); cam(ctx, 540, 1100, 1.0, 0, shake_at(il, [0, 22], 8, 14), f)
        room(ctx, il)
        j = hic_jolt(il, [0], 70)
        kb = draw(ctx, 680, 1640 - 186 * 1.5 - j, 1.5, -1, BOY, P(eye='shock' if il < 10 else 'normal', mouth='open' if il < 10 else 'flat', rsh=20, lsh=-20))
        fall = eio(pop(il, 6, 22))
        draw(ctx, 280, 1640 - 186 * 1.7, 1.7, 1, DAD, P(eye='shock' if fall < 1 else 'closed', mouth='scream' if fall < 1 else 'wavy',
                                                    rsh=150, lsh=-150, rot=-85 * fall))
        ctx.restore()
        kx_, ky_ = kb['head']
        hic_burst(ctx, kx_ - 40, ky_ + 60, pop(il, 0, 9), 1.0)
        label(ctx, "*HIC!*", 790, 760, 110, YEL, 0.06, pop(il, 0, 3))
        if il >= 6:
            label(ctx, "\"AAAAH!\"", 330, 560, 110, RED, -0.08, pop(il, 6, 9))
        if il >= 22:
            label1(ctx, "*TIMBER* *THUD*", WHITE, pop(il, 22, 25), 100, -0.03, y=1500)


def s5(ctx, f):
    lf = f - 470
    if lf < 26:
        kid_ecu(ctx, f, lf, TEAL, (), eye_rest='shock', mouth_rest='flat', z0=1.0 + 0.05 * eout(pop(lf, 0, 26)), lab=False)
        label2(ctx, "\"...wait.", "They're GONE!\"", WHITE, pop(lf, 3, 7), 125, col2=GREEN, y=1440)
    elif lf < 70:
        il = lf - 26
        jump = abs(math.sin(il * 0.35)) * 60
        ctx.save(); cam(ctx, 540, 1080, 1.0, 0, 0, f)
        room(ctx, il)
        draw(ctx, 230, 1640 - 186 * 1.7 - jump, 1.7, 1, DAD, P(eye='happy', mouth='grin', rsh=160, lsh=-160, rel=10, lel=-10))
        draw(ctx, 860, 1640 - 186 * 1.75 - abs(math.sin(il * 0.35 + 1)) * 60, 1.75, -1, MOM, P(eye='happy', mouth='grin', rsh=160, lsh=-160))
        draw(ctx, 545, 1660 - 186 * 1.5 - abs(math.sin(il * 0.35 + 2)) * 80, 1.5, 1, BOY, P(eye='happy', mouth='grin', rsh=160, lsh=-160))
        confetti(ctx, il)
        ctx.restore()
        sparkle(ctx, 160, 760, 40 + 8 * math.sin(il * 0.6)); sparkle(ctx, 930, 700, 34)
        label1(ctx, "\"YAAAAY!!\"", YEL, pop(il, 1, 5), 160, -0.05, y=560)
    elif lf < 106:
        il = lf - 70
        hits = [0]
        cx, cy, R = dad_ecu(ctx, f, il, hx('ff8a1f'), 'shock' if il < 12 else 'shock', 'open' if il < 10 else 'wavy',
                            shake=shake_at(il, hits, 8, 18), z0=1.0 + 0.1 * eout(pop(il, 0, 36)), jolt=hic_jolt(il, hits, 90))
        hic_burst(ctx, cx, cy + R * 0.55 - hic_jolt(il, hits, 90), pop(il, 0, 9), 1.2)
        label(ctx, "*HIC!*", 540, 1480, 170, YEL, 0.06, pop(il, 0, 3))
        label(ctx, "Dad?", 540, 520, 90, WHITE, -0.04, pop(il, 14, 18))
    elif lf < 158:
        il = lf - 106
        turn = eio(pop(il, 0, 14))
        ctx.save(); cam(ctx, 540, 1160, 1.15 + 0.12 * eout(pop(il, 0, 52)), 0, 0, f)
        # low angle: wall + ceiling glow
        ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('3a2a60')); ctx.fill()
        rays(ctx, 540, 900, 200, 1700, il * 0.02, col=(1, 0.4, 0.6), a=0.25, n=16)
        bm = draw(ctx, 330, 1820 - 186 * 2.1, 2.1, 1 if turn > 0.5 else -1, MOM, P(eye='smug' if turn > 0.5 else 'normal', mouth='grin', rsh=-150, rel=-20, head=-6))
        bb = draw(ctx, 780, 1820 - 186 * 1.8, 1.8, -1 if turn > 0.5 else 1, BOY, P(eye='smug' if turn > 0.5 else 'normal', mouth='grin', rsh=-40, rel=-90, head=6))
        ctx.restore()
        hx_, hy_ = bm['front']
        glass(ctx, hx_, hy_ - 60, 2.0, 0.1)
        if turn >= 1:
            label2(ctx, "\"HOLD YOUR", "BREATH, DAD.\"", WHITE, pop(il, 16, 20), 125, col2=RED, y=600)
            twitch(ctx, 540, 1460, il, 1.2) if False else None
    else:
        il = lf - 158
        kid_ecu(ctx, f, il, hx('8a3cff'), (0,), z0=1.02, ray_col=(1, 0.9, 1))
        card(ctx, 'p1', f, 628 - 2)


SHOTS = [(0, s1), (60, s2), (210, s3), (340, s4), (470, s5)]
CUTS = (60, 90, 168, 210, 240, 300, 340, 372, 400, 432, 470, 496, 540, 576, 628)


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
                              "-i", "out/hiccups_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
