"""'There's ALWAYS room for dessert' - original, general-audience comedy short, 22s.
Hook:   after a big dinner the whole family is melted on the sofa with round tummies; Dad groaning "I can't... MOVE..."
        Caption "AFTER EVERY BIG DINNER:"
Beat 1: Dad tries to stand: rocks forward x3 "HNNNGH!!" -> falls back *BOING*
Beat 2: his trouser button POPS *PING!* -> ricochets off the picture frame -> *PLOP* into Mom's tea. "...thanks."
Beat 3: Mom: "Who wants to help with the DISHES?" -> everyone instantly "asleep" *SNORE* -> Mom twitch "...REALLY?!"
Turn:   Mom ECU whisper "...who wants PIE?" -> eyes PING open -> ZOOM: everyone at the table with forks "ME!!" (dog too)
Twist:  "PLOT TWIST: THE DOG GOT THERE FIRST." empty pie dish, round dog under the table *BURP*
        -> Mom with a salad bowl "...who wants SALAD?" -> empty chairs + dust, everyone back on the sofa groaning -> loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face, zzz
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes65 import dog, mug
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
WOOD = hx('c9874e'); CRUST = hx('f0b060'); FILL = hx('c8506a')
DAD = dict(doodle.DAD, shirt=hx('ff9e5c'), pants=hx('3d5a9e'))
MOM = dict(doodle.MOM_G, shirt=hx('8a6cff'), pants=hx('2f4a8a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('5fd3a0'), pants=hx('3d7bff'), shoes=hx('ff4d5e'))
N = 660
FLOOR = 1560
SEAT = 1330                     # sofa seat top
KDAD, KMOM, KKID = 1.05, 1.0, 0.88
TABLE = 1330                    # dining table top
FRAME = (700, 640)              # picture frame centre (button ricochet)
DADX, KIDX, DOGX, MOMX = 300, 600, 780, 1060

CAPS = {'p1': [[("AFTER EVERY ", OUT), ("BIG DINNER:", ORANGE)]],
        'p2': [[("PLOT TWIST:", RED)], [("THE DOG GOT THERE ", OUT), ("FIRST!", PINK)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def belly(ctx, hip, k, f_, g, ch, tor=0.0, wob=0.0):
    """round tummy bulging forward from a seated character's hip; returns the button position"""
    S = k * 1.35
    a = math.radians(tor)
    ux, uy = f_ * math.sin(a), -math.cos(a)
    rx = 46 * S * (1 + 0.75 * g) * (1 + 0.04 * wob); ry = 50 * S * (1 + 0.45 * g) * (1 - 0.04 * wob)
    cx = hip[0] + ux * 52 * S + f_ * 26 * S * g
    cy = hip[1] + uy * 52 * S
    ellipse(ctx, cx, cy, rx, ry, a * f_); fl(ctx, ch['shirt'], max(3, 3.6 * S))
    ctx.save(); ellipse(ctx, cx, cy, rx, ry, a * f_); ctx.clip()
    ctx.rectangle(cx - rx * 1.2, cy + ry * 0.62, rx * 2.4, ry); fl(ctx, ch['pants'], 3 * S)
    ctx.restore()
    ellipse(ctx, cx, cy, rx, ry, a * f_); ink(ctx, max(3, 3.6 * S)); ctx.stroke()
    ellipse(ctx, cx - f_ * rx * 0.35, cy - ry * 0.35, rx * 0.22, ry * 0.12, -0.5 * f_); setc(ctx, (1, 1, 1, 0.45)); ctx.fill()
    return (cx + f_ * rx * 0.45, cy + ry * 0.72)


def tummy_char(ctx, x, hipy, k, f_, ch, p, g, btn=True, wob=0.0):
    b = draw_hip(ctx, x, hipy, k, f_, ch, p)
    bp = belly(ctx, (x, hipy), k, f_, g, ch, p['torso'], wob)
    if btn:
        ellipse(ctx, bp[0], bp[1], 9 * k, 9 * k); fl(ctx, GOLD, 3)
    hd, R = b['head'], b['R']
    ctx.save(); ctx.new_path(); ctx.arc(hd[0], hd[1] - R * 0.3, R * 1.3, 0, 2 * math.pi); ctx.clip()
    draw_hip(ctx, x, hipy, k, f_, ch, p)
    ctx.restore()
    b['btn'] = bp
    return b


