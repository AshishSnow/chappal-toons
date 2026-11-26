"""'The LEMONADE STAND'. Original, general-audience comedy short, 22s.
Hook:   sunny front-yard medium shot: kid on a crate behind a striped lemonade stand, arms waving, screaming
        "LEMONADE!! GET YOUR LEMONADE!!" + caption "THE LEMONADE STAND:".
Beat 1: wide: empty street, a leaf drifts by *cricket* "...anyone?" -> Dad steps out of the house "I'll take ONE!" ->
        kid sparkle-eyes "A CUSTOMER!!" *DING!* coin *clink*.
Beat 2: Dad sips -> the one close-up: *PUCKER!!* face, sour squiggles, hair spikes, "...SO... FRESH." ->
        kid proud "I used 40 LEMONS!"
Beat 3: kid "More SUGAR?" upends the whole bag *FWUMP!* -> Dad sips -> *BZZZT!* sugar rush -> Dutch-tilt zoom laps
        round the yard *ZOOOM!* "SO... GOOD!!!" -> slams coins "ANOTHER!!" *clink clink clink*
Twist:  kid hugs the full jar "SOLD OUT! I'M RICH!!" -> PLOT TWIST: DAD SENT THE BILL. -> a receipt unrolls to the
        grass "LEMONS... SUGAR..." "...CUPS... RENT." -> "...I OWE YOU?!" -> Dad strolls off with the jar *clink*
        -> kid climbs back up "LEMONADE!!" -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r
from scenes58 import sweat, twitch
from scenes65 import dog
from scenes84 import eio
import scenes13
from scenes13 import card as _card13

RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
LEMON = hx('ffe23a'); LEMON2 = hx('f2c200'); ADE = hx('fff3a0')
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff5fa8'), pants=hx('3d7bff'), shoes=hx('ffc93c'))
DAD = dict(doodle.DAD, shirt=hx('7fd0ff'), pants=hx('3a4a8a'))
N = 660
GND = 1600
SX = 1180            # stand centre
TOPY = 1430          # counter top
CRATE = 70           # kid stands on a crate
KKID, KDAD = 0.95, 1.05
CX, CY, CZ = 1190, 1300, 1.30
DOORX = 700
CUSTX = 1520         # where Dad stands to buy

CAPS = {'p1': [[("THE ", OUT), ("LEMONADE STAND:", ORANGE)]],
        'p2': [[("PLOT TWIST:", RED)], [("DAD ", BLUE), ("SENT THE BILL.", OUT)]]}
scenes13.CAPS = CAPS
card = _card13


def stand_ch(ctx, ch, x, k, p, f_=1, feet=GND):
    return draw(ctx, x, feet - 186 * k, k, f_, ch, p)


def ghost(ctx, a, fn):
    ctx.push_group(); fn(); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)


# ------------------------------------------------------------------ set: sunny front yard
def yard(ctx, lf):
    ctx.set_source(vgrad(ctx, 0, 300, 0, 1500, [(0, hx('6ec8ff')), (1, hx('d6f2ff'))]))
    ctx.rectangle(-3000, -3000, 9000, 9000); ctx.fill()
    # sun
    ctx.save(); ctx.translate(1700, 700); ctx.rotate(lf * 0.01)
    for k in range(12):
        a = k * math.pi / 6
        poly(ctx, [(math.cos(a - 0.12) * 110, math.sin(a - 0.12) * 110), (math.cos(a) * 175, math.sin(a) * 175),
                   (math.cos(a + 0.12) * 110, math.sin(a + 0.12) * 110)]); fl(ctx, hx('ffcf3a'), 3)
    ctx.restore()
    ellipse(ctx, 1700, 700, 95, 95); fl(ctx, hx('ffe45a'), 5)
    for sx in (-1, 1):
        ellipse(ctx, 1700 + sx * 32, 690, 8, 12); setc(ctx, INK); ctx.fill()
    ctx.new_path(); ctx.arc(1700, 712, 30, 0.3, math.pi - 0.3); ink(ctx, 5); ctx.stroke()
    for sx in (-1, 1):
        ellipse(ctx, 1700 + sx * 55, 725, 14, 8); setc(ctx, hx('ff9a8a')); ctx.fill()
    cloud(ctx, 760 + (lf * 0.4) % 200, 660, 0.9)
    cloud(ctx, 2150 - (lf * 0.3) % 200, 820, 0.7)
    # house (left)
    poly(ctx, [(240, 1060), (620, 780), (1000, 1060)]); fl(ctx, hx('ff7a5c'), 7)
    for j in range(4):
        ctx.move_to(330 + j * 30, 1060 - j * 70 + 0); ctx.line_to(910 - j * 30, 1060 - j * 70); setc(ctx, (0.7, 0.3, 0.25, 0.5)); ctx.set_line_width(4); ctx.stroke()
    ctx.rectangle(290, 1060, 660, 560); fl(ctx, hx('fff0c8'), 7)
    # door
    rect_r(ctx, DOORX - 75, 1290, 150, 310, 16); fl(ctx, hx('3fa0ff'), 6)
    ellipse(ctx, DOORX + 45, 1450, 10, 10); fl(ctx, GOLD, 3)
    rect_r(ctx, DOORX - 40, 1320, 80, 60, 10); fl(ctx, hx('bfe9ff'), 4)
    # window + flower box
    x, y = 360, 1160
    rect_r(ctx, x, y, 200, 170, 12); fl(ctx, hx('bfe9ff'), 6)
    ctx.move_to(x + 100, y); ctx.line_to(x + 100, y + 170); ctx.move_to(x, y + 85); ctx.line_to(x + 200, y + 85); ink(ctx, 5); ctx.stroke()
    rect_r(ctx, x - 14, y + 172, 228, 46, 8); fl(ctx, hx('c98a52'), 5)
    for k in range(5):
        ellipse(ctx, x + 10 + k * 46, y + 165, 20, 20); fl(ctx, (PINK, YEL, PURPLE, RED, ORANGE)[k], 3)
    # fence across the yard
    for k in range(-6, 26):
        xx = 980 + k * 70
        if 950 < xx or xx < 280:
            poly(ctx, [(xx - 26, 1560), (xx - 26, 1340), (xx, 1310), (xx + 26, 1340), (xx + 26, 1560)]); fl(ctx, WHITE, 4)
    rect_r(ctx, 950, 1380, 1600, 26, 4); fl(ctx, WHITE, 4)
    rect_r(ctx, 950, 1480, 1600, 26, 4); fl(ctx, WHITE, 4)
    # tree (right)
    rect_r(ctx, 1930, 1150, 70, 460, 14); fl(ctx, hx('a46a3a'), 6)
    for dx, dy, r in ((-120, 1080, 130), (110, 1060, 140), (0, 960, 160), (-40, 1150, 120), (90, 1170, 110)):
        ellipse(ctx, 1965 + dx, dy, r, r * 0.9); fl(ctx, GREEN, 6)
    for dx, dy in ((-80, 1000), (60, 950), (130, 1110), (-150, 1120)):
        ellipse(ctx, 1965 + dx, dy, 22, 22); fl(ctx, LEMON, 3)   # a lemon tree!
    # mailbox
    rect_r(ctx, 1715, 1420, 16, 180, 4); fl(ctx, hx('8a5a3a'), 3)
    rect_r(ctx, 1660, 1360, 120, 70, 30); fl(ctx, RED, 5)
    rect_r(ctx, 1770, 1330, 10, 50, 3); fl(ctx, GOLD, 3)
    # grass + sidewalk
    ctx.rectangle(-3000, GND - 40, 9000, 3000); setc(ctx, hx('7fd65a')); ctx.fill()
    ctx.move_to(-3000, GND - 40); ctx.line_to(6000, GND - 40); ink(ctx, 5); ctx.stroke()
    rnd = random.Random(7)
    for k in range(90):
        gx = rnd.uniform(-600, 2800); gy = rnd.uniform(GND - 20, GND + 420)
        ctx.move_to(gx, gy); ctx.line_to(gx - 6, gy - 22); ctx.move_to(gx, gy); ctx.line_to(gx + 8, gy - 18)
        setc(ctx, hx('4fb04a')); ctx.set_line_width(4); ctx.stroke()
    ctx.rectangle(-3000, GND + 160, 9000, 140); fl(ctx, hx('e6e0d6'), 5)
    for k in range(-20, 40):
        ctx.move_to(k * 220, GND + 160); ctx.line_to(k * 220 - 30, GND + 300); setc(ctx, (0.6, 0.55, 0.5, 0.5)); ctx.set_line_width(4); ctx.stroke()
    for fx_, col in ((960, PINK), (1010, YEL), (1820, PURPLE), (1870, RED), (240, ORANGE)):
        ctx.move_to(fx_, GND - 30); ctx.line_to(fx_, GND - 80); setc(ctx, hx('2f9a3a')); ctx.set_line_width(5); ctx.stroke()
        for a in range(5):
            ellipse(ctx, fx_ + 13 * math.cos(a * 1.256), GND - 90 + 13 * math.sin(a * 1.256), 10, 10); fl(ctx, col, 2)
        ellipse(ctx, fx_, GND - 90, 7, 7); fl(ctx, GOLD, 2)


# ------------------------------------------------------------------ props
def lemon(ctx, x, y, r=22, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ellipse(ctx, 0, 0, r, r * 0.78); fl(ctx, LEMON, 3)
    ellipse(ctx, r * 0.98, 0, r * 0.18, r * 0.14); fl(ctx, LEMON2, 2)
    ellipse(ctx, -r * 0.35, -r * 0.3, r * 0.22, r * 0.12, -0.5); setc(ctx, (1, 1, 1, 0.7)); ctx.fill()
    ctx.restore()


def pitcher(ctx, x, y, level=0.75, sugar=0.0):
    # y = bottom
    ctx.save()
    pts = [(x - 52, y), (x - 58, y - 150), (x - 40, y - 170), (x + 46, y - 170), (x + 58, y - 150), (x + 52, y)]
    poly(ctx, pts); ctx.save(); ctx.clip()
    ctx.rectangle(x - 70, y - 160 * level, 140, 200); setc(ctx, ADE if sugar < 0.5 else hx('fffbe6')); ctx.fill()
    for k in range(3):
        ctx.new_path(); ctx.arc(x - 25 + k * 25, y - 50 - k * 30, 14, 0, 2 * math.pi); setc(ctx, LEMON); ctx.fill()
    if sugar > 0:
        ctx.rectangle(x - 70, y - 160 * level - 10, 140, 60 * sugar); setc(ctx, (1, 1, 1, 0.95)); ctx.fill()
    ctx.restore()
    poly(ctx, pts); setc(ctx, (1, 1, 1, 0.25)); ctx.fill_preserve(); ink(ctx, 5); ctx.stroke()
    ctx.new_path(); ctx.arc(x + 62, y - 100, 34, -1.3, 1.3); ink(ctx, 7); ctx.stroke()
    ctx.move_to(x - 30, y - 140); ctx.line_to(x - 30, y - 30); setc(ctx, (1, 1, 1, 0.6)); ctx.set_line_width(7); ctx.stroke()
    ctx.restore()


def cup(ctx, x, y, a=0.0, full=True, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-22, -34), (22, -34), (16, 30), (-16, 30)]); fl(ctx, WHITE, 4)
    if full:
        poly(ctx, [(-19, -24), (19, -24), (15, 26), (-15, 26)]); setc(ctx, ADE); ctx.fill()
    ctx.move_to(-21, -10); ctx.line_to(21, -10); setc(ctx, PINK); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def jar(ctx, x, y, coins, s=1.0):
    # y = bottom
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rect_r(ctx, -42, -110, 84, 110, 18); setc(ctx, (0.85, 0.95, 1, 0.55)); ctx.fill()
    ctx.save(); rect_r(ctx, -42, -110, 84, 110, 18); ctx.clip()
    for i in range(int(coins)):
        cx_ = -26 + (i * 17) % 56; cy_ = -12 - (i // 4) * 11
        ellipse(ctx, cx_, cy_, 14, 7); fl(ctx, GOLD, 2)
    ctx.restore()
    rect_r(ctx, -42, -110, 84, 110, 18); ink(ctx, 5); ctx.stroke()
    rect_r(ctx, -34, -126, 68, 20, 6); fl(ctx, hx('ff8a5c'), 4)
    ctx.move_to(-26, -96); ctx.line_to(-26, -30); setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def coin(ctx, x, y, a=0.0):
    ellipse(ctx, x, y, 18 * max(0.2, abs(math.cos(a))), 18); fl(ctx, GOLD, 3)


def counter(ctx, lf, coins=1, level=0.75, sugar=0.0, show_pitcher=True, show_jar=True):
    """the stand front: posts, striped awning, counter with sign. Call AFTER drawing the kid."""
    x0, x1 = SX - 230, SX + 230
    for xx in (x0 + 16, x1 - 16):
        rect_r(ctx, xx - 12, 1080, 24, TOPY - 1080 + 10, 6); fl(ctx, hx('c98a52'), 4)
    # awning
    poly(ctx, [(x0 - 30, 1080), (x1 + 30, 1080), (x1 + 10, 1010), (x0 - 10, 1010)]); fl(ctx, WHITE, 5)
    for k in range(6):
        xa = x0 - 30 + k * (x1 - x0 + 60) / 6
        if k % 2 == 0:
            poly(ctx, [(xa, 1080), (xa + (x1 - x0 + 60) / 6, 1080), (xa + (x1 - x0 + 60) / 6 - 4, 1010), (xa + 4, 1010)]); fl(ctx, LEMON, 3)
    for k in range(6):
        xa = x0 - 30 + (k + 0.5) * (x1 - x0 + 60) / 6
        ctx.new_path(); ctx.arc(xa, 1080, (x1 - x0 + 60) / 12, 0, math.pi); fl(ctx, LEMON if k % 2 == 0 else WHITE, 4)
    # counter box
    rect_r(ctx, x0 - 20, TOPY - 18, x1 - x0 + 40, 30, 8); fl(ctx, hx('e0a35a'), 5)
    ctx.rectangle(x0, TOPY + 12, x1 - x0, GND - TOPY - 12); fl(ctx, hx('f4c88a'), 6)
    for k in range(1, 5):
        ctx.move_to(x0 + k * (x1 - x0) / 5, TOPY + 14); ctx.line_to(x0 + k * (x1 - x0) / 5, GND - 4); setc(ctx, (0.7, 0.45, 0.25, 0.5)); ctx.set_line_width(4); ctx.stroke()
    # sign
    ctx.save(); ctx.translate(SX, TOPY + 90); ctx.rotate(-0.03)
    rect_r(ctx, -175, -48, 350, 96, 14); fl(ctx, WHITE, 5)
    text(ctx, "LEMONADE", 22, 2, 50, ORANGE, ow=5, shadow=False)
    lemon(ctx, -138, 0, 24, 0.3)
    ctx.restore()
    for k in range(3):
        sparkle(ctx, SX - 150 + k * 150, TOPY + 30 + 140 * (k % 2) + 6 * math.sin(lf * 0.2 + k), 9, YEL)
    # items on the counter
    if show_pitcher:
        pitcher(ctx, SX - 120, TOPY - 16, level, sugar)
    for k in range(3):
        cup(ctx, SX + 30 + k * 4, TOPY - 50 - k * 14, 0, False)
    lemon(ctx, SX + 105, TOPY - 36, 20, 0.2); lemon(ctx, SX + 80, TOPY - 30, 18, -0.4)
    if show_jar:
        jar(ctx, SX + 175, TOPY - 16, coins)


def kid_behind(ctx, p, dx=0, up=0.0):
    return stand_ch(ctx, KID, SX + dx, KKID, p, 1, GND - CRATE - up)


def crate(ctx):
    pass   # hidden behind the counter


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = CZ + 0.04 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, CX, CY, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    yard(ctx, lf)
    w = 14 * math.sin(lf * 0.6)
    kid_behind(ctx, P(eye='happy', mouth='scream', lsh=150 + w, lel=-20, rsh=150 - w, rel=-20, head=4 * math.sin(lf * 0.6)))
    counter(ctx, lf, coins=0)
    dog(ctx, 1560, GND + 40, 0.42, -1, lf, sleep=True)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"LEMONADE!!", 540, 1385, 110, YEL, -0.04, t)
    label(ctx, "GET YOUR LEMONADE!!\"", 540, 1480, 84, WHITE, -0.04, t)


# ------------------------------------------------------------------ shot 2: no customers -> Dad
def beat1(ctx, f, il):
    # 0-40 empty street, leaf, cricket "...anyone?" ; 40-80 Dad steps out + walks "I'll take ONE!" ; 80-110 "A CUSTOMER!!" DING + coin
    pin = eio(pop(il, 80, 96))
    ctx.save(); cam(ctx, lerp(1150, 1300, pin), lerp(1300, 1320, pin), lerp(0.98, 1.34, pin), 0, shake_at(il, [82], 8, 9), f)
    yard(ctx, il)
    if il < 40:
        kp = P(eye='normal', mouth='frown', lsh=10, lel=-10, rsh=-10, rel=-10, head=-10, torso=-4)
    elif il < 80:
        kp = P(eye='shock', mouth='open', lsh=30, lel=-40, rsh=-10, rel=-10, head=6)
    else:
        b = 10 * math.sin(il * 0.8)
        kp = P(eye='happy', mouth='grin', lsh=160 + b, lel=-10, rsh=160 - b, rel=-10, head=4)
    kid_behind(ctx, kp, 0, 30 * abs(math.sin(il * 0.4)) if il >= 80 else 0)
    coins = 0 if il < 98 else 1
    counter(ctx, il, coins=coins)
    # leaf blowing across
    if il < 44:
        u = il / 44
        ctx.save(); ctx.translate(lerp(600, 1800, u), 1450 + 60 * math.sin(u * 9)); ctx.rotate(u * 8)
        ellipse(ctx, 0, 0, 30, 14); fl(ctx, ORANGE, 3); ctx.restore()
    # Dad
    if il >= 40:
        u = eio(pop(il, 44, 78))
        dx = lerp(DOORX, CUSTX, u)
        sw = 25 * math.sin(il * 0.7) * (u < 1)
        if il < 98:
            dp = P(eye='happy', mouth='open', lsh=sw if il < 78 else 60, lel=-20 if il < 78 else -120, rsh=-sw, rel=-20,
                   lhip=sw * 0.6, rhip=-sw * 0.6, head=6)
        else:
            dp = P(eye='happy', mouth='smile', lsh=12, lel=-15, rsh=70, rel=-90)
        d = stand_ch(ctx, DAD, dx, KDAD, dp, -1 if u > 0.05 else 1)
        if 88 <= il < 100:   # coin flies into the jar
            v = pop(il, 88, 98)
            coin(ctx, lerp(d['front'][0], SX + 175, v), lerp(d['front'][1], TOPY - 130, v) - 120 * math.sin(math.pi * v), il * 0.6)
    dog(ctx, 1560, GND + 40, 0.42, -1, il, sleep=True)
    ctx.restore()
    if il < 40:
        label(ctx, "*cricket*", 540, 520, 80, WHITE, 0.04, pop(il, 4, 8))
        label(ctx, "\"...anyone?\"", 540, 1430, 110, WHITE, -0.03, pop(il, 12, 16))
    elif il < 80:
        label(ctx, "\"I'll take ONE!\"", 540, 1430, 110, CYAN, 0.03, pop(il, 46, 50))
    else:
        label(ctx, "\"A CUSTOMER!!\"", 540, 1430, 116, YEL, -0.03, pop(il, 80, 84))
        label(ctx, "*DING!*", 540, 520, 100, GOLD, 0.05, pop(il, 98, 101))
        for k in range(5):
            sparkle(ctx, 300 + k * 120, 900 + 30 * math.sin(il * 0.4 + k), 18, YEL)


def s2(ctx, f):
    beat1(ctx, f, f - 60)


# ------------------------------------------------------------------ shot 3: the sip -> PUCKER close-up
def sour_fx(ctx, d, lf, amt):
    hx_, hy_ = d['head']; R = d['R']
    for k in range(8):   # sour squiggles
        a = k * math.pi / 4 + 0.2
        r0 = R * 1.25; r1 = R * (1.6 + 0.08 * math.sin(lf + k))
        ctx.new_path(); ctx.move_to(hx_ + r0 * math.cos(a), hy_ + r0 * math.sin(a))
        for j in range(1, 5):
            rr = lerp(r0, r1, j / 4); off = 0.08 * (-1) ** j
            ctx.line_to(hx_ + rr * math.cos(a + off), hy_ + rr * math.sin(a + off))
        setc(ctx, LEMON2[:3] + (amt,)); ctx.set_line_width(9); ctx.stroke()
    for k in range(7):   # hair stands up
        a = -math.pi / 2 + (k - 3) * 0.22
        ctx.new_path(); ctx.move_to(hx_ + R * 0.95 * math.cos(a), hy_ + R * 0.95 * math.sin(a))
        ctx.line_to(hx_ + R * (1.2 + 0.15 * amt) * math.cos(a), hy_ + R * (1.2 + 0.15 * amt) * math.sin(a))
        setc(ctx, INK); ctx.set_line_width(10); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def sip(ctx, f, il):
    # 0-25 medium: Dad sips ; 25-75 close-up PUCKER + "...SO... FRESH." ; 75-110 medium: kid "I used 40 LEMONS!"
    if 25 <= il < 75:
        jl = il - 25
        ctx.save(); cam(ctx, CUSTX - 10, 1250, 1.62 + 0.08 * eio(jl / 50), 2 * math.sin(jl * 0.3), shake_at(jl, [0], 14, 22) + (4 if jl < 24 else 0), f)
        yard(ctx, il); counter(ctx, il, coins=1)
        sh = 6 * math.sin(jl * 2.3) if jl < 26 else 0
        if jl < 26:
            dp = P(eye='closed', mouth='wavy', lsh=60, lel=-130, rsh=40, rel=-140, head=sh, torso=-4)
        else:
            dp = P(eye='closed', mouth='flat', lsh=12, lel=-15, rsh=70, rel=-100, head=-4)
        d = stand_ch(ctx, DAD, CUSTX + sh * 0.5, KDAD, dp, -1)
        if jl < 26:
            sour_fx(ctx, d, jl, 1 - 0.3 * pop(jl, 14, 26))
            ctx.save(); ellipse(ctx, d['head'][0], d['head'][1], d['R'] * 1.05, d['R'] * 1.05); setc(ctx, (0.9, 1, 0.2, 0.22 * (1 - pop(jl, 14, 26)))); ctx.fill(); ctx.restore()
        else:
            twitch(ctx, d['head'][0] + d['R'] * 0.7, d['head'][1] - d['R'] * 0.8, jl, 1.2)
            sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.5, jl, 1.0)
        cup(ctx, d['front'][0], d['front'][1] - 20, -0.2, jl >= 26)
        ctx.restore()
        if jl < 26:
            label(ctx, "*PUCKER!!*", 540, 520, 140, LEMON, -0.05, pop(jl, 0, 3))
        else:
            label(ctx, "\"...SO...", 540, 1385, 110, WHITE, -0.03, pop(jl, 27, 31))
            label(ctx, "...FRESH.\"", 540, 1480, 120, LEMON, 0.03, pop(jl, 36, 40))
        return
    ctx.save(); cam(ctx, 1300, 1320, 1.34 if il < 25 else 1.3, 0, 0, f)
    yard(ctx, il)
    if il < 25:
        kp = P(eye='happy', mouth='grin', lsh=150, lel=-20, rsh=20, rel=-60)
    else:
        kp = P(eye='smug', mouth='grin', lsh=-40, lel=-110, rsh=-40, rel=-110, head=-8)
    kid_behind(ctx, kp)
    counter(ctx, il, coins=1)
    if il < 25:
        dp = P(eye='happy', mouth='smile', lsh=12, lel=-15, rsh=70 + 40 * pop(il, 0, 12), rel=-120 - 20 * pop(il, 0, 12), head=-14 * pop(il, 6, 16))
    else:
        dp = P(eye='closed', mouth='wavy', lsh=12, lel=-15, rsh=70, rel=-100, head=-4)
    d = stand_ch(ctx, DAD, CUSTX, KDAD, dp, -1)
    cup(ctx, d['front'][0], d['front'][1] - 20, -0.5 * pop(il, 6, 16) if il < 25 else -0.2, il < 25)
    if il >= 75:
        sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.5, il, 1.0)
        for k in range(4):
            lemon(ctx, SX - 180 + k * 40, 1180 - 20 * abs(math.sin(il * 0.3 + k)), 18, k)
    dog(ctx, 1560 + 150, GND + 40, 0.42, -1, il, sleep=True)
    ctx.restore()
    if il < 25:
        label(ctx, "*sip*", 540, 520, 90, WHITE, 0.04, pop(il, 8, 12))
    else:
        label(ctx, "\"I used 40 LEMONS!\"", 540, 1430, 100, LEMON, -0.03, pop(il, 77, 81))


def s3(ctx, f):
    sip(ctx, f, f - 170)


# ------------------------------------------------------------------ shot 4: SUGAR -> sugar rush
def sugar_bag(ctx, x, y, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    poly(ctx, [(-60, -80), (60, -80), (70, 90), (-70, 90)]); fl(ctx, WHITE, 5)
    text(ctx, "SUGAR", 0, 10, 34, BLUE, ow=4, shadow=False)
    ctx.move_to(-60, -60); ctx.line_to(60, -60); setc(ctx, PINK); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()


LAP = [(1520, 0), (1780, -40), (1880, -10), (1650, 30), (950, 10), (760, -30), (950, -20), (1520, 0)]


def lap_pos(u):
    n = len(LAP) - 1; s = clamp(u) * n; i = min(int(s), n - 1); t = s - i
    return lerp(LAP[i][0], LAP[i + 1][0], t), lerp(LAP[i][1], LAP[i + 1][1], t), (1 if LAP[i + 1][0] > LAP[i][0] else -1)


def rush(ctx, f, il):
    # 0-35 kid upends the sugar bag FWUMP ; 35-50 Dad sips, BZZZT ; 50-100 zoom laps (Dutch) ; 100-120 "ANOTHER!!" coins
    if 50 <= il < 100:
        jl = il - 50
        u = eio(jl / 44)
        ctx.save(); cam(ctx, 1300, 1260, 0.82, -7, 4, f)
        yard(ctx, il)
        kid_behind(ctx, P(eye='shock', mouth='open', lsh=40, lel=-40, rsh=-40, rel=-40, head=-6))
        counter(ctx, il, coins=1, level=0.4, sugar=1)
        for g in range(4, 0, -1):   # motion ghosts
            x, yy, fd = lap_pos(eio(max(0, (jl - g * 2) / 44)))
            ghost(ctx, 0.12 * (5 - g), lambda x=x, yy=yy, fd=fd: stand_ch(ctx, DAD, x, KDAD, P(eye='shock', mouth='grin', lsh=-70, lel=0, rsh=-70, rel=0, torso=20, lhip=50, lkn=-60, rhip=-40, rkn=-10), fd, GND + yy))
        x, yy, fd = lap_pos(u)
        for k in range(6):
            ctx.move_to(x - fd * (90 + k * 30), 1300 + k * 40 + yy); ctx.line_to(x - fd * (300 + k * 50), 1300 + k * 40 + yy)
            setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(8); ctx.stroke()
        sp = 40 * math.sin(jl * 1.3)
        d = stand_ch(ctx, DAD, x, KDAD, P(eye='shock', mouth='grin', lsh=-70, lel=0, rsh=-70, rel=0, torso=20, lhip=50 + sp, lkn=-60, rhip=-40 - sp, rkn=-10), fd, GND + yy)
        dog(ctx, 1700, GND + 40, 0.42, -1, il)
        ctx.restore()
        label(ctx, "*ZOOOOM!*", 540, 520, 130, CYAN, -0.05, pop(jl, 0, 3))
        label(ctx, "\"SO... GOOD!!!\"", 540, 1430, 120, YEL, 0.03, pop(jl, 14, 18))
        return
    ctx.save(); cam(ctx, 1300, 1310, 1.36, 0, shake_at(il, [20, 40, 100, 106, 112], 8, 14), f)
    yard(ctx, il)
    pour = pop(il, 14, 30)
    if il < 35:
        kp = P(eye='happy', mouth='grin', lsh=-30, lel=-120, rsh=150, rel=-30, head=-6)
    else:
        kp = P(eye='shock', mouth='open', lsh=40, lel=-40, rsh=-40, rel=-40, head=-6)
    k_ = kid_behind(ctx, kp)
    sug = min(1, pour * 1.3) if il >= 14 else 0
    counter(ctx, il, coins=1 + (0 if il < 100 else min(9, (il - 100) // 2 * 3)), level=0.75 - 0.35 * (il >= 40), sugar=sug)
    if il < 35:
        bx, by = SX - 120, TOPY - 260
        sugar_bag(ctx, bx, by, -2.5 * eio(pop(il, 6, 16)))
        if 14 <= il < 32:
            for k in range(26):
                rr = random.Random(k * 7 + il)
                ellipse(ctx, bx + rr.uniform(-40, 40), by + 60 + rr.uniform(0, 120), 6, 6); fl(ctx, WHITE, 2)
        if 20 <= il < 35:   # sugar cloud
            v = pop(il, 20, 35)
            for k in range(7):
                ellipse(ctx, SX - 120 + 120 * math.cos(k) * v, TOPY - 200 - 60 * v + 40 * math.sin(k * 2), 50 + 30 * v, 40 + 20 * v)
                setc(ctx, (1, 1, 1, 0.8 * (1 - v))); ctx.fill()
    # Dad
    if il < 35:
        dp = P(eye='shock', mouth='wavy', lsh=12, lel=-15, rsh=60, rel=-100, head=-4)
    elif il < 50:
        dp = P(eye='shock' if il >= 42 else 'closed', mouth='grin' if il >= 42 else 'smile', lsh=12, lel=-15, rsh=110, rel=-120, head=-10 if il < 42 else 0)
    else:
        dp = P(eye='happy', mouth='scream', lsh=150, lel=-20, rsh=60 + 30 * math.sin(il * 1.5), rel=-120, head=4)
    vib = 7 * math.sin(il * 3.1) if il >= 42 else 0
    d = stand_ch(ctx, DAD, CUSTX + vib, KDAD, dp, -1)
    if il < 50:
        cup(ctx, d['front'][0], d['front'][1] - 20, -0.4 if 35 <= il < 42 else -0.1, il < 42)
    if il >= 42 and il < 50:
        for k in range(4):
            a = k * 1.57 + il * 0.5
            ctx.new_path(); ctx.arc(d['head'][0] + 140 * math.cos(a), d['head'][1] - 120 + 40 * math.sin(a), 18, 0, 6); setc(ctx, YEL); ctx.fill()
    if il >= 100:
        for k in range(3):
            v = pop(il, 100 + k * 6, 106 + k * 6)
            if 0 < v < 1:
                coin(ctx, lerp(d['front'][0], SX + 175, v), lerp(d['front'][1], TOPY - 130, v) - 120 * math.sin(math.pi * v), il * 0.6)
    dog(ctx, 1700, GND + 40, 0.42, -1, il, sleep=il < 40)
    ctx.restore()
    if il < 35:
        label(ctx, "\"More SUGAR?\"", 540, 1430, 110, WHITE, -0.03, pop(il, 2, 6))
        if il >= 20:
            label(ctx, "*FWUMP!*", 540, 520, 120, WHITE, 0.05, pop(il, 20, 23))
    elif il < 50:
        label(ctx, "*gulp*", 540, 520, 90, WHITE, -0.04, pop(il, 36, 39))
        if il >= 42:
            label(ctx, "*BZZZT!*", 540, 1430, 130, YEL, 0.04, pop(il, 42, 45))
    else:
        label(ctx, "\"ANOTHER!!\"", 540, 1430, 130, CYAN, -0.03, pop(il, 100, 103))
        label(ctx, "*clink clink clink*", 540, 520, 80, GOLD, 0.04, pop(il, 104, 108))


def s4(ctx, f):
    rush(ctx, f, f - 280)


# ------------------------------------------------------------------ shot 5: rich -> the bill -> loop
def receipt(ctx, x, y, length, lf):
    # hangs from (x, y) down to the grass and piles up
    drop = min(length, GND + 20 - y)
    ctx.save()
    ctx.rectangle(x - 60, y, 120, drop); fl(ctx, WHITE, 4)
    rnd = random.Random(1)
    for k in range(int(drop // 30)):
        w_ = rnd.uniform(30, 70)
        ctx.move_to(x - 44, y + 22 + k * 30); ctx.line_to(x - 44 + w_, y + 22 + k * 30); setc(ctx, (0.5, 0.5, 0.55, 0.8)); ctx.set_line_width(5); ctx.stroke()
        ctx.move_to(x + 20, y + 22 + k * 30); ctx.line_to(x + 44, y + 22 + k * 30); ctx.stroke()
    extra = length - drop
    if extra > 0:   # pile of curls on the grass
        n = int(extra // 60) + 1
        for k in range(min(n, 9)):
            ellipse(ctx, x - 90 + (k * 67) % 180, GND + 10 - 24 * (k // 3), 50, 22, 0.1 * (-1) ** k); fl(ctx, WHITE, 4)
            ellipse(ctx, x - 90 + (k * 67) % 180, GND + 10 - 24 * (k // 3), 30, 11, 0.1 * (-1) ** k); setc(ctx, (0.85, 0.85, 0.88)); ctx.fill()
    ctx.restore()


def finale(ctx, f, il):
    # 0-45 kid hugs full jar "SOLD OUT!" "I'M RICH!!" ; 45 card ; 50-130 receipt unrolls ; 130-170 "...I OWE YOU?!" ;
    # 170-200 Dad strolls off with the jar *clink* ; 200-230 kid climbs back up -> hook
    zin = eio(pop(il, 130, 140)) - eio(pop(il, 168, 176))
    ctx.save(); cam(ctx, lerp(1300, 1370, zin), lerp(1290, 1250, zin), lerp(1.24, 1.5, zin), 0, shake_at(il, [0, 130], 8, 12), f)
    yard(ctx, il)
    has_jar = il < 176
    if il < 45:
        b = 8 * math.sin(il * 0.9)
        kp = P(eye='happy', mouth='grin', lsh=60 + b, lel=-120, rsh=60 - b, rel=-120, head=6 * math.sin(il * 0.5))
    elif il < 130:
        kp = P(eye='normal', mouth='open' if il < 90 else 'wavy', lsh=60, lel=-120, rsh=60, rel=-120, head=-12 * pop(il, 50, 70))
    elif il < 176:
        kp = P(eye='shock', mouth='scream', lsh=150, lel=-20, rsh=150, rel=-20, head=4)
    elif il < 200:
        kp = P(eye='shock', mouth='frown', lsh=20, lel=-40, rsh=-20, rel=-40, head=-10)
    else:
        u = pop(il, 200, 222)
        kp = P(eye='glare', mouth='flat' if il < 214 else 'scream', lsh=lerp(20, 150, u), lel=-20, rsh=lerp(-20, 150, u), rel=-20)
    kd = kid_behind(ctx, kp, 0, 40 * eio(pop(il, 200, 214)) - 40 * eio(pop(il, 222, 230)) if il >= 200 else 0)
    counter(ctx, il, coins=24, level=0.15, sugar=1, show_jar=False)
    if has_jar and il < 176:
        if il < 160:
            jx, jy = SX + 60, TOPY - 14
        else:
            v = eio(pop(il, 160, 176)); jx, jy = lerp(SX + 60, CUSTX - 70, v), lerp(TOPY - 14, 1340, v)
        jar(ctx, jx, jy, 24, 1.25)
        if il < 45:
            for k in range(6):
                sparkle(ctx, jx - 90 + k * 36, jy - 170 - 20 * abs(math.sin(il * 0.3 + k)), 16, YEL)
    # Dad
    if il < 176:
        dx = CUSTX
        if il < 50:
            dp = P(eye='normal', mouth='smile', lsh=12, lel=-15, rsh=12, rel=-15)
        elif il < 160:
            dp = P(eye='smug', mouth='smile', lsh=12, lel=-15, rsh=95, rel=-60, head=4)
        else:
            dp = P(eye='smug', mouth='grin', lsh=12, lel=-15, rsh=90, rel=-90)
        d = stand_ch(ctx, DAD, dx, KDAD, dp, -1)
        if 50 <= il < 160:
            hx_, hy_ = d['front']
            receipt(ctx, hx_ - 10, hy_ - 10, 900 * eio(pop(il, 52, 125)), il)
    else:
        u = eio(pop(il, 176, 230))
        dx = lerp(CUSTX, 2350, u)
        sw = 25 * math.sin(il * 0.7)
        d = stand_ch(ctx, DAD, dx, KDAD, P(eye='happy', mouth='smile', lsh=sw, lel=-20, rsh=90, rel=-90, lhip=sw * 0.6, rhip=-sw * 0.6, head=6), 1)
        jar(ctx, d['front'][0] + 10, d['front'][1] + 30, 24, 1.0)
    dog(ctx, 1760, GND + 40, 0.42, -1, il, sleep=True)
    ctx.restore()
    if 45 <= il < 130:
        card(ctx, 'p2', il, 46)
    if il < 45:
        label(ctx, "\"SOLD OUT!", 540, 1385, 110, YEL, -0.03, pop(il, 2, 6))
        label(ctx, "I'M RICH!!\"", 540, 1480, 120, GOLD, -0.03, pop(il, 10, 14))
    elif il < 130:
        if il >= 62:
            label(ctx, "\"LEMONS... SUGAR...", 540, 1385, 84, WHITE, -0.03, pop(il, 62, 66))
        if il >= 92:
            label(ctx, "...CUPS... RENT.\"", 540, 1480, 96, CYAN, 0.03, pop(il, 92, 96))
    elif il < 176:
        label(ctx, "\"...I OWE YOU?!\"", 540, 1430, 130, PINK, -0.03, pop(il, 130, 133))
    elif il < 200:
        label(ctx, "*clink clink*", 540, 520, 80, GOLD, 0.04, pop(il, 178, 182))
        label(ctx, "\"Pleasure doing business!\"", 540, 1430, 80, WHITE, -0.03, pop(il, 180, 184))
    else:
        label(ctx, "*deep breath*", 540, 1430, 90, WHITE, 0.03, pop(il, 202, 206))


def s5(ctx, f):
    lf = f - 400
    if lf < 230:
        finale(ctx, f, lf)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (170, s3), (280, s4), (400, s5)]
CUTS = (60, 170, 195, 245, 280, 330, 380, 400, 630)


def render(f):
    import sketch
    sketch.BOIL[0] = f // 4
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.1, 0.05, 0.15, 0.16)
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
                              "-i", "out/lemonade_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
