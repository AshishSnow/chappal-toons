"""'Dad's Sneeze' - original, general-audience comedy short, 22s.
Hook: Dad ECU, head tipping back, nostrils flaring "AHH... AHHHH..." + caption "Every Dad's sneeze:"
Beat 1: living room wide: build-up... "CHOOO!!" -> card tower explodes, Mom's hair blown back, dog slides away, frame tilts.
        Mom ECU, hair sideways, empty cup: "...bless you."
Beat 2: "3 houses away:" neighbour in his garden, hose water bent sideways, hat gone: "BLESS YOU!!"
Beat 3: "Mom's sneeze:" tiny "*tchoo!*" + sparkles -> "Awww... SO CUTE!"
Twist: "The KID's sneeze:" kid ECU "ah... ahh..." -> parents "UH-OH." -> house exterior, ROOF launches into the sky
 -> roofless living room, Dad teary-proud "That's MY boy!!" -> Mom ECU under open sky "...who's paying for the ROOF?"
End: Dad's nose twitches AGAIN "AHH..." -> Mom + kid grab the sofa "NOT AGAIN!!" -> Dad ECU loop."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos, _SCR
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes65 import dog
from scenes8 import sit
import scenes13
from scenes13 import card as _card13
import random


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


DAD = dict(doodle.DAD, shirt=hx('3d7bff'), pants=hx('2a3a6a'))
MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'))
BOY = dict(doodle.BOY, hood=False, shades=False, shirt=hx('22b45a'))
NB = dict(doodle.NEIGHBOR, shirt=hx('ff8a1f'))
N = 660
RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); TEAL = hx('19b5a5'); WHITE = (1, 1, 1); SKY = hx('8fd8ff')
FLOOR = 1460
SEAT = 1270

CAPS = {
    'p1': [[("Every ", OUT), ("DAD'S", BLUE), (" sneeze:", OUT)]],
    'p3': [[("Meanwhile,", OUT)], [("3 houses away:", ORANGE)]],
    'p4': [[("MOM'S", PINK), (" sneeze:", OUT)]],
    'p5': [[("Then the ", OUT), ("KID'S", GREEN), (" sneeze:", OUT)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ fx
def wind(ctx, x0, y0, x1, y1, lf, n=10, a=0.8, w=14, seed=3):
    """white gust streaks flowing in the box, moving to +x"""
    rnd = random.Random(seed)
    for k in range(n):
        y = rnd.uniform(y0, y1); L = rnd.uniform(160, 380)
        ph = ((lf * 70 + rnd.uniform(0, 2000)) % (x1 - x0 + L)) + x0 - L
        ctx.new_path(); ctx.move_to(ph, y); ctx.curve_to(ph + L * 0.4, y - 14, ph + L * 0.7, y + 14, ph + L, y)
        setc(ctx, (1, 1, 1, a)); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()


def blown_hair(ctx, cx, cy, R, col, d=1, amt=1.0):
    """hair streaming sideways behind a head (draw BEFORE the head); d=+1 blows to the right"""
    if amt <= 0:
        return
    for k, (dy, ln) in enumerate(((-0.55, 1.5), (-0.25, 1.9), (0.05, 1.6), (0.3, 1.2))):
        L = R * ln * amt
        ctx.new_path(); ctx.move_to(cx, cy + (dy - 0.18) * R)
        ctx.curve_to(cx + d * L * 0.5, cy + (dy - 0.3) * R, cx + d * L * 0.9, cy + (dy - 0.05) * R, cx + d * (R * 0.6 + L), cy + dy * R + 0.1 * R * math.sin(k))
        ctx.curve_to(cx + d * L * 0.8, cy + (dy + 0.22) * R, cx + d * L * 0.4, cy + (dy + 0.16) * R, cx, cy + (dy + 0.18) * R)
        ctx.close_path(); fl(ctx, col, max(4, R * 0.03))


def nostrils(ctx, cx, cy, R, flare, rot=0.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot)
    return
    for sx in (0.02, 0.2):
        ellipse(ctx, R * sx, R * 0.24, R * (0.045 + 0.05 * flare), R * (0.03 + 0.035 * flare)); setc(ctx, hx('5a2a20')); ctx.fill()
    ctx.restore()


def cards(ctx, x, y, lf, blown=-1):
    """card tower on the table; blown = frame index when it explodes"""
    if blown < 0 or lf < blown:
        for row in range(4):
            for c in range(4 - row):
                bx = x - (3 - row) * 34 + c * 68 - 68
                for s in (-1, 1):
                    poly(ctx, [(bx + 34, y - row * 80 - 80), (bx + 34 + s * 26, y - row * 80)])
                    ink(ctx, 7); ctx.stroke()
        return
    rnd = random.Random(5)
    t = (lf - blown)
    for k in range(10):
        px = x + rnd.uniform(-60, 60) + t * rnd.uniform(30, 55); py = y - 150 - t * rnd.uniform(-8, 14) + 0.6 * t * t * 0.3
        ctx.save(); ctx.translate(px, py); ctx.rotate(t * rnd.uniform(0.2, 0.5))
        rect_r(ctx, -28, -40, 56, 80, 8); fl(ctx, WHITE, 5)
        ctx.new_path(); ctx.arc(0, 0, 12, 0, 2 * math.pi); setc(ctx, RED); ctx.fill()
        ctx.restore()


def frame_pic(ctx, x, y, tilt):
    ctx.save(); ctx.translate(x, y); ctx.rotate(tilt)
    ctx.move_to(0, -90); ctx.line_to(-60, -20); ctx.move_to(0, -90); ctx.line_to(60, -20); ink(ctx, 5); ctx.stroke()
    rect_r(ctx, -110, -20, 220, 160, 10); fl(ctx, GOLD, 8)
    ctx.rectangle(-86, 4, 172, 112); setc(ctx, SKY); ctx.fill()
    poly(ctx, [(-86, 116), (-30, 40), (20, 116)]); setc(ctx, GREEN); ctx.fill()
    poly(ctx, [(0, 116), (40, 60), (86, 116)]); setc(ctx, TEAL); ctx.fill()
    ctx.restore()


def room(ctx, lf, roof=True):
    wall = hx('ffd98a')
    if roof:
        ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, wall); ctx.fill()
        for i in range(-30, 40):
            ctx.rectangle(i * 120, -3000, 46, 6000); setc(ctx, dark(wall, 0.95)); ctx.fill()
    else:
        ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, SKY); ctx.fill()
        for k, (x, y) in enumerate(((200, 330), (820, 260), (560, 520))):
            ellipse(ctx, x + (lf * 1.5) % 200, y, 120, 46); setc(ctx, WHITE); ctx.fill(); ellipse(ctx, x + 60 + (lf * 1.5) % 200, y - 30, 70, 50); ctx.fill()
        # broken wall top edge
        pts = [(-3000, 760)] + [(i * 90, 720 + (40 if i % 2 else -10)) for i in range(-2, 16)] + [(4000, 760), (4000, 4000), (-3000, 4000)]
        poly(ctx, pts); setc(ctx, wall); ctx.fill()
        poly(ctx, [(i * 90, 720 + (40 if i % 2 else -10)) for i in range(-2, 16)]); ink(ctx, 7); ctx.stroke()
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('b97a4a')); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()


def sofa_back(ctx, x0=60):
    rect_r(ctx, x0, 960, 560, 340, 50); fl(ctx, hx('8a3cff'), 9)
    rect_r(ctx, x0 + 30, 1000, 250, 240, 40); fl(ctx, hx('a46bff'), 7)
    rect_r(ctx, x0 + 290, 1000, 240, 240, 40); fl(ctx, hx('a46bff'), 7)


def sofa_front(ctx, x0=60):
    rect_r(ctx, x0, SEAT - 10, 560, 190, 30); fl(ctx, hx('8a3cff'), 9)
    for x in (x0 - 50, x0 + 500):
        rect_r(ctx, x, 1100, 110, 340, 50); fl(ctx, hx('6f2ad6'), 9)


def table(ctx, x=780):
    rect_r(ctx, x - 190, 1300, 380, 36, 10); fl(ctx, hx('c96a2a'), 7)
    for lx in (x - 160, x + 140):
        ctx.rectangle(lx, 1336, 22, FLOOR - 1336); fl(ctx, hx('8a4a1a'), 5)


def cup(ctx, x, y, a=0.0, s=1.0, full=True):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-40, -50), (40, -50), (30, 40), (-30, 40)]); fl(ctx, WHITE, 6)
    ctx.new_path(); ctx.arc(48, -6, 22, -1.4, 1.4); ink(ctx, 7); ctx.stroke()
    if full:
        ellipse(ctx, 0, -44, 36, 8); setc(ctx, hx('8a4a1a')); ctx.fill()
    ctx.restore()


def house(ctx, x, y, lf, roof_t=-1, sway=0.0):
    """exterior house; roof_t = frames since the roof launched (-1 = on)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(sway)
    ctx.rectangle(-300, -420, 600, 420); fl(ctx, hx('ffd98a'), 9)
    for wx in (-170, 90):
        ctx.rectangle(wx, -340, 120, 120); fl(ctx, SKY, 7)
        ctx.move_to(wx + 60, -340); ctx.line_to(wx + 60, -220); ctx.move_to(wx, -280); ctx.line_to(wx + 120, -280); ink(ctx, 5); ctx.stroke()
    ctx.rectangle(-50, -180, 100, 180); fl(ctx, hx('c96a2a'), 7)
    ctx.restore()
    if roof_t < 0:
        rx, ry, ra = x, y - 420, sway
    else:
        t = roof_t
        rx = x + 18 * t; ry = y - 420 - 60 * t - 1.5 * t * t; ra = 0.09 * t
    ctx.save(); ctx.translate(rx, ry); ctx.rotate(ra)
    poly(ctx, [(-360, 0), (0, -300), (360, 0)]); fl(ctx, RED, 9)
    ctx.rectangle(140, -240, 70, 140); fl(ctx, hx('a8642e'), 7)
    ctx.restore()


