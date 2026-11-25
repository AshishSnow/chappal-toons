"""'I can dress MYSELF!'. Original, general-audience comedy short, 22s.
Hook:   kid's bedroom medium shot: kid with a T-shirt stuck on his head, arms flailing, Mom frozen in the doorway.
        "I CAN DO IT MYSELF!!" + caption "WHEN KIDS DRESS THEMSELVES:".
Beat 1: Mom "Need help, sweetie?" -> kid stomps "NO! MYSELF!" *STOMP* -> push-in, shirt wriggles *wriggle wriggle*
        -> *POP!* head out, shirt on backwards, a sleeve sticking up like a unicorn horn -> "...DONE!"
Beat 2: Dutch-tilt montage: both legs in one pant leg, hop hop *BOING BOING* *THUD!* -> one rain boot + one flipper
        *squeak* -> swim goggles *SNAP!* + cape *FWOOSH!* + tutu -> low-angle reveal *TA-DAAA!* "READY!"
Turn:   the one close-up: Mom holding in a laugh "It's... PERFECT, sweetie."
Twist:  PLOT TWIST: DAD DRESSED HIMSELF TOO. split screen kid "Ready for SCHOOL!" | Dad (tie on head, socks on hands,
        a flipper) "Ready for WORK!" -> high-five *CLAP!* -> Mom "...Change. BOTH of you." -> both dive into the
        clothes pile *FWUMP!* -> both pop up with shirts stuck on their heads "WE CAN DO IT OURSELVES!!" -> hook loop."""
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
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
TEE = hx('3fd6a0')          # the new T-shirt (mint)
KID0 = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ffffff'), pants=hx('ffb3d1'), shoes=hx('ffe08a'))   # vest + PJ bottoms
KID1 = dict(KID0, shirt=TEE)                                                                                   # shirt on (backwards)
KID2 = dict(KID1, pants=hx('3d7bff'))                                                                          # jeans on
MOM = dict(doodle.MOM_G, shirt=hx('ff7a59'))
DAD = dict(doodle.DAD, shirt=hx('8a6cff'), pants=hx('3a4a8a'))
N = 660
FLOOR, GND = 1560, 1590
MOMX, KIDX, DADX = 800, 1110, 1400
KMOM, KKID, KDAD = 1.02, 0.95, 1.08
CX, CY, CZ = 1080, 1250, 1.2

CAPS = {'p1': [[("WHEN KIDS ", OUT), ("DRESS ", RED), ("THEMSELVES:", PURPLE)]],
        'p2': [[("PLOT TWIST:", RED)], [("DAD DRESSED ", OUT), ("HIMSELF", BLUE), (" TOO.", OUT)]]}
scenes13.CAPS = CAPS
card = _card13


def S_(k):
    return 1.35 * k


def TL_(k):
    return 104 * S_(k) * doodle.CUTE_BODY


