"""'Where Did We Park?' - original, general-audience comedy short, 22s.
Hook: Dad ECU, smug grin, twirling the car keys: "I know EXACTLY where we parked!"
Beat 1: wide parking garage, family loaded with shopping bags, Dad points at spot C3 -> empty, tumbleweed: "...it was RIGHT HERE."
Beat 2: the key trick: fob held high *BEEP BEEP* -> top-down maze of identical cars, the family zig-zags, level sign P1 -> P4 -> P9.
Beat 3: Dad climbs onto a car roof, fob raised like a trophy -> it's a STRANGER's car: alarm WEE-OO, he falls *THUD*.
 2 HOURS LATER: family slumped on the curb, kid asleep, "It's a BLUE car..." - every car is blue.
Twist: Mom, calm: "Honey... we took the BUS." Dad freezes -> "...I KNEW that."
 Bus home -> the driveway is EMPTY: "WHERE'S OUR CAR?!" -> Mom: "You drove it to WORK. Yesterday."
 -> Dad smug ECU again: "I know EXACTLY where I parked!" (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, zzz, bloodshot
from scenes48 import label1, label2
from scenes58 import arm_to, sweat, twitch
from scenes28 import bag
import scenes13
from scenes13 import card as _card13
import random

MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'), pants=hx('3d5a9e'))
DAD = dict(doodle.DAD, shirt=hx('22b45a'), pants=hx('3d5aff'))
BOY = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ffc93c'), pants=hx('8a3cff'))
N = 660
FLOOR = 1450
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
GOLD = hx('ffc93c')
WHITE = (1, 1, 1)
CARBLUE = hx('2f6bff')

CAPS = {
    'p1': [[("DAD:", OUT)], [("\"I REMEMBER WHERE", BLUE)], [("WE PARKED!\"", BLUE)]],
    'p2': [[("THE", OUT)], [("KEY TRICK", ORANGE)]],
    'p3': [[("2 HOURS", RED)], [("LATER...", OUT)]],
    'p4': [[("THEN MOM", OUT)], [("REMEMBERED...", PINK)]],
    'p5': [[("BACK", OUT)], [("HOME...", GREEN)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def fob(ctx, x, y, s=1.0, a=0.0, beep=0.0):
    """car key fob with ring, hanging point at (x, y)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.arc(0, 0, 26, 0, 2 * math.pi); setc(ctx, OUT); ctx.set_line_width(11); ctx.stroke_preserve(); setc(ctx, hx('ffd23f')); ctx.set_line_width(6); ctx.stroke()
    rect_r(ctx, -42, 24, 84, 130, 34); fl(ctx, hx('2a2840'), 7)
    ellipse(ctx, 0, 66, 20, 20); fl(ctx, RED if beep <= 0 else hx('ff9aa8'), 4)
    ellipse(ctx, 0, 116, 15, 15); fl(ctx, hx('6a6a86'), 4)
    if beep > 0:
        for k in range(3):
            r = 80 + k * 55 + 40 * beep
            ctx.arc(0, 66, r, -2.4, -0.7); setc(ctx, YEL + (max(0, 1 - beep) * 0.9,)); ctx.set_line_width(14); ctx.stroke()
    ctx.restore()


def finger_hand(ctx, x, y, s=1.0, a=0.0, col=None):
    """fist with index finger up; fingertip at (x, y - 150*s)"""
    col = col or DAD['skin']
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -24, -160, 48, 130, 24); fl(ctx, col, 7)
    rect_r(ctx, -70, -60, 140, 120, 46); fl(ctx, col, 8)
    for k in range(3):
        ctx.move_to(-40 + k * 30, -40); ctx.line_to(-40 + k * 30, -10)
    ink(ctx, 5); ctx.stroke()
    ctx.restore()


