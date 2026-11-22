"""'Trick birthday candles' - original, general-audience comedy short, 22s.
Hook:   birthday kid mid-blow behind the cake, cheeks puffed red, flames bending but NOT going out.
        Caption "TRICK BIRTHDAY / CANDLES:" + "*FWOOOOO!*" + "WHY WON'T THEY GO OUT?!"
Beat 1: Mom + Dad "Make a WISH!" -> kid blows -> out, smoke, "YAAAY!" -> macro: *pop! pop! pop!* they relight -> kid face "...HUH?!"
Beat 2: MEGA inhale (kid inflates) -> *FWOOOOSH!!* hats fly, picture tilts, frosting splats Dad's face -> flames still lit "STILL. LIT."
Beat 3: frosting-faced Dad with a leaf blower "Step aside. PRO TIME." -> *VRRRMMM!* the whole cake launches -> *SPLAT!* onto Mom's head,
        candles still burning on top of her "...REALLY?"
Twist:  kid pulls out the box TRICK CANDLES, sly grin "Hehe... GOTCHA!!" -> low-angle parents (frosting + cake hat) evil grins "Oh... it's ON."
End:    "10 MINUTES LATER:" super-sweet parents bring a NEW cake "Here's your REAL cake, sweetie!" -> kid blows -> won't go out ->
        split screen: parents with a giant box TRICK CANDLES x100 "PAYBACK." / kid puffing furious -> loops to the hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes64 import puffed, confetti
from scenes56 import splat
from scenes65 import dog
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
FROST = hx('ffc2dc'); CREAM = hx('fff6e6'); SPONGE = hx('ffd28a')
DAD = dict(doodle.DAD, shirt=hx('7fb8ff'), pants=hx('2a3a6a'))
MOM = dict(doodle.MOM_G, shirt=hx('9b4dff'), pants=hx('3d5a9e'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff8a1f'), pants=hx('2a3a6a'), shoes=hx('3ccfb0'))
N = 660
FLOOR = 1600
TT = 1330                       # table top
CX = 560                        # cake x
CS = 0.85                       # cake scale
KDAD, KMOM, KKID = 1.2, 1.1, 1.0
GDAD, GMOM, GKID = TT + 70, TT + 66, TT + 14     # "ground" lines behind the table (feet hidden)

CAPS = {'p1': [[("TRICK BIRTHDAY", OUT)], [("CANDLES:", PINK)]],
        'p2': [[("PLOT TWIST:", RED)]],
        'p3': [[("10 MINUTES LATER...", OUT)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ set
def room(ctx, lf=0, tilt=0.0):
    wall = hx('bdeee0')
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, wall); ctx.fill()
    rnd = random.Random(5)
    for k in range(70):                                   # little star wallpaper
        x, y = rnd.uniform(-500, 1600), rnd.uniform(-200, FLOOR - 40)
        ctx.save(); ctx.translate(x, y); ctx.rotate(rnd.uniform(0, 1))
        pts = [(math.cos(a) * (14 if i % 2 == 0 else 6), math.sin(a) * (14 if i % 2 == 0 else 6)) for i, a in enumerate([j * math.pi / 5 - math.pi / 2 for j in range(10)])]
        poly(ctx, pts); setc(ctx, dark(wall, 0.9)); ctx.fill(); ctx.restore()
    # window (left)
    rect_r(ctx, 40, 560, 290, 330, 14); fl(ctx, hx('9fdcff'), 8)
    for cx_, cy_ in ((140, 680), (250, 760)):
        for dx, r in ((-30, 26), (0, 36), (32, 26)):
            ellipse(ctx, cx_ + dx, cy_, r, r * 0.8); setc(ctx, WHITE); ctx.fill()
    ctx.move_to(185, 560); ctx.line_to(185, 890); ctx.move_to(40, 725); ctx.line_to(330, 725); ink(ctx, 7); ctx.stroke()
    for sx in (20, 300):                                   # curtains
        poly(ctx, [(sx, 540), (sx + 50, 540), (sx + 40 + (10 if sx > 100 else -10), 920), (sx - 6, 920)]); fl(ctx, hx('ff8fb8'), 6)
    # picture frame (right), tilts on the gust
    ctx.save(); ctx.translate(900, 600); ctx.rotate(tilt)
    ctx.move_to(0, -40); ctx.line_to(-60, 30); ctx.move_to(0, -40); ctx.line_to(60, 30); ink(ctx, 4); ctx.stroke()
    rect_r(ctx, -95, 30, 190, 170, 10); fl(ctx, hx('ffb347'), 8)
    rect_r(ctx, -70, 52, 140, 126, 6); fl(ctx, hx('fff6d8'), 5)
    ctx.move_to(0, 150); ctx.curve_to(-60, 100, -30, 60, 0, 90); ctx.curve_to(30, 60, 60, 100, 0, 150); fl(ctx, RED, 4)
    ctx.restore()
    # bunting
    ctx.move_to(-200, 470); ctx.curve_to(300, 540, 800, 540, 1300, 470); ink(ctx, 4); ctx.stroke()
    for k in range(12):
        x = -60 + k * 105; y = 470 + 60 * math.sin(math.pi * clamp((x + 200) / 1500)) * 1.0
        poly(ctx, [(x, y), (x + 90, y), (x + 45, y + 80)]); fl(ctx, (RED, YEL, BLUE, PINK, GREEN)[k % 5], 4)
    # balloons
    for k, (bx, col) in enumerate(((400, RED), (500, YEL), (1010, BLUE), (60, PURPLE))):
        by = 880 + (k % 2) * 70 + 14 * math.sin(lf * 0.1 + k)
        ctx.move_to(bx, by + 80); ctx.curve_to(bx - 20, by + 180, bx + 20, by + 240, bx, by + 400); ink(ctx, 3); ctx.stroke()
        ellipse(ctx, bx, by, 58, 72); fl(ctx, col, 6)
        ellipse(ctx, bx - 20, by - 26, 10, 18); setc(ctx, (1, 1, 1, 0.6)); ctx.fill()
    # floor + rug + plant
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('e0a86c')); ctx.fill()
    for k in range(-10, 30):
        ctx.move_to(k * 140, FLOOR); ctx.line_to(k * 140 - 120, FLOOR + 600)
    setc(ctx, hx('c98f55')); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-3000, FLOOR); ctx.line_to(6000, FLOOR); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 540, FLOOR + 230, 560, 120); fl(ctx, hx('ff9ec4'), 6)
    ellipse(ctx, 540, FLOOR + 230, 470, 90); setc(ctx, hx('ffd0e2')); ctx.fill()
    px = 1040
    poly(ctx, [(px - 60, FLOOR - 130), (px + 60, FLOOR - 130), (px + 45, FLOOR + 10), (px - 45, FLOOR + 10)]); fl(ctx, hx('ff8a1f'), 6)
    for a in (-0.7, -0.25, 0.2, 0.65):
        ellipse(ctx, px + 90 * math.sin(a), FLOOR - 230 - 40 * math.cos(a), 34, 90, a); fl(ctx, GREEN, 5)


def table(ctx):
    rect_r(ctx, 40, TT - 20, 1000, 50, 18); fl(ctx, WHITE, 7)
    # scalloped skirt
    ctx.new_path(); ctx.move_to(50, TT + 20)
    ctx.line_to(1030, TT + 20); ctx.line_to(1030, TT + 150)
    n = 10
    for i in range(n):
        x1 = 1030 - (i + 1) * 98
        ctx.curve_to(1030 - i * 98 - 20, TT + 200, x1 + 20, TT + 200, x1, TT + 150)
    ctx.close_path(); fl(ctx, hx('ff7fb0'), 7)
    for i in range(n):
        ellipse(ctx, 1030 - i * 98 - 49, TT + 100, 14, 14); setc(ctx, WHITE); ctx.fill()
    for x in (120, 920):
        rect_r(ctx, x, TT + 160, 44, FLOOR - TT - 150, 10); fl(ctx, hx('a0603a'), 6)


def hat(ctx, x, y, R, rot=0.0, col=PINK, dot=YEL):
    """party hat sitting on a head drawn at (x, y) with radius R"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    poly(ctx, [(-0.42 * R, -0.78 * R), (0.42 * R, -0.78 * R), (0.02 * R, -1.75 * R)]); fl(ctx, col, 5)
    for t in (0.3, 0.62):
        ctx.move_to(lerp(-0.42, 0.02, t) * R, lerp(-0.78, -1.75, t) * R); ctx.line_to(lerp(0.42, 0.02, t) * R, lerp(-0.78, -1.75, t) * R)
    setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(max(3, R * 0.06)); ctx.stroke()
    ellipse(ctx, 0.02 * R, -1.78 * R, 0.15 * R, 0.15 * R); fl(ctx, dot, 4)
    ctx.restore()


