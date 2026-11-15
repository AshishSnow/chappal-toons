"""'I'm Bored!' - original, general-audience comedy short, ~22s.
Hook: ECU of the kid, droopy half-lids, cheek squished on his fist, grey tick-tock background: "I'M BOOORED..."
 -> wide: a MOUNTAIN of toys behind him, Mom in the doorway: "YOU HAVE 100 TOYS!" - "...they're BORING."
Beat 1: Mom's ideas, 3 whip cuts: "READ A BOOK?" (kid flat on the floor, top-down) - "PLAY OUTSIDE?" (upside down off the bed)
 - "BUILD A FORT?" (kid melts down the wall). Every answer: "BORING."
Beat 2: Mom, calm: "Fine. Then help me with..." -> red lightning ECU: "...THE CHORES." -> kid's eyes pop, POOF:
 he is now playing with EVERY toy at super speed: juggling, rocket, race car. "I'M SO BUSY!!"
Beat 3: Mom leaves, door clicks shut - kid instantly drops everything: "...I'm bored." -> low-angle ECU, Mom is back
 with a mop and bucket: "I HEARD THAT."
Twist: kid mops the house at super speed while Mom lounges on the sofa with popcorn: "Ahh... I'm SO bored." (smug wink)
Loop: kid ECU, same droopy face: "I'M BOOORED..." -> loops to the opening."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos, lids, sofa_back, sofa_front, popcorn, SEAT, clock
from scenes8 import sit
from scenes14 import sweat
import scenes13
from scenes13 import card as _card13
import random

BOY = doodle.BOY
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
GREY = hx('9aa6c0')
LY = 1450

CAPS = {
    'p1': [[("WHEN THE KID SAYS", OUT)], [("\"I'M BORED\"", BLUE)]],
    'p2': [[("MOM'S IDEAS:", OUT)], [("ALL \"BORING\"", GREY)]],
    'p3': [[("THE MAGIC WORD:", OUT)], [("\"CHORES\"", RED)]],
    'p4': [[("MOM'S SUPERPOWER:", OUT)], [("SHE HEARS EVERYTHING", PURPLE)]],
    'p5': [[("PLOT TWIST:", OUT)], [("NOW MOM IS \"BORED\"", PINK)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def ball(ctx, x, y, r, col, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ellipse(ctx, 0, 0, r, r); fl(ctx, col, max(4, r * 0.1))
    ctx.save(); ellipse(ctx, 0, 0, r, r); ctx.clip()
    ctx.rectangle(-r, -r * 0.22, 2 * r, r * 0.44); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.restore(); ellipse(ctx, 0, 0, r, r); ink(ctx, max(4, r * 0.1)); ctx.stroke()
    ctx.restore()


def block(ctx, x, y, s, col, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    rect_r(ctx, -s / 2, -s / 2, s, s, s * 0.12); fl(ctx, col, max(4, s * 0.07))
    rect_r(ctx, -s * 0.3, -s * 0.3, s * 0.6, s * 0.6, s * 0.1); setc(ctx, light(col, 0.4)); ctx.fill()
    ctx.restore()


def teddy(ctx, x, y, s, a=0.0):
    C = hx('c98a52'); Cl = hx('f0c89a')
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ellipse(ctx, 0, 70, 70, 80); fl(ctx, C, 7)
    for sx in (-1, 1):
        ellipse(ctx, sx * 52, -48, 26, 26); fl(ctx, C, 7)
        ellipse(ctx, sx * 70, 70, 26, 40); fl(ctx, C, 7)
    ellipse(ctx, 0, 0, 62, 56); fl(ctx, C, 7)
    ellipse(ctx, 0, 16, 28, 20); fl(ctx, Cl, 5)
    ellipse(ctx, 0, 8, 9, 7); setc(ctx, INK); ctx.fill()
    for sx in (-1, 1):
        ellipse(ctx, sx * 22, -12, 7, 9); setc(ctx, INK); ctx.fill()
    ctx.restore()


def toy_car(ctx, x, y, s, col=RED, f=1):
    ctx.save(); ctx.translate(x, y); ctx.scale(s * f, s)
    rect_r(ctx, -90, -60, 180, 50, 16); fl(ctx, col, 6)
    rect_r(ctx, -50, -100, 90, 50, 14); fl(ctx, col, 6)
    rect_r(ctx, -38, -90, 30, 30, 6); setc(ctx, hx('bfe8ff')); ctx.fill()
    rect_r(ctx, 0, -90, 30, 30, 6); setc(ctx, hx('bfe8ff')); ctx.fill()
    for wx in (-55, 55):
        ellipse(ctx, wx, -8, 22, 22); fl(ctx, hx('2a2a3a'), 5)
        ellipse(ctx, wx, -8, 8, 8); setc(ctx, (0.8, 0.8, 0.85)); ctx.fill()
    ctx.restore()


def rocket(ctx, x, y, s, a=0.0, flame=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if flame > 0:
        poly(ctx, [(-22, 70), (0, 70 + 120 * flame), (22, 70)]); fl(ctx, ORANGE, 5)
        poly(ctx, [(-11, 70), (0, 70 + 70 * flame), (11, 70)]); setc(ctx, YEL); ctx.fill()
    for sx in (-1, 1):
        poly(ctx, [(sx * 30, 20), (sx * 60, 80), (sx * 30, 70)]); fl(ctx, RED, 5)
    ctx.new_path(); ctx.move_to(0, -110); ctx.curve_to(45, -70, 40, 40, 30, 70); ctx.line_to(-30, 70); ctx.curve_to(-40, 40, -45, -70, 0, -110); ctx.close_path(); fl(ctx, (1, 1, 1), 6)
    ellipse(ctx, 0, -20, 17, 17); fl(ctx, hx('6ad0ff'), 5)
    ctx.restore()


TOYCOL = (RED, BLUE, GREEN, ORANGE, PURPLE, PINK, hx('ffd23f'), hx('19b5a5'))


def toy_pile(ctx, cx, base, w, h, seed=3, scatter=0.0):
    """mound of toys, centred at cx, bottom at base"""
    rnd = random.Random(seed)
    items = []
    for k in range(70):
        u = rnd.uniform(-1, 1)
        top = base - h * (1 - u * u) ** 0.8
        y = rnd.uniform(top, base - 30)
        items.append((y, cx + u * w / 2, rnd.random(), rnd.uniform(-0.6, 0.6), rnd.choice(TOYCOL), rnd.uniform(0.75, 1.15)))
    items.sort()
    for y, x, kind, a, col, s in items:
        if scatter > 0:
            x += (x - cx) * 0.4 * scatter; y += 200 * scatter
        if kind < 0.42:
            block(ctx, x, y, 80 * s, col, a)
        elif kind < 0.7:
            ball(ctx, x, y, 44 * s, col, a)
        elif kind < 0.82:
            teddy(ctx, x, y - 30, 0.6 * s, a)
        elif kind < 0.92:
            toy_car(ctx, x, y + 30, 0.6 * s, col, 1 if a > 0 else -1)
        else:
            rocket(ctx, x, y, 0.55 * s, a)


def playroom(ctx, door=0.0, dark_=0.0):
    wall = hx('ffd36e')
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, wall); ctx.fill()
    for i in range(-20, 30):
        for j in range(-10, 30):
            ellipse(ctx, i * 130 + (j % 2) * 65, j * 120, 14, 14); setc(ctx, dark(wall, 0.92)); ctx.fill()
    # window with sun + cloud
    rect_r(ctx, 90, 600, 340, 380, 20); fl(ctx, hx('8fd8ff'), 9)
    ellipse(ctx, 330, 700, 50, 50); fl(ctx, YEL, 5)
    for dx, r in ((-40, 34), (0, 46), (44, 34)):
        ellipse(ctx, 200 + dx, 840, r, r * 0.8); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.move_to(260, 600); ctx.line_to(260, 980); ctx.move_to(90, 790); ctx.line_to(430, 790); ink(ctx, 8); ctx.stroke()
    # doorway at right
    rect_r(ctx, 780, 620, 300, 840, 10); fl(ctx, hx('fff2c0') if door > 0 else hx('d09040'), 9)
    if door > 0:
        poly(ctx, [(780, 620), (780 - 160 * door, 580), (780 - 160 * door, 1500), (780, 1460)]); fl(ctx, hx('c96a2a'), 8)
    else:
        rect_r(ctx, 790, 630, 280, 820, 8); fl(ctx, hx('c96a2a'), 8)
        ellipse(ctx, 820, 1050, 14, 14); fl(ctx, hx('ffd23f'), 4)
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('5ac8a8')); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()
    if dark_ > 0:
        ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, (0.1, 0.1, 0.2, dark_)); ctx.fill()


def mop(ctx, x, y, a, s=1.0, wig=0.0):
    """(x, y) = hand on the handle"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(0, -120); ctx.line_to(0, 420); setc(ctx, OUT); ctx.set_line_width(22); ctx.stroke()
    ctx.move_to(0, -120); ctx.line_to(0, 420); setc(ctx, hx('ff9f5a')); ctx.set_line_width(12); ctx.stroke()
    rect_r(ctx, -40, 410, 80, 30, 8); fl(ctx, BLUE, 5)
    for k in range(-5, 6):
        ctx.move_to(k * 10, 440); ctx.curve_to(k * 14, 480, k * 18 + 20 * wig, 510, k * 20 + 30 * wig, 540)
    setc(ctx, OUT); ctx.set_line_width(14); ctx.stroke_preserve(); setc(ctx, (0.95, 0.95, 0.9)); ctx.set_line_width(7); ctx.stroke()
    ctx.restore()


