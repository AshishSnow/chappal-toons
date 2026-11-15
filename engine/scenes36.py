"""'I'll Walk Him Every Day!' - original, general-audience comedy short, ~22s.
Hook: ECU of the kid, giant pleading eyes: "PLEASE PLEASE PLEASE!" -> wide: puppy in his arms, parents arms crossed. "I'LL WALK HIM EVERY DAY!"
Beat 1: DAY 1 - kid sprints down the street with the dog. "BEST DAY EVER!"
Beat 2: DAY 2 - kid melted into a beanbag with a tablet; the dog sits with the leash in its mouth, staring. "5 more minutes..."
Beat 3: DAY 30 - Mom in a raincoat gets dragged through the rain, SPLASH, umbrella flips. Split screen: kid warm at the window: "BYE MOM!"
Beat 4: 6 AM the dog cannonballs onto Mom's bed. Mom ECU: "I didn't even WANT a dog..."
Twist: kid comes home: "HERE, BOY!" - the dog ZOOMS straight past him into Mom's arms. "WHO'S MOMMY'S BABY?"
Loop: kid ECU, same pleading eyes: "...CAN WE GET A CAT?" -> loops to "PLEASE PLEASE PLEASE!"."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, living, eye_pos, bedroom, bed_back, bed_front, clock
from scenes21 import dog, DOGC, DOGD, DOGL
from scenes14 import sweat
import scenes13
from scenes13 import card as _card13
import random

BOY = doodle.BOY
DAD = doodle.DAD
MOM = doodle.MOM_G
MOM_RAIN = dict(doodle.MOM_G, shirt=hx('ffd23f'), pants=hx('2a6ad0'), shoes=hx('2aa84a'))
N = 660
FLOOR = 1460
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
LEASH = hx('ff3b5c')
LY = 1450

CAPS = {
    'p1': [[("WHEN YOU BEG FOR A PET", OUT)], [("AND PROMISE EVERYTHING", RED)]],
    'p2': [[("DAY 1:", OUT)], [("WORLD'S BEST OWNER", GREEN)]],
    'p3': [[("DAY 2:", OUT)], [("\"5 MORE MINUTES...\"", ORANGE)]],
    'p4': [[("DAY 30: WHO WALKS", OUT)], [("THE DOG?", BLUE)]],
    'p5': [[("MOM, WHO SAID NO,", OUT)], [("NOW DOES EVERYTHING", PURPLE)]],
    'p6': [[("PLOT TWIST:", OUT)], [("IT'S MOM'S DOG NOW", PINK)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def run_dog(ctx, x, y, s, fr, f=1, tongue=1.0, eye='happy', speed=1.0, leash_out=False):
    """running dog, faces +x when f=1, (x, y) = ground under its body. returns collar point (world)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s * f, s)
    ph = fr * 0.9 * speed
    bob = -14 * abs(math.sin(ph))
    ctx.translate(0, bob)
    # tail
    w = math.sin(fr * 1.3)
    ctx.new_path(); ctx.move_to(-110, -150); ctx.curve_to(-170, -170, -200, -230 - 20 * w, -180 + 20 * w, -260)
    ink(ctx, 34); ctx.stroke_preserve(); setc(ctx, DOGC); ctx.set_line_width(20); ctx.stroke()
    # far legs
    for lx, o in ((-70, 0.0), (70, 1.6)):
        a = 0.7 * math.sin(ph + o + math.pi)
        ctx.save(); ctx.translate(lx, -120); ctx.rotate(a)
        rect_r(ctx, -16, 0, 32, 110, 15); fl(ctx, DOGD, 6); ctx.restore()
    # body
    ellipse(ctx, 0, -150, 140, 66); fl(ctx, DOGC, 6)
    ellipse(ctx, 20, -122, 90, 28); setc(ctx, DOGL); ctx.fill()
    ellipse(ctx, -40, -175, 34, 22, 0.2); setc(ctx, DOGD); ctx.fill()
    # near legs
    for lx, o in ((-80, 0.0), (80, 1.6)):
        a = 0.7 * math.sin(ph + o)
        ctx.save(); ctx.translate(lx, -120); ctx.rotate(a)
        rect_r(ctx, -17, 0, 34, 116, 16); fl(ctx, DOGC, 6)
        ellipse(ctx, 8, 112, 26, 13); fl(ctx, DOGL, 5); ctx.restore()
    # collar
    ellipse(ctx, 118, -185, 18, 46, 0.4); fl(ctx, RED, 6)
    ellipse(ctx, 130, -150, 12, 12); fl(ctx, hx('ffcc1f'), 4)
    # head
    ctx.save(); ctx.translate(165, -245)
    ctx.save(); ctx.translate(-30, -30); ctx.rotate(0.5 + 0.3 * math.sin(ph)); ellipse(ctx, 0, 40, 24, 50); fl(ctx, DOGD, 6); ctx.restore()
    ellipse(ctx, 0, 0, 76, 68); fl(ctx, DOGC, 6)
    ellipse(ctx, 62, 22, 52, 36); fl(ctx, DOGL, 6)
    ellipse(ctx, 108, 6, 18, 14); setc(ctx, INK); ctx.fill()
    ex, ey = 26, -20
    if eye == 'happy':
        ctx.new_path(); ctx.arc(ex, ey + 6, 13, math.pi * 1.1, math.pi * 1.9); ink(ctx, 7); ctx.stroke()
    elif eye == 'love':
        sparkle(ctx, ex, ey, 18, PINK)
    else:
        ellipse(ctx, ex, ey, 12, 16); setc(ctx, INK); ctx.fill()
        ellipse(ctx, ex - 3, ey - 6, 4, 5); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.new_path(); ctx.move_to(56, 46); ctx.curve_to(72, 62, 92, 60, 104, 42); ink(ctx, 6); ctx.stroke()
    if tongue > 0:
        tl = 30 + 40 * tongue + 10 * math.sin(ph * 2)
        rect_r(ctx, 64, 46, 32, tl, 15); fl(ctx, hx('ff6f86'), 5)
    ctx.save(); ctx.translate(-12, -40); ctx.rotate(0.3 + 0.5 * abs(math.sin(ph)))
    ctx.new_path(); ctx.move_to(-20, 0); ctx.curve_to(-50, 50, -40, 110, -6, 112); ctx.curve_to(26, 100, 30, 40, 20, 0); ctx.close_path(); fl(ctx, DOGD, 6)
    ctx.restore(); ctx.restore()
    ctx.restore()
    return (x + f * s * 125, y + s * (-160 + bob))


