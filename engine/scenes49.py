"""'Who Left the Lights On?' - original, general-audience comedy short, 22s.
Hook: ECU Dad, red-faced, eye twitching, waving the bill: "WHO LEFT ALL THE LIGHTS ON?!"
Insert: the electric bill unrolls down to the floor -> TOTAL: $$$$
Beat 1: dollhouse cross-section of the house, every room blazing. Dad zips room to room at super speed: CLICK CLICK CLICK, dark.
 Kid reading in bed -> CLICK -> only his eyes: "I WAS READING!" / Dad: "Read FASTER."
Beat 2: Dad climbs INTO the fridge to check if the light really goes off. Door shuts. Dark: "...it DOES go off."
Beat 3: dinner in pitch black, only eyes + one candle. Dad: "See? COZY!" Kid: "That's MY hand."
Twist: December 1st - Dad plugs in his holiday lights: the house becomes a blinding star, the meter spins and smokes.
 Mom + kid in sunglasses: "WHO LEFT THE LIGHTS ON?" Dad: "That's DIFFERENT!" -> new bill arrives -> opening face (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos
from scenes48 import plug, label1, label2
import scenes13
from scenes13 import card as _card13
import random

BOY = dict(doodle.BOY, hood=False)
DAD = doodle.DAD
MOM = doodle.MOM_G
N = 660
FLOOR = 1460
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
NIGHT = hx('141a33')
LY = 1400

CAPS = {
    'p1': [[("WHEN DAD SEES", OUT)], [("THE ELECTRIC BILL", RED)]],
    'p2': [[("OPERATION:", OUT)], [("LIGHTS OFF", BLUE)]],
    'p3': [[("LEVEL 2:", OUT)], [("THE FRIDGE LIGHT", ORANGE)]],
    'p4': [[("DINNER TIME...", PURPLE)]],
    'p5': [[("DECEMBER 1st:", OUT)], [("DAD'S HOLIDAY LIGHTS", GREEN)]],
}
scenes13.CAPS = CAPS
card = _card13
BULBS = (hx('ff3b5c'), hx('ffd23f'), hx('3ccf4e'), hx('1f8bff'), hx('ff5fa8'), hx('ff8a1f'))


# ------------------------------------------------------------------ props
def bill(ctx, x, y, w, length, a=0.0):
    """long receipt hanging from (x, y), unrolled to `length`"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ctx.new_path(); ctx.move_to(-w / 2, 0); ctx.line_to(w / 2, 0); ctx.line_to(w / 2, length)
    for k in range(10):
        ctx.line_to(w / 2 - (k + 0.5) * w / 10, length + (14 if k % 2 == 0 else 0))
    ctx.line_to(-w / 2, length); ctx.close_path(); fl(ctx, (1, 1, 1), 7)
    rnd = random.Random(3)
    yy = 70
    while yy < length - 200:
        ctx.rectangle(-w / 2 + 30, yy, w * rnd.uniform(0.3, 0.5), 14); setc(ctx, hx('b8b8c8')); ctx.fill()
        ctx.rectangle(w / 2 - 30 - w * 0.18, yy, w * 0.18, 14); setc(ctx, hx('b8b8c8')); ctx.fill()
        yy += 46
    if length > 300:
        text(ctx, "TOTAL:", 0, length - 140, w * 0.17, OUT, outline=(1, 1, 1), ow=4, shadow=False)
        text(ctx, "$$$$$", 0, length - 50, w * 0.25, RED, ow=8, shadow=False)
    ctx.restore()


def bulb(ctx, x, y, r, on, col=hx('fff3a0')):
    if on:
        ellipse(ctx, x, y, r * 2.6, r * 2.6); setc(ctx, col + (0.25,)); ctx.fill()
    ellipse(ctx, x, y, r, r * 1.2); fl(ctx, col if on else hx('5a5a6a'), max(3, r * 0.2))


def switch(ctx, x, y, on, s=1.0):
    rect_r(ctx, x - 26 * s, y - 40 * s, 52 * s, 80 * s, 8 * s); fl(ctx, (1, 1, 1), 5)
    rect_r(ctx, x - 10 * s, y + (-30 if on else 2) * s, 20 * s, 28 * s, 5 * s); fl(ctx, hx('d8d8e0'), 4)


ROOMS = [  # x0, y0, w, h, lit colour, kind
    (80, 560, 450, 440, hx('ffe27a'), 'bath'),
    (550, 560, 450, 440, hx('9ee6ff'), 'bed'),
    (80, 1020, 450, 440, hx('ffb38a'), 'tv'),
    (550, 1020, 450, 440, hx('b7f07a'), 'kitchen'),
]


