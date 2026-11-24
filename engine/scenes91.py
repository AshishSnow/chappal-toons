"""'Did I turn off the OVEN?' - original, general-audience comedy short, 22s.
Hook:   street medium shot in front of the house: Mom next to the packed family car, hands on cheeks, mid-panic
        "DID I TURN OFF THE OVEN?!" + caption "EVERY FAMILY TRIP:"; Dad + kid flat-faced in the car windows.
Beat 1: wide tracking: the car zooms off -> *SCREEECH!* "WAIT!!" -> races back in REVERSE *VRRRM!*
Beat 2: kitchen: Mom skids in, push-in macro on the oven knob: it's OFF. "...it's OFF." Dad in the doorway: "TOLD you."
Beat 3: top-down MAP cam: the car heads for the BEACH and U-turns home again and again: "THE DOOR?!" "THE IRON?!"
        "THE TAP?!" -> spaghetti trail, "1 HOUR LATER: 0 MILES."
Turn:   Dad ECU at the wheel (the one close-up), twitching: "NO. MORE." "U-TURNS."
Twist:  highway, finally: "FINALLY!!" -> "PLOT TWIST:" kid: "Mom... where are the SUITCASES?" -> cut home: the suitcases
        stacked on the lawn with the dog sitting on top *WOOF?* -> Dad (same ECU) "...U-TURN." -> the car skids round
        *SCREEECH!* -> back home -> loop to Mom's hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import twitch, sweat
from scenes65 import dog
import scenes77
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); TEAL = hx('19b5a5')
CARCOL = hx('2fc4b2')
DAD = dict(doodle.DAD, shirt=hx('ff8a1f'), pants=hx('3d5a9e'))
MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'), pants=hx('2f4a8a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('7fd04a'), pants=hx('3d7bff'), shoes=hx('ff3b5c'))
N = 660
HZ = scenes77.HZ          # 1190: house bottom / lawn line
ST0, ST1 = 1480, 1900     # street band
GY = 1760                 # car wheels / people ground on the street
KMOM = 1.25

CAPS = {'p1': [[("EVERY ", OUT), ("FAMILY TRIP:", ORANGE)]],
        'p2': [[("PLOT TWIST:", RED)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def family_car(ctx, x, gy, s, faces=None, spin=0.0, tilt=0.0, f_=1, lf=0, bounce=0.0):
    """side view, facing right (f_=-1 faces left). faces: dict seat -> P or None. seats 'kid', 'mom', 'dad'."""
    faces = faces or {}
    ctx.save(); ctx.translate(x, gy - bounce); ctx.rotate(tilt); ctx.scale(s * f_, s)
    # roof rack (EMPTY - the clue)
    for rx in (-170, 130):
        ctx.rectangle(rx, -352, 16, 30); fl(ctx, hx('5a5a6a'), 4)
    rect_r(ctx, -200, -366, 360, 18, 8); fl(ctx, hx('7a7a8a'), 5)
    cab = [(-300, -190), (-250, -330), (150, -330), (250, -190)]
    poly(ctx, cab); fl(ctx, CARCOL, 9)
    wins = [('kid', [(-272, -198), (-236, -306), (-130, -306), (-130, -198)], KID, -196, -232, 44),
            ('mom', [(-110, -198), (-110, -306), (10, -306), (10, -198)], MOM, -50, -236, 46),
            ('dad', [(30, -198), (30, -306), (140, -306), (222, -198)], DAD, 92, -236, 48)]
    for seat, pts, ch, fx, fy, R in wins:
        poly(ctx, pts); setc(ctx, hx('bfe6ff')); ctx.fill()
        ctx.save(); poly(ctx, pts); ctx.clip()
        p = faces.get(seat)
        if p is not None:
            face(ctx, ch, p, fx, fy + 12, R, 0, 1)
        poly(ctx, [(pts[0][0] + 40, pts[1][1]), (pts[0][0] + 66, pts[1][1]), (pts[0][0] + 24, pts[0][1]), (pts[0][0] - 2, pts[0][1])])
        setc(ctx, (1, 1, 1, 0.3)); ctx.fill()
        ctx.restore()
        poly(ctx, pts); ink(ctx, 7); ctx.stroke()
    rect_r(ctx, -360, -210, 720, 150, 52); fl(ctx, CARCOL, 9)
    for dx in (-120, 20):
        ctx.move_to(dx, -205); ctx.line_to(dx, -80); setc(ctx, dark(CARCOL, 0.7)); ctx.set_line_width(5); ctx.stroke()
        rect_r(ctx, dx + 30, -175, 46, 13, 6); fl(ctx, dark(CARCOL, 0.6), 3)
    rect_r(ctx, 318, -190, 40, 34, 12); fl(ctx, YEL, 5)
    rect_r(ctx, -360, -186, 30, 34, 10); fl(ctx, RED, 5)
    # little heart sticker
    ctx.save(); ctx.translate(-250, -130); ctx.scale(0.8, 0.8)
    ctx.move_to(0, 10); ctx.curve_to(-30, -14, -12, -36, 0, -20); ctx.curve_to(12, -36, 30, -14, 0, 10); fl(ctx, PINK, 3)
    ctx.restore()
    for wx in (-210, 210):
        ellipse(ctx, wx, -60, 66, 66); fl(ctx, hx('2a2840'), 8)
        ellipse(ctx, wx, -60, 30, 30); fl(ctx, hx('c8ccd8'), 5)
        ink(ctx, 5)
        for k in range(3):
            a = spin + k * 2 * math.pi / 3
            ctx.move_to(wx, -60); ctx.line_to(wx + math.cos(a) * 26, -60 + math.sin(a) * 26)
        ctx.stroke()
    ctx.restore()


def smoke(ctx, x, y, t, s=1.0, col=(0.92, 0.92, 0.95)):
    if not 0 < t < 1:
        return
    for k in range(6):
        a = k * 1.1
        d = 90 * s * eout(t)
        r = (40 + 14 * (k % 3)) * s * (0.5 + 0.8 * t)
        ellipse(ctx, x - d * (0.6 + 0.4 * math.cos(a)) - 30 * k * s * t, y - 40 * s * t - 20 * math.sin(a) * s, r, r * 0.8)
        fl(ctx, col + (1 - t,) if len(col) == 3 else col, 4)


def motion_lines(ctx, x, y, w, lf, n=5, a=1.0, dirn=1):
    for k in range(n):
        yy = y + k * 46
        xx = x - dirn * ((lf * 40 + k * 70) % 160)
        ctx.move_to(xx, yy); ctx.line_to(xx - dirn * w * (0.5 + 0.1 * k), yy)
    setc(ctx, (1, 1, 1, 0.85 * a)); ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def suitcase(ctx, x, y, w, h, col, a=0.0):
    """(x, y) = bottom centre"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ctx.new_path(); ctx.arc(0, -h - 6, 34, math.pi, 2 * math.pi); setc(ctx, INK); ctx.set_line_width(16); ctx.stroke()
    rect_r(ctx, -w / 2, -h, w, h, 22); fl(ctx, col, 7)
    for dx in (-w * 0.25, w * 0.25):
        ctx.move_to(dx, -h + 10); ctx.line_to(dx, -10); setc(ctx, dark(col, 0.75)); ctx.set_line_width(8); ctx.stroke()
    ctx.new_path(); ctx.arc(-w * 0.3 + 8, -h * 0.4, 20, 0, 2 * math.pi); fl(ctx, YEL, 3)   # stickers
    rect_r(ctx, w * 0.1, -h * 0.75, 40, 28, 6); fl(ctx, WHITE, 3)
    ctx.restore()