def leash(ctx, p0, p1, sag=60):
    mx, my = (p0[0] + p1[0]) / 2, max(p0[1], p1[1]) + sag
    ctx.new_path(); ctx.move_to(*p0); ctx.curve_to(mx, my, mx, my, *p1)
    setc(ctx, OUT); ctx.set_line_width(16); ctx.stroke_preserve(); setc(ctx, LEASH); ctx.set_line_width(9); ctx.stroke()


def pleading_eyes(ctx, cx, cy, Rt, lf):
    """giant wet sparkly 'puppy' eyes over face() 'shock' eyes"""
    for ex, ey, rx in eye_pos(cx, cy, Rt):
        ellipse(ctx, ex, ey + rx * 0.1, rx * 0.95, rx * 1.05); fl(ctx, hx('2a1a3a'), Rt * 0.02)
        ellipse(ctx, ex, ey + rx * 0.2, rx * 0.7, rx * 0.75); setc(ctx, hx('5a3a9a')); ctx.fill()
        ellipse(ctx, ex - rx * 0.3, ey - rx * 0.3, rx * 0.32, rx * 0.36); setc(ctx, (1, 1, 1)); ctx.fill()
        ellipse(ctx, ex + rx * 0.3, ey + rx * 0.35, rx * 0.14, rx * 0.14); setc(ctx, (1, 1, 1)); ctx.fill()
        # wobbling tear line on the lower lid
        ctx.new_path(); ctx.arc(ex, ey + rx * 0.2, rx * 0.85, 0.2 * math.pi, 0.8 * math.pi)
        setc(ctx, (0.6, 0.9, 1, 0.9)); ctx.set_line_width(Rt * 0.035 + 3 * math.sin(lf * 0.8)); ctx.stroke()