# ------------------------------------------------------------------ set: kid's bedroom
def room(ctx, lf):
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, hx('d6efff')); ctx.fill()
    rnd = random.Random(97)
    for k in range(70):   # clouds + stars wallpaper
        x, y = rnd.uniform(300, 1950), rnd.uniform(220, 1250)
        if k % 3 == 0:
            for dx, r in ((-14, 12), (0, 17), (15, 12)):
                ellipse(ctx, x + dx, y, r, r * 0.8); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()
        else:
            sparkle(ctx, x, y, 9, hx('ffe39a'))
    # skirting board + floor
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('e0a86e')); ctx.fill()
    for i in range(-20, 40):
        ctx.move_to(i * 150, FLOOR); ctx.line_to(i * 150 - 60, FLOOR + 400); ink(ctx, 2); ctx.stroke()
    rect_r(ctx, -3000, FLOOR - 26, 9000, 26, 4); fl(ctx, WHITE, 4)
    # door (left) with the hallway behind
    dx0, dy0, dw, dh = 600, 980, 330, 590
    rect_r(ctx, dx0 - 24, dy0 - 24, dw + 48, dh + 40, 10); fl(ctx, WHITE, 6)
    ctx.rectangle(dx0, dy0, dw, dh - 10); setc(ctx, hx('f6d9b0')); ctx.fill()
    rect_r(ctx, dx0 + 90, dy0 + 120, 120, 150, 8); fl(ctx, hx('ffe9c8'), 3)     # hallway picture
    poly(ctx, [(dx0, dy0), (dx0 - 70, dy0 + 40), (dx0 - 70, dy0 + dh - 30), (dx0, dy0 + dh - 10)]); fl(ctx, hx('ffcf7a'), 5)
    ellipse(ctx, dx0 - 52, dy0 + dh * 0.55, 10, 10); fl(ctx, GOLD, 3)
    # window with morning sun + tree
    x, y, w, h = 1260, 620, 300, 380
    rect_r(ctx, x, y, w, h, 18); fl(ctx, hx('9fe0ff'), 8)
    ctx.save(); rect_r(ctx, x, y, w, h, 18); ctx.clip()
    ellipse(ctx, x + 220, y + 90, 46, 46); fl(ctx, hx('ffd84a'), 4)
    for a in range(8):
        aa = a * math.pi / 4 + lf * 0.02
        ctx.move_to(x + 220 + 58 * math.cos(aa), y + 90 + 58 * math.sin(aa)); ctx.line_to(x + 220 + 76 * math.cos(aa), y + 90 + 76 * math.sin(aa))
        setc(ctx, hx('ffb020')); ctx.set_line_width(6); ctx.stroke()
    rect_r(ctx, x + 60, y + 240, 30, 180, 8); fl(ctx, hx('8a5a3a'), 4)
    ellipse(ctx, x + 75, y + 220, 80, 70); fl(ctx, hx('5ccf6a'), 4)
    ctx.restore()
    ctx.move_to(x + w / 2, y); ctx.line_to(x + w / 2, y + h); ctx.move_to(x, y + h * 0.45); ctx.line_to(x + w, y + h * 0.45); ink(ctx, 7); ctx.stroke()
    for sd in (0, 1):   # curtains
        cx_ = x - 30 if sd == 0 else x + w + 30
        ctx.new_path(); ctx.move_to(cx_ - 40, y - 30); ctx.line_to(cx_ + 40, y - 30)
        ctx.curve_to(cx_ + 20, y + 150, cx_ + 46, y + 300, cx_ + 30, y + h + 20); ctx.line_to(cx_ - 30, y + h + 20)
        ctx.curve_to(cx_ - 46, y + 300, cx_ - 20, y + 150, cx_ - 40, y - 30); ctx.close_path(); fl(ctx, hx('ffa6c8'), 5)
        for j in range(4):
            ellipse(ctx, cx_ - 16 + j * 10, y + 60 + j * 90, 7, 7); setc(ctx, WHITE); ctx.fill()
    rect_r(ctx, x - 90, y - 44, w + 180, 18, 8); fl(ctx, hx('b97a4a'), 4)
    # rocket poster (original doodle)
    px, py = 960, 640
    rect_r(ctx, px, py, 200, 260, 8); fl(ctx, hx('2a2a6a'), 6)
    for k in range(9):
        sparkle(ctx, px + 20 + (k * 53) % 170, py + 30 + (k * 71) % 210, 6, YEL)
    ctx.save(); ctx.translate(px + 100, py + 140); ctx.rotate(0.4)
    ellipse(ctx, 0, 0, 30, 70); fl(ctx, WHITE, 4)
    ellipse(ctx, 0, -14, 14, 14); fl(ctx, CYAN, 3)
    poly(ctx, [(-30, 30), (-50, 70), (-20, 56)]); fl(ctx, RED, 3); poly(ctx, [(30, 30), (50, 70), (20, 56)]); fl(ctx, RED, 3)
    poly(ctx, [(-14, 70), (0, 110 + 8 * math.sin(lf)), (14, 70)]); fl(ctx, ORANGE, 3)
    ctx.restore()
    # bunting
    for k in range(9):
        gx = 1000 + k * 60; gy = 470 + 30 * math.sin(k / 8 * math.pi)
        poly(ctx, [(gx - 22, gy), (gx + 22, gy), (gx, gy + 44)]); fl(ctx, (RED, GOLD, MINT, BLUE, PINK)[k % 5], 3)
    ctx.move_to(990, 470); ctx.curve_to(1150, 520, 1350, 520, 1510, 470); ink(ctx, 3); ctx.stroke()
    # bed (right) with a star blanket
    rect_r(ctx, 1560, 1180, 50, 400, 10); fl(ctx, hx('b97a4a'), 5)
    rect_r(ctx, 1580, 1340, 600, 160, 18); fl(ctx, hx('5a7bff'), 5)
    for k in range(6):
        sparkle(ctx, 1640 + k * 70, 1400 + (k % 2) * 40, 14, YEL)
    ellipse(ctx, 1680, 1320, 80, 36); fl(ctx, WHITE, 4)
    # rug
    ellipse(ctx, 1110, FLOOR + 40, 380, 50); fl(ctx, hx('ffd36a'), 5)
    ellipse(ctx, 1110, FLOOR + 40, 300, 36); ctx.set_line_width(5); setc(ctx, hx('ff8a5c')); ctx.stroke()


def dresser(ctx, lf, spill=0.0):
    """chest of drawers behind-left of the kid, drawers open with clothes spilling"""
    x, y, w, h = 840, 1240, 220, 330
    rect_r(ctx, x, y, w, h, 12); fl(ctx, hx('f2a65a'), 6)
    for j in range(3):
        o = 18 * (j % 2 == 0)
        rect_r(ctx, x + 14 - o * 0.3, y + 20 + j * 100 + o * 0.2, w - 28, 84, 8); fl(ctx, hx('ffc07a'), 4)
        ellipse(ctx, x + w / 2, y + 62 + j * 100, 10, 8); fl(ctx, hx('8a5a3a'), 2)
        if j % 2 == 0:   # dangling sock / sleeve
            c = (RED, BLUE, GOLD)[j]
            ctx.new_path(); ctx.move_to(x + 60 + j * 30, y + 30 + j * 100)
            ctx.curve_to(x + 70 + j * 30, y + 80 + j * 100, x + 50 + j * 30 + 6 * math.sin(lf * 0.2), y + 100 + j * 100, x + 66 + j * 30, y + 130 + j * 100)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND); setc(ctx, INK); ctx.set_line_width(26); ctx.stroke_preserve(); setc(ctx, c); ctx.set_line_width(18); ctx.stroke()
    # lamp + little plant on top
    rect_r(ctx, x + 30, y - 60, 12, 60, 4); fl(ctx, WHITE, 3)
    poly(ctx, [(x + 2, y - 60), (x + 70, y - 60), (x + 56, y - 120), (x + 16, y - 120)]); fl(ctx, hx('ffd36a'), 4)
    rect_r(ctx, x + 150, y - 50, 50, 50, 8); fl(ctx, hx('ff8a5c'), 4)
    for a in (-0.6, 0, 0.6):
        ellipse(ctx, x + 175 + 26 * math.sin(a), y - 70 - 16 * math.cos(a), 10, 24, a); fl(ctx, GREEN, 3)


