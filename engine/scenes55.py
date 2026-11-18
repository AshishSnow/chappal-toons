"""'I'm Holding On!' - original, general-audience comedy short, 23s.
Hook: ECU kid in a bike helmet mid-scream, wobbling: "DON'T LET GO!!" -> whip to sweaty Dad: "I'M HOLDING ON!"
Beat 1: side tracking shot, Dad jogs holding the seat... lets go, stops, keeps yelling "STILL HOLDING ON!" while waving.
Beat 2: kid "I'M DOING IT!!" -> looks back: Dad tiny in the distance -> "YOU LET GO?!" -> WOBBLE -> CRASH into a bush, legs up, wheel rolls away.
Beat 3: kid rises from the bush covered in leaves: "AGAIN." -> no-hands speed run, split screen wheelie / Dad crying proud tears.
Twist: Dad squeezes onto the tiny bike "MY TURN!", kid holds the seat "I'M HOLDING ON!"... lets go, Dad looks back,
Dad ECU "DON'T LET GOOO!!" -> CRASH -> cut back to the opening kid scream (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos, zigs
from scenes48 import label1, label2
import scenes13
from scenes13 import card as _card13
import random

BOY = dict(doodle.BOY, hood=False, shirt=hx('ffc93c'), pants=hx('3d7bff'))
DAD = dict(doodle.DAD, shirt=hx('22b4a0'), pants=hx('5a5f7a'))
N = 690
GY = 1330            # ground line in tracking shots
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
LEAF = hx('3ccf5a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
GOLD = hx('ffc83c')
TEAR = hx('5ac8ff')
HELM = hx('ff3b5c')

CAPS = {
    'p1': [[("TEACHING YOUR KID", OUT)], [("TO RIDE A BIKE", RED)]],
    'p2': [[("10 MINUTES", OUT)], [("LATER...", PURPLE)]],
    'p3': [[("DAD'S ", OUT), ("TURN", ORANGE)]],
}
scenes13.CAPS = CAPS
card = _card13

_DUMMY = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4))


# ------------------------------------------------------------------ props
def bike(ctx, x, gy, k, rot=0.0, col=RED):
    """side-view kid bike facing right; returns seat / bar / crank points"""
    r = 62 * k
    bx, fx = x - 105 * k, x + 105 * k
    wy = gy - r
    for wx in (bx, fx):
        wheel(ctx, wx, wy, r, rot, k)
    cx, cy = x - 10 * k, wy + 4 * k
    seat = (x - 40 * k, wy - 112 * k)
    bar = (fx - 20 * k, wy - 150 * k)
    hd = (bar[0] - 10 * k, wy - 110 * k)
    for a_, b_ in (((bx, wy), seat), (seat, (cx, cy)), ((cx, cy), (bx, wy)), (seat, hd), ((cx, cy), hd), (hd, (fx, wy)), (hd, bar)):
        ctx.move_to(*a_); ctx.line_to(*b_); setc(ctx, OUT); ctx.set_line_width(20 * k); ctx.stroke()
        ctx.move_to(*a_); ctx.line_to(*b_); setc(ctx, col); ctx.set_line_width(11 * k); ctx.stroke()
    rect_r(ctx, seat[0] - 34 * k, seat[1] - 12 * k, 68 * k, 22 * k, 10 * k); fl(ctx, hx('2a2a3a'), 5 * k)
    ctx.move_to(bar[0] - 30 * k, bar[1] + 6 * k); ctx.line_to(bar[0] + 12 * k, bar[1]); setc(ctx, OUT); ctx.set_line_width(20 * k); ctx.stroke()
    ctx.move_to(bar[0] - 30 * k, bar[1] + 6 * k); ctx.line_to(bar[0] - 4 * k, bar[1] + 2 * k); setc(ctx, hx('2a2a3a')); ctx.set_line_width(12 * k); ctx.stroke()
    ellipse(ctx, cx, cy, 18 * k, 18 * k); fl(ctx, hx('dddde8'), 4 * k)
    return dict(seat=seat, bar=bar, crank=(cx, cy))


def wheel(ctx, wx, wy, r, rot, k=1.0):
    ellipse(ctx, wx, wy, r, r); setc(ctx, OUT); ctx.set_line_width(16 * k); ctx.stroke()
    ellipse(ctx, wx, wy, r - 8 * k, r - 8 * k); setc(ctx, hx('3a3a4a')); ctx.set_line_width(9 * k); ctx.stroke()
    for s_ in range(4):
        a = rot + s_ * math.pi / 4
        ctx.move_to(wx - math.cos(a) * r * 0.85, wy - math.sin(a) * r * 0.85); ctx.line_to(wx + math.cos(a) * r * 0.85, wy + math.sin(a) * r * 0.85)
        setc(ctx, hx('c8c8d4')); ctx.set_line_width(3 * k); ctx.stroke()
    ellipse(ctx, wx, wy, 9 * k, 9 * k); fl(ctx, hx('dddde8'), 3 * k)


def helmet(ctx, x, y, R, a=0.0, s=1.0, leaves=False):
    """bike helmet dome over a head centred (x, y) of radius R"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, -0.28 * R, 1.14 * R, math.pi * 1.0, math.pi * 2.0)
    ctx.curve_to(1.14 * R, -0.12 * R, 0.9 * R, -0.18 * R, 0.6 * R, -0.22 * R)
    ctx.line_to(-0.6 * R, -0.22 * R); ctx.curve_to(-0.9 * R, -0.18 * R, -1.14 * R, -0.12 * R, -1.14 * R, -0.28 * R)
    ctx.close_path(); fl(ctx, HELM, max(4, R * 0.04))
    for k in (-0.45, 0.0, 0.45):   # vents
        ellipse(ctx, k * R, -0.95 * R + abs(k) * 0.25 * R, 0.1 * R, 0.2 * R); fl(ctx, hx('2a2a3a'), max(3, R * 0.025))
    ctx.new_path(); ctx.arc(0, -0.28 * R, 0.95 * R, math.pi * 1.15, math.pi * 1.45); setc(ctx, (1, 1, 1, 0.6)); ctx.set_line_width(R * 0.07); ctx.stroke()
    if leaves:
        for lx, ly, la in ((-0.7, -0.9, 0.5), (0.1, -1.38, -0.3), (0.6, -1.05, 1.0), (-0.2, -1.15, 2.0), (0.9, -0.5, 0.2)):
            leaf(ctx, lx * R, ly * R, R * 0.2, la)
    ctx.restore()