def room_props(ctx, x0, y0, w, h, kind, on):
    d = 1.0 if on else 0.45
    c = lambda col: dark(col, d) if not on else col
    fy = y0 + h
    if kind == 'bath':
        rect_r(ctx, x0 + 40, fy - 150, 260, 130, 50); fl(ctx, c((1, 1, 1)), 7)
        ctx.rectangle(x0 + 330, fy - 230, 90, 210); fl(ctx, c(hx('dfe9ff')), 6)
    elif kind == 'bed':
        rect_r(ctx, x0 + 40, fy - 140, 340, 120, 20); fl(ctx, c(hx('ff7aa8')), 7)
        rect_r(ctx, x0 + 50, fy - 175, 110, 60, 20); fl(ctx, c((1, 1, 1)), 6)
    elif kind == 'tv':
        rect_r(ctx, x0 + 40, fy - 300, 240, 160, 12); fl(ctx, c(hx('2a2a3a')), 7)
        ctx.rectangle(x0 + 55, fy - 285, 210, 130); setc(ctx, c(hx('5fd0ff')) if on else hx('0c0c14')); ctx.fill()
        rect_r(ctx, x0 + 20, fy - 120, 300, 100, 20); fl(ctx, c(hx('8a3cff')), 7)
    else:
        rect_r(ctx, x0 + 260, fy - 330, 150, 310, 14); fl(ctx, c((1, 1, 1)), 7)
        ctx.rectangle(x0 + 30, fy - 160, 200, 140); fl(ctx, c(hx('c96a2a')), 7)


def dollhouse(ctx, lit, lf):
    """cross-section of the house; lit = list of 4 bools"""
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, NIGHT); ctx.fill()
    rnd = random.Random(5)
    for k in range(40):
        sparkle(ctx, rnd.uniform(-100, 1180), rnd.uniform(-200, 500), rnd.uniform(5, 12) * (0.7 + 0.3 * math.sin(lf * 0.2 + k)), (1, 1, 0.85))
    poly(ctx, [(30, 560), (540, 250), (1050, 560)]); fl(ctx, hx('c84a3a'), 10)
    rect_r(ctx, 60, 540, 960, 940, 6); fl(ctx, hx('8a5a3a'), 10)
    for (x0, y0, w, h, col, kind), on in zip(ROOMS, lit):
        ctx.rectangle(x0, y0, w, h); setc(ctx, col if on else hx('202848')); ctx.fill()
        ctx.rectangle(x0, y0 + h - 16, w, 16); setc(ctx, dark(col if on else hx('202848'), 0.8)); ctx.fill()
        room_props(ctx, x0, y0, w, h, kind, on)
        ctx.move_to(x0 + w / 2, y0); ctx.line_to(x0 + w / 2, y0 + 60); ink(ctx, 5); ctx.stroke()
        bulb(ctx, x0 + w / 2, y0 + 80, 22, on)
        switch(ctx, x0 + w - 50, y0 + 220, on, 0.8)
        ctx.rectangle(x0, y0, w, h); ink(ctx, 8); ctx.stroke()


def fridge(ctx, x, y, w, h, door, glow=1.0):
    """fridge with bottom-left at (x, y+h); door 0 closed .. 1 open (swings to the right)"""
    rect_r(ctx, x, y, w, h, 24); fl(ctx, hx('eef4ff'), 9)
    ctx.save(); rect_r(ctx, x + 18, y + 18, w - 36, h - 36, 14); ctx.clip()
    ctx.rectangle(x, y, w, h); setc(ctx, hx('fffbe0') if glow > 0 else hx('1a1d30')); ctx.fill()
    for k in range(1, 4):
        ctx.rectangle(x + 18, y + k * h / 4, w - 36, 12); setc(ctx, hx('c8d8e8')); ctx.fill()
    if glow > 0:
        ellipse(ctx, x + w / 2, y + 60, 40, 26); setc(ctx, (1, 1, 0.7)); ctx.fill()
        rays(ctx, x + w / 2, y + 60, 40, 260, 0, col=(1, 1, 0.75), a=0.35 * glow, n=12)
    # food
    ellipse(ctx, x + 90, y + h / 4 - 40, 50, 40); fl(ctx, hx('ff5a5a'), 6)
    rect_r(ctx, x + 180, y + h / 4 - 120, 60, 120, 10); fl(ctx, hx('ffffff'), 6)
    ellipse(ctx, x + w - 100, y + h / 2 - 40, 60, 40); fl(ctx, hx('ffd23f'), 6)
    ctx.restore()
    # light button on the side
    rect_r(ctx, x + w - 34, y + 120, 16, 50, 4); fl(ctx, hx('ffffff'), 4)
    # door
    dw = w * (1 - door) + 40 * door
    if door < 1:
        rect_r(ctx, x, y, dw, h, 24); fl(ctx, hx('dfe9f8'), 9)
        ctx.rectangle(x + dw - 60 * (1 - door) - 20, y + 160, 22, 260); fl(ctx, hx('9aa8c0'), 6)
    else:
        poly(ctx, [(x + w, y), (x + w + 200, y - 50), (x + w + 200, y + h + 50), (x + w, y + h)]); fl(ctx, hx('dfe9f8'), 9)


