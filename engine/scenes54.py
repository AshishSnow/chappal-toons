"""'Catching the Tooth Fairy' - original, general-audience comedy short, 23s.
Hook: ECU kid with a fresh gap-tooth grin holding up a tiny tooth: "MY TOOTH CAME OUT!!"
Beat 1: kid with a butterfly net + rope: "Tonight... I CATCH the TOOTH FAIRY."
Beat 2: the trap - net over the pillow, tripwire bell, kid 'asleep' with one giant eye open in the dark.
Beat 3: midnight, Dad tiptoes in with a coin -> foot hits the tripwire *DING* -> *WHOOSH* hangs upside down, flashlight: "GOT YOU!"
Turn: split: Dad "I... AM the tooth fairy?" / kid "Then where are your WINGS?" -> Dad flaps upside down, kid "Okay. PAY UP."
Twist: rope snaps, *THUD*, Dad's OWN tooth pops out -> gap grin "...do I get a COIN too?" -> cut back to the opening grin (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos, zigs, lids, zzz
from scenes48 import label1, label2
import scenes13
from scenes13 import card as _card13
import random

BOY = dict(doodle.BOY, hood=False, shirt=hx('7fd0ff'), pants=hx('3d7bff'))
DAD = dict(doodle.DAD, shirt=hx('ffb347'), pants=hx('8a5cd6'))
N = 690
FLOOR = 1460
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
GOLD = hx('ffc83c')
NIGHT = hx('1d2456')
ROPE = hx('c9934e')

CAPS = {
    'p1': [[("LOSING YOUR", OUT)], [("FIRST TOOTH", PINK)]],
    'p2': [[("THE", OUT)], [("TRAP", ORANGE)]],
    'p3': [[("11:59 PM", PURPLE)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def tooth(ctx, x, y, s=1.0, a=0.0, glow=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 10, 0, 0, 110)
        g.add_color_stop_rgba(0, 1, 1, 0.8, 0.8 * glow); g.add_color_stop_rgba(1, 1, 1, 0.8, 0)
        ctx.set_source(g); ctx.arc(0, 0, 110, 0, 2 * math.pi); ctx.fill()
    ctx.move_to(-40, -40); ctx.curve_to(-50, -70, -10, -70, 0, -55); ctx.curve_to(10, -70, 50, -70, 40, -40)
    ctx.curve_to(38, 0, 30, 40, 20, 55); ctx.curve_to(12, 60, 6, 20, 0, 10); ctx.curve_to(-6, 20, -12, 60, -20, 55)
    ctx.curve_to(-30, 40, -38, 0, -40, -40); ctx.close_path()
    fl(ctx, (1, 1, 1), 6)
    ellipse(ctx, -16, -40, 9, 6); setc(ctx, hx('cfe8ff')); ctx.fill()
    ctx.restore()


def gap(ctx, cx, cy, Rt, f_=1):
    """dark missing-tooth block on a 'grin' mouth drawn with face()"""
    mx, my = cx + f_ * 0.12 * Rt, cy + 0.5 * Rt
    rect_r(ctx, mx - 0.06 * Rt, my - 0.085 * Rt, 0.12 * Rt, 0.1 * Rt, 0.025 * Rt); setc(ctx, hx('5a1424')); ctx.fill()


def coin(ctx, x, y, r=40, spin=0.0):
    w = max(0.15, abs(math.cos(spin)))
    ellipse(ctx, x, y, r * w, r); fl(ctx, GOLD, 5)
    ellipse(ctx, x, y, r * w * 0.7, r * 0.7); setc(ctx, hx('ffe27a')); ctx.fill()
    if w > 0.5:
        text(ctx, "$", x, y + r * 0.35, r * 0.95, hx('b8860b'), outline=(1, 1, 1, 0), ow=1, shadow=False)


def bell(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(-50, 40); ctx.curve_to(-50, -20, -40, -60, 0, -60); ctx.curve_to(40, -60, 50, -20, 50, 40); ctx.line_to(62, 52); ctx.line_to(-62, 52); ctx.close_path()
    fl(ctx, GOLD, 6)
    ellipse(ctx, 0, 62, 16, 16); fl(ctx, hx('b8860b'), 5)
    ellipse(ctx, 0, -66, 12, 10); fl(ctx, GOLD, 5)
    ctx.restore()


def net_mesh(ctx, x, y, w, h, sag=1.0, col=(1, 1, 1)):
    """hanging/dropped net: bag shape with a mesh"""
    ctx.save()
    ctx.move_to(x - w / 2, y); ctx.curve_to(x - w / 2, y + h * sag, x + w / 2, y + h * sag, x + w / 2, y); ctx.close_path()
    setc(ctx, col + (0.18,)); ctx.fill_preserve(); ctx.clip()
    for i in range(-12, 13):
        ctx.move_to(x + i * 34 - h, y); ctx.line_to(x + i * 34 + h, y + h * 1.2)
        ctx.move_to(x + i * 34 + h, y); ctx.line_to(x + i * 34 - h, y + h * 1.2)
    setc(ctx, col + (0.85,)); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()
    ctx.move_to(x - w / 2 - 10, y); ctx.line_to(x + w / 2 + 10, y); setc(ctx, OUT); ctx.set_line_width(16); ctx.stroke_preserve(); setc(ctx, ORANGE); ctx.set_line_width(9); ctx.stroke()


def bedroom(ctx, dark_=0.0, wall=hx('8fd8ff')):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, wall); ctx.fill()
    for i in range(-30, 40):   # wallpaper stars
        for j in range(-10, 14):
            if (i + j) % 2 == 0:
                sparkle(ctx, i * 140 + 70, j * 150 + 40, 9, light(wall, 0.35))
    # window with moon
    rect_r(ctx, 640, 420, 300, 340, 20); fl(ctx, hx('ffffff'), 8)
    ctx.rectangle(660, 440, 260, 300); setc(ctx, hx('243070')); ctx.fill()
    ellipse(ctx, 840, 520, 46, 46); setc(ctx, hx('fff6c0')); ctx.fill()
    ellipse(ctx, 862, 508, 40, 40); setc(ctx, hx('243070')); ctx.fill()
    for sx, sy in ((700, 480), (760, 640), (880, 690)):
        sparkle(ctx, sx, sy, 10, (1, 1, 0.8))
    ctx.move_to(790, 440); ctx.line_to(790, 740); ctx.move_to(660, 590); ctx.line_to(920, 590); ink(ctx, 8); ctx.stroke()
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('c98a52')); ctx.fill()
    ctx.rectangle(-3000, FLOOR - 6, 7000, 12); setc(ctx, OUT); ctx.fill()
    if dark_ > 0:
        ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, (0.04, 0.05, 0.2, 0.62 * dark_)); ctx.fill()


def bed(ctx, x0=60, x1=620, top=1180):
    rect_r(ctx, x0 - 20, top - 200, 60, FLOOR - top + 200, 20); fl(ctx, hx('ff8a5a'), 8)   # headboard
    rect_r(ctx, x0, top, x1 - x0, 170, 24); fl(ctx, hx('ffffff'), 8)
    rect_r(ctx, x0, top + 60, x1 - x0, 140, 24); fl(ctx, hx('ff5f8f'), 8)
    for x in (x0 + 20, x1 - 50):
        ctx.rectangle(x, top + 200, 30, FLOOR - top - 200); fl(ctx, hx('a8561f'), 6)


def pillow(ctx, x, y, s=1.0):
    rect_r(ctx, x - 110 * s, y - 50 * s, 220 * s, 100 * s, 44 * s); fl(ctx, hx('fff8e0'), 7)


def flashlight_cone(ctx, x0, y0, x1, y1, w=260, a=0.4):
    ang = math.atan2(y1 - y0, x1 - x0); px, py = -math.sin(ang), math.cos(ang)
    ctx.move_to(x0 + px * 20, y0 + py * 20); ctx.line_to(x1 + px * w, y1 + py * w); ctx.line_to(x1 - px * w, y1 - py * w); ctx.line_to(x0 - px * 20, y0 - py * 20); ctx.close_path()
    setc(ctx, (1, 1, 0.75, a)); ctx.fill()
    ellipse(ctx, x1, y1, w * 1.0, w * 1.0); setc(ctx, (1, 1, 0.8, a * 0.7)); ctx.fill()


def torch(ctx, x, y, a=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -70, -22, 120, 44, 12); fl(ctx, RED, 6)
    poly(ctx, [(50, -32), (90, -40), (90, 40), (50, 32)]); fl(ctx, hx('dddde8'), 6)
    ctx.restore()


# ------------------------------------------------------------------ opening
def kid_face(ctx, f, lf, lab=True):
    """ECU: kid's fresh gap-tooth grin, tooth held up, sparkles"""
    sh = shake_at(lf, [0], 10, 18)
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eout(pop(lf, 0, 40)), 0, sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8fc8')); ctx.fill()
    rays(ctx, 540, 900, 260, 1700, lf * 0.06, col=(1, 1, 0.75), a=0.5, n=18)
    cx, cy, R = 500, 900, 300
    face(ctx, BOY, P(eye='happy', mouth='grin', head=0), cx, cy, R, -0.04 + 0.03 * math.sin(lf * 0.6))
    gap(ctx, cx, cy, R)
    # hand + tooth held up
    hb = 6 * math.sin(lf * 0.5)
    ellipse(ctx, 880, 690 + hb, 70, 66); fl(ctx, BOY['skin'], 7)
    tooth(ctx, 880, 560 + hb, 1.1, 0.15 * math.sin(lf * 0.3), glow=1.0)
    for k in range(5):
        a = lf * 0.15 + k * 1.26
        sparkle(ctx, 880 + math.cos(a) * 150, 560 + math.sin(a) * 120, 18 + 6 * math.sin(lf * 0.5 + k))
    ctx.restore()
    if lab:
        label2(ctx, "\"MY TOOTH", "CAME OUT!!\"", (1, 1, 1), 1.0 if f < 60 else pop(lf, 0, 3), 116, col2=YEL)


