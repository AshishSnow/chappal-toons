"""'Are We There Yet?' - original, general-audience comedy short, ~35s.
Road trip, minute one: the kid asks "are we there yet?" (still in the driveway). He escalates (sign, sock puppet,
song) until Dad deploys THE QUIET GAME. Hours of peace... they arrive, and the kid finally speaks:
"CAN WE GO HOME NOW?" Dad faceplants on the horn. Road trip home, minute one."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip, head
from scenes6 import cam, pop, sparkle, puff, label, shake_at
from scenes8 import sit
from scenes13 import card as _card13
import scenes13

BOY = dict(doodle.BOY)
DAD = dict(doodle.DAD, shades=True)
N = 1050
KB, KD = 1.05, 1.25
BX, BHIP = 380, 1330          # kid in back seat
DX, DHIP = 720, 1340          # dad at the wheel
ROOF, SILL, ROADY = 820, 1240, 1545
WHL = ((250, 1450), (840, 1450))

CAPS = {
    'p1': [[("ROAD TRIP,", OUT)], [("MINUTE ", OUT), ("ONE", hx('ff3b5c')), (":", OUT)]],
    'p2': [[("5 MINUTES ", OUT), ("LATER", hx('1f8bff'))]],
    'p3': [[("THEN HE GOT ", OUT), ("CREATIVE", hx('8a3cff'))]],
    'p4': [[("DAD'S SECRET WEAPON:", OUT)], [("THE QUIET GAME", hx('2a9d3a'))]],
    'p5': [[("3 HOURS OF ", OUT), ("PURE", hx('1f8bff'))], [("SILENCE", hx('1f8bff'))]],
    'p6': [[("FINALLY THERE.", OUT)], [("AND THEN HE ", OUT), ("SPOKE", hx('ff3b5c'))]],
    'p7': [[("ROAD TRIP HOME,", OUT)], [("MINUTE ", OUT), ("ONE", hx('ff3b5c')), (":", OUT)]],
}
scenes13.CAPS = CAPS
card = _card13


def rect_r(ctx, x, y, w, h, r):
    ctx.new_path(); ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); ctx.close_path()


def mixc(a, b, t):
    return tuple(lerp(a[i], b[i], t) for i in range(3))


def tod_col(tod, day, dusk, night):
    return mixc(day, dusk, tod) if tod <= 1 else mixc(dusk, night, tod - 1)


def wtext(ctx, s, x, y, size, col):
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    w = ctx.text_extents(s).x_advance
    ctx.move_to(x - w / 2, y); ctx.text_path(s); setc(ctx, col); ctx.fill()


# ------------------------------------------------------------------ world
def tree(ctx, x, y, s, col):
    ctx.rectangle(x - 10 * s, y - 60 * s, 20 * s, 60 * s); fl(ctx, hx('8a5a34'), 4)
    for dx, dy, r in ((-30, -90, 46), (30, -90, 46), (0, -130, 54)):
        ellipse(ctx, x + dx * s, y + dy * s, r * s, r * s); fl(ctx, col, 4)


def house(ctx, x, y, col=hx('ff8a6a'), roof=hx('8a3cff'), sign=None):
    """y = ground line"""
    ctx.rectangle(x - 260, y - 360, 520, 360); fl(ctx, col, 7)
    poly(ctx, [(x - 310, y - 350), (x, y - 600), (x + 310, y - 350)]); fl(ctx, roof, 7)
    ctx.rectangle(x - 60, y - 200, 120, 200); fl(ctx, hx('7a4a2c'), 6)
    ellipse(ctx, x + 36, y - 100, 9, 9); fl(ctx, hx('ffd23f'), 3)
    for wx in (x - 180, x + 120):
        ctx.rectangle(wx, y - 290, 90, 90); fl(ctx, hx('fff6c2'), 6)
        ctx.move_to(wx + 45, y - 290); ctx.line_to(wx + 45, y - 200); ctx.move_to(wx, y - 245); ctx.line_to(wx + 90, y - 245); ink(ctx, 4); ctx.stroke()
    if sign:
        # mailbox with a name on it
        mx = x + 360
        ctx.rectangle(mx - 8, y - 150, 16, 150); fl(ctx, hx('7a4a2c'), 4)
        rect_r(ctx, mx - 110, y - 230, 220, 90, 30); fl(ctx, hx('1f8bff'), 6)
        wtext(ctx, sign, mx, y - 170, 40, (1, 1, 1))


def world(ctx, f, scroll=0.0, tod=0.0, houses=(), signs=()):
    sky = tod_col(tod, hx('8fe0ff'), hx('ff9e6b'), hx('1c2560'))
    ctx.rectangle(-1500, -1500, 4200, 4200); setc(ctx, sky); ctx.fill()
    # sun / moon
    if tod < 1.5:
        sy = lerp(520, 1150, clamp(tod / 1.4))
        ellipse(ctx, 820, sy, 90, 90); setc(ctx, tod_col(min(tod, 1), hx('ffe14d'), hx('ff6a3d'), hx('ff6a3d'))); ctx.fill()
    if tod > 1.2:
        a = clamp((tod - 1.2) / 0.6)
        ellipse(ctx, 250, 560, 70, 70); setc(ctx, (1, 0.97, 0.8, a)); ctx.fill()
        ellipse(ctx, 280, 545, 62, 62); setc(ctx, sky + (a,)); ctx.fill()
        for i in range(14):
            sparkle(ctx, (i * 173) % 1300 - 100, 380 + (i * 97) % 560, 9 * a, (1, 1, 1))
    for i in range(6):
        cx_ = ((i * 520 - scroll * 0.05) % 3000) - 900
        for dx, r in ((0, 70), (70, 90), (150, 60)):
            ellipse(ctx, cx_ + dx, 470 + (i % 3) * 120, r, r * 0.6); setc(ctx, (1, 1, 1, 0.85 - 0.5 * clamp(tod - 0.8))); ctx.fill()
    # far hills
    hill = tod_col(tod, hx('6fd06a'), hx('c98a5a'), hx('2a3a6a'))
    off = -(scroll * 0.15) % 900
    ctx.new_path(); ctx.move_to(-1500, 1400)
    for i in range(-3, 6):
        x0 = i * 900 + off - 900
        ctx.curve_to(x0 + 200, 1000, x0 + 500, 980, x0 + 900, 1380)
    ctx.line_to(2700, 1400); ctx.line_to(2700, 2000); ctx.line_to(-1500, 2000); ctx.close_path(); fl(ctx, hill, 6)
    # mid trees
    tcol = tod_col(tod, hx('2fbf5a'), hx('a07a3a'), hx('1f4a4a'))
    off = -(scroll * 0.5) % 300
    for i in range(-6, 12):
        tree(ctx, i * 300 + off, 1440, 1.2 + 0.3 * ((i * 7) % 3), tcol)
    # grass band + houses / signs (near layer, 1x)
    ctx.rectangle(-1500, 1440, 4200, 120); setc(ctx, tod_col(tod, hx('5fd07a'), hx('b0904a'), hx('2a4a4a'))); ctx.fill()
    for hx_, lab in houses:
        house(ctx, hx_ - scroll, 1500, sign=lab)
    for sx_, l1, l2, *rest in signs:
        x = sx_ - scroll
        col = rest[0] if rest else hx('1e9e5a'); y0 = rest[1] if len(rest) > 1 else 560
        ctx.rectangle(x - 10, y0 + 240, 20, 1500 - y0 - 240); fl(ctx, hx('9a9aa8'), 4)
        rect_r(ctx, x - 230, y0, 460, 250, 24); fl(ctx, col, 7)
        rect_r(ctx, x - 212, y0 + 18, 424, 214, 16); setc(ctx, (1, 1, 1)); ctx.set_line_width(5); ctx.stroke()
        wtext(ctx, l1, x, y0 + 105, 54, (1, 1, 1)); wtext(ctx, l2, x, y0 + 190, 64, hx('ffe14d'))
    # road
    ctx.rectangle(-1500, 1500, 4200, 260); setc(ctx, hx('4a4a5a')); ctx.fill()
    ctx.move_to(-1500, 1500); ctx.line_to(2700, 1500); ink(ctx, 7); ctx.stroke()
    off = -(scroll * 1.0) % 240
    for i in range(-7, 14):
        ctx.rectangle(i * 240 + off, 1640, 130, 18); setc(ctx, hx('ffe14d')); ctx.fill()
    ctx.rectangle(-1500, 1760, 4200, 600); setc(ctx, tod_col(tod, hx('4fb86a'), hx('9a7a3a'), hx('1f3a3a'))); ctx.fill()
    ctx.move_to(-1500, 1760); ctx.line_to(2700, 1760); ink(ctx, 7); ctx.stroke()


# ------------------------------------------------------------------ car
CARC = hx('ff3b5c')


def car_back(ctx, dy):
    ctx.save(); ctx.translate(0, dy)
    # far-side door panel shadow inside cabin + seats
    rect_r(ctx, 170, 1010, 90, 260, 30); fl(ctx, hx('3d5a9e'), 6)       # back seat backrest
    rect_r(ctx, 180, 950, 70, 70, 20); fl(ctx, hx('3d5a9e'), 5)
    rect_r(ctx, 560, 1000, 90, 270, 30); fl(ctx, hx('3d5a9e'), 6)       # driver seat backrest
    rect_r(ctx, 570, 930, 70, 80, 22); fl(ctx, hx('3d5a9e'), 5)
    # dashboard
    poly(ctx, [(880, 1140), (990, 1140), (1000, 1260), (860, 1260)]); fl(ctx, hx('2a2a3a'), 6)
    ctx.restore()


def wheel_steer(ctx, dy, turn=0.0):
    ctx.save(); ctx.translate(890, 1135 + dy); ctx.rotate(-0.35)
    ctx.move_to(0, 0); ctx.line_to(60, 70); ink(ctx, 14); ctx.stroke()
    ellipse(ctx, 0, 0, 22, 92); setc(ctx, INK); ctx.set_line_width(22); ctx.stroke()
    ellipse(ctx, 0, 0, 22, 92); setc(ctx, hx('5a5a6a')); ctx.set_line_width(12); ctx.stroke()
    ctx.restore()


def car_front(ctx, dy, scroll, horn=0.0):
    ctx.save(); ctx.translate(0, dy)
    # glass tint + reflection
    for pts in ([(215, ROOF + 20), (545, ROOF + 20), (545, SILL), (110, SILL)], [(590, ROOF + 20), (800, ROOF + 20), (920, SILL), (590, SILL)]):
        poly(ctx, pts); setc(ctx, (0.75, 0.92, 1, 0.12)); ctx.fill()
    for x0 in (300, 660):
        poly(ctx, [(x0, ROOF + 30), (x0 + 40, ROOF + 30), (x0 - 60, SILL - 10), (x0 - 100, SILL - 10)]); setc(ctx, (1, 1, 1, 0.18)); ctx.fill()
    # roof + pillars
    poly(ctx, [(180, ROOF - 10), (810, ROOF - 10), (830, ROOF + 22), (200, ROOF + 22)]); fl(ctx, CARC, 7)
    poly(ctx, [(190, ROOF), (225, ROOF), (120, SILL), (60, SILL)]); fl(ctx, CARC, 7)       # C pillar
    poly(ctx, [(545, ROOF), (590, ROOF), (590, SILL), (545, SILL)]); fl(ctx, CARC, 7)       # B pillar
    poly(ctx, [(790, ROOF), (825, ROOF), (960, SILL), (915, SILL)]); fl(ctx, CARC, 7)       # A pillar
    # body
    ctx.new_path(); ctx.move_to(40, SILL); ctx.line_to(960, SILL); ctx.curve_to(1040, SILL, 1060, 1280, 1060, 1340)
    ctx.line_to(1060, 1420); ctx.curve_to(1060, 1450, 1040, 1460, 1010, 1460); ctx.line_to(70, 1460)
    ctx.curve_to(40, 1460, 20, 1440, 20, 1400); ctx.line_to(20, 1290); ctx.curve_to(20, 1260, 30, SILL, 40, SILL); ctx.close_path()
    fl(ctx, CARC, 7)
    ctx.move_to(40, 1330); ctx.line_to(1050, 1330); setc(ctx, (1, 1, 1, 0.35)); ctx.set_line_width(10); ctx.stroke()
    ctx.move_to(568, SILL); ctx.line_to(568, 1440); ink(ctx, 4); ctx.stroke()
    for hx_ in (470, 860):
        rect_r(ctx, hx_, 1275, 60, 16, 8); fl(ctx, hx('e0e0ea'), 3)
    ellipse(ctx, 1040, 1300, 26, 20); fl(ctx, hx('fff27a'), 4)                 # headlight
    rect_r(ctx, 22, 1280, 22, 40, 6); fl(ctx, hx('ff8a3d'), 3)                   # tail light
    # luggage on the roof
    rect_r(ctx, 260, ROOF - 110, 300, 100, 20); fl(ctx, hx('ffc93c'), 6)
    rect_r(ctx, 580, ROOF - 80, 160, 70, 16); fl(ctx, hx('19b5a5'), 6)
    ctx.move_to(240, ROOF - 60); ctx.line_to(760, ROOF - 60); ink(ctx, 6); ctx.stroke()
    ctx.restore()
    # wheels (no bounce)
    for wx, wy in WHL:
        ellipse(ctx, wx, wy, 98, 98); fl(ctx, hx('2a2a3a'), 7)
        ellipse(ctx, wx, wy, 52, 52); fl(ctx, hx('d8dbe8'), 5)
        a0 = scroll / 98.0
        for k in range(5):
            a = a0 + k * 2 * math.pi / 5
            ctx.move_to(wx, wy); ctx.line_to(wx + math.cos(a) * 46, wy + math.sin(a) * 46); ink(ctx, 6); ctx.stroke()
        ellipse(ctx, wx, wy, 12, 12); fl(ctx, hx('ff3b5c'), 4)
    if horn > 0:
        for k in range(3):
            r = 60 + k * 50 + 40 * horn
            ctx.new_path(); ctx.arc(1080, 1310, r, -0.6, 0.6); setc(ctx, (1, 0.9, 0.2, 0.9)); ctx.set_line_width(12); ctx.stroke()


def dad_drive(**kw):
    p = sit(lsh=78, lel=-30, rsh=74, rel=-24, eye='normal', mouth='smile', torso=4)
    p.update(kw); return p


def kid_sit(**kw):
    p = sit(lsh=40, lel=-60, rsh=40, rel=-60, eye='normal', mouth='smile')
    p.update(kw); return p


def car_scene(ctx, f, scroll=0.0, tod=0.0, moving=True, boy=None, dad=None, houses=(), signs=(), boy_after=None, extra=None,
              horn=0.0, kb=KB, puffed=0.0):
    world(ctx, f, scroll, tod, houses, signs)
    dy = (5 * math.sin(f * 0.9) + 2 * math.sin(f * 2.3)) if moving else 0
    car_back(ctx, dy)
    bh = draw_hip(ctx, BX, BHIP + dy, kb, 1, BOY, boy or kid_sit())
    if puffed > 0:
        x, y = bh['head']; R = bh['R']
        for sx in (-0.45, 0.62):
            ellipse(ctx, x + sx * R, y + R * 0.42, R * 0.26 * puffed, R * 0.2 * puffed); setc(ctx, (1, 0.25, 0.3, 0.55)); ctx.fill()
    if boy_after:
        boy_after(ctx, bh)
    dh = draw_hip(ctx, DX, DHIP + dy, KD, 1, DAD, dad or dad_drive())
    wheel_steer(ctx, dy)
    car_front(ctx, dy, scroll, horn)
    if extra:
        extra(ctx, bh, dh)
    return bh, dh


# ------------------------------------------------------------------ props
def paper_sign(ctx, x, y, a, txt=("ARE WE", "THERE YET?")):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    rect_r(ctx, -140, -100, 280, 180, 10); fl(ctx, (1, 1, 1), 6)
    wtext(ctx, txt[0], 0, -30, 44, hx('ff3b5c')); wtext(ctx, txt[1], 0, 34, 44, hx('ff3b5c'))
    ctx.restore()


def sock_puppet(ctx, x, y, talk):
    ctx.save(); ctx.translate(x, y)
    ctx.new_path(); ctx.move_to(-34, 60); ctx.line_to(-34, -60); ctx.curve_to(-34, -110, 70, -110, 80, -70)
    ctx.line_to(80, -40 + 20 * talk); ctx.line_to(20, -40 + 10 * talk); ctx.line_to(34, 60); ctx.close_path(); fl(ctx, hx('19b5a5'), 6)
    ctx.new_path(); ctx.move_to(80, -60); ctx.line_to(20, -48); ctx.line_to(80, -40 + 20 * talk); ctx.close_path(); fl(ctx, hx('ff6b8a'), 4)
    for ex in (-4, 24):
        ellipse(ctx, ex, -82, 13, 13); fl(ctx, (1, 1, 1), 4); ellipse(ctx, ex + 3, -80, 5, 6); setc(ctx, INK); ctx.fill()
    ctx.rectangle(-36, 30, 72, 22); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.restore()


def note(ctx, x, y, s, col):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 18, 13, -0.4); fl(ctx, col, 4)
    ctx.rectangle(14, -70, 7, 70); setc(ctx, INK); ctx.fill()
    poly(ctx, [(14, -70), (44, -52), (44, -40), (21, -54)]); setc(ctx, INK); ctx.fill()
    ctx.restore()


def sweat(ctx, x, y, s=1.0):
    ctx.new_path(); ctx.move_to(x, y - 26 * s); ctx.curve_to(x + 16 * s, y, x + 14 * s, y + 16 * s, x, y + 16 * s)
    ctx.curve_to(x - 14 * s, y + 16 * s, x - 16 * s, y, x, y - 26 * s); fl(ctx, hx('7fd4ff'), 3)


def twitch(ctx, x, y, a):
    for k in range(3):
        ang = -0.9 + k * 0.6
        ctx.move_to(x + math.cos(ang) * 50, y + math.sin(ang) * 50 - 30)
        ctx.line_to(x + math.cos(ang) * (80 + 10 * a), y + math.sin(ang) * (80 + 10 * a) - 30)
    ink(ctx, 7); ctx.stroke()


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    # ECU on the kid's eager face, pull back: car is still in the driveway
    pull = eout(pop(f, 34, 62))
    z = lerp(2.7, 1.0, pull)
    cx = lerp(BX + 30, 540, pull); cy = lerp(1040, 1120, pull)
    ctx.save(); cam(ctx, cx, cy, z, lerp(-3, 0, pull), shake_at(f, [64], 8, 14), f)
    dad = dad_drive(eye='glare' if f >= 64 else 'normal', mouth='flat' if f >= 64 else 'smile')
    car_scene(ctx, f, 0, 0, moving=False, houses=((300, None),),
              boy=kid_sit(eye='happy', mouth='grin', rsh=150 if f < 34 else 40, rel=-30 if f < 34 else -60, head=-4))
    ctx.restore()
    if 6 <= f < 60:
        label(ctx, "ARE WE THERE YET?", 540, 1420, 100, hx('ffe14d'), -0.03, pop(f, 6, 10))
    elif f >= 64:
        label(ctx, "WE'RE STILL IN", 540, 1380, 84, (1, 1, 1), 0.02, pop(f, 64, 68))
        label(ctx, "THE DRIVEWAY.", 540, 1480, 92, hx('ff6b8a'), -0.02, pop(f, 70, 74))
    card(ctx, 'p1', f, 0, 98)


def mirror_shot(ctx, f, lf, mood):
    """rear-view mirror ECU on Dad's eyes; mood 0..2"""
    # windshield view behind the mirror
    ctx.rectangle(0, 0, W, H); setc(ctx, hx('8fe0ff')); ctx.fill()
    poly(ctx, [(-200, 1500), (540, 1060), (1280, 1500)]); setc(ctx, hx('4a4a5a')); ctx.fill()
    ctx.rectangle(-10, 1060, 1100, 10); setc(ctx, hx('6fd06a')); ctx.fill()
    for k in range(5):
        t = ((f * 0.06 + k / 5) % 1)
        y = lerp(1080, 1520, t ** 2); w = lerp(4, 40, t ** 2)
        ctx.rectangle(540 - w / 2, y, w, w * 2.2); setc(ctx, hx('ffe14d')); ctx.fill()
    ctx.rectangle(0, 1500, W, 500); setc(ctx, hx('2a2a3a')); ctx.fill()
    ctx.move_to(540, 0); ctx.line_to(540, 640); ink(ctx, 16); ctx.stroke()
    sx = 6 * math.sin(lf * 2.2) * (mood >= 2)
    ctx.save(); ctx.translate(sx, 0)
    rect_r(ctx, 90, 640, 900, 420, 80); fl(ctx, hx('2a2a3a'), 10)
    rect_r(ctx, 120, 670, 840, 360, 60); ctx.save(); ctx.clip()
    ctx.rectangle(0, 0, W, H); setc(ctx, hx('3d5a9e')); ctx.fill()
    ctx.save(); ctx.translate(540, 900)
    eye = ('normal', 'smug', 'glare')[mood]
    head(ctx, 420, DAD, P(eye=eye, mouth='flat'), 1, 12)
    ctx.restore()
    if mood >= 1:
        twitch(ctx, 820, 860, math.sin(lf * 1.5))
    ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.06)); ctx.fill()
    poly(ctx, [(300, 670), (380, 670), (240, 1030), (160, 1030)]); setc(ctx, (1, 1, 1, 0.15)); ctx.fill()
    ctx.restore()
    rect_r(ctx, 120, 670, 840, 360, 60); ink(ctx, 8); ctx.stroke()
    ctx.restore()


