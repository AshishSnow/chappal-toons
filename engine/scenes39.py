"""'Did You Brush Your Teeth?' - original, general-audience comedy short, ~22s.
Hook: ECU of the kid, huge shiny fake grin, dry toothbrush held up: "YES, I BRUSHED!"
 -> wide bathroom: Mom in the doorway, arms crossed: "Did you REALLY?" - "...yes?"
Beat 1: '10 SECONDS AGO': insert at the tap - he just waves the brush under the water for one second. *splish*. Smug wink.
Beat 2: Mom's lie detector: "Say 'HAAA'." - a green stink cloud rolls out, Mom's hair blows back, the flower wilts,
 the mirror cracks. Mom ECU, green: "BRUSH. NOW."
Beat 3: super-speed scrubbing, foam fills the whole screen, POP: blinding sparkle smile *DING*.
Twist: midnight, Dad sneaks into the dark bathroom and does the SAME wet-brush trick - lights snap on: Mom and the kid
 in the doorway: "Say 'HAAA', DAD." Dad sweats.
Loop: kid ECU, same fake grin -> loops to the opening."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos, lids
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
STINK = hx('9be04a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
GREY = hx('9aa6c0')
LY = 1450

CAPS = {
    'p1': [[("WHEN MOM ASKS:", OUT)], [("\"DID YOU BRUSH?\"", BLUE)]],
    'p2': [[("10 SECONDS AGO:", OUT)], [("THE WET-BRUSH TRICK", ORANGE)]],
    'p3': [[("MOM'S LIE DETECTOR:", OUT)], [("THE SMELL TEST", GREEN)]],
    'p4': [[("2 MINUTES OF", OUT)], [("PURE DRAMA", PURPLE)]],
    'p5': [[("PLOT TWIST:", OUT)], [("GUESS WHO TAUGHT HIM", PINK)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props / set
def tiles(ctx, col):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, col); ctx.fill()
    setc(ctx, dark(col, 0.86)); ctx.set_line_width(6)
    for i in range(-30, 40):
        ctx.move_to(i * 120, -3000); ctx.line_to(i * 120, 4000)
        ctx.move_to(-3000, i * 120); ctx.line_to(4000, i * 120)
    ctx.stroke()


def toothbrush(ctx, x, y, a, s=1.0, paste=True, wet=0.0, col=hx('ff5fa8')):
    """toothbrush, grip centre at (x, y), head pointing +x"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -150, -16, 330, 32, 16); fl(ctx, col, 6)
    rect_r(ctx, 170, -22, 90, 30, 10); fl(ctx, (1, 1, 1), 5)
    for k in range(6):
        ctx.rectangle(176 + k * 14, -58, 8, 38); setc(ctx, hx('7fd4ff')); ctx.fill()
    ctx.rectangle(172, -60, 88, 40); ink(ctx, 4); ctx.stroke()
    if paste:
        ctx.new_path(); ctx.move_to(172, -60)
        for k in range(5):
            ctx.curve_to(180 + k * 18, -95, 190 + k * 18, -95, 190 + k * 18, -62)
        ctx.line_to(260, -60); ctx.close_path(); fl(ctx, (1, 1, 1), 4)
        ctx.move_to(185, -70); ctx.line_to(250, -72); setc(ctx, hx('7fe0ff')); ctx.set_line_width(8); ctx.stroke()
    if wet > 0:
        for k in range(3):
            ellipse(ctx, 190 + k * 30, -10 + 30 * wet + k * 6, 8, 11); setc(ctx, hx('7fd4ff') + (wet,)); ctx.fill()
    ctx.restore()


def fist(ctx, x, y, s, skin):
    ellipse(ctx, x, y, 58 * s, 50 * s); fl(ctx, skin, 6)
    for k in range(3):
        ctx.move_to(x - 30 * s + k * 26 * s, y - 40 * s); ctx.line_to(x - 30 * s + k * 26 * s, y - 14 * s)
    ink(ctx, 4); ctx.stroke()


