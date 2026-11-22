"""'Dad vs ONE tiny spider' - original, general-audience comedy short, 22s.
Hook:   Dad standing ON a chair screaming, knees knocking, broom raised; kid crouched happily next to a TINY cute spider.
        Caption "DAD vs ONE TINY SPIDER:" + "\"SPIDERRR!!\""
Beat 1: floor-level: giant cute spider in the foreground, Dad tiptoes in with the broom "Stand back. I've GOT this."
        -> the spider WAVES -> Dad ECU "IT WAVED AT ME!!" -> Dad dangling from the ceiling lamp "NOPE." / kid "...Dad?"
Beat 2: glass trick: *CLINK!* "GOT HIM!!" -> push-in: the glass is empty, the spider is sitting on Dad's head "...hi."
        -> Dad runs back and forth flailing "GET IT OFF!!" while the spider rides his head in a tiny cowboy hat "*YEEHAW!*"
Beat 3: Mom walks in with her tea, one finger: the spider hops on "Come here, little guy." -> window "Bye bye!"
        -> Dad on the sofa, hands on hips "I had it under CONTROL." / Mom "Sure, honey."
Twist:  "PLOT TWIST: IT CAME BACK... WITH ITS MOM." giant fluffy mama spider + babies at the window *knock knock*
        -> Mom is now on the chair screaming, shoves the broom to Dad "THAT one's YOURS!" -> both on the chair, kid waves
        "Can they STAY?!" -> loops to the hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face, _SCR
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes65 import dog, mug
from scenes64 import confetti
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
SPID = hx('4a3a66'); WOOD = hx('c9874e')
DAD = dict(doodle.DAD, shirt=hx('7ee0a0'), pants=hx('2a3a6a'))
MOM = dict(doodle.MOM_G, shirt=hx('ff7fb0'), pants=hx('3d5a9e'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ffc93c'), pants=hx('3d7bff'), shoes=hx('ff4d5e'))
N = 660
FLOOR = 1560
SEAT = FLOOR - 210              # chair seat top
CHX = 760                       # chair x
KDAD, KMOM, KKID = 1.1, 1.05, 0.95
LAMP = (520, 700)               # pendant lamp shade centre
WIN = (690, 560, 330, 380)      # window x, y, w, h

CAPS = {'p1': [[("DAD vs ", OUT), ("ONE TINY SPIDER:", PURPLE)]],
        'p2': [[("PLOT TWIST:", RED)], [("IT CAME BACK...", OUT)], [("WITH ITS ", OUT), ("MOM!", PINK)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def spider(ctx, x, y, s=1.0, lf=0, wave=0.0, mama=False, hat=False, eye='normal', hop=0.0):
    """cute round spider standing at (x, y). wave 0..1 raises a front leg and waves it."""
    by = y - 30 * s - hop
    col = hx('c45ab8') if mama else SPID
    # legs
    for side in (-1, 1):
        for i in range(4):
            if side == 1 and i == 0 and wave > 0:
                a = -1.2 - 0.5 * wave + 0.35 * wave * math.sin(lf * 0.8)
                kx, ky = x + side * 40 * s, by - 10 * s
                ex, ey = kx + math.cos(a) * 44 * s, ky + math.sin(a) * 44 * s
                ctx.move_to(x + side * 18 * s, by); ctx.curve_to(x + side * 30 * s, by - 20 * s, kx, ky - 10 * s, ex, ey)
            else:
                sp = (i - 1.5) * 0.34
                kx = x + side * (40 + 10 * (1.5 - abs(i - 1.5))) * s + side * 6 * s * math.sin(lf * 0.5 + i)
                ky = by - (22 - 4 * abs(i - 1.5)) * s
                fx = x + side * (52 + 14 * (1.5 - abs(i - 1.5)) + i * 6 - 9) * s
                ctx.move_to(x + side * 16 * s, by + sp * 20 * s); ctx.curve_to(kx - side * 10 * s, ky, kx, ky, fx, y)
            ink(ctx, max(3, 7 * s)); ctx.stroke()
    # fuzzy body
    ctx.new_path()
    for k in range(24):
        a = k / 24 * 2 * math.pi; r = 34 * s * (1 + 0.07 * (k % 2))
        (ctx.move_to if k == 0 else ctx.line_to)(x + math.cos(a) * r * 1.05, by + math.sin(a) * r * 0.95)
    ctx.close_path(); fl(ctx, col, max(3, 5 * s))
    ellipse(ctx, x - 12 * s, by - 18 * s, 9 * s, 6 * s, -0.5); setc(ctx, (1, 1, 1, 0.35)); ctx.fill()
    # eyes
    for dx in (-12, 12):
        ex, ey = x + dx * s, by - 4 * s
        if eye == 'happy':
            ctx.new_path(); ctx.arc(ex, ey + 3 * s, 7 * s, math.pi * 1.1, math.pi * 1.9); ink(ctx, max(2, 3 * s)); ctx.stroke()
        else:
            ellipse(ctx, ex, ey, 10 * s, 12 * s); fl(ctx, WHITE, max(2, 3 * s))
            ellipse(ctx, ex + 1.5 * s, ey + 2 * s, 6 * s, 7.5 * s); setc(ctx, INK); ctx.fill()
            ellipse(ctx, ex - 1 * s, ey - 1 * s, 2.5 * s, 2.5 * s); setc(ctx, WHITE); ctx.fill()
        if mama:
            for j in range(3):
                ctx.move_to(ex + (j - 1) * 5 * s, ey - 11 * s); ctx.line_to(ex + (j - 1) * 8 * s, ey - 17 * s)
            ink(ctx, max(2, 2.5 * s)); ctx.stroke()
    for dx in (-22, 22):
        ellipse(ctx, x + dx * s, by + 10 * s, 7 * s, 4 * s); setc(ctx, (1, 0.5, 0.62, 0.8)); ctx.fill()
    ctx.new_path(); ctx.arc(x, by + 10 * s, 6 * s, 0.2, math.pi - 0.2); ink(ctx, max(2, 3 * s)); ctx.stroke()
    if mama:                                             # big bow
        for d in (-1, 1):
            poly(ctx, [(x, by - 32 * s), (x + d * 26 * s, by - 46 * s), (x + d * 26 * s, by - 18 * s)]); fl(ctx, PINK, max(2, 3 * s))
        ellipse(ctx, x, by - 32 * s, 7 * s, 7 * s); fl(ctx, PINK, max(2, 3 * s))
    if hat:                                              # tiny cowboy hat
        ctx.save(); ctx.translate(x, by - 30 * s); ctx.rotate(-0.15 + 0.1 * math.sin(lf * 0.6))
        ellipse(ctx, 0, 0, 30 * s, 7 * s); fl(ctx, hx('b5743a'), max(2, 3 * s))
        rect_r(ctx, -14 * s, -22 * s, 28 * s, 22 * s, 6 * s); fl(ctx, hx('b5743a'), max(2, 3 * s))
        ctx.restore()


def chair(ctx, x, top=SEAT):
    rect_r(ctx, x - 110, top - 330, 26, 340, 10); fl(ctx, WOOD, 6)          # back posts
    rect_r(ctx, x + 84, top - 330, 26, 340, 10); fl(ctx, WOOD, 6)
    rect_r(ctx, x - 120, top - 350, 240, 50, 16); fl(ctx, hx('e09a5c'), 6)
    for yy in (top - 240, top - 140):
        rect_r(ctx, x - 96, yy, 192, 18, 8); fl(ctx, hx('e09a5c'), 4)
    for lx in (x - 100, x + 76):
        rect_r(ctx, lx, top + 20, 24, FLOOR - top - 10, 8); fl(ctx, WOOD, 6)
    rect_r(ctx, x - 130, top - 4, 260, 34, 12); fl(ctx, hx('ff8a5c'), 6)


def chair_back_only(ctx, x, top=SEAT):
    pass


def broom(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -9, -60, 18, 330, 8); fl(ctx, hx('d99a5c'), 5)
    poly(ctx, [(-24, 260), (24, 260), (60, 380), (-60, 380)]); fl(ctx, hx('ffd86b'), 6)
    for i in range(-4, 5):
        ctx.move_to(i * 6, 268); ctx.line_to(i * 13, 372)
    ink(ctx, 3); ctx.stroke()
    rect_r(ctx, -28, 250, 56, 22, 6); fl(ctx, RED, 4)
    ctx.restore()


def glass(ctx, x, y, s=1.0):
    """upside-down tumbler, rim on (x, y)"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    poly(ctx, [(-60, 0), (60, 0), (46, -140), (-46, -140)]); setc(ctx, (0.75, 0.92, 1, 0.45)); ctx.fill_preserve(); ink(ctx, 6); ctx.stroke()
    ctx.move_to(-36, -20); ctx.line_to(-28, -120); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()