# ------------------------------------------------------------------ street set
def sky(ctx, lf):
    ctx.rectangle(-4000, -3000, 12000, 9000); setc(ctx, hx('8fd8ff')); ctx.fill()
    ellipse(ctx, 980, 520, 80, 80); fl(ctx, hx('fff27a'), 6)
    for cx_, cy_ in ((300 + 0.4 * lf, 470), (1500 + 0.3 * lf, 430), (2500, 500), (-600, 460), (3600, 450)):
        for dx, r in ((-55, 46), (0, 64), (58, 46)):
            ellipse(ctx, cx_ + dx, cy_, r, r * 0.8); fl(ctx, WHITE, 5)


def street(ctx, lf, x0=-1500, x1=5200):
    sky(ctx, lf)
    scenes77.house(ctx, 540, hx('ffe08a'), hx('ff6b5a'), 0, mine=True)
    scenes77.house(ctx, 1980, hx('a8e0ff'), hx('8a5ac8'), 0)
    scenes77.house(ctx, 3420, hx('ffc2d8'), hx('3d8bff'), 0)
    ctx.rectangle(x0, HZ, x1 - x0, ST0 - HZ); setc(ctx, hx('6fd06a')); ctx.fill()
    ctx.move_to(x0, HZ); ctx.line_to(x1, HZ); ink(ctx, 6); ctx.stroke()
    for k in range(-20, 70):
        x = k * 97 % 6600 - 1400; y = HZ + 40 + (k * 53) % 180
        ctx.move_to(x - 12, y); ctx.line_to(x - 4, y - 22); ctx.line_to(x + 4, y); ctx.line_to(x + 12, y - 18)
    setc(ctx, hx('3fa84a')); ctx.set_line_width(5); ctx.stroke()
    # fences between houses + mailbox + tree
    for hx0 in (1080, 2520):
        for k in range(8):
            x = hx0 + k * 52
            poly(ctx, [(x, HZ + 10), (x, HZ - 140), (x + 20, HZ - 162), (x + 40, HZ - 140), (x + 40, HZ + 10)]); fl(ctx, WHITE, 5)
        ctx.rectangle(hx0 - 10, HZ - 100, 430, 20); fl(ctx, WHITE, 4)
    ctx.rectangle(960, HZ + 200 - 170, 16, 170); fl(ctx, hx('8a5a3a'), 4)
    rect_r(ctx, 910, HZ + 200 - 230, 120, 70, 30); fl(ctx, hx('3d8bff'), 5)
    # sidewalk + street
    ctx.rectangle(x0, ST0 - 70, x1 - x0, 70); fl(ctx, hx('e4e0d8'), 5)
    for k in range(-10, 40):
        ctx.move_to(k * 180, ST0 - 70); ctx.line_to(k * 180, ST0)
    setc(ctx, hx('c8c2b8')); ctx.set_line_width(4); ctx.stroke()
    ctx.rectangle(x0, ST0, x1 - x0, ST1 - ST0 + 1000); setc(ctx, hx('6a6f80')); ctx.fill()
    ctx.move_to(x0, ST0); ctx.line_to(x1, ST0); ink(ctx, 6); ctx.stroke()
    for k in range(-10, 40):
        rect_r(ctx, k * 300, 1830, 160, 20, 8); setc(ctx, hx('fff2a8')); ctx.fill()