def candle(ctx, x, y, lf, s=1.0):
    ellipse(ctx, x, y - 70 * s, 120 * s, 140 * s); setc(ctx, (1, 0.8, 0.3, 0.18)); ctx.fill()
    ctx.rectangle(x - 18 * s, y - 40 * s, 36 * s, 90 * s); fl(ctx, (1, 1, 1), 5)
    fx = 4 * math.sin(lf * 0.9) * s
    poly(ctx, [(x + fx, y - 100 * s), (x + 14 * s, y - 52 * s), (x, y - 40 * s), (x - 14 * s, y - 52 * s)]); fl(ctx, hx('ffb83a'), 4)


def dark_eyes(ctx, x, y, s, kind='normal', look=0.0, blink_=False):
    for dx in (-1, 1):
        ex = x + dx * 44 * s
        if blink_:
            ctx.move_to(ex - 26 * s, y); ctx.line_to(ex + 26 * s, y); setc(ctx, (1, 1, 1)); ctx.set_line_width(7 * s); ctx.stroke(); continue
        ellipse(ctx, ex, y, 30 * s, 38 * s); setc(ctx, (1, 1, 1)); ctx.fill()
        ellipse(ctx, ex + look * 12 * s, y + 6 * s, 13 * s, 16 * s); setc(ctx, INK); ctx.fill()
        if kind == 'glare':   # angry brows
            ctx.move_to(ex - 34 * s * dx, y - 52 * s); ctx.line_to(ex + 34 * s * dx, y - 30 * s)
            setc(ctx, (1, 1, 1)); ctx.set_line_width(9 * s); ctx.stroke()
            ctx.rectangle(ex - 34 * s, y - 40 * s, 68 * s, 12 * s); setc(ctx, (0, 0, 0)); ctx.fill()


def grin_dark(ctx, x, y, s):
    ctx.new_path(); ctx.arc(x, y, 60 * s, 0.15 * math.pi, 0.85 * math.pi); ctx.close_path()
    setc(ctx, (1, 1, 1)); ctx.fill()


def shades(ctx, cx, cy, Rt, f_=1):
    (x1, y1, r1), (x2, y2, r2) = eye_pos(cx, cy, Rt, f_)
    for ex, ey in ((x1, y1), (x2, y2)):
        rect_r(ctx, ex - 0.26 * Rt, ey - 0.14 * Rt, 0.52 * Rt, 0.3 * Rt, 0.1 * Rt); fl(ctx, hx('111122'), Rt * 0.03)
        ctx.move_to(ex - 0.14 * Rt, ey - 0.06 * Rt); ctx.line_to(ex - 0.02 * Rt, ey - 0.06 * Rt); setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(Rt * 0.03); ctx.stroke()
    ctx.move_to(x1 + 0.26 * Rt, y1); ctx.line_to(x2 - 0.26 * Rt, y2); ink(ctx, Rt * 0.04); ctx.stroke()


def light_string(ctx, pts, lf, s=1.0, on=True):
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    setc(ctx, hx('1d3a1d')); ctx.set_line_width(4 * s); ctx.stroke()
    k = 0
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        L = math.hypot(bx - ax, by - ay); n = max(1, int(L / (34 * s)))
        for j in range(n):
            u = j / n; col = BULBS[(k + int(lf / 4)) % len(BULBS)]
            x, y = lerp(ax, bx, u), lerp(ay, by, u)
            if on:
                ellipse(ctx, x, y + 8 * s, 18 * s, 18 * s); setc(ctx, col + (0.3,)); ctx.fill()
            ellipse(ctx, x, y + 8 * s, 8 * s, 11 * s); setc(ctx, col if on else hx('444455')); ctx.fill()
            k += 1


