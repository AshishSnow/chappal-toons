"""'The Jar That Won't Open' - original, general-audience comedy short, 22s.
Hook: ECU Dad, beetroot-red, gritted teeth, veins popping, strangling a pickle jar: "I ALMOST... HAVE IT...!"
Flashback: Mom hands him the jar, Dad cracks his knuckles: "Stand back."
Beat 1: the towel trick - SQUEAK SQUEAK - towel flies off and lands on his head: "It's... WARMED UP now."
Beat 2: hot water - steam, then he juggles the scalding jar: "HOT! HOT! HOT!"
Beat 3: full power - he twists so hard HE spins like a top; dizzy: "The jar is... DEFECTIVE."
 Split: Mom + kid with popcorn: "Better than TV."
Climax: hour 2, safety goggles + giant wrench -> POP! lid rockets off, pickle juice SPLAT on the lens.
Twist: "NAILED IT!" - lid falls on his head *CLANG* - Mom: "Great! Now... THIS one." a GIANT family-size jar slides in.
 Eye twitch -> opening strain face (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos, zigs, popcorn
from scenes48 import label1, label2
import scenes13
from scenes13 import card as _card13
import random

BOY = dict(doodle.BOY, hood=False)
DAD = doodle.DAD
MOM = doodle.MOM_G
STRAIN = dict(DAD, skin=hx('f2735a'))
WARM = dict(DAD, skin=hx('ea9373'))
N = 660
FLOOR = 1460
CT = 1100
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
PICK = hx('5fae3a')
BRINE = hx('dcef9a')
JUICE = hx('9bd13a')
LY = 1400

CAPS = {
    'p1': [[("WHEN MOM SAYS", OUT)], [("\"CAN YOU OPEN THIS?\"", RED)]],
    'p2': [[("ATTEMPT #1:", OUT)], [("THE TOWEL", BLUE)]],
    'p2b': [[("ATTEMPT #2:", OUT)], [("HOT WATER", ORANGE)]],
    'p3': [[("ATTEMPT #3:", OUT)], [("FULL POWER", RED)]],
    'p4': [[("HOUR 2...", PURPLE)]],
    'p5': [[("PLOT TWIST:", OUT)], [("FAMILY SIZE", GREEN)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def lid(ctx, x, y, s=1.0, a=0.0):
    """lid centred at x,y"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -92, -27, 184, 54, 12); fl(ctx, RED, 7)
    for k in range(-4, 5):
        ctx.move_to(k * 19, -18); ctx.line_to(k * 19, 18)
    setc(ctx, dark(RED, 0.75)); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def jar(ctx, x, y, s=1.0, a=0.0, has_lid=True, empty=0.0):
    """pickle jar, bottom centre at x,y; total height 320*s"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -80, -290, 160, 40, 10); fl(ctx, hx('eafaf0'), 6)          # neck
    rect_r(ctx, -105, -262, 210, 262, 44)
    body = ctx.copy_path()
    setc(ctx, BRINE); ctx.fill()
    ctx.save(); ctx.new_path(); ctx.append_path(body); ctx.clip()
    top = -250 + 200 * empty
    ctx.rectangle(-120, -300, 240, top + 300); setc(ctx, hx('eefbe8')); ctx.fill()
    rnd = random.Random(3)
    for k in range(7):
        px, py = rnd.uniform(-70, 70), rnd.uniform(-220, -40)
        if py < top + 20:
            continue
        ellipse(ctx, px, py, 26, 70, rnd.uniform(-0.5, 0.5)); fl(ctx, PICK, 5)
        for j in range(3):
            ellipse(ctx, px + rnd.uniform(-10, 10), py + rnd.uniform(-40, 40), 4, 4); setc(ctx, dark(PICK, 0.7)); ctx.fill()
    ctx.rectangle(-110, -160, 220, 64); fl(ctx, (1, 1, 1), 5)
    ctx.restore()
    text(ctx, "PICKLES", 0, -128, 38, GREEN, outline=(1, 1, 1), ow=2, shadow=False)
    ctx.new_path(); ctx.append_path(body); ink(ctx, 8); ctx.stroke()
    ctx.move_to(-78, -230); ctx.line_to(-78, -60); setc(ctx, (1, 1, 1, 0.75)); ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.restore()
    if has_lid:
        ca, sa = math.cos(a), math.sin(a)
        lid(ctx, x + 300 * s * sa, y - 300 * s * ca, s, a)


def fist(ctx, x, y, s=1.0, col=DAD['skin'], a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -62, -48, 124, 96, 40); fl(ctx, col, 7)
    for k in (-1, 0, 1):
        ctx.move_to(k * 30, -44); ctx.line_to(k * 30, -16)
    ink(ctx, 5); ctx.stroke()
    ctx.restore()


def towel(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(-130, -40); ctx.curve_to(-60, -80, 60, -80, 130, -40); ctx.line_to(150, 60); ctx.curve_to(60, 30, -60, 30, -150, 60); ctx.close_path()
    fl(ctx, hx('3fb6ff'), 7)
    for k in (-1, 1):
        ctx.move_to(k * 50, -60); ctx.line_to(k * 60, 40)
    setc(ctx, (1, 1, 1)); ctx.set_line_width(12); ctx.stroke()
    ctx.restore()


def wrench(ctx, x0, y0, x1, y1, w=40):
    """big wrench from handle end (x0,y0) to jaw (x1,y1)"""
    a = math.atan2(y1 - y0, x1 - x0); L = math.hypot(x1 - x0, y1 - y0)
    ctx.save(); ctx.translate(x0, y0); ctx.rotate(a)
    rect_r(ctx, 0, -w / 2, L, w, w / 2); fl(ctx, hx('9aa4b8'), 7)
    ctx.move_to(L - 20, -w * 2.2); ctx.line_to(L + w * 1.6, -w * 2.2); ctx.line_to(L + w * 1.6, -w * 0.8); ctx.line_to(L + w * 0.4, -w * 0.8)
    ctx.line_to(L + w * 0.4, w * 0.8); ctx.line_to(L + w * 1.6, w * 0.8); ctx.line_to(L + w * 1.6, w * 2.2); ctx.line_to(L - 20, w * 2.2); ctx.close_path()
    fl(ctx, hx('7a8498'), 7)
    ctx.restore()


def goggles(ctx, ex1, ey1, ex2, ey2, r):
    ctx.move_to(ex1 - r * 1.6, ey1); ctx.line_to(ex2 + r * 1.6, ey2); setc(ctx, OUT); ctx.set_line_width(r * 0.5); ctx.stroke()
    for ex, ey in ((ex1, ey1), (ex2, ey2)):
        ellipse(ctx, ex, ey, r, r); setc(ctx, (0.7, 0.95, 1, 0.55)); ctx.fill_preserve(); setc(ctx, hx('ffcf3d')); ctx.set_line_width(r * 0.3); ctx.stroke_preserve()
        ink(ctx, r * 0.08); ctx.stroke()
        ctx.move_to(ex - r * 0.5, ey - r * 0.2); ctx.line_to(ex - r * 0.2, ey - r * 0.5); setc(ctx, (1, 1, 1)); ctx.set_line_width(r * 0.12); ctx.stroke()


def spiral(ctx, x, y, r, t):
    ellipse(ctx, x, y, r, r); fl(ctx, (1, 1, 1), r * 0.12)
    ctx.new_path()
    for i in range(60):
        u = i / 59; a = t + u * 6 * math.pi; rr = r * 0.9 * u
        (ctx.move_to if i == 0 else ctx.line_to)(x + math.cos(a) * rr, y + math.sin(a) * rr)
    ink(ctx, r * 0.1); ctx.stroke()


def vein(ctx, x, y, s=1.0, col=hx('c4162e')):
    """cartoon popping-vein mark"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for a in (0, math.pi / 2, math.pi, 3 * math.pi / 2):
        ctx.save(); ctx.rotate(a)
        ctx.move_to(10, -10); ctx.curve_to(16, -30, 34, -34, 40, -14)
        ctx.restore()
    setc(ctx, col); ctx.set_line_width(11); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.restore()


