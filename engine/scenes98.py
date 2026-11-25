"""'The floor is LAVA!'. Original, general-audience comedy short, 22s.
Hook:   living-room medium shot, the floor glows as bubbling lava: kid on the sofa pointing + screaming
        "THE FLOOR IS LAVA!!", Dad frozen on one leg on the coffee table with his coffee mug + caption "THE FLOOR IS LAVA:".
Beat 1: Dad deadpan "Son... I'm a GROWN-UP." -> lava *BLOOP!* by his foot -> he leaps onto the armchair *BOING!*
        (mug flies) -> crouched "...it's HOT!!"
Beat 2: Dutch-tilt: Dad hops cushion stepping-stones *BOING x3* -> last cushion sinks *glub* "...SINKING!!" -> leaps and
        grabs the curtain rod *CREAK* -> low angle, swinging, kid "GO DAD GO!!"
Turn:   the one close-up: sweaty Dad hanging "NEVER... TOUCH..." "...THE LAVA!!"
Twist:  Mom in the doorway "Dinner's READY!" -> both "MOM!! THE LAVA!!" -> PLOT TWIST: MOM PLAYS TOO. shades on *click*,
        robot vacuum rolls in *beep boop*, she rides it across the lava *WHIRRR* "Last one to the table..." "...does the DISHES."
        -> Dad + kid "...DISHES?!" -> *CRACK!* rod snaps -> *SPLOOSH!* Dad sits in the lava "...I'll get the sponge."
        -> kid "THE FLOOR IS LAVA!!" hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, _SCR
from scenes58 import sweat, twitch
from scenes65 import dog
from scenes84 import eio
import scenes13
from scenes13 import card as _card13

RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
LAVA = hx('ff6a1a'); LAVA2 = hx('ffb030'); LAVA3 = hx('e8321e')
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('3fd6a0'), pants=hx('3d7bff'), shoes=hx('ff4d5e'))
MOM = dict(doodle.MOM_G, shirt=hx('ff7a59'))
DAD = dict(doodle.DAD, shirt=hx('ffd23f'), pants=hx('3a4a8a'))
N = 660
FLOOR, GND = 1560, 1590
KIDX, TABX, CHX, ROD, DOORX = 790, 1080, 1370, 870, 1080
KKID, KDAD, KMOM = 0.92, 1.0, 0.98
CX, CY, CZ = 1090, 1170, 1.12
SEAT = 1400      # sofa seat top
TABTOP = 1455    # coffee table top
CHSEAT = 1415    # armchair seat top

CAPS = {'p1': [[("THE FLOOR ", OUT), ("IS ", OUT), ("LAVA:", ORANGE)]],
        'p2': [[("PLOT TWIST:", RED)], [("MOM ", PURPLE), ("PLAYS TOO.", OUT)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ set: living room
def room(ctx, lf):
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, hx('fff0d6')); ctx.fill()
    for i in range(-10, 30):   # soft stripe wallpaper with little hearts
        ctx.rectangle(i * 90, -3000, 40, 9000); setc(ctx, hx('ffe2c2')); ctx.fill()
    rnd = random.Random(98)
    for k in range(26):
        sparkle(ctx, rnd.uniform(400, 1800), rnd.uniform(450, 1250), 8, hx('ffc0a0'))
    # doorway (centre back) to the hallway
    dx0, dy0, dw, dh = DOORX - 150, 990, 300, 570
    rect_r(ctx, dx0 - 24, dy0 - 24, dw + 48, dh + 30, 10); fl(ctx, WHITE, 6)
    ctx.rectangle(dx0, dy0, dw, dh); setc(ctx, hx('ffd8a8')); ctx.fill()
    rect_r(ctx, dx0 + 100, dy0 + 120, 100, 120, 8); fl(ctx, hx('ffeccc'), 3)
    ctx.rectangle(dx0, FLOOR - 20, dw, 20); setc(ctx, hx('c98a52')); ctx.fill()
    # window (right) with curtain rod
    x, y, w, h = 1250, 905, 290, 300
    rect_r(ctx, x, y, w, h, 16); fl(ctx, hx('9fe0ff'), 8)
    ctx.save(); rect_r(ctx, x, y, w, h, 16); ctx.clip()
    ellipse(ctx, x + 70, y + 80, 40, 40); fl(ctx, hx('ffd84a'), 4)
    for cx_, cy_ in ((x + 190, y + 90), (x + 120, y + 200)):
        for dx, r in ((-24, 22), (0, 30), (26, 22)):
            ellipse(ctx, cx_ + dx, cy_, r, r * 0.75); setc(ctx, WHITE); ctx.fill()
    ellipse(ctx, x + 150, y + h + 30, 220, 90); fl(ctx, hx('6fd37a'), 4)
    ctx.restore()
    ctx.move_to(x + w / 2, y); ctx.line_to(x + w / 2, y + h); ctx.move_to(x, y + h * 0.5); ctx.line_to(x + w, y + h * 0.5); ink(ctx, 6); ctx.stroke()
    for sd in (0, 1):
        cx_ = x - 20 if sd == 0 else x + w + 20
        ctx.new_path(); ctx.move_to(cx_ - 36, ROD + 10); ctx.line_to(cx_ + 36, ROD + 10)
        ctx.curve_to(cx_ + 20, y + 120, cx_ + 42, y + 260, cx_ + 28, y + h + 30); ctx.line_to(cx_ - 28, y + h + 30)
        ctx.curve_to(cx_ - 42, y + 260, cx_ - 20, y + 120, cx_ - 36, ROD + 10); ctx.close_path(); fl(ctx, hx('8a7bff'), 5)
        for j in range(4):
            sparkle(ctx, cx_ - 6 + (j % 2) * 12, y + 20 + j * 90, 7, YEL)
    # picture frames (left wall)
    rect_r(ctx, 640, 930, 170, 130, 8); fl(ctx, hx('ffb36a'), 6)
    rect_r(ctx, 660, 950, 130, 90, 4); fl(ctx, hx('bfe9ff'), 3)
    poly(ctx, [(670, 1030), (715, 975), (760, 1030)]); fl(ctx, hx('6fd37a'), 3)
    ellipse(ctx, 760, 975, 14, 14); fl(ctx, GOLD, 2)
    rect_r(ctx, 830, 880, 80, 100, 8); fl(ctx, hx('ff9ac0'), 5)
    ellipse(ctx, 870, 930, 22, 26); fl(ctx, hx('fff0f5'), 3)
    # floor lamp (far left) + plant (far right)
    rect_r(ctx, 560, 1100, 12, 460, 4); fl(ctx, hx('8a5a3a'), 3)
    poly(ctx, [(510, 1100), (622, 1100), (600, 1010), (532, 1010)]); fl(ctx, hx('ffd36a'), 5)
    rect_r(ctx, 1560, 1440, 90, 120, 12); fl(ctx, hx('ff8a5c'), 5)
    for a in (-0.8, -0.35, 0.1, 0.55, 0.95):
        ellipse(ctx, 1605 + 60 * math.sin(a), 1380 - 50 * math.cos(a), 18, 46, a); fl(ctx, GREEN, 3)
    # skirting
    rect_r(ctx, -3000, FLOOR - 24, 9000, 24, 4); fl(ctx, WHITE, 4)


def lava(ctx, lf, y0=FLOOR):
    """the bubbling-lava floor (it's imaginary... but very hot)"""
    ctx.new_path(); ctx.move_to(-3000, y0)
    for i in range(0, 121):
        xx = -3000 + i * 75
        ctx.line_to(xx, y0 + 7 * math.sin(xx * 0.02 + lf * 0.25))
    ctx.line_to(6000, 4000); ctx.line_to(-3000, 4000); ctx.close_path()
    g = cairo.LinearGradient(0, y0, 0, y0 + 500)
    g.add_color_stop_rgb(0, *LAVA2[:3]); g.add_color_stop_rgb(0.35, *LAVA[:3]); g.add_color_stop_rgb(1, *LAVA3[:3])
    ctx.save(); ctx.set_source(g); ctx.fill_preserve(); ctx.restore(); ink(ctx, 5); ctx.stroke()
    rnd = random.Random(7)
    for k in range(22):   # crust swirls
        x = rnd.uniform(300, 1900); y = y0 + rnd.uniform(40, 460)
        x += 18 * math.sin(lf * 0.05 + k)
        ctx.new_path(); ctx.move_to(x - 50, y); ctx.curve_to(x - 20, y - 16, x + 20, y + 16, x + 50, y)
        setc(ctx, (1, 0.9, 0.5, 0.7)); ctx.set_line_width(7); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    for k in range(9):    # bubbles that grow and pop
        ph = (lf * 0.035 + k * 0.37) % 1
        x = 420 + (k * 173) % 1350; y = y0 + 50 + (k * 97) % 380
        r = 8 + 26 * ph
        if ph < 0.9:
            ellipse(ctx, x, y, r, r * 0.8); fl(ctx, LAVA2, 3)
            ellipse(ctx, x - r * 0.3, y - r * 0.3, r * 0.25, r * 0.2); setc(ctx, (1, 1, 0.85, 0.9)); ctx.fill()
        else:
            for a in range(5):
                aa = a * math.pi / 4 + math.pi
                ctx.move_to(x + 20 * math.cos(aa), y + 16 * math.sin(aa)); ctx.line_to(x + 40 * math.cos(aa), y + 30 * math.sin(aa)); ink(ctx, 4); ctx.stroke()
    # heat glow up the wall
    g2 = cairo.LinearGradient(0, y0 - 260, 0, y0)
    g2.add_color_stop_rgba(0, 1, 0.5, 0.1, 0); g2.add_color_stop_rgba(1, 1, 0.45, 0.1, 0.28)
    ctx.rectangle(-3000, y0 - 260, 9000, 260); ctx.set_source(g2); ctx.fill()


def lava_front(ctx, lf, x0, x1, y):
    """a strip of lava in front of something sitting in it"""
    ctx.new_path(); ctx.move_to(x0, y)
    for i in range(0, 21):
        xx = x0 + (x1 - x0) * i / 20
        ctx.line_to(xx, y + 10 * math.sin(xx * 0.05 + lf * 0.4))
    ctx.line_to(x1, y + 300); ctx.line_to(x0, y + 300); ctx.close_path()
    g = cairo.LinearGradient(0, y - 40, 0, y + 400)
    g.add_color_stop_rgb(0, *LAVA2[:3]); g.add_color_stop_rgb(0.35, *LAVA[:3]); g.add_color_stop_rgb(1, *LAVA3[:3])
    ctx.save(); ctx.set_source(g); ctx.fill(); ctx.restore()
    ctx.new_path(); ctx.move_to(x0, y)
    for i in range(0, 21):
        xx = x0 + (x1 - x0) * i / 20
        ctx.line_to(xx, y + 10 * math.sin(xx * 0.05 + lf * 0.4))
    ink(ctx, 5); ctx.stroke()


def sofa(ctx):
    rect_r(ctx, 620, 1230, 360, 190, 40); fl(ctx, hx('5a7bff'), 6)          # back
    rect_r(ctx, 640, SEAT, 320, 100, 24); fl(ctx, hx('7a95ff'), 5)          # seat
    rect_r(ctx, 600, 1320, 70, 200, 26); fl(ctx, hx('4a68e8'), 5)          # arms
    rect_r(ctx, 930, 1320, 70, 200, 26); fl(ctx, hx('4a68e8'), 5)
    for xx in (630, 960):
        rect_r(ctx, xx, 1510, 20, 50, 6); fl(ctx, hx('8a5a3a'), 3)
    rect_r(ctx, 880, 1290, 90, 80, 22); fl(ctx, hx('ffd36a'), 4)            # throw pillow
    for j in range(3):
        sparkle(ctx, 900 + j * 25, 1320 + (j % 2) * 20, 7, WHITE)


def table(ctx, mug=True):
    rect_r(ctx, TABX - 120, TABTOP, 240, 32, 10); fl(ctx, hx('c98a52'), 5)
    for xx in (TABX - 100, TABX + 84):
        rect_r(ctx, xx, TABTOP + 30, 16, FLOOR - TABTOP - 10, 5); fl(ctx, hx('a46a3a'), 4)
    rect_r(ctx, TABX + 50, TABTOP - 22, 50, 22, 4); fl(ctx, hx('ff5fa8'), 3)   # books
    rect_r(ctx, TABX + 46, TABTOP - 40, 58, 18, 4); fl(ctx, hx('3fd6a0'), 3)


def armchair(ctx):
    rect_r(ctx, CHX - 130, 1250, 260, 190, 40); fl(ctx, hx('ff7a8a'), 6)
    rect_r(ctx, CHX - 120, CHSEAT, 240, 90, 22); fl(ctx, hx('ff98a5'), 5)
    rect_r(ctx, CHX - 160, 1340, 60, 170, 24); fl(ctx, hx('f0606f'), 5)
    rect_r(ctx, CHX + 100, 1340, 60, 170, 24); fl(ctx, hx('f0606f'), 5)
    for xx in (CHX - 140, CHX + 120):
        rect_r(ctx, xx, 1505, 18, 55, 6); fl(ctx, hx('8a5a3a'), 3)


def rod(ctx, broken=0.0):
    if broken <= 0:
        rect_r(ctx, 1150, ROD - 10, 490, 20, 10); fl(ctx, hx('b97a4a'), 4)
        for xx in (1150, 1640):
            ellipse(ctx, xx, ROD, 18, 18); fl(ctx, GOLD, 3)
    else:
        ellipse(ctx, 1150, ROD, 18, 18); fl(ctx, GOLD, 3); ellipse(ctx, 1640, ROD, 18, 18); fl(ctx, GOLD, 3)
        for sd, x0 in ((-1, 1150), (1, 1640)):
            ctx.save(); ctx.translate(x0, ROD); ctx.rotate(-sd * 1.1 * eio(broken))
            rect_r(ctx, 0 if sd < 0 else -245, -10, 245, 20, 10); fl(ctx, hx('b97a4a'), 4)
            ctx.restore()


def mug(ctx, x, y, a=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -22, -30, 44, 50, 8); fl(ctx, WHITE, 4)
    ctx.new_path(); ctx.arc(24, -6, 14, -1.4, 1.4); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 0, -6, 10, 10); setc(ctx, hx('ff8ab0')); ctx.fill()
    ctx.restore()


