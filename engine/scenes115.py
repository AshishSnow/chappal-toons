"""'DAD vs THE SEAGULL'. Original, general-audience comedy short, 22s.
Hook:   sunny beach medium shot: red-faced Dad in a tug-of-war with a cute seagull over his paper cone of fries
        -> "MY. FRIES!!" + caption 'DAD vs THE SEAGULL:' (kid giggling by his sandcastle, umbrella, crab, sea).
Beat 1: Dad wins the tug, gull flaps off -> "Ha! MINE." -> lifts ONE fry to his mouth -> *SWOOP!* the gull snatches it
        straight out of his lips -> "...HEY!!"
Beat 2: Dutch-tilt defence montage: PLAN A: HIDE IT. (fries under his sun hat, gull lifts the hat *flap flap*) NOPE! /
        PLAN B: SCARY FACE. ("RAAAH!" -> gull *SQUAWK!!* blows his hair back) NOPE! / PLAN C: THE FORT. (Dad behind a
        sandcastle wall -> the gull pops out of the tower *POP!* "...hi.") NOPE!
Close-up (the one face shot): sweaty Dad hugging the cone, gull eyes in the sky "I'm SMARTER..." "...than a BIRD!!"
Twist:  the gull is gone -> "VICTORY!" -> a shadow -> tilt up: the sky is FULL of gulls -> PLOT TWIST: IT BROUGHT ITS
        FRIENDS. -> *FWOOOSH!!* feather storm -> the flock flies off with his fries, hat, towel + the kid's bucket ->
        feathered Dad "...of COURSE." -> pulls a BACKUP cone from behind his back -> the gull lands on it *plop* -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face, rays
from scenes48 import label2
from scenes58 import sweat, twitch
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
DAD = dict(doodle.DAD, shirt=hx('ff7eb6'), pants=hx('1fb5c9'), shoes=hx('ffd23f'), sleeve=0.45)
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('7fe3ff'), pants=hx('ff8a1f'), shoes=hx('ffd23f'))
N = 660
SEA, FLOOR, GND = 1180, 1560, 1600
KD, KK = 1.08, 0.82
DADX = 860
GULX = 1140
KIDX = 560
UMX = 330
HAT = hx('ffe08a')

CAPS = {'p1': [[("DAD vs ", OUT), ("THE SEAGULL:", BLUE)]],
        'p2': [[("PLOT TWIST:", RED)], [("IT BROUGHT ", OUT), ("ITS FRIENDS.", BLUE)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def fries(ctx, x, y, s=1.0, a=0.0, n=7):
    """paper cone of fries, (x, y) = where the hand grips (middle of the cone)."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rnd = random.Random(7)
    for k in range(n):
        fx = -40 + k * (80 / max(1, n - 1)) + rnd.uniform(-4, 4)
        rect_r(ctx, fx - 8, -150 + rnd.uniform(0, 30) + abs(fx) * 0.3, 16, 110, 5); fl(ctx, hx('ffd23f'), 3)
    poly(ctx, [(-62, -60), (62, -60), (0, 70)]); fl(ctx, WHITE, 4)
    ctx.save(); poly(ctx, [(-62, -60), (62, -60), (0, 70)]); ctx.clip()
    for k in range(-3, 4):
        poly(ctx, [(k * 36 - 9, -70), (k * 36 + 9, -70), (k * 14 + 4, 80), (k * 14 - 4, 80)])
    setc(ctx, RED); ctx.fill(); ctx.restore()
    poly(ctx, [(-62, -60), (62, -60), (0, 70)]); ink(ctx, 4); ctx.stroke()
    ctx.restore()


def one_fry(ctx, x, y, a=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -8, -50, 16, 100, 5); fl(ctx, hx('ffd23f'), 3); ctx.restore()