# ------------------------------------------------------------------ shot 1: hook
def mom_panic(ctx, x, lf, gy=GY):
    shake_ = 5 * math.sin(lf * 2.1)
    wv = 15 * math.sin(lf * 0.8)
    p = P(eye='shock', mouth='scream', lsh=-135 - wv, lel=-10, rsh=135 + wv, rel=10, torso=-3, head=4 * math.sin(lf * 0.9))
    return draw(ctx, x + shake_, gy - 186 * KMOM, KMOM, 1, MOM, p)


def hook(ctx, f, lf):
    ctx.save(); cam(ctx, 570, 1520, 1.3 + 0.04 * eio(pop(lf, 0, 40)), 0, 3 + shake_at(lf, [0], 7, 8), f)
    street(ctx, lf)
    family_car(ctx, 830, GY, 0.85, {'kid': P(eye='glare', mouth='flat'), 'dad': P(eye='glare', mouth='flat')}, lf=lf)
    d = mom_panic(ctx, 390, lf)
    sweat(ctx, d['head'][0] - d['R'] * 1.1, d['head'][1] - d['R'] * 0.6, lf, 0.9)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"DID I TURN OFF", "THE OVEN?!\"", WHITE, t, 112, col2=ORANGE, y=1400)


# ------------------------------------------------------------------ shot 2a: drive off, screech, reverse
def drive(ctx, f, il):
    # il 0..60: 0-24 drive right ; 24 *SCREEECH!* "WAIT!!" ; 32-52 back in REVERSE ; 52 stop at home
    if il < 24:
        x = lerp(760, 2300, eio(il / 26) ** 1.3)
    elif il < 32:
        x = 2300
    else:
        x = lerp(2300, 760, eio(pop(il, 32, 52)))
    camx = lerp(600, x, 0.85)
    ctx.save(); cam(ctx, camx, 1360, 0.95, 0, shake_at(il, [24, 52], 7, 6), f)
    street(ctx, il)
    tilt = -0.07 * math.sin(math.pi * pop(il, 24, 32)) + 0.05 * math.sin(math.pi * pop(il, 52, 58))
    smoke(ctx, x - 200, GY - 30, pop(il, 24, 36), 1.3)
    mv = (il < 24) or (32 <= il < 52)
    faces = {'kid': P(eye='happy', mouth='open'), 'dad': P(eye='happy', mouth='grin'), 'mom': P(eye='happy', mouth='grin')}
    if il >= 22:
        faces = {'kid': P(eye='shock', mouth='open'), 'dad': P(eye='shock', mouth='open'), 'mom': P(eye='shock', mouth='scream')}
    family_car(ctx, x, GY, 0.95, faces, spin=x * 0.02, tilt=tilt, lf=il, bounce=4 * abs(math.sin(il * 0.8)) * mv)
    if il < 24:
        motion_lines(ctx, x - 420, GY - 300, 220, il, 5, 1.0, 1)
    elif 32 <= il < 52:
        motion_lines(ctx, x + 420, GY - 300, 220, il, 5, 1.0, -1)
    ctx.restore()
    if il < 22:
        label(ctx, "\"VACATION!!\"", 540, 1400, 130, GOLD, -0.04, pop(il, 3, 7))
    elif il < 32:
        label(ctx, "*SCREEECH!*", 540, 700, 110, RED, -0.05, pop(il, 24, 27))
        label(ctx, "\"WAIT!!\"", 540, 1400, 150, WHITE, 0.03, pop(il, 24, 27))
    else:
        label(ctx, "*VRRRRM!*", 540, 700, 120, ORANGE, 0.05, pop(il, 32, 35))
        label(ctx, "REVERSE!!", 540, 1400, 130, WHITE, -0.03, pop(il, 33, 36))


# ------------------------------------------------------------------ shot 2b: kitchen
FLOOR = 1500


