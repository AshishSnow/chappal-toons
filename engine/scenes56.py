"""'Can I Help?' - original, general-audience comedy short, 22s.
Hook: ECU kid in a chef hat, flour on the cheeks, sparkly eyes, whisk up: "CAN I HELP?!" -> Mom's frozen smile, eye twitch: "...sure, sweetie."
Beat 1: top-down bowl: the egg gets SMASHED in fist-first *CRUNCH* -> medium: "I added EXTRA egg!" / Mom with a magnifying glass: "...and EXTRA shell."
Beat 2: mixer dial LOW -> MED -> MAX *click* -> wide batter tornado, splats on every wall -> low angle: ceiling drip *PLOP* onto Mom's head.
Beat 3: kid rips the flour bag *POOF* white-out -> split: ghost-white kid "WE'RE A GREAT TEAM!" / ghost-white Mom twitching "...so great."
Twist: "Can you help me CLEAN UP?" -> *ZOOM* kid vanishes, kid-shaped flour cloud left behind.
 Mom finally alone with a slice of cake... kid pops up from behind the counter with a fork: "Can I help... EAT IT?!" -> opening face (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos, zigs
from scenes48 import label1, label2
from scenes53 import kitchen, table
import scenes13
from scenes13 import card as _card13
import random

BOY = dict(doodle.BOY, hood=False, shirt=hx('ff5fa8'), pants=hx('3d7bff'))
MOM = dict(doodle.MOM_G)
FLOUR = hx('f6f3ee')
WBOY = dict(BOY, skin=hx('f2eee8'), hair=hx('e4e0da'), shirt=hx('ffffff'), pants=hx('e8e6e2'), shoes=hx('f0eeea'))
WMOM = dict(MOM, skin=hx('f2eee8'), hair=hx('e4e0da'), shirt=hx('ffffff'), pants=hx('e8e6e2'), shoes=hx('f0eeea'))
N = 660
FLOOR = 1460
TOP = 1180          # counter top
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
BATTER = hx('ffd98a')
YOLK = hx('ffb21f')

CAPS = {
    'p1': [[("WHEN YOUR KID", OUT)], [("WANTS TO HELP", PINK)]],
    'p2': [[("STEP 1:", OUT)], [("ADD ONE EGG", ORANGE)]],
    'p3': [[("STEP 2:", OUT)], [("MIX GENTLY", BLUE)]],
    'p4': [[("STEP 3:", OUT)], [("ADD FLOUR", PURPLE)]],
    'p5': [[("STEP 4:", OUT)], [("CLEAN UP", GREEN)]],
}
scenes13.CAPS = CAPS
card = _card13

_DUMMY = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4))


# ------------------------------------------------------------------ props
def chef_hat(ctx, x, y, R, a=0.0, col=(1, 1, 1)):
    """chef hat sitting on a head centred (x, y) of radius R"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    for px, py, r in ((-0.5, -1.55, 0.48), (0.5, -1.55, 0.48), (0, -1.85, 0.55)):
        ellipse(ctx, px * R, py * R, r * R, r * R * 0.9); fl(ctx, col, max(4, R * 0.03))
    rect_r(ctx, -0.82 * R, -1.42 * R, 1.64 * R, 0.5 * R, 0.08 * R); fl(ctx, col, max(4, R * 0.03))
    for k in (-0.4, 0.0, 0.4):
        ctx.move_to(k * R, -1.38 * R); ctx.line_to(k * R, -1.0 * R); setc(ctx, (0.85, 0.85, 0.9)); ctx.set_line_width(R * 0.025); ctx.stroke()
    ctx.restore()


def splat(ctx, x, y, r, seed=1, col=BATTER, a=1.0):
    rnd = random.Random(seed)
    ctx.new_path()
    n = 14
    for i in range(n + 1):
        ang = i * 2 * math.pi / n
        rr = r * (1.0 + (0.45 if i % 2 else 0) * rnd.uniform(0.5, 1.2))
        px, py = x + math.cos(ang) * rr, y + math.sin(ang) * rr * 0.85
        ctx.line_to(px, py) if i else ctx.move_to(px, py)
    ctx.close_path(); setc(ctx, col + (a,)) if len(col) == 3 else setc(ctx, col); ctx.fill_preserve(); setc(ctx, INK + (a,)); ctx.set_line_width(max(3, r * 0.06)); ctx.stroke()
    for k in range(3):
        ellipse(ctx, x + rnd.uniform(-2, 2) * r, y + rnd.uniform(-2, 2) * r, r * 0.18, r * 0.16); setc(ctx, col[:3] + (a,)); ctx.fill_preserve(); setc(ctx, INK + (a,)); ctx.set_line_width(3); ctx.stroke()


