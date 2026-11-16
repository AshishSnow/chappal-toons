"""'I Know a Shortcut' - original, general-audience comedy short, ~22s.
Hook: ECU Dad, smug grin, finger up, sparkles: "I KNOW A SHORTCUT!"
 -> windshield cam: Mom: "GPS says 10 minutes..." Dad: "TRUST ME!" *SCREECH* whip turn.
Beat 1 (DIRT ROAD): side view, car bouncing on a dirt track, GPS bubble 'RECALCULATING...', a cow sits in the road.
 HONK -> the cow lies down for a nap. "...she'll move."
Beat 2 (RIVER): "It's SHALLOW!" SPLOOSH. Windshield cam half underwater, fish swim past. "Totally NORMAL."
Beat 3 (MUD): car bursts out into mud, SPLAT on the lens, low-angle reveal: mud + hay + a chicken on the roof. "SEE? WE MADE IT!"
Twist: split screen - the spotless neighbours at the party: "Took the highway. 8 minutes." Dad's jaw drops... then grins:
 "Going home? I know a SHORTCUT!" Mom + kid: "NOOOO!" chicken faints -> loops to the opening ECU."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes29 import car_front
from scenes14 import sweat
import scenes13
from scenes13 import card as _card13
import random

BOY = doodle.BOY
MOM = doodle.MOM_G
DAD = doodle.DAD
NEI = doodle.NEIGHBOR
NMOM = doodle.NMOM
N = 660
GY = 1330
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
MUD = hx('7a4a22')
MUD2 = hx('9a6230')
WATER = hx('3aa8ff')
LY = 1450

CAPS = {
    'p1': [[("DAD:", OUT)], [("\"I KNOW A SHORTCUT\"", PINK)]],
    'p2': [[("MINUTE 5:", OUT)], [("THE \"ROAD\"", ORANGE)]],
    'p3': [[("MINUTE 40:", OUT)], [("WAIT... A RIVER?!", BLUE)]],
    'p4': [[("MINUTE 90:", OUT)], [("DAD = GENIUS?", GREEN)]],
    'p5': [[("PLOT TWIST:", OUT)], [("THE NEIGHBORS", PURPLE)]],
}
scenes13.CAPS = CAPS
card = _card13


def label2(ctx, a, b, col, t, size=104, col2=None, y=LY):
    label(ctx, a, 540, y - 60, size, col, -0.03, t)
    label(ctx, b, 540, y + 50, size, col2 or col, 0.02, t)


# ------------------------------------------------------------------ props
def mud_blobs(ctx, x0, y0, w, h, amt, seed=1, col=MUD):
    if amt <= 0:
        return
    rnd = random.Random(seed)
    for k in range(int(26 * amt)):
        x, y = x0 + rnd.uniform(0, w), y0 + h * (1 - rnd.random() ** 1.6)
        r = rnd.uniform(18, 46)
        ellipse(ctx, x, y, r * 1.2, r, rnd.uniform(0, 3)); setc(ctx, col if k % 3 else MUD2); ctx.fill()


def hay(ctx, x, y, s, seed=2, n=9):
    rnd = random.Random(seed)
    for k in range(n):
        a = rnd.uniform(-0.9, 0.9) - math.pi / 2
        l = rnd.uniform(30, 70) * s
        ctx.move_to(x + rnd.uniform(-30, 30) * s, y); ctx.rel_line_to(math.cos(a) * l, math.sin(a) * l)
    setc(ctx, hx('ffd23f')); ctx.set_line_width(6 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def chicken(ctx, x, y, s, a=0.0, faint=False, flap=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    for lx in (-12, 12):
        ctx.move_to(lx, 20); ctx.line_to(lx, 46); ctx.rel_line_to(10, 0)
    setc(ctx, hx('ff9a1f')); ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    poly(ctx, [(-40, -10), (-70, -40), (-62, 4)]); fl(ctx, (1, 1, 1), 5)
    ellipse(ctx, 0, 0, 46, 36); fl(ctx, (1, 1, 1), 6)
    ctx.save(); ctx.translate(-4, 0); ctx.rotate(-0.6 * flap)
    ellipse(ctx, 0, 6, 24, 15); fl(ctx, hx('eeeeee'), 5); ctx.restore()
    for cx_ in (26, 38, 50):
        ellipse(ctx, cx_, -58 + abs(cx_ - 38) * 0.3, 9, 11); fl(ctx, hx('ff3b3b'), 4)
    ellipse(ctx, 36, -32, 24, 24); fl(ctx, (1, 1, 1), 6)
    poly(ctx, [(56, -36), (78, -28), (56, -22)]); fl(ctx, hx('ff9a1f'), 4)
    ellipse(ctx, 50, -14, 6, 9); setc(ctx, hx('ff3b3b')); ctx.fill()
    if faint:
        ink(ctx, 4)
        for dx in (-6, 6):
            ctx.move_to(40 + dx - 5, -40 - 5); ctx.line_to(40 + dx + 5, -40 + 5)
        ctx.move_to(40 - 1 - 5, -40 + 5); ctx.line_to(40 - 1 + 5, -40 - 5); ctx.stroke()
    else:
        ellipse(ctx, 42, -36, 5, 6); setc(ctx, INK); ctx.fill()
    ctx.restore()


def fish(ctx, x, y, s, col=hx('ff8a1f'), d=1, wig=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s * d, s); ctx.rotate(0.15 * math.sin(wig))
    poly(ctx, [(-50, 0), (-90, -32), (-90, 32)]); fl(ctx, dark(col, 0.85), 5)
    ellipse(ctx, 0, 0, 60, 34); fl(ctx, col, 6)
    ellipse(ctx, 30, -8, 9, 10); fl(ctx, (1, 1, 1), 3); ellipse(ctx, 32, -7, 4, 5); setc(ctx, INK); ctx.fill()
    ctx.new_path(); ctx.arc(52, 10, 7, 1.0, 2.6); ink(ctx, 4); ctx.stroke()
    ctx.restore()


def bubbles(ctx, x, y, lf, n=6, seed=3):
    rnd = random.Random(seed)
    for k in range(n):
        ph = (lf * rnd.uniform(4, 8) + rnd.uniform(0, 200)) % 260
        ellipse(ctx, x + rnd.uniform(-80, 80) + 10 * math.sin(lf * 0.2 + k), y - ph, 10 + k % 3 * 5, 10 + k % 3 * 5)
        setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(4); ctx.stroke()


def splash(ctx, x, y, t, s=1.0, col=WATER):
    if not 0 < t < 1:
        return
    rnd = random.Random(5)
    for k in range(18):
        a = -math.pi / 2 + rnd.uniform(-1.2, 1.2)
        v = rnd.uniform(300, 650) * s
        px = x + math.cos(a) * v * t
        py = y + math.sin(a) * v * t + 900 * s * t * t
        r = rnd.uniform(16, 34) * s * (1 - 0.5 * t)
        ellipse(ctx, px, py, r, r * 1.2); fl(ctx, col, 5)


def screen_splat(ctx, x, y, r, t, seed=1):
    """mud splat on the camera lens"""
    if t <= 0:
        return
    rnd = random.Random(seed)
    g = eout(min(1, t * 3))
    ctx.save(); ctx.translate(x, y); ctx.scale(g, g)
    ctx.new_path()
    for k in range(14):
        a = k / 14 * 2 * math.pi
        rr = r * (0.75 + 0.35 * rnd.random())
        ctx.line_to(math.cos(a) * rr, math.sin(a) * rr)
    ctx.close_path(); fl(ctx, MUD, 8)
    for k in range(7):
        a = rnd.uniform(0, 2 * math.pi); d = r * rnd.uniform(1.1, 1.6)
        ellipse(ctx, math.cos(a) * d, math.sin(a) * d, r * 0.12, r * 0.12); fl(ctx, MUD, 5)
    for k in range(3):
        dx = rnd.uniform(-r * 0.5, r * 0.5)
        rect_r(ctx, dx - 14, 0, 28, r * 0.8 + 160 * max(0, t - 0.3), 14); setc(ctx, MUD); ctx.fill()
    ellipse(ctx, -r * 0.3, -r * 0.3, r * 0.2, r * 0.12, -0.5); setc(ctx, (1, 1, 1, 0.35)); ctx.fill()
    ctx.restore()


def gps_bubble(ctx, x, y, t, txt="RECALCULATING...", s=1.0, a=0.0):
    if t <= 0:
        return
    sc = s * (0.5 + 0.5 * eout(min(1, t * 2)))
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(sc, sc)
    poly(ctx, [(-30, 50), (0, 50), (-50, 110)]); fl(ctx, (1, 1, 1), 6)
    rect_r(ctx, -270, -60, 540, 120, 40); fl(ctx, (1, 1, 1), 7)
    poly(ctx, [(-28, 44), (-2, 44), (-42, 96)]); setc(ctx, (1, 1, 1)); ctx.fill()
    text(ctx, txt, 0, 2, 54, RED, ow=0, shadow=False, maxw=500)
    ctx.restore()


def cow(ctx, x, gy, s, lf, lying=0.0, sleep=False):
    """original cartoon cow facing left"""
    ctx.save(); ctx.translate(x, gy); ctx.scale(s, s)
    ly = 95 * lying
    if lying < 1:
        for lx in (-110, -60, 70, 120):
            rect_r(ctx, lx - 18, -110 + ly, 36, 110 - ly * 0.9 + 1, 12); fl(ctx, (1, 1, 1), 6)
            rect_r(ctx, lx - 20, -22, 40, 22, 8); fl(ctx, hx('3a2a20'), 5)
    # tail
    ctx.new_path(); ctx.move_to(165, -190 + ly); ctx.curve_to(210, -160 + ly, 200, -110 + ly, 215 + 10 * math.sin(lf * 0.3), -90 + ly); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 216 + 10 * math.sin(lf * 0.3), -84 + ly, 14, 18); fl(ctx, INK, 3)
    ellipse(ctx, 10, -175 + ly, 180, 95); fl(ctx, (1, 1, 1), 8)
    ctx.save(); ellipse(ctx, 10, -175 + ly, 176, 91); ctx.clip()
    for px, py, r in ((-60, -220, 50), (80, -150, 60), (130, -240, 40), (-20, -120, 34)):
        ellipse(ctx, px, py + ly, r * 1.2, r); setc(ctx, hx('2a2026')); ctx.fill()
    ctx.restore()
    hy = -215 + ly * 1.05
    # ears + horns
    for ex, a in ((-250, -0.5), (-130, 0.5)):
        ellipse(ctx, ex, hy - 40, 34, 16, a); fl(ctx, (1, 1, 1), 5)
    for hx_ in (-215, -165):
        poly(ctx, [(hx_ - 10, hy - 60), (hx_ + 10, hy - 60), (hx_ + 4, hy - 100)]); fl(ctx, hx('fff0c8'), 5)
    ellipse(ctx, -190, hy, 80, 74); fl(ctx, (1, 1, 1), 7)
    ellipse(ctx, -205, hy + 45, 66, 42); fl(ctx, hx('ffaac0'), 6)
    for nx in (-228, -184):
        ellipse(ctx, nx, hy + 45, 9, 12); setc(ctx, hx('a03050')); ctx.fill()
    for ex in (-230, -160):
        if sleep:
            ink(ctx, 6); ctx.new_path(); ctx.arc(ex, hy - 14, 14, 0.2, math.pi - 0.2); ctx.stroke()
        else:
            ellipse(ctx, ex, hy - 14, 14, 18); fl(ctx, (1, 1, 1), 4)
            ellipse(ctx, ex - 4, hy - 12, 8, 10); setc(ctx, INK); ctx.fill()
            ink(ctx, 6); ctx.new_path(); ctx.move_to(ex - 18, hy - 40); ctx.line_to(ex + 14, hy - 36); ctx.stroke()  # flat unimpressed lids
    ctx.restore()


def car_side(ctx, x, gy, s, lf, spin=0.0, tilt=0.0, mud=0.0, dad_p=None, kid_p=None, chick=None, body=RED, seed=4):
    """side view, facing right. chick = (angle, faint) for a chicken on the roof"""
    ctx.save(); ctx.translate(x, gy); ctx.rotate(tilt); ctx.scale(s, s)
    cab = [(-200, -160), (-150, -300), (110, -300), (210, -160)]
    poly(ctx, cab); fl(ctx, body, 9)
    rw = [(-165, -170), (-132, -278), (-30, -278), (-30, -170)]
    fw = [(-6, -170), (-6, -278), (98, -278), (178, -170)]
    for wpts, who in ((rw, ('kid', -88, -212, 44)), (fw, ('dad', 62, -214, 52))):
        poly(ctx, wpts); setc(ctx, hx('bfe6ff')); ctx.fill()
        ctx.save(); poly(ctx, wpts); ctx.clip()
        kind, fx, fy, R = who
        if kind == 'kid':
            face(ctx, BOY, kid_p or P(eye='shock', mouth='open'), fx, fy + 10, R, 0, 1)
        else:
            face(ctx, DAD, dad_p or P(eye='happy', mouth='grin'), fx, fy + 10, R, 0, 1)
        poly(ctx, [(wpts[0][0] + 40, wpts[1][1]), (wpts[0][0] + 70, wpts[1][1]), (wpts[0][0] + 20, wpts[0][1]), (wpts[0][0] - 10, wpts[0][1])])
        setc(ctx, (1, 1, 1, 0.25)); ctx.fill()
        ctx.restore()
        poly(ctx, wpts); ink(ctx, 7); ctx.stroke()
    rect_r(ctx, -285, -180, 570, 135, 46); fl(ctx, body, 9)
    ctx.move_to(-20, -175); ctx.line_to(-20, -60); ink(ctx, 5); ctx.stroke()
    rect_r(ctx, 20, -150, 50, 14, 7); fl(ctx, dark(body, 0.7), 4)
    ellipse(ctx, 268, -130, 22, 26); fl(ctx, hx('fff6c8'), 5)
    rect_r(ctx, -292, -150, 22, 40, 8); fl(ctx, hx('ffcc33'), 4)
    # mud (clipped to the car)
    if mud > 0:
        ctx.save(); poly(ctx, cab); ctx.clip()
        mud_blobs(ctx, -230, -200, 460, 40, mud * 0.3, seed)
        ctx.restore()
        ctx.save(); rect_r(ctx, -285, -180, 570, 135, 46); ctx.clip()
        mud_blobs(ctx, -300, -190, 600, 150, mud * 0.7, seed + 1)
        ctx.restore()
        hay(ctx, 160, -175, 1.0, seed, int(6 * mud))
        hay(ctx, -200, -175, 0.9, seed + 3, int(5 * mud))
    for wx in (-165, 165):
        ellipse(ctx, wx, -50, 62, 62); fl(ctx, hx('2a2840'), 8)
        ellipse(ctx, wx, -50, 30, 30); fl(ctx, hx('c8c8d8'), 5)
        ink(ctx, 5)
        for k in range(3):
            a = spin + k * 2 * math.pi / 3
            ctx.move_to(wx, -50); ctx.line_to(wx + math.cos(a) * 28, -50 + math.sin(a) * 28)
        ctx.stroke()
        if mud > 0:
            ctx.save(); ellipse(ctx, wx, -50, 60, 60); ctx.clip()
            mud_blobs(ctx, wx - 60, -60, 120, 70, mud * 0.25, seed + wx)
            ctx.restore()
    if chick:
        chicken(ctx, 0, -350, 1.15, chick[0], chick[1], chick[2] if len(chick) > 2 else 0)
    ctx.restore()


# ------------------------------------------------------------------ backgrounds
def tree(ctx, x, y, s):
    rect_r(ctx, x - 14 * s, y - 120 * s, 28 * s, 120 * s, 8); fl(ctx, hx('8a5a2a'), 6)
    ellipse(ctx, x, y - 170 * s, 80 * s, 90 * s); fl(ctx, hx('3fbf4a'), 7)


def country(ctx, off, ground='dirt', river=None, tod=0.0):
    sky = hx('9fd8ff') if tod < 0.5 else hx('ffc28a')
    ctx.rectangle(-1500, -1500, 4500, 5000); setc(ctx, sky); ctx.fill()
    ellipse(ctx, 860, 560, 80, 80); setc(ctx, hx('fff27a')); ctx.fill()
    cloud(ctx, 200 - (off * 0.05) % 400, 560, 0.9); cloud(ctx, 760 - (off * 0.05) % 400, 640, 0.7)
    for k in range(-3, 8):
        hx_ = ((k * 520 - off * 0.25) % 4160) - 1200
        ellipse(ctx, hx_, GY - 120, 420, 260); fl(ctx, hx('8fdc6a') if k % 2 else hx('7ccf5c'), 7)
    for k in range(-3, 10):
        tx = ((k * 330 + 90 - off * 0.6) % 4290) - 1300
        tree(ctx, tx, GY - 60, 0.9 + 0.2 * (k % 2))
    ctx.rectangle(-1500, GY - 60, 4500, 60); setc(ctx, hx('6cc24a')); ctx.fill()
    if ground == 'dirt':
        ctx.rectangle(-1500, GY, 4500, 2000); setc(ctx, hx('c98a4a')); ctx.fill()
        ctx.move_to(-1500, GY); ctx.line_to(3000, GY); ink(ctx, 7); ctx.stroke()
        rnd = random.Random(8)
        for k in range(-6, 30):
            px = ((k * 170 + rnd.uniform(0, 80) - off) % 6120) - 1500
            ellipse(ctx, px, GY + 30 + (k % 3) * 40, 26, 14); fl(ctx, hx('a86a34'), 4)
            ellipse(ctx, px + 70, GY + 140 + (k % 4) * 30, 40, 12); setc(ctx, hx('b47a3e')); ctx.fill()
    elif ground == 'mud':
        ctx.rectangle(-1500, GY, 4500, 2000); setc(ctx, MUD2); ctx.fill()
        ctx.move_to(-1500, GY); ctx.line_to(3000, GY); ink(ctx, 7); ctx.stroke()
        rnd = random.Random(9)
        for k in range(30):
            ellipse(ctx, rnd.uniform(-600, 1700), GY + rnd.uniform(20, 500), rnd.uniform(40, 120), rnd.uniform(14, 30)); setc(ctx, MUD); ctx.fill()
    if river:
        x0, x1 = river
        ctx.new_path(); ctx.move_to(x0 - 40, GY - 20); ctx.curve_to(x0 + 60, GY + 380, x0 + 200, GY + 400, x0 + 300, GY + 400)
        ctx.line_to(x1, GY + 400); ctx.line_to(x1, GY - 20); ctx.close_path(); fl(ctx, WATER, 7)
        ctx.move_to(x0, GY - 20)
        for k in range(int((x1 - x0) / 60) + 1):
            ctx.line_to(x0 + k * 60 + 30, GY - 20 + 12 * math.sin(k + off * 0.1)); ctx.line_to(x0 + k * 60 + 60, GY - 20)
        ink(ctx, 6); ctx.stroke()
        for k in range(6):
            wx = x0 + 80 + k * (x1 - x0 - 160) / 5
            ctx.move_to(wx, GY + 60 + (k % 2) * 80); ctx.rel_line_to(70, 0)
        setc(ctx, (1, 1, 1, 0.6)); ctx.set_line_width(6); ctx.stroke()


def water_front(ctx, x0, x1, lf):
    """front water layer so the car looks submerged"""
    ctx.new_path(); ctx.move_to(x0, GY - 20)
    for k in range(int((x1 - x0) / 60) + 1):
        ctx.line_to(x0 + k * 60 + 30, GY - 20 + 14 * math.sin(k + lf * 0.3)); ctx.line_to(x0 + k * 60 + 60, GY - 20)
    ctx.line_to(x1, GY + 400); ctx.line_to(x0 + 300, GY + 400); ctx.curve_to(x0 + 200, GY + 400, x0 + 120, GY + 300, x0 + 40, GY - 20); ctx.close_path()
    setc(ctx, WATER + (0.82,)); ctx.fill_preserve(); ink(ctx, 6); ctx.stroke()


def party_house(ctx, lf):
    ctx.rectangle(-1500, -1500, 4500, 5000); setc(ctx, hx('9fd8ff')); ctx.fill()
    cloud(ctx, 220, 560, 0.9)
    ctx.rectangle(240, 720, 640, 560); fl(ctx, hx('ffd0e0'), 9)
    poly(ctx, [(200, 730), (560, 470), (920, 730)]); fl(ctx, hx('8a3cff'), 9)
    rect_r(ctx, 480, 1020, 140, 260, 16); fl(ctx, hx('ff8a1f'), 7)
    for wx in (300, 680):
        rect_r(ctx, wx, 820, 120, 110, 10); fl(ctx, hx('fff6c8'), 6)
    # bunting
    ctx.move_to(240, 740); ctx.curve_to(400, 800, 700, 800, 880, 740); ink(ctx, 4); ctx.stroke()
    for k in range(8):
        bx = 270 + k * 80; by = 755 + 35 * math.sin((k + 0.5) / 8 * math.pi)
        poly(ctx, [(bx - 22, by), (bx + 22, by), (bx, by + 40)]); fl(ctx, (PINK, YEL, BLUE, GREEN)[k % 4], 3)
    for k, (bx, col) in enumerate(((180, PINK), (130, YEL), (950, BLUE), (1000, GREEN))):
        by = 860 + 30 * k % 60 + 10 * math.sin(lf * 0.2 + k)
        ctx.move_to(bx, by + 70); ctx.line_to(bx + 10, GY - 30); ink(ctx, 3); ctx.stroke()
        ellipse(ctx, bx, by, 50, 62); fl(ctx, col, 6)
    ctx.rectangle(-1500, GY - 60, 4500, 2000); setc(ctx, hx('6cc24a')); ctx.fill()
    ctx.move_to(-1500, GY - 60); ctx.line_to(3000, GY - 60); ink(ctx, 7); ctx.stroke()


def flash(ctx, u):
    if 0 <= u < 1:
        ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.95 * (1 - u) ** 1.5)); ctx.fill()


# ------------------------------------------------------------------ opening
def opening_face(ctx, f, lf, lab=True):
    sh = shake_at(lf, [0], 10, 18) + 2
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 40)), 0, sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff9a3c')); ctx.fill()
    rays(ctx, 540, 980, 240, 1700, lf * 0.04, col=(1, 0.95, 0.5), a=0.5, n=18)
    cx, cy = 520, 1000 + 8 * math.sin(lf * 0.5)
    face(ctx, DAD, P(eye='happy', mouth='grin', head=0), cx, cy, 300, -0.06 + 0.03 * math.sin(lf * 0.4))
    # finger raised: "I know a shortcut!"
    fx, fy = 880, 1060 - 10 * math.sin(lf * 0.6)
    rect_r(ctx, fx - 22, fy - 150, 44, 120, 22); fl(ctx, DAD['skin'], 9)
    ellipse(ctx, fx, fy, 72, 66); fl(ctx, DAD['skin'], 9)
    rect_r(ctx, fx - 70, fy + 40, 140, 140, 20); fl(ctx, DAD['shirt'], 9)
    for k in range(3):
        sparkle(ctx, fx - 80 + 80 * k, fy - 230 - 25 * (k % 2), 30 + 8 * math.sin(lf * 0.6 + k))
    sparkle(ctx, 220, 760, 34 + 8 * math.sin(lf * 0.5))
    ctx.restore()
    if lab:
        label2(ctx, "\"I KNOW A", "SHORTCUT!\"", YEL, pop(lf, 0, 4) if lf > 0 else 1, 128, col2=(1, 1, 1))


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 45:
        opening_face(ctx, f, f)
    else:
        lf = f - 45
        turn = lf >= 35
        rot = -10 * eout(pop(lf, 35, 42)) if turn else 0
        ctx.save(); cam(ctx, 540, 1020, 1.05 + 0.05 * eout(pop(lf, 0, 35)), rot, shake_at(lf, [35], 12, 18), f)
        pd = P(eye='happy', mouth='grin', head=-4) if not turn else P(eye='glare', mouth='grin', head=-8)
        pm = P(eye='normal', mouth='flat', head=6) if not turn else P(eye='shock', mouth='scream', head=10)
        pk = P(eye='normal', mouth='smile') if not turn else P(eye='shock', mouth='scream')
        car_front(ctx, lf, lf * (6 if not turn else 30), [('back', BOY, pk, 540, 860, 75, 1), ('front', DAD, pd, 330, 900, 110, 1),
                                                          ('front', MOM, pm, 750, 905, 105, -1)], f)
        ctx.restore()
        if not turn:
            label2(ctx, "\"The GPS says", "10 minutes...\"", (1, 1, 1), pop(lf, 0, 4), 100)
        else:
            label(ctx, "\"TRUST ME!\" *SCREECH*", 540, LY + 40, 104, YEL, -0.03, pop(lf, 35, 39))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 60:
        # bouncing down the dirt "road"
        off = lf * 38
        bump = abs(math.sin(lf * 0.55)) * 40
        ctx.save(); cam(ctx, 540, 1080, 1.0, 0, 3 + shake_at(lf % 12, [0], 6, 6), f)
        country(ctx, off, 'dirt')
        # wooden sign whizzing past
        sx = 1200 - lf * 38
        rect_r(ctx, sx - 10, GY - 260, 20, 260, 6); fl(ctx, hx('8a5a2a'), 5)
        ctx.save(); ctx.translate(sx, GY - 280); ctx.rotate(-0.12)
        rect_r(ctx, -150, -50, 300, 100, 10); fl(ctx, hx('c98a4a'), 6)
        text(ctx, "SHORTCUT?", 0, 2, 50, hx('3a2420'), ow=0, shadow=False)
        ctx.restore()
        car_side(ctx, 520, GY - bump, 1.25, lf, spin=lf * 0.6, tilt=0.06 * math.sin(lf * 0.9),
                 dad_p=P(eye='happy', mouth='grin'), kid_p=P(eye='shock', mouth='scream' if (lf // 6) % 2 else 'open'))
        ctx.restore()
        gps_bubble(ctx, 600, 820, pop(lf, 8, 14), "RECALCULATING...", 1.0, -0.04 + 0.03 * math.sin(lf * 0.8))
        label(ctx, "*BUMP* *BUMP* *BUMP*", 540, LY + 40, 104, (1, 1, 1), 0.03 * math.sin(lf * 0.9), pop(lf, 0, 4))
    else:
        il = lf - 60
        honk = 35 <= il < 55
        lying = eout(pop(il, 55, 68))
        ctx.save(); cam(ctx, 600 + 40 * eout(pop(il, 0, 30)), 1100, 1.15 + 0.12 * eout(pop(il, 0, 80)), 0,
                        shake_at(il, [0, 35], 8, 12), f)
        country(ctx, 2280, 'dirt')
        car_side(ctx, 300, GY, 1.2, il, dad_p=P(eye='glare' if honk else 'normal', mouth='scream' if honk else 'flat'),
                 kid_p=P(eye='normal', mouth='flat'))
        cx_ = 1300 - 440 * eout(pop(il, 0, 14))
        cow(ctx, cx_, GY + 10, 1.05, il, lying, sleep=il >= 62)
        if honk:
            for k in range(3):
                ctx.new_path(); ctx.arc(660, 1150, 50 + k * 34 + (il % 6) * 6, -0.6, 0.6); ink(ctx, 7); ctx.stroke()
        if il >= 68:
            for k in range(3):
                zt = ((il - 68) * 0.05 + k * 0.33) % 1
                text(ctx, "z", 700 + 60 * zt + 20 * k, 940 - 160 * zt, 50 + 20 * k, (1, 1, 1), ow=8, shadow=False)
        ctx.restore()
        if il < 35:
            label(ctx, "\"MOOOO.\"", 540, LY + 40, 130, (1, 1, 1), -0.03, pop(il, 0, 4))
        elif il < 55:
            label(ctx, "*HONK! HONK!*", 540, LY + 40, 130, YEL, 0.04, pop(il, 35, 39))
        else:
            label(ctx, "\"...she'll move.\"", 540, LY + 40, 110, (1, 1, 1), -0.03, pop(il, 55, 59))
    card(ctx, 'p2', f, 112, 246)


def s3(ctx, f):
    lf = f - 250
    if lf < 60:
        RV = (620, 2400)
        if lf < 22:
            x = 120 + lf * 12
            ty = 0; tl = 0
        else:
            u = eout(pop(lf, 22, 34))
            x = 384 + 400 * u
            ty = 230 * u; tl = 0.2 * math.sin(u * math.pi)
        ctx.save(); cam(ctx, 560, 1080, 1.0, 0, shake_at(lf, [30], 14, 22), f)
        country(ctx, 900, 'dirt', river=RV)
        car_side(ctx, x, GY + ty, 1.2, lf, spin=lf * 0.4 if lf < 22 else 0, tilt=tl,
                 dad_p=P(eye='happy', mouth='grin'), kid_p=P(eye='shock', mouth='open'))
        if lf >= 30:
            water_front(ctx, 580, 1400, lf)
        splash(ctx, 780, GY - 60, pop(lf, 30, 56), 1.3)
        ctx.restore()
        if lf < 30:
            label(ctx, "\"It's SHALLOW!\"", 540, LY + 40, 120, (1, 1, 1), -0.03, pop(lf, 0, 4))
        else:
            label(ctx, "*SPLOOSH!*", 540, LY + 40, 150, hx('7ad0ff'), 0.04, pop(lf, 30, 33))
    else:
        il = lf - 60
        ctx.save(); cam(ctx, 540, 1000, 1.08 + 0.05 * eout(pop(il, 0, 70)), 2 * math.sin(il * 0.12), shake_at(il, [0], 10, 14), f)
        car_front(ctx, il, 0, [('back', BOY, P(eye='shock', mouth='open'), 540, 860, 75, 1),
                               ('front', DAD, P(eye='happy', mouth='grin', head=-4), 330, 900, 110, 1),
                               ('front', MOM, P(eye='glare', mouth='flat', head=6), 750, 905, 105, -1)], f, bounce=False)
        # everything under water from y~1010 down
        wl = 1010 + 10 * math.sin(il * 0.25)
        ctx.new_path(); ctx.move_to(-200, wl)
        for k in range(24):
            ctx.line_to(-200 + k * 60 + 30, wl + 12 * math.sin(k + il * 0.4)); ctx.line_to(-200 + k * 60 + 60, wl)
        ctx.line_to(1400, 2400); ctx.line_to(-200, 2400); ctx.close_path()
        setc(ctx, WATER + (0.62,)); ctx.fill_preserve(); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(7); ctx.stroke()
        fish(ctx, -150 + il * 16, 1120, 1.3, hx('ff8a1f'), 1, il * 0.6)
        fish(ctx, 1250 - il * 12, 1300, 1.0, hx('ffd23f'), -1, il * 0.7)
        fish(ctx, 1300 - (il - 30) * 20, 1050, 0.8, hx('ff5fa8'), -1, il * 0.8)
        bubbles(ctx, 330, 1230, il, 6, 3); bubbles(ctx, 760, 1260, il, 5, 7)
        ctx.restore()
        label(ctx, "\"Totally NORMAL.\"", 540, LY + 40, 116, (1, 1, 1), 0.03, pop(il, 0, 4))
    card(ctx, 'p3', f, 252, 386)


def s4(ctx, f):
    lf = f - 390
    if lf < 34:
        u = eout(pop(lf, 0, 14))
        ctx.save(); cam(ctx, 540, 1080, 1.05, 0, 4 + shake_at(lf, [10, 16], 12, 22), f)
        country(ctx, 0, 'mud')
        car_side(ctx, 100 + 420 * u, GY - 120 * math.sin(u * math.pi), 1.2, lf, spin=lf * 0.8, tilt=-0.2 * math.sin(u * math.pi),
                 mud=0.4 + 0.6 * u, dad_p=P(eye='happy', mouth='grin'), kid_p=P(eye='shock', mouth='scream'), seed=6)
        splash(ctx, 500, GY - 60, pop(lf, 6, 30), 1.3, MUD)
        ctx.restore()
        screen_splat(ctx, 300, 900, 210, pop(lf, 10, 20), 1)
        screen_splat(ctx, 800, 1150, 170, pop(lf, 14, 24), 2)
        screen_splat(ctx, 560, 660, 130, pop(lf, 18, 28), 3)
        label(ctx, "*SPLAT!*", 540, LY + 40, 160, hx('ffb070'), -0.05, pop(lf, 10, 13))
    else:
        il = lf - 34
        ctx.save(); cam(ctx, 540, 1150, 1.0 + 0.08 * eout(pop(il, 0, 60)), -5, shake_at(il, [0], 10, 14), f, sy=1000)
        party_house(ctx, il)
        car_side(ctx, 520, GY + 10, 1.35, il, mud=1.0, dad_p=P(eye='happy', mouth='grin', head=-6),
                 kid_p=P(eye='closed', mouth='wavy'), chick=(0.08 * math.sin(il * 0.5), False, abs(math.sin(il * 0.6))), seed=6)
        ctx.restore()
        for k in range(3):
            sparkle(ctx, 300 + 240 * k, 760 - 30 * (k % 2), 26 * eout(pop(il, 4 + 4 * k, 10 + 4 * k)))
        label(ctx, "\"SEE? WE MADE IT!\"", 540, LY + 40, 112, YEL, -0.03, pop(il, 0, 4))
    card(ctx, 'p4', f, 392, 496)


def muddy_face(ctx, cx, cy, R, seed=11):
    ctx.save(); ellipse(ctx, cx, cy - R * 0.05, R * 1.02, R * 0.92); ctx.clip()
    rnd = random.Random(seed)
    for k in range(9):
        a = rnd.uniform(0, 2 * math.pi); d = rnd.uniform(0.55, 0.95) * R
        if -1.2 < a - 1.57 < 1.2 and d < 0.7 * R:
            continue
        ellipse(ctx, cx + math.cos(a) * d, cy + math.sin(a) * d, R * rnd.uniform(0.1, 0.2), R * rnd.uniform(0.08, 0.15), a)
        setc(ctx, MUD + (0.9,)); ctx.fill()
    ctx.restore()


def s5(ctx, f):
    lf = f - 500
    if lf < 55:
        # split: spotless neighbours (top) vs muddy Dad (bottom)
        ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
        cam(ctx, 540, 640, 1.0 + 0.04 * eout(pop(lf, 0, 55)), 0, 0, f, sy=640)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('b6f0a0')); ctx.fill()
        rays(ctx, 540, 720, 160, 1200, lf * 0.03, col=(1, 1, 1), a=0.4, n=16)
        face(ctx, NEI, P(eye='happy', mouth='smile', head=0), 360, 740, 140, -0.05)
        face(ctx, NMOM, P(eye='happy', mouth='smile', head=0), 720, 745, 135, 0.05, -1)
        # lemonade
        for gx in (560, 900):
            rect_r(ctx, gx - 34, 800, 68, 110, 10); fl(ctx, hx('fff27a'), 6)
            ctx.move_to(gx + 10, 800); ctx.line_to(gx + 30, 740); setc(ctx, PINK); ctx.set_line_width(8); ctx.stroke()
        for k in range(4):
            sparkle(ctx, 160 + 260 * k, 590 + 40 * (k % 2), 22 + 6 * math.sin(lf * 0.5 + k))
        ctx.restore()
        ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
        cam(ctx, 540, 1250, 1.0 + 0.06 * eout(pop(lf, 0, 40)), 0, shake_at(lf, [22], 10, 16), f, sy=1250)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('c98a4a')); ctx.fill()
        rays(ctx, 540, 1250, 160, 1200, -lf * 0.02, col=(1, 0.9, 0.6), a=0.3, n=16)
        jaw = lf >= 22
        face(ctx, DAD, P(eye='shock' if jaw else 'happy', mouth='scream' if jaw else 'grin', head=0), 540, 1220, 190)
        muddy_face(ctx, 540, 1220, 190)
        hay(ctx, 420, 1040, 1.4, 3, 7)
        chicken(ctx, 600, 1000 - 30 * eout(pop(lf, 22, 28)), 1.1, 0.1 * math.sin(lf * 0.4), False, abs(math.sin(lf * 0.5)))
        ctx.restore()
        ctx.rectangle(0, 952, W, 16); setc(ctx, OUT); ctx.fill()
        label2(ctx, "\"Took the highway.", "8 minutes.\"", (1, 1, 1), pop(lf, 2, 6), 100, col2=YEL)
    elif lf < 95:
        il = lf - 55
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.1 * eout(pop(il, 0, 40)), 0, shake_at(il, [0], 10, 18), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff9a3c')); ctx.fill()
        rays(ctx, 540, 980, 240, 1700, il * 0.04, col=(1, 0.95, 0.5), a=0.5, n=18)
        face(ctx, DAD, P(eye='happy', mouth='grin', head=0), 520, 1000, 290, -0.06)
        muddy_face(ctx, 520, 1000, 290)
        chicken(ctx, 600, 690, 1.5, 0.1, False, abs(math.sin(il * 0.6)))
        fx, fy = 880, 1060
        rect_r(ctx, fx - 22, fy - 150, 44, 120, 22); fl(ctx, DAD['skin'], 9)
        ellipse(ctx, fx, fy, 72, 66); fl(ctx, DAD['skin'], 9)
        rect_r(ctx, fx - 70, fy + 40, 140, 140, 20); fl(ctx, DAD['shirt'], 9)
        mud_blobs(ctx, fx - 70, fy + 40, 140, 140, 0.4, 5)
        sparkle(ctx, fx, fy - 220, 30 * eout(pop(il, 6, 12)))
        ctx.restore()
        label2(ctx, "\"Going home?", "I know a SHORTCUT!\"", YEL, pop(il, 0, 4), 104, col2=(1, 1, 1))
    elif lf < 130:
        il = lf - 95
        for side, ch, x0, bg, fp in ((0, MOM, 0, hx('ff5fa8'), 1), (1, BOY, 540, hx('3aa8ff'), -1)):
            ctx.save(); ctx.rectangle(x0, 0, 540, H); ctx.clip()
            cam(ctx, x0 + 270, 1000, 1.0 + 0.08 * eout(pop(il, 0, 30)), 0, 8 + shake_at(il, [0], 10, 20), f + side * 7, sx=x0 + 270)
            ctx.rectangle(x0 - 600, -500, 1700, 3000); setc(ctx, bg); ctx.fill()
            rays(ctx, x0 + 270, 1000, 120, 1200, il * 0.08 * (1 if side else -1), col=(1, 1, 1), a=0.35, n=12)
            face(ctx, ch, P(eye='shock', mouth='scream', head=0), x0 + 270, 1000, 200, 0.05 * math.sin(il * 2.2 + side), fp)
            ctx.restore()
        ctx.rectangle(532, 0, 16, H); setc(ctx, OUT); ctx.fill()
        # the chicken faints across the middle
        u = eout(pop(il, 8, 20))
        chicken(ctx, 540, 760 + 380 * u, 1.3, 1.6 * u, il >= 8)
        label(ctx, "\"NOOOOO!!!\"", 540, LY + 40, 150, YEL, -0.04, pop(il, 0, 4))
    else:
        il = lf - 130
        opening_face(ctx, f, il)
    if lf < 128:
        card(ctx, 'p5', f, 502, 626)
    else:
        card(ctx, 'p1', f, 630)


SHOTS = [(0, s1), (110, s2), (250, s3), (390, s4), (500, s5)]
CUTS = (45, 110, 170, 250, 310, 390, 424, 500, 555, 595, 630)


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
                              "-i", "out/shortcut_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
