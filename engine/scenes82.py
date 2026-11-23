"""'Dad wrapping ONE present' - original, general-audience comedy short, 22s.
Hook:   living-room medium shot: Dad with both hands taped together + tape on his face, a lumpy present on the rug
        "WHY IS IT STUCK TO ME?!" + caption "DAD vs WRAPPING PAPER:"
Beat 1: at the coffee table, smug "Wrapping? EASY." *SNIP* -> the paper is way too short "...a LITTLE short."
Beat 2: *RIIIIP!* the tape attacks: hand, forehead, cheek, the dog's nose -> "STAY... ON... THE BOX!"
Beat 3: speed-wrap whirlwind -> lumpy present on the rug, Dad proud "DONE! PERFECT!!"
Turn:   Mom drops her gift in a gift bag *FWOOP* "DONE." -> Dad ECU "...that's CHEATING!"
        Mom: "Honey... where's the GIFT?" whip-pan: the box sits unwrapped on the table *cricket*
Twist:  "PLOT TWIST: ...SO WHAT DID HE WRAP?" -> the lump wiggles, a tail pops out *wag wag* *WOOF!*
        *RRRIP!* the dog bursts out with a bow on its head, zooms around Dad with the tape -> Dad mummy
        Mom: "...FROM THE TOP, honey." -> loop to the hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes65 import dog, mug
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
PAPER = hx('ff4f6d'); PAPER_D = hx('d9334f'); BOXC = hx('5fb8ef')
DAD = dict(doodle.DAD, shirt=hx('7ed36b'), pants=hx('3d5a9e'))
MOM = dict(doodle.MOM_G, shirt=hx('8a3cff'), pants=hx('2f4a8a'))
N = 660
FLOOR = 1560
GND = 1590
KDAD, KMOM = 1.1, 1.02
TBX, TBY, TBW = 560, 1400, 400            # coffee table centre x, top y, width
LUMPX = 1250                              # where the wrapped "present" sits
DOGS = 0.5

CAPS = {'p1': [[("DAD vs ", OUT), ("WRAPPING PAPER:", RED)]],
        'p2': [[("PLOT TWIST:", RED)], [("...so what did he ", OUT), ("WRAP?", GREEN)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def tape(ctx, x, y, L, ang, w=34, a=0.85):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    ctx.new_path(); ctx.move_to(-L / 2, -w / 2)
    for i in range(1, 6):
        ctx.line_to(-L / 2 + L * i / 5, -w / 2 + (4 if i % 2 else -3))
    ctx.line_to(L / 2 + 6, 0); ctx.line_to(L / 2, w / 2)
    for i in range(4, -1, -1):
        ctx.line_to(-L / 2 + L * i / 5, w / 2 + (3 if i % 2 else -4))
    ctx.line_to(-L / 2 - 6, 0); ctx.close_path()
    setc(ctx, (1, 0.96, 0.72, a)); ctx.fill_preserve(); ink(ctx, 3); ctx.stroke()
    ctx.move_to(-L / 2 + 10, -w / 6); ctx.line_to(L / 2 - 20, -w / 6); setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def paper_pattern(ctx, x0, y0, x1, y1):
    for i in range(int(x0) - 60, int(x1) + 60, 60):
        for j in range(int(y0) - 60, int(y1) + 60, 60):
            sparkle(ctx, i + (j // 60 % 2) * 30, j, 13, GOLD)


def gift_box(ctx, x, base, w=170, h=130, wrap=0.0, lf=0):
    """plain blue box sitting on base; wrap 0..1 = short paper laid over it"""
    rect_r(ctx, x - w / 2, base - h, w, h, 10); fl(ctx, BOXC, 6)
    rect_r(ctx, x - w / 2 - 8, base - h - 22, w + 16, 30, 8); fl(ctx, hx('8fd8ff'), 6)
    for k in (-1, 1):
        ctx.move_to(x + k * w * 0.2, base - h + 20); ctx.line_to(x + k * w * 0.2, base - 10)
    setc(ctx, hx('3f9ad6')); ctx.set_line_width(4); ctx.stroke()
    if wrap > 0:
        ph = (h + 40) * wrap
        ctx.save(); rect_r(ctx, x - w / 2 - 14, base - h - 30, w + 28, ph, 6); ctx.clip_preserve()
        setc(ctx, PAPER); ctx.fill(); paper_pattern(ctx, x - w / 2 - 14, base - h - 30, x + w / 2 + 14, base - h - 30 + ph)
        ctx.restore()
        rect_r(ctx, x - w / 2 - 14, base - h - 30, w + 28, ph, 6); ink(ctx, 5); ctx.stroke()


def roll(ctx, x, y, ang=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s)
    rect_r(ctx, -32, -180, 64, 180, 14); fl(ctx, PAPER, 6)
    ctx.save(); rect_r(ctx, -32, -180, 64, 180, 14); ctx.clip(); paper_pattern(ctx, -40, -190, 40, 0); ctx.restore()
    ellipse(ctx, 0, -180, 32, 12); fl(ctx, PAPER_D, 5); ellipse(ctx, 0, -180, 12, 5); setc(ctx, hx('c9874e')); ctx.fill()
    ctx.restore()


def dispenser(ctx, x, y):
    ctx.new_path(); ctx.move_to(x - 70, y); ctx.line_to(x - 60, y - 50); ctx.curve_to(x - 40, y - 90, x + 40, y - 90, x + 60, y - 50); ctx.line_to(x + 80, y - 40); ctx.line_to(x + 70, y)
    ctx.close_path(); fl(ctx, hx('ff8a1f'), 6)
    ellipse(ctx, x - 6, y - 52, 30, 30); setc(ctx, (1, 0.96, 0.72)); ctx.fill_preserve(); ink(ctx, 4); ctx.stroke()
    ellipse(ctx, x - 6, y - 52, 12, 12); fl(ctx, hx('ffc93c'), 3)


def bow(ctx, x, y, s=1.0, col=GOLD):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for sg in (-1, 1):
        ctx.new_path(); ctx.move_to(0, 0); ctx.curve_to(sg * 30, -60, sg * 80, -40, sg * 60, 0); ctx.curve_to(sg * 70, 30, sg * 30, 20, 0, 0); fl(ctx, col, 5)
        poly(ctx, [(0, 4), (sg * 34, 50), (sg * 18, 56), (0, 12)]); fl(ctx, col, 4)
    ellipse(ctx, 0, 0, 16, 14); fl(ctx, dark(col, 0.85), 4)
    ctx.restore()


def lump(ctx, x, lf, wig=0.0, tail=0.0, burst=0.0):
    """lumpy over-taped present (secretly the dog). base on the floor at FLOOR+40."""
    if burst >= 1:
        return
    b = FLOOR + 40
    sq = 1 + 0.06 * math.sin(lf * 1.6) * wig
    ctx.save(); ctx.translate(x, b); ctx.scale(1 / sq, sq); ctx.rotate(0.05 * math.sin(lf * 1.1) * wig)
    if tail > 0:                                                         # wagging tail out the back
        ctx.save(); ctx.translate(-120, -110); ctx.rotate(-0.9 + 0.5 * math.sin(lf * 1.4))
        ctx.new_path(); ctx.move_to(0, 0); ctx.curve_to(-20, -30 * tail, -30, -60 * tail, -12, -90 * tail); ink(ctx, 24); ctx.stroke()
        ctx.new_path(); ctx.move_to(0, 0); ctx.curve_to(-20, -30 * tail, -30, -60 * tail, -12, -90 * tail); setc(ctx, hx('e8b878')); ctx.set_line_width(14); ctx.stroke()
        ctx.restore()
    pts = []
    for i in range(14):
        a = i / 14 * 2 * math.pi
        rr = 1 + 0.12 * math.sin(3 * a + 1) + 0.07 * math.sin(5 * a)
        pts.append((150 * rr * math.cos(a), -105 - 100 * rr * math.sin(a) * (1 if math.sin(a) > 0 else 0.95)))
    ctx.new_path(); ctx.move_to(*pts[0])
    for i in range(14):
        p0, p1 = pts[i], pts[(i + 1) % 14]
        m = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
        ctx.curve_to(p0[0], p0[1], p0[0], p0[1], *m)
    ctx.close_path()
    path = ctx.copy_path()
    setc(ctx, PAPER); ctx.fill()
    ctx.save(); ctx.append_path(path); ctx.clip(); paper_pattern(ctx, -180, -230, 180, 0)
    ctx.restore()
    ctx.new_path(); ctx.append_path(path); fl(ctx, (0, 0, 0, 0), 6)
    for (tx, ty, L, a) in ((-60, -150, 150, 0.5), (50, -120, 170, -0.4), (0, -60, 220, 0.1), (-90, -80, 120, 1.2), (90, -170, 110, 0.9), (20, -190, 140, -0.2)):
        tape(ctx, tx, ty, L, a, 28)
    bow(ctx, 10, -205, 1.0)
    ctx.restore()


def gift_bag(ctx, x, y, s=1.0, tissue=0.0):
    """y = bag bottom"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if tissue > 0:
        for k, (dx, a) in enumerate(((-30, -0.4), (10, 0.1), (40, 0.5))):
            ctx.save(); ctx.translate(dx, -190); ctx.rotate(a)
            poly(ctx, [(-30, 10), (0, -90 * tissue), (30, 10)]); fl(ctx, (hx('b8f0ff'), hx('ffe0ef'), hx('fff7c2'))[k], 4)
            ctx.restore()
    poly(ctx, [(-90, -200), (90, -200), (100, 0), (-100, 0)]); fl(ctx, hx('22b45a'), 6)
    for i in range(-2, 3):
        sparkle(ctx, i * 36, -90 + (i % 2) * 40, 12, WHITE)
    for sg in (-1, 1):
        ctx.new_path(); ctx.arc(sg * 40, -200, 26, math.pi, 2 * math.pi); ink(ctx, 6); ctx.stroke()
    ctx.restore()