def house_ext(ctx, lf, lit=0.0):
    """exterior at night; lit 0..1 = holiday lights blast"""
    sky = hx('141a33')
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, sky); ctx.fill()
    if lit > 0:
        ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, (1, 0.95, 0.75, 0.35 * lit)); ctx.fill()
        rays(ctx, 540, 850, 200, 2200, lf * 0.03, col=(1, 0.97, 0.7), a=0.45 * lit, n=20)
    rnd = random.Random(8)
    for k in range(30):
        sparkle(ctx, rnd.uniform(-100, 1180), rnd.uniform(-100, 600), rnd.uniform(5, 11), (1, 1, 0.85))
    ctx.rectangle(-3000, 1360, 7000, 2000); setc(ctx, hx('2e6b3a') if lit == 0 else hx('5fbf5a')); ctx.fill()
    ctx.move_to(-3000, 1360); ctx.line_to(4000, 1360); ink(ctx, 8); ctx.stroke()
    # house
    poly(ctx, [(170, 900), (540, 600), (910, 900)]); fl(ctx, hx('c84a3a'), 10)
    ctx.rectangle(220, 900, 640, 460); fl(ctx, hx('e8c48a'), 10)
    wins = [(270, 960), (650, 960)]
    for wx, wy in wins:
        ctx.rectangle(wx, wy, 160, 150); fl(ctx, hx('fff3a0') if lit > 0 else hx('22284a'), 8)
        ctx.move_to(wx + 80, wy); ctx.line_to(wx + 80, wy + 150); ctx.move_to(wx, wy + 75); ctx.line_to(wx + 160, wy + 75); ink(ctx, 6); ctx.stroke()
    rect_r(ctx, 480, 1130, 120, 230, 10); fl(ctx, hx('8a3cff'), 8)
    # bush / tree at right
    poly(ctx, [(990, 1060), (930, 1220), (1050, 1220)]); fl(ctx, hx('1f8a4a'), 7)
    poly(ctx, [(990, 1140), (910, 1340), (1070, 1340)]); fl(ctx, hx('1f8a4a'), 7)
    if lit > 0:
        light_string(ctx, [(170, 900), (540, 600), (910, 900)], lf)
        light_string(ctx, [(220, 900), (860, 900)], lf + 2)
        light_string(ctx, [(220, 900), (220, 1360)], lf + 1)
        light_string(ctx, [(860, 900), (860, 1360)], lf + 3)
        for wx, wy in wins:
            light_string(ctx, [(wx, wy), (wx + 160, wy), (wx + 160, wy + 150), (wx, wy + 150), (wx, wy)], lf + wx, 0.8)
        light_string(ctx, [(480, 1130), (600, 1130), (600, 1360)], lf + 5, 0.8)
        light_string(ctx, [(960, 1110), (1030, 1180), (930, 1260), (1060, 1330)], lf + 7, 0.8)
        # star on the roof
        sparkle(ctx, 540, 560, 70 + 10 * math.sin(lf * 0.5), hx('fff27a'))


def meter(ctx, cx, cy, R, lf, speed):
    ellipse(ctx, cx, cy, R + 40, R + 40); fl(ctx, hx('6a7a8a'), 9)
    ellipse(ctx, cx, cy, R, R); fl(ctx, (1, 1, 1), 7)
    for k in range(12):
        a = k * math.pi / 6
        ctx.move_to(cx + math.cos(a) * R * 0.82, cy + math.sin(a) * R * 0.82); ctx.line_to(cx + math.cos(a) * R * 0.95, cy + math.sin(a) * R * 0.95)
    ink(ctx, 6); ctx.stroke()
    a = lf * speed
    for j in range(4 if speed > 0.5 else 1):   # motion blur ghosts
        aa = a - j * 0.25
        ctx.move_to(cx, cy); ctx.line_to(cx + math.cos(aa) * R * 0.8, cy + math.sin(aa) * R * 0.8)
        setc(ctx, RED + ((1.0 if j == 0 else 0.25),)); ctx.set_line_width(16); ctx.stroke()
    ellipse(ctx, cx, cy, 22, 22); fl(ctx, INK, 4)
    rect_r(ctx, cx - 160, cy + R * 0.35, 320, 70, 10); fl(ctx, hx('1d1d2a'), 5)
    digits = str(int(10000 + lf * lf * 9 * speed))[-6:]
    text(ctx, digits, cx, cy + R * 0.35 + 52, 54, hx('7aff8a'), ow=0, shadow=False)


