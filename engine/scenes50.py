"""'Who Needs Instructions?' - original, general-audience comedy short, 22s.
Hook: ECU Dad, smug grin, twirling the tiny hex key: "INSTRUCTIONS? WHO NEEDS 'EM!"
Insert: he tosses the instruction booklet over his shoulder -> it lands in the bin: *SWISH*
Beat 1: overhead - 347 pieces explode across the floor around him. "Easy."
 ECU: Screw A or Screw B? eyes darting -> hammers a screw in: "Close ENOUGH."
Beat 2: the shelf is "done" (crooked) + 9 spare screws -> creak... CRASH, a plank bonks his head: "...the floor is UNEVEN."
Beat 3: hour 5 - he rebuilt it AROUND HIMSELF. Mom with coffee: "Where's the way OUT?" / "...pass me the instructions?"
Twist: the kid reads step 1, whirlwind builds a perfect shelf in 10 seconds. Dad: "I LOOSENED it for you."
 Ding-dong: a giant BUNK BED box arrives -> Dad's opening face (loop)."""
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
DAD = doodle.DAD
MOM = doodle.MOM_G
N = 660
FLOOR = 1460
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
WOOD = hx('e7b778')
WOOD_D = hx('c48a4a')
LY = 1400

CAPS = {
    'p1': [[("WHEN DAD BUILDS", OUT)], [("THE NEW BOOKSHELF", RED)]],
    'p2': [[("HOUR 1:", OUT)], [("347 PIECES", BLUE)]],
    'p3': [[("HOUR 3:", OUT)], [("IT'S... DONE?", ORANGE)]],
    'p4': [[("HOUR 5...", PURPLE)]],
    'p5': [[("PLOT TWIST:", OUT)], [("THE KID READS PAGE 1", GREEN)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def plank(ctx, x, y, w, h, a=0.0, col=WOOD, holes=True):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    rect_r(ctx, -w / 2, -h / 2, w, h, min(w, h) * 0.15); fl(ctx, col, 6)
    if holes and w > 3 * h:
        for k in (-1, 1):
            ellipse(ctx, k * (w / 2 - h * 0.6), 0, h * 0.13, h * 0.13); setc(ctx, dark(col, 0.6)); ctx.fill()
    ctx.restore()


def screw(ctx, x, y, s=1.0, a=0.0, bent=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(-10, 0); ctx.line_to(10, 0); ctx.line_to(6, 70 * (1 - 0.4 * bent)); ctx.line_to(0, 90 * (1 - 0.4 * bent)); ctx.line_to(-6, 70 * (1 - 0.4 * bent)); ctx.close_path()
    if bent:
        ctx.new_path(); ctx.move_to(-8, 0); ctx.curve_to(-8, 40, 30 * bent, 50, 60 * bent, 40); ctx.line_to(60 * bent, 26); ctx.curve_to(20 * bent, 34, 8, 30, 8, 0); ctx.close_path()
    fl(ctx, hx('c8ccd8'), 4)
    for k in range(1, 4):
        if not bent:
            ctx.move_to(-8, k * 16); ctx.line_to(8, k * 16 + 6)
    ink(ctx, 3); ctx.stroke()
    rect_r(ctx, -22, -14, 44, 18, 8); fl(ctx, hx('dfe3ec'), 4)
    ctx.move_to(-10, -5); ctx.line_to(10, -5); ink(ctx, 3); ctx.stroke()
    ctx.restore()


def hexkey(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(0, 0); ctx.line_to(0, -120); ctx.line_to(46, -120)
    setc(ctx, OUT); ctx.set_line_width(24); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
    setc(ctx, hx('9aa4b8')); ctx.set_line_width(12); ctx.stroke()
    ctx.restore()


def booklet(ctx, x, y, a, s=1.0, opened=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    w = 120 + 120 * opened
    rect_r(ctx, -w / 2, -80, w, 160, 6); fl(ctx, (1, 1, 1), 5)
    if opened:
        ctx.move_to(0, -80); ctx.line_to(0, 80); ink(ctx, 4); ctx.stroke()
        text(ctx, "1", -w / 4, -36, 40, OUT, outline=(1, 1, 1), ow=2, shadow=False)
        # tiny happy stick figure + shelf
        ellipse(ctx, -w / 4 - 22, 0, 9, 9); ink(ctx, 3); ctx.stroke()
        ctx.move_to(-w / 4 - 22, 9); ctx.line_to(-w / 4 - 22, 40); ctx.stroke()
        ctx.rectangle(w / 4 - 30, -40, 50, 90); ctx.stroke()
        ctx.move_to(w / 4 - 30, 0); ctx.line_to(w / 4 + 20, 0); ctx.stroke()
    else:
        ctx.rectangle(-40, -50, 80, 60); ink(ctx, 4); ctx.stroke()
        ctx.move_to(-40, -20); ctx.line_to(40, -20); ctx.stroke()
        for k in range(3):
            ctx.move_to(-44, 30 + k * 14); ctx.line_to(44 - k * 20, 30 + k * 14)
        ink(ctx, 3); ctx.stroke()
    ctx.restore()


def hammer(ctx, x, y, a, s=1.0):
    """pivot (hand) at x,y; rotates head around it"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -14, -230, 28, 250, 12); fl(ctx, hx('c96a2a'), 6)
    rect_r(ctx, -80, -280, 160, 64, 12); fl(ctx, hx('6a7486'), 7)
    ctx.restore()


def bin_(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    poly(ctx, [(-90, -220), (90, -220), (70, 0), (-70, 0)]); fl(ctx, hx('5fa8ff'), 7)
    for k in (-1, 0, 1):
        ctx.move_to(k * 45, -190); ctx.line_to(k * 36, -24)
    ink(ctx, 4); ctx.stroke()
    rect_r(ctx, -100, -236, 200, 28, 10); fl(ctx, hx('3d7bff'), 6)
    ctx.restore()


def cardboard(ctx, x, y, w, h, flaps=0.0, txt=None, txt2=None):
    ctx.rectangle(x - w / 2, y - h, w, h); fl(ctx, hx('d6a25e'), 8)
    ctx.move_to(x - w / 2, y - h + 40); ctx.line_to(x + w / 2, y - h + 40); setc(ctx, hx('b9874a')); ctx.set_line_width(10); ctx.stroke()
    if flaps:
        for k in (-1, 1):
            poly(ctx, [(x + k * w / 2, y - h), (x + k * (w / 2 + 70 * flaps), y - h - 90 * flaps), (x + k * (w / 2 - 60), y - h - 110 * flaps), (x, y - h)])
            fl(ctx, hx('e0b06e'), 6)
    if txt:
        text(ctx, txt, x, y - h * 0.58, w * 0.13, OUT, outline=hx('d6a25e'), ow=2, shadow=False)
    if txt2:
        text(ctx, txt2, x, y - h * 0.28, w * 0.15, RED, ow=6, shadow=False)


def shelf(ctx, x, base, w, h, lean=0.0, crooked=0.0, books=False, back=True, sq=1.0, ys=(0.25, 0.5, 0.75)):
    """bookshelf with bottom-left at (x, base). lean shears the top sideways; crooked tilts the shelves"""
    ctx.save(); ctx.translate(x, base)
    ctx.transform(cairo.Matrix(1, 0, -lean, sq, 0, 0))
    t = 30
    if back:
        ctx.rectangle(0, -h, w, h); setc(ctx, hx('caa070')); ctx.fill()
    rnd = random.Random(4)
    for i, fy in enumerate(ys):
        yy = -h * fy
        tilt = crooked * (0.18 if i % 2 == 0 else -0.14)
        if books:
            bx = t + 10
            while bx < w - t - 40:
                bw = rnd.uniform(28, 46); bh = rnd.uniform(0.15, 0.2) * h
                ctx.rectangle(bx, yy - bh, bw, bh); fl(ctx, rnd.choice((RED, BLUE, GREEN, ORANGE, PURPLE, PINK)), 4)
                bx += bw + 4
        if not (crooked and i == 1):
            ctx.save(); ctx.translate(w / 2, yy); ctx.rotate(tilt)
            ctx.rectangle(-w / 2 + t / 2, -t / 2, w - t, t); fl(ctx, WOOD, 6)
            ctx.restore()
        else:
            # a shelf hanging off by one end
            ctx.save(); ctx.translate(t, yy - 40); ctx.rotate(1.05)
            ctx.rectangle(0, -t / 2, w * 0.7, t); fl(ctx, WOOD, 6)
            ctx.restore()
    ctx.rectangle(0, -h, t, h); fl(ctx, WOOD_D, 7)
    ctx.rectangle(w - t, -h, t, h); fl(ctx, WOOD_D, 7)
    ctx.rectangle(-10, -h - t, w + 20, t); fl(ctx, WOOD, 7)
    ctx.rectangle(0, -t, w, t); fl(ctx, WOOD, 7)
    ctx.restore()


def room(ctx, wall=hx('7fd3c8')):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, wall); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 110, -3000, 6, 7000); setc(ctx, dark(wall, 0.93)); ctx.fill()
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('c98a52')); ctx.fill()
    for i in range(-30, 40):
        ctx.move_to(i * 160, FLOOR); ctx.line_to(i * 160 - 120, FLOOR + 600)
    setc(ctx, hx('b07640')); ctx.set_line_width(5); ctx.stroke()
    ctx.rectangle(-3000, FLOOR - 30, 7000, 30); fl(ctx, (1, 1, 1), 6)
    # picture frame
    rect_r(ctx, 640, 560, 220, 170, 8); fl(ctx, hx('ffd23f'), 8)
    poly(ctx, [(670, 700), (730, 610), (790, 700)]); fl(ctx, GREEN, 5)
    ellipse(ctx, 815, 610, 22, 22); fl(ctx, ORANGE, 4)


def pupils(ctx, cx, cy, Rt, look, f_=1):
    """over-paint 'shock' eyes with pupils shifted left/right by look (-1..1)"""
    for ex, ey, rx in eye_pos(cx, cy, Rt, f_):
        ry = 0.19 * Rt
        ellipse(ctx, ex, ey, rx * 0.86, ry * 0.86); setc(ctx, (1, 1, 1)); ctx.fill()
        ellipse(ctx, ex + look * rx * 0.5, ey + ry * 0.1, rx * 0.36, ry * 0.36); setc(ctx, INK); ctx.fill()


def sweat(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, -30); ctx.curve_to(18, 0, 18, 22, 0, 22); ctx.curve_to(-18, 22, -18, 0, 0, -30); ctx.close_path()
    fl(ctx, hx('8fd8ff'), 4); ctx.restore()


# ------------------------------------------------------------------ opening
def opening_face(ctx, f, lf, lab=True):
    """ECU: Dad, smug manic grin, hex key twirling"""
    sh = shake_at(lf, [0], 10, 18)
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eout(pop(lf, 0, 40)), 0, sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb52e')); ctx.fill()
    rays(ctx, 540, 880, 240, 1700, lf * 0.04, col=(1, 0.97, 0.6), a=0.4, n=18)
    rnd = random.Random(2)
    for k in range(7):   # floating parts
        a = rnd.uniform(0, 6.28) + lf * 0.03
        px, py = 540 + math.cos(a) * 430, 900 + math.sin(a) * 430
        if k % 2:
            screw(ctx, px, py, 0.9, a)
        else:
            plank(ctx, px, py, 160, 40, a * 1.3)
    cx, cy, R = 540, 880, 300
    face(ctx, DAD, P(eye='smug', mouth='grin', head=0), cx, cy, R, 0.04 * math.sin(lf * 0.5))
    # fist + spinning hex key, right
    hexkey(ctx, 870, 1110, lf * 0.5, 1.1)
    ellipse(ctx, 870, 1120, 70, 60); fl(ctx, DAD['skin'], 7)
    sparkle(ctx, 300, 640, 30 + 10 * math.sin(lf * 0.4)); sparkle(ctx, 800, 620, 24 + 8 * math.cos(lf * 0.4))
    ctx.restore()
    if lab:
        label2(ctx, "\"INSTRUCTIONS?", "WHO NEEDS 'EM!\"", (1, 1, 1), 1.0 if f < 60 else pop(lf, 0, 3), 100, col2=YEL)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 60:
        opening_face(ctx, f, f)
    else:
        lf = f - 60
        # wide: Dad tosses the booklet over his shoulder into the bin
        ctx.save(); cam(ctx, 560, 1150, 1.18, 0, shake_at(lf, [34], 8, 12), f)
        room(ctx)
        cardboard(ctx, 560, FLOOR, 300, 220, 1.0, "BOOKSHELF")
        for k in range(3):
            plank(ctx, 500 + k * 50, FLOOR - 240 - k * 10, 300, 44, -1.2 + k * 0.3)
        bin_(ctx, 920, FLOOR, 0.95)
        thr = lf >= 8
        p = P(torso=-6 if thr else 6, lhip=-10, lkn=0, rhip=10, rkn=0, lsh=-20, lel=-20,
              rsh=170 if thr else -60, rel=-10 if thr else -60, eye='smug', mouth='grin', head=-8)
        b = draw(ctx, 320, FLOOR - 186 * 1.25, 1.25, 1, DAD, p)
        if not thr:
            booklet(ctx, b['front'][0], b['front'][1] - 40, 0.2, 0.9)
        else:
            u = clamp((lf - 8) / 26)
            x0, y0 = b['front']; x1, y1 = 920, FLOOR - 230
            bx_ = lerp(x0, x1, u); by_ = lerp(y0, y1, u) - 520 * math.sin(math.pi * u)
            if u < 1:
                booklet(ctx, bx_, by_, u * 12, 0.9)
                for k in range(3):
                    uu = max(0, u - 0.04 * (k + 1))
                    ellipse(ctx, lerp(x0, x1, uu), lerp(y0, y1, uu) - 520 * math.sin(math.pi * uu), 8, 8); setc(ctx, (1, 1, 1, 0.6)); ctx.fill()
            else:
                puff(ctx, 920, FLOOR - 240, pop(lf, 34, 46), 0.9)
        ctx.restore()
        if 34 <= lf < 50:
            label(ctx, "*SWISH!*", 820, 980, 100, YEL, 0.06, pop(lf, 34, 37))
        if lf >= 36:
            label2(ctx, "\"Nothing", "but NET.\"", (1, 1, 1), pop(lf, 36, 40), 104, col2=YEL)
    card(ctx, 'p1', f, -6, 112)


def s2(ctx, f):
    lf = f - 112
    if lf < 58:
        # overhead: 347 pieces explode across the floor, Dad in the middle, camera spinning
        ctx.save(); cam(ctx, 540, 960, 1.15 - 0.15 * eout(pop(lf, 0, 58)), 14 * eout(pop(lf, 0, 58)), shake_at(lf, [2], 10, 18), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('c98a52')); ctx.fill()
        for i in range(-10, 20):
            ctx.rectangle(-500, i * 130, 2200, 6); setc(ctx, hx('b07640')); ctx.fill()
        rnd = random.Random(11)
        sp = eout(pop(lf, 0, 14))
        for k in range(60):
            a = rnd.uniform(0, 6.28); d = rnd.uniform(260, 820) * sp
            x, y = 540 + math.cos(a) * d, 950 + math.sin(a) * d * 1.1
            r_ = rnd.uniform(0, 6.28)
            kind = k % 4
            if kind == 0:
                plank(ctx, x, y, rnd.uniform(200, 340), 50, r_)
            elif kind == 1:
                plank(ctx, x, y, 120, 120, r_, hx('f2d29a'), False)
            elif kind == 2:
                screw(ctx, x, y, 0.8, r_)
            else:
                ctx.save(); ctx.translate(x, y); ctx.rotate(r_); rect_r(ctx, -12, -40, 24, 80, 10); fl(ctx, hx('f2d29a'), 4); ctx.restore()
        face(ctx, DAD, P(eye='shock', mouth='open', head=0), 540, 900, 190, 0.0)
        ctx.restore()
        if lf >= 8:
            label(ctx, "\"347 pieces?\"", 540, 1310, 96, (1, 1, 1), -0.03, pop(lf, 8, 12))
        if lf >= 26:
            label(ctx, "\"EASY.\"", 540, 1440, 130, YEL, 0.03, pop(lf, 26, 30))
    elif lf < 100:
        il = lf - 58
        # ECU: Screw A or Screw B? eyes darting
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eout(pop(il, 0, 42)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8fc0')); ctx.fill()
        rays(ctx, 540, 860, 200, 1600, il * 0.03, col=(1, 1, 1), a=0.25, n=16)
        face(ctx, DAD, P(eye='shock', mouth='wavy', head=0), 540, 840, 260, 0.0)
        look = 1.0 if (il // 8) % 2 == 0 else -1.0
        pupils(ctx, 540, 840, 260, look)
        sweat(ctx, 330, 700 + (il * 3) % 60, 1.2)
        for k, (x, tag) in enumerate(((230, "A"), (850, "B"))):
            ctx.save(); ctx.translate(x, 1130); ctx.rotate(-0.15 if k == 0 else 0.15)
            screw(ctx, 0, -60, 1.7)
            ellipse(ctx, 0, 60, 70, 56); fl(ctx, DAD['skin'], 6)
            ctx.restore()
            label(ctx, tag, x, 980, 90, YEL if (look < 0) == (k == 0) else (1, 1, 1), 0, 1.0)
        ctx.restore()
        label2(ctx, "\"Screw A...", "or Screw B?\"", (1, 1, 1), pop(il, 2, 6), 100, col2=YEL)
    else:
        il = lf - 100
        # hammering a screw: BONK BONK BONK
        hits = [8, 18, 28]
        ctx.save(); cam(ctx, 540, 1000, 1.05, 0, shake_at(il, hits, 6, 16), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('1f8bff')); ctx.fill()
        rays(ctx, 540, 1000, 160, 1500, -il * 0.03, col=(1, 1, 1), a=0.18, n=14)
        plank(ctx, 540, 1180, 900, 140, 0.0)
        n_hit = sum(1 for h in hits if il >= h)
        screw(ctx, 540, 1100 + 22 * n_hit, 1.4, 0, bent=1.0 if n_hit >= 3 else 0.0)
        # hammer swing: up -> down at each hit
        ph = min((il - h for h in hits if il >= h), default=99)
        nxt = min((h - il for h in hits if h > il), default=99)
        if ph < 3:
            a = -0.05
        elif nxt <= 4:
            a = -1.1 + 1.05 * (1 - nxt / 4)
        else:
            a = -1.1
        hammer(ctx, 860, 1090, -a - 0.5, 1.3)
        ellipse(ctx, 860, 1090, 64, 56); fl(ctx, DAD['skin'], 6)
        if ph < 5:
            for k in range(6):
                aa = k * math.pi / 3
                ctx.move_to(540 + math.cos(aa) * 70, 1070 + math.sin(aa) * 50); ctx.line_to(540 + math.cos(aa) * 130, 1070 + math.sin(aa) * 95)
            ink(ctx, 8); ctx.stroke()
        ctx.restore()
        if 0 < ph < 8:
            label(ctx, "*BONK!*", 300 + 120 * (n_hit % 2), 720, 100, YEL, -0.08 + 0.16 * (n_hit % 2), pop(ph, 0, 3))
        if il >= 30:
            label2(ctx, "\"Close", "ENOUGH.\"", (1, 1, 1), pop(il, 30, 34), 112, col2=YEL)
    card(ctx, 'p2', f, 114, 252)


def s3(ctx, f):
    lf = f - 252
    if lf < 108:
        # Dad proud next to his crooked shelf + spare screws -> it creaks and collapses
        col_u = eout(pop(lf, 74, 90))
        ctx.save(); cam(ctx, 580, 1120, 1.1 + 0.05 * eout(pop(lf, 0, 70)), 0, shake_at(lf, [90], 14, 30), f)
        room(ctx, hx('ffd9a8'))
        sx, sw, sh_ = 560, 380, 760
        if lf < 90:
            wob = 0.03 * math.sin(lf * 0.5) if lf >= 56 else 0.0
            shelf(ctx, sx, FLOOR, sw, sh_, lean=0.16 + wob + 1.0 * col_u, crooked=1.0, sq=1 - 0.8 * col_u)
        else:
            for k in range(5):
                plank(ctx, sx + 200 + (k - 2) * 40, FLOOR - 25 - k * 34, 520 - k * 30, 34, 0.05 * (k - 2))
            puff(ctx, sx + 100, FLOOR - 80, pop(lf, 90, 104), 1.4); puff(ctx, sx + 340, FLOOR - 60, pop(lf, 91, 106), 1.2)
        happy = lf < 74
        p = P(torso=-4 if happy else 6, lhip=-10, lkn=0, rhip=10, rkn=0, lsh=20, lel=-10, rsh=-80, rel=-40,
              eye='happy' if happy else 'shock', mouth='grin' if happy else 'scream', head=-6)
        b = draw(ctx, 300, FLOOR - 186 * 1.3, 1.3, 1, DAD, p)
        if happy:
            hx_, hy_ = b['head'][0] + b['R'] * 1.9, b['head'][1] + b['R'] * 1.5
            ellipse(ctx, hx_, hy_, 46, 30); fl(ctx, DAD['skin'], 6)
            hy_ += 40
            for k in range(9):
                screw(ctx, hx_ - 50 + (k % 3) * 34, hy_ - 70 - (k // 3) * 24, 0.5, -0.6 + k * 0.15)
            if lf >= 20:
                sparkle(ctx, hx_ + 60, hy_ - 120, 30)
        ctx.restore()
        if lf < 40:
            label2(ctx, "\"DONE!", "Like a PRO.\"", (1, 1, 1), pop(lf, 2, 6), 104, col2=YEL)
        elif lf < 62:
            label2(ctx, "\"...and 9", "SPARE screws!\"", (1, 1, 1), pop(lf, 40, 44), 104, col2=YEL)
        elif lf < 90:
            label1(ctx, "*CRRREEEAK...*", (1, 1, 1), pop(lf, 62, 66), 110, y=1430)
        else:
            label1(ctx, "*CRASH!!*", YEL, pop(lf, 90, 93), 160, 0.04, y=1430)
    else:
        il = lf - 108
        # ECU: dusty Dad, a plank drops on his head
        DUST = dict(DAD, skin=hx('cfb8a8'), hair=hx('8a8090'))
        ctx.save(); cam(ctx, 540, 960, 1.0, 0, shake_at(il, [6], 8, 18), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('8a8090')); ctx.fill()
        for k in range(14):
            rnd = random.Random(k)
            ellipse(ctx, rnd.uniform(0, 1080), (rnd.uniform(300, 1600) + il * 2) % 1600 + 200, 8, 8); setc(ctx, (1, 1, 1, 0.5)); ctx.fill()
        face(ctx, DUST, P(eye='closed' if il >= 6 else 'shock', mouth='wavy', head=0), 540, 900, 260, 0.03 * math.sin(il * 0.4))
        py = lerp(200, 560, ein(pop(il, 0, 6)))
        plank(ctx, 540, py, 520, 60, 0.08 if il >= 6 else -0.2)
        if il >= 6:
            zigs(ctx, 540, 600, 210, il, YEL, 5)
        ctx.restore()
        if il < 6:
            pass
        else:
            label2(ctx, "\"...the floor is", "UNEVEN.\"", (1, 1, 1), pop(il, 8, 12), 104, col2=YEL)
    card(ctx, 'p3', f, 254, 340)


def s4(ctx, f):
    lf = f - 400
    if lf < 52:
        # wide: Dad has built the shelf AROUND himself; Mom with coffee
        ctx.save(); cam(ctx, 570, 1130, 1.18 + 0.06 * eout(pop(lf, 0, 52)), 0, 0, f)
        room(ctx, hx('b9a8ff'))
        p = P(torso=0, lhip=-6, lkn=0, rhip=6, rkn=0, lsh=20, lel=-30, rsh=-90, rel=0, eye='normal', mouth='flat', head=0)
        b = draw(ctx, 380, FLOOR - 186 * 1.3, 1.3, 1, DAD, p)
        hy = b['head'][1]; R_ = b['R']
        # shelf frame around him (no back): his face peeks between two shelves
        x0, w = 200, 360; top = hy - R_ * 1.6
        h = FLOOR - top
        shelf(ctx, x0, FLOOR, w, h, back=False, ys=((FLOOR - (hy + R_ * 1.25)) / h, (FLOOR - (hy + R_ * 1.25)) / h * 0.45))
        sweat(ctx, b['head'][0] - R_ * 1.0, hy - R_ * 0.4, 1.0)
        pm = P(torso=0, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=-30, lel=-120, rsh=20, rel=-30, eye='normal', mouth='flat', head=-6)
        bm = draw(ctx, 800, FLOOR - 186 * 1.3, 1.3, -1, MOM, pm)
        mx, my = bm['front']
        rect_r(ctx, mx - 34, my - 60, 68, 76, 10); fl(ctx, (1, 1, 1), 5)
        for k in range(2):
            t = ((lf + k * 12) % 24) / 24
            ctx.move_to(mx - 10 + k * 20, my - 70 - 60 * t); ctx.rel_curve_to(12, -14, -12, -26, 0, -40)
            setc(ctx, (1, 1, 1, 0.8 * (1 - t))); ctx.set_line_width(5); ctx.stroke()
        ctx.restore()
        label2(ctx, "\"Honey...", "where's the way OUT?\"", (1, 1, 1), pop(lf, 4, 8), 92, col2=PINK)
    else:
        il = lf - 52
        # ECU: Dad's face through the shelf bars, push-in
        ctx.save(); cam(ctx, 540, 900, 1.0 + 0.1 * eout(pop(il, 0, 48)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('b9a8ff')); ctx.fill()
        face(ctx, DAD, P(eye='shock', mouth='wavy', head=0), 540, 880, 250, 0.0)
        pupils(ctx, 540, 880, 250, 0.8 * math.sin(il * 0.3))
        ctx.rectangle(80, 540, 920, 60); fl(ctx, WOOD, 8)
        ctx.rectangle(80, 1180, 920, 60); fl(ctx, WOOD, 8)
        ctx.rectangle(100, 300, 70, 1200); fl(ctx, WOOD_D, 8)
        ctx.rectangle(910, 300, 70, 1200); fl(ctx, WOOD_D, 8)
        sweat(ctx, 300, 760 + (il * 2) % 40, 1.1); sweat(ctx, 800, 720 + (il * 3) % 50, 0.9)
        ctx.restore()
        label2(ctx, "\"...can somebody pass", "the INSTRUCTIONS?\"", (1, 1, 1), pop(il, 2, 6), 88, col2=YEL)
    card(ctx, 'p4', f, 402, 500)


def s5(ctx, f):
    lf = f - 500
    if lf < 60:
        ctx.save(); cam(ctx, 540, 1110, 1.12, 0, shake_at(lf, [46], 10, 16), f)
        room(ctx, hx('9ff0b0'))
        if lf < 22:
            # kid with the open booklet
            p = P(torso=0, lhip=-6, lkn=0, rhip=6, rkn=0, lsh=-30, lel=-70, rsh=-30, rel=-70, eye='smug', mouth='smile', head=6)
            b = draw(ctx, 540, FLOOR - 186 * 1.5, 1.5, 1, BOY, p)
            booklet(ctx, 540, b['front'][1] + 30, 0.0, 1.3, 1.0)
        elif lf < 46:
            # whirlwind build
            il = lf - 22
            for k in range(7):
                yy = FLOOR - 60 - k * 110
                rw = 120 + k * 45
                ellipse(ctx, 540 + 30 * math.sin(il * 0.8 + k), yy, rw, 36); setc(ctx, (1, 1, 1, 0.55)); ctx.fill_preserve(); ink(ctx, 5); ctx.stroke()
            rnd = random.Random(9)
            for k in range(10):
                a = il * 0.7 + k * 0.63
                rr = rnd.uniform(200, 360)
                if k % 3 == 2:
                    screw(ctx, 540 + math.cos(a) * rr, 1000 + math.sin(a) * rr * 0.6 - k * 20, 0.8, a)
                else:
                    plank(ctx, 540 + math.cos(a) * rr, 1000 + math.sin(a) * rr * 0.6 - k * 20, 240, 40, a * 2)
            face(ctx, BOY, P(eye='happy', mouth='grin', head=0), 540 + 200 * math.sin(il * 1.3), 700, 90, 0.0)
        else:
            shelf(ctx, 380, FLOOR, 400, 820, books=True)
            p = P(torso=0, lhip=-10, lkn=0, rhip=10, rkn=0, lsh=-150, lel=-20, rsh=20, rel=-20, eye='happy', mouth='grin', head=0)
            draw(ctx, 260, FLOOR - 186 * 1.2, 1.2, 1, BOY, p)
            for k, (x, y) in enumerate(((420, 600), (760, 680), (600, 520))):
                sparkle(ctx, x, y, 40 * (0.6 + 0.4 * math.sin(lf * 0.5 + k)))
        ctx.restore()
        if lf < 22:
            label2(ctx, "\"Step 1:", "READ.\"", (1, 1, 1), pop(lf, 2, 6), 116, col2=YEL)
        elif lf < 46:
            label1(ctx, "*ZOOM ZOOM ZOOM*", YEL, pop(lf, 22, 25), 100, y=1430)
        else:
            label1(ctx, "*DING!* \"DONE!\"", YEL, pop(lf, 46, 49), 110, y=1430)
        card(ctx, 'p5', f, 502, 560)
    elif lf < 100:
        il = lf - 60
        # split: kid + perfect shelf (top) vs Dad stunned (bottom)
        ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
        ctx.rectangle(0, 0, W, 960); setc(ctx, hx('9ff0b0')); ctx.fill()
        rays(ctx, 540, 700, 150, 1300, il * 0.04, col=(1, 1, 1), a=0.35, n=16)
        shelf(ctx, 640, 960, 300, 540, books=True)
        face(ctx, BOY, P(eye='smug', mouth='smile', head=0), 330, 640, 150, 0.0)
        sparkle(ctx, 900, 380, 36)
        ctx.restore()
        ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
        ctx.rectangle(0, 960, W, 960); setc(ctx, hx('ff8a5c')); ctx.fill()
        face(ctx, DAD, P(eye='shock', mouth='scream', head=0), 540, 1150, 170, 0.0)
        ctx.restore()
        ctx.rectangle(0, 952, W, 16); setc(ctx, (1, 1, 1)); ctx.fill()
        if il >= 6:
            label2(ctx, "\"I... LOOSENED", "it for you.\"", (1, 1, 1), pop(il, 6, 10), 98, col2=YEL, y=1430)
    elif lf < 125:
        il = lf - 100
        # ding dong: a GIANT box slides in
        ctx.save(); cam(ctx, 560, 1100, 1.1, 0, shake_at(il, [12], 10, 20), f)
        room(ctx)
        bxx = lerp(1400, 700, eout(pop(il, 0, 12)))
        cardboard(ctx, bxx + 40, FLOOR, 520, 760, 0.0, "BUNK BED", "900 PCS")
        p = P(torso=-4, lhip=-10, lkn=0, rhip=10, rkn=0, lsh=-150, lel=-20, rsh=-150, rel=-20,
              eye='shock' if il < 14 else 'happy', mouth='open' if il < 14 else 'grin', head=-4)
        draw(ctx, 320, FLOOR - 186 * 1.2, 1.2, 1, DAD, p)
        ctx.restore()
        label1(ctx, "*DING-DONG!*", YEL, pop(il, 0, 3), 110, y=1430)
    else:
        il = lf - 125
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 625)


SHOTS = [(0, s1), (112, s2), (252, s3), (400, s4), (500, s5)]
CUTS = (60, 112, 170, 212, 252, 360, 400, 452, 500, 560, 600, 625)


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
                              "-i", "out/flatpack_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