def cushion(ctx, x, y, col, sink=0.0):
    ctx.save(); ctx.translate(x, y + 40 * sink)
    rect_r(ctx, -70, -26, 140, 40, 16); fl(ctx, col, 4)
    ellipse(ctx, 0, -6, 8, 6); fl(ctx, dark(col, 0.8), 2)
    ctx.restore()


def robovac(ctx, x, y, lf, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 110, 30); fl(ctx, hx('5a5f7a'), 5)
    ellipse(ctx, 0, -10, 104, 24); fl(ctx, hx('d8dcef'), 4)
    ellipse(ctx, 0, -14, 30, 9); fl(ctx, hx('8a90b0'), 3)
    if int(lf / 4) % 2 == 0:
        ellipse(ctx, 60, -12, 9, 6); setc(ctx, hx('3dff8a')); ctx.fill()
    for sd in (-1, 1):   # little brush
        ctx.save(); ctx.translate(sd * 92, 18); ctx.rotate(lf * 0.6 * sd)
        for a in range(3):
            ctx.move_to(0, 0); ctx.line_to(24 * math.cos(a * 2.1), 10 * math.sin(a * 2.1)); ink(ctx, 3); ctx.stroke()
        ctx.restore()
    ctx.restore()


def shades(ctx, d):
    for e in ('eyeL', 'eyeR'):
        ex, ey = d[e]
        rect_r(ctx, ex - d['R'] * 0.26, ey - d['R'] * 0.16, d['R'] * 0.52, d['R'] * 0.34, d['R'] * 0.1); fl(ctx, hx('1d1820'), 3)
        ctx.move_to(ex - d['R'] * 0.14, ey - d['R'] * 0.06); ctx.line_to(ex - d['R'] * 0.02, ey - d['R'] * 0.1)
        setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(4); ctx.stroke()
    (ax, ay), (bx, by) = d['eyeL'], d['eyeR']
    ctx.move_to(ax + d['R'] * 0.26, ay); ctx.line_to(bx - d['R'] * 0.26, by); ink(ctx, 6); ctx.stroke()


