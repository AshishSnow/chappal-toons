"""'Dad vs ONE Mosquito' - original, general-audience comedy short, 22s.
Hook: Dad ECU in the dark, bloodshot eyes darting, a tiny mosquito circling his head: "*bzzzzz...*"
Beat 1: *SLAP!* he slaps his own face -> red handprint, the mosquito waves: "...MISSED."
Beat 2: LIGHTS ON -> it vanishes (sitting on top of his head). OFF -> "BZZZ!" in his ear. ON -> silence. faster and faster.
Beat 3: BATTLE MODE: goggles, headlamp, two swatters -> wild swinging, lamp CRASH, pillow POOF, Mom sleeps through it,
 Dad flat on the floor, mosquito lands on his nose: "...it's TOO FAST."
Twist: Mom sits up, eyes still closed, ONE *CLAP!* -> flat mosquito in her palm: "Goodnight." -> Dad: "...HOW?!"
 -> lights off, "Finally... PEACE." -> through the window: the WHOLE mosquito family -> Dad "...honey?"
 -> Mom asleep, flat palm up: "Your turn." -> opening ECU (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos, zigs, zzz, bloodshot, bedroom, bed_back, bed_front
from scenes48 import label1, label2
from scenes58 import arm_to, sweat, twitch
import scenes13
from scenes13 import card as _card13
import random

MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'), pants=hx('3d5a9e'))
DAD = dict(doodle.DAD, shirt=hx('7fd0ff'), pants=hx('3d5aff'))
N = 660
FLOOR = 1460
TOP = 1170
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
GOLD = hx('ffc93c')
WHITE = (1, 1, 1)
NIGHT = hx('141a3e')

CAPS = {
    'p1': [[("DAD", OUT)], [("VS. ONE MOSQUITO", RED)]],
    'p2': [[("LIGHTS ON:", OUT)], [("IT VANISHES", BLUE)]],
    'p3': [[("DAD'S", OUT)], [("BATTLE MODE", ORANGE)]],
    'p4': [[("THEN MOM", OUT)], [("WOKE UP...", PINK)]],
    'p5': [[("BUT IT CAME BACK", OUT)], [("WITH THE FAMILY", RED)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def mosquito(ctx, x, y, s=1.0, lf=0, a=0.0, dead=False, glow=0.0, f_=1):
    """cartoon mosquito, needle nose pointing left (f_=-1 flips). ~220 px wide at s=1"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s * f_, s)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 10, 0, 0, 200)
        g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.55 * glow); g.add_color_stop_rgba(1, 1, 0.95, 0.5, 0)
        ctx.set_source(g); ellipse(ctx, 0, 0, 200, 200); ctx.fill()
    if dead:
        ctx.scale(1.25, 0.35)
    flap = abs(math.sin(lf * 2.6)) if not dead else 0.3
    # legs
    for k in range(3):
        lx = -14 + k * 18
        ctx.move_to(lx, 10); ctx.line_to(lx - 20 + k * 12, 50); ctx.line_to(lx - 30 + k * 18, 82)
    ink(ctx, 5); ctx.stroke()
    # abdomen
    ctx.save(); ctx.translate(60, 4); ctx.rotate(0.22)
    ellipse(ctx, 0, 0, 60, 24); fl(ctx, hx('6a5a7e'), 6)
    for k in range(3):
        ctx.move_to(-28 + k * 22, -22); ctx.line_to(-34 + k * 22, 22)
    setc(ctx, hx('3a3048')); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()
    # wings (flapping)
    for dx, rot in ((10, -0.5), (34, -0.9)):
        ctx.save(); ctx.translate(dx, -24); ctx.rotate(rot - 0.35 * flap)
        ellipse(ctx, 34, 0, 50, 14 + 10 * flap); setc(ctx, (0.85, 0.95, 1, 0.8)); ctx.fill_preserve(); ink(ctx, 4); ctx.stroke()
        ctx.restore()
    # thorax + head
    ellipse(ctx, 4, 0, 30, 26); fl(ctx, hx('4a3e5c'), 6)
    ellipse(ctx, -34, -6, 26, 24); fl(ctx, hx('4a3e5c'), 6)
    # needle nose
    ctx.move_to(-56, 2); ctx.line_to(-118, 26); ink(ctx, 7); ctx.stroke()
    # big cheeky eyes
    for ex in (-48, -26):
        ellipse(ctx, ex, -16, 13, 15); fl(ctx, (1, 1, 1), 4)
        if dead:
            ctx.move_to(ex - 8, -24); ctx.line_to(ex + 8, -8); ctx.move_to(ex + 8, -24); ctx.line_to(ex - 8, -8)
            ink(ctx, 4); ctx.stroke()
        else:
            ellipse(ctx, ex - 4, -14, 6, 7); setc(ctx, INK); ctx.fill()
    ctx.restore()


