"""'THANKSGIVING LEFTOVERS'. Original, general-audience comedy short, 22s.
Hook:   dining-room medium shot: Dad behind the table holding up yet another turkey sandwich, screaming
        "TURKEY... AGAIN?!" + caption 'THANKSGIVING LEFTOVERS:'; the still-huge turkey on the platter, Mom beaming, kid
        slumped on the table, dog watching.
Beat 1: Dutch-tilt push-in day montage: DAY 2 Mom "Turkey SANDWICH!" *DING* Dad "YUM!" -> DAY 3 "Turkey SOUP!" *slurp*
        "...yum." -> DAY 4 "Turkey PANCAKES!" *flip* Dad + kid "PANCAKES?!"
Beat 2: DAY 5: Mom presents "Turkey ICE CREAM!" -> kid *BLEH!*; midnight: POV from INSIDE the fridge, the door opens on
        sneaky Dad "Midnight SNACK..." -> every shelf is turkey *AHHH~* -> "...it's MULTIPLYING?!"
Beat 3: the one close-up in the fridge glow: "It's... NEVER..." "...ENDING!!" -> under the table Dad slips his plate to
        the dog, the dog is round as a ball *BURP!* and nudges it back "...even the DOG?!"
Twist:  *DING-DONG!* Grandma bursts in hugging a turkey bigger than her "I brought LEFTOVERS!" -> PLOT TWIST: GRANDMA
        BROUGHT HERS TOO. -> *THUD!!* plates jump -> Dad twitch "...TURKEY..." -> hook loop "TURKEY... AGAIN?!"."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face, rays
from scenes58 import sweat, twitch
from scenes65 import dog
from scenes84 import eio
import scenes96
from scenes96 import room, table, turkey, FLOOR, GND, TB0, TB1, TTOP, TFR, TX, TY, DADX, MOMX, KIDX, KDAD, KMOM, KKID
import scenes13
from scenes13 import card as _card13

RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
BREAD = hx('f5c27a'); CRUST = hx('c98a42'); MEAT = hx('f0c9a0')
DAD = dict(doodle.DAD, shirt=hx('ff8a3d'), pants=hx('3a4a8a'))
DAD_PJ = dict(DAD, shirt=hx('7fb8ff'), pants=hx('5a7ad8'))
MOM = dict(doodle.MOM_G, shirt=hx('2fb8a8'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('8a3cff'), pants=hx('3d7bff'), shoes=hx('ffc93c'))
GRAN = dict(doodle.NMOM, hair=hx('e4e4ee'), shirt=hx('ff7aa8'), pants=hx('8a3cff'), glasses=hx('8a3cff'))
N = 660
PX, PY = DADX + 10, TTOP + 26        # Dad's plate

CAPS = {'p1': [[("THANKSGIVING ", ORANGE)], [("LEFTOVERS:", OUT)]],
        'p2': [[("PLOT TWIST:", RED)], [("GRANDMA BROUGHT ", OUT), ("HERS TOO.", PURPLE)]]}
scenes13.CAPS = CAPS
card = _card13


def stand(ctx, ch, x, k, p, f_=1, dy=0):
    return draw(ctx, x, GND - 186 * k + dy, k, f_, ch, p)


# ------------------------------------------------------------------ dishes
def sandwich(ctx, x, y, s=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    poly(ctx, [(-70, 30), (70, 30), (0, -80)]); fl(ctx, BREAD, 4)
    ctx.new_path(); ctx.move_to(-78, 8); ctx.curve_to(-40, -6, 40, -6, 78, 8); ctx.line_to(70, 24); ctx.line_to(-70, 24); ctx.close_path(); fl(ctx, MEAT, 3)
    for k in range(5):
        ellipse(ctx, -60 + k * 30, 2 + 4 * (k % 2), 16, 8, 0.3 * k); fl(ctx, hx('7fd65a'), 2)
    poly(ctx, [(-74, 4), (74, 4), (0, -96)]); fl(ctx, BREAD, 4)
    poly(ctx, [(-56, -4), (56, -4), (0, -80)]); setc(ctx, hx('ffe0a8')); ctx.fill()
    ctx.restore()


def plate(ctx, x, y, s=1.0):
    ellipse(ctx, x, y, 110 * s, 22 * s); fl(ctx, WHITE, 4)
    ellipse(ctx, x, y - 2 * s, 80 * s, 14 * s); ctx.set_line_width(2.5); setc(ctx, hx('9fd8ff')); ctx.stroke()


def soup(ctx, x, y, s=1.0, lf=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-90, -30); ctx.curve_to(-90, 40, 90, 40, 90, -30); ctx.close_path(); fl(ctx, hx('ff8aa8'), 4)
    ellipse(ctx, 0, -30, 90, 20); fl(ctx, hx('f0b04a'), 4)
    for dx in (-40, 6, 44):
        ellipse(ctx, dx, -30, 14, 6); fl(ctx, MEAT, 2)
    ellipse(ctx, -14, -26, 7, 4); fl(ctx, ORANGE, 2)
    for k in range(3):   # steam
        ox = -40 + k * 40; ph = lf * 0.15 + k
        ctx.new_path(); ctx.move_to(ox, -60)
        ctx.curve_to(ox + 18 * math.sin(ph), -90, ox - 18 * math.sin(ph), -120, ox, -150); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(7); ctx.stroke()
    ctx.restore()


def drumstick(ctx, x, y, s=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rect_r(ctx, -9, -90, 18, 50, 6); fl(ctx, hx('fff6e8'), 3)
    for k in range(5):
        ellipse(ctx, -12 + k * 6, -94, 7, 10); fl(ctx, WHITE, 2)
    ellipse(ctx, 0, 0, 34, 50); fl(ctx, hx('d9944e'), 4)
    ellipse(ctx, -10, -14, 10, 18, 0.2); setc(ctx, (1, 1, 1, 0.4)); ctx.fill()
    ctx.restore()


def pancakes(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for k in range(4):
        ellipse(ctx, 0, -k * 26, 90, 22); fl(ctx, hx('f2b25a'), 4)
        ellipse(ctx, 0, -k * 26 - 6, 82, 14); setc(ctx, hx('ffd08a')); ctx.fill()
    ctx.new_path(); ctx.move_to(-60, -84); ctx.curve_to(-30, -60, 30, -60, 60, -84); ctx.line_to(30, -60); ctx.curve_to(26, -40, 14, -40, 12, -60)
    ctx.close_path(); fl(ctx, hx('a8642e'), 3)   # gravy drip
    ctx.restore()
    drumstick(ctx, x + 10 * s, y - 120 * s, 0.9 * s, 0.25)


def cone(ctx, x, y, s=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    poly(ctx, [(-50, 0), (50, 0), (0, 150)]); fl(ctx, hx('e8a85a'), 4)
    for k in range(-2, 3):
        ctx.move_to(-40 + k * 24, 0); ctx.line_to(k * 10 + 20, 120)
    setc(ctx, dark(hx('e8a85a'), 0.8)); ctx.set_line_width(3); ctx.stroke()
    ellipse(ctx, 0, -30, 62, 48); fl(ctx, hx('f3e0c0'), 4)
    ellipse(ctx, 0, -86, 48, 40); fl(ctx, hx('f3e0c0'), 4)
    ctx.new_path(); ctx.move_to(-46, -96); ctx.curve_to(-20, -70, 20, -70, 46, -96); ctx.line_to(30, -74); ctx.curve_to(26, -50, 14, -50, 10, -72)
    ctx.close_path(); fl(ctx, hx('a8642e'), 3)
    ctx.restore()
    drumstick(ctx, x + 6 * s, y - 150 * s, 0.85 * s, 0.35 + rot)


def gravy_boat(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-50, -20); ctx.curve_to(-50, 20, 40, 20, 50, -20); ctx.line_to(80, -36); ctx.line_to(40, -26); ctx.close_path(); fl(ctx, WHITE, 4)
    ellipse(ctx, -6, -20, 44, 8); fl(ctx, hx('a8642e'), 2)
    ctx.restore()


def round_dog(ctx, x, y, s, lf, burp=0.0):
    """over-stuffed dog: big round belly"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    fur = hx('e8b878')
    ellipse(ctx, 0, -120, 170, 130); fl(ctx, fur, 6)
    ellipse(ctx, 0, -90, 110, 80); setc(ctx, hx('f8dcae')); ctx.fill()
    for sx in (-1, 1):
        ellipse(ctx, sx * 90, -10, 34, 20); fl(ctx, hx('b9844a'), 4)
    ctx.restore()
    dog(ctx, x + 60 * s, y - 120 * s, s * 0.95, -1, lf)
    ellipse(ctx, x, y - 120 * s, 168 * s, 128 * s); fl(ctx, fur, 6)   # belly over the dog's body
    ellipse(ctx, x + 10 * s, y - 90 * s, 100 * s, 70 * s); setc(ctx, hx('f8dcae')); ctx.fill()
    for sx in (-1, 1):
        ellipse(ctx, x + sx * 90 * s, y - 10 * s, 34 * s, 20 * s); fl(ctx, hx('b9844a'), 4)