def pile(ctx, x, y, s=1.0, lf=0, burst=0.0):
    rnd = random.Random(5)
    cols = (RED, BLUE, GOLD, PINK, MINT, PURPLE, ORANGE, CYAN)
    for k in range(11):
        bx = x + rnd.uniform(-110, 110) * s; by = y - rnd.uniform(0, 70) * s - (k > 6) * 30 * s
        if burst > 0:
            a = rnd.uniform(-2.6, -0.5); d = 420 * burst
            bx += math.cos(a) * d; by += math.sin(a) * d + 900 * burst * burst
        ellipse(ctx, bx, by, rnd.uniform(40, 60) * s, rnd.uniform(22, 32) * s, rnd.uniform(-0.5, 0.5) + burst * 6 * k)
        fl(ctx, cols[k % len(cols)], 4)
        ctx.new_path(); ctx.move_to(bx - 20 * s, by - 4 * s); ctx.line_to(bx + 20 * s, by + 2 * s); setc(ctx, (1, 1, 1, 0.55)); ctx.set_line_width(5 * s); ctx.stroke()


# ------------------------------------------------------------------ outfit pieces
def body_xf(ctx, x, k, dy=0, rot=0, f=1):
    S = S_(k); ground = GND + dy
    ctx.translate(x, ground - 68 * S); ctx.rotate(math.radians(rot) * f)
    return S


def shirt_on_head(ctx, d, col, lf, wob=1.0):
    """a T-shirt pulled down over the head like a hood, sleeves flopping out as ears"""
    x, y = d['head']; R = d['R']
    w = math.sin(lf * 0.7) * wob
    ctx.save(); ctx.translate(x, y); ctx.rotate(0.12 * w)
    for sd in (-1, 1):   # floppy sleeves sticking out of the bunched-up shirt
        ctx.save(); ctx.translate(sd * R * 0.9, -R * 1.45); ctx.rotate(-sd * (1.75 + 0.35 * math.sin(lf * 0.9 + sd)))
        rect_r(ctx, -R * 0.26, -R * 0.1, R * 0.52, R * 0.7, R * 0.14); fl(ctx, dark(col, 0.92), 4)
        ctx.restore()
    ctx.new_path(); ctx.move_to(-R * 1.08, -R * 0.28)
    ctx.curve_to(-R * 1.25, -R * 1.2, -R * 1.0, -R * 1.9, -R * 0.75, -R * 2.25 - 10 * w)
    ctx.line_to(R * 0.75, -R * 2.25 + 10 * w)
    ctx.curve_to(R * 1.0, -R * 1.9, R * 1.25, -R * 1.2, R * 1.08, -R * 0.28)
    ctx.curve_to(R * 0.6, -R * 0.42, -R * 0.6, -R * 0.42, -R * 1.08, -R * 0.28); ctx.close_path()
    fl(ctx, col, 4)
    ellipse(ctx, 0, -R * 2.25, R * 0.76, R * 0.12); fl(ctx, dark(col, 0.8), 3)   # bottom hem opening on top
    for j in range(3):   # stripes
        yy = -R * (0.8 + j * 0.42)
        ctx.new_path(); ctx.move_to(-R * 0.95, yy); ctx.curve_to(-R * 0.3, yy - 14, R * 0.3, yy - 14, R * 0.95, yy)
        setc(ctx, (1, 1, 1, 0.6)); ctx.set_line_width(R * 0.08); ctx.stroke()
    ellipse(ctx, 0, -R * 0.34, R * 0.95, R * 0.12); ink(ctx, 4); ctx.stroke()   # hem
    ctx.restore()


def sleeve_horn(ctx, d, col, lf):
    x, y = d['head']; R = d['R']
    ctx.save(); ctx.translate(x + R * 0.55, y - R * 0.95); ctx.rotate(0.35 + 0.08 * math.sin(lf * 0.6))
    rect_r(ctx, -R * 0.2, -R * 0.75, R * 0.4, R * 0.8, R * 0.12); fl(ctx, col, 4)
    ctx.restore()


def tag(ctx, x, k, f=1):
    S = S_(k)
    ctx.save(); body_xf(ctx, x, k)
    rect_r(ctx, -10 * S, -TL_(k) + 4 * S, 20 * S, 18 * S, 3); fl(ctx, WHITE, 3)
    ctx.restore()