def dad_face(ctx, f, lf):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eout(pop(lf, 0, 50)), 0, shake_at(lf, [0], 8, 14), f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, NIGHT); ctx.fill()
    rays(ctx, 540, 900, 260, 1700, lf * 0.05, col=(1, 0.85, 0.4), a=0.35, n=18)
    cx, cy, R = 520, 900, 300
    face(ctx, DAD, P(eye='happy', mouth='grin', head=0), cx, cy, R, 0.04 * math.sin(lf * 0.4))
    gap(ctx, cx, cy, R)
    for (sx, sy) in ((300, 560), (720, 520), (520, 470)):   # dizzy stars
        sparkle(ctx, sx + 20 * math.sin(lf * 0.3 + sx), sy, 20, YEL)
    hb = 6 * math.sin(lf * 0.5)
    ellipse(ctx, 870, 700 + hb, 76, 70); fl(ctx, DAD['skin'], 7)
    tooth(ctx, 870, 565 + hb, 1.15, 0.12 * math.sin(lf * 0.3), glow=0.8)
    ctx.restore()


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 60:
        kid_face(ctx, f, f)
    else:
        lf = f - 60
        # kid with a butterfly net + rope, scheming grin, push in
        ctx.save(); cam(ctx, 540, 1060, 1.05 + 0.08 * eout(pop(lf, 0, 60)), 0, 0, f)
        bedroom(ctx, 0.35)
        bed(ctx)
        pillow(ctx, 200, 1150)
        tooth(ctx, 200, 1095, 0.5, 0, glow=0.6 + 0.3 * math.sin(lf * 0.3))
        pk = P(torso=0, lhip=-10, lkn=0, rhip=10, rkn=0, lsh=-150, lel=-30, rsh=-40, rel=-80, eye='smug', mouth='grin', head=-6)
        bk = draw(ctx, 760, FLOOR - 186 * 1.15, 1.15, -1, BOY, pk)
        gap(ctx, bk['head'][0], bk['head'][1], bk['R'], -1)
        # butterfly net held up
        hx_, hy_ = bk['back']
        ctx.move_to(hx_, hy_); ctx.line_to(hx_ + 40, hy_ - 380); setc(ctx, OUT); ctx.set_line_width(20); ctx.stroke_preserve(); setc(ctx, hx('a8561f')); ctx.set_line_width(12); ctx.stroke()
        ellipse(ctx, hx_ + 50, hy_ - 470, 100, 90); setc(ctx, (1, 1, 1, 0.3)); ctx.fill_preserve(); ink(ctx, 9); ctx.stroke()
        net_mesh(ctx, hx_ + 50, hy_ - 470, 190, 160, 1.0)
        zigs(ctx, bk['head'][0], bk['head'][1], 160, lf, n=5)
        ctx.restore()
        label2(ctx, "\"Tonight... I CATCH", "the TOOTH FAIRY.\"", (1, 1, 1), pop(lf, 3, 7), 86, col2=PINK)
    card(ctx, 'p1', f, -6, 118)