def pie(ctx, x, y, s=1.0, eaten=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 10, 150, 40); fl(ctx, hx('dfe8f2'), 6)                     # dish
    if eaten < 1:
        ctx.save()
        if eaten > 0:
            ctx.new_path(); ctx.move_to(0, -10); ctx.arc(0, -10, 200, -math.pi / 2 + 2 * math.pi * eaten, 1.5 * math.pi); ctx.close_path(); ctx.clip()
        ellipse(ctx, 0, -6, 128, 34); fl(ctx, CRUST, 6)
        ellipse(ctx, 0, -12, 108, 26); fl(ctx, FILL, 4)
        for i in range(-3, 4):
            ctx.move_to(i * 30 - 20, -34); ctx.line_to(i * 30 + 20, 10)
            ctx.move_to(i * 30 + 20, -34); ctx.line_to(i * 30 - 20, 10)
        ctx.save(); ellipse(ctx, 0, -12, 108, 26); ctx.clip(); setc(ctx, CRUST); ctx.set_line_width(10); ctx.stroke(); ctx.restore()
        ctx.new_path()
        ctx.restore()
    else:
        for cx_, cy_ in ((-40, 0), (20, 6), (60, -4), (-70, 8)):
            ellipse(ctx, cx_, cy_, 9, 6); fl(ctx, CRUST, 2)
    ctx.restore()


