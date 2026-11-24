"""'Dad vs the umbrella' - original, general-audience comedy short, 22s.
Hook:   rainy front-yard medium shot: soaked Dad holding an inside-out umbrella in the wind, forced grin "IT'S... FINE!!"
        + caption "DAD vs THE UMBRELLA:"; Mom + kid dry and giggling at the window.
Beat 1: on the porch, smug: "Rain? I've GOT this." -> *CLICK! FWOMP!* the umbrella pops open + sparkle.
Beat 2: Dutch-tilt wind fight: *FWOOSH!* inside out -> *POP!* fixed -> *FWOOSH!* -> *POP!* -> BIG gust lifts Dad off his feet "WHOAAA!!"
Beat 3: wide: Dad sails over the roofs like a kite past a bird -> *SPLOOSH!* into a giant puddle; umbrella on his head, a frog hops on
        *ribbit* "...I MEANT to do that."
Turn:   Dad ECU (the one close-up), dripping: "I... LOVE..." "...RAIN."
Twist:  "PLOT TWIST: THE SUN CAME OUT." rainbow; Mom + kid stroll out in sunglasses "What a LOVELY day!" / "Dad... why are you WET?"
        -> ONE tiny grey cloud parks right over Dad *drip drip* "...of COURSE." -> he opens the umbrella *FWOMP* "HA!"
        -> the cloud puffs *FWOOSH!* inside out again -> loop to the hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import twitch
from scenes70 import bird
import scenes77
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); TEAL = hx('19b5a5')
WATER = hx('8fd0ff'); UMB = hx('3d8bff'); UMB2 = hx('ffd23f')
DAD = dict(doodle.DAD, shirt=hx('ff8a1f'), pants=hx('3d5a9e'))
MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'), pants=hx('2f4a8a'), shades=True)
KID = dict(doodle.BOY, hood=False, shades=True, shirt=hx('7fd04a'), pants=hx('3d7bff'), shoes=hx('ff3b5c'))
N = 660
HZ = scenes77.HZ          # 1190: house bottom / lawn line
GND = 1580
KDAD, KMOM, KKID = 1.2, 1.1, 0.92
DADX = 600

CAPS = {'p1': [[("DAD vs ", OUT), ("THE UMBRELLA:", BLUE)]],
        'p2': [[("PLOT TWIST:", RED)], [("THE SUN ", OUT), ("CAME OUT.", ORANGE)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def umbrella(ctx, x, y, flip, s=1.0, a=0.0, open_=1.0, shaft=True):
    """(x, y) = hand. flip 0 = dome, 1 = inside out. open_ 0 = furled."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if shaft:
        ctx.move_to(0, 0); ctx.line_to(0, -330); ink(ctx, 9); ctx.stroke()
        ctx.new_path(); ctx.arc(-14, 0, 14, 0, math.pi); ink(ctx, 9); ctx.stroke()          # J handle
    if open_ < 0.05:
        poly(ctx, [(0, -360), (26, -250), (0, -90), (-26, -250)]); fl(ctx, UMB, 5)
        ctx.restore(); return
    sx = open_
    ctx.save(); ctx.scale(sx, 1)
    d = 1 - 2 * flip
    ctx.new_path(); ctx.move_to(-230, -330)
    for k in range(4):
        x0 = -230 + k * 115
        ctx.curve_to(x0 + 30, -330 + 40 * d * 0.3, x0 + 85, -330 + 40 * d * 0.3, x0 + 115, -330)
    ctx.curve_to(170, -330 - 170 * d, -170, -330 - 170 * d, -230, -330); ctx.close_path()
    fl(ctx, UMB, 7)
    # yellow alternating panels
    for k in (0, 2):
        x0 = -230 + k * 115
        ctx.save()
        ctx.new_path(); ctx.move_to(0, -330 - 150 * d); ctx.line_to(x0, -330); ctx.line_to(x0 + 115, -330); ctx.close_path()
        setc(ctx, UMB2); ctx.fill()
        ctx.restore()
    for k in (-230, -115, 0, 115, 230):
        ctx.move_to(0, -330 - 150 * d); ctx.line_to(k, -330); setc(ctx, dark(UMB, 0.6)); ctx.set_line_width(4); ctx.stroke()
    ctx.new_path(); ctx.move_to(-230, -330)
    ctx.curve_to(-170, -330 - 170 * d, 170, -330 - 170 * d, 230, -330); ink(ctx, 6); ctx.stroke()
    ctx.move_to(0, -330 - 150 * d); ctx.line_to(0, -330 - 150 * d - 30 * d); ink(ctx, 7); ctx.stroke()
    ctx.restore()
    ctx.restore()