def s2(ctx, f):
    lf = f - 100
    sc = lf * 40
    if lf < 40:
        ctx.save(); cam(ctx, 540, 1120, kf(lf, [(0, 0.95), (40, 1.05)], eout), 0, 0, f)
        car_scene(ctx, f, sc, 0, signs=((1600, "GRANDMA'S HOUSE", "300 MILES", hx("1e9e5a"), 640),),
                  boy=kid_sit(eye='normal', mouth='open' if lf > 24 else 'smile'))
        ctx.restore()
        if lf >= 24:
            label(ctx, "ARE WE THERE YET?", 540, 1440, 96, hx('ffe14d'), 0.03, pop(lf, 24, 28))
        card(ctx, 'p2', f, 102, 216)
        return
    beat = (lf - 40) // 20
    bl = (lf - 40) % 20
    if beat % 2 == 0:
        # whip to ECU of the kid, alternating tilts
        ctx.save(); cam(ctx, BX + 40, 1040, 2.5, 5 if beat == 0 else -6, shake_at(bl, [0], 6, 10), f)
        car_scene(ctx, f, sc, 0, boy=kid_sit(eye='happy' if beat == 0 else 'shock', mouth='grin' if beat == 0 else 'scream', head=-6))
        ctx.restore()
        label(ctx, "ARE WE THERE YET?" if beat == 0 else "ARE WE THERE YET?!", 540, 1440, 92, hx('ffe14d'), 0.03 * (-1) ** beat, pop(bl, 0, 4))
    else:
        mirror_shot(ctx, f, lf, 1 if beat == 1 else 2)
        label(ctx, "NO." if beat == 1 else "NO!!", 540, 1420, 140, (1, 1, 1) if beat == 1 else hx('ff3b5c'), -0.04, pop(bl, 0, 4))
    card(ctx, 'p2', f, 102, 216)


