"""'The advent calendar: December 1st' - original, general-audience comedy short, 22s.
Hook:   living-room medium shot: kid next to the advent calendar with ALL 24 doors open, cheeks stuffed with chocolate,
        caught-in-the-act shock eyes. Caption "THE ADVENT CALENDAR, DECEMBER 1st:" + "I only opened ONE!"
Beat 1: kid opens door 1 *CLICK!* -> chocolate *NOM!* "Yum!" -> door 2 glows and wiggles *ting* "...just ONE more."
Beat 2: Dutch-tilt speed montage: doors pop open *POP! POP! POP!*, chocolates fly into his mouth, cheeks inflate *NOM NOM NOM*
Beat 3: Mom's voice "Sweetie... did you open door ONE?" kid spreads his arms in front of the calendar "Mm-HMM!"
Turn:   Mom leans round: every door open "...ALL 24?!"  ECU kid: "...it's called PLANNING AHEAD."
Twist:  "PLOT TWIST: DAD HAS ONE TOO." Dad on the sofa slowly turns, cheeks stuffed, his calendar all open "...mm-HMM?"
        Mom confiscates both "NO. MORE. CHOCOLATE." -> split screen: kitchen, Mom opens HER calendar "...just ONE." *nom*
        -> loop to the hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes65 import dog, mug
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
CHOC = hx('7a4426'); CHOC_D = hx('55301a'); PINE = hx('2fae5f')
DAD = dict(doodle.DAD, shirt=hx('1f8bff'), pants=hx('34477e'))
MOM = dict(doodle.MOM_G, shirt=hx('8a3cff'), pants=hx('2f4a8a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff3b5c'))
N = 660
CEIL = 430
FLOOR = 1560
GND = 1590
KD, KM, KK = 1.2, 1.12, 1.0
CBX0, CBX1, CBTOP = 820, 1280, 1330         # sideboard
CALX, CALB = 1050, 1330                     # calendar centre x, base y
CW, CH, ROOF = 420, 330, 110

CAPS = {'p1': [[("THE ADVENT CALENDAR,", OUT)], [("DECEMBER ", OUT), ("1st:", RED)]],
        'p2': [[("PLOT TWIST:", RED)], [("DAD HAS ", OUT), ("ONE TOO.", GREEN)]]}
scenes13.CAPS = CAPS
card = _card13

NUMS = [17, 3, 22, 9, 14, 1, 6, 20, 11, 24, 2, 15, 8, 19, 4, 13, 23, 10, 5, 18, 12, 21, 7, 16]


# ------------------------------------------------------------------ props
def treat(ctx, x, y, r, kind=0, rot=0.0):
    """foil-wrapped chocolate: 0 star, 1 bell, 2 coin"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    if kind == 0:
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            rr = r if k % 2 == 0 else r * 0.5
            pts.append((rr * math.cos(a), rr * math.sin(a)))
        poly(ctx, pts); fl(ctx, GOLD, 3)
    elif kind == 1:
        ctx.new_path(); ctx.move_to(-r * 0.8, r * 0.6); ctx.curve_to(-r * 0.7, -r * 0.2, -r * 0.5, -r * 0.9, 0, -r * 0.9)
        ctx.curve_to(r * 0.5, -r * 0.9, r * 0.7, -r * 0.2, r * 0.8, r * 0.6); ctx.close_path(); fl(ctx, RED, 3)
        ellipse(ctx, 0, r * 0.7, r * 0.18, r * 0.18); fl(ctx, GOLD, 2)
    else:
        ellipse(ctx, 0, 0, r * 0.8, r * 0.8); fl(ctx, hx('ffd86a'), 3)
        ellipse(ctx, 0, 0, r * 0.5, r * 0.5); setc(ctx, dark(GOLD, 0.8)); ctx.set_line_width(2); ctx.stroke()
    sparkle(ctx, -r * 0.25, -r * 0.3, r * 0.25, WHITE)
    ctx.restore()


