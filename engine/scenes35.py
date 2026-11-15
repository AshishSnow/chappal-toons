"""'The Box Wins' - original, general-audience comedy short, ~22s.
Hook: ECU of Dad, huge proud grin: "HAPPY BIRTHDAY, CHAMP!!" -> kid rips the paper, a shiny robot pops out: "IT DOES 47 THINGS!"
Beat 1: kid holds the robot... his eyes drift to the empty BOX. Heavenly choir. Robot dropped: CLUNK. Kid dives into the box.
Beat 2: the box is a race car, a rocket, a pirate ship. The robot sits alone in the corner: *sad beep*.
Beat 3: Dad makes the robot dance - the box just closes its flaps ("DO NOT DISTURB"). Dad ECU: "...it was SO expensive."
Twist: that night the box goes VROOM VROOM - it's DAD in the box, with a crayon steering wheel. Kid catches him.
"...it's a REALLY good box." Loops to the opening ECU."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, living
from scenes34 import present, dark_bg
import scenes13
from scenes13 import card as _card13
import random

BOY = doodle.BOY
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
CARD = hx('d9a066')
CARD_D = hx('b07a44')
LY = 1450

CAPS = {
    'p1': [[("WHEN YOU BUY THE", OUT)], [("MOST EXPENSIVE TOY", RED)]],
    'p2': [[("AND THEY PICK...", OUT)], [("THE BOX", ORANGE)]],
    'p3': [[("THE BOX IS NOW:", OUT)], [("EVERYTHING", PURPLE)]],
    'p4': [[("DAD TRIES TO", OUT)], [("WIN THEM BACK", BLUE)]],
    'p5': [[("THAT NIGHT...", OUT)], [("WHO'S IN THE BOX?", GREEN)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def box_back(ctx, x, top, w=560, h=330, flap=1.0):
    """inside back wall + back flap of an open cardboard box; front face top edge at y=top"""
    d = 60   # perspective depth
    poly(ctx, [(x - w / 2, top), (x - w / 2 + 40, top - d), (x + w / 2 - 40, top - d), (x + w / 2, top)]); fl(ctx, CARD_D, 8)
    # back flap (stands up)
    ctx.save(); ctx.translate(x, top - d); ctx.scale(1, max(0.02, flap))
    poly(ctx, [(-w / 2 + 40, 0), (-w / 2 + 60, -150), (w / 2 - 60, -150), (w / 2 - 40, 0)]); fl(ctx, CARD, 7)
    ctx.restore()


def box_front(ctx, x, top, w=560, h=330, flap=1.0, closed=0.0, doodles=None, sign=None):
    d = 60
    # side flaps: open outward (flap=1) or folded over (closed=1)
    for sg in (-1, 1):
        ox = x + sg * w / 2
        ang = sg * (0.35 + 0.0 * flap) * (1 - closed) + sg * (-math.pi * 0.5) * closed
        ctx.save(); ctx.translate(ox, top - d / 2); ctx.rotate(-ang if sg < 0 else ang)
        if sg < 0:
            poly(ctx, [(0, 0), (0, -d / 2), (-170, -d / 2 - 30), (-170, 30)])
        else:
            poly(ctx, [(0, 0), (0, -d / 2), (170, -d / 2 - 30), (170, 30)])
        fl(ctx, CARD, 7); ctx.restore()
    rect_r(ctx, x - w / 2, top, w, h, 8); fl(ctx, CARD, 9)
    ctx.rectangle(x - 40, top, 80, h * 0.35); setc(ctx, hx('e8c48a')); ctx.fill()            # tape
    ctx.move_to(x - w / 2 + 30, top + h - 40); ctx.line_to(x - w / 2 + 110, top + h - 40); setc(ctx, CARD_D); ctx.set_line_width(6); ctx.stroke()
    # 'this way up' arrows
    for k in (-1, 1):
        ax = x + k * 0.33 * w; ay = top + h * 0.35
        poly(ctx, [(ax, ay - 30), (ax + 22, ay), (ax + 8, ay), (ax + 8, ay + 26), (ax - 8, ay + 26), (ax - 8, ay), (ax - 22, ay)]); setc(ctx, CARD_D); ctx.fill()
    if doodles == 'car':   # crayon wheels + headlight
        for k in (-1, 1):
            ellipse(ctx, x + k * w * 0.32, top + h, 70, 70); fl(ctx, hx('2a2a3a'), 8)
            ellipse(ctx, x + k * w * 0.32, top + h, 26, 26); fl(ctx, hx('c8c8d8'), 5)
        ellipse(ctx, x + w / 2 - 20, top + h * 0.6, 30, 30); fl(ctx, YEL, 6)
        text(ctx, "7", x, top + h * 0.68, 140, RED, ow=8, shadow=False)
    elif doodles == 'rocket':
        for k in (-1, 1):
            poly(ctx, [(x + k * w / 2, top + h * 0.3), (x + k * (w / 2 + 110), top + h + 60), (x + k * w / 2, top + h)]); fl(ctx, RED, 8)
        ellipse(ctx, x, top + h * 0.6, 60, 60); fl(ctx, hx('9fe6ff'), 7)
    elif doodles == 'ship':
        text(ctx, "ARRR", x, top + h * 0.72, 110, hx('2a2a3a'), outline=CARD, ow=2, shadow=False)
    if sign:
        ctx.save(); ctx.translate(x, top + h * 0.62); ctx.rotate(-0.06)
        ctx.rectangle(-230, -60, 460, 120); fl(ctx, (1, 1, 1), 6)
        text(ctx, sign, 0, 18, 50, RED, outline=(1, 1, 1), ow=2, shadow=False)
        ctx.restore()


def robot(ctx, x, y, s=1.0, lf=0, mood='happy', rot=0.0, arms=0.0):
    """shiny toy robot, original design. (x, y) = bottom centre (tread contact)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    # treads
    rect_r(ctx, -110, -60, 220, 60, 28); fl(ctx, hx('3a3a4a'), 7)
    for k in range(5):
        ellipse(ctx, -80 + k * 40, -30, 13, 13); setc(ctx, hx('8a8a9a')); ctx.fill()
    # arms
    for sg in (-1, 1):
        a = sg * (0.4 + 1.2 * arms * (0.5 + 0.5 * math.sin(lf * 0.6 + sg)))
        ctx.save(); ctx.translate(sg * 95, -190); ctx.rotate(-a if sg < 0 else a)
        ctx.rectangle(-12, 0, 24, 110); fl(ctx, hx('c8d0e0'), 6)
        ctx.new_path(); ctx.arc(0, 128, 26, -0.3, math.pi + 0.3); fl(ctx, hx('ff8a1f'), 6)
        ctx.restore()
    # body
    rect_r(ctx, -100, -250, 200, 200, 30); fl(ctx, hx('5ab4ff'), 8)
    rect_r(ctx, -60, -215, 120, 70, 14); fl(ctx, hx('1d2650'), 5)
    for k in range(3):   # blinking chest lights
        on = (lf // 6 + k) % 3 == 0 and mood != 'sad'
        ellipse(ctx, -36 + k * 36, -180, 14, 14); setc(ctx, (RED, YEL, hx('3cff8a'))[k] if on else hx('3a4060')); ctx.fill()
    # head
    rect_r(ctx, -90, -410, 180, 150, 34); fl(ctx, hx('c8d0e0'), 8)
    rect_r(ctx, -66, -385, 132, 100, 22); fl(ctx, hx('15183a'), 5)
    ec = hx('3cf0ff')
    for sg in (-1, 1):
        ex, ey = sg * 30, -335
        if mood == 'sad':
            ctx.new_path(); ctx.arc(ex, ey - 6, 14, 0.2, math.pi - 0.2); setc(ctx, ec); ctx.set_line_width(7); ctx.stroke()
            ellipse(ctx, ex + 8, ey + 30 + (lf % 24) * 1.5, 6, 9); setc(ctx, hx('3cf0ff')); ctx.fill()   # tear
        elif mood == 'love':
            sparkle(ctx, ex, ey, 20, hx('ff5fa8'))
        else:
            ellipse(ctx, ex, ey, 14, 18); setc(ctx, ec); ctx.fill()
    if mood != 'sad':
        ctx.new_path(); ctx.arc(0, -318, 16, 0.3, math.pi - 0.3); setc(ctx, ec); ctx.set_line_width(5); ctx.stroke()
    # antenna
    ctx.move_to(0, -410); ctx.line_to(0, -460); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 0, -470, 18, 18); fl(ctx, RED if (lf // 8) % 2 == 0 or mood == 'sad' else YEL, 5)
    ctx.restore()


def scrap(ctx, x, y, a, col, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-50, -30), (40, -40), (55, 20), (-10, 35), (-45, 15)]); fl(ctx, col, 5)
    ctx.move_to(-30, -25); ctx.line_to(35, 15); setc(ctx, YEL); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()