def sweat_drops(ctx, d, lf):
    sweat(ctx, d['head'][0] - d['R'] * 1.0, d['head'][1] - d['R'] * 0.4, lf, 0.6)
    sweat(ctx, d['head'][0] + d['R'] * 1.05, d['head'][1] - d['R'] * 0.2, lf + 20, 0.5)


def stand(ctx, ch, x, k, p, f_=1, feet=GND):
    return draw(ctx, x, feet - 186 * k, k, f_, ch, p)


def hang(ctx, x, rod_y, p, f_=1, swing=0.0):
    """Dad hanging by both (stretchy cartoon) arms from a bar at rod_y"""
    p = dict(p, lsh=150, lel=-10, rsh=150, rel=-10)
    _SCR.identity_matrix()
    b = draw(_SCR, 0, 0, KDAD, f_, DAD, p)
    R = b['R']; hx0, hy0 = b['head']
    ctx.save(); ctx.translate(x, rod_y); ctx.rotate(swing)
    dy = R * 1.55 - hy0; cx = hx0
    S = S_ = 1.35 * KDAD
    for sd in (-1, 1):   # arms reaching up to the rod (behind the body)
        ctx.new_path(); ctx.move_to(cx + sd * R * 0.55, R * 2.6); ctx.curve_to(cx + sd * R * 1.15, R * 2.0, cx + sd * R * 1.3, R * 0.8, cx + sd * R * 1.25, 0)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); setc(ctx, INK); ctx.set_line_width(30 * S + 8); ctx.stroke_preserve()
        setc(ctx, DAD['skin']); ctx.set_line_width(30 * S); ctx.stroke()
    d = draw(ctx, 0, dy, KDAD, f_, DAD, p)
    for sd in (-1, 1):   # fists gripping the rod
        ellipse(ctx, cx + sd * R * 1.25, 0, 22 * S, 20 * S); fl(ctx, DAD['skin'], 4)
    ctx.restore()
    return d, b, 0


