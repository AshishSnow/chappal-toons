"""'DAD'S FIRST TIME ICE SKATING'. Original, general-audience comedy short, 22s.
Hook:   evening outdoor rink, medium shot: Dad in a red sweater + beanie clinging to the rink boards with both arms,
        legs wobbling on skates, forced grin, sweat "I'M A NATURAL!!" + caption "DAD'S FIRST TIME ICE SKATING:".
Beat 1: kid glides in *SKSHH* "Just LET GO, Dad!" -> "...okay." -> lets go -> slow splits + windmill arms
        "WHOA WHOA WHOA!!" -> *SPLAT!* flat on the ice, stars circling "...a NATURAL."
Beat 2: Dutch-tilt wide: Dad inching along with a cute penguin skating helper "It's for... BALANCE." while kids
        *ZOOM!* past and a tiny kid spins *twirl* -> a little girl taps him "Mister? That's MINE." -> "...sorry."
Beat 3: the one close-up: determined sweaty Dad "ONE... MORE..." "...TRY!!"
Twist:  he GLIDES! arms out, sparkles "I'M FLYING!!" kid "You're DOING it!!" -> PLOT TWIST: HE CAN'T STOP. ->
        "HOW DO I STOP?!" -> *BONK!* end board -> flips into the snowbank *FLOOMP!* only skates sticking out ->
        kid "Lesson TWO..." "...STOPPING." -> Dad pops out "...still a NATURAL." -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r
from scenes58 import sweat, twitch
from scenes84 import eio
import scenes13
from scenes13 import card as _card13

RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
ICE = hx('cdefff'); ICE2 = hx('a8ddff'); SNOW = hx('f6fbff'); SNOWSH = hx('cfe3ff')
DAD = dict(doodle.DAD, shirt=hx('ff4d5e'), pants=hx('3a4a8a'), shoes=hx('fbfbf6'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('3fd6a0'), pants=hx('3d7bff'), shoes=hx('fbfbf6'))
GIRL = dict(doodle.BOY, hood=False, shades=False, hair=hx('8a4a2a'), shirt=hx('ff5fa8'), pants=hx('8a3cff'), shoes=hx('fbfbf6'))
Z1 = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ffc93c'), pants=hx('2a3a6a'), shoes=hx('fbfbf6'))
Z2 = dict(doodle.BOY, hood=False, shades=False, hair=hx('c07a3a'), shirt=hx('8a3cff'), pants=hx('3d7bff'), shoes=hx('fbfbf6'))
N = 660
GND = 1640           # where skaters stand on the ice
RAIL = 1390          # top of the rink boards
BBOT = 1515          # bottom of the boards (back edge of the ice)
ENDX = 2250          # end of the rink, snowbank beyond
PILEX = 2540
KDAD, KKID = 1.0, 0.82
DADX = 1100
CX, CY, CZ = 1180, 1390, 1.3

CAPS = {'p1': [[("DAD'S ", OUT), ("FIRST TIME", RED)], [("ICE SKATING:", BLUE)]],
        'p2': [[("PLOT TWIST:", RED)], [("HE ", OUT), ("CAN'T STOP.", BLUE)]]}
scenes13.CAPS = CAPS
card = _card13


def stand_ch(ctx, ch, x, k, p, f_=1, feet=GND, blades=True, hat=False):
    d = draw(ctx, x, feet - 186 * k, k, f_, ch, p)
    if blades:
        skates(ctx, x, feet, k, f_, p)
    if hat:
        beanie(ctx, d['head'][0], d['head'][1], d['R'], math.radians(p['rot'] + p['torso'] + p.get('head', 0)) * f_)
    return d


def skates(ctx, x, feet, k, f, p):
    S = k * 1.35
    ctx.save(); ctx.translate(x, feet - 68 * S); ctx.rotate(math.radians(p['rot']) * f)
    for side, a1, a2 in ((-1, p['lhip'], p['lkn']), (1, p['rhip'], p['rkn'])):
        r1, r2 = math.radians(a1), math.radians(a1 + a2)
        fx = side * 24 * S + f * math.sin(r1) * 34 * S + f * math.sin(r2) * 34 * S
        fy = -6 * S + math.cos(r1) * 34 * S + math.cos(r2) * 34 * S
        cx_ = fx + f * 12 * S
        for sx in (-14, 16):
            ctx.rectangle(cx_ + sx * S - 3 * S, fy + 14 * S, 6 * S, 10 * S); fl(ctx, hx('9aa6b8'), 2)
        rect_r(ctx, cx_ - 30 * S, fy + 22 * S, 62 * S, 7 * S, 3 * S); fl(ctx, hx('e8eef6'), 2.6)
        ctx.new_path(); ctx.move_to(cx_ + f * 32 * S, fy + 25 * S); ctx.curve_to(cx_ + f * 38 * S, fy + 25 * S, cx_ + f * 38 * S, fy + 16 * S, cx_ + f * 32 * S, fy + 14 * S)
        ink(ctx, 2.6); ctx.stroke()
    ctx.restore()


def beanie(ctx, hx_, hy_, R, ang):
    ctx.save(); ctx.translate(hx_, hy_); ctx.rotate(ang)
    ctx.new_path(); ctx.arc(0, -R * 0.22, R * 0.98, math.pi * 1.04, math.pi * 1.96); ctx.close_path(); fl(ctx, hx('3fa0ff'), 4)
    for k in range(-3, 4):
        ctx.move_to(k * R * 0.22, -R * 0.4); ctx.line_to(k * R * 0.17, -R * 0.95 + abs(k) * R * 0.09)
    setc(ctx, (1, 1, 1, 0.45)); ctx.set_line_width(R * 0.05); ctx.stroke()
    rect_r(ctx, -R * 1.02, -R * 0.42, R * 2.04, R * 0.3, R * 0.12); fl(ctx, WHITE, 4)
    ellipse(ctx, 0, -R * 1.22, R * 0.24, R * 0.24); fl(ctx, YEL, 4)
    ctx.restore()


def ghost(ctx, a, fn):
    ctx.push_group(); fn(); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)


# ------------------------------------------------------------------ set: evening outdoor rink
def pine(ctx, x, y, s):
    rect_r(ctx, x - 16 * s, y - 40 * s, 32 * s, 60 * s, 6 * s); fl(ctx, hx('8a5a3a'), 4)
    for j, (w, h) in enumerate(((150, 120), (120, 110), (86, 100))):
        yy = y - 30 * s - j * 85 * s
        poly(ctx, [(x - w * s, yy), (x, yy - h * s * 1.4), (x + w * s, yy)]); fl(ctx, hx('1f9a6a'), 4)
        ctx.new_path(); ctx.move_to(x - w * s * 0.55, yy - h * s * 0.62)
        ctx.curve_to(x - w * s * 0.2, yy - h * s * 0.85, x + w * s * 0.2, yy - h * s * 0.85, x + w * s * 0.55, yy - h * s * 0.62)
        ctx.line_to(x, yy - h * s * 1.4); ctx.close_path(); fl(ctx, SNOW, 3)


def snowman(ctx, x, y, lf):
    ellipse(ctx, x, y - 70, 85, 72); fl(ctx, SNOW, 5)
    ellipse(ctx, x, y - 185, 62, 56); fl(ctx, SNOW, 5)
    ellipse(ctx, x, y - 280, 46, 44); fl(ctx, SNOW, 5)
    for sx in (-1, 1):
        ellipse(ctx, x + sx * 16, y - 288, 6, 7); setc(ctx, INK); ctx.fill()
        ellipse(ctx, x + sx * 28, y - 270, 9, 5); setc(ctx, hx('ff9aa8')); ctx.fill()
    poly(ctx, [(x - 4, y - 278), (x + 40, y - 270), (x - 2, y - 266)]); fl(ctx, ORANGE, 3)
    ctx.new_path(); ctx.arc(x, y - 262, 14, 0.4, math.pi - 0.4); ink(ctx, 4); ctx.stroke()
    rect_r(ctx, x - 52, y - 238, 104, 24, 10); fl(ctx, RED, 4)
    rect_r(ctx, x + 18, y - 230, 24, 70, 8); fl(ctx, RED, 4)
    for k in range(3):
        ellipse(ctx, x, y - 200 + k * 30, 7, 7); setc(ctx, INK); ctx.fill()
    ctx.save(); ctx.translate(x - 60, y - 190); ctx.rotate(-0.6 + 0.15 * math.sin(lf * 0.2))
    ctx.move_to(0, 0); ctx.line_to(-80, 0); ctx.move_to(-55, 0); ctx.line_to(-75, -20); setc(ctx, hx('8a5a3a')); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()


def cocoa_hut(ctx, x, y, lf):
    rect_r(ctx, x - 150, y - 260, 300, 260, 10); fl(ctx, hx('c98a52'), 6)
    for k in range(1, 6):
        ctx.move_to(x - 150, y - 260 + k * 43); ctx.line_to(x + 150, y - 260 + k * 43); setc(ctx, (0.55, 0.32, 0.18, 0.5)); ctx.set_line_width(4); ctx.stroke()
    poly(ctx, [(x - 190, y - 250), (x, y - 380), (x + 190, y - 250)]); fl(ctx, RED, 6)
    ctx.new_path(); ctx.move_to(x - 190, y - 250); ctx.curve_to(x - 100, y - 320, x + 100, y - 320, x + 190, y - 250)
    ctx.line_to(x, y - 380); ctx.close_path(); fl(ctx, SNOW, 4)
    rect_r(ctx, x - 100, y - 190, 200, 90, 10); fl(ctx, hx('ffe6a0'), 5)
    rect_r(ctx, x - 120, y - 110, 240, 24, 6); fl(ctx, hx('e0a35a'), 4)
    # mug on the counter + steam
    rect_r(ctx, x + 40, y - 150, 44, 42, 8); fl(ctx, WHITE, 3)
    ctx.new_path(); ctx.arc(x + 88, y - 130, 12, -1.4, 1.4); ink(ctx, 4); ctx.stroke()
    for k in range(2):
        ctx.new_path(); ctx.move_to(x + 52 + k * 18, y - 160)
        ctx.curve_to(x + 40 + k * 18 + 10 * math.sin(lf * 0.2), y - 190, x + 66 + k * 18, y - 205, x + 52 + k * 18, y - 230)
        setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(6); ctx.stroke()
    rect_r(ctx, x - 110, y - 240, 220, 46, 10); fl(ctx, WHITE, 4)
    text(ctx, "HOT COCOA", x, y - 216, 30, hx('8a4a2a'), ow=3, shadow=False)


def lights(ctx, x0, x1, y, sag, lf):
    ctx.new_path(); pts = []
    for i in range(41):
        u = i / 40; xx = lerp(x0, x1, u); yy = y + sag * math.sin(math.pi * ((u * 4) % 1))
        pts.append((xx, yy))
    ctx.move_to(*pts[0])
    for q in pts[1:]:
        ctx.line_to(*q)
    ink(ctx, 4); ctx.stroke()
    cols = (RED, YEL, MINT, PINK, BLUE, ORANGE)
    for i, (xx, yy) in enumerate(pts[1:-1:2]):
        on = (i + lf // 8) % 3 != 0
        c = cols[i % 6]
        if on:
            ellipse(ctx, xx, yy + 16, 22, 22); setc(ctx, c[:3] + (0.3,)); ctx.fill()
        ellipse(ctx, xx, yy + 14, 9, 13); fl(ctx, c if on else dark(c, 0.6), 2)


def rink(ctx, lf):
    ctx.set_source(vgrad(ctx, 0, 400, 0, 1400, [(0, hx('3b3a9e')), (0.6, hx('7a6ad6')), (1, hx('c9a8f0'))]))
    ctx.rectangle(-3000, -3000, 9000, 9000); ctx.fill()
    rnd = random.Random(3)
    for k in range(70):
        sx, sy = rnd.uniform(-600, 3000), rnd.uniform(380, 1150)
        tw = 0.5 + 0.5 * math.sin(lf * 0.2 + k)
        sparkle(ctx, sx, sy, 5 + 5 * tw, hx('fff6c0'))
    # moon
    ellipse(ctx, 1720, 760, 80, 80); fl(ctx, hx('fff3c0'), 5)
    ellipse(ctx, 1695, 740, 14, 12); setc(ctx, hx('f0dea0')); ctx.fill()
    ellipse(ctx, 1745, 790, 10, 9); setc(ctx, hx('f0dea0')); ctx.fill()
    # snowy hills
    for (hx_, hy_, r, c) in ((200, 1420, 700, hx('e6f0ff')), (1300, 1440, 800, hx('f2f7ff')), (2500, 1420, 700, hx('e6f0ff'))):
        ellipse(ctx, hx_, hy_, r, 220); fl(ctx, c, 5)
    for x, s in ((-150, 0.9), (60, 1.1), (900, 0.8), (1420, 1.0), (2050, 1.15), (2350, 0.85), (2750, 1.0)):
        pine(ctx, x, 1330, s)
    cocoa_hut(ctx, 560, 1340, lf)
    snowman(ctx, 1760, 1350, lf)
    lights(ctx, -500, 3000, 980, 60, lf)
    # back boards
    ctx.rectangle(-3000, RAIL, ENDX + 3000, BBOT - RAIL); fl(ctx, WHITE, 6)
    ctx.rectangle(-3000, RAIL + 70, ENDX + 3000, 16); setc(ctx, hx('3fa0ff')); ctx.fill()
    ctx.rectangle(-3000, BBOT - 26, ENDX + 3000, 26); setc(ctx, hx('ff4d5e')); ctx.fill()
    for k in range(-10, 20):
        xx = k * 260
        if xx < ENDX - 20:
            ctx.move_to(xx, RAIL); ctx.line_to(xx, BBOT); setc(ctx, (0.6, 0.7, 0.85, 0.7)); ctx.set_line_width(4); ctx.stroke()
    rect_r(ctx, -3000, RAIL - 16, ENDX + 3000 + 16, 24, 10); fl(ctx, hx('ffc93c'), 5)
    # little decorations on the boards
    for k, xx in enumerate((300, 1000, 1640)):
        ellipse(ctx, xx, RAIL + 30, 22, 22); fl(ctx, (RED, MINT, PINK)[k], 3)
        ctx.move_to(xx - 10, RAIL + 10); ctx.line_to(xx + 10, RAIL + 50); ink(ctx, 3); ctx.stroke()
    # ice
    ctx.set_source(vgrad(ctx, 0, BBOT, 0, 2300, [(0, ICE2), (1, ICE)]))
    ctx.rectangle(-3000, BBOT, ENDX + 3000, 3000); ctx.fill()
    ctx.move_to(-3000, BBOT); ctx.line_to(ENDX, BBOT); ink(ctx, 5); ctx.stroke()
    rnd = random.Random(11)
    for k in range(40):
        x0, y0 = rnd.uniform(-600, ENDX - 200), rnd.uniform(BBOT + 40, 2200)
        ctx.new_path(); ctx.move_to(x0, y0); ctx.curve_to(x0 + 60, y0 - 16, x0 + 140, y0 - 10, x0 + 200, y0 + 12)
        setc(ctx, (1, 1, 1, 0.75)); ctx.set_line_width(3); ctx.stroke()
    for k in range(6):
        x0 = -400 + k * 520
        poly(ctx, [(x0, BBOT + 40), (x0 + 60, BBOT + 40), (x0 - 40, 2200), (x0 - 140, 2200)]); setc(ctx, (1, 1, 1, 0.22)); ctx.fill()
    # snowy ground beyond the end of the rink + end board
    ctx.rectangle(ENDX, BBOT - 120, 3000, 3000); setc(ctx, SNOW); ctx.fill()
    ctx.move_to(ENDX, BBOT - 120); ctx.line_to(ENDX + 3000, BBOT - 120); ink(ctx, 5); ctx.stroke()
    snowpile(ctx, 0)
    side_board(ctx)
    falling_snow(ctx, lf)


def side_board(ctx):
    b0, b1 = (ENDX, BBOT), (ENDX + 160, 2300)
    poly(ctx, [b0, b1, (b1[0], b1[1] - 150), (b0[0], b0[1] - 125)]); fl(ctx, WHITE, 6)
    poly(ctx, [(b0[0], b0[1] - 22), (b1[0], b1[1] - 26), (b1[0], b1[1]), b0]); setc(ctx, hx('ff4d5e')); ctx.fill()
    poly(ctx, [(b0[0], b0[1] - 60), (b1[0], b1[1] - 70), (b1[0], b1[1] - 86), (b0[0], b0[1] - 74)]); setc(ctx, hx('3fa0ff')); ctx.fill()
    ctx.new_path(); ctx.move_to(b0[0], b0[1] - 133); ctx.line_to(b1[0], b1[1] - 160); setc(ctx, INK); ctx.set_line_width(22); ctx.stroke()
    ctx.new_path(); ctx.move_to(b0[0], b0[1] - 133); ctx.line_to(b1[0], b1[1] - 160); setc(ctx, hx('ffc93c')); ctx.set_line_width(14); ctx.stroke()


def snowpile(ctx, bump, front=False):
    cx = PILEX; top = GND - 200 - bump * 30
    ctx.new_path(); ctx.move_to(cx - 380, 2400); ctx.line_to(cx - 330, GND + 40)
    ctx.curve_to(cx - 280, GND - 140, cx - 140, top - 10, cx, top)
    ctx.curve_to(cx + 140, top - 10, cx + 280, GND - 140, cx + 330, GND + 40); ctx.line_to(cx + 380, 2400)
    ctx.close_path(); fl(ctx, SNOW, 6)
    ctx.save(); ctx.append_path(ctx.copy_path()) if False else None
    ctx.new_path(); ctx.move_to(cx - 330, GND + 40); ctx.curve_to(cx - 280, GND - 140, cx - 140, top - 10, cx, top)
    ctx.curve_to(cx - 200, top + 60, cx - 290, GND - 40, cx - 300, 2400); ctx.line_to(cx - 380, 2400); ctx.close_path()
    setc(ctx, SNOWSH[:3] + (0.7,)); ctx.fill(); ctx.restore()
    for k in range(6):
        sparkle(ctx, cx - 200 + k * 80, top + 60 + 90 * (k % 3), 10, WHITE)
    for dx, dy, r in ((-170, -100, 50), (150, -110, 44), (0, 20, 70), (-60, -150, 34)):
        ellipse(ctx, cx + dx, GND + dy, r, r * 0.55); setc(ctx, SNOWSH[:3] + (0.6,)); ctx.fill()


def falling_snow(ctx, lf):
    rnd = random.Random(21)
    for k in range(120):
        x0, y0, sp, r = rnd.uniform(-600, 3000), rnd.uniform(0, 1700), rnd.uniform(1.5, 3.5), rnd.uniform(5, 11)
        y = 350 + (y0 + lf * sp) % 1800
        x = x0 + 25 * math.sin(lf * 0.05 + k)
        ellipse(ctx, x, y, r, r); setc(ctx, (1, 1, 1, 0.85)); ctx.fill()


def penguin(ctx, x, y, s=1.0, lf=0):
    """cute plastic penguin skating helper, (x, y) = bottom centre"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for sx in (-1, 1):
        ellipse(ctx, sx * 40, -10, 34, 14); fl(ctx, ORANGE, 3)
    ellipse(ctx, 0, -130, 90, 125); fl(ctx, hx('2a3a6a'), 5)
    ellipse(ctx, 0, -110, 62, 95); fl(ctx, WHITE, 3)
    ellipse(ctx, 0, -250, 62, 56); fl(ctx, hx('2a3a6a'), 5)
    for sx in (-1, 1):
        ellipse(ctx, sx * 22, -258, 15, 17); fl(ctx, WHITE, 2)
        ellipse(ctx, sx * 22, -255, 7, 9); setc(ctx, INK); ctx.fill()
        ellipse(ctx, sx * 20, -260, 3, 3); setc(ctx, WHITE); ctx.fill()
        ellipse(ctx, sx * 38, -232, 10, 6); setc(ctx, hx('ff9aa8')); ctx.fill()
    poly(ctx, [(-14, -238), (14, -238), (0, -220)]); fl(ctx, ORANGE, 3)
    # handle
    ctx.new_path(); ctx.move_to(-70, -170); ctx.line_to(-70, -300); ctx.line_to(70, -300); ctx.line_to(70, -170)
    ink(ctx, 22); ctx.stroke()
    ctx.new_path(); ctx.move_to(-70, -170); ctx.line_to(-70, -300); ctx.line_to(70, -300); ctx.line_to(70, -170)
    setc(ctx, hx('ffc93c')); ctx.set_line_width(13); ctx.stroke()
    ctx.restore()


