"""'The Broccoli Smuggler' - original, general-audience comedy short, ~35s.
Mom: no cake until you eat your broccoli. The kid smuggles every floret away (napkin, plant, Dad's plate,
spoon catapult)... but Dad, hidden behind his newspaper, ate them all and wins the cake."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import cam, pop, sparkle, puff, label, shake_at
from scenes8 import walk, sit
from scenes13 import card as _card13
import scenes13

BOY, MOM = doodle.BOY, doodle.MOM_G
DAD = dict(doodle.DAD, shades=True)
N = 1050
KB, KD, KM = 1.25, 1.45, 1.5
BX, BHIP = 380, 1250          # boy seat
DX, DHIP = 800, 1270          # dad seat
TB, TF, CL = 1215, 1285, 1600  # table back edge, front edge, cloth bottom
KP = (420, 1250)              # kid plate
DP = (790, 1250)              # dad plate
POT = (140, 1240)             # potted plant on the table
NAP = (600, 1262)             # napkin

CAPS = {
    'p1': [[("WHEN MOM SAYS:", OUT)], [("NO ", OUT), ("CAKE", hx('e07b12')), (" UNTIL YOU", OUT)], [("EAT YOUR ", OUT), ("BROCCOLI", hx('2a9d3a'))]],
    'p2': [[("TIME FOR", OUT)], [("OPERATION ", OUT), ("NO GREENS", hx('2a9d3a'))]],
    'p3': [[("MY ", OUT), ("SNEAKY", hx('8a3cff')), (" METHODS", OUT)]],
    'p4': [[("THE ", OUT), ("SPOON", hx('1f8bff')), (" CATAPULT", OUT)]],
    'p5': [[("THEN MOM CAME BACK", OUT)], [("WITH ", OUT), ("ONE", hx('ff3b5c')), (" SLICE", OUT)]],
    'p6': [[("BUT ", OUT), ("DAD", hx('1f8bff')), (" WAS", OUT)], [("PAYING ATTENTION", OUT)]],
    'p7': [[("DAD WINS.", OUT)], [("SAME TIME ", OUT), ("TOMORROW?", hx('e07b12'))]],
}
scenes13.CAPS = CAPS
card = _card13
_tmp = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4))

GONE = [236, 256, 296, 316, 370, 432, 472, 512]      # frames each kid floret leaves the plate


def kid_left(f):
    return 8 - sum(1 for e in GONE if e <= f)


# ------------------------------------------------------------------ props
def rect_r(ctx, x, y, w, h, r):
    ctx.new_path(); ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); ctx.close_path()


def broc(ctx, x, y, s=1.0, a=0.0, face=None):
    """one cartoon broccoli floret, (x,y) = stem bottom"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-11, 0), (11, 0), (9, -34), (-9, -34)]); fl(ctx, hx('b6e67a'), 4)
    for cx_, cy_, r in ((-20, -40, 17), (20, -40, 17), (0, -56, 21), (-11, -32, 14), (12, -32, 14)):
        ellipse(ctx, cx_, cy_, r, r); fl(ctx, hx('2f9e44'), 4)
    for cx_, cy_ in ((-22, -44), (0, -62), (18, -46), (5, -40)):
        ellipse(ctx, cx_, cy_, 4, 4); setc(ctx, hx('6fd06a')); ctx.fill()
    if face:
        # tiny worried face for the hero floret
        for ex in (-8, 8):
            ellipse(ctx, ex, -44, 4, 5); setc(ctx, INK); ctx.fill()
        ink(ctx, 3); ctx.new_path(); ctx.arc(0, -32, 6, math.pi + 0.5, 2 * math.pi - 0.5); ctx.stroke()
    ctx.restore()


def plate(ctx, x, y, n, s=1.0, seed=1, crumbs=False):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 6, 128, 40); setc(ctx, (0, 0, 0, 0.15)); ctx.fill()
    ellipse(ctx, 0, 0, 128, 38); fl(ctx, (1, 1, 1), 5)
    ellipse(ctx, 0, 0, 88, 24); setc(ctx, hx('e6e9f2')); ctx.fill()
    spots = [(-50, 4), (-18, 8), (16, 6), (48, 4), (-34, -6), (0, -8), (32, -6), (-2, 12)]
    for i in range(min(n, len(spots))):
        bx, by = spots[i]
        broc(ctx, bx, by + 6, 0.62, (i * 0.37 % 0.6) - 0.3)
    if crumbs and n == 0:
        for i in range(6):
            ellipse(ctx, -40 + i * 16, (i * 7) % 10 - 4, 3, 3); setc(ctx, hx('6fd06a')); ctx.fill()
    ctx.restore()