def trail(ctx, pts, a=0.6):
    for k, (px, py) in enumerate(pts):
        ellipse(ctx, px, py, 7, 7); setc(ctx, (1, 1, 1, a * (k + 1) / len(pts))); ctx.fill()


def fly_path(lf, cx, cy, rx, ry, sp=0.22, k=0):
    t = lf * sp + k
    return cx + rx * math.cos(t) + 40 * math.sin(t * 3.1), cy + ry * math.sin(2 * t) * 0.6 + 30 * math.cos(t * 2.3)


def swatter(ctx, x, y, a=0.0, s=1.0, col=RED):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(0, 0); ctx.line_to(0, 240); setc(ctx, INK); ctx.set_line_width(34); ctx.stroke()
    ctx.move_to(0, 0); ctx.line_to(0, 240); setc(ctx, GOLD); ctx.set_line_width(18); ctx.stroke()
    rect_r(ctx, -80, -190, 160, 190, 26); fl(ctx, col, 8)
    for k in range(1, 5):
        ctx.move_to(-80 + k * 32, -186); ctx.line_to(-80 + k * 32, -4)
        ctx.move_to(-76, -190 + k * 38); ctx.line_to(76, -190 + k * 38)
    setc(ctx, dark(col, 0.7)); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


def newspaper(ctx, x, y, a=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -30, -230, 60, 260, 22); fl(ctx, hx('eef0f4'), 7)
    for k in range(5):
        ctx.move_to(-18, -200 + k * 40); ctx.line_to(18, -190 + k * 40)
    setc(ctx, hx('a0a6b8')); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def handprint(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    setc(ctx, (1, 0.2, 0.3, 0.6))
    ellipse(ctx, 0, 30, 46, 52); ctx.fill()
    for k in range(4):
        rect_r(ctx, -42 + k * 22, -70 + abs(k - 1.5) * 10, 18, 80, 9); ctx.fill()
    ctx.save(); ctx.translate(48, 40); ctx.rotate(-0.8); rect_r(ctx, -9, -50, 18, 60, 9); ctx.fill(); ctx.restore()
    ctx.restore()


def palm(ctx, x, y, s=1.0, a=0.0, col=None):
    col = col or MOM['skin']
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    for k in range(4):
        rect_r(ctx, -58 + k * 30, -150 + abs(k - 1.5) * 14, 28, 110, 14); fl(ctx, col, 6)
    ctx.save(); ctx.translate(66, -10); ctx.rotate(-0.7); rect_r(ctx, -15, -70, 30, 84, 15); fl(ctx, col, 6); ctx.restore()
    ellipse(ctx, 0, 0, 72, 70); fl(ctx, col, 7)
    ctx.restore()


def goggles(ctx, b, lens=hx('7fe0ff')):
    hx_, hy_ = b['head']; R = b['R']
    ctx.move_to(hx_ - R * 1.0, hy_ + R * 0.1); ctx.line_to(hx_ + R * 1.0, hy_ + R * 0.1); setc(ctx, INK); ctx.set_line_width(R * 0.16); ctx.stroke()
    ctx.move_to(hx_ - R * 1.0, hy_ + R * 0.1); ctx.line_to(hx_ + R * 1.0, hy_ + R * 0.1); setc(ctx, ORANGE); ctx.set_line_width(R * 0.09); ctx.stroke()
    for k in ('eyeL', 'eyeR'):
        ex, ey = b[k]
        ellipse(ctx, ex, ey, R * 0.3, R * 0.26); setc(ctx, lens + (0.6,)); ctx.fill_preserve(); ink(ctx, R * 0.07); ctx.stroke()
        ellipse(ctx, ex - R * 0.1, ey - R * 0.1, R * 0.07, R * 0.05); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()


def headlamp(ctx, b, f_=1, beam=1.0, ang=0.0):
    hx_, hy_ = b['head']; R = b['R']
    lx, ly = hx_ + f_ * R * 0.15, hy_ - R * 0.62
    if beam > 0:
        ctx.save(); ctx.translate(lx, ly); ctx.rotate(ang)
        poly(ctx, [(0, -R * 0.12), (f_ * 1400, -500), (f_ * 1400, 400), (0, R * 0.12)])
        g = cairo.LinearGradient(0, 0, f_ * 1400, 0)
        g.add_color_stop_rgba(0, 1, 0.97, 0.6, 0.55 * beam); g.add_color_stop_rgba(1, 1, 0.97, 0.6, 0)
        ctx.set_source(g); ctx.fill()
        ctx.restore()
    rect_r(ctx, lx - R * 0.2, ly - R * 0.14, R * 0.4, R * 0.28, R * 0.08); fl(ctx, hx('3a3a4a'), R * 0.05)
    ellipse(ctx, lx, ly, R * 0.1, R * 0.1); setc(ctx, YEL); ctx.fill()


def nightstand(ctx, x=1000, lamp=0.0, lit=True):
    """lamp falls over as lamp goes 0 -> 1"""
    rect_r(ctx, x - 90, 1220, 180, FLOOR - 1220, 10); fl(ctx, hx('c96a2a'), 8)
    ctx.save(); ctx.translate(x + 40 * lamp, 1220 + 0 * lamp); ctx.rotate(1.6 * eout(min(1, lamp)))
    ctx.rectangle(-12, -150, 24, 150); fl(ctx, hx('3a3a4a'), 5)
    poly(ctx, [(-70, -150), (70, -150), (45, -250), (-45, -250)]); fl(ctx, YEL if lit else hx('8a8a5a'), 7)
    ctx.restore()


def frame_pic(ctx, x, y, tilt=0.0):
    ctx.save(); ctx.translate(x, y - 90); ctx.rotate(tilt)
    ctx.move_to(0, 0); ctx.line_to(-60, 90); ctx.move_to(0, 0); ctx.line_to(60, 90); ink(ctx, 5); ctx.stroke()
    rect_r(ctx, -110, 90, 220, 170, 8); fl(ctx, hx('ffd23f'), 8)
    ctx.rectangle(-86, 114, 172, 122); setc(ctx, hx('9fe0ff')); ctx.fill()
    poly(ctx, [(-86, 236), (-30, 160), (20, 236)]); setc(ctx, GREEN); ctx.fill()
    poly(ctx, [(0, 236), (50, 180), (86, 236)]); setc(ctx, hx('1f9a4a')); ctx.fill()
    ellipse(ctx, 50, 140, 16, 16); setc(ctx, hx('ff8a1f')); ctx.fill()
    ctx.restore()


def feathers(ctx, x, y, t, n=14):
    if t <= 0 or t >= 1:
        return
    rnd = random.Random(9)
    for k in range(n):
        a = rnd.uniform(0, 2 * math.pi); d = 60 + 380 * eout(t) * rnd.uniform(0.5, 1)
        px, py = x + math.cos(a) * d, y + math.sin(a) * d * 0.7 + 200 * t * t
        ctx.save(); ctx.translate(px, py); ctx.rotate(a + t * 4)
        ellipse(ctx, 0, 0, 30, 12); setc(ctx, (1, 1, 1, 1 - t)); ctx.fill_preserve(); setc(ctx, INK + (1 - t,)); ctx.set_line_width(3); ctx.stroke()
        ctx.restore()


def impact(ctx, x, y, r, t, col=YEL):
    if t <= 0 or t >= 1:
        return
    rr = r * (0.6 + 0.6 * eout(t))
    pts = []
    for k in range(20):
        a = k * math.pi / 10
        d = rr if k % 2 == 0 else rr * 0.55
        pts.append((x + math.cos(a) * d, y + math.sin(a) * d))
    poly(ctx, pts); setc(ctx, col + (1 - t * 0.7,)); ctx.fill_preserve(); setc(ctx, INK + (1 - t * 0.7,)); ctx.set_line_width(8); ctx.stroke()


def dark_eyes(ctx, cx, cy, s, lf, look=0.0):
    """only the eyes glowing in pitch black"""
    for dx in (-1, 1):
        ex = cx + dx * 120 * s
        ellipse(ctx, ex, cy, 90 * s, 110 * s); fl(ctx, (1, 1, 1), 8 * s)
        ellipse(ctx, ex + look * 40 * s, cy + 10 * s, 32 * s, 38 * s); setc(ctx, INK); ctx.fill()
        ellipse(ctx, ex + look * 40 * s - 10 * s, cy - 6 * s, 9 * s, 9 * s); setc(ctx, (1, 1, 1)); ctx.fill()


def bed_scene(ctx, f, lights, z=1.0, cx=540, cy=1150, rot=0.0, shake=0, mom_face=True, lamp=0.0, tilt=0.0, wall_dim=0.0):
    ctx.save(); cam(ctx, cx, cy, z, rot, shake, f)
    bedroom(ctx, lights=lights, hh=3, mm=0)
    frame_pic(ctx, 560, 700, tilt)
    nightstand(ctx, 1040, lamp, lights)
    bed_back(ctx, 120, 900)


def bed_scene_end(ctx, dim=0.0):
    bed_front(ctx, 120, 900)
    if dim > 0:
        ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, (0.03, 0.04, 0.15, dim)); ctx.fill()
    ctx.restore()


