"""'Online Shopping: Expectation vs Delivery' - original, general-audience comedy short, ~22s.
ECU: kid frozen in shock, pinching a doll-sized hoodie out of the delivery box: "SIZE MEDIUM?!"
It fits... his head. Split screen: THE PHOTO (cool model in a huge hoodie) vs WHAT I GOT.
Reorders XXL: the box explodes into a giant hoodie, he's a walking tent, trips on his own sleeve.
Tries to return it: sits on the overstuffed box, it bursts, BOOM, he lands head-first in fabric.
Twist: the tiny hoodie fits the DOG perfectly - slow-mo glamour shot. Loops back to the opening ECU."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, label, shake_at
import scenes21
from scenes21 import dog
import scenes13
from scenes13 import card as _card13
import random

BOY = doodle.BOY
HOOD, HOODD = hx('8a3cff'), hx('6a22d8')
MODEL = dict(BOY, shirt=HOOD)
N = 660
FLOOR = 1430
KB = 1.45

CAPS = {
    'p1': [[("ORDERING CLOTHES ", OUT)], [("ONLINE", hx('8a3cff')), (" BE LIKE:", OUT)]],
    'p2': [[("THE ", OUT), ("PHOTO", hx('1f8bff')), (" VS ", OUT), ("DELIVERY", hx('ff3b5c'))]],
    'p3': [[("SO I ORDERED ", OUT), ("XXL", hx('ff8a1f'))]],
    'p4': [[("OK. JUST ", OUT), ("RETURN IT", hx('2fbf5a'))]],
    'p5': [[("PLOT TWIST: ", OUT)], [("IT FITS ", OUT), ("SOMEONE", hx('8a3cff'))]],
}
scenes13.CAPS = CAPS
card = _card13

WALL, WALL2 = hx('bfeee0'), hx('a6e2d0')


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


def bolt(ctx, x, y, s):
    poly(ctx, [(x - 10 * s, y - 50 * s), (x + 34 * s, y - 50 * s), (x + 8 * s, y - 6 * s), (x + 30 * s, y - 6 * s),
               (x - 22 * s, y + 56 * s), (x - 4 * s, y + 8 * s), (x - 28 * s, y + 8 * s)])
    fl(ctx, hx('ffe14d'), max(2, 5 * s))


# ------------------------------------------------------------------ props
def hoodie(ctx, x, y, s=1.0, a=0.0, sleeve_a=0.0):
    """flat hoodie, chest centre at (x, y). ~400 wide at s=1"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    lw = 7
    ellipse(ctx, 0, -118, 92, 66); fl(ctx, HOODD, lw)
    for sx in (-1, 1):
        ex, ey = sx * (178 + 20 * sleeve_a), 70 - 60 * sleeve_a
        ctx.new_path(); ctx.move_to(sx * 80, -84); ctx.line_to(ex, ey); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        setc(ctx, INK); ctx.set_line_width(70 + 2 * lw); ctx.stroke_preserve(); setc(ctx, HOOD); ctx.set_line_width(70); ctx.stroke()
        ellipse(ctx, ex, ey + 6, 34, 26); fl(ctx, HOODD, lw)
    rect_r(ctx, -104, -112, 208, 222, 34); fl(ctx, HOOD, lw)
    ctx.rectangle(-104, 86, 208, 24); fl(ctx, HOODD, lw)
    ellipse(ctx, 0, -112, 52, 24); fl(ctx, hx('3a1a7a'), lw)
    for sx in (-1, 1):
        ctx.move_to(sx * 18, -96); ctx.line_to(sx * 22, -40); ink(ctx, 5); ctx.stroke()
        ellipse(ctx, sx * 22, -36, 6, 6); fl(ctx, (1, 1, 1), 3)
    rect_r(ctx, -66, 22, 132, 52, 18); fl(ctx, HOODD, 5)
    bolt(ctx, 4, -34, 0.85)
    ctx.restore()


