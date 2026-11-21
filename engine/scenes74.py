"""'It WILL Fit!' - packing the car for vacation. Original, general-audience comedy short, 22s.
Hook: Dad's red strained ECU, both arms pushing a trunk lid down, caption "PACKING THE CAR / FOR VACATION:" + "IT... WILL... FIT!!"
Beat 1: tilt-up reveal: tiny car vs a giant luggage mountain. *crack crack* "EASY."
        top-down trunk puzzle: suitcases drop, spin and slot in *bloop* -> "PERFECT FIT!" *DING*
Beat 2: kid runs in with a teddy bigger than him "DON'T FORGET MR. FLUFFY!!" -> Dad eye twitch.
        Dad sits on the hatch *BOING BOING* -> *SLAM!* "DONE!!"
Twist:  Mom adds ONE pair of sunglasses -> *creak...* -> KA-BOOOM: the trunk explodes, luggage rains down and buries Dad (thumbs up).
End:    car on the road: luggage tower on the roof, Mr. Fluffy in the front seat with shades, Dad squished in the back.
        Mom: "...honey? Where are the SNACKS?" -> loop to the strain hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import sweat, twitch, arm_to
from scenes8 import sit
from scenes37 import teddy
from scenes63 import car as car63
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


DAD = dict(doodle.DAD, shirt=hx('22b45a'), pants=hx('2a3a6a'))
REDDAD = dict(DAD, skin=hx('ff9a86'))
MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'), pants=hx('3d5a9e'))
BOY = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ffc93c'), pants=hx('2a3a6a'))
N = 660
RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
SKY = hx('8fd8ff')
FLOOR = 1460
DK = 1.4
KK = 1.0
SUITC = [RED, BLUE, GREEN, GOLD, ORANGE, PURPLE, PINK, CYAN]

CAPS = {'p1': [[("PACKING THE CAR", OUT)], [("FOR VACATION:", BLUE)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def suitcase(ctx, x, y, w, h, col, a=0.0, top=False):
    """centre (x, y). top=True: seen from above (no wheels)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    lw = max(4, min(w, h) * 0.05)
    if not top:
        ctx.new_path(); ctx.arc(0, -h / 2 - 4, min(w, h) * 0.16, math.pi, 2 * math.pi); ink(ctx, lw * 1.6); ctx.stroke()
        for wx in (-w * 0.32, w * 0.32):
            ellipse(ctx, wx, h / 2 + 4, lw * 2, lw * 2); fl(ctx, hx('2a2840'), lw * 0.6)
    rect_r(ctx, -w / 2, -h / 2, w, h, min(w, h) * 0.14); fl(ctx, col, lw)
    for sx in (-0.22, 0.22):
        ctx.rectangle(sx * w - lw * 0.9, -h / 2 + lw, lw * 1.8, h - 2 * lw); setc(ctx, (1, 1, 1, 0.45)); ctx.fill()
    if top:
        rect_r(ctx, -w * 0.12, -h * 0.08, w * 0.24, h * 0.16, 6); fl(ctx, hx('2a2840'), lw * 0.6)
    ctx.restore()


