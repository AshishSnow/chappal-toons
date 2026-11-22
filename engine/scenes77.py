"""'Washing the car with Dad' - original, general-audience comedy short, 22s.
Hook:   Dad soaked mid-scream, the kid's hose blasting him in the face in front of a car. Caption "WASHING THE CAR / WITH DAD:" + "NOT IN MY FACE!!"
Beat 1: "Just a LITTLE soap, buddy." -> kid empties the whole bottle *GLUG GLUG* -> *FWOOMP!!* foam mountain swallows car + Dad, only his eyes "...a LITTLE."
Beat 2: "RINSE TIME!" -> the hose blasts the foam away AND Dad into the bush (legs kicking) -> the red car gleams *DING!*
Beat 3: low-angle hero shot, wet hi-five *SMACK!* "SPARKLING!!" -> reflection close-up in the shiny door "Best. Car wash. EVER."
Twist:  the neighbour walks out of the house: "Wow! Thanks for washing MY car!" -> pan right: their own BLUE car next door, caked in mud, flies + a bird.
        kid: "Dad... OUR car is BLUE."  neighbour drives off *BEEP BEEP* "See you NEXT WEEK!" -> Dad twitch ECU "...next... WEEK?!"
End:    kid at the muddy blue car lifts the hose, sparkle grin "AGAIN?!" -> *FSSSH* -> loops into the hook (Dad soaked by the blue car)."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes60 import car_side
from scenes39 import foam
from scenes55 import bush
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
MUD = hx('7a5230'); MUD2 = hx('5a3a20'); WATER = hx('6fd0ff')
DAD = dict(doodle.DAD, shirt=hx('ffd23f'), pants=hx('3d5a9e'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff5fa8'), pants=hx('2a3a6a'), shoes=hx('3ccfb0'))
NB = dict(doodle.NEIGHBOR, shirt=hx('9b4dff'))
CARRED = hx('ff4a5a'); CARBLUE = hx('3d8bff')
N = 660
FLOOR = 1480
HZ = 1190          # lawn horizon / house bottom
KD, KK = 1.3, 0.95

CAPS = {'p1': [[("WASHING THE CAR", OUT)], [("WITH DAD:", BLUE)]],
        'p2': [[("PLOT TWIST:", RED)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ set
def sky(ctx, lf=0):
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, hx('8fd8ff')); ctx.fill()
    ellipse(ctx, 160, 520, 80, 80); fl(ctx, hx('fff27a'), 6)
    for cx_, cy_ in ((420 + 0.4 * lf, 470), (1500 + 0.3 * lf, 430), (2300, 520), (-500, 460)):
        for dx, r in ((-55, 46), (0, 64), (58, 46)):
            ellipse(ctx, cx_ + dx, cy_, r, r * 0.8); fl(ctx, WHITE, 5)


def house(ctx, cx, col, roof, door=0.0, mine=False):
    """house front, centred at cx, bottom on HZ. door 0..1 opens the door."""
    rect_r(ctx, cx - 440, 640, 880, HZ - 640 + 10, 8); fl(ctx, col, 8)
    for k in range(6):                         # siding lines
        ctx.move_to(cx - 430, 720 + k * 80); ctx.line_to(cx + 430, 720 + k * 80)
    setc(ctx, dark(col, 0.9)); ctx.set_line_width(5); ctx.stroke()
    poly(ctx, [(cx - 500, 660), (cx, 380), (cx + 500, 660)]); fl(ctx, roof, 9)
    ellipse(ctx, cx, 560, 50, 50); fl(ctx, WHITE, 6)     # round attic window
    ctx.move_to(cx - 50, 560); ctx.line_to(cx + 50, 560); ink(ctx, 5); ctx.stroke()
    # window + flower box
    wx = cx - 250
    rect_r(ctx, wx - 120, 780, 240, 200, 12); fl(ctx, hx('dff4ff'), 8)
    ctx.move_to(wx, 780); ctx.line_to(wx, 980); ctx.move_to(wx - 120, 880); ctx.line_to(wx + 120, 880); ink(ctx, 6); ctx.stroke()
    rect_r(ctx, wx - 140, 980, 280, 46, 10); fl(ctx, hx('c96a2a'), 6)
    for k in range(5):
        ellipse(ctx, wx - 110 + k * 55, 968, 22, 22); fl(ctx, (PINK, YEL, RED, PURPLE, ORANGE)[k], 4)
    # door
    dx0 = cx + 150
    rect_r(ctx, dx0, 880, 170, HZ - 880, 10); fl(ctx, hx('3a2a40'), 7)
    if door < 1:
        ctx.save(); ctx.translate(dx0, 0); ctx.scale(1 - 0.8 * door, 1)
        rect_r(ctx, 0, 880, 170, HZ - 880, 10); fl(ctx, hx('ff8a6a') if not mine else hx('3ccfb0'), 7)
        ellipse(ctx, 140, 1040, 10, 10); fl(ctx, GOLD, 3)
        ctx.restore()
    rect_r(ctx, dx0 - 20, HZ - 6, 210, 24, 8); fl(ctx, hx('c96a2a'), 5)       # doormat
    # potted plant by the door
    px = dx0 + 250
    poly(ctx, [(px - 40, HZ - 90), (px + 40, HZ - 90), (px + 30, HZ), (px - 30, HZ)]); fl(ctx, hx('ff8a1f'), 6)
    for a in (-0.5, 0, 0.5):
        ellipse(ctx, px + 50 * math.sin(a), HZ - 150 - 20 * math.cos(a), 26, 60, a); fl(ctx, GREEN, 5)
    # house number plate
    rect_r(ctx, cx + 360 - 50, 700, 70, 60, 8); fl(ctx, WHITE, 5)
    text(ctx, "12" if mine else "14", cx + 345, 732, 40, OUT, ow=0, shadow=False)


def yard(ctx):
    ctx.rectangle(-3000, HZ, 9000, 4000); setc(ctx, hx('6fd06a')); ctx.fill()
    ctx.move_to(-3000, HZ); ctx.line_to(6000, HZ); ink(ctx, 6); ctx.stroke()
    for k in range(-20, 60):                  # grass tufts
        x = k * 97 % 3600 - 800; y = HZ + 40 + (k * 53) % 600
        ctx.move_to(x - 12, y); ctx.line_to(x - 4, y - 22); ctx.line_to(x + 4, y); ctx.line_to(x + 12, y - 18)
    setc(ctx, hx('3fa84a')); ctx.set_line_width(5); ctx.stroke()
    for cx in (540, 1980):                    # driveways
        poly(ctx, [(cx - 380, HZ), (cx + 380, HZ), (cx + 560, 2400), (cx - 560, 2400)]); fl(ctx, hx('c8ccd8'), 7)
        for k in range(3):
            ctx.move_to(cx - 420 - 50 * k, HZ + 120 + 140 * k); ctx.line_to(cx + 420 + 50 * k, HZ + 120 + 140 * k)
        setc(ctx, hx('b0b6c4')); ctx.set_line_width(5); ctx.stroke()
    # picket fence between the houses
    for k in range(9):
        x = 1100 + k * 60
        poly(ctx, [(x, HZ + 10), (x, HZ - 150), (x + 22, HZ - 175), (x + 44, HZ - 150), (x + 44, HZ + 10)]); fl(ctx, WHITE, 5)
    ctx.rectangle(1090, HZ - 110, 560, 22); fl(ctx, WHITE, 4)
    # mailbox
    ctx.rectangle(1010, HZ + 40 - 170, 16, 170); fl(ctx, hx('8a5a3a'), 4)
    rect_r(ctx, 960, HZ + 40 - 230, 120, 70, 30); fl(ctx, hx('3d8bff'), 5)


def world(ctx, lf, door=0.0):
    sky(ctx, lf)
    house(ctx, 540, hx('ffe08a'), hx('ff6b5a'), door)
    house(ctx, 1980, hx('a8e0ff'), hx('8a5ac8'), 0, mine=True)
    yard(ctx)


def mud(ctx, x, g, s, amt=1.0, lf=0):
    """mud splotches over car_side(x, g, s)"""
    ctx.save(); ctx.translate(x, g); ctx.scale(s, s)
    rnd = random.Random(11)
    for k in range(int(26 * amt)):
        if k % 3 == 0:
            px, py = rnd.uniform(-90, 110), rnd.uniform(-310, -230)
        else:
            px, py = rnd.uniform(-290, 290), rnd.uniform(-200, -95)
        r = rnd.uniform(22, 55)
        ellipse(ctx, px, py, r, r * rnd.uniform(0.6, 1.0), rnd.uniform(0, 3)); fl(ctx, MUD if k % 2 else MUD2, 3)
    for k in range(6):                       # drips
        px = -260 + k * 100
        ctx.move_to(px - 14, -110); ctx.line_to(px - 10, -60 - 12 * (k % 3)); ctx.line_to(px + 10, -60 - 12 * (k % 3)); ctx.line_to(px + 14, -110)
        ctx.close_path(); fl(ctx, MUD2, 3)
    ctx.restore()


def flies(ctx, x, y, lf, n=4, r=120):
    for k in range(n):
        a = lf * 0.35 + k * 2 * math.pi / n
        px = x + math.cos(a) * r * (1 + 0.3 * math.sin(lf * 0.2 + k)); py = y + math.sin(a * 1.6) * r * 0.5
        ellipse(ctx, px - 8, py - 12, 10, 7, -0.6); setc(ctx, (1, 1, 1, 0.85)); ctx.fill()
        ellipse(ctx, px + 8, py - 12, 10, 7, 0.6); setc(ctx, (1, 1, 1, 0.85)); ctx.fill()
        ellipse(ctx, px, py, 9, 9); setc(ctx, INK); ctx.fill()


def bird(ctx, x, y, lf):
    hop = abs(math.sin(lf * 0.4)) * 12
    ellipse(ctx, x, y - hop, 40, 32); fl(ctx, hx('ff6b3d'), 5)
    ellipse(ctx, x + 28, y - 28 - hop, 22, 20); fl(ctx, hx('ff6b3d'), 5)
    ellipse(ctx, x + 33, y - 32 - hop, 5, 5); setc(ctx, INK); ctx.fill()
    poly(ctx, [(x + 48, y - 30 - hop), (x + 66, y - 24 - hop), (x + 48, y - 18 - hop)]); fl(ctx, GOLD, 3)


def bucket(ctx, x, y, s=1.0, bub=0.0, lf=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if bub > 0:
        rnd = random.Random(2)
        for k in range(int(10 * bub)):
            r = rnd.uniform(20, 40) + 4 * math.sin(lf * 0.5 + k)
            ellipse(ctx, rnd.uniform(-70, 70), -150 - rnd.uniform(0, 90) * bub, r, r); fl(ctx, WHITE, 4)
    poly(ctx, [(-95, -150), (95, -150), (75, 0), (-75, 0)]); fl(ctx, hx('3ccfb0'), 7)
    ellipse(ctx, 0, -150, 95, 22); fl(ctx, hx('2a9a84'), 6)
    ctx.new_path(); ctx.arc(0, -150, 92, math.pi, 2 * math.pi); ink(ctx, 7); ctx.stroke()
    ctx.restore()


def sponge(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -46, -30, 92, 60, 16); fl(ctx, hx('ffe14a'), 6)
    for px, py in ((-20, -8), (14, 10), (24, -14)):
        ellipse(ctx, px, py, 6, 5); setc(ctx, hx('d8b020')); ctx.fill()
    ctx.restore()


def soap_bottle(ctx, x, y, s=1.0, a=0.0, pour=0.0, lf=0):
    """bottle held at (x, y) (its middle); when pour>0 a goo stream drips from the cap"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -50, -90, 100, 170, 26); fl(ctx, hx('8a3cff'), 6)
    rect_r(ctx, -20, -130, 40, 46, 8); fl(ctx, hx('ffd23f'), 5)
    rect_r(ctx, -36, -40, 72, 60, 10); fl(ctx, WHITE, 4)
    text(ctx, "SOAP", 0, -8, 24, hx('8a3cff'), ow=0, shadow=False)
    tip = ctx.user_to_device(0, -130)
    ctx.restore()
    if pour > 0:
        tx, ty = ctx.device_to_user(*tip)
        ctx.move_to(tx, ty); ctx.curve_to(tx + 6 * math.sin(lf), ty + 60, tx - 6, ty + 120, tx, ty + 170 * pour)
        setc(ctx, hx('c89bff')); ctx.set_line_width(22); ctx.stroke()


