"""'Due Tomorrow' - original, general-audience comedy short, 22s.
Hook: ECU Mom mid-shriek, coffee flying, clock at 9 PM: "IT'S DUE... TOMORROW?!"
Beat 1: kid casually unfolds a crumpled note: "Oh yeah... I need a VOLCANO. For TOMORROW."
Beat 2: 10 PM spinning overhead table cam - cardboard, tape, glue: parents in panic mode.
 Split: parents frantic / kid asleep on the sofa *SNORE*.
Beat 3: 2 AM test: Dad in goggles "just a LITTLE bit..." -> giant pink foam eruption, foam-soaked parents "...it WORKS."
Turn: science fair - kid with a 1ST ribbon "I did it ALL by MYSELF!" -> pan: a row of zombie parents with coffee "...so did WE."
Twist: back home: "Oh! And I need a SOLAR SYSTEM..." Mom ECU twitch "...for WHEN?" -> "TOMORROW!" -> parents TIMBER,
 cut back to the opening shriek (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos, zigs, lids, bloodshot, clock, zzz
from scenes48 import label1, label2
import scenes13
from scenes13 import card as _card13
import random

BOY = dict(doodle.BOY, hood=False)
MOM = doodle.MOM_G
DAD = doodle.DAD
NMOM = doodle.NMOM
NEIGH = doodle.NEIGHBOR
N = 660
FLOOR = 1460
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
CARD = hx('d9a066')
ROCK = hx('8a5a3c')
LAVA = hx('ff4a2a')
FOAM = hx('ff9fc8')

CAPS = {
    'p1': [[("SUNDAY,", OUT)], [("9 PM", RED)]],
    'p2': [[("10 PM:", OUT)], [("PANIC MODE", ORANGE)]],
    'p3': [[("2 AM:", OUT)], [("THE TEST RUN", PURPLE)]],
    'p4': [[("MONDAY:", OUT)], [("SCIENCE FAIR", BLUE)]],
    'p5': [[("MONDAY,", OUT)], [("4 PM", GREEN)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def kitchen(ctx, wall=hx('7fd6ff')):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, wall); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 130, -3000, 50, 7000); setc(ctx, light(wall, 0.12)); ctx.fill()
    # cupboards
    for x in (90, 330):
        rect_r(ctx, x, 380, 220, 260, 14); fl(ctx, hx('ffe9a0'), 7)
        ellipse(ctx, x + 190, 520, 10, 10); fl(ctx, hx('ff8a1f'), 3)
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('f2d6a8')); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 150, FLOOR, 5, 1500); setc(ctx, hx('d9b47e')); ctx.fill()
    ctx.rectangle(-3000, FLOOR - 6, 7000, 12); setc(ctx, OUT); ctx.fill()


def table(ctx, x0, x1, top):
    rect_r(ctx, x0, top, x1 - x0, 46, 12); fl(ctx, hx('c46a2e'), 8)
    for x in (x0 + 50, x1 - 80):
        ctx.rectangle(x, top + 46, 30, FLOOR - top - 46); fl(ctx, hx('9a4e1e'), 6)


def note(ctx, x, y, s=1.0, a=0.0, lines=("SCIENCE FAIR:", "BUILD A", "VOLCANO!", "DUE MONDAY")):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-150, -190), (-40, -200), (60, -184), (150, -196), (142, -60), (156, 70), (146, 196), (20, 186), (-90, 200), (-152, 186), (-140, 40), (-156, -80)])
    fl(ctx, (1, 1, 1), 6)
    for k, (ax, ay, bx, by) in enumerate(((-120, -100, 40, -160), (-60, 60, 120, 0), (-130, 150, 30, 120))):
        ctx.move_to(ax, ay); ctx.line_to(bx, by); setc(ctx, (0.8, 0.8, 0.88)); ctx.set_line_width(3); ctx.stroke()
    for k, ln in enumerate(lines):
        text(ctx, ln, 0, -120 + k * 82, 46 if k != 2 else 58, RED if k == 2 else (0.2, 0.2, 0.35), outline=(1,1,1,0), ow=1, shadow=False, maxw=270)
    ctx.restore()


def mug(ctx, x, y, s=1.0, a=0.0, col=hx('ff5fa8'), steam=True, lf=0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(62, -10, 34, -math.pi / 2, math.pi / 2); ink(ctx, 26); ctx.stroke_preserve(); setc(ctx, col); ctx.set_line_width(12); ctx.stroke()
    rect_r(ctx, -60, -70, 120, 130, 20); fl(ctx, col, 6)
    ellipse(ctx, 0, -66, 56, 12); setc(ctx, hx('5a3018')); ctx.fill()
    if steam:
        for k in range(2):
            ctx.move_to(-20 + k * 40, -90)
            ctx.curve_to(-40 + k * 40, -130 + 6 * math.sin(lf * 0.3 + k), 0 + k * 40, -150, -20 + k * 40, -190)
        setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()


def volcano(ctx, x, base, s=1.0, built=1.0, paint=1.0, lava=1.0):
    """cone volcano with crater; built 0..1 grows from the base, paint 0..1 cardboard->rock"""
    if built <= 0:
        return
    ctx.save(); ctx.translate(x, base); ctx.scale(s, s * built)
    col = tuple(lerp(a, b, paint) for a, b in zip(CARD, ROCK))
    poly(ctx, [(-260, 0), (260, 0), (80, -300), (-80, -300)]); fl(ctx, col, 8)
    if paint < 0.5:   # cardboard strips + tape
        for k in range(4):
            ctx.move_to(-230 + k * 20, -40 - k * 70); ctx.line_to(230 - k * 20, -40 - k * 70); setc(ctx, dark(CARD, 0.85)); ctx.set_line_width(6); ctx.stroke()
        poly(ctx, [(-60, -10), (-20, -10), (40, -290), (0, -290)]); setc(ctx, (1, 1, 1, 0.55)); ctx.fill()
    else:
        for (px, py) in ((-120, -60), (60, -130), (-20, -210), (150, -40)):
            ellipse(ctx, px, py, 26, 14); setc(ctx, dark(ROCK, 0.8)); ctx.fill()
    ctx.restore()
    ctx.save(); ctx.translate(x, base - 300 * s * built); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 80, 18); fl(ctx, hx('3a2010'), 6)
    if lava > 0 and paint >= 0.5:
        for dx, ln in ((-50, 90), (10, 150), (55, 70)):
            ctx.move_to(dx, 0); ctx.line_to(dx * 1.4, ln * lava)
            setc(ctx, OUT); ctx.set_line_width(36); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke_preserve()
            setc(ctx, LAVA); ctx.set_line_width(24); ctx.stroke()
        ellipse(ctx, 0, 2, 70, 14); setc(ctx, LAVA); ctx.fill()
    ctx.restore()


def goggles(ctx, b, col=hx('7ff0ff')):
    (lx, ly), (rx, ry) = b['eyeL'], b['eyeR']
    r = b['R'] * 0.26
    ctx.move_to(lx - r * 1.6, ly); ctx.line_to(rx + r * 1.6, ry); ink(ctx, 10); ctx.stroke()
    for ex, ey in ((lx, ly), (rx, ry)):
        ellipse(ctx, ex, ey, r * 1.15, r); setc(ctx, col + (0.55,)); ctx.fill_preserve(); ink(ctx, 9); ctx.stroke()


def eyebags(ctx, b, col=(0.45, 0.25, 0.55, 0.7)):
    r = b['R'] * 0.2
    for ex, ey in (b['eyeL'], b['eyeR']):
        ctx.new_path(); ctx.arc(ex, ey + r * 0.4, r * 1.1, 0.2 * math.pi, 0.8 * math.pi); setc(ctx, col); ctx.set_line_width(b['R'] * 0.06); ctx.stroke()


def droop(ctx, b, ch, amt=0.5):
    """half-shut lids on a full-body 'normal' eye"""
    r = b['R'] * 0.2
    for ex, ey in (b['eyeL'], b['eyeR']):
        ctx.rectangle(ex - r * 1.2, ey - r * 2.2, r * 2.4, r * (1.2 + 1.4 * amt)); setc(ctx, ch['skin']); ctx.fill()
        ctx.move_to(ex - r * 1.0, ey - r + 1.4 * r * amt); ctx.line_to(ex + r * 1.0, ey - r + 1.4 * r * amt); ink(ctx, b['R'] * 0.05); ctx.stroke()


def foam_blob(ctx, x, y, w, h, seed=1, n=18, col=FOAM):
    rnd = random.Random(seed)
    pts = [(x + rnd.uniform(-w / 2, w / 2), y + rnd.uniform(-h / 2, h / 2), rnd.uniform(0.2, 0.34) * min(w, h)) for _ in range(n)]
    for px, py, r in pts:
        ellipse(ctx, px, py, r, r); fl(ctx, col, 5)
    for px, py, r in pts:
        ellipse(ctx, px, py, r * 0.9, r * 0.9); setc(ctx, col); ctx.fill()
        ellipse(ctx, px - r * 0.3, py - r * 0.3, r * 0.22, r * 0.16); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()


def ribbon(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    for sx in (-1, 1):
        poly(ctx, [(sx * 10, 20), (sx * 60, 170), (sx * 40, 150), (sx * 20, 180), (sx * -20, 30)]); fl(ctx, BLUE, 5)
    for k in range(12):
        an = k * math.pi / 6
        ellipse(ctx, math.cos(an) * 62, math.sin(an) * 62, 30, 30); fl(ctx, BLUE, 5)
    ellipse(ctx, 0, 0, 70, 70); setc(ctx, BLUE); ctx.fill()
    ellipse(ctx, 0, 0, 52, 52); fl(ctx, YEL, 5)
    text(ctx, "1ST", 0, 16, 40, OUT, outline=(1,1,1,0), ow=1, shadow=False)
    ctx.restore()


def planet(ctx, x, y, r, col, ringed=False):
    if ringed:
        ellipse(ctx, x, y, r * 1.8, r * 0.45, -0.3); ink(ctx, 6); ctx.stroke()
    ellipse(ctx, x, y, r, r); fl(ctx, col, 6)
    if ringed:
        ctx.new_path(); ctx.save(); ctx.translate(x, y); ctx.rotate(-0.3); ctx.scale(1.8, 0.45)
        ctx.arc(0, 0, r, 0, math.pi); ctx.restore(); setc(ctx, YEL); ctx.set_line_width(10); ctx.stroke()


# ------------------------------------------------------------------ opening
def opening_face(ctx, f, lf, lab=True):
    """ECU: Mom mid-shriek, coffee flying, clock at 9 PM"""
    sh = shake_at(lf, [0], 12, 20) + 7
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eout(pop(lf, 0, 40)), 0, sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffcf3d')); ctx.fill()
    rays(ctx, 540, 860, 260, 1700, lf * 0.06, col=(1, 0.45, 0.35), a=0.45, n=18)
    clock(ctx, 840, 560, 80, 9, 0)
    cx, cy, R = 520 + 6 * math.sin(lf * 2.1), 880, 290
    face(ctx, MOM, P(eye='shock', mouth='scream', head=0), cx, cy, R, -0.04 + 0.02 * math.sin(lf * 1.7))
    # coffee mug flying up out of her hand + splash
    u = (lf % 60) / 60
    mug(ctx, 170, 1200 - 120 * math.sin(u * math.pi), 1.0, -0.6 - u * 2, steam=False)
    rnd = random.Random(5)
    for k in range(7):
        ellipse(ctx, 150 + rnd.uniform(-60, 80), 1080 - rnd.uniform(0, 200) - 40 * math.sin(u * 4 + k), 18, 14); fl(ctx, hx('7a4320'), 4)
    ctx.restore()
    if lab:
        label2(ctx, "\"IT'S DUE...", "TOMORROW?!\"", (1, 1, 1), 1.0 if f < 60 else pop(lf, 0, 3), 116, col2=RED)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 56:
        opening_face(ctx, f, f)
    else:
        lf = f - 56
        # kitchen: kid casually unfolds the crumpled note, parents behind freeze
        ctx.save(); cam(ctx, 560, 1080, 1.0 + 0.05 * eout(pop(lf, 0, 54)), 0, 0, f)
        kitchen(ctx)
        table(ctx, 560, 1100, 1180)
        mug(ctx, 900, 1170, 0.8, lf=lf)
        pm = P(torso=0, lhip=-6, lkn=0, rhip=6, rkn=0, lsh=150, lel=20, rsh=-150, rel=-20, eye='shock', mouth='open', head=4)
        draw(ctx, 690, FLOOR - 186 * 1.3, 1.3, -1, MOM, pm)
        pd = P(torso=0, lhip=-6, lkn=0, rhip=6, rkn=0, lsh=20, lel=-10, rsh=20, rel=-10, eye='shock', mouth='scream', head=-4)
        draw(ctx, 880, FLOOR - 186 * 1.35, 1.35, -1, DAD, pd)
        pk = P(torso=0, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=-120, lel=-30, rsh=12, rel=-15, eye='smug', mouth='smile', head=-6)
        draw(ctx, 270, FLOOR - 186 * 1.0, 1.0, 1, BOY, pk)
        unf = eout(pop(lf, 2, 14))
        note(ctx, 420, 980, 0.3 + 0.6 * unf, -0.1 + 0.06 * math.sin(lf * 0.2))
        ctx.restore()
        label2(ctx, "\"Oh yeah... I need", "a VOLCANO.\"", (1, 1, 1), pop(lf, 4, 8), 96, col2=YEL)
    card(ctx, 'p1', f, -6, 110)


def s2(ctx, f):
    lf = f - 110
    if lf < 75:
        # overhead spinning table: parents' hands blur, volcano grows out of cardboard
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.1 * eout(pop(lf, 0, 75)), lf * 2.4, shake_at(lf, [0, 24, 48], 6, 10), f)
        ctx.rectangle(-1000, -1000, 3200, 4000); setc(ctx, hx('c46a2e')); ctx.fill()
        for i in range(-10, 20):
            ctx.rectangle(-1000, i * 140, 3200, 6); setc(ctx, hx('a8561f')); ctx.fill()
        rnd = random.Random(8)
        for k in range(10):     # scraps of cardboard + tape rolls
            x, y = rnd.uniform(60, 1020), rnd.uniform(400, 1500)
            if abs(x - 540) < 240 and abs(y - 960) < 240:
                continue
            ctx.save(); ctx.translate(x, y); ctx.rotate(rnd.uniform(0, 3))
            if k % 3 == 0:
                ellipse(ctx, 0, 0, 50, 50); fl(ctx, hx('dddde8'), 6); ellipse(ctx, 0, 0, 22, 22); fl(ctx, hx('c46a2e'), 5)
            else:
                rect_r(ctx, -70, -40, 140, 80, 6); fl(ctx, CARD, 5)
            ctx.restore()
        g = eout(pop(lf, 0, 70))
        for k in range(int(1 + g * 6)):   # top-down cone rings
            r = 240 - k * 30
            ellipse(ctx, 540, 960, r, r); fl(ctx, CARD if k % 2 else dark(CARD, 0.9), 6)
        ellipse(ctx, 540, 960, 50, 50); fl(ctx, hx('3a2010'), 5)
        # blurred hands (4) zipping around
        for k in range(4):
            a = lf * 0.4 + k * math.pi / 2 + 0.5 * math.sin(lf * 0.5 + k)
            hx_, hy_ = 540 + math.cos(a) * 330, 960 + math.sin(a) * 330
            for tr in range(3):
                aa = a - tr * 0.18
                ellipse(ctx, 540 + math.cos(aa) * 330, 960 + math.sin(aa) * 330, 44, 44); setc(ctx, (MOM if k % 2 else DAD)['skin'] + (0.3 * (3 - tr) / 3,)); ctx.fill()
            ctx.move_to(hx_, hy_); ctx.line_to(540 + math.cos(a) * 1100, 960 + math.sin(a) * 1100)
            setc(ctx, INK); ctx.set_line_width(84); ctx.stroke_preserve(); setc(ctx, (MOM if k % 2 else DAD)['shirt']); ctx.set_line_width(70); ctx.stroke()
            ellipse(ctx, hx_, hy_, 50, 50); fl(ctx, (MOM if k % 2 else DAD)['skin'], 6)
            for j in range(4):
                fa = a + math.pi + (j - 1.5) * 0.35
                ellipse(ctx, hx_ + math.cos(fa) * 52, hy_ + math.sin(fa) * 52, 16, 16); fl(ctx, (MOM if k % 2 else DAD)['skin'], 4)
        ctx.restore()
        if lf < 24:
            label1(ctx, "*RIIIP!*", YEL, pop(lf, 1, 4), 140)
        elif lf < 48:
            label1(ctx, "*SNIP SNIP!*", (1, 1, 1), pop(lf, 24, 27), 130, 0.04)
        else:
            label1(ctx, "\"MORE GLUE!!\"", ORANGE, pop(lf, 48, 51), 130)
        card(ctx, 'p2', f, 112, 180)
    else:
        il = lf - 75
        # split: parents frantic (top) / kid asleep on the sofa (bottom)
        ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
        ctx.save(); cam(ctx, 540, 720, 0.85, 0, 5, f, sy=600)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff7a4a')); ctx.fill()
        rays(ctx, 540, 700, 140, 1300, il * 0.05, col=(1, 0.9, 0.4), a=0.35, n=16)
        volcano(ctx, 540, 940, 0.75, 1.0, eout(pop(il, 0, 50)), 0)
        bm = draw(ctx, 250, 940 - 186 * 1.05 + 8 * math.sin(il * 1.3), 1.05, 1, MOM,
                  P(torso=8, lsh=-110 + 40 * math.sin(il * 1.4), lel=-30, rsh=-60, rel=-20, eye='shock', mouth='open', lhip=-10, lkn=0, rhip=10, rkn=0))
        bd = draw(ctx, 830, 940 - 186 * 1.1 + 8 * math.sin(il * 1.5 + 1), 1.1, -1, DAD,
                  P(torso=8, lsh=-100 + 40 * math.sin(il * 1.6), lel=-30, rsh=-50, rel=-30, eye='glare', mouth='scream', lhip=-10, lkn=0, rhip=10, rkn=0))
        zigs(ctx, bm['head'][0], bm['head'][1], 130, il, n=5)
        ctx.restore(); ctx.restore()
        ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
        ctx.rectangle(0, 960, W, 960); setc(ctx, hx('2a3a7a')); ctx.fill()
        for k in range(14):
            rnd = random.Random(k)
            sparkle(ctx, rnd.uniform(40, 1040), rnd.uniform(1000, 1180), 8 + 4 * math.sin(il * 0.3 + k), (1, 1, 0.8))
        rect_r(ctx, 120, 1220, 840, 230, 40); fl(ctx, hx('ff5a7a'), 8)
        rect_r(ctx, 60, 1170, 130, 300, 50); fl(ctx, hx('e84468'), 8)
        rect_r(ctx, 890, 1170, 130, 300, 50); fl(ctx, hx('e84468'), 8)
        ctx.save(); ctx.translate(540, 1200); ctx.rotate(math.radians(-90)); ctx.translate(-540, -1200)
        breath = 4 * math.sin(il * 0.25)
        draw(ctx, 540, 1200 - 186 * 0.95 + breath, 0.95, 1, BOY,
             P(torso=0, lhip=-4, lkn=0, rhip=4, rkn=0, lsh=-170, lel=0, rsh=10, rel=-60, eye='closed', mouth='open', head=0))
        ctx.restore()
        zzz(ctx, 380, 1150, il, 1.0)
        ctx.restore()
        ctx.rectangle(0, 952, W, 16); setc(ctx, (1, 1, 1)); ctx.fill()
        label(ctx, "\"WHOSE project IS this?!\"", 540, 320, 76, (1, 1, 1), -0.03, pop(il, 2, 6))
        label1(ctx, "*SNOOORE*", hx('c8e6ff'), pop(il, 20, 24), 110, y=1430)


def s3(ctx, f):
    lf = f - 250
    if lf < 50:
        # low angle: goggled Dad pours a huge vinegar bottle, Mom with the soda box
        ctx.save(); cam(ctx, 540, 1040, 1.05 + 0.06 * eout(pop(lf, 0, 50)), -3, 0, f)
        kitchen(ctx, hx('283a72'))
        ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, (0.05, 0.05, 0.2, 0.25)); ctx.fill()
        clock(ctx, 840, 520, 70, 2, 0)
        table(ctx, 180, 900, 1220)
        volcano(ctx, 540, 1220, 0.85, 1.0, 1.0, 0.3)
        pd = P(torso=-6, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=-140, lel=-20, rsh=-60, rel=-40, eye='smug', mouth='grin', head=0)
        bd = draw(ctx, 840, FLOOR - 186 * 1.35, 1.35, -1, DAD, pd)
        goggles(ctx, bd)
        # vinegar bottle tipping over the crater
        tip = eout(pop(lf, 6, 26))
        hxp, hyp = bd['front']; ctx.save(); ctx.translate(hxp, hyp); ctx.rotate(-0.4 - 1.2 * tip)
        rect_r(ctx, -45, -150, 90, 220, 26); fl(ctx, (0.9, 0.95, 1.0), 6)
        rect_r(ctx, -22, -200, 44, 60, 10); fl(ctx, RED, 5)
        rect_r(ctx, -40, -80, 80, 70, 8); fl(ctx, YEL, 4)
        ctx.restore()
        if tip > 0.8:
            ctx.move_to(hxp - 170, hyp - 40); ctx.curve_to(hxp - 190, hyp + 20, 560, 860, 545, 950); setc(ctx, (0.85, 0.95, 1, 0.9)); ctx.set_line_width(18); ctx.stroke()
        pm = P(torso=4, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=-60, lel=-80, rsh=30, rel=-20, eye='shock', mouth='flat', head=0)
        bm = draw(ctx, 210, FLOOR - 186 * 1.3, 1.3, 1, MOM, pm)
        sx_, sy_ = bm['front']; sy_ -= 130; sx_ += 40
        rect_r(ctx, sx_ - 60, sy_ - 40, 120, 150, 10); fl(ctx, (1, 1, 1), 6)
        text(ctx, "SODA", sx_, sy_ + 40, 36, BLUE, outline=(1,1,1,0), ow=1, shadow=False)
        ctx.restore()
        label2(ctx, "\"Just a", "LITTLE bit...\"", (1, 1, 1), pop(lf, 4, 8), 108, col2=YEL)
        card(ctx, 'p3', f, 252, 296)
    elif lf < 95:
        il = lf - 50
        # ERUPTION: pink foam column smashes the ceiling and fills the frame
        g = eout(pop(il, 0, 20))
        ctx.save(); cam(ctx, 540, 1040, 1.05 - 0.15 * g, 0, shake_at(il, [0, 8], 26, 30) + 6 * g, f)
        kitchen(ctx, hx('283a72'))
        table(ctx, 180, 900, 1220)
        volcano(ctx, 540, 1220, 0.85, 1.0, 1.0, 1.0)
        top = 960 - 1300 * g
        ctx.rectangle(470, top, 140, 980 - top); setc(ctx, FOAM); ctx.fill()
        for k in range(14):
            foam_blob(ctx, 540 + 30 * math.sin(k + il * 0.3), 960 - k * (1300 * g / 14), 260 + k * 14, 200, seed=k + il // 3, n=10)
        if il > 14:
            sp = eout(pop(il, 14, 44))
            for k in range(6):
                foam_blob(ctx, 540 + (k - 2.5) * 260 * sp, -200 + 400 * sp + 80 * (k % 2), 360, 300, seed=40 + k, n=12)
        ctx.restore()
        if il > 24:   # foam rolls over the whole lens
            v = eout(pop(il, 24, 40))
            rnd = random.Random(21)
            for k in range(16):
                x, y = rnd.uniform(-40, 1120), rnd.uniform(-40, 1960); r_ = rnd.uniform(160, 320) * v
                ellipse(ctx, x, y, r_, r_); setc(ctx, FOAM); ctx.fill()
                ellipse(ctx, x - r_ * 0.3, y - r_ * 0.3, r_ * 0.2, r_ * 0.14); setc(ctx, (1, 1, 1, 0.7)); ctx.fill()
        label1(ctx, "*FWOOOOSH!*", (1, 1, 1), pop(il, 1, 4), 150, 0.04, y=1360)
    else:
        il = lf - 95
        # aftermath: both parents dripping in foam, hair blown up, deadpan
        ctx.save(); cam(ctx, 540, 1000, 1.18 + 0.05 * eout(pop(il, 0, 55)), 0, 0, f)
        ctx.rectangle(-1000, -1000, 3200, 4000); setc(ctx, hx('ffd0e6')); ctx.fill()
        rnd = random.Random(3)
        for k in range(30):
            ellipse(ctx, rnd.uniform(0, 1080), rnd.uniform(300, 1700), rnd.uniform(40, 120), rnd.uniform(40, 90)); setc(ctx, FOAM); ctx.fill()
        ctx.rectangle(-1000, FLOOR, 3200, 1000); setc(ctx, FOAM); ctx.fill()
        pm = P(torso=0, lhip=-6, lkn=0, rhip=6, rkn=0, lsh=12, lel=-10, rsh=-12, rel=-10, eye='normal', mouth='flat', head=0)
        bm = draw(ctx, 360, FLOOR - 186 * 1.3, 1.3, 1, MOM, pm)
        pd = P(torso=0, lhip=-6, lkn=0, rhip=6, rkn=0, lsh=12, lel=-10, rsh=-60, rel=-130, eye='normal', mouth='flat', head=0)
        bd = draw(ctx, 720, FLOOR - 186 * 1.35, 1.35, -1, DAD, pd)
        goggles(ctx, bd, col=FOAM)
        for b, sd in ((bm, 1), (bd, 2)):
            foam_blob(ctx, b['head'][0], b['head'][1] - b['R'] * 1.0, b['R'] * 1.6, b['R'] * 0.9, seed=sd, n=10)
            for k in range(3):   # drips
                d = (il * 3 + k * 40) % 140
                ellipse(ctx, b['head'][0] + (k - 1) * b['R'] * 0.6, b['head'][1] + b['R'] * 0.3 + d, 14, 20); setc(ctx, FOAM); ctx.fill()
        foam_blob(ctx, 540, FLOOR - 40, 1100, 160, seed=9, n=20)
        ctx.restore()
        label1(ctx, "*drip... drip...*", FOAM, pop(il, 0, 4), 90, y=1250) if il < 22 else None
        if il >= 22:
            label2(ctx, "\"...okay.", "It WORKS.\"", (1, 1, 1), pop(il, 22, 26), 112, col2=PINK)


def s4(ctx, f):
    lf = f - 400
    if lf < 50:
        # science fair: proud kid, polished volcano, blue ribbon
        ctx.save(); cam(ctx, 540, 1060, 1.05 + 0.04 * eout(pop(lf, 0, 50)), 0, shake_at(lf, [14], 6, 10), f)
        ctx.rectangle(-1000, -1000, 3200, 4000); setc(ctx, hx('9fe8a8')); ctx.fill()
        rays(ctx, 540, 900, 200, 1600, lf * 0.03, col=(1, 1, 1), a=0.3, n=18)
        for k in range(9):   # bunting
            x = 60 + k * 120
            poly(ctx, [(x, 420), (x + 110, 420), (x + 55, 500)]); fl(ctx, (RED, YEL, BLUE)[k % 3], 5)
        ctx.move_to(0, 420); ctx.line_to(1080, 420); ink(ctx, 6); ctx.stroke()
        table(ctx, 360, 1020, 1200)
        ctx.rectangle(360, 1246, 660, 120); fl(ctx, (1, 1, 1), 6)
        volcano(ctx, 720, 1200, 0.8, 1.0, 1.0, 1.0)
        pk = P(torso=0, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=-160, lel=-10, rsh=-30, rel=-20, eye='happy', mouth='grin', head=-4)
        bk = draw(ctx, 240, FLOOR - 186 * 1.05, 1.05, 1, BOY, pk)
        if lf >= 14:
            ribbon(ctx, bk['head'][0] + 10, bk['head'][1] + bk['R'] * 1.5, 0.8 * eout(pop(lf, 14, 20)) + 0.01, 0.1)
            for k in range(4):
                a = lf * 0.15 + k * math.pi / 2
                sparkle(ctx, 240 + math.cos(a) * 190, 800 + math.sin(a) * 150, 24 + 8 * math.sin(lf * 0.5 + k))
        ctx.restore()
        label2(ctx, "\"I did it ALL", "by MYSELF!\"", (1, 1, 1), pop(lf, 3, 7), 108, col2=YEL)
        card(ctx, 'p4', f, 402, 446)
    else:
        il = lf - 50
        # whip-pan to the back row: zombie parents with coffee
        pan = eout(pop(il, 0, 10))
        ctx.save(); cam(ctx, 540, 1000, 1.0, 0, 0, f, sx=W / 2 + (1 - pan) * 900)
        ctx.rectangle(-1000, -1000, 3200, 4000); setc(ctx, hx('9b8ad8')); ctx.fill()
        ctx.rectangle(-1000, FLOOR, 3200, 1000); setc(ctx, hx('6a5aa8')); ctx.fill()
        row = ((210, NMOM, 1.0, hx('19b5a5')), (420, DAD, 1.08, hx('ff8a1f')), (640, MOM, 1.04, hx('ff5fa8')), (860, NEIGH, 1.06, hx('1f8bff')))
        for k, (x, ch, s, mc) in enumerate(row):
            sway = 3 * math.sin(il * 0.12 + k)
            p = P(torso=sway, lhip=-6, lkn=0, rhip=6, rkn=0, lsh=-40, lel=-110, rsh=12, rel=-10, eye='normal', mouth='flat', head=-sway * 2)
            b = draw(ctx, x, FLOOR - 186 * s, s, 1 if k % 2 == 0 else -1, ch, p)
            droop(ctx, b, ch, 0.55 + 0.1 * math.sin(il * 0.1 + k))
            eyebags(ctx, b)
            mug(ctx, b['head'][0] + (60 if k % 2 == 0 else -60), b['head'][1] + b['R'] * 1.6, 0.6, 0, mc, True, il)
        # glue and glitter on them
        rnd = random.Random(4)
        for k in range(18):
            sparkle(ctx, rnd.uniform(60, 1020), rnd.uniform(800, 1300), 10, (1, 0.9, 0.3))
        ctx.restore()
        label2(ctx, "\"...SO", "did WE.\"", (1, 1, 1), pop(il, 8, 12), 116, col2=PURPLE)


def s5(ctx, f):
    lf = f - 500
    if lf < 55:
        # home: parents collapsed on the sofa, kid in the doorway with ANOTHER note
        ctx.save(); cam(ctx, 540, 1080, 1.05 + 0.04 * eout(pop(lf, 0, 55)), 0, 0, f)
        ctx.rectangle(-1000, -1000, 3200, 4000); setc(ctx, hx('6fd6c8')); ctx.fill()
        for i in range(-10, 20):
            ctx.rectangle(i * 120, -1000, 46, 4000); setc(ctx, dark(hx('6fd6c8'), 0.94)); ctx.fill()
        ctx.rectangle(-1000, FLOOR, 3200, 1000); setc(ctx, hx('c98a52')); ctx.fill()
        ctx.move_to(-1000, FLOOR); ctx.line_to(2000, FLOOR); ink(ctx, 8); ctx.stroke()
        rect_r(ctx, 60, 1000, 640, 300, 40); fl(ctx, hx('ff5a7a'), 8)
        bm = draw_hip(ctx, 220, 1260, 1.05, 1, MOM, P(torso=-20, lhip=-80, lkn=80, rhip=-75, rkn=85, lsh=30, lel=-10, rsh=-30, rel=-10, eye='closed', mouth='open', head=-20))
        bd = draw_hip(ctx, 520, 1260, 1.1, -1, DAD, P(torso=-22, lhip=-80, lkn=80, rhip=-75, rkn=85, lsh=30, lel=-10, rsh=-30, rel=-10, eye='closed', mouth='open', head=18))
        rect_r(ctx, 60, 1260, 640, 160, 30); fl(ctx, hx('ff5a7a'), 8)
        for x in (20, 640):
            rect_r(ctx, x, 1120, 100, 330, 40); fl(ctx, hx('e84468'), 8)
        zzz(ctx, 300, 900, lf, 0.8)
        pk = P(torso=0, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=-150, lel=-20, rsh=12, rel=-15, eye='happy', mouth='grin', head=4)
        draw(ctx, 880, FLOOR - 186 * 1.0, 1.0, -1, BOY, pk)
        note(ctx, 780, 880, 0.55, 0.12, ("HOMEWORK:", "BUILD THE", "SOLAR SYSTEM!", "DUE..."))
        ctx.restore()
        label2(ctx, "\"Oh! And I need", "a SOLAR SYSTEM...\"", (1, 1, 1), pop(lf, 3, 7), 90, col2=YEL)
        card(ctx, 'p5', f, 502, 548)
    elif lf < 95:
        il = lf - 55
        # Mom ECU, one eye twitching, push in
        ctx.save(); cam(ctx, 540, 900, 1.1 + 0.2 * eout(pop(il, 0, 40)), 0, 5 if (il // 3) % 2 else 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('3a2a6a')); ctx.fill()
        rays(ctx, 540, 860, 200, 1500, il * 0.05, col=(1, 0.4, 0.5), a=0.3, n=16)
        face(ctx, MOM, P(eye='shock', mouth='flat', head=0), 540, 860, 270, 0.0)
        lids(ctx, MOM, 540, 860, 270, 0.35 + (0.3 if (il // 4) % 2 else 0))
        bloodshot(ctx, 540, 860, 270, 1, 4)
        for k in range(5):   # orbiting planets of doom
            a = il * 0.12 + k * 1.25
            planet(ctx, 540 + math.cos(a) * 400, 860 + math.sin(a) * 300, 34 + k * 6, (RED, BLUE, ORANGE, GREEN, YEL)[k], k == 3)
        ctx.restore()
        if il < 20:
            label1(ctx, "\"...due WHEN?\"", (1, 1, 1), pop(il, 2, 6), 116)
        else:
            label1(ctx, "\"TOMORROW!\"", YEL, pop(il, 20, 23), 140, 0.04)
    elif lf < 135:
        il = lf - 95
        # wide: both parents TIMBER backwards onto the floor
        fall = ein(pop(il, 4, 22))
        ctx.save(); cam(ctx, 540, 1150, 0.8, 0, shake_at(il, [22], 18, 26), f)
        ctx.rectangle(-1000, -1000, 3200, 4000); setc(ctx, hx('6fd6c8')); ctx.fill()
        ctx.rectangle(-1000, FLOOR, 3200, 1000); setc(ctx, hx('c98a52')); ctx.fill()
        ctx.move_to(-1000, FLOOR); ctx.line_to(2000, FLOOR); ink(ctx, 8); ctx.stroke()
        for x, ch, s, dirn in ((540, MOM, 1.25, -1), (800, DAD, 1.3, -1)):
            ctx.save(); ctx.translate(x, FLOOR); ctx.rotate(dirn * fall * math.pi / 2 * 0.95); ctx.translate(-x, -FLOOR)
            draw(ctx, x, FLOOR - 186 * s, s, 1, ch, P(torso=0, lhip=-4, lkn=0, rhip=4, rkn=0, lsh=8, lel=0, rsh=-8, rel=0, eye='shock' if fall < 1 else 'closed', mouth='open', head=0))
            ctx.restore()
        if il >= 22:
            puff(ctx, 400, FLOOR - 20, pop(il, 22, 36), 1.6)
        ctx.restore()
        if il < 22:
            label1(ctx, "*TIMBERRR...*", YEL, pop(il, 3, 6), 120)
        else:
            label1(ctx, "*THUD!*", (1, 1, 1), pop(il, 22, 25), 150, -0.04)
    else:
        il = lf - 135
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 635)


SHOTS = [(0, s1), (110, s2), (250, s3), (400, s4), (500, s5)]
CUTS = (56, 110, 185, 250, 300, 345, 400, 450, 500, 555, 595, 635)


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
                              "-i", "out/due_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
