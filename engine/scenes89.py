"""'Shopping with a kid: the sneaky cart' - original, general-audience comedy short, 22s.
Hook:   toy-aisle medium shot: Dad screaming at a shopping cart piled sky-high with toys, kid grinning behind it
        "WHERE did ALL this COME FROM?!" + caption "SHOPPING WITH A KID:"
Beat 1: Dad puts ONE milk carton in the cart "We ONLY need MILK." -> reads his list -> kid sneaks a teddy in *plop*
        -> Dad glances, kid whistles innocently *whistle~*
Beat 2: Dutch-tilt montage: every time Dad reads his list, *plop! plop! plop! plop!* toys fly into the cart
Beat 3: checkout: *BEEP BEEP BEEP* the receipt pours out onto the floor, TOTAL counter spinning "...that's NOT milk."
Turn:   Dad ECU (the one close-up) "Put it ALL... BACK."
Twist:  "PLOT TWIST: DAD FOUND THE TOY CARS." Mom arrives "Did you get the MILK?" -> Dad is crammed in a ride-on toy car
        with a SALE tag *VROOM VROOM* "It was on SALE!" -> kid jumps in, they zoom off *VROOOM!*
        Mom alone hugs a giant plush bunny "...just ONE thing." *plop* -> loop to the hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes37 import teddy, toy_car, ball, block, rocket, toy_pile
from scenes23 import heart
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); TEAL = hx('19b5a5')
METAL = hx('c8d0de'); METAL_D = hx('8a94a8')
DAD = dict(doodle.DAD, shirt=hx('19b5a5'), pants=hx('3d5a9e'))
DAD_R = dict(DAD, skin=hx('f07a6a'))
MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'), pants=hx('2f4a8a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ffc93c'), pants=hx('3d7bff'), shoes=hx('ff3b5c'))
N = 660
GND = 1590
KDAD, KMOM, KKID = 1.1, 1.02, 0.86
DADX, CX, KIDX = 820, 1110, 1420
CS = 1.0                                                     # cart scale

CAPS = {'p1': [[("SHOPPING ", OUT), ("WITH A KID:", PURPLE)]],
        'p2': [[("PLOT TWIST:", RED)], [("DAD FOUND ", OUT), ("THE TOY CARS.", BLUE)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def milk(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-30, -60), (30, -60), (30, 50), (-30, 50)]); fl(ctx, WHITE, 4)
    poly(ctx, [(-30, -60), (0, -90), (30, -60)]); fl(ctx, hx('eef3ff'), 4)
    ctx.rectangle(-30, -20, 60, 34); setc(ctx, hx('5fb8ef')); ctx.fill()
    ellipse(ctx, 0, -3, 12, 9); setc(ctx, WHITE); ctx.fill()
    ctx.restore()


def bunny(ctx, x, y, s=1.0, a=0.0):
    """giant generic plush bunny"""
    C = hx('fbe3f0'); Cp = hx('ff9ccc')
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    for sx in (-1, 1):
        ellipse(ctx, sx * 34, -170, 26, 80, sx * 0.15); fl(ctx, C, 5)
        ellipse(ctx, sx * 34, -165, 12, 56, sx * 0.15); setc(ctx, Cp); ctx.fill()
    ellipse(ctx, 0, 40, 90, 95); fl(ctx, C, 6)
    ellipse(ctx, 0, -70, 78, 68); fl(ctx, C, 6)
    for sx in (-1, 1):
        ellipse(ctx, sx * 28, -78, 9, 12); setc(ctx, INK); ctx.fill()
        ellipse(ctx, sx * 26, -82, 3, 4); setc(ctx, WHITE); ctx.fill()
        ellipse(ctx, sx * 50, -52, 14, 8); setc(ctx, (1, 0.5, 0.6, 0.5)); ctx.fill()
    poly(ctx, [(-8, -58), (8, -58), (0, -48)]); setc(ctx, Cp); ctx.fill()
    ellipse(ctx, 0, 50, 50, 55); setc(ctx, hx('fff6fa')); ctx.fill()
    rect_r(ctx, -40, -14, 80, 22, 10); fl(ctx, hx('7fd0ff'), 3)        # bow-tie ribbon
    ctx.restore()


ITEMS = [('teddy', -50, -250, 0.55, -0.2, None), ('car', 60, -205, 0.55, 0.1, RED), ('ball', -110, -205, 38, 0.0, BLUE),
         ('rocket', 110, -290, 0.5, 0.3, None), ('block', 10, -270, 60, 0.2, GREEN), ('ball', -10, -330, 34, 0.5, PINK),
         ('teddy', 90, -340, 0.5, 0.3, None), ('block', -110, -310, 56, -0.3, ORANGE), ('car', -40, -380, 0.5, -0.2, PURPLE)]


def item(ctx, kind, x, y, s, a, col):
    if kind == 'teddy':
        teddy(ctx, x, y, s, a)
    elif kind == 'car':
        ctx.save(); ctx.translate(x, y); ctx.rotate(a); toy_car(ctx, 0, 30, s, col); ctx.restore()
    elif kind == 'ball':
        ball(ctx, x, y, s, col, a)
    elif kind == 'rocket':
        rocket(ctx, x, y, s, a)
    elif kind == 'block':
        block(ctx, x, y, s, col, a)
    elif kind == 'milk':
        milk(ctx, x, y, s, a)
    elif kind == 'bunny':
        bunny(ctx, x, y, s, a)


def cart(ctx, x, n=0, mountain=0.0, milk_on=True, lf=0, bunny_on=0.0, s=CS):
    """side-view shopping cart; Dad pushes from the left (handle at x-220)."""
    ctx.save(); ctx.translate(x, GND); ctx.scale(s, s)
    # basket back panel
    poly(ctx, [(-190, -380), (200, -380), (160, -170), (-150, -170)]); setc(ctx, (0.85, 0.9, 0.96, 0.5)); ctx.fill()
    # contents
    if milk_on:
        milk(ctx, -60, -250, 0.95)
    for k in range(min(n, len(ITEMS))):
        item(ctx, *ITEMS[k])
    if bunny_on > 0:
        bunny(ctx, 20, -330 - 60 * (1 - eout(bunny_on)), 0.85, 0.1)
    if mountain > 0:
        ctx.save(); ctx.translate(0, -360); ctx.scale(1, mountain)
        toy_pile(ctx, 10, 40, 420, 470, seed=8)
        ctx.restore()
    # front mesh
    ctx.save()
    poly(ctx, [(-190, -380), (200, -380), (160, -170), (-150, -170)]); ctx.clip()
    for k in range(-12, 14):
        ctx.move_to(-200 + k * 32, -390); ctx.line_to(-200 + k * 32 - 24, -160)
    for yy in (-330, -280, -230):
        ctx.move_to(-220, yy); ctx.line_to(220, yy)
    setc(ctx, (*METAL_D, 0.85)); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()
    poly(ctx, [(-190, -380), (200, -380), (160, -170), (-150, -170)]); ink(ctx, 6); ctx.stroke()
    ctx.move_to(-195, -380); ctx.line_to(205, -380); setc(ctx, INK); ctx.set_line_width(14); ctx.stroke_preserve(); setc(ctx, METAL); ctx.set_line_width(8); ctx.stroke()
    # handle
    ctx.move_to(-190, -380); ctx.line_to(-230, -420); setc(ctx, INK); ctx.set_line_width(14); ctx.stroke_preserve(); setc(ctx, METAL); ctx.set_line_width(8); ctx.stroke()
    rect_r(ctx, -262, -432, 64, 26, 12); fl(ctx, RED, 4)
    # lower frame + wheels
    for (a_, b_) in (((-150, -170), (-130, -40)), ((160, -170), (140, -40)), ((-150, -60), (160, -60))):
        ctx.move_to(*a_); ctx.line_to(*b_); setc(ctx, INK); ctx.set_line_width(12); ctx.stroke_preserve(); setc(ctx, METAL); ctx.set_line_width(6); ctx.stroke()
    for wx in (-125, 140):
        ellipse(ctx, wx, -22, 22, 22); fl(ctx, hx('3a3a4a'), 4)
        ctx.move_to(wx, -22); ctx.line_to(wx + 14 * math.cos(lf * 0.6), -22 + 14 * math.sin(lf * 0.6)); setc(ctx, METAL); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def ride_car(ctx, x, lf, s=1.0, f_=1, vib=1.0):
    """kid-size ride-on toy car with a SALE tag (generic, no branding)"""
    ctx.save(); ctx.translate(x, GND + 3 * math.sin(lf * 2.1) * vib); ctx.scale(s * f_, s)
    poly(ctx, [(-200, -60), (-190, -170), (-60, -180), (20, -250), (120, -250), (170, -170), (210, -150), (215, -60)]); fl(ctx, RED, 6)
    poly(ctx, [(30, -240), (110, -240), (150, -175), (0, -175)]); fl(ctx, hx('bfe8ff'), 4)
    ellipse(ctx, 195, -120, 14, 12); fl(ctx, YEL, 3)
    ctx.move_to(-150, -130); ctx.line_to(150, -130); setc(ctx, (1, 1, 1, 0.6)); ctx.set_line_width(6); ctx.stroke()
    for wx in (-130, 140):
        ellipse(ctx, wx, -50, 52, 52); fl(ctx, hx('2a2a3a'), 6)
        ellipse(ctx, wx, -50, 20, 20); fl(ctx, METAL, 3)
        for j in range(3):
            a_ = lf * 0.9 + j * 2.09
            ctx.move_to(wx, -50); ctx.line_to(wx + 40 * math.cos(a_), -50 + 40 * math.sin(a_))
        setc(ctx, METAL_D); ctx.set_line_width(4); ctx.stroke()
    # tag
    ctx.move_to(190, -150); ctx.line_to(240, -110); ink(ctx, 3); ctx.stroke()
    ctx.save(); ctx.translate(250, -85); ctx.rotate(0.25 * math.sin(lf * 0.3))
    poly(ctx, [(-50, -30), (40, -30), (60, 0), (40, 30), (-50, 30)]); fl(ctx, GOLD, 3)
    ctx.restore()
    ctx.restore()
    ctx.save(); ctx.translate(x + 250 * s * f_, GND - 85 * s); ctx.rotate(0.25 * math.sin(lf * 0.3))
    text(ctx, "SALE!", 0, 12, 34 * s, RED, ow=4, shadow=False)
    ctx.restore()


def star_burst(ctx, x, y, r, col, txt, lf):
    pts = []
    for k in range(24):
        a = k * math.pi / 12 + lf * 0.01; rr = r if k % 2 == 0 else r * 0.78
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    poly(ctx, pts); fl(ctx, col, 4)
    text(ctx, txt, x, y + 14, r * 0.5, WHITE, ow=6, shadow=False)


SHELF_X = list(range(160, 2100, 470))


def aisle(ctx, lf):
    wall = hx('dff6ee')
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, wall); ctx.fill()
    for i in range(-20, 40):                                     # soft wall stripes + little stars
        ctx.rectangle(i * 140, -3000, 50, 6000); setc(ctx, dark(wall, 0.965)); ctx.fill()
    rnd = random.Random(89)
    for k in range(26):
        sparkle(ctx, rnd.uniform(0, 2100), rnd.uniform(380, 640), 9, hx('ffd86b'))
    # shelving units full of toys
    for sx in SHELF_X:
        ctx.rectangle(sx, 640, 440, 900); fl(ctx, hx('f2c98a'), 6)
        ctx.rectangle(sx + 14, 654, 412, 872); setc(ctx, hx('e3b06e')); ctx.fill()
        rs = random.Random(sx)
        for row in range(3):
            yy = 900 + row * 230
            ctx.rectangle(sx, yy, 440, 22); fl(ctx, hx('b97a3a'), 4)
            xx = sx + 50
            while xx < sx + 400:
                kind = rs.choice(('teddy', 'ball', 'block', 'car', 'rocket', 'ball'))
                col = rs.choice((RED, BLUE, GREEN, ORANGE, PURPLE, PINK, TEAL))
                if kind == 'teddy':
                    teddy(ctx, xx + 20, yy - 120, 0.62)
                    xx += 120
                elif kind == 'ball':
                    ball(ctx, xx + 12, yy - 40, 38, col); xx += 92
                elif kind == 'block':
                    block(ctx, xx + 10, yy - 34, 64, col); xx += 84
                elif kind == 'car':
                    toy_car(ctx, xx + 50, yy, 0.55, col); xx += 120
                else:
                    rocket(ctx, xx + 14, yy - 66, 0.5); xx += 80
            for tx in (sx + 70, sx + 270):                              # price tags
                rect_r(ctx, tx, yy + 4, 46, 18, 4); setc(ctx, WHITE); ctx.fill()
        # big bunnies on top
        if sx % 940 == 160:
            bunny(ctx, sx + 120, 560, 0.55, -0.08)
    star_burst(ctx, 1600, 760, 70, RED, "SALE", lf)
    # floor
    ctx.rectangle(-3000, GND - 40, 9000, 3000); setc(ctx, hx('eef0f6')); ctx.fill()
    for i in range(-30, 60):
        ctx.move_to(i * 140, GND - 40); ctx.line_to(i * 140 - 180, GND + 600); setc(ctx, hx('d3d9e6')); ctx.set_line_width(4); ctx.stroke()
    for yy in (GND + 60, GND + 200, GND + 380):
        ctx.move_to(-3000, yy); ctx.line_to(6000, yy); setc(ctx, hx('d3d9e6')); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-3000, GND - 40); ctx.line_to(6000, GND - 40); ink(ctx, 6); ctx.stroke()
    # potted plant at the aisle end
    poly(ctx, [(330, GND - 10), (430, GND - 10), (415, GND + 80), (345, GND + 80)]); fl(ctx, hx('e07a4a'), 5)
    for k in range(5):
        a = -math.pi / 2 + (k - 2) * 0.45
        ellipse(ctx, 380 + 70 * math.cos(a), GND - 30 + 80 * math.sin(a), 22, 46, a + math.pi / 2); fl(ctx, GREEN, 4)


# ------------------------------------------------------------------ people
def stand(ctx, ch, x, k, p, f_=1):
    return draw(ctx, x, GND - 186 * k, k, f_, ch, p)


def push_dad(ctx, ch=DAD, eye='normal', mouth='smile', x=DADX, **kw):
    p = P(eye=eye, mouth=mouth, torso=8, lsh=75, lel=-15, rsh=82, rel=-12)
    p.update(kw)
    return stand(ctx, ch, x, KDAD, p)


def kid(ctx, p, x=KIDX, f_=-1):
    return stand(ctx, KID, x, KKID, p, f_)


def fly_item(ctx, idx, u, k_hand, cx=CX):
    kind, dx, dy, s, a, col = ITEMS[idx]
    x0, y0 = k_hand; x1, y1 = cx + dx * CS, GND + dy * CS
    item(ctx, kind, lerp(x0, x1, u), lerp(y0, y1, u) - 260 * 4 * u * (1 - u), s, a + u * 6, col)


def list_paper(ctx, d):
    x, y = d['back']
    ctx.save(); ctx.translate(x + 10, y - 40); ctx.rotate(-0.15)
    rect_r(ctx, -40, -60, 80, 110, 6); fl(ctx, WHITE, 3)
    for j in range(4):
        ctx.move_to(-26, -38 + j * 24); ctx.line_to(26 - 14 * (j % 2), -38 + j * 24)
    setc(ctx, hx('8a94a8')); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    ctx.save(); cam(ctx, 1090, 1210, 1.12 + 0.04 * eio(pop(lf, 0, 40)), 0, 3 + shake_at(lf, [0], 7, 8), f)
    aisle(ctx, lf)
    kid(ctx, P(eye='happy', mouth='grin', lsh=-30, lel=-20, rsh=150, rel=-40, head=-6))
    teddy(ctx, KIDX - 60, GND - 400, 0.5, 0.3)
    d = push_dad(ctx, DAD_R, 'shock', 'scream', lsh=150 + 8 * math.sin(lf * 0.9), lel=-30, rsh=160 + 8 * math.sin(lf * 0.9 + 1), rel=-30, torso=-8)
    cart(ctx, CX, n=len(ITEMS), mountain=1.0, milk_on=False, lf=0)
    sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.6, lf, 1.0)
    twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.9, lf, 0.8)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"WHERE did ALL", "this COME FROM?!\"", WHITE, t, 110, col2=RED, y=1440)


# ------------------------------------------------------------------ shot 2
def only_milk(ctx, f, il):
    # il 0..80: Dad drops milk in (0-10) "We ONLY need MILK." ; 24 Dad reads the list; 36 kid sneaks teddy *plop* (46);
    #           52 Dad glances -> kid freezes, whistles *whistle~*
    ctx.save(); cam(ctx, 1100, 1210, 1.15, 0, shake_at(il, [10], 4, 5), f)
    aisle(ctx, il)
    reading = 24 <= il < 52
    toss = pop(il, 36, 46)
    kp = P(eye='happy', mouth='grin', lsh=20, lel=-20, rsh=lerp(30, 165, eio(pop(il, 28, 36))) if il < 46 else lerp(165, 20, eio(pop(il, 46, 50))), rel=-30, head=-6)
    if il >= 52:
        kp = P(eye='closed', mouth='open', lsh=-20, lel=-140, rsh=20, rel=-140, head=10)
    k = kid(ctx, kp)
    d = push_dad(ctx, DAD, 'happy' if il < 24 else ('normal' if reading else 'glare'), 'grin' if il < 24 else ('flat' if reading else 'flat'),
                 lsh=lerp(140, 75, eio(pop(il, 4, 14))), lel=-20, rsh=82 if not reading else 120, rel=-12 if not reading else -120, head=12 if reading else 0)
    if reading:
        list_paper(ctx, d)
    cart(ctx, CX, n=1 if il >= 46 else 0, milk_on=il >= 10, lf=0)
    if il < 10:
        milk(ctx, lerp(d['back'][0], CX - 60, eio(il / 10)), lerp(d['back'][1], GND - 250, eio(il / 10)), 0.95)
    if 36 <= il < 46:
        fly_item(ctx, 0, eio(toss), k['front'])
    ctx.restore()
    if il < 30:
        label2(ctx, "\"We ONLY", "need MILK.\"", WHITE, pop(il, 4, 8), 120, col2=hx('5fb8ef'), y=1440)
    elif il < 52:
        label(ctx, "*plop*", 540, 660, 110, PURPLE, 0.05, pop(il, 46, 49))
    else:
        label(ctx, "*whistle~*", 540, 660, 110, GREEN, -0.05, pop(il, 52, 55))
        for j in range(2):
            ctx.save(); ctx.translate(780 + 50 * j, 880 - 30 * j - (il - 52) * 2); text(ctx, "~", 0, 0, 70, WHITE, ow=8, shadow=False); ctx.restore()


PLOPS = [6, 18, 30, 42, 54]


def montage(ctx, f, il):
    # il 0..76 Dutch tilt: Dad reads, kid machine-guns toys into the cart; each *plop* Dad looks up -> kid frozen innocent
    rot = -7 if il < 66 else lerp(-7, 0, eio(pop(il, 66, 72)))
    ctx.save(); cam(ctx, 1100, 1210, lerp(1.15, 1.26, eio(il / 76)), rot, shake_at(il, PLOPS, 4, 5), f)
    aisle(ctx, il)
    n = 1 + sum(1 for p_ in PLOPS if il >= p_ + 6)
    cur = [p_ for p_ in PLOPS if p_ <= il < p_ + 6]
    look = any(p_ + 6 <= il < p_ + 10 for p_ in PLOPS)
    for g in (2, 1, 0) if cur else (0,):
        ctx.push_group()
        w = math.sin((il - g) * 2.3)
        if cur:
            kp = P(eye='happy', mouth='grin', torso=-10 * w, lsh=40, lel=-30, rsh=160 - 20 * w, rel=-30 + 20 * w, head=-6)
        else:
            kp = P(eye='closed', mouth='open', lsh=-20, lel=-140, rsh=20, rel=-140, head=10)
        k = kid(ctx, kp, x=KIDX + 12 * w * (g > 0))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(1.0 if g == 0 else 0.25)
    d = push_dad(ctx, DAD, 'shock' if look else 'normal', 'flat', rsh=82 if look else 120, rel=-12 if look else -120, head=0 if look else 12)
    if not look:
        list_paper(ctx, d)
    cart(ctx, CX, n=n, lf=0)
    for p_ in cur:
        fly_item(ctx, PLOPS.index(p_) + 1, eio((il - p_) / 6), k['front'])
    ctx.restore()
    for j, p_ in enumerate(PLOPS):
        if p_ + 6 <= il < p_ + 18:
            label(ctx, "*plop!*", 540 + (-190, 170, -60, 140, -150)[j], (600, 700, 780, 620, 720)[j], 96, PURPLE, (-0.08, 0.07, -0.03, 0.05, 0.06)[j], pop(il, p_ + 6, p_ + 9))
    if il >= 62:
        label2(ctx, "\"...ONLY", "MILK.\"", WHITE, pop(il, 62, 66), 120, col2=hx('5fb8ef'), y=1440)


def s2(ctx, f):
    lf = f - 60
    if lf < 80:
        only_milk(ctx, f, lf)
    else:
        montage(ctx, f, lf - 80)


# ------------------------------------------------------------------ shot 3: checkout
REG_X, REG_Y = 1330, 1220


def checkout(ctx, f, il):
    # il 0..96: low angle at the till: BEEP x many, receipt pours out and piles up; TOTAL spins; 56 Dad "...that's NOT milk."
    ctx.save(); cam(ctx, 1150, 1210, lerp(1.12, 1.2, eio(il / 96)), 0, shake_at(il, [0, 56], 5, 6), f)
    aisle(ctx, il)
    d = stand(ctx, DAD if il < 56 else DAD_R, 900, KDAD, P(eye='normal' if il < 30 else 'shock', mouth='flat' if il < 56 else 'scream',
                                                         lsh=20, lel=-10, rsh=40 if il < 56 else 150, rel=-10 if il < 56 else -40))
    # counter + belt
    rect_r(ctx, 1010, GND - 380, 520, 380, 14); fl(ctx, hx('5a6a8a'), 6)
    rect_r(ctx, 990, GND - 410, 560, 44, 10); fl(ctx, hx('2a2a3a'), 5)
    for j in range(8):                                               # moving belt stripes
        bx = 1000 + ((j * 70 + il * 6) % 540)
        ctx.move_to(bx, GND - 404); ctx.line_to(bx, GND - 372); setc(ctx, hx('4a4a5a')); ctx.set_line_width(5); ctx.stroke()
    # toys sliding along the belt
    for j in range(4):
        kind, _, _, s, a, col = ITEMS[(j + il // 8) % len(ITEMS)]
        item(ctx, kind, 1030 + ((j * 150 + il * 6) % 380), GND - 470, s * 0.9, a, col)
    # register + screen
    rect_r(ctx, REG_X - 110, REG_Y - 40, 220, 160, 14); fl(ctx, hx('dfe6f0'), 5)
    rect_r(ctx, REG_X - 100, REG_Y - 190, 200, 120, 12); fl(ctx, hx('1c2030'), 5)
    tot = int(min(il, 60) ** 2.2 * 3.1 + 12.5 * il)
    text(ctx, "TOTAL", REG_X, REG_Y - 150, 30, hx('7fffb0'), ow=0, shadow=False)
    text(ctx, f"{tot:,}.99", REG_X, REG_Y - 100, 40, hx('7fffb0'), ow=0, shadow=False)
    # receipt pouring down into a pile
    L_ = min(1, il / 60)
    ctx.new_path(); ctx.move_to(REG_X - 40, REG_Y + 10)
    yb = GND - 30
    ctx.line_to(REG_X - 40 + 30 * math.sin(il * 0.5), lerp(REG_Y + 10, yb, L_))
    setc(ctx, INK); ctx.set_line_width(46); ctx.stroke_preserve(); setc(ctx, WHITE); ctx.set_line_width(38); ctx.stroke()
    if il > 20:
        rnd = random.Random(5)
        for j in range(int((il - 20) * 0.9)):
            px = REG_X - 40 + rnd.uniform(-160, 160) * min(1, j / 30 + 0.3); py = yb - rnd.uniform(0, 1) * min(220, j * 3)
            ctx.save(); ctx.translate(px, py); ctx.rotate(rnd.uniform(-1, 1))
            ctx.new_path(); ctx.arc(0, 0, 34, 0.2, 2.8); setc(ctx, INK); ctx.set_line_width(26); ctx.stroke_preserve(); setc(ctx, WHITE); ctx.set_line_width(19); ctx.stroke()
            ctx.restore()
    if il >= 56:
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.9, il, 0.8)
    ctx.restore()
    if il < 56:
        for j in range(3):
            bt = (il + j * 6) % 18
            label(ctx, "*BEEP!*", 540 + (-200, 200, 0)[j], (600, 660, 760)[j], 90, RED, (-0.08, 0.07, 0.02)[j], 1 if bt < 12 else 0)
    else:
        label2(ctx, "\"...that's", "NOT milk.\"", WHITE, pop(il, 56, 60), 120, col2=RED, y=1440)


def s3(ctx, f):
    checkout(ctx, f, f - 216)


# ------------------------------------------------------------------ shot 4: the one close-up
def ecu(ctx, f, il):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eio(il / 70), 0, 2 + shake_at(il, [0, 24], 6, 8), f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('ffd2a0')); ctx.fill()
    rays(ctx, 540, 900, 240, 1500, il * 0.02, col=(1, 1, 1), a=0.35, n=16)
    face(ctx, DAD, P(eye='glare', mouth='flat' if il < 24 else 'scream'), 540, 940, 200, 0.0)
    for j in range(4):
        a = j * 1.57 + il * 0.03
        item(ctx, ('teddy', 'ball', 'rocket', 'block')[j], 540 + 340 * math.cos(a), 960 + 330 * math.sin(a),
             (0.6, 44, 0.55, 64)[j], a, (RED, BLUE, GREEN, ORANGE)[j])
    ctx.restore()
    if il < 24:
        label(ctx, "\"Put it ALL...\"", 540, 1440, 120, WHITE, -0.03, pop(il, 4, 8))
    else:
        label(ctx, "\"...BACK!!\"", 540, 1440, 150, RED, -0.03, pop(il, 24, 27))


def s4(ctx, f):
    ecu(ctx, f, f - 312)


# ------------------------------------------------------------------ shot 5: twist -> loop
def twist(ctx, f, il):
    # il 0..120: Dad + cart with only milk, smug "Just MILK. DONE!"; Mom walks in (0-16) "Did you get the MILK?" (6)
    #            34 pull back: Dad is crammed in a ride-on toy car *VROOM VROOM*; 60 Mom "...HONEY?!"; 86 Dad "It was on SALE!"
    rev = eio(pop(il, 34, 44))
    ctx.save(); cam(ctx, lerp(1110, 1080, rev), lerp(1150, 1210, rev), lerp(1.25, 1.16, rev), 0, shake_at(il, [34], 6, 8), f)
    aisle(ctx, il)
    mx = lerp(1720, 1360, eout(pop(il, 0, 16)))
    m = stand(ctx, MOM, mx, KMOM, P(eye='happy' if il < 34 else 'shock', mouth='smile' if il < 34 else 'open',
                                    lsh=20, lel=-10, rsh=20 if il < 60 else 150, rel=-10 if il < 60 else -40, head=-4), f_=-1)
    vib = 1.0 if il >= 34 else 0.0
    d = stand(ctx, DAD, 880, KDAD * 0.98, P(eye='smug' if il < 60 else ('happy' if il >= 86 else 'shock'), mouth='grin',
                                            lsh=80, lel=-30, rsh=85, rel=-30, torso=6 + 2 * math.sin(il * 2.1) * vib))
    if il >= 34:
        ride_car(ctx, 900, il, 1.0, 1, vib)
    else:
        cart(ctx, 1150, n=0, milk_on=False, lf=0)
    milk(ctx, d['front'][0] + 10, d['front'][1] - 30, 0.9)
    if il >= 86:
        for j in range(3):
            sparkle(ctx, 760 + 90 * j, 1010 - 20 * (j % 2), 14 + 4 * math.sin(il * 0.6 + j), GOLD)
    ctx.restore()
    card(ctx, 'p2', il, 36, 120)
    if il < 34:
        label2(ctx, "\"Did you get", "the MILK?\"", WHITE, pop(il, 6, 10), 110, col2=hx('5fb8ef'), y=1440)
    elif il < 60:
        label(ctx, "*VROOM VROOM*", 540, 1460, 110, RED, -0.03, pop(il, 36, 39))
    elif il < 86:
        label(ctx, "\"...HONEY?!\"", 540, 1440, 140, PINK, -0.03, pop(il, 60, 63))
    else:
        label2(ctx, "\"It was", "on SALE!\"", WHITE, pop(il, 86, 90), 130, col2=GOLD, y=1440)


def zoom_off(ctx, f, il):
    # il 0..50: kid jumps in Dad's lap, they zoom off left *VROOOM!* (14); Mom left with the cart
    ctx.save(); cam(ctx, 1080, 1210, 1.16, 0, shake_at(il, [14], 7, 8), f)
    aisle(ctx, il)
    m = stand(ctx, MOM, 1380, KMOM, P(eye='shock', mouth='open', lsh=20, lel=-10, rsh=-30, rel=-60, head=-4), f_=-1)
    dx = -1400 * eio(pop(il, 14, 40)) ** 1.6
    hop = eio(pop(il, 0, 10))
    d = stand(ctx, DAD, 880 + dx, KDAD * 0.98, P(eye='happy', mouth='grin', lsh=80, lel=-30, rsh=85, rel=-30, torso=-10 * (il >= 14)))
    k = kid(ctx, P(eye='happy', mouth='grin', lsh=160, lel=-10, rsh=170, rel=-10, head=-6), x=lerp(1200, 960, hop) + dx, f_=-1) if il < 10 else \
        stand(ctx, KID, 960 + dx, KKID, P(eye='happy', mouth='open', lsh=160, lel=-10, rsh=170, rel=-10), -1)
    ride_car(ctx, 900 + dx, il * 3, 1.0, 1, 1.5)
    if il >= 14:
        for j in range(6):
            yy = GND - 80 - 60 * j
            ctx.move_to(1100 + dx + 40 * (j % 2), yy); ctx.line_to(1300 + dx + 120 * (j % 3), yy)
        ink(ctx, 6); ctx.stroke()
    ctx.restore()
    if il < 14:
        label(ctx, "\"ME TOO!!\"", 540, 1440, 130, GOLD, -0.03, pop(il, 2, 6))
    else:
        label(ctx, "*VROOOOM!*", 540, 1440, 140, RED, -0.04, pop(il, 14, 17))


def mom_bunny(ctx, f, il):
    # il 0..80: Mom alone, glances left, right ... grabs a giant bunny, hugs it (30) "...just ONE thing." *plop* into the cart (56)
    ctx.save(); cam(ctx, 1240, 1210, lerp(1.2, 1.38, eio(il / 80)), 0, shake_at(il, [56], 5, 5), f)
    aisle(ctx, il)
    look = -1 if (il // 10) % 2 == 0 else 1
    hug = 20 <= il < 52
    m = stand(ctx, MOM, 1300, KMOM, P(eye='smug' if il < 20 else 'happy', mouth='grin' if il < 52 else 'smile',
                                      lsh=150 if hug else 20, lel=-90 if hug else -10, rsh=150 if hug else (lerp(150, 60, eio(pop(il, 52, 56))) if il < 60 else 20), rel=-90 if hug else -10,
                                      head=6 * look if il < 20 else 0), f_=look if il < 20 else -1)
    if il < 20:
        bunny(ctx, 1520, 1300, 0.95, 0.06)
    elif hug:
        bunny(ctx, m['front'][0] - 10, m['front'][1] + 10, 0.95, 0.1 * math.sin(il * 0.5))
        for j in range(3):
            heart(ctx, 1220 + 90 * j, 980 - 20 * (j % 2) - (il - 20) * 1.5, 22, hx('ff3b8a'))
    cart(ctx, 1010, n=0, milk_on=True, lf=0, bunny_on=pop(il, 52, 58) if il >= 52 else 0)
    if 52 <= il < 56:
        bunny(ctx, lerp(m['front'][0], 1030, eio(pop(il, 52, 56))), lerp(m['front'][1], GND - 330, eio(pop(il, 52, 56))), 0.85, 0.1)
    ctx.restore()
    if il < 20:
        label(ctx, "*glance glance*", 540, 660, 96, PURPLE, 0.04, pop(il, 2, 5))
    elif il < 56:
        label2(ctx, "\"...just", "ONE thing.\"", WHITE, pop(il, 24, 28), 120, col2=PINK, y=1440)
    else:
        label(ctx, "*plop*", 540, 660, 110, PURPLE, 0.05, pop(il, 56, 59))


def s5(ctx, f):
    lf = f - 382
    if lf < 120:
        twist(ctx, f, lf)
    elif lf < 166:
        zoom_off(ctx, f, lf - 120)
    elif lf < 248:
        mom_bunny(ctx, f, lf - 166)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (216, s3), (312, s4), (382, s5)]
CUTS = (60, 140, 216, 312, 382, 502, 548, 630)


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
                              "-i", "out/sneaky_cart_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