def bucket(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, -150, 95, math.pi, 2 * math.pi); ink(ctx, 9); ctx.stroke()
    poly(ctx, [(-100, -150), (100, -150), (80, 0), (-80, 0)]); fl(ctx, hx('ff3b8a'), 8)
    ellipse(ctx, 0, -150, 100, 20); fl(ctx, hx('8fd0ff'), 6)
    for k in range(3):
        ellipse(ctx, -40 + k * 40, -180 - 15 * (k % 2), 16, 16); fl(ctx, (1, 1, 1), 4)
    ctx.restore()


def book(ctx, x, y, s, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-120, -10), (0, 10), (0, -140), (-120, -160)]); fl(ctx, (1, 1, 1), 6)
    poly(ctx, [(120, -10), (0, 10), (0, -140), (120, -160)]); fl(ctx, (1, 1, 1), 6)
    for k in range(4):
        ctx.move_to(-100, -120 + k * 25); ctx.line_to(-20, -105 + k * 25); ctx.move_to(100, -120 + k * 25); ctx.line_to(20, -105 + k * 25)
    setc(ctx, GREY); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def bolt(ctx, x, y, s, col=YEL):
    poly(ctx, [(x, y), (x + 60 * s, y), (x + 20 * s, y + 110 * s), (x + 70 * s, y + 110 * s), (x - 20 * s, y + 280 * s), (x + 5 * s, y + 150 * s), (x - 45 * s, y + 150 * s)])
    fl(ctx, col, 7)