def mom_sleeping(ctx, lf, x=250, y=1112, R=78):
    face(ctx, MOM, P(eye='closed', mouth='flat', head=0), x, y, R, -1.25)
    zzz(ctx, x + 40, y - 90, lf, 0.8)


# ------------------------------------------------------------------ opening face
def opening_face(ctx, f, lf, lab=True):
    ctx.save(); cam(ctx, 540, 980, 1.04 + 0.05 * eout(pop(lf, 0, 45)), 0, 3 + shake_at(lf, [0], 10, 16), f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, NIGHT); ctx.fill()
    rays(ctx, 540, 980, 260, 1700, lf * 0.03, col=(0.4, 0.5, 1.0), a=0.3, n=16)
    jx = 6 * math.sin(lf * 1.9)
    cx, cy, R = 540 + jx, 1000, 310
    # pupils dart: alternate head turn left/right following the bug
    mx, my = fly_path(lf, 540, 820, 400, 380, 0.24)
    face(ctx, DAD, P(eye='shock', mouth='wavy', head=0, turn=(mx - 540) / 400), cx, cy, R, 0.04 * (mx - 540) / 400)
    bloodshot(ctx, cx, cy, R, 1, seed=lf // 3)
    sweat(ctx, cx + 0.95 * R, cy - 0.5 * R, lf, 1.3)
    pts = [fly_path(lf - k * 0.8, 540, 820, 400, 380, 0.24) for k in range(12, 0, -1)]
    trail(ctx, pts, 0.5)
    mosquito(ctx, mx, my, 0.75, lf, 0.1 * math.sin(lf), glow=0.6, f_=1 if math.sin(lf * 0.24) > 0 else -1)
    ctx.restore()
    if lab:
        label1(ctx, "*bzzzzzzzz...*", YEL, pop(lf, 0, 4) if lf > 0 else 1, 120, -0.04, y=1420)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 45:
        opening_face(ctx, f, f)
    else:
        lf = f - 45
        cx, cy, R = 540, 1000, 310
        ctx.save(); cam(ctx, 540, 980, 1.08, 0, shake_at(lf, [8], 12, 26), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, NIGHT if lf < 8 else hx('ff5a7a')); ctx.fill()
        if lf >= 8:
            rays(ctx, 540, 980, 260, 1700, lf * 0.05, col=(1, 0.9, 0.5), a=0.4, n=16)
        face(ctx, DAD, P(eye='glare' if lf < 8 else ('closed' if lf < 18 else 'shock'), mouth='flat' if lf < 8 else 'wavy', head=0), cx, cy, R, 0.0 if lf < 8 else -0.08)
        if lf < 12:
            # hand swinging in from the right onto his own cheek
            u = eout(pop(lf, 0, 8))
            hx_, hy_ = 1300 - 520 * u, 1500 - 360 * u
            arm_to(ctx, 1300, 2100, hx_, hy_, DAD['shirt'], DAD['skin'], bend=-60, w=110)
            palm(ctx, hx_, hy_, 1.4, -0.4, DAD['skin'])
            impact(ctx, 760, 1080, 220, pop(lf, 8, 16))
        else:
            handprint(ctx, cx + 0.48 * R, cy + 0.2 * R, 1.25, 0.3)
            mosquito(ctx, 540 + 240 * math.sin(lf * 0.18), 700 + 30 * math.sin(lf * 0.5), 0.75, lf, 0.1, glow=0.4, f_=-1)
        ctx.restore()
        if lf < 18:
            label(ctx, "*SLAP!*", 540, 640, 150, YEL, -0.08, pop(lf, 8, 11))
        else:
            label1(ctx, "\"...MISSED.\"", WHITE, pop(lf, 20, 24), 130, -0.04, y=1420)
    card(ctx, 'p1', f, -6, 86)


# lights flicker: (start, length, on?)
FLICK = [(125, 18, False), (143, 14, True), (157, 12, False), (169, 10, True), (179, 8, False), (187, 6, True), (193, 7, False)]


def s2(ctx, f):
    lf = f - 90
    if f < 125:
        # LIGHTS ON: wide bedroom, Dad standing on the bed with a rolled newspaper. the bug sits on HIS head.
        look = math.sin(lf * 0.25)
        bed_scene(ctx, f, True, 0.98 + 0.04 * eout(pop(lf, 0, 35)), 540, 900, 0, shake_at(lf, [0], 6, 8))
        mom_sleeping(ctx, lf)
        k = 1.25
        b = draw(ctx, 600, TOP - 186 * k + 6, k, 1 if look > 0 else -1, DAD,
                 P(eye='glare', mouth='flat', head=10 * look, lsh=-30, rsh=165, rel=15, lhip=-8, rhip=8))
        newspaper(ctx, b['head'][0] + (1 if look > 0 else -1) * b['R'] * 1.5, b['head'][1] + b['R'] * 0.6, (1 if look > 0 else -1) * 0.35, 1.0)
        hx_, hy_ = b['head']
        bed_scene_end(ctx)
        mosquito(ctx, hx_ + 10, hy_ - b['R'] * 1.15, 0.3, 0, 0.0, f_=-1)
        if lf > 14:
            label(ctx, "!", hx_ + 70, hy_ - b['R'] * 1.7, 70, YEL, 0.1, pop(lf, 14, 17))
        label1(ctx, "\"WHERE ARE YOU?!\"", WHITE, pop(lf, 3, 7), 118, -0.04, y=1420)
        label(ctx, "*CLICK!*", 540, 560, 80, YEL, 0.05, pop(lf, 0, 3) * (1 - pop(lf, 12, 16)))
    else:
        seg = [s for s in FLICK if s[0] <= f][-1]
        st, ln, on = seg
        il = f - st
        idx = FLICK.index(seg)
        if on:
            ctx.save(); cam(ctx, 540, 1000, 1.0, 0, shake_at(il, [0], 4, 6), f)
            ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffe27a')); ctx.fill()
            rays(ctx, 540, 960, 260, 1700, f * 0.02, col=(1, 1, 1), a=0.35, n=14)
            face(ctx, DAD, P(eye='shock', mouth='flat', head=0, turn=(-1) ** idx), 540, 980, 280 + idx * 6, 0.05 * (-1) ** idx)
            bloodshot(ctx, 540, 980, 280 + idx * 6, 1, seed=idx)
            ctx.restore()
            label1(ctx, "*...silence...*", WHITE, pop(il, 1, 3), 100, -0.03, y=1420)
        else:
            ctx.save(); cam(ctx, 540, 960, 1.0, 0, 6 + idx * 2, f)
            ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('05060f')); ctx.fill()
            dark_eyes(ctx, 540, 900, 1.0 + idx * 0.12, il, look=1.0)
            mx = 880 - idx * 20 + 30 * math.sin(il * 0.9); my = 980 + 40 * math.cos(il * 0.7)
            mosquito(ctx, mx, my, 0.55 + 0.08 * idx, il, 0.1, glow=0.9)
            ctx.restore()
            label(ctx, "BZZZZ!" if idx < 6 else "BZZZZZZZ!!", 540, 1420, 130 + idx * 10, YEL, -0.05 + 0.03 * (-1) ** idx, pop(il, 0, 3))
        label(ctx, "*CLICK*", 540, 640, 70, WHITE, 0.05 * (-1) ** idx, pop(il, 0, 2) * (1 - pop(il, ln - 3, ln)))
    card(ctx, 'p2', f, 92, 124)