def fork(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -6, 0, 12, 90, 5); fl(ctx, hx('d8dbe8'), 3)
    for tx in (-12, -4, 4, 12):
        ctx.rectangle(tx - 2, -34, 4, 34); setc(ctx, hx('d8dbe8')); ctx.fill_preserve(); ink(ctx, 2); ctx.stroke()
    rect_r(ctx, -15, -6, 30, 10, 4); fl(ctx, hx('d8dbe8'), 3)
    ctx.restore()


def spoon(ctx, x, y, a, s=1.0, load=False):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -6, 0, 12, 100, 5); fl(ctx, hx('d8dbe8'), 3)
    ellipse(ctx, 0, -26, 24, 32); fl(ctx, hx('d8dbe8'), 4)
    ellipse(ctx, -6, -32, 7, 12); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()
    if load:
        broc(ctx, 0, -10, 0.6)
    ctx.restore()


def napkin(ctx, x, y, stuffed, wob=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(wob)
    if stuffed == 0:
        poly(ctx, [(-60, 8), (60, 8), (40, -20), (-40, -20)]); fl(ctx, hx('ff8aa8'), 4)
    else:
        r = 46 + stuffed * 12
        for k in range(stuffed):
            broc(ctx, -20 + k * 34, -r * 1.25, 0.55, -0.4 + k * 0.6)
        ctx.new_path(); ctx.move_to(-r, 8); ctx.curve_to(-r * 1.2, -r * 0.6, -r * 0.4, -r * 1.3, 0, -r * 1.1)
        ctx.curve_to(r * 0.4, -r * 1.3, r * 1.2, -r * 0.6, r, 8); ctx.close_path(); fl(ctx, hx('ff8aa8'), 5)
        ink(ctx, 3); ctx.new_path(); ctx.move_to(-r * 0.4, -r * 0.2); ctx.curve_to(-r * 0.2, -r * 0.6, r * 0.2, -r * 0.6, r * 0.35, -r * 0.3); ctx.stroke()
    ctx.restore()


def plant(ctx, x, y, n, wob=0.0, burp=0.0):
    """potted plant on the table, n florets stuffed into the soil"""
    ctx.save(); ctx.translate(x, y)
    ctx.save(); ctx.rotate(wob)
    for a, l in ((-0.7, 150), (-0.3, 190), (0.1, 210), (0.5, 170), (0.85, 130)):
        ctx.save(); ctx.translate(0, -90); ctx.rotate(a + 0.15 * burp * math.sin(a * 9))
        ellipse(ctx, 0, -l * 0.5, 26, l * 0.5); fl(ctx, hx('3ccf6a'), 4)
        ctx.new_path(); ctx.move_to(0, -6); ctx.line_to(0, -l * 0.9); setc(ctx, hx('2a9d3a')); ctx.set_line_width(4); ctx.stroke()
        ctx.restore()
    for k in range(n):
        broc(ctx, -26 + k * 50, -86, 0.5, -0.3 + k * 0.6)
    ctx.restore()
    poly(ctx, [(-70, -100), (70, -100), (52, 0), (-52, 0)]); fl(ctx, hx('ff8a3d'), 5)
    rect_r(ctx, -80, -116, 160, 26, 8); fl(ctx, hx('ff6a2a'), 5)
    ctx.restore()


def newspaper(ctx, x, y, s=1.0, lower=0.0, crinkle=0.0):
    """held up in front of Dad; lower 0..1 slides it down"""
    ctx.save(); ctx.translate(x, y + lower * 260); ctx.scale(s, s); ctx.rotate(crinkle)
    w, h = 210, 300
    poly(ctx, [(-w, -h), (0, -h + 14), (w, -h), (w, h * 0.55), (0, h * 0.55 + 14), (-w, h * 0.55)]); fl(ctx, hx('f4f1e6'), 6)
    ctx.move_to(0, -h + 14); ctx.line_to(0, h * 0.55 + 14); ink(ctx, 3); ctx.stroke()
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(40)
    for side in (-1, 1):
        cx0 = side * w * 0.5
        ctx.move_to(cx0 - 86, -h + 70); ctx.text_path("DAILY" if side < 0 else "NEWS"); setc(ctx, INK); ctx.fill()
        ctx.rectangle(cx0 - 86, -h + 96, 172, 8); setc(ctx, INK); ctx.fill()
        if side < 0:
            ctx.rectangle(cx0 - 86, -h + 120, 172, 96); fl(ctx, hx('a9c4e8'), 3)
            ellipse(ctx, cx0 - 30, -h + 170, 20, 20); setc(ctx, hx('ffd23f')); ctx.fill()
            yy = -h + 236
        else:
            yy = -h + 124
        while yy < h * 0.5 - 10:
            ctx.rectangle(cx0 - 86, yy, 172 if (yy // 22) % 4 else 110, 7); setc(ctx, hx('9a978e')); ctx.fill()
            yy += 22
    # Dad's fingers on top edge
    for side in (-1, 1):
        for k in range(3):
            ellipse(ctx, side * (w - 30 - k * 22), -h + 8, 13, 17); fl(ctx, DAD['skin'], 3)
    ctx.restore()


def cake(ctx, x, y, s=1.0, bite=0.0, glow=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if glow > 0:
        g = cairo.RadialGradient(0, -60, 10, 0, -60, 240)
        g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.7 * glow); g.add_color_stop_rgba(1, 1, 0.95, 0.5, 0)
        ctx.set_source(g); ctx.arc(0, -60, 240, 0, 2 * math.pi); ctx.fill()
    ellipse(ctx, 0, 4, 120, 30); fl(ctx, (1, 1, 1), 5)
    # wedge: front face + top
    poly(ctx, [(-90, -10), (70, -10), (70, -110), (-90, -110)]); fl(ctx, hx('7a3e1e'), 5)
    for yy, c in ((-46, hx('ff9ac2')), (-80, hx('ff9ac2'))):
        ctx.rectangle(-88, yy - 7, 156, 14); setc(ctx, c); ctx.fill()
    poly(ctx, [(-90, -110), (70, -110), (100, -140), (-20, -150)]); fl(ctx, hx('ffb0d0'), 5)
    poly(ctx, [(70, -10), (100, -40), (100, -140), (70, -110)]); fl(ctx, hx('5e2e14'), 5)
    for k in range(4):
        ellipse(ctx, -70 + k * 42, -110, 16, 12); fl(ctx, hx('ffb0d0'), 3)
    if bite < 1:
        ellipse(ctx, 20, -160, 20, 20); fl(ctx, hx('ff2a3d'), 4)
        ctx.new_path(); ctx.move_to(20, -178); ctx.curve_to(26, -200, 36, -206, 44, -208); ink(ctx, 4); ctx.stroke()
    if bite > 0:
        ellipse(ctx, -90, -70, 50 * bite, 60 * bite); setc(ctx, hx('fff6e8')); ctx.fill()
    ctx.restore()


def big_bowl(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for i in range(11):
        bx = -110 + (i % 6) * 44 + (22 if i >= 6 else 0); by = -40 - (30 if i >= 6 else 0)
        broc(ctx, bx, by + 20, 0.8, (i * 0.31 % 0.6) - 0.3)
    ctx.new_path(); ctx.move_to(-150, -40); ctx.curve_to(-140, 60, 140, 60, 150, -40); ctx.close_path(); fl(ctx, hx('1f8bff'), 6)
    ctx.new_path(); ctx.move_to(-100, -10); ctx.curve_to(-60, 10, 60, 10, 100, -10); setc(ctx, (1, 1, 1, 0.5)); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()


# ------------------------------------------------------------------ set
def dining(ctx, f, wall=hx('ffd98a'), night=True):
    ctx.rectangle(-1200, -1500, 3600, 4200); setc(ctx, wall); ctx.fill()
    for i in range(-14, 30):
        for j in range(-10, 20):
            if (i + j) % 2 == 0:
                ellipse(ctx, i * 90 + 45, j * 90 + 45, 9, 9); setc(ctx, light(wall, 0.4)); ctx.fill()
    # window (evening)
    ctx.rectangle(640, 470, 300, 330); fl(ctx, hx('3a4a9e') if night else hx('8fe0ff'), 8)
    ellipse(ctx, 860, 550, 34, 34); setc(ctx, hx('fff6c2')); ctx.fill()
    ellipse(ctx, 875, 540, 30, 30); setc(ctx, hx('3a4a9e')); ctx.fill()
    for sx, sy in ((700, 520), (760, 600), (690, 700), (820, 680)):
        sparkle(ctx, sx, sy, 10, (1, 1, 1))
    ctx.move_to(790, 470); ctx.line_to(790, 800); ctx.move_to(640, 635); ctx.line_to(940, 635); ink(ctx, 6); ctx.stroke()
    # picture frame
    ctx.rectangle(150, 560, 240, 180); fl(ctx, hx('fff6e0'), 7)
    poly(ctx, [(165, 725), (230, 640), (290, 690), (330, 650), (375, 725)]); fl(ctx, hx('2fbf5a'), 4)
    # hanging lamp
    ctx.move_to(540, -400); ctx.line_to(540, 380); ink(ctx, 5); ctx.stroke()
    ctx.new_path(); ctx.move_to(440, 470); ctx.curve_to(450, 380, 630, 380, 640, 470); ctx.close_path(); fl(ctx, hx('ff3b5c'), 6)
    g = cairo.LinearGradient(0, 470, 0, 1250)
    g.add_color_stop_rgba(0, 1, 0.96, 0.7, 0.35); g.add_color_stop_rgba(1, 1, 0.96, 0.7, 0)
    poly(ctx, [(440, 470), (640, 470), (1000, 1250), (80, 1250)]); ctx.set_source(g); ctx.fill()
    # floor
    ctx.rectangle(-1200, 1480, 3600, 1400); setc(ctx, hx('b77a4b')); ctx.fill()
    for i in range(-10, 30):
        ctx.move_to(i * 140, 1480); ctx.line_to(i * 140 - 60, 2800); setc(ctx, dark(hx('b77a4b'), 0.85)); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-1200, 1480); ctx.line_to(2400, 1480); ink(ctx, 8); ctx.stroke()


def chair_back(ctx, x, top, col=hx('c98b55')):
    rect_r(ctx, x - 120, top, 240, 320, 30); fl(ctx, col, 7)
    rect_r(ctx, x - 80, top + 40, 160, 220, 20); fl(ctx, light(col, 0.25), 4)


def table(ctx):
    # top surface
    poly(ctx, [(30, TB), (1050, TB), (1090, TF), (-10, TF)]); fl(ctx, hx('fff6e8'), 7)
    # checked cloth front
    ctx.save()
    ctx.new_path(); ctx.move_to(-10, TF)
    ctx.line_to(1090, TF); ctx.line_to(1090, CL - 30)
    for i in range(12):
        x0 = 1090 - i * 91.7
        ctx.curve_to(x0 - 20, CL + 10, x0 - 70, CL + 10, x0 - 91.7, CL - 30)
    ctx.close_path()
    clip = ctx.copy_path()
    setc(ctx, (1, 1, 1)); ctx.fill_preserve(); ctx.clip()
    for i in range(-1, 14):
        ctx.rectangle(i * 90, TF, 45, 400); setc(ctx, (1, 0.3, 0.35, 0.55)); ctx.fill()
    for j in range(0, 6):
        ctx.rectangle(-20, TF + j * 90, 1120, 45); setc(ctx, (1, 0.3, 0.35, 0.55)); ctx.fill()
    ctx.restore()
    ctx.new_path(); ctx.append_path(clip); ink(ctx, 7); ctx.stroke()
    ctx.move_to(-10, TF); ctx.line_to(1090, TF); ink(ctx, 7); ctx.stroke()


def boy_pose(kind, **kw):
    base = dict(
        eat=dict(lsh=40, lel=-90, rsh=60, rel=-70),
        reach=dict(lsh=30, lel=-100, rsh=95, rel=-10, torso=10),
        cheer=dict(lsh=-160, lel=-20, rsh=165, rel=-20, torso=-4),
        point=dict(lsh=30, lel=-100, rsh=150, rel=-20),
        slump=dict(lsh=20, lel=-40, rsh=20, rel=-40, torso=12, head=10),
        shades=dict(lsh=30, lel=-100, rsh=160, rel=-150, head=-4),
    )[kind]
    base.update(kw)
    return sit(**base)


def scene(ctx, f, boy=None, dad=None, kid_n=None, dad_n=4, nap=0, pot_n=0, paper=0.0, paper_on=True, dad_paper_y=0,
          mom=None, extra=None, dad_face=-1, boy_face=1, plant_burp=0.0, nap_wob=0.0, boy_after=None, mom_back=False):
    dining(ctx, f)
    chair_back(ctx, BX, 900)
    chair_back(ctx, DX, 880, hx('b8743e'))
    mh = None
    if mom and mom_back:
        mh = mom(ctx)
    bh = draw_hip(ctx, BX, BHIP, KB, boy_face, BOY, boy or boy_pose('eat'))
    dh = draw_hip(ctx, DX, DHIP, KD, dad_face, DAD, dad or sit(lsh=60, lel=-120, rsh=60, rel=-120, eye='normal', mouth='smile'))
    if paper_on:
        newspaper(ctx, DX - 20, 1010 + dad_paper_y, 0.95, paper)
    if mom and not mom_back:
        mh = mom(ctx)
    table(ctx)
    plant(ctx, POT[0], POT[1] + 20, pot_n, burp=plant_burp, wob=0.05 * plant_burp)
    plate(ctx, *KP, kid_left(f) if kid_n is None else kid_n, crumbs=True)
    plate(ctx, *DP, dad_n)
    napkin(ctx, *NAP, nap, nap_wob)
    if boy_after:
        boy_after(ctx, bh)
    if extra:
        extra(ctx, bh, dh, mh)
    return bh, dh, mh


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    # ECU on a broccoli floret with a worried face, pull back to the kid's disgusted face
    pull = eout(pop(f, 30, 60))
    z = lerp(3.0, 1.25, pull)
    cx = lerp(KP[0], 470, pull); cy = lerp(KP[1] - 40, 1080, pull)
    ctx.save(); cam(ctx, cx, cy, z, lerp(-4, 0, pull), shake_at(f, [62], 10, 18), f)
    gross = f >= 56
    scene(ctx, f, boy=boy_pose('eat', eye='shock' if gross else 'normal', mouth='wavy' if gross else 'flat', torso=-10 if gross else 0, head=-8 if gross else 0))
    # the hero floret staring up
    broc(ctx, KP[0] + 4, KP[1] + 8, 0.9, 0.1 * math.sin(f * 0.3), face=True)
    ctx.restore()
    if f < 30:
        label(ctx, "BROCCOLI.", 540, 1440, 120, hx('5fd07a'), -0.03, pop(f, 4, 8))
    elif f >= 62:
        label(ctx, "EWWW!!", 540, 1440, 140, hx('ffe14d'), 0.05, pop(f, 62, 66))
    card(ctx, 'p1', f, 2, 98)


def s2(ctx, f):
    lf = f - 100
    # low-angle slow push-in: shades slide down, "the plan"
    on = eout(pop(lf, 30, 46))
    pose = boy_pose('shades' if 20 <= lf < 50 else 'eat', eye='smug', mouth='grin' if lf >= 50 else 'flat', shades=1 if lf >= 30 else 0,
                    shades_dy=lerp(-1.4, 0, on))
    z = kf(lf, [(0, 1.5), (120, 1.9)], eout)
    ctx.save(); cam(ctx, kf(lf, [(0, 420), (120, 400)], eout), kf(lf, [(0, 1080), (120, 1000)], eout), z, -5, shake_at(lf, [46], 8, 12), f)
    scene(ctx, f, boy=pose)
    ctx.restore()
    if lf >= 46:
        for i in range(5):
            a = lf * 0.07 + i * 1.256
            sparkle(ctx, 540 + math.cos(a) * 380, 900 + math.sin(a) * 300, 24 * pop(lf, 46, 54), hx('fff27a'))
    if 30 <= lf < 70:
        label(ctx, "*SHADES ON*", 540, 1440, 100, (1, 1, 1), 0.03, pop(lf, 30, 34))
    elif lf >= 70:
        label(ctx, "NOBODY WILL KNOW.", 540, 1440, 86, hx('ffe14d'), -0.02, pop(lf, 70, 74))
    card(ctx, 'p2', f, 102, 216)


def flying(ctx, x0, y0, x1, y1, t, hgt=180, s=0.6):
    t = clamp(t)
    x = lerp(x0, x1, t); y = lerp(y0, y1, t) - math.sin(math.pi * t) * hgt
    broc(ctx, x, y, s, t * 6)


def s3(ctx, f):
    lf = f - 220
    step = 0 if lf < 60 else (1 if lf < 118 else 2)
    sl = lf - (0, 60, 118)[step]
    nap = (1 if f >= GONE[0] else 0) + (1 if f >= GONE[1] else 0)
    pot = (1 if f >= GONE[2] else 0) + (1 if f >= GONE[3] else 0)
    dadn = 4 + (1 if f >= GONE[4] else 0)
    burp = 0.0
    if step == 0:
        pose = boy_pose('reach', eye='smug', mouth='grin', shades=1, rsh=80 + 20 * math.sin(sl * 0.5), rel=-30)
        cx, cy, z, rot = 520, 1150, 1.7, 3
    elif step == 1:
        pose = sit(eye='smug', mouth='grin', shades=1, lsh=110 + 15 * math.sin(sl * 0.5), lel=-20, rsh=40, rel=-90, torso=-14)
        cx, cy, z, rot = 300, 1130, 1.65, -3
        if 76 <= f - 220 + 0 and f >= GONE[3] + 4:
            burp = 1 - pop(f, GONE[3] + 4, GONE[3] + 30)
    else:
        pose = boy_pose('reach', eye='smug', mouth='grin', shades=1, rsh=lerp(60, 100, eout(pop(sl, 10, 30))), rel=-10, torso=lerp(0, 22, eout(pop(sl, 10, 30))))
        cx, cy, z, rot = 600, 1110, kf(sl, [(0, 1.0), (62, 1.08)], eout), 0
    ctx.save(); cam(ctx, cx, cy, kf(sl, [(0, z), (58, z * 1.06)], eout), rot, shake_at(f, [GONE[3] + 4], 10, 16), f)

    def extra(ctx, bh, dh, mh):
        fx, fy = bh['front']; bx_, by_ = bh['back']
        for g_, (x1, y1) in zip(GONE[:5], [(NAP[0], NAP[1] - 40)] * 2 + [(POT[0], POT[1] - 70)] * 2 + [(DP[0], DP[1])]):
            if g_ - 14 <= f < g_:
                hx_, hy_ = (fx, fy) if g_ not in GONE[2:4] else (bx_, by_)
                flying(ctx, KP[0], KP[1], x1, y1, (f - g_ + 14) / 14, 120)
    scene(ctx, f, boy=pose, nap=nap, pot_n=pot, dad_n=dadn, plant_burp=burp, nap_wob=0.08 * math.sin(lf) * (1 - pop(f, GONE[1], GONE[1] + 12)) if step == 0 and f >= GONE[0] else 0,
          extra=extra)
    ctx.restore()
    texts = ["STEP 1: THE NAPKIN", "STEP 2: FEED THE PLANT", "STEP 3: DAD'S PLATE"]
    label(ctx, texts[step], 540, 1360, 72, hx('ffe14d'), -0.02, pop(sl, 2, 6))
    sub = [("*STUFF* *STUFF*", 20), ("*BURP!*", GONE[3] + 4 - 280), ("HE'LL NEVER KNOW.", 40)][step]
    if sl >= sub[1]:
        label(ctx, sub[0], 540, 1470, 80, (1, 1, 1), 0.03, pop(sl, sub[1], sub[1] + 4))
    card(ctx, 'p3', f, 224, 396)


def s4(ctx, f):
    lf = f - 400
    # tracking shot: follow each launched floret across the table in slow-mo, Dad's fork snatches it
    launches = [g - 400 - 22 for g in GONE[5:]]      # launch frames (local)
    dadn = 5
    cam_x = 470
    cur = None
    for i, L0 in enumerate(launches):
        if L0 - 6 <= lf < L0 + 34:
            cur = (i, lf - L0)
    if cur:
        i, t = cur
        cam_x = kf(t, [(-6, 470), (0, 470), (22, 760), (34, 760)], ease)
    landed = sum(1 for L0 in launches if lf >= L0 + 22)
    eaten = sum(1 for L0 in launches if lf >= L0 + 30)
    dadn = 4 + landed - eaten
    z = 1.35
    ctx.save(); cam(ctx, cam_x, 1120, z, 0, shake_at(lf, [L0 + 22 for L0 in launches], 6, 10), f)
    flick = cur is not None and 0 <= cur[1] < 6
    pose = sit(eye='smug', mouth='grin', shades=1, lsh=30, lel=-100, rsh=70 if not flick else 120, rel=-80 if not flick else -10)

    def extra(ctx, bh, dh, mh):
        fx, fy = bh['front']
        loaded = cur is not None and cur[1] < 0
        spoon(ctx, fx + 10, fy + 10, 0.9 if not flick else 0.2, 1.35, load=loaded)
        if cur and 0 <= cur[1] < 22:
            t = cur[1] / 22
            # speed lines + slow-mo arc
            x = lerp(fx + 40, DP[0], t); y = lerp(fy - 40, DP[1] - 10, t) - math.sin(math.pi * t) * 260
            for k in range(5):
                ctx.move_to(x - 60 - k * 18, y - 30 + k * 15); ctx.line_to(x - 140 - k * 18, y - 30 + k * 15); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(5); ctx.stroke()
            broc(ctx, x, y, 1.1, t * 5)
        # Dad's fork hand from under the newspaper
        if cur and 22 <= cur[1] < 34:
            u = (cur[1] - 22) / 12
            reach = math.sin(math.pi * u)
            hx_, hy_ = DP[0] + 70 - 40 * reach, 1170 + 60 * reach
            ctx.new_path(); ctx.move_to(DX - 20, 1130); ctx.line_to(hx_, hy_); setc(ctx, INK); ctx.set_line_width(48); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke_preserve()
            setc(ctx, DAD['skin']); ctx.set_line_width(38); ctx.stroke()
            fork(ctx, hx_ - 20, hy_ + 10, -2.6, 0.9)
            ellipse(ctx, hx_, hy_, 24, 24); fl(ctx, DAD['skin'], 4)
            if u < 0.5:
                broc(ctx, hx_ - 30, hy_ + 30, 0.6)
    scene(ctx, f, boy=pose, nap=2, pot_n=2, dad_n=dadn, extra=extra, paper=0.0)
    ctx.restore()
    if cur and 0 <= cur[1] < 20:
        label(ctx, "SLOW-MO", 540, 1440, 90, hx('5fc8ff'), -0.03, pop(cur[1], 0, 4))
    elif cur and 22 <= cur[1] < 40:
        label(ctx, "*CRUNCH*", 540, 1440, 110, hx('5fd07a'), 0.04, pop(cur[1], 24, 28))
    card(ctx, 'p4', f, 404, 536)


def s5(ctx, f):
    lf = f - 540
    walk_in = eout(pop(lf, 0, 36))
    mx = lerp(1300, 600, walk_in)
    claim = lf >= 96

    def mom(ctx):
        if lf < 36:
            mp = walk(lf * 0.5, eye='normal', mouth='smile', rsh=90, rel=-20)
        else:
            mp = P(eye='smug' if lf < 96 else 'normal', mouth='smile', rsh=95, rel=-15, lsh=-40, lel=-80)
        h = draw(ctx, mx, 1500 - 186 * KM - 160, KM, -1, MOM, mp)
        return h

    def extra(ctx, bh, dh, mh):
        fx, fy = mh['front']
        cake(ctx, fx - 20, fy + 10, 0.9, glow=pop(lf, 36, 50))
    bp = boy_pose('cheer' if claim else 'eat', eye='happy' if claim else 'shock', mouth='grin' if claim else 'open', shades=0)
    z = kf(lf, [(0, 1.0), (40, 1.0), (90, 1.3), (96, 1.05), (180, 1.12)], eout)
    cx = kf(lf, [(0, 560), (40, 560), (90, 600), (96, 500)], eout)
    ctx.save(); cam(ctx, cx, kf(lf, [(0, 1050), (90, 950), (96, 1060)], eout), z, kf(lf, [(0, 0), (90, -4), (96, 0)]), shake_at(lf, [96], 10, 16), f)
    scene(ctx, f, boy=bp, kid_n=0, nap=2, pot_n=2, dad_n=0, mom=mom, extra=extra)
    if lf >= 40:
        for i in range(6):
            a = lf * 0.08 + i * 1.05
            sparkle(ctx, mx - 60 + math.cos(a) * 200, 880 + math.sin(a) * 150, 26 * (0.6 + 0.4 * math.sin(lf * 0.3 + i)), hx('fff27a'))
    if claim:
        sparkle(ctx, KP[0] - 60, KP[1] - 20, 30 * pop(lf, 96, 104), (1, 1, 1)); sparkle(ctx, KP[0] + 70, KP[1] - 10, 22 * pop(lf, 100, 108), (1, 1, 1))
    ctx.restore()
    if 40 <= lf < 92:
        label(ctx, "WHO ATE THE MOST", 540, 1360, 80, (1, 1, 1), 0.02, pop(lf, 40, 44))
        label(ctx, "BROCCOLI?", 540, 1470, 100, hx('5fd07a'), -0.03, pop(lf, 50, 54))
    elif claim:
        label(ctx, "ME! I ATE ALL MINE!", 540, 1440, 84, hx('ffe14d'), 0.03, pop(lf, 96, 100))
    card(ctx, 'p5', f, 544, 716)


def s6(ctx, f):
    lf = f - 720
    lower = eout(pop(lf, 10, 40))
    give = lf >= 104
    # ECU on the newspaper sliding down -> Dad reveal; whip to kid shock; Mom hands cake to Dad
    mom_x = 600

    def mom(ctx):
        mp = P(eye='shock' if 64 <= lf < 104 else 'smug', mouth='open' if 64 <= lf < 104 else 'smile', rsh=95 if not give else 70, rel=-15, lsh=-40, lel=-80,
               torso=0 if not give else 14)
        return draw(ctx, mom_x, 1500 - 186 * KM - 160, KM, -1, MOM, mp)

    def extra(ctx, bh, dh, mh):
        fx, fy = mh['front']
        cx_ = lerp(fx - 20, DP[0] - 10, eout(pop(lf, 104, 120)))
        cy_ = lerp(fy + 10, DP[1] - 5, eout(pop(lf, 104, 120)))
        cake(ctx, cx_, cy_, 0.9, glow=1.0 if lf >= 120 else 0.4)
    dp = sit(eye='smug', mouth='grin', shades=0, lsh=60, lel=-120, rsh=150 if 40 <= lf < 100 else 60, rel=-30 if 40 <= lf < 100 else -120)
    kid_shock = lf >= 70
    bp = boy_pose('slump' if lf >= 120 else 'cheer', eye='shock' if kid_shock else 'happy', mouth='scream' if kid_shock else 'grin')
    if lf < 60:
        cx, cy, z = 760, 960, 2.0
    elif lf < 100:
        cx, cy, z = BX + 20, 980, 2.1
    else:
        cx, cy, z = 600, 1060, kf(lf, [(100, 1.0), (160, 1.08)], eout)
    ctx.save(); cam(ctx, cx, cy, z, (4 if lf < 60 else (-5 if lf < 100 else 0)), shake_at(lf, [60, 70, 120], 10, 20), f)
    scene(ctx, f, boy=bp, dad=dp, kid_n=0, nap=2, pot_n=2, dad_n=0, paper=lower, mom=mom, extra=extra,
          paper_on=lower < 1, mom_back=True)
    ctx.restore()
    if 40 <= lf < 70:
        label(ctx, "I ATE MINE...", 540, 1380, 96, hx('ffe14d'), -0.03, pop(lf, 40, 44))
        if lf >= 52:
            label(ctx, "...AND HIS.", 540, 1480, 96, hx('ff6b8a'), 0.03, pop(lf, 52, 56))
    elif 70 <= lf < 100:
        label(ctx, "WAIT, WHAT?!", 540, 1440, 120, (1, 1, 1), 0.04, pop(lf, 70, 74))
    elif lf >= 120:
        label(ctx, "*BUSTED*", 540, 1440, 130, hx('ff3b5c'), -0.05, pop(lf, 120, 124))
    card(ctx, 'p6', f, 724, 876)


def s7(ctx, f):
    lf = f - 880
    bowl_at = 70
    shades = 128
    # Dad eats the cake with his shades on; Mom drops a huge bowl of seconds; both slide shades on
    bite = clamp((lf - 10) / 40)
    dp = sit(eye='smug', mouth='grin', shades=1 if lf < bowl_at or lf >= shades else 0, lsh=60, lel=-120,
             rsh=80 if lf < 50 else 60, rel=-60 if lf < 50 else -120, head=6 if lf < 50 else 0)
    if lf >= bowl_at and lf < shades:
        dp.update(eye='shock', mouth='open')
    bp = boy_pose('slump' if lf < bowl_at else ('eat' if lf < shades - 10 else 'shades'), eye='glare' if lf < bowl_at else ('shock' if lf < shades else 'smug'),
                  mouth='frown' if lf < bowl_at else ('open' if lf < shades else 'grin'), shades=1 if lf >= shades else 0,
                  shades_dy=lerp(-1.4, 0, eout(pop(lf, shades, shades + 10))))
    if lf >= shades:
        dp['shades_dy'] = lerp(-1.4, 0, eout(pop(lf, shades + 4, shades + 14)))

    def mom(ctx):
        if lf < bowl_at - 20:
            return None
        mx = lerp(1250, 610, eout(pop(lf, bowl_at - 20, bowl_at - 4)))
        mp = P(eye='happy', mouth='grin', rsh=100, rel=-20, lsh=-40, lel=-80)
        return draw(ctx, mx, 1500 - 186 * KM - 160, KM, -1, MOM, mp)

    def extra(ctx, bh, dh, mh):
        if lf < bowl_at:
            cake(ctx, DP[0] - 10, DP[1] - 5, 0.9, bite=bite)
        else:
            plate(ctx, *DP, 0)
            drop = eout(pop(lf, bowl_at - 6, bowl_at))
            big_bowl(ctx, 590, lerp(1000, 1240, drop), 1.0)
        if lf < 50:
            fork(ctx, dh['front'][0] - 10, dh['front'][1] + 6, -2.4, 0.9)
    if lf < bowl_at:
        cx, cy, z = 640, 1070, kf(lf, [(0, 1.35), (bowl_at, 1.5)], eout)
    else:
        cx, cy, z = 580, 1060, kf(lf, [(bowl_at, 1.0), (bowl_at + 6, 1.08), (170, 1.2)], eout)
    ctx.save(); cam(ctx, cx, cy, z, 0, shake_at(lf, [bowl_at, shades + 14], 12, 22), f)
    scene(ctx, f, boy=bp, dad=dp, kid_n=0, nap=2, pot_n=2, dad_n=0, paper_on=False, mom=mom, extra=extra, mom_back=True)
    if lf >= shades + 14:
        for i in range(4):
            sparkle(ctx, 300 + i * 170, 760 + (i % 2) * 60, 26 * pop(lf, shades + 14, shades + 20), hx('fff27a'))
    ctx.restore()
    if 8 <= lf < 60:
        label(ctx, "THANKS, PARTNER.", 540, 1440, 90, hx('ffe14d'), -0.02, pop(lf, 8, 12))
    elif bowl_at <= lf < shades:
        label(ctx, "SECONDS, ANYONE?", 540, 1440, 96, hx('5fd07a'), 0.03, pop(lf, bowl_at, bowl_at + 4))
    elif lf >= shades + 14:
        label(ctx, "NEW PLAN.", 540, 1440, 130, (1, 1, 1), 0.04, pop(lf, shades + 14, shades + 18))
    card(ctx, 'p7', f, 884)


SHOTS = [(0, s1), (100, s2), (220, s3), (400, s4), (540, s5), (720, s6), (880, s7)]


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.25)
    ctx.set_source(g); ctx.paint()
    for c in (100, 220, 280, 338, 400, 540, 720, 780, 820, 880, 950):
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.5 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/v{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/veggie_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