def party(ctx, lf=0):
    """living room + party bits"""
    living(ctx, True)
    for k in range(9):   # bunting
        x = 40 + k * 120
        poly(ctx, [(x, 560), (x + 110, 560), (x + 55, 650)]); fl(ctx, (RED, YEL, BLUE, PINK, GREEN)[k % 5], 5)
    ctx.move_to(-100, 560); ctx.line_to(1200, 560); ink(ctx, 5); ctx.stroke()
    for k, (bx, col) in enumerate(((240, RED), (380, BLUE), (650, YEL))):   # balloons
        by = 780 + 12 * math.sin(lf * 0.1 + k)
        ctx.move_to(bx, by + 90); ctx.curve_to(bx - 20, by + 200, bx + 20, by + 260, bx, by + 360); ink(ctx, 3); ctx.stroke()
        ellipse(ctx, bx, by, 66, 82); fl(ctx, col, 6)
        ellipse(ctx, bx - 22, by - 30, 12, 20); setc(ctx, (1, 1, 1, 0.6)); ctx.fill()


def kid_in_box(ctx, x, top, k, p, lift=0.0):
    """kid sitting in the box: legs hidden by the front face. returns body dict"""
    return draw_hip(ctx, x, top + 80 - lift, k, 1, BOY, p)