def legs_in_one(ctx, x, k, dy, rot, lf, col):
    S = S_(k)
    ctx.save(); body_xf(ctx, x, k, dy, rot)
    fl_ = math.sin(lf * 0.8)
    ctx.new_path(); ctx.move_to(22 * S, 0); ctx.curve_to(60 * S, 10 * S + 10 * fl_, 80 * S, 40 * S, 96 * S, 30 * S + 16 * fl_)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); setc(ctx, INK); ctx.set_line_width(40 * S); ctx.stroke_preserve(); setc(ctx, col); ctx.set_line_width(32 * S); ctx.stroke()
    rect_r(ctx, -36 * S, -10 * S, 72 * S, 74 * S, 20 * S); fl(ctx, col, 4)
    ctx.restore()


def boots(ctx, x, k, dy=0, rot=0):
    S = S_(k)
    ctx.save(); body_xf(ctx, x, k, dy, rot)
    rect_r(ctx, -46 * S, 40 * S, 34 * S, 36 * S, 8 * S); fl(ctx, hx('ffd23f'), 4)       # rain boot
    ellipse(ctx, -24 * S, 76 * S, 26 * S, 9 * S); fl(ctx, hx('ffb020'), 3)
    ctx.new_path(); ctx.move_to(12 * S, 62 * S); ctx.line_to(84 * S, 66 * S); ctx.line_to(94 * S, 84 * S); ctx.line_to(10 * S, 84 * S); ctx.close_path()
    fl(ctx, hx('22c06a'), 4)                                                              # flipper
    for j in range(3):
        ctx.move_to(40 * S + j * 16 * S, 70 * S); ctx.line_to(44 * S + j * 16 * S, 82 * S); ink(ctx, 3); ctx.stroke()
    ctx.restore()


def tutu(ctx, x, k, dy=0):
    S = S_(k)
    ctx.save(); body_xf(ctx, x, k, dy)
    for j in range(9):
        a = math.pi * j / 8
        ellipse(ctx, -60 * S * math.cos(a), 2 * S + 8 * S * math.sin(a), 22 * S, 16 * S); fl(ctx, PINK, 3)
    ctx.restore()


def cape(ctx, x, k, lf, col=RED, dy=0):
    S = S_(k); TL = TL_(k)
    ctx.save(); body_xf(ctx, x, k, dy)
    fl_ = math.sin(lf * 0.5)
    ctx.new_path(); ctx.move_to(-40 * S, -TL + 14 * S); ctx.line_to(40 * S, -TL + 14 * S)
    ctx.curve_to(70 * S, -20 * S, 100 * S + 20 * fl_ * S, 30 * S, 110 * S + 24 * fl_ * S, 60 * S)
    ctx.curve_to(40 * S, 70 * S, -40 * S, 74 * S, -90 * S + 10 * fl_ * S, 56 * S)
    ctx.curve_to(-70 * S, 10 * S, -60 * S, -40 * S, -40 * S, -TL + 14 * S); ctx.close_path()
    fl(ctx, col, 4)
    ctx.restore()


def goggles(ctx, d, col=CYAN):
    for e in ('eyeL', 'eyeR'):
        ex, ey = d[e]
        ellipse(ctx, ex, ey, d['R'] * 0.25, d['R'] * 0.22); setc(ctx, (0.7, 0.95, 1, 0.35)); ctx.fill_preserve()
        setc(ctx, INK); ctx.set_line_width(14); ctx.stroke_preserve(); setc(ctx, col); ctx.set_line_width(8); ctx.stroke()
    (ax, ay), (bx, by) = d['eyeL'], d['eyeR']
    ctx.move_to(ax - d['R'] * 0.25, ay); ctx.line_to(ax - d['R'] * 0.9, ay - 6); ctx.move_to(bx + d['R'] * 0.25, by); ctx.line_to(bx + d['R'] * 0.9, by - 6)
    setc(ctx, INK); ctx.set_line_width(12); ctx.stroke()


def tie_on_head(ctx, d, lf):
    x, y = d['head']; R = d['R']
    ctx.save(); ctx.translate(x, y)
    ctx.new_path(); ctx.move_to(-R * 1.0, -R * 0.55); ctx.curve_to(-R * 0.3, -R * 0.75, R * 0.3, -R * 0.75, R * 1.0, -R * 0.55)
    setc(ctx, INK); ctx.set_line_width(R * 0.22); ctx.stroke_preserve(); setc(ctx, RED); ctx.set_line_width(R * 0.15); ctx.stroke()
    ctx.translate(R * 1.0, -R * 0.55); ctx.rotate(-0.9 + 0.2 * math.sin(lf * 0.6))
    poly(ctx, [(0, -R * 0.08), (R * 0.75, -R * 0.14), (R * 0.9, 0), (R * 0.75, R * 0.14), (0, R * 0.08)]); fl(ctx, RED, 4)
    for j in range(2):
        ctx.move_to(R * (0.25 + j * 0.25), -R * 0.1); ctx.line_to(R * (0.35 + j * 0.25), R * 0.1); setc(ctx, GOLD); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def sock_hands(ctx, d):
    for hnd, c in (('front', hx('ff5fa8')), ('back', hx('ffd23f'))):
        hx_, hy = d[hnd]; R = d['R'] * 0.22
        rect_r(ctx, hx_ - R, hy - R * 1.4, R * 2, R * 2.6, R * 0.8); fl(ctx, c, 4)
        for j in range(2):
            ctx.move_to(hx_ - R, hy - R * 0.6 + j * R * 0.7); ctx.line_to(hx_ + R, hy - R * 0.6 + j * R * 0.7); setc(ctx, WHITE); ctx.set_line_width(5); ctx.stroke()


