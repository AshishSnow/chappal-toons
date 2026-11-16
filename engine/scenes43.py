"""'The WHY? Phase' - original, general-audience comedy short, ~22s.
Hook: ECU of the kid, huge curious eyes, WHY? bubbles popping: "WHY?"
 -> kid tugs Dad on the sofa: "Dad, why is the sky blue?" Dad, confident: "EASY!"
Beat 1 (CHALKBOARD): Dad at a chalkboard draws the sun + light bouncing. Kid: "WHY?" Dad adds the Earth + air. "WHY?" "WHY?"
Beat 2 (THE UNIVERSE): fast board cuts - atoms, E=mc2, the galaxy, the BIG BANG... every answer gets "WHY?"; WHY? bubbles
 flood the room and bury Dad up to his neck.
Beat 3 (MELTDOWN): ECU Dad, eye twitching, steam, the chalk SNAPS -> red bg: "BECAUSE... I SAID SO!" Kid: "Okay!" skips off.
Twist: split-screen phone call. Dad: "Mom... why did YOU always say that?" Grandma: "BECAUSE I SAID SO." Dad's jaw drops,
 then the kid pops up behind him: "WHY?" -> loops to the opening ECU."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, living, sofa_back, sofa_front, SEAT, _SCR
from scenes8 import sit
from scenes14 import sweat
from scenes33 import vein, steam
from scenes25 import GRAN
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
CHALK = (0.96, 0.96, 0.92)
LY = 1450

CAPS = {
    'p1': [[("EVERY KID'S", OUT)], [("\"WHY?\" PHASE", PINK)]],
    'p2': [[("QUESTION 1:", OUT)], [("EASY!", GREEN)]],
    'p3': [[("QUESTION 87:", OUT)], [("THE ENTIRE UNIVERSE", PURPLE)]],
    'p4': [[("QUESTION 112:", OUT)], [("DAD'S FINAL ANSWER", RED)]],
    'p5': [[("PLOT TWIST:", OUT)], [("IT RUNS IN THE FAMILY", PINK)]],
}
scenes13.CAPS = CAPS
card = _card13


def hip(k):
    return FLOOR - 100 * k


# ------------------------------------------------------------------ props
def why_bubble(ctx, x, y, s, t, ang=0.0, col=PINK, txt="WHY?"):
    """pop-in speech bubble saying WHY?"""
    if t <= 0:
        return
    sc = s * (0.4 + 0.6 * eout(min(1, t * 1.6)) + 0.12 * math.sin(min(1, t) * math.pi))
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(sc, sc)
    poly(ctx, [(-40, 60), (-10, 60), (-70, 130)]); fl(ctx, (1, 1, 1), 7)
    ellipse(ctx, 0, 0, 170, 95); fl(ctx, (1, 1, 1), 8)
    poly(ctx, [(-38, 52), (-12, 52), (-62, 115)]); setc(ctx, (1, 1, 1)); ctx.fill()
    text(ctx, txt, 0, 4, 92, col, ow=0, shadow=False)
    ctx.restore()


def chalk_line(ctx, pts, w=8, a=1.0):
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    setc(ctx, CHALK + (a,)); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()


def chalk_text(ctx, s, x, y, size, col=CHALK, ang=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    text(ctx, s, 0, 0, size, col, ow=0, shadow=False)
    ctx.restore()


def board(ctx, x0, y0, w, h, stage, lf=0, draw_u=1.0):
    """green chalkboard on an easel. stage 0 sun, 1 + earth/air, 2 atoms+E=mc2, 3 galaxy/big bang, 4 total chaos"""
    # easel legs
    for dx, a in ((0.15, -0.12), (0.85, 0.12)):
        ctx.save(); ctx.translate(x0 + w * dx, y0 + h - 20); ctx.rotate(a)
        ctx.rectangle(-14, 0, 28, FLOOR - (y0 + h) + 40); fl(ctx, hx('9a5a2a'), 6); ctx.restore()
    rect_r(ctx, x0 - 26, y0 - 26, w + 52, h + 52, 18); fl(ctx, hx('b97a48'), 8)
    ctx.rectangle(x0, y0, w, h); fl(ctx, hx('2f5a44'), 6)
    ctx.save(); ctx.rectangle(x0, y0, w, h); ctx.clip()
    # chalk dust smudges
    for k in range(5):
        ellipse(ctx, x0 + w * (0.15 + 0.18 * k), y0 + h * (0.3 + 0.12 * (k % 3)), 90, 30); setc(ctx, (1, 1, 1, 0.05)); ctx.fill()
    u0 = draw_u if stage == 0 else 1.0
    # stage 0: sun + rays + arrows
    sx, sy = x0 + 120, y0 + 110
    ctx.new_path(); ctx.arc(sx, sy, 55, 0, 2 * math.pi * u0)
    setc(ctx, hx('ffe066')); ctx.set_line_width(9); ctx.stroke()
    for k in range(8):
        if k / 8 < u0:
            a = k * math.pi / 4
            chalk_line(ctx, [(sx + math.cos(a) * 75, sy + math.sin(a) * 75), (sx + math.cos(a) * 105, sy + math.sin(a) * 105)], 7)
    if u0 > 0.5:
        chalk_line(ctx, [(sx + 120, sy + 30), (sx + 230, sy + 90), (sx + 300, sy + 40), (sx + 380, sy + 110)], 6)
        chalk_line(ctx, [(sx + 360, sy + 85), (sx + 380, sy + 110), (sx + 352, sy + 116)], 6)
        chalk_text(ctx, "LIGHT!", sx + 250, sy - 30, 54, hx('ffe066'), -0.05)
    if stage >= 1:
        u1 = draw_u if stage == 1 else 1.0
        ex, ey = x0 + w - 150, y0 + h - 140
        ctx.new_path(); ctx.arc(ex, ey, 95, 0, 2 * math.pi * u1); setc(ctx, hx('7ad0ff')); ctx.set_line_width(9); ctx.stroke()
        if u1 > 0.6:
            ctx.new_path(); ctx.arc(ex, ey, 130, math.pi, 2 * math.pi); setc(ctx, CHALK + (0.8,)); ctx.set_line_width(5); ctx.set_dash([14, 12]); ctx.stroke(); ctx.set_dash([])
            chalk_text(ctx, "AIR", ex - 170, ey - 120, 46, CHALK, 0.1)
            chalk_line(ctx, [(ex - 30, ey - 30), (ex + 20, ey - 10), (ex - 10, ey + 30), (ex + 40, ey + 40)], 6)
    if stage >= 2:
        ax, ay = x0 + 150, y0 + h - 130
        for k in range(3):
            ellipse(ctx, ax, ay, 90, 30, k * math.pi / 3 + lf * 0.05); setc(ctx, CHALK); ctx.set_line_width(5); ctx.stroke()
        ellipse(ctx, ax, ay, 14, 14); setc(ctx, hx('ff8aa8')); ctx.fill()
        chalk_text(ctx, "E = mc²", x0 + w * 0.5, y0 + h * 0.5, 74, hx('ffb0d0'), -0.06)
    if stage >= 3:
        gx, gy = x0 + w * 0.55, y0 + 120
        ctx.new_path()
        for i in range(160):
            t = i / 160 * 4 * math.pi
            r = 6 + t * 7
            px, py = gx + math.cos(t + lf * 0.08) * r, gy + math.sin(t + lf * 0.08) * r * 0.55
            (ctx.move_to if i == 0 else ctx.line_to)(px, py)
        setc(ctx, hx('c8a8ff')); ctx.set_line_width(6); ctx.stroke()
        chalk_text(ctx, "BIG BANG?!", gx + 10, gy + 110, 52, hx('ffe066'), 0.06)
    if stage >= 4:
        rnd = random.Random(9)
        for k in range(16):
            px, py = x0 + rnd.uniform(40, w - 40), y0 + rnd.uniform(40, h - 40)
            chalk_text(ctx, rnd.choice(("?", "??", "?!", "WHY", "π", "∞")), px, py, rnd.uniform(40, 70), CHALK, rnd.uniform(-0.4, 0.4))
        for k in range(6):
            pts = [(x0 + rnd.uniform(0, w), y0 + rnd.uniform(0, h)) for _ in range(4)]
            chalk_line(ctx, pts, 4, 0.6)
    ctx.restore()
    # chalk tray
    ctx.rectangle(x0 - 10, y0 + h + 18, w + 20, 20); fl(ctx, hx('9a5a2a'), 5)


def phone(ctx, x, y, s, ang=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s)
    rect_r(ctx, -45, -90, 90, 180, 18); fl(ctx, hx('2a2a3a'), 6)
    rect_r(ctx, -34, -74, 68, 140, 8); setc(ctx, hx('7ad0ff')); ctx.fill()
    ctx.restore()


def chalk_piece(ctx, x, y, a, broken=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    if broken <= 0:
        rect_r(ctx, -40, -11, 80, 22, 8); fl(ctx, (1, 1, 1), 4)
    else:
        for sgn in (-1, 1):
            ctx.save(); ctx.translate(sgn * (22 + 60 * broken), -40 * broken); ctx.rotate(sgn * 1.5 * broken)
            rect_r(ctx, -20, -11, 40, 22, 6); fl(ctx, (1, 1, 1), 4); ctx.restore()
        for k in range(8):
            ang = k * math.pi / 4
            ellipse(ctx, math.cos(ang) * 70 * broken, math.sin(ang) * 70 * broken, 8 * (1 - broken) + 2, 8 * (1 - broken) + 2)
            setc(ctx, (1, 1, 1, 0.8)); ctx.fill()
    ctx.restore()


def label2(ctx, a, b, col, t, size=104, col2=None, y=LY):
    label(ctx, a, 540, y - 60, size, col, -0.03, t)
    label(ctx, b, 540, y + 50, size, col2 or col, 0.02, t)


def flash(ctx, u):
    if 0 <= u < 1:
        ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.95 * (1 - u) ** 1.5)); ctx.fill()


# ------------------------------------------------------------------ opening
OPEN_BUBBLES = ((250, 640, -0.2, 0), (850, 700, 0.18, 4), (200, 1260, 0.15, 8), (880, 1290, -0.15, 12))


def opening_face(ctx, f, lf, lab=True):
    sh = shake_at(lf, [0], 10, 18) + 3
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 40)), 0, sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd23f')); ctx.fill()
    rays(ctx, 540, 980, 240, 1700, lf * 0.04, col=(1, 1, 1), a=0.45, n=18)
    cx, cy = 540, 990 + 10 * math.sin(lf * 0.5)
    face(ctx, BOY, P(eye='shock', mouth='open', head=0), cx, cy, 290, 0.06 * math.sin(lf * 0.4))
    for k in range(3):
        sparkle(ctx, cx - 120 + 240 * k / 2, cy - 330 - 30 * (k % 2), 30 + 8 * math.sin(lf * 0.6 + k))
    ctx.restore()
    for (bx, by, a, d) in OPEN_BUBBLES:
        why_bubble(ctx, bx, by, 0.75, pop(lf, d, d + 6) if lf > 0 else 1, a, [PINK, BLUE, PURPLE, ORANGE][d // 4])
    if lab:
        label(ctx, "\"WHY?\"", 540, LY + 20, 170, YEL, -0.04, pop(lf, 0, 4) if lf > 0 else 1)


# ------------------------------------------------------------------ shots
BX0, BY0, BW, BH = 120, 560, 840, 460


def board_room(ctx, f, stage, lf, draw_u=1.0, z=1.0, cx=540, cy=1000, shake=0, dad_p=None, kid_p=None, dad_extra=None, kid_x=250):
    ctx.save(); cam(ctx, cx, cy, z, 0, shake, f)
    living(ctx)
    board(ctx, BX0, BY0, BW, BH, stage, lf, draw_u)
    bd = draw_hip(ctx, 810, hip(1.22) - 10, 1.22, -1, DAD, dad_p or P(eye='happy', mouth='grin', rsh=150, rel=20, lsh=-30, lel=-40, head=-4))
    if dad_extra:
        dad_extra(ctx, bd)
    bk = draw_hip(ctx, kid_x, hip(0.9) - 10, 0.9, 1, BOY, kid_p or P(eye='shock', mouth='open', rsh=160, rel=10, lsh=-20, lel=-30, head=-8))
    ctx.restore()
    return bd, bk


def s1(ctx, f):
    if f < 45:
        opening_face(ctx, f, f)
    else:
        lf = f - 45
        ctx.save(); cam(ctx, 560, 1120, 1.05 + 0.08 * eout(pop(lf, 0, 60)), 0, shake_at(lf, [0, 35], 6, 8), f)
        living(ctx)
        sofa_back(ctx)
        confident = lf >= 35
        bd = draw_hip(ctx, 640, SEAT, 1.15, -1, DAD, sit(eye='happy' if confident else 'normal', mouth='grin' if confident else 'smile', head=-4,
                                                        rsh=150 if confident else 70, rel=10 if confident else -90, lsh=60, lel=-90))
        sofa_front(ctx)
        tug = 10 * math.sin(lf * 1.2) if lf < 35 else 0
        draw_hip(ctx, 300 + tug, hip(0.9) - 10, 0.9, 1, BOY, P(eye='shock', mouth='open', rsh=80, rel=-20, lsh=-20, lel=-30, head=-6))
        if confident:
            hx_, hy_ = bd['head']
            for k in range(3):
                sparkle(ctx, hx_ - 90 + 90 * k, hy_ - 200 - 20 * (k % 2), 26 * eout(pop(lf, 35, 42)))
        ctx.restore()
        if lf < 35:
            label2(ctx, "\"Dad, why is", "the sky BLUE?\"", (1, 1, 1), pop(lf, 0, 4), 100)
        else:
            label(ctx, "\"EASY! Watch this.\"", 540, LY + 40, 110, YEL, -0.03, pop(lf, 35, 39))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 50:
        # Dad draws the sun
        def chalk(c, bd):
            fx, fy = bd['front']
            chalk_piece(c, fx - 10, fy - 30 + 8 * math.sin(lf * 1.3), -0.6)
        board_room(ctx, f, 0, lf, draw_u=pop(lf, 0, 34), z=1.0 + 0.04 * eout(pop(lf, 0, 50)), dad_extra=chalk,
                   kid_p=P(eye='normal', mouth='smile', rsh=10, rel=-10, lsh=-10, lel=-10, head=-6))
        label(ctx, "\"The SUN sends LIGHT...\"", 540, LY + 40, 100, (1, 1, 1), 0.03, pop(lf, 0, 4))
    elif lf < 70:
        il = lf - 50
        board_room(ctx, f, 0, lf, z=1.08, shake=shake_at(il, [0], 8, 12))
        why_bubble(ctx, 330, 940, 1.1, pop(il, 0, 6), -0.12)
    elif lf < 115:
        il = lf - 70
        def chalk(c, bd):
            fx, fy = bd['front']
            chalk_piece(c, fx - 10, fy - 30 + 8 * math.sin(il * 1.3), -0.6)
        board_room(ctx, f, 1, lf, draw_u=pop(il, 0, 30), z=1.08 + 0.04 * eout(pop(il, 0, 45)), dad_extra=chalk,
                   dad_p=P(eye='normal', mouth='open', rsh=150, rel=20, lsh=-30, lel=-40, head=-4))
        label(ctx, "\"...it bounces off the AIR!\"", 540, LY + 40, 96, (1, 1, 1), -0.03, pop(il, 0, 4))
    else:
        il = lf - 115
        def sw(c, bd):
            hx_, hy_ = bd['head']
            sweat(c, hx_ + 120, hy_ - 120, il * 3, 1.0)
        board_room(ctx, f, 1, lf, z=1.2 + 0.1 * eout(pop(il, 0, 25)), cx=520, cy=1020, shake=shake_at(il, [0, 10], 8, 12), dad_extra=sw,
                   dad_p=P(eye='shock', mouth='flat', rsh=60, rel=-40, lsh=-30, lel=-40, head=-4))
        why_bubble(ctx, 300, 900, 1.0, pop(il, 0, 5), -0.15)
        why_bubble(ctx, 380, 700, 0.9, pop(il, 10, 15), 0.12, BLUE)
    card(ctx, 'p2', f, 112, 246)


STAGES = ((0, 2, "\"ATOMS! Tiny dots!\""), (24, 2, None), (40, 3, "\"The BIG BANG!\""), (64, 3, None), (80, 4, "\"...SPACE... TIME...\""))


def s3(ctx, f):
    lf = f - 250
    if lf < 100:
        # rapid board cuts, each answered with WHY?
        idx = [i for i, (st, _, _) in enumerate(STAGES) if st <= lf][-1]
        st, stage, line = STAGES[idx]
        il = lf - st
        if line is None:
            # low-angle kid: WHY?
            ctx.save(); cam(ctx, 300, 1180, 1.6, -6 if idx == 1 else 6, shake_at(il, [0], 8, 14), f, sy=1150)
            living(ctx)
            board(ctx, BX0, BY0, BW, BH, stage, lf)
            draw_hip(ctx, 300, hip(0.9) - 10, 0.9, 1, BOY, P(eye='shock', mouth='scream', rsh=160, rel=10, lsh=-160, lel=-10, head=-10))
            ctx.restore()
            why_bubble(ctx, 560 if idx == 1 else 520, 760, 1.3, pop(il, 0, 5), 0.1 if idx == 1 else -0.1, BLUE if idx == 1 else ORANGE)
        else:
            frazz = idx / 4

            def ex(c, bd):
                hx_, hy_ = bd['head']
                fx, fy = bd['front']
                chalk_piece(c, fx - 10, fy - 30 + 10 * math.sin(lf * 2.1), -0.6)
                sweat(c, hx_ + 120, hy_ - 120, lf * 3, 1.0 + frazz * 0.3)
                if idx >= 2:
                    steam(c, hx_ - 160, hy_ - 40, lf * 2, 0.9, -1)
            dad_p = P(eye='shock' if idx >= 2 else 'normal', mouth='scream' if idx == 4 else 'open', rsh=150, rel=20 + 20 * math.sin(lf), lsh=-30, lel=-40, head=-4 + 4 * math.sin(lf * 0.7))
            board_room(ctx, f, stage, lf, draw_u=pop(il, 0, 18), z=1.0 + 0.05 * idx, shake=shake_at(il, [0], 6, 10) + 2 * idx, dad_extra=ex, dad_p=dad_p)
            label(ctx, line, 540, LY + 40, 100, (1, 1, 1), 0.03 * (-1) ** idx, pop(il, 0, 4))
    else:
        # WHY? bubbles flood the room and bury Dad
        il = lf - 100
        lvl = eout(pop(il, 0, 30))
        ctx.save(); cam(ctx, 560, 1000, 1.0, 0, 3 + shake_at(il, [0], 8, 10), f)
        living(ctx)
        board(ctx, BX0, BY0, BW, BH, 4, lf)
        draw_hip(ctx, 790, hip(1.22) - 10, 1.22, -1, DAD, P(eye='shock', mouth='scream', rsh=160, rel=10, lsh=-160, lel=-10, head=0))
        rnd = random.Random(4)
        top = FLOOR - 820 * lvl
        for k in range(40):
            bx = rnd.uniform(-60, 1140); by = rnd.uniform(top, FLOOR + 200); d = rnd.uniform(0, 14)
            why_bubble(ctx, bx, by, rnd.uniform(0.5, 0.8), pop(il, d, d + 5), rnd.uniform(-0.4, 0.4), rnd.choice((PINK, BLUE, PURPLE, ORANGE, GREEN)))
        ctx.restore()
        label(ctx, "*WHY? WHY? WHY? WHY?*", 540, LY + 40, 96, YEL, -0.03, pop(il, 0, 4))
    card(ctx, 'p3', f, 252, 386)


def s4(ctx, f):
    lf = f - 390
    if lf < 35:
        # ECU Dad: twitching eye, steam, chalk snaps
        sh = 2 + (shake_at(lf, [22], 10, 20))
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.12 * eout(pop(lf, 0, 35)), 0, sh, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('2f5a44')); ctx.fill()
        rays(ctx, 540, 980, 240, 1700, lf * 0.02, col=(1, 1, 1), a=0.12, n=18)
        tw = 'closed' if (lf // 3) % 3 == 0 else 'shock'
        face(ctx, DAD, P(eye=tw, mouth='wavy', head=0), 540, 980, 300, 0.02 * math.sin(lf * 3))
        steam(ctx, 240, 960, lf * 2, 1.2, -1); steam(ctx, 850, 960, lf * 2 + 7, 1.2, 1)
        vein(ctx, 710, 770, 1.2 + 0.2 * math.sin(lf))
        chalk_piece(ctx, 800, 1230, -0.4, eout(pop(lf, 22, 32)))
        ctx.restore()
        if lf < 22:
            label(ctx, "*twitch... twitch...*", 540, LY + 40, 100, (1, 1, 1), 0.03, pop(lf, 0, 4))
        else:
            label(ctx, "*SNAP!*", 540, LY + 40, 150, YEL, -0.05, pop(lf, 22, 25))
    elif lf < 80:
        il = lf - 35
        ctx.save(); cam(ctx, 540, 1000, 1.08 + 0.06 * eout(pop(il, 0, 45)), 0, 6 + shake_at(il, [0, 14], 12, 26), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff3b3b')); ctx.fill()
        rays(ctx, 540, 980, 240, 1700, il * 0.06, col=(1, 0.85, 0.3), a=0.5, n=18)
        face(ctx, DAD, P(eye='glare', mouth='scream', head=0), 540 + 6 * math.sin(il * 2.5), 960, 300)
        steam(ctx, 240, 940, il * 3, 1.4, -1); steam(ctx, 850, 940, il * 3 + 7, 1.4, 1)
        ctx.restore()
        label2(ctx, "\"BECAUSE...", "I SAID SO!!!\"", YEL, pop(il, 0, 4) if il < 14 else 1, 124, col2=(1, 1, 1))
    else:
        il = lf - 80
        ctx.save(); cam(ctx, 560, 1010, 1.05, 0, shake_at(il, [0], 6, 8), f)
        living(ctx)
        board(ctx, BX0, BY0, BW, BH, 4, lf)
        draw_hip(ctx, 810, hip(1.22) - 10, 1.22, -1, DAD, P(eye='closed', mouth='wavy', rsh=10, rel=0, lsh=-10, lel=0, head=10, torso=10))
        kx = 300 - 500 * eout(pop(il, 10, 30))
        hop = -40 * abs(math.sin(il * 0.45))
        draw_hip(ctx, kx, hip(0.9) - 10 + hop, 0.9, -1 if il >= 10 else 1, BOY, P(eye='happy', mouth='grin', rsh=160, rel=0, lsh=-40, lel=-30, head=6,
                                                                              lhip=25 * math.sin(il * 0.45), rhip=-25 * math.sin(il * 0.45)))
        ctx.restore()
        label(ctx, "\"Okay!\" *skip skip*", 540, LY + 40, 110, hx('7dff9a'), 0.03, pop(il, 0, 4))
    card(ctx, 'p4', f, 392, 496)


def s5(ctx, f):
    lf = f - 500
    if lf < 130:
        # split screen phone call: Grandma (top) / Dad (bottom)
        gran_on = lf >= 45
        ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
        cam(ctx, 540, 640, 1.0 + 0.06 * eout(pop(lf, 45, 90)), 0, shake_at(lf, [45], 10, 16), f, sy=620)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff9ac8') if gran_on else hx('ffc8e0')); ctx.fill()
        rays(ctx, 540, 660, 200, 1200, lf * 0.03, col=(1, 1, 1), a=0.35 if gran_on else 0.15, n=16)
        gx, gy = 500, 690
        face(ctx, GRAN, P(eye='glare' if gran_on else 'happy', mouth='open' if gran_on else 'smile', head=0), gx, gy, 200)
        phone(ctx, gx + 240, gy + 30, 1.1, 0.25)
        ctx.restore()
        ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
        jaw = gran_on
        cam(ctx, 540, 1250, 1.0 + 0.05 * eout(pop(lf, 0, 40)), 0, shake_at(lf, [48], 10, 18), f, sy=1250)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('9fd8ff')); ctx.fill()
        rays(ctx, 540, 1250, 200, 1200, -lf * 0.02, col=(1, 1, 1), a=0.3, n=16)
        dx, dy = 560, 1230
        face(ctx, DAD, P(eye='shock' if jaw else 'normal', mouth='scream' if jaw else 'open', head=0), dx, dy, 200)
        phone(ctx, dx - 250, dy + 30, 1.1, -0.25)
        if lf >= 95:
            # kid pops up behind Dad's shoulder
            u = eout(pop(lf, 95, 103))
            face(ctx, BOY, P(eye='shock', mouth='open', head=0), 870, 1460 - 260 * u, 130, -0.15)
        ctx.restore()
        ctx.rectangle(0, 952, W, 16); setc(ctx, OUT); ctx.fill()
        if lf < 45:
            label2(ctx, "\"Mom... why did YOU", "always say that?\"", (1, 1, 1), pop(lf, 0, 4), 92)
        elif lf < 95:
            label2(ctx, "\"BECAUSE", "I SAID SO.\"", YEL, pop(lf, 45, 49), 120, col2=PINK)
        else:
            why_bubble(ctx, 820, 1120, 0.8, pop(lf, 100, 105), 0.15)
            label(ctx, "\"...WHY?\"", 540, LY + 40, 130, YEL, -0.03, pop(lf, 100, 104))
    else:
        il = lf - 130
        opening_face(ctx, f, il)
    if lf < 128:
        card(ctx, 'p5', f, 502, 626)
    else:
        card(ctx, 'p1', f, 630)


SHOTS = [(0, s1), (110, s2), (250, s3), (390, s4), (500, s5)]
CUTS = (45, 110, 160, 180, 225, 250, 274, 290, 314, 330, 350, 390, 425, 470, 500, 545, 630)


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
                              "-i", "out/why_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