def box(ctx, x, y, w, h, open_=0.0, tag=None, bulge=0.0, t=0.0, lid_pop=0.0):
    """cardboard box, bottom-centre at (x, y)"""
    bx = w * (1 + 0.12 * bulge * (1 + 0.3 * math.sin(t * 1.3)))
    by = h * (1 - 0.06 * bulge)
    top = y - by
    if bulge > 0:
        # fabric squeezing out of the seams
        for k, (dx, r) in enumerate(((-0.42, 60), (-0.1, 74), (0.25, 66), (0.46, 54))):
            ellipse(ctx, x + dx * bx, top - 10 - 40 * bulge * (1 + 0.2 * math.sin(t * 0.9 + k)), r * (0.5 + bulge), r * (0.4 + 0.6 * bulge))
            fl(ctx, HOOD, 6)
        for sx in (-1, 1):
            ellipse(ctx, x + sx * bx / 2, y - by * 0.5, 40 * bulge, 70 * bulge); fl(ctx, HOOD, 6)
    # flaps hinged on the top edges, swinging outwards
    if open_ > 0:
        a_ = open_ * 2.2
        fh = by * 0.42
        for sx in (-1, 1):
            hx0 = x + sx * bx / 2
            tipx = hx0 - sx * fh * math.cos(a_) * 0.9
            tipy = top - fh * math.sin(a_)
            poly(ctx, [(hx0, top), (x + sx * bx * 0.08, top), (x + sx * bx * 0.08 + (tipx - hx0), tipy), (tipx, tipy)])
            fl(ctx, hx('c88a50'), 6)
    rect_r(ctx, x - bx / 2, top, bx, by, 10); fl(ctx, hx('dda56a'), 8)
    ctx.rectangle(x - bx / 2 + 10, top + by * 0.45, bx - 20, 6); setc(ctx, (0, 0, 0, 0.1)); ctx.fill()
    if open_ <= 0:
        ctx.rectangle(x - 34, top, 68, by * 0.35); setc(ctx, hx('f0d7a8')); ctx.fill_preserve(); ink(ctx, 4); ctx.stroke()
        ctx.move_to(x - bx / 2 + 6, top + 4); ctx.line_to(x + bx / 2 - 6, top + 4); ink(ctx, 6); ctx.stroke()
    # shipping label
    rect_r(ctx, x + bx * 0.1, top + by * 0.55, bx * 0.3, by * 0.28, 8); fl(ctx, (1, 1, 1), 5)
    for j in range(3):
        ctx.move_to(x + bx * 0.14, top + by * (0.62 + j * 0.07)); ctx.line_to(x + bx * 0.36 - (j * bx * 0.06), top + by * (0.62 + j * 0.07)); ink(ctx, 4); ctx.stroke()
    if tag:
        text(ctx, tag, x - bx * 0.2, top + by * 0.62, by * 0.26, hx('ff8a1f'), ow=10, ang=-0.08, shadow=False)
    return top


def rain_cloud(ctx, x, y, t, s=1.0):
    for k in range(4):
        tt = (t * 0.06 + k / 4) % 1
        ctx.move_to(x - 60 * s + k * 40 * s, y + 30 * s + tt * 150 * s); ctx.line_to(x - 66 * s + k * 40 * s, y + 60 * s + tt * 150 * s)
        setc(ctx, hx('5aa8ff', 0.9) if False else (0.35, 0.65, 1, 1 - tt)); ctx.set_line_width(8 * s); ctx.stroke()
    for dx, r in ((-60, 46), (0, 64), (58, 48)):
        ellipse(ctx, x + dx * s, y, r * s, r * 0.8 * s)
    setc(ctx, hx('8a94a8')); ctx.fill_preserve(); ink(ctx, 5); ctx.stroke()
    for dx, r in ((-60, 46), (0, 64), (58, 48)):
        ellipse(ctx, x + dx * s, y, r * s - 3, r * 0.8 * s - 3)
    setc(ctx, hx('8a94a8')); ctx.fill()