def lamp(ctx, x, y, swing=0.0):
    ctx.save(); ctx.translate(x, -400); ctx.rotate(swing); ctx.translate(-x, 400)
    ctx.move_to(x, -400); ctx.line_to(x, y - 60); ink(ctx, 6); ctx.stroke()
    ctx.new_path(); ctx.move_to(x - 110, y + 40); ctx.curve_to(x - 100, y - 40, x - 50, y - 70, x, y - 70)
    ctx.curve_to(x + 50, y - 70, x + 100, y - 40, x + 110, y + 40); ctx.close_path(); fl(ctx, hx('ffb347'), 7)
    ellipse(ctx, x, y + 46, 30, 18); setc(ctx, hx('fff6c0')); ctx.fill()
    ctx.restore()


def window(ctx, family=0.0, lf=0, open_=0.0, tiny=None):
    x, y, w, h = WIN
    rect_r(ctx, x, y, w, h, 14); fl(ctx, hx('a8e0ff'), 8)
    ctx.save(); rect_r(ctx, x, y, w, h, 14); ctx.clip()
    for cx_, cy_ in ((x + 90, y + 90), (x + 240, y + 170)):
        for dx, r in ((-28, 24), (0, 34), (30, 24)):
            ellipse(ctx, cx_ + dx, cy_, r, r * 0.8); setc(ctx, WHITE); ctx.fill()
    ellipse(ctx, x + 60, y + h + 40, 200, 110); fl(ctx, hx('7ed36b'), 5)
    ellipse(ctx, x + 280, y + h + 60, 180, 120); fl(ctx, hx('5cc25a'), 5)
    if family > 0:
        up = eout(family)
        spider(ctx, x + w / 2 + 10, lerp(y + h + 330, y + h * 0.55 + 130, up), 3.6, lf, wave=1.0, mama=True)
    if tiny:
        tiny()
    ctx.restore()
    if family > 0:
        up = eout(family)
        for i in range(5):                                        # babies on the sill
            spider(ctx, x + 40 + i * 62, y + h + 6, 0.55, lf + i * 3, wave=1.0 if (i % 2 == 0) else 0, hop=8 * abs(math.sin(lf * 0.4 + i)) * up)
    if open_ < 0.5:
        ctx.move_to(x + w / 2, y); ctx.line_to(x + w / 2, y + h); ink(ctx, 7); ctx.stroke()
    ctx.move_to(x, y + h / 2 - 10); ctx.line_to(x + 14, y + h / 2 - 10); ink(ctx, 5); ctx.stroke()
    rect_r(ctx, x - 24, y + h - 4, w + 48, 26, 8); fl(ctx, WHITE, 6)
    for sx, d in ((x - 40, -1), (x + w - 10, 1)):                  # curtains
        poly(ctx, [(sx, y - 30), (sx + 50, y - 30), (sx + 50 + d * 10, y + h + 50), (sx - 10 + d * 4, y + h + 50)]); fl(ctx, hx('ffd34f'), 6)
    rect_r(ctx, x - 70, y - 44, w + 140, 20, 8); fl(ctx, hx('a0603a'), 5)


