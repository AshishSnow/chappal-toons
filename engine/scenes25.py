"""'Grandma Says You Look Thin' - original, general-audience comedy short, ~22s.
ECU: kid with stuffed hamster cheeks, Grandma's arm slides in ANOTHER plate: "YOU LOOK SO THIN!"
Split screen: what Grandma sees (shivering stick kid) vs reality (round kid, 3 plates in).
Food avalanche: plates fly in faster and faster, a tower grows, the kid's belly grows with it.
Dessert: giant cake, one bite -> jeans button pops and flies INTO the camera lens (crack).
Twist: leaving, Grandma hands "a little snack" - camera pulls out: the bag is the size of a house,
it tips over and flattens him. Loops back to the opening ECU."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, label, shake_at
import scenes13
from scenes13 import card as _card13
import random

BOY = doodle.BOY
GRAN = dict(skin=hx('f2c7a5'), hair=hx('e2e2ec'), hairstyle='mom', shirt=hx('ff7aa8'), pants=hx('7a5ab0'), shoes=hx('8a5a3a'),
            earring=True, sindoor=False, sleeve=1.0, glasses=hx('8a3cff'))
N = 660
FLOOR = 1430
KB = 1.45

CAPS = {
    'p1': [[("ME AT ", OUT), ("GRANDMA'S", hx('ff4fa0')), (" HOUSE:", OUT)]],
    'p2': [[("WHAT ", OUT), ("SHE SEES", hx('1f8bff')), (" VS ", OUT), ("REALITY", hx('ff3b5c'))]],
    'p3': [[("\"NO THANKS\"", hx('ff3b5c')), (" MEANS", OUT)], [("\"MORE PLEASE\"", hx('2fbf5a'))]],
    'p4': [[("AND THEN... ", OUT), ("DESSERT", hx('ff4fa0'))]],
    'p5': [[("PLOT TWIST: ", OUT)], [("THE ", OUT), ("GOODBYE SNACK", hx('8a3cff'))]],
}
scenes13.CAPS = CAPS
card = _card13

WALL, WALL2 = hx('ffe3c2'), hx('ffc9a0')


def cam(ctx, cx, cy, z, rot=0, shake=0, f=0, sx=W / 2, sy=H / 2):
    rnd = random.Random(f * 31 + 7)
    dx, dy = (rnd.uniform(-1, 1) * shake, rnd.uniform(-1, 1) * shake) if shake else (0, 0)
    ctx.translate(sx + dx, sy + dy); ctx.rotate(math.radians(rot)); ctx.scale(z, z); ctx.translate(-cx, -cy)


def rect_r(ctx, x, y, w, h, r):
    ctx.new_path(); ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); ctx.close_path()


def rays(ctx, x, y, r0, r1, t, col=(1, 0.97, 0.6), a=0.8, n=12):
    for k in range(n):
        ang = k * 2 * math.pi / n + t
        ctx.move_to(x + math.cos(ang) * r0, y + math.sin(ang) * r0)
        ctx.line_to(x + math.cos(ang - 0.09) * r1, y + math.sin(ang - 0.09) * r1)
        ctx.line_to(x + math.cos(ang + 0.09) * r1, y + math.sin(ang + 0.09) * r1); ctx.close_path()
    setc(ctx, col + (a,)); ctx.fill()


def heart(ctx, x, y, s, col=hx('ff3b6b')):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, 30); ctx.curve_to(-60, -10, -30, -55, 0, -25); ctx.curve_to(30, -55, 60, -10, 0, 30); ctx.close_path()
    fl(ctx, col, 4 / max(s, 0.3)); ctx.restore()


# ------------------------------------------------------------------ food
def plate(ctx, x, y, s=1.0, kind='pasta'):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 150, 34); fl(ctx, (1, 1, 1), 6)
    ellipse(ctx, 0, -4, 100, 20); setc(ctx, hx('e8eef8')); ctx.fill()
    if kind == 'pasta':
        ellipse(ctx, 0, -30, 95, 40); fl(ctx, hx('ffd86b'), 6)
        ink(ctx, 4)
        for k in range(5):
            ctx.new_path(); ctx.move_to(-70 + k * 30, -20); ctx.curve_to(-50 + k * 30, -60, -30 + k * 30, -10, -10 + k * 30, -45); ctx.stroke()
        ellipse(ctx, 0, -52, 50, 20); fl(ctx, hx('e0322a'), 5)
        for mx in (-28, 22):
            ellipse(ctx, mx, -60, 18, 16); fl(ctx, hx('8a4a2a'), 4)
    elif kind == 'pancakes':
        for k in range(4):
            ellipse(ctx, 0, -14 - k * 22, 100, 24); fl(ctx, hx('e8a85a'), 5)
        ctx.rectangle(-22, -100, 44, 26); fl(ctx, hx('fff1a0'), 4)
        ctx.move_to(-70, -84); ctx.curve_to(-80, -40, -90, -30, -86, -10); ink(ctx, 4); setc(ctx, hx('a8501a')); ctx.set_line_width(12); ctx.stroke()
    elif kind == 'dumplings':
        for k, (dx, dy) in enumerate(((-60, -18), (0, -22), (60, -18), (-30, -50), (30, -50))):
            ctx.new_path(); ctx.arc(dx, dy, 32, math.pi, 2 * math.pi); ctx.close_path(); fl(ctx, hx('fff6e8'), 5)
            ink(ctx, 3); ctx.new_path(); ctx.move_to(dx - 14, dy - 22); ctx.line_to(dx - 8, dy - 30); ctx.move_to(dx + 4, dy - 24); ctx.line_to(dx + 10, dy - 32); ctx.stroke()
    elif kind == 'drumstick':
        for dx, a in ((-40, -0.4), (40, 0.5)):
            ctx.save(); ctx.translate(dx, -36); ctx.rotate(a)
            ctx.rectangle(-8, -80, 16, 50); fl(ctx, (1, 1, 1), 4)
            ellipse(ctx, -10, -84, 12, 12); fl(ctx, (1, 1, 1), 4); ellipse(ctx, 10, -84, 12, 12); fl(ctx, (1, 1, 1), 4)
            ellipse(ctx, 0, 0, 44, 52); fl(ctx, hx('c8702a'), 5)
            ctx.restore()
    elif kind == 'pie':
        poly(ctx, [(-90, -14), (90, -14), (60, -64), (-60, -64)]); fl(ctx, hx('f0b860'), 5)
        ctx.rectangle(-60, -74, 120, 14); fl(ctx, hx('c8402a'), 4)
    elif kind == 'salad':
        for k, (dx, dy, c) in enumerate(((-50, -24, '3fbf4a'), (20, -30, '2f9f3a'), (60, -20, '5fd85a'), (-10, -50, '3fbf4a'))):
            ellipse(ctx, dx, dy, 44, 30); fl(ctx, hx(c), 4)
        ellipse(ctx, 40, -50, 16, 16); fl(ctx, hx('ff3b3b'), 4)
    ctx.restore()


FOODS = ['pasta', 'pancakes', 'dumplings', 'drumstick', 'pie', 'salad']


def cake(ctx, x, y, s=1.0, sliced=False):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 280, 50); fl(ctx, hx('e8eef8'), 7)
    for k, (w, h, c) in enumerate(((240, 150, 'ff8fb8'), (180, 130, 'fff4f0'), (120, 110, 'ff8fb8'))):
        y0 = -sum(hh for _, hh, _ in ((240, 150, 0), (180, 130, 0), (120, 110, 0))[:k]) - 10
        ctx.rectangle(-w, y0 - h, 2 * w, h); fl(ctx, hx(c), 7)
        ctx.new_path(); ctx.move_to(-w, y0 - h)
        for j in range(8):
            xx = -w + (j + 0.5) * 2 * w / 8
            ctx.line_to(xx, y0 - h + 34 + 14 * (j % 2)); ctx.line_to(-w + (j + 1) * 2 * w / 8, y0 - h)
        ctx.close_path(); fl(ctx, hx('fffaf6') if c != 'fff4f0' else hx('ff8fb8'), 5)
    top = -10 - 150 - 130 - 110
    ellipse(ctx, 0, top - 26, 30, 30); fl(ctx, hx('e0123a'), 6)
    ctx.move_to(6, top - 54); ctx.curve_to(16, top - 90, 40, top - 100, 50, top - 96); ink(ctx, 6); ctx.stroke()
    ctx.restore()


def pot(ctx, x, y, s=1.0, t=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for k in range(3):
        xx = -50 + k * 50 + 10 * math.sin(t * 0.2 + k)
        ctx.move_to(xx, -150); ctx.curve_to(xx + 30, -200, xx - 30, -240, xx + 10, -290)
        setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.rectangle(-150, -130, 300, 140); fl(ctx, hx('ff5a3a'), 7)
    ellipse(ctx, 0, -130, 150, 30); fl(ctx, hx('ffcf5a'), 6)
    for sx in (-1, 1):
        ctx.rectangle(sx * 150 - (30 if sx > 0 else 0) + (0 if sx > 0 else -30) + 30 * (sx > 0), -100, 30, 22); fl(ctx, hx('c8402a'), 5)
    ctx.restore()


def sack(ctx, x, y, w, h, a=0.0, piv=None):
    """giant goodie bag, bottom-centre at (x, y)"""
    ctx.save()
    if piv:
        ctx.translate(*piv); ctx.rotate(a); ctx.translate(-piv[0], -piv[1])
    # stuff poking out the top
    ctx.save(); ctx.translate(x - w * 0.18, y - h + 40); ctx.rotate(-0.3)
    rect_r(ctx, -40, -260, 80, 300, 40); fl(ctx, hx('e8b060'), 9)
    for k in range(3):
        ctx.move_to(-24, -200 + k * 70); ctx.line_to(24, -230 + k * 70); ink(ctx, 6); ctx.stroke()
    ctx.restore()
    ellipse(ctx, x + w * 0.12, y - h + 10, 90, 90); fl(ctx, hx('ff3b3b'), 9)
    ctx.move_to(x + w * 0.12, y - h - 80); ctx.line_to(x + w * 0.16, y - h - 120); ink(ctx, 9); ctx.stroke()
    ctx.save(); ctx.translate(x + w * 0.3, y - h + 20); ctx.rotate(0.25)
    ctx.rectangle(-55, -150, 110, 170); fl(ctx, hx('ffe8a0'), 9)
    ctx.rectangle(-60, -170, 120, 40); fl(ctx, hx('ff8a1f'), 8)
    ctx.restore()
    # bag body
    ctx.new_path(); ctx.move_to(x - w * 0.42, y - h); ctx.curve_to(x - w * 0.62, y - h * 0.5, x - w * 0.6, y - h * 0.05, x - w * 0.45, y)
    ctx.line_to(x + w * 0.45, y); ctx.curve_to(x + w * 0.6, y - h * 0.05, x + w * 0.62, y - h * 0.5, x + w * 0.42, y - h); ctx.close_path()
    fl(ctx, hx('c98a52'), 12)
    for k in range(4):
        ctx.move_to(x - w * 0.4 + k * w * 0.27, y - h + 60); ctx.curve_to(x - w * 0.3 + k * w * 0.27, y - h * 0.6, x - w * 0.42 + k * w * 0.27, y - h * 0.3, x - w * 0.36 + k * w * 0.27, y - 40)
        setc(ctx, (0, 0, 0, 0.12)); ctx.set_line_width(10); ctx.stroke()
    heart(ctx, x, y - h * 0.45, 3.2)
    # small handle loop at top-left
    ctx.new_path(); ctx.arc(x - w * 0.42, y - h - 20, 50, math.pi, 2 * math.pi); ink(ctx, 12); ctx.stroke()
    ctx.restore()


# ------------------------------------------------------------------ sets
def dining(ctx, t=0):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, WALL); ctx.fill()
    for i in range(-20, 30):
        for j in range(-16, 14):
            x, y = i * 140 + (j % 2) * 70, j * 140
            for k in range(5):
                a_ = k * 2 * math.pi / 5
                ellipse(ctx, x + math.cos(a_) * 12, y + math.sin(a_) * 12, 9, 9)
            setc(ctx, WALL2); ctx.fill()
    # window with curtains
    rect_r(ctx, 600, 470, 340, 300, 14); fl(ctx, hx('bfe8ff'), 9)
    ctx.move_to(770, 470); ctx.line_to(770, 770); ctx.move_to(600, 620); ctx.line_to(940, 620); ink(ctx, 7); ctx.stroke()
    for sx in (580, 880):
        ctx.new_path(); ctx.move_to(sx, 450); ctx.line_to(sx + 80, 450); ctx.curve_to(sx + 60, 600, sx + 90, 700, sx + 70, 800); ctx.line_to(sx, 800); ctx.close_path()
        fl(ctx, hx('ff8fb8'), 7)
    # picture frame with a heart
    rect_r(ctx, 130, 520, 220, 180, 10); fl(ctx, hx('c98a52'), 9)
    ctx.rectangle(160, 550, 160, 120); fl(ctx, hx('fff6e8'), 5)
    heart(ctx, 240, 615, 0.9)
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('b97a4a')); ctx.fill()
    for i in range(-30, 40):
        ctx.move_to(i * 110, FLOOR); ctx.line_to(i * 110 - 60, FLOOR + 1500); setc(ctx, (0, 0, 0, 0.1)); ctx.set_line_width(6); ctx.stroke()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()


def table(ctx, x0, x1, y, depth=600):
    ctx.rectangle(x0, y, x1 - x0, depth); fl(ctx, (1, 1, 1), 9)
    ctx.save(); ctx.rectangle(x0, y, x1 - x0, depth); ctx.clip()
    for i in range(int((x1 - x0) / 60) + 2):
        ctx.rectangle(x0 + i * 60, y, 30, depth); setc(ctx, hx('ff5a6a', 0.55) if False else (1, 0.35, 0.42, 0.55)); ctx.fill()
    for j in range(int(depth / 60) + 1):
        ctx.rectangle(x0, y + 10 + j * 60, x1 - x0, 30); setc(ctx, (1, 0.35, 0.42, 0.45)); ctx.fill()
    ctx.restore()
    ctx.rectangle(x0, y, x1 - x0, depth); ink(ctx, 9); ctx.stroke()
    ctx.move_to(x0, y); ctx.line_to(x1, y); ink(ctx, 10); ctx.stroke()


def porch(ctx):
    ctx.rectangle(-4000, -4000, 9000, 9000); setc(ctx, hx('9fdcff')); ctx.fill()
    for cx_, cy_ in ((-300, -200), (900, -500), (1500, 100)):
        for dx, r in ((-80, 90), (0, 130), (90, 100)):
            ellipse(ctx, cx_ + dx, cy_, r, r * 0.8)
        setc(ctx, (1, 1, 1)); ctx.fill()
    # house wall
    ctx.rectangle(-1400, 200, 1900, FLOOR - 200); fl(ctx, hx('ffd0a0'), 10)
    for j in range(16):
        ctx.move_to(-1400, 260 + j * 80); ctx.line_to(500, 260 + j * 80); setc(ctx, (0, 0, 0, 0.07)); ctx.set_line_width(6); ctx.stroke()
    poly(ctx, [(-1500, 220), (-450, -400), (600, 220)]); fl(ctx, hx('e0503a'), 10)
    # door
    rect_r(ctx, -200, 760, 320, FLOOR - 760, 12); fl(ctx, hx('2f8a6a'), 10)
    ctx.new_path(); ctx.arc(-40, 900, 70, 0, 2 * math.pi); setc(ctx, INK); ctx.set_line_width(26); ctx.stroke()
    ctx.new_path(); ctx.arc(-40, 900, 70, 0, 2 * math.pi); setc(ctx, hx('3fbf4a')); ctx.set_line_width(18); ctx.stroke()
    ellipse(ctx, 80, 1110, 16, 16); fl(ctx, hx('ffd23f'), 5)
    # flower pots
    for px in (-420, 260):
        poly(ctx, [(px - 60, FLOOR - 120), (px + 60, FLOOR - 120), (px + 44, FLOOR), (px - 44, FLOOR)]); fl(ctx, hx('d0703a'), 7)
        for k in range(3):
            ellipse(ctx, px - 40 + k * 40, FLOOR - 170 - 20 * (k % 2), 28, 28); fl(ctx, (hx('ff4fa0'), hx('ffd23f'), hx('8a3cff'))[k], 5)
    ctx.rectangle(-4000, FLOOR, 9000, 1600); setc(ctx, hx('7ac85a')); ctx.fill()
    ctx.rectangle(-300, FLOOR, 520, 1600); setc(ctx, hx('d8d0c0')); ctx.fill()
    ctx.move_to(-4000, FLOOR); ctx.line_to(5000, FLOOR); ink(ctx, 8); ctx.stroke()


# ------------------------------------------------------------------ characters
_SCR = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4))


def probe(x, hipy, k, f_, ch, p):
    return draw_hip(_SCR, x, hipy, k, f_, ch, p)


def belly(ctx, x, hipy, k, g, f_=1, btn=True):
    """round tummy over the torso; g=0 normal-ish, 1 = very round"""
    if g <= 0:
        return
    rx, ry = 70 * k * (1 + 1.25 * g), 62 * k * (1 + 1.0 * g)
    cy = hipy - 52 * k - ry * 0.25
    cx = x + f_ * 12 * k * g
    ellipse(ctx, cx, cy, rx, ry); fl(ctx, BOY['shirt'], 3.7 * k * 1.35)
    ctx.new_path(); ctx.arc(cx, cy + ry * 0.2, rx * 0.55, 0.25 * math.pi, 0.75 * math.pi); ink(ctx, 4 * k); ctx.stroke()
    # jeans waistband + button
    ctx.save(); ellipse(ctx, cx, cy, rx, ry); ctx.clip()
    ctx.rectangle(cx - rx, cy + ry * 0.72, 2 * rx, ry); fl(ctx, BOY['pants'], 4 * k)
    ctx.restore()
    ellipse(ctx, cx, cy, rx, ry); ink(ctx, 3.7 * k * 1.35); ctx.stroke()
    if btn:
        ellipse(ctx, cx + f_ * rx * 0.1, cy + ry * 0.82, 13 * k, 13 * k); fl(ctx, hx('ffd23f'), 4 * k)
    return (cx + f_ * rx * 0.1, cy + ry * 0.82)


def chubby_boy(ctx, x, hipy, k, f_, p, g, btn=True, cheeks=0.0):
    b = draw_hip(ctx, x, hipy, k, f_, BOY, p)
    bp = belly(ctx, x, hipy, k, g, f_, btn)
    hd, R = b['head'], b['R']
    if g > 0:
        # redraw the head on top of the tummy
        ctx.save(); ctx.new_path(); ctx.arc(hd[0], hd[1] - R * 0.4, R * 1.28, 0, 2 * math.pi); ctx.clip()
        draw_hip(ctx, x, hipy, k, f_, BOY, p)
        ctx.restore()
    if cheeks > 0:
        for sx in (-1, 1):
            ellipse(ctx, hd[0] + sx * R * 0.78, hd[1] + R * 0.32, R * 0.3 * cheeks, R * 0.26 * cheeks); fl(ctx, BOY['skin'], 3.7 * k * 1.35)
            ellipse(ctx, hd[0] + sx * R * 0.8, hd[1] + R * 0.34, R * 0.14, R * 0.08); setc(ctx, (1, 0.55, 0.6, 0.6)); ctx.fill()
    b['btn'] = bp
    return b


def stick_kid(ctx, x, ground, t):
    """what Grandma sees: a shivering skin-and-bones kid"""
    sh = 5 * math.sin(t * 2.7)
    x += sh
    lw = 6
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for dx in (-18, 18):
        ctx.move_to(x + dx, ground - 230); ctx.line_to(x + dx * 1.4, ground - 10); setc(ctx, INK); ctx.set_line_width(24); ctx.stroke_preserve()
        setc(ctx, BOY['pants']); ctx.set_line_width(12); ctx.stroke()
        ellipse(ctx, x + dx * 1.4 + 10, ground - 6, 26, 13); fl(ctx, BOY['shoes'], 5)
    rect_r(ctx, x - 38, ground - 470, 76, 250, 26); fl(ctx, BOY['shirt'], lw)
    for k in range(4):
        ctx.new_path(); ctx.arc(x, ground - 420 + k * 34, 26, 0.15 * math.pi, 0.85 * math.pi); ink(ctx, 4); ctx.stroke()
    for sx in (-1, 1):
        ctx.move_to(x + sx * 36, ground - 450); ctx.line_to(x + sx * 70, ground - 360); ctx.line_to(x + sx * 20, ground - 330)
        setc(ctx, INK); ctx.set_line_width(22); ctx.stroke_preserve(); setc(ctx, BOY['skin']); ctx.set_line_width(10); ctx.stroke()
    R = 120
    ctx.save(); ctx.translate(x, ground - 470 - R * 0.75)
    doodle.head(ctx, R, BOY, P(eye='shock', mouth='wavy'), 1, lw)
    ctx.restore()
    # cold wind
    for k in range(3):
        yy = ground - 600 + k * 120
        ctx.new_path(); ctx.move_to(x - 230, yy); ctx.curve_to(x - 170, yy - 30, x - 130, yy + 30, x - 90 - 10 * math.sin(t * 0.4 + k), yy)
        setc(ctx, (1, 1, 1, 0.9)); ctx.set_line_width(8); ctx.stroke()


def gran_arm(ctx, x0, y0, x1, y1, w=60):
    ctx.new_path(); ctx.move_to(x0, y0); ctx.line_to(x1, y1); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    setc(ctx, INK); ctx.set_line_width(w + 14); ctx.stroke_preserve(); setc(ctx, GRAN['shirt']); ctx.set_line_width(w); ctx.stroke()
    ellipse(ctx, x1, y1, w * 0.62, w * 0.62); fl(ctx, GRAN['skin'], 7)


def fork(ctx, x, y, a, s=1.0, food=True):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.rectangle(-9, -10, 18, 190); fl(ctx, hx('c8d0e0'), 5)
    ctx.rectangle(-30, -70, 60, 64); fl(ctx, hx('c8d0e0'), 5)
    for dx in (-15, 0, 15):
        ctx.move_to(dx, -70); ctx.line_to(dx, -120); ink(ctx, 10); ctx.stroke()
    if food:
        ellipse(ctx, 0, -110, 32, 30); fl(ctx, hx('8a4a2a'), 5)
    ctx.restore()


# ------------------------------------------------------------------ shots
def opening_face(ctx, f, lf, loop=False):
    pb = P(rsh=40, rel=-110, lsh=25, lel=20, eye='shock', mouth='wavy', torso=-4, head=4)
    pr = probe(540, 1300, KB, 1, BOY, pb)
    hd, R = pr['head'], pr['R']
    ctx.save()
    cam(ctx, hd[0], hd[1] + 40, 1.9, 2 * math.sin(lf * 0.2), shake_at(lf, [0, 26], 8, 12) + 2, f, sy=880)
    dining(ctx)
    rays(ctx, hd[0], hd[1], R * 1.2, 1600, lf * 0.02, col=(1, 1, 1), a=0.22, n=16)
    b = chubby_boy(ctx, 540, 1300, KB, 1, pb, 0.6, cheeks=1.0 + 0.06 * math.sin(lf * 0.9))
    for j, (dx, ph) in enumerate(((-1.25, 0), (1.3, 9))):
        tt = ((lf + ph) % 22) / 22
        sweat(ctx, hd[0] + dx * R, hd[1] - R * 0.4 + tt * R * 0.9, 1.4)
    fork(ctx, b['front'][0], b['front'][1], 0.15, 1.0)
    ty = hd[1] + R * 1.5
    table(ctx, -400, 1500, ty)
    plate(ctx, 450, ty + 40, 1.0, 'pasta')
    # Grandma's arm sliding ANOTHER plate in
    u = eout(pop(lf, 4, 18)) if not loop else 1.0
    px = lerp(-300, 330, u)
    plate(ctx, px - 40, ty + 100, 0.9, 'pancakes')
    gran_arm(ctx, px - 500, ty + 260, px - 150, ty + 110)
    ctx.restore()
    label(ctx, "\"YOU LOOK SO THIN!\"", 540, 1440, 80, (1, 1, 1), -0.04, 1 if lf >= 0 else 0)


def s1(ctx, f):
    if f < 64:
        opening_face(ctx, f, f)
    else:
        lf = f - 64
        # Grandma low-angle, beaming with a steaming pot
        ctx.save(); cam(ctx, 540, 1000, lerp(1.05, 1.18, lf / 56), -3, shake_at(lf, [0], 8, 12), f)
        dining(ctx)
        rays(ctx, 540, 700, 140, 1600, lf * 0.03, col=(1, 0.85, 0.9), a=0.5, n=18)
        g = draw_hip(ctx, 540, FLOOR - 92 * 1.6, 1.6, 1, GRAN, P(rsh=60, rel=-80, lsh=50, lel=-80, eye='happy', mouth='grin', head=-4 + 3 * math.sin(lf * 0.4)))
        pot(ctx, 540, g['front'][1] + 60, 1.0, lf)
        for k in range(3):
            tt = ((lf * 0.025) + k / 3) % 1
            heart(ctx, 300 + k * 240, 700 - 300 * tt, 0.8 * (1 - tt) + 0.2)
        ctx.restore()
        label(ctx, "\"EAT, EAT!\"", 540, 1440, 130, hx('ffe14d'), 0.04, pop(lf, 2, 6))
    card(ctx, 'p1', f, -6, 118)


def s2(ctx, f):
    lf = f - 120
    ctx.rectangle(0, 0, W, H); setc(ctx, INK); ctx.fill()
    # LEFT: what Grandma sees
    sl = eout(pop(lf, 0, 10))
    ctx.save(); ctx.translate(lerp(-540, 0, sl), 0)
    ctx.rectangle(0, 0, 534, H); ctx.clip()
    ctx.rectangle(0, 0, 540, H); setc(ctx, hx('a8c8f0')); ctx.fill()
    for i in range(12):
        for j in range(16):
            sparkle(ctx, 20 + i * 50 + (j % 2) * 25, 20 + j * 130, 8, (1, 1, 1))
    ctx.rectangle(0, 1330, 540, 600); setc(ctx, hx('7a90b8')); ctx.fill()
    ctx.move_to(0, 1330); ctx.line_to(540, 1330); ink(ctx, 7); ctx.stroke()
    stick_kid(ctx, 280, 1330, lf)
    plate(ctx, 150, 1300, 0.55, 'empty')
    ellipse(ctx, 150, 1288, 10, 10); fl(ctx, hx('3fbf4a'), 3)
    text(ctx, "GRANDMA SEES", 270, 600, 54, (1, 1, 1), ow=10)
    ctx.restore()
    # RIGHT: reality
    sr = eout(pop(lf, 6, 16))
    ctx.save(); ctx.translate(lerp(540, 0, sr), 0)
    ctx.rectangle(546, 0, 534, H); ctx.clip()
    ctx.rectangle(540, 0, 540, H); setc(ctx, hx('ffd08a')); ctx.fill()
    rays(ctx, 750, 1000, 100, 1200, lf * 0.02, col=(1, 1, 1), a=0.3, n=14)
    ctx.rectangle(540, 1330, 540, 600); setc(ctx, hx('d89a5a')); ctx.fill()
    ctx.move_to(540, 1330); ctx.line_to(1080, 1330); ink(ctx, 7); ctx.stroke()
    hop = 10 * abs(math.sin(lf * 0.3))
    b = chubby_boy(ctx, 750, 1330 - 92 * 0.95 - hop, 0.95, -1, P(rsh=150, rel=20, lsh=40, lel=-60, eye='happy', mouth='grin', head=6), 1.0, cheeks=0.8)
    hn = b['front']
    ctx.save(); ctx.translate(hn[0], hn[1] - 30); ctx.rotate(0.4); ctx.scale(0.7, 0.7)
    ctx.rectangle(-8, -80, 16, 50); fl(ctx, (1, 1, 1), 4); ellipse(ctx, 0, 0, 44, 52); fl(ctx, hx('c8702a'), 5)
    ctx.restore()
    for k in range(3):
        plate(ctx, 640 + k * 14, 1300 - k * 18, 0.45, 'empty')
    text(ctx, "REALITY", 770, 600, 60, hx('ffe14d'), ow=10)
    ctx.restore()
    if lf >= 18:
        u = pop(lf, 18, 24)
        label(ctx, "\"SKIN AND BONES!\"", 540, 1470, 92, (1, 1, 1), -0.03, u)
    card(ctx, 'p2', f, 124, 246)


STACK_T = [6, 34, 56, 72, 86, 98, 108, 116, 123, 129]


def s3(ctx, f):
    lf = f - 250
    n_land = sum(1 for t in STACK_T if lf >= t + 8)
    g = 0.55 + 0.75 * n_land / len(STACK_T)
    zoom = lerp(1.0, 0.86, eout(pop(lf, 40, 130)))
    cy = lerp(1030, 930, eout(pop(lf, 40, 130)))
    hits = [t + 8 for t in STACK_T]
    ctx.save(); cam(ctx, 540, cy, zoom, 0, shake_at(lf, hits, 7, 10 + 2 * n_land), f)
    dining(ctx)
    # boy seated right, tummy growing
    ctx.rectangle(700, 1250, 260, 34); fl(ctx, hx('a86b3a'), 6)
    eye = 'normal' if n_land < 3 else ('shock' if n_land < 7 else 'closed')
    chubby_boy(ctx, 830, 1240, 1.3, -1, P(rsh=-30, rel=-20, lsh=20, lel=-20, eye=eye, mouth='wavy' if n_land >= 3 else 'smile',
                                         head=-4 + (3 * math.sin(lf * 0.8) if n_land >= 7 else 0), lhip=88, lkn=-82, rhip=95, rkn=-90), g, cheeks=0.6 + 0.04 * n_land)
    # Grandma left, flinging plates
    fl_ph = min([lf - t for t in STACK_T if lf - t >= 0] or [99])
    throw = fl_ph < 8
    gm = draw_hip(ctx, 170, FLOOR - 92 * 1.4, 1.4, 1, GRAN, P(rsh=150 if throw else 60, rel=-10 if throw else -70, lsh=40, lel=-60,
                                                             eye='happy', mouth='grin' if throw else 'open', head=-6))
    table(ctx, 330, 1100, 1270, 500)
    # tower of plates
    base = 1270
    for k, t in enumerate(STACK_T):
        u = pop(lf, t, t + 8)
        if u <= 0:
            continue
        tx, ty = 560, base - 10 - k * 64
        if u < 1:
            hx_, hy_ = gm['front']
            x = lerp(hx_, tx, u); y = lerp(hy_, ty, u) - 260 * math.sin(math.pi * u)
            plate(ctx, x, y, 0.8, FOODS[k % len(FOODS)])
        else:
            wob = (3 * math.sin(lf * 0.5 + k)) * (k / 10) if n_land > 6 else 0
            plate(ctx, tx + wob * k, ty, 0.8, FOODS[k % len(FOODS)])
    ctx.restore()
    if lf < 34:
        label(ctx, "\"ONE MORE!\"", 540, 1450, 120, hx('ffe14d'), 0.04, pop(lf, 2, 6))
    elif lf < 72:
        label(ctx, "\"I'M FULL...\"", 540, 1450, 120, (1, 1, 1), -0.04, pop(lf, 36, 40))
    elif lf < 108:
        label(ctx, "\"JUST A BITE!\"", 540, 1450, 116, hx('ffe14d'), 0.04, pop(lf, 74, 78))
    else:
        label(ctx, "\"ONE MORE!!\"", 540, 1450, 140, hx('ff3b5c'), -0.05, pop(lf, 108, 112))
    card(ctx, 'p3', f, 254, 396)


def s4(ctx, f):
    lf = f - 400
    if lf < 44:
        ctx.save(); cam(ctx, 540, 1000, lerp(1.0, 1.12, lf / 44), 4, shake_at(lf, [4], 10, 18), f)
        dining(ctx)
        rays(ctx, 540, 900, 160, 1600, lf * 0.04, col=(1, 0.95, 0.5), a=0.55, n=20)
        draw_hip(ctx, 540, FLOOR - 92 * 1.8, 1.8, 1, GRAN, P(rsh=170, rel=10, lsh=170, lel=-10, eye='happy', mouth='grin', head=0))
        table(ctx, -200, 1300, 1300, 600)
        drop = eout(pop(lf, 0, 6))
        cake(ctx, 540, lerp(800, 1330, drop), 0.85)
        for k in range(6):
            a_ = k * math.pi / 3 + lf * 0.05
            sparkle(ctx, 540 + math.cos(a_) * 430, 900 + math.sin(a_) * 260, 30, (1, 1, 1))
        ctx.restore()
        label(ctx, "\"DESSERT TIME!\"", 540, 1450, 120, hx('ff4fa0'), -0.04, pop(lf, 4, 8))
    else:
        il = lf - 44
        popped = il >= 22
        ctx.save(); cam(ctx, 600, 1060, 1.18, 0, shake_at(il, [22], 8, 14) + (2 if il < 22 else 0), f)
        dining(ctx)
        ctx.rectangle(420, 1270, 360, 36); fl(ctx, hx('a86b3a'), 6)
        for lx in (440, 740):
            ctx.rectangle(lx, 1306, 24, FLOOR - 1306); fl(ctx, hx('a86b3a'), 5)
        gulp = 0.08 * math.sin(math.pi * pop(il, 8, 20))
        b = chubby_boy(ctx, 600, 1260, 1.25, 1, P(rsh=-150 if il < 10 else -20, rel=-20, lsh=30, lel=-40,
                                                 eye='closed' if il < 20 else 'shock', mouth='wavy' if il < 20 else 'open', head=-6),
                       1.45 + gulp, btn=not popped, cheeks=1.1 if il < 20 else 0.7)
        ctx.restore()
        # button flies at the lens
        if popped:
            u = pop(il, 22, 34)
            bx0, by0 = 600 + (b['btn'][0] - 600) * 1.18, 960 + (b['btn'][1] - 1060) * 1.18
            if u < 1:
                x, y = lerp(bx0, 540, eout(u)), lerp(by0, 900, eout(u)) - 200 * math.sin(math.pi * u)
                r = lerp(16, 230, u ** 2)
                ctx.save(); ctx.translate(x, y); ctx.rotate(il * 0.7)
                ellipse(ctx, 0, 0, r, r); fl(ctx, hx('ffd23f'), max(4, r * 0.08))
                for dx, dy in ((-0.3, -0.3), (0.3, -0.3), (-0.3, 0.3), (0.3, 0.3)):
                    ellipse(ctx, dx * r, dy * r, r * 0.12, r * 0.12); setc(ctx, INK); ctx.fill()
                ctx.restore()
            else:
                # stuck on the lens + crack
                sl = eout(pop(il, 46, 76))
                x, y = 540, 900 + sl * 1300
                rnd = random.Random(3)
                for k in range(10):
                    a_ = k * 2 * math.pi / 10 + rnd.uniform(-0.2, 0.2)
                    pts = [(540, 900)]
                    rr = 0
                    for j in range(4):
                        rr += rnd.uniform(120, 260)
                        pts.append((540 + math.cos(a_ + rnd.uniform(-0.15, 0.15)) * rr, 900 + math.sin(a_ + rnd.uniform(-0.15, 0.15)) * rr))
                    ctx.new_path(); ctx.move_to(*pts[0])
                    for q in pts[1:]:
                        ctx.line_to(*q)
                    setc(ctx, (0, 0, 0, 0.55)); ctx.set_line_width(10); ctx.stroke_preserve(); setc(ctx, (1, 1, 1, 0.95)); ctx.set_line_width(5); ctx.stroke()
                r = 230
                ctx.save(); ctx.translate(x, y); ctx.rotate(0.3)
                ellipse(ctx, 0, 0, r, r); fl(ctx, hx('ffd23f'), 18)
                for dx, dy in ((-0.3, -0.3), (0.3, -0.3), (-0.3, 0.3), (0.3, 0.3)):
                    ellipse(ctx, dx * r, dy * r, r * 0.12, r * 0.12); setc(ctx, INK); ctx.fill()
                ctx.restore()
        if il < 22:
            label(ctx, "*GULP*", 540, 1450, 120, (1, 1, 1), 0.04, pop(il, 8, 12))
        elif il < 34:
            label(ctx, "POP!", 540, 1450, 170, hx('ff3b5c'), -0.05, pop(il, 22, 26))
        else:
            label(ctx, "PING!", 540, 1450, 170, hx('ffe14d'), 0.05, pop(il, 34, 38))
    card(ctx, 'p4', f, 404, 516)


GX, SX, BXW = -100, 560, 1150
PIV = (SX + 0.45 * 700, FLOOR)


def gran_pose(lf):
    return P(rsh=100 if lf < 46 else 150, rel=-20 if lf < 46 else 10, lsh=30, lel=-50,
             eye='happy', mouth='grin' if lf < 46 else 'open', head=-4)


def s5(ctx, f):
    lf = f - 520
    if lf < 106:
        gp = probe(GX, FLOOR - 92 * 1.4, 1.4, 1, GRAN, gran_pose(lf))
        hn = gp['front']
        # camera: tight on Grandma + her rope -> pull out to reveal the giant bag -> push to the squashed kid
        zo = eout(pop(lf, 16, 40))
        z = lerp(1.6, 0.62, zo)
        cx, cy = lerp(GX + 90, SX, zo), lerp(gp['head'][1] + 160, 760, zo)
        if lf >= 62:
            zi = eout(pop(lf, 62, 80))
            z = lerp(0.62, 0.85, zi); cx = lerp(SX, 1000, zi); cy = lerp(760, 1120, zi)
        ctx.save(); cam(ctx, cx, cy, z, 0, shake_at(lf, [60], 14, 30), f)
        porch(ctx)
        tip = ein(pop(lf, 46, 60))
        flat = lf >= 60
        if not flat:
            wob = 6 * math.sin(lf * 0.4)
            chubby_boy(ctx, BXW, FLOOR - 92 * 1.3, 1.3, -1, P(rot=wob, rsh=-20, lsh=20, eye='normal' if lf < 40 else 'shock',
                                                              mouth='smile' if lf < 40 else 'scream', head=0), 1.3)
        gm = draw_hip(ctx, GX, FLOOR - 92 * 1.4, 1.4, 1, GRAN, gran_pose(lf))
        ang = tip * math.pi / 2 if not flat else math.pi / 2 - 0.1 * math.exp(-(lf - 60) * 0.25) * math.cos((lf - 60) * 1.2)
        # rope from Grandma's hand to the bag
        ctx.save(); ctx.translate(*PIV); ctx.rotate(ang); ctx.translate(-PIV[0], -PIV[1])
        top = ctx.user_to_device(SX - 0.42 * 700, FLOOR - 1250 + 30)
        ctx.restore()
        top = ctx.device_to_user(*top)
        if lf < 50:
            ctx.new_path(); ctx.move_to(*gm['front'])
            ctx.curve_to(gm['front'][0] + 60, gm['front'][1] - 200, top[0] - 80, top[1] + 300, *top)
            setc(ctx, INK); ctx.set_line_width(20); ctx.stroke_preserve(); setc(ctx, hx('e8c890')); ctx.set_line_width(11); ctx.stroke()
            ellipse(ctx, *gm['front'], 30, 30); fl(ctx, GRAN['skin'], 6)
        if flat:
            # wiggling legs poke out from under the bag
            for k in range(2):
                a_ = 0.35 * math.sin(lf * 0.9 + k * 2)
                ctx.save(); ctx.translate(PIV[0] + 40, FLOOR - 60 - k * 80); ctx.rotate(1.87 + a_)
                ctx.move_to(0, 0); ctx.line_to(0, 200); setc(ctx, INK); ctx.set_line_width(66); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke_preserve()
                setc(ctx, BOY['pants']); ctx.set_line_width(52); ctx.stroke()
                ellipse(ctx, 26, 222, 34, 54); fl(ctx, BOY['shoes'], 7)
                ctx.restore()
        sack(ctx, SX, FLOOR, 700, 1250, ang, PIV)
        if flat:
            up_ = eout(pop(lf, 80, 88))
            if up_ > 0:
                ctx.save(); ctx.translate(1330, FLOOR - 690 - 150 * up_); ctx.scale(1.5, 1.5)
                ctx.rectangle(-26, 0, 52, 150 * up_ + 10); fl(ctx, BOY['shirt'], 7)
                ellipse(ctx, 0, -20, 48, 42); fl(ctx, BOY['skin'], 7)
                rect_r(ctx, -14, -110, 30, 80, 14); fl(ctx, BOY['skin'], 6)
                ctx.restore()
            puff(ctx, PIV[0] + 500, FLOOR - 40, pop(lf, 60, 76), 3.0)
            puff(ctx, PIV[0] + 100, FLOOR - 40, pop(lf, 61, 78), 2.4)
        ctx.restore()
        if lf < 34:
            label(ctx, "\"A LITTLE SNACK!\"", 540, 1450, 104, hx('ffe14d'), -0.04, pop(lf, 2, 6))
        elif lf < 60:
            label(ctx, "LITTLE?!", 540, 1450, 160, hx('ff3b5c'), 0.05, pop(lf, 34, 38))
        else:
            label(ctx, "\"THANKS, GRANDMA...\"", 540, 1450, 78, (1, 1, 1), -0.03, pop(lf, 66, 70))
        card(ctx, 'p5', f, 524, 622)
    else:
        il = lf - 106
        opening_face(ctx, f, il, loop=True)
        card(ctx, 'p1', f, 626)


SHOTS = [(0, s1), (120, s2), (250, s3), (400, s4), (520, s5)]
CUTS = (64, 120, 250, 400, 444, 520, 626)


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.25)
    ctx.set_source(g); ctx.paint()
    for c in CUTS:
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.5 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/w{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/gran_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