def flame(ctx, x, y, s, bend=0.0, lf=0, k=0):
    """flame whose base is at (x, y); s = size 0..1, bend = sideways lean (-1..1)"""
    if s <= 0.02:
        return
    fx = 5 * math.sin(lf * 0.9 + k * 1.7) * s
    tipx = x + fx + bend * 46 * s; tipy = y - 64 * s * (1 - 0.35 * abs(bend))
    ellipse(ctx, x, y - 26 * s, 44 * s, 52 * s); setc(ctx, (1, 0.85, 0.3, 0.25)); ctx.fill()
    ctx.move_to(tipx, tipy); ctx.curve_to(x + 22 * s, y - 30 * s, x + 18 * s, y + 4 * s, x, y + 4 * s)
    ctx.curve_to(x - 18 * s, y + 4 * s, x - 22 * s, y - 30 * s, tipx, tipy); fl(ctx, hx('ffb02e'), 3)
    ellipse(ctx, x + bend * 8 * s, y - 10 * s, 8 * s, 12 * s); setc(ctx, hx('fff3a0')); ctx.fill()


def smoke(ctx, x, y, t, k=0):
    if not 0 < t < 1:
        return
    for j in range(3):
        tt = clamp(t * 1.4 - j * 0.15)
        if tt <= 0:
            continue
        r = 10 + 22 * tt
        ellipse(ctx, x + 18 * math.sin(tt * 6 + k + j), y - 30 - 130 * tt, r, r); setc(ctx, (0.75, 0.75, 0.8, 0.7 * (1 - tt))); ctx.fill()


