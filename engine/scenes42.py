"""'Who Touched the Thermostat?' - original, general-audience comedy short, ~22s.
Hook: ECU of Dad, red-faced, steam from his ears: "WHO TOUCHED THE THERMOSTAT?!"
 -> rewind: the kid in a hoodie sneaks to the hallway thermostat: *click click* 68 -> 72.
Beat 1 (DAD SENSE): Dad on the sofa behind his newspaper - radar rings - eyes snap open "+4 DEGREES?!",
 ZOOM - he's at the thermostat in one frame: "NOT. ON. MY. WATCH." 72 -> 68.
Beat 2 (THE LOCKDOWN): a cage slams over the thermostat, padlock CLUNK, sign "68. FOREVER."; Mom + kid wrapped in
 blankets, snow falling INDOORS, teeth chattering; Dad strolls in with an ice cream cone: "It's NOT cold."
Beat 3 (WEEK 2): the living room is Antarctica - Mom + kid frozen in ice blocks, snowman on the sofa, a penguin waddles
 through; split screen kid frozen / Dad fanning himself "Ahh... PERFECT."
Twist (3 AM): Dad tiptoes with a flashlight, unlocks the cage, "just ONE degree..." cranks it 68 -> 75,
 LIGHTS ON: Mom + kid in blankets, arms crossed: "WHO. TOUCHED. THE THERMOSTAT?" -> loops to Dad's face."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, living, sofa_back, sofa_front, SEAT, _SCR
from scenes8 import sit
from scenes14 import sweat
from scenes33 import vein, steam
from scenes13 import flashlight
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
ICE = hx('1fb5ff')
YEL = hx('fff27a')
LY = 1450

CAPS = {
    'p1': [[("DAD VS", OUT)], [("THE THERMOSTAT", RED)]],
    'p2': [[("+4 DEGREES?", OUT)], [("HE FELT IT FROM THE SOFA", ORANGE)]],
    'p3': [[("THE LOCKDOWN:", OUT)], [("68. FOREVER.", BLUE)]],
    'p4': [[("WEEK 2:", OUT)], [("THE HOUSE IS NOW ANTARCTICA", ICE)]],
    'p5': [[("3 AM:", OUT)], [("PLOT TWIST", PINK)]],
}
scenes13.CAPS = CAPS
card = _card13


def hip(k):
    return FLOOR - 100 * k


# ------------------------------------------------------------------ props
def thermostat(ctx, x, y, s, temp, cage=0.0, lock_open=0.0, sign=False, glow=False, dark_=False):
    """centre (x, y), scale s. cage: 0 none .. 1 fully dropped in place"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rect_r(ctx, -100 + 10, -130 + 14, 200, 260, 34); setc(ctx, (0, 0, 0, 0.25)); ctx.fill()
    rect_r(ctx, -100, -130, 200, 260, 34); fl(ctx, hx('f4f4ee') if not dark_ else hx('8a8aa0'), 8)
    rect_r(ctx, -72, -100, 144, 110, 16); fl(ctx, hx('1a3a2a'), 6)
    col = hx('7dff9a') if temp <= 70 else (hx('ffb03a') if temp <= 73 else hx('ff5a3a'))
    if glow:
        ellipse(ctx, 0, -45, 120, 80); setc(ctx, col + (0.25,)); ctx.fill()
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(78)
    st = f"{temp}°"; w = ctx.text_extents(st).x_advance
    ctx.move_to(-w / 2 + 6, -16); ctx.text_path(st); setc(ctx, col); ctx.fill()
    # up / down buttons
    poly(ctx, [(-50, 70), (-20, 70), (-35, 44)]); fl(ctx, hx('ff5a3a'), 4)
    poly(ctx, [(20, 46), (50, 46), (35, 72)]); fl(ctx, hx('3ab0ff'), 4)
    ctx.restore()
    if cage > 0:
        dy = -(1 - eout(cage)) * 900
        ctx.save(); ctx.translate(x, y + dy * s); ctx.scale(s, s)
        rect_r(ctx, -150, -175, 300, 360, 20); setc(ctx, OUT); ctx.set_line_width(22); ctx.stroke()
        rect_r(ctx, -150, -175, 300, 360, 20); setc(ctx, hx('9aa4b8')); ctx.set_line_width(11); ctx.stroke()
        for k in range(1, 7):
            bx = -150 + k * 300 / 7
            ctx.move_to(bx, -175); ctx.line_to(bx, 185)
            setc(ctx, OUT); ctx.set_line_width(16); ctx.stroke_preserve(); setc(ctx, hx('b8c0d0')); ctx.set_line_width(7); ctx.stroke()
        # padlock
        lx, ly = 0, 200
        ctx.new_path(); ctx.arc(lx, ly - 30 - 40 * lock_open, 36, math.pi, 0)
        ctx.line_to(lx + 36, ly - 30 * (1 - lock_open)); ctx.move_to(lx - 36, ly - 30 - 40 * lock_open); ctx.line_to(lx - 36, ly)
        setc(ctx, OUT); ctx.set_line_width(20); ctx.stroke_preserve(); setc(ctx, hx('c0c8d8')); ctx.set_line_width(10); ctx.stroke()
        rect_r(ctx, lx - 58, ly - 20, 116, 100, 16); fl(ctx, hx('ffc21f'), 7)
        ellipse(ctx, lx, ly + 22, 11, 11); setc(ctx, OUT); ctx.fill(); ctx.rectangle(lx - 4, ly + 22, 8, 26); ctx.fill()
        if sign:
            ctx.save(); ctx.translate(0, -255); ctx.rotate(-0.06)
            rect_r(ctx, -200, -50, 400, 100, 8); fl(ctx, (1, 1, 1), 6)
            text(ctx, "68. FOREVER.", 0, 0, 52, RED, ow=0, shadow=False)
            for tx_ in (-180, 180):
                ctx.save(); ctx.translate(tx_, -46); ctx.rotate(0.6 if tx_ < 0 else -0.6)
                ctx.rectangle(-30, -10, 60, 20); setc(ctx, (1, 0.95, 0.6, 0.8)); ctx.fill(); ctx.restore()
            ctx.restore()
        ctx.restore()