def salad(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for i, (dx, dy, c) in enumerate(((-50, -40, GREEN), (0, -56, hx('7ed36b')), (50, -40, GREEN), (-20, -30, RED), (30, -28, hx('ffb347')))):
        ellipse(ctx, dx, dy, 44, 30, 0.3 * (i - 2)); fl(ctx, c, 4)
    ctx.new_path(); ctx.move_to(-110, -20); ctx.curve_to(-100, 70, 100, 70, 110, -20); ctx.close_path(); fl(ctx, hx('ffffff'), 6)
    ctx.move_to(-80, 10); ctx.curve_to(-40, 30, 40, 30, 80, 10); setc(ctx, CYAN); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def fork(ctx, x, y, a=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -6, -10, 12, 90, 5); fl(ctx, hx('d8dde6'), 3)
    rect_r(ctx, -18, -50, 36, 44, 6); fl(ctx, hx('d8dde6'), 3)
    for i in (-9, 0, 9):
        ctx.move_to(i, -50); ctx.line_to(i, -26)
    ink(ctx, 3); ctx.stroke()
    ctx.restore()


def dishes(ctx, x, y):
    for i in range(7):
        ellipse(ctx, x + 6 * math.sin(i * 1.7), y - i * 18, 90, 20); fl(ctx, WHITE if i % 2 else hx('dfe8f2'), 4)
    for i in range(4):
        ellipse(ctx, x + 170 + 4 * math.sin(i), y - i * 16, 70, 16); fl(ctx, hx('ffe08a'), 4)
    rect_r(ctx, x - 160, y - 90, 50, 90, 10); fl(ctx, hx('a8e0ff'), 4)      # glass


def fat_dog(ctx, x, y, s, f_, lf, g=1.0, sleep=True, pie_face=False):
    dog(ctx, x, y, s, f_, lf, sleep=sleep)
    if g > 0:
        ctx.save(); ctx.translate(x, y); ctx.scale(f_ * s, s)
        for fx in (-90, 70):
            ellipse(ctx, fx, -8, 34, 16); fl(ctx, hx('b9844a'), 6)
        ellipse(ctx, -10, -105, 150 + 30 * g, 95 + 20 * g); fl(ctx, hx('e8b878'), 7)
        ellipse(ctx, -60, -150, 40, 16, -0.3); setc(ctx, (1, 1, 1, 0.45)); ctx.fill()
        ctx.new_path(); ctx.arc(-10, -80, 50, 0.3, math.pi - 0.3); ink(ctx, 4); ctx.stroke()
        ctx.restore()
        ctx.save(); ctx.translate(x, y); ctx.scale(f_ * s, s); ctx.new_path(); ctx.arc(160, -228, 104, 0, 2 * math.pi); ctx.restore()
        ctx.save(); ctx.clip(); dog(ctx, x, y, s, f_, lf, sleep=sleep); ctx.restore()
    if pie_face:
        ctx.save(); ctx.translate(x, y); ctx.scale(f_ * s, s)
        for cx_, cy_, r in ((205, -170, 18), (230, -190, 12), (180, -160, 14), (215, -150, 10)):
            ellipse(ctx, cx_, cy_, r, r * 0.8); fl(ctx, FILL if r > 12 else CRUST, 3)
        ctx.restore()


def window(ctx, lf):
    x, y, w, h = 300, 560, 300, 330
    rect_r(ctx, x, y, w, h, 14); fl(ctx, hx('2a3a7a'), 8)                  # night sky
    ctx.save(); rect_r(ctx, x, y, w, h, 14); ctx.clip()
    ellipse(ctx, x + 210, y + 90, 40, 40); setc(ctx, hx('fff6c0')); ctx.fill()
    ellipse(ctx, x + 226, y + 80, 36, 36); setc(ctx, hx('2a3a7a')); ctx.fill()
    for i, (sx, sy) in enumerate(((x + 60, y + 70), (x + 120, y + 180), (x + 250, y + 230), (x + 80, y + 260))):
        sparkle(ctx, sx, sy, 10 + 3 * math.sin(lf * 0.3 + i), YEL)
    ctx.restore()
    ctx.move_to(x + w / 2, y); ctx.line_to(x + w / 2, y + h); ink(ctx, 7); ctx.stroke()
    rect_r(ctx, x - 24, y + h - 4, w + 48, 26, 8); fl(ctx, WHITE, 6)
    for sx, d in ((x - 40, -1), (x + w - 10, 1)):
        poly(ctx, [(sx, y - 30), (sx + 50, y - 30), (sx + 50 + d * 10, y + h + 50), (sx - 10 + d * 4, y + h + 50)]); fl(ctx, hx('ff9e5c'), 6)
    rect_r(ctx, x - 70, y - 44, w + 140, 20, 8); fl(ctx, hx('a0603a'), 5)


def picture(ctx, tilt=0.0):
    ctx.save(); ctx.translate(*FRAME); ctx.rotate(tilt)
    ctx.move_to(0, -110); ctx.line_to(-60, -75); ctx.move_to(0, -110); ctx.line_to(60, -75); ink(ctx, 4); ctx.stroke()
    rect_r(ctx, -90, -75, 180, 150, 10); fl(ctx, hx('8ad4ff'), 7)
    rect_r(ctx, -70, -55, 140, 110, 6); fl(ctx, hx('fff6d8'), 4)
    for dx, c in ((-30, hx('ff9ec4')), (0, hx('ffc93c')), (30, hx('7ed36b'))):           # tiny family doodle
        ellipse(ctx, dx, -5, 14, 14); fl(ctx, c, 3)
        ctx.move_to(dx, 10); ctx.line_to(dx, 38); ink(ctx, 4); ctx.stroke()
    ctx.restore()


def bunting(ctx, x0, x1, y):
    ctx.move_to(x0, y); ctx.curve_to(x0 + (x1 - x0) * 0.3, y + 60, x0 + (x1 - x0) * 0.7, y + 60, x1, y); ink(ctx, 4); ctx.stroke()
    cols = (ORANGE, GOLD, RED, hx('c8506a'), GREEN)
    n = 9
    for i in range(n):
        t = (i + 0.5) / n
        px = x0 + (x1 - x0) * t; py = y + 60 * 4 * t * (1 - t) * 0.75
        poly(ctx, [(px - 24, py), (px + 24, py), (px, py + 46)]); fl(ctx, cols[i % 5], 3)


def sofa(ctx, x0=40, x1=600):
    rect_r(ctx, x0, SEAT - 260, x1 - x0, 300, 50); fl(ctx, hx('6fa8ff'), 8)
    rect_r(ctx, x0 - 40, SEAT - 60, 90, 230, 30); fl(ctx, hx('5a94f0'), 7)
    rect_r(ctx, x1 - 50, SEAT - 60, 90, 230, 30); fl(ctx, hx('5a94f0'), 7)
    rect_r(ctx, x0 + 30, SEAT - 10, x1 - x0 - 60, 140, 30); fl(ctx, hx('8fc0ff'), 7)
    ellipse(ctx, x0 + 110, SEAT - 110, 60, 46, 0.3); fl(ctx, hx('ffd34f'), 5)          # cushion
    for lx in (x0 + 10, x1 - 40):
        rect_r(ctx, lx, SEAT + 160, 30, FLOOR - SEAT - 150, 8); fl(ctx, hx('5a3a2a'), 5)


def armchair(ctx, x):
    rect_r(ctx, x - 150, SEAT - 230, 300, 280, 50); fl(ctx, hx('ff8fb8'), 8)
    rect_r(ctx, x - 180, SEAT - 50, 70, 210, 26); fl(ctx, hx('ff6fa0'), 7)
    rect_r(ctx, x + 110, SEAT - 50, 70, 210, 26); fl(ctx, hx('ff6fa0'), 7)
    rect_r(ctx, x - 120, SEAT - 6, 240, 130, 26); fl(ctx, hx('ffb3cf'), 7)
    for lx in (x - 150, x + 120):
        rect_r(ctx, lx, SEAT + 120, 28, FLOOR - SEAT - 110, 8); fl(ctx, hx('5a3a2a'), 5)


def chair(ctx, x, f_=1):
    bx = x - f_ * 80
    rect_r(ctx, bx - 14, TABLE - 260, 28, FLOOR - TABLE + 270, 10); fl(ctx, WOOD, 6)
    rect_r(ctx, bx - 30, TABLE - 280, 60, 60, 16); fl(ctx, hx('e09a5c'), 5)
    rect_r(ctx, x - 100, TABLE + 60, 200, 30, 10); fl(ctx, hx('ff8a5c'), 6)
    rect_r(ctx, x + f_ * 70 - 12, TABLE + 80, 24, FLOOR - TABLE - 70, 8); fl(ctx, WOOD, 6)


def table(ctx, x0=1380, x1=2160, top=TABLE):
    rect_r(ctx, x0 + 30, top + 30, 34, FLOOR - top - 20, 8); fl(ctx, WOOD, 6)
    rect_r(ctx, x1 - 64, top + 30, 34, FLOOR - top - 20, 8); fl(ctx, WOOD, 6)
    rect_r(ctx, x0, top, x1 - x0, 40, 12); fl(ctx, WOOD, 7)
    poly(ctx, [(x0 - 10, top - 4), (x1 + 10, top - 4), (x1 + 10, top + 90), (x0 - 10, top + 90)]); fl(ctx, hx('fff6d8'), 6)  # cloth
    for i in range(int((x1 - x0) / 60) + 1):
        ellipse(ctx, x0 + i * 60, top + 90, 30, 14); fl(ctx, hx('fff6d8'), 4)
    for i in range(0, int((x1 - x0) / 60)):
        rect_r(ctx, x0 + i * 60 + 20, top + 20, 20, 20, 4); setc(ctx, (1, 0.6, 0.6, 0.6)); ctx.fill()


def room(ctx, lf, frame_tilt=0.0):
    wall = hx('ffe3b8')
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, wall); ctx.fill()
    rnd = random.Random(80)
    for k in range(140):                                       # little stars wallpaper
        sx, sy = rnd.uniform(-400, 2500), rnd.uniform(-300, FLOOR - 140)
        sparkle(ctx, sx, sy, 9, dark(wall, 0.9))
    ctx.rectangle(-3000, FLOOR - 120, 9000, 120); setc(ctx, hx('ffd29a')); ctx.fill()
    ctx.move_to(-3000, FLOOR - 120); ctx.line_to(6000, FLOOR - 120); ink(ctx, 5); ctx.stroke()
    window(ctx, lf)
    picture(ctx, frame_tilt)
    bunting(ctx, 60, 1160, 380)
    bunting(ctx, 1360, 2200, 380)
    # floor lamp right of the armchair
    ctx.move_to(1240, FLOOR); ctx.line_to(1240, 860); ink(ctx, 8); ctx.stroke()
    poly(ctx, [(1180, 860), (1300, 860), (1270, 760), (1210, 760)]); fl(ctx, hx('ffd34f'), 6)
    ellipse(ctx, 1240, FLOOR, 50, 12); fl(ctx, hx('5a3a2a'), 5)
    # dining: hanging lamp + shelf with a plant
    ctx.move_to(1770, -400); ctx.line_to(1770, 760); ink(ctx, 6); ctx.stroke()
    ctx.new_path(); ctx.move_to(1680, 840); ctx.curve_to(1690, 770, 1730, 740, 1770, 740); ctx.curve_to(1810, 740, 1850, 770, 1860, 840); ctx.close_path(); fl(ctx, hx('7ed36b'), 6)
    ellipse(ctx, 1770, 846, 26, 14); setc(ctx, hx('fff6c0')); ctx.fill()
    rect_r(ctx, 1420, 760, 200, 18, 6); fl(ctx, hx('a0603a'), 4)
    poly(ctx, [(1490, 760), (1550, 760), (1540, 700), (1500, 700)]); fl(ctx, hx('7a8cff'), 4)
    for a in (-0.6, 0, 0.6):
        ellipse(ctx, 1520 + 40 * math.sin(a), 660 - 20 * math.cos(a), 16, 40, a); fl(ctx, GREEN, 3)
    # floor + rug
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('d8a06a')); ctx.fill()
    for k in range(-10, 40):
        ctx.move_to(k * 150, FLOOR); ctx.line_to(k * 150 - 140, FLOOR + 600)
    setc(ctx, hx('c48b55')); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-3000, FLOOR); ctx.line_to(6000, FLOOR); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 620, FLOOR + 130, 520, 90); fl(ctx, hx('ffb3cf'), 6)
    ellipse(ctx, 620, FLOOR + 130, 430, 66); setc(ctx, hx('ffd6e5')); ctx.fill()
    sofa(ctx)
    armchair(ctx, MOMX)
    # plant between sofa & window side
    px = -60
    poly(ctx, [(px - 55, FLOOR - 120), (px + 55, FLOOR - 120), (px + 42, FLOOR + 10), (px - 42, FLOOR + 10)]); fl(ctx, hx('7a8cff'), 6)
    for a in (-0.7, -0.25, 0.2, 0.65):
        ellipse(ctx, px + 80 * math.sin(a), FLOOR - 210 - 36 * math.cos(a), 30, 84, a); fl(ctx, GREEN, 5)