def kitchen(ctx, lf):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('ffe6a8')); ctx.fill()
    for i in range(-20, 30):                       # wallpaper stars
        for j in range(12):
            x = i * 150 + (j % 2) * 75; y = 300 + j * 110
            ctx.new_path()
            for k in range(10):
                r = 16 if k % 2 == 0 else 7
                a = -math.pi / 2 + k * math.pi / 5
                ctx.line_to(x + r * math.cos(a), y + r * math.sin(a))
            ctx.close_path(); setc(ctx, hx('ffd27a')); ctx.fill()
    # window with curtains
    rect_r(ctx, 640, 540, 300, 260, 14); fl(ctx, hx('bfe8ff'), 8)
    ctx.move_to(790, 540); ctx.line_to(790, 800); ctx.move_to(640, 670); ctx.line_to(940, 670); ink(ctx, 6); ctx.stroke()
    for sx in (0, 1):
        x0 = 620 + sx * 250
        poly(ctx, [(x0, 520), (x0 + 90, 520), (x0 + 60 - 20 * sx, 830), (x0 + 10 + 20 * sx, 830)]); fl(ctx, PINK, 6)
    rect_r(ctx, 610, 510, 360, 24, 10); fl(ctx, hx('c96a2a'), 5)
    # wall clock
    ctx.new_path(); ctx.arc(1080, 400, 60, 0, 2 * math.pi); fl(ctx, WHITE, 7)
    ctx.move_to(1080, 400); ctx.line_to(1080, 360); ctx.move_to(1080, 400); ctx.line_to(1112, 412); ink(ctx, 6); ctx.stroke()
    # doorway left
    rect_r(ctx, 130, 640, 280, FLOOR - 640, 10); fl(ctx, hx('c98a5a'), 8)
    rect_r(ctx, 150, 660, 240, FLOOR - 660, 6); setc(ctx, hx('ffd9a8')); ctx.fill()
    rect_r(ctx, 200, 760, 140, 110, 8); fl(ctx, hx('bfe8ff'), 5)          # picture in the hall
    # counter + cabinets
    ctx.rectangle(430, 1060, 1400, 30); fl(ctx, hx('f4f4f0'), 6)
    ctx.rectangle(430, 1090, 1400, FLOOR - 1090); fl(ctx, hx('7fc4ef'), 7)
    for k in range(4):
        rect_r(ctx, 460 + k * 180, 1120, 150, 330, 10); fl(ctx, hx('9fd6ff'), 5)
        ellipse(ctx, 590 + k * 180, 1280, 9, 9); fl(ctx, GOLD, 3)
    # plant + fruit bowl on the counter
    poly(ctx, [(470, 1060), (550, 1060), (535, 980), (485, 980)]); fl(ctx, ORANGE, 5)
    for a in (-0.6, 0, 0.6):
        ellipse(ctx, 510 + 46 * math.sin(a), 930 - 16 * math.cos(a), 22, 52, a); fl(ctx, GREEN, 4)
    ellipse(ctx, 1140, 1040, 80, 26); fl(ctx, WHITE, 5)
    for k, c in enumerate((RED, YEL, GREEN)):
        ellipse(ctx, 1105 + k * 34, 1010, 24, 24); fl(ctx, c, 4)
    # floor tiles
    ctx.rectangle(-3000, FLOOR, 7000, 2000); setc(ctx, hx('f6d6c2')); ctx.fill()
    for i in range(-20, 30):
        for j in range(8):
            if (i + j) % 2 == 0:
                ctx.rectangle(i * 120, FLOOR + j * 120, 120, 120)
    setc(ctx, hx('ecbfa8')); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 7); ctx.stroke()


OVX = 860


def oven(ctx, x, knob_a=0.0, lf=0):
    """free-standing oven/stove, bottom-centre (x, FLOOR). knob 0 = OFF (pointing up)."""
    rect_r(ctx, x - 200, 1020, 400, FLOOR - 1020, 18); fl(ctx, WHITE, 8)
    ctx.rectangle(x - 200, 1020, 400, 90); fl(ctx, hx('dfe6f2'), 6)
    for k in range(4):                                     # knobs
        kx = x - 140 + k * 94
        ctx.new_path(); ctx.arc(kx, 1065, 24, 0, 2 * math.pi); fl(ctx, hx('3a3a4a') if k else RED, 5)
        a = knob_a if k == 0 else 0.0
        ctx.move_to(kx, 1065); ctx.line_to(kx + 18 * math.sin(a), 1065 - 18 * math.cos(a)); setc(ctx, WHITE); ctx.set_line_width(6); ctx.stroke()
    rect_r(ctx, x - 160, 1150, 320, 240, 14); fl(ctx, hx('2a2840'), 7)        # oven window (cold, dark)
    ctx.move_to(x - 120, 1180); ctx.line_to(x - 60, 1180); setc(ctx, (1, 1, 1, 0.3)); ctx.set_line_width(8); ctx.stroke()
    rect_r(ctx, x - 140, 1125, 280, 16, 8); fl(ctx, hx('c8ccd8'), 4)          # handle
    # stovetop with a kettle
    ctx.rectangle(x - 210, 1000, 420, 24); fl(ctx, hx('3a3a4a'), 5)
    ellipse(ctx, x + 80, 960, 70, 50); fl(ctx, YEL, 6)
    ctx.move_to(x + 140, 950); ctx.line_to(x + 190, 920); ink(ctx, 12); ctx.stroke()