def bored_bg(ctx, lf, col=hx('7f8fb0')):
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, col); ctx.fill()
    for k in range(-6, 14):   # slow diagonal stripes
        x = k * 200 + (lf * 1.5) % 200
        poly(ctx, [(x, -200), (x + 90, -200), (x - 900, 2400), (x - 990, 2400)]); setc(ctx, dark(col, 0.93)); ctx.fill()


def fist_chin(ctx, cx, cy, Rt, ch=BOY):
    """fist propping the cheek (from below-left)"""
    ctx.save()
    rect_r(ctx, cx - 0.55 * Rt, cy + 0.75 * Rt, 0.42 * Rt, 1.6 * Rt, 0.2 * Rt); fl(ctx, ch['shirt'], Rt * 0.03)
    ellipse(ctx, cx - 0.32 * Rt, cy + 0.72 * Rt, 0.3 * Rt, 0.26 * Rt); fl(ctx, ch['skin'], Rt * 0.03)
    for k in range(3):
        ctx.move_to(cx - 0.5 * Rt + k * 0.13 * Rt, cy + 0.55 * Rt); ctx.line_to(cx - 0.47 * Rt + k * 0.13 * Rt, cy + 0.68 * Rt)
    ink(ctx, Rt * 0.02); ctx.stroke()
    ctx.restore()


