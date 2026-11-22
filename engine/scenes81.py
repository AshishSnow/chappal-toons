"""'Dad vs the fitted sheet' - original, general-audience comedy short, 22s.
Hook:   bedroom medium shot: Dad red-faced, leaning over the bed corner, dragging the LAST corner of a fitted sheet "ONE... MORE... CORNER!!"
        Caption "DAD vs THE FITTED SHEET:"
Beat 1: *SNAP!* it's on, "GOT IT!!" arms up -> *PING!* the far corner pops, *PING!* *PING!* the whole sheet springs off -> "...WHAT?!"
Beat 2: speed montage, Dad dashing corner to corner while they pop behind him "STAY. DOWN!!" -> the sheet swallows him
Beat 3: Dad as a sheet ghost staggering around, *BONK!* into the wardrobe "I'm... WINNING!" -> kid + dog at the door "Mom! Dad's a GHOST again!"
Turn:   Mom walks in with tea, ONE flick *FWOOMP!* -> sheet flies onto the bed, SNAP SNAP SNAP SNAP *DING!* -> Dad ECU "...HOW?!" -> "Practice, honey."
Twist:  "PLOT TWIST: THE KID FOUND A TRAMPOLINE." kid + dog dive on the bed *BOING!* -> all 4 corners PING off, the sheet lands on Dad (ghost again)
        Mom: "...YOUR turn, honey." -> loop to the strain hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes65 import dog, mug
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
WOOD = hx('c9874e'); SHEET = hx('8fd8ff'); SHEET_D = hx('5fb8ef'); MATT = hx('fff4dc')
DAD = dict(doodle.DAD, shirt=hx('ffb347'), pants=hx('3d5a9e'))
MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'), pants=hx('2f4a8a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('7ed36b'), pants=hx('3d7bff'), shoes=hx('ff4d5e'))
N = 660
FLOOR = 1560
GND = 1590                                   # where people stand (in front of the bed)
KDAD, KMOM, KKID = 1.1, 1.02, 0.86
BL, BR, FL_, FR = (320, 1220), (920, 1220), (240, 1340), (1000, 1340)   # mattress top corners
CEN = (620, 1280)
MTH = 72                                     # mattress thickness
DADX = 1090

CAPS = {'p1': [[("DAD vs THE ", OUT), ("FITTED SHEET:", BLUE)]],
        'p2': [[("PLOT TWIST:", RED)], [("THE KID FOUND A ", OUT), ("TRAMPOLINE!", GREEN)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ set
def window(ctx, lf):
    x, y, w, h = 440, 520, 360, 300
    rect_r(ctx, x, y, w, h, 16); fl(ctx, hx('9fdcff'), 8)
    ctx.save(); rect_r(ctx, x, y, w, h, 16); ctx.clip()
    ellipse(ctx, x + 290, y + 70, 42, 42); fl(ctx, hx('ffe35a'), 4)
    for i, (cx_, cy_) in enumerate(((x + 90 + 10 * math.sin(lf * 0.03), y + 110), (x + 220 + 8 * math.sin(lf * 0.03 + 2), y + 200))):
        for dx, r in ((-36, 26), (0, 36), (36, 26)):
            ellipse(ctx, cx_ + dx, cy_, r, r * 0.8); setc(ctx, WHITE); ctx.fill()
    ctx.restore()
    ctx.move_to(x + w / 2, y); ctx.line_to(x + w / 2, y + h); ctx.move_to(x, y + h / 2); ctx.line_to(x + w, y + h / 2); ink(ctx, 6); ctx.stroke()
    rect_r(ctx, x - 24, y + h - 6, w + 48, 24, 8); fl(ctx, WHITE, 5)
    for sx, d in ((x - 50, -1), (x + w - 10, 1)):
        poly(ctx, [(sx, y - 30), (sx + 60, y - 30), (sx + 60 + d * 12, y + h + 40), (sx - 10 + d * 6, y + h + 40)]); fl(ctx, hx('ffb3cf'), 6)
    rect_r(ctx, x - 80, y - 44, w + 160, 20, 8); fl(ctx, hx('a0603a'), 5)


def picture(ctx, x, y, tilt=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(tilt)
    ctx.move_to(0, -100); ctx.line_to(-50, -70); ctx.move_to(0, -100); ctx.line_to(50, -70); ink(ctx, 4); ctx.stroke()
    rect_r(ctx, -80, -70, 160, 130, 10); fl(ctx, hx('ffc93c'), 7)
    rect_r(ctx, -62, -52, 124, 94, 6); fl(ctx, hx('dff4ff'), 4)
    poly(ctx, [(-50, 34), (-14, -20), (16, 34)]); fl(ctx, hx('7ed36b'), 3)
    poly(ctx, [(0, 34), (30, -4), (54, 34)]); fl(ctx, hx('5fb86b'), 3)
    ellipse(ctx, 34, -28, 12, 12); fl(ctx, hx('ff8a1f'), 3)
    ctx.restore()


def wardrobe(ctx, tilt=0.0):
    ctx.save(); ctx.translate(1420, FLOOR + 10); ctx.rotate(tilt); ctx.translate(-1420, -FLOOR - 10)
    rect_r(ctx, 1270, 880, 300, 690, 18); fl(ctx, hx('d99a62'), 8)
    rect_r(ctx, 1290, 905, 125, 640, 10); fl(ctx, hx('e8b07a'), 5)
    rect_r(ctx, 1425, 905, 125, 640, 10); fl(ctx, hx('e8b07a'), 5)
    for kx in (1400, 1440):
        ellipse(ctx, kx, 1220, 10, 10); fl(ctx, GOLD, 3)
    rect_r(ctx, 1250, 860, 340, 32, 10); fl(ctx, hx('b97a48'), 6)
    # box + teddy on top
    rect_r(ctx, 1300, 780, 130, 82, 8); fl(ctx, hx('ff9e5c'), 5)
    ellipse(ctx, 1500, 820, 40, 40); fl(ctx, hx('c98a5a'), 5)
    for ex in (-26, 26):
        ellipse(ctx, 1500 + ex, 786, 14, 14); fl(ctx, hx('c98a5a'), 4)
    for ex in (-12, 12):
        ellipse(ctx, 1500 + ex, 815, 4, 5); setc(ctx, INK); ctx.fill()
    ctx.restore()


def door(ctx):
    rect_r(ctx, 1680, 840, 270, 730, 10); fl(ctx, hx('fff0d0'), 8)          # hallway glimpse
    rect_r(ctx, 1700, 860, 230, 700, 6); setc(ctx, hx('ffe2a8')); ctx.fill()
    poly(ctx, [(1930, 860), (2020, 820), (2020, 1600), (1930, 1560)]); fl(ctx, hx('ffffff'), 6)   # open door leaf
    ellipse(ctx, 1995, 1220, 10, 10); fl(ctx, GOLD, 3)


def nightstand(ctx, lf):
    rect_r(ctx, 40, 1360, 170, 210, 12); fl(ctx, hx('ff9ec4'), 7)
    rect_r(ctx, 58, 1400, 134, 64, 8); fl(ctx, hx('ffc1da'), 4)
    ellipse(ctx, 125, 1432, 9, 9); fl(ctx, GOLD, 3)
    ctx.move_to(100, 1360); ctx.line_to(100, 1250); ink(ctx, 7); ctx.stroke()          # lamp
    poly(ctx, [(50, 1260), (150, 1260), (128, 1180), (72, 1180)]); fl(ctx, hx('fff27a'), 6)
    ellipse(ctx, 100, 1360, 34, 8); fl(ctx, hx('a0603a'), 4)
    ellipse(ctx, 170, 1330, 30, 30); fl(ctx, hx('7fe3ff'), 5)                        # little clock
    ctx.move_to(170, 1330); ctx.line_to(170, 1312); ctx.move_to(170, 1330); ctx.line_to(184, 1334); ink(ctx, 4); ctx.stroke()


def room(ctx, lf, ward_tilt=0.0, pic_tilt=0.0):
    wall = hx('d9ccff')
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, wall); ctx.fill()
    rnd = random.Random(81)
    for k in range(150):
        sx, sy = rnd.uniform(-400, 2500), rnd.uniform(-300, FLOOR - 140)
        sparkle(ctx, sx, sy, 9, dark(wall, 0.9))
    ctx.rectangle(-3000, FLOOR - 110, 9000, 110); setc(ctx, hx('c3b2f5')); ctx.fill()
    ctx.move_to(-3000, FLOOR - 110); ctx.line_to(6000, FLOOR - 110); ink(ctx, 5); ctx.stroke()
    window(ctx, lf)
    picture(ctx, 1120, 760, pic_tilt + 0.03 * math.sin(lf * 0.05))
    # garland of little stars over the bed
    ctx.move_to(200, 420); ctx.curve_to(450, 500, 800, 500, 1040, 420); ink(ctx, 4); ctx.stroke()
    for i in range(8):
        t = (i + 0.5) / 8
        px = 200 + 840 * t; py = 420 + 80 * 4 * t * (1 - t) * 0.75 + 16
        sparkle(ctx, px, py, 22, (GOLD, PINK, CYAN, GREEN)[i % 4])
    # floor
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('d8a06a')); ctx.fill()
    for k in range(-10, 40):
        ctx.move_to(k * 150, FLOOR); ctx.line_to(k * 150 - 140, FLOOR + 600)
    setc(ctx, hx('c48b55')); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-3000, FLOOR); ctx.line_to(6000, FLOOR); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 700, FLOOR + 150, 560, 95); fl(ctx, hx('7fe3ff'), 6)
    ellipse(ctx, 700, FLOOR + 150, 470, 72); setc(ctx, hx('b8f0ff')); ctx.fill()
    wardrobe(ctx, ward_tilt)
    door(ctx)
    nightstand(ctx, lf)
    # plant between wardrobe and door
    px = 1625
    poly(ctx, [(px - 45, FLOOR - 90), (px + 45, FLOOR - 90), (px + 34, FLOOR + 20), (px - 34, FLOOR + 20)]); fl(ctx, hx('ff8a5c'), 6)
    for a in (-0.6, -0.2, 0.2, 0.6):
        ellipse(ctx, px + 60 * math.sin(a), FLOOR - 170 - 30 * math.cos(a), 24, 70, a); fl(ctx, GREEN, 5)
    # pet bed bottom-left
    ellipse(ctx, -120, FLOOR + 70, 130, 44); fl(ctx, hx('ff6f86'), 6)
    ellipse(ctx, -120, FLOOR + 56, 96, 26); fl(ctx, hx('ffc1da'), 4)


def bed_back(ctx):
    """headboard + frame + bare mattress (drawn before the sheet)"""
    ctx.new_path(); ctx.move_to(290, 1230); ctx.line_to(290, 1020); ctx.curve_to(290, 930, 950, 930, 950, 1020); ctx.line_to(950, 1230); ctx.close_path()
    fl(ctx, hx('ff9e5c'), 8)
    ctx.new_path(); ctx.move_to(330, 1220); ctx.line_to(330, 1040); ctx.curve_to(330, 980, 910, 980, 910, 1040); ctx.line_to(910, 1220); ctx.close_path()
    fl(ctx, hx('ffc28a'), 4)
    for hx_ in (470, 620, 770):
        sparkle(ctx, hx_, 1060, 20, hx('fff27a'))
    # frame + legs
    for lx in (250, 960):
        rect_r(ctx, lx, FL_[1] + MTH, 34, FLOOR - FL_[1] - MTH + 10, 8); fl(ctx, hx('a0603a'), 6)
    rect_r(ctx, 220, FL_[1] + MTH - 6, 800, 50, 10); fl(ctx, hx('ff9e5c'), 7)
    # mattress front face + top
    rect_r(ctx, FL_[0], FL_[1] - 6, FR[0] - FL_[0], MTH + 6, 14); fl(ctx, MATT, 7)
    poly(ctx, [BL, BR, FR, FL_]); fl(ctx, MATT, 7)
    ctx.save(); poly(ctx, [BL, BR, FR, FL_]); ctx.clip()
    for i in range(-6, 14):
        ctx.move_to(240 + i * 70, 1220); ctx.line_to(240 + i * 70 + 120, 1340)
        ctx.move_to(240 + i * 70 + 120, 1220); ctx.line_to(240 + i * 70, 1340)
    setc(ctx, hx('eadcbc')); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def pillows(ctx, dy=0.0):
    for px, c in ((450, hx('ffffff')), (790, hx('ffe0ef'))):
        ctx.new_path(); ctx.move_to(px - 120, 1210 + dy); ctx.curve_to(px - 130, 1150 + dy, px + 130, 1150 + dy, px + 120, 1210 + dy)
        ctx.curve_to(px + 110, 1250 + dy, px - 110, 1250 + dy, px - 120, 1210 + dy); fl(ctx, c, 6)


def _lp(a, b, t):
    return (lerp(a[0], b[0], t), lerp(a[1], b[1], t))


def sheet(ctx, h, lf, pull=None, flap=True):
    """fitted sheet on the mattress; h = hook amount (0 popped .. 1 on) for [BL, BR, FR, FL]; pull = override FR point"""
    cs = [BL, BR, FR, FL_]
    pts = []
    for i, c in enumerate(cs):
        hh = clamp(h[i])
        q = _lp(CEN, c, 0.55 + 0.45 * hh)
        if hh < 1:
            q = (q[0] + 6 * math.sin(lf * 0.9 + i), q[1] + 4 * math.cos(lf * 0.8 + i))
        pts.append(q)
    if pull is not None:
        pts[2] = pull
    # front flap (sheet folded down the mattress front)
    if flap:
        hl, hr = clamp(h[3]), clamp(h[2]) if pull is None else 0.5
        if hl + hr > 0.05:
            ctx.new_path(); ctx.move_to(*pts[3]); ctx.line_to(*pts[2])
            ctx.line_to(pts[2][0] - 6, pts[2][1] + MTH * hr); ctx.line_to(pts[3][0] + 6, pts[3][1] + MTH * hl); ctx.close_path()
            fl(ctx, SHEET_D, 6)
    ctx.new_path(); ctx.move_to(*pts[0])
    for i in range(4):
        a, b = pts[i], pts[(i + 1) % 4]
        m = _lp(a, b, 0.5)
        sag = (2 - clamp(h[i]) - clamp(h[(i + 1) % 4])) * 0.12
        cpt = _lp(m, CEN, sag)
        ctx.curve_to(lerp(a[0], cpt[0], 0.66), lerp(a[1], cpt[1], 0.66), lerp(b[0], cpt[0], 0.66), lerp(b[1], cpt[1], 0.66), *b)
    ctx.close_path()
    fl(ctx, SHEET, 7)
    # polka dots
    ctx.save(); ctx.new_path(); ctx.move_to(*pts[0])
    for i in range(4):
        ctx.line_to(*pts[(i + 1) % 4])
    ctx.close_path(); ctx.clip()
    for i in range(-2, 12):
        for j in range(0, 5):
            ellipse(ctx, 240 + i * 75 + (j % 2) * 36, 1214 + j * 32, 9, 6); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()
    ctx.restore()
    # popped corners curl up
    for i, q in enumerate(pts):
        if clamp(h[i]) < 0.5 and not (pull is not None and i == 2):
            ellipse(ctx, q[0], q[1] - 10, 30, 18, 0.4 * (1 if i % 2 else -1)); fl(ctx, SHEET_D, 5)
    return pts


def cloth(ctx, x, y, w, hgt, lf, rot=0.0):
    """free-flying sheet"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.new_path(); ctx.move_to(-w / 2, -hgt / 2)
    for i in range(1, 5):
        xx = -w / 2 + w * i / 4
        ctx.curve_to(xx - w / 6, -hgt / 2 - 30 * math.sin(lf * 0.7 + i), xx - w / 12, -hgt / 2 + 30 * math.sin(lf * 0.7 + i), xx, -hgt / 2)
    ctx.curve_to(w / 2 + 20, -hgt / 6, w / 2 - 20, hgt / 6, w / 2, hgt / 2)
    for i in range(3, -1, -1):
        xx = -w / 2 + w * i / 4
        ctx.curve_to(xx + w / 6, hgt / 2 + 26 * math.sin(lf * 0.8 + i), xx + w / 12, hgt / 2 - 26 * math.sin(lf * 0.8 + i), xx, hgt / 2)
    ctx.curve_to(-w / 2 - 20, hgt / 6, -w / 2 + 20, -hgt / 6, -w / 2, -hgt / 2); ctx.close_path()
    fl(ctx, SHEET, 7)
    ctx.save(); ctx.clip()
    for i in range(-6, 7):
        for j in range(-3, 4):
            ellipse(ctx, i * 60 + (j % 2) * 30, j * 40, 9, 6); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()
    ctx.restore()
    ctx.restore()