# ------------------------------------------------------------------ set
def window(ctx, lf):
    x, y, w, h = 420, 520, 360, 300
    rect_r(ctx, x, y, w, h, 16); fl(ctx, hx('3a4a8a'), 8)
    ctx.save(); rect_r(ctx, x, y, w, h, 16); ctx.clip()
    ellipse(ctx, x + 280, y + 70, 36, 36); fl(ctx, hx('fff7c2'), 4)
    rnd = random.Random(5)
    for k in range(26):
        sx = x + rnd.uniform(0, w); sy = y + (rnd.uniform(0, h) + lf * rnd.uniform(1.5, 3)) % h
        ellipse(ctx, sx, sy, 6, 6); setc(ctx, WHITE); ctx.fill()
    ctx.new_path(); ctx.move_to(x, y + h); ctx.curve_to(x + 100, y + h - 60, x + 260, y + h - 30, x + w, y + h - 70); ctx.line_to(x + w, y + h); ctx.close_path()
    setc(ctx, WHITE); ctx.fill()
    ctx.restore()
    ctx.move_to(x + w / 2, y); ctx.line_to(x + w / 2, y + h); ctx.move_to(x, y + h / 2); ctx.line_to(x + w, y + h / 2); ink(ctx, 6); ctx.stroke()
    rect_r(ctx, x - 24, y + h - 6, w + 48, 24, 8); fl(ctx, WHITE, 5)
    for sx, d in ((x - 50, -1), (x + w - 10, 1)):
        poly(ctx, [(sx, y - 30), (sx + 60, y - 30), (sx + 60 + d * 12, y + h + 40), (sx - 10 + d * 6, y + h + 40)]); fl(ctx, hx('ffd34f'), 6)
    rect_r(ctx, x - 80, y - 44, w + 160, 20, 8); fl(ctx, hx('a0603a'), 5)


