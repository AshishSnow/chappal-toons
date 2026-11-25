"""'Dad makes toast' - the smoke alarm. Original, general-audience comedy short, 22s.
Hook:   kitchen medium shot: Dad on a chair frantically fanning a dish towel at the beeping smoke alarm, smoke cloud,
        burnt toast smoking on the counter, kid covering his ears, dog howling. "IT'S JUST TOAST!!" + caption "DAD MAKES TOAST:".
Beat 1: "Toast? EASY." *click* lever -> *tick tick* toaster glows -> *KA-POW!* black toast rockets up, *POOF!* smoke ->
        sooty Dad, toast lands on his head *plop* "...a LITTLE crispy." -> *BEEP! BEEP! BEEP!*
Beat 2: Dutch-tilt fanning montage (Dad on the chair + towel, kid + tray, dog *AWOOO*) "FAN! FAN! FAN!" -> silence
        "...PHEW." -> the toast lets out one tiny smoke ring *puff* -> *BEEP!!* "...AGAIN?!"
Turn:   Dad ECU (the one close-up): "It's... JUST..." "...TOAST!!"
Twist:  PLOT TWIST: MOM MAKES TOAST. golden toast *DING!*, alarm silent, "...PERFECT." -> Dad steps in "Ooh, TOAST!"
        -> *BEEP BEEP!!* "I didn't even TOUCH it!!" -> alarm macro glares: "IT'S NOT THE TOAST. IT'S DAD."
        -> Mom hands him the towel "...fan, honey." -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes65 import dog
from scenes82 import window, picture
from scenes84 import eio
import scenes13
from scenes13 import card as _card13

RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
MOM = dict(doodle.MOM_G, shirt=hx('8a3cff'), pants=hx('2f4a8a'))
DAD = dict(doodle.DAD, shirt=hx('1f8bff'), pants=hx('3d5a3e'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff8a1f'), pants=hx('3d7bff'), shoes=hx('ff3b5c'))
N = 660
FLOOR, GND = 1560, 1590
CEIL = 640
ALX, ALY = 1010, 692                 # smoke alarm (ceiling)
TX0, TX1, TY = 1170, 1660, 1300      # counter
TOX = 1450                           # toaster centre x
CHX = 1000                           # chair
KDAD, KMOM, KKID = 1.08, 1.0, 0.82

CAPS = {'p1': [[("DAD ", OUT), ("MAKES TOAST:", ORANGE)]],
        'p2': [[("PLOT TWIST:", RED)], [("MOM ", OUT), ("MAKES TOAST.", PURPLE)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ set
def kitchen(ctx, lf, beep=False):
    wall = hx('e6f4ff')
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, wall); ctx.fill()
    for i in range(-20, 40):
        ctx.rectangle(i * 120, -3000, 46, 6000); setc(ctx, dark(wall, 0.965)); ctx.fill()
    rnd = random.Random(94)
    for k in range(70):
        sparkle(ctx, rnd.uniform(-300, 2400), rnd.uniform(560, 1100), 9, dark(wall, 0.9))
    # ceiling + crown moulding
    ctx.rectangle(-3000, -3000, 9000, CEIL + 3000); setc(ctx, hx('fffaf0')); ctx.fill()
    for i in range(-20, 40):   # wooden ceiling planks
        ctx.rectangle(i * 160, -3000, 150, CEIL + 3000); setc(ctx, hx('ffe6c4') if i % 2 else hx('ffdcb4')); ctx.fill()
        ctx.move_to(i * 160, CEIL); ctx.line_to(i * 160, CEIL - 700); ink(ctx, 2); ctx.stroke()
    rect_r(ctx, -3000, CEIL - 10, 9000, 26, 4); fl(ctx, hx('ffb86a'), 5)
    for lx in (560, 1500):     # pendant lamps
        ctx.move_to(lx, CEIL - 600); ctx.line_to(lx, CEIL - 120); ink(ctx, 4); ctx.stroke()
        poly(ctx, [(lx - 30, CEIL - 120), (lx + 30, CEIL - 120), (lx + 80, CEIL - 50), (lx - 80, CEIL - 50)]); fl(ctx, hx('ffc93c') if lx < 1000 else hx('7fe3ff'), 5)
        ellipse(ctx, lx, CEIL - 46, 22, 14); fl(ctx, hx('fff7c2'), 3)
    for k in range(5):         # paper bunting
        bx = 1150 + k * 90
        poly(ctx, [(bx, CEIL + 22), (bx + 70, CEIL + 22), (bx + 35, CEIL + 80)]); fl(ctx, (PINK, GOLD, CYAN, GREEN, ORANGE)[k], 3)
    # checker backsplash band
    for i in range(-10, 40):
        for j in range(2):
            ctx.rectangle(i * 60, 1150 + j * 60, 60, 60); setc(ctx, WHITE if (i + j) % 2 else hx('ffc2d6')); ctx.fill()
    ctx.move_to(-3000, 1150); ctx.line_to(6000, 1150); ctx.move_to(-3000, 1270); ctx.line_to(6000, 1270); ink(ctx, 4); ctx.stroke()
    ctx.rectangle(-3000, 1270, 9000, FLOOR - 1270); setc(ctx, hx('ffd9a8')); ctx.fill()
    ctx.save(); ctx.translate(-20, 190); window(ctx, lf); ctx.restore()
    picture(ctx, 1290, 860, 0.02 * math.sin(lf * 0.05))
    # little wall clock + hanging plant
    ellipse(ctx, 1560, 760, 56, 56); fl(ctx, WHITE, 6)
    ctx.move_to(1560, 760); ctx.line_to(1560 + 32 * math.sin(lf * 0.05), 760 - 32 * math.cos(lf * 0.05))
    ctx.move_to(1560, 760); ctx.line_to(1580, 744); ink(ctx, 5); ctx.stroke()
    ctx.move_to(260, CEIL); ctx.line_to(260, CEIL + 70); ink(ctx, 3); ctx.stroke()
    poly(ctx, [(220, CEIL + 70), (300, CEIL + 70), (290, CEIL + 130), (230, CEIL + 130)]); fl(ctx, hx('ff8a5c'), 4)
    for a in (-0.9, -0.3, 0.3, 0.9):
        ellipse(ctx, 260 + 50 * math.sin(a), CEIL + 150 + 10 * abs(a) * 3, 13, 36, a); fl(ctx, GREEN, 3)
    # doorway on the right
    rect_r(ctx, 1700, 720, 300, 860, 10); fl(ctx, hx('ffe8b0'), 7)
    rect_r(ctx, 1730, 750, 240, 830, 6); setc(ctx, hx('ffd082')); ctx.fill()
    # fridge on the left
    rect_r(ctx, 60, 820, 280, 760, 30); fl(ctx, hx('fff0f5'), 7)
    ctx.move_to(70, 1080); ctx.line_to(330, 1080); ink(ctx, 5); ctx.stroke()
    rect_r(ctx, 300, 920, 14, 110, 6); fl(ctx, hx('b8c4d6'), 3); rect_r(ctx, 300, 1110, 14, 140, 6); fl(ctx, hx('b8c4d6'), 3)
    for k, c in enumerate((GOLD, PINK, CYAN)):
        ellipse(ctx, 110 + 60 * k, 860, 14, 14); fl(ctx, c, 3)
    rect_r(ctx, 120, 1140, 130, 110, 4); fl(ctx, WHITE, 4)
    ellipse(ctx, 185, 1185, 26, 26); fl(ctx, GOLD, 3)
    # floor + rug + pet bed
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('c9874e')); ctx.fill()
    for i in range(-20, 40):
        ctx.move_to(i * 140, FLOOR); ctx.line_to(i * 140 - 60, FLOOR + 400); ink(ctx, 2); ctx.stroke()
    ellipse(ctx, 760, GND + 40, 300, 46); fl(ctx, hx('9fe0d0'), 5)
    ellipse(ctx, 760, GND + 40, 230, 30); setc(ctx, hx('c2f0e4')); ctx.fill()
    alarm(ctx, ALX, ALY, beep, lf)


def counter(ctx):
    ctx.rectangle(TX0 + 10, TY, TX1 - TX0 - 20, FLOOR - TY + 10); fl(ctx, hx('ffb2c8'), 6)
    for k in range(2):
        x0 = TX0 + 30 + k * (TX1 - TX0 - 60) / 2
        rect_r(ctx, x0 + 8, TY + 50, (TX1 - TX0 - 60) / 2 - 16, FLOOR - TY - 80, 10); ink(ctx, 4); ctx.stroke()
        ellipse(ctx, x0 + (TX1 - TX0 - 60) / 4, TY + 90, 10, 10); fl(ctx, GOLD, 3)
    rect_r(ctx, TX0 - 10, TY - 24, TX1 - TX0 + 20, 36, 8); fl(ctx, hx('f4f0ea'), 6)
    # butter dish + jam jar
    rect_r(ctx, TX0 + 20, TY - 70, 110, 46, 10); fl(ctx, hx('fff2a8'), 4)
    rect_r(ctx, TX0 + 10, TY - 40, 130, 18, 6); fl(ctx, WHITE, 3)
    rect_r(ctx, TX0 + 160, TY - 100, 60, 76, 12); fl(ctx, hx('d8304a'), 4)
    rect_r(ctx, TX0 + 154, TY - 112, 72, 20, 6); fl(ctx, hx('fff0c4'), 3)


def alarm(ctx, x, y, beep, lf, eyes=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    on = beep and (lf % 10) < 6
    if on:
        g = cairo.RadialGradient(0, 30, 10, 0, 30, 200)
        g.add_color_stop_rgba(0, 1, 0.2, 0.3, 0.45); g.add_color_stop_rgba(1, 1, 0.2, 0.3, 0)
        ctx.set_source(g); ctx.arc(0, 30, 200, 0, 2 * math.pi); ctx.fill()
    rect_r(ctx, -34, -60, 68, 30, 6); fl(ctx, hx('f4f0ea'), 4)
    ellipse(ctx, 0, 0, 78, 44); fl(ctx, WHITE, 5)
    ellipse(ctx, 0, -4, 54, 26); fl(ctx, hx('eef2f6'), 3)
    for k in range(-2, 3):
        if eyes <= 0:
            ctx.move_to(k * 16, -16); ctx.line_to(k * 16, 6); ink(ctx, 3); ctx.stroke()
    ellipse(ctx, 50, 18, 10, 8); fl(ctx, RED if on else hx('7a2a34'), 3)
    if eyes > 0:   # the alarm glaring (twist macro)
        for ex in (-26, 26):
            ellipse(ctx, ex, 14, 13, 13 * eyes); setc(ctx, INK); ctx.fill()
            ellipse(ctx, ex + 4, 10, 4, 4 * eyes); setc(ctx, WHITE); ctx.fill()
            ctx.move_to(ex - 18 * (1 if ex < 0 else -1), -2); ctx.line_to(ex + 14 * (1 if ex < 0 else -1), 6); ink(ctx, 5); ctx.stroke()
    if on:
        for k in (1, 2, 3):
            for sd in (-1, 1):
                ctx.new_path(); ctx.arc(sd * 70, 10, 26 * k, -0.6 if sd > 0 else math.pi - 0.6, 0.6 if sd > 0 else math.pi + 0.6)
                setc(ctx, RED); ctx.set_line_width(7); ctx.stroke()
    ctx.restore()


def toast(ctx, x, y, s=1.0, rot=0.0, burnt=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    crust = mix(hx('c8893a'), hx('1e1a1c'), burnt); inner = mix(hx('f2c66a'), hx('3a3134'), burnt)
    ctx.new_path(); ctx.move_to(-46, 50); ctx.line_to(-46, -20)
    ctx.curve_to(-70, -70, -20, -76, 0, -58); ctx.curve_to(20, -76, 70, -70, 46, -20); ctx.line_to(46, 50); ctx.close_path()
    fl(ctx, crust, 4)
    ctx.new_path(); ctx.move_to(-34, 40); ctx.line_to(-34, -16)
    ctx.curve_to(-52, -54, -14, -60, 0, -44); ctx.curve_to(14, -60, 52, -54, 34, -16); ctx.line_to(34, 40); ctx.close_path()
    setc(ctx, inner); ctx.fill()
    if burnt < 0.5:
        rect_r(ctx, -14, -10, 28, 22, 4); setc(ctx, hx('fff2a8')); ctx.fill()   # pat of butter
    ctx.restore()


def mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def toaster(ctx, x, y, lever=0.0, glow=0.0, s=1.0):
    """(x, y) = bottom centre on the counter"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, -70, 0, 16, 8); fl(ctx, INK, 2); ellipse(ctx, 70, 0, 16, 8); fl(ctx, INK, 2)
    rect_r(ctx, -110, -170, 220, 164, 50); fl(ctx, hx('7fd3ff'), 6)
    ctx.move_to(-80, -120); ctx.line_to(-80, -40); setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(10); ctx.stroke()
    for sx in (-40, 40):
        rect_r(ctx, sx - 30, -176, 60, 18, 8); fl(ctx, hx('39506a') if glow < 0.3 else mix(hx('39506a'), hx('ff5a2a'), glow), 3)
    rect_r(ctx, 106, -150 + 80 * lever, 30, 20, 6); fl(ctx, RED, 3)
    ellipse(ctx, 0, -60, 16, 16); fl(ctx, WHITE, 3)
    ctx.move_to(0, -60); ctx.line_to(10, -70); ink(ctx, 3); ctx.stroke()
    if glow > 0:
        g = cairo.RadialGradient(0, -176, 4, 0, -176, 120)
        g.add_color_stop_rgba(0, 1, 0.4, 0.1, 0.6 * glow); g.add_color_stop_rgba(1, 1, 0.4, 0.1, 0)
        ctx.set_source(g); ctx.arc(0, -176, 120, 0, 2 * math.pi); ctx.fill()
    ctx.restore()


