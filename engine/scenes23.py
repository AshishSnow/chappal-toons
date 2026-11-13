"""'The Remote War' - original, general-audience comedy short, ~22s.
Split-screen ECU: brother vs sister glaring, both gripping ONE TV remote: "MINE!" / "NO, MINE!".
Tug of war on the sofa -> every tug flips the channel -> they stand on the sofa, cushions flying.
The remote slips and flies across the room in slow motion... Mom snatches it out of the air, clicks the TV OFF:
"HOMEWORK. NOW." Twist: kids at the doorway glaring while Mom is on the sofa with popcorn watching HER show.
Loops back to the split-screen glare."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, label, shake_at
import scenes13
from scenes13 import card as _card13
import random

BOY, MOM = doodle.BOY, doodle.MOM_G
SIS = dict(skin=hx('f0c4a0'), hair=hx('7a3a1e'), hairstyle='mom', shirt=hx('ff6fae'), pants=hx('2fbf8a'), shoes=hx('8a3cff'),
           earring=False, sindoor=False, sleeve=1.0)
N = 660
FLOOR = 1430
SEAT = 1225
KB, KS, KM = 1.45, 1.4, 1.75

CAPS = {
    'p1': [[("ONE ", OUT), ("REMOTE", hx('ff3b5c')), (".", OUT)], [("TWO ", OUT), ("KIDS", hx('1f8bff')), (".", OUT)]],
    'p2': [[("THE ", OUT), ("CHANNEL WAR", hx('ff8a1f'))]],
    'p3': [[("THEN IT ", OUT), ("SLIPPED", hx('8a3cff')), ("...", OUT)]],
    'p4': [[("MOM ", OUT), ("CAUGHT IT", hx('ff3b5c'))]],
    'p5': [[("PLOT TWIST: ", OUT)], [("MOM", hx('8a3cff')), (" WANTED THE TV", OUT)]],
}
scenes13.CAPS = CAPS
card = _card13

WALL, WALL2 = hx('ffcf8a'), hx('ffc070')
SOFA, SOFA2 = hx('3fa7a0'), hx('2f8a84')


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


# ------------------------------------------------------------------ props
def remote(ctx, x, y, a=0.0, s=1.0, glow=False):
    """TV remote, long axis vertical before rotation (power button at -y end)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if glow:
        ellipse(ctx, 0, 0, 120, 170); setc(ctx, (1, 1, 0.7, 0.35)); ctx.fill()
    rect_r(ctx, -34, -110, 68, 220, 26); fl(ctx, hx('2a2a3a'), 6)
    ellipse(ctx, 0, -80, 13, 13); setc(ctx, hx('ff3b5c')); ctx.fill()
    for r_ in range(3):
        for c_ in range(2):
            ellipse(ctx, -12 + c_ * 24, -40 + r_ * 26, 8, 8); setc(ctx, hx('d8dde8')); ctx.fill()
    rect_r(ctx, -18, 40, 36, 50, 10); setc(ctx, hx('1f8bff')); ctx.fill()
    ctx.restore()


def cushion(ctx, x, y, a, col):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    rect_r(ctx, -70, -55, 140, 110, 30); fl(ctx, col, 6)
    ctx.move_to(-30, 0); ctx.line_to(30, 0); ink(ctx, 4); ctx.stroke()
    ctx.restore()


