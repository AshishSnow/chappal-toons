"""'We Leave In 5 Minutes' - original, general-audience comedy short, ~22s.
ECU: Dad at the front door jangling keys: "WE LEAVE IN 5 MINUTES!" Windshield cam: he honks alone in the car.
Beat 1: kid hops around with one shoe - the other is spinning on the ceiling fan.
Beat 2: car rolls... Mom: "DID I TURN OFF THE OVEN?!" - screech, reverse. "It was off."
Beat 3: 10 seconds in, kid: "I need the bathroom." Dad ECU, eye twitch, steam.
Twist: Mom reads the invitation: the party is TOMORROW. Triple split-screen glare at Dad. Loops to the ECU."""
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
FLOOR = 1430
RED = hx('ff3b5c')

CAPS = {
    'p1': [[("WHEN DAD SAYS WE", OUT)], [("LEAVE IN ", OUT), ("5 MINUTES", RED)]],
    'p2': [[("SOMEONE LOST", OUT)], [("ONE SHOE", hx('1f8bff'))]],
    'p3': [[("THEN MOM REMEMBERS", OUT)], [("THE OVEN", hx('ff8a1f'))]],
    'p4': [[("10 SECONDS INTO", OUT)], [("THE DRIVE", hx('8a3cff'))]],
    'p5': [[("AND THEN THE", OUT)], [("PLOT TWIST", RED)]],
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


def face(ctx, ch, p, cx, cy, Rt, rot=0.0, f_=1):
    b = draw_hip(_SCR, 0, 0, 1, f_, ch, p)
    hd, R = b['head'], b['R']
    s = Rt / R
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s); ctx.translate(-hd[0], -hd[1])
    draw_hip(ctx, 0, 0, 1, f_, ch, p)
    ctx.restore()


def talk(lf, a='open', b='scream', rate=4):
    return a if (lf // rate) % 2 == 0 else b


def hspeed(ctx, x0, x1, y0, y1, t, n=12, seed=3, a=0.8, dirn=1):
    rnd = random.Random(seed)
    for k in range(n):
        yy = rnd.uniform(y0, y1); ln = rnd.uniform(120, 340)
        xx = x0 + ((rnd.uniform(0, 1) * (x1 - x0) + dirn * t * 90) % (x1 - x0))
        ctx.move_to(xx, yy); ctx.line_to(xx + ln, yy)
        setc(ctx, (1, 1, 1, a)); ctx.set_line_width(rnd.uniform(6, 14)); ctx.stroke()


# ------------------------------------------------------------------ props
def shoe(ctx, x, y, s=1.0, a=0.0, col=hx('ff4d5e')):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-70, 20); ctx.curve_to(-72, -30, -50, -50, -20, -48); ctx.line_to(10, -20)
    ctx.curve_to(50, -16, 80, -6, 80, 20); ctx.close_path(); fl(ctx, col, 6)
    ctx.rectangle(-72, 14, 154, 16); fl(ctx, (1, 1, 1), 5)
    for k in range(3):
        ctx.move_to(-20 + k * 14, -40 + k * 8); ctx.line_to(-6 + k * 14, -44 + k * 8); setc(ctx, (1, 1, 1)); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def wall_clock(ctx, x, y, r, t):
    ellipse(ctx, x, y, r, r); fl(ctx, (1, 1, 1), 10)
    for k in range(12):
        a = k * math.pi / 6
        ctx.move_to(x + math.cos(a) * r * 0.78, y + math.sin(a) * r * 0.78); ctx.line_to(x + math.cos(a) * r * 0.9, y + math.sin(a) * r * 0.9); ink(ctx, 6); ctx.stroke()
    for ang, ln, w in ((t, 0.75, 8), (t / 12, 0.5, 12)):
        ctx.move_to(x, y); ctx.line_to(x + math.sin(ang) * r * ln, y - math.cos(ang) * r * ln); ink(ctx, w); ctx.stroke()
    ellipse(ctx, x, y, 10, 10); setc(ctx, RED); ctx.fill()