def sweat(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, -30); ctx.curve_to(18, 0, 18, 22, 0, 22); ctx.curve_to(-18, 22, -18, 0, 0, -30); ctx.close_path()
    fl(ctx, hx('8fd8ff'), 4); ctx.restore()


def steam(ctx, x, y, lf, s=1.0, n=3):
    for k in range(n):
        t = ((lf + k * 9) % 27) / 27
        ellipse(ctx, x + 30 * math.sin(lf * 0.2 + k) * s, y - 160 * t * s, (30 + 50 * t) * s, (26 + 40 * t) * s)
        setc(ctx, (1, 1, 1, 0.75 * (1 - t))); ctx.fill()


def splats(ctx, x, y, s=1.0, seed=1, col=JUICE):
    rnd = random.Random(seed)
    for k in range(5):
        ellipse(ctx, x + rnd.uniform(-40, 40) * s, y + rnd.uniform(-30, 30) * s, rnd.uniform(14, 30) * s, rnd.uniform(12, 24) * s); setc(ctx, col); ctx.fill()


def kitchen(ctx, wall=hx('7fd3c8')):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, wall); ctx.fill()
    for i in range(-30, 40):           # backsplash tiles
        ctx.rectangle(i * 90, 760, 4, CT - 760); setc(ctx, light(wall, 0.25)); ctx.fill()
    for j in range(5):
        ctx.rectangle(-3000, 760 + j * 85, 7000, 4); setc(ctx, light(wall, 0.25)); ctx.fill()
    for x in range(-900, 2000, 320):   # upper cabinets
        rect_r(ctx, x + 12, 330, 296, 360, 14); fl(ctx, hx('fff3d6'), 6)
        ellipse(ctx, x + 160 + (60 if (x // 320) % 2 else -60), 640, 12, 12); fl(ctx, hx('ffcf3d'), 4)
    ctx.rectangle(-3000, CT + 40, 7000, FLOOR - CT); setc(ctx, hx('ffb26b')); ctx.fill()
    for x in range(-900, 2000, 260):
        rect_r(ctx, x + 14, CT + 66, 232, FLOOR - CT - 110, 10); fl(ctx, hx('ffc48a'), 5)
    ctx.rectangle(-3000, CT, 7000, 44); fl(ctx, hx('8e9aaf'), 7)
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('f5f1e6')); ctx.fill()
    for i in range(-30, 40):
        for j in range(8):
            if (i + j) % 2:
                poly(ctx, [(i * 140 - j * 70, FLOOR + j * 70), (i * 140 + 140 - j * 70, FLOOR + j * 70), (i * 140 + 70 - (j + 1) * 70 + 70, FLOOR + (j + 1) * 70), (i * 140 - (j + 1) * 70, FLOOR + (j + 1) * 70)])
                setc(ctx, hx('ff8fa8')); ctx.fill()
    ctx.rectangle(-3000, FLOOR - 6, 7000, 12); setc(ctx, OUT); ctx.fill()


def strain_jar(ctx, cx, top, lf, s=1.0, jx=540):
    """jar gripped by two fists, lid hand twisting"""
    tw = 0.06 * math.sin(lf * 1.9)
    jar(ctx, jx, top + 320 * s, s, tw * 0.3)
    fist(ctx, jx - 120 * s, top + 220 * s, 0.95 * s, STRAIN['skin'], 0.3)
    fist(ctx, jx + 60 * s, top + 20 * s, 0.95 * s, STRAIN['skin'], -0.2 + tw * 3)


# ------------------------------------------------------------------ opening
def opening_face(ctx, f, lf, lab=True):
    """ECU: Dad, red, gritted teeth, veins popping, strangling the jar"""
    sh = shake_at(lf, [0], 12, 20) + 6
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eout(pop(lf, 0, 40)), 0, sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff5a3c')); ctx.fill()
    rays(ctx, 540, 820, 260, 1700, lf * 0.05, col=(1, 0.85, 0.35), a=0.4, n=18)
    cx, cy, R = 540 + 5 * math.sin(lf * 2.3), 790, 290
    face(ctx, STRAIN, P(eye='closed', mouth='grin', head=0), cx, cy, R, 0.02 * math.sin(lf * 1.7))
    vein(ctx, cx + 170, cy - 190, 1.3 + 0.15 * math.sin(lf * 0.9)); vein(ctx, cx - 190, cy - 150, 1.0 + 0.15 * math.cos(lf * 0.9))
    sweat(ctx, cx - 300, cy - 30 + (lf * 4) % 70, 1.4); sweat(ctx, cx + 300, cy + 10 + (lf * 5) % 60, 1.2)
    steam(ctx, cx - 320, cy - 60, lf, 1.0); steam(ctx, cx + 320, cy - 60, lf + 13, 1.0)
    strain_jar(ctx, cx, 1010, lf, 1.0)
    ctx.restore()
    if lab:
        label2(ctx, "\"I ALMOST...", "HAVE IT...!\"", (1, 1, 1), 1.0 if f < 60 else pop(lf, 0, 3), 108, col2=YEL)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 60:
        opening_face(ctx, f, f)
    else:
        lf = f - 60
        # wide kitchen: Mom hands over the jar, Dad cracks his knuckles
        ctx.save(); cam(ctx, 540, 1130, 1.12 + 0.05 * eout(pop(lf, 0, 50)), 0, shake_at(lf, [26], 6, 10), f)
        kitchen(ctx)
        pm = P(torso=4, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=-20, lel=-20, rsh=80, rel=-10, eye='normal', mouth='smile', head=-4)
        bm = draw(ctx, 280, FLOOR - 186 * 1.3, 1.3, 1, MOM, pm)
        jar(ctx, bm['front'][0] + 50, bm['front'][1] + 50, 0.42)
        flex = lf >= 24
        pd = P(torso=-6 if flex else 0, lhip=-10, lkn=0, rhip=10, rkn=0,
               lsh=70 if flex else 30, lel=-120 if flex else -20, rsh=70 if flex else 20, rel=-120 if flex else -20,
               eye='smug' if flex else 'normal', mouth='grin' if flex else 'smile', head=-8)
        bd = draw(ctx, 790, FLOOR - 186 * 1.32, 1.32, -1, DAD, pd)
        if flex:
            hx_, hy_ = bd['front']
            sparkle(ctx, hx_ - 40, hy_ - 60, 30 + 10 * math.sin(lf * 0.6)); sparkle(ctx, hx_ + 60, hy_ + 10, 20)
        ctx.restore()
        if lf < 24:
            label2(ctx, "\"Honey, can you", "open this?\"", (1, 1, 1), pop(lf, 2, 6), 100, col2=PINK)
        else:
            if lf < 40:
                label(ctx, "*CRACK!*", 800, 1010, 96, YEL, 0.1, pop(lf, 26, 29))
            label2(ctx, "\"Stand back,", "honey.\"", (1, 1, 1), pop(lf, 28, 32), 108, col2=YEL)
    card(ctx, 'p1', f, -6, 110)


def s2(ctx, f):
    lf = f - 110
    if lf < 60:
        # the towel trick
        sq = [6, 16, 26, 34]
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eout(pop(lf, 0, 60)), 0, shake_at(lf, sq, 5, 9), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('5fc8ff')); ctx.fill()
        rays(ctx, 540, 760, 220, 1600, lf * 0.03, col=(1, 1, 1), a=0.22, n=16)
        face(ctx, WARM, P(eye='closed' if lf < 38 else 'normal', mouth='grin' if lf < 38 else 'flat', head=0), 540, 800, 230, 0.0)
        if lf < 38:
            vein(ctx, 690, 640, 1.0)
        tw = 0.25 * math.sin(lf * 0.9) if lf < 38 else 0
        jar(ctx, 540, 1350, 1.0, 0, has_lid=lf < 38)
        if lf < 38:
            towel(ctx, 540, 1060, 1.0, tw)
            fist(ctx, 420, 1260, 0.95, WARM['skin'], 0.3)
            fist(ctx, 610, 1050, 0.95, WARM['skin'], -0.2 + tw)
        else:
            lid(ctx, 540, 1050, 1.0)
            u = eout(pop(lf, 38, 46))
            if u < 1:
                towel(ctx, 540, lerp(1060, 300, u) + 260 * u * u, 1.0, u * 8)
            else:
                # towel draped over his head
                ctx.save(); ctx.translate(540, 610)
                ctx.move_to(-250, 40); ctx.curve_to(-240, -170, 240, -170, 250, 40); ctx.line_to(270, 160); ctx.curve_to(150, 120, 80, 40, 0, 30)
                ctx.curve_to(-80, 40, -150, 120, -270, 160); ctx.close_path(); fl(ctx, hx('3fb6ff'), 8)
                for k in (-1, 1):
                    ctx.move_to(k * 110, -110); ctx.line_to(k * 150, 110)
                setc(ctx, (1, 1, 1)); ctx.set_line_width(14); ctx.stroke()
                ctx.restore()
        ctx.restore()
        ph = min((lf - h for h in sq if lf >= h), default=99)
        if lf < 38 and ph < 8:
            n_ = sum(1 for h in sq if lf >= h)
            label(ctx, "*SQUEAK!*", 280 if n_ % 2 else 800, 1000, 84, YEL, -0.1 if n_ % 2 else 0.1, pop(ph, 0, 3))
        if lf >= 46:
            label2(ctx, "\"See? It's", "WARMED UP now.\"", (1, 1, 1), pop(lf, 46, 50), 100, col2=YEL)
        card(ctx, 'p2', f, 112, 170)
    else:
        il = lf - 60
        if il < 36:
            # sink: hot water + steam
            ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eout(pop(il, 0, 36)), 0, 0, f)
            ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('d6f0ff')); ctx.fill()
            for i in range(-5, 15):
                ctx.rectangle(i * 120, -500, 5, 3000); setc(ctx, hx('b8e0f5')); ctx.fill()
                ctx.rectangle(-500, i * 120, 2200, 5); setc(ctx, hx('b8e0f5')); ctx.fill()
            # faucet
            rect_r(ctx, 600, 470, 80, 260, 30); fl(ctx, hx('c8ccd8'), 7)
            ctx.move_to(640, 520); ctx.curve_to(640, 420, 480, 420, 480, 540); ctx.line_to(480, 620)
            setc(ctx, OUT); ctx.set_line_width(80); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke_preserve(); setc(ctx, hx('c8ccd8')); ctx.set_line_width(64); ctx.stroke()
            rect_r(ctx, 660, 420, 90, 40, 14); fl(ctx, RED, 6)
            # water stream onto the lid
            ctx.new_path(); ctx.rectangle(458 + 3 * math.sin(il), 640, 44, 330); setc(ctx, hx('6fc8ff')); ctx.fill()
            for k in range(4):
                yy = 640 + ((il * 30 + k * 80) % 330)
                ctx.rectangle(470, yy, 8, 40); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()
            jar(ctx, 500, 1360, 1.15, 0.05)
            fist(ctx, 360, 1260, 1.0, WARM['skin'], 0.3)
            # sink basin
            rect_r(ctx, 40, 1400, 1000, 200, 40); fl(ctx, hx('9aa4b8'), 8)
            steam(ctx, 380, 980, il, 1.4, 4); steam(ctx, 640, 1000, il + 11, 1.6, 4)
            ctx.restore()
            if il >= 8:
                label1(ctx, "*HISSSSS...*", (1, 1, 1), pop(il, 8, 12), 100, y=1440)
        else:
            jl = il - 36
            # ECU: HOT HOT HOT - juggling the jar
            ctx.save(); cam(ctx, 540, 960, 1.0, 0, 10 + shake_at(jl, [0], 8, 12), f)
            ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8a1f')); ctx.fill()
            rays(ctx, 540, 760, 220, 1600, -jl * 0.06, col=(1, 0.95, 0.5), a=0.35, n=16)
            face(ctx, STRAIN, P(eye='shock', mouth='scream', head=0), 540, 740, 250, 0.05 * math.sin(jl * 0.8))
            steam(ctx, 250, 720, jl, 1.2); steam(ctx, 830, 720, jl + 9, 1.2)
            ph = jl * 0.45
            jx = 540 + 270 * math.sin(ph); jy = 1130 - 210 * abs(math.cos(ph))
            jar(ctx, jx, jy + 160, 0.7, ph * 1.5)
            for k in (-1, 1):
                ux = 540 + k * 300; uy = 1220 - (40 if (math.sin(ph) * k) > 0.7 else 0)
                ctx.save(); ctx.translate(ux, uy)
                rect_r(ctx, -70, -50, 140, 90, 40); fl(ctx, STRAIN['skin'], 7)
                for j in range(4):
                    rect_r(ctx, -60 + j * 32, -100, 26, 60, 12); fl(ctx, STRAIN['skin'], 5)
                ctx.restore()
            ctx.restore()
            label2(ctx, "\"HOT! HOT!", "HOT! HOT!\"", (1, 1, 1), pop(jl, 0, 4), 116, col2=YEL)
        card(ctx, 'p2b', f, 172, 250)