def popcorn(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for k in range(7):
        ellipse(ctx, -50 + k * 17, -30 - 12 * (k % 2), 20, 18); fl(ctx, hx('fff6d8'), 3)
    poly(ctx, [(-70, -30), (70, -30), (50, 50), (-50, 50)]); fl(ctx, (1, 1, 1), 5)
    for k in range(3):
        poly(ctx, [(-52 + k * 40, -30), (-36 + k * 40, -30), (-30 + k * 37, 50), (-42 + k * 37, 50)]); setc(ctx, hx('ff3b5c')); ctx.fill()
    ctx.restore()


# ------------------------------------------------------------------ TV
def channel(ctx, k, x, y, w, h, t):
    """draw channel k into screen rect"""
    ctx.save(); ctx.rectangle(x, y, w, h); ctx.clip()
    cx, cy = x + w / 2, y + h / 2
    if k == 0:      # cooking: pot + steam
        ctx.rectangle(x, y, w, h); setc(ctx, hx('ff8a1f')); ctx.fill()
        rect_r(ctx, cx - 120, cy - 10, 240, 120, 20); fl(ctx, hx('d8dde8'), 6)
        for j in range(3):
            ctx.move_to(cx - 60 + j * 60, cy - 30)
            ctx.curve_to(cx - 90 + j * 60, cy - 80, cx - 30 + j * 60, cy - 110, cx - 60 + j * 60, cy - 160 - 10 * math.sin(t + j))
            setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(12); ctx.stroke()
    elif k == 1:    # sports: field + ball
        ctx.rectangle(x, y, w, h); setc(ctx, hx('2fbf5a')); ctx.fill()
        for j in range(5):
            ctx.rectangle(x + j * w / 5, y, w / 10, h); setc(ctx, (1, 1, 1, 0.12)); ctx.fill()
        ctx.move_to(cx, y); ctx.line_to(cx, y + h); setc(ctx, (1, 1, 1)); ctx.set_line_width(6); ctx.stroke()
        ellipse(ctx, cx + 80 * math.sin(t), cy + 20, 46, 46); fl(ctx, (1, 1, 1), 6)
    elif k == 2:    # weather
        ctx.rectangle(x, y, w, h); setc(ctx, hx('5ab8ff')); ctx.fill()
        ellipse(ctx, cx - 90, cy - 40, 70, 70); fl(ctx, hx('ffd23f'), 6)
        for dx, r in ((-50, 50), (10, 70), (70, 50)):
            ellipse(ctx, cx + 60 + dx, cy + 40, r, r * 0.8); fl(ctx, (1, 1, 1), 5)
    elif k == 3:    # news ticker
        ctx.rectangle(x, y, w, h); setc(ctx, hx('1f3a8a')); ctx.fill()
        ellipse(ctx, cx, cy - 20, 110, 110); fl(ctx, hx('5ab8ff'), 6)
        ctx.new_path(); ctx.move_to(cx - 110, cy - 20); ctx.line_to(cx + 110, cy - 20); ctx.move_to(cx, cy - 130); ctx.line_to(cx, cy + 90)
        ink(ctx, 5); ctx.stroke()
        ctx.rectangle(x, y + h - 80, w, 80); setc(ctx, hx('ff3b5c')); ctx.fill()
        text(ctx, "NEWS", x + 120, y + h - 40, 44, (1, 1, 1), outline=hx('ff3b5c'), ow=1, shadow=False)
    elif k == 4:    # nature
        ctx.rectangle(x, y, w, h); setc(ctx, hx('bfeaff')); ctx.fill()
        poly(ctx, [(x - 20, y + h), (cx - 80, cy - 80), (cx + 60, y + h)]); fl(ctx, hx('6b8ac9'), 6)
        poly(ctx, [(cx - 20, y + h), (cx + 120, cy - 30), (x + w + 20, y + h)]); fl(ctx, hx('4a6ab0'), 6)
        poly(ctx, [(cx - 80, cy - 80), (cx - 112, cy - 30), (cx - 48, cy - 30)]); setc(ctx, (1, 1, 1)); ctx.fill()
    elif k == 5:    # static
        rnd = random.Random(int(t * 10))
        ctx.rectangle(x, y, w, h); setc(ctx, hx('8a8a96')); ctx.fill()
        for _ in range(120):
            setc(ctx, (rnd.random(),) * 3); ctx.rectangle(x + rnd.random() * w, y + rnd.random() * h, 18, 8); ctx.fill()
    elif k == 6:    # Mom's show: sunset romance
        g = cairo.LinearGradient(0, y, 0, y + h); g.add_color_stop_rgb(0, 1, 0.55, 0.7); g.add_color_stop_rgb(1, 1, 0.8, 0.45)
        ctx.rectangle(x, y, w, h); ctx.set_source(g); ctx.fill()
        ellipse(ctx, cx, y + h * 0.75, 110, 110); setc(ctx, hx('fff27a')); ctx.fill()
        for j, (dx, s_) in enumerate(((-70, 1.0), (60, 0.7))):
            heart(ctx, cx + dx, cy - 40 - 12 * math.sin(t + j), 60 * s_)
    ctx.restore()


def heart(ctx, x, y, r, col=hx('ff3b5c')):
    ctx.new_path(); ctx.move_to(x, y + r * 0.9)
    ctx.curve_to(x - r * 1.3, y, x - r * 0.7, y - r * 1.0, x, y - r * 0.35)
    ctx.curve_to(x + r * 0.7, y - r * 1.0, x + r * 1.3, y, x, y + r * 0.9); ctx.close_path(); fl(ctx, col, 5)


def tv(ctx, x, y, w, h, ch=0, t=0.0, off=0.0):
    rect_r(ctx, x - 30, y - 30, w + 60, h + 60, 24); fl(ctx, hx('2a2a3a'), 8)
    ctx.rectangle(x, y, w, h); setc(ctx, hx('101018')); ctx.fill()
    if off < 1:
        if off <= 0:
            channel(ctx, ch, x, y, w, h, t)
        else:
            # CRT switch-off: squash to a line, then a dot
            u = off
            hh = h * max(0.02, 1 - u * 2)
            ww = w * (1 if u < 0.5 else max(0.02, 1 - (u - 0.5) * 2))
            ctx.rectangle(x + (w - ww) / 2, y + (h - hh) / 2, ww, hh); setc(ctx, (1, 1, 1)); ctx.fill()
    ellipse(ctx, x + w - 20, y + h + 16, 7, 7); setc(ctx, hx('2fbf5a') if off < 1 else hx('ff3b5c')); ctx.fill()


# ------------------------------------------------------------------ sets
def living(ctx, f):
    ctx.rectangle(-1500, -1500, 4200, 4200); setc(ctx, WALL); ctx.fill()
    for i in range(-14, 26):
        ellipse(ctx, i * 120 + 60, 700 + (i % 2) * 120, 14, 14); setc(ctx, WALL2); ctx.fill()
        ellipse(ctx, i * 120, 1000 + (i % 2) * 120, 14, 14); setc(ctx, WALL2); ctx.fill()
    # picture frame
    rect_r(ctx, 400, 560, 280, 200, 10); fl(ctx, hx('fff8e8'), 7)
    poly(ctx, [(420, 740), (500, 640), (560, 700), (600, 660), (660, 740)]); setc(ctx, hx('2fbf5a')); ctx.fill()
    ellipse(ctx, 620, 610, 22, 22); setc(ctx, hx('ffd23f')); ctx.fill()
    # lamp
    ctx.rectangle(-60, 820, 14, FLOOR - 820); fl(ctx, INK, 3)
    poly(ctx, [(-120, 820), (10, 820), (-20, 720), (-90, 720)]); fl(ctx, hx('ff6f9a'), 6)
    # floor + rug
    ctx.rectangle(-1500, FLOOR, 4200, 900); setc(ctx, hx('b9784a')); ctx.fill()
    for i in range(-14, 26):
        ctx.move_to(i * 140, FLOOR); ctx.line_to(i * 140 - 60, FLOOR + 900); setc(ctx, (0, 0, 0, 0.1)); ctx.set_line_width(5); ctx.stroke()
    ellipse(ctx, 540, FLOOR + 130, 560, 90); fl(ctx, hx('8a3cff'), 6)
    ellipse(ctx, 540, FLOOR + 130, 440, 60); setc(ctx, hx('a86bff')); ctx.fill()
    ctx.move_to(-1500, FLOOR); ctx.line_to(2700, FLOOR); ink(ctx, 8); ctx.stroke()


def sofa_back(ctx, x0=120, x1=960, squash=0.0):
    rect_r(ctx, x0, 930 + squash, x1 - x0, 320, 60); fl(ctx, SOFA, 8)
    for k in range(2):
        xx = lerp(x0, x1, (k + 1) / 3)
        ctx.move_to(xx, 970 + squash); ctx.line_to(xx, 1200); setc(ctx, SOFA2); ctx.set_line_width(6); ctx.stroke()


def sofa_front(ctx, x0=120, x1=960):
    rect_r(ctx, x0 + 20, SEAT - 10, x1 - x0 - 40, 130, 34); fl(ctx, light(SOFA, 0.15), 8)
    ctx.move_to(540 + (x0 + x1 - 1080) / 2, SEAT); ctx.line_to(540 + (x0 + x1 - 1080) / 2, SEAT + 110); setc(ctx, SOFA2); ctx.set_line_width(6); ctx.stroke()
    for ax in (x0 - 40, x1 - 80):
        rect_r(ctx, ax, 1100, 120, 260, 50); fl(ctx, SOFA, 8)
    for lx in (x0 + 10, x1 - 40):
        ctx.rectangle(lx, 1350, 30, FLOOR - 1350); fl(ctx, hx('6b3a1e'), 5)


# ------------------------------------------------------------------ poses
def tug(f_, pull, scream=False, glare=True, stand=False, ph=0.0):
    s_ = math.sin(ph)
    base = dict(rsh=95, rel=-5, lsh=80, lel=10, eye='glare' if glare else 'shock', mouth='scream' if scream else 'grin',
                torso=-14 - 10 * pull, head=6)
    if stand:
        base.update(lhip=8 + 12 * s_, rhip=-14 - 12 * s_, lkn=-6, rkn=-10)
    else:
        base.update(lhip=88, lkn=-82, rhip=95, rkn=-90)
    return P(**base)


def hand_pt(d):
    return d['front']


# ------------------------------------------------------------------ shots
_SCR = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4))