def hands_together(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for sg in (-1, 1):
        ctx.save(); ctx.rotate(sg * 0.12)
        rect_r(ctx, sg * 4 - (40 if sg < 0 else 0), -80, 40, 150, 20); fl(ctx, BOY['skin'], 7); ctx.restore()
    ctx.restore()


def street(ctx, off, rain=0.0):
    sky = hx('8fd8ff') if rain <= 0 else hx('5a6a8a')
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, sky); ctx.fill()
    if rain <= 0:
        ellipse(ctx, 860, 640, 90, 90); fl(ctx, YEL, 7)
        rays(ctx, 860, 640, 110, 220, off * 0.002, col=(1, 0.95, 0.5), a=0.6, n=12)
    for k in range(-2, 8):   # houses scroll
        x = k * 380 - (off * 0.6) % 380
        hcol = (hx('ff9f5a'), hx('b98aff'), hx('5ad0a0'), hx('ff7fa8'))[(k + int(off * 0.6 // 380)) % 4]
        if rain > 0:
            hcol = dark(hcol, 0.6)
        ctx.rectangle(x, 860, 300, 520); fl(ctx, hcol, 7)
        poly(ctx, [(x - 20, 860), (x + 150, 720), (x + 320, 860)]); fl(ctx, dark(hcol, 0.7), 7)
        rect_r(ctx, x + 40, 950, 90, 100, 8); fl(ctx, hx('fff2b0') if rain > 0 else hx('bfe8ff'), 5)
        rect_r(ctx, x + 180, 1180, 80, 200, 8); fl(ctx, dark(hcol, 0.55), 5)
    ctx.rectangle(-3000, 1380, 7000, 80); setc(ctx, hx('d8d8e0') if rain <= 0 else hx('8a8a9a')); ctx.fill()
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('6a6a78') if rain <= 0 else hx('3a3a4a')); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()
    for k in range(-1, 8):
        x = k * 300 - (off * 1.0) % 300
        ctx.rectangle(x, 1640, 150, 22); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()


def rain_fx(ctx, fr, a=1.0):
    rnd = random.Random(4)
    for k in range(110):
        x0, y0 = rnd.uniform(-200, 1300), rnd.uniform(0, 2200)
        y = (y0 + fr * 70) % 2200 - 100; x = x0 - (y * 0.25)
        ctx.move_to(x, y); ctx.line_to(x - 14, y + 60)
    setc(ctx, (0.8, 0.9, 1, 0.75 * a)); ctx.set_line_width(5); ctx.stroke()


def umbrella(ctx, x, y, flip, s=1.0, a=0.0):
    """(x, y) = hand. flip 0=normal dome, 1=inside out"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(0, 0); ctx.line_to(0, -330); ink(ctx, 9); ctx.stroke()
    d = 1 - 2 * flip   # dome direction
    ctx.new_path(); ctx.move_to(-230, -330)
    for k in range(4):
        x0 = -230 + k * 115
        ctx.curve_to(x0 + 30, -330 + 40 * d * 0.3, x0 + 85, -330 + 40 * d * 0.3, x0 + 115, -330)
    ctx.curve_to(170, -330 - 170 * d, -170, -330 - 170 * d, -230, -330); ctx.close_path(); fl(ctx, PINK, 8)
    for k in (-115, 0, 115):
        ctx.move_to(0, -330 - 150 * d); ctx.line_to(k, -330); setc(ctx, dark(PINK, 0.7)); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def splash(ctx, x, y, t, s=1.0):
    if not 0 < t < 1:
        return
    for k in range(9):
        a = -math.pi * (0.1 + 0.8 * k / 8)
        d = 260 * s * eout(t)
        ellipse(ctx, x + math.cos(a) * d, y + math.sin(a) * d * 1.2 + 300 * t * t * s, 26 * s * (1 - 0.5 * t), 34 * s * (1 - 0.5 * t)); fl(ctx, hx('8fd0ff'), 5)
    ellipse(ctx, x, y + 20, 280 * s, 40 * s); fl(ctx, hx('5a8ad0'), 6)


def beanbag(ctx, x, y, front=False):
    if not front:
        ctx.new_path(); ctx.move_to(x - 260, y + 160); ctx.curve_to(x - 300, y - 120, x - 120, y - 260, x + 30, y - 220)
        ctx.curve_to(x + 200, y - 180, x + 300, y - 20, x + 270, y + 160); ctx.close_path(); fl(ctx, PURPLE, 9)
    else:
        ctx.new_path(); ctx.move_to(x - 280, y + 170); ctx.curve_to(x - 260, y + 10, x - 60, y - 10, x + 60, y + 30)
        ctx.curve_to(x + 200, y + 40, x + 300, y + 60, x + 290, y + 170); ctx.close_path(); fl(ctx, dark(PURPLE, 0.85), 9)


def tablet(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -90, -60, 180, 120, 14); fl(ctx, hx('2a2a3a'), 6)
    rect_r(ctx, -78, -50, 156, 100, 8); setc(ctx, hx('6af0ff')); ctx.fill()
    ctx.restore()


def heart(ctx, x, y, r, col=PINK):
    ctx.save(); ctx.translate(x, y)
    ctx.new_path(); ctx.move_to(0, r * 0.9); ctx.curve_to(-r * 1.6, -r * 0.2, -r * 0.8, -r * 1.3, 0, -r * 0.5)
    ctx.curve_to(r * 0.8, -r * 1.3, r * 1.6, -r * 0.2, 0, r * 0.9); ctx.close_path(); fl(ctx, col, max(3, r * 0.12))
    ctx.restore()


def blanket_shoulders(ctx, cx, cy, Rt, col=hx('3ccfb0')):
    ctx.new_path(); ctx.move_to(cx - 1.6 * Rt, cy + 3 * Rt); ctx.curve_to(cx - 1.5 * Rt, cy + 0.6 * Rt, cx - 0.7 * Rt, cy + 0.75 * Rt, cx, cy + 0.85 * Rt)
    ctx.curve_to(cx + 0.7 * Rt, cy + 0.75 * Rt, cx + 1.5 * Rt, cy + 0.6 * Rt, cx + 1.6 * Rt, cy + 3 * Rt); ctx.close_path(); fl(ctx, col, Rt * 0.035)
    for k in range(-2, 3):
        ctx.move_to(cx + k * 0.5 * Rt, cy + 1.0 * Rt); ctx.line_to(cx + k * 0.6 * Rt, cy + 3 * Rt)
    setc(ctx, dark(col, 0.8)); ctx.set_line_width(Rt * 0.05); ctx.stroke()


def mug(ctx, x, y, s, lf):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(70, 0, 34, -1.3, 1.3); ink(ctx, 12); ctx.stroke()
    rect_r(ctx, -70, -70, 140, 150, 18); fl(ctx, RED, 7)
    ellipse(ctx, 0, -70, 70, 16); fl(ctx, hx('7a4a2c'), 5)
    for k in (-25, 25):
        ctx.move_to(k, -100); ctx.curve_to(k + 20, -140, k - 20, -170, k + 5 * math.sin(lf * 0.3), -210)
    setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()


# ------------------------------------------------------------------ shots
def opening_face(ctx, f, lf, lab=True, txt="\"PLEASE PLEASE PLEASE!\""):
    """ECU: kid, giant pleading puppy eyes, hands clasped"""
    sh = shake_at(lf, [0], 10, 18) + 2
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(lf, 0, 50)), 0, sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8ac0')); ctx.fill()
    rays(ctx, 540, 960, 260, 1500, lf * 0.02, col=(1, 1, 1), a=0.4, n=18)
    cx, cy, Rt = 540, 880 + 5 * math.sin(lf * 0.6), 300
    wob = 0.03 * math.sin(lf * 0.9)
    face(ctx, BOY, P(eye='shock', mouth='open', head=0), cx, cy, Rt, wob)
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(wob); ctx.translate(-cx, -cy)
    pleading_eyes(ctx, cx, cy, Rt, lf)
    ctx.restore()
    hy = 1250 + 6 * math.sin(lf * 1.2)
    for sg in (-1, 1):
        ellipse(ctx, 540 + sg * 48, hy, 66, 74); fl(ctx, BOY['skin'], 8)
    ctx.move_to(540, hy - 60); ctx.line_to(540, hy + 60); ink(ctx, 7); ctx.stroke()
    for k in range(5):
        sparkle(ctx, cx + 430 * math.cos(lf * 0.1 + k * 1.25), cy + 380 * math.sin(lf * 0.1 + k * 1.25), 26, (1, 1, 1))
    ctx.restore()
    if lab:
        label(ctx, txt, 540, LY + 40, 104, YEL, -0.04, pop(lf, 0, 4) if lf > 0 else 1)


def s1(ctx, f):
    if f < 50:
        opening_face(ctx, f, f)
    else:
        lf = f - 50
        ctx.save(); cam(ctx, 560, 1080, 0.92 + 0.06 * eout(pop(lf, 0, 60)), 0, shake_at(lf, [0, 30], 8, 12), f)
        living(ctx, True)
        # parents, arms crossed, skeptical
        mp = P(eye='glare', mouth='flat', lsh=40, lel=-130, rsh=40, rel=-130, head=4)
        draw_hip(ctx, 170, FLOOR - 230, 1.25, 1, DAD, mp)
        draw_hip(ctx, 360, FLOOR - 210, 1.15, 1, MOM, mp)
        # kid holds puppy up like a trophy
        up_ = 30 * eout(pop(lf, 28, 36))
        kp = P(eye='happy', mouth='grin', rsh=-150, rel=-30, lsh=-150, lel=30, head=-4)
        b = draw_hip(ctx, 760, FLOOR - 170, 1.05, -1, BOY, kp)
        hx_, hy_ = b['head']
        dog(ctx, hx_ - 60, hy_ - 120 - up_, 0.55, -1, lf, look=1, tongue=1.0, eye='happy', tail=1.5)
        if lf >= 30:
            for k in range(4):
                sparkle(ctx, hx_ - 60 + 220 * math.cos(lf * 0.2 + k * 1.6), hy_ - 260 + 120 * math.sin(lf * 0.2 + k * 1.6), 22, YEL)
        ctx.restore()
        if lf < 30:
            label(ctx, "\"I'LL WALK HIM EVERY DAY!\"", 540, LY, 88, (1, 1, 1), -0.03, pop(lf, 0, 4))
        else:
            label(ctx, "\"I PROMISE!!\"", 540, LY, 120, YEL, 0.04, pop(lf, 30, 34))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 60:
        # DAY 1: sprint down the street, both delighted
        ctx.save(); cam(ctx, 540, 1150, 0.95, -3, 3, f)
        street(ctx, lf * 26)
        hlines(ctx, lf // 2, 0.45, (1, 1, 1), 1050, 1450)
        cp = run_dog(ctx, 640, FLOOR + 10, 0.95, lf, 1, 1.0, 'happy', 1.3)
        kp = run_pose(lf * 0.9, eye='happy', mouth='grin', rsh=-70, rel=-20)
        b = draw_hip(ctx, 300, FLOOR - 165, 1.0, 1, BOY, kp)
        leash(ctx, b['front'], cp, 30)
        for k in range(3):
            ellipse(ctx, 120 - k * 90 - (lf * 9) % 90, FLOOR - 20 - k * 10, 50 + 10 * k, 36 + 6 * k); fl(ctx, (1, 1, 1), 5)
        ctx.restore()
        label(ctx, "\"BEST DAY EVER!\"", 540, LY + 60, 116, YEL, -0.04, pop(lf, 2, 6))
        card(ctx, 'p2', f, 112, 168)
    else:
        il = lf - 60
        # DAY 2: kid melted into a beanbag. dog waits with the leash in its mouth.
        push = eout(pop(il, 24, 60))
        ctx.save(); cam(ctx, 560 + 80 * push, 1150 - 60 * push, 0.95 + 0.4 * push, 0, 0, f)
        living(ctx, True)
        beanbag(ctx, 400, 1290)
        kp = P(eye='closed' if il < 30 else 'smug', mouth='smile', torso=-30, head=12, rsh=-40, rel=-100, lsh=-30, lel=-110)
        b = draw_hip(ctx, 390, 1330, 1.0, 1, BOY, kp)
        tablet(ctx, b['front'][0] + 70, b['front'][1] + 40, -0.5, 0.8)
        ctx.save(); g = cairo.RadialGradient(b['head'][0], b['head'][1], 20, b['head'][0], b['head'][1], 260)
        g.add_color_stop_rgba(0, 0.4, 0.95, 1, 0.35); g.add_color_stop_rgba(1, 0.4, 0.95, 1, 0); ctx.set_source(g); ctx.paint(); ctx.restore()
        beanbag(ctx, 400, 1290, True)
        mx, my = dog(ctx, 720, FLOOR, 1.0, -1, il, look=1, tongue=0.0, eye='normal', tail=0.5 if il < 30 else 0.05, tilt=0.1 * math.sin(il * 0.2) if il < 30 else 0)
        # leash hanging from the dog's mouth to the floor
        leash(ctx, (mx + 10, my - 10), (mx + 90, FLOOR - 10), 20)
        ctx.new_path(); ctx.move_to(mx + 90, FLOOR - 10); ctx.curve_to(mx + 200, FLOOR + 10, mx + 260, FLOOR - 20, mx + 330, FLOOR + 5)
        setc(ctx, OUT); ctx.set_line_width(16); ctx.stroke_preserve(); setc(ctx, LEASH); ctx.set_line_width(9); ctx.stroke()
        ctx.restore()
        if il < 30:
            label(ctx, "*wag wag?*", 540, LY, 110, (1, 1, 1), 0.04, pop(il, 2, 6))
        else:
            label(ctx, "\"5 more minutes...\"", 540, LY, 100, ORANGE, -0.03, pop(il, 30, 34))
        card(ctx, 'p3', f, 172, 228)


def s3(ctx, f):
    lf = f - 230
    if lf < 72:
        # DAY 30: Mom in a raincoat, dragged through the rain
        ctx.save(); cam(ctx, 540, 1130, 0.92, -6 + 2 * math.sin(lf * 0.4), 4 + shake_at(lf, [22, 46], 10, 22), f)
        street(ctx, lf * 30, rain=1.0)
        cp = run_dog(ctx, 720, FLOOR + 10, 0.95, lf, 1, 1.0, 'happy', 1.5)
        mp = P(eye='shock', mouth='scream', torso=-28, head=6, rsh=-80, rel=-10, lsh=-150, lel=20,
               lhip=-35, lkn=10, rhip=-20, rkn=5)
        b = draw_hip(ctx, 330, FLOOR - 150, 1.05, 1, MOM_RAIN, mp)
        leash(ctx, b['front'], cp, 0)
        ux, uy = b['back']
        flip = eout(pop(lf, 46, 52))
        umbrella(ctx, ux, uy, flip, 0.7, -0.5 - 0.4 * flip + 0.1 * math.sin(lf * 0.8))
        splash(ctx, 470, FLOOR + 20, pop(lf, 22, 44), 1.1)
        rain_fx(ctx, lf)
        hlines(ctx, lf // 2, 0.35, (1, 1, 1), 1000, 1450)
        ctx.restore()
        if lf < 22:
            label(ctx, "*WOOF WOOF!*", 540, LY + 60, 112, (1, 1, 1), 0.03, pop(lf, 1, 5))
        elif lf < 46:
            label(ctx, "*SPLASH!*", 540, LY + 60, 124, hx('8fd0ff'), -0.04, pop(lf, 22, 26))
        else:
            label(ctx, "*FWOOMP!*", 540, LY + 60, 124, PINK, 0.04, pop(lf, 46, 50))
    else:
        il = lf - 72
        # split screen: soaked Mom (top) vs kid warm at the window (bottom)
        mid = 1000
        ctx.save(); ctx.rectangle(0, 0, W, mid); ctx.clip()
        ctx.save(); cam(ctx, 540, 740, 1.0, 0, shake_at(il, [0], 8, 10), f, sy=740)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('4a5a7a')); ctx.fill()
        face(ctx, MOM_RAIN, P(eye='glare', mouth='flat', head=0), 540, 720, 200, 0.03)
        for k in range(6):   # drips off her hair
            dy = (il * 9 + k * 37) % 160
            ellipse(ctx, 360 + k * 75, 560 + dy + 40 * (k % 2), 10, 15); fl(ctx, hx('8fd0ff'), 3)
        rain_fx(ctx, il + 40)
        ctx.restore(); ctx.restore()
        ctx.save(); ctx.rectangle(0, mid, W, H - mid); ctx.clip()
        ctx.rectangle(0, mid, W, H - mid); setc(ctx, hx('ffb46a')); ctx.fill()
        rect_r(ctx, 150, mid + 60, 780, 560, 20); fl(ctx, hx('2a3a5a'), 10)          # window
        ctx.save(); rect_r(ctx, 160, mid + 70, 760, 540, 16); ctx.clip()
        ctx.rectangle(0, mid, W, 700); setc(ctx, hx('fff0c8')); ctx.fill()
        kw = 0.5 + 0.5 * math.sin(il * 0.6)
        face(ctx, BOY, P(eye='happy', mouth='grin', head=0), 470, mid + 330, 170, -0.05)
        blanket_shoulders(ctx, 470, mid + 330, 170)
        mug(ctx, 720, mid + 520, 0.8, il)
        # waving hand
        ctx.save(); ctx.translate(250, mid + 380); ctx.rotate(-0.4 + 0.5 * kw)
        rect_r(ctx, -30, -120, 60, 130, 28); fl(ctx, BOY['skin'], 6); ctx.restore()
        ctx.restore()
        ctx.move_to(540, mid + 60); ctx.line_to(540, mid + 620); ctx.move_to(150, mid + 340); ctx.line_to(930, mid + 340)
        setc(ctx, hx('2a3a5a')); ctx.set_line_width(6); ctx.stroke()
        ctx.restore()
        ctx.move_to(0, mid); ctx.line_to(W, mid); setc(ctx, OUT); ctx.set_line_width(14); ctx.stroke()
        if il >= 8:
            label(ctx, "\"BYE MOM! HAVE FUN!\"", 540, LY + 170, 92, YEL, -0.03, pop(il, 8, 12))
    card(ctx, 'p4', f, 234, 366)


def s4(ctx, f):
    lf = f - 370
    if lf < 56:
        # 6 AM: the dog cannonballs onto Mom's bed with the leash
        ctx.save(); cam(ctx, 540, 1100, 0.95, 0, shake_at(lf, [20], 12, 26), f)
        bedroom(ctx, lights=False, hh=6, mm=0)
        bed_back(ctx)
        jump = eout(pop(lf, 6, 20))
        up_ = (1 - jump) * 0 + (0 if lf >= 20 else 0)
        mp = P(eye='closed' if lf < 20 else 'shock', mouth='flat' if lf < 20 else 'scream', torso=-60 if lf < 20 else -10,
               head=-20 if lf < 20 else 0, rsh=-20 if lf < 20 else -160, rel=-20, lsh=20 if lf < 20 else 160, lel=20)
        draw_hip(ctx, 380, 1250 - (0 if lf < 20 else 30), 1.1, 1, MOM, mp)
        bed_front(ctx, squash=1.0 if lf >= 20 and lf < 26 else 0.0)
        # dog arc in from the right
        t = min(1, lf / 20)
        dxp = 1250 - 560 * t; dyp = 1170 - 420 * math.sin(math.pi * t) if lf < 20 else 1180 - 30 * abs(math.sin((lf - 20) * 0.4))
        mx, my = dog(ctx, dxp, dyp, 0.85, -1, lf, look=1, tongue=1.0 if lf >= 20 else 0.4, eye='happy', tail=1.5, tilt=-0.3 if lf < 20 else 0)
        leash(ctx, (mx, my - 10), (mx + 120, my + 80), 30)
        if lf < 20:
            text(ctx, "z", 420, 980 - lf * 4, 70, hx('c8e6ff'), ow=10, shadow=False)
        ctx.restore()
        if lf < 20:
            label(ctx, "*6:00 AM*", 540, LY + 60, 112, (1, 1, 1), 0.03, pop(lf, 1, 5))
        else:
            label(ctx, "*BOOF!*", 540, LY + 60, 130, YEL, -0.04, pop(lf, 20, 24))
    else:
        il = lf - 56
        # Mom ECU, exhausted, getting licked
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.07 * eout(pop(il, 0, 74)), -3, shake_at(il, [0], 6, 10), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('5a6ad8')); ctx.fill()
        rays(ctx, 540, 900, 260, 1500, il * 0.01, col=(0.35, 0.4, 0.85), a=0.5, n=14)
        face(ctx, MOM, P(eye='glare', mouth='flat', head=0), 480, 880, 280, 0.04)
        for k, sx in enumerate((-0.2, 0.42)):   # dark circles
            ctx.new_path(); ctx.arc(480 + sx * 280, 880 + 0.12 * 280, 55, 0.2 * math.pi, 0.8 * math.pi); setc(ctx, (0.35, 0.2, 0.5, 0.7)); ctx.set_line_width(10); ctx.stroke()
        lick = abs(math.sin(il * 0.35))
        mx, my = dog(ctx, 960, 1380, 1.1, -1, il, look=1, tongue=0.6 + 0.6 * lick, eye='happy', tail=1.5, tilt=-0.15 * lick)
        sweat(ctx, 700, 740, il, 1.4)
        ctx.restore()
        label(ctx, "\"I didn't even WANT a dog...\"", 540, LY + 50, 84, (1, 1, 1), -0.03, pop(il, 4, 8))
    card(ctx, 'p5', f, 374, 496)


def s5(ctx, f):
    lf = f - 500
    if lf < 60:
        # kid comes home: "HERE, BOY!" -> dog zooms right past him to Mom
        ctx.save(); cam(ctx, 540, 1100, 0.9, 0, shake_at(lf, [26], 10, 20), f)
        living(ctx, True, door=1.0)
        # Mom on the left, arms open
        mp = P(eye='happy', mouth='grin', rsh=-120, rel=-30, lsh=120, lel=30)
        draw_hip(ctx, 170, FLOOR - 220, 1.2, 1, MOM, mp)
        spin = lf >= 32
        kp = P(eye='happy' if lf < 26 else 'shock', mouth='grin' if lf < 26 else 'open', rsh=-120, rel=-20, lsh=120, lel=20)
        draw_hip(ctx, 690, FLOOR - 165, 1.05, 1 if spin else -1, BOY, kp)
        if lf < 18:
            dog(ctx, 400, FLOOR, 0.8, 1, lf, look=1, tongue=0.0, eye='normal', tail=0.3)
        elif lf < 30:
            t = (lf - 18) / 12
            run_dog(ctx, 400 + 480 * t if t < 0.5 else 880 - 1300 * (t - 0.5), FLOOR + 10, 0.8, lf, 1 if t < 0.5 else -1, 1.0, 'happy', 2.0)
            hlines(ctx, lf, 0.6, (1, 1, 1), 1150, 1450)
        else:
            run_dog(ctx, 330, FLOOR - 120 - 80 * abs(math.sin(lf * 0.4)), 0.7, lf, -1, 1.0, 'love', 0.6)
            for k in range(3):
                heart(ctx, 260 + k * 70, 1000 - ((lf * 6 + k * 40) % 160), 24)
        ctx.restore()
        if lf < 18:
            label(ctx, "\"HERE, BOY!\"", 540, LY + 60, 120, YEL, -0.03, pop(lf, 1, 5))
        elif lf < 32:
            label(ctx, "*ZOOOM!*", 540, LY + 60, 128, (1, 1, 1), 0.04, pop(lf, 18, 22))
        else:
            label(ctx, "\"...HEY?!\"", 540, LY + 60, 124, RED, -0.04, pop(lf, 32, 36))
    elif lf < 126:
        il = lf - 60
        # Mom + dog cuddle ECU, hearts everywhere
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(il, 0, 66)), 2, shake_at(il, [0], 6, 10), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb0d8')); ctx.fill()
        rays(ctx, 540, 900, 240, 1500, il * 0.02, col=(1, 1, 1), a=0.4, n=16)
        face(ctx, MOM, P(eye='happy', mouth='grin', head=0), 420, 860, 250, -0.1)
        dog(ctx, 560, 1440, 1.25, -1, il, look=1, tongue=1.0, eye='happy', tail=2.0, tilt=-0.2)
        for k in range(6):
            heart(ctx, 540 + 420 * math.cos(il * 0.08 + k * 1.05), 900 + 360 * math.sin(il * 0.08 + k * 1.05), 34)
        ctx.restore()
        label(ctx, "\"WHO'S MOMMY'S BABY?!\"", 540, LY + 50, 96, (1, 1, 1), -0.03, pop(il, 4, 8))
        # kid, jealous glare, inset (left, below the caption)
        if il >= 24:
            u = eout(pop(il, 24, 32))
            ctx.save(); ctx.translate(200 - 320 * (1 - u), 1180)
            ellipse(ctx, 0, 0, 130, 130); fl(ctx, YEL, 8); ctx.save(); ellipse(ctx, 0, 0, 122, 122); ctx.clip()
            face(ctx, BOY, P(eye='glare', mouth='frown', head=0), 0, 10, 95, 0.05)
            ctx.restore(); ctx.restore()
    else:
        il = lf - 126
        opening_face(ctx, f, il, True, "\"...CAN WE GET A CAT?\"")
    if lf < 126:
        card(ctx, 'p6', f, 504, 622)
    else:
        card(ctx, 'p1', f, 626)


SHOTS = [(0, s1), (110, s2), (230, s3), (370, s4), (500, s5)]
CUTS = (50, 110, 170, 230, 302, 370, 426, 500, 560, 626)


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
                              "-i", "out/walk_the_dog_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