def beach_ball(ctx, x, y, r, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    cols = [RED, WHITE, BLUE, WHITE, GOLD, WHITE]
    for k in range(6):
        ctx.move_to(0, 0); ctx.arc(0, 0, r, k * math.pi / 3, (k + 1) * math.pi / 3); ctx.close_path(); setc(ctx, cols[k]); ctx.fill()
    ctx.new_path(); ctx.arc(0, 0, r, 0, 2 * math.pi); ink(ctx, max(4, r * 0.07)); ctx.stroke()
    ctx.restore()


def shades(ctx, x, y, s, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    for sx in (-1, 1):
        ellipse(ctx, sx * 34, 0, 30, 22); fl(ctx, hx('1a1a2a'), 5)
        ellipse(ctx, sx * 34 - 8, -7, 8, 5); setc(ctx, (1, 1, 1, 0.7)); ctx.fill()
    ctx.move_to(-6, -4); ctx.line_to(6, -4); ink(ctx, 6); ctx.stroke()
    ctx.restore()


# items of the luggage mountain: (x, y, w, h, colour index) built bottom-up
def _mountain():
    rnd = random.Random(7)
    out = []
    y = FLOOR
    rows = [(3, 150), (3, 130), (2, 150), (3, 110), (2, 120), (2, 100), (1, 130)]
    for r, (n, hh) in enumerate(rows):
        tot = 440 - r * 30
        x0 = 790 - tot / 2
        for k in range(n):
            w = tot / n - 8
            out.append((x0 + (k + 0.5) * tot / n + rnd.uniform(-10, 10), y - hh / 2, w, hh, rnd.randrange(8), rnd.uniform(-0.06, 0.06)))
        y -= hh + 6
    return out, y


MOUNT, MTOP = _mountain()


def mountain(ctx, lf, wob=0.0):
    for i, (x, y, w, h, c, a) in enumerate(MOUNT):
        dx = wob * (FLOOR - y) * 0.04 * math.sin(lf * 0.25)
        suitcase(ctx, x + dx, y, w, h, SUITC[c], a)
    dx = wob * (FLOOR - MTOP) * 0.04 * math.sin(lf * 0.25)
    beach_ball(ctx, 790 + dx, MTOP - 60, 62, lf * 0.02)


def driveway_bg(ctx, lf):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, SKY); ctx.fill()
    for (cx, cy, r) in ((180, 360, 70), (880, 250, 90)):
        for dx in (-r, 0, r):
            ellipse(ctx, cx + dx + (lf * 0.3) % 40, cy + (0 if dx else -r * 0.4), r, r * 0.7); setc(ctx, WHITE); ctx.fill()
    rect_r(ctx, -400, 560, 900, 900, 0); fl(ctx, hx('ffd9a8'), 8)
    for k in range(10):
        ctx.move_to(-400, 600 + k * 85); ctx.line_to(500, 600 + k * 85)
    setc(ctx, hx('f2c590')); ctx.set_line_width(5); ctx.stroke()
    poly(ctx, [(-440, 600), (40, 370), (540, 600)]); fl(ctx, hx('c8463a'), 8)
    rect_r(ctx, 60, 720, 220, 220, 10); fl(ctx, hx('bfe8ff'), 7)
    ctx.rectangle(-3000, FLOOR - 60, 7000, 3000); setc(ctx, hx('6fd86a')); ctx.fill()
    ctx.rectangle(-3000, FLOOR - 20, 7000, 3000); setc(ctx, hx('a8acb8')); ctx.fill()
    ctx.move_to(-3000, FLOOR - 20); ctx.line_to(4000, FLOOR - 20); ink(ctx, 7); ctx.stroke()


# ------------------------------------------------------------------ hook
def hook_face(ctx, f, lf):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eio(pop(lf, 0, 54)), 0, 5, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8a3c')); ctx.fill()
    rays(ctx, 540, 860, 260, 1500, lf * 0.03, col=(1, 0.95, 0.5), a=0.35, n=18)
    cx, cy, R = 540, 840, 270
    jit = 4 * math.sin(lf * 2.3)
    # trunk lid at the bottom with luggage bulging out
    suitcase(ctx, 300, 1235, 300, 150, BLUE, -0.25)
    suitcase(ctx, 790, 1230, 280, 140, PINK, 0.3)
    teddy(ctx, 560, 1200, 0.8, 0.4)
    face(ctx, REDDAD, P(eye='glare', mouth='grin'), cx, cy + jit * 0.5, R, 0.02 * math.sin(lf * 1.3))
    ctx.save(); ctx.translate(540, 1340 + jit); ctx.rotate(0.02 * math.sin(lf * 1.7))
    rect_r(ctx, -620, -70, 1240, 600, 40); fl(ctx, hx('ff4d5e'), 10)
    rect_r(ctx, -620, -70, 1240, 40, 20); setc(ctx, hx('ff8a96')); ctx.fill()
    ctx.restore()
    for side in (-1, 1):
        arm_to(ctx, cx + side * 0.55 * R, cy + 1.0 * R, cx + side * 330, 1300 + jit, DAD['shirt'], REDDAD['skin'], bend=side * 50, w=120)
        ellipse(ctx, cx + side * 330, 1300 + jit, 70, 46); fl(ctx, REDDAD['skin'], 7)
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
    label(ctx, "\"IT... WILL... FIT!!\"", 540, 1440, 120, WHITE, -0.03, t)


# ------------------------------------------------------------------ beat 1
def reveal_shot(ctx, f, il):
    # il 0..56: tilt up from the tiny car to the top of the luggage mountain
    t = eio(pop(il, 4, 30))
    ctx.save(); cam(ctx, 560, lerp(1240, 960, t), lerp(1.35, 0.98, t), 0, 0, f)
    driveway_bg(ctx, il)
    mountain(ctx, il)
    car63(ctx, 330, FLOOR, 0.62, True, False)
    # Dad cracks his knuckles in front of the car
    crack = 30 <= il < 44 and (il // 4) % 2 == 0
    p = P(eye='smug', mouth='smug', lsh=-70, lel=-110, rsh=70, rel=110, torso=-2) if crack else P(eye='smug', mouth='smug', lsh=10, rel=-120, rsh=-150, lel=-20)
    draw(ctx, 520, FLOOR - 186 * 1.25, 1.25, 1, DAD, p)
    ctx.restore()
    if il < 30:
        label(ctx, "THE LUGGAGE:", 540, 460, 96, WHITE, -0.03, pop(il, 8, 12))
    else:
        label(ctx, "*crack crack*", 540, 460, 80, WHITE, 0.03, pop(il, 30, 33))
        label(ctx, "\"EASY.\"", 540, 1440, 130, YEL, -0.03, pop(il, 40, 44))


# top-down trunk puzzle
TX0, TY0, CW, CH = 160, 560, 190, 210
PIECES = [(0, 3, 2, 1, 0), (2, 3, 2, 1, 1), (0, 1, 1, 2, 2), (1, 2, 2, 1, 3), (3, 1, 1, 2, 4), (1, 1, 2, 1, 5), (0, 0, 4, 1, 6)]


def puzzle_shot(ctx, f, il):
    done = il >= 82
    ctx.save(); cam(ctx, 540, 980, 1.0 + 0.04 * eio(pop(il, 82, 90)), 0, shake_at(il, [82], 8, 10), f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('a8acb8')); ctx.fill()
    rect_r(ctx, TX0 - 70, TY0 - 70, 4 * CW + 140, 4 * CH + 140, 60); fl(ctx, hx('ff4d5e'), 10)
    ctx.rectangle(TX0, TY0, 4 * CW, 4 * CH); fl(ctx, hx('3a2a40'), 8)
    for c in range(1, 4):
        ctx.move_to(TX0 + c * CW, TY0); ctx.line_to(TX0 + c * CW, TY0 + 4 * CH)
    for r in range(1, 4):
        ctx.move_to(TX0, TY0 + r * CH); ctx.line_to(TX0 + 4 * CW, TY0 + r * CH)
    setc(ctx, (1, 1, 1, 0.08)); ctx.set_line_width(4); ctx.stroke()
    ctx.save(); ctx.rectangle(TX0 - 70, -500, 4 * CW + 140, TY0 + 4 * CH + 570); ctx.clip()
    last_land = -1
    for k, (c, r, w, h, ci) in enumerate(PIECES):
        st = 4 + k * 11
        if il < st:
            continue
        t = clamp((il - st) / 9)
        tx = TX0 + (c + w / 2) * CW; ty = TY0 + (r + h / 2) * CH
        y = lerp(TY0 - 360, ty, t * t)
        a = (1 - t) * (math.pi / 2 if k % 2 else -math.pi / 2)
        sq = 1 + 0.12 * math.sin(math.pi * clamp((il - st - 9) / 4)) if t >= 1 else 1
        ctx.save(); ctx.translate(tx, y); ctx.scale(sq, 2 - sq)
        suitcase(ctx, 0, 0, w * CW - 14, h * CH - 14, SUITC[ci], a, top=True)
        ctx.restore()
        if t >= 1:
            last_land = k
    ctx.restore()
    if done:
        ctx.rectangle(TX0, TY0, 4 * CW, 4 * CH); setc(ctx, (1, 1, 0.7, 0.4 * (1 - pop(il, 82, 90)))); ctx.fill()
        for k in range(8):
            a = k * math.pi / 4 + il * 0.05
            sparkle(ctx, 540 + math.cos(a) * 520, 980 + math.sin(a) * 560, 30, YEL)
    ctx.restore()
    label(ctx, "LEVEL: DAD", 540, 400, 90, WHITE, -0.02, pop(il, 0, 4))
    if not done and last_land >= 0:
        k = last_land; st = 4 + k * 11 + 9
        if il - st < 6:
            c, r, w, h, ci = PIECES[k]
            label(ctx, "*bloop!*", TX0 + (c + w / 2) * CW, TY0 + (r + h / 2) * CH, 64, WHITE, 0.05, pop(il, st, st + 2))
    if done:
        label(ctx, "\"PERFECT FIT!\"", 540, 1450, 120, YEL, -0.03, pop(il, 82, 85))


def s2(ctx, f):
    lf = f - 54
    if lf < 56:
        reveal_shot(ctx, f, lf)
    else:
        puzzle_shot(ctx, f, lf - 56)


# ------------------------------------------------------------------ beat 2
def kid_run(ctx, f, il):
    ctx.save(); cam(ctx, 560, 1120, 1.05, 0, 3, f)
    driveway_bg(ctx, il)
    car63(ctx, 420, FLOOR, 0.62, True, True)
    x = lerp(1250, 640, eout(pop(il, 0, 22)))
    stop = il >= 22
    p = run_pose(il * 0.9, eye='happy', mouth='grin', torso=10) if not stop else P(eye='happy', mouth='grin')
    p.update(lsh=165, lel=10, rsh=-165, rel=-10)
    b = draw(ctx, x, FLOOR - 186 * KK, KK, -1, BOY, p)
    hx0, hy0 = b['head']
    teddy(ctx, hx0, hy0 - 470 + 10 * math.sin(il * 0.6), 2.4, 0.08 * math.sin(il * 0.4))
    if stop:
        for k in range(4):
            sparkle(ctx, hx0 - 250 + k * 170, hy0 - 680 + (k % 2) * 60, 22 + 6 * math.sin(il * 0.5 + k), YEL)
    ctx.restore()
    label2(ctx, "\"DON'T FORGET", "MR. FLUFFY!!\"", WHITE, pop(il, 6, 10), 100, col2=YEL, y=1420)


def dad_twitch(ctx, f, il):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.1 * eout(pop(il, 0, 20)), 0, 2, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('5a3aa8')); ctx.fill()
    rays(ctx, 540, 900, 260, 1500, il * 0.02, col=(0.8, 0.6, 1), a=0.25, n=16)
    face(ctx, DAD, P(eye='shock', mouth='flat'), 540, 900, 300, 0)
    twitch(ctx, 540 + 0.62 * 300, 900 - 0.78 * 300, il, 1.5)
    sweat(ctx, 540 - 330, 860, il, 1.3)
    ctx.restore()
    label(ctx, "*twitch*", 540, 1440, 100, WHITE, 0.04, pop(il, 4, 7))


def rear_car(ctx, f, il, z=1.06, shake=0, bulge=0.0, squash=0.0, cy=1060):
    ctx.save(); cam(ctx, 560, cy, z, 0, shake, f)
    driveway_bg(ctx, il)
    ctx.save(); ctx.translate(0, FLOOR); ctx.scale(1, 1 - squash); ctx.translate(0, -FLOOR)
    car63(ctx, 640, FLOOR, 1.0, False, False)
    # paw + suitcase corner stuck in the hatch seam
    ellipse(ctx, 712, 1260, 30, 22); fl(ctx, hx('c98a52'), 6)
    rect_r(ctx, 708, 1310, 60, 30, 8); fl(ctx, RED, 6)
    if bulge > 0:
        ctx.new_path(); ctx.move_to(610, 1070); ctx.curve_to(700 + 60 * bulge, 1110, 760 + 70 * bulge, 1300, 720, 1400)
        ink(ctx, 8); ctx.stroke()
    ctx.restore()
    return


def s3(ctx, f):
    lf = f - 200
    if lf < 50:
        kid_run(ctx, f, lf)
    elif lf < 72:
        dad_twitch(ctx, f, lf - 50)
    else:
        il = lf - 72   # 0..68
        if il < 40:
            b = abs(math.sin(il * 0.32))
            rear_car(ctx, f, il, squash=0.07 * (1 - b), shake=4)
            p = sit(torso=-6, eye='glare', mouth='grin', lsh=160, lel=10, rsh=-160, rel=-10)
            draw_hip(ctx, 640, 1060 - 70 * b, DK, -1, DAD, p)
            ctx.restore()
            label(ctx, "*BOING! BOING!*", 540, 460, 100, YEL, -0.04, pop(il, 2, 5))
        else:
            jl = il - 40
            rear_car(ctx, f, jl, shake=shake_at(jl, [0], 10, 22))
            for k in range(5):
                sparkle(ctx, 300 + k * 110, 980 + (k % 2) * 60, 20 + 6 * math.sin(jl * 0.5 + k), YEL)
            draw(ctx, 330, FLOOR - 186 * DK, DK, 1, DAD, P(eye='happy', mouth='grin', lsh=160, lel=20, rsh=-160, rel=-20))
            ctx.restore()
            label(ctx, "*SLAM!*", 540, 460, 120, WHITE, 0.04, pop(jl, 0, 3))
            label(ctx, "\"DONE!!\"", 540, 1440, 130, GREEN, -0.03, pop(jl, 6, 9))


# ------------------------------------------------------------------ twist
FLY = [(c, random.Random(i).uniform(170, 640), random.Random(i + 50).uniform(-0.6, 0.6)) for i, c in enumerate(range(10))]


def s4(ctx, f):
    lf = f - 340
    if lf < 60:
        il = lf
        bulge = clamp((il - 34) / 20)
        rear_car(ctx, f, il, bulge=bulge, shake=3 * bulge + (2 if il >= 34 else 0))
        draw(ctx, 330, FLOOR - 186 * DK, DK, 1, DAD, P(eye='happy' if il < 34 else 'shock', mouth='grin' if il < 34 else 'wavy', lsh=-20, rsh=20))
        mx = lerp(1250, 900, eout(pop(il, 0, 16)))
        mp = P(eye='happy', mouth='smile', rsh=-150, rel=-20) if il < 22 else P(eye='happy', mouth='smile', rsh=-20)
        draw(ctx, mx, FLOOR - 186 * 1.3, 1.3, -1, MOM, mp)
        sy = lerp(800, 1062, eout(pop(il, 18, 28))) if il >= 18 else 800
        sxx = lerp(mx - 120, 600, eout(pop(il, 18, 28))) if il >= 18 else mx - 120
        shades(ctx, sxx, sy - 14, 0.9, 0.1)
        ctx.restore()
        label2(ctx, "\"Oh! And my", "SUNGLASSES.\"", WHITE, pop(il, 4, 8), 100, col2=PINK, y=1420) if il < 34 else None
        if il >= 34:
            label(ctx, "*CREEEAK...*", 540, 460, 100, YEL, 0.03 * math.sin(il), pop(il, 34, 37))
    else:
        il = lf - 60   # 0..80
        ctx.save(); cam(ctx, 560, 1000, 0.92, 0, shake_at(il, [0, 34], 14, 30), f)
        driveway_bg(ctx, il)
        car63(ctx, 640, FLOOR, 1.0, True, False)
        # Dad + falling pile
        buried = il >= 30
        if not buried:
            draw(ctx, 330, FLOOR - 186 * DK, DK, 1, DAD, P(eye='shock', mouth='scream', lsh=150, rsh=-150))
        pile = []
        for i in range(10):
            st = 2 + i * 2
            t = clamp((il - st) / 26)
            px = 200 + (i % 4) * 85 + (i // 4) * 40; py = FLOOR - 70 - (i // 4) * 110 - (i % 2) * 20
            if t <= 0:
                continue
            x = lerp(720, px, t)
            y = lerp(1250, py, t) - 1500 * 4 * t * (1 - t)
            a = (1 - t) * 8 * FLY[i][2] + (0.2 * FLY[i][2] if t >= 1 else 0)
            suitcase(ctx, x, y, 170, 110, SUITC[i % 8], a)
        if buried:
            # thumbs-up hand poking out of the top of the pile
            hy = FLOOR - 380 - 20 * eout(pop(il, 44, 52))
            if il >= 44:
                rect_r(ctx, 200, hy, 54, 120, 20); fl(ctx, DAD['shirt'], 6)
                ellipse(ctx, 227, hy - 10, 40, 34); fl(ctx, DAD['skin'], 6)
                rect_r(ctx, 214, hy - 70, 24, 52, 12); fl(ctx, DAD['skin'], 5)
        tt = clamp((il - 26) / 30)
        if tt > 0:
            ty = lerp(-300, FLOOR - 500, eout(tt)) if il < 56 else FLOOR - 500
            teddy(ctx, 450, ty, 1.5, 0.3 * (1 - tt))
            if il >= 56:
                shades(ctx, 450, ty - 10, 0.9, 0.05)
        ctx.restore()
        label(ctx, "*KA-BOOOOM!!*", 540, 440, 130, RED, -0.05, pop(il, 0, 3))
        if il >= 52:
            label(ctx, "\"...ALMOST.\"", 540, 1440, 120, WHITE, 0.03, pop(il, 52, 55))


# ------------------------------------------------------------------ end
def road_shot(ctx, f, il):
    bump = 6 * abs(math.sin(il * 0.5))
    zt = eio(pop(il, 20, 70))
    ctx.save(); cam(ctx, lerp(540, 600, zt), lerp(960, 1000, zt), lerp(1.0, 1.45, zt), 0, 3, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, SKY); ctx.fill()
    for k in range(-2, 8):
        hx0 = (k * 300 - il * 6) % 2100 - 400
        ellipse(ctx, hx0, 1060, 220, 160); setc(ctx, hx('6fd86a')); ctx.fill()
    ctx.rectangle(-500, 1100, 2200, 900); setc(ctx, hx('6a6e7e')); ctx.fill()
    ctx.move_to(-500, 1100); ctx.line_to(1700, 1100); ink(ctx, 7); ctx.stroke()
    for k in range(-2, 12):
        xx = (k * 260 - il * 40) % 2600 - 400
        ctx.rectangle(xx, 1560, 140, 22); setc(ctx, WHITE); ctx.fill()
    for k in range(6):
        yy = 600 + k * 120
        xx = 1000 + (k * 97 + il * 50) % 300
        ctx.move_to(xx, yy); ctx.line_to(xx + 160, yy)
    setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(8); ctx.stroke()
    G = 1380 - bump
    S = 1.25
    cx = 860
    # people in the windows (drawn before the car body is drawn on top? draw after with window clip)
    car63(ctx, cx, G, S, False, False)
    # front window: Mr. Fluffy with shades + seatbelt
    fxw = cx - 315 * S; fyw = G - 310 * S
    ctx.save(); poly(ctx, [(cx - 430 * S, G - 255 * S), (cx - 320 * S, G - 365 * S), (cx - 200 * S, G - 365 * S), (cx - 200 * S, G - 255 * S)]); ctx.clip()
    teddy(ctx, fxw, fyw + 40, 1.0, 0.0)
    shades(ctx, fxw, fyw + 32, 0.75)
    ctx.move_to(fxw - 70, fyw - 10); ctx.line_to(fxw + 60, fyw + 140); setc(ctx, hx('2a2840')); ctx.set_line_width(14); ctx.stroke()
    ctx.restore()
    # rear window: Dad squished by a suitcase
    rxw = cx - 85 * S; ryw = G - 310 * S
    ctx.save(); poly(ctx, [(cx - 175 * S, G - 255 * S), (cx - 175 * S, G - 365 * S), (cx - 50 * S, G - 365 * S), (cx + 20 * S, G - 255 * S)]); ctx.clip()
    ctx.rectangle(cx - 200 * S, G - 380 * S, 260 * S, 140 * S); setc(ctx, hx('bfe8ff')); ctx.fill()
    ctx.save(); ctx.translate(rxw - 10, ryw + 10); ctx.scale(1.25, 0.8)
    face(ctx, DAD, P(eye='closed', mouth='wavy'), 0, 0, 62, 0.15)
    ctx.restore()
    suitcase(ctx, rxw + 85, ryw - 5, 120, 150, PURPLE, -0.3)
    ctx.restore()
    # luggage tower on the roof, tied down
    roof = G - 390 * S
    ctx.save(); ctx.translate(cx - 185 * S, roof); ctx.rotate(0.04 * math.sin(il * 0.3))
    yy = 0
    for k, (w, h) in enumerate([(380, 100), (320, 110), (340, 90), (260, 100), (220, 90)]):
        suitcase(ctx, ((k % 2) * 2 - 1) * 12, yy - h / 2 - 8, w, h, SUITC[(k + 3) % 8], 0.03 * ((k % 3) - 1))
        yy -= h + 4
    beach_ball(ctx, 0, yy - 50, 50, il * 0.1)
    for sx in (-120, 120):
        ctx.move_to(sx, 0); ctx.line_to(sx * 0.6, yy + 30)
    setc(ctx, hx('8a5a2a')); ctx.set_line_width(9); ctx.stroke()
    ctx.restore()
    ctx.restore()
    label2(ctx, "MR. FLUFFY GOT", "THE FRONT SEAT.", WHITE, pop(il, 4, 8), 88, col2=GOLD, y=1430)


def mom_snacks(ctx, f, il):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eout(pop(il, 0, 30)), 0, 3, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('3a8bd8')); ctx.fill()
    rays(ctx, 540, 900, 260, 1500, il * 0.02, col=(0.8, 0.95, 1), a=0.25, n=16)
    suitcase(ctx, 140, 1150, 260, 380, ORANGE, 0.2)
    suitcase(ctx, 950, 1100, 240, 360, GREEN, -0.2)
    face(ctx, MOM, P(eye='normal', mouth='open'), 540, 880, 290, 0.05)
    ctx.restore()
    label2(ctx, "\"...honey? Where", "are the SNACKS?\"", WHITE, pop(il, 2, 6), 96, col2=YEL, y=1420)


def s5(ctx, f):
    lf = f - 480
    if lf < 90:
        road_shot(ctx, f, lf)
    elif lf < 132:
        mom_snacks(ctx, f, lf - 90)
    else:
        s1(ctx, f, f - 612)


SHOTS = [(0, s1), (54, s2), (200, s3), (340, s4), (480, s5)]
CUTS = (54, 110, 200, 250, 272, 312, 340, 400, 480, 570, 612)


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
                              "-i", "out/it_will_fit_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
