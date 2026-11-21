"""'Brain Freeze' - the slushie lesson. Original, general-audience comedy short, 22s.
Hook: kid ECU, head turning to ice from the top down + caption 'Every kid with a SLUSHIE:' "BRAIN... FREEZE!!".
Beat 1: hot backyard, Dad on a lawn chair "Sip it SLOWLY, buddy." kid "Okay!" -> *SLUUURP* whole cup ->
        ECU ice sweeps down *CRACKLE* -> kid frozen inside an ice block, Dad knocks *CLINK* "...told you."
Beat 2: Mom thaws him with a hair dryer *WHIRRR* -> kid pops out "AGAIN!!" -> SLUSHIE #2 frozen, SLUSHIE #3 frozen + penguin,
        split: Mom "...AGAIN?!" / frozen kid "WORTH IT!"
Twist:  Dad low angle "Amateurs. Watch a PRO." chugs a MEGA cup *GLUG GLUG* "See? NOTHING." -> Dad ECU freezes "...uh-oh."
End:    Dad is an ice statue with his own snow cloud + bird on his head, Mom + kid with hair dryers,
        kid: "Sip it SLOWLY, Dad." -> kid *SLUUURP* -> loop to the hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import sweat, twitch
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


DAD = dict(doodle.DAD, shirt=hx('ff8a1f'), pants=hx('3d5aff'))
BOY = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff3b5c'), pants=hx('2a3a6a'))
MOM = dict(doodle.MOM_G, shirt=hx('22b45a'), pants=hx('3d5a9e'))
ICEC = dict(skin=hx('aee8ff'), hair=hx('5ab8ea'), shirt=hx('d6f4ff'), pants=hx('8fd6f5'), shoes=hx('7ac0e8'))
BOY_I = dict(BOY, **ICEC)
DAD_I = dict(DAD, **ICEC)
N = 660
RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); TEAL = hx('19b5a5'); WHITE = (1, 1, 1)
CYAN = hx('7fe3ff'); SLUSH = hx('2fa8ff'); SLUSH_R = hx('ff3b6e')
FLOOR = 1500
KK, DK, MK = 0.95, 1.4, 1.35

CAPS = {
    'p1': [[("Every ", OUT), ("KID", RED), (" with a", OUT)], [("SLUSHIE:", BLUE)]],
}
scenes13.CAPS = CAPS
card = _card13
SIT = dict(lhip=-80, lkn=80, rhip=-80, rkn=80)


# ------------------------------------------------------------------ props
def slushie(ctx, x, y, s=1.0, level=1.0, a=0.0, col=SLUSH, straw=True):
    """giant slushie cup; (x, y) = where the hand grips"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    body = [(-70, -130), (70, -130), (52, 100), (-52, 100)]
    poly(ctx, body); setc(ctx, (0.93, 0.97, 1.0)); ctx.fill()
    if level > 0:
        ctx.save(); poly(ctx, body); ctx.clip()
        top = 100 - 230 * level
        ctx.rectangle(-80, top, 160, 240); setc(ctx, col); ctx.fill()
        rnd = random.Random(5)
        for k in range(14):
            yy = rnd.uniform(-125, 95)
            if yy > top + 8:
                ellipse(ctx, rnd.uniform(-55, 55), yy, 7, 5); setc(ctx, (1, 1, 1, 0.45)); ctx.fill()
        ctx.restore()
    rect_r(ctx, -40, -100, 14, 170, 7); setc(ctx, (1, 1, 1, 0.55)); ctx.fill()
    poly(ctx, body); ink(ctx, 7); ctx.stroke()
    # dome lid
    ctx.new_path(); ctx.move_to(-78, -128); ctx.curve_to(-70, -200, 70, -200, 78, -128); ctx.close_path()
    setc(ctx, (0.9, 0.96, 1.0, 0.8)); ctx.fill_preserve(); ink(ctx, 6); ctx.stroke()
    rect_r(ctx, -82, -138, 164, 18, 9); fl(ctx, WHITE, 5)
    if straw:
        ctx.save(); ctx.translate(10, -180); ctx.rotate(0.18)
        rect_r(ctx, -10, -150, 20, 170, 6); fl(ctx, WHITE, 5)
        for k in range(5):
            ctx.rectangle(-8, -140 + k * 34, 16, 14); setc(ctx, RED); ctx.fill()
        ctx.restore()
    ctx.restore()