def party_hat(ctx, b, s=1.0, col=PINK):
    hx_, hy_ = b['head']; R = b['R']
    poly(ctx, [(hx_ - 0.45 * R, hy_ - 0.75 * R), (hx_ + 0.45 * R, hy_ - 0.75 * R), (hx_ + 0.05 * R, hy_ - 1.8 * R)]); fl(ctx, col, 6)
    ellipse(ctx, hx_ + 0.05 * R, hy_ - 1.82 * R, 0.16 * R, 0.16 * R); fl(ctx, YEL, 5)


# ------------------------------------------------------------------ shots
def opening_face(ctx, f, lf, lab=True):
    """ECU: Dad, proud as can be, holding up the big present"""
    sh = shake_at(lf, [0], 10, 20) + 2
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(lf, 0, 50)), 0, sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffcc3c')); ctx.fill()
    rays(ctx, 540, 960, 260, 1500, lf * 0.02, col=(1, 1, 1), a=0.45, n=18)
    cx, cy, Rt = 540, 900 + 6 * math.sin(lf * 0.5), 300
    face(ctx, DAD, P(eye='happy', mouth='grin', head=0), cx, cy, Rt, 0.04 * math.sin(lf * 0.3))
    present(ctx, 540, 1330, 380, 170, 0.0, BLUE, YEL)
    for k in range(5):
        sparkle(ctx, cx + 440 * math.cos(lf * 0.1 + k * 1.25), cy + 400 * math.sin(lf * 0.1 + k * 1.25), 28, (1, 1, 1))
    ctx.restore()
    if lab:
        label(ctx, "\"HAPPY BIRTHDAY!!\"", 540, LY + 30, 112, RED, -0.04, pop(lf, 0, 4) if lf > 0 else 1)