def sink(ctx, x0=40, x1=480, top=1150):
    """counter + basin + tap, against the left wall"""
    rect_r(ctx, x0, top + 40, x1 - x0, FLOOR - top - 40, 10); fl(ctx, hx('ffb85a'), 8)   # cabinet
    for xx in ((x0 + x1) / 2 - 60, (x0 + x1) / 2 + 60):
        ellipse(ctx, xx, top + 180, 12, 12); fl(ctx, hx('fff27a'), 4)
    ctx.move_to((x0 + x1) / 2, top + 70); ctx.line_to((x0 + x1) / 2, FLOOR - 30); ink(ctx, 6); ctx.stroke()
    rect_r(ctx, x0 - 20, top, x1 - x0 + 40, 50, 14); fl(ctx, (1, 1, 1), 8)              # counter top
    mx = (x0 + x1) / 2
    ellipse(ctx, mx, top + 4, 150, 26); fl(ctx, hx('dff1ff'), 6)                         # basin rim
    rect_r(ctx, mx - 16, top - 130, 32, 130, 12); fl(ctx, hx('c8ccd8'), 6)              # tap
    rect_r(ctx, mx - 16, top - 140, 110, 34, 14); fl(ctx, hx('c8ccd8'), 6)
    ellipse(ctx, mx - 50, top - 120, 30, 16); fl(ctx, RED, 5)
    # cup with brushes
    rect_r(ctx, x1 - 110, top - 110, 80, 110, 14); fl(ctx, hx('7fd4ff'), 6)
    for k, c in enumerate((hx('ff5fa8'), hx('22b45a'), hx('ffd23f'))):
        ctx.move_to(x1 - 90 + k * 20, top - 100); ctx.line_to(x1 - 100 + k * 26, top - 200)
        setc(ctx, OUT); ctx.set_line_width(20); ctx.stroke_preserve(); setc(ctx, c); ctx.set_line_width(11); ctx.stroke()


def mirror(ctx, x, y, w, h, crack=0.0, fog=0.0):
    rect_r(ctx, x, y, w, h, 26); fl(ctx, hx('ffd23f'), 10)
    rect_r(ctx, x + 22, y + 22, w - 44, h - 44, 14); fl(ctx, hx('c8f0ff'), 6)
    for k in range(2):
        ctx.move_to(x + 70 + k * 70, y + 60); ctx.line_to(x + 30 + k * 70, y + 160)
    setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(16); ctx.stroke()
    if fog > 0:
        rect_r(ctx, x + 22, y + 22, w - 44, h - 44, 14); setc(ctx, STINK + (0.6 * fog,)); ctx.fill()
    if crack > 0:
        cx, cy = x + w * 0.55, y + h * 0.45
        rnd = random.Random(4)
        for k in range(7):
            a = k * 2 * math.pi / 7 + rnd.uniform(-0.2, 0.2); L = (0.25 + 0.2 * rnd.random()) * min(w, h) * crack
            ctx.move_to(cx, cy)
            ctx.line_to(cx + math.cos(a + 0.2) * L * 0.5, cy + math.sin(a + 0.2) * L * 0.5)
            ctx.line_to(cx + math.cos(a) * L, cy + math.sin(a) * L)
        ink(ctx, 5); ctx.stroke()