def picture(ctx, x, y, tilt=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(tilt)
    ctx.move_to(0, -100); ctx.line_to(-50, -70); ctx.move_to(0, -100); ctx.line_to(50, -70); ink(ctx, 4); ctx.stroke()
    rect_r(ctx, -80, -70, 160, 130, 10); fl(ctx, hx('ff8a5c'), 7)
    rect_r(ctx, -62, -52, 124, 94, 6); fl(ctx, hx('fff4dc'), 4)
    ellipse(ctx, 0, -2, 30, 30); fl(ctx, hx('e8b878'), 4)               # dog portrait
    for sg in (-1, 1):
        ellipse(ctx, sg * 26, -22, 10, 18, sg * 0.4); fl(ctx, hx('b9844a'), 3)
    ellipse(ctx, -9, -6, 4, 5); setc(ctx, INK); ctx.fill(); ellipse(ctx, 9, -6, 4, 5); ctx.fill()
    ctx.restore()


def tree(ctx, x, lf):
    rect_r(ctx, x - 22, FLOOR - 90, 44, 100, 6); fl(ctx, hx('a0603a'), 6)
    rect_r(ctx, x - 60, FLOOR - 40, 120, 60, 10); fl(ctx, hx('ff4f6d'), 6)
    for i, (w, y) in enumerate(((230, FLOOR - 90), (190, FLOOR - 260), (140, FLOOR - 410))):
        poly(ctx, [(x - w, y), (x + w, y), (x, y - 240)]); fl(ctx, hx('2fae5f'), 7)
    cols = (RED, GOLD, CYAN, PINK, PURPLE)
    for k in range(12):
        a = k * 2.4
        bx = x + math.sin(a) * (40 + 12 * (k % 5) * 3); by = FLOOR - 140 - k * 42
        on = (lf // 8 + k) % 3 != 0
        ellipse(ctx, bx, by, 15, 15); fl(ctx, cols[k % 5] if on else dark(cols[k % 5], 0.7), 3)
    sparkle(ctx, x, FLOOR - 650, 46, GOLD)


def sofa(ctx):
    rect_r(ctx, 1380, 1160, 520, 260, 50); fl(ctx, hx('ff9e5c'), 8)
    rect_r(ctx, 1330, 1300, 620, 200, 40); fl(ctx, hx('ffb27a'), 8)
    for cx_ in (1350, 1930):
        rect_r(ctx, cx_ - 50, 1260, 100, 260, 40); fl(ctx, hx('ff9e5c'), 7)
    ellipse(ctx, 1520, 1270, 70, 60, 0.2); fl(ctx, hx('7fe3ff'), 6)       # cushion
    sparkle(ctx, 1520, 1270, 22, WHITE)


def table(ctx):
    for lx in (TBX - TBW / 2 + 30, TBX + TBW / 2 - 60):
        rect_r(ctx, lx, TBY + 20, 30, FLOOR - TBY + 10, 8); fl(ctx, hx('a0603a'), 6)
    rect_r(ctx, TBX - TBW / 2, TBY - 10, TBW, 40, 12); fl(ctx, hx('d99a62'), 7)


def room(ctx, lf, pic_tilt=0.0):
    wall = hx('ffe9c7')
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, wall); ctx.fill()
    rnd = random.Random(82)
    for k in range(150):
        sparkle(ctx, rnd.uniform(-400, 2500), rnd.uniform(-300, FLOOR - 140), 9, dark(wall, 0.9))
    ctx.rectangle(-3000, FLOOR - 110, 9000, 110); setc(ctx, hx('ffd9a0')); ctx.fill()
    ctx.move_to(-3000, FLOOR - 110); ctx.line_to(6000, FLOOR - 110); ink(ctx, 5); ctx.stroke()
    window(ctx, lf)
    picture(ctx, 1220, 820, pic_tilt + 0.03 * math.sin(lf * 0.05))
    # paper-chain garland
    ctx.move_to(-100, 420); ctx.curve_to(400, 520, 1000, 520, 1700, 420); ink(ctx, 4); ctx.stroke()
    for i in range(14):
        t = (i + 0.5) / 14
        sparkle(ctx, -100 + 1800 * t, 420 + 100 * 4 * t * (1 - t) * 0.75 + 16, 20, (GOLD, PINK, CYAN, GREEN)[i % 4])
    ctx.rectangle(-3000, FLOOR, 9000, 3000); setc(ctx, hx('c9874e')); ctx.fill()
    for k in range(-10, 40):
        ctx.move_to(k * 150, FLOOR); ctx.line_to(k * 150 - 140, FLOOR + 600)
    setc(ctx, hx('b5743e')); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-3000, FLOOR); ctx.line_to(6000, FLOOR); ink(ctx, 7); ctx.stroke()
    ellipse(ctx, 950, FLOOR + 150, 640, 100); fl(ctx, hx('b98cff'), 6)
    ellipse(ctx, 950, FLOOR + 150, 540, 76); setc(ctx, hx('d6bcff')); ctx.fill()
    tree(ctx, 60, lf)
    sofa(ctx)
    # plant by the sofa
    px = 2010
    poly(ctx, [(px - 45, FLOOR - 90), (px + 45, FLOOR - 90), (px + 34, FLOOR + 20), (px - 34, FLOOR + 20)]); fl(ctx, hx('5fb8ef'), 6)
    for a in (-0.6, -0.2, 0.2, 0.6):
        ellipse(ctx, px + 60 * math.sin(a), FLOOR - 170 - 30 * math.cos(a), 24, 70, a); fl(ctx, GREEN, 5)
    # pet bed under the window
    ellipse(ctx, 900, FLOOR + 40, 120, 40); fl(ctx, hx('ff6f86'), 6)
    ellipse(ctx, 900, FLOOR + 28, 90, 24); fl(ctx, hx('ffc1da'), 4)
    table(ctx)