def sunhat(ctx, x, y, s=1.0, a=0.0):
    """bucket sun hat, (x, y) = centre of the brim."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 120, 26); fl(ctx, HAT, 4)
    ctx.move_to(-74, 2); ctx.curve_to(-70, -90, 70, -90, 74, 2); ctx.close_path(); fl(ctx, HAT, 4)
    ctx.move_to(-72, -14); ctx.curve_to(-30, -4, 30, -4, 72, -14); setc(ctx, hx('ff5fa8')); ctx.set_line_width(14); ctx.stroke()
    ctx.restore()


def feather(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(0, -34); ctx.curve_to(16, -20, 14, 20, 0, 34); ctx.curve_to(-14, 20, -16, -20, 0, -34); fl(ctx, WHITE, 3)
    ctx.move_to(0, -30); ctx.line_to(0, 40); ink(ctx, 2.5); ctx.stroke()
    ctx.restore()


def gull(ctx, x, y, s=1.0, f_=1, lf=0, fly=False, mood='smug', beak=0.0, flap=None, carry=None):
    """original cute seagull. standing: (x, y) = feet. flying: (x, y) = body centre. f_=1 faces right.
    returns the beak tip (user coords) for props."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s * f_, s)
    grey = hx('aebdd4'); dk = hx('5c6a86')
    if fly:
        ph = lf * 0.7 if flap is None else flap
        wy = 90 * math.cos(ph)
        # back wing
        ctx.move_to(-10, -14); ctx.curve_to(-40, -14 - wy * 0.6, -70, -10 - wy, -96, -wy * 1.05); ctx.curve_to(-60, -wy * 0.4, -30, 4, 10, 4)
        ctx.close_path(); fl(ctx, dark(grey, 0.85), 3)
        ellipse(ctx, 0, 0, 74, 34, -0.08); fl(ctx, WHITE, 4)
        poly(ctx, [(-60, -6), (-112, -26), (-106, 14)]); fl(ctx, grey, 3)
        hx_, hy_ = 64, -24
    else:
        for lx in (-14, 14):
            ctx.move_to(lx, -46); ctx.line_to(lx * 1.2, 0); setc(ctx, hx('ff9a3c')); ctx.set_line_width(7); ctx.stroke()
            poly(ctx, [(lx * 1.2 - 4, 0), (lx * 1.2 + 24, 0), (lx * 1.2 + 10, -12)]); fl(ctx, hx('ff9a3c'), 2)
        poly(ctx, [(-56, -96), (-112, -118), (-100, -74)]); fl(ctx, grey, 3)
        ellipse(ctx, 0, -86, 70, 48, -0.18); fl(ctx, WHITE, 4)
        hx_, hy_ = 40, -148
    ellipse(ctx, hx_, hy_, 42, 40); fl(ctx, WHITE, 4)
    # beak (upper + lower)
    bx = hx_ + 34
    op = 0.5 * beak
    ctx.save(); ctx.translate(bx, hy_ + 6); ctx.rotate(-op * 0.6)
    poly(ctx, [(0, -10), (54, -4), (60, 4), (0, 6)]); fl(ctx, hx('ffd23f'), 3)
    ctx.restore()
    ctx.save(); ctx.translate(bx, hy_ + 8); ctx.rotate(op * 0.9)
    poly(ctx, [(0, 2), (48, 2), (0, 14)]); fl(ctx, hx('ffc21a'), 3)
    ellipse(ctx, 40, 6, 5, 4); setc(ctx, RED); ctx.fill()
    ctx.restore()
    tip = ctx.user_to_device(bx + 58, hy_ + 8)
    # eye
    ex, ey = hx_ + 8, hy_ - 8
    ellipse(ctx, ex, ey, 15, 16); fl(ctx, WHITE, 3)
    ellipse(ctx, ex + 3, ey + 1, 9, 10); setc(ctx, INK); ctx.fill()
    ellipse(ctx, ex + 6, ey - 3, 3.5, 3.5); setc(ctx, WHITE); ctx.fill()
    ellipse(ctx, ex - 2, ey + 4, 1.8, 1.8); setc(ctx, WHITE); ctx.fill()
    if mood in ('smug', 'angry'):
        ctx.move_to(ex - 18, ey - 24 + (8 if mood == 'angry' else 0)); ctx.line_to(ex + 16, ey - 14 - (2 if mood == 'angry' else -4))
        ink(ctx, 5); ctx.stroke()
        if mood == 'smug':
            ctx.rectangle(ex - 18, ey - 18, 36, 9); setc(ctx, WHITE); ctx.fill()   # half-lidded
            ctx.move_to(ex - 16, ey - 9); ctx.line_to(ex + 16, ey - 9); ink(ctx, 3); ctx.stroke()
    ellipse(ctx, hx_ - 8, hy_ + 18, 11, 6); setc(ctx, (1, 0.55, 0.65, 0.7)); ctx.fill()
    if not fly:
        ctx.move_to(-20, -96); ctx.curve_to(10, -110, 40, -86, 30, -64); ctx.curve_to(0, -60, -30, -70, -50, -90); ctx.close_path()
        fl(ctx, grey, 3)
        poly(ctx, [(-50, -90), (-86, -104), (-70, -80)]); fl(ctx, dk, 2)
    else:
        ctx.move_to(-6, -10); ctx.curve_to(-30, -10 - wy * 0.7, -60, -8 - wy * 1.05, -90, -wy * 1.15); ctx.curve_to(-50, -wy * 0.45, -20, 8, 20, 6)
        ctx.close_path(); fl(ctx, grey, 3)
        ex2 = -90; ey2 = -wy * 1.15
        ellipse(ctx, ex2 + 6, ey2 + 4, 14, 8, 0.4); fl(ctx, dk, 2)
    ctx.restore()
    tip = ctx.device_to_user(*tip)
    return tip


