"""'We Have Food At Home' - original, general-audience comedy short, ~22s.
Kid begs for pizza. Mom: "We have food at home." The food at home = one egg, half a lemon and a tumbleweed.
Mom cooks it into a blob that burps and blinks. Then Dad walks in with pizza - Mom grabs it,
kid says "but we have food at home!"... Mom slides him the blob: "YOU have food at home." Kid begs again -> loop."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import cam, pop, sparkle, puff, label, shake_at
from scenes8 import sit
import scenes13
from scenes13 import card as _card13

BOY, MOM, DAD = doodle.BOY, doodle.MOM_G, doodle.DAD
N = 660
FLOOR = 1500
KB, KM, KD = 1.5, 1.7, 1.75
BHIP, MHIP, DHIP = FLOOR - 92 * KB, FLOOR - 92 * KM, FLOOR - 92 * KD
KIDX, MOMX = 330, 790
FX0, FX1, FY0 = 470, 860, 560      # fridge box

CAPS = {
    'p1': [[("CAN WE GET ", OUT), ("PIZZA", hx('ff8a1f')), ("?", OUT)]],
    'p2': [[("THE FOOD ", OUT), ("AT HOME", hx('1f8bff')), (":", OUT)]],
    'p3': [[("MOM'S ", OUT), ("SPECIAL", hx('2fbf5a'))]],
    'p4': [[("THEN DAD WALKS IN WITH", OUT)], [("PIZZA", hx('ff8a1f'))]],
    'p5': [[("MOM, ", OUT), ("NEVER LOSING", hx('ff3b8a')), (":", OUT)]],
}
scenes13.CAPS = CAPS
card = _card13


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


# ------------------------------------------------------------------ props
def egg(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 34, 44); fl(ctx, hx('fff6e6'), 5)
    ellipse(ctx, -10, -14, 7, 11); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.restore()


def lemon(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 44, math.pi, 2 * math.pi); ctx.close_path(); fl(ctx, hx('ffe14d'), 5)
    ctx.new_path(); ctx.arc(0, 0, 34, math.pi, 2 * math.pi); ctx.close_path(); setc(ctx, hx('fff7b0')); ctx.fill()
    for k in range(5):
        ang = math.pi + (k + 0.5) * math.pi / 5
        ctx.move_to(0, 0); ctx.line_to(math.cos(ang) * 32, math.sin(ang) * 32)
    setc(ctx, hx('ffd21f')); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def ketchup(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -30, -60, 60, 120, 18); fl(ctx, hx('ff3b3b'), 5)
    ctx.rectangle(-14, -82, 28, 24); fl(ctx, (1, 1, 1), 4)
    ctx.rectangle(-30, 40, 60, 0)
    ctx.restore()


def tumbleweed(ctx, x, y, r, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    setc(ctx, hx('b98a4e')); ctx.set_line_width(5)
    for k in range(9):
        ctx.new_path(); ctx.arc(math.cos(k * 1.7) * r * 0.25, math.sin(k * 1.3) * r * 0.25, r * (0.5 + 0.08 * (k % 4)), k, k + 4.2); ctx.stroke()
    ctx.new_path(); ctx.restore()


def pizza_slice(ctx, x, y, s=1.0, a=0.0, bite=False):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    pts = [(-55, -70), (55, -70), (0, 90)]
    if bite:
        ctx.new_path(); ctx.move_to(-55, -70); ctx.line_to(55, -70); ctx.line_to(14, 50)
        ctx.arc_negative(0, 70, 22, -0.3, math.pi + 0.3); ctx.close_path()
    else:
        poly(ctx, pts)
    fl(ctx, hx('ffcc3a'), 5)
    rect_r(ctx, -62, -88, 124, 30, 14); fl(ctx, hx('e0903a'), 5)
    for px, py in ((-20, -35), (22, -30), (2, 10)):
        ellipse(ctx, px, py, 13, 13); fl(ctx, hx('e0263a'), 3)
    ctx.restore()


def pizza_box(ctx, x, y, s=1.0, open_=0.0, glow=0.0, t=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if glow > 0:
        rays(ctx, 0, -40, 90, 330, t, a=0.55 * glow)
    if open_ > 0:
        # lid swung up behind
        h = 150 * open_
        poly(ctx, [(-150, -30), (150, -30), (130, -30 - h), (-130, -30 - h)]); fl(ctx, hx('f5e6c8'), 6)
        ellipse(ctx, 0, -30, 125, 22 * open_ + 4); fl(ctx, hx('ffcc3a'), 5)
        for px in (-70, -20, 40, 80):
            ellipse(ctx, px, -30 + (px % 3) * 3, 14, 6 * open_ + 2); fl(ctx, hx('e0263a'), 3)
    rect_r(ctx, -150, -30, 300, 60, 8); fl(ctx, hx('f5e6c8'), 6)
    ctx.move_to(-120, 0); ctx.line_to(120, 0); setc(ctx, hx('e0903a')); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def blob(ctx, x, y, s, f, eyes=0.0, droop=0.0, fork=True, burp=0.0):
    """the 'food at home': wobbling grey-green blob on a plate"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 20, 170, 34); fl(ctx, (1, 1, 1), 6)
    ellipse(ctx, 0, 20, 120, 20); setc(ctx, hx('e4e9f2')); ctx.fill()
    wob = 1 + 0.12 * burp
    ctx.new_path()
    for i in range(41):
        ang = math.pi + i * math.pi / 40
        r = 110 * wob + 8 * math.sin(ang * 5 + f * 0.25) + 5 * math.sin(ang * 9 - f * 0.4)
        px, py = math.cos(ang) * r * 1.05, math.sin(ang) * r * 0.8 + 14
        ctx.line_to(px, py)
    ctx.close_path(); fl(ctx, hx('9bb35a'), 6)
    for k, (bx, by) in enumerate(((-50, -20), (30, -50), (60, -10), (-10, -60))):
        r = 8 + 6 * ((f * 0.07 + k * 0.3) % 1)
        ellipse(ctx, bx, by, r, r); setc(ctx, hx('c7da86')); ctx.fill()
    ellipse(ctx, -40, -40, 22, 10, -0.4); setc(ctx, (1, 1, 1, 0.45)); ctx.fill()
    if eyes > 0:
        for ex in (-28, 28):
            ellipse(ctx, ex, -38, 16, 18 * eyes); fl(ctx, (1, 1, 1), 4)
            ellipse(ctx, ex + 3, -36, 6, 7 * eyes); setc(ctx, INK); ctx.fill()
    if fork:
        ctx.save(); ctx.translate(46, -40); ctx.rotate(0.25 + droop * 1.9)
        ctx.move_to(0, 0); ctx.curve_to(0, -60, 10 * droop, -100, 30 * droop, -150 + 40 * droop); ink(ctx, 16); ctx.stroke()
        ctx.move_to(0, 0); ctx.curve_to(0, -60, 10 * droop, -100, 30 * droop, -150 + 40 * droop); setc(ctx, hx('c8ccd8')); ctx.set_line_width(9); ctx.stroke()
        ctx.restore()
    for k in range(3):
        tt = ((f * 0.02 + k / 3) % 1)
        sx = -40 + k * 40 + math.sin(f * 0.1 + k) * 10
        ctx.new_path(); ctx.arc(sx, -110 - tt * 120, 12 + tt * 10, 0, 2 * math.pi); setc(ctx, (0.75, 0.85, 0.5, 0.55 * (1 - tt))); ctx.fill()
    ctx.restore()


