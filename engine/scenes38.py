"""'Faking Sick' - original, general-audience comedy short, ~22s.
Hook: ECU of the kid in bed, ice pack on his head, blanket to the chin, over-acting: "*cough* I'm SO sick..."
 -> wide: Mom in the doorway, arms crossed: "Too sick for the TEST?" - "*cough*... so sick."
Beat 1: Mom holds up the thermometer. Insert: kid secretly presses it on the glowing bedside lamp, the numbers
 race up, it smokes. Mom ECU reads it: "...150 DEGREES?!"
Beat 2: Mom, sweetly: "Oh no... you'll MISS the PIZZA PARTY." (pizza thought bubble) -> kid GASP -> blanket flies,
 low-angle hero pose: "I'M CURED!!"
Beat 3: classroom: chalkboard "MATH TEST TODAY", no pizza. Split screen: kid melting at his desk / Mom at home
 sipping coffee, waving: "Good luck, sweetie!"
Twist: that evening Dad in an apron: "Honey, YOUR turn to cook!" - Mom in bed, ice pack, thermometer in her mouth,
 a lamp glowing under HER blanket: "*cough* I'm SO sick..." -> the kid in the doorway: "NICE TRY, MOM."
Loop: kid ECU, same over-acted cough -> loops to the opening."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos, lids, bedroom, bed_back, bed_front, clock
from scenes14 import sweat
import scenes13
from scenes13 import card as _card13
import random

BOY = doodle.BOY
MOM = doodle.MOM_G
DAD = doodle.DAD
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
    'p1': [[("WHEN YOU \"FEEL SICK\"", OUT)], [("ON A TEST DAY", RED)]],
    'p2': [[("THE SECRET TRICK:", OUT)], [("THE LAMP", ORANGE)]],
    'p3': [[("MOM'S MIRACLE CURE:", OUT)], [("\"PIZZA PARTY\"", GREEN)]],
    'p4': [[("THE PIZZA PARTY:", OUT)], [("NEVER EXISTED", PURPLE)]],
    'p5': [[("PLOT TWIST:", OUT)], [("GUESS WHO TAUGHT HIM", PINK)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def clerp(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def thermo(ctx, x, y, s, a, txt, hot=0.0):
    """digital thermometer centred at (x, y), tip pointing +x"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, 130, -12, 90, 24, 12); fl(ctx, clerp(hx('c8ccd8'), RED, hot), 5)
    rect_r(ctx, -170, -36, 320, 72, 34); fl(ctx, (1, 1, 1), 6)
    rect_r(ctx, -140, -24, 170, 48, 10); fl(ctx, clerp(hx('bff0c0'), hx('ffb0a0'), hot), 4)
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(38)
    e = ctx.text_extents(txt)
    ctx.move_to(-55 - e.x_advance / 2, 14); ctx.text_path(txt); setc(ctx, clerp(INK, hx('c8102e'), hot)); ctx.fill()
    ellipse(ctx, 80, 0, 14, 14); fl(ctx, BLUE, 4)
    ctx.restore()


def heat_waves(ctx, x, y, lf, s=1.0, a=0.8):
    for k in range(3):
        ph = ((lf * 2 + k * 12) % 36) / 36
        xx = x + (k - 1) * 50 * s
        ctx.move_to(xx, y - 260 * ph * s)
        for j in range(1, 7):
            ctx.line_to(xx + 14 * s * (1 if j % 2 else -1), y - (260 * ph + j * 22) * s)
        setc(ctx, (1, 1, 1, a * (1 - ph))); ctx.set_line_width(8 * s); ctx.stroke()