def calendar(ctx, x, base, s, opened, lf=0, eaten=None, glow=-1, wig=0.0):
    """advent calendar house. opened: set/list of door indices open (0..23) or an int -> first n in pop order.
    eaten: indices whose treat is gone (default = opened). glow: door index that glows/wiggles."""
    if isinstance(opened, (int, float)):
        opened = set(range(int(opened)))
    eaten = opened if eaten is None else eaten
    ctx.save(); ctx.translate(x, base); ctx.scale(s, s)
    w, h = CW, CH
    # roof + body
    poly(ctx, [(-w / 2 - 30, -h), (0, -h - ROOF), (w / 2 + 30, -h)]); fl(ctx, hx('2fae5f'), 6)
    for k in range(5):                                         # snow on roof
        ellipse(ctx, -w / 2 + 30 + k * (w - 60) / 4, -h - 10 - ROOF * 0.15 * (2 - abs(k - 2)), 34, 14); setc(ctx, WHITE); ctx.fill()
    star_x, star_y = 0, -h - ROOF - 10
    treat(ctx, star_x, star_y, 34, 0, 0.1 * math.sin(lf * 0.2))
    rect_r(ctx, -w / 2, -h, w, h, 14); fl(ctx, hx('e8343f'), 6)
    rect_r(ctx, -w / 2 + 12, -h + 12, w - 24, h - 24, 10); setc(ctx, hx('ff6f6f')); ctx.set_line_width(4); ctx.stroke()
    cols, rows = 6, 4
    dw, dh = 56, 62
    gx = (w - 40 - cols * dw) / (cols - 1); gy = (h - 40 - rows * dh) / (rows - 1)
    for i in range(24):
        c, r = i % cols, i // cols
        dx = -w / 2 + 20 + c * (dw + gx); dy = -h + 20 + r * (dh + gy)
        n_ = NUMS[i]
        idx = n_ - 1                                         # door index == day number - 1
        if idx in opened:
            ctx.rectangle(dx, dy, dw, dh); fl(ctx, hx('4a1c22'), 4)
            if idx not in eaten:
                treat(ctx, dx + dw / 2, dy + dh / 2 + 2, 20, n_ % 3)
            poly(ctx, [(dx, dy), (dx - 22, dy + 8), (dx - 22, dy + dh - 8), (dx, dy + dh)]); fl(ctx, hx('fff4dc'), 3)
        else:
            jx = 0
            if idx == glow:
                jx = 5 * math.sin(lf * 2.2) * wig
                ellipse(ctx, dx + dw / 2, dy + dh / 2, dw * 0.9, dh * 0.85); setc(ctx, (1, 0.95, 0.5, 0.45)); ctx.fill()
            rect_r(ctx, dx + jx, dy, dw, dh, 6); fl(ctx, hx('fff4dc') if (n_ % 2) else hx('dff5e6'), 4)
            text(ctx, str(n_), dx + jx + dw / 2, dy + dh / 2 + 13, 34, RED if n_ % 2 else GREEN, ow=0, shadow=False)
            if idx == glow:
                sparkle(ctx, dx + dw + 6, dy - 4, 12 + 4 * math.sin(lf * 0.7), GOLD)
    ctx.restore()


def door_pos(i_day, x=CALX, base=CALB, s=1.0):
    """world centre of door for day i_day (0-based)"""
    i = NUMS.index(i_day + 1)
    cols = 6; dw, dh = 56, 62
    gx = (CW - 40 - cols * dw) / (cols - 1); gy = (CH - 40 - 4 * dh) / 3
    c, r = i % cols, i // cols
    dx = -CW / 2 + 20 + c * (dw + gx) + dw / 2; dy = -CH + 20 + r * (dh + gy) + dh / 2
    return x + dx * s, base + dy * s


def stuffed(ctx, d, amt, ch, f_=1, smear=True):
    """chipmunk cheeks + chocolate smears on a drawn character"""
    if amt <= 0:
        return
    (cx, cy), R = d['head'], d['R']
    ctx.save()
    for sx in (-1, 1):
        ellipse(ctx, cx + f_ * R * 0.06 + sx * R * (0.36 + 0.14 * amt), cy + R * 0.42, R * (0.2 + 0.16 * amt), R * (0.18 + 0.13 * amt))
        setc(ctx, ch['skin']); ctx.fill_preserve(); ink(ctx, 3.5); ctx.stroke()
        ellipse(ctx, cx + f_ * R * 0.06 + sx * R * (0.4 + 0.14 * amt), cy + R * 0.44, R * 0.12, R * 0.07); setc(ctx, (1, 0.45, 0.55, 0.6)); ctx.fill()
    ellipse(ctx, cx + f_ * R * 0.06, cy + R * 0.52, R * 0.08, R * 0.05); fl(ctx, CHOC_D, 3)
    if smear:
        for (ox, oy, rx, ry) in ((-0.22, 0.64, 0.1, 0.05), (0.3, 0.6, 0.07, 0.04), (0.5, 0.2, 0.05, 0.03), (-0.5, 0.1, 0.04, 0.03)):
            ellipse(ctx, cx + f_ * R * ox, cy + R * oy, R * rx, R * ry); setc(ctx, CHOC); ctx.fill()
    ctx.restore()