# ------------------------------------------------------------------ people
SIT = dict(torso=-22, head=6, lhip=88, lkn=-88, rhip=82, rkn=-82, lsh=-30, lel=-20, rsh=-18, rel=-30)


def sofa_dad(ctx, lf, g=1.0, p=None, wob=0.0, btn=True, x=DADX, hipy=SEAT + 4):
    p = p or P(eye='closed', mouth='wavy', **SIT)
    return tummy_char(ctx, x, hipy, KDAD, 1, DAD, p, g, btn, wob)


def floor_kid(ctx, lf, g=1.0, p=None):
    p = p or P(eye='closed', mouth='wavy', torso=-38, head=10, lhip=90, lkn=-6, rhip=86, rkn=-10, lsh=-40, lel=-10, rsh=-30, rel=-10)
    return tummy_char(ctx, KIDX, FLOOR + 50, KKID, -1, KID, p, g, False)


def chair_mom(ctx, lf, p=None, mug_on=True, splash=0.0):
    p = p or P(eye='smug', mouth='smile', torso=-8, lhip=88, lkn=-88, rhip=82, rkn=-82, lsh=10, lel=-60, rsh=40, rel=-110)
    m = draw_hip(ctx, MOMX, SEAT + 4, KMOM, -1, MOM, p)
    if mug_on:
        mug(ctx, m['back'][0] - 30, m['back'][1] - 30, 0.8, lf)
    return m