def thought_steam(ctx, x, y, lf, a=1.0):
    for k in range(3):
        ox = x - 40 + k * 40; ph = lf * 0.15 + k
        ctx.new_path(); ctx.move_to(ox, y)
        ctx.curve_to(ox + 18 * math.sin(ph), y - 30, ox - 18 * math.sin(ph), y - 60, ox, y - 90); setc(ctx, (1, 1, 1, 0.8 * a)); ctx.set_line_width(7); ctx.stroke()


# ------------------------------------------------------------------ shot 1: hook
def dinner(ctx, lf, dp, dish='sandwich', mp=None, kp=None, kid_dy=-70, dish_s=1.0, turkey_s=1.0, jump=0.0, hold=True):
    room(ctx, lf)
    m = stand(ctx, MOM, MOMX, KMOM, mp or P(eye='happy', mouth='grin', lsh=30, lel=-60, rsh=120, rel=-50), 1)
    k = stand(ctx, KID, KIDX, KKID, kp or P(eye='closed', mouth='wavy', torso=-30, head=-20, lsh=150, lel=-40, rsh=150, rel=-40), -1, kid_dy)
    d = stand(ctx, DAD, DADX, KDAD, dp, 1)
    table(ctx, lf, jump)
    turkey(ctx, TX + 60, TY - 26 * jump, turkey_s)
    plate(ctx, PX, PY - 26 * jump)
    if dish == 'sandwich' and hold:
        hx_, hy = d['front']
        sandwich(ctx, hx_, hy - 30, 0.95, -0.2)
    elif dish == 'sandwich':
        sandwich(ctx, PX, PY - 4, dish_s)
    elif dish == 'soup':
        soup(ctx, PX, PY - 10, dish_s, lf)
    elif dish == 'pancakes':
        pancakes(ctx, PX, PY - 8, dish_s)
    gravy_boat(ctx, m['front'][0] + 10, m['front'][1], 0.9)
    return d, m, k


