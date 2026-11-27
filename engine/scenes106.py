"""'BUILDING A SNOWMAN WITH DAD'. Original, general-audience comedy short, 22s.
Hook:   snowy back-yard medium shot: red-faced Dad pushing a snowball as big as he is "BIGGER... BIGGER!!" +
        caption 'BUILDING A SNOWMAN WITH DAD:'; the kid next to his tiny finished snowman, the dog watching.
Beat 1: kid "Dad... that's big ENOUGH!" -> Dad "ONE more ROLL!" -> *CRUNCH* the ball tips over the edge of the hill,
        Dad flops face-first *FLOMP* -> looks up "...uh-oh."
Beat 2: Dutch-tilt chase down the hill: the ball rumbles and GROWS, scooping up the garden gnome *BONK!* and the sled,
        Dad sprinting after it "COME BACK!!" -> it hits a stump *BOING*, rolls BACK uphill at him "...it's coming BACK?!"
        -> *FWUMP!* swallows Dad, arms + boots spinning "HELP!!"
Beat 3: *KA-THUMP!* into the bottom fence -> the one close-up: frozen blue Dad's head poking out next to the gnome
        "...big ENOUGH?"
Twist:  the kid adds a carrot nose *boop* + buttons "BEST. SNOWMAN. EVER!" Mom *CLICK* photo -> PLOT TWIST: IT STILL
        NEEDS A HEAD. kid points up the hill "Now the HEAD, Dad!" -> Dad twitch "...the HEAD?!" -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face, rays
from scenes58 import sweat, twitch
from scenes65 import dog
from scenes84 import eio
import scenes85
from scenes85 import blob, chunks, hat, snow_fall, pine as pine85
import scenes13
from scenes13 import card as _card13

RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
SNOW = hx('f7fbff'); SNOW_S = hx('cfe3f7'); ICE = hx('a8d8ff')
DAD = dict(doodle.DAD, shirt=hx('ff4d5e'), pants=hx('34477e'), shoes=hx('7a4a2c'))
DAD_R = dict(DAD, skin=hx('f28a78'))
DAD_B = dict(DAD, skin=hx('b8d4f0'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('3fd6a0'), pants=hx('3d7bff'), shoes=hx('ffc93c'))
MOM = dict(doodle.MOM_G, shirt=hx('b88aff'))
N = 660
HZ = 1190                 # back lawn line (house base)
TOP = 1560                # feet on the flat yard
EDGE, FOOT = 1500, 2900   # slope from EDGE (top) to FOOT (bottom)
BOT = 2340                # feet at the bottom of the hill
FENCE = 3120

CAPS = {'p1': [[("BUILDING A ", OUT), ("SNOWMAN", BLUE)], [("WITH ", OUT), ("DAD:", RED)]],
        'p2': [[("PLOT TWIST:", RED)], [("IT STILL NEEDS ", OUT), ("A HEAD.", PURPLE)]]}
scenes13.CAPS = CAPS
card = _card13


def gy(x):
    if x <= EDGE:
        return TOP
    if x >= FOOT:
        return BOT
    u = (x - EDGE) / (FOOT - EDGE)
    return lerp(TOP, BOT, 0.5 - 0.5 * math.cos(math.pi * u))


def stand(ctx, ch, x, k, p, f_=1, feet=None):
    feet = gy(x) if feet is None else feet
    return draw(ctx, x, feet - 186 * k, k, f_, ch, p)


# ------------------------------------------------------------------ props
def gnome(ctx, x, y, s=1.0, rot=0.0, eye='normal'):
    """little garden gnome, (x, y) = base"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rect_r(ctx, -34, -70, 68, 70, 20); fl(ctx, hx('3d7bff'), 4)
    ellipse(ctx, 0, -92, 30, 28); fl(ctx, hx('ffd2b0'), 4)
    poly(ctx, [(-34, -66), (34, -66), (22, -40), (0, -24), (-22, -40)]); fl(ctx, WHITE, 4)
    poly(ctx, [(-36, -106), (36, -106), (6, -190)]); fl(ctx, RED, 4)
    ellipse(ctx, 0, -84, 9, 7); setc(ctx, hx('ff9a9a')); ctx.fill()
    for sx in (-1, 1):
        if eye == 'shock':
            ellipse(ctx, sx * 12, -98, 6, 7); fl(ctx, WHITE, 2)
        else:
            ellipse(ctx, sx * 12, -98, 4, 4); setc(ctx, INK); ctx.fill()
    ctx.restore()