def room(ctx, lf, family=0.0, lamp_on=True, tiny=None):
    wall = hx('ffe3b8')
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, wall); ctx.fill()
    rnd = random.Random(9)
    for k in range(90):                                     # polka-dot wallpaper
        ellipse(ctx, rnd.uniform(-500, 1600), rnd.uniform(-300, FLOOR - 30), 9, 9); setc(ctx, dark(wall, 0.93)); ctx.fill()
    ctx.rectangle(-3000, FLOOR - 120, 9000, 120); setc(ctx, hx('ffd29a')); ctx.fill()      # wainscot
    ctx.move_to(-3000, FLOOR - 120); ctx.line_to(6000, FLOOR - 120); ink(ctx, 5); ctx.stroke()
    window(ctx, family, lf, tiny=tiny)
    # picture frames (left)
    rect_r(ctx, 110, 560, 190, 150, 10); fl(ctx, hx('8ad4ff'), 7)
    rect_r(ctx, 130, 580, 150, 110, 6); fl(ctx, hx('fff6d8'), 4)
    ctx.move_to(150, 670); ctx.line_to(190, 620); ctx.line_to(220, 650); ctx.line_to(250, 610); ctx.line_to(270, 670); ink(ctx, 4); ctx.stroke()
    ellipse(ctx, 245, 605, 12, 12); setc(ctx, GOLD); ctx.fill()
    rect_r(ctx, 340, 600, 110, 110, 10); fl(ctx, hx('ff9ec4'), 6)
    ctx.move_to(395, 690); ctx.curve_to(345, 650, 370, 615, 395, 640); ctx.curve_to(420, 615, 445, 650, 395, 690); fl(ctx, RED, 3)
    # sofa (left, behind)
    rect_r(ctx, -40, 1120, 520, 320, 50); fl(ctx, hx('6fa8ff'), 8)
    rect_r(ctx, -10, 1150, 220, 200, 34); fl(ctx, hx('8fc0ff'), 6)
    rect_r(ctx, 230, 1150, 220, 200, 34); fl(ctx, hx('8fc0ff'), 6)
    rect_r(ctx, -60, 1330, 570, 150, 30); fl(ctx, hx('5a94f0'), 8)
    ellipse(ctx, 330, 1280, 60, 46, 0.3); fl(ctx, hx('ffd34f'), 5)          # cushion
    for lx in (10, 440):
        rect_r(ctx, lx, 1480, 30, FLOOR - 1470, 8); fl(ctx, hx('5a3a2a'), 5)
    # floor + rug + plant
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('d8a06a')); ctx.fill()
    for k in range(-10, 30):
        ctx.move_to(k * 150, FLOOR); ctx.line_to(k * 150 - 140, FLOOR + 600)
    setc(ctx, hx('c48b55')); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-3000, FLOOR); ctx.line_to(6000, FLOOR); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 560, FLOOR + 150, 470, 90); fl(ctx, hx('9be38a'), 6)
    ellipse(ctx, 560, FLOOR + 150, 390, 66); setc(ctx, hx('c4f2b6')); ctx.fill()
    px = 1070
    poly(ctx, [(px - 55, FLOOR - 120), (px + 55, FLOOR - 120), (px + 42, FLOOR + 10), (px - 42, FLOOR + 10)]); fl(ctx, hx('7a8cff'), 6)
    for a in (-0.7, -0.25, 0.2, 0.65):
        ellipse(ctx, px + 80 * math.sin(a), FLOOR - 210 - 36 * math.cos(a), 30, 84, a); fl(ctx, GREEN, 5)
    if lamp_on:
        lamp(ctx, *LAMP)