def nozzle(ctx, x, y, a, s=1.0):
    """spray gun held at (x, y), barrel pointing at angle a; returns world tip"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -20, -18, 110, 36, 14); fl(ctx, hx('ff8a1f'), 6)
    rect_r(ctx, -24, -10, 40, 70, 12); fl(ctx, hx('ff8a1f'), 6)
    rect_r(ctx, 84, -12, 30, 24, 6); fl(ctx, hx('ffd23f'), 5)
    tip = ctx.user_to_device(118, 0)
    tail = ctx.user_to_device(-8, 60)
    ctx.restore()
    return ctx.device_to_user(*tip), ctx.device_to_user(*tail)


def hose_tail(ctx, x, y, x1, y1):
    ctx.move_to(x, y); ctx.curve_to(x - 40, y + 160, x1 + 120, y1 - 60, x1, y1)
    setc(ctx, INK); ctx.set_line_width(34); ctx.stroke_preserve(); setc(ctx, hx('22b45a')); ctx.set_line_width(22); ctx.stroke()


def stream(ctx, x0, y0, x1, y1, lf, w=30, arc=-80, a=1.0):
    """water jet from (x0,y0) to (x1,y1) with a slight arc + splash at the end"""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + arc
    ctx.move_to(x0, y0); ctx.curve_to(mx, my, mx, my, x1, y1)
    setc(ctx, WATER + (0.95 * a,)); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    for k in range(5):                         # moving highlight dashes
        t = ((lf * 0.09 + k * 0.2) % 1)
        t2 = min(1, t + 0.06)
        def bz(t):
            return ((1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1)
        p, q = bz(t), bz(t2)
        ctx.move_to(*p); ctx.line_to(*q); setc(ctx, (1, 1, 1, 0.9 * a)); ctx.set_line_width(w * 0.3); ctx.stroke()
    rnd = random.Random(int(lf) % 7)
    for k in range(10):                        # splash
        an = rnd.uniform(0, 2 * math.pi); d = rnd.uniform(20, 110)
        ellipse(ctx, x1 + math.cos(an) * d, y1 + math.sin(an) * d * 0.8, rnd.uniform(8, 18), rnd.uniform(10, 22)); setc(ctx, WATER + (0.9 * a,)); ctx.fill()


def drips(ctx, x, y, lf, w=120, n=6):
    for k in range(n):
        yy = y + ((lf * 9 + k * 37) % 220)
        xx = x - w / 2 + (k * 47) % w
        ctx.move_to(xx, yy - 18); ctx.curve_to(xx + 10, yy, xx + 8, yy + 10, xx, yy + 10)
        ctx.curve_to(xx - 8, yy + 10, xx - 10, yy, xx, yy - 18); setc(ctx, WATER + (0.9,)); ctx.fill()


def puddle(ctx, x, y, w):
    ellipse(ctx, x, y, w, w * 0.16); setc(ctx, hx('9fe6ff') + (0.85,)); ctx.fill()
    ellipse(ctx, x - w * 0.3, y - w * 0.03, w * 0.25, w * 0.04); setc(ctx, (1, 1, 1, 0.7)); ctx.fill()


def legs_up(ctx, x, y, lf):
    """Dad's legs sticking up out of a bush, kicking"""
    for side, ph in ((-1, 0), (1, 1.7)):
        a = side * 0.25 + 0.25 * math.sin(lf * 0.6 + ph)
        x1 = x + side * 30 + math.sin(a) * 130; y1 = y - math.cos(a) * 130
        x2 = x1 + math.sin(a * 1.4) * 110; y2 = y1 - math.cos(a * 1.4) * 110
        ctx.move_to(x + side * 30, y); ctx.line_to(x1, y1); ctx.line_to(x2, y2)
        setc(ctx, INK); ctx.set_line_width(62); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
        setc(ctx, DAD['pants']); ctx.set_line_width(48); ctx.stroke()
        ellipse(ctx, x2 + side * 8, y2 - 20, 26, 46, a); fl(ctx, DAD['shoes'], 5)