def sled(ctx, x, y, s=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rect_r(ctx, -110, -40, 220, 40, 14); fl(ctx, RED, 4)
    ctx.new_path(); ctx.move_to(-120, 14); ctx.line_to(110, 14); ctx.curve_to(150, 14, 150, -30, 120, -40)
    ink(ctx, 14); ctx.stroke()
    ctx.new_path(); ctx.move_to(-120, 14); ctx.line_to(110, 14); ctx.curve_to(150, 14, 150, -30, 120, -40)
    setc(ctx, GOLD); ctx.set_line_width(7); ctx.stroke()
    ctx.restore()


def carrot(ctx, x, y, s=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    poly(ctx, [(0, -14), (70, 0), (0, 14)]); fl(ctx, ORANGE, 3)
    for k in range(2):
        ctx.move_to(22 + k * 18, -8 + k * 2); ctx.line_to(26 + k * 18, 6 - k * 2)
    setc(ctx, dark(ORANGE, 0.7)); ctx.set_line_width(3); ctx.stroke()
    for a in (-0.5, 0, 0.5):
        ctx.move_to(0, 0); ctx.line_to(-22 * math.cos(a), -22 * math.sin(a))
    setc(ctx, INK); ctx.set_line_width(12); ctx.stroke_preserve(); setc(ctx, GREEN); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def tiny_snowman(ctx, x, y, s=1.0, lf=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, -48, 56, 50); fl(ctx, SNOW, 4)
    ellipse(ctx, 0, -128, 40, 37); fl(ctx, SNOW, 4)
    for sx in (-1, 1):
        ellipse(ctx, sx * 13, -136, 5, 6); setc(ctx, INK); ctx.fill()
        ellipse(ctx, sx * 24, -120, 7, 4); setc(ctx, hx('ff9aa8')); ctx.fill()
    poly(ctx, [(-3, -128), (34, -122), (-2, -116)]); fl(ctx, ORANGE, 2)
    ctx.new_path(); ctx.arc(0, -114, 10, 0.4, math.pi - 0.4); ink(ctx, 3); ctx.stroke()
    rect_r(ctx, -40, -100, 80, 16, 7); fl(ctx, PINK, 3)
    for k in range(2):
        ellipse(ctx, 0, -64 + k * 24, 5, 5); setc(ctx, INK); ctx.fill()
    for sx in (-1, 1):
        ctx.move_to(sx * 46, -60); ctx.line_to(sx * 96, -88 - 6 * math.sin(lf * 0.2)); setc(ctx, hx('8a5a3a')); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def snowball(ctx, x, y, r, ang, items=(), lf=0):
    """rolling snowball; items = list of (kind, angle_on_ball, size)"""
    ellipse(ctx, x + r * 0.15, y + r * 0.96, r * 0.95, r * 0.14); setc(ctx, (0.55, 0.66, 0.85, 0.45)); ctx.fill()
    ellipse(ctx, x, y, r, r); fl(ctx, SNOW, max(6, r * 0.03))
    ctx.save(); ellipse(ctx, x, y, r, r); ctx.clip()
    g = cairo.RadialGradient(x - r * 0.35, y - r * 0.4, r * 0.1, x, y, r * 1.05)
    g.add_color_stop_rgb(0, 1, 1, 1); g.add_color_stop_rgb(0.6, 0.9, 0.94, 1.0); g.add_color_stop_rgb(1, 0.66, 0.77, 0.95)
    ctx.set_source(g); ctx.paint()
    rnd = random.Random(3)
    for k in range(9):                       # rotating clumps + swirl, sells the roll
        a = ang + rnd.uniform(0, 6.28); d = r * rnd.uniform(0.25, 0.85)
        ellipse(ctx, x + d * math.cos(a), y + d * math.sin(a), r * 0.13, r * 0.09, a); setc(ctx, (0.72, 0.82, 0.96, 0.75)); ctx.fill()
    for k in range(3):
        a = ang + k * 2.1
        ctx.new_path(); ctx.arc(x, y, r * (0.45 + 0.15 * k), a, a + 1.2); setc(ctx, (0.6, 0.72, 0.92, 0.6)); ctx.set_line_width(max(3, r * 0.02)); ctx.stroke()
    ctx.restore()
    for kind, a0, s in items:
        a = ang + a0
        px, py = x + r * 0.92 * math.cos(a), y + r * 0.92 * math.sin(a)
        if kind == 'gnome':
            gnome(ctx, px, py, s, a + math.pi / 2 + math.pi, 'shock')
        elif kind == 'sled':
            sled(ctx, px, py, s, a + math.pi / 2)
        elif kind == 'mitten':
            ellipse(ctx, px, py, 26 * s, 34 * s, a); fl(ctx, PINK, 3)
    ellipse(ctx, x - r * 0.42, y - r * 0.45, r * 0.16, r * 0.1, -0.6); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()


def dad_in_ball(ctx, x, y, r, ang, lf, p=None, ch=DAD_R, boots=True, arms=True, hk=0.34):
    """Dad packed into the snowball: head out at angle ang-90deg, mitts + boots poking out."""
    up = ang - math.pi / 2
    Rt = r * hk
    # boots + mitts behind the packed snow
    if boots:
        for da in (math.pi - 0.38, math.pi + 0.38):
            a = up + da; bx, by = x + r * 0.98 * math.cos(a), y + r * 0.98 * math.sin(a)
            ctx.save(); ctx.translate(bx, by); ctx.rotate(a + math.pi / 2)
            rect_r(ctx, -Rt * 0.3, -Rt * 0.5, Rt * 0.6, Rt * 0.7, Rt * 0.15); fl(ctx, DAD['pants'], 4)
            ellipse(ctx, Rt * 0.12, Rt * 0.3, Rt * 0.42, Rt * 0.26); fl(ctx, DAD['shoes'], 4)
            ctx.restore()
    if arms:
        wv = 0.25 * math.sin(lf * 0.8)
        for sd in (-1, 1):
            a = up + sd * (1.15 + wv * sd)
            bx, by = x + r * 1.02 * math.cos(a), y + r * 1.02 * math.sin(a)
            ctx.save(); ctx.translate(bx, by); ctx.rotate(a + math.pi / 2)
            rect_r(ctx, -Rt * 0.18, -Rt * 0.1, Rt * 0.36, Rt * 0.6, Rt * 0.15); fl(ctx, ch['shirt'], 4)
            ellipse(ctx, 0, -Rt * 0.18, Rt * 0.26, Rt * 0.24); fl(ctx, hx('ffc93c'), 4)
            ctx.restore()
    hxp, hyp = x + r * 0.9 * math.cos(up), y + r * 0.9 * math.sin(up)
    p = p or P(eye='shock', mouth='scream')
    ctx.save()
    ctx.rectangle(-5000, -5000, 15000, 15000); ctx.new_sub_path(); ctx.arc(x, y, r * 0.74, 0, 2 * math.pi)
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); ctx.clip(); ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    face(ctx, ch, p, hxp, hyp, Rt, up + math.pi / 2)
    ctx.restore()
    # snow lumps packed round his neck
    for k in range(5):
        a = up + (k - 2) * 0.16
        ellipse(ctx, x + r * 0.73 * math.cos(a), y + r * 0.73 * math.sin(a), r * 0.09, r * 0.06, a); setc(ctx, SNOW); ctx.fill()
    return hxp, hyp, Rt


# ------------------------------------------------------------------ set: snowy back yard on a hill
def sky(ctx, lf):
    ctx.set_source(vgrad(ctx, 0, -600, 0, 2200, [(0, hx('8fc8ff')), (0.6, hx('cfe8ff')), (1, hx('eaf4ff'))]))
    ctx.rectangle(-3000, -3000, 9000, 9000); ctx.fill()
    ellipse(ctx, 180, 300, 90, 90); fl(ctx, hx('fff3a0'), 5)
    for cx_, cy_ in ((500 + 0.3 * lf, 360), (1500 + 0.2 * lf, 280), (2600, 420), (3400, 600)):
        for dx, r in ((-60, 50), (0, 70), (64, 50)):
            ellipse(ctx, cx_ + dx, cy_, r, r * 0.8); fl(ctx, WHITE, 5)
    # distant valley hills + tiny pines
    for (x, y, rx, ry, c) in ((2300, 1700, 900, 380, hx('d6e4fb')), (3500, 1750, 1000, 420, hx('c6d8f6')), (1700, 1850, 600, 300, hx('dfeafc'))):
        ellipse(ctx, x, y, rx, ry); fl(ctx, c, 4)
    rnd = random.Random(2)
    for k in range(14):
        x = rnd.uniform(1700, 4000); y = 1480 + rnd.uniform(0, 260)
        poly(ctx, [(x - 26, y), (x, y - 80), (x + 26, y)]); fl(ctx, hx('7fb8a0'), 3)


def ground(ctx):
    # top edge of the snow: back lawn line on the flat yard, then follows the hill down
    ctx.new_path(); ctx.move_to(-3000, HZ)
    x = EDGE - 300
    ctx.line_to(x, HZ)
    for i in range(41):
        xx = EDGE - 300 + i * (FOOT + 200 - EDGE + 300) / 40
        ctx.line_to(xx, gy(xx + 300) - (TOP - HZ))
    ctx.line_to(6000, BOT - (TOP - HZ)); ctx.line_to(6000, 5000); ctx.line_to(-3000, 5000); ctx.close_path()
    fl(ctx, SNOW, 6)
    rnd = random.Random(8)
    for k in range(40):
        x = rnd.uniform(-800, 3800); y = gy(x) - rnd.uniform(-120, 300)
        ellipse(ctx, x, y, 60, 10); setc(ctx, SNOW_S[:3] + (0.7,)); ctx.fill()
    # sled tracks down the hill
    for off in (-14, 14):
        ctx.new_path()
        for i in range(30):
            xx = EDGE + 200 + i * 45
            ctx.line_to(xx, gy(xx) - 60 + off)
        setc(ctx, (0.7, 0.8, 0.95, 0.8)); ctx.set_line_width(5); ctx.stroke()


def house(ctx, lf, mom=False):
    cx = 120
    rect_r(ctx, cx - 420, 620, 840, HZ - 620 + 10, 8); fl(ctx, hx('ffd8a8'), 7)
    for k in range(6):
        ctx.move_to(cx - 410, 700 + k * 80); ctx.line_to(cx + 410, 700 + k * 80)
    setc(ctx, dark(hx('ffd8a8'), 0.9)); ctx.set_line_width(4); ctx.stroke()
    poly(ctx, [(cx - 480, 640), (cx, 380), (cx + 480, 640)]); fl(ctx, hx('d0566a'), 8)
    ctx.new_path(); ctx.move_to(cx - 500, 656); ctx.line_to(cx, 360); ctx.line_to(cx + 500, 656)
    for i in range(8):
        xq = cx + 500 - 1000 * (i + 1) / 8; xm = xq + 1000 / 16
        ctx.curve_to(xm + 20, 700, xm - 20, 700, xq, 656)
    ctx.close_path(); fl(ctx, SNOW, 6)
    for k in range(8):
        xq = cx - 420 + k * 110
        poly(ctx, [(xq - 12, 670), (xq + 12, 670), (xq + 2, 670 + 40 + 30 * (k % 3))]); fl(ctx, ICE, 3)
    # back door window with warm light (+ Mom later)
    wx = cx + 220
    rect_r(ctx, wx - 110, 760, 220, 200, 12); fl(ctx, hx('ffe9a8'), 7)
    if mom:
        ctx.save(); rect_r(ctx, wx - 110, 760, 220, 200, 12); ctx.clip()
        face(ctx, MOM, P(eye='happy', mouth='smile'), wx - 20, 880, 60)
        ctx.restore()
    ctx.move_to(wx, 760); ctx.line_to(wx, 960); ctx.move_to(wx - 110, 860); ctx.line_to(wx + 110, 860); ink(ctx, 6); ctx.stroke()
    blob(ctx, wx - 130, wx + 130, 964, 30, 3, lw=4)
    # star garland under the eaves
    for k in range(9):
        sparkle(ctx, cx - 380 + k * 95, 720 + 14 * math.sin(k * 1.3), 14, GOLD if k % 2 else PINK)


def feeder(ctx, x, lf):
    ctx.rectangle(x - 8, 900, 16, TOP - 380 - 900 + 380); fl(ctx, hx('8a5a3a'), 4)
    poly(ctx, [(x - 80, 920), (x, 860), (x + 80, 920)]); fl(ctx, RED, 4)
    blob(ctx, x - 80, x + 80, 905, 26, 4, lw=3)
    rect_r(ctx, x - 60, 920, 120, 70, 6); fl(ctx, hx('ffd8a8'), 4)
    ellipse(ctx, x, 955, 22, 22); setc(ctx, INK); ctx.fill()
    # little bird
    hop = abs(math.sin(lf * 0.25)) * 10
    ellipse(ctx, x + 40, 1000 - hop, 26, 20); fl(ctx, hx('3d8bff'), 3)
    ellipse(ctx, x + 56, 988 - hop, 14, 13); fl(ctx, hx('3d8bff'), 3)
    poly(ctx, [(x + 68, 986 - hop), (x + 82, 990 - hop), (x + 68, 994 - hop)]); fl(ctx, ORANGE, 2)
    ellipse(ctx, x + 60, 984 - hop, 3, 3); setc(ctx, INK); ctx.fill()


def fence(ctx):
    y = BOT
    for k in range(12):
        x = FENCE + k * 60 - 80
        poly(ctx, [(x, y + 40), (x, y - 220), (x + 22, y - 246), (x + 44, y - 220), (x + 44, y + 40)]); fl(ctx, hx('c98a52'), 5)
        ellipse(ctx, x + 22, y - 246, 26, 10); fl(ctx, SNOW, 3)
    for yy in (y - 170, y - 60):
        ctx.rectangle(FENCE - 90, yy, 740, 22); fl(ctx, hx('b07a46'), 4)


def stump(ctx, x):
    y = gy(x)
    rect_r(ctx, x - 60, y - 90, 120, 100, 14); fl(ctx, hx('9a6a3e'), 5)
    ellipse(ctx, x, y - 92, 60, 20); fl(ctx, hx('e0b880'), 4)
    blob(ctx, x - 64, x + 64, y - 96, 30, 6, lw=3)


STUMP = 2620


def world(ctx, lf, gnome_on=True, sled_on=True, mom=False, snowman_on=True):
    sky(ctx, lf)
    house(ctx, lf, mom)
    pine85(ctx, 720, HZ + 60, 0.75)
    ground(ctx)
    feeder(ctx, 1240, lf)
    fence(ctx)
    pine85(ctx, 3560, BOT + 40, 0.9)
    stump(ctx, STUMP)
    blob(ctx, 2960, 3200, BOT + 60, 70, 9, lw=4)
    if sled_on:
        sled(ctx, 1830, gy(1830) - 14, 0.8, math.atan2(gy(1850) - gy(1810), 40))
    if gnome_on:
        gnome(ctx, 2150, gy(2150) + 6, 0.9, 0.35)
    if snowman_on:
        tiny_snowman(ctx, 440, TOP + 10, 1.0, lf)


# ------------------------------------------------------------------ shot 1: hook
BX0, BR0 = 1170, 215           # ball at the hook
DADX0 = 880


def push_dad(ctx, lf, x, ch=DAD_R, eye='glare', mouth='scream', k=1.08):
    w = math.sin(lf * 0.7)
    p = P(eye=eye, mouth=mouth, torso=24, head=-14, lsh=-80 + 10 * w, lel=-20, rsh=-90 - 10 * w, rel=-10,
          lhip=-30 + 20 * w, lkn=-30, rhip=24 - 20 * w, rkn=-10)
    d = stand(ctx, ch, x, k, p, 1)
    hat(ctx, d, BLUE)
    sweat(ctx, d['head'][0] - d['R'] * 1.0, d['head'][1] - d['R'] * 0.3, lf, 1.0)
    return d


def hook(ctx, f, lf):
    z = 1.06 + 0.03 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, 900, 1230, z, 0, 2 + shake_at(lf, [0], 6, 8), f)
    world(ctx, lf)
    kp = P(eye='normal', mouth='flat', lsh=-30, lel=-100, rsh=30, rel=100, head=6)
    kd = stand(ctx, KID, 600, 0.78, kp, 1)
    hat(ctx, kd, PINK)
    dog(ctx, 290, TOP + 20, 0.42, 1, lf)
    bx = BX0 + 6 * math.sin(lf * 0.7)
    snowball(ctx, bx, TOP - BR0, BR0, lf * 0.04, (('mitten', 2.4, 1.0),), lf)
    push_dad(ctx, lf, DADX0 + 6 * math.sin(lf * 0.7))
    ctx.restore()
    snow_fall(ctx, lf, 26, 0.7)


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"BIGGER...", 540, 1360, 110, WHITE, -0.04, t)
    label(ctx, "BIGGER!!\"", 540, 1465, 136, RED, 0.03, t)


