"""'THE LAST PUZZLE PIECE'. Original, general-audience comedy short, 22s.
Hook:   sunny living-room medium shot: Dad kneeling at the coffee table next to a 1000-piece puzzle with ONE hole,
        holding the empty box upside down, screaming "WHERE'S THE LAST PIECE?!" + caption; kid on the sofa, cat asleep.
        (Rewatch easter egg: the red balloon piece is stuck in Dad's hair the whole time.)
Beat 1: top-down macro on the puzzle "999 PIECES DONE..." -> the hole glows "ONE LEFT!" -> medium: Dad grins, digs in
        the box *rustle rustle* -> flips it *shake shake* -> one crumb falls -> "...EMPTY?!"
Beat 2: Dutch-tilt search montage: cushions fly "THE SOFA?" NOPE! / magnifying glass over the rug "THE RUG?" NOPE! /
        lifts the stretchy cat "THE CAT?" *HISSS!* NOPE!
Beat 3: the one close-up: sweaty Dad, magnifying glass, twitch "It was RIGHT..." "...HERE!!" (piece visible in his hair)
Twist:  kid "Dad... your HAIR." -> PLOT TWIST: IT WAS IN DAD'S HAIR. -> "FOUND IT!!" -> macro *CLICK!* *DING!* confetti
        "DONE!!" -> the cat leaps onto the table *MEOW!* -> *CRASH!!* 1000 pieces everywhere, cat sits in the box ->
        Dad "...from the TOP." -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face, rays
from scenes58 import sweat, twitch
from scenes84 import eio
import scenes13
from scenes13 import card as _card13

RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
DAD = dict(doodle.DAD, shirt=hx('5aa8ff'), pants=hx('3a4a6a'), shoes=hx('7a4a2c'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff8a5c'), pants=hx('3d7bff'), shoes=hx('ffc93c'))
FUR = hx('ffa94d'); FURD = hx('e07a2a'); FURL = hx('fff0d8')
N = 660
FLOOR, GND = 1560, 1595
TX, TTOP = 1060, 1430          # coffee table centre x, top surface y
PW, PH, COLS, ROWS = 600, 420, 10, 7
CW = PW / COLS
HOLE = (7, 1)                  # the missing piece (top of the red balloon)
CX, CY, CZ = 1055, 1290, 1.17

CAPS = {'p1': [[("THE ", OUT), ("LAST ", RED), ("PUZZLE PIECE:", BLUE)]],
        'p2': [[("PLOT TWIST:", RED)], [("IT WAS IN ", OUT), ("DAD'S HAIR.", PURPLE)]]}
scenes13.CAPS = CAPS
card = _card13


def stand(ctx, ch, x, k, p, f_=1, feet=GND):
    return draw(ctx, x, feet - 186 * k, k, f_, ch, p)


SIT = dict(lhip=86, lkn=-86, rhip=88, rkn=-88)
KNEEL = dict(lhip=6, lkn=95, rhip=-6, rkn=95)


def kneel(ctx, ch, x, k, p, f_=1, feet=GND):
    return draw(ctx, x, feet - 186 * k + 62 * k * 1.35, k, f_, ch, p)


def sit(ctx, ch, x, k, p, f_=1, feet=GND):
    return draw(ctx, x, feet - 186 * k + 70 * k * 1.35, k, f_, ch, p)


# ------------------------------------------------------------------ the puzzle picture
def picture(ctx, lf=0):
    """the puzzle's picture in local coords (0,0)-(PW,PH): sunny hills + a red hot-air balloon"""
    ctx.set_source(vgrad(ctx, 0, 0, 0, PH, [(0, hx('6fc8ff')), (0.6, hx('bfeaff')), (1, hx('dff6ff'))]))
    ctx.rectangle(0, 0, PW, PH); ctx.fill()
    rays(ctx, 90, 80, 50, 120, 0.2, (1, 0.95, 0.5), 0.6, 12)
    ellipse(ctx, 90, 80, 42, 42); setc(ctx, hx('ffd23f')); ctx.fill()
    for (x, y, s) in ((230, 70, 1.0), (330, 160, 0.8), (560, 60, 0.7)):
        for dx, dy, r in ((-30, 6, 24), (0, -8, 32), (32, 6, 24)):
            ellipse(ctx, x + dx * s, y + dy * s, r * s, r * s); setc(ctx, WHITE); ctx.fill()
    ellipse(ctx, 140, 470, 320, 200); setc(ctx, hx('5fd06a')); ctx.fill()
    ellipse(ctx, 500, 480, 300, 190); setc(ctx, hx('3fb85a')); ctx.fill()
    for k in range(14):
        x = 20 + k * 43; y = 360 + 25 * math.sin(k * 1.7)
        ellipse(ctx, x, y, 7, 7); setc(ctx, (PINK, YEL, WHITE)[k % 3]); ctx.fill()
    # little house on the hill
    ctx.rectangle(240, 300, 60, 46); setc(ctx, hx('fff1c9')); ctx.fill()
    poly(ctx, [(232, 302), (270, 268), (308, 302)]); setc(ctx, RED); ctx.fill()
    # balloon
    bx, by = 450, 112
    for k in range(-1, 2):
        ctx.move_to(bx + k * 30, by + 50); ctx.line_to(bx + k * 14, by + 112)
    setc(ctx, hx('6a4a2a')); ctx.set_line_width(3); ctx.stroke()
    ellipse(ctx, bx, by, 58, 64); setc(ctx, RED); ctx.fill()
    ellipse(ctx, bx, by, 22, 64); setc(ctx, YEL); ctx.fill()
    ellipse(ctx, bx, by, 8, 64); setc(ctx, RED); ctx.fill()
    ellipse(ctx, bx - 26, by - 30, 10, 16); setc(ctx, (1, 1, 1, 0.6)); ctx.fill()
    rect_r(ctx, bx - 18, by + 108, 36, 28, 5); setc(ctx, hx('b9844a')); ctx.fill()


def _edge(ctx, x0, y0, x1, y1, sgn):
    """jigsaw edge from (x0,y0) to (x1,y1) with a knob bulging to side sgn (0 = flat)"""
    if sgn == 0:
        ctx.line_to(x1, y1); return
    dx, dy = x1 - x0, y1 - y0
    nx, ny = -dy, dx
    P_ = lambda u, v: (x0 + dx * u + nx * v * sgn, y0 + dy * u + ny * v * sgn)
    ctx.line_to(*P_(0.36, 0))
    ctx.curve_to(*P_(0.42, 0.06), *P_(0.28, 0.3), *P_(0.5, 0.3))
    ctx.curve_to(*P_(0.72, 0.3), *P_(0.58, 0.06), *P_(0.64, 0))
    ctx.line_to(x1, y1)