def s3(ctx, f):
    lf = f - 250
    if lf < 90:
        spin = 10 <= lf < 46
        ang = 0.0
        if lf >= 10:
            t = min(lf, 46) - 10
            ang = 0.02 * t * t
        dizzy = lf >= 46
        rot = 5 * math.sin(lf * 0.35) if spin else 0
        ctx.save(); cam(ctx, 540, 1110, 1.12, rot, 6 if spin else 0, f)
        kitchen(ctx, hx('ffd166'))
        if spin:
            for k in range(4):   # whirl lines
                a0 = ang * 2 + k * math.pi / 2
                ctx.new_path(); ctx.arc(540, 1150 - k * 60, 260 + k * 20, a0, a0 + 1.6)
                setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        sx = math.cos(ang)
        sx = math.copysign(max(0.08, abs(sx)), sx)
        sway = 10 * math.sin((lf - 46) * 0.3) if dizzy else 0
        ctx.save(); ctx.translate(540, 0); ctx.scale(sx, 1); ctx.translate(-540, 0)
        p = P(torso=sway, rot=sway * 0.6, lhip=-12, lkn=0, rhip=12, rkn=0, lsh=80, lel=-60, rsh=90, rel=-40,
              eye='closed' if not dizzy else 'shock', mouth='grin' if not dizzy else 'wavy', head=-sway)
        b = draw(ctx, 540, FLOOR - 186 * 1.4, 1.4, 1, DAD, p)
        jar(ctx, b['front'][0] + 10, b['front'][1] + 70, 0.5)
        if dizzy:
            for e in ('eyeL', 'eyeR'):
                ex, ey = b[e]
                spiral(ctx, ex, ey - b['R'] * 0.06, b['R'] * 0.17, lf * 0.5)
        ctx.restore()
        if dizzy:
            hx_, hy_ = b['head']
            for k in range(5):
                a = lf * 0.2 + k * 2 * math.pi / 5
                sparkle(ctx, hx_ + math.cos(a) * 170, hy_ - 200 + math.sin(a) * 40, 26)
        ctx.restore()
        if lf < 10:
            label1(ctx, "\"FULL... POWER!\"", (1, 1, 1), pop(lf, 0, 4), 110)
        elif spin:
            label1(ctx, "*WHIRRRRR!*", YEL, pop(lf, 10, 13), 116)
        else:
            label2(ctx, "\"The jar is...", "DEFECTIVE.\"", (1, 1, 1), pop(lf, 50, 54), 104, col2=YEL)
        card(ctx, 'p3', f, 252, 340)
    else:
        il = lf - 90
        # split: Mom + kid with popcorn (top) vs puffing Dad (bottom)
        ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
        ctx.rectangle(0, 0, W, 960); setc(ctx, hx('9ff0b0')); ctx.fill()
        rays(ctx, 540, 700, 150, 1300, il * 0.03, col=(1, 1, 1), a=0.3, n=16)
        face(ctx, MOM, P(eye='happy', mouth='grin', head=0), 320, 660, 150, -0.05)
        face(ctx, BOY, P(eye='happy', mouth='open' if (il // 6) % 2 else 'grin', head=0), 760, 680, 135, 0.05)
        popcorn(ctx, 540, 900, 0.9)
        ctx.restore()
        ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
        ctx.rectangle(0, 960, W, 960); setc(ctx, hx('ff8a5c')); ctx.fill()
        face(ctx, STRAIN, P(eye='glare', mouth='flat', head=0), 540, 1200, 180, 0.0)
        steam(ctx, 300, 1180, il, 1.0); steam(ctx, 780, 1180, il + 9, 1.0)
        sweat(ctx, 330, 1100 + (il * 3) % 40, 1.0)
        ctx.restore()
        ctx.rectangle(0, 952, W, 16); setc(ctx, (1, 1, 1)); ctx.fill()
        label(ctx, "\"Better than TV!\"", 540, 400, 96, (1, 1, 1), -0.03, pop(il, 2, 6))
        if il >= 20:
            label2(ctx, "\"I'm just...", "WARMING UP.\"", (1, 1, 1), pop(il, 20, 24), 96, col2=YEL, y=1440)


def s4(ctx, f):
    lf = f - 400
    if lf < 50:
        # hour 2: goggles + giant wrench, low angle
        tug = 0.5 + 0.5 * math.sin(lf * 0.7)
        ctx.save(); cam(ctx, 560, 1080, 1.1 + 0.05 * eout(pop(lf, 0, 50)), -4, 3, f)
        kitchen(ctx, hx('b9a8ff'))
        jar(ctx, 840, CT + 10, 0.8)
        p = P(torso=-16 - 6 * tug, lhip=-24, lkn=10, rhip=24, rkn=0, lsh=60, lel=-10, rsh=70, rel=-20, eye='closed', mouth='grin', head=8)
        b = draw(ctx, 330, FLOOR - 186 * 1.45, 1.45, 1, STRAIN, p)
        hx_, hy_ = b['front']
        wrench(ctx, hx_ - 20, hy_ + 10, 840 - 120, CT + 10 - 300 * 0.8 + 6 + 20 * tug, 36)
        fist(ctx, hx_, hy_, 0.7, STRAIN['skin'])
        R = b['R']
        goggles(ctx, b['eyeL'][0], b['eyeL'][1] - R * 0.08, b['eyeR'][0], b['eyeR'][1] - R * 0.08, R * 0.22)
        vein(ctx, b['head'][0] - R * 0.5, b['head'][1] - R * 0.7, 0.7)
        sweat(ctx, b['head'][0] - R * 1.2, b['head'][1] + (lf * 4) % 40, 1.0)
        ctx.restore()
        label2(ctx, "\"ONE... MORE...", "...TRY!\"", (1, 1, 1), pop(lf, 2, 6), 108, col2=YEL)
        card(ctx, 'p4', f, 402, 450)
    elif lf < 70:
        il = lf - 50
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.12 * eout(pop(il, 0, 20)), 0, 6 + il * 1.2, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('e0263a')); ctx.fill()
        rays(ctx, 540, 860, 200, 1600, il * 0.1, col=(1, 0.85, 0.3), a=0.45, n=20)
        face(ctx, dict(STRAIN, skin=hx('ff4a3a')), P(eye='closed', mouth='grin', head=0), 540, 880, 300, 0.0)
        for (ex, ey, rx) in eye_pos(540, 880, 300):
            pass
        goggles(ctx, 540 - 0.2 * 300 - 30, 880 + 0.02 * 300, 540 + 0.42 * 300 - 30, 880 + 0.02 * 300, 300 * 0.24)
        vein(ctx, 720, 640, 1.4); vein(ctx, 340, 660, 1.1)
        zigs(ctx, 540, 860, 420, il, YEL, 7)
        ctx.restore()
        label1(ctx, "\"HNNNNNGH!!\"", YEL, pop(il, 0, 3), 130)
    else:
        il = lf - 70
        # POP! lid rockets, juice geyser, SPLAT on the lens
        ctx.save(); cam(ctx, 540, 1100, 1.0, 0, shake_at(il, [0], 16, 34), f)
        kitchen(ctx, hx('b9a8ff'))
        jar(ctx, 540, CT + 30 + 260, 1.3, 0, has_lid=False, empty=0.6 * eout(pop(il, 0, 10)))
        u = eout(pop(il, 0, 6))
        if il < 8:
            lid(ctx, 540 + 40 * u, lerp(CT - 130, -200, u), 1.3, u * 3)
            for k in range(5):
                ctx.move_to(500 + k * 20, CT - 140); ctx.line_to(500 + k * 20, CT - 140 - 400 * u)
            setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(8); ctx.stroke()
        rnd = random.Random(5)
        g = pop(il, 0, 16)
        for k in range(26):
            a = -math.pi / 2 + rnd.uniform(-0.9, 0.9); sp = rnd.uniform(600, 1300)
            px = 540 + math.cos(a) * sp * g; py = CT - 120 + math.sin(a) * sp * g + 900 * g * g
            r_ = rnd.uniform(18, 40) * (1 + g)
            if k % 4 == 0:
                ellipse(ctx, px, py, r_ * 0.6, r_ * 1.6, a); fl(ctx, PICK, 5)
            else:
                ellipse(ctx, px, py, r_, r_); fl(ctx, JUICE, 4)
        ctx.restore()
        if il >= 12:
            # juice splat on the lens
            v = max(0.03, eout(pop(il, 12, 16)))
            rnd = random.Random(8)
            for k in range(14):
                x, y = rnd.uniform(-50, 1130), rnd.uniform(200, 1700); r_ = rnd.uniform(90, 230) * v
                ellipse(ctx, x, y, r_, r_ * 0.9); setc(ctx, JUICE + (0.92,)); ctx.fill()
                d = (il - 16) * 9 * rnd.uniform(0.5, 1.2)
                if d > 0:
                    rect_r(ctx, x - 16, y, 32, r_ * 0.6 + d, 16); setc(ctx, JUICE + (0.92,)); ctx.fill()
            ellipse(ctx, 540, 960, 480 * v, 420 * v); setc(ctx, JUICE + (0.92,)); ctx.fill()
        if il < 12:
            label1(ctx, "*POP!!*", YEL, pop(il, 0, 3), 170, 0.05, y=600)
        else:
            label1(ctx, "*SPLOOSH!*", (1, 1, 1), pop(il, 12, 15), 140, -0.04)


def s5(ctx, f):
    lf = f - 500
    if lf < 50:
        # victory, everyone soaked; the lid falls back down on Dad
        ctx.save(); cam(ctx, 540, 1110, 1.12, 0, shake_at(lf, [34], 10, 18), f)
        kitchen(ctx, hx('ffd9a8'))
        for k, (x, y) in enumerate(((150, 520), (820, 430), (420, 820), (980, 900), (60, 1000))):
            splats(ctx, x, y, 1.6, k)
        pm = P(torso=0, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=10, lel=-10, rsh=10, rel=-10, eye='normal', mouth='flat', head=0)
        bm = draw(ctx, 180, FLOOR - 186 * 1.25, 1.25, 1, MOM, pm)
        pk = P(torso=0, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=10, lel=-10, rsh=10, rel=-10, eye='normal', mouth='flat', head=0)
        bk = draw(ctx, 900, FLOOR - 186 * 1.0, 1.0, -1, BOY, pk)
        clang = lf >= 34
        pd = P(torso=0, lhip=-14, lkn=0, rhip=14, rkn=0, lsh=-160, lel=-10, rsh=-160, rel=-10,
               eye='happy' if not clang else 'closed', mouth='grin' if not clang else 'wavy', head=0)
        bd = draw(ctx, 540, FLOOR - 186 * 1.35, 1.35, 1, DAD, pd)
        jar(ctx, bd['front'][0], bd['front'][1] + 40, 0.45, 0.2, has_lid=False, empty=0.7)
        for b_ in (bm, bk, bd):
            hx_, hy_ = b_['head']; R = b_['R']
            splats(ctx, hx_, hy_ - R * 0.2, R / 90, int(hx_))
            for k in range(2):
                dy = ((lf * 4 + k * 40) % 120)
                ellipse(ctx, hx_ - R * 0.6 + k * R * 1.1, hy_ + R * 0.3 + dy, 8, 12); setc(ctx, JUICE); ctx.fill()
        hx_, hy_ = bd['head']; R = bd['R']
        ellipse(ctx, hx_ + 10, hy_ - R * 1.05, 26, 70, 1.3); fl(ctx, PICK, 5)   # pickle on his head
        ly = lerp(-200, hy_ - R * 1.1, ein(pop(lf, 26, 34)))
        lid(ctx, hx_ - 30, ly, 0.6, 0.3 if lf < 34 else 0.15)
        if clang:
            zigs(ctx, hx_, hy_ - R * 0.4, R * 1.4, lf, YEL, 5)
        ctx.restore()
        if not clang:
            label1(ctx, "\"NAILED IT!\"", YEL, pop(lf, 2, 6), 130)
        else:
            label1(ctx, "*CLANG!*", (1, 1, 1), pop(lf, 34, 37), 130, 0.05)
    elif lf < 110:
        il = lf - 50
        # Mom: "Great! Now THIS one." - giant jar slides in
        ctx.save(); cam(ctx, 540, 1060, 1.08 - 0.06 * eout(pop(il, 0, 20)), 0, shake_at(il, [14], 12, 26), f)
        kitchen(ctx, hx('ffd9a8'))
        jx = lerp(1700, 750, eout(pop(il, 0, 14)))
        pm = P(torso=0, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=-20, lel=-20, rsh=100, rel=-10, eye='happy', mouth='grin', head=0)
        draw(ctx, 110, FLOOR - 186 * 1.2, 1.2, 1, MOM, pm)
        pd = P(torso=-8, lhip=-10, lkn=0, rhip=10, rkn=0, lsh=20, lel=-20, rsh=30, rel=-20,
               eye='shock' if il >= 14 else 'normal', mouth='scream' if il >= 14 else 'flat', head=-20 if il >= 14 else 0)
        bd = draw(ctx, 320, FLOOR - 186 * 1.2, 1.2, 1, DAD, pd)
        hx_, hy_ = bd['head']; R = bd['R']
        ellipse(ctx, hx_ + 10, hy_ - R * 1.05, 22, 60, 1.3); fl(ctx, PICK, 5)
        jar(ctx, jx, FLOOR + 10, 2.6)
        if il >= 14:
            puff(ctx, jx - 280, FLOOR - 40, pop(il, 14, 28), 1.2)
            sweat(ctx, hx_ - R * 1.1, hy_ - R * 0.2 + (il * 3) % 30, 1.0)
        ctx.restore()
        if il < 14:
            label2(ctx, "\"Great! Now...", "THIS one.\"", (1, 1, 1), pop(il, 0, 4), 108, col2=PINK)
        else:
            if il < 30:
                label1(ctx, "*THUD!*", YEL, pop(il, 14, 17), 140, 0.04)
            else:
                label2(ctx, "\"Great! Now...", "THIS one.\"", (1, 1, 1), 1.0, 108, col2=PINK)
        card(ctx, 'p5', f, 552, 610)
    elif lf < 125:
        il = lf - 110
        # ECU eye twitch
        ctx.save(); cam(ctx, 600, 860, 1.25 + 0.2 * eout(pop(il, 0, 15)), 0, 4 if (il // 3) % 2 else 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('3fd0a0')); ctx.fill()
        rays(ctx, 600, 860, 200, 1500, il * 0.05, col=(1, 1, 1), a=0.25, n=16)
        face(ctx, DAD, P(eye='shock', mouth='wavy', head=0), 540, 860, 280, 0.0)
        tw = (il // 2) % 2
        if tw:
            ex, ey, rx = eye_pos(540, 860, 280)[1]
            ctx.rectangle(ex - rx * 1.2, ey - rx * 1.3, rx * 2.4, rx * 0.9); setc(ctx, DAD['skin']); ctx.fill()
            ctx.move_to(ex - rx * 1.1, ey - rx * 0.4); ctx.line_to(ex + rx * 1.1, ey - rx * 0.4); ink(ctx, 10); ctx.stroke()
        sweat(ctx, 300, 760 + il * 4, 1.4)
        ctx.restore()
        label(ctx, "*twitch*", 760, 1300, 90, YEL, 0.1, pop(il, 1, 4))
    else:
        il = lf - 125
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 625)


SHOTS = [(0, s1), (110, s2), (250, s3), (400, s4), (500, s5)]
CUTS = (60, 110, 170, 206, 250, 340, 400, 450, 470, 500, 550, 610, 625)


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
                              "-i", "out/jar_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