# ------------------------------------------------------------------ opening
def opening_face(ctx, f, lf, lab=True):
    """ECU: Dad, red, eye twitching, bill in hand"""
    sh = shake_at(lf, [0, 14], 10, 20)
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 40)), 0, sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff4f6a')); ctx.fill()
    rays(ctx, 540, 900, 240, 1700, lf * 0.05, col=(1, 0.95, 0.5), a=0.35, n=18)
    cx, cy, R = 540, 880, 300
    face(ctx, DAD, P(eye='glare', mouth='scream', head=0), cx, cy, R, 0.04 * math.sin(lf * 1.4))
    # twitching eye: a flicking lower lid line
    if (lf // 3) % 2 == 0:
        (ex, ey, rx), _ = eye_pos(cx, cy, R)
        ctx.move_to(ex - rx * 1.2, ey + rx * 1.1); ctx.line_to(ex + rx * 1.2, ey + rx * 0.8); ink(ctx, 8); ctx.stroke()
    # steam puffs
    for k, x in enumerate((240, 840)):
        t = ((lf + k * 9) % 18) / 18
        ellipse(ctx, x, cy - 260 - 120 * t, 40 + 50 * t, 40 + 50 * t); setc(ctx, (1, 1, 1, 0.8 * (1 - t))); ctx.fill()
    # the bill shaking in his fist, bottom right
    bill(ctx, 840, 1100, 180, 300, 0.25 + 0.05 * math.sin(lf * 2))
    ctx.restore()
    if lab:
        label2(ctx, "\"WHO LEFT ALL THE", "LIGHTS ON?!\"", (1, 1, 1), 1.0 if f < 56 else pop(lf, 0, 3), 104, col2=YEL)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 56:
        opening_face(ctx, f, f)
    else:
        lf = f - 56
        # insert: the bill unrolls ... and unrolls
        ctx.save(); cam(ctx, 540, 960, 1.0, 0, shake_at(lf, [30], 10, 16), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd23f')); ctx.fill()
        for i in range(-6, 16):
            ctx.rectangle(i * 140 + (lf * 4) % 140, -500, 60, 3000); setc(ctx, hx('ffe066')); ctx.fill()
        length = lerp(200, 1000, eout(pop(lf, 0, 28)))
        bill(ctx, 540, 520, 440, length, 0.0)
        ctx.restore()
        if lf < 28:
            label1(ctx, "*RRRRRRRRIP*", (1, 1, 1), pop(lf, 0, 4), 100, y=1440)
        else:
            sparkle(ctx, 300, 1250, 40); sparkle(ctx, 780, 1300, 50)
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 92:
        # dollhouse: Dad zips from room to room, clicking everything off
        order = [0, 1, 2, 3]
        per = 20
        idx = min(3, max(0, (lf - 8) // per))
        sub = (lf - 8) - idx * per
        lit = [True] * 4
        for j, r in enumerate(order):
            if lf - 8 >= j * per + 10:
                lit[r] = False
        ctx.save(); cam(ctx, 540, 1000, 1.02, 0, 3 if (lf >= 18 and (lf - 18) % per < 3) else 0, f)
        dollhouse(ctx, lit, lf)
        if lf >= 8:
            x0, y0, w, h, col, kind = ROOMS[order[idx]]
            dx = x0 + w - 130; fy = y0 + h - 16
            # speed lines from where he came from
            if sub < 6:
                for k in range(4):
                    ctx.move_to(dx - 60 - k * 10, fy - 200 + k * 40); ctx.rel_line_to(-200, 0)
                ctx.set_source_rgba(1, 1, 1, 0.8); ctx.set_line_width(8); ctx.stroke()
            p = P(torso=-4, lhip=-10, lkn=0, rhip=10, rkn=0, lsh=-20, lel=-20, rsh=-140 if sub >= 8 else -60, rel=-30,
                  eye='glare', mouth='grin', head=-4)
            draw(ctx, dx, fy - 186 * 0.95, 0.95, 1, DAD, p)
        ctx.restore()
        if lf >= 18:
            k = min(3, (lf - 18) // per)
            cl = (lf - 18) - k * per
            x0, y0, w, h, col, kind = ROOMS[order[k]]
            label(ctx, "CLICK!", x0 + w / 2, y0 + 170, 80, YEL, (-0.08 if k % 2 else 0.08), pop(cl, 0, 3))
        if lf >= 82:
            label1(ctx, "\"MUCH better.\"", (1, 1, 1), pop(lf, 82, 86), 104, y=1440)
    elif lf < 126:
        il = lf - 92
        # kid reading in bed with a lamp -> click -> darkness
        off = il >= 12
        ctx.save(); cam(ctx, 540, 1050, 1.1 + 0.05 * eout(pop(il, 12, 34)), 0, shake_at(il, [12], 8, 14), f)
        ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('9ee6ff') if not off else hx('080a18')); ctx.fill()
        if not off:
            rect_r(ctx, 140, 1180, 760, 260, 30); fl(ctx, hx('ff7aa8'), 9)
            face(ctx, BOY, P(eye='happy', mouth='smile', head=0), 470, 1010, 170, -0.1)
            rect_r(ctx, 360, 1080, 240, 170, 10); fl(ctx, hx('2f6bff'), 8)   # book
            ctx.move_to(480, 1080); ctx.line_to(480, 1250); ink(ctx, 6); ctx.stroke()
            ctx.rectangle(850, 920, 14, 260); fl(ctx, hx('3a3a4a'), 4)
            poly(ctx, [(790, 920), (930, 920), (900, 820), (820, 820)]); fl(ctx, hx('ffd23f'), 6)
            ctx.rectangle(-500, 1440, 2200, 500); setc(ctx, hx('c98a52')); ctx.fill()
            # Dad's hand coming in from the left with a pointing finger
            hx_ = lerp(-200, 40, eout(pop(il, 0, 10)))
            rect_r(ctx, hx_ - 300, 860, 300, 70, 30); fl(ctx, DAD['shirt'], 7)
            rect_r(ctx, hx_, 870, 90, 50, 25); fl(ctx, DAD['skin'], 6)
        else:
            dark_eyes(ctx, 470, 1010, 1.6, 'glare', 0.5)
        ctx.restore()
        if off:
            label2(ctx, "\"I WAS", "READING!!\"", (1, 1, 1), pop(il, 14, 18), 116, col2=YEL)
        else:
            label1(ctx, "*click*", YEL, pop(il, 10, 13), 110, y=1440)
    else:
        il = lf - 126
        # Dad in the dark: only his eyes + grin
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.04 * eout(pop(il, 0, 30)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('080a18')); ctx.fill()
        dark_eyes(ctx, 540, 860, 2.0, 'normal', -0.4)
        grin_dark(ctx, 540, 1000, 1.8)
        ctx.restore()
        label2(ctx, "\"Read", "FASTER.\"", (1, 1, 1), pop(il, 2, 6), 120, col2=YEL)
    card(ctx, 'p2', f, 112, 200)


def s3(ctx, f):
    lf = f - 270
    if lf < 70:
        # Dad suspicious at the open fridge, climbs in to check the light
        ctx.save(); cam(ctx, 540, 1060, 1.05 + 0.1 * eout(pop(lf, 0, 70)), 0, shake_at(lf, [52], 12, 22), f)
        ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('1d2c50')); ctx.fill()
        for i in range(-30, 40):
            ctx.rectangle(i * 120, -3000, 46, 6000); setc(ctx, dark(hx('1d2c50'), 0.9)); ctx.fill()
        ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('2a2040')); ctx.fill()
        ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()
        door = 1.0 if lf < 50 else 1 - eout(pop(lf, 50, 54))
        fx, fy, fw, fh = 330, 620, 420, 840
        # light spill on the floor
        if door > 0:
            poly(ctx, [(fx, FLOOR), (fx + fw, FLOOR), (fx + fw + 250, 2000), (fx - 250, 2000)]); setc(ctx, (1, 1, 0.7, 0.3 * door)); ctx.fill()
        if lf < 50:
            fridge(ctx, fx, fy, fw, fh, 1.0)
            if lf < 24:
                # Dad leaning in, poking the light, squinting
                p = P(torso=30, lhip=-10, lkn=0, rhip=10, rkn=0, lsh=-100, lel=-20, rsh=-60, rel=-40, eye='glare', mouth='flat', head=10)
                draw(ctx, fx + fw + 110, FLOOR - 186 * 1.35, 1.35, -1, DAD, p)
            else:
                # Dad climbing IN - only legs + bum sticking out, then fully in
                inn = eout(pop(lf, 24, 44))
                ctx.save(); rect_r(ctx, fx + 18, fy + 18, fw - 36, fh - 36, 14); ctx.clip()
                p = P(torso=-6, lhip=-30, lkn=-60, rhip=20, rkn=-80, lsh=-150, lel=-10, rsh=-120, rel=-30, eye='glare', mouth='flat', head=0)
                draw(ctx, fx + fw / 2, fy + 180, 1.1, 1, DAD, p)
                ctx.restore()
                if inn < 1:
                    # legs dangling out the front
                    lx = fx + fw / 2 + 30
                    for k in (-1, 1):
                        ctx.save(); ctx.translate(lx + k * 40, fy + fh - 80 - 200 * inn); ctx.rotate(0.3 * k + 0.2 * math.sin(lf * 0.8))
                        rect_r(ctx, -26, 0, 52, 240 * (1 - inn), 20); fl(ctx, DAD['pants'], 7)
                        rect_r(ctx, -36, 240 * (1 - inn) - 10, 80, 40, 16); fl(ctx, DAD['shoes'], 6)
                        ctx.restore()
        else:
            fridge(ctx, fx, fy, fw, fh, door, glow=1.0 if door > 0.3 else 0.0)
        ctx.restore()
        if lf < 24:
            label2(ctx, "\"Does it REALLY", "go off...?\"", (1, 1, 1), pop(lf, 2, 6), 100, col2=ORANGE)
        elif lf < 50:
            label1(ctx, "\"Only one way to know.\"", (1, 1, 1), pop(lf, 26, 30), 90, y=1440)
        else:
            label1(ctx, "*THUNK!*", YEL, pop(lf, 52, 55), 150, 0.04, y=1440)
    elif lf < 126:
        il = lf - 70
        # inside the closed fridge: pitch black, Dad's eyes + a lettuce
        ctx.save(); cam(ctx, 540, 960, 1.0, 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('05060c')); ctx.fill()
        ctx.rectangle(80, 640, 920, 14); setc(ctx, hx('1a2030')); ctx.fill()
        ctx.rectangle(80, 1240, 920, 14); setc(ctx, hx('1a2030')); ctx.fill()
        bl = 24 <= il < 28
        dark_eyes(ctx, 540, 930, 2.0, 'normal', 0.6 * math.sin(il * 0.15), blink_=bl)
        # frosty breath
        t = (il % 30) / 30
        ellipse(ctx, 620 + 60 * t, 1100 - 30 * t, 30 + 40 * t, 20 + 25 * t); setc(ctx, (0.8, 0.9, 1, 0.5 * (1 - t))); ctx.fill()
        ctx.restore()
        label2(ctx, "\"...it DOES", "go off.\"", (1, 1, 1), pop(il, 6, 10), 116, col2=hx('9ee6ff'))
        if il > 34:
            label1(ctx, "\"...Honey?\"", hx('9ee6ff'), pop(il, 34, 38), 90, 0.03, y=560)
    else:
        il = lf - 126
        # wide: Mom opens the fridge, frozen Dad with icicles, shiver
        ctx.save(); cam(ctx, 540, 1060, 1.08, 0, 4 if il < 10 else 0, f)
        ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('1d2c50')); ctx.fill()
        ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('2a2040')); ctx.fill()
        ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()
        fx, fy, fw, fh = 230, 620, 420, 840
        poly(ctx, [(fx, FLOOR), (fx + fw, FLOOR), (fx + fw + 250, 2000), (fx - 250, 2000)]); setc(ctx, (1, 1, 0.7, 0.3)); ctx.fill()
        fridge(ctx, fx, fy, fw, fh, 1.0)
        ctx.save(); rect_r(ctx, fx + 18, fy + 18, fw - 36, fh - 36, 14); ctx.clip()
        DADB = dict(DAD, skin=hx('a8d8ff'))
        draw(ctx, fx + fw / 2 + 6 * math.sin(il * 2.5), fy + 200, 1.1, 1, DADB,
             P(torso=0, lhip=-30, lkn=-60, rhip=20, rkn=-80, lsh=20, lel=-140, rsh=-20, rel=140, eye='shock', mouth='wavy', head=0))
        for k in range(6):
            poly(ctx, [(fx + 40 + k * 65, fy + 18), (fx + 60 + k * 65, fy + 18), (fx + 50 + k * 65, fy + 70 + 20 * (k % 2))]); fl(ctx, (0.85, 0.95, 1), 3)
        ctx.restore()
        draw(ctx, fx + fw + 290, FLOOR - 186 * 1.4, 1.4, -1, MOM,
             P(torso=0, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=-100, lel=-10, rsh=30, rel=-120, eye='glare', mouth='flat', head=0))
        ctx.restore()
        label2(ctx, "\"Saving", "ELECTRICITY.\"", (1, 1, 1), pop(il, 2, 6), 104, col2=hx('9ee6ff'))
    card(ctx, 'p3', f, 272, 340)


