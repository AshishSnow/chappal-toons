"""'Where's the LID?!' - the leftovers container with no matching lid. Original, general-audience comedy short, 22s.
Hook:   kitchen medium shot: Mom half-buried in a pile of plastic food containers still raining from the open cupboard,
        holding a container + the WRONG lid up, screaming "WHERE'S THE LID?!" + caption "EVERY KITCHEN'S CONTAINER CUPBOARD:".
Beat 1: "Leftovers? EASY." -> opens the cupboard -> *CRASH!* avalanche buries her to the neck "...ow."
        counter macro: lid #1 TOO BIG (slides off), #2 TOO SMALL (sinks into the pasta), #3 "...SQUARE?!" + *NOPE!* stamps.
Beat 2: wide: kitchen floor is a sea of containers, kid in a bowl helmet, Dad hauls in a tower "I found 47 LIDS!" ->
        speed montage *NOPE! NOPE! NOPE!* lids fly -> "...ZERO fit." *cricket*
Turn:   Mom ECU (the one close-up): "There is ALWAYS..." "...a LID!!"
Twist:  PLOT TWIST: THE DOG HAD IT. dog trots in with the glowing lid *AHHH~* -> macro *CLICK!* perfect fit *DING!* "YESSS!!"
        -> Mom proudly puts it away, closes the cupboard "...PERFECT." -> *rumble* -> *CRASH!!* avalanche -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face
from scenes48 import label2
from scenes58 import sweat, twitch, pasta, x_stamp
from scenes65 import dog
from scenes84 import kitchen as _kitchen, eio
import scenes13
from scenes13 import card as _card13

RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
TUBC = [hx('7fd3ff'), hx('ff9ec2'), hx('b8f07a'), hx('ffd86a'), hx('c9a8ff'), hx('ffb27a')]
MATCH = hx('4fb8ff')
MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'), pants=hx('2f4a8a'))
DAD = dict(doodle.DAD, shirt=hx('22b45a'), pants=hx('3d5a9e'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ffc93c'), pants=hx('3d7bff'), shoes=hx('ff3b5c'))
N = 660
FLOOR, GND = 1560, 1590
CX0, CX1, CY0, CY1 = 900, 1300, 600, 960       # upper cupboard
TX0, TX1, TY = 880, 1420, 1300                  # counter
MOMX = 690
KMOM, KDAD, KKID = 1.0, 1.08, 0.82

CAPS = {'p1': [[("EVERY KITCHEN'S", OUT)], [("CONTAINER CUPBOARD:", BLUE)]],
        'p2': [[("PLOT TWIST:", RED)], [("THE DOG ", OUT), ("HAD IT.", ORANGE)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def tub(ctx, x, y, w, h, col, rot=0.0, round_=False, lidcol=None):
    """side-view container, (x, y) = centre"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    if round_:
        poly(ctx, [(-w / 2, -h / 2), (w / 2, -h / 2), (w * 0.4, h / 2), (-w * 0.4, h / 2)]); fl(ctx, col, 4)
    else:
        rect_r(ctx, -w / 2, -h / 2, w, h, min(w, h) * 0.22); fl(ctx, col, 4)
    ctx.move_to(-w * 0.32, -h * 0.25); ctx.line_to(-w * 0.32, h * 0.2); setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(5); ctx.stroke()
    if lidcol is not None:
        rect_r(ctx, -w / 2 - 6, -h / 2 - 12, w + 12, 16, 7); fl(ctx, lidcol, 3)
    ctx.restore()