def smoke(ctx, x, y, amt, lf, spread=1.0, seed=1, rise=1.0):
    if amt <= 0:
        return
    rnd = random.Random(seed)
    for i in range(int(14 * amt) + 2):
        ph = (lf * 0.012 * rise + rnd.random()) % 1
        px = x + rnd.uniform(-90, 90) * spread * (0.5 + ph) + 30 * math.sin(lf * 0.08 + i)
        py = y - ph * 330 * rise
        r = (40 + 70 * ph) * (0.6 + 0.4 * amt) * spread
        a = 0.75 * (1 - ph) * min(1, amt)
        ellipse(ctx, px, py, r, r * 0.85); setc(ctx, (0.42, 0.42, 0.48, a)); ctx.fill_preserve()
        setc(ctx, (0.25, 0.22, 0.25, a * 0.6)); ctx.set_line_width(3); ctx.stroke()


def cloud(ctx, x, y, w, amt, lf):
    """flat smoke cloud hugging the ceiling"""
    if amt <= 0:
        return
    for i in range(9):
        px = x + (i - 4) * w / 9 + 20 * math.sin(lf * 0.07 + i)
        r = (60 + 20 * math.sin(i * 1.7)) * amt
        ellipse(ctx, px, y + 14 * math.sin(i * 2.3 + lf * 0.1), r * 1.2, r * 0.8); setc(ctx, (0.45, 0.45, 0.5, 0.6 * amt)); ctx.fill_preserve()
        setc(ctx, (0.25, 0.22, 0.25, 0.4 * amt)); ctx.set_line_width(3); ctx.stroke()


