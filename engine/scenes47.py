"""'Hide and Seek with a Little Kid' - original, general-audience comedy short, 22s.
Hook: ECU kid with both hands over his eyes, one eye peeking through the fingers: "YOU CAN'T SEE ME!"
 -> wide: he is "hiding" in the middle of the living room. Dad plays along: "Hmm... where could he BE?"
Beat 1: curtain with two little feet poking out + "hee hee". Dad: "NOT behind the curtain..."
Beat 2: giggling blanket lump on the sofa. Dad sits on it. *SQUISH* "HEY!!"
Beat 3: Dad's turn: kid counts, Dad super-speeds into a kitchen cupboard (*SQUEEEZE*, shirt stuck in the door, *CLICK*),
 POV from inside the dark cupboard: "He'll NEVER find me."
Split screen 20 minutes later: Dad sweating with a spider / kid on the sofa with ice cream: "...wait, we were playing?"
Twist: 3 HOURS LATER, Dad has a long beard and a mouse friend: "I... still... WIN." Mom opens the cupboard for a pan,
 Dad bursts out "DID I WIN?!", pan *CLANG* -> cut back to the opening peek (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, living, sofa_back, sofa_front, SEAT, eye_pos
from scenes8 import sit
from scenes14 import sweat
from scenes19 import cobweb
from scenes20 import pan
from scenes42 import ice_cream
import scenes13
from scenes13 import card as _card13
import random

BOY = dict(doodle.BOY, hood=False)
DAD = doodle.DAD
MOM = doodle.MOM_G
N = 660
FLOOR = 1460
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
LY = 1400

CAPS = {
    'p1': [[("HIDE AND SEEK", OUT)], [("WITH A LITTLE KID", RED)]],
    'p2': [[("HIDING SPOT #1:", OUT)], [("THE CURTAIN", ORANGE)]],
    'p2b': [[("HIDING SPOT #2:", OUT)], [("THE SOFA", PINK)]],
    'p3': [[("NOW IT'S", OUT)], [("DAD'S TURN TO HIDE", GREEN)]],
    'p4': [[("20 MINUTES LATER...", BLUE)]],
    'p5': [[("PLOT TWIST:", OUT)], [("NOBODY CAME LOOKING", PURPLE)]],
}
scenes13.CAPS = CAPS
card = _card13


def label2(ctx, a, b, col, t, size=104, col2=None, y=LY):
    label(ctx, a, 540, y - 60, size, col, -0.03, t)
    label(ctx, b, 540, y + 50, size, col2 or col, 0.02, t)


def label1(ctx, s, col, t, size=110, ang=-0.03, y=LY + 20):
    label(ctx, s, 540, y, size, col, ang, t)


# ------------------------------------------------------------------ props
def hand(ctx, x, y, s, ch, a=0.0, gap=0.0):
    """open hand, fingers pointing up (rotated by a). gap opens a slit between 2nd and 3rd finger"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    for k, (dx, L) in enumerate(((-48, 92), (-16, 112), (16, 108), (46, 90))):
        sh = (-gap if k < 2 else gap) * 18
        ctx.save(); ctx.translate(dx + sh, -30); ctx.rotate((-0.12 + 0.08 * k) + (-0.25 if k < 2 else 0.25) * gap)
        rect_r(ctx, -15, -L, 30, L + 20, 15); fl(ctx, ch['skin'], 6)
        ctx.restore()
    ellipse(ctx, 0, 10, 70, 62); fl(ctx, ch['skin'], 6)
    ctx.restore()