# ------------------------------------------------------------------ shot 2: big enough? -> one more roll -> over the edge
def beat1(ctx, f, il):
    # 0-40 kid "that's big ENOUGH!" ; 40-70 Dad "ONE more ROLL!" pushing ; 70 *CRUNCH* tip ; 72-110 ball rolls off,
    # Dad flops *FLOMP* @78 ; 110-140 Dad looks up "...uh-oh."
    if il < 40:
        cx, cy, z = 760, 1240, 1.15
    elif il < 70:
        u = eio(pop(il, 40, 50)); cx, cy, z = lerp(760, 1080, u), 1240, lerp(1.15, 1.1, u)
    else:
        u = eio(pop(il, 70, 100)); cx, cy, z = lerp(1080, 1500, u), lerp(1240, 1420, u), lerp(1.1, 0.92, u)
    ctx.save(); cam(ctx, cx, cy, z, 0, shake_at(il, [70, 78], 12, 18), f)
    world(ctx, il)
    # kid + dog
    if il < 40:
        kp = P(eye='normal', mouth='open', lsh=-20, lel=-40, rsh=-120, rel=-30, head=6)
    else:
        kp = P(eye='shock', mouth='open', lsh=-150, lel=-20, rsh=150, rel=20)
    kd = stand(ctx, KID, 600, 0.78, kp, 1)
    hat(ctx, kd, PINK)
    dog(ctx, 290, TOP + 20, 0.42, 1, il)
    # ball
    if il < 40:
        bx = BX0 + 4 * math.sin(il * 0.7); r = BR0; ang = il * 0.02
    elif il < 70:
        u = pop(il, 40, 70); bx = lerp(BX0, EDGE - 40, u); r = BR0 + 15 * u; ang = (bx - BX0) / r
    else:
        u = pop(il, 70, 110); bx = lerp(EDGE - 40, EDGE + 900, ein(u)); r = BR0 + 15 + 40 * u; ang = (bx - BX0) / r
    by = gy(bx) - r
    snowball(ctx, bx, by, r, ang, (('mitten', 2.4, 1.0),), il)
    # Dad
    if il < 40:
        p = P(eye='happy', mouth='grin', lsh=-20, lel=-60, rsh=-160, rel=10, torso=-4)
        d = stand(ctx, DAD_R, DADX0, 1.08, p, 1); hat(ctx, d, BLUE)
    elif il < 72:
        dx = lerp(DADX0, EDGE - 40 - BR0 - 290, pop(il, 40, 70))
        push_dad(ctx, il * 1.4, dx, eye='glare', mouth='grin')
    elif il < 110:
        fall = eout(pop(il, 72, 80))
        dx = EDGE - 40 - BR0 - 290 + 140 * fall
        p = P(eye='shock', mouth='scream', torso=24 + 66 * fall, head=-14, lsh=-150, lel=0, rsh=-160, rel=0, lhip=-20, rhip=40, lkn=-10, rkn=-10)
        d = draw(ctx, dx, TOP - 186 * 1.08 + 120 * fall, 1.08, 1, DAD_R, p); hat(ctx, d, BLUE)
        if il >= 78:
            dust_puff(ctx, dx + 150, TOP - 10, pop(il, 78, 96))
    else:
        dx = EDGE - 40 - BR0 - 150
        p = P(eye='shock', mouth='flat', torso=90, head=-70, lsh=-150, lel=0, rsh=-160, rel=0, lhip=-20, rhip=40, lkn=-10, rkn=-10)
        d = draw(ctx, dx, TOP - 186 * 1.08 + 120, 1.08, 1, DAD_R, p); hat(ctx, d, BLUE)
    ctx.restore()
    snow_fall(ctx, il, 26, 0.7)
    if il < 40:
        label(ctx, "\"Dad... that's", 540, 1360, 100, MINT, -0.03, pop(il, 3, 7))
        if il >= 14:
            label(ctx, "big ENOUGH!\"", 540, 1465, 120, MINT, 0.03, pop(il, 14, 18))
    elif il < 70:
        label(ctx, "\"ONE more", 540, 1360, 110, WHITE, -0.03, pop(il, 42, 46))
        if il >= 52:
            label(ctx, "ROLL!\"", 540, 1465, 140, RED, 0.04, pop(il, 52, 55))
    elif il < 110:
        label(ctx, "*CRUNCH!*", 540, 520, 110, CYAN, -0.05, pop(il, 70, 73))
        if il >= 80:
            label(ctx, "*FLOMP!*", 540, 1430, 120, WHITE, 0.04, pop(il, 80, 83))
    else:
        label(ctx, "\"...uh-oh.\"", 540, 1430, 120, YEL, 0.03, pop(il, 112, 116))