def hallway(ctx, lights=True):
    wall = hx('ffd08a') if lights else hx('1b2440')
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, wall); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 120, -3000, 46, 6000); setc(ctx, dark(wall, 0.95)); ctx.fill()
    # picture frame (simple landscape)
    rect_r(ctx, 90, 700, 260, 200, 8); fl(ctx, hx('9a5a2a') if lights else hx('3a2a40'), 8)
    ctx.rectangle(115, 725, 210, 150); setc(ctx, hx('9fe0ff') if lights else hx('2a3460')); ctx.fill()
    ellipse(ctx, 280, 765, 24, 24); setc(ctx, hx('ffd23f') if lights else hx('5a5a3a')); ctx.fill()
    poly(ctx, [(115, 875), (190, 790), (260, 875)]); setc(ctx, hx('3ccf4e') if lights else hx('1f3a3a')); ctx.fill()
    # skirting + floor
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('b97a48') if lights else hx('22183a')); ctx.fill()
    ctx.rectangle(-3000, FLOOR - 40, 7000, 40); setc(ctx, (1, 1, 1) if lights else hx('3a3a5a')); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()
    ctx.move_to(-3000, FLOOR - 40); ctx.line_to(4000, FLOOR - 40); ink(ctx, 6); ctx.stroke()