def scraps(ctx, lf, n=10, seed=1, alpha=1.0):
    rnd = random.Random(seed)
    for k in range(n):
        x = rnd.uniform(300, 1500); y = FLOOR + rnd.uniform(20, 150)
        ctx.save(); ctx.translate(x, y); ctx.rotate(rnd.uniform(-1, 1))
        poly(ctx, [(-30, -14), (26, -18), (32, 12), (-24, 16)]); fl(ctx, PAPER, 3)
        ctx.restore()


# ------------------------------------------------------------------ people
def stuck_dad(ctx, x, lf, r=1.0):
    """hands taped together over his head, tape on face"""
    w = math.sin(lf * 1.5)
    p = P(eye='shock', mouth='scream', lsh=165 + 6 * w * r, lel=-5, rsh=158 - 6 * w * r, rel=-5, torso=4 * w * r)
    d = draw(ctx, x, GND - 186 * KDAD, KDAD, -1, DAD, p)
    hx_, hy_ = (d['front'][0] + d['back'][0]) / 2, (d['front'][1] + d['back'][1]) / 2
    for k in range(3):
        tape(ctx, hx_, hy_ + (k - 1) * 18, 130, 0.3 * (k - 1) + 0.2 * w, 30)
    hd, R = d['head'], d['R']
    tape(ctx, hd[0] - R * 0.1, hd[1] - R * 0.55, R * 1.4, 0.25, 30)
    tape(ctx, hd[0] + R * 0.45, hd[1] + R * 0.35, R * 0.8, -0.7, 26)
    return d


def mom_stand(ctx, x, lf, p=None, cup=False, f_=-1):
    p = p or P(eye='smug', mouth='smile', lsh=40, lel=-120, rsh=10, rel=-20)
    m = draw(ctx, x, GND - 186 * KMOM, KMOM, f_, MOM, p)
    if cup:
        mug(ctx, m['front'][0] + f_ * 10, m['front'][1] - 26, 0.6, lf)
    return m


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = 1.28 + 0.05 * eio(pop(lf, 0, 54))
    ctx.save(); cam(ctx, 1060, 1290, z, 0, 3, f)
    room(ctx, lf)
    gift_box(ctx, TBX, TBY - 10)
    roll(ctx, TBX + 120, TBY - 10, 1.45, 0.8)
    scraps(ctx, lf, 8, 3)
    lump(ctx, LUMPX + 60, lf)
    d = stuck_dad(ctx, 930, lf)
    sweat(ctx, d['head'][0] + d['R'] * 0.95, d['head'][1] - d['R'] * 0.5, lf, 1.0)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"WHY IS IT", "STUCK TO ME?!\"", WHITE, t, 112, col2=ORANGE, y=1440)


