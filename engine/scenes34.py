"""'The Present Hunt' - original, general-audience comedy short, ~22s.
Hook: ECU of the kid lit from below by a flashlight, wild eyes: "THEY'RE IN THIS HOUSE." -> tiptoe through the dark hallway.
Beat 1: search montage in a flashlight spot: under the bed (one sock), the cupboard (broccoli), under the sofa (the lost remote).
Beat 2: a wobbly tower (basket + stool + books) to the TOP SHELF -> a glowing wrapped present. *RATTLE RATTLE*
Beat 3: lights ON. Mom in the doorway: "LOOKING FOR SOMETHING?" - tower collapses - "...I was dusting?"
Twist: Mom opens the box: a note "NICE TRY." Cut: Mom, flashlight under her own face: "NOW... WHERE DID DAD HIDE MINE?"
Loops to the opening ECU."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos
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
YEL = hx('fff27a')
LY = 1450

CAPS = {
    'p1': [[("WHEN YOU KNOW THE", OUT)], [("PRESENTS ARE HIDDEN", RED)]],
    'p2': [[("SEARCH MODE:", OUT)], [("PROFESSIONAL", PURPLE)]],
    'p3': [[("THE TOP SHELF.", OUT)], [("OBVIOUSLY.", ORANGE)]],
    'p4': [[("AND THEN...", OUT)], [("THE LIGHTS TURN ON", RED)]],
    'p5': [[("PLOT TWIST:", OUT)], [("IT RUNS IN THE FAMILY", GREEN)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props / fx
def flashlight(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -30, -20, 120, 40, 10); fl(ctx, hx('ff3b5c'), 6)
    poly(ctx, [(86, -26), (124, -36), (124, 36), (86, 26)]); fl(ctx, hx('c8c8d8'), 6)
    ellipse(ctx, 124, 0, 9, 36); setc(ctx, YEL); ctx.fill()
    ctx.restore()


def beam(ctx, x0, y0, x1, y1, w0=20, w1=180, a=0.45):
    dx, dy = x1 - x0, y1 - y0; L_ = math.hypot(dx, dy) or 1; nx, ny = -dy / L_, dx / L_
    poly(ctx, [(x0 + nx * w0, y0 + ny * w0), (x1 + nx * w1, y1 + ny * w1), (x1 - nx * w1, y1 - ny * w1), (x0 - nx * w0, y0 - ny * w0)])
    g = cairo.LinearGradient(x0, y0, x1, y1); g.add_color_stop_rgba(0, 1, 0.97, 0.6, a); g.add_color_stop_rgba(1, 1, 0.97, 0.6, a * 0.5)
    ctx.set_source(g); ctx.fill()
    ellipse(ctx, x1, y1, w1, w1 * 1.05); setc(ctx, (1, 0.97, 0.6, a * 0.7)); ctx.fill()


def under_light(ctx, cx, cy, Rt, k=1.0):
    """spooky 'flashlight under the chin' lighting over a drawn face"""
    g = cairo.LinearGradient(0, cy - 1.3 * Rt, 0, cy + 1.1 * Rt)
    g.add_color_stop_rgba(0, 0.05, 0.02, 0.15, 0.6 * k); g.add_color_stop_rgba(0.55, 0.05, 0.02, 0.15, 0.12 * k); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g); ctx.rectangle(-500, -500, 2200, 3000); ctx.fill()
    g = cairo.RadialGradient(cx, cy + 0.9 * Rt, 20, cx, cy + 0.9 * Rt, 1.2 * Rt)
    g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.45 * k); g.add_color_stop_rgba(1, 1, 0.9, 0.4, 0)
    ctx.set_source(g); ctx.rectangle(-500, -500, 2200, 3000); ctx.fill()


def dark_bg(ctx, lf, col=hx('1b1640')):
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, col); ctx.fill()
    rays(ctx, 540, 960, 280, 1500, lf * 0.015, col=(0.5, 0.45, 1.0), a=0.18, n=16)


def present(ctx, x, y, w, h, lid=0.0, col=hx('ff3b5c'), rib=hx('ffd23f')):
    ctx.rectangle(x - w / 2, y - h / 2, w, h); fl(ctx, col, 8)
    ctx.rectangle(x - w * 0.07, y - h / 2, w * 0.14, h); fl(ctx, rib, 5)
    ctx.save(); ctx.translate(x - w * 0.55, y - h / 2); ctx.rotate(-1.9 * lid); ctx.translate(-(x - w * 0.55), -(y - h / 2))
    ctx.rectangle(x - w * 0.55, y - h / 2 - h * 0.2, w * 1.1, h * 0.22); fl(ctx, col, 8)
    ctx.rectangle(x - w * 0.07, y - h / 2 - h * 0.2, w * 0.14, h * 0.22); fl(ctx, rib, 5)
    for sg in (-1, 1):   # bow
        ellipse(ctx, x + sg * w * 0.16, y - h / 2 - h * 0.3, w * 0.15, h * 0.12); fl(ctx, rib, 6)
    ellipse(ctx, x, y - h / 2 - h * 0.26, w * 0.06, w * 0.06); fl(ctx, rib, 5)
    ctx.restore()


def sock(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(0.3)
    ctx.new_path(); ctx.move_to(-40, -120); ctx.line_to(40, -120); ctx.line_to(40, 20); ctx.curve_to(40, 70, 120, 60, 130, 90)
    ctx.curve_to(140, 130, 60, 140, 0, 110); ctx.curve_to(-50, 90, -40, 40, -40, 20); ctx.close_path(); fl(ctx, (1, 1, 1), 7)
    ctx.rectangle(-40, -120, 80, 30); fl(ctx, hx('ff3b5c'), 6)
    ctx.restore()
    for k in range(3):   # stink lines
        ctx.new_path(); ctx.move_to(x - 60 + k * 50, y - 170)
        ctx.curve_to(x - 80 + k * 50, y - 210, x - 40 + k * 50, y - 240, x - 60 + k * 50, y - 280)
        setc(ctx, hx('9be86a')); ctx.set_line_width(10); ctx.stroke()


def dust_bunny(ctx, x, y, lf):
    rnd = random.Random(4)
    for k in range(14):
        a = k * 2 * math.pi / 14
        ellipse(ctx, x + math.cos(a) * 55, y + math.sin(a) * 40, 30, 30); setc(ctx, hx('b8b4c8')); ctx.fill()
    ellipse(ctx, x, y, 60, 46); setc(ctx, hx('c8c4d8')); ctx.fill()
    for sx in (-18, 18):
        ellipse(ctx, x + sx, y - 6, 9, 12 if (lf // 20) % 4 else 2); setc(ctx, INK); ctx.fill()


def broccoli(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    poly(ctx, [(-30, 0), (30, 0), (20, 150), (-20, 150)]); fl(ctx, hx('9be86a'), 7)
    for dx, dy, r in ((-60, -20, 60), (60, -20, 60), (0, -60, 70), (-30, 20, 50), (30, 20, 50)):
        ellipse(ctx, dx, dy, r, r); fl(ctx, hx('22b45a'), 7)
    for sx in (-22, 22):   # little smug face
        ellipse(ctx, sx, 70, 7, 10); setc(ctx, INK); ctx.fill()
    ctx.new_path(); ctx.arc(0, 90, 16, 0.3, math.pi - 0.3); ink(ctx, 5); ctx.stroke()
    ctx.restore()


def remote(ctx, x, y, a=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -55, -150, 110, 300, 30); fl(ctx, hx('3a3a4a'), 7)
    ellipse(ctx, 0, -100, 18, 18); setc(ctx, RED); ctx.fill()
    for r_ in range(3):
        for c_ in range(2):
            ellipse(ctx, -20 + c_ * 40, -30 + r_ * 50, 12, 12); setc(ctx, hx('c8c8d8')); ctx.fill()
    ctx.restore()


def spot_panel(ctx, f, il, item, lab, col):
    """dark frame, a flashlight spot reveals an item; kid's head peeks from the left with the torch"""
    sh = shake_at(il, [10], 6, 12)
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(il, 0, 30)), [-4, 3, -3][item], sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('120e2a')); ctx.fill()
    u = eout(pop(il, 0, 8))
    sx, sy = 640, 980
    g = cairo.RadialGradient(sx, sy, 40, sx, sy, 360 * u + 1)
    g.add_color_stop_rgba(0, 1, 0.96, 0.7, 1); g.add_color_stop_rgba(0.85, 1, 0.92, 0.55, 0.95); g.add_color_stop_rgba(1, 1, 0.9, 0.5, 0)
    ctx.set_source(g); ellipse(ctx, sx, sy, 360 * u + 1, 360 * u + 1); ctx.fill()
    if u > 0.5:
        ctx.save(); ellipse(ctx, sx, sy, 340, 340); ctx.clip()
        if item == 0:
            ctx.rectangle(-100, 1130, 1400, 400); setc(ctx, hx('8a6a52')); ctx.fill()
            sock(ctx, 600, 1060, 1.1); dust_bunny(ctx, 820, 1110, il)
        elif item == 1:
            ctx.rectangle(-100, 1130, 1400, 400); setc(ctx, hx('e8d0a0')); ctx.fill()
            ctx.move_to(-100, 1130); ctx.line_to(1400, 1130); ink(ctx, 8); ctx.stroke()
            broccoli(ctx, 640, 1000, 1.25)
        else:
            ctx.rectangle(-100, 1130, 1400, 400); setc(ctx, hx('8a6a52')); ctx.fill()
            remote(ctx, 640, 1000, 1.2, 1.1)
            for k in range(4):
                sparkle(ctx, 640 + 220 * math.cos(il * 0.2 + k * 1.6), 980 + 200 * math.sin(il * 0.2 + k * 1.6), 26)
        ctx.restore()
    # kid peeking in from the left edge
    kx = 250 - 300 * (1 - u)
    face(ctx, BOY, P(eye=('shock' if item < 2 else 'happy'), mouth=('wavy' if item < 2 else 'grin'), head=0), kx, 1240, 170, 0.15)
    flashlight(ctx, kx + 110, 1380, -0.55, 1.1)
    ctx.restore()
    label(ctx, lab, 540, LY, 92, col, -0.03, pop(il, 8, 12))