def eyes_in_foam(ctx, x, y, lf, s=1.0):
    for dx in (-48, 48):
        ellipse(ctx, x + dx * s, y, 34 * s, 40 * s); fl(ctx, WHITE, 5)
        ellipse(ctx, x + dx * s + 4 * math.sin(lf * 0.4), y + 6, 13 * s, 15 * s); setc(ctx, INK); ctx.fill()
    ctx.move_to(x - 80 * s, y - 54 * s); ctx.line_to(x - 20 * s, y - 44 * s)
    ctx.move_to(x + 80 * s, y - 54 * s); ctx.line_to(x + 20 * s, y - 44 * s); ink(ctx, 8); ctx.stroke()


def shine(ctx, x, g, s, t):
    """diagonal glint sweeping across car_side(x, g, s)"""
    if not 0 < t < 1:
        return
    ctx.save(); ctx.translate(x, g); ctx.scale(s, s)
    rect_r(ctx, -320, -330, 640, 300, 50); ctx.clip()
    sx = lerp(-500, 500, t)
    poly(ctx, [(sx, -340), (sx + 60, -340), (sx - 60, -20), (sx - 120, -20)]); setc(ctx, (1, 1, 1, 0.7)); ctx.fill()
    ctx.restore()


# ------------------------------------------------------------------ shot 1: hook (blue muddy car, Dad soaked)
def hook(ctx, f, lf):
    ctx.save(); cam(ctx, 1980, 1090, 1.0 + 0.04 * eio(pop(lf, 0, 54)), 0, 3 + shake_at(lf, [0], 10, 12), f)
    world(ctx, lf)
    car_side(ctx, 2020, 1330, 1.05, CARBLUE)
    mud(ctx, 2020, 1330, 1.05, 0.55)
    puddle(ctx, 2240, FLOOR + 10, 210)
    kx = 1640
    b = draw(ctx, kx, FLOOR - 186 * KK, KK, 1, KID, P(eye='happy', mouth='grin', rsh=100, rel=-20, lsh=80, lel=-30))
    hx_, hy_ = b['front']
    tip, tail = nozzle(ctx, hx_ + 10, hy_ - 4, -0.32, 1.0)
    hose_tail(ctx, tail[0], tail[1], 1440, FLOOR + 140)
    j = 6 * math.sin(lf * 2.2)
    d = draw(ctx, 2240 + j, FLOOR - 186 * KD, KD, -1, DAD, P(eye='shock', mouth='scream', lsh=165, lel=20, rsh=140, rel=30, torso=-14, head=-8))
    hd = d['head']
    stream(ctx, tip[0], tip[1], hd[0] - 20, hd[1] + 20, lf, 30, -60)
    drips(ctx, hd[0], hd[1] + 120, lf, 200, 8)
    sweat(ctx, hd[0] + 120, hd[1] - 120, lf, 1.0)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "*FSSSSHHH!*", 540, 610, 96, CYAN, 0.04, t)
    label2(ctx, "\"NOT IN", "MY FACE!!\"", WHITE, t, 128, col2=YEL, y=1430)


