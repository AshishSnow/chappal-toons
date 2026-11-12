"""'Where Is My Charger?!' - original desi family comedy short, ~35s."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import cam, pop, sparkle, puff, label, shake_at, room, sofa_back, sofa_front, coffee_table, run_pose, book
from scenes7 import bedroom, chair, desk, night
from scenes8 import head_of, sit, walk, sock
from scenes9 import kitchen

BOY, MOM = doodle.BOY, doodle.MOM
MOMG = dict(MOM, glasses=hx('d0263a'))
N = 1050
STAND = 1500
SEAT = 1235
KB, KM = 1.5, 1.75

CAPS = {
    'p1': [[("WHERE IS", OUT)], [("MY CHARGER?!", hx('1f8bff'))]],
    'p2': [[("THE SCARIEST LINE:", OUT)], [("\"IF I COME AND FIND IT...\"", hx('e0123a'))]],
    'p3': [[("1 HOUR LATER...", hx('7a3cff'))]],
    'p4': [[("MOM'S MAGIC ONLY", OUT)], [("WORKS ON MY STUFF", hx('ff3b5c'))]],
}


def card(ctx, key, f, appear, gone=10 ** 9):
    u = min(pop(f, appear, appear + 6), 1 - pop(f, gone - 5, gone))
    if u <= 0:
        return
    lines = CAPS[key]; size = 70
    ctx.save()
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    widths = [sum(ctx.text_extents(t).x_advance for t, _ in ln) for ln in lines]
    mw = max(widths)
    if mw > 820:
        size *= 820 / mw; ctx.set_font_size(size); widths = [sum(ctx.text_extents(t).x_advance for t, _ in ln) for ln in lines]; mw = max(widths)
    w = mw + 70; lh = size * 1.18; h = lh * len(lines) + 40
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


# ------------------------------------------------------------------ props
def charger(ctx, x, y, a=0, s=1.0, glow=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 10, 0, 0, 200); g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.9 * glow); g.add_color_stop_rgba(1, 1, 0.9, 0.4, 0)
        ctx.set_source(g); ellipse(ctx, 0, 0, 200, 200); ctx.fill()
    ctx.new_path(); ctx.move_to(0, 30); ctx.curve_to(10, 90, 90, 80, 110, 130); ctx.curve_to(130, 170, 60, 190, 40, 150)
    setc(ctx, INK); ctx.set_line_width(14); ctx.stroke_preserve(); setc(ctx, (1, 1, 1)); ctx.set_line_width(7); ctx.stroke()
    ctx.rectangle(-36, -40, 72, 72); fl(ctx, (1, 1, 1), 6)
    for dx in (-14, 14):
        ctx.rectangle(dx - 5, -66, 10, 26); fl(ctx, hx('c7cede'), 3)
    ellipse(ctx, 0, -5, 10, 10); setc(ctx, hx('5fd07a')); ctx.fill()
    ctx.restore()


def flying(ctx, f, t0, seed, cx, cy, kinds, spread=500, dur=24):
    u = pop(f, t0, t0 + dur)
    if not 0 < u < 1:
        return
    rnd = random.Random(seed)
    for i, k in enumerate(kinds):
        ang = rnd.uniform(-2.6, -0.5)
        sp = rnd.uniform(0.6, 1.0) * spread
        x = cx + math.cos(ang) * sp * u
        y = cy + math.sin(ang) * sp * u + 900 * u * u
        rot = u * rnd.uniform(6, 12)
        if k == 'sock':
            sock(ctx, x, y, rot, [hx('ff3b8a'), hx('3fb6ff'), hx('5fd07a')][i % 3])
        elif k == 'book':
            book(ctx, x, y, rot, 0.8, [hx('ff5a5a'), hx('3f8bff'), hx('ffd23f')][i % 3])
        elif k == 'shirt':
            ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
            poly(ctx, [(-50, -40), (-20, -50), (20, -50), (50, -40), (70, -10), (45, 0), (40, 50), (-40, 50), (-45, 0), (-70, -10)])
            fl(ctx, [hx('ff8a3d'), hx('3fb6a8'), hx('b06bff')][i % 3], 5); ctx.restore()
        elif k == 'paper':
            ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.rectangle(-40, -50, 80, 100); fl(ctx, (1, 1, 1), 4); ctx.restore()
        elif k == 'toy':
            ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
            ctx.rectangle(-45, -20, 90, 34); fl(ctx, hx('ff3b5c'), 5)
            for dx in (-25, 25):
                ellipse(ctx, dx, 18, 14, 14); fl(ctx, INK, 3)
            ctx.restore()
        elif k == 'coin':
            ellipse(ctx, x, y, 18, 18); fl(ctx, hx('ffd23f'), 4)


def wardrobe_set(ctx, open_=1.0):
    ctx.rectangle(-900, -900, W + 1800, 2200); ctx.set_source(vgrad(ctx, 0, 0, 0, 1250, [(0, hx('ffe9f2')), (1, hx('ffd6e6'))])); ctx.fill()
    ctx.rectangle(-900, 1250, W + 1800, 1600); setc(ctx, hx('e3c9a8')); ctx.fill()
    ctx.move_to(-900, 1250); ctx.line_to(W + 900, 1250); ink(ctx, 8); ctx.stroke()
    ctx.rectangle(240, 420, 600, 1060); fl(ctx, hx('a86c3a'), 9)
    ctx.rectangle(270, 450, 540, 980); setc(ctx, hx('5a3a20')); ctx.fill()
    ctx.move_to(270, 560); ctx.line_to(810, 560); ink(ctx, 10); ctx.stroke()
    cols = [hx('ff8a3d'), hx('3fb6a8'), hx('b06bff'), hx('ffd23f'), hx('ff3b8a'), hx('5fd07a')]
    for i in range(7):
        x = 300 + i * 72
        poly(ctx, [(x, 570), (x + 60, 570), (x + 66, 820), (x - 6, 820)]); fl(ctx, cols[i % 6], 4)
    for r in range(3):
        for i in range(5):
            ctx.rectangle(290 + i * 100, 900 + r * 160, 90, 110); fl(ctx, cols[(i + r) % 6], 4)
    for side in (0, 1):
        w_ = 270 * (1 - open_ * 0.85)
        x_ = 270 if side == 0 else 810 - w_
        ctx.rectangle(x_, 450, w_, 980); fl(ctx, hx('c98b55'), 6)


def drawer_open(ctx, amt, items=True, charger_in=False):
    """desk drawer pulled out (world coords on the bedroom desk)"""
    dx = 120 * amt
    ctx.rectangle(180 + dx * 0.0, 1300 + dx * 0.25, 240, 90 + dx * 0.4); fl(ctx, hx('8a5a30'), 5)
    ctx.rectangle(180, 1300, 240, 90); fl(ctx, hx('a86c3a'), 5)
    if amt > 0.3:
        ctx.rectangle(190, 1300 - 10 * amt, 220, 20); setc(ctx, hx('5a3a20')); ctx.fill()
        if charger_in:
            charger(ctx, 300, 1285, 0.2, 0.45)


def kitchen_cook(ctx, f):
    kitchen(ctx)
    ctx.rectangle(560, 1040, 380, 60); fl(ctx, hx('3a3f5a'), 7)
    for x in (650, 850):
        ellipse(ctx, x, 1040, 60, 14); setc(ctx, hx('ff6b2c', 0.8)); ctx.fill()
    ctx.new_path(); ctx.move_to(560, 880); ctx.line_to(760, 880); ctx.line_to(740, 1030); ctx.line_to(580, 1030); ctx.close_path(); fl(ctx, hx('c7cede'), 7)
    for i in range(3):
        t = ((f + i * 10) % 30) / 30
        ctx.new_path(); ctx.move_to(610 + i * 50, 860 - t * 160); ctx.curve_to(580 + i * 50, 820 - t * 160, 640 + i * 50, 790 - t * 160, 610 + i * 50, 760 - t * 160)
        setc(ctx, (1, 1, 1, 0.8 * (1 - t))); ctx.set_line_width(8); ctx.stroke()


def ladle(ctx, x, y, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ctx.move_to(0, 0); ctx.line_to(0, 150); ink(ctx, 14); ctx.stroke_preserve(); setc(ctx, hx('c7cede')); ctx.set_line_width(7); ctx.stroke()
    ellipse(ctx, 0, 165, 34, 22); fl(ctx, hx('c7cede'), 6)
    ctx.restore()


def magnifier(ctx, x, y, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ctx.move_to(0, 0); ctx.line_to(0, 110); ink(ctx, 20); ctx.stroke_preserve(); setc(ctx, hx('7a4a2c')); ctx.set_line_width(11); ctx.stroke()
    ellipse(ctx, 0, -60, 60, 60); setc(ctx, (0.8, 0.95, 1, 0.5)); ctx.fill_preserve(); setc(ctx, INK); ctx.set_line_width(14); ctx.stroke()
    ctx.restore()


def glasses_on_head(ctx, h, mom_f=1):
    hx_, hy_ = h['head']; R = h['R']
    for dx in (-R * 0.32, R * 0.32):
        ellipse(ctx, hx_ + dx, hy_ - R * 0.98, R * 0.22, R * 0.15); setc(ctx, (0.8, 0.95, 1, 0.4)); ctx.fill_preserve()
        setc(ctx, hx('d0263a')); ctx.set_line_width(R * 0.06); ctx.stroke()
    ctx.move_to(hx_ - R * 0.1, hy_ - R * 1.0); ctx.line_to(hx_ + R * 0.1, hy_ - R * 1.0); setc(ctx, hx('d0263a')); ctx.set_line_width(R * 0.05); ctx.stroke()


def scan_beams(ctx, h, t, a=1.0):
    for e in ('eyeL', 'eyeR'):
        ex, ey = h[e]
        ang = -0.9 + 1.8 * (0.5 + 0.5 * math.sin(t * 4))
        ctx.move_to(ex, ey); ctx.line_to(ex + math.cos(ang) * 1400, ey + math.sin(ang) * 1400 + 300)
        setc(ctx, (1, 0.2, 0.2, 0.5 * a)); ctx.set_line_width(26); ctx.stroke_preserve(); setc(ctx, (1, 1, 1, 0.8 * a)); ctx.set_line_width(7); ctx.stroke()


def messy_floor(ctx, a=1.0):
    if a <= 0:
        return
    sock(ctx, 480, 1560, 0.6, hx('ff3b8a')); sock(ctx, 900, 1620, -0.4, hx('3fb6ff'))
    book(ctx, 680, 1640, 0.5, 0.8, hx('ffd23f'))
    poly(ctx, [(140, 1560), (230, 1540), (270, 1600), (180, 1640)]); fl(ctx, hx('b06bff'), 4)
    ctx.rectangle(1000, 1520, 70, 90); fl(ctx, (1, 1, 1), 4)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    # hook: frantic search, items exploding out, close then wide
    ctx.save(); cam(ctx, 520, kf(f, [(0, 900), (40, 1080)], eout), kf(f, [(0, 2.0), (40, 1.1)], eout), 3 * math.sin(f * 0.3), shake_at(f, [8, 30, 52, 74], 6, 12), f)
    bedroom(ctx, f, 0.2, True, 0, None, 0, 600); chair(ctx); desk(ctx, 3)
    messy_floor(ctx, pop(f, 20, 40))
    ph = f * 0.9
    pose = P(torso=10 + 10 * math.sin(ph), head=10 * math.sin(ph * 1.3), lsh=-150 + 80 * math.sin(ph), lel=-30, rsh=-140 + 90 * math.sin(ph + 2), rel=-40,
             lhip=10, rhip=-10, eye='shock', mouth='scream', sway=0.8 * math.sin(ph))
    draw(ctx, 520 + 60 * math.sin(f * 0.15), STAND - 186 * KB, KB, 1 if math.sin(f * 0.15) > 0 else -1, BOY, pose)
    for i, t0 in enumerate((4, 26, 48, 70)):
        flying(ctx, f, t0, i, 520, 1150, ['sock', 'book', 'shirt', 'toy', 'paper'][i:] + ['sock'], 520, 26)
    ctx.restore()
    for i in range(3):
        t = ((f + i * 6) % 18) / 18
        sweat(ctx, [300, 780, 820][i], 820 + t * 220, 1.5)
    label(ctx, "WHERE IS IT?!", 540, 1520, 120, hx('ffe14d'), -0.05, pop(f, 6, 11))
    card(ctx, 'p1', f, 2, 328)


SEARCH = [(100, 'bed'), (160, 'wardrobe'), (220, 'sofa'), (280, 'drawer')]


def s2(ctx, f):
    lf = f - 100
    which = [w for t0, w in SEARCH if t0 <= f][-1]
    t0 = [t for t, w in SEARCH if w == which][0]
    ll = f - t0
    if which == 'bed':
        ctx.save(); cam(ctx, 1050, 1180, 1.15, 0, shake_at(ll, [10, 30], 6, 10), f)
        bedroom(ctx, f, 0.2, True, 0, None, 0, 604)
        dig = math.sin(ll * 1.2)
        draw_hip(ctx, 860, 1450, KB, 1, BOY, P(rot=80, head=-60, lsh=40 + 30 * dig, lel=-20, rsh=60 - 30 * dig, rel=-20, lhip=4, lkn=10, rhip=-4, rkn=20, eye='shock', mouth='open'))
        flying(ctx, f, t0 + 6, 11, 1000, 1400, ['sock', 'toy', 'coin', 'book'], 600, 24)
        flying(ctx, f, t0 + 26, 12, 1000, 1400, ['paper', 'sock', 'coin'], 600, 24)
        ctx.restore()
        label(ctx, "UNDER THE BED?", 540, 1450, 84, (1, 1, 1), 0.03, pop(ll, 2, 7))
    elif which == 'wardrobe':
        ctx.save(); cam(ctx, 540, 1080, 1.05, 0, shake_at(ll, [8, 28], 6, 10), f)
        wardrobe_set(ctx, 1.0)
        dig = math.sin(ll * 1.3)
        draw(ctx, 540, STAND - 186 * KB, KB, 1, BOY, P(torso=-6, head=-14, lsh=-120 + 40 * dig, lel=-40, rsh=-130 - 40 * dig, rel=-40, eye='shock', mouth='open'))
        flying(ctx, f, t0 + 4, 21, 540, 900, ['shirt', 'shirt', 'sock', 'shirt'], 650, 24)
        flying(ctx, f, t0 + 26, 22, 540, 900, ['shirt', 'sock', 'shirt'], 650, 24)
        ctx.restore()
        label(ctx, "IN THE WARDROBE?", 540, 1560, 84, (1, 1, 1), 0.03, pop(ll, 2, 7))
    elif which == 'sofa':
        ctx.save(); cam(ctx, 470, 1120, 1.15, 0, shake_at(ll, [8, 30], 6, 10), f)
        room(ctx, f); sofa_back(ctx); sofa_front(ctx, ease(pop(ll, 6, 14))); coffee_table(ctx)
        dig = math.sin(ll * 1.2)
        draw(ctx, 440, STAND - 186 * KB, KB, 1, BOY, P(torso=30, head=20, lsh=60 + 30 * dig, lel=-30, rsh=70 - 30 * dig, rel=-30, eye='shock', mouth='wavy'))
        flying(ctx, f, t0 + 10, 31, 420, 1250, ['coin', 'coin', 'paper', 'coin', 'sock'], 500, 22)
        ctx.restore()
        label(ctx, "SOFA? ONLY COINS...", 540, 1560, 80, hx('ffd23f'), 0.03, pop(ll, 12, 17))
    else:
        ctx.save(); cam(ctx, 420, 1180, 1.35, 0, shake_at(ll, [10], 6, 10), f)
        bedroom(ctx, f, 0.3, True, 0, None, 0, 610); chair(ctx); desk(ctx, 3)
        drawer_open(ctx, ease(pop(ll, 4, 10)) - ease(pop(ll, 34, 40)))
        draw(ctx, 600, STAND - 186 * KB, KB, -1, BOY, P(torso=24, head=18, lsh=60, lel=-40, rsh=80 + 20 * math.sin(ll * 1.4), rel=-30, eye='shock', mouth='open'))
        flying(ctx, f, t0 + 10, 41, 300, 1300, ['paper', 'paper', 'coin', 'paper'], 450, 22)
        ctx.restore()
        label(ctx, "DESK DRAWER?", 540, 1560, 84, (1, 1, 1), 0.03, pop(ll, 2, 7))
        if ll >= 40:
            label(ctx, "10 MINUTES LATER...", 540, 1680, 66, hx('8fe9ff'), 0.02, pop(ll, 40, 44))
    if 22 <= ll < 34 or (which == 'bed' and ll >= 44):
        label(ctx, "NOT HERE!", 540, 1080, 130, hx('ff3b5c'), -0.08, pop(ll, 22, 26) if ll < 44 else 1)
    card(ctx, 'p1', f, 2, 328)


def s3(ctx, f):
    lf = f - 330
    if lf < 40:
        ctx.save(); cam(ctx, 540, 1000, 1.4, 0, 0, f)
        bedroom(ctx, f, 0.3, True, 0, None, 0, 612); chair(ctx); desk(ctx, 3); messy_floor(ctx)
        draw(ctx, 540, STAND - 186 * KB, KB, 1, BOY, P(torso=-10, head=-16, lsh=-60, lel=-80, rsh=-50, rel=-90, eye='closed', mouth='scream', sq=0.05 * math.sin(lf)))
        ctx.restore()
        label(ctx, "MOM! WHERE IS", 540, 1430, 96, hx('ffe14d'), -0.03, pop(lf, 2, 6))
        label(ctx, "MY CHARGER?!", 540, 1540, 110, hx('ffe14d'), 0.03, pop(lf, 6, 10))
    else:
        threat = lf >= 54
        z = kf(lf, [(40, 1.2), (54, 1.2), (66, 2.0), (90, 2.15)], eout)
        pose = P(lsh=40, lel=-110, rsh=-80 if not threat else 100, rel=-60 if not threat else -10, eye='normal' if not threat else 'glare',
                 mouth='smile' if not threat else 'frown', lhip=8, rhip=-8, head=-4 if threat else 6)
        (hxp, hyp), R = head_of(330, STAND - 186 * KM, KM, -1, MOM, pose)
        ctx.save(); cam(ctx, lerp(560, hxp, pop(lf, 54, 66)), lerp(1100, hyp + 150, pop(lf, 54, 66)), z, 0, shake_at(lf, [54], 10, 18), f)
        kitchen_cook(ctx, f)
        h = draw(ctx, 330, STAND - 186 * KM, KM, -1, MOM, pose)
        hx_, hy_ = h['front']; ladle(ctx, hx_, hy_ - 30, 2.6 if threat else 0.4 + 0.3 * math.sin(lf * 0.5))
        ctx.restore()
        if threat:
            ctx.rectangle(0, 0, W, H); setc(ctx, (0.6, 0, 0.1, 0.2)); ctx.fill()
            speed_lines(ctx, 540, 960, lf // 2, 0.3, n=50, inner=520, col=INK)
            label(ctx, "IF I COME AND", 540, 1440, 96, (1, 1, 1), -0.03, pop(lf, 56, 60))
            label(ctx, "FIND IT...", 540, 1560, 130, hx('ff3b5c'), 0.03, pop(lf, 62, 66))
        else:
            label(ctx, "*STIRRING*", 540, 1520, 76, (1, 1, 1), 0.03, 1)
        card(ctx, 'p2', f, 386, 470)


def s4(ctx, f):
    lf = f - 420
    if lf < 70:
        # slow-mo dramatic entrance, low angle, scanning eyes
        u = pop(lf, 0, 50)
        mx = lerp(1150, 720, ease(u))
        pose = walk(lf * 0.22, eye='glare', mouth='frown') if u < 1 else P(eye='glare', mouth='frown', lsh=40, lel=-135, rsh=35, rel=-138)
        ctx.save(); cam(ctx, 640, 1250, 1.05, -4, 0, f)
        bedroom(ctx, f, 0.3, True, 0, None, 0, 615); chair(ctx); desk(ctx, 3); messy_floor(ctx)
        draw(ctx, 260, STAND - 186 * KB, KB, 1, BOY, P(eye='shock', mouth='open', lsh=8, rsh=-8))
        h = draw(ctx, mx, STAND - 186 * KM, KM, -1, MOM, pose)
        if lf >= 50:
            scan_beams(ctx, h, lf * 0.05, pop(lf, 50, 54))
        ctx.restore()
        hlines(ctx, lf, 0.2, col=(1, 1, 1))
        label(ctx, "*SLOW MOTION*", 540, 1580, 70, (1, 1, 1), 0.02, 1)
        if lf >= 52:
            label(ctx, "SCANNING...", 540, 1460, 90, hx('ff3b5c'), -0.03, pop(lf, 52, 56))
    else:
        found = lf >= 92
        ctx.save(); cam(ctx, kf(lf, [(70, 430), (92, 430), (98, 640)], eout), 1150, kf(lf, [(70, 1.2), (92, 1.2), (98, 1.2)], eout), 0, shake_at(lf, [92], 8, 14), f)
        bedroom(ctx, f, 0.3, True, 0, None, 0, 616); chair(ctx); desk(ctx, 3); messy_floor(ctx)
        drawer_open(ctx, ease(pop(lf, 74, 82)), charger_in=not found)
        mp = P(torso=20 if lf < 92 else -4, head=10, lsh=40, lel=-110, rsh=70 if lf < 92 else -160, rel=-30 if lf < 92 else -10,
               eye='normal' if lf < 92 else 'smug', mouth='flat' if lf < 92 else 'smile')
        h = draw(ctx, 560, STAND - 186 * KM, KM, -1, MOM, mp)
        if found:
            hx_, hy_ = h['front']
            charger(ctx, hx_, hy_ - 60, -0.2, 1.0, glow=1.0)
        draw(ctx, 900, STAND - 186 * KB, KB, -1, BOY, P(eye='shock', mouth='scream' if found else 'open', lsh=-150 if found else 8, rsh=-160 if found else -8, lel=-30, rel=-30))
        ctx.restore()
        if lf < 92:
            label(ctx, "1 SECOND.", 540, 1560, 110, (1, 1, 1), -0.03, pop(lf, 74, 78))
        else:
            label(ctx, "TING!", 760, 640, 110, hx("ffe14d"), 0.1, pop(lf, 92, 96))
            if lf >= 104:
                label(ctx, "I LOOKED THERE!!", 540, 1560, 96, hx('ff3b5c'), 0.04, pop(lf, 104, 108))
    card(ctx, 'p2', f, 386, 470)


def s5(ctx, f):
    lf = f - 560
    ctx.save(); cam(ctx, 560, 1080, 1.15, 0, shake_at(lf, [6, 70], 8, 14), f)
    bedroom(ctx, f, 0.3, True, 0, None, 0, 620); chair(ctx); desk(ctx, 3); messy_floor(ctx)
    point = math.sin(lf * 0.9)
    if lf < 70:
        mp = P(lsh=40, lel=-130, rsh=95, rel=-5 + 6 * point, eye='glare', mouth='scream' if lf % 16 < 10 else 'frown', torso=6, lhip=8, rhip=-8)
    else:
        mp = P(lsh=40, lel=-130, rsh=60 + 60 * pop(lf, 70, 76), rel=-60, eye='glare', mouth='scream' if lf % 16 < 10 else 'frown', lhip=8, rhip=-8)
    h = draw(ctx, 330, STAND - 186 * KM, KM, 1, MOM, mp)
    hx_, hy_ = h['front']
    charger(ctx, hx_ + 20, hy_ - 40, 0.3, 0.8)
    deflate = pop(lf, 110, 140)
    draw(ctx, 820, STAND - 186 * KB, KB, -1, BOY, P(eye='shock' if lf < 110 else 'closed', mouth='wavy', lsh=8, rsh=-8, sq=-0.12 * deflate, torso=8 * deflate, head=14 * deflate))
    ctx.restore()
    if lf < 70:
        label(ctx, "YOU NEVER LOOK", 540, 1440, 96, hx('ffe14d'), -0.03, pop(lf, 4, 8))
        label(ctx, "PROPERLY!", 540, 1550, 120, hx('ffe14d'), 0.03, pop(lf, 10, 14))
    elif lf < 110:
        label(ctx, "NOW CLEAN THIS ROOM!", 540, 1520, 76, hx('ff3b5c'), -0.03, pop(lf, 72, 76))
    else:
        label(ctx, "...YES MOM.", 540, 1520, 100, (1, 1, 1), 0.02, pop(lf, 112, 117))


def s6(ctx, f):
    lf = f - 720
    ctx.save(); cam(ctx, 520, 1100, 1.1, 0, shake_at(lf, [30, 70, 110], 6, 10), f)
    room(ctx, f); sofa_back(ctx); sofa_front(ctx, ease(pop(lf, 20, 40))); coffee_table(ctx)
    frantic = math.sin(lf * 0.9)
    mp = P(torso=24 + 8 * frantic, head=14, lsh=60 + 40 * frantic, lel=-40, rsh=-150 + 60 * frantic, rel=-40, eye='shock', mouth='scream' if lf % 18 < 10 else 'open', lhip=8, rhip=-8)
    mx = 420 + 120 * math.sin(lf * 0.06)
    h = draw(ctx, mx, STAND - 186 * KM, KM, 1 if math.cos(lf * 0.06) > 0 else -1, MOM, mp)
    glasses_on_head(ctx, h)
    for i, t0 in enumerate((24, 64, 104)):
        u = pop(lf, t0, t0 + 22)
        if 0 < u < 1:
            ctx.save(); ctx.translate(mx + (i - 1) * 200 * u, 1200 - math.sin(u * math.pi) * 380 + 300 * u * u); ctx.rotate(u * 8)
            ctx.rectangle(-90, -55, 180, 110); fl(ctx, hx('5fd0c0'), 6); ctx.restore()
    if lf >= 120:
        draw(ctx, 900, STAND - 186 * KB, KB, -1, BOY, P(eye='smug', mouth='grin', rsh=90, rel=-30, lsh=10))
    ctx.restore()
    if lf < 120:
        label(ctx, "WHERE ARE MY", 540, 1440, 96, hx('ffe14d'), -0.03, pop(lf, 6, 10))
        label(ctx, "GLASSES?!", 540, 1550, 120, hx('ffe14d'), 0.03, pop(lf, 12, 16))
        if lf >= 40:
            ctx.save(); hx_, hy_ = 0, 0
            label(ctx, "(ON HER HEAD)", 540, 1680, 60, hx('8fe9ff'), 0.02, pop(lf, 40, 44))
            ctx.restore()
    else:
        label(ctx, "...", 540, 1520, 130, (1, 1, 1), 0, pop(lf, 120, 124))
    card(ctx, 'p3', f, 722, 900)


def s7(ctx, f):
    lf = f - 900
    ctx.save(); cam(ctx, kf(lf, [(0, 600), (60, 600), (66, 480)], eout), 1080, kf(lf, [(0, 1.25), (60, 1.25), (66, 1.6), (110, 1.6), (116, 1.1)], eout), 0, shake_at(lf, [110], 10, 18), f)
    room(ctx, f); sofa_back(ctx); sofa_front(ctx, 1.0); coffee_table(ctx)
    if lf < 34:
        mp = P(lsh=40, lel=-130, rsh=35, rel=-136, eye='shock', mouth='open', lhip=8, rhip=-8)
        h = draw(ctx, 420, STAND - 186 * KM, KM, 1, MOM, mp); glasses_on_head(ctx, h)
    elif lf < 60:
        mp = P(lsh=40, lel=-130, rsh=-170, rel=-60, eye='normal', mouth='flat', lhip=8, rhip=-8)
        h = draw(ctx, 420, STAND - 186 * KM, KM, 1, MOM, mp); glasses_on_head(ctx, h)
    elif lf < 110:
        mp = P(lsh=40, lel=-130, rsh=35, rel=-136, eye='normal', mouth='flat', lhip=8, rhip=-8, head=-4)
        h = draw(ctx, 420, STAND - 186 * KM, KM, 1, MOMG, mp)
    else:
        mp = P(lsh=40, lel=-130, rsh=95, rel=-5, eye='glare', mouth='scream', lhip=8, rhip=-8)
        h = draw(ctx, 420, STAND - 186 * KM, KM, 1, MOMG, mp)
    if lf < 110:
        draw(ctx, 850, STAND - 186 * KB, KB, -1, BOY, P(eye='smug' if lf < 60 else 'happy', mouth='grin', rsh=90 if lf < 34 else 30, rel=-30 if lf < 34 else -100, lsh=10))
    else:
        u = pop(lf, 116, 140)
        draw(ctx, lerp(850, 1400, ease(u)), STAND - 186 * KB - abs(math.sin(lf * 0.8)) * 30, KB, 1, BOY, run_pose(lf * 1.2, eye='shock', mouth='scream'))
    ctx.restore()
    if lf < 34:
        label(ctx, "THEY'RE ON YOUR HEAD.", 540, 1520, 72, hx('8fe9ff'), -0.03, pop(lf, 2, 6))
    elif lf < 60:
        label(ctx, "*TOUCH*", 540, 1520, 90, (1, 1, 1), 0.03, 1)
    elif lf < 110:
        if 66 <= lf < 84:
            label(ctx, "*CRICKETS*", 540, 1680, 66, hx('8fe9ff'), 0.02, 1)
        if lf >= 84:
            label(ctx, "...I KNEW THAT.", 540, 1560, 110, hx('ffe14d'), -0.03, pop(lf, 84, 88))
    else:
        label(ctx, "GO STUDY!!", 540, 1540, 140, hx('ff3b5c'), 0.04, pop(lf, 110, 114))
    card(ctx, 'p4', f, 1004)


SHOTS = [(0, s1), (100, s2), (330, s3), (420, s4), (560, s5), (720, s6), (900, s7)]


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.28)
    ctx.set_source(g); ctx.paint()
    for c in (100, 160, 220, 280, 330, 370, 420, 490, 560, 720, 900):
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.55 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/b{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/charger_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