# ------------------------------------------------------------------ rooms
def parents_room(ctx, lights=False):
    wall = hx('ffb87a') if lights else hx('2a2350')
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, wall); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 140, -3000, 60, 6000); setc(ctx, dark(wall, 0.95)); ctx.fill()
    # open wardrobe on the left
    ctx.rectangle(120, 500, 640, 960); fl(ctx, hx('c96a2a') if lights else hx('4a3050'), 9)
    ctx.rectangle(150, 530, 580, 900); setc(ctx, hx('7a3e1a') if lights else hx('2a1a34')); ctx.fill()
    ctx.rectangle(150, 860, 580, 26); fl(ctx, hx('e0a060') if lights else hx('5a4060'), 6)      # top shelf
    ctx.move_to(170, 960); ctx.line_to(710, 960); ink(ctx, 8); ctx.stroke()                   # rail
    for k, col in enumerate((hx('3ccfb0'), hx('ff5fa8'), hx('1f8bff'), hx('ffd23f'))):         # hanging clothes
        x = 200 + k * 120
        poly(ctx, [(x, 960), (x + 90, 960), (x + 110, 1250), (x - 20, 1250)]); fl(ctx, col if lights else dark(col, 0.45), 6)
    # doorway right
    rect_r(ctx, 830, 620, 260, 840, 10); fl(ctx, dark(wall, 0.7), 9)
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('c98a52') if lights else hx('2a2040')); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()