def s3(ctx, f):
    lf = f - 220
    step = 0 if lf < 60 else (1 if lf < 120 else 2)
    sl = lf - step * 60
    sc = f * 40
    dad = dad_drive(eye='glare' if sl > 30 else 'normal', mouth='flat' if sl > 30 else 'smile')

    if step == 0:
        boy = kid_sit(rsh=140, rel=-30, lsh=135, lel=-30, eye='happy', mouth='grin')

        def aft(ctx, bh):
            paper_sign(ctx, 400, 1080 + 8 * math.sin(sl * 0.5), 0.06 * math.sin(sl * 0.3))
        cx, cy, z, rot = 520, 1080, kf(sl, [(0, 1.45), (58, 1.6)], eout), -3
    elif step == 1:
        talk = abs(math.sin(sl * 0.6))
        boy = kid_sit(rsh=165, rel=-5, eye='smug', mouth='smile')

        def aft(ctx, bh):
            x, y = bh['front']
            sock_puppet(ctx, x, y - 30, talk if sl > 14 else 0)
        cx, cy, z, rot = 470, 1010, kf(sl, [(0, 1.7), (58, 1.9)], eout), 4
    else:
        boy = kid_sit(rsh=170 + 10 * math.sin(sl * 0.4), rel=-20, lsh=-170, lel=-20, eye='happy', mouth='scream', head=6 * math.sin(sl * 0.4))

        def aft(ctx, bh):
            for k in range(4):
                t = ((sl * 0.03 + k * 0.25) % 1)
                note(ctx, bh['head'][0] + 80 + t * 380, bh['head'][1] - 60 - t * 200 + 20 * math.sin(t * 9), 1.2, (hx('ff3b5c'), hx('1f8bff'), hx('2a9d3a'), hx('8a3cff'))[k])
        cx, cy, z, rot = 560, 1090, kf(sl, [(0, 1.15), (58, 1.3)], eout), 0

    def ext(ctx, bh, dh):
        if sl > 30:
            x, y = dh['head']
            twitch(ctx, x + 40, y - 40, math.sin(sl))
            sweat(ctx, x - 120, y - 60 + (sl % 20) * 2, 1.2)
    ctx.save(); cam(ctx, cx, cy, z, rot, shake_at(sl, [0], 6, 10), f)
    car_scene(ctx, f, sc, 0, boy=boy, dad=dad, boy_after=aft, extra=ext)
    ctx.restore()
    texts = ["METHOD 1: THE SIGN", "METHOD 2: THE PUPPET", "METHOD 3: THE SONG"]
    label(ctx, texts[step], 540, 1360, 68, hx('ffe14d'), -0.02, pop(sl, 2, 6))
    sub = ["*TAP TAP TAP*", "ARE WE THERE YET?", "ARE WE THERE YEEET~"][step]
    if sl >= 14:
        label(ctx, sub, 540, 1470, 76, (1, 1, 1), 0.03, pop(sl, 14, 18))
    card(ctx, 'p3', f, 224, 396)