def towel(ctx, hx_, hy_, lf, sp=1.0):
    a = -1.2 + 0.9 * math.sin(lf * 0.9 * sp)
    ctx.save(); ctx.translate(hx_, hy_); ctx.rotate(a)
    ctx.new_path(); ctx.move_to(0, -10); ctx.line_to(150, -26 + 16 * math.sin(lf * 1.3)); ctx.line_to(160, 40 + 16 * math.sin(lf * 1.3 + 1)); ctx.line_to(0, 26); ctx.close_path()
    fl(ctx, WHITE, 4)
    for k in (40, 90, 130):
        ctx.move_to(k, -12 - k * 0.08); ctx.line_to(k + 4, 28 + k * 0.08); setc(ctx, RED); ctx.set_line_width(9); ctx.stroke()
    ctx.restore()


def tray(ctx, x, y, lf):
    a = 0.5 * math.sin(lf * 1.1)
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ellipse(ctx, 0, -60, 70, 26); fl(ctx, hx('d8e0ea'), 4)
    ellipse(ctx, 0, -60, 52, 17); ink(ctx, 3); ctx.stroke()
    ctx.restore()


def chair(ctx, x):
    seat = GND - 150
    for dx in (-60, 60):
        rect_r(ctx, x + dx - 8, seat, 16, 150, 5); fl(ctx, hx('a0603a'), 4)
    rect_r(ctx, x - 80, seat - 18, 160, 26, 8); fl(ctx, hx('ff8a5c'), 5)
    rect_r(ctx, x + 56, seat - 160, 20, 150, 6); fl(ctx, hx('a0603a'), 4)