# ------------------------------------------------------------------ sets
def entry(ctx):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, WALL); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 120, -3000, 50, 3000 + FLOOR); setc(ctx, WALL2); ctx.fill()
    # front door
    rect_r(ctx, -140, 620, 380, FLOOR - 620, 14); fl(ctx, hx('ff6b5a'), 10)
    for yy in (700, 1000):
        rect_r(ctx, -90, yy, 280, 240, 10); setc(ctx, (0, 0, 0, 0.1)); ctx.fill_preserve(); ink(ctx, 5); ctx.stroke()
    ellipse(ctx, 190, 1060, 18, 18); fl(ctx, hx('ffd23f'), 5)
    # coat hooks + hanging cap
    ctx.rectangle(400, 640, 300, 30); fl(ctx, hx('c98a52'), 7)
    for hxp in (450, 550, 650):
        ellipse(ctx, hxp, 690, 12, 12); fl(ctx, hx('ffd23f'), 4)
    ctx.new_path(); ctx.arc(550, 760, 60, math.pi, 2 * math.pi); ctx.close_path(); fl(ctx, hx('1f8bff'), 6)
    ellipse(ctx, 600, 762, 50, 12); fl(ctx, hx('1f8bff'), 5)
    # framed plant picture
    rect_r(ctx, 780, 520, 230, 280, 10); fl(ctx, hx('fff6e8'), 9)
    poly(ctx, [(840, 760), (950, 760), (930, 700), (860, 700)]); fl(ctx, hx('d0703a'), 5)
    for k in range(3):
        ellipse(ctx, 870 + k * 25, 650 - 20 * (k % 2), 22, 40, -0.4 + 0.4 * k); fl(ctx, hx('3fbf4a'), 4)
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('e0a868')); ctx.fill()
    for i in range(-30, 40):
        ctx.move_to(i * 120, FLOOR); ctx.line_to(i * 120 - 80, FLOOR + 1500); setc(ctx, (0, 0, 0, 0.08)); ctx.set_line_width(6); ctx.stroke()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()
    ellipse(ctx, 560, FLOOR + 90, 430, 70); setc(ctx, hx('ff8fb8')); ctx.fill_preserve(); ink(ctx, 6); ctx.stroke()
    ellipse(ctx, 560, FLOOR + 90, 360, 50); setc(ctx, (1, 1, 1, 0.35)); ctx.set_line_width(8); ctx.stroke()


# ------------------------------------------------------------------ characters
_SCR = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4))


def probe(x, hipy, k, f_, ch, p):
    return draw_hip(_SCR, x, hipy, k, f_, ch, p)


def head_on_top(ctx, x, hipy, k, f_, ch, p, b, r=1.3):
    hd, R = b['head'], b['R']
    ctx.save(); ctx.new_path(); ctx.arc(hd[0], hd[1] - R * 0.25, R * r, 0, 2 * math.pi); ctx.clip()
    draw_hip(ctx, x, hipy, k, f_, ch, p)
    ctx.restore()


def beanie_kid(ctx, x, hipy, k, f_, p, t=0.0):
    """kid wearing the tiny hoodie on his head like a hat"""
    b = draw_hip(ctx, x, hipy, k, f_, BOY, p)
    hd, R = b['head'], b['R']
    hoodie(ctx, hd[0] + f_ * R * 0.05, hd[1] - R * 0.82, R / 250, f_ * (0.06 + 0.03 * math.sin(t * 0.3)), sleeve_a=-0.5)
    return b