def s1(ctx, f):
    if f < 50:
        opening_face(ctx, f, f)
    else:
        lf = f - 50
        # wide: kid rips the paper, robot pops out of the box
        rip = eout(pop(lf, 0, 12)); rise = eout(pop(lf, 12, 26))
        ctx.save(); cam(ctx, 540, 1080, 0.9 + 0.05 * eout(pop(lf, 10, 60)), -2, shake_at(lf, [0, 14], 8, 16), f)
        party(ctx, lf)
        top = 1130
        box_back(ctx, 600, top, 460, 300, rise)
        if rise > 0:
            g = cairo.RadialGradient(600, top - 150, 20, 600, top - 150, 420)
            g.add_color_stop_rgba(0, 1, 1, 0.7, 0.8 * rise); g.add_color_stop_rgba(1, 1, 1, 0.7, 0)
            ctx.set_source(g); ellipse(ctx, 600, top - 150, 420, 420); ctx.fill()
            robot(ctx, 600, top + 120 - 250 * rise, 0.9, lf, 'happy', 0, 1.0)
        box_front(ctx, 600, top, 460, 300)
        if rip < 1:
            ctx.save(); ctx.translate(600, top + 50); ctx.scale(1 - 0.6 * rip, 1)
            ctx.rectangle(-240, -230, 480, 450); fl(ctx, RED, 8)
            ctx.rectangle(-30, -230, 60, 450); setc(ctx, YEL); ctx.fill()
            ctx.restore()
        rnd = random.Random(3)
        for k in range(10):   # paper scraps flying
            t = pop(lf, 2, 40)
            if 0 < t < 1:
                a = rnd.uniform(-2.6, -0.5)
                scrap(ctx, 600 + math.cos(a) * 900 * t, top + math.sin(a) * 700 * t + 900 * t * t, lf * 0.3 + k, RED if k % 2 else YEL, 0.9)
        kp = P(eye='shock', mouth='open', rsh=-150, rel=-20, lsh=150, lel=20)
        b = draw_hip(ctx, 210, FLOOR - 150, 1.05, 1, BOY, kp)
        party_hat(ctx, b)
        ctx.restore()
        if lf < 22:
            label(ctx, "*RIIIIIP!*", 540, LY, 120, YEL, 0.04, pop(lf, 1, 5))
        else:
            label(ctx, "\"IT DOES 47 THINGS!\"", 540, LY, 96, (1, 1, 1), -0.03, pop(lf, 22, 26))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 40:
        # kid holds robot, but his gaze drifts... (push-in)
        ctx.save(); cam(ctx, 540, 1040, 1.0 + 0.1 * eout(pop(lf, 0, 40)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('6fd6c8')); ctx.fill()
        drift = eout(pop(lf, 10, 30))
        face(ctx, BOY, P(eye='normal', mouth='flat', head=0), 380 - 40 * drift, 900, 270, -0.05 - 0.1 * drift, 1)
        robot(ctx, 250, 1310, 0.62, lf, 'happy', 0.0, 0.7)
        # arrow of attention
        if drift > 0.2:
            for k in range(3):
                sparkle(ctx, 760 + 70 * k, 760 + 30 * k, 18 * drift, YEL)
        ctx.restore()
        label(ctx, "*BEEP BOOP!*", 540, LY, 100, hx('3cf0ff'), 0.03, pop(lf, 2, 6))
        # the box, peeking in from the right edge of frame
        ctx.save(); ctx.translate(980 - 60 * drift, 1180); ctx.rotate(-0.2)
        ctx.rectangle(-60, -100, 200, 200); fl(ctx, CARD, 8)
        ctx.restore()
    elif lf < 80:
        il = lf - 40
        # heavenly box
        ctx.save(); cam(ctx, 540, 1060, 1.05 + 0.08 * eout(pop(il, 0, 40)), 0, shake_at(il, [0], 6, 10), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffe9a0')); ctx.fill()
        rays(ctx, 540, 1000, 160, 1600, il * 0.03, col=(1, 1, 1), a=0.8, n=20)
        g = cairo.RadialGradient(540, 1000, 40, 540, 1000, 520)
        g.add_color_stop_rgba(0, 1, 1, 1, 0.9); g.add_color_stop_rgba(1, 1, 1, 1, 0)
        ctx.set_source(g); ellipse(ctx, 540, 1000, 520, 520); ctx.fill()
        bob = 14 * math.sin(il * 0.25)
        box_back(ctx, 540, 1040 + bob, 520, 300)
        box_front(ctx, 540, 1040 + bob, 520, 300)
        for k in range(6):
            sparkle(ctx, 540 + 400 * math.cos(il * 0.12 + k * 1.05), 1080 + 300 * math.sin(il * 0.12 + k * 1.05), 30, (1, 1, 1))
        ctx.restore()
        label(ctx, "*AAAAHHH~*", 540, LY, 116, hx('ffb000'), 0.03, pop(il, 2, 6))
    else:
        il = lf - 80
        # drop the robot (CLUNK) and dive into the box
        ctx.save(); cam(ctx, 540, 1080, 0.92, 0, shake_at(il, [6, 20], 10, 20), f)
        party(ctx, il)
        top = 1150
        box_back(ctx, 620, top, 500, 300)
        dive = eout(pop(il, 10, 22))
        if il < 10:
            kp = P(eye='shock', mouth='grin', rsh=-100, rel=-30, lsh=100, lel=30, lhip=-30, lkn=40, rhip=30, rkn=10)
            draw_hip(ctx, 330, FLOOR - 160, 1.05, 1, BOY, kp)
        else:
            kp = P(eye='happy', mouth='grin', rsh=-160 + 20 * math.sin(il * 0.8), rel=-10, lsh=160 - 20 * math.sin(il * 0.8), lel=10)
            b = kid_in_box(ctx, 620, top, 1.05, kp, 140 * (1 - dive) - 30 * math.sin(pop(il, 22, 40) * math.pi * 3) * pop(il, 22, 26))
            party_hat(ctx, b)
        box_front(ctx, 620, top, 500, 300)
        # robot upside down on the floor
        fall = eout(pop(il, 0, 6))
        robot(ctx, 340, FLOOR - 30 - 400 * (1 - fall), 0.42, il, 'sad' if il > 8 else 'happy', -1.45 * fall)
        puff(ctx, 620, top - 60, pop(il, 12, 24), 1.4)
        ctx.restore()
        if il < 16:
            label(ctx, "*CLUNK*", 540, LY, 120, (1, 1, 1), -0.04, pop(il, 6, 10))
        else:
            label(ctx, "\"BEST. GIFT. EVER!\"", 540, LY, 104, YEL, 0.03, pop(il, 16, 20))
    card(ctx, 'p2', f, 114, 230)


def imagination(ctx, f, il, kind):
    if kind == 0:   # race car
        ctx.save(); cam(ctx, 540, 1040, 1.0, -4, 4, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('7ad0ff')); ctx.fill()
        ctx.rectangle(-500, 1150, 2200, 1500); setc(ctx, hx('5a5a6a')); ctx.fill()
        for k in range(8):
            x = ((k * 300 - il * 60) % 2400) - 700
            ctx.rectangle(x, 1330, 160, 26); setc(ctx, (1, 1, 1)); ctx.fill()
        hlines(ctx, il // 2, 0.7, (1, 1, 1), 600, 1300)
        top = 1000 + 6 * math.sin(il * 1.3)
        box_back(ctx, 540, top, 540, 250)
        kp = P(eye='happy', mouth='scream', rsh=-80, rel=-40, lsh=-70, lel=-50, head=-6, torso=-8)
        b = kid_in_box(ctx, 540, top, 1.05, kp)
        # helmet (paper bowl)
        hx_, hy_ = b['head']; R = b['R']
        ctx.new_path(); ctx.arc(hx_, hy_ - 0.2 * R, 1.08 * R, math.pi, 2 * math.pi); ctx.close_path(); fl(ctx, RED, 7)
        box_front(ctx, 540, top, 540, 250, doodles='car')
        for k in range(4):   # dust clouds behind
            ellipse(ctx, 160 - k * 90 - (il * 8) % 90, 1290 - k * 10, 60 + 10 * k, 50 + 8 * k); fl(ctx, (1, 1, 1), 5)
        ctx.restore()
        label(ctx, "\"VROOOOOM!\"", 540, LY, 124, RED, -0.04, pop(il, 2, 6))
    elif kind == 1:   # rocket
        ctx.save(); cam(ctx, 540, 1000, 1.0, 3, 6, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('15123a')); ctx.fill()
        rnd = random.Random(9)
        for k in range(50):
            sx, sy = rnd.uniform(-100, 1200), (rnd.uniform(0, 2400) + il * 40) % 2400 - 200
            ctx.rectangle(sx, sy, 5, 30 + rnd.uniform(0, 40)); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()
        ellipse(ctx, 920, 680, 90, 90); fl(ctx, hx('ffb46a'), 6)
        ctx.new_path(); ctx.arc(920, 680, 150, 2.6, 6.2); setc(ctx, hx('ffd23f')); ctx.set_line_width(14); ctx.stroke()
        top = 1000
        box_back(ctx, 540, top, 400, 260)
        kp = P(eye='shock', mouth='grin', rsh=-170, rel=-5, lsh=170, lel=5)
        b = kid_in_box(ctx, 540, top, 1.0, kp)
        # flames
        for k in range(3):
            fh = 260 + 60 * math.sin(il * 1.7 + k)
            poly(ctx, [(540 - 130 + k * 130 - 50, top + 260), (540 - 130 + k * 130 + 50, top + 260), (540 - 130 + k * 130, top + 260 + fh)]); fl(ctx, (ORANGE, YEL, ORANGE)[k], 6)
        box_front(ctx, 540, top, 400, 260, doodles='rocket')
        ctx.restore()
        label(ctx, "\"BLAST OFF!\"", 540, LY + 20, 120, YEL, 0.04, pop(il, 2, 6))
    else:   # pirate ship
        ctx.save(); cam(ctx, 540, 1040, 1.0, 5 * math.sin(il * 0.25), 2, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb46a')); ctx.fill()
        ellipse(ctx, 540, 1100, 220, 220); setc(ctx, hx('fff27a')); ctx.fill()
        top = 1010 + 20 * math.sin(il * 0.25)
        # mast + flag
        ctx.rectangle(530, top - 520, 20, 520); fl(ctx, hx('7a4a2c'), 5)
        poly(ctx, [(550, top - 520), (780, top - 470), (550, top - 400)]); fl(ctx, hx('2a2a3a'), 6)
        text(ctx, "X", 630, top - 440, 60, (1, 1, 1), ow=3, shadow=False)
        box_back(ctx, 540, top, 560, 260)
        kp = P(eye='smug', mouth='grin', rsh=-140, rel=40, lsh=60, lel=-100)
        b = kid_in_box(ctx, 400, top, 1.0, kp)
        hx_, hy_ = b['head']; R = b['R']   # paper pirate hat
        poly(ctx, [(hx_ - 1.25 * R, hy_ - 0.55 * R), (hx_ + 1.25 * R, hy_ - 0.55 * R), (hx_, hy_ - 1.6 * R)]); fl(ctx, hx('2a2a3a'), 6)
        ctx.move_to(hx_ - 0.2 * R, hy_ - 1.15 * R); ctx.line_to(hx_ + 0.2 * R, hy_ - 0.85 * R); ctx.move_to(hx_ + 0.2 * R, hy_ - 1.15 * R); ctx.line_to(hx_ - 0.2 * R, hy_ - 0.85 * R)
        setc(ctx, (1, 1, 1)); ctx.set_line_width(8); ctx.stroke()
        box_front(ctx, 540, top, 560, 260, doodles='ship')
        # waves
        for row in range(2):
            ctx.new_path(); y0 = 1300 + row * 70
            ctx.move_to(-200, 2400)
            for k in range(14):
                x = -200 + k * 110 + (il * (6 + row * 4)) % 110
                ctx.line_to(x, y0 + 30 * math.sin(k + il * 0.2)); ctx.line_to(x + 55, y0 - 30)
            ctx.line_to(1400, 2400); ctx.close_path(); fl(ctx, (BLUE, hx('3ca8ff'))[row], 7)
        ctx.restore()
        label(ctx, "\"ARRR, MATEY!\"", 540, LY + 10, 116, (1, 1, 1), -0.03, pop(il, 2, 6))


def s3(ctx, f):
    lf = f - 230
    if lf < 108:
        k = min(2, lf // 36)
        imagination(ctx, f, lf - 36 * k, k)
    else:
        il = lf - 108
        # the robot, alone in the corner, rain cloud
        ctx.save(); cam(ctx, 300, 1180, 1.25 + 0.05 * eout(pop(il, 0, 30)), 0, 0, f)
        party(ctx, il)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, (0.1, 0.1, 0.3, 0.35)); ctx.fill()
        robot(ctx, 300, FLOOR + 10, 0.55, il, 'sad', 0, 0)
        cloud(ctx, 300, 1010, 0.7, hx('8a8aa8'), hx('6a6a88'))
        for k in range(6):
            dy = (il * 14 + k * 50) % 120
            ctx.rectangle(220 + k * 32, 1070 + dy, 5, 30); setc(ctx, hx('9fd6ff')); ctx.fill()
        ctx.restore()
        label(ctx, "*sad beep*", 540, LY, 100, hx('9fd6ff'), 0.03, pop(il, 2, 6))
    card(ctx, 'p3', f, 234, 366)


def s4(ctx, f):
    lf = f - 370
    if lf < 66:
        # Dad shows off the robot: it dances. The box closes its flaps.
        ctx.save(); cam(ctx, 540, 1060, 0.9, 0, shake_at(lf, [40], 10, 18), f)
        party(ctx, lf)
        top = 1150
        cl = eout(pop(lf, 30, 40))
        box_back(ctx, 760, top, 420, 300, 1 - cl)
        if cl < 1:
            kp = P(eye='normal', mouth='flat', rsh=-150, rel=-20, lsh=150, lel=20)
            ctx.save(); ctx.rectangle(-500, -500, 2200, top + 800); ctx.clip()
            kid_in_box(ctx, 760, top, 0.95, kp, -300 * cl)
            ctx.restore()
        box_front(ctx, 760, top, 420, 300, closed=cl, sign="DO NOT DISTURB" if lf >= 38 else None)
        if cl >= 1:   # closed lid
            poly(ctx, [(760 - 210, top), (760 - 170, top - 60), (760 + 170, top - 60), (760 + 210, top)]); fl(ctx, CARD, 8)
            ctx.move_to(760, top - 60); ctx.line_to(760, top); ink(ctx, 6); ctx.stroke()
        dp = P(eye='happy', mouth='grin', rsh=-60 - 30 * math.sin(lf * 0.5), rel=-60, lsh=40, lel=-30)
        draw_hip(ctx, 300, FLOOR - 220, 1.3, 1, DAD, dp)
        robot(ctx, 420, 1000 + 20 * abs(math.sin(lf * 0.4)), 0.5, lf, 'love', 0.25 * math.sin(lf * 0.4), 1.0)
        for k in range(4):
            sparkle(ctx, 420 + 160 * math.cos(lf * 0.3 + k * 1.6), 820 + 120 * math.sin(lf * 0.3 + k * 1.6), 22, YEL)
        ctx.restore()
        if lf < 38:
            label(ctx, "\"LOOK! IT DANCES!\"", 540, LY, 104, YEL, -0.03, pop(lf, 2, 6))
        else:
            label(ctx, "*FLAP FLAP*", 540, LY, 116, (1, 1, 1), 0.04, pop(lf, 38, 42))
    else:
        il = lf - 66
        # Dad ECU, defeated, robot sad in his hands
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.08 * eout(pop(il, 0, 60)), -3, shake_at(il, [0], 6, 10), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('5a6ad8')); ctx.fill()
        rays(ctx, 540, 900, 260, 1500, il * 0.01, col=(0.3, 0.35, 0.8), a=0.5, n=14)
        face(ctx, DAD, P(eye='closed', mouth='frown', head=0), 540, 880, 290, 0.06)
        ellipse(ctx, 420, 980 + (il % 20) * 8, 16, 24); fl(ctx, hx('9fd6ff'), 4)   # tear
        robot(ctx, 540, 1330, 0.45, il, 'sad', 0, 0)
        ctx.restore()
        label(ctx, "\"...it was SO expensive.\"", 540, LY + 30, 88, (1, 1, 1), -0.03, pop(il, 4, 8))
    card(ctx, 'p4', f, 374, 496)


def night_room(ctx):
    living(ctx, False)
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, (0.05, 0.05, 0.2, 0.25)); ctx.fill()


def s5(ctx, f):
    lf = f - 500
    if lf < 34:
        # dark room, the box rumbles: VROOM VROOM
        ctx.save(); cam(ctx, 540, 1150, 1.1 + 0.1 * eout(pop(lf, 0, 34)), 0, 4 + 6 * (lf % 8 < 4), f)
        night_room(ctx)
        top = 1150
        wig = 0.04 * math.sin(lf * 1.4)
        ctx.save(); ctx.translate(540, FLOOR); ctx.rotate(wig); ctx.translate(-540, -FLOOR)
        box_back(ctx, 540, top, 500, 300, 0)
        box_front(ctx, 540, top, 500, 300, closed=1.0)
        poly(ctx, [(540 - 250, top), (540 - 210, top - 60), (540 + 210, top - 60), (540 + 250, top)]); fl(ctx, CARD, 8)
        ctx.restore()
        for k in range(3):
            zx = 540 + (k - 1) * 300; zy = 900 - 40 * math.sin(lf * 0.5 + k)
            ctx.move_to(zx - 40, zy); ctx.line_to(zx + 40, zy - 30); setc(ctx, YEL); ctx.set_line_width(10); ctx.stroke()
        ctx.restore()
        label(ctx, "\"VROOM VROOM!\"", 540, LY, 116, YEL, 0.03, pop(lf, 2, 6))
    elif lf < 70:
        il = lf - 34
        # flaps fly open: it's DAD, with a crayon steering wheel. Kid in pyjamas catches him.
        ctx.save(); cam(ctx, 540, 1080, 0.95, 0, shake_at(il, [0, 16], 10, 20), f)
        night_room(ctx)
        top = 1150
        box_back(ctx, 470, top, 520, 300)
        froze = il >= 16
        dp = P(eye='happy' if not froze else 'shock', mouth='scream' if not froze else 'open', rsh=-80, rel=-30, lsh=-70, lel=-40,
               torso=-6 + (0 if froze else 4 * math.sin(il * 1.2)))
        b = draw_hip(ctx, 470, top + 70, 1.1, 1, DAD, dp)
        # paper-plate steering wheel
        wx, wy = b['front']
        ellipse(ctx, wx + 10, wy - 10, 70, 70); fl(ctx, (1, 1, 1), 7); ellipse(ctx, wx + 10, wy - 10, 22, 22); fl(ctx, RED, 5)
        box_front(ctx, 470, top, 520, 300, doodles='car')
        # kid in the doorway (right), hands on hips
        if froze:
            u = eout(pop(il, 16, 24))
            kp = P(eye='glare', mouth='flat', rsh=40, rel=-120, lsh=-40, lel=120)
            ctx.save(); g = cairo.LinearGradient(0, 600, 0, 1500)
            ctx.restore()
            draw_hip(ctx, 850 + 250 * (1 - u), FLOOR - 160, 1.0, -1, BOY, kp)
        ctx.restore()
        if il < 16:
            label(ctx, "\"VROOOM VROO—\"", 540, LY, 112, YEL, -0.03, pop(il, 0, 4))
        else:
            label(ctx, "*FREEZE*", 540, LY, 124, (1, 1, 1), 0.04, pop(il, 16, 20))
    elif lf < 126:
        il = lf - 70
        # Dad ECU in the box, caught, sheepish grin
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.07 * eout(pop(il, 0, 56)), 2, shake_at(il, [0], 6, 10), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8ac0')); ctx.fill()
        rays(ctx, 540, 900, 240, 1500, il * 0.02, col=(1, 1, 1), a=0.35, n=16)
        face(ctx, DAD, P(eye='shock', mouth='grin', head=0), 540, 860, 290, -0.08)
        sweat(ctx, 820, 760 + (il % 20) * 5, 2.0)
        ctx.rectangle(-500, 1180, 2200, 800); fl(ctx, CARD, 10)   # box rim in the foreground
        ctx.rectangle(500, 1180, 80, 160); setc(ctx, hx('e8c48a')); ctx.fill()
        ctx.restore()
        label(ctx, "\"...it's a GOOD box.\"", 540, LY + 30, 100, (1, 1, 1), -0.03, pop(il, 4, 8))
        # robot, now happily playing with the wrapping-paper ball, inset bottom-left
        if il >= 26:
            u = eout(pop(il, 26, 34))
            ctx.save(); ctx.translate(190 - 300 * (1 - u), 1220)
            ellipse(ctx, 0, 0, 130, 130); fl(ctx, YEL, 8); ctx.save(); ellipse(ctx, 0, 0, 122, 122); ctx.clip()
            robot(ctx, 0, 120, 0.42, il, 'love', 0.2 * math.sin(il * 0.4), 1.0)
            scrap(ctx, 60, 60, il * 0.3, RED, 0.8)
            ctx.restore(); ctx.restore()
    else:
        il = lf - 126
        opening_face(ctx, f, il, True)
    if lf < 126:
        card(ctx, 'p5', f, 504, 622)
    else:
        card(ctx, 'p1', f, 626)


SHOTS = [(0, s1), (110, s2), (230, s3), (370, s4), (500, s5)]
CUTS = (50, 110, 150, 190, 230, 266, 302, 338, 370, 436, 500, 534, 570, 626)


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
                              "-i", "out/the_box_wins_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