def leaf(ctx, x, y, r, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ctx.move_to(-r, 0); ctx.curve_to(-r * 0.4, -r * 0.7, r * 0.4, -r * 0.7, r, 0); ctx.curve_to(r * 0.4, r * 0.7, -r * 0.4, r * 0.7, -r, 0); ctx.close_path()
    fl(ctx, LEAF, max(2.5, r * 0.12))
    ctx.move_to(-r * 0.8, 0); ctx.line_to(r * 0.8, 0); setc(ctx, hx('1d8a3a')); ctx.set_line_width(max(2, r * 0.08)); ctx.stroke()
    ctx.restore()


def bush(ctx, x, gy, s=1.0, wob=0.0):
    ctx.save(); ctx.translate(x, gy); ctx.scale(s * (1 + 0.06 * wob), s * (1 - 0.05 * wob))
    for bx, by, r in ((-170, -90, 120), (170, -90, 120), (-90, -200, 140), (90, -200, 140), (0, -270, 140), (0, -100, 170)):
        ellipse(ctx, bx + 8 * wob * math.sin(bx), by, r, r); fl(ctx, GREEN, 9)
    for bx, by in ((-120, -230), (60, -300), (130, -150), (-40, -130)):
        ctx.new_path(); ctx.arc(bx, by, 40, math.pi * 1.1, math.pi * 1.7); setc(ctx, hx('6fe07f')); ctx.set_line_width(10); ctx.stroke()
    ctx.restore()


def leaf_burst(ctx, x, y, t, n=18, spread=520, seed=3):
    if not 0 < t < 1.4:
        return
    rnd = random.Random(seed)
    for i in range(n):
        a = rnd.uniform(-math.pi, 0.2)
        d = spread * eout(min(1, t)) * rnd.uniform(0.4, 1.0)
        leaf(ctx, x + math.cos(a) * d, y + math.sin(a) * d + 300 * t * t, rnd.uniform(18, 40), a + t * 6 * rnd.uniform(-1, 1))


def park(ctx, scroll, gy=GY, dark_=0.0):
    """side-on park, scrolled horizontally (parallax)"""
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('8fdcff')); ctx.fill()
    ellipse(ctx, 860, 560, 90, 90); setc(ctx, hx('fff2a0')); ctx.fill()
    for i in range(-2, 8):    # clouds
        cx_ = (i * 520 - scroll * 0.1) % 2600 - 600
        for dx, dy, r in ((0, 0, 60), (60, -20, 70), (120, 0, 55)):
            ellipse(ctx, cx_ + dx, 420 + (i % 3) * 120 + dy, r, r * 0.8); setc(ctx, (1, 1, 1)); ctx.fill()
    # hills
    off = -(scroll * 0.25) % 900
    ctx.move_to(-600, gy - 200)
    for i in range(-2, 6):
        x0 = off + i * 900 - 900
        ctx.curve_to(x0 + 200, gy - 480, x0 + 500, gy - 480, x0 + 900, gy - 200)
    ctx.line_to(1800, gy + 400); ctx.line_to(-600, gy + 400); ctx.close_path(); setc(ctx, hx('7fd36a')); ctx.fill()
    # trees
    for i in range(-2, 8):
        tx = (i * 380 - scroll * 0.6) % 2280 - 600
        ctx.rectangle(tx - 18, gy - 260, 36, 160); fl(ctx, hx('a8642e'), 6)
        ellipse(ctx, tx, gy - 320, 110, 120); fl(ctx, hx('2fbf5a'), 7)
        ellipse(ctx, tx - 40, gy - 360, 40, 30); setc(ctx, hx('6fe07f')); ctx.fill()
    # path
    ctx.rectangle(-600, gy - 60, 2400, 130); setc(ctx, hx('f0d9a8')); ctx.fill()
    ctx.move_to(-600, gy - 60); ctx.line_to(1800, gy - 60); ink(ctx, 6); ctx.stroke()
    ctx.move_to(-600, gy + 70); ctx.line_to(1800, gy + 70); ink(ctx, 6); ctx.stroke()
    ctx.rectangle(-600, gy + 70, 2400, 900); setc(ctx, hx('4cc45a')); ctx.fill()
    for i in range(-2, 14):   # path pebbles + grass tufts
        px = (i * 170 - scroll) % 2380 - 600
        ellipse(ctx, px, gy + 20, 14, 8); setc(ctx, hx('d4b980')); ctx.fill()
        gx = (i * 210 + 90 - scroll * 1.2) % 2940 - 600
        for d in (-14, 0, 14):
            ctx.move_to(gx + d, gy + 200); ctx.line_to(gx + d * 1.8, gy + 150); setc(ctx, hx('2f9a3f')); ctx.set_line_width(7); ctx.stroke()
    if dark_:
        ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, (0, 0, 0, dark_)); ctx.fill()