def hold_broom(ctx, b, f, a):
    hx_, hy_ = b['front']
    broom(ctx, hx_, hy_, a, 0.9)


def knock(lf, amp=10):
    return amp * math.sin(lf * 1.6)


# ------------------------------------------------------------------ shot 1: hook
def chair_dad(ctx, lf, ch=DAD, k=KDAD, x=CHX, p=None, brm=True):
    kn = knock(lf)
    p = p or P(eye='shock', mouth='scream', lsh=150, lel=20, rsh=75, rel=-20, lhip=6 + kn, lkn=-4, rhip=-6 - kn, rkn=-4, torso=-4, head=-8)
    b = draw(ctx, x + 6 * math.sin(lf * 1.9), SEAT - 186 * k, k, -1, ch, p)
    if brm:
        hold_broom(ctx, b, -1, 0.75 + 0.15 * math.sin(lf * 0.9))
    return b


def hook(ctx, f, lf):
    ctx.save(); cam(ctx, 560, 1250, 1.08 + 0.04 * eio(pop(lf, 0, 54)), 0, 4, f)
    room(ctx, lf)
    dog(ctx, 150, FLOOR + 230, 0.5, 1, lf, sleep=True)
    chair(ctx, CHX)
    b = chair_dad(ctx, lf)
    sweat(ctx, b['head'][0] - b['R'] * 1.0, b['head'][1] - b['R'] * 0.6, lf, 1.2)
    draw(ctx, 280, FLOOR + 40 - 186 * KKID, KKID, 1, KID, P(eye='happy', mouth='grin', torso=22, head=10, rsh=70, rel=-10, lsh=20, lel=-30, lhip=40, lkn=-60, rhip=30, rkn=-70))
    spider(ctx, 540, FLOOR + 20, 1.5, lf, wave=1.0)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"SPIDERRR!!\"", 540, 1440, 150, YEL, -0.04, t)


