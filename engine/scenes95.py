"""'Dad vs the vending machine'. Original, general-audience comedy short, 22s.
Hook:   hallway medium shot: Dad hugging + shaking the vending machine, ONE snack dangling on the coil.
        "COME... ON...!!" + caption "DAD vs THE VENDING MACHINE:".
Beat 1: "Snack time!" *clink* *boop* -> macro push-in: the coil turns... the bag tips... and STOPS. *creak* -> "...NO."
        -> 2nd coin *clink* -> 2nd bag hangs on the 1st -> "...TWO?!"
Beat 2: Dutch-tilt montage *SHAKE!* *THUNK!* *BONK!* "OW OW OW!" -> "Double or NOTHING." -> 3 bags hanging "...THREE?!"
Turn:   POV from INSIDE the machine: Dad's face pressed on the glass behind the dangling bags "It's... MOCKING me."
Twist:  PLOT TWIST: THE KID BUYS ONE. *clink* -> his bag pushes the whole chain -> *THUNK! x4* -> kid with an armful
        "Thanks, DAD!" -> "...HOW?!" -> Dad tries again alone -> dangles AGAIN "...of COURSE." -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes65 import dog
from scenes84 import eio
import scenes13
from scenes13 import card as _card13

RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
DAD = dict(doodle.DAD, shirt=hx('22b45a'), pants=hx('3a4a8a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff5fa8'), pants=hx('3d7bff'), shoes=hx('ffc93c'))
N = 660
FLOOR, GND = 1560, 1590
VX = 1200                                # vending machine centre x
MX0, MX1, MTOP = VX - 210, VX + 200, 700  # machine body
GX0, GX1, GY0, GY1 = VX - 95, VX + 180, 760, 1250   # glass
KX = VX - 152                            # keypad column centre
COLS, ROWS = 3, 4
SW, SH = (GX1 - GX0) / COLS, (GY1 - GY0) / ROWS
TC, TR = 1, 1                            # target slot (col, row)
KDAD, KKID = 1.1, 0.82
DADX = VX - 360

CAPS = {'p1': [[("DAD ", OUT), ("vs ", RED), ("THE VENDING MACHINE:", GREEN)]],
        'p2': [[("PLOT TWIST:", RED)], [("THE KID ", OUT), ("BUYS ONE.", PINK)]]}
scenes13.CAPS = CAPS
card = _card13


def slot(c, r):
    return GX0 + SW * (c + 0.5), GY0 + SH * (r + 0.5) - 4


# ------------------------------------------------------------------ chain state (global timeline)
COILS = [(100, 128), (166, 186), (296, 316), (440, 458), (550, 570)]   # (start, end) of each purchase


def chain(f):
    """returns (n_hanging, moving_progress or None, drop_t or None)"""
    if f >= 630:
        return 1, None, None
    if f >= 570:
        return 1, None, None
    if 550 <= f < 570:
        return 0, pop(f, 550, 570), None
    if f >= 458:
        return 0, None, f - 458
    if 440 <= f < 458:
        return 3, pop(f, 440, 458), None
    if f >= 316:
        return 3, None, None
    if 296 <= f < 316:
        return 2, pop(f, 296, 316), None
    if f >= 186:
        return 2, None, None
    if 166 <= f < 186:
        return 1, pop(f, 166, 186), None
    if f >= 128:
        return 1, None, None
    if 100 <= f < 128:
        return 0, pop(f, 100, 128), None
    if f < 60:
        return 1, None, None
    return 0, None, None


def coil_phase(f):
    ph = 0
    for a, b in COILS:
        ph += pop(f, a, b)
    return ph


# ------------------------------------------------------------------ props
def packet(ctx, x, y, col, s=1.0, rot=0.0, kind=0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    if kind == 2:   # little juice bottle
        rect_r(ctx, -22, -40, 44, 80, 14); fl(ctx, col, 4)
        rect_r(ctx, -12, -54, 24, 16, 4); fl(ctx, WHITE, 3)
        rect_r(ctx, -22, -10, 44, 26, 3); setc(ctx, (1, 1, 1, 0.75)); ctx.fill()
        ellipse(ctx, 0, 3, 8, 8); fl(ctx, GOLD, 2)
        ctx.restore(); return
    w, h = 40, 50
    ctx.new_path(); ctx.move_to(-w, -h)
    for i in range(9):
        ctx.line_to(-w + (i + 0.5) * w / 4.5, -h - (7 if i % 2 == 0 else 0))
    ctx.line_to(w, -h); ctx.curve_to(w + 6, -10, w + 6, 10, w, h)
    for i in range(9):
        ctx.line_to(w - (i + 0.5) * w / 4.5, h + (7 if i % 2 == 0 else 0))
    ctx.line_to(-w, h); ctx.curve_to(-w - 6, 10, -w - 6, -10, -w, -h); ctx.close_path()
    fl(ctx, col, 4)
    ellipse(ctx, 0, 4, 24, 20); fl(ctx, WHITE, 3)
    if kind == 0:   # a crisp
        ellipse(ctx, 0, 4, 13, 10, 0.4); fl(ctx, GOLD, 2)
    else:           # a cookie
        ellipse(ctx, 0, 4, 13, 13); fl(ctx, hx('c8893a'), 2)
        for dx, dy in ((-4, 0), (5, 6), (2, -4)):
            ellipse(ctx, dx, 4 + dy, 2.5, 2.5); setc(ctx, INK); ctx.fill()
    ctx.move_to(-w + 10, -h + 10); ctx.line_to(-w + 10, h - 16); setc(ctx, (1, 1, 1, 0.5)); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


SNACK = {(0, 0): (RED, 0), (1, 0): (GOLD, 1), (2, 0): (PURPLE, 0),
         (0, 1): (CYAN, 1), (1, 1): (ORANGE, 0), (2, 1): (PINK, 1),
         (0, 2): (GREEN, 0), (1, 2): (BLUE, 1), (2, 2): (RED, 1),
         (0, 3): (hx('ff8a5c'), 2), (1, 3): (hx('7fe3ff'), 2), (2, 3): (hx('9be36a'), 2)}


def coil(ctx, x, y, ph):
    for i in range(4):
        xx = x - 36 + i * 24 + (ph * 24) % 24
        ctx.new_path(); ctx.arc(xx, y, 13, math.pi * 0.1, math.pi * 1.9); setc(ctx, hx('c9d2de')); ctx.set_line_width(5); ctx.stroke()
        ctx.new_path(); ctx.arc(xx, y, 13, math.pi * 0.1, math.pi * 1.9); setc(ctx, (0.3, 0.3, 0.4, 0.5)); ctx.set_line_width(1.5); ctx.stroke()


def dangle_pos(i, sw):
    cx, cy = slot(TC, TR)
    return cx + (10 if i % 2 else -6) * (i > 0), cy + 34 + 34 * i, 0.42 + 0.12 * (i % 2) - 0.08 * (i > 1) + sw


def machine(ctx, f, lf, shake_rot=0.0, show_hang=True, glow=0.0, flap=0.0):
    """vending machine + its contents (uses the global chain state)"""
    ctx.save()
    ctx.translate(VX, FLOOR); ctx.rotate(shake_rot); ctx.translate(-VX, -FLOOR)
    # shadow + body
    ellipse(ctx, VX, FLOOR + 6, 250, 26); setc(ctx, (0, 0, 0, 0.18)); ctx.fill()
    rect_r(ctx, MX0, MTOP, MX1 - MX0, FLOOR - MTOP + 4, 34); fl(ctx, hx('ff5a6e'), 8)
    rect_r(ctx, MX0 + 16, MTOP + 14, MX1 - MX0 - 32, 36, 14); fl(ctx, hx('ffd0d6'), 4)
    for k in range(7):
        sparkle(ctx, MX0 + 60 + k * 50, MTOP + 32, 10, GOLD if k % 2 else WHITE)
    # glass interior
    rect_r(ctx, GX0 - 8, GY0 - 8, GX1 - GX0 + 16, GY1 - GY0 + 16, 16); fl(ctx, hx('2c3557'), 6)
    ctx.save(); rect_r(ctx, GX0, GY0, GX1 - GX0, GY1 - GY0, 10); ctx.clip()
    ctx.rectangle(GX0, GY0, GX1 - GX0, GY1 - GY0); setc(ctx, hx('3a4670')); ctx.fill()
    ph = coil_phase(f)
    n, mv, drop = chain(f)
    sw = 0.06 * math.sin(lf * 0.35) + 0.25 * shake_rot * 10
    for r in range(ROWS):
        y = GY0 + SH * (r + 1) - 10
        ctx.rectangle(GX0, y, GX1 - GX0, 10); setc(ctx, hx('aab6c8')); ctx.fill()
        for c in range(COLS):
            x, yy = slot(c, r)
            coil(ctx, x, y - 10, ph if (c, r) == (TC, TR) else 0)
            col, kd = SNACK[(c, r)]
            if (c, r) == (TC, TR):
                continue
            packet(ctx, x, yy, col, 0.72, 0.03 * math.sin(c + r), kd)
    # target slot: seated bag (always a fresh one behind), hanging chain, moving bag, falling bags
    col, kd = SNACK[(TC, TR)]
    cx, cy = slot(TC, TR)
    if mv is None:
        packet(ctx, cx, cy, col, 0.72, 0.0, kd)
    if show_hang and drop is None:
        for i in range(n):
            x, y, a = dangle_pos(i, sw * (1 + 0.4 * i))
            packet(ctx, x, y, col, 0.74, a, kd)
    if mv is not None:
        x, y, a = dangle_pos(n, sw)
        m = eio(mv)
        if drop is None and n < 3:
            packet(ctx, lerp(cx, x, m), lerp(cy, y, m), col, 0.74, lerp(0, a, m), kd)
        else:
            packet(ctx, lerp(cx, x, m), lerp(cy, y, m), col, 0.74, lerp(0, a, m), kd)
            packet(ctx, cx, cy, col, 0.72 * m, 0, kd) if m > 0.6 else None
    if drop is not None:
        for i in range(4):
            t = drop - i * 4
            x, y, a = dangle_pos(min(i, 3), 0)
            if t < 0:
                packet(ctx, x, y, col, 0.74, a, kd)
            else:
                packet(ctx, x, y + 2.2 * t * t, col, 0.74, a + 0.3 * t, kd)
        packet(ctx, cx, cy, col, 0.72, 0.0, kd)
    ctx.restore()
    # glass sheen
    ctx.save(); rect_r(ctx, GX0, GY0, GX1 - GX0, GY1 - GY0, 10); ctx.clip()
    for k, (x0, w) in enumerate(((GX0 + 30, 34), (GX0 + 90, 14), (GX0 + 200, 22))):
        poly(ctx, [(x0, GY0), (x0 + w, GY0), (x0 + w - 160, GY1), (x0 - 160, GY1)]); setc(ctx, (1, 1, 1, 0.14)); ctx.fill()
    ctx.restore()
    rect_r(ctx, GX0, GY0, GX1 - GX0, GY1 - GY0, 10); ink(ctx, 5); ctx.stroke()
    # keypad column
    rect_r(ctx, KX - 40, GY0, 80, 66, 10); fl(ctx, hx('1d2340'), 5)
    text(ctx, "B2" if glow > 0 else "--", KX, GY0 + 34, 34, hx('7fffa0'), ow=0, shadow=False)
    for i in range(3):
        for j in range(2):
            ellipse(ctx, KX - 18 + j * 36, GY0 + 110 + i * 46, 15, 15); fl(ctx, hx('fff0c4') if not (glow > 0 and i == 1 and j == 0) else YEL, 3)
    rect_r(ctx, KX - 28, GY0 + 260, 56, 70, 10); fl(ctx, hx('d8e0ea'), 4)          # coin slot
    rect_r(ctx, KX - 4, GY0 + 272, 8, 44, 3); setc(ctx, INK); ctx.fill()
    rect_r(ctx, KX - 28, GY0 + 360, 56, 40, 10); fl(ctx, hx('d8e0ea'), 4)          # coin return
    # lower panel + flap
    rect_r(ctx, GX0 - 8, GY1 + 40, GX1 - GX0 + 16, 120, 14); fl(ctx, hx('2c3557'), 6)
    ctx.save(); ctx.translate(0, -50 * flap)
    rect_r(ctx, GX0 + 10, GY1 + 56, GX1 - GX0 - 20, 88, 10); fl(ctx, hx('4a5788'), 4)
    rect_r(ctx, (GX0 + GX1) / 2 - 50, GY1 + 70, 100, 14, 6); setc(ctx, hx('aab6c8')); ctx.fill()
    ctx.restore()
    text(ctx, "PUSH", (GX0 + GX1) / 2, GY1 + 196, 30, WHITE, ow=4, shadow=False)
    # little feet
    for x in (MX0 + 40, MX1 - 40):
        rect_r(ctx, x - 22, FLOOR - 6, 44, 18, 6); fl(ctx, hx('3a2a40'), 3)
    ctx.restore()


# ------------------------------------------------------------------ set: school/community hallway
def hallway(ctx, lf):
    wall = hx('dff7ea')
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, wall); ctx.fill()
    rnd = random.Random(95)
    for k in range(80):   # stars on the wallpaper
        sparkle(ctx, rnd.uniform(-300, 2400), rnd.uniform(300, 1150), 9, dark(wall, 0.9))
    # ceiling strip + light
    ctx.rectangle(-3000, -3000, 9000, 3000 + 420); setc(ctx, hx('fff6e0')); ctx.fill()
    rect_r(ctx, -3000, 410, 9000, 22, 4); fl(ctx, hx('ffb86a'), 5)
    # wainscot
    ctx.rectangle(-3000, 1180, 9000, FLOOR - 1180); setc(ctx, hx('9fd8ff')); ctx.fill()
    for i in range(-20, 40):
        rect_r(ctx, i * 180 + 20, 1210, 140, FLOOR - 1250, 10); ink(ctx, 3); ctx.stroke()
    ctx.move_to(-3000, 1180); ctx.line_to(6000, 1180); ink(ctx, 5); ctx.stroke()
    rect_r(ctx, -3000, 1170, 9000, 20, 4); fl(ctx, hx('ffd36a'), 4)
    # window with daytime sky
    x, y, w, h = 160, 560, 330, 420
    rect_r(ctx, x, y, w, h, 18); fl(ctx, hx('9fe2ff'), 8)
    for cx_, cy_ in ((x + 90 + 20 * math.sin(lf * 0.02), y + 120), (x + 230, y + 250)):
        for dx, r in ((-30, 30), (0, 42), (34, 30)):
            ellipse(ctx, cx_ + dx, cy_, r, r * 0.8); setc(ctx, WHITE); ctx.fill()
    ellipse(ctx, x + w - 60, y + 70, 34, 34); fl(ctx, GOLD, 4)
    ctx.move_to(x + w / 2, y); ctx.line_to(x + w / 2, y + h); ctx.move_to(x, y + h / 2); ctx.line_to(x + w, y + h / 2); ink(ctx, 7); ctx.stroke()
    rect_r(ctx, x - 20, y + h - 6, w + 40, 26, 6); fl(ctx, WHITE, 5)
    # bulletin board with kid drawings
    bx, by = 560, 640
    rect_r(ctx, bx, by, 330, 240, 12); fl(ctx, hx('d9a066'), 7)
    for k, (dx, dy, col, a) in enumerate(((20, 22, YEL, -0.08), (120, 30, PINK, 0.06), (220, 18, CYAN, -0.04), (40, 130, WHITE, 0.05), (160, 128, hx('c8ffb0'), -0.06))):
        ctx.save(); ctx.translate(bx + dx + 45, by + dy + 42); ctx.rotate(a)
        ctx.rectangle(-45, -42, 90, 84); fl(ctx, col, 3)
        if k == 0:
            ellipse(ctx, 0, 0, 20, 20); fl(ctx, ORANGE, 3)
        elif k == 1:
            poly(ctx, [(-25, 10), (0, -20), (25, 10)]); fl(ctx, RED, 3); ctx.rectangle(-18, 10, 36, 24); fl(ctx, GOLD, 3)
        elif k == 2:
            sparkle(ctx, 0, 0, 26, GOLD)
        elif k == 3:
            ctx.move_to(-30, 10); ctx.curve_to(-10, -30, 10, 30, 30, -10); setc(ctx, GREEN); ctx.set_line_width(6); ctx.stroke()
        else:
            ellipse(ctx, 0, 0, 22, 16); fl(ctx, PINK, 3); ellipse(ctx, 8, -4, 3, 3); setc(ctx, INK); ctx.fill()
        ellipse(ctx, 0, -38, 6, 6); fl(ctx, RED, 2)
        ctx.restore()
    # wall clock
    ellipse(ctx, 1080, 560, 50, 50); fl(ctx, WHITE, 6)
    ctx.move_to(1080, 560); ctx.line_to(1080 + 30 * math.sin(lf * 0.05), 560 - 30 * math.cos(lf * 0.05))
    ctx.move_to(1080, 560); ctx.line_to(1096, 546); ink(ctx, 5); ctx.stroke()
    # star bunting
    for k in range(9):
        bx_ = 520 + k * 120
        poly(ctx, [(bx_, 440), (bx_ + 90, 440), (bx_ + 45, 510)]); fl(ctx, (PINK, GOLD, CYAN, GREEN, ORANGE)[k % 5], 3)
    # doorway on the right with a round window
    rect_r(ctx, 1540, 620, 330, 950, 12); fl(ctx, hx('ffe8b0'), 7)
    rect_r(ctx, 1570, 650, 270, 920, 8); setc(ctx, hx('ffcf7a')); ctx.fill()
    ellipse(ctx, 1705, 820, 60, 60); fl(ctx, hx('bff0ff'), 5)
    ellipse(ctx, 1600, 1130, 14, 14); fl(ctx, GOLD, 3)
    # floor tiles
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('fff0d6')); ctx.fill()
    for i in range(-20, 40):
        for j in range(4):
            if (i + j) % 2:
                ctx.rectangle(i * 110 - j * 30, FLOOR + j * 60, 110, 60); setc(ctx, hx('ffd0a0')); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(6000, FLOOR); ink(ctx, 5); ctx.stroke()
    # potted plant + bench
    rect_r(ctx, 470, 1440, 90, 120, 12); fl(ctx, hx('ff8a5c'), 5)
    for a in (-0.8, -0.35, 0.1, 0.55, 0.95):
        ellipse(ctx, 515 + 70 * math.sin(a), 1380 - 40 * math.cos(a), 18, 52, a); fl(ctx, GREEN, 3)
    rect_r(ctx, 1500, 1440, 300, 30, 10); fl(ctx, hx('a0603a'), 5)
    for x in (1530, 1770):
        rect_r(ctx, x - 8, 1468, 16, 92, 5); fl(ctx, hx('7a4a2e'), 3)


def stand(ctx, ch, x, k, p, f_=1, dy=0):
    return draw(ctx, x, GND - 186 * k + dy, k, f_, ch, p)


def coin(ctx, x, y, s=1.0):
    ellipse(ctx, x, y, 16 * s, 16 * s); fl(ctx, GOLD, 3)
    ellipse(ctx, x, y, 9 * s, 9 * s); ink(ctx, 2); ctx.stroke()


def bag_armful(ctx, x, y, lf):
    col, kd = SNACK[(TC, TR)]
    for i, (dx, dy, a) in enumerate(((-34, -10, -0.3), (30, -16, 0.25), (-10, -40, -0.1), (16, 10, 0.4))):
        packet(ctx, x + dx, y + dy + 3 * math.sin(lf * 0.4 + i), col, 0.62, a, kd)


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = 1.04 + 0.04 * eio(pop(lf, 0, 40))
    rot = 0.035 * math.sin(lf * 1.3)
    ctx.save(); cam(ctx, 1080, 1150, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    hallway(ctx, lf)
    dog(ctx, 1580, GND + 5, 0.75, -1, lf)
    machine(ctx, f, lf, rot)
    sw = math.sin(lf * 1.3)
    d = stand(ctx, DAD, DADX + 8 * sw, KDAD, P(eye='glare', mouth='scream', lsh=92 + 8 * sw, lel=-8, rsh=78 + 8 * sw, rel=-4, torso=8, head=-6), 1)
    sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.5, lf, 1.0)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"COME... ON...!!\"", 540, 1450, 120, WHITE, -0.04, t)
    label(ctx, "*SHAKE! SHAKE!*", 540, 520, 80, ORANGE, 0.04, 1 if lf == f else pop(lf, 2, 5))


# ------------------------------------------------------------------ shot 2: the first coin
def first_try(ctx, f, il):
    # il 0..140: 0-24 walk in "Snack time!" ; 28 *clink* ; 36 *boop* ; 40-70 macro coil ; 68 *creak* stop ; 80 "...NO." ;
    #            100 *clink* ; 106-126 2nd bag ; 128 "...TWO?!"
    sx, sy = slot(TC, TR)
    mac = eio(pop(il, 38, 46)) * (1 - eio(pop(il, 76, 82)))
    cx = lerp(1080, sx - 10, mac); cy = lerp(1150, sy + 60, mac); z = lerp(1.06, 2.5, mac)
    ctx.save(); cam(ctx, cx, cy, z, 0, shake_at(il, [68, 128], 8, 6), f)
    hallway(ctx, il)
    machine(ctx, f, il, 0, glow=1.0 if 36 <= il < 70 or 104 <= il < 128 else 0)
    wx = lerp(DADX - 420, DADX, eio(pop(il, 0, 22)))
    bob = 10 * abs(math.sin(il * 0.5)) * (il < 22)
    reach = (26 <= il < 40) or (98 <= il < 108)
    if il < 80:
        p = P(eye='happy' if il < 68 else 'shock', mouth='grin' if il < 68 else 'flat',
              lsh=88 if reach else 20, lel=-10 if reach else -20, rsh=-20, rel=-30, head=-4)
    else:
        p = P(eye='glare' if il < 120 else 'shock', mouth='flat' if il < 120 else 'scream',
              lsh=88 if reach else 20, lel=-10 if reach else 10, rsh=-20, rel=-10, head=-6)
    d = stand(ctx, DAD, wx, KDAD, p, 1, -bob)
    if 22 <= il < 30 or 96 <= il < 102:
        coin(ctx, d['back'][0] + 10, d['back'][1] - 10)
    if il >= 128:
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.7, il, 1.0)
    ctx.restore()
    if il < 26:
        label(ctx, "\"Snack time!\"", 540, 1450, 120, WHITE, -0.03, pop(il, 2, 6))
    elif il < 38:
        label(ctx, "*clink*", 540, 560, 90, GOLD, -0.05, pop(il, 28, 31))
        label(ctx, "*boop*", 540, 1450, 90, CYAN, 0.04, pop(il, 34, 37))
    elif il < 68:
        label(ctx, "*whirrrr...*", 540, 1450, 100, CYAN, 0.03, pop(il, 42, 45))
    elif il < 80:
        label(ctx, "*...creak.*", 540, 1450, 110, ORANGE, -0.04, pop(il, 68, 71))
    elif il < 98:
        label(ctx, "\"...NO.\"", 540, 1450, 150, WHITE, 0.03, pop(il, 80, 83))
    elif il < 128:
        label(ctx, "*clink*", 540, 560, 90, GOLD, -0.05, pop(il, 100, 103))
        label(ctx, "\"ONE more try...\"", 540, 1450, 110, WHITE, 0.03, pop(il, 102, 106))
    else:
        label(ctx, "\"...TWO?!\"", 540, 1450, 150, RED, -0.03, pop(il, 128, 131))


def s2(ctx, f):
    first_try(ctx, f, f - 60)


# ------------------------------------------------------------------ shot 3: shake montage + double or nothing
def montage(ctx, f, il):
    # il 0..130: 0-25 SHAKE ; 25-50 THUNK shoulder ; 50-80 BONK kick + OW hop ; 82 "Double or NOTHING." ; 90 *clink* ;
    #            96-116 3rd bag ; 116 "...THREE?!"
    j = min(2, il // 25) if il < 80 else 3
    rot = (-6, 5, -4, 0)[j]
    mrot = 0
    if j == 0:
        mrot = 0.05 * math.sin(il * 1.6)
    elif j == 1:
        mrot = 0.04 * math.sin(pop(il, 30, 40) * math.pi)
    elif j == 2:
        mrot = 0.02 * math.sin(pop(il, 52, 60) * math.pi)
    zz = 1.1 if j < 3 else 1.06
    ctx.save(); cam(ctx, 1060, 1160, zz, rot, shake_at(il, [0, 30, 52, 116], 8, 9), f)
    hallway(ctx, il)
    dog(ctx, 1580, GND + 5, 0.75, -1, il)
    machine(ctx, f, il, mrot, glow=1.0 if 92 <= il < 116 else 0)
    if j == 0:
        sw = math.sin(il * 1.6)
        d = stand(ctx, DAD, DADX + 10 * sw, KDAD, P(eye='glare', mouth='scream', lsh=92, lel=-8, rsh=80, rel=-4, torso=8), 1)
    elif j == 1:
        lean = 40 * math.sin(pop(il, 25, 40) * math.pi)
        d = stand(ctx, DAD, DADX + 20 + lean, KDAD, P(eye='glare', mouth='scream', lsh=-30, lel=-20, rsh=-20, rel=-30, torso=22), 1)
    elif j == 2:
        hop = 30 * abs(math.sin(il * 0.6)) * (il >= 60)
        if il < 60:
            d = stand(ctx, DAD, DADX + 20, KDAD, P(eye='glare', mouth='scream', rhip=-70, rkn=-10, lsh=-40, rsh=40, torso=-6), 1)
        else:
            d = stand(ctx, DAD, DADX - 40, KDAD, P(eye='shock', mouth='scream', lhip=40, lkn=-90, lsh=40, lel=60, rsh=-40, rel=-20, head=8), 1, -hop)
    else:
        reach = 88 <= il < 96
        p = P(eye='smug' if il < 116 else 'shock', mouth='smile' if il < 116 else 'scream',
              lsh=88 if reach else 30, lel=-10 if reach else -40, rsh=-20, rel=-20)
        d = stand(ctx, DAD, DADX, KDAD, p, 1)
        if 84 <= il < 92:
            coin(ctx, d['back'][0] + 10, d['back'][1] - 10)
        if il >= 116:
            twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.7, il, 1.1)
    ctx.restore()
    if il < 80:
        word = ("*SHAKE! SHAKE!*", "*THUNK!*", "*BONK!*")[j]
        label(ctx, word, 540, (560, 600, 580)[j], 110, (ORANGE, PURPLE, RED)[j], (-0.07, 0.06, -0.05)[j], pop(il, 25 * j + 2, 25 * j + 5))
        if j == 2 and il >= 60:
            label(ctx, "\"OW! OW! OW!\"", 540, 1450, 120, WHITE, 0.03, pop(il, 60, 63))
        elif j < 2:
            label(ctx, "\"DROP... IT...!!\"", 540, 1450, 115, WHITE, 0.03, pop(il, 3, 6))
    elif il < 116:
        label2(ctx, "\"Double or", "NOTHING.\"", WHITE, pop(il, 82, 86), 110, col2=GOLD, y=1430)
        if il >= 90:
            label(ctx, "*clink*", 540, 560, 90, GOLD, -0.05, pop(il, 90, 93))
    else:
        label(ctx, "\"...THREE?!\"", 540, 1450, 150, RED, 0.03, pop(il, 116, 119))


def s3(ctx, f):
    montage(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: POV from inside the machine (the one close-up)
def s4(ctx, f):
    il = f - 330
    # blurred hallway behind, through the glass
    ctx.save(); cam(ctx, 900, 1050, 1.3, 0, 0, f)
    hallway(ctx, il)
    ctx.restore()
    ctx.rectangle(0, 0, W, H); setc(ctx, (0.17, 0.2, 0.35, 0.35)); ctx.fill()
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.08 * eio(il / 70), 0, shake_at(il, [0, 36], 6, 8), f)
    squish = 0.92 if il >= 36 else 1.0
    ctx.save(); ctx.translate(540, 1080); ctx.scale(1.0, squish); ctx.translate(-540, -1080)
    face(ctx, DAD, P(eye='glare', mouth='flat' if il < 36 else 'scream'), 600, 1080, 200, 0.0)
    ctx.restore()
    # nose smudge on the glass
    ellipse(ctx, 620, 1110, 70, 40); setc(ctx, (1, 1, 1, 0.18)); ctx.fill()
    twitch(ctx, 600 + 200 * 0.95, 1080 - 200 * 0.7, il, 1.6)
    # glass streaks
    for x0, w in ((120, 70), (300, 26), (820, 50)):
        poly(ctx, [(x0, 0), (x0 + w, 0), (x0 + w - 400, H), (x0 - 400, H)]); setc(ctx, (1, 1, 1, 0.1)); ctx.fill()
    # foreground: the coil shelf + the dangling chain, huge
    ctx.rectangle(-50, 640, 1200, 34); fl(ctx, hx('aab6c8'), 5)
    for i in range(5):
        ctx.new_path(); ctx.arc(120 + i * 80, 620, 44, math.pi * 0.1, math.pi * 1.9); setc(ctx, hx('c9d2de')); ctx.set_line_width(12); ctx.stroke()
    col, kd = SNACK[(TC, TR)]
    sw = 0.06 * math.sin(il * 0.3)
    for i, (x, y, a) in enumerate(((250, 690, 0.5), (300, 810, 0.65), (230, 910, 0.38))):
        packet(ctx, x, y, col, 1.6, a + sw * (1 + i * 0.5), kd)
    ctx.restore()
    if il < 36:
        label(ctx, "\"It's... MOCKING me.\"", 540, 1450, 105, WHITE, -0.03, pop(il, 3, 7))
    else:
        label(ctx, "\"...MOCKING!!\"", 540, 1450, 150, RED, 0.03, pop(il, 36, 39))


# ------------------------------------------------------------------ shot 5: the kid buys one -> loop
def kid_wins(ctx, f, il):
    # il 0..130: card ; 0-24 kid walks in ; 28 *clink* ; 36 *boop* ; 40-58 push ; 58-74 *THUNK x4* ; 78 flap ;
    #            86 "Thanks, DAD!" ; 106 "...HOW?!"
    ctx.save(); cam(ctx, 1060, 1150, 1.06, 0, shake_at(il, [58, 62, 66, 70], 5, 8), f)
    hallway(ctx, il)
    machine(ctx, f, il, 0.012 * math.sin(il * 2) * (58 <= il < 76), glow=1.0 if 36 <= il < 58 else 0, flap=pop(il, 76, 80) * (1 - pop(il, 84, 88)))
    # Dad stepped back, arms crossed
    dp = P(eye='smug' if il < 58 else 'shock', mouth='smile' if il < 58 else ('scream' if il >= 100 else 'open'),
           lsh=50, lel=-120, rsh=40, rel=-110) if il < 58 else P(eye='shock', mouth='scream' if il >= 100 else 'open', lsh=150, lel=-20, rsh=160, rel=-10, head=-6)
    d = stand(ctx, DAD, DADX - 130, KDAD, dp, 1)
    if il >= 100:
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.7, il, 1.1)
    kx = lerp(1700, VX - 240, eio(pop(il, 0, 24)))
    bob = 8 * abs(math.sin(il * 0.5)) * (il < 24)
    reach = 26 <= il < 40
    if il < 80:
        k = stand(ctx, KID, kx, KKID, P(eye='happy', mouth='grin', lsh=150 if reach else 20, lel=-10, rsh=-20, rel=-20), -1 if il < 24 else 1, -bob)
        if 20 <= il < 30:
            coin(ctx, k['back'][0], k['back'][1] - 10, 0.8)
    else:
        k = stand(ctx, KID, VX - 240, KKID, P(eye='happy', mouth='grin', lsh=70, lel=-80, rsh=60, rel=-80), -1)
        bag_armful(ctx, k['front'][0] - 10, k['front'][1] - 10, il)
        sparkle(ctx, k['head'][0] + 70, k['head'][1] - 80, 20, GOLD)
    ctx.restore()
    card(ctx, 'p2', il, 0, 56)
    if il < 40:
        label(ctx, "*clink*", 540, 1450, 90, GOLD, -0.05, pop(il, 28, 31))
    elif il < 58:
        label(ctx, "*whirrrr...*", 540, 1450, 100, CYAN, 0.03, pop(il, 40, 43))
    elif il < 80:
        label(ctx, "*THUNK! THUNK! THUNK! THUNK!*", 540, 600, 84, RED, -0.05, pop(il, 58, 61))
    elif il < 100:
        label(ctx, "\"Thanks, DAD!\"", 540, 1450, 120, WHITE, 0.03, pop(il, 84, 87))
    else:
        label(ctx, "\"...HOW?!\"", 540, 1450, 150, RED, -0.03, pop(il, 100, 103))


def again(ctx, f, il):
    # il 0..100 (f 530..630): kid strolls off munching ; 20 *clink* ; 20-40 coil ; 40 dangles *creak* ; 56 "...of COURSE."
    ctx.save(); cam(ctx, 1080, 1150, 1.08 + 0.05 * eio(pop(il, 40, 100)), 0, shake_at(il, [40], 6, 6), f)
    hallway(ctx, il)
    dog(ctx, 1580, GND + 5, 0.75, -1, il)
    machine(ctx, f, il, 0, glow=1.0 if 16 <= il < 40 else 0)
    kx = lerp(VX + 260, 1950, eio(pop(il, 0, 50)))
    k = stand(ctx, KID, kx, KKID, P(eye='happy', mouth='open' if (il // 4) % 2 else 'grin', lsh=70, lel=-80, rsh=60, rel=-80), 1, -6 * abs(math.sin(il * 0.5)))
    bag_armful(ctx, k['front'][0] + 10, k['front'][1] - 10, il)
    reach = 10 <= il < 22
    p = P(eye='smug' if il < 40 else 'glare', mouth='smile' if il < 40 else 'flat', lsh=88 if reach else 20, lel=-10 if reach else 10, rsh=-20, rel=-10)
    d = stand(ctx, DAD, DADX, KDAD, p, 1)
    if 6 <= il < 12:
        coin(ctx, d['back'][0] + 10, d['back'][1] - 10)
    if il >= 44:
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.7, il, 1.0)
    ctx.restore()
    if il < 40:
        label(ctx, "*crunch crunch*", 540, 560, 84, ORANGE, 0.04, pop(il, 2, 5))
        label(ctx, "\"MY turn.\"", 540, 1450, 120, WHITE, -0.03, pop(il, 4, 8))
    elif il < 56:
        label(ctx, "*...creak.*", 540, 1450, 110, ORANGE, -0.04, pop(il, 40, 43))
    else:
        label(ctx, "\"...of COURSE.\"", 540, 1450, 130, WHITE, 0.03, pop(il, 56, 59))


def s5(ctx, f):
    lf = f - 400
    if lf < 130:
        kid_wins(ctx, f, lf)
    elif lf < 230:
        again(ctx, f, lf - 130)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (200, s3), (330, s4), (400, s5)]
CUTS = (60, 200, 330, 400, 530, 630)


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
                              "-i", "out/vending_machine_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