def soot(ctx, d):
    hx_, hy_, R = d['head'][0], d['head'][1], d['R']
    for dx, dy, r in ((-0.45, 0.3, 0.18), (0.5, 0.45, 0.14), (0.1, -0.5, 0.16), (-0.1, 0.65, 0.1)):
        ellipse(ctx, hx_ + dx * R, hy_ + dy * R, r * R, r * R * 0.7); setc(ctx, (0.2, 0.18, 0.2, 0.55)); ctx.fill()


def stand(ctx, ch, x, k, p, f_=1, dy=0):
    return draw(ctx, x, GND - 186 * k + dy, k, f_, ch, p)


def fan_dad(ctx, lf, eye='shock', mouth='scream', sp=1.0, sooty=True):
    sw = math.sin(lf * 0.9 * sp)
    chair(ctx, CHX)
    d = stand(ctx, DAD, CHX - 10, KDAD, P(eye=eye, mouth=mouth, lsh=160 + 12 * sw, lel=-20, rsh=150, rel=-30, head=-10), 1, -150)
    towel(ctx, d['front'][0], d['front'][1], lf, sp)
    if sooty:
        soot(ctx, d)
    return d


def kid_ears(ctx, x, lf, fan=False):
    if fan:
        k = stand(ctx, KID, x, KKID, P(eye='shock', mouth='open', lsh=160, lel=-10, rsh=140, rel=-30), 1)
        tray(ctx, k['front'][0], k['front'][1], lf)
    else:
        k = stand(ctx, KID, x, KKID, P(eye='glare', mouth='scream', lsh=150, lel=-150, rsh=150, rel=-150), 1)
    return k


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = 1.12 + 0.04 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, 1000, 1060, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    kitchen(ctx, lf, True)
    cloud(ctx, ALX, CEIL + 120, 1100, 1.0, lf)
    counter(ctx)
    toaster(ctx, TOX, TY - 20)
    toast(ctx, TOX - 160, TY - 50, 0.8, 0.3)
    smoke(ctx, TOX - 160, TY - 80, 0.8, lf, 0.7, 3)
    dog(ctx, 430, GND + 5, 0.75, 1, lf)
    kid_ears(ctx, 700, lf)
    d = fan_dad(ctx, lf, sp=1.6)
    sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.5, lf, 1.0)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"IT'S JUST TOAST!!\"", 540, 1450, 115, WHITE, -0.04, t)
    label(ctx, "*BEEP! BEEP! BEEP!*", 540, 690, 84, RED, 0.04, 1 if lf == f else pop(lf, 2, 5))