def living(ctx, f, lf, cx=620, cy=1210, z=1.05, shake=0, dad_p=None, kid_p=None, mom_p=None, g=1.0, wob=0.0, btn=True,
           frame_tilt=0.0, dog_sleep=True, empty=False):
    ctx.save(); cam(ctx, cx, cy, z, 0, shake, f)
    room(ctx, lf, frame_tilt)
    out = {}
    if not empty:
        out['dad'] = sofa_dad(ctx, lf, g, dad_p, wob, btn)
        fat_dog(ctx, DOGX, FLOOR + 140, 0.55, 1, lf, g, sleep=dog_sleep)
        out['kid'] = floor_kid(ctx, lf, g, kid_p)
    out['mom'] = chair_mom(ctx, lf, mom_p)
    return out


def groan(ctx, d, lf):
    sweat(ctx, d['head'][0] - d['R'] * 1.0, d['head'][1] - d['R'] * 0.5, lf, 1.1)


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    o = living(ctx, f, lf, 610, 1130, 1.0 + 0.04 * eio(pop(lf, 0, 54)), 0, wob=math.sin(lf * 0.5))
    groan(ctx, o['dad'], lf)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"I can't... MOVE...\"", 540, 1460, 120, YEL, -0.04, t)


# ------------------------------------------------------------------ shot 2: stand attempt + button
def stand(ctx, f, il):
    # il 0..66: rock forward x3, fall back at 46 *BOING*
    if il < 46:
        r = abs(math.sin(il * math.pi / 15))
        tor = lerp(-22, 26, r)
        p = P(eye='glare', mouth='flat' if r < 0.6 else 'scream', torso=tor, head=-6, lhip=88 - 0.3 * tor, lkn=-88, rhip=82 - 0.3 * tor, rkn=-82,
              lsh=60 + 60 * r, lel=-10, rsh=50 + 60 * r, rel=-10)
        hipy = SEAT + 4 - 10 * r
        sh = 0
    else:
        bt = pop(il, 46, 58)
        p = P(eye='shock', mouth='open', torso=-34 + 12 * math.sin(bt * math.pi * 3) * (1 - bt), head=8, lhip=110, lkn=-60, rhip=100, rkn=-70,
              lsh=140, lel=-10, rsh=120, rel=-10)
        hipy = SEAT + 10 - 30 * math.sin(bt * math.pi * 2) * (1 - bt)
        sh = shake_at(il, [46], 8, 10)
    ctx.save(); cam(ctx, 420, 1180, 1.45, 0, sh, f)
    room(ctx, il)
    fat_dog(ctx, DOGX, FLOOR + 140, 0.55, 1, il, 1.0)
    floor_kid(ctx, il)
    d = sofa_dad(ctx, il, 1.0, p, math.sin(il * 0.9) * 2, x=DADX, hipy=hipy)
    if il < 46:
        groan(ctx, d, il)
    ctx.restore()
    if il < 46:
        label(ctx, "\"HNNNGH!!\"", 540, 1460, 140, ORANGE, -0.04, pop(il, 2, 5))
    else:
        label(ctx, "*BOING!*", 540, 460, 120, CYAN, 0.05, pop(il, 46, 49))
        label(ctx, "\"...nope.\"", 540, 1460, 130, WHITE, -0.03, pop(il, 52, 55))