def s2(ctx, f):
    lf = f - 120
    if lf < 75:
        # trap build: net rigged over the pillow, tripwire + bell; quick snap-zooms on each part
        stage = 0 if lf < 25 else (1 if lf < 50 else 2)
        foci = ((330, 760, 1.35), (760, 1300, 1.45), (540, 1060, 0.95))
        fx, fy, fz = foci[stage]
        sl = lf - stage * 25
        ctx.save(); cam(ctx, fx, fy, fz + 0.06 * eout(pop(sl, 0, 25)), 0, shake_at(sl, [3], 8, 14), f)
        bedroom(ctx, 0.45)
        bed(ctx)
        pillow(ctx, 330, 1150)
        tooth(ctx, 330, 1095, 0.5, 0, glow=0.7)
        # rope from ceiling hook over the pillow
        ctx.move_to(330, 180); ctx.line_to(330, 600); setc(ctx, OUT); ctx.set_line_width(14); ctx.stroke_preserve(); setc(ctx, ROPE); ctx.set_line_width(8); ctx.stroke()
        ellipse(ctx, 330, 170, 20, 20); fl(ctx, hx('aaaab8'), 5)
        drop = 1 - eout(pop(lf, 2, 14))
        net_mesh(ctx, 330, 600 - 300 * drop, 360, 260, 0.7)
        # tripwire across the floor to the bell on the door handle
        if lf >= 25:
            tw = eout(pop(lf, 26, 36))
            ctx.move_to(620, FLOOR - 30); ctx.line_to(620 + 380 * tw, FLOOR - 30); setc(ctx, (1, 1, 1)); ctx.set_line_width(5); ctx.stroke()
            ctx.move_to(1000, FLOOR - 30); ctx.line_to(1000, 1160); setc(ctx, (1, 1, 1)); ctx.set_line_width(4); ctx.stroke()
            rect_r(ctx, 960, 700, 260, 760, 10); fl(ctx, hx('d98a4a'), 8)     # door
            ellipse(ctx, 990, 1100, 20, 20); fl(ctx, GOLD, 5)
            bell(ctx, 1000, 1180, 0.8, 0.3 * math.sin(lf * 0.9) * (1 - pop(lf, 36, 50)))
        # kid tying knots, hands blur
        pk = P(torso=6, lhip=-10, lkn=0, rhip=10, rkn=0, lsh=-90 + 40 * math.sin(lf * 1.1), lel=-40, rsh=-60 + 40 * math.sin(lf * 1.3 + 1), rel=-40, eye='smug', mouth='grin', head=4)
        if stage > 0:
            bk = draw(ctx, 580, FLOOR - 186 * 1.0, 1.0, -1, BOY, pk)
        ctx.restore()
        if stage == 0:
            label1(ctx, "*NET: READY*", (1, 1, 1), pop(sl, 1, 4), 110)
        elif stage == 1:
            label1(ctx, "*TRIPWIRE: SET*", YEL, pop(sl, 1, 4), 104)
        else:
            label2(ctx, "\"NOBODY gets", "past ME.\"", (1, 1, 1), pop(sl, 1, 5), 108, col2=ORANGE)
        card(ctx, 'p2', f, 122, 192)
    else:
        il = lf - 75
        # pitch dark: kid "asleep" with ONE giant eye wide open, fake snore
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.1 * eout(pop(il, 0, 65)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('0d1030')); ctx.fill()
        cx, cy, R = 540, 900, 290
        face(ctx, BOY, P(eye='closed', mouth='flat', head=0), cx, cy, R, 0)
        # blanket pulled up to the nose
        rect_r(ctx, 60, cy + 0.38 * R, 960, 900, 90); fl(ctx, hx('ff5f8f'), 10)
        for k in range(5):
            ctx.move_to(120 + k * 190, cy + 0.38 * R + 60); ctx.line_to(120 + k * 190, 1900); setc(ctx, hx('ff86aa')); ctx.set_line_width(22); ctx.stroke()
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, (0.02, 0.02, 0.12, 0.55)); ctx.fill()
        # one HUGE eye pops open, darting
        (lx, ly, lr), (rx, ry, rr) = eye_pos(cx, cy, R)
        op = eout(pop(il, 14, 20))
        if op > 0:
            ellipse(ctx, rx, ry, rr * 1.5, rr * 1.5 * op); fl(ctx, (1, 1, 1), 8)
            dx = 0.6 * rr * math.sin(il * 0.25)
            ellipse(ctx, rx + dx, ry, rr * 0.6, rr * 0.6 * op); setc(ctx, INK); ctx.fill()
            ellipse(ctx, rx + dx - rr * 0.2, ry - rr * 0.2 * op, rr * 0.18, rr * 0.18 * op); setc(ctx, (1, 1, 1)); ctx.fill()
        ctx.restore()
        label1(ctx, "\"zzz... *fake snore*\"", hx('c8e6ff'), pop(il, 2, 6), 92, y=1440)