def s4(ctx, f):
    lf = f - 400
    sc = f * 40
    zip_at = 80
    # low-angle push on Dad raising one finger, whip to kid zipping his lips, wide shot of calm
    if lf < 66:
        dad = dad_drive(rsh=172, rel=-8, eye='smug', mouth='grin', head=-4)
        ctx.save(); cam(ctx, kf(lf, [(0, 760), (60, 740)], eout), kf(lf, [(0, 1080), (60, 1020)], eout), kf(lf, [(0, 1.6), (60, 2.0)], eout), -6,
                        shake_at(lf, [8], 8, 14), f)
        car_scene(ctx, f, sc, 0, dad=dad, boy=kid_sit(eye='shock', mouth='open'))
        ctx.restore()
        if lf >= 10:
            for i in range(4):
                a = lf * 0.08 + i * 1.57
                sparkle(ctx, 540 + math.cos(a) * 360, 860 + math.sin(a) * 260, 26 * pop(lf, 10, 18), hx('fff27a'))
        if lf >= 22:
            label(ctx, "FIRST ONE TO TALK", 540, 1380, 80, (1, 1, 1), 0.02, pop(lf, 22, 26))
            label(ctx, "LOSES!", 540, 1490, 110, hx('ff3b5c'), -0.03, pop(lf, 30, 34))
    else:
        zl = lf - 66
        t = eout(pop(zl, 4, 20))
        boy = kid_sit(rsh=lerp(70, 60, t), rel=lerp(-120, -150, t), eye='smug' if zl > 20 else 'normal', mouth='flat', head=-4)

        def aft(ctx, bh):
            if 4 <= zl < 26:
                x, y = bh['head']; R = bh['R']
                mx = lerp(x - R * 0.35, x + R * 0.5, t); my = y + R * 0.52
                ctx.move_to(x - R * 0.35, my); ctx.line_to(mx, my); setc(ctx, hx('ffe14d')); ctx.set_line_width(10); ctx.stroke()
        z = kf(zl, [(0, 2.4), (24, 2.4), (40, 1.0)], eout)
        cx = kf(zl, [(0, BX + 40), (24, BX + 40), (40, 540)], eout); cy = kf(zl, [(0, 1030), (24, 1030), (40, 1120)], eout)
        ctx.save(); cam(ctx, cx, cy, z, 0, shake_at(zl, [20], 6, 10), f)
        car_scene(ctx, f, sc, 0, boy=boy, dad=dad_drive(eye='happy', mouth='grin'), boy_after=aft)
        ctx.restore()
        if 4 <= zl < 40:
            label(ctx, "*ZIP*", 540, 1440, 130, hx('ffe14d'), 0.05, pop(zl, 6, 10))
        elif zl >= 44:
            label(ctx, "...", 540, 1440, 140, (1, 1, 1), 0, pop(zl, 44, 48))
    card(ctx, 'p4', f, 404, 536)