def rain(ctx, lf, x0=-600, x1=2400, y0=-600, y1=2600, wind=0.25, a=1.0, n=170, seed=3):
    if a <= 0:
        return
    rnd = random.Random(seed)
    for k in range(n):
        x = rnd.uniform(x0, x1); sp = rnd.uniform(55, 80)
        y = y0 + (rnd.uniform(0, y1 - y0) + lf * sp) % (y1 - y0)
        xx = x + (y - y0) * wind
        ctx.move_to(xx, y); ctx.line_to(xx - 60 * wind - 4, y - 60)
    setc(ctx, (0.85, 0.93, 1.0, 0.75 * a)); ctx.set_line_width(5); ctx.stroke()


def wind_lines(ctx, lf, x0, y0, n=5, a=1.0):
    for k in range(n):
        y = y0 + k * 90 + 20 * math.sin(lf * 0.3 + k)
        x = x0 + ((lf * 70 + k * 260) % 1600) - 400
        ctx.new_path(); ctx.move_to(x, y); ctx.curve_to(x + 120, y - 30, x + 220, y + 30, x + 320, y)
        ctx.arc_negative(x + 320, y - 30, 30, math.pi / 2, -math.pi)
        setc(ctx, (1, 1, 1, 0.8 * a)); ctx.set_line_width(7); ctx.stroke()


def drips(ctx, x, y, w, lf, n=6, s=1.0):
    for k in range(n):
        t = ((lf * 0.07 + k * 0.37) % 1)
        xx = x - w / 2 + (k * 0.61 % 1) * w
        yy = y + t * 160 * s
        ctx.new_path(); ctx.move_to(xx, yy - 16 * s); ctx.curve_to(xx + 9 * s, yy, xx + 8 * s, yy + 10 * s, xx, yy + 10 * s)
        ctx.curve_to(xx - 8 * s, yy + 10 * s, xx - 9 * s, yy, xx, yy - 16 * s); setc(ctx, WATER + (1 - t,)); ctx.fill()


def puddle(ctx, x, y, w, ripple=0.0, lf=0):
    ellipse(ctx, x, y, w, w * 0.2); fl(ctx, hx('7fc4ef'), 5)
    ellipse(ctx, x - w * 0.3, y - w * 0.05, w * 0.25, w * 0.04); setc(ctx, (1, 1, 1, 0.7)); ctx.fill()
    for k in range(3):
        r = ((lf * 0.04 + k * 0.33) % 1)
        ellipse(ctx, x + (k - 1) * w * 0.35, y + 4, w * 0.18 * r + 4, w * 0.04 * r + 2); setc(ctx, (1, 1, 1, 0.6 * (1 - r))); ctx.set_line_width(3); ctx.stroke()


def splash(ctx, x, y, t, s=1.0):
    if not 0 < t < 1:
        return
    for k in range(11):
        a = -math.pi * (0.08 + 0.84 * k / 10)
        d = 300 * s * eout(t)
        ellipse(ctx, x + math.cos(a) * d, y + math.sin(a) * d * 1.3 + 340 * t * t * s, 30 * s * (1 - 0.5 * t), 40 * s * (1 - 0.5 * t)); fl(ctx, WATER, 4)


def frog(ctx, x, y, s=1.0, croak=0.0):
    G = hx('5fd05a')
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 60, 40); fl(ctx, G, 5)
    for sx in (-1, 1):
        ellipse(ctx, sx * 30, -36, 20, 20); fl(ctx, G, 4)
        ellipse(ctx, sx * 30, -36, 10, 11); setc(ctx, INK); ctx.fill()
        ellipse(ctx, sx * 27, -40, 4, 4); setc(ctx, WHITE); ctx.fill()
        ellipse(ctx, sx * 44, 8, 10, 6); setc(ctx, (1, 0.5, 0.6, 0.6)); ctx.fill()
    if croak > 0:
        ellipse(ctx, 0, 26, 26 * croak, 18 * croak); fl(ctx, hx('ffd0e0'), 3)
    ctx.new_path(); ctx.arc(0, 4, 22, 0.3, math.pi - 0.3); ink(ctx, 4); ctx.stroke()
    ctx.restore()