def knob_macro(ctx, cx, cy, Rr, a):
    """big knob with OFF / LOW / HIGH marks"""
    ctx.new_path(); ctx.arc(cx, cy, Rr * 1.55, 0, 2 * math.pi); fl(ctx, hx('dfe6f2'), 8)
    for txt, ang, col in (("OFF", 0.0, GREEN), ("LOW", 1.2, ORANGE), ("HIGH", 2.3, RED)):
        tx = cx + math.sin(ang) * Rr * 1.3; ty = cy - math.cos(ang) * Rr * 1.3
        text(ctx, txt, tx, ty + 10, int(Rr * 0.34), col, ow=0, shadow=False)
    ctx.new_path(); ctx.arc(cx, cy, Rr, 0, 2 * math.pi); fl(ctx, RED, 9)
    ctx.move_to(cx, cy); ctx.line_to(cx + math.sin(a) * Rr * 0.85, cy - math.cos(a) * Rr * 0.85); setc(ctx, WHITE); ctx.set_line_width(Rr * 0.16)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def knob_insert(ctx, f, il):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.08 * eio(il / 24), 0, 0, f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('dfe6f2')); ctx.fill()
    rays(ctx, 540, 960, 260, 900, il * 0.03, col=(0.6, 1, 0.6), a=0.5, n=14)
    knob_macro(ctx, 540, 960, 170, 0.0)
    for j in range(4):
        sparkle(ctx, 540 + (-330, 330, 300, -300)[j], 960 + (-260, -230, 250, 240)[j], 22 + 6 * math.sin(il * 0.6 + j), GOLD)
    ctx.restore()
    label(ctx, "\"...it's OFF.\"", 540, 1420, 140, WHITE, -0.03, pop(il, 2, 6))


def kitchen_shot(ctx, f, il):
    # il 0..80: 0-10 Mom dashes in ; 12-24 she peers at the knob ; 24-48 macro insert (OFF) "...it's OFF." ;
    #           48 back: Mom relieved, Dad in the doorway "TOLD you."
    if 24 <= il < 48:
        knob_insert(ctx, f, il - 24); return
    z = 1.25 if il < 24 else lerp(1.3, 1.22, eio(pop(il, 48, 80)))
    ctx.save(); cam(ctx, 640 if il < 48 else 600, 1140, z, 0, shake_at(il, [8], 6, 6), f)
    kitchen(ctx, il)
    oven(ctx, OVX, 0.0, il)
    if il >= 48:
        draw(ctx, 330, FLOOR - 186 * 1.15, 1.15, 1, DAD, P(eye='smug', mouth='smile', lsh=-30, lel=110, rsh=-30, rel=110, head=-4))
    mx = lerp(-200, OVX - 190, eout(pop(il, 0, 10)))
    lean = 18 if 12 <= il < 48 else 4
    eye = 'shock' if il < 24 else 'happy'
    draw(ctx, mx, FLOOR - 186 * KMOM, KMOM, 1, MOM, P(eye=eye, mouth='open' if il < 24 else 'grin', torso=lean, head=8,
                                                      rsh=60, rel=-40, lsh=-20, lel=-30))
    if il < 10:
        motion_lines(ctx, mx - 260, FLOOR - 420, 200, il, 4, 1.0, 1)
    ctx.restore()
    if il < 24:
        label(ctx, "*SKRRT!*", 540, 560, 110, ORANGE, -0.05, pop(il, 6, 9))
    else:
        label(ctx, "\"TOLD you.\"", 540, 1420, 130, WHITE, 0.03, pop(il, 52, 56))


def s2(ctx, f):
    lf = f - 60
    if lf < 60:
        drive(ctx, f, lf)
    else:
        kitchen_shot(ctx, f, lf - 60)


# ------------------------------------------------------------------ shot 3: top-down MAP
HOMEY, BEACHY = 1500, 420


def road_x(y):
    return 540 + 120 * math.sin((y - 400) / 260.0)


TRIPS = [(0, 36, 0.55, "\"THE DOOR?!\""), (36, 70, 0.42, "\"THE IRON?!\""), (70, 100, 0.28, "\"THE TAP?!\"")]


def car_path(il):
    """returns (x, y, ang, trip_index, turning) for the map car"""
    for j, (t0, t1, reach, _) in enumerate(TRIPS):
        if t0 <= il < t1:
            u = (il - t0) / (t1 - t0)
            off = (j - 1) * 26
            ytop = lerp(HOMEY, BEACHY, reach)
            if u < 0.45:
                v = eio(u / 0.45); y = lerp(HOMEY, ytop, v); return road_x(y) + off - 18, y, 0.0, j, False
            if u < 0.58:
                v = (u - 0.45) / 0.13; return road_x(ytop) + off, ytop - 30 * math.sin(math.pi * v), math.pi * v, j, True
            v = eio((u - 0.58) / 0.42); y = lerp(ytop, HOMEY, v); return road_x(y) + off + 18, y, math.pi, j, False
    return road_x(HOMEY), HOMEY, 0.0, 3, False