def hsg(i, j):   # horizontal edge on row-line j, column i
    return 0 if j in (0, ROWS) else (1 if (i + j) % 2 else -1)


def vsg(i, j):   # vertical edge on column-line i, row j
    return 0 if i in (0, COLS) else (1 if (i * 3 + j) % 2 else -1)


def cell_path(ctx, i, j):
    x0, y0, x1, y1 = i * CW, j * CW, (i + 1) * CW, (j + 1) * CW
    ctx.new_path(); ctx.move_to(x0, y0)
    _edge(ctx, x0, y0, x1, y0, -hsg(i, j))
    _edge(ctx, x1, y0, x1, y1, -vsg(i + 1, j))
    _edge(ctx, x1, y1, x0, y1, -hsg(i, j + 1))
    _edge(ctx, x0, y1, x0, y0, -vsg(i, j))
    ctx.close_path()


def grid(ctx, a=0.35, lw=2.0):
    ctx.new_path()
    for j in range(1, ROWS):
        ctx.move_to(0, j * CW)
        for i in range(COLS):
            _edge(ctx, i * CW, j * CW, (i + 1) * CW, j * CW, -hsg(i, j))
    for i in range(1, COLS):
        ctx.move_to(i * CW, 0)
        for j in range(ROWS):
            _edge(ctx, i * CW, j * CW, i * CW, (j + 1) * CW, vsg(i, j))
    setc(ctx, (0.2, 0.15, 0.2, a)); ctx.set_line_width(lw); ctx.stroke()


def puzzle(ctx, lf, hole=True, glow=0.0, done=0.0):
    """full puzzle in local coords"""
    rect_r(ctx, -10, -10, PW + 20, PH + 20, 6); setc(ctx, (0, 0, 0, 0.18)); ctx.fill()
    ctx.save(); ctx.rectangle(0, 0, PW, PH); ctx.clip()
    picture(ctx, lf)
    grid(ctx, 0.3 * (1 - done))
    if hole:
        ctx.save(); ctx.translate(3, 4); cell_path(ctx, *HOLE); setc(ctx, (0, 0, 0, 0.25)); ctx.fill(); ctx.restore()
        cell_path(ctx, *HOLE); setc(ctx, hx('c98a52')); ctx.fill_preserve()
        ink(ctx, 2.5); ctx.stroke()
        if glow > 0:
            cell_path(ctx, *HOLE); setc(ctx, YEL[:3] + (0.5 * glow * (0.6 + 0.4 * math.sin(lf * 0.6)),)); ctx.set_line_width(14); ctx.stroke()
    ctx.restore()
    rect_r(ctx, 0, 0, PW, PH, 4); ink(ctx, 4); ctx.stroke()
    if done > 0:
        rect_r(ctx, -6, -6, PW + 12, PH + 12, 6); setc(ctx, GOLD[:3] + (done,)); ctx.set_line_width(10); ctx.stroke()


def piece(ctx, x, y, s, rot=0.0, shadow=True):
    """the missing piece itself, centred at (x,y)"""
    i, j = HOLE
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s); ctx.translate(-(i + 0.5) * CW, -(j + 0.5) * CW)
    if shadow:
        ctx.save(); ctx.translate(4, 6); cell_path(ctx, i, j); setc(ctx, (0, 0, 0, 0.25)); ctx.fill(); ctx.restore()
    ctx.save(); cell_path(ctx, i, j); ctx.clip(); picture(ctx); ctx.restore()
    cell_path(ctx, i, j); ink(ctx, 3.5 / max(s, 0.3)); ctx.stroke()
    ctx.restore()


def bit(ctx, x, y, s, rot, col):
    """a generic flying puzzle piece"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-30, -30)
    _edge(ctx, -30, -30, 30, -30, -1); _edge(ctx, 30, -30, 30, 30, -1); _edge(ctx, 30, 30, -30, 30, 1); _edge(ctx, -30, 30, -30, -30, 0)
    ctx.close_path(); fl(ctx, col, 3)
    ctx.restore()


BITCOL = (hx('6fc8ff'), hx('bfeaff'), hx('5fd06a'), hx('3fb85a'), RED, YEL, WHITE, hx('ffd23f'))


def box(ctx, x, y, s, rot=0.0, upside=False):
    """the puzzle box (open, no lid), held at (x,y)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot + (math.pi if upside else 0)); ctx.scale(s, s)
    rect_r(ctx, -110, -60, 220, 120, 8); fl(ctx, hx('ffcf5a'), 5)
    ctx.save(); rect_r(ctx, -96, -48, 150, 96, 4); ctx.clip()
    ctx.translate(-96, -48); ctx.scale(150 / PW, 96 / PH); picture(ctx)
    ctx.restore()
    rect_r(ctx, -96, -48, 150, 96, 4); ink(ctx, 3); ctx.stroke()
    ctx.restore()
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    text(ctx, "1000", 82 if not upside else -82, 0, 30, WHITE, ow=6, ang=-1.57 if not upside else 1.57, shadow=False)
    ctx.restore()


def stamp(ctx, s, x, y, t, ang=-0.15, col=RED):
    if t <= 0:
        return
    sc = 1.6 - 0.6 * eout(min(1, t * 2))
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(sc, sc)
    rect_r(ctx, -190, -70, 380, 140, 16); setc(ctx, (1, 1, 1, 0.85)); ctx.fill_preserve()
    setc(ctx, col); ctx.set_line_width(12); ctx.stroke()
    text(ctx, s, 0, 0, 100, col, outline=WHITE, ow=8, shadow=False)
    ctx.restore()


