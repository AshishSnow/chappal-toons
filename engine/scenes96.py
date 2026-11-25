"""'Dad carves the turkey'. Original, general-audience comedy short, 22s.
Hook:   dining-room medium shot: Dad sawing at the holiday turkey, SPARKS flying, Mom + kid behind the table.
        "IT'S... SO... TENDER!!" + caption "DAD CARVES THE TURKEY:".
Beat 1: "Carving? EASY." *shing!* -> first cut *CLANG!* knife + Dad vibrate *BOINNNG* -> macro *KNOCK KNOCK* -> "...a LITTLE firm."
Beat 2: Dutch-tilt tool montage: cleaver *CLANG!*, hand saw *SKREEEE!* spark shower, hammer *BONK!* -> turkey pops up
        and lands *THUNK!* plates jump -> "It's... VERY... TENDER!!"
Turn:   the one close-up: sweaty Dad, ice chips flying "It's... PERFECTLY..." "...COOKED!!"
Twist:  PLOT TWIST: IT'S STILL FROZEN. kid pokes it *tink! tink!* frost spreads, icicles -> Mom "Honey... I said THAW it."
        -> "...THAW?!" -> *DING-DONG!* kid "PIZZA!!" -> family munches pizza, Dad alone "...MORE for ME." -> saw -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face
from scenes58 import sweat, twitch
from scenes65 import dog
from scenes84 import eio
import scenes13
from scenes13 import card as _card13

RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); ICE = hx('bfefff')
DAD = dict(doodle.DAD, shirt=hx('ff8a3d'), pants=hx('3a4a8a'))
MOM = dict(doodle.MOM_G, shirt=hx('2fb8a8'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('8a3cff'), pants=hx('3d7bff'), shoes=hx('ffc93c'))
N = 660
FLOOR, GND = 1560, 1590
TB0, TB1, TTOP, TFR = 670, 1580, 1390, 1425   # table x-range, back edge, front edge
TX, TY = 1215, 1412                            # turkey centre (platter)
DADX, MOMX, KIDX = 995, 765, 1440
KDAD, KMOM, KKID = 1.1, 0.98, 0.82

CAPS = {'p1': [[("DAD ", OUT), ("CARVES ", RED), ("THE TURKEY:", ORANGE)]],
        'p2': [[("PLOT TWIST:", RED)], [("IT'S STILL ", OUT), ("FROZEN.", BLUE)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def turkey(ctx, x, y, s=1.0, frost=0.0, rot=0.0, platter=True):
    if platter:
        ellipse(ctx, x, y + 6, 190 * s, 34 * s); fl(ctx, WHITE, 5)
        ellipse(ctx, x, y + 2, 150 * s, 22 * s); ctx.set_line_width(2.5); setc(ctx, hx('9fd8ff')); ctx.stroke()
        for dx in (-130, 128):   # lettuce frill
            ellipse(ctx, x + dx * s, y - 4 * s, 34 * s, 16 * s, 0.3 * (1 if dx > 0 else -1)); fl(ctx, hx('7fd65a'), 3)
    ctx.save(); ctx.translate(x, y - 8 * s); ctx.rotate(rot); ctx.scale(s, s)
    body = hx('e0a25a')
    # drumsticks (behind)
    for sd in (-1, 1):
        ctx.save(); ctx.translate(sd * 92, -40); ctx.rotate(sd * 0.75)
        ellipse(ctx, 0, 0, 34, 52); fl(ctx, dark(body, 0.9), 4)
        rect_r(ctx, -9, -86, 18, 46, 6); fl(ctx, hx('fff6e8'), 3)
        for k in range(5):   # paper frill
            ellipse(ctx, -12 + k * 6, -92, 7, 10); fl(ctx, WHITE, 2)
        ctx.restore()
    # body
    ctx.new_path(); ctx.move_to(-130, 0); ctx.curve_to(-140, -110, 130, -140, 132, -10); ctx.curve_to(120, 12, -120, 14, -130, 0); ctx.close_path()
    fl(ctx, body, 5)
    ctx.new_path(); ctx.move_to(-90, -60); ctx.curve_to(-60, -100, 20, -110, 60, -96); setc(ctx, (1, 1, 1, 0.45)); ctx.set_line_width(12); ctx.stroke()
    for sd in (-1, 1):   # wings
        ellipse(ctx, sd * 64, -28, 40, 22, -sd * 0.3); fl(ctx, dark(body, 0.92), 3)
    # frost
    if frost > 0:
        ctx.new_path(); ctx.move_to(-130, 0); ctx.curve_to(-140, -110, 130, -140, 132, -10); ctx.curve_to(120, 12, -120, 14, -130, 0); ctx.close_path()
        setc(ctx, ICE + (0.75 * frost,)); ctx.fill()
        rnd = random.Random(7)
        for k in range(int(9 * frost)):
            sparkle(ctx, rnd.uniform(-100, 100), rnd.uniform(-95, -10), rnd.uniform(9, 15), WHITE)
        for k in range(7):   # icicles
            ix = -100 + k * 33
            ln = (22 + 14 * (k % 3)) * frost
            poly(ctx, [(ix - 8, 6), (ix + 8, 6), (ix, 6 + ln)]); fl(ctx, ICE, 2)
    ctx.restore()


def sparks(ctx, x, y, lf, n=10, r=90, seed=0):
    rnd = random.Random(lf * 13 + seed)
    for k in range(n):
        a = rnd.uniform(-math.pi, 0.2); d0 = rnd.uniform(10, 30); d1 = d0 + rnd.uniform(30, r)
        ctx.move_to(x + d0 * math.cos(a), y + d0 * math.sin(a)); ctx.line_to(x + d1 * math.cos(a), y + d1 * math.sin(a))
        setc(ctx, (GOLD, YEL, ORANGE, WHITE)[k % 4]); ctx.set_line_width(rnd.uniform(4, 8)); ctx.stroke()
    sparkle(ctx, x, y, 26, YEL)


def ice_chips(ctx, x, y, lf, n=6, seed=0):
    rnd = random.Random(lf * 7 + seed)
    for k in range(n):
        a = rnd.uniform(-math.pi, 0); d = rnd.uniform(40, 120)
        cx_, cy_ = x + d * math.cos(a), y + d * math.sin(a)
        poly(ctx, [(cx_, cy_ - 10), (cx_ + 8, cy_), (cx_, cy_ + 10), (cx_ - 8, cy_)]); fl(ctx, ICE, 2)


def knife(ctx, x, y, a, s=1.0, cleaver=False):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -46, -12, 56, 24, 9); fl(ctx, hx('8a4a2a'), 4)
    for k in (-30, -10):
        ellipse(ctx, k, 0, 4, 4); setc(ctx, GOLD); ctx.fill()
    if cleaver:
        rect_r(ctx, 8, -20, 130, 70, 8); fl(ctx, hx('dfe7f0'), 4)
        ellipse(ctx, 118, -2, 9, 9); fl(ctx, hx('9aa8b8'), 2)
    else:
        ctx.new_path(); ctx.move_to(8, -14); ctx.line_to(150, -6); ctx.curve_to(168, -4, 170, 4, 158, 10); ctx.line_to(8, 14); ctx.close_path()
        fl(ctx, hx('dfe7f0'), 4)
    ctx.move_to(20, -4); ctx.line_to(120, -2); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def fork(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -40, -9, 50, 18, 7); fl(ctx, hx('8a4a2a'), 3)
    rect_r(ctx, 8, -6, 50, 12, 4); fl(ctx, hx('dfe7f0'), 3)
    for dy in (-12, 0, 12):
        rect_r(ctx, 52, dy - 3, 44, 7, 3); fl(ctx, hx('dfe7f0'), 2)
    ctx.restore()


def saw(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(10, -34); ctx.line_to(220, -12)
    for k in range(14):
        ctx.line_to(220 - k * 15 - 7, 18 + 8); ctx.line_to(220 - k * 15 - 15, 18)
    ctx.line_to(10, 30); ctx.close_path(); fl(ctx, hx('dfe7f0'), 4)
    rect_r(ctx, -50, -40, 70, 76, 22); fl(ctx, RED, 4)
    rect_r(ctx, -30, -20, 30, 36, 10); fl(ctx, hx('fff0dc'), 3)
    ctx.restore()


def hammer(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -30, -10, 170, 20, 8); fl(ctx, hx('d9a066'), 4)
    rect_r(ctx, 120, -46, 50, 92, 10); fl(ctx, hx('8a94a8'), 4)
    ctx.restore()


def pizza_box(ctx, x, y, lf, bites=0):
    poly(ctx, [(x - 150, y + 10), (x + 150, y + 10), (x + 120, y - 60), (x - 120, y - 60)]); fl(ctx, hx('e8c08a'), 5)
    ellipse(ctx, x, y - 24, 118, 30); fl(ctx, hx('f0b050'), 4)
    ellipse(ctx, x, y - 24, 100, 24); fl(ctx, hx('ffd36a'), 3)
    rnd = random.Random(4)
    for k in range(7):
        ellipse(ctx, x + rnd.uniform(-80, 80), y - 24 + rnd.uniform(-12, 12), 11, 6); fl(ctx, RED, 2)
    for k in range(bites):
        poly(ctx, [(x, y - 24), (x + 100 * math.cos(-0.4 + k * 0.7), y - 24 + 24 * math.sin(-0.4 + k * 0.7)),
                   (x + 100 * math.cos(0.3 + k * 0.7), y - 24 + 24 * math.sin(0.3 + k * 0.7))]); setc(ctx, hx('e8c08a')); ctx.fill()


def slice_(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(0, 0), (90, -22), (90, 22)]); fl(ctx, hx('ffd36a'), 3)
    rect_r(ctx, 82, -24, 16, 48, 6); fl(ctx, hx('f0b050'), 3)
    for dx, dy in ((40, -4), (66, 8)):
        ellipse(ctx, dx, dy, 7, 7); fl(ctx, RED, 2)
    ctx.restore()


# ------------------------------------------------------------------ set: cosy dining room
def room(ctx, lf):
    wall = hx('fff0d8')
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, wall); ctx.fill()
    rnd = random.Random(96)
    for k in range(90):   # stars + dots wallpaper
        x, y = rnd.uniform(300, 1900), rnd.uniform(250, 1250)
        if k % 2:
            sparkle(ctx, x, y, 9, hx('ffd9a8'))
        else:
            ellipse(ctx, x, y, 6, 6); setc(ctx, hx('ffcfa0')); ctx.fill()
    # wainscot
    ctx.rectangle(-3000, 1180, 9000, FLOOR - 1180); setc(ctx, hx('c8e6a0')); ctx.fill()
    for i in range(-20, 40):
        rect_r(ctx, i * 170 + 18, 1210, 134, FLOOR - 1250, 10); ink(ctx, 3); ctx.stroke()
    rect_r(ctx, -3000, 1170, 9000, 20, 4); fl(ctx, hx('ffb36a'), 4)
    # window with an autumn tree + falling leaves
    x, y, w, h = 560, 600, 300, 420
    rect_r(ctx, x, y, w, h, 18); fl(ctx, hx('a8e4ff'), 8)
    ctx.save(); rect_r(ctx, x, y, w, h, 18); ctx.clip()
    rect_r(ctx, x + 120, y + 250, 36, 200, 8); fl(ctx, hx('8a5a3a'), 4)
    for dx, dy, r, c in ((140, 210, 90, ORANGE), (90, 250, 60, hx('ff5a3a')), (200, 240, 64, GOLD)):
        ellipse(ctx, x + dx, y + dy, r, r * 0.85); fl(ctx, c, 4)
    for k in range(5):
        lx = x + (40 + k * 60 + 20 * math.sin(lf * 0.08 + k)) % w
        ly = y + (lf * 2.2 + k * 90) % h
        ellipse(ctx, lx, ly, 10, 6, lf * 0.1 + k); fl(ctx, (ORANGE, GOLD, RED)[k % 3], 2)
    ctx.restore()
    ctx.move_to(x + w / 2, y); ctx.line_to(x + w / 2, y + h); ctx.move_to(x, y + h * 0.45); ctx.line_to(x + w, y + h * 0.45); ink(ctx, 7); ctx.stroke()
    rect_r(ctx, x - 20, y + h - 6, w + 40, 26, 6); fl(ctx, WHITE, 5)
    # picture frame: a doodled cat portrait
    px, py = 1330, 650
    rect_r(ctx, px, py, 230, 190, 10); fl(ctx, hx('ffcf7a'), 7)
    rect_r(ctx, px + 20, py + 20, 190, 150, 6); fl(ctx, hx('ffe0f0'), 3)
    ellipse(ctx, px + 115, py + 110, 46, 40); fl(ctx, hx('ffa64d'), 3)
    poly(ctx, [(px + 78, py + 90), (px + 88, py + 56), (px + 104, py + 80)]); fl(ctx, hx('ffa64d'), 3)
    poly(ctx, [(px + 126, py + 80), (px + 142, py + 56), (px + 152, py + 90)]); fl(ctx, hx('ffa64d'), 3)
    for ex in (-16, 16):
        ellipse(ctx, px + 115 + ex, py + 106, 5, 7); setc(ctx, INK); ctx.fill()
    # paper-leaf garland
    for k in range(10):
        gx = 880 + k * 46; gy = 560 + 26 * math.sin(k / 9 * math.pi)
        ellipse(ctx, gx, gy + 18, 15, 22, 0.4 * ((-1) ** k)); fl(ctx, (ORANGE, GOLD, RED, hx('c86a2a'))[k % 4], 3)
    ctx.move_to(870, 560); ctx.curve_to(980, 610, 1180, 610, 1300, 560); ink(ctx, 3); ctx.stroke()
    # hanging lamp
    ctx.move_to(1200, 0); ctx.line_to(1200, 760); ink(ctx, 4); ctx.stroke()
    poly(ctx, [(1140, 830), (1260, 830), (1230, 760), (1170, 760)]); fl(ctx, hx('ffd36a'), 5)
    ellipse(ctx, 1200, 838, 22, 12); fl(ctx, YEL, 3)
    # sideboard + plant (right) and floor
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('d99a62')); ctx.fill()
    for i in range(-20, 40):
        ctx.move_to(i * 150, FLOOR); ctx.line_to(i * 150 - 60, FLOOR + 400); ink(ctx, 2); ctx.stroke()
    ctx.move_to(-3000, FLOOR); ctx.line_to(6000, FLOOR); ink(ctx, 5); ctx.stroke()
    rect_r(ctx, 1660, 1250, 330, 310, 14); fl(ctx, hx('a8643a'), 6)
    for dx in (0, 165):
        rect_r(ctx, 1675 + dx, 1270, 150, 270, 8); ink(ctx, 3); ctx.stroke()
    rect_r(ctx, 380, 1430, 100, 130, 14); fl(ctx, hx('ff8a5c'), 5)
    for a in (-0.8, -0.35, 0.1, 0.55, 0.95):
        ellipse(ctx, 430 + 70 * math.sin(a), 1370 - 40 * math.cos(a), 18, 52, a); fl(ctx, GREEN, 3)


def table(ctx, lf, jump=0.0, candles=False):
    # top surface + cloth
    poly(ctx, [(TB0 + 30, TTOP), (TB1 - 30, TTOP), (TB1, TFR), (TB0, TFR)]); fl(ctx, hx('fff6ea'), 5)
    ctx.new_path(); ctx.move_to(TB0, TFR); ctx.line_to(TB1, TFR); ctx.line_to(TB1 + 6, FLOOR - 40)
    for k in range(12):
        x0 = TB1 + 6 - k * (TB1 - TB0 + 12) / 12
        ctx.curve_to(x0 - 20, FLOOR - 10, x0 - (TB1 - TB0 + 12) / 12 + 20, FLOOR - 10, x0 - (TB1 - TB0 + 12) / 12, FLOOR - 40)
    ctx.close_path(); fl(ctx, hx('ff7a6a'), 5)
    for k in range(7):   # checks
        x0 = TB0 + 50 + k * 160
        ctx.rectangle(x0, TFR + 6, 60, FLOOR - TFR - 60); setc(ctx, (1, 1, 1, 0.35)); ctx.fill()
    # plates, glasses, candles, mini pumpkins
    j = -26 * jump
    for x in (TB0 + 120, TB1 - 140):
        ellipse(ctx, x, TTOP + 22 + j, 70, 14); fl(ctx, WHITE, 4)
    for x in (TB0 + 230, TB1 - 260):
        rect_r(ctx, x - 16, TTOP - 50 + j * 1.3, 32, 64, 8); fl(ctx, hx('d8f4ff'), 3)
        rect_r(ctx, x - 14, TTOP - 20 + j * 1.3, 28, 32, 6); setc(ctx, (1, 0.6, 0.3, 0.6)); ctx.fill()
    if candles:
        for x in (TB0 + 330, TB1 - 380):
            rect_r(ctx, x - 10, TTOP - 70 + j, 20, 80, 5); fl(ctx, hx('fff2b0'), 3)
            fl_ = 1 + 0.15 * math.sin(lf * 0.9 + x)
            ellipse(ctx, x, TTOP - 84 + j, 8 * fl_, 16 * fl_); fl(ctx, ORANGE, 2)
            ellipse(ctx, x, TTOP - 80 + j, 4, 8); setc(ctx, YEL); ctx.fill()
    for x in (TB0 + 40, TB1 - 30):
        ellipse(ctx, x, TTOP + 2 + j, 34, 26); fl(ctx, ORANGE, 3)
        rect_r(ctx, x - 4, TTOP - 34 + j, 8, 14, 3); fl(ctx, GREEN, 2)


def stand(ctx, ch, x, k, p, f_=1, dy=0):
    return draw(ctx, x, GND - 186 * k + dy, k, f_, ch, p)


def family(ctx, lf, mp=None, kp=None, mom_f=1, kid_f=-1):
    m = stand(ctx, MOM, MOMX, KMOM, mp or P(eye='normal', mouth='flat', lsh=30, lel=-60, rsh=20, rel=-50), mom_f)
    k = stand(ctx, KID, KIDX, KKID, kp or P(eye='normal', mouth='flat', lsh=20, lel=-30, rsh=20, rel=-30), kid_f, -70)
    return m, k


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = 1.1 + 0.04 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, 1110, 1270, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    room(ctx, lf)
    family(ctx, lf, P(eye='shock', mouth='open', lsh=150, lel=-30, rsh=140, rel=-40), P(eye='shock', mouth='open', lsh=150, lel=-160, rsh=150, rel=-160))
    sw = math.sin(lf * 1.4)
    d = stand(ctx, DAD, DADX, KDAD, P(eye='glare', mouth='scream', rsh=132 + 6 * sw, rel=-10, lsh=118, lel=30, torso=10, head=-4), 1)
    table(ctx, lf)
    turkey(ctx, TX, TY)
    hx_, hy = d['front']
    knife(ctx, hx_ + 26 * sw, hy, 0.35)
    sparks(ctx, TX - 40 + 26 * sw, TY - 120, lf)
    sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.5, lf, 1.0)
    dog(ctx, 1490, GND + 8, 0.6, -1, lf)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"IT'S... SO... TENDER!!\"", 540, 1500, 108, WHITE, -0.04, t)
    label(ctx, "*SKREEEE!*", 540, 560, 84, ORANGE, 0.04, 1 if lf == f else pop(lf, 2, 5))


# ------------------------------------------------------------------ shot 2: the first cut
def first_try(ctx, f, il):
    # il 0..140: 0-30 flourish ; 34 CLANG + vibrate ; 62-100 macro knock knock ; 100-140 "...a LITTLE firm."
    mac = eio(pop(il, 60, 68)) * (1 - eio(pop(il, 98, 104)))
    cx = lerp(1110, TX - 40, mac); cy = lerp(1270, TY - 120, mac); z = lerp(1.12, 2.2, mac)
    ctx.save(); cam(ctx, cx, cy, z, 0, shake_at(il, [34, 70, 82], 10, 9), f)
    room(ctx, il)
    family(ctx, il)
    vib = 12 * math.sin(il * 3.2) * (1 - pop(il, 34, 58)) * (il >= 34)
    if il < 34:
        up_ = eio(pop(il, 0, 14))
        p = P(eye='smug', mouth='grin', rsh=lerp(60, 170, up_) if il < 28 else lerp(170, 120, pop(il, 28, 34)), rel=-20,
              lsh=lerp(40, 160, up_), lel=-20, head=-4)
    elif il < 60:
        p = P(eye='shock', mouth='scream', rsh=150, rel=-40, lsh=150, lel=-30, head=6)
    elif il < 100:
        kn = pop(il, 70, 76) + pop(il, 82, 88)
        p = P(eye='normal', mouth='flat', rsh=120 + 12 * math.sin(kn * math.pi), rel=-30, lsh=30, lel=-20, torso=8)
    else:
        p = P(eye='glare', mouth='grin', rsh=40, rel=-40, lsh=30, lel=-20)
    d = stand(ctx, DAD, DADX + vib, KDAD, p, 1)
    table(ctx, il)
    turkey(ctx, TX, TY)
    hx_, hy = d['front']
    if il < 34:
        knife(ctx, hx_, hy, -1.2 if il < 28 else lerp(-1.2, 0.4, pop(il, 28, 34)))
        fork(ctx, d['back'][0], d['back'][1], -1.4)
        if 10 <= il < 30:
            sparkle(ctx, hx_ + 40, hy - 160, 30 * (1 - pop(il, 10, 30)) + 8, WHITE)
    elif il < 60:
        knife(ctx, hx_ + vib * 2, hy, -0.8 + 0.4 * math.sin(il * 3.0) * (1 - pop(il, 34, 58)))
        if il < 42:
            sparks(ctx, TX - 40, TY - 120, il, 14, 120)
    elif il < 100:
        for h in (70, 82):
            if h <= il < h + 8:
                for a in (-0.9, -0.4, 0.1):
                    ctx.move_to(hx_ + 30 * math.cos(a) + 20, hy + 30 * math.sin(a) - 10)
                    ctx.line_to(hx_ + 60 * math.cos(a) + 20, hy + 60 * math.sin(a) - 10); ink(ctx, 5); ctx.stroke()
    else:
        knife(ctx, hx_, hy, -1.0)
    if il >= 110:
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.7, il, 1.0)
    ctx.restore()
    if il < 34:
        label(ctx, "\"Carving? EASY.\"", 540, 1500, 115, WHITE, -0.03, pop(il, 2, 6))
        label(ctx, "*shing!*", 540, 560, 84, CYAN, 0.04, pop(il, 12, 15))
    elif il < 60:
        label(ctx, "*CLANG!*", 540, 560, 130, RED, -0.05, pop(il, 34, 37))
        label(ctx, "*BOINNNG*", 540, 1500, 100, ORANGE, 0.03, pop(il, 40, 43))
    elif il < 100:
        label(ctx, "*KNOCK KNOCK*", 540, 1500, 110, PURPLE, 0.03, pop(il, 70, 73))
    else:
        label(ctx, "\"...a LITTLE firm.\"", 540, 1500, 115, WHITE, -0.03, pop(il, 102, 106))


def s2(ctx, f):
    first_try(ctx, f, f - 60)


# ------------------------------------------------------------------ shot 3: tool montage
def montage(ctx, f, il):
    # il 0..130: 0-30 cleaver CLANG ; 30-60 saw SKREEE ; 60-90 hammer BONK -> turkey pops up ; 104 lands THUNK ; "VERY TENDER"
    j = min(3, il // 30)
    rot = (-6, 5, -5, 0)[j]
    hop = 0.0
    if il >= 66:
        t = pop(il, 66, 104)
        hop = 4 * t * (1 - t) * 420 if t < 1 else 0
    jump = 1.0 if 104 <= il < 112 else 0.0
    ctx.save(); cam(ctx, 1110, 1260, 1.18 if j < 3 else 1.12, rot, shake_at(il, [2, 32, 62, 104], 9, 10), f)
    room(ctx, il)
    family(ctx, il, P(eye='glare', mouth='flat', lsh=50, lel=-120, rsh=40, rel=-110),
           P(eye='shock' if j >= 2 else 'normal', mouth='open' if j >= 2 else 'flat', lsh=20, lel=-30, rsh=20, rel=-30))
    if j == 0:
        ch = math.sin(pop(il, 0, 8) * math.pi)
        p = P(eye='glare', mouth='scream', rsh=150 - 40 * eio(pop(il, 0, 4)), rel=-20, lsh=110, lel=30, torso=10)
    elif j == 1:
        sw = math.sin(il * 1.6)
        p = P(eye='glare', mouth='scream', rsh=128 + 8 * sw, rel=-10, lsh=118, lel=30, torso=12)
    elif j == 2:
        p = P(eye='glare', mouth='scream', rsh=170 - 60 * eio(pop(il, 60, 64)), rel=-20, lsh=60, lel=-20, torso=10)
    else:
        p = P(eye='shock' if il < 112 else 'happy', mouth='scream' if il < 112 else 'grin', rsh=150, rel=-40, lsh=150, lel=-30, head=6)
    d = stand(ctx, DAD, DADX, KDAD, p, 1)
    table(ctx, il, jump)
    turkey(ctx, TX, TY - hop, 1.0, rot=0.5 * math.sin(pop(il, 66, 104) * math.pi * 2) if 66 <= il < 104 else 0, platter=False)
    ellipse(ctx, TX, TY + 6, 190, 34); fl(ctx, WHITE, 5)
    if hop <= 0:
        turkey(ctx, TX, TY, platter=False)
    hx_, hy = d['front']
    if j == 0:
        knife(ctx, hx_, hy, lerp(-1.2, 0.3, eio(pop(il, 0, 4))), 1.1, cleaver=True)
        if il < 12:
            sparks(ctx, TX - 30, TY - 120, il, 16, 130)
    elif j == 1:
        sw = math.sin(il * 1.6)
        saw(ctx, hx_ + 40 * sw, hy, 0.3)
        sparks(ctx, TX - 20 + 40 * sw, TY - 120, il, 18, 150, 3)
    elif j == 2:
        hammer(ctx, hx_, hy, lerp(-1.6, 0.2, eio(pop(il, 60, 64))))
        if 62 <= il < 70:
            sparks(ctx, TX, TY - 120, il, 12, 110, 5)
    else:
        hammer(ctx, hx_, hy, -1.2)
        if 104 <= il < 116:
            for a in range(6):
                aa = math.pi + a * math.pi / 5
                ctx.move_to(TX + 160 * math.cos(aa), TY - 40 + 40 * math.sin(aa)); ctx.line_to(TX + 220 * math.cos(aa), TY - 40 + 60 * math.sin(aa)); ink(ctx, 6); ctx.stroke()
    ctx.restore()
    words = ("*CLANG!*", "*SKREEEE!*", "*BONK!*")
    if j < 3:
        label(ctx, words[j], 540, (560, 600, 570)[j], 120, (RED, ORANGE, PURPLE)[j], (-0.07, 0.06, -0.05)[j], pop(il, 30 * j + 1, 30 * j + 4))
        if j < 2:
            label(ctx, "\"TENDER... TENDER...!!\"", 540, 1500, 105, WHITE, 0.03, pop(il, 3, 7))
        else:
            label(ctx, "*BOING!*", 540, 1500, 110, GOLD, 0.03, pop(il, 70, 73))
    elif il < 112:
        label(ctx, "*THUNK!*", 540, 570, 130, RED, 0.04, pop(il, 104, 107))
    else:
        label(ctx, "\"VERY... TENDER!!\"", 540, 1500, 120, WHITE, -0.03, pop(il, 112, 116))


def s3(ctx, f):
    montage(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: the one close-up
def s4(ctx, f):
    il = f - 330
    ctx.save(); cam(ctx, 950, 1000, 1.5, 0, 0, f)
    room(ctx, il)
    ctx.restore()
    ctx.rectangle(0, 0, W, H); setc(ctx, (0.35, 0.2, 0.1, 0.35)); ctx.fill()
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.08 * eio(il / 70), 0, shake_at(il, [0, 36], 6, 8), f)
    face(ctx, DAD, P(eye='glare' if il < 36 else 'shock', mouth='grin' if il < 36 else 'scream'), 560, 980, 205, 0.0)
    sweat(ctx, 560 - 205 * 0.95, 1000 - 205 * 0.5, il, 1.5)
    sweat(ctx, 560 + 205 * 0.9, 1000 - 205 * 0.3, il + 40, 1.3)
    if il >= 36:
        twitch(ctx, 560 + 205 * 0.95, 1000 - 205 * 0.75, il, 1.6)
    # ice chips + a frosty tip on the moustache (foreshadowing)
    ctx.rectangle(-100, 1330, W + 200, 900); fl(ctx, hx('ff7a6a'), 6)
    ctx.rectangle(-100, 1300, W + 200, 40); fl(ctx, hx('fff6ea'), 5)
    turkey(ctx, 560, 1420, 1.9)
    sparks(ctx, 470, 1200, il, 14, 160, 4)
    ice_chips(ctx, 470, 1200, il // 3, 6, 1); ice_chips(ctx, 600, 1180, il // 3, 4, 2)
    ctx.restore()
    if il < 36:
        label(ctx, "\"It's... PERFECTLY...\"", 540, 560, 105, WHITE, -0.03, pop(il, 3, 7))
    else:
        label(ctx, "\"...COOKED!!\"", 540, 560, 150, ORANGE, 0.03, pop(il, 36, 39))


# ------------------------------------------------------------------ shot 5: it's frozen -> pizza -> loop
def frozen(ctx, f, il):
    # il 0..130: card 0-60 ; 8, 18 *tink!* ; frost 14-50 ; 60 Mom "I said THAW it." ; 84 "...THAW?!" ; 104 DING-DONG ; 112 "PIZZA!!"
    frost = eio(pop(il, 14, 50))
    ctx.save(); cam(ctx, 1110, 1270, 1.12, 0, shake_at(il, [84, 104], 8, 8), f)
    room(ctx, il)
    poke = 1 if (8 <= il < 12 or 18 <= il < 22) else 0
    mp = P(eye='glare', mouth='flat', lsh=50, lel=-120, rsh=40, rel=-110) if il < 104 else P(eye='happy', mouth='grin', lsh=150, lel=-20, rsh=160, rel=-10)
    if il < 104:
        kp = P(eye='normal', mouth='open', rsh=100 - 20 * poke, rel=-20, lsh=20, lel=-30)
    else:
        kp = P(eye='happy', mouth='grin', lsh=160, lel=-20, rsh=150, rel=-10)
    kdy = -20 * abs(math.sin(il * 0.5)) if il >= 104 else 0
    m = stand(ctx, MOM, MOMX, KMOM, mp, 1)
    k = stand(ctx, KID, KIDX, KKID, kp, -1, -70 + kdy)
    dp = P(eye='smug', mouth='grin', rsh=40, rel=-40, lsh=30, lel=-20) if il < 84 else P(eye='shock', mouth='scream', lsh=150, lel=-20, rsh=160, rel=-10, head=-6)
    d = stand(ctx, DAD, DADX, KDAD, dp, 1)
    if il >= 84:
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.7, il, 1.1)
    table(ctx, il)
    turkey(ctx, TX, TY, frost=frost)
    if il < 104:
        fork(ctx, k['front'][0], k['front'][1], math.pi + 0.5)
        if poke:
            sparkle(ctx, TX + 70, TY - 90, 30, ICE)
    ctx.restore()
    card(ctx, 'p2', il, 0, 60)
    if il < 60:
        label(ctx, "*tink! tink!*", 540, 1500, 105, CYAN, 0.03, pop(il, 8, 11))
    elif il < 84:
        label(ctx, "\"Honey... I said THAW it.\"", 540, 1500, 92, WHITE, -0.03, pop(il, 60, 64))
    elif il < 104:
        label(ctx, "\"...THAW?!\"", 540, 1500, 150, RED, 0.03, pop(il, 84, 87))
    else:
        label(ctx, "*DING-DONG!*", 540, 560, 110, GOLD, -0.04, pop(il, 104, 107))
        label(ctx, "\"PIZZA!!\"", 540, 1500, 150, WHITE, 0.03, pop(il, 110, 113))


def pizza_party(ctx, f, il):
    # il 0..100 (f 530..630): pizza on the table, Mom + kid munch ; 14 "...MORE for ME." ; 56 grabs the saw ; 70 SKREEE
    ctx.save(); cam(ctx, 1110, 1270, 1.12 + 0.04 * eio(pop(il, 50, 100)), 0, shake_at(il, [70], 6, 6), f)
    room(ctx, il)
    chew = (il // 4) % 2
    m = stand(ctx, MOM, MOMX, KMOM, P(eye='happy', mouth='open' if chew else 'grin', lsh=20, lel=-40, rsh=120, rel=-60), 1)
    k = stand(ctx, KID, KIDX, KKID, P(eye='happy', mouth='grin' if chew else 'open', lsh=120, lel=-60, rsh=20, rel=-30), -1, -70)
    if il < 56:
        dp = P(eye='glare', mouth='flat', rsh=40, rel=-40, lsh=30, lel=-20)
    else:
        sw = math.sin(il * 1.4) * (il >= 66)
        dp = P(eye='glare', mouth='scream' if il >= 66 else 'flat', rsh=132 + 6 * sw, rel=-10, lsh=118, lel=30, torso=10)
    d = stand(ctx, DAD, DADX, KDAD, dp, 1)
    table(ctx, il)
    pizza_box(ctx, MOMX + 40, TTOP + 30, il, 2)
    turkey(ctx, TX, TY, frost=1.0 - 0.0)
    slice_(ctx, m['back'][0], m['back'][1], -0.6, 0.9)
    slice_(ctx, k['back'][0], k['back'][1], math.pi + 0.6, 0.8)
    if il >= 56:
        hx_, hy = d['front']
        sw = math.sin(il * 1.4) * (il >= 66)
        saw(ctx, hx_ + 40 * sw, hy, 0.3)
        if il >= 66:
            sparks(ctx, TX - 20 + 40 * sw, TY - 120, il, 14, 130, 9)
            ice_chips(ctx, TX - 20, TY - 120, il // 2, 4, 3)
    if il >= 66:
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.7, il, 1.0)
    dog(ctx, 1490, GND + 8, 0.6, -1, il)
    slice_(ctx, 1490 - 120 * 0.6, GND + 8 - 170 * 0.6, math.pi, 0.6)
    ctx.restore()
    label(ctx, "*munch munch*", 540, 560, 84, ORANGE, 0.04, pop(il, 2, 5))
    if il < 66:
        label(ctx, "\"...MORE for ME.\"", 540, 1500, 120, WHITE, -0.03, pop(il, 14, 18))
    else:
        label(ctx, "*SKREEEE!*", 540, 1500, 120, ORANGE, 0.03, pop(il, 66, 69))


def s5(ctx, f):
    lf = f - 400
    if lf < 130:
        frozen(ctx, f, lf)
    elif lf < 230:
        pizza_party(ctx, f, lf - 130)
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
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.15, 0.05, 0.0, 0.2)
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
                              "-i", "out/turkey_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