def rainbow(ctx, x, y, r, a):
    if a <= 0:
        return
    for k, c in enumerate((RED, ORANGE, YEL, GREEN, BLUE, PURPLE)):
        ctx.new_path(); ctx.arc(x, y, r - k * 34, math.pi, math.pi + math.pi * a)
        setc(ctx, c + (0.85,)); ctx.set_line_width(34); ctx.stroke()


def grey_cloud(ctx, x, y, s=1.0, puff=0.0, lf=0):
    col = hx('8a94a8')
    ctx.save(); ctx.translate(x, y); ctx.scale(s * (1 + 0.15 * puff), s * (1 - 0.1 * puff))
    for dx, dy, r in ((-90, 10, 60), (-20, -30, 80), (70, 0, 66), (10, 30, 70)):
        ctx.new_path(); ctx.arc(dx, dy, r, 0, 2 * math.pi); fl(ctx, col, 6)
    for dx, dy, r in ((-90, 10, 54), (-20, -30, 74), (70, 0, 60), (10, 30, 64)):
        ctx.new_path(); ctx.arc(dx, dy, r, 0, 2 * math.pi); setc(ctx, col); ctx.fill()
    # cheeky face
    for sx in (-1, 1):
        ellipse(ctx, sx * 30, 0, 9, 12 if puff < 0.5 else 4); setc(ctx, INK); ctx.fill()
    if puff > 0.3:
        ellipse(ctx, -70, 30, 22 * puff, 20 * puff); setc(ctx, INK); ctx.fill()
    else:
        ctx.new_path(); ctx.arc(0, 20, 18, 0.3, math.pi - 0.3); ink(ctx, 4); ctx.stroke()
    ctx.restore()


# ------------------------------------------------------------------ set
def sky(ctx, lf, sun=0.0):
    c0 = hx('7d8aa6'); c1 = hx('8fd8ff')
    col = tuple(lerp(a, b, sun) for a, b in zip(c0, c1))
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, col); ctx.fill()
    if sun > 0:
        rays(ctx, 1050, 430, 130, 520, lf * 0.02, col=(1, 0.95, 0.5), a=0.55 * sun, n=14)
        ctx.new_path(); ctx.arc(1050, 430, 105, 0, 2 * math.pi); fl(ctx, hx('ffd23f'), 7)
    gc = tuple(lerp(a, b, sun) for a, b in zip(hx('b0b8c8'), (1, 1, 1)))
    for cx_, cy_ in ((300 + 0.4 * lf, 360), (1300 + 0.3 * lf, 330), (-500 + 0.2 * lf, 420)):
        for dx, r in ((-60, 50), (0, 70), (62, 50)):
            ellipse(ctx, cx_ + dx, cy_ + 60 * sun, r, r * 0.8); fl(ctx, gc, 5)


def lawn(ctx, lf, sun=0.0):
    g = tuple(lerp(a, b, sun) for a, b in zip(hx('4fae5a'), hx('6fd06a')))
    ctx.rectangle(-3000, HZ, 9000, 4000); setc(ctx, g); ctx.fill()
    ctx.move_to(-3000, HZ); ctx.line_to(6000, HZ); ink(ctx, 6); ctx.stroke()
    for k in range(-20, 60):
        x = k * 97 % 3600 - 800; y = HZ + 40 + (k * 53) % 900
        ctx.move_to(x - 12, y); ctx.line_to(x - 4, y - 22); ctx.line_to(x + 4, y); ctx.line_to(x + 12, y - 18)
    setc(ctx, dark(g, 0.75)); ctx.set_line_width(5); ctx.stroke()
    # front path from the door
    poly(ctx, [(690, HZ), (860, HZ), (1000, 2600), (480, 2600)]); fl(ctx, hx('d8d2c8'), 6)
    for k in range(6):
        yy = HZ + 70 + k * 120
        ctx.move_to(690 - (yy - HZ) * 0.15, yy); ctx.line_to(860 + (yy - HZ) * 0.1, yy)
    setc(ctx, hx('b8b0a4')); ctx.set_line_width(4); ctx.stroke()
    # flower bed under the window
    for k in range(7):
        x = 150 + k * 70
        ctx.move_to(x, HZ + 70); ctx.line_to(x, HZ + 10); setc(ctx, GREEN); ctx.set_line_width(6); ctx.stroke()
        ellipse(ctx, x, HZ + 4, 20, 20); fl(ctx, (PINK, YEL, RED, PURPLE, ORANGE, PINK, YEL)[k], 4)
    # picket fence to the right
    for k in range(10):
        x = 1060 + k * 60
        poly(ctx, [(x, HZ + 30), (x, HZ - 130), (x + 22, HZ - 155), (x + 44, HZ - 130), (x + 44, HZ + 30)]); fl(ctx, WHITE, 5)
    ctx.rectangle(1050, HZ - 90, 620, 22); fl(ctx, WHITE, 4)
    # mailbox
    ctx.rectangle(1150, HZ + 300 - 190, 16, 190); fl(ctx, hx('8a5a3a'), 4)
    rect_r(ctx, 1100, HZ + 300 - 250, 120, 70, 30); fl(ctx, RED, 5)
    # gnome-ish garden mushroom
    ellipse(ctx, 250, HZ + 330, 60, 30); fl(ctx, RED, 5)
    ctx.rectangle(235, HZ + 340, 30, 50); fl(ctx, WHITE, 4)
    for dx in (-25, 10, 30):
        ellipse(ctx, 250 + dx, HZ + 318, 8, 6); setc(ctx, WHITE); ctx.fill()