def car_side(ctx, x, g, s=1.0, col=CARBLUE, flash=0.0, f_=1, dent=0.0):
    """sedan side view, bottom-centre (x, g). ~640 px wide at s=1"""
    ctx.save(); ctx.translate(x, g); ctx.scale(s * f_, s)
    if flash > 0:
        g_ = cairo.RadialGradient(0, -160, 50, 0, -160, 520)
        g_.add_color_stop_rgba(0, 1, 0.6, 0.1, 0.6 * flash); g_.add_color_stop_rgba(1, 1, 0.6, 0.1, 0)
        ctx.set_source(g_); ellipse(ctx, 0, -160, 520, 360); ctx.fill()
    poly(ctx, [(-190, -200), (-120, -330 + 20 * dent), (130, -330 + 20 * dent), (220, -200)]); fl(ctx, col, 8)
    poly(ctx, [(-160, -205), (-105, -300 + 18 * dent), (-5, -300 + 18 * dent), (-5, -205)]); fl(ctx, hx('bfe8ff'), 6)
    poly(ctx, [(15, -205), (15, -300 + 18 * dent), (115, -300 + 18 * dent), (185, -205)]); fl(ctx, hx('bfe8ff'), 6)
    rect_r(ctx, -320, -220, 640, 150, 50); fl(ctx, col, 8)
    ctx.move_to(-10, -210); ctx.line_to(-10, -90); setc(ctx, dark(col, 0.7)); ctx.set_line_width(6); ctx.stroke()
    rect_r(ctx, 40, -175, 50, 14, 7); fl(ctx, dark(col, 0.6), 3)
    hl = YEL if flash <= 0 else (hx('ffb02e') if flash > 0.5 else YEL)
    rect_r(ctx, 280, -195, 40, 34, 12); fl(ctx, hl, 5)
    rect_r(ctx, -320, -195, 34, 34, 12); fl(ctx, RED if flash <= 0.5 else hx('ffb02e'), 5)
    for wx in (-190, 190):
        ellipse(ctx, wx, -70, 70, 70); fl(ctx, hx('2a2840'), 8)
        ellipse(ctx, wx, -70, 30, 30); fl(ctx, hx('c8ccd8'), 5)
    ctx.restore()


def car_top(ctx, x, y, s=1.0, col=CARBLUE, a=0.0, blink=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if blink > 0:
        for sx in (-1, 1):
            for sy in (-1, 1):
                ellipse(ctx, sx * 70, sy * 150, 50, 50); setc(ctx, (1, 0.75, 0.2, 0.7 * blink)); ctx.fill()
    rect_r(ctx, -80, -160, 160, 320, 50); fl(ctx, col, 7)
    rect_r(ctx, -64, -96, 128, 54, 14); fl(ctx, hx('bfe8ff'), 5)
    rect_r(ctx, -64, 60, 128, 44, 14); fl(ctx, hx('bfe8ff'), 5)
    rect_r(ctx, -60, -40, 120, 96, 20); setc(ctx, dark(col, 0.85)); ctx.fill()
    ctx.restore()


def garage(ctx, lvl='C3', col=hx('b8c0d4'), floor=FLOOR):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, col); ctx.fill()
    ctx.rectangle(-3000, -3000, 7000, 3480); setc(ctx, dark(col, 0.82)); ctx.fill()          # ceiling band
    for k in range(-6, 10):
        rect_r(ctx, k * 380 - 90, 330, 180, 30, 14); fl(ctx, hx('fffbe0'), 5)                 # strip lights
        poly(ctx, [(k * 380 - 90, 360), (k * 380 + 90, 360), (k * 380 + 170, 620), (k * 380 - 170, 620)])
        setc(ctx, (1, 1, 0.85, 0.12)); ctx.fill()
    ctx.rectangle(-3000, 470, 7000, 26); setc(ctx, hx('ffc93c')); ctx.fill()                  # yellow stripe
    ctx.rectangle(-3000, floor, 7000, 3000); setc(ctx, hx('8a92a8')); ctx.fill()
    ctx.move_to(-3000, floor); ctx.line_to(4000, floor); ink(ctx, 8); ctx.stroke()
    for k in range(-6, 10):                                                                   # pillars
        px = k * 760 + 80
        ctx.rectangle(px - 60, 496, 120, floor - 496); fl(ctx, hx('d8deea'), 7)
        for j in range(4):
            poly(ctx, [(px - 60, floor - 60 - j * 70), (px + 60, floor - 120 - j * 70), (px + 60, floor - 90 - j * 70), (px - 60, floor - 30 - j * 70)])
            setc(ctx, hx('ffc93c') if j % 2 == 0 else hx('2a2840')); ctx.fill()
        rect_r(ctx, px - 52, 600, 104, 90, 14); fl(ctx, BLUE, 5)
        text(ctx, lvl, px, 662, 56, (1, 1, 1), ow=0, shadow=False)