def dust_puff(ctx, x, y, t):
    if t <= 0 or t >= 1:
        return
    for k in range(7):
        a = math.pi + k * math.pi / 6
        d = 40 + 140 * eout(t)
        ellipse(ctx, x + d * math.cos(a) * 1.4, y + d * math.sin(a) * 0.6, 40 * (1 - t) + 10, 32 * (1 - t) + 8); setc(ctx, (1, 1, 1, 0.9 * (1 - t))); ctx.fill()


def s2(ctx, f):
    beat1(ctx, f, f - 60)


# ------------------------------------------------------------------ shot 3: chase down the hill
def ballx_chase(il):
    # 0-60 roll down from EDGE+600 to STUMP-ish ; 60 BOING off the stump -> rolls back ; 86 FWUMP swallows Dad ; then on down
    if il < 60:
        return lerp(EDGE + 650, STUMP - 330, ease(il / 60))
    if il < 86:
        return lerp(STUMP - 330, STUMP - 640, eout(pop(il, 60, 86)))
    return lerp(STUMP - 640, STUMP - 330, ein(pop(il, 86, 130)))


def chase(ctx, f, il):
    bx = ballx_chase(il)
    r = 260 + 70 * pop(il, 0, 60)
    by = gy(bx) - r
    ang = bx / r + (0 if il < 60 else 0)
    dxp0 = lerp(EDGE + 200, STUMP - 1140, ease(il / 60)) if il < 60 else STUMP - 1100
    cxc = (bx + dxp0) / 2 if il < 86 else bx - 40
    cyc = (by + gy(dxp0) - 200) / 2 + 60 if il < 86 else by + 60
    ctx.save(); cam(ctx, cxc, cyc, 0.7, -9, 3 + shake_at(il, [10, 34, 60, 86], 12, 18), f)
    world(ctx, il, gnome_on=il < 10, sled_on=il < 34)
    items = [('mitten', 2.4, 1.0)]
    if il >= 10:
        items.append(('gnome', 1.2, 1.2))
    if il >= 34:
        items.append(('sled', -0.9, 1.1))
    # Dad running behind, then swallowed
    if il < 86:
        ph = il * 0.9; s = math.sin(ph)
        dxp = lerp(EDGE + 200, STUMP - 1140, ease(il / 60)) if il < 60 else lerp(STUMP - 1140, STUMP - 1080, pop(il, 60, 86))
        if il < 60:
            p = P(eye='glare', mouth='scream', torso=14, lsh=-120 + 40 * s, lel=-20, rsh=-150 - 30 * s, rel=0,
                  lhip=40 * s, rhip=-40 * s, lkn=-60, rkn=-60)
        else:
            p = P(eye='shock', mouth='scream', torso=-14, lsh=-160, lel=0, rsh=160, rel=0, lhip=-10, rhip=20, lkn=-20, rkn=-10)
        bob = abs(s) * 30 if il < 60 else 0
        d = stand(ctx, DAD_R, dxp, 1.1, p, 1, gy(dxp) - bob); hat(ctx, d, BLUE)
        snowball(ctx, bx, by, r, ang, items, il)
    else:
        snowball(ctx, bx, by, r, ang, items, il)
        dad_in_ball(ctx, bx, by, r, ang, il)
        if il < 96:
            dust_puff(ctx, bx - r * 0.6, by, pop(il, 86, 96))
    if 60 <= il < 72:
        rays(ctx, STUMP - 80, gy(STUMP) - 100, 40, 200, il * 0.1, (1, 1, 0.7), 0.6, 10)
    ctx.restore()
    snow_fall(ctx, il, 30, 0.7)
    if il < 34:
        label(ctx, "\"COME BACK!!\"", 540, 1430, 120, RED, -0.03, pop(il, 2, 6))
        if il >= 10:
            label(ctx, "*BONK!*", 540, 520, 100, YEL, 0.05, pop(il, 10, 13))
    elif il < 60:
        label(ctx, "*RUMBLE RUMBLE*", 540, 520, 90, CYAN, -0.04, pop(il, 34, 37))
        label(ctx, "\"COME BACK!!\"", 540, 1430, 120, RED, 0.03, 1)
    elif il < 86:
        label(ctx, "*BOING!*", 540, 520, 110, YEL, 0.05, pop(il, 60, 63))
        label(ctx, "\"...it's coming", 540, 1360, 100, WHITE, -0.03, pop(il, 64, 68))
        label(ctx, "BACK?!\"", 540, 1465, 140, RED, 0.04, pop(il, 70, 73))
    else:
        label(ctx, "*FWUMP!*", 540, 520, 120, WHITE, -0.05, pop(il, 86, 89))
        if il >= 96:
            label(ctx, "\"HELP!!\"", 540, 1430, 140, RED, 0.04, pop(il, 96, 99))


