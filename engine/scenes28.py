"""'Who Wants To Help With The Groceries?' - original, general-audience comedy short, ~22s.
ECU: Mom in the doorway, arms full of bags: "WHO WANTS TO HELP?" Wide: Dad + kid on the sofa... POOF, gone.
Hiding: Dad behind the curtain on a 'very important call' (it's a banana); kid pretending to be a lamp.
Mom carries a skyscraper of bags in ONE TRIP. THUD. Then she whispers "who wants ice cream?" - ZOOM, both at the table.
Twist: "It's in the car... with the other 30 bags." POOF again. Loops to the ECU."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
import scenes13
from scenes13 import card as _card13
import random

BOY = doodle.BOY
DAD = doodle.DAD
MOM = doodle.MOM_G
N = 660
FLOOR = 1430

CAPS = {
    'p1': [[("WHEN MOM ASKS", OUT)], [("WHO WANTS TO ", OUT), ("HELP", hx('2fbf5a'))]],
    'p2': [[("SUDDENLY EVERYONE", OUT)], [("IS ", OUT), ("VERY BUSY", hx('1f8bff'))]],
    'p3': [[("SO SHE DOES IT IN", OUT)], [("ONE TRIP", hx('ff3b5c'))]],
    'p4': [[("THEN SHE SAYS THE", OUT)], [("MAGIC WORDS", hx('8a3cff'))]],
    'p5': [[("THE ICE CREAM", OUT)], [("WAS A ", OUT), ("TRAP", hx('ff3b5c'))]],
}
scenes13.CAPS = CAPS
card = _card13


def label(ctx, s, x, y, size, col, ang=0, t=1.0):
    if t <= 0:
        return
    sc = 0.5 + 0.5 * eout(min(1, t * 2)) + 0.08 * math.sin(min(1, t) * math.pi)
    ctx.save(); ctx.translate(x, y); ctx.scale(sc, sc)
    text(ctx, s, 0, 0, size, col, ang=ang, ow=12, maxw=860)
    ctx.restore()


def cam(ctx, cx, cy, z, rot=0, shake=0, f=0, sx=W / 2, sy=H / 2):
    rnd = random.Random(f * 31 + 7)
    dx, dy = (rnd.uniform(-1, 1) * shake, rnd.uniform(-1, 1) * shake) if shake else (0, 0)
    ctx.translate(sx + dx, sy + dy); ctx.rotate(math.radians(rot)); ctx.scale(z, z); ctx.translate(-cx, -cy)


def rect_r(ctx, x, y, w, h, r):
    ctx.new_path(); ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); ctx.close_path()


def rays(ctx, x, y, r0, r1, t, col=(1, 0.97, 0.6), a=0.8, n=12):
    for k in range(n):
        ang = k * 2 * math.pi / n + t
        ctx.move_to(x + math.cos(ang) * r0, y + math.sin(ang) * r0)
        ctx.line_to(x + math.cos(ang - 0.09) * r1, y + math.sin(ang - 0.09) * r1)
        ctx.line_to(x + math.cos(ang + 0.09) * r1, y + math.sin(ang + 0.09) * r1); ctx.close_path()
    setc(ctx, col + (a,)); ctx.fill()


_SCR = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4))


def face(ctx, ch, p, cx, cy, Rt, rot=0.0, f_=1):
    b = draw_hip(_SCR, 0, 0, 1, f_, ch, p)
    hd, R = b['head'], b['R']
    s = Rt / R
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s); ctx.translate(-hd[0], -hd[1])
    draw_hip(ctx, 0, 0, 1, f_, ch, p)
    ctx.restore()


def talk(lf, a='open', b='scream', rate=4):
    return a if (lf // rate) % 2 == 0 else b


def speed_lines(ctx, x, y, w, h, t, n=10, seed=2, col=(1, 1, 1), a=0.8):
    rnd = random.Random(seed)
    for k in range(n):
        yy = y + rnd.uniform(0, h); ln = rnd.uniform(0.3, 1) * w
        xx = x + ((rnd.uniform(0, 1) * w + t * 60) % w)
        ctx.move_to(xx, yy); ctx.line_to(xx + ln * 0.5, yy)
        setc(ctx, col + (a,)); ctx.set_line_width(rnd.uniform(6, 14)); ctx.stroke()


# ------------------------------------------------------------------ props
def bag(ctx, x, y, s=1.0, a=0.0, kind=0):
    """paper grocery bag, bottom-centre at (x, y)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    # stuff poking out
    if kind % 3 == 0:   # long bread + greens
        ctx.save(); ctx.translate(-30, -230); ctx.rotate(-0.35)
        rect_r(ctx, -22, -110, 44, 190, 22); fl(ctx, hx('e8a85a'), 6)
        for k in range(4):
            ctx.move_to(-14, -80 + k * 36); ctx.line_to(12, -66 + k * 36); ink(ctx, 5); ctx.stroke()
        ctx.restore()
        for k in range(4):
            ellipse(ctx, 40 + k * 14, -250 - 20 * (k % 2), 26, 50, -0.4 + 0.3 * k); fl(ctx, hx('3fbf4a'), 5)
    elif kind % 3 == 1:  # carrots + apple
        for k in range(3):
            ctx.save(); ctx.translate(-30 + k * 26, -230); ctx.rotate(-0.3 + k * 0.25)
            poly(ctx, [(-14, 0), (14, 0), (0, -110)]); fl(ctx, hx('ff8a1f'), 5)
            poly(ctx, [(-10, 6), (0, 40), (10, 6)]); fl(ctx, hx('3fbf4a'), 4)
            ctx.restore()
        ellipse(ctx, 50, -235, 40, 38); fl(ctx, hx('ff3b5c'), 6)
    else:               # milk carton + leek
        rect_r(ctx, -60, -310, 80, 110, 6); fl(ctx, (1, 1, 1), 6)
        poly(ctx, [(-60, -310), (-20, -350), (20, -310)]); fl(ctx, hx('1f8bff'), 6)
        ctx.save(); ctx.translate(50, -250); ctx.rotate(0.3)
        rect_r(ctx, -14, -90, 28, 130, 12); fl(ctx, hx('f6f6e0'), 5)
        poly(ctx, [(-14, -88), (0, -170), (14, -88)]); fl(ctx, hx('3fbf4a'), 5)
        ctx.restore()
    poly(ctx, [(-100, 0), (100, 0), (88, -240), (-88, -240)]); fl(ctx, hx('d9a46a'), 8)
    poly(ctx, [(-88, -240), (88, -240), (84, -214), (-84, -214)]); fl(ctx, hx('c48a4e'), 5)
    ctx.move_to(-40, -150); ctx.curve_to(-20, -130, 20, -130, 40, -150); setc(ctx, hx('a8703a')); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def banana(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-70, -30); ctx.curve_to(-40, 50, 40, 50, 70, -30)
    ctx.curve_to(40, 20, -40, 20, -70, -30); ctx.close_path(); fl(ctx, hx('ffe14d'), 6)
    ctx.rectangle(-80, -40, 16, 18); fl(ctx, hx('6a4a2c'), 4)
    ctx.restore()


