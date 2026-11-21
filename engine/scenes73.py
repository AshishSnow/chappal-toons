"""'Don't Wake the Baby' - original, general-audience comedy short, 22s.
Hook: Dad ECU sweating, finger on lips, caption "THE BABY IS / FINALLY ASLEEP..." + "SHHHHH!!"
Beat 1: dark hallway tiptoe -> *CREEEAK* -> Dad frozen on one leg -> crib ECU: the baby opens ONE eye... closes it.
        top-down floor map: red X creaky boards, Dad hops the safe boards to the kitchen.
Beat 2: microwave 0:03 -> 0:02 -> slow-mo Dad dive -> STOP at 0:01 *click*.
        split: courier's finger creeping to the doorbell / Dad sprinting -> door flies open: "SHHHHH!!" "...package?"
Twist:  Dad collapses on the sofa "Ahh... SILENCE." -> falls asleep -> *HONK-SHOOOO!!* chainsaw snore, frames tilt,
        Mom's tea flies -> crib: baby's eyes SNAP open -> *WAAAAH!!* tear fountains.
End:    split: baby screaming / Dad sleeping like a baby. Mom ECU glare "...YOUR turn." -> loop to the hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face, living, sofa_back, sofa_front, SEAT, zzz, bedroom
from scenes48 import label2, drool_bubble
from scenes58 import sweat, twitch, arm_to
from scenes8 import sit
from scenes13 import tiptoe
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


DAD = dict(doodle.DAD, shirt=hx('1f8bff'), pants=hx('2a3a6a'))
MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'), pants=hx('3d5a9e'))
COURIER = dict(doodle.NEIGHBOR, shirt=hx('ff8a1f'), pants=hx('5a3a2a'), tie=None, glasses=None, hair=hx('b8482e'))
N = 660
RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
BSKIN = hx('f6cfae')
FLOOR = 1460
DK = 1.45

CAPS = {'p1': [[("THE BABY IS", OUT)], [("FINALLY ASLEEP...", BLUE)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def finger_shh(ctx, cx, cy, R, skin):
    """index finger over the lips of a face at (cx, cy) radius R"""
    mx, my = cx + 0.06 * R, cy + 0.5 * R
    arm_to(ctx, cx + 0.2 * R, cy + 2.2 * R, mx + 0.02 * R, my + 0.32 * R, DAD['shirt'], skin, bend=-0.3 * R, w=0.42 * R)
    rect_r(ctx, mx - 0.07 * R, my - 0.42 * R, 0.14 * R, 0.62 * R, 0.07 * R); fl(ctx, skin, max(4, R * 0.022))
    ellipse(ctx, mx, my - 0.34 * R, 0.045 * R, 0.035 * R); setc(ctx, (1, 0.85, 0.85)); ctx.fill()


def baby(ctx, x, y, R, mood, lf):
    """baby head + blanket. mood: sleep | peek | awake | cry"""
    # blanket body
    rect_r(ctx, x - R * 1.35, y + R * 0.6, R * 2.7, R * 1.6, R * 0.5); fl(ctx, hx('9fd8ff'), R * 0.05)
    for k in range(5):
        sparkle(ctx, x - R * 0.9 + k * R * 0.45, y + R * 1.1 + (k % 2) * R * 0.4, R * 0.12, YEL)
    lw = max(4, R * 0.05)
    for ex in (-R * 0.95, R * 0.95):
        ellipse(ctx, x + ex, y + R * 0.1, R * 0.16, R * 0.2); fl(ctx, BSKIN, lw)
    ctx.new_path(); ctx.arc(x, y, R, 0, 2 * math.pi); fl(ctx, BSKIN, lw)
    # curl
    ctx.new_path(); ctx.arc(x + R * 0.08, y - R * 1.0, R * 0.14, math.pi * 0.2, math.pi * 1.9); ink(ctx, lw * 0.9); ctx.stroke()
    for bx in (-0.55, 0.55):
        ellipse(ctx, x + bx * R, y + 0.3 * R, R * 0.17, R * 0.1); setc(ctx, (1, 0.5, 0.55, 0.6 if mood != 'cry' else 0.95)); ctx.fill()
    ey = y - 0.05 * R
    for side, ex in ((-1, x - 0.36 * R), (1, x + 0.36 * R)):
        st = mood
        if mood == 'peek':
            st = 'sleep' if side < 0 else 'awake'
        if st == 'sleep':
            ctx.new_path(); ctx.arc(ex, ey - 0.04 * R, 0.13 * R, math.pi * 0.15, math.pi * 0.85); ink(ctx, lw); ctx.stroke()
        elif st == 'awake':
            ellipse(ctx, ex, ey, 0.17 * R, 0.2 * R); fl(ctx, WHITE, lw * 0.8)
            dx = 0.04 * R * math.sin(lf * 0.3) if mood == 'peek' else 0
            ellipse(ctx, ex + dx, ey + 0.02 * R, 0.08 * R, 0.1 * R); setc(ctx, INK); ctx.fill()
            ellipse(ctx, ex + dx - 0.03 * R, ey - 0.03 * R, 0.03 * R, 0.03 * R); setc(ctx, WHITE); ctx.fill()
        else:   # cry: squeezed > <
            ctx.move_to(ex - side * 0.15 * R, ey - 0.12 * R); ctx.line_to(ex + side * 0.12 * R, ey); ctx.line_to(ex - side * 0.15 * R, ey + 0.12 * R)
            ink(ctx, lw * 1.1); ctx.stroke()
    my = y + 0.45 * R
    if mood in ('sleep', 'peek'):
        # pacifier
        ellipse(ctx, x, my, 0.3 * R, 0.16 * R); fl(ctx, hx('7fe3ff'), lw * 0.8)
        ctx.new_path(); ctx.arc(x, my + 0.02 * R, 0.1 * R, 0, 2 * math.pi); setc(ctx, PINK); ctx.set_line_width(lw); ctx.stroke()
    elif mood == 'awake':
        ellipse(ctx, x, my, 0.08 * R, 0.1 * R); fl(ctx, hx('8a1c2c'), lw * 0.7)
    else:
        w = 0.36 * R * (1 + 0.08 * math.sin(lf * 1.7))
        ellipse(ctx, x, my + 0.08 * R, w, 0.3 * R); fl(ctx, hx('8a1c2c'), lw)
        ellipse(ctx, x, my + 0.24 * R, w * 0.6, 0.12 * R); setc(ctx, hx('ff6f86')); ctx.fill()
        # tear fountains
        for side in (-1, 1):
            for k in range(7):
                ph = ((lf * 0.06 + k / 7) % 1)
                tx = x + side * (0.45 * R + ph * 1.6 * R)
                ty = ey - 0.1 * R - math.sin(ph * math.pi) * 0.9 * R + ph * 0.8 * R
                ellipse(ctx, tx, ty, 0.07 * R, 0.09 * R); fl(ctx, CYAN, lw * 0.5)


def crib(ctx, x0, x1, top, bottom, front=True):
    if not front:
        rect_r(ctx, x0, top - 60, x1 - x0, bottom - top + 60, 30); fl(ctx, hx('ffe3a3'), 8)
        return
    ctx.rectangle(x0, top - 30, x1 - x0, 44); fl(ctx, hx('ffffff'), 8)
    n = 7
    for k in range(n):
        bx = x0 + 30 + k * (x1 - x0 - 60) / (n - 1)
        rect_r(ctx, bx - 14, top, 28, bottom - top, 12); fl(ctx, WHITE, 6)
    ctx.rectangle(x0, bottom - 30, x1 - x0, 50); fl(ctx, WHITE, 8)


def nursery_shot(ctx, f, lf, mood, z=1.0, shake=0, R=230, cy=1000, sy=H / 2):
    ctx.save(); cam(ctx, 540, cy, z, 0, shake, f, sy=sy)
    bedroom(ctx, lights=False, hh=2, mm=10)
    if mood == 'cry':
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, (1, 0.2, 0.3, 0.25)); ctx.fill()
        rays(ctx, 540, 1000, 200, 1500, lf * 0.05, col=(1, 0.9, 0.5), a=0.3, n=18)
    crib(ctx, 60, 1020, 1060, 1500, front=False)
    baby(ctx, 540, 960, R, mood, lf)
    crib(ctx, 60, 1020, 1060, 1500)
    ctx.restore()


def microwave(ctx, x, y, s, disp, lf, stopped=False):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rect_r(ctx, -400, -250, 800, 500, 40); fl(ctx, hx('d8dde8'), 10)
    rect_r(ctx, -360, -200, 500, 400, 26); fl(ctx, hx('2a2f45'), 8)
    # inside: spinning bowl
    ctx.save(); rect_r(ctx, -350, -190, 480, 380, 20); ctx.clip()
    ctx.rectangle(-360, -200, 500, 400); setc(ctx, (1, 0.85, 0.4, 0.35 if not stopped else 0.08)); ctx.fill()
    ellipse(ctx, -110, 140, 170, 30); fl(ctx, hx('f4f4f4'), 5)
    sw = 0 if stopped else math.sin(lf * 0.3)
    ellipse(ctx, -110 + 30 * sw, 90, 90, 55); fl(ctx, hx('ff8a1f'), 6)
    if not stopped:
        for k in range(3):
            yy = 20 - ((lf * 3 + k * 25) % 70)
            ctx.move_to(-150 + k * 40, 40 + yy); ctx.curve_to(-170 + k * 40, 10 + yy, -130 + k * 40, -10 + yy, -150 + k * 40, -40 + yy)
        setc(ctx, (1, 1, 1, 0.6)); ctx.set_line_width(7); ctx.stroke()
    ctx.restore()
    # panel
    rect_r(ctx, 190, -200, 180, 110, 14); fl(ctx, hx('0e1a12'), 6)
    text(ctx, disp, 280, -128, 74, hx('5dff7a'), ow=0, shadow=False)
    for k in range(6):
        rect_r(ctx, 205 + (k % 2) * 85, -60 + (k // 2) * 60, 66, 40, 10); fl(ctx, hx('f4f4f4'), 4)
    ctx.new_path(); ctx.arc(280, 170, 50, 0, 2 * math.pi); fl(ctx, RED, 6)
    text(ctx, "STOP", 280, 186, 32, WHITE, ow=0, shadow=False)
    ctx.restore()


def door_bell(ctx, x, y, s=1.0, lit=False):
    rect_r(ctx, x - 40 * s, y - 60 * s, 80 * s, 120 * s, 16 * s); fl(ctx, hx('c9ced8'), 5)
    ctx.new_path(); ctx.arc(x, y, 24 * s, 0, 2 * math.pi); fl(ctx, YEL if lit else WHITE, 5)


def parcel(ctx, x, y, s=1.0):
    rect_r(ctx, x - 90 * s, y - 70 * s, 180 * s, 140 * s, 8); fl(ctx, hx('c98a4a'), 6)
    ctx.rectangle(x - 18 * s, y - 70 * s, 36 * s, 140 * s); setc(ctx, hx('e8c27a')); ctx.fill()


def frame_pic(ctx, x, y, a, col):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    rect_r(ctx, -80, -100, 160, 200, 8); fl(ctx, hx('ffc93c'), 7)
    rect_r(ctx, -58, -78, 116, 156, 4); fl(ctx, col, 4)
    ctx.restore()


# ------------------------------------------------------------------ hook
def hook_face(ctx, f, lf):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eio(pop(lf, 0, 54)), 0, 2, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('23307a')); ctx.fill()
    rays(ctx, 540, 900, 260, 1500, lf * 0.02, col=(0.6, 0.75, 1), a=0.22, n=18)
    for k in range(12):
        rnd = random.Random(k)
        sparkle(ctx, rnd.uniform(60, 1020), rnd.uniform(560, 1500), 14 + 6 * math.sin(lf * 0.2 + k), hx('ffe98a'))
    cx, cy, R = 540, 900, 280
    face(ctx, DAD, P(eye='shock', mouth='flat'), cx, cy, R, 0.02 * math.sin(lf * 0.9))
    finger_shh(ctx, cx, cy, R, DAD['skin'])
    sweat(ctx, cx - 0.95 * R, cy - 60, lf, 1.3)
    sweat(ctx, cx + 1.0 * R, cy - 20, lf + 9, 1.1)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook_face(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"SHHHHHH!!\"", 540, 1420, 140, WHITE, -0.03, t)


# ------------------------------------------------------------------ beat 1
def hallway_night(ctx):
    ctx.rectangle(-2000, -2000, 5000, 5000); setc(ctx, hx('2b3570')); ctx.fill()
    for k in range(-8, 20):
        ctx.rectangle(k * 140, -2000, 60, 3500); setc(ctx, hx('27306a')); ctx.fill()
    frame_pic(ctx, 260, 700, -0.03, hx('7fe3ff'))
    frame_pic(ctx, 820, 660, 0.04, hx('ff9fc4'))
    # nursery door with a little moon sign
    rect_r(ctx, 880, 820, 260, 640, 10); fl(ctx, hx('3a2a50'), 8)
    ctx.rectangle(-2000, FLOOR, 5000, 2000); setc(ctx, hx('5a3a3a')); ctx.fill()
    for k in range(-10, 20):
        ctx.move_to(k * 150, FLOOR); ctx.line_to(k * 150, FLOOR + 600)
    setc(ctx, hx('442a2a')); ctx.set_line_width(6); ctx.stroke()
    ctx.move_to(-2000, FLOOR); ctx.line_to(3000, FLOOR); ink(ctx, 7); ctx.stroke()


def tiptoe_shot(ctx, f, lf):
    frozen = lf >= 30
    ctx.save(); cam(ctx, 540, 1150, 1.08, 0, shake_at(lf, [30], 10, 12), f)
    hallway_night(ctx)
    if not frozen:
        x = lerp(150, 520, lf / 30)
        draw(ctx, x, FLOOR - 186 * DK, DK, 1, DAD, tiptoe(lf * 0.45, eye='normal', mouth='flat'))
    else:
        x = 520
        # creaky board glows red
        ctx.rectangle(450, FLOOR, 150, 40); setc(ctx, (1, 0.2, 0.3, 0.7)); ctx.fill()
        for k in range(4):
            a = math.pi + k * 0.33 + 0.3
            ctx.move_to(525 + math.cos(a) * 90, FLOOR + 10 + math.sin(a) * 50); ctx.line_to(525 + math.cos(a) * 150, FLOOR + 10 + math.sin(a) * 90)
        setc(ctx, YEL); ctx.set_line_width(8); ctx.stroke()
        p = P(torso=4, lhip=70, lkn=-100, rhip=-4, rkn=0, lsh=150, lel=-30, rsh=-150, rel=30, eye='shock', mouth='wavy')
        draw(ctx, x, FLOOR - 186 * DK, DK, 1, DAD, p)
    ctx.restore()
    label(ctx, "*tip... tip... tip...*", 540, 560, 76, CYAN, -0.03, pop(lf, 2, 6) if lf < 30 else 0)
    if frozen:
        label(ctx, "*CREEEEAK*", 540, 560, 120, YEL, 0.04, pop(lf, 30, 33))
        sweat(ctx, 760, 820, lf, 1.2)


SAFE = [(540, 1420), (300, 1290), (560, 1160), (800, 1040), (560, 900), (330, 780), (540, 640)]


def floor_map(ctx, f, il):
    ctx.save(); cam(ctx, 540, 1000, 1.0, 0, 0, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('1d1f3a')); ctx.fill()
    ctx.rectangle(60, 520, 960, 1000); setc(ctx, hx('8a5a3a')); ctx.fill()
    rnd = random.Random(3)
    rows = 8
    for r in range(rows):
        y0 = 520 + r * 125
        ctx.move_to(60, y0); ctx.line_to(1020, y0)
        off = (r % 2) * 120
        for c in range(5):
            xx = 60 + off + c * 240
            ctx.move_to(xx, y0); ctx.line_to(xx, y0 + 125)
    setc(ctx, hx('5a3a2a')); ctx.set_line_width(6); ctx.stroke()
    # creaky boards
    for r in range(rows):
        for c in range(4 - (r % 2)):
            xx = 60 + (r % 2) * 120 + c * 240 + 120; yy = 520 + r * 125 + 62
            if not any(abs(xx - sx) < 160 and abs(yy - sy) < 70 for sx, sy in SAFE) and rnd.random() < 0.85:
                a = 0.5 + 0.3 * math.sin(il * 0.4 + r + c)
                ctx.move_to(xx - 40, yy - 34); ctx.line_to(xx + 40, yy + 34); ctx.move_to(xx + 40, yy - 34); ctx.line_to(xx - 40, yy + 34)
                setc(ctx, (1, 0.2, 0.3, a)); ctx.set_line_width(16); ctx.stroke()
    ctx.rectangle(60, 520, 960, 1000); ink(ctx, 12); ctx.stroke()
    # kitchen door at top
    rect_r(ctx, 420, 470, 240, 60, 10); fl(ctx, hx('5dff7a'), 6)
    # route so far
    seg = il / 8.0
    k = min(int(seg), len(SAFE) - 2); t = seg - k if seg < len(SAFE) - 1 else 1
    ctx.new_path(); ctx.move_to(*SAFE[0])
    for j in range(1, k + 1):
        ctx.line_to(*SAFE[j])
    x = lerp(SAFE[k][0], SAFE[k + 1][0], eio(t)); y = lerp(SAFE[k][1], SAFE[k + 1][1], eio(t))
    ctx.line_to(x, y)
    ctx.set_dash([24, 22]); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(10); ctx.stroke(); ctx.set_dash([])
    hop = math.sin(math.pi * t)
    ellipse(ctx, x, y + 20, 70 - 20 * hop, 26 - 8 * hop); setc(ctx, (0, 0, 0, 0.35)); ctx.fill()
    face(ctx, DAD, P(eye='shock', mouth='flat'), x, y - 30 - 90 * hop, 95 + 25 * hop, 0.2 * math.sin(il * 0.5))
    ctx.restore()


def s2(ctx, f):
    lf = f - 54
    if lf < 60:
        tiptoe_shot(ctx, f, lf)
    elif lf < 92:
        il = lf - 60
        mood = 'peek' if 8 <= il < 24 else 'sleep'
        nursery_shot(ctx, f, il, mood, 1.0 + 0.12 * eout(pop(il, 0, 10)))
        if mood == 'peek':
            label(ctx, "\"...?\"", 540, 430, 130, WHITE, 0.04, pop(il, 8, 11))
        elif il >= 24:
            label(ctx, "*phew...*", 540, 430, 100, CYAN, -0.03, pop(il, 24, 27))
    else:
        il = lf - 92   # 0..54
        floor_map(ctx, f, il)
        label(ctx, "MISSION: KITCHEN", 540, 330, 92, hx('5dff7a'), -0.02, pop(il, 0, 4))
        label(ctx, "*hop! hop! hop!*", 540, 1600 - 140, 80, WHITE, 0.03, pop(il, 6, 10))


# ------------------------------------------------------------------ beat 2
def mw_shot(ctx, f, il):
    # il 0..70
    if il < 16:
        disp = "0:03"
    elif il < 46:
        disp = "0:02" if il < 40 else "0:01"
    else:
        disp = "0:01"
    stopped = il >= 46
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eio(pop(il, 0, 46)), 0, shake_at(il, [46], 10, 16), f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb347') if il < 16 else hx('ff7a5a')); ctx.fill()
    for k in range(-6, 14):
        ctx.rectangle(k * 140, -500, 60, 3000); setc(ctx, (1, 1, 1, 0.08)); ctx.fill()
    ctx.rectangle(-500, 1240, 2200, 600); setc(ctx, hx('c98a4a')); ctx.fill()
    ctx.move_to(-500, 1240); ctx.line_to(1700, 1240); ink(ctx, 8); ctx.stroke()
    microwave(ctx, 540, 1000, 1.0, disp, il, stopped)
    # Dad dives in slow motion from the left
    if 16 <= il < 52:
        t = eout(pop(il, 16, 46))
        x = lerp(-260, 700, t)
        y = 760 - 60 * math.sin(math.pi * t)
        ctx.save(); ctx.translate(x, y); ctx.rotate(-1.35)
        draw(ctx, 0, -186 * 1.3, 1.3, 1, DAD, P(torso=0, lsh=175, rsh=170, lel=0, rel=0, lhip=-10, rhip=10, eye='shock', mouth='scream'))
        ctx.restore()
        for k in range(5):
            ctx.move_to(x - 260 - k * 30, y - 120 + k * 50); ctx.line_to(x - 520 - k * 30, y - 120 + k * 50)
        setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(8); ctx.stroke()
    if stopped:
        ctx.new_path(); ctx.arc(820, 1170, 70, 0, 2 * math.pi); setc(ctx, (1, 1, 1, 0.5)); ctx.fill()
        arm_to(ctx, 1200, 1500, 830, 1180, DAD['shirt'], DAD['skin'], bend=-60, w=90)
    ctx.restore()
    if il < 16:
        label(ctx, "*hmmmmmmm*", 540, 560, 90, WHITE, -0.03, pop(il, 0, 4))
    elif il < 46:
        label(ctx, "*S L O W - M O*", 540, 420, 72, WHITE, 0.0, pop(il, 16, 20))
        label(ctx, "\"NOOOOOOO...\"", 540, 1450, 110, YEL, -0.03, pop(il, 18, 22))
    else:
        label(ctx, "*click.*", 540, 560, 110, WHITE, 0.04, pop(il, 46, 49))
        label(ctx, "\"...phew.\"", 540, 1450, 120, GREEN, -0.03, pop(il, 52, 56))


def door_split(ctx, f, il):
    # top: courier's finger to the bell. bottom: Dad sprinting
    t = pop(il, 0, 34)
    ctx.save(); ctx.rectangle(0, 0, W, H / 2); ctx.clip()
    ctx.save(); cam(ctx, 540, 600, 1.0, 0, 0, f, sy=480)
    ctx.rectangle(-500, -500, 2200, 2000); setc(ctx, hx('6fd6c8')); ctx.fill()
    ctx.rectangle(-500, 260, 640, 900); fl(ctx, hx('c96a2a'), 8)
    door_bell(ctx, 260, 560, 1.6, lit=False)
    fx = lerp(1100, 330, eio(t) * 0.92)
    arm_to(ctx, 1300, 700, fx, 560, COURIER['shirt'], COURIER['skin'], bend=40, w=110)
    rect_r(ctx, fx - 110, 540, 120, 44, 20); fl(ctx, COURIER['skin'], 6)
    ctx.restore(); ctx.restore()
    ctx.save(); ctx.rectangle(0, H / 2, W, H / 2); ctx.clip()
    ctx.save(); cam(ctx, 540, 1150, 0.9, 0, 4, f, sy=1450)
    hallway_night(ctx)
    for k in range(8):
        yy = 900 + k * 70
        xx = (k * 230 + il * 90) % 1400 - 200
        ctx.move_to(xx, yy); ctx.line_to(xx - 260, yy)
    setc(ctx, (1, 1, 1, 0.6)); ctx.set_line_width(8); ctx.stroke()
    draw(ctx, 540, FLOOR - 186 * DK, DK, 1, DAD, run_pose(il * 1.4, eye='shock', mouth='scream', torso=24))
    ctx.restore(); ctx.restore()
    ctx.rectangle(0, H / 2 - 8, W, 16); setc(ctx, OUT); ctx.fill()
    label(ctx, "DING-DONG IN 3...", 540, 330, 74, YEL, -0.03, pop(il, 0, 4))
    label(ctx, "\"NO NO NO NO!!\"", 540, 1450, 100, WHITE, 0.03, pop(il, 4, 8))


def door_open(ctx, f, il):
    ctx.save(); cam(ctx, 540, 1060, 1.06, 0, shake_at(il, [0], 10, 18), f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('8fd8ff')); ctx.fill()
    ctx.rectangle(-500, FLOOR, 2200, 800); setc(ctx, hx('7ac46a')); ctx.fill()
    ctx.move_to(-500, FLOOR); ctx.line_to(1700, FLOOR); ink(ctx, 7); ctx.stroke()
    # door frame on the left with Dad inside
    rect_r(ctx, 40, 520, 470, 960, 10); fl(ctx, hx('2b3570'), 10)
    door_bell(ctx, 580, 900, 1.2)
    b = draw(ctx, 270, FLOOR - 186 * DK, DK, 1, DAD, P(eye='glare', mouth='flat', lsh=20))
    finger_shh(ctx, b['head'][0], b['head'][1], b['R'], DAD['skin'])
    draw(ctx, 820, FLOOR - 186 * 1.35, 1.35, -1, COURIER, P(eye='shock', mouth='flat', lsh=-100, lel=0, rsh=20))
    parcel(ctx, 800, 1180, 1.1)
    ctx.restore()
    label(ctx, "\"SHHHHHHH!!\"", 540, 560, 130, WHITE, -0.04, pop(il, 0, 3))
    if il >= 16:
        label(ctx, "\"...package?\"", 540, 1470, 90, CYAN, 0.03, pop(il, 16, 19))


def s3(ctx, f):
    lf = f - 200
    if lf < 72:
        mw_shot(ctx, f, lf)
    elif lf < 108:
        door_split(ctx, f, lf - 72)
    else:
        door_open(ctx, f, lf - 108)


# ------------------------------------------------------------------ twist
def sofa_scene(ctx, f, il, snore=0.0, mom_shock=False):
    ctx.save(); cam(ctx, 500, 1120, 0.96 + 0.04 * eio(pop(il, 0, 60)), 0, 26 * snore if snore > 0 else 0, f)
    living(ctx, lights=False)
    tilt = 0.25 * snore
    frame_pic(ctx, 260, 640, -0.03 - tilt, hx('7fe3ff'))
    frame_pic(ctx, 560, 600, 0.03 + tilt, hx('ff9fc4'))
    sofa_back(ctx)
    asleep = snore > 0 or il >= 40
    p = sit(torso=-14, head=-22 + 4 * math.sin(il * 0.12), eye='closed' if asleep else 'happy', mouth='open' if asleep else 'smile',
            lsh=20, lel=-60, rsh=50, rel=-80)
    b = draw_hip(ctx, 360, SEAT, 1.5, 1, DAD, p)
    sofa_front(ctx)
    # Mom tiptoes in with tea
    mx = lerp(1050, 760, eout(pop(il, 0, 30))) if not mom_shock else 760
    draw(ctx, mx, FLOOR - 186 * 1.35, 1.35, -1, MOM, P(eye='shock' if mom_shock else 'happy', mouth='open' if mom_shock else 'smile',
                                                     lsh=-60, lel=-60, rsh=-140 if mom_shock else 20, rel=-30))
    if not mom_shock:
        rect_r(ctx, mx + 70, 1060, 60, 70, 10); fl(ctx, WHITE, 5)
    if asleep and snore == 0:
        zzz(ctx, 520, 860, il, 1.0)
    if snore > 0:
        for k in range(4):
            r = 120 + ((il * 30 + k * 160) % 640)
            ctx.new_path(); ctx.arc(420, 940, r, 0, 2 * math.pi); setc(ctx, (1, 1, 1, 0.5 * (1 - r / 760))); ctx.set_line_width(14); ctx.stroke()
        # flying tea cup
        t = clamp(il / 20)
        ctx.save(); ctx.translate(lerp(840, 1100, t), lerp(1060, 600, t) + 900 * (t - 0.5) ** 2 - 225); ctx.rotate(t * 8)
        rect_r(ctx, -30, -35, 60, 70, 10); fl(ctx, WHITE, 5); ctx.restore()
    ctx.restore()


def s4(ctx, f):
    lf = f - 340
    if lf < 62:
        sofa_scene(ctx, f, lf)
        label(ctx, "*flomp*", 540, 560, 80, WHITE, -0.03, pop(lf, 0, 3) if lf < 30 else 0)
        label2(ctx, "\"Ahh...", "SILENCE.\"", WHITE, pop(lf, 6, 10), 110, col2=CYAN, y=1430)
    elif lf < 100:
        il = lf - 62
        sofa_scene(ctx, f, il + 60, snore=1.0 if il % 16 < 10 else 0.35, mom_shock=True)
        label(ctx, "*HONK-SHOOOO!!*", 540, 560, 120, YEL, -0.05 + 0.03 * math.sin(il), pop(il, 0, 3))
        label(ctx, "THE REAL THREAT:", 540, 1440, 96, RED, 0.03, pop(il, 8, 12))
    else:
        il = lf - 100   # 0..40
        mood = 'sleep' if il < 10 else 'awake'
        nursery_shot(ctx, f, il, mood, 1.0 + 0.25 * eout(pop(il, 10, 16)), shake_at(il, [10], 10, 14))
        if il >= 10:
            label(ctx, "*BLINK.*", 540, 430, 120, WHITE, 0.04, pop(il, 10, 13))


# ------------------------------------------------------------------ end
def split_end(ctx, f, il):
    ctx.save(); ctx.rectangle(0, 0, W, H / 2); ctx.clip()
    nursery_shot(ctx, f, il + 60, 'cry', 0.85, 6, R=220, cy=900, sy=540)
    ctx.restore()
    ctx.save(); ctx.rectangle(0, H / 2, W, H / 2); ctx.clip()
    ctx.save(); cam(ctx, 380, 1000, 1.0, 0, 0, f, sy=1440)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('2b3570')); ctx.fill()
    rays(ctx, 380, 900, 240, 1400, il * 0.02, col=(0.6, 0.75, 1), a=0.2, n=16)
    face(ctx, DAD, P(eye='closed', mouth='smile'), 420, 960, 240, -0.2)
    drool_bubble(ctx, 455, 1095, 26 + 12 * math.sin(il * 0.15))
    zzz(ctx, 700, 860, il, 1.2)
    ctx.restore(); ctx.restore()
    ctx.rectangle(0, H / 2 - 8, W, 16); setc(ctx, OUT); ctx.fill()
    label(ctx, "*WAAAAAAAH!!*", 540, 320, 96, RED, -0.04 + 0.03 * math.sin(il * 0.9), 1)
    label(ctx, "MEANWHILE, DAD:", 540, 1030, 80, YEL, 0.02, pop(il, 6, 10))


def mom_glare(ctx, f, il):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.08 * eout(pop(il, 0, 24)), 0, 3, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff4f6a')); ctx.fill()
    rays(ctx, 540, 900, 260, 1500, il * 0.03, col=(1, 0.9, 0.5), a=0.3, n=18)
    face(ctx, MOM, P(eye='glare', mouth='flat'), 540, 900, 290, 0.0)
    twitch(ctx, 540 + 0.6 * 290, 900 - 0.75 * 290, il, 1.3)
    ctx.restore()
    label(ctx, "\"...YOUR turn.\"", 540, 1430, 130, WHITE, -0.03, pop(il, 3, 7))


def s5(ctx, f):
    lf = f - 480
    if lf < 44:
        nursery_shot(ctx, f, lf, 'cry', 1.05 + 0.05 * math.sin(lf * 0.6), 14 if lf < 12 else 6)
        label(ctx, "*WAAAAAAAH!!*", 540, 430, 130, RED, -0.04 + 0.03 * math.sin(lf * 0.9), pop(lf, 0, 3))
    elif lf < 98:
        split_end(ctx, f, lf - 44)
    elif lf < 132:
        mom_glare(ctx, f, lf - 98)
    else:
        s1(ctx, f, f - 612)


SHOTS = [(0, s1), (54, s2), (200, s3), (340, s4), (480, s5)]
CUTS = (54, 114, 146, 200, 272, 308, 340, 402, 440, 480, 524, 578, 612)


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
                              "-i", "out/dont_wake_the_baby_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