def ice_block(ctx, x0, y0, w, h, crack=0.0, a=0.62):
    rect_r(ctx, x0, y0, w, h, 26); setc(ctx, (0.6, 0.9, 1.0, a)); ctx.fill_preserve()
    setc(ctx, hx('3a9fd8')); ctx.set_line_width(9); ctx.stroke()
    for k, (u, v, l) in enumerate(((0.12, 0.1, 0.5), (0.22, 0.08, 0.25), (0.8, 0.6, 0.3))):
        ctx.move_to(x0 + w * u, y0 + h * v); ctx.line_to(x0 + w * u + 40, y0 + h * (v + l))
        setc(ctx, (1, 1, 1, 0.75)); ctx.set_line_width(16 if k == 0 else 10); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    if crack > 0:
        cx, cy = x0 + w * 0.6, y0 + h * 0.3
        rnd = random.Random(9)
        for k in range(5):
            ang = k * 1.25 + 0.3; px, py = cx, cy
            ctx.move_to(px, py)
            for j in range(3):
                px += math.cos(ang + rnd.uniform(-0.5, 0.5)) * 50 * crack; py += math.sin(ang + rnd.uniform(-0.5, 0.5)) * 50 * crack
                ctx.line_to(px, py)
        setc(ctx, (1, 1, 1, 0.9)); ctx.set_line_width(5); ctx.stroke()


def frost_face(ctx, ch, chi, p, pi_, cx, cy, R, rot, lev, lf):
    """face that turns to ice from the top; lev 0..1 = how far down the ice has spread"""
    face(ctx, ch, p, cx, cy, R, rot)
    if lev <= 0:
        return
    top, bot = cy - 1.45 * R, cy + 1.25 * R
    yl = lerp(top, bot, lev)
    ctx.save()
    ctx.new_path(); ctx.move_to(cx - 2 * R, top - 400)
    ctx.line_to(cx + 2 * R, top - 400); ctx.line_to(cx + 2 * R, yl)
    nn = 12
    for k in range(nn, -1, -1):
        xx = cx - 2 * R + 4 * R * k / nn
        ctx.line_to(xx, yl + (0.09 * R if k % 2 else -0.02 * R))
    ctx.close_path(); ctx.clip()
    face(ctx, chi, pi_, cx, cy, R, rot)
    ctx.restore()
    # icicles + frost sparkle along the edge
    if lev < 0.98:
        for k in range(7):
            xx = cx - 1.0 * R + 2.0 * R * k / 6
            ln = (0.1 + 0.07 * ((k * 37) % 3)) * R
            poly(ctx, [(xx - 0.05 * R, yl), (xx + 0.05 * R, yl), (xx, yl + ln)]); fl(ctx, hx('dff6ff'), max(3, R * 0.012))
    rnd = random.Random(int(cx) + 3)
    for k in range(9):
        sx, sy = cx + rnd.uniform(-1.1, 1.1) * R, rnd.uniform(top + 0.3 * R, yl)
        if sy < yl:
            sparkle(ctx, sx, sy, (0.05 + 0.02 * math.sin(lf * 0.6 + k)) * R, col=WHITE)


def flakes(ctx, lf, x0, x1, y0, y1, n=40, seed=1, s=1.0):
    rnd = random.Random(seed)
    for k in range(n):
        x = rnd.uniform(x0, x1) + 20 * math.sin(lf * 0.1 + k)
        y = y0 + ((rnd.uniform(0, 1) * (y1 - y0) + lf * rnd.uniform(4, 9)) % (y1 - y0))
        r = rnd.uniform(6, 13) * s
        ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()