# ------------------------------------------------------------------ shot 2: soap -> foam -> rinse
def soap(ctx, f, il):
    # il 0..70
    boom = il >= 40
    fa = eout(pop(il, 40, 54))
    ctx.save(); cam(ctx, 560, 1090, 1.0 + 0.05 * eio(pop(il, 0, 40)), 0, shake_at(il, [40], 12, 18), f)
    world(ctx, il)
    car_side(ctx, 560, 1330, 1.05, CARRED)
    mud(ctx, 560, 1330, 1.05, 0.2)
    bucket(ctx, 470, FLOOR, 1.0, eout(pop(il, 18, 40)), il)
    kx = 250
    pouring = 14 <= il < 40
    b = draw(ctx, kx, FLOOR - 186 * KK, KK, 1, KID, P(eye='happy', mouth='grin', rsh=120 if pouring else 70, rel=10, lsh=60, lel=-20))
    bx, by = b['front']
    soap_bottle(ctx, bx + 40, by - 40, 0.9, 2.2 if pouring else 0.2, 1.0 if pouring else 0, il)
    dad_p = P(eye='normal', mouth='smile', lsh=150, lel=30, rsh=60, rel=-50) if il < 14 else \
        P(eye='shock', mouth='open', lsh=60, lel=-20, rsh=130, rel=40, torso=-6)
    d = draw(ctx, 860, FLOOR - 186 * KD, KD, -1, DAD, dad_p)
    sponge(ctx, *d['front'], 1.0, 0.3)
    if boom:
        foam(ctx, 600, 1180, 0.25 + 0.75 * fa, il, seed=4, spread=0.9)
        if il >= 50:
            eyes_in_foam(ctx, 860, d['head'][1], il, 1.0)
    ctx.restore()
    if il < 14:
        label2(ctx, "\"Just a LITTLE", "soap, buddy.\"", WHITE, pop(il, 1, 5), 110, col2=YEL, y=1430)
    elif not boom:
        label(ctx, "*GLUG GLUG GLUG*", 540, 520, 96, hx('c89bff'), -0.04, pop(il, 16, 19))
    else:
        label(ctx, "*FWOOMP!!*", 540, 520, 130, WHITE, 0.04, pop(il, 40, 43))
        label(ctx, "\"...a LITTLE.\"", 540, 1440, 120, YEL, -0.03, pop(il, 54, 57))


