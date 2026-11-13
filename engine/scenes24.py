"""'Blank In The Exam' - original, general-audience comedy short, ~22s.
ECU: kid staring at the exam paper, sweating: "MIND: BLANK." / "WHAT'S A NUMBER?!"
Flashback: last night at home he answered Mom's flash cards like a genius ("56! EASY!").
Zoom INTO his head: his brain is dancing to a song, opens the MATHS drawer -> empty, a moth flies out.
Clock spins, teacher: "PENS DOWN!" Twist: one step out of the classroom, lightbulb DING - every answer floods back.
"NOW you remember?!" Loops back to the opening ECU."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, label, shake_at
import scenes13
from scenes13 import card as _card13
import random

BOY, MOM, TEACH = doodle.BOY, doodle.MOM_G, doodle.NMOM
N = 660
FLOOR = 1430
KB = 1.45

CAPS = {
    'p1': [[("THE ", OUT), ("EXAM", hx('ff3b5c')), (" STARTS...", OUT)]],
    'p2': [[("LAST NIGHT ", OUT), ("AT HOME", hx('1f8bff')), (":", OUT)]],
    'p3': [[("MEANWHILE, ", OUT), ("MY BRAIN", hx('ff4fa0')), (":", OUT)]],
    'p4': [[("THE ", OUT), ("CLOCK", hx('ff8a1f')), (" HAS NO MERCY", OUT)]],
    'p5': [[("PLOT TWIST: ", OUT)], [("1 SECOND ", hx('8a3cff')), ("AFTER THE EXAM", OUT)]],
}
scenes13.CAPS = CAPS
card = _card13

BOARD, WALLC = hx('2f6b4f'), hx('9ad8c8')
PINK, PINK2 = hx('ff8fb8'), hx('e0608f')


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


def ptext(ctx, s, x, y, size, col=INK, ang=0, anchor='c'):
    text(ctx, s, x, y, size, col, outline=col, ow=1, ang=ang, anchor=anchor, shadow=False)


# ------------------------------------------------------------------ props
def paper(ctx, x, y, w, h, a=0.0, lines=(), blank=True, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.rectangle(-w / 2 + 10, -h / 2 + 12, w, h); setc(ctx, (0, 0, 0, 0.18)); ctx.fill()
    ctx.rectangle(-w / 2, -h / 2, w, h); fl(ctx, (1, 1, 1), 6)
    ctx.move_to(-w / 2 + 70, -h / 2); ctx.line_to(-w / 2 + 70, h / 2); setc(ctx, hx('ff8a9a')); ctx.set_line_width(4); ctx.stroke()
    yy = -h / 2 + 90
    for i, (s_, sz, col) in enumerate(lines):
        ptext(ctx, s_, -w / 2 + 100, yy, sz, col, anchor='l'); yy += sz * 1.5
    while yy < h / 2 - 30:
        ctx.move_to(-w / 2 + 90, yy); ctx.line_to(w / 2 - 30, yy); setc(ctx, hx('9fc6ff')); ctx.set_line_width(3); ctx.stroke(); yy += 56
    ctx.restore()


def pencil(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.rectangle(-18, -200, 36, 170); fl(ctx, hx('ffd23f'), 5)
    ctx.rectangle(-18, -230, 36, 34); fl(ctx, hx('ff8fb8'), 5)
    poly(ctx, [(-18, -30), (18, -30), (0, 20)]); fl(ctx, hx('f6d2a0'), 5)
    poly(ctx, [(-6, 4), (6, 4), (0, 20)]); setc(ctx, INK); ctx.fill()
    ctx.restore()


def bulb(ctx, x, y, s=1.0, on=1.0, t=0.0):
    if s <= 0.01:
        return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if on > 0:
        rays(ctx, 0, -10, 90, 260, t, col=(1, 0.95, 0.4), a=0.55 * on, n=14)
        ellipse(ctx, 0, -10, 130, 130); setc(ctx, (1, 0.95, 0.5, 0.35 * on)); ctx.fill()
    ellipse(ctx, 0, -20, 70, 74); fl(ctx, hx('fff27a') if on > 0.5 else hx('e8e8f0'), 7)
    ctx.move_to(-16, 10); ctx.line_to(-8, -24); ctx.line_to(8, -24); ctx.line_to(16, 10); ink(ctx, 5); ctx.stroke()
    rect_r(ctx, -32, 50, 64, 46, 10); fl(ctx, hx('a0a6b8'), 6)
    for yy in (64, 80):
        ctx.move_to(-32, yy); ctx.line_to(32, yy); ink(ctx, 4); ctx.stroke()
    ctx.restore()


def clock(ctx, x, y, r, mins, blur=0.0):
    ellipse(ctx, x, y, r + 22, r + 22); fl(ctx, hx('ff3b5c'), 8)
    ellipse(ctx, x, y, r, r); fl(ctx, (1, 1, 1), 6)
    for k in range(12):
        a_ = k * math.pi / 6
        ctx.move_to(x + math.cos(a_) * r * 0.82, y + math.sin(a_) * r * 0.82)
        ctx.line_to(x + math.cos(a_) * r * 0.94, y + math.sin(a_) * r * 0.94); ink(ctx, 8 if k % 3 == 0 else 4); ctx.stroke()
    am = mins / 60 * 2 * math.pi - math.pi / 2
    ah = mins / 720 * 2 * math.pi - math.pi / 2 + 1.0
    if blur > 0:
        ctx.move_to(x, y); ctx.arc_negative(x, y, r * 0.78, am, am - blur); ctx.close_path(); setc(ctx, (0.2, 0.2, 0.3, 0.25)); ctx.fill()
    ctx.move_to(x, y); ctx.line_to(x + math.cos(ah) * r * 0.5, y + math.sin(ah) * r * 0.5); ink(ctx, 16); ctx.stroke()
    ctx.move_to(x, y); ctx.line_to(x + math.cos(am) * r * 0.78, y + math.sin(am) * r * 0.78); ink(ctx, 10); ctx.stroke()
    ellipse(ctx, x, y, 14, 14); setc(ctx, INK); ctx.fill()


def note(ctx, x, y, s=1.0, col=hx('8a3cff')):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.rectangle(14, -90, 10, 90); setc(ctx, col); ctx.fill()
    ctx.move_to(24, -90); ctx.curve_to(60, -70, 60, -40, 44, -20); ctx.curve_to(50, -45, 40, -60, 24, -62); ctx.close_path(); setc(ctx, col); ctx.fill()
    ellipse(ctx, 0, 0, 28, 20, -0.4); fl(ctx, col, 5)
    ctx.restore()


def brain(ctx, x, y, s=1.0, eye='normal', mouth='grin', ph=0.0, arms=(30, -30), legs=True):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if legs:
        for side in (-1, 1):
            fx = side * 50 + 14 * math.sin(ph + (0 if side < 0 else math.pi))
            fy = 190 - 20 * max(0, math.sin(ph + (0 if side < 0 else math.pi)))
            ctx.move_to(side * 40, 80); ctx.line_to(fx, fy); ink(ctx, 14); ctx.stroke()
            ellipse(ctx, fx + side * 14, fy + 6, 30, 16); fl(ctx, hx('ff3b5c'), 5)
    for side, ang in ((-1, arms[0]), (1, arms[1])):
        sx_, sy_ = side * 128, 10
        a_ = math.radians(ang)
        ex, ey = sx_ + side * math.cos(a_) * 90, sy_ - math.sin(a_) * 90
        ctx.move_to(sx_, sy_); ctx.line_to(ex, ey); ink(ctx, 14); ctx.stroke()
        ellipse(ctx, ex, ey, 20, 20); fl(ctx, (1, 1, 1), 5)
    rx, ry, n = 140, 108, 15
    ctx.new_path()
    for i in range(n):
        a_ = i * 2 * math.pi / n + math.pi
        cx_, cy_ = rx * math.cos(a_), ry * math.sin(a_) * (1.0 if math.sin(a_) < 0 else 0.92)
        ctx.arc(cx_, cy_, 40, a_ - 1.2, a_ + 1.2)
    ctx.close_path(); fl(ctx, PINK, 8)
    ctx.save(); setc(ctx, PINK2); ctx.set_line_width(7); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(0, -120); ctx.curve_to(-20, -80, 20, -60, 0, -30); ctx.stroke()
    for sx_ in (-1, 1):
        ctx.move_to(sx_ * 110, -60); ctx.curve_to(sx_ * 70, -80, sx_ * 80, -40, sx_ * 50, -50); ctx.stroke()
        ctx.move_to(sx_ * 130, 50); ctx.curve_to(sx_ * 100, 30, sx_ * 110, 80, sx_ * 80, 70); ctx.stroke()
    ctx.restore()
    for ex in (-42, 42):
        if eye == 'shock':
            ellipse(ctx, ex, 10, 30, 36); fl(ctx, (1, 1, 1), 5); ellipse(ctx, ex, 14, 8, 9); setc(ctx, INK); ctx.fill()
        elif eye == 'happy':
            ink(ctx, 8); ctx.new_path(); ctx.arc(ex, 18, 18, math.pi * 1.1, math.pi * 1.9); ctx.stroke()
        else:
            ellipse(ctx, ex, 10, 22, 26); fl(ctx, (1, 1, 1), 5); ellipse(ctx, ex + 4, 14, 9, 11); setc(ctx, INK); ctx.fill()
    if mouth == 'grin':
        ctx.new_path(); ctx.arc(0, 48, 30, 0.2, math.pi - 0.2); ctx.close_path(); fl(ctx, hx('8a1c2c'), 5)
    elif mouth == 'open':
        ellipse(ctx, 0, 60, 18, 22); fl(ctx, hx('8a1c2c'), 5)
    else:
        ctx.move_to(-18, 60); ctx.line_to(18, 60); ink(ctx, 6); ctx.stroke()
    ctx.restore()


def moth(ctx, x, y, t, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    w = 0.35 + 0.65 * abs(math.sin(t * 1.6))
    for side in (-1, 1):
        ctx.save(); ctx.scale(side * w, 1)
        ellipse(ctx, 34, -10, 36, 26, -0.3); fl(ctx, hx('c8bfae'), 5)
        ellipse(ctx, 26, 20, 22, 16, 0.4); fl(ctx, hx('b0a690'), 5)
        ctx.restore()
    ellipse(ctx, 0, 0, 10, 30); fl(ctx, hx('6b5e4a'), 4)
    for side in (-1, 1):
        ctx.move_to(side * 4, -26); ctx.curve_to(side * 10, -48, side * 22, -52, side * 26, -46); ink(ctx, 3); ctx.stroke()
    ctx.restore()


def cabinet(ctx, x, y, open_=0.0):
    rect_r(ctx, x - 130, y - 260, 260, 520, 12); fl(ctx, hx('8aa0b8'), 8)
    for k in range(3):
        dy = y - 245 + k * 170
        if k == 0 and open_ > 0:
            ctx.rectangle(x - 115, dy, 230, 150); setc(ctx, hx('2a2a3a')); ctx.fill()
            u = open_
            ctx.save(); ctx.translate(x, dy + 75 + 60 * u); ctx.scale(1 + 0.18 * u, 1 + 0.18 * u)
            ctx.rectangle(-150, -70 - 60 * u, 300, 60 * u + 10); fl(ctx, hx('6b7f96'), 6)
            rect_r(ctx, -115, -70, 230, 140, 8); fl(ctx, hx('a8bcd2'), 6)
            rect_r(ctx, -50, -10, 100, 24, 10); fl(ctx, hx('d8dde8'), 4)
            ctx.rectangle(-80, -55, 160, 38); fl(ctx, (1, 1, 1), 3); ptext(ctx, "MATHS", 0, -36, 30)
            ctx.restore()
        else:
            rect_r(ctx, x - 115, dy, 230, 150, 8); fl(ctx, hx('a8bcd2'), 6)
            rect_r(ctx, x - 50, dy + 65, 100, 24, 10); fl(ctx, hx('d8dde8'), 4)
            ctx.rectangle(x - 80, dy + 20, 160, 38); fl(ctx, (1, 1, 1), 3)
            ptext(ctx, ("MATHS", "SONGS", "SNACKS")[k], x, dy + 39, 30)


def desk(ctx, x0, x1, y):
    ctx.rectangle(x0, y, x1 - x0, 60); fl(ctx, hx('c98a52'), 8)
    ctx.rectangle(x0 + 10, y + 60, x1 - x0 - 20, 30); fl(ctx, hx('a86b3a'), 6)


# ------------------------------------------------------------------ sets
def classroom(ctx):
    ctx.rectangle(-2000, -2000, 5000, 5000); setc(ctx, WALLC); ctx.fill()
    for i in range(-20, 30):
        ctx.rectangle(i * 160, -2000, 70, 5000); setc(ctx, (1, 1, 1, 0.12)); ctx.fill()
    rect_r(ctx, -300, 420, 1680, 560, 16); fl(ctx, hx('8a5a34'), 10)
    ctx.rectangle(-270, 450, 1620, 500); setc(ctx, BOARD); ctx.fill()
    for s_, x, y, a in (("2x + 3 = ?", 120, 560, -0.05), ("a² + b² = c²", 700, 600, 0.04), ("7 x 8", 360, 820, 0.02), ("√49", 960, 840, -0.06)):
        text(ctx, s_, x, y, 64, (1, 1, 1, 0.75), outline=(1, 1, 1, 0.75), ow=1, ang=a, shadow=False)
    ctx.rectangle(-2000, FLOOR, 5000, 1200); setc(ctx, hx('d7b98c')); ctx.fill()
    for i in range(-20, 30):
        ctx.move_to(i * 120, FLOOR); ctx.line_to(i * 120, FLOOR + 1200); setc(ctx, (0, 0, 0, 0.08)); ctx.set_line_width(5); ctx.stroke()
    ctx.move_to(-2000, FLOOR); ctx.line_to(3000, FLOOR); ink(ctx, 8); ctx.stroke()


def bedroom(ctx):
    ctx.rectangle(-2000, -2000, 5000, 5000); setc(ctx, hx('ffd6a0')); ctx.fill()
    for i in range(-20, 30):
        for j in range(-6, 14):
            sparkle(ctx, i * 150 + (j % 2) * 75, j * 150, 14, hx('ffc070'))
    rect_r(ctx, 640, 520, 300, 220, 12); fl(ctx, hx('bfe8ff'), 8)
    ctx.move_to(790, 520); ctx.line_to(790, 740); ctx.move_to(640, 630); ctx.line_to(940, 630); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 700, 580, 26, 26); setc(ctx, hx('fff6c8')); ctx.fill()
    ctx.rectangle(-2000, FLOOR, 5000, 1200); setc(ctx, hx('6b8ad9')); ctx.fill()
    ctx.move_to(-2000, FLOOR); ctx.line_to(3000, FLOOR); ink(ctx, 8); ctx.stroke()


def corridor(ctx):
    ctx.rectangle(-2000, -2000, 5000, 5000); setc(ctx, hx('ffe7a8')); ctx.fill()
    cols = (hx('1f8bff'), hx('ff6f9a'), hx('2fbf8a'), hx('ff8a1f'))
    for i in range(-6, 14):
        x = i * 150
        rect_r(ctx, x, 620, 140, FLOOR - 640, 8); fl(ctx, cols[i % 4], 7)
        for k in range(3):
            ctx.move_to(x + 40, 680 + k * 22); ctx.line_to(x + 100, 680 + k * 22); ink(ctx, 4); ctx.stroke()
        ctx.rectangle(x + 108, 960, 12, 50); setc(ctx, INK); ctx.fill()
    ctx.rectangle(-2000, FLOOR, 5000, 1200); setc(ctx, hx('c8ccd8')); ctx.fill()
    for i in range(-20, 30):
        ctx.rectangle(i * 160, FLOOR + (i % 2) * 80, 80, 80); setc(ctx, (1, 1, 1, 0.35)); ctx.fill()
    ctx.move_to(-2000, FLOOR); ctx.line_to(3000, FLOOR); ink(ctx, 8); ctx.stroke()


def inside_head(ctx, t):
    g = cairo.RadialGradient(540, 1000, 100, 540, 1000, 1200)
    g.add_color_stop_rgb(0, 1, 0.78, 0.86); g.add_color_stop_rgb(1, 0.62, 0.32, 0.55)
    ctx.rectangle(-500, -500, 2100, 2900); ctx.set_source(g); ctx.fill()
    # eye-windows looking out at the exam
    for ex in (330, 750):
        ellipse(ctx, ex, 620, 170, 110); fl(ctx, (1, 1, 1), 10)
        ctx.save(); ellipse(ctx, ex, 620, 160, 100); ctx.clip()
        paper(ctx, ex, 650, 260, 300, 0.05, [("Q1. ?", 40, INK)])
        ctx.restore()
    ctx.move_to(-100, 1460); ctx.curve_to(300, 1380, 780, 1380, 1180, 1460); ctx.line_to(1180, 2000); ctx.line_to(-100, 2000); ctx.close_path()
    fl(ctx, hx('c9578a'), 8)


# ------------------------------------------------------------------ shots
_SCR = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4))


def probe(x, hipy, k, f_, ch, p):
    return draw_hip(_SCR, x, hipy, k, f_, ch, p)


def flash_border(ctx, t):
    """dreamy cloud border for the flashback"""
    rnd = random.Random(5)
    ctx.rectangle(0, 0, W, H); setc(ctx, (1, 0.85, 0.5, 0.12)); ctx.fill()
    pts = [(x, -10) for x in range(0, W + 1, 120)] + [(x, H + 10) for x in range(0, W + 1, 120)] + \
          [(-10, y) for y in range(0, H + 1, 140)] + [(W + 10, y) for y in range(0, H + 1, 140)]
    for (x, y) in pts:
        r = 70 + 18 * math.sin(t * 0.15 + rnd.uniform(0, 6))
        ctx.new_sub_path(); ellipse(ctx, x, y, r, r)
    setc(ctx, (1, 1, 1, 0.85)); ctx.fill()


def exam_face(ctx, f, lf, z=1.95, loop=False, zoom_in=0.0):
    pb = P(rsh=30, rel=20, lsh=25, lel=20, eye='shock', mouth='wavy', torso=6, head=-4)
    pr = probe(540, 1300, KB, 1, BOY, pb)
    hd, R = pr['head'], pr['R']
    zz = z * (1 + 7 * ein(zoom_in))
    ctx.save()
    cam(ctx, hd[0] + R * 0.1 * ein(zoom_in), hd[1] + 30 - R * 0.55 * ein(zoom_in), zz, 2 * math.sin(lf * 0.2), shake_at(lf, [0, 30], 8, 10) + 3, f, sy=860)
    classroom(ctx)
    rays(ctx, hd[0], hd[1], R * 1.2, 1600, lf * 0.02, col=(1, 1, 1), a=0.18, n=16)
    draw_hip(ctx, 540, 1300, KB, 1, BOY, pb)
    for j, (dx, ph) in enumerate(((-1.15, 0), (1.2, 7), (1.05, 15))):
        tt = ((lf + ph) % 22) / 22
        sweat(ctx, hd[0] + dx * R, hd[1] - R * 0.3 + tt * R * 0.9, 1.4 - 0.2 * j)
    dy = hd[1] + R * 1.45
    ctx.rectangle(-200, dy + 60, 1480, 1400); fl(ctx, hx('a86b3a'), 8)
    for k in range(4):
        ctx.move_to(-200, dy + 160 + k * 110); ctx.line_to(1280, dy + 160 + k * 110); setc(ctx, (0, 0, 0, 0.12)); ctx.set_line_width(6); ctx.stroke()
    desk(ctx, -200, 1280, dy)
    paper(ctx, 540, dy - 10, 520, 120, 0.04, [], s=1.0)
    pencil(ctx, 760 + 4 * math.sin(lf * 2.1), dy - 40, 0.5 + 0.05 * math.sin(lf * 2.7), 0.8)
    ctx.restore()
    if zoom_in < 0.3:
        label(ctx, "MIND: BLANK.", 540, 1440, 120, (1, 1, 1), -0.04, 1 if loop else pop(lf, 2, 6))


def s1(ctx, f):
    if f < 62:
        exam_face(ctx, f, f)
    else:
        lf = f - 62
        # paper insert: top-down, pencil trembling
        ctx.save(); cam(ctx, 540, 960, lerp(1.0, 1.08, lf / 58), -2, shake_at(lf, [0], 6, 10), f)
        ctx.rectangle(-500, -500, 2100, 2900); setc(ctx, hx('c98a52')); ctx.fill()
        for i in range(-4, 12):
            ctx.move_to(-500, i * 180 + 40 * math.sin(i)); ctx.curve_to(200, i * 180 + 30, 800, i * 180 - 30, 1600, i * 180); setc(ctx, (0, 0, 0, 0.08)); ctx.set_line_width(6); ctx.stroke()
        paper(ctx, 520, 960, 760, 1000, -0.03, [("MATHS TEST", 64, hx('ff3b5c')), ("Q1.  7 x 8 = ____", 58, INK), ("Q2.  2x + 3 = 11", 58, INK), ("Q3.  √49 = ____", 58, INK)])
        sh = 6 * math.sin(lf * 2.3)
        ctx.new_path(); ctx.move_to(1300, 1700); ctx.line_to(820 + sh, 1180)
        setc(ctx, INK); ctx.set_line_width(150); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke_preserve()
        setc(ctx, BOY['shirt']); ctx.set_line_width(134); ctx.stroke()
        pencil(ctx, 760 + sh, 1060, 0.45, 1.2)
        ellipse(ctx, 800 + sh, 1150, 70, 64); fl(ctx, BOY['skin'], 7)
        for k in range(3):
            ctx.move_to(900 + k * 30, 1080 - k * 10); ctx.line_to(940 + k * 30, 1060 - k * 10); ink(ctx, 6); ctx.stroke()
        ctx.restore()
        label(ctx, "WHAT'S A NUMBER?!", 540, 1440, 90, hx('ffe14d'), 0.03, pop(lf, 10, 14))
    card(ctx, 'p1', f, -6, 116)


def s2(ctx, f):
    lf = f - 120
    if lf < 66:
        ctx.save(); cam(ctx, 540, 1030, lerp(1.0, 1.06, lf / 66), 0, shake_at(lf, [20], 6, 10), f)
        bedroom(ctx)
        m = draw_hip(ctx, 230, FLOOR - 92 * 1.45, 1.45, 1, MOM, P(rsh=130, rel=-20, lsh=20, lel=-30, eye='happy', mouth='smile', head=6))
        hn = m['front']
        ctx.save(); ctx.translate(hn[0] + 40, hn[1] - 90); ctx.rotate(-0.08)
        rect_r(ctx, -120, -80, 240, 160, 14); fl(ctx, (1, 1, 1), 7); ptext(ctx, "7 x 8?", 0, 0, 62, hx('1f8bff'))
        ctx.restore()
        # boy on chair, confident
        ctx.rectangle(640, 1240, 300, 40); fl(ctx, hx('ff8a1f'), 7)
        for lx in (660, 900):
            ctx.rectangle(lx, 1280, 24, FLOOR - 1280); fl(ctx, hx('a86b3a'), 5)
        b = draw_hip(ctx, 790, 1240, 1.4, -1, BOY, P(rsh=150, rel=10, lsh=20, lel=-40, eye='happy' if lf > 20 else 'smug', mouth='grin', head=-6,
                                                     lhip=88, lkn=-82, rhip=95, rkn=-90, torso=-6))
        bulb(ctx, b['head'][0], b['head'][1] - b['R'] * 1.9, 0.9 * eout(pop(lf, 18, 24)), on=pop(lf, 18, 22), t=lf * 0.05)
        ctx.restore()
        flash_border(ctx, lf)
        label(ctx, "\"56! EASY!\"", 540, 1440, 130, (1, 1, 1), -0.04, pop(lf, 20, 24))
    else:
        il = lf - 66
        # low-angle hero shot: standing on the chair, books orbiting
        ctx.save(); cam(ctx, 540, 1000, 1.12, -4 + 2 * math.sin(il * 0.15), shake_at(il, [0], 8, 12), f)
        bedroom(ctx)
        rays(ctx, 540, 820, 120, 1600, il * 0.03, col=(1, 0.95, 0.4), a=0.45, n=18)
        ctx.rectangle(390, 1240, 300, 40); fl(ctx, hx('ff8a1f'), 7)
        for lx in (410, 650):
            ctx.rectangle(lx, 1280, 24, FLOOR - 1280); fl(ctx, hx('a86b3a'), 5)
        hop = 18 * abs(math.sin(il * 0.25))
        draw_hip(ctx, 540, 1240 - 92 * 1.25 + 30 - hop, 1.25, 1, BOY, P(rsh=165, rel=10, lsh=160, lel=-10, eye='happy', mouth='grin', head=-6))
        cols = (hx('ff3b5c'), hx('1f8bff'), hx('2fbf5a'), hx('8a3cff'), hx('ff8a1f'))
        for k in range(5):
            a_ = il * 0.08 + k * 2 * math.pi / 5
            bx, by = 540 + math.cos(a_) * 360, 880 + math.sin(a_) * 140
            ctx.save(); ctx.translate(bx, by); ctx.rotate(a_ * 0.5)
            rect_r(ctx, -60, -42, 120, 84, 8); fl(ctx, cols[k], 6); ctx.rectangle(-60, 26, 120, 14); setc(ctx, (1, 1, 1)); ctx.fill()
            ctx.restore()
        clap = abs(math.sin(il * 0.6))
        draw_hip(ctx, 150, FLOOR - 92 * 1.2, 1.2, 1, MOM, P(rsh=70 + 20 * clap, rel=-60, lsh=60 - 10 * clap, lel=-70, eye='happy', mouth='grin', head=-8))
        ctx.restore()
        flash_border(ctx, lf)
        label(ctx, "I'M A GENIUS!", 540, 1440, 120, hx('ffe14d'), 0.04, pop(il, 2, 6))
    card(ctx, 'p2', f, 122, 246)


def s3(ctx, f):
    lf = f - 250
    if lf < 34:
        exam_face(ctx, f, lf + 40, zoom_in=pop(lf, 4, 34))
        a_ = pop(lf, 26, 34)
        if a_ > 0:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 0.8, 0.88, a_)); ctx.fill()
    else:
        il = lf - 34
        ctx.save(); cam(ctx, 540, 1010, lerp(1.12, 1.0, eout(pop(il, 0, 12))), 0, shake_at(il, [62], 10, 18), f)
        inside_head(ctx, il)
        opn = eout(pop(il, 60, 70))
        cabinet(ctx, 840, 1180, opn)
        if il < 52:
            ph = il * 0.5
            bx = 420 + 30 * math.sin(il * 0.25)
            brain(ctx, bx, 1150 - 30 * abs(math.sin(ph)), 1.15, eye='happy', mouth='grin', ph=ph,
                  arms=(60 + 50 * math.sin(ph), 60 - 50 * math.sin(ph)))
            for k in range(4):
                tt = ((il * 0.03) + k / 4) % 1
                note(ctx, bx - 220 + k * 140 + 30 * math.sin(tt * 6), 980 - 340 * tt, 1.0 - 0.3 * tt,
                     (hx('8a3cff'), hx('1f8bff'), hx('ff3b5c'), hx('ff8a1f'))[k])
        else:
            ph = 0
            shock = il >= 72
            brain(ctx, lerp(460, 560, eout(pop(il, 52, 60))), 1150, 1.15, eye='shock' if shock else 'normal', mouth='open' if shock else 'grin',
                  arms=(40, 70 if not shock else 110))
            if il >= 66:
                mt = il - 66
                moth(ctx, 840 - 120 * math.sin(mt * 0.12) - mt * 3, 1000 - mt * 9, mt, 1.3)
                puff(ctx, 840, 1010, pop(il, 62, 78), 1.3)
        ctx.restore()
        if il < 52:
            label(ctx, "LA LA LA~", 540, 1440, 130, hx('ffe14d'), -0.04, pop(il, 4, 8))
        elif il < 70:
            label(ctx, "MATHS FILE...?", 540, 1440, 110, (1, 1, 1), 0.03, pop(il, 54, 58))
        else:
            label(ctx, "EMPTY.", 540, 1440, 150, hx('ff3b5c'), -0.04, pop(il, 72, 76))
    card(ctx, 'p3', f, 256, 396)


def s4(ctx, f):
    lf = f - 400
    if lf < 42:
        ctx.save(); cam(ctx, 540, 900, 1.0 + 0.004 * lf, 3 * math.sin(lf * 0.5), shake_at(lf % 10, [0], 5, 8), f)
        classroom(ctx)
        speed_lines(ctx, 540, 900, lf, alpha=0.5, n=50, inner=380)
        clock(ctx, 540, 900, 300, 30 + lf * 9, blur=1.2)
        ctx.restore()
        label(ctx, "5 MINUTES LEFT!", 540, 1440, 112, hx('ff3b5c'), 0.03, pop(lf, 2, 6))
    else:
        il = lf - 42
        ctx.save(); cam(ctx, 540, 1040, 1.06, 0, shake_at(il, [28, 50], 10, 16), f)
        classroom(ctx)
        clock(ctx, 860, 640, 75, 58)
        flop = eout(pop(il, 46, 54))
        scrib = il < 28
        bp = P(rsh=55 + (18 * math.sin(il * 1.7) if scrib else 0), rel=-30, lsh=40, lel=-30, eye='shock' if il < 46 else 'closed',
               mouth='scream' if il < 46 else 'frown', torso=lerp(14, 70, flop), head=lerp(10, 30, flop), lhip=88, lkn=-82, rhip=95, rkn=-90)
        draw_hip(ctx, 700, 1250, 1.3, -1, BOY, bp)
        desk(ctx, 380, 900, 1240)
        if il < 28:
            paper(ctx, 600, 1225, 240, 50, 0.0, [], s=1.0)
            for k in range(3):
                sparkle(ctx, 560 + 50 * k + 10 * math.sin(il + k), 1170 - 20 * k, 16 + 6 * math.sin(il * 2 + k), (1, 1, 1))
        walk = eout(pop(il, 0, 24))
        t = draw_hip(ctx, lerp(-200, 260, walk), FLOOR - 92 * 1.45, 1.45, 1, TEACH,
                     P(rsh=70 if il >= 28 else 20, rel=-20 if il >= 28 else -10, lsh=-15, lel=-10, eye='glare' if il >= 24 else 'normal',
                       mouth='open' if 28 <= il < 44 else 'flat', head=4,
                       lhip=6 + (14 * math.sin(il * 0.6) if il < 24 else 0), rhip=-6 - (14 * math.sin(il * 0.6) if il < 24 else 0)))
        if il >= 28:
            hn = t['front']
            paper(ctx, hn[0] + 70, hn[1] - 40, 160, 210, 0.2, [], s=1.0)
        ctx.restore()
        if il < 28:
            label(ctx, "SCRIBBLE SCRIBBLE", 540, 1440, 96, (1, 1, 1), -0.03, pop(il, 2, 6))
        else:
            label(ctx, "\"PENS DOWN!\"", 540, 1440, 130, hx('ff3b5c'), 0.04, pop(il, 28, 32))
    card(ctx, 'p4', f, 404, 516)


ANSWERS = [("56", hx('ff3b5c')), ("x = 4", hx('1f8bff')), ("7", hx('2fbf5a')), ("56!!", hx('8a3cff')), ("EASY", hx('ff8a1f'))]


def s5(ctx, f):
    lf = f - 520
    if lf < 106:
        ctx.save(); cam(ctx, 540, 1000, lerp(1.0, 1.14, eout(pop(lf, 16, 30))), 0, shake_at(lf, [18], 12, 20), f)
        corridor(ctx)
        # classroom door behind him, just closed
        rect_r(ctx, 60, 660, 300, FLOOR - 660, 6); fl(ctx, hx('a86b3a'), 9)
        ctx.rectangle(110, 720, 200, 140); fl(ctx, hx('bfe8ff'), 6)
        ellipse(ctx, 320, 1080, 18, 18); fl(ctx, hx('ffd23f'), 5)
        step = eout(pop(lf, 0, 14))
        ding = lf >= 18
        bp = P(rsh=-10 if lf < 64 else 150, rel=-10 if lf < 64 else 30, lsh=-15, lel=-10,
               eye='closed' if lf < 18 else ('shock' if lf < 64 else 'glare'), mouth='frown' if lf < 18 else ('scream' if lf < 64 else 'flat'),
               torso=10 if lf < 18 else 0, head=14 if lf < 18 else (-6 if lf < 64 else 0))
        b = draw_hip(ctx, lerp(360, 560, step), FLOOR - 92 * 1.45, 1.45, 1 if lf < 64 else -1, BOY, bp)
        hd, R = b['head'], b['R']
        if ding:
            bulb(ctx, hd[0], hd[1] - R * 1.75, 1.0 * eout(pop(lf, 18, 24)), on=1, t=lf * 0.05)
            for k, (s_, col) in enumerate(ANSWERS):
                tt = pop(lf, 22 + k * 5, 50 + k * 5)
                if tt > 0:
                    a_ = -math.pi / 2 + (k - 2) * 0.62
                    rr = 120 + 420 * eout(tt)
                    ax, ay = hd[0] + math.cos(a_) * rr * 1.1, hd[1] - R * 0.6 + math.sin(a_) * rr * 0.9
                    ax = max(220, min(880, ax)); ay = max(520, ay)
                    ctx.save(); ctx.translate(ax, ay); ctx.scale(max(0.01, eout(min(1, tt * 3))), max(0.01, eout(min(1, tt * 3))))
                    ellipse(ctx, 0, 0, 105, 66); fl(ctx, (1, 1, 1), 6)
                    ptext(ctx, s_, 0, 0, 48, col)
                    ctx.restore()
        ctx.restore()
        if lf < 18:
            label(ctx, "*PHEW*", 540, 1440, 120, (1, 1, 1), 0.03, pop(lf, 4, 8))
        elif lf < 64:
            label(ctx, "OH! IT'S 56!!", 540, 1440, 124, hx('ffe14d'), -0.04, pop(lf, 20, 24))
        else:
            label(ctx, "NOW YOU REMEMBER?!", 540, 1440, 72, hx('ff3b5c'), 0.03, pop(lf, 66, 70))
        card(ctx, 'p5', f, 524, 622)
    else:
        il = lf - 106
        exam_face(ctx, f, il, loop=True)
        card(ctx, 'p1', f, 626)


SHOTS = [(0, s1), (120, s2), (250, s3), (400, s4), (520, s5)]
CUTS = (62, 120, 186, 284, 400, 442, 520, 626)


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
            render(f).write_to_png(f'out/w{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/exam_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