# ------------------------------------------------------------------ set
def window(ctx, lf):
    x, y, w, h = 140, 640, 330, 330
    rect_r(ctx, x, y, w, h, 16); fl(ctx, hx('9fd8ff'), 8)
    ctx.save(); rect_r(ctx, x, y, w, h, 16); ctx.clip()
    rnd = random.Random(5)
    for k in range(20):
        sx = x + rnd.uniform(0, w); sy = y + (rnd.uniform(0, h) + lf * rnd.uniform(1.5, 3)) % h
        ellipse(ctx, sx, sy, 6, 6); setc(ctx, WHITE); ctx.fill()
    ctx.new_path(); ctx.move_to(x, y + h); ctx.curve_to(x + 100, y + h - 60, x + 260, y + h - 30, x + w, y + h - 70); ctx.line_to(x + w, y + h); ctx.close_path()
    setc(ctx, WHITE); ctx.fill()
    ctx.restore()
    ctx.move_to(x + w / 2, y); ctx.line_to(x + w / 2, y + h); ctx.move_to(x, y + h / 2); ctx.line_to(x + w, y + h / 2); ink(ctx, 6); ctx.stroke()
    rect_r(ctx, x - 24, y + h - 6, w + 48, 24, 8); fl(ctx, WHITE, 5)
    for sx, d in ((x - 50, -1), (x + w - 10, 1)):
        poly(ctx, [(sx, y - 30), (sx + 60, y - 30), (sx + 60 + d * 12, y + h + 40), (sx - 10 + d * 6, y + h + 40)]); fl(ctx, hx('5fb8ef'), 6)
    rect_r(ctx, x - 80, y - 44, w + 160, 20, 8); fl(ctx, hx('a0603a'), 5)


def picture(ctx, x, y, tilt=0.0, col=hx('ffb84d')):
    ctx.save(); ctx.translate(x, y); ctx.rotate(tilt)
    ctx.move_to(0, -100); ctx.line_to(-50, -70); ctx.move_to(0, -100); ctx.line_to(50, -70); ink(ctx, 4); ctx.stroke()
    rect_r(ctx, -70, -70, 140, 120, 10); fl(ctx, col, 7)
    rect_r(ctx, -54, -54, 108, 88, 6); fl(ctx, hx('fff4dc'), 4)
    ellipse(ctx, 0, -6, 24, 24); fl(ctx, hx('ffd34f'), 3)                  # little sun doodle
    ctx.restore()