def rinse(ctx, f, il):
    # il 0..76: hose blasts the foam (and Dad) away; Dad lands in the bush; car gleams
    blast = eout(pop(il, 10, 34))
    ctx.save(); cam(ctx, 600, 1090, 1.0, 0, shake_at(il, [30], 10, 14) + (5 if 10 <= il < 34 else 0), f)
    world(ctx, il)
    car_side(ctx, 560, 1330, 1.05, CARRED)
    bush(ctx, 1000, HZ + 260, 0.9, 1 if 30 <= il < 40 else 0)
    if il >= 34:
        shine(ctx, 560, 1330, 1.05, pop(il, 44, 62))
        for k, (sx, sy) in enumerate(((300, 1020), (720, 1000), (520, 1180), (820, 1150))):
            if il >= 40 + 3 * k:
                sparkle(ctx, sx, sy, 30 + 10 * math.sin(il * 0.5 + k), WHITE)
    bucket(ctx, 470, FLOOR, 1.0)
    # foam shrinking from the left
    if blast < 1:
        ctx.save(); ctx.rectangle(lerp(-200, 1300, blast), -500, 3000, 4000); ctx.clip()
        foam(ctx, 600, 1180, 1.0, il, seed=4, spread=0.9)
        if il < 22:
            eyes_in_foam(ctx, 860, 1000, il, 1.0)
        ctx.restore()
    # Dad flying into the bush
    if 22 <= il < 32:
        t = pop(il, 22, 32)
        ctx.save(); ctx.translate(lerp(860, 1000, t), lerp(1000, 900, t) + 600 * t * t); ctx.rotate(t * 5)
        face(ctx, DAD, P(eye='shock', mouth='scream'), 0, 0, 90, 0)
        ctx.restore()
    if il >= 32:
        legs_up(ctx, 1000, HZ + 60, il)
    kx = 200
    b = draw(ctx, kx, FLOOR - 186 * KK, KK, 1, KID, P(eye='happy', mouth='grin', rsh=100, rel=-20, lsh=80, lel=-30))
    tip, tail = nozzle(ctx, b['front'][0] + 10, b['front'][1] - 4, -0.12, 1.0)
    hose_tail(ctx, tail[0], tail[1], 0, FLOOR + 140)
    if 6 <= il < 36:
        stream(ctx, tip[0], tip[1], lerp(380, 1000, blast), 1200, il, 34, -60)
    ctx.restore()
    if il < 22:
        label(ctx, "\"RINSE TIME!!\"", 540, 1440, 120, WHITE, -0.03, pop(il, 2, 5))
        label(ctx, "*FSSSSHHH!*", 540, 520, 100, CYAN, 0.04, pop(il, 8, 11))
    elif il < 44:
        label(ctx, "*SPLOOSH!*", 540, 520, 120, CYAN, 0.04, pop(il, 30, 33))
    else:
        label(ctx, "*DING!*", 540, 520, 120, YEL, -0.04, pop(il, 44, 47))
        label(ctx, "\"...I'm OKAY!\"", 540, 1440, 110, WHITE, 0.03, pop(il, 50, 53))