# ------------------------------------------------------------------ shot 2: the toaster
def make_toast(ctx, f, il):
    # il 0..140: 0-22 "Toast? EASY." ; 20 *click* ; 24-60 tick + glow ; 62 *KA-POW!* ; 62-90 smoke ; 85 plop on head ;
    #            92 "...a LITTLE crispy." ; 112 *BEEP!*
    lever = eio(pop(il, 18, 22)) * (1 - eio(pop(il, 62, 64)))
    glow = pop(il, 24, 60) * (1 - pop(il, 62, 70))
    beep = il >= 112
    ctx.save(); cam(ctx, 1290 if il < 105 else 1200, 1130 if il < 105 else 1010, 1.45 if il < 105 else 1.25, 0,
                    shake_at(il, [62, 112], 10, 8), f)
    kitchen(ctx, il, beep)
    counter(ctx)
    toaster(ctx, TOX, TY - 20, lever, glow)
    smoke(ctx, TOX, TY - 200, glow * 0.6, il, 0.4, 5)
    blown = il >= 62
    if not blown:
        d = stand(ctx, DAD, 1220, KDAD, P(eye='smug' if il < 22 else 'happy', mouth='grin', lsh=40 if il < 18 else 70,
                                          lel=-100 if il < 18 else -40, rsh=30, rel=60, head=-2))
        if il < 18:
            for j in (-1, 1):
                toast(ctx, TOX + 40 * j, TY - 230 + 70 * eio(pop(il, 10, 18)), 0.8, 0, 0)
        if il < 22:
            sparkle(ctx, d['head'][0] + d['R'] * 1.6, d['head'][1] - d['R'] * 1.2, 22, GOLD)
    else:
        t = il - 62
        d = stand(ctx, DAD, 1220, KDAD, P(eye='shock' if t < 30 else ('glare' if not beep else 'shock'), mouth='scream' if t < 8 else 'flat',
                                          lsh=20, lel=10, rsh=-20, rel=-10, head=-6 if beep else 0))
        soot(ctx, d)
        hy_ = d['head'][1] - d['R'] * 1.05
        for j in (-1, 1):   # toast flies up, comes down
            yy = TY - 200 - 60 * t + 2.2 * t * t
            xx = TOX + 40 * j + lerp(0, d['head'][0] - TOX - 40 * j + 30 * j, clamp(t / 23))
            if yy < hy_ or t < 12:
                toast(ctx, xx, yy, 0.8, t * 0.4 * j, 1.0)
            else:
                toast(ctx, d['head'][0] + 30 * j, hy_ - 20 + 10 * (j > 0), 0.7, 0.3 * j, 1.0)
        smoke(ctx, TOX - 100, TY - 160, 1.6 * (1 - pop(t, 10, 40)) + 0.5, il, 1.4, 7)
        smoke(ctx, d['head'][0], d['head'][1] - d['R'] * 1.5, 0.5, il, 0.4, 8, 0.6)
        if beep:
            twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.7, il, 1.0)
    ctx.restore()
    if il < 22:
        label2(ctx, "\"Toast?", "EASY.\"", WHITE, pop(il, 2, 6), 120, col2=GOLD, y=1440)
    elif il < 62:
        label(ctx, "*click*", 540, 640, 90, CYAN, -0.05, pop(il, 20, 23))
        label(ctx, "*tick... tick... tick...*", 540, 1460, 84, ORANGE, 0.03, pop(il, 28, 31))
    elif il < 92:
        label(ctx, "*KA-POW!!*", 540, 620, 150, RED, -0.06, pop(il, 62, 65))
        if il >= 84:
            label(ctx, "*plop*", 540, 1460, 90, ORANGE, 0.03, pop(il, 84, 87))
    elif il < 112:
        label(ctx, "\"...a LITTLE crispy.\"", 540, 1450, 115, WHITE, -0.03, pop(il, 92, 95))
    else:
        label(ctx, "*BEEP! BEEP! BEEP!*", 540, 1450, 100, RED, 0.04, pop(il, 112, 115))