def stars_ring(ctx, x, y, lf, r=90):
    for k in range(5):
        a = lf * 0.25 + k * 1.256
        sparkle(ctx, x + r * math.cos(a), y + 0.35 * r * math.sin(a), 20, YEL)


def speed_lines(ctx, x, y, fd, n=6, col=(1, 1, 1, 0.85)):
    for k in range(n):
        ctx.move_to(x - fd * (90 + k * 20), y - 200 + k * 50); ctx.line_to(x - fd * (300 + k * 40), y - 200 + k * 50)
        setc(ctx, col); ctx.set_line_width(8); ctx.stroke()


def ice_spray(ctx, x, y, u):
    if not 0 < u < 1:
        return
    for k in range(10):
        a = math.pi + 0.25 + k * 0.12
        r = 40 + 140 * u
        ellipse(ctx, x + r * math.cos(a) * -1, y + r * math.sin(a) * 0.6, 10 * (1 - u) + 3, 10 * (1 - u) + 3); setc(ctx, (1, 1, 1, 1 - u)); ctx.fill()


# ------------------------------------------------------------------ poses
def cling_pose(lf, amt=1.0):
    w = math.sin(lf * 0.9)
    return P(eye='shock', mouth='grin', lsh=-95 * amt + 10 * w, lel=-10, rsh=95 * amt - 10 * w, rel=10,
             lhip=-22 + 12 * w, lkn=6, rhip=22 + 12 * w, rkn=-6, torso=3 * w, head=4 * math.sin(lf * 1.3))