CANDLE_COLS = (BLUE, PINK, GREEN, YEL, PURPLE)


def cake(ctx, x, y, s=1.0, lit=(1, 1, 1, 1, 1), bend=0.0, lf=0, bite=0.0, smk=None, pops=None, rot=0.0, plate=True):
    """two-tier birthday cake, plate on (x, y). lit = flame size per candle. returns candle wick points (world)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    if plate:
        ellipse(ctx, 0, 0, 200, 34); fl(ctx, WHITE, 6)
    rect_r(ctx, -160, -130, 320, 130, 26); fl(ctx, SPONGE, 7)
    rect_r(ctx, -168, -138, 336, 46, 22); fl(ctx, FROST, 6)
    for i in range(7):                                       # drips
        dx = -140 + i * 46
        ctx.move_to(dx - 14, -96); ctx.line_to(dx - 12, -80 - 14 * (i % 3)); ctx.curve_to(dx - 12, -60 - 14 * (i % 3), dx + 12, -60 - 14 * (i % 3), dx + 12, -80 - 14 * (i % 3))
        ctx.line_to(dx + 14, -96); ctx.close_path(); setc(ctx, FROST); ctx.fill()
    rect_r(ctx, -110, -230, 220, 100, 22); fl(ctx, CREAM, 7)
    rect_r(ctx, -116, -236, 232, 34, 16); fl(ctx, FROST, 5)
    rnd = random.Random(3)
    for i in range(16):                                      # sprinkles
        px, py = rnd.uniform(-140, 140), rnd.uniform(-75, -20)
        if i % 2:
            px, py = rnd.uniform(-95, 95), rnd.uniform(-190, -150)
        ctx.save(); ctx.translate(px, py); ctx.rotate(rnd.uniform(0, 3))
        rect_r(ctx, -9, -3, 18, 6, 3); setc(ctx, (RED, BLUE, GREEN, YEL, PURPLE)[i % 5]); ctx.fill(); ctx.restore()
    wicks = []
    for i in range(5):
        cx_ = -80 + i * 40; top = -236 - 70
        rect_r(ctx, cx_ - 9, top, 18, 72, 5); fl(ctx, CANDLE_COLS[i], 4)
        for j in range(3):
            ctx.move_to(cx_ - 9, top + 14 + j * 20); ctx.line_to(cx_ + 9, top + 6 + j * 20)
        setc(ctx, (1, 1, 1, 0.85)); ctx.set_line_width(4); ctx.stroke()
        ctx.move_to(cx_, top); ctx.line_to(cx_, top - 10); ink(ctx, 3); ctx.stroke()
        wicks.append(ctx.user_to_device(cx_, top - 8))
    ctx.restore()
    wicks = [ctx.device_to_user(*w) for w in wicks]
    for i, (wx, wy) in enumerate(wicks):
        flame(ctx, wx, wy, lit[i] * s, bend, lf, i)
        if smk is not None:
            smoke(ctx, wx, wy, smk[i], i)
        if pops is not None and 0 < pops[i] < 1:
            t = pops[i]
            for a in range(8):
                an = a * math.pi / 4
                r0 = 20 * s + 70 * s * t
                ctx.move_to(wx + math.cos(an) * r0, wy - 30 * s + math.sin(an) * r0)
                ctx.line_to(wx + math.cos(an) * (r0 + 30 * s * (1 - t)), wy - 30 * s + math.sin(an) * (r0 + 30 * s * (1 - t)))
            setc(ctx, hx('ffb02e')); ctx.set_line_width(7 * s); ctx.stroke()
    return wicks


def wind(ctx, x0, y0, x1, y1, lf, strength=1.0, n=5):
    """gust lines from (x0, y0) toward (x1, y1)"""
    if strength <= 0:
        return
    ang = math.atan2(y1 - y0, x1 - x0); L = math.hypot(x1 - x0, y1 - y0)
    ctx.save(); ctx.translate(x0, y0); ctx.rotate(ang)
    for k in range(n):
        off = (k - (n - 1) / 2) * 34 * strength
        ph = (lf * 0.12 + k * 0.23) % 1
        a0 = L * 0.1 + L * 0.5 * ph; a1 = a0 + L * 0.45
        ctx.move_to(a0, off * 0.5); ctx.curve_to(a0 + (a1 - a0) * 0.3, off - 20 * math.sin(lf * 0.5 + k), a0 + (a1 - a0) * 0.7, off * 1.3 + 20, a1, off * 1.5)
        setc(ctx, INK); ctx.set_line_width(14 * strength); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke_preserve()
        setc(ctx, WHITE); ctx.set_line_width(8 * strength); ctx.stroke()
    ctx.restore()


def mouth_of(b, f=1):
    hx_, hy_ = b['head']; R = b['R']
    return hx_ + f * R * 0.12, hy_ + R * 0.5


def blower(ctx, x, y, a, s=1.0):
    """leaf blower held at (x, y), tube toward angle a; returns tip"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -10, -18, 300, 36, 16); fl(ctx, hx('9aa4b8'), 6)
    rect_r(ctx, 270, -24, 46, 48, 10); fl(ctx, hx('6a7488'), 5)
    rect_r(ctx, -110, -70, 140, 110, 30); fl(ctx, ORANGE, 7)
    ellipse(ctx, -40, -15, 34, 34); fl(ctx, hx('3a2a40'), 5)
    rect_r(ctx, -90, -110, 100, 26, 12); fl(ctx, hx('3a2a40'), 5)
    tip = ctx.user_to_device(320, 0)
    ctx.restore()
    return ctx.device_to_user(*tip)