def map_bg(ctx, il):
    ctx.rectangle(-2000, -2000, 5000, 6000); setc(ctx, hx('9fe08a')); ctx.fill()
    rnd = random.Random(5)
    for k in range(40):                         # tiny trees
        x = rnd.uniform(-200, 1300); y = rnd.uniform(200, 1800)
        if abs(x - road_x(y)) < 130:
            continue
        ctx.new_path(); ctx.arc(x, y, 22, 0, 2 * math.pi); fl(ctx, hx('3fbf4a'), 4)
    # sea + beach at the top
    ctx.rectangle(-2000, -2000, 5000, 2000 + BEACHY - 120); setc(ctx, hx('4fb8ff')); ctx.fill()
    for k in range(-10, 20):
        ctx.new_path(); ctx.arc(k * 110 + (il * 2) % 110, BEACHY - 130, 55, 0, math.pi); setc(ctx, hx('4fb8ff')); ctx.fill()
    ctx.rectangle(-2000, BEACHY - 120, 5000, 130); setc(ctx, hx('ffe39a')); ctx.fill()
    # beach umbrella icon
    ctx.move_to(780, BEACHY - 20); ctx.line_to(780, BEACHY - 110); ink(ctx, 6); ctx.stroke()
    ctx.new_path(); ctx.arc(780, BEACHY - 110, 60, math.pi, 2 * math.pi); ctx.close_path(); fl(ctx, RED, 5)
    text(ctx, "BEACH", 380, BEACHY - 40, 56, OUT, ow=0, shadow=False)
    # winding road
    ctx.new_path()
    for k in range(60):
        y = BEACHY - 20 + k * (HOMEY + 200 - BEACHY) / 59; ctx.line_to(road_x(y), y)
    setc(ctx, INK); ctx.set_line_width(140); ctx.stroke_preserve(); setc(ctx, hx('7a7f90')); ctx.set_line_width(124); ctx.stroke()
    ctx.new_path()
    for k in range(60):
        y = BEACHY - 20 + k * (HOMEY + 200 - BEACHY) / 59; ctx.line_to(road_x(y), y)
    ctx.set_dash([30, 30]); setc(ctx, hx('fff2a8')); ctx.set_line_width(8); ctx.stroke(); ctx.set_dash([])
    # home icon
    hxm = road_x(HOMEY) + 190
    rect_r(ctx, hxm - 70, HOMEY - 40, 140, 110, 8); fl(ctx, hx('ffe08a'), 6)
    poly(ctx, [(hxm - 90, HOMEY - 30), (hxm, HOMEY - 110), (hxm + 90, HOMEY - 30)]); fl(ctx, hx('ff6b5a'), 6)
    text(ctx, "HOME", hxm, HOMEY + 120, 50, OUT, ow=0, shadow=False)


def map_shot(ctx, f, il):
    # il 0..130
    x, y, a, j, turning = car_path(il)
    ctx.save(); cam(ctx, 560, lerp(1000, 1000, 0), 1.0 + 0.05 * eio(il / 130), -3 + 2 * math.sin(il * 0.05), 0, f)
    map_bg(ctx, il)
    # spaghetti trail of every trip so far
    ctx.set_dash([16, 14])
    for jj, (t0, t1, reach, _) in enumerate(TRIPS):
        if il <= t0:
            continue
        ctx.new_path()
        for s_ in range(t0, min(il, t1) + 1):
            px, py, *_ = car_path(s_)
            ctx.line_to(px, py)
        setc(ctx, (PINK, PURPLE, ORANGE)[jj]); ctx.set_line_width(10); ctx.stroke()
    ctx.set_dash([])
    from scenes60 import car_top
    car_top(ctx, x, y, 0.75, CARCOL, a)
    if turning:
        smoke(ctx, x, y + 40, 0.5, 0.6)
    ctx.restore()
    for jj, (t0, t1, reach, txt) in enumerate(TRIPS):
        tt = t0 + (t1 - t0) * 0.45
        if tt - 1 <= il < t1 - 2:
            label(ctx, txt, 540, 1400, 130, WHITE, (-0.04, 0.04, -0.03)[jj], pop(il, tt - 1, tt + 2))
            label(ctx, "*SCREECH!*", 540, 720, 90, RED, 0.05, pop(il, tt - 1, tt + 2)) if il < tt + 8 else None
    if il >= 102:
        label2(ctx, "1 HOUR LATER:", "0 MILES.", WHITE, pop(il, 102, 106), 115, col2=RED, y=1360)


def s3(ctx, f):
    map_shot(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: Dad ECU (the one close-up)
def car_interior(ctx, il, scroll=0.0):
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('8fd8ff')); ctx.fill()
    # passing scenery through the side window
    for k in range(-2, 8):
        x = ((k * 360 - scroll) % 2880) - 600
        ctx.rectangle(x, 760, 26, 160); fl(ctx, hx('8a5a2a'), 4)
        ellipse(ctx, x + 13, 720, 90, 100); fl(ctx, hx('3fbf4a'), 6)
    ctx.rectangle(-600, 900, 2400, 400); setc(ctx, hx('6fd06a')); ctx.fill()
    # window frame / seat
    ctx.rectangle(-600, -600, 2400, 760); setc(ctx, hx('3a3f55')); ctx.fill()
    rect_r(ctx, -40, 150, 1160, 900, 60); ink(ctx, 14); ctx.stroke()
    ctx.rectangle(-600, 1250, 2400, 1600); setc(ctx, hx('3a3f55')); ctx.fill()
    rect_r(ctx, 200, 700, 680, 900, 140); fl(ctx, hx('ff8a6a'), 8)         # seat back
    ctx.move_to(260, 1000); ctx.line_to(820, 1000); setc(ctx, hx('e06a50')); ctx.set_line_width(8); ctx.stroke()