# ------------------------------------------------------------------ shot 2: easy -> too short -> tape attack
def easy(ctx, f, il):
    # il 0..90: 0-26 smug "Wrapping? EASY.", 26 *SNIP*, 30-46 paper wraps over -> too short, 50+ "...a LITTLE short."
    z = 1.25 + 0.25 * eio(pop(il, 46, 64))
    cy = 1300
    ctx.save(); cam(ctx, lerp(760, 640, eio(pop(il, 46, 64))), cy, z, 0, shake_at(il, [26], 6, 8), f)
    room(ctx, il)
    wrap = eio(pop(il, 30, 44)) * 0.62
    gift_box(ctx, TBX, TBY - 10, wrap=wrap, lf=il)
    dispenser(ctx, TBX - 130, TBY - 10)
    if il < 26:
        roll(ctx, TBX + 150, TBY - 10, 1.57, 0.8)
        p = P(eye='smug', mouth='smile', lsh=70, lel=10, rsh=40 + 10 * math.sin(il * 0.3), rel=-20)
    elif il < 46:
        roll(ctx, TBX + 150, TBY - 10, 1.57, 0.8)
        p = P(eye='happy', mouth='grin', lsh=90, lel=-10, rsh=80, rel=-10, torso=14)
    else:
        roll(ctx, TBX + 150, TBY - 10, 1.57, 0.8)
        p = P(eye='shock', mouth='flat', lsh=50, lel=-40, rsh=30, rel=-40, head=-8 + 4 * math.sin(il))
    d = draw(ctx, 900, GND - 186 * KDAD, KDAD, -1, DAD, p)
    if 22 <= il < 30:                                                      # scissors flash
        ctx.save(); ctx.translate(d['front'][0] - 20, d['front'][1]); ctx.rotate(-0.6)
        for sg in (-1, 1):
            ellipse(ctx, -30, sg * 14, 16, 12); fl(ctx, ORANGE, 4)
            ctx.move_to(-14, sg * 10); ctx.line_to(60, -sg * 8 * (1 - pop(il, 24, 27)))
            ink(ctx, 9); ctx.stroke()
        ctx.restore()
    if il >= 50:
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.9, il, 1.1)
        # arrow at the gap
        ctx.move_to(TBX + 130, TBY - 170); ctx.line_to(TBX + 40, TBY - 70); setc(ctx, RED); ctx.set_line_width(10); ctx.stroke()
        poly(ctx, [(TBX + 30, TBY - 58), (TBX + 70, TBY - 72), (TBX + 46, TBY - 100)]); setc(ctx, RED); ctx.fill()
    ctx.restore()
    if il < 26:
        label(ctx, "\"Wrapping? EASY.\"", 540, 1450, 130, WHITE, -0.03, pop(il, 2, 5))
    elif il < 46:
        label(ctx, "*SNIP!*", 540, 520, 130, CYAN, -0.05, pop(il, 26, 29))
    else:
        label(ctx, "\"...a LITTLE short.\"", 540, 1450, 120, ORANGE, -0.03, pop(il, 50, 53))


def tape_attack(ctx, f, il):
    # il 0..96: 0 *RIIIIP!* long strip pulled; 14 sticks hand; 26 flick -> forehead; 40 cheek; 54 dog's nose; 66 hands stuck
    rot = 5 * math.sin(il * 0.09)
    ctx.save(); cam(ctx, 900, 1290, 1.1, rot, shake_at(il, [14, 26, 40, 54], 6, 8), f)
    room(ctx, il)
    gift_box(ctx, TBX, TBY - 10, wrap=0.62)
    dispenser(ctx, TBX - 130, TBY - 10)
    # dog by the pet bed, sniffs over
    dx_ = lerp(1350, 1230, eio(pop(il, 36, 52)))
    dog(ctx, dx_, GND + 20, DOGS, -1, il)
    stage = 0 if il < 14 else 1 if il < 26 else 2 if il < 40 else 3 if il < 54 else 4
    shakeA = 30 * math.sin(il * 1.3) if stage >= 1 else 0
    p = P(eye='glare' if stage < 4 else 'shock', mouth='scream', lsh=80 + shakeA, lel=10, rsh=60 - shakeA, rel=-10, torso=-6,
          lhip=10 * math.sin(il * 0.8), rhip=-10 * math.sin(il * 0.8))
    d = draw(ctx, 860, GND - 186 * KDAD, KDAD, -1, DAD, p)
    hd, R = d['head'], d['R']
    fh, bh = d['front'], d['back']
    if stage == 0:                                                         # pulling a long strip from the dispenser
        L = 60 + 300 * eout(il / 12)
        ax, ay = TBX - 130, TBY - 60
        ang = math.atan2(fh[1] - ay, fh[0] - ax)
        tape(ctx, (ax + fh[0]) / 2, (ay + fh[1]) / 2, min(L, math.hypot(fh[0] - ax, fh[1] - ay)), ang, 30)
    else:
        tape(ctx, fh[0], fh[1], 120, 0.8 + 0.3 * math.sin(il * 1.3), 30)
    if stage >= 2:
        tape(ctx, hd[0] - R * 0.1, hd[1] - R * 0.55, R * 1.4, 0.25, 30)
    if stage >= 3:
        tape(ctx, hd[0] + R * 0.45, hd[1] + R * 0.35, R * 0.8, -0.7, 26)
    if stage >= 4:                                                         # dog's nose
        tape(ctx, dx_ - 0.5 * 215, GND + 20 - 0.5 * 205, 70, 0.4, 24)
    if stage >= 4:
        tape(ctx, bh[0], bh[1], 110, -0.6, 30)
    ctx.restore()
    if stage == 0:
        label(ctx, "*RIIIIIP!*", 540, 520, 130, YEL, -0.05, pop(il, 0, 3))
    elif stage < 4:
        k = (14, 26, 40)[stage - 1]
        label(ctx, ("*THWAP!*", "*THWAP!*", "*THWAP!*")[stage - 1], 540, 520, 130, ORANGE, 0.05 * (-1) ** stage, pop(il, k, k + 3))
        label2(ctx, "\"STAY... ON...", "THE BOX!!\"", WHITE, pop(il, 16, 20), 110, col2=CYAN, y=1440)
    else:
        label(ctx, "*sniff sniff... ACHOO!*", 540, 520, 96, YEL, -0.04, pop(il, 54, 57))
        label2(ctx, "\"STAY... ON...", "THE BOX!!\"", WHITE, 1, 110, col2=CYAN, y=1440)