def window_faces(ctx, lf, mood='giggle'):
    """Mom + kid peeking out of the house window (window centred x=290, y 780..980)"""
    ctx.save(); rect_r(ctx, 170, 780, 240, 200, 12); ctx.clip()
    ctx.rectangle(170, 780, 240, 200); setc(ctx, hx('ffe9c2')); ctx.fill()
    bob = 6 * math.sin(lf * 0.5)
    face(ctx, MOM, P(eye='happy', mouth='grin', shades=0), 240, 905 + bob, 52)
    face(ctx, KID, P(eye='happy', mouth='open', shades=0), 345, 920 - bob, 46)
    ctx.restore()
    ctx.move_to(290, 780); ctx.line_to(290, 980); ctx.move_to(170, 880); ctx.line_to(410, 880); setc(ctx, (1, 1, 1, 0.5)); ctx.set_line_width(6); ctx.stroke()


def world(ctx, lf, sun=0.0, door=0.0, faces=True):
    sky(ctx, lf, sun)
    scenes77.house(ctx, 540, hx('ffe08a') if sun > 0.5 else hx('ecd283'), hx('ff6b5a'), door, mine=True)
    if faces:
        window_faces(ctx, lf)
    lawn(ctx, lf, sun)


# ------------------------------------------------------------------ people
def stand(ctx, ch, x, k, p, f_=1, y=GND):
    return draw(ctx, x, y - 186 * k, k, f_, ch, p)


def dad_umb(ctx, x, flip, eye='normal', mouth='smile', y=GND, rot=0, open_=1.0, ua=0.0, ch=DAD, **kw):
    p = P(eye=eye, mouth=mouth, rsh=165, rel=-10, lsh=30, lel=-20, rot=rot)
    p.update(kw)
    d = stand(ctx, ch, x, KDAD, p, y=y)
    hx_, hy_ = d['front']
    umbrella(ctx, hx_, hy_, flip, 0.95, ua, open_)
    return d


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    ctx.save(); cam(ctx, 640, 1170, 1.16 + 0.04 * eio(pop(lf, 0, 40)), 0, 3 + shake_at(lf, [0], 7, 8), f)
    world(ctx, lf)
    puddle(ctx, 640, GND + 10, 220, lf=lf)
    d = dad_umb(ctx, DADX, 1.0, 'glare', 'grin', torso=-10 + 3 * math.sin(lf * 0.7), ua=0.35 + 0.08 * math.sin(lf * 0.9),
                lsh=-60, lel=-60)
    drips(ctx, d['head'][0], d['head'][1] + d['R'] * 0.6, d['R'] * 2, lf, 7)
    twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.9, lf, 0.8)
    rain(ctx, lf, wind=0.35)
    wind_lines(ctx, lf, 200, 1150, 3, 0.7)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"IT'S... FINE!!\"", 540, 1440, 130, WHITE, -0.03, t)