def speed_lines(ctx, lf, n=10, col=(1, 1, 1, 0.8), y0=500, y1=1300):
    rnd = random.Random(int(lf) // 2)
    for _ in range(n):
        y = rnd.uniform(y0, y1); x = rnd.uniform(-100, 1100); L = rnd.uniform(120, 320)
        ctx.move_to(x, y); ctx.line_to(x + L, y); setc(ctx, col); ctx.set_line_width(rnd.uniform(5, 10)); ctx.stroke()


def pedal_pose(ph, **kw):
    s = math.sin(ph)
    d = P(torso=10, lhip=40 + 18 * s, lkn=-60 - 25 * s, rhip=40 - 18 * s, rkn=-60 + 25 * s, lsh=70, lel=-10, rsh=70, rel=-10)
    d.update(kw); return d


def rider(ctx, x, gy, k, ch, pose, bk=1.1, roll=0.0, tilt=0.0, helm=True, helm_s=1.0, leaves=False):
    """kid bike + rider. tilt rotates everything round the contact point"""
    ctx.save(); ctx.translate(x, gy); ctx.rotate(tilt); ctx.translate(-x, -gy)
    b = bike(ctx, x, gy, bk, roll)
    d = draw_hip(ctx, b['seat'][0], b['seat'][1] - 10 * bk, k, 1, ch, pose)
    if helm:
        helmet(ctx, d['head'][0], d['head'][1], d['R'], math.radians(pose['torso'] + pose.get('head', 0)) * 1, helm_s, leaves)
    ctx.restore()
    return b, d


def hand_at(ctx, ch, k, f_, pose, hx_, hy_, gy):
    """draw a standing character so its front hand lands at (hx_, hy_)"""
    o = draw(_DUMMY, 0, gy - 186 * k, k, f_, ch, pose)
    return draw(ctx, hx_ - o['front'][0], gy - 186 * k, k, f_, ch, pose)


def tears(ctx, cx, cy, R, lf):
    for ex, ey, rx in eye_pos(cx, cy, R):
        for j in range(3):
            ph = ((lf * 0.06 + j / 3) % 1)
            sx = ex + (-1 if ex < cx else 1) * (R * 0.2 + ph * R * 0.9)
            sy = ey + R * 0.1 + ph * ph * R * 1.2
            ellipse(ctx, sx, sy, R * 0.07, R * 0.1); fl(ctx, TEAR, R * 0.02)
        ctx.move_to(ex, ey + R * 0.15); ctx.line_to(ex, ey + R * 0.9); setc(ctx, TEAR + (0.8,)); ctx.set_line_width(R * 0.07); ctx.stroke()


def sweat(ctx, x, y, s, lf, k=0):
    yy = y + ((lf * 4 + k * 23) % 50)
    ctx.move_to(x, yy - 30 * s); ctx.curve_to(x + 18 * s, yy, x + 14 * s, yy + 18 * s, x, yy + 18 * s); ctx.curve_to(x - 14 * s, yy + 18 * s, x - 18 * s, yy, x, yy - 30 * s)
    fl(ctx, TEAR, 4)


# ------------------------------------------------------------------ opening / ending faces
def kid_scream(ctx, f, lf):
    sh = 10 + 6 * math.sin(lf)
    ctx.save(); cam(ctx, 540, 960, 1.02 + 0.04 * eout(pop(lf, 0, 40)), 2 * math.sin(lf * 0.9), sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd23f')); ctx.fill()
    rays(ctx, 540, 900, 260, 1700, lf * 0.06, col=(1, 1, 1), a=0.45, n=18)
    cx, cy, R = 540, 930, 300
    rot = 0.12 * math.sin(lf * 0.7)
    face(ctx, BOY, P(eye='shock', mouth='scream', head=0), cx, cy, R, rot)
    helmet(ctx, cx, cy, R, rot)
    # white-knuckle grip on the handlebars at the bottom
    ctx.move_to(60, 1640); ctx.line_to(1020, 1620); setc(ctx, OUT); ctx.set_line_width(56); ctx.stroke(); ctx.move_to(60, 1640); ctx.line_to(1020, 1620); setc(ctx, hx('2a2a3a')); ctx.set_line_width(40); ctx.stroke()
    for hx_ in (230, 850):
        ellipse(ctx, hx_, 1630, 90, 70); fl(ctx, BOY['skin'], 8)
    for k in range(3):
        sweat(ctx, 200 + k * 320, 560 + (k % 2) * 80, 1.4, lf, k)
    ctx.restore()


def dad_holding(ctx, f, lf):
    ctx.save(); cam(ctx, 540, 960, 1.02 + 0.05 * eout(pop(lf, 0, 40)), 0, shake_at(lf, [0], 10, 16), f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('6fd0ff')); ctx.fill()
    speed_lines(ctx, lf, 14, (1, 1, 1, 0.7), 300, 1600)
    cx, cy, R = 520, 900 + 18 * abs(math.sin(lf * 0.5)), 290
    face(ctx, DAD, P(eye='happy', mouth='grin', head=0), cx, cy, R, 0.05 * math.sin(lf * 0.5))
    for k in range(4):
        sweat(ctx, 220 + k * 200, 560 + (k % 2) * 90, 1.3, lf, k)
    ctx.restore()


def dad_scream(ctx, f, lf):
    sh = 14 + 6 * math.sin(lf)
    ctx.save(); cam(ctx, 540, 960, 1.04, 3 * math.sin(lf * 1.1), sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8a5a')); ctx.fill()
    rays(ctx, 540, 900, 260, 1700, -lf * 0.08, col=(1, 1, 0.8), a=0.4, n=18)
    cx, cy, R = 540, 940, 300
    rot = -0.12 * math.sin(lf * 0.8)
    face(ctx, DAD, P(eye='shock', mouth='scream', head=0), cx, cy, R, rot)
    helmet(ctx, cx + 0.05 * R, cy - 0.55 * R, R, rot, 0.55)       # tiny borrowed helmet
    ctx.move_to(60, 1640); ctx.line_to(1020, 1620); setc(ctx, OUT); ctx.set_line_width(56); ctx.stroke(); ctx.move_to(60, 1640); ctx.line_to(1020, 1620); setc(ctx, hx('2a2a3a')); ctx.set_line_width(40); ctx.stroke()
    for hx_ in (230, 850):
        ellipse(ctx, hx_, 1630, 96, 76); fl(ctx, DAD['skin'], 8)
    for k in range(4):
        sweat(ctx, 180 + k * 240, 540 + (k % 2) * 80, 1.5, lf, k)
    # the bush rushing in
    if lf > 14:
        u = ein(pop(lf, 14, 30))
        bush(ctx, 1300 - 900 * u, 2100, 1.2 + 2.5 * u)
    ctx.restore()


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 38:
        kid_scream(ctx, f, f)
        label2(ctx, "\"DON'T", "LET GO!!\"", (1, 1, 1), 1.0 if f < 30 else 1.0, 124, col2=RED)
    else:
        lf = f - 38
        dad_holding(ctx, f, lf)
        label2(ctx, "\"I'M HOLDING", "ON! I GOT YOU!\"", (1, 1, 1), pop(lf, 1, 5), 100, col2=YEL)
    card(ctx, 'p1', f, -6, 72)


def s2(ctx, f):
    lf = f - 75
    scroll = lf * 14
    ctx.save(); cam(ctx, 540, 1000, 1.0, 0, 0, f)
    park(ctx, scroll)
    kx = 600
    wob = 0.06 * math.sin(lf * 0.5) * (1 - pop(lf, 70, 100))
    let = lf >= 48
    # Dad: jogs holding the seat, then lets go, stops and drifts out of frame left, still yelling + waving
    if not let:
        seat = (kx - 40 * 1.1, GY - 174 * 1.1)
        hand_at(ctx, DAD, 1.2, 1, run_pose(lf * 0.5, rsh=95, rel=-5, torso=18, eye='happy', mouth='grin'), seat[0] - 10, seat[1] + 10, GY + 10)
        b, d = rider(ctx, kx, GY, 1.0, BOY, pedal_pose(lf * 0.45, eye='shock', mouth='open'), roll=lf * 0.3, tilt=wob)
    else:
        dx = -14 * (lf - 48) - 6 * (lf - 48) ** 1.1
        wv = math.sin(lf * 0.8)
        draw(ctx, 340 + dx, GY + 10 - 186 * 1.2, 1.2, 1, DAD, P(rsh=-160 + 25 * wv, rel=-20 * wv, lsh=-20, eye='happy', mouth='grin'))
        happy = lf >= 88
        b, d = rider(ctx, kx, GY, 1.0, BOY, pedal_pose(lf * 0.45, eye='happy' if happy else 'shock', mouth='grin' if happy else 'open'), roll=lf * 0.3, tilt=wob)
    ctx.restore()
    if lf < 48:
        label1(ctx, "\"I GOT YOU! I GOT YOU!\"", (1, 1, 1), pop(lf, 2, 6), 86)
    elif lf < 86:
        label2(ctx, "*lets go*", "\"STILL HOLDING ON!\"", YEL, pop(lf, 49, 53), 90, col2=(1, 1, 1))
    else:
        label2(ctx, "\"I'M DOING IT!", "I'M DOING IT!!\"", (1, 1, 1), pop(lf, 87, 91), 100, col2=GREEN)


def s3(ctx, f):
    lf = f - 200
    if lf < 40:
        # over-the-shoulder look back: big kid face (right) looking back at tiny Dad far down the path
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eout(pop(lf, 16, 30)), 0, shake_at(lf, [16], 10, 18), f)
        park(ctx, 2000 + lf * 6, GY)
        draw(ctx, 170, GY + 10 - 186 * 0.38, 0.38, 1, DAD, P(rsh=-160 + 25 * math.sin(lf * 0.8), rel=-20 * math.sin(lf * 0.8), eye='happy', mouth='grin'))
        rect_r(ctx, 520, 1190, 700, 800, 140); fl(ctx, BOY['shirt'], 9)
        cx, cy, R = 760, 900, 320
        shock = lf >= 16
        face(ctx, BOY, P(eye='shock' if shock else 'happy', mouth='scream' if shock else 'grin', head=0), cx, cy, R, -0.05, f_=-1)
        helmet(ctx, cx, cy, R, -0.05)
        ctx.restore()
        if lf < 16:
            label1(ctx, "\"...DAD?\"", (1, 1, 1), pop(lf, 1, 4), 120, y=1440)
        else:
            label2(ctx, "\"YOU", "LET GO?!\"", (1, 1, 1), pop(lf, 16, 19), 124, col2=RED, y=1420)
    elif lf < 80:
        il = lf - 40
        # wobble wobble: bike swerves, kid flails, bush approaching
        ctx.save(); cam(ctx, 540, 1000, 1.0, 0, 0, f)
        park(ctx, 2600 + il * 12)
        tilt = 0.32 * math.sin(il * 0.55)
        p = pedal_pose(il * 0.8, eye='shock', mouth='scream', lsh=170 + 30 * math.sin(il * 1.3), lel=20, rsh=150 + 30 * math.sin(il * 1.1 + 1), rel=-20, torso=-5)
        rider(ctx, 500 + il * 2, GY, 1.0, BOY, p, roll=il * 0.3, tilt=tilt)
        bush(ctx, 1450 - il * 9, GY + 60, 1.0)
        for k in range(3):   # wobble arcs
            ctx.new_path(); ctx.arc(520, GY - 260, 260 + k * 40, math.pi * 1.15, math.pi * 1.35); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(8); ctx.stroke()
            ctx.new_path(); ctx.arc(520, GY - 260, 260 + k * 40, math.pi * 1.65, math.pi * 1.85); ctx.stroke()
        ctx.restore()
        label1(ctx, "*WOBBLE WOBBLE*", YEL, pop(il, 1, 4), 110)
    elif lf < 98:
        il = lf - 80
        # CRASH: kid plunges into the bush, leaves explode
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.08 * eout(pop(il, 0, 6)), 0, shake_at(il, [2], 16, 34), f)
        park(ctx, 3080)
        if il < 3:
            rider(ctx, 580 + il * 60, GY, 1.0, BOY, pedal_pose(0, eye='shock', mouth='scream', lsh=170, rsh=170), tilt=0.5)
        bush(ctx, 830, GY + 60, 1.0, 1.0 * math.sin(il * 1.4) * (1 - pop(il, 0, 18)))
        leaf_burst(ctx, 830, GY - 250, pop(il, 1, 18), 22, 620)
        ctx.restore()
        label1(ctx, "*CRASH!!*", (1, 1, 1), pop(il, 1, 4), 160, -0.06)
    else:
        il = lf - 98
        # legs sticking up out of the bush, kicking; the front wheel rolls away on its own
        ctx.save(); cam(ctx, 540, 1000, 1.0, 0, 0, f)
        park(ctx, 3080)
        for side, ph in ((-1, 0), (1, 1.6)):
            k_ = math.sin(il * 0.5 + ph) * 12
            hx_, hy_ = 800 + side * 30, GY - 300
            kx_, ky_ = hx_ + side * 30 + k_, hy_ - 120
            fx_, fy_ = kx_ + side * 10 - k_, ky_ - 110
            ctx.move_to(hx_, hy_); ctx.line_to(kx_, ky_); ctx.line_to(fx_, fy_); setc(ctx, OUT); ctx.set_line_width(62); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
            ctx.move_to(hx_, hy_); ctx.line_to(kx_, ky_); ctx.line_to(fx_, fy_); setc(ctx, BOY['pants']); ctx.set_line_width(48); ctx.stroke()
            ellipse(ctx, fx_ + side * 14, fy_ - 20, 26, 46, side * 0.3); fl(ctx, BOY['shoes'], 7)
        bush(ctx, 830, GY + 60, 1.0, 0.3 * math.sin(il * 0.9))
        wx = 300 + il * 22
        wheel(ctx, wx, GY - 68 + 6 * abs(math.sin(il * 0.6)), 68, il * 0.4, 1.1)
        ctx.restore()
        label1(ctx, "\"...I'm OKAY!\"", (1, 1, 1), pop(il, 2, 6), 110)


def s4(ctx, f):
    lf = f - 330
    if lf < 40:
        # kid rises from the bush, leaves everywhere, determined glare
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.08 * eout(pop(lf, 0, 40)), 0, shake_at(lf, [10], 10, 16), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff5a4a')); ctx.fill()
        rays(ctx, 540, 900, 240, 1700, lf * 0.05, col=(1, 0.85, 0.3), a=0.5, n=16)
        rise = eout(pop(lf, 0, 12))
        cx, cy, R = 540, 1300 - 420 * rise, 290
        face(ctx, BOY, P(eye='glare', mouth='flat', head=0), cx, cy, R, 0)
        helmet(ctx, cx, cy, R, -0.08, leaves=True)
        leaf(ctx, cx - 0.6 * R, cy + 0.55 * R, 40, 0.6)
        leaf(ctx, cx + 0.95 * R, cy + 0.1 * R, 34, 2.2)
        for bx in range(-300, 1500, 180):
            ellipse(ctx, bx, 1700, 170, 190); fl(ctx, GREEN, 9)
        ctx.restore()
        label1(ctx, "\"AGAIN.\"", (1, 1, 1), pop(lf, 10, 13), 150)
    elif lf < 95:
        il = lf - 40
        # no-hands speed run
        ctx.save(); cam(ctx, 540, 1000, 1.0, 0, 3 * math.sin(il * 2), f)
        park(ctx, 4000 + il * 44)
        speed_lines(ctx, il, 12)
        p = pedal_pose(il * 1.2, eye='happy', mouth='grin', lsh=165, lel=15, rsh=-165 + 330, rel=-15, torso=0)
        rider(ctx, 540, GY, 1.0, BOY, p, roll=il * 0.9)
        for k in range(6):
            ctx.move_to(300 - k * 30, GY - 60 - k * 40); ctx.line_to(150 - k * 60, GY - 60 - k * 40); setc(ctx, (1, 1, 1, 0.9)); ctx.set_line_width(9); ctx.stroke()
        ctx.restore()
        label2(ctx, "\"LOOK, DAD!", "NO HANDS!!\"", (1, 1, 1), pop(il, 3, 7), 108, col2=YEL)
        card(ctx, 'p2', f, 370, 400)
    else:
        il = lf - 95
        # split: low-angle wheelie (top) / Dad crying proud tears (bottom)
        ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
        ctx.rectangle(0, 0, W, 960); setc(ctx, hx('ffb3d9')); ctx.fill()
        rays(ctx, 540, 560, 100, 1200, il * 0.06, col=(1, 1, 1), a=0.5, n=16)
        ctx.rectangle(0, 900, W, 100); setc(ctx, hx('f0d9a8')); ctx.fill(); ctx.move_to(0, 900); ctx.line_to(W, 900); ink(ctx, 6); ctx.stroke()
        bx_ = 560 - 105 * 1.1
        ctx.save(); ctx.translate(bx_, 900); ctx.rotate(-0.33 - 0.05 * math.sin(il * 0.4)); ctx.translate(-bx_, -900)
        rider(ctx, 560, 900, 1.0, BOY, pedal_pose(il * 0.6, eye='happy', mouth='grin', torso=-8), roll=il * 0.4)
        ctx.restore()
        ctx.restore()
        ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
        ctx.rectangle(0, 960, W, 960); setc(ctx, hx('6fd0ff')); ctx.fill()
        cx, cy, R = 540, 1230, 240
        face(ctx, DAD, P(eye='closed', mouth='wavy', head=0), cx, cy, R, 0.03 * math.sin(il * 0.4))
        tears(ctx, cx, cy, R, il)
        ctx.restore()
        ctx.rectangle(0, 952, W, 16); setc(ctx, (1, 1, 1)); ctx.fill()
        label1(ctx, "*WHEEEELIE!*", YEL, pop(il, 1, 4), 92, y=305)
        label1(ctx, "\"*sniff* That's MY KID!\"", (1, 1, 1), pop(il, 12, 16), 84, y=1470)


def s5(ctx, f):
    lf = f - 480
    if lf < 50:
        # Dad squeezes onto the tiny bike, knees to his ears, wearing the tiny helmet
        ctx.save(); cam(ctx, 540, 1060, 1.12 + 0.05 * eout(pop(lf, 0, 50)), 0, shake_at(lf, [6], 12, 18), f)
        park(ctx, 900)
        squash = 0.08 * eout(pop(lf, 4, 10))
        b = bike(ctx, 600, GY, 1.1, 0)
        pd = P(torso=-8, lhip=155, lkn=-150, rhip=145, rkn=-140, lsh=85, lel=-10, rsh=85, rel=-10, eye='smug', mouth='grin', head=0)
        d = draw_hip(ctx, b['seat'][0], b['seat'][1] + 10 + 40 * squash, 1.15, 1, DAD, pd)
        helmet(ctx, d['head'][0] + 0.05 * d['R'], d['head'][1] - 0.6 * d['R'], d['R'], 0.1, 0.55)
        for k in range(3):   # creak lines under the seat
            ctx.move_to(b['seat'][0] - 60 + k * 50, b['seat'][1] + 40); ctx.line_to(b['seat'][0] - 40 + k * 50, b['seat'][1] + 70); setc(ctx, (1, 1, 1)); ctx.set_line_width(7); ctx.stroke()
        draw(ctx, 200, GY + 10 - 186 * 0.95, 0.95, 1, BOY, P(eye='shock', mouth='open', lsh=-30, rsh=60, rel=-90))
        ctx.restore()
        label1(ctx, "\"MY TURN!\"", (1, 1, 1), pop(lf, 2, 6), 130)
        card(ctx, 'p3', f, 480, 528)
    elif lf < 105:
        il = lf - 50
        # tracking: the kid jogs behind holding Dad's seat... lets go, stops, waves
        ctx.save(); cam(ctx, 540, 1000, 1.0, 0, 0, f)
        park(ctx, 5000 + il * 14)
        pd = P(torso=-8, lhip=155 + 10 * math.sin(il * 0.5), lkn=-150, rhip=145 - 10 * math.sin(il * 0.5), rkn=-140, lsh=85, lel=-10, rsh=85, rel=-10,
               eye='happy' if il < 40 else 'normal', mouth='grin' if il < 40 else 'open', head=0)
        let = il >= 26
        if let:
            dx = -16 * (il - 26) - 5 * (il - 26) ** 1.1
            wv = math.sin(il * 0.8)
            draw(ctx, 330 + dx, GY + 10 - 186 * 0.95, 0.95, 1, BOY, P(rsh=-160 + 25 * wv, rel=-20 * wv, eye='happy', mouth='grin'))
        ctx.save(); ctx.translate(640, GY); ctx.rotate(0.05 * math.sin(il * 0.6)); ctx.translate(-640, -GY)
        b = bike(ctx, 640, GY, 1.1, il * 0.3)
        d = draw_hip(ctx, b['seat'][0], b['seat'][1] + 14, 1.15, 1, DAD, pd)
        helmet(ctx, d['head'][0] + 0.05 * d['R'], d['head'][1] - 0.6 * d['R'], d['R'], 0.1, 0.55)
        ctx.restore()
        if not let:
            hand_at(ctx, BOY, 0.95, 1, run_pose(il * 0.6, rsh=80, rel=-10, torso=22, eye='smug', mouth='grin'), b['seat'][0] - 30, b['seat'][1] + 20, GY + 10)
        ctx.restore()
        if il < 26:
            label1(ctx, "\"I'M HOLDING ON!\"", (1, 1, 1), pop(il, 2, 6), 104)
        else:
            label1(ctx, "*lets go*", YEL, pop(il, 27, 30), 110)
    elif lf < 140:
        il = lf - 105
        # Dad looks back: tiny kid far away waving
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eout(pop(il, 12, 26)), 0, shake_at(il, [12], 10, 18), f)
        park(ctx, 6200 + il * 6, GY)
        draw(ctx, 170, GY + 10 - 186 * 0.32, 0.32, 1, BOY, P(rsh=-160 + 25 * math.sin(il * 0.8), rel=-20 * math.sin(il * 0.8), eye='happy', mouth='grin'))
        rect_r(ctx, 500, 1190, 720, 800, 140); fl(ctx, DAD['shirt'], 9)
        cx, cy, R = 760, 900, 320
        shock = il >= 12
        face(ctx, DAD, P(eye='shock' if shock else 'happy', mouth='scream' if shock else 'grin', head=0), cx, cy, R, -0.05, f_=-1)
        helmet(ctx, cx - 0.05 * R, cy - 0.58 * R, R, -0.1, 0.55)
        ctx.restore()
        if il < 12:
            label1(ctx, "\"...SON?\"", (1, 1, 1), pop(il, 1, 4), 120, y=1440)
        else:
            label2(ctx, "\"YOU", "LET GO?!\"", (1, 1, 1), pop(il, 12, 15), 124, col2=RED, y=1420)
    elif lf < 182:
        il = lf - 140
        dad_scream(ctx, f, il)
        if il < 30:
            label2(ctx, "\"DON'T", "LET GOOO!!\"", (1, 1, 1), pop(il, 1, 4), 124, col2=RED)
        else:
            # CRASH into the bush: green wipe + leaf burst
            u = pop(il, 30, 36)
            ctx.rectangle(0, 0, W, H); setc(ctx, GREEN + (0.9 * u,)); ctx.fill()
            leaf_burst(ctx, 540, 1100, pop(il, 30, 42), 30, 900, seed=9)
            label1(ctx, "*CRASH!!*", (1, 1, 1), pop(il, 30, 33), 170, 0.05, y=1000)
    else:
        il = lf - 182
        kid_scream(ctx, f, il)
        label2(ctx, "\"DON'T", "LET GO!!\"", (1, 1, 1), pop(il, 0, 3), 124, col2=RED)
        card(ctx, 'p1', f, 666)


SHOTS = [(0, s1), (75, s2), (200, s3), (330, s4), (480, s5)]
CUTS = (38, 75, 200, 240, 280, 298, 330, 370, 425, 480, 530, 585, 620, 662)


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
                              "-i", "out/bike_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