def bowl(ctx, x, y, s=1.0, fill=BATTER, shells=0, seed=4):
    """side-view mixing bowl, rim centre at (x, y)"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 200, 46); fl(ctx, hx('5ab8ff'), 7)
    ellipse(ctx, 0, 4, 176, 34); setc(ctx, fill); ctx.fill()
    rnd = random.Random(seed)
    for k in range(shells):
        sx, sy = rnd.uniform(-140, 140), rnd.uniform(-10, 18)
        poly(ctx, [(sx - 16, sy), (sx - 4, sy - 14), (sx + 6, sy - 4), (sx + 16, sy - 12), (sx + 14, sy + 6)]); fl(ctx, (1, 1, 1), 3)
    ctx.move_to(-200, 0); ctx.curve_to(-190, 170, 190, 170, 200, 0); ctx.close_path(); fl(ctx, hx('5ab8ff'), 7)
    ctx.move_to(-150, 50); ctx.curve_to(-120, 110, -60, 125, -20, 128); setc(ctx, (1, 1, 1, 0.55)); ctx.set_line_width(12); ctx.stroke()
    ctx.restore()


def egg(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 52, 66); fl(ctx, hx('fff6e6'), 6)
    ellipse(ctx, -16, -24, 10, 18, -0.3); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.restore()


def shell_bits(ctx, x, y, t, n=16, spread=520, seed=2):
    if not 0 < t < 1.3:
        return
    rnd = random.Random(seed)
    for i in range(n):
        a = rnd.uniform(0, 2 * math.pi)
        d = spread * eout(min(1, t)) * rnd.uniform(0.3, 1.0)
        px, py = x + math.cos(a) * d, y + math.sin(a) * d * 0.7 + 200 * t * t
        ctx.save(); ctx.translate(px, py); ctx.rotate(a + t * 8)
        s = rnd.uniform(0.8, 1.6)
        poly(ctx, [(-18 * s, 0), (-5 * s, -15 * s), (6 * s, -4 * s), (18 * s, -13 * s), (15 * s, 8 * s)]); fl(ctx, (1, 1, 1), 4)
        ctx.restore()


def mixer(ctx, x, y, s=1.0, a=0.0, spin=0.0, col=hx('ff8a1f')):
    """hand mixer: (x, y) = handle grip; beaters point down"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    for bx in (-28, 28):
        ctx.move_to(bx, 60); ctx.line_to(bx, 200); setc(ctx, INK); ctx.set_line_width(14); ctx.stroke()
        ctx.move_to(bx, 60); ctx.line_to(bx, 200); setc(ctx, hx('d0d6e6')); ctx.set_line_width(7); ctx.stroke()
        w = 26 * math.cos(spin + bx)
        ellipse(ctx, bx, 220, abs(w) + 6, 34); setc(ctx, INK); ctx.set_line_width(9); ctx.stroke()
        ellipse(ctx, bx, 220, abs(w) + 6, 34); setc(ctx, hx('d0d6e6')); ctx.set_line_width(4); ctx.stroke()
    rect_r(ctx, -110, -10, 220, 90, 30); fl(ctx, col, 7)
    ctx.move_to(-80, -10); ctx.curve_to(-80, -90, 80, -90, 80, -10); setc(ctx, INK); ctx.set_line_width(36); ctx.stroke()
    ctx.move_to(-80, -10); ctx.curve_to(-80, -90, 80, -90, 80, -10); setc(ctx, col); ctx.set_line_width(22); ctx.stroke()
    ellipse(ctx, 70, 34, 14, 14); fl(ctx, RED, 4)
    ctx.restore()


def flour_bag(ctx, x, y, s=1.0, a=0.0, torn=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-120, -170), (120, -170), (135, 170), (-135, 170)]); fl(ctx, hx('fff4dc'), 7)
    rect_r(ctx, -95, -40, 190, 110, 18); fl(ctx, hx('ffd23f'), 5)
    text(ctx, "FLOUR", 0, 34, 54, RED, outline=(1, 1, 1, 0), ow=1, shadow=False)
    if torn > 0:
        ctx.move_to(-120, -170)
        for i in range(9):
            ctx.line_to(-120 + i * 30, -170 + (18 if i % 2 else -6) * torn)
        setc(ctx, INK); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def flour_cloud(ctx, cx, cy, r, seed=3, a=1.0, lf=0):
    if r < 2:
        return
    rnd = random.Random(seed)
    for k in range(18):
        ang = rnd.uniform(0, 2 * math.pi); d = rnd.uniform(0, r)
        rr = rnd.uniform(0.35, 0.6) * r * (1 + 0.04 * math.sin(lf * 0.3 + k))
        ellipse(ctx, cx + math.cos(ang) * d, cy + math.sin(ang) * d * 0.8, rr, rr * 0.85)
        setc(ctx, (0.97, 0.96, 0.94, a)); ctx.fill_preserve(); setc(ctx, (0.8, 0.79, 0.78, a * 0.8)); ctx.set_line_width(4); ctx.stroke()