def oven(ctx, x, y, s=1.0, t=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rect_r(ctx, -110, -110, 220, 220, 16); fl(ctx, hx('dfe6f2'), 7)
    rect_r(ctx, -80, -40, 160, 120, 10); fl(ctx, hx('2a2840'), 6)
    for k in range(3):
        ellipse(ctx, -60 + k * 60, -78, 12, 12); fl(ctx, hx('ff8a1f'), 4)
    for k in range(3):   # flames inside
        fx = -45 + k * 45; fh = 40 + 12 * math.sin(t * 0.6 + k * 2)
        poly(ctx, [(fx - 18, 70), (fx + 18, 70), (fx, 70 - fh)]); setc(ctx, hx('ff8a1f')); ctx.fill()
        poly(ctx, [(fx - 9, 70), (fx + 9, 70), (fx, 70 - fh * 0.55)]); setc(ctx, hx('ffe14d')); ctx.fill()
    ctx.restore()


def invite(ctx, x, y, s, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -110, -80, 220, 160, 10); fl(ctx, hx('fff6c8'), 6)
    ctx.rectangle(-110, -80, 220, 40); fl(ctx, hx('ff6fa8'), 6)
    for k in range(3):
        ctx.move_to(-80, -10 + k * 26); ctx.line_to(80 - 30 * (k % 2), -10 + k * 26); ink(ctx, 6); ctx.stroke()
    for k in range(3):   # little balloon doodles
        ellipse(ctx, -60 + k * 60, -60, 12, 15); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.restore()


def keys_jangle(ctx, x, y, lf, s=2.4):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    keychain(ctx, 0, 0, 0.5 * math.sin(lf * 0.9))
    keychain(ctx, 6, 4, -0.4 + 0.5 * math.sin(lf * 0.9 + 1.5))
    ctx.restore()


# ------------------------------------------------------------------ sets
def hallway(ctx, door=True):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('ffe08a')); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 120, -3000, 46, 6000); setc(ctx, hx('ffd46a')); ctx.fill()
    if door:
        ctx.rectangle(250, 300, 580, 1300); fl(ctx, hx('9fd8ff'), 12)
        ellipse(ctx, 380, 600, 110, 60); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()
        ellipse(ctx, 700, 520, 80, 44); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()
        ctx.rectangle(250, 1250, 580, 400); setc(ctx, hx('6fd06a')); ctx.fill()
        rect_r(ctx, 360, 1000, 360, 230, 30); fl(ctx, hx('ff3b5c'), 10)   # the car waiting outside
        ctx.rectangle(250, 300, 580, 1300); ink(ctx, 12); ctx.stroke()


def street(ctx, off):
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('9fd8ff')); ctx.fill()
    cols = [hx('ffb3d1'), hx('b6f0a0'), hx('ffe08a'), hx('c8b6ff')]
    for k in range(-4, 8):
        x = ((k * 360 - off) % 3600) - 900
        hh = 300 + 80 * (k % 3)
        ctx.rectangle(x, 760 - hh, 300, hh + 200); fl(ctx, cols[k % 4], 8)
        poly(ctx, [(x - 20, 760 - hh), (x + 150, 760 - hh - 120), (x + 320, 760 - hh)]); fl(ctx, hx('e05a4a'), 8)
        rect_r(ctx, x + 60, 760 - hh + 60, 80, 80, 8); fl(ctx, hx('fff6c8'), 6)
        tx = ((k * 360 + 200 - off * 1.3) % 3600) - 900
        ellipse(ctx, tx, 640, 90, 110); fl(ctx, hx('3fbf4a'), 8)
    cloud(ctx, 120 - off * 0.1 % 300, 420, 1.0); cloud(ctx, 760 - off * 0.1 % 300, 360, 0.8)
    ctx.rectangle(-500, 900, 2200, 2000); setc(ctx, hx('6b6b7d')); ctx.fill()