def ghost(ctx, x, ground, k, lf, tilt=0.0, eye='normal', arms=0.0):
    """Dad stuck under the sheet: wavy dome, eye holes, shoes poking out"""
    s = k
    ctx.save(); ctx.translate(x, ground); ctx.rotate(tilt)
    for dx in (-44, 44):                                                # shoes
        ellipse(ctx, dx * s + 14 * s, -10 * s, 40 * s, 20 * s); fl(ctx, DAD['shoes'], 5)
    hw, ht = 150 * s, 470 * s
    ctx.new_path(); ctx.move_to(-hw, -28 * s)
    ctx.curve_to(-hw - 10 * s, -ht * 0.5, -hw * 0.9, -ht, 0, -ht)
    ctx.curve_to(hw * 0.9, -ht, hw + 10 * s, -ht * 0.5, hw, -28 * s)
    for i in range(6):
        xx = hw - (i + 1) * 2 * hw / 6
        ctx.curve_to(xx + hw / 4, -28 * s + 26 * s * math.sin(lf * 0.6 + i), xx + hw / 8, -28 * s - 10 * s, xx, -28 * s)
    ctx.close_path(); fl(ctx, SHEET, 7)
    ctx.save(); ctx.clip()
    for i in range(-4, 5):
        for j in range(0, 10):
            ellipse(ctx, i * 60 + (j % 2) * 30, -40 * s - j * 46 * s, 9, 6); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()
    ctx.restore()
    for sg in (-1, 1):                                                  # flailing arm bumps
        a = arms * math.sin(lf * 0.5 + sg)
        ellipse(ctx, sg * (hw + 10 * s), -ht * 0.5 - 60 * s * a, 34 * s, 26 * s, sg * 0.5); fl(ctx, SHEET, 6)
    for ex in (-46, 46):                                                # eye holes
        ex *= s
        if eye == 'closed':
            ink(ctx, 6); ctx.new_path(); ctx.arc(ex, -ht * 0.72, 18 * s, 0.2, math.pi - 0.2); ctx.stroke()
        else:
            ellipse(ctx, ex, -ht * 0.72, 26 * s, 34 * s); setc(ctx, hx('2a2440')); ctx.fill()
            ellipse(ctx, ex, -ht * 0.72 + 4 * s, 11 * s, 13 * s); setc(ctx, WHITE); ctx.fill()
            ellipse(ctx, ex - 4 * s, -ht * 0.72, 4 * s, 4 * s); setc(ctx, INK); ctx.fill()
    ctx.restore()
    return (x, ground - 470 * s)