def dad_fit(ctx, x, k, p, lf, dy=0, f_=1):
    d = draw(ctx, x, GND - 186 * k + dy, k, f_, DAD, p)
    tag(ctx, x, k)
    boots(ctx, x, k, dy)
    tie_on_head(ctx, d, lf)
    sock_hands(ctx, d)
    return d


def kid_full(ctx, x, k, p, lf, dy=0, f_=1, rot_cape=True):
    if rot_cape:
        cape(ctx, x, k, lf, RED, dy)
    d = draw(ctx, x, GND - 186 * k + dy, k, f_, KID2, p)
    tutu(ctx, x, k, dy)
    boots(ctx, x, k, dy)
    tag(ctx, x, k)
    sleeve_horn(ctx, d, TEE, lf)
    goggles(ctx, d)
    return d


def stand(ctx, ch, x, k, p, f_=1, dy=0):
    return draw(ctx, x, GND - 186 * k + dy, k, f_, ch, p)


def mom(ctx, p, f_=1):
    return stand(ctx, MOM, MOMX, KMOM, p, f_)


FLAIL = lambda lf, **kw: P(lsh=150 + 25 * math.sin(lf * 1.1), lel=-40 + 30 * math.sin(lf * 1.3), rsh=150 + 25 * math.sin(lf * 1.2 + 1),
                          rel=-40 + 30 * math.sin(lf * 0.9 + 2), **kw)


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = CZ + 0.04 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, CX, CY + 10, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    room(ctx, lf); dresser(ctx, lf)
    mom(ctx, P(eye='shock', mouth='open', lsh=40, lel=-150, rsh=30, rel=-140, head=4))
    hop = -18 * abs(math.sin(lf * 0.35))
    d = stand(ctx, KID0, KIDX, KKID, FLAIL(lf, eye='glare', mouth='scream', head=8 * math.sin(lf * 0.5), lhip=14, rhip=-14), 1, hop)
    shirt_on_head(ctx, d, TEE, lf)
    pile(ctx, 1330, FLOOR + 50, 0.85, lf)
    dog(ctx, 1450, GND + 20, 0.5, -1, lf)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"I CAN DO IT MYSELF!!\"", 540, 1470, 100, WHITE, -0.04, t)
    label(ctx, "*wriggle wriggle*", 540, 600, 78, MINT, 0.04, 1 if lf == f else pop(lf, 2, 5))


# ------------------------------------------------------------------ shot 2: NO HELP -> pop
def beat1(ctx, f, il):
    # il 0..140: 0-30 Mom "Need help?" ; 30 STOMP "NO! MYSELF!" ; 56-100 push-in wriggle ; 100 POP ; 106-140 "...DONE!"
    pin = eio(pop(il, 56, 96))
    d0 = eio(pop(il, 100, 106))
    z = lerp(CZ, 1.75, pin) - 0.35 * d0
    cy = lerp(CY, 1200, pin)
    ctx.save(); cam(ctx, lerp(CX, KIDX, pin), cy, z, 0, shake_at(il, [30, 100], 10, 12), f)
    room(ctx, il); dresser(ctx, il)
    mp = P(eye='smile' if False else 'happy', mouth='smile', lsh=30, lel=-60, rsh=120, rel=-30, head=-4) if il < 30 else \
        P(eye='shock', mouth='open', lsh=40, lel=-150, rsh=30, rel=-140)
    mom(ctx, mp)
    if il < 30:
        d = stand(ctx, KID0, KIDX, KKID, FLAIL(il, eye='glare', mouth='flat', lhip=14, rhip=-14), 1)
        shirt_on_head(ctx, d, TEE, il, 0.6)
    elif il < 100:
        st = (il < 40) * 1.0
        wr = il >= 56
        p = P(eye='glare', mouth='scream', lsh=40, lel=-80, rsh=40, rel=-80, rhip=-40 * st, rkn=10 * st, lhip=6) if not wr else \
            FLAIL(il * 1.6, eye='glare', mouth='scream', head=10 * math.sin(il * 0.9))
        d = stand(ctx, KID0, KIDX + (6 * math.sin(il * 2.1) if wr else 0), KKID, p, 1)
        shirt_on_head(ctx, d, TEE, il * (2 if wr else 1), 1.5 if wr else 0.4)
    else:
        p = P(eye='smug', mouth='grin', lsh=150, lel=-20, rsh=20, rel=-90, head=-6)
        d = stand(ctx, KID1, KIDX, KKID, p, 1)
        tag(ctx, KIDX, KKID)
        sleeve_horn(ctx, d, TEE, il)
        if il < 116:
            for a in range(8):
                aa = a * math.pi / 4
                r0 = 160 + 260 * pop(il, 100, 116)
                ctx.move_to(d['head'][0] + r0 * math.cos(aa), d['head'][1] + r0 * math.sin(aa))
                ctx.line_to(d['head'][0] + (r0 + 50) * math.cos(aa), d['head'][1] + (r0 + 50) * math.sin(aa)); ink(ctx, 7); ctx.stroke()
        else:
            sparkle(ctx, d['head'][0] + 160, d['head'][1] - 140, 26 + 6 * math.sin(il * 0.5), YEL)
    pile(ctx, 1330, FLOOR + 50, 0.85, il)
    dog(ctx, 1450, GND + 20, 0.5, -1, il)
    ctx.restore()
    if il < 30:
        label(ctx, "\"Need help, sweetie?\"", 540, 1470, 100, WHITE, -0.03, pop(il, 2, 6))
    elif il < 56:
        label(ctx, "\"NO! MYSELF!\"", 540, 1470, 130, RED, 0.03, pop(il, 30, 33))
        label(ctx, "*STOMP!*", 540, 600, 110, ORANGE, -0.05, pop(il, 31, 34))
    elif il < 100:
        label(ctx, "*wriggle wriggle*", 540, 1470, 100, MINT, 0.03, pop(il, 58, 62))
    else:
        label(ctx, "*POP!*", 540, 600, 140, GOLD, -0.05, pop(il, 100, 103))
        label(ctx, "\"...DONE!\"", 540, 1470, 130, WHITE, -0.03, pop(il, 108, 112))