# ------------------------------------------------------------------ shot 2: floor-level, wave, ECU, lamp
def floor_level(ctx, f, il):
    # il 0..66: Dad tiptoes in (bg), giant cute spider in the fg; waves at il 40
    t = eio(pop(il, 0, 40))
    ph = il * 0.35
    ctx.save(); cam(ctx, 600, 1300, 1.0 + 0.08 * eio(pop(il, 0, 66)), 0, 0, f)
    room(ctx, il)
    dp = P(eye='glare', mouth='flat', torso=18, head=-6, lsh=150, lel=40, rsh=140, rel=40,
           lhip=20 * math.sin(ph), lkn=-30, rhip=-20 * math.sin(ph), rkn=-30)
    if il >= 42:
        dp = P(eye='shock', mouth='open', torso=-10, lsh=150, lel=20, rsh=70, rel=-20)
    b = draw(ctx, lerp(1000, 820, t), FLOOR - 40 - 186 * KDAD, KDAD, -1, DAD, dp)
    hold_broom(ctx, b, -1, 3.6 if il < 42 else 0.75)
    ctx.restore()
    # foreground spider (screen space, big)
    wv = eout(pop(il, 40, 46))
    spider(ctx, 360, 1560 - 30 * abs(math.sin(il * 0.25)) * 0, 4.2, il, wave=wv, eye='normal')
    if il >= 44:
        for j in range(3):
            sparkle(ctx, 200 + j * 150, 1180 + 30 * (j % 2), 16 + 6 * math.sin(il * 0.6 + j), YEL)
    if il < 40:
        label2(ctx, "\"Stand back.", "I've GOT this.\"", WHITE, pop(il, 3, 7), 104, col2=YEL, y=520)
    else:
        label(ctx, "*wave wave*", 540, 560, 104, PINK, -0.04, pop(il, 42, 45))


def waved(ctx, f, il):
    # il 0..40: Dad ECU
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eio(pop(il, 0, 40)), 0, shake_at(il, [0], 12, 18) + 3, f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('b98bff')); ctx.fill()
    rays(ctx, 540, 960, 240, 1500, il * 0.03, col=(1, 1, 1), a=0.3, n=16)
    R = 205; cx, cy = 540, 930
    face(ctx, DAD, P(eye='shock', mouth='scream'), cx, cy, R, 0.04 * math.sin(il * 1.3))
    sweat(ctx, cx + 1.0 * R, cy - 0.6 * R, il, 1.3); sweat(ctx, cx - 1.05 * R, cy - 0.4 * R, il + 20, 1.1)
    ctx.restore()
    label2(ctx, "\"IT WAVED", "AT ME!!\"", WHITE, pop(il, 2, 6), 130, col2=RED, y=1440)


def bookcase(ctx, x0, x1, top):
    rect_r(ctx, x0, top, x1 - x0, FLOOR - top + 10, 12); fl(ctx, hx('b5743a'), 8)
    rnd = random.Random(4)
    nsh = 4; hsh = (FLOOR - top - 40) / nsh
    for i in range(nsh):
        y0 = top + 20 + i * hsh
        rect_r(ctx, x0 + 18, y0, x1 - x0 - 36, hsh - 16, 6); fl(ctx, hx('7a4a2c'), 4)
        bx = x0 + 26
        while bx < x1 - 60:
            w = rnd.uniform(22, 38); hh = rnd.uniform(0.6, 0.9) * (hsh - 24)
            rect_r(ctx, bx, y0 + hsh - 18 - hh, w, hh, 4); fl(ctx, rnd.choice((RED, BLUE, GOLD, GREEN, PINK, PURPLE)), 3)
            bx += w + 4