# ------------------------------------------------------------------ the cat (original)
def cat(ctx, x, y, s, f=1, lf=0, mode='sit', eye='normal', rot=0.0, hiss=False):
    """mode sit/sleep: (x,y)=feet ; dangle: (x,y)=head centre ; leap: (x,y)=body centre"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(f * s, s)
    lw = 5
    if mode == 'sleep':
        ctx.new_path(); ctx.move_to(-80, -20); ctx.curve_to(-150, -10, -120, 30, -40, 10); ink(ctx, 26); ctx.stroke_preserve()
        setc(ctx, FUR); ctx.set_line_width(16); ctx.stroke()
        b = 1 + 0.03 * math.sin(lf * 0.15)
        ellipse(ctx, 0, -48, 100, 48 * b); fl(ctx, FUR, lw)
        for k in range(3):
            ctx.move_to(-40 + k * 30, -92 * b); ctx.line_to(-34 + k * 30, -70); setc(ctx, FURD); ctx.set_line_width(8); ctx.stroke()
        hx_, hy_ = 80, -78
    elif mode == 'sit':
        ctx.new_path(); ctx.move_to(-40, -10); ctx.curve_to(-110, -10, -110, -90, -80, -120 + 8 * math.sin(lf * 0.3)); ink(ctx, 26); ctx.stroke_preserve()
        setc(ctx, FUR); ctx.set_line_width(16); ctx.stroke()
        ellipse(ctx, 0, -70, 62, 72); fl(ctx, FUR, lw)
        ellipse(ctx, 10, -60, 30, 50); setc(ctx, FURL); ctx.fill()
        for px in (-22, 26):
            ellipse(ctx, px, -6, 22, 12); fl(ctx, FURL, 4)
        hx_, hy_ = 6, -160
    elif mode == 'dangle':
        sw = math.sin(lf * 0.4) * 0.15
        ctx.save(); ctx.rotate(sw)
        ctx.new_path(); ctx.move_to(0, 230); ctx.curve_to(10, 290, -20, 330, 0, 380); ink(ctx, 26); ctx.stroke_preserve()
        setc(ctx, FUR); ctx.set_line_width(16); ctx.stroke()
        for lx in (-24, 24):
            rect_r(ctx, lx - 14, 200, 28, 90, 12); fl(ctx, FUR, 4)
        ellipse(ctx, 0, 150, 52, 120); fl(ctx, FUR, lw)
        ellipse(ctx, 0, 160, 26, 80); setc(ctx, FURL); ctx.fill()
        for k in range(4):
            ctx.move_to(-50, 90 + k * 40); ctx.line_to(-30, 96 + k * 40); ctx.move_to(50, 90 + k * 40); ctx.line_to(30, 96 + k * 40)
        setc(ctx, FURD); ctx.set_line_width(7); ctx.stroke()
        ctx.restore()
        hx_, hy_ = 0, 0
    else:  # leap
        ctx.new_path(); ctx.move_to(-100, 0); ctx.curve_to(-170, -10, -200, -60, -230, -50); ink(ctx, 26); ctx.stroke_preserve()
        setc(ctx, FUR); ctx.set_line_width(16); ctx.stroke()
        for (a, b_) in (((-80, 10), (-150, 60)), ((70, 10), (150, 50))):
            ctx.new_path(); ctx.move_to(*a); ctx.line_to(*b_); ink(ctx, 34); ctx.stroke_preserve(); setc(ctx, FUR); ctx.set_line_width(22); ctx.stroke()
        ellipse(ctx, 0, 0, 120, 46); fl(ctx, FUR, lw)
        for k in range(3):
            ctx.move_to(-50 + k * 35, -44); ctx.line_to(-44 + k * 35, -20); setc(ctx, FURD); ctx.set_line_width(8); ctx.stroke()
        hx_, hy_ = 130, -40
    # head
    ctx.save(); ctx.translate(hx_, hy_)
    for sx in (-1, 1):
        poly(ctx, [(sx * 22, -36), (sx * 50, -74), (sx * 52, -18)]); fl(ctx, FUR, lw)
        poly(ctx, [(sx * 30, -36), (sx * 47, -60), (sx * 46, -30)]); setc(ctx, hx('ffb3c0')); ctx.fill()
    ellipse(ctx, 0, 0, 58, 50); fl(ctx, FUR, lw)
    for k in (-1, 0, 1):
        ctx.move_to(k * 14, -48); ctx.line_to(k * 12, -30); setc(ctx, FURD); ctx.set_line_width(7); ctx.stroke()
    if mode == 'sleep' or eye == 'closed':
        for sx in (-1, 1):
            ctx.new_path(); ctx.arc(sx * 22, -2, 10, 0.3, math.pi - 0.3); ink(ctx, 4); ctx.stroke()
    elif eye == 'glare':
        for sx in (-1, 1):
            ellipse(ctx, sx * 22, 0, 11, 11); setc(ctx, hx('a8e05a')); ctx.fill()
            ellipse(ctx, sx * 22, 0, 3, 9); setc(ctx, INK); ctx.fill()
            ctx.new_path(); ctx.move_to(sx * 36, -16); ctx.line_to(sx * 8, -6); ink(ctx, 6); ctx.stroke()
    else:
        for sx in (-1, 1):
            ellipse(ctx, sx * 22, -2, 13, 15); setc(ctx, INK); ctx.fill()
            ellipse(ctx, sx * 22 - 4, -7, 5, 5); setc(ctx, WHITE); ctx.fill()
    for sx in (-1, 1):
        ellipse(ctx, sx * 38, 16, 9, 5); setc(ctx, hx('ff9aa8')); ctx.fill()
        for dy in (-4, 6):
            ctx.move_to(sx * 30, 14 + dy); ctx.line_to(sx * 70, 8 + dy * 2)
        ink(ctx, 2); ctx.stroke()
    poly(ctx, [(-6, 10), (6, 10), (0, 17)]); setc(ctx, hx('ff7a90')); ctx.fill()
    if hiss:
        ellipse(ctx, 0, 30, 18, 14); fl(ctx, hx('8a2a3a'), 3)
        for sx in (-1, 1):
            poly(ctx, [(sx * 10, 18), (sx * 4, 18), (sx * 7, 28)]); setc(ctx, WHITE); ctx.fill()
    else:
        ctx.new_path(); ctx.arc(-6, 18, 6, 0.2, math.pi - 0.2); ctx.new_sub_path(); ctx.arc(6, 18, 6, 0.2, math.pi - 0.2); ink(ctx, 3); ctx.stroke()
    ctx.restore()
    ctx.restore()


# ------------------------------------------------------------------ set: sunny living room
def room(ctx, lf, cushions=True, mess=0.0):
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, hx('fff0c4')); ctx.fill()
    rnd = random.Random(103)
    for k in range(70):   # tiny heart/dot wallpaper
        x, y = rnd.uniform(200, 2200), rnd.uniform(500, 1520)
        ellipse(ctx, x, y, 6, 6); setc(ctx, hx('ffcf8a')); ctx.fill()
    # window with sun + clouds
    x, y, w, h = 700, 820, 250, 270
    rect_r(ctx, x - 14, y - 14, w + 28, h + 28, 14); fl(ctx, WHITE, 6)
    rect_r(ctx, x, y, w, h, 10); fl(ctx, hx('8fd8ff'), 4)
    ctx.save(); rect_r(ctx, x, y, w, h, 10); ctx.clip()
    ellipse(ctx, x + 70, y + 70, 36, 36); setc(ctx, hx('ffe066')); ctx.fill()
    for (cx_, cy_) in ((x + 170 + 10 * math.sin(lf * 0.02), y + 90), (x + 60, y + 190)):
        for dx, r in ((-24, 20), (0, 28), (24, 20)):
            ellipse(ctx, cx_ + dx, cy_, r, r * 0.8); setc(ctx, WHITE); ctx.fill()
    ellipse(ctx, x + 125, y + 330, 220, 90); setc(ctx, hx('7fd86a')); ctx.fill()
    ctx.restore()
    ctx.move_to(x + w / 2, y); ctx.line_to(x + w / 2, y + h); ctx.move_to(x, y + h / 2); ctx.line_to(x + w, y + h / 2)
    setc(ctx, WHITE); ctx.set_line_width(12); ctx.stroke()
    for sx in (-1, 1):   # curtains
        xx = x + w / 2 + sx * (w / 2 + 10)
        poly(ctx, [(xx - 30, y - 30), (xx + 30, y - 30), (xx + 24 * sx + 10, y + h + 30), (xx - 24 * sx - 10, y + h + 30)]); fl(ctx, hx('ff9ab8'), 4)
    rect_r(ctx, x - 70, y - 44, w + 140, 16, 8); fl(ctx, hx('c98a52'), 3)
    # framed picture + wall clock
    rect_r(ctx, 1100, 860, 170, 130, 8); fl(ctx, hx('ff8a5c'), 6)
    rect_r(ctx, 1118, 878, 134, 94, 4); fl(ctx, hx('bfe9ff'), 3)
    ellipse(ctx, 1185, 960, 60, 26); setc(ctx, hx('6fd37a')); ctx.fill()
    ellipse(ctx, 1220, 905, 14, 14); setc(ctx, YEL); ctx.fill()
    ellipse(ctx, 1380, 900, 46, 46); fl(ctx, WHITE, 5)
    ctx.move_to(1380, 900); ctx.line_to(1380, 872); ctx.move_to(1380, 900); ctx.line_to(1402, 908); ink(ctx, 5); ctx.stroke()
    # bookshelf + plant (right)
    rect_r(ctx, 1460, 1110, 200, 450, 10); fl(ctx, hx('c98a52'), 6)
    for j in range(3):
        yy = 1160 + j * 130
        rect_r(ctx, 1472, yy + 92, 176, 14, 4); fl(ctx, hx('a46a3a'), 3)
        for b in range(5):
            cols = (PINK, MINT, GOLD, BLUE, PURPLE)
            rect_r(ctx, 1482 + b * 32, yy + 20 + (b % 2) * 12, 26, 72 - (b % 2) * 12, 4); fl(ctx, cols[(b + j) % 5], 3)
    rect_r(ctx, 1525, 1050, 70, 60, 10); fl(ctx, hx('5aa8ff'), 4)
    for a in (-0.7, -0.2, 0.3, 0.8):
        ellipse(ctx, 1560 + 44 * math.sin(a), 1010 - 30 * math.cos(a), 14, 34, a); fl(ctx, GREEN, 3)
    # floor lamp (left)
    rect_r(ctx, 545, 1080, 12, 480, 4); fl(ctx, hx('8a5a3a'), 3)
    poly(ctx, [(495, 1080), (607, 1080), (585, 990), (517, 990)]); fl(ctx, hx('ffd36a'), 5)
    # floor + skirting + rug
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('e8b98a')); ctx.fill()
    for k in range(-20, 60):
        ctx.move_to(k * 140, FLOOR); ctx.line_to(k * 140 - 60, FLOOR + 600); setc(ctx, (0.7, 0.5, 0.35, 0.35)); ctx.set_line_width(4); ctx.stroke()
    rect_r(ctx, -3000, FLOOR - 24, 9000, 24, 4); fl(ctx, WHITE, 4)
    ellipse(ctx, 1110, 1640, 520, 78); fl(ctx, hx('b8a8ff'), 5)
    ellipse(ctx, 1110, 1640, 420, 56); setc(ctx, hx('d8ccff')); ctx.fill()
    ellipse(ctx, 1110, 1640, 300, 36); setc(ctx, hx('b8a8ff')); ctx.fill()
    # pet bed with toy mouse (right of the table)
    ellipse(ctx, 1560, 1600, 100, 34); fl(ctx, hx('ff8a8a'), 5)
    ellipse(ctx, 1560, 1592, 72, 20); setc(ctx, hx('ffd0d0')); ctx.fill()
    ellipse(ctx, 1600, 1585, 18, 10); fl(ctx, hx('b0b0c0'), 3)
    # sofa (left)
    sofa(ctx, cushions)
    if mess > 0:
        for (x_, y_, c, a) in ((640, 1590, MINT, 0.4), (1500, 1585, PINK, -0.3), (900, 1630, GOLD, 0.2)):
            rect_r(ctx, x_ - 70, y_ - 30, 140, 60, 20); ctx.save(); fl(ctx, c, 5); ctx.restore()


def sofa(ctx, cushions=True):
    rect_r(ctx, 610, 1250, 430, 200, 36); fl(ctx, hx('5aa8a0'), 6)           # back
    if cushions:
        for k, c in enumerate((MINT, PINK, GOLD)):
            rect_r(ctx, 640 + k * 130, 1290 + (k % 2) * 8, 120, 100, 26); fl(ctx, c, 5)
    rect_r(ctx, 600, 1400, 450, 110, 26); fl(ctx, hx('6ac0b8'), 6)           # seat
    for sx in (585, 1015):
        rect_r(ctx, sx, 1330, 60, 190, 26); fl(ctx, hx('5aa8a0'), 6)        # arms
    for lx in (630, 1010):
        rect_r(ctx, lx, 1505, 22, FLOOR - 1505 + 20, 6); fl(ctx, hx('8a5a3a'), 3)


def table(ctx, lf, hole=True, glow=0.0, done=0.0, puzzle_on=True):
    for lx in (TX - 200, TX + 176):
        rect_r(ctx, lx, TTOP + 80, 24, GND - TTOP - 80, 6); fl(ctx, hx('a46a3a'), 4)
    rect_r(ctx, TX - 240, TTOP, 480, 100, 14); fl(ctx, hx('c98a52'), 6)
    rect_r(ctx, TX - 240, TTOP + 76, 480, 30, 10); fl(ctx, hx('a46a3a'), 4)
    if puzzle_on:
        ctx.save(); ctx.translate(TX - 175, TTOP + 8); ctx.scale(350 / PW, 62 / PH)
        puzzle(ctx, lf, hole, glow, done)
        ctx.restore()


def hair_piece(ctx, d, k=1.0, s=None, rot=0.5):
    """the missing piece stuck in Dad's hair (drawn after Dad)"""
    hx_, hy_ = d['head']; R = d['R']
    piece(ctx, hx_ + 0.22 * R, hy_ - 0.98 * R, s if s else R / 190, rot, False)


