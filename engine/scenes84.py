"""'Dad vs the ketchup bottle' - original, general-audience comedy short, 22s.
Hook:   kitchen medium shot: red-faced Dad shaking an upside-down ketchup bottle over the kid's dry fries
        "COME... ON...!!" + caption "DAD vs THE KETCHUP BOTTLE:"
Beat 1: "Ketchup? EASY." *TAP! TAP! TAP!* on the bottom -> nothing *cricket*
Beat 2: macro: the ketchup creeps down to the cap... "almost..." -> *shloop* slides back up "...it went BACK?!"
Beat 3: Dutch-tilt *SHAKE! SHAKE!* -> two-hand squeeze, the bottle bulges "HNNNGH!!"
Turn:   kid: "Dad... it still has the SEAL on." -> Dad ECU "...the WHAT?!"
        macro: cap off, foil seal, *RIIIP* -> the bottle trembles "...uh-oh."
        *SPLOOORT!!* jet across the kitchen hits Mom walking in with a salad -> "...thanks, honey." ; dog licks
Twist:  "PLOT TWIST: HE LIKES THEM PLAIN." kid: "Actually... I like them PLAIN."
        Mom hands Dad a pickle jar "Honey... open THIS?" -> Dad strains -> loop to the hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes65 import dog
from scenes82 import window, picture
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
KET = hx('e8232f'); KET_D = hx('b3121c'); KET_L = hx('ff6a6a')
DAD = dict(doodle.DAD, shirt=hx('5fb8ef'), pants=hx('3d5a9e'))
DAD_R = dict(DAD, skin=hx('f07a6a'))
MOM = dict(doodle.MOM_G, shirt=hx('ffc93c'), pants=hx('2f4a8a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('22b45a'), pants=hx('3d7bff'), shoes=hx('ff5fa8'))
N = 660
FLOOR = 1560
GND = 1590
KDAD, KMOM, KKID = 1.1, 1.02, 0.86
TX0, TX1, TY = 760, 1330, 1330          # table left/right, top
DADX, KIDX, PLATE = 700, 1240, 870

CAPS = {'p1': [[("DAD vs ", OUT), ("THE KETCHUP BOTTLE:", RED)]],
        'p2': [[("PLOT TWIST:", RED)], [("HE LIKES THEM ", OUT), ("PLAIN.", GREEN)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def bottle(ctx, x, y, ang=math.pi, s=1.0, bulge=0.0, cap=True, seal=False, peel=0.0, fill=0.75, creep=0.0, tremble=0.0, lf=0):
    """squeeze bottle. (x, y) = grip point (middle of the body); ang 0 = cap up, pi = cap down.
    returns the nozzle tip in user space."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang + tremble * 0.06 * math.sin(lf * 2.3)); ctx.scale(s, s)
    w, h = 62 * (1 + 0.35 * bulge), 190
    # body (rounded, bulging in the middle)
    ctx.new_path()
    ctx.move_to(-40, -h / 2)
    ctx.curve_to(-w - 4, -h / 2 + 10, -w * 1.08, 0, -w, h / 2 - 30)
    ctx.curve_to(-w, h / 2 + 4, -w + 10, h / 2 + 10, 0, h / 2 + 10)
    ctx.curve_to(w - 10, h / 2 + 10, w, h / 2 + 4, w, h / 2 - 30)
    ctx.curve_to(w * 1.08, 0, w + 4, -h / 2 + 10, 40, -h / 2)
    ctx.close_path()
    body = ctx.copy_path()
    fl(ctx, hx('ffe3e3'), 6)
    # ketchup inside: rests at the BOTTOM (base end) in world space; creep pulls a tongue toward the cap
    ctx.save(); ctx.new_path(); ctx.append_path(body); ctx.clip()
    base_y = h / 2 + 10
    lvl = base_y - (h + 10) * fill
    ctx.rectangle(-200, lvl, 400, 400); setc(ctx, KET); ctx.fill()
    if creep > 0:
        ctx.new_path(); ctx.move_to(-30, lvl + 2)
        ctx.curve_to(-26, lvl - 60 * creep, -14, -h / 2 - 20 * creep, 0, lvl - (lvl + h / 2 + 10) * creep)
        ctx.curve_to(14, -h / 2 - 20 * creep, 26, lvl - 60 * creep, 30, lvl + 2); ctx.close_path(); setc(ctx, KET); ctx.fill()
    ctx.rectangle(-w * 0.55, -h / 2 + 30, 14, h - 70); setc(ctx, (1, 1, 1, 0.45)); ctx.fill()   # shine
    ctx.restore()
    ctx.new_path(); ctx.append_path(body); ink(ctx, 6); ctx.stroke()
    # label: a cute tomato (no brand)
    rect_r(ctx, -w * 0.8, -20, w * 1.6, 70, 14); fl(ctx, WHITE, 4)
    ellipse(ctx, 0, 16, 22, 19); fl(ctx, KET, 3)
    poly(ctx, [(-10, -2), (0, 4), (10, -2), (0, -8)]); fl(ctx, GREEN, 2)
    # neck + seal + cap
    rect_r(ctx, -40, -h / 2 - 22, 80, 26, 8); fl(ctx, hx('ffe3e3'), 5)
    tip = (0, -h / 2 - 22)
    if seal:
        # silver foil seal, peel lifts it from the left edge
        ctx.save(); ctx.translate(-40, -h / 2 - 22); ctx.rotate(-1.9 * peel)
        rect_r(ctx, 0, -10, 80, 12, 4); fl(ctx, hx('d8dde6'), 4)
        poly(ctx, [(0, -6), (-34, -18), (-34, 2)]); fl(ctx, hx('d8dde6'), 3)              # pull tab
        for k in range(3):
            sparkle(ctx, 18 + 22 * k, -4, 7, WHITE)
        ctx.restore()
    if cap:
        rect_r(ctx, -46, -h / 2 - 66, 92, 50, 14); fl(ctx, WHITE, 5)
        poly(ctx, [(-14, -h / 2 - 64), (14, -h / 2 - 64), (6, -h / 2 - 92), (-6, -h / 2 - 92)]); fl(ctx, WHITE, 4)
        ellipse(ctx, 0, -h / 2 - 93, 5, 3); setc(ctx, INK); ctx.fill()
        tip = (0, -h / 2 - 94)
    out = ctx.user_to_device(*tip)
    ctx.restore()
    return ctx.device_to_user(*out)


