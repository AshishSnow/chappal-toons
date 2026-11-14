"""'Dad's Home Haircut' - original, general-audience comedy short, ~22s.
Mirror ECU: kid stares at a bald stripe down the middle of his hair. 5 minutes earlier: Dad with clippers, "I watched ONE video".
Beat 1: the first "little trim" - clippers plough a runway through the hair. Dad: "...oops."
Beat 2: "I'll even it out" - whirlwind montage, hair everywhere, kid ends up with 3 hairs. "...Nailed it."
Beat 3: Mom walks in, mug shatters. Split screen: Dad: "HE MOVED."
Twist: that night the kid tiptoes to sleeping Dad with the clippers. Morning: Dad in the mirror with the same stripe. Loops."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
import scenes13
from scenes13 import card as _card13
import random

BOY = doodle.BOY
BALD = dict(doodle.BOY, hairstyle='uncle')
DAD = doodle.DAD
MOM = doodle.MOM_G
N = 660
FLOOR = 1430
RED = hx('ff3b5c')
BLUE = hx('1f8bff')

CAPS = {
    'p1': [[("WHEN DAD SAYS", OUT)], [("\"I'LL CUT IT MYSELF\"", RED)]],
    'p2': [[("THE FIRST", OUT)], [("\"LITTLE TRIM\"", BLUE)]],
    'p3': [[("THEN HE TRIES TO", OUT)], [("EVEN IT OUT", hx('ff8a1f'))]],
    'p4': [[("THEN MOM", OUT)], [("WALKS IN", hx('8a3cff'))]],
    'p5': [[("THAT NIGHT...", OUT)], [("PAYBACK TIME", RED)]],
}
scenes13.CAPS = CAPS
card = _card13


def label(ctx, s, x, y, size, col, ang=0, t=1.0):
    if t <= 0:
        return
    sc = 0.5 + 0.5 * eout(min(1, t * 2)) + 0.08 * math.sin(min(1, t) * math.pi)
    ctx.save(); ctx.translate(x, y); ctx.scale(sc, sc)
    text(ctx, s, 0, 0, size, col, ang=ang, ow=12, maxw=860)
    ctx.restore()


def cam(ctx, cx, cy, z, rot=0, shake=0, f=0, sx=W / 2, sy=H / 2):
    rnd = random.Random(f * 31 + 7)
    dx, dy = (rnd.uniform(-1, 1) * shake, rnd.uniform(-1, 1) * shake) if shake else (0, 0)
    ctx.translate(sx + dx, sy + dy); ctx.rotate(math.radians(rot)); ctx.scale(z, z); ctx.translate(-cx, -cy)


def rect_r(ctx, x, y, w, h, r):
    ctx.new_path(); ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); ctx.close_path()


def rays(ctx, x, y, r0, r1, t, col=(1, 0.97, 0.6), a=0.8, n=12):
    for k in range(n):
        ang = k * 2 * math.pi / n + t
        ctx.move_to(x + math.cos(ang) * r0, y + math.sin(ang) * r0)
        ctx.line_to(x + math.cos(ang - 0.09) * r1, y + math.sin(ang - 0.09) * r1)
        ctx.line_to(x + math.cos(ang + 0.09) * r1, y + math.sin(ang + 0.09) * r1); ctx.close_path()
    setc(ctx, col + (a,)); ctx.fill()


_SCR = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4))


def face(ctx, ch, p, cx, cy, Rt, rot=0.0, f_=1, head_only=False):
    b = draw_hip(_SCR, 0, 0, 1, f_, ch, p)
    hd, R = b['head'], b['R']
    s = Rt / R
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot)
    if head_only:
        ctx.rectangle(-4 * Rt, -4 * Rt, 8 * Rt, 4.9 * Rt); ctx.clip()
    ctx.scale(s, s); ctx.translate(-hd[0], -hd[1])
    draw_hip(ctx, 0, 0, 1, f_, ch, p)
    ctx.restore()


def talk(lf, a='open', b='scream', rate=4):
    return a if (lf // rate) % 2 == 0 else b


# ------------------------------------------------------------------ haircut helpers
def scalp(ctx, cx, cy, Rt, f_, rot, patches, top=-1.3, skin=None, ch=BOY):
    """paint bald patches (x0, x1, ybottom) in head-R units over the hair of a face() drawn at (cx, cy, Rt)"""
    skin = skin or ch['skin']
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(Rt * f_, Rt)
    ctx.new_path(); ctx.save(); ctx.translate(0, -0.12); ctx.scale(1.0, 1.02); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    ctx.clip()
    for x0, x1, yb, *rest in patches:
        yt = rest[0] if rest else top
        rect_r(ctx, x0, yt, x1 - x0, yb - yt, min(0.1, (x1 - x0) / 2.2))
        setc(ctx, light(skin, 0.12)); ctx.fill()
        # stubble dots + shine
        rnd = random.Random(int(x0 * 100))
        for _ in range(int((x1 - x0) * 30)):
            ellipse(ctx, rnd.uniform(x0 + 0.04, x1 - 0.04), rnd.uniform(max(yt, -1.1) + 0.05, yb - 0.04), 0.012, 0.012); setc(ctx, dark(skin, 0.7)); ctx.fill()
        ellipse(ctx, (x0 + x1) / 2 - 0.03, max(yt, -1.05) + 0.18, (x1 - x0) * 0.18, 0.08); setc(ctx, (1, 1, 1, 0.55)); ctx.fill()
    # re-ink the dome edge
    ctx.new_path(); ctx.save(); ctx.translate(0, -0.12); ctx.scale(1.0, 1.02); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    setc(ctx, INK); ctx.set_line_width(0.09); ctx.stroke()
    ctx.restore()


def stripe_patch(prog=1.0):
    """central runway; prog grows it from the fringe up to the crown"""
    yt = lerp(-0.42, -1.3, prog)
    return [(-0.22, 0.3, -0.36, yt)]


def head_cut(ctx, stage, cx, cy, Rt, p, rot=0.0, f_=1, prog=1.0, head_only=False):
    """stage 0 full hair, 1 runway, 2 runway + side bite, 3 three hairs left"""
    if stage >= 3:
        face(ctx, BALD, p, cx, cy, Rt, rot, f_, head_only)
        return
    face(ctx, BOY, p, cx, cy, Rt, rot, f_, head_only)
    pts = []
    if stage >= 1:
        pts += stripe_patch(prog if stage == 1 else 1.0)
    if stage >= 2:
        pts += [(-0.95, -0.5, -0.38, -1.3), (0.48, 0.95, -0.3, -0.95)]
    if pts:
        scalp(ctx, cx, cy, Rt, f_, rot, pts)


def clippers(ctx, x, y, a=0.0, s=1.0, lf=0, on=True):
    j = 3 * math.sin(lf * 2.7) if on else 0
    ctx.save(); ctx.translate(x + j, y - j * 0.5); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -46, -40, 92, 190, 40); fl(ctx, hx('3fa9f5'), 7)
    rect_r(ctx, -30, 20, 60, 90, 24); setc(ctx, hx('2a7fd0')); ctx.fill()
    ellipse(ctx, 0, 40, 12, 12); fl(ctx, hx('ffe14d') if on else hx('9aa0b4'), 4)
    rect_r(ctx, -56, -84, 112, 52, 10); fl(ctx, hx('dfe6f2'), 7)
    for k in range(9):
        ctx.move_to(-48 + k * 12, -84); ctx.line_to(-48 + k * 12, -100); ink(ctx, 6); ctx.stroke()
    ctx.move_to(0, 150); ctx.curve_to(10, 220, -40, 260, -20, 340); ink(ctx, 8); ctx.stroke()
    ctx.restore()
    if on:
        for k in range(3):
            r = 70 + k * 22 + (lf % 4) * 4
            ctx.new_path(); ctx.arc(x, y - 30 * s, r * s, -2.4, -0.8); setc(ctx, (1, 1, 1, 0.6 - k * 0.15)); ctx.set_line_width(6); ctx.stroke()


def clump(ctx, x, y, a, s=1.0, col=hx('1c1a2e')):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-30, 0); ctx.curve_to(-20, -26, 20, -26, 34, -6); ctx.curve_to(14, -12, -8, -10, -30, 0); ctx.close_path()
    setc(ctx, col); ctx.fill_preserve(); ink(ctx, 3); ctx.stroke()
    ctx.restore()


def falling_hair(ctx, lf, x0, x1, y0, seed=1, n=10, rate=4, life=40, s=1.0, floor=2200):
    rnd = random.Random(seed)
    for k in range(n):
        st = rnd.uniform(0, rate * n) ; ph = (lf - st) % (rate * n)
        if ph > life or lf < st:
            continue
        t = ph / life
        x = rnd.uniform(x0, x1) + math.sin(t * 6 + k) * 40 + rnd.uniform(-1, 1) * 200 * t
        y = min(floor, y0 + rnd.uniform(-30, 30) + 900 * t * t + 120 * t)
        clump(ctx, x, y, rnd.uniform(0, 6) + t * 4 * rnd.choice((-1, 1)), s * rnd.uniform(0.7, 1.3))


def cape(ctx, x, top, bot, w=560, col=hx('ff4d8d')):
    ctx.new_path(); ctx.move_to(x - 90, top); ctx.curve_to(x - w * 0.45, top + 80, x - w * 0.55, bot - 200, x - w / 2, bot)
    ctx.line_to(x + w / 2, bot); ctx.curve_to(x + w * 0.55, bot - 200, x + w * 0.45, top + 80, x + 90, top); ctx.close_path()
    fl(ctx, col, 10)
    ctx.save(); ctx.new_path(); ctx.move_to(x - 90, top); ctx.curve_to(x - w * 0.45, top + 80, x - w * 0.55, bot - 200, x - w / 2, bot)
    ctx.line_to(x + w / 2, bot); ctx.curve_to(x + w * 0.55, bot - 200, x + w * 0.45, top + 80, x + 90, top); ctx.close_path(); ctx.clip()
    for k in range(-4, 5):
        ctx.move_to(x + k * 70, top); ctx.line_to(x + k * 110, bot); setc(ctx, (1, 1, 1, 0.5)); ctx.set_line_width(16); ctx.stroke()
    ctx.restore()
    rect_r(ctx, x - 110, top - 20, 220, 44, 20); fl(ctx, (1, 1, 1), 7)


def hair_pile(ctx, x, y, h, w=420):
    if h <= 0:
        return
    ctx.new_path(); ctx.move_to(x - w / 2, y); ctx.curve_to(x - w * 0.3, y - h * 1.2, x + w * 0.3, y - h * 1.2, x + w / 2, y); ctx.close_path()
    fl(ctx, hx('1c1a2e'), 8)
    rnd = random.Random(9)
    for k in range(int(h / 8)):
        clump(ctx, x + rnd.uniform(-w * 0.35, w * 0.35), y - rnd.uniform(0, h * 0.8), rnd.uniform(0, 6), 0.8, hx('2e2a48'))


def mug(ctx, x, y, a=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(60, 0, 34, -1.4, 1.4); ink(ctx, 26); ctx.stroke(); ctx.new_path(); ctx.arc(60, 0, 34, -1.4, 1.4); setc(ctx, (1, 1, 1)); ctx.set_line_width(14); ctx.stroke()
    rect_r(ctx, -60, -70, 130, 150, 18); fl(ctx, (1, 1, 1), 7)
    ellipse(ctx, 5, -66, 60, 12); fl(ctx, hx('8a5a30'), 5)
    ellipse(ctx, 5, 10, 22, 22); setc(ctx, RED); ctx.fill()
    ctx.restore()


# ------------------------------------------------------------------ sets
def bathroom(ctx, night=False):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('7fdcd0')); ctx.fill()
    for i in range(-20, 30):
        ctx.move_to(i * 150, -3000); ctx.line_to(i * 150, 4000); setc(ctx, hx('5fc4b8')); ctx.set_line_width(8); ctx.stroke()
        ctx.move_to(-3000, i * 150); ctx.line_to(4000, i * 150); ctx.stroke()


def mirror(ctx, inner):
    """mirror frame centred on screen; inner(ctx) draws the reflection"""
    x, y, w, h = 110, 560, 860, 1000
    rect_r(ctx, x - 30, y - 30, w + 60, h + 60, 90); fl(ctx, hx('ffd23f'), 12)
    ctx.save(); rect_r(ctx, x, y, w, h, 70); ctx.clip()
    ctx.rectangle(x, y, w, h); setc(ctx, hx('cdeeff')); ctx.fill()
    ctx.rectangle(x, y + h * 0.62, w, h); setc(ctx, hx('a8d8f0')); ctx.fill()
    inner(ctx)
    poly(ctx, [(x + 560, y), (x + 700, y), (x + 260, y + h), (x + 120, y + h)]); setc(ctx, (1, 1, 1, 0.22)); ctx.fill()
    poly(ctx, [(x + 740, y), (x + 790, y), (x + 350, y + h), (x + 300, y + h)]); setc(ctx, (1, 1, 1, 0.16)); ctx.fill()
    ctx.restore()
    rect_r(ctx, x, y, w, h, 70); ink(ctx, 10); ctx.stroke()
    for bx in (x + 120, x + 330, x + 540, x + 750):   # vanity bulbs
        ellipse(ctx, bx, y - 30, 30, 30); fl(ctx, hx('fff6c8'), 6)


def kitchen(ctx):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, hx('ffe08a')); ctx.fill()
    for i in range(-30, 40):
        ctx.rectangle(i * 120, -3000, 46, 6000); setc(ctx, hx('ffd46a')); ctx.fill()
    rect_r(ctx, 640, 380, 360, 300, 20); fl(ctx, hx('9fd8ff'), 10)   # window
    ctx.move_to(820, 380); ctx.line_to(820, 680); ctx.move_to(640, 530); ctx.line_to(1000, 530); ink(ctx, 8); ctx.stroke()
    ctx.rectangle(-3000, FLOOR, 7000, 1500); setc(ctx, hx('c98a52')); ctx.fill()
    for i in range(-20, 30):
        ctx.move_to(i * 160, FLOOR); ctx.line_to(i * 160 - 200, FLOOR + 600); setc(ctx, hx('b5773f')); ctx.set_line_width(6); ctx.stroke()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 8); ctx.stroke()


def stool(ctx, x):
    ctx.rectangle(x - 150, FLOOR - 240, 300, 40); fl(ctx, hx('a86a3a'), 8)
    for lx in (x - 120, x + 100):
        ctx.rectangle(lx, FLOOR - 200, 20, 200); fl(ctx, hx('8a5428'), 6)


BX, BY, BR = 400, 820, 150   # boy head in the wide kitchen shot


def stretch_arm(ctx, a, b, w=44, col=DAD['skin']):
    ctx.new_path(); ctx.move_to(*a); ctx.curve_to(a[0], a[1] - 120, b[0] + 60, b[1] + 40, *b)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); setc(ctx, INK); ctx.set_line_width(w + 12); ctx.stroke_preserve(); setc(ctx, col); ctx.set_line_width(w); ctx.stroke()


def wide(ctx, f, lf, stage, dad_p, phi=-0.35, pile=0.0, buzz=True, show_dad=True, boy_p=None):
    kitchen(ctx)
    stool(ctx, BX)
    hair_pile(ctx, BX, FLOOR + 10, pile)
    cape(ctx, BX, BY + 120, FLOOR - 150)
    head_cut(ctx, stage, BX, BY, BR, boy_p or P(eye='normal', mouth='smile'), head_only=True)
    if show_dad:
        b = draw_hip(ctx, 850, 1260, 1.6, -1, DAD, dad_p)
        hx_, hy_ = b['front']
        cxp, cyp = BX + math.cos(phi) * (BR + 70), BY - 20 + math.sin(phi) * (BR + 70)
        hxp, hyp = cxp + math.cos(phi) * 110, cyp + math.sin(phi) * 110
        stretch_arm(ctx, (hx_, hy_), (hxp, hyp))
        clippers(ctx, cxp, cyp, phi - math.pi / 2, 0.75, lf, buzz)
        ellipse(ctx, hxp, hyp, 34, 34); fl(ctx, DAD['skin'], 7)


# ------------------------------------------------------------------ shots
def opening_face(ctx, f, lf, lab=True):
    sh = shake_at(lf, [0], 12, 20) + 1.5
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 60)), 0, sh, f)
    bathroom(ctx)

    def inner(c):
        rays(c, 540, 1060, 250, 1200, lf * 0.02, col=(1, 1, 1), a=0.5, n=16)
        p = P(eye='shock', mouth=talk(lf, 'scream', 'open', 6), head=0)
        head_cut(c, 1, 540 + 6 * math.sin(lf * 0.5), 1120, 340, p)
        falling_hair(c, lf + 20, 380, 700, 720, seed=2, n=6, rate=6, life=36, s=1.4)
    mirror(ctx, inner)
    ctx.restore()
    if lab:
        label(ctx, "\"WHAT DID YOU DO?!\"", 540, 1450, 100, (1, 1, 1), -0.04, pop(lf, 0, 4) if lf > 0 else 1)


def s1(ctx, f):
    if f < 56:
        opening_face(ctx, f, f)
    else:
        lf = f - 56
        dp = P(eye='smug', mouth='grin', rsh=95, rel=-10, lsh=-20, lel=-30, head=-4)
        ctx.save(); cam(ctx, 600, 1000, 1.0 + 0.06 * eout(pop(lf, 0, 54)), 0, 2, f)
        wide(ctx, f, lf, 0, dp, boy_p=P(eye='normal', mouth='flat'))
        ctx.restore()
        label(ctx, "5 MINUTES EARLIER", 540, 580, 60, hx('ffe14d'), 0.0, pop(lf, 0, 4))
        label(ctx, "\"I WATCHED ONE VIDEO\"", 540, 1470, 92, (1, 1, 1), -0.03, pop(lf, 8, 12))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 62:
        # close-up: clippers plough a runway from the fringe to the crown
        prog = eout(pop(lf, 14, 40))
        cx, cy, Rt = 540, 1150, 300
        ctx.save(); cam(ctx, 540, 1050, 1.0 + 0.08 * eout(pop(lf, 0, 60)), 0, 3 + shake_at(lf, [14], 10, 18), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd46a')); ctx.fill()
        rays(ctx, 540, 1000, 200, 1500, lf * 0.02, col=(1, 1, 1), a=0.3, n=14)
        p = P(eye='normal' if lf < 14 else 'shock', mouth='flat' if lf < 14 else 'open')
        head_cut(ctx, 1 if lf >= 14 else 0, cx, cy, Rt, p, prog=max(0.001, prog))
        # clippers ride the top of the runway
        yt = cy + lerp(-0.35, -1.25, prog) * Rt
        cy_ = yt - 40 if lf >= 14 else lerp(500, yt - 40, eout(pop(lf, 0, 14)))
        clippers(ctx, cx + 0.04 * Rt, cy_, math.pi, 1.0, lf, True)
        if lf >= 14:
            falling_hair(ctx, lf, 420, 680, cy - 250, seed=5, n=10, rate=3, life=30, s=1.3)
        ctx.restore()
        if lf >= 14:
            label(ctx, "*BZZZZZT*", 540, 1450, 120, hx('ffe14d'), -0.05, pop(lf, 14, 18))
    else:
        il = lf - 62
        tw = (il // 4) % 2
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.12 * eout(pop(il, 0, 60)), 0, 2 + shake_at(il, [30], 8, 14), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('c8b6ff')); ctx.fill()
        rays(ctx, 540, 960, 300, 1500, il * 0.02, col=(1, 1, 1), a=0.35, n=18)
        later = il >= 30
        face(ctx, DAD, P(eye='smug' if later else 'shock', mouth='grin' if later else 'wavy', head=-6 if later else 4), 540, 1000, 360, 0.0)
        if not later:
            sweat(ctx, 860, 760 + (il % 18) * 6, 2.2); sweat(ctx, 220, 820 + ((il + 9) % 18) * 6, 1.8)
        clippers(ctx, 900, 1260, 0.4, 0.9, il, later)
        ctx.restore()
        if not later:
            label(ctx, "\"...OOPS.\"", 540, 1450, 130, (1, 1, 1), -0.04, pop(il, 2, 6))
        else:
            label(ctx, "\"I'LL EVEN IT OUT\"", 540, 1450, 100, hx('ffe14d'), 0.03, pop(il, 30, 34))
    card(ctx, 'p2', f, 114, 226)


def s3(ctx, f):
    lf = f - 230
    if lf < 92:
        # whirlwind montage in the wide shot
        stage = 1 if lf < 30 else (2 if lf < 62 else 3)
        spin = lf * 0.9
        dp = P(eye='glare', mouth='scream', rsh=95, rel=-10,
               lsh=-60 + 30 * math.sin(spin * 0.7), lel=-40, head=-4 + 4 * math.sin(spin), torso=-6 * math.sin(spin * 0.5))
        bp = P(eye='shock' if stage < 3 else 'closed', mouth='open' if stage < 3 else 'wavy')
        ctx.save(); cam(ctx, 560, 1000, 1.0, 2 * math.sin(lf * 0.4), 6 + shake_at(lf, [30, 62], 8, 14), f)
        wide(ctx, f, lf, stage, dp, phi=-0.75 + 0.55 * math.sin(spin * 0.8), pile=min(160, lf * 2.0), boy_p=bp)
        falling_hair(ctx, lf, BX - 220, BX + 220, BY - 150, seed=7, n=16, rate=2, life=26, s=1.0, floor=FLOOR)
        # whoosh arcs around the head
        for k in range(3):
            a0 = spin * 1.4 + k * 2.1
            ctx.new_path(); ctx.arc(BX, BY - 20, 230 + k * 30, a0, a0 + 1.4); setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(12); ctx.stroke()
        ctx.restore()
        label(ctx, "*BZZZZZZZZZT*", 540, 1460, 110, hx('ffe14d'), -0.04 + 0.03 * math.sin(lf * 0.6), pop(lf, 2, 6))
        if 30 <= lf < 62:
            label(ctx, "LEFT SIDE...", 400, 1250, 64, (1, 1, 1), 0.06, pop(lf, 30, 34))
        elif lf >= 62:
            label(ctx, "RIGHT SIDE...", 400, 1250, 64, (1, 1, 1), -0.06, pop(lf, 62, 66))
    else:
        il = lf - 92
        # deadpan reveal ECU: three hairs left, one drifts down
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.1 * eout(pop(il, 0, 48)), 0, shake_at(il, [0], 10, 16), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('b6f0a0')); ctx.fill()
        rays(ctx, 540, 1000, 300, 1500, il * 0.01, col=(1, 1, 1), a=0.3, n=16)
        head_cut(ctx, 3, 540, 1080, 340, P(eye='normal' if il < 20 else 'glare', mouth='flat'))
        # a lone hair drifting down
        u = pop(il, 4, 44)
        clump(ctx, 650 + 80 * math.sin(u * 9), lerp(700, 1500, u), 0.6 * math.sin(u * 7), 1.4)
        # Dad's thumbs-up from the right edge
        tx = lerp(1200, 880, eout(pop(il, 14, 22)))
        ellipse(ctx, tx, 1300, 70, 62); fl(ctx, DAD['skin'], 8)
        rect_r(ctx, tx - 22, 1170, 44, 110, 20); fl(ctx, DAD['skin'], 8)
        ctx.restore()
        label(ctx, "\"...NAILED IT.\"", 540, 1460, 110, (1, 1, 1), -0.03, pop(il, 16, 20))
    card(ctx, 'p3', f, 234, 366)


def split_panel(ctx, x0, x1, ch, p, fp, bg, cx_off=0, extra=None):
    ctx.save()
    ctx.rectangle(x0, 0, x1 - x0, H); ctx.clip()
    ctx.rectangle(x0, 0, x1 - x0, H); setc(ctx, bg); ctx.fill()
    cx = (x0 + x1) / 2 + cx_off
    if extra:
        extra(ctx, cx)
    else:
        face(ctx, ch, p, cx, 1000, 230, 0, fp)
    ctx.restore()


def s4(ctx, f):
    lf = f - 370
    if lf < 62:
        # Mom in the doorway, low angle push-in, mug slips
        DROP = 22
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.12 * eout(pop(lf, 0, 20)), 0, shake_at(lf, [0, DROP + 14], 10, 22), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb3d1')); ctx.fill()
        rays(ctx, 540, 960, 300, 1500, lf * 0.02, col=(1, 1, 1), a=0.4, n=16)
        ctx.rectangle(140, 300, 800, 1700); fl(ctx, hx('fff2c8'), 12)   # door frame
        face(ctx, MOM, P(eye='normal' if lf < 6 else 'shock', mouth='smile' if lf < 6 else talk(lf, 'scream', 'open', 5), head=4), 540, 980, 340, 0.0)
        u = pop(lf, DROP, DROP + 14)
        if u < 1:
            mug(ctx, 820 + 40 * u, lerp(1260, 1500, ein(u)), 1.4 * u, 1.2)
        else:
            rnd = random.Random(3)
            for k in range(8):   # shards fly
                v = pop(lf, DROP + 14, DROP + 34)
                sx = 860 + rnd.uniform(-1, 1) * 300 * v; sy = 1480 - rnd.uniform(100, 300) * math.sin(math.pi * v)
                poly(ctx, [(sx, sy), (sx + 30, sy + 8), (sx + 8, sy + 34)]); fl(ctx, (1, 1, 1), 5)
            ellipse(ctx, 860, 1520, 1 + 220 * eout(pop(lf, DROP + 14, DROP + 24)), 40); setc(ctx, hx('8a5a30', 0.8)); ctx.fill()
        ctx.restore()
        label(ctx, "\"WHAT HAPPENED?!\"", 540, 1400, 100, (1, 1, 1), -0.03, pop(lf, 6, 10))
        if lf >= DROP + 14:
            label(ctx, "*CRASH*", 820, 1250, 90, hx('ffe14d'), 0.1, pop(lf, DROP + 14, DROP + 18))
    else:
        il = lf - 62
        sl = eout(pop(il, 0, 8))
        ctx.save(); cam(ctx, 540, 960, 1.0, 0, shake_at(il, [10], 8, 16), f)
        mid = 540

        def dad_point(c, cx):
            face(c, DAD, P(eye='smug' if il < 40 else 'shock', mouth=talk(il, 'open', 'flat', 5) if il < 34 else 'wavy', head=-6), cx - 20, 1000, 220, 0, 1)
            # pointing finger towards the kid's panel
            c.save(); c.translate(cx + 210, 1240)
            ellipse(c, 0, 0, 56, 48); fl(c, DAD['skin'], 7)
            rect_r(c, 20, -22, 120, 40, 20); fl(c, DAD['skin'], 7)
            c.restore()
            if il >= 40:
                sweat(c, cx + 170, 820 + (il % 16) * 5, 1.6)

        def kid_glare(c, cx):
            head_cut(c, 3, cx + 10, 1000, 220, P(eye='glare', mouth='flat', head=4), 0, -1)

        split_panel(ctx, -10, lerp(-10, mid, sl), DAD, None, 1, hx('ffe08a'), extra=dad_point)
        split_panel(ctx, lerp(1090, mid, sl), 1090, BOY, None, -1, hx('9fd8ff'), extra=kid_glare)
        ctx.move_to(lerp(-10, mid, sl), 0); ctx.line_to(lerp(-10, mid, sl), H); ink(ctx, 14); ctx.stroke()
        ctx.restore()
        label(ctx, "\"HE MOVED.\"", 540, 1450, 120, (1, 1, 1), -0.04, pop(il, 6, 10))
    card(ctx, 'p4', f, 374, 496)


def s5(ctx, f):
    lf = f - 500
    if lf < 70:
        # night: Dad asleep on the sofa, kid tiptoes in with the clippers
        ctx.save(); cam(ctx, 600, 1050, 1.0 + 0.15 * eout(pop(lf, 40, 70)), 0, shake_at(lf, [52], 10, 22), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('2a2f6a')); ctx.fill()
        rect_r(ctx, 60, 560, 260, 240, 20); fl(ctx, hx('3a4a9a'), 10)
        ellipse(ctx, 190, 680, 60, 60); setc(ctx, hx('fff6c8')); ctx.fill()
        ellipse(ctx, 212, 666, 52, 52); setc(ctx, hx('3a4a9a')); ctx.fill()   # crescent moon
        ctx.rectangle(-500, FLOOR, 2200, 800); setc(ctx, hx('3a2f5a')); ctx.fill()
        # sofa
        rect_r(ctx, 20, 960, 760, 300, 60); fl(ctx, hx('6a4aa8'), 10)
        rect_r(ctx, -20, 1180, 840, 260, 60); fl(ctx, hx('7a5ac0'), 10)
        face(ctx, DAD, P(eye='closed', mouth='open', head=0), 300, 1090, 170, -0.5)
        ctx.new_path(); ctx.move_to(380, 1190); ctx.curve_to(500, 1120, 700, 1140, 780, 1200); ctx.line_to(780, 1320); ctx.line_to(360, 1320); ctx.close_path()
        fl(ctx, hx('ffd23f'), 9)   # blanket
        zz = (lf % 30) / 30
        label(ctx, "Z", 430 + 60 * zz, 900 - 120 * zz, 60 + 30 * zz, (1, 1, 1))
        # kid creeping in from the right
        kx = lerp(1250, 820, eout(pop(lf, 0, 34)))
        tip = abs(math.sin(lf * 0.3)) * 30 * (1 - pop(lf, 30, 34))
        bp = P(eye='glare', mouth='grin', torso=-8, rsh=160, rel=-20, lsh=60, lel=-60, lhip=-14, lkn=20, rhip=14, rkn=-6)
        b = draw_hip(ctx, kx, FLOOR - 145 - tip, 1.5, -1, BALD, bp)
        hd = b['head']
        clippers(ctx, hd[0] - 150, hd[1] - 120, -0.5, 0.6, lf, lf >= 46)
        ctx.restore()
        if lf < 40:
            label(ctx, "*TIPTOE TIPTOE*", 540, 1460, 90, hx('c8b6ff'), -0.04, pop(lf, 4, 8))
        else:
            label(ctx, "*BZZZZZT*", 540, 1460, 120, hx('ffe14d'), 0.04, pop(lf, 46, 50))
        if lf >= 52:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.8 * (1 - pop(lf, 52, 58)))); ctx.fill()
        card(ctx, 'p5', f, 504, 616)
    elif lf < 120:
        il = lf - 70
        # morning: Dad in the same mirror with the same runway
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(il, 0, 50)), 0, shake_at(il, [0, 26], 12, 20) + 1.5, f)
        bathroom(ctx)

        def inner(c):
            rays(c, 540, 1060, 250, 1200, il * 0.02, col=(1, 1, 1), a=0.5, n=16)
            face(c, DAD, P(eye='shock', mouth=talk(il, 'scream', 'open', 6), head=0), 540, 1120, 340, 0.0)
            scalp(c, 540, 1120, 340, 1, 0.0, [(-0.22, 0.3, -0.58)], ch=DAD)
            # the kid peeks in at the bottom corner, whistling innocently
            u = eout(pop(il, 22, 30))
            head_cut(c, 3, 860, lerp(1700, 1420, u), 140, P(eye='happy', mouth='open', head=8), 0.15, -1)
        mirror(ctx, inner)
        ctx.restore()
        label(ctx, "\"WHO DID THIS?!\"", 540, 1450, 110, (1, 1, 1), -0.04, pop(il, 2, 6))
        card(ctx, 'p5', f, 504, 616)
    else:
        il = lf - 120
        opening_face(ctx, f, il, True)
        card(ctx, 'p1', f, 620)


SHOTS = [(0, s1), (110, s2), (230, s3), (370, s4), (500, s5)]
CUTS = (56, 110, 172, 230, 322, 370, 432, 500, 570, 620)


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.25)
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
                              "-i", "out/haircut_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