def s3(ctx, f):
    lf = f - 260
    if lf < 60:
        # low angle: Dad tiptoes in with a shiny coin, exaggerated sneaking
        ctx.save(); cam(ctx, 540, 1100, 1.0 + 0.05 * eout(pop(lf, 0, 60)), -3, 0, f)
        bedroom(ctx, 0.8)
        bed(ctx, 40, 520)
        pillow(ctx, 200, 1150)
        ellipse(ctx, 380, 1170, 110, 60); fl(ctx, hx('ff5f8f'), 7)   # sleeping kid lump
        net_mesh(ctx, 200, 600, 340, 240, 0.7)
        ctx.move_to(200, -200); ctx.line_to(200, 600); setc(ctx, ROPE); ctx.set_line_width(8); ctx.stroke()
        ctx.move_to(560, FLOOR - 30); ctx.line_to(1100, FLOOR - 30); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(5); ctx.stroke()
        step = lf / 20.0
        x = 980 - 160 * eout(pop(lf, 0, 60))
        lift = abs(math.sin(step * math.pi))
        pd = P(torso=-12, lhip=-40 * lift, lkn=70 * lift, rhip=20, rkn=10, lsh=-120, lel=-60, rsh=-150, rel=-30, eye='smug', mouth='flat', head=8)
        bd = draw(ctx, x, FLOOR - 186 * 1.3 - 30 * lift, 1.3, -1, DAD, pd)
        coin(ctx, bd['front'][0], bd['front'][1] - 50, 34, lf * 0.3)
        sparkle(ctx, bd['front'][0] + 30, bd['front'][1] - 100, 14 + 6 * math.sin(lf * 0.6))
        ctx.restore()
        label2(ctx, "\"Sneaky...", "SNEAKY...\"", (1, 1, 1), pop(lf, 3, 7), 104, col2=PURPLE)
        card(ctx, 'p3', f, 262, 318)
    elif lf < 100:
        il = lf - 60
        # floor-level ECU: big bare foot slowly comes down... onto the tripwire
        ctx.save(); cam(ctx, 540, 1100, 1.0, 0, shake_at(il, [20], 10, 18), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('1a1f4a')); ctx.fill()
        ctx.rectangle(-500, 1300, 2200, 1000); setc(ctx, dark(hx('c98a52'), 0.55)); ctx.fill()
        ctx.move_to(-500, 1300); ctx.line_to(1700, 1300); ink(ctx, 8); ctx.stroke()
        down = eout(pop(il, 0, 20))
        tw_y = 1240 + (14 if il >= 20 else 0) * math.sin(il * 2.5) * (1 - pop(il, 20, 40))
        ctx.move_to(-100, 1240); ctx.line_to(540, tw_y); ctx.line_to(1200, 1240); setc(ctx, (1, 1, 1)); ctx.set_line_width(9); ctx.stroke()
        fy = 760 + 470 * down
        ctx.save(); ctx.translate(560, fy)
        ctx.rectangle(-90, -900, 180, 820); fl(ctx, DAD['pants'], 9)
        ellipse(ctx, 20, 0, 230, 110); fl(ctx, DAD['skin'], 9)
        for k in range(5):
            ellipse(ctx, 150 + k * 24 - k * k * 6, -70 + k * 22, 40 - k * 5, 34 - k * 4); fl(ctx, DAD['skin'], 7)
        ctx.restore()
        ctx.restore()
        if il < 20:
            label1(ctx, "*tiptoe... tiptoe...*", hx('c8e6ff'), pop(il, 1, 4), 92)
        else:
            label1(ctx, "*TWANG!*", YEL, pop(il, 20, 23), 150, 0.05)
    else:
        il = lf - 100
        # WHOOSH: Dad yanked up, hanging upside down by one ankle, swinging; flashlight snaps on
        ctx.save(); cam(ctx, 540, 1000, 0.95, 0, shake_at(il, [0, 8], 20, 26), f)
        bedroom(ctx, 0.85 if il < 22 else 0.5)
        bed(ctx, 40, 520)
        pillow(ctx, 200, 1150)
        tooth(ctx, 200, 1095, 0.5, 0, glow=0.6)
        up = eout(pop(il, 0, 10))
        sw = 0.22 * math.sin(il * 0.22) * math.exp(-il * 0.02)
        ax, ay = 660, 260
        ctx.save(); ctx.translate(ax, ay); ctx.rotate(sw)
        rope_len = 260 + (1 - up) * 900
        ctx.move_to(0, -500); ctx.line_to(0, rope_len); setc(ctx, OUT); ctx.set_line_width(14); ctx.stroke_preserve(); setc(ctx, ROPE); ctx.set_line_width(8); ctx.stroke()
        ctx.translate(0, rope_len); ctx.rotate(math.pi)
        s_ = 1.3
        pd = P(torso=0, lhip=-4, lkn=0, rhip=60, rkn=80, lsh=170, lel=10, rsh=-170, rel=-10, eye='shock', mouth='scream', head=0)
        bd = draw(ctx, 0, -186 * s_, s_, 1, DAD, pd)
        ctx.restore()
        if il < 30:
            coin(ctx, 640, 900 + 600 * ein(pop(il, 4, 24)), 34, il * 0.5)
        # kid pops up in bed with the flashlight
        if il >= 22:
            kp = eout(pop(il, 22, 28))
            pk = P(torso=-6, lhip=-80, lkn=80, rhip=-75, rkn=85, lsh=-70, lel=-20, rsh=-40, rel=-40, eye='smug', mouth='grin', head=0)
            bk = draw_hip(ctx, 300, 1210 + 120 * (1 - kp), 0.95, 1, BOY, pk)
            rect_r(ctx, 60, 1180, 460, 160, 30); fl(ctx, hx('ff5f8f'), 8)
            hx_, hy_ = bk['front']
            flashlight_cone(ctx, hx_ + 40, hy_, 660, 640, 230, 0.35 * kp)
            torch(ctx, hx_, hy_, math.atan2(640 - hy_, 660 - hx_), 1.0)
        ctx.restore()
        if il < 22:
            label1(ctx, "*WHOOOSH!*", (1, 1, 1), pop(il, 1, 4), 150, -0.05)
        else:
            label2(ctx, "\"GOT YOU,", "TOOTH FAIRY!!\"", (1, 1, 1), pop(il, 22, 26), 108, col2=YEL)