def s5(ctx, f):
    lf = f - 540
    # time-lapse: sky runs day -> sunset -> night, scroll speeds up, slow push-in
    tod = kf(lf, [(0, 0.0), (150, 2.0)], ease)
    sc = 21600 + lf * lerp(40, 120, pop(lf, 0, 60))
    puffed = 0.6 + 0.4 * pop(lf, 40, 120)
    boy = kid_sit(eye='glare' if lf > 60 else 'smug', mouth='flat', lsh=40, lel=-110, rsh=40, rel=-110)
    dad = dad_drive(eye='happy', mouth='grin', head=4 * math.sin(lf * 0.15))
    z = kf(lf, [(0, 1.0), (176, 1.3)], ease)

    def aft(ctx, bh):
        x, y = bh['head']; R = bh['R']
        if lf > 70:
            sweat(ctx, x - R * 0.95, y - R * 0.3 + (lf % 24) * 2, 1.2)
            sweat(ctx, x + R * 1.0, y - R * 0.5 + ((lf + 12) % 24) * 2, 1.0)

    def ext(ctx, bh, dh):
        for k in range(3):
            t = ((lf * 0.02 + k / 3) % 1)
            note(ctx, dh['head'][0] + 60 + t * 220, dh['head'][1] - 120 - t * 220, 0.9, hx('ffe14d'))
    ctx.save(); cam(ctx, 560, kf(lf, [(0, 1120), (176, 1060)], ease), z, 0, 0, f)
    car_scene(ctx, f, sc, tod, boy=boy, dad=dad, boy_after=aft, extra=ext, puffed=puffed)
    ctx.restore()
    if 20 <= lf < 80:
        label(ctx, "*HUMMING*", 540, 1440, 100, hx('ffe14d'), -0.03, pop(lf, 20, 24))
    elif lf >= 96:
        label(ctx, "*CRICKETS*", 540, 1440, 100, (1, 1, 1), 0.03, pop(lf, 96, 100))
    card(ctx, 'p5', f, 544, 716)


