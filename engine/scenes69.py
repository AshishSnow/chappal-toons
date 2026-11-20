"""'Don't Touch the Buttons' - kid in an elevator. Original, general-audience comedy short, 22s.
Hook: Dad ECU, horrified + sweating "DON'T. TOUCH. THE BUTTONS." + caption 'Every kid in an ELEVATOR:'.
Beat 1: inside the car: Dad presses 7 "Floor 7. EASY." - kid's eyes sparkle at the panel.
        panel macro: kid's finger lights EVERY button BOOP BOOP BOOP -> Dad ECU "NOOOO!!"
Beat 2: hallway view, the doors open on every floor: F2 neighbour "Going DOWN?", F3 nobody *cricket*,
        F4 lady with groceries, F5/F6 faster and faster.
Beat 3: split screen: twitching Dad "...floor... SIX." / kid "BEST. RIDE. EVER!"
Twist:  F7 "FINALLY!" kid hops out, Dad leans back on the panel "Phew..." -> his back presses EVERY button,
        doors shut with Dad inside, kid waves "BYE, DAD!", display 8..12, "NOOOO..." fades upward.
End:    F12 doors open on a wrecked Dad - kid already there "HI DAD! I took the STAIRS!" - steps in,
        kid ECU sparkling eyes + finger -> Dad ECU loop "DON'T. TOUCH. THE BUTTONS." """
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes8 import walk
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


DAD = dict(doodle.DAD, shirt=hx('3d7bff'), pants=hx('2a3a6a'))
BOY = dict(doodle.BOY, hood=False, shades=False, shirt=hx('22b45a'))
NB = dict(doodle.NEIGHBOR, shirt=hx('ffc93c'))
NM = dict(doodle.NMOM, shirt=hx('ff5fa8'))
N = 660
RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); TEAL = hx('19b5a5'); WHITE = (1, 1, 1); SKY = hx('8fd8ff')
FLOOR = 1500
OX0, OX1, OY0 = 200, 880, 560      # elevator opening
DK, KK = 1.5, 0.95

CAPS = {
    'p1': [[("Every ", OUT), ("KID", GREEN), (" in an", OUT)], [("ELEVATOR:", RED)]],
}
scenes13.CAPS = CAPS
card = _card13


def num(ctx, s, x, y, size, col):
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s)
    ctx.move_to(x - e.x_advance / 2, y + size * 0.36); ctx.text_path(s); setc(ctx, col); ctx.fill()


# ------------------------------------------------------------------ props
def bpos(n):
    """button n (1..12) position inside a unit panel: 2 cols, 6 rows, 1 at bottom-left"""
    r, c = (n - 1) // 2, (n - 1) % 2
    return (-30 + 60 * c, 150 - r * 62)