def tumbleweed(ctx, x, y, r, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    for k in range(7):
        ctx.arc(0, 0, r * (0.4 + 0.1 * k), k, k + 4.2)
        setc(ctx, hx('a8783a')); ctx.set_line_width(7); ctx.stroke()
    ellipse(ctx, 0, 0, r, r); ink(ctx, 5); ctx.stroke()
    ctx.restore()


def family_wide(ctx, lf, x0=420, dad_p=None, mom_p=None, boy_p=None, k=1.0, g=FLOOR, bags_on=True, f_=1, show=('mom', 'dad', 'boy')):
    """Mom, Dad, kid standing in a row holding bags; returns dict of bodies"""
    out = {}
    walk = math.sin(lf * 0.5)
    if 'mom' in show:
        b = draw(ctx, x0 - 210 * k, g - 186 * k * 0.98, 0.98 * k, f_, MOM, mom_p or P(mouth='flat', lsh=8, rsh=-8))
        if bags_on:
            bag(ctx, b['back'][0], b['back'][1] + 200 * k * 0.6, 0.6 * k, 0.05, 1)
        out['mom'] = b
    if 'boy' in show:
        b = draw(ctx, x0 + 260 * k, g - 186 * k * 0.66, 0.66 * k, f_, BOY, boy_p or P(mouth='flat'))
        out['boy'] = b
    if 'dad' in show:
        b = draw(ctx, x0, g - 186 * k, k, f_, DAD, dad_p or P(mouth='grin'))
        if bags_on:
            bag(ctx, b['back'][0], b['back'][1] + 220 * k * 0.62, 0.62 * k, -0.05, 0)
        out['dad'] = b
    return out


def bus(ctx, x, g, s=1.0, faces=True, lf=0, door=0.0):
    ctx.save(); ctx.translate(x, g); ctx.scale(s, s)
    rect_r(ctx, -620, -560, 1240, 480, 60); fl(ctx, hx('19b5a5'), 9)
    ctx.rectangle(-620, -250, 1240, 50); setc(ctx, hx('ffc93c')); ctx.fill()
    for k in range(5):
        wx = -540 + k * 190
        rect_r(ctx, wx, -500, 160, 180, 22); fl(ctx, hx('bfe8ff'), 6)
    # door at the front (right)
    rect_r(ctx, 440, -500, 130, 400, 16); fl(ctx, hx('bfe8ff') if door > 0 else hx('8fd8ff'), 6)
    rect_r(ctx, 580, -480, 30, 120, 10); fl(ctx, hx('bfe8ff'), 4)
    rect_r(ctx, 590, -210, 30, 40, 10); fl(ctx, YEL, 4)
    for wx in (-400, 380):
        ellipse(ctx, wx, -80, 85, 85); fl(ctx, hx('2a2840'), 9)
        ellipse(ctx, wx, -80, 36, 36); fl(ctx, hx('c8ccd8'), 5)
    if faces:
        face(ctx, DAD, P(eye='smug', mouth='grin', head=0), -460 + 80, -400, 60, 0.0)
        face(ctx, MOM, P(eye='normal', mouth='smile', head=0), -270 + 80, -400, 58, 0.0)
        face(ctx, BOY, P(eye='happy', mouth='grin', head=0), -80 + 80, -390, 48, 0.0)
    ctx.restore()


def house_ext(ctx):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('8fd8ff')); ctx.fill()
    ellipse(ctx, 900, 420, 90, 90); setc(ctx, hx('fff27a')); ctx.fill()
    for cx_, cy_ in ((200, 450), (650, 380)):
        for dx, r in ((-50, 45), (0, 62), (55, 45)):
            ellipse(ctx, cx_ + dx, cy_, r, r * 0.8); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.rectangle(-3000, 1150, 7000, 3000); setc(ctx, hx('5fd068')); ctx.fill()
    # house left
    rect_r(ctx, -60, 700, 520, 520, 10); fl(ctx, hx('ffd9a8'), 8)
    poly(ctx, [(-110, 720), (200, 520), (510, 720)]); fl(ctx, hx('c94a3a'), 8)
    rect_r(ctx, 60, 860, 140, 360, 10); fl(ctx, hx('8a4a2c'), 7)
    rect_r(ctx, 270, 820, 140, 130, 10); fl(ctx, hx('bfe8ff'), 7)
    # garage door + driveway
    rect_r(ctx, 470, 820, 520, 400, 10); fl(ctx, hx('eef0f4'), 8)
    for k in range(4):
        ctx.move_to(470, 880 + k * 80); ctx.line_to(990, 880 + k * 80)
    setc(ctx, hx('b8c0d4')); ctx.set_line_width(6); ctx.stroke()
    poly(ctx, [(470, 1220), (990, 1220), (1180, FLOOR + 400), (280, FLOOR + 400)]); fl(ctx, hx('a8b0c4'), 7)
    ellipse(ctx, 730, 1360, 130, 40); setc(ctx, hx('4a4e60')); ctx.fill()                      # oil stain


