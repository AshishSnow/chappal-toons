"""'The Last Slice' - original, general-audience comedy short, ~22s.
Hook: ECU Dad, sweaty, staring down at a glowing slice: "Is anyone gonna eat that?"
 -> wide: one slice left in the box. Mom: "Anyone want it?" ALL: "NO NO, YOU HAVE IT!" (polite fake smiles)
Beat 1 (STARE-DOWN): triple split, eyes darting, western whistle. Then three hands creep in slow-mo toward the slice.
Beat 2 (GRAB): all three touch it at once - freeze - yank back "OH NO, YOU TAKE IT!" Mom splits it with a ruler:
 "EXACTLY. EQUAL." three tiny slivers.
Beat 3 (BLACKOUT): *CLICK* lights out, only eyes... plus a 4th pair low down. *CHOMP CHOMP*. Lights on: plate empty,
 "YOU ATE IT!" everyone points at each other.
Twist: the dog under the table, cheese moustache, *BURP*. DING DONG: Grandma with a tower of pizza boxes: "I brought PIZZA!"
 10 minutes later... ONE slice left. -> loops to the opening ECU."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes20 import pizza_slice, pizza_box
from scenes21 import dog
from scenes14 import sweat
import scenes13
from scenes13 import card as _card13
import random

BOY = doodle.BOY
MOM = doodle.MOM_G
DAD = doodle.DAD
GRAN = dict(doodle.NMOM, hair=hx('dcdce6'), shirt=hx('ff8ac0'), glasses=hx('8a3cff'))
N = 660
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
WALL = hx('ffd98a')
LY = 1400
TY = 1060          # table top

CAPS = {
    'p1': [[("THE LAST SLICE", OUT)], [("OF PIZZA", ORANGE)]],
    'p2': [[("STEP 1:", OUT)], [("THE STARE-DOWN", PURPLE)]],
    'p3': [[("STEP 2:", OUT)], [("THE GRAB", RED)]],
    'p4': [[("STEP 3:", OUT)], [("THE BLACKOUT", BLUE)]],
    'p5': [[("PLOT TWIST:", OUT)], [("THE DOG", GREEN)]],
    'p6': [[("10 MINUTES LATER:", OUT)], [("...SERIOUSLY?", PINK)]],
}
scenes13.CAPS = CAPS
card = _card13


def label2(ctx, a, b, col, t, size=104, col2=None, y=LY):
    label(ctx, a, 540, y - 60, size, col, -0.03, t)
    label(ctx, b, 540, y + 50, size, col2 or col, 0.02, t)


def label1(ctx, s, col, t, size=110, ang=-0.03):
    label(ctx, s, 540, LY + 40, size, col, ang, t)


# ------------------------------------------------------------------ props / sets
def room(ctx):
    ctx.rectangle(-1500, -1500, 4500, 5000); setc(ctx, WALL); ctx.fill()
    for i in range(-6, 16):
        ctx.rectangle(i * 120, -1500, 50, 5000); setc(ctx, hx('ffcf70')); ctx.fill()
    # window + hanging lamp
    rect_r(ctx, 720, 420, 260, 240, 14); fl(ctx, hx('2a2a5a'), 9)
    ctx.move_to(850, 420); ctx.line_to(850, 660); ctx.move_to(720, 540); ctx.line_to(980, 540); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 930, 470, 22, 22); setc(ctx, hx('fff6c8')); ctx.fill()
    rect_r(ctx, 90, 470, 200, 160, 10); fl(ctx, hx('c98a52'), 8)
    ctx.rectangle(115, 495, 150, 110); fl(ctx, hx('9fe0ff'), 4)
    poly(ctx, [(130, 600), (190, 530), (250, 600)]); fl(ctx, hx('3fbf4a'), 4)


def table_front(ctx, y=TY, cloth=hx('ff5a6a')):
    ctx.rectangle(-300, y, 1680, 1200); fl(ctx, (1, 1, 1), 10)
    ctx.save(); ctx.rectangle(-300, y, 1680, 1200); ctx.clip()
    for i in range(-6, 30):
        ctx.rectangle(i * 70, y, 35, 1200); setc(ctx, cloth + (0.5,)); ctx.fill()
    for j in range(20):
        ctx.rectangle(-300, y + 15 + j * 70, 1680, 35); setc(ctx, cloth + (0.4,)); ctx.fill()
    ctx.restore()
    ctx.move_to(-300, y); ctx.line_to(1400, y); ink(ctx, 10); ctx.stroke()


def plate(ctx, x, y, s=1.0):
    ellipse(ctx, x, y, 190 * s, 46 * s); fl(ctx, (1, 1, 1), 7)
    ellipse(ctx, x, y, 130 * s, 28 * s); setc(ctx, hx('e4e9f2')); ctx.fill()


def glow_slice(ctx, x, y, s, lf, glow=1.0, a=0.0, cut=0.0):
    if glow > 0:
        rays(ctx, x, y, 80 * s, 420 * s, lf * 0.03, col=(1, 0.97, 0.6), a=0.55 * glow, n=14)
        for k in range(3):
            sparkle(ctx, x - 120 * s + 120 * s * k, y - 150 * s - 20 * s * (k % 2), (18 + 6 * math.sin(lf * 0.5 + k)) * s * glow)
    if cut <= 0:
        pizza_slice(ctx, x, y, s * 1.6, a)
    else:
        # three thin slivers drifting apart
        for k, dx in enumerate((-1, 0, 1)):
            ctx.save(); ctx.translate(x + dx * 70 * s * cut, y); ctx.rotate(dx * 0.12 * cut)
            ctx.save(); ctx.rectangle(-28 * s + dx * 30 * s, -200 * s, 60 * s, 400 * s); ctx.clip()
            pizza_slice(ctx, -dx * 10 * s, 0, s * 1.6, a)
            ctx.restore(); ctx.restore()


def arm(ctx, x0, y0, x1, y1, ch, w=70):
    ctx.move_to(x0, y0); ctx.line_to(x1, y1); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ink(ctx, w + 16); ctx.stroke_preserve(); setc(ctx, ch['shirt']); ctx.set_line_width(w); ctx.stroke()
    a = math.atan2(y1 - y0, x1 - x0)
    ctx.save(); ctx.translate(x1, y1); ctx.rotate(a)
    ellipse(ctx, 30, 0, 52, 40); fl(ctx, ch['skin'], 8)
    for k in (-1, 0, 1):
        rect_r(ctx, 50, -28 + k * 22 + 18, 54, 20, 10); fl(ctx, ch['skin'], 6)
    ctx.restore()


def eyes_only(ctx, x, y, s, look, col=(1, 1, 1), blink=False):
    for dx in (-60, 60):
        if blink:
            ctx.move_to(x + dx * s - 30 * s, y); ctx.line_to(x + dx * s + 30 * s, y); setc(ctx, col); ctx.set_line_width(8 * s); ctx.stroke()
            continue
        ellipse(ctx, x + dx * s, y, 40 * s, 30 * s); setc(ctx, col); ctx.fill()
        ellipse(ctx, x + dx * s + look * 20 * s, y + 4 * s, 14 * s, 16 * s); setc(ctx, INK); ctx.fill()


def finger_point(ctx, x, y, ang, ch, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s)
    ctx.move_to(-260, 0); ctx.line_to(0, 0); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ink(ctx, 80); ctx.stroke_preserve(); setc(ctx, ch['shirt']); ctx.set_line_width(64); ctx.stroke()
    ellipse(ctx, 30, 0, 50, 40); fl(ctx, ch['skin'], 8)
    rect_r(ctx, 50, -18, 90, 30, 15); fl(ctx, ch['skin'], 6)
    ctx.restore()


def family_wide(ctx, lf, pm, pd, pk, slice_glow=1.0, slice_on=True, rot=(0, 0, 0)):
    room(ctx)
    face(ctx, MOM, pm, 220, 860, 120, rot[0], 1)
    face(ctx, DAD, pd, 540, 820, 130, rot[1], 1)
    face(ctx, BOY, pk, 860, 880, 110, rot[2], -1)
    table_front(ctx)
    pizza_box(ctx, 540, TY + 210, 1.9, 1.0)
    if slice_on:
        glow_slice(ctx, 540, TY + 150, 0.9, lf, slice_glow, a=math.pi / 2)


# ------------------------------------------------------------------ opening
def opening_face(ctx, f, lf, lab=True):
    sh = shake_at(lf, [0], 10, 18) + 2
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 40)), 0, sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff9a3c')); ctx.fill()
    rays(ctx, 540, 1000, 240, 1700, lf * 0.04, col=(1, 0.95, 0.5), a=0.45, n=18)
    cx, cy = 540, 750 + 6 * math.sin(lf * 0.5)
    face(ctx, DAD, P(eye='shock', mouth='wavy', head=8), cx, cy, 255, 0.02 * math.sin(lf * 0.7))
    sweat(ctx, 780, 540, lf, 1.6)
    # drool drop
    dl = (lf * 2.5) % 60
    ellipse(ctx, 590, 930 + dl, 14, 20 + dl * 0.2); fl(ctx, hx('bfe6ff'), 4)
    table_front(ctx, 1130)
    # the slice in the foreground, glowing
    glow_slice(ctx, 540, 1150, 0.75, lf, 1.0, a=math.pi / 2 + 0.1 * math.sin(lf * 0.2))
    ctx.restore()
    if lab:
        label2(ctx, "\"Is anyone gonna", "eat that?\"", (1, 1, 1), pop(lf, 0, 4) if lf > 0 else 1, 110, col2=YEL)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 45:
        opening_face(ctx, f, f)
    else:
        lf = f - 45
        nono = lf >= 30
        ctx.save(); cam(ctx, 540, 1080, 1.0 + 0.06 * eout(pop(lf, 0, 60)), 0, shake_at(lf, [30], 10, 14), f)
        if not nono:
            family_wide(ctx, lf, P(eye='happy', mouth='smile', head=6), P(eye='normal', mouth='flat', head=8),
                        P(eye='normal', mouth='flat', head=8))
        else:
            family_wide(ctx, lf, P(eye='happy', mouth='grin', head=4), P(eye='happy', mouth='grin', head=-4),
                        P(eye='happy', mouth='grin', head=-4), rot=(0.05 * math.sin(lf), -0.05 * math.sin(lf), 0.05 * math.sin(lf + 1)))
            for k, (x, y) in enumerate(((220, 640), (540, 590), (860, 680))):
                sparkle(ctx, x + 110, y, 26 * eout(pop(lf, 30 + 3 * k, 36 + 3 * k)))
        ctx.restore()
        if not nono:
            label2(ctx, "MOM: \"Anyone", "want it?\"", (1, 1, 1), pop(lf, 0, 4), 104, col2=PINK)
        else:
            label2(ctx, "\"NO NO NO,", "YOU HAVE IT!\"", YEL, pop(lf, 30, 34), 112, col2=(1, 1, 1))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 66:
        # triple split stare-down: eyes darting left/right
        chars = ((MOM, hx('ff5fa8'), 1), (DAD, hx('ffb43a'), 1), (BOY, hx('3aa8ff'), -1))
        for i, (ch, bg, fp) in enumerate(chars):
            x0 = i * 360
            ctx.save(); ctx.rectangle(x0, 0, 360, H); ctx.clip()
            cam(ctx, x0 + 180, 960, 1.0 + 0.1 * eout(pop(lf, 0, 66)), 0, shake_at(lf, [0], 8, 10), f + i * 5, sx=x0 + 180)
            ctx.rectangle(x0 - 600, -500, 1600, 3000); setc(ctx, bg); ctx.fill()
            rays(ctx, x0 + 180, 960, 100, 1200, lf * 0.05 * (1 if i % 2 else -1), col=(1, 1, 1), a=0.3, n=10)
            dart = 1 if ((lf + i * 7) // 10) % 2 else -1
            face(ctx, ch, P(eye='glare', mouth='flat', head=0), x0 + 180 + 10 * dart, 960, 150, 0.08 * dart, fp)
            ctx.restore()
        for x in (352, 712):
            ctx.rectangle(x, 0, 16, H); setc(ctx, OUT); ctx.fill()
        label1(ctx, "*STARE*", (1, 1, 1), pop(lf, 0, 4), 140, 0.03 * math.sin(lf * 0.3))
    else:
        il = lf - 66
        # three hands creep in slowly toward the slice (top-down close)
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.12 * eout(pop(il, 0, 74)), 3 * math.sin(il * 0.05), 2, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8a96')); ctx.fill()
        for i in range(-10, 30):
            ctx.rectangle(i * 90, -500, 45, 3000); setc(ctx, (1, 1, 1, 0.45)); ctx.fill()
        for j in range(-10, 30):
            ctx.rectangle(-500, j * 90, 2200, 45); setc(ctx, (1, 1, 1, 0.35)); ctx.fill()
        ellipse(ctx, 540, 1000, 300, 300); fl(ctx, (1, 1, 1), 8)
        ellipse(ctx, 540, 1000, 220, 220); setc(ctx, hx('e4e9f2')); ctx.fill()
        glow_slice(ctx, 540, 1000, 1.3, il, 1.0, a=0.0)
        u = ein(pop(il, 4, 74)) * 0.62
        arm(ctx, -150, 700, -150 + (420 - -150) * u, 700 + (930 - 700) * u, MOM)
        arm(ctx, 1230, 760, 1230 + (660 - 1230) * u, 760 + (940 - 760) * u, BOY, 60)
        arm(ctx, 540, 2100, 540, 2100 + (1190 - 2100) * u, DAD, 80)
        ctx.restore()
        label1(ctx, "...s l o w l y...", (1, 1, 1), pop(il, 0, 4), 110)
    card(ctx, 'p2', f, 112, 246)


def s3(ctx, f):
    lf = f - 250
    if lf < 50:
        # TOUCH: all three hands land at once, freeze
        hit = lf >= 10
        ctx.save(); cam(ctx, 540, 1000, 1.25 + (0.2 * eout(pop(lf, 10, 16)) if hit else 0), 0, shake_at(lf, [10], 14, 26), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8a96')); ctx.fill()
        for i in range(-10, 30):
            ctx.rectangle(i * 90, -500, 45, 3000); setc(ctx, (1, 1, 1, 0.45)); ctx.fill()
        if hit:
            rays(ctx, 540, 1000, 120, 1500, lf * 0.02, col=(1, 1, 1), a=0.6, n=20)
        ellipse(ctx, 540, 1000, 300, 300); fl(ctx, (1, 1, 1), 8)
        glow_slice(ctx, 540, 1000, 1.3, lf, 0.6, a=0.0)
        u = 0.62 + 0.38 * eout(pop(lf, 0, 10))
        arm(ctx, -150, 700, -150 + (420 - -150) * u, 700 + (930 - 700) * u, MOM)
        arm(ctx, 1230, 760, 1230 + (660 - 1230) * u, 760 + (940 - 760) * u, BOY, 60)
        arm(ctx, 540, 2100, 540, 2100 + (1190 - 2100) * u, DAD, 80)
        ctx.restore()
        if hit:
            label1(ctx, "*TOUCH* !!!", YEL, pop(lf, 10, 13), 150, -0.05)
    elif lf < 92:
        il = lf - 50
        ctx.save(); cam(ctx, 540, 1080, 1.05, 0, shake_at(il, [0], 12, 20), f)
        family_wide(ctx, il, P(eye='shock', mouth='grin', head=-6), P(eye='shock', mouth='grin', head=6),
                    P(eye='shock', mouth='grin', head=6), rot=(-0.1, 0.08, 0.1))
        for x, y in ((220, 860), (540, 820), (860, 880)):
            sweat(ctx, x + 110, y - 120, il, 1.0)
        ctx.restore()
        label2(ctx, "\"OH NO,", "YOU TAKE IT!\"", (1, 1, 1), pop(il, 0, 4), 112, col2=YEL)
    else:
        il = lf - 92
        # Mom splits it with a ruler and a magnifying glass
        ctx.save(); cam(ctx, 540, 1000, 1.15, -4, shake_at(il, [20], 10, 14), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('9b4dff')); ctx.fill()
        rays(ctx, 540, 1000, 100, 1400, il * 0.03, col=(1, 1, 1), a=0.2, n=16)
        face(ctx, MOM, P(eye='glare', mouth='flat', head=10), 540, 640, 150, 0.05)
        ellipse(ctx, 540, 1120, 300, 120); fl(ctx, (1, 1, 1), 8)
        glow_slice(ctx, 540, 1100, 1.0, il, 0.0, a=math.pi / 2, cut=eout(pop(il, 20, 34)))
        # ruler
        rx = 540 + 200 * math.sin(il * 0.25) * (il < 20)
        ctx.save(); ctx.translate(rx, 980); ctx.rotate(-0.05)
        rect_r(ctx, -260, -28, 520, 56, 8); fl(ctx, hx('ffd23f'), 6)
        for k in range(13):
            ctx.move_to(-240 + k * 40, -28); ctx.rel_line_to(0, 22 if k % 2 else 34)
        ink(ctx, 4); ctx.stroke(); ctx.restore()
        # magnifying glass
        mx, my = 800, 1150 + 20 * math.sin(il * 0.3)
        ctx.move_to(mx + 60, my + 60); ctx.line_to(mx + 170, my + 170); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ink(ctx, 34); ctx.stroke()
        ellipse(ctx, mx, my, 86, 86); setc(ctx, (0.8, 0.95, 1, 0.5)); ctx.fill_preserve(); ink(ctx, 14); ctx.stroke()
        ctx.restore()
        if il < 20:
            label2(ctx, "MOM: \"Fine. We", "SPLIT it.\"", (1, 1, 1), pop(il, 0, 4), 104, col2=YEL)
        else:
            label2(ctx, "\"EXACTLY.", "EQUAL.\"", YEL, pop(il, 20, 24), 130, col2=(1, 1, 1))
    card(ctx, 'p3', f, 252, 386)


def s4(ctx, f):
    lf = f - 390
    if lf < 62:
        # *CLICK* blackout: only eyes. A 4th pair low down...
        if lf < 4:
            ctx.save(); cam(ctx, 540, 1080, 1.05, 0, 0, f)
            family_wide(ctx, lf, P(eye='glare', mouth='flat'), P(eye='glare', mouth='flat'), P(eye='glare', mouth='flat'), 0.3)
            ctx.restore()
        else:
            ctx.rectangle(0, 0, W, H); setc(ctx, hx('0d0b1a')); ctx.fill()
            il = lf - 4
            look = math.sin(il * 0.25)
            blink = (il % 25) < 2
            eyes_only(ctx, 220, 860, 0.9, look, blink=blink)
            eyes_only(ctx, 540, 820, 1.0, -look, blink=(il % 31) < 2)
            eyes_only(ctx, 860, 880, 0.85, look)
            if il > 18:
                eyes_only(ctx, 540, 1250, 0.7 * eout(pop(il, 18, 24)), 0.0, col=hx('ffd23f'))
            if il > 30:
                for k in range(3):
                    if (il // 5 + k) % 2:
                        text(ctx, "CHOMP", 300 + 240 * k, 1120 + 30 * k, 60, (1, 1, 1), ow=8, shadow=False, ang=-0.1 + 0.1 * k)
        if lf < 30:
            label1(ctx, "*CLICK*", (1, 1, 1), pop(lf, 2, 6), 140)
        else:
            label1(ctx, "*CHOMP CHOMP*", YEL, pop(lf, 30, 34), 120, 0.04)
    else:
        il = lf - 62
        ctx.save(); cam(ctx, 540, 1080, 1.05 + 0.05 * eout(pop(il, 0, 48)), 0, shake_at(il, [0], 12, 20), f)
        family_wide(ctx, il, P(eye='glare', mouth='scream', head=0), P(eye='glare', mouth='scream', head=0),
                    P(eye='glare', mouth='scream', head=0), slice_on=False)
        # pointing at each other
        finger_point(ctx, 330, 960, -0.15, MOM, 0.8)
        finger_point(ctx, 450, 940, math.pi + 0.2, DAD, 0.8)
        finger_point(ctx, 760, 990, math.pi - 0.2, BOY, 0.75)
        for x, y in ((540, TY + 140),):
            text(ctx, "?", x, y, 90, (1, 1, 1), ow=10, shadow=False)
        ctx.restore()
        label1(ctx, "\"YOU ATE IT!!\"", YEL, pop(il, 0, 4), 140, -0.04)
    card(ctx, 'p4', f, 392, 496)


def s5(ctx, f):
    lf = f - 500
    if lf < 50:
        # the dog under the table, cheese moustache, BURP
        burp = lf >= 26
        ctx.save(); cam(ctx, 540, 1150, 1.0 + 0.1 * eout(pop(lf, 0, 50)), 0, shake_at(lf, [26], 10, 16), f, sy=1100)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('3a2a40')); ctx.fill()
        ctx.rectangle(-500, 1500, 2200, 1000); setc(ctx, hx('b97a4a')); ctx.fill()
        # tablecloth edge hanging down from the top
        ctx.new_path(); ctx.move_to(-300, 450); ctx.line_to(1400, 450)
        for k in range(18):
            ctx.line_to(1400 - k * 100 - 50, 560); ctx.line_to(1400 - (k + 1) * 100, 450)
        ctx.line_to(-300, -200); ctx.line_to(1400, -200); ctx.close_path(); fl(ctx, hx('ff5a6a'), 8)
        dog(ctx, 520, 1500, 2.4, 1, lf, eye='happy' if not burp else 'closed', mouth=0.6 if burp else 0.0,
            tongue=0.0 if burp else 0.6 + 0.3 * math.sin(lf * 0.6), tail=2.0)
        # cheese moustache + crumbs
        ctx.save(); ctx.translate(520 + 48 * 2.4 + 64 * 2.4, 1500 - 250 * 2.4 + 50 * 2.4)
        for k in (-1, 1):
            ctx.move_to(0, 0); ctx.curve_to(k * 40, 30, k * 70, 50, k * 90, 90)
        setc(ctx, hx('ffcc3a')); ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke(); ctx.restore()
        for k in range(5):
            ellipse(ctx, 300 + 120 * k, 1540 + 10 * (k % 2), 12, 8); setc(ctx, hx('e0903a')); ctx.fill()
        if burp:
            puff(ctx, 940, 1000, pop(lf, 26, 46), 1.4)
        ctx.restore()
        if not burp:
            label1(ctx, "*lick lick*", (1, 1, 1), pop(lf, 2, 6), 120)
        else:
            label1(ctx, "*BUUURP!*", YEL, pop(lf, 26, 29), 150, 0.05)
        card(ctx, 'p5', f, 502, 548)
    elif lf < 100:
        il = lf - 50
        # DING DONG: Grandma with a tower of pizza boxes
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(il, 0, 50)), 0, shake_at(il, [0, 20], 10, 16), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, WALL); ctx.fill()
        rect_r(ctx, 130, 380, 820, 1500, 20); fl(ctx, hx('9fd8ff'), 12)
        rays(ctx, 540, 900, 150, 1200, il * 0.04, col=(1, 1, 1), a=0.45, n=16)
        face(ctx, GRAN, P(eye='happy', mouth='grin', head=0), 540, 730, 140, 0.06 * math.sin(il * 0.4))
        for k in range(4):
            pizza_box(ctx, 540 + 6 * math.sin(il * 0.5 + k), 1270 - k * 60, 1.6, 0.0)
        ctx.restore()
        if il < 20:
            label1(ctx, "*DING DONG*", (1, 1, 1), pop(il, 0, 4), 140)
        else:
            label2(ctx, "GRANDMA: \"I brought", "PIZZA!\"", (1, 1, 1), pop(il, 20, 24), 96, col2=YEL)
            for k in range(4):
                sparkle(ctx, 200 + 230 * k, 600 - 40 * (k % 2), 28 * eout(pop(il, 22 + 3 * k, 28 + 3 * k)))
        card(ctx, 'p5', f, 552, 598)
    elif lf < 130:
        il = lf - 100
        # 10 minutes later: ONE slice left. Again.
        ctx.save(); cam(ctx, 540, 1080, 1.0 + 0.1 * eout(pop(il, 0, 30)), 0, shake_at(il, [0], 10, 14), f)
        family_wide(ctx, il, P(eye='glare', mouth='flat', head=8), P(eye='shock', mouth='wavy', head=8),
                    P(eye='glare', mouth='flat', head=8))
        for k in range(3):
            pizza_box(ctx, 130 + k * 50, TY + 250 - k * 50, 1.1, 0.0)
        ctx.restore()
        label2(ctx, "...ONE", "slice left.", (1, 1, 1), pop(il, 0, 4), 120, col2=YEL)
        card(ctx, 'p6', f, 602, 628)
    else:
        il = lf - 130
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 630)


SHOTS = [(0, s1), (110, s2), (250, s3), (390, s4), (500, s5)]
CUTS = (45, 110, 176, 250, 300, 342, 390, 452, 500, 550, 600, 630)


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
                              "-i", "out/lastslice_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
