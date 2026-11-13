"""'Dad Joins The Video Call' - original, general-audience comedy short, ~22s.
ECU: Dad's giant face jammed against the camera: "CAN YOU SEE ME??" Kid pops in: "Dad, you're on MUTE."
Dad yells louder (still muted). "I'll fix it": ceiling-fan view, forehead-only view, potato filter.
Wide: he waves the phone around, it slips... SPLOOSH into the fish bowl. Now the fish is on the call.
Twist: Grandma joins in crisp 4K with a ring light - "...why is your dad a fish?" Loops to the ECU."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at


def label(ctx, s, x, y, size, col, ang=0, t=1.0):
    if t <= 0:
        return
    sc = 0.5 + 0.5 * eout(min(1, t * 2)) + 0.08 * math.sin(min(1, t) * math.pi)
    ctx.save(); ctx.translate(x, y); ctx.scale(sc, sc)
    text(ctx, s, 0, 0, size, col, ang=ang, ow=12, maxw=860)
    ctx.restore()
import scenes13
from scenes13 import card as _card13
import random

BOY = doodle.BOY
DAD = doodle.DAD
GRAN = dict(doodle.NMOM, hair=hx('dcdce6'), shirt=hx('ff6fa8'), glasses=hx('8a3cff'))
N = 660
FLOOR = 1430
UI = hx('1b1930')

CAPS = {
    'p1': [[("WHEN DAD JOINS", OUT)], [("THE FAMILY ", OUT), ("VIDEO CALL", hx('1f8bff'))]],
    'p2': [[("DAD... YOU'RE ON ", OUT), ("MUTE", hx('ff3b5c'))]],
    'p3': [[("DAD: \"I'LL ", OUT), ("FIX IT", hx('2fbf5a')), ("\"", OUT)]],
    'p4': [[("STILL ", OUT), ("FIXING", hx('ff8a1f')), (" IT...", OUT)]],
    'p5': [[("THEN ", OUT), ("GRANDMA", hx('8a3cff')), (" JOINS", OUT)]],
}
scenes13.CAPS = CAPS
card = _card13


def cam(ctx, cx, cy, z, rot=0, shake=0, f=0, sx=W / 2, sy=H / 2):
    rnd = random.Random(f * 31 + 7)
    dx, dy = (rnd.uniform(-1, 1) * shake, rnd.uniform(-1, 1) * shake) if shake else (0, 0)
    ctx.translate(sx + dx, sy + dy); ctx.rotate(math.radians(rot)); ctx.scale(z, z); ctx.translate(-cx, -cy)


def rect_r(ctx, x, y, w, h, r):
    ctx.new_path(); ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); ctx.close_path()


def rays(ctx, x, y, r0, r1, t, col=(1, 0.97, 0.6), a=0.8, n=12):
    for k in range(n):
        ang = k * 2 * math.pi / n + t
        ctx.move_to(x + math.cos(ang) * r0, y + math.sin(ang) * r0)
        ctx.line_to(x + math.cos(ang - 0.09) * r1, y + math.sin(ang - 0.09) * r1)
        ctx.line_to(x + math.cos(ang + 0.09) * r1, y + math.sin(ang + 0.09) * r1); ctx.close_path()
    setc(ctx, col + (a,)); ctx.fill()


_SCR = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4))


def face(ctx, ch, p, cx, cy, Rt, rot=0.0, f_=1):
    """draw a character so its head centre lands at (cx, cy) with head radius Rt"""
    b = draw_hip(_SCR, 0, 0, 1, f_, ch, p)
    hd, R = b['head'], b['R']
    s = Rt / R
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s); ctx.translate(-hd[0], -hd[1])
    draw_hip(ctx, 0, 0, 1, f_, ch, p)
    ctx.restore()


# ------------------------------------------------------------------ call UI
def call_bg(ctx):
    ctx.rectangle(0, 0, W, H); setc(ctx, UI); ctx.fill()


def tile(ctx, x, y, w, h, name, content, muted=False, glow=0.0, t=0):
    ctx.save()
    rect_r(ctx, x, y, w, h, 34); ctx.clip()
    content(ctx)
    ctx.restore()
    rect_r(ctx, x, y, w, h, 34)
    if glow > 0:
        setc(ctx, hx('2fbf5a') + (glow,)); ctx.set_line_width(16); ctx.stroke_preserve()
    ink(ctx, 8); ctx.stroke()
    # name tag
    ctx.save(); ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    fs = 40 if w > 500 else 30
    ctx.set_font_size(fs); tw = ctx.text_extents(name).x_advance
    pw = tw + 40 + (fs * 1.2 if muted else 0)
    rect_r(ctx, x + 22, y + h - fs - 46, pw, fs + 26, (fs + 26) / 2); setc(ctx, (0, 0, 0, 0.6)); ctx.fill()
    ctx.move_to(x + 42, y + h - 36); ctx.text_path(name); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.restore()
    if muted:
        mic(ctx, x + 22 + tw + 40 + fs * 0.4, y + h - 33 - fs * 0.35, fs * 0.022, slash=True, bare=True)


def mic(ctx, x, y, s, slash=True, bare=False):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if not bare:
        ellipse(ctx, 0, 0, 60, 60); fl(ctx, hx('ff3b5c'), 7)
    rect_r(ctx, -14, -34, 28, 46, 14); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.new_path(); ctx.arc(0, 2, 24, 0, math.pi); setc(ctx, (1, 1, 1)); ctx.set_line_width(7); ctx.stroke()
    ctx.move_to(0, 26); ctx.line_to(0, 38); ctx.stroke()
    if slash:
        ctx.move_to(-32, -36); ctx.line_to(32, 36); setc(ctx, hx('ff3b5c') if bare else (1, 1, 1)); ctx.set_line_width(9); ctx.stroke()
    ctx.restore()


def end_bar(ctx):
    # call controls just under the main tile (above the bottom safe zone line art only)
    for k, (col, ic) in enumerate(((hx('3a3858'), 'mic'), (hx('ff3b5c'), 'end'), (hx('3a3858'), 'cam'))):
        x = 360 + k * 180
        ellipse(ctx, x, 1600, 56, 56); fl(ctx, col, 6)
        if ic == 'mic':
            mic(ctx, x, 1600, 0.8, slash=True, bare=True)
        elif ic == 'end':
            ctx.save(); ctx.translate(x, 1606); ctx.rotate(math.pi)
            ctx.new_path(); ctx.arc(0, 0, 28, math.pi * 1.1, math.pi * 1.9); setc(ctx, (1, 1, 1)); ctx.set_line_width(14); ctx.stroke(); ctx.restore()
        else:
            rect_r(ctx, x - 26, 1584, 36, 32, 6); setc(ctx, (1, 1, 1)); ctx.fill()
            poly(ctx, [(x + 12, 1600), (x + 28, 1588), (x + 28, 1612)]); setc(ctx, (1, 1, 1)); ctx.fill()


# ------------------------------------------------------------------ backgrounds
def dad_room(ctx, ox=0, oy=0, s=1.0):
    ctx.rectangle(-2000, -2000, 6000, 6000); setc(ctx, hx('ffd9a0')); ctx.fill()
    for i in range(-20, 30):
        ctx.rectangle(i * 110, -2000, 44, 6000); setc(ctx, hx('ffcf8a')); ctx.fill()
    rect_r(ctx, 120, 560, 240, 190, 10); fl(ctx, hx('fff6e8'), 8)
    poly(ctx, [(150, 720), (230, 620), (290, 700), (330, 650), (340, 720)]); fl(ctx, hx('3fbf4a'), 5)
    ellipse(ctx, 300, 610, 22, 22); fl(ctx, hx('ffe14d'), 4)
    # lamp
    ctx.rectangle(866, 720, 12, 500); fl(ctx, hx('7a4a2c'), 4)
    poly(ctx, [(810, 730), (934, 730), (900, 620), (844, 620)]); fl(ctx, hx('ff8a1f'), 6)


def kid_room(ctx):
    ctx.rectangle(-2000, -2000, 6000, 6000); setc(ctx, hx('9fd8ff')); ctx.fill()
    for k in range(6):
        ellipse(ctx, 680 + k * 60, 1060 + 30 * (k % 2), 10, 10); setc(ctx, (1, 1, 1, 0.6)); ctx.fill()
    rect_r(ctx, 860, 1060, 70, 90, 6); fl(ctx, hx('ff8a1f'), 4)


def gran_room(ctx, t):
    ctx.rectangle(-2000, -2000, 6000, 6000); setc(ctx, hx('fff2c8')); ctx.fill()
    rays(ctx, 540, 780, 60, 1200, t * 0.02, col=(1, 1, 1), a=0.5, n=18)
    # ring light behind her
    ctx.new_path(); ctx.arc(540, 760, 250, 0, 2 * math.pi); setc(ctx, INK); ctx.set_line_width(56); ctx.stroke()
    ctx.new_path(); ctx.arc(540, 760, 250, 0, 2 * math.pi); setc(ctx, (1, 1, 0.92)); ctx.set_line_width(40); ctx.stroke()
    # plant + bookshelf
    ctx.rectangle(110, 640, 200, 22); fl(ctx, hx('c98a52'), 5)
    for k, c in enumerate(('ff3b5c', '1f8bff', '2fbf5a', 'ffd23f')):
        ctx.rectangle(130 + k * 40, 560, 32, 80); fl(ctx, hx(c), 4)
    poly(ctx, [(840, 960), (940, 960), (925, 880), (855, 880)]); fl(ctx, hx('d0703a'), 5)
    for k in range(4):
        ellipse(ctx, 865 + k * 18, 820 - 25 * (k % 2), 20, 46, -0.5 + 0.33 * k); fl(ctx, hx('3fbf4a'), 4)


def living_room(ctx):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('c8e6ff')); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 120, -3000, 50, 3000 + FLOOR); setc(ctx, hx('b6dcff')); ctx.fill()
    # window
    rect_r(ctx, 80, 560, 330, 380, 14); fl(ctx, hx('fff6c8'), 10)
    ctx.move_to(245, 560); ctx.line_to(245, 940); ctx.move_to(80, 750); ctx.line_to(410, 750); ink(ctx, 8); ctx.stroke()
    # sofa
    rect_r(ctx, -60, 1150, 420, 200, 40); fl(ctx, hx('ff6b8a'), 9)
    rect_r(ctx, -60, 1260, 460, 170, 30); fl(ctx, hx('ff8fa8'), 9)
    # side table
    ctx.rectangle(640, 1170, 360, 30); fl(ctx, hx('c98a52'), 8)
    for lx in (670, 950):
        ctx.rectangle(lx, 1200, 24, FLOOR - 1200); fl(ctx, hx('a86a3a'), 6)
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('e0a868')); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()


def fish(ctx, x, y, s, f_=1, t=0, eye='normal'):
    ctx.save(); ctx.translate(x, y); ctx.scale(s * f_, s); ctx.rotate(0.06 * math.sin(t * 0.3))
    wag = 0.25 * math.sin(t * 0.6)
    poly(ctx, [(-70, 0), (-130, -50 + 20 * wag), (-120, 0), (-130, 50 + 20 * wag)]); fl(ctx, hx('ff7a1f'), 6)
    poly(ctx, [(-10, -50), (30, -78), (40, -44)]); fl(ctx, hx('ff7a1f'), 5)
    ellipse(ctx, 0, 0, 80, 56); fl(ctx, hx('ff9a3c'), 7)
    ctx.move_to(-20, -40); ctx.curve_to(-6, -10, -6, 10, -20, 40); setc(ctx, hx('ffd23f')); ctx.set_line_width(10); ctx.stroke()
    if eye == 'shock':
        ellipse(ctx, 34, -12, 22, 24); fl(ctx, (1, 1, 1), 5); ellipse(ctx, 36, -10, 7, 8); setc(ctx, INK); ctx.fill()
    else:
        ellipse(ctx, 34, -12, 16, 18); fl(ctx, (1, 1, 1), 5); ellipse(ctx, 38, -10, 8, 9); setc(ctx, INK); ctx.fill()
    ellipse(ctx, 70, 14, 7 + 3 * math.sin(t * 0.5), 9 + 3 * math.sin(t * 0.5)); fl(ctx, hx('8a1c2c'), 4)
    ctx.restore()


def bubbles(ctx, t, x0=60, x1=1020, y0=520, y1=1420, n=14, seed=4):
    rnd = random.Random(seed)
    for k in range(n):
        bx = rnd.uniform(x0, x1); sp = rnd.uniform(3, 7); r = rnd.uniform(10, 26)
        by = y1 - ((t * sp + rnd.uniform(0, 900)) % (y1 - y0))
        ellipse(ctx, bx + 10 * math.sin(t * 0.1 + k), by, r, r); setc(ctx, (1, 1, 1, 0.75)); ctx.set_line_width(5); ctx.stroke()


def fishbowl(ctx, x, y, t, splash=0.0, phone=False):
    """bowl standing at (x, y) bottom"""
    ellipse(ctx, x, y - 120, 150, 130); setc(ctx, (0.6, 0.85, 1, 0.55)); ctx.fill()
    ctx.save(); ellipse(ctx, x, y - 120, 150, 130); ctx.clip()
    ctx.rectangle(x - 200, y - 175 - 10 * math.sin(t * 0.2), 400, 300); setc(ctx, hx('5ab8ff', 0.8) if False else (0.35, 0.7, 1, 0.8)); ctx.fill()
    if phone:
        ctx.save(); ctx.translate(x - 30, y - 50); ctx.rotate(0.5)
        rect_r(ctx, -30, -55, 60, 110, 10); fl(ctx, hx('2a2840'), 5); ctx.restore()
    fish(ctx, x + 30 * math.sin(t * 0.05), y - 110, 0.55, 1 if math.cos(t * 0.05) > 0 else -1, t, 'shock' if phone else 'normal')
    ctx.restore()
    ellipse(ctx, x, y - 120, 150, 130); ink(ctx, 8); ctx.stroke()
    ellipse(ctx, x, y - 244, 80, 18); setc(ctx, (0.9, 0.97, 1)); ctx.fill_preserve(); ink(ctx, 6); ctx.stroke()
    ellipse(ctx, x - 70, y - 170, 18, 40, 0.4); setc(ctx, (1, 1, 1, 0.7)); ctx.fill()
    if splash > 0:
        for k in range(9):
            a_ = -math.pi / 2 + (k - 4) * 0.28
            d = 60 + 340 * eout(splash)
            px, py = x + math.cos(a_) * d, y - 250 + math.sin(a_) * d + 700 * splash ** 2
            r = 22 * (1 - splash) + 6
            ellipse(ctx, px, py, r, r * 1.3); fl(ctx, hx('8fd8ff'), 4)


def potato(ctx, cx, cy, R, p, t):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(0.05 * math.sin(t * 0.2))
    ctx.new_path()
    pts = [(math.cos(a) * R * (1.05 + 0.08 * math.sin(a * 3 + 1)), math.sin(a) * R * (1.25 + 0.06 * math.cos(a * 2))) for a in [k * math.pi / 10 for k in range(20)]]
    ctx.move_to(*pts[0])
    for k in range(20):
        p0, p1 = pts[k], pts[(k + 1) % 20]
        ctx.curve_to(p0[0] + (p1[0] - pts[k - 1][0]) * 0.17, p0[1] + (p1[1] - pts[k - 1][1]) * 0.17,
                     p1[0] - (pts[(k + 2) % 20][0] - p0[0]) * 0.17, p1[1] - (pts[(k + 2) % 20][1] - p0[1]) * 0.17, *p1)
    ctx.close_path(); fl(ctx, hx('d9a75a'), 10)
    for dx, dy, r in ((-0.6, -0.7, 0.07), (0.55, -0.4, 0.05), (-0.4, 0.8, 0.06), (0.7, 0.6, 0.05), (0.1, -1.0, 0.04)):
        ellipse(ctx, dx * R, dy * R, r * R, r * R * 0.7); setc(ctx, hx('a8783a')); ctx.fill()
    lw = R * 0.035
    ctx.save(); ctx.translate(0, -R * 0.1); doodle.eyes(ctx, R * 0.9, p.get('eye', 'shock'), 0, lw); ctx.restore()
    ctx.save(); ctx.translate(0, R * 0.05); doodle.mouth(ctx, p.get('mouth', 'open'), R * 0.9, 0, lw)
    mx = R * 0.04
    ctx.new_path(); ctx.move_to(mx, R * 0.33); ctx.curve_to(mx - R * 0.15, R * 0.28, mx - R * 0.3, R * 0.34, mx - R * 0.34, R * 0.46)
    ctx.curve_to(mx - R * 0.2, R * 0.4, mx - R * 0.08, R * 0.42, mx, R * 0.39)
    ctx.curve_to(mx + R * 0.08, R * 0.42, mx + R * 0.2, R * 0.4, mx + R * 0.34, R * 0.46)
    ctx.curve_to(mx + R * 0.3, R * 0.34, mx + R * 0.15, R * 0.28, mx, R * 0.33); ctx.close_path(); fl(ctx, DAD['moustache'], lw)
    ctx.restore()
    ctx.restore()


def talk(lf, a='open', b='scream', rate=4):
    return a if (lf // rate) % 2 == 0 else b


# ------------------------------------------------------------------ shots
MAIN = (60, 520, 960, 900)


def opening_face(ctx, f, lf, loop=False, lab=True):
    call_bg(ctx)
    pd = P(eye='shock', mouth=talk(lf, 'scream', 'open', 5), head=-8, torso=-4, rsh=20, lsh=-20)

    def c(ctx):
        sh = shake_at(lf, [0], 10, 16) + 3
        ctx.save(); cam(ctx, 540, 970, 1.0, 0, sh, f)
        dad_room(ctx)
        face(ctx, DAD, pd, 520 + 10 * math.sin(lf * 0.3), 1000, 430 + 14 * math.sin(lf * 0.5), -0.12)
        sweat(ctx, 140, 760 + (lf % 20) * 6, 2.0)
        ctx.restore()
    tile(ctx, *MAIN, "DAD", c, muted=True, glow=0.6 + 0.4 * math.sin(lf * 0.5))
    end_bar(ctx)
    if lab:
        label(ctx, "\"CAN YOU SEE ME??\"", 540, 1450, 104, (1, 1, 1), -0.04, 1)


def kid_pip(ctx, lf, pose, x=650, y=1010, w=300, h=380, appear=0):
    u = eout(pop(lf, appear, appear + 8))
    if u <= 0:
        return
    ctx.save(); ctx.translate(x + w / 2, y + h / 2); ctx.scale(u, u); ctx.translate(-(x + w / 2), -(y + h / 2))

    def c(ctx):
        kid_room(ctx)
        face(ctx, BOY, pose, x + w / 2, y + h * 0.42, 120)
    tile(ctx, x, y, w, h, "ME", c)
    ctx.restore()


def s1(ctx, f):
    opening_face(ctx, f, f, lab=f < 56)
    if f >= 56:
        lf = f - 56
        kid_pip(ctx, lf, P(eye='normal', mouth='flat', head=6, rsh=160, rel=10), appear=0)
        label(ctx, "\"DAD. YOU'RE ON MUTE.\"", 540, 1450, 92, hx('ffe14d'), 0.03, pop(lf, 4, 8))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    call_bg(ctx)
    grow = eout(pop(lf, 0, 90))
    pd = P(eye='glare' if lf > 50 else 'shock', mouth=talk(lf, 'scream', 'open', 3), head=6 * math.sin(lf * 0.4), torso=-4)

    def c(ctx):
        ctx.save(); cam(ctx, 540, 970, 1.0 + 0.5 * grow, 2 * math.sin(lf * 0.5), 6 + 10 * grow, f)
        dad_room(ctx)
        face(ctx, DAD, pd, 540, 1000, 330 + 120 * grow, 0.08 * math.sin(lf * 0.3))
        # silent shout lines
        for k in range(6):
            a_ = -math.pi * 0.9 + k * 0.35
            r0 = 520 + 30 * math.sin(lf * 0.8 + k)
            ctx.move_to(540 + math.cos(a_) * r0, 1000 + math.sin(a_) * r0)
            ctx.line_to(540 + math.cos(a_) * (r0 + 90), 1000 + math.sin(a_) * (r0 + 90)); ink(ctx, 12); ctx.stroke()
        ctx.restore()
    tile(ctx, *MAIN, "DAD", c, muted=True)
    # giant flashing mute icon
    on = (lf // 6) % 2 == 0
    if lf >= 7:
        mic(ctx, 540, 1180, 1.6 * (1 + 0.1 * on) * eout(pop(lf, 6, 12)), slash=True)
    kid_pip(ctx, lf + 20, P(eye='closed', mouth='flat', head=-8, rsh=150, rel=60), x=650, y=560, h=330)
    end_bar(ctx)
    if lf < 50:
        label(ctx, "*SILENT YELLING*", 540, 1450, 110, (1, 1, 1), -0.04, pop(lf, 2, 6))
    else:
        label(ctx, "*LOUDER SILENT YELLING*", 540, 1450, 84, hx('ff3b5c'), 0.04, pop(lf, 50, 54))
    card(ctx, 'p2', f, 114, 216)


def s3(ctx, f):
    lf = f - 220
    call_bg(ctx)
    beat = min(2, lf // 50)
    il = lf - beat * 50

    def c(ctx):
        if beat == 0:
            # ceiling view: camera flipped
            ctx.save(); cam(ctx, 540, 970, 1.0, 0, shake_at(il, [0], 8, 18), f)
            ctx.rectangle(-500, -500, 2000, 3000); setc(ctx, hx('fff6e8')); ctx.fill()
            for k in range(-4, 12):
                ctx.move_to(k * 130, 0); ctx.line_to(k * 130 + 400, 2000); setc(ctx, (0, 0, 0, 0.05)); ctx.set_line_width(8); ctx.stroke()
            ellipse(ctx, 540, 960, 70, 70); fl(ctx, hx('c9c9d6'), 8)
            ctx.save(); ctx.translate(540, 960); ctx.rotate(il * 0.5)
            for k in range(4):
                ctx.save(); ctx.rotate(k * math.pi / 2)
                ellipse(ctx, 0, -230, 56, 190); fl(ctx, hx('a86a3a'), 8); ctx.restore()
            ctx.restore()
            ellipse(ctx, 540, 960, 50, 50); fl(ctx, hx('ffe14d'), 7)
            ctx.restore()
        elif beat == 1:
            ctx.save(); cam(ctx, 540, 970, 1.0, 0, shake_at(il, [0], 8, 18), f)
            dad_room(ctx)
            face(ctx, DAD, P(eye='normal' if il < 25 else 'shock', mouth='flat', head=0), 540 + 40 * math.sin(il * 0.15), 1420 - 40 + 8 * math.sin(il * 0.4), 470)
            ctx.restore()
        else:
            ctx.save(); cam(ctx, 540, 970, 1.0, 0, shake_at(il, [0], 10, 22), f)
            dad_room(ctx)
            rays(ctx, 540, 980, 200, 1200, il * 0.03, col=(1, 1, 1), a=0.35, n=16)
            # body under the potato
            b = draw_hip(_SCR, 0, 0, 1, 1, DAD, P())
            potato(ctx, 540, 980 + 8 * math.sin(il * 0.3), 300, P(eye='shock', mouth=talk(il, 'scream', 'open', 4)), il)
            for k in range(5):
                a_ = k * 1.25 + il * 0.08
                sparkle(ctx, 540 + math.cos(a_) * 400, 980 + math.sin(a_) * 360, 26, (1, 1, 1))
            ctx.restore()
    tile(ctx, *MAIN, "DAD", c, muted=beat < 2)
    end_bar(ctx)
    txt = ("THE CEILING CAM", "FOREHEAD MODE", "\"I AM NOT A POTATO!\"")[beat]
    col = ((1, 1, 1), hx('ffe14d'), hx('ff8a1f'))[beat]
    label(ctx, txt, 540, 1450, 100 if beat < 2 else 92, col, 0.04 * (1 if beat % 2 else -1), pop(il, 2, 6))
    card(ctx, 'p3', f, 224, 366)


PHONE_FLY = 44


def s4(ctx, f):
    lf = f - 370
    if lf < 92:
        ctx.save()
        z = lerp(0.95, 1.05, lf / 92)
        cam(ctx, 560, 1080, z, 0, shake_at(lf, [PHONE_FLY + 20], 16, 34), f)
        living_room(ctx)
        hit = PHONE_FLY + 20
        splash = pop(lf, hit, hit + 24)
        fishbowl(ctx, 830, 1172, lf, splash if lf >= hit else 0, phone=lf >= hit)
        if lf < PHONE_FLY:
            sw = math.sin(lf * 0.35)
            pk = P(rsh=165 + 15 * sw, rel=10 * sw, lsh=40, lel=-60, eye='normal', mouth=talk(lf, 'open', 'grin', 6), head=-8 * sw,
                   torso=6 * sw, lhip=10, rhip=-10)
            fdir = 1
        else:
            pk = P(rsh=150, rel=-10, lsh=120, lel=-20, eye='shock', mouth='scream', head=6, torso=8)
            fdir = 1
        b = draw_hip(ctx, 380, FLOOR - 92 * 1.35, 1.35, fdir, DAD, pk)
        hn = b['front']
        if lf < PHONE_FLY:
            ctx.save(); ctx.translate(hn[0], hn[1] - 30); ctx.rotate(0.3 * math.sin(lf * 0.35))
            rect_r(ctx, -34, -60, 68, 120, 12); fl(ctx, hx('2a2840'), 6)
            rect_r(ctx, -24, -48, 48, 92, 6); setc(ctx, hx('5ab8ff') if False else (0.4, 0.75, 1)); ctx.fill()
            ctx.restore()
        elif lf < hit:
            u = pop(lf, PHONE_FLY, hit)
            px = lerp(hn[0], 820, u); py = lerp(hn[1] - 30, 1060, u) - 520 * math.sin(math.pi * u)
            ctx.save(); ctx.translate(px, py); ctx.rotate(u * 9)
            rect_r(ctx, -34, -60, 68, 120, 12); fl(ctx, hx('2a2840'), 6); ctx.restore()
        ctx.restore()
        if lf < PHONE_FLY:
            label(ctx, "\"HOW ABOUT NOW?\"", 540, 1450, 110, (1, 1, 1), -0.04, pop(lf, 2, 6))
        elif lf < hit:
            label(ctx, "*SLIP*", 540, 1450, 140, hx('ffe14d'), 0.05, pop(lf, PHONE_FLY, PHONE_FLY + 4))
        else:
            label(ctx, "*SPLOOSH!*", 540, 1450, 150, hx('1f8bff'), -0.05, pop(lf, hit, hit + 4))
    else:
        il = lf - 92
        call_bg(ctx)

        def c(ctx):
            ctx.save(); cam(ctx, 540, 970, 1.0, 0, shake_at(il, [0], 8, 16) + 2, f)
            ctx.rectangle(-500, -500, 2000, 3000); setc(ctx, (0.3, 0.66, 1)); ctx.fill()
            for k in range(5):
                ctx.move_to(100 + k * 220, 400); ctx.curve_to(80 + k * 220, 900, 140 + k * 220, 1200, 100 + k * 220, 1500)
                setc(ctx, (1, 1, 1, 0.12)); ctx.set_line_width(40); ctx.stroke()
            bubbles(ctx, il * 3)
            fish(ctx, 540, 980, 4.2 + 0.2 * eout(pop(il, 0, 30)), -1, il, 'shock')
            ctx.restore()
        tile(ctx, *MAIN, "DAD", c, muted=True)
        end_bar(ctx)
        label(ctx, "NEW CALLER: THE FISH", 540, 1450, 92, hx('ffe14d'), 0.04, pop(il, 2, 6))
    card(ctx, 'p4', f, 374, 496)


def s5(ctx, f):
    lf = f - 500
    if lf < 120:
        call_bg(ctx)
        top = (60, 520, 960, 520)
        bot = (60, 1060, 960, 360)
        gp = P(eye='happy' if lf < 60 else 'normal', mouth='grin' if lf < 60 else 'open', head=4 * math.sin(lf * 0.2),
               rsh=150 + 15 * math.sin(lf * 0.6) if lf < 60 else 20, rel=20)
        sl = eout(pop(lf, 0, 10))

        def cg(ctx):
            ctx.save()
            gran_room(ctx, lf)
            face(ctx, GRAN, gp, 540, 740, 180)
            ctx.restore()
            for k in range(6):
                a_ = k * math.pi / 3 + lf * 0.05
                sparkle(ctx, 540 + math.cos(a_) * 380, 780 + math.sin(a_) * 200, 18 + 8 * math.sin(lf * 0.4 + k), (1, 1, 1))
            # crisp HD badge
            rect_r(ctx, 820, 550, 170, 64, 14); fl(ctx, hx('2fbf5a'), 5)
            text(ctx, "4K HD", 905, 583, 38, (1, 1, 1), ow=6, shadow=False)

        def cf(ctx):
            ctx.save()
            ctx.rectangle(-500, -500, 2000, 3000); setc(ctx, (0.3, 0.66, 1)); ctx.fill()
            bubbles(ctx, lf * 3, y0=1060, y1=1420, n=8)
            fish(ctx, 540, 1240, 2.0, -1, lf, 'normal')
            ctx.restore()
        ctx.save(); ctx.translate(0, lerp(-600, 0, sl))
        tile(ctx, *top, "GRANDMA", cg, glow=0.6 + 0.4 * math.sin(lf * 0.4))
        ctx.restore()
        tile(ctx, *bot, "DAD", cf, muted=True)
        end_bar(ctx)
        if lf < 60:
            label(ctx, "\"HELLO MY DARLINGS!\"", 540, 1450, 96, hx('ff6fa8'), -0.03, pop(lf, 4, 8))
        else:
            label(ctx, "\"...WHY IS DAD A FISH?\"", 540, 1450, 88, hx('ffe14d'), 0.04, pop(lf, 60, 64))
        card(ctx, 'p5', f, 504, 616)
    else:
        il = lf - 120
        opening_face(ctx, f, il, loop=True)
        card(ctx, 'p1', f, 620)


SHOTS = [(0, s1), (110, s2), (220, s3), (370, s4), (500, s5)]
CUTS = (56, 110, 220, 270, 320, 370, 462, 500, 620)


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.25)
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
                              "-i", "out/call_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