HANG_P = lambda lf, **kw: P(**dict(dict(eye='shock', mouth='scream'), **kw), lhip=60 + 14 * math.sin(lf * 0.5), lkn=-90, rhip=-50 + 14 * math.sin(lf * 0.5 + 1), rkn=-80)
PANIC_K = lambda lf, **kw: P(lsh=150 + 20 * math.sin(lf * 1.1), lel=-30, rsh=40, rel=-60, **kw)


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = CZ + 0.04 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, CX, CY + 10, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    room(ctx, lf); rod(ctx); lava(ctx, lf); sofa(ctx); armchair(ctx); table(ctx)
    hop = -16 * abs(math.sin(lf * 0.4))
    stand(ctx, KID, KIDX, KKID, P(eye='happy', mouth='scream', lsh=150 + 10 * math.sin(lf * 0.8), lel=-20, rsh=60, rel=-90,
                                   head=6, lhip=10, rhip=-10), 1, SEAT + hop)
    wob = 4 * math.sin(lf * 0.6)
    d = stand(ctx, DAD, TABX - 20, KDAD, P(eye='shock', mouth='open', lsh=110, lel=-40, rsh=70, rel=-90, rhip=-70, rkn=80,
                                            lhip=4, rot=wob), 1, TABTOP)
    mug(ctx, d['front'][0], d['front'][1] - 10, 0.2)
    sweat_drops(ctx, d, lf)
    dog(ctx, CHX + 10, CHSEAT + 4, 0.42, -1, lf)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"THE FLOOR IS LAVA!!\"", 540, 1560, 96, YEL, -0.04, t)
    label(ctx, "*bubble bubble*", 540, 620, 74, ORANGE, 0.04, 1 if lf == f else pop(lf, 2, 5))