def fries(ctx, x, y, s=1.0, dollop=0.0, lf=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 6, 120, 26); fl(ctx, WHITE, 5)
    ellipse(ctx, 0, 2, 90, 16); setc(ctx, hx('e8eef6')); ctx.fill()
    rnd = random.Random(3)
    for k in range(11):
        a = rnd.uniform(-0.5, 0.5); fx = rnd.uniform(-70, 70)
        ctx.save(); ctx.translate(fx, 4); ctx.rotate(a)
        rect_r(ctx, -8, -70 + rnd.uniform(0, 20), 16, 70, 4); fl(ctx, hx('ffd34f'), 3)
        ctx.restore()
    if dollop > 0:
        ellipse(ctx, 8, -40, 26 * dollop, 18 * dollop); fl(ctx, KET, 3)
        ellipse(ctx, 0, -46, 8 * dollop, 5 * dollop); setc(ctx, (1, 1, 1, 0.6)); ctx.fill()
    ctx.restore()


def splats(ctx, x, y, r, seed, n=7, amt=1.0):
    if amt <= 0:
        return
    rnd = random.Random(seed)
    for k in range(n):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, r)
        rr = rnd.uniform(0.1, 0.22) * r * amt
        ellipse(ctx, x + math.cos(a) * d, y + math.sin(a) * d * 0.9, rr, rr * rnd.uniform(0.7, 1.1), a); fl(ctx, KET, 3)
        ctx.rectangle(x + math.cos(a) * d - rr * 0.2, y + math.sin(a) * d * 0.9, rr * 0.4, rr * 1.4 * amt); setc(ctx, KET); ctx.fill()