def car_front(ctx, lf, off, who, f, bounce=True, body=hx('ff3b5c')):
    """windshield camera: looking at the car head-on through the glass.
    who: list of (kind, ch, pose, x, y, R, flip) drawn inside the windshield"""
    by = 6 * math.sin(lf * 0.9) if bounce else 0
    street(ctx, off)
    ctx.save(); ctx.translate(0, by)
    # wheels
    for wx in (190, 890):
        rect_r(ctx, wx - 90, 1420, 180, 160, 40); fl(ctx, hx('2a2840'), 9)
    # roof + body
    rect_r(ctx, 60, 620, 960, 900, 120); fl(ctx, body, 12)
    WS = [(200, 720), (880, 720), (960, 1150), (120, 1150)]
    poly(ctx, WS); fl(ctx, hx('586a96'), 10)
    ctx.save(); poly(ctx, WS); ctx.clip()
    # rear window glow + seats
    ctx.rectangle(260, 740, 560, 120); setc(ctx, hx('9fd8ff')); ctx.fill()
    for kind, ch, p, x, y, R, fp in who:
        if kind == 'back':
            face(ctx, ch, p, x, y, R, 0, fp)
    for sx in (330, 750):
        rect_r(ctx, sx - 120, 820, 240, 400, 60); fl(ctx, hx('2a2840'), 8)
        rect_r(ctx, sx - 70, 780, 140, 80, 26); fl(ctx, hx('3a3a52'), 7)
    for kind, ch, p, x, y, R, fp in who:
        if kind == 'front':
            face(ctx, ch, p, x, y, R, 0, fp)
        elif kind == 'lean':
            face(ctx, ch, p, x, y, R, 0, fp)
    # steering wheel
    ctx.new_path(); ctx.arc(330, 1100, 120, math.pi, 2 * math.pi); ink(ctx, 34); ctx.stroke()
    ctx.new_path(); ctx.arc(330, 1100, 120, math.pi, 2 * math.pi); setc(ctx, hx('3a3a52')); ctx.set_line_width(20); ctx.stroke()
    # glass sheen
    poly(ctx, [(620, 720), (720, 720), (480, 1150), (380, 1150)]); setc(ctx, (1, 1, 1, 0.13)); ctx.fill()
    poly(ctx, [(760, 720), (800, 720), (560, 1150), (520, 1150)]); setc(ctx, (1, 1, 1, 0.1)); ctx.fill()
    ctx.restore()
    poly(ctx, WS); ink(ctx, 12); ctx.stroke()
    # mirror
    rect_r(ctx, 480, 730, 120, 44, 14); fl(ctx, hx('2a2840'), 6)
    # hood, lights, grille
    rect_r(ctx, 60, 1150, 960, 330, 60); fl(ctx, body, 12)
    for hx_ in (200, 880):
        ellipse(ctx, hx_, 1290, 85, 60); fl(ctx, hx('fff6c8'), 9)
        ellipse(ctx, hx_ - 20, 1275, 25, 16); setc(ctx, (1, 1, 1)); ctx.fill()
    rect_r(ctx, 360, 1250, 360, 110, 30); fl(ctx, hx('2a2840'), 8)
    for k in range(4):
        ctx.move_to(390, 1272 + k * 22); ctx.line_to(690, 1272 + k * 22); setc(ctx, hx('6b6b7d')); ctx.set_line_width(6); ctx.stroke()
    rect_r(ctx, 40, 1420, 1000, 70, 30); fl(ctx, hx('dfe6f2'), 9)
    ctx.restore()


DRIVE = dict(rsh=150, rel=-30, lsh=-150, lel=30, torso=0)