def dangle(ctx, f, il):
    # il 0..40: Dad crouched on TOP of the tall bookcase, broom like a sword; kid below with the spider on his palm
    ctx.save(); cam(ctx, 600, 1040, 1.0, 0, shake_at(il, [0], 8, 14), f)
    room(ctx, il)
    dog(ctx, 150, FLOOR + 230, 0.5, 1, il, sleep=True)
    top = 960
    bookcase(ctx, 780, 1060, top)
    kn = knock(il, 8)
    dp = P(eye='shock', mouth='open', torso=10, lsh=150, lel=30, rsh=70, rel=-20, lhip=50 + kn, lkn=-80, rhip=40 - kn, rkn=-80)
    b = draw(ctx, 920 + 4 * math.sin(il * 1.9), top + 30 - 186 * KDAD, KDAD, -1, DAD, dp)
    hold_broom(ctx, b, -1, 0.8 + 0.12 * math.sin(il * 0.9))
    sweat(ctx, b['head'][0] + b['R'] * 1.0, b['head'][1] - b['R'] * 0.6, il, 1.2)
    kp = P(eye='normal', mouth='smile', head=-14, rsh=60, rel=-60, lsh=20, lel=-20)
    kb = draw(ctx, 380, FLOOR + 40 - 186 * KKID, KKID, 1, KID, kp)
    spider(ctx, kb['front'][0] + 6, kb['front'][1] - 12, 0.6, il, wave=1.0)
    ctx.restore()
    label(ctx, "\"NOPE.\"", 540, 330, 130, RED, -0.04, pop(il, 2, 5))
    label(ctx, "\"...Dad?\"", 540, 1440, 120, WHITE, 0.03, pop(il, 18, 21))


def s2(ctx, f):
    lf = f - 54
    if lf < 66:
        floor_level(ctx, f, lf)
    elif lf < 106:
        waved(ctx, f, lf - 66)
    else:
        dangle(ctx, f, lf - 106)


# ------------------------------------------------------------------ shot 3: glass trick + run
def glass_trick(ctx, f, il):
    # il 0..66: 0-18 crouch + lift glass, 18 CLINK, 18-36 "GOT HIM!!", 36-66 push-in to head: spider says hi
    slam = il >= 18
    gy = FLOOR + 40 - (0 if slam else 120 * eio(pop(il, 0, 14)))
    z = 1.0 + 0.6 * eio(pop(il, 36, 54))
    ctx.save(); cam(ctx, lerp(560, 640, eio(pop(il, 36, 54))), lerp(1250, 1000, eio(pop(il, 36, 54))), z, 0, shake_at(il, [18], 10, 20), f)
    room(ctx, il)
    chair(ctx, CHX + 200)
    dp = P(eye='glare' if not slam else 'smug', mouth='flat' if not slam else 'grin', torso=55, head=-40, lsh=95, lel=-10, rsh=80, rel=-10,
           lhip=80, lkn=-110, rhip=70, rkn=-100)
    if il >= 40:
        dp = dict(dp, eye='normal', mouth='flat', head=-30)
    b = draw(ctx, 760, FLOOR + 30 - 186 * KDAD, KDAD, -1, DAD, dp)
    glass(ctx, 520, gy, 1.0)
    if il >= 30:                                                    # spider sits on Dad's head
        hx_, hy_ = b['head']; R = b['R']
        spider(ctx, hx_ - 0.1 * R, hy_ - R * 0.88 - 14 * eout(pop(il, 30, 34)), 1.0, il, wave=1.0 if il >= 44 else 0)
    ctx.restore()
    if slam and il < 36:
        label(ctx, "*CLINK!*", 540, 560, 100, CYAN, 0.04, pop(il, 18, 21))
        label(ctx, "\"GOT HIM!!\"", 540, 1440, 140, YEL, -0.04, pop(il, 20, 23))
    if il >= 46:
        label(ctx, "\"...hi.\"", 540, 420, 140, PINK, -0.03, pop(il, 46, 49))


def run_scene(ctx, f, il):
    # il 0..74: Dad runs back and forth flailing, spider rides his head in a cowboy hat
    ph = il * 0.13
    x = 560 + 300 * math.sin(ph)
    dirn = 1 if math.cos(ph) > 0 else -1
    ctx.save(); cam(ctx, 560, 1120, 1.02, 3 * math.sin(il * 0.2), 4, f)
    room(ctx, il)
    chair(ctx, CHX + 200)
    for j in range(4):                                       # speed lines
        yy = 1150 + j * 90
        ctx.move_to(x - dirn * 140, yy); ctx.line_to(x - dirn * (300 + 60 * j), yy); ink(ctx, 6); ctx.stroke()
    fl_ = 50 * math.sin(il * 1.2)
    rp = run_pose(il * 0.9, eye='shock', mouth='scream', lsh=160 + fl_, lel=30, rsh=150 - fl_, rel=30, torso=4)
    b = draw(ctx, x, FLOOR + 40 - 186 * KDAD, KDAD, dirn, DAD, rp)
    hx_, hy_ = b['head']; R = b['R']
    spider(ctx, hx_, hy_ - R * 0.88, 1.0, il, wave=1.0, hat=True, eye='happy')
    ctx.restore()
    label(ctx, "\"GET IT OFF!!\"", 540, 1440, 140, WHITE, -0.04, pop(il, 2, 5))
    if il >= 30:
        label(ctx, "*YEEHAW!*", 540, 360, 110, ORANGE, 0.05, pop(il, 30, 33))


