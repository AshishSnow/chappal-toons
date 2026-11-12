"""'Dad vs The AC Remote' - Chappal Toons original, ~35s."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import cam, pop, sparkle, puff, label, shake_at, room, sofa_back, sofa_front, coffee_table, run_pose
from scenes7 import bedroom, night
from scenes8 import head_of, sit, walk, glare_aura

BOY, MOM, DAD = doodle.BOY, doodle.MOM, doodle.DAD
N = 1050
STAND = 1500
SEAT = 1235
KB, KD, KM = 1.5, 1.75, 1.75

CAPS = {
    'p1': [[("WHAT HAPPENS WHEN", OUT)], [("I TOUCH THE ", OUT), ("AC REMOTE", hx('1f8bff')), ("?", OUT)]],
    'p2': [[("DAD:", OUT)], [("ELECTRICITY BILL ", hx('e0123a')), ("LECTURE", OUT)]],
    'p3': [[("2 AM:", hx('7a3cff'))], [("DAD'S ROOM...", OUT)]],
    'p4': [[("RULES ARE", OUT)], [("ONLY FOR KIDS", hx('ff3b5c'))]],
}


def card(ctx, key, f, appear, gone=10 ** 9):
    u = min(pop(f, appear, appear + 6), 1 - pop(f, gone - 5, gone))
    if u <= 0:
        return
    lines = CAPS[key]; size = 72
    ctx.save()
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    widths = [sum(ctx.text_extents(t).x_advance for t, _ in ln) for ln in lines]
    w = max(widths) + 70; lh = size * 1.18; h = lh * len(lines) + 40
    s = 0.7 + 0.3 * eout(u)
    ctx.translate(W / 2, 300 + h / 2); ctx.scale(s, s)
    ctx.rectangle(-w / 2 + 8, -h / 2 + 10, w, h); setc(ctx, (0, 0, 0, 0.35 * u)); ctx.fill()
    ctx.rectangle(-w / 2, -h / 2, w, h); setc(ctx, (1, 1, 1, 0.97 * u)); ctx.fill_preserve(); setc(ctx, OUT + (u,)); ctx.set_line_width(5); ctx.stroke()
    y = -h / 2 + 20 + size * 0.92
    for ln, lw_ in zip(lines, widths):
        x = -lw_ / 2
        for t, col in ln:
            ctx.move_to(x, y); ctx.text_path(t); setc(ctx, col[:3] + (u,)); ctx.fill()
            x += ctx.text_extents(t).x_advance
        y += lh
    ctx.restore()


# ------------------------------------------------------------------ props & fx
def ac_unit(ctx, x, y, temp, on=True, s=1.0, f=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-200, -60); ctx.line_to(200, -60); ctx.curve_to(215, -60, 215, 50, 200, 60); ctx.line_to(-200, 60); ctx.curve_to(-215, 50, -215, -60, -200, -60)
    fl(ctx, (1, 1, 1), 7)
    ctx.rectangle(-180, 30, 360, 14); fl(ctx, hx('dfe6f2'), 4)
    ctx.rectangle(110, -35, 70, 40); fl(ctx, hx('1e2a3a'), 4)
    text(ctx, f"{temp}", 145, -14, 30, hx('6be2ff') if on else hx('445566'), outline=hx('1e2a3a'), ow=1, shadow=False)
    ellipse(ctx, -160, -30, 7, 7); setc(ctx, hx('5fd07a') if on else hx('aa3344')); ctx.fill()
    ctx.restore()
    if on and temp <= 20:
        for i in range(5):
            t = ((f + i * 7) % 30) / 30
            yy = y + 70 * s + t * 260 * s
            ctx.new_path(); ctx.move_to(x - 160 * s + i * 80 * s, yy); ctx.curve_to(x - 140 * s + i * 80 * s, yy + 30, x - 180 * s + i * 80 * s, yy + 60, x - 160 * s + i * 80 * s, yy + 90)
            setc(ctx, (0.75, 0.92, 1, 0.8 * (1 - t))); ctx.set_line_width(8 * s); ctx.stroke()


def remote(ctx, x, y, a, s=1.0, temp=None, glow=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 10, 0, 0, 220); g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.8 * glow); g.add_color_stop_rgba(1, 1, 0.9, 0.4, 0)
        ctx.set_source(g); ellipse(ctx, 0, 0, 220, 220); ctx.fill()
    ctx.new_path(); ctx.move_to(-40, -110); ctx.line_to(40, -110); ctx.line_to(46, 110); ctx.line_to(-46, 110); ctx.close_path(); fl(ctx, (1, 1, 1), 6)
    ctx.rectangle(-30, -95, 60, 40); fl(ctx, hx('1e2a3a'), 3)
    if temp is not None:
        text(ctx, f"{temp}", 0, -75, 26, hx('6be2ff'), outline=hx('1e2a3a'), ow=1, shadow=False)
    for i, c in enumerate((hx('ff3b5c'), hx('3fb6ff'), hx('3fb6ff'))):
        ellipse(ctx, 0 if i == 0 else (-16 if i == 1 else 16), -25 if i == 0 else 20, 14, 14); fl(ctx, c, 3)
    for r in range(2):
        for c_ in range(3):
            ellipse(ctx, -22 + c_ * 22, 60 + r * 26, 7, 7); setc(ctx, hx('c7cede')); ctx.fill()
    ctx.restore()


def big_remote(ctx, f, temp, beep=False):
    ctx.rectangle(0, 0, W, H); setc(ctx, hx('ffd34f')); ctx.fill()
    for i in range(18):
        a = i * math.pi / 9 + f * 0.01
        ctx.move_to(540, 1000); ctx.line_to(540 + math.cos(a) * 2000, 1000 + math.sin(a) * 2000); ctx.line_to(540 + math.cos(a + 0.17) * 2000, 1000 + math.sin(a + 0.17) * 2000); ctx.close_path()
    setc(ctx, hx('ffe38a')); ctx.fill()
    ctx.save(); ctx.translate(540, 1050); ctx.rotate(-0.05); ctx.scale(3.4, 3.4)
    ctx.new_path(); ctx.move_to(-80, -200); ctx.line_to(80, -200); ctx.line_to(90, 200); ctx.line_to(-90, 200); ctx.close_path(); fl(ctx, (1, 1, 1), 3)
    ctx.rectangle(-62, -175, 124, 80); fl(ctx, hx('1e2a3a'), 2)
    text(ctx, f"{temp}°", 0, -134, 56, hx('6be2ff'), outline=hx('1e2a3a'), ow=1, shadow=False)
    for i, (bx, by, c) in enumerate(((0, -40, hx('ff3b5c')), (-36, 40, hx('3fb6ff')), (36, 40, hx('3fb6ff')))):
        ellipse(ctx, bx, by, 26 if not (beep and i == 1) else 22, 26 if not (beep and i == 1) else 22); fl(ctx, c, 2)
    text(ctx, "-", -36, 38, 30, (1, 1, 1), ow=1, shadow=False); text(ctx, "+", 36, 38, 30, (1, 1, 1), ow=1, shadow=False)
    ctx.restore()


def fan(ctx, x, y, spin, speed=1.0):
    ctx.rectangle(x - 8, y - 200, 16, 200); fl(ctx, hx('c7cede'), 4)
    ctx.save(); ctx.translate(x, y)
    for i in range(3):
        a = spin + i * 2 * math.pi / 3
        ctx.save(); ctx.scale(1, 0.25); ctx.rotate(a)
        ellipse(ctx, 170, 0, 160, 36); fl(ctx, hx('f2f2f2'), 5)
        ctx.restore()
    if speed > 0.6:
        ellipse(ctx, 0, 0, 330, 82); setc(ctx, (1, 1, 1, 0.35)); ctx.fill()
    ellipse(ctx, 0, 0, 40, 28); fl(ctx, hx('c7cede'), 5)
    ctx.restore()


def heat(ctx, f, a=1.0):
    if a <= 0:
        return
    ctx.rectangle(0, 0, W, H); setc(ctx, (1, 0.45, 0.1, 0.18 * a)); ctx.fill()
    setc(ctx, (1, 0.6, 0.2, 0.45 * a)); ctx.set_line_width(7)
    for i in range(7):
        y0 = 700 + i * 160 - (f * 6) % 160
        ctx.new_path(); ctx.move_to(60, y0)
        for k in range(12):
            ctx.rel_curve_to(30, -25, 50, 25, 80, 0)
        ctx.stroke()


def frost(ctx, f, a=1.0):
    if a <= 0:
        return
    ctx.rectangle(0, 0, W, H); setc(ctx, (0.55, 0.85, 1, 0.22 * a)); ctx.fill()
    rnd = random.Random(3)
    for i in range(40):
        x = rnd.uniform(0, W); sp = rnd.uniform(3, 7)
        y = (rnd.uniform(0, H) + f * sp) % H
        r = rnd.uniform(10, 20)
        setc(ctx, (1, 1, 1, 0.9 * a)); ctx.set_line_width(3)
        for k in range(3):
            ang = k * math.pi / 3 + f * 0.05
            ctx.move_to(x - math.cos(ang) * r, y - math.sin(ang) * r); ctx.line_to(x + math.cos(ang) * r, y + math.sin(ang) * r)
        ctx.stroke()
    g = cairo.RadialGradient(W / 2, H / 2, 500, W / 2, H / 2, 1100); g.add_color_stop_rgba(0, 1, 1, 1, 0); g.add_color_stop_rgba(1, 0.85, 0.95, 1, 0.7 * a)
    ctx.set_source(g); ctx.paint()


def sweat_drops(ctx, f, pts, s=1.5):
    for i, (x, y) in enumerate(pts):
        t = ((f + i * 6) % 18) / 18
        sweat(ctx, x, y + t * 220, s)


def bill(ctx, x, y, unroll):
    L = 80 + 900 * unroll
    ctx.rectangle(x - 150, y, 300, L); fl(ctx, (1, 1, 1), 6)
    text(ctx, "ELECTRICITY BILL", x, y + 50, 34, hx('e0123a'), outline=INK, ow=0.5, shadow=False)
    for i in range(int((L - 120) / 50)):
        ctx.rectangle(x - 120, y + 100 + i * 50, 160 if i % 2 else 200, 12); setc(ctx, hx('b8bfcc')); ctx.fill()
    if unroll > 0.7:
        text(ctx, "RS. 8,990!!", x, y + L - 60, 54, hx('e0123a'), outline=INK, ow=4, shadow=False)
    ellipse(ctx, x, y + L, 160, 26); fl(ctx, hx('eeeeee'), 5)


def study_set(ctx):
    ctx.rectangle(-900, -900, W + 1800, 2200); ctx.set_source(vgrad(ctx, 0, 0, 0, 1250, [(0, hx('fff1c9')), (1, hx('ffe2a0'))])); ctx.fill()
    ctx.rectangle(600, 560, 380, 520); fl(ctx, hx('a86c3a'), 8)
    cols = [hx('ff5a5a'), hx('3f8bff'), hx('5fd07a'), hx('ffd23f'), hx('b06bff')]
    for r in range(3):
        ctx.rectangle(620, 720 + r * 160, 340, 14); fl(ctx, hx('7a4a2c'), 3)
        for i in range(6):
            ctx.rectangle(630 + i * 52, 640 + r * 160, 40, 80); fl(ctx, cols[(i + r) % 5], 3)
    ctx.rectangle(-900, 1250, W + 1800, 1600); setc(ctx, hx('d8b48a')); ctx.fill()
    ctx.move_to(-900, 1250); ctx.line_to(W + 900, 1250); ink(ctx, 8); ctx.stroke()


def armchair(ctx, front=False):
    if not front:
        ctx.new_path(); ctx.move_to(130, 1250); ctx.line_to(130, 900); ctx.curve_to(130, 820, 560, 820, 560, 900); ctx.line_to(560, 1250); ctx.close_path(); fl(ctx, hx('8a3cff'), 8)
    else:
        ctx.rectangle(110, 1240, 470, 110); fl(ctx, hx('7a2cef'), 8)
        for x in (90, 520):
            ctx.rectangle(x, 1100, 90, 260); fl(ctx, hx('6a1cdf'), 8)


def newspaper(ctx, x, y, a=0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.rectangle(-170, -120, 340, 240); fl(ctx, hx('f4f1e8'), 6)
    ctx.move_to(0, -120); ctx.line_to(0, 120); ink(ctx, 4); ctx.stroke()
    text(ctx, "NEWS", -85, -85, 34, INK, outline=INK, ow=0.5, shadow=False)
    for i in range(6):
        ctx.rectangle(-150, -50 + i * 26, 120, 9); ctx.rectangle(20, -95 + i * 32, 130, 9)
    setc(ctx, hx('9aa0ad')); ctx.fill()
    ctx.restore()


def fridge(ctx, open_=1.0, f=0):
    ctx.rectangle(600, 520, 420, 980); fl(ctx, hx('dff6ff'), 8)
    if open_ > 0:
        ctx.rectangle(625, 545, 370, 930); ctx.set_source(vgrad(ctx, 0, 545, 0, 1475, [(0, hx('ffffff')), (1, hx('bfe8ff'))])); ctx.fill()
        for yy in (760, 980, 1200):
            ctx.rectangle(625, yy, 370, 12); fl(ctx, hx('b8d8ee'), 3)
        ellipse(ctx, 700, 730, 40, 26); fl(ctx, hx('ff8a3d'), 4); ellipse(ctx, 850, 950, 60, 30); fl(ctx, hx('5fd07a'), 4)
        ctx.rectangle(880, 1110, 60, 90); fl(ctx, (1, 1, 1), 4)
        for i in range(4):
            t = ((f + i * 8) % 32) / 32
            ellipse(ctx, 700 + i * 70, 1450 + t * 60, 60 + 30 * t, 22); setc(ctx, (1, 1, 1, 0.6 * (1 - t))); ctx.fill()
        poly(ctx, [(1020, 520), (1180, 470), (1180, 1550), (1020, 1500)]); fl(ctx, hx('cdeefc'), 8)
    else:
        ctx.rectangle(600, 520, 420, 330); fl(ctx, hx('dff6ff'), 8)
    g = cairo.RadialGradient(810, 1000, 50, 810, 1000, 700); g.add_color_stop_rgba(0, 0.8, 0.95, 1, 0.5 * open_); g.add_color_stop_rgba(1, 0.8, 0.95, 1, 0)
    ctx.set_source(g); ctx.paint()


def kitchen(ctx):
    ctx.rectangle(-900, -900, W + 1800, 2200); setc(ctx, hx('fff6e8')); ctx.fill()
    setc(ctx, hx('ffd6a8')); ctx.set_line_width(3)
    for i in range(-10, 20):
        ctx.move_to(i * 90, 500); ctx.line_to(i * 90, 1100)
    for j in range(7):
        ctx.move_to(-900, 500 + j * 90); ctx.line_to(W + 900, 500 + j * 90)
    ctx.stroke()
    ctx.rectangle(-200, 1100, 760, 400); fl(ctx, hx('3fb6a8'), 8)
    ctx.rectangle(-220, 1080, 800, 30); fl(ctx, hx('e8e8f0'), 6)
    ctx.rectangle(-900, 1500, W + 1800, 600); setc(ctx, hx('e3c9a8')); ctx.fill()
    ctx.move_to(-900, 1500); ctx.line_to(W + 900, 1500); ink(ctx, 8); ctx.stroke()


def radar(ctx, x, y, t):
    for i in range(3):
        u = (t + i / 3) % 1
        ellipse(ctx, x, y, 80 + 500 * u, 80 + 500 * u); setc(ctx, (1, 0.25, 0.2, 0.8 * (1 - u))); ctx.set_line_width(10); ctx.stroke()


def blanket(ctx, x0, x1, y, b=0, col=hx('3f7bff')):
    ctx.new_path(); ctx.move_to(x0, y + 60); ctx.curve_to(x0, y - 90 - b, x1, y - 110 - b, x1, y + 60); ctx.close_path()
    fl(ctx, col, 7)
    setc(ctx, light(col, 0.3)); ctx.set_line_width(5)
    for i in range(1, 5):
        xx = lerp(x0, x1, i / 5)
        ctx.move_to(xx, y - 60 - b); ctx.line_to(xx, y + 50)
    ctx.stroke()


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 34:
        pose = sit(eye='closed', mouth='open', sq=0.08 * math.sin(f * 0.4), torso=-14, lsh=10, rsh=-10, lel=0, rel=0)
        (hxp, hyp), R = head_of(430, SEAT - (186 - 68 * 1.35) * KB, KB, 1, BOY, pose)
        ctx.save(); cam(ctx, hxp + 10, hyp + 100, 2.4, 0, 0, f)
        room(ctx, f); sofa_back(ctx); draw_hip(ctx, 430, SEAT, KB, 1, BOY, pose); sofa_front(ctx); ctx.restore()
        heat(ctx, f, 1.0)
        sweat_drops(ctx, f, [(250, 820), (820, 760), (300, 1040), (800, 1000), (540, 700)], 2.0)
        label(ctx, "45°C!!!", 540, 1500, 150, hx('ff5a1f'), -0.06, pop(f, 2, 7))
    else:
        melt = 0.12 * math.sin(f * 0.3)
        pose = sit(eye='closed' if f < 78 else 'shock', mouth='open', torso=-18 + 4 * math.sin(f * 0.2), head=-10, lsh=-30, lel=-20, rsh=40, rel=-20, lhip=70, lkn=-30, rhip=74, rkn=-30, sq=melt)
        ctx.save(); cam(ctx, 560, 1100, 1.05, 0, 0, f)
        room(ctx, f); sofa_back(ctx); fan(ctx, 540, 480, f * 0.06, 0.2)
        draw_hip(ctx, 430, SEAT, KB, 1, BOY, pose); sofa_front(ctx); coffee_table(ctx)
        remote(ctx, 930, 1360, 1.4, 0.7, glow=pop(f, 76, 86))
        ctx.restore()
        heat(ctx, f, 1.0)
        sweat_drops(ctx, f, [(300, 900), (520, 860), (640, 980)], 1.4)
        if 40 <= f < 76:
            label(ctx, "*FAN CREAKING*", 540, 1520, 76, hx('ffe14d'), 0.03, pop(f, 40, 46))
        if f >= 80:
            sparkle(ctx, 880, 1330, 70 * abs(math.sin(f * 0.4)), (1, 1, 1))
            label(ctx, "THE REMOTE!", 540, 1520, 110, hx('8fe9ff'), -0.04, pop(f, 80, 85))
    card(ctx, 'p1', f, 2, 248)


def s2(ctx, f):
    lf = f - 100
    if lf < 32:
        u = ease(pop(lf, 0, 30))
        ctx.save(); cam(ctx, 860, 1250, 1.9, 0, 0, f)
        room(ctx, f); sofa_back(ctx); sofa_front(ctx); coffee_table(ctx)
        remote(ctx, 930, 1360, 1.4, 0.7, glow=1.0)
        hx_, hy_ = lerp(640, 905, u), lerp(1180, 1340, u)
        ctx.new_path(); ctx.move_to(500, 1150); ctx.line_to(hx_, hy_); setc(ctx, INK); ctx.set_line_width(40 + 10); ctx.stroke_preserve(); setc(ctx, BOY['skin']); ctx.set_line_width(36); ctx.stroke()
        ellipse(ctx, hx_, hy_, 30, 30); fl(ctx, BOY['skin'], 5)
        ctx.restore()
        label(ctx, "*SLOW MOTION*", 540, 1520, 76, (1, 1, 1), 0.03, 1)
    elif lf < 76:
        temp = max(16, 24 - int((lf - 32) / 5))
        big_remote(ctx, f, temp, beep=(lf - 32) % 5 < 2)
        if (lf - 32) % 5 < 2:
            label(ctx, "BEEP!", 820, 760, 80, hx('ff3b5c'), 0.1, 1)
        if temp == 16:
            label(ctx, "16°C", 540, 1560, 140, hx('3fb6ff'), -0.04, pop(lf, 72, 76))
    else:
        ctx.save(); cam(ctx, 560, 1080, kf(lf, [(76, 1.0), (150, 1.12)]), 0, 0, f)
        room(ctx, f); sofa_back(ctx); ac_unit(ctx, 560, 470, 16, True, 1.0, f)
        pose = sit(eye='happy', mouth='grin', torso=-20, head=-12, lsh=-170, lel=-80, rsh=-165, rel=-80, lhip=78, lkn=-10, rhip=82, rkn=-8)
        draw_hip(ctx, 430, SEAT, KB, 1, BOY, pose); sofa_front(ctx); coffee_table(ctx)
        remote(ctx, 930, 1360, 1.4, 0.7)
        ctx.restore()
        frost(ctx, f, pop(lf, 76, 90))
        label(ctx, "AAAAHHH...", 540, 1520, 120, hx('8fe9ff'), -0.04, pop(lf, 80, 86))
    card(ctx, 'p1', f, 2, 248)


def s3(ctx, f):
    lf = f - 250
    if lf < 84:
        alert = lf >= 30
        ctx.save(); cam(ctx, 380, 980, kf(lf, [(0, 1.15), (30, 1.15), (40, 1.6)], eout), 0, shake_at(lf, [30], 10, 16), f)
        study_set(ctx); armchair(ctx)
        drop = ease(pop(lf, 28, 36))
        pose = sit(eye='glare' if alert else 'normal', mouth='frown' if alert else 'smile', lsh=60, lel=-70, rsh=64, rel=-74)
        h = draw_hip(ctx, 340, SEAT, KD, 1, DAD, pose)
        armchair(ctx, True)
        hx_, hy_ = h['front']
        newspaper(ctx, hx_ + 10, hy_ - 90 + 260 * drop, -0.05, 1.0)
        if alert:
            radar(ctx, h['head'][0], h['head'][1], (lf - 30) / 20)
        ctx.restore()
        if alert:
            label(ctx, "DAD SENSE: ACTIVATED", 540, 1520, 76, hx('ff3b5c'), -0.03, pop(lf, 32, 37))
            if lf % 10 < 5:
                label(ctx, "BEEP BEEP", 820, 760, 64, (1, 1, 1), 0.1, 1)
        else:
            label(ctx, "MEANWHILE...", 540, 1520, 90, (1, 1, 1), 0.03, pop(lf, 2, 8))
        if 70 <= lf < 84:
            puff(ctx, 380, 1000, pop(lf, 70, 84), 3.0)
    else:
        ctx.save(); cam(ctx, 600, 1080, 1.05, 0, shake_at(lf, [84], 10, 22), f)
        room(ctx, f, door_open=1, hall_light=1); sofa_back(ctx); ac_unit(ctx, 560, 470, 16, True, 1.0, f)
        draw_hip(ctx, 430, SEAT, KB, 1, BOY, sit(eye='shock', mouth='scream', lsh=-150, rsh=-160, lel=-30, rel=-30, torso=-10))
        sofa_front(ctx); coffee_table(ctx); remote(ctx, 930, 1360, 1.4, 0.7)
        draw(ctx, 960, STAND - 186 * KD, KD, -1, DAD, P(eye='glare', mouth='frown', lsh=40, lel=-135, rsh=35, rel=-138))
        puff(ctx, 960, 1100, pop(lf, 84, 96), 2.5)
        ctx.restore()
        frost(ctx, f, 0.6)
        label(ctx, "!!!", 420, 820, 150, hx('ff3b5c'), 0.1, pop(lf, 86, 89))


def s4(ctx, f):
    lf = f - 360
    if lf < 90:
        unroll = ease(pop(lf, 26, 66))
        ctx.save(); cam(ctx, 600, 1050, 1.15, 0, shake_at(lf, [40, 70], 8, 16), f)
        room(ctx, f); sofa_back(ctx); ac_unit(ctx, 560, 470, 16, True, 1.0, f)
        draw_hip(ctx, 330, SEAT, KB, 1, BOY, sit(eye='shock', mouth='wavy', lsh=10, rsh=-10, lel=-5, rel=-5))
        sofa_front(ctx); coffee_table(ctx)
        h = draw(ctx, 780, STAND - 186 * KD, KD, -1, DAD, P(eye='glare', mouth='scream' if lf % 14 < 9 else 'frown', lsh=40, lel=-120, rsh=100, rel=-20))
        hx_, hy_ = h['front']
        if lf < 26:
            remote(ctx, hx_, hy_ - 30, 0.2, 0.7)
        else:
            bill(ctx, hx_ - 30, hy_ - 60, unroll)
        ctx.restore()
        frost(ctx, f, 0.5 * (1 - pop(lf, 60, 90)))
        if lf < 26:
            label(ctx, "WHO SET 16?!", 540, 1540, 110, hx('ff3b5c'), -0.04, pop(lf, 2, 6))
        else:
            label(ctx, "DO YOU KNOW THE BILL?!", 540, 1600, 80, hx('ffe14d'), 0.03, pop(lf, 28, 33))
    elif lf < 130:
        temp = min(26, 16 + int((lf - 90) / 3.5))
        big_remote(ctx, f, temp, beep=(lf - 90) % 4 < 2)
        label(ctx, f"{temp}°C", 540, 1560, 130, hx('ff9a1f') if temp >= 26 else hx('3fb6ff'), -0.04, 1)
        if (lf - 90) % 4 < 2:
            label(ctx, "BEEP!", 280, 760, 80, hx('ff3b5c'), -0.1, 1)
    else:
        spin = f * (0.5 if lf > 150 else 0.1)
        ctx.save(); cam(ctx, 560, 1080, 1.05, 0, 0, f)
        room(ctx, f); sofa_back(ctx); ac_unit(ctx, 560, 470, 26, True, 1.0, f); fan(ctx, 540, 600, spin, 1.0 if lf > 150 else 0.3)
        melt = 0.1 * math.sin(f * 0.3)
        draw_hip(ctx, 330, SEAT, KB, 1, BOY, sit(eye='closed', mouth='wavy', sq=melt, torso=-12, lsh=10, rsh=-10, lel=0, rel=0))
        sofa_front(ctx); coffee_table(ctx)
        u = pop(lf, 165, 200)
        if u < 1:
            h = draw(ctx, 780 + 500 * ease(u), STAND - 186 * KD, KD, -1 if u <= 0 else 1, DAD,
                     P(eye='glare', mouth='frown', lsh=40, lel=-120, rsh=-150 if lf < 165 else 30, rel=-20 if lf < 165 else -100) if u <= 0 else walk(lf * 0.5, eye='smug', mouth='smile'))
            if lf < 165:
                hx_, hy_ = h['front']; remote(ctx, hx_, hy_ - 40, 0.3, 0.7)
        ctx.restore()
        heat(ctx, f, pop(lf, 130, 160))
        sweat_drops(ctx, f, [(240, 900), (480, 860)], 1.4)
        if lf < 165:
            label(ctx, "FAN IS ENOUGH!", 540, 1540, 110, hx('ffe14d'), -0.04, pop(lf, 132, 137))
        else:
            label(ctx, "*REMOTE CONFISCATED*", 540, 1540, 70, (1, 1, 1), 0.03, pop(lf, 166, 171))
    card(ctx, 'p2', f, 364, 558)


def s5(ctx, f):
    lf = f - 560
    if lf < 50:
        ctx.save(); cam(ctx, 1120, 1120, 1.05, 0, 0, f)
        bedroom(ctx, f, 2.0, False, 0, None, 0, 120)
        b = 0
        h = draw_hip(ctx, 1230, 1215, KB, 1, BOY, P(rot=-90, head=-6, lsh=-170, lel=-30, rsh=-60, rel=-80, lhip=4, lkn=-6, rhip=10, rkn=-12, eye='normal', mouth='wavy'))
        ctx.restore()
        night(ctx, 0.85)
        heat(ctx, f, 0.5)
        sweat_drops(ctx, f, [(500, 900), (380, 960)], 1.4)
        label(ctx, "CAN'T SLEEP...", 540, 1520, 100, hx('ff9a5a'), 0.03, pop(lf, 4, 10))
    elif lf < 100:
        # sneaking down the dark hallway
        ctx.rectangle(0, 0, W, H); ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('1b2050')), (1, hx('2a2f6a'))])); ctx.fill()
        ctx.rectangle(0, 1450, W, 470); setc(ctx, hx('161a3e')); ctx.fill()
        ctx.rectangle(760, 620, 260, 830); fl(ctx, hx('3a3f7a'), 8)
        ctx.rectangle(785, 1440, 210, 14); setc(ctx, hx('9fe8ff')); ctx.fill()
        u = pop(lf, 50, 100)
        x = lerp(80, 620, u)
        ph = lf * 0.45
        pose = run_pose(ph, torso=24, eye='smug', mouth='flat', lsh=-60 + 20 * math.sin(ph), lel=-80, rsh=40, rel=-110)
        pose['lhip'] *= 0.6; pose['rhip'] *= 0.6
        draw(ctx, x, 1450 + 40 - 186 * KB, KB, 1, BOY, pose)
        label(ctx, "MISSION: REMOTE", 540, 1650, 92, hx('5fd07a'), -0.03, pop(lf, 52, 58))
        if lf % 16 < 8:
            label(ctx, "TIPTOE...", 300, 900, 70, (1, 1, 1), 0.06, 1)
    else:
        ctx.save(); cam(ctx, kf(lf, [(100, 1060), (130, 1060)]), 1100, kf(lf, [(100, 1.0), (130, 1.08), (200, 1.15)]), 0, 0, f)
        bedroom(ctx, f, 2.0, False, 0, None, 0, 120)
        ac_unit(ctx, 1150, 560, 16, True, 1.0, f)
        b = 6 * math.sin(lf * 0.12)
        draw_hip(ctx, 1330, 1215, KD, 1, DAD, P(rot=-90, head=-6, lsh=-170, lel=-30, rsh=-60, rel=-80, lhip=4, lkn=-6, rhip=10, rkn=-12, eye='closed', mouth='open'))
        blanket(ctx, 1180, 1580, 1215, b)
        for i in range(5):
            poly(ctx, [(820 + i * 160, 1160), (850 + i * 160, 1160), (835 + i * 160, 1230 + (i % 2) * 30)]); fl(ctx, hx('dff6ff'), 4)
        draw(ctx, 640, STAND - 186 * KB, KB, 1, BOY, P(eye='shock', mouth='scream', lsh=-150, rsh=-160, lel=-30, rel=-30, torso=-10))
        ctx.restore()
        night(ctx, 0.55)
        frost(ctx, f, 0.8)
        for i in range(3):
            t = ((lf + i * 20) % 60) / 60
            label(ctx, "Z", 700 + i * 60, 900 - t * 260, 70 + i * 16, (1, 1, 1), 0.2, 1)
        label(ctx, "16°C?!", 760, 760, 120, hx('3fb6ff'), 0.08, pop(lf, 108, 112))
        label(ctx, "WHAT?!", 540, 1540, 140, hx('ff3b5c'), -0.05, pop(lf, 116, 120))
        card(ctx, 'p3', f, 664, 758)


def s6(ctx, f):
    lf = f - 760
    ctx.save()
    if lf < 70:
        cam(ctx, 1000, 1120, kf(lf, [(0, 1.3), (20, 2.0)], eout), 0, shake_at(lf, [20], 8, 12), f)
    else:
        cam(ctx, 1000, 1100, 1.0, 0, 0, f)
    bedroom(ctx, f, 2.0, False, 0, None, 0, 125)
    ac_unit(ctx, 1150, 560, 16, True, 1.0, f)
    eye = 'closed' if lf < 18 else 'glare'
    cover = ease(pop(lf, 90, 104))
    draw_hip(ctx, 1330, 1215, KD, 1, DAD, P(rot=-90, head=-6, lsh=-170, lel=-30, rsh=-60, rel=-80, lhip=4, lkn=-6, rhip=10, rkn=-12, eye=eye, mouth='frown' if lf >= 18 else 'open'))
    blanket(ctx, lerp(1180, 820, cover), 1580, 1215, 0)
    if lf >= 70:
        u = pop(lf, 104, 140)
        bx = lerp(640, 100, ease(u))
        draw(ctx, bx, STAND - 186 * KB, KB, -1 if u > 0 else 1, BOY, P(eye='normal', mouth='flat', rsh=-150, rel=-115, lsh=6) if u <= 0 else walk(lf * 0.4, eye='normal', mouth='flat'))
    ctx.restore()
    night(ctx, 0.55)
    frost(ctx, f, 0.6)
    if 20 <= lf < 70:
        label(ctx, "26 IS FOR KIDS.", 540, 1440, 96, hx('ffe14d'), -0.03, pop(lf, 22, 27))
        label(ctx, "GO TO SLEEP!", 540, 1560, 110, hx('ff3b5c'), 0.03, pop(lf, 34, 39))
    if lf >= 104:
        label(ctx, "...OKAY.", 540, 1520, 100, (1, 1, 1), 0.02, pop(lf, 106, 111))
    card(ctx, 'p4', f, 784, 898)


def s7(ctx, f):
    lf = f - 900
    ctx.save(); cam(ctx, 720, 1120, 1.08, 0, shake_at(lf, [100], 12, 28), f)
    kitchen(ctx); fridge(ctx, 1.0, f)
    hit = lf >= 100
    bp = P(torso=55, head=30, lsh=-20, lel=-40, rsh=30, rel=-60, lhip=-6, rhip=6, eye='happy' if not hit else 'ko', mouth='grin' if not hit else 'wavy')
    h = draw(ctx, 640, STAND - 186 * KB, KB, 1, BOY, bp)
    if lf >= 50:
        u = pop(lf, 50, 64)
        draw(ctx, lerp(-100, 330, ease(u)), STAND - 186 * KM, KM, 1, MOM, P(eye='glare', mouth='scream' if lf < 96 else 'smug', lsh=40, lel=-120, rsh=-150 if lf < 86 else 80, rel=-30 if lf < 86 else 0))
    if 86 <= lf < 100:
        u = pop(lf, 86, 100)
        slipper(ctx, lerp(420, h['head'][0] - 40, u), lerp(860, h['head'][1], u) - math.sin(u * math.pi) * 150, u * 14, 1.5)
    if hit:
        slipper(ctx, h['head'][0] - 60, h['head'][1] + 200 + min(300, (lf - 100) * 20), 2.5, 1.5)
        stars_ko(ctx, h['head'][0], h['head'][1] - 150, (lf - 100) / 30, r=100)
    ctx.restore()
    if lf < 50:
        label(ctx, "THE ONLY COOL PLACE", 540, 1560, 84, hx('8fe9ff'), -0.03, pop(lf, 4, 10))
    elif lf < 86:
        label(ctx, "CLOSE THE FRIDGE!!", 540, 1560, 96, hx('ff3b5c'), 0.03, pop(lf, 56, 61))
    elif lf < 100:
        hlines(ctx, lf, 0.4, col=INK, y0=700, y1=1100)
    else:
        label(ctx, "THWACK!", 540, 1540, 150, hx('ffe14d'), -0.06, pop(lf, 100, 104))


SHOTS = [(0, s1), (100, s2), (250, s3), (360, s4), (560, s5), (760, s6), (900, s7)]


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.28)
    ctx.set_source(g); ctx.paint()
    for c in (34, 100, 132, 176, 250, 334, 360, 450, 490, 560, 610, 660, 760, 900):
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.55 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/a{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/ac_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
