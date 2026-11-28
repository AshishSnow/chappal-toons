"""'MOM SITS DOWN FOR ONE MINUTE'. Original, general-audience comedy short, 22s.
Hook:   cosy living-room medium shot: Mom has JUST sat down on the sofa with her tea, tea splashing, frazzled -
        the kid tugs her arm "MOM! MOM!", the dog drops its leash at her feet *WOOF!*, Dad calls from the doorway
        "HONEY?!" -> Mom "I JUST... SAT DOWN!!" + caption 'MOM SITS DOWN FOR ONE MINUTE:'.
Beat 1: "FINALLY... ME TIME." she sinks into the cushions with tea + book, sparkles *ahhh~* -> *sip* -> the kid pops up
        from behind the sofa "MOM! I'm HUNGRY!"
Beat 2: Dutch-tilt yo-yo montage: Mom up / *FLOMP* down / up ... "Here's a SNACK." -> Dad "Where are my KEYS?!"
        -> "...in your HAND." -> dog with leash *WOOF! WOOF!* -> "...ask your DAD." -> kid "Where's my SHOE?!"
        -> "...on your FOOT."
Beat 3: macro on the mug: she finally sips *sip* ... frost creeps over the tea "...it's COLD." *cricket*
Close-up (the one face shot): twitching Mom "I just want..." "...ONE MINUTE!!"
Twist:  Dad herds kid + dog out "Okay! Everybody OUT!" *CLICK* -> silence -> "...ahhh. PEACE." -> she glances around
        "...too QUIET." -> grabs her phone -> PLOT TWIST: MOM CALLS HER MOM. split screen: Mom bouncing "MOM! MOM! MOM!"
        / Grandma just sitting down with HER tea, phone ringing "...I JUST SAT DOWN." -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face, rays
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes65 import dog
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
TEAL = hx('19b8b0'); TEA = hx('c98a4a'); ICE = hx('c9f1ff')
MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'), pants=hx('3d5a9e'), shoes=hx('ffffff'))
DAD = dict(doodle.DAD, shirt=hx('1f8bff'), pants=hx('4a4f6a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ffc93c'), pants=hx('22b45a'), shoes=hx('ff4d5e'))
GRAN = dict(doodle.NMOM, hair=hx('dcdce6'), shirt=hx('b98cff'), pants=hx('5a4a8a'), shoes=hx('ff6b8a'), glasses=hx('8a3cff'))
N = 660
FLOOR, GND = 1560, 1595
SEAT = 1400
KM, KK, KD, KG = 1.1, 0.85, 1.05, 1.05
SX0, SX1 = 680, 1180          # sofa
MX = 950                      # Mom's seat x
DX0, DX1, DTOP = 1290, 1500, 940   # doorway

CAPS = {'p1': [[("MOM SITS DOWN", PINK)], [("FOR ", OUT), ("ONE MINUTE:", BLUE)]],
        'p2': [[("PLOT TWIST:", RED)], [("MOM CALLS ", OUT), ("HER MOM.", PURPLE)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def mug(ctx, x, y, s=1.0, lf=0, steam=1.0, col=hx('7fd6ff'), tilt=0.0, frost=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(tilt); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(30, -4, 16, -1.5, 1.5); ink(ctx, 16); ctx.stroke()
    ctx.new_path(); ctx.arc(30, -4, 16, -1.5, 1.5); setc(ctx, col); ctx.set_line_width(8); ctx.stroke()
    rect_r(ctx, -30, -34, 60, 64, 14); fl(ctx, col, 5)
    ellipse(ctx, 0, -34, 28, 8); fl(ctx, TEA if frost < 0.5 else ICE, 3)
    heart(ctx, 0, -4, 11, WHITE)
    if frost > 0:
        for k in range(7):
            a = k * 0.9
            sparkle(ctx, 22 * math.cos(a), -10 + 22 * math.sin(a), 9 * frost, ICE)
    ctx.restore()
    if steam > 0:
        for k in range(2):
            ox = x - 10 * s + 20 * k * s
            ctx.move_to(ox, y - 44 * s); ctx.curve_to(ox - 14 * s, y - 66 * s - 6 * math.sin(lf * 0.2 + k), ox + 14 * s, y - 82 * s, ox, y - 106 * s)
        setc(ctx, (1, 1, 1, 0.85 * steam)); ctx.set_line_width(6 * s); ctx.stroke()


def heart(ctx, x, y, r, col=PINK):
    ctx.new_path(); ctx.move_to(x, y + r * 0.7); ctx.curve_to(x - r * 1.4, y - r * 0.3, x - r * 0.5, y - r * 1.3, x, y - r * 0.4)
    ctx.curve_to(x + r * 0.5, y - r * 1.3, x + r * 1.4, y - r * 0.3, x, y + r * 0.7); setc(ctx, col); ctx.fill()


def book(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-60, -40), (0, -30), (0, 40), (-60, 30)]); fl(ctx, hx('fff6e0'), 4)
    poly(ctx, [(60, -40), (0, -30), (0, 40), (60, 30)]); fl(ctx, hx('fff6e0'), 4)
    for k in range(3):
        ctx.move_to(-50, -20 + k * 16); ctx.line_to(-10, -14 + k * 16); ctx.move_to(10, -14 + k * 16); ctx.line_to(50, -20 + k * 16)
    setc(ctx, hx('c9bfa8')); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()


def keys(ctx, x, y, s=1.0, lf=0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(0.3 * math.sin(lf * 0.5)); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 12, 0, 2 * math.pi); ink(ctx, 5); ctx.stroke()
    for k, c in enumerate((GOLD, hx('c9d2e0'))):
        ctx.save(); ctx.rotate(-0.5 + k * 0.9)
        rect_r(ctx, -7, 10, 14, 44, 5); fl(ctx, c, 3); ctx.restore()
    ctx.restore()


def phone(ctx, x, y, a=0.3, s=1.0, ring=0.0, lf=0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a + (0.12 * math.sin(lf * 2.2) if ring else 0)); ctx.scale(s, s)
    rect_r(ctx, -30, -60, 60, 120, 12); fl(ctx, hx('2a2a3a'), 4)
    rect_r(ctx, -22, -50, 44, 96, 7); setc(ctx, hx('6be2ff') if not ring else hx('9dffb0')); ctx.fill()
    heart(ctx, 0, -6, 14, PINK)
    ctx.restore()
    if ring:
        for k in range(3):
            ctx.new_path(); ctx.arc(x, y, 80 * s + k * 26 * s, -0.7, 0.7); ink(ctx, 5); ctx.stroke()
            ctx.new_path(); ctx.arc(x, y, 80 * s + k * 26 * s, math.pi - 0.7, math.pi + 0.7); ink(ctx, 5); ctx.stroke()


def snack(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for k, (cx_, cy_) in enumerate(((-28, -20), (0, -28), (26, -18))):
        ellipse(ctx, cx_, cy_, 18, 14); fl(ctx, hx('ff8a5c') if k != 1 else hx('ffd23f'), 3)
    ctx.new_path(); ctx.move_to(-56, -14); ctx.curve_to(-46, 36, 46, 36, 56, -14); ctx.close_path(); fl(ctx, MINT, 5)
    ctx.restore()


def leash(ctx, x0, y0, x1, y1, sag=60):
    ctx.new_path(); ctx.move_to(x0, y0); ctx.curve_to(x0, y0 + sag, x1, y1 + sag, x1, y1)
    ink(ctx, 14); ctx.stroke_preserve(); setc(ctx, RED); ctx.set_line_width(7); ctx.stroke()
    ellipse(ctx, x1, y1, 16, 12); fl(ctx, RED, 4)


# ------------------------------------------------------------------ set: cosy living room
def living(ctx, lf, door=1.0, gran_room=False):
    wall = hx('fff0c9') if not gran_room else hx('ffe0e8')
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, wall); ctx.fill()
    rnd = random.Random(112 + gran_room)
    for k in range(80):   # little stars / hearts wallpaper
        x, y = rnd.uniform(-300, 2400), rnd.uniform(300, 1520)
        if k % 2:
            sparkle(ctx, x, y, 10, dark(wall, 0.9))
        else:
            heart(ctx, x, y, 8, dark(wall, 0.9))
    # floor + skirting
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('dca878')); ctx.fill()
    for k in range(-30, 60):
        ctx.move_to(k * 110, FLOOR); ctx.line_to(k * 110 - 300, FLOOR + 900)
    setc(ctx, hx('c99464')); ctx.set_line_width(4); ctx.stroke()
    rect_r(ctx, -3000, FLOOR - 22, 9000, 24, 4); fl(ctx, WHITE, 4)
    if not gran_room:
        # window with curtains (left)
        rect_r(ctx, 300, 800, 280, 360, 12); fl(ctx, WHITE, 6)
        ctx.set_source(vgrad(ctx, 0, 820, 0, 1140, [(0, hx('8fd8ff')), (1, hx('d8f4ff'))])); rect_r(ctx, 318, 818, 244, 324, 8); ctx.fill()
        ellipse(ctx, 400, 900, 40, 18); setc(ctx, WHITE); ctx.fill(); ellipse(ctx, 440, 890, 30, 16); ctx.fill()
        ctx.move_to(440, 818); ctx.line_to(440, 1142); ctx.move_to(318, 980); ctx.line_to(562, 980); ink(ctx, 5); ctx.stroke()
        for cx_ in (270, 610):
            poly(ctx, [(cx_ - 40, 780), (cx_ + 40, 780), (cx_ + 50, 1200), (cx_ - 50, 1200)]); fl(ctx, hx('ff8fb8'), 5)
        rect_r(ctx, 200, 768, 480, 18, 8); fl(ctx, hx('a8683e'), 4)
        # picture frames over the sofa
        for (fx, fy, w, h, c) in ((800, 900, 150, 120, GOLD), (990, 870, 120, 150, MINT)):
            rect_r(ctx, fx - w / 2, fy - h / 2, w, h, 8); fl(ctx, c, 5)
            rect_r(ctx, fx - w / 2 + 14, fy - h / 2 + 14, w - 28, h - 28, 5); fl(ctx, hx('dff4ff'), 3)
        poly(ctx, [(739, 945), (780, 890), (810, 925), (835, 900), (861, 945)]); fl(ctx, GREEN, 3)
        heart(ctx, 990, 870, 26, RED)
        # wall clock
        ellipse(ctx, 1130, 820, 50, 50); fl(ctx, WHITE, 5)
        ctx.move_to(1130, 820); ctx.line_to(1130 + 30 * math.sin(lf * 0.2), 820 - 30 * math.cos(lf * 0.2)); ctx.move_to(1130, 820); ctx.line_to(1150, 830); ink(ctx, 5); ctx.stroke()
        # doorway (right) with hallway beyond + door
        rect_r(ctx, DX0 - 22, DTOP - 22, DX1 - DX0 + 44, FLOOR - DTOP + 22, 10); fl(ctx, WHITE, 5)
        ctx.rectangle(DX0, DTOP, DX1 - DX0, FLOOR - DTOP); setc(ctx, hx('c9b8ff')); ctx.fill()
        # bookshelf (far right)
        rect_r(ctx, 1560, 1040, 240, 520, 10); fl(ctx, hx('c98a52'), 5)
        for r in range(3):
            y = 1080 + r * 160
            for k in range(5):
                c = (RED, BLUE, GOLD, MINT, PURPLE)[(k + r) % 5]
                rect_r(ctx, 1580 + k * 42, y + 10 * (k % 2), 34, 120 - 10 * (k % 2), 4); fl(ctx, c, 3)
            ctx.move_to(1560, y + 132); ctx.line_to(1800, y + 132); ink(ctx, 5); ctx.stroke()
        # plant (left) + side table + lamp
        rect_r(ctx, 150, 1440, 110, 120, 16); fl(ctx, hx('ff8a5c'), 5)
        for a in (-0.9, -0.4, 0.1, 0.6, 1.0):
            ellipse(ctx, 205 + 80 * math.sin(a), 1390 - 60 * math.cos(a), 22, 54, a); fl(ctx, GREEN, 3)
        rect_r(ctx, 520, 1330, 140, 26, 8); fl(ctx, hx('c98a52'), 4)
        rect_r(ctx, 576, 1350, 28, 210, 6); fl(ctx, hx('a8683e'), 4)
        ctx.move_to(560, 1330); ctx.line_to(560, 1180); ink(ctx, 7); ctx.stroke()
        poly(ctx, [(490, 1190), (630, 1190), (600, 1090), (520, 1090)]); fl(ctx, YEL, 4)
        # rug + dog bed
        ellipse(ctx, 980, FLOOR + 110, 480, 66); fl(ctx, hx('8ad0ff'), 5)
        ellipse(ctx, 980, FLOOR + 110, 380, 44); setc(ctx, hx('c6ecff')); ctx.fill()
        ellipse(ctx, 1330, FLOOR + 40, 110, 30); fl(ctx, hx('ffb347'), 5)
        ellipse(ctx, 1330, FLOOR + 30, 80, 16); setc(ctx, hx('ffd9a0')); ctx.fill()
    else:
        # Grandma's room: lace curtains window, framed photo of little Mom, cuckoo clock, yarn basket
        rect_r(ctx, 640, 820, 260, 320, 12); fl(ctx, WHITE, 6)
        ctx.set_source(vgrad(ctx, 0, 838, 0, 1122, [(0, hx('ffb38a')), (1, hx('ffe2b8'))])); rect_r(ctx, 658, 838, 224, 284, 8); ctx.fill()
        ctx.move_to(770, 838); ctx.line_to(770, 1122); ctx.move_to(658, 980); ctx.line_to(882, 980); ink(ctx, 5); ctx.stroke()
        for k in range(9):
            ellipse(ctx, 650 + k * 30, 836, 16, 12); fl(ctx, WHITE, 3)
        rect_r(ctx, 1080, 860, 150, 170, 8); fl(ctx, GOLD, 5)
        rect_r(ctx, 1094, 874, 122, 142, 5); fl(ctx, hx('dff4ff'), 3)
        ctx.save(); ctx.translate(1155, 960); ctx.scale(0.3, 0.3)
        face(ctx, dict(KID, hair=MOM['hair'], hairstyle='mom', skin=MOM['skin']), P(eye='happy', mouth='grin'), 0, 0, 160)
        ctx.restore()
        # cuckoo clock
        poly(ctx, [(1300, 840), (1380, 780), (1460, 840)]); fl(ctx, hx('a8683e'), 5)
        rect_r(ctx, 1310, 840, 140, 150, 8); fl(ctx, hx('c98a52'), 5)
        ellipse(ctx, 1380, 900, 40, 40); fl(ctx, WHITE, 4)
        ctx.move_to(1380, 900); ctx.line_to(1380, 872); ctx.move_to(1380, 900); ctx.line_to(1400, 908); ink(ctx, 4); ctx.stroke()
        ctx.move_to(1360, 990); ctx.line_to(1360, 1080 + 10 * math.sin(lf * 0.3)); ctx.move_to(1400, 990); ctx.line_to(1400, 1060); ink(ctx, 4); ctx.stroke()
        # rug
        ellipse(ctx, 1000, FLOOR + 110, 460, 66); fl(ctx, hx('c7a2ff'), 5)
        ellipse(ctx, 1000, FLOOR + 110, 360, 44); setc(ctx, hx('e2d0ff')); ctx.fill()
        # yarn basket
        rect_r(ctx, 1270, 1460, 170, 100, 20); fl(ctx, hx('e8c48a'), 5)
        for k, c in enumerate((RED, MINT, GOLD)):
            ellipse(ctx, 1300 + k * 52, 1452, 30, 30); fl(ctx, c, 4)
        ctx.move_to(1320, 1440); ctx.line_to(1400, 1370); ctx.move_to(1350, 1440); ctx.line_to(1300, 1360); ink(ctx, 5); ctx.stroke()


def room_door(ctx, door):
    """the door inside the doorway; door 1 = wide open (folded to the jamb), 0 = shut"""
    w = (DX1 - DX0) * (1 - 0.86 * door)
    ctx.rectangle(DX0, DTOP, w, FLOOR - DTOP); fl(ctx, hx('ff8a5c'), 5)
    if door < 0.6:
        rect_r(ctx, DX0 + w * 0.2, DTOP + 60, w * 0.6, 220, 14); fl(ctx, hx('ffb38a'), 4)
        rect_r(ctx, DX0 + w * 0.2, DTOP + 340, w * 0.6, 220, 14); fl(ctx, hx('ffb38a'), 4)
        ellipse(ctx, DX0 + w * 0.85, DTOP + 320, 12, 12); fl(ctx, GOLD, 3)


def sofa_back(ctx):
    rect_r(ctx, SX0, 1170, SX1 - SX0, 260, 46); fl(ctx, hx('7a6cff'), 6)


def sofa_front(ctx, cush=True):
    if cush:
        for k, (c, x) in enumerate(((GOLD, SX0 + 60), (MINT, SX1 - 170))):
            rect_r(ctx, x, 1220 + k * 8, 110, 100, 28); fl(ctx, c, 5)
    rect_r(ctx, SX0 + 20, SEAT, SX1 - SX0 - 40, 100, 26); fl(ctx, hx('9a8cff'), 5)
    for xx in (SX0 - 30, SX1 - 50):
        rect_r(ctx, xx, 1300, 80, 230, 30); fl(ctx, hx('6a5cee'), 5)
    for xx in (SX0 + 10, SX1 - 30):
        rect_r(ctx, xx, 1525, 20, 40, 6); fl(ctx, hx('8a5a3a'), 3)


def armchair(ctx, x):
    rect_r(ctx, x - 170, SEAT - 240, 340, 300, 60); fl(ctx, hx('ff8fb8'), 6)
    rect_r(ctx, x - 140, SEAT - 6, 280, 120, 26); fl(ctx, hx('ffb3cf'), 5)
    for xx in (x - 210, x + 140):
        rect_r(ctx, xx, SEAT - 70, 70, 220, 28); fl(ctx, hx('ff6fa0'), 5)
    for lx in (x - 160, x + 140):
        rect_r(ctx, lx, SEAT + 140, 22, FLOOR - SEAT - 130, 6); fl(ctx, hx('5a3a2a'), 3)
    # doily
    for k in range(7):
        ellipse(ctx, x - 90 + k * 30, SEAT - 236, 16, 12); fl(ctx, WHITE, 3)


# ------------------------------------------------------------------ people
def stand(ctx, ch, x, k, p, f_=1, g=GND):
    return draw(ctx, x, g - 186 * k, k, f_, ch, p)


SIT = dict(lhip=85, lkn=-88, rhip=80, rkn=-84)


def mom_sit(ctx, x, eye, mouth, lsh=-40, lel=-30, rsh=60, rel=-100, torso=0, head=0, sink=0.0, f_=1, rot=0, ch=None):
    p = P(eye=eye, mouth=mouth, lsh=lsh, lel=lel, rsh=rsh, rel=rel, torso=torso, head=head, rot=rot, **SIT)
    return draw_hip(ctx, x, SEAT + 6 + sink, KM if ch is None else KG, f_, ch or MOM, p)


def splash(ctx, x, y, lf, s=1.0):
    for k in range(5):
        a = -2.4 + k * 0.4
        r = 50 + (lf * 9 + k * 13) % 60
        ellipse(ctx, x + r * math.cos(a) * s, y + r * math.sin(a) * s, 10 * s, 13 * s); fl(ctx, TEA, 3)


# ------------------------------------------------------------------ shot 1: hook
def hook_scene(ctx, lf):
    living(ctx, lf)
    dd = stand(ctx, DAD, 1395, KD, P(eye='shock', mouth='open', lsh=20, lel=-40, rsh=60, rel=-60, head=-6), -1)
    keys(ctx, dd['front'][0], dd['front'][1] + 10, 1.2, lf)
    room_door(ctx, 1.0)
    sofa_back(ctx)
    sofa_front(ctx)
    jig = 6 * math.sin(lf * 1.3)
    m = mom_sit(ctx, MX, 'shock', 'scream', lsh=-75, lel=-10, rsh=95, rel=-70, torso=-4 + jig * 0.3, head=jig * 0.6)
    mug(ctx, m['front'][0] + 6, m['front'][1] - 24, 1.0, lf, 0.6, tilt=0.25 * math.sin(lf * 0.9))
    splash(ctx, m['front'][0] + 10, m['front'][1] - 70, lf)
    sweat(ctx, m['head'][0] + m['R'] * 1.05, m['head'][1] - m['R'] * 0.4, lf, 0.9)
    tug = 10 * math.sin(lf * 0.9)
    k = stand(ctx, KID, 730 + tug, KK, P(eye='happy', mouth='scream', lsh=110, lel=-20, rsh=95, rel=-10, torso=-10, head=4), 1)
    dog(ctx, 1150, GND - 10, 0.5, -1, lf)
    leash(ctx, 1150 - 0.5 * 205, GND - 10 - 0.5 * 175, 1040, GND - 20, 30)
    return m


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    z = 1.06 + 0.03 * eio(pop(lf, 0, 54))
    ctx.save(); cam(ctx, 1010, 1300, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    hook_scene(ctx, lf)
    ctx.restore()
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"I JUST...", "SAT DOWN!!\"", WHITE, t, 120, col2=PINK, y=1440)
    if lf < 60:
        b = (lf // 8) % 3
        label(ctx, "\"MOM! MOM!\"", 250, 640, 62, YEL, -0.12, 1 if lf == f else pop(lf, 2, 5))
        label(ctx, "*WOOF!*", 760, 1300, 58, GOLD, 0.06, 1 if lf == f else pop(lf, 4, 7))
        label(ctx, "\"HONEY?!\"", 870, 720, 62, CYAN, 0.1, 1 if lf == f else pop(lf, 6, 9))


# ------------------------------------------------------------------ shot 2: me time -> kid pops up
def s2(ctx, f):
    il = f - 60   # 0..80
    z = 1.2 + 0.1 * eio(il / 50)
    ctx.save(); cam(ctx, 950, 1250, z, 0, shake_at(il, [50], 10, 14), f)
    living(ctx, il)
    room_door(ctx, 1.0)
    pk = eout(pop(il, 50, 56))
    if il >= 50:   # kid popping up from behind the sofa
        ctx.save(); ctx.rectangle(0, 0, 3000, 1300); ctx.clip()
        stand(ctx, KID, 1170, KK, P(eye='happy', mouth='scream', lsh=160, lel=-20, rsh=170, rel=-10, head=6), -1, GND + 60 - 320 * pk)
        ctx.restore()
    sofa_back(ctx)
    sofa_front(ctx)
    sink = 14 * eio(pop(il, 0, 16))
    if il < 50:
        sip = il >= 30
        m = mom_sit(ctx, MX, 'closed', 'smile', lsh=60, lel=-110, rsh=110 if sip else 70, rel=-140 if sip else -100, torso=-10, head=8, sink=sink)
        book(ctx, m['back'][0] + 10, m['back'][1] - 10, 0.9, -0.2)
        mug(ctx, m['front'][0] + 4, m['front'][1] - 24, 0.95, il, 1.0)
        for j in range(3):
            sparkle(ctx, m['head'][0] - 150 + j * 150, m['head'][1] - m['R'] * 1.3 - 10 * math.sin(il * 0.2 + j), 18, YEL)
    else:
        m = mom_sit(ctx, MX, 'shock', 'open', lsh=60, lel=-110, rsh=110, rel=-140, torso=-4, head=-8, sink=sink)
        book(ctx, m['back'][0] + 10, m['back'][1] - 10, 0.9, -0.2)
        mug(ctx, m['front'][0] + 4, m['front'][1] - 24, 0.95, il, 0.4, tilt=0.3)
        splash(ctx, m['front'][0] + 20, m['front'][1] - 70, il)
    ctx.restore()
    if il < 30:
        label2(ctx, "\"FINALLY...", "ME TIME.\"", WHITE, pop(il, 2, 6), 120, col2=MINT, y=1440)
        label(ctx, "*ahhh~*", 540, 600, 90, YEL, 0.04, pop(il, 8, 12))
    elif il < 50:
        label(ctx, "*sip*", 540, 600, 100, CYAN, -0.04, pop(il, 30, 33))
    else:
        label(ctx, "\"MOM! I'm HUNGRY!\"", 540, 1440, 104, YEL, -0.03, pop(il, 50, 53))


# ------------------------------------------------------------------ shot 3: the yo-yo montage
ANS = ["\"Here's a SNACK.\"", "\"...in your HAND.\"", "\"...ask your DAD.\"", "\"...on your FOOT.\""]
CALL = [("\"HONEY! Where", "are my KEYS?!\""), ("*WOOF!", "WOOF!*"), ("\"MOM! Where's", "my SHOE?!\""), None]


def s3(ctx, f):
    il = f - 140   # 0..140
    i, c = min(3, il // 35), il % 35 if il < 140 else 34
    up_ = c < 12
    flomp = 35 * i + 12
    ctx.save(); cam(ctx, 1000, 1290, 1.0, 7, shake_at(il, [12, 47, 82, 117], 7, 12), f)
    living(ctx, il + 80)
    room_door(ctx, 1.0)
    # callers
    dad_call = (i == 0 and c >= 20) or (i == 1 and up_)
    dd = stand(ctx, DAD, 1395, KD, P(eye='shock' if i == 0 else 'happy', mouth='open' if i == 0 else 'grin', lsh=20, lel=-40,
                                     rsh=115 if dad_call else 50, rel=-15 if dad_call else -50, head=-6), -1)
    keys(ctx, dd['front'][0], dd['front'][1] + 10, 1.2, il)
    sofa_back(ctx)
    sofa_front(ctx)
    if up_:
        pts = [(eye, mouth) for eye, mouth in [('glare', 'flat')]][0]
        if i == 0:
            m = stand(ctx, MOM, 850, KM, P(eye='happy', mouth='smile', lsh=20, rsh=-80, rel=-20, head=-4), -1)
            snack(ctx, m['front'][0] - 20, m['front'][1] - 10, 0.9)
        elif i == 1:
            m = stand(ctx, MOM, 980, KM, P(eye='glare', mouth='flat', lsh=20, rsh=100, rel=-10, head=6), 1)
        elif i == 2:
            m = stand(ctx, MOM, 900, KM, P(eye='glare', mouth='flat', lsh=20, rsh=110, rel=-20, head=6), 1)
        else:
            m = stand(ctx, MOM, 850, KM, P(eye='glare', mouth='flat', lsh=20, rsh=-100, rel=10, head=-6), -1)
        for k in range(4):   # whoosh lines (she just shot up)
            y = m['head'][1] + 80 + k * 70
            ctx.move_to(m['head'][0] - 110, y + 60); ctx.line_to(m['head'][0] - 110, y + 160)
            ctx.move_to(m['head'][0] + 110, y + 60); ctx.line_to(m['head'][0] + 110, y + 160)
        setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(7); ctx.stroke()
    else:
        cl = c >= 20 and CALL[i]
        m = mom_sit(ctx, MX, 'shock' if cl else 'closed', 'open' if cl else 'smile', lsh=60, lel=-110, rsh=80, rel=-100, torso=-8, head=6)
        mug(ctx, m['front'][0] + 4, m['front'][1] - 24, 0.95, il, max(0, 0.7 - 0.2 * i))
        if c < 18:
            for k in range(5):
                a = k * 0.6 + 0.4
                ctx.move_to(MX + 300 * math.cos(a + 2.5), SEAT + 30 + 60 * math.sin(a + 2.5)); ctx.line_to(MX + 360 * math.cos(a + 2.5), SEAT + 30 + 80 * math.sin(a + 2.5))
            ink(ctx, 6); ctx.stroke()
    # the kid (left)
    kp = P(eye='happy', mouth='grin', lsh=30, rsh=120 if (i == 2 and c >= 20) else 30, rel=-20)
    if i == 0 and up_:
        kp = P(eye='happy', mouth='grin', lsh=30, rsh=80, rel=-40)
    if i == 3 and up_:
        kp = P(eye='shock', mouth='open', lsh=30, rsh=30, rkn=-60, rhip=40)
    k = stand(ctx, KID, 640, KK, kp, 1)
    if i >= 1 or (i == 0 and up_):
        snack(ctx, k['back'][0], k['back'][1] - 6, 0.6)
    # the dog (front right) with leash
    bark = i == 1 and c >= 20
    dog(ctx, 1180, GND - 10 - (20 * abs(math.sin(il * 0.6)) if bark else 0), 0.5, -1, il)
    if i >= 1:
        leash(ctx, 1180 - 0.5 * 205, GND - 10 - 0.5 * 175, 1080, GND - 20, 30)
    ctx.restore()
    if up_:
        label(ctx, ANS[i], 540, 1440, 104, WHITE, -0.03, pop(c, 1, 4))
    else:
        if c < 20:
            label(ctx, "*FLOMP!*", 540, 1440, 110, PURPLE, 0.04, pop(c, 12, 15))
        elif CALL[i]:
            col = (CYAN, GOLD, YEL)[i]
            label2(ctx, CALL[i][0], CALL[i][1], col, pop(c, 20, 23), 96, y=620)


# ------------------------------------------------------------------ shot 4a: mug macro, 4b: close-up
def s4a(ctx, f, il):
    # il 0..50: macro of the mug in Mom's hand: *sip* ... frost creeps over "...it's COLD." *cricket*
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('fff0c9')), (1, hx('ffd9a8'))])); ctx.paint()
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eio(il / 50), 0, 0, f)
    rnd = random.Random(5)
    for k in range(30):
        sparkle(ctx, rnd.uniform(0, 1080), rnd.uniform(300, 1700), 14, hx('ffe2a8'))
    fr = eio(pop(il, 14, 30))
    rays(ctx, 540, 1000, 300, 1200, il * 0.02, ICE, 0.35 * fr, 14)
    # Mom's hand holding the mug
    ctx.save(); ctx.translate(540, 1072); ctx.scale(6.2, 6.2)
    ellipse(ctx, 34, 20, 24, 20); fl(ctx, MOM['skin'], 3)
    ctx.restore()
    mug(ctx, 540, 1000, 6.2, il, 0.0, frost=fr)
    ctx.save(); ctx.translate(540, 1072); ctx.scale(6.2, 6.2)
    for k in range(3):
        ellipse(ctx, 22 + k * 3, 8 + k * 9, 10, 6); fl(ctx, MOM['skin'], 2)
    ctx.restore()
    ctx.restore()
    label(ctx, "*sip*", 540, 560, 110, CYAN, -0.04, pop(il, 2, 5))
    if il >= 20:
        label(ctx, "\"...it's COLD.\"", 540, 1440, 120, ICE, 0.03, pop(il, 20, 24))
    if il >= 34:
        label(ctx, "*cricket*", 820, 700, 60, WHITE, 0.1, pop(il, 34, 37))


def s4b(ctx, f, il):
    # il 0..70: Mom ECU, hair frazzled, twitch "I just want..." 34 "...ONE MINUTE!!"
    z = 1.0 + 0.06 * eio(il / 70)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('ffd0e4')), (1, hx('fff0c9'))])); ctx.paint()
    ctx.save(); cam(ctx, 540, 960, z, 0, shake_at(il, [34], 8, 12), f)
    rays(ctx, 540, 900, 200, 1200, il * 0.03, (1, 1, 1), 0.35, 16)
    face(ctx, MOM, P(eye='glare', mouth='grin' if il < 34 else 'scream'), 540, 900, 205)
    for (x, y, a) in ((360, 650, -0.7), (470, 600, -0.2), (620, 600, 0.3), (720, 660, 0.8)):   # frazzled hair strands
        ctx.move_to(x, y); ctx.curve_to(x + 30 * math.sin(a), y - 40, x + 60 * math.sin(a), y - 30, x + 70 * math.sin(a) + 10, y - 80)
    ink(ctx, 7); ctx.stroke()
    twitch(ctx, 780, 690, il, 1.6)
    sweat(ctx, 300, 720, il, 1.5)
    ctx.restore()
    label(ctx, "\"I just want...", 540, 1380, 110, WHITE, -0.03, pop(il, 3, 7))
    if il >= 34:
        label(ctx, "...ONE MINUTE!!\"", 540, 1500, 120, RED, 0.03, pop(il, 34, 38))


def s4(ctx, f):
    il = f - 280
    if il < 50:
        s4a(ctx, f, il)
    else:
        s4b(ctx, f, il - 50)


# ------------------------------------------------------------------ shot 5: everybody out -> peace -> phone -> split
def out_scene(ctx, f, il):
    # il 0..100
    ctx.save(); cam(ctx, 1010, 1300, 1.06, 0, shake_at(il, [40], 6, 10), f)
    living(ctx, il + 300)
    door = 1 - eio(pop(il, 34, 40))
    u = eio(pop(il, 4, 34))
    room_door(ctx, door)
    sofa_back(ctx)
    sofa_front(ctx)
    if il < 40:
        m = mom_sit(ctx, MX, 'happy', 'smile', lsh=60, lel=-110, rsh=80, rel=-100, torso=-6, head=4)
        mug(ctx, m['front'][0] + 4, m['front'][1] - 24, 0.95, il, 0.0)
        if il < 34:   # Dad herds kid + dog out the door
            stand(ctx, KID, lerp(1130, 1420, u), KK, P(eye='happy', mouth='grin', lsh=30, rsh=30, lhip=20 * math.sin(il), rhip=-20 * math.sin(il)), 1)
            dog(ctx, lerp(1230, 1520, u), GND - 10, 0.5, 1, il)
            stand(ctx, DAD, lerp(1260, 1480, u), KD, P(eye='happy', mouth='grin', lsh=-60, lel=-30, rsh=150, rel=-20, head=-4), -1)
    elif il < 74:
        m = mom_sit(ctx, MX, 'closed', 'smile', lsh=60, lel=-110, rsh=80, rel=-100, torso=-12, head=10, sink=14 * eio(pop(il, 44, 56)))
        mug(ctx, m['front'][0] + 4, m['front'][1] - 24, 0.95, il, 0.0)
        for j in range(3):
            sparkle(ctx, m['head'][0] - 150 + j * 150, m['head'][1] - m['R'] * 1.3 - 10 * math.sin(il * 0.2 + j), 18 * eout(pop(il, 46, 54)), YEL)
    else:
        look = 14 * math.sin((il - 74) * 0.35)
        ph = il >= 90
        m = mom_sit(ctx, MX, 'normal', 'flat', lsh=60, lel=-110, rsh=150 if ph else 80, rel=-140 if ph else -100, head=look, sink=14)
        if ph:
            phone(ctx, m['front'][0], m['front'][1] - 30, 0.2, 0.9)
        else:
            mug(ctx, m['front'][0] + 4, m['front'][1] - 24, 0.95, il, 0.0)
    ctx.restore()
    if il < 40:
        label2(ctx, "\"Okay! Everybody", "OUT!\"", WHITE, pop(il, 2, 6), 110, col2=CYAN, y=1440)
    elif il < 46:
        label(ctx, "*CLICK*", 540, 600, 110, GOLD, -0.04, pop(il, 40, 43))
    elif il < 74:
        label2(ctx, "\"...ahhh.", "PEACE.\"", WHITE, pop(il, 48, 52), 120, col2=MINT, y=1440)
        label(ctx, "*silence*", 540, 600, 80, WHITE, 0.04, pop(il, 46, 50))
    else:
        label(ctx, "*cricket*", 540, 600, 70, WHITE, 0.08, pop(il, 74, 77))
        label(ctx, "\"...too QUIET.\"", 540, 1440, 120, WHITE, -0.03, pop(il, 78, 82))


def mom_phone(ctx, lf, bounce=True):
    jig = 6 * math.sin(lf * 0.9) if bounce else 0
    m = mom_sit(ctx, MX, 'happy', 'grin', lsh=-30, lel=-40, rsh=150, rel=-150, head=jig * 0.5, sink=14 - abs(jig) * 2)
    phone(ctx, m['head'][0] + m['R'] * 0.95, m['head'][1] + m['R'] * 0.15, 0.25, 1.0)
    ellipse(ctx, m['head'][0] + m['R'] * 0.95, m['head'][1] + m['R'] * 0.45, 22, 20); fl(ctx, MOM['skin'], 4)
    return m


def gran_scene(ctx, lf):
    living(ctx, lf, gran_room=True)
    armchair(ctx, 1000)
    rg = lf >= 12
    gl = lf >= 34
    g = mom_sit(ctx, 1000, 'glare' if gl else 'closed', 'flat' if gl else 'smile', lsh=50, lel=-110, rsh=80, rel=-100,
                torso=-6, head=4, sink=10 * eio(pop(lf, 0, 10)), ch=GRAN)
    mug(ctx, g['front'][0] + 4, g['front'][1] - 24, 0.95, lf, 1.0, col=hx('ffb3cf'))
    # side table with ringing phone
    rect_r(ctx, 680, 1330, 140, 26, 8); fl(ctx, hx('c98a52'), 4)
    rect_r(ctx, 736, 1350, 28, 210, 6); fl(ctx, hx('a8683e'), 4)
    phone(ctx, 750, 1290, 1.4, 0.8, ring=1.0 if rg else 0.0, lf=lf)
    if gl:
        twitch(ctx, g['head'][0] + g['R'] * 0.8, g['head'][1] - g['R'] * 0.9, lf, 1.0)
    return g


def split(ctx, f, il):
    # il 0..90: top = Mom calling, bottom = Grandma just sat down
    ctx.save(); ctx.rectangle(0, 0, W, 958); ctx.clip()
    ctx.save(); cam(ctx, 980, 1240, 1.15, 0, 0, f, sx=540, sy=640)
    living(ctx, il + 400); room_door(ctx, 0.0); sofa_back(ctx); sofa_front(ctx)
    mom_phone(ctx, il)
    ctx.restore(); ctx.restore()
    ctx.save(); ctx.rectangle(0, 962, W, H - 962); ctx.clip()
    ctx.save(); cam(ctx, 980, 1300, 1.0, 0, shake_at(il, [12], 6, 8), f, sx=540, sy=1270)
    gran_scene(ctx, il)
    ctx.restore(); ctx.restore()
    ctx.rectangle(0, 952, W, 16); setc(ctx, WHITE); ctx.fill()
    ctx.move_to(0, 952); ctx.line_to(W, 952); ctx.move_to(0, 968); ctx.line_to(W, 968); ink(ctx, 5); ctx.stroke()
    label(ctx, "\"MOM! MOM! MOM!\"", 540, 330, 96, YEL, -0.03, pop(il, 2, 5))
    if 12 <= il < 34:
        label(ctx, "*RING RING!*", 540, 1100, 80, GOLD, 0.04, pop(il, 12, 15))
    if il >= 34:
        label2(ctx, "\"...I JUST", "SAT DOWN.\"", WHITE, pop(il, 34, 38), 100, col2=PURPLE, y=1480)


def call_scene(ctx, f, il):
    # il 0..40: Mom on the phone, card PLOT TWIST
    ctx.save(); cam(ctx, 960, 1260, 1.2 + 0.08 * eio(il / 40), 0, shake_at(il, [0], 6, 10), f)
    living(ctx, il + 400); room_door(ctx, 0.0); sofa_back(ctx); sofa_front(ctx)
    mom_phone(ctx, il)
    ctx.restore()
    card(ctx, 'p2', il, 0)
    label(ctx, "*boop boop beep*", 540, 1440, 90, CYAN, -0.03, pop(il, 2, 6))


def s5(ctx, f):
    lf = f - 400
    if lf < 100:
        out_scene(ctx, f, lf)
    elif lf < 140:
        call_scene(ctx, f, lf - 100)
    elif lf < 230:
        split(ctx, f, lf - 140)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (140, s3), (280, s4), (400, s5)]
CUTS = (60, 140, 280, 330, 400, 500, 540, 630)


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
                              "-i", "out/mom_one_minute_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
