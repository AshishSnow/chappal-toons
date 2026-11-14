"""'I'm Not Tired!' - original, general-audience comedy short, ~22s.
Hook: ECU of the kid at bedtime, wired, bloodshot eyes, huge grin: "I'M NOT TIRED!!" - Mom: "BEDTIME." - he bounces on the bed.
Beat 1: a GIANT yawn ECU; he snaps his eyes open with his fingers: "THAT WASN'T A YAWN!"
Beat 2: the eyelid battle - head nods, "I'M UP!", nods faster, "I'M UP!!"
Beat 3: low angle hero pose on the bed "I COULD STAY UP ALL NIGH-" ... falls asleep standing and tips over like a tree: TIMBER.
Twist: Mom & Dad celebrate "GROWN-UP TIME!", both pass out on the sofa in 2 seconds; at midnight the kid appears in the doorway
fully recharged: "GREAT NAP! LET'S PLAY!" - split screen parents' eyes pop open. Loops to the opening face."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes8 import sit
import scenes13
from scenes13 import card as _card13
import random

BOY = doodle.BOY
DAD = doodle.DAD
MOM = doodle.MOM_G
N = 660
FLOOR = 1460
RED = hx('ff3b5c')
BLUE = hx('1f8bff')
GREEN = hx('3ccf4e')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
LY = 1450   # label baseline (keeps clear of the bottom 420 px)

CAPS = {
    'p1': [[("WHEN THE KID SAYS", OUT)], [("\"I'M NOT TIRED!\"", RED)]],
    'p2': [[("8:01 PM:", OUT)], [("THE FIRST YAWN", BLUE)]],
    'p3': [[("8:03 PM:", OUT)], [("THE EYELIDS FIGHT BACK", ORANGE)]],
    'p4': [[("8:05 PM:", OUT)], [("PARENTS' MOVIE NIGHT", PURPLE)]],
    'p5': [[("PLOT TWIST:", OUT)], [("MIDNIGHT. GUESS WHO'S UP?", RED)]],
}
scenes13.CAPS = CAPS
card = _card13


def label(ctx, s, x, y, size, col, ang=0, t=1.0):
    if t <= 0:
        return
    sc = 0.5 + 0.5 * eout(min(1, t * 2)) + 0.08 * math.sin(min(1, t) * math.pi)
    ctx.save(); ctx.translate(x, y); ctx.scale(sc, sc)
    text(ctx, s, 0, 0, size, col, ang=ang, ow=12, maxw=860)
    ctx.restore()


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
    b = draw_hip(_SCR, 0, 0, 1, f_, ch, p)
    hd, R = b['head'], b['R']
    s = Rt / R
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot)
    ctx.scale(s, s); ctx.translate(-hd[0], -hd[1])
    draw_hip(ctx, 0, 0, 1, f_, ch, p)
    ctx.restore()


def eye_pos(cx, cy, Rt, f_=1):
    return ((cx + f_ * (-0.2 * Rt), cy + 0.06 * Rt, 0.17 * 0.88 * Rt), (cx + f_ * 0.42 * Rt, cy + 0.06 * Rt, 0.17 * Rt))


def lids(ctx, ch, cx, cy, Rt, droop, f_=1, rot=0.0):
    """heavy eyelids over 'shock' eyes drawn by face() at (cx, cy, Rt). droop 0=open, 1=shut"""
    if droop <= 0:
        return
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.translate(-cx, -cy)
    ry = 0.19 * Rt
    for ex, ey, rx in eye_pos(cx, cy, Rt, f_):
        ctx.save(); ellipse(ctx, ex, ey, rx * 1.12, ry * 1.12); ctx.clip()
        yl = ey - ry * 1.15 + 2.3 * ry * min(1, droop)
        ctx.rectangle(ex - rx * 1.3, ey - ry * 1.4, rx * 2.6, yl - (ey - ry * 1.4)); setc(ctx, ch['skin']); ctx.fill()
        ctx.move_to(ex - rx * 1.3, yl); ctx.line_to(ex + rx * 1.3, yl); ink(ctx, Rt * 0.035); ctx.stroke()
        ctx.restore()
        ellipse(ctx, ex, ey, rx, ry); ink(ctx, Rt * 0.03); ctx.stroke()
    ctx.restore()


def bloodshot(ctx, cx, cy, Rt, f_=1, seed=1):
    rnd = random.Random(seed)
    setc(ctx, hx('ff4060')); ctx.set_line_width(Rt * 0.012)
    for ex, ey, rx in eye_pos(cx, cy, Rt, f_):
        for k in range(6):
            a = rnd.uniform(0, 2 * math.pi)
            ctx.move_to(ex + math.cos(a) * rx * 0.95, ey + math.sin(a) * rx * 1.05)
            ctx.line_to(ex + math.cos(a + 0.2) * rx * 0.6, ey + math.sin(a + 0.2) * rx * 0.65)
            ctx.line_to(ex + math.cos(a - 0.1) * rx * 0.42, ey + math.sin(a - 0.1) * rx * 0.45)
            ctx.stroke()
    for ex, ey, rx in eye_pos(cx, cy, Rt, f_):   # dark circles
        ctx.new_path(); ctx.arc(ex, ey + rx * 0.35, rx * 1.05, 0.25 * math.pi, 0.75 * math.pi); setc(ctx, (0.45, 0.25, 0.55, 0.55)); ctx.set_line_width(Rt * 0.03); ctx.stroke()


def zigs(ctx, x, y, r, lf, col=hx('fff27a'), n=6):
    """energy zig-zags around a head"""
    for k in range(n):
        a = k * 2 * math.pi / n + lf * 0.05
        r0 = r + 20 * math.sin(lf * 0.6 + k)
        px, py = x + math.cos(a) * r0, y + math.sin(a) * r0
        ctx.save(); ctx.translate(px, py); ctx.rotate(a)
        ctx.move_to(0, -30); ctx.line_to(30, -10); ctx.line_to(10, 5); ctx.line_to(45, 30)
        setc(ctx, OUT); ctx.set_line_width(22); ctx.stroke_preserve(); setc(ctx, col); ctx.set_line_width(12); ctx.stroke()
        ctx.restore()


def zzz(ctx, x, y, lf, s=1.0, col=hx('c8e6ff')):
    for k in range(3):
        ph = ((lf + k * 14) % 42) / 42
        text(ctx, "Z", x + 60 * ph * s + k * 10, y - 260 * ph * s, (50 + 40 * ph) * s, col + (1,), ow=10, ang=-0.2, shadow=False)


def yawn_mouth(ctx, cx, cy, Rt, g):
    mx, my = cx + 0.04 * Rt, cy + 0.55 * Rt
    ellipse(ctx, mx, my, Rt * (0.22 + 0.1 * g), Rt * (0.12 + 0.3 * g)); fl(ctx, hx('5a1020'), Rt * 0.03)
    ellipse(ctx, mx, my + Rt * 0.22 * g, Rt * 0.16 * g + 1, Rt * 0.1 * g + 1); setc(ctx, hx('ff7f9a')); ctx.fill()
    ctx.rectangle(mx - Rt * 0.12, my - Rt * (0.12 + 0.3 * g) + Rt * 0.01, Rt * 0.24, Rt * 0.06); setc(ctx, (1, 1, 1)); ctx.fill()


# ------------------------------------------------------------------ props / sets
def clock(ctx, x, y, r, hh, mm, s=1.0):
    ellipse(ctx, x, y, r, r); fl(ctx, (1, 1, 1), 7)
    for k in range(12):
        a = k * math.pi / 6
        ctx.move_to(x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8); ctx.line_to(x + math.cos(a) * r * 0.92, y + math.sin(a) * r * 0.92)
    ink(ctx, 5); ctx.stroke()
    am = math.radians(mm * 6 - 90); ah = math.radians((hh % 12 + mm / 60) * 30 - 90)
    ctx.move_to(x, y); ctx.line_to(x + math.cos(ah) * r * 0.5, y + math.sin(ah) * r * 0.5); ink(ctx, 10); ctx.stroke()
    ctx.move_to(x, y); ctx.line_to(x + math.cos(am) * r * 0.78, y + math.sin(am) * r * 0.78); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, x, y, 8, 8); setc(ctx, RED); ctx.fill()


def bedroom(ctx, lights=False, hh=8, mm=0):
    wall = hx('5a6ad8') if lights else hx('27306e')
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, wall); ctx.fill()
    rnd = random.Random(5)
    for k in range(40):   # star wallpaper
        sx, sy = rnd.uniform(-600, 1700), rnd.uniform(300, 1200)
        sparkle(ctx, sx, sy, 14, hx('ffe98a') if not lights else hx('fff6c8'))
    # window with moon
    rect_r(ctx, 90, 560, 330, 380, 20); fl(ctx, hx('122050'), 9)
    ellipse(ctx, 300, 680, 70, 70); setc(ctx, hx('fff2b0')); ctx.fill(); ellipse(ctx, 330, 660, 60, 60); setc(ctx, hx('122050')); ctx.fill()
    ctx.move_to(255, 560); ctx.line_to(255, 940); ctx.move_to(90, 750); ctx.line_to(420, 750); ink(ctx, 8); ctx.stroke()
    clock(ctx, 820, 690, 95, hh, mm)
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('3a2f5a') if not lights else hx('8a5ac8')); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()


def bed_back(ctx, x0=120, x1=960, top=1170):
    rect_r(ctx, x0 - 40, top - 260, 60, FLOOR - top + 260, 18); fl(ctx, hx('ff9f5a'), 8)   # headboard
    rect_r(ctx, x0, top, x1 - x0, 110, 30); fl(ctx, (1, 1, 1), 8)                         # mattress
    rect_r(ctx, x0 + 20, top - 70, 230, 100, 45); fl(ctx, hx('dff1ff'), 7)                 # pillow


def bed_front(ctx, x0=120, x1=960, top=1170, squash=0.0):
    rect_r(ctx, x0 + 200, top + 10 + 20 * squash, x1 - x0 - 190, 150 - 20 * squash, 30); fl(ctx, hx('3ccfb0'), 8)   # blanket
    for k in range(5):
        ctx.move_to(x0 + 260 + k * 140, top + 30); ctx.line_to(x0 + 260 + k * 140, top + 150); setc(ctx, hx('2aa890')); ctx.set_line_width(10); ctx.stroke()
    ctx.rectangle(x0, top + 160, x1 - x0, FLOOR - top - 160); fl(ctx, hx('ff9f5a'), 8)
    for xx in (x0 + 10, x1 - 50):
        ctx.rectangle(xx, FLOOR - 20, 40, 30); fl(ctx, hx('c96a2a'), 6)


def living(ctx, lights=True, tv=0.0, door=0.0):
    wall = hx('6fd6c8') if lights else hx('1d2c50')
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, wall); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 120, -3000, 46, 6000); setc(ctx, dark(wall, 0.94)); ctx.fill()
    # doorway at right
    rect_r(ctx, 780, 620, 300, 840, 10); fl(ctx, hx('ffe9a0') if door > 0 else dark(wall, 0.7), 9)
    if door > 0:
        poly(ctx, [(780, 1460), (1080, 1460), (1400, 2200), (500, 2200)]); setc(ctx, (1, 0.95, 0.6, 0.35 * door)); ctx.fill()
        poly(ctx, [(780, 620), (780 - 160 * door, 580), (780 - 160 * door, 1500), (780, 1460)]); fl(ctx, hx('c96a2a'), 8)
    else:
        rect_r(ctx, 790, 630, 280, 820, 8); fl(ctx, hx('c96a2a') if lights else hx('3a2a40'), 8)
        ellipse(ctx, 820, 1050, 14, 14); fl(ctx, hx('ffd23f'), 4)
    # lamp
    ctx.rectangle(80, 900, 16, 560); fl(ctx, hx('3a3a4a'), 4)
    poly(ctx, [(20, 900), (156, 900), (126, 790), (50, 790)]); fl(ctx, hx('ffd23f') if lights else hx('5a5a3a'), 6)
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('c98a52') if lights else hx('2a2040')); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()
    if tv > 0:   # flicker of the TV (off-screen, front)
        ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, (0.5, 0.8, 1, 0.12 * tv)); ctx.fill()


SEAT = 1270


def sofa_back(ctx):
    rect_r(ctx, 120, 900, 760, 400, 50); fl(ctx, hx('ff5a7a'), 9)
    for x in (140, 500):
        rect_r(ctx, x, 940, 340, 300, 40); fl(ctx, hx('ff7f9a'), 7)


def sofa_front(ctx):
    rect_r(ctx, 120, SEAT - 10, 760, 200, 30); fl(ctx, hx('ff5a7a'), 9)
    for x in (60, 820):
        rect_r(ctx, x, 1060, 120, 380, 50); fl(ctx, hx('e84468'), 9)
    for x in (160, 800):
        ctx.rectangle(x, SEAT + 190, 40, FLOOR - SEAT - 190); fl(ctx, hx('5a3a2a'), 6)


def popcorn(ctx, x, y, s=1.0, spill=0.0, lf=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(-0.9 * spill)
    for k in range(9):
        ellipse(ctx, -70 + (k % 5) * 35, -60 - (k // 5) * 26 + 10 * math.sin(k), 26, 22); fl(ctx, hx('fff6d8'), 4)
    poly(ctx, [(-100, -60), (100, -60), (75, 70), (-75, 70)]); fl(ctx, (1, 1, 1), 7)
    for k in range(4):
        ctx.rectangle(-86 + k * 46, -58, 22, 126); setc(ctx, RED); ctx.fill()
    poly(ctx, [(-100, -60), (100, -60), (75, 70), (-75, 70)]); ink(ctx, 7); ctx.stroke()
    ctx.restore()
    if spill > 0:
        rnd = random.Random(9)
        for k in range(12):
            st = rnd.uniform(0, 0.5); u = clamp((spill - st) / 0.5)
            if u <= 0:
                continue
            px = x - 80 * s - rnd.uniform(0, 200) * u; py = y - 60 * s + 400 * u * u - 120 * u
            ellipse(ctx, px, py, 22 * s, 18 * s); fl(ctx, hx('fff6d8'), 4)


# ------------------------------------------------------------------ shots
def opening_face(ctx, f, lf, lab=True):
    """ECU: the kid, wired at bedtime"""
    sh = shake_at(lf, [0], 12, 22) + 3
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 60)), 0, sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff4fa0')); ctx.fill()
    rays(ctx, 540, 1000, 260, 1600, lf * 0.06, col=(1, 0.95, 0.4), a=0.45, n=18)
    jx = 9 * math.sin(lf * 2.1); jy = 6 * math.cos(lf * 1.7)
    cx, cy, Rt = 540 + jx, 1010 + jy, 330
    face(ctx, BOY, P(eye='shock', mouth='grin' if (lf // 4) % 2 == 0 else 'scream', head=0), cx, cy, Rt, 0.02)
    bloodshot(ctx, cx, cy, Rt, 1, seed=lf // 3)
    zigs(ctx, cx, cy - 40, 470, lf)
    ctx.restore()
    if lab:
        label(ctx, "\"I'M NOT TIRED!!\"", 540, LY, 116, (1, 1, 1), -0.04, pop(lf, 0, 4) if lf > 0 else 1)


def bounce_pose(lf):
    ph = lf * 0.32
    return P(eye='shock', mouth='grin', rsh=170 + 10 * math.sin(ph), rel=-10, lsh=-170 - 10 * math.sin(ph), lel=10,
             lhip=-20 * abs(math.sin(ph)), lkn=30 * abs(math.sin(ph)), rhip=20 * abs(math.sin(ph)), rkn=-30 * abs(math.sin(ph)))


def s1(ctx, f):
    if f < 56:
        opening_face(ctx, f, f)
    else:
        lf = f - 56
        ctx.save(); cam(ctx, 560, 1080, 1.0 + 0.05 * eout(pop(lf, 0, 54)), 0, 2 + shake_at(lf, [0], 8, 12), f)
        bedroom(ctx, lights=True, hh=8, mm=0)
        bed_back(ctx)
        jump = abs(math.sin(lf * 0.16)) * 170
        bed_front(ctx, squash=1 - min(1, jump / 60))
        draw_hip(ctx, 640, 1250 - jump, 1.3, 1, BOY, bounce_pose(lf))
        # Mom in the doorway (left foreground), arms crossed
        mp = P(eye='glare', mouth='flat', lsh=40, lel=-130, rsh=40, rel=-130, head=4)
        draw_hip(ctx, 200, FLOOR - 20, 1.45, 1, MOM, mp)
        ctx.restore()
        if lf < 22:
            label(ctx, "\"BEDTIME.\"", 540, LY, 120, (1, 1, 1), -0.03, pop(lf, 0, 4))
        else:
            label(ctx, "*BOING! BOING!*", 540, LY, 104, hx('fff27a'), 0.04, pop(lf, 22, 26))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 60:
        # giant yawn ECU, slow push-in
        g = eout(pop(lf, 4, 30)) * (1 - 0.15 * pop(lf, 44, 60))
        ctx.save(); cam(ctx, 540, 1080, 1.0 + 0.18 * eout(pop(lf, 0, 60)), 0, 1 + shake_at(lf, [26], 14, 10), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('8fb8ff')); ctx.fill()
        rays(ctx, 540, 1100, 260, 1500, lf * 0.01, col=(1, 1, 1), a=0.3, n=16)
        cx, cy, Rt = 540, 960 - 30 * g, 340
        face(ctx, BOY, P(eye='closed', mouth='flat', head=-6 * g), cx, cy, Rt, -0.08 * g)
        yawn_mouth(ctx, cx, cy, Rt, g)
        for k in range(3):   # yawn wind
            yy = 1300 + k * 50; u = ((lf * 3 + k * 40) % 120) / 120
            ctx.move_to(540 - 200 * u, yy); ctx.curve_to(540 - 300 * u, yy - 30, 540 - 400 * u, yy + 30, 540 - 520 * u, yy)
            setc(ctx, (1, 1, 1, 0.8 * (1 - u))); ctx.set_line_width(10); ctx.stroke()
        ctx.restore()
        label(ctx, "*YAAAAAWN*", 540, LY, 116, hx('fff27a'), -0.03, pop(lf, 8, 12))
    else:
        il = lf - 60
        # dutch-angle ECU: snaps eyes open with his fingers
        ctx.save(); cam(ctx, 540, 1000, 1.06 + 0.06 * eout(pop(il, 0, 60)), 7, 2 + shake_at(il, [0], 12, 20), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd23f')); ctx.fill()
        rays(ctx, 540, 1000, 260, 1600, il * 0.04, col=(1, 1, 1), a=0.4, n=16)
        cx, cy, Rt = 540, 1000, 330
        face(ctx, BOY, P(eye='shock', mouth='grin' if il < 30 else 'wavy', head=0), cx, cy, Rt)
        bloodshot(ctx, cx, cy, Rt, 1, seed=2)
        for ex, ey, rx in eye_pos(cx, cy, Rt):   # fingers propping the eyelids up
            hxp = ex + (-1 if ex < cx else 1) * 20
            rect_r(ctx, hxp - 28, ey - 0.19 * Rt - 210, 56, 200, 28); fl(ctx, BOY['skin'], 8)
            ellipse(ctx, hxp, ey - 0.19 * Rt - 230, 70, 60); fl(ctx, BOY['skin'], 8)
        if il > 30:
            sweat(ctx, 860, 760 + (il % 18) * 6, 2.0)
        ctx.restore()
        label(ctx, "\"THAT WASN'T A YAWN!\"", 540, LY, 104, (1, 1, 1), -0.03, pop(il, 4, 8))
    card(ctx, 'p2', f, 114, 226)


def nod_state(il):
    """returns (droop, drop, snap_frame) for the head-nod battle"""
    seq = [(0, 22, 28), (28, 44, 50), (50, 62, 68)]   # droop start, head falls, snap
    for a, b, c in seq:
        if a <= il < b:
            return pop(il, a, b), 0.0, None
        if b <= il < c:
            return 1.0, eout(pop(il, b, b + 3)), None
    return 0.2, 0.0, None


def s3(ctx, f):
    lf = f - 230
    if lf < 70:
        il = lf
        droop, drop, _ = nod_state(il)
        snaps = [28, 50]
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.04 * sum(1 for s in snaps if il >= s) + 0.02 * pop(il, 0, 70), 0, shake_at(il, snaps, 10, 26), f)
        bedroom(ctx, lights=True, hh=8, mm=3)
        cx, cy, Rt = 540, 1000 + 220 * drop, 290
        rot = 0.5 * drop
        face(ctx, BOY, P(eye='shock' if drop < 0.5 else 'closed', mouth='flat' if drop < 0.5 else 'open', head=0), cx, cy, Rt, rot)
        if drop < 0.5:
            lids(ctx, BOY, cx, cy, Rt, droop * 0.92, 1, rot)
        else:
            zzz(ctx, cx + 260, cy - 220, il, 1.2)
        ctx.restore()
        if 28 <= il < 50:
            label(ctx, "\"I'M UP!\"", 540, LY, 120, (1, 1, 1), -0.04, pop(il, 28, 32))
        elif il >= 50:
            label(ctx, "\"I'M UP!!\"", 540, LY, 140, hx('fff27a'), 0.04, pop(il, 50, 54))
        else:
            label(ctx, "\"I'M... NOT...\"", 540, LY, 100, (1, 1, 1), -0.03, pop(il, 6, 10))
    else:
        il = lf - 70
        # low-angle hero pose on the bed... then TIMBER
        tip = eout(pop(il, 30, 44)) if il < 44 else 1.0
        bounce_land = shake_at(il, [44], 14, 28)
        ctx.save(); cam(ctx, 600, 1000, 1.3 - 0.2 * eout(pop(il, 0, 44)), -5, bounce_land, f, sy=H / 2 + 60)
        bedroom(ctx, lights=True, hh=8, mm=4)
        bed_back(ctx)
        bed_front(ctx)
        fx, fy = 720, 1180
        ctx.save(); ctx.translate(fx, fy); ctx.rotate(-math.radians(84) * tip); ctx.translate(-fx, -fy)
        asleep = il >= 28
        hp = P(eye='closed' if asleep else 'smug', mouth=('open' if asleep else ('grin' if il < 14 else 'open')),
               rsh=170 if not asleep else 150, rel=-10, lsh=40, lel=-120, torso=-4, lhip=8, rhip=-8, head=6 if asleep else -6)
        draw_hip(ctx, fx, fy - 186 * 1.25 + 68 * 1.35 * 1.25, 1.25, 1, BOY, hp)
        ctx.restore()
        if il >= 44:
            zzz(ctx, 420, 900, il, 1.3)
            if il < 56:
                puff(ctx, 560, 1300, pop(il, 44, 56), 1.4)
        ctx.restore()
        if il < 28:
            label(ctx, "\"I COULD STAY UP ALL NIGH—\"", 540, LY, 84, (1, 1, 1), -0.03, pop(il, 2, 6))
        elif il < 44:
            label(ctx, "*TIMBERRR*", 540, LY, 116, hx('ffb35a'), 0.05, pop(il, 30, 34))
        else:
            label(ctx, "*THUD* ZZZ...", 540, LY, 116, hx('c8e6ff'), -0.04, pop(il, 44, 48))
    card(ctx, 'p3', f, 234, 366)


def s4(ctx, f):
    lf = f - 370
    asleep = lf >= 62
    il = lf - 62 if asleep else lf
    ctx.save(); cam(ctx, 520, 1080, 1.0 + (0.05 * eout(pop(lf, 0, 60)) if not asleep else 0.08 + 0.08 * eout(pop(il, 0, 66))), 0,
                    shake_at(lf, [0], 8, 12) + shake_at(il, [10], 10, 16) * asleep, f)
    living(ctx, lights=True, tv=0.6 + 0.4 * math.sin(f * 0.7))
    sofa_back(ctx)
    if not asleep:
        hype = abs(math.sin(lf * 0.3))
        dp = sit(eye='happy', mouth='grin', rsh=150 + 20 * hype, rel=-20, lsh=60, lel=-80, head=-4)
        mp = sit(eye='happy', mouth='open' if (lf // 6) % 2 else 'grin', rsh=60, rel=-80, lsh=150 + 20 * hype, lel=-20, head=4)
    else:
        dp = sit(eye='closed', mouth='open', rsh=20, rel=-30, lsh=30, lel=-40, head=24, torso=8)
        mp = sit(eye='closed', mouth='flat', rsh=20, rel=-40, lsh=20, lel=-40, head=-22, torso=-10)
    bd = draw_hip(ctx, 330, SEAT, 1.15, 1, DAD, dp)
    bm = draw_hip(ctx, 670, SEAT, 1.1, -1, MOM, mp)
    sofa_front(ctx)
    popcorn(ctx, 500, SEAT - 40, 0.9, pop(il, 4, 26) if asleep else 0.0, lf)
    if asleep:
        zzz(ctx, bd['head'][0] - 40, bd['head'][1] - 140, il, 1.0)
        zzz(ctx, bm['head'][0] + 20, bm['head'][1] - 160, il + 20, 0.9)
    else:
        for k in range(4):
            sparkle(ctx, 500 + 360 * math.cos(lf * 0.15 + k * 1.6), 860 + 120 * math.sin(lf * 0.15 + k * 1.6), 26)
    ctx.restore()
    if not asleep:
        label(ctx, "\"FINALLY! GROWN-UP TIME!\"", 540, LY, 92, (1, 1, 1), -0.03, pop(lf, 4, 8))
    elif il < 26:
        label(ctx, "*2 SECONDS LATER*", 540, LY, 100, hx('fff27a'), 0.0, pop(il, 0, 4))
    else:
        label(ctx, "*SNOOOORE*", 540, LY, 116, hx('c8e6ff'), -0.04, pop(il, 26, 30))
    card(ctx, 'p4', f, 374, 496)


def s5(ctx, f):
    lf = f - 500
    if lf < 66:
        door = eout(pop(lf, 6, 16))
        ctx.save(); cam(ctx, 600, 1060, 1.0 + 0.08 * eout(pop(lf, 16, 66)), 0, shake_at(lf, [6], 10, 14), f, sx=W / 2)
        living(ctx, lights=False, tv=0.0, door=door)
        sofa_back(ctx)
        dp = sit(eye='closed', mouth='open', rsh=20, rel=-30, lsh=30, lel=-40, head=24, torso=8)
        mp = sit(eye='closed', mouth='flat', rsh=20, rel=-40, lsh=20, lel=-40, head=-22, torso=-10)
        bd = draw_hip(ctx, 300, SEAT, 1.15, 1, DAD, dp)
        bm = draw_hip(ctx, 620, SEAT, 1.1, -1, MOM, mp)
        sofa_front(ctx)
        zzz(ctx, bd['head'][0] - 40, bd['head'][1] - 140, lf, 0.9)
        if door > 0:
            # the kid in the doorway, fully recharged
            bob = abs(math.sin(lf * 0.3)) * 30
            kp = P(eye='shock', mouth='grin', rsh=170, rel=-10, lsh=-170, lel=10, head=-4)
            b = draw_hip(ctx, 950, FLOOR - 120 - bob, 0.95, -1, BOY, kp)
            for k in range(4):
                sparkle(ctx, b['head'][0] + 170 * math.cos(lf * 0.25 + k * 1.6), b['head'][1] + 150 * math.sin(lf * 0.25 + k * 1.6), 24)
        ctx.restore()
        if lf < 6:
            pass
        elif lf < 20:
            label(ctx, "*CREEEAK*", 540, LY, 110, hx('ffe14d'), 0.04, pop(lf, 6, 10))
        else:
            label(ctx, "\"GREAT NAP! LET'S PLAY!\"", 540, LY, 96, hx('fff27a'), -0.03, pop(lf, 20, 24))
        card(ctx, 'p5', f, 504, 616)
    elif lf < 120:
        il = lf - 66
        # split screen: Dad top, Mom bottom - eyes snap open in horror
        snap = il >= 8
        for k, (ch, y0, bg, f_) in enumerate(((DAD, 0, hx('2b3a8a'), 1), (MOM, H / 2, hx('5a2b8a'), -1))):
            ctx.save(); ctx.rectangle(0, y0, W, H / 2); ctx.clip()
            ctx.translate(0, y0)
            sh = shake_at(il, [8 + k * 3], 12, 22)
            rnd = random.Random(f * 7 + k)
            ctx.translate(rnd.uniform(-1, 1) * sh, rnd.uniform(-1, 1) * sh)
            ctx.rectangle(-100, -100, W + 200, H / 2 + 200); setc(ctx, bg); ctx.fill()
            if snap:
                rays(ctx, 540, 520, 200, 1200, il * 0.03, col=(1, 1, 1), a=0.3, n=16)
            cx, cy, Rt = 540, 560 if k == 0 else 470, 300
            face(ctx, ch, P(eye='shock' if il >= 8 + k * 3 else 'closed', mouth='scream' if il >= 8 + k * 3 else 'flat', head=0), cx, cy, Rt, 0.0, f_)
            if il >= 8 + k * 3:
                bloodshot(ctx, cx, cy, Rt, f_, seed=k + 5)
            ctx.restore()
        ctx.rectangle(0, H / 2 - 8, W, 16); setc(ctx, (1, 1, 1)); ctx.fill()
        ctx.rectangle(0, H / 2 - 8, W, 16); ink(ctx, 5); ctx.stroke()
        if il >= 8:
            label(ctx, "\"NOOOOOO!\"", 540, H / 2, 140, hx('ff6b8a'), -0.04, pop(il, 8, 12))
        card(ctx, 'p5', f, 504, 616)
    else:
        il = lf - 120
        opening_face(ctx, f, il, True)
        card(ctx, 'p1', f, 620)


SHOTS = [(0, s1), (110, s2), (230, s3), (370, s4), (500, s5)]
CUTS = (56, 110, 170, 230, 300, 370, 432, 500, 566, 620)


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
                              "-i", "out/not_tired_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