def tower(ctx, x, n, wob):
    """n pieces stacked (0..3): basket, stool, books. returns top y"""
    ctx.save(); ctx.translate(x, FLOOR); ctx.rotate(wob); ctx.translate(-x, -FLOOR)
    top = FLOOR
    if n >= 1:   # laundry basket
        poly(ctx, [(x - 140, top - 120), (x + 140, top - 120), (x + 110, top), (x - 110, top)]); fl(ctx, hx('3ccfb0'), 8)
        for k in range(3):
            ctx.move_to(x - 125 + k * 10, top - 90 + k * 32); ctx.line_to(x + 125 - k * 10, top - 90 + k * 32)
        setc(ctx, hx('1f8a78')); ctx.set_line_width(8); ctx.stroke()
        top -= 120
    if n >= 2:   # stool
        ctx.rectangle(x - 110, top - 30, 220, 30); fl(ctx, hx('ffd23f'), 7)
        for sx in (-80, 60):
            ctx.rectangle(x + sx, top - 130, 20, 100); fl(ctx, hx('ff8a1f'), 6)
        ctx.rectangle(x - 120, top - 150, 240, 30); fl(ctx, hx('ffd23f'), 7)
        top -= 150
    if n >= 3:   # books
        for k, col in enumerate((hx('1f8bff'), hx('ff3b5c'), hx('8a3cff'))):
            ctx.rectangle(x - 100 + k * 8, top - 30, 200 - k * 16, 30); fl(ctx, col, 6)
            top -= 30
    ctx.restore()
    return top


