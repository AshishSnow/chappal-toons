"""'Dad vs the Christmas tree' - original, general-audience comedy short, 22s.
Hook:   living-room medium shot: red-faced Dad yanking the trunk of a huge tree stuck sideways in the front door
        "COME... IN...!!" + caption "DAD vs THE CHRISTMAS TREE:"
Beat 1: *POP!* the tree shoots in, needles burst, Dad flies onto the sofa *FLOMP*
Beat 2: tree stood up in its stand -> way too tall, the top bends along the ceiling *CREEEAK* *BONK* lamp swings "...TOO TALL."
Beat 3: Dutch-tilt saw montage *ZZZT!* x3 "A LITTLE OFF THE BOTTOM..." -> logs pile up -> the tree is now knee-high "PERFECT!"
Turn:   Mom + kid walk in with a giant gold star, the kid puts it on -> the tiny tree folds to the floor *BOINK*
        Mom: "...honey. It's a BUSH."  ECU: Dad covered in needles, twitching "...it's a TABLE tree."
Twist:  "PLOT TWIST: GRANDMA SENT ANOTHER ONE." *DING-DONG* door opens: an even BIGGER tree with a bow + "LOVE, GRANDMA" tag
        kid "YAAAY!!" / Mom "It's even BIGGER!" / Dad "...of COURSE it is." -> grabs the trunk "HNNNGH!!" -> loop to the hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
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
PINE = hx('2fae5f'); PINE_D = hx('1f8a48'); BARK = hx('8a5a3a'); WOOD = hx('d99a62')
DAD = dict(doodle.DAD, shirt=hx('e8473f'), pants=hx('34477e'))
DAD_R = dict(DAD, skin=hx('f07a6a'))
MOM = dict(doodle.MOM_G, shirt=hx('8a3cff'), pants=hx('2f4a8a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('22b45a'))
N = 660
CEIL = 430            # ceiling line
FLOOR = 1560
GND = 1590
KD, KM, KK = 1.1, 1.02, 0.85
TX = 1040             # tree stand x
DOORX0, DOORX1, DOORTOP = 1560, 1820, 960

CAPS = {'p1': [[("DAD vs ", OUT), ("THE CHRISTMAS TREE:", GREEN)]],
        'p2': [[("PLOT TWIST:", RED)], [("GRANDMA SENT ", OUT), ("ANOTHER ONE.", GREEN)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ the tree
def _tree_local(ctx, h, wsc=1.0, lf=0, deco=0.0, snow=0.0, bow=False):
    """tree in local coords: trunk base at (0,0), tip at (0,-h)."""
    tr = min(110, 0.16 * h)
    ctx.rectangle(-22 * wsc, -tr - 10, 44 * wsc, tr + 10); fl(ctx, BARK, 6)
    tiers = 4 if h > 500 else 3
    body = h - tr
    for i in range(tiers):
        y0 = -tr - body * i / (tiers + 0.6)
        top = y0 - body * 1.6 / (tiers + 0.6)
        w = (0.36 * body / (tiers * 0.55) * (1 - i / (tiers + 1.2))) * wsc
        w = min(w, 330 * wsc + 0.05 * body)
        ctx.new_path(); ctx.move_to(-w, y0)
        for j in range(7):                                       # jaggy hem
            ctx.line_to(-w + 2 * w * (j + 0.5) / 7, y0 + 18)
            ctx.line_to(-w + 2 * w * (j + 1) / 7, y0)
        ctx.line_to(0, max(top, -h)); ctx.close_path(); fl(ctx, PINE if i % 2 == 0 else hx('35b866'), 7)
        ctx.move_to(-w * 0.45, y0 - 30); ctx.line_to(-w * 0.15, (y0 + top) / 2 + 10); setc(ctx, PINE_D); ctx.set_line_width(5); ctx.stroke()
        if snow > 0:
            for j in range(3):
                ellipse(ctx, -w * 0.6 + j * w * 0.6, y0 - 8, w * 0.18, 14); setc(ctx, (1, 1, 1, snow)); ctx.fill()
    if deco > 0:
        cols = (RED, GOLD, CYAN, PINK, PURPLE)
        nb = int(14 * deco) if h > 500 else 5
        for k in range(nb):
            v = (k + 0.5) / nb
            by = -tr - body * 0.92 * v
            ww = (h - tr) * 0.33 * (1 - v) * wsc
            bx = ww * math.sin(k * 2.3)
            on = (lf // 8 + k) % 3 != 0
            ellipse(ctx, bx, by, 14 + 4 * (h > 500), 14 + 4 * (h > 500)); fl(ctx, cols[k % 5] if on else dark(cols[k % 5], 0.7), 3)
    if bow:
        ctx.save(); ctx.translate(0, -h * 0.45); ctx.scale(2.2, 2.2)
        for sg in (-1, 1):
            ctx.new_path(); ctx.move_to(0, 0); ctx.curve_to(sg * 30, -60, sg * 80, -40, sg * 60, 0); ctx.curve_to(sg * 70, 30, sg * 30, 20, 0, 0); fl(ctx, RED, 3)
            poly(ctx, [(0, 4), (sg * 34, 50), (sg * 18, 56), (0, 12)]); fl(ctx, RED, 3)
        ellipse(ctx, 0, 0, 16, 14); fl(ctx, dark(RED, 0.85), 3)
        ctx.restore()


def xtree(ctx, x, base, h, wsc=1.0, ang=0.0, lf=0, deco=0.0, snow=0.0, bow=False, bend=0.0):
    """tree standing at (x, base) rotated by ang. bend: fold the part above the ceiling to the right (0..1)."""
    top = base - h
    if bend <= 0 or top >= CEIL:
        ctx.save(); ctx.translate(x, base); ctx.rotate(ang)
        _tree_local(ctx, h, wsc, lf, deco, snow, bow); ctx.restore()
        return
    yc = CEIL - base                                    # local y of the ceiling (negative)
    ctx.save(); ctx.rectangle(-3000, CEIL, 9000, 6000); ctx.clip()
    ctx.translate(x, base); _tree_local(ctx, h, wsc, lf, deco, snow, bow); ctx.restore()
    ctx.save(); ctx.translate(x, CEIL + 20); ctx.rotate(math.pi / 2 * bend); ctx.translate(0, -yc)
    ctx.rectangle(-3000, -6000, 6000, 6000 + yc); ctx.clip()
    _tree_local(ctx, h, wsc, lf, deco, snow, bow); ctx.restore()


def stand_base(ctx, x, s=1.0):
    rect_r(ctx, x - 90 * s, FLOOR - 50 * s, 180 * s, 70 * s, 16 * s); fl(ctx, RED, 6)
    ctx.rectangle(x - 90 * s, FLOOR - 30 * s, 180 * s, 12 * s); setc(ctx, GOLD); ctx.fill()


def star(ctx, x, y, r, ang=0.0, glow=True):
    if glow:
        ellipse(ctx, x, y, r * 1.6, r * 1.6); setc(ctx, (1, 0.95, 0.5, 0.35)); ctx.fill()
    pts = []
    for k in range(10):
        a = ang - math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    poly(ctx, pts); fl(ctx, GOLD, 6)
    sparkle(ctx, x - r * 0.2, y - r * 0.2, r * 0.3, WHITE)


def needles(ctx, x, y, u, n=26, seed=3, spread=600):
    if u <= 0 or u >= 1:
        return
    rnd = random.Random(seed)
    for k in range(n):
        a = rnd.uniform(0, 2 * math.pi); d = spread * u * rnd.uniform(0.4, 1.1)
        px = x + math.cos(a) * d; py = y + math.sin(a) * d * 0.7 + 300 * u * u
        b = a + 5 * u
        ctx.move_to(px - 14 * math.cos(b), py - 14 * math.sin(b)); ctx.line_to(px + 14 * math.cos(b), py + 14 * math.sin(b))
    setc(ctx, PINE_D + (1 - u * 0.6,)); ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def logs(ctx, x, n):
    """pile of sawn trunk discs on the floor"""
    rnd = random.Random(7)
    for k in range(n):
        row = 0 if k < 4 else 1 if k < 7 else 2
        i = k if row == 0 else k - 4 if row == 1 else k - 7
        cx = x + i * 74 + row * 37; cy = FLOOR + 40 - row * 62
        ellipse(ctx, cx, cy, 38, 34); fl(ctx, WOOD, 5)
        for r in (22, 11):
            ellipse(ctx, cx, cy, r, r * 0.9); setc(ctx, BARK); ctx.set_line_width(3); ctx.stroke()


def saw(ctx, hand, L=300, ang=0.0):
    ctx.save(); ctx.translate(*hand); ctx.rotate(ang)
    poly(ctx, [(10, -26), (L, -14), (L, 22), (10, 30)]); fl(ctx, hx('c8ccd8'), 5)
    ctx.new_path(); ctx.move_to(10, 30)
    for j in range(14):
        ctx.line_to(10 + (L - 10) * (j + 0.5) / 14, 44); ctx.line_to(10 + (L - 10) * (j + 1) / 14, 26)
    ink(ctx, 4); ctx.stroke()
    rect_r(ctx, -50, -36, 70, 72, 20); fl(ctx, ORANGE, 5)
    ctx.restore()


def tag(ctx, x, y, a=0.15):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ctx.move_to(0, -60); ctx.line_to(0, 0); ink(ctx, 4); ctx.stroke()
    rect_r(ctx, -120, 0, 240, 110, 14); fl(ctx, hx('fff4dc'), 5)
    text(ctx, "LOVE,", 0, 44, 40, RED, ow=0, shadow=False)
    text(ctx, "GRANDMA", 0, 90, 40, RED, ow=0, shadow=False)
    ctx.restore()


# ------------------------------------------------------------------ set
def window(ctx, lf):
    x, y, w, h = 170, 640, 360, 320
    rect_r(ctx, x, y, w, h, 16); fl(ctx, hx('2a3a7a'), 8)
    ctx.save(); rect_r(ctx, x, y, w, h, 16); ctx.clip()
    ellipse(ctx, x + 270, y + 80, 36, 36); fl(ctx, hx('fff7c2'), 4)
    rnd = random.Random(5)
    for k in range(24):
        sx = x + rnd.uniform(0, w); sy = y + (rnd.uniform(0, h) + lf * rnd.uniform(1.5, 3)) % h
        ellipse(ctx, sx, sy, 6, 6); setc(ctx, WHITE); ctx.fill()
    ctx.new_path(); ctx.move_to(x, y + h); ctx.curve_to(x + 100, y + h - 60, x + 260, y + h - 30, x + w, y + h - 70); ctx.line_to(x + w, y + h); ctx.close_path()
    setc(ctx, WHITE); ctx.fill()
    ctx.restore()
    ctx.move_to(x + w / 2, y); ctx.line_to(x + w / 2, y + h); ctx.move_to(x, y + h / 2); ctx.line_to(x + w, y + h / 2); ink(ctx, 6); ctx.stroke()
    rect_r(ctx, x - 24, y + h - 6, w + 48, 24, 8); fl(ctx, WHITE, 5)
    for sx, d in ((x - 50, -1), (x + w - 10, 1)):
        poly(ctx, [(sx, y - 30), (sx + 60, y - 30), (sx + 60 + d * 12, y + h + 40), (sx - 10 + d * 6, y + h + 40)]); fl(ctx, hx('ff8ab8'), 6)
    rect_r(ctx, x - 80, y - 44, w + 160, 20, 8); fl(ctx, hx('a0603a'), 5)


def picture(ctx, x, y, tilt=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(tilt)
    ctx.move_to(0, -100); ctx.line_to(-50, -70); ctx.move_to(0, -100); ctx.line_to(50, -70); ink(ctx, 4); ctx.stroke()
    rect_r(ctx, -80, -70, 160, 130, 10); fl(ctx, hx('5fb8ef'), 7)
    rect_r(ctx, -62, -52, 124, 94, 6); fl(ctx, hx('fff4dc'), 4)
    for cx_, cy_, r in ((-24, 8, 26), (18, 14, 20), (-2, -22, 16)):            # snowman doodle
        pass
    ellipse(ctx, 0, 18, 22, 20); fl(ctx, WHITE, 3); ellipse(ctx, 0, -14, 15, 14); fl(ctx, WHITE, 3)
    poly(ctx, [(0, -14), (0, -9), (16, -12)]); fl(ctx, ORANGE, 2)
    ctx.restore()


def door(ctx, lf, opn=0.0, outside_tree=False):
    """front door on the right wall. opn 0 closed .. 1 wide open"""
    x0, x1, top = DOORX0, DOORX1, DOORTOP
    rect_r(ctx, x0 - 30, top - 30, x1 - x0 + 60, FLOOR - top + 30, 8); fl(ctx, WHITE, 7)        # frame
    # outside: snowy night porch
    ctx.save(); ctx.rectangle(x0, top, x1 - x0, FLOOR - top); ctx.clip()
    ctx.rectangle(x0, top, x1 - x0, FLOOR - top); setc(ctx, hx('243a78')); ctx.fill()
    rnd = random.Random(11)
    for k in range(14):
        sx = x0 + rnd.uniform(0, x1 - x0); sy = top + (rnd.uniform(0, 600) + lf * 2.4) % 600
        ellipse(ctx, sx, sy, 6, 6); setc(ctx, WHITE); ctx.fill()
    ctx.rectangle(x0, FLOOR - 70, x1 - x0, 80); setc(ctx, hx('eef6ff')); ctx.fill()
    ctx.restore()
    # door leaf swings in (gets narrower)
    if opn < 1:
        w = (x1 - x0) * (1 - 0.82 * opn)
        rect_r(ctx, x1 - w, top, w, FLOOR - top, 6); fl(ctx, hx('3ccfb0'), 7)
        if opn < 0.3:
            ctx.new_path(); ctx.arc(x1 - w / 2, top + 170, 54, 0, 6.29); setc(ctx, INK); ctx.set_line_width(28); ctx.stroke_preserve()
            setc(ctx, GREEN); ctx.set_line_width(20); ctx.stroke()
            for k in range(5):
                ellipse(ctx, x1 - w / 2 + 54 * math.cos(k * 1.26), top + 170 + 54 * math.sin(k * 1.26), 8, 8); fl(ctx, RED, 2)
        ellipse(ctx, x1 - w + 30 if opn < 0.5 else x1 - w + 20, top + 330, 12, 12); fl(ctx, GOLD, 3)
    rect_r(ctx, x0 - 20, FLOOR - 6, x1 - x0 + 40, 26, 8); fl(ctx, hx('a0603a'), 5)              # doormat
    # coat hooks by the door
    for k in range(3):
        ellipse(ctx, x0 - 150 + k * 50, top + 40, 9, 9); fl(ctx, GOLD, 3)
    ctx.new_path(); ctx.move_to(x0 - 150, top + 40); ctx.curve_to(x0 - 190, top + 160, x0 - 120, top + 230, x0 - 100, top + 240); ctx.line_to(x0 - 150, top + 250)
    ctx.curve_to(x0 - 170, top + 200, x0 - 160, top + 120, x0 - 150, top + 40); fl(ctx, hx('ff8a1f'), 4)   # scarf


def sofa(ctx, x0=80, x1=640, squish=0.0):
    ctx.save(); ctx.translate((x0 + x1) / 2, FLOOR); ctx.scale(1, 1 - 0.12 * squish); ctx.translate(-(x0 + x1) / 2, -FLOOR)
    rect_r(ctx, x0 + 40, 1170, x1 - x0 - 80, 250, 50); fl(ctx, hx('ff9e5c'), 8)
    rect_r(ctx, x0, 1310, x1 - x0, 200, 40); fl(ctx, hx('ffb27a'), 8)
    for cx_ in (x0 + 20, x1 - 20):
        rect_r(ctx, cx_ - 50, 1270, 100, 260, 40); fl(ctx, hx('ff9e5c'), 7)
    ellipse(ctx, x0 + 170, 1280, 66, 56, 0.2); fl(ctx, hx('7fe3ff'), 6); sparkle(ctx, x0 + 170, 1280, 20, WHITE)
    ctx.restore()


def ceiling(ctx, lf, swing=0.0):
    ctx.rectangle(-3000, -3000, 9000, CEIL + 3000); setc(ctx, hx('fff6e6')); ctx.fill()
    ctx.move_to(-3000, CEIL); ctx.line_to(6000, CEIL); ink(ctx, 6); ctx.stroke()
    ctx.rectangle(-3000, CEIL, 9000, 26); setc(ctx, hx('f0d2a8')); ctx.fill()
    # hanging lamp
    lx = 560
    a = swing * math.sin(lf * 0.5) * 0.5
    ctx.save(); ctx.translate(lx, CEIL + 26); ctx.rotate(a)
    ctx.move_to(0, 0); ctx.line_to(0, 150); ink(ctx, 4); ctx.stroke()
    poly(ctx, [(-70, 230), (70, 230), (34, 150), (-34, 150)]); fl(ctx, hx('ffd34f'), 6)
    ellipse(ctx, 0, 236, 26, 14); fl(ctx, hx('fff7c2'), 3)
    ctx.restore()


def room(ctx, lf, pic_tilt=0.0, swing=0.0, opn=0.0, sofa_sq=0.0):
    wall = hx('ffe0d0')
    ctx.rectangle(-3000, CEIL, 9000, 6000); setc(ctx, wall); ctx.fill()
    rnd = random.Random(86)
    for k in range(140):
        sparkle(ctx, rnd.uniform(-400, 2500), rnd.uniform(CEIL + 40, FLOOR - 140), 9, dark(wall, 0.9))
    ctx.rectangle(-3000, FLOOR - 110, 9000, 110); setc(ctx, hx('ffc9b0')); ctx.fill()
    ctx.move_to(-3000, FLOOR - 110); ctx.line_to(6000, FLOOR - 110); ink(ctx, 5); ctx.stroke()
    window(ctx, lf)
    picture(ctx, 790, 820, pic_tilt + 0.03 * math.sin(lf * 0.05))
    picture(ctx, 1330, 760, -0.04)
    door(ctx, lf, opn)
    # floor
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('c9874e')); ctx.fill()
    for k in range(-10, 40):
        ctx.move_to(k * 150, FLOOR); ctx.line_to(k * 150 - 140, FLOOR + 600)
    setc(ctx, hx('b5743e')); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-3000, FLOOR); ctx.line_to(6000, FLOOR); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, TX, FLOOR + 150, 560, 96); fl(ctx, hx('ff6f86'), 6)                        # round rug
    ellipse(ctx, TX, FLOOR + 150, 470, 72); setc(ctx, hx('ffc1da')); ctx.fill()
    sofa(ctx, squish=sofa_sq)
    # plant + pet bed with sleeping dog
    px = 1440
    poly(ctx, [(px - 45, FLOOR - 90), (px + 45, FLOOR - 90), (px + 34, FLOOR + 20), (px - 34, FLOOR + 20)]); fl(ctx, hx('5fb8ef'), 6)
    for a in (-0.6, -0.2, 0.2, 0.6):
        ellipse(ctx, px + 60 * math.sin(a), FLOOR - 170 - 30 * math.cos(a), 24, 70, a); fl(ctx, GREEN, 5)
    ceiling(ctx, lf, swing)


# ------------------------------------------------------------------ people
def stand(ctx, ch, x, k, p, f_=1):
    return draw(ctx, x, GND - 186 * k, k, f_, ch, p)


def pull_dad(ctx, lf, x=1240, amp=1.0, ch=DAD_R):
    """Dad leaning back, both hands on the trunk to his right"""
    w = math.sin(lf * 1.4) * amp
    d = stand(ctx, ch, x + 8 * w, KD, P(eye='glare', mouth='scream', torso=-22 + 5 * w, head=10, lsh=85, lel=5, rsh=95, rel=-5,
                                         lhip=-20, lkn=10, rhip=20, rkn=-10))
    return d


def mom_stand(ctx, x, lf, p=None, f_=1):
    p = p or P(eye='smug', mouth='smile', lsh=20, lel=-20, rsh=10, rel=-20)
    return stand(ctx, MOM, x, KM, p, f_)


def kid_stand(ctx, x, lf, p=None, f_=1, hop=0.0):
    p = p or P(eye='happy', mouth='grin', lsh=20, lel=-20, rsh=20, rel=-20)
    return draw(ctx, x, GND - 186 * KK - hop, KK, f_, KID, p)


# ------------------------------------------------------------------ shot 1: hook
def door_tree(ctx, lf, slide=0.0):
    """tree lying sideways, crown stuck outside the door, trunk sticking into the room"""
    tx = 1330 - 900 * slide                       # trunk end x
    ty = 1300
    jit = 6 * math.sin(lf * 1.4) * (1 - slide)
    ctx.save(); ctx.translate(tx, ty + jit); ctx.rotate(math.pi / 2)
    ctx.scale(1.0, 1.0)
    _tree_local(ctx, 1500, 0.55 + 0.45 * slide, lf, snow=0.7)
    ctx.restore()


def hook(ctx, f, lf, z=None):
    z = z or 1.14 + 0.04 * eio(pop(lf, 0, 54))
    ctx.save(); cam(ctx, 1330, 1270, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    room(ctx, lf, opn=1.0)
    dog(ctx, 760, GND + 20, 0.5, 1, lf, sleep=False)
    door_tree(ctx, lf)
    # needle tufts poking out around the door frame
    for k in range(7):
        a = k * 0.9
        ctx.move_to(DOORX0 - 10, 1120 + k * 50); ctx.line_to(DOORX0 - 50 - 20 * math.sin(lf * 0.7 + a), 1100 + k * 50)
    setc(ctx, PINE_D); ctx.set_line_width(8); ctx.stroke()
    d = pull_dad(ctx, lf)
    sweat(ctx, d['head'][0] - d['R'] * 1.0, d['head'][1] - d['R'] * 0.4, lf, 1.0)
    needles(ctx, DOORX0, 1250, ((lf * 0.05) % 1), 10, int(lf * 0.05), 260)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"COME...", "...IN...!!\"", WHITE, t, 124, col2=GREEN, y=1470)


# ------------------------------------------------------------------ shot 2: POP -> too tall -> saw
def pop_in(ctx, f, il):
    # il 0..56: 0-6 last tug; 6 *POP!* tree slides in, Dad flies onto the sofa; 20 *FLOMP*; 34 "...GOT IT."
    sl = eout(pop(il, 6, 18))
    z = lerp(1.14, 0.92, eio(pop(il, 4, 16)))
    ctx.save(); cam(ctx, lerp(1330, 960, eio(pop(il, 4, 16))), 1250, z, 0, shake_at(il, [6, 20], 12, 10), f)
    room(ctx, il, opn=1.0, sofa_sq=pop(il, 20, 24) * (1 - pop(il, 24, 30)), pic_tilt=0.12 * pop(il, 6, 10))
    dog(ctx, lerp(760, 1460, eout(pop(il, 8, 20))), GND + 20, 0.5, 1, il)
    door_tree(ctx, il, sl)
    if il < 6:
        d = pull_dad(ctx, il, amp=1.6)
    elif il < 20:
        u = eout(pop(il, 6, 20))
        x = lerp(1240, 520, u); hop = 380 * 4 * u * (1 - u)
        d = draw(ctx, x, GND - 186 * KD - hop, KD, 1, DAD, P(eye='shock', mouth='scream', rot=-40 * u, lsh=170, lel=0, rsh=150, rel=0, lhip=40, rhip=-40))
    else:
        d = draw(ctx, 520, 1330 - 186 * KD, KD, 1, DAD, P(eye='happy' if il > 30 else 'shock', mouth='grin' if il > 30 else 'open',
                                                          rot=-20, torso=-10, lsh=150, lel=-10, rsh=40, rel=-60, lhip=80, rhip=70, lkn=-80, rkn=-70))
    needles(ctx, 1200, 1250, pop(il, 6, 30), 34, 4, 700)
    ctx.restore()
    if il < 20:
        label(ctx, "*POP!*", 540, 460, 150, GREEN, -0.05, pop(il, 6, 9))
    elif il < 34:
        label(ctx, "*FLOMP!*", 540, 460, 130, ORANGE, 0.05, pop(il, 20, 23))
    else:
        label(ctx, "\"...GOT IT.\"", 540, 1470, 130, WHITE, -0.03, pop(il, 34, 37))


def too_tall(ctx, f, il):
    # il 0..50: low wide angle, tree in its stand, top folded along the ceiling; 6 *CREEEAK*, 16 *BONK* lamp swings, 28 "...TOO TALL."
    bend = eio(pop(il, 4, 16))
    cy = lerp(1150, 1080, eio(il / 50))
    ctx.save(); cam(ctx, 1000, cy, 0.86, 0, shake_at(il, [16], 10, 10), f)
    room(ctx, il, swing=pop(il, 16, 20), opn=0.0)
    stand_base(ctx, TX)
    xtree(ctx, TX, FLOOR - 30, 1500, 0.95, lf=il, bend=bend)
    ceiling(ctx, il, pop(il, 16, 20))
    d = stand(ctx, DAD, 1420, KD, P(eye='shock', mouth='open' if il < 28 else 'flat', head=-28, torso=-6, lsh=20, lel=-20, rsh=30, rel=-30), f_=-1)
    if il >= 28:
        twitch(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 1.0, il, 1.1)
    dog(ctx, 1640, GND + 20, 0.5, -1, il)
    ctx.restore()
    if il < 16:
        label(ctx, "*CREEEAK...*", 540, 560, 104, hx('c98a4a'), 0.04, pop(il, 3, 6))
    elif il < 28:
        label(ctx, "*BONK!*", 540, 560, 140, RED, -0.05, pop(il, 16, 19))
    else:
        label(ctx, "\"...TOO TALL.\"", 540, 1470, 130, WHITE, -0.03, pop(il, 28, 31))


HS = (1500, 1150, 820, 330)


def saw_montage(ctx, f, il):
    # il 0..80: Dutch tilt; *ZZZT!* cuts at 8, 28, 48 shrink the tree; 62 tiny tree "PERFECT!"
    stage = 0 if il < 12 else 1 if il < 32 else 2 if il < 52 else 3
    h = HS[stage]
    rot = -7 if il < 60 else lerp(-7, 0, eio(pop(il, 60, 66)))
    cy = lerp(1180, 1330, eio(pop(il, 0, 60)))
    z = lerp(0.95, 1.18, eio(pop(il, 52, 66)))
    ctx.save(); cam(ctx, lerp(1080, 1120, eio(pop(il, 52, 66))), cy, z, rot, shake_at(il, [12, 32, 52], 8, 8), f)
    room(ctx, il)
    logs(ctx, 1260, (0, 3, 6, 9)[stage])
    stand_base(ctx, TX)
    xtree(ctx, TX, FLOOR - 30, h, 0.95 if h > 500 else 0.75, lf=il, bend=1.0 if h > 1130 else 0.0)
    ceiling(ctx, il)
    if il < 60:
        for g in (2, 1, 0):
            ctx.push_group()
            w = math.sin((il - g) * 2.2)
            d = stand(ctx, DAD_R, 820 + 20 * w, KD, P(eye='glare', mouth='scream', torso=34, head=-20, lsh=100 + 22 * w, lel=-10, rsh=80 + 22 * w, rel=0,
                                                        lhip=-30, lkn=60, rhip=40, rkn=-10))
            saw(ctx, d['front'], 300, 0.15)
            ctx.pop_group_to_source(); ctx.paint_with_alpha(1.0 if g == 0 else 0.25)
        sweat(ctx, d['head'][0] - d['R'] * 1.0, d['head'][1] - d['R'] * 0.4, il, 1.0)
        for k in range(3):
            ellipse(ctx, TX - 20 + 40 * math.sin(il * 1.7 + k), FLOOR - 60 - 20 * k - (il * 9 + k * 30) % 90, 10, 8); setc(ctx, hx('f0c890')); ctx.fill()
    else:
        d = stand(ctx, DAD, 800, KD, P(eye='happy', mouth='grin', torso=-4, lsh=150, lel=-20, rsh=160, rel=-20))
        for k, (sx, sy) in enumerate(((TX - 160, FLOOR - 260), (TX + 170, FLOOR - 200), (TX, FLOOR - 400))):
            sparkle(ctx, sx, sy, 24 + 8 * math.sin(il * 0.5 + k), GOLD)
    ctx.restore()
    if il < 60:
        for j, a in enumerate((8, 28, 48)):
            label(ctx, "*ZZZT!*", 540 + (-150, 150, 0)[j], (520, 640, 760)[j], 110, PURPLE, (-0.08, 0.07, -0.04)[j], pop(il, a, a + 3))
        label2(ctx, "\"A LITTLE OFF", "THE BOTTOM...\"", WHITE, pop(il, 2, 6), 104, col2=ORANGE, y=1470)
    else:
        label(ctx, "\"PERFECT!\"", 540, 1470, 140, GOLD, -0.03, pop(il, 62, 65))


def s2(ctx, f):
    lf = f - 54
    if lf < 56:
        pop_in(ctx, f, lf)
    elif lf < 106:
        too_tall(ctx, f, lf - 56)
    else:
        saw_montage(ctx, f, lf - 106)


# ------------------------------------------------------------------ shot 3: the star -> it's a bush
def star_scene(ctx, f, il):
    # il 0..100: 0-30 Mom + kid walk in with a giant star; 30-44 kid hops, places star; 44 *BOINK* tree folds; 58 Mom "...honey. It's a BUSH."
    fold = eout(pop(il, 44, 52))
    ctx.save(); cam(ctx, 980, 1300, 1.0, 0, shake_at(il, [44], 8, 8), f)
    room(ctx, il)
    logs(ctx, 1260, 9)
    stand_base(ctx, TX, 0.8)
    # tiny tree, folds sideways under the star
    ctx.save(); ctx.translate(TX, FLOOR - 26); ctx.rotate(1.0 * fold)
    _tree_local(ctx, 330, 0.75, il, deco=1.0)
    if il >= 40:
        star(ctx, 0, -330 - 60, 80, 0.2 * math.sin(il * 0.3))
    ctx.restore()
    d = stand(ctx, DAD, 1390, KD, P(eye='happy' if il < 44 else 'shock', mouth='grin' if il < 44 else 'flat', lsh=150 if il < 44 else 20, lel=-20,
                                     rsh=160 if il < 44 else 30, rel=-20), f_=-1)
    if il > 50:
        twitch(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 1.0, il, 1.1)
    mx = lerp(300, 620, eout(pop(il, 0, 26)))
    m = mom_stand(ctx, mx, il, P(eye='happy' if il < 44 else 'smug', mouth='smile' if il < 44 else 'flat', lsh=20, lel=-30 if il < 50 else -120, rsh=10, rel=-20))
    if 4 < il < 40:
        hop = 160 * 4 * pop(il, 30, 40) * (1 - pop(il, 30, 40))
        kx = lerp(-100, lerp(760, 860, pop(il, 26, 40)), eout(pop(il, 4, 28)))
        k = kid_stand(ctx, kx, il, P(eye='happy', mouth='grin', lsh=170, lel=-10, rsh=160, rel=-10, lhip=-10 + 10 * math.sin(il), rhip=10), hop=hop)
        star(ctx, k['head'][0] + 30, k['head'][1] - k['R'] * 2.3, 70)
    else:
        k = kid_stand(ctx, 840 if il >= 40 else -200, il, P(eye='happy', mouth='open', lsh=150, lel=-10, rsh=40, rel=-20))
    ctx.restore()
    if il < 44:
        label(ctx, "\"Ooh! The STAR!\"", 540, 1470, 120, GOLD, -0.03, pop(il, 8, 11))
    elif il < 58:
        label(ctx, "*BOINK!*", 540, 560, 140, PINK, 0.05, pop(il, 44, 47))
    else:
        label2(ctx, "\"...honey.", "It's a BUSH.\"", WHITE, pop(il, 58, 62), 120, col2=GREEN, y=1470)


def s3(ctx, f):
    star_scene(ctx, f, f - 240)


# ------------------------------------------------------------------ shot 4: the one close-up
def ecu(ctx, f, il):
    # il 0..80: Dad's face full of pine needles, eye twitching "...it's a TABLE tree."
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.07 * eio(il / 80), 0, 2 + shake_at(il, [0], 6, 8), f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('c8f0d4')); ctx.fill()
    rays(ctx, 540, 900, 240, 1500, il * 0.02, col=(1, 1, 1), a=0.35, n=16)
    face(ctx, DAD, P(eye='glare', mouth='grin'), 540, 940, 200, 0.0)
    rnd = random.Random(9)
    for k in range(34):                                     # needles stuck in hair/face
        a = rnd.uniform(math.pi * 1.05, math.pi * 1.95) if k < 24 else rnd.uniform(0, math.pi * 2)
        r = rnd.uniform(160, 230) if k < 24 else rnd.uniform(60, 150)
        x = 540 + math.cos(a) * r; y = 920 + math.sin(a) * r
        b = rnd.uniform(0, 3.14)
        ctx.move_to(x - 18 * math.cos(b), y - 18 * math.sin(b)); ctx.line_to(x + 18 * math.cos(b), y + 18 * math.sin(b))
    setc(ctx, PINE_D); ctx.set_line_width(7); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.save(); ctx.translate(690, 700); ctx.rotate(0.5); _tree_local(ctx, 120, 0.5, il); ctx.restore()      # a twig on his head
    twitch(ctx, 760, 760, il, 1.4)
    ctx.restore()
    label2(ctx, "\"...it's a", "TABLE tree.\"", WHITE, pop(il, 8, 12), 124, col2=GREEN, y=1470)


def s4(ctx, f):
    ecu(ctx, f, f - 340)


# ------------------------------------------------------------------ shot 5: twist -> loop
def grandma(ctx, f, il):
    # il 0..110: 0 *DING-DONG!*; 10-22 door opens: GIANT tree with a bow fills the doorway; 30 kid "YAAAY!!"; 66 Mom "It's even BIGGER!"
    opn = eio(pop(il, 10, 22))
    z = lerp(0.98, 1.06, eio(il / 110))
    ctx.save(); cam(ctx, 1200, 1280, z * 0.97, 0, shake_at(il, [0, 22], 6, 8), f)
    room(ctx, il, opn=opn)
    # giant tree on the porch fills the doorway (clipped to the opening)
    ctx.save(); ctx.rectangle(DOORX0, DOORTOP, DOORX1 - DOORX0, FLOOR - DOORTOP); ctx.clip()
    xtree(ctx, (DOORX0 + DOORX1) / 2, FLOOR + 20, 1500, 0.42, lf=il, snow=0.8)
    ctx.restore()
    if opn > 0.5:
        ctx.save(); ctx.translate(DOORX0 + 130, 1260); ctx.scale(1.3, 1.3)
        for sg in (-1, 1):
            ctx.new_path(); ctx.move_to(0, 0); ctx.curve_to(sg * 30, -60, sg * 80, -40, sg * 60, 0); ctx.curve_to(sg * 70, 30, sg * 30, 20, 0, 0); fl(ctx, RED, 4)
            poly(ctx, [(0, 4), (sg * 34, 50), (sg * 18, 56), (0, 12)]); fl(ctx, RED, 4)
        ellipse(ctx, 0, 0, 16, 14); fl(ctx, dark(RED, 0.85), 4)
        ctx.restore()
        tag(ctx, DOORX0 + 160, 1340, 0.12 + 0.05 * math.sin(il * 0.2))
        for k in range(7):
            ctx.move_to(DOORX0 - 10, 1020 + k * 70); ctx.line_to(DOORX0 - 60, 1000 + k * 70 + 10 * math.sin(il * 0.5 + k))
        setc(ctx, PINE_D); ctx.set_line_width(8); ctx.stroke()
    # family
    hop = 120 * abs(math.sin(il * 0.35)) if 28 < il < 66 else 0
    kid_stand(ctx, 1170, il, P(eye='happy', mouth='open' if il > 28 else 'smile', lsh=170 if il > 28 else 20, lel=-10, rsh=170 if il > 28 else 20, rel=-10), hop=hop)
    mom_stand(ctx, 970, il, P(eye='happy', mouth='grin' if il > 60 else 'smile', lsh=60, lel=-30, rsh=20, rel=-20))
    d = stand(ctx, DAD, 770, KD, P(eye='shock' if il > 22 else 'normal', mouth='flat', lsh=20, lel=-10, rsh=20, rel=-10))
    if il > 40:
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 1.0, il, 1.1)
    dog(ctx, 1460, GND + 20, 0.5, 1, il)
    ctx.restore()
    card(ctx, 'p2', il, 14)
    if il < 28:
        label(ctx, "*DING-DONG!*", 540, 1470, 116, GOLD, -0.04, pop(il, 0, 3))
    elif il < 66:
        label(ctx, "\"YAAAY!!\"", 540, 1470, 140, PINK, 0.04, pop(il, 30, 33))
    else:
        label2(ctx, "\"It's even", "BIGGER!\"", WHITE, pop(il, 66, 70), 124, col2=GREEN, y=1470)


def of_course(ctx, f, il):
    # il 0..100: Dad ECU-medium "...of COURSE it is." -> rolls up sleeves, marches to the door, grabs the trunk "HNNNGH!!"
    ctx.save(); cam(ctx, lerp(900, 1300, eio(pop(il, 44, 70))), 1270, lerp(1.25, 1.14, eio(pop(il, 44, 70))), 0, shake_at(il, [74], 8, 8), f)
    room(ctx, il, opn=1.0)
    ctx.save(); ctx.rectangle(DOORX0, DOORTOP, DOORX1 - DOORX0, FLOOR - DOORTOP); ctx.clip()
    xtree(ctx, (DOORX0 + DOORX1) / 2, FLOOR + 20, 1500, 0.42, lf=il, snow=0.8)
    ctx.restore()
    tag(ctx, DOORX0 + 160, 1340, 0.12)
    if il < 44:
        d = stand(ctx, DAD, 900, KD, P(eye='glare', mouth='flat', lsh=20, lel=-10, rsh=20, rel=-10, head=6 * math.sin(il * 0.3)))
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 1.0, il, 1.1)
    elif il < 70:
        u = eio(pop(il, 44, 70))
        w = math.sin(il * 0.9)
        stand(ctx, DAD, lerp(900, 1240, u), KD, P(eye='glare', mouth='grin', lsh=40 * w, lel=-90, rsh=-40 * w, rel=-90, lhip=25 * w, rhip=-25 * w))
    else:
        d = pull_dad(ctx, il, amp=1.4)
        sweat(ctx, d['head'][0] - d['R'] * 1.0, d['head'][1] - d['R'] * 0.4, il, 1.0)
    ctx.restore()
    if il < 44:
        label2(ctx, "\"...of COURSE", "it is.\"", WHITE, pop(il, 4, 8), 120, col2=RED, y=1470)
    elif il < 74:
        label(ctx, "\"HERE... WE... GO.\"", 540, 1470, 112, WHITE, -0.03, pop(il, 46, 49))
    else:
        label(ctx, "\"HNNNNGH!!\"", 540, 1470, 130, RED, -0.03, pop(il, 74, 77))


def s5(ctx, f):
    lf = f - 420
    if lf < 110:
        grandma(ctx, f, lf)
    elif lf < 210:
        of_course(ctx, f, lf - 110)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (54, s2), (240, s3), (340, s4), (420, s5)]
CUTS = (54, 110, 160, 240, 340, 420, 530, 630)


def render(f):
    import sketch
    sketch.BOIL[0] = f // 4
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.0, 0.05, 0.15, 0.2)
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
                              "-i", "out/xmastree_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