def s2(ctx, f):
    lf = f - 54
    if lf < 70:
        soap(ctx, f, lf)
    else:
        rinse(ctx, f, lf - 70)


# ------------------------------------------------------------------ shot 3: hero low angle + reflection
def hero(ctx, f, il):
    # il 0..70: low-angle push-in, hi-five at 30
    ctx.save(); cam(ctx, 560, 1170, 1.1 + 0.08 * eio(pop(il, 0, 70)), -3, shake_at(il, [30], 8, 12), f)
    world(ctx, il)
    rays(ctx, 560, 1100, 300, 1500, il * 0.03, col=(1, 1, 0.8), a=0.3, n=16)
    car_side(ctx, 560, 1330, 1.05, CARRED)
    shine(ctx, 560, 1330, 1.05, pop(il, 4, 26))
    shine(ctx, 560, 1330, 1.05, pop(il, 40, 62))
    for k, (sx, sy) in enumerate(((290, 1030), (700, 990), (520, 1190), (840, 1160), (180, 1180))):
        sparkle(ctx, sx, sy, 26 + 12 * math.sin(il * 0.45 + k * 1.3), WHITE)
    hi = pop(il, 22, 30)
    up_ = il >= 30
    kp = P(eye='happy', mouth='grin', rsh=lerp(60, 165, hi), rel=0, lsh=40, lel=-20)
    dp = P(eye='happy', mouth='grin', lsh=lerp(60, 165, hi), lel=0, rsh=40, rel=-30)
    b = draw(ctx, 380, FLOOR - 186 * KK, KK, 1, KID, kp)
    d = draw(ctx, 760, FLOOR - 186 * KD, KD, -1, DAD, dp)
    hd = d['head']; ellipse(ctx, hd[0] + 40, hd[1] - d['R'] * 0.95, 34, 24, 0.4); fl(ctx, hx('3fa84a'), 4)     # leaf in Dad's hair
    if up_:
        mx = (b['front'][0] + d['front'][0]) / 2; my = min(b['front'][1], d['front'][1])
        t = pop(il, 30, 44)
        rnd = random.Random(8)
        for k in range(14):
            a = rnd.uniform(0, 2 * math.pi); r = 40 + 260 * t
            ellipse(ctx, mx + math.cos(a) * r, my + math.sin(a) * r * 0.7 + 200 * t * t, 12, 16); setc(ctx, WATER + (1 - t,)); ctx.fill()
    ctx.restore()
    if up_:
        label(ctx, "*SMACK!*", 540, 520, 120, YEL, 0.04, pop(il, 30, 33))
    label(ctx, "\"SPARKLING!!\"", 540, 1450, 130, WHITE, -0.03, pop(il, 36, 40))