def garland(ctx, lf):
    """string of fairy lights along the ceiling"""
    ctx.new_path(); ctx.move_to(-200, CEIL + 40)
    for k in range(12):
        x0 = -200 + k * 220
        ctx.curve_to(x0 + 70, CEIL + 110, x0 + 150, CEIL + 110, x0 + 220, CEIL + 40)
    ink(ctx, 4); ctx.stroke()
    cols = (RED, GOLD, CYAN, PINK, GREEN)
    for k in range(48):
        x = -200 + k * 55; seg = (x + 200) % 220 / 220
        y = CEIL + 40 + 70 * 4 * seg * (1 - seg) * 0.95
        on = (lf // 6 + k) % 3 != 0
        ellipse(ctx, x, y + 16, 9, 13); fl(ctx, cols[k % 5] if on else dark(cols[k % 5], 0.6), 3)


def sideboard(ctx):
    rect_r(ctx, CBX0, CBTOP, CBX1 - CBX0, FLOOR - CBTOP - 20, 12); fl(ctx, hx('5fb8ef'), 7)
    rect_r(ctx, CBX0 - 16, CBTOP - 18, CBX1 - CBX0 + 32, 30, 10); fl(ctx, hx('a0603a'), 6)
    for k in range(2):
        rect_r(ctx, CBX0 + 24 + k * (CBX1 - CBX0) / 2, CBTOP + 40, (CBX1 - CBX0) / 2 - 48, FLOOR - CBTOP - 100, 8); fl(ctx, hx('8fd0ff'), 5)
        ellipse(ctx, CBX0 + (CBX1 - CBX0) / 2 + (-26 if k == 0 else 26), CBTOP + 120, 9, 9); fl(ctx, GOLD, 3)
    for lx in (CBX0 + 30, CBX1 - 30):
        ctx.rectangle(lx - 10, FLOOR - 24, 20, 26); fl(ctx, hx('a0603a'), 4)
    # mini potted pine on the sideboard
    px = CBX0 + 60
    poly(ctx, [(px - 30, CBTOP - 70), (px + 30, CBTOP - 70), (px + 22, CBTOP - 16), (px - 22, CBTOP - 16)]); fl(ctx, ORANGE, 5)
    poly(ctx, [(px - 50, CBTOP - 70), (px, CBTOP - 220), (px + 50, CBTOP - 70)]); fl(ctx, PINE, 5)
    for k, (bx, by) in enumerate(((px - 20, CBTOP - 100), (px + 18, CBTOP - 130), (px - 6, CBTOP - 170))):
        ellipse(ctx, bx, by, 8, 8); fl(ctx, (RED, GOLD, CYAN)[k], 2)


def sofa(ctx, x0=1380, x1=1980):
    rect_r(ctx, x0 + 40, 1170, x1 - x0 - 80, 250, 50); fl(ctx, hx('ff9e5c'), 8)
    rect_r(ctx, x0, 1310, x1 - x0, 200, 40); fl(ctx, hx('ffb27a'), 8)
    for cx_ in (x0 + 20, x1 - 20):
        rect_r(ctx, cx_ - 50, 1270, 100, 260, 40); fl(ctx, hx('ff9e5c'), 7)
    ellipse(ctx, x1 - 170, 1280, 62, 52, -0.2); fl(ctx, hx('7fe3ff'), 6); sparkle(ctx, x1 - 170, 1280, 18, WHITE)


def room(ctx, lf, pic_tilt=0.0):
    wall = hx('ffe8c9')
    ctx.rectangle(-3000, CEIL, 9000, 6000); setc(ctx, wall); ctx.fill()
    rnd = random.Random(87)
    for k in range(150):
        sparkle(ctx, rnd.uniform(-400, 2600), rnd.uniform(CEIL + 60, FLOOR - 140), 9, dark(wall, 0.9))
    ctx.rectangle(-3000, FLOOR - 110, 9000, 110); setc(ctx, hx('ffd2a6')); ctx.fill()
    ctx.move_to(-3000, FLOOR - 110); ctx.line_to(6000, FLOOR - 110); ink(ctx, 5); ctx.stroke()
    window(ctx, lf)
    picture(ctx, 690, 820, pic_tilt + 0.03 * math.sin(lf * 0.05))
    picture(ctx, 1500, 820, -0.05, hx('8fd06a'))
    picture(ctx, 1760, 860, 0.04, hx('ff8ab8'))
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('c9874e')); ctx.fill()
    for k in range(-10, 40):
        ctx.move_to(k * 150, FLOOR); ctx.line_to(k * 150 - 140, FLOOR + 600)
    setc(ctx, hx('b5743e')); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-3000, FLOOR); ctx.line_to(6000, FLOOR); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 900, FLOOR + 150, 560, 96); fl(ctx, hx('7fd88a'), 6)
    ellipse(ctx, 900, FLOOR + 150, 470, 72); setc(ctx, hx('c6f2c8')); ctx.fill()
    sofa(ctx)
    sideboard(ctx)
    ctx.rectangle(-3000, -3000, 9000, CEIL + 3000); setc(ctx, hx('fff6e6')); ctx.fill()
    ctx.move_to(-3000, CEIL); ctx.line_to(6000, CEIL); ink(ctx, 6); ctx.stroke()
    garland(ctx, lf)


# ------------------------------------------------------------------ people
def stand(ctx, ch, x, k, p, f_=1):
    return draw(ctx, x, GND - 186 * k, k, f_, ch, p)


def kid(ctx, x, p, f_=1, hop=0.0):
    return draw(ctx, x, GND - 186 * KK - hop, KK, f_, KID, p)


SEAT = 1360


def sit(ch, k, x, ctx, f_=1, **kw):
    p = P(torso=2, lsh=30, lel=-100, rsh=34, rel=-104, lhip=86, lkn=-86, rhip=88, rkn=-88); p.update(kw)
    return draw_hip(ctx, x, SEAT, k, f_, ch, p)


