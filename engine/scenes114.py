"""'THE MISSING SOCK'. Original, general-audience comedy short, 22s.
Hook:   cosy laundry-room medium shot: Dad holding up ONE striped sock, the laundry basket overflowing, paired socks on the dryer
        -> "WHERE'S THE OTHER ONE?!" + caption 'THE MISSING SOCK:'.
        (rewatch easter egg: a striped sock puppet with button eyes peeks out from behind the dryer the whole time)
Beat 1: "Socks? EASY." -> *pair! pair! pair!* pairs land on the dryer -> the last one alone *cricket* "...only ONE?!"
Beat 2: Dutch-tilt search montage: SEARCH #1 THE BASKET. clothes rain, shirt on his head NOPE! / SEARCH #2 THE DOG. lifts the
        sleepy dog *snore* NOPE! / SEARCH #3 THE DRYER. dives head-first in, legs kicking *BONK!* "...STUCK."
Close-up (the one face shot, POV from inside the dryer drum): lint in hair "Socks don't just..." "...VANISH!!"
Twist:  *hee hee* -> a sock puppet rises behind the dryer "Hello, DAD!" -> the kid pops up, puppets on both hands + a puppet
        row -> PLOT TWIST: THE KID MADE SOCK PUPPETS. -> Dad grabs the striped one *FWIP!* -> *DING!* "FINALLY... A PAIR."
        -> Mom walks in with a heaped basket "Here's the NEXT load!" *FWUMP!* -> Dad buried, pops out with one sock
        -> twitch "...of COURSE." -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face, rays
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes65 import dog
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
MOM = dict(doodle.MOM_G, shirt=hx('3fd6a0'), pants=hx('3d5a9e'), shoes=hx('ffffff'))
DAD = dict(doodle.DAD, shirt=hx('1f8bff'), pants=hx('5a4a8e'), sleeve=0.45)
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ffc93c'), pants=hx('ff5fa8'), shoes=hx('8a3cff'))
N = 660
FLOOR, GND = 1560, 1595
KD, KK, KM = 1.05, 0.85, 1.05
DRX, DRW, DRH = 700, 290, 320       # dryer centre x / width / height (bottom on FLOOR)
DRT = FLOOR - DRH                    # dryer top
WAX = 400                            # washer centre x
BSX = 960                            # basket x
DADX = 1150
DOGX = 1390

# sock colour schemes: (base, stripe)
STRIPE = (hx('ff5f7e'), hx('fff27a'))   # THE missing pair
SOCKS = [(hx('7fe3ff'), hx('1f8bff')), (hx('b48cff'), hx('ffffff')), (hx('3fd6a0'), hx('ffc93c')), (hx('ff8a1f'), hx('ffffff')),
         (hx('ffffff'), hx('ff5f7e')), (hx('ffd23f'), hx('8a3cff'))]

CAPS = {'p1': [[("THE ", OUT), ("MISSING SOCK:", RED)]],
        'p2': [[("PLOT TWIST:", RED)], [("THE KID MADE ", OUT), ("SOCK PUPPETS.", PURPLE)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def sock_path(ctx):
    ctx.new_path()
    ctx.move_to(-24, -90); ctx.line_to(24, -90); ctx.line_to(24, 4)
    ctx.curve_to(60, 4, 86, 14, 86, 34); ctx.curve_to(86, 52, 66, 56, 40, 56)
    ctx.line_to(-4, 56); ctx.curve_to(-26, 56, -24, 30, -24, 10); ctx.close_path()


def sock(ctx, x, y, a=0.0, s=1.0, col=STRIPE, f_=1):
    """L-shaped sock, (x, y) = centre of the leg."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s * f_, s)
    sock_path(ctx); fl(ctx, col[0], 4)
    ctx.save(); sock_path(ctx); ctx.clip()
    for k in range(4):
        ctx.rectangle(-40, -66 + k * 30, 140, 12)
    setc(ctx, col[1]); ctx.fill()
    ctx.rectangle(30, 20, 80, 60); setc(ctx, col[1]); ctx.fill()   # toe
    ctx.restore()
    rect_r(ctx, -28, -98, 56, 20, 8); fl(ctx, col[1], 3)   # cuff
    ctx.restore()


def pair(ctx, x, y, col, s=0.7, a=0.0):
    sock(ctx, x - 16 * s, y, a - 0.1, s, col); sock(ctx, x + 16 * s, y + 6 * s, a + 0.12, s, col)