# ------------------------------------------------------------------ shots
def opening_face(ctx, f, lf, lab=True):
    sh = shake_at(lf, [0], 12, 20) + 2
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.04 * eout(pop(lf, 0, 60)), 0, sh, f)
    hallway(ctx)
    rays(ctx, 540, 980, 300, 1400, lf * 0.02, col=(1, 1, 1), a=0.35, n=16)
    pd = P(eye='shock', mouth=talk(lf, 'scream', 'open', 5), head=6)
    face(ctx, DAD, pd, 540 + 8 * math.sin(lf * 0.4), 980, 400, 0.05 + 0.03 * math.sin(lf * 0.3))
    # arm thrust up, keys jangling
    ellipse(ctx, 900, 1200, 66, 60); fl(ctx, DAD["skin"], 9)
    keys_jangle(ctx, 900, 1220, lf, 2.0)
    sweat(ctx, 160, 720 + (lf % 24) * 5, 2.2)
    ctx.restore()
    if lab:
        label(ctx, "\"WE LEAVE IN 5 MINUTES!\"", 540, 1480, 92, (1, 1, 1), -0.04, pop(lf, 0, 4) if lf > 0 else 1)


def s1(ctx, f):
    if f < 56:
        opening_face(ctx, f, f)
    else:
        lf = f - 56
        HONKS = [4, 20, 36]
        ctx.save(); cam(ctx, 540, 1040, 1.1 + 0.05 * eout(pop(lf, 0, 54)), 0, shake_at(lf, HONKS, 8, 18), f)
        hon = any(h <= lf < h + 10 for h in HONKS)
        pd = P(eye='glare' if hon else 'normal', mouth='scream' if hon else 'flat', rsh=170, rel=-10, lsh=-150, lel=30, head=-4)
        car_front(ctx, lf, 0, [('front', DAD, pd, 330, 900, 110, 1)], f, bounce=False)
        if hon:
            for k in range(3):
                ctx.move_to(250 + k * 90, 1210); ctx.line_to(230 + k * 110, 1150 - k * 10); setc(ctx, hx('ffe14d')); ctx.set_line_width(12); ctx.stroke()
        ctx.restore()
        if lf >= 4:
            label(ctx, "*HONK HONK*", 540, 1530, 130, hx('ffe14d'), -0.05, pop(lf, 4, 8))
        if lf >= 26:
            label(ctx, "(4 MINUTES EARLY)", 540, 1640, 56, (1, 1, 1), 0.03, pop(lf, 26, 30))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 60:
        il = lf
        ctx.save(); cam(ctx, 540, 1000, 1.0, 2 * math.sin(il * 0.3), shake_at(il, [10, 30], 6, 12), f)
        hallway(ctx, door=False)
        ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('c98a52')); ctx.fill()
        ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()
        wall_clock(ctx, 820, 650, 110, il * 0.9)
        # shoe rack on the left, shoes flying out of it
        ctx.rectangle(60, 1100, 280, 330); fl(ctx, hx('a86a3a'), 8)
        ctx.move_to(60, 1260); ctx.line_to(340, 1260); ink(ctx, 7); ctx.stroke()
        rnd = random.Random(4)
        for k in range(6):
            t0 = k * 8
            v = pop(il, t0, t0 + 26)
            if 0 < v < 1:
                sx = lerp(200, rnd.uniform(-100, 1180), v); sy = 1180 - 700 * math.sin(math.pi * v) + 300 * v
                shoe(ctx, sx, sy, 0.8, v * 9 + k, [hx('1f8bff'), hx('3fbf4a'), hx('ffe14d'), hx('8a3cff')][k % 4])
        # boy hopping on one foot
        hop = abs(math.sin(il * 0.35)) * 90
        pb = P(eye='shock', mouth=talk(il, 'open', 'scream', 6), lhip=-60, lkn=90, rhip=0, rkn=0, rsh=-150, rel=-30, lsh=140, lel=30, torso=-6)
        draw_hip(ctx, 600, FLOOR - 210 - hop, 1.8, -1, BOY, pb)
        sweat(ctx, 790, 700 - hop + (il % 16) * 4, 1.8)
        ctx.restore()
        label(ctx, "\"WHERE'S MY SHOE?!\"", 540, 1500, 100, (1, 1, 1), -0.04, pop(il, 2, 6))
        label(ctx, "+10 MIN", 820, 830, 70, RED, 0.08, pop(il, 30, 34))
    else:
        il = lf - 60
        # low angle looking UP at the ceiling fan, shoe spinning on a blade
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.1 * eout(pop(il, 0, 60)), 0, shake_at(il, [14], 10, 16), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('fff2c8')); ctx.fill()
        for k in range(10):
            ctx.new_path(); ctx.arc(540, 760, 120 + k * 120, 0, 2 * math.pi); setc(ctx, hx('ffe9a8')); ctx.set_line_width(40); ctx.stroke()
        spin = il * 0.5
        for k in range(4):
            a = spin + k * math.pi / 2
            ctx.save(); ctx.translate(540, 760); ctx.rotate(a)
            rect_r(ctx, 40, -50, 380, 100, 40); fl(ctx, hx('c98a52'), 9)
            if k == 0:
                shoe(ctx, 330, -10, 1.1, 0.3, hx('ff4d5e'))
            ctx.restore()
        ellipse(ctx, 540, 760, 70, 70); fl(ctx, hx('dfe6f2'), 9)
        # boy face at the bottom, looking up, shocked
        face(ctx, BOY, P(eye='shock', mouth='open' if il < 14 else 'scream', head=-20), 540, 1340, 240, 0.0)
        ctx.restore()
        if il >= 14:
            label(ctx, "...HOW?!", 540, 1620, 110, hx('ffe14d'), 0.05, pop(il, 14, 18))
    card(ctx, 'p2', f, 114, 226)