def flat_lid(ctx, x, y, w, col, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    rect_r(ctx, -w / 2, -9, w, 18, 8); fl(ctx, col, 4)
    rect_r(ctx, w / 2 - 4, -5, 20, 10, 4); fl(ctx, col, 3)        # little tab
    ctx.restore()


def item(ctx, kind, x, y, s, col, rot):
    if kind == 0:
        tub(ctx, x, y, 110 * s, 70 * s, col, rot)
    elif kind == 1:
        tub(ctx, x, y, 90 * s, 80 * s, col, rot, True)
    else:
        flat_lid(ctx, x, y, 120 * s, col, rot)


def tub3(ctx, x, y, r, h, col, food=True):
    """3/4-view round container standing on the counter, (x, y) = bottom centre. returns rim centre y"""
    top = y - h
    ctx.new_path(); ctx.move_to(x - r, top); ctx.line_to(x - r * 0.82, y - r * 0.12)
    ctx.curve_to(x - r * 0.6, y + r * 0.2, x + r * 0.6, y + r * 0.2, x + r * 0.82, y - r * 0.12); ctx.line_to(x + r, top); ctx.close_path()
    fl(ctx, col, 6)
    ctx.move_to(x - r * 0.7, top + h * 0.25); ctx.line_to(x - r * 0.62, y - h * 0.12); setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(9); ctx.stroke()
    ellipse(ctx, x, top, r, r * 0.32); fl(ctx, dark(col, 0.8), 6)
    if food:
        ctx.save(); ellipse(ctx, x, top, r * 0.9, r * 0.27); ctx.clip()
        ellipse(ctx, x, top + r * 0.05, r * 0.85, r * 0.25); setc(ctx, hx('ffd86a')); ctx.fill()
        for k in range(7):
            ctx.new_path(); ctx.arc(x - r * 0.6 + k * r * 0.2, top + 4, r * 0.12, 0.2, math.pi * 1.2)
            setc(ctx, hx('e8a83a')); ctx.set_line_width(4); ctx.stroke()
        for k in range(3):
            ellipse(ctx, x - r * 0.4 + k * r * 0.4, top - 2 + 6 * (k % 2), r * 0.1, r * 0.07); setc(ctx, RED); ctx.fill()
        ctx.restore()
    return top


def lid3(ctx, x, y, r, col, rot=0.0, square=False):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ry = r * 0.32
    for dy, c in ((14, dark(col, 0.8)), (0, col)):
        if square:
            poly(ctx, [(-r, dy), (0, -ry * 1.2 + dy), (r, dy), (0, ry * 1.2 + dy)])
        else:
            ellipse(ctx, 0, dy, r, ry)
        fl(ctx, c, 5)
    if square:
        poly(ctx, [(-r * 0.6, 0), (0, -ry * 0.7), (r * 0.6, 0), (0, ry * 0.7)])
    else:
        ellipse(ctx, 0, 0, r * 0.62, ry * 0.6)
    setc(ctx, (1, 1, 1, 0.45)); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def cupboard(ctx, o=0.0, rattle=0.0, lf=0, stuffed=True):
    sx = rattle * math.sin(lf * 2.7) * 6
    ctx.save(); ctx.translate(sx, 0)
    rect_r(ctx, CX0 - 14, CY0 - 14, CX1 - CX0 + 28, CY1 - CY0 + 28, 10); fl(ctx, hx('ffb86a'), 7)
    ctx.rectangle(CX0, CY0, CX1 - CX0, CY1 - CY0); fl(ctx, hx('8a5a3a'), 5)
    if stuffed and o > 0:
        rnd = random.Random(93)
        for k in range(16):
            item(ctx, rnd.randint(0, 2), rnd.uniform(CX0 + 50, CX1 - 50), CY1 - 30 - (k // 4) * 80 - rnd.uniform(0, 20), 0.9,
                 TUBC[k % 6], rnd.uniform(-0.4, 0.4))
    hw = (CX1 - CX0) / 2
    ang = o * 0.65 * math.pi; c = math.cos(ang); w = max(14, hw * abs(c))
    for side in (-1, 1):
        if side < 0:
            x0 = CX0 if c > 0 else CX0 - w
        else:
            x0 = CX1 - w if c > 0 else CX1
        rect_r(ctx, x0, CY0 - 8 * o, w, CY1 - CY0 + 16 * o, 8); fl(ctx, hx('ffd59a'), 6)
        rect_r(ctx, x0 + w * 0.15, CY0 + 30, w * 0.7, CY1 - CY0 - 60, 8); ink(ctx, 3); ctx.stroke()
        if c > 0:
            kx = x0 + w - 24 if side < 0 else x0 + 24
            ellipse(ctx, kx, (CY0 + CY1) / 2, 11, 11); fl(ctx, GOLD, 3)
    if rattle > 0:
        for k in range(3):
            ctx.move_to(CX0 - 40, CY0 + 80 + k * 90); ctx.line_to(CX0 - 80, CY0 + 70 + k * 90)
            ctx.move_to(CX1 + 40, CY0 + 80 + k * 90); ctx.line_to(CX1 + 80, CY0 + 70 + k * 90)
        ink(ctx, 6); ctx.stroke()
    ctx.restore()


def counter(ctx):
    ctx.rectangle(TX0 + 10, TY, TX1 - TX0 - 20, FLOOR - TY + 10); fl(ctx, hx('9fe0d0'), 6)
    for k in range(3):
        x0 = TX0 + 30 + k * (TX1 - TX0 - 60) / 3
        rect_r(ctx, x0 + 8, TY + 50, (TX1 - TX0 - 60) / 3 - 16, FLOOR - TY - 80, 10); ink(ctx, 4); ctx.stroke()
        ellipse(ctx, x0 + (TX1 - TX0 - 60) / 6, TY + 90, 10, 10); fl(ctx, GOLD, 3)
    rect_r(ctx, TX0 - 10, TY - 24, TX1 - TX0 + 20, 36, 8); fl(ctx, hx('f4f0ea'), 6)
    # little pot plant + cookbook on the far end
    poly(ctx, [(TX1 - 110, TY - 24), (TX1 - 40, TY - 24), (TX1 - 50, TY - 90), (TX1 - 100, TY - 90)]); fl(ctx, hx('ff8a5c'), 4)
    for a in (-0.7, -0.2, 0.3, 0.8):
        ellipse(ctx, TX1 - 75 + 40 * math.sin(a), TY - 110 - 16 * math.cos(a), 13, 32, a); fl(ctx, GREEN, 3)


def kitchen(ctx, lf, o=0.0, rattle=0.0):
    _kitchen(ctx, lf)
    cupboard(ctx, o, rattle, lf)
    counter(ctx)


# ------------------------------------------------------------------ falling + piles
def faller(seed, n, spread=1.0):
    rnd = random.Random(seed)
    return [dict(t0=i * 0.75 + rnd.uniform(0, 0.6), x=rnd.uniform(CX0 + 40, CX1 - 40), y=rnd.uniform(CY0 + 120, CY1 - 20),
                 vx=rnd.uniform(-9, -1.5) * spread, vy=rnd.uniform(-10, -2), vr=rnd.uniform(-0.3, 0.3), kind=rnd.randint(0, 2),
                 col=TUBC[i % 6], s=rnd.uniform(0.8, 1.15), land=GND - rnd.uniform(60, 260)) for i in range(n)]


AVAL = faller(7, 46)


def avalanche(ctx, il, items=AVAL, g=1.7):
    for it in items:
        t = il - it['t0']
        if t < 0:
            continue
        y = it['y'] + it['vy'] * t + 0.5 * g * t * t
        if y > it['land']:
            continue
        item(ctx, it['kind'], it['x'] + it['vx'] * t, y, it['s'], it['col'], it['vr'] * t)


def rain(ctx, lf, n=14, period=26):
    """continuous gentle shower out of the open cupboard (hook)"""
    rnd = random.Random(31)
    for i in range(n):
        t = (lf + i * period / n) % period
        x0 = rnd.uniform(CX0 + 50, CX1 - 50); vx = rnd.uniform(-9, -3); vr = rnd.uniform(-0.3, 0.3)
        item(ctx, rnd.randint(0, 2), x0 + vx * t, CY1 - 40 - 4 * t + 0.5 * 1.7 * t * t, rnd.uniform(0.85, 1.1), TUBC[i % 6], vr * t)


PILE = []
_r = random.Random(4)
for _i in range(150):
    _x = _r.uniform(-1, 1)
    PILE.append((_x, _r.uniform(0, 1), _r.randint(0, 2), TUBC[_i % 6], _r.uniform(-0.6, 0.6), _r.uniform(0.85, 1.15)))
PILE.sort(key=lambda q: q[1])


def pile(ctx, cx, halfw, height, u=1.0):
    """mound of containers centred at cx on the floor; u = how much of it has landed"""
    n = int(len(PILE) * clamp(u))
    for x, h, kind, col, rot, s in PILE[:n]:
        top = height * (1 - x * x) * clamp(u * 1.15)
        item(ctx, kind, cx + x * halfw, GND - 20 - h * top, s, col, rot)


SEA = []
_r = random.Random(9)
for _i in range(120):
    SEA.append((_r.uniform(300, 1700), _r.uniform(0, 1), _r.randint(0, 2), TUBC[_i % 6], _r.uniform(-0.7, 0.7), _r.uniform(0.85, 1.1)))
SEA.sort(key=lambda q: q[1])


def sea(ctx, h=150):
    for x, y, kind, col, rot, s in SEA:
        item(ctx, kind, x, GND + 10 - y * h, s, col, rot)


# ------------------------------------------------------------------ people
def stand(ctx, ch, x, k, p, f_=1, dy=0):
    return draw(ctx, x, GND - 186 * k + dy, k, f_, ch, p)


def mom_hold(ctx, lf, eye='shock', mouth='scream', x=MOMX, lidcol=PINK, shake=1.0):
    sh = math.sin(lf * 1.4) * shake
    d = stand(ctx, MOM, x, KMOM, P(eye=eye, mouth=mouth, lsh=150 + 10 * sh, lel=-20, rsh=165 - 10 * sh, rel=10, head=-4))
    hx_, hy_, R = d['head'][0], d['head'][1], d['R']
    tub(ctx, hx_ + R * 1.9, hy_ - R * 0.9 + 8 * sh, 120, 80, MATCH, 0.15 + 0.1 * sh)
    flat_lid(ctx, hx_ - R * 1.6, hy_ - R * 1.2 - 8 * sh, 70, lidcol, -0.4 - 0.15 * sh)
    return d


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf, z=None):
    z = z or (1.22 + 0.04 * eio(pop(lf, 0, 40)))
    ctx.save(); cam(ctx, 890, 1250, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    kitchen(ctx, lf, 1.0)
    d = mom_hold(ctx, lf)
    pile(ctx, MOMX + 40, 330, 210, 1.0)
    rain(ctx, lf)
    sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.5, lf, 1.0)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"WHERE'S THE LID?!\"", 540, 1440, 120, WHITE, -0.04, t)
    label(ctx, "*CLATTER!*", 540, 640, 90, ORANGE, 0.05, 1 if lf == f else pop(lf, 2, 5))