def hook(ctx, f, lf):
    z = 1.12 + 0.04 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, 1110, 1200, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    sh = math.sin(lf * 1.6) * 8
    dp = P(eye='shock', mouth='scream', rsh=150 + sh, rel=-30, lsh=150 - sh, lel=30, head=-6)
    d, m, k = dinner(ctx, lf, dp)
    sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.5, lf, 1.0)
    dog(ctx, 1640, GND + 8, 0.6, -1, lf)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"TURKEY...", 540, 1360, 110, WHITE, -0.04, t)
    label(ctx, "AGAIN?!\"", 540, 1470, 150, ORANGE, 0.03, t)


# ------------------------------------------------------------------ shot 2: day montage
DAYS = [(0, "DAY 2:", 'sandwich', "\"Turkey SANDWICH!\"", "\"YUM!\""),
        (46, "DAY 3:", 'soup', "\"Turkey SOUP!\"", "\"...yum.\""),
        (92, "DAY 4:", 'pancakes', "\"Turkey PANCAKES!\"", "\"PANCAKES?!\"")]


def montage(ctx, f, il):
    i = 0 if il < 46 else (1 if il < 92 else 2)
    t0, day, dish, mom_line, dad_line = DAYS[i]
    l = il - t0
    rot = (-6, 6, -6)[i]
    z = 1.22 + 0.06 * eio(l / 46) + 0.08 * i
    ctx.save(); cam(ctx, 1010, 1200, z, rot, shake_at(l, [6], 10, 6), f)
    ds = max(0.03, eout(pop(l, 4, 9)))
    mp = P(eye='happy', mouth='open', lsh=30, lel=-60, rsh=100 - 30 * pop(l, 0, 8), rel=-20, torso=10)
    if i == 0:
        dp = P(eye='happy' if l >= 20 else 'normal', mouth='grin' if l >= 20 else 'smile', rsh=160 if l >= 20 else 20, rel=-20, lsh=20, lel=-20)
        kp = None
    elif i == 1:
        dp = P(eye='normal', mouth='flat', rsh=20, rel=-60, lsh=20, lel=-20, head=8)
        kp = None
    else:
        dp = P(eye='shock', mouth='scream', rsh=150, rel=-30, lsh=150, lel=30)
        kp = P(eye='shock', mouth='scream', lsh=150, lel=-30, rsh=150, rel=-30)
    d, m, k = dinner(ctx, il, dp, dish, mp, kp, -70 if kp is None else 0, ds, hold=False)
    if 6 <= l < 18:
        sparkle(ctx, PX + 90, PY - 120, 34 * (1 - pop(l, 6, 18)) + 8, YEL)
    if i == 1:
        thought_steam(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 1.0, il, 0)
    dog(ctx, 1640, GND + 8, 0.6, -1, il)
    ctx.restore()
    label(ctx, day, 540, 520, 120, GOLD, -0.04, pop(l, 0, 3))
    label(ctx, mom_line, 540, 1330, 96, MINT, -0.03, pop(l, 4, 8))
    if l >= 22:
        label(ctx, dad_line, 540, 1480, 130 if i != 1 else 110, ORANGE if i != 1 else WHITE, 0.03, pop(l, 22, 25))
    sfx = ("*DING!*", "*slurp*", "*flip flip!*")[i]
    if 6 <= l < 22:
        label(ctx, sfx, 820, 700, 70, WHITE, 0.08, pop(l, 6, 9))