# ------------------------------------------------------------------ shot 2
def porch(ctx, f, il):
    # il 0..70: Dad on the path by the door, smug "Rain? I've GOT this." ; 36 *CLICK! FWOMP!* opens ; 50 "EASY."
    ctx.save(); cam(ctx, 700, 1180, lerp(1.12, 1.24, eio(il / 70)), 0, shake_at(il, [36], 5, 6), f)
    world(ctx, il, door=1.0, faces=False)
    puddle(ctx, 1000, GND + 30, 160, lf=il)
    op = eout(pop(il, 36, 41))
    d = dad_umb(ctx, 760, 0.0, 'smug' if il < 36 else 'happy', 'grin', open_=op, ua=0.0 if op > 0 else 0.1,
                rsh=lerp(60, 165, eio(pop(il, 28, 36))), rel=lerp(-40, -10, eio(pop(il, 28, 36))))
    if op > 0.9:
        for j in range(4):
            sparkle(ctx, 760 + (-220, 220, -120, 150)[j], 760 + (0, -20, -120, -110)[j], 16 + 5 * math.sin(il * 0.6 + j), GOLD)
    rain(ctx, il, wind=0.12)
    ctx.restore()
    if il < 36:
        label2(ctx, "\"Rain? I've", "GOT this.\"", WHITE, pop(il, 4, 8), 120, col2=BLUE, y=1440)
    elif il < 52:
        label(ctx, "*CLICK! FWOMP!*", 540, 660, 104, BLUE, -0.04, pop(il, 36, 39))
    else:
        label(ctx, "\"EASY.\"", 540, 1440, 140, WHITE, -0.03, pop(il, 52, 55))


GUSTS = [0, 28]
POPS = [14, 40]
LIFT = 54


def flip_at(il):
    fl_ = 0.0
    for g, p_ in zip(GUSTS, POPS):
        if il >= g:
            fl_ = eout(pop(il, g, g + 4))
        if il >= p_:
            fl_ = 1 - eout(pop(il, p_, p_ + 3))
    if il >= LIFT:
        fl_ = eout(pop(il, LIFT, LIFT + 4)) * 0.0     # big gust keeps it as a dome -> kite
    return fl_


def windfight(ctx, f, il):
    # il 0..86 Dutch tilt
    rot = -8
    ctx.save(); cam(ctx, 660, 1150, lerp(1.18, 1.1, eio(il / 86)), rot, shake_at(il, GUSTS + POPS + [LIFT], 6, 6), f)
    world(ctx, il, faces=True)
    puddle(ctx, 960, GND + 30, 170, lf=il)
    fl_ = flip_at(il)
    up = eio(pop(il, LIFT, 84)) ** 1.4
    yy = GND - 1100 * up
    kick_ = math.sin(il * 1.2) * 25 * (il >= LIFT)
    pull = any(p_ - 2 <= il < p_ + 4 for p_ in POPS)
    gust = any(g <= il < g + 10 for g in GUSTS) or il >= LIFT
    eye = 'shock' if gust else ('glare' if pull else 'normal')
    mouth = 'scream' if il >= LIFT else ('open' if gust else 'flat')
    d = dad_umb(ctx, DADX + 140 * up, fl_, eye, mouth, y=yy, ua=(0.45 if gust else 0.1) + 0.05 * math.sin(il * 1.3),
                torso=(-14 if gust else 4), lsh=(-60 + kick_ if il >= LIFT else (150 if pull else -40)), lel=-40,
                rot=-6 * up)
    drips(ctx, d['head'][0], d['head'][1] + d['R'] * 0.6, d['R'] * 2, il, 5)
    rain(ctx, il, wind=0.45)
    wind_lines(ctx, il, 100, 1000, 5, 1.0 if gust else 0.4)
    ctx.restore()
    for j, g in enumerate(GUSTS):
        if g <= il < g + 12:
            label(ctx, "*FWOOSH!*", 540 + (-150, 150)[j], 660, 110, CYAN, (-0.06, 0.06)[j], pop(il, g, g + 3))
    for j, p_ in enumerate(POPS):
        if p_ <= il < p_ + 12:
            label(ctx, "*POP!*", 540 + (170, -170)[j], 700, 110, GOLD, (0.06, -0.06)[j], pop(il, p_, p_ + 3))
    if il >= LIFT:
        label(ctx, "\"WHOAAA!!\"", 540, 1440, 150, WHITE, -0.04, pop(il, LIFT + 2, LIFT + 6))


def s2(ctx, f):
    lf = f - 60
    if lf < 70:
        porch(ctx, f, lf)
    else:
        windfight(ctx, f, lf - 70)


# ------------------------------------------------------------------ shot 3
PX, PY = 1000, GND + 60       # big puddle


