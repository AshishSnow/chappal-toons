"""'The Closet Strategy' - original, general-audience comedy short, ~35s.
Mom says clean your room. The kid shoves everything in the closet... until Mom opens it."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import cam, pop, sparkle, puff, label, shake_at
from scenes8 import walk
from scenes13 import card as _card13
import scenes13

BOY, MOM, DAD = doodle.BOY, doodle.MOM_G, doodle.DAD
N = 1050
STAND = 1500
KB, KM = 1.25, 1.5
CL = (720, 560, 330, 940)          # closet x, y, w, h (world)
DOORL = (-60, 640, 290, 860)       # bedroom door on the left
BX = 470                           # boy home x

CAPS = {
    'p1': [[("WHEN MOM SAYS", OUT)], [("CLEAN YOUR ROOM", hx('1f8bff'))]],
    'p2': [[("BUT I HAD A", OUT)], [("GENIUS", hx('e07b12')), (" PLAN", OUT)]],
    'p3': [[("SPEED CLEANING", hx('ff3b5c'))], [("ACTIVATED", OUT)]],
    'p4': [[("IT FITS...", OUT)], [("BARELY", hx('8a3cff'))]],
    'p5': [[("THEN MOM WENT", OUT)], [("FOR THE ", OUT), ("CLOSET", hx('ff3b5c'))]],
    'p6': [[("THE CLOSET", OUT)], [("HAD ", OUT), ("ENOUGH", hx('e07b12'))]],
    'p7': [[("PLAN B: ", hx('1f8bff')), ("UNDER", OUT)], [("THE BED", OUT)]],
}
scenes13.CAPS = CAPS
card = _card13
_tmp = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4))


# ------------------------------------------------------------------ props
def rect_r(ctx, x, y, w, h, r):
    ctx.new_path(); ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); ctx.close_path()


def item(ctx, kind, x, y, a=0.0, s=1.0, col=None):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if kind == 'sock':
        c = col or hx('ff3b8a')
        poly(ctx, [(-18, -60), (18, -60), (18, 10), (50, 22), (50, 50), (-18, 50)]); fl(ctx, c, 5)
        ctx.rectangle(-18, -60, 36, 18); fl(ctx, (1, 1, 1), 4)
    elif kind == 'ball':
        ellipse(ctx, 0, 0, 46, 46); fl(ctx, col or hx('ff4d3d'), 5)
        ctx.new_path(); ctx.arc(-60, 0, 52, -0.8, 0.8); setc(ctx, (1, 1, 1)); ctx.set_line_width(7); ctx.stroke()
        ctx.new_path(); ctx.arc(60, 0, 52, math.pi - 0.8, math.pi + 0.8); ctx.stroke()
    elif kind == 'book':
        ctx.rectangle(-48, -34, 96, 68); fl(ctx, col or hx('2f6bff'), 5)
        ctx.rectangle(-48, 22, 96, 12); fl(ctx, (1, 1, 1), 4)
        ctx.rectangle(-30, -20, 50, 12); setc(ctx, (1, 1, 1, 0.7)); ctx.fill()
    elif kind == 'box':
        ctx.rectangle(-62, -20, 124, 40); fl(ctx, hx('e8b46a'), 5)
        ctx.move_to(-62, -6); ctx.line_to(62, -6); ink(ctx, 4); ctx.stroke()
        ellipse(ctx, 0, 6, 14, 6); setc(ctx, hx('d0263a')); ctx.fill()
    elif kind == 'car':
        rect_r(ctx, -50, -24, 100, 32, 10); fl(ctx, col or hx('ff3b5c'), 5)
        rect_r(ctx, -26, -44, 50, 24, 8); fl(ctx, hx('8fe9ff'), 5)
        for wx in (-28, 28):
            ellipse(ctx, wx, 10, 15, 15); fl(ctx, hx('2a2f45'), 4)
    elif kind == 'shirt':
        c = col or hx('2fbf5a')
        poly(ctx, [(-24, -40), (-60, -24), (-48, 0), (-30, -8), (-30, 44), (30, 44), (30, -8), (48, 0), (60, -24), (24, -40), (10, -30), (-10, -30)])
        fl(ctx, c, 5)
        ctx.rectangle(-30, 4, 60, 10); setc(ctx, light(c, 0.4)); ctx.fill()
    elif kind == 'cup':
        ctx.rectangle(-24, -30, 48, 56); fl(ctx, col or hx('ffd23f'), 5)
        ctx.new_path(); ctx.arc(26, -2, 15, -1.4, 1.4); ink(ctx, 9); ctx.stroke()
    elif kind == 'bear':
        c = col or hx('b07040')
        for ex in (-26, 26):
            ellipse(ctx, ex, -40, 15, 15); fl(ctx, c, 4)
        ellipse(ctx, 0, 24, 36, 32); fl(ctx, c, 5)
        ellipse(ctx, 0, -18, 34, 30); fl(ctx, c, 5)
        for ex in (-11, 11):
            ellipse(ctx, ex, -22, 4, 5); setc(ctx, INK); ctx.fill()
        ellipse(ctx, 0, -8, 12, 9); fl(ctx, light(c, 0.5), 3)
    elif kind == 'plane':
        poly(ctx, [(-60, 0), (60, -16), (-30, 26)]); fl(ctx, (1, 1, 1), 5)
        ctx.move_to(-60, 0); ctx.line_to(0, 6); ink(ctx, 3); ctx.stroke()
    elif kind == 'cube':
        ctx.rectangle(-32, -32, 64, 64); fl(ctx, INK, 5)
        cs = (hx('ff3b5c'), hx('ffd23f'), hx('2f6bff'), hx('2fbf5a'), (1, 1, 1), hx('ff8a3d'))
        for i in range(3):
            for j in range(3):
                ctx.rectangle(-28 + i * 19, -28 + j * 19, 16, 16); setc(ctx, cs[(i * 2 + j) % 6]); ctx.fill()
    elif kind == 'guitar':
        ctx.rectangle(-8, -110, 16, 90); fl(ctx, hx('7a4a2c'), 4)
        ellipse(ctx, 0, 0, 40, 34); fl(ctx, hx('ff8a3d'), 5)
        ellipse(ctx, 0, 34, 50, 40); fl(ctx, hx('ff8a3d'), 5)
        ellipse(ctx, 0, 8, 12, 12); setc(ctx, INK); ctx.fill()
    ctx.restore()


# floor mess: (kind, x, y, angle, scale, colour)
MESS = [
    ('shirt', 110, 1470, 0.3, 1.0, hx('2fbf5a')), ('sock', 300, 1500, -0.5, 0.9, hx('ff3b8a')), ('ball', 640, 1470, 0, 1.0, None),
    ('book', 760, 1500, 0.2, 1.0, hx('2f6bff')), ('box', 900, 1505, -0.1, 1.0, None), ('car', 220, 1545, 0.1, 1.0, None),
    ('cup', 990, 1450, 0.3, 1.0, None), ('bear', 600, 1560, -0.3, 1.0, None), ('plane', 400, 1210, 0.4, 1.0, None),
    ('cube', 880, 1590, 0.3, 1.0, None), ('sock', 820, 1610, 0.8, 0.9, hx('8a3cff')), ('shirt', 360, 1600, -0.4, 0.9, hx('ff8a3d')),
    ('book', 140, 1590, -0.3, 0.9, hx('ff3b5c')), ('guitar', 1010, 1300, 0.5, 1.0, None), ('shirt', 270, 1260, 0.6, 0.9, hx('ffd23f')),
    ('sock', 520, 1620, -0.2, 0.9, hx('2fbf5a')),
]
FLY0, FLYD, FLYDT = 236, 14, 8    # cleaning montage timing


def fly_state(i, f):
    """returns None if still on floor, (x,y,a) mid-air, or 'in' once inside closet"""
    t0 = FLY0 + i * FLYDT
    if f < t0:
        return None
    t = (f - t0) / FLYD
    if t >= 1:
        return 'in'
    k, x, y, a, s, c = MESS[i]
    tx, ty = CL[0] + CL[2] * (0.3 + 0.4 * ((i * 7) % 5) / 4), CL[1] + 300 + ((i * 3) % 4) * 90
    return (lerp(x, tx, t), lerp(y, ty, t) - math.sin(t * math.pi) * 360, a + t * 9 * (1 if i % 2 else -1))


def draw_mess(ctx, f, cleaned=None):
    for i, (k, x, y, a, s, c) in enumerate(MESS):
        st = fly_state(i, f) if cleaned is None else ('in' if cleaned else None)
        if st is None:
            item(ctx, k, x, y, a, s, c)
        elif st != 'in':
            item(ctx, k, st[0], st[1], st[2], s, c)


# ------------------------------------------------------------------ set
def closet(ctx, f, open_=0.0, bulge=0.0, stuffed=1.0, poke=0.0):
    x, y, w, h = CL
    ctx.rectangle(x - 22, y - 22, w + 44, h + 22); fl(ctx, hx('f2e6d0'), 8)
    ctx.rectangle(x, y, w, h); setc(ctx, hx('2a2340')); ctx.fill()
    # interior stuff (seen when open)
    if open_ > 0.02 and stuffed > 0:
        rnd = random.Random(9)
        ctx.save(); ctx.rectangle(x, y, w, h); ctx.clip()
        kinds = [m[0] for m in MESS]
        for j in range(int(30 * stuffed)):
            item(ctx, kinds[j % len(kinds)], x + rnd.uniform(20, w - 20), y + h - rnd.uniform(0, h * stuffed), rnd.uniform(-3, 3), 1.0,
                 (hx('ff3b8a'), hx('2fbf5a'), hx('ffd23f'), hx('2f6bff'), hx('8a3cff'))[j % 5])
        ctx.restore()
    # door panel: hinge on right, swings so panel narrows toward right
    pw = w * (1 - open_ * 0.85)
    x0 = x + w - pw
    b = bulge * 40
    ctx.new_path(); ctx.move_to(x0, y); ctx.line_to(x + w, y); ctx.line_to(x + w, y + h); ctx.line_to(x0, y + h)
    ctx.curve_to(x0 - b, y + h * 0.7, x0 - b, y + h * 0.3, x0, y); ctx.close_path()
    fl(ctx, hx('5fb8ff'), 8)
    if pw > 120:
        for yy in (y + 60, y + h * 0.52 + 20):
            rect_r(ctx, x0 + 40 - b * 0.4, yy, pw - 80, h * 0.36, 10); setc(ctx, light(hx('5fb8ff'), 0.3)); ctx.fill_preserve(); ink(ctx, 5); ctx.stroke()
        ellipse(ctx, x0 + 26 - b * 0.8, y + h * 0.52, 12, 12); fl(ctx, hx('ffd23f'), 4)
    if poke > 0:
        # stuff poking out the gap on the left edge of the door
        item(ctx, 'sock', x0 - 20 - b, y + h * 0.4, -1.6, 0.8 * poke, hx('ff3b8a'))
        item(ctx, 'shirt', x0 - 26 - b, y + h * 0.7, -1.3, 0.7 * poke, hx('ffd23f'))
        item(ctx, 'car', x0 - 18 - b * 0.6, y + 70, 1.2, 0.6 * poke)


def room(ctx, f, wall=hx('ffb84d')):
    ctx.rectangle(-1200, -1500, 3600, 3200); setc(ctx, wall); ctx.fill()
    rnd = random.Random(15)
    for _ in range(46):
        xx, yy = rnd.uniform(-900, 1900), rnd.uniform(-1200, 1450)
        ellipse(ctx, xx, yy, 9, 9); setc(ctx, light(wall, 0.3)); ctx.fill()
    # ceiling line (seen in the final tilt-up)
    ctx.rectangle(-1200, -1500, 3600, 1300); setc(ctx, light(wall, 0.55)); ctx.fill()
    ctx.move_to(-1200, -200); ctx.line_to(2400, -200); ink(ctx, 8); ctx.stroke()
    # window
    ctx.rectangle(330, 620, 300, 300); fl(ctx, hx('8fe0ff'), 8)
    ellipse(ctx, 560, 690, 34, 34); setc(ctx, hx('fff27a')); ctx.fill()
    ellipse(ctx, 420, 820, 70, 30); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.move_to(480, 620); ctx.line_to(480, 920); ctx.move_to(330, 770); ctx.line_to(630, 770); ink(ctx, 6); ctx.stroke()
    # poster (abstract star)
    ctx.rectangle(400, 380, 160, 180); fl(ctx, hx('8a3cff'), 6); sparkle(ctx, 480, 470, 50, hx('ffd23f'))
    # bedroom door
    x, y, w, h = DOORL
    ctx.rectangle(x - 18, y - 18, w + 36, h + 18); fl(ctx, hx('f2e6d0'), 8)
    ctx.rectangle(x, y, w, h); fl(ctx, hx('c98b55'), 7)
    ellipse(ctx, x + w - 40, y + h * 0.55, 13, 13); fl(ctx, hx('ffd23f'), 4)
    # floor
    ctx.rectangle(-1200, STAND - 60, 3600, 1400); setc(ctx, hx('7a5236')); ctx.fill()
    ctx.move_to(-1200, STAND - 60); ctx.line_to(2400, STAND - 60); ink(ctx, 8); ctx.stroke()
    ellipse(ctx, 560, 1560, 420, 90); setc(ctx, hx('ff6b8a')); ctx.fill_preserve(); ink(ctx, 6); ctx.stroke()   # rug


def bed(ctx, x=30, top=1250, lift=0.0, tower=0.0, f=0):
    """small bed at left edge; lift raises it on a growing tower of stuff"""
    yb = top - lift
    if tower > 0:
        rnd = random.Random(31)
        kinds = [m[0] for m in MESS]
        n = int(6 + 40 * tower)
        for j in range(n):
            item(ctx, kinds[j % len(kinds)], x + 40 + rnd.uniform(0, 320), STAND - 40 - rnd.uniform(0, max(10, lift + 140)), rnd.uniform(-3, 3), 1.0,
                 (hx('ff3b8a'), hx('2fbf5a'), hx('ffd23f'), hx('2f6bff'), hx('8a3cff'))[j % 5])
    ctx.rectangle(x - 40, yb - 220, 50, 330); fl(ctx, hx('3fb5a5'), 7)
    ctx.rectangle(x, yb, 420, 70); fl(ctx, (1, 1, 1), 7)
    ctx.rectangle(x, yb + 70, 420, 40); fl(ctx, hx('c98b55'), 6)
    ctx.new_path(); ctx.move_to(x + 160, yb + 10); ctx.curve_to(x + 160, yb - 50, x + 420, yb - 50, x + 430, yb + 10); ctx.line_to(x + 430, yb + 80); ctx.line_to(x + 150, yb + 80); ctx.close_path()
    fl(ctx, hx('5fd07a'), 6)
    if lift < 10:
        for lx in (x + 20, x + 390):
            ctx.rectangle(lx, yb + 110, 20, STAND - 60 - yb - 110 + 10); fl(ctx, hx('8a5a34'), 5)


def stand(x, k, f, ch, p, ctx):
    return draw(ctx, x, STAND - 186 * k, k, f, ch, p)


def basket(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for j, c in enumerate((hx('ff3b8a'), hx('2fbf5a'), hx('ffd23f'))):
        ellipse(ctx, -50 + j * 50, -30, 40, 24); fl(ctx, c, 4)
    poly(ctx, [(-90, -20), (90, -20), (70, 60), (-70, 60)]); fl(ctx, hx('f5e2b8'), 6)
    for j in range(5):
        ctx.move_to(-70 + j * 35, -14); ctx.line_to(-56 + j * 28, 54); ink(ctx, 3); ctx.stroke()
    ctx.restore()


def pile(ctx, f, h_=1.0, seed=5):
    """avalanche mound covering the floor"""
    rnd = random.Random(seed)
    top = STAND - 60 - 520 * h_
    ctx.new_path(); ctx.move_to(-200, STAND + 600)
    for j in range(13):
        xx = -200 + j * 125
        ctx.line_to(xx, top + 130 * abs(math.sin(j * 1.7)) + abs(xx - 700) * 0.35 * h_)
    ctx.line_to(1400, STAND + 600); ctx.close_path(); fl(ctx, hx('ff8ad0'), 8)
    kinds = [m[0] for m in MESS]
    for j in range(60):
        xx = rnd.uniform(-100, 1200)
        yy = rnd.uniform(top + 60 + abs(xx - 700) * 0.35 * h_, STAND + 400)
        item(ctx, kinds[j % len(kinds)], xx, yy, rnd.uniform(-3, 3), 1.1,
             (hx('ff3b8a'), hx('2fbf5a'), hx('ffd23f'), hx('2f6bff'), hx('8a3cff'))[j % 5])


# ------------------------------------------------------------------ poses
IDLE = dict(lsh=10, lel=-10, rsh=-10, rel=-10)


def shock_p(**kw):
    p = P(eye='shock', mouth='scream', lsh=-160, lel=-30, rsh=160, rel=30); p.update(kw); return p


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    say = f < 52
    bp = P(eye='normal' if f < 50 else 'shock', mouth='smile' if f < 50 else 'scream', head=-6,
           **(IDLE if f < 50 else dict(lsh=-150, lel=-40, rsh=150, rel=40)))
    mp = P(eye='glare', mouth='open' if (f // 5) % 2 == 0 and f < 80 else 'flat', torso=4, lsh=10, lel=-10, rsh=80, rel=-5)
    z = kf(f, [(0, 0.82), (50, 0.9), (56, 1.2), (99, 1.3)], eout)
    ctx.save(); cam(ctx, kf(f, [(0, 480), (56, 330)], eout), kf(f, [(0, 1080), (56, 1080)], eout), z, 0, shake_at(f, [50], 12, 22), f)
    room(ctx, f)
    bed(ctx)
    closet(ctx, f)
    draw_mess(ctx, 0, cleaned=False)
    stand(90, KM, 1, MOM, mp, ctx)
    stand(BX + 80, KB, -1, BOY, bp, ctx)
    ctx.restore()
    if say:
        label(ctx, "CLEAN YOUR ROOM!", 540, 1440, 86, hx('ffe14d'), -0.03, pop(f, 4, 8))
    else:
        label(ctx, "5 MINUTES!", 540, 1440, 130, hx('ff3b5c'), 0.04, pop(f, 52, 56))
    card(ctx, 'p1', f, 2, 98)


def s2(ctx, f):
    lf = f - 100
    # ECU on boy: idea strikes, whip-pan to closet
    pan = eout(pop(lf, 54, 66))
    bp = P(eye='normal' if lf < 26 else 'smug', mouth='flat' if lf < 26 else 'grin', head=-6 + 6 * math.sin(lf * 0.1), **IDLE)
    h = draw(_tmp, BX + 80, STAND - 186 * KB, KB, -1, BOY, bp)
    cx = lerp(h['head'][0], CL[0] + CL[2] / 2, pan)
    cy = lerp(h['head'][1] + 60, CL[1] + 380, pan)
    z = lerp(2.3, 1.25, pan) if lf < 66 else kf(lf, [(66, 1.25), (120, 1.4)], eout)
    ctx.save(); cam(ctx, cx, cy, z, lerp(0, -6, math.sin(pan * math.pi)), 0, f)
    room(ctx, f); bed(ctx)
    gl = pop(lf, 64, 80)
    if gl > 0:
        x, y, w, hh = CL
        g = cairo.RadialGradient(x + w / 2, y + hh / 2, 50, x + w / 2, y + hh / 2, 700)
        g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.7 * gl); g.add_color_stop_rgba(1, 1, 0.95, 0.5, 0)
        ctx.set_source(g); ctx.arc(x + w / 2, y + hh / 2, 700, 0, 7); ctx.fill()
    closet(ctx, f)
    draw_mess(ctx, 0, cleaned=False)
    stand(BX + 80, KB, -1, BOY, bp, ctx)
    if 26 <= lf < 54:
        # eye glint
        sparkle(ctx, h['eyeR'][0] - 20, h['eyeR'][1] - 30, 40 * pop(lf, 26, 32), (1, 1, 1))
    if gl > 0:
        for i in range(5):
            a = lf * 0.08 + i * 1.256
            sparkle(ctx, CL[0] + CL[2] / 2 + math.cos(a) * 260, CL[1] + 420 + math.sin(a) * 380, 34 * gl, hx('fff27a'))
    ctx.restore()
    if lf < 54:
        if lf >= 26:
            label(ctx, "*DING*", 540, 1440, 100, hx('ffe14d'), -0.04, pop(lf, 26, 30))
    else:
        hlines(ctx, lf, 0.35 * (1 - pop(lf, 64, 70)), y0=600, y1=1500)
        if lf >= 66:
            label(ctx, "THE CLOSET.", 540, 1440, 110, hx('8fe9ff'), 0.03, pop(lf, 66, 70))
    card(ctx, 'p2', f, 102, 216)


def s3(ctx, f):
    lf = f - 220
    door = eout(pop(lf, 0, 10)) if lf < 160 else 1.0
    spin = lf >= 12 and f < FLY0 + len(MESS) * FLYDT + FLYD
    done = not spin and lf > 20
    ph = lf * 0.9
    if spin:
        bp = P(eye='shock' if (lf // 6) % 2 else 'normal', mouth='grin', torso=8 * math.sin(ph),
               lsh=120 * math.sin(ph), lel=-40, rsh=-120 * math.sin(ph), rel=-40,
               lhip=25 * math.sin(ph), lkn=-30, rhip=-25 * math.sin(ph), rkn=-30)
        bx = 520 + math.sin(lf * 0.21) * 260
        fac = 1 if math.cos(lf * 0.21) > 0 else -1
    else:
        bp = P(eye='happy', mouth='grin', lsh=-160, lel=-20, rsh=160, rel=20)
        bx, fac = 470, 1
    z = kf(lf, [(0, 0.86), (170, 0.95)], eout)
    ctx.save(); cam(ctx, 560, 1080, z, 0, 3 if spin else 0, f)
    room(ctx, f); bed(ctx)
    closet(ctx, f, open_=door, stuffed=clamp((f - FLY0) / (len(MESS) * FLYDT)))
    draw_mess(ctx, f)
    if spin:
        # dust cloud blur around the kid
        for i in range(7):
            a = lf * 0.5 + i * 0.9
            ellipse(ctx, bx + math.cos(a) * 150, 1260 + math.sin(a) * 160, 70, 50); setc(ctx, (1, 1, 1, 0.55)); ctx.fill()
    stand(bx, KB, fac, BOY, bp, ctx)
    if done:
        for i in range(6):
            sparkle(ctx, 200 + i * 150, 1380 + (i % 2) * 120, 40 * pop(lf, 150, 156) * (0.7 + 0.3 * math.sin(lf * 0.4 + i)), hx('fff27a'))
    ctx.restore()
    if spin:
        hlines(ctx, lf, 0.3, y0=700, y1=1450)
        label(ctx, "*WHOOSH WHOOSH*", 540, 1440, 82, (1, 1, 1), 0.03 * math.sin(lf * 0.5), pop(lf, 14, 18))
    elif done:
        label(ctx, "SPOTLESS!", 540, 1440, 120, hx('5fd07a'), -0.04, pop(lf, 150, 154))
    card(ctx, 'p3', f, 224, 396)


def s4(ctx, f):
    lf = f - 400
    # low angle: kid wrestling the closet door shut
    if lf < 70:
        push = 0.5 + 0.5 * math.sin(lf * 0.35)
        door = lerp(0.35, 0.18, push)
        bx = CL[0] - 70 - door * 160
        bp = P(eye='closed' if push > 0.5 else 'shock', mouth='scream' if push > 0.5 else 'wavy', torso=-14 - 6 * push, head=-6,
               lsh=-80, lel=-20, rsh=-70, rel=-30, lhip=30 + 10 * push, lkn=-10, rhip=-10, rkn=-20)
        by = 0
    elif lf < 92:
        # run-up and body slam
        t = pop(lf, 70, 92)
        door = 0.35 - 0.35 * eout(pop(lf, 86, 92))
        bx = lerp(CL[0] - 320, CL[0] - 70, ein(t))
        by = -math.sin(t * math.pi) * 180
        bp = P(eye='glare', mouth='scream', torso=-30, lsh=-120, lel=-30, rsh=-110, rel=-40, lhip=60, lkn=-90, rhip=20, rkn=-60)
    else:
        door = 0.0
        bx, by = CL[0] - 70, 0
        bp = P(eye='smug' if lf > 104 else 'shock', mouth='grin' if lf > 104 else 'open', torso=-10, lsh=-90, lel=-40, rsh=-160, rel=-20)
    bulge = 1.0 if lf < 92 else max(0.2, 1 - pop(lf, 92, 100)) + 0.25 * math.sin(lf * 0.6) * (1 - pop(lf, 100, 150))
    z = kf(lf, [(0, 1.45), (70, 1.3), (92, 1.3), (98, 1.6), (140, 1.65)], eout)
    ctx.save(); cam(ctx, kf(lf, [(0, 740), (70, 700), (98, 720)], eout), kf(lf, [(0, 1080), (98, 1060)], eout), z, -5, shake_at(lf, [92], 12, 26), f)
    room(ctx, f)
    closet(ctx, f, open_=door, bulge=bulge, stuffed=1.0, poke=1.0 if lf < 92 else 0.0)
    draw(ctx, bx, STAND - 186 * KB + by, KB, -1, BOY, bp)
    if lf < 70:
        sweat_drop(ctx, bx - 60, 760, lf)
    if 92 <= lf < 104:
        burst(ctx, CL[0] + 30, 1100, 140 * (1 - pop(lf, 92, 104)) + 20, seed=lf)
    ctx.restore()
    if lf < 70:
        label(ctx, "*CREAK* *GRUNT*", 540, 1440, 80, (1, 1, 1), 0.03, pop(lf, 4, 8))
    elif lf < 92:
        label(ctx, "HIYAAA!", 540, 1440, 120, hx('ff8a3d'), -0.05, pop(lf, 74, 78))
    else:
        label(ctx, "*CLICK*", 540, 1440, 110, hx('5fd07a'), 0.04, pop(lf, 92, 96))
    card(ctx, 'p4', f, 404, 536)


def sweat_drop(ctx, x, y, t, s=1.0):
    for i in range(2):
        tt = (t * 0.05 + i * 0.5) % 1
        ctx.save(); ctx.translate(x + i * 40 * s, y + tt * 80 * s); ctx.scale(s, s)
        ctx.new_path(); ctx.move_to(0, -26); ctx.curve_to(16, 0, 16, 18, 0, 18); ctx.curve_to(-16, 18, -16, 0, 0, -26); ctx.close_path()
        fl(ctx, hx('8fe9ff'), 4); ctx.restore()


def s5(ctx, f):
    lf = f - 540
    walk_in = eout(pop(lf, 0, 30))
    to_closet = eout(pop(lf, 96, 146))
    mx = lerp(-120, 200, walk_in) + to_closet * 160
    walking = lf < 30 or 96 <= lf < 146
    hold = dict(lsh=50, lel=-70, rsh=50, rel=-70)
    if walking:
        mp = walk(lf * 0.5, eye='happy', mouth='smile', **hold)
    else:
        mp = P(eye='happy', mouth='open' if (lf // 5) % 2 == 0 and lf < 90 else 'grin', **hold)
    panic = lf >= 132
    bp = P(eye='smug' if lf < 96 else ('normal' if not panic else 'shock'), mouth='grin' if lf < 96 else ('wavy' if not panic else 'scream'),
           torso=-8, lsh=-90, lel=-40, rsh=-160 if not panic else 150, rel=-20 if not panic else 30)
    bxx = CL[0] - 70 - to_closet * 20
    z = kf(lf, [(0, 0.9), (40, 1.0), (96, 1.0), (146, 1.12)], eout)
    ctx.save(); cam(ctx, kf(lf, [(0, 440), (96, 500), (146, 640)], eout), 1080, z, 0, shake_at(lf, [132], 10, 14), f)
    room(ctx, f); bed(ctx)
    closet(ctx, f, bulge=0.25 + 0.15 * math.sin(lf * 0.5))
    hm = stand(mx, KM, 1, MOM, mp, ctx)
    fx, fy = hm['front']
    basket(ctx, fx + 30, fy + 10, 0.9)
    stand(bxx, KB, -1, BOY, bp, ctx)
    if 30 <= lf < 90:
        for i in range(5):
            sparkle(ctx, 120 + i * 170, 1360 + (i % 2) * 140, 30 * (0.6 + 0.4 * math.sin(lf * 0.3 + i)), hx('fff27a'))
    if 20 <= lf < 96:
        sweat_drop(ctx, bxx + 40, 680, lf, 0.9)
    ctx.restore()
    if lf < 60:
        label(ctx, "WOW! SO CLEAN!", 540, 1440, 96, hx('5fd07a'), -0.03, pop(lf, 32, 36))
    elif lf < 130:
        label(ctx, "LET ME PUT AWAY", 540, 1400, 74, hx('ffe14d'), 0.02, pop(lf, 62, 66))
        label(ctx, "YOUR LAUNDRY!", 540, 1490, 74, hx('ffe14d'), 0.02, pop(lf, 66, 70))
    else:
        label(ctx, "WAIT, NOOO!", 540, 1440, 120, hx('ff3b5c'), -0.05, pop(lf, 132, 136))
    card(ctx, 'p5', f, 600, 716)


def s6(ctx, f):
    lf = f - 720
    opened = lf >= 24
    door = eout(pop(lf, 18, 26))
    av = eout(pop(lf, 24, 60))
    settle = lf >= 70
    mp = P(eye='happy' if lf < 24 else 'shock', mouth='smile' if lf < 24 else 'scream', lsh=50, lel=-70, rsh=90 if lf < 24 else 160, rel=0 if lf < 24 else 20)
    z = kf(lf, [(0, 1.15), (24, 0.95), (60, 0.85), (70, 1.0), (160, 1.15)], eout)
    ctx.save(); cam(ctx, kf(lf, [(0, 660), (24, 600), (70, 560)], eout), kf(lf, [(0, 1080), (70, 1180)], eout), z, 0, shake_at(lf, [24, 40], 18, 34), f)
    room(ctx, f); bed(ctx)
    closet(ctx, f, open_=door, stuffed=1.0)
    if not settle:
        hm = stand(570, KM, 1, MOM, mp, ctx)
        if lf < 24:
            fx, fy = hm['back']; basket(ctx, fx, fy + 10, 0.9)
        stand(230, KB, 1, BOY, P(eye='shock', mouth='scream', lsh=-150, lel=-40, rsh=150, rel=40), ctx)
    if opened:
        # flying stuff bursting from the closet
        rnd = random.Random(77)
        kinds = [m[0] for m in MESS]
        for j in range(50):
            d0 = rnd.uniform(0, 30)
            t = clamp((lf - 24 - d0) / 24)
            if t <= 0:
                continue
            sx, sy = CL[0] + rnd.uniform(40, 280), CL[1] + rnd.uniform(100, 800)
            ex, ey = rnd.uniform(-100, 900), rnd.uniform(900, 1700)
            item(ctx, kinds[j % len(kinds)], lerp(sx, ex, t), lerp(sy, ey, t) - math.sin(t * math.pi) * 300, rnd.uniform(-3, 3) + t * 6, 1.2,
                 (hx('ff3b8a'), hx('2fbf5a'), hx('ffd23f'), hx('2f6bff'), hx('8a3cff'))[j % 5])
        pile(ctx, f, av)
    if settle:
        # heads pop out of the pile
        up = eout(pop(lf, 80, 92))
        hm = draw(ctx, 470, STAND + 260 - 360 * up, KM, 1, MOM, P(eye='glare', mouth='flat', lsh=-170, lel=0, rsh=10, rel=-10))
        item(ctx, 'sock', hm['head'][0] + 10, hm['head'][1] - 150, 0.3, 1.1, hx('8a3cff'))
        bu = eout(pop(lf, 100, 110))
        draw(ctx, 820, STAND + 300 - 300 * bu, KB, -1, BOY, P(eye='normal', mouth='wavy', head=10, lsh=-170, lel=0))
        pile_front(ctx, f)
    if 24 <= lf < 40:
        burst(ctx, CL[0] + 150, 1000, 300 * (1 - pop(lf, 24, 40)) + 50, seed=lf)
    ctx.restore()
    if lf < 24:
        label(ctx, "*CREAK...*", 540, 1440, 90, (1, 1, 1), 0.03, pop(lf, 4, 8))
    elif lf < 76:
        label(ctx, "AVALANCHE!!!", 540, 1440, 120, hx('ff3b5c'), -0.05 + 0.03 * math.sin(lf), pop(lf, 26, 30))
    elif lf >= 112:
        label(ctx, "CLEAN. IT. PROPERLY.", 540, 1440, 80, hx('ffe14d'), 0.02, pop(lf, 114, 118))
    card(ctx, 'p6', f, 780, 876)


def pile_front(ctx, f):
    # front lip of the pile so popped-up characters look buried
    rnd = random.Random(12)
    ctx.new_path(); ctx.move_to(-200, STAND + 700)
    for j in range(14):
        ctx.line_to(-200 + j * 110, STAND + 30 + 40 * math.sin(j * 2.1))
    ctx.line_to(1400, STAND + 700); ctx.close_path(); fl(ctx, hx('ff8ad0'), 8)
    kinds = [m[0] for m in MESS]
    for j in range(16):
        item(ctx, kinds[(j * 3) % len(kinds)], rnd.uniform(0, 1100), rnd.uniform(STAND + 70, STAND + 260), rnd.uniform(-3, 3), 1.1,
             (hx('ff3b8a'), hx('2fbf5a'), hx('ffd23f'), hx('2f6bff'), hx('8a3cff'))[j % 5])


def s7(ctx, f):
    lf = f - 880
    shove = lf < 70
    rise = eout(pop(lf, 70, 130))
    lift = rise * 1180
    bonk = lf >= 130
    z = kf(lf, [(0, 1.05), (70, 1.0), (130, 0.95)], eout)
    cy = lerp(1150, 120, rise)
    ctx.save(); cam(ctx, 400, cy, z, 0, shake_at(lf, [130], 12, 28), f)
    room(ctx, f)
    bed(ctx, lift=lift, tower=clamp(lf / 70) if lf < 70 else 1.0, f=lf)
    closet(ctx, f)
    if shove:
        # kid on hands and knees stuffing things under the bed, items zipping in
        ph = lf * 0.9
        bp = P(eye='glare', mouth='grin', torso=60, head=-50, lsh=60 + 50 * math.sin(ph), lel=-20, rsh=60 - 50 * math.sin(ph), rel=-20,
               lhip=90, lkn=-90, rhip=80, rkn=-80)
        draw(ctx, 560, STAND - 186 * KB + 90, KB, -1, BOY, bp)
        rnd = random.Random(lf)
        kinds = [m[0] for m in MESS]
        for j in range(3):
            t = ((lf * 3 + j * 11) % 20) / 20
            item(ctx, kinds[(lf // 7 + j) % len(kinds)], lerp(820, 300, t), 1440 - math.sin(t * math.pi) * 120, t * 8, 0.9)
    else:
        # kid lounging on the bed as it rises
        yb = 1250 - lift
        bp = P(rot=-90, eye='happy' if not bonk else 'shock', mouth='grin' if not bonk else 'scream', head=-4,
               lsh=-170, lel=-40, rsh=-60, rel=-80, lhip=4, lkn=-6, rhip=10, rkn=-12)
        draw_hip(ctx, 300, yb - 30, 1.0, 1, BOY, bp)
        if bonk:
            burst(ctx, 360, -200, 120 * (1 - pop(lf, 130, 140)) + 10, seed=lf)
            for i in range(3):
                a = lf * 0.25 + i * 2.1
                sparkle(ctx, 200 + math.cos(a) * 110, yb - 230 + math.sin(a) * 30, 26, hx('fff27a'))
    ctx.restore()
    if shove:
        label(ctx, "*STUFF STUFF STUFF*", 540, 1440, 74, (1, 1, 1), 0.03, pop(lf, 4, 8))
    elif not bonk:
        label(ctx, "UH OH...", 540, 1440, 110, hx('ffe14d'), -0.03, pop(lf, 80, 84))
    else:
        label(ctx, "*BONK!*", 540, 1350, 120, hx('ff3b5c'), -0.05, pop(lf, 130, 134))
        label(ctx, "ROOM: CLEAN.", 540, 1480, 90, hx('5fd07a'), 0.03, pop(lf, 142, 146))
    card(ctx, 'p7', f, 884)


SHOTS = [(0, s1), (100, s2), (220, s3), (400, s4), (540, s5), (720, s6), (880, s7)]


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.25)
    ctx.set_source(g); ctx.paint()
    for c in (100, 166, 220, 400, 470, 492, 540, 720, 744, 880, 1010):
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.5 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/c{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/closet_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