def jar(ctx, x, y, s=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rect_r(ctx, -55, -70, 110, 140, 22); fl(ctx, hx('d9f5ff'), 6)
    ctx.save(); rect_r(ctx, -55, -70, 110, 140, 22); ctx.clip()
    for k in range(5):
        ellipse(ctx, -28 + 28 * (k % 3), -30 + 30 * (k // 2), 18, 34, 0.3 * k); fl(ctx, hx('7ed36b'), 3)
    ctx.restore()
    rect_r(ctx, -60, -96, 120, 32, 8); fl(ctx, GOLD, 5)
    ctx.restore()


def bowl(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for k in range(6):
        ellipse(ctx, -50 + 20 * k, -26 - 10 * (k % 2), 26, 18, 0.4 * k); fl(ctx, (GREEN, hx('7ed36b'))[k % 2], 3)
    ellipse(ctx, 30, -36, 12, 12); fl(ctx, RED, 3)
    ctx.new_path(); ctx.move_to(-80, -20); ctx.curve_to(-70, 40, 70, 40, 80, -20); ctx.close_path(); fl(ctx, hx('ff9ec2'), 5)
    ctx.restore()


# ------------------------------------------------------------------ set: cosy kitchen
def kitchen(ctx, lf, pic_tilt=0.0, mess=0.0):
    wall = hx('fff0c4')
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, wall); ctx.fill()
    for i in range(-20, 40):                                          # soft wallpaper stripes + little hearts
        ctx.rectangle(i * 120, -3000, 46, 6000); setc(ctx, dark(wall, 0.96)); ctx.fill()
    rnd = random.Random(84)
    for k in range(70):
        sparkle(ctx, rnd.uniform(-300, 2400), rnd.uniform(-200, 1100), 9, dark(wall, 0.9))
    # checker backsplash band
    for i in range(-10, 40):
        for j in range(2):
            ctx.rectangle(i * 60, 1150 + j * 60, 60, 60); setc(ctx, WHITE if (i + j) % 2 else hx('9fe0d0')); ctx.fill()
    ctx.move_to(-3000, 1150); ctx.line_to(6000, 1150); ctx.move_to(-3000, 1270); ctx.line_to(6000, 1270); ink(ctx, 4); ctx.stroke()
    ctx.rectangle(-3000, 1270, 9000, FLOOR - 1270); setc(ctx, hx('ffd9a8')); ctx.fill()
    window(ctx, lf)
    # shelf with jars + plant
    rect_r(ctx, 880, 720, 360, 22, 6); fl(ctx, hx('a0603a'), 5)
    for k, c in enumerate((PINK, GOLD, CYAN)):
        rect_r(ctx, 900 + 70 * k, 640, 54, 80, 12); fl(ctx, c, 4)
        rect_r(ctx, 896 + 70 * k, 628, 62, 18, 6); fl(ctx, WHITE, 3)
    poly(ctx, [(1140, 720), (1210, 720), (1200, 660), (1150, 660)]); fl(ctx, hx('ff8a5c'), 4)
    for a in (-0.7, -0.2, 0.3, 0.8):
        ellipse(ctx, 1175 + 46 * math.sin(a), 640 - 18 * math.cos(a), 14, 36, a); fl(ctx, GREEN, 3)
    # wall clock
    ellipse(ctx, 1520, 620, 70, 70); fl(ctx, WHITE, 6)
    ctx.move_to(1520, 620); ctx.line_to(1520 + 40 * math.sin(lf * 0.05), 620 - 40 * math.cos(lf * 0.05))
    ctx.move_to(1520, 620); ctx.line_to(1545, 600); ink(ctx, 5); ctx.stroke()
    picture(ctx, 1520, 920, pic_tilt + 0.02 * math.sin(lf * 0.05))
    # doorway on the right
    rect_r(ctx, 1680, 720, 300, 860, 10); fl(ctx, hx('ffe8b0'), 7)
    rect_r(ctx, 1710, 750, 240, 830, 6); setc(ctx, hx('ffd082')); ctx.fill()
    # fridge on the left
    rect_r(ctx, 120, 820, 280, 760, 30); fl(ctx, hx('dff3ff'), 7)
    ctx.move_to(130, 1080); ctx.line_to(390, 1080); ink(ctx, 5); ctx.stroke()
    rect_r(ctx, 360, 920, 14, 110, 6); fl(ctx, hx('b8c4d6'), 3); rect_r(ctx, 360, 1110, 14, 140, 6); fl(ctx, hx('b8c4d6'), 3)
    for k, c in enumerate((GOLD, PINK, CYAN)):                         # magnets + a kid drawing
        ellipse(ctx, 170 + 60 * k, 860, 14, 14); fl(ctx, c, 3)
    rect_r(ctx, 180, 1140, 130, 110, 4); fl(ctx, WHITE, 4)
    ellipse(ctx, 245, 1185, 26, 26); fl(ctx, GOLD, 3)
    # floor
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('c9874e')); ctx.fill()
    for k in range(-10, 40):
        ctx.move_to(k * 140, FLOOR); ctx.line_to(k * 140 - 130, FLOOR + 600)
    setc(ctx, hx('b5743e')); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-3000, FLOOR); ctx.line_to(6000, FLOOR); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 1040, FLOOR + 140, 640, 90); fl(ctx, hx('9fd8ff'), 6)
    ellipse(ctx, 1040, FLOOR + 140, 540, 66); setc(ctx, hx('c8ebff')); ctx.fill()
    if mess > 0:                                                       # ketchup on the wall / picture after the blast
        splats(ctx, 1470, 960, 90, 5, 6, mess)
        splats(ctx, 1150, 690, 70, 6, 5, mess)
        splats(ctx, 1300, 1200, 60, 7, 4, mess)


def table(ctx, dollop=0.0, lf=0, plate=True, mess=0.0):
    for lx in (TX0 + 40, TX1 - 40):
        rect_r(ctx, lx - 16, TY + 60, 32, GND - TY - 50, 8); fl(ctx, hx('a0603a'), 5)
    ctx.new_path(); ctx.move_to(TX0 - 20, TY)
    ctx.line_to(TX1 + 20, TY); ctx.line_to(TX1 + 20, TY + 80)
    n = 9
    for i in range(n):
        x1 = TX1 + 20 - (TX1 - TX0 + 40) * (i + 1) / n; xm = (x1 + TX1 + 20 - (TX1 - TX0 + 40) * i / n) / 2
        ctx.curve_to(xm + 10, TY + 110, xm - 10, TY + 110, x1, TY + 80)
    ctx.close_path(); fl(ctx, WHITE, 6)
    ctx.save(); ctx.move_to(TX0 - 20, TY); ctx.line_to(TX1 + 20, TY); ctx.line_to(TX1 + 20, TY + 100); ctx.line_to(TX0 - 20, TY + 100); ctx.clip()
    for i in range(0, 20):                                             # gingham checks
        ctx.rectangle(TX0 - 20 + i * 32, TY, 16, 110); setc(ctx, (0.95, 0.3, 0.35, 0.35)); ctx.fill()
    ctx.restore()
    if mess > 0:
        splats(ctx, 1150, TY + 40, 50, 9, 4, mess)
    if plate:
        fries(ctx, PLATE, TY - 6, 0.9, dollop, lf)