def box(ctx, x, y, s=1.0, rot=0.0, big=False):
    """candle box: 'TRICK CANDLES' (x100 when big)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rect_r(ctx, -150, -100, 300, 200, 18); fl(ctx, PURPLE, 7)
    rect_r(ctx, -132, -82, 264, 164, 12); fl(ctx, hx('ffe14a'), 5)
    text(ctx, "TRICK", 0, -36, 58, RED, ow=0, shadow=False)
    text(ctx, "CANDLES", 0, 18, 50, PURPLE, ow=0, shadow=False)
    text(ctx, "x100!" if big else "never go out!", 0, 60, 40 if big else 26, OUT, ow=0, shadow=False)
    for i in range(3):                                   # little candle icons
        ctx.rectangle(-130 + i * 16, -128, 10, 30); setc(ctx, CANDLE_COLS[i]); ctx.fill()
    ctx.restore()


def frosting_face(ctx, b, seed=4):
    hx_, hy_ = b['head']; R = b['R']
    splat(ctx, hx_ + R * 0.05, hy_ + R * 0.15, R * 0.55, seed, FROST)
    ellipse(ctx, hx_ - R * 0.25, hy_ + R * 0.02, R * 0.13, R * 0.15); fl(ctx, WHITE, 4)       # eyes blinking out
    ellipse(ctx, hx_ + R * 0.3, hy_ + R * 0.02, R * 0.13, R * 0.15); fl(ctx, WHITE, 4)
    for dx in (-0.22, 0.32):
        ellipse(ctx, hx_ + R * dx, hy_ + R * 0.04, R * 0.05, R * 0.06); setc(ctx, INK); ctx.fill()
    ellipse(ctx, hx_ + R * 0.3, hy_ - R * 0.35, R * 0.1, R * 0.1); fl(ctx, hx('ff3b5c'), 3)      # cherry


def cake_on_head(ctx, b, lf, lit=1.0):
    hx_, hy_ = b['head']; R = b['R']
    for i in range(5):                                         # frosting drips down the face
        dx = (-0.6 + i * 0.3) * R
        ctx.move_to(hx_ + dx - 14, hy_ - R * 0.55); ctx.line_to(hx_ + dx - 12, hy_ - R * 0.2 + 22 * (i % 2)); ctx.curve_to(hx_ + dx - 12, hy_ - R * 0.08 + 22 * (i % 2), hx_ + dx + 12, hy_ - R * 0.08 + 22 * (i % 2), hx_ + dx + 12, hy_ - R * 0.2 + 22 * (i % 2))
        ctx.line_to(hx_ + dx + 14, hy_ - R * 0.55); ctx.close_path(); fl(ctx, FROST, 3)
    cake(ctx, hx_ + R * 0.05, hy_ - R * 0.45, 0.62 * R / 100, (lit,) * 5, 0, lf, rot=-0.12, plate=False)


def mega_body(ctx, x, g, k, f, ch, p, amt):
    """draw a character slightly inflated (amt 0..1) around its head"""
    if amt <= 0:
        return draw(ctx, x, g - 186 * k, k, f, ch, p)
    s = 1 + 0.22 * amt
    ctx.save(); ctx.translate(x, g - 200 * k); ctx.scale(s, s * (1 - 0.04 * amt)); ctx.translate(-x, -(g - 200 * k))
    b = draw(ctx, x, g - 186 * k, k, f, ch, p)
    m = ctx.get_matrix()
    ctx.restore()
    # map head coords through the inflation transform
    sx_ = lambda px, py: (x + (px - x) * s, (g - 200 * k) + (py - (g - 200 * k)) * s * (1 - 0.04 * amt))
    b = dict(b); b['head'] = sx_(*b['head']); b['R'] = b['R'] * s
    return b


# ------------------------------------------------------------------ party table helper
def party(ctx, f, lf, kid_p, dad_p, mom_p, puff_amt=0.0, blow=0.0, lit=(1,) * 5, bend=0.0, smk=None, pops=None,
          tilt=0.0, hats=(0, 0, 0), dad_frost=False, mom_cake=False, mom_cake_lit=1.0, cake_on=True, inflate=0.0, after=None):
    room(ctx, lf, tilt)
    dog(ctx, 930, FLOOR + 250, 0.55, -1, lf, sleep=True)
    m = draw(ctx, 190, GMOM - 186 * KMOM, KMOM, 1, MOM, mom_p)
    d = draw(ctx, 900, GDAD - 186 * KDAD, KDAD, -1, DAD, dad_p)
    k = mega_body(ctx, 400, GKID, KKID, 1, KID, kid_p, inflate)
    for b, col, dot, flyoff in ((m, YEL, PINK, hats[0]), (d, BLUE, YEL, hats[1]), (k, PINK, YEL, hats[2])):
        if b is m and mom_cake:
            continue
        hx_, hy_ = b['head']
        if flyoff > 0:
            hat(ctx, hx_ + 900 * flyoff, hy_ - 400 * flyoff + 300 * flyoff * flyoff, b['R'], flyoff * 9, col, dot)
        else:
            hat(ctx, hx_, hy_, b['R'], 0.12 if b is not d else -0.12, col, dot)
    if puff_amt > 0:
        puffed(ctx, k['head'][0] + 0.08 * k['R'], k['head'][1], k['R'], puff_amt, RED)
    if dad_frost:
        frosting_face(ctx, d)
    if mom_cake:
        cake_on_head(ctx, m, lf, mom_cake_lit)
    table(ctx)
    wicks = cake(ctx, CX, TT, CS, lit, bend, lf, smk=smk, pops=pops) if cake_on else None
    if blow > 0 and wicks:
        mx, my = mouth_of(k)
        wind(ctx, mx + 40, my + 10, wicks[2][0] + 40, wicks[2][1] - 30, lf, blow)
    if after:
        after(k, d, m, wicks)
    return k, d, m, wicks


BLOWK = P(eye='closed', mouth='flat', lsh=20, lel=-30, rsh=-20, rel=-30, torso=8, head=10)


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    ctx.save(); cam(ctx, 560, 1100, 1.14 + 0.04 * eio(pop(lf, 0, 54)), 0, 3, f)
    party(ctx, f, lf, BLOWK, P(eye='shock', mouth='open', lsh=40, lel=-60, rsh=30, rel=-40),
          P(eye='shock', mouth='open', lsh=150, lel=40, rsh=20, rel=-20),
          puff_amt=1.0, blow=1.0, lit=(1,) * 5, bend=0.9 + 0.1 * math.sin(lf * 0.7))
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "*FWOOOOO!*", 540, 600, 96, CYAN, 0.04, t)
    label2(ctx, "\"WHY WON'T THEY", "GO OUT?!\"", WHITE, t, 104, col2=YEL, y=1440)


# ------------------------------------------------------------------ shot 2: wish -> out -> relight
def wish(ctx, f, il):
    # il 0..70
    sing = il < 22
    inh = pop(il, 22, 32); bl = 32 <= il < 44
    out = eout(pop(il, 32, 42))
    cheer = il >= 44
    lit = tuple(max(0, 1 - out * (1.6 - 0.15 * i)) for i in range(5))
    smk = tuple(pop(il, 38 + i, 66 + i) for i in range(5))
    up_ = 165 + 15 * math.sin(il * 0.5)
    if cheer:
        kp = P(eye='happy', mouth='grin', lsh=up_, lel=20, rsh=up_, rel=20)
        dp = P(eye='happy', mouth='grin', lsh=up_, lel=20, rsh=up_, rel=20)
        mp = P(eye='happy', mouth='grin', lsh=up_, lel=20, rsh=up_, rel=20)
    else:
        kp = P(eye='closed', mouth='smile', lsh=60, lel=-110, rsh=60, rel=-110) if sing else BLOWK
        sw = 20 * math.sin(il * 0.35)
        dp = P(eye='happy', mouth='open', lsh=120 + sw, lel=30, rsh=40, rel=-30)
        mp = P(eye='happy', mouth='open', lsh=40, lel=-30, rsh=120 - sw, rel=30)
    ctx.save(); cam(ctx, 560, 1070, 1.0 + 0.05 * eio(pop(il, 0, 70)), 0, 0, f)
    party(ctx, f, il, kp, dp, mp, puff_amt=inh if il < 44 else 0, blow=1.0 if bl else 0, lit=lit, bend=0.8 if bl else 0, smk=smk)
    if cheer:
        confetti(ctx, il - 44, 7)
    ctx.restore()
    if sing:
        label2(ctx, "\"Make a", "WISH!!\"", WHITE, pop(il, 1, 5), 120, col2=PINK, y=1440)
    elif not cheer:
        label(ctx, "*FFFFOOO!*", 540, 600, 100, CYAN, 0.04, pop(il, 32, 35))
    else:
        label(ctx, "\"YAAAAY!!\"", 540, 1440, 140, YEL, -0.04, pop(il, 44, 47))


def relight(ctx, f, il):
    # il 0..76 : 0-40 cake macro, candles relight; 40-76 kid face "...HUH?!"
    if il < 40:
        pops = tuple(pop(il, 8 + 6 * i, 16 + 6 * i) for i in range(5))
        lit = tuple(eout(pop(il, 8 + 6 * i, 12 + 6 * i)) for i in range(5))
        smk = tuple(clamp(0.45 + il / 30) if lit[i] == 0 else 0 for i in range(5))
        ctx.save(); cam(ctx, CX, TT - 180, 2.5 + 0.2 * eio(pop(il, 0, 40)), 0, shake_at(il, [8, 14, 20, 26, 32], 4, 8), f)
        room(ctx, il)
        table(ctx)
        cake(ctx, CX, TT, CS, lit, 0, il, smk=smk, pops=pops)
        ctx.restore()
        for i in range(5):
            if il >= 8 + 6 * i:
                label(ctx, "*pop!*", (300, 780, 380, 700, 540)[i], (600, 660, 1420, 1460, 560)[i] if i != 4 else 1400, 84, YEL, (-0.1, 0.1, 0.06, -0.06, 0)[i], pop(il, 8 + 6 * i, 11 + 6 * i))
        return
    il -= 40
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eio(pop(il, 0, 36)), 0, shake_at(il, [0], 8, 14), f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('ffd86b')); ctx.fill()
    rays(ctx, 540, 960, 240, 1500, il * 0.02, col=(1, 1, 1), a=0.35, n=16)
    R = 205; cx, cy = 540, 900
    face(ctx, KID, P(eye='shock', mouth='open'), cx, cy, R, 0.03)
    hat(ctx, cx + 0.02 * R, cy - 0.02 * R, R * 1.0, 0.15, PINK, YEL)
    sweat(ctx, cx + 0.9 * R, cy - 0.5 * R, il, 1.2)
    ctx.restore()
    label(ctx, "\"...HUH?!\"", 540, 1440, 150, WHITE, -0.03, pop(il, 3, 7))


def s2(ctx, f):
    lf = f - 54
    if lf < 70:
        wish(ctx, f, lf)
    else:
        relight(ctx, f, lf - 70)


# ------------------------------------------------------------------ shot 3: mega blow + leaf blower
def mega(ctx, f, il):
    # il 0..70: 0-22 inhale/inflate, 22-50 MEGA BLOW, 50-70 aftermath
    inf = eout(pop(il, 0, 20)) if il < 24 else max(0, 1 - pop(il, 24, 46))
    blowing = 22 <= il < 50
    hit = pop(il, 30, 36)
    tilt = 0.35 * eout(pop(il, 24, 34))
    hats = (pop(il, 26, 50), 0 if il < 26 else 0, 0)
    kp = P(eye='closed', mouth='flat', lsh=60, lel=-40, rsh=60, rel=-40, torso=-6) if il < 22 else BLOWK
    if il >= 50:
        kp = P(eye='shock', mouth='open', lsh=30, lel=-50, rsh=30, rel=-50)
    dp = P(eye='shock', mouth='open', lsh=40, lel=-40, rsh=30, rel=-40) if il < 22 else \
        P(eye='closed', mouth='scream', lsh=150, lel=30, rsh=140, rel=30, torso=-14, head=-12)
    if il >= 50:
        dp = P(eye='normal', mouth='flat', lsh=20, lel=-20, rsh=20, rel=-20)
    mp = P(eye='shock', mouth='open', lsh=150, lel=40, rsh=20, rel=-20) if il < 22 else \
        P(eye='closed', mouth='scream', lsh=160, lel=30, rsh=150, rel=30, torso=-10)
    if il >= 50:
        mp = P(eye='shock', mouth='open', lsh=40, lel=-40, rsh=30, rel=-40)
    sh = shake_at(il, [22], 26, 22) + (6 if blowing else 0)
    ctx.save(); cam(ctx, 560, 1060, 1.0, 0, sh, f)

    def after(k, d, m, wicks):
        # frosting blob flying from the cake to Dad's face
        if 26 <= il < 34:
            t = pop(il, 26, 34)
            hx_, hy_ = d['head']
            bx = lerp(CX + 20, hx_, t); by = lerp(TT - 220, hy_, t) - 120 * math.sin(math.pi * t)
            splat(ctx, bx, by, 40, 2, FROST)
        if blowing:
            mx, my = mouth_of(k)
            wind(ctx, mx + 40, my, 1200, my + 60, il, 2.2, 7)
    party(ctx, f, il, kp, dp, mp, puff_amt=(1.6 * inf) if il < 22 else (0.9 if blowing else 0),
          lit=(1,) * 5, bend=1.0 if blowing else 0, tilt=tilt, hats=hats, dad_frost=il >= 34,
          inflate=inf if il < 24 else 0, after=after)
    ctx.restore()
    if il < 22:
        label(ctx, "*HUUUUUUP*", 540, 600, 100, WHITE, -0.03, pop(il, 2, 6))
    elif il < 50:
        label(ctx, "*FWOOOOOSH!!*", 540, 600, 110, CYAN, 0.04, pop(il, 22, 25))
        if il >= 34:
            label(ctx, "*SPLAT!*", 760, 1440, 100, FROST, -0.06, pop(il, 34, 37))
    else:
        label2(ctx, "\"STILL.", "LIT.\"", WHITE, pop(il, 50, 54), 130, col2=ORANGE, y=1440)


def leaf_blower(ctx, f, il):
    # il 0..70: Dad (frosting face) + leaf blower: 0-18 brag, 18-40 VRRRM cake flies, 40 SPLAT on Mom, 44-70 "...REALLY?"
    blast = 18 <= il < 42
    fly = pop(il, 26, 40)
    landed = il >= 40
    kp = P(eye='shock', mouth='open', lsh=40, lel=-50, rsh=40, rel=-50)
    if il >= 48:
        kp = P(eye='happy', mouth='grin', lsh=60, lel=-100, rsh=60, rel=-100)     # giggling behind hands
    dp = P(eye='smug', mouth='grin', lsh=70, lel=-60, rsh=80, rel=-40) if il < 42 else P(eye='shock', mouth='flat', lsh=70, lel=-60, rsh=80, rel=-40)
    mp = P(eye='shock', mouth='open', lsh=150, lel=40, rsh=140, rel=40) if not landed else P(eye='glare', mouth='flat', lsh=20, lel=-20, rsh=20, rel=-20)
    sh = shake_at(il, [40], 14, 20) + (5 if blast else 0)
    ctx.save(); cam(ctx, 560, 1060, 1.0 + 0.04 * eio(pop(il, 0, 70)), 0, sh, f)

    def after(k, d, m, wicks):
        tip = blower(ctx, d['front'][0] + 30, d['front'][1], math.pi + 0.18, 0.9)
        if blast:
            wind(ctx, tip[0] - 10, tip[1], 200, TT - 120, il, 1.8, 6)
        if 26 <= il < 40:
            hx_, hy_ = m['head']
            cx_ = lerp(CX, hx_, eio(fly)); cy_ = lerp(TT, hy_ - m['R'] * 0.4, fly) - 360 * math.sin(math.pi * fly)
            cake(ctx, cx_, cy_, 0.8, (1,) * 5, -1, il, rot=-fly * 6.28, plate=False)
    party(ctx, f, il, kp, dp, mp, lit=(1,) * 5, bend=-0.8 if 18 <= il < 26 else 0, hats=(0, 0, 0), dad_frost=True,
          mom_cake=landed, cake_on=il < 26, tilt=0.35, after=after)
    ctx.restore()
    if il < 18:
        label2(ctx, "\"Step aside.", "PRO TIME.\"", WHITE, pop(il, 1, 5), 116, col2=YEL, y=1440)
    elif il < 40:
        label(ctx, "*VRRRRMMMM!*", 540, 600, 104, ORANGE, -0.04, pop(il, 18, 21))
    else:
        label(ctx, "*SPLAT!!*", 540, 600, 130, FROST, 0.05, pop(il, 40, 43))
        label(ctx, "\"...REALLY?\"", 540, 1440, 124, WHITE, -0.03, pop(il, 48, 51))


def s3(ctx, f):
    lf = f - 200
    if lf < 70:
        mega(ctx, f, lf)
    else:
        leaf_blower(ctx, f, lf - 70)


# ------------------------------------------------------------------ shot 4: twist
def gotcha(ctx, f, il):
    # il 0..60: kid holds up the TRICK CANDLES box, sly grin; push-in on kid
    lift = eout(pop(il, 4, 16))
    ctx.save(); cam(ctx, 470, 1100, 1.25 + 0.1 * eio(pop(il, 0, 60)), 0, 0, f)

    def after(k, d, m, wicks):
        bx, by = k['front']
        box(ctx, lerp(560, bx + 60, lift), lerp(TT + 200, by - 40, lift), 0.8, -0.1 * lift)
        if il >= 16:
            for j in range(3):
                sparkle(ctx, 300 + j * 130, k['head'][1] - k['R'] * 1.9 + 30 * (j % 2), 22 + 8 * math.sin(il * 0.6 + j), YEL)
    party(ctx, f, il, P(eye='smug', mouth='grin', lsh=30, lel=-40, rsh=110, rel=-60, head=-6),
          P(eye='shock', mouth='flat', lsh=20, lel=-20, rsh=20, rel=-20),
          P(eye='glare', mouth='flat', lsh=20, lel=-20, rsh=20, rel=-20),
          dad_frost=True, mom_cake=True, cake_on=False, tilt=0.35, after=after)
    ctx.restore()
    label2(ctx, "\"Hehe...", "GOTCHA!!\"", WHITE, pop(il, 18, 22), 124, col2=PINK, y=1440)


def its_on(ctx, f, il):
    # il 0..80: low-angle parents, glare -> evil grins
    evil = il >= 34
    ctx.save(); cam(ctx, 560, 1080, 1.08 + 0.08 * eio(pop(il, 0, 80)), -3, shake_at(il, [34], 8, 10), f)
    room(ctx, il, 0.35)
    rays(ctx, 560, 950, 200, 1600, il * 0.02, col=(1, 0.4, 0.5), a=0.22, n=16)
    m = draw(ctx, 330, GMOM - 186 * KMOM, KMOM, 1, MOM,
             P(eye='smug' if evil else 'glare', mouth='grin' if evil else 'flat', lsh=60, lel=-100, rsh=60, rel=-100))
    d = draw(ctx, 790, GDAD - 186 * KDAD, KDAD, -1, DAD,
             P(eye='smug' if evil else 'glare', mouth='grin' if evil else 'flat', lsh=60, lel=-100, rsh=60, rel=-100))
    frosting_face(ctx, d, 4)
    cake_on_head(ctx, m, il)
    table(ctx)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, (0.3, 0, 0.2, 0.12 if evil else 0)); ctx.fill()
    ctx.restore()
    if evil:
        label2(ctx, "\"Oh...", "it's ON.\"", WHITE, pop(il, 36, 40), 130, col2=RED, y=1440)


def s4(ctx, f):
    lf = f - 340
    if lf < 60:
        gotcha(ctx, f, lf)
        card(ctx, 'p2', lf, 0)
    else:
        its_on(ctx, f, lf - 60)


# ------------------------------------------------------------------ shot 5: payback
def new_cake(ctx, f, il):
    # il 0..80: sweet parents bring a NEW cake; kid blows; won't go out
    slide = eio(pop(il, 4, 22))
    bl = 40 <= il < 64
    shock = il >= 64
    kp = P(eye='happy', mouth='grin', lsh=60, lel=-110, rsh=60, rel=-110) if il < 40 else BLOWK
    if shock:
        kp = P(eye='shock', mouth='open', lsh=30, lel=-50, rsh=30, rel=-50)
    sweet = P(eye='happy', mouth='grin', lsh=30, lel=-40, rsh=40, rel=-60)
    ctx.save(); cam(ctx, 560, 1070, 1.0 + 0.06 * eio(pop(il, 0, 80)), 0, 0, f)

    def after(k, d, m, wicks):
        wk = cake(ctx, lerp(1300, CX, slide), TT, CS, (1,) * 5, 0.9 if bl else 0, il)
        if bl:
            mx, my = mouth_of(k)
            wind(ctx, mx + 40, my + 10, wk[2][0] + 40, wk[2][1] - 30, il, 1.0)
        for j in range(4):
            if 22 <= il < 40:
                sparkle(ctx, (200, 900)[j % 2] + 60 * (j // 2), 700 + 80 * (j // 2), 20 + 8 * math.sin(il * 0.6 + j), WHITE)
    party(ctx, f, il, kp, sweet, sweet, puff_amt=1.0 if bl else 0, cake_on=False, tilt=0.0, after=after)
    ctx.restore()
    if il < 40:
        label2(ctx, "\"Here's your REAL", "cake, sweetie!\"", WHITE, pop(il, 8, 12), 104, col2=PINK, y=1440)
    elif not shock:
        label(ctx, "*FWOOOOO!*", 540, 600, 100, CYAN, 0.04, pop(il, 40, 43))
    else:
        label(ctx, "\"...WAIT.\"", 540, 1440, 130, YEL, -0.03, pop(il, 64, 67))


def payback(ctx, f, il):
    # il 0..60: split screen: top parents with the giant box, bottom kid puffing at the cake
    ctx.save(); ctx.rectangle(0, 0, W, H / 2); ctx.clip()
    ctx.save(); cam(ctx, 560, 1060, 1.15, 0, 0, f, sy=H * 0.36)
    room(ctx, il)
    m = draw(ctx, 300, GMOM - 186 * KMOM, KMOM, 1, MOM, P(eye='smug', mouth='grin', lsh=120, lel=-40, rsh=60, rel=-90))
    d = draw(ctx, 820, GDAD - 186 * KDAD, KDAD, -1, DAD, P(eye='smug', mouth='grin', lsh=120, lel=-40, rsh=60, rel=-90))
    hat(ctx, *m['head'], m['R'], 0.12, YEL, PINK); hat(ctx, *d['head'], d['R'], -0.12, BLUE, YEL)
    box(ctx, 560, 1200 - 30 * eout(pop(il, 0, 10)), 1.05, 0.05, big=True)
    ctx.restore(); ctx.restore()
    ctx.save(); ctx.rectangle(0, H / 2, W, H / 2); ctx.clip()
    ctx.save(); cam(ctx, 520, 1130, 1.35, 0, 3, f, sy=H * 0.72)
    party(ctx, f, il, BLOWK, P(eye='happy', mouth='grin'), P(eye='happy', mouth='grin'), puff_amt=1.0, blow=1.0,
          bend=0.9 + 0.1 * math.sin(il * 0.7))
    ctx.restore(); ctx.restore()
    ctx.rectangle(0, H / 2 - 8, W, 16); setc(ctx, OUT); ctx.fill()
    label(ctx, "\"PAYBACK.\"", 540, 330, 130, RED, -0.04, pop(il, 6, 10))


def s5(ctx, f):
    lf = f - 480
    if lf < 80:
        new_cake(ctx, f, lf)
        card(ctx, 'p3', lf, 0, 30)
    elif lf < 140:
        payback(ctx, f, lf - 80)
    else:
        s1(ctx, f, f - 620)


SHOTS = [(0, s1), (54, s2), (200, s3), (340, s4), (480, s5)]
CUTS = (54, 124, 164, 200, 270, 340, 400, 480, 560, 620)


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
                              "-i", "out/trick_candles_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