def s2(ctx, f):
    montage(ctx, f, f - 60)


# ------------------------------------------------------------------ shot 3: ice cream -> fridge POV
def ice_cream(ctx, f, il):
    # 0..50: DAY 5 Mom shows the cone ; 26 kid *BLEH!*
    z = 1.2 + 0.05 * eio(il / 50)
    ctx.save(); cam(ctx, 1040, 1200, z, 3, shake_at(il, [26], 10, 8), f)
    mp = P(eye='happy', mouth='grin', lsh=30, lel=-60, rsh=150, rel=-10, torso=8)
    if il < 26:
        kp = P(eye='normal', mouth='flat', lsh=20, lel=-30, rsh=20, rel=-30)
    else:
        kp = P(eye='closed', mouth='wavy', lsh=150, lel=-150, rsh=150, rel=-150, torso=-10)
    dp = P(eye='shock' if il >= 14 else 'normal', mouth='open' if il >= 14 else 'flat', rsh=20, rel=-40, lsh=20, lel=-20, head=6)
    room(ctx, il)
    m = stand(ctx, MOM, MOMX, KMOM, mp, 1)
    k = stand(ctx, KID, KIDX, KKID, kp, -1, 0)
    d = stand(ctx, DAD, DADX, KDAD, dp, 1)
    table(ctx, il)
    turkey(ctx, TX + 60, TY)
    plate(ctx, PX, PY)
    hx_, hy = m['front']
    cone(ctx, hx_, hy - 40, 1.0 * max(0.05, eout(pop(il, 0, 6))), 0.1)
    if il < 20:
        sparkle(ctx, hx_ + 60, hy - 260, 30, YEL); sparkle(ctx, hx_ - 70, hy - 180, 20, WHITE)
    if il >= 26:
        for a in (-0.6, 0, 0.6):    # gag lines
            kx, ky = k['head']
            ctx.move_to(kx - 80 * math.sin(a), ky + 30); ctx.line_to(kx - 150 * math.sin(a) - 30, ky + 60 + 20 * a); setc(ctx, GREEN); ctx.set_line_width(8); ctx.stroke()
    dog(ctx, 1640, GND + 8, 0.6, -1, il)
    ctx.restore()
    label(ctx, "DAY 5:", 540, 520, 120, GOLD, -0.04, pop(il, 0, 3))
    label(ctx, "\"Turkey ICE CREAM!\"", 540, 1360, 100, MINT, -0.03, pop(il, 4, 8))
    if il >= 26:
        label(ctx, "*BLEH!*", 540, 1470, 140, GREEN, 0.04, pop(il, 26, 29))