# ------------------------------------------------------------------ shot 2: the cupboard + lid tries
def crash(ctx, f, il):
    # il 0..75: 0-22 "Leftovers? EASY." ; 22 opens ; 26 *CRASH!* avalanche ; pile to the neck by 55 ; 55 "...ow."
    o = eio(pop(il, 20, 26))
    u = eio(pop(il, 26, 55))
    ctx.save(); cam(ctx, 900, 1240, 1.2, 0, shake_at(il, [26, 34, 42], 9, 7), f)
    kitchen(ctx, il, o)
    if il < 22:
        d = stand(ctx, MOM, MOMX, KMOM, P(eye='smug', mouth='grin', lsh=30, lel=-110, rsh=60, rel=-80, head=-2))
        tub(ctx, d['front'][0] + 40, d['front'][1] - 40, 120, 80, MATCH)
        sparkle(ctx, d['front'][0] + 90, d['front'][1] - 140, 22, GOLD)
    else:
        sc = il >= 26
        d = stand(ctx, MOM, MOMX, KMOM, P(eye='shock' if sc else 'normal', mouth='scream' if sc and il < 55 else ('flat' if sc else 'smile'),
                                              lsh=40, lel=-60, rsh=150, rel=-10, head=-6 if sc else 0))
        if il < 26:
            tub(ctx, d['back'][0] + 20, d['back'][1] - 30, 120, 80, MATCH)
    pile(ctx, MOMX + 30, 360, 250, u)
    if il >= 26:
        avalanche(ctx, il - 26)
    if il >= 55:   # the leftovers land on top of the pile
        tub(ctx, MOMX + 170, GND - 330, 120, 80, MATCH, 0.2)
    ctx.restore()
    if il < 22:
        label2(ctx, "\"Leftovers?", "EASY.\"", WHITE, pop(il, 2, 6), 120, col2=GOLD, y=1440)
    elif il < 55:
        label(ctx, "*CRASH!!*", 540, 600, 140, RED, -0.06, pop(il, 26, 29))
        label(ctx, "*CLATTER CLATTER*", 540, 1460, 90, ORANGE, 0.03, pop(il, 32, 35))
    else:
        label(ctx, "\"...ow.\"", 540, 1450, 130, WHITE, -0.03, pop(il, 55, 58))