def s3(ctx, f):
    lf = f - 230
    OVEN = 44
    pm_ok = P(eye='happy', mouth='grin', head=4)
    pb_ok = P(eye='happy', mouth='smile')
    if lf < OVEN:
        off = 30 * lf * eout(pop(lf, 0, 20))
        pd = dict(DRIVE); pd.update(eye='happy', mouth='grin', head=-4)
        ctx.save(); cam(ctx, 540, 1040, 1.1, 0, 3, f)
        car_front(ctx, lf, off, [('back', BOY, P(**pb_ok), 540, 860, 75, 1), ('front', DAD, P(**pd), 330, 900, 110, 1),
                                 ('front', MOM, pm_ok, 750, 905, 105, -1)], f)
        hspeed(ctx, -100, 1180, 200, 600, lf, seed=5, a=0.5, dirn=-1)
        ctx.restore()
        label(ctx, "FINALLY!", 540, 1530, 130, hx('3fbf5a'), -0.04, pop(lf, 4, 8))
    elif lf < 96:
        il = lf - OVEN
        # SCREECH + reverse
        rev = pop(il, 14, 40)
        off = 30 * OVEN * 0.9 - 900 * ein(rev)
        pd = dict(DRIVE); pd.update(eye='shock', mouth='scream', head=-6)
        pm = P(eye='shock', mouth=talk(il, 'scream', 'open', 4), head=8, rsh=-170, rel=0, lsh=170, lel=0)
        ctx.save(); cam(ctx, 540, 1040, 1.1 + 0.06 * eout(pop(il, 0, 6)), -3 * eout(rev) * math.sin(il * 0.8), shake_at(il, [0, 14], 10, 26), f)
        car_front(ctx, il, off, [('back', BOY, P(eye='shock', mouth='open'), 540, 860, 75, 1), ('front', DAD, P(**pd), 330, 900, 110, 1),
                                 ('front', MOM, pm, 750, 905, 105, -1)], f, bounce=rev > 0)
        if 0 < rev < 1:
            hspeed(ctx, -100, 1180, 200, 640, il, seed=8, a=0.8, dirn=1)
        ctx.restore()
        # thought bubble with a blazing oven
        u = eout(pop(il, 2, 10))
        if u > 0:
            ctx.save(); ctx.translate(820, 650); ctx.scale(1.3 * u, 1.3 * u)
            for k, (bx, byy, r) in enumerate(((-70, 120, 16), (-50, 86, 24))):
                ellipse(ctx, bx, byy, r, r); fl(ctx, (1, 1, 1), 6)
            cloud(ctx, -150, -40, 1.25)
            oven(ctx, 0, -20, 0.62, il)
            ctx.restore()
        if il < 22:
            label(ctx, "\"DID I TURN OFF", 540, 1450, 90, (1, 1, 1), -0.03, pop(il, 2, 6))
            label(ctx, "THE OVEN?!\"", 540, 1560, 110, hx('ff8a1f'), 0.03, pop(il, 6, 10))
        else:
            label(ctx, "*SCREEECH!*", 540, 1500, 130, (1, 1, 1), -0.05, pop(il, 22, 26))
    else:
        il = lf - 96
        # Mom flops back in: "it was off."
        pd = dict(DRIVE); pd.update(eye='glare', mouth='flat', head=-4)
        back = eout(pop(il, 0, 10))
        ctx.save(); cam(ctx, 540, 1040, 1.1, 0, shake_at(il, [8], 10, 22), f)
        car_front(ctx, il, 0, [('back', BOY, P(eye='normal', mouth='flat'), 540, 860, 75, 1), ('front', DAD, P(**pd), 330, 900, 110, 1),
                               ('front', MOM, P(eye='happy', mouth='smile', head=6), 750, lerp(1300, 905, back), 105, -1)], f, bounce=False)
        ctx.restore()
        label(ctx, "*SLAM*", 860, 1200, 80, (1, 1, 1), 0.08, pop(il, 8, 12))
        label(ctx, "\"IT WAS OFF.\"", 540, 1480, 110, (1, 1, 1), -0.03, pop(il, 12, 16))
    card(ctx, 'p3', f, 234, 366)