def s6(ctx, f):
    lf = f - 720
    stop = 40
    # car brakes in front of grandma's house; dad cheers, kid stays silent; "you can talk now!"; huge inhale ECU
    sc_end = 30000
    sc = sc_end - 1400 * (1 - eout(pop(lf, 0, stop)))
    houses = ((sc_end + 420, None),)
    signs = ((sc_end + 920, "WELCOME TO", "GRANDMA'S!", hx('ff3b8a'), 620),)
    moving = lf < stop
    if lf < 100:
        dad = dad_drive(rsh=160 if lf >= stop else 74, rel=-20 if lf >= stop else -24, lsh=150 if lf >= stop else 78, lel=-20 if lf >= stop else -30,
                        eye='happy', mouth='grin', torso=-2)
        boy = kid_sit(lsh=40, lel=-110, rsh=40, rel=-110, eye='smug', mouth='flat')
        z = kf(lf, [(0, 0.85), (stop, 0.85), (60, 1.05), (100, 1.15)], eout)
        cx = kf(lf, [(0, 540), (stop, 540), (60, 560)], eout)
        ctx.save(); cam(ctx, cx, kf(lf, [(0, 1080), (60, 1100)], eout), z, 0, shake_at(lf, [stop], 10, 18), f)
        car_scene(ctx, f, sc, 0.3, moving=moving, dad=dad, boy=boy, houses=houses, signs=signs)
        ctx.restore()
        if lf < stop:
            for k in range(6):
                ctx.move_to(-20, 1300 + k * 50); ctx.line_to(200 - k * 20, 1300 + k * 50); setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(8); ctx.stroke()
            if lf >= 22:
                label(ctx, "*SCREEECH*", 540, 1440, 100, (1, 1, 1), -0.04, pop(lf, 22, 26))
        elif lf < 70:
            label(ctx, "WE'RE HERE!", 540, 1440, 120, hx('ffe14d'), 0.03, pop(lf, stop + 2, stop + 6))
        else:
            label(ctx, "YOU CAN TALK NOW!", 540, 1440, 92, (1, 1, 1), -0.03, pop(lf, 70, 74))
    else:
        il = lf - 100
        inh = eout(pop(il, 4, 50))
        boy = kid_sit(lsh=60 + 40 * inh, lel=-40, rsh=60 + 40 * inh, rel=-40, eye='shock' if il > 4 else 'smug', mouth='open', torso=-8 * inh, head=-10 * inh)
        z = kf(il, [(0, 2.0), (56, 2.8)], eout)
        ctx.save(); cam(ctx, BX + 40, 1030, z, kf(il, [(0, 0), (56, -6)]), shake_at(il, [46], 10, 8) + 3 * inh, f)
        car_scene(ctx, f, sc, 0.3, moving=False, boy=boy, houses=houses, signs=signs, kb=KB * (1 + 0.1 * inh))
        ctx.restore()
        label(ctx, "*DEEP BREATH*", 540, 1440, 100, hx('5fc8ff'), 0.03, pop(il, 6, 10))
    card(ctx, 'p6', f, 724, 876)