def flight(ctx, f, il):
    # il 0..54 wide: Dad sails across the sky over the roof, bird passes "...hi." ; 44 drops ; 52 *SPLOOSH!*
    ctx.save(); cam(ctx, 760, 1050, 0.6, 0, shake_at(il, [52], 10, 8), f)
    world(ctx, il)
    scenes77.house(ctx, 1980, hx('a8e0ff'), hx('8a5ac8'), 0, mine=False)
    lawn_fill = None
    puddle(ctx, PX, PY, 330, lf=il)
    u = clamp(il / 44)
    x = lerp(-80, PX + 60, u); y = lerp(500, 260, math.sin(math.pi * min(u, 0.75) / 1.5) * 1.0)
    if il >= 44:
        v = eio(pop(il, 44, 52)); x = PX + 60; y = lerp(y, PY - 60, v * v)
    if il < 52:
        d = dad_umb(ctx, x, 0.0, 'shock', 'scream', y=y + 186 * KDAD * 2, ua=0.25 * math.sin(il * 0.4), rot=10 * math.sin(il * 0.3),
                    lsh=-60 + 30 * math.sin(il * 1.1), lel=-40)
    if 14 <= il < 40:
        bird(ctx, lerp(1500, 300, (il - 14) / 26), 560, 0.8, il)
    splash(ctx, PX, PY, pop(il, 52, 62) if il >= 52 else 0, 1.4)
    rain(ctx, il, wind=0.45, n=260, x0=-1200, x1=2800, y0=-800, y1=2800)
    ctx.restore()
    if 18 <= il < 44:
        label(ctx, "\"...hi.\"", 540, 1440, 120, WHITE, 0.03, pop(il, 20, 24))
    if il >= 52:
        label(ctx, "*SPLOOSH!!*", 540, 700, 130, BLUE, -0.05, pop(il, 52, 55))


def in_puddle(ctx, f, il, ch=DAD, lf=None):
    lf = il if lf is None else lf
    ctx.save(); cam(ctx, PX - 60, 1260, 1.25, 0, shake_at(il, [0], 6, 6), f)
    world(ctx, lf)
    puddle(ctx, PX, PY, 330, lf=lf)
    d = draw(ctx, PX, PY - 186 * KDAD * 0.55, KDAD, 1, DAD, P(eye='glare' if il > 20 else 'shock', mouth='flat', lsh=-40, lel=-60, rsh=40, rel=-60, torso=0))
    # water covering legs
    ellipse(ctx, PX, PY + 20, 330, 66); setc(ctx, hx('7fc4ef') + (0.85,)); ctx.fill()
    # inside-out umbrella on his head like a hat
    hx_, hy_ = d['head']; R = d['R']
    umbrella(ctx, hx_ + 10, hy_ + 260 * 0.55 - R * 0.6, 1.0, 0.55, 0.15, shaft=False)
    hop = eio(pop(il, 14, 24))
    frog(ctx, lerp(PX + 380, hx_ + 20, hop), lerp(PY, hy_ - R * 1.15 - 30, hop) - 140 * math.sin(math.pi * hop), 0.75,
         croak=(0.5 + 0.5 * math.sin(il * 1.2)) if il > 26 else 0)
    drips(ctx, hx_, hy_ + R * 0.5, R * 2, lf, 6)
    ctx.restore()
    return d


def s3(ctx, f):
    il = f - 216
    if il < 54:
        flight(ctx, f, il)
    else:
        j = il - 54
        in_puddle(ctx, f, j)
        if 26 <= j < 42:
            label(ctx, "*ribbit*", 540, 680, 110, GREEN, 0.05, pop(j, 26, 29))
        if j >= 14:
            label2(ctx, "\"...I MEANT", "to do that.\"", WHITE, pop(j, 16, 20), 115, col2=CYAN, y=1440)