def dad_kneel(ctx, lf, p, x=1290, k=1.12, f_=-1, hair=True):
    d = kneel(ctx, DAD, x, k, p, f_)
    if hair:
        hair_piece(ctx, d)
    return d


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = CZ + 0.04 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, CX, CY, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    room(ctx, lf)
    cat(ctx, 985, 1405, 0.45, -1, lf, 'sleep')
    sit(ctx, KID, 830, 0.9, P(eye='shock', mouth='open', lsh=20, lel=-120, rsh=30, rel=-130, head=-4, **SIT), 1, 1500)
    table(ctx, lf)
    w = math.sin(lf * 1.2)
    p = P(eye='shock', mouth='scream', lsh=165 + 8 * w, lel=-10, rsh=160 - 8 * w, rel=-20, head=-8 + 4 * w, torso=-4, **KNEEL)
    d = dad_kneel(ctx, lf, p)
    box(ctx, d['head'][0] + 10 * w, d['head'][1] - d['R'] * 1.3, 0.85, 0.1 * w, True)
    sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.4, lf, 0.9)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"WHERE'S THE", 540, 1400, 96, YEL, -0.04, t)
    label(ctx, "LAST PIECE?!\"", 540, 1500, 118, WHITE, 0.03, t)


# ------------------------------------------------------------------ shot 2: macro + empty box
def macro(ctx, f, lf, glow=0.0, hole=True, done=0.0, zoom=1.0, cx=PW / 2, cy=PH / 2):
    """top-down view of the puzzle on the wooden table"""
    ctx.save(); ctx.translate(540, 940); ctx.scale(1.5 * zoom, 1.5 * zoom); ctx.translate(-cx, -cy)
    ctx.rectangle(-2000, -2000, 5000, 5000); setc(ctx, hx('c98a52')); ctx.fill()
    for k in range(-30, 40):
        ctx.move_to(-2000, k * 46); ctx.curve_to(0, k * 46 + 10, 400, k * 46 - 10, 2600, k * 46 + 6)
    setc(ctx, (0.55, 0.35, 0.2, 0.35)); ctx.set_line_width(3); ctx.stroke()
    # spare mug + glasses on the table
    ellipse(ctx, -120, 380, 60, 60); fl(ctx, WHITE, 5); ellipse(ctx, -120, 380, 44, 44); setc(ctx, hx('7a4a2c')); ctx.fill()
    puzzle(ctx, lf, hole, glow, done)
    ctx.restore()