# ------------------------------------------------------------------ people
def stand(ctx, ch, x, k, p, f_=1):
    return draw(ctx, x, GND - 186 * k, k, f_, ch, p)


def kid_at(ctx, lf, eye='flat', mouth='flat', p=None, x=KIDX):
    p = p or P(eye=eye, mouth=mouth, lsh=40, lel=-90, rsh=60, rel=-100)
    return stand(ctx, KID, x, KKID, p, f_=-1)


def dad_shake(ctx, lf, amp=1.0, ch=DAD_R, x=DADX, eye='glare', mouth='scream'):
    sh = math.sin(lf * 1.6) * amp
    d = stand(ctx, ch, x, KDAD, P(eye=eye, mouth=mouth, torso=8, lsh=120 + 14 * sh, lel=-30, rsh=135 + 14 * sh, rel=-20, head=6))
    return d, sh


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = 1.2 + 0.04 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, 990, 1270, z, 0, 3, f)
    kitchen(ctx, lf)
    kid_at(ctx, lf, eye='normal', mouth='flat', p=P(eye='normal', mouth='flat', lsh=40, lel=-120, rsh=30, rel=-130, head=-6))
    d, sh = dad_shake(ctx, lf)
    table(ctx, 0, lf)
    hx_, hy_ = d['front']
    bottle(ctx, hx_ + 75, hy_ - 30 + 22 * sh, math.pi + 0.15 * sh, 0.9)
    for k in range(3):                                                 # shake lines
        ctx.move_to(hx_ + 90, hy_ - 40 + 40 * k); ctx.line_to(hx_ + 130, hy_ - 50 + 40 * k)
        ctx.move_to(hx_ - 50, hy_ - 40 + 40 * k); ctx.line_to(hx_ - 90, hy_ - 50 + 40 * k)
    ink(ctx, 5); ctx.stroke()
    sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.6, lf, 1.0)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"COME...", "...ON...!!\"", WHITE, t, 120, col2=RED, y=1440)


# ------------------------------------------------------------------ shot 2
def tapping(ctx, f, il):
    # il 0..66: 0-22 smug "Ketchup? EASY."; taps at 24/34/44 + 50-56 rapid; 58 "...nothing." *cricket*
    taps = [24, 34, 44, 50, 53, 56]
    ctx.save(); cam(ctx, 1000, 1280, 1.14, 0, shake_at(il, taps, 4, 4), f)
    kitchen(ctx, il)
    kid_at(ctx, il, eye='normal', mouth='smile' if il < 22 else 'flat')
    if il < 22:
        d = stand(ctx, DAD, DADX, KDAD, P(eye='smug', mouth='grin', lsh=20, lel=-30, rsh=150, rel=-20, torso=-4))
        table(ctx, 0, il)
        hx_, hy_ = d['front']
        bottle(ctx, hx_, hy_ - 60, 0.15, 0.9)
        sparkle(ctx, hx_ + 70, hy_ - 150, 22, GOLD)
    else:
        k = max([q for q in taps if q <= il] + [0])
        hit = 1 - pop(il, k, k + 3)
        d = stand(ctx, DAD, DADX, KDAD, P(eye='glare', mouth='flat', torso=6, lsh=130 + 30 * hit, lel=-60 - 40 * hit, rsh=135, rel=-20, head=6))
        table(ctx, 0, il)
        hx_, hy_ = d['front']
        bottle(ctx, hx_ + 75, hy_ - 30 + 6 * hit, math.pi, 0.9)
    ctx.restore()
    if il < 22:
        label2(ctx, "\"Ketchup?", "EASY.\"", WHITE, pop(il, 2, 6), 120, col2=GOLD, y=1440)
    elif 24 <= il < 58:
        k = max([q for q in taps if q <= il])
        i = taps.index(k)
        label(ctx, "*TAP!*" if i < 3 else "*tap tap tap*", 540, 560 + 70 * min(i, 3), 120 if i < 3 else 96, ORANGE, (-0.06, 0.05, -0.03, 0.04, 0, -0.04)[i], pop(il, k, k + 3))
    elif il >= 58:
        label(ctx, "...nothing.", 540, 1450, 120, WHITE, -0.03, pop(il, 58, 61))