def hanging_dad(ctx, cx, cy, s, il, pose, rope_top=-600):
    ctx.save(); ctx.translate(cx, rope_top); ctx.rotate(0.06 * math.sin(il * 0.2))
    ctx.move_to(0, 0); ctx.line_to(0, cy - rope_top); setc(ctx, OUT); ctx.set_line_width(14); ctx.stroke_preserve(); setc(ctx, ROPE); ctx.set_line_width(8); ctx.stroke()
    ctx.translate(0, cy - rope_top); ctx.rotate(math.pi)
    b = draw(ctx, 0, -186 * s, s, 1, DAD, pose)
    ctx.restore()
    return b


def s4(ctx, f):
    lf = f - 420
    if lf < 70:
        # split: Dad upside down (top) / kid squinting behind the flashlight (bottom)
        ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
        ctx.rectangle(0, 0, W, 960); setc(ctx, hx('ff8a5a')); ctx.fill()
        rays(ctx, 540, 600, 120, 1300, lf * 0.04, col=(1, 1, 0.7), a=0.35, n=16)
        hanging_dad(ctx, 540, 190, 1.15, lf, P(torso=0, lhip=-4, lkn=0, rhip=60, rkn=80, lsh=150, lel=30, rsh=-60, rel=-60, eye='normal', mouth='wavy', head=0))
        ctx.restore()
        ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
        ctx.rectangle(0, 960, W, 960); setc(ctx, hx('1d2456')); ctx.fill()
        cx, cy, R = 470, 1200, 230
        face(ctx, BOY, P(eye='smug', mouth='flat', head=0), cx, cy, R, 0.05)
        lids(ctx, BOY, cx, cy, R, 0.45)
        torch(ctx, 820, 1280, -0.5, 1.6)
        flashlight_cone(ctx, 900, 1200, 1100, 900, 180, 0.3)
        ctx.restore()
        ctx.rectangle(0, 952, W, 16); setc(ctx, (1, 1, 1)); ctx.fill()
        if lf < 32:
            label(ctx, "\"I... AM the tooth fairy?\"", 540, 840, 74, (1, 1, 1), -0.03, pop(lf, 2, 6))
        if lf >= 30:
            label2(ctx, "\"Then where", "are your WINGS?\"", (1, 1, 1), pop(lf, 30, 34), 96, col2=PINK, y=1460)
    else:
        il = lf - 70
        # wide: Dad flaps his arms like wings upside down; kid holds out a palm
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.04 * eout(pop(il, 0, 70)), 0, 0, f)
        bedroom(ctx, 0.5)
        bed(ctx, 40, 520)
        flap = math.sin(il * 0.9)
        b = hanging_dad(ctx, 700, 380, 1.2, il, P(torso=0, lhip=-4, lkn=0, rhip=60, rkn=80, lsh=90 + 60 * flap, lel=20, rsh=-90 - 60 * flap, rel=-20, eye='happy', mouth='grin', head=0))
        for k in range(3):   # flap motion lines
            for sx in (-1, 1):
                ctx.move_to(700 + sx * (260 + k * 30), 700 + k * 40); ctx.line_to(700 + sx * (320 + k * 30), 720 + k * 40); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(7); ctx.stroke()
        pk = P(torso=0, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=-80, lel=-10, rsh=12, rel=-15, eye='smug', mouth='flat', head=-4)
        bk = draw(ctx, 260, FLOOR - 186 * 1.0, 1.0, 1, BOY, pk)
        if il >= 36:
            fx_, fy_ = bk['front']
            ellipse(ctx, fx_ + 20, fy_ - 10, 50, 22); fl(ctx, BOY['skin'], 6)   # open palm
        ctx.restore()
        if il < 34:
            label1(ctx, "*flap... flap...*", (1, 1, 1), pop(il, 2, 5), 110)
        else:
            label2(ctx, "\"Okay.", "PAY UP.\"", (1, 1, 1), pop(il, 36, 40), 116, col2=GOLD)


