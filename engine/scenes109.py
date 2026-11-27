"""'THE CHRISTMAS WISH LIST'. Original, general-audience comedy short, 22s.
Hook:   cosy living-room medium shot (tree, sofa, window with snow): the kid proudly holds up his wish list - it hangs to
        the floor, snakes through Dad's hands and runs off out of frame; Dad reads it in shock "Just a FEW things!"
        + caption 'THE CHRISTMAS WISH LIST:'.
Beat 1: Dad lets the roll go *FWIIIIP!* it rolls across the rug, bumps the door open and rolls out "...a FEW?!"
        -> paper macro: the list scrolls past Dad's thumb: 1. A PONY 2. A ROBOT 3. A ROCKET 4. ANOTHER PONY... "ANOTHER pony?!"
Beat 2: snowy street wide shot: the roll keeps unrolling down the street, Dad chasing it "COME BACK!!" -> the neighbour
        shovelling his drive picks it up and reads "...a VOLCANO?"
Beat 3: the one close-up: Dad reaches the end "ITEM 999..." "...a real DRAGON?!" -> living room: Dad with a big red
        marker *SCRIBBLE!* "NO. NO. NO." while the kid makes huge sparkly puppy eyes.
Twist:  Mom walks in with a cute little scroll with a bow "Honey... here's MINE!" -> she lets go *FWOOOOSH!!* a paper
        tidal wave fills the room and buries Dad -> PLOT TWIST: MOM'S LIST IS LONGER. -> Dad's head in the paper pile,
        twitching "...just a FEW things?!" while Mom and the kid high-five -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face, rays, _SCR
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes65 import dog
import scenes86 as R86
from scenes86 import xtree, star, FLOOR, GND, CEIL, DOORX0, DOORX1, DOORTOP
import scenes85
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
PAPER = hx('fff8e6'); PAPER_D = hx('f0e2c0'); PEN = hx('3a5ad8')
DAD = dict(doodle.DAD, shirt=hx('2fae5f'), pants=hx('34477e'))
DAD_R = dict(DAD, skin=hx('f07a6a'))
MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'), pants=hx('2f4a8a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff3b5c'))
NB = dict(doodle.NEIGHBOR, shirt=hx('9b4dff'), pants=hx('2a3a6a'))
N = 660
KD, KM, KK = 1.05, 1.0, 0.85
KIDX, DADX, MOMX = 560, 1010, 1330
TREEX = 1390

CAPS = {'p1': [[("THE CHRISTMAS ", OUT), ("WISH LIST:", RED)]],
        'p2': [[("PLOT TWIST:", RED)], [("MOM'S LIST ", OUT), ("IS LONGER.", PINK)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ paper props
def ribbon(ctx, pts, w=70, seed=0, scrib=True, red=0.0):
    """paper strip along a centre line; little handwriting lines across it. red: share of lines crossed out"""
    if len(pts) < 2:
        return
    L, Rr, nrm = [], [], []
    for i, (x, y) in enumerate(pts):
        a = pts[max(0, i - 1)]; b = pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        nrm.append((nx, ny))
        L.append((x + nx * w / 2, y + ny * w / 2)); Rr.append((x - nx * w / 2, y - ny * w / 2))
    poly(ctx, L + Rr[::-1]); fl(ctx, PAPER, 5)
    if not scrib:
        return
    rnd = random.Random(seed)
    acc = 0.0
    for i in range(1, len(pts)):
        seg = math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
        acc += seg
        if acc < 22:
            continue
        acc = 0
        x, y = pts[i]; nx, ny = nrm[i]
        a0 = rnd.uniform(-0.36, -0.2); a1 = rnd.uniform(0.0, 0.36)
        ctx.move_to(x + nx * w * a0, y + ny * w * a0); ctx.line_to(x + nx * w * a1, y + ny * w * a1)
        setc(ctx, PEN); ctx.set_line_width(4); ctx.stroke()
        if rnd.random() < red:
            ctx.move_to(x + nx * w * -0.4 - 6, y + ny * w * -0.4 - 6); ctx.line_to(x + nx * w * 0.4 + 6, y + ny * w * 0.4 + 6)
            setc(ctx, RED); ctx.set_line_width(7); ctx.stroke()


def roll(ctx, x, y, r, ang=0.0, bow=False):
    """paper roll seen end-on, resting with its bottom at y"""
    cy = y - r
    ellipse(ctx, x, cy, r, r); fl(ctx, PAPER, 6)
    ctx.save(); ctx.translate(x, cy); ctx.rotate(ang)
    ctx.new_path()
    for k in range(60):
        t = k / 59 * 4.5 * math.pi
        rr = r * 0.12 + r * 0.8 * t / (4.5 * math.pi)
        (ctx.move_to if k == 0 else ctx.line_to)(rr * math.cos(t), rr * math.sin(t))
    setc(ctx, PAPER_D); ctx.set_line_width(max(2, r * 0.06)); ctx.stroke()
    ellipse(ctx, 0, 0, r * 0.14, r * 0.14); fl(ctx, hx('c9a070'), 3)
    ctx.restore()
    if bow:
        for s in (-1, 1):
            poly(ctx, [(x, cy - r), (x + s * r * 0.9, cy - r * 1.5), (x + s * r * 0.9, cy - r * 0.6)]); fl(ctx, RED, 4)
        ellipse(ctx, x, cy - r, r * 0.22, r * 0.22); fl(ctx, RED, 4)


def marker(ctx, hand, ang=-0.6, s=1.0):
    ctx.save(); ctx.translate(*hand); ctx.rotate(ang); ctx.scale(s, s)
    rect_r(ctx, -20, -16, 150, 32, 14); fl(ctx, RED, 4)
    rect_r(ctx, -20, -16, 50, 32, 12); fl(ctx, WHITE, 4)
    poly(ctx, [(130, -12), (160, -4), (160, 4), (130, 12)]); fl(ctx, RED, 3)
    ctx.restore()


def presents(ctx, x):
    for dx, w, h, c, rc in ((-150, 120, 90, BLUE, GOLD), (-40, 90, 130, PINK, WHITE), (70, 130, 80, GOLD, RED)):
        rect_r(ctx, x + dx, FLOOR + 30 - h, w, h, 8); fl(ctx, c, 5)
        ctx.rectangle(x + dx + w / 2 - 8, FLOOR + 30 - h, 16, h); setc(ctx, rc); ctx.fill()
        poly(ctx, [(x + dx + w / 2, FLOOR + 30 - h), (x + dx + w / 2 - 26, FLOOR + 30 - h - 20), (x + dx + w / 2 - 22, FLOOR + 30 - h + 6)]); fl(ctx, rc, 3)
        poly(ctx, [(x + dx + w / 2, FLOOR + 30 - h), (x + dx + w / 2 + 26, FLOOR + 30 - h - 20), (x + dx + w / 2 + 22, FLOOR + 30 - h + 6)]); fl(ctx, rc, 3)


def stocking(ctx, x, y, c):
    ctx.move_to(x, y); ctx.line_to(x + 50, y); ctx.line_to(x + 50, y + 90); ctx.curve_to(x + 50, y + 130, x - 30, y + 140, x - 30, y + 110)
    ctx.curve_to(x - 30, y + 90, x, y + 95, x, y + 80); ctx.close_path(); fl(ctx, c, 4)
    rect_r(ctx, x - 6, y - 12, 62, 26, 10); fl(ctx, WHITE, 4)


def room(ctx, lf, opn=0.0):
    R86.room(ctx, lf, opn=opn)
    xtree(ctx, TREEX, FLOOR + 10, 760, 0.62, lf=lf, deco=1.0)
    star(ctx, TREEX, FLOOR - 760, 44, 0.1 * math.sin(lf * 0.1))
    presents(ctx, TREEX)
    dog(ctx, 300, GND + 40, 0.42, 1, lf, sleep=True)
    for k, c in enumerate((RED, GREEN, BLUE)):
        stocking(ctx, 620 + k * 130, 1000, c)


def smooth(cp, n=10):
    out = []
    for i in range(len(cp) - 1):
        p0 = cp[max(0, i - 1)]; p1 = cp[i]; p2 = cp[i + 1]; p3 = cp[min(len(cp) - 1, i + 2)]
        for j in range(n):
            t = j / n; t2 = t * t; t3 = t2 * t
            out.append(tuple(0.5 * (2 * p1[c] + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2 + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in (0, 1)))
    out.append(cp[-1])
    return out


def path_floor(x0, x1, y, amp=10, ph=0.0, step=20):
    n = max(2, int(abs(x1 - x0) / step))
    return [(x0 + (x1 - x0) * i / n, y + amp * math.sin(i * 0.5 + ph)) for i in range(n + 1)]


def hang(a, b, sag=0.0, n=16):
    (x0, y0), (x1, y1) = a, b
    return [(lerp(x0, x1, i / n), lerp(y0, y1, i / n) + sag * math.sin(math.pi * i / n)) for i in range(n + 1)]


# ------------------------------------------------------------------ people
def stand(ctx, ch, x, k, p, f_=1, g=GND):
    return draw(ctx, x, g - 186 * k, k, f_, ch, p)


def kid_proud(ctx, x, lf, eye='happy', mouth='grin'):
    b = 3 * math.sin(lf * 0.4)
    return draw(ctx, x, GND - 186 * KK - abs(b), KK, 1, KID, P(eye=eye, mouth=mouth, lsh=30, lel=-30, rsh=140, rel=-50, head=-6))


def dad_read(ctx, x, lf, ch=DAD, eye='shock', mouth='open'):
    return stand(ctx, ch, x, KD, P(eye=eye, mouth=mouth, torso=6, head=12, lsh=70, lel=-80, rsh=60, rel=-90, lhip=-6, rhip=8), -1)


def list_scene(ctx, lf, dad_eye='shock', dad_mouth='open', kid_eye='happy'):
    k = kid_proud(_SCR, KIDX, lf, kid_eye)
    top = k['front']
    ribbon(ctx, smooth([(top[0], top[1] - 60), (top[0] + 10, top[1] + 200), (KIDX + 110, FLOOR - 20), (KIDX + 200, FLOOR + 70)]), 66, 1)
    k = kid_proud(ctx, KIDX, lf, kid_eye)
    d = dad_read(ctx, DADX, lf, DAD, dad_eye, dad_mouth)
    h1, h2 = d['front'], d['back']
    hm = ((h1[0] + h2[0]) / 2, (h1[1] + h2[1]) / 2)
    w = 4 * math.sin(lf * 0.2)
    cp = [(KIDX + 200, FLOOR + 70), (DADX - 200, FLOOR + 80 + w), (DADX - 120, FLOOR - 80), (hm[0] - 40, hm[1] + 10),
          (hm[0] + 50, hm[1] + 20), (DADX + 130, FLOOR - 40), (DADX + 230, FLOOR + 80), (DADX + 600, FLOOR + 74 - w), (2600, FLOOR + 80)]
    ribbon(ctx, smooth(cp), 66, 2)
    return k, d


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = 1.0 + 0.04 * eio(pop(lf, 0, 54))
    ctx.save(); cam(ctx, 860, 1190, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    room(ctx, lf)
    k, d = list_scene(ctx, lf)
    sweat(ctx, d['head'][0] + d['R'] * 1.0, d['head'][1] - d['R'] * 0.3, lf, 0.9)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"Just a", "FEW things!\"", WHITE, t, 120, col2=GREEN, y=1430)


# ------------------------------------------------------------------ shot 2: the roll escapes -> paper macro
def escape(ctx, f, il):
    # il 0..60: 4 Dad lets go; roll zooms right along the floor *FWIIIIP!*; 26 door bursts open, roll gone ; 36 "...a FEW?!"
    u = eio(pop(il, 4, 28))
    rx = lerp(DADX + 160, 1900, u)
    opn = pop(il, 22, 28)
    ctx.save(); cam(ctx, 1150, 1210, 0.86, 0, shake_at(il, [26], 8, 10), f)
    room(ctx, il, opn=opn)
    ke, km = ('shock' if il > 10 else 'happy'), ('open' if il > 10 else 'grin')
    top = kid_proud(_SCR, KIDX, il, ke, km)['front']
    ribbon(ctx, smooth([(top[0], top[1] - 60), (top[0] + 10, top[1] + 200), (KIDX + 110, FLOOR - 20), (KIDX + 200, FLOOR + 70)]), 66, 1)
    k = kid_proud(ctx, KIDX, il, ke, km)
    d = stand(ctx, DAD, DADX, KD, P(eye='shock', mouth='scream' if il > 30 else 'open', torso=-4, head=-6, lsh=140, lel=-20, rsh=150, rel=-30, lhip=-10, rhip=10), -1)
    pts = path_floor(KIDX + 200, min(rx, DOORX1 + 200), FLOOR + 70, 8, il * 0.2)
    ribbon(ctx, pts, 66, 2)
    if rx < DOORX0 + 160:
        roll(ctx, rx, FLOOR + 110, 90 - 20 * u, rx * 0.03)
        for j in range(3):   # speed lines
            ctx.move_to(rx - 130 - j * 40, FLOOR + 10 + j * 30); ctx.line_to(rx - 240 - j * 50, FLOOR + 10 + j * 30)
        setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()
    if il < 36:
        label(ctx, "*FWIIIIP!*", 540, 560, 120, GOLD, -0.05, pop(il, 4, 7))
    else:
        label(ctx, "\"...a FEW?!\"", 540, 1500, 140, RED, -0.03, pop(il, 36, 40))


ITEMS = [("1. A PONY", PINK), ("2. A ROBOT", BLUE), ("3. A ROCKET", ORANGE), ("4. ANOTHER PONY", PINK),
         ("5. A CASTLE", PURPLE), ("6. A VOLCANO", RED), ("7. MORE SNOW", BLUE), ("8. A 3rd PONY", PINK)]


def doodle_icon(ctx, i, x, y, s=1.0):
    if i in (0, 3, 7):   # little pony-ish horse head doodle: just a heart
        ctx.move_to(x, y + 14 * s); ctx.curve_to(x - 34 * s, y - 14 * s, x - 14 * s, y - 40 * s, x, y - 20 * s)
        ctx.curve_to(x + 14 * s, y - 40 * s, x + 34 * s, y - 14 * s, x, y + 14 * s); fl(ctx, PINK, 3)
    else:
        sparkle(ctx, x, y - 10, 26 * s, GOLD)


def macro(ctx, f, il):
    # il 0..80 the list scrolls up past Dad's thumb ; item 4 centred around il 44 -> "ANOTHER pony?!"
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('ffe0d0')), (1, hx('ffc9b0'))])); ctx.paint()
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eio(il / 80), -4, shake_at(il, [44], 6, 8), f)
    poly(ctx, [(150, -200), (930, -200), (950, 2200), (130, 2200)]); fl(ctx, PAPER, 8)
    off = 760 - il * 9.0 if il < 44 else 760 - 44 * 9.0 - (il - 44) * 3.5
    for k in range(-2, 30):
        y = (off % 120) + k * 120
        ctx.move_to(170, y); ctx.line_to(930, y); setc(ctx, hx('bcd4ff')); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(260, -200); ctx.line_to(260, 2200); setc(ctx, hx('ffb0b8')); ctx.set_line_width(5); ctx.stroke()
    y0 = off - 240
    text(ctx, "DEAR SANTA,", 560, y0, 92, PEN, ow=0, shadow=False, ang=-0.03)
    for i, (s, c) in enumerate(ITEMS):
        y = off + i * 240
        big = 1.25 if i == 3 and il >= 44 else 1.0
        text(ctx, s, 570, y, 78 * big, c if i == 3 else PEN, ow=0, shadow=False, ang=0.02 * ((i % 3) - 1))
        doodle_icon(ctx, i, 870, y - 30, 1.0)
        if i == 3 and il >= 44:
            ctx.new_path(); ctx.save(); ctx.translate(570, y - 26); ctx.scale(1, 0.4)
            ctx.arc(0, 0, 380, 0, 6.29); ctx.restore(); setc(ctx, RED); ctx.set_line_width(9); ctx.stroke()
    # Dad's thumb on the edge
    tx_ = 150
    rect_r(ctx, -60, 1180, 260, 150, 70); fl(ctx, DAD['skin'], 7)
    rect_r(ctx, -120, 1160, 160, 200, 40); fl(ctx, DAD['shirt'], 7)
    ctx.restore()
    if il >= 44:
        label(ctx, "\"ANOTHER", 540, 1440, 120, WHITE, -0.03, pop(il, 44, 48))
        label(ctx, "PONY?!\"", 540, 1560, 150, PINK, 0.03, pop(il, 48, 51))


def s2(ctx, f):
    il = f - 60
    if il < 60:
        escape(ctx, f, il)
    else:
        macro(ctx, f, il - 60)


# ------------------------------------------------------------------ shot 3: down the street
SG = scenes85.SGND


def street(ctx, f, il):
    # il 0..140: 0-70 roll unrolls down the street, Dad chasing "COME BACK!!" ; 70-140 neighbour reads it "...a VOLCANO?"
    if il < 70:
        u = il / 70
        cx = lerp(900, 1700, eio(u)); z = 0.9
    else:
        cx = lerp(1700, 2150, eio(pop(il, 70, 84))); z = lerp(0.9, 1.05, eio(pop(il, 70, 84)))
    ctx.save(); cam(ctx, cx, 1380, z, -4 if il < 70 else 0, 3 if il < 70 else 0, f)
    scenes85.world(ctx, il, drive=0.0, nb_drive=0.8, nb_house=True, kid=False)
    rx = lerp(760, 3400, il / 110)
    door_x = scenes85.DX
    pts = hang((door_x + 10, scenes85.HZ + 60), (door_x + 100, SG + 20), 40, 10)
    pts += path_floor(door_x + 100, min(rx, 4000), SG + 20, 10, il * 0.2)[1:]
    ribbon(ctx, pts, 62, 3)
    if rx < 3300:
        roll(ctx, rx, SG + 60, 70, rx * 0.04)
    # neighbour on his drive
    nx = 2280
    if il < 70:
        n = stand(ctx, NB, nx, 1.0, P(eye='normal', mouth='smile', torso=14, lsh=120, lel=-10, rsh=130, rel=-10), -1, g=1560)
        R85hat(ctx, n)
    else:
        n = stand(ctx, NB, nx, 1.0, P(eye='smug', mouth='flat', head=14, lsh=60, lel=-80, rsh=50, rel=-90), -1, g=1560)
        R85hat(ctx, n)
        a, b = n['front'], n['back']
        ribbon(ctx, hang((a[0] - 40, SG + 20), ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 20), -60, 8) +
               hang(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 20), (a[0] + 160, SG + 20), 20, 8)[1:], 62, 4)
    # Dad chasing
    dxp = lerp(820, 1900, il / 140)
    s_ = math.sin(il * 0.9)
    d = stand(ctx, DAD_R, dxp, KD, P(eye='shock', mouth='scream', torso=14, lsh=150 + 20 * s_, lel=-20, rsh=-40 - 20 * s_, rel=-40,
                                    lhip=-30 * s_, lkn=-20, rhip=30 * s_, rkn=-20), 1, g=SG)
    sweat(ctx, d['head'][0] - d['R'] * 1.0, d['head'][1] - d['R'] * 0.3, il, 0.9)
    ctx.restore()
    scenes85.snow_fall(ctx, il)
    if il < 70:
        label(ctx, "*ROLL ROLL ROLL*", 540, 560, 96, CYAN, -0.04, pop(il, 2, 6))
        label(ctx, "\"COME BACK!!\"", 540, 1500, 130, RED, 0.03, pop(il, 20, 24))
    else:
        label(ctx, "\"...a", 540, 1400, 110, WHITE, -0.03, pop(il, 88, 92))
        label(ctx, "VOLCANO?\"", 540, 1510, 140, RED, 0.03, pop(il, 94, 97))


def R85hat(ctx, d):
    try:
        scenes85.hat(ctx, d, GOLD)
    except TypeError:
        scenes85.hat(ctx, d)


def s3(ctx, f):
    street(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: close-up -> scribble
def closeup(ctx, f, il):
    # il 0..52: Dad ECU holding the last bit of the list "ITEM 999..." 24 "...a real DRAGON?!"
    z = 1.0 + 0.06 * eio(il / 52)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('6fd08a')), (1, hx('d6f5c8'))])); ctx.paint()
    ctx.save(); cam(ctx, 540, 960, z, 0, shake_at(il, [24], 12, 14), f)
    rays(ctx, 540, 860, 200, 1200, il * 0.03, (1, 1, 1), 0.25, 16)
    face(ctx, DAD_R if il >= 24 else DAD, P(eye='shock', mouth='scream' if il >= 24 else 'open'), 540, 860, 200)
    pts = hang((-40, 1250), (1120, 1210), -40, 20)
    ribbon(ctx, pts, 170, 9)
    ctx.restore()
    label(ctx, "\"ITEM 999...", 540, 1380, 110, WHITE, -0.03, pop(il, 3, 7))
    if il >= 24:
        label(ctx, "...a real DRAGON?!\"", 540, 1490, 112, RED, 0.03, pop(il, 24, 27))


def scribble(ctx, f, il):
    # il 0..48: Dad crosses items out with a big red marker *SCRIBBLE!* "NO. NO. NO." ; kid sparkly puppy eyes
    ctx.save(); cam(ctx, 800, 1210, 1.12, 3, shake_at(il, [4, 18, 32], 4, 5), f)
    room(ctx, il)
    k = draw(ctx, KIDX + 40, GND - 186 * KK, KK, 1, KID, P(eye='shock', mouth='wavy', lsh=150, lel=-150, rsh=150, rel=-150, head=-12))
    for s in (-1, 1):
        sparkle(ctx, k['head'][0] + s * k['R'] * 0.32 + 14, k['head'][1] - k['R'] * 0.02, 18 + 6 * math.sin(il * 0.6), WHITE)
    d = stand(ctx, DAD, DADX, KD, P(eye='glare', mouth='scream', torso=10, head=8, lsh=60, lel=-70, rsh=90 + 30 * math.sin(il * 1.3), rel=-50), -1)
    a = d['back']
    red = min(1.0, il / 40)
    pts = hang((DADX - 260, FLOOR + 70), (a[0] - 10, a[1] - 10), -30, 8)
    pts += hang((a[0] - 10, a[1] - 10), (DADX + 240, FLOOR + 70), 20, 10)[1:]
    ribbon(ctx, pts, 66, 5, red=red)
    marker(ctx, d['front'], -2.4 + 0.3 * math.sin(il * 1.3), 1.0)
    ctx.restore()
    label(ctx, "*SCRIBBLE!*", 540, 560, 110, RED, -0.05, pop(il, 2, 5))
    words = ["\"NO.", "NO.", "NO.\""]
    for j, w in enumerate(words):
        if il >= 4 + 14 * j:
            label(ctx, w, 260 + 280 * j, 1500, 130, WHITE if j < 2 else RED, (-0.06, 0.04, -0.03)[j], pop(il, 4 + 14 * j, 7 + 14 * j))


def s4(ctx, f):
    il = f - 340
    if il < 52:
        closeup(ctx, f, il)
    else:
        scribble(ctx, f, il - 52)


# ------------------------------------------------------------------ shot 5: Mom's list
def paper_mound(ctx, x0, x1, h, lf, seed=7):
    if h <= 2:
        return
    rnd = random.Random(seed)
    n = 9
    pts = [(x0, FLOOR + 120)]
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        e = math.sin(math.pi * (0.08 + 0.84 * i / n)) ** 0.5
        pts.append((x, FLOOR + 120 - h * e * rnd.uniform(0.85, 1.05) - 8 * math.sin(lf * 0.3 + i)))
    pts.append((x1, FLOOR + 120))
    poly(ctx, pts); fl(ctx, PAPER, 7)
    for k in range(int((x1 - x0) * h / 9000)):   # loops of paper + handwriting
        x = rnd.uniform(x0 + 60, x1 - 60)
        top = min(y for (px, y) in pts if abs(px - x) < (x1 - x0) / n) if False else FLOOR + 120 - h * 0.8
        y = rnd.uniform(top + 30, FLOOR + 90)
        ctx.new_path(); ctx.arc(x, y, rnd.uniform(26, 50), rnd.uniform(0, 3), rnd.uniform(3.5, 6)); setc(ctx, PAPER_D); ctx.set_line_width(5); ctx.stroke()
        ctx.move_to(x - 30, y + 20); ctx.line_to(x + 20, y + 16); setc(ctx, PEN); ctx.set_line_width(4); ctx.stroke()


def mom_scene(ctx, f, il):
    # il 0..120: 0 Mom walks in from the door with a cute small scroll "Honey... here's MINE!" ; 50 lets go *FWOOOOSH!!*
    #            54-80 a paper tidal wave fills the room, buries Dad ; 62 card p2
    ctx.save(); cam(ctx, 1000, 1190, 0.98, 0, shake_at(il, [50], 14, 26) + (4 if 50 <= il < 80 else 0), f)
    room(ctx, il, opn=1.0 - pop(il, 20, 30))
    k = draw(ctx, KIDX, GND - 186 * KK, KK, 1, KID, P(eye='shock' if il >= 50 else 'normal', mouth='open' if il >= 50 else 'smile', lsh=40, lel=-30, rsh=30, rel=-30))
    mx = lerp(1720, MOMX, eout(pop(il, 0, 18)))
    s_ = math.sin(il * 0.7) if il < 18 else 0
    if il < 50:
        d = stand(ctx, DAD, DADX, KD, P(eye='normal' if il < 30 else 'shock', mouth='smile' if il < 30 else 'open', lsh=20, lel=-20, rsh=30, rel=-20), 1)
        m = stand(ctx, MOM, mx, KM, P(eye='happy', mouth='grin', lsh=70, lel=-70, rsh=85 if il >= 24 else 40, rel=-40, lhip=16 * s_, rhip=-16 * s_), -1)
        hp = m['front']
        roll(ctx, hp[0], hp[1] + 40, 40, 0, bow=True)
    else:
        u = eout(pop(il, 50, 80))
        h = 520 * u
        d = stand(ctx, DAD, DADX, KD, P(eye='shock', mouth='scream', lsh=160, lel=-10, rsh=160, rel=-10))
        m = stand(ctx, MOM, MOMX, KM, P(eye='happy', mouth='grin', lsh=70, lel=-70, rsh=120, rel=-30), -1)
        # the wave: big ribbons flying out of her roll, mound rising around Dad
        rx = lerp(MOMX - 60, 300, u)
        paper_mound(ctx, DADX - 330 - 200 * u, DADX + 260, h, il)
        for j in range(4):
            ph = il * 0.25 + j * 1.3
            pts = [(MOMX - 80 - t * (900 * u + 100), FLOOR - 200 - j * 70 - 260 * math.sin(t * math.pi) * u + 30 * math.sin(ph + t * 8)) for t in [i / 24 for i in range(25)]]
            ribbon(ctx, pts, 60, 11 + j)
        if il < 70:
            roll(ctx, m['front'][0] - 20, m['front'][1] + 120, 50 * (1 - 0.4 * u), il * 0.8)
    ctx.restore()
    if il < 50:
        label(ctx, "\"Honey...", 540, 1400, 110, WHITE, -0.03, pop(il, 18, 22))
        label(ctx, "here's MINE!\"", 540, 1510, 130, PINK, 0.03, pop(il, 28, 31))
    elif il < 62:
        label(ctx, "*FWOOOOSH!!*", 540, 600, 130, GOLD, -0.05, pop(il, 50, 53))
    card(ctx, 'p2', il, 62)


def buried(ctx, f, il):
    # il 0..60: Dad's head poking out of the paper pile, twitch "...just a FEW things?!" ; Mom + kid high-five
    ctx.save(); cam(ctx, 940, 1400, 1.08, 0, 0, f)
    room(ctx, il + 120)
    hf = pop(il, 30, 36)
    k = draw(ctx, KIDX - 40, GND - 186 * KK - 30 * math.sin(math.pi * hf), KK, 1, KID, P(eye='happy', mouth='grin', lsh=30, lel=-20, rsh=150, rel=-20))
    m = stand(ctx, MOM, MOMX, KM, P(eye='happy', mouth='grin', lsh=30, lel=-20, rsh=150, rel=-20), -1)
    paper_mound(ctx, DADX - 560, DADX + 300, 260, il * 0.3, 8)
    d = stand(ctx, DAD, DADX, KD, P(eye='glare', mouth='wavy', head=-6), -1, g=GND + 190)
    paper_mound(ctx, DADX - 240, DADX + 240, 70, il * 0.3, 9)
    if il > 6:
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.9, il, 1.0)
    ctx.restore()
    label(ctx, "\"...just a", 540, 1440, 110, WHITE, -0.03, pop(il, 4, 8))
    label(ctx, "FEW things?!\"", 540, 1550, 130, GREEN, 0.03, pop(il, 16, 19))
    if il >= 32:
        label(ctx, "*CLAP!*", 300, 600, 90, GOLD, -0.08, pop(il, 32, 35))


def s5(ctx, f):
    lf = f - 440
    if lf < 130:
        mom_scene(ctx, f, lf)
    elif lf < 190:
        buried(ctx, f, lf - 130)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (200, s3), (340, s4), (440, s5)]
CUTS = (60, 120, 200, 340, 392, 440, 570, 630)


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
                              "-i", "out/wish_list_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