def clinging_dad(ctx, lf, x=DADX):
    w = 5 * math.sin(lf * 1.7)
    d = stand_ch(ctx, DAD, x + w, KDAD, cling_pose(lf), 1, hat=True)
    sweat(ctx, d['head'][0] + d['R'] * 0.95, d['head'][1] - d['R'] * 0.4, lf, 1.0)
    return d


def glide_pose(lf, fd=-1):
    return P(eye='happy', mouth='grin', lsh=-70, lel=-10, rsh=70, rel=10, lhip=-6, rhip=40, rkn=-20, torso=8, head=-4)


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = CZ + 0.04 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, CX, CY, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    rink(ctx, lf)
    kx = 1460 + 70 * math.sin(lf * 0.06)
    stand_ch(ctx, KID, kx, KKID, glide_pose(lf), -1, GND - 30)
    clinging_dad(ctx, lf)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"I'M A", 540, 1385, 104, YEL, -0.04, t)
    label(ctx, "NATURAL!!\"", 540, 1480, 124, WHITE, -0.04, t)


# ------------------------------------------------------------------ shot 2: let go -> splits -> SPLAT
def beat1(ctx, f, il):
    # 0-40 kid glides in "Just LET GO, Dad!" ; 40-60 "...okay." lets go ; 60-95 splits + windmill ;
    # 95-102 falls ; 102 SPLAT ; 102-130 lying + stars ; "...a NATURAL."
    pin = eio(pop(il, 96, 106))
    ctx.save(); cam(ctx, lerp(1180, 1110, pin), lerp(1390, 1440, pin), lerp(1.3, 1.36, pin), 0, shake_at(il, [102], 12, 18), f)
    rink(ctx, il)
    # kid
    ku = eio(pop(il, 0, 26))
    kx = lerp(1900, 1420, ku)
    if il < 30:
        kp = glide_pose(il)
    elif il < 104:
        kp = P(eye='happy', mouth='open', lsh=-20, lel=-90, rsh=40, rel=-100, head=6)
    else:
        kp = P(eye='shock', mouth='open', lsh=150, lel=-20, rsh=-150, rel=20, head=-6)
    stand_ch(ctx, KID, kx, KKID, kp, -1, GND - 30)
    ice_spray(ctx, kx + 60, GND - 40, pop(il, 22, 36))
    # Dad
    if il < 40:
        clinging_dad(ctx, il)
    elif il < 60:
        u = eio(pop(il, 42, 56))
        p = cling_pose(il, 1 - u * 0.75); p['eye'] = 'closed' if il < 50 else 'shock'; p['mouth'] = 'wavy'
        d = stand_ch(ctx, DAD, DADX, KDAD, p, 1, hat=True)
        sweat(ctx, d['head'][0] + d['R'] * 0.95, d['head'][1] - d['R'] * 0.4, il, 1.0)
    elif il < 96:
        u = pop(il, 60, 94)
        sp = 20 + 55 * eio(u)
        dx = DADX + 80 * u
        drop = 68 * 1.35 * KDAD * (1 - math.cos(math.radians(sp)))
        wa = il * 0.55
        p = P(eye='shock', mouth='scream', lsh=math.degrees(wa) % 360 - 180, lel=-10, rsh=math.degrees(wa + 2.2) % 360 - 180, rel=10,
              lhip=-sp, lkn=0, rhip=sp, rkn=0, head=6 * math.sin(il * 1.4))
        stand_ch(ctx, DAD, dx, KDAD, p, 1, GND + drop, hat=True)
    else:
        u = eio(pop(il, 96, 102))
        dx = DADX + 80
        p = P(eye='shock' if il < 102 else 'closed', mouth='scream' if il < 102 else 'wavy', rot=-88 * u,
              lsh=150, lel=-10, rsh=-150, rel=10, lhip=-30 + 20 * u, rhip=30 - 10 * u, lkn=-10, rkn=10)
        d = stand_ch(ctx, DAD, dx, KDAD, p, 1, GND + 70 * u + 30, hat=True)
        if il >= 102:
            stars_ring(ctx, d['head'][0], d['head'][1] - d['R'] * 0.9, il)
        if 102 <= il < 112:
            v = pop(il, 102, 112)
            for k in range(10):
                a = k * 0.63
                ellipse(ctx, dx - 80 + 220 * math.cos(a) * v, GND + 60 + 60 * math.sin(a) * v, 14 * (1 - v) + 2, 14 * (1 - v) + 2)
                setc(ctx, (1, 1, 1, 1 - v)); ctx.fill()
    ctx.restore()
    if il < 40:
        label(ctx, "*SKSHHH!*", 540, 470, 90, CYAN, 0.04, pop(il, 20, 24))
        label(ctx, "\"Just LET GO, Dad!\"", 540, 1430, 100, MINT, -0.03, pop(il, 26, 30))
    elif il < 60:
        label(ctx, "\"...okay.\"", 540, 1430, 110, WHITE, 0.03, pop(il, 42, 46))
    elif il < 102:
        label(ctx, "\"WHOA WHOA", 540, 1385, 104, YEL, -0.04, pop(il, 64, 68))
        label(ctx, "WHOA!!\"", 540, 1480, 120, YEL, 0.04, pop(il, 74, 78))
    else:
        label(ctx, "*SPLAT!*", 540, 470, 140, RED, -0.05, pop(il, 102, 105))
        if il >= 112:
            label(ctx, "\"...a NATURAL.\"", 540, 1430, 110, WHITE, -0.03, pop(il, 112, 116))