# ------------------------------------------------------------------ shot 1: hook
def hook_scene(ctx, f, lf, z=None):
    z = z or 1.32 + 0.04 * eio(pop(lf, 0, 54))
    ctx.save(); cam(ctx, 880, 1230, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    room(ctx, lf)
    calendar(ctx, CALX, CALB, 1.0, 24, lf)
    dog(ctx, 1230, GND + 20, 0.45, -1, lf)
    d = kid(ctx, 730, P(eye='shock', mouth='flat', torso=-4, head=-6, lsh=150, lel=-30, rsh=40, rel=-60, lhip=-10, rhip=10))
    stuffed(ctx, d, 1.0, KID)
    treat(ctx, d['front'][0], d['front'][1] - 10, 22, 2, 0.3)
    sweat(ctx, d['head'][0] - d['R'] * 1.05, d['head'][1] - d['R'] * 0.4, lf, 0.9)
    for k in range(4):                                         # foil wrappers on the floor
        treat(ctx, 600 + k * 90, FLOOR + 40 + 14 * (k % 2), 16, k % 3, k * 0.7)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook_scene(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"I only opened", "ONE!\"", WHITE, t, 120, col2=RED, y=1470)


# ------------------------------------------------------------------ shot 2: door 1 -> montage -> Mom calls
def door_one(ctx, f, il):
    # il 0..60: 4 *CLICK!* door 1 opens; 14 chocolate to mouth *NOM!*; 22 "Yum!"; 34 door 2 glows + wiggles "...just ONE more."
    opened = set() if il < 4 else {0}
    eaten = set() if il < 14 else {0}
    ctx.save(); cam(ctx, 950, 1180, 1.42, 0, shake_at(il, [4], 5, 6), f)
    room(ctx, il)
    calendar(ctx, CALX, CALB, 1.0, opened, il, eaten=eaten, glow=1 if il >= 30 else -1, wig=1.0)
    dog(ctx, 1230, GND + 20, 0.45, -1, il)
    if il < 14:
        d = kid(ctx, 760, P(eye='happy', mouth='open', lsh=40, lel=-10, rsh=95, rel=-10, head=-10))
    else:
        u = pop(il, 14, 20)
        d = kid(ctx, 760, P(eye='happy' if il < 30 else 'normal', mouth='grin' if 20 < il < 30 else 'smile', lsh=40, lel=-10, rsh=lerp(95, 150, u), rel=lerp(-10, -150, u),
                             head=-10 if il < 30 else -22))
        if il < 18:
            treat(ctx, d['front'][0], d['front'][1] - 10, 20, 1, 0)
        stuffed(ctx, d, 0.25, KID, smear=il >= 30)
    if 4 <= il < 14:
        dx, dy = door_pos(0)
        treat(ctx, lerp(dx, d['front'][0], pop(il, 8, 14)), lerp(dy, d['front'][1], pop(il, 8, 14)), 20, 1, 0)
    ctx.restore()
    if il < 14:
        label(ctx, "*CLICK!*", 540, 640, 120, GOLD, -0.05, pop(il, 4, 7))
    elif il < 30:
        label(ctx, "*NOM!*", 540, 640, 130, CHOC, 0.05, pop(il, 14, 17))
        label(ctx, "\"Yum!\"", 540, 1470, 130, WHITE, -0.03, pop(il, 20, 23))
    else:
        label(ctx, "*ting!*", 760, 640, 90, GOLD, 0.05, pop(il, 30, 33))
        label2(ctx, "\"...just", "ONE more.\"", WHITE, pop(il, 36, 40), 120, col2=GOLD, y=1470)


POPS = [6, 14, 21, 27, 33, 38, 43, 48, 52, 56, 60, 63]


def montage(ctx, f, il):
    # il 0..90 Dutch tilt: doors pop open in bursts, treats fly into his mouth, cheeks inflate; 72 *GULP*
    nopen = 1 + sum(2 for p_ in POPS if il >= p_)
    nopen = min(24, nopen if il < 66 else 24)
    amt = clamp(0.25 + 0.75 * (nopen - 1) / 23)
    rot = -8 if il < 66 else lerp(-8, 0, eio(pop(il, 66, 72)))
    z = lerp(1.35, 1.55, eio(il / 90))
    ctx.save(); cam(ctx, 960, 1180, z, rot, shake_at(il, POPS[::3] + [72], 6, 6), f)
    room(ctx, il)
    calendar(ctx, CALX, CALB, 1.0, nopen, il)
    dog(ctx, 1230, GND + 20, 0.45, -1, il)
    if il < 66:
        for g in (2, 1, 0):
            ctx.push_group()
            w = math.sin((il - g) * 2.4)
            d = kid(ctx, 760 + 14 * w, P(eye='happy', mouth='smile', torso=6 * w, lsh=60 + 40 * w, lel=-10, rsh=120 - 40 * w, rel=-60, head=-10 + 6 * w))
            stuffed(ctx, d, amt, KID)
            ctx.pop_group_to_source(); ctx.paint_with_alpha(1.0 if g == 0 else 0.25)
        # flying treats
        for j, p_ in enumerate(POPS):
            u = pop(il, p_, p_ + 7)
            if 0 < u < 1:
                dx, dy = door_pos(min(23, 2 + 2 * j))
                hx_, hy_ = d['head'][0], d['head'][1] + d['R'] * 0.4
                treat(ctx, lerp(dx, hx_, u), lerp(dy, hy_, u) - 140 * 4 * u * (1 - u), 20, j % 3, il * 0.4)
    else:
        d = kid(ctx, 760, P(eye='shock' if il < 72 else 'happy', mouth='flat', lsh=20, lel=-20, rsh=20, rel=-20, head=-6))
        stuffed(ctx, d, 1.0, KID)
    ctx.restore()
    if il < 66:
        for j, p_ in enumerate(POPS[:9]):
            if il < p_ + 10:
                label(ctx, "*POP!*" if j % 2 == 0 else "*NOM!*", 540 + (-170, 170, 0)[j % 3], (560, 680, 800)[j % 3], 100, GOLD if j % 2 == 0 else CHOC,
                      (-0.08, 0.07, -0.03)[j % 3], pop(il, p_, p_ + 3))
        label2(ctx, "\"...and ONE more...", "and ONE more...\"", WHITE, pop(il, 4, 8), 96, col2=GOLD, y=1470)
    else:
        label(ctx, "*GULP.*", 540, 660, 130, CHOC, -0.04, pop(il, 72, 75))


def mom_calls(ctx, f, il):
    # il 0..60: Mom in the doorway (left) "Sweetie... did you open door ONE?" -> 14 kid jumps in front of the calendar, arms spread "Mm-HMM!"
    u = eout(pop(il, 6, 14))
    ctx.save(); cam(ctx, 820, 1200, 1.18, 0, shake_at(il, [14], 6, 6), f)
    room(ctx, il)
    calendar(ctx, CALX, CALB, 1.0, 24, il)
    dog(ctx, 1230, GND + 20, 0.45, -1, il)
    m = stand(ctx, MOM, lerp(220, 330, eout(pop(il, 0, 12))), KM, P(eye='normal', mouth='smile', lsh=20, lel=-20, rsh=60, rel=-120, head=6))
    mug(ctx, m['front'][0] + 10, m['front'][1] - 20, 0.5)
    hop = 120 * 4 * u * (1 - u)
    d = kid(ctx, lerp(760, 1010, u), P(eye='shock' if il < 30 else 'happy', mouth='flat', lsh=lerp(20, 120, u), lel=0, rsh=lerp(20, 120, u), rel=0, head=0), f_=-1, hop=hop)
    stuffed(ctx, d, 1.0, KID, f_=-1)
    if il > 20:
        sweat(ctx, d['head'][0] + d['R'] * 1.0, d['head'][1] - d['R'] * 0.4, il, 0.9)
    ctx.restore()
    if il < 26:
        label2(ctx, "\"Sweetie... did you", "open door ONE?\"", WHITE, pop(il, 0, 4), 98, col2=PURPLE, y=1470)
    else:
        label(ctx, "\"Mm-HMM!\"", 540, 1470, 140, RED, -0.03, pop(il, 26, 29))
        label(ctx, "*nods*", 540, 640, 90, WHITE, 0.04, pop(il, 28, 31))


def s2(ctx, f):
    lf = f - 54
    if lf < 60:
        door_one(ctx, f, lf)
    elif lf < 150:
        montage(ctx, f, lf - 60)
    else:
        mom_calls(ctx, f, lf - 150)


# ------------------------------------------------------------------ shot 3: Mom leans round
def reveal(ctx, f, il):
    # il 0..56: low angle, Mom leans round the kid (kid stretched to cover), sees every door open; 14 *gasp* ; 22 "...ALL 24?!"
    ctx.save(); cam(ctx, 1000, 1150, 1.3, 0, shake_at(il, [14], 8, 8), f)
    room(ctx, il)
    calendar(ctx, CALX, CALB, 1.0, 24, il)
    lean = eio(pop(il, 2, 12))
    m = stand(ctx, MOM, 1330, KM, P(eye='normal' if il < 14 else 'shock', mouth='smile' if il < 14 else 'open', torso=-24 * lean, head=-14 * lean,
                                    lsh=20, lel=-20, rsh=60, rel=-120), f_=-1)
    mug(ctx, m['front'][0] - 10, m['front'][1] - 20, 0.5)
    d = kid(ctx, 1000, P(eye='shock', mouth='flat', lsh=125, lel=0, rsh=125, rel=0, rot=6 * math.sin(il * 0.6)), f_=1)
    stuffed(ctx, d, 1.0, KID)
    sweat(ctx, d['head'][0] - d['R'] * 1.0, d['head'][1] - d['R'] * 0.4, il, 0.9)
    if il >= 14:
        for k, (sx, sy) in enumerate(((CALX - 240, 900), (CALX + 240, 940), (CALX, 830))):
            sparkle(ctx, sx, sy, 20 + 6 * math.sin(il * 0.5 + k), GOLD)
    ctx.restore()
    if il < 22:
        label(ctx, "*gasp!*", 540, 640, 110, PURPLE, -0.05, pop(il, 14, 17))
    else:
        label(ctx, "\"...ALL 24?!\"", 540, 1470, 140, RED, -0.03, pop(il, 22, 25))


def s3(ctx, f):
    reveal(ctx, f, f - 264)


# ------------------------------------------------------------------ shot 4: the one close-up
def ecu(ctx, f, il):
    # il 0..80: kid face, stuffed cheeks, chocolate smears, smug: "...it's called PLANNING AHEAD."
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eio(il / 80), 0, 2 + shake_at(il, [0], 6, 8), f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('ffe0ec')); ctx.fill()
    rays(ctx, 540, 900, 240, 1500, il * 0.02, col=(1, 1, 1), a=0.35, n=16)
    p = P(eye='smug' if il > 24 else 'shock', mouth='flat')
    face(ctx, KID, p, 540, 940, 200, 0.0)
    R = 200 * 1.0
    d = {'head': (540, 940), 'R': R}
    stuffed(ctx, d, 1.0, KID)
    for k in range(6):
        treat(ctx, 540 + 330 * math.cos(il * 0.04 + k * 1.05), 940 + 300 * math.sin(il * 0.04 + k * 1.05), 26, k % 3, il * 0.05 + k)
    ctx.restore()
    label2(ctx, "\"...it's called", "PLANNING AHEAD.\"", WHITE, pop(il, 8, 12), 118, col2=GOLD, y=1470)