def beat1(ctx, f, il):
    # 0-46 macro: "999 PIECES DONE..." -> hole glows "ONE LEFT!" ; 46-140 medium: rustle, flip, shake, crumb, "...EMPTY?!"
    if il < 46:
        z = 1.0 + 0.25 * eio(pop(il, 18, 40))
        cx_ = lerp(PW / 2, (HOLE[0] + 0.5) * CW, eio(pop(il, 18, 40)))
        cy_ = lerp(PH / 2, (HOLE[1] + 0.5) * CW + 40, eio(pop(il, 18, 40)))
        ctx.save(); cam(ctx, 540, 960, 1, 0, 0, f)
        macro(ctx, f, il, glow=pop(il, 18, 24), zoom=z, cx=cx_, cy=cy_)
        ctx.restore()
        label(ctx, "999 PIECES DONE...", 540, 380, 84, WHITE, -0.03, pop(il, 2, 6))
        if il >= 22:
            label(ctx, "ONE LEFT!", 540, 1460, 130, YEL, 0.04, pop(il, 22, 25))
        return
    j = il - 46
    zz = 1.45 if j < 60 else lerp(1.45, 1.8, eout(pop(j, 60, 66)))
    ctx.save(); cam(ctx, lerp(1200, 1300, pop(j, 60, 66)), lerp(1300, 1200, pop(j, 60, 66)), zz, 0, shake_at(j, [60], 12, 20), f)
    room(ctx, il)
    cat(ctx, 985, 1405, 0.45, -1, il, 'sleep')
    sit(ctx, KID, 830, 0.9, P(eye='normal', mouth='smile', lsh=20, lel=-60, rsh=30, rel=-60, **SIT), 1, 1500)
    table(ctx, il, glow=0.5)
    if j < 26:   # rummage
        w = math.sin(j * 1.4)
        p = P(eye='happy', mouth='grin', lsh=60 + 10 * w, lel=-40, rsh=70 - 10 * w, rel=-50, head=6, **KNEEL)
        d = dad_kneel(ctx, il, p)
        box(ctx, d['front'][0] - 30, d['front'][1] + 20, 0.85, -0.05)
    elif j < 60:  # flip + shake
        w = math.sin(j * 2.2)
        p = P(eye='normal' if j < 44 else 'shock', mouth='open', lsh=150 + 10 * w, lel=-20, rsh=150 - 10 * w, rel=-20, head=-6, **KNEEL)
        d = dad_kneel(ctx, il, p)
        bx_ = d['head'][0]; by_ = d['head'][1] - d['R'] * 1.3
        box(ctx, bx_ + 12 * w, by_, 0.85, 0.12 * w, True)
        if j >= 44:   # a single crumb falls
            cyb = by_ + 80 + 600 * (pop(j, 44, 58) ** 2)
            ellipse(ctx, bx_, cyb, 5, 5); setc(ctx, hx('b9844a')); ctx.fill()
    else:
        p = P(eye='shock', mouth='scream', lsh=150, lel=-20, rsh=150, rel=-20, head=-10, **KNEEL)
        d = dad_kneel(ctx, il, p)
        bx_ = d['head'][0]; by_ = d['head'][1] - d['R'] * 1.3
        box(ctx, bx_, by_, 0.85, 0, True)
        sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.3, j, 0.9)
    ctx.restore()
    if j < 26:
        label(ctx, "*rustle rustle*", 540, 1430, 90, CYAN, -0.03, pop(j, 2, 5))
    elif j < 44:
        label(ctx, "*shake shake*", 540, 1430, 100, WHITE, 0.03, pop(j, 26, 29))
    elif j < 60:
        label(ctx, "*plink.*", 540, 1430, 90, CYAN, 0.03, pop(j, 52, 55))
    else:
        label(ctx, "\"...EMPTY?!\"", 540, 1450, 140, RED, -0.04, pop(j, 60, 63))


