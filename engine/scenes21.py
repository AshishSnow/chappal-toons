"""'The Dog Ate My Homework' - original, general-audience comedy short, ~22s.
Kid forgot his homework -> plan: make the excuse TRUE. The dog sniffs it: NOPE. Peanut butter: licks it clean.
Wrapped round a sausage: eats the sausage, spits the paper onto the kid's face.
Then Dad puts down his big report - CHOMP, GULP, gone. Next morning Dad on the phone: "boss... the dog ate it."
"SURE IT DID." -> cut back to the kid's panic face (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import cam, pop, sparkle, puff, label, shake_at
import scenes13
from scenes13 import card as _card13

BOY, MOM, DAD = doodle.BOY, doodle.MOM_G, doodle.DAD
N = 660
FLOOR = 1500
KB, KD = 1.5, 1.75
BHIP, DHIP = FLOOR - 92 * KB, FLOOR - 92 * KD
KIDX = 300
DOGX, DOGS = 700, 1.25
TX0, TX1, TY = 760, 1180, 1290        # coffee table

CAPS = {
    'p1': [[("WHEN YOU ", OUT), ("FORGOT", hx('ff3b5c'))], [("YOUR HOMEWORK", OUT)]],
    'p2': [[("STEP 1: ", OUT), ("MAKE IT TRUE", hx('1f8bff'))]],
    'p3': [[("PLAN ", OUT), ("B", hx('ff8a1f'))]],
    'p4': [[("THEN DAD PUTS DOWN", OUT)], [("HIS ", OUT), ("BIG REPORT", hx('2fbf5a'))]],
    'p5': [[("DAD, ", OUT), ("NEXT MORNING", hx('8a3cff')), (":", OUT)]],
}
scenes13.CAPS = CAPS
card = _card13

DOGC, DOGD, DOGL = hx('f2b45a'), hx('c9782a'), hx('ffe0b0')


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


# ------------------------------------------------------------------ the dog (original design)
def dog(ctx, x, y, s, f, fr, look=1, mouth=0.0, tongue=0.0, eye='normal', tail=1.0, tilt=0.0, sniff=0.0, puffed=0.0):
    """sitting dog, faces +x when f=1. look=-1 turns the head away. returns world mouth point."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s * f, s)
    wag = math.sin(fr * 0.9) * tail
    # tail
    ctx.new_path(); ctx.move_to(-70, -50); ctx.curve_to(-130, -60, -150, -110 - 30 * wag, -130 + 25 * wag, -170 - 20 * wag)
    ink(ctx, 34); ctx.stroke_preserve(); setc(ctx, DOGC); ctx.set_line_width(20); ctx.stroke()
    # haunch + body
    ellipse(ctx, -30, -62, 82, 62); fl(ctx, DOGC, 6)
    ellipse(ctx, 15, -125, 72 + 10 * puffed, 108 + 6 * puffed); fl(ctx, DOGC, 6)
    ellipse(ctx, 40, -120, 36, 70); setc(ctx, DOGL); ctx.fill()
    ellipse(ctx, -25, -140, 30, 24, 0.3); setc(ctx, DOGD); ctx.fill()
    # back paw
    ellipse(ctx, -50, -10, 46, 16); fl(ctx, DOGC, 6)
    # front legs
    for lx in (18, 62):
        rect_r(ctx, lx - 17, -120, 34, 118, 16); fl(ctx, DOGC, 6)
        ellipse(ctx, lx + 8, -8, 28, 14); fl(ctx, DOGL, 6)
    # collar
    ellipse(ctx, 32, -195, 58, 16, 0.1); fl(ctx, hx('ff3b5c'), 6)
    ellipse(ctx, 55, -172, 13, 13); fl(ctx, hx('ffcc1f'), 4)
    # head
    hx_, hy_ = 48, -250
    ctx.save(); ctx.translate(hx_, hy_); ctx.rotate(tilt)
    if look < 0:
        ctx.scale(-1, 1)
    sn = math.sin(fr * 1.6) * 4 * sniff
    # back ear
    ctx.save(); ctx.translate(-30, -30); ctx.rotate(0.5 + 0.1 * wag)
    ellipse(ctx, 0, 40, 26, 52); fl(ctx, DOGD, 6); ctx.restore()
    ellipse(ctx, 0, 0, 80, 72); fl(ctx, DOGC, 6)
    ellipse(ctx, 64 + sn, 24, 54, 38); fl(ctx, DOGL, 6)
    ellipse(ctx, 112 + sn, 8, 19, 15); setc(ctx, INK); ctx.fill()
    ellipse(ctx, 107 + sn, 3, 6, 4); setc(ctx, (1, 1, 1)); ctx.fill()
    # eye + brow
    ex, ey = 28, -20
    if eye == 'normal':
        ellipse(ctx, ex, ey, 12, 16); setc(ctx, INK); ctx.fill()
        ellipse(ctx, ex - 3, ey - 6, 4, 5); setc(ctx, (1, 1, 1)); ctx.fill()
    elif eye == 'happy':
        ctx.new_path(); ctx.arc(ex, ey + 6, 13, math.pi * 1.1, math.pi * 1.9); ink(ctx, 7); ctx.stroke()
    elif eye == 'closed':
        ctx.new_path(); ctx.arc(ex, ey - 4, 13, math.pi * 0.1, math.pi * 0.9); ink(ctx, 7); ctx.stroke()
    elif eye == 'smug':
        ellipse(ctx, ex, ey, 12, 14); setc(ctx, INK); ctx.fill()
        ctx.new_path(); ctx.move_to(ex - 18, ey - 6); ctx.line_to(ex + 18, ey - 9); ink(ctx, 7); ctx.stroke()
    elif eye == 'shock':
        ellipse(ctx, ex, ey, 22, 25); fl(ctx, (1, 1, 1), 5)
        ellipse(ctx, ex + 2, ey + 2, 6, 7); setc(ctx, INK); ctx.fill()
    elif eye == 'hungry':
        ellipse(ctx, ex, ey, 22, 25); fl(ctx, (1, 1, 1), 5)
        poly(ctx, [(ex - 9, ey - 9), (ex + 9, ey - 9), (ex + 4, ey + 3), (ex + 9, ey + 14), (ex - 9, ey + 14), (ex - 4, ey + 3)]); setc(ctx, hx('2fbf5a')); ctx.fill()
    ctx.new_path(); ctx.move_to(ex - 16, ey - 34); ctx.curve_to(ex - 6, ey - 42, ex + 8, ey - 42, ex + 18, ey - 36); ink(ctx, 7); ctx.stroke()
    # mouth
    if mouth > 0:
        poly(ctx, [(42 + sn, 46), (118 + sn, 34), (104 + sn, 46 + 52 * mouth), (54 + sn, 50 + 40 * mouth)]); fl(ctx, hx('8a1c2c'), 6)
        ellipse(ctx, 80 + sn, 52 + 34 * mouth, 22, 10 * mouth + 2); setc(ctx, hx('ff6f86')); ctx.fill()
    else:
        ctx.new_path(); ctx.move_to(58 + sn, 48); ctx.curve_to(72 + sn, 60, 92 + sn, 58, 104 + sn, 42); ink(ctx, 6); ctx.stroke()
    if tongue > 0:
        tl = 30 + 40 * tongue
        rect_r(ctx, 70 + sn, 46, 34, tl, 16); fl(ctx, hx('ff6f86'), 5)
        ctx.move_to(87 + sn, 52); ctx.line_to(87 + sn, 40 + tl); setc(ctx, hx('e0485f')); ctx.set_line_width(4); ctx.stroke()
    # front ear
    ctx.save(); ctx.translate(-12, -40); ctx.rotate(0.3 + 0.15 * wag)
    ctx.new_path(); ctx.move_to(-20, 0); ctx.curve_to(-50, 50, -40, 110, -6, 112); ctx.curve_to(26, 100, 30, 40, 20, 0); ctx.close_path(); fl(ctx, DOGD, 6)
    ctx.restore()
    if sniff > 0:
        for k in range(3):
            tt = (fr * 0.12 + k / 3) % 1
            ctx.new_path(); ctx.arc(150 + 30 * tt, 8 - 26 * k + 10 * tt, 10 + 8 * tt, -1.0, 1.0); setc(ctx, INK + (0.7 * (1 - tt) * sniff,)); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()
    ctx.restore()
    mx = x + f * s * (hx_ + look * 90 + look * 0)
    return (mx, y + s * (hy_ + 50))


