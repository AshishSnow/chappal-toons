"""'Toy Block at 3 AM' - original, general-audience comedy short, ~22s.
Hook: ECU Dad mid-scream "AAAAAAH!!!" with pain stars - he just stepped on a toy block in the dark.
 -> wide dark living room: he hops on one foot... and lands on ANOTHER one. *CRUNCH*
Beat 1 (MINEFIELD): top-down view of the floor: bare feet tiptoe between glowing blocks... foot lands on a toy car,
 side view: Dad surfs across the room "WHOAAA!" and pancakes into the door.
Beat 2 (REVENGE): morning, low angle Dad with a bucket "NEVER. AGAIN.", super-speed cleanup, sparkling floor "SPOTLESS."
Beat 3 (NIGHT 2): 3 AM, Dad strolls in the dark, eyes shut, whistling "Floor's CLEAR!"
Twist: *clack... clack...* flashlight: the kid is ASLEEP on the floor, building a block castle in his sleep.
 Dad: "Okay... back away... slowly..." -> floor-level slow-mo: his bare foot descends onto a block -> CRUNCH
 -> cuts back to the opening scream (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, zzz, living
from scenes34 import beam
from scenes45 import arm
import scenes13
from scenes13 import card as _card13
import random

BOY = dict(doodle.BOY, shirt=hx('7fc8ff'), pants=hx('7fc8ff'), shoes=hx('f3c29a'), hood=False)   # pajamas, bare feet
DAD = dict(doodle.DAD, shirt=hx('ffd23f'), pants=hx('3d5a9e'), shoes=hx('d9a079'))               # pajama dad, bare feet
N = 660
FLOOR = 1460
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
LY = 1400
BCOLS = [hx('ff3b5c'), hx('1f8bff'), hx('ffd23f'), hx('22b45a'), hx('ff8a1f'), hx('8a3cff')]

CAPS = {
    'p1': [[("STEPPING ON A TOY BLOCK", OUT)], [("AT 3 AM", RED)]],
    'p2': [[("STEP 1:", OUT)], [("THE MINEFIELD", ORANGE)]],
    'p3': [[("STEP 2:", OUT)], [("REVENGE CLEAN-UP", GREEN)]],
    'p4': [[("NIGHT 2, 3 AM:", OUT)], [("TOTALLY SAFE...", BLUE)]],
    'p5': [[("PLOT TWIST:", OUT)], [("HE BUILDS IN HIS SLEEP", PURPLE)]],
}
scenes13.CAPS = CAPS
card = _card13


def label2(ctx, a, b, col, t, size=104, col2=None, y=LY):
    label(ctx, a, 540, y - 60, size, col, -0.03, t)
    label(ctx, b, 540, y + 50, size, col2 or col, 0.02, t)


def label1(ctx, s, col, t, size=110, ang=-0.03):
    label(ctx, s, 540, LY + 20, size, col, ang, t)


# ------------------------------------------------------------------ props
def brick(ctx, x, y, s, col, a=0.0):
    """side view toy block sitting on (x, y)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    for sx in (-28, 28):
        rect_r(ctx, sx - 17, -78, 34, 22, 6); fl(ctx, col, 5)
    rect_r(ctx, -60, -60, 120, 60, 8); fl(ctx, col, 6)
    ctx.rectangle(-48, -52, 30, 10); setc(ctx, (1, 1, 1, 0.45)); ctx.fill()
    ctx.restore()


