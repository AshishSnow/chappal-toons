"""'DAD vs THE PRINTER'. Original, general-audience comedy short, 22s.
Hook:   cosy home-office medium shot: Dad hugging + shaking the home printer, its red light blinking *BEEP! BEEP!*,
        crumpled paper flying, the kid holding his homework folder -> "PRINT... ALREADY!!" + caption 'DAD vs THE PRINTER:'.
        (rewatch easter egg: a grey cat tail swishes out of the printer's paper drawer the whole time; the cat bed is empty)
Beat 1: kid "Dad! I need my HOMEWORK printed!" -> Dad "Printing? EASY." *click* -> *whirrr...* -> *CRUNCH!* ->
        display macro "PAPER JAM" blinking -> "...PAPER JAM?!"
Beat 2: Dutch-tilt fix montage: FIX #1 PULL IT. *RIIIP!* "...HALF." / FIX #2 OFF... AND ON. *boop* -> "LOW INK" "...LOW INK?!"
        / FIX #3 THE SMACK. *BONK!* -> *BRRRRT!* sheets machine-gun out *FWIP FWIP FWIP* and bury Dad "...TOO MUCH!!"
Close-up (the one face shot): Dad in the paper pile "I'm SMARTER..." "...than a PRINTER!!"
Twist:  the printer *purrrr~* "...it PURRS?!" -> kid "Dad... it's the CAT." -> drawer *SHHK!* -> PLOT TWIST: THE CAT WAS THE JAM.
        -> cat hops out *hop* -> *DING!* perfect homework -> "YAY!" / "...NAILED IT." -> Mom in the doorway "Honey! Can you
        print my BOARDING PASS?" -> the cat hops back in *mrrp* -> *BEEP!* red light -> Dad twitch "...of COURSE." -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face, rays
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes111 import cat, tube, FUR
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
PAPER = hx('fffdf4'); PR = hx('dfe7f5'); PRD = hx('aab8d6')
MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'), pants=hx('3d5a9e'), shoes=hx('ffffff'))
DAD = dict(doodle.DAD, shirt=hx('ff8a1f'), pants=hx('3d5a9e'), sleeve=0.45)
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('3fd6a0'), pants=hx('8a3cff'), shoes=hx('ff4d5e'))
N = 660
FLOOR, GND = 1560, 1595
KD, KK, KM = 1.05, 0.85, 1.05
PX, PYB = 880, 1305            # printer centre x / bottom (sits on the desk top)
DX0, DX1, DTOP = 1290, 1480, 960   # doorway
DADX = 1150

CAPS = {'p1': [[("DAD vs ", OUT), ("THE PRINTER:", BLUE)]],
        'p2': [[("PLOT TWIST:", RED)], [("THE CAT ", OUT), ("WAS THE JAM.", PURPLE)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def sheet(ctx, x, y, a=0.0, s=1.0, crumple=False, txt=True, hw=False):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if crumple:
        pts = [(46 * math.cos(k * 0.7) * (0.75 + 0.25 * ((k * 7) % 3) / 2), 40 * math.sin(k * 0.7) * (0.75 + 0.25 * ((k * 5) % 3) / 2)) for k in range(9)]
        poly(ctx, pts); fl(ctx, PAPER, 4)
        ctx.move_to(-20, -10); ctx.line_to(6, 4); ctx.line_to(-6, 22); ctx.move_to(10, -20); ctx.line_to(18, 8)
        setc(ctx, hx('c9c2ae')); ctx.set_line_width(3); ctx.stroke()
    else:
        rect_r(ctx, -60, -80, 120, 160, 6); fl(ctx, PAPER, 4)
        if txt:
            for k in range(6):
                ctx.move_to(-42, -54 + k * 22); ctx.line_to(42 - (k % 3) * 14, -54 + k * 22)
            setc(ctx, hx('b9c4dc')); ctx.set_line_width(5); ctx.stroke()
        if hw:   # the finished homework: gold star
            sparkle(ctx, 30, 52, 20, GOLD)
    ctx.restore()


def folder(ctx, x, y, a=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -70, -54, 140, 108, 10); fl(ctx, hx('ffd23f'), 5)
    rect_r(ctx, -40, -18, 80, 36, 8); fl(ctx, WHITE, 3)
    ctx.move_to(-26, 0); ctx.line_to(26, 0); setc(ctx, hx('8a8a9a')); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def printer(ctx, lf, state='ready', drawer=0.0, tail=True, out=0.0, shake=0.0, cat_in=False, cat_eye='closed'):
    """home printer on the desk. state: ready | jam | ink | off | work. drawer 0..1 = paper drawer pulled out.
    out 0..1 = sheet coming out of the slot"""
    jx = shake * math.sin(lf * 2.3); jy = shake * 0.5 * math.cos(lf * 3.1)
    ctx.save(); ctx.translate(PX + jx, PYB + jy)
    w, h = 340, 210
    # paper in the input tray (behind)
    rect_r(ctx, -110, -h - 70, 220, 100, 6); fl(ctx, PAPER, 4)
    rect_r(ctx, -130, -h - 30, 260, 40, 8); fl(ctx, PRD, 4)
    # body
    rect_r(ctx, -w / 2, -h, w, h, 24); fl(ctx, PR, 5)
    rect_r(ctx, -w / 2 - 6, -h - 8, w + 12, 44, 16); fl(ctx, hx('eef3fb'), 5)   # scanner lid
    # output slot
    rect_r(ctx, -120, -h + 64, 240, 20, 8); setc(ctx, hx('39405a')); ctx.fill()
    if out > 0:
        ctx.save(); ctx.rectangle(-200, -h - 200, 400, h + 68 + 200 - 4); ctx.clip()
        sheet(ctx, 0, -h + 74 - 150 * out + 80, 0, 0.95, txt=state == 'work', hw=state == 'work')
        ctx.restore()
        rect_r(ctx, -120, -h + 64, 240, 12, 6); setc(ctx, hx('39405a')); ctx.fill()
    # control panel (right): display + light + button
    rect_r(ctx, 52, -h + 104, 104, 46, 8); fl(ctx, hx('39405a'), 4)
    dc = {'ready': hx('9dffb0'), 'work': hx('9dffb0'), 'jam': RED, 'ink': ORANGE, 'off': hx('22263a')}[state]
    blinkon = state in ('jam', 'ink') and (lf // 5) % 2 == 0
    rect_r(ctx, 60, -h + 112, 88, 30, 5); setc(ctx, dc if (blinkon or state in ('ready', 'work')) else dark(dc, 0.55) if state != 'off' else dc); ctx.fill()
    if state in ('jam', 'ink'):
        ctx.move_to(104, -h + 118); ctx.line_to(104, -h + 130); ctx.move_to(104, -h + 135); ctx.line_to(104, -h + 136)
        setc(ctx, WHITE); ctx.set_line_width(5); ctx.stroke()
    ellipse(ctx, -130, -h + 128, 14, 14); fl(ctx, dc if state != 'off' else hx('8a8a9a'), 3)   # status light
    if blinkon:
        for k in range(6):
            a = k * 1.05
            ctx.move_to(-130 + 22 * math.cos(a), -h + 128 + 22 * math.sin(a)); ctx.line_to(-130 + 34 * math.cos(a), -h + 128 + 34 * math.sin(a))
        setc(ctx, dc); ctx.set_line_width(5); ctx.stroke()
    ellipse(ctx, -94, -h + 128, 12, 12); fl(ctx, hx('ffffff'), 3)   # power button
    # paper drawer
    dy = 26 * drawer
    if drawer > 0:   # top of the pulled-out drawer (seen from slightly above): paper stack + cat
        poly(ctx, [(-w / 2 + 14, -64 + dy), (w / 2 - 14, -64 + dy), (w / 2 - 34, -64 + dy - 70 * drawer), (-w / 2 + 34, -64 + dy - 70 * drawer)])
        fl(ctx, hx('c4cfe6'), 4)
        poly(ctx, [(-w / 2 + 40, -68 + dy), (w / 2 - 40, -68 + dy), (w / 2 - 54, -68 + dy - 54 * drawer), (-w / 2 + 54, -68 + dy - 54 * drawer)])
        fl(ctx, PAPER, 3)
        if cat_in:
            cat(ctx, -10, -60 + dy - 10 * drawer, 0.5, 1, lf, 'sleep' if cat_eye == 'closed' else 'sit', eye=cat_eye)
    rect_r(ctx, -w / 2 + 14, -64 + dy, w - 28, 54, 12); fl(ctx, hx('cbd5ea'), 4)
    rect_r(ctx, -40, -46 + dy, 80, 16, 8); fl(ctx, PRD, 3)
    if tail and drawer == 0:   # grey tail poking out of the drawer gap (the secret!)
        sw = 14 * math.sin(lf * 0.25)
        tube(ctx, [(-110, -36), (-166, -30), (-186 - sw * 0.5, -6), (-196 - sw, 22)], 13, FUR, 4)
    ctx.restore()


def crumples(ctx, lf, n=6, seed=1, x=PX, y=PYB - 240, spread=1.0):
    rnd = random.Random(seed)
    for k in range(n):
        ph = (lf * 0.035 + rnd.random()) % 1
        a = rnd.uniform(-2.6, -0.5)
        r = 120 + 420 * ph * spread
        cx = x + r * math.cos(a); cy = y + r * math.sin(a) + 900 * ph * ph
        sheet(ctx, cx, cy, ph * 6 + k, 0.7, crumple=True)


# ------------------------------------------------------------------ set: cosy home office
def office(ctx, lf, door=1.0):
    wall = hx('dff4ec')
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, wall); ctx.fill()
    rnd = random.Random(113)
    for k in range(80):   # tiny stars wallpaper
        sparkle(ctx, rnd.uniform(-300, 2400), rnd.uniform(300, 1520), 10, dark(wall, 0.92))
    # floor
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('d9a878')); ctx.fill()
    for k in range(-30, 60):
        ctx.move_to(k * 110, FLOOR); ctx.line_to(k * 110 - 300, FLOOR + 900)
    setc(ctx, hx('c49364')); ctx.set_line_width(4); ctx.stroke()
    rect_r(ctx, -3000, FLOOR - 22, 9000, 24, 4); fl(ctx, WHITE, 4)
    # window (left) with blinds + clouds
    rect_r(ctx, 190, 820, 280, 340, 12); fl(ctx, WHITE, 6)
    ctx.set_source(vgrad(ctx, 0, 838, 0, 1142, [(0, hx('8fd8ff')), (1, hx('d8f4ff'))])); rect_r(ctx, 208, 838, 244, 304, 8); ctx.fill()
    ellipse(ctx, 290, 920, 40, 18); setc(ctx, WHITE); ctx.fill(); ellipse(ctx, 330, 910, 30, 16); ctx.fill()
    for k in range(5):
        ctx.move_to(208, 850 + k * 18); ctx.line_to(452, 850 + k * 18)
    setc(ctx, hx('ffffff')); ctx.set_line_width(10); ctx.stroke()
    ctx.move_to(330, 838); ctx.line_to(330, 1142); ink(ctx, 5); ctx.stroke()
    # cork board with kid drawings + wall clock
    rect_r(ctx, 600, 820, 300, 200, 12); fl(ctx, hx('d9a05a'), 5)
    for (x, y, a, c) in ((650, 870, -0.1, hx('ffe3ef')), (750, 860, 0.08, hx('fff6c9')), (840, 900, -0.05, hx('e2f0ff'))):
        ctx.save(); ctx.translate(x, y); ctx.rotate(a)
        rect_r(ctx, -40, -40, 80, 90, 4); fl(ctx, c, 3)
        ellipse(ctx, 0, -40, 7, 7); setc(ctx, RED); ctx.fill()
        ctx.restore()
    sparkle(ctx, 650, 880, 22, GOLD)
    ctx.save(); ctx.translate(750, 875); doodle_house(ctx); ctx.restore()
    ellipse(ctx, 840, 905, 22, 22); fl(ctx, hx('ffb347'), 3)   # a sun drawing
    ellipse(ctx, 1050, 850, 48, 48); fl(ctx, WHITE, 5)
    ctx.move_to(1050, 850); ctx.line_to(1050 + 28 * math.sin(lf * 0.2), 850 - 28 * math.cos(lf * 0.2)); ctx.move_to(1050, 850); ctx.line_to(1068, 860); ink(ctx, 5); ctx.stroke()
    # shelf with books + plant
    rect_r(ctx, 560, 1060, 360, 20, 6); fl(ctx, hx('b87a48'), 4)
    for k in range(5):
        rect_r(ctx, 580 + k * 34, 960 + 12 * (k % 2), 28, 100 - 12 * (k % 2), 4); fl(ctx, (RED, BLUE, GOLD, MINT, PURPLE)[k], 3)
    rect_r(ctx, 820, 1010, 60, 50, 10); fl(ctx, hx('ff8a5c'), 4)
    for a in (-0.8, -0.3, 0.2, 0.7):
        ellipse(ctx, 850 + 40 * math.sin(a), 990 - 30 * math.cos(a), 12, 28, a); fl(ctx, GREEN, 3)
    # doorway (right) with hallway beyond
    rect_r(ctx, DX0 - 22, DTOP - 22, DX1 - DX0 + 44, FLOOR - DTOP + 22, 10); fl(ctx, WHITE, 5)
    ctx.rectangle(DX0, DTOP, DX1 - DX0, FLOOR - DTOP); setc(ctx, hx('ffd9b8')); ctx.fill()
    ww = (DX1 - DX0) * (1 - 0.86 * door)
    ctx.rectangle(DX0, DTOP, ww, FLOOR - DTOP); fl(ctx, hx('8ad0ff'), 5)
    # tall plant (far left)
    rect_r(ctx, 90, 1440, 110, 120, 16); fl(ctx, hx('ff8fb8'), 5)
    for a in (-0.9, -0.4, 0.1, 0.6, 1.0):
        ellipse(ctx, 145 + 80 * math.sin(a), 1390 - 60 * math.cos(a), 22, 54, a); fl(ctx, GREEN, 3)
    # rug + EMPTY cat bed (easter egg)
    ellipse(ctx, 900, FLOOR + 110, 480, 66); fl(ctx, hx('ffb3cf'), 5)
    ellipse(ctx, 900, FLOOR + 110, 380, 44); setc(ctx, hx('ffd9e6')); ctx.fill()
    ellipse(ctx, 1250, FLOOR + 30, 100, 28); fl(ctx, hx('b98cff'), 5)
    ellipse(ctx, 1250, FLOOR + 22, 72, 14); setc(ctx, hx('e2d0ff')); ctx.fill()
    # waste basket full of crumpled paper
    poly(ctx, [(460, 1450), (560, 1450), (545, 1565), (475, 1565)]); fl(ctx, hx('7a8cc9'), 5)
    for k in range(3):
        sheet(ctx, 480 + k * 30, 1440 - 10 * (k % 2), k, 0.5, crumple=True)


def doodle_house(ctx):
    poly(ctx, [(-24, 0), (24, 0), (24, 30), (-24, 30)]); fl(ctx, hx('ff8a5c'), 3)
    poly(ctx, [(-30, 0), (0, -26), (30, 0)]); fl(ctx, RED, 3)


def desk(ctx):
    rect_r(ctx, 560, PYB, 600, 34, 10); fl(ctx, hx('c98a52'), 5)
    for x in (590, 1110):
        rect_r(ctx, x, PYB + 30, 26, FLOOR - PYB - 20, 6); fl(ctx, hx('a8683e'), 4)
    rect_r(ctx, 600, PYB + 34, 160, 100, 8); fl(ctx, hx('b87a48'), 4)   # drawer unit
    ellipse(ctx, 680, PYB + 84, 10, 6); fl(ctx, GOLD, 3)
    # pencil cup + lamp
    rect_r(ctx, 1080, PYB - 80, 54, 80, 10); fl(ctx, hx('ff8a5c'), 4)
    for k, c in enumerate((RED, BLUE, GOLD)):
        ctx.move_to(1092 + k * 14, PYB - 80); ctx.line_to(1088 + k * 18, PYB - 130); setc(ctx, INK); ctx.set_line_width(12); ctx.stroke_preserve(); setc(ctx, c); ctx.set_line_width(6); ctx.stroke()


def lamp(ctx):
    rect_r(ctx, 620, PYB - 20, 90, 20, 8); fl(ctx, hx('ff5fa8'), 4)
    ctx.move_to(665, PYB - 20); ctx.line_to(640, PYB - 160); ctx.line_to(700, PYB - 230); ink(ctx, 8); ctx.stroke()
    poly(ctx, [(670, PYB - 250), (740, PYB - 220), (730, PYB - 170), (680, PYB - 200)]); fl(ctx, hx('ff5fa8'), 4)


# ------------------------------------------------------------------ people
def stand(ctx, ch, x, k, p, f_=1, g=GND):
    return draw(ctx, x, g - 186 * k, k, f_, ch, p)


def kid_folder(ctx, x, eye='shock', mouth='open', lf=0, hold=True, f_=1, extra=None):
    p = P(eye=eye, mouth=mouth, lsh=-60, lel=-70, rsh=70, rel=-90, head=4)
    if extra:
        p.update(extra)
    k = stand(ctx, KID, x, KK, p, f_)
    if hold:
        folder(ctx, k['front'][0] + 10 * f_, k['front'][1] - 20, -0.1, 0.8)
    return k


def dad_hug(ctx, lf, eye='shock', mouth='scream', jig=True):
    j = 7 * math.sin(lf * 1.4) if jig else 0
    d = stand(ctx, DAD, 1105 + j * 0.6, KD, P(eye=eye, mouth=mouth, lsh=80, lel=-10, rsh=105, rel=-30, torso=-10 + j * 0.4, head=j * 0.5), -1)
    return d


# ------------------------------------------------------------------ shot 1: hook
def hook_scene(ctx, lf):
    office(ctx, lf)
    lamp(ctx); desk(ctx)
    printer(ctx, lf, 'jam', shake=8)
    sheet(ctx, PX - 10, PYB - 130, 0.2 * math.sin(lf * 0.7), 0.85, crumple=True)   # crumpled sheet jammed in the slot
    d = dad_hug(ctx, lf)
    sweat(ctx, d['head'][0] - d['R'] * 1.0, d['head'][1] - d['R'] * 0.4, lf, 0.9)
    crumples(ctx, lf, 6, 3)
    k = kid_folder(ctx, 560, 'shock', 'open', lf)
    return d


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    z = 1.1 + 0.03 * eio(pop(lf, 0, 54))
    ctx.save(); cam(ctx, 870, 1320, z + 0.1, 0, 3 + shake_at(lf, [0], 6, 8), f)
    hook_scene(ctx, lf)
    ctx.restore()
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"PRINT...", "ALREADY!!\"", WHITE, t, 124, col2=ORANGE, y=1440)
    if lf < 60:
        label(ctx, "*BEEP! BEEP!*", 380, 640, 60, RED, -0.1, 1 if lf == f else pop(lf, 2, 5))
        label(ctx, "*SHAKE!*", 830, 660, 62, YEL, 0.1, 1 if lf == f else pop(lf, 5, 8))


# ------------------------------------------------------------------ shot 2: easy -> whirr -> jam (+ display macro)
def s2(ctx, f):
    il = f - 60   # 0..90
    if il >= 66:
        return jam_macro(ctx, f, il - 66)
    z = 1.24 + 0.08 * eio(il / 66)
    ctx.save(); cam(ctx, 880, 1310, z, 0, shake_at(il, [50], 10, 14), f)
    office(ctx, il)
    lamp(ctx); desk(ctx)
    st = 'ready' if il < 34 else 'work' if il < 50 else 'jam'
    out = 0.0 if il < 34 else 0.5 * eio(pop(il, 34, 50)) if il < 50 else 0.5
    printer(ctx, il, st, out=out, shake=3 if 34 <= il < 50 else 0)
    if il >= 50:
        sheet(ctx, PX - 10, PYB - 130, 0.2, 0.85, crumple=True)
    if il < 26:
        d = stand(ctx, DAD, DADX, KD, P(eye='happy', mouth='grin', lsh=-30, lel=-120, rsh=-30, rel=-120, head=-6), -1)   # hands on hips
    elif il < 50:
        press = il < 34
        d = stand(ctx, DAD, DADX, KD, P(eye='happy', mouth='grin', lsh=-30, lel=-120, rsh=95 if press else 30, rel=-10 if press else -60, head=-4), -1)
    else:
        d = stand(ctx, DAD, DADX + 10, KD, P(eye='shock', mouth='open', lsh=150, lel=-20, rsh=160, rel=-20, head=6, torso=6), -1)
    kid_folder(ctx, 560, 'happy' if il < 50 else 'shock', 'grin' if il < 50 else 'open', il,
               extra=dict(rsh=150, rel=-30) if il < 20 else None)
    ctx.restore()
    if il < 24:
        label2(ctx, "\"Dad! I need my", "HOMEWORK printed!\"", YEL, pop(il, 1, 5), 96, y=1440)
    elif il < 34:
        label2(ctx, "\"Printing?", "EASY.\"", WHITE, pop(il, 24, 28), 120, col2=MINT, y=1440)
        if il >= 30:
            label(ctx, "*click*", 540, 620, 90, CYAN, -0.05, pop(il, 30, 33))
    elif il < 50:
        label2(ctx, "\"Printing?", "EASY.\"", WHITE, 1, 120, col2=MINT, y=1440)
        label(ctx, "*whirrr...*", 540, 620, 96, CYAN, 0.04, pop(il, 34, 38))
    else:
        label(ctx, "*CRUNCH!*", 540, 620, 120, RED, -0.06, pop(il, 50, 53))


def jam_macro(ctx, f, il):
    # il 0..24: macro on the display blinking PAPER JAM
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('dfe7f5')), (1, hx('aab8d6'))])); ctx.paint()
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eio(il / 24), 0, shake_at(il, [0], 6, 10), f)
    rays(ctx, 540, 1000, 300, 1200, il * 0.03, RED, 0.25, 14)
    rect_r(ctx, 120, 760, 840, 480, 60); fl(ctx, hx('39405a'), 8)
    on = (il // 4) % 2 == 0
    rect_r(ctx, 170, 810, 740, 380, 36); setc(ctx, RED if on else dark(RED, 0.6)); ctx.fill()
    text(ctx, "PAPER", 540, 960, 150, WHITE, ow=0, maxw=640)
    text(ctx, "JAM", 540, 1130, 170, WHITE, ow=0, maxw=640)
    ctx.restore()
    label(ctx, "*BEEP! BEEP!*", 540, 600, 90, RED, -0.04, pop(il, 0, 3))
    label(ctx, "\"...PAPER JAM?!\"", 540, 1440, 120, WHITE, 0.03, pop(il, 6, 10))


# ------------------------------------------------------------------ shot 3: the fix montage (Dutch tilt)
FIX = [("FIX #1:", "PULL IT."), ("FIX #2:", "OFF... AND ON."), ("FIX #3:", "THE SMACK.")]


def s3(ctx, f):
    il = f - 150   # 0..150
    i, c = min(2, il // 50), il - 50 * min(2, il // 50)
    rot = (7, -7, 7)[i]
    ctx.save(); cam(ctx, 900, 1300, 1.22, rot, shake_at(c, [24] if i == 0 else [26] if i == 2 else [], 8, 16), f)
    office(ctx, il + 90)
    lamp(ctx); desk(ctx)
    if i == 0:   # pull the jammed sheet -> RIIIP
        rip = c >= 24
        pull = eio(pop(c, 4, 24))
        printer(ctx, c, 'jam', shake=6 * (1 - rip) * pull)
        d = stand(ctx, DAD, DADX + 40 * pull + (30 if rip else 0), KD, P(eye='glare' if not rip else 'shock', mouth='grin' if not rip else 'open',
                                                                   lsh=70, lel=-20, rsh=80, rel=-10, torso=16 * pull + (12 if rip else 0), head=8), -1)
        if not rip:
            sheet(ctx, PX + 60 + 60 * pull, PYB - 110, 1.2 + 0.2 * pull, 0.6)
        else:
            sheet(ctx, PX + 10, PYB - 130, 0.1, 0.7, crumple=True)
            ctx.save(); ctx.translate(d['front'][0] - 40, d['front'][1] - 40); ctx.rotate(-0.4)
            poly(ctx, [(-50, -60), (50, -60), (40, 0), (20, -14), (0, 6), (-20, -10), (-50, 4)]); fl(ctx, PAPER, 4)
            ctx.restore()
        kid_folder(ctx, 560, 'shock' if rip else 'normal', 'open' if rip else 'flat', c)
    elif i == 1:  # off and on -> LOW INK
        st = 'jam' if c < 12 else 'off' if c < 26 else 'ink'
        printer(ctx, c, st)
        press = c < 14 or 22 <= c < 28
        d = stand(ctx, DAD, DADX - 10, KD, P(eye='happy' if c < 30 else 'shock', mouth='grin' if c < 30 else 'open',
                                             lsh=-30, lel=-120, rsh=105 if press else 40, rel=-30 if press else -60, head=-4), -1)
        kid_folder(ctx, 560, 'normal' if c < 30 else 'shock', 'flat' if c < 30 else 'open', c)
    else:         # smack -> machine-gun pages bury Dad
        hit = c >= 26
        up = eio(pop(c, 8, 24))
        printer(ctx, c, 'work' if hit else 'ink', out=((c * 0.35) % 1) * 0.6 if hit else 0, shake=10 if hit else 0)
        d = stand(ctx, DAD, DADX + (40 if hit else 0), KD, P(eye='glare' if not hit else 'shock', mouth='grin' if not hit else 'scream',
                                                             lsh=60 if hit else 30, lel=-20, rsh=(60 + 110 * up) if not hit else 150, rel=-20 if not hit else -30,
                                                             head=-6, torso=8 if hit else -6), -1)
        kid_folder(ctx, 560, 'happy' if hit else 'normal', 'grin' if hit else 'flat', c)
        if hit:
            rnd = random.Random(7)
            n_ = min(26, (c - 26) * 2)
            for k in range(n_):   # pile growing on Dad
                sheet(ctx, DADX + rnd.uniform(-130, 130), GND - 20 - rnd.uniform(0, 1) * (40 + 13 * n_), rnd.uniform(-1.2, 1.2), 0.75)
            for k in range(5):    # pages in flight
                ph = ((c - 26) * 0.12 + k / 5) % 1
                sheet(ctx, PX + 80 + 280 * ph, PYB - 160 - 160 * math.sin(ph * math.pi), ph * 5 + k, 0.7)
    ctx.restore()
    label2(ctx, FIX[i][0], FIX[i][1], GOLD, pop(c, 0, 4), 88, col2=WHITE, y=640)
    if i == 0 and c >= 24:
        label(ctx, "*RIIIIP!*", 540, 1340, 110, RED, -0.05, pop(c, 24, 27))
        label(ctx, "\"...HALF.\"", 540, 1470, 100, WHITE, 0.03, pop(c, 32, 36))
    if i == 1:
        if c < 26:
            label(ctx, "*boop*" if c < 22 else "*boop!*", 540, 1440, 100, CYAN, 0.04, pop(c, 12, 15))
        else:
            label(ctx, "\"...LOW INK?!\"", 540, 1440, 116, ORANGE, -0.03, pop(c, 30, 34))
    if i == 2:
        if c < 26:
            label(ctx, "*BONK!*", 540, 1440, 120, RED, -0.05, pop(c, 24, 26))
        else:
            label(ctx, "*FWIP FWIP FWIP!*", 540, 1340, 90, CYAN, 0.03, pop(c, 26, 29))
            label(ctx, "\"...TOO MUCH!!\"", 540, 1470, 104, WHITE, -0.03, pop(c, 36, 40))


# ------------------------------------------------------------------ shot 4: close-up in the paper pile
def s4(ctx, f):
    il = f - 300   # 0..70
    z = 1.0 + 0.06 * eio(il / 70)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('ffe2c9')), (1, hx('dff4ec'))])); ctx.paint()
    ctx.save(); cam(ctx, 540, 960, z, 0, shake_at(il, [36], 8, 12), f)
    rays(ctx, 540, 900, 200, 1200, il * 0.03, (1, 1, 1), 0.35, 16)
    face(ctx, DAD, P(eye='glare', mouth='grin' if il < 36 else 'scream'), 540, 900, 205)
    rnd = random.Random(4)
    for k in range(22):   # paper pile up to his chin
        sheet(ctx, rnd.uniform(160, 920), rnd.uniform(1180, 1500), rnd.uniform(-1, 1), 1.3)
    sheet(ctx, 620, 640, 0.35, 1.0)   # a sheet stuck on his head
    twitch(ctx, 790, 700, il, 1.6)
    sweat(ctx, 300, 760, il, 1.4)
    ctx.restore()
    label(ctx, "\"I'm SMARTER...", 540, 1380, 110, WHITE, -0.03, pop(il, 3, 7))
    if il >= 36:
        label(ctx, "...than a PRINTER!!\"", 540, 1500, 100, ORANGE, 0.03, pop(il, 36, 40))


# ------------------------------------------------------------------ shot 5: purr -> cat -> twist -> Mom -> loop
def pile(ctx, n=18):
    rnd = random.Random(7)
    for k in range(n):
        sheet(ctx, DADX + rnd.uniform(-160, 160) - 40, GND - 10 - rnd.uniform(0, 60), rnd.uniform(-1.4, 1.4), 0.75)


def s5(ctx, f):
    lf = f - 370
    if lf >= 260:
        return s1(ctx, f, f - 630)
    if 62 <= lf < 100:
        zoom, cx, cy = 1.5, 900, 1250
    else:
        zoom, cx, cy = (1.2, 880, 1310) if lf < 160 else (1.04, 930, 1320)
    ctx.save(); cam(ctx, cx, cy, zoom, 0, shake_at(lf, [62, 222], 8, 12), f)
    office(ctx, lf + 300, door=1.0)
    lamp(ctx); desk(ctx)
    if lf < 60:           # purr -> kid: it's the cat
        printer(ctx, lf, 'ink', shake=2 if (lf // 6) % 2 else 0)
        pile(ctx)
        d = stand(ctx, DAD, DADX, KD, P(eye='normal', mouth='flat', lsh=-20, rsh=60, rel=-120, head=-10), -1)
        kid_folder(ctx, 560, 'happy' if lf >= 30 else 'normal', 'grin' if lf >= 30 else 'flat', lf,
                   extra=dict(rsh=80, rel=-10) if lf >= 30 else None, hold=lf < 30)
    elif lf < 100:        # pull the drawer: cat on the paper
        dr = eio(pop(lf, 62, 70))
        wake = lf >= 76
        printer(ctx, lf, 'ink', drawer=dr, cat_in=True, cat_eye='normal' if wake else 'closed')
        pile(ctx)
        d = stand(ctx, DAD, DADX, KD, P(eye='shock', mouth='open', lsh=-20, rsh=90, rel=-10, head=-6), -1)
        kid_folder(ctx, 560, 'happy', 'grin', lf)
        if wake:
            for k in range(2):
                sparkle(ctx, PX - 60 + 120 * k, PYB - 160 - 8 * math.sin(lf * 0.4 + k), 14, PINK)
    elif lf < 160:        # cat hops out -> DING -> perfect homework
        hop = eio(pop(lf, 100, 112))
        printer(ctx, lf, 'ready' if lf < 116 else 'work', drawer=1 - eio(pop(lf, 112, 118)), tail=False,
                out=0 if lf < 116 else min(1.0, eio(pop(lf, 116, 132))) if lf < 132 else 0)
        pile(ctx)
        cx_ = lerp(PX - 10, 800, hop); cy_ = lerp(PYB - 50, GND - 4, hop) - 180 * math.sin(math.pi * hop)
        if lf < 112:
            cat(ctx, cx_, cy_, 0.5, -1, lf, 'sit', eye='happy' if hop > 0 else 'normal')
        else:
            cat(ctx, 800, GND - 4, 0.5, -1, lf, 'sit', eye='smug')
        got = lf >= 132
        d = stand(ctx, DAD, DADX, KD, P(eye='happy' if got else 'shock', mouth='grin' if got else 'open', lsh=-30, lel=-120,
                                        rsh=110 if got else 40, rel=-70 if got else -60, head=-4), -1)
        if got:   # thumbs up
            ellipse(ctx, d['front'][0], d['front'][1] - 24, 12, 22); fl(ctx, DAD['skin'], 3)
        k = kid_folder(ctx, 560, 'happy', 'grin', lf, hold=False, extra=dict(lsh=150, lel=-20, rsh=150, rel=-20))
        if got:
            sheet(ctx, (k['front'][0] + k['back'][0]) / 2 + 10, min(k['front'][1], k['back'][1]) - 60, 0.05, 0.9, hw=True)
            for j in range(3):
                sparkle(ctx, 500 + j * 90, k['head'][1] - 150 - 10 * math.sin(lf * 0.3 + j), 16, YEL)
    else:                 # Mom in doorway -> cat hops back in -> BEEP -> twitch
        back = eio(pop(lf, 200, 212))
        dr = 1.0 if 196 <= lf < 216 else eio(pop(lf, 192, 196)) if lf < 196 else 1 - eio(pop(lf, 216, 222))
        mom = stand(ctx, MOM, 1340, KM, P(eye='happy', mouth='grin', lsh=-20, rsh=80, rel=-40, head=-6), -1)
        sheet(ctx, mom['front'][0] - 20, mom['front'][1] - 20, -0.2, 0.5, txt=True)
        printer(ctx, lf, 'jam' if lf >= 222 else 'ready', drawer=dr, cat_in=lf >= 212, cat_eye='closed', tail=lf >= 222)
        pile(ctx)
        if lf < 212:
            cx_ = lerp(800, PX - 10, back); cy_ = lerp(GND - 4, PYB - 50, back) - 200 * math.sin(math.pi * back)
            cat(ctx, cx_, cy_, 0.5, 1, lf, 'sit', eye='smug' if back == 0 else 'happy')
        tw = lf >= 222
        d = stand(ctx, DAD, DADX - 40, KD, P(eye='happy' if lf < 200 else 'shock' if not tw else 'glare', mouth='grin' if lf < 200 else 'open' if not tw else 'flat',
                                             lsh=-30, lel=-120, rsh=40, rel=-60, head=-12 if lf < 200 else 6), -1)
        if tw:
            twitch(ctx, d['head'][0] - d['R'] * 0.8, d['head'][1] - d['R'] * 0.9, lf, 1.0)
        k = kid_folder(ctx, 560, 'happy', 'grin', lf, hold=False)
        sheet(ctx, k['front'][0] + 10, k['front'][1] - 30, 0.05, 0.6, hw=True)
    ctx.restore()
    # labels
    if lf < 30:
        label(ctx, "*purrrr~*", 540, 640, 100, PINK, 0.04, pop(lf, 2, 6))
        if lf >= 12:
            label(ctx, "\"...it PURRS?!\"", 540, 1440, 116, WHITE, -0.03, pop(lf, 12, 16))
    elif lf < 60:
        label2(ctx, "\"Dad...", "it's the CAT.\"", YEL, pop(lf, 30, 34), 112, y=1440)
    elif lf < 100:
        if lf < 76:
            label(ctx, "*SHHK!*", 540, 1440, 110, WHITE, -0.04, pop(lf, 62, 65))
        card(ctx, 'p2', lf, 64)
        if lf >= 76:
            label(ctx, "*mrrp?*", 540, 1440, 110, PINK, 0.03, pop(lf, 76, 80))
    elif lf < 160:
        if lf < 116:
            label(ctx, "*hop*", 540, 640, 100, CYAN, -0.04, pop(lf, 102, 105))
        elif lf < 132:
            label(ctx, "*DING!*", 540, 640, 120, GREEN, 0.04, pop(lf, 116, 119))
        else:
            label(ctx, "\"YAY!\"", 330, 700, 100, YEL, -0.08, pop(lf, 132, 135))
            label2(ctx, "\"...NAILED", "IT.\"", WHITE, pop(lf, 138, 142), 120, col2=MINT, y=1440)
    else:
        if lf < 200:
            label2(ctx, "\"Honey! Can you print", "my BOARDING PASS?\"", PINK, pop(lf, 162, 166), 90, y=1440)
        elif lf < 222:
            label(ctx, "*hop* *mrrp~*", 540, 640, 96, CYAN, 0.04, pop(lf, 200, 204))
        else:
            label(ctx, "*BEEP! BEEP!*", 540, 640, 100, RED, -0.04, pop(lf, 222, 225))
            label2(ctx, "\"...of", "COURSE.\"", WHITE, pop(lf, 228, 232), 124, col2=ORANGE, y=1440)


SHOTS = [(0, s1), (60, s2), (150, s3), (300, s4), (370, s5)]
CUTS = (60, 126, 150, 200, 250, 300, 370, 432, 470, 630)


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
                              "-i", "out/dad_vs_printer_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