def s3(ctx, f):
    chase(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: KA-THUMP into the fence -> close-up
RF = 340
BXF = FENCE - 90 - RF + 20


def crash(ctx, f, il):
    # 0-16 last roll into the fence ; 16 KA-THUMP ; 16-44 settle
    u = pop(il, 0, 16)
    bx = lerp(BXF - 700, BXF, ein(u) if il < 16 else 1)
    by = gy(bx) - RF
    ang = (bx - BXF) / RF
    ctx.save(); cam(ctx, BXF - 60, BOT - 420, 0.72, 0, shake_at(il, [16], 16, 30), f)
    world(ctx, il, gnome_on=False, sled_on=False)
    snowball(ctx, bx, by, RF, ang, (('mitten', 2.4, 1.0), ('gnome', 1.2, 1.2), ('sled', -0.9, 1.1)), il)
    dad_in_ball(ctx, bx, by, RF, ang, il, P(eye='closed' if il >= 16 else 'shock', mouth='wavy' if il >= 16 else 'scream'), arms=True)
    if il >= 16:
        dust_puff(ctx, bx + RF * 0.6, by - RF * 0.6, pop(il, 16, 36))
        dust_puff(ctx, bx + RF * 0.8, by + RF * 0.4, pop(il, 17, 38))
        stars_ko(ctx, bx, by - RF - 60, il * 0.2)
    ctx.restore()
    snow_fall(ctx, il, 26, 0.7)
    if il >= 16:
        label(ctx, "*KA-THUMP!!*", 540, 520, 120, YEL, -0.05, pop(il, 16, 19))


def stars_ko(ctx, x, y, t):
    for k in range(4):
        a = t + k * math.pi / 2
        sparkle(ctx, x + 110 * math.cos(a), y + 30 * math.sin(a), 22, YEL)


def closeup(ctx, f, il):
    # the one face shot: frozen Dad's head out of the snow, gnome beside him, teeth chatter
    z = 1 + 0.05 * eio(il / 60)
    ctx.save(); cam(ctx, 540, 960, z, 2 * math.sin(il * 0.3), 2 + 3 * (il % 4 < 2), f)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('bfe0ff')), (1, hx('eaf4ff'))])); ctx.paint()
    for cx_, cy_ in ((200, 420), (900, 330)):
        for dx, r in ((-60, 50), (0, 70), (64, 50)):
            ellipse(ctx, cx_ + dx, cy_, r, r * 0.8); fl(ctx, WHITE, 5)
    sh = 6 * math.sin(il * 2.2)
    face(ctx, DAD_B, P(eye='shock', mouth='flat'), 540 + sh, 880, 200)
    hat(ctx, dict(head=(540 + sh, 880), R=200 * 1.0), BLUE, snowy=True)
    # icicle drips + frost
    for k, x in enumerate((420, 520, 640)):
        poly(ctx, [(x - 10 + sh, 1050), (x + 10 + sh, 1050), (x + sh, 1100 + 20 * (k % 2))]); fl(ctx, ICE, 3)
    # big snow surface up to his chin
    ctx.new_path(); ctx.move_to(-200, 1060)
    for i in range(9):
        x = -200 + i * 190
        ctx.curve_to(x + 60, 1010 + 30 * (i % 2), x + 130, 1010 + 30 * (i % 2), x + 190, 1040)
    ctx.line_to(1300, 2200); ctx.line_to(-200, 2200); ctx.close_path(); fl(ctx, SNOW, 7)
    ctx.rectangle(-200, 1250, 1500, 900); setc(ctx, (0.78, 0.87, 0.98, 0.5)); ctx.fill()
    gnome(ctx, 860, 1180, 1.7, 0.3, 'shock')
    ellipse(ctx, 230, 1150, 40, 50, 0.4); fl(ctx, PINK, 4)
    for k in range(3):
        sparkle(ctx, 140 + k * 380, 1200 + 40 * k, 18, WHITE)
    ctx.restore()
    label(ctx, "*chatter chatter*", 540, 520, 80, CYAN, 0.03, pop(il, 2, 6))
    label(ctx, "\"...big", 540, 1360, 110, WHITE, -0.03, pop(il, 8, 12))
    if il >= 26:
        label(ctx, "ENOUGH?\"", 540, 1465, 140, BLUE, 0.04, pop(il, 26, 29))