def fridge_shelf_items(ctx, lf, n, glow):
    """turkey everywhere on the foreground shelves (POV from inside the fridge)"""
    rnd = random.Random(5)
    spots = [(200, 1350, 'leg', 1.7), (870, 1360, 'box', 1.3), (540, 1830, 'turkey', 2.0), (190, 1830, 'box', 1.4),
             (900, 1830, 'leg', 1.8), (760, 890, 'leg', 1.4), (300, 890, 'box', 1.1), (560, 890, 'leg', 1.2)]
    for k, (x, y, kind, s) in enumerate(spots[:n]):
        bob = -10 * abs(math.sin(lf * 0.3 + k))
        if kind == 'leg':
            drumstick(ctx, x, y - 50 + bob, s, 0.4 * (1 if k % 2 else -1))
        elif kind == 'box':
            rect_r(ctx, x - 90 * s, y - 110 * s + bob, 180 * s, 110 * s, 16); fl(ctx, hx('e8f6ff'), 5)
            rect_r(ctx, x - 96 * s, y - 126 * s + bob, 192 * s, 28 * s, 10); fl(ctx, PINK, 4)
            ctx.save(); ctx.translate(x, y - 50 * s + bob); ctx.scale(s, s)
            text(ctx, "TURKEY", 0, 12, 34, ORANGE, ow=6)
            ctx.restore()
        else:
            turkey(ctx, x, y + bob, s * 0.9)


