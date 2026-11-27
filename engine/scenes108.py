"""'DAD vs THE FROZEN CAR'. Original, general-audience comedy short, 22s.
Hook:   snowy driveway medium shot: Dad in a red coat + blue beanie scraping the iced-over windshield of a teal car like
        a maniac, ice chips flying, sweating "5 MINUTES... TOPS!!" + caption 'DAD vs THE FROZEN CAR:'.
Beat 1: windshield macro: the scraper grinds a tiny peephole *SKRRT! SKRRT!* "...PROGRESS!" -> medium: proud Dad leans on
        the car -> *creak...* the roof snow slides off *FWUMP!!* buries him to the eyes, the glass frosts over "...ow."
Beat 2: Dutch-tilt tool montage: THE SPATULA *tink tink* NOPE! -> THE HAIR DRYER *VRRRR* the cord is too short *POP!*
        NOPE! -> HOT BREATH *HAAAAH...* -> *crackle* Dad freezes blue himself "...uh-oh."
Beat 3: the one close-up: frozen Dad, icicles on his eyebrows, teeth chattering "I... WILL... NOT..." "...LOSE!!" ->
        the mega-scrape *SKRRRRRRT!!* blizzard of ice -> *DING!* sparkling glass "SPARKLING!!"
Twist:  the neighbour steps out with a mug, *BEEP BEEP!* the car flashes "Thanks, NEIGHBOR!" -> PLOT TWIST: IT WAS THE
        NEIGHBOR'S CAR. whip-pan to Dad's own car: a snow mountain with icicles, the kid laughing in the window ->
        Dad twitch "...5 MINUTES..." "...TOPS." -> scrapes again -> hook loop.
Rewatch easter egg: house numbers 12 (Dad) / 14 (neighbour) on the houses."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face, rays
from scenes58 import sweat, twitch
from scenes84 import eio
import scenes85
from scenes85 import blob, hat, snow_fall, GND, KD, DX, HZ
import scenes13
from scenes13 import card as _card13

RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
SNOW = hx('f7fbff'); SNOW_S = hx('cfe3f7'); ICE = hx('a8d8ff'); FROST = hx('e4f2ff')
CARCOL = hx('2fc4b2')
DAD = dict(doodle.DAD, shirt=hx('ff4d5e'), pants=hx('34477e'), shoes=hx('7a4a2c'))
DAD_R = dict(DAD, skin=hx('f28a78'))
DAD_B = dict(DAD, skin=hx('b8d4f0'))
NB = dict(doodle.NEIGHBOR, shirt=hx('9b4dff'), pants=hx('2a3a6a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff5fa8'))
N = 660
CX = 2060                 # the (neighbour's) car on the neighbour's driveway, facing left
CS = 0.82
MYCX = DX + 40            # Dad's own car
DADX = 1690
GY = GND

CAPS = {'p1': [[("DAD vs ", OUT), ("THE FROZEN CAR:", BLUE)]],
        'p2': [[("PLOT TWIST:", RED)], [("IT WAS THE ", OUT), ("NEIGHBOR'S CAR.", PURPLE)]]}
scenes13.CAPS = CAPS
card = _card13


def stand(ctx, ch, x, k, p, f_=1, g=GND):
    return draw(ctx, x, g - 186 * k, k, f_, ch, p)


# ------------------------------------------------------------------ props
WINS = [[(-272, -198), (-236, -306), (-130, -306), (-130, -198)],
        [(-110, -198), (-110, -306), (10, -306), (10, -198)],
        [(30, -198), (30, -306), (140, -306), (222, -198)]]     # [2] = front / windshield side


def frost_tex(ctx, x0, y0, x1, y1, seed=3, a=1.0, lw=3):
    rnd = random.Random(seed)
    for k in range(int(abs(x1 - x0) * abs(y1 - y0) / 1600) + 4):
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1); r = rnd.uniform(8, 22)
        for j in range(3):
            an = j * math.pi / 3 + rnd.uniform(0, 0.5)
            ctx.move_to(x - math.cos(an) * r, y - math.sin(an) * r); ctx.line_to(x + math.cos(an) * r, y + math.sin(an) * r)
    setc(ctx, (1, 1, 1, 0.85 * a)); ctx.set_line_width(lw); ctx.stroke()


def car(ctx, x, gy, s=CS, f_=-1, frost=1.0, clear=0.0, snow=1.0, ice=1.0, flash=0.0, lf=0, slab=None, sparkle_on=0.0):
    """teal hatchback, side view. f_=-1 faces left. clear: 0..1 cleared share of the windshield; snow: roof snow;
    slab: (dx, dy, rot) offset of the roof snow slab when it slides off."""
    ctx.save(); ctx.translate(x, gy); ctx.scale(s * f_, s)
    cab = [(-300, -190), (-250, -330), (150, -330), (250, -190)]
    poly(ctx, cab); fl(ctx, CARCOL, 9)
    for i, pts in enumerate(WINS):
        poly(ctx, pts); setc(ctx, hx('bfe6ff')); ctx.fill()
        ctx.save(); poly(ctx, pts); ctx.clip()
        # inside: seat backs
        rect_r(ctx, pts[0][0] + 20, -260, 60, 80, 18); fl(ctx, hx('3a4a8a'), 4)
        poly(ctx, [(pts[0][0] + 40, pts[1][1]), (pts[0][0] + 66, pts[1][1]), (pts[0][0] + 24, pts[0][1]), (pts[0][0] - 2, pts[0][1])])
        setc(ctx, (1, 1, 1, 0.3)); ctx.fill()
        if frost > 0:
            cl = clear if i == 2 else 0.0
            ctx.save()
            if cl > 0:   # cleared area grows from the bottom of the windshield, wavy scrape edge
                ctx.new_path(); ctx.rectangle(-400, -400, 900, 400)
                top = -198 - 110 * cl
                ctx.move_to(240, -190); ctx.line_to(240, top)
                for k in range(9):
                    xx = 240 - k * 26
                    ctx.line_to(xx, top + 10 * math.sin(k * 1.7))
                ctx.line_to(20, top); ctx.line_to(20, -190); ctx.close_path()
                ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); ctx.clip()
            ctx.rectangle(-400, -400, 900, 400); setc(ctx, FROST[:3] + (0.96 * frost,)); ctx.fill()
            frost_tex(ctx, pts[0][0], -310, pts[3][0], -196, 7 + i, frost)
            ctx.restore()
        ctx.restore()
        poly(ctx, pts); ink(ctx, 7); ctx.stroke()
    rect_r(ctx, -360, -210, 720, 150, 52); fl(ctx, CARCOL, 9)
    for dx in (-120, 20):
        ctx.move_to(dx, -205); ctx.line_to(dx, -80); setc(ctx, dark(CARCOL, 0.7)); ctx.set_line_width(5); ctx.stroke()
        rect_r(ctx, dx + 30, -175, 46, 13, 6); fl(ctx, dark(CARCOL, 0.6), 3)
    hl = YEL if flash <= 0 else (1, 1, 0.7)
    rect_r(ctx, 318, -190, 40, 34, 12); fl(ctx, hl, 5)
    rect_r(ctx, -360, -186, 30, 34, 10); fl(ctx, RED if flash <= 0 else hx('ffb0b0'), 5)
    if flash > 0:
        for (lx, col) in ((338, (1, 1, 0.6)), (-345, (1, 0.5, 0.5))):
            ellipse(ctx, lx, -172, 90 * flash, 70 * flash); setc(ctx, col + (0.55 * flash,)); ctx.fill()
    # heart sticker
    ctx.save(); ctx.translate(-250, -130); ctx.scale(0.8, 0.8)
    ctx.move_to(0, 10); ctx.curve_to(-30, -14, -12, -36, 0, -20); ctx.curve_to(12, -36, 30, -14, 0, 10); fl(ctx, PINK, 3)
    ctx.restore()
    if ice > 0:   # icy crust on the body + icicles on the bumpers
        rect_r(ctx, -356, -206, 712, 60, 40); setc(ctx, (0.85, 0.94, 1.0, 0.45 * ice)); ctx.fill()
        for k in range(10):
            xx = -330 + k * 70
            L = (18 + 22 * ((k * 37) % 3)) * ice
            poly(ctx, [(xx - 9, -64), (xx + 9, -64), (xx + 1, -64 + L)]); fl(ctx, ICE, 3)
    for wx in (-210, 210):
        ellipse(ctx, wx, -60, 66, 66); fl(ctx, hx('2a2840'), 8)
        ellipse(ctx, wx, -60, 30, 30); fl(ctx, hx('c8ccd8'), 5)
    # snow on the roof + hood
    if snow > 0:
        if slab is None:
            blob(ctx, -270, 170, -326, 80 * snow, 5, lw=5)
        blob(ctx, 230, 362, -204, 34 * min(1, snow), 6, lw=4)
        blob(ctx, -362, -250, -204, 30 * min(1, snow), 8, lw=4)
    if slab is not None:
        dx, dy, rot = slab
        ctx.save(); ctx.translate(-50 + dx, -330 + dy); ctx.rotate(rot)
        blob(ctx, -220, 220, 4, 80, 5, lw=5)
        ctx.restore()
    ctx.restore()
    for k in range(3):
        if sparkle_on > 0:
            sparkle(ctx, x + f_ * s * (60 + k * 60), gy - s * (240 + 30 * (k % 2)), 30 * sparkle_on * (0.7 + 0.3 * math.sin(lf * 0.6 + k)), WHITE)


def wind_pt(x, gy, s=CS, f_=-1):
    """centre of the windshield in world coords"""
    return x + f_ * s * 120, gy - s * 252


def scraper(ctx, hand, target, L=110, col=hx('ffc93c'), blade=hx('7fe3ff'), sc=1.0):
    hx_, hy_ = hand
    a = math.atan2(target[1] - hy_, target[0] - hx_)
    ctx.save(); ctx.translate(hx_, hy_); ctx.rotate(a); ctx.scale(sc, sc)
    rect_r(ctx, -20, -12, L, 24, 12); fl(ctx, col, 4)
    ctx.move_to(L - 6, -40); ctx.line_to(L + 24, -46); ctx.line_to(L + 24, 46); ctx.line_to(L - 6, 40); ctx.close_path(); fl(ctx, blade, 4)
    ctx.restore()
    return hx_ + math.cos(a) * (L + 24) * sc, hy_ + math.sin(a) * (L + 24) * sc


def chips(ctx, x, y, lf, n=7, spread=1.0, seed=0, a=1.0):
    rnd = random.Random(seed)
    for k in range(n):
        u = ((lf * 0.09 + k / n) % 1)
        an = rnd.uniform(-2.6, -0.5)
        sp = rnd.uniform(120, 260) * spread
        cx_ = x + math.cos(an) * sp * u - 40 * u; cy_ = y + math.sin(an) * sp * u + 260 * u * u
        r = rnd.uniform(7, 14) * (1 - 0.5 * u)
        poly(ctx, [(cx_ - r, cy_), (cx_, cy_ - r * 1.3), (cx_ + r, cy_), (cx_, cy_ + r * 0.9)]); fl(ctx, ICE[:3] + (a * (1 - u * 0.6),) if False else ICE, 2)


def spatula(ctx, hand, target):
    hx_, hy_ = hand
    a = math.atan2(target[1] - hy_, target[0] - hx_)
    ctx.save(); ctx.translate(hx_, hy_); ctx.rotate(a)
    rect_r(ctx, -20, -9, 100, 18, 9); fl(ctx, hx('8a5a3a'), 4)
    rect_r(ctx, 76, -34, 70, 68, 12); fl(ctx, hx('ff8ab8'), 4)
    for k in range(3):
        ctx.move_to(92 + k * 18, -18); ctx.line_to(92 + k * 18, 18)
    ink(ctx, 4); ctx.stroke()
    ctx.restore()


def hair_dryer(ctx, hand, target, plug_x, plug_y, taut=0.0, lf=0, on=True):
    hx_, hy_ = hand
    # cord: from the hand back to the plug (sags, then pulls straight)
    sag = 140 * (1 - taut)
    ctx.move_to(hx_, hy_ + 10); ctx.curve_to(hx_ - 80, hy_ + 60 + sag, plug_x + 80, plug_y + sag, plug_x, plug_y)
    setc(ctx, INK); ctx.set_line_width(11); ctx.stroke_preserve(); setc(ctx, hx('5a5a6a')); ctx.set_line_width(6); ctx.stroke()
    a = math.atan2(target[1] - hy_, target[0] - hx_)
    ctx.save(); ctx.translate(hx_, hy_); ctx.rotate(a)
    rect_r(ctx, -14, -10, 26, 70, 10); fl(ctx, PURPLE, 4)               # grip (points down/back)
    rect_r(ctx, -40, -46, 120, 56, 24); fl(ctx, hx('b88aff'), 5)
    ellipse(ctx, 84, -18, 14, 30); fl(ctx, hx('5a3a9a'), 4)
    if on:
        for k in range(4):
            u = (lf * 0.12 + k / 4) % 1
            ctx.move_to(100 + 140 * u, -30 + 10 * math.sin(lf + k)); ctx.line_to(140 + 140 * u, -30 + 10 * math.sin(lf + k + 1))
        setc(ctx, (1, 0.7, 0.4, 0.8)); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def plug(ctx, x, y, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    rect_r(ctx, -22, -18, 44, 36, 8); fl(ctx, WHITE, 4)
    for dy in (-8, 8):
        ctx.rectangle(-42, dy - 3, 22, 6); fl(ctx, GOLD, 2)
    ctx.restore()


def mug(ctx, x, y, s=1.0, lf=0):
    rect_r(ctx, x - 24 * s, y - 30 * s, 48 * s, 56 * s, 10 * s); fl(ctx, GOLD, 4)
    ctx.new_path(); ctx.arc(x + 26 * s, y - 2 * s, 14 * s, -1.4, 1.4); ink(ctx, 6); ctx.stroke()
    for k in range(2):
        ox = x - 8 * s + 16 * k * s
        ctx.move_to(ox, y - 36 * s); ctx.curve_to(ox - 12 * s, y - 56 * s - 6 * math.sin(lf * 0.2), ox + 12 * s, y - 70 * s, ox, y - 90 * s)
    setc(ctx, (1, 1, 1, 0.85)); ctx.set_line_width(5); ctx.stroke()


def key_fob(ctx, x, y, s=1.0):
    rect_r(ctx, x - 16 * s, y - 26 * s, 32 * s, 50 * s, 12 * s); fl(ctx, hx('3a3a4a'), 4)
    ellipse(ctx, x, y - 8 * s, 8 * s, 8 * s); fl(ctx, RED, 2)


def icicle_face(ctx, cx, cy, R):
    """icicles hanging off eyebrows + nose on a face of radius R centred cx, cy"""
    for (dx, dy, L) in ((-0.42, -0.2, 0.18), (-0.3, -0.2, 0.26), (-0.18, -0.21, 0.16), (0.2, -0.22, 0.2), (0.32, -0.2, 0.28), (0.45, -0.18, 0.15)):
        x = cx + dx * R; y = cy + dy * R
        poly(ctx, [(x - R * 0.045, y), (x + R * 0.045, y), (x + R * 0.005, y + L * R)]); fl(ctx, ICE, 3)
    for k in range(6):
        sparkle(ctx, cx + R * (-0.9 + 0.36 * k), cy - R * (0.95 + 0.12 * (k % 2)), R * 0.08, WHITE)


# ------------------------------------------------------------------ set + Dad
def world(ctx, lf, slab=None, car_kw=None, my_car=True, nb=None):
    scenes85.world(ctx, lf, drive=0.85, nb_drive=0.6, nb_house=True, kid=True)
    if my_car:
        own_car(ctx, lf)
    car(ctx, CX, GY + 20, CS, -1, lf=lf, slab=slab, **(car_kw or {}))


def own_car(ctx, lf):
    car(ctx, MYCX, GY + 20, CS, 1, frost=1.0, snow=2.6, ice=1.6, lf=lf)
    blob(ctx, MYCX - 360, MYCX + 380, GY + 30, 120, 61, lw=5)       # snow banks over the wheels
    blob(ctx, MYCX - 250, MYCX + 160, GY + 20 - CS * 326, 170, 62, lw=5)   # mountain on the roof
    blob(ctx, MYCX - 150, MYCX + 60, GY + 20 - CS * 326 - 150, 80, 63, lw=4)


def scrape_pose(lf, amp=1.0, eye='glare', mouth='scream', speed=1.2):
    w = math.sin(lf * speed) * amp
    return P(eye=eye, mouth=mouth, torso=10 + 4 * w, head=-8, rsh=118 + 22 * w, rel=-34 - 12 * w, lsh=80, lel=-50,
             lhip=-14, rhip=16, rkn=-10)


def dad_scrape(ctx, lf, ch=DAD_R, x=DADX, amp=1.0, eye='glare', mouth='scream', speed=1.2, chip_n=7):
    d = stand(ctx, ch, x, KD, scrape_pose(lf, amp, eye, mouth, speed))
    hat(ctx, d, BLUE)
    tip = scraper(ctx, d['front'], wind_pt(CX, GY + 20))
    if chip_n:
        chips(ctx, tip[0], tip[1], lf * speed * 1.4, chip_n, 1.0, 3)
    return d, tip


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = 1.08 + 0.04 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, 2000, 1260, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    world(ctx, lf, car_kw=dict(clear=0.25 + 0.04 * math.sin(lf * 0.5)))
    d, tip = dad_scrape(ctx, lf)
    sweat(ctx, d['head'][0] - d['R'] * 1.0, d['head'][1] - d['R'] * 0.3, lf, 1.0)
    ctx.restore()
    snow_fall(ctx, lf, 26, 0.7)


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"5 MINUTES...", 540, 1380, 110, WHITE, -0.04, t)
    label(ctx, "TOPS!!\"", 540, 1490, 150, RED, 0.03, t)


# ------------------------------------------------------------------ shot 2: macro peephole -> roof avalanche
def macro(ctx, f, il):
    # il 0..50: windshield fills the frame; the scraper grinds a peephole; 30 "...PROGRESS!"
    z = 1.0 + 0.08 * eio(il / 50)
    ctx.save(); cam(ctx, 540, 960, z, 0, 3, f)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('bcdcff')), (1, hx('dceeff'))])); ctx.paint()
    # car body around the glass
    poly(ctx, [(-100, 520), (1180, 520), (1180, 2100), (-100, 2100)]); fl(ctx, CARCOL, 10)
    glass = [(150, 540), (930, 540), (1050, 1460), (30, 1460)]
    poly(ctx, glass); setc(ctx, hx('9fd0f0')); ctx.fill()
    ctx.save(); poly(ctx, glass); ctx.clip()
    # interior seen through the hole: steering wheel, seats, a little star charm
    rect_r(ctx, 150, 940, 320, 560, 60); fl(ctx, hx('3a4a8a'), 6)
    rect_r(ctx, 610, 940, 320, 560, 60); fl(ctx, hx('3a4a8a'), 6)
    ctx.new_path(); ctx.arc(360, 1400, 180, 0, 2 * math.pi); setc(ctx, INK); ctx.set_line_width(40); ctx.stroke_preserve()
    setc(ctx, hx('4a4a5a')); ctx.set_line_width(28); ctx.stroke()
    ctx.move_to(540, 600); ctx.line_to(540, 760); ink(ctx, 4); ctx.stroke()
    sw = 0.3 * math.sin(il * 0.25)
    ctx.save(); ctx.translate(540, 760); ctx.rotate(sw); sparkle(ctx, 0, 40, 46, GOLD); ctx.restore()
    # frost with a growing hole
    r = 210 * eout(pop(il, 4, 34))
    hcx, hcy = 540, 980
    ctx.new_path(); ctx.rectangle(-200, -200, 1500, 2400)
    if r > 0:
        for k in range(24):
            a = k * 2 * math.pi / 24
            rr = r * (1 + 0.08 * math.sin(k * 2.3))
            (ctx.move_to if k == 0 else ctx.line_to)(hcx + math.cos(a) * rr, hcy + math.sin(a) * rr * 0.85)
        ctx.close_path()
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); setc(ctx, FROST); ctx.fill()
    ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    frost_tex(ctx, 40, 540, 1040, 1460, 11, 1.0, 5)
    if r > 0:   # re-cover the hole area texture
        ctx.save(); ctx.new_path()
        for k in range(24):
            a = k * 2 * math.pi / 24
            rr = r * (1 + 0.08 * math.sin(k * 2.3))
            (ctx.move_to if k == 0 else ctx.line_to)(hcx + math.cos(a) * rr, hcy + math.sin(a) * rr * 0.85)
        ctx.close_path(); ctx.clip()
        rect_r(ctx, 150, 940, 320, 560, 60); fl(ctx, hx('3a4a8a'), 6)
        rect_r(ctx, 610, 940, 320, 560, 60); fl(ctx, hx('3a4a8a'), 6)
        ctx.move_to(540, 600); ctx.line_to(540, 760); ink(ctx, 4); ctx.stroke()
        ctx.save(); ctx.translate(540, 760); ctx.rotate(sw); sparkle(ctx, 0, 40, 46, GOLD); ctx.restore()
        ctx.restore()
    ctx.restore()
    poly(ctx, glass); ink(ctx, 10); ctx.stroke()
    # wipers + snowy cowl
    blob(ctx, -100, 1180, 1500, 90, 21, lw=6)
    ctx.move_to(180, 1450); ctx.line_to(560, 1350); ink(ctx, 14); ctx.stroke()
    # Dad's mitten + big scraper circling
    a = il * 0.7
    hxp, hyp = hcx + 150 + math.cos(a) * 90 * (r / 210 + 0.3), hcy + 380 + math.sin(a) * 60
    tip = scraper(ctx, (hxp + 140, hyp + 220), (hxp - 60, hyp - 200), 200, sc=1.5)
    rect_r(ctx, hxp + 90, hyp + 200, 200, 120, 50); fl(ctx, DAD['shirt'], 6)
    ellipse(ctx, hxp + 120, hyp + 220, 70, 60); fl(ctx, BLUE, 6)
    chips(ctx, tip[0], tip[1], il * 1.6, 10, 2.0, 5)
    ctx.restore()
    if il < 30:
        label(ctx, "*SKRRT! SKRRT!*", 540, 520, 100, CYAN, -0.04, pop(il, 2, 5))
    else:
        label(ctx, "\"...PROGRESS!\"", 540, 1470, 130, GOLD, -0.03, pop(il, 30, 34))


def avalanche(ctx, f, il):
    # il 0..90: proud Dad leans on the car ; 12 *creak...* the roof slab wobbles ; 26-34 slides ; 34 *FWUMP!!* ; 48 "...ow."
    ctx.save(); cam(ctx, 2000, 1260, 1.1, 0, shake_at(il, [34], 12, 22), f)
    if il < 26:
        wob = math.sin(il * 1.4) * 0.03 * pop(il, 12, 16)
        slab = (0, 0, wob) if il >= 12 else None
    else:
        u = eio(pop(il, 26, 34))
        slab = (lerp(0, 300, u), lerp(0, 230, u), lerp(0, 0.5, u)) if il < 34 else None
    clear = 0.42 if il < 34 else 0.0
    world(ctx, il, slab=slab, car_kw=dict(clear=clear, snow=1.0 if il < 34 else 0.15))
    if il < 34:
        d = stand(ctx, DAD, DADX, KD, P(eye='smug', mouth='grin', torso=-6, rsh=60, rel=-20, lsh=10, lel=-10, lhip=-10, rhip=14))
        hat(ctx, d, BLUE)
        scraper(ctx, d['back'], (d['back'][0] - 30, d['back'][1] + 200), 90)
    else:
        # buried to the eyes
        ctx.save(); ctx.rectangle(-3000, -3000, 9000, 3000 + GND - 200); ctx.clip()
        d = stand(ctx, DAD, DADX, KD, P(eye='glare' if il >= 46 else 'shock', mouth='flat', lsh=20, lel=-10, rsh=20, rel=-10))
        ctx.restore()
        hat(ctx, d, BLUE, snowy=True)
        blob(ctx, DADX - 260, DADX + 250, GND + 40, 300 + 30 * (1 - pop(il, 34, 40)), 71, lw=6)
        scraper(ctx, (DADX + 150, GND - 230), (DADX + 200, GND - 420), 90)
        for k in range(8):
            a = math.pi + k * math.pi / 7
            dd = 80 + 260 * eout(pop(il, 34, 50))
            ellipse(ctx, DADX + dd * math.cos(a), GND - 200 + dd * math.sin(a) * 0.6, 26, 22); setc(ctx, (1, 1, 1, 0.9 * (1 - pop(il, 34, 50)))); ctx.fill()
    ctx.restore()
    snow_fall(ctx, il, 26, 0.7)
    if il < 26:
        label(ctx, "*creak...*", 540, 520, 90, CYAN, 0.04, pop(il, 12, 15))
    elif il < 46:
        label(ctx, "*FWUMP!!*", 540, 520, 130, WHITE, -0.05, pop(il, 34, 37))
    else:
        label(ctx, "*FWUMP!!*", 540, 520, 130, WHITE, -0.05, 1)
        label(ctx, "\"...ow.\"", 540, 1480, 140, WHITE, -0.03, pop(il, 48, 52))


def s2(ctx, f):
    il = f - 60
    if il < 50:
        macro(ctx, f, il)
    else:
        avalanche(ctx, f, il - 50)


# ------------------------------------------------------------------ shot 3: tool montage
TOOLS = [(0, "THE SPATULA!", "*tink! tink!*"), (45, "THE HAIR DRYER!", "*VRRRRR...*"), (90, "HOT BREATH!", "*HAAAAH...*")]


def montage(ctx, f, il):
    i = 0 if il < 45 else (1 if il < 90 else 2)
    t0, name, sfx = TOOLS[i]
    l = il - t0
    rot = (-6, 6, -5)[i]
    z = 1.18 + 0.05 * eio(l / 45) + (0.1 if i == 2 else 0)
    cx = 1830 if i < 2 else 1840
    ctx.save(); cam(ctx, cx, 1270, z, rot, shake_at(l, [26] if i < 2 else [24], 10, 10), f)
    world(ctx, il, car_kw=dict(clear=0.0))
    wp = wind_pt(CX, GY + 20)
    if i == 0:
        bounce = 0.5 + 0.5 * math.sin(l * 1.3)
        p = P(eye='glare' if l < 26 else 'shock', mouth='scream' if l < 26 else 'open', torso=10, head=-6,
              rsh=110 + 20 * bounce, rel=-30, lsh=80, lel=-50, lhip=-14, rhip=16)
        d = stand(ctx, DAD_R, DADX, KD, p); hat(ctx, d, BLUE)
        spatula(ctx, d['front'], wp)
        if 4 <= l < 26 and l % 6 < 3:
            sparkle(ctx, wp[0] - 60, wp[1] + 20, 26, WHITE)
    elif i == 1:
        taut = pop(l, 14, 22)
        p = P(eye='happy' if l < 20 else 'shock', mouth='grin' if l < 20 else 'scream', torso=6, head=-6,
              rsh=100 - 30 * taut, rel=-20, lsh=60, lel=-40, lhip=-14, rhip=16)
        dxp = DADX + 30 * pop(l, 0, 14) - 60 * eout(pop(l, 20, 28))
        d = stand(ctx, DAD_R, dxp, KD, p); hat(ctx, d, BLUE)
        popped = l >= 26
        px_, py_ = (1340, GND - 60) if not popped else (lerp(1340, 1560, eout(pop(l, 26, 34))), GND - 60 - 260 * math.sin(math.pi * pop(l, 26, 40)))
        hair_dryer(ctx, d['front'], wp, px_, py_, taut if not popped else 0, l, on=not popped)
        plug(ctx, px_, py_, l * 0.6 if popped else 0)
    else:
        # leaning in, breath cloud on the glass -> frost creeps back onto Dad's face
        frz = eio(pop(l, 22, 34))
        ch = DAD_R if frz < 0.5 else DAD_B
        p = P(eye='closed' if l < 22 else 'shock', mouth='open' if l < 22 else 'wavy', torso=24, head=10,
              rsh=40, rel=-20, lsh=30, lel=-20, lhip=-24, rhip=20)
        d = stand(ctx, ch, DADX + 110, KD, p); hat(ctx, d, BLUE, snowy=frz > 0.5)
        hx_, hy_ = d['head']
        if l < 26:
            for k in range(4):   # breath puffs towards the glass
                u = (l * 0.06 + k / 4) % 1
                ellipse(ctx, hx_ + 90 + 120 * u, hy_ + 30 - 20 * u, 22 + 40 * u, 18 + 30 * u); setc(ctx, (1, 1, 1, 0.75 * (1 - u))); ctx.fill()
        if frz > 0:
            icicle_face(ctx, hx_, hy_, d['R'])
            ctx.new_path(); ctx.arc(hx_, hy_, d['R'] * 1.05, 0, 2 * math.pi); setc(ctx, (0.85, 0.95, 1, 0.3 * frz)); ctx.fill()
    ctx.restore()
    snow_fall(ctx, il, 22, 0.6)
    label(ctx, name, 540, 520, 110, GOLD, -0.04, pop(l, 0, 3))
    if l < 26:
        label(ctx, sfx, 540, 1470, 100, CYAN if i != 1 else PURPLE, 0.04, pop(l, 4, 7))
    elif i == 0:
        label(ctx, "NOPE!", 540, 1480, 160, RED, -0.08, pop(l, 26, 29))
    elif i == 1:
        label(ctx, "*POP!*", 820, 760, 90, WHITE, 0.08, pop(l, 26, 29))
        label(ctx, "\"...TOO SHORT?!\"", 540, 1480, 120, ORANGE, -0.03, pop(l, 28, 32))
    else:
        label(ctx, "*crackle!*", 540, 700, 90, CYAN, 0.06, pop(l, 22, 25))
        label(ctx, "\"...uh-oh.\"", 540, 1480, 130, WHITE, -0.03, pop(l, 30, 34))


def s3(ctx, f):
    montage(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: close-up -> mega scrape
def closeup(ctx, f, il):
    z = 1.25 + 0.08 * eio(il / 56)
    ch = 3 * math.sin(il * 2.6) if il < 28 else 0
    ctx.save(); cam(ctx, 540, 1000, z, 2 * math.sin(il * 0.2), 2 + shake_at(il, [28], 12, 14), f)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('5aa8ff')), (1, hx('bfe4ff'))])); ctx.paint()
    ctx.restore(); ctx.save(); ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('5aa8ff')), (1, hx('bfe4ff'))])); ctx.paint(); ctx.restore()
    ctx.save(); cam(ctx, 540, 1000, z, 2 * math.sin(il * 0.2), 2 + shake_at(il, [28], 12, 14), f)
    rays(ctx, 540, 900, 200, 1200, il * 0.03, (1, 1, 1), 0.25, 16)
    face(ctx, DAD_B, P(eye='glare', mouth='scream' if il >= 28 else 'wavy'), 540 + ch, 900, 210)
    hat(ctx, dict(head=(540 + ch, 900), R=210), BLUE, snowy=True)
    icicle_face(ctx, 540 + ch, 900, 210)
    ctx.restore()
    snow_fall(ctx, il, 30, 0.8)
    if il < 28:
        label(ctx, "*chatter chatter*", 540, 520, 80, CYAN, 0.03, pop(il, 2, 6))
    label(ctx, "\"I... WILL... NOT...", 540, 1380, 96, WHITE, -0.03, pop(il, 4, 8))
    if il >= 28:
        label(ctx, "...LOSE!!\"", 540, 1490, 150, RED, 0.04, pop(il, 28, 31))


def mega(ctx, f, il):
    # il 0..44: arm blur *SKRRRRRT!!* ice blizzard -> 22 *DING!* clear + sparkle "SPARKLING!!"
    done = il >= 22
    ctx.save(); cam(ctx, 2000, 1260, 1.1, -3 if not done else 0, 8 if not done else shake_at(il, [22], 8, 10), f)
    clear = eio(pop(il, 0, 22))
    world(ctx, il, car_kw=dict(clear=clear, frost=1 - pop(il, 16, 22), snow=0.15, ice=1 - pop(il, 14, 22), sparkle_on=pop(il, 22, 26)))
    if not done:
        for g in range(3):   # motion ghosts of the arm
            d, tip = dad_scrape(ctx, il * 3 + g * 2, DAD_R, amp=1.6, speed=1.4, chip_n=14 if g == 0 else 0)
        ctx.save(); ctx.translate(tip[0], tip[1])
        for k in range(18):
            rr = random.Random(k + il)
            ellipse(ctx, rr.uniform(-160, 120), rr.uniform(-200, 60), rr.uniform(8, 18), rr.uniform(6, 12)); fl(ctx, ICE, 2)
        ctx.restore()
    else:
        d = stand(ctx, DAD, DADX, KD, P(eye='happy', mouth='grin', torso=-4, rsh=160, rel=-20, lsh=150, lel=-30, lhip=-10, rhip=14))
        hat(ctx, d, BLUE)
        scraper(ctx, d['front'], (d['front'][0] + 40, d['front'][1] - 200))
    ctx.restore()
    if not done:
        label(ctx, "*SKRRRRRRT!!*", 540, 520, 110, CYAN, -0.05, pop(il, 0, 3))
    else:
        label(ctx, "*DING!*", 540, 520, 120, GOLD, -0.04, pop(il, 22, 25))
        label(ctx, "\"SPARKLING!!\"", 540, 1480, 140, MINT, -0.03, pop(il, 24, 28))


def s4(ctx, f):
    il = f - 340
    if il < 56:
        closeup(ctx, f, il)
    else:
        mega(ctx, f, il - 56)


# ------------------------------------------------------------------ shot 5: the neighbour
NBX0, NBX1 = 2480, 2420


def neighbour(ctx, f, il):
    # il 0..70: neighbour steps out with a mug, 16 *BEEP BEEP!* lights flash, 26 "Thanks, NEIGHBOR!"
    ctx.save(); cam(ctx, 2000, 1250, 1.12, 0, shake_at(il, [16], 6, 6), f)
    fl_ = 0.0
    for b in (16, 21):
        if b <= il < b + 4:
            fl_ = 1 - (il - b) / 4
    world(ctx, il, car_kw=dict(clear=1.0, frost=0.0, snow=0.15, ice=0.0, flash=fl_))
    nx = lerp(NBX0, NBX1, eout(pop(il, 0, 14)))
    s_ = math.sin(il * 0.6) if il < 14 else 0
    n = stand(ctx, NB, nx, KD, P(eye='happy', mouth='grin', lsh=60, lel=-80, rsh=90 if il >= 12 else 30, rel=-30 if il >= 12 else -60,
                                 lhip=18 * s_, rhip=-18 * s_), f_=-1)
    hat(ctx, n, GOLD)
    mug(ctx, n['back'][0], n['back'][1] - 10, 0.9, il)
    key_fob(ctx, n['front'][0], n['front'][1] - 6, 1.0)
    dp = P(eye='happy' if il < 22 else 'shock', mouth='grin' if il < 22 else 'open', torso=-4, rsh=150 if il < 22 else 60, rel=-20,
           lsh=40, lel=-30, lhip=-10, rhip=14)
    d = stand(ctx, DAD, DADX, KD, dp); hat(ctx, d, BLUE)
    scraper(ctx, d['front'], (d['front'][0] + 60, d['front'][1] - 200))
    if il >= 26:
        sweat(ctx, d['head'][0] - d['R'] * 1.0, d['head'][1] - d['R'] * 0.3, il, 1.0)
    ctx.restore()
    snow_fall(ctx, il, 22, 0.6)
    if 16 <= il < 30:
        label(ctx, "*BEEP BEEP!*", 540, 560, 100, GOLD, 0.05, pop(il, 16, 19))
    if il >= 30:
        label(ctx, "\"Thanks,", 540, 1380, 110, WHITE, -0.03, pop(il, 30, 34))
        label(ctx, "NEIGHBOR!\"", 540, 1490, 140, PURPLE, 0.03, pop(il, 36, 39))


def reveal(ctx, f, il):
    # il 0..60 : whip-pan to Dad's own house: his car is a snow mountain, the kid laughing in the window ; card p2
    u = eio(pop(il, 0, 12))
    cx = lerp(2000, 760, u); z = lerp(1.12, 1.18, u)
    ctx.save(); cam(ctx, cx, 1150, z, 0, 0, f)
    world(ctx, il + 70, car_kw=dict(clear=1.0, frost=0.0, snow=0.15, ice=0.0))
    if u < 1:
        ctx.restore(); ctx.save()
        for k in range(10):   # whip-pan streaks
            y = 300 + k * 160
            ctx.move_to(0, y); ctx.line_to(1080, y + 20)
        setc(ctx, (1, 1, 1, 0.5 * math.sin(math.pi * u))); ctx.set_line_width(30); ctx.stroke()
    ctx.restore()
    snow_fall(ctx, il, 22, 0.6)
    card(ctx, 'p2', il, 10)
    if il >= 16:
        label(ctx, "*HA HA HA!*", 300, 580, 70, PINK, -0.06, pop(il, 16, 19))
    if il >= 22:
        label(ctx, "*VROOOM~*", 540, 1480, 100, PURPLE, 0.04, pop(il, 22, 26))


def twitch_end(ctx, f, il):
    # il 0..70: Dad trudges to his own buried car, twitch "...5 MINUTES..." "...TOPS." ; 56 starts scraping again
    ctx.save(); cam(ctx, 1040, 1260, 1.12, 0, 0, f)
    world(ctx, il + 130)
    x = 1290
    if il < 50:
        d = stand(ctx, DAD, x, KD, P(eye='glare', mouth='wavy', torso=2, rsh=30, rel=-20, lsh=20, lel=-20, head=4), f_=-1)
        hat(ctx, d, BLUE)
        scraper(ctx, d['front'], (d['front'][0] - 20, d['front'][1] + 200), 90)
        if il > 8:
            twitch(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.9, il, 1.0)
    else:
        w = math.sin(il * 1.4)
        d = stand(ctx, DAD_R, x, KD, P(eye='glare', mouth='scream', torso=10 + 4 * w, head=-8, rsh=95 + 18 * w, rel=-10 - 10 * w,
                                       lsh=80, lel=-50, lhip=-14, rhip=16), f_=-1)
        hat(ctx, d, BLUE)
        tip = scraper(ctx, d['front'], (MYCX + 100, GY - 160))
        chips(ctx, tip[0], tip[1], il * 1.7, 9, 1.0, 4)
    ctx.restore()
    snow_fall(ctx, il, 26, 0.7)
    if il < 50:
        label(ctx, "\"...5 MINUTES...\"", 540, 1380, 110, WHITE, -0.03, pop(il, 6, 10))
        if il >= 26:
            label(ctx, "\"...TOPS.\"", 540, 1490, 130, RED, 0.03, pop(il, 26, 29))
    else:
        label(ctx, "*SKRRT! SKRRT!*", 540, 520, 100, CYAN, -0.04, pop(il, 50, 53))


def s5(ctx, f):
    lf = f - 440
    if lf < 70:
        neighbour(ctx, f, lf)
    elif lf < 120:
        reveal(ctx, f, lf - 70)
    elif lf < 190:
        twitch_end(ctx, f, lf - 120)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (200, s3), (340, s4), (440, s5)]
CUTS = (60, 110, 200, 245, 290, 340, 396, 440, 560, 630)


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
                              "-i", "out/frozen_car_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