# ------------------------------------------------------------------ shots
def opening_face(ctx, f, lf, lab=True):
    """ECU: kid lit from below by the flashlight"""
    sh = shake_at(lf, [0], 10, 20) + 2
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(lf, 0, 50)), 0, sh, f)
    dark_bg(ctx, lf)
    cx, cy, Rt = 540 + 4 * math.sin(lf * 0.7), 960, 310
    face(ctx, BOY, P(eye='shock', mouth='grin', head=0), cx, cy, Rt, 0.03 * math.sin(lf * 0.4))
    under_light(ctx, cx, cy, Rt)
    flashlight(ctx, 470, 1330, -1.45, 1.4)
    for k in range(4):
        sparkle(ctx, cx + 430 * math.cos(lf * 0.1 + k * 1.57), cy + 420 * math.sin(lf * 0.1 + k * 1.57), 24, YEL)
    ctx.restore()
    if lab:
        label(ctx, "\"THEY'RE IN THIS HOUSE.\"", 540, LY, 100, YEL, -0.04, pop(lf, 0, 4) if lf > 0 else 1)


def s1(ctx, f):
    if f < 52:
        opening_face(ctx, f, f)
    else:
        lf = f - 52
        # dark hallway, tiptoe with a scanning beam
        ctx.save(); cam(ctx, 540 + 2 * lf, 1080, 0.95 + 0.002 * lf, 2, 0, f)
        ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('1d2650')); ctx.fill()
        for i in range(-30, 40):
            ctx.rectangle(i * 120, -3000, 46, 6000); setc(ctx, hx('1a2248')); ctx.fill()
        for k, x in enumerate((180, 900)):   # picture frames on the wall
            rect_r(ctx, x - 90, 700, 180, 140, 6); fl(ctx, hx('2a3468'), 7)
        ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('2a2040')); ctx.fill()
        ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()
        ph = lf * 0.35
        x = 330 + 3.2 * lf
        kp = P(eye='shock', mouth='flat', torso=8, rsh=-80, rel=-20, lsh=50, lel=-90,
               lhip=-30 + 25 * math.sin(ph), lkn=40 + 20 * math.sin(ph), rhip=15 - 25 * math.sin(ph), rkn=10 + 30 * max(0, math.sin(ph)))
        b = draw_hip(ctx, x, FLOOR - 190 - 14 * abs(math.sin(ph)), 1.05, 1, BOY, kp)
        hxx, hyy = b['front']
        tx = hxx + 700; ty = 820 + 260 * math.sin(lf * 0.12)
        beam(ctx, hxx + 30, hyy, tx, ty, 18, 150, 0.4)
        flashlight(ctx, hxx - 20, hyy, math.atan2(ty - hyy, tx - hxx), 0.9)
        ctx.restore()
        label(ctx, "*TIPTOE... TIPTOE...*", 540, LY, 96, hx('c8b8ff'), 0.03, pop(lf, 2, 6))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 92:
        k = min(2, lf // 30)
        il = lf - 30 * k
        labs = [("UNDER THE BED: ONE SOCK", hx('9be86a')), ("CUPBOARD: BROCCOLI?!", (1, 1, 1)), ("UNDER THE SOFA: THE REMOTE!", YEL)]
        spot_panel(ctx, f, il, k, *labs[k])
    else:
        il = lf - 92
        # idea: kid ECU looks up, light bulb
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(il, 0, 28)), 0, shake_at(il, [6], 8, 12), f)
        dark_bg(ctx, il, hx('2a1f60'))
        face(ctx, BOY, P(eye='smug', mouth='grin', head=-12), 540, 1060, 300, -0.12)
        under_light(ctx, 540, 1060, 300, 0.7)
        u = eout(pop(il, 4, 12))
        if u > 0:
            ctx.save(); ctx.translate(780, 610); ctx.scale(u, u)
            rays(ctx, 0, 0, 90, 200, il * 0.1, col=(1, 0.95, 0.4), a=0.7, n=12)
            ellipse(ctx, 0, 0, 70, 80); fl(ctx, YEL, 8); ctx.rectangle(-30, 70, 60, 40); fl(ctx, hx('c8c8d8'), 6)
            ctx.restore()
        ctx.restore()
        label(ctx, "*DING!*", 540, LY, 120, YEL, 0.04, pop(il, 6, 10))
    card(ctx, 'p2', f, 114, 230)