TRIES = [  # (t0, kind, colour, label)
    (0, 'big', PINK, "TOO BIG!"),
    (22, 'small', GREEN, "TOO SMALL!"),
    (44, 'square', GOLD, "\"...SQUARE?!\""),
]
MX, MY = 1150, TY - 10


def macro(ctx, f, il, final=False):
    # il 0..66 (3 tries) ; final=True: the matching lid, il 0..60
    ctx.save(); cam(ctx, MX, MY - 120, 2.3 + 0.1 * eio(il / 66), 0, shake_at(il, [8, 30, 52] if not final else [12], 7, 6), f)
    kitchen(ctx, il, 0.0)
    top = tub3(ctx, MX, MY, 120, 110, MATCH)
    if final:
        u = eio(pop(il, 0, 12))
        lid3(ctx, MX, lerp(top - 260, top, u), 124, MATCH)
        if il >= 12:
            for j in range(6):
                a = j * math.pi / 3 + il * 0.05
                sparkle(ctx, MX + 200 * math.cos(a), top - 30 + 90 * math.sin(a), 18 + 6 * math.sin(il * 0.5 + j), GOLD)
    else:
        j = max(k for k in range(3) if TRIES[k][0] <= il)
        t0, kind, col, _ = TRIES[j]
        t = il - t0
        u = eio(pop(t, 0, 8))
        if kind == 'big':
            slide = eio(pop(t, 10, 20))
            lid3(ctx, MX + 160 * slide, lerp(top - 260, top - 6, u) + 200 * slide * slide, 200, col, 0.6 * slide)
        elif kind == 'small':
            sink = eio(pop(t, 10, 18))
            lid3(ctx, MX + 10, lerp(top - 260, top + 4, u) + 16 * sink, 58, col, 0.15 * sink)
        else:
            lid3(ctx, MX, lerp(top - 260, top - 10, u), 120, col, 0.12 + 0.05 * math.sin(t * 0.8), square=True)
    ctx.restore()
    if final:
        label(ctx, "*CLICK!*", 540, 620, 140, CYAN, -0.05, pop(il, 12, 15))
        label(ctx, "\"IT FITS!!\"", 540, 1440, 140, GOLD, 0.03, pop(il, 22, 25))
        if il >= 22:
            rnd = random.Random(il // 2)
            for k in range(22):
                ctx.rectangle(rnd.uniform(0, W), (rnd.uniform(0, H) + il * 22) % H, 18, 30); setc(ctx, (PINK, GOLD, CYAN, GREEN)[k % 4]); ctx.fill()
        return
    t0, kind, col, txt = TRIES[j]
    label(ctx, txt, 540, 1440, 130, WHITE, (-0.04, 0.04, -0.03)[j], pop(il, t0 + 8, t0 + 11))
    if il - t0 >= 12:
        x_stamp(ctx, 540, 760, pop(il, t0 + 12, t0 + 16), 0.6)
        label(ctx, "*NOPE!*", 540, 560, 100, RED, 0.05, pop(il, t0 + 12, t0 + 15))


def s2(ctx, f):
    il = f - 60
    if il < 75:
        crash(ctx, f, il)
    else:
        macro(ctx, f, il - 75)


# ------------------------------------------------------------------ shot 3: the sea of containers
DADX, KIDX = 1330, 930


def lid_stack(ctx, x, y, n, lf=0):
    for k in range(n):
        flat_lid(ctx, x + 6 * math.sin(k * 1.3 + lf * 0.2), y - k * 17, 150, TUBC[k % 6], 0.03 * math.sin(k * 2.1))


def bowl_helmet(ctx, d):
    hx_, hy_ = d['head']; R = d['R']
    ctx.new_path(); ctx.arc(hx_, hy_ - R * 0.3, R * 1.05, math.pi, 2 * math.pi); ctx.close_path(); fl(ctx, hx('ff9ec2'), 5)
    rect_r(ctx, hx_ - R * 1.15, hy_ - R * 0.38, R * 2.3, R * 0.22, 6); fl(ctx, hx('ff7fb0'), 4)


def wide(ctx, f, il):
    # il 0..130: 0-50 Dad hauls in the tower "I found 47 LIDS!" ; 50-95 montage *NOPE!* ; 95+ "...ZERO fit." twitch
    ctx.save(); cam(ctx, 1060, 1260, 1.02 + 0.04 * eio(il / 130), -4 if 50 <= il < 95 else 0, shake_at(il, [52, 64, 76, 88], 4, 4), f)
    kitchen(ctx, il, 1.0)
    walk = eio(pop(il, 0, 22))
    dx = lerp(1650, DADX, walk)
    bob = 10 * abs(math.sin(il * 0.5)) * (1 - walk)
    nstack = 14 if il < 50 else max(0, 14 - int((il - 50) / 3))
    if il < 95:
        dp = P(eye='happy' if il < 50 else 'glare', mouth='grin' if il < 50 else 'open', lsh=150, lel=-60, rsh=150, rel=-60, head=4)
    else:
        dp = P(eye='glare', mouth='flat', lsh=20, lel=10, rsh=-20, rel=-10)
    d = stand(ctx, DAD, dx, KDAD, dp, -1, -bob)
    mp = P(eye='glare' if il >= 50 else 'shock', mouth='open' if 50 <= il < 95 else 'flat', lsh=130, lel=-40, rsh=150, rel=-30)
    m = stand(ctx, MOM, MOMX, KMOM, mp)
    tub(ctx, m['head'][0] + m['R'] * 0.3, m['head'][1] - m['R'] * 1.7, 120, 80, MATCH, -0.2)
    k = stand(ctx, KID, KIDX, KKID, P(eye='happy' if il < 95 else 'glare', mouth='grin' if il < 95 else 'flat',
                                       lsh=160 if il < 95 else 20, lel=0, rsh=150 if il < 95 else -20, rel=0), -1)
    bowl_helmet(ctx, k)
    sea(ctx, 120)
    if nstack:
        lid_stack(ctx, d['head'][0] - d['R'] * 1.5, d['head'][1] + d['R'] * 2.6, nstack, il)
    # flying rejected lids during the montage
    if 50 <= il < 95:
        for j in range(8):
            t = (il - 50 - j * 5)
            if 0 <= t < 16:
                x = lerp(MOMX + 120, MOMX - 500 + 140 * (j % 3), t / 16); y = 900 - 30 * t + 2.4 * t * t
                flat_lid(ctx, x, y, 130, TUBC[j % 6], t * 0.5)
    if il >= 95:
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.7, il, 1.2)
        twitch(ctx, m['head'][0] + m['R'] * 0.9, m['head'][1] - m['R'] * 0.7, il + 7, 1.2)
    ctx.restore()
    if il < 50:
        label2(ctx, "\"I found", "47 LIDS!!\"", WHITE, pop(il, 14, 18), 120, col2=GOLD, y=1440)
    elif il < 95:
        j = (il - 50) // 11
        label(ctx, "*NOPE!*", 540, (560, 640, 600, 680)[j % 4], 120, RED, (-0.08, 0.06, -0.04, 0.08)[j % 4], pop(il, 50 + 11 * j, 53 + 11 * j))
        label(ctx, "\"NOPE! NOPE! NOPE!\"", 540, 1450, 100, WHITE, 0.03, pop(il, 52, 55))
    else:
        label(ctx, "\"...ZERO fit.\"", 540, 1450, 130, WHITE, -0.03, pop(il, 97, 100))
        label(ctx, "*cricket*", 540, 600, 80, GREEN, 0.04, pop(il, 105, 108))


