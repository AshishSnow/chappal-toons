"""'Unexpected Item in the Bagging Area' - original, general-audience comedy short, 22s.
Hook: Dad ECU, red alarm light flashing on his sweaty face, robot box "UNEXPECTED ITEM IN BAGGING AREA." + caption.
Beat 1: store wide: huge line at the cashier, Dad + kid stroll past "Long line? PFF. SELF-CHECKOUT!"
        kiosk: BEEP banana -> into the bag -> RED LIGHT "UNEXPECTED ITEM" -> "It's a BANANA!!"
Beat 2: lift it -> "PLACE ITEM IN BAGGING AREA." / put it down -> "UNEXPECTED ITEM." ping-pong snap cuts
Beat 3: split screen: twitching Dad "I'm... BEGGING you." / kiosk with angry screen eyes
        "20 MINUTES LATER": pull back -> enormous line behind Dad, cashier lane EMPTY "NEXT!"
Twist: Dad heaves the heavy bag -> the KID pops out of it "HI, DAD!" -> Dad ECU "...UNEXPECTED ITEM."
End: green screen "THANK YOU!" -> kid dives back in "AGAIN!!" -> red light -> Dad ECU loop."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, _SCR
from scenes48 import label2
from scenes58 import sweat, twitch
from scenes8 import sit, walk
import scenes13
from scenes13 import card as _card13
import random


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


DAD = dict(doodle.DAD, shirt=hx('3d7bff'), pants=hx('2a3a6a'))
BOY = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff8a1f'))
Q1 = dict(doodle.NEIGHBOR, shirt=hx('8fd8ff'))
Q2 = dict(doodle.NMOM, shirt=hx('ff5fa8'))
Q3 = dict(doodle.UNCLE, shirt=hx('22b45a'))
Q4 = dict(doodle.MOM_G, shirt=hx('ffc93c'), hair=hx('6a3a20'))
Q5 = dict(doodle.NEIGHBOR, shirt=hx('ff3b5c'), tie=None, glasses=None, hair=hx('c9a050'))
CASH = dict(doodle.MOM_G, shirt=hx('19b5a5'), hair=hx('1d1820'))
N = 660
RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); TEAL = hx('19b5a5'); WHITE = (1, 1, 1); SKY = hx('8fd8ff')
FLOOR = 1460
KX, KS = 560, 0.72
BX, BY, BS = KX + 350 * KS, FLOOR - 420 * KS, 0.85


def shop_cam(ctx, cx, z, rot=0, sh=0, f=0, fy=1600):
    cam(ctx, cx, FLOOR - (fy - 960) / z, z, rot, sh, f)

CAPS = {
    'p1': [[("Every ", OUT), ("DAD", BLUE), (" at", OUT)], [("SELF-CHECKOUT:", RED)]],
    'p3': [[("20 MINUTES", PURPLE)], [("LATER...", OUT)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def robo(ctx, l1, l2, t, y=1330, good=False):
    """machine-voice box: dark screen bubble with glowing caps text"""
    if t <= 0:
        return
    u = eout(min(1, t * 2))
    ctx.save(); ctx.translate(540, y); ctx.scale(0.6 + 0.4 * u, 0.6 + 0.4 * u)
    col = hx('5dff7a') if good else hx('ff4d5e')
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    sz = 62
    ctx.set_font_size(sz)
    ws = [ctx.text_extents(s).x_advance for s in (l1, l2) if s]
    if max(ws) > 760:
        sz *= 760 / max(ws); ctx.set_font_size(sz); ws = [ctx.text_extents(s).x_advance for s in (l1, l2) if s]
    nl = 2 if l2 else 1
    w = max(ws) + 90; h = sz * 1.25 * nl + 50
    rect_r(ctx, -w / 2 + 10, -h / 2 + 12, w, h, 28); setc(ctx, (0, 0, 0, 0.35)); ctx.fill()
    rect_r(ctx, -w / 2, -h / 2, w, h, 28); fl(ctx, hx('1a1830'), 8)
    # little speaker grille icon on the left edge
    for k in range(3):
        ctx.new_path(); ctx.arc(-w / 2 + 6, 0, 16 + k * 12, -0.7, 0.7); setc(ctx, col + (0.0,)); ctx.stroke()
    yy = -h / 2 + 25 + sz * 0.95
    for s, wd in zip([s for s in (l1, l2) if s], ws):
        ctx.move_to(-wd / 2, yy); ctx.text_path(s)
        setc(ctx, col + (0.35,)); ctx.set_line_width(10); ctx.stroke_preserve()
        setc(ctx, col); ctx.fill()
        yy += sz * 1.25
    ctx.restore()


def banana(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-70, -20); ctx.curve_to(-40, 40, 40, 40, 70, -20)
    ctx.curve_to(40, 14, -40, 14, -70, -20); ctx.close_path(); fl(ctx, hx('ffe14d'), 6)
    ctx.rectangle(64, -34, 14, 18); fl(ctx, hx('6a4a20'), 4)
    ctx.restore()


def bag(ctx, x, y, s=1.0, lean=0.0, full=True):
    """paper shopping bag, bottom-centre at (x, y)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(lean); ctx.scale(s, s)
    if full:
        rect_r(ctx, -60, -260, 50, 80, 12); fl(ctx, hx('8fd8ff'), 6)      # cereal-ish box poking out
        ctx.new_path(); ctx.arc(30, -240, 34, 0, 2 * math.pi); fl(ctx, hx('ff3b5c'), 6)   # apple
        ctx.new_path(); ctx.move_to(30, -272); ctx.line_to(36, -290); ink(ctx, 5); ctx.stroke()
    poly(ctx, [(-120, 0), (120, 0), (108, -230), (-108, -230)]); fl(ctx, hx('d9a46a'), 8)
    poly(ctx, [(-108, -230), (108, -230), (100, -250), (-100, -250)]); fl(ctx, hx('c48c52'), 6)
    ctx.restore()