def panel(ctx, x, y, s, lit, blink=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rect_r(ctx, -68, -230, 136, 440, 18); fl(ctx, hx('a9b4c6'), 5 / s * 1.6)
    rect_r(ctx, -54, -216, 108, 50, 8); setc(ctx, hx('1a1830')); ctx.fill()
    for k in range(3):
        ellipse(ctx, -26 + k * 26, -191, 7, 7); setc(ctx, hx('ff8a1f') if k == 1 else hx('444458')); ctx.fill()
    for n_ in range(1, 13):
        bx, by = bpos(n_)
        on = n_ in lit
        if on:
            ctx.new_path(); ctx.arc(bx, by, 30, 0, 2 * math.pi); setc(ctx, (1, 0.95, 0.4, 0.45 + 0.2 * blink)); ctx.fill()
        ctx.new_path(); ctx.arc(bx, by, 22, 0, 2 * math.pi); fl(ctx, hx('ffe14d') if on else hx('e8edf5'), 4 / s * 1.6)
        num(ctx, str(n_), bx, by, 22, hx('8a3a00') if on else hx('5a6478'))
    ctx.restore()


def display(ctx, x, y, n_, up=True, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rect_r(ctx, -110, -50, 220, 100, 16); fl(ctx, hx('1a1830'), 7)
    num(ctx, str(n_), 25, 0, 70, hx('ff8a1f'))
    if up:
        poly(ctx, [(-70, 22), (-40, 22), (-55, -24)]); setc(ctx, hx('ff8a1f')); ctx.fill()
    ctx.restore()


def car(ctx, lit, blink=0, x0=OX0 - 60, x1=OX1 + 60, panel_x=OX1 - 70):
    """inside of the elevator car (back wall, handrail, light, button panel)"""
    ctx.rectangle(x0, -600, x1 - x0, FLOOR + 600); setc(ctx, hx('d7dfeb')); ctx.fill()
    for k in range(int(x0), int(x1), 120):
        ctx.rectangle(k, -600, 6, FLOOR + 600); setc(ctx, hx('bfc9d8')); ctx.fill()
    ctx.rectangle(x0, FLOOR, x1 - x0, 1500); setc(ctx, hx('6a5a7a')); ctx.fill()
    ctx.move_to(x0, FLOOR); ctx.line_to(x1, FLOOR); ink(ctx, 7); ctx.stroke()
    rect_r(ctx, x0 + 40, 1170, x1 - x0 - 80, 22, 11); fl(ctx, hx('f0f3f8'), 5)
    panel(ctx, panel_x, 1000, 0.9, lit, blink)


def doors(ctx, o):
    w = (OX1 - OX0) / 2
    for side in (-1, 1):
        if side < 0:
            xa, xb = OX0, OX0 + w * (1 - o)
        else:
            xa, xb = OX1 - w * (1 - o), OX1
        if xb - xa < 1:
            continue
        ctx.rectangle(xa, OY0, xb - xa, FLOOR - OY0); fl(ctx, hx('b4bfcf'), 6)
        ctx.rectangle(xa + 20, OY0 + 30, max(0, xb - xa - 40), 10); setc(ctx, hx('dfe6f0')); ctx.fill()


def hallway(ctx, col, o, n_, lit, inside, blink=0, up=True, pcol=None):
    """hallway view, doors open by o (0..1); inside(ctx) draws the people in the car"""
    ctx.rectangle(-2000, -2000, 5000, 5000); setc(ctx, col); ctx.fill()
    for k in range(-20, 30):
        ctx.rectangle(k * 140, 0, 4, FLOOR); setc(ctx, dark(col, 0.92)); ctx.fill()
    ctx.rectangle(-2000, FLOOR, 5000, 800); setc(ctx, pcol or hx('5a4a6a')); ctx.fill()
    ctx.move_to(-2000, FLOOR); ctx.line_to(3000, FLOOR); ink(ctx, 8); ctx.stroke()
    # frame
    rect_r(ctx, OX0 - 40, OY0 - 40, OX1 - OX0 + 80, FLOOR - OY0 + 40, 10); fl(ctx, hx('8a94a8'), 7)
    ctx.save(); ctx.rectangle(OX0, OY0, OX1 - OX0, FLOOR - OY0); ctx.clip()
    car(ctx, lit, blink)
    inside(ctx)
    doors(ctx, o)
    ctx.restore()
    ctx.rectangle(OX0, OY0, OX1 - OX0, FLOOR - OY0); ink(ctx, 7); ctx.stroke()
    display(ctx, 540, 440, n_, up)
    # call button beside the door
    rect_r(ctx, OX1 + 70, 980, 60, 110, 12); fl(ctx, hx('a9b4c6'), 5)
    ctx.new_path(); ctx.arc(OX1 + 100, 1035, 18, 0, 2 * math.pi); fl(ctx, hx('ffe14d'), 4)


def finger(ctx, tx, ty, s=1.0):
    """kid's arm coming in from the lower right, fingertip at (tx, ty)"""
    ctx.save(); ctx.translate(tx, ty); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(70, 150); ctx.line_to(560, 1100)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); setc(ctx, INK); ctx.set_line_width(200); ctx.stroke_preserve()
    setc(ctx, BOY['shirt']); ctx.set_line_width(184); ctx.stroke()
    ctx.new_path(); ctx.move_to(40, 100); ctx.line_to(160, 260); setc(ctx, INK); ctx.set_line_width(142); ctx.stroke_preserve()
    setc(ctx, BOY['skin']); ctx.set_line_width(126); ctx.stroke()
    ctx.new_path(); ctx.move_to(4, 6); ctx.line_to(46, 90); setc(ctx, INK); ctx.set_line_width(58); ctx.stroke_preserve()
    setc(ctx, BOY['skin']); ctx.set_line_width(44); ctx.stroke()
    ctx.restore()


# ------------------------------------------------------------------ close-ups
def dad_ecu(ctx, f, lf, bg, eye='shock', mouth='wavy', z0=1.0, shake=0, tw=True, sw=True):
    ctx.save(); cam(ctx, 540, 960, z0, 0, shake, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    rays(ctx, 540, 900, 260, 1700, lf * 0.03, col=(1, 1, 1), a=0.2, n=18)
    cx, cy, R = 540, 880, 300
    face(ctx, DAD, P(eye=eye, mouth=mouth), cx, cy, R, 0.03 * math.sin(lf * 0.7))
    if sw:
        sweat(ctx, cx + 0.85 * R, cy - 0.45 * R, lf, 1.3); sweat(ctx, cx - 0.75 * R, cy - 0.2 * R, lf + 20, 1.0)
    if tw:
        twitch(ctx, cx + 0.55 * R, cy - 0.7 * R, lf, 1.3)
    ctx.restore()


def kid_ecu(ctx, f, lf, bg, z0=1.0, shake=0, eye='shock', mouth='grin', spark=True):
    ctx.save(); cam(ctx, 540, 960, z0, 0, shake, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    rays(ctx, 540, 900, 260, 1700, -lf * 0.04, col=(1, 1, 0.7), a=0.25, n=18)
    cx, cy, R = 540, 880, 290
    face(ctx, BOY, P(eye=eye, mouth=mouth), cx, cy, R, 0.04 * math.sin(lf * 0.5))
    if spark:
        for ex, s_ in ((cx - 0.2 * R, 0.8), (cx + 0.42 * R, 1.0)):
            sparkle(ctx, ex, cy + 0.06 * R, (34 + 10 * math.sin(lf * 0.9)) * s_)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    dad_ecu(ctx, f, lf, TEAL, z0=1.0 + 0.07 * eio(pop(lf, 0, 54)), shake=4 if (lf // 4) % 2 == 0 else 2)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"DON'T. TOUCH.", "THE BUTTONS.\"", WHITE, t, 110, col2=YEL, y=1400)


# ------------------------------------------------------------------ shots
def interior(ctx, f, lf):
    """inside the car: Dad presses 7, kid's eyes sparkle at the panel"""
    ctx.save(); cam(ctx, 560, 1000 + 20 * eio(pop(lf, 26, 56)), 1.05 + 0.15 * eio(pop(lf, 26, 56)), 0, 0, f)
    car(ctx, {7} if lf >= 14 else set(), x0=-400, x1=1500, panel_x=790)
    ctx.restore()
    ctx.save(); cam(ctx, 560, 1000 + 20 * eio(pop(lf, 26, 56)), 1.05 + 0.15 * eio(pop(lf, 26, 56)), 0, 0, f)
    press = lf < 22
    draw(ctx, 620, FLOOR - 186 * DK, DK, 1, DAD,
         P(eye='smug', mouth='grin', rsh=-115 if press else 10, rel=-30 if press else 0, lsh=10))
    ke = 'shock' if lf >= 26 else 'normal'
    draw(ctx, 300, FLOOR - 186 * KK, KK, 1, BOY, P(eye=ke, mouth='grin' if lf >= 26 else 'smile', head=-8 if lf >= 26 else 0, lsh=10, rsh=-10))
    if lf >= 26:
        b = draw(doodle_scr(), 300, FLOOR - 186 * KK, KK, 1, BOY, P(eye=ke, head=-8))
        for k, key in enumerate(('eyeL', 'eyeR')):
            ex, ey = b[key]
            sparkle(ctx, ex, ey, 18 + 6 * math.sin(lf * 0.9 + k))
    ctx.restore()
    if 14 <= lf < 22:
        label(ctx, "*boop*", 760, 760, 80, YEL, 0.06, pop(lf, 14, 16))
    label2(ctx, "\"Floor 7.", "EASY.\"", WHITE, pop(lf, 4, 8) if lf < 30 else 0, 110, col2=BLUE, y=1400)
    if lf >= 32:
        label(ctx, "*sparkle*", 540, 1400, 100, YEL, -0.04, pop(lf, 32, 35))


_S = [None]


def doodle_scr():
    if _S[0] is None:
        _S[0] = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4))
    return _S[0]


ORDER = [3, 10, 1, 12, 5, 8, 2, 11, 6, 9, 4]
PS = 3.0
PX, PY = 470, 960


def press_times():
    return [8 + 4.5 * k for k in range(len(ORDER))]


def panel_macro(ctx, f, il):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eio(pop(il, 0, 60)), 0, 6 if 8 <= il < 58 else 0, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('d7dfeb')); ctx.fill()
    for k in range(-4, 14):
        ctx.rectangle(k * 120, -500, 8, 3000); setc(ctx, hx('bfc9d8')); ctx.fill()
    ts = press_times()
    lit = {7} | {n_ for n_, t in zip(ORDER, ts) if il >= t}
    panel(ctx, PX, PY, PS, lit, 0.5 + 0.5 * math.sin(il * 0.8))
    # finger position: hops from button to button
    pts = [(PX + bpos(n_)[0] * PS, PY + bpos(n_)[1] * PS) for n_ in ORDER]
    start = (PX + 260, PY + 700)
    if il < ts[0]:
        a, b, u = start, pts[0], eio(pop(il, 0, ts[0]))
    elif il >= ts[-1]:
        a, b, u = pts[-1], (PX + 300, PY + 640), eio(pop(il, ts[-1] + 3, ts[-1] + 10))
    else:
        k = max(i for i, t in enumerate(ts) if il >= t)
        a, b = pts[k], pts[k + 1]
        u = eio(pop(il, ts[k] + 1.2, ts[k + 1]))
    fx, fy = lerp(a[0], b[0], u), lerp(a[1], b[1], u) - 30 * math.sin(math.pi * u)
    finger(ctx, fx - 8, fy - 8, 0.8)
    ctx.restore()
    for k, t in enumerate(ts):
        if t <= il < t + 6:
            x, y = pts[k]
            label(ctx, "BOOP!", min(860, max(220, x + (-160 if k % 2 else 160))), y - 60, 70, YEL, 0.1 * (-1) ** k, pop(il, t, t + 2))
    if il >= ts[-1] + 4:
        label2(ctx, "\"ALL OF", "THEM!!\"", WHITE, pop(il, ts[-1] + 4, ts[-1] + 8), 120, col2=GREEN, y=1400)


def s2(ctx, f):
    lf = f - 54
    if lf < 56:
        interior(ctx, f, lf)
    elif lf < 116:
        panel_macro(ctx, f, lf - 56)
    else:
        il = lf - 116   # 0..20
        dad_ecu(ctx, f, il, RED, eye='shock', mouth='scream', z0=1.05 + 0.1 * eout(pop(il, 0, 20)), shake=10)
        label(ctx, "\"NOOOO!!\"", 540, 1420, 160, YEL, -0.05, pop(il, 1, 4))


# floor stops: (start frame, floor, hallway colour, floor colour, length)
STOPS = [(190, 2, hx('ffe08a'), hx('6a5a7a'), 42), (232, 3, hx('ffb3d1'), hx('3a6a6a'), 32),
         (264, 4, hx('b8f0b0'), hx('6a4a3a'), 24), (288, 5, hx('b8d8ff'), hx('5a4a6a'), 16), (304, 6, hx('ffc9a0'), hx('4a5a7a'), 14)]


def dad_in(ctx, lf, eye='glare', mouth='wavy', x=640, **kw):
    p = P(eye=eye, mouth=mouth, lsh=10, rsh=-10); p.update(kw)
    b = draw(ctx, x, FLOOR - 186 * DK, DK, 1, DAD, p)
    return b


def kid_in(ctx, lf, x=380, eye='happy', mouth='grin', **kw):
    hop = abs(math.sin(lf * 0.45)) * 30
    p = P(eye=eye, mouth=mouth, lsh=150, rsh=-150, lel=20, rel=-20); p.update(kw)
    draw(ctx, x, FLOOR - 186 * KK - hop, KK, 1, BOY, p)


def door_o(il, ln, oa=6, cb=6):
    return min(eio(pop(il, 0, oa)), 1 - eio(pop(il, ln - cb, ln)))


def s3(ctx, f):
    k = max(i for i, s_ in enumerate(STOPS) if s_[0] <= f)
    st, fl_, col, pc, ln = STOPS[k]
    il = f - st
    o = door_o(il, ln, 6 if ln > 20 else 4, 6 if ln > 20 else 4)
    lit = set(range(fl_ + 1, 13))
    z = [0.95, 1.0, 1.05, 1.1, 1.15][k]
    rot = [0, 3, -3, 4, -4][k]
    ctx.save(); cam(ctx, 540, 900, z, rot, shake_at(il, [0], 6, 10), f)

    def inside(c):
        dad_in(c, il, eye='glare' if k < 2 else 'shock', mouth='wavy' if k < 3 else 'flat', x=660)
        kid_in(c, il, x=390)
    hallway(ctx, col, o, fl_, lit, inside, pcol=pc)
    if k == 0:
        draw(ctx, 60, FLOOR - 186 * 1.6, 1.6, 1, NB, P(eye='normal', mouth='smile', rsh=-60, rel=-80, lsh=10))
        ctx.new_path(); rect_r(ctx, 150, 1080, 50, 70, 8); fl(ctx, WHITE, 5)   # coffee cup
    if k == 2:
        draw(ctx, 1000, FLOOR - 186 * 1.5, 1.5, -1, NM, P(eye='shock', mouth='open', lsh=30, rsh=-30))
    ctx.restore()
    label(ctx, "*DING!*", 540, 330, 90 + 10 * k, YEL, (-1) ** k * 0.06, pop(il, 0, 3))
    if k == 0 and il >= 10:
        label(ctx, "\"Going DOWN?\"", 380, 1400, 100, WHITE, -0.04, pop(il, 10, 14))
    if k == 1 and il >= 8:
        label(ctx, "*cricket*", 540, 1400, 90, GREEN, 0.04, pop(il, 8, 11))
    if k == 2 and il >= 6:
        label(ctx, "\"...HI?\"", 540, 1400, 110, PINK, -0.04, pop(il, 6, 9))
    if k >= 3:
        label(ctx, f"FLOOR {fl_}!", 540, 1400, 130 + 10 * (k - 3), ORANGE, (-1) ** k * 0.05, pop(il, 0, 2))


def split(ctx, f, il):
    ctx.save(); ctx.rectangle(0, 0, W, H / 2); ctx.clip()
    ctx.translate(0, -300)
    dad_ecu(ctx, f, il, PURPLE, eye='glare', mouth='flat', z0=0.85, shake=2)
    ctx.restore()
    ctx.save(); ctx.rectangle(0, H / 2, W, H / 2); ctx.clip()
    ctx.translate(0, 560)
    kid_ecu(ctx, f, il, GOLD, z0=0.8, eye='happy', mouth='grin', spark=False)
    ctx.restore()
    ctx.rectangle(0, H / 2 - 8, W, 16); setc(ctx, OUT); ctx.fill()
    label2(ctx, "\"...floor...", "SIX.\"", WHITE, pop(il, 3, 7), 96, col2=YEL, y=860)
    label2(ctx, "\"BEST. RIDE.", "EVER!!\"", WHITE, pop(il, 14, 18), 110, col2=GREEN, y=1400)


def s4(ctx, f):
    lf = f - 318
    if lf < 40:
        split(ctx, f, lf)
        return
    il = lf - 40   # 0..112 floor 7
    CLOSE0, CLOSE1 = 76, 90
    o = eio(pop(il, 0, 8)) if il < CLOSE0 else 1 - eio(pop(il, CLOSE0, CLOSE1))
    LEAN = 46; BOOP = 60
    lit = set(range(8, 13)) if il >= BOOP else set()
    blink = 0.5 + 0.5 * math.sin(il * 0.9)
    fl_ = 7 if il < 92 else min(12, 7 + int((il - 92) / 3.5) + 1)
    zoom = 1.0 if il < 92 else lerp(1.0, 0.85, eio(pop(il, 92, 112)))
    ctx.save(); cam(ctx, 540, 900, zoom, 0, shake_at(il, [BOOP], 12, 16), f)

    def inside(c):
        if il < LEAN:
            dad_in(c, il, eye='happy', mouth='grin', x=540, lsh=150, rsh=-150, lel=20, rel=-20)
        else:
            u = eio(pop(il, LEAN, BOOP))
            if il < BOOP:
                dad_in(c, il, eye='closed', mouth='smile', x=lerp(540, 690, u), torso=-10 * u, lsh=40, rsh=-40)
            else:
                dad_in(c, il, eye='shock', mouth='scream', x=690, torso=-6, lsh=160, rsh=-160, lel=20, rel=-20)
        if il < 12:
            kid_in(c, il, x=340)
    hallway(ctx, hx('a8e6ff'), o, fl_, lit, inside, blink=blink, pcol=hx('4a4a7a'))
    if il >= 12:
        u = eio(pop(il, 12, 30))
        kx = lerp(340, 160, u); hop = 120 * math.sin(math.pi * pop(il, 12, 30))
        wave = il >= CLOSE1
        draw(ctx, kx, FLOOR - 186 * KK - hop, KK, 1, BOY,
             P(eye='happy', mouth='grin', rsh=-150 + (30 * math.sin(il * 0.8) if wave else 0), rel=-20, lsh=20 if wave else 150, lel=0 if wave else 20))
    ctx.restore()
    if il < 40:
        label(ctx, "FLOOR 7!", 540, 330, 90, ORANGE, -0.05, pop(il, 0, 3))
        label2(ctx, "\"FINALLY!!\"", "", WHITE, pop(il, 6, 10), 130, y=1440)
    elif il < BOOP:
        label(ctx, "\"Phew...\"", 600, 1400, 120, WHITE, 0.04, pop(il, LEAN, LEAN + 4))
    elif il < 92:
        label(ctx, "*BOOP-BOOP-BOOP!*", 540, 1400, 96, YEL, -0.05, pop(il, BOOP, BOOP + 3))
    else:
        label2(ctx, "\"BYE,", "DAD!!\"", WHITE, pop(il, 92, 96), 120, col2=GREEN, y=1400)
        # Dad's scream drifting upward and shrinking
        u = pop(il, 92, 112)
        label(ctx, "\"NOOOOO...\"", 600, lerp(860, 340, u), lerp(110, 60, u), YEL, 0.05, 1)


def s5(ctx, f):
    lf = f - 470
    if lf < 92:
        o = eio(pop(lf, 0, 8))
        fl_ = 12
        walk_in = pop(lf, 54, 78)
        ctx.save(); cam(ctx, 540, 900, 1.0 + 0.06 * eio(pop(lf, 0, 90)), 0, shake_at(lf, [0], 8, 12), f)

        def inside(c):
            dad_in(c, lf, eye='glare', mouth='wavy', x=610, torso=10, head=12, lsh=5, rsh=-5)
        hallway(ctx, hx('d6c2ff'), o, fl_, set(), inside, pcol=hx('3a3a5a'))
        if walk_in <= 0:
            kx = lerp(-200, 240, eio(pop(lf, 22, 34)))
            draw(ctx, kx, FLOOR - 186 * KK, KK, 1, BOY, P(eye='happy', mouth='grin', rsh=-150, rel=-20, lsh=20))
            if lf >= 22:
                sweat(ctx, kx + 70, FLOOR - 186 * KK * 2.3, lf, 0.8)
        else:
            kx = lerp(240, 400, eio(walk_in))
            draw(ctx, kx, FLOOR - 186 * KK, KK, 1, BOY, walk(lf * 0.6, eye='happy', mouth='grin') if walk_in < 1 else
                 P(eye='shock', mouth='grin', head=-8, rsh=-120, rel=-30, lsh=10))
        ctx.restore()
        label(ctx, "FLOOR 12.", 540, 330, 90, ORANGE, 0.04, pop(lf, 0, 3))
        if lf < 22:
            label(ctx, "*ding.*", 540, 1400, 100, WHITE, -0.04, pop(lf, 2, 5))
        elif lf < 56:
            label2(ctx, "\"HI DAD! I took", "the STAIRS!\"", WHITE, pop(lf, 24, 28), 96, col2=GREEN, y=1400)
        elif lf >= 76:
            label(ctx, "*sparkle*", 540, 1400, 100, YEL, -0.04, pop(lf, 76, 79))
    elif lf < 140:
        il = lf - 92
        kid_ecu(ctx, f, il, GOLD, z0=1.0 + 0.12 * eio(pop(il, 0, 48)))
        # finger creeping toward a glowing button in the corner
        u = eio(pop(il, 6, 40))
        ctx.save()
        ctx.new_path(); ctx.arc(760, 1300, 100, 0, 2 * math.pi); setc(ctx, (1, 0.95, 0.4, 0.5)); ctx.fill()
        ctx.new_path(); ctx.arc(760, 1300, 76, 0, 2 * math.pi); fl(ctx, hx('e8edf5'), 7)
        num(ctx, "7", 760, 1300, 76, hx('5a6478'))
        finger(ctx, lerp(1050, 790, u), lerp(1800, 1330, u), 0.75)
        ctx.restore()
        label(ctx, "\"...boop?\"", 540, 330, 120, WHITE, -0.05, pop(il, 20, 24))
    else:
        s1(ctx, f, f - 610 + 8)


SHOTS = [(0, s1), (54, s2), (190, s3), (318, s4), (470, s5)]
CUTS = (54, 110, 170, 190, 232, 264, 288, 304, 318, 358, 470, 562, 610)


def render(f):
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
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/v{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/dont_touch_the_buttons_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