def s2(ctx, f):
    lf = f - 54
    if lf < 90:
        easy(ctx, f, lf)
    else:
        tape_attack(ctx, f, lf - 90)


# ------------------------------------------------------------------ shot 3: speed wrap -> "PERFECT!!"
def speed_wrap(ctx, f, il):
    # il 0..100: 0-48 whirlwind (paper + tape flying), 48 *POOF*, 52+ lump on the rug, proud Dad "DONE! PERFECT!!"
    ctx.save(); cam(ctx, 1080, 1280, 1.05, 0, shake_at(il, [48], 10, 12), f)
    room(ctx, il)
    gift_box(ctx, TBX, TBY - 10, wrap=0.62)
    dispenser(ctx, TBX - 130, TBY - 10)
    rnd = random.Random(il)
    if il < 48:
        # whirlwind ball of paper with Dad's limbs and the dog's tail poking out
        cx_, cy_ = 1090 + 30 * math.sin(il * 0.7), 1330 + 20 * math.cos(il * 0.9)
        ctx.save(); ctx.translate(cx_, cy_); ctx.scale(1.6, 1.6); ctx.translate(-cx_, -cy_)
        for k in range(14):
            a = il * 0.6 + k * 0.45; r = 130 + 60 * math.sin(k * 1.7 + il * 0.3)
            ctx.save(); ctx.translate(cx_ + math.cos(a) * r, cy_ + math.sin(a) * r * 0.8); ctx.rotate(a * 2)
            if k % 3 == 0:
                tape(ctx, 0, 0, 90, 0, 24)
            else:
                poly(ctx, [(-40, -20), (36, -24), (44, 18), (-34, 22)]); fl(ctx, PAPER, 4)
            ctx.restore()
        ellipse(ctx, cx_, cy_, 170, 140); fl(ctx, (1, 1, 1), 6)
        for k in range(6):
            a = il * 0.4 + k
            ctx.move_to(cx_ + math.cos(a) * 60, cy_ + math.sin(a) * 50); ctx.line_to(cx_ + math.cos(a + 0.8) * 150, cy_ + math.sin(a + 0.8) * 120)
        ink(ctx, 6); ctx.stroke()
        face(ctx, DAD, P(eye='glare', mouth='scream'), cx_ - 40 + 20 * math.sin(il * 1.3), cy_ - 30, 56)
        ctx.save(); ctx.translate(cx_ + 80, cy_ + 50); ctx.rotate(il * 0.9)          # dog's tail poking out
        ctx.move_to(0, 0); ctx.curve_to(20, -20, 30, -40, 20, -60); setc(ctx, hx('e8b878')); ctx.set_line_width(14); ctx.stroke()
        ctx.restore()
        for sx in (-1, 1):
            ellipse(ctx, cx_ + sx * 70, cy_ + 140, 34, 18); fl(ctx, DAD['shoes'], 4)
        ctx.restore()
    else:
        scraps(ctx, il, 12, 7)
        lump(ctx, LUMPX + 60, il)
        p = P(eye='happy', mouth='grin', lsh=150, lel=10, rsh=40, rel=-90, torso=-6)
        d = draw(ctx, 930, GND - 186 * KDAD, KDAD, 1, DAD, p)
        hd, R = d['head'], d['R']
        tape(ctx, hd[0] - R * 0.1, hd[1] - R * 0.55, R * 1.4, 0.25, 30)
        tape(ctx, hd[0] - R * 0.45, hd[1] + R * 0.35, R * 0.8, 0.7, 26)
        tape(ctx, d['front'][0], d['front'][1], 100, 0.5, 26)
        for k in range(4):
            sparkle(ctx, 1180 + k * 70, 1330 - 40 * (k % 2), 22 + 6 * math.sin(il * 0.5 + k), YEL)
        if il < 58:
            for k in range(10):
                a = k * 0.63; r = 80 + 300 * pop(il, 48, 58)
                ellipse(ctx, 1150 + math.cos(a) * r, 1400 + math.sin(a) * r * 0.6, 40, 30); setc(ctx, (1, 1, 1, 1 - pop(il, 48, 58))); ctx.fill()
    ctx.restore()
    if il < 48:
        label(ctx, "*RIP! SNIP! RIIIP!*", 540, 520, 110, YEL, 0.04 * math.sin(il * 0.4), pop(il, 0, 3))
        label(ctx, "*WOOF?!*", 540, 1450, 110, GOLD, -0.04, pop(il, 24, 27))
    else:
        label(ctx, "\"DONE! PERFECT!!\"", 540, 1450, 140, GREEN, -0.03, pop(il, 50, 53))


def s3(ctx, f):
    speed_wrap(ctx, f, f - 240)