def button(ctx, f, il):
    # il 0..80: 0-20 strain push-in on the belly, 20 PING!, ricochet off the frame (28) -> into Mom's tea (36) -> "...thanks."
    pan = eio(pop(il, 20, 34))
    z = lerp(2.0, 1.25, pan) if il >= 20 else 1.6 + 0.4 * eio(pop(il, 0, 20))
    cx = lerp(DADX + 120, 900, pan); cy = lerp(1150, 1020, pan)
    ctx.save(); cam(ctx, cx, cy, z, 0, shake_at(il, [20, 28], 8, 14), f)
    room(ctx, il, frame_tilt=0.28 * eout(pop(il, 28, 32)) + 0.06 * math.sin(il * 0.6) * (il >= 28))
    fat_dog(ctx, DOGX, FLOOR + 140, 0.55, 1, il, 1.0)
    floor_kid(ctx, il)
    p = P(eye='shock' if il >= 20 else 'glare', mouth='open' if il >= 20 else 'flat', **{k: v for k, v in SIT.items()})
    d = sofa_dad(ctx, il, 1.08 if il < 20 else 1.0, p, (il < 20) * 3 * math.sin(il * 2.2), btn=il < 20)
    sp = pop(il, 36, 48)
    m = chair_mom(ctx, il, P(eye='normal' if il < 40 else 'smug', mouth='flat', torso=-8, lhip=88, lkn=-88, rhip=82, rkn=-82, lsh=10, lel=-60, rsh=40, rel=-110))
    mx, my = m['back'][0] - 30 + 52 * 0.8, m['back'][1] - 30 - 40 * 0.8
    if il >= 20 and il < 36:                                      # flying button
        b0 = d['btn']
        if il < 28:
            t = (il - 20) / 8; bx = lerp(b0[0], FRAME[0], t); by = lerp(b0[1], FRAME[1] + 40, t) - 220 * math.sin(math.pi * t)
        else:
            t = (il - 28) / 8; bx = lerp(FRAME[0], mx, t); by = lerp(FRAME[1] + 40, my, t) - 160 * math.sin(math.pi * t)
        for j in range(3):
            ellipse(ctx, bx - (j + 1) * 22, by + (j + 1) * 6, 8 - 2 * j, 8 - 2 * j); setc(ctx, (1, 0.8, 0.2, 0.5)); ctx.fill()
        ctx.save(); ctx.translate(bx, by); ctx.rotate(il * 0.8)
        ellipse(ctx, 0, 0, 16, 16); fl(ctx, GOLD, 4)
        for dx in (-5, 5):
            ellipse(ctx, dx, 0, 2.5, 2.5); setc(ctx, INK); ctx.fill()
        ctx.restore()
    if 0 < sp < 1:                                                 # tea splash
        for j in range(6):
            a = -math.pi / 2 + (j - 2.5) * 0.35
            ellipse(ctx, mx + math.cos(a) * 70 * sp, my + math.sin(a) * 90 * sp + 120 * sp * sp, 10, 13); fl(ctx, hx('c98a4a'), 3)
    ctx.restore()
    if il < 20:
        label(ctx, "*creeeak...*", 540, 1460, 110, WHITE, -0.03, pop(il, 3, 6))
    elif il < 36:
        label(ctx, "*PING!*", 540, 460, 130, GOLD, 0.05, pop(il, 20, 23))
    else:
        label(ctx, "*PLOP!*", 540, 460, 120, CYAN, -0.05, pop(il, 36, 39))
        label(ctx, "\"...thanks.\"", 540, 1460, 130, PINK, -0.03, pop(il, 46, 49))


def s2(ctx, f):
    lf = f - 54
    if lf < 66:
        stand(ctx, f, lf)
    else:
        button(ctx, f, lf - 66)


# ------------------------------------------------------------------ shot 3: dishes -> instant sleep
def dishes_ask(ctx, f, il):
    # il 0..50: Mom stands by the table with the dish mountain, the family listens (eyes open)
    ctx.save(); cam(ctx, 1010, 1100, 0.92, 0, 0, f)
    room(ctx, il)
    table(ctx)
    dishes(ctx, 1640, TABLE - 6)
    sofa_dad(ctx, il, 1.0, P(eye='normal', mouth='flat', **SIT))
    fat_dog(ctx, DOGX, FLOOR + 140, 0.55, 1, il, 1.0, sleep=False)
    floor_kid(ctx, il, 1.0, P(eye='normal', mouth='flat', torso=-38, head=10, lhip=90, lkn=-6, rhip=86, rkn=-10, lsh=-40, lel=-10, rsh=-30, rel=-10))
    draw(ctx, 1190, FLOOR + 30 - 186 * KMOM, KMOM, -1, MOM, P(eye='happy', mouth='grin', lsh=150, lel=20, rsh=20, rel=-30))
    ctx.restore()
    label2(ctx, "\"Who wants to help", "with the DISHES?\"", WHITE, pop(il, 2, 6), 100, col2=CYAN, y=1440)


