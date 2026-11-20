"""'When the Kids Are TOO Quiet' - original, general-audience comedy short, 22s.
Hook: Mom ECU, eyes wide, frozen with her tea: caption "The house is... / TOO QUIET."
Beat 1: tiptoe down the hallway (side tracking) -> door bursts open -> wall covered in crayon art,
 kid with a crayon moustache: "...it's ART!"
Beat 2: 10 minutes later, quiet AGAIN -> bathroom: toilet paper everywhere, kid pops up as a MUMMY "BOO!"
 -> Mom ECU eye twitch "...that was 12 ROLLS."
Beat 3: backyard: kid + dog with matching marker moustaches "We're TWINS!" -> Mom gives up:
 split screen kid bangs pots "BANG! CLANG!" / Mom with tea "Ahh... NOISE is GOOD."
Twist: banging stops -> Mom ECU snaps -> kid asleep on the pots (phew) -> "...wait. Where's DAD?"
 -> pantry door creaks open, Dutch tilt: Dad on the floor in a pile of wrappers, chocolate all over his face:
 "...it's ART?" -> Mom ECU loop."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, zzz, _SCR
from scenes48 import label1, label2
from scenes58 import sweat, twitch
import scenes13
from scenes13 import card as _card13
import random


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


DAD = dict(doodle.DAD, shirt=hx('ff8a1f'), pants=hx('3d5a9e'), sleeve=0.45)
MOM = dict(doodle.MOM_G, shirt=hx('19b5a5'))
BOY = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff3b5c'))
N = 660
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
GOLD = hx('ffc93c')
TEAL = hx('19b5a5')
CHOC = hx('6b3a1e')
WHITE = (1, 1, 1)

CAPS = {
    'p1': [[("The house is...", OUT)], [("TOO QUIET.", PURPLE)]],
    'p2': [[("10 MINUTES LATER...", BLUE)]],
    'p3': [[("1 HOUR LATER...", RED)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def mug(ctx, x, y, s=1.0, steam_t=None):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(52, 0, 30, -1.4, 1.4); ink(ctx, 14); ctx.stroke()
    ctx.new_path(); ctx.arc(52, 0, 30, -1.4, 1.4); setc(ctx, GOLD); ctx.set_line_width(7); ctx.stroke()
    rect_r(ctx, -50, -60, 100, 120, 18); fl(ctx, GOLD, 6)
    ctx.new_path(); ctx.arc(0, 8, 18, 0, 2 * math.pi); fl(ctx, RED, 4)
    if steam_t is not None:
        for k in (-1, 1):
            ctx.new_path(); ctx.move_to(k * 18, -70)
            for i in range(3):
                ctx.rel_curve_to(14 * math.sin(steam_t * 0.2 + i), -18, -14 * math.sin(steam_t * 0.2 + i), -30, 0, -44)
            setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(7); ctx.stroke()
    ctx.restore()


def crayon(ctx, x, y, a, col, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -12, -70, 24, 110, 6); fl(ctx, col, 4)
    poly(ctx, [(-12, -70), (12, -70), (0, -100)]); fl(ctx, col, 4)
    ctx.rectangle(-12, -40, 24, 30); setc(ctx, (1, 1, 1, 0.7)); ctx.fill()
    ctx.restore()


def wall_art(ctx, x0, y0, x1, y1, amt=1.0, seed=4):
    """crayon chaos all over a wall (original doodles)"""
    rnd = random.Random(seed)
    cols = [RED, BLUE, GREEN, PURPLE, ORANGE, PINK]
    n = int(26 * amt)
    for i in range(n):
        c = cols[i % 6]
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1)
        kind = i % 5
        ctx.new_path()
        if kind == 0:   # zigzag
            ctx.move_to(x, y)
            for k in range(7):
                ctx.rel_line_to(rnd.uniform(25, 45), (-1) ** k * rnd.uniform(30, 70))
        elif kind == 1:  # spiral
            for k in range(60):
                a = k * 0.32; r = 4 + k * 1.3
                (ctx.move_to if k == 0 else ctx.line_to)(x + math.cos(a) * r, y + math.sin(a) * r)
        elif kind == 2:  # sun
            ctx.arc(x, y, 40, 0, 2 * math.pi)
            for k in range(8):
                a = k * math.pi / 4
                ctx.move_to(x + math.cos(a) * 52, y + math.sin(a) * 52); ctx.line_to(x + math.cos(a) * 80, y + math.sin(a) * 80)
        elif kind == 3:  # stick figure
            ctx.arc(x, y - 50, 22, 0, 2 * math.pi)
            ctx.move_to(x, y - 28); ctx.line_to(x, y + 30); ctx.move_to(x - 34, y - 10); ctx.line_to(x + 34, y - 10)
            ctx.move_to(x, y + 30); ctx.line_to(x - 24, y + 70); ctx.move_to(x, y + 30); ctx.line_to(x + 24, y + 70)
        else:  # house
            ctx.move_to(x - 50, y + 50); ctx.line_to(x - 50, y - 10); ctx.line_to(x, y - 60); ctx.line_to(x + 50, y - 10)
            ctx.line_to(x + 50, y + 50); ctx.close_path()
        setc(ctx, c); ctx.set_line_width(9); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()


def tache(ctx, hd, R, f=1, col=BLUE, curl=1.0):
    """big marker moustache drawn over a face; hd = head centre"""
    mx = hd[0] + f * R * 0.14; my = hd[1] + R * 0.38
    ctx.save(); ctx.translate(mx, my)
    for s in (-1, 1):
        ctx.new_path(); ctx.move_to(0, 0)
        ctx.curve_to(s * R * 0.2, -R * 0.12, s * R * 0.45, R * 0.05, s * R * 0.5 * curl, -R * 0.14)
        setc(ctx, col); ctx.set_line_width(R * 0.11); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.restore()


def choc_smear(ctx, hd, R, f=1):
    ctx.save()
    for dx, dy, rx, ry in ((0.14, 0.52, 0.36, 0.16), (-0.35, 0.3, 0.14, 0.1), (0.55, 0.15, 0.12, 0.09), (0.2, -0.45, 0.1, 0.07)):
        ellipse(ctx, hd[0] + f * R * dx, hd[1] + R * dy, R * rx, R * ry); setc(ctx, CHOC + (0.85,)); ctx.fill()
    ctx.restore()


def tp_strip(ctx, pts, w=34):
    ctx.new_path(); ctx.move_to(*pts[0])
    for i in range(1, len(pts) - 2, 3):
        ctx.curve_to(*pts[i], *pts[i + 1], *pts[i + 2])
    path = ctx.copy_path()
    ink(ctx, w + 10); ctx.stroke()
    ctx.append_path(path); setc(ctx, WHITE); ctx.set_line_width(w); ctx.stroke()


def tp_roll(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rect_r(ctx, -40, -50, 80, 100, 16); fl(ctx, WHITE, 6)
    ellipse(ctx, -40, 0, 14, 50); fl(ctx, hx('eeeeee'), 5)
    ellipse(ctx, -40, 0, 6, 20); fl(ctx, hx('c8a070'), 3)
    ctx.restore()


def mummy(ctx, b, s, lf):
    """wrap toilet paper bands over a drawn kid (b = draw() result, s = scale)"""
    hx_, hy_ = b['head']; R = b['R']
    rnd = random.Random(9)
    # body bands
    for k in range(6):
        y = hy_ + R * 0.95 + k * 34 * s
        ctx.new_path(); ctx.move_to(hx_ - 80 * s, y + rnd.uniform(-8, 8)); ctx.line_to(hx_ + 80 * s, y - 14 * s + rnd.uniform(-8, 8))
        ink(ctx, 32 * s); ctx.stroke()
        ctx.new_path(); ctx.move_to(hx_ - 80 * s, y + rnd.uniform(-8, 8)); ctx.line_to(hx_ + 80 * s, y - 14 * s + rnd.uniform(-8, 8))
        setc(ctx, WHITE); ctx.set_line_width(24 * s); ctx.stroke()
    # head bands (leave the eye slot)
    for dy in (-0.75, -0.45, 0.42, 0.68):
        ctx.new_path(); ctx.move_to(hx_ - R * 1.05, hy_ + R * dy); ctx.line_to(hx_ + R * 1.05, hy_ + R * dy - R * 0.08)
        ink(ctx, R * 0.3); ctx.stroke()
        ctx.new_path(); ctx.move_to(hx_ - R * 1.05, hy_ + R * dy); ctx.line_to(hx_ + R * 1.05, hy_ + R * dy - R * 0.08)
        setc(ctx, WHITE); ctx.set_line_width(R * 0.22); ctx.stroke()
    # trailing strip
    tp_strip(ctx, [(hx_ + 70 * s, hy_ + R * 2), (hx_ + 150 * s, hy_ + R * 2.2 + 20 * math.sin(lf * 0.3)),
                   (hx_ + 200 * s, hy_ + R * 3), (hx_ + 260 * s, hy_ + R * 3.4)], 22 * s)


def dog(ctx, x, y, s=1.0, f=1, lf=0, tache_col=None, spots=False, sleep=False):
    """original flat doodle dog, (x, y) = feet line centre"""
    ctx.save(); ctx.translate(x, y); ctx.scale(f * s, s)
    fur = hx('e8b878'); dk = hx('b9844a')
    wag = math.sin(lf * 0.9) * 0.5
    # tail
    ctx.save(); ctx.translate(-120, -150); ctx.rotate(-0.6 + wag)
    ctx.new_path(); ctx.move_to(0, 0); ctx.curve_to(-30, -40, -40, -80, -20, -110); ink(ctx, 30); ctx.stroke()
    ctx.new_path(); ctx.move_to(0, 0); ctx.curve_to(-30, -40, -40, -80, -20, -110); setc(ctx, fur); ctx.set_line_width(20); ctx.stroke()
    ctx.restore()
    # legs
    for lx in (-90, -50, 60, 100):
        rect_r(ctx, lx - 18, -100, 36, 100, 16); fl(ctx, dk if lx in (-50, 100) else fur, 6)
    # body
    ellipse(ctx, 0, -140, 150, 75); fl(ctx, fur, 7)
    if spots:
        for sx, sy, r in ((-60, -150, 26), (10, -170, 20), (40, -120, 22), (-20, -110, 16)):
            ellipse(ctx, sx, sy, r, r * 0.8); setc(ctx, BLUE); ctx.fill()
    # head
    ellipse(ctx, 140, -230, 80, 72); fl(ctx, fur, 7)
    ellipse(ctx, 200, -205, 44, 32); fl(ctx, hx('f6d6a8'), 6)
    ellipse(ctx, 236, -216, 16, 12); setc(ctx, INK); ctx.fill()
    # ear
    ctx.new_path(); ctx.move_to(100, -290); ctx.curve_to(60, -280, 50, -200, 80, -180); ctx.curve_to(110, -200, 120, -260, 100, -290)
    fl(ctx, dk, 6)
    # eye
    if sleep:
        ink(ctx, 6); ctx.new_path(); ctx.arc(160, -250, 12, 0.2, math.pi - 0.2); ctx.stroke()
    else:
        ellipse(ctx, 160, -250, 13, 17); setc(ctx, INK); ctx.fill()
        ellipse(ctx, 156, -256, 5, 5); setc(ctx, WHITE); ctx.fill()
    # tongue
    if not sleep:
        ctx.new_path(); ctx.move_to(200, -180); ctx.curve_to(200, -150, 225, -150, 225, -180); fl(ctx, hx('ff6f86'), 5)
    if tache_col:
        for sgn in (-1, 1):
            ctx.new_path(); ctx.move_to(205, -192); ctx.curve_to(205 + sgn * 18, -205, 205 + sgn * 40, -180, 205 + sgn * 46, -200)
            setc(ctx, tache_col); ctx.set_line_width(11); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ellipse(ctx, 120, -175, 60, 14); setc(ctx, RED); ctx.fill_preserve(); ink(ctx, 5); ctx.stroke()   # collar
    ctx.restore()


def pot(ctx, x, y, s=1.0, a=0.0, col=hx('9aa4b8')):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -80, -40, 160, 80, 14); fl(ctx, col, 6)
    rect_r(ctx, -96, -52, 192, 22, 10); fl(ctx, light(col, 0.2), 6)
    rect_r(ctx, 90, -20, 60, 16, 8); fl(ctx, hx('3a2a40'), 4)
    ctx.restore()


def spoon(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -9, -10, 18, 130, 8); fl(ctx, hx('d49a5a'), 5)
    ellipse(ctx, 0, -30, 26, 36); fl(ctx, hx('d49a5a'), 5)
    ctx.restore()


def wrapper(ctx, x, y, a, col):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    poly(ctx, [(-40, -18), (40, -22), (44, 16), (-36, 20)]); fl(ctx, col, 4)
    ctx.move_to(-20, -2); ctx.line_to(20, -4); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def choc_bar(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -50, -30, 100, 60, 6); fl(ctx, CHOC, 5)
    for k in (-25, 0, 25):
        ctx.move_to(k, -28); ctx.line_to(k, 28)
    ctx.move_to(-48, 0); ctx.line_to(48, 0); setc(ctx, dark(CHOC, 0.7)); ctx.set_line_width(4); ctx.stroke()
    rect_r(ctx, -54, 0, 108, 40, 4); fl(ctx, PURPLE, 5)
    ctx.restore()


# ------------------------------------------------------------------ sets
def hallway(ctx, door=0.0):
    ctx.rectangle(-3000, -3000, 9000, 7000); setc(ctx, hx('cfe7ff')); ctx.fill()
    for k in range(-30, 60):
        ctx.rectangle(k * 140, -3000, 70, 4450)
    setc(ctx, hx('bcdcff')); ctx.fill()
    # frames on the wall
    for x, c in ((-260, GOLD), (380, PINK), (1500, GREEN)):
        rect_r(ctx, x, 700, 200, 160, 8); fl(ctx, c, 7)
        rect_r(ctx, x + 18, 718, 164, 124, 4); fl(ctx, hx('fff8e8'), 4)
        ctx.new_path(); ctx.arc(x + 100, 790, 30, 0, 2 * math.pi); fl(ctx, c, 4)
    # kid's door at x 900..1260
    rect_r(ctx, 880, 720, 400, 760, 12); fl(ctx, hx('8a5a3a'), 9)
    ctx.save(); ctx.rectangle(900, 740, 360, 740); setc(ctx, hx('fff2a0')); ctx.fill(); ctx.restore()
    dw = 360 * (1 - door)
    rect_r(ctx, 900, 740, max(14, dw), 740, 6); fl(ctx, hx('ff8a1f'), 7)
    if door < 0.5:
        ellipse(ctx, 900 + dw - 40, 1110, 18, 18); fl(ctx, GOLD, 5)
        rect_r(ctx, 980, 830, 180, 70, 10); fl(ctx, WHITE, 5)
        text(ctx, "KEEP OUT", 1070, 865, 34, RED, ow=0, shadow=False)
    ctx.rectangle(-3000, 1480, 9000, 3000); setc(ctx, hx('b97a48')); ctx.fill()
    ctx.move_to(-3000, 1480); ctx.line_to(6000, 1480); ink(ctx, 7); ctx.stroke()
    rect_r(ctx, -400, 1540, 2400, 90, 40); fl(ctx, hx('ff6b8a'), 6)


def kidroom(ctx, art=1.0):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('fff6d8')); ctx.fill()
    wall_art(ctx, 40, 560, 1040, 1300, art)
    ctx.rectangle(-3000, 1450, 7000, 3000); setc(ctx, hx('7fd0ff')); ctx.fill()
    ctx.move_to(-3000, 1450); ctx.line_to(4000, 1450); ink(ctx, 7); ctx.stroke()


def bathroom(ctx):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('dff7f2')); ctx.fill()
    for i in range(-10, 20):
        for j in range(-10, 30):
            ctx.rectangle(i * 110 + 4, j * 110 + 4, 102, 102)
    setc(ctx, hx('c6efe6')); ctx.fill()
    # tub on the right
    rect_r(ctx, 640, 1180, 520, 300, 60); fl(ctx, WHITE, 8)
    # toilet on the left
    rect_r(ctx, 40, 1040, 170, 200, 20); fl(ctx, WHITE, 7)
    ellipse(ctx, 160, 1300, 140, 60); fl(ctx, WHITE, 7)
    rect_r(ctx, 100, 1300, 120, 180, 20); fl(ctx, WHITE, 7)
    ctx.rectangle(-3000, 1480, 7000, 3000); setc(ctx, hx('6fb7c8')); ctx.fill()
    ctx.move_to(-3000, 1480); ctx.line_to(4000, 1480); ink(ctx, 7); ctx.stroke()


def yard(ctx):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('8fd8ff')); ctx.fill()
    ellipse(ctx, 220, 640, 90, 44); setc(ctx, WHITE); ctx.fill(); ellipse(ctx, 300, 620, 70, 50); ctx.fill()
    ctx.new_path(); ctx.arc(900, 560, 80, 0, 2 * math.pi); fl(ctx, YEL, 6)
    # fence
    for k in range(-4, 14):
        poly(ctx, [(k * 100, 1300), (k * 100, 1000), (k * 100 + 40, 960), (k * 100 + 80, 1000), (k * 100 + 80, 1300)]); fl(ctx, WHITE, 5)
    ctx.rectangle(-3000, 1080, 7000, 30); fl(ctx, WHITE, 5)
    ctx.rectangle(-3000, 1300, 7000, 3000); setc(ctx, hx('5cc85a')); ctx.fill()
    ctx.move_to(-3000, 1300); ctx.line_to(4000, 1300); ink(ctx, 7); ctx.stroke()


def kitchen(ctx):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('ffe3c2')); ctx.fill()
    for k in range(-20, 30):
        ctx.rectangle(k * 90, 1100, 86, 40)
    setc(ctx, hx('ffd2a0')); ctx.fill()
    rect_r(ctx, -200, 1300, 1500, 300, 10); fl(ctx, hx('5aa0e0'), 8)
    ctx.rectangle(-3000, 1560, 7000, 3000); setc(ctx, hx('c98a52')); ctx.fill()


def pantry(ctx, door=1.0, lf=0):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('3a2a50')); ctx.fill()
    # doorway with warm light
    rect_r(ctx, 120, 420, 840, 1300, 14); fl(ctx, hx('6b4a2a'), 10)
    ctx.rectangle(150, 450, 780, 1260); setc(ctx, hx('ffe9a8')); ctx.fill()
    # shelves with jars
    for sy in (640, 900, 1160):
        ctx.rectangle(150, sy, 780, 22); fl(ctx, hx('b97a48'), 5)
        for k in range(5):
            jx = 210 + k * 150
            rect_r(ctx, jx, sy - 110, 90, 110, 14); fl(ctx, (RED, BLUE, GREEN, ORANGE, PINK)[(k + sy // 100) % 5], 5)
            rect_r(ctx, jx - 6, sy - 126, 102, 22, 6); fl(ctx, WHITE, 4)
    # SECRET box on a shelf, open
    rect_r(ctx, 640, 1260, 260, 140, 10); fl(ctx, PURPLE, 6)
    text(ctx, "MOM'S", 770, 1310, 40, YEL, ow=0, shadow=False)
    text(ctx, "SECRET", 770, 1360, 40, YEL, ow=0, shadow=False)
    ctx.rectangle(150, 1700, 780, 30); setc(ctx, hx('8a5a3a')); ctx.fill()
    # door swinging (on the right hinge)
    dw = 780 * (1 - door)
    if dw > 4:
        rect_r(ctx, 930 - dw, 450, dw, 1260, 8); fl(ctx, hx('ff8a1f'), 8)


# ------------------------------------------------------------------ close-ups
def mom_ecu(ctx, f, lf, bg, eye='shock', mouth='flat', z0=1.0, shake=0, look=0.0, tea=True, ray_col=(1, 1, 1), tw=False):
    ctx.save(); cam(ctx, 540, 960, z0, 0, shake, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    rays(ctx, 540, 880, 260, 1700, lf * 0.02, col=ray_col, a=0.3, n=18)
    cx, cy, R = 540 + look, 880, 300
    face(ctx, MOM, P(eye=eye, mouth=mouth, head=0), cx, cy, R, 0.02 * math.sin(lf * 0.4))
    if eye == 'shock':
        sweat(ctx, cx + 1.02 * R, cy - 0.4 * R, lf, 1.3)
    if tw:
        twitch(ctx, cx + 0.5 * R, cy - 0.55 * R, lf, 1.3)
    if tea:
        mug(ctx, cx - 280, cy + 380, 1.6, lf)
    ctx.restore()
    return cx, cy, R


def silence_waves(ctx, lf, y=1440):
    """tiny '...' bubbles drifting = silence"""
    for k in range(3):
        a = 0.5 + 0.5 * math.sin(lf * 0.25 - k * 0.9)
        ctx.new_path(); ctx.arc(470 + k * 70, y, 16, 0, 2 * math.pi); setc(ctx, (1, 1, 1, a)); ctx.fill_preserve()
        setc(ctx, OUT + (a,)); ctx.set_line_width(5); ctx.stroke()


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    mom_ecu(ctx, f, f, PURPLE, 'shock', 'flat', z0=1.0 + 0.08 * eout(pop(f, 0, 60)), look=10 * math.sin(f * 0.3), ray_col=(1, 0.9, 1))
    card(ctx, 'p1', f, -6, 56)
    label(ctx, "*silence*", 540, 1460, 100, WHITE, -0.04, pop(f, 8, 12))


def s2(ctx, f):
    lf = f - 60
    if lf < 40:
        # side tracking: tiptoe down the hallway
        px = 200 + lf * 12
        ctx.save(); cam(ctx, px + 160, 1100, 0.9, 0, 0, f)
        hallway(ctx, 0)
        tip = math.sin(lf * 0.45)
        draw(ctx, px, 1500 - 186 * 1.75 + 10, 1.75, 1, MOM,
             P(eye='shock', mouth='flat', rsh=110, rel=-70, lsh=-110, lel=60, torso=12, head=6, lhip=-12 + 20 * tip, rhip=12 - 20 * tip, lkn=20, rkn=20))
        ctx.restore()
        label1(ctx, "*tiptoe... tiptoe...*", WHITE, pop(lf, 2, 6), 90, 0.03, y=1460)
        if lf >= 20:
            label(ctx, "*scribble scribble*", 600, 600, 80, YEL, -0.05, pop(lf, 20, 24))
    elif lf < 92:
        il = lf - 40
        sh = shake_at(il, [0], 10, 22)
        ctx.save(); cam(ctx, 540, 1030, 1.0 + 0.04 * eout(pop(il, 0, 50)), 0, sh, f)
        kidroom(ctx, 1.0)
        b = draw(ctx, 560, 1560 - 186 * 1.5, 1.5, 1, BOY, P(eye='shock', mouth='open', rsh=-150, rel=-10, lsh=20, head=-4))
        crayon(ctx, b['front'][0], b['front'][1] - 40, 0.3, RED, 1.2)
        crayon(ctx, b['back'][0], b['back'][1], -0.4, BLUE, 1.2)
        tache(ctx, b['head'], b['R'], 1, GREEN)
        ctx.restore()
        label(ctx, "*CREEEAK*", 540, 560, 110, WHITE, -0.05, pop(il, 0, 4))
        if il >= 14:
            label1(ctx, "\"THE WALL!!\"", RED, pop(il, 14, 18), 140, 0.04, y=1460)
    else:
        il = lf - 92
        # kid ECU, proud
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.1 * eout(pop(il, 0, 48)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, GOLD); ctx.fill()
        rays(ctx, 540, 900, 260, 1700, il * 0.03, a=0.45, n=18)
        R = 300; hd = (540, 900)
        face(ctx, BOY, P(eye='happy', mouth='grin'), 540, 900, R)
        tache(ctx, (hd[0] - R * 0.08, hd[1] + R * 0.07), R * 1.0, 1, GREEN)
        crayon(ctx, 830, 1230, 0.4, RED, 1.6)
        ctx.restore()
        sparkle(ctx, 200, 640, 46 + 8 * math.sin(il * 0.5)); sparkle(ctx, 880, 700, 36)
        label2(ctx, "\"...it's", "ART!\"", WHITE, pop(il, 3, 7), 140, col2=GREEN, y=1420)


def s3(ctx, f):
    lf = f - 200
    if lf < 34:
        cx, cy, R = mom_ecu(ctx, f, lf, BLUE, 'normal' if lf < 12 else 'shock', 'flat', z0=1.0 + 0.06 * eout(pop(lf, 10, 20)),
                            look=-60 * eio(pop(lf, 12, 18)), ray_col=(0.85, 0.9, 1))
        card(ctx, 'p2', f, 200, 232)
        if lf >= 12:
            label2(ctx, "...too quiet.", "AGAIN.", WHITE, pop(lf, 12, 16), 110, col2=YEL, y=1420)
        else:
            silence_waves(ctx, lf)
    elif lf < 92:
        il = lf - 34
        ctx.save(); cam(ctx, 540, 1080, 1.0, -4 + 4 * eio(pop(il, 0, 20)), shake_at(il, [10], 12, 22), f)
        bathroom(ctx)
        # paper everywhere
        tp_strip(ctx, [(-50, 700), (200, 600), (400, 900), (600, 760), (800, 620), (1000, 880), (1150, 760)], 40)
        tp_strip(ctx, [(-50, 1350), (250, 1250), (400, 1500), (700, 1420), (900, 1320), (1050, 1560), (1150, 1450)], 40)
        tp_strip(ctx, [(160, 1050), (200, 900), (120, 760), (240, 560)], 34)
        for x, y in ((230, 1520), (420, 1470), (880, 1500)):
            tp_roll(ctx, x, y, 0.8)
        rise = eout(pop(il, 6, 14))
        b = draw(ctx, 560, 1560 - 186 * 1.5 + 300 * (1 - rise), 1.5, 1, BOY,
                 P(eye='shock' if il >= 10 else 'normal', mouth='scream' if il >= 10 else 'flat', rsh=-120, rel=-40, lsh=120, lel=40))
        mummy(ctx, b, 1.5 * 1.35 / 1.5, il)
        # pile of paper in front
        for k in range(7):
            ellipse(ctx, 330 + k * 75, 1560, 90, 50); fl(ctx, WHITE, 6)
        ctx.restore()
        if il >= 10:
            label2(ctx, "\"BOO!", "I'm a MUMMY!\"", WHITE, pop(il, 10, 14), 110, col2=YEL, y=520)
        else:
            label(ctx, "*rustle rustle*", 540, 600, 90, WHITE, 0.04, pop(il, 0, 4))
    else:
        il = lf - 92
        mom_ecu(ctx, f, il, RED, 'glare', 'wavy', z0=1.05 + 0.08 * eout(pop(il, 0, 38)), shake=2, tea=False, ray_col=(1, 0.8, 0.6), tw=True)
        label2(ctx, "\"...that was", "12 ROLLS.\"", WHITE, pop(il, 4, 8), 120, col2=YEL, y=1420)


def s4(ctx, f):
    lf = f - 330
    if lf < 70:
        il = lf
        ctx.save(); cam(ctx, 540 + 30 * eio(pop(il, 0, 70)), 1060, 1.0 + 0.08 * eio(pop(il, 0, 70)), 0, shake_at(il, [30, 46], 8, 12), f)
        yard(ctx)
        hop = abs(math.sin(il * 0.3)) * 40 if il > 26 else 0
        b = draw(ctx, 300, 1520 - 186 * 1.5 - hop, 1.5, 1, BOY, P(eye='happy', mouth='grin', rsh=-150, rel=-20, lsh=150, lel=20))
        tache(ctx, b['head'], b['R'], 1, BLUE)
        for sx, sy in ((-30, 120), (30, 170), (0, 230)):
            ellipse(ctx, b['head'][0] + sx, b['head'][1] + sy, 18, 14); setc(ctx, BLUE); ctx.fill()
        dog(ctx, 700, 1500 - hop * 0.5, 1.2, -1, il, tache_col=BLUE, spots=True)
        ctx.restore()
        card(ctx, 'p3', f, 330, 362)
        if il >= 26:
            label2(ctx, "\"We're", "TWINS!\"", WHITE, pop(il, 26, 30), 140, col2=BLUE, y=1440)
        if il >= 46:
            label(ctx, "*WOOF!*", 830, 640, 100, YEL, 0.08, pop(il, 46, 49))
    else:
        il = lf - 70
        # split screen: kid banging pots (top) / relaxed Mom (bottom)
        bang = [0, 10, 20, 30, 38, 46, 54, 62]
        ctx.save(); ctx.rectangle(0, 0, W, 955); ctx.clip()
        cam(ctx, 540, 1140, 1.0, 0, shake_at(il, bang, 6, 14), f, sy=560)
        kitchen(ctx)
        hit = any(t <= il < t + 4 for t in bang)
        b = draw(ctx, 540, 1560 - 186 * 1.5, 1.5, 1, BOY, P(eye='happy', mouth='scream', rsh=-150 if not hit else -60, rel=-20, lsh=150 if not hit else 60, lel=20))
        spoon(ctx, b['front'][0], b['front'][1], 2.6 if not hit else 1.9, 1.2)
        spoon(ctx, b['back'][0], b['back'][1], -2.6 if not hit else -1.9, 1.2)
        pot(ctx, 330, 1520, 1.1, -0.1); pot(ctx, 760, 1520, 1.1, 0.1, hx('ff8a1f'))
        ctx.restore()
        ctx.save(); ctx.rectangle(0, 965, W, 955); ctx.clip()
        cam(ctx, 540, 900, 0.75, 0, 0, f, sy=1400)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, TEAL); ctx.fill()
        rays(ctx, 540, 880, 220, 1600, il * 0.02, a=0.25, n=16)
        face(ctx, MOM, P(eye='closed', mouth='smile'), 540, 880, 300, 0.05 * math.sin(il * 0.1))
        mug(ctx, 300, 1180, 1.6, il)
        ctx.restore()
        ctx.rectangle(0, 952, W, 16); setc(ctx, OUT); ctx.fill()
        for t in bang:
            if t <= il < t + 8:
                k = bang.index(t) % 2
                label(ctx, ("*BANG!*", "*CLANG!*")[k], (330, 750)[k], 400, 110, (YEL, ORANGE)[k], (-0.1, 0.1)[k], pop(il, t, t + 3))
        label2(ctx, "\"Ahh... NOISE", "is GOOD.\"", WHITE, pop(il, 8, 12), 90, col2=YEL, y=1100)


def s5(ctx, f):
    lf = f - 470
    if lf < 26:
        mom_ecu(ctx, f, lf, PURPLE, 'shock', 'flat', z0=1.0 + 0.1 * eout(pop(lf, 0, 8)), shake=shake_at(lf, [0], 8, 12), ray_col=(1, 0.9, 1))
        label(ctx, "*...silence*", 540, 1460, 100, WHITE, -0.04, pop(lf, 2, 6))
    elif lf < 60:
        il = lf - 26
        ctx.save(); cam(ctx, 540, 1200, 1.15, 0, 0, f)
        kitchen(ctx)
        # kid asleep across the pots, dog asleep too
        pot(ctx, 420, 1530, 1.1, -0.1); pot(ctx, 680, 1540, 1.1, 0.15, hx('ff8a1f'))
        draw(ctx, 560, 1480 - 186 * 1.4, 1.4, 1, BOY, P(eye='closed', mouth='open', rot=-80, rsh=60, lsh=-60))
        dog(ctx, 870, 1580, 0.8, -1, 0, sleep=True)
        ctx.restore()
        zzz(ctx, 470, 980, il, 1.6)
        label2(ctx, "\"Aww...", "PHEW.\"", WHITE, pop(il, 6, 10), 120, col2=PINK, y=1440)
    elif lf < 92:
        il = lf - 60
        cx, cy, R = mom_ecu(ctx, f, il, BLUE, 'smug' if il < 12 else 'shock', 'smile' if il < 12 else 'flat',
                            z0=1.0 + 0.12 * eout(pop(il, 12, 20)), look=-40 * eio(pop(il, 12, 18)), ray_col=(0.85, 0.9, 1))
        if il >= 12:
            label2(ctx, "\"...wait.", "Where's DAD?\"", WHITE, pop(il, 12, 16), 120, col2=YEL, y=1420)
        else:
            silence_waves(ctx, il)
    elif lf < 158:
        il = lf - 92
        door = eio(pop(il, 0, 18))
        ctx.save(); cam(ctx, 540, 1060, 1.0 + 0.1 * eout(pop(il, 18, 66)), -8 * eio(pop(il, 14, 24)), shake_at(il, [20], 8, 16), f)
        pantry(ctx, door, il)
        # Dad on the floor in a sea of wrappers
        rnd = random.Random(3)
        for k in range(16):
            wrapper(ctx, 230 + rnd.uniform(0, 600), 1560 + rnd.uniform(-40, 120), rnd.uniform(-1, 1), (PURPLE, RED, GOLD, BLUE)[k % 4])
        if door > 0.3:
            b = draw(ctx, 450, 1640 - 186 * 1.6, 1.6, 1, DAD,
                     P(torso=2, lsh=30, lel=-110, rsh=34, rel=-120, lhip=86, lkn=-86, rhip=88, rkn=-88,
                       eye='shock' if il >= 20 else 'happy', mouth='open' if il < 20 else 'grin'))
            choc_smear(ctx, b['head'], b['R'], 1)
            choc_bar(ctx, b['front'][0] + 10, b['front'][1] - 30, -0.3, 1.2)
        ctx.restore()
        if il < 18:
            label(ctx, "*CREEEAK*", 540, 560, 110, WHITE, -0.05, pop(il, 0, 4))
        elif il < 36:
            label(ctx, "*munch munch*", 540, 560, 110, CHOC, 0.04, pop(il, 4, 8)) if il < 20 else None
            label(ctx, "*FREEZE*", 540, 560, 120, BLUE, 0.04, pop(il, 20, 23))
        if il >= 36:
            label2(ctx, "\"...it's", "ART?\"", WHITE, pop(il, 36, 40), 140, col2=CHOC, y=600)
    else:
        il = lf - 158
        mom_ecu(ctx, f, il, PURPLE, 'shock', 'flat', z0=1.0, look=10 * math.sin(il * 0.3), ray_col=(1, 0.9, 1))
        card(ctx, 'p1', f, 628 - 2)
        label(ctx, "*silence*", 540, 1460, 100, WHITE, -0.04, 1)


SHOTS = [(0, s1), (60, s2), (200, s3), (330, s4), (470, s5)]
CUTS = (60, 100, 152, 200, 234, 292, 330, 400, 470, 496, 530, 562, 628)


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.22)
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
                              "-i", "out/too_quiet_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()