def wheel(ctx, x, y, r, rot):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.new_path(); ctx.arc(0, 0, r, 0, 2 * math.pi); setc(ctx, INK); ctx.set_line_width(64); ctx.stroke()
    ctx.new_path(); ctx.arc(0, 0, r, 0, 2 * math.pi); setc(ctx, hx('2a2a3a')); ctx.set_line_width(46); ctx.stroke()
    for a in (0.0, 2.1, -2.1):
        ctx.move_to(0, 0); ctx.line_to(math.sin(a) * r, math.cos(a) * r); setc(ctx, hx('2a2a3a')); ctx.set_line_width(36); ctx.stroke()
    ctx.new_path(); ctx.arc(0, 0, 60, 0, 2 * math.pi); fl(ctx, hx('5a5a6a'), 6)
    ctx.restore()


def dad_ecu(ctx, f, il, lines, mood=0):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eio(il / 70), 0, 2 + shake_at(il, [0, 30], 6, 8), f)
    car_interior(ctx, il, il * 40)
    face(ctx, DAD, P(eye='glare', mouth='flat' if mood == 0 else 'wavy'), 540, 900, 200, 0.0)
    twitch(ctx, 540 + 200 * 0.95, 900 - 200 * 0.7, il, 1.6)
    sweat(ctx, 540 - 230, 760, il, 1.4)
    # hands gripping the wheel
    wheel(ctx, 540, 1460, 330, 0.08 * math.sin(il * 0.7))
    for sx in (-1, 1):
        ellipse(ctx, 540 + sx * 300, 1230, 56, 64); fl(ctx, DAD['skin'], 6)
    ctx.restore()
    if len(lines) == 1:
        label(ctx, lines[0], 540, 1430, 150, WHITE, -0.03, pop(il, 3, 7))
    else:
        if il < 30:
            label(ctx, lines[0], 540, 1430, 160, WHITE, -0.03, pop(il, 3, 7))
        else:
            label(ctx, lines[1], 540, 1430, 160, RED, 0.03, pop(il, 30, 33))


def s4(ctx, f):
    dad_ecu(ctx, f, f - 330, ["\"NO. MORE.\"", "\"U-TURNS.\""])


# ------------------------------------------------------------------ shot 5: twist -> loop
def hills(ctx, scroll):
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, hx('8fd8ff')); ctx.fill()
    ellipse(ctx, 900, 560, 80, 80); fl(ctx, hx('fff27a'), 6)
    for k in range(-3, 9):
        hx_ = ((k * 520 - scroll * 0.25) % 4160) - 1200
        ellipse(ctx, hx_, 1320, 420, 260); fl(ctx, hx('8fdc6a') if k % 2 else hx('7ccf5c'), 7)
    for k in range(-3, 12):
        tx = ((k * 330 + 90 - scroll * 0.6) % 4950) - 1300
        ctx.rectangle(tx - 14, 1300, 28, 120); fl(ctx, hx('8a5a2a'), 5)
        ellipse(ctx, tx, 1260, 70, 80); fl(ctx, hx('3fbf4a'), 6)
    ctx.rectangle(-3000, 1400, 9000, 80); setc(ctx, hx('6cc24a')); ctx.fill()
    ctx.rectangle(-3000, ST0, 9000, 2000); setc(ctx, hx('6a6f80')); ctx.fill()
    ctx.move_to(-3000, ST0); ctx.line_to(6000, ST0); ink(ctx, 7); ctx.stroke()
    for k in range(-3, 14):
        x = ((k * 300 - scroll) % 4200) - 1200
        rect_r(ctx, x, 1830, 160, 20, 8); setc(ctx, hx('fff2a8')); ctx.fill()


def road_sign(ctx, x, txt):
    ctx.rectangle(x - 10, 1080, 20, 400); fl(ctx, hx('9aa4b8'), 5)
    rect_r(ctx, x - 190, 960, 380, 140, 16); fl(ctx, GREEN, 7)
    text(ctx, txt, x, 1050, 60, WHITE, ow=0, shadow=False)