def kiosk(ctx, x, lf, state='idle', s=KS, bag_=True, bag_lean=0.0, angry=False):
    """self-checkout kiosk; x = centre of scanner. state: idle | red | green"""
    ctx.save(); ctx.translate(x, FLOOR); ctx.scale(s, s)
    # cabinet
    rect_r(ctx, -200, -560, 400, 560, 20); fl(ctx, hx('dfe6f0'), 8)
    ctx.rectangle(-170, -420, 340, 18); setc(ctx, hx('b8c2d2')); ctx.fill()
    # scanner glass
    rect_r(ctx, -170, -600, 340, 60, 12); fl(ctx, hx('3a3a4a'), 7)
    ctx.rectangle(-140, -586, 280, 30); setc(ctx, hx('2a5a4a')); ctx.fill()
    ctx.move_to(-140, -571); ctx.line_to(140, -571); setc(ctx, (1, 0.2, 0.25, 0.8)); ctx.set_line_width(5); ctx.stroke()
    # bagging platform (right)
    ctx.rectangle(200, -380, 300, 380); fl(ctx, hx('c9d2e0'), 8)
    rect_r(ctx, 190, -420, 320, 44, 10); fl(ctx, hx('9aa6ba'), 7)
    # pole + screen
    ctx.rectangle(-26, -1000, 52, 400); fl(ctx, hx('9aa6ba'), 6)
    scol = {'idle': hx('1f8bff'), 'red': hx('ff3b5c'), 'green': hx('22b45a')}[state]
    if state == 'red' and (lf // 4) % 2:
        scol = dark(scol, 0.8)
    rect_r(ctx, -190, -1190, 380, 280, 24); fl(ctx, hx('2a2a3a'), 8)
    rect_r(ctx, -166, -1166, 332, 232, 14); setc(ctx, scol); ctx.fill()
    if state == 'green':
        poly(ctx, [(-60, -1050), (-15, -1000), (70, -1110)]); setc(ctx, WHITE); ctx.set_line_width(26)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    elif state == 'red' or angry:
        # angry pixel eyes
        for sx in (-1, 1):
            ctx.rectangle(sx * 70 - 28, -1070, 56, 56); setc(ctx, WHITE); ctx.fill()
            poly(ctx, [(sx * 110, -1120), (sx * 20, -1088), (sx * 20, -1074), (sx * 110, -1100)]); setc(ctx, hx('1a1830')); ctx.fill()
        ctx.rectangle(-60, -985, 120, 16); setc(ctx, WHITE); ctx.fill()
    else:
        for sx in (-1, 1):
            ctx.rectangle(sx * 70 - 22, -1080, 44, 54); setc(ctx, WHITE); ctx.fill()
        ctx.new_path(); ctx.arc(0, -1010, 60, 0.3, math.pi - 0.3); setc(ctx, WHITE); ctx.set_line_width(14); ctx.stroke()
    # beacon light on top
    ctx.rectangle(-14, -1250, 28, 60); fl(ctx, hx('9aa6ba'), 5)
    on = state == 'red' and (lf // 4) % 2 == 0
    if state == 'red':
        rays(ctx, 0, -1290, 50, 420, lf * 0.35, col=(1, 0.2, 0.25), a=0.28 if on else 0.12, n=10)
    ctx.new_path(); ctx.arc(0, -1290, 52, math.pi, 2 * math.pi); ctx.line_to(52, -1250); ctx.line_to(-52, -1250); ctx.close_path()
    fl(ctx, hx('ff3b5c') if on else (hx('7a2a3a') if state == 'red' else hx('8a8f9a')), 7)
    ctx.restore()
    if bag_:
        bag(ctx, x + 350 * s, FLOOR - 420 * s, BS, bag_lean)


def store(ctx, lf, x0=-3000, x1=4000):
    ctx.rectangle(x0, -3000, x1 - x0, 7000); setc(ctx, hx('fff1d6')); ctx.fill()
    # shelves on the back wall
    rnd = random.Random(2)
    cols = [RED, BLUE, GREEN, GOLD, PINK, TEAL, ORANGE, PURPLE]
    for sx in range(-2400, 3600, 520):
        ctx.rectangle(sx, 560, 480, 620); fl(ctx, hx('e7c79a'), 7)
        for row in range(3):
            yy = 560 + 40 + row * 200
            ctx.rectangle(sx, yy + 150, 480, 16); setc(ctx, hx('b98a5a')); ctx.fill()
            xx = sx + 20
            while xx < sx + 440:
                w_ = rnd.choice((50, 60, 70)); h_ = rnd.choice((90, 110, 130))
                rect_r(ctx, xx, yy + 150 - h_, w_, h_, 8); fl(ctx, rnd.choice(cols), 4)
                xx += w_ + 10
    ctx.rectangle(x0, FLOOR, x1 - x0, 1500); setc(ctx, hx('e9eef5')); ctx.fill()
    for i in range(-30, 40):
        ctx.move_to(i * 160, FLOOR); ctx.line_to(i * 160 - 200, FLOOR + 600); setc(ctx, hx('c9d2e0')); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(x0, FLOOR); ctx.line_to(x1, FLOOR); ink(ctx, 8); ctx.stroke()


def hang_sign(ctx, x, y, s, col, w=520):
    ctx.move_to(x - w / 3, y - 300); ctx.line_to(x - w / 3, y - 50); ctx.move_to(x + w / 3, y - 300); ctx.line_to(x + w / 3, y - 50)
    ink(ctx, 5); ctx.stroke()
    rect_r(ctx, x - w / 2, y - 60, w, 110, 18); fl(ctx, col, 7)
    text(ctx, s, x, y + 14, 56, WHITE, ow=8, shadow=False)


def counter(ctx, x):
    """regular cashier counter"""
    rect_r(ctx, x - 230, FLOOR - 420, 460, 420, 16); fl(ctx, hx('5a6a8a'), 8)
    rect_r(ctx, x - 250, FLOOR - 450, 500, 50, 10); fl(ctx, hx('2a2a3a'), 7)
    rect_r(ctx, x + 60, FLOOR - 600, 150, 150, 14); fl(ctx, hx('dfe6f0'), 6)


def basket(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, -40, 70, math.pi, 2 * math.pi); setc(ctx, INK); ctx.set_line_width(9); ctx.stroke()
    banana(ctx, -10, -40, 0.6, -0.2)
    poly(ctx, [(-90, -40), (90, -40), (70, 60), (-70, 60)]); fl(ctx, RED, 7)
    for k in range(-2, 3):
        ctx.move_to(k * 30, -30); ctx.line_to(k * 24, 50); setc(ctx, dark(RED, 0.7)); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def red_glow(ctx, lf, a=0.28):
    if (lf // 4) % 2 == 0:
        g = cairo.RadialGradient(120, 300, 50, 120, 300, 1400)
        g.add_color_stop_rgba(0, 1, 0.15, 0.2, a); g.add_color_stop_rgba(1, 1, 0.15, 0.2, 0)
        ctx.set_source(g); ctx.paint()


# ------------------------------------------------------------------ close-ups
def dad_ecu(ctx, f, lf, bg, eye='shock', mouth='wavy', z0=1.0, shake=0, tw=True, alarm=True, sw=True, rot=None):
    ctx.save(); cam(ctx, 540, 960, z0, 0, shake, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    rays(ctx, 540, 900, 260, 1700, lf * 0.03, col=(1, 1, 1), a=0.2, n=18)
    cx, cy, R = 540, 880, 300
    face(ctx, DAD, P(eye=eye, mouth=mouth), cx, cy, R, 0.03 * math.sin(lf * 0.7) if rot is None else rot)
    if sw:
        sweat(ctx, cx + 0.85 * R, cy - 0.45 * R, lf, 1.3); sweat(ctx, cx - 0.75 * R, cy - 0.2 * R, lf + 20, 1.0)
    if tw:
        twitch(ctx, cx + 0.55 * R, cy - 0.7 * R, lf, 1.3)
    ctx.restore()
    if alarm:
        red_glow(ctx, lf, 0.4)


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    dad_ecu(ctx, f, lf, hx('ffb36b'), z0=1.0 + 0.07 * eio(pop(lf, 0, 54)), shake=4 if (lf // 4) % 2 == 0 else 2)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    robo(ctx, "UNEXPECTED ITEM", "IN BAGGING AREA.", 1 if lf == f else pop(lf, 0, 3), y=1390)


def queue_people(ctx, x0, lf, n=4, dx=170, k=1.05, bored=False, face_=-1):
    chars = [Q1, Q2, Q3, Q4, Q5, Q1, Q2, Q3, Q4, Q5, Q1, Q2, Q3, Q4]
    for i in range(n):
        ch = chars[i % len(chars)]
        tap = 6 * math.sin(lf * 0.5 + i) if bored else 0
        eye = 'closed' if (bored and i % 3 == 1) else ('glare' if bored else 'normal')
        p = P(eye=eye, mouth='flat' if bored else 'smile', lsh=10, rsh=-10 if i % 2 else 20, lhip=tap, rhip=-tap, head=4 * math.sin(lf * 0.1 + i))
        if bored and i % 3 == 2:
            p.update(rsh=-150, rel=-30)   # tapping a watch / fist
        draw(ctx, x0 + i * dx, FLOOR - 186 * k, k, face_, ch, p)
        if bored and i % 3 == 1:
            label(ctx, "z", x0 + i * dx + 60, FLOOR - 186 * k * 2.4 - (lf * 2) % 60, 50, WHITE, 0.1, 1)


# ------------------------------------------------------------------ shots
DADX = 250
DK = 1.6


def s2(ctx, f):
    lf = f - 54
    if lf < 50:
        # store wide: long cashier line on the left, Dad + kid strolling right
        ctx.save(); shop_cam(ctx, 380 + 300 * eio(pop(lf, 0, 50)), 0.72, 0, 0, f)
        store(ctx, lf)
        hang_sign(ctx, -200, 400, "CHECKOUT", BLUE, 460)
        draw(ctx, -330, FLOOR - 186 * 1.9, 1.9, 1, CASH, P(eye='closed', mouth='flat', lsh=20, rsh=-20))
        counter(ctx, -300)
        queue_people(ctx, -60, lf, 4, 150, 1.15, bored=True)
        dx_ = 560 + 380 * eio(pop(lf, 0, 50))
        bd = draw(ctx, dx_, FLOOR - 186 * DK, DK, 1, DAD, walk(lf * 0.5, eye='smug', mouth='grin', rsh=-40, rel=-90))
        basket(ctx, bd['front'][0], bd['front'][1] + 40, 1.0)
        draw(ctx, dx_ + 200, FLOOR - 186 * 0.95, 0.95, 1, BOY, walk(lf * 0.6 + 1, eye='happy', mouth='grin'))
        hang_sign(ctx, 1250, 400, "SELF-CHECKOUT", GREEN, 640)
        ctx.restore()
        label2(ctx, "\"Long line? PFF.", "SELF-CHECKOUT!\"", WHITE, pop(lf, 6, 10), 100, col2=GREEN, y=520)
    else:
        il = lf - 50   # 0..76
        RED_AT = 26
        st = 'red' if il >= RED_AT else 'idle'
        ctx.save(); shop_cam(ctx, 560, 1.1 + 0.06 * eio(pop(il, RED_AT, RED_AT + 8)), 0, shake_at(il, [RED_AT], 14, 22), f)
        store(ctx, il)
        kiosk(ctx, KX, il, st)
        if il < 10:
            pp = P(eye='smug', mouth='grin', rsh=-70, rel=-20, lsh=20)
        elif il < 20:
            pp = P(eye='smug', mouth='grin', rsh=-100, rel=-10, lsh=20)
        elif il < RED_AT:
            pp = P(eye='happy', mouth='grin', rsh=-80, rel=-10, lsh=20)
        else:
            pp = P(eye='shock', mouth='scream', rsh=-150, rel=-30, lsh=150, lel=30, torso=-8)
        bd = draw(ctx, DADX, FLOOR - 186 * DK, DK, 1, DAD, pp)
        if il < 10:
            hxp, hyp = bd['front']
            banana(ctx, hxp + 30, hyp - 10, 0.8, -0.3)
        elif il < 20:
            t = pop(il, 10, 20)
            banana(ctx, lerp(KX, BX, eio(t)), lerp(FLOOR - 470, BY - 130, eio(t)) - 100 * math.sin(math.pi * t), 0.8, 0.2)
        else:
            banana(ctx, BX, BY - 130, 0.8, 0.1)
        ctx.restore()
        if 8 <= il < 18:
            label(ctx, "BEEP!", 600, 640, 100, YEL, 0.06, pop(il, 8, 10))
        if il >= RED_AT:
            red_glow(ctx, il, 0.3)
            robo(ctx, "UNEXPECTED ITEM", "IN BAGGING AREA.", pop(il, RED_AT, RED_AT + 3), y=390)
        if il >= 48:
            label2(ctx, "\"It's a", "BANANA!!\"", WHITE, pop(il, 48, 52), 120, col2=YEL, y=1400)


def kiosk_close(ctx, f, il, lifted, st, txt, z=1.2, sh=0):
    """tighter angle on the bagging area: Dad's arm lifting / dropping the banana"""
    ctx.save(); shop_cam(ctx, 600, z, -4 if lifted else 4, sh, f)
    store(ctx, il)
    kiosk(ctx, KX, il, st, bag_=True)
    p = P(eye='glare' if not lifted else 'shock', mouth='wavy', rsh=-160 if lifted else -100, rel=-20 if lifted else -5, lsh=20, torso=6)
    bd = draw(ctx, DADX + 160, FLOOR - 186 * DK, DK, 1, DAD, p)
    hxp, hyp = bd['front']
    if lifted:
        banana(ctx, hxp + 20, hyp - 10, 0.8, 0.1)
    else:
        banana(ctx, BX, BY - 130, 0.8, 0.1)
    ctx.restore()
    red_glow(ctx, il, 0.3)
    robo(ctx, txt[0], txt[1], pop(il, 0, 3), y=390)


def s3(ctx, f):
    lf = f - 180
    if lf < 80:
        # ping-pong: lift -> PLACE ITEM / drop -> UNEXPECTED ITEM, cuts get faster
        seg = [0, 22, 40, 54, 64, 72, 80]
        k = max(i for i in range(len(seg) - 1) if seg[i] <= lf)
        il = lf - seg[k]
        lifted = k % 2 == 0
        txt = ("PLEASE PLACE ITEM", "IN BAGGING AREA.") if lifted else ("UNEXPECTED ITEM", "IN BAGGING AREA.")
        kiosk_close(ctx, f, il, lifted, 'red', txt, 1.15 + 0.04 * k, shake_at(il, [0], 8, 12 + 3 * k))
        if lf < 22:
            label(ctx, "*lift*", 540, 1400, 90, WHITE, -0.06, pop(il, 0, 3))
        elif lf < 40:
            label(ctx, "*plop*", 540, 1400, 90, WHITE, 0.06, pop(il, 0, 3))
        else:
            label(ctx, "UP!" if lifted else "DOWN!", 540, 1400, 140, YEL if lifted else ORANGE, -0.05 if lifted else 0.05, pop(il, 0, 2))
    else:
        il = lf - 80   # 0..60 split screen
        ctx.save(); ctx.rectangle(0, 0, W, H / 2); ctx.clip()
        ctx.translate(0, -300)
        dad_ecu(ctx, f, il, hx('ffb36b'), eye='glare', mouth='wavy', z0=0.85, shake=2, alarm=False)
        ctx.restore()
        ctx.save(); ctx.rectangle(0, H / 2, W, H / 2); ctx.clip()
        ctx.rectangle(0, H / 2, W, H / 2); setc(ctx, hx('3a3a52')); ctx.fill()
        rays(ctx, 540, 1400, 100, 1200, il * 0.03, col=(1, 0.3, 0.35), a=0.15, n=16)
        ctx.translate(540, 1330); ctx.scale(2.0, 2.0); ctx.translate(-KX, -(FLOOR - 1050 * KS))
        kiosk(ctx, KX, il, 'red', bag_=False)
        ctx.restore()
        red_glow(ctx, il, 0.25)
        ctx.rectangle(0, H / 2 - 8, W, 16); setc(ctx, OUT); ctx.fill()
        label2(ctx, "\"I'm... BEGGING", "you...\"", WHITE, pop(il, 4, 8), 96, col2=YEL, y=850)
        if il >= 28:
            robo(ctx, "UNEXPECTED ITEM.", "", pop(il, 28, 31), y=1590 - 140)


def s4(ctx, f):
    lf = f - 320
    if lf < 66:
        # pull back + pan along an endless line to the EMPTY cashier lane
        t1 = eio(pop(lf, 0, 18)); t2 = eio(pop(lf, 20, 44))
        z = lerp(lerp(1.1, 0.6, t1), 0.8, t2); cx = lerp(lerp(560, 0, t1), -3050, t2)
        ctx.save(); shop_cam(ctx, cx, z, 0, 0, f)
        store(ctx, lf, -6000, 4000)
        kiosk(ctx, KX, lf, 'red')
        bd = draw(ctx, DADX, FLOOR - 186 * DK, DK, 1, DAD, P(eye='glare', mouth='wavy', rsh=-150, rel=-20, lsh=20))
        banana(ctx, bd['front'][0] + 20, bd['front'][1] - 10, 0.8, 0.1)
        queue_people(ctx, -2650, lf, 16, 170, 1.25, bored=True, face_=1)
        draw(ctx, -3330, FLOOR - 186 * 1.9, 1.9, 1, CASH, P(eye='happy', mouth='smile', rsh=-160, rel=-20, lsh=20))
        counter(ctx, -3300)
        hang_sign(ctx, -3300, 560, "CHECKOUT", BLUE, 460)
        ctx.restore()
        card(ctx, 'p3', f, 322, 380)
        if lf >= 44:
            label(ctx, "\"NEXT!\"", 330, 720, 120, GREEN, -0.06, pop(lf, 44, 48))
            label(ctx, "(empty lane)", 540, 1400, 80, WHITE, 0.03, pop(lf, 48, 52))
    elif lf < 116:
        # Dad heaves the heavy bag -> kid pops out
        il = lf - 66
        POP = 26
        ctx.save(); shop_cam(ctx, 640, 1.15, 0, shake_at(il, [POP], 12, 26) + (3 if il < POP else 0), f)
        store(ctx, il)
        kiosk(ctx, KX, il, 'red', bag_=False)
        lift = 110 * eio(pop(il, 4, POP)) + 6 * math.sin(il * 1.7) * (il < POP)
        bx, by = BX, BY - lift
        dp = P(eye='closed' if il < POP else 'shock', mouth='wavy' if il < POP else 'scream', rsh=-120, rel=-50, lsh=-110, lel=-60, torso=-10)
        draw(ctx, 560, FLOOR - 186 * DK, DK, 1, DAD, dp)
        if il >= POP:
            u = eout(pop(il, POP, POP + 7))
            ctx.save(); ctx.rectangle(-5000, -5000, 10000, by - 30 + 5000); ctx.clip()
            draw(ctx, bx, by - 20 - 186 * 0.85 + 220 * (1 - u) - 130 * u, 0.85, -1, BOY,
                 P(eye='happy', mouth='grin', rsh=-150 * u, lsh=150 * u, rel=-20, lel=-20))
            ctx.restore()
        bag(ctx, bx, by, BS, 0.03 * math.sin(il * 1.3), full=il < POP)
        ctx.restore()
        if il < POP:
            red_glow(ctx, il, 0.25)
            label(ctx, "\"HNNNGH!!\"", 540, 420, 120, WHITE, -0.05, pop(il, 3, 7))
        else:
            label(ctx, "*POP!*", 540, 420, 120, YEL, 0.06, pop(il, POP, POP + 3))
            label2(ctx, "\"HI,", "DAD!!\"", WHITE, pop(il, POP + 4, POP + 8), 140, col2=ORANGE, y=1400)
    else:
        il = lf - 116   # 0..34
        dad_ecu(ctx, f, il, PURPLE, eye='shock', mouth='flat', z0=1.0 + 0.06 * eout(pop(il, 0, 34)), tw=True, alarm=False, sw=False)
        label2(ctx, "\"...UNEXPECTED", "ITEM.\"", WHITE, pop(il, 3, 7), 110, col2=YEL, y=1400)


def s5(ctx, f):
    lf = f - 470
    if lf < 90:
        DIVE = 50
        st = 'green' if lf < DIVE + 10 else 'red'
        ctx.save(); shop_cam(ctx, 540, 1.05, 0, shake_at(lf, [DIVE + 10], 12, 24), f)
        store(ctx, lf)
        kiosk(ctx, KX, lf, st, bag_=False)
        bag(ctx, BX, BY, BS, 0, full=False)
        if lf < DIVE:
            draw(ctx, 360, FLOOR - 186 * DK, DK, 1, DAD, P(eye='happy', mouth='grin', rsh=-150, rel=-20, lsh=150, lel=20))
            draw(ctx, 140, FLOOR - 186 * 0.95, 0.95, 1, BOY, P(eye='happy', mouth='grin', rsh=-60, lsh=40))
        else:
            t = pop(lf, DIVE, DIVE + 10)
            draw(ctx, 360, FLOOR - 186 * DK, DK, 1, DAD, P(eye='shock', mouth='scream', rsh=-160, rel=-30, lsh=160, lel=30, torso=-6))
            if t < 1:
                kx = lerp(140, BX, eio(t)); ky = FLOOR - 186 * 0.95 - 500 * math.sin(math.pi * t)
                ctx.save(); ctx.translate(kx, ky + 140); ctx.rotate(1.2 * t); ctx.translate(-kx, -ky - 140)
                draw(ctx, kx, ky, 0.95, 1, BOY, P(eye='happy', mouth='grin', rsh=-170, lsh=170, lhip=-20, rhip=-30))
                ctx.restore()
                bag(ctx, BX, BY, BS, 0, full=False)
            else:
                top = BY - 250 * BS
                ctx.new_path(); ctx.arc(BX, top + 8, 62, math.pi, 2 * math.pi); fl(ctx, BOY['hair'], 6)
                bag(ctx, BX, BY, BS, 0.03 * math.sin(lf), full=False)
                for sx in (-1, 1):
                    ellipse(ctx, BX + sx * 80, top - 10 - 12 * abs(math.sin(lf * 0.8 + sx)), 24, 24); fl(ctx, BOY['skin'], 5)
        ctx.restore()
        if lf < DIVE:
            sparkle(ctx, 300, 700, 30 + 8 * math.sin(lf * 0.6)); sparkle(ctx, 860, 640, 24 + 8 * math.cos(lf * 0.6))
            robo(ctx, "THANK YOU!", "", pop(lf, 0, 3), y=390, good=True)
            if lf < 30:
                label2(ctx, "\"FINALLY!", "FREEDOM!!\"", WHITE, pop(lf, 6, 10), 120, col2=GREEN, y=1400)
            else:
                label2(ctx, "\"Dad! Dad!", "AGAIN!!\"", WHITE, pop(lf, 30, 34), 120, col2=ORANGE, y=1400)
        elif lf < DIVE + 10:
            label(ctx, "*WHEEE!*", 540, 1400, 120, ORANGE, -0.06, 1)
        else:
            red_glow(ctx, lf, 0.35)
            robo(ctx, "UNEXPECTED ITEM", "IN BAGGING AREA.", pop(lf, DIVE + 10, DIVE + 13), y=390)
            label(ctx, "*FLOMP!*", 540, 1400, 120, YEL, 0.06, pop(lf, DIVE + 10, DIVE + 12))
    elif lf < 140:
        il = lf - 90
        dad_ecu(ctx, f, il, RED, eye='shock', mouth='scream', z0=1.0 + 0.1 * eout(pop(il, 0, 50)), shake=6, tw=True)
        label(ctx, "\"NOOOO!!\"", 540, 1420, 160, YEL, -0.05, pop(il, 2, 5))
    else:
        s1(ctx, f, f - 610 + 18)


SHOTS = [(0, s1), (54, s2), (180, s3), (320, s4), (470, s5)]
CUTS = (54, 104, 180, 202, 220, 234, 244, 252, 260, 320, 386, 436, 470, 560, 610)


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
                              "-i", "out/unexpected_item_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
