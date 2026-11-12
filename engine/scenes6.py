"""Mom's Look - extended 34s story with varied camera work. Original characters."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip

BOY, MOM = doodle.BOY, doodle.MOM
N = 1020
FLOOR = 1250
SEAT = 1235          # sofa seat top (hip height when sitting)
STAND = 1500         # ground line for standing chars in room shots
KB = 1.55            # boy scale
KM = 1.9             # mom scale


# ------------------------------------------------------------------ helpers
def cam(ctx, cx, cy, z, rot=0, shake=0, f=0):
    rnd = random.Random(f * 31 + 7)
    sx, sy = (rnd.uniform(-1, 1) * shake, rnd.uniform(-1, 1) * shake) if shake else (0, 0)
    ctx.translate(W / 2 + sx, H / 2 + sy); ctx.rotate(math.radians(rot)); ctx.scale(z, z); ctx.translate(-cx, -cy)


def shake_at(f, hits, dur=10, amp=24):
    a = 0
    for h in hits:
        if h <= f < h + dur:
            a = max(a, amp * (1 - (f - h) / dur))
    return a


def pop(f, a, b):
    """0..1 progress within [a,b]"""
    return clamp((f - a) / (b - a))


def blink(f, seed=0):
    return 1 if (f + seed * 37) % 97 < 4 else 0


def sparkle(ctx, x, y, r, col=hx('fff27a')):
    poly(ctx, [(x, y - r), (x + r * 0.22, y - r * 0.22), (x + r, y), (x + r * 0.22, y + r * 0.22), (x, y + r), (x - r * 0.22, y + r * 0.22), (x - r, y), (x - r * 0.22, y - r * 0.22)])
    fl(ctx, col, 3)


def puff(ctx, x, y, t, s=1.0):
    if not 0 < t < 1:
        return
    for i in range(6):
        a = i * math.pi / 3
        d = 60 * s * eout(t)
        ellipse(ctx, x + math.cos(a) * d, y + math.sin(a) * d, 34 * s * (1 - t), 34 * s * (1 - t)); fl(ctx, (1, 1, 1), 4)
    sparkle(ctx, x, y, 40 * s * (1 - t))


def label(ctx, s, x, y, size, col, ang=0, t=1.0):
    if t <= 0:
        return
    sc = 0.5 + 0.5 * eout(min(1, t * 2)) + 0.08 * math.sin(min(1, t) * math.pi)
    ctx.save(); ctx.translate(x, y); ctx.scale(sc, sc)
    text(ctx, s, 0, 0, size, col, ang=ang, ow=12)
    ctx.restore()


CAPS = {
    'p1': [[("ME THINKING ", OUT), ("NOBODY", hx('ff3b5c'))], [("CAN CONTROL ME", OUT)]],
    'p2': [[("THEN MOM GIVES ME", OUT)], [("THE LOOK", hx('e0123a'))]],
    'p3': [[("ME, ", OUT), ("5 SECONDS", hx('1f8bff')), (" LATER", OUT)]],
    'p4': [[("MOM'S EYES ", OUT), (">", hx('e0123a')), (" ANY RULE", OUT)]],
}


def card(ctx, key, f, appear, gone=10 ** 9):
    u = min(pop(f, appear, appear + 6), 1 - pop(f, gone - 5, gone))
    if u <= 0:
        return
    lines = CAPS[key]; size = 74
    ctx.save()
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    widths = [sum(ctx.text_extents(t).x_advance for t, _ in ln) for ln in lines]
    w = max(widths) + 70; lh = size * 1.18; h = lh * len(lines) + 40
    s = 0.7 + 0.3 * eout(u)
    ctx.translate(W / 2, 300 + h / 2); ctx.scale(s, s)
    ctx.rectangle(-w / 2 + 8, -h / 2 + 10, w, h); setc(ctx, (0, 0, 0, 0.35 * u)); ctx.fill()
    ctx.rectangle(-w / 2, -h / 2, w, h); setc(ctx, (1, 1, 1, 0.97 * u)); ctx.fill_preserve(); setc(ctx, OUT + (u,)); ctx.set_line_width(5); ctx.stroke()
    y = -h / 2 + 20 + size * 0.92
    for ln, lw_ in zip(lines, widths):
        x = -lw_ / 2
        for t, col in ln:
            ctx.move_to(x, y); ctx.text_path(t); setc(ctx, col[:3] + (u,)); ctx.fill()
            x += ctx.text_extents(t).x_advance
        y += lh
    ctx.restore()


# ------------------------------------------------------------------ sets & props
def room(ctx, f, door_open=0.0, hall_light=0.0):
    ctx.rectangle(-900, -900, W + 1800, 2200); ctx.set_source(vgrad(ctx, 0, 0, 0, FLOOR, [(0, hx('fbf3e8')), (1, hx('efe2d2'))])); ctx.fill()
    # framed picture + clock
    ctx.rectangle(150, 640, 170, 140); fl(ctx, hx('9fe0ff'), 8)
    poly(ctx, [(160, 770), (230, 690), (290, 770)]); fl(ctx, hx('5fd07a'), 4)
    ellipse(ctx, 520, 700, 62, 62); fl(ctx, (1, 1, 1), 8)
    ink(ctx, 6); ctx.move_to(520, 700); ctx.line_to(520, 660); ctx.move_to(520, 700); ctx.line_to(550, 712); ctx.stroke()
    # door (right)
    ctx.rectangle(860, 560, 240, 690); fl(ctx, hx('fff6e8'), 8)
    if hall_light > 0 or door_open > 0:
        ctx.rectangle(880, 580, 200, 670); ctx.set_source(vgrad(ctx, 0, 580, 0, 1250, [(0, hx('ffe9a8')), (1, hx('ffc85a'))])); ctx.fill()
    dw = 200 * (1 - door_open * 0.85)
    ctx.rectangle(880, 580, dw, 670); fl(ctx, hx('c98b55'), 7)
    if dw > 60:
        ellipse(ctx, 880 + dw - 30, 930, 13, 13); fl(ctx, hx('ffd23f'), 4)
    # floor
    ctx.rectangle(-900, FLOOR, W + 1800, 1600); setc(ctx, hx('d8cfe0')); ctx.fill()
    ctx.move_to(-900, FLOOR); ctx.line_to(W + 900, FLOOR); ink(ctx, 8); ctx.stroke()
    for i in range(-10, 14):
        ctx.move_to(540 + i * 150, FLOOR); ctx.line_to(540 + i * 450, 2300)
    for y in (1330, 1450, 1640, 1900):
        ctx.move_to(-900, y); ctx.line_to(W + 900, y)
    setc(ctx, (0.07, 0.06, 0.08, 0.3)); ctx.set_line_width(4); ctx.stroke()
    # rug
    ellipse(ctx, 470, 1520, 420, 90); fl(ctx, hx('ffcf6b'), 6)
    ellipse(ctx, 470, 1520, 330, 64); setc(ctx, hx('ffb23e')); ctx.fill()
    # door light spill
    if door_open > 0:
        poly(ctx, [(880, 1250), (1080, 1250), (760, 1900), (200, 1900)]); setc(ctx, (1, 0.85, 0.4, 0.22 * door_open)); ctx.fill()


def sofa_back(ctx):
    ctx.rectangle(60, 1000, 720, 250); fl(ctx, hx('3fb6a8'), 8)
    for x in (90, 320, 550):
        ctx.rectangle(x, 1030, 210, 150); fl(ctx, hx('5fd0c0'), 6)


def sofa_front(ctx, cushion_mess=0.0):
    ctx.rectangle(40, 1235, 760, 120); fl(ctx, hx('34a294'), 8)
    for x, a in ((10, 0), (750, 0)):
        ctx.rectangle(x, 1110, 90, 260); fl(ctx, hx('2e9184'), 8)
    for x in (110, 640):
        ctx.rectangle(x, 1355, 24, 40); fl(ctx, hx('7a4a2c'), 4)
    if cushion_mess > 0:
        for i, (x, y, a) in enumerate(((240, 1450, 0.6), (720, 1520, -0.5))):
            ctx.save(); ctx.translate(x, y); ctx.rotate(a * cushion_mess)
            ctx.rectangle(-90, -55, 180, 110); fl(ctx, hx('5fd0c0'), 6); ctx.restore()


def coffee_table(ctx):
    ctx.rectangle(780, 1380, 300, 30); fl(ctx, hx('c98b55'), 6)
    for x in (800, 1040):
        ctx.rectangle(x, 1410, 22, 90); fl(ctx, hx('a86c3a'), 5)


def book(ctx, x, y, a, s=1.0, col=hx('2f6bff')):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.rectangle(-55, -40, 110, 80); fl(ctx, col, 6)
    ctx.rectangle(-45, -30, 40, 60); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()
    ink(ctx, 4); ctx.move_to(-55, 0); ctx.line_to(55, 0); ctx.stroke()
    ctx.restore()


def bag(ctx, x, y):
    ctx.new_path(); ctx.move_to(x - 70, y); ctx.line_to(x - 60, y - 140); ctx.curve_to(x - 40, y - 175, x + 40, y - 175, x + 60, y - 140); ctx.line_to(x + 70, y); ctx.close_path()
    fl(ctx, hx('ff6b4a'), 7)
    ctx.rectangle(x - 45, y - 80, 90, 60); fl(ctx, hx('ffcf3d'), 5)


def phone(ctx, x, y, a, glow=True):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ctx.rectangle(-55, -30, 110, 60); fl(ctx, hx('1e1e2a'), 6)
    ctx.rectangle(-46, -22, 92, 44); setc(ctx, hx('6be2ff') if glow else hx('333344')); ctx.fill()
    if glow:
        ellipse(ctx, -15, 0, 10, 10); setc(ctx, hx('ff3b8a')); ctx.fill(); ellipse(ctx, 20, -5, 7, 7); setc(ctx, hx('ffd23f')); ctx.fill()
    ctx.restore()


def chips(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-45, -70); ctx.line_to(45, -70); ctx.line_to(55, 60); ctx.line_to(-55, 60); ctx.close_path(); fl(ctx, hx('ff8c1f'), 6)
    ellipse(ctx, 0, 0, 26, 26); fl(ctx, hx('ffd23f'), 4)
    for i in range(-2, 3):
        ellipse(ctx, i * 18, -78, 9, 6); fl(ctx, hx('ffe08a'), 3)
    ctx.restore()


def crumbs(ctx, seed, n, x0, x1, y0, y1, a=1.0):
    rnd = random.Random(seed)
    for _ in range(n):
        ellipse(ctx, rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(7, 13), rnd.uniform(5, 9), rnd.uniform(0, 3))
        setc(ctx, hx('ffcf3d', a)); ctx.fill_preserve(); setc(ctx, (0.07, 0.06, 0.08, a)); ctx.set_line_width(2.5); ctx.stroke()


def note(ctx, x, y, col):
    ellipse(ctx, x, y, 22, 16, -0.4); fl(ctx, col, 4)
    ctx.rectangle(x + 14, y - 75, 9, 75); setc(ctx, INK); ctx.fill()
    ctx.move_to(x + 23, y - 75); ctx.curve_to(x + 50, y - 60, x + 50, y - 40, x + 35, y - 30); ink(ctx, 7); ctx.stroke()


# mess items: (kind, x, y, angle, pop_frame)
MESS = [('chips', 330, 1450, 0.5, 712), ('book', 150, 1600, 0.9, 728), ('cush', 240, 1450, 0.6, 744), ('crumbs', 0, 0, 0, 760),
        ('cush2', 720, 1520, -0.5, 776), ('bag', 990, 1560, 0.2, 792)]


# ------------------------------------------------------------------ shots
def s1_hook(ctx, f):
    # ECU on face as shades slide on, pull out to sofa throne
    z = kf(f, [(0, 3.4), (22, 3.4), (60, 1.08), (90, 1.0)], ease)
    cx = kf(f, [(0, 420), (22, 420), (60, 520)], ease)
    cy = kf(f, [(0, 860), (22, 860), (60, 1150)], ease)
    ctx.save(); cam(ctx, cx, cy, z, kf(f, [(0, -4), (60, 0)]), 0, f)
    room(ctx, f); sofa_back(ctx)
    sd = kf(f, [(0, -2.2), (16, 0)], eout)
    lean = ease(pop(f, 26, 50))
    pose = P(torso=-14 * lean, head=-4, lsh=lerp(20, -170, lean), lel=lerp(-30, -95, lean), rsh=lerp(-20, -165, lean), rel=lerp(-30, -95, lean),
             lhip=82, lkn=lerp(-80, -10, lean), rhip=86, rkn=lerp(-80, -6, lean), eye='smug', mouth='grin' if f > 20 else 'smile', shades=1, shades_dy=sd,
             sway=0.15 * math.sin(f * 0.3))
    h = draw_hip(ctx, 420, SEAT, KB, 1, BOY, pose)
    sofa_front(ctx)
    coffee_table(ctx)
    ctx.restore()
    if 14 <= f < 30:
        u = pop(f, 14, 30)
        sparkle(ctx, 640, 820, 120 * math.sin(u * math.pi), (1, 1, 1))
    if 70 <= f < 90:
        label(ctx, "SNAP!", 760, 980, 90, hx('ffe14d'), -0.1, pop(f, 70, 80))
    card(ctx, 'p1', f, 4, 452)


def s2_homework(ctx, f):
    lf = f - 90
    pan = ease(pop(lf, 62, 74))
    cx = lerp(760, 380, pan) if lf < 92 else lerp(380, 760, ease(pop(lf, 92, 100)))
    ctx.save(); cam(ctx, cx, 1180, 1.35, 0, shake_at(lf, [86], 10, 20), f)
    room(ctx, f); sofa_back(ctx); sofa_front(ctx); coffee_table(ctx)
    bag(ctx, 990, 1380)
    k = KB
    # pick up, look, toss
    pick = ease(pop(lf, 6, 20)); look = pop(lf, 20, 46); wind = ease(pop(lf, 46, 56)); thr = eout(pop(lf, 56, 62))
    rsh = lerp(-10, 70, pick)
    rsh = lerp(rsh, -150, wind); rsh = lerp(rsh, 60, thr)
    rel = lerp(-20, -90, pick); rel = lerp(rel, -40, wind); rel = lerp(rel, 10, thr)
    torso = lerp(0, -12, wind) + lerp(0, 14, thr)
    eye = 'smug' if lf < 20 else ('normal' if lf < 46 else 'happy')
    mouth = 'smile' if lf < 20 else ('flat' if lf < 46 else 'grin')
    pose = P(torso=torso, head=-6 if 20 <= lf < 46 else 0, lsh=35, lel=-110, rsh=rsh, rel=rel, lhip=6, rhip=-6, eye=eye, mouth=mouth, shades=1,
             blink=blink(f, 1), sway=0.3 * math.sin(lf * 0.4))
    if lf >= 62:
        pose.update(dict(lsh=-20, lel=-30, rsh=-20 + 30 * math.sin(lf * 1.2), rel=-60, eye='happy', mouth='grin'))
    h = draw(ctx, 760, STAND - 186 * k, k, 1, BOY, pose)
    if lf < 58:
        if pick > 0:
            bx, by = h['front']
            book(ctx, bx + 10, by - 30, 0.1 + wind * -1.2, 0.95)
        else:
            book(ctx, 990, 1250, 0.0, 0.95)
    elif lf < 90:
        u = pop(lf, 58, 86)
        book(ctx, lerp(820, 120, u), lerp(950, 820, u) - math.sin(u * math.pi) * 300, u * 14, 0.95)
    else:
        book(ctx, 150, 1230 if lf < 92 else 1240, 1.2, 0.95)
    ctx.restore()
    if 20 <= lf < 46:
        label(ctx, "HOMEWORK?", 540, 760, 92, hx('8fe9ff'), -0.05, pop(lf, 20, 26))
    if 58 <= lf < 82:
        label(ctx, "NAH.", 760, 820, 110, hx('ffe14d'), 0.08, pop(lf, 58, 63))
        hlines(ctx, lf, 0.35, col=INK, y0=700, y1=1300)
    if 86 <= lf < 104:
        label(ctx, "THUD!", 300, 1000, 120, hx('ff5a36'), -0.1, pop(lf, 86, 90))
    card(ctx, 'p1', f, 4, 452)


def s3_gaming(ctx, f):
    lf = f - 200
    if lf < 88:
        z, cx, cy = kf(lf, [(0, 2.4), (88, 2.55)]), 430, 900
    else:
        z = kf(lf, [(88, 2.55), (100, 1.0)], eout); cx = kf(lf, [(88, 430), (100, 520)], eout); cy = kf(lf, [(88, 900), (100, 1150)], eout)
    ctx.save(); cam(ctx, cx, cy, z, 2 * math.sin(lf * 0.05), shake_at(lf, [100], 10, 16), f)
    room(ctx, f); sofa_back(ctx)
    crumbs(ctx, 3, 30, 120, 760, 1230, 1260)
    tap = math.sin(lf * 1.7)
    win = lf >= 100
    if not win:
        pose = P(torso=6 + 3 * tap * 0.3, head=8, lsh=58, lel=-80 + 6 * tap, rsh=62, rel=-86 - 6 * tap, lhip=84, lkn=-84, rhip=86, rkn=-86,
                 eye='normal', mouth='grin' if lf % 30 < 15 else 'open', shades=0, sway=0.2 * tap, blink=blink(f, 2))
    else:
        u = pop(lf, 100, 108)
        pose = P(torso=-6, head=-8, lsh=58, lel=-80, rsh=-170, rel=-10 + 20 * math.sin(lf * 0.8), lhip=84, lkn=-84, rhip=88, rkn=-88,
                 eye='happy', mouth='grin', shades=0, sway=0.4 * math.sin(lf * 0.6))
    h = draw_hip(ctx, 420, SEAT, KB, 1, BOY, pose)
    hb = h['back']
    phone(ctx, hb[0] + 30, hb[1] - 10, -0.1 + 0.05 * tap, True)
    chips(ctx, 640, 1200, -0.25, 0.9)
    sofa_front(ctx); coffee_table(ctx)
    chips(ctx, 900, 1340, 0.6, 0.8)
    crumbs(ctx, 5, 40, 120, 1050, 1400, 1700)
    if win:
        rnd = random.Random(9)
        for i in range(30):
            t = pop(lf, 100, 130)
            x = 420 + rnd.uniform(-500, 500) * eout(t); y = 700 + rnd.uniform(-400, 200) * eout(t) + 500 * t * t
            ctx.save(); ctx.translate(x, y); ctx.rotate(i + t * 8); ctx.rectangle(-10, -5, 20, 10)
            setc(ctx, [hx('ff3b8a'), hx('ffd23f'), hx('3fb6ff'), hx('5fd07a')][i % 4]); ctx.fill(); ctx.restore()
    ctx.restore()
    if not win:
        # phone glow on face
        g = cairo.RadialGradient(540, 980, 50, 540, 980, 700); g.add_color_stop_rgba(0, 0.4, 0.9, 1, 0.22); g.add_color_stop_rgba(1, 0.4, 0.9, 1, 0)
        ctx.set_source(g); ctx.paint()
        if lf % 12 < 6:
            label(ctx, "TAP TAP", 820, 1300, 70, hx('8fe9ff'), 0.1, 1)
    else:
        label(ctx, "VICTORY!", 540, 820, 120, hx('ffe14d'), -0.06, pop(lf, 100, 106))
    card(ctx, 'p1', f, 4, 452)


DANCE = [P(torso=-5, lsh=-150, lel=-20, rsh=-60, rel=-80, lhip=-15, lkn=-10, rhip=25, rkn=-40),
         P(torso=8, lsh=60, lel=-90, rsh=-160, rel=-10, lhip=10, lkn=-30, rhip=-20, rkn=-20),
         P(torso=0, lsh=-120, lel=40, rsh=-120, rel=40, lhip=-25, lkn=-5, rhip=25, rkn=-5),
         P(torso=-10, lsh=-30, lel=-100, rsh=-170, rel=-10, lhip=0, lkn=-60, rhip=70, rkn=-110)]


def dance_pose(lf, beat=15):
    i = (lf // beat) % len(DANCE); j = (i + 1) % len(DANCE)
    u = eout(pop(lf % beat, 0, 6))
    prev = DANCE[(i - 1) % len(DANCE)]
    return kf(u, [(0, prev), (1, DANCE[i])], lambda t: t)


def s4_dance(ctx, f, frozen_at=None):
    lf = f - 330
    ff = lf if frozen_at is None else frozen_at
    beat = 15
    ph = (ff % beat) / beat
    jump = math.sin(ph * math.pi) * 120
    sq = 0.35 if ph < 0.12 or ph > 0.92 else -0.1 * math.sin(ph * math.pi)
    punch = 0.06 * math.exp(-(ff % beat) / 4)
    rot = 3 * math.sin(ff * 0.21)
    ctx.save(); cam(ctx, 470, 1030, 1.02 + punch, rot, 0, f)
    room(ctx, f); sofa_back(ctx)
    pose = dance_pose(ff)
    pose.update(eye='happy' if (ff // beat) % 2 else 'smug', mouth='grin', shades=1, headphones=1, sq=sq, sway=0.6 * math.sin(ff * 0.5))
    k = KB
    gy = SEAT + 20  # standing on cushions
    shadow_s = 1 - jump / 400
    ellipse(ctx, 430, gy + 10, 130 * shadow_s, 22 * shadow_s); setc(ctx, (0, 0, 0, 0.2)); ctx.fill()
    draw(ctx, 430, gy - 186 * k - jump, k, 1, BOY, pose)
    sofa_front(ctx, 1.0); coffee_table(ctx)
    chips(ctx, 900, 1340, 0.6, 0.8); crumbs(ctx, 5, 40, 120, 1050, 1400, 1700)
    # flying chips from bag
    rnd = random.Random(int(ff // beat))
    for i in range(5):
        t = (ff % beat) / beat
        x = 640 + rnd.uniform(-200, 300) * t; y = 1150 - rnd.uniform(200, 450) * math.sin(t * math.pi)
        ellipse(ctx, x, y, 14, 10, i); fl(ctx, hx('ffcf3d'), 3)
    ctx.restore()
    for i in range(3):
        t = ((ff + i * 13) % 40) / 40
        note(ctx, [170, 880, 780][i] + 30 * math.sin(t * 6 + i), 1250 - t * 520, [hx('ff3b8a'), hx('ffd23f'), hx('3fb6ff')][i])
    if (ff % beat) < 4:
        label(ctx, ["BOOM!", "YEAH!", "WOO!", "LET'S GO!"][(ff // beat) % 4], 820, 820, 90, hx('ffe14d'), 0.1, 1)
    card(ctx, 'p1', f, 4, 336)


def s5_freeze(ctx, f):
    lf = f - 450
    s4_dance(ctx, 450 + 0, frozen_at=124)
    # desaturate wash + shadow wedge from the door
    ctx.rectangle(0, 0, W, H); setc(ctx, (0.85, 0.85, 0.95, 0.25 + 0.15 * pop(lf, 0, 10))); ctx.fill()
    sh = ease(pop(lf, 14, 50))
    if sh > 0:
        ctx.new_path(); ctx.move_to(W + 50, 0); ctx.line_to(W + 50, H); ctx.line_to(W - 1500 * sh, H); ctx.line_to(W - 900 * sh, 0); ctx.close_path()
        setc(ctx, (0.05, 0.02, 0.1, 0.62)); ctx.fill()
    if lf < 8:
        label(ctx, "SCRRTCH!", 540, 1500, 110, hx('ff5a36'), -0.05, pop(lf, 0, 4))
    if 10 <= lf < 60:
        label(ctx, "CREEAAK...", 760, 1350, 80, (1, 1, 1), 0.05, pop(lf, 10, 18))


def s6_mom(ctx, f):
    lf = f - 510
    lit = lf >= 34
    if lf < 34:
        z, cx, cy, rot = 1.05, 760, 1050, -6
    else:
        z = kf(lf, [(34, 1.15), (60, 1.6), (78, 4.2), (90, 4.4)], ease)
        cx = kf(lf, [(34, 760), (60, 900), (78, 946)], ease); cy = kf(lf, [(34, 1050), (60, 980), (78, 915)], ease); rot = kf(lf, [(34, -6), (78, 0)])
    ctx.save(); cam(ctx, cx, cy, z, rot, shake_at(lf, [34], 8, 14) + (2 if lf > 60 else 0), f)
    room(ctx, f, door_open=1.0, hall_light=1.0)
    pose = P(torso=0, head=-4, lsh=40, lel=-135, rsh=35, rel=-138, lhip=8, rhip=-8, eye='glare', mouth='frown')
    k = KM
    mx = 960
    if not lit:
        ctx.push_group()
        h = draw(ctx, mx, STAND - 186 * k, k, -1, MOM, pose)
        pat = ctx.pop_group()
        setc(ctx, (0.05, 0.03, 0.08)); ctx.mask(pat)
        # glowing eyes in silhouette
        for e in ('eyeL', 'eyeR'):
            ex, ey = h[e]
            g = cairo.RadialGradient(ex, ey, 0, ex, ey, 70); g.add_color_stop_rgba(0, 1, 1, 1, 1); g.add_color_stop_rgba(0.35, 1, 0.2, 0.2, 0.9); g.add_color_stop_rgba(1, 1, 0, 0, 0)
            ctx.set_source(g); ellipse(ctx, ex, ey, 70, 70); ctx.fill()
    else:
        draw(ctx, mx, STAND - 186 * k, k, -1, MOM, pose)
    ctx.restore()
    if lit:
        ctx.rectangle(0, 0, W, H); setc(ctx, (1, 0.3, 0.2, 0.12 * pop(lf, 34, 50))); ctx.fill()
    if 34 <= lf < 40:
        ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.7 * (1 - pop(lf, 34, 40)))); ctx.fill()
    if lf >= 80 and lf < 90:
        u = pop(lf, 80, 90)
        sparkle(ctx, 300, 960, 160 * math.sin(u * math.pi), (1, 1, 1)); sparkle(ctx, 800, 930, 120 * math.sin(u * math.pi), (1, 1, 1))
    if lf >= 60:
        speed_lines(ctx, 540, 960, lf // 2, 0.25 + 0.2 * pop(lf, 60, 78), n=50, inner=520, col=INK)
    card(ctx, 'p2', f, 516, 692)


def s7_panic(ctx, f):
    lf = f - 600
    k = KB * kf(lf, [(0, 1.0), (58, 1.0), (72, 0.82)], eout)
    z = kf(lf, [(0, 1.6), (50, 1.7), (58, 2.4), (66, 1.7)], eout)
    ctx.save(); cam(ctx, 430, 840 if lf < 58 else kf(lf, [(58, 800), (66, 880)]), z, 0, 3 + shake_at(lf, [20], 8, 14), f)
    room(ctx, f)
    sofa_back(ctx)
    ctx.rectangle(-900, -900, W + 1800, 4000); setc(ctx, (0.35, 0.3, 0.45, 0.45)); ctx.fill()
    jit = math.sin(lf * 3.3) * 5
    sd = kf(lf, [(0, 0), (30, 0), (40, 0.55), (48, 0.6), (52, 3.0)], ein)
    base = dance_pose(124)
    stiff = ease(pop(lf, 50, 64))
    pose = kf(stiff, [(0, base), (1, P(torso=0, lsh=8, lel=-4, rsh=-8, rel=-4, lhip=4, lkn=-2, rhip=-4, rkn=-2))], lambda t: t)
    pose.update(eye='shock', mouth='wavy' if lf < 58 else 'open', shades=1 if lf < 52 else 0, shades_dy=sd, crack=lf >= 20, headphones=1, sway=0.5 * math.sin(lf * 2))
    draw(ctx, 430 + jit, SEAT + 20 - 186 * k, k, 1, BOY, pose)
    sofa_front(ctx, 1.0)
    if 52 <= lf < 70:
        u = pop(lf, 52, 70)
        ctx.save(); ctx.translate(500 + 120 * u, 900 + 550 * u * u); ctx.rotate(u * 7)
        for ex in (-34, 34):
            ellipse(ctx, ex, 0, 28, 20); fl(ctx, INK, 4)
        ctx.restore()
    ctx.restore()
    for i in range(4):
        t = ((lf + i * 6) % 18) / 18
        sweat(ctx, [270, 760, 820, 300][i], 640 + t * 300, 1.7)
    if 20 <= lf < 34:
        label(ctx, "CRACK!", 780, 760, 100, (1, 1, 1), 0.1, pop(lf, 20, 24))
    if 58 <= lf < 80:
        label(ctx, "GULP.", 540, 1450, 120, hx('8fe9ff'), -0.05, pop(lf, 58, 62))
    card(ctx, 'p2', f, 516, 692)


def s8_cleanup(ctx, f):
    lf = f - 690
    if lf < 112:
        ctx.save(); cam(ctx, 540, 1180, 1.0, 0, 0, f)
        room(ctx, f); sofa_back(ctx)
        # boy as a speed streak along a zigzag path
        path = [(150, 1450), (330, 1450), (700, 1500), (240, 1460), (900, 1550), (500, 1400), (150, 1600), (990, 1560), (430, 1450)]
        t = pop(lf, 6, 106) * (len(path) - 1)
        i = min(int(t), len(path) - 2); u = t - i
        x = lerp(path[i][0], path[i + 1][0], u); y = lerp(path[i][1], path[i + 1][1], u)
        dirx = 1 if path[i + 1][0] > path[i][0] else -1
        sofa_front(ctx, 1 - pop(lf, 54, 90))
        coffee_table(ctx)
        for kind, mxx, myy, ang, pf in MESS:
            if f < pf:
                if kind == 'chips':
                    chips(ctx, mxx, myy, ang, 0.8)
                elif kind == 'book':
                    book(ctx, mxx, myy, ang)
                elif kind == 'crumbs':
                    crumbs(ctx, 5, 40, 120, 1050, 1400, 1700)
                elif kind == 'bag':
                    bag(ctx, mxx, myy)
            else:
                puff(ctx, mxx if kind != 'crumbs' else 540, myy if kind != 'crumbs' else 1550, pop(f, pf, pf + 12))
        if 6 <= lf < 106:
            for j in range(5, 0, -1):
                ctx.push_group()
                draw(ctx, x - dirx * j * 50, y - 186 * KB, KB, dirx, BOY, run_pose(lf * 1.4, eye='shock', mouth='open', shades=0))
                ctx.pop_group_to_source(); ctx.paint_with_alpha(0.12 * (6 - j) / 5)
            draw(ctx, x, y - 186 * KB, KB, dirx, BOY, run_pose(lf * 1.4, eye='shock', mouth='open', shades=0))
            hlines(ctx, lf, 0.3, col=INK, y0=y - 500, y1=y)
        ctx.restore()
        if lf >= 100:
            label(ctx, "ROOM: CLEAN", 540, 1700, 90, hx('5fd07a'), -0.04, pop(lf, 100, 106))
    else:
        desk_scene(ctx, f, lf - 112)
    card(ctx, 'p3', f, 694, 902)


def desk_set(ctx):
    ctx.rectangle(-900, -900, W + 1800, 2200); ctx.set_source(vgrad(ctx, 0, 0, 0, FLOOR, [(0, hx('e9f6ff')), (1, hx('d6ecfb'))])); ctx.fill()
    ctx.rectangle(560, 560, 300, 330); fl(ctx, hx('bfe8ff'), 9)
    ctx.move_to(710, 560); ctx.line_to(710, 890); ctx.move_to(560, 725); ctx.line_to(860, 725); ink(ctx, 7); ctx.stroke()
    ctx.rectangle(120, 640, 300, 26); fl(ctx, hx('c98b55'), 5)
    for i, c in enumerate((hx('ff5a5a'), hx('3f8bff'), hx('5fd07a'), hx('ffd23f'))):
        ctx.rectangle(140 + i * 50, 540, 40, 100); fl(ctx, c, 4)
    ctx.rectangle(-900, FLOOR, W + 1800, 1600); setc(ctx, hx('d8cfe0')); ctx.fill()
    ctx.move_to(-900, FLOOR); ctx.line_to(W + 900, FLOOR); ink(ctx, 8); ctx.stroke()


def desk_front(ctx, pages=0):
    ctx.rectangle(140, 1200, 700, 40); fl(ctx, hx('c98b55'), 7)
    ctx.rectangle(170, 1240, 640, 300); fl(ctx, hx('b97a45'), 7)
    ctx.rectangle(220, 1300, 240, 90); fl(ctx, hx('a86c3a'), 5)
    # lamp
    ctx.move_to(760, 1200); ctx.line_to(740, 1020); ctx.line_to(660, 990); ink(ctx, 10); ctx.stroke()
    poly(ctx, [(600, 960), (700, 940), (720, 1020), (620, 1040)]); fl(ctx, hx('ffd23f'), 6)
    # stack of done pages
    for i in range(int(pages)):
        ctx.rectangle(200 + (i % 2) * 4, 1185 - i * 9, 150, 14); fl(ctx, (1, 1, 1), 3)


def desk_scene(ctx, f, dl, mom=None):
    """boy studying at desk; dl = local frame"""
    ctx.save(); cam(ctx, 520, 1080, 1.25 if mom is None else 1.05, 0, 0, f)
    desk_set(ctx)
    k = KB
    angel = dl >= 50 if mom is None else True
    if not angel:
        wr = math.sin(dl * 2.6)
        pose = P(torso=12, head=10, lsh=70, lel=-40, rsh=78 + 10 * wr, rel=-40 + 12 * wr, lhip=86, lkn=-86, rhip=88, rkn=-88, eye='shock', mouth='flat', sway=0.4 * wr)
    else:
        pose = P(torso=0, head=0, lsh=32, lel=-105, rsh=34, rel=-108, lhip=86, lkn=-86, rhip=88, rkn=-88, eye='happy', mouth='smile', blink=0)
    if mom is not None:
        pose.update(mom['boy'])
    h = draw_hip(ctx, 520, 1235, k, 1, BOY, pose)
    pages = min(14, dl * 0.3) if mom is None else 14
    desk_front(ctx, pages)
    if not angel and mom is None:
        hb = h['front']
        ctx.move_to(hb[0] + 10, hb[1]); ctx.line_to(hb[0] + 40, hb[1] + 60); ink(ctx, 12); ctx.stroke()
        rnd = random.Random(dl)
        for i in range(3):
            book(ctx, 300 + rnd.uniform(-80, 300), 1100 - rnd.uniform(0, 300), rnd.uniform(-1, 1), 0.5, (1, 1, 1))
    if angel and (mom is None or mom.get('halo', True)):
        hx_, hy_ = h['head']
        ellipse(ctx, hx_ - 10, hy_ - h['R'] * 1.45, h['R'] * 0.6, h['R'] * 0.15); setc(ctx, hx('ffe14d')); ctx.set_line_width(14); ctx.stroke_preserve()
        setc(ctx, INK); ctx.set_line_width(3); ctx.stroke()
    if mom is not None:
        mom['draw'](ctx, h)
    ctx.restore()
    if angel and mom is None:
        rnd = random.Random(3)
        for i in range(6):
            t = ((dl + i * 7) % 24) / 24
            sparkle(ctx, rnd.uniform(140, 940), rnd.uniform(620, 1300), 38 * math.sin(t * math.pi))
        label(ctx, "SO OBEDIENT", 540, 1600, 90, hx('ffe14d'), -0.04, pop(dl, 52, 58))
    if not angel and mom is None:
        label(ctx, "SCRIBBLE x1000", 540, 1600, 80, hx('8fe9ff'), 0.04, 1)


def s9_ending(ctx, f):
    lf = f - 900
    k = KM

    def draw_mom(ctx, h):
        if lf < 34:
            u = pop(lf, 0, 34)
            mx = lerp(1300, 820, eout(u)); pose = run_pose(lf * 0.5, torso=0, eye='normal', mouth='smile')
            pose['lhip'] *= 0.6; pose['rhip'] *= 0.6; pose['lsh'] *= 0.5; pose['rsh'] *= 0.5
            draw(ctx, mx, STAND - 186 * k, k, -1, MOM, pose)
        elif lf < 62:
            pat = abs(math.sin((lf - 34) * 0.45))
            draw(ctx, 820, STAND - 186 * k, k, -1, MOM, P(lsh=30, lel=-110, rsh=120 + 18 * pat, rel=-30, lhip=8, rhip=-8, eye='happy', mouth='smile'))
        elif lf < 88:
            u = pop(lf, 62, 88)
            pose = run_pose(lf * 0.5, eye='normal', mouth='smile'); pose['lhip'] *= 0.6; pose['rhip'] *= 0.6; pose['lsh'] *= 0.5; pose['rsh'] *= 0.5
            draw(ctx, lerp(820, 930, u), STAND - 186 * k, k, 1, MOM, pose)
        else:
            gl = lf >= 96
            draw(ctx, 930, STAND - 186 * k, k, -1 if gl else 1, MOM, P(lsh=40, lel=-135, rsh=35, rel=-138, head=-6 if gl else 0, eye='glare' if gl else 'normal', mouth='frown' if gl else 'smile'))

    if lf < 34:
        bp = dict(eye='happy', mouth='smile')
    elif lf < 62:
        pat = abs(math.sin((lf - 34) * 0.45))
        bp = dict(eye='closed', mouth='wavy', sq=0.2 * pat, sway=0.6 * pat)
    elif lf < 96:
        relax = ease(pop(lf, 68, 82))
        bp = dict(torso=-10 * relax, rsh=lerp(34, -160, relax), rel=lerp(-108, -60, relax), eye='closed' if relax > 0.5 else 'normal', mouth='open' if relax > 0.5 else 'smile')
    else:
        bp = dict(eye='shock', mouth='flat', torso=4, sq=-0.08 * math.exp(-(lf - 96) / 5))
    desk_scene(ctx, f, 60, mom=dict(boy=bp, draw=draw_mom, halo=lf < 62 or lf >= 100))
    if 34 <= lf < 62 and (lf - 34) % 14 < 6:
        label(ctx, "PAT PAT", 760, 760, 80, hx('ffb3d1'), 0.08, 1)
    if 76 <= lf < 96:
        label(ctx, "PHEW...", 380, 820, 90, hx('8fe9ff'), -0.06, pop(lf, 76, 80))
    if 96 <= lf < 118:
        label(ctx, "!!", 420, 780, 150, hx('ff3b5c'), 0.1, pop(lf, 96, 99))
    card(ctx, 'p4', f, 940)


SHOTS = [(0, s1_hook), (90, s2_homework), (200, s3_gaming), (330, s4_dance), (450, s5_freeze), (510, s6_mom), (600, s7_panic), (690, s8_cleanup), (900, s9_ending)]


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.3)
    ctx.set_source(g); ctx.paint()
    for c in (90, 200, 330, 510, 600, 690, 802, 900):
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.6 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/x{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/mom_audio34.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