def giant_hoodie_kid(ctx, x, k, p, t=0.0, f_=1, spread=1.0):
    """kid swallowed by an XXL hoodie: only the face pokes out"""
    hipy = FLOOR - 92 * k
    b = draw_hip(ctx, x, hipy, k, f_, BOY, p)
    hd, R = b['head'], b['R']
    top = hd[1] + R * 0.55
    w = 760 * spread
    sw = 6 * math.sin(t * 0.35)
    # sleeves pooling on the floor
    for sx in (-1, 1):
        ctx.new_path(); ctx.move_to(x + sx * 170, top + 120)
        ctx.curve_to(x + sx * 360, top + 260, x + sx * (w / 2 + 40), FLOOR - 160, x + sx * (w / 2 + 200 + sw * sx), FLOOR - 50)
        ctx.curve_to(x + sx * (w / 2 + 320), FLOOR - 10, x + sx * (w / 2 + 420), FLOOR - 40, x + sx * (w / 2 + 470), FLOOR - 50)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); setc(ctx, INK); ctx.set_line_width(150); ctx.stroke_preserve()
        setc(ctx, HOOD); ctx.set_line_width(134); ctx.stroke()
        ellipse(ctx, x + sx * (w / 2 + 490), FLOOR - 52, 40, 64); fl(ctx, HOODD, 8)
    ctx.new_path(); ctx.move_to(x - 170, top)
    ctx.curve_to(x - 260, top + 200, x - w / 2 - sw, FLOOR - 300, x - w / 2 - sw, FLOOR)
    ctx.line_to(x + w / 2 + sw, FLOOR)
    ctx.curve_to(x + w / 2 + sw, FLOOR - 300, x + 260, top + 200, x + 170, top); ctx.close_path()
    fl(ctx, HOOD, 10)
    ctx.rectangle(x - w / 2 - 20, FLOOR - 60, w + 40, 60); fl(ctx, HOODD, 8)
    rect_r(ctx, x - 200, FLOOR - 330, 400, 150, 40); fl(ctx, HOODD, 8)
    bolt(ctx, x + 10, top + 280, 2.6)
    # hood around the face
    ellipse(ctx, hd[0], hd[1] + R * 0.1, R * 1.75, R * 1.6); fl(ctx, HOOD, 10)
    ellipse(ctx, hd[0], hd[1] + R * 0.12, R * 1.32, R * 1.22); fl(ctx, hx('3a1a7a'), 8)
    ctx.save(); ellipse(ctx, hd[0], hd[1] + R * 0.12, R * 1.32, R * 1.22); ctx.clip()
    draw_hip(ctx, x, hipy, k, f_, BOY, p)
    ctx.restore()
    for sx in (-1, 1):
        ctx.move_to(hd[0] + sx * R * 0.5, hd[1] + R * 1.25); ctx.line_to(hd[0] + sx * R * 0.6, top + 420 + 10 * math.sin(t * 0.5 + sx)); ink(ctx, 9); ctx.stroke()
        ellipse(ctx, hd[0] + sx * R * 0.6, top + 430 + 10 * math.sin(t * 0.5 + sx), 14, 14); fl(ctx, (1, 1, 1), 6)
    return b


def dog_hoodie(ctx, x, y, s, f_, fr, **kw):
    """the dog in the tiny hoodie - a perfect fit"""
    dog(ctx, x, y, s, f_, fr, **kw)
    ctx.save(); ctx.translate(x, y); ctx.scale(s * f_, s)
    for lx in (18, 62):
        rect_r(ctx, lx - 22, -150, 44, 82, 18); fl(ctx, HOOD, 6)
        ctx.rectangle(lx - 22, -82, 44, 14); fl(ctx, HOODD, 5)
    ellipse(ctx, 15, -128, 84, 100); fl(ctx, HOOD, 6)
    ellipse(ctx, -50, -205, 58, 40, -0.4); fl(ctx, HOODD, 6)
    bolt(ctx, 30, -120, 0.9)
    ctx.restore()
    ctx.save(); ctx.translate(x, y); ctx.scale(s * f_, s)
    ellipse(ctx, 66, -262, 122, 96); ctx.restore()
    ctx.save(); ctx.clip(); dog(ctx, x, y, s, f_, fr, **kw); ctx.restore()


# ------------------------------------------------------------------ shots
def opening_face(ctx, f, lf, loop=False):
    pb = P(rsh=30, rel=-120, lsh=25, lel=20, eye='shock', mouth='scream', torso=-3, head=5)
    pr = probe(540, 1300, KB, 1, BOY, pb)
    hd, R = pr['head'], pr['R']
    ctx.save()
    cam(ctx, hd[0], hd[1] + 80, 1.85, 2 * math.sin(lf * 0.2), shake_at(lf, [0], 10, 14) + 2, f, sy=900)
    entry(ctx)
    rays(ctx, hd[0], hd[1], R * 1.2, 1600, lf * 0.02, col=(1, 1, 1), a=0.25, n=16)
    b = draw_hip(ctx, 540, 1300, KB, 1, BOY, pb)
    for j, (dx, ph) in enumerate(((-1.25, 0), (1.3, 9))):
        tt = ((lf + ph) % 22) / 22
        sweat(ctx, hd[0] + dx * R, hd[1] - R * 0.4 + tt * R * 0.9, 1.4)
    # the box in the foreground
    box(ctx, 540, hd[1] + R * 3.7, 760, 260, open_=1.0)
    # tiny hoodie pinched in his fingers, swinging
    hn = b['front']
    sw = 0.18 * math.sin(lf * 0.25)
    hy = hn[1] - 10 * abs(math.sin(lf * 0.25))
    hxp = hn[0]
    hoodie(ctx, hxp - math.sin(sw) * 80, hy + 82, 0.38, sw)
    ellipse(ctx, hxp, hy, 22, 22); fl(ctx, BOY['skin'], 5)
    ctx.restore()
    label(ctx, "\"SIZE... MEDIUM?!\"", 540, 1440, 96, (1, 1, 1), -0.04, 1 if (loop or lf >= 0) else 0)