def pan(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.rectangle(110, -12, 150, 22); fl(ctx, hx('3a3a4a'), 5)
    ctx.new_path(); ctx.move_to(-120, -20); ctx.line_to(120, -20); ctx.line_to(100, 30); ctx.line_to(-100, 30); ctx.close_path(); fl(ctx, hx('4a4a5e'), 6)
    ctx.restore()


# ------------------------------------------------------------------ sets
def kitchen(ctx, door=0.0):
    ctx.rectangle(-1500, -1500, 4200, 4200); setc(ctx, hx('a8ecd0')); ctx.fill()
    for i in range(-8, 16):
        ctx.rectangle(i * 150, -400, 60, FLOOR + 400); setc(ctx, (1, 1, 1, 0.16)); ctx.fill()
    # clock
    ellipse(ctx, 210, 640, 80, 80); fl(ctx, (1, 1, 1), 8)
    ctx.move_to(210, 640); ctx.line_to(210, 585); ctx.move_to(210, 640); ctx.line_to(250, 660); ink(ctx, 7); ctx.stroke()
    # fridge
    rect_r(ctx, FX0, FY0, FX1 - FX0, FLOOR - FY0, 30); fl(ctx, hx('f4f8ff'), 8)
    ctx.move_to(FX0, FY0 + 300); ctx.line_to(FX1, FY0 + 300); ink(ctx, 6); ctx.stroke()
    for yy, hh in ((FY0 + 120, 120), (FY0 + 400, 220)):
        rect_r(ctx, FX0 + 30, yy, 22, hh, 10); fl(ctx, hx('c8ccd8'), 5)
    # fridge magnets (original doodles: star, heart)
    poly(ctx, [(FX1 - 90 + 30 * math.cos(k * math.pi / 5 - math.pi / 2) * (1 if k % 2 == 0 else 0.45),
                FY0 + 120 + 30 * math.sin(k * math.pi / 5 - math.pi / 2) * (1 if k % 2 == 0 else 0.45)) for k in range(10)])
    fl(ctx, hx('ffcc1f'), 4)
    rect_r(ctx, FX1 - 200, FY0 + 460, 140, 170, 6); fl(ctx, (1, 1, 1), 4)
    ctx.move_to(FX1 - 180, FY0 + 600); ctx.line_to(FX1 - 150, FY0 + 520); ctx.line_to(FX1 - 120, FY0 + 580); ctx.line_to(FX1 - 90, FY0 + 500)
    setc(ctx, hx('1f8bff')); ctx.set_line_width(6); ctx.stroke()
    ellipse(ctx, FX1 - 130, FY0 + 450, 12, 12); fl(ctx, hx('ff3b5c'), 3)
    # front door on the far right
    rect_r(ctx, 900, 640, 330, 870, 10); fl(ctx, hx('8a5a34'), 8)
    if door > 0:
        ctx.rectangle(916, 656, 298, 850); setc(ctx, hx('ffe9a8')); ctx.fill()
        poly(ctx, [(916, 656), (916 + 298 * (1 - door * 0.85), 690), (916 + 298 * (1 - door * 0.85), 1470), (916, 1506)]); fl(ctx, hx('b97a44'), 6)
    else:
        ellipse(ctx, 950, 1100, 14, 14); fl(ctx, hx('ffcc1f'), 4)
    # floor
    ctx.rectangle(-1500, FLOOR, 4200, 900); setc(ctx, hx('f0c27a')); ctx.fill()
    for i in range(-10, 20):
        for j in range(0, 6):
            if (i + j) % 2 == 0:
                ctx.rectangle(i * 110, FLOOR + j * 110, 110, 110); setc(ctx, (1, 1, 1, 0.3)); ctx.fill()
    ctx.move_to(-1500, FLOOR); ctx.line_to(2700, FLOOR); ink(ctx, 8); ctx.stroke()


def counter(ctx):
    ctx.rectangle(-300, 1200, 760, 300); fl(ctx, hx('ff8a5c'), 7)
    rect_r(ctx, -320, 1170, 800, 44, 10); fl(ctx, hx('fff2de'), 7)
    for xx in (60, 300):
        rect_r(ctx, xx - 70, 1158, 140, 18, 6); setc(ctx, INK); ctx.fill()


def fridge_open(ctx, o, t):
    """open fridge interior + swung door; o 0..1"""
    if o <= 0:
        return
    ix0, iy0, ix1, iy1 = FX0 + 22, FY0 + 22, FX1 - 22, FLOOR - 30
    ctx.rectangle(ix0, iy0, ix1 - ix0, iy1 - iy0); setc(ctx, hx('eaf7ff')); ctx.fill()
    g = cairo.RadialGradient((ix0 + ix1) / 2, FY0 + 120, 20, (ix0 + ix1) / 2, FY0 + 300, 600)
    g.add_color_stop_rgba(0, 1, 1, 0.85, 0.9 * o); g.add_color_stop_rgba(1, 1, 1, 1, 0)
    ctx.rectangle(ix0, iy0, ix1 - ix0, iy1 - iy0); ctx.set_source(g); ctx.fill()
    for sy in (FY0 + 300, FY0 + 560, FY0 + 780):
        ctx.rectangle(ix0, sy, ix1 - ix0, 14); fl(ctx, hx('bfe6ff'), 4)
    ctx.rectangle(ix0, iy0, ix1 - ix0, iy1 - iy0); ink(ctx, 6); ctx.stroke()
    ellipse(ctx, (ix0 + ix1) / 2, FY0 + 60, 26, 14); setc(ctx, hx('fffbd0')); ctx.fill()
    # door swung to the right (perspective strip)
    w = 160 * o
    poly(ctx, [(FX1, FY0), (FX1 + w, FY0 - 40), (FX1 + w, FLOOR + 30), (FX1, FLOOR)]); fl(ctx, hx('dde6f5'), 7)


# ------------------------------------------------------------------ characters
def beg_pose(f):
    return P(lsh=-60, lel=-110, rsh=-35, rel=-125, eye='shock', mouth='open', head=5 + 3 * math.sin(f * 0.5), torso=-5)


def beg_kid(ctx, f, x=KIDX):
    h = draw_hip(ctx, x, BHIP, KB, 1, BOY, beg_pose(f))
    # puppy-eye shines
    for e in ('eyeL', 'eyeR'):
        ex, ey = h[e]
        ellipse(ctx, ex - 6, ey - 26, 10, 12); setc(ctx, (1, 1, 1)); ctx.fill()
        ellipse(ctx, ex + 8, ey - 6, 5, 6); setc(ctx, (1, 1, 1)); ctx.fill()
    return h


def beg_shot(ctx, f, lf):
    ctx.save(); cam(ctx, 380, 1040, 2.25, -4 + 2 * math.sin(lf * 0.2), 0, f)
    kitchen(ctx)
    h = beg_kid(ctx, f)
    for i in range(4):
        a = lf * 0.08 + i * math.pi / 2
        sparkle(ctx, h['head'][0] + math.cos(a) * 230, h['head'][1] + math.sin(a) * 210, 20 + 6 * math.sin(lf * 0.4 + i), hx('fff27a'))
    ctx.restore()


def s1(ctx, f):
    if f < 46:
        beg_shot(ctx, f, f)
        label(ctx, "PLEEEASE?", 540, 1460, 130, hx('ffe14d'), -0.04, 1)
    else:
        # whip pan to Mom: arms crossed
        lf = f - 46
        u = eout(pop(lf, 0, 8))
        cx = lerp(380, 800, u); z = lerp(2.25, 2.0, u)
        ctx.save(); cam(ctx, cx, 1000, z, lerp(-4, 3, u), shake_at(lf, [8], 10, 18), f)
        kitchen(ctx)
        draw_hip(ctx, KIDX, BHIP, KB, 1, BOY, beg_pose(f))
        draw_hip(ctx, MOMX, MHIP, KM, -1, MOM, P(lsh=-60, lel=-100, rsh=-60, rel=-100, eye='smug', mouth='flat', head=-3))
        ctx.restore()
        if u < 1:
            for k in range(8):
                ctx.rectangle(0, 300 + k * 170, W, 18); setc(ctx, (1, 1, 1, 0.35 * (1 - u))); ctx.fill()
        label(ctx, "WE HAVE", 540, 1330, 100, (1, 1, 1), 0.03, pop(lf, 8, 12))
        label(ctx, "FOOD AT HOME.", 540, 1450, 112, hx('ff3b5c'), -0.03, pop(lf, 14, 18))
    card(ctx, 'p1', f, -6, 100)


def s2(ctx, f):
    lf = f - 100
    if lf < 50:
        # mom flings the fridge open like a game-show reveal
        o = eout(pop(lf, 12, 22))
        ctx.save(); cam(ctx, 600, 1060, 1.0, 0, shake_at(lf, [14], 10, 14), f)
        kitchen(ctx)
        fridge_open(ctx, o, lf)
        if o > 0:
            rays(ctx, (FX0 + FX1) / 2, 1000, 200, 700, lf * 0.03, a=0.3 * o)
        draw_hip(ctx, 260, MHIP, KM, 1, MOM, P(rsh=150 if lf > 12 else 60, rel=-10 if lf > 12 else 90, lsh=-160 if lf > 12 else -20, lel=-20,
                                              eye='happy', mouth='grin', torso=-6 if lf > 12 else 4))
        ctx.restore()
        if lf >= 14:
            label(ctx, "TA-DAAA!", 540, 1450, 140, hx('ffe14d'), -0.04, pop(lf, 14, 18))
    else:
        # push into the fridge: the 'food'
        il = lf - 50
        z = kf(il, [(0, 1.15), (14, 1.5), (150, 1.62)], eout)
        cy = kf(il, [(0, 1100), (14, 1070)], eout)
        ctx.save(); cam(ctx, (FX0 + FX1) / 2, cy, z, 0, shake_at(il, [12, 30, 52, 76], 6, 6), f)
        kitchen(ctx)
        fridge_open(ctx, 1, il)
        mid = (FX0 + FX1) / 2
        egg(ctx, mid - 90, FY0 + 300 - 44, 1.0, 0.1)
        lemon(ctx, mid + 80, FY0 + 560, 1.1, 0)
        ketchup(ctx, mid - 95, FY0 + 780 - 62, 0.9, -0.5)
        if il >= 70:
            tw = eout(pop(il, 70, 110))
            tumbleweed(ctx, lerp(FX0 - 100, mid + 95, tw), FY0 + 780 - 44, 42, tw * 9)
        ctx.restore()
        txt = None
        if il >= 6: txt = ("1 EGG.", hx('ffffff'), 6)
        if il >= 26: txt = ("HALF A LEMON.", hx('ffe14d'), 26)
        if il >= 48: txt = ("SAD KETCHUP.", hx('ff3b5c'), 48)
        if il >= 76: txt = ("...A TUMBLEWEED?", hx('f0b46a'), 76)
        if txt:
            label(ctx, txt[0], 540, 1450, 92 if len(txt[0]) > 13 else 110, txt[1], 0.03 * (-1) ** (il // 22), pop(il, txt[2], txt[2] + 4))
    card(ctx, 'p2', f, 104, 250)


def s3(ctx, f):
    lf = f - 250
    if lf < 66:
        # mom at the counter tosses everything in the pan -> POOF
        ctx.save(); cam(ctx, 300, 1080, 1.15, -3, shake_at(lf, [44], 12, 20), f)
        kitchen(ctx)
        h = draw_hip(ctx, 420, MHIP, KM, -1, MOM, P(rsh=70 + 30 * math.sin(lf * 0.6), rel=60, lsh=-20, lel=-40, eye='happy', mouth='grin', torso=6))
        counter(ctx)
        pan(ctx, 180, 1145, 1.4)
        items = [(egg, 0), (lemon, 10), (ketchup, 20), (tumbleweed, 30)]
        for fn, st in items:
            t = pop(lf, st, st + 14)
            if 0 < t < 1:
                x = lerp(500, 180, t); y = lerp(950, 1120, t) - 300 * math.sin(math.pi * t)
                if fn is tumbleweed:
                    fn(ctx, x, y, 34, t * 8)
                else:
                    fn(ctx, x, y, 0.8, t * 6)
        if lf >= 44:
            for k in range(5):
                puff(ctx, 180 + (k - 2) * 70, 1060 - k % 2 * 60, pop(lf, 44, 66), 3.0)
        ctx.restore()
        if lf < 44:
            label(ctx, "A LITTLE OF THIS...", 540, 1450, 84, (1, 1, 1), 0.03, pop(lf, 2, 6))
        else:
            label(ctx, "POOF!", 540, 1450, 150, hx('ffe14d'), -0.05, pop(lf, 44, 48))
    else:
        # the dish: kid at the table, pokes it, it BURPS, then opens its eyes
        il = lf - 66
        z = kf(il, [(0, 1.25), (80, 1.5)], eout)
        burp = pop(il, 30, 34) * (1 - pop(il, 34, 44))
        ctx.save(); cam(ctx, 520, 1120, z, 0, shake_at(il, [30], 12, 18), f)
        kitchen(ctx)
        eye = 'normal' if il < 30 else 'shock'
        mo = 'flat' if il < 30 else 'scream'
        h = draw_hip(ctx, KIDX, FLOOR - 160, KB, 1, BOY, sit(rsh=70, rel=40 if il < 30 else -40, lsh=-20, lel=-30, eye=eye, mouth=mo,
                                                            torso=0 if il < 30 else -14))
        rect_r(ctx, 340, 1250, 760, 50, 12); fl(ctx, hx('ffffff'), 7)
        for lx in (380, 1040):
            ctx.rectangle(lx, 1300, 30, 200); fl(ctx, hx('8a5a34'), 6)
        blob(ctx, 680, 1220, 1.0, f, eyes=eout(pop(il, 56, 62)), droop=eout(pop(il, 40, 54)), burp=burp)
        ctx.restore()
        if il < 30:
            label(ctx, "*POKE*", 540, 1450, 110, (1, 1, 1), 0.03, pop(il, 12, 16))
        elif il < 56:
            label(ctx, "BLORP!", 540, 1450, 150, hx('9bdc4a'), -0.05, pop(il, 30, 34))
        else:
            label(ctx, "IT BLINKED.", 540, 1450, 120, hx('ffe14d'), 0.03, pop(il, 58, 62))
    card(ctx, 'p3', f, 254, 400)


def dad_with_pizza(ctx, f, x, ph=0.0, glow=1.0, t=0.0, open_=0.0):
    p = P(rsh=70, rel=70, lsh=60, lel=80, eye='happy', mouth='grin', torso=3 * math.sin(ph))
    if ph:
        s = math.sin(ph); p.update(lhip=20 * s, rhip=-20 * s, lkn=-20 * max(0, s), rkn=-20 * max(0, -s))
    h = draw_hip(ctx, x, DHIP - 6 * abs(math.sin(ph)), KD, -1, DAD, p)
    fx, fy = h['front']
    pizza_box(ctx, fx + 30, fy - 10, 0.9, open_, glow, t)
    return h


def s4(ctx, f):
    lf = f - 400
    if lf < 46:
        # doorbell -> door swings open -> Dad, glowing pizza, angel choir
        d = eout(pop(lf, 6, 14))
        ctx.save(); cam(ctx, 930, 1080, 1.2, 0, shake_at(lf, [0], 8, 10), f)
        kitchen(ctx, door=d)
        if lf >= 10:
            dad_with_pizza(ctx, f, lerp(1110, 1000, eout(pop(lf, 10, 30))), ph=lf * 0.4 if lf < 30 else 0, glow=pop(lf, 10, 20), t=lf * 0.03)
        ctx.restore()
        if lf < 12:
            label(ctx, "DING DONG!", 540, 1450, 130, (1, 1, 1), -0.04, pop(lf, 0, 4))
        else:
            label(ctx, "WHO WANTS PIZZA?", 540, 1450, 104, hx('ff8a1f'), 0.03, pop(lf, 18, 22))
    elif lf < 84:
        # Mom zips across the frame and grabs it
        il = lf - 46
        ctx.save(); cam(ctx, 780, 1080, 1.05, 0, shake_at(il, [10], 10, 20), f)
        kitchen(ctx, door=1)
        dad_with_pizza(ctx, f, 1000, glow=0.6, t=lf * 0.03, open_=eout(pop(il, 4, 10)))
        mx = lerp(-200, 720, eout(pop(il, 0, 10)))
        h = draw_hip(ctx, mx, MHIP, KM, 1, MOM, P(rsh=80, rel=0, lsh=-40, lel=-20, eye='happy' if il > 10 else 'shock', mouth='grin', torso=14))
        if il < 10:
            for k in range(6):
                ctx.move_to(mx - 200 - k * 30, 900 + k * 90); ctx.line_to(mx - 500 - k * 30, 900 + k * 90); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(10); ctx.stroke()
        else:
            fx, fy = h['front']
            pizza_slice(ctx, fx + 10, fy - 50, 1.0, 0.3)
        ctx.restore()
        label(ctx, "MINE!", 540, 1450, 150, hx('ff3b8a'), -0.04, pop(il, 10, 14))
    else:
        # kid points: reversal
        il = lf - 84
        ctx.save(); cam(ctx, 420, 1060, 1.9, -5, shake_at(il, [0], 8, 12), f)
        kitchen(ctx, door=1)
        draw_hip(ctx, KIDX, BHIP, KB, 1, BOY, P(rsh=110, rel=0, lsh=-30, lel=-40, eye='glare', mouth='open', torso=-6, head=4))
        ctx.restore()
        label(ctx, "BUT MOM...", 540, 1250, 90, (1, 1, 1), 0.03, pop(il, 2, 6))
        label(ctx, "WE HAVE FOOD", 540, 1360, 100, hx('ffe14d'), -0.03, pop(il, 10, 14))
        label(ctx, "AT HOME!", 540, 1470, 110, hx('ffe14d'), -0.03, pop(il, 14, 18))
    card(ctx, 'p4', f, 404, 530)


def s5(ctx, f):
    lf = f - 530
    if lf < 66:
        # Mom, smug, slides the blob plate across the table to the kid
        slide = eout(pop(lf, 14, 30))
        ctx.save(); cam(ctx, 560, 1110, kf(lf, [(0, 1.0), (66, 1.1)], eout), 0, shake_at(lf, [30], 8, 10), f)
        kitchen(ctx, door=1)
        draw_hip(ctx, KIDX, FLOOR - 160, KB, 1, BOY, sit(rsh=30, rel=-30, lsh=-20, lel=-30, eye='normal' if lf < 30 else 'shock', mouth='flat'))
        h = draw_hip(ctx, 790, MHIP, KM, -1, MOM, P(rsh=60, rel=30 + 30 * slide, lsh=-150, lel=60, eye='smug', mouth='grin', head=-4))
        bx, by = h['back']
        pizza_slice(ctx, bx, by - 40, 0.9, -0.4, bite=True)
        rect_r(ctx, 280, 1250, 820, 50, 12); fl(ctx, hx('ffffff'), 7)
        for lx in (320, 1040):
            ctx.rectangle(lx, 1300, 30, 200); fl(ctx, hx('8a5a34'), 6)
        blob(ctx, lerp(700, 500, slide), 1220, 0.9, f, eyes=1, fork=False)
        ctx.restore()
        label(ctx, "“YOU HAVE", 540, 1340, 104, (1, 1, 1), 0.03, pop(lf, 4, 8))
        label(ctx, "FOOD AT HOME.”", 540, 1460, 110, hx('ff3b8a'), -0.03, pop(lf, 10, 14))
        card(ctx, 'p5', f, 534, 596)
    elif lf < 100:
        # kid ECU vs blob ECU: it winks
        il = lf - 66
        ctx.save(); cam(ctx, 400, 1080, 2.0, 4, shake_at(il, [14], 10, 16), f)
        kitchen(ctx, door=1)
        draw_hip(ctx, KIDX - 60, FLOOR - 160, KB, 1, BOY, sit(rsh=-40, rel=-120, lsh=-40, lel=-110, eye='shock', mouth='wavy', head=-6))
        rect_r(ctx, 280, 1250, 820, 50, 12); fl(ctx, hx('ffffff'), 7)
        blob(ctx, 480, 1220, 0.9, f, eyes=1 if il % 20 < 16 else 0.15, fork=False, burp=pop(il, 14, 18) * (1 - pop(il, 18, 26)))
        ctx.restore()
        label(ctx, "BLORP.", 540, 1460, 130, hx('9bdc4a'), 0.04, pop(il, 14, 18))
    else:
        # loop: right back to begging
        il = lf - 100
        beg_shot(ctx, f, il)
        label(ctx, "PLEEEASE?", 540, 1460, 130, hx('ffe14d'), -0.04, pop(il, 0, 4))
        card(ctx, 'p1', f, 630)


SHOTS = [(0, s1), (100, s2), (250, s3), (400, s4), (530, s5)]


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.25)
    ctx.set_source(g); ctx.paint()
    for c in (100, 150, 250, 316, 400, 446, 484, 530, 596, 630):
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.5 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/w{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/food_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