def highway(ctx, f, il):
    # il 0..70: car cruising right, scenery scrolls; 6 "FINALLY!!" ; 30 PLOT TWIST card ; 40 kid asks ; 58 shock
    zoom = lerp(1.05, 1.35, eio(pop(il, 34, 50)))
    cx = lerp(540, 480, eio(pop(il, 34, 50)))
    ctx.save(); cam(ctx, cx, 1480, zoom, 0, shake_at(il, [58], 6, 6), f)
    hills(ctx, il * 60)
    road_sign(ctx, 1500 - il * 60 * 0.9, "BEACH  1 mi")
    shock = il >= 58
    faces = {'kid': P(eye='shock' if shock else 'normal', mouth='open' if il >= 40 else 'smile', head=-6),
             'mom': P(eye='shock' if shock else 'happy', mouth='scream' if shock else 'grin'),
             'dad': P(eye='shock' if shock else 'happy', mouth='scream' if shock else 'grin')}
    family_car(ctx, 540, GY, 1.0, faces, spin=il * 0.9, lf=il, bounce=4 * abs(math.sin(il * 0.8)))
    motion_lines(ctx, 100, GY - 300, 220, il, 5, 0.9, 1)
    ctx.restore()
    if il < 36:
        label(ctx, "\"FINALLY!!\"", 540, 1400, 150, GOLD, -0.04, pop(il, 6, 10))
    elif il < 58:
        label2(ctx, "\"Mom... where are", "the SUITCASES?\"", WHITE, pop(il, 40, 44), 100, col2=CYAN, y=1400)
    else:
        label(ctx, "\"...!!!\"", 540, 1400, 160, RED, 0.04, pop(il, 58, 61))
    card(ctx, 'p2', il, 28)


def home_cases(ctx, f, il):
    # il 0..60: home lawn, the suitcases stacked on the sidewalk, the dog sitting on top *WOOF?*
    ctx.save(); cam(ctx, 560, 1300, lerp(1.15, 1.35, eio(il / 60)), 0, 0, f)
    street(ctx, il)
    base = ST0 - 20
    suitcase(ctx, 560, base, 360, 220, PURPLE)
    suitcase(ctx, 545, base - 230, 300, 190, ORANGE, -0.03)
    suitcase(ctx, 570, base - 430, 240, 160, RED, 0.04)
    ctx.save(); ctx.translate(560, base - 600); ctx.rotate(0.15 * math.sin(il * 0.3) if il >= 20 else 0)
    dog(ctx, 0, 0, 0.62, 1, il)
    ctx.restore()
    # beach ball + sunhat left behind too
    ctx.new_path(); ctx.arc(260, base - 70, 70, 0, 2 * math.pi); fl(ctx, WHITE, 6)
    for k, c in enumerate((RED, BLUE, YEL)):
        ctx.new_path(); ctx.arc(260, base - 70, 70, k * 2.1, k * 2.1 + 1.0); ctx.line_to(260, base - 70); ctx.close_path(); setc(ctx, c); ctx.fill()
    ctx.restore()
    if il >= 18:
        label(ctx, "*WOOF?*", 540, 1400, 140, GOLD, -0.04, pop(il, 18, 21))


def uturn(ctx, f, il):
    # il 0..50 wide highway: brake, the car spins round *SCREEECH!!* and blasts back the other way
    flip = eio(pop(il, 6, 20))
    f_ = math.cos(math.pi * flip)
    x = 540 if il < 20 else lerp(540, -800, eio(pop(il, 22, 46)) ** 1.5)
    ctx.save(); cam(ctx, 540, 1400, 1.0, 0, shake_at(il, [6], 8, 8), f)
    hills(ctx, 1000 - 40 * max(0, il - 22))
    for k in range(int(min(il, 20))):     # skid circle
        a = k * 0.3
        ellipse(ctx, 540 + 260 * math.cos(a) * 0.9, GY - 10 + 30 * math.sin(a), 30, 10); setc(ctx, (0.15, 0.15, 0.2, 0.5)); ctx.fill()
    smoke(ctx, 540 + 240, GY - 40, pop(il, 6, 24), 1.6)
    smoke(ctx, 540 - 240, GY - 40, pop(il, 8, 26), 1.6)
    faces = {'kid': P(eye='happy', mouth='open'), 'mom': P(eye='shock', mouth='open'), 'dad': P(eye='glare', mouth='flat')}
    family_car(ctx, x, GY, 1.0, faces, spin=-il, tilt=0.05 * math.sin(il * 0.9) * (il < 22), f_=f_ if abs(f_) > 0.08 else 0.08 * (1 if f_ >= 0 else -1), lf=il)
    if il >= 22:
        motion_lines(ctx, x + 420, GY - 300, 240, il, 5, 1.0, -1)
    ctx.restore()
    label(ctx, "*SCREEEECH!!*", 540, 700, 110, RED, -0.05, pop(il, 6, 9))


def s5(ctx, f):
    lf = f - 400
    if lf < 70:
        highway(ctx, f, lf)
    elif lf < 130:
        home_cases(ctx, f, lf - 70)
    elif lf < 180:
        dad_ecu(ctx, f, lf - 130, ["\"...U-TURN.\""], mood=1)
    elif lf < 230:
        uturn(ctx, f, lf - 180)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (200, s3), (330, s4), (400, s5)]
CUTS = (60, 120, 200, 330, 400, 470, 530, 580, 630)


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
                              "-i", "out/did_i_turn_off_the_oven_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