def s7(ctx, f):
    lf = f - 880
    honk = 64
    sc_end = 30000
    houses = ((sc_end + 420, None),)
    signs = ((sc_end + 920, "WELCOME TO", "GRANDMA'S!", hx('ff3b8a'), 620),)
    if lf < 56:
        # ECU kid blurts it out
        boy = kid_sit(rsh=150, rel=-30, lsh=140, lel=-30, eye='happy', mouth='scream', torso=-6)
        ctx.save(); cam(ctx, BX + 40, 1030, 2.5, 4, shake_at(lf, [2], 12, 20), f)
        car_scene(ctx, f, sc_end, 0.3, moving=False, boy=boy, houses=houses, signs=signs)
        ctx.restore()
        label(ctx, "CAN WE GO", 540, 1360, 110, hx('ffe14d'), -0.03, pop(lf, 2, 6))
        label(ctx, "HOME NOW?", 540, 1480, 120, hx('ff6b8a'), 0.03, pop(lf, 10, 14))
        card(ctx, 'p6', f, 0, 880 + 30)
        return
    # dad faceplants on the horn; then the car reverses home and the kid starts again
    fp = eout(pop(lf, honk - 8, honk))
    dad = dad_drive(torso=lerp(4, 30, fp), head=lerp(0, 14, fp), eye='closed' if lf >= honk else 'shock', mouth='wavy' if lf >= honk else 'open',
                    rsh=lerp(74, 20, fp), rel=lerp(-24, -10, fp), lsh=lerp(78, 20, fp), lel=lerp(-30, -10, fp))
    leave = 120
    sc = sc_end + (0 if lf < leave else -((lf - leave) ** 2) * 1.6)
    boy = kid_sit(eye='happy', mouth='grin' if lf < leave + 20 else 'open', rsh=150 if lf >= leave + 20 else 40, rel=-30 if lf >= leave + 20 else -60)
    horn = pop(lf, honk, honk + 10) if honk <= lf < honk + 40 else 0
    z = kf(lf, [(56, 1.5), (honk, 1.5), (honk + 4, 1.25), (leave, 1.0), (170, 0.95)], eout)
    cx = kf(lf, [(56, 760), (honk + 4, 720), (leave, 560)], eout)
    ctx.save(); cam(ctx, cx, kf(lf, [(56, 1100), (leave, 1120)], eout), z, 0, shake_at(lf, [honk], 14, 24), f)
    car_scene(ctx, f, sc, 0.3, moving=lf >= leave, dad=dad, boy=boy, houses=houses, signs=signs, horn=horn)
    ctx.restore()
    if honk <= lf < leave:
        label(ctx, "*HOOOONK*", 540, 1440, 130, hx('ffe14d'), -0.05, pop(lf, honk, honk + 4))
    elif lf >= leave + 20:
        label(ctx, "ARE WE HOME YET?", 540, 1440, 100, hx('ffe14d'), 0.03, pop(lf, leave + 20, leave + 24))
    if lf >= honk + 30:
        card(ctx, 'p7', f, 880 + honk + 30)


SHOTS = [(0, s1), (100, s2), (220, s3), (400, s4), (540, s5), (720, s6), (880, s7)]


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.25)
    ctx.set_source(g); ctx.paint()
    for c in (100, 140, 160, 180, 200, 220, 280, 340, 400, 466, 540, 720, 820, 880, 936):
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.5 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/v{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/roadtrip_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