def newspaper(ctx, x, y, w=300, h=220, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    rect_r(ctx, -w / 2, -h / 2, w, h, 6); fl(ctx, hx('f2f0e6'), 7)
    ctx.move_to(0, -h / 2); ctx.line_to(0, h / 2); ink(ctx, 4); ctx.stroke()
    text(ctx, "NEWS", -w / 4, -h / 2 + 34, 34, OUT, ow=0, shadow=False)
    for k in range(5):
        ctx.rectangle(-w / 2 + 18, -h / 2 + 64 + k * 26, w / 2 - 36, 9); setc(ctx, (0.5, 0.5, 0.5)); ctx.fill()
        ctx.rectangle(18, -h / 2 + 30 + k * 32, w / 2 - 36, 9); ctx.fill()
    ctx.restore()


def radar(ctx, x, y, lf, col=hx('ff3b5c')):
    for k in range(4):
        u = ((lf * 0.06) + k * 0.25) % 1
        ctx.new_path(); ctx.arc(x, y, 60 + 380 * u, 0, 2 * math.pi)
        setc(ctx, col + (0.9 * (1 - u),)); ctx.set_line_width(14 * (1 - u) + 3); ctx.stroke()


def blanket_wrap(ctx, b, w, bottom, col, stripe=(1, 1, 1)):
    hx_, hy_ = b['head']; R = b['R']
    top = hy_ + R * 0.95
    ctx.save()
    ctx.new_path(); ctx.move_to(hx_ - w * 0.42, top); ctx.curve_to(hx_ - w * 0.15, top - R * 0.5, hx_ + w * 0.15, top - R * 0.5, hx_ + w * 0.42, top)
    ctx.curve_to(hx_ + w * 0.62, top + 80, hx_ + w * 0.6, bottom - 60, hx_ + w * 0.52, bottom)
    ctx.line_to(hx_ - w * 0.52, bottom); ctx.curve_to(hx_ - w * 0.6, bottom - 60, hx_ - w * 0.62, top + 80, hx_ - w * 0.42, top)
    ctx.close_path(); path = ctx.copy_path()
    setc(ctx, col); ctx.fill_preserve(); ctx.clip()
    for k in range(-3, 4):
        ctx.rectangle(hx_ + k * w * 0.2 - 12, top - 200, 24, bottom - top + 300); setc(ctx, stripe + (0.6,)); ctx.fill()
    ctx.restore()
    ctx.new_path(); ctx.append_path(path); ink(ctx, 7); ctx.stroke()


def breath(ctx, x, y, lf, side=1, s=1.0):
    ph = (lf % 30) / 30
    if ph < 0.6:
        u = ph / 0.6
        ellipse(ctx, x + side * 70 * u * s, y - 10 * u * s, (20 + 40 * u) * s, (16 + 28 * u) * s)
        setc(ctx, (1, 1, 1, 0.85 * (1 - u))); ctx.fill()


def snow(ctx, lf, n=26, seed=3, y0=-200, y1=2000, a=1.0):
    rnd = random.Random(seed)
    for k in range(n):
        x = rnd.uniform(-50, 1130); sp = rnd.uniform(5, 11); r = rnd.uniform(9, 18)
        y = y0 + ((rnd.uniform(0, 1) * (y1 - y0) + lf * sp) % (y1 - y0))
        x += 30 * math.sin(lf * 0.07 + k)
        ctx.save(); ctx.translate(x, y); ctx.rotate(lf * 0.05 + k)
        for j in range(3):
            ctx.move_to(-r, 0); ctx.line_to(r, 0); ctx.rotate(math.pi / 3)
        setc(ctx, (1, 1, 1, a)); ctx.set_line_width(5); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        ctx.restore()


def icicles(ctx, x0, x1, y, n, L=90, seed=5):
    rnd = random.Random(seed)
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n; l = L * rnd.uniform(0.5, 1.2)
        poly(ctx, [(x - 18, y), (x + 18, y), (x + 2, y + l)]); fl(ctx, hx('c8f2ff'), 4)
    ctx.rectangle(x0 - 20, y - 22, x1 - x0 + 40, 30); fl(ctx, (1, 1, 1), 5)


def ice_cream(ctx, x, y, s=1.0, a=0.0, bites=0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-34, -10), (34, -10), (0, 100)]); fl(ctx, hx('e9a85a'), 6)
    for k in range(3):
        ctx.move_to(-28 + k * 20, -8); ctx.line_to(4 + k * 8, 70)
    ink(ctx, 3); ctx.stroke()
    ellipse(ctx, 0, -40, 44, 40); fl(ctx, hx('ffb3d9'), 6)
    ellipse(ctx, 0, -92, 36, 32); fl(ctx, hx('fff3c8'), 6)
    ctx.restore()


def ice_block(ctx, x, y, w, h, lf=0):
    rect_r(ctx, x - w / 2, y - h / 2, w, h, 26); setc(ctx, (0.6, 0.9, 1.0, 0.55)); ctx.fill_preserve()
    setc(ctx, OUT); ctx.set_line_width(8); ctx.stroke()
    for k, (dx, dy, L) in enumerate(((-0.35, -0.38, 0.22), (-0.3, -0.25, 0.12), (0.28, 0.3, 0.16))):
        ctx.move_to(x + dx * w, y + dy * h); ctx.line_to(x + (dx + L) * w, y + (dy - L * 0.6) * h)
        setc(ctx, (1, 1, 1, 0.85)); ctx.set_line_width(12); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def snowman(ctx, x, yb, s=1.0):
    ctx.save(); ctx.translate(x, yb); ctx.scale(s, s)
    for r, cy in ((120, -120), (90, -310), (66, -450)):
        ellipse(ctx, 0, cy, r, r * 0.95); fl(ctx, (1, 1, 1), 8)
    for ex in (-22, 22):
        ellipse(ctx, ex, -465, 9, 9); setc(ctx, OUT); ctx.fill()
    poly(ctx, [(0, -445), (0, -425), (70, -440)]); fl(ctx, hx('ff8a1f'), 4)
    for k in range(3):
        ellipse(ctx, 0, -340 + k * 40, 9, 9); setc(ctx, OUT); ctx.fill()
    ctx.move_to(-56, -390); ctx.curve_to(-20, -370, 20, -370, 56, -390); setc(ctx, OUT); ctx.set_line_width(30); ctx.stroke_preserve()
    setc(ctx, RED); ctx.set_line_width(20); ctx.stroke()
    ctx.restore()