# ------------------------------------------------------------------ shot 4: Mom's gift bag + "where's the gift?"
def mom_bag(ctx, f, il):
    # il 0..50: Mom walks in (0-14), drops box in the bag (18), *FWOOP* tissue (20-26), "DONE." (28+)
    ctx.save(); cam(ctx, 1200, 1280, 1.1, 0, shake_at(il, [18], 5, 6), f)
    room(ctx, il)
    scraps(ctx, il, 12, 7)
    lump(ctx, LUMPX + 60, il)
    d = draw(ctx, 900, GND - 186 * KDAD, KDAD, 1, DAD, P(eye='shock' if il > 22 else 'happy', mouth='open' if il > 22 else 'grin', lsh=20, lel=-20, rsh=10, rel=-20))
    hd, R = d['head'], d['R']
    tape(ctx, hd[0] - R * 0.1, hd[1] - R * 0.55, R * 1.4, 0.25, 30)
    mx = lerp(1700, 1520, eio(il / 14))
    m = mom_stand(ctx, mx, il, P(eye='smug' if il > 26 else 'normal', mouth='smile', lsh=20, lel=-90, rsh=-10, rel=-20,
                                 lhip=18 * math.sin(il * 0.6) * (il < 14), rhip=-18 * math.sin(il * 0.6) * (il < 14)))
    bx, by = m['front'][0] - 40, GND - 30
    gift_bag(ctx, bx, by, 0.8, tissue=eout(pop(il, 20, 26)))
    if il < 22:                                                         # small box falling into the bag
        u = ein(pop(il, 14, 20))
        rect_r(ctx, bx - 40, lerp(by - 330, by - 140, u), 80, 70, 8); fl(ctx, PINK, 5)
    if il >= 28:
        bow(ctx, bx, by - 175, 0.6, RED)
        sparkle(ctx, bx + 80, by - 230, 24 + 6 * math.sin(il * 0.6), YEL)
    ctx.restore()
    if il < 28:
        label(ctx, "*FWOOP!*", 540, 520, 130, CYAN, -0.05, pop(il, 20, 23))
    else:
        label(ctx, "\"DONE.\"", 540, 1450, 150, PINK, -0.03, pop(il, 28, 31))


def cheating(ctx, f, il):
    # il 0..40: Dad ECU (the one big close-up), tape on face
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.08 * eio(il / 40), 0, shake_at(il, [0], 6, 8), f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('ffd34f')); ctx.fill()
    rays(ctx, 540, 900, 240, 1500, il * 0.02, col=(1, 1, 1), a=0.35, n=16)
    face(ctx, DAD, P(eye='shock', mouth='scream'), 540, 900, 205, 0.04 * math.sin(il * 2))
    tape(ctx, 500, 740, 260, 0.25, 50)
    tape(ctx, 660, 990, 160, -0.7, 44)
    twitch(ctx, 760, 690, il, 1.5)
    ctx.restore()
    label(ctx, "\"...that's CHEATING!\"", 540, 1440, 124, RED, -0.04, pop(il, 2, 5))


def wheres_gift(ctx, f, il):
    # il 0..70: Mom points "Honey... where's the GIFT?" (0-30); whip-pan left to the table (30-40): box sits unwrapped *cricket*
    pan = eio(pop(il, 30, 40))
    cx_ = lerp(1220, 600, pan)
    ctx.save(); cam(ctx, cx_, 1280, 1.05 + 0.25 * eio(pop(il, 42, 60)), 0, 0, f)
    room(ctx, il)
    gift_box(ctx, TBX, TBY - 10, wrap=0.62)
    dispenser(ctx, TBX - 130, TBY - 10)
    scraps(ctx, il, 12, 7)
    lump(ctx, LUMPX + 60, il)
    draw(ctx, 930, GND - 186 * KDAD, KDAD, 1, DAD, P(eye='normal', mouth='flat', lsh=10, lel=-10, rsh=10, rel=-10, head=6 * math.sin(il * 0.3)))
    mom_stand(ctx, 1520, il, P(eye='normal', mouth='open', lsh=100, lel=0, rsh=-10, rel=-20), f_=-1)
    if pan > 0:
        for k in range(8):
            yy = 900 + k * 90
            ctx.move_to(cx_ - 600, yy); ctx.line_to(cx_ + 600, yy); setc(ctx, (1, 1, 1, 0.6 * math.sin(math.pi * pan))); ctx.set_line_width(14); ctx.stroke()
    if il >= 44:
        for k in range(3):
            sparkle(ctx, TBX - 90 + k * 90, TBY - 200 - 20 * (k % 2), 18 + 6 * math.sin(il * 0.5 + k), YEL)
    ctx.restore()
    if il < 34:
        label2(ctx, "\"Honey...", "where's the GIFT?\"", PINK, pop(il, 2, 6), 110, col2=WHITE, y=1440)
    else:
        label(ctx, "*cricket... cricket...*", 540, 1450, 100, WHITE, -0.03, pop(il, 42, 46))


def s4(ctx, f):
    lf = f - 340
    if lf < 50:
        mom_bag(ctx, f, lf)
    elif lf < 90:
        cheating(ctx, f, lf - 50)
    else:
        wheres_gift(ctx, f, lf - 90)