def hair_dryer(ctx, x, y, s=1.0, a=0.0, lf=0, on=True, col=PINK):
    """(x, y) = handle grip; points to +x (rotated by a)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -26, -20, 52, 130, 20); fl(ctx, dark(col, 0.8), 6)
    ellipse(ctx, 0, -60, 80, 62); fl(ctx, col, 7)
    rect_r(ctx, 40, -94, 120, 68, 18); fl(ctx, col, 7)
    ellipse(ctx, 0, -60, 30, 24); fl(ctx, WHITE, 5)
    if on:
        for k in range(3):
            yy = -78 + k * 18
            ctx.move_to(180, yy)
            for j in range(6):
                ctx.line_to(200 + j * 40, yy + (14 if (j + k + lf // 2) % 2 else -14))
        setc(ctx, (1, 0.6, 0.2, 0.85)); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()


def penguin(ctx, x, ground, s=1.0, lf=0):
    ctx.save(); ctx.translate(x, ground); ctx.scale(s, s); ctx.rotate(0.08 * math.sin(lf * 0.4))
    ellipse(ctx, 0, -110, 75, 110); fl(ctx, hx('1d1a2e'), 7)
    ellipse(ctx, 0, -95, 50, 85); setc(ctx, WHITE); ctx.fill()
    for sx in (-1, 1):
        ellipse(ctx, sx * 22, -165, 13, 15); fl(ctx, WHITE, 4)
        ellipse(ctx, sx * 22 + 3, -162, 6, 7); setc(ctx, INK); ctx.fill()
        ellipse(ctx, sx * 30, 0, 28, 12); fl(ctx, ORANGE, 5)
    poly(ctx, [(-16, -140), (16, -140), (0, -112)]); fl(ctx, ORANGE, 5)
    ctx.restore()


def bird(ctx, x, y, s=1.0, lf=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 46, 38); fl(ctx, GOLD, 6)
    ellipse(ctx, 16, -8, 7, 8); setc(ctx, INK); ctx.fill()
    poly(ctx, [(40, -4), (66, 4), (40, 12)]); fl(ctx, ORANGE, 5)
    ctx.move_to(-10, 0); ctx.line_to(-40, -14 - 10 * math.sin(lf * 0.8)); ctx.line_to(-30, 14); ctx.close_path(); fl(ctx, dark(GOLD, 0.85), 5)
    ctx.restore()


def cloud(ctx, x, y, s=1.0, col=hx('c9d6e8')):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for dx, dy, r in ((-90, 10, 60), (-20, -30, 80), (70, 0, 66), (10, 30, 70)):
        ctx.new_path(); ctx.arc(dx, dy, r, 0, 2 * math.pi); fl(ctx, col, 6)
    for dx, dy, r in ((-90, 10, 54), (-20, -30, 74), (70, 0, 60), (10, 30, 64)):
        ctx.new_path(); ctx.arc(dx, dy, r, 0, 2 * math.pi); setc(ctx, col); ctx.fill()
    ctx.restore()


def backyard(ctx, lf, sun=True, sky=hx('8fd8ff'), grass=hx('6fd36a')):
    ctx.rectangle(-2000, -2000, 5000, 5000); setc(ctx, sky); ctx.fill()
    if sun:
        rays(ctx, 880, 380, 120, 420, lf * 0.02, col=(1, 0.95, 0.5), a=0.6, n=14)
        ctx.new_path(); ctx.arc(880, 380, 110, 0, 2 * math.pi); fl(ctx, hx('ffd23f'), 8)
    # fence
    for k in range(-12, 22):
        x = k * 110
        poly(ctx, [(x, 1500), (x, 1060), (x + 45, 1020), (x + 90, 1060), (x + 90, 1500)]); fl(ctx, hx('fff1dc'), 6)
    ctx.rectangle(-2000, 1130, 5000, 30); fl(ctx, hx('f0dcc0'), 5)
    ctx.rectangle(-2000, 1300, 5000, 30); fl(ctx, hx('f0dcc0'), 5)
    ctx.rectangle(-2000, FLOOR - 40, 5000, 2000); setc(ctx, grass); ctx.fill()
    ctx.move_to(-2000, FLOOR - 40); ctx.line_to(3000, FLOOR - 40); ink(ctx, 7); ctx.stroke()
    for k in range(-10, 30):
        x = k * 90 + 30
        ctx.move_to(x, FLOOR + 60); ctx.line_to(x + 10, FLOOR + 30); ctx.move_to(x + 18, FLOOR + 60); ctx.line_to(x + 22, FLOOR + 26)
    setc(ctx, dark(grass, 0.8)); ctx.set_line_width(5); ctx.stroke()


def lawn_chair(ctx, x, seat, s=1.0):
    ctx.save(); ctx.translate(x, seat); ctx.scale(s, s)
    ctx.move_to(-90, 0); ctx.line_to(-120, 120); ctx.move_to(90, 0); ctx.line_to(120, 120)
    ctx.move_to(-90, 0); ctx.line_to(-110, -190)
    ink(ctx, 14); ctx.stroke()
    poly(ctx, [(-110, -190), (-60, -190), (-40, 0), (-90, 0)]); fl(ctx, hx('19b5a5'), 6)
    rect_r(ctx, -100, -16, 200, 32, 12); fl(ctx, hx('19b5a5'), 6)
    ctx.restore()


# ------------------------------------------------------------------ close-ups
def kid_freeze_ecu(ctx, f, lf, lev, bg=CYAN, z0=1.0, shake=0, eye='shock', mouth='wavy', cup=True):
    ctx.save(); cam(ctx, 540, 960, z0, 0, shake, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    rays(ctx, 540, 900, 260, 1420, lf * 0.03, col=(1, 1, 1), a=0.25, n=18)
    flakes(ctx, lf, -100, 1180, -100, 2000, 30, 4, 1.4)
    cx, cy, R = 540, 900, 300
    rot = 0.025 * math.sin(lf * 2.1) * (1 if lev > 0.3 else 0)
    pp = P(eye=eye, mouth=mouth)
    frost_face(ctx, BOY, BOY_I, pp, pp, cx, cy, R, rot, lev, lf)
    if cup:
        slushie(ctx, 830, 1380, 1.5, 0.15, -0.15, SLUSH, straw=True)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    lev = lerp(0.72, 1.0, eout(pop(lf, 0, 14)))
    kid_freeze_ecu(ctx, f, lf, lev, z0=1.02 + 0.06 * eio(pop(lf, 0, 54)), shake=6 if lf < 12 else 2)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"BRAIN...", "FREEZE!!\"", WHITE, t, 120, col2=CYAN, y=1400)


# ------------------------------------------------------------------ shots
def yard_wide(ctx, f, lf, dad_p, kid_p, kid_level=1.0, kid_frozen=False, z=1.0, cx=540, cy=960, shake=0, extra=None, dad_x=290, kid_x=760,
              block=None, kid_cup=True):
    ctx.save(); cam(ctx, cx, cy, z, 0, shake, f)
    backyard(ctx, lf)
    lawn_chair(ctx, dad_x, FLOOR - 150, 1.2)
    draw_hip(ctx, dad_x, FLOOR - 170, DK, 1, DAD, dict(dad_p, **SIT))
    ch = BOY_I if kid_frozen else BOY
    b = draw(ctx, kid_x, FLOOR - 186 * KK, KK, -1, ch, kid_p)
    if kid_cup:
        slushie(ctx, b['front'][0], b['front'][1], 0.9, kid_level, 0.0, SLUSH)
    if block is not None:
        h, crack = block
        ice_block(ctx, kid_x - 150, FLOOR + 20 - h, 300, h, crack)
    if extra:
        extra(ctx)
    ctx.restore()
    return b


def s2(ctx, f):
    lf = f - 54
    if lf < 50:
        talk = lf < 30
        yard_wide(ctx, f, lf, P(eye='smug', mouth='open' if talk and (lf // 4) % 2 else 'smile', rsh=-60, rel=-40, lsh=10),
                  P(eye='happy', mouth='grin', rsh=-50, rel=-70, lsh=20), z=1.25 + 0.05 * eio(pop(lf, 0, 50)), cx=580, cy=1220, dad_x=360, kid_x=760)
        sweat(ctx, 380, 380, lf, 1.3)
        label2(ctx, "\"Sip it SLOWLY,", "buddy.\"", WHITE, pop(lf, 2, 6), 100, col2=YEL, y=1400) if lf < 32 else \
            label(ctx, "\"Okay!\"", 640, 1420, 120, GREEN, -0.04, pop(lf, 32, 35))
    elif lf < 80:
        il = lf - 50
        level = 1 - eio(pop(il, 4, 26))
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.12 * eio(pop(il, 0, 30)), 0, 6 if il >= 4 else 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd86b')); ctx.fill()
        rays(ctx, 540, 900, 260, 1420, il * 0.08, col=(1, 1, 1), a=0.3, n=18)
        face(ctx, BOY, P(eye='closed', mouth='open'), 470, 820, 270, -0.05)
        slushie(ctx, 640, 1330, 1.7, level, -0.18, SLUSH)
        ctx.restore()
        label(ctx, "*SLUUUUURP!*", 540, 1420, 120, SLUSH, -0.05, pop(il, 4, 7))
    elif lf < 116:
        il = lf - 80
        lev = eio(pop(il, 3, 22))
        kid_freeze_ecu(ctx, f, il, lev, bg=hx('b8f0ff'), z0=1.0 + 0.1 * eio(pop(il, 0, 30)), shake=shake_at(il, [3, 22], 10, 16),
                       eye='normal' if il < 8 else 'shock', mouth='smile' if il < 8 else 'wavy', cup=False)
        if il >= 6:
            label(ctx, "*CRACKLE*", 540, 330, 100, WHITE, 0.05, pop(il, 6, 9))
        if il >= 22:
            label2(ctx, "\"BRAIN...", "FREEZE!!\"", WHITE, pop(il, 22, 25), 120, col2=CYAN, y=1400)
    else:
        il = lf - 116
        knock = il >= 16
        yard_wide(ctx, f, il, P(eye='smug', mouth='smile', rsh=-120 if knock else 10, rel=-40 if knock else 0, lsh=10, torso=10 if knock else 0),
                  P(eye='shock', mouth='wavy', rsh=-50, rel=-70, lsh=20), kid_level=0.0, kid_frozen=True,
                  z=1.3, cx=580, cy=1220, shake=shake_at(il, [0, 18, 24], 8, 14), block=(560, 0.6 * eio(pop(il, 18, 26))), dad_x=360, kid_x=760)
        label(ctx, "*FROZEN*", 540, 330, 110, CYAN, -0.05, pop(il, 0, 3) if il < 18 else 0)
        if il >= 18:
            label(ctx, "*CLINK* *CLINK*", 540, 330, 80, WHITE, 0.04, pop(il, 18, 21))
        if il >= 24:
            label(ctx, "\"...told you.\"", 540, 1420, 110, YEL, -0.04, pop(il, 24, 28))


def mom_thaw(ctx, f, il):
    """Mom melts the ice block with a hair dryer, kid pops out"""
    melt = eio(pop(il, 2, 26))
    out_ = il >= 26
    ctx.save(); cam(ctx, 540, 1220, 1.28, 0, shake_at(il, [26], 10, 14), f)
    backyard(ctx, il)
    # puddle
    ellipse(ctx, 740, FLOOR + 30, 120 + 200 * melt, 30 + 20 * melt); setc(ctx, (0.55, 0.85, 1.0, 0.8)); ctx.fill()
    bm = draw(ctx, 280, FLOOR - 186 * MK, MK, 1, MOM, P(eye='glare' if not out_ else 'shock', mouth='flat', rsh=-80, rel=0, lsh=10))
    hair_dryer(ctx, bm['front'][0], bm['front'][1], 0.9, 0.0, il, on=not out_)
    if not out_:
        draw(ctx, 740, FLOOR - 186 * KK, KK, -1, BOY_I, P(eye='shock', mouth='wavy', rsh=-50, rel=-70, lsh=20))
        h = lerp(560, 120, melt)
        ice_block(ctx, 740 - 175, FLOOR + 20 - h, 350, h, 0.4)
        for k in range(4):
            yy = FLOOR + 20 - h + ((il * 8 + k * 40) % 120)
            ellipse(ctx, 590 + k * 100, yy, 10, 16); fl(ctx, hx('8fd8ff'), 4)
    else:
        hop = 160 * math.sin(math.pi * pop(il, 26, 40))
        draw(ctx, 740, FLOOR - 186 * KK - hop, KK, -1, BOY, P(eye='happy', mouth='grin', lsh=160, rsh=-160, lel=20, rel=-20))
    ctx.restore()
    if not out_:
        label(ctx, "*WHIRRRR*", 540, 330, 100, ORANGE, -0.05, pop(il, 2, 5))
    else:
        label2(ctx, "\"AGAIN!!\"", "", WHITE, pop(il, 28, 31), 140, y=1400)


def montage(ctx, f, il, k):
    """SLUSHIE #2 / #3: kid frozen mid-pose in a block"""
    bg = [hx('ffb3d1'), hx('d6c2ff')][k]
    ctx.save(); cam(ctx, 560, 1200, 1.35 + 0.06 * eio(pop(il, 0, 18)), [-4, 4][k], shake_at(il, [0], 8, 16), f)
    backyard(ctx, il, sky=bg)
    poses = [P(eye='happy', mouth='grin', lsh=160, rsh=-160, lel=20, rel=-20, rhip=-30, rkn=40),
             P(eye='shock', mouth='open', lsh=40, rsh=-120, rel=-60, torso=-10)]
    b = draw(ctx, 540, FLOOR - 186 * KK - (60 if k == 0 else 0), KK, -1 if k else 1, BOY_I, poses[k])
    slushie(ctx, b['front'][0], b['front'][1], 0.9, 0.0, 0.3 if k == 0 else 0, [SLUSH_R, hx('22c55a')][k])
    ice_block(ctx, 300, FLOOR + 20 - 600, 480, 600, 0.3)
    if k == 1:
        penguin(ctx, 870, FLOOR + 10, 1.1, il)
        flakes(ctx, il, 0, 1080, 200, 1600, 30, 7)
    ctx.restore()
    label(ctx, f"SLUSHIE #{k + 2}", 540, 330, 110, [PINK, PURPLE][k], (-1) ** k * 0.05, pop(il, 0, 3))
    label(ctx, "*FREEZE!*", 540, 1420, 110, CYAN, 0.04, pop(il, 2, 5))