def macro_creep(ctx, f, il):
    # il 0..50: upside-down bottle fills the frame; ketchup creeps to the cap (0-26) "almost..." ; 30 *shloop* back up
    creep = eio(pop(il, 2, 26)) * (1 - eio(pop(il, 30, 36)))
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eio(pop(il, 0, 28)), 0, shake_at(il, [30], 6, 6), f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('fff0c4')); ctx.fill()
    for i in range(-6, 14):
        ctx.rectangle(i * 120, -600, 46, 3200); setc(ctx, dark(hx('fff0c4'), 0.96)); ctx.fill()
    fries(ctx, 540, 1520, 2.4)
    bottle(ctx, 540, 820, math.pi, 2.6, creep=creep, fill=0.7)
    for sx in (-1, 1):                                                 # Dad's fingers gripping
        for k in range(3):
            ellipse(ctx, 540 + sx * 190, 700 + 60 * k, 44, 30); fl(ctx, DAD['skin'], 5)
    if il < 30:
        rays(ctx, 540, 1180, 120, 260, il * 0.05, col=(1, 1, 1), a=0.5 * pop(il, 18, 26), n=12)
    ctx.restore()
    if il < 30:
        label(ctx, "almost...", 540, 1450, 112, WHITE, -0.03, pop(il, 10, 14))
    else:
        label(ctx, "*shloop*", 540, 560, 112, KET_L, 0.04, pop(il, 30, 33))
        label2(ctx, "\"...it went", "BACK?!\"", WHITE, pop(il, 34, 38), 116, col2=RED, y=1440)


def shake_squeeze(ctx, f, il):
    # il 0..70: 0-36 Dutch-tilt violent shaking with ghosts; 36-70 two-hand squeeze, bottle bulges "HNNNGH!!"
    ctx.save()
    rot = 8 if il < 36 else -4
    cam(ctx, 960, 1260, 1.18 if il < 36 else 1.3, rot, shake_at(il, list(range(0, 36, 6)) + [36], 6, 8), f)
    kitchen(ctx, il, pic_tilt=0.12 * pop(il, 0, 30))
    kid_at(ctx, il, eye='shock', mouth='open', p=P(eye='shock', mouth='open', lsh=40, lel=-120, rsh=30, rel=-130, rot=-4))
    if il < 36:
        d, sh = dad_shake(ctx, il * 1.8, 1.4)
        table(ctx, 0, il)
        hx_, hy_ = d['front']
        for g in (2, 1):                                               # speed ghosts
            ctx.push_group()
            bottle(ctx, hx_ + 75, hy_ - 30 + 34 * math.sin((il - g) * 2.9), math.pi + 0.3 * math.sin((il - g) * 2.9), 0.9)
            ctx.pop_group_to_source(); ctx.paint_with_alpha(0.25)
        bottle(ctx, hx_ + 75, hy_ - 30 + 34 * math.sin(il * 2.9), math.pi + 0.3 * math.sin(il * 2.9), 0.9)
    else:
        u = eio(pop(il, 38, 64))
        d = stand(ctx, DAD_R, DADX + 20, KDAD, P(eye='closed', mouth='grin', torso=4, lsh=120, lel=-90, rsh=110, rel=-80, head=4,
                                                rot=1.5 * math.sin(il * 2)))
        table(ctx, 0, il)
        bx = (d['front'][0] + d['back'][0]) / 2 + 10; by = (d['front'][1] + d['back'][1]) / 2
        bottle(ctx, bx, by, 0.0, 0.9, bulge=u * 1.4, tremble=u, lf=il)
        for sx in (-1, 1):
            ellipse(ctx, bx + sx * (56 + 30 * u), by, 22, 30); fl(ctx, DAD_R['skin'], 4)
        sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.6, il, 1.0)
        sweat(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.7, il + 20, 0.8)
    ctx.restore()
    if il < 36:
        for j, (a, y) in enumerate(((0, 540), (12, 640), (24, 740))):
            label(ctx, "*SHAKE!*", 540 + (-120, 120, 0)[j], y, 110, PURPLE, (-0.08, 0.07, -0.04)[j], pop(il, a, a + 3))
    else:
        label2(ctx, "\"HNNNNGH...", "...!!\"", WHITE, pop(il, 40, 44), 116, col2=RED, y=1440)


def s2(ctx, f):
    lf = f - 54
    if lf < 66:
        tapping(ctx, f, lf)
    elif lf < 116:
        macro_creep(ctx, f, lf - 66)
    else:
        shake_squeeze(ctx, f, lf - 116)


# ------------------------------------------------------------------ shot 3: the seal
def seal_line(ctx, f, il):
    # il 0..50: kid leans in and points at the bottle "Dad... it still has the SEAL on."
    ctx.save(); cam(ctx, 1000, 1280, 1.18, 0, 0, f)
    kitchen(ctx, il, pic_tilt=0.12)
    kx = lerp(KIDX, KIDX - 120, eio(il / 12))
    k = kid_at(ctx, il, p=P(eye='smug', mouth='smile', lsh=-30, lel=-20, rsh=-95, rel=0, torso=-6), x=kx)
    d = stand(ctx, DAD_R, DADX + 20, KDAD, P(eye='shock', mouth='flat', torso=4, lsh=120, lel=-90, rsh=110, rel=-80, head=4))
    table(ctx, 0, il)
    bx = (d['front'][0] + d['back'][0]) / 2 + 10; by = (d['front'][1] + d['back'][1]) / 2
    bottle(ctx, bx, by, 0.0, 0.9, bulge=1.4, tremble=0.5, lf=il)
    for sx in (-1, 1):
        ellipse(ctx, bx + sx * 86, by, 22, 30); fl(ctx, DAD_R['skin'], 4)
    ctx.restore()
    label2(ctx, "\"Dad... it still has", "the SEAL on.\"", WHITE, pop(il, 4, 8), 100, col2=GOLD, y=1440)