def fridge_pov(ctx, f, il):
    # il 0..90 : 0-12 door opens (light floods in) ; Dad sneaky "Midnight SNACK..." ; 34 sees turkey *AHHH~* ; 52 "...MULTIPLYING?!"
    o = eout(pop(il, 0, 12))
    z = 1.0 + 0.06 * eio(pop(il, 34, 60))
    ctx.save(); cam(ctx, 540, 960, z, 0, shake_at(il, [34, 52], 10, 8), f)
    # dark night kitchen behind Dad
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('1c2240')); ctx.fill()
    rect_r(ctx, 120, 420, 260, 300, 16); fl(ctx, hx('2c3a70'), 6)
    ellipse(ctx, 250, 520, 46, 46); setc(ctx, hx('fff2b0')); ctx.fill()
    ellipse(ctx, 272, 506, 40, 40); setc(ctx, hx('2c3a70')); ctx.fill()
    for k in range(4):
        sparkle(ctx, 160 + k * 60, 640 - 30 * (k % 2), 8, hx('fff2b0'))
    rect_r(ctx, 720, 520, 260, 60, 10); fl(ctx, hx('3a3060'), 4)    # cabinet
    for k in range(3):
        rect_r(ctx, 740 + k * 80, 420, 50, 100, 8); fl(ctx, (PINK, GOLD, MINT)[k], 4)
    # fridge light on Dad
    ctx.save(); ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, (1, 0.96, 0.7, 0.42 * o)); ctx.fill(); ctx.restore()
    shock = il >= 34
    dp = P(eye='shock' if shock else 'smug', mouth='scream' if il >= 52 else ('open' if shock else 'grin'),
           lsh=150 if shock else 60, lel=-30 if shock else -100, rsh=150 if shock else 40, rel=30 if shock else -110, head=-6 if shock else 8, torso=4)
    d = draw(ctx, 540, 1420 - 186 * 1.45, 1.45, 1, DAD_PJ, dp)
    if shock:
        sweat(ctx, d['head'][0] - d['R'] * 0.95, d['head'][1] - d['R'] * 0.5, il, 1.1)
    # fridge interior frame (we are inside the fridge)
    ctx.restore()
    ctx.save(); cam(ctx, 540, 960, 1.0, 0, shake_at(il, [34, 52], 6, 6), f)
    walls = hx('eef6ff')
    poly(ctx, [(-40, -40), (1120, -40), (980, 260), (100, 260)]); fl(ctx, walls, 7)             # top
    poly(ctx, [(-40, -40), (100, 260), (100, 1900), (-40, 2000)]); fl(ctx, dark(walls, 0.93), 7)  # left
    poly(ctx, [(1120, -40), (980, 260), (980, 1900), (1120, 2000)]); fl(ctx, dark(walls, 0.93), 7)
    ellipse(ctx, 540, 150, 80, 26); setc(ctx, (1, 1, 0.75)); ctx.fill()
    for y in (900, 1360, 1830):   # glass shelves in the foreground
        poly(ctx, [(-40, y), (1120, y), (1120, y + 46), (-40, y + 46)]); setc(ctx, (0.75, 0.9, 1.0, 0.55)); ctx.fill()
        ctx.move_to(-40, y); ctx.line_to(1120, y); ink(ctx, 5); ctx.stroke()
    n = 0 if il < 34 else min(8, 3 + int((il - 34) / 3))
    fridge_shelf_items(ctx, il, n, o)
    if shock:
        rays(ctx, 540, 1420, 300, 900, il * 0.04, (1, 1, 0.75), 0.18, 14)
    # door edge sliding open (dark) at the start
    if o < 1:
        ctx.rectangle(lerp(-40, 1120, o), -40, 1200, 2100); setc(ctx, hx('dfe9f8')); ctx.fill()
        ctx.move_to(lerp(-40, 1120, o), -40); ctx.line_to(lerp(-40, 1120, o), 2100); ink(ctx, 7); ctx.stroke()
    ctx.restore()
    label(ctx, "*creak...*", 540, 520, 80, CYAN, 0.04, pop(il, 2, 6) * (il < 34))
    if il < 34:
        label(ctx, "\"Midnight", 540, 1360, 100, WHITE, -0.03, pop(il, 10, 14))
        label(ctx, "SNACK...\"", 540, 1470, 120, GOLD, 0.03, pop(il, 16, 19))
    else:
        label(ctx, "*AHHH~*", 540, 520, 100, YEL, -0.04, pop(il, 34, 37))
        if il >= 52:
            label(ctx, "\"...it's", 540, 1360, 100, WHITE, -0.03, pop(il, 52, 56))
            label(ctx, "MULTIPLYING?!\"", 540, 1470, 120, ORANGE, 0.03, pop(il, 58, 61))


def s3(ctx, f):
    il = f - 200
    if il < 50:
        ice_cream(ctx, f, il)
    else:
        fridge_pov(ctx, f, il - 50)