def probe(x, hipy, k, f_, ch, p):
    """where would the head / hands land (no drawing visible)"""
    return draw_hip(_SCR, x, hipy, k, f_, ch, p)


def split_glare(ctx, f, lf, loop=False):
    """two ECU halves: boy top, sister bottom; ONE remote lies across the divider, both gripping it"""
    tugx = 40 * math.sin(lf * 0.7)
    pb = P(rsh=60, rel=-20, lsh=50, lel=-10, eye='glare', mouth='grin', torso=-6, head=4)
    hb = probe(430, SEAT, KB, 1, BOY, pb)['head']
    ctx.save(); ctx.rectangle(0, 0, W, H / 2); ctx.clip()
    ctx.rectangle(0, 0, W, H); setc(ctx, hx('5ab8ff')); ctx.fill()
    rays(ctx, 540, 600, 120, 900, lf * 0.03, col=(1, 1, 1), a=0.25, n=14)
    ctx.save(); cam(ctx, hb[0], hb[1], 1.5, -4, shake_at(lf, [0, 26], 8, 12), f, sx=540 - tugx * 0.3, sy=610)
    draw_hip(ctx, 430, SEAT, KB, 1, BOY, pb)
    ctx.restore(); ctx.restore()
    ps = P(rsh=60, rel=-20, lsh=50, lel=-10, eye='glare', mouth='grin', torso=-6, head=4)
    hs = probe(650, SEAT, KS, -1, SIS, ps)['head']
    ctx.save(); ctx.rectangle(0, H / 2, W, H / 2); ctx.clip()
    ctx.rectangle(0, 0, W, H); setc(ctx, hx('ff8fc4')); ctx.fill()
    rays(ctx, 540, 1230, 120, 900, -lf * 0.03, col=(1, 1, 1), a=0.25, n=14)
    ctx.save(); cam(ctx, hs[0], hs[1], 1.5, 4, shake_at(lf, [12, 36], 8, 12), f, sx=540 + tugx * 0.3, sy=1200)
    draw_hip(ctx, 650, SEAT, KS, -1, SIS, ps)
    ctx.restore(); ctx.restore()
    ctx.rectangle(0, H / 2 - 9, W, 18); setc(ctx, INK); ctx.fill()
    # the one remote, lying across the divider, tugged left/right
    rx = 540 + tugx
    for side, col, y0 in ((-1, BOY['shirt'], 700), (1, SIS['shirt'], 1220)):
        hx_ = rx + side * 120
        ctx.new_path(); ctx.move_to(540 + side * 640, y0); ctx.line_to(hx_ + side * 30, 960)
        setc(ctx, INK); ctx.set_line_width(100); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke_preserve()
        setc(ctx, col); ctx.set_line_width(86); ctx.stroke()
    remote(ctx, rx, 960, math.pi / 2, 1.3)
    for side, sk in ((-1, BOY['skin']), (1, SIS['skin'])):
        ellipse(ctx, rx + side * 120, 960, 52, 48); fl(ctx, sk, 7)
    label(ctx, "MINE!", 540, 860, 96, hx('ffe14d'), -0.05, 1 if loop else pop(lf, 0, 4))
    label(ctx, "NO, MINE!", 540, 1462, 100, hx('ffe14d'), 0.05, 1 if loop else pop(lf, 12, 16))