def s2(ctx, f):
    beat1(ctx, f, f - 60)


# ------------------------------------------------------------------ shot 3: the outfit montage
def montage(ctx, f, il):
    # il 0..130: 0-50 one pant leg hop hop -> THUD ; 50-80 boots squeak ; 80-104 goggles SNAP + cape FWOOSH ; 104-130 low-angle TA-DAA
    if il < 104:
        j = 0 if il < 50 else (1 if il < 80 else 2)
        rot = (-6, 6, -5)[j]
        z = (1.3, 1.45, 1.35)[j]
        cy = (1290, 1420, 1230)[j]
        ctx.save(); cam(ctx, KIDX, cy, z, rot, shake_at(il, [12, 24, 36, 50, 82, 92], 7, 10), f)
        room(ctx, il); dresser(ctx, il)
        mom(ctx, P(eye='shock', mouth='open', lsh=30, lel=-150, rsh=20, rel=-140))
        if j == 0:
            hop = -90 * abs(math.sin(il * math.pi / 12)) if il < 36 else 0
            fall = eio(pop(il, 36, 44))
            rot_b = 0 if il < 36 else -80 * fall
            dyy = hop + 60 * fall
            p = FLAIL(il, eye='shock' if il >= 36 else 'glare', mouth='scream', lhip=2, rhip=-2, lkn=0, rkn=0, rot=rot_b)
            d = stand(ctx, KID1, KIDX + (80 * fall), KKID, p, 1, dyy)
            legs_in_one(ctx, KIDX + 80 * fall, KKID, dyy, rot_b, il, hx('3d7bff'))
            if il >= 36:
                for k in range(6):
                    a = k * math.pi / 5 + math.pi
                    ctx.move_to(KIDX - 60 + 170 * math.cos(a), GND - 20 + 50 * math.sin(a)); ctx.line_to(KIDX - 60 + 240 * math.cos(a), GND - 20 + 70 * math.sin(a)); ink(ctx, 6); ctx.stroke()
            else:
                sleeve_horn(ctx, d, TEE, il)
        elif j == 1:
            stp = math.sin(il * 0.8)
            p = P(eye='happy', mouth='grin', lsh=40, lel=-60, rsh=40, rel=-60, lhip=10 * stp, rhip=-10 * stp)
            d = stand(ctx, KID2, KIDX, KKID, p, 1, -10 * abs(stp))
            boots(ctx, KIDX, KKID, -10 * abs(stp))
            tag(ctx, KIDX, KKID); sleeve_horn(ctx, d, TEE, il)
        else:
            if il >= 92:
                cape(ctx, KIDX, KKID, il * 2, RED)
            p = P(eye='smug', mouth='grin', lsh=170, lel=-60, rsh=170, rel=-60)
            d = stand(ctx, KID2, KIDX, KKID, p, 1)
            tutu(ctx, KIDX, KKID); boots(ctx, KIDX, KKID); tag(ctx, KIDX, KKID); sleeve_horn(ctx, d, TEE, il)
            if il >= 82:
                goggles(ctx, d)
        pile(ctx, 1330, FLOOR + 50, 0.85, il)
        ctx.restore()
        if j == 0:
            if il < 36:
                label(ctx, "*BOING! BOING!*", 540, 600, 105, GOLD, -0.05, pop(il, 1, 4))
            else:
                label(ctx, "*THUD!*", 540, 600, 140, RED, 0.05, pop(il, 44, 47))
            label(ctx, "\"PANTS? EASY!\"", 540, 1470, 115, WHITE, 0.03, pop(il, 2, 6))
        elif j == 1:
            label(ctx, "*squeak squeak*", 540, 600, 105, GREEN, 0.05, pop(il, 51, 54))
            label(ctx, "\"SHOES? DONE!\"", 540, 1470, 115, WHITE, -0.03, pop(il, 52, 56))
        else:
            label(ctx, "*SNAP!*", 540, 600, 110, CYAN, -0.05, pop(il, 82, 85))
            if il >= 92:
                label(ctx, "*FWOOSH!*", 540, 1470, 115, RED, 0.03, pop(il, 92, 95))
    else:
        # low-angle hero reveal
        lt = il - 104
        ctx.save(); cam(ctx, KIDX, 1250, 1.5 + 0.06 * eio(lt / 26), 0, shake_at(lt, [0], 6, 8), f)
        # rays behind
        ctx.save(); ctx.translate(KIDX, 1300)
        for a in range(16):
            aa = a * math.pi / 8 + lt * 0.03
            poly(ctx, [(0, 0), (2000 * math.cos(aa), 2000 * math.sin(aa)), (2000 * math.cos(aa + 0.2), 2000 * math.sin(aa + 0.2))])
            setc(ctx, (GOLD, hx('ffe08a'))[a % 2]); ctx.fill()
        ctx.restore()
        ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('e0a86e')); ctx.fill()
        ellipse(ctx, 1110, FLOOR + 40, 380, 50); fl(ctx, hx('ffd36a'), 5)
        kid_full(ctx, KIDX, KKID, P(eye='happy', mouth='grin', lsh=175, lel=0, rsh=60, rel=-100, head=-4), lt * 2)
        for k in range(6):
            sparkle(ctx, KIDX + 300 * math.cos(k + lt * 0.08), 1250 + 250 * math.sin(k * 1.7 + lt * 0.08), 18 + 6 * math.sin(lt * 0.5 + k), WHITE)
        ctx.restore()
        label(ctx, "*TA-DAAA!*", 540, 470, 130, RED, -0.04, pop(lt, 0, 3))
        label(ctx, "\"READY!\"", 540, 1470, 150, WHITE, 0.03, pop(lt, 4, 8))


