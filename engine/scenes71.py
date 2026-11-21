"""'The Leaf Pile' - Dad vs the leaf pile. Original, general-audience comedy short, 22s.
Hook: Dad ECU mid-scream, leaves flying past the lens, caption 'Dad vs the LEAF PILE:' "NOT... THE... PILE!!".
Beat 1: super-speed raking -> perfect pile + flag "PERFECT." -> kid ECU sparkle eyes behind a bush "...ooh." ->
        side run + "CANNONBALL!!" (Dad "NO NO NO!") -> KA-FLOOMP, kid in the flattened leaves "BEST. DAY. EVER!!"
Beat 2: ATTEMPT #2 low angle: Dad guards the pile + KEEP OUT sign "NOBODY. TOUCHES. IT." -> *WHOOOSH* wind blows the whole
        pile over the fence -> split: neighbour kid in a giant pile "THANKS, MISTER!!" / Dad twitch "...my... PILE."
Twist:  6 HOURS LATER "ONE. LAST. PILE." -> eyes dart "...nobody's watching?" -> Dad flies in "WHEEEEE!!" ->
        Dad in the leaves "...okay. I GET it now." -> Mom + kid "DAD?!" -> family leaf fight -> the tree dumps ALL its
        leaves *FWUMP* -> three pairs of eyes "...worth it."
End:    NEXT MORNING "PERFECT." -> the dog's sparkle eyes, wiggle -> "...don't you DARE." -> dog leaps -> loop to the hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw, draw_hip
from eng3 import run_pose
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes65 import dog
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


DAD = dict(doodle.DAD, shirt=hx('2f8fff'), pants=hx('8a5a3a'))
BOY = dict(doodle.BOY, hood=False, shades=False, shirt=hx('22b45a'), pants=hx('2a3a6a'))
NBOY = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff3b5c'), pants=hx('3d5aff'), hair=hx('b8482e'), skin=hx('f6d2b0'))
MOM = dict(doodle.MOM_G, shirt=hx('9b4dff'), pants=hx('3d5a9e'))
N = 660
RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
LEAFC = [hx('ff8a1f'), hx('e8442e'), hx('ffc93c'), hx('c9662a'), hx('f5a623')]
FLOOR = 1500
KK, DK, MK = 0.95, 1.4, 1.35
PX = 600   # pile centre

CAPS = {
    'p1': [[("Dad vs the ", OUT), ("LEAF PILE:", ORANGE)]],
}
scenes13.CAPS = CAPS
card = _card13
SIT = dict(lhip=-80, lkn=80, rhip=-80, rkn=80)


# ------------------------------------------------------------------ props
def leaf(ctx, x, y, s, a, col):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(0, -30)
    ctx.curve_to(14, -26, 26, -6, 20, 6); ctx.curve_to(26, 14, 10, 26, 0, 32)
    ctx.curve_to(-10, 26, -26, 14, -20, 6); ctx.curve_to(-26, -6, -14, -26, 0, -30); ctx.close_path()
    setc(ctx, col); ctx.fill_preserve(); ink(ctx, 3.2); ctx.stroke()
    ctx.move_to(0, -22); ctx.line_to(0, 40); setc(ctx, dark(col, 0.7)); ctx.set_line_width(2.6); ctx.stroke()
    ctx.restore()


def pile(ctx, x, ground, w, h, seed=1, flag=False, sign=False):
    if h < 3:
        return
    ctx.new_path(); ctx.move_to(x - w / 2, ground + 6)
    ctx.curve_to(x - w * 0.42, ground - h * 1.25, x + w * 0.42, ground - h * 1.25, x + w / 2, ground + 6); ctx.close_path()
    fl(ctx, hx('d9661f'), 8)
    rnd = random.Random(seed)
    n = int(min(170, 18 + w * h / 1800))
    for k in range(n):
        u = rnd.uniform(-0.5, 0.5); v = rnd.uniform(0, 1) ** 0.7
        hm = h * (1 - (2 * u) ** 2) * 0.95
        leaf(ctx, x + u * w * 0.94, ground - v * hm + 6, rnd.uniform(1.1, 1.7) * min(1, 0.5 + h / 300), rnd.uniform(0, 6.3),
             LEAFC[rnd.randrange(5)])
    top = ground - h * 0.94
    if flag:
        ctx.move_to(x, top); ctx.line_to(x, top - 150); ink(ctx, 7); ctx.stroke()
        poly(ctx, [(x, top - 150), (x + 90, top - 125), (x, top - 100)]); fl(ctx, RED, 5)
    if sign:
        ctx.move_to(x - 20, top + 10); ctx.line_to(x - 20, top - 140); ink(ctx, 10); ctx.stroke()
        ctx.save(); ctx.translate(x - 20, top - 160); ctx.rotate(-0.06)
        rect_r(ctx, -130, -55, 260, 110, 14); fl(ctx, hx('fff27a'), 6)
        text(ctx, "KEEP OUT", 0, 14, 50, RED, ow=0, shadow=False)
        ctx.restore()


def scatter(ctx, x0, x1, y0, y1, n, seed, keep=1.0):
    rnd = random.Random(seed)
    for k in range(n):
        x, y, a, c = rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(0, 6.3), LEAFC[rnd.randrange(5)]
        if rnd.random() < keep:
            leaf(ctx, x, y, 1.2, a, c)


def burst(ctx, cx, cy, t, n=80, seed=3, sp=1.0, big=False):
    """leaves exploding out of a pile; t in seconds since impact"""
    if t < 0:
        return
    rnd = random.Random(seed)
    for k in range(n):
        ang = rnd.uniform(-math.pi * 0.95, -math.pi * 0.05)
        v = rnd.uniform(500, 1900) * sp
        d = v * (1 - math.exp(-3.2 * t)) / 3.2
        x = cx + math.cos(ang) * d + 40 * math.sin(t * 4 + k)
        y = cy + math.sin(ang) * d + 900 * t * t + 150 * t
        s = rnd.uniform(1.2, 2.4) * (1 + (rnd.random() < 0.12 and big) * 1.4)
        leaf(ctx, x, y, s, rnd.uniform(0, 6.3) + t * rnd.uniform(-8, 8), LEAFC[k % 5])


def falling(ctx, lf, x0, x1, y0, y1, n=24, seed=1, s=1.3):
    rnd = random.Random(seed)
    for k in range(n):
        x = rnd.uniform(x0, x1) + 40 * math.sin(lf * 0.12 + k)
        y = y0 + ((rnd.uniform(0, 1) * (y1 - y0) + lf * rnd.uniform(3, 7)) % (y1 - y0))
        leaf(ctx, x, y, s * rnd.uniform(0.8, 1.2), math.sin(lf * 0.15 + k) * 1.2 + k, LEAFC[k % 5])


def rake(ctx, x, y, a, s=1.0):
    """(x, y) = grip; head points along angle a"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(-120, 0); ctx.line_to(300, 0); ink(ctx, 22); ctx.stroke()
    ctx.move_to(-120, 0); ctx.line_to(300, 0); setc(ctx, hx('c98a4a')); ctx.set_line_width(12); ctx.stroke()
    poly(ctx, [(290, -20), (300, -90), (330, -90), (330, 90), (300, 90), (290, 20)]); fl(ctx, hx('3aa55a'), 6)
    for k in range(7):
        yy = -80 + k * 26.6
        ctx.move_to(330, yy); ctx.line_to(380, yy + 8)
    ink(ctx, 7); ctx.stroke()
    ctx.restore()