def sofa_tug(ctx, f, lf, stand=False, cushions=0.0):
    pull = math.sin(lf * 0.55)
    hy = SEAT if not stand else 1080
    bx, sx = 350 - 26 * pull, 730 - 26 * pull
    living(ctx, f)
    sofa_back(ctx)
    sofa_front(ctx)
    k = KB * (1.0 if not stand else 0.95)
    b = draw_hip(ctx, bx, hy - (abs(math.sin(lf * 0.55)) * 20 if stand else 0), k, 1, BOY,
                 tug(1, max(0, pull), scream=stand, stand=stand, ph=lf * 0.55))
    s = draw_hip(ctx, sx, hy - (abs(math.cos(lf * 0.55)) * 20 if stand else 0), KS, -1, SIS,
                 tug(-1, max(0, -pull), scream=stand, stand=stand, ph=lf * 0.55 + 1))
    (x1, y1), (x2, y2) = b['front'], s['front']
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ang = math.atan2(y2 - y1, x2 - x1)
    remote(ctx, mx, my, ang + math.pi / 2, 1.0)
    # strain marks
    for k_ in range(3):
        a_ = -0.6 + k_ * 0.6
        ctx.move_to(mx + math.cos(a_ - 1.57) * 120, my + math.sin(a_ - 1.57) * 120)
        ctx.line_to(mx + math.cos(a_ - 1.57) * 170, my + math.sin(a_ - 1.57) * 170); ink(ctx, 8); ctx.stroke()
    if cushions > 0:
        for j, (x0, vx, vy, col) in enumerate(((300, -9, -34, hx('ff8a1f')), (780, 10, -38, hx('ffd23f')), (540, 2, -44, hx('ff6f9a')))):
            t = max(0, cushions * 60 - j * 6)
            if t > 0:
                cushion(ctx, x0 + vx * t, SEAT - 40 + vy * t + 1.2 * t * t, t * 0.15 * (1 if j % 2 else -1), col)
    return b, s