def s3(ctx, f):
    lf = f - 230
    if lf < 84:
        # build the tower and climb (dark parents' room, beam from the torch)
        n = 1 + (lf >= 8) + (lf >= 16)
        drops = [0, 8, 16]
        wob = 0.05 * math.sin(lf * 0.5) * pop(lf, 26, 40)
        ctx.save(); cam(ctx, 540, 1000, 0.92 + 0.08 * eout(pop(lf, 30, 84)), 0, shake_at(lf, drops, 6, 12), f)
        parents_room(ctx, False)
        top = tower(ctx, 470, n, wob)
        if lf >= 24:
            climb = eout(pop(lf, 24, 44))
            hip = FLOOR - 85 + (top - FLOOR) * climb
            reach = pop(lf, 48, 64)
            kp = P(eye='shock' if lf < 60 else 'happy', mouth='flat' if lf < 60 else 'grin', rsh=-170 * reach - 20 * (1 - reach), rel=-10,
                   lsh=-60, lel=-40, rot=math.degrees(wob) * 1.6, lhip=-6 + 20 * math.sin(lf * 0.5) * (1 - reach), rkn=-4)
            ox = 470 + (top - FLOOR) * math.sin(wob)
            b = draw_hip(ctx, ox - 80 * (1 - climb), hip, 0.9, -1, BOY, kp)
        # the glowing present on the top shelf
        g = cairo.RadialGradient(300, 790, 20, 300, 790, 260)
        g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.7 * pop(lf, 40, 60)); g.add_color_stop_rgba(1, 1, 0.9, 0.4, 0)
        ctx.set_source(g); ellipse(ctx, 300, 790, 260, 260); ctx.fill()
        present(ctx, 300, 800, 200, 110)
        ctx.restore()
        if lf < 24:
            label(ctx, "*STACK! STACK! STACK!*", 540, LY, 92, YEL, 0.03, pop(lf, 2, 6))
        else:
            label(ctx, "*WOBBLE WOBBLE*", 540, LY, 104, hx('c8b8ff'), -0.03, pop(lf, 26, 30))
    else:
        il = lf - 84
        # ECU: the present in the kid's arms, choir glow, rattle
        rat = 14 * math.sin(il * 2.5) * pop(il, 24, 30)
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(il, 0, 56)), 0, 3 + abs(rat) * 0.3, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffcc3c')); ctx.fill()
        rays(ctx, 540, 1000, 220, 1500, il * 0.04, col=(1, 1, 1), a=0.6, n=18)
        face(ctx, BOY, P(eye='happy' if il < 24 else 'shock', mouth='grin' if il < 24 else 'open', head=0), 540, 760, 230, 0.05)
        present(ctx, 540 + rat, 1150, 420, 250)
        for k in range(5):
            sparkle(ctx, 540 + 420 * math.cos(il * 0.15 + k * 1.25), 1000 + 360 * math.sin(il * 0.15 + k * 1.25), 30, (1, 1, 1))
        ctx.restore()
        if il < 24:
            label(ctx, "\"JACKPOT!!\"", 540, LY, 124, hx('ff3b5c'), -0.04, pop(il, 2, 6))
        else:
            label(ctx, "*RATTLE RATTLE*", 540, LY, 110, (1, 1, 1), 0.04, pop(il, 24, 28))
    card(ctx, 'p3', f, 234, 366)