def battle_dad(ctx, x, k, lf, f_, swing):
    """Dad in full gear; swing in [-1, 1] alternates the swatters"""
    p = P(eye='glare', mouth='scream' if abs(swing) > 0.6 else 'grin', head=0,
          lsh=-150 + 90 * swing, lel=-30, rsh=150 + 90 * swing, rel=30, lhip=-14, rhip=14, lkn=6, rkn=6)
    b = draw(ctx, x, TOP - 186 * k + 6, k, f_, DAD, p)
    for side, a in (('front', -0.4 + 0.9 * swing), ('back', 0.4 + 0.9 * swing)):
        swatter(ctx, b[side][0], b[side][1], a + math.pi, 0.7 * k, RED if side == 'front' else BLUE)
    goggles(ctx, b)
    headlamp(ctx, b, f_, 0.0)
    return b


def s3(ctx, f):
    lf = f - 200
    if lf < 40:
        # gear-up: snap zooms (goggles -> swatter -> full low angle)
        k = 1.5
        ctx.save()
        if lf < 9:
            z, cx, cy = 2.6, 560, 780
        elif lf < 18:
            z, cx, cy = 2.2, 380, 900
        else:
            z, cx, cy = 0.95 - 0.05 * eout(pop(lf, 18, 40)), 540, 1000
        cam(ctx, cx, cy, z, -3 if lf >= 18 else 4, shake_at(lf, [0, 9, 18], 6, 12), f)
        ctx.rectangle(-1000, -1000, 3200, 4000); setc(ctx, hx('ff3b5c')); ctx.fill()
        rays(ctx, 540, 900, 200, 2200, lf * 0.06, col=(1, 0.85, 0.3), a=0.5, n=18)
        ctx.rectangle(-1000, TOP + 40, 3200, 2000); setc(ctx, hx('3ccfb0')); ctx.fill()
        ctx.move_to(-1000, TOP + 40); ctx.line_to(2200, TOP + 40); ink(ctx, 8); ctx.stroke()
        b = draw(ctx, 540, TOP + 40 - 186 * k, k, 1, DAD, P(eye='glare', mouth='grin', lsh=-160, lel=-20, rsh=160, rel=20, lhip=-14, rhip=14))
        swatter(ctx, b['front'][0], b['front'][1], math.pi - 0.3, 0.9, RED)
        swatter(ctx, b['back'][0], b['back'][1], math.pi + 0.3, 0.9, BLUE)
        goggles(ctx, b)
        headlamp(ctx, b, 1, 0.8, -0.5)
        ctx.restore()
        if lf < 9:
            label(ctx, "GOGGLES", 540, 1420, 120, YEL, -0.05, pop(lf, 0, 3))
        elif lf < 18:
            label(ctx, "SWATTERS x2", 540, 1420, 120, YEL, 0.05, pop(lf, 9, 12))
        else:
            label2(ctx, "\"THIS. MEANS.", "WAR.\"", WHITE, pop(lf, 19, 23), 124, col2=YEL, y=1400)
        card(ctx, 'p3', f, 220, 240)
    elif lf < 100:
        il = lf - 40
        # chaos: wild swinging, the bug dodges everything; lamp, frame, pillow casualties. Mom sleeps.
        swing = math.sin(il * 0.75)
        lamp = pop(il, 14, 22); tilt = 0.5 * eout(pop(il, 28, 34))
        bed_scene(ctx, f, True, 0.92, 540, 1020, 2 * math.sin(il * 0.4), 4 + shake_at(il, [14, 28, 42], 12, 20), lamp=lamp, tilt=tilt)
        mom_sleeping(ctx, il)
        f_ = 1 if (il // 14) % 2 == 0 else -1
        battle_dad(ctx, 600 + 60 * math.sin(il * 0.3), 1.2, il, f_, swing)
        bed_scene_end(ctx)
        ctx.save(); cam(ctx, 540, 1020, 0.92, 2 * math.sin(il * 0.4), 0, f)
        feathers(ctx, 260, 1080, pop(il, 42, 66))
        impact(ctx, 1060, 1100, 150, pop(il, 22, 30))
        mx, my = fly_path(il, 600, 700, 380, 300, 0.33)
        pts = [fly_path(il - k * 0.7, 600, 700, 380, 300, 0.33) for k in range(10, 0, -1)]
        trail(ctx, pts, 0.7)
        mosquito(ctx, mx, my, 0.45, il, 0.2 * math.sin(il), f_=1 if math.cos(il * 0.33) < 0 else -1)
        ctx.restore()
        label1(ctx, "\"HOLD. STILL!!\"", WHITE, pop(il, 2, 6), 120, -0.04, y=1420)
        for st, s_, x, y, col in ((6, "*WHACK!*", 300, 620, YEL), (22, "*CRASH!*", 760, 640, ORANGE), (42, "*POOF!*", 330, 640, WHITE)):
            if st <= il < st + 14:
                label(ctx, s_, x, y, 92, col, -0.1, pop(il, st, st + 3))
    else:
        il = lf - 100
        # flat on the floor, upside-down ECU, the bug lands on his nose
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eout(pop(il, 0, 30)), 0, shake_at(il, [0], 14, 26), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('8a5ac8')); ctx.fill()
        for i in range(-10, 20):
            ctx.move_to(-500, i * 140); ctx.line_to(2000, i * 140 + 300)
        setc(ctx, hx('7a4ab8')); ctx.set_line_width(12); ctx.stroke()
        cx, cy, R = 540, 940, 290
        face(ctx, DAD, P(eye='closed', mouth='wavy', head=0), cx, cy, R, math.pi * 0.94)
        hx_, hy_ = cx, cy + 0.0 * R
        for k in range(5):     # dizzy stars
            a = il * 0.2 + k * 1.25
            sparkle(ctx, cx + math.cos(a) * 380, cy + 360 + math.sin(a) * 90, 30)
        land = eout(pop(il, 6, 18))
        mosquito(ctx, 540 + 300 * (1 - land), 900 - 320 * (1 - land) - 10, 0.6, il if land < 1 else 0, 0.0, f_=-1)
        ctx.restore()
        label(ctx, "*THUD!*", 540, 640, 120, ORANGE, -0.08, pop(il, 0, 3) * (1 - pop(il, 12, 16)))
        label2(ctx, "\"...it's...", "TOO FAST.\"", WHITE, pop(il, 8, 12), 116, col2=YEL, y=1400)