def s2(ctx, f):
    beat1(ctx, f, f - 60)


# ------------------------------------------------------------------ shot 3: penguin helper (Dutch tilt)
def zoomer(ctx, ch, x, fd, k, lf, feet):
    stand_ch(ctx, ch, x, k, P(eye='happy', mouth='grin', lsh=-60, lel=-20, rsh=60, rel=20, lhip=-8, rhip=40, rkn=-20, torso=14), fd, feet)
    speed_lines(ctx, x, feet - 80, fd, 5)


def penguin_beat(ctx, f, il):
    # 0-80 Dad inches with the penguin ; zoomers at 18-36 and 42-58 ; tiny spinner 56-80 ;
    # 80-104 girl skates in "Mister? That's MINE." ; 104-120 "...sorry." she takes it away
    ctx.save(); cam(ctx, 1150, 1400, 1.08, -6, shake_at(il, [20, 44], 6, 6), f)
    rink(ctx, il)
    # tiny spinner (background)
    if 52 <= il < 120:
        a = il * 0.9
        fd = 1 if math.cos(a) > 0 else -1
        stand_ch(ctx, Z2, 1700, 0.62, P(eye='happy', mouth='smile', lsh=170, lel=0, rsh=-170, rel=0, lhip=0, rhip=-2), fd, GND - 60)
        for k in range(3):
            ctx.new_path(); ctx.arc(1700, GND - 260 + k * 60, 70 + k * 10, a + k, a + k + 2.2); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(6); ctx.stroke()
    # Dad + penguin
    u = clamp(il / 104)
    px = lerp(1010, 1240, u) + (0 if il < 104 else 0)
    w = math.sin(il * 1.1)
    has_pen = il < 106
    dx = px - 215
    if il < 80:
        dp = P(eye='shock', mouth='grin', lsh=70, lel=-10, rsh=75, rel=-10, torso=18, head=-14,
               lhip=-12 + 10 * w, rhip=14 - 10 * w, lkn=4, rkn=-4)
    elif il < 104:
        dp = P(eye='shock', mouth='open', lsh=70, lel=-10, rsh=75, rel=-10, torso=10, head=-6, lhip=-12, rhip=14)
    else:
        dp = P(eye='closed', mouth='wavy', lsh=10, lel=-20, rsh=60, rel=-60, torso=0, head=-12, lhip=-12, rhip=14)
    d = stand_ch(ctx, DAD, dx, KDAD, dp, 1, hat=True)
    if il < 80:
        sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.5, il, 1.0)
    # girl
    if il >= 78:
        gu = eio(pop(il, 78, 92))
        if il < 106:
            gx = lerp(400, px + 150, gu)
            gp = P(eye='glare' if il >= 92 else 'normal', mouth='frown' if il >= 92 else 'smile', lsh=-10, lel=-20,
                   rsh=-120 if 92 <= il < 102 else -10, rel=-30, head=4)
            gfd = -1 if il >= 92 else 1
            if il < 92:
                gx = lerp(400, px - 330, gu)
                gfd = 1
            else:
                gx = px + 160
        else:
            v = eio(pop(il, 106, 120))
            gx = lerp(px + 160, 1900, v)
            gp = P(eye='happy', mouth='grin', lsh=-60, lel=-80, rsh=-60, rel=-80, torso=10)
            gfd = 1
        if has_pen:
            penguin(ctx, px, GND - 8, 0.74, il)
            g = stand_ch(ctx, GIRL, gx, 0.6, gp, gfd, GND - 10)
        else:
            g = stand_ch(ctx, GIRL, gx, 0.6, gp, gfd, GND - 10)
            penguin(ctx, gx + 120, GND - 8, 0.75, il)
    else:
        penguin(ctx, px, GND - 8, 0.74, il)
    # zoomers
    for (t0, ch, fd, x0, x1, feet) in ((18, Z1, 1, 300, 2300, GND + 60), (42, KID, -1, 2300, 300, GND - 40)):
        if t0 <= il < t0 + 18:
            v = (il - t0) / 18
            zoomer(ctx, ch, lerp(x0, x1, v), fd, 0.78, il, feet)
    ctx.restore()
    if il < 18:
        label(ctx, "\"It's for...", 540, 1385, 96, WHITE, -0.03, pop(il, 2, 6))
        label(ctx, "BALANCE.\"", 540, 1480, 116, CYAN, 0.03, pop(il, 8, 12))
    elif il < 52:
        label(ctx, "*ZOOM!*", 540, 470, 120, YEL, -0.05, pop(il, 18, 21))
        if il >= 42:
            label(ctx, "*ZOOM!*", 540, 650, 110, MINT, 0.05, pop(il, 42, 45))
        label(ctx, "\"...BALANCE.\"", 540, 1430, 100, CYAN, 0.03, 1)
    elif il < 80:
        label(ctx, "*twirl twirl*", 540, 470, 90, PINK, 0.04, pop(il, 54, 58))
        label(ctx, "\"...show-off.\"", 540, 1430, 100, WHITE, -0.03, pop(il, 60, 64))
    elif il < 104:
        label(ctx, "*tap tap*", 540, 470, 80, WHITE, 0.04, pop(il, 90, 93))
        label(ctx, "\"Mister?", 540, 1385, 100, PINK, -0.03, pop(il, 92, 95))
        label(ctx, "That's MINE.\"", 540, 1480, 110, PINK, 0.03, pop(il, 96, 99))
    else:
        label(ctx, "\"...sorry.\"", 540, 1430, 110, WHITE, -0.03, pop(il, 105, 108))


