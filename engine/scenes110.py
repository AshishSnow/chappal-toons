"""'GRANDMA'S HOMEMADE SWEATER'. Original, general-audience comedy short, 22s.
Hook:   cosy living-room medium shot: the kid drowning in a huge lumpy knitted reindeer sweater (sleeves flop to the floor)
        with a forced grin + sweat, Grandma beaming next to him with her yarn ball "I... LOVE it!!"
        + caption 'GRANDMA'S HOMEMADE SWEATER:'.
Beat 1: sweater macro: the knitted reindeer is cross-eyed; its nose lights up *blink blink* and plays a tinny jingle
        "...it SINGS?!" -> Grandma waves "Bye, sweetie!" and leaves, door *CLICK* -> kid whips it off *FWIP!* and
        stuffs it in a present box with the dog watching "...BYE, sweater."
Beat 2: *DING-DONG!* Grandma pops back in "I forgot my GLASSES!" -> Dutch-tilt *ZOOP!* blur -> kid wearing it again,
        upside-down reindeer + a sleeve flopped over his head "Still... WEARING it!" -> Grandma melts with hearts.
Beat 3: the one close-up: twitching forced grin "It's... my FAVOURITE." -> Grandma "Good! I made you... TWELVE MORE!"
        *THUMP!* a wobbling tower of sweaters.
Twist:  PLOT TWIST: DAD GOT ONE TOO. Dad shuffles in with a giant matching sweater up to his nose, nose blinking,
        "...help me." + the dog in a tiny matching one, wagging. Grandma "Everybody SMILE!" *CLICK!* flash ->
        family-photo freeze with a twitching kid -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face, rays, _SCR
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes65 import dog
import scenes109 as W9
from scenes86 import FLOOR, GND, DOORX0, DOORX1, DOORTOP
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
KNIT = hx('e8344e'); KNIT_D = hx('c0233c'); DEER = hx('a8683e'); YARN = hx('3fb56a')
DAD = dict(doodle.DAD, shirt=hx('3a5ad8'), pants=hx('34477e'))
MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'), pants=hx('2f4a8a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ffc93c'))
GRAN = dict(doodle.NMOM, hair=hx('dcdce6'), shirt=hx('b98cff'), pants=hx('5a4a8a'), shoes=hx('ff6b8a'), glasses=hx('8a3cff'))
N = 660
KD, KK, KG = 1.05, 0.85, 0.95
KIDX, GRX, DADX = 760, 1180, 1250

CAPS = {'p1': [[("GRANDMA'S ", OUT), ("HOMEMADE SWEATER:", RED)]],
        'p2': [[("PLOT TWIST:", RED)], [("DAD GOT ", OUT), ("ONE TOO.", BLUE)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ the sweater
def deer_face(ctx, x, y, r, nose=0.0, flip=False):
    ctx.save(); ctx.translate(x, y)
    if flip:
        ctx.rotate(math.pi)
    for s in (-1, 1):   # antlers
        ctx.new_path(); ctx.move_to(s * r * 0.4, -r * 0.8); ctx.line_to(s * r * 0.9, -r * 1.7)
        ctx.move_to(s * r * 0.65, -r * 1.25); ctx.line_to(s * r * 1.2, -r * 1.35)
        ctx.move_to(s * r * 0.8, -r * 1.55); ctx.line_to(s * r * 0.5, -r * 1.95)
        setc(ctx, INK); ctx.set_line_width(r * 0.32); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke_preserve()
        setc(ctx, hx('f6e0b0')); ctx.set_line_width(r * 0.2); ctx.stroke()
        ellipse(ctx, s * r * 0.95, -r * 0.55, r * 0.32, r * 0.18, s * 0.5); fl(ctx, DEER, 3)
    ellipse(ctx, 0, 0, r * 0.85, r); fl(ctx, DEER, 4)
    for s in (-1, 1):   # cross-eyed
        ellipse(ctx, s * r * 0.34, -r * 0.2, r * 0.22, r * 0.26); fl(ctx, WHITE, 3)
        ellipse(ctx, s * r * 0.2, -r * 0.16, r * 0.1, r * 0.12); setc(ctx, INK); ctx.fill()
    if nose > 0:
        ellipse(ctx, 0, r * 0.55, r * 0.6 * nose, r * 0.6 * nose); setc(ctx, (1, 0.3, 0.35, 0.35)); ctx.fill()
    ellipse(ctx, 0, r * 0.55, r * 0.3, r * 0.26); fl(ctx, hx('ff2a3a') if nose > 0 else hx('c0233c'), 3)
    if nose > 0:
        ellipse(ctx, -r * 0.08, r * 0.48, r * 0.08, r * 0.06); setc(ctx, WHITE); ctx.fill()
    ctx.restore()


def zig(ctx, x0, x1, y, h, col, lw=6):
    ctx.new_path(); n = max(2, int((x1 - x0) / (h * 1.2)))
    for i in range(n + 1):
        (ctx.move_to if i == 0 else ctx.line_to)(lerp(x0, x1, i / n), y + (h / 2 if i % 2 else -h / 2))
    setc(ctx, col); ctx.set_line_width(lw); ctx.stroke()


def tube(ctx, pts, w, col, lw=5):
    ctx.new_path(); ctx.move_to(*pts[0])
    if len(pts) == 4:
        ctx.curve_to(*pts[1], *pts[2], *pts[3])
    else:
        for q in pts[1:]:
            ctx.line_to(*q)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    setc(ctx, INK); ctx.set_line_width(w + lw * 2); ctx.stroke_preserve(); setc(ctx, col); ctx.set_line_width(w); ctx.stroke()


def sweater(ctx, d, x, k, g=GND, big=1.3, col=KNIT, nose=0.0, flip=False, sleeve_head=False, droop=1.0, collar_up=0.0, lf=0):
    """lumpy knitted sweater drawn over a standing upright character (draw() result d)"""
    S = k * 1.35
    hip = g - 68 * S
    TL = 104 * S * 0.88
    neck = hip - TL + 8 * S
    sw, bw = 54 * S * big, 66 * S * big
    bot = hip + 46 * S * big
    lw = max(4, 3.2 * S)
    sh = {s: (x + s * 44 * S, neck + 22 * S) for s in (-1, 1)}
    # sleeves first (behind body edges), ending way past the hands
    hands = [d['front'], d['back']]
    for s in (-1, 1):
        sp = sh[s]
        if sleeve_head and s == 1:
            continue
        hd = min(hands, key=lambda h: (h[0] - sp[0]) ** 2 + (h[1] - sp[1]) ** 2)
        dx, dy = hd[0] - sp[0], hd[1] - sp[1]
        L = math.hypot(dx, dy) or 1
        ex = (hd[0] + dx / L * 40 * S * big, hd[1] + dy / L * 40 * S * big)
        end = (ex[0] + s * 18 * S, min(FLOOR + 40, ex[1] + 120 * S * droop * big))
        tube(ctx, [sp, hd, ex, end], 40 * S * big ** 0.5, col, lw)
        ellipse(ctx, end[0], end[1], 22 * S * big ** 0.5, 14 * S * big ** 0.5); fl(ctx, WHITE, lw)
    # body
    w8 = 6 * S * math.sin(lf * 0.3)
    pts = [(x - 34 * S, neck - 4 * S), (x - sw, neck + 20 * S), (x - bw - 8 * S, bot - 30 * S), (x - bw, bot)]
    for i in range(1, 6):
        pts.append((lerp(x - bw, x + bw, i / 6), bot + (10 * S if i % 2 else -4 * S) + (w8 if i == 3 else 0)))
    pts += [(x + bw, bot), (x + bw + 8 * S, bot - 30 * S), (x + sw, neck + 20 * S), (x + 34 * S, neck - 4 * S)]
    poly(ctx, pts); fl(ctx, col, lw)
    ctx.save(); poly(ctx, pts); ctx.clip()
    zig(ctx, x - bw - 20, x + bw + 20, neck + 52 * S * big, 18 * S, WHITE, 6 * S)
    zig(ctx, x - bw - 20, x + bw + 20, bot - 22 * S, 16 * S, YARN, 6 * S)
    for j, (fx, fy) in enumerate(((-0.62, 0.48), (0.66, 0.5), (-0.5, 0.82), (0.55, 0.8))):
        sparkle(ctx, x + fx * bw, neck + fy * (bot - neck), 9 * S, WHITE)
    ctx.restore()
    deer_face(ctx, x, neck + 0.62 * (bot - neck), 24 * S * big, nose, flip)
    # rolled collar (can ride up over the chin)
    cy = neck - collar_up * 60 * S
    rect_r(ctx, x - 40 * S * big, cy - 14 * S * big, 80 * S * big, 30 * S * big + collar_up * 60 * S, 14 * S); fl(ctx, KNIT_D, lw)
    for i in range(5):
        xx = x - 30 * S * big + i * 15 * S * big
        ctx.move_to(xx, cy - 8 * S * big); ctx.line_to(xx, cy + 10 * S * big + collar_up * 60 * S)
    setc(ctx, dark(KNIT_D, 0.85)); ctx.set_line_width(3); ctx.stroke()
    if sleeve_head:   # right sleeve flopped over his head like a hat
        hd = d['head']; R = d['R']
        tube(ctx, [sh[1], (hd[0] + R * 1.2, hd[1] - R * 0.2), (hd[0] + R * 0.3, hd[1] - R * 1.5), (hd[0] - R * 1.1, hd[1] - R * 0.6)],
             40 * S * big ** 0.5, col, lw)
        ellipse(ctx, hd[0] - R * 1.1, hd[1] - R * 0.6, 22 * S, 14 * S); fl(ctx, WHITE, lw)


def dog_sweater(ctx, x, y, s, f_=1, col=KNIT):
    ctx.save(); ctx.translate(x, y); ctx.scale(f_ * s, s)
    ctx.rectangle(-400, -400, 470, 600); ctx.clip()
    ellipse(ctx, -10, -140, 128, 72); fl(ctx, col, 6)
    ctx.save(); ellipse(ctx, -10, -140, 128, 72); ctx.clip()
    zig(ctx, -150, 120, -150, 26, WHITE, 9)
    ctx.restore()
    ctx.restore()


def yarn(ctx, x, y, r=34, lf=0):
    ellipse(ctx, x, y, r, r); fl(ctx, YARN, 5)
    for a in (-0.6, 0.0, 0.6):
        ctx.new_path(); ctx.arc(x + r * 0.3 * math.sin(a), y, r * 0.75, a + 1.0, a + 2.6); setc(ctx, dark(YARN, 0.8)); ctx.set_line_width(4); ctx.stroke()
    for s in (-1, 1):
        ctx.move_to(x + s * 10, y - r * 0.9); ctx.line_to(x + s * 40, y - r * 2.2)
    setc(ctx, hx('c9a070')); ctx.set_line_width(8); ctx.stroke()


def heart(ctx, x, y, r, col=PINK):
    ctx.new_path(); ctx.move_to(x, y + r * 0.7); ctx.curve_to(x - r * 1.4, y - r * 0.3, x - r * 0.5, y - r * 1.3, x, y - r * 0.4)
    ctx.curve_to(x + r * 0.5, y - r * 1.3, x + r * 1.4, y - r * 0.3, x, y + r * 0.7); fl(ctx, col, 4)


# ------------------------------------------------------------------ people
def stand(ctx, ch, x, k, p, f_=1, g=GND):
    return draw(ctx, x, g - 186 * k, k, f_, ch, p)


def kid_in_sweater(ctx, x, lf, eye='happy', mouth='grin', nose=0.0, flip=False, sleeve_head=False, arms=(40, 40), head=0, hop=0.0, rot=0):
    p = P(eye=eye, mouth=mouth, lsh=arms[0], lel=-20, rsh=arms[1], rel=-20, head=head, rot=rot)
    g = GND - hop
    d = stand(ctx, KID, x, KK, p, 1, g)
    sweater(ctx, d, x, KK, g, 1.35, nose=nose, flip=flip, sleeve_head=sleeve_head, lf=lf)
    return d


def gran(ctx, x, lf, eye='happy', mouth='grin', f_=-1, wave=False, yarn_ball=True):
    r = 110 + 30 * math.sin(lf * 0.6) if wave else 60
    d = stand(ctx, GRAN, x, KG, P(eye=eye, mouth=mouth, lsh=30, lel=-60, rsh=r, rel=-40 if not wave else -20, head=-4), f_)
    if yarn_ball and not wave:
        yarn(ctx, d['front'][0], d['front'][1] - 10, 34, lf)
    return d


def room(ctx, lf, opn=0.0):
    W9.room(ctx, lf, opn=opn)


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    z = 1.08 + 0.04 * eio(pop(lf, 0, 54))
    ctx.save(); cam(ctx, 960, 1300, z, 0, shake_at(lf, [0], 6, 8), f)
    room(ctx, lf)
    g = gran(ctx, GRX, lf)
    for j in range(2):
        heart(ctx, g['head'][0] - 60 + j * 120, g['head'][1] - g['R'] * 1.5 - 14 * math.sin(lf * 0.2 + j), 22, PINK)
    d = kid_in_sweater(ctx, KIDX, lf, 'happy', 'grin', arms=(30, 30))
    sweat(ctx, d['head'][0] - d['R'] * 1.05, d['head'][1] - d['R'] * 0.4, lf, 0.9)
    twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.9, lf, 0.8)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"I... LOVE", "it!!\"", WHITE, t, 130, col2=RED, y=1420)


# ------------------------------------------------------------------ shot 2: macro -> Grandma leaves -> hide it
def knit_bg(ctx, col=KNIT):
    ctx.rectangle(-200, -200, W + 400, H + 400); setc(ctx, col); ctx.fill()
    for r in range(-2, 40):
        for c in range(-1, 18):
            x = c * 70 + (35 if r % 2 else 0); y = r * 56
            ctx.move_to(x - 22, y - 16); ctx.line_to(x, y + 14); ctx.line_to(x + 22, y - 16)
    setc(ctx, dark(col, 0.85)); ctx.set_line_width(6); ctx.stroke()


def macro(ctx, f, il):
    # il 0..70: big knitted reindeer, cross-eyed; 14 nose blinks *blink blink* ; 34 jingle notes ; 44 "...it SINGS?!"
    z = 1.0 + 0.08 * eio(il / 70)
    ctx.save(); cam(ctx, 540, 960, z, -3, shake_at(il, [44], 8, 10), f)
    knit_bg(ctx)
    ctx.save(); ctx.rectangle(-200, 300, W + 400, 70); ctx.clip(); knit_bg(ctx, WHITE); ctx.restore()
    zig(ctx, -100, W + 100, 335, 40, KNIT, 14)
    ctx.save(); ctx.rectangle(-200, 1540, W + 400, 70); ctx.clip(); knit_bg(ctx, YARN); ctx.restore()
    for (sx, sy) in ((170, 640), (900, 700), (150, 1340), (930, 1300)):
        sparkle(ctx, sx, sy, 44, WHITE)
    on = il >= 14 and (il // 5) % 2 == 0
    deer_face(ctx, 540, 1000, 210, 1.0 if on else 0.0)
    if il >= 34:
        for j in range(3):
            t = (il - 34 - j * 6) / 30
            if 0 < t < 1:
                nx = 540 + (j - 1) * 220 + 60 * math.sin(t * 6); ny = 1180 - t * 500
                ellipse(ctx, nx, ny, 26, 20, -0.3); fl(ctx, GOLD, 5)
                ctx.move_to(nx + 24, ny); ctx.line_to(nx + 24, ny - 80); setc(ctx, INK); ctx.set_line_width(7); ctx.stroke()
    ctx.restore()
    if 14 <= il < 44:
        label(ctx, "*blink blink*", 540, 560, 100, GOLD, -0.05, pop(il, 14, 18))
    if il >= 34:
        label(ctx, "*JINGLE~*", 540, 680, 90, YEL, 0.05, pop(il, 34, 37))
    if il >= 44:
        label(ctx, "\"...it SINGS?!\"", 540, 1420, 140, WHITE, -0.03, pop(il, 44, 48))


def leave(ctx, f, il):
    # il 0..70: Grandma waves "Bye, sweetie!" and walks out the door (0-24), door shuts 26 *CLICK*;
    #           30 kid whips the sweater off *FWIP!* -> 40 stuffs it in a present box, dog watching "...BYE, sweater."
    ctx.save(); cam(ctx, 1080, 1310, 0.98, 0, shake_at(il, [30], 6, 8), f)
    opn = pop(il, 0, 6) * (1 - pop(il, 22, 27))
    room(ctx, il, opn=opn)
    gx = lerp(GRX + 80, DOORX0 + 120, eio(pop(il, 8, 24)))
    if il < 25:
        s_ = math.sin(il * 0.8) if il > 8 else 0
        gran(ctx, gx, il, 'happy', 'grin', 1 if il > 8 else -1, wave=True)
    dog(ctx, 1150, GND + 20, 0.4, -1, il, sleep=False)
    if il < 30:
        d = kid_in_sweater(ctx, KIDX, il, 'happy' if il < 24 else 'normal', 'grin' if il < 24 else 'smile', arms=(30, 130 if il < 24 else 30))
    else:
        d = stand(ctx, KID, KIDX, KK, P(eye='smug', mouth='grin', lsh=120, lel=-30, rsh=120, rel=-30))
        u = eio(pop(il, 30, 44))
        bx, by = lerp(KIDX, 990, u), lerp(d['head'][1] - 120, FLOOR + 10, u) - 260 * math.sin(math.pi * u)
        if il < 46:
            ctx.save(); ctx.translate(bx, by); ctx.rotate(il * 0.5)
            ellipse(ctx, 0, 0, 90, 60); fl(ctx, KNIT, 6)
            zig(ctx, -80, 80, 0, 20, WHITE, 8)
            ctx.restore()
        # present box with lid popping
        lid = 1 - pop(il, 44, 50)
        rect_r(ctx, 900, FLOOR - 120, 180, 150, 10); fl(ctx, BLUE, 6)
        ctx.rectangle(980, FLOOR - 120, 20, 150); setc(ctx, GOLD); ctx.fill()
        ctx.save(); ctx.translate(990, FLOOR - 130 - 60 * lid); ctx.rotate(-0.4 * lid)
        rect_r(ctx, -100, -20, 200, 34, 8); fl(ctx, BLUE, 6)
        ctx.rectangle(-10, -20, 20, 34); setc(ctx, GOLD); ctx.fill()
        ctx.restore()
        if il >= 50:
            ctx.move_to(1080, FLOOR - 90); ctx.curve_to(1110, FLOOR - 90, 1100, FLOOR - 40, 1130, FLOOR - 40); setc(ctx, KNIT); ctx.set_line_width(22); ctx.stroke()
    ctx.restore()
    if il < 26:
        label2(ctx, "\"Bye,", "sweetie!\"", WHITE, pop(il, 2, 6), 110, col2=PINK, y=1420)
    elif il < 30:
        label(ctx, "*CLICK*", 540, 560, 100, GOLD, 0, pop(il, 26, 28))
    else:
        if il < 50:
            label(ctx, "*FWIP!*", 540, 560, 120, GOLD, -0.05, pop(il, 30, 33))
        if il >= 48:
            label2(ctx, "\"...BYE,", "sweater.\"", WHITE, pop(il, 48, 52), 120, col2=RED, y=1420)


def s2(ctx, f):
    il = f - 60
    if il < 70:
        macro(ctx, f, il)
    else:
        leave(ctx, f, il - 70)


# ------------------------------------------------------------------ shot 3: Grandma's back -> ZOOP
def box(ctx, open_=0.0):
    rect_r(ctx, 900, FLOOR - 120, 180, 150, 10); fl(ctx, BLUE, 6)
    ctx.rectangle(980, FLOOR - 120, 20, 150); setc(ctx, GOLD); ctx.fill()
    ctx.save(); ctx.translate(990 - 120 * open_, FLOOR - 130 - 60 * open_); ctx.rotate(-1.2 * open_)
    rect_r(ctx, -100, -20, 200, 34, 8); fl(ctx, BLUE, 6)
    ctx.rectangle(-10, -20, 20, 34); setc(ctx, GOLD); ctx.fill()
    ctx.restore()


def back_again(ctx, f, il):
    # il 0..140: 0 *DING-DONG!* door flies open, Grandma "I forgot my GLASSES!" ; 40 Dutch tilt: kid dives *ZOOP!*
    #            speed blur 40-58 ; 60 kid in the sweater again: upside-down deer + sleeve on head "Still... WEARING it!"
    #            96 Grandma melts with hearts "Aww! You LOVE it!"
    rot = 6 * eio(pop(il, 38, 44)) * (1 - eio(pop(il, 58, 64)))
    z = 1.0 if il < 60 else 1.0 + 0.06 * eio(pop(il, 60, 90))
    ctx.save(); cam(ctx, 1120, 1300, z, rot, shake_at(il, [0, 40, 60], 8, 12), f)
    room(ctx, il + 70, opn=eout(pop(il, 0, 6)))
    gx = lerp(DOORX0 + 130, GRX + 120, eio(pop(il, 10, 34)))
    melt = il >= 96
    g = gran(ctx, gx, il, 'happy' if melt or il < 10 else 'normal', 'grin' if melt else 'open', -1, yarn_ball=False)
    if melt:
        for j in range(3):
            heart(ctx, g['head'][0] - 110 + j * 110, g['head'][1] - g['R'] * 1.5 - 16 * math.sin(il * 0.25 + j) - (il - 96) * 1.2, 24 + 4 * j % 8, PINK)
    dog(ctx, 1150, GND + 20, 0.4, -1, il, sleep=False)
    if il < 40:
        box(ctx, 0)
        d = stand(ctx, KID, KIDX, KK, P(eye='shock', mouth='scream', lsh=150, lel=-20, rsh=150, rel=-20))
        sweat(ctx, d['head'][0] - d['R'] * 1.05, d['head'][1] - d['R'] * 0.4, il, 0.9)
    elif il < 60:
        u = (il - 40) / 20
        box(ctx, min(1, u * 3))
        for j in range(5):   # speed ghost trail kid <-> box
            x = lerp(KIDX, 990, 0.5 + 0.5 * math.sin(il * 1.4 + j * 0.6))
            ellipse(ctx, x, FLOOR - 220, 90, 160); setc(ctx, (1, 0.25, 0.35, 0.22 + 0.08 * j)); ctx.fill()
        for j in range(6):
            ctx.move_to(KIDX - 160, FLOOR - 420 + j * 60); ctx.line_to(1100, FLOOR - 420 + j * 60)
        setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(7); ctx.stroke()
    else:
        box(ctx, 1)
        d = kid_in_sweater(ctx, KIDX, il, 'happy', 'grin', flip=True, sleeve_head=True, arms=(40, 40))
        sweat(ctx, d['head'][0] - d['R'] * 1.05, d['head'][1] - d['R'] * 0.4, il, 0.9)
    ctx.restore()
    if il < 40:
        label(ctx, "*DING-DONG!*", 540, 560, 110, GOLD, -0.04, pop(il, 0, 3))
        label2(ctx, "\"I forgot", "my GLASSES!\"", WHITE, pop(il, 12, 16), 110, col2=PURPLE, y=1420)
    elif il < 60:
        label(ctx, "*ZOOP!*", 540, 600, 150, CYAN, -0.06, pop(il, 40, 43))
    elif il < 96:
        label2(ctx, "\"Still...", "WEARING it!\"", WHITE, pop(il, 62, 66), 120, col2=RED, y=1420)
    else:
        label2(ctx, "\"Aww! You", "LOVE it!\"", WHITE, pop(il, 96, 100), 120, col2=PINK, y=1420)


def s3(ctx, f):
    back_again(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: close-up -> twelve more
def closeup(ctx, f, il):
    # il 0..50: kid ECU in the collar, forced grin twitch "It's... my FAVOURITE."
    z = 1.0 + 0.05 * eio(il / 50)
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('ffd0dc')), (1, hx('fff0d8'))])); ctx.paint()
    ctx.save(); cam(ctx, 540, 960, z, 0, shake_at(il, [26], 6, 8), f)
    rays(ctx, 540, 900, 200, 1200, il * 0.03, (1, 1, 1), 0.3, 16)
    face(ctx, KID, P(eye='happy', mouth='grin'), 540, 880, 205)
    # knitted collar + shoulders across the bottom
    poly(ctx, [(160, 1110), (920, 1110), (1160, 1500), (1160, 2100), (-80, 2100), (-80, 1500)]); fl(ctx, KNIT, 8)
    ctx.save(); poly(ctx, [(160, 1110), (920, 1110), (1160, 1500), (1160, 2100), (-80, 2100), (-80, 1500)]); ctx.clip()
    zig(ctx, -80, 1160, 1250, 40, WHITE, 14)
    deer_face(ctx, 540, 1730, 70, 1.0 if (il // 5) % 2 else 0.0)
    ctx.restore()
    rect_r(ctx, 270, 1010, 540, 150, 60); fl(ctx, KNIT_D, 8)
    for i in range(10):
        ctx.move_to(310 + i * 51, 1030); ctx.line_to(310 + i * 51, 1140)
    setc(ctx, dark(KNIT_D, 0.85)); ctx.set_line_width(5); ctx.stroke()
    twitch(ctx, 790, 680, il, 1.6)
    sweat(ctx, 300, 700, il, 1.5)
    ctx.restore()
    label(ctx, "\"It's...", 540, 1400, 110, WHITE, -0.03, pop(il, 3, 7))
    if il >= 20:
        label(ctx, "my FAVOURITE.\"", 540, 1500, 120, RED, 0.03, pop(il, 20, 24))


def stack_col(i):
    return (KNIT, BLUE, YARN, PURPLE, ORANGE, PINK)[i % 6]


def tower(ctx, x, gy, n, lf, drop=1.0):
    for i in range(n):
        y = gy - 60 - i * 58 + (0 if i < n - 1 else -300 * (1 - drop))
        wob = 6 * math.sin(lf * 0.4 + i * 0.6) * (i / max(1, n))
        rect_r(ctx, x - 120 + wob, y - 28, 240, 60, 18); fl(ctx, stack_col(i), 5)
        ctx.save(); rect_r(ctx, x - 120 + wob, y - 28, 240, 60, 18); ctx.clip()
        zig(ctx, x - 130 + wob, x + 130 + wob, y + 2, 16, WHITE, 5)
        ctx.restore()


def twelve(ctx, f, il):
    # il 0..50: medium: Grandma "Good! I made you... TWELVE MORE!" 18 *THUMP!* tower of sweaters lands
    ctx.save(); cam(ctx, 1000, 1290, 1.0, 0, shake_at(il, [18], 12, 16), f)
    room(ctx, il + 210)
    g = gran(ctx, GRX, il, 'happy', 'grin', -1, yarn_ball=False)
    n = 12 if il >= 18 else 0
    if n:
        tower(ctx, 1460, FLOOR + 40, n, il, eout(pop(il, 18, 22)))
    d = kid_in_sweater(ctx, KIDX, il, 'shock' if il >= 18 else 'happy', 'scream' if il >= 18 else 'grin', flip=True, sleeve_head=True)
    ctx.restore()
    if il < 18:
        label2(ctx, "\"Good! I made", "you...\"", WHITE, pop(il, 0, 4), 110, col2=WHITE, y=1420)
    else:
        label(ctx, "*THUMP!*", 400, 560, 120, GOLD, -0.05, pop(il, 18, 21))
        label(ctx, "\"TWELVE MORE!\"", 540, 1440, 140, RED, 0.03, pop(il, 20, 24))


def s4(ctx, f):
    il = f - 340
    if il < 50:
        closeup(ctx, f, il)
    else:
        twelve(ctx, f, il - 50)


# ------------------------------------------------------------------ shot 5: Dad too -> photo
def dad_scene(ctx, f, il):
    # il 0..130: low-angle wide push: Dad shuffles in from the hall door in a GIANT matching sweater up to his nose,
    #            nose blinking; 50 "...help me." ; 70 the dog trots in, tiny matching sweater, wagging *wag wag* ; card p2 at 8
    z = 0.92 + 0.08 * eio(il / 130)
    ctx.save(); cam(ctx, 1060, 1290, z, 0, shake_at(il, [0], 6, 8), f)
    room(ctx, il + 260)
    g = gran(ctx, GRX - 160, il, 'happy', 'grin', 1, yarn_ball=True)
    d0 = kid_in_sweater(ctx, KIDX - 60, il, 'shock', 'open', flip=True, sleeve_head=True)
    dx = lerp(1800, 1360, eio(pop(il, 0, 30)))
    s_ = math.sin(il * 0.6) if il < 30 else 0
    on = (il // 6) % 2 == 0
    dd = stand(ctx, DAD, dx, KD, P(eye='glare' if il > 40 else 'normal', mouth='flat', lsh=25, lel=-20, rsh=25, rel=-20, lhip=14 * s_, rhip=-14 * s_), -1)
    sweater(ctx, dd, dx, KD, GND, 1.6, nose=1.0 if on else 0.0, droop=1.3, collar_up=0.9, lf=il)
    dgx = lerp(2100, 1150, eio(pop(il, 60, 90)))
    dog(ctx, dgx, GND + 60, 0.5, -1, il * 2, sleep=False)
    dog_sweater(ctx, dgx, GND + 60, 0.5, -1)
    ctx.restore()
    card(ctx, 'p2', il, 8)
    if il >= 46:
        label(ctx, "\"...help me.\"", 540, 1440, 130, WHITE, -0.03, pop(il, 46, 50))


def photo(ctx, f, il):
    # il 0..60: Grandma "Everybody SMILE!" 0 ; 20 *CLICK!* white flash -> polaroid freeze, kid twitch
    ctx.save(); cam(ctx, 1060, 1330, 0.95, 0, shake_at(il, [20], 8, 10), f)
    room(ctx, il + 390)
    frozen = il >= 20
    lf = 20 if frozen else il
    g = gran(ctx, 1340, lf, 'happy', 'grin', -1, yarn_ball=False)
    sweater(ctx, g, 1340, KG, GND, 1.2, lf=lf)
    dd = stand(ctx, DAD, 1070, KD, P(eye='glare', mouth='flat', lsh=25, lel=-20, rsh=25, rel=-20))
    sweater(ctx, dd, 1070, KD, GND, 1.6, nose=1.0, droop=1.3, collar_up=0.9, lf=lf)
    k = kid_in_sweater(ctx, 800, lf, 'happy', 'grin', flip=True, sleeve_head=True)
    dog(ctx, 690, GND + 70, 0.46, 1, lf * 2, sleep=False)
    dog_sweater(ctx, 690, GND + 70, 0.46, 1)
    if frozen:
        twitch(ctx, k['head'][0] + k['R'] * 0.9, k['head'][1] - k['R'] * 0.9, il, 0.8)
    ctx.restore()
    if frozen:   # polaroid frame
        ctx.rectangle(0, 0, W, 330); ctx.rectangle(0, 0, 70, H); ctx.rectangle(W - 70, 0, 70, H); ctx.rectangle(0, 1380, W, 600)
        setc(ctx, hx('fffdf6')); ctx.fill()
        ctx.rectangle(70, 330, W - 140, 1050); ink(ctx, 6); ctx.stroke()
        label(ctx, "FAMILY PHOTO!", 540, 1500, 100, BLUE, -0.02, pop(il, 22, 26))
        if il < 24:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 1 - (il - 20) / 4)); ctx.fill()
    else:
        label2(ctx, "\"Everybody", "SMILE!\"", WHITE, pop(il, 0, 4), 120, col2=GOLD, y=1420)
    if 20 <= il < 34:
        label(ctx, "*CLICK!*", 540, 520, 120, GOLD, -0.05, pop(il, 20, 23))


def s5(ctx, f):
    lf = f - 440
    if lf < 130:
        dad_scene(ctx, f, lf)
    elif lf < 190:
        photo(ctx, f, lf - 130)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (200, s3), (340, s4), (440, s5)]
CUTS = (60, 130, 200, 340, 390, 440, 570, 630)


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
                              "-i", "out/grandma_sweater_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