# ------------------------------------------------------------------ shot 2: "I'm a GROWN-UP" -> BLOOP -> leap
def beat1(ctx, f, il):
    # il 0..140: 0-44 deadpan ; 44 BLOOP ; 70-96 leap to armchair ; 96-140 crouched "it's HOT!!"
    pin = eio(pop(il, 0, 40))
    z = lerp(CZ, 1.45, pin)
    cx = lerp(CX, 1180, pin)
    ctx.save(); cam(ctx, cx, lerp(CY, 1230, pin), z, 0, shake_at(il, [44, 96], 10, 12), f)
    room(ctx, il); rod(ctx); lava(ctx, il); sofa(ctx); armchair(ctx); table(ctx)
    stand(ctx, KID, KIDX, KKID, P(eye='happy' if il < 44 else 'shock', mouth='grin' if il < 44 else 'open', lsh=40, lel=-80, rsh=40, rel=-80), 1, SEAT)
    if il < 70:
        sc = il >= 44
        d = stand(ctx, DAD, TABX, KDAD, P(eye='smug' if not sc else 'shock', mouth='flat' if not sc else 'scream',
                                          lsh=20, lel=-110, rsh=30, rel=-40, head=-6 if not sc else 4,
                                          rhip=-30 * sc, rkn=60 * sc), 1, TABTOP - 30 * pop(il, 44, 50) * (1 - pop(il, 50, 60)))
        mug(ctx, d['front'][0] + 6, d['front'][1] - 14, 0.1)
        if sc:
            sweat_drops(ctx, d, il)
        # the bubble
        bx, by = TABX + 150, FLOOR + 40
        r = 20 + 60 * pop(il, 20, 44)
        if il < 44:
            ellipse(ctx, bx, by, r, r * 0.8); fl(ctx, LAVA2, 4)
            ellipse(ctx, bx - r * 0.3, by - r * 0.3, r * 0.25, r * 0.2); setc(ctx, (1, 1, 0.85, 0.9)); ctx.fill()
        elif il < 62:
            u = pop(il, 44, 62)
            for k in range(7):
                a = math.pi + k * math.pi / 6
                ellipse(ctx, bx + 160 * u * math.cos(a), by + 240 * u * math.sin(a) + 300 * u * u, 14, 14); fl(ctx, LAVA2, 3)
    elif il < 96:
        u = eio(pop(il, 70, 94))
        x = lerp(TABX, CHX, u); y = lerp(TABTOP, CHSEAT, u) - 260 * math.sin(math.pi * u)
        stand(ctx, DAD, x, KDAD, P(eye='shock', mouth='scream', lsh=160, lel=-20, rsh=150, rel=-20, lhip=50, lkn=-70, rhip=-40, rkn=-60,
                                   rot=-20 * math.sin(math.pi * u)), 1, y)
        mug(ctx, lerp(TABX + 40, TABX + 260, u), 1300 - 400 * math.sin(math.pi * u * 0.9), u * 9)
    else:
        bounce = 20 * math.exp(-(il - 96) / 6) * abs(math.sin((il - 96) * 0.9))
        d = stand(ctx, DAD, CHX, KDAD, P(eye='shock', mouth='wavy', lsh=50, lel=-120, rsh=40, rel=-110, lhip=40, lkn=-60, rhip=-40, rkn=-50),
                  1, CHSEAT - bounce)
        sweat_drops(ctx, d, il)
        for k in range(3):   # steam from the lava
            sx = CHX - 200 + k * 200; sy = FLOOR - 40 - ((il * 4 + k * 40) % 140)
            ctx.new_path(); ctx.move_to(sx, sy); ctx.curve_to(sx + 20, sy - 30, sx - 20, sy - 50, sx, sy - 80)
            setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(10); ctx.stroke()
        if il > 104:
            mug(ctx, TABX + 300, FLOOR + 40 + (il - 104) * 1.5, 2.6)
    if il < 96:
        dog(ctx, CHX + 10, CHSEAT + 4, 0.42, -1, il)
    else:
        dog(ctx, KIDX - 120, SEAT + 4, 0.42, 1, il)
    ctx.restore()
    if il < 44:
        label(ctx, "\"Son... I'm a", 540, 1440, 96, WHITE, -0.03, pop(il, 2, 6))
        label(ctx, "GROWN-UP.\"", 540, 1550, 110, WHITE, -0.03, pop(il, 8, 12))
    elif il < 70:
        label(ctx, "*BLOOP!*", 540, 1500, 130, ORANGE, -0.05, pop(il, 44, 47))
    elif il < 96:
        label(ctx, "*BOING!*", 540, 1500, 130, GOLD, 0.05, pop(il, 72, 75))
    else:
        label(ctx, "\"...it's HOT!!\"", 540, 1500, 120, YEL, 0.03, pop(il, 100, 104))