def tree(ctx, x, ground, full=1.0, shake=0.0, lf=0):
    ctx.save(); ctx.translate(x, ground); ctx.rotate(shake * math.sin(lf * 2.3)); ctx.translate(-x, -ground)
    poly(ctx, [(x - 55, ground), (x + 55, ground), (x + 34, ground - 900), (x - 34, ground - 900)]); fl(ctx, hx('8a5a3a'), 8)
    for (bx, by, ex, ey) in ((x, ground - 650, x + 230, ground - 930), (x, ground - 760, x - 200, ground - 1010), (x, ground - 880, x + 60, ground - 1120)):
        ctx.move_to(bx, by); ctx.line_to(ex, ey); setc(ctx, INK); ctx.set_line_width(36); ctx.stroke()
        ctx.move_to(bx, by); ctx.line_to(ex, ey); setc(ctx, hx('8a5a3a')); ctx.set_line_width(22); ctx.stroke()
    if full > 0.02:
        for k, (dx, dy, r, c) in enumerate(((-200, -980, 210, 0), (190, -960, 220, 4), (0, -1130, 250, 2), (-60, -880, 200, 1), (150, -1150, 170, 0))):
            ellipse(ctx, x + dx, ground + dy, r * full, r * 0.85 * full); fl(ctx, LEAFC[c], 8)
        for dx, dy in ((-120, -1060), (100, -1010), (10, -920), (200, -1100)):
            leaf(ctx, x + dx, ground + dy, 1.8 * full, dx * 0.01, LEAFC[(dx // 50) % 5])
    ctx.restore()


def yard(ctx, lf, sky=hx('8fd8ff'), grass=hx('8fcf5a'), fence=hx('fff1dc'), tree_full=1.0, tree_x=150, tree_shake=0.0, sun=True):
    ctx.rectangle(-2000, -2000, 5000, 5000); setc(ctx, sky); ctx.fill()
    if sun:
        ctx.new_path(); ctx.arc(900, 300, 110, 0, 2 * math.pi); setc(ctx, (1, 0.95, 0.6, 0.5)); ctx.fill()
        ctx.new_path(); ctx.arc(900, 300, 80, 0, 2 * math.pi); fl(ctx, hx('ffd23f'), 7)
    for k in range(-12, 22):
        x = k * 110
        poly(ctx, [(x, 1500), (x, 1080), (x + 45, 1040), (x + 90, 1080), (x + 90, 1500)]); fl(ctx, fence, 6)
    ctx.rectangle(-2000, 1150, 5000, 28); fl(ctx, dark(fence, 0.92), 5)
    ctx.rectangle(-2000, 1320, 5000, 28); fl(ctx, dark(fence, 0.92), 5)
    tree(ctx, tree_x, FLOOR - 30, tree_full, tree_shake, lf)
    ctx.rectangle(-2000, FLOOR - 40, 5000, 2000); setc(ctx, grass); ctx.fill()
    ctx.move_to(-2000, FLOOR - 40); ctx.line_to(3000, FLOOR - 40); ink(ctx, 7); ctx.stroke()
    for k in range(-10, 30):
        x = k * 90 + 30
        ctx.move_to(x, FLOOR + 60); ctx.line_to(x + 10, FLOOR + 30); ctx.move_to(x + 18, FLOOR + 60); ctx.line_to(x + 22, FLOOR + 26)
    setc(ctx, dark(grass, 0.8)); ctx.set_line_width(5); ctx.stroke()


def leaf_hat(ctx, b, seed=2):
    hx_, hy_ = b['head']; R = b['R']
    rnd = random.Random(seed)
    for k in range(5):
        leaf(ctx, hx_ + rnd.uniform(-0.7, 0.7) * R, hy_ - R * rnd.uniform(0.75, 1.0), 1.5, rnd.uniform(-1, 1), LEAFC[k])


def flyers(ctx, lf, front=False):
    """leaves rushing past the lens (radial, growing)"""
    rnd = random.Random(11 if front else 12)
    for k in range(26 if front else 34):
        ang = rnd.uniform(0, 2 * math.pi)
        ph = (rnd.uniform(0, 1) + lf * rnd.uniform(0.025, 0.045)) % 1.0
        d = 120 + 1300 * ph ** 1.6
        x, y = 540 + math.cos(ang) * d, 1000 + math.sin(ang) * d * 1.2
        if front and d < 520:
            continue
        leaf(ctx, x, y, (1.0 + 4.5 * ph) * (1.3 if front else 0.9), ang + lf * 0.2 * (1 if k % 2 else -1), LEAFC[k % 5])


# ------------------------------------------------------------------ hook
def dad_scream(ctx, f, lf, z0=1.0):
    ctx.save(); cam(ctx, 540, 960, z0, 0, 7 if lf < 12 else 3, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb347')); ctx.fill()
    rays(ctx, 540, 900, 260, 1420, lf * 0.03, col=(1, 1, 1), a=0.25, n=18)
    flyers(ctx, lf)
    face(ctx, DAD, P(eye='shock', mouth='open'), 540, 900, 300, 0.03 * math.sin(lf * 1.9))
    twitch(ctx, 540 + 0.6 * 300, 900 - 0.75 * 300, lf, 1.4)
    sweat(ctx, 540 - 0.95 * 300, 860, lf, 1.3)
    rake(ctx, 1000, 1560, -1.3, 1.5)
    flyers(ctx, lf, True)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    dad_scream(ctx, f, lf, 1.02 + 0.06 * eio(pop(lf, 0, 54)))
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"NOT... THE...", "PILE!!\"", WHITE, t, 124, col2=ORANGE, y=1400)


# ------------------------------------------------------------------ beat 1
def s2(ctx, f):
    lf = f - 54
    if lf < 46:
        p = eio(pop(lf, 2, 30))
        ctx.save(); cam(ctx, 560, 1180, 1.22, 0, shake_at(lf, [30], 8, 10), f)
        yard(ctx, lf)
        scatter(ctx, -100, 1200, FLOOR - 20, FLOOR + 260, 60, 4, keep=1 - p)
        pile(ctx, PX, FLOOR, 560, 330 * p, seed=7, flag=lf >= 30)
        if lf < 30:
            for g in (2, 1, 0):
                l2 = lf - g
                x = PX + 340 * math.sin(l2 * 1.1)
                ctx.push_group()
                b = draw(ctx, x, FLOOR - 186 * DK, DK, 1 if math.cos(l2 * 1.1) > 0 else -1, DAD,
                         P(eye='glare', mouth='grin', rsh=-60, rel=-30, lsh=30, torso=18))
                rake(ctx, b['front'][0], b['front'][1], 1.2 if (l2 // 2) % 2 else 0.9, 0.9)
                ctx.pop_group_to_source(); ctx.paint_with_alpha(1.0 if g == 0 else 0.3)
            for k in range(6):
                yy = 1100 + k * 70
                ctx.move_to(-100, yy); ctx.line_to(1200, yy + 20)
            setc(ctx, (1, 1, 1, 0.5)); ctx.set_line_width(6); ctx.stroke()
        else:
            b = draw(ctx, 250, FLOOR - 186 * DK, DK, 1, DAD, P(eye='smug', mouth='grin', rsh=-160, rel=-20, lsh=20))
            rake(ctx, b['front'][0], b['front'][1], -1.1, 0.9)
        ctx.restore()
        if lf < 30:
            label(ctx, "*SCRITCH! SCRITCH!*", 540, 330, 92, ORANGE, -0.04, pop(lf, 2, 5))
        else:
            label(ctx, "\"PERFECT.\"", 540, 1420, 130, YEL, -0.04, pop(lf, 30, 34))
    elif lf < 70:
        il = lf - 46
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.1 * eio(pop(il, 0, 24)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffe07a')); ctx.fill()
        rays(ctx, 540, 900, 260, 1420, il * 0.05, col=(1, 1, 1), a=0.35, n=18)
        cx, cy, R = 540, 950 - 120 * eout(pop(il, 0, 8)) + 120, 300
        face(ctx, BOY, P(eye='shock', mouth='smile'), cx, cy, R, -0.08)
        for ex, ey in ((cx - 0.2 * R, cy + 0.08 * R), (cx + 0.42 * R, cy + 0.08 * R)):
            sparkle(ctx, ex, ey, (0.16 + 0.03 * math.sin(il * 0.9)) * R, col=YEL)
        for k in range(9):
            ellipse(ctx, -60 + k * 150, 1330 + 40 * ((k * 7) % 3), 160, 150); fl(ctx, hx('3aa55a'), 8)
        for k in range(9):
            ellipse(ctx, -60 + k * 150 + 30, 1300 + 40 * ((k * 7) % 3), 50, 30); setc(ctx, hx('5fd86f')); ctx.fill()
        ctx.restore()
        sparkle(ctx, 220, 640, 50 + 10 * math.sin(il), YEL); sparkle(ctx, 870, 560, 40 + 10 * math.cos(il), YEL)
        label(ctx, "\"...ooh.\"", 540, 1440, 130, WHITE, -0.04, pop(il, 4, 8))
    elif lf < 106:
        il = lf - 70
        ctx.save(); cam(ctx, 560, 1180, 1.22, 0, 0, f)
        yard(ctx, il)
        pile(ctx, PX, FLOOR, 560, 330, seed=7, flag=True)
        bd = draw(ctx, 230, FLOOR - 186 * DK, DK, 1, DAD, P(eye='shock', mouth='open', rsh=-100, rel=-10, lsh=60))
        if il < 12:
            x = lerp(1250, 930, il / 12)
            draw(ctx, x, FLOOR - 186 * KK, KK, -1, BOY, run_pose(il * 0.9, eye='happy', mouth='grin'))
        else:
            t = clamp((il - 12) / 18)
            x = lerp(930, PX, t); y = lerp(FLOOR - 186 * KK, FLOOR - 186 * KK - 200, t) - 520 * math.sin(math.pi * t)
            draw(ctx, x, y, KK, -1, BOY, P(eye='happy', mouth='open', lsh=160, rsh=-160, lel=10, rel=-10, rot=-25 * t, **SIT))
        # speed lines
        if il < 12:
            for k in range(4):
                ctx.move_to(1000 + k * 30, 1300 + k * 40); ctx.line_to(1250, 1300 + k * 40)
            setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(8); ctx.stroke()
        ctx.restore()
        if il >= 10:
            label(ctx, "\"CANNONBALL!!\"", 540, 330, 120, GREEN, -0.05, pop(il, 10, 13))
        if il >= 16:
            label(ctx, "\"NO NO NO!\"", 540, 1440, 120, RED, 0.04, pop(il, 16, 19))
    else:
        il = lf - 106   # 0..56
        ctx.save(); cam(ctx, 560, 1180, 1.22 + 0.04 * eio(pop(il, 20, 56)), 0, shake_at(il, [0], 16, 26), f)
        yard(ctx, il)
        bd = draw(ctx, 230, FLOOR - 186 * DK, DK, 1, DAD, P(eye='shock', mouth='open', rsh=-30, rel=-10, lsh=10))
        rake(ctx, bd['front'][0], bd['front'][1], 1.45, 0.9)
        if il >= 8:
            up_ = eout(pop(il, 8, 16))
            bk = draw(ctx, PX + 30, FLOOR + 60 - 140 * up_ - 186 * KK, KK, -1, BOY, P(eye='happy', mouth='grin', lsh=150, rsh=-150, lel=20, rel=-20))
            leaf_hat(ctx, bk)
        pile(ctx, PX, FLOOR + 30, 980, 110, seed=8)
        burst(ctx, PX, FLOOR - 100, il / 30, 90, 3, big=True)
        if il < 4:
            ctx.rectangle(-500, -500, 2500, 3000); setc(ctx, (1, 1, 1, 0.6 * (1 - il / 4))); ctx.fill()
        if il >= 22:
            twitch(ctx, bd['head'][0] + bd['R'] * 0.6, bd['head'][1] - bd['R'] * 0.8, il, 1.0)
        ctx.restore()
        label(ctx, "*KA-FLOOMP!!*", 540, 330, 120, ORANGE, -0.05, pop(il, 0, 3))
        if il >= 22:
            label2(ctx, "\"BEST.", "DAY. EVER!!\"", WHITE, pop(il, 22, 26), 116, col2=GREEN, y=1400)


# ------------------------------------------------------------------ beat 2
def guard_scene(ctx, f, il, wind=0.0, z=1.12, rot=-3, shake=0):
    PX2 = 700
    ctx.save(); cam(ctx, 560, 1150, z, rot, shake, f)
    yard(ctx, il, sky=hx('9fd0ff'), tree_x=-80)
    hh = 380 * (1 - wind)
    pile(ctx, PX2 + 80 * wind, FLOOR, 600, hh, seed=9, sign=wind < 0.3)
    lean = 22 * min(1, wind * 4) if 0 < wind < 1.01 else 0
    b = draw(ctx, 320, FLOOR - 186 * 1.7, 1.7, 1, DAD, P(eye='glare' if wind == 0 else 'shock', mouth='flat' if wind == 0 else 'open',
                                                       rsh=-40, rel=-60, lsh=40, lel=60, torso=-lean))
    rake(ctx, b['front'][0], b['front'][1], -0.55, 1.1)
    if wind > 0:
        # leaves streaming over the fence
        rnd = random.Random(21)
        for k in range(70):
            ph = (rnd.uniform(0, 1) + il * 0.05) % 1.0
            if ph > wind * 1.4:
                continue
            x = PX2 - 200 + ph * 1400; y = FLOOR - 100 - ph * 900 + 60 * math.sin(ph * 12 + k) + rnd.uniform(-150, 150)
            leaf(ctx, x, y, 1.5, il * 0.3 + k, LEAFC[k % 5])
        # spinning sign
        if wind >= 0.3:
            t = (wind - 0.3) / 0.7
            ctx.save(); ctx.translate(PX2 + 900 * t, FLOOR - 560 - 600 * t); ctx.rotate(t * 9)
            rect_r(ctx, -130, -55, 260, 110, 14); fl(ctx, hx('fff27a'), 6)
            text(ctx, "KEEP OUT", 0, 14, 50, RED, ow=0, shadow=False)
            ctx.restore()
        for k in range(6):
            yy = 500 + k * 170 + 30 * math.sin(il * 0.4 + k)
            x0 = -200 + ((il * 70 + k * 330) % 1600)
            ctx.move_to(x0, yy); ctx.curve_to(x0 + 150, yy - 40, x0 + 250, yy + 40, x0 + 400, yy)
        setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(10); ctx.stroke()
    ctx.restore()


def split(ctx, f, il):
    ctx.save(); ctx.rectangle(0, 0, W, H / 2); ctx.clip()
    ctx.save(); cam(ctx, 540, 1100, 0.9, 0, 0, f, sy=700)
    yard(ctx, il, sky=hx('c5b3ff'), fence=hx('d6f4ff'), tree_x=-200, sun=False)
    pile(ctx, 560, FLOOR, 900, 560, seed=12)
    hop = 90 * abs(math.sin(il * 0.25))
    b = draw(ctx, 560, FLOOR - 560 - 186 * KK - hop + 200, KK, 1, NBOY, P(eye='happy', mouth='grin', lsh=160, rsh=-160, lel=20, rel=-20, lhip=-30, lkn=50))
    falling(ctx, il, 100, 1000, 400, 1400, 20, 5)
    ctx.restore()
    ctx.restore()
    ctx.save(); ctx.rectangle(0, H / 2, W, H / 2); ctx.clip()
    ctx.translate(0, 360)
    ctx.save(); cam(ctx, 540, 960, 0.85, 0, 2, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb347')); ctx.fill()
    rays(ctx, 540, 900, 260, 1420, il * 0.03, col=(1, 1, 1), a=0.2, n=18)
    face(ctx, DAD, P(eye='glare', mouth='wavy'), 540, 880, 300, 0.02 * math.sin(il * 0.5))
    twitch(ctx, 540 + 0.6 * 300, 880 - 0.75 * 300, il, 1.3)
    ctx.restore()
    ctx.restore()
    ctx.rectangle(0, H / 2 - 8, W, 16); setc(ctx, OUT); ctx.fill()
    label(ctx, "\"THANKS, MISTER!!\"", 540, 860, 100, WHITE, -0.04, pop(il, 2, 6))
    label(ctx, "\"...my... PILE.\"", 540, 1450, 110, ORANGE, 0.03, pop(il, 16, 20))


def s3(ctx, f):
    lf = f - 216
    if lf < 46:
        guard_scene(ctx, f, lf, 0.0, z=1.12 + 0.05 * eio(pop(lf, 0, 46)), shake=shake_at(lf, [0], 8, 12))
        label(ctx, "ATTEMPT #2", 540, 330, 100, YEL, -0.05, pop(lf, 0, 3))
        label2(ctx, "\"NOBODY.", "TOUCHES. IT.\"", WHITE, pop(lf, 4, 8), 110, col2=RED, y=1400)
    elif lf < 80:
        il = lf - 46
        w_ = eio(pop(il, 3, 26))
        guard_scene(ctx, f, il, max(0.001, w_), z=1.12, rot=0, shake=4)
        label(ctx, "*WHOOOOOSH!*", 540, 330, 120, CYAN, -0.05, pop(il, 2, 5))
    else:
        split(ctx, f, lf - 80)


# ------------------------------------------------------------------ twist
SUNSET = hx('ff9a6b')


def s4(ctx, f):
    lf = f - 340
    if lf < 26:
        ctx.save(); cam(ctx, 560, 1120, 1.1 + 0.04 * eio(pop(lf, 0, 26)), 0, 0, f)
        yard(ctx, lf, sky=SUNSET, fence=hx('ffe0c8'), sun=False)
        pile(ctx, 650, FLOOR, 720, 470, seed=14, flag=True)
        b = draw(ctx, 210, FLOOR - 186 * DK, DK, 1, DAD, P(eye='closed', mouth='smile', rsh=-30, rel=-10, lsh=10))
        rake(ctx, b['front'][0], b['front'][1], -1.5, 0.9)
        sweat(ctx, b['head'][0] - 120, b['head'][1] - 40, lf, 1.0)
        ctx.restore()
        label(ctx, "6 HOURS LATER", 540, 330, 96, YEL, -0.04, pop(lf, 0, 3))
        label2(ctx, "\"ONE. LAST.", "PILE.\"", WHITE, pop(lf, 3, 7), 116, col2=ORANGE, y=1400)
    elif lf < 50:
        il = lf - 26
        ctx.save(); cam(ctx, 540, 960, 1.05 + 0.06 * eio(pop(il, 0, 24)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, SUNSET); ctx.fill()
        rays(ctx, 540, 900, 260, 1420, il * 0.02, col=(1, 1, 1), a=0.2, n=18)
        fd = 1 if (il // 6) % 2 == 0 else -1
        face(ctx, DAD, P(eye='smug', mouth='flat'), 540 + 30 * fd, 900, 300, 0.1 * fd, f_=fd)
        ctx.restore()
        label(ctx, "*glance* *glance*", 540, 330, 90, WHITE, 0.04, pop(il, 0, 3))
        label(ctx, "\"...nobody's watching?\"", 540, 1440, 104, YEL, -0.04, pop(il, 6, 10))
    elif lf < 82:
        il = lf - 50
        t = clamp(il / 30)
        ctx.save(); cam(ctx, 540, 1100, 1.0, 8, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, SUNSET); ctx.fill()
        rays(ctx, 540, 1100, 200, 1600, il * 0.06, col=(1, 0.9, 0.5), a=0.4, n=16)
        falling(ctx, il * 3, -100, 1200, 0, 2000, 30, 9, 1.6)
        pile(ctx, 700, 1900, 1100, 300, seed=15)
        x = lerp(60, 680, t); y = lerp(1250, 1050, t) - 150 * math.sin(math.pi * t)
        draw(ctx, x, y, 2.0, 1, DAD, P(eye='happy', mouth='open', rot=70, lsh=175, rsh=-175, lel=0, rel=0, lhip=10, rhip=-10))
        for k in range(5):
            ctx.move_to(x - 480 - k * 30, y + 120 + k * 60); ctx.line_to(x - 800, y + 120 + k * 60)
        setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(10); ctx.stroke()
        ctx.restore()
        label(ctx, "\"WHEEEEEE!!\"", 540, 330, 130, YEL, -0.05, pop(il, 2, 5))
    else:
        il = lf - 82   # 0..58
        pull = eio(pop(il, 34, 46))
        ctx.save(); cam(ctx, lerp(560, 620, pull), lerp(1180, 1120, pull), lerp(1.3, 1.08, pull), 0, shake_at(il, [0], 16, 26), f)
        yard(ctx, il, sky=SUNSET, fence=hx('ffe0c8'), sun=False)
        if il >= 34:
            draw(ctx, 1010, FLOOR - 186 * MK, MK, -1, MOM, P(eye='shock', mouth='open', lsh=20, rsh=-20))
            draw(ctx, 850, FLOOR - 186 * KK, KK, -1, BOY, P(eye='shock', mouth='open', lsh=60, rsh=-60, lel=-30, rel=30))
        up_ = eout(pop(il, 8, 16))
        b = draw(ctx, 600, FLOOR + 140 - 200 * up_ - 186 * DK, DK, 1, DAD, P(eye='happy', mouth='grin', lsh=140, rsh=-140, lel=20, rel=-20))
        leaf_hat(ctx, b, 5)
        pile(ctx, 600, FLOOR + 30, 1000, 130, seed=16)
        burst(ctx, 600, FLOOR - 120, il / 30, 100, 6, big=True)
        if il < 4:
            ctx.rectangle(-500, -500, 2500, 3000); setc(ctx, (1, 1, 1, 0.6 * (1 - il / 4))); ctx.fill()
        ctx.restore()
        if il < 34:
            label(ctx, "*KA-FLOOMP!!*", 540, 330, 120, ORANGE, -0.05, pop(il, 0, 3))
        else:
            label(ctx, "\"DAD?!\"", 540, 330, 130, CYAN, -0.05, pop(il, 34, 37))
        if il >= 16:
            label2(ctx, "\"...okay.", "I GET it now.\"", WHITE, pop(il, 16, 20), 108, col2=YEL, y=1400)


# ------------------------------------------------------------------ end
def s5(ctx, f):
    lf = f - 480
    if lf < 50:
        ctx.save(); cam(ctx, 560, 1120, 1.12, 0, 0, f)
        yard(ctx, lf, sky=hx('ffc08a'), sun=False, tree_x=170)
        for x, ch, k, s in ((330, DAD, DK, 1), (620, BOY, KK, -1), (870, MOM, MK, -1)):
            ph = lf * 0.45 + x
            arms = 150 + 20 * math.sin(ph)
            b = draw(ctx, x, FLOOR + 70 - 186 * k - 30 * abs(math.sin(ph * 0.5)), k, s, ch,
                     P(eye='happy', mouth='grin' if ch is not MOM else 'open', lsh=arms, rsh=-arms, lel=20, rel=-20))
            leaf_hat(ctx, b, x)
        pile(ctx, 600, FLOOR + 40, 1150, 150, seed=17)
        for k in range(3):
            burst(ctx, 330 + k * 270, FLOOR - 60, ((lf + k * 12) % 36) / 30, 18, 30 + k, sp=0.6)
        ctx.restore()
        label(ctx, "*LEAF FIGHT!!*", 540, 330, 116, ORANGE, -0.05, pop(lf, 0, 3))
    elif lf < 92:
        il = lf - 50
        drop = eio(pop(il, 8, 16))
        ctx.save(); cam(ctx, 560, 1080, 1.05, 0, shake_at(il, [16], 14, 24), f)
        yard(ctx, il, sky=hx('ffc08a'), sun=False, tree_x=170, tree_full=1 - drop, tree_shake=0.04 if il < 16 else 0)
        if il < 16:
            for x, ch, k, s in ((330, DAD, DK, 1), (620, BOY, KK, -1), (870, MOM, MK, -1)):
                b = draw(ctx, x, FLOOR + 130 - 186 * k, k, s, ch, P(eye='shock', mouth='open', lsh=20, rsh=-20))
            pile(ctx, 600, FLOOR + 40, 1150, 150, seed=17)
            # falling mass of leaves
            rnd = random.Random(40)
            for k in range(120):
                x = 170 + rnd.uniform(-300, 900)
                y = lerp(380, FLOOR - 200, drop) + rnd.uniform(-300, 300) * (1 - drop * 0.5)
                leaf(ctx, x, y, 1.6, k, LEAFC[k % 5])
        else:
            pile(ctx, 600, FLOOR + 40, 1500, 760, seed=18)
            for j, (ex, ey) in enumerate(((330, 1150), (620, 1310), (870, 1180))):
                bl = ((il + j * 5) % 26) < 2
                for dx in (-34, 34):
                    if bl:
                        ctx.move_to(ex + dx - 24, ey); ctx.line_to(ex + dx + 24, ey); ink(ctx, 7); ctx.stroke()
                    else:
                        ellipse(ctx, ex + dx, ey, 28, 34); fl(ctx, WHITE, 5)
                        ellipse(ctx, ex + dx, ey + 6, 11, 13); setc(ctx, INK); ctx.fill()
        ctx.restore()
        if il >= 14:
            label(ctx, "*FWUMP!!*", 540, 330, 130, ORANGE, -0.05, pop(il, 14, 17))
        else:
            label(ctx, "*rustle...*", 540, 330, 90, WHITE, 0.04, pop(il, 0, 3))
        if il >= 24:
            label(ctx, "\"...worth it.\"", 540, 1440, 120, YEL, -0.04, pop(il, 24, 28))
    elif lf < 132:
        il = lf - 92   # 0..40
        ctx.save(); cam(ctx, 560, 1160, 1.15, 0, 0, f)
        yard(ctx, il, sky=hx('a8e4ff'), tree_x=170, tree_full=0.0)
        pile(ctx, 620, FLOOR, 540, 340, seed=19, flag=True)
        b = draw(ctx, 270, FLOOR - 186 * DK, DK, 1, DAD, P(eye='smug' if il < 20 else 'shock', mouth='grin' if il < 20 else 'flat',
                                                         rsh=-60, rel=-20, lsh=20))
        rake(ctx, b['front'][0], b['front'][1], -0.6 if il < 20 else -0.3, 0.9)
        if il >= 14:
            wig = 0.06 * math.sin(il * 2.2) if il < 32 else 0
            jump = eio(pop(il, 32, 40))
            dx = lerp(1250, 950, eout(pop(il, 14, 22)))
            ctx.save(); ctx.translate(dx, FLOOR + 10); ctx.rotate(wig - 0.5 * jump); ctx.translate(-dx, -(FLOOR + 10))
            dog(ctx, dx - 250 * jump, FLOOR + 10 - 380 * jump, 0.95, -1, il)
            sparkle(ctx, dx - 250 * jump - 160 * 0.95, FLOOR + 10 - 380 * jump - 250 * 0.95, 30 + 6 * math.sin(il), YEL)
            ctx.restore()
        ctx.restore()
        label(ctx, "NEXT MORNING", 540, 330, 96, BLUE, -0.04, pop(il, 0, 3))
        if il < 20:
            label(ctx, "\"PERFECT.\"", 540, 1440, 130, YEL, -0.04, pop(il, 2, 6))
        else:
            label(ctx, "\"...don't you DARE.\"", 540, 1440, 110, RED, -0.04, pop(il, 20, 24))
    else:
        s1(ctx, f, f - 612)


SHOTS = [(0, s1), (54, s2), (216, s3), (340, s4), (480, s5)]
CUTS = (54, 100, 124, 160, 216, 262, 296, 340, 366, 390, 422, 480, 530, 572, 612)


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
                              "-i", "out/leaf_pile_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