def peek_face(ctx, ch, cx, cy, R, lf, peek=1.0, mouth='grin', rot=0.0):
    """face with both hands over the eyes; right hand opens a slit to peek through"""
    face(ctx, ch, P(eye='shock', mouth=mouth, head=0), cx, cy, R, rot)
    (lx, ly, _), (rx, ry, _) = eye_pos(cx, cy, R)
    hand(ctx, lx - 0.04 * R, ly + 0.2 * R, R / 230, ch, -0.18)
    hand(ctx, rx + 0.02 * R, ry + 0.2 * R, R / 230, ch, 0.18, gap=peek)
    if peek > 0.3:
        # the peeking eye in the slit
        ex, ey = rx + 0.02 * R + 0.02 * R, ry - 0.02 * R
        ellipse(ctx, ex, ey, 0.09 * R, 0.15 * R * min(1, peek)); fl(ctx, (1, 1, 1), R * 0.02)
        ellipse(ctx, ex + 0.015 * R * math.sin(lf * 0.2), ey + 0.01 * R, 0.035 * R, 0.05 * R * min(1, peek)); setc(ctx, INK); ctx.fill()


def giggle(ctx, x, y, lf, size=60, col=None):
    u = (lf % 20) / 20
    text(ctx, "hee hee", x + 10 * math.sin(lf * 0.4), y - 40 * u, size, (col or YEL) + (1 - 0.6 * u,), ow=8, shadow=False)


def curtain_set(ctx, lf, feet=True):
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd98a')); ctx.fill()
    for i in range(-6, 16):
        ctx.rectangle(i * 130, -500, 50, 3000); setc(ctx, (1, 1, 1, 0.18)); ctx.fill()
    # window (night sky)
    rect_r(ctx, 380, 560, 520, 640, 12); fl(ctx, hx('9ad8ff'), 10)
    ellipse(ctx, 780, 680, 50, 50); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()
    ctx.rectangle(-500, FLOOR, 2200, 600); setc(ctx, hx('c98a52')); ctx.fill()
    ctx.move_to(-500, FLOOR); ctx.line_to(1700, FLOOR); ink(ctx, 8); ctx.stroke()
    # rod
    ctx.rectangle(320, 520, 640, 20); fl(ctx, hx('8a5a3a'), 6)
    # left curtain (flat)
    poly(ctx, [(330, 540), (520, 540), (500, FLOOR - 30), (310, FLOOR - 30)]); fl(ctx, hx('ff5a7a'), 8)
    # right curtain with a kid-shaped bulge
    w = 6 * math.sin(lf * 0.5) if feet else 0
    ctx.new_path(); ctx.move_to(740, 540); ctx.line_to(950, 540)
    ctx.line_to(955, FLOOR - 30)
    if feet:
        ctx.line_to(700, FLOOR - 30)
        ctx.curve_to(640 + w, 1300, 600 + w, 1050, 640 + w, 880)
        ctx.curve_to(660, 800, 720, 760, 740, 700)
    else:
        ctx.line_to(760, FLOOR - 30)
    ctx.close_path(); fl(ctx, hx('ff5a7a'), 8)
    for k in range(3):
        ctx.move_to(790 + k * 50, 560); ctx.line_to(790 + k * 50 - (20 if feet else 0), FLOOR - 50)
    setc(ctx, dark(hx('ff5a7a'), 0.8)); ctx.set_line_width(8); ctx.stroke()
    if feet:
        for k, fx in enumerate((700, 790)):
            wig = 6 * math.sin(lf * 0.6 + k * 2)
            ctx.save(); ctx.translate(fx, FLOOR - 18); ctx.rotate(0.15 * math.sin(lf * 0.6 + k * 2))
            ellipse(ctx, -14, 0, 52, 26); fl(ctx, BOY['shoes'], 7)
            ctx.restore()