def s2(ctx, f):
    beat1(ctx, f, f - 60)


# ------------------------------------------------------------------ shot 3: cushion hops -> curtain rod
CUSH = [(1210, PURPLE), (1050, MINT), (890, GOLD)]


def montage(ctx, f, il):
    # il 0..130 : 0-20 kid throws cushions "USE THE CUSHIONS!" ; 20-62 hops BOING x3 (right->left ... then back) ;
    # 62-78 last cushion sinks "SINKING!!" ; 78-96 leap to the rod ; 96-130 low angle swing "GO DAD GO!!"
    if il < 96:
        ctx.save(); cam(ctx, 1100, 1260, 1.2, -5, shake_at(il, [26, 40, 54, 80], 7, 10), f)
        room(ctx, il); rod(ctx); lava(ctx, il); sofa(ctx); armchair(ctx); table(ctx)
        # kid on the sofa
        thr = il < 20
        stand(ctx, KID, KIDX, KKID, P(eye='happy', mouth='scream', lsh=160 if thr else 150, lel=-10, rsh=60 if thr else 150, rel=-40), 1, SEAT)
        # cushions (fly in, then float)
        for j, (cx_, col) in enumerate(CUSH):
            u = eio(pop(il, j * 5, j * 5 + 14))
            x = lerp(KIDX + 40, cx_, u); y = lerp(1250, FLOOR + 20, u) - 200 * math.sin(math.pi * u)
            sink = pop(il, 62, 80) if j == 2 else 0
            cushion(ctx, x, y + 4 * math.sin(il * 0.3 + j), col, sink)
        # Dad: armchair -> cushion 0 -> 1 -> 2 (hop arcs)
        stops = [(CHX, CHSEAT)] + [(c[0], FLOOR + 6) for c in CUSH]
        if il < 20:
            x, y = stops[0]; rot = 0; air = 0
        elif il < 62:
            seg = min(2, (il - 20) // 14); u = ((il - 20) - seg * 14) / 14
            (x0, y0), (x1, y1) = stops[seg], stops[seg + 1]
            x = lerp(x0, x1, eio(u)); y = lerp(y0, y1, eio(u)) - 150 * math.sin(math.pi * u); air = math.sin(math.pi * u); rot = -10 * air
        elif il < 78:
            x, y = stops[3]; y += 40 * pop(il, 62, 80); rot = 6 * math.sin(il * 1.3); air = 0
        else:
            u = eio(pop(il, 78, 94))
            x = lerp(stops[3][0], 1300, u); y = lerp(stops[3][1] + 40, ROD + 380, u) - 160 * math.sin(math.pi * u); rot = -14 * u; air = 1
        if il < 86:
            p = P(eye='shock' if il >= 62 else 'glare', mouth='scream', lsh=150 if air > 0.3 else 60, lel=-20 if air > 0.3 else -100,
                  rsh=140 if air > 0.3 else 50, rel=-20 if air > 0.3 else -100, lhip=40 * air, lkn=-60 * air, rhip=-30 * air, rkn=-50 * air, rot=rot)
            d = stand(ctx, DAD, x, KDAD, p, -1 if il >= 20 else 1, y)
            if il >= 62:
                sweat_drops(ctx, d, il)
        else:
            hang(ctx, 1300, ROD, HANG_P(il), 1, 0.15 * math.sin(il * 0.3))
        dog(ctx, KIDX - 120, SEAT + 4, 0.42, 1, il)
        ctx.restore()
        if il < 20:
            label(ctx, "\"USE THE CUSHIONS!\"", 540, 1500, 100, WHITE, -0.03, pop(il, 1, 5))
        elif il < 62:
            label(ctx, "*BOING! BOING! BOING!*", 540, 1500, 90, GOLD, -0.05, pop(il, 22, 25))
        elif il < 80:
            label(ctx, "*glub glub*", 540, 1390, 100, ORANGE, 0.05, pop(il, 62, 65))
            label(ctx, "\"...SINKING!!\"", 540, 1520, 120, YEL, 0.03, pop(il, 64, 68))
        else:
            label(ctx, "*CREAK!*", 540, 1500, 120, hx('d08a4a'), -0.04, pop(il, 88, 91))
    else:
        # low angle: Dad swinging from the rod, kid cheering
        lt = il - 96
        ctx.save(); cam(ctx, 1110, 1200, 1.02, 4, shake_at(lt, [0], 6, 8), f)
        room(ctx, il); rod(ctx); lava(ctx, il); sofa(ctx); armchair(ctx); table(ctx)
        stand(ctx, KID, KIDX, KKID, P(eye='happy', mouth='grin', lsh=165, lel=-10, rsh=160, rel=-10), 1, SEAT - 30 * abs(math.sin(lt * 0.4)))
        hang(ctx, 1300 + 0 * lt, ROD, HANG_P(il), 1, 0.25 * math.sin(lt * 0.25))
        for j, (cx_, col) in enumerate(CUSH[:2]):
            cushion(ctx, cx_, FLOOR + 24 + 4 * math.sin(il * 0.3 + j), col)
        dog(ctx, KIDX - 120, SEAT + 4, 0.42, 1, il)
        ctx.restore()
        label(ctx, "\"GO DAD GO!!\"", 540, 1500, 120, MINT, 0.03, pop(lt, 2, 6))


def s3(ctx, f):
    montage(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: the one close-up
def s4(ctx, f):
    il = f - 330
    ctx.save(); cam(ctx, 1300, ROD + 230, 1.9 + 0.1 * eio(il / 70), 0, shake_at(il, [36], 5, 6) + 2, f)
    room(ctx, il); rod(ctx); lava(ctx, il)
    d, b, hy = hang(ctx, 1300, ROD, HANG_P(il, eye='glare' if il < 36 else 'shock', mouth='scream'), 1, 0.04 * math.sin(il * 0.3))
    ctx.restore()
    if il < 36:
        label(ctx, "\"NEVER... TOUCH...\"", 540, 1400, 110, WHITE, -0.03, pop(il, 3, 7))
    else:
        label(ctx, "\"...THE LAVA!!\"", 540, 1400, 130, YEL, 0.03, pop(il, 36, 39))
    # sweat in screen space (around the face)
    for k in range(3):
        sweat(ctx, 220 + k * 330, 700 + ((il * 6 + k * 50) % 300), il, 1.0)


# ------------------------------------------------------------------ shot 5: Mom plays too -> loop
def finale(ctx, f, il):
    # il 0..230 (f 400..630): 0-40 Mom "Dinner's READY!" ; 40-76 "MOM!! THE LAVA!!" ; 76 shades click ; 90 robovac beep ;
    # 100-160 ride across "Last one to the table... does the DISHES." ; 160-180 "...DISHES?!" ; 180 CRACK ; 188 SPLOOSH ;
    # 196-230 Dad in the lava "...I'll get the sponge."
    ctx.save(); cam(ctx, CX, CY + 20, 1.16, 0, shake_at(il, [40, 76, 180, 188], 8, 10), f)
    room(ctx, il)
    rod(ctx, pop(il, 180, 186))
    lava(ctx, il); sofa(ctx); armchair(ctx); table(ctx)
    # kid
    if il < 40:
        kp = P(eye='happy', mouth='grin', lsh=40, lel=-80, rsh=40, rel=-80)
    elif il < 100:
        kp = PANIC_K(il, eye='shock', mouth='scream')
    elif il < 160:
        kp = P(eye='shock', mouth='open', lsh=30, lel=-150, rsh=30, rel=-140)
    elif il < 196:
        kp = P(eye='shock', mouth='scream', lsh=150, lel=-20, rsh=150, rel=-20)
    else:
        kp = P(eye='closed', mouth='grin', lsh=30, lel=-150, rsh=40, rel=-90, head=10 * math.sin(il * 0.8))
    stand(ctx, KID, KIDX, KKID, kp, 1, SEAT)
    # Mom: doorway -> robot vacuum ride
    if il < 100:
        mp = P(eye='happy', mouth='smile', lsh=150, lel=-20, rsh=30, rel=-40) if il < 40 else \
            (P(eye='shock', mouth='open', lsh=30, lel=-60, rsh=20, rel=-60, head=-8) if il < 66 else
             P(eye='smug', mouth='grin', lsh=30, lel=-60, rsh=150, rel=-150, head=-4))
        vx = lerp(DOORX + 500, DOORX, eio(pop(il, 82, 98)))
        if il >= 82:
            robovac(ctx, vx, FLOOR + 30, il)
        d = stand(ctx, MOM, DOORX, KMOM, mp, -1, FLOOR - 4)
        if il >= 76:
            shades(ctx, d)
    else:
        u = eio(pop(il, 104, 160))
        mx = lerp(DOORX, 1750, u)
        robovac(ctx, mx, FLOOR + 30, il)
        d = stand(ctx, MOM, mx, KMOM, P(eye='smug', mouth='grin', lsh=150, lel=-20, rsh=30, rel=-60, torso=-6, head=-4), 1, FLOOR - 4)
        shades(ctx, d)
        if il < 160:
            for k in range(3):
                ctx.move_to(mx - 160 - k * 50, FLOOR - 80 + k * 30); ctx.line_to(mx - 260 - k * 50, FLOOR - 80 + k * 30); ink(ctx, 6); ctx.stroke()
    # Dad: hanging -> falls -> sits in the lava
    if il < 180:
        hp = HANG_P(il, eye='shock' if il < 100 else 'shock', mouth='scream' if 40 <= il < 76 or il >= 160 else 'open')
        hang(ctx, 1300, ROD, hp, 1, 0.08 * math.sin(il * 0.3))
    elif il < 188:
        u = pop(il, 180, 188)
        stand(ctx, DAD, 1300, KDAD, P(eye='shock', mouth='scream', lsh=170, lel=-6, rsh=170, rel=-6, lhip=40, lkn=-60, rhip=-30, rkn=-50),
              1, lerp(ROD + 520, FLOOR + 60, u * u))
    else:
        sp = pop(il, 188, 200)
        stand(ctx, DAD, 1300, KDAD, P(eye='closed' if il > 200 else 'shock', mouth='flat', lsh=30, lel=-10, rsh=30, rel=-10,
                                     lhip=86, lkn=-86, rhip=88, rkn=-88), 1, FLOOR + 110)
        lava_front(ctx, il, 1110, 1490, FLOOR + 30)
        if il < 206:
            for k in range(9):
                a = math.pi + k * math.pi / 8
                ellipse(ctx, 1300 + 260 * sp * math.cos(a), FLOOR + 20 + 300 * sp * math.sin(a) + 400 * sp * sp, 16, 16); fl(ctx, LAVA2, 3)
        else:
            for k in range(2):
                sx = 1240 + k * 120; sy = FLOOR - 40 - ((il * 4 + k * 60) % 120)
                ctx.new_path(); ctx.move_to(sx, sy); ctx.curve_to(sx + 20, sy - 30, sx - 20, sy - 50, sx, sy - 80)
                setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(10); ctx.stroke()
    dog(ctx, KIDX - 120, SEAT + 4, 0.42, 1, il)
    ctx.restore()
    if 76 <= il < 160:
        card(ctx, 'p2', il, 78)
    if il < 40:
        label(ctx, "\"Dinner's READY!\"", 540, 1500, 110, WHITE, -0.03, pop(il, 2, 6))
    elif il < 76:
        label(ctx, "\"MOM!! THE LAVA!!\"", 540, 1500, 115, YEL, 0.03, pop(il, 40, 43))
    elif il < 100:
        label(ctx, "*click*", 540, 640, 90, WHITE, -0.04, pop(il, 76, 79))
        label(ctx, "*beep boop*", 540, 1500, 100, CYAN, 0.04, pop(il, 86, 89))
    elif il < 160:
        if il < 130:
            label(ctx, "\"Last one to the table...\"", 540, 1500, 90, WHITE, -0.03, pop(il, 102, 106))
        else:
            label(ctx, "\"...does the DISHES.\"", 540, 1500, 105, PINK, 0.03, pop(il, 130, 134))
    elif il < 180:
        label(ctx, "\"...DISHES?!\"", 540, 1500, 130, YEL, -0.03, pop(il, 160, 163))
    elif il < 196:
        label(ctx, "*CRACK!*", 540, 640, 130, hx('d08a4a'), 0.05, pop(il, 180, 183))
        label(ctx, "*SPLOOSH!*", 540, 1500, 130, ORANGE, -0.04, pop(il, 188, 191))
    else:
        label(ctx, "\"...I'll get the sponge.\"", 540, 1500, 95, WHITE, -0.03, pop(il, 200, 204))


def s5(ctx, f):
    lf = f - 400
    if lf < 230:
        finale(ctx, f, lf)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (200, s3), (330, s4), (400, s5)]
CUTS = (60, 200, 296, 330, 400, 630)


def render(f):
    import sketch
    sketch.BOIL[0] = f // 4
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.1, 0.05, 0.15, 0.2)
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
                              "-i", "out/lava_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