def s2(ctx, f):
    make_toast(ctx, f, f - 60)


# ------------------------------------------------------------------ shot 3: fanning montage
def fanning(ctx, f, il):
    # il 0..130: 0-62 FAN! montage (dutch) ; 62 silence ; 72 "...PHEW." ; 94 *puff* ring ; 100 *BEEP!!* ; 104 "...AGAIN?!"
    beep = il < 62 or il >= 100
    rot = -5 * math.sin(il * 0.25) if il < 62 else 0
    ctx.save(); cam(ctx, 1000, 1150, 1.0 + 0.05 * eio(il / 130), rot, shake_at(il, [0, 100], 8, 7), f)
    kitchen(ctx, il, beep)
    cloud(ctx, ALX, CEIL + 120, 1300, 1.0 - 0.7 * pop(il, 20, 62), il)
    counter(ctx)
    toaster(ctx, TOX, TY - 20)
    toast(ctx, TOX - 170, TY - 50, 0.8, 0.3)
    if il < 62:
        d = fan_dad(ctx, il, sp=2.2)
        k = kid_ears(ctx, 700, il * 2, True)
        dog(ctx, 430, GND + 5, 0.75, 1, il)
    else:
        calm = il < 100
        d = fan_dad(ctx, il, 'happy' if calm else 'shock', 'smile' if calm else 'scream', 0.15 if calm else 2.2)
        k = stand(ctx, KID, 700, KKID, P(eye='happy' if calm else 'glare', mouth='grin' if calm else 'scream',
                                         lsh=150 if not calm else 20, lel=-150 if not calm else 10, rsh=150 if not calm else -20, rel=-150 if not calm else -10), 1)
        dog(ctx, 430, GND + 5, 0.75, 1, il)
        if il >= 94:   # one tiny smoke ring rises from the toast
            t = il - 94
            ctx.new_path(); ctx.arc(TOX - 170, TY - 110 - 30 * t, 22 + 2 * t, 0, 2 * math.pi)
            setc(ctx, (0.4, 0.4, 0.45, max(0, 0.9 - t * 0.03))); ctx.set_line_width(12); ctx.stroke()
        if il >= 100:
            twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.7, il, 1.1)
    ctx.restore()
    if il < 62:
        j = il // 15
        label(ctx, "*AWOOOO!*" if j == 2 else "*FWAP! FWAP!*", 540, (600, 660, 620, 680, 640)[j % 5], 100, PURPLE if j == 2 else ORANGE,
              (-0.08, 0.06, -0.04, 0.08, -0.05)[j % 5], pop(il, 15 * j, 15 * j + 3))
        label(ctx, "\"FAN! FAN! FAN!\"", 540, 1450, 115, WHITE, 0.03, pop(il, 3, 6))
    elif il < 94:
        label(ctx, "*...silence*", 540, 640, 90, GREEN, 0.04, pop(il, 62, 65))
        if il >= 72:
            label(ctx, "\"...PHEW.\"", 540, 1450, 130, WHITE, -0.03, pop(il, 72, 75))
    elif il < 100:
        label(ctx, "*puff*", 540, 1450, 100, WHITE, 0.03, pop(il, 94, 97))
    else:
        label(ctx, "*BEEP!!*", 540, 640, 130, RED, -0.05, pop(il, 100, 103))
        label(ctx, "\"...AGAIN?!\"", 540, 1450, 130, WHITE, 0.03, pop(il, 104, 107))