def bed(ctx, h, lf, pull=None, bare=False):
    bed_back(ctx)
    pts = None
    if not bare:
        pts = sheet(ctx, h, lf, pull)
    pillows(ctx)
    return pts


# ------------------------------------------------------------------ people
def strain_dad(ctx, lf, x=DADX, r=1.0):
    """leaning over the bed corner, pulling"""
    w = math.sin(lf * 1.3)
    p = P(eye='glare', mouth='scream' if r > 0.5 else 'flat', torso=34 + 4 * w * r, head=-14, lsh=74 + 5 * w * r, lel=8, rsh=66 + 5 * w * r, rel=10,
          lhip=-14, lkn=6, rhip=14, rkn=-6)
    return draw(ctx, x + 3 * w * r, GND - 186 * KDAD, KDAD, -1, DAD, p)


def mom_stand(ctx, x, lf, p=None, cup=True, f_=-1):
    p = p or P(eye='smug', mouth='smile', lsh=40, lel=-120, rsh=10, rel=-20)
    m = draw(ctx, x, GND - 186 * KMOM, KMOM, f_, MOM, p)
    if cup:
        mug(ctx, m['front'][0] + f_ * 10, m['front'][1] - 26, 0.6, lf)
    return m


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf, z=None):
    z = z or 1.15 + 0.04 * eio(pop(lf, 0, 54))
    ctx.save(); cam(ctx, 820, 1250, z, 0, 3, f)
    ctx.push_group(); hand = strain_dad(ctx, lf)['front']; ctx.pop_group()
    room(ctx, lf)
    bed_back(ctx)
    sheet(ctx, [1, 1, 0, 1], lf, pull=(hand[0] - 10, hand[1] - 4))
    pillows(ctx)
    d = strain_dad(ctx, lf)
    sweat(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.6, lf, 1.1)
    sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.3, lf + 40, 0.9)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"ONE... MORE...", "CORNER!!\"", WHITE, t, 116, col2=ORANGE, y=1440)