def puppet(ctx, x, y, s=1.0, col=STRIPE, lf=0, talk=False, f_=1, a=0.0):
    """sock puppet on an arm/hand: (x, y) = bottom of the sleeve."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s * f_, s)
    bob = 6 * math.sin(lf * 0.5)
    ctx.translate(0, bob)
    # body (leg of the sock)
    rect_r(ctx, -34, -170, 68, 170, 30); fl(ctx, col[0], 4)
    ctx.save(); rect_r(ctx, -34, -170, 68, 170, 30); ctx.clip()
    for k in range(4):
        ctx.rectangle(-40, -150 + k * 38, 80, 14)
    setc(ctx, col[1]); ctx.fill(); ctx.restore()
    rect_r(ctx, -40, -18, 80, 24, 8); fl(ctx, col[1], 3)
    # head (toe) bent forward
    ellipse(ctx, 14, -186, 58, 44); fl(ctx, col[0], 4)
    m = 14 if talk and (lf // 4) % 2 == 0 else 4
    ctx.move_to(-10, -170); ctx.curve_to(20, -170 + m, 50, -170 + m, 66, -178); ink(ctx, 5); ctx.stroke()
    for ex in (0, 36):   # button eyes
        ellipse(ctx, ex, -202, 13, 13); fl(ctx, WHITE, 3)
        ellipse(ctx, ex + 3, -201, 6, 6); setc(ctx, INK); ctx.fill()
        ellipse(ctx, ex + 1, -204, 2.4, 2.4); setc(ctx, WHITE); ctx.fill()
    for k in range(3):   # yarn hair
        ctx.move_to(-10 + k * 12, -226); ctx.curve_to(-14 + k * 12, -246, -2 + k * 12, -250, 0 + k * 12, -238)
    setc(ctx, col[1]); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def shirt_blob(ctx, x, y, a, s, col):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-50, -40), (-20, -50), (20, -50), (50, -40), (70, -10), (44, 0), (40, 50), (-40, 50), (-44, 0), (-70, -10)])
    fl(ctx, col, 4)
    ctx.restore()


CLOTH = [hx('ff8fb8'), hx('7fe3ff'), hx('ffd23f'), hx('b48cff'), hx('3fd6a0'), hx('ffffff')]


def basket(ctx, x, full=1.0, lf=0, y=GND):
    """wicker laundry basket on the floor, heaped with clothes."""
    if full > 0:
        rnd = random.Random(31)
        for k in range(int(9 * full)):
            shirt_blob(ctx, x + rnd.uniform(-110, 110), y - 170 - rnd.uniform(0, 70) * full, rnd.uniform(-0.6, 0.6), 0.9, CLOTH[k % 6])
        sock(ctx, x - 60, y - 230 * full - 20, -0.5, 0.55, SOCKS[1])
        sock(ctx, x + 70, y - 210 * full - 20, 0.6, 0.55, SOCKS[2])
    poly(ctx, [(x - 150, y - 170), (x + 150, y - 170), (x + 124, y), (x - 124, y)]); fl(ctx, hx('e0a868'), 5)
    for k in range(1, 4):
        ctx.move_to(x - 150 + 6 * k, y - 170 + 42 * k); ctx.line_to(x + 150 - 6 * k, y - 170 + 42 * k)
    setc(ctx, hx('b97a3e')); ctx.set_line_width(5); ctx.stroke()
    rect_r(ctx, x - 160, y - 186, 320, 30, 12); fl(ctx, hx('c98a4a'), 5)


def dryer(ctx, lf, run=True, lint=0.0):
    x0 = DRX - DRW / 2
    rect_r(ctx, x0, DRT, DRW, DRH, 26); fl(ctx, hx('ffffff'), 5)
    rect_r(ctx, x0 + 10, DRT + 10, DRW - 20, 56, 14); fl(ctx, hx('dfe7f5'), 3)
    ellipse(ctx, x0 + 60, DRT + 38, 18, 18); fl(ctx, hx('ffb3cf'), 3)   # dial
    ctx.move_to(x0 + 60, DRT + 38); ctx.line_to(x0 + 60 + 12 * math.cos(lf * 0.1), DRT + 38 + 12 * math.sin(lf * 0.1)); ink(ctx, 4); ctx.stroke()
    for k in range(3):
        ellipse(ctx, x0 + 150 + k * 32, DRT + 38, 8, 8); setc(ctx, (MINT, GOLD, PINK)[k] if run else hx('c4cfe6')); ctx.fill()
    # round door + window
    cy = DRT + 200
    ellipse(ctx, DRX, cy, 104, 104); fl(ctx, hx('dfe7f5'), 5)
    ellipse(ctx, DRX, cy, 78, 78); fl(ctx, hx('8fb8e6'), 4)
    if run:
        ctx.save(); ellipse(ctx, DRX, cy, 76, 76); ctx.clip()
        for k in range(5):
            a = lf * 0.18 + k * 1.26
            shirt_blob(ctx, DRX + 42 * math.cos(a), cy + 42 * math.sin(a), a, 0.45, CLOTH[k])
        ctx.restore()
    ellipse(ctx, DRX - 30, cy - 30, 22, 12, -0.7); setc(ctx, (1, 1, 1, 0.6)); ctx.fill()
    rect_r(ctx, DRX + 96, cy - 26, 16, 52, 6); fl(ctx, hx('c4cfe6'), 3)


def washer(ctx, lf):
    x0 = WAX - DRW / 2
    rect_r(ctx, x0, DRT, DRW, DRH, 26); fl(ctx, hx('eef3fb'), 5)
    rect_r(ctx, x0 + 10, DRT + 10, DRW - 20, 56, 14); fl(ctx, hx('dfe7f5'), 3)
    ellipse(ctx, x0 + 220, DRT + 38, 18, 18); fl(ctx, hx('7fe3ff'), 3)
    cy = DRT + 200
    ellipse(ctx, WAX, cy, 104, 104); fl(ctx, hx('dfe7f5'), 5)
    ellipse(ctx, WAX, cy, 78, 78); fl(ctx, hx('9fe0ff'), 4)
    ctx.save(); ellipse(ctx, WAX, cy, 76, 76); ctx.clip()
    ctx.move_to(WAX - 80, cy + 10 + 8 * math.sin(lf * 0.3))
    for k in range(9):
        ctx.line_to(WAX - 80 + k * 20, cy + 10 + 8 * math.sin(lf * 0.3 + k * 0.9))
    ctx.line_to(WAX + 80, cy + 90); ctx.line_to(WAX - 80, cy + 90); ctx.close_path(); setc(ctx, hx('4fb8f0')); ctx.fill()
    for k in range(4):
        ellipse(ctx, WAX - 40 + k * 26, cy - 20 - ((lf * 2 + k * 17) % 50), 7, 7); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()
    ctx.restore()


def laundry_room(ctx, lf, door=0.0):
    wall = hx('e9e0ff')
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, wall); ctx.fill()
    rnd = random.Random(114)
    for k in range(80):
        sparkle(ctx, rnd.uniform(-300, 2400), rnd.uniform(300, 1520), 10, dark(wall, 0.92))
    # tiled floor
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('b9d8f0')); ctx.fill()
    for k in range(-30, 60):
        ctx.move_to(k * 120, FLOOR); ctx.line_to(k * 120 - 280, FLOOR + 900)
    for k in range(1, 5):
        ctx.move_to(-3000, FLOOR + k * 60); ctx.line_to(6000, FLOOR + k * 60)
    setc(ctx, hx('9cc0e0')); ctx.set_line_width(4); ctx.stroke()
    rect_r(ctx, -3000, FLOOR - 22, 9000, 24, 4); fl(ctx, WHITE, 4)
    # window with clouds (right)
    rect_r(ctx, 1040, 830, 270, 320, 12); fl(ctx, WHITE, 6)
    ctx.set_source(vgrad(ctx, 0, 848, 0, 1132, [(0, hx('8fd8ff')), (1, hx('d8f4ff'))])); rect_r(ctx, 1058, 848, 234, 284, 8); ctx.fill()
    for cx_, cy_ in ((1120 + (lf * 0.3) % 140, 920), (1230, 1010)):
        ellipse(ctx, cx_, cy_, 36, 16); setc(ctx, WHITE); ctx.fill(); ellipse(ctx, cx_ + 26, cy_ - 8, 24, 14); ctx.fill()
    ctx.move_to(1175, 848); ctx.line_to(1175, 1132); ctx.move_to(1058, 990); ctx.line_to(1292, 990); ink(ctx, 5); ctx.stroke()
    # clothesline with pegged socks across the top
    ctx.move_to(220, 760); ctx.curve_to(600, 820, 900, 820, 1340, 760); ink(ctx, 4); ctx.stroke()
    for k, (t, c) in enumerate(((0.12, SOCKS[0]), (0.3, SOCKS[3]), (0.52, SOCKS[4]), (0.74, SOCKS[5]))):
        px = 220 + 1120 * t; py = 760 + 60 * math.sin(math.pi * t) * 0.9
        sock(ctx, px, py + 70, 0.05 * math.sin(lf * 0.2 + k), 0.55, c)
        rect_r(ctx, px - 6, py - 10, 12, 28, 4); fl(ctx, hx('ffb347'), 2)
    # shelf above the machines: plain detergent bottles, plant, framed picture
    rect_r(ctx, 230, 1110, 640, 20, 6); fl(ctx, hx('c98a52'), 4)
    for k, (c, h) in enumerate(((hx('ff8fb8'), 110), (hx('7fe3ff'), 90), (hx('ffd23f'), 120))):
        rect_r(ctx, 270 + k * 70, 1110 - h, 54, h, 14); fl(ctx, c, 4)
        rect_r(ctx, 284 + k * 70, 1110 - h - 18, 26, 20, 5); fl(ctx, WHITE, 3)
        ellipse(ctx, 297 + k * 70, 1110 - h / 2, 14, 14); fl(ctx, WHITE, 2)
    rect_r(ctx, 560, 1050, 60, 60, 12); fl(ctx, hx('ff8a5c'), 4)
    for a in (-0.8, -0.3, 0.2, 0.7):
        ellipse(ctx, 590 + 40 * math.sin(a), 1030 - 30 * math.cos(a), 12, 28, a); fl(ctx, GREEN, 3)
    rect_r(ctx, 680, 960, 140, 120, 8); fl(ctx, hx('ffcf6a'), 5)
    rect_r(ctx, 694, 974, 112, 92, 4); fl(ctx, hx('fff6e0'), 3)
    ellipse(ctx, 750, 1010, 18, 18); fl(ctx, hx('ffb347'), 3)
    pair(ctx, 750, 1040, SOCKS[2], 0.28)
    # door (far right)
    rect_r(ctx, 1420, 960, 220, FLOOR - 960, 10); fl(ctx, WHITE, 5)
    ctx.rectangle(1440, 980, 180, FLOOR - 980); setc(ctx, hx('ffd9b8')); ctx.fill()
    ww = 180 * (1 - 0.85 * door)
    ctx.rectangle(1440, 980, ww, FLOOR - 980); fl(ctx, hx('ffb3cf'), 5)
    # rug + dog bed
    ellipse(ctx, 980, FLOOR + 120, 520, 70); fl(ctx, hx('ffd0e0'), 5)
    ellipse(ctx, 980, FLOOR + 120, 420, 48); setc(ctx, hx('ffe6ef')); ctx.fill()


def dogbed(ctx, x=DOGX, dogon=True, lf=0):
    ellipse(ctx, x, GND - 10, 150, 40); fl(ctx, hx('b98cff'), 5)
    ellipse(ctx, x, GND - 18, 116, 22); setc(ctx, hx('e2d0ff')); ctx.fill()
    if dogon:
        dog(ctx, x - 20, GND - 6, 0.42, -1, lf, sleep=True)


# ------------------------------------------------------------------ people
def stand(ctx, ch, x, k, p, f_=1, g=GND):
    return draw(ctx, x, g - 186 * k, k, f_, ch, p)


def dad_up(ctx, x, lf, eye='shock', mouth='scream', jig=True, sockup=True):
    j = 6 * math.sin(lf * 1.2) if jig else 0
    d = stand(ctx, DAD, x, KD, P(eye=eye, mouth=mouth, lsh=-30, lel=-120, rsh=-125, rel=-15, torso=-4 + j * 0.3, head=6 + j * 0.4), -1)
    if sockup:
        sock(ctx, max(d['front'], d['back'])[0] + 10, max(d['front'], d['back'])[1] - 60, 0.1 * math.sin(lf * 0.6), 0.85, STRIPE)
    return d


def peek_puppet(ctx, lf):
    """easter egg: the missing striped sock as a puppet peeking from behind the dryer"""
    up_ = 40 + 20 * max(0, math.sin(lf * 0.08))
    puppet(ctx, DRX - DRW / 2 + 40, DRT + 120 - up_, 0.55, STRIPE, lf, f_=-1, a=-0.15)


def machines(ctx, lf, run=True, peek=True, dryer_top=3):
    if peek:
        peek_puppet(ctx, lf)
    washer(ctx, lf); dryer(ctx, lf, run)
    for k in range(dryer_top):   # paired socks on top of the dryer
        pair(ctx, DRX - 90 + k * 90, DRT - 34, SOCKS[k], 0.42)


# ------------------------------------------------------------------ shot 1: hook
def hook_scene(ctx, lf):
    laundry_room(ctx, lf)
    machines(ctx, lf)
    dogbed(ctx, lf=lf)
    basket(ctx, BSX)
    d = dad_up(ctx, DADX, lf)
    sweat(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.5, lf, 0.9)
    return d


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    z = 1.12 + 0.03 * eio(pop(lf, 0, 54))
    ctx.save(); cam(ctx, 900, 1300, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    hook_scene(ctx, lf)
    ctx.restore()
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"WHERE'S THE", "OTHER ONE?!\"", WHITE, t, 116, col2=ORANGE, y=1440)


# ------------------------------------------------------------------ shot 2: easy pairing -> one left
def s2(ctx, f):
    il = f - 60   # 0..90
    z = 1.2 + 0.1 * eio(il / 90)
    cx = lerp(900, 960, eio(il / 90))
    ctx.save(); cam(ctx, cx, 1300, z, 0, shake_at(il, [62], 6, 8), f)
    laundry_room(ctx, il + 60)
    npair = 0 if il < 24 else min(3, 1 + (il - 24) // 10)
    machines(ctx, il, dryer_top=npair)
    dogbed(ctx, lf=il)
    basket(ctx, BSX, 1.0 - 0.25 * npair)
    if il < 24:
        d = stand(ctx, DAD, DADX, KD, P(eye='happy', mouth='grin', lsh=-30, lel=-120, rsh=-30, rel=-120, head=-6), -1)
    elif il < 56:
        ph = ((il - 24) % 10) / 10
        d = stand(ctx, DAD, DADX, KD, P(eye='happy', mouth='grin', lsh=-30, lel=-120, rsh=60 + 80 * ph, rel=-40, head=-4, torso=-6), -1)
        sock(ctx, d['front'][0], d['front'][1] - 20, ph * 2, 0.5, SOCKS[min(2, npair)])
    else:
        d = dad_up(ctx, DADX, il, eye='shock' if il >= 62 else 'normal', mouth='open' if il >= 62 else 'flat', jig=False)
    ctx.restore()
    if il < 24:
        label2(ctx, "\"Socks?", "EASY.\"", WHITE, pop(il, 1, 5), 120, col2=MINT, y=1440)
    elif il < 56:
        k = (il - 24) // 10
        label(ctx, ("*pair!*", "*pair!*", "*pair!*", "*pair!*")[k], 540, 640 + 0 * k, 100, (CYAN, GOLD, MINT, PINK)[k], (-0.06, 0.05, -0.03, 0.04)[k], pop(il, 24 + 10 * k, 27 + 10 * k))
    else:
        label(ctx, "*cricket*", 540, 640, 80, hx('9dffb0'), 0.04, pop(il, 56, 60))
        if il >= 62:
            label(ctx, "\"...only ONE?!\"", 540, 1440, 116, WHITE, -0.03, pop(il, 62, 66))


# ------------------------------------------------------------------ shot 3: the search montage (Dutch tilt)
SRCH = [("SEARCH #1:", "THE BASKET."), ("SEARCH #2:", "THE DOG."), ("SEARCH #3:", "THE DRYER.")]


def nope(ctx, t):
    if t <= 0:
        return
    s = 1.6 - 0.6 * eout(min(1, t * 1.5))
    ctx.save(); ctx.translate(540, 1080); ctx.rotate(-0.18); ctx.scale(s, s)
    rect_r(ctx, -230, -70, 460, 140, 20); setc(ctx, (1, 1, 1, 0.92)); ctx.fill_preserve(); setc(ctx, RED); ctx.set_line_width(12); ctx.stroke()
    text(ctx, "NOPE!", 0, 40, 120, RED, ow=0)
    ctx.restore()


def s3(ctx, f):
    il = f - 150   # 0..150
    i, c = min(2, il // 50), il - 50 * min(2, il // 50)
    rot = (7, -7, 7)[i]
    tx = (980, 1250, 820)[i]
    ctx.save(); cam(ctx, tx, 1300, 1.25, rot, shake_at(c, [10] if i == 0 else [30] if i == 2 else [], 8, 16), f)
    laundry_room(ctx, il + 150)
    if i == 0:   # dump the basket over his head
        machines(ctx, c, dryer_top=3); dogbed(ctx, lf=c)
        tip = eio(pop(c, 2, 10))
        d = stand(ctx, DAD, DADX - 100, KD, P(eye='glare' if c < 10 else 'shock', mouth='grin' if c < 10 else 'open',
                                              lsh=170 * tip, lel=-10, rsh=170 * tip, rel=-10, head=4), -1)
        ctx.save(); ctx.translate(d['head'][0], d['head'][1] - d['R'] * 1.2 - 60 * tip); ctx.rotate(math.pi * tip)
        basket(ctx, 0, 0.0, y=90); ctx.restore()
        if c >= 10:
            rnd = random.Random(5)
            for k in range(10):
                ph = clamp((c - 10) / 24 + rnd.uniform(-0.2, 0.1))
                shirt_blob(ctx, d['head'][0] + rnd.uniform(-260, 260) * ph, d['head'][1] - 60 + 360 * ph, ph * 4 + k, 0.8, CLOTH[k % 6])
            shirt_blob(ctx, d['head'][0], d['head'][1] - d['R'] * 0.9, 0.1, 1.0, CLOTH[0])   # shirt on his head
    elif i == 1:  # lift the sleepy dog
        machines(ctx, c, dryer_top=3); basket(ctx, BSX, 0.3)
        lift = eio(pop(c, 4, 16))
        dogbed(ctx, dogon=False)
        d = stand(ctx, DAD, DOGX - 150, KD, P(eye='happy' if c < 28 else 'shock', mouth='grin' if c < 28 else 'open',
                                              lsh=70 + 50 * lift, lel=-30, rsh=80 + 50 * lift, rel=-30, head=-4), 1)
        dog(ctx, DOGX - 10, GND - 6 - 210 * lift, 0.42, -1, c, sleep=True)
        if lift > 0.5:
            for k in range(3):
                ellipse(ctx, DOGX - 30 + k * 40, GND - 30 - 210 * lift + 26 * math.sin(c * 0.3 + k), 14, 14); fl(ctx, WHITE, 2)
    else:         # dive into the dryer
        machines(ctx, c, run=False, dryer_top=3, peek=False); dogbed(ctx, lf=c); basket(ctx, BSX, 0.3)
        dive = eio(pop(c, 4, 20))
        if c < 20:
            d = stand(ctx, DAD, lerp(DADX - 80, DRX + 220, dive), KD, P(eye='glare', mouth='grin', lsh=-150 + 0 * dive, lel=0, rsh=-150, rel=0,
                                                                            torso=-40 * dive, head=-10, rot=-30 * dive), -1)
        else:   # only legs + bum sticking out of the door, kicking
            kick = 20 * math.sin(c * 0.9)
            cy = DRT + 200
            for side, kk in ((-1, kick), (1, -kick)):
                ctx.save(); ctx.translate(DRX + 70, cy + 14 * side); ctx.rotate(math.radians(-8 + kk * side * 0.6))
                rect_r(ctx, 0, -24, 200, 48, 22); fl(ctx, DAD['pants'], 5)
                rect_r(ctx, 186, -30, 64, 60, 22); fl(ctx, DAD['shoes'], 5)
                ctx.restore()
            ellipse(ctx, DRX + 70, cy, 70, 64); fl(ctx, DAD['pants'], 5)
            if c >= 30:
                dryer_shake = 4 * math.sin(c * 2)
                for k in range(3):
                    sparkle(ctx, DRX - 80 + 80 * k + dryer_shake, DRT - 90, 14, YEL)
    ctx.restore()
    label2(ctx, SRCH[i][0], SRCH[i][1], GOLD, pop(c, 0, 4), 88, col2=WHITE, y=640)
    if i == 0 and c >= 10:
        label(ctx, "*FWUMP!*", 540, 1440, 110, CYAN, -0.04, pop(c, 10, 13))
        nope(ctx, pop(c, 30, 36))
    if i == 1:
        if c >= 12:
            label(ctx, "*snore~*", 540, 1440, 100, hx('c8e6ff'), 0.04, pop(c, 12, 16))
        nope(ctx, pop(c, 30, 36))
    if i == 2:
        if c >= 30:
            label(ctx, "*BONK!*", 540, 1340, 120, RED, -0.05, pop(c, 30, 32))
            label(ctx, "\"...STUCK.\"", 540, 1470, 104, WHITE, 0.03, pop(c, 36, 40))


# ------------------------------------------------------------------ shot 4: POV from inside the dryer
def s4(ctx, f):
    il = f - 300   # 0..70
    z = 1.0 + 0.06 * eio(il / 70)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('c4cfe6')), (1, hx('8fa0c6'))])); ctx.paint()
    ctx.save(); cam(ctx, 540, 960, z, 0, shake_at(il, [36], 8, 12), f)
    # drum holes
    for yy in range(300, 1700, 90):
        for xx in range(60 + (yy // 90 % 2) * 45, 1080, 90):
            ellipse(ctx, xx, yy, 12, 12); setc(ctx, hx('7a88aa')); ctx.fill()
    ellipse(ctx, 540, 940, 380, 380); setc(ctx, hx('ffe2c9')); ctx.fill()   # opening, the room beyond
    rays(ctx, 540, 940, 150, 380, il * 0.03, (1, 1, 1), 0.35, 16)
    face(ctx, DAD, P(eye='glare', mouth='grin' if il < 36 else 'scream'), 540, 980, 200)
    rnd = random.Random(9)
    for k in range(9):   # lint fluff in his hair
        ellipse(ctx, 540 + rnd.uniform(-160, 160), 790 + rnd.uniform(-40, 30), 22, 14, rnd.uniform(0, 3)); fl(ctx, hx('eef0ff'), 3)
    sock(ctx, 360, 840, -0.6, 0.7, SOCKS[0])   # sock stuck to his ear (static!)
    # door ring frame
    ctx.new_path(); ctx.arc(540, 940, 420, 0, 2 * math.pi); ctx.arc_negative(540, 940, 372, 2 * math.pi, 0)
    fl(ctx, hx('dfe7f5'), 6)
    twitch(ctx, 760, 760, il, 1.4)
    ctx.restore()
    label(ctx, "\"Socks don't just...", 540, 1440, 100, WHITE, -0.03, pop(il, 3, 7))
    if il >= 36:
        label(ctx, "...VANISH!!\"", 540, 1560, 120, ORANGE, 0.03, pop(il, 36, 40))


# ------------------------------------------------------------------ shot 5: puppets -> twist -> Mom -> loop
def kid_behind(ctx, x, rise, lf, eye='happy', mouth='grin', arms=True):
    """kid standing behind the dryer: drawn before it, so only head + raised arms show."""
    k = stand(ctx, KID, x, KK, P(eye=eye, mouth=mouth, lsh=160 if arms else -10, lel=10, rsh=160 if arms else -10, rel=10, head=-4), 1,
              g=GND - 230 * rise + 200 * (1 - rise))
    return k


def s5(ctx, f):
    lf = f - 370
    if lf >= 260:
        return s1(ctx, f, f - 630)
    if lf < 110:
        zoom, cx, cy = (1.25, 860, 1280) if lf < 60 else (1.35 + 0.06 * eio((lf - 60) / 50), 790, 1220)
    elif lf < 160:
        zoom, cx, cy = 1.25, 900, 1290
    else:
        zoom, cx, cy = 1.08, 1000, 1310
    ctx.save(); cam(ctx, cx, cy, zoom, 0, shake_at(lf, [60, 196], 8, 12), f)
    laundry_room(ctx, lf + 300, door=eio(pop(lf, 150, 162)) if lf < 236 else 1.0)
    rise = 0 if lf < 50 else eio(pop(lf, 50, 62))
    talk = lf < 110
    if lf < 160:
        # puppets rising behind the dryer, then the kid
        kx = DRX - 10
        if lf >= 50:
            k = kid_behind(ctx, kx, rise, lf)
            hands = [k['back'], k['front']]
        else:
            hands = [(DRX - 40, DRT + 40), (DRX + 60, DRT + 40)]
        p1 = eio(pop(lf, 4, 16))
        grabbed = lf >= 120
        if not grabbed:
            puppet(ctx, hands[0][0], hands[0][1] + 160 - 220 * p1, 0.6, STRIPE, lf, talk=talk and lf < 50, f_=-1)
        else:
            puppet(ctx, hands[0][0], hands[0][1] + 20, 0.0001, STRIPE, lf)   # bare hand (puppet gone)
        p2 = eio(pop(lf, 22, 34))
        puppet(ctx, hands[1][0], hands[1][1] + 160 - 220 * p2, 0.6, SOCKS[0], lf + 7, talk=talk and 22 <= lf < 50)
        machines(ctx, lf, peek=False, dryer_top=0)
        if lf >= 56:   # a row of puppet socks along the dryer top
            for j, c in enumerate(SOCKS[1:5]):
                u = eio(pop(lf, 56 + j * 4, 62 + j * 4))
                puppet(ctx, DRX - 120 + j * 80, DRT + 6, 0.34 * u + 0.0001, c, lf + j * 3)
        dogbed(ctx, lf=lf); basket(ctx, BSX, 0.3)
        if lf < 110:
            d = stand(ctx, DAD, DADX, KD, P(eye='shock' if lf >= 8 else 'normal', mouth='open' if lf >= 8 else 'flat',
                                            lsh=-30, lel=-120, rsh=60, rel=-60, head=-8), -1)
        elif lf < 130:
            reach = eio(pop(lf, 110, 120))
            d = stand(ctx, DAD, DADX - 160 * reach, KD, P(eye='glare', mouth='grin', lsh=-30, lel=-120, rsh=60 + 60 * reach, rel=-20, head=-6, torso=-10 * reach), -1)
            if grabbed:
                sock(ctx, d['front'][0], d['front'][1] - 30, 0.3, 0.7, STRIPE)
        else:
            d = stand(ctx, DAD, DADX - 60, KD, P(eye='happy', mouth='grin', lsh=-30, lel=-120, rsh=-125, rel=-15, head=6), -1)
            pair(ctx, max(d['front'], d['back'])[0] + 10, max(d['front'], d['back'])[1] - 60, STRIPE, 0.85)
            for j in range(3):
                sparkle(ctx, d['front'][0] - 80 + j * 80, d['front'][1] - 200 - 10 * math.sin(lf * 0.3 + j), 16, YEL)
    else:
        # Mom arrives with a heaped basket and dumps it on Dad
        machines(ctx, lf, peek=False, dryer_top=3)
        k = stand(ctx, KID, DRX - 150, KK, P(eye='happy', mouth='grin', lsh=-20, rsh=120, rel=-40), 1)
        puppet(ctx, k['front'][0], k['front'][1] + 20, 0.45, SOCKS[0], lf)
        dogbed(ctx, lf=lf)
        walk = eio(pop(lf, 160, 182))
        mx = lerp(1600, 1400, walk)
        dump = eio(pop(lf, 190, 198))
        buried = lf >= 196
        if not buried:
            d = stand(ctx, DAD, DADX - 120, KD, P(eye='happy' if lf < 186 else 'shock', mouth='grin' if lf < 186 else 'open',
                                                 lsh=-30, lel=-120, rsh=-125, rel=-15, head=6), -1)
            pair(ctx, max(d['front'], d['back'])[0] + 10, max(d['front'], d['back'])[1] - 60, STRIPE, 0.85)
        mom = stand(ctx, MOM, mx, KM, P(eye='happy', mouth='grin', lsh=100 + 60 * dump, lel=-30, rsh=100 + 60 * dump, rel=-30,
                                        head=-6, torso=-12 * dump), -1)
        ctx.save(); ctx.translate((mom['front'][0] + mom['back'][0]) / 2 - 60 - 120 * dump, (mom['front'][1] + mom['back'][1]) / 2 + 40 * dump)
        ctx.rotate(-1.4 * dump); ctx.scale(0.75, 0.75); basket(ctx, 0, 1.0 - dump, y=180); ctx.restore()
        if buried:   # a mountain of single socks
            rnd = random.Random(21)
            for j in range(34):
                col = (SOCKS + [STRIPE])[j % 7] if j != 33 else SOCKS[3]
                sock(ctx, DADX - 120 + rnd.uniform(-210, 210), GND - 30 - rnd.uniform(0, 1) ** 0.7 * 240 + (rnd.random() * 30),
                     rnd.uniform(-2, 2), 0.6, col)
            if lf >= 232:
                pop_ = eio(pop(lf, 232, 238))
                hx_, hy_ = DADX - 120, GND - 230 - 70 * pop_
                face(ctx, DAD, P(eye='glare', mouth='flat'), hx_, hy_, 70)
                twitch(ctx, hx_ + 50, hy_ - 60, lf, 0.7)
                sock(ctx, hx_ + 90, hy_ - 10, 0.4, 0.55, SOCKS[3])
    ctx.restore()
    # labels
    if lf < 50:
        label(ctx, "*hee hee*", 540, 640, 96, PINK, 0.04, pop(lf, 0, 4))
        if lf >= 22:
            label2(ctx, "\"Hello,", "DAD!\"", YEL, pop(lf, 22, 26), 116, col2=PINK, y=1440)
    elif lf < 110:
        label(ctx, "*TA-DAAA!*", 540, 1440, 110, GOLD, -0.03, pop(lf, 52, 56))
        card(ctx, 'p2', lf, 60)
    elif lf < 160:
        if lf < 130:
            label(ctx, "\"...MY SOCK!\"", 540, 1440, 116, WHITE, -0.03, pop(lf, 110, 114))
            if lf >= 120:
                label(ctx, "*FWIP!*", 540, 640, 110, CYAN, 0.04, pop(lf, 120, 123))
        else:
            label(ctx, "*DING!*", 540, 640, 120, GREEN, 0.04, pop(lf, 130, 133))
            label2(ctx, "\"FINALLY...", "A PAIR.\"", WHITE, pop(lf, 134, 138), 116, col2=MINT, y=1440)
    else:
        if lf < 194:
            label2(ctx, "\"Honey! Here's", "the NEXT load!\"", PINK, pop(lf, 164, 168), 100, y=1440)
        elif lf < 230:
            label(ctx, "*FWUMP!!*", 540, 640, 130, CYAN, -0.04, pop(lf, 196, 199))
        else:
            label2(ctx, "\"...of", "COURSE.\"", WHITE, pop(lf, 238, 242), 124, col2=ORANGE, y=1440)


SHOTS = [(0, s1), (60, s2), (150, s3), (300, s4), (370, s5)]
CUTS = (60, 150, 200, 250, 300, 370, 480, 530, 630)


def render(f):
    import sketch
    sketch.BOIL[0] = f // 4
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.1, 0.05, 0.15, 0.14)
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
                              "-i", "out/missing_sock_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