def s4(ctx, f):
    ecu(ctx, f, f - 320)


# ------------------------------------------------------------------ shot 5: twist -> loop
def dad_turn(ctx, f, il):
    # il 0..90: wide: Mom turns to Dad on the sofa (his back to us -> turns), 30 Dad turns: cheeks stuffed, his calendar all open "...mm-HMM?"
    ctx.save(); cam(ctx, 1330, 1200, lerp(1.05, 1.15, eio(il / 90)), 0, shake_at(il, [30], 6, 8), f)
    room(ctx, il)
    calendar(ctx, CALX, CALB, 1.0, 24, il)
    m = stand(ctx, MOM, 1210, KM, P(eye='glare' if il < 30 else 'shock', mouth='open' if il < 30 else 'scream', lsh=20, lel=-20, rsh=100, rel=-30), f_=1)
    d = kid(ctx, 1020, P(eye='happy' if il < 30 else 'shock', mouth='flat', lsh=20, lel=-20, rsh=20, rel=-20), f_=1)
    stuffed(ctx, d, 1.0, KID)
    turned = il >= 30
    dd = sit(DAD, KD, 1640, ctx, f_=-1 if turned else 1, eye='normal' if not turned else 'shock', mouth='flat', head=0, rsh=40, rel=-100, lsh=40, lel=-100)
    if turned:
        stuffed(ctx, dd, 1.0, DAD, f_=-1)
        calendar(ctx, 1640, SEAT + 20, 0.42, 24, il)
    else:
        calendar(ctx, 1700, SEAT + 20, 0.42, 24, il)
    dog(ctx, 1400, GND + 20, 0.45, 1, il)
    ctx.restore()
    card(ctx, 'p2', il, 4)
    if il < 30:
        label(ctx, "\"HONEY! Look at THIS!\"", 540, 1470, 100, WHITE, -0.03, pop(il, 8, 11))
    else:
        label(ctx, "\"...mm-HMM?\"", 540, 1470, 140, GOLD, -0.03, pop(il, 32, 35))