def brick_top(ctx, x, y, s, col, a=0.0, glow=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if glow > 0:
        ellipse(ctx, 0, 0, 120, 90); setc(ctx, (1, 0.2, 0.25, 0.28 * glow)); ctx.fill()
    rect_r(ctx, -62, -42, 124, 84, 10); fl(ctx, col, 6)
    for dx in (-30, 30):
        for dy in (-15, 15):
            ellipse(ctx, dx, dy, 15, 15); fl(ctx, light(col, 0.25), 4)
    ctx.restore()


def foot_top(ctx, x, y, s, a=0.0, lift=0.0):
    """bare foot seen from above (toes up the screen), pajama cuff at the heel"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); sc = s * (1 + 0.25 * lift); ctx.scale(sc, sc)
    if lift > 0:
        ellipse(ctx, 12, 40, 60, 100); setc(ctx, (0, 0, 0, 0.25)); ctx.fill()
    ellipse(ctx, 0, 0, 52, 95); fl(ctx, DAD['skin'], 7)
    for k, (tx, ty, r) in enumerate(((-30, -88, 19), (-6, -100, 15), (14, -98, 13), (31, -90, 11), (45, -78, 10))):
        ellipse(ctx, tx, ty, r, r * 1.1); fl(ctx, DAD['skin'], 5)
    ellipse(ctx, 0, 95, 64, 44); fl(ctx, DAD['pants'], 7)
    ctx.restore()


def foot_side(ctx, x, y, s, f_=1):
    """big bare foot side view, sole at y, toes toward +x*f_"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s * f_, s)
    ctx.rectangle(-150, -900, 150, 760); fl(ctx, DAD['pants'], 8)
    ctx.new_path(); ctx.move_to(-150, -160); ctx.line_to(-150, -40); ctx.curve_to(-150, 0, -110, 8, -60, 8)
    ctx.line_to(150, 8); ctx.curve_to(210, 8, 220, -50, 170, -70); ctx.curve_to(90, -95, 20, -120, 0, -160); ctx.close_path()
    fl(ctx, DAD['skin'], 8)
    for k in range(4):
        ellipse(ctx, 175 - k * 32, -40 - k * 6, 22 - k * 2, 24 - k * 2); fl(ctx, DAD['skin'], 5)
    ctx.rectangle(-160, -170, 170, 30); fl(ctx, dark(DAD['pants'], 0.8), 7)
    ctx.restore()


def toy_car(ctx, x, y, s, spin=0.0, col=hx('ff3b5c')):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rect_r(ctx, -90, -70, 180, 46, 16); fl(ctx, col, 6)
    rect_r(ctx, -46, -104, 92, 40, 12); fl(ctx, col, 6)
    rect_r(ctx, -34, -96, 30, 24, 5); fl(ctx, hx('bfe6ff'), 4)
    rect_r(ctx, 6, -96, 30, 24, 5); fl(ctx, hx('bfe6ff'), 4)
    for wx in (-52, 52):
        ellipse(ctx, wx, -22, 22, 22); fl(ctx, INK, 4)
        ctx.move_to(wx, -22); ctx.line_to(wx + 14 * math.cos(spin), -22 + 14 * math.sin(spin)); setc(ctx, (1, 1, 1)); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def bucket(ctx, x, y, s, full=0.0, lf=0):
    """bucket with its bottom at (x, y)"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if full > 0:
        rnd = random.Random(5)
        for k in range(int(9 * full)):
            brick(ctx, rnd.uniform(-60, 60), -150 - rnd.uniform(0, 50) * full, 0.55, BCOLS[k % 6], rnd.uniform(-0.6, 0.6))
    poly(ctx, [(-100, -160), (100, -160), (78, 0), (-78, 0)]); fl(ctx, hx('3ccfb0'), 7)
    ellipse(ctx, 0, -160, 100, 24); fl(ctx, dark(hx('3ccfb0'), 0.75), 6)
    ctx.new_path(); ctx.arc(0, -160, 96, math.pi, 2 * math.pi); ink(ctx, 7); ctx.stroke()
    ctx.restore()


def pain_zigs(ctx, x, y, r, lf, col=YEL, n=8):
    for k in range(n):
        a = k * 2 * math.pi / n + 0.2 * math.sin(lf * 0.6 + k)
        r0, r1 = r, r * (1.45 + 0.15 * math.sin(lf + k))
        ctx.move_to(x + math.cos(a) * r0, y + math.sin(a) * r0)
        mx, my = x + math.cos(a + 0.12) * (r0 + r1) / 2, y + math.sin(a + 0.12) * (r0 + r1) / 2
        ctx.line_to(mx, my); ctx.line_to(x + math.cos(a) * r1, y + math.sin(a) * r1)
    ink(ctx, 16); ctx.stroke_preserve(); setc(ctx, col); ctx.set_line_width(8); ctx.stroke()


def floor_top(ctx, dark_=True):
    base = hx('3a2d52') if dark_ else hx('c98a52')
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, base); ctx.fill()
    for i in range(-6, 16):
        ctx.rectangle(i * 150, -600, 6, 3200); setc(ctx, dark(base, 0.75)); ctx.fill()
        for j in range(-4, 14):
            ctx.rectangle(i * 150, -600 + j * 360 + (i % 2) * 180, 150, 6); setc(ctx, dark(base, 0.75)); ctx.fill()


def hop_pose(lf, **kw):
    b = abs(math.sin(lf * 0.35))
    p = P(torso=-8 + 6 * math.sin(lf * 0.35), lhip=4, lkn=-6 - 20 * (1 - b), rhip=75, rkn=-120, lsh=150 + 25 * math.sin(lf * 0.7), lel=-30,
          rsh=55, rel=-35, eye='shock', mouth='scream', head=-6)
    p.update(kw); return p


def dark_mask(ctx, shapes, a=0.86):
    """darken everything except the given light shapes (callables that build a path)"""
    ctx.push_group()
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, (0.03, 0.02, 0.08, a)); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    for sh in shapes:
        sh(ctx); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.pop_group_to_source(); ctx.paint()


# ------------------------------------------------------------------ opening
def opening_face(ctx, f, lf, lab=True):
    sh = shake_at(lf, [0], 14, 26) + 5
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(lf, 0, 30)), 1.5 * math.sin(lf * 0.9), sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff3b5c')); ctx.fill()
    rays(ctx, 540, 820, 240, 1700, lf * 0.05, col=(1, 0.9, 0.4), a=0.5, n=18)
    cx, cy = 540, 820 + 8 * math.sin(lf * 1.3)
    pain_zigs(ctx, cx, cy, 330, lf)
    face(ctx, DAD, P(eye='shock', mouth='scream', head=0), cx, cy, 255, 0.04 * math.sin(lf * 1.1))
    stars_ko(ctx, cx, cy - 300, lf * 0.12, 5, 230)
    for k in (-1, 1):
        ellipse(ctx, cx + k * 300, cy - 120 + (lf * 6 % 80), 16, 24); fl(ctx, hx('bfe6ff'), 4)
    # the culprit in the foreground
    brick(ctx, 760, 1330, 1.3, RED, 0.05 * math.sin(lf))
    pain_zigs(ctx, 760, 1290, 120, lf, col=(1, 1, 1), n=6)
    ctx.restore()
    if lab:
        label1(ctx, "AAAAAAAH!!!", YEL, pop(lf, 0, 3) if lf > 0 else 1, 150, -0.04)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 45:
        opening_face(ctx, f, f)
    else:
        lf = f - 45
        crunch = lf >= 36
        ctx.save(); cam(ctx, 540, 1080, 1.0 + (0.12 * eout(pop(lf, 36, 42)) if crunch else 0), 0, shake_at(lf, [36], 14, 30), f)
        living(ctx, lights=False)
        # moonlight patch
        poly(ctx, [(160, 700), (420, 700), (620, 1460), (-60, 1460)]); setc(ctx, (0.7, 0.8, 1, 0.12)); ctx.fill()
        rnd = random.Random(11)
        for k in range(6):
            brick(ctx, rnd.uniform(60, 1020), FLOOR + rnd.uniform(-10, 30), 0.7, BCOLS[k], rnd.uniform(-0.3, 0.3))
        if not crunch:
            x = 260 + 300 * lf / 36
            hy = abs(math.sin(lf * 0.35)) * 120
            draw(ctx, x, FLOOR - 186 * 1.6 - hy, 1.6, 1, DAD, hop_pose(lf))
            brick(ctx, 640, FLOOR + 10, 0.9, BLUE)
        else:
            il = lf - 36
            draw(ctx, 560, FLOOR - 186 * 1.6 - 30, 1.6, 1, DAD,
                 P(torso=0, lhip=-40, lkn=-10, rhip=40, rkn=-10, lsh=160, lel=-20, rsh=-160, rel=20, eye='shock', mouth='scream', head=0))
            brick(ctx, 560, FLOOR + 10, 0.9, BLUE)
            pain_zigs(ctx, 560, FLOOR - 20, 90, il, n=7)
            stars_ko(ctx, 560, 640, il * 0.15, 4, 140)
        ctx.restore()
        if not crunch:
            label1(ctx, "*HOP! HOP! HOP!*", (1, 1, 1), pop(lf, 0, 4), 120)
        else:
            label2(ctx, "*CRUNCH!*", "...AGAIN?!", YEL, pop(lf, 36, 39), 130, col2=(1, 1, 1))
    card(ctx, 'p1', f, -6, 108)


PATH = [(380, 1700), (640, 1550), (420, 1330), (660, 1150), (430, 960), (650, 780), (440, 600)]
BLOCKS = [(240, 1500, 0), (520, 1680, 1), (800, 1420, 2), (560, 1280, 3), (280, 1150, 4), (800, 1060, 5),
          (560, 980, 0), (300, 820, 1), (780, 700, 2), (220, 540, 3), (870, 1260, 4), (150, 1320, 5), (900, 900, 1), (600, 640, 4)]


def s2(ctx, f):
    lf = f - 110
    if lf < 72:
        # top-down: the minefield, bare feet tiptoe between blocks
        step = min(len(PATH) - 1, lf // 11)
        camy = 1500 - 520 * eout(pop(lf, 0, 72))
        ctx.save(); cam(ctx, 540, camy, 1.0, -3, 0, f, sy=1000)
        floor_top(ctx)
        for k, (bx, by, c) in enumerate(BLOCKS):
            brick_top(ctx, bx, by, 0.85, BCOLS[c], 0.4 * math.sin(k * 1.7), glow=0.6 + 0.4 * math.sin(lf * 0.4 + k))
        # the toy car waiting on the path
        ctx.save(); ctx.translate(560, 470); ctx.rotate(-math.pi / 2)
        toy_car(ctx, 0, 40, 1.2); ctx.restore()
        for k in range(step + 1):
            x, y = PATH[k]
            if k < step - 1:
                continue
            lift = 0.0 if k < step else 1 - eout(pop(lf, k * 11, k * 11 + 6))
            foot_top(ctx, x, y, 1.2, 0.1 * (1 if k % 2 else -1), lift)
        ctx.restore()
        label1(ctx, "...tiptoe... tiptoe...", (1, 1, 1), pop(lf, 0, 4), 104)
    else:
        il = lf - 72
        # side view: surfing across the room on the toy car, then pancake into the door
        hit = il >= 44
        ctx.save(); cam(ctx, 540, 1080, 1.0, 0, shake_at(il, [44], 14, 32), f)
        living(ctx, lights=False)
        poly(ctx, [(160, 700), (420, 700), (620, 1460), (-60, 1460)]); setc(ctx, (0.7, 0.8, 1, 0.12)); ctx.fill()
        if not hit:
            x = -100 + 820 * ein(pop(il, 0, 44))
            for k in range(7):
                ctx.move_to(x - 260 - k * 40, 760 + k * 100); ctx.rel_line_to(-200 - 60 * (k % 3), 0)
            setc(ctx, (1, 1, 1, 0.5)); ctx.set_line_width(10); ctx.stroke()
            toy_car(ctx, x, FLOOR, 1.4, il * 0.9)
            w = math.sin(il * 0.8)
            draw(ctx, x, FLOOR - 60 - 186 * 1.6, 1.6, 1, DAD,
                 P(torso=-14 + 6 * w, lhip=-28, lkn=-14, rhip=28, rkn=-14, lsh=120 + 60 * w, lel=-30, rsh=-120 + 60 * w, rel=30,
                   eye='shock', mouth='scream', head=-8))
            label1(ctx, "\"WHOAAAAA!\"", YEL, pop(il, 0, 4), 140, -0.05)
        else:
            jl = il - 44
            # flat against the door, slowly sliding down
            sl = 60 * eout(pop(jl, 4, 20))
            # upside down against the door, legs up the wall, sliding down
            ctx.save(); ctx.translate(740, 930 + 0.5 * sl); ctx.rotate(math.pi * 0.92)
            draw(ctx, 0, -186 * 1.6 + 300, 1.6, 1, DAD,
                 P(torso=0, lhip=-25, lkn=-20, rhip=30, rkn=-30, lsh=140, lel=-20, rsh=-130, rel=20, eye='closed', mouth='wavy'))
            ctx.restore()
            toy_car(ctx, 380 - 60 * eout(pop(jl, 0, 10)), FLOOR, 1.4, 0.3)
            stars_ko(ctx, 760, 1180, jl * 0.15, 5, 170)
            puff(ctx, 820, 1100, pop(jl, 0, 14), 2.2)
        ctx.restore()
        if hit:
            label1(ctx, "*CRASH!*", (1, 1, 1), pop(il, 44, 47), 150, 0.04)
    card(ctx, 'p2', f, 112, 246)


def s3(ctx, f):
    lf = f - 250
    if lf < 50:
        # morning, low angle: Dad with a bucket
        ctx.save(); cam(ctx, 540, 1100, 1.0 + 0.08 * eout(pop(lf, 0, 50)), -4, shake_at(lf, [0, 26], 10, 18), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('6fd6c8')); ctx.fill()
        rays(ctx, 540, 760, 200, 1600, lf * 0.03, col=(1, 1, 1), a=0.25, n=16)
        # ceiling light
        poly(ctx, [(380, 480), (700, 480), (620, 400), (460, 400)]); fl(ctx, hx('ffd23f'), 8)
        b = draw(ctx, 540, 1900 - 186 * 2.6, 2.6, 1, DAD,
                 P(torso=0, lhip=-14, lkn=0, rhip=14, rkn=0, lsh=20, lel=-10, rsh=-35, rel=-10, eye='glare', mouth='flat', head=0))
        hx_, hy_ = b['front']
        ctx.move_to(hx_, hy_); ctx.line_to(hx_ - 40, hy_ + 60); ink(ctx, 8); ctx.stroke()
        bucket(ctx, hx_ - 40, hy_ + 230, 1.2)
        # bandaged toe
        ctx.restore()
        if lf < 26:
            label2(ctx, "DAD, THE NEXT", "MORNING:", (1, 1, 1), pop(lf, 0, 4), 100, col2=YEL)
        else:
            label2(ctx, "\"NEVER.", "AGAIN.\"", RED, pop(lf, 26, 29), 140, col2=(1, 1, 1))
    elif lf < 95:
        il = lf - 50
        # super-speed clean-up
        ctx.save(); cam(ctx, 540, 1080, 1.0, 0, 4, f)
        living(ctx, lights=True)
        for k in range(10):
            ctx.move_to(-100, 620 + k * 90); ctx.rel_line_to(1300, 0)
        setc(ctx, (1, 1, 1, 0.25)); ctx.set_line_width(12); ctx.stroke()
        rnd = random.Random(21)
        left = 12 - int(12 * pop(il, 2, 40))
        for k in range(12):
            if k < left:
                brick(ctx, rnd.uniform(60, 640), FLOOR + rnd.uniform(-10, 30), 0.7, BCOLS[k % 6], rnd.uniform(-0.3, 0.3))
            else:
                rnd.uniform(0, 1); rnd.uniform(0, 1); rnd.uniform(0, 1)
        for k in range(5):
            u = ((il * 0.12 + k * 0.2) % 1)
            x = lerp(200 + 80 * k, 860, u); y = FLOOR - 40 - 520 * math.sin(math.pi * u)
            brick(ctx, x, y, 0.7, BCOLS[k], il * 0.4 + k)
        bucket(ctx, 860, FLOOR + 20, 1.2, full=pop(il, 0, 40), lf=il)
        # Dad as a speed blur
        for j in range(3):
            xx = 420 + 220 * math.sin(il * 0.55 - j * 0.35)
            ctx.push_group()
            draw(ctx, xx, FLOOR - 186 * 1.9, 1.9, 1 if math.cos(il * 0.55) > 0 else -1, DAD,
                 P(torso=35, lhip=40, lkn=-60, rhip=-30, rkn=-30, lsh=80, lel=-20, rsh=40, rel=-20, eye='glare', mouth='grin', head=-20))
            ctx.pop_group_to_source(); ctx.paint_with_alpha(1.0 if j == 0 else 0.35)
        ctx.restore()
        label1(ctx, "*SWOOSH SWOOSH SWOOSH*", (1, 1, 1), pop(il, 0, 4), 96)
    else:
        il = lf - 95
        ctx.save(); cam(ctx, 540, 1080, 1.0 + 0.06 * eout(pop(il, 0, 45)), 0, shake_at(il, [0], 8, 12), f)
        living(ctx, lights=True)
        ctx.rectangle(-500, FLOOR + 6, 2200, 600); setc(ctx, hx('e0a868')); ctx.fill()
        # shelf with the full bucket, way up high
        ctx.rectangle(560, 700, 220, 22); fl(ctx, hx('8a5a3a'), 6)
        bucket(ctx, 670, 700, 0.8, full=1.0)
        draw(ctx, 330, FLOOR - 186 * 1.7, 1.7, 1, DAD,
             P(torso=-4, lhip=-12, lkn=0, rhip=12, rkn=0, lsh=-40, lel=120, rsh=40, rel=-120, eye='smug', mouth='smile', head=-6))
        for k in range(6):
            sparkle(ctx, 120 + 170 * k, FLOOR + 60 + 30 * (k % 2), 30 * eout(pop(il, 2 + 3 * k, 8 + 3 * k)) * (1 + 0.2 * math.sin(il * 0.5 + k)))
        ctx.restore()
        label2(ctx, "\"SPOTLESS.\"", "*DING!*", (1, 1, 1), pop(il, 0, 4), 120, col2=YEL)
    card(ctx, 'p3', f, 252, 386)


def s4(ctx, f):
    lf = f - 390
    # night 2: Dad strolls in the dark, eyes shut, whistling
    ctx.save(); cam(ctx, 540, 1080, 1.05, 0, 0, f)
    living(ctx, lights=False)
    poly(ctx, [(160, 700), (420, 700), (620, 1460), (-60, 1460)]); setc(ctx, (0.7, 0.8, 1, 0.12)); ctx.fill()
    x = 160 + 440 * lf / 50
    ph = lf * 0.4
    s_ = math.sin(ph)
    draw(ctx, x, FLOOR - 186 * 1.6 - 8 * abs(s_), 1.6, 1, DAD,
         P(torso=-6, lhip=22 * s_, lkn=-10 - 20 * max(0, s_), rhip=-22 * s_, rkn=-10 - 20 * max(0, -s_), lsh=-30, lel=110, rsh=30, rel=-110,
           eye='closed', mouth='smile', head=-10))
    for k in range(3):
        u = ((lf + k * 12) % 36) / 36
        text(ctx, "~", x + 150 + 80 * u, 640 - 160 * u, 70, YEL + (1,), ow=8, shadow=False)
    ctx.restore()
    label2(ctx, "\"Floor's", "CLEAR!\"", (1, 1, 1), pop(lf, 0, 4), 120, col2=YEL)
    card(ctx, 'p4', f, 392, 438)


def kid_building(ctx, lf, tower=1.0):
    # castle of blocks + sleeping kid on the floor building it
    base_x = 700
    rnd = random.Random(8)
    rows = [5, 4, 3, 2]
    nshow = int(14 * tower + 0.5)
    c = 0
    for r, cnt in enumerate(rows):
        for j in range(cnt):
            if c >= nshow:
                break
            bx = base_x - (cnt - 1) * 52 + j * 104
            brick(ctx, bx, FLOOR - r * 66, 0.85, BCOLS[(r * 3 + j) % 6])
            c += 1
    # kid body (sitting) behind his arm
    rect_r(ctx, 180, 1080, 300, 400, 90); fl(ctx, BOY['shirt'], 9)
    for k in range(4):
        sparkle(ctx, 230 + 70 * k, 1180 + 80 * (k % 2), 16, col=(1, 1, 1))
    face(ctx, BOY, P(eye='closed', mouth='smile', head=0), 330, 900, 150, 0.12 + 0.05 * math.sin(lf * 0.2))
    # arm placing a block on top
    u = 0.5 + 0.5 * math.sin(lf * 0.25)
    hx_, hy_ = lerp(520, 640, u), lerp(1150, 1150 - 120, u)
    arm(ctx, 420, 1150, hx_, hy_, BOY, 54)
    brick(ctx, hx_ + 60, hy_ + 20, 0.7, PURPLE, 0.1)
    zzz(ctx, 270, 720, lf, 1.0)


def s5(ctx, f):
    lf = f - 440
    if lf < 80:
        lights = lf >= 22
        ctx.save(); cam(ctx, 540, 1080, 1.0 + 0.08 * eout(pop(lf, 22, 80)), 0, shake_at(lf, [22], 8, 12), f)
        living(ctx, lights=True)
        kid_building(ctx, lf, 1.0)
        # Dad at the left edge holding the flashlight
        face(ctx, DAD, P(eye='shock', mouth='open', head=0), -20, 720, 130, 0.1)
        ctx.restore()
        if not lights:
            dark_mask(ctx, [lambda c: (ellipse(c, 700 + 40 * math.sin(lf * 0.5), 1300, 40, 30))], 0.93)
            label1(ctx, "*clack... clack...*", (1, 1, 1), pop(lf, 0, 4), 110)
        else:
            def bm(c):
                c.move_to(60, 820); c.line_to(1100, 700); c.line_to(1100, 1600); c.line_to(60, 860); c.close_path()
            dark_mask(ctx, [bm, lambda c: ellipse(c, 560, 1120, 420, 440)], 0.86)
            ctx.save(); cam(ctx, 540, 1080, 1.0 + 0.08 * eout(pop(lf, 22, 80)), 0, 0, f)
            beam(ctx, 60, 840, 560, 1120, 20, 380, 0.16)
            ctx.restore()
            label2(ctx, "\"He's...", "ASLEEP?!\"", (1, 1, 1), pop(lf, 26, 30), 120, col2=YEL)
        card(ctx, 'p5', f, 464, 518)
    elif lf < 128:
        il = lf - 80
        # Dad ECU whispering, sweating, backing away
        ctx.save(); cam(ctx, 540, 900, 1.0 + 0.1 * eout(pop(il, 0, 48)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('1d2c50')); ctx.fill()
        rays(ctx, 540, 900, 200, 1500, il * 0.02, col=(0.6, 0.7, 1), a=0.15, n=14)
        face(ctx, DAD, P(eye='shock', mouth='wavy', head=0), 540 - 3 * il, 880, 240, -0.04)
        for k in (-1, 1):
            ellipse(ctx, 540 + k * 290 - 3 * il, 760 + (il * 5 % 70), 14, 22); fl(ctx, hx('bfe6ff'), 4)
        ctx.restore()
        label2(ctx, "\"Okay... back away...", "s l o w l y...\"", (1, 1, 1), pop(il, 0, 4), 92, col2=YEL)
    elif lf < 190:
        il = lf - 128
        # floor-level slow-mo: the foot descends onto a block
        u = ein(pop(il, 0, 58))
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.15 * u, 0, 2 if il > 40 else 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('1d2c50')); ctx.fill()
        ctx.rectangle(-500, 1240, 2200, 1500); setc(ctx, hx('3a2d52')); ctx.fill()
        ctx.move_to(-500, 1240); ctx.line_to(1700, 1240); ink(ctx, 8); ctx.stroke()
        for k in range(8):
            ctx.move_to(-500, 1280 + k * k * 18); ctx.line_to(1700, 1280 + k * k * 18)
        setc(ctx, (0, 0, 0, 0.25)); ctx.set_line_width(5); ctx.stroke()
        rays(ctx, 600, 1180, 140, 1200, il * 0.01, col=(1, 0.3, 0.3), a=0.12 + 0.12 * u, n=16)
        brick(ctx, 600, 1250, 1.5, RED)
        foot_side(ctx, 470, lerp(560, 1150, u), 1.1, 1)
        ctx.restore()
        label1(ctx, "n o o o o o o . . .", (1, 1, 1), pop(il, 0, 4), 110)
    else:
        il = lf - 190
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 630)


SHOTS = [(0, s1), (110, s2), (250, s3), (390, s4), (440, s5)]
CUTS = (45, 110, 182, 250, 300, 345, 390, 440, 520, 568, 630)


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
                              "-i", "out/toyblock_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