def s4(ctx, f):
    lf = f - 410
    # dinner in total darkness: eyes + a candle
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.12 * eout(pop(lf, 0, 90)), 1.5 * math.sin(lf * 0.04), 0, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('06070f')); ctx.fill()
    poly(ctx, [(120, 1240), (960, 1240), (1060, 1400), (20, 1400)]); setc(ctx, hx('1a1424')); ctx.fill()
    candle(ctx, 540, 1230, lf, 1.2)
    # Dad left, Mom right, kid middle-back
    dark_eyes(ctx, 230, 940, 1.1, 'normal', 0.3)
    if lf < 40:
        grin_dark(ctx, 230, 1050, 0.9)
    dark_eyes(ctx, 850, 940, 1.1, 'glare', -0.3)
    kid_y = 760
    dark_eyes(ctx, 540, kid_y, 0.9, 'normal', -1 if lf < 60 else 0.0, blink_=(lf % 40) < 3)
    if lf >= 60:
        # kid's fork stab -> Dad's hand
        ctx.move_to(540, 880); ctx.line_to(300, 1180); setc(ctx, (0.8, 0.8, 0.85)); ctx.set_line_width(10); ctx.stroke()
        for k in range(3):
            ctx.move_to(300 + k * 12, 1180); ctx.rel_line_to(-10, 40)
        ctx.stroke()
    ctx.restore()
    if lf < 40:
        label2(ctx, "\"See?", "COZY!\"", (1, 1, 1), pop(lf, 4, 8), 116, col2=YEL)
    elif lf < 60:
        label1(ctx, "\"Where's my FORK...?\"", (1, 1, 1), pop(lf, 40, 44), 92, y=1440)
    else:
        label1(ctx, "\"OWW! That's my HAND!\"", YEL, pop(lf, 60, 63), 92, 0.04, y=1440)
    card(ctx, 'p4', f, 412, 500)