def lump(ctx, x, y, lf, squash=0.0):
    """giggling blanket lump sitting on the sofa seat at y"""
    h = 230 * (1 - 0.75 * squash)
    wob = 8 * math.sin(lf * 0.7) * (1 - squash)
    ctx.new_path(); ctx.move_to(x - 200 - 40 * squash, y)
    ctx.curve_to(x - 200, y - h * 0.8, x - 90 + wob, y - h, x + wob, y - h)
    ctx.curve_to(x + 100 + wob, y - h, x + 200, y - h * 0.7, x + 210 + 40 * squash, y); ctx.close_path()
    fl(ctx, hx('5fd0ff'), 9)
    for k in range(3):
        ellipse(ctx, x - 90 + k * 90 + wob * 0.5, y - h * 0.45, 22, 22 * (1 - 0.5 * squash)); setc(ctx, (1, 1, 1, 0.7)); ctx.fill()
    # a shoe poking out
    ctx.save(); ctx.translate(x + 215 + 40 * squash, y - 20); ctx.rotate(-0.3 + 0.2 * math.sin(lf * 0.6))
    ellipse(ctx, 20, 0, 40, 22); fl(ctx, BOY['shoes'], 6); ctx.restore()


def kitchen(ctx, door=0.0, dark_=False):
    wall = hx('a8ecd0') if not dark_ else hx('1d2c50')
    ctx.rectangle(-1500, -1500, 4200, 4200); setc(ctx, wall); ctx.fill()
    for i in range(-8, 16):
        ctx.rectangle(i * 150, -400, 60, FLOOR + 400); setc(ctx, (1, 1, 1, 0.14)); ctx.fill()
    # upper shelf + jars
    ctx.rectangle(140, 720, 800, 20); fl(ctx, hx('8a5a3a'), 6)
    for k, c in enumerate((hx('ff8a1f'), hx('ff5fa8'), hx('ffd23f'))):
        rect_r(ctx, 200 + k * 230, 590, 120, 130, 18); fl(ctx, (1, 1, 1), 6)
        rect_r(ctx, 210 + k * 230, 640, 100, 76, 12); setc(ctx, c); ctx.fill()
        rect_r(ctx, 194 + k * 230, 570, 132, 30, 8); fl(ctx, hx('8a5a3a'), 5)
    # counter top + cabinets
    ctx.rectangle(-500, FLOOR, 2200, 600); setc(ctx, hx('e0a868') if not dark_ else hx('2a2040')); ctx.fill()
    ctx.move_to(-500, FLOOR); ctx.line_to(1700, FLOOR); ink(ctx, 8); ctx.stroke()
    ctx.rectangle(80, 1000, 920, 40); fl(ctx, hx('f4f8ff'), 8)
    ctx.rectangle(100, 1040, 880, 420); fl(ctx, hx('ffcf6a'), 8)
    for k, x0 in enumerate((110, 400, 690)):
        if k == 1:
            continue
        rect_r(ctx, x0 + 10, 1060, 270, 380, 10); fl(ctx, hx('ffbf3a'), 7)
        rect_r(ctx, x0 + (220 if k == 0 else 30), 1220, 20, 70, 8); fl(ctx, hx('8a5a3a'), 4)


def cab_door(ctx, openv=0.0, shirt=0.0):
    """middle cupboard door (x 410-680). openv 0 closed .. 1 swung open to the left"""
    x0, x1, y0, y1 = 410, 680, 1060, 1440
    if openv < 0.02:
        rect_r(ctx, x0, y0, x1 - x0, y1 - y0, 10); fl(ctx, hx('ffbf3a'), 7)
        rect_r(ctx, x0 + 30, 1220, 20, 70, 8); fl(ctx, hx('8a5a3a'), 4)
        if shirt > 0:
            poly(ctx, [(x0 + 4, 1180), (x0 - 50 * shirt, 1200), (x0 - 40 * shirt, 1250), (x0 + 4, 1240)]); fl(ctx, DAD['shirt'], 5)
    else:
        rect_r(ctx, x0, y0, x1 - x0, y1 - y0, 6); fl(ctx, hx('2a1a30'), 7)
        w = (x1 - x0) * (1 - openv)
        poly(ctx, [(x0, y0), (x0 - w * 0.0 - 30 * openv, y0 - 40 * openv), (x0 - 30 * openv, y1 + 40 * openv), (x0, y1)])
        xx = x0 - 30 * openv
        poly(ctx, [(x0, y0), (x0 + w - (x1 - x0) * 0 - 2 * 0, y0), (x0 + w, y1), (x0, y1)]) if False else None
        # door seen swinging toward camera: drawn as a skewed panel to the left
        pw = 270 * (1 - 0.65 * openv)
        poly(ctx, [(x0, y0), (x0 - pw, y0 - 60 * openv), (x0 - pw, y1 + 60 * openv), (x0, y1)]); fl(ctx, hx('ffbf3a'), 7)