# ------------------------------------------------------------------ set
def beach(ctx, lf, shade=0.0):
    ctx.rectangle(-3000, -3000, 9000, 9000)
    ctx.set_source(vgrad(ctx, 0, 0, 0, SEA, [(0, hx('5fc4ff')), (1, hx('c8f0ff'))])); ctx.fill()
    # sun + clouds
    rays(ctx, 1380, 620, 110, 260, lf * 0.01, hx('fff3a0'), 0.5, 14)
    ellipse(ctx, 1380, 620, 100, 100); fl(ctx, hx('ffe14d'), 5)
    for cx_, cy_, s_ in ((200 + (lf * 0.4) % 300, 560, 1.0), (760, 760, 0.8), (1700, 820, 0.9)):
        ellipse(ctx, cx_, cy_, 90 * s_, 34 * s_); fl(ctx, WHITE, 3)
        ellipse(ctx, cx_ + 40 * s_, cy_ - 26 * s_, 56 * s_, 34 * s_); fl(ctx, WHITE, 3)
        ellipse(ctx, cx_ + 4, cy_ + 6, 84 * s_, 26 * s_); setc(ctx, WHITE); ctx.fill()
    # sea with wave lines + a little sailboat
    ctx.rectangle(-3000, SEA, 9000, 300); setc(ctx, hx('2fa8e8')); ctx.fill()
    for r_ in range(4):
        yy = SEA + 40 + r_ * 50
        for k in range(-10, 40):
            xx = k * 90 + (lf * (1.5 + r_ * 0.5)) % 90 + r_ * 30
            ctx.move_to(xx, yy); ctx.curve_to(xx + 15, yy - 10, xx + 30, yy - 10, xx + 45, yy)
        setc(ctx, (1, 1, 1, 0.55)); ctx.set_line_width(4); ctx.stroke()
    bx = 1000 + 10 * math.sin(lf * 0.03)
    poly(ctx, [(bx - 50, SEA + 20), (bx + 50, SEA + 20), (bx + 34, SEA + 44), (bx - 34, SEA + 44)]); fl(ctx, hx('ff8a1f'), 3)
    poly(ctx, [(bx, SEA - 70), (bx, SEA + 14), (bx + 50, SEA + 14)]); fl(ctx, WHITE, 3)
    # foam edge + sand
    ctx.move_to(-3000, SEA + 260)
    for k in range(-30, 80):
        ctx.line_to(k * 60, SEA + 250 + 12 * math.sin(k * 1.3 + lf * 0.08))
    ctx.line_to(6000, 6000); ctx.line_to(-3000, 6000); ctx.close_path(); setc(ctx, hx('ffe3a8')); ctx.fill()
    ctx.move_to(-3000, SEA + 262)
    for k in range(-30, 80):
        ctx.line_to(k * 60, SEA + 252 + 12 * math.sin(k * 1.3 + lf * 0.08))
    setc(ctx, WHITE); ctx.set_line_width(12); ctx.stroke()
    rnd = random.Random(115)
    for k in range(160):
        ellipse(ctx, rnd.uniform(-600, 2400), rnd.uniform(SEA + 300, 2400), 4, 3); setc(ctx, hx('e8c47c')); ctx.fill()
    # shells + starfish
    for sx, sy, c in ((1260, 1660, hx('ff9fc4')), (640, 1700, hx('ffd0e0')), (1500, 1590, hx('ffb38a'))):
        ctx.move_to(sx - 22, sy); ctx.curve_to(sx - 20, sy - 30, sx + 20, sy - 30, sx + 22, sy); ctx.close_path(); fl(ctx, c, 3)
        for j in (-10, 0, 10):
            ctx.move_to(sx, sy); ctx.line_to(sx + j, sy - 20); ink(ctx, 2); ctx.stroke()
    pts = []
    for j in range(10):
        r_ = 30 if j % 2 == 0 else 13
        a = -math.pi / 2 + j * math.pi / 5
        pts.append((360 + r_ * math.cos(a), 1720 + r_ * math.sin(a)))
    poly(ctx, pts); fl(ctx, hx('ff8a5c'), 3)
    if shade > 0:   # shadow of the flock
        ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, (0.15, 0.15, 0.35, 0.35 * shade)); ctx.fill()


def umbrella(ctx, x=UMX, lf=0):
    ctx.move_to(x, GND + 10); ctx.line_to(x + 40, 1080); setc(ctx, INK); ctx.set_line_width(14); ctx.stroke()
    ctx.move_to(x, GND + 10); ctx.line_to(x + 40, 1080); setc(ctx, WHITE); ctx.set_line_width(7); ctx.stroke()
    cx, cy = x + 40, 1090
    cols = [RED, WHITE, GOLD, WHITE, BLUE, WHITE]
    for k in range(6):
        a0 = math.pi + k * math.pi / 6; a1 = a0 + math.pi / 6
        ctx.move_to(cx, cy - 4); ctx.arc(cx, cy, 300, a0, a1); ctx.close_path(); setc(ctx, cols[k]); ctx.fill()
    ctx.new_path(); ctx.arc(cx, cy, 300, math.pi, 2 * math.pi)
    for k in range(6):
        a1 = math.pi + (k + 1) * math.pi / 6
        ctx.move_to(cx, cy); ctx.line_to(cx + 300 * math.cos(a1), cy + 300 * math.sin(a1))
    ink(ctx, 5); ctx.stroke()
    ellipse(ctx, cx, cy - 300, 16, 16); fl(ctx, GOLD, 3)