def s3(ctx, f):
    fanning(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: Dad ECU (the one close-up)
def s4(ctx, f):
    il = f - 330
    ctx.save(); cam(ctx, 1000, 900, 1.5, 0, 0, f)
    kitchen(ctx, il, True)
    cloud(ctx, ALX, CEIL + 160, 1300, 1.0, il)
    ctx.restore()
    ctx.rectangle(0, 0, W, H); setc(ctx, (1, 0.9, 0.9, 0.3)); ctx.fill()
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.07 * eio(il / 70), 0, shake_at(il, [0, 34], 6, 8), f)
    face(ctx, DAD, P(eye='glare', mouth='flat' if il < 34 else 'scream'), 540, 940, 200, 0.0)
    for dx, dy, r in ((-0.45, 0.3, 0.18), (0.5, 0.45, 0.14), (0.1, -0.5, 0.16)):
        ellipse(ctx, 540 + dx * 200, 940 + dy * 200, r * 200, r * 140); setc(ctx, (0.2, 0.18, 0.2, 0.5)); ctx.fill()
    toast(ctx, 540, 940 - 230, 1.3, 0.15, 1.0)
    smoke(ctx, 540, 940 - 300, 0.7, il, 0.6, 9, 0.8)
    twitch(ctx, 540 + 200 * 0.95, 940 - 200 * 0.7, il, 1.6)
    ctx.restore()
    if il < 34:
        label(ctx, "\"It's... JUST...\"", 540, 1450, 115, WHITE, -0.03, pop(il, 3, 7))
    else:
        label(ctx, "\"...TOAST!!\"", 540, 1450, 170, RED, 0.03, pop(il, 34, 37))