def penguin(ctx, x, yb, s, lf):
    ctx.save(); ctx.translate(x, yb); ctx.scale(s, s); ctx.rotate(0.12 * math.sin(lf * 0.6))
    for fx in (-30, 30):
        ellipse(ctx, fx, -6, 34, 14); fl(ctx, hx('ff9a1f'), 5)
    ellipse(ctx, 0, -130, 95, 130); fl(ctx, hx('22263a'), 8)
    ellipse(ctx, 12, -110, 62, 100); fl(ctx, (1, 1, 1), 0)
    ellipse(ctx, -78, -120, 22, 66, 0.3 + 0.3 * math.sin(lf * 0.6)); fl(ctx, hx('22263a'), 6)
    for ex in (-10, 40):
        ellipse(ctx, ex, -205, 15, 18); fl(ctx, (1, 1, 1), 4)
        ellipse(ctx, ex + 5, -203, 7, 9); setc(ctx, OUT); ctx.fill()
    poly(ctx, [(5, -185), (55, -185), (80, -172), (30, -165)]); fl(ctx, hx('ff9a1f'), 5)
    ctx.restore()


def key(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 26, 0, 2 * math.pi); fl(ctx, hx('ffc21f'), 6)
    ellipse(ctx, 0, 0, 9, 9); setc(ctx, OUT); ctx.fill()
    ctx.rectangle(22, -8, 80, 16); fl(ctx, hx('ffc21f'), 5)
    ctx.rectangle(80, 4, 10, 18); fl(ctx, hx('ffc21f'), 4)
    ctx.restore()