def ghost(ctx, a, fn):
    ctx.push_group(); fn(); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)


# ------------------------------------------------------------------ shots
def opening_face(ctx, f, lf, lab=True, txt="\"I'M BOOORED...\""):
    """ECU: the kid, melted with boredom, cheek squished on his fist"""
    sh = shake_at(lf, [0], 6, 10)
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 50)), -3, sh, f)
    bored_bg(ctx, lf)
    sag = 0.6 + 0.08 * math.sin(lf * 0.15)
    cx, cy, Rt = 560, 930 + 8 * math.sin(lf * 0.12), 310
    rot = 0.16
    face(ctx, BOY, P(eye='shock', mouth='wavy', head=0), cx, cy, Rt, rot)
    lids(ctx, BOY, cx, cy, Rt, sag, 1, rot)
    fist_chin(ctx, cx, cy, Rt)
    # a long sigh puff
    ph = (lf % 40) / 40
    ellipse(ctx, cx + 260 + 80 * ph, cy + 160 - 40 * ph, 40 + 40 * ph, 26 + 26 * ph); setc(ctx, (1, 1, 1, 0.7 * (1 - ph))); ctx.fill()
    ctx.restore()
    if lab:
        label(ctx, txt, 540, LY + 40, 108, (1, 1, 1), -0.03, pop(lf, 0, 4) if lf > 0 else 1)


def s1(ctx, f):
    if f < 50:
        opening_face(ctx, f, f)
    else:
        lf = f - 50
        # wide: the toy mountain. kid flat on the floor. Mom in the doorway.
        pull = eout(pop(lf, 0, 14))
        ctx.save(); cam(ctx, 560, 1150, 1.45 - 0.4 * pull, 0, shake_at(lf, [0], 8, 12), f)
        playroom(ctx, door=1.0)
        toy_pile(ctx, 360, FLOOR + 10, 760, 560)
        mp = P(eye='glare', mouth='open', rsh=-130, rel=-20, lsh=40, lel=-130, head=-4)
        draw_hip(ctx, 900, FLOOR - 220, 1.2, -1, MOM, mp)
        # kid lying face-up in front of the pile
        ctx.save(); ctx.translate(560, FLOOR - 40); ctx.rotate(-math.pi / 2)
        draw_hip(ctx, 0, 0, 0.95, -1, BOY, P(eye='closed' if lf < 30 else 'smug', mouth='flat', lsh=160, lel=0, rsh=-160, rel=0))
        ctx.restore()
        ctx.restore()
        if lf < 30:
            label(ctx, "\"YOU HAVE 100 TOYS!\"", 540, LY + 40, 100, YEL, -0.03, pop(lf, 0, 4))
        else:
            label(ctx, "\"...they're BORING.\"", 540, LY + 40, 100, (1, 1, 1), 0.03, pop(lf, 30, 34))
    card(ctx, 'p1', f, -6, 108)


IDEAS = ("\"READ A BOOK?\"", "\"PLAY OUTSIDE?\"", "\"BUILD A FORT?\"")