def s2(ctx, f):
    beat1(ctx, f, f - 60)


# ------------------------------------------------------------------ shot 3: search montage
def cushion(ctx, x, y, col, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    rect_r(ctx, -60, -50, 120, 100, 26); fl(ctx, col, 5)
    ctx.restore()


def magnifier(ctx, x, y, s, ang, inner=None):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s)
    rect_r(ctx, -12, 70, 24, 110, 10); fl(ctx, hx('a46a3a'), 4)
    ctx.new_path(); ctx.arc(0, 0, 80, 0, 7); setc(ctx, hx('dff6ff')[:3] + (0.55,)); ctx.fill_preserve()
    setc(ctx, INK); ctx.set_line_width(26); ctx.stroke_preserve(); setc(ctx, hx('ffc93c')); ctx.set_line_width(16); ctx.stroke()
    if inner:
        ctx.save(); ctx.arc(0, 0, 72, 0, 7); ctx.clip(); inner(ctx); ctx.restore()
    ellipse(ctx, -30, -30, 14, 24, 0.6); setc(ctx, (1, 1, 1, 0.7)); ctx.fill()
    ctx.restore()


def search(ctx, f, il):
    sub = 0 if il < 43 else (1 if il < 86 else 2)
    j = il - (0, 43, 86)[sub]
    tilt = (-6, 6, -5)[sub]
    hit = [0]
    if sub == 0:
        ctx.save(); cam(ctx, 830, 1330, 1.5, tilt, shake_at(j, [0, 30], 8, 12), f)
        room(ctx, il, cushions=False)
        cat(ctx, 985, 1405, 0.45, -1, il, 'sleep')
        w = math.sin(j * 1.6)
        p = P(eye='glare', mouth='scream', lsh=150 + 30 * w, lel=-20, rsh=-40 - 60 * w, rel=-60, torso=-10 + 8 * w, head=-6)
        for k, c in enumerate((MINT, PINK, GOLD, MINT)):
            u = ((j * 0.045 + k * 0.27) % 1.0)
            x_ = lerp(820, 560 + 560 * (k % 2), u); y_ = 1350 - 520 * math.sin(u * math.pi)
            cushion(ctx, x_, y_, c, u * 6 + k)
        d = stand(ctx, DAD, 860, 1.12, p, -1)
        hair_piece(ctx, d)
        ctx.restore()
        label(ctx, "THE SOFA?", 540, 1380, 110, WHITE, -0.04, pop(j, 2, 5))
        label(ctx, "*FWUMP! FWUMP!*", 540, 470, 80, CYAN, 0.03, pop(j, 4, 7))
        stamp(ctx, "NOPE!", 540, 1500, pop(j, 30, 34))
    elif sub == 1:
        ctx.save(); cam(ctx, 1110, 1380, 1.55, tilt, shake_at(j, [30], 8, 12), f)
        room(ctx, il, cushions=False, mess=1)
        cat(ctx, 985, 1405, 0.45, -1, il, 'sleep')
        sw = math.sin(j * 0.25)
        p = P(eye='glare', mouth='flat', lsh=100, lel=-20, rsh=110, rel=-10, torso=42, head=10, lhip=-30, rhip=-10, lkn=20, rkn=10)
        d = stand(ctx, DAD, 1060 + 40 * sw, 1.12, p, 1)
        hair_piece(ctx, d)
        mx, my = 1280 + 60 * sw, 1600
        def inner(c):
            c.scale(2.2, 2.2); c.translate(-mx / 1 + 0, -my)  # magnified rug pattern
            c.rectangle(mx - 200, my - 200, 400, 400); setc(c, hx('d8ccff')); c.fill()
            for k in range(-4, 5):
                c.move_to(mx - 200, my + k * 18); c.line_to(mx + 200, my + k * 18 + 6)
            setc(c, hx('b8a8ff')); c.set_line_width(5); c.stroke()
        magnifier(ctx, mx, my - 40, 1.0, -0.4, None)
        # a giant magnified eye inside the glass
        ellipse(ctx, mx, my - 40, 46, 34); setc(ctx, WHITE); ctx.fill_preserve(); ink(ctx, 4); ctx.stroke()
        ellipse(ctx, mx + 10 * sw, my - 38, 20, 22); setc(ctx, INK); ctx.fill()
        ellipse(ctx, mx + 10 * sw - 6, my - 46, 6, 6); setc(ctx, WHITE); ctx.fill()
        ctx.restore()
        label(ctx, "THE RUG?", 540, 1380, 110, WHITE, 0.04, pop(j, 2, 5))
        label(ctx, "*sniff sniff*", 540, 470, 80, CYAN, -0.03, pop(j, 6, 9))
        stamp(ctx, "NOPE!", 540, 1500, pop(j, 30, 34), 0.12)
    else:
        ctx.save(); cam(ctx, 1000, 1250, 1.45, tilt, shake_at(j, [18, 32], 10, 18), f)
        room(ctx, il, cushions=False, mess=1)
        p = P(eye='shock' if j >= 18 else 'normal', mouth='open' if j >= 18 else 'flat', lsh=100, lel=-10, rsh=95, rel=-10, head=-4, torso=-8)
        d = stand(ctx, DAD, 900, 1.12, p, 1)
        hair_piece(ctx, d)
        hxm = (d['front'][0] + d['back'][0]) / 2; hym = min(d['front'][1], d['back'][1])
        cat(ctx, hxm + 50, hym - 20, 0.75, 1, il, 'dangle', 'glare' if j >= 18 else 'closed', 0, hiss=j >= 18)
        if j >= 18:
            for k in range(3):
                a = -0.8 + k * 0.8
                ctx.move_to(hxm + 10 + 90 * math.cos(a - 1.57), hym - 50 + 90 * math.sin(a - 1.57))
                ctx.line_to(hxm + 10 + 130 * math.cos(a - 1.57), hym - 50 + 130 * math.sin(a - 1.57))
            ink(ctx, 6); ctx.stroke()
        ctx.restore()
        label(ctx, "THE CAT?", 540, 1380, 110, WHITE, -0.04, pop(j, 2, 5))
        if j >= 18:
            label(ctx, "*HISSSS!*", 540, 470, 110, RED, 0.04, pop(j, 18, 21))
        stamp(ctx, "NOPE!", 540, 1500, pop(j, 32, 36), -0.1)
    # speed lines on cut-in
    if j < 6:
        speed_lines(ctx, 540, 960, il, 0.5 * (1 - j / 6), 50, 500)