def s1(ctx, f):
    if f < 64:
        opening_face(ctx, f, f)
    else:
        lf = f - 64
        ctx.save(); cam(ctx, 540, 930, lerp(1.22, 1.34, lf / 56), 0, shake_at(lf, [6], 8, 14), f)
        entry(ctx)
        rays(ctx, 540, 800, 140, 1600, lf * 0.02, col=(1, 1, 1), a=0.25, n=18)
        box(ctx, 860, FLOOR, 300, 180, open_=1.0)
        pk = P(rsh=-20, rel=-10, lsh=15, lel=-10, eye='normal', mouth='flat', head=0, blink=1 if 40 <= lf < 44 else 0)
        beanie_kid(ctx, 520, FLOOR - 92 * 1.55, 1.55, 1, pk, lf)
        ctx.restore()
        label(ctx, "IT FITS... MY HEAD", 540, 1440, 96, hx('ffe14d'), 0.04, pop(lf, 8, 12))
    card(ctx, 'p1', f, -6, 118)


def s2(ctx, f):
    lf = f - 120
    ctx.rectangle(0, 0, W, H); setc(ctx, INK); ctx.fill()
    # LEFT: the photo
    sl = eout(pop(lf, 0, 10))
    ctx.save(); ctx.translate(lerp(-540, 0, sl), 0)
    ctx.rectangle(0, 0, 534, H); ctx.clip()
    ctx.rectangle(0, 0, 540, H); setc(ctx, hx('ffb8d8')); ctx.fill()
    rays(ctx, 270, 1000, 80, 1300, lf * 0.03, col=(1, 1, 1), a=0.45, n=16)
    ctx.rectangle(0, 1330, 540, 600); setc(ctx, hx('ff8fb8')); ctx.fill()
    ctx.move_to(0, 1330); ctx.line_to(540, 1330); ink(ctx, 7); ctx.stroke()
    pm = P(rsh=150, rel=30, lsh=-30, lel=-60, eye='smug', mouth='grin', head=-6, shades=1, torso=-4, rhip=-10, lhip=10)
    b = draw_hip(ctx, 280, 1330 - 92 * 1.2, 1.2, 1, MODEL, pm)
    bolt(ctx, 280, 1330 - 92 * 1.2 - 55 * 1.35 * 1.2, 1.2)
    for k in range(5):
        a_ = k * 1.3 + lf * 0.06
        sparkle(ctx, 280 + math.cos(a_) * 210, 900 + math.sin(a_) * 260, 22 + 8 * math.sin(lf * 0.3 + k), (1, 1, 1))
    text(ctx, "THE PHOTO", 270, 600, 60, (1, 1, 1), ow=10)
    ctx.restore()
    # RIGHT: what I got
    sr = eout(pop(lf, 6, 16))
    ctx.save(); ctx.translate(lerp(540, 0, sr), 0)
    ctx.rectangle(546, 0, 534, H); ctx.clip()
    ctx.rectangle(540, 0, 540, H); setc(ctx, hx('a8b4c8')); ctx.fill()
    ctx.rectangle(540, 1330, 540, 600); setc(ctx, hx('7a8498')); ctx.fill()
    ctx.move_to(540, 1330); ctx.line_to(1080, 1330); ink(ctx, 7); ctx.stroke()
    pr = P(rsh=-10, rel=-5, lsh=10, lel=-5, eye='normal', mouth='frown', head=4)
    b2 = beanie_kid(ctx, 800, 1330 - 92 * 1.2, 1.2, -1, pr, lf)
    rain_cloud(ctx, 800, b2['head'][1] - b2['R'] * 2.2, lf, 0.9)
    text(ctx, "WHAT I GOT", 810, 600, 60, hx('ffe14d'), ow=10)
    ctx.restore()
    if lf >= 30:
        label(ctx, "\"TRUE TO SIZE!\"", 540, 1470, 104, (1, 1, 1), -0.03, pop(lf, 30, 36))
    card(ctx, 'p2', f, 124, 246)