def s5(ctx, f):
    lf = f - 500
    if lf < 60:
        # Dad on the lawn with the BIG plug... KA-CHUNK
        on = lf >= 30
        ctx.save(); cam(ctx, 540, 1000, 1.0 if not on else 1.0 + 0.06 * eout(pop(lf, 30, 60)), 0, shake_at(lf, [30], 14, 28), f)
        house_ext(ctx, lf, 1.0 if on else 0.0)
        p = P(torso=10, lhip=-10, lkn=0, rhip=10, rkn=0, lsh=-120, lel=-20, rsh=-90, rel=-10, eye='happy' if on else 'smug', mouth='grin', head=0)
        b = draw(ctx, 165, 1360 - 186 * 1.2, 1.2, 1, DAD, p)
        hx_, hy_ = b['front']
        rect_r(ctx, 228, 1210, 60, 80, 10); fl(ctx, hx('dddddd'), 5)   # outdoor socket on the wall
        px = lerp(hx_ + 40, 258, eout(pop(lf, 20, 30)))
        plug(ctx, px, 1250 - 50 * (1 - eout(pop(lf, 20, 30))), 1.57, 0.6)
        if on:
            for k in range(3):
                sparkle(ctx, 300 + k * 260, 760 + 80 * (k % 2), 50 * (1 - pop(lf, 30 + k * 3, 50)) + 1)
        ctx.restore()
        if not on:
            label1(ctx, "\"Just a FEW lights...\"", (1, 1, 1), pop(lf, 2, 6), 96, y=1450)
        else:
            label1(ctx, "*KA-CHUNK!*", YEL, pop(lf, 30, 33), 140, 0.04, y=1450)
        card(ctx, 'p5', f, 502, 590)
    elif lf < 92:
        il = lf - 60
        # the meter goes crazy
        ctx.save(); cam(ctx, 540, 940, 1.0 + 0.08 * eout(pop(il, 0, 32)), 0, 6 + il * 0.4, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('8a3cff')); ctx.fill()
        rays(ctx, 540, 940, 200, 1600, il * 0.1, col=(1, 0.95, 0.5), a=0.3, n=16)
        meter(ctx, 540, 900, 300, il, 0.9)
        for k in range(3):
            t = ((il + k * 8) % 24) / 24
            ellipse(ctx, 540 + (k - 1) * 160, 520 - 160 * t, 50 + 50 * t, 50 + 50 * t); setc(ctx, (0.3, 0.3, 0.35, 0.7 * (1 - t))); ctx.fill()
        ctx.restore()
        label1(ctx, "*WHIRRRRRRR*", YEL, pop(il, 0, 4), 120, 0.03, y=1440)
    elif lf < 125:
        il = lf - 92
        # split: Mom + kid in sunglasses (top) vs Dad grinning (bottom)
        ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
        ctx.rectangle(0, 0, W, 960); setc(ctx, hx('fff3a0')); ctx.fill()
        rays(ctx, 540, 600, 200, 1300, il * 0.05, col=(1, 1, 1), a=0.5, n=16)
        face(ctx, MOM, P(eye='normal', mouth='flat', head=0), 330, 600, 170, 0.0)
        shades(ctx, 330, 600, 170)
        face(ctx, BOY, P(eye='normal', mouth='flat', head=0), 760, 640, 140, 0.0)
        shades(ctx, 760, 640, 140)
        ctx.restore()
        label(ctx, "\"WHO LEFT", 540, 800, 92, (1, 1, 1), -0.02, pop(il, 0, 4))
        label(ctx, "THE LIGHTS ON?\"", 540, 900, 92, YEL, 0.02, pop(il, 0, 4))
        ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
        ctx.rectangle(0, 960, W, 960); setc(ctx, hx('22b45a')); ctx.fill()
        rnd = random.Random(1)
        for k in range(14):
            bulb(ctx, rnd.uniform(40, 1040), rnd.uniform(1000, 1500), 14, (k + il // 4) % 2 == 0, BULBS[k % 6])
        face(ctx, DAD, P(eye='happy', mouth='grin', head=0), 540, 1130, 180, 0.06 * math.sin(il * 0.4))
        ctx.restore()
        ctx.rectangle(0, 952, W, 16); setc(ctx, (1, 1, 1)); ctx.fill()
        if il >= 12:
            label2(ctx, "\"That's", "DIFFERENT!\"", (1, 1, 1), pop(il, 12, 16), 104, col2=YEL, y=1450)
    else:
        il = lf - 125
        # loop: the new bill arrives -> opening face
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 625)


SHOTS = [(0, s1), (110, s2), (270, s3), (410, s4), (500, s5)]
CUTS = (56, 110, 202, 236, 270, 340, 396, 410, 500, 560, 592, 625)


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
                              "-i", "out/lights_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