def the_what(ctx, f, il):
    # il 0..40: the one big Dad close-up
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.08 * eio(il / 40), 0, shake_at(il, [0], 6, 8), f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('ffd34f')); ctx.fill()
    rays(ctx, 540, 900, 240, 1500, il * 0.02, col=(1, 1, 1), a=0.35, n=16)
    face(ctx, DAD_R, P(eye='shock', mouth='open'), 540, 900, 205, 0.04 * math.sin(il * 2))
    ctx.restore()
    label2(ctx, "\"...the", "WHAT?!\"", WHITE, pop(il, 2, 5), 128, col2=RED, y=1440)


def s3(ctx, f):
    lf = f - 240
    if lf < 50:
        seal_line(ctx, f, lf)
    else:
        the_what(ctx, f, lf - 50)


# ------------------------------------------------------------------ shot 4: peel -> SPLOOORT
def peel_macro(ctx, f, il):
    # il 0..42: cap twists off (0-10), foil seal, finger pulls the tab *RIIIP* (14-24), bottle trembles "...uh-oh." (28)
    ctx.save(); cam(ctx, 540, 960, 1.0, 0, shake_at(il, [16], 6, 6) + (2 if il > 26 else 0), f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('ffe3ef')); ctx.fill()
    for i in range(-6, 14):
        ctx.rectangle(i * 120, -600, 46, 3200); setc(ctx, dark(hx('ffe3ef'), 0.96)); ctx.fill()
    for k in range(12):
        sparkle(ctx, 80 + (k * 211) % 920, 500 + (k * 137) % 1000, 12, dark(hx('ffe3ef'), 0.88))
    peel = eio(pop(il, 14, 24))
    bottle(ctx, 540, 1180, 0.0, 2.4, bulge=1.4, cap=False, seal=True, peel=peel, tremble=pop(il, 24, 30), lf=il)
    if il < 12:                                                        # cap spinning away
        u = pop(il, 0, 12)
        ctx.save(); ctx.translate(lerp(540, 900, u), lerp(800, 560, u) + 300 * u * u); ctx.rotate(u * 6)
        rect_r(ctx, -110, -60, 220, 120, 30); fl(ctx, WHITE, 6); ctx.restore()
    fx = lerp(440, 300, peel); fy = lerp(890, 760, peel)                # Dad's finger on the tab
    rect_r(ctx, fx - 260, fy - 30, 260, 70, 34); fl(ctx, DAD_R['skin'], 6)
    ellipse(ctx, fx - 10, fy + 4, 40, 34); fl(ctx, DAD_R['skin'], 6)
    if il > 26:
        for k in range(6):
            a = -1.57 + (k - 2.5) * 0.35
            ctx.move_to(540 + 200 * math.cos(a), 900 + 200 * math.sin(a)); ctx.line_to(540 + 260 * math.cos(a), 900 + 260 * math.sin(a))
        ink(ctx, 6); ctx.stroke()
    ctx.restore()
    if il < 12:
        label(ctx, "*twist*", 540, 560, 104, WHITE, -0.04, pop(il, 1, 4))
    elif il < 28:
        label(ctx, "*RIIIIP!*", 540, 560, 124, hx('9fb3c8'), 0.04, pop(il, 15, 18))
    else:
        label(ctx, "\"...uh-oh.\"", 540, 1450, 130, WHITE, -0.03, pop(il, 28, 31))