def s3(ctx, f):
    lf = f - 250
    if lf < 84:
        # box drops in, kid hypes, box erupts
        z = lerp(1.0, 1.12, lf / 84)
        ctx.save(); cam(ctx, 560, 1080, z, 0, shake_at(lf, [10], 10, 22) + shake_at(lf, [52], 22, 30), f)
        entry(ctx)
        drop = ein(pop(lf, 0, 10))
        by = lerp(-300, FLOOR, drop)
        sq = 0.0 if lf < 10 else 0.1 * math.exp(-(lf - 10) * 0.3) * math.cos((lf - 10) * 1.2)
        hype = lf < 50
        pk = P(rsh=160 if hype else 40, rel=10 if hype else -100, lsh=160 if hype else 30, lel=-10 if hype else -20,
               eye='happy' if hype else 'shock', mouth='grin' if hype else 'scream', head=3 * math.sin(lf * 0.5) if hype else 0)
        jump = abs(math.sin(lf * 0.35)) * 40 if 12 < lf < 46 else 0
        draw_hip(ctx, 880, FLOOR - 92 * 1.3 - jump, 1.3, -1, BOY, pk)
        ctx.save(); ctx.translate(500, by); ctx.scale(1 + sq, 1 - sq); ctx.translate(-500, -by)
        box(ctx, 500, by, 440, 300, open_=eout(pop(lf, 44, 52)), tag="XXL")
        ctx.restore()
        if lf >= 10:
            puff(ctx, 300, FLOOR - 20, pop(lf, 10, 24), 1.4); puff(ctx, 700, FLOOR - 20, pop(lf, 10, 24), 1.4)
        # eruption
        if lf >= 50:
            u = eout(pop(lf, 50, 66))
            hoodie(ctx, 500, lerp(FLOOR - 300, 760, u), lerp(0.2, 3.6, u), 0.25 * math.sin(lf * 0.4) * (1 - u), sleeve_a=-0.3 + 0.6 * math.sin(lf * 0.6))
        ctx.restore()
        if lf < 50:
            label(ctx, "\"XXL! FINALLY!\"", 540, 1450, 110, hx('ffe14d'), 0.04, pop(lf, 12, 16))
        else:
            label(ctx, "*FWOOMP*", 540, 1450, 150, hx('ff8a1f'), -0.05, pop(lf, 52, 56))
    else:
        il = lf - 84
        fall = ein(pop(il, 40, 50))
        bounce = 0 if il < 50 else 0.04 * math.exp(-(il - 50) * 0.3) * math.sin((il - 50) * 1.4)
        ctx.save(); cam(ctx, 540, 1050, 0.82, 0, shake_at(il, [50], 12, 30), f)
        entry(ctx)
        x = 560 - min(il, 40) * 2
        pk = P(rsh=-10, rel=0, lsh=10, lel=0, eye='normal' if il < 40 else 'shock', mouth='flat' if il < 40 else 'scream',
               head=4 * math.sin(il * 0.3))
        piv = (x + 300, FLOOR)
        ctx.save(); ctx.translate(x, FLOOR); ctx.scale(1 + 0.35 * fall + bounce * 3, 1 - 0.62 * fall - bounce * 3); ctx.translate(-x, -FLOOR)
        giant_hoodie_kid(ctx, x, 1.25, pk, il)
        ctx.restore()
        if il >= 50:
            puff(ctx, x - 450, FLOOR - 30, pop(il, 50, 64), 2.2); puff(ctx, x + 450, FLOOR - 30, pop(il, 50, 64), 2.2)
            stars_ko(ctx, x, FLOOR - 470, il * 0.1, 4, 140)
        ctx.restore()
        if il < 40:
            label(ctx, "\"I'M A TENT.\"", 540, 1450, 120, (1, 1, 1), -0.04, pop(il, 4, 8))
        else:
            label(ctx, "*THUD*", 540, 1450, 160, hx('ff3b5c'), 0.05, pop(il, 50, 54))
    card(ctx, 'p3', f, 254, 396)


