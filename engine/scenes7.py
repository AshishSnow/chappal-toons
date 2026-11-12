"""'Study Plan vs Reality' - original characters, doodle style, ~35s loopable."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import cam, pop, sparkle, puff, label, book, phone, note, shake_at

BOY = doodle.BOY
N = 1050
FLOOR = 1250
SEAT = 1235
KB = 1.55
WIN = (600, 500, 270, 330)


def blink(f):
    return 1 if f % 83 < 4 else 0


CAPS = {
    'p1': [[("ME: TODAY I'LL STUDY", OUT)], [("FOR ", OUT), ("5 HOURS", hx('1f8bff'))]],
    'p2': [[("AFTER ", OUT), ("5 MINUTES", hx('ff3b5c')), (":", OUT)], [("SETTING BIG GOALS", OUT)]],
    'p3': [[("AFTER ", OUT), ("15 MINUTES", hx('ff3b5c')), (":", OUT)], [("JUST A SMALL BREAK", OUT)]],
    'p4': [[("11:58 PM", hx('7a3cff'))], [("OKAY... ", OUT), ("TOMORROW", hx('ff3b5c'))]],
    'p5': [[("THE NEXT DAY:", OUT)], [("SAME PLAN AGAIN", hx('1fa84f'))]],
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


# ------------------------------------------------------------------ time of day
def sky_col(tod):
    """tod 0 = day, 1 = sunset, 2 = night, 3 = morning"""
    keys = [(0, hx('6bd0ff')), (1, hx('ff9a5a')), (2, hx('1b2050')), (3, hx('ffd9a0'))]
    for (a, c0), (b, c1) in zip(keys, keys[1:]):
        if tod <= b:
            u = (tod - a) / (b - a)
            return tuple(lerp(x, y, u) for x, y in zip(c0, c1))
    return keys[-1][1]


def clock(ctx, x, y, r, minutes, wl=8):
    ellipse(ctx, x, y, r, r); fl(ctx, (1, 1, 1), wl)
    ink(ctx, wl * 0.6)
    for i in range(12):
        a = i * math.pi / 6
        ctx.move_to(x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8); ctx.line_to(x + math.cos(a) * r * 0.9, y + math.sin(a) * r * 0.9)
    ctx.stroke()
    ha = (minutes / 720) * 2 * math.pi - math.pi / 2; ma = (minutes / 60) * 2 * math.pi - math.pi / 2
    ink(ctx, wl * 1.1); ctx.move_to(x, y); ctx.line_to(x + math.cos(ha) * r * 0.5, y + math.sin(ha) * r * 0.5); ctx.stroke()
    ink(ctx, wl * 0.8); ctx.move_to(x, y); ctx.line_to(x + math.cos(ma) * r * 0.78, y + math.sin(ma) * r * 0.78); ctx.stroke()
    ellipse(ctx, x, y, wl, wl); setc(ctx, hx('ff3b5c')); ctx.fill()


def timetable(ctx, prog):
    x0, y0, w, h = 90, 600, 440, 330
    if prog <= 0:
        return
    ctx.save(); ctx.translate(x0 + w / 2, y0); ctx.scale(1, min(1, prog * 4)); ctx.translate(-x0 - w / 2, -y0)
    ctx.rectangle(x0, y0, w, h); fl(ctx, (1, 1, 1), 7)
    text(ctx, "TIMETABLE", x0 + w / 2, y0 + 40, 40, hx('ff3b5c'), ow=6, shadow=False)
    cols = [hx('ff6b6b'), hx('ffd23f'), hx('5fd07a'), hx('3fb6ff'), hx('b06bff'), hx('ff9fd0')]
    n = int(clamp((prog - 0.2) / 0.8) * 24)
    for i in range(n):
        r, c = divmod(i, 6)
        ctx.rectangle(x0 + 20 + c * 68, y0 + 80 + r * 60, 60, 50); fl(ctx, cols[(i * 7 + r) % 6], 3)
    ctx.restore()
    ellipse(ctx, x0 + 20, y0 + 14, 9, 9); fl(ctx, hx('ff3b5c'), 3)
    ellipse(ctx, x0 + w - 20, y0 + 14, 9, 9); fl(ctx, hx('ff3b5c'), 3)


NOTES = [("RANK 1", 560, 980, -0.08, hx('fff27a'), 300), ("6 AM", 700, 1080, 0.1, hx('9fe8ff'), 312), ("NO PHONE", 150, 990, 0.06, hx('ffb3d1'), 324),
         ("100%", 380, 1010, -0.05, hx('b8f5a8'), 336)]


def sticky(ctx, s, x, y, a, col, t=1.0, size=34):
    if t <= 0:
        return
    sc = eout(min(1, t * 1.6)) * (1 + 0.15 * math.sin(min(1, t * 1.6) * math.pi))
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(sc, sc)
    ctx.rectangle(-75, -55, 150, 110); fl(ctx, col, 5)
    text(ctx, s, 0, 6, size, INK, outline=INK, ow=0.5, shadow=False, maxw=128)
    ctx.restore()


def bedroom(ctx, f, tod=0.0, lamp=True, prog=0.0, notes_f=None, tomorrow=0.0, clock_min=600):
    ctx.rectangle(-900, -900, W + 2400, 2200); ctx.set_source(vgrad(ctx, 0, 0, 0, FLOOR, [(0, hx('e7f4ff')), (1, hx('d3e8fb'))])); ctx.fill()
    # window
    x, y, w, h = WIN
    ctx.rectangle(x, y, w, h); setc(ctx, sky_col(tod)); ctx.fill_preserve(); ink(ctx, 9); ctx.stroke()
    if tod < 1.4:
        sy = y + 80 + 260 * clamp(tod / 1.2)
        ellipse(ctx, x + 190, sy, 40, 40); setc(ctx, hx('fff27a') if tod < 0.6 else hx('ffb35a')); ctx.fill()
    if tod > 1.5 and tod < 2.8:
        ellipse(ctx, x + 80, y + 90, 36, 36); setc(ctx, hx('fff6d0')); ctx.fill()
        ellipse(ctx, x + 96, y + 80, 30, 30); setc(ctx, sky_col(tod)); ctx.fill()
        rnd = random.Random(1)
        for _ in range(8):
            ellipse(ctx, x + rnd.uniform(20, w - 20), y + rnd.uniform(20, h - 20), 3, 3); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()
    if tod >= 2.8:
        ellipse(ctx, x + 200, y + 260 - 100 * (tod - 2.8) * 5, 40, 40); setc(ctx, hx('ffd34f')); ctx.fill()
    ctx.move_to(x + w / 2, y); ctx.line_to(x + w / 2, y + h); ctx.move_to(x, y + h / 2); ctx.line_to(x + w, y + h / 2); ink(ctx, 7); ctx.stroke()
    ctx.rectangle(x - 20, y + h, w + 40, 24); fl(ctx, (1, 1, 1), 6)
    clock(ctx, 760 if False else 300, 470, 62, clock_min)
    # shelf + poster
    ctx.rectangle(960, 640, 300, 24); fl(ctx, hx('c98b55'), 5)
    for i, c in enumerate((hx('ff5a5a'), hx('3f8bff'), hx('5fd07a'), hx('ffd23f'))):
        ctx.rectangle(980 + i * 50, 545, 40, 95); fl(ctx, c, 4)
    timetable(ctx, prog)
    if notes_f is not None:
        for s_, nx, ny, a, c, pf in NOTES:
            sticky(ctx, s_, nx, ny, a, c, pop(notes_f, pf, pf + 10))
    if tomorrow > 0:
        sticky(ctx, "TOMORROW!", 175, 690, -0.12, hx("ff8a3d"), tomorrow, 30)
    # floor
    ctx.rectangle(-900, FLOOR, W + 2400, 1600); setc(ctx, hx('e3c9a8')); ctx.fill()
    for i in range(-10, 20):
        ctx.move_to(-900, FLOOR + 40 + i * 0); ctx.line_to(-900, FLOOR)
    for yy in (1310, 1400, 1530, 1720, 1960):
        ctx.move_to(-900, yy); ctx.line_to(W + 1500, yy)
    setc(ctx, (0.55, 0.38, 0.22, 0.5)); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-900, FLOOR); ctx.line_to(W + 1500, FLOOR); ink(ctx, 8); ctx.stroke()
    # bed (right side of the world)
    ctx.rectangle(800, 1160, 700, 70); fl(ctx, hx('7a4a2c'), 7)
    ctx.rectangle(780, 1050, 40, 380); fl(ctx, hx('8a5a34'), 7)
    ctx.rectangle(800, 1230, 700, 140); fl(ctx, hx('ffffff'), 7)
    ctx.rectangle(800, 1370, 700, 60); fl(ctx, hx('8a5a34'), 7)


def chair(ctx):
    ctx.rectangle(270, 1000, 40, 250); fl(ctx, hx('3fb6a8'), 6)
    ctx.rectangle(260, 1235, 300, 30); fl(ctx, hx('3fb6a8'), 6)


def desk(ctx, books=3, lamp_on=True, pile_open=False):
    ctx.rectangle(100, 1200, 700, 40); fl(ctx, hx('c98b55'), 7)
    ctx.rectangle(130, 1240, 640, 300); fl(ctx, hx('b97a45'), 7)
    ctx.rectangle(180, 1300, 240, 90); fl(ctx, hx('a86c3a'), 5)
    ellipse(ctx, 300, 1345, 12, 8); fl(ctx, hx('ffd23f'), 3)
    # lamp
    ctx.move_to(740, 1200); ctx.line_to(720, 1010); ctx.line_to(640, 980); ink(ctx, 11); ctx.stroke()
    poly(ctx, [(580, 950), (680, 930), (700, 1010), (600, 1030)]); fl(ctx, hx('ffd23f') if lamp_on else hx('b8a050'), 6)
    cols = [hx('ff5a5a'), hx('3f8bff'), hx('5fd07a'), hx('b06bff')]
    for i in range(books):
        ctx.rectangle(150 + (i % 2) * 8, 1160 - i * 42, 190, 40); fl(ctx, cols[i % 4], 5)
        ctx.rectangle(155 + (i % 2) * 8, 1168 - i * 42, 170, 8); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()


def lamp_glow(ctx, a):
    if a <= 0:
        return
    g = cairo.RadialGradient(640, 1080, 30, 640, 1080, 700)
    g.add_color_stop_rgba(0, 1, 0.92, 0.6, 0.45 * a); g.add_color_stop_rgba(1, 1, 0.92, 0.6, 0)
    ctx.set_source(g); ctx.paint()


def night(ctx, a, lamp=0.0):
    if a <= 0:
        return
    ctx.rectangle(-900, -900, W + 3000, 4000); setc(ctx, (0.06, 0.08, 0.25, 0.55 * a)); ctx.fill()
    lamp_glow(ctx, lamp)


def headband(ctx, h, on=1.0):
    if on <= 0:
        return
    hx_, hy_ = h['head']; R = h['R']
    ctx.save(); ctx.translate(hx_, hy_ - R * 0.62)
    ctx.rectangle(-R * 0.98, -R * 0.12, R * 1.96 * on, R * 0.24); fl(ctx, hx('ff3b5c'), 5)
    if on >= 1:
        for a in (-0.5, 0.4):
            ctx.save(); ctx.translate(-R * 0.98, 0); ctx.rotate(a + math.pi)
            ctx.rectangle(0, -R * 0.08, R * 0.4, R * 0.16); fl(ctx, hx('ff3b5c'), 4); ctx.restore()
        ellipse(ctx, 0, 0, R * 0.12, R * 0.12); fl(ctx, (1, 1, 1), 3)
        text(ctx, "5H", 0, 2, R * 0.13, hx('ff3b5c'), outline=hx('ff3b5c'), ow=0.5, shadow=False)
    ctx.restore()


def sit_pose(**kw):
    p = P(torso=8, head=6, lsh=60, lel=-50, rsh=66, rel=-56, lhip=86, lkn=-86, rhip=88, rkn=-88, eye='normal', mouth='smile')
    p.update(kw); return p


def desk_shot(ctx, f, z, cx, cy, pose, books=3, tod=0, lamp=True, prog=0, notes_f=None, tomorrow=0, clock_min=600, hb=1.0, extra=None, rot=0, shake=0):
    ctx.save(); cam(ctx, cx, cy, z, rot, shake, f)
    bedroom(ctx, f, tod, lamp, prog, notes_f, tomorrow, clock_min)
    chair(ctx)
    h = draw_hip(ctx, 420, SEAT, KB, 1, BOY, pose)
    headband(ctx, h, hb)
    desk(ctx, books, lamp)
    if extra:
        extra(ctx, h)
    night(ctx, clamp(tod - 1) if tod <= 2 else clamp(3 - tod), 1.0 if lamp else 0)
    ctx.restore()
    return h


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    z = kf(f, [(0, 3.3), (30, 3.3), (58, 1.3)], ease)
    cy = kf(f, [(0, 760), (30, 760), (58, 1020)], ease); cx = kf(f, [(0, 430), (30, 430), (58, 440)], ease)
    books = 0 if f < 64 else (1 if f < 72 else (2 if f < 80 else 3))
    knuck = 92 <= f < 112
    pose = sit_pose(eye='normal', mouth='flat' if f < 30 else 'grin', blink=blink(f), torso=0, head=0)
    if knuck:
        j = math.sin(f * 2.2) * 8
        pose.update(lsh=55 + j, lel=-110, rsh=58 - j, rel=-112, eye='smug')
    if f >= 112:
        pose.update(rsh=-160, rel=-20, eye='happy', mouth='grin')
    desk_shot(ctx, f, z, cx, cy, pose, books=books, hb=pop(f, 6, 20), shake=shake_at(f, [64, 72, 80], 6, 10))
    if f < 30:
        # determination fire glints
        for i, (x, y) in enumerate(((360, 980), (720, 980))):
            r = 70 + 10 * math.sin(f * 0.8 + i)
            sparkle(ctx, x, y, r * pop(f, 4, 10), (1, 1, 1))
        label(ctx, "STUDY MODE: ON", 540, 1480, 92, hx('ffe14d'), -0.04, pop(f, 10, 16))
    for i, fr in enumerate((64, 72, 80)):
        if fr <= f < fr + 8:
            label(ctx, "THUMP!", 300 + i * 120, 1200 - i * 60, 70, hx('ff9a5a'), -0.1 + i * 0.1, 1)
    if knuck:
        label(ctx, "CRACK CRACK", 540, 1460, 80, (1, 1, 1), 0.04, 1)
    if f >= 112:
        label(ctx, "LET'S GO!", 540, 1460, 120, hx('ffe14d'), -0.06, pop(f, 112, 117))
    card(ctx, 'p1', f, 2, 205)


def s2(ctx, f):
    lf = f - 120
    if lf < 62:
        look = ease(pop(lf, 36, 48))
        def ex(ctx, h):
            bx, by = h['front']; book(ctx, bx + 20, by - 40, -0.25, 1.4, hx('3f8bff'))
        pose = sit_pose(torso=4, head=-4 + 10 * look, lsh=70, lel=-90, rsh=72, rel=-94, eye='normal', mouth='flat', blink=blink(f))
        desk_shot(ctx, f, 1.55, 430, 960, pose, books=3, extra=ex)
        if lf < 36 and lf % 18 < 10:
            label(ctx, "HMM...", 760, 860, 70, hx('8fe9ff'), 0.05, 1)
    else:
        u = pop(lf, 62, 90)
        ctx.save(); cam(ctx, 300, 470, 3.2, 0, 0, f)
        bedroom(ctx, f, clock_min=600 + 5 * ease(u))
        ctx.restore()
        if lf % 10 < 5:
            label(ctx, "TICK", 760, 1300, 90, (1, 1, 1), 0.06, 1)
        else:
            label(ctx, "TOCK", 320, 1350, 90, (1, 1, 1), -0.06, 1)
    card(ctx, 'p1', f, 2, 205)


def s3(ctx, f):
    lf = f - 210
    prog = ease(pop(lf, 10, 90))
    ctx.save(); cam(ctx, 400, 1000, 1.0, 0, 0, f)
    bedroom(ctx, f, 0.1, True, prog, notes_f=f + 0, clock_min=605)
    chair(ctx); desk(ctx, 3)
    if lf < 100:
        dr = math.sin(lf * 1.6)
        pose = P(torso=-4, head=-10, lsh=20, lel=-40, rsh=-150 + 30 * dr, rel=-10 + 20 * dr, lhip=6, rhip=-6, eye='happy', mouth='grin', sway=0.5 * dr)
        h = draw(ctx, 560, 1560 - 186 * KB, KB, -1, BOY, pose)
        hb_ = h
        fx, fy = h['front']
        ctx.move_to(fx, fy); ctx.line_to(fx - 30, fy - 50); ink(ctx, 12); ctx.stroke()
    else:
        u = pop(lf, 100, 112)
        pose = P(torso=-6, head=-14, lsh=40, lel=-110, rsh=35, rel=-115, lhip=10, rhip=-10, eye='happy', mouth='grin', sq=0.1 * math.sin(lf * 0.5))
        h = draw(ctx, lerp(560, 740, ease(u)), 1560 - 186 * KB, KB, -1, BOY, pose)
    headband(ctx, h, 1)
    ctx.restore()
    if lf < 100:
        hlines(ctx, lf, 0.18, col=INK, y0=600, y1=950)
        if lf % 20 < 12:
            label(ctx, "PLANNING...", 540, 1650, 80, hx('8fe9ff'), 0.04, 1)
    if 90 <= lf < 125:
        for i, (_, nx, ny, a, c, pf) in enumerate(NOTES):
            if pf <= f < pf + 8:
                label(ctx, "POP!", nx, ny - 110, 60, (1, 1, 1), a, 1)
    if lf >= 120:
        # dream bubble
        u = pop(lf, 120, 132)
        ctx.save(); ctx.translate(560, 1180); ctx.scale(max(0.01, eout(u)), max(0.01, eout(u)))
        for i, (bx, by, r) in enumerate(((150, 240, 26), (110, 160, 40))):
            ellipse(ctx, bx, by, r, r); fl(ctx, (1, 1, 1), 6)
        for dx, dy, r in ((-160, 0, 150), (0, -60, 180), (170, 0, 150), (0, 70, 160)):
            ellipse(ctx, dx, dy, r, r * 0.8)
        setc(ctx, INK); ctx.set_line_width(14); ctx.stroke_preserve(); setc(ctx, (1, 1, 1)); ctx.fill()
        # podium + trophy + mini boy
        ctx.rectangle(-90, 20, 180, 110); fl(ctx, hx('ffd23f'), 6)
        text(ctx, "1", 0, 75, 70, hx('ff3b5c'), ow=6, shadow=False)
        draw(ctx, -10, 20 - 186 * 0.6, 0.6, 1, BOY, P(lsh=-160, lel=-10, rsh=-160, rel=-10, eye='happy', mouth='grin'))
        poly(ctx, [(70, -150), (130, -150), (120, -100), (80, -100)]); fl(ctx, hx('ffd23f'), 5)
        ctx.rectangle(92, -100, 16, 30); fl(ctx, hx('ffd23f'), 4)
        for i in range(10):
            t = ((lf + i * 5) % 30) / 30
            ctx.save(); ctx.translate(-200 + i * 45, -160 + t * 260); ctx.rotate(i + t * 6); ctx.rectangle(-8, -4, 16, 8)
            setc(ctx, [hx('ff3b8a'), hx('ffd23f'), hx('3fb6ff'), hx('5fd07a')][i % 4]); ctx.fill(); ctx.restore()
        ctx.restore()
        label(ctx, "FUTURE TOPPER", 540, 1500, 90, hx('ffe14d'), -0.04, pop(lf, 126, 132))
    card(ctx, 'p2', f, 214, 388)


def s4(ctx, f):
    lf = f - 390
    if lf < 40:
        st = ease(pop(lf, 0, 16)) - ease(pop(lf, 26, 40))
        pose = sit_pose(torso=-8 * st, lsh=lerp(60, -170, st), lel=lerp(-50, -10, st), rsh=lerp(66, -172, st), rel=lerp(-56, -10, st), eye='closed' if st > 0.5 else 'normal',
                        mouth='open' if st > 0.5 else 'smile')
        if lf >= 30:
            def ex(ctx, h):
                bx, by = h['front']; phone(ctx, bx + 20, by - 30, -0.2, True)
            pose.update(rsh=60, rel=-70, eye='happy', mouth='grin')
        else:
            ex = None
        desk_shot(ctx, f, 1.35, 430, 1000, pose, prog=1, notes_f=10 ** 5, extra=ex)
        label(ctx, "JUST 5 MINUTES...", 540, 1500, 90, (1, 1, 1), 0.03, pop(lf, 8, 14))
    elif lf < 110:
        tap = math.sin(lf * 1.7)
        pose = sit_pose(torso=14, head=12, lsh=58, lel=-80 + 6 * tap, rsh=62, rel=-86 - 6 * tap, eye='normal', mouth='grin' if lf % 30 < 15 else 'open', blink=blink(f), sway=0.3 * tap)
        def ex(ctx, h):
            bx, by = h['back']; phone(ctx, bx + 30, by - 10, -0.1 + 0.05 * tap, True)
        desk_shot(ctx, f, 2.4, 470, 900, pose, prog=1, notes_f=10 ** 5, extra=ex, rot=2 * math.sin(lf * 0.05))
        g = cairo.RadialGradient(540, 1050, 50, 540, 1050, 700); g.add_color_stop_rgba(0, 0.4, 0.9, 1, 0.25); g.add_color_stop_rgba(1, 0.4, 0.9, 1, 0)
        ctx.set_source(g); ctx.paint()
        if lf % 12 < 6:
            label(ctx, "TAP TAP", 820, 1350, 70, hx('8fe9ff'), 0.1, 1)
        if 80 <= lf < 110:
            label(ctx, "LEVEL UP!", 540, 1500, 100, hx('ffe14d'), -0.05, pop(lf, 80, 85))
    else:
        u = pop(lf, 110, 210)
        tod = 2.0 * ease(u)
        tap = math.sin(lf * 1.7)
        pose = sit_pose(torso=14, head=12, lsh=58, lel=-80 + 6 * tap, rsh=62, rel=-86 - 6 * tap, eye='normal', mouth='grin', sway=0.3 * tap)
        def ex(ctx, h):
            bx, by = h['back']; phone(ctx, bx + 30, by - 10, -0.1, True)
        desk_shot(ctx, f, 1.0, 480, 1000, pose, tod=tod, prog=1, notes_f=10 ** 5, extra=ex, clock_min=605 + 600 * ease(u))
        hlines(ctx, lf, 0.12, col=(1, 1, 1))
        for i, st in enumerate((118, 150, 182)):
            if st <= lf < st + 26:
                label(ctx, "ONE MORE GAME...", 540, 1430 + i * 60, 80 + i * 8, [hx('ffe14d'), hx('ff9a5a'), hx('ff3b5c')][i], (-1) ** i * 0.05, pop(lf, st, st + 5))
        label(ctx, ">> FAST FORWARD", 540, 1700, 50, (1, 1, 1), 0, 1)
    card(ctx, 'p3', f, 394, 598)


def s5(ctx, f):
    lf = f - 600
    if lf < 30:
        ctx.save(); cam(ctx, 300, 470, 3.2, 0, shake_at(lf, [0, 15], 6, 8), f)
        bedroom(ctx, f, 2.0, clock_min=718)
        ctx.restore()
        night(ctx, 0.6)
        if lf % 15 < 8:
            label(ctx, "TICK...", 540, 1350, 100, (1, 1, 1), 0.04, 1)
    else:
        def tom_extra(ctx, h):
            if 92 <= lf < 140:
                hx_, hy_ = h['front']
                if lf < 140:
                    sticky(ctx, "TOMORROW!", hx_ + 40, hy_ - 30, -0.2, hx('ff8a3d'), 1, 30)
        if lf < 60:
            shock = lf >= 40
            pose = sit_pose(torso=-6 if shock else 14, head=-12 if shock else 12, lsh=58, lel=-80, rsh=62, rel=-86, eye='shock' if shock else 'normal', mouth='open' if shock else 'grin')
            def ex(ctx, h):
                bx, by = h['back']; phone(ctx, bx + 30, by - 10, -0.1, not shock)
            z = 1.5 if not shock else kf(lf, [(40, 1.5), (46, 2.2)], eout)
            desk_shot(ctx, f, z, 430, 960, pose, tod=2.0, prog=1, notes_f=10 ** 5, extra=ex, clock_min=719, shake=shake_at(lf, [40], 8, 14))
            if shock:
                label(ctx, "THE BOOKS!!", 540, 1500, 110, hx('ff3b5c'), -0.05, pop(lf, 40, 44))
                for i in range(3):
                    t = ((lf + i * 6) % 18) / 18
                    sweat(ctx, [300, 780, 820][i], 760 + t * 220, 1.6)
        elif lf < 92:
            y_ = math.sin(pop(lf, 60, 92) * math.pi)
            pose = sit_pose(torso=-12 * y_, head=-10 * y_, lsh=lerp(60, -165, y_), lel=-20, rsh=lerp(66, -168, y_), rel=-20, eye='closed', mouth='scream' if y_ > 0.3 else 'smile')
            desk_shot(ctx, f, 1.45, 430, 980, pose, tod=2.0, prog=1, notes_f=10 ** 5, clock_min=719)
            label(ctx, "YAAAWN", 540, 1500, 120, hx('b8c7ff'), 0.03, pop(lf, 64, 70))
        else:
            wr = math.sin(lf * 2.5)
            if lf < 140:
                pose = sit_pose(torso=10, head=8, rsh=80 + 8 * wr, rel=-40 + 8 * wr, eye='smug', mouth='smile')
            elif lf < 150:
                pose = P(torso=-6, rsh=-140, rel=-20, lsh=40, lel=-90, lhip=86, lkn=-86, rhip=88, rkn=-88, eye='happy', mouth='grin')
            else:
                pose = sit_pose(torso=-4, rsh=-60, rel=-120, eye='happy', mouth='grin', head=-6)
            desk_shot(ctx, f, 1.15, 380, 1000, pose, tod=2.0, prog=1, notes_f=10 ** 5, tomorrow=pop(lf, 140, 146), clock_min=719, extra=tom_extra,
                      shake=shake_at(lf, [140], 8, 16))
            if 96 <= lf < 140:
                label(ctx, "WRITING A NEW PLAN...", 540, 1500, 70, (1, 1, 1), 0.03, 1)
            if 140 <= lf < 158:
                label(ctx, "SLAP!", 330, 1000, 120, hx('ff9a5a'), -0.1, pop(lf, 140, 144))
            if lf >= 158:
                label(ctx, "DONE. GOODNIGHT!", 540, 1500, 96, hx('ffe14d'), -0.03, pop(lf, 158, 164))
    card(ctx, 'p4', f, 604, 782)


def s6(ctx, f):
    lf = f - 780
    lamp_on = lf < 10
    cx = kf(lf, [(0, 420), (14, 420), (40, 1120)], ease)
    z = kf(lf, [(0, 1.1), (40, 1.0), (120, 1.0), (210, 1.3)], ease)
    cy = kf(lf, [(0, 1000), (40, 1080), (210, 1170)], ease)
    ctx.save(); cam(ctx, cx, cy, z, 0, 0, f)
    bedroom(ctx, f, 2.0, lamp_on, 1, 10 ** 5, 1, 720)
    chair(ctx); desk(ctx, 3, lamp_on)
    if lf < 42:
        u = pop(lf, 12, 42)
        x = lerp(560, 1150, ease(u)); y = 1500 - math.sin(u * math.pi) * 260
        rot = -90 * ease(pop(lf, 26, 42))
        draw(ctx, x, y - 186 * KB, KB, 1, BOY, run_pose(lf * 0.6, rot=rot, eye='happy', mouth='grin'))
    else:
        b = max(0, 26 * math.sin((lf - 42) * 0.6) * math.exp(-(lf - 42) * 0.2))
        breath = 0.05 * math.sin(lf * 0.12)
        h = draw_hip(ctx, 1230, 1215 - b, KB, 1, BOY, P(rot=-90, head=-6, lsh=-170, lel=-30, rsh=-60, rel=-80, lhip=4, lkn=-6, rhip=10, rkn=-12, eye='closed', mouth='open' if lf % 80 < 40 else 'smile', sq=breath))
        # pillow under head then blanket
        hx_, hy_ = h['head']
        ctx.new_path(); ctx.move_to(1130, 1240 - b); ctx.curve_to(1180, 1130 - b, 1480, 1130 - b, 1520, 1240 - b); ctx.line_to(1520, 1290); ctx.line_to(1130, 1290); ctx.close_path()
        fl(ctx, hx('ff8ab0'), 7)
        for i in range(4):
            ellipse(ctx, 1220 + i * 80, 1210 - b, 16, 16); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()
        # snore bubble
        t = (lf % 80) / 80
        ellipse(ctx, hx_ + 60, hy_ + 40, 20 + 50 * t, 20 + 50 * t); setc(ctx, (0.8, 0.95, 1, 0.6)); ctx.fill_preserve(); setc(ctx, (1, 1, 1, 0.9)); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()
    dark = 0.85 if not lamp_on else 0.45
    night(ctx, dark)
    # moonbeam
    if not lamp_on:
        ctx.new_path(); ctx.move_to(W * 0.15, 0); ctx.line_to(W * 0.5, 0); ctx.line_to(W, H); ctx.line_to(W * 0.45, H); ctx.close_path()
        setc(ctx, (0.75, 0.85, 1, 0.08)); ctx.fill()
    if 8 <= lf < 18:
        label(ctx, "CLICK", 400, 1000, 90, (1, 1, 1), 0.06, 1)
    if lf >= 50:
        for i in range(3):
            t = ((lf + i * 20) % 60) / 60
            label(ctx, "Z", 560 + i * 70 + 40 * math.sin(t * 6), 1000 - t * 300 - i * 50, 70 + i * 20, (1, 1, 1), 0.2, 1 - t * 0.2)
    if lf >= 120:
        label(ctx, "DREAMING OF RANK 1", 540, 1550, 76, hx('b8c7ff'), 0.02, pop(lf, 120, 126))


def s7(ctx, f):
    lf = f - 990
    pose = sit_pose(eye='normal', mouth='grin' if lf > 20 else 'flat', torso=0, head=0, blink=0)
    if lf >= 30:
        pose.update(rsh=-160, rel=-20, eye='happy', mouth='grin')
    desk_shot(ctx, f, kf(lf, [(0, 1.3), (60, 1.45)]), 440, 1000, pose, books=3, tod=3.0, prog=1, notes_f=10 ** 5, tomorrow=1, clock_min=420, hb=1)
    if lf < 6:
        ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.8 * (1 - lf / 6))); ctx.fill()
    if lf >= 30:
        label(ctx, "LET'S GO!", 540, 1480, 120, hx('ffe14d'), -0.06, pop(lf, 30, 35))
    card(ctx, 'p5', f, 992)


SHOTS = [(0, s1), (120, s2), (210, s3), (390, s4), (600, s5), (780, s6), (990, s7)]


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.28)
    ctx.set_source(g); ctx.paint()
    for c in (120, 182, 210, 390, 430, 500, 600, 630, 780, 990):
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.55 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/y{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/study_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