def reflect(ctx, f, il):
    # il 0..70: close-up on the shiny red door, Dad + kid reflected
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eio(pop(il, 0, 70)), 0, 0, f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, CARRED); ctx.fill()
    ctx.rectangle(-600, 1380, 2400, 30); setc(ctx, dark(CARRED, 0.7)); ctx.fill()
    rect_r(ctx, 700, 1300, 150, 34, 17); fl(ctx, dark(CARRED, 0.6), 4)                  # door handle
    ctx.push_group()
    face(ctx, DAD, P(eye='happy', mouth='grin'), 680, 960, 200, -0.06)
    face(ctx, KID, P(eye='happy', mouth='grin'), 360, 1050, 150, 0.08)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(0.85)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, (1, 0.25, 0.3, 0.22)); ctx.fill()    # red tint
    for k in range(3):                                                                     # glints
        x0 = 120 + k * 300 + 80 * math.sin(il * 0.05 + k)
        poly(ctx, [(x0, 560), (x0 + 50, 560), (x0 - 80, 1360), (x0 - 130, 1360)]); setc(ctx, (1, 1, 1, 0.28)); ctx.fill()
    sparkle(ctx, 880, 720, 40 + 10 * math.sin(il * 0.4), WHITE); sparkle(ctx, 200, 820, 28, WHITE)
    ctx.restore()
    label2(ctx, "\"Best. Car wash.", "EVER.\"", WHITE, pop(il, 4, 8), 112, col2=YEL, y=1460)


def s3(ctx, f):
    lf = f - 200
    if lf < 70:
        hero(ctx, f, lf)
    else:
        reflect(ctx, f, lf - 70)


# ------------------------------------------------------------------ shot 4: twist
def neighbour_out(ctx, f, il):
    # il 0..60: neighbour comes out of the house behind; Dad + kid turn
    ctx.save(); cam(ctx, 640, 1060, 1.0, 0, 0, f)
    world(ctx, il, door=eout(pop(il, 0, 8)))
    car_side(ctx, 560, 1330, 1.05, CARRED)
    sparkle(ctx, 300, 1030, 26, WHITE)
    nx = lerp(780, 650, eio(pop(il, 6, 30)))
    walking = 6 <= il < 30
    nb = draw(ctx, nx, 1370 - 186 * 0.9, 0.9, -1, NB,
              run_pose(il * 0.5, eye='happy', mouth='grin') if walking else P(eye='happy', mouth='grin', rsh=150, rel=30, lsh=40, lel=-60))
    mx_, my_ = nb['back']
    rect_r(ctx, mx_ - 22, my_ - 30, 44, 50, 8); fl(ctx, WHITE, 4)
    look = il >= 22
    b = draw(ctx, 250, FLOOR - 186 * KK, KK, 1, KID, P(eye='shock' if look else 'happy', mouth='open' if look else 'grin', head=-10 if look else 0))
    d = draw(ctx, 960, FLOOR - 186 * KD, KD, -1, DAD, P(eye='shock' if look else 'happy', mouth='flat' if look else 'grin', lsh=50, rsh=40, rel=-40))
    sponge(ctx, *d['front'], 1.0, 0.3)
    ctx.restore()
    label2(ctx, "\"Wow! Thanks for", "washing MY car!\"", WHITE, pop(il, 10, 14), 104, col2=YEL, y=1440)


def reveal(ctx, f, il):
    # il 0..80: whip pan right to their own BLUE car, caked in mud
    t = eio(pop(il, 0, 16))
    ctx.save(); cam(ctx, lerp(640, 1980, t), 1080, lerp(1.0, 1.06, eio(pop(il, 16, 80))), 0, 0, f)
    world(ctx, il)
    car_side(ctx, 560, 1330, 1.05, CARRED)
    car_side(ctx, 1980, 1330, 1.05, CARBLUE)
    mud(ctx, 1980, 1330, 1.05, 1.0)
    flies(ctx, 1980, 1000, il, 5, 160)
    bird(ctx, 1990, 980, il)
    ctx.restore()
    if 0 < t < 1:   # whip-pan blur lines
        for k in range(12):
            y = 300 + k * 130
            ctx.move_to(0, y); ctx.line_to(1080, y); setc(ctx, (1, 1, 1, 0.5 * math.sin(math.pi * t))); ctx.set_line_width(18); ctx.stroke()
    label(ctx, "*bzzz...*", 540, 560, 84, WHITE, 0.03, pop(il, 18, 21))
    label2(ctx, "\"Dad... OUR car", "is BLUE.\"", WHITE, pop(il, 30, 34), 112, col2=CYAN, y=1440)


def s4(ctx, f):
    lf = f - 340
    if lf < 60:
        neighbour_out(ctx, f, lf)
        card(ctx, 'p2', lf, 0)
    else:
        reveal(ctx, f, lf - 60)


