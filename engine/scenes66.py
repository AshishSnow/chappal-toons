"""'MOM! WATCH THIS!' - original, general-audience comedy short, 22s.
Hook: soaked kid ECU with goggles, yelling "MOM! MOM! WATCH THIS!!" + caption "Every kid at the pool:"
Beat 1: wide pool deck: huge wind-up... tiny hop *plip*. Mom on the lounger, flat: "Wow. AMAZING."
Beat 2: underwater cross-section: kid holds breath, cheeks inflate, "1... 2... 3!!" -> bursts up "NEW RECORD!!"
Beat 3: "WATCH THIS #47": Mom ECU, sunglasses slide down -> she's asleep "wow... so... amazing..." -> "I'M WATCHING!!"
Twist: low-angle diving board: Dad "Hey family... WATCH THIS." -> CANNONBALL -> KER-SPLOOSH fills the lens
 -> the pool is EMPTY, Mom + kid drenched, Dad at the bottom: "...did you SEE that?!" / "...we SAW."
End: kid turns to Dad "DAD! DAD! WATCH THIS!!" -> Dad in Mom's shades + hat, dead-eyed "...wow. AMAZING."
 -> Mom smug with a drink "Welcome to MY life." -> kid ECU loop."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, zzz, eye_pos, _SCR
from scenes48 import label1, label2
from scenes58 import sweat, twitch
import scenes13
from scenes13 import card as _card13
import random


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


SKIN_B = doodle.BOY['skin']; SKIN_D = doodle.DAD['skin']
BOY = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff3b5c'), pants=SKIN_B, shoes=SKIN_B)
DAD = dict(doodle.DAD, shirt=hx('ffc93c'), pants=SKIN_D, shoes=SKIN_D, sleeve=0.0)
MOM = dict(doodle.MOM_G, shirt=hx('19b5a5'))
N = 660
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
GOLD = hx('ffc93c')
TEAL = hx('19b5a5')
WATER = hx('35c0ff')
DEEP = hx('1a8fe0')
WHITE = (1, 1, 1)
NAVY = hx('1f3a8a')

CAPS = {
    'p1': [[("Every kid at", OUT)], [("the pool:", BLUE)]],
    'p2': [[("WATCH THIS", OUT), (" #2", BLUE)]],
    'p3': [[("WATCH THIS", OUT), (" #47", RED)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def drops(ctx, x, y, lf, n=3, s=1.0, spread=200, seed=1):
    rnd = random.Random(seed)
    for k in range(n):
        dx = rnd.uniform(-spread, spread); ph = ((lf * 2.2 + rnd.uniform(0, 100)) % 100) / 100
        yy = y + ph * 220 * s
        ctx.new_path(); ctx.move_to(x + dx, yy - 30 * s); ctx.curve_to(x + dx + 20 * s, yy, x + dx + 16 * s, yy + 22 * s, x + dx, yy + 22 * s)
        ctx.curve_to(x + dx - 16 * s, yy + 22 * s, x + dx - 20 * s, yy, x + dx, yy - 30 * s); fl(ctx, hx('8fe0ff'), 4)


def goggles(ctx, cx, cy, R, on_eyes=False):
    """swim goggles; on the forehead by default"""
    y = cy + (0.06 * R if on_eyes else -0.58 * R)
    ctx.new_path(); ctx.move_to(cx - 1.02 * R, y + 0.02 * R); ctx.line_to(cx + 1.02 * R, y - 0.02 * R)
    ink(ctx, R * 0.13); ctx.stroke()
    ctx.new_path(); ctx.move_to(cx - 1.02 * R, y + 0.02 * R); ctx.line_to(cx + 1.02 * R, y - 0.02 * R)
    setc(ctx, PURPLE); ctx.set_line_width(R * 0.08); ctx.stroke()
    for ex in (cx - 0.2 * R, cx + 0.42 * R):
        ellipse(ctx, ex, y, R * 0.21, R * 0.17); setc(ctx, hx('8fe8ff') + (0.85,)); ctx.fill_preserve()
        setc(ctx, YEL); ctx.set_line_width(R * 0.05); ctx.stroke_preserve(); ink(ctx, R * 0.02); ctx.stroke()
        ellipse(ctx, ex - R * 0.07, y - R * 0.05, R * 0.05, R * 0.035); setc(ctx, WHITE); ctx.fill()


def shades(ctx, cx, cy, R, dy=0.0, col=INK):
    """sunglasses over a face drawn by face() at (cx, cy, R); dy in R units (slides down the nose)"""
    for ex, ey, rx in eye_pos(cx, cy, R):
        rect_r(ctx, ex - R * 0.27, ey - R * 0.17 + dy * R, R * 0.54, R * 0.36, R * 0.12); fl(ctx, col, R * 0.02)
        ctx.new_path(); ctx.move_to(ex - R * 0.14, ey - R * 0.08 + dy * R); ctx.line_to(ex - R * 0.2, ey + R * 0.08 + dy * R)
        setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(R * 0.035); ctx.stroke()
    ctx.new_path(); ctx.move_to(cx - R * 0.0, cy - R * 0.02 + dy * R); ctx.line_to(cx + R * 0.15, cy - R * 0.02 + dy * R)
    ink(ctx, R * 0.035); ctx.stroke()


def sunhat(ctx, cx, cy, R, droop=0.0):
    by = cy - 0.72 * R
    ctx.save(); ctx.translate(cx, by); ctx.rotate(-0.08)
    ctx.new_path(); ctx.move_to(-1.5 * R, 0.05 * R + droop * 0.4 * R)
    ctx.curve_to(-1.2 * R, -0.25 * R, 1.2 * R, -0.25 * R, 1.5 * R, 0.05 * R + droop * 0.4 * R)
    ctx.curve_to(1.2 * R, 0.25 * R + droop * 0.3 * R, -1.2 * R, 0.25 * R + droop * 0.3 * R, -1.5 * R, 0.05 * R + droop * 0.4 * R)
    ctx.close_path(); fl(ctx, hx('f6d27a'), R * 0.025)
    ctx.new_path(); ctx.move_to(-0.75 * R, -0.05 * R); ctx.curve_to(-0.75 * R, -0.85 * R, 0.75 * R, -0.85 * R, 0.75 * R, -0.05 * R)
    ctx.curve_to(0.4 * R, 0.05 * R, -0.4 * R, 0.05 * R, -0.75 * R, -0.05 * R); ctx.close_path(); fl(ctx, hx('f6d27a'), R * 0.025)
    ctx.new_path(); ctx.move_to(-0.74 * R, -0.18 * R); ctx.curve_to(-0.4 * R, -0.08 * R, 0.4 * R, -0.08 * R, 0.74 * R, -0.18 * R)
    setc(ctx, PINK); ctx.set_line_width(R * 0.1); ctx.stroke()
    ctx.restore()


def drink(ctx, x, y, s=1.0, lf=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    poly(ctx, [(-50, -80), (50, -80), (34, 70), (-34, 70)]); fl(ctx, hx('ffffff'), 6)
    poly(ctx, [(-44, -50), (44, -50), (32, 64), (-32, 64)]); setc(ctx, ORANGE); ctx.fill()
    ctx.new_path(); ctx.move_to(14, -40); ctx.line_to(40, -150); ctx.line_to(80, -160); ink(ctx, 16); ctx.stroke()
    ctx.new_path(); ctx.move_to(14, -40); ctx.line_to(40, -150); ctx.line_to(80, -160); setc(ctx, PINK); ctx.set_line_width(9); ctx.stroke()
    ctx.new_path(); ctx.arc(-46, -80, 30, 0, 2 * math.pi); fl(ctx, YEL, 5)
    ctx.restore()


def book(ctx, x, y, a=0.0, s=1.0, wet=False):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-70, -50), (0, -40), (70, -50), (70, 40), (0, 50), (-70, 40)]); fl(ctx, BLUE if not wet else hx('7aa6d6'), 5)
    ctx.move_to(0, -40); ctx.line_to(0, 50); ink(ctx, 4); ctx.stroke()
    ctx.restore()


def trunks(ctx, x, hipy, k, col=NAVY):
    S = k * 1.35
    rect_r(ctx, x - 52 * S, hipy - 16 * S, 104 * S, 40 * S, 10 * S); fl(ctx, col, max(3, 3.7 * S))


# ------------------------------------------------------------------ sets
DECK_Y = 1300


def sky(ctx, y1=900):
    ctx.rectangle(-3000, -3000, 9000, 3000 + y1); setc(ctx, hx('8fd8ff')); ctx.fill()


def pool_set(ctx, lf, empty=False, wet=False):
    sky(ctx)
    ctx.new_path(); ctx.arc(900, 470, 80, 0, 2 * math.pi); fl(ctx, YEL, 6)
    ellipse(ctx, 260, 470, 100, 44); setc(ctx, WHITE); ctx.fill(); ellipse(ctx, 340, 450, 70, 50); ctx.fill()
    # hedge
    for k in range(-3, 16):
        ctx.new_path(); ctx.arc(k * 90, 780, 70, 0, 2 * math.pi); setc(ctx, hx('3fae54')); ctx.fill()
    ctx.rectangle(-3000, 780, 9000, 120); setc(ctx, hx('3fae54')); ctx.fill()
    # deck
    ctx.rectangle(-3000, 860, 9000, 3000); setc(ctx, hx('f4e2c0')); ctx.fill()
    for k in range(-20, 30):
        ctx.move_to(k * 120, 860); ctx.line_to(k * 120 - 40, DECK_Y)
    setc(ctx, hx('e6cfa6')); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-3000, 860); ctx.line_to(6000, 860); ink(ctx, 6); ctx.stroke()
    if wet:
        for x, y, rx in ((520, 1000, 120), (880, 940, 90), (200, 1270, 140), (1000, 1200, 80)):
            ellipse(ctx, x, y, rx, rx * 0.22); setc(ctx, hx('8fe0ff')); ctx.fill()
    # pool
    ctx.rectangle(-3000, DECK_Y, 9000, 3000)
    if empty:
        setc(ctx, hx('cdeeff')); ctx.fill()
        ctx.rectangle(-3000, DECK_Y, 9000, 110); setc(ctx, hx('9fd6f2')); ctx.fill()
        for i in range(-10, 20):
            ctx.move_to(i * 110, DECK_Y + 110); ctx.line_to(i * 110, 3000)
        for j in range(0, 12):
            ctx.move_to(-3000, DECK_Y + 110 + j * 110); ctx.line_to(6000, DECK_Y + 110 + j * 110)
        setc(ctx, hx('b2e0f8')); ctx.set_line_width(5); ctx.stroke()
        ctx.move_to(-3000, DECK_Y + 110); ctx.line_to(6000, DECK_Y + 110); ink(ctx, 5); ctx.stroke()
        ellipse(ctx, 300, 1820, 160, 30); setc(ctx, WATER); ctx.fill()
    else:
        setc(ctx, WATER); ctx.fill()
        for j in range(8):
            y = DECK_Y + 60 + j * 90
            ctx.new_path(); ctx.move_to(-100, y)
            for i in range(14):
                ctx.rel_curve_to(30, -14, 60, -14, 90, 0)
            setc(ctx, (1, 1, 1, 0.35)); ctx.set_line_width(6)
            ctx.save(); ctx.translate((lf * 2 + j * 37) % 90 - 90, 0); ctx.stroke(); ctx.restore()
    rect_r(ctx, -200, DECK_Y - 22, 1500, 40, 14); fl(ctx, WHITE, 6)


def lounger(ctx, x0=110, y=1180, w=400, back=True):
    for lx in (x0 + 30, x0 + w - 40):
        ctx.rectangle(lx, y, 14, 80); fl(ctx, hx('aab4c4'), 4)
    rect_r(ctx, x0, y - 30, w, 40, 14); fl(ctx, hx('ffffff'), 6)
    for k in range(5):
        ctx.rectangle(x0 + 20 + k * 80, y - 28, 40, 36); setc(ctx, hx('1f8bff') + (0.8,)); ctx.fill()
    if back:
        ctx.save(); ctx.translate(x0 + 30, y - 20); ctx.rotate(-1.05)
        rect_r(ctx, 0, -20, 260, 40, 14); fl(ctx, WHITE, 6)
        for k in range(3):
            ctx.rectangle(20 + k * 80, -18, 40, 36); setc(ctx, hx('1f8bff') + (0.8,)); ctx.fill()
        ctx.restore()


def umbrella(ctx, x=210, top=640, base=1200):
    ctx.rectangle(x - 8, top, 16, base - top); fl(ctx, hx('ffffff'), 4)
    for k in range(6):
        a0 = math.pi + k * math.pi / 6; a1 = a0 + math.pi / 6
        ctx.new_path(); ctx.move_to(x, top - 60)
        ctx.line_to(x + math.cos(a0) * 280, top + 40 + math.sin(a0) * -0)
        ctx.line_to(x + math.cos(a1) * 280, top + 40)
        ctx.close_path()
    ctx.new_path(); ctx.move_to(x - 280, top + 40); ctx.curve_to(x - 200, top - 80, x + 200, top - 80, x + 280, top + 40)
    ctx.close_path(); fl(ctx, RED, 6)
    for k in (-1, 1):
        ctx.new_path(); ctx.move_to(x, top - 54); ctx.curve_to(x + k * 60, top - 20, x + k * 110, top + 10, x + k * 140, top + 38)
        ctx.line_to(x + k * 60, top + 40); ctx.close_path(); setc(ctx, WHITE); ctx.fill()


def mom_lounging(ctx, lf, wet=False, eye='smug', mouth='flat', reading=True):
    lounger(ctx)
    hipy = 1140
    b = draw_hip(ctx, 330, hipy, 1.0, 1, MOM,
                 P(torso=-48, head=10, lhip=86, lkn=-2, rhip=90, rkn=-4, rsh=70, rel=-100, lsh=60, lel=-80, eye=eye, mouth=mouth))
    hd, R = b['head'], b['R']
    sunhat(ctx, hd[0], hd[1], R, 0.8 if wet else 0)
    shades(ctx, hd[0], hd[1], R)
    if reading:
        book(ctx, b['front'][0] + 10, b['front'][1] - 20, -0.3, 0.9, wet)
    if wet:
        drops(ctx, hd[0], hd[1] + R * 0.4, lf, 4, 0.6, 90, 3)
    return b


def kid_in_water(ctx, x, wl, k, p, lf, ripple=True):
    """kid drawn standing in water; the part below the waterline wl is tinted"""
    b = draw(ctx, x, wl + 0.55 * 186 * k - 186 * k, k, 1, BOY, p)
    ctx.rectangle(x - 300, wl, 600, 600); setc(ctx, WATER + (0.82,)); ctx.fill()
    if ripple:
        r = 1 + 0.1 * math.sin(lf * 0.4)
        ellipse(ctx, x, wl, 150 * k * r, 22 * k); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(8); ctx.stroke()
    return b


def splash(ctx, x, y, t, s=1.0, seed=2):
    """burst of droplets; t 0..1"""
    if not 0 <= t < 1:
        return
    rnd = random.Random(seed)
    for k in range(14):
        a = -math.pi * rnd.uniform(0.1, 0.9); v = rnd.uniform(160, 360) * s
        px = x + math.cos(a) * v * t; py = y + math.sin(a) * v * t + 500 * s * t * t
        r = rnd.uniform(12, 26) * s * (1 - 0.5 * t)
        ellipse(ctx, px, py, r, r * 1.2); fl(ctx, hx('bff0ff'), 4)


# ------------------------------------------------------------------ close-ups
def kid_ecu(ctx, f, lf, bg, eye='happy', mouth='scream', z0=1.0, shake=0, look=0.0, wet=True, rot=0.0):
    ctx.save(); cam(ctx, 540, 960, z0, 0, shake, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    for j in range(14):
        y = j * 160 - 200 + (lf * 3) % 160
        ctx.new_path(); ctx.move_to(-200, y)
        for i in range(10):
            ctx.rel_curve_to(40, -26, 80, -26, 160, 0)
        setc(ctx, (1, 1, 1, 0.18)); ctx.set_line_width(12); ctx.stroke()
    rays(ctx, 540, 880, 260, 1700, lf * 0.03, col=(1, 1, 1), a=0.25, n=18)
    cx, cy, R = 540 + look, 880, 300
    face(ctx, BOY, P(eye=eye, mouth=mouth), cx, cy, R, rot + 0.03 * math.sin(lf * 0.5))
    goggles(ctx, cx, cy, R)
    if wet:
        drops(ctx, cx, cy - 0.2 * R, lf, 5, 1.2, 330, 7)
    ctx.restore()
    return cx, cy, R


def mom_ecu(ctx, f, lf, bg, eye='smug', mouth='flat', z0=1.0, shake=0, sdy=0.0, wet=False, glass=True, ray_col=(1, 1, 1), tw=False, hat=True):
    ctx.save(); cam(ctx, 540, 960, z0, 0, shake, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    rays(ctx, 540, 880, 260, 1700, lf * 0.02, col=ray_col, a=0.3, n=18)
    cx, cy, R = 540, 900, 290
    face(ctx, MOM, P(eye=eye, mouth=mouth), cx, cy, R, 0.02 * math.sin(lf * 0.3))
    if hat:
        sunhat(ctx, cx, cy, R, 0.8 if wet else 0)
    if sdy is not None:
        shades(ctx, cx, cy, R, sdy)
    if tw:
        twitch(ctx, cx + 0.6 * R, cy - 0.5 * R, lf, 1.3)
    if glass:
        drink(ctx, cx - 300, cy + 420, 1.4, lf)
    if wet:
        drops(ctx, cx, cy - 0.3 * R, lf, 5, 1.2, 330, 5)
    ctx.restore()
    return cx, cy, R


# ------------------------------------------------------------------ shots
def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    kid_ecu(ctx, f, lf, BLUE, z0=1.0 + 0.06 * eout(pop(lf, 0, 50)), shake=4 if lf % 30 < 6 else 0)
    sparkle(ctx, 190, 700, 44 + 10 * math.sin(lf * 0.5)); sparkle(ctx, 900, 760, 36)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    label2(ctx, "\"MOM! MOM!", "WATCH THIS!!\"", WHITE, pop(lf, -4, 0) if lf == f else 1, 120, col2=YEL, y=1420)


def s2(ctx, f):
    lf = f - 54
    if lf < 76:
        # wide pool: wind-up... tiny hop
        sh = shake_at(lf, [44], 8, 6)
        ctx.save(); cam(ctx, 540 + 40 * eio(pop(lf, 0, 76)), 1080, 1.0 + 0.05 * eio(pop(lf, 0, 76)), 0, sh, f)
        pool_set(ctx, lf)
        umbrella(ctx)
        mom_lounging(ctx, lf)
        x = 740
        if lf < 34:
            wind = math.sin(lf * 0.5)
            crouch = eio(pop(lf, 14, 30))
            b = draw(ctx, x, DECK_Y - 186 * 1.5 + 30 * crouch, 1.5, 1, BOY,
                     P(eye='happy', mouth='grin', rsh=-160 + 120 * wind, rel=-10, lsh=160 - 120 * wind, lel=10, lhip=10 - 40 * crouch,
                       lkn=60 * crouch, rhip=-10 - 40 * crouch, rkn=60 * crouch, torso=10 * crouch))
            goggles(ctx, b['head'][0], b['head'][1], b['R'], True)
        elif lf < 44:
            t = pop(lf, 34, 44)
            hop = 30 * math.sin(math.pi * t)
            b = draw(ctx, x + 30 * t, DECK_Y - 186 * 1.5 - hop + 160 * t * t, 1.5, 1, BOY,
                     P(eye='closed', mouth='open', rsh=-170, lsh=170, lhip=20, lkn=20, rhip=-20, rkn=20))
            goggles(ctx, b['head'][0], b['head'][1], b['R'], True)
        else:
            il = lf - 44
            b = kid_in_water(ctx, x + 30, 1500, 1.5, P(eye='happy', mouth='scream' if il > 10 else 'grin', rsh=-160, rel=-20, lsh=160, lel=20), il)
            goggles(ctx, b['head'][0], b['head'][1], b['R'], True)
            splash(ctx, x + 30, 1500, pop(il, 0, 14), 0.5)
        ctx.restore()
        if lf < 34:
            label(ctx, "\"WATCH THIS!\"", 560, 420, 120, YEL, -0.05, pop(lf, 0, 4))
            if lf >= 14:
                label(ctx, "*wind... up...*", 540, 1450, 90, WHITE, 0.04, pop(lf, 14, 18))
        elif lf < 56:
            label(ctx, "*plip.*", 760, 600, 90, WHITE, 0.05, pop(lf, 44, 47))
        else:
            label2(ctx, "\"DID YOU", "SEE THAT?!\"", WHITE, pop(lf, 56, 60), 110, col2=YEL, y=600)
    else:
        il = lf - 76
        cx, cy, R = mom_ecu(ctx, f, il, TEAL, 'smug', 'smile', z0=1.0 + 0.06 * eout(pop(il, 0, 50)))
        # thumbs up
        tx, ty = cx + 330, cy + 400
        ellipse(ctx, tx, ty, 80, 70); fl(ctx, MOM['skin'], 7)
        rect_r(ctx, tx - 22, ty - 170, 44, 120, 22); fl(ctx, MOM['skin'], 7)
        label2(ctx, "\"Wow.", "AMAZING.\"", WHITE, pop(il, 4, 8), 120, col2=GOLD, y=1440)


def s3(ctx, f):
    lf = f - 180
    if lf < 82:
        # underwater cross-section
        WL = 800
        ctx.save(); cam(ctx, 540, 1000 - 40 * eio(pop(lf, 0, 60)), 1.0 + 0.06 * eio(pop(lf, 0, 60)), 0, shake_at(lf, [62], 12, 18), f)
        sky(ctx, 520)
        ctx.rectangle(-3000, 480, 9000, 60); setc(ctx, hx('3fae54')); ctx.fill()
        ctx.rectangle(-3000, 540, 9000, 260); setc(ctx, hx('f4e2c0')); ctx.fill()
        # mom tiny on the deck
        ctx.save(); ctx.translate(470, -520); ctx.scale(1.0, 1.0)
        mom_lounging(ctx, lf, reading=True)
        ctx.restore()
        # water
        g = cairo.LinearGradient(0, WL, 0, 1900); g.add_color_stop_rgb(0, *WATER); g.add_color_stop_rgb(1, *DEEP)
        ctx.rectangle(-3000, WL, 9000, 3000); ctx.set_source(g); ctx.fill()
        for i in range(-10, 20):
            ctx.move_to(i * 140, 1500); ctx.line_to(i * 140, 3000)
        ctx.move_to(-3000, 1500); ctx.line_to(6000, 1500); setc(ctx, (1, 1, 1, 0.2)); ctx.set_line_width(5); ctx.stroke()
        for k in range(6):
            x = (k * 210 + lf * 3) % 1300 - 100
            poly(ctx, [(x, WL), (x + 60, WL), (x - 120, 1500), (x - 200, 1500)]); setc(ctx, (1, 1, 1, 0.12)); ctx.fill()
        ctx.new_path(); ctx.move_to(-200, WL)
        for i in range(20):
            ctx.rel_curve_to(30, -12, 60, -12, 90, 0)
        ink(ctx, 6); ctx.stroke()
        if lf < 62:
            puffc = eio(pop(lf, 4, 58))
            bob = 12 * math.sin(lf * 0.2)
            b = draw(ctx, 540, 1200 + bob, 1.7, 1, BOY,
                     P(eye='closed', mouth='flat', rsh=-120, rel=40, lsh=120, lel=-40, lhip=-40, lkn=80, rhip=30, rkn=50, torso=-6,
                       head=4 * math.sin(lf * 0.6) * puffc))
            hd, R = b['head'], b['R']
            goggles(ctx, hd[0], hd[1], R, True)
            for sx in (-0.48, 0.7):
                ellipse(ctx, hd[0] + R * sx, hd[1] + R * 0.38, R * (0.18 + 0.2 * puffc), R * (0.15 + 0.18 * puffc))
                fl(ctx, hx('ff8aa0'), 5)
            # cheeks turn red then purple
            for k in range(4):
                ph = ((lf * 3 + k * 25) % 100) / 100
                ctx.new_path(); ctx.arc(hd[0] + 40 + 20 * math.sin(ph * 9 + k), hd[1] + 0.3 * R - ph * 340, 12 + 8 * k % 3 * 4, 0, 2 * math.pi)
                setc(ctx, (1, 1, 1, 0.9 * (1 - ph))); ctx.set_line_width(5); ctx.stroke()
        else:
            il = lf - 62
            up = eout(pop(il, 0, 8))
            b = draw(ctx, 540, 1200 - 480 * up, 1.7, 1, BOY, P(eye='happy', mouth='scream', rsh=-170, rel=-10, lsh=170, lel=10))
            goggles(ctx, b['head'][0], b['head'][1], b['R'], True)
            splash(ctx, 540, WL, pop(il, 0, 18), 1.4, 5)
        ctx.restore()
        card(ctx, 'p2', f, 180, 240)
        if lf < 62:
            for k, (t0, s_, c) in enumerate(((10, "1...", WHITE), (28, "2...", YEL), (46, "3!!", RED))):
                if lf >= t0:
                    label(ctx, s_, (230, 850, 540)[k], (1300, 1300, 1450)[k], 130, c, (-0.1, 0.1, 0)[k], pop(lf, t0, t0 + 4))
            label(ctx, "*blub blub*", 820, 1000, 70, WHITE, 0.05, pop(lf, 4, 8))
        else:
            label2(ctx, "\"NEW RECORD!!", "3 SECONDS!!\"", WHITE, pop(lf, 64, 68), 110, col2=YEL, y=1420)
    else:
        il = lf - 82
        if il < 36:
            # asleep behind the shades
            sdy = 0.38 * eio(pop(il, 2, 16))
            mom_ecu(ctx, f, il, PURPLE, 'closed', 'open', z0=1.04 + 0.05 * eout(pop(il, 0, 36)), sdy=sdy, ray_col=(1, 0.9, 1))
            zzz(ctx, 820, 640, il, 1.4)
            card(ctx, 'p3', f, 262, 296)
            label2(ctx, "\"wow... so...", "amazing...\"", WHITE, pop(il, 14, 18), 100, col2=hx('c8e6ff'), y=1440)
        else:
            jl = il - 36
            mom_ecu(ctx, f, jl, RED, 'shock', 'scream', z0=1.1, shake=shake_at(jl, [0], 10, 22), sdy=-0.9 * eout(pop(jl, 0, 4)), ray_col=(1, 0.85, 0.6))
            label2(ctx, "\"I'M", "WATCHING!!\"", WHITE, pop(jl, 1, 5), 130, col2=YEL, y=1440)


def s4(ctx, f):
    lf = f - 320
    if lf < 46:
        # low angle: Dad on the diving board
        bounce = 14 * math.sin(lf * 0.9) * (1 - pop(lf, 0, 30))
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.08 * eio(pop(lf, 0, 46)), -6, shake_at(lf, [26], 10, 10), f)
        g = cairo.LinearGradient(0, -400, 0, 2000); g.add_color_stop_rgb(0, *hx('5ab8ff')); g.add_color_stop_rgb(1, *hx('c8eeff'))
        ctx.rectangle(-1000, -1000, 3200, 4000); ctx.set_source(g); ctx.fill()
        rays(ctx, 640, 620, 200, 1800, lf * 0.02, col=(1, 0.97, 0.7), a=0.45, n=16)
        ctx.new_path(); ctx.arc(640, 620, 170, 0, 2 * math.pi); fl(ctx, YEL, 7)
        # ladder tower
        for lx in (120, 260):
            ctx.rectangle(lx, 1000, 22, 1200); fl(ctx, hx('c0c8d8'), 6)
        for k in range(8):
            ctx.rectangle(120, 1080 + k * 110, 160, 18); fl(ctx, hx('c0c8d8'), 5)
        # board (seen from below)
        ctx.save(); ctx.translate(100, 1000); ctx.rotate(-0.02 + bounce * 0.002)
        poly(ctx, [(0, 0), (780, -20 + bounce), (790, 40 + bounce), (0, 60)]); fl(ctx, hx('2ac0ff'), 8)
        ctx.restore()
        b = draw(ctx, 700, 980 + bounce - 186 * 1.9, 1.9, 1, DAD,
                 P(eye='smug', mouth='grin', rsh=-140, rel=-80, lsh=-140, lel=80, head=-6))
        trunks(ctx, 700, 980 + bounce - 186 * 1.9 + 186 * 1.9 - 68 * 1.35 * 1.9, 1.9, RED)
        goggles(ctx, b['head'][0], b['head'][1], b['R'], False)
        ctx.restore()
        label(ctx, "\"Hey, family...\"", 540, 1330, 100, WHITE, -0.04, pop(lf, 2, 6))
        if lf >= 24:
            label(ctx, "\"WATCH THIS.\"", 540, 1470, 140, YEL, 0.03, pop(lf, 24, 28))
    elif lf < 78:
        il = lf - 46
        # flying cannonball
        ctx.save(); cam(ctx, 540, 960, 1.0, 0, 6, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('5ab8ff')); ctx.fill()
        for k in range(5):
            y = (k * 420 - il * 60) % 2400 - 300
            ellipse(ctx, 200 + (k * 330) % 800, y, 140, 50); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()
        for k in range(9):
            y = 300 + k * 150
            ctx.move_to(100 + (k * 97) % 300, y); ctx.line_to(980 - (k * 61) % 300, y - 260)
        setc(ctx, (1, 1, 1, 0.5)); ctx.set_line_width(14); ctx.stroke()
        t = il / 32
        x = 200 + 680 * t; y = 520 + 760 * t
        ctx.save(); ctx.translate(x, y); ctx.rotate(il * 0.35)
        b = draw_hip(ctx, 0, 0, 1.6, 1, DAD,
                     P(eye='closed', mouth='scream', lhip=-130, lkn=150, rhip=-120, rkn=150, lsh=-110, lel=-60, rsh=-100, rel=-70, torso=24, head=10))
        ctx.restore()
        ctx.restore()
        label(ctx, "CANNONBAAALL!!", 540, 1420, 120, YEL, -0.06, pop(il, 0, 4))
    elif lf < 102:
        il = lf - 78
        # KER-SPLOOSH
        ctx.save(); cam(ctx, 540, 1080, 1.0 + 0.1 * eout(pop(il, 0, 20)), 0, shake_at(il, [0], 20, 40), f)
        pool_set(ctx, il)
        umbrella(ctx)
        mom_lounging(ctx, il, eye='shock', mouth='scream', reading=False)
        h = eout(pop(il, 0, 14))
        rnd = random.Random(11)
        for k in range(22):
            ax = 700 + rnd.uniform(-260, 260) * (0.4 + h)
            ay = DECK_Y + 100 - h * rnd.uniform(500, 1500)
            r = rnd.uniform(90, 200) * (0.3 + h)
            ellipse(ctx, ax, ay, r, r * 1.1); fl(ctx, hx('bff0ff') if k % 2 else WATER, 7)
        ctx.restore()
        cover = pop(il, 12, 20)
        if cover > 0:
            ctx.rectangle(0, H * (1 - cover), W, H * cover + 10); setc(ctx, WATER); ctx.fill()
            for k in range(6):
                ellipse(ctx, k * 220, H * (1 - cover), 140, 60); setc(ctx, WATER); ctx.fill()
        label(ctx, "*KER-SPLOOSH!!*", 540, 1350, 130, WHITE, -0.06, pop(il, 0, 4))
    else:
        il = lf - 102
        ctx.save(); cam(ctx, 540, 1100, 1.0, 0, 0, f)
        pool_set(ctx, il, empty=True, wet=True)
        umbrella(ctx)
        # float hanging off the umbrella
        ellipse(ctx, 350, 700, 70, 40); fl(ctx, PINK, 6); ellipse(ctx, 350, 700, 30, 16); setc(ctx, hx('8fd8ff')); ctx.fill()
        mom_lounging(ctx, il, wet=True, eye='normal', mouth='flat', reading=True)
        b = draw(ctx, 560, DECK_Y - 30 - 186 * 1.3, 1.3, 1, BOY, P(eye='normal', mouth='flat', rsh=-6, lsh=6))
        goggles(ctx, b['head'][0], b['head'][1], b['R'], False)
        drops(ctx, b['head'][0], b['head'][1], il, 3, 0.6, 70, 9)
        # Dad at the bottom of the empty pool
        bd = draw_hip(ctx, 760, 1700, 1.3, -1, DAD, P(eye='happy', mouth='grin', lhip=86, lkn=-4, rhip=88, rkn=-4, rsh=-160, rel=-10, lsh=-150, lel=10, torso=-4))
        goggles(ctx, bd['head'][0], bd['head'][1], bd['R'], False)
        ctx.restore()
        if il < 24:
            label2(ctx, "\"...did you", "SEE that?!\"", WHITE, pop(il, 2, 6), 110, col2=YEL, y=520)
        else:
            label2(ctx, "\"...we", "SAW.\"", WHITE, pop(il, 24, 28), 130, col2=hx('8fe0ff'), y=520)


def s5(ctx, f):
    lf = f - 470
    if lf < 62:
        kid_ecu(ctx, f, lf, PINK, 'happy', 'scream', z0=1.0 + 0.08 * eout(pop(lf, 0, 40)), look=-30 * eio(pop(lf, 0, 8)), shake=4 if lf % 24 < 5 else 0)
        sparkle(ctx, 190, 700, 44 + 10 * math.sin(lf * 0.5)); sparkle(ctx, 900, 760, 36)
        label2(ctx, "\"DAD! DAD!", "WATCH THIS!!\"", WHITE, pop(lf, 2, 6), 120, col2=YEL, y=1420)
    elif lf < 122:
        il = lf - 62
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eout(pop(il, 0, 60)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('cdeeff')); ctx.fill()
        for i in range(-2, 12):
            ctx.move_to(i * 160, -500); ctx.line_to(i * 160, 2500)
        for j in range(-2, 16):
            ctx.move_to(-500, j * 160); ctx.line_to(1700, j * 160)
        setc(ctx, hx('b2e0f8')); ctx.set_line_width(8); ctx.stroke()
        cx, cy, R = 540, 900, 300
        face(ctx, DAD, P(eye='smug', mouth='flat'), cx, cy, R, 0.0)
        sunhat(ctx, cx, cy, R, 0.4)
        shades(ctx, cx, cy, R, 0.3)
        twitch(ctx, cx + 0.7 * R, cy - 0.45 * R, il, 1.3)
        drops(ctx, cx, cy - 0.3 * R, il, 4, 1.1, 300, 4)
        ctx.restore()
        label2(ctx, "\"...wow.", "AMAZING.\"", WHITE, pop(il, 6, 10), 130, col2=GOLD, y=1440)
    elif lf < 158:
        il = lf - 122
        mom_ecu(ctx, f, il, GOLD, 'happy', 'grin', z0=1.0 + 0.06 * eout(pop(il, 0, 36)), sdy=-0.75, ray_col=(1, 1, 0.8))
        sparkle(ctx, 200, 640, 40); sparkle(ctx, 880, 700, 30)
        label2(ctx, "\"Welcome to", "MY life.\"", WHITE, pop(il, 3, 7), 120, col2=PINK, y=1440)
    else:
        s1(ctx, f, f - 628 + 40)


SHOTS = [(0, s1), (54, s2), (180, s3), (320, s4), (470, s5)]
CUTS = (54, 130, 180, 242, 262, 298, 320, 366, 398, 422, 470, 532, 592, 628)


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
                              "-i", "out/watch_this_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