def s3(ctx, f):
    lf = f - 200
    if lf < 66:
        glass_trick(ctx, f, lf)
    else:
        run_scene(ctx, f, lf - 66)


# ------------------------------------------------------------------ shot 4: Mom
def mom_rescue(ctx, f, il):
    # il 0..70: 0-14 Mom walks in, 14-40 finger, spider hops over, 40-70 window bye
    walk = eio(pop(il, 0, 14))
    mx = lerp(1250, 900, walk)
    ctx.save(); cam(ctx, 600, 1250, 1.05, 0, 0, f)

    def tiny_out():
        if il >= 46:
            spider(ctx, WIN[0] + 190, WIN[1] + WIN[3] - 4, 0.7, il, wave=1.0, eye='happy')
    room(ctx, il, tiny=None)
    dp = P(eye='shock', mouth='flat', torso=-6, lsh=150, lel=40, rsh=140, rel=40)
    b = draw(ctx, 470, FLOOR + 40 - 186 * KDAD, KDAD, 1, DAD, dp)
    hx_, hy_ = b['head']; R = b['R']
    mp = P(eye='normal', mouth='smile', lsh=10, lel=-60, rsh=100 if 14 <= il < 46 else 30, rel=-20 if 14 <= il < 46 else -100,
           lhip=10 * math.sin(il * 0.6) if il < 14 else 6, rhip=-10 * math.sin(il * 0.6) if il < 14 else -6)
    m = draw(ctx, mx if il < 40 else lerp(900, 830, eio(pop(il, 40, 50))), FLOOR + 40 - 186 * KMOM, KMOM, -1, MOM, mp)
    mug(ctx, m['back'][0] - 10, m['back'][1] - 30, 0.75, il)
    hop = pop(il, 22, 34)
    if il < 22:
        spider(ctx, hx_, hy_ - R * 0.88, 1.0, il, wave=0.0, eye='normal')
    elif il < 46:
        fx, fy = m['front']
        sx = lerp(hx_, fx, hop); sy = lerp(hy_ - R * 0.88, fy - 18, hop) - 160 * math.sin(math.pi * hop)
        spider(ctx, sx, sy, 1.0, il, wave=1.0 if il >= 34 else 0, eye='happy' if il >= 34 else 'normal')
    ctx.restore()
    if il >= 46:   # outside on the sill, small, drawn in world again via cam
        ctx.save(); cam(ctx, 600, 1250, 1.05, 0, 0, f)
        spider(ctx, WIN[0] + WIN[2] / 2, WIN[1] + WIN[3] - 2, 1.3, il, wave=1.0, eye='happy')
        ctx.restore()
    if il < 40:
        label2(ctx, "\"Come here,", "little guy.\"", WHITE, pop(il, 14, 18), 110, col2=PINK, y=1440)
    else:
        label(ctx, "\"Bye bye!\"", 540, 1440, 140, PINK, -0.03, pop(il, 48, 51))


def control(ctx, f, il):
    # il 0..70: Dad hands on hips "I had it under CONTROL." / Mom deadpan "Sure, honey."
    ctx.save(); cam(ctx, 600, 1260, 1.12 + 0.05 * eio(pop(il, 0, 70)), 0, 0, f)
    room(ctx, il)
    dp = P(eye='smug', mouth='grin', lsh=40, lel=-120, rsh=40, rel=-120, head=-8, torso=-6)
    b = draw(ctx, 480, FLOOR + 40 - 186 * KDAD, KDAD, 1, DAD, dp)
    if il < 36:
        for j in range(2):
            sparkle(ctx, b['head'][0] + (j * 2 - 1) * b['R'] * 1.3, b['head'][1] - b['R'] * 0.9, 18 + 6 * math.sin(il * 0.7 + j), YEL)
    mp = P(eye='normal' if il < 36 else 'smug', mouth='flat', lsh=10, lel=-60, rsh=30, rel=-100, head=6)
    m = draw(ctx, 860, FLOOR + 40 - 186 * KMOM, KMOM, -1, MOM, mp)
    mug(ctx, m['back'][0] - 10, m['back'][1] - 30, 0.75, il)
    ctx.restore()
    if il < 36:
        label2(ctx, "\"I had it under", "CONTROL.\"", WHITE, pop(il, 2, 6), 110, col2=GREEN, y=1440)
    else:
        label(ctx, "\"Sure, honey.\"", 540, 1440, 130, PINK, -0.03, pop(il, 36, 39))