def s4(ctx, f):
    il = f - 340
    if il < 40:
        crash(ctx, f, il)
    else:
        closeup(ctx, f, il - 40)


# ------------------------------------------------------------------ shot 5: decorate -> photo -> needs a head
def finale(ctx, f, il):
    # 0-60 kid + dog run down, carrot *boop* @20, buttons @30/36/42, "BEST. SNOWMAN. EVER!" 44-70 ;
    # 74 Mom at the top *CLICK* flash ; 84-114 card ; 114-200 kid points uphill "Now the HEAD, Dad!" ; Dad twitch "...the HEAD?!"
    bx, by = BXF, BOT - RF
    if il < 114:
        cx, cy, z = BXF - 450, BOT - 500, 0.72
    else:
        u = eio(pop(il, 114, 130)); cx, cy, z = lerp(BXF - 450, BXF - 200, u), lerp(BOT - 500, BOT - 400, u), lerp(0.72, 1.0, u)
    ctx.save(); cam(ctx, cx, cy, z, 0, shake_at(il, [20, 74], 8, 10), f)
    world(ctx, il, gnome_on=False, sled_on=False)
    snowball(ctx, bx, by, RF, 0, (('mitten', 2.4, 1.0), ('gnome', 1.2, 1.2), ('sled', -0.9, 1.1)), il)
    if il < 150:
        dp = P(eye='closed' if il < 20 else 'shock', mouth='wavy' if il < 60 else 'flat')
    else:
        dp = P(eye='glare', mouth='scream')
    hxp, hyp, Rt = dad_in_ball(ctx, bx, by, RF, 0, il, dp, ch=DAD_B, hk=0.42)
    hat(ctx, dict(head=(hxp, hyp), R=Rt), BLUE, snowy=True)
    if il >= 20:
        carrot(ctx, hxp + Rt * 0.25, hyp + Rt * 0.15, max(0.03, 0.9 * eout(pop(il, 20, 24))), 0.1)
    for k, t0 in enumerate((30, 36, 42)):
        if il >= t0:
            rr = 26 * eout(pop(il, t0 - 1, t0 + 3))
            ellipse(ctx, bx, by - RF * 0.25 + k * RF * 0.28, rr, rr); fl(ctx, hx('3a3040'), 3)
    if il >= 150:
        twitch(ctx, hxp + Rt * 1.0, hyp - Rt * 1.1, il, 1.0)
    # kid + dog
    kx = lerp(BXF - 900, BXF - 520, eout(pop(il, 0, 18)))
    if il < 18:
        s = math.sin(il * 1.0)
        kp = P(eye='happy', mouth='open', torso=10, lsh=-120 + 40 * s, lel=-20, rsh=-150 - 30 * s, rel=0, lhip=40 * s, rhip=-40 * s, lkn=-50, rkn=-50)
    elif il < 46:
        kp = P(eye='happy', mouth='grin', torso=8, lsh=-20, lel=-40, rsh=-120, rel=-20)
    elif il < 114:
        hop = 1
        kp = P(eye='happy', mouth='open', lsh=-160, lel=-10, rsh=160, rel=10)
    else:
        kp = P(eye='happy', mouth='open', lsh=-20, lel=-40, rsh=-130, rel=-20, head=-8)
    jump = abs(math.sin((il - 46) * 0.4)) * 50 if 46 <= il < 80 else 0
    kd = stand(ctx, KID, kx, 0.95, kp, 1 if il < 114 else -1, BOT - jump)
    hat(ctx, kd, PINK)
    dog(ctx, lerp(BXF - 1150, BXF - 760, eout(pop(il, 0, 22))), BOT + 20, 0.55, 1, il)
    if 56 <= il < 114:
        mx = lerp(BXF - 1500, BXF - 960, eout(pop(il, 56, 70)))
        mp = P(eye='happy', mouth='grin', lsh=-100, lel=-40, rsh=-110, rel=-30, head=-4)
        md = stand(ctx, MOM, mx, 1.0, mp, 1, BOT)
        fx, fy = md['front']
        rect_r(ctx, fx - 10, fy - 70, 56, 90, 10); fl(ctx, hx('3a3a4a'), 4)
    ctx.restore()
    # Mom's photo flash
    if 74 <= il < 84:
        ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.85 * (1 - (il - 74) / 10))); ctx.fill()
    snow_fall(ctx, il, 26, 0.7)
    if 84 <= il < 114:
        card(ctx, 'p2', il, 84, 114)
    if il < 30:
        label(ctx, "*boop*", 540, 520, 90, ORANGE, 0.04, pop(il, 20, 23))
    elif il < 74:
        label(ctx, "*pop! pop! pop!*", 540, 520, 80, WHITE, -0.03, pop(il, 30, 33))
        if il >= 46:
            label(ctx, "\"BEST. SNOWMAN.", 540, 1360, 100, MINT, -0.03, pop(il, 46, 50))
            label(ctx, "EVER!\"", 540, 1465, 140, MINT, 0.04, pop(il, 54, 57))
    elif il < 84:
        label(ctx, "*CLICK!*", 540, 1430, 120, WHITE, 0.04, pop(il, 74, 77))
    elif il >= 114 and il < 150:
        label(ctx, "\"Now make the", 540, 1360, 100, MINT, -0.03, pop(il, 116, 120))
        label(ctx, "HEAD, Dad!\"", 540, 1465, 130, MINT, 0.04, pop(il, 124, 127))
    elif il >= 150:
        label(ctx, "\"...the", 540, 1360, 100, WHITE, -0.03, pop(il, 152, 156))
        label(ctx, "HEAD?!\"", 540, 1465, 150, RED, 0.04, pop(il, 160, 163))


def s5(ctx, f):
    lf = f - 440
    if lf < 190:
        finale(ctx, f, lf)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (200, s3), (340, s4), (440, s5)]
CUTS = (60, 200, 340, 380, 440, 630)


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
                              "-i", "out/snowman_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
