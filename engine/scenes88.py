"""'Dad vs the gingerbread house' - original, general-audience comedy short, 22s.
Hook:   kitchen medium shot: red-faced Dad pressing two gingerbread walls together, icing oozing, house wobbling
        "HOLD... STILL...!!" + caption "DAD vs THE GINGERBREAD HOUSE:"
Beat 1: Dad slowly lets go "...DONE!" -> the roof slides off *SHLOOP* -> the walls fold flat *FLOMP!* "...WHAT?!"
Beat 2: Dutch-tilt speed montage: *SQUIRT! SQUIRT! SQUIRT!* icing everywhere, the house rebuilds itself "MORE... ICING!!"
Beat 3: kid snaps off the front door *SNAP!* *NOM!* -> Dad "That was the DOOR!!"
Turn:   low angle: last gumdrop *boop* -> sparkles "PERFECT." ; Dad ECU "...a MASTERPIECE."
Twist:  "PLOT TWIST: ONE TINY SPRINKLE." kid adds a star sprinkle on top *tink* -> *creeeak...* -> *KA-CRUNCH!!* crumbs
        Mom walks in with milk, she + kid munch the rubble "Mmm! Best house EVER!" -> Dad twitch "...my... HOUSE."
        Dad grabs a new box "FROM. THE. TOP." -> loop to the hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes65 import dog
import scenes84
from scenes84 import kitchen
from scenes87 import stuffed
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
GB = hx('c97a3a'); GB_D = hx('9a5526'); GB_L = hx('e39a55'); ICE = hx('fffaf2')
DAD = dict(doodle.DAD, shirt=hx('ff8a1f'), pants=hx('3d5a9e'))
DAD_R = dict(DAD, skin=hx('f07a6a'))
MOM = dict(doodle.MOM_G, shirt=hx('22b45a'), pants=hx('2f4a8a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('8a3cff'), pants=hx('3d7bff'), shoes=hx('ffc93c'))
N = 660
FLOOR = 1560
GND = 1590
KDAD, KMOM, KKID = 1.1, 1.02, 0.86
TX0, TX1, TY = 790, 1330, 1440
HX = 1056                                    # house centre x on the table
DADX, KIDX = 740, 1270
HS = 1.1
scenes84.TX0, scenes84.TX1, scenes84.TY = TX0, TX1, TY

CAPS = {'p1': [[("DAD vs ", OUT)], [("THE GINGERBREAD HOUSE:", GB_D)]],
        'p2': [[("PLOT TWIST:", RED)], [("ONE ", OUT), ("TINY SPRINKLE.", PINK)]]}
scenes13.CAPS = CAPS
card = _card13

GUMS = [(-70, -175, RED), (70, -175, GREEN), (-35, -215, GOLD), (35, -215, PINK), (0, -250, CYAN)]


# ------------------------------------------------------------------ props
def gumdrop(ctx, x, y, r, col):
    ctx.new_path(); ctx.move_to(x - r, y + r * 0.6); ctx.curve_to(x - r, y - r * 0.9, x + r, y - r * 0.9, x + r, y + r * 0.6)
    ctx.close_path(); fl(ctx, col, 3)
    ellipse(ctx, x - r * 0.35, y - r * 0.2, r * 0.2, r * 0.14); setc(ctx, (1, 1, 1, 0.7)); ctx.fill()


def drip_line(ctx, pts, w=14, col=ICE):
    """wavy icing piping along a polyline"""
    ctx.new_path(); ctx.move_to(*pts[0])
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        L_ = math.hypot(x1 - x0, y1 - y0); nseg = max(1, int(L_ / 22))
        for k in range(1, nseg + 1):
            t = k / nseg; px, py = lerp(x0, x1, t), lerp(y0, y1, t)
            ctx.line_to(px + 4 * math.sin(k * 2.1), py + 5 * math.cos(k * 2.1))
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    setc(ctx, INK); ctx.set_line_width(w + 6); ctx.stroke_preserve(); setc(ctx, col); ctx.set_line_width(w); ctx.stroke()


def blob(ctx, x, y, r, drip=0.0):
    ellipse(ctx, x, y, r, r * 0.8); fl(ctx, ICE, 3)
    if drip > 0:
        ctx.new_path(); ctx.move_to(x - r * 0.3, y); ctx.line_to(x - r * 0.25, y + r * 1.4 * drip)
        ctx.arc(x, y + r * 1.4 * drip, r * 0.25, math.pi, 0); ctx.line_to(x + r * 0.3, y); ctx.close_path(); fl(ctx, ICE, 3)


def roof_panel(ctx, side, gum=True, gum_on=None, star=False):
    """one roof slab, local coords: peak at (0,-262); side -1 left, +1 right"""
    pts = [(0, -268), (side * 152, -138), (side * 152, -112), (0, -238)]
    poly(ctx, pts); fl(ctx, GB, 5)
    for k in range(4):                                              # shingle scallops
        t = (k + 0.5) / 4
        ellipse(ctx, side * 152 * t, -253 + 130 * t + 6, 16, 9); setc(ctx, GB_L); ctx.fill()
    drip_line(ctx, [(side * 6, -262), (side * 150, -134)], 10)
    for k, (gx, gy, c) in enumerate(GUMS):
        if gum and (gum_on is None or k in gum_on) and gx * side > 0:
            gumdrop(ctx, gx, gy + 8, 15, c)


def house(ctx, x, base, s=1.0, lf=0, roof_slide=0.0, fall=0.0, icing=0.0, door=True, gum_on=None, star=0.0, wob=0.0, crumble=0.0):
    ctx.save(); ctx.translate(x, base); ctx.scale(s, s)
    if crumble < 1:
        ctx.push_group()
        ctx.save()
        ctx.rotate(wob * 0.06 * math.sin(lf * 1.3))
        ctx.scale(1, 1 - 0.86 * fall)
        # side wall peeking (3/4 view)
        poly(ctx, [(110, 0), (150, -24), (150, -170), (110, -150)]); fl(ctx, GB_D, 5)
        # front wall
        poly(ctx, [(-110, 0), (110, 0), (110, -150), (0, -250), (-110, -150)]); fl(ctx, GB, 6)
        for k in range(3):                                          # biscuit dots
            ellipse(ctx, -70 + 70 * k, -30, 4, 4); setc(ctx, GB_D); ctx.fill()
        # door
        rect_r(ctx, -34, -96, 68, 96, 30)
        if door:
            fl(ctx, GB_L, 4)
            ellipse(ctx, 18, -48, 5, 5); fl(ctx, GOLD, 2)
            drip_line(ctx, [(-34, -70), (0, -100), (34, -70)], 7)
        else:
            fl(ctx, hx('4a2416'), 4)
        # window
        rect_r(ctx, 40, -138, 46, 46, 6); fl(ctx, hx('ffe27a'), 4)
        ctx.move_to(63, -138); ctx.line_to(63, -92); ctx.move_to(40, -115); ctx.line_to(86, -115)
        setc(ctx, ICE); ctx.set_line_width(5); ctx.stroke()
        rect_r(ctx, -90, -138, 40, 40, 6); fl(ctx, hx('ffe27a'), 4)
        drip_line(ctx, [(-112, -6), (112, -6)], 9)
        # extra icing (montage)
        if icing > 0:
            rnd = random.Random(31)
            for k in range(int(14 * icing)):
                bx = rnd.uniform(-120, 140); by = rnd.uniform(-240, -10)
                blob(ctx, bx, by, rnd.uniform(14, 30) * min(1, icing * 1.5), drip=rnd.uniform(0.3, 1.0))
        ctx.restore()
        # roof slabs (slide off sideways and fall onto the table)
        for side in (-1, 1):
            ctx.save()
            u = clamp(roof_slide)
            ctx.translate(side * 200 * eio(u), 150 * u * u)
            ctx.rotate(side * 0.42 * eio(u))
            if fall > 0 and roof_slide <= 0:
                ctx.translate(0, 0)
            roof_panel(ctx, side, True, gum_on)
            ctx.restore()
        if star > 0:
            ss = 18 * eout(star)
            sy = -290 - 120 * (1 - eout(min(1, star * 1.4)))
            pts = []
            for k in range(10):
                a = -math.pi / 2 + k * math.pi / 5; rr = ss if k % 2 == 0 else ss * 0.45
                pts.append((rr * math.cos(a), sy + rr * math.sin(a)))
            poly(ctx, pts); fl(ctx, PINK, 3)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(1 - clamp(crumble * 1.6))
    if crumble > 0:                                                 # crumb pile
        rnd = random.Random(77)
        u = eout(crumble)
        for k in range(46):
            a = rnd.uniform(math.pi, 2 * math.pi); rr = rnd.uniform(0, 1) ** 0.6
            cx_ = math.cos(a) * 190 * rr * (0.6 + 0.4 * u); cy_ = math.sin(a) * 90 * rr * u - 6
            sz = rnd.uniform(10, 26)
            poly(ctx, [(cx_ - sz, cy_), (cx_ - sz * 0.4, cy_ - sz * 0.8), (cx_ + sz * 0.7, cy_ - sz * 0.5), (cx_ + sz, cy_ + sz * 0.2)])
            fl(ctx, (GB, GB_L, GB_D)[k % 3], 3)
        for k, (gx, gy, c) in enumerate(GUMS):
            gumdrop(ctx, -150 + 75 * k, -20 - 30 * (k % 2) * u, 14, c)
    ctx.restore()


def piping_bag(ctx, x, y, a=0.6, squeeze=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    sq = 1 - 0.18 * squeeze
    poly(ctx, [(-34 * sq, -50), (34 * sq, -50), (6, 40), (-6, 40)]); fl(ctx, hx('dff3ff'), 4)
    poly(ctx, [(-6, 40), (6, 40), (0, 62)]); fl(ctx, hx('c8ccd8'), 3)
    rect_r(ctx, -36, -64, 72, 18, 6); fl(ctx, RED, 3)
    ctx.restore()


def box(ctx, x, y, s=1.0, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rect_r(ctx, -110, -80, 220, 160, 10); fl(ctx, hx('ffcf5a'), 5)
    rect_r(ctx, -80, -50, 160, 100, 8); fl(ctx, WHITE, 3)
    poly(ctx, [(-40, 30), (40, 30), (40, -10), (0, -42), (-40, -10)]); fl(ctx, GB, 3)
    for k in range(3):
        sparkle(ctx, -60 + 60 * k, 60, 10, RED)
    ctx.restore()


def milk(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    poly(ctx, [(-22, -60), (22, -60), (18, 10), (-18, 10)]); fl(ctx, WHITE, 4)
    ctx.rectangle(-19, -40, 38, 46); setc(ctx, hx('f4f7ff')); ctx.fill()
    ctx.restore()


# ------------------------------------------------------------------ set
def table(ctx):
    scenes84.table(ctx, plate=False)


def set_(ctx, lf):
    kitchen(ctx, lf)
    dog(ctx, 1520, GND + 30, 0.42, -1, lf, sleep=True)


# ------------------------------------------------------------------ people
def stand(ctx, ch, x, k, p, f_=1):
    return draw(ctx, x, GND - 186 * k, k, f_, ch, p)


def kid_at(ctx, p, x=KIDX, f_=-1):
    return stand(ctx, KID, x, KKID, p, f_)


def dad_hold(ctx, lf, ch=DAD_R, x=DADX, eye='glare', mouth='scream', amp=1.0):
    sh = math.sin(lf * 1.7) * amp
    d = stand(ctx, ch, x, KDAD, P(eye=eye, mouth=mouth, torso=14, lsh=118 + 5 * sh, lel=-8, rsh=100 + 5 * sh, rel=-16, head=4))
    return d, sh


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf, new=False):
    z = 1.28 + 0.04 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, 1010, 1290, z, 0, 3 + shake_at(lf, [0], 6, 6), f)
    set_(ctx, lf)
    kid_at(ctx, P(eye='happy', mouth='open', lsh=40, lel=-120, rsh=30, rel=-130, head=-6))
    d, sh = dad_hold(ctx, lf)
    table(ctx)
    house(ctx, HX, TY - 4, HS, lf, icing=0.4, wob=1.0)
    # dad's hands pressing the left wall + roof
    for hk, (ox, oy) in (('back', (0, 0)), ('front', (0, 0))):
        pass
    for k in range(3):                                                 # strain lines
        ctx.move_to(d['head'][0] - d['R'] * 1.25, d['head'][1] - 40 + 40 * k); ctx.line_to(d['head'][0] - d['R'] * 1.6, d['head'][1] - 50 + 40 * k)
    ink(ctx, 5); ctx.stroke()
    sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.6, lf, 1.0)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"HOLD...", "STILL...!!\"", WHITE, t, 120, col2=RED, y=1440)


# ------------------------------------------------------------------ shot 2
def let_go(ctx, f, il):
    # il 0..70: 0-12 Dad eases hands off, 14 "...DONE!" arms up; 26 roof slides *SHLOOP*; 40 walls fold *FLOMP!*; 50 "...WHAT?!"
    ctx.save(); cam(ctx, 1010, 1290, 1.26, 0, shake_at(il, [40], 8, 10), f)
    set_(ctx, il)
    kid_at(ctx, P(eye='happy' if il < 40 else 'shock', mouth='smile' if il < 40 else 'open', lsh=40, lel=-120, rsh=30, rel=-130))
    u = eio(pop(il, 0, 14))
    happy = 12 <= il < 40
    d = stand(ctx, DAD if il < 40 else DAD_R, DADX, KDAD,
              P(eye='happy' if happy else ('shock' if il >= 40 else 'normal'), mouth='grin' if happy else ('scream' if il >= 46 else 'flat'),
                torso=lerp(14, 0, u), lsh=lerp(88, 160, u) if il >= 12 else lerp(88, 70, u), lel=-10, rsh=lerp(100, 165, u) if il >= 12 else lerp(100, 80, u), rel=-10))
    table(ctx)
    house(ctx, HX, TY - 4, HS, il, roof_slide=pop(il, 26, 38), fall=eout(pop(il, 40, 46)), wob=0.5 if il < 26 else 0)
    if 12 <= il < 26:
        for k in range(3):
            sparkle(ctx, HX - 120 + 120 * k, TY - 350 - 20 * (k % 2), 16 + 4 * math.sin(il * 0.6 + k), GOLD)
    ctx.restore()
    if il < 26:
        label(ctx, "\"...DONE!\"", 540, 1440, 130, GREEN, -0.03, pop(il, 12, 15))
    elif il < 40:
        label(ctx, "*SHLOOP*", 540, 640, 110, GB_D, 0.05, pop(il, 26, 29))
    elif il < 50:
        label(ctx, "*FLOMP!*", 540, 640, 130, GB_D, -0.05, pop(il, 40, 43))
    else:
        label(ctx, "*FLOMP!*", 540, 640, 130, GB_D, -0.05, 1)
        label(ctx, "\"...WHAT?!\"", 540, 1440, 140, RED, -0.03, pop(il, 50, 53))


SQ = [8, 22, 36, 50]


def montage(ctx, f, il):
    # il 0..80 Dutch tilt: Dad squirts icing like crazy, the house rebuilds itself, 66 standing *DING*
    rot = -8 if il < 64 else lerp(-8, 0, eio(pop(il, 64, 70)))
    ctx.save(); cam(ctx, 1010, 1280, lerp(1.25, 1.4, eio(il / 80)), rot, shake_at(il, SQ, 5, 6), f)
    set_(ctx, il)
    kid_at(ctx, P(eye='shock', mouth='open', lsh=40, lel=-120, rsh=30, rel=-130))
    fall = 1 - eio(pop(il, 6, 60))
    rs = 1 - eio(pop(il, 20, 62))
    if il < 64:
        for g in (2, 1, 0):
            ctx.push_group()
            w = math.sin((il - g) * 2.3)
            d = stand(ctx, DAD_R, DADX + 16 * w, KDAD, P(eye='glare', mouth='scream', torso=10 + 6 * w, lsh=70 + 30 * w, lel=-20, rsh=95 - 20 * w, rel=-30, head=4 * w))
            ctx.pop_group_to_source(); ctx.paint_with_alpha(1.0 if g == 0 else 0.25)
        bx, by = d['front']
    else:
        d = stand(ctx, DAD, DADX, KDAD, P(eye='happy', mouth='grin', torso=0, lsh=40, lel=-10, rsh=100, rel=-40))
        bx, by = d['front']
    table(ctx)
    house(ctx, HX, TY - 4, HS, il, roof_slide=rs, fall=fall, icing=min(1, il / 50), wob=0.3)
    if il < 64:
        piping_bag(ctx, bx + 10, by - 30, 2.2 + 0.2 * math.sin(il * 2.3), squeeze=(il % 6) / 6)
        for j, p_ in enumerate(SQ):                                     # icing jets
            u = pop(il, p_, p_ + 6)
            if 0 < u < 1:
                tx_, ty_ = HX - 90 + 60 * j, TY - 140 - 50 * (j % 2)
                ctx.move_to(bx + 50, by - 10); ctx.line_to(lerp(bx + 50, tx_, u), lerp(by - 10, ty_, u))
                ctx.set_line_cap(cairo.LINE_CAP_ROUND); setc(ctx, INK); ctx.set_line_width(20); ctx.stroke_preserve(); setc(ctx, ICE); ctx.set_line_width(14); ctx.stroke()
    else:
        piping_bag(ctx, bx, by - 10, 0.3)
        for k in range(3):
            sparkle(ctx, HX - 130 + 130 * k, TY - 360 - 20 * (k % 2), 18 + 5 * math.sin(il * 0.6 + k), GOLD)
    ctx.restore()
    if il < 64:
        for j, p_ in enumerate(SQ):
            if il < p_ + 12:
                label(ctx, "*SQUIRT!*", 540 + (-180, 170, -60, 120)[j], (580, 690, 800, 600)[j], 96, hx('5fb8ef'), (-0.08, 0.07, -0.03, 0.05)[j], pop(il, p_, p_ + 3))
        label2(ctx, "\"MORE...", "ICING!!\"", WHITE, pop(il, 4, 8), 120, col2=hx('5fb8ef'), y=1440)
    else:
        label(ctx, "*DING!*", 540, 640, 120, GOLD, -0.04, pop(il, 66, 69))


def door_snack(ctx, f, il):
    # il 0..60: kid leans over, snaps off the door *SNAP!* (10), *NOM!* (18) -> Dad "That was the DOOR!!" (30)
    ctx.save(); cam(ctx, 1080, 1300, 1.3, 0, shake_at(il, [10, 30], 6, 6), f)
    set_(ctx, il)
    reach = eio(pop(il, 0, 10)) * (1 - eio(pop(il, 12, 20)))
    k = kid_at(ctx, P(eye='happy', mouth='open' if il < 18 else 'flat', torso=-18 * reach, lsh=40, lel=-100,
                      rsh=lerp(60, 100, reach) if il < 12 else 160, rel=lerp(-100, -10, reach) if il < 12 else -150, head=-6), x=KIDX - 30 * reach)
    d = stand(ctx, DAD if il < 30 else DAD_R, DADX, KDAD, P(eye='happy' if il < 22 else 'shock', mouth='smile' if il < 22 else 'scream', torso=0,
                                                         lsh=40, lel=-10, rsh=60 if il < 30 else 150, rel=-30 if il < 30 else -40))
    table(ctx)
    house(ctx, HX, TY - 4, HS, il, icing=1.0, door=il < 10)
    if 10 <= il < 18:
        rect_r(ctx, k['front'][0] - 22, k['front'][1] - 50, 44, 62, 20); fl(ctx, GB_L, 3)
    if il >= 18:
        stuffed(ctx, k, 0.6, KID, f_=-1)
    ctx.restore()
    if il < 18:
        label(ctx, "*SNAP!*", 540, 640, 120, GB_D, -0.05, pop(il, 10, 13))
    elif il < 30:
        label(ctx, "*NOM!*", 540, 640, 130, GB_D, 0.05, pop(il, 18, 21))
    else:
        label2(ctx, "\"That was", "the DOOR!!\"", WHITE, pop(il, 30, 33), 120, col2=RED, y=1440)


def s2(ctx, f):
    lf = f - 54
    if lf < 70:
        let_go(ctx, f, lf)
    elif lf < 150:
        montage(ctx, f, lf - 70)
    else:
        door_snack(ctx, f, lf - 150)


# ------------------------------------------------------------------ shot 3: last gumdrop (low angle)
def last_gum(ctx, f, il):
    # il 0..56: low angle across the table: Dad's hand puts the last gumdrop on top *boop* (14) -> sparkles "PERFECT." (24)
    ctx.save(); cam(ctx, 1020, 1250, lerp(1.45, 1.55, eio(il / 56)), 0, shake_at(il, [14], 5, 5), f)
    set_(ctx, il)
    d = stand(ctx, DAD, DADX + 60, KDAD, P(eye='normal' if il < 14 else 'happy', mouth='flat' if il < 14 else 'grin', torso=10,
                                           lsh=40, lel=-10, rsh=lerp(120, 90, pop(il, 0, 14)), rel=lerp(-60, -20, pop(il, 0, 14)), head=-4))
    table(ctx)
    gum = {0, 1, 2, 3} if il < 14 else None
    house(ctx, HX + 10, TY - 4, HS * 1.04, il, icing=1.0, door=False, gum_on=gum)
    if il < 14:
        gumdrop(ctx, d['front'][0] + 10, d['front'][1] - 18, 17, CYAN)
    else:
        for k in range(5):
            sparkle(ctx, HX + 20 + 170 * math.cos(il * 0.08 + k * 1.25), TY - 190 + 130 * math.sin(il * 0.08 + k * 1.25), 16 + 5 * math.sin(il * 0.5 + k), GOLD)
    ctx.restore()
    if il < 24:
        label(ctx, "*boop*", 540, 640, 110, CYAN, -0.05, pop(il, 14, 17))
    else:
        label(ctx, "\"PERFECT.\"", 540, 1440, 140, GOLD, -0.03, pop(il, 24, 27))


def s3(ctx, f):
    last_gum(ctx, f, f - 264)


# ------------------------------------------------------------------ shot 4: the one close-up
def ecu(ctx, f, il):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eio(il / 80), 0, 2 + shake_at(il, [0], 6, 8), f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('fff0c4')); ctx.fill()
    rays(ctx, 540, 900, 240, 1500, il * 0.02, col=(1, 1, 1), a=0.4, n=16)
    face(ctx, DAD, P(eye='happy' if il < 40 else 'smug', mouth='grin'), 540, 940, 200, 0.0)
    for (ox, oy, r) in ((-120, 150, 16), (70, 170, 12), (150, -60, 10), (-160, -120, 9)):         # icing smudges
        blob(ctx, 540 + ox, 940 + oy, r)
    for k in range(5):
        gumdrop(ctx, 540 + 330 * math.cos(il * 0.04 + k * 1.25), 940 + 300 * math.sin(il * 0.04 + k * 1.25), 24, (RED, GREEN, GOLD, PINK, CYAN)[k])
    ctx.restore()
    label2(ctx, "\"...a", "MASTERPIECE.\"", WHITE, pop(il, 8, 12), 120, col2=GOLD, y=1440)


def s4(ctx, f):
    ecu(ctx, f, f - 320)


# ------------------------------------------------------------------ shot 5: twist -> loop
def sprinkle(ctx, f, il):
    # il 0..100: kid tiptoes, places a tiny star on top *tink* (20) -> *creeeak...* (36) wobble -> Dad "...don't." (44) -> *KA-CRUNCH!!* (62)
    ctx.save(); cam(ctx, 1050, 1290, lerp(1.22, 1.32, eio(il / 60)) if il < 62 else 1.25, 0, shake_at(il, [62], 12, 16), f)
    set_(ctx, il)
    reach = eio(pop(il, 0, 10)) * (1 - eio(pop(il, 22, 32)))
    k = kid_at(ctx, P(eye='happy' if il < 62 else 'shock', mouth='smile' if il < 62 else 'open', torso=-16 * reach, lsh=40, lel=-100,
                      rsh=lerp(60, 165, reach), rel=lerp(-100, -10, reach), head=-12), x=KIDX - 30 * reach)
    d = stand(ctx, DAD if il < 62 else DAD_R, DADX, KDAD,
              P(eye='smug' if il < 36 else 'shock', mouth='grin' if il < 36 else ('flat' if il < 62 else 'scream'), torso=0,
                lsh=40, lel=-10, rsh=60 if il < 36 else 120, rel=-30 if il < 36 else -10))
    table(ctx)
    wob = 0 if il < 36 else 1.6
    house(ctx, HX, TY - 4, HS, il * 2, icing=1.0, door=False, star=1.0 if il >= 20 else 0.0, wob=wob, crumble=pop(il, 62, 70))
    if il < 20:                                                    # the star sprinkle flies from the kid's hand to the roof
        u = eio(pop(il, 10, 20))
        sx0, sy0 = k['front']; sx1, sy1 = HX, TY - 4 - 290 * HS
        sx_ = lerp(sx0, sx1, u); sy_ = lerp(sy0, sy1, u) - 160 * 4 * u * (1 - u)
        pts = []
        for j in range(10):
            a_ = -math.pi / 2 + j * math.pi / 5 + il * 0.4; rr = 20 if j % 2 == 0 else 9
            pts.append((sx_ + rr * math.cos(a_), sy_ + rr * math.sin(a_)))
        poly(ctx, pts); fl(ctx, PINK, 3)
    if il >= 62:
        for j in range(8):                                             # flying crumbs
            u = pop(il, 62, 74)
            a = -math.pi * (0.1 + 0.8 * j / 7)
            ctx.save(); ctx.translate(HX + math.cos(a) * 300 * u, TY - 100 + math.sin(a) * 260 * u + 300 * u * u)
            ctx.rotate(il * 0.3 + j); poly(ctx, [(-12, 0), (-4, -12), (10, -6), (12, 6)]); fl(ctx, GB, 3); ctx.restore()
        twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.9, il, 0.8)
    ctx.restore()
    card(ctx, 'p2', il, 0, 60)
    if il < 36:
        label2(ctx, "\"...and a", "STAR!\"", WHITE, pop(il, 14, 18), 120, col2=PINK, y=1440)
        label(ctx, "*tink*", 540, 760, 90, PINK, 0.05, pop(il, 20, 23)) if il < 36 else None
    elif il < 62:
        label(ctx, "*creeeak...*", 540, 760, 100, GB_D, -0.04, pop(il, 36, 39))
        label(ctx, "\"...don't.\"", 540, 1440, 130, WHITE, -0.03, pop(il, 44, 47))
    else:
        label(ctx, "*KA-CRUNCH!!*", 540, 640, 120, RED, -0.05, pop(il, 62, 65))


def munch_scene(ctx, f, il):
    # il 0..60: Mom walks in with milk; she + kid munch the rubble "Mmm! Best house EVER!"; Dad twitch "...my... HOUSE."
    ctx.save(); cam(ctx, 1070, 1300, 1.2, 0, 0, f)
    set_(ctx, il)
    k = kid_at(ctx, P(eye='happy', mouth='flat', lsh=40, lel=-100, rsh=150 + 10 * math.sin(il * 0.9), rel=-160), x=KIDX - 40)
    stuffed(ctx, k, 0.6, KID, f_=-1)
    mx = lerp(1700, 1420, eout(pop(il, 0, 14)))
    m = stand(ctx, MOM, mx, KMOM, P(eye='happy', mouth='flat' if il > 16 else 'smile', lsh=60, lel=-60, rsh=150 + 10 * math.sin(il * 0.9 + 1), rel=-160), f_=-1)
    milk(ctx, m['back'][0], m['back'][1] + 10, 0.9)
    if il > 16:
        stuffed(ctx, m, 0.5, MOM, f_=-1)
    d = stand(ctx, DAD_R, DADX, KDAD, P(eye='shock', mouth='flat', lsh=20, lel=-10, rsh=25, rel=-10))
    twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 0.9, il, 0.8)
    table(ctx)
    house(ctx, HX, TY - 4, HS, il, crumble=1.0)
    ctx.restore()
    label(ctx, "*munch munch*", 540, 640, 96, GB_D, 0.04, pop(il, 4, 7))
    if il < 32:
        label2(ctx, "\"Mmm! Best", "house EVER!\"", WHITE, pop(il, 8, 12), 110, col2=GREEN, y=1440)
    else:
        label2(ctx, "\"...my...", "HOUSE.\"", WHITE, pop(il, 32, 36), 130, col2=RED, y=1440)


def top_again(ctx, f, il):
    # il 0..70: Dad slams a new kit on the table *THUMP* (6), grabs two walls "FROM. THE. TOP." push-in
    ctx.save(); cam(ctx, 980, 1290, lerp(1.25, 1.45, eio(il / 70)), 0, shake_at(il, [6], 8, 10), f)
    set_(ctx, il)
    k = kid_at(ctx, P(eye='happy', mouth='flat', lsh=40, lel=-100, rsh=150, rel=-160), x=KIDX - 40)
    stuffed(ctx, k, 0.6, KID, f_=-1)
    d = stand(ctx, DAD_R, DADX, KDAD, P(eye='glare', mouth='scream' if il > 20 else 'flat', torso=10, lsh=80, lel=-10, rsh=95, rel=-20, head=4))
    table(ctx)
    u = eout(pop(il, 0, 6))
    box(ctx, HX, lerp(TY - 500, TY - 84, u), 1.0, 0.08 * (1 - u))
    sweat(ctx, d['head'][0] - d['R'] * 0.9, d['head'][1] - d['R'] * 0.6, il, 1.0)
    ctx.restore()
    label(ctx, "*THUMP!*", 540, 640, 120, GB_D, -0.05, pop(il, 6, 9))
    label2(ctx, "\"FROM.", "THE. TOP.\"", WHITE, pop(il, 20, 24), 130, col2=RED, y=1440)


def s5(ctx, f):
    lf = f - 400
    if lf < 100:
        sprinkle(ctx, f, lf)
    elif lf < 160:
        munch_scene(ctx, f, lf - 100)
    elif lf < 230:
        top_again(ctx, f, lf - 160)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (54, s2), (264, s3), (320, s4), (400, s5)]
CUTS = (54, 124, 204, 264, 320, 400, 500, 560, 630)


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
                              "-i", "out/gingerbread_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