def mouse(ctx, x, y, s, lf):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(60, -10); ctx.curve_to(120, -10, 120, -60, 160, -50); ink(ctx, 5); ctx.stroke()
    ellipse(ctx, 0, -40, 70, 45); fl(ctx, hx('b8b8c8'), 6)
    ellipse(ctx, -55, -85, 26, 26); fl(ctx, hx('ffb3c8'), 5)
    ellipse(ctx, -20, -95, 26, 26); fl(ctx, hx('ffb3c8'), 5)
    ellipse(ctx, -60, -50, 6, 7); setc(ctx, INK); ctx.fill()
    ellipse(ctx, -72, -36, 8, 6); setc(ctx, hx('ff5fa8')); ctx.fill()
    ctx.restore()


def spider(ctx, x, y, s, lf):
    ctx.move_to(x, -200); ctx.line_to(x, y); setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(3); ctx.stroke()
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for sd in (-1, 1):
        for k in range(4):
            a = -0.6 + k * 0.4 + 0.1 * math.sin(lf * 0.5 + k)
            ctx.move_to(0, 0); ctx.line_to(sd * 50 * math.cos(a), 30 * math.sin(a) - 10); ctx.line_to(sd * 75 * math.cos(a), 30 * math.sin(a) + 25)
    ink(ctx, 6); ctx.stroke()
    ellipse(ctx, 0, 0, 30, 34); setc(ctx, INK); ctx.fill()
    for dx in (-10, 10):
        ellipse(ctx, dx, -8, 8, 9); setc(ctx, (1, 1, 1)); ctx.fill()
        ellipse(ctx, dx, -6, 3, 4); setc(ctx, INK); ctx.fill()
    ctx.restore()


def beard(ctx, cx, cy, R, lf):
    ctx.new_path(); ctx.move_to(cx - 0.85 * R, cy + 0.15 * R)
    ctx.curve_to(cx - 0.9 * R, cy + 1.2 * R, cx - 0.4 * R, cy + 1.9 * R, cx + 0.05 * R, cy + 2.1 * R + 6 * math.sin(lf * 0.3))
    ctx.curve_to(cx + 0.5 * R, cy + 1.9 * R, cx + 1.0 * R, cy + 1.2 * R, cx + 0.95 * R, cy + 0.15 * R)
    ctx.curve_to(cx + 0.6 * R, cy + 0.75 * R, cx + 0.2 * R, cy + 0.4 * R, cx + 0.05 * R, cy + 0.5 * R)
    ctx.curve_to(cx - 0.2 * R, cy + 0.4 * R, cx - 0.6 * R, cy + 0.75 * R, cx - 0.85 * R, cy + 0.15 * R); ctx.close_path()
    fl(ctx, hx('d8d8e4'), R * 0.03)
    for k in range(5):
        ctx.move_to(cx - 0.5 * R + k * 0.25 * R, cy + 0.9 * R); ctx.line_to(cx - 0.4 * R + k * 0.22 * R, cy + 1.5 * R)
    setc(ctx, hx('a8a8b8')); ctx.set_line_width(R * 0.02); ctx.stroke()