def fake_sleep(ctx, f, il):
    # il 0..90: everyone instantly "asleep" snoring; Mom twitches
    ctx.save(); cam(ctx, 740, 1120, 0.98 + 0.04 * eio(pop(il, 0, 90)), 0, shake_at(il, [0], 6, 8), f)
    room(ctx, il)
    table(ctx)
    dishes(ctx, 1640, TABLE - 6)
    snore_m = 'open' if (il // 10) % 2 == 0 else 'flat'
    d = sofa_dad(ctx, il, 1.0, P(eye='closed', mouth=snore_m, **dict(SIT, head=14)))
    fat_dog(ctx, DOGX, FLOOR + 140, 0.55, 1, il, 1.0)
    k = floor_kid(ctx, il, 1.0, P(eye='closed', mouth=snore_m, torso=-38, head=14, lhip=90, lkn=-6, rhip=86, rkn=-10, lsh=-40, lel=-10, rsh=-30, rel=-10))
    m = draw(ctx, 1190, FLOOR + 30 - 186 * KMOM, KMOM, -1, MOM, P(eye='glare' if il > 30 else 'shock', mouth='flat', lsh=40, lel=-120, rsh=40, rel=-120))
    if il > 30:
        twitch(ctx, m['head'][0] - m['R'] * 0.9, m['head'][1] - m['R'] * 0.8, il, 1.2)
    for (hx_, hy_, R), off in (((d['head'][0], d['head'][1], d['R']), 0), ((k['head'][0], k['head'][1], k['R']), 9), ((DOGX - 90, FLOOR - 40, 60), 17)):
        zzz(ctx, hx_ + R * 0.9, hy_ - R * 1.0, il + off, 1.0)
    ctx.restore()
    label(ctx, "*SNOOORE*", 540, 470, 110, CYAN, 0.04, pop(il, 1, 4))
    if il > 30:
        label(ctx, "\"...REALLY?!\"", 540, 1460, 140, RED, -0.04, pop(il, 32, 35))


def s3(ctx, f):
    lf = f - 200
    if lf < 50:
        dishes_ask(ctx, f, lf)
    else:
        fake_sleep(ctx, f, lf - 50)


# ------------------------------------------------------------------ shot 4: pie whisper -> PING -> ZOOM
def whisper(ctx, f, il):
    # il 0..40: Mom ECU (the one close-up), sly whisper, holds a pie
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eio(pop(il, 0, 40)), 0, 0, f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('ffb3cf')); ctx.fill()
    rays(ctx, 540, 900, 240, 1500, il * 0.02, col=(1, 1, 1), a=0.3, n=16)
    face(ctx, MOM, P(eye='smug', mouth='smile'), 470, 860, 200, -0.06)
    pie(ctx, 720, 1230, 1.25)
    for j in range(3):
        ctx.move_to(660 + j * 50, 1150 - 20 * j); ctx.curve_to(640 + j * 50, 1100 - 20 * j, 690 + j * 50, 1060 - 20 * j, 665 + j * 50, 1010 - 20 * j - 6 * math.sin(il * 0.3 + j))
        setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()
    label2(ctx, "\"...who wants", "PIE?\"", WHITE, pop(il, 2, 6), 120, col2=PINK, y=1440)


def ping(ctx, f, il):
    # il 0..30: eyes PING open in the wide shot
    o = living(ctx, f, il, 610, 1130, 1.06, shake_at(il, [0], 8, 10), dog_sleep=False,
               dad_p=P(eye='shock', mouth='open', **dict(SIT, torso=-10)),
               kid_p=P(eye='shock', mouth='open', torso=-20, head=0, lhip=90, lkn=-6, rhip=86, rkn=-10, lsh=-40, lel=-10, rsh=-30, rel=-10))
    for c in (o['dad'], o['kid']):
        for j in range(2):
            sparkle(ctx, c['head'][0] + (j * 2 - 1) * c['R'] * 1.15, c['head'][1] - c['R'] * 0.9, 22 + 8 * math.sin(il * 0.8 + j), YEL)
    sparkle(ctx, DOGX + 40, FLOOR - 120, 22 + 8 * math.sin(il * 0.8), YEL)
    ctx.restore()
    label(ctx, "*PING!*", 540, 470, 140, GOLD, 0.05, pop(il, 0, 3))


SEATS = [(1470, KDAD, DAD, 1), (1790, KKID, KID, -1)]


def table_scene(ctx, f, il, cx, cy, z, eaters=True, dust=0.0, mom_mode=None, pie_state=None, dog_on_chair=True, shake=0, eye='happy', mouth='grin'):
    ctx.save(); cam(ctx, cx, cy, z, 0, shake, f)
    room(ctx, il)
    chair(ctx, 1470, 1); chair(ctx, 1790, -1)
    chair(ctx, 2060, -1)
    out = {}
    if eaters:
        db = tummy_char(ctx, 1470, TABLE + 66, KDAD, 1, DAD, P(eye=eye, mouth=mouth, torso=6, lhip=88, lkn=-88, rhip=82, rkn=-82, lsh=150, lel=10, rsh=40, rel=-40), 1.0, False)
        kb = tummy_char(ctx, 1790, TABLE + 66, KKID, -1, KID, P(eye=eye, mouth=mouth, torso=6, lhip=88, lkn=-88, rhip=82, rkn=-82, lsh=150, lel=10, rsh=40, rel=-40), 1.0, False)
        for b in (db, kb):
            fork(ctx, b['front'][0], b['front'][1] - 10, 0.15 * math.sin(il * 0.9), 1.4)
        out['dad'], out['kid'] = db, kb
        if dog_on_chair:
            fat_dog(ctx, 2080, TABLE + 80, 0.5, -1, il, 1.0, sleep=False)
    table(ctx)
    if pie_state is not None:
        pie(ctx, 1630, TABLE - 20, 1.0, pie_state)
    if dust > 0:
        for i, sx in enumerate((1470, 1790, 2080)):
            for j in range(4):
                ellipse(ctx, sx - 50 + j * 34 + 6 * math.sin(i + j), TABLE - 60 - 30 * (j % 2), 50 * dust + 14, 40 * dust + 12); fl(ctx, (0.88, 0.86, 0.9), 4)
            for j in range(3):
                ctx.move_to(sx - 80, TABLE - 120 + j * 40); ctx.line_to(sx - 80 - 260 * dust, TABLE - 140 + j * 40)
            ink(ctx, 6); ctx.stroke()
    ctx.restore()
    return out