def s1(ctx, f):
    if f < 50:
        split_glare(ctx, f, f)
    else:
        lf = f - 50
        u = eout(pop(lf, 0, 12))
        ctx.save(); cam(ctx, 540, lerp(1000, 1060, u), lerp(1.5, 1.05, u), 0, shake_at(lf, [0, 20, 40], 6, 10), f)
        sofa_tug(ctx, f, lf)
        ctx.restore()
        label(ctx, "GIVE IT!!", 540, 1440, 140, (1, 1, 1), -0.04, pop(lf, 4, 8))
    card(ctx, 'p1', f, -6, 110)


def s2(ctx, f):
    lf = f - 110
    if lf < 62:
        # TV insert: each tug flips the channel; their hands fighting over the remote below
        chs = [0, 1, 2, 3, 4, 5, 1, 0, 3, 2, 4]
        k = chs[min(len(chs) - 1, lf // 6)]
        ctx.save(); cam(ctx, 540, 920, 1.0 + 0.002 * lf, 0, shake_at(lf % 6, [0], 4, 8), f)
        ctx.rectangle(-1000, -1000, 3000, 4000); setc(ctx, hx('ffcf8a')); ctx.fill()
        rays(ctx, 540, 820, 150, 1100, lf * 0.02, col=(1, 1, 1), a=0.3, n=16)
        tv(ctx, 170, 520, 740, 520, k, lf * 0.3)
        # hands + remote, POV from the sofa
        pull = 40 * math.sin(lf * 1.05)
        rx, ry = 540 + pull, 1230
        for side, col, sk in ((-1, BOY['shirt'], BOY['skin']), (1, SIS['shirt'], SIS['skin'])):
            hx_ = rx + side * 80
            ctx.new_path(); ctx.move_to(540 + side * 560, 1600); ctx.line_to(hx_ + side * 30, ry + 20)
            setc(ctx, INK); ctx.set_line_width(150); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke_preserve()
            setc(ctx, col); ctx.set_line_width(134); ctx.stroke()
            ellipse(ctx, hx_, ry, 70, 64); fl(ctx, sk, 7)
        remote(ctx, rx, ry, math.pi / 2, 1.25)
        ctx.restore()
        label(ctx, "CLICK! CLICK! CLICK!", 540, 1440, 96, hx('ffe14d'), -0.03, pop(lf, 2, 6))
    else:
        # low angle: both standing on the sofa, cushions flying
        il = lf - 62
        ctx.save(); cam(ctx, 540, 1010, 1.0, -3 + 2 * math.sin(il * 0.3), shake_at(il, [0, 22, 44], 8, 14), f)
        sofa_tug(ctx, f, il + 10, stand=True, cushions=min(1, il / 40))
        ctx.restore()
        label(ctx, "WAR!!!", 540, 1440, 150, hx('ff3b5c'), 0.04, pop(il, 2, 6))
    card(ctx, 'p2', f, 114, 230)


def s3(ctx, f):
    lf = f - 240
    # slow-motion: remote spins across the room, both kids diving after it
    u = lf / 130.0
    ctx.save(); cam(ctx, lerp(500, 600, u), 1020, 1.08, 0, 0, f)
    living(ctx, f)
    sofa_back(ctx)
    sofa_front(ctx)
    dive = eout(pop(lf, 6, 60))
    s = draw_hip(ctx, lerp(620, 640, dive), lerp(SEAT - 40, SEAT - 120, dive), KS, 1, SIS,
                 P(rsh=150, rel=0, lsh=165, lel=0, eye='shock', mouth='scream', rot=lerp(0, 72, dive), lhip=-20, rhip=-35, lkn=-20, rkn=-40, head=-20))
    b = draw_hip(ctx, lerp(300, 330, dive), lerp(SEAT - 40, SEAT - 300, dive), KB, 1, BOY,
                 P(rsh=150, rel=0, lsh=165, lel=0, eye='shock', mouth='scream', rot=lerp(0, 66, dive), lhip=-20, rhip=-35, lkn=-20, rkn=-40, head=-20))
    # remote arc
    rx = lerp(560, 1100, u)
    ry = 820 - 220 * math.sin(min(1, u * 1.1) * math.pi * 0.62)
    for j in range(5):
        uu = max(0, u - j * 0.02)
        tx = lerp(560, 1100, uu); ty = 820 - 220 * math.sin(min(1, uu * 1.1) * math.pi * 0.62)
        ellipse(ctx, tx, ty, 40 - j * 6, 40 - j * 6); setc(ctx, (1, 1, 1, 0.4 - j * 0.07)); ctx.fill()
    remote(ctx, rx, ry, lf * 0.12, 1.15, glow=True)
    ctx.restore()
    # slow-mo frame bars
    ctx.rectangle(0, 0, W, 210); setc(ctx, (0, 0, 0, 0.85)); ctx.fill()
    ctx.rectangle(0, H - 260, W, 260); setc(ctx, (0, 0, 0, 0.85)); ctx.fill()
    if lf < 56:
        label(ctx, "SLOW MOTION...", 540, 1440, 96, (1, 1, 1), 0.02, pop(lf, 4, 8))
    else:
        label(ctx, "NOOOOOO!", 540, 1440, 150, hx('ff3b5c'), -0.04, pop(lf, 56, 60))
    card(ctx, 'p3', f, 244, 370)


def s4(ctx, f):
    lf = f - 370
    if lf < 40:
        # ECU: Mom's hand snatches the remote out of the air
        caught = lf >= 6
        pm = P(rsh=10, rel=-10, lsh=20, lel=-30, eye='glare', mouth='flat', torso=-4, head=10)
        pr = probe(560, 1330, KM, -1, MOM, pm)
        hd, hn = pr['head'], pr['front']
        ctx.save(); cam(ctx, hd[0] - 150, hd[1] - 60, 1.2, -6, shake_at(lf, [6], 12, 26), f, sy=1000)
        ctx.rectangle(-1000, -1000, 3000, 4000); setc(ctx, hx('8a3cff')); ctx.fill()
        rays(ctx, hn[0], hn[1] - 120, 100, 1000, lf * 0.04, col=(1, 1, 1), a=0.25, n=18)
        draw_hip(ctx, 560, 1330, KM, -1, MOM, pm)
        hn = (hd[0] - 360, hd[1] - 230)
        sh0 = (hd[0] - 70, hd[1] + 260)
        ctx.new_path(); ctx.move_to(*sh0); ctx.line_to(hn[0] + 30, hn[1] + 60); ctx.line_to(*hn)
        setc(ctx, INK); ctx.set_line_width(112); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
        setc(ctx, MOM["shirt"]); ctx.set_line_width(98); ctx.stroke()
        rxp, ryp = hn[0], hn[1] - 70
        if caught:
            remote(ctx, rxp, ryp, -0.2, 1.1)
            ellipse(ctx, hn[0], hn[1], 46, 46); fl(ctx, MOM['skin'], 7)
            for k in range(8):
                a_ = k * math.pi / 4
                ctx.move_to(rxp + math.cos(a_) * 150, ryp + math.sin(a_) * 150)
                ctx.line_to(rxp + math.cos(a_) * 210, ryp + math.sin(a_) * 210); ink(ctx, 10); ctx.stroke()
        else:
            ellipse(ctx, hn[0], hn[1], 46, 46); fl(ctx, MOM['skin'], 7)
            remote(ctx, lerp(rxp - 400, rxp, lf / 6), lerp(ryp + 500, ryp, lf / 6), lf * 0.4, 1.1, glow=True)
        ctx.restore()
        if caught:
            label(ctx, "SNATCH!", 540, 1450, 150, hx('ffe14d'), -0.04, pop(lf, 6, 10))
    elif lf < 80:
        # insert: TV switches OFF
        il = lf - 40
        ctx.save(); cam(ctx, 540, 860, 1.0 + 0.004 * il, 0, shake_at(il, [8], 6, 10), f)
        ctx.rectangle(-1000, -1000, 3000, 4000); setc(ctx, hx('ffcf8a')); ctx.fill()
        tv(ctx, 170, 560, 740, 520, 1, il * 0.3, off=0 if il < 8 else min(1, (il - 8) / 10))
        ctx.restore()
        label(ctx, "*CLICK*", 540, 1440, 140, (1, 1, 1), 0.04, pop(il, 8, 12))
    else:
        # Mom points: HOMEWORK. NOW.  Kids deflate.
        il = lf - 80
        ctx.save(); cam(ctx, 540, 1020, 1.08, 0, shake_at(il, [10], 8, 14), f)
        living(ctx, f)
        sofa_back(ctx); sofa_front(ctx)
        sag = eout(pop(il, 10, 30))
        draw_hip(ctx, 180, FLOOR - 92 * 1.15, 1.15, 1, BOY, P(rsh=-10, rel=-10, lsh=-15, lel=-10, eye='shock' if il < 10 else 'closed',
                                                             mouth='open' if il < 10 else 'frown', torso=20 * sag, head=25 * sag, rot=0))
        draw_hip(ctx, 410, FLOOR - 92 * 1.1, 1.1, 1, SIS, P(rsh=-10, rel=-10, lsh=-15, lel=-10, eye='shock' if il < 10 else 'closed',
                                                              mouth='open' if il < 10 else 'frown', torso=20 * sag, head=25 * sag))
        m = draw_hip(ctx, 830, FLOOR - 92 * KM, KM, -1, MOM, P(rsh=95, rel=0, lsh=-30, lel=-80, eye='glare', mouth='flat', torso=-4, head=4))
        remote(ctx, m['back'][0] + 10, m['back'][1] - 10, 0.3, 0.8)
        ctx.restore()
        label(ctx, "\"HOMEWORK.\"", 540, 1290, 100, (1, 1, 1), 0.03, pop(il, 4, 8))
        label(ctx, "\"NOW.\"", 540, 1440, 130, hx('ff3b5c'), -0.03, pop(il, 12, 16))
    card(ctx, 'p4', f, 374, 520)


def s5(ctx, f):
    lf = f - 520
    if lf < 106:
        # twist: Mom flopped on the sofa with popcorn watching HER show; kids glaring from the doorway
        ctx.save(); cam(ctx, 540, 1040, lerp(1.0, 1.06, eout(pop(lf, 0, 106))), 0, shake_at(lf, [0], 8, 12), f)
        living(ctx, f)
        # doorway left
        ctx.rectangle(40, 720, 260, FLOOR - 720); setc(ctx, hx('3a2a4a')); ctx.fill()
        peek = eout(pop(lf, 30, 44))
        draw_hip(ctx, lerp(-40, 150, peek), FLOOR - 92 * 1.2, 1.2, 1, SIS, P(eye='glare', mouth='frown', torso=14, head=6, lsh=-10, rsh=20))
        draw_hip(ctx, lerp(-60, 160, peek), FLOOR - 92 * 1.0 + 140, 1.0, 1, BOY, P(eye='glare', mouth='frown', torso=26, head=8, lsh=-10, rsh=20))
        # wall left of the door hides their backs
        ctx.rectangle(-600, 600, 660, FLOOR - 600); setc(ctx, WALL); ctx.fill()
        rect_r(ctx, 40, 700, 260, FLOOR - 700, 8); ink(ctx, 14); ctx.stroke()
        rect_r(ctx, 40, 700, 260, FLOOR - 700, 8); setc(ctx, (1, 1, 1)); ctx.set_line_width(6); ctx.stroke()
        # sofa (centre-right) facing the TV on the right
        sofa_back(ctx, 360, 760)
        sofa_front(ctx, 360, 760)
        bob = 6 * math.sin(lf * 0.3)
        m = draw_hip(ctx, 560, SEAT + 5, KM * 0.9, 1, MOM, P(rsh=60, rel=-90, lsh=40, lel=-60, eye='happy', mouth='grin', torso=-22 + bob * 0.4,
                                                          head=8, lhip=80, lkn=-30, rhip=88, rkn=-20))
        popcorn(ctx, m['back'][0] - 10, m['back'][1] - 10, 0.9)
        # popcorn toss
        t_ = (lf % 24) / 24
        ellipse(ctx, lerp(m['back'][0], m['head'][0] + 40, t_), m['back'][1] - 60 - 140 * math.sin(t_ * math.pi), 14, 13); fl(ctx, hx('fff6d8'), 3)
        # TV on a stand at right
        ctx.rectangle(800, 1240, 170, FLOOR - 1240); fl(ctx, hx('8a5a34'), 6)
        tv(ctx, 815, 1010, 140, 190, 6, lf * 0.15)
        for k in range(3):
            tt = ((lf * 0.02) + k / 3) % 1
            heart(ctx, 660 + 40 * k, 760 - 180 * tt, 26 * (1 - tt * 0.5))
        ctx.restore()
        if lf < 30:
            label(ctx, "\"AHH... MY SHOW.\"", 540, 1440, 100, (1, 1, 1), 0.03, pop(lf, 4, 8))
        else:
            label(ctx, "...WE'VE BEEN PLAYED", 540, 1440, 86, hx('ffe14d'), -0.03, pop(lf, 46, 50))
        card(ctx, 'p5', f, 524, 626)
    else:
        il = lf - 106
        split_glare(ctx, f, il, loop=True)
        card(ctx, 'p1', f, 626)


SHOTS = [(0, s1), (110, s2), (240, s3), (370, s4), (520, s5)]
CUTS = (50, 110, 172, 240, 370, 410, 450, 520, 626)


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
                              "-i", "out/remote_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