def cupboard_pov(ctx, f, lf, bearded=False):
    """inside the dark cupboard: Dad crammed in, lit by the slit of light through the door crack"""
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 50)), 0, 0, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('120c1c')); ctx.fill()
    # shelf plank + pots in silhouette
    ctx.rectangle(-500, 1360, 2200, 30); setc(ctx, hx('2a1a30')); ctx.fill()
    for k, (x, w_, h_) in enumerate(((150, 160, 120), (930, 180, 150))):
        rect_r(ctx, x - w_ / 2, 1360 - h_, w_, h_, 20); setc(ctx, hx('2e2440')); ctx.fill()
    ellipse(ctx, 170, 1150, 60, 80); setc(ctx, hx('2e2440')); ctx.fill()
    cx, cy, R = 520, 880, 250
    face(ctx, DAD, P(eye='smug' if not bearded else 'shock', mouth='grin' if not bearded else 'wavy', head=0), cx, cy, R, -0.18)
    if bearded:
        beard(ctx, cx + 10, cy + 40, R, lf)
        cobweb(ctx, cx - 300, 520, 1.6)
        cobweb(ctx, 1020, 1300, 1.3)
    # knees squashed against his face
    for kx in (300, 760):
        ellipse(ctx, kx, 1260, 150, 120); fl(ctx, DAD['pants'], 9)
    if bearded:
        mouse(ctx, 920, 1360, 1.2, lf)
        # tiny party hat on the mouse
        poly(ctx, [(900, 1250), (850, 1300), (950, 1300)]) if False else None
    ctx.restore()
    # light slit
    ctx.save()
    ctx.push_group()
    ctx.rectangle(0, 0, W, H); setc(ctx, (0, 0, 0, 0.55)); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    poly(ctx, [(560, 0), (620, 0), (760, H), (520, H)]); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.pop_group_to_source(); ctx.paint()
    poly(ctx, [(560, 0), (620, 0), (760, H), (520, H)]); setc(ctx, (1, 0.95, 0.7, 0.12)); ctx.fill()
    ctx.restore()