# ------------------------------------------------------------------ shot 5: Mom's toast -> the alarm knows Dad -> loop
def mom_toast(ctx, f, il):
    # il 0..130: card ; 0-30 Mom presses ; 38 *DING!* golden toast ; 50 "...PERFECT." ; 72 Dad steps in "Ooh, TOAST!" ;
    #            92 *BEEP BEEP!!* ; 104 "I didn't even TOUCH it!!"
    beep = il >= 92
    lever = eio(pop(il, 8, 12)) * (1 - eio(pop(il, 38, 40)))
    ctx.save(); cam(ctx, 1010, 1090, 1.0, 0, shake_at(il, [92], 9, 8), f)
    kitchen(ctx, il, beep)
    counter(ctx)
    toaster(ctx, TOX, TY - 20, lever, 0.3 * pop(il, 12, 36) * (1 - pop(il, 38, 42)))
    m = stand(ctx, MOM, 1250, KMOM, P(eye='smug' if il < 92 else 'glare', mouth='smile' if il < 92 else 'flat', lsh=60, lel=-50, rsh=30, rel=60))
    if il >= 38:
        t = il - 38
        for j in (-1, 1):
            yy = TY - 200 - 40 * t + 3 * t * t
            toast(ctx, TOX + 40 * j, min(yy, TY - 230) if t > 4 else yy, 0.8, 0, 0.0)
        if il < 92:
            for j in range(5):
                a = j * 1.25 + il * 0.06
                sparkle(ctx, TOX + 150 * math.cos(a), TY - 260 + 80 * math.sin(a), 16 + 6 * math.sin(il * 0.5 + j), GOLD)
    wx = lerp(720, 960, eio(pop(il, 66, 88)))
    bob = 10 * abs(math.sin(il * 0.5)) * (66 <= il < 88)
    if il < 92:
        d = stand(ctx, DAD, wx, KDAD, P(eye='shock' if il < 38 else 'happy', mouth='flat' if il < 38 else 'grin',
                                        lsh=150, lel=-150, rsh=150, rel=-150) if il < 38 else
                  P(eye='happy', mouth='grin', lsh=60, lel=-40, rsh=40, rel=40), 1, -bob)
    else:
        d = stand(ctx, DAD, wx, KDAD, P(eye='shock', mouth='scream', lsh=160, lel=-10, rsh=170, rel=-10, head=-6), 1)
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.7, il, 1.1)
    kid_ears(ctx, 560, il) if il >= 92 else stand(ctx, KID, 560, KKID, P(eye='happy', mouth='grin'), 1)
    ctx.restore()
    card(ctx, 'p2', il, 0, 66)
    if il < 38:
        label(ctx, "*click*", 540, 1460, 90, CYAN, -0.05, pop(il, 10, 13))
    elif il < 66:
        label(ctx, "*DING!*", 540, 1350, 110, GOLD, 0.05, pop(il, 38, 41))
        label(ctx, "\"...PERFECT.\"", 540, 1480, 110, WHITE, -0.03, pop(il, 48, 51))
    elif il < 92:
        label(ctx, "\"Ooh, TOAST!\"", 540, 1450, 120, WHITE, 0.03, pop(il, 70, 73))
    else:
        label(ctx, "*BEEP! BEEP!!*", 540, 620, 110, RED, -0.05, pop(il, 92, 95))
        label2(ctx, "\"I didn't even", "TOUCH it!!\"", WHITE, pop(il, 102, 106), 110, col2=RED, y=1440)


def alarm_macro(ctx, f, il):
    # il 0..55: the alarm glares at Dad
    ctx.save(); cam(ctx, ALX, ALY + 60, 3.2 + 0.25 * eio(il / 55), 0, shake_at(il, [0, 26], 7, 6), f)
    kitchen(ctx, il, False)
    alarm(ctx, ALX, ALY, il % 20 < 10, il, eyes=eio(pop(il, 4, 12)))
    ctx.restore()
    label2(ctx, "IT'S NOT THE TOAST.", "IT'S DAD.", WHITE, pop(il, 8, 12), 100, col2=RED, y=1420)


def hand_towel(ctx, f, il):
    # il 0..50: Mom hands Dad the towel "...fan, honey."
    ctx.save(); cam(ctx, 1000, 1110, 1.15, 0, 0, f)
    kitchen(ctx, il, True)
    counter(ctx)
    toaster(ctx, TOX, TY - 20)
    toast(ctx, TOX - 170, TY - 50, 0.8, 0.0, 0.0)
    chair(ctx, CHX)
    d = stand(ctx, DAD, 860, KDAD, P(eye='glare', mouth='flat', lsh=20, lel=10, rsh=60, rel=-20), 1)
    m = stand(ctx, MOM, 1180, KMOM, P(eye='smug', mouth='smile', lsh=80, lel=-20, rsh=20, rel=60), -1)
    hx_ = lerp(m['front'][0], d['front'][0] + 40, eio(pop(il, 4, 18))); hy_ = lerp(m['front'][1], d['front'][1], eio(pop(il, 4, 18)))
    towel(ctx, hx_, hy_, 0, 0)
    twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.7, il, 1.0)
    stand(ctx, KID, 600, KKID, P(eye='glare', mouth='scream', lsh=150, lel=-150, rsh=150, rel=-150), 1)
    ctx.restore()
    label(ctx, "\"...fan, honey.\"", 540, 1450, 120, WHITE, -0.03, pop(il, 8, 11))


def s5(ctx, f):
    lf = f - 400
    if lf < 130:
        mom_toast(ctx, f, lf)
    elif lf < 180:
        alarm_macro(ctx, f, lf - 130)
    elif lf < 230:
        hand_towel(ctx, f, lf - 180)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (200, s3), (330, s4), (400, s5)]
CUTS = (60, 200, 330, 400, 530, 580, 630)


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
                              "-i", "out/dad_makes_toast_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