def s3(ctx, f):
    penguin_beat(ctx, f, f - 190)


# ------------------------------------------------------------------ shot 4: the one close-up
def closeup(ctx, f, il):
    z = 1.62 + 0.12 * eio(il / 90)
    ctx.save(); cam(ctx, DADX + 10, 1250, z, 2 * math.sin(il * 0.2), shake_at(il, [30], 10, 16) + 2, f)
    rink(ctx, il)
    w = math.sin(il * 1.2)
    p = P(eye='glare', mouth='flat' if il < 30 else 'scream', lsh=-30, lel=-110, rsh=30, rel=110,
          lhip=-18 + 8 * w, rhip=18 + 8 * w, head=3 * w)
    d = stand_ch(ctx, DAD, DADX + 4 * w, KDAD, p, 1, hat=True)
    sweat(ctx, d['head'][0] + d['R'] * 0.95, d['head'][1] - d['R'] * 0.4, il, 1.3)
    sweat(ctx, d['head'][0] - d['R'] * 1.0, d['head'][1] - d['R'] * 0.2, il + 40, 1.0)
    if il >= 30:
        twitch(ctx, d['head'][0] + d['R'] * 0.8, d['head'][1] - d['R'] * 1.1, il, 1.2)
    ctx.restore()
    label(ctx, "\"ONE... MORE...", 540, 1385, 104, WHITE, -0.03, pop(il, 4, 8))
    if il >= 30:
        label(ctx, "...TRY!!\"", 540, 1480, 140, RED, 0.04, pop(il, 30, 33))
    if il >= 62:
        label(ctx, "*deep breath*", 540, 470, 80, CYAN, 0.03, pop(il, 62, 66))