def s3(ctx, f):
    wide(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: Mom ECU (the one close-up)
def s4(ctx, f):
    il = f - 330
    ctx.save(); cam(ctx, 1000, 1000, 1.5, 0, 0, f)
    kitchen(ctx, il, 1.0)
    rain(ctx, il * 0.6, 10, 30)
    ctx.restore()
    ctx.rectangle(0, 0, W, H); setc(ctx, (1, 0.95, 0.85, 0.35)); ctx.fill()
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.07 * eio(il / 70), 0, shake_at(il, [0, 34], 6, 8), f)
    face(ctx, MOM, P(eye='glare', mouth='flat' if il < 34 else 'scream'), 540, 930, 200, 0.0)
    twitch(ctx, 540 + 200 * 0.95, 930 - 200 * 0.7, il, 1.6)
    flat_lid(ctx, 240, 1220, 160, PINK, 0.4 + 0.1 * math.sin(il * 0.6))
    tub(ctx, 840, 1230, 170, 110, MATCH, -0.2)
    ctx.restore()
    if il < 34:
        label(ctx, "\"There is ALWAYS...\"", 540, 1440, 110, WHITE, -0.03, pop(il, 3, 7))
    else:
        label(ctx, "\"...a LID!!\"", 540, 1440, 170, RED, 0.03, pop(il, 34, 37))