def s3(ctx, f):
    search(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: the one close-up
def closeup(ctx, f, il):
    z = 1 + 0.06 * eio(il / 90)
    ctx.save(); cam(ctx, 540, 960, z, 2 * math.sin(il * 0.2), shake_at(il, [40], 10, 18) + 2, f)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('ffe08a')), (1, hx('ff9a5a'))])); ctx.paint()
    rays(ctx, 540, 900, 150, 1400, il * 0.01, (1, 1, 1), 0.25, 18)
    w = math.sin(il * 1.2)
    p = P(eye='glare', mouth='flat' if il < 40 else 'scream', lsh=-20, lel=-100, rsh=120, rel=40, head=3 * w)
    face(ctx, DAD, p, 470, 900, 200)
    piece(ctx, 470 + 0.22 * 200, 900 - 0.98 * 200, 200 / 150, 0.5, False)
    magnifier(ctx, 760, 1080, 1.5, 0.5)
    ellipse(ctx, 760, 1080, 56, 42, 0.5); setc(ctx, WHITE); ctx.fill_preserve(); ink(ctx, 5); ctx.stroke()
    ellipse(ctx, 768, 1082, 24, 28); setc(ctx, INK); ctx.fill()
    ellipse(ctx, 760, 1072, 8, 8); setc(ctx, WHITE); ctx.fill()
    sweat(ctx, 470 - 230, 900 - 120, il, 1.4)
    if il >= 40:
        twitch(ctx, 470 + 190, 900 - 210, il, 1.5)
    ctx.restore()
    label(ctx, "\"It was RIGHT...\"", 540, 1370, 100, WHITE, -0.03, pop(il, 4, 8))
    if il >= 40:
        label(ctx, "\"...HERE!!\"", 540, 1520, 150, RED, 0.04, pop(il, 40, 43))


def s4(ctx, f):
    closeup(ctx, f, f - 330)


# ------------------------------------------------------------------ shot 5: twist -> click -> CRASH
def confetti(ctx, t, x0, y0, n=60, seed=3):
    rnd = random.Random(seed)
    for k in range(n):
        vx, vy = rnd.uniform(-700, 700), rnd.uniform(-1300, -500)
        x = x0 + vx * t; y = y0 + vy * t + 1400 * t * t
        ctx.save(); ctx.translate(x, y); ctx.rotate(k + t * 8)
        ctx.rectangle(-10, -5, 20, 10); setc(ctx, (RED, YEL, MINT, PINK, BLUE, GOLD)[k % 6]); ctx.fill(); ctx.restore()