def s4(ctx, f):
    closeup(ctx, f, f - 310)


# ------------------------------------------------------------------ shot 5: flying -> can't stop -> snowbank
def dad_x(il):
    # glide position along the ice
    if il < 60:
        return lerp(800, 1450, eio(il / 60) * 0.5 + 0.5 * il / 60)
    if il < 140:
        u = (il - 60) / 80
        return lerp(1450, ENDX - 90, u * u * 0.5 + 0.5 * u)
    return ENDX - 90


def finale(ctx, f, il):
    # 0-60 glide "I'M FLYING!!" ; 60-90 card ; 90-140 "HOW DO I STOP?!" ; 140 BONK -> flip arc 140-158 ;
    # 158 FLOOMP ; 158-200 legs sticking out, kid "Lesson TWO... STOPPING." ; 200-230 Dad pops out
    x = dad_x(min(il, 140))
    cx = clamp(lerp(x + 120, x + 120, 1), 1100, 2280) if il < 140 else lerp(2280, 2440, eio(pop(il, 140, 160)))
    z = 1.12 if il < 140 else lerp(1.12, 1.3, eio(pop(il, 150, 170)))
    ctx.save(); cam(ctx, cx, 1400, z, 0, shake_at(il, [140, 158], 12, 22), f)
    rink(ctx, il)
    # kid follows
    if il < 158:
        kx = x - 330 if il < 140 else lerp(ENDX - 420, ENDX - 300, pop(il, 140, 158))
        kp = P(eye='happy', mouth='open', lsh=150, lel=-20, rsh=-150, rel=20, lhip=-6, rhip=40, rkn=-20) if il < 90 else \
            P(eye='shock', mouth='open', lsh=150, lel=-20, rsh=-150, rel=20, head=-6)
        stand_ch(ctx, KID, kx, KKID, kp, 1, GND - 40)
    else:
        kx = lerp(ENDX - 300, ENDX - 130, eio(pop(il, 158, 172)))
        kp = P(eye='smug', mouth='smile', lsh=-20, lel=-90, rsh=40, rel=-110, head=6)
        stand_ch(ctx, KID, kx, KKID, kp, 1, GND - 40)
    bump = pop(il, 158, 163) - 0.6 * pop(il, 163, 172)
    if il < 140:
        if il < 60:
            p = P(eye='happy', mouth='grin', lsh=-90, lel=0, rsh=90, rel=0, lhip=-4, rhip=-50, rkn=-10, torso=10, head=-6)
        elif il < 90:
            p = P(eye='shock', mouth='grin', lsh=-90, lel=0, rsh=90, rel=0, lhip=-4, rhip=-30, rkn=-10, torso=10)
        else:
            a = il * 0.7
            p = P(eye='shock', mouth='scream', lsh=-150 + 40 * math.sin(a), lel=-20, rsh=150 + 40 * math.sin(a + 1), rel=20,
                  lhip=-10 + 15 * math.sin(a), rhip=10 - 15 * math.sin(a), torso=-8)
        fd = 1
        for g in range(3, 0, -1):
            gx = dad_x(max(0, il - g * 3))
            ghost(ctx, 0.12 * (4 - g), lambda gx=gx: stand_ch(ctx, DAD, gx, KDAD, p, fd, hat=True))
        d = stand_ch(ctx, DAD, x, KDAD, p, fd, hat=True)
        if il < 60:
            for k in range(6):
                sparkle(ctx, x - 160 - k * 60, GND - 200 - 80 * math.sin(il * 0.3 + k), 16, YEL)
        if il >= 60:
            speed_lines(ctx, x, GND - 120, 1, 6)
        if il >= 90:
            sweat(ctx, d['head'][0] - d['R'] * 0.95, d['head'][1] - d['R'] * 0.4, il, 1.0)
    elif il < 158:
        v = (il - 140) / 18
        fx = lerp(ENDX - 90, PILEX, v)
        hip = lerp(GND - 96, 1452, v) - 360 * math.sin(math.pi * v)
        rot = 200 * eio(v)
        p = P(eye='shock', mouth='scream', rot=rot, lsh=150, lel=-20, rsh=-150, rel=20, lhip=-30, rhip=30)
        stand_ch(ctx, DAD, fx, KDAD, p, 1, hip + 68 * 1.35 * KDAD, hat=True)
        if il < 146:
            stars_ring(ctx, ENDX, GND - 260, il, 70)
    else:
        if il < 200:
            k_ = math.sin(il * 0.9) * 8
            p = P(eye='closed', mouth='flat', rot=180, lsh=10, lel=0, rsh=-10, rel=0, lhip=-14 + k_, lkn=-8, rhip=14 - k_, rkn=8)
            stand_ch(ctx, DAD, PILEX, KDAD, p, 1, 1418 + 68 * 1.35 * KDAD, hat=False)
        else:
            u = eout(pop(il, 200, 208))
            p = P(eye='closed' if il < 212 else 'smug', mouth='smile', lsh=10, lel=-20, rsh=-10, rel=20, head=-10)
            d = stand_ch(ctx, DAD, PILEX + 10, KDAD, p, 1, lerp(1900, 1650, u), blades=False, hat=True)
            for k in range(5):   # snow on the head
                ellipse(ctx, d['head'][0] - 60 + k * 30, d['head'][1] - d['R'] * 1.3 - 6 * (k % 2), 24, 16); fl(ctx, SNOW, 2)
        snowpile(ctx, bump, front=True)
        if il < 170:
            v = pop(il, 158, 170)
            for k in range(14):
                a = -math.pi * k / 13
                ellipse(ctx, PILEX + 320 * math.cos(a) * v, 1400 + 260 * math.sin(a) * v, 26 * (1 - v) + 4, 26 * (1 - v) + 4)
                setc(ctx, (1, 1, 1, 1 - v * 0.8)); ctx.fill()
    ctx.restore()
    if 60 <= il < 90:
        card(ctx, 'p2', il, 60)
    if il < 60:
        label(ctx, "\"I'M FLYING!!\"", 540, 1385, 120, YEL, -0.03, pop(il, 4, 8))
        if il >= 26:
            label(ctx, "\"You're DOING it!!\"", 540, 1480, 90, MINT, 0.03, pop(il, 26, 30))
    elif il < 90:
        label(ctx, "*whooosh...*", 540, 1430, 100, CYAN, 0.03, pop(il, 62, 66))
    elif il < 140:
        label(ctx, "\"HOW DO I", 540, 1385, 110, WHITE, -0.04, pop(il, 92, 96))
        label(ctx, "STOP?!\"", 540, 1480, 140, RED, 0.04, pop(il, 100, 104))
    elif il < 158:
        label(ctx, "*BONK!*", 540, 470, 140, RED, -0.05, pop(il, 140, 143))
    elif il < 200:
        label(ctx, "*FLOOMP!*", 540, 470, 130, WHITE, 0.05, pop(il, 158, 161))
        if il >= 170:
            label(ctx, "\"Lesson TWO...", 540, 1385, 100, MINT, -0.03, pop(il, 170, 174))
        if il >= 182:
            label(ctx, "...STOPPING.\"", 540, 1480, 116, YEL, 0.03, pop(il, 182, 186))
    else:
        label(ctx, "\"...still a", 540, 1385, 96, WHITE, -0.03, pop(il, 208, 212))
        label(ctx, "NATURAL.\"", 540, 1480, 120, YEL, 0.03, pop(il, 214, 218))


def s5(ctx, f):
    lf = f - 400
    if lf < 230:
        finale(ctx, f, lf)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (190, s3), (310, s4), (400, s5)]
CUTS = (60, 190, 310, 400, 540, 630)


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
                              "-i", "out/skating_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