def s4(ctx, f):
    lf = f - 370
    if lf < 70:
        # lights ON - Mom in the doorway, kid frozen on top of the tower
        fall = pop(lf, 46, 62)
        wob = 0.03 * math.sin(lf * 0.6) + 0.9 * ein(fall)
        ctx.save(); cam(ctx, 560, 1000, 0.92, 0, shake_at(lf, [0, 62], 10, 22), f)
        parents_room(ctx, True)
        top = tower(ctx, 470, 3, wob)
        ox = 470 + (top - FLOOR) * math.sin(wob)
        hip = top - 85 + 500 * ein(fall) ** 2
        kp = P(eye='shock', mouth='scream' if lf > 40 else 'flat', rsh=50, rel=-100, lsh=-50, lel=100, rot=math.degrees(wob) * 1.2)
        b = draw_hip(ctx, ox - 30, min(hip, FLOOR - 120), 0.9, -1, BOY, kp)
        present(ctx, b['front'][0] * 0.5 + b['back'][0] * 0.5, b['front'][1] + 10, 160, 90)
        mp = P(eye='glare', mouth='flat', rsh=60, rel=-130, lsh=-60, lel=130, head=-4)
        draw_hip(ctx, 960, FLOOR - 20, 1.25, -1, MOM, mp)
        ctx.restore()
        if lf < 4:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.9 - 0.2 * lf)); ctx.fill()
        if lf < 8:
            label(ctx, "*CLICK*", 540, LY, 120, YEL, 0.04, pop(lf, 1, 4))
        elif lf < 44:
            label(ctx, "\"LOOKING FOR SOMETHING?\"", 540, LY, 92, (1, 1, 1), -0.03, pop(lf, 8, 12))
        else:
            label(ctx, "*CRASH!*", 540, LY, 140, YEL, 0.05, pop(lf, 60, 64))
    else:
        il = lf - 70
        # kid on the floor in the pile, hugging the present, nervous grin
        ctx.save(); cam(ctx, 540, 1100, 1.05 + 0.08 * eout(pop(il, 0, 60)), -5, shake_at(il, [0], 8, 14), f)
        parents_room(ctx, True)
        # rubble
        for k, col in enumerate((hx('1f8bff'), hx('ff3b5c'), hx('8a3cff'))):
            ctx.save(); ctx.translate(300 + k * 260, FLOOR - 30); ctx.rotate(0.3 * (k - 1)); ctx.rectangle(-100, -22, 200, 44); fl(ctx, col, 6); ctx.restore()
        ctx.save(); ctx.translate(760, FLOOR - 70); ctx.rotate(1.2)
        poly(ctx, [(-140, -170), (140, -170), (110, 0), (-110, 0)]); fl(ctx, hx('3ccfb0'), 8); ctx.restore()
        face(ctx, BOY, P(eye='shock', mouth='grin', head=0), 540, 1060, 270, -0.15)
        sweat(ctx, 800, 900 + (il % 20) * 6, 2.0)
        present(ctx, 540, 1320, 300, 160)
        sock(ctx, 200, 1200, 0.6)   # the sock lands on his head? no - beside him
        ctx.restore()
        label(ctx, "\"...I was DUSTING?\"", 540, LY, 104, (1, 1, 1), -0.03, pop(il, 8, 12))
    card(ctx, 'p4', f, 374, 496)