# ------------------------------------------------------------------ opening
def opening_face(ctx, f, lf, lab=True):
    sh = shake_at(lf, [0], 8, 14)
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 30)), 1.5 * math.sin(lf * 0.5), sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffcf3d')); ctx.fill()
    rays(ctx, 540, 860, 240, 1700, lf * 0.04, col=(1, 1, 1), a=0.35, n=18)
    cx, cy = 540, 880 + 10 * math.sin(lf * 0.9)
    peek_face(ctx, BOY, cx, cy, 300, lf, peek=eout(pop(lf, 6, 14)), rot=0.05 * math.sin(lf * 0.45))
    giggle(ctx, 880, 720, lf, 70)
    ctx.restore()
    if lab:
        label2(ctx, "\"YOU CAN'T", "SEE ME!\"", (1, 1, 1), pop(lf, 0, 3) if lf > 0 else 1, 130, col2=RED)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 50:
        opening_face(ctx, f, f)
    else:
        lf = f - 50
        ctx.save(); cam(ctx, 540, 1080, 1.0 + 0.06 * eout(pop(lf, 0, 60)), 0, 0, f)
        living(ctx, lights=True)
        # kid "hiding" in the middle of the room
        b = draw(ctx, 620, FLOOR - 186 * 1.35, 1.35, -1, BOY,
                 P(torso=0, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=150, lel=-110, rsh=150, rel=-110, eye='happy', mouth='grin', head=0))
        hx_, hy_ = b['head']; R = b['R']
        (lx, ly, _), (rx, ry, _) = eye_pos(hx_, hy_, R, -1)
        hand(ctx, (lx + rx) / 2 - 0.25 * R, hy_ + 0.25 * R, R / 230, BOY, -0.18)
        hand(ctx, (lx + rx) / 2 + 0.25 * R, hy_ + 0.25 * R, R / 230, BOY, 0.18)
        giggle(ctx, 760, 760, lf, 56)
        # Dad pretending to search, hand above his eyes
        sw = math.sin(lf * 0.12)
        draw(ctx, 230, FLOOR - 186 * 1.7, 1.7, 1, DAD,
             P(torso=-4, lhip=-10, lkn=0, rhip=10, rkn=0, lsh=150, lel=-120, rsh=-30, rel=110, eye='smug', mouth='open', head=8 * sw))
        ctx.restore()
        label2(ctx, "\"Hmm... where", "could he BE?\"", (1, 1, 1), pop(lf, 0, 4), 104, col2=YEL)
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 70:
        ctx.save(); cam(ctx, 560 - 20 * eout(pop(lf, 0, 70)), 1280, 1.0 + 0.08 * eout(pop(lf, 0, 70)), 0, 0, f)
        curtain_set(ctx, lf)
        giggle(ctx, 660, 900, lf, 64, (1, 1, 1))
        draw(ctx, 310, FLOOR - 186 * 1.7, 1.7, 1, DAD,
             P(torso=-4, lhip=-10, lkn=0, rhip=10, rkn=0, lsh=-40, lel=120, rsh=150, rel=-130, eye='smug', mouth='open', head=-6))
        ctx.restore()
        label2(ctx, "\"Hmm... he's NOT", "behind the curtain...\"", (1, 1, 1), pop(lf, 4, 8), 96, col2=YEL)
        card(ctx, 'p2', f, 112, 176)
    else:
        il = lf - 70
        hit = il >= 34
        ctx.save(); cam(ctx, 520, 1100, 1.05 + (0.1 * eout(pop(il, 34, 40)) if hit else 0), 0, shake_at(il, [34], 12, 26), f)
        living(ctx, lights=True)
        sofa_back(ctx)
        if not hit:
            lump(ctx, 520, SEAT, il)
            x = lerp(980, 560, eout(pop(il, 0, 26)))
            sink = 120 * eout(pop(il, 22, 34))
            ph = il * 0.5
            p = sit(eye='smug', mouth='smile', lsh=20, rel=-40) if il >= 24 else \
                P(torso=4, lhip=20 * math.sin(ph), lkn=-20, rhip=-20 * math.sin(ph), rkn=-20, lsh=-30, lel=110, rsh=30, rel=-110, eye='smug', mouth='smile')
            if il < 24:
                draw(ctx, x, FLOOR - 186 * 1.5, 1.5, -1, DAD, p)
            else:
                draw_hip(ctx, x, SEAT - 230 + sink, 1.5, -1, DAD, p)
            giggle(ctx, 420, 980, il, 60, (1, 1, 1))
        else:
            jl = il - 34
            lump(ctx, 520, SEAT, jl, 1.0)
            draw_hip(ctx, 560, SEAT - 90, 1.5, -1, DAD, sit(eye='shock', mouth='open', lsh=150, lel=-20, rsh=150, rel=-20, head=0))
            puff(ctx, 760, SEAT - 40, pop(jl, 0, 14), 1.6)
        sofa_front(ctx)
        ctx.restore()
        if not hit:
            label2(ctx, "\"What a comfy", "sofa...\"", (1, 1, 1), pop(il, 2, 6), 110, col2=YEL)
        else:
            label2(ctx, "*SQUISH!*", "\"HEY!!\"", YEL, pop(il, 34, 37), 140, col2=RED)
        card(ctx, 'p2b', f, 182, 246)