def split(ctx, f, il):
    ctx.save(); ctx.rectangle(0, 0, W, H / 2); ctx.clip()
    ctx.translate(0, -360)
    ctx.save(); cam(ctx, 540, 960, 0.85, 0, 2, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb36b')); ctx.fill()
    rays(ctx, 540, 900, 260, 1420, il * 0.03, col=(1, 1, 1), a=0.2, n=18)
    face(ctx, MOM, P(eye='glare', mouth='flat'), 540, 880, 300, 0.02 * math.sin(il * 0.5))
    twitch(ctx, 540 + 0.55 * 300, 880 - 0.7 * 300, il, 1.3)
    hair_dryer(ctx, 760, 1180, 1.1, -0.4, il, on=True)
    ctx.restore()
    ctx.restore()
    ctx.save(); ctx.rectangle(0, H / 2, W, H / 2); ctx.clip()
    ctx.translate(0, 330)
    kid_freeze_ecu(ctx, f, il, 1.0, bg=CYAN, z0=0.8, eye='happy', mouth='grin', cup=False)
    ctx.restore()
    ctx.rectangle(0, H / 2 - 8, W, 16); setc(ctx, OUT); ctx.fill()
    label(ctx, "\"...AGAIN?!\"", 540, 330, 110, WHITE, -0.04, pop(il, 2, 6))
    label(ctx, "\"WORTH IT!!\"", 540, 1460, 110, CYAN, 0.03, pop(il, 16, 20))


def s3(ctx, f):
    lf = f - 210
    if lf < 46:
        mom_thaw(ctx, f, lf)
    elif lf < 64:
        montage(ctx, f, lf - 46, 0)
    elif lf < 82:
        montage(ctx, f, lf - 64, 1)
    else:
        split(ctx, f, lf - 82)


def mega_cup(ctx, x, y, level, a=0.0, s=1.7):
    slushie(ctx, x, y, s, level, a, SLUSH_R)
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    text(ctx, "XXL", 0, 10, 44, WHITE, ow=6, ang=0)
    ctx.restore()


def s4(ctx, f):
    lf = f - 330
    if lf < 46:
        # low angle: Dad stands up with the MEGA cup
        ctx.save(); cam(ctx, 540, 1080, 1.05 + 0.05 * eio(pop(lf, 0, 46)), -3, shake_at(lf, [20], 8, 12), f)
        backyard(ctx, lf, sky=hx('7fc8ff'))
        b = draw(ctx, 540, FLOOR - 186 * 1.9, 1.9, 1, DAD, P(eye='smug', mouth='grin', rsh=-70, rel=-50, lsh=150 if lf < 20 else 20, lel=20))
        mega_cup(ctx, b['front'][0], b['front'][1], 1.0, 0.0)
        ctx.restore()
        label2(ctx, "\"Amateurs.", "Watch a PRO.\"", WHITE, pop(lf, 3, 7), 110, col2=ORANGE, y=1400)
        if lf >= 20:
            label(ctx, "*MEGA SIZE*", 540, 330, 100, RED, -0.05, pop(lf, 20, 23))
    elif lf < 80:
        il = lf - 46
        level = 1 - eio(pop(il, 4, 30))
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.1 * eio(pop(il, 0, 34)), 0, 5 if il >= 4 else 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff9a5a')); ctx.fill()
        rays(ctx, 540, 900, 260, 1420, il * 0.08, col=(1, 1, 1), a=0.3, n=18)
        face(ctx, DAD, P(eye='closed', mouth='open'), 500, 1060, 280, -0.35)
        mega_cup(ctx, 640, 560, level, 2.6, 1.6)
        ctx.restore()
        label(ctx, "*GLUG! GLUG! GLUG!*", 540, 1420, 100, YEL, -0.05, pop(il, 4, 7))
    elif lf < 110:
        il = lf - 80
        ctx.save(); cam(ctx, 560, 1240, 1.35, 0, 0, f)
        backyard(ctx, il)
        b = draw(ctx, 380, FLOOR - 186 * DK, DK, 1, DAD, P(eye='smug', mouth='grin', rsh=80, rel=-70, lsh=10))
        mega_cup(ctx, b['front'][0], b['front'][1], 0.0, 0.4, 1.0)
        draw(ctx, 860, FLOOR - 186 * MK, MK, -1, MOM, P(eye='glare', mouth='flat', lsh=30, rsh=-30))
        draw(ctx, 690, FLOOR - 186 * KK, KK, -1, BOY, P(eye='shock', mouth='open', lsh=10, rsh=-10))
        ctx.restore()
        label2(ctx, "\"See?", "NOTHING.\"", WHITE, pop(il, 2, 6), 120, col2=GREEN, y=1400)
    else:
        il = lf - 110   # 0..40
        lev = eio(pop(il, 6, 34))
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.12 * eio(pop(il, 0, 40)), 0, 2 + shake_at(il, [12, 24], 8, 10), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('b8f0ff') if il > 10 else hx('ffd86b')); ctx.fill()
        rays(ctx, 540, 900, 260, 1420, il * 0.03, col=(1, 1, 1), a=0.25, n=18)
        pp = P(eye='smug' if il < 10 else 'shock', mouth='grin' if il < 10 else 'wavy')
        frost_face(ctx, DAD, DAD_I, pp, pp, 540, 880, 300, 0, lev, il)
        if il > 10:
            sweat(ctx, 540 + 0.85 * 300, 880 - 0.2 * 300, il, 1.2)
        ctx.restore()
        if il >= 6:
            label(ctx, "*crk... crk...*", 540, 330, 90, WHITE, 0.05, pop(il, 6, 9))
        if il >= 18:
            label(ctx, "\"...uh-oh.\"", 540, 1420, 130, YEL, -0.04, pop(il, 18, 22))