# ------------------------------------------------------------------ shot 2: got it -> pops -> montage
def got_it(ctx, f, il):
    # il 0..66: 0-6 final yank, 6 SNAP on, 8-30 "GOT IT!!" arms up, 30/36/42 corners PING off, 44+ "...WHAT?!"
    z = 1.12 + 0.12 * eio(pop(il, 40, 60))
    sh = shake_at(il, [6, 30, 36, 42], 7, 9)
    ctx.save(); cam(ctx, 800, 1260, z, 0, sh, f)
    room(ctx, il)
    hooks = [1 - pop(il, 30, 33), 1 - pop(il, 36, 39), 1 - pop(il, 42, 45), 1 - pop(il, 46, 49)]
    if il < 6:
        ctx.save(); ctx.push_group(); d = strain_dad(ctx, il); ctx.pop_group(); ctx.restore()
        hand = d['front']
        bed(ctx, hooks, il, pull=_lp((hand[0] - 10, hand[1] - 4), FR, il / 6))
        d = strain_dad(ctx, il)
    else:
        bed(ctx, hooks, il)
        if il < 30:
            p = P(eye='happy', mouth='grin', lsh=160, lel=10, rsh=150, rel=10, torso=-4)
            hop = 30 * abs(math.sin((il - 6) * 0.35)) * (il < 26)
        elif il < 44:
            p = P(eye='normal', mouth='flat', lsh=150, lel=20, rsh=140, rel=10, head=-10 + 8 * math.sin(il))
            hop = 0
        else:
            p = P(eye='shock', mouth='scream', lsh=150, lel=-120, rsh=150, rel=-120, torso=-8)
            hop = 0
        d = draw(ctx, DADX, GND - 186 * KDAD - hop, KDAD, -1, DAD, p)
        if il >= 44:
            twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.9, il, 1.2)
    # flying corner streaks
    for k_, c in ((30, BL), (36, BR), (42, FR), (46, FL_)):
        u = pop(il, k_, k_ + 6)
        if 0 < u < 1:
            for j in range(5):
                a = j * 1.25
                ctx.move_to(c[0] + math.cos(a) * 30, c[1] - 20 + math.sin(a) * 30)
                ctx.line_to(c[0] + math.cos(a) * (40 + 70 * u), c[1] - 20 + math.sin(a) * (40 + 70 * u))
            setc(ctx, YEL); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()
    if il < 30:
        label(ctx, "*SNAP!*", 540, 500, 120, CYAN, -0.05, pop(il, 6, 9))
        label(ctx, "\"GOT IT!!\"", 540, 1450, 150, GREEN, -0.04, pop(il, 9, 12))
    else:
        label(ctx, "*PING! PING! PING!*", 540, 500, 110, GOLD, 0.04, pop(il, 30, 33))
        if il >= 44:
            label(ctx, "\"...WHAT?!\"", 540, 1450, 150, RED, -0.04, pop(il, 46, 49))