def s4(ctx, f):
    lf = f - 330
    if lf < 42:
        # Mom sits up, eyes still closed; bug buzzing at her
        bed_scene(ctx, f, True, 1.18, 420, 1050, 0, 0)
        b = draw_hip(ctx, 330, TOP + 60, 1.15, 1, MOM, P(eye='closed', mouth='flat', lsh=-20, rsh=20, torso=-6 + 6 * eout(pop(lf, 0, 10))))
        bed_scene_end(ctx)
        ctx.save(); cam(ctx, 420, 1050, 1.18, 0, 0, f)
        mx, my = 560 + 90 * math.sin(lf * 0.4), 760 + 50 * math.cos(lf * 0.6)
        mosquito(ctx, mx, my, 0.4, lf, 0.1, f_=1)
        ctx.restore()
        # Dad peeking from the floor (bottom-left)
        label1(ctx, "*bzz... bzz...*", YEL, pop(lf, 4, 8), 100, -0.04, y=1420 - 0)
        card(ctx, 'p4', f, 332, 372)
    elif lf < 72:
        il = lf - 42
        # ECU: one-handed? no: ONE clap, eyes still closed
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eout(pop(il, 0, 30)), 0, shake_at(il, [8], 16, 30), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffc8e4') if il < 8 else hx('ff5fa8')); ctx.fill()
        rays(ctx, 540, 1180, 200, 1700, il * 0.05, col=(1, 1, 1), a=0.3 if il < 8 else 0.55, n=18)
        cx, cy, R = 540, 820, 270
        face(ctx, MOM, P(eye='closed', mouth='flat', head=0), cx, cy, R, 0)
        u = eout(pop(il, 2, 8))
        gap = 330 * (1 - u) + 10
        if il < 8:
            mosquito(ctx, 540, 1180, 0.5, il, 0.0, f_=1)
        arm_to(ctx, -100, 1900, 540 - gap - 40, 1190, MOM['shirt'], MOM['skin'], bend=40, w=110)
        arm_to(ctx, 1180, 1900, 540 + gap + 40, 1190, MOM['shirt'], MOM['skin'], bend=-40, w=110)
        for sx in (-1, 1):
            ctx.save(); ctx.translate(540 + sx * (gap + 30), 1180); ctx.rotate(sx * 1.57); ctx.scale(-sx, 1)
            palm(ctx, 0, 0, 1.3, 0)
            ctx.restore()
        impact(ctx, 540, 1180, 260, pop(il, 8, 18), WHITE)
        ctx.restore()
        label(ctx, "*CLAP!*", 540, 1420, 170, YEL, -0.06, pop(il, 8, 11))
    elif lf < 100:
        il = lf - 72
        # palm opens: flat bug. "Goodnight."
        ctx.save(); cam(ctx, 540, 960, 1.05, 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd9ec')); ctx.fill()
        for k in range(5):
            ellipse(ctx, 540, 1080, 300 + k * 170, 300 + k * 170); setc(ctx, (1, 1, 1, 0.3)); ctx.set_line_width(30); ctx.stroke()
        face(ctx, MOM, P(eye='closed', mouth='smile', head=0), 540, 700, 200, -0.05)
        arm_to(ctx, 540, 1900, 540, 1180, MOM['shirt'], MOM['skin'], bend=0, w=110)
        palm(ctx, 540, 1150, 2.2, 0)
        mosquito(ctx, 540, 1100, 1.1, 0, 0.0, dead=True)
        sparkle(ctx, 300, 980, 30); sparkle(ctx, 790, 1040, 26)
        ctx.restore()
        label1(ctx, "\"Goodnight.\"", WHITE, pop(il, 4, 8), 130, -0.04, y=1440)
    else:
        il = lf - 100
        # Dad, jaw on the floor
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.1 * eout(pop(il, 0, 30)), 0, shake_at(il, [0], 10, 20), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd23f')); ctx.fill()
        rays(ctx, 540, 960, 260, 1700, il * 0.06, col=(1, 1, 1), a=0.5, n=18)
        cx, cy, R = 540, 960, 300
        b = {'head': (cx, cy - 0.06 * R), 'R': R * 0.95, 'eyeL': (cx - 0.2 * R, cy + 0.06 * R), 'eyeR': (cx + 0.42 * R, cy + 0.06 * R)}
        face(ctx, DAD, P(eye='shock', mouth='scream', head=0), cx, cy, R, 0)
        goggles(ctx, b)
        ctx.restore()
        label1(ctx, "\"...HOW?!\"", WHITE, pop(il, 2, 5), 150, -0.04, y=1420)


def s5(ctx, f):
    lf = f - 460
    if lf < 55:
        # lights off, both in bed. Dad finally smiles.
        bed_scene(ctx, f, False, 1.2, 440, 980, 0, 0)
        rect_r(ctx, 360, 1060, 250, 100, 45); fl(ctx, hx('b8c8e0'), 7)
        mom_sleeping(ctx, lf, 250, 1115, 72)
        face(ctx, DAD, P(eye='closed' if lf > 20 else 'happy', mouth='smile', head=0), 490, 1100, 86, -1.15)
        bed_scene_end(ctx, 0.25)
        label2(ctx, "\"Finally...", "PEACE.\"", WHITE, pop(lf, 6, 10), 116, col2=hx('9fe0ff'), y=1400)
        label(ctx, "*click*", 540, 640, 70, WHITE, 0.05, pop(lf, 0, 2) * (1 - pop(lf, 10, 14)))
    elif lf < 120:
        il = lf - 55
        # the window: a whole mosquito family flies in, formation, glowing
        ctx.save(); cam(ctx, 255, 760, 2.2 + 0.25 * eout(pop(il, 0, 65)), 0, 2 + shake_at(il, [30], 8, 12), f)
        bedroom(ctx, lights=False)
        rect_r(ctx, 95, 565, 320, 370, 16); setc(ctx, hx('122050')); ctx.fill()
        ellipse(ctx, 300, 680, 70, 70); setc(ctx, hx('fff2b0')); ctx.fill(); ellipse(ctx, 330, 660, 60, 60); setc(ctx, hx('122050')); ctx.fill()
        u = eout(pop(il, 4, 50))
        form = [(0, 0, 0.42), (-70, -55, 0.34), (70, -55, 0.34), (-140, -110, 0.26), (140, -110, 0.26), (0, -130, 0.2), (-40, 60, 0.18)]
        for k, (dx, dy, s) in enumerate(form):
            x = 255 + dx * (0.4 + 0.6 * u) + 6 * math.sin(il * 0.5 + k)
            y = 820 - 260 * (1 - u) + dy * (0.4 + 0.6 * u) + 6 * math.cos(il * 0.6 + k)
            mosquito(ctx, x, y, s * (0.5 + 0.6 * u), il + k, 0.0, glow=0.8)
        ctx.move_to(255, 565); ctx.line_to(255, 935); ctx.move_to(95, 750); ctx.line_to(415, 750); ink(ctx, 8); ctx.stroke()
        ctx.restore()
        label(ctx, "*BZZZZZZZZZZ!!*", 540, 1430, 120, YEL, -0.04, pop(il, 10, 14))
        card(ctx, 'p5', f, 517, 580)
    elif lf < 165:
        il = lf - 120
        # Dad ECU in the dark, swarm all around: "...honey?"
        ctx.save(); cam(ctx, 540, 980, 1.0 + 0.08 * eout(pop(il, 0, 45)), 0, 4, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, NIGHT); ctx.fill()
        cx, cy, R = 540, 1000, 290
        face(ctx, DAD, P(eye='shock', mouth='wavy', head=0), cx, cy, R, 0.03 * math.sin(il * 2))
        bloodshot(ctx, cx, cy, R, 1, seed=il // 3)
        sweat(ctx, cx - 0.95 * R, cy - 0.6 * R, il, 1.3); sweat(ctx, cx + 0.95 * R, cy - 0.4 * R, il + 40, 1.1)
        for k in range(7):
            mx, my = fly_path(il, 540, 900, 420, 420, 0.2, k * 0.9)
            mosquito(ctx, mx, my, 0.32, il + k, 0.1, glow=0.5, f_=1 if (k % 2) else -1)
        ctx.restore()
        label1(ctx, "\"...honey?\"", WHITE, pop(il, 6, 10), 130, -0.04, y=1420)
    elif lf < 186:
        il = lf - 165
        # Mom, asleep, rolls over, one flat palm up: "Your turn."
        ctx.save(); cam(ctx, 540, 960, 1.05, 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('2a2f6e')); ctx.fill()
        face(ctx, MOM, P(eye='closed', mouth='smile', head=0), 420, 900, 230, -0.2)
        zzz(ctx, 620, 720, il, 1.0)
        palm(ctx, 800, 1200, 1.5, 0.2)
        ctx.restore()
        label1(ctx, "\"Your turn.\"", WHITE, pop(il, 2, 5), 130, -0.04, y=1440)
    else:
        il = lf - 186
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 646)


SHOTS = [(0, s1), (90, s2), (200, s3), (330, s4), (460, s5)]
CUTS = (45, 90, 125, 143, 157, 169, 179, 187, 193, 200, 209, 218, 240, 300, 330, 372, 402, 430, 460, 515, 580, 625, 646)


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
                              "-i", "out/mosquito_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