def lamp(ctx, x, y, s=1.0, glow=1.0, tilt=0.0):
    """bedside lamp, base centre at (x, y); bulb exposed under a tilted shade"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 120, 30); fl(ctx, hx('3a3a4a'), 6)
    ctx.rectangle(-14, -380, 28, 380); fl(ctx, hx('5a5a6a'), 5)
    bx, by = 0, -420
    if glow > 0:
        g = cairo.RadialGradient(bx, by, 10, bx, by, 360)
        g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.75 * glow); g.add_color_stop_rgba(1, 1, 0.9, 0.4, 0)
        ctx.set_source(g); ctx.arc(bx, by, 360, 0, 2 * math.pi); ctx.fill()
    ellipse(ctx, bx, by, 62, 70); fl(ctx, clerp(hx('d8d8c0'), hx('fff27a'), glow), 6)
    ctx.save(); ctx.translate(0, -450); ctx.rotate(tilt)
    poly(ctx, [(-130, -40), (130, -40), (80, -200), (-80, -200)]); fl(ctx, hx('ff8ac0'), 7)
    ctx.restore()
    ctx.restore()


def ice_pack(ctx, cx, cy, Rt, rot=0.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot)
    rect_r(ctx, -0.55 * Rt, -0.95 * Rt, 1.1 * Rt, 0.38 * Rt, 0.16 * Rt); fl(ctx, hx('7fd4ff'), Rt * 0.03)
    for k in range(3):
        ellipse(ctx, -0.3 * Rt + k * 0.3 * Rt, -0.78 * Rt, 0.07 * Rt, 0.05 * Rt); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()
    ctx.restore()


def blanket_chin(ctx, cx, cy, Rt, col=hx('3ccfb0')):
    """blanket pulled up to the chin in an ECU"""
    ctx.new_path(); ctx.move_to(-500, cy + 0.82 * Rt)
    ctx.curve_to(cx - Rt, cy + 0.7 * Rt, cx + Rt, cy + 0.7 * Rt, 1600, cy + 0.9 * Rt)
    ctx.line_to(1600, 3000); ctx.line_to(-500, 3000); ctx.close_path(); fl(ctx, col, Rt * 0.03)
    for k in range(-3, 4):
        ctx.move_to(cx + k * 0.6 * Rt, cy + 0.95 * Rt); ctx.line_to(cx + k * 0.6 * Rt, 3000)
    setc(ctx, dark(col, 0.85)); ctx.set_line_width(Rt * 0.05); ctx.stroke()


def pizza(ctx, x, y, s, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-110, -90), (110, -90), (0, 150)]); fl(ctx, hx('ffd23f'), 7)
    rect_r(ctx, -125, -120, 250, 46, 22); fl(ctx, hx('e08a3a'), 7)
    for px, py in ((-40, -40), (35, -30), (0, 40)):
        ellipse(ctx, px, py, 22, 22); fl(ctx, RED, 4)
    ctx.restore()


def bubble(ctx, x, y, rx, ry, tail):
    for k, (tx, ty, r) in enumerate(tail):
        ellipse(ctx, tx, ty, r, r); fl(ctx, (1, 1, 1), 6)
    ellipse(ctx, x, y, rx, ry); fl(ctx, (1, 1, 1), 8)


def mug(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(70, -60, 36, -math.pi / 2, math.pi / 2); ink(ctx, 14); ctx.stroke()
    rect_r(ctx, -60, -120, 130, 130, 18); fl(ctx, hx('ff5fa8'), 7)
    ctx.restore()
    for k in range(2):
        ctx.move_to(x - 15 + k * 40, y - 140 * s); ctx.curve_to(x + 15 + k * 40, y - 180 * s, x - 35 + k * 40, y - 210 * s, x - 5 + k * 40, y - 250 * s)
        setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(8); ctx.stroke()


def spatula(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(0, 40); ctx.line_to(0, -170); setc(ctx, OUT); ctx.set_line_width(20); ctx.stroke()
    ctx.move_to(0, 40); ctx.line_to(0, -170); setc(ctx, hx('ff9f5a')); ctx.set_line_width(10); ctx.stroke()
    rect_r(ctx, -45, -280, 90, 120, 16); fl(ctx, hx('c8ccd8'), 6)
    ctx.restore()


def chalk(ctx, s, x, y, size, a=0.0, col=(1, 1, 1)):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s); ctx.move_to(-e.x_advance / 2, size * 0.35); ctx.text_path(s); setc(ctx, col); ctx.fill()
    ctx.restore()


def classroom(ctx):
    wall = hx('8fd8c0')
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, wall); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(-3000, i * 110, 7000, 44); setc(ctx, dark(wall, 0.95)); ctx.fill()
    rect_r(ctx, 70, 560, 940, 520, 18); fl(ctx, hx('a0612e'), 9)
    rect_r(ctx, 100, 590, 880, 460, 8); fl(ctx, hx('1f5a40'), 6)
    chalk(ctx, "MATH TEST", 540, 690, 140, -0.03)
    chalk(ctx, "TODAY!", 500, 860, 110, 0.02, hx('fff27a'))
    ctx.move_to(170, 980); ctx.line_to(910, 980); setc(ctx, (1, 1, 1, 0.6)); ctx.set_line_width(6); ctx.stroke()
    clock(ctx, 920, 470, 60, 9, 0)
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('d8a868')); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()


def desk(ctx, x, y, w=420):
    rect_r(ctx, x - w / 2, y, w, 40, 10); fl(ctx, hx('ffb85a'), 7)
    for xx in (x - w / 2 + 30, x + w / 2 - 60):
        ctx.rectangle(xx, y + 40, 30, FLOOR - y - 40); fl(ctx, hx('5a5a6a'), 5)


def test_paper(ctx, x, y, s, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -120, -150, 240, 300, 8); fl(ctx, (1, 1, 1), 6)
    chalk(ctx, "TEST", 0, -100, 46, 0, RED)
    for k in range(5):
        ctx.move_to(-90, -40 + k * 40); ctx.line_to(90, -40 + k * 40)
    setc(ctx, GREY); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


# ------------------------------------------------------------------ shared shots
def sick_face(ctx, ch, lf, cx, cy, Rt, rot, bg):
    """ECU: over-acted sick face in bed (ice pack, blanket to the chin), coughing"""
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    for k in range(-6, 14):
        x = k * 200 + (lf * 1.2) % 200
        poly(ctx, [(x, -200), (x + 90, -200), (x - 900, 2400), (x - 990, 2400)]); setc(ctx, dark(bg, 0.93)); ctx.fill()
    ellipse(ctx, cx - 40, cy + 0.2 * Rt, 1.7 * Rt, 0.9 * Rt); fl(ctx, hx('dff1ff'), Rt * 0.03)   # pillow
    cough = (lf % 24) < 9
    jx = 10 * math.sin(lf * 2.3) if cough else 0
    face(ctx, ch, P(eye='closed' if cough else 'normal', mouth='scream' if cough else 'wavy', head=0), cx + jx, cy, Rt, rot)
    if not cough:
        lids(ctx, ch, cx, cy, Rt, 0.55, 1, rot)
    ice_pack(ctx, cx + jx, cy, Rt, rot)
    blanket_chin(ctx, cx, cy, Rt)
    if cough:
        for k in range(3):
            ellipse(ctx, cx + 0.9 * Rt + k * 40, cy + 0.35 * Rt - k * 30, 18 + 6 * k, 14 + 5 * k); setc(ctx, (1, 1, 1, 0.75)); ctx.fill()


def opening_face(ctx, f, lf, lab=True):
    sh = (shake_at(lf % 24, [0], 9, 10))
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 50)), -3, sh, f)
    sick_face(ctx, BOY, lf, 540, 960, 300, 0.12, hx('6f7fd8'))
    ctx.restore()
    if lab:
        label(ctx, "\"*cough* I'm SO sick...\"", 540, LY + 40, 96, (1, 1, 1), -0.03, pop(lf, 0, 4) if lf > 0 else 1)


def head_in_bed(ctx, ch, p, x, y, R, rot=-0.2):
    face(ctx, ch, p, x, y, R, rot)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 52:
        opening_face(ctx, f, f)
    else:
        lf = f - 52
        pull = eout(pop(lf, 0, 14))
        ctx.save(); cam(ctx, 540, 1130, 1.35 - 0.3 * pull, 0, shake_at(lf, [0], 8, 12), f)
        bedroom(ctx, lights=True, hh=7, mm=30)
        bed_back(ctx)
        cough = lf >= 30 and (lf % 20) < 8
        head_in_bed(ctx, BOY, P(eye='closed' if cough else 'shock', mouth='open' if cough else 'wavy'), 250, 1090, 110)
        ice_pack(ctx, 250, 1090, 110, -0.2)
        bed_front(ctx)
        draw_hip(ctx, 870, FLOOR - 220, 1.15, -1, MOM, P(eye='glare', mouth='flat', rsh=-130, rel=-110, lsh=130, lel=-110, head=-6))
        ctx.restore()
        if lf < 30:
            label(ctx, "\"Too sick for the TEST?\"", 540, LY + 40, 96, YEL, -0.03, pop(lf, 0, 4))
        else:
            label(ctx, "\"*cough*... SO sick.\"", 540, LY + 40, 100, (1, 1, 1), 0.03, pop(lf, 30, 34))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 36:
        # Mom ECU holding up the thermometer
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 36)), 2, shake_at(lf, [0], 8, 12), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('b98aff')); ctx.fill()
        rays(ctx, 540, 900, 240, 1600, lf * 0.02, col=(1, 1, 1), a=0.3, n=16)
        face(ctx, MOM, P(eye='smug', mouth='smile', head=0), 470, 920, 280, -0.04)
        rise = eout(pop(lf, 0, 10))
        thermo(ctx, 780, 1280 - 260 * rise, 1.25, -1.2, "98.6°")
        sparkle(ctx, 880, 820 - 260 * rise + 260, 34, (1, 1, 1))
        ctx.restore()
        label(ctx, "\"Let's check your temperature.\"", 540, LY + 40, 80, (1, 1, 1), -0.02, pop(lf, 2, 6))
    elif lf < 88:
        il = lf - 36
        # insert: kid sneaks the thermometer onto the hot lamp bulb
        ctx.save(); cam(ctx, 560, 880, 1.0 + 0.12 * eout(pop(il, 0, 52)), -4, 2 if il > 30 else 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('27306e')); ctx.fill()
        rect_r(ctx, 560, 1240, 520, 400, 16); fl(ctx, hx('c96a2a'), 8)   # nightstand
        lamp(ctx, 820, 1240, 1.1, 1.0, 0.25)
        # kid peeking from under the blanket, left
        face(ctx, BOY, P(eye='smug', mouth='grin', head=0), 290, 1120, 190, 0.25)
        blanket_chin(ctx, 290, 1180, 190)
        # arm reaching to the bulb
        hxp, hyp = 300, 610
        ctx.move_to(440, 1320); ctx.curve_to(470, 1050, 320, 850, hxp, hyp); setc(ctx, OUT); ctx.set_line_width(70); ctx.stroke()
        ctx.move_to(440, 1320); ctx.curve_to(470, 1050, 320, 850, hxp, hyp); setc(ctx, BOY['shirt']); ctx.set_line_width(56); ctx.stroke()
        val = 98.6 + 52 * ein(pop(il, 6, 40))
        thermo(ctx, hxp + 218, hyp + 67, 1.5, 0.3, f"{val:.1f}°" if val < 150 else "150°", hot=pop(il, 6, 40))
        ellipse(ctx, hxp, hyp, 46, 40); fl(ctx, BOY['skin'], 6)
        if il > 14:
            heat_waves(ctx, 820, 760, il, 1.0)
        ctx.restore()
        if il < 26:
            label(ctx, "*sneaky...*", 540, LY + 40, 100, (1, 1, 1), 0.03, pop(il, 2, 6))
        else:
            label(ctx, "*SIZZLE!*", 540, LY + 40, 120, ORANGE, -0.04, pop(il, 26, 30))
    else:
        il = lf - 88
        # Mom ECU reads it: thermometer smoking in the foreground
        ctx.save(); cam(ctx, 540, 1000, 1.05 + 0.06 * eout(pop(il, 0, 30)), -3, shake_at(il, [0], 12, 18), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8a1f')); ctx.fill()
        rays(ctx, 540, 900, 240, 1600, il * 0.04, col=(1, 1, 0.7), a=0.45, n=18)
        face(ctx, MOM, P(eye='shock', mouth='flat', head=0), 540, 820, 270, 0.04)
        thermo(ctx, 540, 1230, 2.2, -0.08, "150°", hot=1.0)
        heat_waves(ctx, 640, 1170, il, 1.4)
        ctx.restore()
        label(ctx, "\"...150 DEGREES?!\"", 540, LY + 40, 110, YEL, 0.03, pop(il, 2, 6))
    card(ctx, 'p2', f, 146, 228)


def s3(ctx, f):
    lf = f - 230
    if lf < 52:
        # Mom, sweetly: you'll miss the PIZZA PARTY (thought bubble)
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 52)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb0d8')); ctx.fill()
        rays(ctx, 540, 900, 240, 1600, lf * 0.02, col=(1, 1, 1), a=0.35, n=16)
        face(ctx, MOM, P(eye='smug' if lf < 26 else 'happy', mouth='smile', head=0), 400, 1060, 270, -0.06)
        u = eout(pop(lf, 6, 16))
        if u > 0:
            ctx.save(); ctx.translate(780, 720); ctx.scale(u, u); ctx.translate(-780, -720)
            bubble(ctx, 780, 720, 210, 180, ((620, 930, 26), (580, 990, 18)))
            pizza(ctx, 780, 700, 0.95, 0.15 * math.sin(lf * 0.2))
            for k in range(3):
                sparkle(ctx, 640 + k * 140, 560 + 60 * (k % 2), 20 + 6 * math.sin(lf * 0.4 + k), YEL)
            ctx.restore()
        ctx.restore()
        if lf < 26:
            label(ctx, "\"Oh no... then you'll MISS...\"", 540, LY + 40, 84, (1, 1, 1), -0.02, pop(lf, 2, 6))
        else:
            label(ctx, "\"...the PIZZA PARTY.\"", 540, LY + 40, 104, YEL, 0.03, pop(lf, 26, 30))
    elif lf < 70:
        il = lf - 52
        # kid ECU in bed: eyes POP
        ctx.save(); cam(ctx, 540, 1000, 1.1 + 0.1 * eout(pop(il, 0, 6)), 0, shake_at(il, [0], 10, 28), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8a1f')); ctx.fill()
        rays(ctx, 540, 950, 240, 1600, il * 0.05, col=(1, 1, 0.6), a=0.5, n=18)
        face(ctx, BOY, P(eye='shock', mouth='scream', head=0), 540, 930, 320, 0)
        for ex, ey, rx in eye_pos(540, 930, 320):
            ellipse(ctx, ex, ey, rx * 1.25, rx * 1.45); fl(ctx, (1, 1, 1), 8)
            ellipse(ctx, ex, ey, rx * 0.35, rx * 0.4); setc(ctx, INK); ctx.fill()
        ice_pack(ctx, 540, 930 - 140 * eout(pop(il, 4, 14)), 320, 0.3 * pop(il, 4, 14))
        blanket_chin(ctx, 540, 930, 320)
        ctx.restore()
        label(ctx, "\"PIZZA?!\"", 540, LY + 40, 128, (1, 1, 1), -0.04, pop(il, 0, 4))
    else:
        il = lf - 70
        # low angle: blanket flies, hero pose I'M CURED
        ctx.save(); cam(ctx, 540, 1150, 1.0, -5 + 2 * math.sin(il * 0.2), shake_at(il, [0], 12, 22), f)
        bedroom(ctx, lights=True, hh=7, mm=45)
        rays(ctx, 540, 900, 200, 1700, il * 0.04, col=(1, 0.95, 0.5), a=0.45, n=18)
        bed_back(ctx)
        bed_front(ctx)
        jump = math.sin(min(1, il / 22) * math.pi) * 260 if il < 22 else 0
        b = draw_hip(ctx, 560, 1160 - jump, 1.25, 1, BOY, P(eye='happy', mouth='grin', rsh=-160, rel=-20, lsh=160, lel=20, lhip=20, rhip=-20))
        # flying blanket
        t = pop(il, 0, 30)
        if t < 1:
            ctx.save(); ctx.translate(540 + 500 * t, 1180 - 900 * t + 900 * t * t); ctx.rotate(t * 5)
            rect_r(ctx, -260, -90, 520, 180, 40); fl(ctx, hx('3ccfb0'), 8); ctx.restore()
        ip = eout(pop(il, 0, 8))
        ctx.save(); ctx.translate(560 - 300 * ip, 900 - 600 * ip + 900 * ip * ip); ctx.rotate(ip * 4)
        rect_r(ctx, -60, -25, 120, 50, 18); fl(ctx, hx('7fd4ff'), 5); ctx.restore()
        for j in range(6):
            sparkle(ctx, 560 + 330 * math.cos(il * 0.12 + j), 800 + 300 * math.sin(il * 0.12 + j), 26 + 8 * math.sin(il * 0.4 + j), YEL)
        ctx.restore()
        if il < 34:
            label(ctx, "\"I'M CURED!!\"", 540, LY + 40, 128, YEL, -0.04, pop(il, 1, 5))
        else:
            label(ctx, "\"IT'S A MIRACLE!\"", 540, LY + 40, 112, (1, 1, 1), 0.04, pop(il, 34, 38))
    card(ctx, 'p3', f, 256, 366)


def s4(ctx, f):
    lf = f - 370
    if lf < 56:
        # classroom wide: chalkboard says MATH TEST, kid in the doorway with a party hat
        push = eout(pop(lf, 20, 56))
        ctx.save(); cam(ctx, 540, 1010 - 20 * push, 0.95 + 0.1 * push, 0, shake_at(lf, [20], 12, 20), f)
        classroom(ctx)
        for x in (230, 560):
            desk(ctx, x, 1260, 290)
        dropped = lf >= 20
        b = draw_hip(ctx, 830, FLOOR - 165, 0.98, -1, BOY, P(eye='happy' if not dropped else 'shock', mouth='grin' if not dropped else 'wavy',
                                                             rsh=-150 if not dropped else 10, rel=-20 if not dropped else -5, lsh=150 if not dropped else -10, lel=20))
        hx_, hy_ = b['head']; R = b['R']
        poly(ctx, [(hx_ - 0.45 * R, hy_ - 0.85 * R), (hx_ + 0.35 * R, hy_ - 0.9 * R), (hx_ - 0.1 * R, hy_ - 2.0 * R)]); fl(ctx, PINK, 6)
        ellipse(ctx, hx_ - 0.1 * R, hy_ - 2.0 * R, 16, 16); fl(ctx, YEL, 4)
        ctx.restore()
        if lf < 20:
            label(ctx, "\"PIZZA TIME!!\"", 540, LY + 40, 116, YEL, -0.03, pop(lf, 0, 4))
        else:
            label(ctx, "\"...where's the PIZZA?\"", 540, LY + 40, 96, (1, 1, 1), 0.03, pop(lf, 20, 24))
    else:
        il = lf - 56
        # split screen: kid melting at his desk (top) / Mom at home, coffee + wave (bottom)
        ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
        ctx.save(); cam(ctx, 540, 640, 1.0, 0, shake_at(il, [0], 8, 12), f, sy=520)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('8fd8c0')); ctx.fill()
        rect_r(ctx, 160, 380, 760, 150, 12); fl(ctx, hx('1f5a40'), 8)
        chalk(ctx, "MATH TEST", 540, 458, 92, -0.02)
        melt = eout(pop(il, 4, 40))
        face(ctx, BOY, P(eye='shock', mouth='wavy', head=0), 470, 760 + 50 * melt, 180, 0.05)
        sweat(ctx, 630, 640 + 50 * melt, il, 1.1)
        rect_r(ctx, -100, 960, 1300, 300, 10); fl(ctx, hx('ffb85a'), 8)
        test_paper(ctx, 790, 900, 0.8, 0.12)
        ctx.restore(); ctx.restore()
        ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
        ctx.save(); cam(ctx, 540, 1360, 1.0, 0, 0, f, sy=1440)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd36e')); ctx.fill()
        for i in range(-10, 20):
            for j in range(0, 30):
                ellipse(ctx, i * 130 + (j % 2) * 65, 900 + j * 120, 12, 12); setc(ctx, dark(hx('ffd36e'), 0.92)); ctx.fill()
        wave = math.sin(il * 0.5)
        face(ctx, MOM, P(eye='happy' if (il // 12) % 2 else 'smug', mouth='smile', head=0), 470, 1210, 200, -0.05)
        mug(ctx, 250, 1500, 0.9)
        ctx.save(); ctx.translate(760, 1220); ctx.rotate(0.3 * wave)
        ellipse(ctx, 0, 0, 60, 70); fl(ctx, MOM['skin'], 6)
        for k in range(4):
            rect_r(ctx, -50 + k * 28, -120, 22, 70, 11); fl(ctx, MOM['skin'], 5)
        ctx.restore()
        ctx.restore(); ctx.restore()
        ctx.rectangle(0, 948, W, 24); setc(ctx, OUT); ctx.fill()
        label(ctx, "\"MATH?!\"", 540, 890, 96, (1, 1, 1), -0.03, pop(il, 0, 4))
        label(ctx, "\"Good luck, sweetie!\"", 540, LY + 40, 92, YEL, 0.03, pop(il, 10, 14))
    card(ctx, 'p4', f, 380, 424)


def s5(ctx, f):
    lf = f - 500
    if lf < 72:
        # that evening: Dad with a spatula, Mom in bed with ice pack, thermometer, lamp glowing under HER blanket
        ctx.save(); cam(ctx, 540, 1140, 1.15, 0, shake_at(lf, [30], 8, 12), f)
        bedroom(ctx, lights=False, hh=6, mm=0)
        bed_back(ctx)
        cough = lf >= 30 and (lf % 20) < 8
        head_in_bed(ctx, MOM, P(eye='closed' if cough else 'normal', mouth='open' if cough else 'wavy'), 250, 1090, 110)
        ice_pack(ctx, 250, 1090, 110, -0.2)
        thermo(ctx, 330, 1150, 0.5, 0.5, "150°", hot=1.0)
        bed_front(ctx)
        g = cairo.RadialGradient(560, 1260, 20, 560, 1260, 360)
        g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.8); g.add_color_stop_rgba(1, 1, 0.9, 0.4, 0)
        ctx.set_source(g); ctx.arc(560, 1260, 360, 0, 2 * math.pi); ctx.fill()
        ctx.move_to(600, 1330); ctx.curve_to(700, 1440, 760, 1400, 1100, 1450); ink(ctx, 8); ctx.stroke()   # lamp cord
        if lf >= 30:
            heat_waves(ctx, 420, 1080, lf, 0.8)
        b = draw_hip(ctx, 800, FLOOR - 230, 1.1, -1, DAD, P(eye='happy', mouth='grin', rsh=-60, rel=-90, lsh=20, lel=-20))
        spatula(ctx, b['front'][0], b['front'][1], -0.3, 0.9)
        ctx.restore()
        if lf < 30:
            label(ctx, "\"Honey, YOUR turn to cook!\"", 540, LY + 40, 86, YEL, -0.03, pop(lf, 2, 6))
        else:
            label(ctx, "\"*cough* I'm SO sick...\"", 540, LY + 40, 96, PINK, 0.03, pop(lf, 30, 34))
    elif lf < 126:
        il = lf - 72
        # kid ECU, arms crossed, smug: NICE TRY, MOM. (Mom inset, caught)
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(il, 0, 54)), 2, shake_at(il, [0], 8, 12), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('22b45a')); ctx.fill()
        rays(ctx, 540, 900, 240, 1500, il * 0.02, col=(1, 1, 1), a=0.35, n=16)
        face(ctx, BOY, P(eye='smug', mouth='smile', head=0), 520, 900, 290, -0.06)
        thermo(ctx, 560, 1300, 1.4, -0.15, "150°", hot=1.0)
        ctx.restore()
        label(ctx, "\"NICE TRY, MOM.\"", 540, LY + 40, 116, YEL, -0.03, pop(il, 2, 6))
        if il >= 16:
            u = eout(pop(il, 16, 24))
            ctx.save(); ctx.translate(810 + 320 * (1 - u), 660)
            ellipse(ctx, 0, 0, 120, 120); fl(ctx, YEL, 8); ctx.save(); ellipse(ctx, 0, 0, 112, 112); ctx.clip()
            face(ctx, MOM, P(eye='shock', mouth='wavy', head=0), 0, 10, 82, 0.05)
            ice_pack(ctx, 0, 10, 82, 0.05)
            ctx.restore(); ctx.restore()
    else:
        il = lf - 126
        opening_face(ctx, f, il, True)
    if lf < 126:
        card(ctx, 'p5', f, 504, 622)
    else:
        card(ctx, 'p1', f, 626)


SHOTS = [(0, s1), (110, s2), (230, s3), (370, s4), (500, s5)]
CUTS = (52, 110, 146, 198, 230, 282, 300, 370, 426, 500, 572, 626)


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
                              "-i", "out/faking_sick_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