def s3(ctx, f):
    lf = f - 250
    if lf < 34:
        # low-angle kid at the wall, counting
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(lf, 0, 34)), -3, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('6fd6c8')); ctx.fill()
        for i in range(-6, 16):
            ctx.rectangle(i * 120, -500, 46, 3000); setc(ctx, dark(hx('6fd6c8'), 0.94)); ctx.fill()
        peek_face(ctx, BOY, 540, 900, 260, lf, peek=0.0, mouth='open')
        ctx.restore()
        label1(ctx, "\"1... 2... 3...\"", (1, 1, 1), pop(lf, 0, 4), 120)
    elif lf < 84:
        il = lf - 34
        click_ = il >= 34
        ctx.save(); cam(ctx, 545, 1180, 1.12, 0, shake_at(il, [34], 10, 16), f)
        kitchen(ctx)
        if il < 12:
            # super-speed zoom in from the right
            x = lerp(1200, 560, eout(pop(il, 0, 12)))
            for k in range(6):
                ctx.move_to(x + 160 + k * 30, 900 + k * 90); ctx.rel_line_to(260, 0)
            setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(10); ctx.stroke()
            cab_door(ctx, 1.0)
            draw(ctx, x, FLOOR - 186 * 1.6, 1.6, -1, DAD,
                 P(torso=-25, lhip=-50, lkn=-40, rhip=50, rkn=-60, lsh=-60, lel=-30, rsh=60, rel=-30, eye='smug', mouth='grin', head=10))
        elif not click_:
            jl = il - 12
            sq = eout(pop(jl, 0, 16))
            cab_door(ctx, 1.0)
            ctx.save()
            ctx.rectangle(400, 1050, 290, 400); ctx.clip()
            ctx.translate(545, 1440); ctx.scale(1.0 - 0.15 * sq, 1.0 - 0.45 * sq); ctx.translate(-545, -1440)
            draw(ctx, 545, FLOOR - 20 - 186 * 1.6 + 120 * sq, 1.6, -1, DAD,
                 P(torso=40 * sq, lhip=-70 * sq, lkn=110 * sq, rhip=-60 * sq, rkn=100 * sq, lsh=40, lel=-120, rsh=60, rel=-120,
                   eye='closed', mouth='wavy', head=-10))
            ctx.restore()
            # the part that doesn't fit yet
            if sq < 0.9:
                ellipse(ctx, 545, 1000 + 60 * sq, 70, 50); fl(ctx, DAD['shirt'], 7)
        else:
            jl = il - 34
            cab_door(ctx, 0.0, shirt=1.0 if jl < 8 else 0.0)
            if jl >= 8:
                puff(ctx, 420, 1210, pop(jl, 8, 16), 0.6)
        ctx.restore()
        if il < 12:
            label1(ctx, "*ZOOM!*", YEL, pop(il, 0, 3), 150, 0.04)
        elif not click_:
            label1(ctx, "*SQUEEEEEZE*", (1, 1, 1), pop(il, 12, 15), 124)
        else:
            label1(ctx, "*CLICK!*", YEL, pop(il, 34, 37), 150, -0.04)
    else:
        il = lf - 84
        cupboard_pov(ctx, f, il)
        label2(ctx, "\"He'll NEVER", "find me.\"", (1, 1, 1), pop(il, 2, 6), 120, col2=YEL)
    card(ctx, 'p3', f, 252, 330)


def s4(ctx, f):
    lf = f - 390
    # split screen: top = Dad in the cupboard, bottom = kid on the sofa
    ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
    ctx.save(); cam(ctx, 540, 900, 0.82, 0, 0, f, sy=560)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('120c1c')); ctx.fill()
    poly(ctx, [(560, -200), (620, -200), (760, 1500), (520, 1500)]); setc(ctx, (1, 0.95, 0.7, 0.1)); ctx.fill()
    face(ctx, DAD, P(eye='shock', mouth='flat', head=0), 520, 880, 250, -0.18)
    sweat(ctx, 760, 700, lf, 1.6)
    for kx in (300, 760):
        ellipse(ctx, kx, 1260, 150, 120); fl(ctx, DAD['pants'], 9)
    spider(ctx, 300, 520 + 140 * eout(pop(lf, 10, 40)), 1.3, lf)
    ctx.restore()
    ctx.restore()
    label1(ctx, "\"Any second now...\"", (1, 1, 1), pop(lf, 4, 8), 88, y=880)
    # bottom
    ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
    ctx.save(); cam(ctx, 520, 1180, 0.85, 0, 0, f, sy=1390)
    living(ctx, lights=True, tv=0.6 + 0.4 * math.sin(lf * 0.9))
    sofa_back(ctx)
    b = draw_hip(ctx, 500, SEAT, 1.35, 1, BOY, sit(eye='happy', mouth='grin', lsh=30, lel=-130, rsh=40, rel=-90))
    hx_, hy_ = b['front']
    ice_cream(ctx, hx_ + 10, hy_ - 40, 1.1, 0.1)
    sofa_front(ctx)
    ctx.restore()
    ctx.restore()
    ctx.rectangle(0, 952, W, 16); setc(ctx, (1, 1, 1)); ctx.fill()
    if lf >= 50:
        label2(ctx, "\"...wait, we were", "playing something?\"", YEL, pop(lf, 50, 54), 88, col2=(1, 1, 1), y=1420)
    card(ctx, 'p4', f, 392, 500)