# ------------------------------------------------------------------ shot 4: close-up -> the dog is full
def closeup(ctx, f, il):
    z = 1 + 0.06 * eio(il / 50)
    ctx.save(); cam(ctx, 540, 960, z, 2 * math.sin(il * 0.2), 2 + shake_at(il, [26], 10, 10), f)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('2a2f5a')), (1, hx('4a4a7a'))])); ctx.paint()
    rays(ctx, 540, 900, 200, 1200, il * 0.03, (1, 0.97, 0.7), 0.25, 16)
    face(ctx, DAD_PJ, P(eye='shock', mouth='scream' if il >= 26 else 'wavy'), 540, 900, 200)
    sweat(ctx, 540 - 230, 820, il, 1.4); sweat(ctx, 540 + 230, 760, il + 20, 1.2)
    # turkey legs reflected / floating around his head
    for k, (x, y, a) in enumerate(((180, 1180, -0.5), (900, 1160, 0.5), (230, 620, 0.3), (880, 600, -0.3))):
        drumstick(ctx, x, y + 10 * math.sin(il * 0.2 + k), 1.1, a + 0.05 * math.sin(il * 0.3 + k))
    ctx.restore()
    label(ctx, "\"It's... NEVER...", 540, 1360, 100, WHITE, -0.03, pop(il, 4, 8))
    if il >= 26:
        label(ctx, "...ENDING!!\"", 540, 1470, 140, ORANGE, 0.04, pop(il, 26, 29))


def under_table(ctx, f, il):
    # 0..50 low angle under the table: Dad's hand slides the plate to the round dog ; 18 *BURP!* ; 28 nudges it back
    ctx.save(); cam(ctx, 1150, 1450, 1.35, -4, shake_at(il, [18], 10, 8), f)
    room(ctx, il)
    d = stand(ctx, DAD, DADX, KDAD, P(eye='smug', mouth='grin', rsh=40, rel=-30, lsh=20, lel=-20, torso=20, head=10), 1)
    table(ctx, il)
    turkey(ctx, TX + 60, TY)
    # tablecloth shadow under the table
    ctx.rectangle(TB0, TFR + 20, TB1 - TB0, FLOOR - TFR); setc(ctx, (0.25, 0.1, 0.1, 0.0)); ctx.fill()
    burp = pop(il, 18, 24)
    round_dog(ctx, 1300, GND + 10, 0.62 + 0.04 * math.sin(burp * math.pi), il)
    px = lerp(1060, 1180, eout(pop(il, 0, 12))) if il < 28 else lerp(1180, 1000, eout(pop(il, 28, 40)))
    plate(ctx, px, GND - 8, 0.8)
    sandwich(ctx, px, GND - 16, 0.6)
    if il < 28:
        ctx.save(); ctx.translate(px - 120, GND - 50)
        rect_r(ctx, -60, -20, 120, 40, 18); fl(ctx, DAD['shirt'], 4)
        ellipse(ctx, 60, 0, 30, 26); fl(ctx, DAD['skin'], 4)
        ctx.restore()
    if 18 <= il < 30:
        for k in range(3):
            ellipse(ctx, 1150 + k * 30, GND - 260 - k * 40 - 40 * burp, 18 + 8 * k, 18 + 8 * k); setc(ctx, (1, 1, 1, 0.7 * (1 - burp * 0.6))); ctx.fill()
    ctx.restore()
    if il < 18:
        label(ctx, "*psst... here, boy*", 540, 1470, 80, WHITE, -0.03, pop(il, 2, 6))
    elif il < 30:
        label(ctx, "*BURP!*", 540, 560, 140, GREEN, 0.05, pop(il, 18, 21))
    else:
        label(ctx, "*BURP!*", 540, 560, 140, GREEN, 0.05, 1)
        label(ctx, "\"...even the DOG?!\"", 540, 1470, 110, ORANGE, -0.03, pop(il, 32, 36))


def s4(ctx, f):
    il = f - 340
    if il < 50:
        closeup(ctx, f, il)
    else:
        under_table(ctx, f, il - 50)