# ------------------------------------------------------------------ shot 4: the one close-up
def ecu(ctx, f, il):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eio(il / 70), 0, 2 + shake_at(il, [0, 34], 6, 8), f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('7d8aa6')); ctx.fill()
    rays(ctx, 540, 900, 240, 1500, il * 0.02, col=(1, 1, 1), a=0.18, n=16)
    face(ctx, DAD, P(eye='glare', mouth='flat' if il < 34 else 'wavy'), 540, 960, 200, 0.0)
    umbrella(ctx, 560, 960 - 200 * 0.25, 1.0, 1.1, 0.12, shaft=False)
    frog(ctx, 620, 960 - 200 * 1.05 - 120, 1.4, croak=0.4 + 0.4 * math.sin(il * 1.1))
    drips(ctx, 540, 1060, 380, il, 10, 2.0)
    if il >= 34:
        twitch(ctx, 540 + 200 * 0.95, 960 - 200 * 0.6, il, 1.6)
    rain(ctx, il, wind=0.2, n=80)
    ctx.restore()
    if il < 34:
        label(ctx, "\"I... LOVE...\"", 540, 1440, 130, WHITE, -0.03, pop(il, 4, 8))
    else:
        label(ctx, "\"...RAIN.\"", 540, 1440, 160, CYAN, -0.03, pop(il, 34, 37))


def s4(ctx, f):
    ecu(ctx, f, f - 312)


# ------------------------------------------------------------------ shot 5: twist -> loop
def sunny(ctx, f, il):
    # il 0..120: sun bursts out, rainbow; Dad still in the puddle; door opens 18-28, Mom + kid stroll out in shades
    #            34 Mom "What a LOVELY day!" ; 74 kid "Dad... why are you WET?" ; 100 Dad twitch
    sun = eio(pop(il, 0, 14))
    ctx.save(); cam(ctx, 760, 1200, 1.06, 0, shake_at(il, [0], 5, 6), f)
    world(ctx, il, sun=sun, door=eio(pop(il, 16, 24)), faces=False)
    rainbow(ctx, 760, 1180, 760, eio(pop(il, 4, 26)))
    puddle(ctx, PX, PY, 330, lf=il)
    if il >= 18:
        walk = eio(pop(il, 22, 46))
        bob = abs(math.sin(il * 0.5)) * 10 * (22 <= il < 46)
        m = stand(ctx, MOM, lerp(770, 480, walk), KMOM, P(eye='happy', mouth='grin', shades=1, lsh=20, lel=-10,
                                                         rsh=150 if 34 <= il < 70 else 30, rel=-30, head=-4), f_=1, y=GND - bob)
        k = stand(ctx, KID, lerp(790, 650, walk), KKID, P(eye='happy', mouth='open' if il >= 74 else 'grin', shades=1,
                                                         rsh=150 if il >= 74 else 20, rel=-60 if il >= 74 else -10, lsh=20, lel=-10), f_=1, y=GND + 40 - bob)
    d = draw(ctx, PX, PY - 186 * KDAD * 0.55, KDAD, 1, DAD, P(eye='glare' if il < 100 else 'shock', mouth='flat', lsh=-40, lel=-60, rsh=40, rel=-60))
    ellipse(ctx, PX, PY + 20, 330, 66); setc(ctx, hx('7fc4ef') + (0.85,)); ctx.fill()
    hx_, hy_ = d['head']; R = d['R']
    umbrella(ctx, hx_ + 10, hy_ + 260 * 0.55 - R * 0.6, 1.0, 0.55, 0.15, shaft=False)
    frog(ctx, hx_ + 20, hy_ - R * 1.15 - 30, 0.75)
    drips(ctx, hx_, hy_ + R * 0.5, R * 2, il, 6)
    if il >= 100:
        twitch(ctx, hx_ + R * 0.9, hy_ - R * 0.9, il, 0.8)
    for j in range(3):
        sparkle(ctx, 300 + 280 * j, 520 + 40 * (j % 2), 14 + 4 * math.sin(il * 0.5 + j), GOLD)
    ctx.restore()
    card(ctx, 'p2', il, 6, 120)
    if 34 <= il < 74:
        label2(ctx, "\"What a", "LOVELY day!\"", WHITE, pop(il, 34, 38), 120, col2=GOLD, y=1440)
    elif il >= 74:
        label2(ctx, "\"Dad... why", "are you WET?\"", WHITE, pop(il, 74, 78), 115, col2=CYAN, y=1440)