# ------------------------------------------------------------------ shot 5: the dog -> click -> crash -> loop
def dog_lid(ctx, x, lf, s=0.85):
    dog(ctx, x, GND + 5, s, -1, lf)
    mx, my = x - 215 * s, GND + 5 - 200 * s
    g = cairo.RadialGradient(mx, my, 10, mx, my, 150)
    g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.75); g.add_color_stop_rgba(1, 1, 0.95, 0.5, 0)
    ctx.set_source(g); ctx.arc(mx, my, 150, 0, 2 * math.pi); ctx.fill()
    flat_lid(ctx, mx - 10, my + 4, 120, MATCH, -0.15)
    for j in range(4):
        sparkle(ctx, mx + (-90, 70, -50, 100)[j], my + (-90, -70, 60, 40)[j], 16 + 6 * math.sin(lf * 0.6 + j), GOLD)


def dog_in(ctx, f, il):
    # il 0..70: card ; dog trots in 0-34 ; family shock ; *AHHH~*
    ctx.save(); cam(ctx, 1070, 1290, 1.05, 0, 0, f)
    kitchen(ctx, il, 1.0)
    sh = il >= 30
    stand(ctx, DAD, DADX + 90, KDAD, P(eye='shock' if sh else 'glare', mouth='open' if sh else 'flat', lsh=20, lel=10, rsh=-20, rel=-10), -1)
    m = stand(ctx, MOM, MOMX + 40, KMOM, P(eye='shock' if sh else 'glare', mouth='open' if sh else 'flat', lsh=130, lel=-40, rsh=40, rel=60))
    tub(ctx, m['head'][0] - m['R'] * 1.8, m['head'][1] - m['R'] * 0.6, 120, 80, MATCH, -0.2)
    k = stand(ctx, KID, KIDX - 20, KKID, P(eye='shock' if sh else 'normal', mouth='open' if sh else 'flat', lsh=40, lel=100, rsh=-40, rel=-100), -1)
    bowl_helmet(ctx, k)
    sea(ctx, 110)
    dog_lid(ctx, lerp(1950, 1330, eio(pop(il, 0, 34))), il)
    ctx.restore()
    card(ctx, 'p2', il, 0, 70)
    if il >= 34:
        label(ctx, "*AHHH~*", 540, 1450, 120, GOLD, -0.03, pop(il, 34, 37))


