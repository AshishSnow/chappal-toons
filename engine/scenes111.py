"""'GETTING THE CAT INTO THE CARRIER'. Original, general-audience comedy short, 22s.
Hook:   hallway medium shot (front door, coat rack, console table, 'VET 10AM' calendar): sweaty Dad holding the cat out
        over the open pet carrier, the cat STARFISHED - all four legs locked straight out on the rim
        "GET... IN... THE BOX!!" + caption 'GETTING THE CAT INTO THE CARRIER:'; kid watching, shocked.
Beat 1: PLAN A: TREATS. macro on the carrier: a treat drops in *plink* -> a sneaky paw reaches in *swipe* and fishes it
        out -> NOPE! -> medium: cat munching outside the carrier *crunch crunch*, Dad "...SMART kitty."
Beat 2: PLAN B: THE BLANKET. Dutch tilt: Dad tiptoes with a blanket at the sleeping cat -> *FWUMP!* pounce "GOT HER!!"
        -> lifts it: "...EMPTY?!" -> tilt up: the cat sits on top of the coat rack wearing Dad's hat *meow.* "...HOW?!"
Beat 3: the one close-up: scratched-up Dad, hair full of fur, twitch "I'm SMARTER..." "...than a CAT!!"
Twist:  Dad puts the carrier on his own head to demonstrate "SEE? It's COZY!" -> the cat on the console table taps the
        door shut *CLICK!* -> PLOT TWIST: NOW DAD'S STUCK. "...a little HELP?" kid laughing -> Mom walks in with the car
        keys "Who's going to the VET?" -> kid + cat both point at Dad "HIM!" -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face, rays, _SCR
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes103 import stamp
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
TEAL = hx('19b8b0'); CARR = hx('4fc3ff'); CARR_D = hx('2a8fd0')
FUR = hx('a7b2d6'); FURD = hx('6f7aa3'); FURL = hx('f6f6ff')
DAD = dict(doodle.DAD, shirt=hx('ff8a1f'), pants=hx('34477e'))
MOM = dict(doodle.MOM_G, shirt=hx('8a3cff'), pants=hx('2f4a8a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('22b45a'), pants=hx('3d7bff'), shoes=hx('ffc93c'))
N = 660
FLOOR, GND = 1560, 1595
KD, KK, KM = 1.1, 0.85, 1.0
DOORX0, DOORX1, DOORTOP = 1620, 1880, 940
RACKX = 1430

CAPS = {'p1': [[("GETTING THE ", OUT), ("CAT", PURPLE)], [("INTO THE ", OUT), ("CARRIER:", BLUE)]],
        'p2': [[("PLOT TWIST:", RED)], [("NOW ", OUT), ("DAD'S", ORANGE), (" STUCK.", OUT)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ the cat (original, fluffy grey-blue)
def tube(ctx, pts, w, col, lw=5):
    ctx.new_path(); ctx.move_to(*pts[0])
    if len(pts) == 4:
        ctx.curve_to(*pts[1], *pts[2], *pts[3])
    else:
        for q in pts[1:]:
            ctx.line_to(*q)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    setc(ctx, INK); ctx.set_line_width(w + lw * 2); ctx.stroke_preserve(); setc(ctx, col); ctx.set_line_width(w); ctx.stroke()


def paw(ctx, x, y, r):
    ellipse(ctx, x, y, r, r * 0.85); fl(ctx, FURL, 4)
    for k in (-1, 0, 1):
        ctx.move_to(x + k * r * 0.4, y - r * 0.8); ctx.line_to(x + k * r * 0.4, y - r * 0.3)
    ink(ctx, 3); ctx.stroke()


def cat_head(ctx, eye='normal', hiss=False, hat=False, lf=0):
    for sx in (-1, 1):
        poly(ctx, [(sx * 22, -36), (sx * 54, -80), (sx * 54, -16)]); fl(ctx, FUR, 5)
        poly(ctx, [(sx * 30, -36), (sx * 49, -64), (sx * 48, -28)]); setc(ctx, hx('ffb3c0')); ctx.fill()
    ellipse(ctx, 0, 0, 62, 52); fl(ctx, FUR, 5)
    for k in (-1, 0, 1):   # tabby stripes
        ctx.move_to(k * 14, -50); ctx.line_to(k * 12, -32); setc(ctx, FURD); ctx.set_line_width(7); ctx.stroke()
    ellipse(ctx, 0, 22, 30, 20); setc(ctx, FURL); ctx.fill()
    if eye == 'closed':
        for sx in (-1, 1):
            ctx.new_path(); ctx.arc(sx * 23, -2, 11, 0.3, math.pi - 0.3); ink(ctx, 4); ctx.stroke()
    elif eye == 'smug':
        for sx in (-1, 1):
            ellipse(ctx, sx * 23, 0, 13, 9); setc(ctx, hx('ffd23f')); ctx.fill()
            ellipse(ctx, sx * 23, 1, 3, 8); setc(ctx, INK); ctx.fill()
            ctx.new_path(); ctx.move_to(sx * 38, -6); ctx.line_to(sx * 8, -6); ink(ctx, 6); ctx.stroke()
    elif eye == 'glare':
        for sx in (-1, 1):
            ellipse(ctx, sx * 23, 0, 12, 12); setc(ctx, hx('ffd23f')); ctx.fill()
            ellipse(ctx, sx * 23, 0, 3, 10); setc(ctx, INK); ctx.fill()
            ctx.new_path(); ctx.move_to(sx * 38, -18); ctx.line_to(sx * 8, -6); ink(ctx, 6); ctx.stroke()
    else:   # big shiny eyes
        for sx in (-1, 1):
            ellipse(ctx, sx * 23, -2, 15, 17); setc(ctx, INK); ctx.fill()
            ellipse(ctx, sx * 23 - 5, -8, 6, 6); setc(ctx, WHITE); ctx.fill()
            ellipse(ctx, sx * 23 + 5, 4, 3, 3); setc(ctx, WHITE); ctx.fill()
    for sx in (-1, 1):
        ellipse(ctx, sx * 40, 16, 9, 5); setc(ctx, hx('ff9aa8')); ctx.fill()
        for dy in (-4, 6):
            ctx.move_to(sx * 32, 14 + dy); ctx.line_to(sx * 74, 8 + dy * 2)
        ink(ctx, 2); ctx.stroke()
    poly(ctx, [(-7, 10), (7, 10), (0, 18)]); setc(ctx, hx('ff7a90')); ctx.fill()
    if hiss:
        ellipse(ctx, 0, 32, 18, 14); fl(ctx, hx('8a2a3a'), 3)
        for sx in (-1, 1):
            poly(ctx, [(sx * 10, 20), (sx * 4, 20), (sx * 7, 30)]); setc(ctx, WHITE); ctx.fill()
    else:
        ctx.new_path(); ctx.arc(-6, 19, 6, 0.2, math.pi - 0.2); ctx.new_sub_path(); ctx.arc(6, 19, 6, 0.2, math.pi - 0.2); ink(ctx, 3); ctx.stroke()
    if hat:   # Dad's blue bobble hat, way too big
        ctx.save(); ctx.rotate(-0.15)
        ctx.new_path(); ctx.arc(0, -40, 66, math.pi, 2 * math.pi); ctx.close_path(); fl(ctx, BLUE, 5)
        rect_r(ctx, -72, -48, 144, 26, 12); fl(ctx, hx('ffffff'), 5)
        ellipse(ctx, 0, -112, 20, 20); fl(ctx, RED, 4)
        ctx.restore()


def cat(ctx, x, y, s, f=1, lf=0, mode='sit', eye='normal', hiss=False, hat=False, munch=False):
    """sit/sleep: (x,y)=feet"""
    ctx.save(); ctx.translate(x, y); ctx.scale(f * s, s)
    if mode == 'sleep':
        tube(ctx, [(-80, -20), (-150, -10), (-120, 30), (-40, 10)], 16, FUR)
        b = 1 + 0.04 * math.sin(lf * 0.15)
        ellipse(ctx, 0, -48, 104, 50 * b); fl(ctx, FUR, 5)
        for k in range(3):
            ctx.move_to(-40 + k * 30, -94 * b); ctx.line_to(-34 + k * 30, -72); setc(ctx, FURD); ctx.set_line_width(8); ctx.stroke()
        ctx.translate(84, -76); ctx.scale(0.95, 0.95); cat_head(ctx, 'closed')
    else:
        sw = 8 * math.sin(lf * 0.3)
        tube(ctx, [(-40, -10), (-120, -10), (-120, -90), (-86 + sw, -126)], 16, FUR)
        ellipse(ctx, 0, -72, 64, 74); fl(ctx, FUR, 5)
        ellipse(ctx, 10, -60, 32, 52); setc(ctx, FURL); ctx.fill()
        for px in (-24, 28):
            ellipse(ctx, px, -6, 24, 13); fl(ctx, FURL, 4)
        ctx.translate(6, -166 + (4 * math.sin(lf * 1.2) if munch else 0)); cat_head(ctx, eye, hiss, hat, lf)
        if munch:   # treat crumbs
            for k in range(3):
                ellipse(ctx, 40 + k * 14, 40 + ((lf * 5 + k * 9) % 30), 5, 5); setc(ctx, hx('b5703a')); ctx.fill()
    ctx.restore()


def star_cat(ctx, cx, cy, s, legs, eye='glare', hiss=True, lf=0):
    """the cat STARFISHED: body centre (cx,cy), legs = 4 paw targets in world coords (straight locked limbs)"""
    vib = 2.5 * math.sin(lf * 2.1)
    roots = [(-34, -50), (34, -50), (-30, 60), (30, 60)]
    tube(ctx, [(cx, cy + 80 * s), (cx + 10 * s, cy + 150 * s), (cx - 40 * s, cy + 170 * s), (cx - 10 * s + vib, cy + 210 * s)], 16 * s, FUR, 5 * s)
    for (rx, ry), (px, py) in zip(roots, legs):
        a = (cx + rx * s, cy + ry * s)
        tube(ctx, [a, (px + vib, py)], 30 * s, FUR, 5 * s)
        paw(ctx, px + vib, py, 18 * s)
    ellipse(ctx, cx, cy, 62 * s, 96 * s); fl(ctx, FUR, 5)
    ellipse(ctx, cx, cy + 12 * s, 32 * s, 62 * s); setc(ctx, FURL); ctx.fill()
    for k in range(3):   # puffed-up fur tufts
        for sx in (-1, 1):
            ctx.move_to(cx + sx * 60 * s, cy - 40 * s + k * 34 * s); ctx.line_to(cx + sx * 80 * s, cy - 50 * s + k * 34 * s)
    ink(ctx, 5); ctx.stroke()
    ctx.save(); ctx.translate(cx + vib, cy - 130 * s); ctx.scale(s, s); cat_head(ctx, eye, hiss); ctx.restore()


# ------------------------------------------------------------------ the pet carrier (front view)
def carrier(ctx, x, yb, w=250, h=190, door=0.0, lid=0.0, treat=False, inner=None):
    """front-loading pet carrier standing on yb. door 0 = shut (grille), 1 = swung wide open to the left.
    lid>0: top hatch flipped open. inner(ctx) draws whatever is visible inside the door hole"""
    x0, y0 = x - w / 2, yb - h
    if lid > 0:   # open top hatch behind
        ctx.save(); ctx.translate(x, y0); ctx.scale(1, -0.25 - 0.4 * lid)
        rect_r(ctx, -w / 2, 0, w, h * 0.55, 20); fl(ctx, CARR_D, 5)
        ctx.restore()
    # body
    rect_r(ctx, x0, y0, w, h, 26); fl(ctx, CARR, 5)
    # top shell band + handle
    rect_r(ctx, x0, y0, w, h * 0.32, 26); fl(ctx, CARR_D, 5)
    if lid == 0:
        ctx.new_path(); ctx.arc(x, y0 + 4, w * 0.22, math.pi, 2 * math.pi); setc(ctx, INK); ctx.set_line_width(26); ctx.stroke()
        ctx.new_path(); ctx.arc(x, y0 + 4, w * 0.22, math.pi, 2 * math.pi); setc(ctx, hx('ffd23f')); ctx.set_line_width(14); ctx.stroke()
    for k in range(3):   # vent slots
        rect_r(ctx, x0 + 14, y0 + h * 0.42 + k * 26, 10, 18, 5); setc(ctx, CARR_D); ctx.fill()
        rect_r(ctx, x0 + w - 24, y0 + h * 0.42 + k * 26, 10, 18, 5); setc(ctx, CARR_D); ctx.fill()
    # door hole
    dw, dh = w * 0.62, h * 0.56
    dx0, dy0 = x - dw / 2, yb - dh - 18
    rect_r(ctx, dx0, dy0, dw, dh, 16); fl(ctx, hx('2a2440'), 4)
    if treat:
        ellipse(ctx, x + 10, yb - 34, 16, 11); fl(ctx, hx('c07a3a'), 3)
    if inner:
        ctx.save(); rect_r(ctx, dx0, dy0, dw, dh, 16); ctx.clip(); inner(ctx, dx0, dy0, dw, dh); ctx.restore()
    # grille door, hinged on the left edge
    sc = math.cos(door * math.pi * 0.85)
    ctx.save(); ctx.translate(dx0, 0); ctx.scale(sc if abs(sc) > 0.05 else 0.05, 1)
    rect_r(ctx, 0, dy0, dw, dh, 16); ink(ctx, 12); ctx.stroke_preserve(); setc(ctx, hx('dfe6f0')); ctx.set_line_width(6); ctx.stroke()
    for k in range(1, 6):
        ctx.move_to(dw * k / 6, dy0 + 4); ctx.line_to(dw * k / 6, dy0 + dh - 4)
    ink(ctx, 11); ctx.stroke()
    for k in range(1, 6):
        ctx.move_to(dw * k / 6, dy0 + 4); ctx.line_to(dw * k / 6, dy0 + dh - 4)
    setc(ctx, hx('dfe6f0')); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()
    # paw-print sticker
    for (px, py, r) in ((x0 + w - 44, y0 + 24, 9),):
        ellipse(ctx, px, py + 4, r, r * 0.8); setc(ctx, WHITE); ctx.fill()
        for a in (-1, 0, 1):
            ellipse(ctx, px + a * r * 0.8, py - r * 0.9 + abs(a) * 3, r * 0.35, r * 0.35); setc(ctx, WHITE); ctx.fill()
    return (dx0, dy0, dw, dh)


# ------------------------------------------------------------------ set: cosy front hallway
def coat_rack(ctx, x, lf, hat=True):
    ctx.move_to(x, FLOOR + 10); ctx.line_to(x, FLOOR - 560)
    setc(ctx, INK); ctx.set_line_width(30); ctx.stroke()
    ctx.move_to(x, FLOOR + 10); ctx.line_to(x, FLOOR - 560); setc(ctx, hx('a8683e')); ctx.set_line_width(18); ctx.stroke()
    for s in (-1, 1):
        ctx.move_to(x, FLOOR - 520); ctx.line_to(x + s * 60, FLOOR - 570)
        ctx.move_to(x, FLOOR + 6); ctx.line_to(x + s * 80, FLOOR + 24)
    setc(ctx, INK); ctx.set_line_width(16); ctx.stroke()
    ellipse(ctx, x, FLOOR - 572, 22, 16); fl(ctx, hx('a8683e'), 4)
    # coats
    for s, c in ((-1, RED), (1, TEAL)):
        cx = x + s * 52
        poly(ctx, [(cx - 30, FLOOR - 560), (cx + 30, FLOOR - 560), (cx + 55, FLOOR - 300), (cx - 55, FLOOR - 300)]); fl(ctx, c, 5)
        ctx.move_to(cx, FLOOR - 540); ctx.line_to(cx, FLOOR - 310); setc(ctx, dark(c, 0.8)); ctx.set_line_width(4); ctx.stroke()
    if hat:
        ctx.save(); ctx.translate(x, FLOOR - 590)
        ctx.new_path(); ctx.arc(0, 0, 50, math.pi, 2 * math.pi); ctx.close_path(); fl(ctx, BLUE, 5)
        rect_r(ctx, -56, -8, 112, 22, 10); fl(ctx, WHITE, 4)
        ellipse(ctx, 0, -56, 16, 16); fl(ctx, RED, 4)
        ctx.restore()


def hallway(ctx, lf, opn=0.0, hat=True, table_cat=None):
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, hx('d9f3e6')); ctx.fill()
    rnd = random.Random(111)
    for k in range(90):   # little stars + paw prints wallpaper
        x, y = rnd.uniform(-200, 2400), rnd.uniform(300, 1520)
        if k % 2:
            sparkle(ctx, x, y, 10, hx('a6e3c8'))
        else:
            ellipse(ctx, x, y, 7, 6); setc(ctx, hx('a6e3c8')); ctx.fill()
            for a in (-1, 0, 1):
                ellipse(ctx, x + a * 6, y - 8 + abs(a) * 2, 2.6, 2.6); ctx.fill()
    # wainscot
    ctx.rectangle(-3000, FLOOR - 300, 9000, 300); setc(ctx, hx('fff6df')); ctx.fill()
    ctx.move_to(-3000, FLOOR - 300); ctx.line_to(6000, FLOOR - 300); ink(ctx, 5); ctx.stroke()
    for k in range(-10, 40):
        ctx.move_to(k * 120, FLOOR - 280); ctx.line_to(k * 120, FLOOR - 20)
    setc(ctx, hx('efe0bf')); ctx.set_line_width(4); ctx.stroke()
    # floor
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('d9a46a')); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(6000, FLOOR); ink(ctx, 6); ctx.stroke()
    for k in range(-30, 60):
        ctx.move_to(k * 110, FLOOR); ctx.line_to(k * 110 - 300, FLOOR + 900)
    setc(ctx, hx('c78f58')); ctx.set_line_width(4); ctx.stroke()
    # front door (right)
    rect_r(ctx, DOORX0 - 24, DOORTOP - 24, DOORX1 - DOORX0 + 48, FLOOR - DOORTOP + 24, 10); fl(ctx, WHITE, 5)
    ctx.rectangle(DOORX0, DOORTOP, DOORX1 - DOORX0, FLOOR - DOORTOP); setc(ctx, hx('ffe9a8')); ctx.fill()
    dw = (DOORX1 - DOORX0) * (1 - 0.82 * opn)
    ctx.rectangle(DOORX0, DOORTOP, dw, FLOOR - DOORTOP); fl(ctx, hx('ff6f61'), 5)
    if opn < 0.5:
        rect_r(ctx, DOORX0 + dw * 0.25, DOORTOP + 60, dw * 0.5, 140, 60); fl(ctx, hx('bfeaff'), 4)
        ellipse(ctx, DOORX0 + dw * 0.18, DOORTOP + 360, 12, 12); fl(ctx, GOLD, 3)
        # little wreath
        ctx.new_path(); ctx.arc(DOORX0 + dw / 2, DOORTOP + 300, 50, 0, 2 * math.pi); setc(ctx, INK); ctx.set_line_width(30); ctx.stroke()
        ctx.new_path(); ctx.arc(DOORX0 + dw / 2, DOORTOP + 300, 50, 0, 2 * math.pi); setc(ctx, GREEN); ctx.set_line_width(20); ctx.stroke()
        ellipse(ctx, DOORX0 + dw / 2, DOORTOP + 350, 16, 12); fl(ctx, RED, 3)
    # doormat
    rect_r(ctx, DOORX0 - 10, FLOOR + 10, DOORX1 - DOORX0 + 20, 40, 10); fl(ctx, hx('ffb347'), 4)
    # calendar 'VET 10AM'
    cx, cy = 980, 860
    ctx.move_to(cx, cy - 30); ctx.line_to(cx, cy - 10); ink(ctx, 4); ctx.stroke()
    ellipse(ctx, cx, cy - 34, 6, 6); setc(ctx, INK); ctx.fill()
    rect_r(ctx, cx - 90, cy - 10, 180, 200, 8); fl(ctx, WHITE, 4)
    ctx.rectangle(cx - 90, cy - 10, 180, 44); setc(ctx, RED); ctx.fill()
    for r in range(4):
        for c in range(5):
            ctx.rectangle(cx - 78 + c * 32, cy + 46 + r * 34, 22, 22); setc(ctx, hx('e6e6ee')); ctx.fill()
    ctx.new_path(); ellipse(ctx, cx + 22, cy + 96, 36, 26); setc(ctx, RED); ctx.set_line_width(5); ctx.stroke()
    text(ctx, "VET", cx + 22, cy + 96, 26, RED, outline=WHITE, ow=4, shadow=False)
    # framed cat portrait
    fx, fy = 560, 880
    rect_r(ctx, fx - 80, fy - 90, 160, 180, 8); fl(ctx, hx('ffc93c'), 5)
    rect_r(ctx, fx - 60, fy - 70, 120, 140, 6); fl(ctx, hx('ffe4f0'), 4)
    ctx.save(); ctx.translate(fx, fy + 10); ctx.scale(0.55, 0.55); cat_head(ctx, 'closed'); ctx.restore()
    # console table + lamp + plant + key bowl
    tx0, tx1, ty = 180, 700, FLOOR - 250
    for lx in (tx0 + 30, tx1 - 30):
        rect_r(ctx, lx - 12, ty, 24, 250, 8); fl(ctx, hx('a8683e'), 4)
    rect_r(ctx, tx0, ty - 26, tx1 - tx0, 34, 10); fl(ctx, hx('c98a52'), 5)
    rect_r(ctx, tx0 + 40, ty + 30, tx1 - tx0 - 80, 60, 8); fl(ctx, hx('b97a44'), 4)
    poly(ctx, [(tx0 + 80, ty - 26), (tx0 + 120, ty - 26), (tx0 + 110, ty - 120), (tx0 + 90, ty - 120)]); fl(ctx, hx('ff9ab8'), 4)
    poly(ctx, [(tx0 + 40, ty - 120), (tx0 + 160, ty - 120), (tx0 + 130, ty - 210), (tx0 + 70, ty - 210)]); fl(ctx, YEL, 4)
    rect_r(ctx, tx1 - 130, ty - 90, 70, 66, 14); fl(ctx, hx('ff8a5c'), 4)
    for a in (-0.7, -0.25, 0.2, 0.6):
        ellipse(ctx, tx1 - 95 + 50 * math.sin(a), ty - 120 - 20 * math.cos(a), 18, 40, a); fl(ctx, GREEN, 4)
    if table_cat:
        table_cat(ctx, (tx0 + tx1) / 2 + 40, ty - 26)
    # shoe rack under the table
    for k, c in enumerate((RED, BLUE, GOLD, PINK)):
        ellipse(ctx, tx0 + 90 + k * 100, FLOOR - 16, 40, 18); fl(ctx, c, 4)
    # scratching post + cat bed
    rect_r(ctx, -40, FLOOR - 340, 60, 340, 10); fl(ctx, hx('e8c48a'), 5)
    for k in range(8):
        ctx.move_to(-38, FLOOR - 320 + k * 40); ctx.line_to(18, FLOOR - 300 + k * 40)
    setc(ctx, hx('b5925a')); ctx.set_line_width(4); ctx.stroke()
    ellipse(ctx, -10, FLOOR - 350, 70, 20); fl(ctx, PINK, 5)
    # rug
    ellipse(ctx, 1020, FLOOR + 110, 420, 70); fl(ctx, hx('b98cff'), 5)
    ellipse(ctx, 1020, FLOOR + 110, 330, 46); setc(ctx, hx('d7c0ff')); ctx.fill()
    coat_rack(ctx, RACKX, lf, hat)


# ------------------------------------------------------------------ people
def stand(ctx, ch, x, k, p, f_=1, g=GND):
    return draw(ctx, x, g - 186 * k, k, f_, ch, p)


def kneel(ctx, ch, x, k, p, f_=1, feet=GND):
    return draw(ctx, x, feet - 186 * k + 62 * k * 1.35, k, f_, ch, p)


CARX = 860   # carrier position in the hall


def hold_scene(ctx, lf, dad_eye='glare', dad_mouth='scream', kid=True):
    """Dad holding the starfished cat over the open-top carrier"""
    if kid:
        dk = stand(ctx, KID, 470, KK, P(eye='shock', mouth='open', lsh=160, lel=-60, rsh=160, rel=-60, head=4))
    carrier(ctx, CARX, FLOOR + 30, 270, 200, door=0.0, lid=1.0)
    jig = 3 * math.sin(lf * 1.7)
    d = stand(ctx, DAD, 1090, KD, P(eye=dad_eye, mouth=dad_mouth, lsh=95, lel=-10, rsh=85, rel=-5, torso=14, head=-8, lhip=10, rhip=-14), -1)
    rim = FLOOR + 30 - 200
    cx, cy = CARX + 20 + jig, (d['front'][1] + d['back'][1]) / 2 - 10
    legs = [(cx - 190, cy - 110), (cx + 150, cy - 150), (CARX - 175, rim + 6), (CARX + 165, rim + 6)]
    star_cat(ctx, cx, cy, 1.0, legs, 'glare', True, lf)
    # Dad's hands gripping the cat's sides
    for h in (d['front'], d['back']):
        tube(ctx, [h, (cx + 58, cy - 20 + (h[1] - d['front'][1]) * 0.5)], 30 * KD * 1.35 * 0.88, DAD['skin'], 4)
        ellipse(ctx, cx + 58, cy - 20 + (h[1] - d['front'][1]) * 0.5, 22, 20); fl(ctx, DAD['skin'], 4)
    sweat(ctx, d['head'][0] + d['R'] * 1.0, d['head'][1] - d['R'] * 0.3, lf, 0.9)
    return d


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = 1.12 + 0.04 * eio(pop(lf, 0, 54))
    ctx.save(); cam(ctx, 880, 1290, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    hallway(ctx, lf)
    hold_scene(ctx, lf)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"GET... IN...", "THE BOX!!\"", WHITE, t, 120, col2=GOLD, y=1440)
    if lf < 40:
        label(ctx, "*HISSSS!*", 330, 700, 80, PINK, -0.12, 1 if lf == f else pop(lf, 2, 5))


# ------------------------------------------------------------------ shot 2: PLAN A treats
def macro(ctx, f, il):
    # il 0..70: big carrier, door open; 6 treat drops in *plink* ; 22 paw sneaks in *swipe* ; 40 pulls it out ; 46 NOPE!
    ctx.save(); cam(ctx, 840, 1400, 2.5 + 0.08 * eio(il / 70), 0, shake_at(il, [10, 46], 6, 6), f)
    hallway(ctx, il)

    def inner(c, dx0, dy0, dw, dh):
        # paw comes in from the left edge of the door hole, hooks the treat, slides back out
        u = eio(pop(il, 22, 36)) * (1 - eio(pop(il, 40, 50)))
        tx = lerp(dx0 - 60, CARX + 10, u)
        tube(c, [(dx0 - 120, FLOOR - 16), (tx - 20, FLOOR - 16)], 46, FUR, 5)
        paw(c, tx, FLOOR - 18, 30)
    tr = il < 6 or (il >= 10 and il < 40)
    carrier(ctx, CARX, FLOOR + 30, 270, 200, door=1.0, treat=tr, inner=inner)
    if il < 10:   # treat falling in
        y = lerp(FLOOR - 300, FLOOR - 4, eio(il / 10))
        ellipse(ctx, CARX + 10, y, 16, 11); fl(ctx, hx('c07a3a'), 3)
    if 40 <= il < 70:   # the paw waves the treat outside the door, left
        u = eio(pop(il, 40, 50))
        tube(ctx, [(CARX - 300, FLOOR + 40), (CARX - 160, FLOOR + 20 - 60 * u)], 46, FUR, 5)
        paw(ctx, CARX - 160, FLOOR + 20 - 60 * u, 30)
        ellipse(ctx, CARX - 160, FLOOR - 16 - 60 * u, 16, 11); fl(ctx, hx('c07a3a'), 3)
    ctx.restore()
    label(ctx, "PLAN A: TREATS.", 540, 560, 100, GOLD, -0.03, pop(il, 0, 4))
    if 6 <= il < 22:
        label(ctx, "*plink*", 540, 1560, 90, WHITE, 0.04, pop(il, 6, 9))
    if 22 <= il < 46:
        label(ctx, "*swipe*", 540, 1560, 100, CYAN, -0.04, pop(il, 22, 25))
    if il >= 46:
        stamp(ctx, "NOPE!", 540, 1440, pop(il, 46, 50), -0.12)


def munch_scene(ctx, f, il):
    # il 0..70: cat munching the treat beside the carrier *crunch crunch*, Dad kneeling, glaring "...SMART kitty."
    ctx.save(); cam(ctx, 900, 1330, 1.25, 0, 0, f)
    hallway(ctx, il + 70)
    carrier(ctx, CARX + 40, FLOOR + 30, 270, 200, door=1.0, treat=False)
    d = kneel(ctx, DAD, 1200, KD, P(eye='glare', mouth='flat', lsh=20, lel=-110, rsh=-20, rel=-100, torso=6), -1)
    cat(ctx, 620, FLOOR + 40, 0.8, 1, il, 'sit', 'closed', munch=True)
    ctx.restore()
    label(ctx, "*crunch crunch*", 540, 600, 90, GOLD, 0.03, pop(il, 0, 4))
    label2(ctx, "\"...SMART", "kitty.\"", WHITE, pop(il, 20, 24), 120, col2=PURPLE, y=1440)


def s2(ctx, f):
    il = f - 60
    if il < 70:
        macro(ctx, f, il)
    else:
        munch_scene(ctx, f, il - 70)


# ------------------------------------------------------------------ shot 3: PLAN B blanket
def blanket(ctx, pts, col=hx('ff9ab8')):
    poly(ctx, pts); fl(ctx, col, 5)
    ctx.save(); poly(ctx, pts); ctx.clip()
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    for k in range(int(min(xs)) - 300, int(max(xs)) + 300, 60):
        ctx.move_to(k, min(ys) - 10); ctx.line_to(k + 200, max(ys) + 10)
    setc(ctx, (1, 1, 1, 0.55)); ctx.set_line_width(14); ctx.stroke()
    ctx.restore()


def plan_b(ctx, f, il):
    # il 0..140: Dutch tilt; 0-36 Dad tiptoes with a blanket toward the sleeping cat on the rug;
    #            38 *FWUMP!* pounce, Dad kneels on a blanket lump "GOT HER!!" ; 70 lifts it: nothing "...EMPTY?!"
    #            96 tilt up to the coat rack top: the cat sits on it, wearing Dad's hat *meow.* "...HOW?!"
    up = eio(pop(il, 96, 106))
    rot = 9 * (1 - up) - 4 * up
    ctx.save(); cam(ctx, lerp(1000, RACKX + 150, up), lerp(1310, 1060, up), lerp(1.1, 1.5, up), rot, shake_at(il, [38], 12, 14), f)
    hallway(ctx, il + 140, hat=il < 90)
    catx = 1000
    if il < 38:
        cat(ctx, catx, FLOOR + 90, 0.75, 1, il, 'sleep')
        x = lerp(1440, 1220, eio(il / 36)); s_ = math.sin(il * 0.7)
        hy = GND - 560 - 10 * abs(s_)
        blanket(ctx, [(x - 230, hy), (x + 150, hy - 30), (x + 190, hy + 260), (x - 120, hy + 300)])
        d = stand(ctx, DAD, x, KD, P(eye='smug', mouth='grin', lsh=165, lel=-10, rsh=-160, rel=10, torso=10, lhip=16 * s_, rhip=-16 * s_, lkn=-20, rkn=-20), -1, GND - 10 * abs(s_))
    elif il < 70:
        sq = 1 - 0.15 * eout(pop(il, 38, 44))
        blanket(ctx, [(catx - 220, FLOOR + 130), (catx - 120, FLOOR - 60 * sq), (catx + 90, FLOOR - 80 * sq), (catx + 230, FLOOR + 130)])
        d = kneel(ctx, DAD, catx + 150, KD, P(eye='happy', mouth='grin', lsh=60, lel=-30, rsh=40, rel=-40, torso=30), -1)
        for k in range(6):
            a = k * 1.05 + 0.3
            ctx.move_to(catx + 260 * math.cos(a), FLOOR + 40 + 120 * math.sin(a)); ctx.line_to(catx + 330 * math.cos(a), FLOOR + 40 + 150 * math.sin(a))
        ink(ctx, 6); ctx.stroke()
    else:
        d = stand(ctx, DAD, catx + 120, KD, P(eye='shock', mouth='open', lsh=105, lel=-10, rsh=-105, rel=10), -1)
        a, b = d['front'], d['back']
        blanket(ctx, [a, b, (b[0] + 30, FLOOR - 10), (a[0] - 30, FLOOR)])
        if il >= 90:
            cat(ctx, RACKX, FLOOR - 568, 0.55, -1, il, 'sit', 'smug', hat=True)
    ctx.restore()
    if il < 38:
        label(ctx, "PLAN B: THE BLANKET.", 540, 560, 90, PINK, -0.03, pop(il, 0, 4))
        label(ctx, "*tiptoe tiptoe*", 540, 1440, 90, WHITE, 0.03, pop(il, 6, 10))
    elif il < 70:
        label(ctx, "*FWUMP!*", 540, 600, 130, GOLD, -0.05, pop(il, 38, 41))
        label(ctx, "\"GOT HER!!\"", 540, 1440, 130, WHITE, 0.03, pop(il, 44, 48))
    elif il < 96:
        label(ctx, "\"...EMPTY?!\"", 540, 1440, 130, WHITE, -0.03, pop(il, 72, 76))
    else:
        label(ctx, "*meow.*", 540, 560, 100, PURPLE, 0.04, pop(il, 104, 108))
        label(ctx, "\"...HOW?!\"", 540, 1440, 130, WHITE, -0.03, pop(il, 112, 116))


def s3(ctx, f):
    plan_b(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: close-up
def closeup(ctx, f, il):
    # il 0..80: Dad ECU, scratches + fur in his hair, twitch "I'm SMARTER..." 34 "...than a CAT!!"
    z = 1.0 + 0.06 * eio(il / 80)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('ffe0c4')), (1, hx('d9f3e6'))])); ctx.paint()
    ctx.save(); cam(ctx, 540, 960, z, 0, shake_at(il, [34], 8, 10), f)
    rays(ctx, 540, 900, 200, 1200, il * 0.03, (1, 1, 1), 0.35, 16)
    face(ctx, DAD, P(eye='glare', mouth='grin' if il < 34 else 'scream'), 540, 900, 205)
    # cat scratches (cute zig marks) + fluff stuck in hair + band-aid
    for (x, y, a) in ((420, 960, 0.4), (680, 1000, -0.3)):
        ctx.save(); ctx.translate(x, y); ctx.rotate(a)
        for k in range(3):
            ctx.move_to(-30, -14 + k * 14); ctx.line_to(30, -20 + k * 14)
        setc(ctx, hx('ff4a6a')); ctx.set_line_width(5); ctx.stroke(); ctx.restore()
    ctx.save(); ctx.translate(560, 800); ctx.rotate(-0.4)
    rect_r(ctx, -60, -18, 120, 36, 16); fl(ctx, hx('ffd7a8'), 4); ctx.restore()
    for (x, y) in ((380, 640), (520, 600), (700, 650), (610, 560)):
        for a in range(5):
            ctx.move_to(x, y); ctx.line_to(x + 26 * math.cos(a * 1.25), y + 26 * math.sin(a * 1.25))
        setc(ctx, FUR); ctx.set_line_width(9); ctx.stroke()
    twitch(ctx, 780, 680, il, 1.6)
    sweat(ctx, 290, 720, il, 1.5)
    ctx.restore()
    label(ctx, "\"I'm SMARTER...", 540, 1380, 110, WHITE, -0.03, pop(il, 3, 7))
    if il >= 34:
        label(ctx, "...than a CAT!!\"", 540, 1500, 120, RED, 0.03, pop(il, 34, 38))


def s4(ctx, f):
    closeup(ctx, f, f - 340)


# ------------------------------------------------------------------ shot 5: Dad demonstrates -> stuck -> Mom
def dad_with_carrier(ctx, x, lf, door, eye='happy', mouth='grin', wob=0.0, arms=(150, 150)):
    p = P(eye=eye, mouth=mouth, lsh=arms[0], lel=-40, rsh=arms[1], rel=-40, rot=wob, lhip=8, rhip=-8)
    d = stand(ctx, DAD, x, KD, p, -1)
    hd, R = d['head'], d['R']
    w, h = R * 2.9, R * 2.35

    def inner(c, dx0, dy0, dw, dh):
        pass
    # carrier over the head: draw its shell with the door hole cut out so Dad's face shows through
    ctx.save(); ctx.translate(hd[0], hd[1]); ctx.rotate(math.radians(wob) * -1)
    yb = h * 0.56
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    x0, y0 = -w / 2, yb - h
    dw, dh = w * 0.62, h * 0.56
    dx0, dy0 = -dw / 2, yb - dh - 18
    ctx.new_path(); rect_r(ctx, x0, y0, w, h, 26); ctx.new_sub_path()
    ctx.move_to(dx0, dy0 + 16); ctx.line_to(dx0, dy0 + dh - 16); ctx.line_to(dx0 + dw, dy0 + dh - 16); ctx.line_to(dx0 + dw, dy0 + 16); ctx.close_path()
    fl(ctx, CARR, 5)
    ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    ctx.new_path(); rect_r(ctx, x0, y0, w, h * 0.3, 26); fl(ctx, CARR_D, 5)
    ctx.new_path(); ctx.arc(0, y0 + 4, w * 0.22, math.pi, 2 * math.pi); setc(ctx, INK); ctx.set_line_width(26); ctx.stroke()
    ctx.new_path(); ctx.arc(0, y0 + 4, w * 0.22, math.pi, 2 * math.pi); setc(ctx, hx('ffd23f')); ctx.set_line_width(14); ctx.stroke()
    for k in range(3):
        rect_r(ctx, x0 + 14, y0 + h * 0.42 + k * 26, 10, 18, 5); setc(ctx, CARR_D); ctx.fill()
        rect_r(ctx, x0 + w - 24, y0 + h * 0.42 + k * 26, 10, 18, 5); setc(ctx, CARR_D); ctx.fill()
    sc = math.cos(door * math.pi * 0.85)
    ctx.translate(dx0, 0); ctx.scale(sc if abs(sc) > 0.05 else 0.05, 1)
    rect_r(ctx, 0, dy0, dw, dh, 16); ink(ctx, 12); ctx.stroke_preserve(); setc(ctx, hx('dfe6f0')); ctx.set_line_width(6); ctx.stroke()
    for col, lw_ in ((INK, 11), (hx('dfe6f0'), 5)):
        for k in range(1, 6):
            ctx.move_to(dw * k / 6, dy0 + 4); ctx.line_to(dw * k / 6, dy0 + dh - 4)
        setc(ctx, col); ctx.set_line_width(lw_); ctx.stroke()
    ctx.restore()
    ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    d['ctop'] = (hd[0], hd[1] - 0.44 * h)
    return d


def demo(ctx, f, il):
    # il 0..80: Dad puts the carrier on his own head "SEE? It's COZY!" ; cat on the console table ;
    #           44 paw taps the door *tap* -> 48-54 door swings shut *CLICK!* -> Dad's eyes pop
    ctx.save(); cam(ctx, 760, 1260, 1.2, 0, shake_at(il, [52], 8, 10), f)
    door = 1 - eio(pop(il, 46, 54))
    paw_out = eio(pop(il, 38, 46)) * (1 - eio(pop(il, 54, 62)))

    def tcat(c, x, y):
        cat(c, x - 20, y, 0.62, -1, il, 'sit', 'smug' if il < 56 else 'closed')
    hallway(ctx, il + 300, table_cat=tcat)
    shut = il >= 52
    d = dad_with_carrier(ctx, 800, il, door, 'shock' if shut else 'happy', 'open' if shut else 'grin', arms=(150, 150) if not shut else (40, 30))
    if 38 <= il < 64:   # cat paw reaching to the door
        sx = 480; sy = FLOOR - 250 - 26 - 100
        tx = lerp(sx, d['head'][0] - d['R'] * 1.0, paw_out)
        tube(ctx, [(sx, sy), (tx, d['head'][1] + 10)], 22, FUR, 4)
        paw(ctx, tx, d['head'][1] + 10, 16)
    ctx.restore()
    if il < 44:
        label2(ctx, "\"SEE? It's", "COZY!\"", WHITE, pop(il, 2, 6), 120, col2=TEAL, y=1440)
    elif il < 52:
        label(ctx, "*tap*", 540, 600, 100, PURPLE, 0.04, pop(il, 44, 47))
    else:
        label(ctx, "*CLICK!*", 540, 600, 130, GOLD, -0.05, pop(il, 52, 55))


def stuck(ctx, f, il):
    # il 0..70: Dad wobbles around with the carrier stuck on his head, kid laughs, cat smug ; card p2 ; "...a little HELP?"
    wob = 8 * math.sin(il * 0.25)
    ctx.save(); cam(ctx, 900, 1300, 1.08, -3, 0, f)

    def tcat(c, x, y):
        cat(c, x - 20, y, 0.62, -1, il, 'sit', 'smug')
    hallway(ctx, il + 380, table_cat=tcat)
    k = stand(ctx, KID, 1260, KK, P(eye='happy', mouth='scream', lsh=60, lel=-100, rsh=60, rel=-100, rot=4 * math.sin(il * 0.8)), -1)
    dad_with_carrier(ctx, 860 + 40 * math.sin(il * 0.12), il, 0.0, 'shock', 'open', wob, arms=(150 + 10 * math.sin(il * 0.6), 160))
    ctx.restore()
    card(ctx, 'p2', il, 4)
    if il < 40:
        label(ctx, "*HA HA HA!*", 790, 800, 76, YEL, 0.08, pop(il, 6, 9))
    label2(ctx, "\"...a little", "HELP?\"", WHITE, pop(il, 24, 28), 120, col2=ORANGE, y=1440)


def mom_scene(ctx, f, il):
    # il 0..60: Mom opens the front door with car keys "Who's going to the VET?" ; 30 kid + cat point at Dad "HIM!"
    ctx.save(); cam(ctx, 1180, 1250, 0.98, 0, shake_at(il, [30], 6, 8), f)
    hallway(ctx, il + 450, opn=eout(pop(il, 0, 6)))
    m = stand(ctx, MOM, lerp(1720, 1540, eio(pop(il, 0, 14))), KM, P(eye='happy', mouth='smile', lsh=20, rsh=120, rel=-60), -1)
    h = m['front']   # car keys
    ellipse(ctx, h[0], h[1] - 30, 16, 16); ink(ctx, 5); ctx.stroke()
    rect_r(ctx, h[0] - 8, h[1] - 18, 16, 40, 5); fl(ctx, GOLD, 3)
    pt = il >= 30
    k = stand(ctx, KID, 1270, KK, P(eye='happy', mouth='grin', lsh=20, rsh=100 if pt else 20, rel=0), -1)
    d = dad_with_carrier(ctx, 950, il, 0.0, 'shock', 'open', 0, arms=(150, 160))
    tx, ty = d['ctop']
    cat(ctx, tx + 10, ty + 6, 0.75, 1, il, 'sit', 'happy' if pt else 'smug')
    if pt:   # the cat points a paw down at Dad
        tube(ctx, [(tx + 30, ty - 60), (tx - 50, ty + 10)], 20, FUR, 4); paw(ctx, tx - 50, ty + 10, 15)
    ctx.restore()
    if il < 30:
        label2(ctx, "\"Who's going", "to the VET?\"", WHITE, pop(il, 4, 8), 110, col2=PURPLE, y=1440)
    else:
        label(ctx, "\"HIM!\"", 540, 1440, 170, GOLD, -0.04, pop(il, 30, 33))
        label(ctx, "*meow!*", 540, 600, 90, PURPLE, -0.08, pop(il, 32, 35))


def s5(ctx, f):
    lf = f - 420
    if lf < 80:
        demo(ctx, f, lf)
    elif lf < 150:
        stuck(ctx, f, lf - 80)
    elif lf < 210:
        mom_scene(ctx, f, lf - 150)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (200, s3), (340, s4), (420, s5)]
CUTS = (60, 130, 200, 340, 420, 500, 570, 630)


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
                              "-i", "out/cat_carrier_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