def s4(ctx, f):
    lf = f - 370
    ECU = 52
    if lf < ECU:
        off = 26 * lf
        pd = dict(DRIVE); pd.update(eye='normal' if lf < 16 else 'shock', mouth='smile' if lf < 16 else 'open', head=-4)
        lean = eout(pop(lf, 8, 16))
        pb = P(eye='closed' if lf > 18 else 'normal', mouth='wavy', head=0, rsh=-30, lsh=30)
        ctx.save(); cam(ctx, 540, 1040, 1.1 + 0.1 * eout(pop(lf, 8, ECU)), 0, shake_at(lf, [16], 8, 14), f, sy=H / 2)
        car_front(ctx, lf, off, [('front', DAD, P(**pd), 330, 900, 110, 1), ('front', MOM, P(eye='normal', mouth='flat', head=6), 750, 905, 105, -1),
                                 ('lean', BOY, pb, 540, lerp(860, 900, lean), lerp(75, 115, lean), 1)], f)
        ctx.restore()
        if lf >= 16:
            label(ctx, "\"I NEED THE BATHROOM\"", 540, 1520, 96, hx('ffe14d'), -0.03, pop(lf, 16, 20))
    else:
        il = lf - ECU
        tw = (il // 3) % 2 if il > 10 else 0
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.18 * eout(pop(il, 0, 78)), 0, 4 + shake_at(il, [10, 30, 50], 6, 12), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff6b5a')); ctx.fill()
        rays(ctx, 540, 960, 300, 1500, il * 0.03, col=hx('ff3b30')[:3], a=0.6, n=18)
        face(ctx, DAD, P(eye='glare', mouth='flat' if tw == 0 else 'wavy', head=0), 540 + (6 if tw else -6), 980, 380, 0.0)
        for k, sx in enumerate((150, 930)):
            for j in range(3):
                u = ((il + j * 9 + k * 4) % 27) / 27
                puff(ctx, sx, 900 - 380 * u, u, 1.2)
        ctx.restore()
        label(ctx, "WE LEFT 10 SECONDS AGO", 540, 1520, 76, (1, 1, 1), -0.03, pop(il, 4, 8))
    card(ctx, 'p4', f, 374, 496)


def glare_panel(ctx, f, x0, x1, ch, p, fp, bg, sweat_=False, il=0):
    ctx.save()
    ctx.rectangle(x0, 0, x1 - x0, H); ctx.clip()
    ctx.rectangle(x0, 0, x1 - x0, H); setc(ctx, bg); ctx.fill()
    cx = (x0 + x1) / 2
    face(ctx, ch, p, cx, 980, 200, 0, fp)
    if sweat_:
        sweat(ctx, cx + 150, 860 + (il % 20) * 5, 1.4)
        sweat(ctx, cx - 150, 900 + ((il + 10) % 20) * 5, 1.2)
    ctx.restore()
    ctx.move_to(x1, 0); ctx.line_to(x1, H); ink(ctx, 14); ctx.stroke()


def s5(ctx, f):
    lf = f - 500
    if lf < 72:
        reveal = lf >= 36
        pd = dict(DRIVE); pd.update(eye='shock' if reveal else 'smug', mouth='scream' if reveal else 'smile', head=-4)
        pm = P(eye='shock' if reveal else 'normal', mouth='open' if reveal else 'flat', head=10, rsh=-120, rel=-40)
        ctx.save(); cam(ctx, 600, 1000, 1.08 + 0.12 * eout(pop(lf, 36, 48)), 0, shake_at(lf, [36], 12, 24), f)
        car_front(ctx, lf, 0, [('back', BOY, P(eye='shock' if reveal else 'normal', mouth='open' if reveal else 'flat'), 540, 860, 75, 1),
                               ('front', DAD, P(**pd), 330, 900, 110, 1), ('front', MOM, pm, 750, 905, 105, -1)], f, bounce=False)
        ctx.restore()
        invite(ctx, 760, 1180, 1.45, -0.12 + 0.03 * math.sin(lf * 0.4))
        if not reveal:
            label(ctx, "\"THE PARTY IS ON...\"", 540, 1520, 96, (1, 1, 1), -0.03, pop(lf, 4, 8))
        else:
            label(ctx, "\"...TOMORROW.\"", 540, 1520, 130, RED, 0.04, pop(lf, 36, 40))
        card(ctx, 'p5', f, 504, 616)
    elif lf < 120:
        il = lf - 72
        # triple split screen: Mom + kid glare, Dad sweats
        sl = eout(pop(il, 0, 8))
        ctx.save(); cam(ctx, 540, 960, 1.0, 0, shake_at(il, [0], 10, 16), f)
        glare_panel(ctx, f, -10, 360, MOM, P(eye='glare', mouth='flat', head=-4), 1, hx('c8b6ff'))
        glare_panel(ctx, f, 360, 720, BOY, P(eye='glare', mouth='flat', head=4), -1, hx('b6f0a0'))
        glare_panel(ctx, f, 720, 1100, DAD, P(eye='shock', mouth='wavy', head=-8 + 4 * math.sin(il * 0.6)), -1, hx('ffe08a'), True, il)
        ctx.restore()
        label(ctx, "*CRICKETS*", 540, 1500, 120, (1, 1, 1), -0.04, pop(il, 6, 10))
        card(ctx, 'p5', f, 504, 616)
    else:
        il = lf - 120
        label_ = True
        opening_face(ctx, f, il, label_)
        card(ctx, 'p1', f, 620)


SHOTS = [(0, s1), (110, s2), (230, s3), (370, s4), (500, s5)]
CUTS = (56, 110, 170, 230, 274, 326, 370, 422, 500, 572, 620)


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
                              "-i", "out/leave_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