def put_away(ctx, f, il):
    # il 0..100: 0-22 Mom puts it in, closes ; 22 "...PERFECT." ; 45 *rumble* ; 70 *CRASH!!* avalanche ; 85 "NOT AGAIN!!"
    o = 1 - eio(pop(il, 10, 20)) if il < 70 else eio(pop(il, 70, 74))
    rat = 1.0 if 45 <= il < 70 else 0.0
    ctx.save(); cam(ctx, 950, 1250, 1.2, 0, shake_at(il, [70, 78], 10, 8) + (3 if rat else 0), f)
    kitchen(ctx, il, o, rat)
    if il < 12:
        d = stand(ctx, MOM, MOMX + 60, KMOM, P(eye='happy', mouth='grin', lsh=20, lel=10, rsh=170, rel=-10))
        tub(ctx, d['front'][0] + 40, d['front'][1] - 30, 120, 80, MATCH, 0, False, MATCH)
    elif il < 70:
        st = P(eye='smug', mouth='smile', lsh=-30, lel=-80, rsh=30, rel=80) if il < 45 else P(eye='shock', mouth='flat', lsh=-30, lel=-80, rsh=30, rel=80)
        stand(ctx, MOM, MOMX + 60, KMOM, st)
        if il < 45:
            sparkle(ctx, MOMX + 200, 1060, 24, GOLD)
    else:
        stand(ctx, MOM, MOMX + 60, KMOM, P(eye='shock', mouth='scream', lsh=160, lel=-10, rsh=170, rel=-10))
        pile(ctx, MOMX + 60, 330, 210, eio(pop(il, 70, 96)))
        avalanche(ctx, il - 70)
    ctx.restore()
    if il < 45:
        label(ctx, "\"...PERFECT.\"", 540, 1450, 130, WHITE, -0.03, pop(il, 22, 25))
    elif il < 70:
        label(ctx, "*rumble rumble*", 540, 600, 100, PURPLE, 0.05, pop(il, 45, 48))
        label(ctx, "\"...uh-oh.\"", 540, 1450, 120, WHITE, -0.03, pop(il, 55, 58))
    else:
        label(ctx, "*CRASH!!*", 540, 600, 150, RED, -0.06, pop(il, 70, 73))
        label(ctx, "\"NOT AGAIN!!\"", 540, 1450, 130, WHITE, 0.03, pop(il, 84, 87))


def s5(ctx, f):
    lf = f - 400
    if lf < 70:
        dog_in(ctx, f, lf)
    elif lf < 130:
        macro(ctx, f, lf - 70, final=True)
    elif lf < 230:
        put_away(ctx, f, lf - 130)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (200, s3), (330, s4), (400, s5)]
CUTS = (60, 135, 200, 330, 400, 470, 530, 630)


def render(f):
    import sketch
    sketch.BOIL[0] = f // 4
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.0, 0.05, 0.15, 0.2)
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
                              "-i", "out/no_matching_lid_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