def lampshade(ctx, x, y, s, glow=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if glow > 0:
        poly(ctx, [(-90, 0), (90, 0), (260, 520), (-260, 520)]); setc(ctx, (1, 0.95, 0.5, 0.35 * glow)); ctx.fill()
    poly(ctx, [(-70, -150), (70, -150), (110, 20), (-110, 20)]); fl(ctx, hx('ffd23f') if glow > 0 else hx('ffe9a8'), 9)
    for k in range(3):
        ctx.move_to(-90 + k * 6, -60 + k * 40); ctx.line_to(90 - k * 6, -60 + k * 40); setc(ctx, hx('ff8a1f')); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()


def tub(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    poly(ctx, [(-80, 0), (80, 0), (95, -130), (-95, -130)]); fl(ctx, hx('ffb3d1'), 7)
    rect_r(ctx, -102, -160, 204, 36, 12); fl(ctx, hx('ff6fa8'), 7)
    ellipse(ctx, 0, -66, 34, 34); fl(ctx, hx('fff2c8'), 5)
    poly(ctx, [(-22, -56), (22, -56), (0, -6)]); fl(ctx, hx('e8a85a'), 4)
    ctx.restore()


def car(ctx, x, y, s, t=0, bags_n=0):
    """hatchback seen from behind, trunk open, bottom-centre (x, y)"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for wx in (-220, 220):
        ellipse(ctx, wx, -40, 70, 60); fl(ctx, hx('2a2840'), 8)
    rect_r(ctx, -330, -260, 660, 200, 50); fl(ctx, hx('1f8bff'), 9)
    rect_r(ctx, -300, -420, 600, 200, 60); fl(ctx, hx('1f8bff'), 9)
    rect_r(ctx, -250, -380, 500, 140, 30); fl(ctx, hx('2a2840'), 7)
    # bags crammed inside, spilling out of the open hatch
    rnd = random.Random(9)
    pts = []
    for k in range(bags_n):
        bx = rnd.uniform(-220, 220); by = -200 - rnd.uniform(0, 260) - (k // 6) * 30
        pts.append((by, bx, k))
    for by, bx, k in sorted(pts, reverse=False):
        bag(ctx, bx, by + 120, 0.55, rnd.uniform(-0.3, 0.3), k)
    for lx in (-300, 300):
        rect_r(ctx, lx - 30, -230, 60, 40, 10); fl(ctx, hx('ff3b5c'), 6)
    # open hatch lid above
    poly(ctx, [(-290, -430), (290, -430), (250, -600), (-250, -600)]); fl(ctx, hx('1f8bff'), 9)
    poly(ctx, [(-230, -460), (230, -460), (200, -570), (-200, -570)]); fl(ctx, hx('8fd8ff'), 6)
    ctx.restore()


# ------------------------------------------------------------------ sets
def hallway(ctx):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('ffe08a')); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 120, -3000, 46, 6000); setc(ctx, hx('ffd46a')); ctx.fill()
    # open front door frame behind her
    ctx.rectangle(250, 300, 580, 1300); fl(ctx, hx('9fd8ff'), 12)
    ellipse(ctx, 380, 600, 110, 60); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()
    ellipse(ctx, 700, 520, 80, 44); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()
    ctx.rectangle(250, 1250, 580, 400); setc(ctx, hx('6fd06a')); ctx.fill()
    ctx.rectangle(250, 300, 580, 1300); ink(ctx, 12); ctx.stroke()


def living_room(ctx, curtain=False):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('c8e6ff')); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 120, -3000, 50, 3000 + FLOOR); setc(ctx, hx('b6dcff')); ctx.fill()
    # window
    rect_r(ctx, 640, 520, 330, 380, 14); fl(ctx, hx('fff6c8'), 10)
    ctx.move_to(805, 520); ctx.line_to(805, 900); ctx.move_to(640, 710); ctx.line_to(970, 710); ink(ctx, 8); ctx.stroke()
    # TV on stand (left)
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('e0a868')); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()


def sofa(ctx, x=540, y=FLOOR):
    rect_r(ctx, x - 380, y - 400, 760, 240, 50); fl(ctx, hx('ff6b8a'), 9)
    rect_r(ctx, x - 400, y - 220, 800, 190, 36); fl(ctx, hx('ff8fa8'), 9)
    for ax in (x - 440, x + 360):
        rect_r(ctx, ax, y - 290, 80, 260, 36); fl(ctx, hx('ff6b8a'), 9)
    ctx.move_to(x, y - 210); ctx.line_to(x, y - 40); ink(ctx, 6); ctx.stroke()


def kitchen(ctx):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('d6f5c8')); ctx.fill()
    for i in range(-20, 30):
        for j in range(-10, 30):
            if (i + j) % 2 == 0:
                ctx.rectangle(i * 90, j * 90, 90, 90); setc(ctx, hx('c6edb6')); ctx.fill()
    # window with car outside
    rect_r(ctx, 120, 480, 520, 440, 16); fl(ctx, hx('9fd8ff'), 10)


def table(ctx, y=1240):
    ctx.rectangle(-200, y, 1480, 50); fl(ctx, hx('c98a52'), 9)
    for lx in (120, 900):
        ctx.rectangle(lx, y + 50, 40, FLOOR + 200 - y); fl(ctx, hx('a86a3a'), 7)


# ------------------------------------------------------------------ shots
def opening_face(ctx, f, lf, lab=True):
    sh = shake_at(lf, [0], 12, 20) + 2
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.04 * eout(pop(lf, 0, 60)), 0, sh, f)
    hallway(ctx)
    rays(ctx, 540, 980, 300, 1400, lf * 0.02, col=(1, 1, 1), a=0.35, n=16)
    pm = P(eye='shock', mouth=talk(lf, 'scream', 'open', 6), head=-6)
    face(ctx, MOM, pm, 540 + 8 * math.sin(lf * 0.4), 980, 400, -0.06 + 0.03 * math.sin(lf * 0.3))
    sweat(ctx, 930, 700 + (lf % 24) * 5, 2.2)
    # bags hanging up in the foreground corners
    bag(ctx, 150, 1760 + 10 * math.sin(lf * 0.3), 1.5, 0.15, 0)
    bag(ctx, 930, 1770 + 10 * math.sin(lf * 0.3 + 1), 1.5, -0.12, 1)
    ctx.restore()
    if lab:
        label(ctx, "\"WHO WANTS TO HELP?\"", 540, 1470, 104, (1, 1, 1), -0.04, pop(lf, 0, 4) if lf > 0 else 1)


def s1(ctx, f):
    if f < 50:
        opening_face(ctx, f, f)
    else:
        lf = f - 50
        GONE = 16
        ctx.save(); cam(ctx, 540, 1080, 1.0, 0, shake_at(lf, [GONE], 12, 26), f)
        living_room(ctx)
        sofa(ctx)
        if lf < GONE:
            pd = P(eye='shock', mouth='open', torso=-4, lhip=-80, lkn=80, rhip=-80, rkn=80, rsh=40, lsh=-30, head=-10)
            draw_hip(ctx, 360, FLOOR - 230, 1.3, 1, DAD, pd)
            pb = P(eye='shock', mouth='open', torso=4, lhip=-80, lkn=80, rhip=-80, rkn=80, rsh=-30, lsh=30, head=10)
            draw_hip(ctx, 720, FLOOR - 230, 1.0, -1, BOY, pb)
        else:
            u = pop(lf, GONE, GONE + 14)
            puff(ctx, 360, 950, u, 2.6)
            puff(ctx, 720, 1050, u, 2.2)
            # dashed 'outline was here' + speed lines out of frame
            if lf > GONE + 6:
                for k in range(4):
                    yy = 900 + k * 70
                    ctx.move_to(-20, yy); ctx.line_to(200 - 40 * k, yy); ink(ctx, 10); ctx.stroke()
                    ctx.move_to(1100, yy + 60); ctx.line_to(880 + 40 * k, yy + 60); ink(ctx, 10); ctx.stroke()
            # remote spinning down onto the cushion
            v = pop(lf, GONE, GONE + 30)
            rx, ry = 540 + 60 * v, lerp(700, 1190, eout(v) if v < 1 else 1)
            ctx.save(); ctx.translate(rx, ry); ctx.rotate(v * 12)
            rect_r(ctx, -24, -70, 48, 140, 14); fl(ctx, hx('2a2840'), 6)
            for k in range(3):
                ellipse(ctx, 0, -40 + k * 30, 9, 9); setc(ctx, hx('ff3b5c') if k == 0 else (1, 1, 1)); ctx.fill()
            ctx.restore()
        ctx.restore()
        if lf < GONE:
            label(ctx, "!!", 540, 1500, 150, hx('ffe14d'), 0.05, pop(lf, 0, 4))
        else:
            label(ctx, "*POOF*", 540, 1500, 150, (1, 1, 1), -0.05, pop(lf, GONE, GONE + 4))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 60:
        il = lf
        # low angle on the curtain: Dad's shoes poke out, he peeks with a banana phone
        ctx.save(); cam(ctx, 540, 1000, 1.05 - 0.05 * eout(pop(il, 0, 60)), 3, shake_at(il, [14], 10, 18), f)
        living_room(ctx)
        ctx.rectangle(260, 300, 560, 30); fl(ctx, hx('a86a3a'), 7)
        pk = P(eye='smug', mouth=talk(il, 'open', 'smile', 5) if il > 14 else 'flat', head=-14, rsh=150, rel=-120, torso=-10)
        peek = eout(pop(il, 8, 16))
        # dad body hidden behind curtain; head pokes out on the right
        bd = draw_hip(_SCR, 0, 0, 1, 1, DAD, pk)
        dx_ = 520 + 230 * peek
        draw_hip(ctx, 600, FLOOR - 230, 1.4, -1, DAD, pk)
        # curtain over him
        for k in range(6):
            x0 = 280 + k * 90
            ctx.move_to(x0, 330); ctx.curve_to(x0 + 10, 800, x0 - 20, 1100, x0 + 10, FLOOR - 70)
            ctx.line_to(x0 + 100, FLOOR - 70); ctx.curve_to(x0 + 80, 1100, x0 + 110, 800, x0 + 90, 330); ctx.close_path()
            fl(ctx, hx('8a3cff') if k % 2 == 0 else hx('9b55ff'), 7)
        # shoes peeking under curtain
        for sx in (450, 600):
            ellipse(ctx, sx, FLOOR - 30, 60, 30); fl(ctx, DAD['shoes'], 7)
        # head peeks out past the curtain edge, banana 'phone' at his ear
        hx_ = lerp(690, 820, peek)
        ctx.save(); ellipse(ctx, hx_, 830, 180, 165); ctx.clip()
        face(ctx, DAD, pk, hx_, 840, 140, -0.25 * peek, -1)
        ctx.restore()
        banana(ctx, hx_ + 150, 860, 1.3, -1.9 + 0.1 * math.sin(il * 0.5))
        ellipse(ctx, hx_ + 130, 930, 26, 26); fl(ctx, DAD['skin'], 6)
        ctx.restore()
        if il > 14:
            label(ctx, "\"SORRY, I'M ON A CALL\"", 540, 1480, 96, (1, 1, 1), -0.04, pop(il, 14, 18))
        if il > 34:
            # reveal the 'phone'
            label(ctx, "(IT'S A BANANA)", 540, 1590, 64, hx('ffe14d'), 0.03, pop(il, 34, 38))
    else:
        il = lf - 60
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.12 * eout(pop(il, 0, 60)), 0, shake_at(il, [20], 8, 14), f)
        living_room(ctx)
        # boy frozen in the corner wearing a lampshade, holding the cord
        pb = P(eye='normal' if il % 40 > 3 else 'closed', mouth='flat', rsh=4, rel=0, lsh=-4, lel=0, lhip=2, rhip=-2)
        b = draw_hip(ctx, 540, FLOOR - 180, 1.5, 1, BOY, pb)
        hd = b['head']
        glow = 1.0 if il >= 20 else 0.0
        lampshade(ctx, hd[0], hd[1] - b['R'] * 0.25, 1.35, glow)
        # cord from his hand to the socket
        hn = b['front']
        ctx.move_to(*hn); ctx.curve_to(hn[0] + 80, FLOOR + 20, 880, FLOOR + 10, 930, 1300); ink(ctx, 8); ctx.stroke()
        rect_r(ctx, 905, 1270, 50, 70, 8); fl(ctx, (1, 1, 1), 6)
        if glow:
            sparkle(ctx, hd[0] + 160, hd[1] - 150, 34, (1, 1, 1))
            sparkle(ctx, hd[0] - 170, hd[1] - 100, 24, (1, 1, 1))
        ctx.restore()
        label(ctx, "\"I AM A LAMP\"", 540, 1480, 120, hx('ffe14d'), 0.04, pop(il, 4, 8))
        if il >= 20:
            label(ctx, "*CLICK*", 300, 1610, 70, (1, 1, 1), -0.06, pop(il, 20, 24))
    card(ctx, 'p2', f, 114, 226)


TOWER = [(0, 0.0), (1, 0.12), (2, -0.1), (0, 0.08), (1, -0.12), (2, 0.1), (0, -0.05)]


def s3(ctx, f):
    lf = f - 230
    DROP = 104
    if lf < DROP:
        # tilt down the skyscraper of bags onto straining Mom
        cy = lerp(-200, 1060, ease(pop(lf, 4, 64)))
        z = lerp(0.85, 1.0, ease(pop(lf, 4, 64)))
        ctx.save(); cam(ctx, 540, cy, z, 2 * math.sin(lf * 0.2), 3, f)
        hallway(ctx)
        ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('c98a52')); ctx.fill()
        ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()
        step = math.sin(lf * 0.35)
        pm = P(eye='glare', mouth='flat' if lf % 30 < 20 else 'open', rsh=170, rel=10, lsh=-170, lel=-10, torso=3 * step,
               lhip=12 * step, lkn=-10, rhip=-12 * step, rkn=-10, head=0)
        b = draw_hip(ctx, 540 + 20 * step, FLOOR - 190, 1.4, 1, MOM, pm)
        # bags hanging off each arm
        bag(ctx, 300, FLOOR - 40, 0.8, 0.1 * step, 1)
        bag(ctx, 780, FLOOR - 40, 0.8, -0.1 * step, 2)
        # tower on her hands
        hy = b['head'][1] - b['R'] * 1.15
        sway = 0.025 * math.sin(lf * 0.18)
        ctx.save(); ctx.translate(540 + 20 * step, hy)
        for k, (kind, off) in enumerate(TOWER):
            ctx.rotate(sway)
            bag(ctx, off * 200, 0, 1.0, off * 0.4, kind)
            ctx.translate(0, -250)
        ellipse(ctx, 0, -60, 110, 85); fl(ctx, hx('3fbf4a'), 8)  # watermelon on top
        for k in range(5):
            ctx.move_to(-80 + k * 40, -130); ctx.curve_to(-70 + k * 40, -60, -90 + k * 40, -10, -80 + k * 40, 15)
            setc(ctx, hx('1f7a2c')); ctx.set_line_width(8); ctx.stroke()
        ctx.restore()
        sweat(ctx, b['head'][0] + 130, b['head'][1] - 40 + (lf % 20) * 4, 1.6)
        ctx.restore()
        if lf < 50:
            label(ctx, "47 BAGS. 2 ARMS.", 540, 1480, 110, (1, 1, 1), -0.04, pop(lf, 4, 8))
        else:
            label(ctx, "*STRAIN*", 540, 1480, 130, hx('ff8a1f'), 0.04, pop(lf, 50, 54))
    else:
        il = lf - DROP
        ctx.save(); cam(ctx, 540, 1100, 1.0 + 0.08 * eout(pop(il, 0, 12)), 0, shake_at(il, [0], 16, 40), f)
        kitchen(ctx)
        ctx.rectangle(-200, 1150, 1480, 700); fl(ctx, hx('ffffff'), 9)
        ctx.rectangle(-200, 1120, 1480, 40); fl(ctx, hx('ff8a1f'), 8)
        rnd = random.Random(5)
        for k in range(9):
            bag(ctx, 90 + k * 110, 1130, 0.75, rnd.uniform(-0.25, 0.25), k)
        pm = P(eye='happy', mouth='grin', rsh=170, rel=20, lsh=-30, lel=-80, head=-8)
        draw_hip(ctx, 820, 1000, 1.2, -1, MOM, pm)
        for k in range(4):
            sparkle(ctx, 200 + k * 220, 760 + 60 * (k % 2), 30 * eout(pop(il, 4, 12)), (1, 1, 1))
        ctx.restore()
        label(ctx, "*THUD!*", 540, 1480, 150, hx('ff3b5c'), -0.05, pop(il, 0, 4))
    card(ctx, 'p3', f, 234, 366)


def s4(ctx, f):
    lf = f - 370
    APPEAR = 46
    if lf < APPEAR:
        # ECU smug whisper, slow push in
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.15 * eout(pop(lf, 0, APPEAR)), 0, 0, f)
        kitchen(ctx)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, (0.15, 0.08, 0.25, 0.55)); ctx.fill()
        face(ctx, MOM, P(eye='smug', mouth='smile', head=8), 540, 980, 360, 0.08)
        ctx.restore()
        # cupped whisper text
        label(ctx, "\"...who wants", 540, 1440, 80, (1, 1, 1), 0.03, pop(lf, 4, 8))
        label(ctx, "ICE CREAM?\"", 540, 1560, 120, hx('ff6fa8'), -0.03, pop(lf, 16, 20))
    else:
        il = lf - APPEAR
        ctx.save(); cam(ctx, 540, 1040, 1.0, 0, shake_at(il, [0], 12, 30), f)
        kitchen(ctx)
        for who, x, k_, fd in ((DAD, 330, 1.3, 1), (BOY, 760, 1.05, -1)):
            arr = eout(pop(il, 0, 6))
            sx = x + (-900 if fd == 1 else 900) * (1 - arr)
            if il < 8:
                speed_lines(ctx, sx - 500 * fd, 700, 400, 500, il, col=(1, 1, 1), seed=x)
            p = P(eye='happy', mouth='grin', rsh=165, rel=0 + 10 * math.sin(il * 0.6), lsh=-30, head=6 * math.sin(il * 0.5))
            b = draw_hip(ctx, sx, 1240, k_, fd, who, p)
            hn = b['front']
            # spoon held up
            ctx.save(); ctx.translate(hn[0], hn[1]); ctx.rotate(0.2 * fd)
            ctx.rectangle(-7, -120, 14, 110); fl(ctx, hx('c9c9d6'), 5)
            ellipse(ctx, 0, -140, 24, 34); fl(ctx, hx('dcdce6'), 5)
            ctx.restore()
            # bib
            ctx.save()
            hd = b['head']
            poly(ctx, [(hd[0] - 50 * k_, hd[1] + b['R'] * 1.0), (hd[0] + 50 * k_, hd[1] + b['R'] * 1.0), (hd[0] + 34 * k_, hd[1] + b['R'] * 1.9), (hd[0] - 34 * k_, hd[1] + b['R'] * 1.9)])
            fl(ctx, (1, 1, 1), 6)
            ctx.restore()
        table(ctx)
        for k in range(4):
            sparkle(ctx, 160 + k * 250, 620 + 40 * (k % 2), 30, hx('ffe14d'))
        ctx.restore()
        label(ctx, "*ZOOOM!*", 540, 1480, 140, hx('ffe14d'), 0.05, pop(il, 0, 4))
        if il > 30:
            label(ctx, "0.2 SECONDS LATER", 540, 1610, 64, (1, 1, 1), -0.02, pop(il, 30, 34))
    card(ctx, 'p4', f, 374, 496)


def s5(ctx, f):
    lf = f - 500
    if lf < 72:
        # Mom points at the window: the car, trunk open, bursting with bags
        ctx.save(); cam(ctx, 540, 1040, 1.0, 0, shake_at(lf, [36], 10, 20), f)
        kitchen(ctx)
        ctx.save(); rect_r(ctx, 120, 480, 520, 440, 16); ctx.clip()
        ctx.rectangle(120, 800, 520, 200); setc(ctx, hx('9a9aa8')); ctx.fill()
        car(ctx, 380, 900, 0.62, lf, bags_n=16)
        ctx.restore()
        rect_r(ctx, 120, 480, 520, 440, 16); ink(ctx, 10); ctx.stroke()
        pm = P(eye='smug', mouth='smile', lsh=110, lel=-10, rsh=110, rel=0, head=-6)
        draw_hip(ctx, 860, 1180, 1.25, -1, MOM, pm)
        table(ctx)
        # dad + boy faces in the foreground, reacting
        shock = lf >= 36
        face(ctx, DAD, P(eye='shock' if shock else 'happy', mouth='scream' if shock else 'grin', head=-8), 260, 1340, 170, -0.1)
        face(ctx, BOY, P(eye='shock' if shock else 'happy', mouth='scream' if shock else 'grin', head=8), 660, 1360, 150, 0.1, -1)
        ctx.restore()
        if lf < 36:
            label(ctx, "\"IT'S IN THE CAR...\"", 540, 1530, 100, (1, 1, 1), -0.03, pop(lf, 2, 6))
        else:
            label(ctx, "\"...WITH THE OTHER 30 BAGS\"", 540, 1530, 84, hx('ff3b5c'), 0.03, pop(lf, 36, 40))
        card(ctx, 'p5', f, 504, 616)
    elif lf < 120:
        il = lf - 72
        ctx.save(); cam(ctx, 540, 1040, 1.0, 0, shake_at(il, [0], 12, 26), f)
        kitchen(ctx)
        ctx.save(); rect_r(ctx, 120, 480, 520, 440, 16); ctx.clip()
        ctx.rectangle(120, 800, 520, 200); setc(ctx, hx('9a9aa8')); ctx.fill()
        car(ctx, 380, 900, 0.62, lf, bags_n=16)
        ctx.restore()
        rect_r(ctx, 120, 480, 520, 440, 16); ink(ctx, 10); ctx.stroke()
        draw_hip(ctx, 860, 1180, 1.25, -1, MOM, P(eye='glare', mouth='flat', rsh=20, lsh=-20, head=0))
        table(ctx)
        u = pop(il, 0, 16)
        puff(ctx, 260, 1300, u, 2.8)
        puff(ctx, 660, 1320, u, 2.4)
        # spoons clatter on the table
        for k, sx in enumerate((360, 700)):
            v = pop(il, 2 + k * 3, 16 + k * 3)
            ctx.save(); ctx.translate(sx, lerp(900, 1230, eout(v))); ctx.rotate(v * 9 + k)
            ctx.rectangle(-7, -60, 14, 110); fl(ctx, hx('c9c9d6'), 5); ellipse(ctx, 0, -80, 24, 34); fl(ctx, hx('dcdce6'), 5)
            ctx.restore()
        ctx.restore()
        label(ctx, "*POOF*", 540, 1530, 150, (1, 1, 1), -0.05, pop(il, 0, 4))
        card(ctx, 'p5', f, 504, 616)
    else:
        il = lf - 120
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 620)


SHOTS = [(0, s1), (110, s2), (230, s3), (370, s4), (500, s5)]
CUTS = (50, 110, 170, 230, 334, 370, 416, 500, 572, 620)


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
                              "-i", "out/grocery_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