def flower(ctx, x, y, wilt=0.0, s=1.0):
    """vase on a shelf, base at (x, y)"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    stem_tip = (60 * wilt, -220 + 150 * wilt)
    ctx.move_to(0, -60); ctx.curve_to(0, -160, 30 * wilt, -220 + 40 * wilt, stem_tip[0], stem_tip[1])
    setc(ctx, OUT); ctx.set_line_width(18); ctx.stroke_preserve(); setc(ctx, GREEN); ctx.set_line_width(9); ctx.stroke()
    hx_, hy_ = stem_tip
    pc = clerp(hx('ff5fa8'), hx('8a7a5a'), wilt)
    for k in range(6):
        a = k * math.pi / 3 + wilt * 1.2
        ellipse(ctx, hx_ + math.cos(a) * 34, hy_ + math.sin(a) * 34 + 20 * wilt * (k % 2), 26, 20, a); fl(ctx, pc, 5)
    ellipse(ctx, hx_, hy_, 22, 22); fl(ctx, clerp(YEL, hx('a08a40'), wilt), 5)
    poly(ctx, [(-50, -80), (50, -80), (36, 0), (-36, 0)]); fl(ctx, BLUE, 7)
    ctx.restore()
    if wilt > 0.4:   # falling petals
        for k in range(3):
            t = ((wilt - 0.4) / 0.6 + k * 0.2) % 1
            ellipse(ctx, x + 60 * s + k * 30, y - 100 * s + 200 * t, 14, 10, t * 6); fl(ctx, pc, 3)


def clerp(a, b, t):
    return tuple(p + (q - p) * t for p, q in zip(a, b))


def stink(ctx, x, y, t, s, lf, a=1.0):
    """green breath cloud starting at (x, y), rolling +x, grown to t (0..1)"""
    if t <= 0:
        return
    rnd = random.Random(11)
    for k in range(14):
        u = k / 13
        if u > t:
            break
        px = x + 700 * u * s + 20 * math.sin(lf * 0.3 + k)
        py = y + rnd.uniform(-1, 1) * 120 * u * s + 14 * math.cos(lf * 0.25 + k)
        r = (60 + 160 * u) * s
        ellipse(ctx, px, py, r, r * 0.8); setc(ctx, clerp(STINK, hx('6fbf2a'), rnd.random()) + (0.85 * a,)); ctx.fill()
    for k in range(4):   # wiggly stink lines
        u = min(t, 0.3 + 0.2 * k)
        px = x + 700 * u * s; py = y - 200 * s
        ctx.move_to(px - 30, py)
        for j in range(4):
            ctx.rel_line_to(20 * (1 if j % 2 else -1) + 0 * lf, -36)
        setc(ctx, hx('3f7a1a') + (a,)); ctx.set_line_width(9); ctx.stroke()


def foam(ctx, cx, cy, amt, lf, seed=3, spread=1.0):
    rnd = random.Random(seed)
    n = int(80 * amt)
    for k in range(n):
        a = rnd.uniform(0, 2 * math.pi); d = rnd.uniform(0, 1) ** 0.6 * 900 * amt * spread
        r = rnd.uniform(30, 90) * (0.6 + 0.6 * amt) + 6 * math.sin(lf * 0.5 + k)
        ellipse(ctx, cx + math.cos(a) * d, cy + math.sin(a) * d * 1.2, r, r); fl(ctx, (1, 1, 1), 4)
        ellipse(ctx, cx + math.cos(a) * d - r * 0.3, cy + math.sin(a) * d * 1.2 - r * 0.3, r * 0.22, r * 0.18); setc(ctx, hx('c8f0ff')); ctx.fill()


def water(ctx, x, y0, y1, lf, a=1.0):
    ctx.rectangle(x - 16, y0, 32, y1 - y0); setc(ctx, hx('7fd4ff') + (0.9 * a,)); ctx.fill()
    for k in range(4):
        yy = y0 + ((lf * 22 + k * 50) % max(1, (y1 - y0)))
        ctx.move_to(x - 6, yy); ctx.line_to(x - 6, yy + 30)
    setc(ctx, (1, 1, 1, 0.8 * a)); ctx.set_line_width(5); ctx.stroke()


def bathroom(ctx, lights=True, wilt=0.0, crack=0.0, fog=0.0):
    tiles(ctx, hx('8fd8ff') if lights else hx('22305e'))
    mirror(ctx, 70, 620, 420, 420, crack, fog)
    # shelf with flower
    rect_r(ctx, 640, 860, 260, 30, 10); fl(ctx, hx('ffb85a'), 6)
    flower(ctx, 760, 860, wilt, 0.9)
    # towel hook
    rect_r(ctx, 640, 1000, 190, 260, 30); fl(ctx, hx('ff8ac0') if lights else hx('6a3a6a'), 7)
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('ffffff') if lights else hx('5a6a9a')); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 160, FLOOR, 80, 1500); setc(ctx, hx('dfe6f4') if lights else hx('4a5a8a')); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()
    sink(ctx)


def doorway(ctx, x=760, w=330, lit=True):
    rect_r(ctx, x, 560, w, FLOOR - 560, 10); fl(ctx, hx('fff2b0') if lit else hx('101830'), 9)


def shine_teeth(ctx, cx, cy, Rt, lf, k=1.0):
    mx, my = cx + 0.04 * Rt, cy + 0.5 * Rt
    sparkle(ctx, mx + 0.12 * Rt, my - 0.05 * Rt, (0.12 + 0.03 * math.sin(lf * 0.6)) * Rt * k, (1, 1, 1))
    sparkle(ctx, mx - 0.14 * Rt, my + 0.02 * Rt, (0.06 + 0.02 * math.cos(lf * 0.7)) * Rt * k, YEL)


# ------------------------------------------------------------------ shared shots
def opening_face(ctx, f, lf, lab=True):
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 50)), -3, shake_at(lf, [0], 9, 10), f)
    tiles(ctx, hx('6fd6ff'))
    rays(ctx, 540, 940, 240, 1600, lf * 0.02, col=(1, 1, 1), a=0.3, n=16)
    face(ctx, BOY, P(eye='happy', mouth='grin', head=0), 520, 930, 300, -0.08)
    shine_teeth(ctx, 520, 930, 300, lf)
    bob = 12 * math.sin(lf * 0.4)
    toothbrush(ctx, 790, 1310 + bob, -1.1, 1.3, paste=True)
    fist(ctx, 790, 1310 + bob, 1.3, BOY['skin'])
    sweat(ctx, 760, 700, lf, 0.9)
    ctx.restore()
    if lab:
        label(ctx, "\"YES, I BRUSHED!\"", 540, LY + 40, 112, (1, 1, 1), -0.03, pop(lf, 0, 4) if lf > 0 else 1)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 52:
        opening_face(ctx, f, f)
    else:
        lf = f - 52
        pull = eout(pop(lf, 0, 14))
        ctx.save(); cam(ctx, 560, 1100, 1.3 - 0.27 * pull, 0, shake_at(lf, [0], 8, 12), f)
        bathroom(ctx)
        doorway(ctx)
        b = draw_hip(ctx, 450, FLOOR - 165, 0.98, 1, BOY, P(eye='shock' if lf >= 30 else 'happy', mouth='wavy' if lf >= 30 else 'grin',
                                                              rsh=-25, rel=-50, lsh=10, lel=-10))
        hx_, hy_ = b['front']
        toothbrush(ctx, hx_, hy_, -0.5, 0.55)
        if lf >= 30:
            sweat(ctx, b['head'][0] + 70, b['head'][1] - 60, lf, 0.7)
        draw_hip(ctx, 880, FLOOR - 220, 1.15, -1, MOM, P(eye='glare', mouth='flat', rsh=-130, rel=-110, lsh=130, lel=-110, head=-6))
        ctx.restore()
        if lf < 30:
            label(ctx, "\"Did you REALLY?\"", 540, LY + 40, 104, YEL, -0.03, pop(lf, 0, 4))
        else:
            label(ctx, "\"...yes?\"", 540, LY + 40, 112, (1, 1, 1), 0.03, pop(lf, 30, 34))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 66:
        # insert at the tap: brush under the water for ONE second
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.08 * eout(pop(lf, 0, 66)), 2, shake_at(lf, [24], 8, 10), f)
        tiles(ctx, hx('8fd8ff'))
        # big tap from the top-left
        rect_r(ctx, 120, 560, 420, 110, 50); fl(ctx, hx('c8ccd8'), 10)
        rect_r(ctx, 420, 600, 120, 170, 30); fl(ctx, hx('c8ccd8'), 10)
        ellipse(ctx, 200, 560, 90, 40); fl(ctx, RED, 8)
        water(ctx, 480, 770, 1500, lf)
        ellipse(ctx, 540, 1520, 520, 120); fl(ctx, (1, 1, 1), 10)
        ellipse(ctx, 540, 1520, 440, 80); fl(ctx, hx('dff1ff'), 6)
        # hand sweeps in from the right, dips for a beat, sweeps out
        t_in = eout(pop(lf, 4, 18)); t_out = ein(pop(lf, 30, 42))
        hxp = 1300 - 760 * t_in + 760 * t_out
        wet = pop(lf, 22, 30)
        toothbrush(ctx, hxp + 60, 1080, math.pi, 1.6, paste=True, wet=wet)
        fist(ctx, hxp + 60, 1080, 1.7, BOY['skin'])
        ctx.move_to(hxp + 120, 1080); ctx.line_to(hxp + 700, 1180); setc(ctx, OUT); ctx.set_line_width(100); ctx.stroke()
        ctx.move_to(hxp + 120, 1080); ctx.line_to(hxp + 700, 1180); setc(ctx, BOY['shirt']); ctx.set_line_width(84); ctx.stroke()
        if 22 <= lf < 34:
            for k in range(6):
                a = -math.pi / 2 + (k - 2.5) * 0.35; d = 60 + 18 * (lf - 22)
                ellipse(ctx, 480 + math.cos(a) * d, 1050 + math.sin(a) * d * 0.6, 14, 18); setc(ctx, hx('7fd4ff')); ctx.fill()
        ctx.restore()
        if lf < 22:
            label(ctx, "*sneaky...*", 540, LY + 40, 100, (1, 1, 1), 0.03, pop(lf, 2, 6))
        else:
            label(ctx, "*SPLISH!*", 540, LY + 40, 128, BLUE, -0.04, pop(lf, 22, 26))
    else:
        il = lf - 66
        # smug wink ECU with the dripping brush
        ctx.save(); cam(ctx, 540, 1000, 1.05 + 0.06 * eout(pop(il, 0, 50)), -2, shake_at(il, [0], 8, 10), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb85a')); ctx.fill()
        rays(ctx, 540, 900, 240, 1600, il * 0.03, col=(1, 1, 0.8), a=0.4, n=16)
        face(ctx, BOY, P(eye='smug', mouth='grin', head=0), 480, 900, 280, 0.06)
        # wink: close the right eye
        ex, ey, rx = eye_pos(480, 900, 280)[1]
        if 10 <= il < 34:
            ellipse(ctx, ex, ey, rx * 0.9, rx * 1.1); setc(ctx, BOY['skin']); ctx.fill()
            ctx.new_path(); ctx.arc(ex, ey - 6, rx * 0.6, 0.15 * math.pi, 0.85 * math.pi); ink(ctx, 12); ctx.stroke()
        toothbrush(ctx, 760, 1290, -1.0, 1.3, paste=True, wet=1.0)
        fist(ctx, 760, 1290, 1.3, BOY['skin'])
        sparkle(ctx, 880, 860, 40 + 10 * math.sin(il * 0.5), (1, 1, 1))
        ctx.restore()
        if il < 26:
            label(ctx, "\"DONE!\"", 540, LY + 40, 128, YEL, -0.03, pop(il, 0, 4))
        else:
            label(ctx, "\"Brushed. Technically.\"", 540, LY + 40, 88, (1, 1, 1), 0.03, pop(il, 26, 30))
    card(ctx, 'p2', f, 112, 228)


def s3(ctx, f):
    lf = f - 230
    if lf < 44:
        # Mom ECU leaning in: say HAAA
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.08 * eout(pop(lf, 0, 44)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('b98aff')); ctx.fill()
        rays(ctx, 540, 900, 240, 1600, lf * 0.02, col=(1, 1, 1), a=0.3, n=16)
        face(ctx, MOM, P(eye='smug', mouth='smile', head=0), 560, 960, 300, 0.05)
        ctx.restore()
        label(ctx, "\"Okay. Say 'HAAA'.\"", 540, LY + 40, 100, (1, 1, 1), -0.02, pop(lf, 2, 6))
    elif lf < 100:
        il = lf - 44
        # the breath: side by side, stink cloud rolls right; Mom's hair blows, flower wilts, mirror cracks
        ctx.save(); cam(ctx, 540, 1040, 1.0, 0, shake_at(il, [8, 30], 10, 14) + (4 if il > 8 else 0), f)
        t = eout(pop(il, 6, 30))
        bathroom(ctx, wilt=pop(il, 14, 36), crack=eout(pop(il, 30, 34)), fog=0.6 * t)
        face(ctx, BOY, P(eye='closed', mouth='scream', head=0), 240, 1130, 170, 0.12)
        stink(ctx, 330, 1180, t, 1.0, il)
        lean = 0.25 * t
        face(ctx, MOM, P(eye='shock', mouth='scream' if il > 12 else 'open', head=0), 790, 1120 + 20 * t, 180, lean, -1)
        if il > 10:   # hair blown back streaks
            for k in range(4):
                ctx.move_to(900, 1000 + k * 40); ctx.line_to(1040 + 20 * math.sin(il + k), 980 + k * 44)
            setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(8); ctx.stroke()
        stink(ctx, 330, 1180, t, 1.0, il, 0.35)
        ctx.restore()
        if il < 30:
            label(ctx, "\"HAAAAAA...\"", 540, LY + 40, 120, STINK, -0.03, pop(il, 4, 8))
        else:
            label(ctx, "*CRACK!*", 540, LY + 40, 130, (1, 1, 1), 0.05, pop(il, 30, 34))
    else:
        il = lf - 100
        # Mom ECU, green-faced, glare: BRUSH. NOW.
        ctx.save(); cam(ctx, 540, 1000, 1.15 - 0.1 * eout(pop(il, 0, 8)), -3, shake_at(il, [0, 16], 12, 18), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('e0263a')); ctx.fill()
        rays(ctx, 540, 900, 240, 1600, il * 0.05, col=(1, 0.6, 0.4), a=0.5, n=18)
        face(ctx, MOM, P(eye='glare', mouth='flat', head=0), 540, 920, 300, 0)
        ellipse(ctx, 540, 960, 300 * 1.02, 300 * 1.0); setc(ctx, STINK + (0.28,)); ctx.fill()
        stink(ctx, -200, 1300, 0.4, 1.0, il, 0.5)
        ctx.restore()
        label(ctx, "\"BRUSH. NOW.\"", 540, LY + 40, 130, YEL, -0.03, pop(il, 0, 4))
    card(ctx, 'p3', f, 232, 368)


def s4(ctx, f):
    lf = f - 370
    if lf < 70:
        # super-speed scrubbing at the sink, foam grows
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.12 * eout(pop(lf, 0, 70)), 3 * math.sin(lf * 0.9), 6, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('22b45a')); ctx.fill()
        rays(ctx, 540, 900, 200, 1600, lf * 0.08, col=(1, 1, 1), a=0.3, n=20)
        amt = eout(pop(lf, 4, 66))
        face(ctx, BOY, P(eye='closed' if (lf // 3) % 2 else 'shock', mouth='scream', head=0), 540, 900, 280, 0.08 * math.sin(lf * 1.7))
        foam(ctx, 560, 1080, 0.15 + 0.25 * amt, lf, seed=5, spread=0.6)
        bx = 600 + 90 * math.sin(lf * 2.2)
        toothbrush(ctx, bx + 150, 1060, math.pi + 0.2, 1.2, paste=False)
        fist(ctx, bx + 150, 1060, 1.3, BOY['skin'])
        for k in range(5):   # speed lines
            yy = 960 + k * 50
            ctx.move_to(bx + 300, yy); ctx.line_to(bx + 520, yy)
        setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(10); ctx.stroke()
        foam(ctx, 540, 1250, max(0, amt - 0.35) * 1.3, lf, seed=8, spread=0.8)
        ctx.restore()
        label(ctx, "*SCRUB SCRUB SCRUB!*", 540, LY + 40, 96, (1, 1, 1), 0.03 * math.sin(lf * 0.8), pop(lf, 2, 6))
    else:
        il = lf - 70
        # foam fills, POP: blinding sparkle smile
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(il, 10, 60)), 0, shake_at(il, [10], 12, 20), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('6fd6ff')); ctx.fill()
        rays(ctx, 540, 940, 220, 1700, il * 0.04, col=(1, 1, 0.7), a=0.6, n=20)
        face(ctx, BOY, P(eye='happy', mouth='grin', head=0), 540, 930, 300, 0)
        shine_teeth(ctx, 540, 930, 300, il, 1.6)
        for j in range(6):
            sparkle(ctx, 540 + 380 * math.cos(il * 0.1 + j), 930 + 360 * math.sin(il * 0.1 + j), 30 + 10 * math.sin(il * 0.4 + j), YEL)
        if il < 12:
            foam(ctx, 540, 1000, 1.0, il, seed=8, spread=1.0)
        ctx.restore()
        if il < 10:
            pass
        elif il < 40:
            label(ctx, "*DING!*", 540, LY + 40, 140, YEL, -0.04, pop(il, 10, 14))
        else:
            label(ctx, "\"Minty FRESH!\"", 540, LY + 40, 116, (1, 1, 1), 0.03, pop(il, 40, 44))
    card(ctx, 'p4', f, 372, 496)


def s5(ctx, f):
    lf = f - 500
    if lf < 60:
        # midnight: Dad tiptoes in, same wet-brush trick
        lit = lf >= 44
        ctx.save(); cam(ctx, 520, 1100, 1.12, 0, shake_at(lf, [44], 10, 16), f)
        bathroom(ctx, lights=lit)
        doorway(ctx, lit=lit)
        tip = math.sin(lf * 0.5)
        b = draw_hip(ctx, 500, FLOOR - 230 + 10 * abs(tip), 1.1, -1, DAD,
                     P(eye='shock' if lit else 'smug', mouth='scream' if lit else 'grin', rsh=-80, rel=-40, lsh=30, lel=-30, lhip=10 + 10 * tip, rhip=-10 - 10 * tip))
        hx_, hy_ = b['front']
        toothbrush(ctx, 335 + 194, 1085, math.pi, 0.9, wet=pop(lf, 22, 30))
        if 16 <= lf < 36:
            water(ctx, 335, 1012, 1150, lf)
        if not lit:
            ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, (0.05, 0.05, 0.2, 0.2)); ctx.fill()
        else:
            sweat(ctx, b['head'][0] + 60, b['head'][1] - 60, lf, 0.8)
        ctx.restore()
        if lf < 22:
            label(ctx, "*tiptoe... tiptoe...*", 540, LY + 40, 92, (1, 1, 1), 0.03, pop(lf, 2, 6))
        elif lf < 44:
            label(ctx, "*splish* \"...Done!\"", 540, LY + 40, 100, BLUE, -0.03, pop(lf, 22, 26))
        else:
            label(ctx, "*CLICK!*", 540, LY + 40, 130, YEL, 0.04, pop(lf, 44, 48))
    elif lf < 120:
        il = lf - 60
        # the doorway: Mom + kid, arms crossed - Dad inset sweating
        ctx.save(); cam(ctx, 700, 1080, 1.05 + 0.05 * eout(pop(il, 0, 60)), 0, shake_at(il, [0], 8, 12), f)
        tiles(ctx, hx('8fd8ff'))
        doorway(ctx, 300, 760)
        draw_hip(ctx, 520, FLOOR - 220, 1.15, 1, MOM, P(eye='glare', mouth='flat', rsh=-130, rel=-110, lsh=130, lel=-110, head=4))
        draw_hip(ctx, 820, FLOOR - 165, 0.98, -1, BOY, P(eye='glare', mouth='smile', rsh=-130, rel=-110, lsh=130, lel=-110, head=-4))
        ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, (1, 1, 1)); ctx.fill()
        ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()
        ctx.restore()
        label(ctx, "\"Say 'HAAA', DAD.\"", 540, LY + 40, 108, YEL, -0.03, pop(il, 2, 6))
        if il >= 14:
            u = eout(pop(il, 14, 22))
            ctx.save(); ctx.translate(820 + 360 * (1 - u), 680)
            ellipse(ctx, 0, 0, 130, 130); fl(ctx, YEL, 8); ctx.save(); ellipse(ctx, 0, 0, 122, 122); ctx.clip()
            face(ctx, DAD, P(eye='shock', mouth='wavy', head=0), 0, 10, 88, 0.05)
            ctx.restore(); ctx.restore()
            sweat(ctx, 720 + 360 * (1 - u), 590, il, 0.7)
    else:
        il = lf - 120
        opening_face(ctx, f, il, True)
    if lf < 120:
        card(ctx, 'p5', f, 502, 618)
    else:
        card(ctx, 'p1', f, 620)


SHOTS = [(0, s1), (110, s2), (230, s3), (370, s4), (500, s5)]
CUTS = (52, 110, 176, 230, 274, 330, 370, 440, 500, 560, 620)


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
                              "-i", "out/did_you_brush_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
