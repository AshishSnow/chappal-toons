"""'DAD'S FIRST DAY AT THE GYM'. Original, general-audience comedy short, 22s.
Hook:   gym medium shot: Dad in a sweatband running for his life on a treadmill (display: SPEED 1), gripping the rails,
        forced grin "I'M... FINE!!" + caption 'DAD'S FIRST DAY AT THE GYM:'; kid with a water bottle and the dog watching.
Beat 1: barbell "Warm-up? EASY." -> *HNNNGH!!* it doesn't budge -> NOPE! -> he proudly lifts the tiny pink 1 KG dumbbell,
        arm shaking "...WARM-UP."
Beat 2: Dutch tilt: sitting on the exercise ball "Sit-ups? EASY." -> wobble -> *BOING!* ball shoots away -> flat on his
        back, legs in the air, ball bonks him "...ow."
Beat 3: macro console: *beep beep beep* SPEED 1 -> 10 "Level... TEN!" -> wide: legs blur *ZOOOM* -> flung off the back
        into the exercise-ball pile *FWUMP!!* legs sticking out "...NAILED IT."
Close-up (the one face shot): sweaty determined Dad "I'LL BE BACK..." "...TOMORROW!!"
Twist:  'DAY 3:' Dad on the sofa (still in the sweatband) eating chips "My muscles are... RESTING." ->
        PLOT TWIST: THE DOG KEPT GOING. the dog in a sweatband sprints on the treadmill at SPEED 10, kid cheering
        "GO, BUDDY!!", medal *DING* "MEMBER OF THE MONTH!" -> Dad gets the photo on his phone, chips fall, glare
        "...oh, it's ON." -> leaps up -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face, rays
from scenes58 import sweat, twitch
from scenes65 import dog
from scenes84 import eio
import scenes13
from scenes13 import card as _card13

RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
DADG = dict(doodle.DAD, shirt=hx('ff4d6d'), pants=hx('5b6478'), shoes=hx('3fd6a0'), sleeve=0.0)
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ffc93c'), pants=hx('3d7bff'), shoes=hx('ff4d5e'))
N = 660
FLOOR, GND = 1560, 1595
DECK = 1540                       # treadmill belt top
TX0, TX1 = 820, 1300              # treadmill deck x range
DADX, KIDX, DOGX = 1040, 1500, 650
CX, CY, CZ = 1080, 1270, 1.17

CAPS = {'p1': [[("DAD'S FIRST DAY ", OUT), ("AT THE GYM:", RED)]],
        'p2': [[("DAY 3:", PURPLE)]],
        'p3': [[("PLOT TWIST:", RED)], [("THE DOG ", OUT), ("KEPT GOING.", GREEN)]]}
scenes13.CAPS = CAPS
card = _card13


def stand(ctx, ch, x, k, p, f_=1, feet=GND):
    return draw(ctx, x, feet - 186 * k, k, f_, ch, p)


def band(ctx, d, col=CYAN, ang=0.0, p=None):
    hx_, hy_ = d['head']; R = d['R']
    if p is not None:
        ang = p['torso'] + p.get('head', 0) + p['rot']
    ctx.save(); ctx.translate(hx_, hy_); ctx.rotate(math.radians(ang)); ctx.translate(-hx_, -hy_)
    rect_r(ctx, hx_ - R * 0.97, hy_ - R * 0.66, R * 1.94, R * 0.25, R * 0.1); fl(ctx, col, 4)
    for k in range(4):
        ctx.move_to(hx_ - R * 0.7 + k * R * 0.45, hy_ - R * 0.62); ctx.line_to(hx_ - R * 0.6 + k * R * 0.45, hy_ - R * 0.45)
    setc(ctx, (1, 1, 1, 0.6)); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def run_pose(lf, spd=0.9, **kw):
    ph = lf * spd; s = math.sin(ph); c = math.cos(ph)
    p = dict(lhip=38 * s, rhip=-38 * s, lkn=-70 * (0.5 + 0.5 * c), rkn=-70 * (0.5 - 0.5 * c))
    p.update(kw)
    return P(**p)


# ------------------------------------------------------------------ props
def bottle(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rect_r(ctx, -18, -70, 36, 80, 10); fl(ctx, hx('7fd0ff'), 4)
    rect_r(ctx, -12, -86, 24, 18, 4); fl(ctx, BLUE, 3)
    ctx.rectangle(-16, -40, 32, 16); setc(ctx, (1, 1, 1, 0.6)); ctx.fill()
    ctx.restore()


def dumbbell(ctx, x, y, s=1.0, col=PINK, rot=0.0, tag=None):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rect_r(ctx, -40, -7, 80, 14, 6); fl(ctx, hx('b8c0cc'), 3)
    for sx in (-1, 1):
        rect_r(ctx, sx * 40 - 14, -26, 28, 52, 10); fl(ctx, col, 4)
    if tag:
        text(ctx, tag, 0, -46, 30, WHITE, outline=OUT, ow=6, shadow=False)
    ctx.restore()


def barbell(ctx, x, y, jig=0.0):
    ctx.save(); ctx.translate(x, y + jig)
    rect_r(ctx, -330, -9, 660, 18, 8); fl(ctx, hx('b8c0cc'), 4)
    for sx in (-1, 1):
        for i, (rx, ry, col) in enumerate(((30, 100, hx('3a3a4a')), (26, 82, hx('ff3b5c')))):
            ellipse(ctx, sx * (250 + i * 46), 0, rx, ry); fl(ctx, col, 5)
        rect_r(ctx, sx * 320 - 14, -16, 28, 32, 6); fl(ctx, hx('8a92a6'), 3)
    rect_r(ctx, -70, 30, 140, 46, 10); fl(ctx, YEL, 4)
    text(ctx, "100 KG", 0, 53, 32, OUT, outline=WHITE, ow=0, shadow=False)
    ctx.restore()


def ball(ctx, x, y, r, col, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ellipse(ctx, 0, 0, r, r); fl(ctx, col, 5)
    ctx.new_path(); ctx.arc(0, 0, r * 0.72, -2.4, -1.2); setc(ctx, (1, 1, 1, 0.45)); ctx.set_line_width(r * 0.12); ctx.stroke()
    ctx.new_path(); ctx.move_to(-r, 0); ctx.curve_to(-r * 0.3, r * 0.25, r * 0.3, r * 0.25, r, 0); setc(ctx, (0, 0, 0, 0.12)); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


BALLS = [(330, GND - 100, 100, hx('ff5fa8')), (520, GND - 95, 95, hx('3fa8ff')), (420, GND - 255, 90, hx('ffc93c')),
         (250, GND - 245, 80, hx('3fd6a0')), (600, GND - 245, 78, hx('b88aff'))]


def ball_pile(ctx, lf, burst_t=-1.0, front=False):
    """burst_t: 0..1 progress of the Dad impact (balls scatter + settle)."""
    for i, (x, y, r, c) in enumerate(BALLS):
        if front and i not in (0, 1):
            continue
        if burst_t >= 0:
            dirx = (x - 430) / 140.0 + (0.6 if i % 2 else -0.6)
            u = eout(min(1, burst_t * 1.4))
            bounce = abs(math.sin(burst_t * math.pi * 3)) * (1 - burst_t) * 220
            nx = x + dirx * 260 * u
            ny = min(GND - r, y - bounce) if burst_t < 1 else GND - r
            ny = lerp(y, GND - r, u) - bounce
            ball(ctx, nx, ny, r, c, dirx * u * 2)
        else:
            ball(ctx, x, y, r, c)


def treadmill(ctx, phase=0.0, disp=1, glow=0.0, lf=0):
    # deck
    rect_r(ctx, TX0 - 20, DECK - 6, TX1 - TX0 + 40, 62, 26); fl(ctx, hx('4a5068'), 6)
    rect_r(ctx, TX0, DECK - 6, TX1 - TX0, 20, 8); fl(ctx, hx('2a2e3e'), 3)
    for k in range(9):        # moving belt stripes
        xx = TX0 + ((k * 60 - phase * 60) % (TX1 - TX0))
        ctx.move_to(xx, DECK - 3); ctx.line_to(xx + 18, DECK - 3)
    setc(ctx, (1, 1, 1, 0.35)); ctx.set_line_width(5); ctx.stroke()
    for xx in (TX0 + 10, TX1 - 10):
        ellipse(ctx, xx, DECK + 26, 24, 24); fl(ctx, hx('8a92a6'), 4)
    # upright + console
    ctx.new_path(); ctx.move_to(TX1 - 30, DECK); ctx.line_to(TX1 + 40, DECK - 330)
    ink(ctx, 34); ctx.stroke_preserve(); setc(ctx, hx('8a92a6')); ctx.set_line_width(24); ctx.stroke()
    ctx.new_path(); ctx.move_to(TX1 + 14, DECK - 220); ctx.line_to(TX1 - 250, DECK - 220)       # handrail
    ink(ctx, 22); ctx.stroke_preserve(); setc(ctx, hx('ff8a1f')); ctx.set_line_width(13); ctx.stroke()
    ctx.save(); ctx.translate(TX1 + 50, DECK - 360); ctx.rotate(-0.12)
    rect_r(ctx, -110, -60, 220, 120, 22); fl(ctx, hx('3fd6a0'), 6)
    rect_r(ctx, -90, -44, 180, 60, 10); fl(ctx, hx('1a2030'), 3)
    hot = disp >= 10
    col = RED if hot and (lf // 3) % 2 == 0 else YEL
    text(ctx, f"SPEED {disp}", 0, -13, 30, col, outline=hx('1a2030'), ow=0, shadow=False)
    if glow > 0:
        ellipse(ctx, 0, -14, 120, 50); setc(ctx, (1, 0.3, 0.3, 0.25 * glow)); ctx.fill()
    for i, (bx, sym, bc) in enumerate(((-50, '-', hx('ff5fa8')), (50, '+', hx('ffc93c')))):
        ellipse(ctx, bx, 38, 22, 15); fl(ctx, bc, 4)
        text(ctx, sym, bx, 37, 28, OUT, outline=WHITE, ow=0, shadow=False)
    ctx.restore()


def gym(ctx, lf, tread=True, phase=0.0, disp=1, balls=True, burst=-1.0):
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, hx('ffe9d6')); ctx.fill()
    rnd = random.Random(105)
    for k in range(70):   # tiny star wallpaper
        x, y = rnd.uniform(-300, 2500), rnd.uniform(380, 1500)
        ctx.save(); ctx.translate(x, y); ctx.rotate(rnd.uniform(0, 1))
        poly(ctx, [(0, -9), (3, -3), (9, -3), (4, 2), (6, 9), (0, 5), (-6, 9), (-4, 2), (-9, -3), (-3, -3)])
        setc(ctx, hx('ffd2b3')); ctx.fill(); ctx.restore()
    ctx.rectangle(-3000, 1180, 9000, 60); setc(ctx, hx('ffc6a8')); ctx.fill()       # wall stripe
    # big wall mirror
    rect_r(ctx, 760, 830, 640, 560, 16); fl(ctx, hx('c9a47a'), 6)
    rect_r(ctx, 780, 850, 600, 520, 10); fl(ctx, hx('d6f0ff'), 4)
    ctx.save(); rect_r(ctx, 780, 850, 600, 520, 10); ctx.clip()
    for xx in (860, 960, 1200):
        poly(ctx, [(xx, 850), (xx + 50, 850), (xx - 190, 1370), (xx - 240, 1370)])
    setc(ctx, (1, 1, 1, 0.55)); ctx.fill(); ctx.restore()
    # poster (left)
    ctx.save(); ctx.translate(560, 980); ctx.rotate(-0.04)
    rect_r(ctx, -120, -150, 240, 300, 10); fl(ctx, YEL, 5)
    text(ctx, "YOU", 0, -88, 54, RED, outline=WHITE, ow=6, shadow=False)
    text(ctx, "GOT", 0, -22, 54, RED, outline=WHITE, ow=6, shadow=False)
    text(ctx, "THIS!", 0, 46, 54, RED, outline=WHITE, ow=6, shadow=False)
    dumbbell(ctx, 0, 110, 0.9, BLUE)
    ctx.restore()
    for (px, py) in ((450, 836), (670, 836)):
        ellipse(ctx, px, py, 9, 9); fl(ctx, RED, 3)
    # wall clock (right)
    ellipse(ctx, 1560, 900, 62, 62); fl(ctx, WHITE, 6)
    ctx.move_to(1560, 900); ctx.line_to(1560, 858); ctx.move_to(1560, 900); ctx.line_to(1590, 912); ink(ctx, 6); ctx.stroke()
    # floor: soft rubber mats
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('9fc4e6')); ctx.fill()
    for i in range(-30, 60):
        ctx.move_to(i * 110, FLOOR); ctx.line_to(i * 110 - 60, FLOOR + 600)
    for j in range(1, 8):
        ctx.move_to(-3000, FLOOR + j * 70); ctx.line_to(6000, FLOOR + j * 70)
    setc(ctx, hx('86afd6')); ctx.set_line_width(4); ctx.stroke()
    rect_r(ctx, -3000, FLOOR - 22, 9000, 22, 4); fl(ctx, hx('e0b48a'), 4)
    # dumbbell rack (right)
    rect_r(ctx, 1640, 1290, 440, 26, 8); fl(ctx, hx('6a7390'), 4)
    rect_r(ctx, 1640, 1440, 440, 26, 8); fl(ctx, hx('6a7390'), 4)
    for xx in (1660, 2040):
        rect_r(ctx, xx, 1290, 22, GND - 1290, 6); fl(ctx, hx('4a5068'), 4)
    for i, (c, s) in enumerate(((PINK, 0.7), (MINT, 0.8), (BLUE, 0.9), (ORANGE, 1.0))):
        dumbbell(ctx, 1730 + i * 100, 1262 + (1 - s) * 30, s, c)
    for i, (c, s) in enumerate(((PURPLE, 1.1), (RED, 1.2), (hx('3a3a4a'), 1.3))):
        dumbbell(ctx, 1745 + i * 135, 1408 + (1.3 - s) * 20, s, c)
    # water cooler + plant (far right)
    rect_r(ctx, 2150, 1300, 120, 260, 14); fl(ctx, WHITE, 5)
    rect_r(ctx, 2160, 1140, 100, 170, 30); fl(ctx, hx('bfe8ff'), 5)
    rect_r(ctx, -40, 1440, 100, 120, 14); fl(ctx, hx('ff8a5c'), 5)
    for a in (-0.9, -0.4, 0.1, 0.6, 1.0):
        ellipse(ctx, 10 + 70 * math.sin(a), 1400 - 50 * math.cos(a), 20, 48, a); fl(ctx, GREEN, 3)
    if balls:
        ball_pile(ctx, lf, burst)
    if tread:
        treadmill(ctx, phase, disp, lf=lf)


def gym_dog(ctx, x, feet, s, lf, run=False, medal=0.0):
    """dog in a pink sweatband; run=True -> galloping bob"""
    bob = abs(math.sin(lf * 0.9)) * 22 if run else 0
    rot = 0.06 * math.sin(lf * 0.9) if run else 0
    ctx.save(); ctx.translate(x, feet - bob); ctx.rotate(rot)
    dog(ctx, 0, 0, s, 1, lf * (2 if run else 1))
    ctx.save(); ctx.scale(s, s)
    rect_r(ctx, 70, -302, 150, 30, 10); fl(ctx, PINK, 4)
    if medal > 0:
        u = eout(medal)
        ctx.new_path(); ctx.move_to(80, -190); ctx.line_to(130, -110 - 20 * (1 - u)); ctx.line_to(170, -190)
        setc(ctx, BLUE); ctx.set_line_width(10); ctx.stroke()
        ellipse(ctx, 130, -100 - 20 * (1 - u), 30 * u, 30 * u); fl(ctx, GOLD, 4)
        sparkle(ctx, 130, -100, 12 * u, WHITE)
    ctx.restore()
    if run:
        for k in range(3):   # leg blur arcs
            ctx.new_path(); ctx.arc(-20 * s + k * 50 * s, -40 * s, 60 * s, 0.3, 2.8)
            setc(ctx, (1, 1, 1, 0.5)); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = CZ + 0.04 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, CX, CY, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    gym(ctx, lf, phase=lf * 0.5)
    gym_dog(ctx, DOGX, GND, 0.5, lf)
    bob = abs(math.sin(lf * 0.9)) * 10
    dp = run_pose(lf, 0.9, eye='shock', mouth='grin', torso=-8, lsh=80, lel=-10, rsh=88, rel=-12, head=-4)
    d = stand(ctx, DADG, DADX, 1.12, dp, 1, DECK - bob)
    band(ctx, d, p=dp)
    sweat(ctx, d['head'][0] - d['R'] * 1.05, d['head'][1] - d['R'] * 0.5, lf, 0.9)
    sweat(ctx, d['head'][0] + d['R'] * 1.0, d['head'][1] - d['R'] * 0.8, lf + 40, 0.8)
    w = math.sin(lf * 0.5)
    kp = P(eye='normal', mouth='flat', lsh=20, lel=-20, rsh=40, rel=-110, head=3 * w)
    kd = stand(ctx, KID, KIDX, 0.95, kp, -1)
    bottle(ctx, kd['front'][0], kd['front'][1] + 20, 0.9)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"I'M... FINE!!\"", 540, 1450, 130, YEL, -0.04, t)


# ------------------------------------------------------------------ shot 2a: the barbell
def barbell_shot(ctx, f, il):
    # 0-20 "Warm-up? EASY." ; 20-46 *HNNNGH!!* ; 46-56 NOPE ; 56-70 pink 1 KG dumbbell "...WARM-UP."
    zz = 1.3 + (0.08 * eio(pop(il, 20, 46)) if il < 56 else 0)
    ctx.save(); cam(ctx, 1640, 1300, zz, 0, shake_at(il, [46], 10, 14) + (4 if 20 <= il < 46 else 0), f)
    gym(ctx, il, tread=False, balls=False)
    BX = 1640
    if il < 56:
        strain = 20 <= il < 46
        dp = P(eye='glare' if strain else 'happy', mouth='scream' if strain else 'grin', torso=18, head=-6,
               lsh=12, lel=-8, rsh=8, rel=-8, lhip=60, lkn=-100, rhip=55, rkn=-95)
        jx = (random.Random(il).uniform(-6, 6) if strain else 0)
        d = stand(ctx, DADG, BX + jx - 10, 1.12, dp, 1, GND + 30)
        band(ctx, d, p=dp)
        if strain:
            sweat(ctx, d['head'][0] - d['R'] * 1.05, d['head'][1] - d['R'] * 0.4, il * 2, 0.9)
            twitch(ctx, d['head'][0] + d['R'] * 0.8, d['head'][1] - d['R'] * 0.9, il, 1.0)
        barbell(ctx, BX, GND - 100, -3 * (il % 2) if strain else 0)
    else:
        sh = 8 * math.sin(il * 2.5)
        dp = P(eye='happy', mouth='grin', lsh=20, lel=-20, rsh=125 + sh, rel=-40, head=4, torso=-4)
        d = stand(ctx, DADG, BX + 40, 1.12, dp, 1)
        band(ctx, d, p=dp)
        dumbbell(ctx, d['front'][0], d['front'][1] - 4, 0.95, PINK, 0.2 + 0.05 * sh / 8, "1 KG")
        barbell(ctx, BX, GND - 100)
        sweat(ctx, d['head'][0] - d['R'] * 1.05, d['head'][1] - d['R'] * 0.4, il * 2, 0.8)
        for k in range(3):
            sparkle(ctx, d['front'][0] + 70 * math.cos(il * 0.3 + k * 2), d['front'][1] - 60 + 40 * math.sin(il * 0.3 + k * 2), 12, YEL)
    ctx.restore()
    if il < 20:
        label(ctx, "\"Warm-up? EASY.\"", 540, 1450, 108, WHITE, -0.03, pop(il, 2, 6))
    elif il < 46:
        label(ctx, "*HNNNNGH!!*", 540, 470, 110, ORANGE, 0.03, pop(il, 20, 24))
    elif il < 56:
        stamp(ctx, "NOPE!", 540, 1430, pop(il, 46, 50), -0.12)
    else:
        label(ctx, "\"...WARM-UP.\"", 540, 1450, 118, PINK, 0.03, pop(il, 58, 61))


def stamp(ctx, s, x, y, t, ang=-0.15, col=RED):
    if t <= 0:
        return
    sc = 1.6 - 0.6 * eout(min(1, t * 2))
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(sc, sc)
    rect_r(ctx, -200, -70, 400, 140, 16); setc(ctx, (1, 1, 1, 0.85)); ctx.fill_preserve()
    setc(ctx, col); ctx.set_line_width(12); ctx.stroke()
    text(ctx, s, 0, 0, 96, col, outline=WHITE, ow=8, shadow=False)
    ctx.restore()


# ------------------------------------------------------------------ shot 2b: the exercise ball
def ball_shot(ctx, f, il):
    # 0-30 sitting, wobbling "Sit-ups? EASY." ; 30-42 *BOING!* ball shoots off, Dad falls ; 42-70 flat on his back, ball bonk "...ow."
    ctx.save(); cam(ctx, 900, 1310, 1.22, -6, shake_at(il, [40, 52], 12, 18), f)
    gym(ctx, il, tread=False)
    BXX, R0 = 900, 120
    if il < 30:
        wob = math.sin(il * 0.5) * (6 + il * 0.5)
        ball(ctx, BXX + wob * 0.6, GND - R0, R0, PURPLE, wob * 0.01)
        dp = P(eye='happy' if il < 16 else 'shock', mouth='grin' if il < 16 else 'wavy', lhip=80, lkn=-80, rhip=75, rkn=-75,
               lsh=120 + wob, lel=-30, rsh=110 - wob, rel=-30, rot=wob * 0.7, torso=-4)
        d = draw_hip(ctx, BXX + wob, GND - 2 * R0 - 10, 1.1, 1, DADG, dp)
        band(ctx, d, p=dp)
    else:
        u = pop(il, 30, 42)
        bx = BXX + 900 * eout(u) if il < 50 else lerp(BXX + 900, BXX + 120, eio(pop(il, 50, 60)))
        by = GND - R0 - (abs(math.sin(pop(il, 50, 66) * math.pi * 2)) * 220 * (1 - pop(il, 50, 66)) if il >= 50 else 0)
        fall = eout(pop(il, 30, 40))
        hipy = lerp(GND - 2 * R0 - 10, GND - 125, fall)
        lie = il >= 40
        dp = P(eye='closed' if lie else 'shock', mouth='open' if lie else 'scream', lhip=80, lkn=-30 if lie else -80, rhip=70, rkn=-40 if lie else -75,
               lsh=150, lel=-20, rsh=140, rel=-20, rot=-95 * fall)
        d = draw_hip(ctx, BXX + 170 * fall, hipy, 1.1, 1, DADG, dp)
        band(ctx, d, p=dp)
        if lie:
            stars_ko(ctx, d['head'][0], d['head'][1] - 90, il * 0.15, 4, 80)
        ball(ctx, bx, by, R0, PURPLE, (bx - BXX) * 0.01)
    ctx.restore()
    if il < 30:
        label(ctx, "\"Sit-ups? EASY.\"", 540, 1450, 108, WHITE, -0.03, pop(il, 2, 6))
    elif il < 52:
        label(ctx, "*BOING!*", 540, 470, 140, PURPLE, 0.04, pop(il, 30, 33))
    else:
        label(ctx, "\"...ow.\"", 540, 1450, 140, MINT, -0.03, pop(il, 58, 61))


def s2(ctx, f):
    if f < 130:
        barbell_shot(ctx, f, f - 60)
    else:
        ball_shot(ctx, f, f - 130)


# ------------------------------------------------------------------ shot 3: SPEED 10 -> flung into the balls
def speed_shot(ctx, f, il):
    if il < 32:
        lvl = 1 + min(9, int(pop(il, 4, 26) * 9.99))
        ctx.save(); cam(ctx, TX1 - 40, DECK - 380, 2.7, 3, shake_at(il, [6, 12, 18, 24], 4, 6), f)
        gym(ctx, il, phase=il * 0.5 * (1 + lvl * 0.2), disp=lvl, balls=False)
        dp = run_pose(il, 0.9, eye='smug', mouth='smile', lsh=80, lel=-10, rsh=88, rel=-12)
        d = stand(ctx, DADG, DADX, 1.12, dp, 1, DECK)
        band(ctx, d, p=dp)
        treadmill(ctx, il * 0.5, lvl, glow=1.0 if lvl >= 10 else 0, lf=il)
        ctx.restore()
        # big poking finger from the bottom left (screen space)
        poke = max([0] + [1 - abs(il - t) / 3 for t in (6, 12, 18, 24) if abs(il - t) < 3])
        hx_, hy_ = 690 - 40 * poke, 1260 - 60 * poke
        ctx.new_path(); ctx.move_to(200, 1950); ctx.line_to(hx_ - 30, hy_ + 60); ink(ctx, 150); ctx.stroke_preserve()
        setc(ctx, DADG['skin']); ctx.set_line_width(128); ctx.stroke()
        ellipse(ctx, hx_ - 40, hy_ + 50, 95, 80, -0.6); fl(ctx, DADG['skin'], 7)
        ctx.new_path(); ctx.move_to(hx_ - 20, hy_ + 20); ctx.line_to(hx_ + 40, hy_ - 40); ink(ctx, 58); ctx.stroke_preserve()
        setc(ctx, DADG['skin']); ctx.set_line_width(42); ctx.stroke()
        label(ctx, "\"Level...\"", 540, 470, 100, WHITE, -0.03, pop(il, 2, 6))
        if il >= 24:
            label(ctx, "TEN!", 540, 1480, 170, RED, 0.04, pop(il, 24, 27))
        return
    j = il - 32
    ctx.save(); cam(ctx, 900 - 180 * eio(pop(j, 26, 40)), 1300, 1.0 + 0.12 * eio(pop(j, 26, 40)), 0, (6 if j < 18 else 0) + shake_at(j, [30], 16, 28), f)
    bt = pop(j, 30, 46) if j >= 30 else -1
    gym(ctx, il, phase=il * 2.2, disp=10, burst=bt)
    gym_dog(ctx, 1560, GND, 0.5, il)
    kp = P(eye='shock', mouth='open', lsh=150, lel=-20, rsh=150, rel=-20)
    stand(ctx, KID, 1820, 0.95, kp, -1)
    if j < 18:
        dp = run_pose(il, 2.4, eye='shock', mouth='scream', torso=-14, lsh=100, lel=-10, rsh=100, rel=-10, head=-8)
        d = stand(ctx, DADG, DADX - 6 * j, 1.12, dp, 1, DECK - abs(math.sin(il * 2.4)) * 12)
        band(ctx, d, p=dp)
        for k in range(5):
            ctx.move_to(d['head'][0] + 80 + k * 30, 1300 + k * 50); ctx.line_to(d['head'][0] + 260 + k * 30, 1300 + k * 50)
        setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(8); ctx.stroke()
    elif j < 30:
        u = eio(pop(j, 18, 30))
        x = lerp(DADX - 100, 430, u); feet = lerp(DECK, GND - 330, u) - 260 * math.sin(u * math.pi)
        dp = P(eye='shock', mouth='scream', lsh=160, lel=-10, rsh=170, rel=-10, lhip=40, rhip=-30, rot=-200 * u)
        d = stand(ctx, DADG, x, 1.12, dp, 1, feet)
        band(ctx, d, p=dp)
    else:
        tw = 10 * math.sin(j * 1.3) if j > 40 else 0
        dp = P(eye='closed', mouth='open', lhip=10 + tw, rhip=-20 - tw, lkn=-10, rkn=-30, lsh=10, rsh=-10, rot=180)
        d = stand(ctx, DADG, 470, 1.12, dp, 1, GND - 400)
        hx_, hy_ = d['head']
        ball(ctx, hx_ + 10, min(hy_, GND - 115), 115, hx('ff5fa8'), 0.3)
        ball(ctx, hx_ + 120, GND - 95, 95, hx('ffc93c'), -0.2)
        ball(ctx, hx_ - 110, GND - 90, 90, hx('3fa8ff'), 0.5)
    ctx.restore()
    if j < 18:
        label(ctx, "*ZOOOOOM!*", 540, 470, 120, CYAN, -0.03, pop(j, 0, 3))
    elif j < 30:
        label(ctx, "*WHOOOSH!*", 540, 470, 120, WHITE, 0.03, pop(j, 18, 21))
    elif j < 44:
        label(ctx, "*FWUMP!!*", 540, 470, 140, ORANGE, -0.04, pop(j, 30, 33))
    else:
        label(ctx, "\"...NAILED IT.\"", 540, 1450, 118, YEL, -0.03, pop(j, 44, 47))


def s3(ctx, f):
    speed_shot(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: the one close-up
def closeup(ctx, f, il):
    z = 1 + 0.06 * eio(il / 70)
    ctx.save(); cam(ctx, 540, 960, z, 2 * math.sin(il * 0.2), shake_at(il, [34], 10, 16) + 2, f)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('ffd36a')), (1, hx('ff7a4a'))])); ctx.paint()
    rays(ctx, 540, 900, 150, 1400, il * 0.01, (1, 1, 1), 0.25, 18)
    p = P(eye='glare', mouth='flat' if il < 34 else 'open', head=-3)
    face(ctx, DADG, p, 540, 900, 200, 0, 1)
    band(ctx, {'head': (540, 900), 'R': 200 * 1.0})
    sweat(ctx, 540 - 230, 900 - 120, il, 1.4)
    sweat(ctx, 540 + 220, 900 - 180, il + 50, 1.2)
    if il >= 34:
        twitch(ctx, 540 + 200, 900 - 220, il, 1.5)
    ctx.restore()
    label(ctx, "\"I'LL BE BACK...\"", 540, 1350, 100, WHITE, -0.03, pop(il, 4, 8))
    if il >= 34:
        label(ctx, "TOMORROW!!", 540, 1500, 150, RED, 0.04, pop(il, 34, 37))


def s4(ctx, f):
    closeup(ctx, f, f - 300)


# ------------------------------------------------------------------ set: living room (day 3)
SEAT = 1420


def living(ctx, lf):
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, hx('ece4ff')); ctx.fill()
    rnd = random.Random(7)
    for k in range(70):
        x, y = rnd.uniform(-300, 2500), rnd.uniform(380, 1500)
        ctx.save(); ctx.translate(x, y); ctx.rotate(rnd.uniform(0, 1))
        poly(ctx, [(0, -9), (3, -3), (9, -3), (4, 2), (6, 9), (0, 5), (-6, 9), (-4, 2), (-9, -3), (-3, -3)])
        setc(ctx, hx('d9ccff')); ctx.fill(); ctx.restore()
    # window (evening)
    rect_r(ctx, 540, 820, 300, 340, 14); fl(ctx, WHITE, 6)
    ctx.set_source(vgrad(ctx, 0, 840, 0, 1140, [(0, hx('5a4ab8')), (1, hx('ff9a7a'))])); rect_r(ctx, 560, 840, 260, 300, 8); ctx.fill()
    ellipse(ctx, 760, 900, 26, 26); setc(ctx, hx('fff2b0')); ctx.fill()
    ctx.move_to(690, 840); ctx.line_to(690, 1140); ctx.move_to(560, 990); ctx.line_to(820, 990); ink(ctx, 6); ctx.stroke()
    # picture frame
    rect_r(ctx, 1220, 860, 200, 160, 10); fl(ctx, hx('ffc93c'), 6)
    rect_r(ctx, 1240, 880, 160, 120, 6); fl(ctx, hx('bfe8ff'), 3)
    poly(ctx, [(1240, 1000), (1300, 930), (1340, 970), (1370, 940), (1400, 1000)]); fl(ctx, GREEN, 3)
    # floor + rug
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('e6c49a')); ctx.fill()
    for i in range(-20, 40):
        ctx.move_to(-3000, FLOOR + i * 50); ctx.line_to(6000, FLOOR + i * 50)
    setc(ctx, hx('d6b088')); ctx.set_line_width(3); ctx.stroke()
    rect_r(ctx, -3000, FLOOR - 22, 9000, 22, 4); fl(ctx, WHITE, 4)
    ellipse(ctx, 1080, 1640, 520, 60); fl(ctx, hx('ff8aa8'), 5)
    ellipse(ctx, 1080, 1640, 420, 40); setc(ctx, hx('ffb3c6')); ctx.fill()
    # lamp (left) + plant (right) + empty dog bed
    ctx.move_to(500, 1560); ctx.line_to(500, 1180); ink(ctx, 10); ctx.stroke()
    poly(ctx, [(420, 1200), (580, 1200), (540, 1080), (460, 1080)]); fl(ctx, hx('ffd36a'), 5)
    rect_r(ctx, 1620, 1450, 100, 110, 14); fl(ctx, hx('ff8a5c'), 5)
    for a in (-0.9, -0.4, 0.1, 0.6, 1.0):
        ellipse(ctx, 1670 + 70 * math.sin(a), 1410 - 50 * math.cos(a), 20, 48, a); fl(ctx, GREEN, 3)
    ellipse(ctx, 1480, 1570, 110, 34); fl(ctx, hx('8ad0ff'), 5)
    ellipse(ctx, 1480, 1558, 80, 18); setc(ctx, hx('c6ecff')); ctx.fill()
    # sofa
    rect_r(ctx, 800, 1230, 560, 200, 44); fl(ctx, hx('5a7bff'), 6)
    rect_r(ctx, 820, SEAT, 520, 100, 26); fl(ctx, hx('7a95ff'), 5)
    rect_r(ctx, 770, 1320, 80, 220, 28); fl(ctx, hx('4a68e8'), 5)
    rect_r(ctx, 1310, 1320, 80, 220, 28); fl(ctx, hx('4a68e8'), 5)
    for xx in (800, 1350):
        rect_r(ctx, xx, 1530, 20, 40, 6); fl(ctx, hx('8a5a3a'), 3)
    rect_r(ctx, 1200, 1300, 100, 90, 24); fl(ctx, hx('ffd36a'), 4)


def chips_bowl(ctx, x, y, s=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    for k, (cx_, cy_) in enumerate(((-40, -26), (-10, -36), (20, -30), (45, -22), (0, -20))):
        ellipse(ctx, cx_, cy_, 22, 14, k * 0.5); fl(ctx, GOLD, 3)
    ctx.new_path(); ctx.move_to(-80, -16); ctx.curve_to(-70, 50, 70, 50, 80, -16); ctx.close_path(); fl(ctx, RED, 5)
    ctx.restore()


def phone(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(-0.3); ctx.scale(s, s)
    rect_r(ctx, -32, -56, 64, 112, 12); fl(ctx, hx('2a2e3e'), 4)
    rect_r(ctx, -24, -46, 48, 88, 6); setc(ctx, hx('bfe8ff')); ctx.fill()
    ellipse(ctx, 0, -6, 16, 14); setc(ctx, hx('e8b878')); ctx.fill()
    rect_r(ctx, -16, -20, 32, 7, 3); setc(ctx, PINK); ctx.fill()
    ellipse(ctx, 0, 22, 10, 10); setc(ctx, GOLD); ctx.fill()
    ctx.restore()


def sofa_shot(ctx, f, il, phase):
    """phase 'a': chilling with chips ; phase 'b': gets the photo, reacts, leaps up"""
    if phase == 'a':
        ctx.save(); cam(ctx, 1080, 1290, 1.17 + 0.05 * eio(il / 70), 0, 0, f)
        living(ctx, il)
        chew = (il // 5) % 2
        hand = 0.5 + 0.5 * math.sin(il * 0.4)
        dp = P(eye='closed', mouth='open' if chew else 'flat', lhip=85, lkn=-88, rhip=80, rkn=-84, torso=-16, head=10,
               lsh=60, lel=-60, rsh=120 + 30 * hand, rel=-120, rot=0)
        d = draw_hip(ctx, 1060, SEAT + 6, 1.12, 1, DADG, dp)
        band(ctx, d, p=dp)
        chips_bowl(ctx, d['back'][0] + 40, d['back'][1] + 10, 0.9)
        ellipse(ctx, d['front'][0], d['front'][1] - 6, 16, 11); fl(ctx, GOLD, 3)
        ctx.restore()
        card(ctx, 'p2', il, 0)
        label(ctx, "\"My muscles are...\"", 540, 1380, 96, WHITE, -0.03, pop(il, 8, 12))
        if il >= 34:
            label(ctx, "RESTING.", 540, 1500, 140, MINT, 0.03, pop(il, 34, 37))
        return
    # phase b: il 0..50
    zz = lerp(1.25, 1.6, eio(pop(il, 0, 14)))
    ctx.save(); cam(ctx, 1080, 1250, zz if il < 34 else 1.3, 0, shake_at(il, [12, 34], 12, 20), f)
    living(ctx, il)
    if il < 34:
        dp = P(eye='shock' if il < 12 else 'glare', mouth='open' if il < 12 else 'flat', lhip=85, lkn=-88, rhip=80, rkn=-84,
               torso=-4, head=-6, lsh=40, lel=-40, rsh=95, rel=-100)
        d = draw_hip(ctx, 1060, SEAT + 6, 1.12, 1, DADG, dp)
        band(ctx, d, p=dp)
        phone(ctx, d['front'][0] + 8, d['front'][1] - 40, 1.0)
        if il < 12:
            chips_bowl(ctx, d['back'][0] + 40, d['back'][1] + 10, 0.9)
        else:
            u = eout(pop(il, 12, 20))
            chips_bowl(ctx, lerp(d['back'][0] + 40, 1180, u), lerp(d['back'][1] + 10, GND - 20, u), 0.9, 2.6 * u)
            twitch(ctx, d['head'][0] + d['R'] * 0.8, d['head'][1] - d['R'] * 0.9, il, 1.0)
    else:
        u = eout(pop(il, 34, 42))
        dp = P(eye='glare', mouth='grin', lsh=150, lel=-20, rsh=160, rel=-10, lhip=-20, lkn=-40, rhip=30, rkn=-60, torso=8)
        d = stand(ctx, DADG, 1060 + 40 * u, 1.12, dp, 1, GND - 160 * math.sin(u * math.pi))
        band(ctx, d, p=dp)
        chips_bowl(ctx, 1180, GND - 20, 0.9, 2.6)
        sparkle(ctx, 1000, 1150, 20 * u, YEL); sparkle(ctx, 1200, 1100, 16 * u, YEL)
    ctx.restore()
    if il < 12:
        label(ctx, "*DING!*", 540, 470, 110, CYAN, 0.03, pop(il, 1, 4))
    elif il < 34:
        label(ctx, "\"...oh,", 540, 1380, 110, WHITE, -0.03, pop(il, 14, 17))
        label(ctx, "it's ON.\"", 540, 1500, 140, RED, 0.03, pop(il, 22, 25))
    else:
        label(ctx, "*FWUMP!*", 540, 470, 120, ORANGE, -0.03, pop(il, 34, 37))


def dog_shot(ctx, f, j):
    # j 0..100 : dog sprinting on the treadmill (SPEED 10), kid cheering, medal at 64
    ctx.save(); cam(ctx, 1080, 1290, 1.2 + 0.05 * eio(j / 100), 0, 3 + shake_at(j, [64], 10, 14), f)
    gym(ctx, j, phase=j * 2.2, disp=10)
    gym_dog(ctx, 1020, DECK, 0.72, j, run=True, medal=pop(j, 64, 72))
    for k in range(5):
        y = 1330 + k * 40
        ctx.move_to(820 - k * 20, y); ctx.line_to(640 - k * 20, y)
    setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(8); ctx.stroke()
    jump = abs(math.sin(j * 0.45)) * 50
    kp = P(eye='happy', mouth='grin', lsh=165, lel=-20, rsh=160, rel=-20, lhip=-10, rhip=10, head=6 * math.sin(j * 0.45))
    stand(ctx, KID, 815, 0.95, kp, 1, GND - jump)
    ctx.restore()
    card(ctx, 'p3', j, 2, 62)
    if j < 64:
        label(ctx, "\"GO, BUDDY!!\"", 540, 1450, 130, YEL, -0.03, pop(j, 16, 20))
    else:
        label(ctx, "*DING!*", 540, 470, 100, GOLD, 0.03, pop(j, 64, 67))
        label(ctx, "\"MEMBER OF THE MONTH!\"", 540, 1450, 92, GOLD, 0.03, pop(j, 66, 70))


def s5(ctx, f):
    lf = f - 370
    if lf < 70:
        sofa_shot(ctx, f, lf, 'a')
    elif lf < 170:
        dog_shot(ctx, f, lf - 70)
    elif lf < 220:
        sofa_shot(ctx, f, lf - 170, 'b')
    else:
        s1(ctx, f, f - 590)


SHOTS = [(0, s1), (60, s2), (200, s3), (300, s4), (370, s5)]
CUTS = (60, 130, 200, 232, 300, 370, 440, 540, 590)


def render(f):
    import sketch
    sketch.BOIL[0] = f // 4
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.1, 0.05, 0.15, 0.16)
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
                              "-i", "out/gym_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