def confiscate(ctx, f, il):
    # il 0..60: Mom holds both calendars up, kid + Dad sad on the sofa: "NO. MORE. CHOCOLATE."
    ctx.save(); cam(ctx, 1380, 1260, 1.2, 0, shake_at(il, [4], 8, 8), f)
    room(ctx, il)
    m = stand(ctx, MOM, 1140, KM, P(eye='glare', mouth='scream' if il % 20 < 12 else 'open', lsh=60, lel=-10, rsh=60, rel=-10), f_=1)
    calendar(ctx, m['back'][0] - 70, m['back'][1] + 110, 0.36, 24, il)
    calendar(ctx, m['front'][0] + 70, m['front'][1] + 110, 0.36, 24, il)
    dd = sit(DAD, KD, 1720, ctx, f_=-1, eye='normal', mouth='frown', head=8)
    stuffed(ctx, dd, 0.6, DAD, f_=-1)
    kd = sit(KID, KK, 1500, ctx, f_=-1, eye='normal', mouth='frown', head=8)
    stuffed(ctx, kd, 0.6, KID, f_=-1)
    dog(ctx, 900, GND + 20, 0.45, 1, il)
    ctx.restore()
    label2(ctx, "\"NO. MORE.", "CHOCOLATE.\"", WHITE, pop(il, 4, 8), 130, col2=RED, y=1470)