def towel(ctx, x=KIDX + 40, on=True):
    if not on:
        return
    poly(ctx, [(x - 260, GND + 30), (x + 220, GND + 30), (x + 260, GND + 150), (x - 300, GND + 150)]); fl(ctx, hx('8a3cff'), 4)
    for k in range(3):
        ctx.move_to(x - 270 + k * 4, GND + 60 + k * 30); ctx.line_to(x + 236 + k * 8, GND + 60 + k * 30)
    setc(ctx, hx('fff27a')); ctx.set_line_width(10); ctx.stroke()


def castle(ctx, x, y, s=1.0):
    """sandcastle, (x, y) = base centre."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    sand = hx('f2c46e')
    rect_r(ctx, -150, -110, 300, 110, 10); fl(ctx, sand, 4)
    for tx in (-120, 0, 120):
        h = 200 if tx == 0 else 160
        rect_r(ctx, tx - 40, -h, 80, h, 8); fl(ctx, sand, 4)
        for j in (-1, 0, 1):
            ctx.rectangle(tx - 40 + 30 * (j + 1), -h - 18, 20, 20)
        fl(ctx, sand, 3)
        rect_r(ctx, tx - 12, -h + 40, 24, 34, 10); setc(ctx, dark(sand, 0.7)); ctx.fill()
    ctx.move_to(0, -218); ctx.line_to(0, -290); ink(ctx, 4); ctx.stroke()
    poly(ctx, [(0, -290), (44, -276), (0, -262)]); fl(ctx, RED, 3)
    ctx.restore()


def bucket(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-40, -80), (40, -80), (30, 0), (-30, 0)]); fl(ctx, hx('ff5fa8'), 4)
    ctx.move_to(-38, -76); ctx.curve_to(-30, -130, 30, -130, 38, -76); ink(ctx, 4); ctx.stroke()
    ctx.restore()


def crab(ctx, x, y, lf):
    ctx.save(); ctx.translate(x + 8 * math.sin(lf * 0.15), y)
    for sd in (-1, 1):
        for j in range(3):
            ctx.move_to(sd * 20, -10 - j * 6); ctx.line_to(sd * (44 + j * 4), 4 - j * 2)
        setc(ctx, hx('e0442e')); ctx.set_line_width(5); ctx.stroke()
        ellipse(ctx, sd * 50, -42 - 6 * abs(math.sin(lf * 0.3)), 16, 12, sd * 0.5); fl(ctx, hx('ff5a3c'), 3)
    ellipse(ctx, 0, -20, 40, 24); fl(ctx, hx('ff5a3c'), 4)
    for ex in (-12, 12):
        ellipse(ctx, ex, -50, 8, 9); fl(ctx, WHITE, 2); ellipse(ctx, ex + 1, -49, 4, 5); setc(ctx, INK); ctx.fill()
    ctx.move_to(-10, -18); ctx.curve_to(-4, -12, 4, -12, 10, -18); ink(ctx, 3); ctx.stroke()
    ctx.restore()


def set_bg(ctx, lf, shade=0.0, kid=True, kid_eye='happy', kid_mouth='grin', tw=True, bk=True):
    beach(ctx, lf, shade)
    umbrella(ctx, lf=lf)
    towel(ctx, on=tw)
    castle(ctx, KIDX - 160, GND + 70, 0.55)
    if bk:
        bucket(ctx, KIDX + 150, GND + 80, 0.8)
    crab(ctx, 1400, GND + 60, lf)
    if kid:
        j = 8 * abs(math.sin(lf * 0.4))
        stand(ctx, KID, KIDX, KK, P(eye=kid_eye, mouth=kid_mouth, lsh=-40, lel=-110, rsh=40, rel=110 - j, head=6), 1, g=GND + 60)


# ------------------------------------------------------------------ people
def stand(ctx, ch, x, k, p, f_=1, g=GND):
    return draw(ctx, x, g - 186 * k, k, f_, ch, p)


def front_hand(d):
    return max(d['front'], d['back'], key=lambda q: q[0])


def held_up(d):
    hd, R = d['head'], d['R']
    return hd[0] + R * 1.45, hd[1] - R * 0.25


def dad_tug(ctx, x, lf, eye='glare', mouth='grin'):
    j = 10 * math.sin(lf * 0.9)
    d = stand(ctx, DAD, x + j * 0.3, KD, P(eye=eye, mouth=mouth, lsh=75, lel=10, rsh=85, rel=5, torso=-16 + j * 0.4, head=8,
                                           lhip=-20, rhip=20), 1)
    return d, j


def hook_scene(ctx, lf):
    set_bg(ctx, lf)
    d, j = dad_tug(ctx, DADX, lf)
    hx_, hy_ = front_hand(d)
    cx_ = hx_ + 70 + j * 0.5
    fries(ctx, cx_, hy_ - 10, 0.85, math.radians(80 + j * 0.8))
    gx = cx_ + 210 + j * 0.4
    gull(ctx, gx, GND + 10, 1.05, -1, lf, mood='angry')
    for k in range(3):
        feather(ctx, gx - 40 + 50 * k + 20 * math.sin(lf * 0.2 + k), GND - 260 - ((lf * 4 + k * 40) % 160), lf * 0.2 + k, 0.7)
    sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.5, lf, 0.9)
    return d


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    z = 1.12 + 0.03 * eio(pop(lf, 0, 54))
    ctx.save(); cam(ctx, 900, 1360, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    hook_scene(ctx, lf)
    ctx.restore()
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"MY.", "FRIES!!\"", WHITE, t, 124, col2=ORANGE, y=1440)


# ------------------------------------------------------------------ shot 2: win -> one fry -> SWOOP
def s2(ctx, f):
    il = f - 60   # 0..100
    z = 1.15 + 0.15 * eio(pop(il, 20, 60))
    cx = lerp(940, 900, eio(il / 100))
    ctx.save(); cam(ctx, cx, lerp(1360, 1240, eio(pop(il, 20, 60))), z, 0, shake_at(il, [58], 8, 12), f)
    set_bg(ctx, il + 60, kid_eye='shock' if il >= 60 else 'happy', kid_mouth='open' if il >= 60 else 'grin')
    if il < 30:
        d = stand(ctx, DAD, DADX, KD, P(eye='smug', mouth='grin', lsh=-30, lel=-100, rsh=-130, rel=-30, head=-6, torso=-4), 1)
        fries(ctx, *held_up(d), 0.85, 0.25)
        gull(ctx, lerp(1200, 1700, eio(il / 30)), lerp(1300, 700, eio(il / 30)), 0.9, 1, il, fly=True, mood='angry')
    else:
        u = eio(pop(il, 30, 46))
        snatched = il >= 58
        d = stand(ctx, DAD, DADX, KD, P(eye='smug' if il < 58 else 'shock', mouth='grin' if il < 46 else ('open' if il < 58 else 'scream'),
                                        lsh=40 + 30 * u, lel=40 + 80 * u, rsh=50, rel=70, head=-4, torso=-2), 1)
        fries(ctx, d['front'][0] + 30, d['front'][1] - 30, 0.85, 0.2)
        hd = d['head']; R = d['R']
        mx, my = hd[0] + R * 0.5, hd[1] + R * 0.45
        if not snatched:
            bh = d['back']
            one_fry(ctx, lerp(bh[0], mx + 20, u), lerp(bh[1] - 30, my, u), lerp(0.2, 1.5, u), 0.9)
        # swoop from the right, snatch at 58, exit left
        if il >= 50:
            sw = (il - 50) / 22
            gx = lerp(1500, 200, sw); gy = my - 60 + 120 * math.sin(math.pi * clamp(sw)) * -0.3
            tip = gull(ctx, gx, gy, 0.85, -1, il, fly=True, mood='smug', beak=0.0 if snatched else 1.0)
            if snatched:
                one_fry(ctx, tip[0] + 20, tip[1] + 4, 1.5, 0.9)
            if 54 <= il < 66:
                for k in range(6):
                    ctx.move_to(gx + 120 + k * 30, gy - 60 + k * 24); ctx.line_to(gx + 320 + k * 30, gy - 60 + k * 24)
                setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(6); ctx.stroke()
        if il >= 60:
            rnd = random.Random(3)
            for k in range(5):
                ph = clamp((il - 58) / 30)
                feather(ctx, mx + rnd.uniform(-120, 120) * ph, my - 40 + 200 * ph, ph * 5 + k, 0.7)
    ctx.restore()
    if il < 30:
        label2(ctx, "\"Ha!", "MINE.\"", WHITE, pop(il, 2, 6), 124, col2=MINT, y=1440)
    elif il < 58:
        label(ctx, "*munch time...*", 540, 640, 84, GOLD, 0.03, pop(il, 32, 36))
    else:
        label(ctx, "*SWOOP!*", 540, 640, 130, CYAN, -0.05, pop(il, 58, 61))
        if il >= 70:
            label(ctx, "\"...HEY!!\"", 540, 1440, 130, WHITE, 0.03, pop(il, 70, 74))


# ------------------------------------------------------------------ shot 3: defence montage (Dutch tilt)
PLANS = [("PLAN A:", "HIDE IT."), ("PLAN B:", "SCARY FACE."), ("PLAN C:", "THE FORT.")]


def nope(ctx, t):
    if t <= 0:
        return
    s = 1.6 - 0.6 * eout(min(1, t * 1.5))
    ctx.save(); ctx.translate(540, 1100); ctx.rotate(-0.18); ctx.scale(s, s)
    rect_r(ctx, -230, -70, 460, 140, 20); setc(ctx, (1, 1, 1, 0.92)); ctx.fill_preserve(); setc(ctx, RED); ctx.set_line_width(12); ctx.stroke()
    text(ctx, "NOPE!", 0, 40, 120, RED, ow=0)
    ctx.restore()


def s3(ctx, f):
    il = f - 160   # 0..150
    i, c = min(2, il // 50), il - 50 * min(2, il // 50)
    rot = (7, -7, 7)[i]
    ctx.save(); cam(ctx, (950, 980, 900)[i], 1300, 1.3, rot, shake_at(c, [24] if i == 1 else [22] if i == 2 else [], 8, 16), f)
    set_bg(ctx, il + 160, kid=(i != 2))
    if i == 0:   # fries under the hat on his head; gull lifts the hat
        d = stand(ctx, DAD, DADX, KD, P(eye='smug' if c < 24 else 'shock', mouth='grin' if c < 24 else 'open',
                                        lsh=-60, lel=-110, rsh=60, rel=110, head=-4), 1)
        hd, R = d['head'], d['R']
        lift = eio(pop(c, 16, 34))
        top = hd[1] - R * 0.8
        if lift < 0.4:
            fries(ctx, hd[0], top - 40, 0.55, 0.0, 5)
        gx, gy = hd[0] + 20, lerp(500, top - 220, eio(pop(c, 0, 16))) - 260 * lift
        tip = gull(ctx, gx - 40, gy - 60, 0.75, 1, c, fly=True, mood='smug', beak=0.3)
        sunhat(ctx, hd[0] + 10, top - 10 - 300 * lift, 0.75, 0.3 * lift)
        if lift >= 0.4:
            fries(ctx, hd[0], top - 40, 0.55, 0.0, 4)
            one_fry(ctx, tip[0] + 10, tip[1], 1.4, 0.7)
    elif i == 1:  # roar contest
        gx = DADX + 300
        blast = eio(pop(c, 22, 28))
        d = stand(ctx, DAD, DADX - 60 * blast, KD, P(eye='glare' if c < 22 else 'shock', mouth='scream', lsh=-120 + 40 * blast, lel=-40,
                                                     rsh=120 - 60 * blast, rel=-40, torso=12 - 26 * blast, head=10 - 20 * blast, rot=-8 * blast), 1)
        fries(ctx, d['back'][0] - 20, d['back'][1] - 20, 0.7, -0.4)
        gs = 1.05 + 0.35 * blast
        gull(ctx, gx, GND + 10, gs, -1, c, mood='angry', beak=1.0 if c >= 22 else 0.2)
        if c >= 22:
            for k in range(9):
                yy = 1060 + k * 46
                ctx.move_to(gx - 120, yy); ctx.line_to(gx - 120 - 260 - 40 * math.sin(k + c), yy + (k - 4) * 14)
            setc(ctx, (1, 1, 1, 0.85)); ctx.set_line_width(7); ctx.stroke()
            hd = d['head']
            for k in range(4):   # hair strands blown back
                ctx.move_to(hd[0] - 60, hd[1] - 70 + k * 16); ctx.line_to(hd[0] - 150 - 20 * math.sin(c + k), hd[1] - 90 + k * 22)
            ink(ctx, 6); ctx.stroke()
    else:         # sandcastle fort; gull pops out of the tower
        d = stand(ctx, DAD, DADX, KD, P(eye='smug' if c < 22 else 'shock', mouth='grin' if c < 22 else 'open',
                                        lsh=-30, lel=-120, rsh=40, rel=120, head=-6), 1)
        fries(ctx, d['front'][0] + 20, d['front'][1] - 40, 0.75, 0.1)
        pu = eio(pop(c, 20, 26))
        if pu > 0:
            gull(ctx, DADX + 300, GND - 240 - 130 * pu + 130, 0.8, -1, c, mood='smug')
        castle(ctx, DADX + 60, GND + 40, 1.45)
        if c >= 30:
            one_fry(ctx, DADX + 200, GND - 330, -1.2, 0.8)
    ctx.restore()
    label2(ctx, PLANS[i][0], PLANS[i][1], GOLD, pop(c, 0, 4), 88, col2=WHITE, y=640)
    if i == 0:
        if c >= 18:
            label(ctx, "*flap flap*", 540, 1440, 104, CYAN, -0.03, pop(c, 18, 22))
        nope(ctx, pop(c, 34, 40))
    if i == 1:
        if c < 22:
            label(ctx, "\"RAAAH!\"", 540, 1440, 120, WHITE, -0.03, pop(c, 4, 8))
        else:
            label(ctx, "*SQUAWK!!*", 540, 1440, 140, ORANGE, 0.04, pop(c, 22, 25))
        nope(ctx, pop(c, 36, 42))
    if i == 2:
        if c >= 22:
            label(ctx, "*POP!*", 540, 900, 110, PINK, 0.05, pop(c, 22, 25))
            label(ctx, "\"...hi.\"", 540, 1440, 120, WHITE, -0.03, pop(c, 26, 30))
        nope(ctx, pop(c, 38, 44))


# ------------------------------------------------------------------ shot 4: the one close-up
def s4(ctx, f):
    il = f - 310   # 0..70
    z = 1.0 + 0.07 * eio(il / 70)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('5fc4ff')), (0.7, hx('c8f0ff')), (0.7, hx('ffe3a8')), (1, hx('ffe3a8'))])); ctx.paint()
    ctx.save(); cam(ctx, 540, 960, z, 0, shake_at(il, [36], 8, 12), f)
    rays(ctx, 540, 1000, 200, 900, il * 0.02, (1, 1, 1), 0.35, 16)
    # gull eyes peering from the sky
    for k, (gx, gy) in enumerate(((180, 560), (900, 520), (130, 1500))):
        bob = 10 * math.sin(il * 0.2 + k)
        gull(ctx, gx, gy + bob, 0.55, 1 if gx < 540 else -1, il + k * 5, fly=True, mood='smug')
    face(ctx, DAD, P(eye='glare', mouth='grin' if il < 36 else 'scream'), 540, 1000, 200)
    sunhat(ctx, 540, 840, 1.6, -0.05)
    fries(ctx, 790, 1260, 1.1, 0.25)
    sweat(ctx, 330, 900, il, 1.2)
    twitch(ctx, 770, 760, il, 1.4)
    ctx.restore()
    label(ctx, "\"I'm SMARTER...", 540, 1440, 104, WHITE, -0.03, pop(il, 3, 7))
    if il >= 36:
        label(ctx, "...than a BIRD!!\"", 540, 1560, 112, ORANGE, 0.03, pop(il, 36, 40))


# ------------------------------------------------------------------ shot 5: victory -> the flock -> loop
def s5(ctx, f):
    lf = f - 380
    if lf >= 250:
        return s1(ctx, f, f - 630)
    if lf < 50:
        zoom, cx, cy, rot = 1.2, 900, 1260, 0
    elif lf < 130:   # tilt up to the sky
        u = eio(pop(lf, 52, 80))
        zoom, cx, cy, rot = lerp(1.2, 0.95, u), 900, lerp(1260, 1080, u), 0
    elif lf < 200:
        zoom, cx, cy, rot = 1.0, 900, 1200, 0
    else:
        zoom, cx, cy, rot = 1.18, 900, 1250, 0
    shade = eio(pop(lf, 44, 60)) * (1 - eio(pop(lf, 150, 170)))
    ctx.save(); cam(ctx, cx, cy, zoom, rot, shake_at(lf, [130], 12, 18), f)
    gone = lf >= 150
    set_bg(ctx, lf + 380, shade, kid_eye='happy' if not (60 <= lf < 150) else 'shock', kid_mouth='grin' if lf < 60 or lf >= 150 else 'open',
           tw=not gone, bk=not gone)
    if lf < 130:
        hat_on = True
        d = stand(ctx, DAD, DADX, KD, P(eye='happy' if lf < 50 else 'shock', mouth='grin' if lf < 50 else 'open',
                                        lsh=-30, lel=-100, rsh=-130, rel=-30, head=-6 if lf < 50 else -14), 1)
        fries(ctx, *held_up(d), 0.85, 0.25)
        hd, R = d['head'], d['R']
        sunhat(ctx, hd[0] + 6, hd[1] - R * 0.8, 0.75, 0.05)
        if lf < 50:
            for j in range(3):
                sparkle(ctx, d['front'][0] - 120 + j * 100, d['front'][1] - 230 - 12 * math.sin(lf * 0.3 + j), 18, YEL)
        # the flock circling overhead
        if lf >= 44:
            rnd = random.Random(44)
            for k in range(22):
                a = lf * 0.03 * (1 if k % 2 else -1) + k * 0.7
                r_ = 220 + 60 * (k % 4)
                gx = 900 + r_ * 1.7 * math.cos(a) + rnd.uniform(-60, 60)
                gy = 380 + r_ * 0.6 * math.sin(a) + rnd.uniform(-40, 40) - 200 * (1 - eio(pop(lf, 44, 70)))
                gull(ctx, gx, gy, 0.5 + 0.1 * (k % 3), 1 if math.sin(a) > 0 else -1, lf + k * 3, fly=True, mood='smug' if k % 3 else 'angry')
        if lf >= 120:   # dive streaks
            for k in range(10):
                ctx.move_to(500 + k * 80, 400); ctx.line_to(700 + k * 30, 1200)
            setc(ctx, (1, 1, 1, 0.6)); ctx.set_line_width(8); ctx.stroke()
    else:
        # feather storm, then the flock flies off with everything
        rnd = random.Random(8)
        lift = eio(pop(lf, 150, 200))
        if lf < 200:
            d = stand(ctx, DAD, DADX, KD, P(eye='shock', mouth='scream', lsh=-150, lel=-20, rsh=150, rel=20, head=-10), 1)
        else:
            d = stand(ctx, DAD, DADX, KD, P(eye='glare', mouth='flat', lsh=-12, lel=-15, rsh=12, rel=-15, head=4), 1) \
                if lf < 220 else stand(ctx, DAD, DADX, KD, P(eye='smug', mouth='grin', lsh=-12, lel=-15, rsh=-150, rel=-30, head=-6), 1)
        hd, R = d['head'], d['R']
        for k in range(6):   # feathers stuck in his hair
            feather(ctx, hd[0] - 70 + k * 28, hd[1] - R * 0.95 - (k % 2) * 16, -0.6 + k * 0.25, 0.75)
        if lf < 150:
            for k in range(26):
                ph = clamp((lf - 130) / 20 + rnd.uniform(-0.3, 0))
                feather(ctx, hd[0] + rnd.uniform(-420, 420) * (0.3 + ph), hd[1] + rnd.uniform(-300, 300) * (0.3 + ph), k + lf * 0.2, 1.0)
            for k in range(8):
                a = k * 0.78 + lf * 0.2
                gull(ctx, hd[0] + 260 * math.cos(a), hd[1] + 60 + 220 * math.sin(a), 0.6, 1 if math.cos(a) < 0 else -1, lf + k, fly=True, mood='angry')
        # flock carrying loot up and away
        if lf >= 150:
            loot = [('fries', 560, 900), ('hat', 820, 760), ('towel', 1120, 860), ('bucket', 1380, 980)]
            for k, (what, lx, ly) in enumerate(loot):
                yy = ly - 700 * lift + 20 * math.sin(lf * 0.3 + k); xx = lx + 300 * lift * (1 if k % 2 else -0.4)
                if what == 'fries':
                    fries(ctx, xx, yy + 90, 0.7, 0.2)
                elif what == 'hat':
                    sunhat(ctx, xx, yy + 70, 0.6, 0.4)
                elif what == 'towel':
                    poly(ctx, [(xx - 130, yy + 40), (xx + 130, yy + 40), (xx + 110, yy + 140), (xx - 150, yy + 130)]); fl(ctx, hx('8a3cff'), 4)
                    ctx.move_to(xx - 130, yy + 80); ctx.line_to(xx + 120, yy + 80); setc(ctx, YEL); ctx.set_line_width(10); ctx.stroke()
                else:
                    bucket(ctx, xx, yy + 140, 0.7, 0.3)
                for j in (-1, 1) if what == 'towel' else (0,):
                    gull(ctx, xx + j * 110, yy, 0.6, 1, lf + k * 4 + j, fly=True, mood='smug')
        if lf >= 220:   # backup cone from behind his back -> the gull lands on it
            cx_, cy_ = held_up(d)
            fries(ctx, cx_, cy_, 0.85, 0.25)
            land = eio(pop(lf, 234, 244))
            gull(ctx, lerp(1500, cx_ + 130, land), lerp(700, cy_ - 60, land), 0.95, -1, lf, fly=land < 1, mood='smug') \
                if land < 1 else gull(ctx, cx_ + 130, cy_ + 120, 0.95, -1, lf, mood='smug', beak=0.6)
        if 200 <= lf < 220:
            twitch(ctx, hd[0] + R * 0.8, hd[1] - R * 0.9, lf, 0.8)
    ctx.restore()
    # labels
    if lf < 50:
        label(ctx, "\"...it's GONE.\"", 540, 1440, 110, WHITE, -0.03, pop(lf, 2, 6))
        if lf >= 22:
            label(ctx, "\"VICTORY!\"", 540, 640, 130, GOLD, 0.04, pop(lf, 22, 26))
    elif lf < 130:
        label(ctx, "*SQUAWK! SQUAWK!*", 540, 1530, 96, WHITE, -0.03, pop(lf, 48, 52))
        card(ctx, 'p2', lf, 72)
    elif lf < 200:
        label(ctx, "*FWOOOSH!!*", 540, 640, 130, CYAN, -0.04, pop(lf, 130, 133))
        if lf >= 160:
            label(ctx, "*flap flap flap*", 540, 1440, 96, WHITE, 0.03, pop(lf, 160, 164))
    elif lf < 220:
        label2(ctx, "\"...of", "COURSE.\"", WHITE, pop(lf, 202, 206), 124, col2=ORANGE, y=1440)
    else:
        label2(ctx, "\"...BACKUP", "fries.\"", WHITE, pop(lf, 222, 226), 116, col2=GOLD, y=1440)
        if lf >= 244:
            label(ctx, "*plop*", 540, 640, 110, PINK, 0.04, pop(lf, 244, 247))


SHOTS = [(0, s1), (60, s2), (160, s3), (310, s4), (380, s5)]
CUTS = (60, 160, 210, 260, 310, 380, 510, 630)


def render(f):
    import sketch
    sketch.BOIL[0] = f // 4
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.1, 0.05, 0.15, 0.14)
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
                              "-i", "out/dad_vs_seagull_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