def s4(ctx, f):
    lf = f - 400
    boom = 62
    ctx.save()
    if lf < boom:
        z = lerp(1.0, 1.12, lf / boom)
        cam(ctx, 540, 1080, z, 3 * math.sin(lf * 0.4), 3 + shake_at(lf % 14, [0], 6, 10), f)
    else:
        cam(ctx, 540, 1050, 0.95, 0, shake_at(lf, [boom], 18, 40), f)
    entry(ctx)
    if lf < boom:
        bl = pop(lf, 0, boom)
        hop = abs(math.sin(lf * 0.45)) * 40
        top = box(ctx, 540, FLOOR, 520, 300, bulge=0.3 + 0.9 * bl, t=lf)
        draw_hip(ctx, 540, top - 10 - hop, 1.3, 1, BOY, P(rsh=-150, rel=-30, lsh=-140, lel=-30, eye='closed', mouth='wavy',
                                                        lhip=88, lkn=-82, rhip=95, rkn=-90, head=-3 * math.sin(lf * 0.45)))
    else:
        bl = lf - boom
        # cardboard shards + fabric cloud
        rnd = random.Random(9)
        u = eout(pop(bl, 0, 20))
        for k in range(7):
            a_ = rnd.uniform(-math.pi, 0)
            d = 300 + rnd.uniform(0, 500)
            px, py = 540 + math.cos(a_) * d * u, FLOOR - 150 + math.sin(a_) * d * u + 900 * pop(bl, 10, 50) ** 2
            ctx.save(); ctx.translate(px, py); ctx.rotate(bl * 0.2 * (k % 3 - 1) + k)
            ctx.rectangle(-70, -50, 140, 100); fl(ctx, hx('dda56a'), 6); ctx.restore()
        for k in range(9):
            a_ = k * 2 * math.pi / 9
            r = 180 * u + 30
            ellipse(ctx, 540 + math.cos(a_) * 380 * u, FLOOR - 120 + math.sin(a_) * 120 * u, r, r * 0.7); fl(ctx, HOOD, 8)
        ellipse(ctx, 540, FLOOR - 100, 520 * u + 40, 200 * u + 20); fl(ctx, HOOD, 9)
        bolt(ctx, 600, FLOOR - 140, 1.4 * u)
        # kid launched up then nose-dives into the pile
        if bl < 24:
            yy = lerp(FLOOR - 500, -900, eout(pop(bl, 0, 24)))
            ctx.save(); ctx.translate(540, yy); ctx.rotate(bl * 0.4)
            draw_hip(ctx, 0, 0, 1.2, 1, BOY, P(rsh=170, rel=0, lsh=170, lel=0, eye='shock', mouth='scream', lhip=30, rhip=-30))
            ctx.restore()
        elif bl >= 34:
            dl = pop(bl, 34, 44)
            yy = lerp(-900, FLOOR - 160, ein(dl))
            ctx.save(); ctx.translate(540, yy); ctx.rotate(math.pi)
            if dl < 1:
                draw_hip(ctx, 0, 0, 1.2, 1, BOY, P(rsh=10, lsh=-10, lhip=10, rhip=-10, eye='shock', mouth='scream'))
            else:
                # buried head-first: legs wiggle out of the pile
                for k, sx in enumerate((-1, 1)):
                    a_ = 0.3 * math.sin(bl * 0.9 + k * 2) + sx * 0.2
                    ctx.save(); ctx.translate(sx * 30, 0); ctx.rotate(a_)
                    ctx.move_to(0, 0); ctx.line_to(0, 230); setc(ctx, INK); ctx.set_line_width(66); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke_preserve()
                    setc(ctx, BOY['pants']); ctx.set_line_width(52); ctx.stroke()
                    ellipse(ctx, 0, 256, 50, 30); fl(ctx, BOY['shoes'], 7)
                    ctx.restore()
            ctx.restore()
            if dl >= 1:
                puff(ctx, 540, FLOOR - 200, pop(bl, 44, 58), 2.4)
    ctx.restore()
    if lf < boom:
        label(ctx, "*SQUISH* *SQUISH*", 540, 1450, 96, (1, 1, 1), 0.04 * math.sin(lf * 0.3), pop(lf, 4, 8))
    elif lf < boom + 34:
        label(ctx, "BOOM!", 540, 1450, 180, hx('ff3b5c'), -0.05, pop(lf, boom, boom + 4))
    else:
        label(ctx, "*FLOMP*", 540, 1450, 150, hx('ffe14d'), 0.05, pop(lf, boom + 44, boom + 48))
    card(ctx, 'p4', f, 404, 516)