def split(ctx, f, il):
    # il 0..60: split: left = kid + Dad sad on the sofa; right = kitchen, Mom opens HER calendar: "...just ONE." -> *nom*
    ctx.save(); ctx.rectangle(0, 0, W / 2 - 6, H); ctx.clip()
    cam(ctx, 1620, 1270, 0.95, 0, 0, f, sx=W / 4)
    room(ctx, il)
    dd = sit(DAD, KD, 1720, ctx, f_=-1, eye='normal', mouth='frown', head=8)
    stuffed(ctx, dd, 0.6, DAD, f_=-1)
    kd = sit(KID, KK, 1500, ctx, f_=-1, eye='normal', mouth='frown', head=8)
    stuffed(ctx, kd, 0.6, KID, f_=-1)
    ctx.restore()
    ctx.save(); ctx.rectangle(W / 2 + 6, 0, W / 2, H); ctx.clip()
    cam(ctx, 600, 1230, 1.2, 0, shake_at(il, [30], 5, 6), f, sx=W * 0.75)
    ctx.rectangle(-2000, -2000, 5000, 5000); setc(ctx, hx('dff5e6')); ctx.fill()
    for k in range(-6, 12):                                     # kitchen tiles
        for j in range(8):
            if (k + j) % 2 == 0:
                ctx.rectangle(k * 90, 900 + j * 90, 90, 90); setc(ctx, hx('c6ecd2')); ctx.fill()
    rect_r(ctx, 150, 1330, 900, 260, 12); fl(ctx, hx('ffb27a'), 7)                     # counter
    rect_r(ctx, 130, 1310, 940, 30, 10); fl(ctx, hx('a0603a'), 6)
    rect_r(ctx, 200, 640, 360, 220, 12); fl(ctx, hx('ffe39a'), 6)                       # cupboard
    calendar(ctx, 760, 1310, 0.5, 23 if il < 30 else 23, il, eaten=set(range(22)) if il < 30 else set(range(23)))
    m = stand(ctx, MOM, 480, KM, P(eye='smug' if il < 30 else 'happy', mouth='smile' if il < 30 else 'flat', lsh=20, lel=-20, rsh=70, rel=-100, head=-8), f_=1)
    if il >= 30:
        stuffed(ctx, m, 0.7, MOM)
    ctx.restore()
    ctx.rectangle(W / 2 - 6, 0, 12, H); setc(ctx, WHITE); ctx.fill()
    if il < 30:
        label(ctx, "\"...just ONE.\"", 540, 1470, 130, WHITE, -0.03, pop(il, 4, 7))
    else:
        label(ctx, "*nom.*", 810, 560, 120, CHOC, 0.05, pop(il, 30, 33))
        label(ctx, "\"...just ONE.\"", 540, 1470, 130, WHITE, -0.03, 1)


def s5(ctx, f):
    lf = f - 400
    if lf < 90:
        dad_turn(ctx, f, lf)
    elif lf < 140:
        confiscate(ctx, f, lf - 90)
    elif lf < 230:
        split(ctx, f, lf - 140)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (54, s2), (264, s3), (320, s4), (400, s5)]
CUTS = (54, 114, 204, 264, 320, 400, 490, 540, 630)


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
                              "-i", "out/advent_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