def s5(ctx, f):
    lf = f - 500
    if lf < 50:
        cupboard_pov(ctx, f, lf, bearded=True)
        label1(ctx, "3 HOURS LATER...", (1, 1, 1), pop(lf, 0, 4), 96, 0.0, y=545)
        label2(ctx, "\"I... still...", "WIN.\"", (1, 1, 1), pop(lf, 14, 18), 120, col2=YEL)
        card(ctx, 'p5', f, 502, 548)
    elif lf < 125:
        il = lf - 50
        burst = il >= 18
        ctx.save(); cam(ctx, 540, 1150, 1.0 + 0.08 * eout(pop(il, 18, 30)), 0, shake_at(il, [18, 40], 14, 26), f)
        kitchen(ctx)
        if not burst:
            cab_door(ctx, eout(pop(il, 6, 16)))
            draw(ctx, 830, FLOOR - 186 * 1.6, 1.6, -1, MOM,
                 P(torso=20, lhip=-10, lkn=0, rhip=10, rkn=0, lsh=60, lel=-30, rsh=40, rel=-20, eye='normal', mouth='smile', head=10))
        else:
            jl = il - 18
            cab_door(ctx, 1.0)
            # Dad bursts out, beard and cobwebs
            up_ = eout(pop(jl, 0, 8))
            b = draw(ctx, 545, FLOOR - 186 * 1.6 - 120 * up_, 1.6, 1, DAD,
                     P(torso=0, lhip=-30, lkn=-20, rhip=30, rkn=-20, lsh=160, lel=-20, rsh=-160, rel=20, eye='shock', mouth='grin', head=0))
            hx_, hy_ = b['head']
            beard(ctx, hx_ + 10, hy_ + 20, b['R'], jl)
            cobweb(ctx, hx_ - 60, hy_ - 120, 0.7)
            draw(ctx, 860, FLOOR - 186 * 1.6, 1.6, -1, MOM,
                 P(torso=-10, lhip=-20, lkn=0, rhip=20, rkn=0, lsh=150, lel=-20, rsh=-150, rel=20, eye='shock', mouth='open', head=-6))
            if jl < 22:
                pan(ctx, 760, 900 + 600 * ein(pop(jl, 0, 22)), 1.0)
            else:
                pan(ctx, 760, FLOOR - 20, 1.0)
                stars_ko(ctx, 760, FLOOR - 120, jl * 0.2, 4, 90)
            mouse(ctx, 640, FLOOR - 4, 0.9, jl)
        ctx.restore()
        if not burst:
            label2(ctx, "\"Where's my", "big pan...?\"", (1, 1, 1), pop(il, 0, 4), 104, col2=YEL)
        elif il < 40:
            label1(ctx, "\"DID I WIN?!\"", YEL, pop(il, 18, 21), 150, -0.04)
        else:
            label2(ctx, "*CLANG!*", "\"AAAAAH!!\"", (1, 1, 1), pop(il, 40, 43), 130, col2=RED)
    else:
        il = lf - 125
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 625)


SHOTS = [(0, s1), (110, s2), (250, s3), (390, s4), (500, s5)]
CUTS = (50, 110, 180, 250, 284, 334, 390, 500, 550, 625)


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
                              "-i", "out/hideseek_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