def s5(ctx, f):
    lf = f - 520
    if lf < 120:
        if lf < 44:
            # low-angle glamour push-in on the dog
            z = lerp(1.25, 1.55, eout(lf / 44))
            ctx.save(); cam(ctx, 560, 1080, z, -3, shake_at(lf, [0], 8, 14), f)
            ctx.rectangle(-2000, -2000, 5000, 5000); setc(ctx, hx('ffb8d8')); ctx.fill()
            rays(ctx, 560, 900, 100, 1800, lf * 0.04, col=(1, 1, 1), a=0.5, n=20)
            ctx.rectangle(-2000, FLOOR, 5000, 2000); setc(ctx, hx('ff8fb8')); ctx.fill()
            ctx.move_to(-2000, FLOOR); ctx.line_to(3000, FLOOR); ink(ctx, 8); ctx.stroke()
            dog_hoodie(ctx, 500, FLOOR, 1.5, 1, lf * 0.5, eye='smug', tail=1.6, tilt=-0.15)
            for k in range(6):
                a_ = k * math.pi / 3 + lf * 0.05
                sparkle(ctx, 560 + math.cos(a_) * 330, 1000 + math.sin(a_) * 300, 26 + 10 * math.sin(lf * 0.4 + k), (1, 1, 1))
            ctx.restore()
            label(ctx, "THE DOG.", 540, 1450, 150, hx('ffe14d'), -0.04, pop(lf, 6, 10))
        else:
            il = lf - 44
            ctx.save(); cam(ctx, 600, 1020, lerp(0.92, 0.98, il / 76), 0, shake_at(il, [0], 8, 16), f)
            entry(ctx)
            giant_hoodie_kid(ctx, 360, 1.15, P(rsh=-10, lsh=10, eye='shock' if il < 40 else 'normal',
                                               mouth='scream' if il < 40 else 'wavy', head=-6), il, spread=0.8)
            dog_hoodie(ctx, 800, FLOOR, 1.15, -1, il * 0.6, eye='smug' if il < 50 else 'happy', tail=1.8, tilt=0.1 * math.sin(il * 0.2))
            for k in range(4):
                a_ = k * math.pi / 2 + il * 0.06
                sparkle(ctx, 760 + math.cos(a_) * 200, 1040 + math.sin(a_) * 180, 20, (1, 1, 1))
            ctx.restore()
            if il < 36:
                label(ctx, "PERFECT FIT.", 540, 1450, 140, (1, 1, 1), 0.04, pop(il, 2, 6))
            else:
                label(ctx, "\"...CAN WE SWAP?\"", 540, 1450, 104, hx('ffe14d'), -0.04, pop(il, 36, 40))
        card(ctx, 'p5', f, 524, 636)
    else:
        il = lf - 120
        opening_face(ctx, f, il, loop=True)
        card(ctx, 'p1', f, 640)


SHOTS = [(0, s1), (120, s2), (250, s3), (400, s4), (520, s5)]
CUTS = (64, 120, 250, 334, 400, 520, 564, 640)


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
            render(f).write_to_png(f'out/w{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/shop_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