def montage(ctx, f, il):
    # il 0..80: Dad zips corner to corner, corners pop behind him; 62+ the sheet flies up and swallows him
    rot = 4 * math.sin(il * 0.12)
    ctx.save(); cam(ctx, 660, 1240, 1.0, rot, shake_at(il, [62], 8, 10), f)
    room(ctx, il)
    ph = il % 16
    side = (il // 16) % 2                       # 0 = right corner, 1 = left corner
    hooks = []
    for i in range(4):
        hooks.append(0.5 + 0.5 * math.sin(il * 0.55 + i * 1.7))
    if il < 62:
        bed(ctx, hooks, il)
        x0, x1 = (DADX, 130) if side == 0 else (130, DADX)
        t = eio(ph / 7) if ph < 7 else 1
        x = lerp(x0, x1, t)
        fdir = -1 if x1 > 600 else 1
        p = P(eye='glare', mouth='scream', torso=30, head=-10, lsh=80, lel=10, rsh=70, rel=10,
              lhip=30 * math.sin(il * 1.6), lkn=-30, rhip=-30 * math.sin(il * 1.6), rkn=-30)
        if ph < 7:                              # speed ghosts
            for g in (0.3, 0.6):
                ctx.push_group(); draw(ctx, lerp(x0, x1, max(0, t - g * 0.4)), GND - 186 * KDAD, KDAD, fdir, DAD, p); ctx.pop_group_to_source(); ctx.paint_with_alpha(0.3)
            for j in range(5):
                yy = GND - 120 - j * 70
                ctx.move_to(x - fdir * 60, yy); ctx.line_to(x - fdir * 260, yy); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(10); ctx.stroke()
        else:
            fdir = 1 if x < 600 else -1
        draw(ctx, x, GND - 186 * KDAD, KDAD, fdir, DAD, p)
    else:
        jl = il - 62
        bed(ctx, [0, 0, 0, 0], il, bare=True)
        u = eio(jl / 10)
        gx = lerp(620, DADX - 60, u); gy = lerp(1180, GND - 230, u) - 200 * math.sin(math.pi * min(1, jl / 10))
        if jl < 10:
            draw(ctx, DADX - 60, GND - 186 * KDAD, KDAD, -1, DAD, P(eye='shock', mouth='scream', lsh=150, lel=-60, rsh=150, rel=-60))
            cloth(ctx, gx, gy, lerp(700, 340, u), lerp(180, 420, u), il, 0.4 * u)
        else:
            ghost(ctx, DADX - 60, GND, KDAD, il, 0.08 * math.sin(il * 0.5), arms=1.0)
    ctx.restore()
    if il < 62:
        label(ctx, "*PING!*", 380 + 300 * side, 500, 100, GOLD, 0.06 * (1 - 2 * side), pop(ph, 8, 10))
        label(ctx, "\"STAY. DOWN!!\"", 540, 1450, 140, ORANGE, -0.03, pop(il, 4, 7))
    else:
        label(ctx, "*FWUMP!*", 540, 500, 120, CYAN, -0.04, pop(il, 62, 65))


def s2(ctx, f):
    lf = f - 54
    if lf < 66:
        got_it(ctx, f, lf)
    else:
        montage(ctx, f, lf - 66)


# ------------------------------------------------------------------ shot 3: sheet ghost
def ghost_walk(ctx, f, il):
    # il 0..140: 0-34 ghost staggers right, 34 *BONK* wardrobe; 70+ kid + dog peek in the doorway
    cx = lerp(900, 1320, eio(pop(il, 60, 80)))
    z = 0.98
    ctx.save(); cam(ctx, cx, 1240, z, 0, shake_at(il, [34], 10, 12), f)
    tilt = 0.06 * eout(pop(il, 34, 38)) * (1 - pop(il, 40, 56))
    room(ctx, il, ward_tilt=tilt, pic_tilt=0.2 * pop(il, 34, 38))
    bed(ctx, [0, 0, 0, 0], il, bare=True)
    if il < 34:
        gx = lerp(DADX - 60, 1250, eio(il / 34)) + 20 * math.sin(il * 0.4)
        gt = 0.12 * math.sin(il * 0.35)
    else:
        bt = pop(il, 34, 50)
        gx = 1250 - 130 * eout(bt) + 10 * math.sin(il * 0.3)
        gt = -0.25 * math.sin(math.pi * bt) * (1 - bt) * 2 + 0.06 * math.sin(il * 0.3)
    if il >= 70:                                # kid + dog in the doorway
        kt = eout(pop(il, 70, 80))
        kx = lerp(2100, 1770, kt)
        dog(ctx, kx - 150, GND + 30, 0.42, -1, il)
        k = draw(ctx, kx, GND - 186 * KKID, KKID, -1, KID, P(eye='shock', mouth='open', lsh=60, lel=-110, rsh=20, rel=-20))
        if il >= 84:
            for j in range(3):
                sparkle(ctx, k['head'][0] + (j - 1) * 50, k['head'][1] - k['R'] * 1.5, 14 + 4 * math.sin(il * 0.5 + j), YEL)
    gh = ghost(ctx, gx, GND, KDAD, il, gt, arms=1.0, eye='closed' if 34 <= il < 46 else 'normal')
    if 34 <= il < 60:
        for j in range(3):                      # dizzy stars
            a = il * 0.3 + j * 2.1
            sparkle(ctx, gh[0] + math.cos(a) * 110, gh[1] - 30 + math.sin(a) * 30, 22, YEL)
    ctx.restore()
    if il < 70:
        if il >= 34:
            label(ctx, "*BONK!*", 540, 500, 140, ORANGE, 0.05, pop(il, 34, 37))
        label(ctx, "\"I'm... WINNING!\"", 540, 1450, 130, WHITE, -0.03, pop(il, 6, 9))
    else:
        label2(ctx, "\"MOM! Dad's a", "GHOST again!\"", WHITE, pop(il, 84, 88), 104, col2=CYAN, y=1440)
        label(ctx, "*WOOF!*", 540, 500, 110, GOLD, -0.05, pop(il, 76, 79))


def s3(ctx, f):
    ghost_walk(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: Mom's one flick
def flick(ctx, f, il):
    # il 0..60: Mom walks to the ghost (0-18), grabs + FLICK (22), sheet arcs to the bed (22-42), corners snap (42-54), DING
    ctx.save(); cam(ctx, 930, 1240, 0.96, 0, shake_at(il, [22, 42], 6, 8), f)
    room(ctx, il)
    hooks = [pop(il, 42, 44), pop(il, 45, 47), pop(il, 48, 50), pop(il, 51, 53)]
    landed = il >= 42
    bed(ctx, hooks, il, bare=not landed)
    gx = 1120
    mx = lerp(1700, 1330, eio(il / 18))
    if il < 22:
        ghost(ctx, gx, GND, KDAD, il, 0.05 * math.sin(il * 0.4), arms=0.6)
        mp = P(eye='smug', mouth='smile', lsh=40, lel=-120, rsh=60 if il > 16 else 10, rel=-20, lhip=20 * math.sin(il * 0.6) * (il < 18), rhip=-20 * math.sin(il * 0.6) * (il < 18))
        mom_stand(ctx, mx, il, mp)
    else:
        spin = pop(il, 22, 40)
        dp = P(eye='shock', mouth='open', lsh=40, lel=-30, rsh=-30, rel=-30, rot=0)
        d = draw(ctx, gx, GND - 186 * KDAD, KDAD, -1 if (il // 3) % 2 == 0 or spin >= 1 else 1, DAD, dp)
        # messy hair tufts
        for j in range(4):
            a = -2.2 + j * 0.45
            ctx.move_to(d['head'][0] + math.cos(a) * d['R'] * 0.95, d['head'][1] + math.sin(a) * d['R'] * 0.95)
            ctx.line_to(d['head'][0] + math.cos(a) * d['R'] * 1.3, d['head'][1] + math.sin(a) * d['R'] * 1.3)
        ink(ctx, 8); ctx.stroke()
        mom_stand(ctx, 1330, il, P(eye='happy', mouth='grin', lsh=40, lel=-120, rsh=150, rel=10))
        if not landed:
            u = eio((il - 22) / 20)
            cx_ = lerp(gx, 620, u); cy_ = lerp(GND - 260, 1260, u) - 420 * math.sin(math.pi * u)
            cloth(ctx, cx_, cy_, lerp(320, 780, u), lerp(400, 120, u), il, -0.6 * (1 - u))
    if il >= 54:
        for j, (sx, sy) in enumerate((BL, BR, FR, FL_)):
            sparkle(ctx, sx, sy - 30, 30 + 8 * math.sin(il * 0.6 + j), YEL)
    ctx.restore()
    if il < 22:
        label(ctx, "*sip*", 540, 500, 100, WHITE, 0.04, pop(il, 2, 5))
    elif il < 42:
        label(ctx, "*FWOOMP!*", 540, 500, 130, CYAN, -0.05, pop(il, 22, 25))
    elif il < 54:
        label(ctx, "*SNAP SNAP SNAP SNAP*", 540, 500, 100, GOLD, 0.03, pop(il, 42, 45))
    else:
        label(ctx, "*DING!*", 540, 500, 140, YEL, -0.04, pop(il, 54, 57))


def how(ctx, f, il):
    # il 0..40: Dad ECU (the one close-up), twitching
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.08 * eio(il / 40), 0, shake_at(il, [0], 6, 8), f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('ffd34f')); ctx.fill()
    rays(ctx, 540, 900, 240, 1500, il * 0.02, col=(1, 1, 1), a=0.35, n=16)
    face(ctx, DAD, P(eye='shock', mouth='scream'), 540, 900, 205, 0.04 * math.sin(il * 2))
    twitch(ctx, 760, 700, il, 1.5)
    ctx.restore()
    label(ctx, "\"...HOW?!\"", 540, 1440, 170, RED, -0.04, pop(il, 2, 5))


def practice(ctx, f, il):
    # il 0..40: Mom smug next to the perfect bed, Dad dizzy behind
    ctx.save(); cam(ctx, 900, 1240, 1.05, 0, 0, f)
    room(ctx, il)
    bed(ctx, [1, 1, 1, 1], il)
    draw(ctx, 1250, GND - 186 * KDAD, KDAD, -1, DAD, P(eye='shock', mouth='open', lsh=20, lel=-20, rsh=-20, rel=-20, head=8 * math.sin(il * 0.4)))
    mom_stand(ctx, 1040, il, P(eye='smug', mouth='smile', lsh=40, lel=-120, rsh=110, rel=-10, head=-6), f_=-1)
    for j in range(3):
        sparkle(ctx, 400 + j * 220, 1190 - 30 * (j % 2), 24 + 6 * math.sin(il * 0.4 + j), WHITE)
    ctx.restore()
    label(ctx, "\"Practice, honey.\"", 540, 1450, 130, PINK, -0.03, pop(il, 2, 5))


def s4(ctx, f):
    lf = f - 340
    if lf < 60:
        flick(ctx, f, lf)
    elif lf < 100:
        how(ctx, f, lf - 60)
    else:
        practice(ctx, f, lf - 100)


# ------------------------------------------------------------------ shot 5: trampoline twist
def tramp(ctx, f, il):
    # il 0..70: kid + dog run in and dive (4-20), land *BOING* (20) -> all 4 corners PING off, sheet rockets up (22-40) and drops on Dad (40-56)
    ctx.save(); cam(ctx, 830, 1230, 0.98, 0, shake_at(il, [20, 56], 9, 10), f)
    room(ctx, il)
    pp = pop(il, 21, 24)
    land = il >= 20
    bed_back(ctx)
    if il < 22:
        sheet(ctx, [1 - pp] * 4, il)
    pillows(ctx, -40 * math.sin(math.pi * pop(il, 20, 30)))
    # dad standing left of the bed, proud -> shock
    dpx = 1180
    if il < 56:
        dp = P(eye='happy' if il < 20 else 'shock', mouth='grin' if il < 20 else 'scream', lsh=150 if il >= 20 else 20, lel=-60 if il >= 20 else -20, rsh=150 if il >= 20 else -20, rel=-60 if il >= 20 else -20)
        draw(ctx, dpx, GND - 186 * KDAD, KDAD, -1, DAD, dp)
    else:
        ghost(ctx, dpx, GND, KDAD, il, 0.04 * math.sin(il * 0.5), arms=0.4)
    # kid + dog
    if il < 20:
        u = eio((il - 2) / 18)
        kx = lerp(1850, 650, u); ky = lerp(GND, 1290, u) - 380 * math.sin(math.pi * u)
        dx_ = lerp(2050, 450, u); dy_ = lerp(GND, 1300, u) - 300 * math.sin(math.pi * u)
        kp = P(eye='happy', mouth='grin', torso=-40 * u, lsh=160, lel=0, rsh=150, rel=0, lhip=40, lkn=-60, rhip=-30, rkn=-40)
    else:
        b = abs(math.sin((il - 20) * math.pi / 14))
        kx, ky = 650, 1290 - 220 * b
        dx_, dy_ = 450, 1300 - 160 * abs(math.sin((il - 24) * math.pi / 14))
        kp = P(eye='happy', mouth='grin', lsh=160 - 30 * b, lel=0, rsh=150 - 30 * b, rel=0, lhip=10 + 30 * b, lkn=-40 * b, rhip=-10 - 30 * b, rkn=-40 * b)
    dog(ctx, dx_, dy_, 0.42, -1, il)
    draw(ctx, kx, ky - 186 * KKID, KKID, -1, KID, kp)
    # the flying sheet
    if 22 <= il < 56:
        if il < 40:
            u = eout((il - 22) / 18); sx_, sy_ = lerp(620, 860, u), lerp(1240, 640, u)
        else:
            u = eio((il - 40) / 16); sx_, sy_ = lerp(860, dpx, u), lerp(640, GND - 260, u)
        cloth(ctx, sx_, sy_, lerp(760, 360, max(0, (il - 40) / 16)), lerp(140, 420, max(0, (il - 34) / 22)), il, 0.3 * math.sin(il * 0.3))
    if 21 <= il < 30:
        for c in (BL, BR, FR, FL_):
            for j in range(4):
                a = j * 1.57 + 0.6
                ctx.move_to(c[0] + math.cos(a) * 30, c[1] - 20 + math.sin(a) * 30); ctx.line_to(c[0] + math.cos(a) * 100, c[1] - 20 + math.sin(a) * 100)
            setc(ctx, YEL); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()
    card(ctx, 'p2', il, 0)
    if il < 20:
        label(ctx, "\"BED TIME!!\"", 540, 1450, 140, GREEN, -0.03, pop(il, 2, 5))
    elif il < 56:
        label(ctx, "*BOING!*", 540, 570, 120, GREEN, -0.04, pop(il, 20, 23))
        label(ctx, "*PING PING PING PING!*", 540, 1450, 100, GOLD, 0.03, pop(il, 22, 25))
    else:
        label(ctx, "*FWUMP!*", 540, 1450, 140, CYAN, -0.04, pop(il, 56, 59))


def your_turn(ctx, f, il):
    # il 0..70: Mom hands it back; kid keeps bouncing on the bare mattress
    ctx.save(); cam(ctx, 980, 1240, 1.0 + 0.04 * eio(il / 70), 0, 0, f)
    room(ctx, il)
    bed(ctx, [0] * 4, il, bare=True)
    b = abs(math.sin(il * math.pi / 14))
    dog(ctx, 450, 1300 - 150 * abs(math.sin((il + 4) * math.pi / 14)), 0.42, -1, il)
    draw(ctx, 680, 1290 - 200 * b - 186 * KKID, KKID, -1, KID, P(eye='happy', mouth='grin', lsh=160 - 30 * b, lel=0, rsh=150 - 30 * b, rel=0, lhip=10 + 30 * b, lkn=-40 * b, rhip=-10 - 30 * b, rkn=-40 * b))
    ghost(ctx, 1140, GND, KDAD, il, 0.05 * math.sin(il * 0.3), eye='closed' if (il // 12) % 3 == 2 else 'normal')
    mom_stand(ctx, 1370, il, P(eye='smug', mouth='smile', lsh=40, lel=-120, rsh=70, rel=-40, head=-6))
    ctx.restore()
    label2(ctx, "\"...YOUR turn,", "honey.\"", PINK, pop(il, 4, 8), 116, col2=WHITE, y=1440)


def s5(ctx, f):
    lf = f - 480
    if lf < 70:
        tramp(ctx, f, lf)
    elif lf < 140:
        your_turn(ctx, f, lf - 70)
    else:
        s1(ctx, f, f - 620)


SHOTS = [(0, s1), (54, s2), (200, s3), (340, s4), (480, s5)]
CUTS = (54, 120, 200, 340, 400, 440, 480, 550, 620)


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
                              "-i", "out/fitted_sheet_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
