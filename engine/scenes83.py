"""'Dad vs the air mattress' - original, general-audience comedy short, 22s.
Hook:   guest-room medium shot: red-faced Dad blowing into a half-flat air mattress, cheeks puffed
        "HUFF... PUFF...!!" + caption "DAD vs THE AIR MATTRESS:"
Beat 1: "No pump? No PROBLEM." *HUUUFF* x3 -> the mattress barely grows, Dad turns blue + dizzy stars
Beat 2: kid strolls in with an electric pump "Dad... we have a PUMP." -> Dad ECU "...NOW you tell me?!"
Beat 3: *VRRRRRR* the pump over-inflates the mattress into a monster that pins Dad to the bookshelf "TOO... MUCH!!"
        *POP!* the cap shoots off -> *PFFFFRRRT* the mattress rockets around the room -> lands flat on Dad "...ow."
Turn:   Mom: "Honey... GRANDMA'S here!"
Twist:  "PLOT TWIST: GRANDMA CAME PREPARED." tiny pouch, one tug *FWOOMP!* a perfect bed pops up, "Night night, dear."
        kid with a stack of flat mattresses: "SLEEPOVER! 5 FRIENDS!!" -> Dad's face -> loop to the hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes65 import dog, mug
from scenes82 import window, picture
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
MAT = hx('5f9dff'); MAT_T = hx('9cc4ff'); MAT_D = hx('3f74d6')
DAD = dict(doodle.DAD, shirt=hx('ff9e3d'), pants=hx('3d5a9e'))
MOM = dict(doodle.MOM_G, shirt=hx('22b45a'), pants=hx('2f4a8a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff5fa8'), pants=hx('3d7bff'), shoes=hx('ffc93c'))
GRAN = dict(doodle.NMOM, hair=hx('dcdce6'), shirt=hx('b98cff'), pants=hx('5a4a8a'), shoes=hx('ff6b8a'), glasses=hx('8a3cff'))
N = 660
FLOOR = 1560
GND = 1590
KDAD, KMOM, KKID, KGRAN = 1.1, 1.02, 0.86, 0.98
MX, ML, MH = 1080, 720, 170           # mattress centre x, length, full height
SHELF = 300                           # bookshelf x (left wall)

CAPS = {'p1': [[("DAD vs ", OUT), ("THE AIR MATTRESS:", BLUE)]],
        'p2': [[("PLOT TWIST:", RED)], [("GRANDMA CAME ", OUT), ("PREPARED.", PURPLE)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def mattress(ctx, cx, base, inf, L=ML, H=MH, lf=0, pillow=False, quilt=False):
    """side view air mattress sitting on base. inf 0 = flat, 1 = full, >1 = over-inflated monster.
    returns valve position (left end)."""
    if inf < 0.08:                                                    # flat crumpled sheet
        w = L
        ctx.new_path(); ctx.move_to(cx - w / 2, base)
        for i in range(13):
            ctx.line_to(cx - w / 2 + w * (i + 0.5) / 12, base - 22 - 10 * ((i * 7) % 3))
        ctx.line_to(cx + w / 2, base); ctx.close_path(); fl(ctx, MAT, 6)
        return (cx - w / 2 + 30, base - 20)
    big = max(0.0, inf - 1)
    w = L * (1 + 0.45 * big)
    h = max(26, H * min(inf, 1) * (1 + 1.9 * big))
    r = min(h / 2 - 2, 46 + 120 * big)
    wob = 16 * (1 - min(1, inf))
    x0 = cx - w / 2
    ctx.new_path()
    ctx.move_to(x0 + r, base - h)
    for i in range(1, 13):                                            # wavy (wrinkly) top while half full
        xx = x0 + r + (w - 2 * r) * i / 12
        ctx.line_to(xx, base - h + wob * math.sin(i * 1.9 + lf * 0.2) + 4 * big * math.sin(i * 1.3 + lf * 0.6))
    ctx.curve_to(x0 + w, base - h, x0 + w, base - h, x0 + w, base - h + r)
    ctx.line_to(x0 + w, base - r * 0.4)
    ctx.curve_to(x0 + w, base, x0 + w, base, x0 + w - r * 0.4, base)
    ctx.line_to(x0 + r * 0.4, base)
    ctx.curve_to(x0, base, x0, base, x0, base - r * 0.4)
    ctx.line_to(x0, base - h + r)
    ctx.curve_to(x0, base - h, x0, base - h, x0 + r, base - h)
    ctx.close_path()
    path = ctx.copy_path()
    fl(ctx, MAT, 7)
    ctx.save(); ctx.append_path(path); ctx.clip()
    ctx.rectangle(x0 - 10, base - h - 30, w + 20, min(h * 0.32, 60 + 80 * big) + 30); setc(ctx, MAT_T); ctx.fill()
    # quilted tufts
    if inf > 0.5:
        nx = int(6 + 3 * big)
        for i in range(nx):
            for j in range(1 + int(big * 2)):
                tx = x0 + w * (i + 0.5) / nx; ty = base - h * (0.45 + 0.25 * j) / (1 + 0.3 * j)
                ellipse(ctx, tx, ty, 9 + 6 * big, 6 + 4 * big); setc(ctx, MAT_D); ctx.fill()
    ctx.move_to(x0, base - 18); ctx.line_to(x0 + w, base - 18); setc(ctx, MAT_D); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()
    ctx.new_path(); ctx.append_path(path); ink(ctx, 7); ctx.stroke()
    if quilt:
        poly(ctx, [(x0 + w * 0.32, base - h - 6), (x0 + w + 8, base - h - 6), (x0 + w + 14, base - h * 0.35), (x0 + w * 0.3, base - h * 0.35)])
        fl(ctx, hx('ffb3d1'), 6)
        for i in range(5):
            sparkle(ctx, x0 + w * (0.38 + 0.12 * i), base - h * 0.68, 13, WHITE)
    if pillow:
        rect_r(ctx, x0 + 26, base - h - 50, 170, 66, 30); fl(ctx, WHITE, 6)
    vx, vy = x0 + 10, base - h * 0.55                                 # valve on the left end
    rect_r(ctx, vx - 26, vy - 16, 30, 32, 8); fl(ctx, hx('ffd34f'), 5)
    return (vx - 24, vy)


def hose(ctx, a, b, sag=40):
    ctx.new_path(); ctx.move_to(*a)
    ctx.curve_to(a[0] - 30, a[1] + sag, b[0] + 10, b[1] + sag, *b)
    ink(ctx, 20); ctx.stroke()
    ctx.new_path(); ctx.move_to(*a); ctx.curve_to(a[0] - 30, a[1] + sag, b[0] + 10, b[1] + sag, *b)
    setc(ctx, hx('7fe3ff')); ctx.set_line_width(11); ctx.stroke()


def pump(ctx, x, base, lf=0, on=False):
    jx = 4 * math.sin(lf * 3.1) if on else 0
    ctx.save(); ctx.translate(x + jx, base)
    rect_r(ctx, -60, -90, 120, 90, 22); fl(ctx, hx('ffc93c'), 6)
    rect_r(ctx, -30, -118, 60, 34, 12); fl(ctx, hx('ff8a1f'), 5)
    ellipse(ctx, 0, -48, 26, 26); fl(ctx, WHITE, 4)
    for k in range(3):
        a = lf * 0.9 * on + k * 2.09
        ctx.move_to(0, -48); ctx.line_to(math.cos(a) * 20, -48 + math.sin(a) * 20)
    ink(ctx, 4); ctx.stroke()
    ellipse(ctx, 40, -70, 7, 7); setc(ctx, GREEN if on else hx('ff3b5c')); ctx.fill()
    ctx.restore()
    if on:
        for k in range(3):
            a = -1.2 + k * 0.4
            ctx.move_to(x + 70 * math.cos(a), base - 60 + 70 * math.sin(a)); ctx.line_to(x + 95 * math.cos(a), base - 60 + 95 * math.sin(a))
        ink(ctx, 5); ctx.stroke()


def puffed(ctx, hd, R, amt, tint, f_=1):
    if amt <= 0:
        return
    cx, cy = hd
    ctx.save()
    for sx in (-1, 1):
        ellipse(ctx, cx + f_ * R * 0.04 + sx * R * (0.32 + 0.12 * amt), cy + R * 0.42, R * (0.2 + 0.12 * amt), R * (0.18 + 0.1 * amt))
        setc(ctx, tuple(DAD['skin'][i] * (1 - 0.45 * amt) + tint[i] * 0.45 * amt for i in range(3))); ctx.fill_preserve(); ink(ctx, 4); ctx.stroke()
    ellipse(ctx, cx + f_ * R * 0.04, cy + R * 0.5, R * 0.09, R * 0.07); fl(ctx, hx('d0505a'), 4)
    ctx.restore()


def dizzy(ctx, x, y, lf, r=70, col=GOLD):
    for k in range(4):
        a = lf * 0.25 + k * math.pi / 2
        sparkle(ctx, x + math.cos(a) * r, y + math.sin(a) * r * 0.35, 18, col)
    ctx.new_path(); ctx.save(); ctx.translate(x, y); ctx.scale(1, 0.35); ctx.arc(0, 0, r, 0, 2 * math.pi); ctx.restore()
    setc(ctx, (1, 1, 1, 0.5)); ctx.set_line_width(3); ctx.stroke()


def suitcase(ctx, x, base):
    rect_r(ctx, x - 70, base - 170, 140, 170, 18); fl(ctx, hx('ff6f86'), 6)
    ctx.move_to(x - 30, base - 170); ctx.line_to(x - 30, base - 220); ctx.line_to(x + 30, base - 220); ctx.line_to(x + 30, base - 170); ink(ctx, 7); ctx.stroke()
    for k in (-1, 1):
        ctx.move_to(x + 36 * k, base - 160); ctx.line_to(x + 36 * k, base - 10)
    setc(ctx, hx('d9334f')); ctx.set_line_width(5); ctx.stroke()
    sparkle(ctx, x, base - 90, 20, WHITE)


# ------------------------------------------------------------------ set: guest room / den
def bookshelf(ctx, x, lf, tilt=0.0):
    ctx.save(); ctx.translate(x, FLOOR); ctx.rotate(tilt); ctx.translate(-x, -FLOOR)
    rect_r(ctx, x - 130, FLOOR - 640, 260, 650, 10); fl(ctx, hx('b8743e'), 7)
    rnd = random.Random(7)
    cols = (RED, BLUE, GOLD, GREEN, PURPLE, PINK, CYAN)
    for s in range(4):
        sy = FLOOR - 620 + s * 155
        rect_r(ctx, x - 112, sy, 224, 135, 4); setc(ctx, hx('8a5530')); ctx.fill()
        bx = x - 104
        while bx < x + 80:
            bw = rnd.uniform(18, 30); bh = rnd.uniform(80, 125)
            rect_r(ctx, bx, sy + 135 - bh, bw, bh, 3); fl(ctx, cols[rnd.randrange(7)], 3)
            bx += bw + 3
    # little plant on top
    poly(ctx, [(x - 40, FLOOR - 640), (x + 40, FLOOR - 640), (x + 30, FLOOR - 700), (x - 30, FLOOR - 700)]); fl(ctx, hx('ff8a5c'), 5)
    for a in (-0.7, 0, 0.7):
        ellipse(ctx, x + 40 * math.sin(a), FLOOR - 740, 16, 40, a); fl(ctx, GREEN, 4)
    ctx.restore()


def lamp(ctx, x):
    rect_r(ctx, x - 50, FLOOR - 200, 100, 200, 10); fl(ctx, hx('ffd34f'), 6)            # side table
    rect_r(ctx, x - 8, FLOOR - 320, 16, 120, 4); fl(ctx, hx('a0603a'), 4)
    poly(ctx, [(x - 60, FLOOR - 320), (x + 60, FLOOR - 320), (x + 38, FLOOR - 400), (x - 38, FLOOR - 400)]); fl(ctx, hx('ff9ec2'), 5)


def room(ctx, lf, pic_tilt=0.0, shelf_tilt=0.0):
    wall = hx('d6f2e6')
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, wall); ctx.fill()
    rnd = random.Random(83)
    for k in range(150):
        sparkle(ctx, rnd.uniform(-400, 2500), rnd.uniform(-300, FLOOR - 140), 10, dark(wall, 0.88))
    ctx.rectangle(-3000, FLOOR - 110, 9000, 110); setc(ctx, hx('b5e3d0')); ctx.fill()
    ctx.move_to(-3000, FLOOR - 110); ctx.line_to(6000, FLOOR - 110); ink(ctx, 5); ctx.stroke()
    window(ctx, lf)
    picture(ctx, 1380, 800, pic_tilt + 0.03 * math.sin(lf * 0.05))
    # bunting
    ctx.move_to(800, 430); ctx.curve_to(1100, 520, 1500, 520, 1900, 430); ink(ctx, 4); ctx.stroke()
    for i in range(8):
        t = (i + 0.5) / 8; bx = 800 + 1100 * t; by = 430 + 90 * 4 * t * (1 - t) * 0.8
        poly(ctx, [(bx - 28, by), (bx + 28, by), (bx, by + 50)]); fl(ctx, (PINK, GOLD, CYAN, GREEN)[i % 4], 4)
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('c9874e')); ctx.fill()
    for k in range(-10, 40):
        ctx.move_to(k * 150, FLOOR); ctx.line_to(k * 150 - 140, FLOOR + 600)
    setc(ctx, hx('b5743e')); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-3000, FLOOR); ctx.line_to(6000, FLOOR); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 1050, FLOOR + 150, 660, 100); fl(ctx, hx('ffb27a'), 6)
    ellipse(ctx, 1050, FLOOR + 150, 560, 76); setc(ctx, hx('ffd2a8')); ctx.fill()
    bookshelf(ctx, SHELF, lf, shelf_tilt)
    lamp(ctx, 1820)
    # dog bed + plant on the right
    ellipse(ctx, 1640, FLOOR + 40, 120, 40); fl(ctx, hx('ff6f86'), 6)
    ellipse(ctx, 1640, FLOOR + 28, 90, 24); fl(ctx, hx('ffc1da'), 4)
    px = 2020
    poly(ctx, [(px - 45, FLOOR - 90), (px + 45, FLOOR - 90), (px + 34, FLOOR + 20), (px - 34, FLOOR + 20)]); fl(ctx, hx('5fb8ef'), 6)
    for a in (-0.6, -0.2, 0.2, 0.6):
        ellipse(ctx, px + 60 * math.sin(a), FLOOR - 170 - 30 * math.cos(a), 24, 70, a); fl(ctx, GREEN, 5)


# ------------------------------------------------------------------ people
def blowing_dad(ctx, x, lf, inf, amt=None, tint=RED, pale=False):
    """Dad bent over the valve, cheeks puffed, hose from mouth to valve"""
    amt = (0.6 + 0.4 * math.sin(lf * 0.5)) if amt is None else amt
    ch = dict(DAD, skin=hx('9ec8ff')) if pale else DAD
    p = P(eye='closed' if not pale else 'shock', mouth='flat', torso=16 + 4 * math.sin(lf * 0.5), head=10,
          lsh=40, lel=-60, rsh=60, rel=-40, lhip=14, lkn=10, rhip=-4, rkn=6)
    d = draw(ctx, x, GND - 186 * KDAD, KDAD, 1, ch, p)
    hd, R = d['head'], d['R']
    if not pale:
        puffed(ctx, hd, R, amt, tint)
    v = mattress(ctx, MX, FLOOR + 30, inf, lf=lf)
    hose(ctx, (hd[0] + R * 0.08, hd[1] + R * 0.52), v, 90)
    return d


def stand(ctx, ch, x, k, p, f_=1):
    return draw(ctx, x, GND - 186 * k, k, f_, ch, p)


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = 1.22 + 0.05 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, 990, 1290, z, 0, 3, f)
    room(ctx, lf)
    inf = 0.42 + 0.05 * math.sin(lf * 0.5)
    d = blowing_dad(ctx, 680, lf, inf)
    sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.6, lf, 1.0)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"HUFF... PUFF...", "...ALMOST!!\"", WHITE, t, 112, col2=ORANGE, y=1440)


# ------------------------------------------------------------------ shot 2: no pump -> dizzy -> kid has a pump -> ECU
def no_pump(ctx, f, il):
    # il 0..96: 0-26 smug "No pump? No PROBLEM.", 26/42/58 *HUUUFF*, mattress barely grows, 74+ blue dizzy "...seeing... STARS..."
    puffs = [26, 42, 58]
    inf = 0.12 + 0.04 * sum(eout(pop(il, k, k + 10)) for k in puffs)
    z = 1.12 + 0.12 * eio(pop(il, 74, 92))
    ctx.save(); cam(ctx, lerp(950, 820, eio(pop(il, 74, 92))), 1300, z, 0, shake_at(il, puffs, 4, 6), f)
    room(ctx, il)
    if il < 26:
        mattress(ctx, MX, FLOOR + 30, 0.0, lf=il)
        hold = P(eye='smug', mouth='smile', lsh=160, lel=-10, rsh=30, rel=-110, torso=-4)
        d = stand(ctx, DAD, 600, KDAD, hold)
    elif il < 74:
        k = max([q for q in puffs if q <= il])
        amt = 1 - eout(pop(il, k + 2, k + 12))
        d = blowing_dad(ctx, 620, il, inf, amt=amt)
    else:
        sway = 10 * math.sin(il * 0.35)
        mattress(ctx, MX, FLOOR + 30, inf, lf=il)
        d = stand(ctx, dict(DAD, skin=hx('a8d0ff')), 620, KDAD, P(eye='shock', mouth='wavy', rot=sway, lsh=30, lel=-20, rsh=-30, rel=-20, head=-sway))
        dizzy(ctx, d['head'][0], d['head'][1] - d['R'] * 1.1, il, 90)
    ctx.restore()
    if il < 26:
        label2(ctx, "\"No pump?", "No PROBLEM.\"", WHITE, pop(il, 2, 6), 116, col2=GOLD, y=1440)
    elif il < 74:
        k = max([q for q in puffs if q <= il])
        label(ctx, "*HUUUFF!*", 540, 540 + 60 * puffs.index(k), 120, CYAN, (-0.05, 0.04, -0.03)[puffs.index(k)], pop(il, k, k + 3))
        label(ctx, "...barely.", 540, 1450, 104, WHITE, -0.03, pop(il, 64, 67))
    else:
        label2(ctx, "\"...seeing...", "STARS...\"", WHITE, pop(il, 76, 80), 112, col2=GOLD, y=1440)


def kid_pump(ctx, f, il):
    # il 0..50: kid strolls in from the right holding a pump "Dad... we have a PUMP."
    ctx.save(); cam(ctx, 1000, 1300, 1.12, 0, 0, f)
    room(ctx, il)
    mattress(ctx, MX, FLOOR + 30, 0.24, lf=il)
    sway = 8 * math.sin(il * 0.3)
    stand(ctx, dict(DAD, skin=hx('c4ddf5')), 620, KDAD, P(eye='shock', mouth='open', rot=sway * 0.5, lsh=20, lel=-20, rsh=-20, rel=-20))
    kx = lerp(1700, 1300, eio(il / 16))
    walk = il < 16
    k = stand(ctx, KID, kx, KKID, P(eye='smug', mouth='smile', lsh=-40, lel=-80, rsh=-60, rel=-70,
                                     lhip=18 * math.sin(il * 0.8) * walk, rhip=-18 * math.sin(il * 0.8) * walk), f_=-1)
    pump(ctx, k['front'][0] - 10, k['front'][1] + 70, il)
    ctx.restore()
    label2(ctx, "\"Dad... we have", "a PUMP.\"", WHITE, pop(il, 4, 8), 112, col2=GOLD, y=1440)


def now_you_tell_me(ctx, f, il):
    # il 0..44: the one big Dad close-up
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.08 * eio(il / 44), 0, shake_at(il, [0], 6, 8), f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('7fe3ff')); ctx.fill()
    rays(ctx, 540, 900, 240, 1500, il * 0.02, col=(1, 1, 1), a=0.35, n=16)
    face(ctx, DAD, P(eye='glare', mouth='scream'), 540, 900, 205, 0.04 * math.sin(il * 2))
    twitch(ctx, 760, 690, il, 1.5)
    ctx.restore()
    label2(ctx, "\"...NOW you", "tell me?!\"", WHITE, pop(il, 2, 5), 124, col2=RED, y=1440)


def s2(ctx, f):
    lf = f - 54
    if lf < 96:
        no_pump(ctx, f, lf)
    elif lf < 146:
        kid_pump(ctx, f, lf - 96)
    else:
        now_you_tell_me(ctx, f, lf - 146)


# ------------------------------------------------------------------ shot 3: pump -> monster -> rocket -> flat on Dad
def monster(ctx, f, il):
    # il 0..62: *VRRRR* mattress swells (0-50) and pins Dad against the bookshelf; 50 "TOO... MUCH...!!"
    u = eio(pop(il, 4, 50))
    inf = lerp(0.24, 2.4, u)
    z = lerp(1.1, 0.82, eio(pop(il, 0, 40)))
    ctx.save(); cam(ctx, lerp(1000, 990, u), lerp(1300, 1190, u), z, 0, shake_at(il, list(range(10, 60, 6)), 4 + 6 * u, 4), f)
    room(ctx, il, pic_tilt=0.25 * u, shelf_tilt=-0.03 * u * (1 + 0.3 * math.sin(il)))
    right = 1480
    w = ML * (1 + 0.45 * max(0, inf - 1))
    cx_ = right - w / 2
    left = right - w
    dx = min(lerp(640, 470, u), left - 40)
    squish = clamp((640 - dx) / 170)
    ctx.save(); ctx.translate(dx, GND); ctx.scale(1 - 0.4 * squish, 1); ctx.translate(-dx, -GND)
    stand(ctx, DAD, dx, KDAD, P(eye='shock', mouth='scream', lsh=160, lel=-20, rsh=150, rel=-30, torso=-6))
    ctx.restore()
    v = mattress(ctx, cx_, FLOOR + 30, inf, lf=il)
    pump(ctx, 1590, FLOOR + 40, il, on=True)
    hose(ctx, (1560, FLOOR - 50), (right - 10, FLOOR - 60), 40)
    ctx.restore()
    label(ctx, "*VRRRRRRRRR!*", 540, 560, 116, GOLD, 0.03 * math.sin(il * 0.6), pop(il, 0, 3))
    if il >= 40:
        label2(ctx, "\"TOO...", "MUCH...!!\"", WHITE, pop(il, 40, 44), 120, col2=RED, y=1440)


def rocket(ctx, f, il):
    # il 0..58: *POP!* (0), mattress rockets around the room deflating (2-44), lands flat on Dad (44) "...ow."
    ctx.save(); cam(ctx, 940, 1200, 0.84, 0, shake_at(il, [0, 16, 30, 44], 10, 8), f)
    room(ctx, il, pic_tilt=0.25 + 0.4 * (il >= 16), shelf_tilt=-0.06 * (il >= 30) * math.exp(-(il - 30) * 0.1))
    path = [(1200, 1300), (1700, 800), (1380, 640), (800, 600), (300, 900), (700, 1200), (800, 1520)]
    t = clamp((il - 2) / 42) * (len(path) - 1)
    i = min(int(t), len(path) - 2); fr = t - i
    px = lerp(path[i][0], path[i + 1][0], fr); py = lerp(path[i][1], path[i + 1][1], fr)
    if il >= 44:
        px, py = 800, FLOOR + 30
    infl = lerp(2.0, 0.1, eio(il / 44))
    # Dad: slid down to the floor (lying) after being released
    if il < 44:
        stand(ctx, DAD, 470, KDAD, P(eye='shock', mouth='scream', lsh=170, lel=-10, rsh=-170, rel=10, rot=-6 * math.sin(il * 0.5)))
    if il < 44:
        ang = math.atan2(path[i + 1][1] - path[i][1], path[i + 1][0] - path[i][0])
        # speed trail + air puffs from the valve
        for k in range(5):
            ellipse(ctx, px - math.cos(ang) * (120 + 70 * k), py - math.sin(ang) * (120 + 70 * k), 40 - 6 * k, 28 - 4 * k)
            setc(ctx, (1, 1, 1, 0.7 - 0.12 * k)); ctx.fill()
        ctx.save(); ctx.translate(px, py); ctx.rotate(ang + math.pi + 0.3 * math.sin(il * 1.7))
        mattress(ctx, 0, 0 + 40, infl, L=ML * 0.9, lf=il)
        ctx.restore()
    else:
        # flat mattress on top of Dad: head pokes out left, shoes out right
        face(ctx, DAD, P(eye='shock', mouth='flat'), px - ML / 2 - 30, FLOOR - 10, 70, -1.2)
        for k in (-1, 1):
            ellipse(ctx, px + ML / 2 + 20, FLOOR + 10 + k * 22, 30, 18); fl(ctx, DAD['shoes'], 5)
        mattress(ctx, px, FLOOR + 30, 0.0, lf=il)
        dizzy(ctx, px - ML / 2 - 30, FLOOR - 110, il, 70)
    ctx.restore()
    if il < 10:
        label(ctx, "*POP!*", 540, 560, 150, RED, -0.05, pop(il, 0, 3))
    elif il < 44:
        label(ctx, "*PFFFFRRRRT!!*", 540, 560, 120, CYAN, 0.05 * math.sin(il * 0.5), pop(il, 10, 13))
        if il >= 16:
            label(ctx, "*BONK!*", 540, 1450, 120, ORANGE, -0.04, pop(il, 16, 19))
    else:
        label(ctx, "\"...ow.\"", 540, 1450, 140, WHITE, -0.03, pop(il, 46, 49))


def s3(ctx, f):
    lf = f - 240
    if lf < 62:
        monster(ctx, f, lf)
    else:
        rocket(ctx, f, lf - 62)


# ------------------------------------------------------------------ shot 4: "Grandma's here!"
def grandma_here(ctx, f, il):
    # il 0..90: Dad under the flat mattress; Mom leans in at 6 "Honey... GRANDMA'S here!"; 50 Dad pops up panicking
    ctx.save(); cam(ctx, 1060, 1290, 1.05, 0, shake_at(il, [50], 6, 8), f)
    room(ctx, il, pic_tilt=0.65)
    mx = lerp(1750, 1360, eio(il / 14))
    stand(ctx, MOM, mx, KMOM, P(eye='normal', mouth='open', lsh=-20, lel=-20, rsh=-110, rel=-40, head=-6,
                               lhip=16 * math.sin(il * 0.7) * (il < 14), rhip=-16 * math.sin(il * 0.7) * (il < 14)), f_=-1)
    if il < 50:
        face(ctx, DAD, P(eye='shock', mouth='flat'), 1010 - ML / 2 - 30, FLOOR - 10, 70, -1.2)
        for k in (-1, 1):
            ellipse(ctx, 1010 + ML / 2 + 20, FLOOR + 10 + k * 22, 30, 18); fl(ctx, DAD['shoes'], 5)
        mattress(ctx, 1010, FLOOR + 30, 0.0, lf=il)
    else:
        mattress(ctx, 900, FLOOR + 30, 0.0, lf=il)
        d = stand(ctx, DAD, 760, KDAD, P(eye='shock', mouth='scream', lsh=150, lel=-60, rsh=150, rel=-60, rot=4 * math.sin(il * 1.5)))
        sweat(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.6, il, 1.2)
    ctx.restore()
    if il < 50:
        label2(ctx, "\"Honey...", "GRANDMA'S here!\"", WHITE, pop(il, 8, 12), 112, col2=PURPLE, y=1440)
    else:
        label(ctx, "\"...ALREADY?!\"", 540, 1450, 140, RED, -0.04, pop(il, 50, 53))


def s4(ctx, f):
    grandma_here(ctx, f, f - 360)


# ------------------------------------------------------------------ shot 5: the twist
def prepared(ctx, f, il):
    # il 0..100: Grandma rolls in with a suitcase (0-16); pulls a tiny pouch + tug (24-34); *FWOOMP!* perfect bed (34)
    #            she lies down (60) "Night night, dear." ; Dad twitch
    ctx.save(); cam(ctx, 1030, 1260, 0.95, 0, shake_at(il, [34], 8, 10), f)
    room(ctx, il, pic_tilt=0.65)
    mattress(ctx, 620, FLOOR + 30, 0.0, lf=il)
    d = stand(ctx, DAD, 590, KDAD, P(eye='shock', mouth='open' if il < 60 else 'flat', lsh=30, lel=-30, rsh=10, rel=-30))
    if il >= 60:
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.9, il, 1.1)
    gx = lerp(1800, 1440, eio(il / 16))
    suitcase(ctx, gx + 150, FLOOR + 30)
    bed_x = 1110
    pop_u = max(0.03, eout(pop(il, 34, 42)))
    if il < 34:
        # tiny pouch on the floor
        rect_r(ctx, bed_x - 30, FLOOR - 10, 60, 40, 12); fl(ctx, MAT, 5)
        ctx.move_to(bed_x + 30, FLOOR + 10); ctx.line_to(lerp(bed_x + 30, gx - 60, 1), FLOOR - 120 + 30 * pop(il, 26, 32))
        ink(ctx, 4); ctx.stroke()
    else:
        sq = 1 + 0.15 * math.sin(pop(il, 34, 50) * math.pi * 3) * (1 - pop(il, 34, 50))
        ctx.save(); ctx.translate(bed_x, FLOOR + 30); ctx.scale(pop_u * sq, pop_u / sq); ctx.translate(-bed_x, -FLOOR - 30)
        mattress(ctx, bed_x, FLOOR + 30, 1.0, lf=il, pillow=True, quilt=il < 60)
        ctx.restore()
        if il < 52:
            for k in range(10):
                a = k * 0.63; r = 80 + 420 * pop(il, 34, 50)
                sparkle(ctx, bed_x + math.cos(a) * r, 1380 + math.sin(a) * r * 0.5, 26, (GOLD, PINK, CYAN)[k % 3])
    if il < 60:
        stand(ctx, GRAN, gx, KGRAN, P(eye='happy', mouth='smile', lsh=-30, lel=-40, rsh=-60 if il < 24 else -100, rel=-30,
                                      lhip=14 * math.sin(il * 0.7) * (il < 16), rhip=-14 * math.sin(il * 0.7) * (il < 16)), f_=-1)
    else:
        # Grandma tucked in under the quilt, sleep mask, zzz
        top = FLOOR + 30 - MH
        face(ctx, GRAN, P(eye='closed', mouth='smile'), bed_x - ML / 2 + 115, top - 70, 96, -0.15)
        poly(ctx, [(bed_x - ML / 2 + 170, top - 6), (bed_x + ML / 2 + 8, top - 6), (bed_x + ML / 2 + 14, top + MH * 0.6), (bed_x - ML / 2 + 160, top + MH * 0.6)])
        fl(ctx, hx('ffb3d1'), 6)
        ctx.new_path(); ctx.move_to(bed_x - 160, top - 6); ctx.curve_to(bed_x, top - 70, bed_x + 200, top - 60, bed_x + ML / 2, top - 6); fl(ctx, hx('ffb3d1'), 6)
        for k in range(3):
            label(ctx, "z", bed_x - ML / 2 + 200 + 50 * k, top - 140 - 60 * k - 10 * math.sin(il * 0.2 + k), 50 + 14 * k, WHITE, 0.2, 1)
    ctx.restore()
    card(ctx, 'p2', il, 0)
    if il < 34:
        label(ctx, "*tug*", 540, 1450, 110, WHITE, -0.03, pop(il, 26, 29))
    elif il < 60:
        label(ctx, "*FWOOMP!*", 540, 1450, 150, PURPLE, -0.04, pop(il, 34, 37))
    else:
        label2(ctx, "\"Night night,", "dear.\"", PINK, pop(il, 62, 66), 112, col2=WHITE, y=1440)


def sleepover(ctx, f, il):
    # il 0..50: kid bursts in with a tower of flat mattresses "SLEEPOVER! 5 FRIENDS!!" -> Dad's jaw drops
    ctx.save(); cam(ctx, 900, 1290, 1.1, 0, shake_at(il, [14], 6, 8), f)
    room(ctx, il, pic_tilt=0.65)
    mattress(ctx, 560, FLOOR + 30, 0.0, lf=il)
    d = stand(ctx, DAD, 620, KDAD, P(eye='shock', mouth='scream' if il > 20 else 'flat', lsh=20, lel=-20, rsh=10, rel=-20, rot=-4 * (il > 20)))
    if il > 20:
        sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.6, il, 1.2)
    kx = lerp(1700, 1130, eout(il / 14))
    k = stand(ctx, KID, kx, KKID, P(eye='happy', mouth='grin', lsh=-160, lel=0, rsh=-160, rel=0,
                                     lhip=20 * math.sin(il * 0.9) * (il < 14), rhip=-20 * math.sin(il * 0.9) * (il < 14)), f_=-1)
    top = k['head'][1] - k['R'] * 1.1
    for j in range(5):                                                 # stack of folded flat mattresses held overhead
        rect_r(ctx, kx - 110 + 6 * math.sin(il * 0.4 + j), top - 46 * (j + 1), 220, 42, 16); fl(ctx, (MAT, hx('ff8a5c'), hx('7ed36b'), PINK, GOLD)[j], 5)
    ctx.restore()
    label2(ctx, "\"DAD! SLEEPOVER!", "5 FRIENDS!!\"", WHITE, pop(il, 4, 8), 112, col2=GREEN, y=1440)


def s5(ctx, f):
    lf = f - 470
    if lf < 100:
        prepared(ctx, f, lf)
    elif lf < 150:
        sleepover(ctx, f, lf - 100)
    else:
        s1(ctx, f, f - 620)


SHOTS = [(0, s1), (54, s2), (240, s3), (360, s4), (470, s5)]
CUTS = (54, 150, 200, 240, 302, 360, 470, 570, 620)


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
                              "-i", "out/air_mattress_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