def blast(ctx, f, il):
    # il 0..60: Mom walks in with salad (0-8); *SPLOOORT!!* jet 4-30 hits Mom; 36 "...thanks, honey." dog licks
    jet = pop(il, 4, 10) * (1 - pop(il, 28, 34))
    hit = eio(pop(il, 8, 20))
    ctx.save(); cam(ctx, 1150, 1250, 0.92, 0, shake_at(il, [4, 10, 16], 12, 10), f)
    kitchen(ctx, il, pic_tilt=0.12 + 0.3 * hit, mess=hit)
    mx = lerp(1880, 1640, eio(il / 8))
    m = stand(ctx, MOM, mx, KMOM, P(eye='happy' if il < 10 else 'shock', mouth='open' if il < 10 else 'flat', lsh=60, lel=-100, rsh=70, rel=-100,
                                   lhip=16 * math.sin(il * 0.8) * (il < 8), rhip=-16 * math.sin(il * 0.8) * (il < 8)), f_=-1)
    bowl(ctx, (m['front'][0] + m['back'][0]) / 2, (m['front'][1] + m['back'][1]) / 2, 0.9)
    # kid ducks under the jet
    duck = eio(pop(il, 4, 10))
    ctx.save(); ctx.rectangle(-3000, -3000, 9000, TY + 3060); ctx.clip()          # kid ducks behind the table
    draw(ctx, KIDX, GND - 186 * KKID + 230 * duck, KKID, -1, KID, P(eye='shock', mouth='open', lsh=170, lel=-40, rsh=170, rel=-40))
    ctx.restore()
    d = stand(ctx, DAD_R, DADX + 20, KDAD, P(eye='shock', mouth='scream', torso=-8, lsh=80, lel=-30, rsh=75, rel=-20, head=-4, rot=-3 * jet))
    table(ctx, 0, il, mess=hit)
    bx = (d['front'][0] + d['back'][0]) / 2 + 20; by = (d['front'][1] + d['back'][1]) / 2
    tip = bottle(ctx, bx, by, math.pi / 2 + 0.1, 0.9, bulge=1.4 * (1 - pop(il, 4, 30)), cap=False, lf=il, tremble=jet)
    if jet > 0:
        tx, ty = mx - 30, m['head'][1] + 10
        reach = pop(il, 4, 8)
        ex, ey = lerp(tip[0], tx, reach), lerp(tip[1], ty, reach)
        for wdt, col in ((70 * jet + 14, INK), (70 * jet, KET), (22 * jet, KET_L)):
            ctx.new_path(); ctx.move_to(*tip)
            ctx.curve_to(lerp(tip[0], ex, 0.35), tip[1] - 160 * reach + 10 * math.sin(il * 1.7), lerp(tip[0], ex, 0.7), ey - 120 * reach, ex, ey)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND); setc(ctx, col); ctx.set_line_width(wdt); ctx.stroke()
        for k in range(8):                                             # flying droplets
            u = ((il * 0.13 + k * 0.137) % 1)
            ellipse(ctx, lerp(tip[0], ex, u), lerp(tip[1], ey, u) - 200 * u * (1 - u) + 60 * math.sin(k * 3), 14, 11); fl(ctx, KET, 3)
    if hit > 0:                                                        # Mom covered
        splats(ctx, m['head'][0], m['head'][1], m['R'] * 1.1, 11, 9, hit)
        splats(ctx, m['head'][0], m['head'][1] + m['R'] * 1.9, m['R'] * 1.1, 12, 6, hit)
        if il > 20:
            for k in range(3):
                y_ = m['head'][1] + m['R'] * 0.9 + ((il * 4 + 50 * k) % 160)
                ellipse(ctx, m['head'][0] - 60 + 60 * k, y_, 8, 12); fl(ctx, KET, 3)
    if il >= 34:                                                       # dog runs in and licks the floor puddle
        gx = lerp(2050, 1520, eout(pop(il, 34, 46)))
        ellipse(ctx, 1560, FLOOR + 30, 120, 22); fl(ctx, KET, 4)
        dog(ctx, gx, FLOOR + 60, 0.42, -1, il)
    ctx.restore()
    if il < 30:
        label(ctx, "*SPLOOOORT!!*", 540, 560, 132, KET, 0.04 * math.sin(il * 0.7), pop(il, 4, 7))
    else:
        label2(ctx, "\"...thanks,", "honey.\"", WHITE, pop(il, 36, 40), 116, col2=KET_L, y=1440)
        if il > 48:
            label(ctx, "*lick lick*", 540, 560, 96, GOLD, -0.04, pop(il, 48, 51))


def got_it(ctx, f, il):
    # il 0..38: splattered Dad, flat empty bottle, thumbs up "...GOT IT." ; kid's fries get ONE dollop *plip*
    ctx.save(); cam(ctx, 940, 1280, 1.16, 0, shake_at(il, [20], 4, 4), f)
    kitchen(ctx, il, pic_tilt=0.42, mess=1)
    kid_at(ctx, il, eye='happy', mouth='grin', p=P(eye='happy', mouth='grin', lsh=40, lel=-120, rsh=30, rel=-130))
    d = stand(ctx, DAD_R, DADX + 20, KDAD, P(eye='closed', mouth='grin', lsh=30, lel=-20, rsh=150, rel=-80, torso=-2))
    splats(ctx, d['head'][0], d['head'][1], d['R'] * 0.9, 21, 6)
    drop = pop(il, 8, 20)
    table(ctx, eout(pop(il, 20, 26)), il, mess=1)
    hx_, hy_ = d['front']
    ellipse(ctx, hx_, hy_ - 30, 16, 34); fl(ctx, DAD_R['skin'], 4)             # thumb
    if 8 <= il < 20:
        ellipse(ctx, PLATE + 8, lerp(900, TY - 50, drop * drop), 14, 18); fl(ctx, KET, 3)
    ctx.restore()
    label2(ctx, "\"...GOT", "IT.\"", WHITE, pop(il, 2, 6), 124, col2=GOLD, y=1440)
    if il >= 20:
        label(ctx, "*plip*", 540, 600, 96, KET, 0.05, pop(il, 20, 23))


def s4(ctx, f):
    lf = f - 330
    if lf < 42:
        peel_macro(ctx, f, lf)
    elif lf < 102:
        blast(ctx, f, lf - 42)
    else:
        got_it(ctx, f, lf - 102)