def hand(ctx, x, y, s, skin, ang=0.0, point=True):
    """big cartoon hand (index finger out) reaching from below/left"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s)
    ctx.rectangle(-60, 60, 120, 400); fl(ctx, skin, 8)
    ellipse(ctx, 0, 40, 85, 80); fl(ctx, skin, 8)
    if point:
        rect_r(ctx, -24, -110, 48, 140, 24); fl(ctx, skin, 8)
    ctx.restore()


def label2(ctx, a, b, col, t, size=104, col2=None):
    label(ctx, a, 540, LY - 60, size, col, -0.03, t)
    label(ctx, b, 540, LY + 50, size, col2 or col, 0.02, t)


def stool(ctx, x, top):
    rect_r(ctx, x - 110, top, 220, 40, 10); fl(ctx, hx('e0263a'), 7)
    for dx in (-80, 60):
        ctx.rectangle(x + dx, top + 40, 22, FLOOR - top - 40); fl(ctx, hx('8a4a2a'), 6)


def flash(ctx, u):
    if 0 <= u < 1:
        ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.95 * (1 - u) ** 1.5)); ctx.fill()


def speedlines(ctx, lf, n=14, y0=900, y1=1500, a=0.75):
    for k in range(n):
        rnd = random.Random(lf // 2 * 13 + k)
        y = rnd.uniform(y0, y1); x = rnd.uniform(0, 900); L = rnd.uniform(160, 360)
        ctx.move_to(x, y); ctx.line_to(x + L, y)
    setc(ctx, (1, 1, 1, a)); ctx.set_line_width(9); ctx.stroke()


# ------------------------------------------------------------------ opening
def opening_face(ctx, f, lf, lab=True):
    sh = shake_at(lf, [0], 12, 22) + 4
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 40)), 0, sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff4a3a')); ctx.fill()
    rays(ctx, 540, 980, 240, 1700, lf * 0.04, col=(1, 0.85, 0.3), a=0.45, n=18)
    cx, cy, Rt = 540 + 6 * math.sin(lf * 2.3), 1000, 300
    face(ctx, DAD, P(eye='shock', mouth='scream', head=0), cx, cy, Rt, 0.02 * math.sin(lf * 1.7))
    steam(ctx, cx - 300, cy - 20, lf * 2, 1.3, -1)
    steam(ctx, cx + 310, cy - 20, lf * 2 + 9, 1.3, 1)
    vein(ctx, cx + 170, cy - 210, 1.3 + 0.15 * math.sin(lf * 0.9))
    sweat(ctx, cx - 230, cy - 260, lf * 2, 1.2)
    ctx.restore()
    if lab:
        label2(ctx, "\"WHO TOUCHED THE", "THERMOSTAT?!\"", YEL, pop(lf, 0, 4) if lf > 0 else 1, 110)


# ------------------------------------------------------------------ shots
def temp_sneak(lf):
    return min(72, 68 + max(0, (lf - 14)) // 8)


STOOL_TOP = FLOOR - 170
KID_X = 420


def sneak_shot(ctx, f, lf, temp, kid_eye='smug', kid_mouth='grin', z=1.18, shake=0, dad=None, kid_pose=None):
    ctx.save(); cam(ctx, 560, 1120, z, 0, shake, f)
    hallway(ctx)
    k = 1.0
    kp = kid_pose or P(eye=kid_eye, mouth=kid_mouth, rsh=150, rel=10, lsh=-30, lel=-40, head=-6, lhip=-4, rhip=4)
    hy = STOOL_TOP - 100 * k
    ref = draw_hip(_SCR, KID_X, hy, k, 1, BOY, P(rsh=150, rel=10))
    tx, ty = ref['front'][0] + 95, ref['front'][1] - 10
    thermostat(ctx, tx, ty, 0.8, temp, glow=True)
    stool(ctx, KID_X, STOOL_TOP)
    draw_hip(ctx, KID_X, hy, k, 1, BOY, kp)
    if dad:
        dad(ctx, tx, ty)
    ctx.restore()


def s1(ctx, f):
    if f < 50:
        opening_face(ctx, f, f)
    else:
        lf = f - 50
        temp = temp_sneak(lf)
        sneak_shot(ctx, f, lf, temp, shake=shake_at(lf, [0], 6, 8), z=1.12 + 0.08 * eout(pop(lf, 0, 60)))
        if lf < 12:
            label(ctx, "*sneak sneak*", 540, LY + 40, 110, (1, 1, 1), 0.03, pop(lf, 0, 4))
        else:
            label(ctx, "*click... click... click...*", 540, LY + 40, 92, YEL, -0.03, pop(lf, 12, 16))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 40:
        sense = lf >= 10
        z = 1.05 + (0.35 * eout(pop(lf, 10, 30)) if sense else 0)
        ctx.save(); cam(ctx, 690, 1040 - (60 * eout(pop(lf, 10, 30)) if sense else 0), z, 0, shake_at(lf, [10], 10, 16), f)
        living(ctx)
        sofa_back(ctx)
        b = draw_hip(ctx, 680, SEAT, 1.15, -1, DAD, sit(eye='shock' if sense else 'closed', mouth='open' if sense else 'smile', head=-2,
                                                          rsh=70, rel=-90, lsh=60, lel=-90))
        sofa_front(ctx)
        hx_, hy_ = b['head']
        if sense:
            radar(ctx, hx_, hy_ - 30, lf)
            newspaper(ctx, 560, hy_ + 180 + 80 * eout(pop(lf, 10, 16)), a=0.5 * eout(pop(lf, 10, 16)))
        else:
            newspaper(ctx, 560, hy_ + 60)
        ctx.restore()
        if not sense:
            label(ctx, "*peaceful sofa time*", 540, LY + 40, 96, (1, 1, 1), 0.03, pop(lf, 0, 4))
        else:
            label(ctx, "\"...+4 DEGREES?!\"", 540, LY + 40, 120, YEL, -0.04, pop(lf, 10, 14))
    else:
        il = lf - 40
        temp = 72 if il < 34 else 68

        def dad_fn(c, tx, ty):
            if il < 6:
                speedlines(c, il, y0=700, y1=1500)
                return
            pose = P(eye='glare', mouth='flat', rsh=150 if il >= 30 else 60, rel=10 if il >= 30 else -60, lsh=-40, lel=-80, head=6)
            bx = 860 + 40 * (1 - eout(pop(il, 6, 12)))
            draw_hip(c, bx, hip(1.25) - 10, 1.25, -1, DAD, pose)
            if il < 12:
                for j in range(4):
                    puff(c, 900 + 60 * j - 80, 1300 - 60 * j, (il - 6) / 6, 1.4)
        kid_p = P(eye='shock', mouth='scream', rsh=150, rel=10, lsh=-160, lel=-20, head=-10, rot=-4) if il >= 6 else None
        sneak_shot(ctx, f, il, temp, kid_eye='shock', kid_mouth='open', z=1.0, shake=shake_at(il, [6, 34], 10, 18), dad=dad_fn,
                   kid_pose=kid_p)
        if il < 6:
            label(ctx, "*ZOOOM!*", 540, LY + 40, 140, YEL, 0.03, pop(il, 0, 3))
        elif il < 34:
            label(ctx, "\"NOT. ON. MY. WATCH.\"", 540, LY + 40, 110, (1, 1, 1), -0.03, pop(il, 8, 12))
        else:
            label(ctx, "*BEEP* 68.", 540, LY + 40, 130, hx('7dff9a'), 0.03, pop(il, 34, 38))
    card(ctx, 'p2', f, 112, 228)


def s3(ctx, f):
    lf = f - 230
    if lf < 60:
        # ECU: the cage slams over the thermostat
        cg = pop(lf, 4, 14)
        lock = lf >= 22
        ctx.save(); cam(ctx, 540, 940, 1.0 + 0.04 * eout(pop(lf, 0, 60)), 0, shake_at(lf, [14, 24], 10, 22), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd08a')); ctx.fill()
        for i in range(-10, 20):
            ctx.rectangle(i * 120, -500, 46, 3000); setc(ctx, dark(hx('ffd08a'), 0.95)); ctx.fill()
        thermostat(ctx, 540, 1000, 1.35, 68, cage=cg, lock_open=0 if lock else 1, sign=lf >= 34, glow=True)
        if 16 <= lf < 40:   # Dad's hand turning the key
            hand(ctx, 690 - 30 * eout(pop(lf, 16, 22)), 1400, 1.0, DAD['skin'], -0.5, point=False)
            key(ctx, 560, 1300, 1.2 if lock else 0.3, 1.2)
        ctx.restore()
        if lf < 14:
            label(ctx, "*WHOOSH...*", 540, LY + 40, 110, (1, 1, 1), 0.03, pop(lf, 2, 6))
        elif lf < 34:
            label(ctx, "*CLANG! CLICK!*", 540, LY + 40, 120, ORANGE, -0.04, pop(lf, 14, 18))
        else:
            label(ctx, "\"Nobody. Touches. It.\"", 540, LY + 40, 104, YEL, -0.03, pop(lf, 34, 38))
    else:
        il = lf - 60
        ctx.save(); cam(ctx, 560, 1150, 1.08 + 0.05 * eout(pop(il, 0, 80)), 0, 3 + shake_at(il, [0], 6, 8), f)
        living(ctx)
        icicles(ctx, 780, 1080, 620, 6, 110)
        sofa_back(ctx)
        ch = 4 * math.sin(il * 3.1)
        bm = draw_hip(ctx, 290 + ch, SEAT, 1.12, 1, MOM, sit(eye='glare', mouth='wavy', head=4))
        bk = draw_hip(ctx, 520 - ch, SEAT + 10, 0.95, 1, BOY, sit(eye='shock', mouth='wavy', head=-4))
        blanket_wrap(ctx, bm, 300, SEAT + 120, hx('ff8a3d'))
        blanket_wrap(ctx, bk, 270, SEAT + 110, hx('3ccf9e'))
        sofa_front(ctx)
        for b, sd, sk in ((bm, 1, 0), (bk, 1, 11)):
            hx_, hy_ = b['head']
            breath(ctx, hx_ + 90, hy_ + 40, il + sk, sd, 1.0)
        # Dad strolls in with ice cream
        if il >= 30:
            dx = 1000 - 200 * eout(pop(il, 30, 46))
            bd = draw_hip(ctx, dx, hip(1.2) - 10, 1.2, -1, DAD, P(eye='happy', mouth='grin', rsh=70, rel=-110, lsh=-20, lel=-20, head=4,
                                                                    lhip=6 * math.sin(il * 0.5), rhip=-6 * math.sin(il * 0.5)))
            ice_cream(ctx, bd['front'][0] - 10, bd['front'][1] - 50, 1.0, -0.1)
        snow(ctx, il, 26, 3, a=0.95)
        ctx.restore()
        if il < 30:
            label(ctx, "*chatter chatter chatter*", 540, LY + 40, 96, (1, 1, 1), 0.03 * math.sin(il), pop(il, 0, 4))
        else:
            label(ctx, "\"It's NOT cold.\"", 540, LY + 40, 120, YEL, -0.03, pop(il, 34, 38))
    card(ctx, 'p3', f, 232, 368)


def frozen_room(ctx, f, il):
    ctx.save(); cam(ctx, 520, 1080, 0.9 + 0.06 * eout(pop(il, 0, 70)), 0, shake_at(il, [0], 6, 10), f)
    living(ctx)
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, (0.55, 0.85, 1.0, 0.35)); ctx.fill()
    icicles(ctx, 780, 1080, 620, 7, 170, 9)
    icicles(ctx, -200, 760, 500, 14, 130, 4)
    sofa_back(ctx)
    bm = draw_hip(ctx, 290, SEAT, 1.12, 1, MOM, sit(eye='shock', mouth='wavy', head=4))
    bk = draw_hip(ctx, 490, SEAT + 10, 0.95, 1, BOY, sit(eye='shock', mouth='wavy', head=-4))
    blanket_wrap(ctx, bm, 300, SEAT + 120, hx('ff8a3d'))
    blanket_wrap(ctx, bk, 270, SEAT + 110, hx('3ccf9e'))
    ice_block(ctx, 290, 1090, 300, 420)
    ice_block(ctx, 490, 1130, 250, 360)
    snowman(ctx, 700, SEAT + 30, 0.85)
    sofa_front(ctx)
    # snow drifts on the floor
    for x, r in ((-60, 220), (300, 160), (620, 200), (1000, 240)):
        ellipse(ctx, x, FLOOR + 30, r, 70); fl(ctx, (1, 1, 1), 6)
    px = 1150 - 1100 * pop(il, 6, 70)
    penguin(ctx, px, FLOOR + 40, 0.9, il)
    snow(ctx, il, 34, 8, a=1.0)
    ctx.restore()


def s4(ctx, f):
    lf = f - 370
    if lf < 70:
        frozen_room(ctx, f, lf)
        if lf < 30:
            label(ctx, "*WHOOOOSH*", 540, LY + 40, 120, (1, 1, 1), 0.03, pop(lf, 0, 4))
        else:
            label(ctx, "*a penguin moved in*", 540, LY + 40, 100, YEL, -0.03, pop(lf, 30, 34))
    else:
        il = lf - 70
        # split screen: kid frozen (top) / Dad comfy (bottom)
        ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
        cam(ctx, 540, 640, 1.0 + 0.05 * eout(pop(il, 0, 60)), 0, 3, f, sy=600)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('9fe4ff')); ctx.fill()
        rays(ctx, 540, 640, 200, 1200, il * 0.02, col=(1, 1, 1), a=0.35, n=16)
        fx, fy = 540 + 5 * math.sin(il * 3.3), 760
        face(ctx, BOY, P(eye='shock', mouth='wavy', head=0), fx, fy, 200)
        ellipse(ctx, fx, fy, 270, 270); setc(ctx, (0.45, 0.75, 1.0, 0.35)); ctx.fill()
        icicles(ctx, fx - 60, fx + 120, fy + 110, 3, 80, 2)   # under the nose
        ice_block(ctx, fx, fy - 30, 520, 470)
        snow(ctx, il, 14, 5, y0=200, y1=960)
        ctx.restore()
        ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
        cam(ctx, 540, 1250, 1.0 + 0.05 * eout(pop(il, 0, 60)), 0, 0, f, sy=1250)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb85a')); ctx.fill()
        rays(ctx, 540, 1250, 200, 1200, -il * 0.02, col=(1, 1, 1), a=0.3, n=16)
        face(ctx, DAD, P(eye='happy', mouth='grin', head=0), 540, 1230, 200, 0.05 * math.sin(il * 0.3))
        # fanning hand + newspaper fan
        newspaper(ctx, 830, 1150, 190, 140, 0.4 * math.sin(il * 0.8))
        ctx.restore()
        ctx.rectangle(0, 952, W, 16); setc(ctx, OUT); ctx.fill()
        label(ctx, "*shiver shiver*", 540, 1010, 70, (1, 1, 1), -0.02, pop(il, 2, 6))
        if il >= 18:
            label(ctx, "\"Ahh... PERFECT.\"", 540, LY + 40, 116, YEL, 0.03, pop(il, 18, 22))
    card(ctx, 'p4', f, 372, 498)


def s5(ctx, f):
    lf = f - 500
    if lf < 45:
        # dark hallway: Dad tiptoes with a flashlight
        ctx.save(); cam(ctx, 560, 1080, 1.0, 0, 0, f)
        hallway(ctx, lights=False)
        thermostat(ctx, 760, 980, 0.8, 68, cage=1.0, sign=True, dark_=True)
        u = pop(lf, 0, 45)
        x = 250 + 300 * u
        ph = lf * 0.5
        bd = draw_hip(ctx, x, hip(1.2) - 30 - 20 * abs(math.sin(ph)), 1.2, 1, DAD,
                      P(eye='normal', mouth='flat', torso=18, head=-10, lsh=-30, lel=-90, rsh=80, rel=-30,
                        lhip=30 * math.sin(ph), lkn=-60 * max(0, math.sin(ph)), rhip=-30 * math.sin(ph), rkn=-60 * max(0, -math.sin(ph))))
        fx, fy = bd['front']
        ang = -0.75 + 0.2 * math.sin(lf * 0.15)
        ctx.restore()
        ctx.rectangle(0, 0, W, H); setc(ctx, (0.02, 0.02, 0.08, 0.45)); ctx.fill()
        ctx.save(); cam(ctx, 560, 1080, 1.0, 0, 0, f)
        flashlight(ctx, fx + 20, fy, ang, True, 900, 0.3)
        ctx.restore()
        label(ctx, "*tiptoe... tiptoe...*", 540, LY + 40, 100, (1, 1, 1), 0.03, pop(lf, 0, 4))
    elif lf < 85:
        il = lf - 45
        opened = il >= 10
        temp = 68 if il < 16 else min(75, 68 + (il - 16) // 2)
        ctx.save(); cam(ctx, 540, 940, 1.0 + 0.06 * eout(pop(il, 0, 40)), 0, shake_at(il, [10], 8, 12), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('1b2440')); ctx.fill()
        ellipse(ctx, 540, 1000, 560, 640); setc(ctx, (1, 0.97, 0.7, 0.35)); ctx.fill()
        thermostat(ctx, 540, 1000, 1.35, temp, cage=1.0, lock_open=1.0 if opened else 0.0, sign=True, glow=True)
        if il < 12:
            hand(ctx, 690, 1400, 1.0, DAD['skin'], -0.5, point=False)
            key(ctx, 560, 1300, 1.2 if not opened else 0.3, 1.2)
        else:
            hand(ctx, 600, 1150 + 6 * math.sin(il * 2), 0.9, DAD['skin'], -0.35)
        ctx.restore()
        if il < 16:
            label(ctx, "*click*", 540, LY + 40, 120, (1, 1, 1), 0.03, pop(il, 0, 4))
        else:
            label(ctx, "\"Just ONE degree...\"", 540, LY + 40, 104, YEL, -0.03, pop(il, 16, 20))
    elif lf < 130:
        il = lf - 85
        ctx.save(); cam(ctx, 560, 1080, 1.0 + 0.05 * eout(pop(il, 0, 40)), 0, shake_at(il, [0, 16], 10, 20), f)
        hallway(ctx, lights=True)
        thermostat(ctx, 740, 980, 0.8, 75, cage=1.0, lock_open=1.0, sign=True, glow=True)
        bd = draw_hip(ctx, 820, hip(1.2) - 10, 1.2, -1, DAD, P(eye='shock', mouth='scream', rsh=150, rel=10, lsh=-150, lel=-20, head=-8))
        bm = draw_hip(ctx, 210, hip(1.12) - 10, 1.12, 1, MOM, P(eye='glare', mouth='flat', rsh=60, rel=-130, lsh=50, lel=-130, head=6))
        bk = draw_hip(ctx, 430, hip(0.95) - 10, 0.95, 1, BOY, P(eye='glare', mouth='flat', rsh=60, rel=-130, lsh=50, lel=-130, head=6))
        blanket_wrap(ctx, bm, 260, FLOOR - 120, hx('ff8a3d'))
        blanket_wrap(ctx, bk, 230, FLOOR - 120, hx('3ccf9e'))
        sweat(ctx, bd['head'][0] - 140, bd['head'][1] - 120, il * 3, 1.0)
        ctx.restore()
        flash(ctx, il / 6)
        if il < 14:
            label(ctx, "*CLICK!* LIGHTS ON", 540, LY + 40, 110, (1, 1, 1), 0.03, pop(il, 0, 3))
        else:
            label2(ctx, "\"WHO. TOUCHED.", "THE. THERMOSTAT?\"", YEL, pop(il, 16, 20), 104)
    else:
        il = lf - 130
        opening_face(ctx, f, il)
    if lf < 128:
        card(ctx, 'p5', f, 502, 626)
    else:
        card(ctx, 'p1', f, 630)


SHOTS = [(0, s1), (110, s2), (230, s3), (370, s4), (500, s5)]
CUTS = (50, 110, 150, 230, 290, 370, 440, 500, 545, 585, 630)


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
                              "-i", "out/thermostat_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