def cake(ctx, x, y, s=1.0, shells=True, slice_out=False):
    """lopsided cake on a plate, base centre at (x, y)"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 6, 200, 30); fl(ctx, (1, 1, 1), 6)
    poly(ctx, [(-150, 0), (150, 0), (140, -150), (-130, -220)]); fl(ctx, hx('ffcf7a'), 7)
    ctx.move_to(-130, -220); ctx.curve_to(-60, -250, 60, -190, 140, -150); ctx.line_to(145, -110)
    for i in range(6):
        ctx.line_to(145 - i * 50, -110 - i * 18 + (14 if i % 2 else -6))
    ctx.line_to(-133, -175); ctx.close_path(); fl(ctx, hx('ff8ac0'), 6)
    if slice_out:
        poly(ctx, [(40, 0), (150, 0), (143, -145), (40, -180)]); setc(ctx, hx('fff4dc')); ctx.fill()
        ctx.move_to(40, 0); ctx.line_to(40, -180); ink(ctx, 6); ctx.stroke()
    if shells:
        for sx, sy, sa in ((-80, -235, 0.4), (20, -215, -0.6), (-20, -120, 1.2), (90, -80, 0.2)):
            if slice_out and sx > 40:
                continue
            ctx.save(); ctx.translate(sx, sy); ctx.rotate(sa)
            poly(ctx, [(-20, 10), (-8, -22), (6, -6), (20, -24), (18, 10)]); fl(ctx, (1, 1, 1), 4)
            ctx.restore()
    ctx.restore()


def mop(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(0, -400); ctx.line_to(0, 0); setc(ctx, INK); ctx.set_line_width(26); ctx.stroke()
    ctx.move_to(0, -400); ctx.line_to(0, 0); setc(ctx, hx('a8642e')); ctx.set_line_width(14); ctx.stroke()
    for k in range(-5, 6):
        ctx.move_to(k * 8, 0); ctx.curve_to(k * 14, 40, k * 18, 70, k * 20, 110); setc(ctx, INK); ctx.set_line_width(20); ctx.stroke()
        ctx.move_to(k * 8, 0); ctx.curve_to(k * 14, 40, k * 18, 70, k * 20, 110); setc(ctx, hx('9ad8ff')); ctx.set_line_width(11); ctx.stroke()
    ctx.restore()


def fork(ctx, x, y, s=1.0, a=0.0, bite=False):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    for k in (-16, -5, 6, 17):
        ctx.move_to(k, -60); ctx.line_to(k, -20); setc(ctx, INK); ctx.set_line_width(11); ctx.stroke()
        ctx.move_to(k, -60); ctx.line_to(k, -20); setc(ctx, hx('dfe3ee')); ctx.set_line_width(5); ctx.stroke()
    ctx.move_to(0, -24); ctx.line_to(0, 110); setc(ctx, INK); ctx.set_line_width(20); ctx.stroke()
    ctx.move_to(0, -24); ctx.line_to(0, 110); setc(ctx, hx('dfe3ee')); ctx.set_line_width(11); ctx.stroke()
    if bite:
        poly(ctx, [(-34, -66), (34, -66), (30, -120), (-30, -130)]); fl(ctx, hx('ffcf7a'), 5)
        poly(ctx, [(-30, -130), (30, -120), (30, -108), (-32, -116)]); fl(ctx, hx('ff8ac0'), 4)
    ctx.restore()


def flour_spots(ctx, cx, cy, R, seed=7):
    rnd = random.Random(seed)
    for k in range(5):
        ellipse(ctx, cx + rnd.uniform(-0.6, 0.7) * R, cy + rnd.uniform(0.0, 0.6) * R, rnd.uniform(0.07, 0.14) * R, rnd.uniform(0.05, 0.1) * R)
        setc(ctx, (1, 1, 1, 0.92)); ctx.fill()


def twitch(ctx, x, y, R, lf):
    """little eye-twitch strain marks"""
    if (lf // 3) % 2:
        for k in range(3):
            a = -0.9 + k * 0.45
            ctx.move_to(x + math.cos(a) * R * 0.32, y + math.sin(a) * R * 0.32); ctx.line_to(x + math.cos(a) * R * 0.5, y + math.sin(a) * R * 0.5)
            setc(ctx, RED); ctx.set_line_width(R * 0.04); ctx.stroke()


def stool(ctx, x, top, h):
    rect_r(ctx, x - 110, top, 220, 34, 10); fl(ctx, hx('ff8a1f'), 7)
    for dx in (-80, 60):
        ctx.rectangle(x + dx, top + 34, 22, h); fl(ctx, hx('c45a10'), 6)


def splats_wall(ctx, k, seed=11):
    rnd = random.Random(seed)
    for i in range(k):
        splat(ctx, rnd.uniform(20, 1060), rnd.uniform(380, 1100), rnd.uniform(26, 60), seed + i)


# ------------------------------------------------------------------ opening face
def opening_face(ctx, f, lf, lab=True):
    bob = 16 * abs(math.sin(lf * 0.35))
    ctx.save(); cam(ctx, 540, 960, 1.02 + 0.04 * eout(pop(lf, 0, 40)), 1.5 * math.sin(lf * 0.4), 6, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd23f')); ctx.fill()
    rays(ctx, 540, 900, 260, 1700, lf * 0.06, col=(1, 1, 1), a=0.5, n=18)
    cx, cy, R = 540, 1070 - bob, 250
    rot = 0.08 * math.sin(lf * 0.5)
    # whisk raised in a fist
    wx, wy = 170, 1260 - bob
    ctx.save(); ctx.translate(wx, wy); ctx.rotate(-0.35)
    ctx.move_to(0, 0); ctx.line_to(0, -330); setc(ctx, INK); ctx.set_line_width(30); ctx.stroke(); ctx.move_to(0, 0); ctx.line_to(0, -330); setc(ctx, hx('ff5fa8')); ctx.set_line_width(18); ctx.stroke()
    for k in (-1, -0.5, 0, 0.5, 1):
        ctx.move_to(0, -300); ctx.curve_to(k * 110, -380, k * 90, -560, 0, -560); setc(ctx, INK); ctx.set_line_width(12); ctx.stroke()
        ctx.move_to(0, -300); ctx.curve_to(k * 110, -380, k * 90, -560, 0, -560); setc(ctx, hx('dfe3ee')); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()
    ellipse(ctx, wx, wy, 80, 70); fl(ctx, BOY['skin'], 7)
    face(ctx, BOY, P(eye='shock', mouth='grin', head=0), cx, cy, R, rot)
    chef_hat(ctx, cx, cy, R, rot)
    flour_spots(ctx, cx, cy, R)
    for ex, ey, rx in eye_pos(cx, cy, R):
        sparkle(ctx, ex + rx * 0.25, ey - rx * 0.35, rx * 0.35, (1, 1, 1))
    for k in range(5):
        sparkle(ctx, 120 + k * 210, 560 + 70 * ((k * 3) % 2) + 10 * math.sin(lf * 0.4 + k), 26 + 8 * math.sin(lf * 0.5 + k))
    ctx.restore()
    if lab:
        label2(ctx, "\"MOM! MOM!", "CAN I HELP?!\"", (1, 1, 1), 1.0, 112, col2=PINK)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 48:
        opening_face(ctx, f, f)
    else:
        lf = f - 48
        # Mom ECU: frozen polite smile, eye twitch, sweat
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.1 * eout(pop(lf, 0, 42)), 0, shake_at(lf, [0], 8, 12), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('8fdcff')); ctx.fill()
        rays(ctx, 540, 900, 260, 1700, lf * 0.03, col=(1, 1, 1), a=0.35, n=14)
        cx, cy, R = 540, 940, 290
        face(ctx, MOM, P(eye='normal', mouth='grin', head=0), cx, cy, R, 0)
        ex, ey, rx = eye_pos(cx, cy, R)[1]
        twitch(ctx, ex, ey, R, lf)
        y_ = cy - 0.6 * R + ((lf * 3) % 120)
        ctx.move_to(cx - 0.95 * R, y_ - 40); ctx.curve_to(cx - 0.95 * R + 26, y_, cx - 0.95 * R + 20, y_ + 26, cx - 0.95 * R, y_ + 26)
        ctx.curve_to(cx - 0.95 * R - 20, y_ + 26, cx - 0.95 * R - 26, y_, cx - 0.95 * R, y_ - 40); fl(ctx, hx('5ac8ff'), 5)
        ctx.restore()
        label2(ctx, "\"...sure,", "sweetie.\"", (1, 1, 1), pop(lf, 2, 6), 110, col2=YEL)
    card(ctx, 'p1', f, -6, 86)


def s2(ctx, f):
    lf = f - 90
    if lf < 48:
        # top-down bowl, giant fist with an egg SLAMS in
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.08 * eout(pop(lf, 18, 26)), 0, shake_at(lf, [18], 12, 30), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb3d9')); ctx.fill()
        for i in range(-4, 12):
            ctx.rectangle(i * 160, -500, 80, 3000); setc(ctx, hx('ffc8e4')); ctx.fill()
        ellipse(ctx, 540, 1000, 400, 400); fl(ctx, hx('5ab8ff'), 9)
        ellipse(ctx, 540, 1000, 340, 340); setc(ctx, hx('9ad8ff')); ctx.fill()
        ellipse(ctx, 540, 1000, 250, 250); setc(ctx, BATTER); ctx.fill_preserve(); ink(ctx, 5); ctx.stroke()
        if lf < 18:
            u = ein(pop(lf, 0, 18))
            ex_, ey_ = 540, 1900 - 900 * u
            s = 2.2 - 0.9 * u
            egg(ctx, ex_, ey_ - 90 * s, s, 0.2)
            ellipse(ctx, ex_, ey_, 150 * s / 1.6, 120 * s / 1.6); fl(ctx, BOY['skin'], 8)
            ctx.rectangle(ex_ - 90 * s / 1.6, ey_, 180 * s / 1.6, 900); fl(ctx, BOY['shirt'], 8)
        else:
            splat(ctx, 540, 1000, 120, 5, YOLK)
            ellipse(ctx, 540, 1000, 60, 50); setc(ctx, hx('ff9a00')); ctx.fill()
            shell_bits(ctx, 540, 1000, pop(lf, 18, 40), 22, 520)
            ellipse(ctx, 540, 1060, 130, 100); fl(ctx, BOY['skin'], 8)
            ctx.rectangle(450, 1060, 180, 900); fl(ctx, BOY['shirt'], 8)
            ellipse(ctx, 540, 1060, 130, 100); fl(ctx, BOY['skin'], 8)
            for k in range(4):
                ellipse(ctx, 470 + k * 46, 990, 26, 30); fl(ctx, BOY['skin'], 5)
        ctx.restore()
        if lf < 18:
            label1(ctx, "\"I GOT THIS!\"", (1, 1, 1), pop(lf, 1, 4), 110, y=560)
        else:
            label1(ctx, "*CRUNCH!!*", YEL, pop(lf, 18, 21), 150, 0.05, y=560)
        card(ctx, 'p2', f, 92, 132)
    else:
        il = lf - 48
        # medium shot: proud kid on stool / Mom with magnifying glass counting shells
        ctx.save(); cam(ctx, 540, 1060, 1.06 + 0.06 * eout(pop(il, 0, 72)), 0, 0, f)
        kitchen(ctx)
        stool(ctx, 270, 1290, 140)
        draw(ctx, 270, 1290 - 186 * 1.0, 1.0, 1, BOY, P(lsh=-150, lel=-20, rsh=-30, rel=-60, eye='happy', mouth='grin', lhip=-6, lkn=0, rhip=6, rkn=0))
        bm = draw(ctx, 820, FLOOR - 186 * 1.3, 1.3, -1, MOM, P(torso=6, head=12, lsh=40, lel=-20, rsh=130, rel=-30, eye='glare', mouth='flat'))
        table(ctx, 330, 1000, TOP)
        bowl(ctx, 560, TOP - 120, 1.0, BATTER, 12)
        hx_, hy_ = bm['front']
        ctx.move_to(hx_, hy_); ctx.line_to(hx_ - 70, hy_ - 60); setc(ctx, INK); ctx.set_line_width(22); ctx.stroke()
        ctx.move_to(hx_, hy_); ctx.line_to(hx_ - 70, hy_ - 60); setc(ctx, hx('a8642e')); ctx.set_line_width(12); ctx.stroke()
        ellipse(ctx, hx_ - 70, hy_ + 20, 40, 34); fl(ctx, MOM['skin'], 7)
        ellipse(ctx, hx_ - 120, hy_ - 110, 66, 66); setc(ctx, (0.85, 0.95, 1, 0.6)); ctx.fill_preserve(); ink(ctx, 12); ctx.stroke()
        ellipse(ctx, hx_ - 120, hy_ - 110, 66, 66); setc(ctx, hx('ffd23f')); ctx.set_line_width(6); ctx.stroke()
        ctx.restore()
        if il < 50:
            label2(ctx, "\"I added", "EXTRA EGG!\"", (1, 1, 1), pop(il, 1, 5), 104, col2=YEL, y=560)
        else:
            label2(ctx, "\"...and", "EXTRA SHELL.\"", (1, 1, 1), pop(il, 50, 54), 104, col2=ORANGE, y=560)


def dial(ctx, cx, cy, pos):
    """speed slider: pos 0=LOW 1=MED 2=MAX (float)"""
    rect_r(ctx, cx - 380, cy - 200, 760, 400, 60); fl(ctx, hx('ff8a1f'), 10)
    rect_r(ctx, cx - 300, cy - 30, 600, 60, 30); fl(ctx, hx('3a2a20'), 6)
    for k, (t, col) in enumerate((("LOW", GREEN), ("MED", YEL), ("MAX", RED))):
        text(ctx, t, cx - 240 + k * 240, cy - 110, 64, col, ow=10)
        ctx.move_to(cx - 240 + k * 240, cy + 40); ctx.line_to(cx - 240 + k * 240, cy + 70); ink(ctx, 8); ctx.stroke()
    kx = cx - 240 + pos * 240
    rect_r(ctx, kx - 50, cy - 60, 100, 120, 24); fl(ctx, (1, 1, 1), 8)


def s3(ctx, f):
    lf = f - 210
    if lf < 40:
        # ECU speed slider, kid's finger shoves it to MAX
        sh = shake_at(lf, [26], 10, 26)
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.12 * eout(pop(lf, 20, 30)), 0, sh, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('2a2a4a')); ctx.fill()
        rays(ctx, 540, 960, 200, 1600, lf * 0.05, col=(1, 0.3, 0.3), a=0.3 * pop(lf, 22, 26), n=16)
        pos = 0 if lf < 10 else (eout(pop(lf, 10, 16)) if lf < 20 else 1 + eout(pop(lf, 20, 26)))
        dial(ctx, 540, 1000, pos)
        kx = 540 - 240 + pos * 240
        ctx.move_to(kx - 300, 1500); ctx.line_to(kx - 30, 1060); setc(ctx, INK); ctx.set_line_width(110); ctx.stroke()
        ctx.move_to(kx - 300, 1500); ctx.line_to(kx - 30, 1060); setc(ctx, BOY['skin']); ctx.set_line_width(92); ctx.stroke()
        ellipse(ctx, kx - 20, 1050, 42, 50); fl(ctx, BOY['skin'], 7)
        ctx.restore()
        if lf < 10:
            label1(ctx, "\"LOW speed, okay?\"", (1, 1, 1), pop(lf, 1, 4), 96, y=600)
        elif lf < 26:
            label1(ctx, "*click*", YEL, pop(lf, 10, 13), 110, y=600)
        else:
            label1(ctx, "*CLICK!*", RED, pop(lf, 26, 29), 140, 0.05, y=600)
        card(ctx, 'p3', f, 212, 236)
    elif lf < 95:
        il = lf - 40
        # wide: batter tornado, splats fill the walls
        ctx.save(); cam(ctx, 540, 1040, 1.0, 2 * math.sin(il * 1.7), 9, f)
        kitchen(ctx)
        splats_wall(ctx, min(18, int(il * 0.5)))
        table(ctx, 200, 900, TOP)
        bowl(ctx, 520, TOP - 120, 1.0, BATTER)
        rnd = random.Random(il)
        for k in range(10):   # flying batter blobs
            a = rnd.uniform(-math.pi, 0); d = rnd.uniform(150, 700)
            splat(ctx, 520 + math.cos(a + il * 0.4) * d, TOP - 200 + math.sin(a) * d * 0.9, rnd.uniform(16, 34), k + il)
        for k in range(3):
            ctx.new_path(); ctx.arc(520, TOP - 200, 200 + k * 60, -math.pi + il * 0.5 + k, -math.pi + il * 0.5 + k + 1.2)
            setc(ctx, BATTER); ctx.set_line_width(22); ctx.stroke()
        stool(ctx, 300, 1290, 140)
        jit = 8 * math.sin(il * 3)
        bk = draw(ctx, 300 + jit, 1290 - 186 * 1.0, 1.0, 1, BOY, P(lsh=-110, lel=-20, rsh=-100, rel=-10, eye='shock', mouth='scream', lhip=-6, lkn=0, rhip=6, rkn=0, torso=-6))
        mixer(ctx, 520 + jit, TOP - 330, 0.8, 0.05 * math.sin(il * 4), il * 2.0)
        draw(ctx, 800, FLOOR - 186 * 1.2 + 40, 1.2, -1, MOM, P(torso=-30, head=-10, lsh=-160, lel=-60, rsh=-150, rel=-70, eye='shock', mouth='scream', lhip=20, lkn=-40, rhip=-10, rkn=-40))
        splat(ctx, 860, 640, 50, 31)
        ctx.restore()
        label1(ctx, "*BRRRRRRRR!!*", YEL, pop(il, 1, 4), 120, 0.03 * math.sin(il), y=560)
    else:
        il = lf - 95
        # low angle from the counter: ceiling drip lands on Mom's head
        ctx.save(); cam(ctx, 540, 960, 1.0, 0, shake_at(il, [20], 10, 22), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('7fd6ff')); ctx.fill()
        ctx.rectangle(-500, -500, 2200, 820); setc(ctx, hx('fff4dc')); ctx.fill()
        ctx.move_to(-500, 320); ctx.line_to(1700, 320); ink(ctx, 8); ctx.stroke()
        for x in (180, 520, 860):
            splat(ctx, x, 300, 60, x)
        # the drip stretches then falls
        stretch = eout(pop(il, 0, 14))
        fall = ein(pop(il, 12, 20))
        dy = 330 + 120 * stretch + 520 * fall
        ctx.move_to(500, 300); ctx.curve_to(520, dy - 60, 560, dy - 60, 580, 300); setc(ctx, BATTER); ctx.fill()
        if il < 20:
            ellipse(ctx, 540, dy, 54, 66); fl(ctx, BATTER, 6)
        cx, cy, R = 540, 1200, 300
        face(ctx, MOM, P(eye='shock' if il < 20 else 'closed', mouth='open' if il < 20 else 'flat', head=0), cx, cy, R, 0)
        if il >= 20:
            u = eout(pop(il, 20, 26))
            ctx.move_to(cx - 0.9 * R, cy - 0.85 * R)
            ctx.curve_to(cx - 0.6 * R, cy - 1.5 * R * u, cx + 0.6 * R, cy - 1.5 * R * u, cx + 0.9 * R, cy - 0.85 * R)
            for k in range(6):
                ctx.line_to(cx + 0.9 * R - k * 0.36 * R, cy - 0.7 * R + (0.25 * R if k % 2 else 0) * u)
            ctx.close_path(); fl(ctx, BATTER, 7)
        ctx.restore()
        if il < 20:
            label1(ctx, "*drip...*", (1, 1, 1), pop(il, 2, 5), 100, y=600)
        else:
            label1(ctx, "*PLOP!*", YEL, pop(il, 20, 23), 150, -0.05, y=600)


def s4(ctx, f):
    lf = f - 340
    if lf < 30:
        # kid rips open a giant flour bag
        ctx.save(); cam(ctx, 540, 1060, 1.05 + 0.15 * eout(pop(lf, 0, 30)), 0, shake_at(lf, [22], 10, 26), f)
        kitchen(ctx)
        splats_wall(ctx, 18)
        table(ctx, 200, 900, TOP)
        stool(ctx, 360, 1290, 140)
        draw(ctx, 360, 1290 - 186 * 1.0, 1.0, 1, BOY, P(lsh=-150 + 30 * pop(lf, 10, 22), lel=-10, rsh=-120, rel=-10, eye='glare', mouth='grin', lhip=-6, lkn=0, rhip=6, rkn=0))
        flour_bag(ctx, 640, TOP - 330, 1.0, 0.1 * math.sin(lf * 0.8), pop(lf, 14, 22))
        ctx.restore()
        if lf < 22:
            label1(ctx, "\"How MUCH flour?\"", (1, 1, 1), pop(lf, 1, 4), 100, y=600)
        else:
            flour_cloud(ctx, 640, 900, 500 * eout(pop(lf, 22, 30)), 5, 1.0, lf)
            label1(ctx, "*POOF!!*", (1, 1, 1), pop(lf, 22, 25), 160, y=600)
        card(ctx, 'p4', f, 342, 366)
    elif lf < 52:
        il = lf - 30
        # white-out
        ctx.rectangle(0, 0, W, H); setc(ctx, (0.97, 0.96, 0.94)); ctx.fill()
        flour_cloud(ctx, 540, 960, 900, 9, 1.0, il)
        for k in range(2):  # two pairs of blinking eyes in the cloud
            x0 = 360 if k == 0 else 720
            op = (il // 6 + k) % 4 != 0
            for dx in (-44, 44):
                if op:
                    ellipse(ctx, x0 + dx, 960, 30, 36); fl(ctx, (1, 1, 1), 6); ellipse(ctx, x0 + dx, 966, 12, 14); setc(ctx, INK); ctx.fill()
                else:
                    ctx.move_to(x0 + dx - 30, 960); ctx.line_to(x0 + dx + 30, 960); ink(ctx, 8); ctx.stroke()
        label1(ctx, "*cough*", (0.5, 0.5, 0.55), pop(il, 6, 9), 100, y=600)
    else:
        il = lf - 52
        # split: ghost-white kid beaming (top) / ghost-white Mom twitching (bottom)
        ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
        ctx.rectangle(0, 0, W, 960); setc(ctx, hx('ffb3d9')); ctx.fill()
        rays(ctx, 540, 640, 120, 1200, il * 0.06, col=(1, 1, 1), a=0.5, n=16)
        cx, cy, R = 540, 640 + 10 * abs(math.sin(il * 0.4)), 220
        face(ctx, WBOY, P(eye='happy', mouth='grin', head=0), cx, cy, R, 0.05 * math.sin(il * 0.4))
        chef_hat(ctx, cx, cy, R, 0.05 * math.sin(il * 0.4))
        for k in range(3):
            ellipse(ctx, cx - 300 + k * 300 + 20 * math.sin(il * 0.2 + k), 400 - ((il * 2 + k * 30) % 80), 24, 20); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()
        ctx.restore()
        ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
        ctx.rectangle(0, 960, W, 960); setc(ctx, hx('8a9ab0')); ctx.fill()
        cx, cy, R = 540, 1260, 240
        face(ctx, WMOM, P(eye='normal', mouth='flat', head=0), cx, cy, R, 0)
        ex, ey, rx = eye_pos(cx, cy, R)[1]
        twitch(ctx, ex, ey, R, il)
        ellipse(ctx, cx + 0.95 * R, cy + 0.3 * R + ((il * 2) % 60), 14, 18); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()
        ctx.restore()
        ctx.rectangle(0, 952, W, 16); setc(ctx, (1, 1, 1)); ctx.fill()
        label(ctx, "\"WE'RE A GREAT TEAM!\"", 540, 880, 80, (1, 1, 1), -0.03, pop(il, 2, 6))
        label1(ctx, "\"...so great.\"", (1, 1, 1), pop(il, 30, 34), 100, y=1440)


def s5(ctx, f):
    lf = f - 460
    if lf < 60:
        # wide disaster kitchen, floury Mom holds out the mop
        ctx.save(); cam(ctx, 540, 1040, 1.0 + 0.05 * eout(pop(lf, 0, 60)), 0, 0, f)
        kitchen(ctx)
        splats_wall(ctx, 18)
        for k in range(6):
            ellipse(ctx, 80 + k * 190, FLOOR + 30, 90, 26); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()
        table(ctx, 140, 640, TOP)
        cake(ctx, 380, TOP, 0.9)
        draw(ctx, 260, FLOOR - 186 * 1.0, 1.0, 1, WBOY, P(eye='happy', mouth='grin', lsh=-20, rsh=20))
        chef = draw(_DUMMY, 260, FLOOR - 186 * 1.0, 1.0, 1, WBOY, P(eye='happy', mouth='grin', lsh=-20, rsh=20))
        chef_hat(ctx, chef['head'][0], chef['head'][1], chef['R'], 0)
        bm = draw(ctx, 820, FLOOR - 186 * 1.3, 1.3, -1, WMOM, P(lsh=-70, lel=-10, rsh=10, eye='smug', mouth='smile'))
        mop(ctx, bm['front'][0], bm['front'][1] + 200, 1.0, -0.3)
        ctx.restore()
        label2(ctx, "\"Can you help me", "CLEAN UP?\"", (1, 1, 1), pop(lf, 2, 6), 100, col2=GREEN, y=720)
        card(ctx, 'p5', f, 462, 500)
    elif lf < 100:
        il = lf - 60
        # *ZOOM*: kid vanishes, kid-shaped flour puff left behind
        ctx.save(); cam(ctx, 540, 1040, 1.05, 0, shake_at(il, [3], 10, 22), f)
        kitchen(ctx)
        splats_wall(ctx, 18)
        table(ctx, 140, 640, TOP)
        cake(ctx, 380, TOP, 0.9)
        if il < 3:
            draw(ctx, 260, FLOOR - 186 * 1.0, 1.0, 1, WBOY, P(eye='shock', mouth='open', lsh=-20, rsh=20))
        else:
            a = 1 - pop(il, 18, 40)
            ctx.save(); ctx.push_group()
            draw(ctx, 260, FLOOR - 186 * 1.0, 1.0, 1, WBOY, P(eye='closed', mouth='flat', lsh=-20, rsh=20))
            ctx.pop_group_to_source(); ctx.paint_with_alpha(0.55 * a); ctx.restore()
            for k in range(8):
                y = 900 + k * 70
                ctx.move_to(-200 + 30 * k % 90, y); ctx.line_to(180, y); setc(ctx, (1, 1, 1, 0.8 * a)); ctx.set_line_width(14); ctx.stroke()
        bm = draw(ctx, 820, FLOOR - 186 * 1.3, 1.3, -1, WMOM, P(lsh=-70, lel=-10, rsh=10, eye='shock' if il < 30 else 'glare', mouth='open' if il < 30 else 'flat'))
        mop(ctx, bm['front'][0], bm['front'][1] + 200, 1.0, -0.3 + 0.8 * ein(pop(il, 12, 24)))
        ctx.restore()
        if il < 30:
            label1(ctx, "*ZOOM!*", YEL, pop(il, 3, 6), 150, -0.05, y=600)
        else:
            label1(ctx, "\"...of course.\"", (1, 1, 1), pop(il, 30, 34), 104, y=600)
    elif lf < 158:
        il = lf - 100
        # Mom alone at last with a slice of cake... a little head rises behind the counter
        ctx.save(); cam(ctx, 540, 980, 1.05 + 0.08 * eout(pop(il, 0, 58)), 0, shake_at(il, [34], 8, 16), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffcf9a')); ctx.fill()
        rays(ctx, 540, 900, 200, 1600, il * 0.02, col=(1, 1, 1), a=0.25, n=14)
        cx, cy, R = 460, 820, 270
        face(ctx, WMOM, P(eye='closed' if il < 34 else 'shock', mouth='smile' if il < 34 else 'open', head=0), cx, cy, R, -0.05)
        lift = eout(pop(il, 4, 30))
        fork(ctx, 230, 1240 - 260 * lift, 1.4, 0.3, True)
        ellipse(ctx, 230, 1290 - 260 * lift, 70, 60); fl(ctx, WMOM['skin'], 7)
        # counter edge in the foreground
        rect_r(ctx, -100, 1300, 1300, 90, 16); fl(ctx, hx('c46a2e'), 9)
        ctx.rectangle(-100, 1390, 1300, 800); setc(ctx, hx('9a4e1e')); ctx.fill()
        rise = eout(pop(il, 30, 38))
        if rise > 0:
            ctx.save(); ctx.rectangle(-500, -500, 2200, 1800); ctx.clip()
            kx, ky, kR = 780, 1460 - 210 * rise, 170
            face(ctx, WBOY, P(eye='shock', mouth='flat', head=0), kx, ky, kR, 0.05)
            chef_hat(ctx, kx, ky, kR, 0.05)
            ctx.restore()
            fork(ctx, 920, 1300 - 120 * rise, 1.1, -0.2)
            ellipse(ctx, 920, 1310 - 120 * rise, 46, 40); fl(ctx, WBOY['skin'], 6)
        ctx.restore()
        if il < 30:
            label1(ctx, "\"Ahh... finally. Quiet.\"", (1, 1, 1), pop(il, 3, 7), 90, y=480)
        else:
            label1(ctx, "\"Can I help...\"", PINK, pop(il, 34, 38), 104, y=480)
    elif lf < 192:
        il = lf - 158
        # kid ECU, fork raised: "...EAT IT?!"
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.08 * eout(pop(il, 0, 20)), 0, shake_at(il, [0], 8, 16), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8ac0')); ctx.fill()
        rays(ctx, 540, 900, 260, 1700, il * 0.08, col=(1, 1, 1), a=0.5, n=18)
        cx, cy, R = 540, 960, 290
        face(ctx, WBOY, P(eye='shock', mouth='grin', head=0), cx, cy, R, 0.04)
        chef_hat(ctx, cx, cy, R, 0.04)
        for ex, ey, rx in eye_pos(cx, cy, R):
            sparkle(ctx, ex + rx * 0.25, ey - rx * 0.35, rx * 0.4, (1, 1, 1))
        fork(ctx, 180, 1250, 2.0, -0.3)
        ellipse(ctx, 200, 1300, 80, 70); fl(ctx, WBOY['skin'], 7)
        ctx.restore()
        label1(ctx, "\"...EAT IT?!\"", YEL, pop(il, 0, 4), 140)
    else:
        il = lf - 192
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 652)


SHOTS = [(0, s1), (90, s2), (210, s3), (340, s4), (460, s5)]
CUTS = (48, 90, 138, 210, 250, 305, 340, 370, 392, 460, 520, 560, 618, 652)


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
                              "-i", "out/help_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