# ------------------------------------------------------------------ shot 5: Grandma's turkey
def grandma(ctx, f, il):
    # 0 *DING-DONG!* ; 8-40 Gran walks in with a giant turkey "I brought LEFTOVERS!" ; 60-90 card ;
    # 96 *THUD!!* on the table ; 110-190 Dad twitch "...TURKEY..."
    if il < 96:
        cx, cy, z = 820, 1180, 1.05
    else:
        u = eio(pop(il, 96, 120)); cx, cy, z = lerp(820, 880, u), lerp(1180, 1220, u), lerp(1.05, 1.2, u)
    ctx.save(); cam(ctx, cx, cy, z, 0, shake_at(il, [0, 96], 8, 22), f)
    room(ctx, il)
    jump = math.sin(math.pi * pop(il, 96, 108)) if il >= 96 else 0.0
    m = stand(ctx, MOM, 1230, KMOM, P(eye='shock' if il < 96 else 'happy', mouth='open', lsh=150, lel=-30, rsh=150, rel=-40), 1)
    k = stand(ctx, KID, KIDX, KKID, P(eye='shock', mouth='scream', lsh=150, lel=-150, rsh=150, rel=-150), -1, 0)
    if il < 110:
        dp = P(eye='shock', mouth='scream' if il >= 30 else 'open', rsh=150, rel=-30, lsh=150, lel=30, head=-6)
    else:
        dp = P(eye='glare', mouth='wavy', rsh=20, rel=-30, lsh=20, lel=-20, head=4)
    d = stand(ctx, DAD, DADX, KDAD, dp, 1)
    table(ctx, il, jump)
    turkey(ctx, TX + 60, TY - 26 * jump)
    plate(ctx, PX, PY - 26 * jump)
    # Grandma + giant turkey
    if il < 96:
        gx = lerp(120, 470, eout(pop(il, 6, 30)))
        s_ = math.sin(il * 0.5) if il < 30 else 0
        gp = P(eye='happy', mouth='grin', lsh=120, lel=-40, rsh=120, rel=-40, lhip=20 * s_, rhip=-20 * s_, torso=-6)
        g = stand(ctx, GRAN, gx, 0.92, gp, 1)
        turkey(ctx, g['front'][0] + 120, g['front'][1] + 150, 1.45, platter=False)
    else:
        g = stand(ctx, GRAN, 430, 0.92, P(eye='happy', mouth='grin', lsh=-20, lel=-40, rsh=-130, rel=-20), 1)
        turkey(ctx, 700, TTOP - 10 - 30 * jump, 1.5, platter=False)
    if il >= 96:
        for k_ in range(6):
            a = math.pi + k_ * math.pi / 5
            dd = 60 + 160 * eout(pop(il, 96, 112))
            ellipse(ctx, 700 + dd * math.cos(a) * 1.5, TTOP + dd * math.sin(a) * 0.4, 30, 22); setc(ctx, (1, 1, 1, 0.8 * (1 - pop(il, 96, 112)))); ctx.fill()
    if il >= 120:
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.7, il, 1.0)
    dog(ctx, 1640, GND + 8, 0.6, -1, il)
    ctx.restore()
    if il < 60:
        label(ctx, "*DING-DONG!*", 540, 520, 100, GOLD, -0.04, pop(il, 0, 3))
        if il >= 14:
            label(ctx, "\"I brought", 540, 1360, 100, PINK, -0.03, pop(il, 14, 18))
            label(ctx, "LEFTOVERS!\"", 540, 1470, 130, PINK, 0.03, pop(il, 24, 27))
    if 60 <= il < 92:
        card(ctx, 'p2', il, 60, 92)
    if il >= 96 and il < 130:
        label(ctx, "*THUD!!*", 540, 520, 130, RED, -0.05, pop(il, 96, 99))
    if il >= 130:
        label(ctx, "\"...MORE...", 540, 1360, 100, WHITE, -0.03, pop(il, 130, 134))
        if il >= 150:
            label(ctx, "TURKEY?!\"", 540, 1470, 150, ORANGE, 0.04, pop(il, 150, 153))


def s5(ctx, f):
    lf = f - 440
    if lf < 190:
        grandma(ctx, f, lf)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (200, s3), (340, s4), (440, s5)]
CUTS = (60, 106, 152, 200, 250, 340, 390, 440, 630)


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
                              "-i", "out/leftovers_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