# ------------------------------------------------------------------ props
def paper(ctx, x, y, s=1.0, a=0.0, smear=0.0, shine=0.0, crumple=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    w, h = 150, 190
    if crumple > 0:
        pts = []
        for i in range(16):
            ang = i * 2 * math.pi / 16
            r = 70 + 14 * math.sin(i * 2.7)
            pts.append((math.cos(ang) * r * lerp(1.4, 1, crumple), math.sin(ang) * r * lerp(1.6, 1, crumple)))
        poly(ctx, pts); fl(ctx, (1, 1, 1), 6)
    else:
        poly(ctx, [(-w / 2, -h / 2), (w / 2 - 26, -h / 2), (w / 2, -h / 2 + 26), (w / 2, h / 2), (-w / 2, h / 2)]); fl(ctx, (1, 1, 1), 6)
        for k in range(6):
            yy = -h / 2 + 42 + k * 24
            ctx.move_to(-w / 2 + 14, yy); ctx.line_to(w / 2 - 12, yy)
        setc(ctx, hx('8fc4ff')); ctx.set_line_width(3); ctx.stroke()
        ctx.move_to(-w / 2 + 30, -h / 2 + 6); ctx.line_to(-w / 2 + 30, h / 2 - 6); setc(ctx, hx('ff8a9a')); ctx.set_line_width(3); ctx.stroke()
        if smear > 0:
            for k, (sx, sy, rx, ry) in enumerate(((-10, -30, 50, 24), (20, 10, 44, 20), (-20, 45, 40, 18))):
                ellipse(ctx, sx, sy, rx * smear, ry * smear, 0.3 * k); setc(ctx, hx('b5702c')); ctx.fill()
                ellipse(ctx, sx - 10, sy - 6, rx * 0.4 * smear, ry * 0.3 * smear, 0.3 * k); setc(ctx, hx('d99a55')); ctx.fill()
    ctx.restore()
    if shine > 0:
        for k in range(4):
            ang = k * 1.7 + shine * 3
            sparkle(ctx, x + math.cos(ang) * 110 * s, y + math.sin(ang) * 120 * s, 26 * s * (0.6 + 0.4 * math.sin(shine * 9 + k)))


def pb_jar(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rect_r(ctx, -60, -130, 120, 130, 22); fl(ctx, hx('c9823a'), 6)
    rect_r(ctx, -66, -160, 132, 40, 10); fl(ctx, hx('ff3b5c'), 6)
    rect_r(ctx, -48, -95, 96, 60, 8); fl(ctx, hx('fff2de'), 4)
    ellipse(ctx, 0, -65, 22, 18); setc(ctx, hx('c9823a')); ctx.fill()
    ctx.restore()


def knife(ctx, x, y, a, s=1.0, pb=True):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -12, 0, 24, 70, 10); fl(ctx, hx('3a3a4a'), 5)
    poly(ctx, [(-14, 0), (14, 0), (12, -110), (-4, -120), (-14, -100)]); fl(ctx, hx('d8dde8'), 5)
    if pb:
        ellipse(ctx, 0, -95, 16, 22); setc(ctx, hx('b5702c')); ctx.fill()
    ctx.restore()


def sausage(ctx, x, y, a=0.0, s=1.0, wrapped=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -120, -26, 240, 52, 26); fl(ctx, hx('d9573a'), 6)
    ctx.move_to(-80, -10); ctx.line_to(-40, -10); setc(ctx, (1, 1, 1, 0.5)); ctx.set_line_width(6); ctx.stroke()
    if wrapped > 0:
        w = 150 * wrapped
        rect_r(ctx, -w / 2, -42, w, 84, 6); fl(ctx, (1, 1, 1), 6)
        for k in range(3):
            ctx.move_to(-w / 2 + 10, -20 + k * 20); ctx.line_to(w / 2 - 10, -20 + k * 20)
        setc(ctx, hx('8fc4ff')); ctx.set_line_width(3); ctx.stroke()
        ctx.move_to(-w / 2 + 14, 42); ctx.line_to(-w / 2 + 24, -42); setc(ctx, INK); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def folder(ctx, x, y, a=0.0, s=1.0, glow=0.0, t=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if glow > 0:
        rays(ctx, 0, 0, 120, 330, t, a=0.5 * glow)
    rect_r(ctx, -120, -96, 90, 30, 8); fl(ctx, hx('1f6bd6'), 6)
    rect_r(ctx, -120, -80, 240, 160, 10); fl(ctx, hx('2f8bff'), 6)
    rect_r(ctx, -80, -38, 160, 56, 6); fl(ctx, (1, 1, 1), 4)
    text(ctx, "REPORT", 0, -10, 34, INK, outline=INK, ow=1, shadow=False)
    ctx.restore()


def bulb(ctx, x, y, t, s=1.0):
    if t <= 0:
        return
    k = s * (0.4 + 0.6 * eout(min(1, t * 2)))
    rays(ctx, x, y, 90 * k, 170 * k, t * 2, col=(1, 0.95, 0.4), a=0.8, n=10)
    ctx.save(); ctx.translate(x, y); ctx.scale(k, k)
    ellipse(ctx, 0, 0, 62, 66); fl(ctx, hx('ffe14d'), 6)
    rect_r(ctx, -28, 56, 56, 40, 8); fl(ctx, hx('b8bcc8'), 6)
    ctx.move_to(-14, 20); ctx.line_to(-6, -10); ctx.line_to(6, 20); ctx.line_to(14, -10); setc(ctx, hx('ff8a1f')); ctx.set_line_width(6); ctx.stroke()
    ellipse(ctx, -22, -24, 12, 18, 0.4); setc(ctx, (1, 1, 1, 0.7)); ctx.fill()
    ctx.restore()


def phone_ear(ctx, x, y, a=0.3):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    rect_r(ctx, -32, -70, 64, 140, 14); fl(ctx, hx('2a2a3a'), 6)
    rect_r(ctx, -24, -58, 48, 112, 8); setc(ctx, hx('6ad0ff')); ctx.fill()
    ctx.restore()


def bubble(ctx, x, y, w, h, tail_x, tail_y, s, col=(1, 1, 1)):
    rect_r(ctx, x - w / 2, y - h / 2, w, h, 40); setc(ctx, col); ctx.fill_preserve(); ink(ctx, 7); ctx.stroke()
    by = y - h / 2 + 4 if tail_y < y else y + h / 2 - 4
    poly(ctx, [(x - 40, by), (x + 30, by), (tail_x, tail_y)]); setc(ctx, col); ctx.fill_preserve(); ink(ctx, 7); ctx.stroke()
    rect_r(ctx, x - w / 2 + 5, y - h / 2 + 5, w - 10, h - 10, 34); setc(ctx, col); ctx.fill()
    text(ctx, s, x, y, 62, INK, outline=INK, ow=1, shadow=False)


# ------------------------------------------------------------------ set
def room(ctx, table=True):
    ctx.rectangle(-1500, -1500, 4200, 4200); setc(ctx, hx('ffd88a')); ctx.fill()
    for i in range(-10, 20):
        ctx.rectangle(i * 120, -400, 40, FLOOR + 400); setc(ctx, (1, 1, 1, 0.2)); ctx.fill()
    # window
    rect_r(ctx, 60, 560, 380, 420, 20); fl(ctx, hx('8fdcff'), 9)
    ellipse(ctx, 330, 660, 46, 46); setc(ctx, hx('fff27a')); ctx.fill()
    ctx.move_to(250, 560); ctx.line_to(250, 980); ctx.move_to(60, 770); ctx.line_to(440, 770); ink(ctx, 8); ctx.stroke()
    # framed doodle (original: paw print)
    rect_r(ctx, 640, 600, 220, 200, 10); fl(ctx, hx('ffffff'), 8)
    ellipse(ctx, 750, 720, 34, 30); setc(ctx, DOGD); ctx.fill()
    for px, py in ((712, 670), (742, 655), (772, 655), (800, 672)):
        ellipse(ctx, px, py, 12, 14); setc(ctx, DOGD); ctx.fill()
    # floor lamp
    ctx.move_to(1080, 860); ctx.line_to(1080, FLOOR - 10); ink(ctx, 10); ctx.stroke()
    poly(ctx, [(1010, 860), (1150, 860), (1120, 760), (1040, 760)]); fl(ctx, hx('ff8a5c'), 7)
    # floor + rug
    ctx.rectangle(-1500, FLOOR, 4200, 900); setc(ctx, hx('c98f5a')); ctx.fill()
    for i in range(-14, 26):
        ctx.move_to(i * 140, FLOOR); ctx.line_to(i * 140 - 60, FLOOR + 900); setc(ctx, (0, 0, 0, 0.1)); ctx.set_line_width(5); ctx.stroke()
    ellipse(ctx, 520, FLOOR + 60, 520, 70); fl(ctx, hx('ff6f9a'), 7)
    ellipse(ctx, 520, FLOOR + 60, 400, 46); setc(ctx, hx('ff9fbd')); ctx.fill()
    ctx.move_to(-1500, FLOOR); ctx.line_to(2700, FLOOR); ink(ctx, 8); ctx.stroke()
    if table:
        coffee_table(ctx)


def coffee_table(ctx):
    for lx in (TX0 + 30, TX1 - 60):
        ctx.rectangle(lx, TY + 30, 30, FLOOR - TY - 20); fl(ctx, hx('8a5a34'), 6)
    rect_r(ctx, TX0, TY, TX1 - TX0, 40, 10); fl(ctx, hx('b97a44'), 7)


# ------------------------------------------------------------------ shots
def kid(ctx, x=KIDX, **kw):
    p = P(**kw)
    return draw_hip(ctx, x, BHIP, KB, 1, BOY, p)


def panic_shot(ctx, f, lf):
    """opening / loop: ECU kid, panic, holding blank homework"""
    ctx.save(); cam(ctx, KIDX + 80, 980, 2.3, -5 + 2 * math.sin(lf * 0.3), shake_at(lf, [0], 10, 14), f)
    room(ctx)
    h = kid(ctx, rsh=150, rel=-30, lsh=-40, lel=-120, eye='shock', mouth='scream', head=-6 + 3 * math.sin(lf * 0.9), torso=-4)
    fx, fy = h['front']
    paper(ctx, fx + 60, fy - 40, 1.0, 0.2 + 0.04 * math.sin(lf * 1.3))
    hx_, hy_ = h['head']
    for k in range(3):
        ctx.new_path(); ctx.arc(hx_ - 130 + k * 20, hy_ - 120 - k * 10, 14, 0, 2 * math.pi)
    ellipse(ctx, hx_ - 170, hy_ - 40 + (lf * 4) % 60, 12, 18); fl(ctx, hx('8fdcff'), 4)
    ctx.restore()


def s1(ctx, f):
    if f < 44:
        panic_shot(ctx, f, f)
        label(ctx, "DUE TOMORROW?!", 540, 1450, 98, hx('ff3b5c'), -0.04, 1)
    else:
        lf = f - 44
        u = eout(pop(lf, 26, 40))
        ctx.save(); cam(ctx, lerp(380, 520, u), lerp(1060, 1120, u), lerp(1.65, 1.0, u), lerp(-3, 0, u), shake_at(lf, [4], 8, 10), f)
        room(ctx)
        h = kid(ctx, rsh=40, rel=-30, lsh=-150, lel=10, eye='smug', mouth='grin', head=4, torso=-3)
        fx, fy = h['front']
        paper(ctx, fx + 40, fy - 10, 0.8, 0.3)
        hx_, hy_ = h['head']
        bulb(ctx, hx_ - 30, hy_ - 300, pop(lf, 4, 14), 0.9)
        dog(ctx, DOGX, FLOOR, DOGS, -1, f, eye='happy', mouth=0.6, tongue=0.6, tail=1)
        ctx.restore()
        if lf < 30:
            label(ctx, "IDEA!", 540, 1450, 150, hx('ffe14d'), -0.05, pop(lf, 4, 8))
        else:
            label(ctx, "\"THE DOG ATE IT!\"", 540, 1450, 104, (1, 1, 1), 0.03, pop(lf, 32, 36))
    card(ctx, 'p1', f, -6, 110)


def s2(ctx, f):
    lf = f - 110
    if lf < 66:
        # offer -> sniff -> NOPE (low angle two-shot)
        nope = lf >= 34
        ctx.save(); cam(ctx, 520, 1180, 1.55, 2, shake_at(lf, [34], 8, 10), f)
        room(ctx)
        reach = eout(pop(lf, 0, 8))
        h = kid(ctx, x=KIDX + 10, rsh=lerp(40, 92, reach), rel=-10, lsh=-20, lel=-40, eye='happy' if not nope else 'shock',
                mouth='grin' if not nope else 'open', torso=8, head=2)
        fx, fy = h['front']
        paper(ctx, fx + 70, fy - 20, 0.75, 0.1)
        dog(ctx, DOGX, FLOOR, DOGS, -1, f, look=-1 if nope else 1, eye='closed' if nope else 'normal',
            sniff=1 if 8 <= lf < 34 else 0, tail=0.2 if nope else 0.6, tilt=-0.15 if nope else 0.1)
        ctx.restore()
        if lf < 34:
            label(ctx, "SNIFF SNIFF...", 540, 1450, 104, (1, 1, 1), 0.03, pop(lf, 8, 12))
        else:
            label(ctx, "NOPE.", 540, 1450, 150, hx('ff3b5c'), -0.05, pop(lf, 34, 38))
    elif lf < 96:
        # insert: peanut butter smear on the homework
        il = lf - 66
        ctx.save(); cam(ctx, 540, 1000, 1.0, 0, shake_at(il, [2], 6, 8), f)
        ctx.rectangle(-1000, -1000, 3000, 4000); setc(ctx, hx('ffd88a')); ctx.fill()
        rays(ctx, 540, 900, 150, 900, il * 0.02, col=(1, 1, 1), a=0.35, n=16)
        paper(ctx, 520, 930, 2.3, -0.06, smear=eout(pop(il, 4, 22)))
        pb_jar(ctx, 860, 1250, 1.3)
        kx = lerp(700, 380, pop(il, 4, 22))
        knife(ctx, kx, 900 + 40 * math.sin(il * 0.9), 1.9, 1.6)
        ctx.restore()
        label(ctx, "+ PEANUT BUTTER", 540, 1450, 104, hx('e0903a'), 0.03, pop(il, 2, 6))
    else:
        # dog licks it spotless
        il = lf - 96
        clean = pop(il, 4, 38)
        ctx.save(); cam(ctx, 520, 1200, kf(il, [(0, 1.7), (54, 1.9)], eout), -3, 0, f)
        room(ctx)
        h = kid(ctx, x=KIDX + 10, rsh=92, rel=-10, lsh=-20, lel=-40, eye='happy' if il < 40 else 'shock', mouth='grin' if il < 40 else 'scream', torso=8)
        fx, fy = h['front']
        dog(ctx, DOGX - 30, FLOOR, DOGS, -1, f, mouth=0.5 if il < 40 else 0, tongue=(0.5 + 0.5 * math.sin(il * 1.4)) if il < 40 else 0,
            eye='happy' if il < 40 else 'smug', tail=1.2, tilt=0.12 * math.sin(il * 1.4) if il < 40 else -0.1)
        paper(ctx, fx + 70, fy - 20, 0.75, 0.1, smear=1 - clean, shine=pop(il, 38, 54) * (1 if il >= 38 else 0))
        ctx.restore()
        if il < 38:
            label(ctx, "SLURP SLURP", 540, 1450, 110, hx('ff6f86'), 0.03 * (-1) ** (il // 8), pop(il, 2, 6))
        else:
            label(ctx, "LICKED IT CLEAN.", 540, 1450, 100, (1, 1, 1), -0.03, pop(il, 38, 42))
    card(ctx, 'p2', f, 114, 260)


def s3(ctx, f):
    lf = f - 260
    if lf < 34:
        # insert: wrap the paper round a sausage
        ctx.save(); cam(ctx, 540, 1000, 1.0, 3 * math.sin(lf * 0.2), 0, f)
        ctx.rectangle(-1000, -1000, 3000, 4000); setc(ctx, hx('a8ecd0')); ctx.fill()
        rays(ctx, 540, 960, 150, 900, lf * 0.02, col=(1, 1, 1), a=0.35, n=16)
        sausage(ctx, 540, 960, -0.15, 2.4, wrapped=eout(pop(lf, 4, 18)))
        ctx.restore()
        label(ctx, "SAUSAGE DISGUISE", 540, 1450, 100, hx('ff8a1f'), -0.03, pop(lf, 2, 6))
    elif lf < 84:
        # toss -> dog leaps -> CHOMP
        il = lf - 34
        ctx.save(); cam(ctx, 540, 1100, 1.05, 0, shake_at(il, [16], 10, 18), f)
        room(ctx)
        h = kid(ctx, rsh=lerp(120, 30, eout(pop(il, 0, 8))), rel=-20, lsh=-20, lel=-40, eye='happy', mouth='grin', torso=-6)
        jump = math.sin(math.pi * pop(il, 8, 26))
        mp = dog(ctx, DOGX, FLOOR - 220 * jump, DOGS, -1, f, mouth=1.0 if il < 16 else 0.3 * (il % 8 < 4), eye='hungry' if il < 16 else 'happy', tail=1.5)
        if il < 16:
            t = pop(il, 4, 16)
            sausage(ctx, lerp(h['front'][0] + 60, mp[0], t), lerp(h['front'][1], mp[1], t) - 260 * math.sin(math.pi * t), il * 0.4, 0.8)
        else:
            sausage(ctx, mp[0] - 20, mp[1] + 10, 0.3, 0.75)
        ctx.restore()
        if il < 16:
            label(ctx, "FETCH!", 540, 1450, 140, (1, 1, 1), 0.04, pop(il, 2, 6))
        elif il < 30:
            label(ctx, "CHOMP!", 540, 1450, 150, hx('ffe14d'), -0.05, pop(il, 16, 20))
        else:
            label(ctx, "CHEW... CHEW...", 540, 1450, 100, (1, 1, 1), 0.03, pop(il, 30, 34))
    else:
        # PTOO: paper flies back and sticks to kid's face
        il = lf - 84
        if il < 14:
            ctx.save(); cam(ctx, 520, 1150, 1.4, 0, shake_at(il, [0], 8, 12), f)
            room(ctx)
            h = kid(ctx, eye='shock', mouth='open', lsh=-20, lel=-30, rsh=20, rel=-30)
            mp = dog(ctx, DOGX, FLOOR, DOGS, -1, f, mouth=1, eye='closed', tail=0.5, puffed=1 - pop(il, 0, 4))
            t = pop(il, 2, 14)
            paper(ctx, lerp(mp[0], h['head'][0], t), lerp(mp[1], h['head'][1], t) - 120 * math.sin(math.pi * t), 0.6, il * 0.6, crumple=1 - t)
            ctx.restore()
            label(ctx, "PTOO!", 540, 1450, 150, hx('9bdc4a'), 0.05, pop(il, 1, 5))
        else:
            jl = il - 14
            ctx.save(); cam(ctx, KIDX + 30, 940, 2.2, 4, shake_at(jl, [0], 10, 20), f)
            room(ctx)
            h = kid(ctx, eye='shock', mouth='flat', lsh=-60, lel=-110, rsh=-60, rel=-110, torso=-8, head=-4)
            hx_, hy_ = h['head']
            paper(ctx, hx_ + 10, hy_ + 10, 1.45, -0.12)
            for k in range(3):
                dy = ((jl * 3 + k * 30) % 90)
                ellipse(ctx, hx_ - 60 + k * 60, hy_ + 150 + dy, 9, 14); fl(ctx, hx('c8f0ff'), 3)
            ctx.restore()
            label(ctx, "SPLAT.", 540, 1450, 150, (1, 1, 1), -0.04, pop(jl, 0, 4))
    card(ctx, 'p3', f, 264, 400)


def s4(ctx, f):
    lf = f - 400
    if lf < 44:
        # dad places the report on the coffee table
        ctx.save(); cam(ctx, 760, 1100, 1.1, 0, 0, f)
        room(ctx)
        dog(ctx, 520, FLOOR, DOGS, 1, f, eye='normal', tail=0.4)
        set_down = eout(pop(lf, 10, 22))
        ph = lf * 0.45 if lf < 12 or lf > 30 else 0
        dx = lerp(1250, 1000, eout(pop(lf, 0, 12))) if lf <= 30 else lerp(1000, 1350, ein(pop(lf, 30, 44)))
        s_ = math.sin(ph)
        h = draw_hip(ctx, dx, DHIP - 6 * abs(s_), KD, -1 if lf <= 30 else 1, DAD,
                     P(rsh=lerp(60, 30, set_down), rel=lerp(70, -10, set_down), lsh=-10, lel=-20, eye='normal', mouth='smile', torso=lerp(3, 18, set_down) if lf <= 30 else 3,
                       lhip=20 * s_, rhip=-20 * s_, lkn=-20 * max(0, s_), rkn=-20 * max(0, -s_)))
        if lf < 18:
            fx, fy = h['front']
            folder(ctx, fx - 40, fy - 30, -0.1, 0.8)
        else:
            folder(ctx, 930, TY - 50, 0, 0.8, glow=pop(lf, 22, 30) * (1 - pop(lf, 36, 44)), t=lf * 0.03)
        ctx.restore()
        label(ctx, "\"SUPER IMPORTANT.\"", 540, 1450, 96, (1, 1, 1), 0.03, pop(lf, 12, 16))
    elif lf < 88:
        il = lf - 44
        if il < 12:
            # ECU dog eyes lock on
            ctx.save(); cam(ctx, 600, 1240, 2.6, -6, 0, f)
            room(ctx)
            folder(ctx, 930, TY - 50, 0, 0.8, glow=1, t=il * 0.05)
            dog(ctx, 520, FLOOR, DOGS, 1, f, eye='hungry', mouth=0.4, tongue=0.8, tail=1.5)
            ctx.restore()
            label(ctx, "!!!", 540, 1450, 160, hx('ff3b5c'), 0, pop(il, 0, 3))
        else:
            jl = il - 12
            ctx.save(); cam(ctx, 760, 1180, 1.35, 0, shake_at(jl, [4, 20], 10, 22), f)
            room(ctx)
            dx = lerp(520, 800, eout(pop(jl, 0, 5))) if jl < 20 else lerp(800, 560, eout(pop(jl, 20, 30)))
            jump = math.sin(math.pi * pop(jl, 0, 8)) * 0.6
            mp = dog(ctx, dx, FLOOR - 120 * jump, DOGS, 1, f, mouth=0.9 if jl < 4 else (0.4 if jl < 20 else 0),
                     eye='hungry' if jl < 4 else ('closed' if jl < 30 else 'happy'), tail=2, puffed=pop(jl, 4, 12) * (1 - pop(jl, 20, 26)))
            if jl < 4:
                folder(ctx, 930, TY - 50, 0, 0.8)
            elif jl < 20:
                folder(ctx, mp[0] + 20, mp[1] + 10, 0.4 + 0.1 * math.sin(jl * 2), 0.8 * (1 - 0.6 * pop(jl, 8, 20)))
            if jl >= 26:
                for k in range(3):
                    sparkle(ctx, 640 + k * 120, 1040 - k * 40, 22 + 8 * math.sin(jl * 0.5 + k), hx('fff27a'))
            ctx.restore()
            if jl < 20:
                label(ctx, "CHOMP!", 540, 1450, 150, hx('ffe14d'), -0.05, pop(jl, 4, 8))
            else:
                label(ctx, "GULP.", 540, 1450, 150, (1, 1, 1), 0.05, pop(jl, 20, 24))
    else:
        # kid, outraged
        il = lf - 88
        ctx.save(); cam(ctx, KIDX + 30, 960, 2.0, 5, shake_at(il, [0], 8, 14), f)
        room(ctx)
        h = kid(ctx, eye='glare', mouth='scream', lsh=-150, lel=-20, rsh=-150, rel=20, torso=-4)
        ctx.restore()
        label(ctx, "SERIOUSLY?!", 540, 1450, 140, hx('ff3b5c'), -0.04, pop(il, 2, 6))
    card(ctx, 'p4', f, 404, 530)


def dad_phone(ctx, f, lf, eye, mouth, sweat=1.0):
    h = draw_hip(ctx, 560, DHIP, KD, -1, DAD, P(rsh=160, rel=-150, lsh=-10, lel=-20, eye=eye, mouth=mouth, head=-6, torso=-2))
    hx_, hy_ = h['head']
    phone_ear(ctx, hx_ + 175, hy_ + 10, 0.25)
    if sweat:
        for k in range(2):
            dy = (lf * 3 + k * 40) % 80
            ellipse(ctx, hx_ - 150 + k * 300, hy_ - 60 + dy, 14, 22); fl(ctx, hx('8fdcff'), 4)
    return h


def s5(ctx, f):
    lf = f - 530
    if lf < 50:
        ctx.save(); cam(ctx, 600, 920, 1.75, -3, 0, f)
        room(ctx, table=False)
        dad_phone(ctx, f, lf, 'normal', 'wavy')
        ctx.restore()
        label(ctx, "\"UH, BOSS...\"", 540, 1310, 84, (1, 1, 1), 0.03, pop(lf, 4, 8))
        label(ctx, "\"THE DOG ATE IT.\"", 540, 1450, 96, hx('ffe14d'), -0.03, pop(lf, 22, 26))
        card(ctx, 'p5', f, 534, 590)
    elif lf < 96:
        # split screen: dad (top) / smug dog (bottom), phone bubble in the middle
        il = lf - 50
        ctx.save(); ctx.rectangle(0, 0, W, H / 2); ctx.clip()
        ctx.save(); cam(ctx, 760, 1200, 1.45, 0, shake_at(il, [10], 10, 14), f)
        room(ctx, table=False)
        dad_phone(ctx, f, il, 'shock' if il >= 10 else 'normal', 'scream' if il >= 10 else 'wavy')
        ctx.restore(); ctx.restore()
        ctx.save(); ctx.rectangle(0, H / 2, W, H / 2); ctx.clip()
        ctx.save(); cam(ctx, 600, 1160, 1.55, 0, 0, f)
        ctx.translate(0, 120 / 1.55)
        room(ctx)
        dog(ctx, 540, FLOOR, DOGS, 1, f, eye='smug', mouth=0, tail=1.5)
        ctx.restore(); ctx.restore()
        ctx.rectangle(0, H / 2 - 9, W, 18); setc(ctx, INK); ctx.fill()
        bubble(ctx, 790, 640, 480, 130, 650, 420, "SURE IT DID.", col=hx('fff2de')) if il >= 6 else None
        label(ctx, "*WAG WAG*", 540, 1450, 120, hx('ffe14d'), 0.04, pop(il, 18, 22))
    else:
        il = lf - 96
        panic_shot(ctx, f, il)
        label(ctx, "DUE TOMORROW?!", 540, 1450, 98, hx('ff3b5c'), -0.04, pop(il, 0, 4))
        card(ctx, 'p1', f, 626)


SHOTS = [(0, s1), (110, s2), (260, s3), (400, s4), (530, s5)]
CUTS = (44, 110, 176, 206, 260, 294, 344, 358, 400, 444, 456, 488, 530, 580, 626)


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
            render(f).write_to_png(f'out/w{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/dog_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