# ------------------------------------------------------------------ shot 5: drive-off, Dad twitch, AGAIN?!
def drive_off(ctx, f, il):
    # il 0..50
    ctx.save(); cam(ctx, 1100, 1080, 0.82, 0, 0, f)
    world(ctx, il)
    cx_ = lerp(560, 2100, eio(pop(il, 4, 44)))
    car_side(ctx, cx_, 1330, 1.05, CARRED)
    face(ctx, NB, P(eye='happy', mouth='grin'), cx_ + 105, 1330 - 270, 52, 0)
    ctx.save(); ctx.translate(cx_ - 120, 1310)
    for k in range(4):
        ctx.move_to(-400 - k * 60, -40 + k * 40); ctx.line_to(-200 - k * 60, -40 + k * 40)
    setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(10); ctx.stroke()
    ctx.restore()
    car_side(ctx, 1980, 1330, 1.05, CARBLUE)
    mud(ctx, 1980, 1330, 1.05, 1.0)
    flies(ctx, 1980, 1000, il, 4, 140)
    wv = 30 * math.sin(il * 0.8)
    draw(ctx, 800, FLOOR - 186 * KK, KK, 1, KID, P(eye='normal', mouth='flat', rsh=170 + wv, rel=10))
    d = draw(ctx, 1160, FLOOR - 186 * KD, KD, -1, DAD, P(eye='normal', mouth='grin', rsh=170 + wv, rel=10, lsh=30))
    ctx.restore()
    label(ctx, "*BEEP BEEP!*", 540, 520, 110, YEL, 0.04, pop(il, 4, 7))
    label2(ctx, "\"See you", "NEXT WEEK!\"", WHITE, pop(il, 10, 14), 118, col2=YEL, y=1440)


def dad_ecu(ctx, f, il):
    # il 0..60: the one big face close-up: Dad's frozen grin + twitch
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.1 * eio(pop(il, 0, 60)), 0, 2, f)
    sky(ctx, il)
    ctx.rectangle(-600, 1200, 2400, 1200); setc(ctx, hx('6fd06a')); ctx.fill()
    rays(ctx, 540, 960, 250, 1500, il * 0.02, col=(1, 0.9, 0.6), a=0.3, n=16)
    cx, cy, R = 540, 960, 205
    face(ctx, DAD, P(eye='shock', mouth='grin'), cx + 3 * math.sin(il * 2.5), cy, R, 0.03)
    ellipse(ctx, cx - 0.5 * R, cy - 0.95 * R, 32, 26); setc(ctx, (0.3, 0.6, 0.2)); ctx.fill()   # the leaf
    twitch(ctx, cx + 0.7 * R, cy - 0.75 * R, il, 1.3)
    sweat(ctx, cx - 0.85 * R, cy - 0.5 * R, il, 1.2)
    drips(ctx, cx, cy + 1.2 * R, il, 260, 6)
    ctx.restore()
    label2(ctx, "\"...next...", "WEEK?!\"", WHITE, pop(il, 4, 8), 124, col2=RED, y=1440)


def again(ctx, f, il):
    # il 0..22: kid by the muddy blue car raises the nozzle, sparkle grin
    ctx.save(); cam(ctx, 1840, 1150, 1.25, 0, 0, f)
    world(ctx, il)
    car_side(ctx, 2020, 1330, 1.05, CARBLUE)
    mud(ctx, 2020, 1330, 1.05, 0.9)
    b = draw(ctx, 1640, FLOOR - 186 * KK, KK, 1, KID, P(eye='happy', mouth='grin', rsh=lerp(70, 110, eout(pop(il, 0, 8))), rel=-20, lsh=80, lel=-30))
    tip, tail = nozzle(ctx, b['front'][0] + 10, b['front'][1] - 4, -0.32, 1.0)
    hose_tail(ctx, tail[0], tail[1], 1440, FLOOR + 140)
    for k in range(3):
        sparkle(ctx, 1560 + k * 90, b['head'][1] - 160 - 20 * k, 24 + 8 * math.sin(il * 0.6 + k), YEL)
    ctx.restore()
    label(ctx, "\"AGAIN?!\"", 540, 1440, 140, YEL, -0.04, pop(il, 2, 5))


def s5(ctx, f):
    lf = f - 480
    if lf < 50:
        drive_off(ctx, f, lf)
    elif lf < 110:
        dad_ecu(ctx, f, lf - 50)
    elif lf < 132:
        again(ctx, f, lf - 110)
    else:
        s1(ctx, f, f - 612)


SHOTS = [(0, s1), (54, s2), (200, s3), (340, s4), (480, s5)]
CUTS = (54, 124, 200, 270, 340, 400, 480, 530, 590, 612)


def render(f):
    import sketch
    sketch.BOIL[0] = f // 4
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
    sketch.paper(s)
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/v{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/car_wash_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