# ------------------------------------------------------------------ shot 5: twist
def plain(ctx, f, il):
    # il 0..90: kid pushes the plate away "Actually... I like them PLAIN." -> 50 Dad + Mom (both red) twitch "...PLAIN?!"
    ctx.save(); cam(ctx, 1140, 1250, lerp(0.93, 0.98, eio(pop(il, 46, 70))), 0, shake_at(il, [50], 6, 8), f)
    kitchen(ctx, il, pic_tilt=0.42, mess=1)
    m = stand(ctx, MOM, 1580, KMOM, P(eye='glare' if il > 50 else 'flat', mouth='flat', lsh=20, lel=-20, rsh=30, rel=-20), f_=-1)
    splats(ctx, m['head'][0], m['head'][1], m['R'] * 1.1, 11, 9)
    splats(ctx, m['head'][0], m['head'][1] + m['R'] * 1.9, m['R'] * 1.1, 12, 6)
    push = eio(pop(il, 14, 24))
    kid_at(ctx, il, p=P(eye='happy', mouth='smile', lsh=-80, lel=-10, rsh=-90 * push, rel=-10, head=-8))
    d = stand(ctx, DAD_R, DADX + 20, KDAD, P(eye='shock' if il < 50 else 'glare', mouth='flat' if il < 50 else 'scream', lsh=20, lel=-20, rsh=10, rel=-20))
    splats(ctx, d['head'][0], d['head'][1], d['R'] * 0.9, 21, 6)
    table(ctx, 0, il, plate=False, mess=1)
    fries(ctx, lerp(PLATE + 150, PLATE - 40, push), TY - 6, 0.9, 1.0, il)
    if il > 50:
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.9, il, 1.1)
        twitch(ctx, m['head'][0] - m['R'] * 0.9, m['head'][1] - m['R'] * 0.9, il + 1, 1.0)
    ctx.restore()
    card(ctx, 'p2', il, 0)
    if il < 50:
        label2(ctx, "\"Actually... I like", "them PLAIN.\"", WHITE, pop(il, 6, 10), 100, col2=GREEN, y=1440)
    else:
        label(ctx, "\"...PLAIN?!\"", 540, 1450, 140, RED, -0.04, pop(il, 50, 53))


def jar_time(ctx, f, il):
    # il 0..70: Mom hands Dad a pickle jar "Honey... can you open THIS?" -> 40 Dad strains on the lid
    ctx.save(); cam(ctx, 1000, 1270, 1.16 + 0.06 * eio(pop(il, 40, 70)), 0, shake_at(il, list(range(42, 70, 6)), 3, 4), f)
    kitchen(ctx, il, pic_tilt=0.42, mess=1)
    m = stand(ctx, MOM, 1250, KMOM, P(eye='smug', mouth='smile', lsh=20, lel=-20, rsh=-80 if il < 30 else 20, rel=-10), f_=-1)
    splats(ctx, m['head'][0], m['head'][1], m['R'] * 1.1, 11, 9)
    if il < 40:
        d = stand(ctx, DAD_R, DADX + 20, KDAD, P(eye='shock', mouth='flat', lsh=20, lel=-20, rsh=60, rel=-50))
        splats(ctx, d['head'][0], d['head'][1], d['R'] * 0.9, 21, 6)
        table(ctx, 0, il, plate=False, mess=1)
        jx = lerp(m['front'][0], d['front'][0] + 40, eio(pop(il, 22, 34)))
        jar(ctx, jx, m['front'][1] - 20, 0.85)
        if il > 30:
            twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.9, il, 1.1)
    else:
        d = stand(ctx, DAD_R, DADX + 20, KDAD, P(eye='closed', mouth='grin', torso=4, lsh=120, lel=-90, rsh=110, rel=-80, head=4, rot=1.5 * math.sin(il * 2)))
        splats(ctx, d['head'][0], d['head'][1], d['R'] * 0.9, 21, 6)
        table(ctx, 0, il, plate=False, mess=1)
        bx = (d['front'][0] + d['back'][0]) / 2 + 10; by = (d['front'][1] + d['back'][1]) / 2
        jar(ctx, bx, by, 0.85, 0.08 * math.sin(il * 2.5))
        sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.6, il, 1.0)
    ctx.restore()
    if il < 40:
        label2(ctx, "\"Honey... can you", "open THIS?\"", WHITE, pop(il, 4, 8), 104, col2=GREEN, y=1440)
    else:
        label(ctx, "\"HNNNNGH!!\"", 540, 1450, 130, RED, -0.03, pop(il, 42, 45))


def s5(ctx, f):
    lf = f - 470
    if lf < 90:
        plain(ctx, f, lf)
    elif lf < 160:
        jar_time(ctx, f, lf - 90)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (54, s2), (240, s3), (330, s4), (470, s5)]
CUTS = (54, 120, 170, 240, 290, 330, 372, 432, 470, 560, 630)


def render(f):
    import sketch
    sketch.BOIL[0] = f // 4
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
    sketch.paper(s)
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/v{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/ketchup_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