def s4(ctx, f):
    lf = f - 340
    if lf < 70:
        mom_rescue(ctx, f, lf)
    else:
        control(ctx, f, lf - 70)


# ------------------------------------------------------------------ shot 5: twist
def comeback(ctx, f, il):
    # il 0..64: window push-in: *knock knock* -> mama spider rises with babies
    fam = pop(il, 14, 34)
    z = 1.25 + 0.35 * eio(pop(il, 0, 64))
    ctx.save(); cam(ctx, WIN[0] + WIN[2] / 2, WIN[1] + WIN[3] / 2 + 60, z, 0, shake_at(il, [4, 10], 6, 8), f)
    room(ctx, il, family=fam)
    ctx.restore()
    if il < 14:
        label(ctx, "*knock knock*", 540, 1440, 110, WHITE, -0.03, pop(il, 3, 6))


def both_on_chair(ctx, f, il):
    # il 0..76: 0-38 Mom on the chair screaming, shoves the broom at Dad; 38-76 both on the chair, kid waves at the window
    both = il >= 38
    ctx.save(); cam(ctx, 640, 1130, 1.0, 0, 4 if not both else 3, f)
    room(ctx, il, family=1.0)
    dog(ctx, 150, FLOOR + 230, 0.5, 1, il, sleep=True)
    chair(ctx, CHX)
    kn = knock(il)
    mp = P(eye='shock', mouth='scream', lsh=150, lel=20, rsh=100, rel=0, lhip=6 + kn, rhip=-6 - kn, head=-6)
    if not both:
        m = draw(ctx, CHX + 4 * math.sin(il * 1.9), SEAT - 186 * KMOM, KMOM, -1, MOM, mp)
        b = draw(ctx, 460, FLOOR + 40 - 186 * KDAD, KDAD, 1, DAD, P(eye='shock', mouth='open', lsh=80, lel=-10, rsh=60, rel=-10))
        broom(ctx, lerp(m['front'][0], b['front'][0], eio(pop(il, 6, 16))), lerp(m['front'][1], b['front'][1], eio(pop(il, 6, 16))), lerp(2.8, 5.6, eio(pop(il, 6, 16))), 0.9)
        twitch(ctx, b['head'][0] - b['R'] * 0.9, b['head'][1] - b['R'] * 0.8, il, 1.0)
    else:
        mp = dict(mp, lsh=150, rsh=150, rel=30)
        draw(ctx, CHX - 75 + 4 * math.sin(il * 1.9), SEAT - 186 * KMOM, KMOM, -1, MOM, mp)
        chair_dad(ctx, il, x=CHX + 75, brm=False)
        kb = draw(ctx, 300, FLOOR + 40 - 186 * KKID, KKID, 1, KID,
                  P(eye='happy', mouth='grin', lsh=20, lel=-20, rsh=160 + 20 * math.sin(il * 0.8), rel=20))
    ctx.restore()
    if not both:
        label2(ctx, "\"THAT one's", "YOURS!!\"", WHITE, pop(il, 2, 6), 120, col2=RED, y=1440)
    else:
        label2(ctx, "\"Can they", "STAY?!\"", WHITE, pop(il, 40, 44), 120, col2=YEL, y=1440)


def s5(ctx, f):
    lf = f - 480
    if lf < 64:
        comeback(ctx, f, lf)
        card(ctx, 'p2', lf, 0)
    elif lf < 140:
        both_on_chair(ctx, f, lf - 64)
    else:
        s1(ctx, f, f - 620)


SHOTS = [(0, s1), (54, s2), (200, s3), (340, s4), (480, s5)]
CUTS = (54, 120, 160, 200, 266, 340, 410, 480, 544, 620)


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
                              "-i", "out/tiny_spider_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
