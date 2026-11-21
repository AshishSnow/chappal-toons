"""'Tangled Lights' - untangling the holiday lights. Original, general-audience comedy short, 22s.
Hook: Dad's red strained ECU wrestling a giant knot of holiday lights, caption "EVERY YEAR:" / "THE HOLIDAY LIGHTS" + "ALMOST... GOT IT...!"
Beat 1: the box says "PACKED NEATLY!" -> lid pops, a giant knot springs out *BOING!* "...HOW?!"
        Dad yanks one end -> the knot wraps around him -> light-ball cocoon "...it's FINE."
Beat 2: kid tugs the plug end -> Dad spins like a top, the string comes out perfectly straight *DING* "Like THIS?"
        dizzy Dad: "...BEGINNER'S LUCK."
        night: *CLICK* the house lights up "TA-DAAA!"
Twist:  calendar flips to JANUARY, Mom "Time to take them DOWN!" -> Dad coils them NEATLY, tapes the box *RIIIP*
        "MEANWHILE, IN THE BOX..." the plug opens its eyes and knots the string up by itself, giggling.
End:    loop back to Dad's strain ECU."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import sweat, twitch, arm_to
from scenes8 import sit
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


DAD = dict(doodle.DAD, shirt=hx('e8333f'), pants=hx('2a3a6a'))
REDDAD = dict(DAD, skin=hx('ff9a86'))
MOM = dict(doodle.MOM_G, shirt=hx('22b45a'), pants=hx('3d5a9e'))
BOY = dict(doodle.BOY, hood=False, shades=False, shirt=hx('1f8bff'), pants=hx('2a3a6a'))
N = 660
RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
WIRE = hx('1f6b3a')
BULBS = [RED, GOLD, BLUE, GREEN, PINK, ORANGE]
FLOOR = 1460
DK = 1.4
KK = 1.0

CAPS = {'p1': [[("EVERY YEAR:", OUT)], [("THE HOLIDAY LIGHTS", RED)]],
        'p2': [[("MEANWHILE,", OUT)], [("IN THE BOX...", PURPLE)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def bz(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    u = 1 - t
    return (u ** 3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t ** 3 * x3,
            u ** 3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t ** 3 * y3)


def bulb(ctx, x, y, a, col, lit=True, s=1.0, tw=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if lit:
        g = cairo.RadialGradient(0, 30, 4, 0, 30, 80)
        g.add_color_stop_rgba(0, col[0], col[1], col[2], 0.55 * tw); g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
        ctx.set_source(g); ctx.arc(0, 30, 80, 0, 2 * math.pi); ctx.fill()
    rect_r(ctx, -11, -4, 22, 20, 5); fl(ctx, WIRE, 4)
    ctx.move_to(0, 14); ctx.curve_to(24, 22, 20, 52, 0, 62); ctx.curve_to(-20, 52, -24, 22, 0, 14); ctx.close_path()
    c = light(col, 0.35 * tw) if lit else dark(col, 0.75)
    fl(ctx, c, 4)
    ellipse(ctx, -6, 32, 4, 9); setc(ctx, (1, 1, 1, 0.75 if lit else 0.35)); ctx.fill()
    ctx.restore()


def _knot(seed, n=22):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        pts = []
        for j in range(4):
            a = rnd.uniform(0, 2 * math.pi); r = math.sqrt(rnd.uniform(0.05, 1)) * 0.95
            pts.append((math.cos(a) * r, math.sin(a) * r))
        out.append((pts, rnd.uniform(0, 6.28), rnd.randrange(6)))
    return out


KNOTS = {s: _knot(s) for s in (1, 2, 3, 4)}


def knot_ball(ctx, x, y, r, lf, seed=1, lit=True, wob=1.0, a=0.0):
    if r <= 2:
        return
    K = KNOTS[seed]
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ellipse(ctx, 0, 0, r * 0.82, r * 0.82); setc(ctx, (0.08, 0.25, 0.14, 0.55)); ctx.fill()
    lw = max(3, r * 0.03)
    curves = []
    for i, (pts, ph, ci) in enumerate(K):
        pp = [(px * r + wob * r * 0.04 * math.sin(lf * 0.25 + ph + j), py * r + wob * r * 0.04 * math.cos(lf * 0.21 + ph + 2 * j)) for j, (px, py) in enumerate(pts)]
        curves.append((pp, ph, ci))
    for pp, ph, ci in curves:
        ctx.move_to(*pp[0]); ctx.curve_to(*pp[1], *pp[2], *pp[3]); ink(ctx, lw * 2.4); ctx.stroke()
        ctx.move_to(*pp[0]); ctx.curve_to(*pp[1], *pp[2], *pp[3]); setc(ctx, WIRE); ctx.set_line_width(lw); ctx.stroke()
    for i, (pp, ph, ci) in enumerate(curves):
        for k, t in enumerate((0.25, 0.7)):
            bx, by = bz(pp, t)
            tw = 0.6 + 0.4 * math.sin(lf * 0.5 + ph * 3 + k * 2)
            bulb(ctx, bx, by, ph + k * 2.1, BULBS[(ci + k) % 6], lit, r / 420, tw)
    ctx.restore()


def strand(ctx, pts, lf, lit=True, spacing=90, s=0.9, hang=True, a0=0.0, flick=1):
    """polyline wire with bulbs every `spacing` px"""
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ink(ctx, 16); ctx.stroke()
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    setc(ctx, WIRE); ctx.set_line_width(7); ctx.stroke()
    acc = spacing * 0.5; k = 0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d = math.hypot(x1 - x0, y1 - y0)
        while acc <= d and d > 0:
            t = acc / d
            bx, by = lerp(x0, x1, t), lerp(y0, y1, t)
            ang = (0 if hang else math.atan2(y1 - y0, x1 - x0) + math.pi / 2) + (0.35 if k % 2 else -0.35) + a0
            tw = 0.6 + 0.4 * math.sin(lf * 0.6 * flick + k * 1.7)
            bulb(ctx, bx, by - 6, ang, BULBS[k % 6], lit, s, tw)
            acc += spacing; k += 1
        acc -= d


def plug(ctx, x, y, a, s=1.0, eyes=0.0, lf=0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    for px in (-14, 14):
        rect_r(ctx, px - 5, -78, 10, 36, 3); fl(ctx, hx('d8d8e0'), 4)
    rect_r(ctx, -36, -46, 72, 70, 14); fl(ctx, hx('f4efe2'), 6)
    if eyes > 0:
        for ex in (-14, 14):
            ellipse(ctx, ex, -14, 11, 13 * eyes); fl(ctx, WHITE, 4)
            ellipse(ctx, ex + 3, -12, 5, 6 * eyes); setc(ctx, INK); ctx.fill()
        ctx.move_to(-14, 6); ctx.curve_to(-6, 16, 6, 16, 14, 6); ink(ctx, 4); ctx.stroke()
    ctx.restore()


def box(ctx, x, yb, w, h, flap=0.0, lab="LIGHTS", note=True):
    """cardboard box, bottom-centre (x, yb). flap 0=closed, 1=open"""
    for sx in (-1, 1):
        a = sx * (1.9 * flap)
        ctx.save(); ctx.translate(x + sx * w / 2, yb - h); ctx.rotate(a)
        if flap > 0:
            poly(ctx, [(0, 0), (-sx * w / 2, 0), (-sx * w / 2 + sx * 10, -h * 0.3), (sx * -10, -h * 0.3)])
            fl(ctx, hx('d9a05a'), 7)
        ctx.restore()
    ctx.rectangle(x - w / 2, yb - h, w, h); fl(ctx, hx('e8b46a'), 8)
    if flap == 0:
        ctx.move_to(x, yb - h); ctx.line_to(x, yb - h + 40); ink(ctx, 6); ctx.stroke()
    text(ctx, lab, x, yb - h * 0.52, h * 0.22, RED, ow=8, shadow=False)
    if note:
        ctx.save(); ctx.translate(x + w * 0.22, yb - h * 0.2); ctx.rotate(-0.08)
        ctx.rectangle(-w * 0.2, -h * 0.13, w * 0.4, h * 0.26); fl(ctx, YEL, 5)
        text(ctx, "NEATLY!", 0, 0, h * 0.085, OUT, ow=0, shadow=False)
        ctx.restore()


def room_bg(ctx, wall=hx('ffd9a8')):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, wall); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 130, -3000, 50, 6000); setc(ctx, dark(wall, 0.95)); ctx.fill()
    rect_r(ctx, 660, 520, 300, 360, 12); fl(ctx, hx('2a3a7a'), 9)
    for k in range(9):
        ellipse(ctx, 690 + (k * 71) % 260, 560 + (k * 113) % 300, 7, 7); setc(ctx, WHITE); ctx.fill()
    ctx.move_to(810, 520); ctx.line_to(810, 880); ctx.move_to(660, 700); ctx.line_to(960, 700); ink(ctx, 8); ctx.stroke()
    ctx.rectangle(-3000, FLOOR, 7000, 3000); setc(ctx, hx('b86a3c')); ctx.fill()
    for k in range(-20, 30):
        ctx.move_to(k * 160, FLOOR); ctx.line_to(k * 160 - 200, FLOOR + 600)
    setc(ctx, hx('a35a30')); ctx.set_line_width(5); ctx.stroke()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 7); ctx.stroke()


def snow(ctx, lf, n=40, a=0.9):
    rnd = random.Random(5)
    for i in range(n):
        x0 = rnd.uniform(-100, 1180); sp = rnd.uniform(2, 5); ph = rnd.uniform(0, 2000)
        y = (ph + lf * sp) % 2100 - 100
        x = x0 + 20 * math.sin(lf * 0.05 + i)
        ellipse(ctx, x, y, 7, 7); setc(ctx, (1, 1, 1, a)); ctx.fill()


# ------------------------------------------------------------------ hook
def hook_face(ctx, f, lf):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eio(pop(lf, 0, 54)), 0, 5, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('3a2a8a')); ctx.fill()
    rays(ctx, 540, 860, 260, 1500, lf * 0.03, col=(1, 0.85, 0.4), a=0.25, n=18)
    snow(ctx, lf, 30, 0.6)
    cx, cy, R = 540, 820, 260
    jit = 5 * math.sin(lf * 2.3)
    face(ctx, REDDAD, P(eye='glare', mouth='grin'), cx, cy + jit * 0.5, R, 0.03 * math.sin(lf * 1.3))
    # a strand caught across his face
    strand(ctx, [(cx - 420, cy - 200), (cx - 150, cy + 60 + jit), (cx + 150, cy - 10 + jit), (cx + 420, cy + 230)], lf, True, 120, 0.8)
    knot_ball(ctx, 540, 1260 + jit, 330, lf, 1, True, 1.0, 0.02 * math.sin(lf))
    for side in (-1, 1):
        arm_to(ctx, cx + side * 0.55 * R, cy + 0.95 * R, cx + side * 300, 1200 + jit, DAD['shirt'], REDDAD['skin'], bend=side * 60, w=110)
    twitch(ctx, cx + 0.62 * R, cy - 0.78 * R, lf, 1.3)
    twitch(ctx, cx - 0.62 * R, cy - 0.78 * R, lf + 5, 1.0)
    sweat(ctx, cx - 1.0 * R, cy - 40, lf, 1.3)
    sweat(ctx, cx + 1.02 * R, cy - 10, lf + 9, 1.1)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook_face(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"ALMOST... GOT IT...!\"", 540, 1450, 110, WHITE, -0.03, t)


# ------------------------------------------------------------------ beat 1
def box_pop(ctx, f, il):
    # il 0..66
    popped = il >= 24
    z = 1.0 + (0.12 * eout(pop(il, 24, 34)) if popped else 0)
    ctx.save(); cam(ctx, 480, 1120, z + 0.2, 0, shake_at(il, [24], 10, 20), f)
    room_bg(ctx)
    flap = eout(pop(il, 22, 26))
    if popped:
        t = eout(pop(il, 24, 34))
        r = lerp(60, 270, t) * (1 + 0.08 * math.sin(math.pi * pop(il, 30, 40)))
        knot_ball(ctx, 700, lerp(1280, 990, t), r, il, 2, False, 1.0, il * 0.02)
    box(ctx, 700, FLOOR, 380, 260, flap)
    if not popped:
        p = P(eye='happy', mouth='grin', rsh=-150, rel=-30, lsh=10)
    else:
        p = P(eye='shock', mouth='scream', lsh=150, lel=20, rsh=-150, rel=-20)
    draw(ctx, 270, FLOOR - 186 * DK, DK, 1, DAD, p)
    ctx.restore()
    if not popped:
        label2(ctx, "\"Packed them NEATLY", "last year!\"", WHITE, pop(il, 2, 6), 90, col2=YEL, y=1440)
    else:
        label(ctx, "*BOING!*", 540, 440, 120, YEL, -0.04, pop(il, 24, 27))
        label(ctx, "\"...HOW?!\"", 540, 1450, 140, WHITE, 0.03, pop(il, 36, 39))


def yank(ctx, f, il):
    # il 0..80: yank -> spin -> cocoon
    if il < 22:
        ctx.save(); cam(ctx, 510, 1130, 1.2, 0, 4, f)
        room_bg(ctx)
        knot_ball(ctx, 770, 1210, 230, il, 2, False, 1.6)
        b = draw(ctx, 290, FLOOR - 186 * DK, DK, 1, DAD, P(eye='glare', mouth='grin', torso=-14, lsh=95, lel=-10, rsh=80, rel=-10))
        strand(ctx, [(430, 1180), (640, 1190), (720, 1200)], il, False, 80, 0.7, hang=True)
        ctx.restore()
        label(ctx, "*YANK!*", 540, 440, 120, WHITE, -0.04, pop(il, 4, 7))
        label(ctx, "\"HNNNNGH!!\"", 540, 1450, 120, RED, 0.03, pop(il, 2, 5))
        return
    jl = il - 22
    spin = jl < 22
    rot = 0 if not spin else 360 * eio(jl / 22)
    ctx.save(); cam(ctx, 540, 1100, 1.3 if spin else 1.3 + 0.08 * eout(pop(jl, 22, 50)), rot, 6 if spin else 0, f)
    room_bg(ctx)
    d = 1 if (not spin or (jl // 2) % 2 == 0) else -1
    b = draw(ctx, 540, FLOOR - 186 * DK, DK, d, DAD, P(eye='shock' if spin else 'normal', mouth='wavy' if spin else 'flat', lsh=-8, rsh=8))
    hx0, hy0 = b['head']
    rb = 230 if not spin else lerp(120, 230, jl / 22)
    knot_ball(ctx, 540, hy0 + b['R'] + rb * 0.85, rb, jl, 3, not spin, 0.6)
    if spin:
        for k in range(3):
            ctx.new_path(); ctx.arc(540, 1100, 330 + k * 60, k + jl * 0.5, k + jl * 0.5 + 2.2); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(12); ctx.stroke()
    else:
        bulb(ctx, hx0 + 4, hy0 + 0.1 * b['R'], 3.14, RED, True, 0.6)
    ctx.restore()
    if spin:
        label(ctx, "*WHIRRR!*", 540, 440, 110, YEL, 0.04, pop(jl, 0, 3))
    else:
        label(ctx, "\"...it's FINE.\"", 540, 1450, 130, WHITE, -0.03, pop(jl, 26, 29))


def s2(ctx, f):
    lf = f - 54
    if lf < 66:
        box_pop(ctx, f, lf)
    else:
        yank(ctx, f, lf - 66)


# ------------------------------------------------------------------ beat 2
def kid_tug(ctx, f, il):
    # il 0..140
    ctx.save()
    spin = 46 <= il < 96
    dizzy = il >= 96
    cam(ctx, 600, 1130 if not dizzy else 1160, 1.1, 0, shake_at(il, [46], 8, 16) + (4 if spin else 0), f)
    room_bg(ctx)
    kx = lerp(1250, 830, eout(pop(il, 0, 22))) if il < 46 else lerp(830, 900, eout(pop(il, 46, 70)))
    dx = 340
    if not spin and not dizzy:
        b = draw(ctx, dx, FLOOR - 186 * DK, DK, 1, DAD, P(eye='normal', mouth='flat', lsh=-8, rsh=8))
        hx0, hy0 = b['head']
        knot_ball(ctx, dx, hy0 + b['R'] + 195, 230, il, 3, False, 0.6)
        # the plug end lying on the floor between them
        plug(ctx, lerp(560, kx - 60, eout(pop(il, 26, 38))), lerp(FLOOR - 30, FLOOR - 230, eout(pop(il, 26, 38))), 0.4 if il < 26 else -1.6, 1.0)
        ctx.move_to(dx + 150, FLOOR - 40); ctx.curve_to(400, FLOOR - 10, 500, FLOOR - 20, lerp(560, kx - 60, eout(pop(il, 26, 38))), lerp(FLOOR - 30, FLOOR - 230, eout(pop(il, 26, 38))) + 20)
        ink(ctx, 14); ctx.stroke()
        kp = P(eye='happy', mouth='smile', lsh=60, lel=-20) if il >= 26 else run_pose(il * 0.8, eye='happy', mouth='smile', torso=6)
        draw(ctx, kx, FLOOR - 186 * KK, KK, -1, BOY, kp)
    elif spin:
        jl = il - 46
        d = 1 if (jl // 2) % 2 == 0 else -1
        b = draw(ctx, dx, FLOOR - 186 * DK, DK, d, DAD, P(eye='shock', mouth='scream', lsh=120, rsh=-120))
        hx0, hy0 = b['head']
        rb = 230 * (1 - eio(jl / 40))
        knot_ball(ctx, dx, hy0 + b['R'] + 195, rb, jl, 3, False, 0.6, jl * 0.6)
        for k in range(3):
            ctx.new_path(); ctx.arc(dx, 1150, 220 + k * 50, jl * 0.6 + k, jl * 0.6 + k + 2.4); setc(ctx, (1, 1, 1, 0.85)); ctx.set_line_width(10); ctx.stroke()
        strand(ctx, [(dx + 60, 1200), (kx - 70, 1200)], jl, False, 85, 0.7)
        plug(ctx, kx - 60, 1200, -1.57, 0.9)
        draw(ctx, kx, FLOOR - 186 * KK, KK, -1, BOY, P(eye='happy', mouth='open', lsh=80, lel=0, torso=-10))
    else:
        jl = il - 96
        p = sit(eye='closed', mouth='wavy', lsh=-30, rsh=30)
        b = draw_hip(ctx, dx, FLOOR - 40, DK, 1, DAD, p)
        hx0, hy0 = b['head']
        stars_ko(ctx, hx0, hy0 - b['R'] * 1.2, jl * 0.1, 4, 110)
        strand(ctx, [(dx + 120, FLOOR - 20), (kx - 70, FLOOR - 20)], jl, False, 85, 0.7)
        draw(ctx, kx, FLOOR - 186 * KK, KK, -1, BOY, P(eye='happy', mouth='grin', lsh=150, lel=20, rsh=-150, rel=-20))
        for k in range(4):
            sparkle(ctx, 450 + k * 120, FLOOR - 120 - (k % 2) * 60, 22 + 6 * math.sin(jl * 0.5 + k), YEL)
    ctx.restore()
    if il < 46:
        label(ctx, "\"Like THIS?\"", 540, 1450, 120, WHITE, -0.03, pop(il, 28, 31))
        label(ctx, "*tug*", 540, 440, 100, YEL, 0.04, pop(il, 40, 43))
    elif spin:
        label(ctx, "*FWIIIIIP!!*", 540, 440, 120, YEL, -0.04, pop(il, 46, 49))
        if il >= 86:
            label(ctx, "*DING!*", 540, 1450, 120, GREEN, 0.03, pop(il, 86, 89))
    else:
        label(ctx, "\"...BEGINNER'S LUCK.\"", 540, 1450, 110, WHITE, 0.03, pop(il, 100, 103))


def house_shot(ctx, f, il):
    # il 0..70
    on = il >= 26
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(il, 26, 50)), 0, shake_at(il, [26], 6, 10), f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('1a1f4a')); ctx.fill()
    ellipse(ctx, 860, 420, 60, 60); setc(ctx, hx('fff2b0')); ctx.fill()
    snow(ctx, il + 300, 40)
    # house
    if on:
        g = cairo.RadialGradient(540, 1000, 100, 540, 1000, 800)
        g.add_color_stop_rgba(0, 1, 0.9, 0.5, 0.35); g.add_color_stop_rgba(1, 1, 0.9, 0.5, 0)
        ctx.set_source(g); ctx.paint()
    ctx.rectangle(200, 900, 680, 480); fl(ctx, hx('5a6bb8') if not on else hx('7a8ad8'), 9)
    poly(ctx, [(140, 920), (540, 620), (940, 920)]); fl(ctx, hx('8a3a4a'), 9)
    rect_r(ctx, 480, 1120, 120, 260, 10); fl(ctx, hx('8a5a2a'), 8)
    for wx in (300, 680):
        rect_r(ctx, wx, 1020, 120, 120, 8); fl(ctx, hx('ffe08a') if on else hx('2a3a6a'), 8)
    # lights along the roof
    pts = []
    for k in range(13):
        t = k / 12
        x = lerp(140, 940, t); y = (lerp(920, 620, t * 2) if t <= 0.5 else lerp(620, 920, (t - 0.5) * 2))
        pts.append((x, y + 30 * abs(math.sin(math.pi * t * 6))))
    strand(ctx, pts, il, on, 70, 0.75)
    strand(ctx, [(200, 1380), (300, 1400), (400, 1380), (520, 1400)], il, on, 70, 0.65)
    ctx.rectangle(-500, 1380, 2200, 900); setc(ctx, (0.95, 0.97, 1)); ctx.fill()
    ctx.move_to(-500, 1380); ctx.line_to(1700, 1380); ink(ctx, 7); ctx.stroke()
    draw(ctx, 820, 1380 - 186 * 1.0, 1.0, -1, DAD, P(eye='happy' if on else 'normal', mouth='grin' if on else 'smile', lsh=150 if on else 40, rsh=-150 if on else 60))
    if on:
        for k in range(6):
            sparkle(ctx, 200 + k * 140, 560 + (k % 2) * 80, 24 + 8 * math.sin(il * 0.5 + k), YEL)
    ctx.restore()
    if not on:
        label(ctx, "*CLICK*", 540, 440, 110, WHITE, 0.03, pop(il, 20, 23))
    else:
        label(ctx, "\"TA-DAAA!\"", 540, 1450, 140, YEL, -0.03, pop(il, 28, 31))


# ------------------------------------------------------------------ twist
def calendar(ctx, f, il):
    # il 0..30
    ctx.save(); cam(ctx, 540, 960, 1.0, 0, shake_at(il, [20], 8, 18), f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd9a8')); ctx.fill()
    rays(ctx, 540, 940, 300, 1500, il * 0.03, col=(1, 1, 1), a=0.3, n=16)
    rect_r(ctx, 220, 560, 640, 760, 30); fl(ctx, WHITE, 10)
    jan = il >= 20
    rect_r(ctx, 220, 560, 640, 190, 30); fl(ctx, hx('3a8bd8') if jan else RED, 10)
    text(ctx, "JANUARY" if jan else "DECEMBER", 540, 660, 92, WHITE, ow=10, shadow=False)
    text(ctx, "2" if jan else "24", 540, 1060, 300, OUT if jan else RED, ow=0, shadow=False)
    if not jan:
        # pages tearing off
        for k in range(4):
            st = 2 + k * 4
            t = clamp((il - st) / 10)
            if t <= 0:
                continue
            ctx.save(); ctx.translate(540 + 700 * t * (1 if k % 2 else -1), 940 - 600 * t + 900 * t * t); ctx.rotate(t * 3 * (1 if k % 2 else -1))
            rect_r(ctx, -300, -360, 600, 720, 30); fl(ctx, WHITE, 8)
            ctx.restore()
    ctx.restore()
    if jan:
        label(ctx, "*THUMP*", 540, 1450, 110, WHITE, -0.03, pop(il, 20, 23))


def mom_down(ctx, f, il):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eout(pop(il, 0, 30)), 0, 3, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('22b45a')); ctx.fill()
    rays(ctx, 540, 900, 260, 1500, il * 0.02, col=(0.9, 1, 0.8), a=0.25, n=16)
    face(ctx, MOM, P(eye='happy', mouth='grin'), 540, 860, 290, 0.05)
    box(ctx, 540, 1900, 820, 560, 0.0, note=False)
    ctx.restore()
    label2(ctx, "\"Okay! Time to take", "them DOWN!\"", WHITE, pop(il, 2, 6), 96, col2=YEL, y=1420)


def dad_twitch(ctx, f, il):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.12 * eout(pop(il, 0, 20)), 0, 3, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('5a3aa8')); ctx.fill()
    rays(ctx, 540, 900, 260, 1500, il * 0.02, col=(0.8, 0.6, 1), a=0.25, n=16)
    face(ctx, DAD, P(eye='shock', mouth='flat'), 540, 880, 300, 0)
    twitch(ctx, 540 + 0.62 * 300, 880 - 0.78 * 300, il, 1.5)
    sweat(ctx, 540 - 330, 840, il, 1.3)
    knot_ball(ctx, 540, 1560, 420, il, 1, False, 0.5)
    ctx.restore()
    label(ctx, "*twitch*", 540, 1450, 110, WHITE, 0.04, pop(il, 3, 6))


def s4(ctx, f):
    lf = f - 340
    if lf < 60:
        house_shot(ctx, f, lf)
    elif lf < 88:
        calendar(ctx, f, lf - 60)
    elif lf < 122:
        mom_down(ctx, f, lf - 88)
    else:
        dad_twitch(ctx, f, lf - 122)


# ------------------------------------------------------------------ end
def spiral_pts(cx, cy, r0, r1, turns, frac):
    pts = []
    n = int(220 * frac) + 2
    for i in range(n):
        t = i / 219
        a = t * turns * 2 * math.pi
        r = lerp(r1, r0, t)
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r * 0.92))
    return pts


def coil_shot(ctx, f, il):
    # il 0..62: top-down box, Dad coils the lights neatly, tapes it shut
    ctx.save(); cam(ctx, 540, 960, 1.0, 0, shake_at(il, [48], 6, 10), f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('b86a3c')); ctx.fill()
    for k in range(-5, 14):
        ctx.move_to(k * 160, -200); ctx.line_to(k * 160 + 300, 2200)
    setc(ctx, hx('a35a30')); ctx.set_line_width(5); ctx.stroke()
    shut = eout(pop(il, 40, 48))
    rect_r(ctx, 160, 560, 760, 760, 14); fl(ctx, hx('e8b46a'), 9)
    ctx.rectangle(200, 600, 680, 680); fl(ctx, hx('8a5a30'), 7)
    frac = eio(pop(il, 0, 38))
    pts = spiral_pts(540, 940, 40, 300, 6, frac)
    if len(pts) > 2:
        strand(ctx, pts, il, False, 80, 0.55, hang=False)
    if frac < 1:
        ex, ey = pts[-1]
        arm_to(ctx, 1250, 1500, ex, ey, DAD['shirt'], DAD['skin'], bend=60, w=110)
    else:
        plug(ctx, 540 + 40, 940, 0.3, 0.8)
    if shut > 0:
        for sx in (-1, 1):
            ctx.save(); ctx.translate(540 + sx * 380, 940)
            ctx.scale(shut, 1)
            ctx.rectangle(0 if sx < 0 else -380, -380, 380, 760); fl(ctx, hx('d9a05a'), 8)
            ctx.restore()
        if il >= 48:
            t = eout(pop(il, 48, 54))
            ctx.rectangle(500, 560, 80, 760 * t); setc(ctx, (0.85, 0.85, 0.7, 0.85)); ctx.fill()
            text(ctx, "LIGHTS", 540, 760, 70, RED, ow=8, shadow=False, ang=0)
    ctx.restore()
    if il < 40:
        label2(ctx, "\"NEATLY.", "THIS. TIME.\"", WHITE, pop(il, 2, 6), 110, col2=GREEN, y=1420)
    elif il >= 48:
        label(ctx, "*RIIIIP!*", 540, 1450, 120, YEL, 0.03, pop(il, 48, 51))


def inbox_shot(ctx, f, il):
    # il 0..70: inside the dark box, the plug wakes up and knots the string by itself
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.1 * eio(pop(il, 0, 70)), 0, 2 if il > 40 else 0, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('140e24')); ctx.fill()
    for k in range(-3, 12):
        ctx.move_to(-200, 500 + k * 120); ctx.line_to(1300, 520 + k * 120)
    setc(ctx, (1, 1, 1, 0.04)); ctx.set_line_width(30); ctx.stroke()
    m = eio(pop(il, 18, 60))
    if m < 1:
        ctx.save(); ctx.translate(540, 1080); ctx.scale(1, 0.45); ctx.translate(-540, -1080)
        strand(ctx, spiral_pts(540, 1080, 40, 300, 6, 1.0), il, False, 80, 0.55, hang=False)
        ctx.restore()
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, (0.08, 0.05, 0.14, m)); ctx.fill()
    knot_ball(ctx, 540, 1060, 290 * m, il, 4, False, 1.5, il * 0.08)
    # the plug weaves around like a snake
    eyes = eout(pop(il, 4, 10))
    a = il * 0.32
    px = 540 + 300 * math.sin(a) * (0.4 + 0.6 * eio(pop(il, 12, 24)))
    py = 820 + 100 * math.sin(2 * a)
    ctx.move_to(540, 1060); ctx.curve_to(540, 950, px, py + 160, px, py + 40); ink(ctx, 18); ctx.stroke()
    ctx.move_to(540, 1060); ctx.curve_to(540, 950, px, py + 160, px, py + 40); setc(ctx, WIRE); ctx.set_line_width(8); ctx.stroke()
    plug(ctx, px, py, 0.4 * math.cos(a), 1.6, eyes, il)
    ctx.restore()
    if il >= 10:
        label(ctx, "*hee hee hee*", 540, 1450, 110, PINK, 0.04 * math.sin(il * 0.3), pop(il, 10, 13))


def s5(ctx, f):
    lf = f - 480
    if lf < 62:
        coil_shot(ctx, f, lf)
    elif lf < 132:
        inbox_shot(ctx, f, lf - 62)
        card(ctx, 'p2', lf - 62, 0)
    else:
        s1(ctx, f, f - 612)


def s3_(ctx, f):
    lf = f - 200
    kid_tug(ctx, f, lf)


SHOTS = [(0, s1), (54, s2), (200, s3_), (340, s4), (480, s5)]
CUTS = (54, 120, 142, 200, 340, 400, 428, 462, 480, 542, 612)


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
                              "-i", "out/tangled_lights_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