def note(ctx, x, y, s, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.rectangle(-210, -130, 420, 260); fl(ctx, (1, 1, 1), 7)
    for k in range(4):
        ctx.move_to(-180, -70 + k * 50); ctx.line_to(180, -70 + k * 50)
    setc(ctx, hx('b9dfff')); ctx.set_line_width(4); ctx.stroke()
    text(ctx, "NICE TRY.", 0, -10, 84, RED, ow=6, shadow=False)
    text(ctx, "- MOM", 90, 80, 46, OUT, outline=(1, 1, 1), ow=2, shadow=False)
    ctx.restore()


def s5(ctx, f):
    lf = f - 500
    if lf < 56:
        # Mom opens the box: a note pops out
        lid = eout(pop(lf, 6, 16)); up = eout(pop(lf, 12, 26))
        ctx.save(); cam(ctx, 540, 1040, 1.0 + 0.06 * eout(pop(lf, 12, 56)), 0, shake_at(lf, [14], 8, 14), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8ac0')); ctx.fill()
        rays(ctx, 540, 1000, 200, 1500, lf * 0.03, col=(1, 1, 1), a=0.35, n=16)
        present(ctx, 540, 1250, 420, 230, lid)
        if up > 0:
            note(ctx, 540, 1180 - 330 * up, 0.4 + 0.75 * up, -0.08 * up)
        # kid's horrified face, inset bottom-left
        ctx.save(); ctx.translate(200, 1260 - 0 * lf)
        ellipse(ctx, 0, 0, 130, 130); fl(ctx, YEL, 8); ctx.save(); ellipse(ctx, 0, 0, 122, 122); ctx.clip()
        face(ctx, BOY, P(eye='shock', mouth='scream', head=0), 0, 20, 96, 0.1)
        ctx.restore(); ctx.restore()
        ctx.restore()
        if lf < 14:
            label(ctx, "*RIIIP*", 540, LY, 120, (1, 1, 1), 0.04, pop(lf, 2, 6))
        else:
            label(ctx, "\"NOOOOO!\"", 700, LY, 116, YEL, -0.04, pop(lf, 16, 20))
    elif lf < 126:
        il = lf - 56
        # Mom, alone in the dark, flashlight under her own face
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.07 * eout(pop(il, 0, 70)), 0, shake_at(il, [0], 8, 14) + 2, f)
        dark_bg(ctx, il, hx('241238'))
        cx, cy, Rt = 540, 960, 310
        face(ctx, MOM, P(eye='smug', mouth='grin', head=0), cx, cy, Rt, -0.04 + 0.03 * math.sin(il * 0.3))
        under_light(ctx, cx, cy, Rt)
        flashlight(ctx, 610, 1330, -1.7, 1.4)
        ctx.restore()
        label(ctx, "\"NOW... WHERE DID DAD HIDE MINE?\"", 540, LY, 78, YEL, -0.03, pop(il, 4, 8))
        # tiny kid face peeking in, bottom right corner, shocked
        if il >= 36:
            u = eout(pop(il, 36, 44))
            ctx.save(); ctx.translate(840 + 300 * (1 - u), 1200)
            ellipse(ctx, 0, 0, 120, 120); fl(ctx, YEL, 8); ctx.save(); ellipse(ctx, 0, 0, 112, 112); ctx.clip()
            face(ctx, BOY, P(eye='shock', mouth='open', head=0), 0, 20, 88, -0.1)
            ctx.restore(); ctx.restore()
    else:
        il = lf - 126
        opening_face(ctx, f, il, True)
    if lf < 126:
        card(ctx, 'p5', f, 504, 622)
    else:
        card(ctx, 'p1', f, 626)


SHOTS = [(0, s1), (110, s2), (230, s3), (370, s4), (500, s5)]
CUTS = (52, 110, 140, 170, 202, 230, 314, 370, 440, 500, 556, 626)


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
                              "-i", "out/present_hunt_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