def tree(ctx, x, y, lean=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    poly(ctx, [(-24, 0), (24, 0), (16 + lean * 60, -260), (-16 + lean * 60, -260)]); fl(ctx, hx('8a4a1a'), 7)
    for dx, dy, r in ((0, -330, 130), (-90, -260, 90), (90, -270, 95)):
        ctx.new_path(); ctx.arc(dx + lean * 200, dy, r, 0, 2 * math.pi); fl(ctx, hx('3fae54'), 7)
    ctx.restore()


def outdoor(ctx, lf):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, SKY); ctx.fill()
    for k, (x, y) in enumerate(((180, 420), (760, 330))):
        ellipse(ctx, x, y, 120, 46); setc(ctx, WHITE); ctx.fill()
    ctx.rectangle(-3000, 1350, 7000, 3000); setc(ctx, hx('5cc96a')); ctx.fill()
    ctx.move_to(-3000, 1350); ctx.line_to(4000, 1350); ink(ctx, 7); ctx.stroke()


# ------------------------------------------------------------------ close-ups
def dad_ecu(ctx, f, lf, bg, build=1.0, z0=1.0, shake=0, eye='closed', mouth='open', blown=0.0, sweat_=False):
    ctx.save(); cam(ctx, 540, 960, z0, 0, shake, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    rays(ctx, 540, 900, 260, 1700, lf * 0.03, col=(1, 1, 1), a=0.22, n=18)
    rot = -0.22 * build + 0.02 * math.sin(lf * 0.9) * build
    cx, cy, R = 540, 900 - 30 * build, 300
    blown_hair(ctx, cx, cy, R, DAD['hair'], -1, blown)
    face(ctx, DAD, P(eye=eye, mouth=mouth), cx, cy, R, rot)
    nostrils(ctx, cx, cy, R, build * (0.6 + 0.4 * math.sin(lf * 0.8)), rot)
    if sweat_:
        sweat(ctx, cx + 0.8 * R, cy - 0.4 * R, lf, 1.3)
    ctx.restore()


def mom_ecu(ctx, f, lf, bg, eye='normal', mouth='flat', z0=1.0, shake=0, blown=0.0, sky=False, tw=False, cup_=True):
    ctx.save(); cam(ctx, 540, 960, z0, 0, shake, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    if sky:
        for k, (x, y) in enumerate(((220, 380), (860, 300))):
            ellipse(ctx, x + lf, y, 130, 50); setc(ctx, WHITE); ctx.fill()
    else:
        rays(ctx, 540, 900, 260, 1700, lf * 0.02, col=(1, 1, 1), a=0.25, n=18)
    cx, cy, R = 540, 900, 290
    blown_hair(ctx, cx, cy, R, MOM['hair'], 1, blown)
    face(ctx, MOM, P(eye=eye, mouth=mouth), cx, cy, R, 0.02 * math.sin(lf * 0.3))
    if tw:
        twitch(ctx, cx + 0.6 * R, cy - 0.5 * R, lf, 1.3)
    if cup_:
        cup(ctx, cx - 300, cy + 430, -0.6 if blown else 0, 1.6, not blown)
    ctx.restore()
    return cx, cy, R


def kid_ecu(ctx, f, lf, bg, build=1.0, z0=1.0, shake=0):
    ctx.save(); cam(ctx, 540, 960, z0, 0, shake, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    rays(ctx, 540, 900, 260, 1700, lf * 0.03, col=(1, 1, 1), a=0.22, n=18)
    rot = -0.2 * build + 0.03 * math.sin(lf * 1.1) * build
    cx, cy, R = 540, 900, 300
    face(ctx, BOY, P(eye='closed', mouth='open'), cx, cy, R, rot)
    nostrils(ctx, cx, cy, R, build * (0.6 + 0.4 * math.sin(lf * 0.9)), rot)
    ctx.restore()


# ------------------------------------------------------------------ shots
def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    b = 0.7 + 0.3 * eio(pop(lf, 0, 50))
    dad_ecu(ctx, f, lf, ORANGE, b, z0=1.0 + 0.08 * eio(pop(lf, 0, 54)), shake=3 + lf // 10)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    label(ctx, "\"AHH...\"", 330, 1350, 110, WHITE, -0.08, 1 if lf == f else pop(lf, 0, 3))
    if lf >= 22:
        label(ctx, "\"AHHHHH...\"", 560, 1490, 130, YEL, 0.05, pop(lf, 22, 26))


def living_wide(ctx, f, lf, boom=-1, z=1.0, cx=540, cy=1080, sh=0, roof=True, dad_p=None, kid_p=None, mom_p=None, hair=0.0, cards_=True, extra=None):
    ctx.save(); cam(ctx, cx, cy, z, 0, sh, f)
    room(ctx, lf, roof)
    blown = boom >= 0 and lf >= boom
    bt = lf - boom if blown else 0
    if roof:
        frame_pic(ctx, 760, 820, 0.35 * eout(pop(bt, 0, 8)) if blown else 0.0)
        # lamp
        la = -1.1 * eout(pop(bt, 2, 12)) if blown else 0.0
        ctx.save(); ctx.translate(1010, FLOOR); ctx.rotate(-la)
        ctx.rectangle(-8, -560, 16, 560); fl(ctx, hx('3a3a4a'), 4)
        poly(ctx, [(-70, -560), (70, -560), (40, -670), (-40, -670)]); fl(ctx, YEL, 6)
        ctx.restore()
    sofa_back(ctx)
    dp = dad_p or sit(eye='closed', mouth='open', head=-18)
    sofa_front(ctx)
    bd = draw(ctx, 330, SEAT - 186 * 1.25 * 0.62, 1.25, 1, DAD, dp)
    hd, R = bd['head'], bd['R']
    if not blown and dad_p is None:
        nostrils(ctx, hd[0], hd[1], R, 0.7 + 0.3 * math.sin(lf * 0.8))
    table(ctx)
    if cards_:
        cards(ctx, 780, 1300, lf, boom)
    # kid on the floor by the table (right), Mom standing far right
    kx = 760 + (180 * eout(pop(bt, 0, 10)) if blown else 0)
    kp = kid_p or P(eye='shock', mouth='open', rsh=-40, lsh=40, lhip=80, lkn=-90, rhip=84, rkn=-88)
    if blown:
        sc = _SCR
        kb = draw(sc, kx, 1390 - 186 * 1.0, 1.0, -1, BOY, kp)
        blown_hair(ctx, kb['head'][0], kb['head'][1], kb['R'], BOY['hair'], 1, hair)
    draw(ctx, kx, 1390 - 186 * 1.0 * 0.9, 1.0, -1, BOY, kp)
    mp = mom_p or P(eye='shock', mouth='open', rsh=-60, rel=-90, lsh=30)
    mb = draw(_SCR, 940, FLOOR - 186 * 1.3, 1.3, -1, MOM, mp)
    if blown:
        blown_hair(ctx, mb['head'][0], mb['head'][1], mb['R'], MOM['hair'], 1, hair)
    mb = draw(ctx, 940, FLOOR - 186 * 1.3, 1.3, -1, MOM, mp)
    cup(ctx, mb['front'][0] - 10, mb['front'][1] - 30, -0.9 * eout(pop(bt, 0, 6)) if blown else 0, 0.7, not blown)
    if blown and bt < 30:
        rnd = random.Random(9)
        for k in range(8):
            px = mb['front'][0] + bt * 30 + rnd.uniform(-60, 60); py = mb['front'][1] - 40 + bt * rnd.uniform(-4, 10)
            ellipse(ctx, px, py, 14, 10); setc(ctx, hx('8a4a1a')); ctx.fill()
    # dog slides away
    if blown:
        dog(ctx, 600 + bt * 40, FLOOR + 10, 0.8, 1, lf)
    else:
        dog(ctx, 600, FLOOR + 10, 0.8, 1, lf)
    if extra:
        extra(ctx)
    ctx.restore()
    return bd


def s2(ctx, f):
    lf = f - 54
    BOOM = 46
    if lf < 92:
        bt = lf - BOOM
        if lf < BOOM:
            z = 0.8 + 0.14 * eio(pop(lf, 0, BOOM)); sh = 2 + lf // 8
            dp = sit(eye='closed', mouth='open', head=-18 - 10 * eio(pop(lf, 0, BOOM)))
        else:
            z = 0.8; sh = shake_at(bt, [0], 18, 36)
            dp = sit(eye='closed', mouth='scream', head=22, torso=24, lsh=-40, rsh=-30)
        living_wide(ctx, f, lf, BOOM, z, 460 + 200 * (1 - eio(pop(lf, 0, BOOM))) if lf < BOOM else 660, 1040, sh, dad_p=dp,
                    kid_p=None if lf < BOOM else P(eye='shock', mouth='scream', rsh=-150, lsh=150, lhip=80, lkn=-90, rhip=84, rkn=-88, torso=-14),
                    mom_p=None if lf < BOOM else P(eye='shock', mouth='scream', rsh=-150, lsh=160, torso=-12),
                    hair=eout(pop(bt, 0, 6)) if lf >= BOOM else 0)
        if lf >= BOOM:
            wind(ctx, -200, 700, 1300, 1500, lf, 14, 0.85, 16)
            label(ctx, "CHOOO!!!", 540, 520, 200, YEL, -0.08, pop(bt, 0, 3))
        else:
            label(ctx, "\"AHH... AHHHH...\"", 540, 560, 100, WHITE, -0.04, pop(lf, 0, 4))
    else:
        il = lf - 92
        mom_ecu(ctx, f, il, PINK, 'normal', 'flat', z0=1.0 + 0.05 * eout(pop(il, 0, 34)), blown=1.0, tw=il > 14)
        label2(ctx, "\"...bless", "you.\"", WHITE, pop(il, 4, 8), 130, col2=YEL, y=1440)


def s3(ctx, f):
    lf = f - 180
    if lf < 72:
        BOOM = 22
        bt = lf - BOOM
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eio(pop(lf, 0, 72)), 0, shake_at(bt, [0], 14, 20) if lf >= BOOM else 0, f)
        outdoor(ctx, lf)
        house(ctx, 200, 1350, lf)
        tree(ctx, 900, 1360, 0.15 * eout(pop(bt, 0, 8)) if lf >= BOOM else 0.0)
        hp = P(eye='happy', mouth='smile', rsh=-50, rel=-30, lsh=20) if lf < BOOM else P(eye='shock', mouth='scream', rsh=-60, rel=-30, lsh=150, torso=-12)
        b0 = draw(_SCR, 620, 1500 - 186 * 1.4, 1.4, -1, NB, hp)
        if lf >= BOOM:
            blown_hair(ctx, b0['head'][0], b0['head'][1], b0['R'], NB['hair'], 1, eout(pop(bt, 0, 6)))
        b = draw(ctx, 620, 1500 - 186 * 1.4, 1.4, -1, NB, hp)
        # hose + water arc
        hx_, hy = b['front'] if 'front' in b else (520, 1200)
        ctx.new_path(); ctx.move_to(hx_, hy)
        bend = eout(pop(bt, 0, 6)) if lf >= BOOM else 0
        ex, ey = hx_ - 300 + 600 * bend, hy + 80 - 260 * bend
        ctx.curve_to(hx_ - 120 + 160 * bend, hy - 160, ex - 60, ey - 120, ex, ey)
        setc(ctx, hx('8fe0ff')); ctx.set_line_width(22); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        if lf >= BOOM:
            # his hat flies off
            ctx.save(); ctx.translate(b['head'][0] + bt * 30, b['head'][1] - b['R'] - bt * 12); ctx.rotate(bt * 0.3)
            ellipse(ctx, 0, 0, 110, 24); fl(ctx, hx('f6d27a'), 6); rect_r(ctx, -60, -70, 120, 70, 30); fl(ctx, hx('f6d27a'), 6)
            ctx.restore()
        ctx.restore()
        card(ctx, 'p3', f, 180, 248)
        if lf >= BOOM:
            wind(ctx, -200, 600, 1300, 1500, lf, 12, 0.75, 14, seed=7)
            label(ctx, "*WHOOOSH*", 540, 640, 110, WHITE, 0.05, pop(bt, 0, 3))
            if bt >= 14:
                label2(ctx, "\"BLESS", "YOU!!\"", WHITE, pop(bt, 14, 18), 130, col2=ORANGE, y=1440)
    else:
        il = lf - 72
        cx, cy, R = mom_ecu(ctx, f, il, hx('ffb3d9'), 'closed' if il < 34 else 'happy', 'open' if il < 34 else 'smile',
                            z0=1.0 + 0.05 * eout(pop(il, 0, 68)), cup_=False)
        card(ctx, 'p4', f, 252, 316)
        if il >= 20:
            for k, (x, y, r) in enumerate(((240, 700, 50), (850, 760, 40), (300, 1150, 34), (820, 1180, 46))):
                sparkle(ctx, x, y, r * eout(pop(il, 20 + k, 26 + k)) + 6 * math.sin(il * 0.6 + k))
            label(ctx, "*tchoo!*", 540, 1260, 62, WHITE, -0.04, pop(il, 20, 23))
        if il >= 36:
            label2(ctx, "\"Awww...", "SO CUTE!\"", WHITE, pop(il, 36, 40), 120, col2=PINK, y=1450)


def s4(ctx, f):
    lf = f - 320
    if lf < 44:
        b = 0.5 + 0.5 * eio(pop(lf, 0, 40))
        kid_ecu(ctx, f, lf, GREEN, b, z0=1.0 + 0.1 * eio(pop(lf, 0, 44)), shake=2 + lf // 8)
        card(ctx, 'p5', f, 320, 362)
        label2(ctx, "\"ah...", "AHHH...\"", WHITE, pop(lf, 4, 8), 120, col2=YEL, y=1440)
    elif lf < 70:
        il = lf - 44
        # parents squeezed side by side, terrified
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.04 * il / 26, 0, 4, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, PURPLE); ctx.fill()
        rays(ctx, 540, 900, 200, 1700, il * 0.04, col=(1, 0.9, 1), a=0.25, n=18)
        face(ctx, DAD, P(eye='shock', mouth='scream'), 320, 920, 230, -0.08)
        face(ctx, MOM, P(eye='shock', mouth='scream'), 770, 920, 220, 0.08)
        sweat(ctx, 480, 760, il, 1.2); sweat(ctx, 950, 760, il, 1.2)
        ctx.restore()
        label(ctx, "\"UH-OH.\"", 540, 1420, 150, YEL, -0.04, pop(il, 2, 6))
    elif lf < 112:
        il = lf - 70
        ctx.save(); cam(ctx, 540, 1000, 0.92, 0, shake_at(il, [0], 20, 40), f)
        outdoor(ctx, il)
        tree(ctx, 920, 1360, 0.2 * eout(pop(il, 0, 6)))
        house(ctx, 440, 1350, il, il, 0.02 * math.sin(il * 2) * (1 - pop(il, 0, 20)))
        rnd = random.Random(4)
        for k in range(5):   # birds flee
            bx = 900 + rnd.uniform(-100, 100) + il * 22; by = 900 - il * rnd.uniform(8, 16)
            ctx.new_path(); ctx.move_to(bx - 30, by); ctx.curve_to(bx - 15, by - 20, bx, by - 10, bx, by); ctx.curve_to(bx, by - 10, bx + 15, by - 20, bx + 30, by)
            ink(ctx, 6); ctx.stroke()
        ctx.restore()
        wind(ctx, -200, 400, 1300, 1500, il, 14, 0.8, 16, seed=11)
        label(ctx, "ACHOOOO!!!", 540, 1480, 170, YEL, -0.06, pop(il, 0, 3))
    else:
        il = lf - 112
        dp = P(eye='happy', mouth='grin', rsh=-150, rel=-20, lsh=40, lel=-60)
        living_wide(ctx, f, il + 200, 0, 0.8, 660, 1020, 0, roof=False,
                    dad_p=sit(eye='happy', mouth='grin', rsh=-150, rel=-20),
                    kid_p=P(eye='happy', mouth='grin', rsh=-150, lsh=150, lhip=80, lkn=-90, rhip=84, rkn=-88),
                    mom_p=P(eye='normal', mouth='flat', rsh=10, lsh=-10), hair=1.0, cards_=False)
        sparkle(ctx, 300, 820, 30 + 8 * math.sin(il * 0.6))
        label2(ctx, "\"That's MY", "BOY!!\"", WHITE, pop(il, 3, 7), 130, col2=BLUE, y=560)


def s5(ctx, f):
    lf = f - 470
    if lf < 66:
        mom_ecu(ctx, f, lf, SKY, 'normal', 'flat', z0=1.0 + 0.05 * eout(pop(lf, 0, 66)), blown=1.0, sky=True, tw=lf > 30)
        label2(ctx, "\"...who's paying", "for the ROOF?\"", WHITE, pop(lf, 4, 8), 104, col2=RED, y=1440)
    elif lf < 158:
        il = lf - 66
        z = 0.8 + 0.2 * eio(pop(il, 30, 92))
        living_wide(ctx, f, il + 400, -1, z, 660 - 240 * eio(pop(il, 30, 92)), 1040, 2 + il // 20, roof=False,
                    dad_p=sit(eye='closed', mouth='open', head=-24),
                    kid_p=P(eye='shock', mouth='scream', rsh=-100, lsh=-90, lhip=80, lkn=-90, rhip=84, rkn=-88, torso=-10),
                    mom_p=P(eye='shock', mouth='scream', rsh=-100, lsh=-80, torso=-10), cards_=False)
        if il < 30:
            label(ctx, "*sniff*", 330, 600, 90, WHITE, -0.05, pop(il, 0, 3))
        label(ctx, "\"AHH...\"", 330, 470 if il >= 30 else 800, 110, YEL, -0.05, pop(il, 12, 16))
        if il >= 36:
            label2(ctx, "\"NOT", "AGAIN!!\"", WHITE, pop(il, 36, 40), 140, col2=RED, y=1420)
    else:
        s1(ctx, f, f - 628 + 24)


SHOTS = [(0, s1), (54, s2), (180, s3), (320, s4), (470, s5)]
CUTS = (54, 146, 180, 252, 320, 364, 390, 432, 470, 536, 628)


def render(f):
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
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/v{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/dads_sneeze_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