def statue_scene(ctx, f, il, z, cx, cy, kid_talk=False, dryers=False, shake=0):
    ctx.save(); cam(ctx, cx, cy, z, 0, shake, f)
    backyard(ctx, il)
    # Dad's own private snow cloud
    cloud(ctx, 400, 360 + 8 * math.sin(il * 0.2), 1.3)
    ctx.save(); ctx.rectangle(160, 420, 480, FLOOR - 420); ctx.clip(); flakes(ctx, il, 180, 620, 400, FLOOR, 40, 3); ctx.restore()
    b = draw(ctx, 400, FLOOR - 186 * DK, DK, 1, DAD_I, P(eye='shock', mouth='wavy', rsh=80, rel=-70, lsh=10, head=-6))
    mega_cup(ctx, b['front'][0], b['front'][1], 0.0, 0.4, 1.0)
    ellipse(ctx, 400, FLOOR + 10, 230, 30); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()   # snow pile
    land = eout(pop(il, 14, 26))
    bird(ctx, lerp(1100, b['head'][0] + 10, land), lerp(300, b['head'][1] - b['R'] - 30, land) - 60 * math.sin(math.pi * land), 1.0, il)
    if dryers:
        bm = draw(ctx, 880, FLOOR - 186 * MK, MK, -1, MOM, P(eye='glare', mouth='flat', rsh=-80, rel=0, lsh=10))
        hair_dryer(ctx, bm['front'][0], bm['front'][1], 0.9, math.pi, il, on=True)
        bk = draw(ctx, 690, FLOOR - 186 * KK, KK, -1, BOY, P(eye='smug', mouth='smile' if not kid_talk else ('open' if (il // 4) % 2 else 'smile'),
                                                             rsh=-80, rel=0, lsh=10))
        hair_dryer(ctx, bk['front'][0], bk['front'][1], 0.65, math.pi, il, on=True, col=GOLD)
    ctx.restore()


def s5(ctx, f):
    lf = f - 480
    if lf < 56:
        statue_scene(ctx, f, lf, 1.2 + 0.06 * eio(pop(lf, 0, 56)), 440, 1120, shake=shake_at(lf, [0], 10, 18))
        label(ctx, "*FREEZE!!*", 540, 330, 120, CYAN, -0.05, pop(lf, 0, 3))
        if lf >= 26:
            label(ctx, "*tweet*", 640, 1420, 100, GOLD, 0.05, pop(lf, 26, 29))
    elif lf < 116:
        il = lf - 56
        statue_scene(ctx, f, il + 56, 1.25, 580, 1180, kid_talk=il >= 18, dryers=True)
        label(ctx, "*WHIRRRR*", 540, 330, 100, ORANGE, -0.05, pop(il, 0, 3))
        if il >= 18:
            label2(ctx, "\"Sip it SLOWLY,", "Dad.\"", WHITE, pop(il, 18, 22), 104, col2=YEL, y=1400)
    elif lf < 132:
        il = lf - 116
        ctx.save(); cam(ctx, 540, 960, 1.05 + 0.08 * eio(pop(il, 0, 16)), 0, 6, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd86b')); ctx.fill()
        rays(ctx, 540, 900, 260, 1420, il * 0.08, col=(1, 1, 1), a=0.3, n=18)
        face(ctx, BOY, P(eye='closed', mouth='open'), 470, 820, 270, -0.05)
        slushie(ctx, 640, 1330, 1.7, 1 - eio(pop(il, 0, 14)), -0.18, SLUSH)
        ctx.restore()
        label(ctx, "*SLUUUUURP!*", 540, 1420, 120, SLUSH, -0.05, pop(il, 0, 3))
    else:
        s1(ctx, f, f - 612)


SHOTS = [(0, s1), (54, s2), (210, s3), (330, s4), (480, s5)]
CUTS = (54, 104, 134, 170, 210, 256, 274, 292, 330, 376, 410, 440, 480, 536, 596, 612)


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
                              "-i", "out/brain_freeze_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