def s3(ctx, f):
    montage(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: the one close-up
def s4(ctx, f):
    il = f - 330
    ctx.save(); cam(ctx, MOMX + 40, 1300, 1.8 + 0.1 * eio(il / 70), 0, shake_at(il, [36], 5, 6), f)
    room(ctx, il); dresser(ctx, il)
    shake = 3 * math.sin(il * 2.3) if il >= 36 else 0
    d = stand(ctx, MOM, MOMX + shake, KMOM, P(eye='happy' if il < 36 else 'closed', mouth='wavy' if il < 36 else 'flat',
                                              lsh=30, lel=-150, rsh=20, rel=-140, head=-3))
    if il >= 36:
        twitch(ctx, d['head'][0] + d['R'] * 0.95, d['head'][1] - d['R'] * 0.75, il, 0.7)
        sweat(ctx, d['head'][0] - d['R'] * 0.95, d['head'][1] - d['R'] * 0.5, il, 0.6)
    ctx.restore()
    if il < 36:
        label(ctx, "\"It's... PERFECT,\"", 540, 520, 110, WHITE, -0.03, pop(il, 3, 7))
    else:
        label(ctx, "\"...sweetie.\"", 540, 520, 120, PINK, 0.03, pop(il, 36, 39))
        label(ctx, "*snrrk*", 540, 1470, 100, GOLD, -0.04, pop(il, 44, 47))


# ------------------------------------------------------------------ shot 5: Dad too -> loop
def half(ctx, f, il, side):
    ctx.save()
    ctx.rectangle(0 if side < 0 else W / 2, 0, W / 2, H); ctx.clip()
    ctx.rectangle(0, 0, W, H); setc(ctx, hx('d6efff')); ctx.fill()
    slide = 1 - eio(pop(il, 0 if side < 0 else 6, 14 if side < 0 else 20))
    cam(ctx, (KIDX if side < 0 else DADX) - 0 * side, 1300, 1.0, 0, shake_at(il, [0], 6, 6), f,
        sx=W / 4 if side < 0 else 3 * W / 4, sy=H / 2 + 1200 * slide * side)
    room(ctx, il)
    if side < 0:
        kid_full(ctx, KIDX, KKID, P(eye='happy', mouth='grin', lsh=150, lel=-20, rsh=40, rel=-80), il)
    else:
        dad_fit(ctx, DADX, KDAD, P(eye='smug', mouth='grin', lsh=40, lel=-80, rsh=150, rel=-20), il)
    ctx.restore()


def finale(ctx, f, il):
    # il 0..230 (f 400..630): split 0-76 ; wide 76: high-five 86 CLAP ; 112 Mom "Change. BOTH of you." ; 150 dive FWUMP ;
    # 176 both pop up with shirts on heads "WE CAN DO IT OURSELVES!!"
    if il < 76:
        half(ctx, f, il, -1); half(ctx, f, il, 1)
        ctx.rectangle(W / 2 - 7, 0, 14, H); setc(ctx, WHITE); ctx.fill()
        ctx.move_to(W / 2 - 7, 0); ctx.line_to(W / 2 - 7, H); ctx.move_to(W / 2 + 7, 0); ctx.line_to(W / 2 + 7, H); ink(ctx, 4); ctx.stroke()
        card(ctx, 'p2', il, 0, 60)
        label(ctx, "\"Ready for", 290, 1400, 66, WHITE, -0.03, pop(il, 8, 12))
        label(ctx, "SCHOOL!\"", 290, 1490, 80, WHITE, -0.03, pop(il, 10, 14))
        label(ctx, "\"Ready for", 800, 1400, 66, GOLD, 0.03, pop(il, 22, 26))
        label(ctx, "WORK!\"", 800, 1490, 80, GOLD, 0.03, pop(il, 24, 28))
        return
    lt = il - 76
    ctx.save(); cam(ctx, 1100, 1250, 1.18 + 0.05 * eio(pop(lt, 0, 80)), 0, shake_at(lt, [10, 74, 100], 8, 10), f)
    room(ctx, il); dresser(ctx, il)
    if lt < 36:
        mp = P(eye='shock', mouth='open', lsh=30, lel=-150, rsh=20, rel=-140)
    elif lt < 74:
        mp = P(eye='glare', mouth='flat', lsh=50, lel=-120, rsh=150, rel=-20)
    else:
        mp = P(eye='closed', mouth='frown', lsh=160, lel=-120, rsh=20, rel=-60, head=6)
    mom(ctx, mp)
    burst = pop(lt, 74, 96)
    if lt < 74:
        hf = lt >= 10
        kp = P(eye='happy', mouth='grin', lsh=40, lel=-60, rsh=160 if hf else 60, rel=-10, head=4) if lt < 36 else \
            P(eye='shock', mouth='open', lsh=40, lel=-60, rsh=60, rel=-40)
        dp = P(eye='happy', mouth='grin', lsh=40, lel=-80, rsh=160 if hf else 60, rel=-10) if lt < 36 else \
            P(eye='shock', mouth='open', lsh=40, lel=-80, rsh=60, rel=-40)
        kid_full(ctx, KIDX - 40, KKID, kp, il)
        dad_fit(ctx, DADX, KDAD, dp, il, 0, -1)
        if 10 <= lt < 20:
            sparkle(ctx, 1250, 1030, 50, YEL)
        pile(ctx, 1250, FLOOR + 60, 0.9, il)
    elif lt < 100:
        # dive: legs sticking out of the pile, clothes flying
        pile(ctx, 1250, FLOOR + 60, 1.2, il)
        for x_, ch in ((1180, KID2), (1330, DAD)):
            kick = math.sin(lt * 1.2 + x_)
            for sd in (-1, 1):
                ctx.move_to(x_ + sd * 18, FLOOR + 20); ctx.line_to(x_ + sd * 30 + 14 * kick * sd, FLOOR - 90)
                setc(ctx, INK); ctx.set_line_width(40); ctx.stroke_preserve(); setc(ctx, ch['pants']); ctx.set_line_width(30); ctx.stroke()
                ellipse(ctx, x_ + sd * 30 + 14 * kick * sd, FLOOR - 104, 26, 16); fl(ctx, ch['shoes'], 4)
        pile(ctx, 1250, FLOOR + 30, 0.9, il, burst)
    else:
        u = lt - 100
        up_ = eio(pop(u, 0, 8))
        d = stand(ctx, KID0, 1060, KKID, FLAIL(u, eye='glare', mouth='scream', lhip=14, rhip=-14), 1, 400 * (1 - up_))
        shirt_on_head(ctx, d, TEE, u)
        d2 = stand(ctx, DAD, DADX, KDAD, FLAIL(u + 7, eye='glare', mouth='scream', lhip=14, rhip=-14), -1, 400 * (1 - up_))
        shirt_on_head(ctx, d2, hx('ffd23f'), u + 5)
        pile(ctx, 1290, FLOOR + 70, 0.9, il)
    dog(ctx, 1520, GND + 30, 0.5, -1, il)
    ctx.restore()
    if lt < 36:
        label(ctx, "*CLAP!*", 540, 600, 130, GOLD, -0.05, pop(lt, 10, 13))
        label(ctx, "\"HIGH FIVE!\"", 540, 1470, 120, WHITE, 0.03, pop(lt, 12, 16))
    elif lt < 74:
        label(ctx, "\"...Change.\"", 540, 600, 110, WHITE, -0.03, pop(lt, 36, 40))
        label(ctx, "\"BOTH of you.\"", 540, 1470, 120, RED, 0.03, pop(lt, 50, 54))
    elif lt < 100:
        label(ctx, "*FWUMP!*", 540, 600, 140, PURPLE, 0.04, pop(lt, 74, 77))
    else:
        label(ctx, "\"WE CAN DO IT", 540, 1390, 100, WHITE, -0.03, pop(lt, 102, 106))
        label(ctx, "OURSELVES!!\"", 540, 1500, 100, WHITE, -0.03, pop(lt, 104, 108))


def s5(ctx, f):
    lf = f - 400
    if lf < 230:
        finale(ctx, f, lf)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (200, s3), (330, s4), (400, s5)]
CUTS = (60, 200, 330, 400, 476, 630)


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
                              "-i", "out/dress_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