def s5(ctx, f):
    lf = f - 560
    if lf < 50:
        # rope SNAPS -> Dad drops, THUD, his own tooth pops out flying
        snap = 12
        fall = ein(pop(lf, snap, snap + 10))
        ctx.save(); cam(ctx, 540, 1000, 0.95, 0, shake_at(lf, [snap + 10], 26, 30), f)
        bedroom(ctx, 0.5)
        bed(ctx, 40, 520)
        if lf < snap:
            hanging_dad(ctx, 700, 380, 1.2, lf, P(torso=0, lhip=-4, lkn=0, rhip=60, rkn=80, lsh=150, lel=20, rsh=-150, rel=-20, eye='shock', mouth='open', head=0))
            # fraying rope
            for k in range(4):
                ctx.move_to(700, 60); ctx.line_to(700 + (k - 1.5) * 18, 20 + k * 10); setc(ctx, ROPE); ctx.set_line_width(5); ctx.stroke()
        elif fall < 1:
            ctx.save(); ctx.translate(0, 900 * fall)
            hanging_dad(ctx, 700, 380, 1.2, lf, P(torso=0, lhip=-4, lkn=0, rhip=60, rkn=80, lsh=170, lel=0, rsh=-170, rel=0, eye='shock', mouth='scream', head=0), rope_top=200)
            ctx.restore()
        else:
            draw_hip(ctx, 600, FLOOR - 60, 1.2, -1, DAD, P(torso=-70, lhip=-90, lkn=10, rhip=-80, rkn=20, lsh=-160, lel=0, rsh=160, rel=0, eye='closed', mouth='open', head=-10))
            puff(ctx, 560, FLOOR - 20, pop(lf, snap + 10, snap + 26), 1.6)
            u = pop(lf, snap + 10, snap + 34)
            tooth(ctx, 560 - 300 * u, 1100 - 700 * math.sin(u * math.pi * 0.85), 0.7, u * 8)
            for k in range(3):
                a = lf * 0.3 + k * 2.1
                sparkle(ctx, 640 + math.cos(a) * 120, 1150 + math.sin(a) * 40, 22, YEL)
        ctx.restore()
        if lf < snap + 10:
            label1(ctx, "*SNAP!*", (1, 1, 1), pop(lf, 2, 5), 150, 0.05)
        else:
            label1(ctx, "*THUD!*", YEL, pop(lf, snap + 10, snap + 13), 150, -0.04)
    elif lf < 112:
        il = lf - 50
        # twist: Dad's own gap grin, holding up HIS tooth
        dad_face(ctx, f, il)
        if il < 26:
            label2(ctx, "\"...MY tooth", "CAME OUT!\"", (1, 1, 1), pop(il, 2, 6), 110, col2=YEL)
        else:
            label2(ctx, "\"Do I get", "a COIN too?\"", (1, 1, 1), pop(il, 26, 30), 110, col2=GOLD)
    else:
        il = lf - 112
        kid_face(ctx, f, il)
        card(ctx, 'p1', f, 672)


SHOTS = [(0, s1), (120, s2), (260, s3), (420, s4), (560, s5)]
CUTS = (60, 120, 195, 260, 320, 360, 420, 490, 560, 610, 672)


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
                              "-i", "out/tooth_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