# ------------------------------------------------------------------ opening face
def opening_face(ctx, f, lf, lab=True):
    ctx.save(); cam(ctx, 540, 960, 1.04 + 0.05 * eout(pop(lf, 0, 45)), 0, 2 + shake_at(lf, [0], 10, 16), f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb02e')); ctx.fill()
    rays(ctx, 540, 980, 260, 1700, lf * 0.04, col=(1, 1, 0.8), a=0.4, n=16)
    cx, cy, R = 520, 1000, 300
    face(ctx, DAD, P(eye='smug', mouth='grin', head=0), cx, cy, R, -0.08 + 0.02 * math.sin(lf * 0.3))
    # finger up, keys twirling on it
    fx, fy = 880, 1180
    arm_to(ctx, 1200, 1900, fx, fy + 30, DAD['shirt'], DAD['skin'], bend=-60, w=120)
    finger_hand(ctx, fx, fy, 1.2, 0.12)
    tip = (fx + 1.2 * 150 * math.sin(0.12), fy - 1.2 * 150 * math.cos(0.12))
    fob(ctx, tip[0], tip[1] + 10, 1.0, lf * 0.55)
    sparkle(ctx, 300, 640, 34 + 8 * math.sin(lf * 0.5)); sparkle(ctx, 790, 760, 26)
    ctx.restore()
    if lab:
        label2(ctx, "\"I know EXACTLY", "where we parked!\"", WHITE, pop(lf, 0, 4) if lf > 0 else 1, 104, col2=YEL, y=1410)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 45:
        opening_face(ctx, f, f)
    else:
        lf = f - 45
        ctx.save(); cam(ctx, 520, 1380, 1.3 + 0.06 * eout(pop(lf, 0, 40)), 0, shake_at(lf, [0], 6, 8), f)
        garage(ctx, 'C3')
        # parked cars either side of the EMPTY spot
        car_side(ctx, -260, FLOOR, 0.9, hx('ff8a1f'))
        car_side(ctx, 1340, FLOOR, 0.9, hx('8a3cff'), f_=-1)
        ctx.rectangle(240, FLOOR + 10, 600, 18); setc(ctx, (1, 1, 1)); ctx.fill()
        tw = eout(pop(lf, 10, 45))
        tumbleweed(ctx, 1100 - 700 * tw, FLOOR - 60 - 40 * abs(math.sin(lf * 0.4)), 55, -lf * 0.3)
        point = P(eye='smug' if lf < 16 else 'shock', mouth='grin' if lf < 16 else 'wavy', rsh=95, rel=0, lsh=10)
        fam = family_wide(ctx, lf, 420, dad_p=point,
                          mom_p=P(eye='normal' if lf < 20 else 'glare', mouth='flat', lsh=8, rsh=-8),
                          boy_p=P(eye='shock' if lf > 16 else 'normal', mouth='open' if lf > 16 else 'flat'), k=0.95, g=FLOOR + 160)
        ctx.restore()
        if lf < 16:
            label1(ctx, "\"RIGHT... HERE!\"", WHITE, pop(lf, 1, 5), 120, -0.04, y=1420)
        else:
            label1(ctx, "\"...it WAS right here.\"", WHITE, pop(lf, 18, 22), 104, -0.04, y=1420)
    card(ctx, 'p1', f, -6, 86)


def s2(ctx, f):
    lf = f - 90
    if lf < 28:
        # ECU: fob held high, BEEP BEEP
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eout(pop(lf, 0, 28)), -4, shake_at(lf, [4, 14], 8, 14), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('3a3e6e')); ctx.fill()
        rays(ctx, 540, 820, 200, 1700, lf * 0.05, col=(1, 0.9, 0.4), a=0.25, n=16)
        arm_to(ctx, 700, 2000, 560, 1000, DAD['shirt'], DAD['skin'], bend=-60, w=150)
        ellipse(ctx, 560, 960, 110, 100); fl(ctx, DAD['skin'], 8)
        fob(ctx, 560, 620, 2.2, 0.0, beep=(lf % 10) / 10 if lf >= 4 else 0.0)
        ctx.restore()
        label(ctx, "*BEEP!*", 300, 640, 110, YEL, -0.12, pop(lf, 4, 7))
        label(ctx, "*BEEP!*", 790, 700, 110, YEL, 0.12, pop(lf, 14, 17))
        card(ctx, 'p2', f, 92, 200)
    else:
        il = lf - 28
        # top-down maze of identical cars, family zig-zags; level sign climbs
        lvl = ['P1', 'P4', 'P9'][min(2, il // 28)]
        ctx.save(); cam(ctx, 540, 960, 0.92, 0, shake_at(il, [0, 28, 56], 5, 10), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('8a92a8')); ctx.fill()
        for r in range(-1, 8):
            for c in range(-1, 8):
                x = 60 + c * 210; y = 330 + r * 400
                ctx.rectangle(x - 105, y - 190, 6, 380); setc(ctx, (1, 1, 1)); ctx.fill()
                rnd = (r * 7 + c * 3 + il // 28) % 5
                blink = 1.0 if (il // 6 + r + c) % 7 == 0 else 0.0
                car_top(ctx, x, y, 0.95, CARBLUE, 0.03 * ((r + c) % 3 - 1), blink)
        # family path (heads seen from above) through the aisle
        aisle_y = [530, 930, 1330][min(2, il // 28)]
        t = (il % 28) / 28
        hxp = -100 + 1300 * t if (il // 28) % 2 == 0 else 1180 - 1300 * t
        dirx = 1 if (il // 28) % 2 == 0 else -1
        ctx.rectangle(-500, aisle_y - 75, 2200, 150); setc(ctx, hx('9aa2b8')); ctx.fill()
        for k, (ch, R) in enumerate(((DAD, 66), (MOM, 60), (BOY, 50))):
            px = hxp - dirx * k * 150
            face(ctx, ch, P(eye='shock' if k == 0 else 'glare', mouth='wavy' if k == 0 else 'flat', head=0), px, aisle_y + 6 * math.sin(il * 0.9 + k), R, 0)
        ctx.restore()
        # level sign (big, centred top area below the safe line)
        rect_r(ctx, 380, 300, 320, 170, 30); fl(ctx, BLUE, 8)
        text(ctx, lvl, 540, 410, 110, (1, 1, 1), ow=10)
        label1(ctx, ["\"It's around here...\"", "\"...somewhere...\"", "\"...it's a BLUE car!\""][min(2, il // 28)], WHITE, pop(il % 28, 1, 5), 104, -0.04, y=1420)


def s3(ctx, f):
    lf = f - 200
    if lf < 60:
        # low angle: Dad on a car roof, fob raised like a trophy -> alarm, falls
        alarm = lf >= 22
        flash = (0.5 + 0.5 * math.sin(lf * 1.6)) if alarm else 0.0
        fall = eout(pop(lf, 40, 52))
        ctx.save(); cam(ctx, 540, 1000, 0.85, -6 if not alarm else -6 + 4 * math.sin(lf), 2 + (14 if alarm else 0) + shake_at(lf, [52], 14, 30), f)
        garage(ctx, 'P9', col=hx('b8c0d4') if not alarm else (hx('ffb3a0') if flash > 0.5 else hx('b8c0d4')))
        car_side(ctx, 540, FLOOR, 1.25, CARBLUE, flash=flash)
        roof = FLOOR - 330 * 1.25
        if lf < 40:
            k = 1.0
            b = draw(ctx, 540, roof - 186 * k, k, 1, DAD, P(eye='happy' if not alarm else 'shock', mouth='grin' if not alarm else 'scream',
                                                       rsh=170, rel=0, lsh=-120 if not alarm else -150, lel=-30, lhip=-10, rhip=10, rot=0))
            fob(ctx, b['front'][0], b['front'][1] - 40, 0.9, 3.14, beep=(lf % 8) / 8 if not alarm else 0)
            if not alarm:
                sparkle(ctx, b['front'][0] - 120, b['front'][1] - 60, 40); sparkle(ctx, b['front'][0] + 110, b['front'][1] - 20, 30)
        else:
            k = 1.0
            b = draw(ctx, 540 + 260 * fall, roof - 186 * k + 420 * fall * fall, k, 1, DAD,
                     P(eye='shock', mouth='scream', rsh=150, lsh=-150, lel=-40, rel=40, lhip=-40, rhip=40, rot=90 * fall))
        ctx.restore()
        if not alarm:
            label1(ctx, "\"FOUND IT!!\"", WHITE, pop(lf, 2, 6), 130, -0.04, y=1420)
        else:
            label(ctx, "WEE-OO! WEE-OO!", 540, 1300 if lf < 52 else 1420, 112, RED if (lf // 4) % 2 else ORANGE, 0.04 * math.sin(lf), pop(lf, 22, 25))
            if lf >= 30 and lf < 52:
                label1(ctx, "\"NOT OUR CAR!!\"", WHITE, pop(lf, 30, 34), 110, -0.04, y=1440)
        if lf >= 52:
            label(ctx, "*THUD!*", 540, 700, 130, ORANGE, -0.1, pop(lf, 52, 55))
    else:
        il = lf - 60
        # 2 HOURS LATER: family slumped on the curb; every car is blue
        ctx.save(); cam(ctx, 455 + 30 * eout(pop(il, 0, 70)), 1460, 1.35, 0, 0, f)
        garage(ctx, 'P9', col=hx('a8b0c4'))
        for k in range(-2, 4):
            car_side(ctx, k * 680 + 200, FLOOR - 40, 0.8, CARBLUE)
        rect_r(ctx, -500, FLOOR + 60, 2200, 60, 10); fl(ctx, hx('d8deea'), 7)          # curb
        g = FLOOR + 230
        sit = dict(lhip=-80, lkn=80, rhip=-80, rkn=80)
        bm = draw(ctx, 250, g - 186 * 0.95 - 70, 0.95, 1, MOM, P(eye='glare', mouth='flat', lsh=20, rsh=-10, **sit))
        bd = draw(ctx, 680, g - 186 * 1.0 - 70, 1.0, -1, DAD, P(eye='closed', mouth='wavy', head=14, torso=10, lsh=30, rsh=30, **sit))
        bb = draw(ctx, 470, g - 186 * 0.66 - 70, 0.66, 1, BOY, P(eye='closed', mouth='open', head=22, torso=12, **sit))
        zzz(ctx, bb['head'][0] - 10, bb['head'][1] - 90, il, 0.7)
        sweat(ctx, bd['head'][0] + 80, bd['head'][1] - 70, il, 1.0)
        for k, (bx, kind) in enumerate(((860, 0), (950, 2), (110, 1))):
            bag(ctx, bx, g - 40, 0.6, 0.6 * (k % 2) - 0.2, kind)
        ctx.restore()
        label2(ctx, "\"It's a BLUE car...", "...I'm SURE.\"", WHITE, pop(il, 8, 12), 98, col2=hx('9fd0ff'), y=1400)
        card(ctx, 'p3', f, 262, 328)


def s4(ctx, f):
    lf = f - 330
    if lf < 50:
        # Mom ECU, calm, sipping nothing, deadpan
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eout(pop(lf, 0, 50)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd9ec')); ctx.fill()
        for k in range(6):
            ellipse(ctx, 540, 960, 280 + k * 170, 280 + k * 170); setc(ctx, (1, 1, 1, 0.3)); ctx.set_line_width(30); ctx.stroke()
        face(ctx, MOM, P(eye='normal' if lf < 22 else 'smug', mouth='flat' if lf < 22 else 'smile', head=0), 540, 960, 300, 0.05)
        ctx.restore()
        if lf < 22:
            label1(ctx, "\"Honey...\"", WHITE, pop(lf, 2, 6), 130, -0.04, y=1420)
        else:
            label2(ctx, "\"...we took", "the BUS.\"", WHITE, pop(lf, 22, 26), 120, col2=PINK, y=1400)
        card(ctx, 'p4', f, 332, 378)
    elif lf < 92:
        il = lf - 50
        # Dad freezes: crash zoom, shatter lines, twitch
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.25 * eout(pop(il, 0, 8)), 0, shake_at(il, [0], 12, 30), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd23f')); ctx.fill()
        rays(ctx, 540, 960, 260, 1700, il * 0.02, col=(1, 1, 1), a=0.5, n=20)
        cx, cy, R = 540, 960, 280
        face(ctx, DAD, P(eye='shock', mouth='wavy', head=0), cx, cy, R, 0)
        twitch(ctx, cx + 0.5 * R, cy - 0.55 * R, il, 1.2)
        sweat(ctx, cx - 0.95 * R, cy - 0.6 * R, il, 1.4)
        ctx.restore()
        label(ctx, "*GASP!*", 540, 640, 110, WHITE, -0.08, pop(il, 0, 3) * (1 - pop(il, 16, 20)))
        if il >= 18:
            label1(ctx, "\"...the BUS?\"", WHITE, pop(il, 18, 22), 130, -0.04, y=1420)
    else:
        il = lf - 92
        # Dad, recovering, smug again
        ctx.save(); cam(ctx, 540, 960, 1.05, 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('7fd0ff')); ctx.fill()
        rays(ctx, 540, 960, 260, 1700, il * 0.03, col=(1, 1, 1), a=0.3, n=16)
        face(ctx, DAD, P(eye='smug', mouth='grin', head=0), 540, 960, 280, -0.06)
        sweat(ctx, 540 + 270, 960 - 180, il, 1.3)
        ctx.restore()
        label2(ctx, "\"...I KNEW that.", "It was a TEST.\"", WHITE, pop(il, 3, 7), 104, col2=YEL, y=1400)


def s5(ctx, f):
    lf = f - 460
    if lf < 60:
        # the bus: rolls in, family waves, rolls out
        ctx.save(); cam(ctx, 540, 1060, 0.78, 0, shake_at(lf, [20], 5, 8), f)
        ctx.rectangle(-1000, -1000, 3200, 4000); setc(ctx, hx('8fd8ff')); ctx.fill()
        for k in range(-3, 5):
            rect_r(ctx, k * 330 - 120, 520 + 120 * (k % 2), 260, 900, 8); fl(ctx, [hx('ffb3a0'), hx('ffd9a8'), hx('c8b8ff')][k % 3], 7)
            for j in range(4):
                rect_r(ctx, k * 330 - 80, 600 + 120 * (k % 2) + j * 180, 70, 90, 8); fl(ctx, hx('bfe8ff'), 5)
        ctx.rectangle(-1000, FLOOR, 3200, 2000); setc(ctx, hx('6a6e80')); ctx.fill()
        ctx.rectangle(-1000, FLOOR - 30, 3200, 40); fl(ctx, hx('d8deea'), 6)
        if lf < 20:
            bx = 1900 - 1360 * eout(lf / 20)
        elif lf < 38:
            bx = 540
        else:
            bx = 540 - 1700 * ein(pop(lf, 38, 60))
        bus(ctx, bx, FLOOR + 90, 1.05, faces=True, lf=lf)
        ctx.restore()
        if lf < 38:
            label1(ctx, "\"Bus 42... HOME!\"", WHITE, pop(lf, 20, 24), 116, -0.04, y=1420)
        else:
            label(ctx, "*VROOOM*", 540, 1420, 110, YEL, -0.05, pop(lf, 38, 41))
    elif lf < 130:
        il = lf - 60
        # home: the driveway is EMPTY
        ctx.save(); cam(ctx, 600, 1230, 1.2 + 0.08 * eout(pop(il, 30, 50)), 0, shake_at(il, [30], 14, 24), f)
        house_ext(ctx)
        tw = eout(pop(il, 4, 60))
        tumbleweed(ctx, 1150 - 800 * tw, 1330 - 30 * abs(math.sin(il * 0.4)), 50, -il * 0.3)
        shock = il >= 30
        family_wide(ctx, il, 520, dad_p=P(eye='shock' if shock else 'happy', mouth='scream' if shock else 'grin', lsh=-150 if shock else 10, rsh=150 if shock else -10, lel=-30, rel=30),
                    mom_p=P(eye='normal', mouth='flat', lsh=8, rsh=-8), boy_p=P(eye='shock' if shock else 'happy', mouth='open'), k=0.85, g=FLOOR + 40, bags_on=not shock)
        ctx.restore()
        if not shock:
            label1(ctx, "\"Home sweet—\"", WHITE, pop(il, 4, 8), 120, -0.04, y=1420)
        else:
            label2(ctx, "\"WHERE'S", "OUR CAR?!\"", WHITE, pop(il, 30, 34), 128, col2=RED, y=1400)
        card(ctx, 'p5', f, 522, 586)
    elif lf < 166:
        il = lf - 130
        # Mom deadpan ECU
        ctx.save(); cam(ctx, 540, 960, 1.05 + 0.05 * eout(pop(il, 0, 36)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8fc4')); ctx.fill()
        for k in range(6):
            ellipse(ctx, 540, 960, 280 + k * 170, 280 + k * 170); setc(ctx, (1, 1, 1, 0.25)); ctx.set_line_width(30); ctx.stroke()
        face(ctx, MOM, P(eye='glare', mouth='flat', head=0), 540, 960, 300, -0.04)
        ctx.restore()
        label2(ctx, "\"You drove it", "to WORK. Yesterday.\"", WHITE, pop(il, 2, 6), 100, col2=YEL, y=1400)
    else:
        il = lf - 166
        opening_face(ctx, f, il)
        label(ctx, "*DING!*", 540, 640, 90, WHITE, 0.08, pop(il, 0, 3) * (1 - pop(il, 10, 14)))
        card(ctx, 'p1', f, 626)


SHOTS = [(0, s1), (90, s2), (200, s3), (330, s4), (460, s5)]
CUTS = (45, 90, 118, 146, 174, 200, 252, 260, 330, 380, 422, 460, 520, 590, 626)


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
                              "-i", "out/park_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