# ------------------------------------------------------------------ shot 5: the twist
def wiggle(ctx, f, il):
    # il 0..70: low floor-level push-in on the lump: wiggles (8+), tail pops out (22), *WOOF!* (36); 50 *RRRIP!* dog bursts out
    z = 1.3 + 0.2 * eio(pop(il, 0, 36))
    ctx.save(); cam(ctx, LUMPX + 40, 1470, z, 0, shake_at(il, [36, 50], 8, 10), f)
    room(ctx, il)
    scraps(ctx, il, 12, 7)
    burst = pop(il, 50, 52)
    if il < 50:
        lump(ctx, LUMPX + 60, il, wig=pop(il, 8, 14) * (1 + (il >= 36)), tail=eout(pop(il, 22, 28)))
        draw(ctx, 860, GND - 186 * KDAD, KDAD, 1, DAD, P(eye='shock', mouth='open', lsh=40, lel=-40, rsh=20, rel=-30))
    else:
        jl = il - 50
        u = eout(jl / 14)
        dog(ctx, LUMPX + 60, GND + 20 - 260 * math.sin(math.pi * min(1, jl / 14)), DOGS * 1.1, -1, il)
        bow(ctx, LUMPX + 60 - DOGS * 1.1 * 140, GND + 20 - 260 * math.sin(math.pi * min(1, jl / 14)) - DOGS * 1.1 * 300, 0.7)
        rnd = random.Random(9)
        for k in range(16):
            a = rnd.uniform(0, 2 * math.pi); r = 60 + 520 * u
            ctx.save(); ctx.translate(LUMPX + 60 + math.cos(a) * r, 1460 + math.sin(a) * r * 0.7 + 200 * u * u); ctx.rotate(a + jl * 0.3)
            poly(ctx, [(-34, -18), (30, -22), (36, 16), (-28, 20)]); fl(ctx, PAPER, 4)
            ctx.restore()
        draw(ctx, 860, GND - 186 * KDAD, KDAD, 1, DAD, P(eye='shock', mouth='scream', lsh=150, lel=-60, rsh=150, rel=-60))
    ctx.restore()
    card(ctx, 'p2', il, 0)
    if il < 22:
        label(ctx, "*wiggle wiggle*", 540, 1450, 110, WHITE, -0.03, pop(il, 8, 11))
    elif il < 36:
        label(ctx, "*wag wag*", 540, 1450, 120, GOLD, 0.03, pop(il, 22, 25))
    elif il < 50:
        label(ctx, "*WOOF!*", 540, 1450, 150, ORANGE, -0.04, pop(il, 36, 39))
    else:
        label(ctx, "*RRRRIP!!*", 540, 1450, 150, RED, -0.04, pop(il, 50, 53))


def zoomies(ctx, f, il):
    # il 0..70: dog with a bow zooms circles around Dad trailing tape -> Dad mummy-taped (0-40); Mom "...FROM THE TOP, honey." (40+)
    ctx.save(); cam(ctx, 1060, 1280, 1.05, 0, shake_at(il, [40], 6, 8), f)
    room(ctx, il)
    scraps(ctx, il, 14, 11)
    dpx = 980
    wraps = min(5, int(il / 8))
    p = P(eye='shock', mouth='scream' if il < 40 else 'flat', lsh=150 if il < 40 else 20, lel=-30 if il < 40 else -10, rsh=150 if il < 40 else -20, rel=-30 if il < 40 else -10,
          rot=10 * math.sin(il * 0.8) * (il < 40))
    draw(ctx, dpx, GND - 186 * KDAD, KDAD, 1, DAD, p)
    for k in range(wraps):                                              # tape bands around Dad
        tape(ctx, dpx, GND - 100 - k * 70, 230, 0.12 * (-1) ** k, 34, 0.9)
    if il < 40:
        a = il * 0.45
        ddx = dpx + math.cos(a) * 330; front = math.sin(a) > 0
        dog(ctx, ddx, GND + 20 + (30 if front else -20), DOGS, -1 if math.sin(a) > 0 else 1, il)
        dispenser(ctx, ddx + 60 * (-1 if math.sin(a) > 0 else 1), GND - 100)
    else:
        dog(ctx, 1260, GND + 20, DOGS, -1, il)
        bow(ctx, 1260 - DOGS * 140, GND + 20 - DOGS * 300, 0.7)
        mom_stand(ctx, 1440, il, P(eye='smug', mouth='smile', lsh=40, lel=-120, rsh=60, rel=-40, head=-6), cup=True)
        lump(ctx, -400, il)
    ctx.restore()
    if il < 40:
        label(ctx, "*ZOOM! ZOOM! ZOOM!*", 540, 520, 110, CYAN, 0.04, pop(il, 2, 5))
        label(ctx, "\"BAD DOG!!\"", 540, 1450, 140, RED, -0.03, pop(il, 12, 15))
    else:
        label2(ctx, "\"...FROM THE TOP,", "honey.\"", PINK, pop(il, 42, 46), 112, col2=WHITE, y=1440)


def s5(ctx, f):
    lf = f - 480
    if lf < 70:
        wiggle(ctx, f, lf)
    elif lf < 140:
        zoomies(ctx, f, lf - 70)
    else:
        s1(ctx, f, f - 620)


SHOTS = [(0, s1), (54, s2), (240, s3), (340, s4), (480, s5)]
CUTS = (54, 144, 240, 340, 390, 430, 480, 550, 620)


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
                              "-i", "out/wrapping_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
