"""'Snow Day: Fully Dressed... "I Need to PEE."' - original, general-audience comedy short, 22s.
Hook: Mom ECU, gritted teeth, sweating, yanking a stuck snowsuit zipper: "ALMOST... DONE...!"
Beat 1: hallway, Mom whirlwinds around the kid: 3 SOCKS, 2 SWEATERS, SNOWSUIT, BOOTS, SCARF, HAT, MITTENS
 -> kid swells into a round puffball with starfish arms. "DONE!!"
Beat 2: tiny voice "...Mom?" -> kid ECU squished in the hood: "I need to PEE." -> Mom ECU twitch "...NOW?!"
Beat 3: REWIND (clothes fly off), *FLUSH!* with Mom holding the clothes tower, FAST FORWARD (clothes fly back on).
Twist: door opens -> sunny, the snow has MELTED, snowman puddle. Mom: "...you're KIDDING."
 -> kid ECU: "Mom... I need to pee AGAIN." -> Mom ECU strain (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label1, label2
from scenes58 import sweat, twitch
import scenes13
from scenes13 import card as _card13
import random

MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'), pants=hx('3d5a9e'))
BOY = dict(doodle.BOY, hood=False, shades=False)
N = 660
FLOOR = 1450
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
GOLD = hx('ffc93c')
SKY = hx('7fd0ff')
WHITE = (1, 1, 1)
BROWN = hx('8a4a2c')

CAPS = {
    'p1': [[("SNOW DAY!", BLUE)], [("TIME TO GET DRESSED...", OUT)]],
    'p2': [[("45 MINUTES", OUT)], [("LATER...", ORANGE)]],
    'p3': [[("UNDO.", OUT)], [("EVERYTHING.", RED)]],
    'p4': [[("FINALLY...", OUT)], [("OUTSIDE!", GREEN)]],
}
scenes13.CAPS = CAPS
card = _card13

LAYERS = ["3 SOCKS", "2 SWEATERS", "SNOWSUIT", "BOOTS", "SCARF", "HAT", "MITTENS"]
LT = [64, 82, 100, 118, 136, 154, 172]


def head_at(ctx, ch, p, x, y, R, rot=0.0, f_=1):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    doodle.head(ctx, R, ch, p, f_, max(3.0, R * 0.04))
    ctx.restore()


def ghost(ctx, a, fn):
    ctx.push_group(); fn(); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)


# ------------------------------------------------------------------ props
def hat(ctx, x, y, R, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ctx.new_path(); ctx.arc(0, 0, R * 1.07, math.pi, 2 * math.pi); ctx.close_path(); fl(ctx, GOLD, max(4, R * 0.05))
    for k in range(5):
        ctx.move_to(-R * 0.8 + k * R * 0.4, -R * 0.1); ctx.line_to(-R * 0.6 + k * R * 0.3, -R * 0.85)
    setc(ctx, hx('e0a020')); ctx.set_line_width(R * 0.05); ctx.stroke()
    rect_r(ctx, -R * 1.12, -R * 0.22, R * 2.24, R * 0.32, R * 0.14); fl(ctx, RED, max(4, R * 0.05))
    ellipse(ctx, 0, -R * 1.17, R * 0.3, R * 0.28); fl(ctx, WHITE, max(4, R * 0.05))
    ctx.restore()


def scarf(ctx, x, y, R, a=0.0, tail=True):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    if tail:
        rect_r(ctx, R * 0.35, R * 0.1, R * 0.42, R * 1.1, R * 0.12); fl(ctx, RED, max(4, R * 0.05))
        for k in range(2):
            ctx.rectangle(R * 0.35, R * 0.45 + k * R * 0.35, R * 0.42, R * 0.12); setc(ctx, WHITE); ctx.fill()
    rect_r(ctx, -R * 1.02, -R * 0.26, R * 2.04, R * 0.56, R * 0.24); fl(ctx, RED, max(4, R * 0.05))
    for k in range(4):
        ctx.rectangle(-R * 0.75 + k * R * 0.45, -R * 0.24, R * 0.14, R * 0.52); setc(ctx, WHITE); ctx.fill()
    rect_r(ctx, -R * 1.02, -R * 0.26, R * 2.04, R * 0.56, R * 0.24); ink(ctx, max(4, R * 0.05)); ctx.stroke()
    ctx.restore()


def boot(ctx, x, y, s=1.0, a=0.0, f_=1):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s * f_, s)
    ctx.new_path(); ctx.move_to(-40, -110); ctx.line_to(30, -110); ctx.line_to(34, -30)
    ctx.curve_to(90, -30, 100, 0, 96, 22); ctx.line_to(-46, 22); ctx.close_path(); fl(ctx, BROWN, 7)
    rect_r(ctx, -50, -130, 92, 36, 16); fl(ctx, WHITE, 6)
    ctx.restore()


def mitten(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ellipse(ctx, -36, 4, 18, 26, -0.5); fl(ctx, RED, 6)
    ellipse(ctx, 0, 0, 36, 46); fl(ctx, RED, 6)
    ctx.rectangle(-30, 36, 60, 18); fl(ctx, WHITE, 5)
    ctx.restore()


def sock(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-22, -70); ctx.line_to(22, -70); ctx.line_to(22, 10); ctx.curve_to(70, 10, 74, 46, 40, 50)
    ctx.line_to(-12, 50); ctx.curve_to(-30, 50, -22, 30, -22, 10); ctx.close_path(); fl(ctx, WHITE, 6)
    ctx.rectangle(-22, -50, 44, 14); setc(ctx, BLUE); ctx.fill()
    ctx.restore()


def sweater(ctx, x, y, s=1.0, a=0.0, col=GREEN):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-60, -60), (-120, 10), (-90, 40), (-60, 10), (-60, 70), (60, 70), (60, 10), (90, 40), (120, 10), (60, -60)]); fl(ctx, col, 6)
    ctx.move_to(-50, 20); ctx.line_to(-25, 0); ctx.line_to(0, 20); ctx.line_to(25, 0); ctx.line_to(50, 20)
    setc(ctx, WHITE); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()


ITEMS = [sock, sock, sweater, sweater, boot, boot, None, None, mitten, mitten]


def draw_item(ctx, i, x, y, s, a):
    if i == 6:
        hat(ctx, x, y, 55 * s, a)
    elif i == 7:
        scarf(ctx, x, y, 55 * s, a)
    elif i == 3:
        sweater(ctx, x, y, s, a, col=PURPLE)
    else:
        ITEMS[i](ctx, x, y, s, a)


def flying_items(ctx, cx, cy, t, lf):
    """t: 0 = on the kid, 1 = flown far out"""
    rnd = random.Random(5)
    for i in range(10):
        ang = rnd.uniform(0, 2 * math.pi); dist = rnd.uniform(380, 640)
        d = dist * t
        x = cx + math.cos(ang) * d; y = cy + math.sin(ang) * d * 0.9
        if t > 0.02:
            draw_item(ctx, i, x, y, 0.9, ang + lf * 0.4 * (1 if i % 2 else -1))


# ------------------------------------------------------------------ kid in layers
def kid_ball(ctx, x, g, k, s=1.0, eye='normal', mouth='smile', lf=0, wob=0.0):
    k = clamp(k, 0, 7)
    ctx.save(); ctx.translate(x, g); ctx.scale(s, s); ctx.rotate(wob)
    bw = 105 + 27 * k; bh = 140 + 16 * k
    legh = 120 - 6 * k
    by = -legh - bh * 0.9
    suit = k >= 2.5
    bodycol = hx('9fd8ff') if k < 1.5 else (GREEN if k < 2.5 else BLUE)
    a_ = math.radians(18 + 8.5 * k)
    al = 150 + 10 * k; aw = 46 + 9 * k
    for sx in (-1, 1):
        sh = (sx * bw * 0.7, by - bh * 0.42)
        tip = (sh[0] + sx * math.sin(a_) * al, sh[1] + math.cos(a_) * al)
        ctx.move_to(*sh); ctx.line_to(*tip); ink(ctx, aw + 14); ctx.stroke()
        ctx.move_to(*sh); ctx.line_to(*tip); setc(ctx, bodycol); ctx.set_line_width(aw); ctx.stroke()
        if k >= 6.5:
            mitten(ctx, tip[0], tip[1] + 10, 0.9 + 0.04 * k, -sx * 0.4)
        else:
            ellipse(ctx, tip[0], tip[1], 30, 30); fl(ctx, BOY['skin'], 6)
    for sx in (-1, 1):
        lx = sx * bw * 0.36
        lwid = 56 + 6 * k
        rect_r(ctx, lx - lwid / 2, -legh - 30, lwid, legh + 20, 20); fl(ctx, bodycol if suit else hx('9fd8ff'), 7)
        if k >= 3.5:
            boot(ctx, lx, -2, 0.85 + 0.03 * k, 0, sx)
        else:
            ellipse(ctx, lx + sx * 14, -8, 46, 22); fl(ctx, WHITE if k >= 0.5 else BOY['skin'], 6)
    ellipse(ctx, 0, by, bw, bh); fl(ctx, bodycol, 8)
    if suit:
        for i in (-1, 0, 1):
            ctx.new_path(); ctx.move_to(-bw * 0.92, by + i * bh * 0.42 - bh * 0.05)
            ctx.curve_to(-bw * 0.3, by + i * bh * 0.42 + bh * 0.12, bw * 0.3, by + i * bh * 0.42 + bh * 0.12, bw * 0.92, by + i * bh * 0.42 - bh * 0.05)
            setc(ctx, hx('1468c8')); ctx.set_line_width(7); ctx.stroke()
        ctx.move_to(0, by - bh * 0.98); ctx.line_to(0, by + bh * 0.95); ink(ctx, 6); ctx.stroke()
        for j in range(10):
            yy = by - bh * 0.9 + j * bh * 0.19
            ctx.move_to(-8, yy); ctx.line_to(8, yy)
        setc(ctx, hx('c8ccd8')); ctx.set_line_width(5); ctx.stroke()
    elif k < 1.5:
        for (dx, dy) in ((-0.4, -0.3), (0.35, -0.5), (0.0, 0.1), (-0.5, 0.4), (0.45, 0.35)):
            ellipse(ctx, bw * dx, by + bh * dy, 14, 14); setc(ctx, WHITE); ctx.fill()
    else:
        ctx.move_to(-bw * 0.9, by);
        for j in range(8):
            ctx.line_to(-bw * 0.9 + (j + 0.5) * bw * 0.225, by + (-30 if j % 2 == 0 else 0));
        setc(ctx, WHITE); ctx.set_line_width(10); ctx.stroke()
    R = 105
    hy = by - bh - 60 + 8 * k
    if suit:
        ellipse(ctx, 0, hy + 4, R * 1.38, R * 1.36); fl(ctx, BLUE, 8)
        ellipse(ctx, 0, hy + 4, R * 1.14, R * 1.12); fl(ctx, hx('1468c8'), 5)
    head_at(ctx, BOY, P(eye=eye, mouth=mouth, head=0), 0, hy, R)
    if k >= 5.5:
        hat(ctx, 0, hy - R * 0.12, R)
    if k >= 4.5:
        scarf(ctx, 0, hy + R * 0.55, R)
    ctx.restore()
    return (x, g + hy * s), R * s


# ------------------------------------------------------------------ sets
def hallway(ctx, lf=0, tint=None):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('ffd9a8')); ctx.fill()
    for k in range(-20, 30):
        ctx.rectangle(k * 90, -3000, 30, 7000)
    setc(ctx, hx('ffcf96')); ctx.fill()
    # front door with snowy window
    rect_r(ctx, 860, 560, 320, 790, 20); fl(ctx, hx('2a9d8f'), 8)
    ctx.save(); rect_r(ctx, 900, 620, 150, 220, 18); ctx.clip()
    ctx.rectangle(880, 600, 200, 260); setc(ctx, hx('cfe8ff')); ctx.fill()
    rnd = random.Random(2)
    for k in range(18):
        sx_ = rnd.uniform(900, 1050); sy_ = (rnd.uniform(600, 860) + lf * rnd.uniform(2, 4)) % 240 + 610
        ellipse(ctx, sx_ + 6 * math.sin(lf * 0.1 + k), sy_, 7, 7); setc(ctx, WHITE); ctx.fill()
    ctx.restore()
    rect_r(ctx, 900, 620, 150, 220, 18); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 890, 1000, 20, 20); fl(ctx, GOLD, 5)
    # coat hooks
    rect_r(ctx, 20, 640, 260, 30, 12); fl(ctx, BROWN, 6)
    rect_r(ctx, 60, 670, 120, 300, 40); fl(ctx, RED, 7)
    rect_r(ctx, 190, 670, 70, 220, 30); fl(ctx, hx('ffc93c'), 7)
    # floor
    ctx.rectangle(-3000, FLOOR - 120, 7000, 3000); setc(ctx, hx('c98a52')); ctx.fill()
    for k in range(-10, 20):
        ctx.move_to(k * 160, FLOOR - 120); ctx.line_to(k * 160 - 80, FLOOR + 700)
    setc(ctx, hx('a86e3e')); ctx.set_line_width(5); ctx.stroke()
    ctx.move_to(-3000, FLOOR - 120); ctx.line_to(4000, FLOOR - 120); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 480, FLOOR - 30, 400, 70); fl(ctx, hx('ff6b8a'), 6)
    ellipse(ctx, 480, FLOOR - 30, 300, 46); setc(ctx, hx('ff9fb3')); ctx.fill()


def mom_body(ctx, x, lf, eye='glare', mouth='grin', fac=1, arms='busy', k=1.45, ground=FLOOR):
    w = math.sin(lf * 1.3)
    if arms == 'busy':
        p = P(eye=eye, mouth=mouth, rsh=110 + 40 * w, rel=-40, lsh=-100 - 40 * w, lel=-30, lhip=-20 * w, rhip=20 * w, torso=8 * fac, head=-4)
    elif arms == 'pant':
        p = P(eye=eye, mouth=mouth, rsh=20, rel=-10, lsh=-20, lel=-10, lhip=-10, rhip=10, torso=18, head=14)
    elif arms == 'hold':
        p = P(eye=eye, mouth=mouth, rsh=80, rel=-70, lsh=80, lel=-70, head=-4)
    else:
        p = P(eye=eye, mouth=mouth, rsh=20, rel=-10, lsh=-20, head=0)
    return draw(ctx, x, ground - 186 * k + 40, k, fac, MOM, p)


def speed_lines(ctx, cx, cy, lf, r0=330, r1=520, n=14, col=WHITE):
    for k in range(n):
        a = k * 2 * math.pi / n + lf * 0.35
        ctx.new_path(); ctx.arc(cx, cy, r0 + (k % 3) * 60, a, a + 0.7)
        setc(ctx, col + (0.8,)); ctx.set_line_width(12); ctx.stroke()


def whirl_scene(ctx, f, lf, k, mode='dress', z=1.0, shake=0, kid_eye='shock', kid_mouth='flat'):
    ctx.save(); cam(ctx, 520, 1060, z, 0, shake, f)
    hallway(ctx, lf)
    kc = (480, FLOOR - 340)
    speed_lines(ctx, kc[0], kc[1], lf * (1 if mode != 'rewind' else -1))
    for dt, a in ((4, 0.18), (2, 0.35), (0, 1.0)):
        ph = (lf - dt) * 0.55 * (1 if mode != 'rewind' else -1)
        mx = 480 + 380 * math.sin(ph)
        fac = 1 if math.cos(ph) > 0 else -1
        behind = math.cos(ph) < -0.3
        if behind:
            ghost(ctx, a, lambda mx=mx, fac=fac: mom_body(ctx, mx, lf, fac=fac, k=1.3, ground=FLOOR - 50))
    kid_ball(ctx, 480, FLOOR - 20, k, 0.9, kid_eye, kid_mouth, lf, 0.04 * math.sin(lf * 0.9))
    for dt, a in ((4, 0.18), (2, 0.35), (0, 1.0)):
        ph = (lf - dt) * 0.55 * (1 if mode != 'rewind' else -1)
        mx = 480 + 380 * math.sin(ph)
        fac = 1 if math.cos(ph) > 0 else -1
        if not math.cos(ph) < -0.3:
            ghost(ctx, a, lambda mx=mx, fac=fac: mom_body(ctx, mx, lf, fac=fac))
    ctx.restore()


def vhs(ctx, lf, col):
    ctx.rectangle(0, 0, W, H); setc(ctx, col + (0.16,)); ctx.fill()
    for y in range(0, H, 14):
        ctx.rectangle(0, y, W, 5)
    setc(ctx, (0, 0, 0, 0.08)); ctx.fill()
    yb = (lf * 37) % H
    ctx.rectangle(0, yb, W, 40); setc(ctx, (1, 1, 1, 0.18)); ctx.fill()


def tri_icon(ctx, x, y, s, back=True):
    d = -1 if back else 1
    for k in (0, 1):
        ox = x + (k - 0.5) * 64 * s * d
        poly(ctx, [(ox - 34 * s * d, y - 40 * s), (ox + 34 * s * d, y), (ox - 34 * s * d, y + 40 * s)]); fl(ctx, WHITE, 6)


# ------------------------------------------------------------------ close-ups
def mom_ecu(ctx, f, lf, bg, eye='glare', mouth='grin', shake=0, zip_=False, twitch_=True, z0=1.0, ray_col=(1, 1, 1)):
    ctx.save(); cam(ctx, 540, 960, z0, 0, shake, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    rays(ctx, 540, 900, 260, 1700, lf * 0.03, col=ray_col, a=0.35, n=18)
    cx, cy, R = 540, 860, 290
    jit = 6 * math.sin(lf * 2.7) if zip_ else 0
    face(ctx, MOM, P(eye=eye, mouth=mouth, head=0), cx + jit, cy, R, 0.02 * math.sin(lf * 0.9))
    if twitch_:
        twitch(ctx, cx + 0.55 * R, cy - 0.6 * R, lf, 1.3)
    sweat(ctx, cx - 1.0 * R, cy - 0.55 * R, lf, 1.4)
    sweat(ctx, cx + 1.02 * R, cy - 0.2 * R, lf + 40, 1.1)
    if zip_:
        # puffy snowsuit + stuck zipper in the foreground
        ellipse(ctx, 540, 1720, 620, 420); fl(ctx, BLUE, 9)
        for i in range(3):
            ctx.new_path(); ctx.arc(540, 1720 + i * 150, 600, math.pi * 1.15, math.pi * 1.85)
            setc(ctx, hx('1468c8')); ctx.set_line_width(9); ctx.stroke()
        ctx.move_to(540, 1320); ctx.line_to(540, 1920); ink(ctx, 8); ctx.stroke()
        zy = 1310 - 18 * abs(math.sin(lf * 1.4))
        for j in range(12):
            ctx.move_to(526, 1340 + j * 40); ctx.line_to(554, 1340 + j * 40)
        setc(ctx, hx('c8ccd8')); ctx.set_line_width(7); ctx.stroke()
        rect_r(ctx, 520, zy - 10, 40, 70, 10); fl(ctx, hx('c8ccd8'), 6)
        for sx in (-1, 1):
            ellipse(ctx, 540 + sx * 70 + jit, zy - 40, 92, 78); fl(ctx, MOM['skin'], 9)
            for j in range(3):
                ctx.move_to(540 + sx * 70 - 40 + j * 28 + jit, zy - 98); ctx.line_to(540 + sx * 70 - 44 + j * 28 + jit, zy - 70)
            ink(ctx, 5); ctx.stroke()
        for sx in (-1, 1):
            for j in range(3):
                a = -0.5 + j * 0.5
                ctx.move_to(540 + sx * (190 + j * 10), zy - 90 + j * 50); ctx.line_to(540 + sx * (250 + j * 20), zy - 110 + j * 60)
        ink(ctx, 8); ctx.stroke()
    ctx.restore()


def opening_face(ctx, f, lf, lab=True):
    mom_ecu(ctx, f, lf, hx('ffb02e'), shake=2 + shake_at(lf, [0], 8, 10), zip_=True, z0=1.02 + 0.05 * eout(pop(lf, 0, 50)))
    if lab:
        label1(ctx, "\"ALMOST... DONE...!\"", WHITE, pop(lf, 0, 4) if lf > 0 else 1, 112, -0.04, y=1480)
        label(ctx, "*ZZZT!*", 860, 1180, 70, YEL, 0.15, 1 if (lf // 6) % 2 == 0 else 0)


def kid_ecu(ctx, f, lf, bg, eye='shock', mouth='wavy', hot=False, shake=0):
    ctx.save(); cam(ctx, 540, 960, 1.02 + 0.06 * eout(pop(lf, 0, 40)), 0, shake, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    rays(ctx, 540, 960, 300, 1700, lf * 0.02, col=(1, 1, 1), a=0.3, n=16)
    cx, cy, R = 540, 930, 250
    ellipse(ctx, cx, cy + 600, 560, 420); fl(ctx, BLUE, 9)                 # puffy shoulders
    ellipse(ctx, cx, cy + 20, R * 1.5, R * 1.45); fl(ctx, BLUE, 9)          # hood
    ellipse(ctx, cx, cy + 20, R * 1.2, R * 1.2); fl(ctx, hx('1468c8'), 6)
    head_at(ctx, BOY, P(eye=eye, mouth=mouth, head=0), cx, cy, R, 0.03 * math.sin(lf * 0.5))
    for sx in (-1, 1):   # hood squishing the cheeks
        ellipse(ctx, cx + sx * 1.02 * R, cy + 0.35 * R, 0.3 * R, 0.45 * R); fl(ctx, BLUE, 8)
    hat(ctx, cx, cy - 0.12 * R, R)
    scarf(ctx, cx, cy + 0.95 * R, R, tail=False)
    if hot:
        sweat(ctx, cx - 0.8 * R, cy - 0.3 * R, lf, 1.2); sweat(ctx, cx + 0.85 * R, cy - 0.1 * R, lf + 30, 1.0)
        for k in range(3):
            xx = cx - 200 + k * 200
            ctx.move_to(xx, cy - 1.45 * R); ctx.curve_to(xx + 30, cy - 1.6 * R, xx - 30, cy - 1.75 * R, xx, cy - 1.9 * R - 10 * math.sin(lf * 0.3 + k))
        setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(12); ctx.stroke()
    ctx.restore()


# ------------------------------------------------------------------ outside
def yard(ctx, lf):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, SKY); ctx.fill()
    rays(ctx, 900, 330, 120, 900, lf * 0.02, col=(1, 0.97, 0.6), a=0.4, n=14)
    ellipse(ctx, 900, 330, 110, 110); fl(ctx, YEL, 7)
    # house front
    rect_r(ctx, -100, 520, 1280, 900, 0); fl(ctx, hx('ffb38a'), 8)
    for k in range(9):
        ctx.move_to(-100, 560 + k * 90); ctx.line_to(1180, 560 + k * 90)
    setc(ctx, hx('f0a078')); ctx.set_line_width(5); ctx.stroke()
    poly(ctx, [(-160, 560), (540, 380), (1240, 560)]); fl(ctx, hx('c8463a'), 8)
    # drips from the roof
    for k in range(6):
        dx = 60 + k * 190; dy = 560 + ((lf * 6 + k * 50) % 260)
        ellipse(ctx, dx, dy, 9, 14); setc(ctx, hx('5ac8ff')); ctx.fill()
    # open door
    rect_r(ctx, 230, 700, 520, 660, 20); fl(ctx, hx('5a3a2a'), 8)
    ctx.rectangle(200, 680, 30, 690); fl(ctx, hx('2a9d8f'), 6)
    # lawn, puddles
    ctx.rectangle(-3000, 1340, 7000, 3000); setc(ctx, hx('6fd86a')); ctx.fill()
    ctx.move_to(-3000, 1340); ctx.line_to(4000, 1340); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 220, 1440, 120, 26); fl(ctx, hx('9fdcff'), 5)


def melted_snowman(ctx, x, y, lf):
    ellipse(ctx, x, y, 170, 44); fl(ctx, hx('bfe8ff'), 6)
    ctx.new_path(); ctx.move_to(x - 70, y - 4); ctx.curve_to(x - 60, y - 70, x + 60, y - 70, x + 70, y - 4); ctx.close_path(); fl(ctx, WHITE, 6)
    for dx in (-30, 10, 40):
        ellipse(ctx, x + dx, y - 26 + (dx % 7), 9, 9); setc(ctx, INK); ctx.fill()
    poly(ctx, [(x - 10, y - 40), (x + 70, y - 30 + 3 * math.sin(lf * 0.2)), (x - 10, y - 22)]); fl(ctx, ORANGE, 5)
    ctx.save(); ctx.translate(x - 110, y - 6 + 4 * math.sin(lf * 0.15)); ctx.rotate(-0.4)
    rect_r(ctx, -40, -40, 80, 50, 6); fl(ctx, hx('2a2840'), 5); rect_r(ctx, -60, 6, 120, 16, 6); fl(ctx, hx('2a2840'), 5)
    ctx.restore()
    for sx in (-1, 1):
        ctx.move_to(x + sx * 90, y - 10); ctx.line_to(x + sx * 170, y - 40); ctx.line_to(x + sx * 190, y - 70)
    setc(ctx, BROWN); ctx.set_line_width(9); ctx.stroke()


def bird(ctx, x, y, lf):
    hop = abs(math.sin(lf * 0.4)) * 14
    ellipse(ctx, x, y - hop, 44, 36); fl(ctx, hx('ff6b3d'), 6)
    ellipse(ctx, x + 30, y - 30 - hop, 24, 22); fl(ctx, hx('ff6b3d'), 6)
    ellipse(ctx, x + 36, y - 34 - hop, 5, 5); setc(ctx, INK); ctx.fill()
    poly(ctx, [(x + 52, y - 32 - hop), (x + 72, y - 26 - hop), (x + 52, y - 20 - hop)]); fl(ctx, GOLD, 4)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    opening_face(ctx, f, f)
    card(ctx, 'p1', f, -6, 56)


def s2(ctx, f):
    lf = f - 60
    if f < 196:
        k = sum(eout(pop(f, t, t + 5)) for t in LT)
        hit = [t - 60 for t in LT]
        zoom = 1.0 + 0.04 * sum(1 for t in LT if t <= f < t + 4)
        whirl_scene(ctx, f, lf, k, z=zoom, shake=shake_at(lf, hit, 6, 12), kid_eye='shock', kid_mouth='flat' if k < 4.5 else 'smile')
        idx = max([i for i, t in enumerate(LT) if f >= t - 2] or [-1])
        if idx >= 0:
            t0 = LT[idx]
            ang = (-0.06, 0.05, -0.04, 0.06, -0.05, 0.04, -0.06)[idx]
            label(ctx, LAYERS[idx] + "!", 540, 470, 112, [WHITE, PURPLE, BLUE, ORANGE, RED, GOLD, RED][idx], ang, pop(f, t0 - 2, t0 + 2))
            puff(ctx, 480, 1100, pop(f, t0, t0 + 10), 1.5)
        else:
            label(ctx, "*WHOOSH!*", 540, 470, 110, WHITE, -0.05, pop(lf, 0, 4))
    else:
        il = f - 196
        ctx.save(); cam(ctx, 520, 1060, 1.05 + 0.04 * eout(pop(il, 0, 30)), 0, shake_at(il, [0], 10, 14), f)
        hallway(ctx, f)
        kid_ball(ctx, 560, FLOOR - 20, 7, 1.0, 'normal', 'smile', f)
        mom_body(ctx, 170, il, eye='closed', mouth='open', arms='pant', k=1.4)
        sweat(ctx, 150, 700, il, 1.2)
        ctx.restore()
        sparkle(ctx, 300, 860, 36 + 8 * math.sin(il * 0.6)); sparkle(ctx, 860, 760, 26)
        label1(ctx, "\"DONE!!\"", WHITE, pop(il, 2, 6), 150, -0.04, y=1500)
        card(ctx, 'p2', f, 198, 236)


def s3(ctx, f):
    lf = f - 240
    if lf < 26:
        ctx.save(); cam(ctx, 560, 1040, 1.12, 0, 0, f)
        hallway(ctx, f)
        kid_ball(ctx, 560, FLOOR - 20, 7, 1.0, 'shock', 'wavy', f)
        mom_body(ctx, 170, 0, eye='normal', mouth='flat', arms='idle', k=1.4)
        ctx.restore()
        label(ctx, "\"...Mom?\"", 640, 520, 84, WHITE, -0.04, pop(lf, 3, 7))
    elif lf < 62:
        il = lf - 26
        kid_ecu(ctx, f, il, hx('8fd8ff'), eye='shock', mouth='wavy')
        label2(ctx, "\"I need", "to PEE.\"", WHITE, pop(il, 3, 7), 130, col2=YEL, y=1460)
    else:
        il = lf - 62
        mom_ecu(ctx, f, il, hx('ff3b5c'), eye='shock', mouth='scream', shake=shake_at(il, [0], 14, 30), z0=1.0 + 0.18 * eout(pop(il, 0, 8)), ray_col=(1, 0.8, 0.6))
        label1(ctx, "\"...NOW?!\"", WHITE, pop(il, 2, 5), 160, -0.05, y=1480)


def s4(ctx, f):
    lf = f - 340
    if lf < 44:
        t = eout(pop(lf, 2, 40))
        whirl_scene(ctx, f, lf, 7 * (1 - t), mode='rewind', kid_eye='shock', kid_mouth='open')
        ctx.save(); flying_items(ctx, 480, 1040, eout(pop(lf, 0, 30)), lf); ctx.restore()
        vhs(ctx, lf, hx('3d5aff'))
        tri_icon(ctx, 540, 580, 1.0, back=True)
        label(ctx, "REWIND!", 540, 700, 120, WHITE, -0.04, pop(lf, 0, 4))
        card(ctx, 'p3', f, 342, 382)
    elif lf < 82:
        il = lf - 44
        sh = shake_at(il, [14], 12, 18)
        ctx.save(); cam(ctx, 540, 1060, 1.06, 0, sh, f)
        hallway(ctx, f)
        rect_r(ctx, 170, 640, 420, 820, 16); fl(ctx, hx('ffffff'), 8)
        ellipse(ctx, 540, 1060, 20, 20); fl(ctx, GOLD, 5)
        rect_r(ctx, 300, 720, 160, 110, 14); fl(ctx, hx('cfe8ff'), 6)
        ctx.new_path(); ctx.arc(380, 790, 26, math.pi, 2 * math.pi); ctx.close_path(); fl(ctx, WHITE, 5)   # tiny toilet sign
        rect_r(ctx, 356, 790, 48, 22, 8); fl(ctx, WHITE, 5)
        tap = max(0, math.sin(il * 1.4)) * 12
        b = mom_body(ctx, 810, il, eye='glare', mouth='frown', fac=-1, arms='hold', k=1.45)
        hx_, hy_ = b['head']
        cols = [BLUE, GREEN, PURPLE, RED, GOLD, WHITE, BROWN, RED]
        for j, c in enumerate(cols):
            rect_r(ctx, hx_ - 130 + (j % 2) * 16 - 8, hy_ + 520 - j * 62, 240, 64, 22); fl(ctx, c, 6)
        ctx.restore()
        if il < 14:
            label1(ctx, "\"HURRY!!\"", WHITE, pop(il, 1, 5), 120, -0.04, y=1500)
        else:
            label(ctx, "*FLUSH!*", 390, 560, 130, hx('5ac8ff'), -0.08, pop(il, 14, 18))
            for k in range(3):
                ctx.new_path(); ctx.arc(380, 1060, 80 + k * 50 + 30 * pop(il, 14, 30), il * 0.4 + k, il * 0.4 + k + 2.2)
                setc(ctx, hx('5ac8ff')); ctx.set_line_width(12); ctx.stroke()
    elif lf < 114:
        il = lf - 82
        t = eout(pop(il, 0, 26))
        whirl_scene(ctx, f, il, 7 * t, mode='dress', kid_eye='happy', kid_mouth='grin', shake=shake_at(il, [26], 8, 14))
        ctx.save(); flying_items(ctx, 480, 1040, 1 - eout(pop(il, 0, 22)), il); ctx.restore()
        vhs(ctx, il, hx('22b45a'))
        tri_icon(ctx, 540, 450, 1.0, back=False)
        label(ctx, "FAST FORWARD!", 540, 580, 112, YEL, -0.04, pop(il, 0, 4))
    else:
        il = lf - 114
        ctx.save(); cam(ctx, 540, 1100, 1.1, -3, shake_at(il, [0], 10, 16), f)
        hallway(ctx, f)
        kid_ball(ctx, 620, FLOOR - 20, 7, 1.0, 'happy', 'grin', f)
        b = draw(ctx, 340, FLOOR - 186 * 1.3 + 150, 1.3, 1, MOM, P(eye='closed', mouth='open', rot=-70, rsh=150, lsh=-150, lel=-40, rel=-40, lhip=-30, rhip=30))
        ctx.restore()
        label1(ctx, "\"DONE... AGAIN.\"", WHITE, pop(il, 2, 6), 120, -0.04, y=560)


def s5(ctx, f):
    lf = f - 476
    if lf < 60:
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(lf, 0, 60)), 0, 0, f)
        yard(ctx, lf)
        mom_body(ctx, 540, lf, eye='shock', mouth='open', arms='idle', fac=-1, k=1.3, ground=1400)
        kid_ball(ctx, 290, 1390, 7, 0.62, 'shock', 'flat', lf)
        melted_snowman(ctx, 790, 1385, lf)
        bird(ctx, 120, 1300, lf)
        ctx.restore()
        if lf < 22:
            card(ctx, 'p4', f, 478, 498)
            label(ctx, "*TWEET TWEET*", 300, 1200, 60, WHITE, -0.06, pop(lf, 6, 10))
        else:
            label1(ctx, "\"...it MELTED.\"", WHITE, pop(lf, 22, 26), 120, -0.04, y=1530)
    elif lf < 100:
        il = lf - 60
        mom_ecu(ctx, f, il, hx('ffd23f'), eye='glare', mouth='flat', shake=shake_at(il, [0], 8, 10), z0=1.0 + 0.08 * eout(pop(il, 0, 40)), ray_col=(1, 1, 1))
        label1(ctx, "\"...you're KIDDING.\"", WHITE, pop(il, 3, 7), 112, -0.04, y=1480)
    elif lf < 146:
        il = lf - 100
        kid_ecu(ctx, f, il, hx('ffb3d9'), eye='shock', mouth='wavy', hot=True, shake=shake_at(il, [0], 6, 8))
        label2(ctx, "\"Mom... I need", "to pee AGAIN.\"", WHITE, pop(il, 3, 7), 110, col2=YEL, y=1460)
    else:
        il = lf - 146
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 624)


SHOTS = [(0, s1), (60, s2), (240, s3), (340, s4), (476, s5)]
CUTS = (60, 196, 240, 266, 302, 340, 384, 422, 454, 476, 536, 576, 622)


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
                              "-i", "out/snow_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