def s2(ctx, f):
    lf = f - 110
    k, il = min(2, lf // 40), lf - min(2, lf // 40) * 40
    kick_ = eout(pop(il, 0, 8))
    if k == 0:
        # top-down: kid starfished on the rug, a book on his face
        ctx.save(); cam(ctx, 540, 1000, 1.05 + 0.05 * kick_, 4, shake_at(il, [20], 6, 10), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('5ac8a8')); ctx.fill()
        ellipse(ctx, 540, 1000, 470, 560); fl(ctx, hx('ff8ac0'), 9)
        ellipse(ctx, 540, 1000, 360, 440); setc(ctx, hx('ffb0d8')); ctx.fill()
        for j, (x, y) in enumerate(((160, 560), (900, 640), (140, 1360), (930, 1300))):
            ball(ctx, x, y, 50, TOYCOL[j], j)
        b = draw_hip(ctx, 540, 1180, 1.15, 1, BOY, P(eye='closed', mouth='flat', lsh=120, lel=-10, rsh=-120, rel=10, lhip=30, rhip=-30))
        if il >= 20:
            book(ctx, b['head'][0], b['head'][1] + 60, 0.9, 0.1)
        ctx.restore()
    elif k == 1:
        # upside down off the edge of the bed, low angle
        ctx.save(); cam(ctx, 540, 1060, 1.0 + 0.06 * kick_, -6, shake_at(il, [20], 6, 10), f)
        playroom(ctx)
        rect_r(ctx, -200, 980, 900, 140, 30); fl(ctx, (1, 1, 1), 8)
        rect_r(ctx, -200, 1110, 900, 350, 20); fl(ctx, hx('ff9f5a'), 8)
        ctx.save(); ctx.translate(420, 1010); ctx.rotate(math.pi + 0.15)
        draw_hip(ctx, 0, 0, 1.0, -1, BOY, P(eye='normal' if il < 20 else 'smug', mouth='flat', lsh=170, lel=0, rsh=-170, rel=0, lhip=-10, rhip=10, sway=0.3 * math.sin(il * 0.3)))
        ctx.restore()
        ctx.restore()
    else:
        # melting down the wall
        slide = eout(pop(il, 0, 38))
        ctx.save(); cam(ctx, 560, 1220, 1.3 + 0.08 * kick_, 3, shake_at(il, [20], 6, 10), f)
        playroom(ctx)
        ctx.save(); ctx.translate(560, FLOOR - 230 + 160 * slide); ctx.scale(1 + 0.25 * slide, 1 - 0.3 * slide)
        draw_hip(ctx, 0, 0, 1.05, 1, BOY, P(eye='closed', mouth='wavy', torso=-8, head=20 * slide, lsh=20, lel=10, rsh=-20, rel=-10, lhip=60 * slide, lkn=-60 * slide, rhip=-60 * slide, rkn=60 * slide))
        ctx.restore()
        ellipse(ctx, 560, FLOOR + 10, 180 + 160 * slide, 30); setc(ctx, (0, 0, 0, 0.15)); ctx.fill()
        ctx.restore()
    if il < 20:
        label(ctx, IDEAS[k], 540, LY + 40, 104, YEL, -0.03 if k % 2 else 0.03, pop(il, 0, 4))
    else:
        label(ctx, "\"BORING.\"", 540, LY + 40, 124, GREY, 0.04 if k % 2 else -0.04, pop(il, 20, 24))
    card(ctx, 'p2', f, 112, 228)


def s3(ctx, f):
    lf = f - 230
    if lf < 62:
        # Mom ECU: calm ... then CHORES with red lightning
        red = lf >= 34
        ctx.save(); cam(ctx, 540, 1000, 1.0 + (0.04 * eout(pop(lf, 0, 34)) if not red else 0.18), 0, shake_at(lf, [34], 14, 26), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('b98aff') if not red else hx('c8102e')); ctx.fill()
        if red:
            rays(ctx, 540, 900, 240, 1600, lf * 0.03, col=(0.3, 0, 0.05), a=0.5, n=16)
            bolt(ctx, 140, 520, 1.1); bolt(ctx, 880, 600, 0.9)
        face(ctx, MOM, P(eye='smug' if not red else 'glare', mouth='smile' if not red else 'grin', head=0), 540, 900, 300, 0.03 if not red else -0.03)
        ctx.restore()
        if not red:
            label(ctx, "\"Fine. Then help me with...\"", 540, LY + 40, 84, (1, 1, 1), -0.02, pop(lf, 2, 6))
        else:
            label(ctx, "\"...THE CHORES.\"", 540, LY + 40, 120, YEL, 0.03, pop(lf, 34, 38))
    elif lf < 78:
        il = lf - 62
        # kid ECU: eyes pop -> POOF
        ctx.save(); cam(ctx, 540, 1000, 1.1 + 0.1 * eout(pop(il, 0, 6)), 0, shake_at(il, [0], 10, 28), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8a1f')); ctx.fill()
        rays(ctx, 540, 950, 240, 1600, il * 0.05, col=(1, 1, 0.6), a=0.5, n=18)
        face(ctx, BOY, P(eye='shock', mouth='scream', head=0), 540, 930, 330, 0)
        for ex, ey, rx in eye_pos(540, 930, 330):
            ellipse(ctx, ex, ey, rx * 1.25, rx * 1.45); fl(ctx, (1, 1, 1), 8)
            ellipse(ctx, ex, ey, rx * 0.35, rx * 0.4); setc(ctx, INK); ctx.fill()
        puff(ctx, 540, 1000, pop(il, 8, 16), 3.0)
        ctx.restore()
        label(ctx, "*GASP!*", 540, LY + 40, 128, (1, 1, 1), -0.04, pop(il, 0, 4))
    else:
        il = lf - 78
        # super-speed "busy" playing with EVERY toy
        ctx.save(); cam(ctx, 540, 1150, 1.1, 2 * math.sin(il * 0.5), 4, f)
        playroom(ctx)
        hlines(ctx, il // 2, 0.35, (1, 1, 1), 700, 1450)
        bx, hip = 540, FLOOR - 175

        def kid(dx):
            ph = il * 1.6
            return draw_hip(ctx, bx + dx, hip, 1.05, 1, BOY, P(eye='happy', mouth='grin', rsh=-150 + 40 * math.sin(ph), rel=-30, lsh=150 - 40 * math.sin(ph + 1), lel=30,
                                                                   lhip=20 * math.sin(ph), rhip=-20 * math.sin(ph)))
        for dx, a in ((-150, 0.18), (150, 0.18)):
            ghost(ctx, a, lambda dx=dx: kid(dx * math.sin(il * 0.9)))
        b = kid(0)
        hx_, hy_ = b['head']
        for j in range(4):   # juggled balls
            a = il * 0.5 + j * math.pi / 2
            ball(ctx, hx_ + 240 * math.cos(a), hy_ - 150 + 120 * math.sin(a), 42, TOYCOL[j], a)
        # rocket loops around
        ra = il * 0.22
        rocket(ctx, 540 + 380 * math.cos(ra), 900 + 200 * math.sin(ra), 0.8, ra + math.pi, 1.0)
        # race car zooms back and forth along the floor
        cxp = 540 + 420 * math.sin(il * 0.35)
        toy_car(ctx, cxp, FLOOR + 20, 0.9, RED, 1 if math.cos(il * 0.35) > 0 else -1)
        # block tower grows
        for j in range(min(6, il // 6)):
            block(ctx, 160, FLOOR - 40 - j * 80, 80, TOYCOL[(j + 2) % 8], 0.05 * math.sin(il * 0.3 + j))
        teddy(ctx, 880, FLOOR - 150 - 60 * abs(math.sin(il * 0.4)), 0.7, 0.3 * math.sin(il * 0.4))
        ctx.restore()
        if il < 30:
            label(ctx, "\"I'M SO BUSY!!\"", 540, LY + 40, 120, YEL, -0.04, pop(il, 1, 5))
        else:
            label(ctx, "\"BEST TOYS EVER!\"", 540, LY + 40, 116, (1, 1, 1), 0.04, pop(il, 30, 34))
    card(ctx, 'p3', f, 264, 366)


def s4(ctx, f):
    lf = f - 370
    if lf < 56:
        # Mom leaves, door clicks shut. Kid instantly drops everything.
        gone = lf >= 18
        ctx.save(); cam(ctx, 540, 1100, 0.95, 0, shake_at(lf, [18, 24], 8, 14), f)
        door = 1.0 - eout(pop(lf, 8, 18))
        playroom(ctx, door=door)
        if lf < 14:
            draw_hip(ctx, 880 + 10 * lf, FLOOR - 220, 1.2, 1, MOM, P(eye='happy', mouth='smile'))
        if not gone:
            b = draw_hip(ctx, 440, FLOOR - 175, 1.05, 1, BOY, P(eye='happy', mouth='grin', rsh=-150, rel=-30, lsh=150, lel=30))
            for j in range(3):
                ball(ctx, 300 + j * 140, 880 - 40 * (j % 2), 42, TOYCOL[j], j)
        else:
            t = pop(lf, 24, 34)
            for j in range(3):   # balls drop and bounce
                yb = min(FLOOR - 40, 880 + 900 * t * t)
                ball(ctx, 300 + j * 140, yb, 42, TOYCOL[j], j + t * 3)
            ctx.save(); ctx.translate(500, FLOOR - 40); ctx.rotate(-math.pi / 2 * eout(pop(lf, 24, 32)))
            draw_hip(ctx, 0, -135 * (1 - eout(pop(lf, 24, 32))), 1.05, -1, BOY, P(eye='smug' if lf < 24 else 'closed', mouth='flat', lsh=160, lel=0, rsh=-160, rel=0))
            ctx.restore()
        ctx.restore()
        if lf < 18:
            label(ctx, "*click*", 540, LY + 40, 100, (1, 1, 1), 0.03, pop(lf, 14, 18))
        else:
            label(ctx, "\"...I'm bored.\"", 540, LY + 40, 110, GREY, -0.03, pop(lf, 24, 28))
    else:
        il = lf - 56
        # low-angle ECU: Mom is back with a mop and a bucket
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.08 * eout(pop(il, 0, 74)), -4, shake_at(il, [0], 14, 30), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('6a3cc8')); ctx.fill()
        rays(ctx, 540, 900, 260, 1600, il * 0.02, col=(0.9, 0.8, 1), a=0.35, n=16)
        face(ctx, MOM, P(eye='glare', mouth='smile', head=0), 560, 880, 290, -0.06)
        mop(ctx, 180, 760, 0.15, 1.2, math.sin(il * 0.3))
        bucket(ctx, 860, 1420, 1.1)
        sparkle(ctx, 560 + 0.42 * 290, 880 - 40, 40, (1, 1, 1))
        ctx.restore()
        label(ctx, "\"I HEARD THAT.\"", 540, LY + 40, 120, YEL, -0.03, pop(il, 2, 6))
    card(ctx, 'p4', f, 428, 496)


def s5(ctx, f):
    lf = f - 500
    if lf < 72:
        # living room: Mom lounging with popcorn, kid mops at super speed behind her
        ctx.save(); cam(ctx, 540, 1180, 0.8, 0, 0, f)
        ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('6fd6c8')); ctx.fill()
        for i in range(-30, 40):
            ctx.rectangle(i * 120, -3000, 46, 6000); setc(ctx, dark(hx('6fd6c8'), 0.94)); ctx.fill()
        ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('e8b878')); ctx.fill()
        ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()
        sofa_back(ctx)
        draw_hip(ctx, 470, SEAT, 1.15, 1, MOM, sit(eye='closed' if lf < 40 else 'happy', mouth='smile', torso=-14, head=-6, rsh=-160, rel=-60, lsh=40, lel=-70, lhip=80, lkn=-20, rhip=84, rkn=-24))
        sofa_front(ctx)
        popcorn(ctx, 340, SEAT + 20, 0.9)
        # super-speed kid zipping left <-> right, mop scrubbing
        kx = 540 + 460 * math.sin(lf * 0.32)
        dirn = 1 if math.cos(lf * 0.32) > 0 else -1
        for g_ in (3, 2, 1):
            ghost(ctx, 0.12 * (4 - g_), lambda g_=g_: draw_hip(ctx, kx - dirn * g_ * 70, FLOOR + 120, 0.95, dirn, BOY, run_pose(lf * 1.2, eye='shock', mouth='open')))
        b = draw_hip(ctx, kx, FLOOR + 120, 0.95, dirn, BOY, run_pose(lf * 1.2, eye='shock', mouth='open', rsh=-60, rel=-30))
        mop(ctx, b['front'][0], b['front'][1], -dirn * 0.9, 0.8, math.sin(lf))
        sweat(ctx, b['head'][0] + 60, b['head'][1] - 40, lf, 0.9)
        hlines(ctx, lf // 2, 0.4, (1, 1, 1), 1450, 1800)
        for j in range(5):
            sparkle(ctx, 120 + j * 200 + 20 * math.sin(lf * 0.3 + j), FLOOR + 200 + 30 * (j % 2), 22 + 8 * math.sin(lf * 0.4 + j), (1, 1, 1))
        ctx.restore()
        if lf < 36:
            label(ctx, "*SCRUB SCRUB SCRUB!*", 540, LY + 40, 96, (1, 1, 1), 0.03, pop(lf, 1, 5))
        else:
            label(ctx, "\"Ahh... I'm SO bored.\"", 540, LY + 40, 100, PINK, -0.03, pop(lf, 36, 40))
    elif lf < 126:
        il = lf - 72
        # Mom ECU: smug wink + popcorn, kid inset exhausted
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(il, 0, 54)), 2, shake_at(il, [0], 6, 10), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb0d8')); ctx.fill()
        rays(ctx, 540, 900, 240, 1500, il * 0.02, col=(1, 1, 1), a=0.4, n=16)
        wink = 12 <= il < 30
        face(ctx, MOM, P(eye='smug' if not wink else 'happy', mouth='grin', head=0), 540, 880, 280, -0.05)
        popcorn(ctx, 300, 1300, 1.4)
        ctx.restore()
        label(ctx, "\"Mop the stairs too, sweetie!\"", 540, LY + 40, 84, (1, 1, 1), -0.03, pop(il, 4, 8))
        if il >= 20:
            u = eout(pop(il, 20, 28))
            ctx.save(); ctx.translate(880 + 320 * (1 - u), 1160)
            ellipse(ctx, 0, 0, 120, 120); fl(ctx, YEL, 8); ctx.save(); ellipse(ctx, 0, 0, 112, 112); ctx.clip()
            face(ctx, BOY, P(eye='shock', mouth='wavy', head=0), 0, 10, 88, 0.05)
            ctx.restore(); ctx.restore()
    else:
        il = lf - 126
        opening_face(ctx, f, il, True)
    if lf < 126:
        card(ctx, 'p5', f, 504, 622)
    else:
        card(ctx, 'p1', f, 626)


SHOTS = [(0, s1), (110, s2), (230, s3), (370, s4), (500, s5)]
CUTS = (50, 110, 150, 190, 230, 264, 292, 308, 370, 426, 500, 572, 626)


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
                              "-i", "out/im_bored_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