def cloudy(ctx, f, il):
    # il 0..68: one tiny grey cloud slides in over Dad, rains only on him *drip drip* ; 36 "...of COURSE."
    ctx.save(); cam(ctx, 790, 1180, 1.16, 0, 0, f)
    world(ctx, il, sun=1.0, door=1.0, faces=False)
    rainbow(ctx, 760, 1180, 760, 1.0)
    puddle(ctx, PX, PY, 330, lf=il)
    d = draw(ctx, PX, PY - 186 * KDAD * 0.55, KDAD, 1, DAD, P(eye='glare', mouth='flat', lsh=-40, lel=-60, rsh=40, rel=-60))
    ellipse(ctx, PX, PY + 20, 330, 66); setc(ctx, hx('7fc4ef') + (0.85,)); ctx.fill()
    hx_, hy_ = d['head']; R = d['R']
    umbrella(ctx, hx_ + 10, hy_ + 260 * 0.55 - R * 0.6, 1.0, 0.55, 0.15, shaft=False)
    frog(ctx, hx_ + 20, hy_ - R * 1.15 - 30, 0.75)
    cx_ = lerp(1700, PX, eout(pop(il, 0, 16)))
    cy_ = hy_ - 470
    if il >= 14:
        ctx.save(); ctx.rectangle(cx_ - 180, cy_, 360, 900); ctx.clip()
        rain(ctx, il, x0=cx_ - 180, x1=cx_ + 180, y0=cy_, y1=PY, wind=0.0, n=30, seed=8)
        ctx.restore()
    grey_cloud(ctx, cx_, cy_, 1.0, 0, il)
    stand(ctx, MOM, 480, KMOM, P(eye='happy', mouth='grin', shades=1, lsh=20, lel=-10, rsh=150, rel=-140, head=-6), f_=1)
    stand(ctx, KID, 650, KKID, P(eye='happy', mouth='open', shades=1, lsh=150, lel=-150, rsh=20, rel=-10, head=-6), f_=1, y=GND + 40)
    if il >= 36:
        twitch(ctx, hx_ + R * 0.9, hy_ - R * 0.9, il, 0.8)
    ctx.restore()
    if il < 36:
        label(ctx, "*drip drip drip*", 540, 690, 100, BLUE, 0.04, pop(il, 16, 19))
    else:
        label2(ctx, "\"...of", "COURSE.\"", WHITE, pop(il, 36, 40), 130, col2=CYAN, y=1440)


def comeback(ctx, f, il):
    # il 0..60: Dad stands in the puddle, opens the umbrella *FWOMP* "HA!" (6) ; 28 cloud puffs *FWOOSH!* -> inside out
    ctx.save(); cam(ctx, 860, 1150, lerp(1.2, 1.3, eio(il / 60)), 0, shake_at(il, [6, 30], 6, 6), f)
    world(ctx, il, sun=1.0, door=1.0, faces=False)
    puddle(ctx, PX, PY, 330, lf=il)
    gust = il >= 28
    fl_ = eout(pop(il, 30, 34))
    d = dad_umb(ctx, PX, fl_, 'smug' if not gust else 'shock', 'grin' if not gust else 'open', y=PY - 20,
                open_=eout(pop(il, 4, 9)), ua=0.4 * fl_, torso=-10 * fl_, lsh=-40, lel=-60)
    ellipse(ctx, PX, PY + 10, 300, 50); setc(ctx, hx('7fc4ef') + (0.85,)); ctx.fill()
    hx_, hy_ = d['head']; R = d['R']
    cy_ = hy_ - 560
    puff = eio(pop(il, 22, 30)) * (1 - eio(pop(il, 40, 50)))
    grey_cloud(ctx, PX - 60, cy_, 1.0, puff, il)
    if gust:
        wind_lines(ctx, il, PX - 600, cy_ + 120, 5, 1.0)
    if il >= 34:
        ctx.save(); ctx.rectangle(PX - 240, cy_, 360, 900); ctx.clip()
        rain(ctx, il, x0=PX - 240, x1=PX + 120, y0=cy_, y1=PY, wind=0.2, n=40, seed=8)
        ctx.restore()
    ctx.restore()
    if il < 28:
        label(ctx, "\"HA!\"", 540, 1440, 160, GOLD, -0.04, pop(il, 8, 11))
    else:
        label(ctx, "*FWOOSH!*", 540, 1440, 140, CYAN, -0.04, pop(il, 30, 33))


def s5(ctx, f):
    lf = f - 382
    if lf < 120:
        sunny(ctx, f, lf)
    elif lf < 188:
        cloudy(ctx, f, lf - 120)
    elif lf < 248:
        comeback(ctx, f, lf - 188)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (216, s3), (312, s4), (382, s5)]
CUTS = (60, 130, 216, 270, 312, 382, 502, 570, 630)


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
                              "-i", "out/dad_vs_umbrella_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