def finale(ctx, f, il):
    # 0-44 kid "Dad... your HAIR." ; 30-62 push-in on hair + PLOT TWIST card ; 62-92 "FOUND IT!!" held high ;
    # 92-122 macro *CLICK!* *DING!* "DONE!!" confetti ; 122-150 medium cheer, cat wiggles ;
    # 150-162 cat leaps ; 162 *CRASH!!* ; 162-210 pieces rain, cat in the box, Dad "...from the TOP."
    if 92 <= il < 122:
        j = il - 92
        ctx.save(); cam(ctx, 540, 960, 1, 0, shake_at(j, [12], 8, 14), f)
        done = eout(pop(j, 12, 18))
        macro(ctx, f, il, glow=0 if j >= 12 else 0.6, hole=j < 12, done=done, zoom=1.15, cx=(HOLE[0] + 0.5) * CW - 40, cy=(HOLE[1] + 0.5) * CW + 60)
        if j < 12:   # hand lowers the piece in
            u = eio(pop(j, 0, 12))
            px_ = 540 + ((HOLE[0] + 0.5) * CW - ((HOLE[0] + 0.5) * CW - 40)) * 1.725
            py_ = 960 + ((HOLE[1] + 0.5) * CW - ((HOLE[1] + 0.5) * CW + 60)) * 1.725 - 20
            yy = lerp(py_ + 420, py_, u)
            ctx.new_path(); ctx.move_to(px_ + 40, yy + 60); ctx.line_to(px_ + 160, 2100)
            setc(ctx, INK); ctx.set_line_width(110); ctx.stroke()
            ctx.new_path(); ctx.move_to(px_ + 40, yy + 60); ctx.line_to(px_ + 160, 2100)
            setc(ctx, DAD['skin']); ctx.set_line_width(96); ctx.stroke()
            ctx.new_path(); ctx.move_to(px_ + 120, yy + 420); ctx.line_to(px_ + 190, 2100)
            setc(ctx, INK); ctx.set_line_width(136); ctx.stroke()
            ctx.new_path(); ctx.move_to(px_ + 120, yy + 420); ctx.line_to(px_ + 190, 2100)
            setc(ctx, DAD['shirt']); ctx.set_line_width(122); ctx.stroke()
            piece(ctx, px_, yy, 1.725, lerp(0.5, 0, u))
            ellipse(ctx, px_ + 30, yy + 40, 40, 30); fl(ctx, DAD['skin'], 4)
        else:
            rays(ctx, 540, 940, 300, 1400, j * 0.02, (1, 1, 0.7), 0.35 * done, 16)
            confetti(ctx, (j - 12) / 30, 540, 900)
        ctx.restore()
        if j >= 12:
            label(ctx, "*CLICK!*", 540, 420, 110, YEL, -0.04, pop(j, 12, 15))
            label(ctx, "\"DONE!!\"", 540, 1470, 160, GOLD, 0.04, pop(j, 14, 17))
        return
    # medium shots
    if il < 30:
        cx_, cy_, z = 1060, 1300, 1.2
    elif il < 62:
        u = eio(pop(il, 30, 42)); cx_, cy_, z = lerp(1060, 1265, u), lerp(1300, 1170, u), lerp(1.2, 2.6, u)
    elif il < 92:
        cx_, cy_, z = 1150, 1250, 1.5
    elif il < 162:
        cx_, cy_, z = 1060, 1300, 1.2
    else:
        u = eio(pop(il, 186, 200)); cx_, cy_, z = lerp(1060, 1210, u), lerp(1300, 1260, u), lerp(1.2, 1.7, u)
    ctx.save(); cam(ctx, cx_, cy_, z, 0, shake_at(il, [162], 16, 30), f)
    room(ctx, il, cushions=False, mess=1)
    done = 1.0 if il >= 122 else 0.0
    crashed = il >= 162
    table(ctx, il, hole=il < 92, done=done if not crashed else 0, puzzle_on=not crashed)
    # kid
    if il < 62:
        kp = P(eye='normal', mouth='open', lsh=20, lel=-20, rsh=110, rel=-10, head=-6)
        kd = stand(ctx, KID, 820, 0.9, kp, 1)
    elif il < 162:
        kp = P(eye='happy', mouth='open', lsh=-160, lel=0, rsh=160, rel=0) if il >= 122 else P(eye='happy', mouth='smile', lsh=20, lel=-20, rsh=30, rel=-20)
        kd = stand(ctx, KID, 820, 0.9, kp, 1, GND - (abs(math.sin(il * 0.4)) * 40 if il >= 122 else 0))
    else:
        kd = stand(ctx, KID, 820, 0.9, P(eye='shock', mouth='open', lsh=40, lel=-120, rsh=40, rel=-120), 1)
    # Dad
    hair = il < 62
    if il < 30:
        p = P(eye='normal', mouth='flat', lsh=20, lel=-20, rsh=30, rel=-20, head=4, **KNEEL)
    elif il < 62:
        p = P(eye='shock', mouth='open', lsh=20, lel=-20, rsh=130, rel=-120, head=-10, **KNEEL)
    elif il < 92:
        p = P(eye='happy', mouth='scream', lsh=-20, lel=-20, rsh=140, rel=0, head=-8, **KNEEL)
    elif il < 162:
        p = P(eye='happy', mouth='scream', lsh=-165, lel=0, rsh=165, rel=0, head=-6, **KNEEL)
    elif il < 186:
        p = P(eye='shock', mouth='scream', lsh=-160, lel=0, rsh=160, rel=0, head=0, **KNEEL)
    else:
        p = P(eye='closed', mouth='flat', lsh=-10, lel=-10, rsh=10, rel=-10, head=6, **KNEEL)
    d = dad_kneel(ctx, il, p, hair=hair)
    if 62 <= il < 92:
        px_, py_ = d['head'][0] - d['R'] * 1.6, d['head'][1] - d['R'] * 0.7
        piece(ctx, px_, py_, 1.0, 0.3 * math.sin(il * 0.3))
        for k in range(5):
            a = k * 1.25 + il * 0.2
            sparkle(ctx, px_ + 90 * math.cos(a), py_ + 90 * math.sin(a), 16, YEL)
    if 30 <= il < 62:
        hx_, hy_ = d['head'][0] + 0.22 * d['R'], d['head'][1] - 0.98 * d['R']
        for k in range(4):
            a = k * 1.57 + il * 0.15
            sparkle(ctx, hx_ + 70 * math.cos(a), hy_ + 70 * math.sin(a), 12, YEL)
    # the cat
    if il < 150:
        wig = math.sin(il * 1.5) * 0.12 if il >= 128 else 0
        cat(ctx, 985, 1405, 0.45, 1, il, 'sit', 'glare' if il >= 128 else 'normal', wig)
    elif il < 162:
        u = pop(il, 150, 162)
        x_ = lerp(985, TX, u); y_ = lerp(1330, TTOP - 20, u) - 260 * math.sin(u * math.pi)
        cat(ctx, x_, y_, 0.5, 1, il, 'leap', 'glare', -0.4 + 0.6 * u)
    else:
        # pieces rain down
        rnd = random.Random(7)
        t = (il - 162) / 30
        for k in range(70):
            vx, vy = rnd.uniform(-900, 900), rnd.uniform(-1500, -500)
            x = TX + vx * t; y = TTOP + vy * t + 1700 * t * t
            y = min(y, GND + rnd.uniform(-20, 40))
            bit(ctx, x, y, 0.45, k + t * 6 * (y < GND), BITCOL[k % len(BITCOL)])
        # cat in the empty box on the table
        box(ctx, TX + 40, TTOP - 30, 0.85, 0)
        cat(ctx, TX + 40, TTOP - 50, 0.42, 1, il, 'sit', 'normal')
        if il >= 186:   # pieces on Dad's head
            for k in range(5):
                bit(ctx, d['head'][0] - 60 + k * 30, d['head'][1] - d['R'] * 0.95 - (k % 2) * 14, 0.35, k, BITCOL[k])
    if 122 <= il < 150:
        confetti(ctx, (il - 110) / 30, TX, TTOP - 200, 40, 9)
    ctx.restore()
    if 34 <= il < 62:
        card(ctx, 'p2', il, 34, 62)
    if il < 30:
        label(ctx, "*tap tap*", 540, 470, 80, CYAN, 0.03, pop(il, 1, 4))
        label(ctx, "\"Dad... your", 540, 1400, 100, MINT, -0.03, pop(il, 6, 10))
        label(ctx, "HAIR.\"", 540, 1500, 130, MINT, 0.03, pop(il, 14, 17))
    elif 62 <= il < 92:
        label(ctx, "\"FOUND IT!!\"", 540, 1450, 140, YEL, -0.04, pop(il, 63, 66))
    elif 122 <= il < 150:
        label(ctx, "\"YESSS!!\"", 540, 1450, 140, YEL, 0.04, pop(il, 123, 126))
        if il >= 136:
            label(ctx, "*wiggle wiggle*", 540, 470, 80, ORANGE, -0.03, pop(il, 136, 139))
    elif 150 <= il < 162:
        label(ctx, "*MEOW!*", 540, 470, 110, ORANGE, 0.04, pop(il, 150, 153))
    elif 162 <= il < 186:
        label(ctx, "*CRASH!!*", 540, 470, 150, RED, -0.05, pop(il, 162, 165))
    elif il >= 186:
        label(ctx, "\"...from the", 540, 1400, 100, WHITE, -0.03, pop(il, 188, 192))
        label(ctx, "TOP.\"", 540, 1500, 150, YEL, 0.03, pop(il, 194, 197))


def s5(ctx, f):
    lf = f - 420
    if lf < 210:
        finale(ctx, f, lf)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (200, s3), (330, s4), (420, s5)]
CUTS = (60, 106, 200, 243, 286, 330, 420, 512, 542, 630)


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
                              "-i", "out/puzzle_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