def zoom(ctx, f, il):
    # il 0..70: whip-pan to the table: everyone already seated, forks up "ME!!"
    tt = eio(pop(il, 0, 10))
    cx = lerp(640, 1760, tt)
    table_scene(ctx, f, il, cx, 1170, 1.05, dust=max(0, 1 - il / 18) if il < 18 else 0, shake=shake_at(il, [8], 8, 12))
    if il < 10:
        for j in range(8):                                        # whoosh lines
            yy = 500 + j * 130
            ctx.move_to(0, yy); ctx.line_to(1080, yy + 20); setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(14); ctx.stroke()
    label(ctx, "*ZOOOM!*", 540, 470, 120, CYAN, -0.05, pop(il, 0, 3))
    label(ctx, "\"ME!! ME!! ME!!\"", 540, 1460, 130, YEL, 0.03, pop(il, 12, 15))


def s4(ctx, f):
    lf = f - 340
    if lf < 40:
        whisper(ctx, f, lf)
    elif lf < 70:
        ping(ctx, f, lf - 40)
    else:
        zoom(ctx, f, lf - 70)


# ------------------------------------------------------------------ shot 5: twist + salad + loop
def empty_pie(ctx, f, il):
    # il 0..80: Mom brings the pie dish... EMPTY. tilt down: round dog under the table with pie face *BURP*
    tilt = eio(pop(il, 34, 46))
    table_scene(ctx, f, il, 1700, lerp(1150, 1420, tilt), lerp(1.05, 1.3, tilt), dog_on_chair=False, pie_state=1.0, eye='shock' if il >= 8 else 'happy', mouth='scream' if il >= 8 else 'grin')
    ctx.save(); cam(ctx, 1700, lerp(1150, 1420, tilt), lerp(1.05, 1.3, tilt), 0, shake_at(il, [50], 8, 10), f)
    fat_dog(ctx, 1640, FLOOR + 150, 0.62, 1, il, 1.3 + 0.08 * math.sin(il * 0.4), sleep=il < 50, pie_face=True)
    ctx.restore()
    card(ctx, 'p2', il, 0)
    if il < 34:
        label(ctx, "\"...wait. WHERE'S THE PIE?\"", 540, 1460, 100, WHITE, -0.03, pop(il, 8, 11))
    if il >= 50:
        label(ctx, "*BUUURP!*", 540, 1460, 140, ORANGE, -0.05, pop(il, 50, 53))


def salad_time(ctx, f, il):
    # il 0..60: 0-30 Mom offers SALAD to the family at the table; 30 *ZOOM*: chairs empty + dust; pan back to the sofa
    if il < 30:
        table_scene(ctx, f, il, 1800, 1150, 1.0, dog_on_chair=True, pie_state=None, eye='shock', mouth='open')
        ctx.save(); cam(ctx, 1800, 1150, 1.0, 0, 0, f)
        m = draw(ctx, 2230, FLOOR + 30 - 186 * KMOM, KMOM, -1, MOM, P(eye='smug', mouth='grin', lsh=100, lel=-40, rsh=90, rel=-50))
        salad(ctx, m['front'][0] - 40, m['front'][1] - 20, 1.0)
        ctx.restore()
        label2(ctx, "\"Okay... who wants", "SALAD?\"", WHITE, pop(il, 2, 6), 104, col2=GREEN, y=1440)
    else:
        jl = il - 30
        table_scene(ctx, f, il, 1800, 1150, 1.0, eaters=False, dust=max(0.2, 1 - jl / 30))
        label(ctx, "*ZOOOM!*", 540, 470, 120, CYAN, -0.05, pop(jl, 0, 3))
        label(ctx, "\"...SERIOUSLY?\"", 540, 1460, 130, PINK, -0.03, pop(jl, 8, 11))


def s5(ctx, f):
    lf = f - 480
    if lf < 80:
        empty_pie(ctx, f, lf)
    elif lf < 140:
        salad_time(ctx, f, lf - 80)
    else:
        s1(ctx, f, f - 620)


SHOTS = [(0, s1), (54, s2), (200, s3), (340, s4), (480, s5)]
CUTS = (54, 120, 200, 250, 340, 380, 410, 480, 560, 590, 620)


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
                              "-i", "out/room_for_dessert_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
