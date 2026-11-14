"""'Mom's Phone Voice' - original, general-audience comedy short, ~22s.
Hook: ECU of Mom mid-yell, red, steam: "CLEAN YOUR ROOM!!!" - *RING RING* - instant pastel angel: "Hellooo? Oh, HIII!"
Beat 1: wide - "Oh, the kids are ANGELS!" while behind her the kid's ball smashes the vase. Phone covered, whip: "I. SAW. THAT."
Beat 2: split face - left half sweet (to the phone), right half demon (to the kid); then the switching gets faster and faster. "LOVE YOU, BYE!" *CLICK*
Beat 3: call ends - dark low angle, slow turn: "NOW... WHERE WAS I?" - kid gulps.
Twist: the kid holds up a tablet: "GRANDMA'S ON VIDEO CALL!" - Mom instantly flips back to angel: "MOM! HIII!" - kid winks.
Loops to the opening yell."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
import scenes32
from scenes32 import label, cam, rect_r, rays, face, eye_pos, living
import scenes13
from scenes13 import card as _card13
import random

BOY = doodle.BOY
MOM = doodle.MOM_G
GRAN = dict(doodle.NMOM, hair=hx('dcdce6'), shirt=hx('ff8ac0'), glasses=hx('8a3cff'))
N = 660
FLOOR = 1460
RED = hx('ff3b5c')
BLUE = hx('1f8bff')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
LY = 1450

CAPS = {
    'p1': [[("WHEN MOM IS YELLING", OUT)], [("AND THE PHONE RINGS", RED)]],
    'p2': [[("THE PHONE VOICE:", OUT)], [("ACTIVATED", PINK)]],
    'p3': [[("SWITCHING SPEED:", OUT)], [("0.1 SECONDS", ORANGE)]],
    'p4': [[("THE CALL ENDS.", OUT)], [("SHE REMEMBERS.", RED)]],
    'p5': [[("PLOT TWIST:", OUT)], [("THE KID HAS A SECRET WEAPON", GREEN)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ fx helpers
def heart(ctx, x, y, r, col=hx('ff6fae'), a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(r / 50, r / 50)
    ctx.new_path(); ctx.move_to(0, 40)
    ctx.curve_to(-70, -5, -45, -60, 0, -25); ctx.curve_to(45, -60, 70, -5, 0, 40); ctx.close_path()
    fl(ctx, col, 7)
    ctx.restore()


def steam(ctx, x, y, lf, s=1.0, side=1):
    for k in range(3):
        ph = ((lf * 1.4 + k * 12) % 36) / 36
        px = x + side * (40 * ph + 30 * math.sin(lf * 0.3 + k)) * s
        py = y - 200 * ph * s
        r = (30 + 50 * ph) * s
        ellipse(ctx, px, py, r, r * 0.85); fl(ctx, (1, 1, 1, 1 - 0.6 * ph), 6 * s)


def vein(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for a in (0.785, 2.356, 3.927, 5.498):
        ctx.new_path(); ctx.move_to(math.cos(a) * 12, math.sin(a) * 12)
        ctx.curve_to(math.cos(a - 0.4) * 30, math.sin(a - 0.4) * 30, math.cos(a + 0.4) * 34, math.sin(a + 0.4) * 34, math.cos(a) * 46, math.sin(a) * 46)
        setc(ctx, OUT); ctx.set_line_width(20); ctx.stroke_preserve(); setc(ctx, hx('ff2a4a')); ctx.set_line_width(11); ctx.stroke()
    ctx.restore()


def phone_at_ear(ctx, cx, cy, Rt, side=-1, covered=False):
    """a big phone pressed to the ear on the given side (-1 = screen-left)"""
    px, py = cx + side * 0.98 * Rt, cy + 0.12 * Rt
    ctx.save(); ctx.translate(px, py); ctx.rotate(side * 0.22)
    rect_r(ctx, -0.17 * Rt, -0.42 * Rt, 0.34 * Rt, 0.84 * Rt, 0.07 * Rt); fl(ctx, hx('24243a'), Rt * 0.03)
    rect_r(ctx, -0.13 * Rt, -0.36 * Rt, 0.26 * Rt, 0.7 * Rt, 0.04 * Rt); setc(ctx, hx('6be2ff')); ctx.fill()
    ellipse(ctx, side * -0.05 * Rt, 0.18 * Rt, 0.2 * Rt, 0.14 * Rt); fl(ctx, MOM['skin'], Rt * 0.03)     # fingers
    if covered:
        ellipse(ctx, 0, -0.3 * Rt, 0.2 * Rt, 0.16 * Rt); fl(ctx, MOM['skin'], Rt * 0.03)               # palm over the mic
    ctx.restore()


def blush(ctx, cx, cy, Rt):
    for ex, ey, rx in eye_pos(cx, cy, Rt):
        ellipse(ctx, ex + (-1 if ex < cx else 1) * 0.06 * Rt, ey + 0.26 * Rt, 0.13 * Rt, 0.07 * Rt); setc(ctx, (1, 0.45, 0.6, 0.6)); ctx.fill()


def sweet_bg(ctx, lf, cx=540, cy=1000):
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd1ea')); ctx.fill()
    rays(ctx, cx, cy, 260, 1600, lf * 0.02, col=(1, 1, 1), a=0.55, n=18)
    rnd = random.Random(3)
    for k in range(9):
        x0, y0 = rnd.uniform(80, 1000), rnd.uniform(500, 1500)
        heart(ctx, x0 + 20 * math.sin(lf * 0.1 + k), y0 - (lf * 2 + k * 40) % 200, rnd.uniform(28, 46), hx('ff8ac0'), 0.2 * math.sin(lf * 0.1 + k))
    for k in range(5):
        sparkle(ctx, cx + 420 * math.cos(lf * 0.08 + k * 1.25), cy + 380 * math.sin(lf * 0.08 + k * 1.25), 30, (1, 1, 1))


def angry_bg(ctx, lf, cx=540, cy=1000):
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('e0263a')); ctx.fill()
    rays(ctx, cx, cy, 260, 1600, -lf * 0.05, col=(1, 0.75, 0.2), a=0.45, n=18)


def sweet_face(ctx, cx, cy, Rt, lf, rot=0.0, phone=True):
    face(ctx, MOM, P(eye='happy', mouth='grin', head=0), cx, cy, Rt, rot)
    blush(ctx, cx, cy, Rt)
    if phone:
        phone_at_ear(ctx, cx, cy, Rt, -1)


def angry_face(ctx, cx, cy, Rt, lf, rot=0.0, mouth='scream', phone=False, covered=False):
    face(ctx, MOM, P(eye='glare', mouth=mouth, head=0), cx, cy, Rt, rot)
    vein(ctx, cx + 0.45 * Rt, cy - 0.62 * Rt, Rt / 300)
    steam(ctx, cx - 0.9 * Rt, cy - 0.4 * Rt, lf, Rt / 300, -1)
    steam(ctx, cx + 0.9 * Rt, cy - 0.4 * Rt, lf + 9, Rt / 300, 1)
    if phone:
        phone_at_ear(ctx, cx, cy, Rt, -1, covered)


# ------------------------------------------------------------------ props
def table_phone(ctx, x, y, lf, ringing=True):
    jx = 6 * math.sin(lf * 3.1) if ringing else 0
    ctx.save(); ctx.translate(x + jx, y); ctx.rotate(0.05 * math.sin(lf * 2.3) if ringing else 0)
    rect_r(ctx, -150, -270, 300, 540, 40); fl(ctx, hx('24243a'), 9)
    rect_r(ctx, -125, -240, 250, 470, 24); setc(ctx, hx('3ccf4e') if (lf // 5) % 2 else hx('6be2ff')); ctx.fill()
    # caller avatar: a simple heart + the word MOM? no - keep it textless: a big round avatar + green answer button
    ellipse(ctx, 0, -90, 70, 70); fl(ctx, (1, 1, 1), 6)
    ellipse(ctx, 0, -110, 26, 26); setc(ctx, hx('9aa0b8')); ctx.fill()
    ellipse(ctx, 0, -50, 46, 28); setc(ctx, hx('9aa0b8')); ctx.fill()
    ellipse(ctx, 0, 150, 48, 48); fl(ctx, (1, 1, 1), 6)
    ctx.restore()
    if ringing:
        for k in range(3):
            r = 200 + k * 60 + 15 * math.sin(lf * 0.8)
            for sgn in (-1, 1):
                ctx.new_path(); ctx.arc(x, y, r, (0 if sgn > 0 else math.pi) - 0.45, (0 if sgn > 0 else math.pi) + 0.45)
                setc(ctx, OUT); ctx.set_line_width(20); ctx.stroke_preserve(); setc(ctx, hx('fff27a')); ctx.set_line_width(10); ctx.stroke()


def vase(ctx, x, y, broken=0.0, lf=0):
    """vase on a pedestal; broken>0 -> shards fly"""
    ctx.rectangle(x - 70, y, 140, FLOOR - y); fl(ctx, hx('f4e6c8'), 8)
    ctx.rectangle(x - 95, y - 10, 190, 26); fl(ctx, hx('e0cfa8'), 7)
    if broken <= 0:
        ctx.new_path(); ctx.move_to(x - 40, y - 10); ctx.curve_to(x - 110, y - 120, x - 50, y - 200, x - 30, y - 240)
        ctx.line_to(x + 30, y - 240); ctx.curve_to(x + 50, y - 200, x + 110, y - 120, x + 40, y - 10); ctx.close_path()
        fl(ctx, hx('2fb8ff'), 8)
        ctx.new_path(); ctx.move_to(x - 70, y - 120); ctx.line_to(x + 70, y - 120); setc(ctx, (1, 1, 1)); ctx.set_line_width(14); ctx.stroke()
        for k, col in enumerate((hx('ff5fa8'), hx('ffd23f'), hx('ff8a1f'))):
            fx_, fy_ = x - 50 + k * 50, y - 300 - 20 * (k % 2)
            ctx.move_to(x, y - 230); ctx.line_to(fx_, fy_); setc(ctx, hx('22b45a')); ctx.set_line_width(8); ctx.stroke()
            for j in range(5):
                a = j * 2 * math.pi / 5
                ellipse(ctx, fx_ + math.cos(a) * 18, fy_ + math.sin(a) * 18, 14, 14); fl(ctx, col, 4)
    else:
        rnd = random.Random(11)
        for k in range(10):
            ang = rnd.uniform(-2.8, -0.3); sp = rnd.uniform(300, 700)
            u = broken
            px = x + math.cos(ang) * sp * u; py = y - 120 + math.sin(ang) * sp * u + 900 * u * u
            py = min(py, FLOOR - 20)
            ctx.save(); ctx.translate(px, py); ctx.rotate(k + u * 8)
            poly(ctx, [(-30, -20), (30, -26), (12, 26)]); fl(ctx, hx('2fb8ff'), 6)
            ctx.restore()


def ball(ctx, x, y, r=48, spin=0):
    ellipse(ctx, x, y, r, r); fl(ctx, (1, 1, 1), 7)
    ctx.save(); ctx.translate(x, y); ctx.rotate(spin)
    for a in range(5):
        aa = a * 2 * math.pi / 5
        ellipse(ctx, math.cos(aa) * r * 0.55, math.sin(aa) * r * 0.55, r * 0.22, r * 0.22); setc(ctx, OUT); ctx.fill()
    ctx.restore()


def tablet(ctx, x, y, s, lf, gran_wave=True):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rect_r(ctx, -230, -170, 460, 340, 34); fl(ctx, hx('24243a'), 9)
    ctx.save(); rect_r(ctx, -205, -145, 410, 290, 18); ctx.clip()
    ctx.rectangle(-210, -150, 420, 300); setc(ctx, hx('b9f0ff')); ctx.fill()
    face(ctx, GRAN, P(eye='happy', mouth='grin', head=0), 0, 30, 120, 0.12 * math.sin(lf * 0.35))
    # waving hand
    wx = 140 + 14 * math.sin(lf * 0.6)
    ellipse(ctx, wx, 30, 40, 48); fl(ctx, GRAN['skin'], 5)
    ctx.restore()
    ellipse(ctx, 160, -110, 12, 12); setc(ctx, hx('ff3b5c')); ctx.fill()   # live dot
    ctx.restore()


# ------------------------------------------------------------------ shots
def opening_face(ctx, f, lf, lab=True):
    """ECU: Mom mid-yell"""
    sh = shake_at(lf, [0], 12, 24) + 4
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(lf, 0, 44)), 0, sh, f)
    angry_bg(ctx, lf)
    cx, cy, Rt = 540 + 6 * math.sin(lf * 2.4), 1010, 320
    angry_face(ctx, cx, cy, Rt, lf, 0.03 * math.sin(lf * 0.9))
    ctx.restore()
    if lab:
        label(ctx, "\"CLEAN YOUR ROOM!!!\"", 540, LY, 112, (1, 1, 1), -0.04, pop(lf, 0, 4) if lf > 0 else 1)


def s1(ctx, f):
    if f < 44:
        opening_face(ctx, f, f)
    elif f < 62:
        lf = f - 44
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.04 * pop(lf, 0, 18), -6, 3, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('2b3a8a')); ctx.fill()
        rays(ctx, 540, 1000, 200, 1500, lf * 0.05, col=(1, 1, 1), a=0.25, n=16)
        table_phone(ctx, 540, 1000, lf)
        ctx.restore()
        label(ctx, "*RING RING*", 540, LY, 116, hx('fff27a'), 0.04, pop(lf, 0, 4))
    else:
        lf = f - 62
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 48)), 0, shake_at(lf, [0], 6, 10), f)
        sweet_bg(ctx, lf)
        sweet_face(ctx, 540, 1000, 320, lf, 0.08 * math.sin(lf * 0.12))
        ctx.restore()
        label(ctx, "\"Hellooo? Oh, HIII!\"", 540, LY, 108, hx('ff5fa8'), -0.03, pop(lf, 2, 6))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 56:
        hit = 34
        ctx.save(); cam(ctx, 540, 1060, 1.0 + 0.04 * eout(pop(lf, 0, 56)), 0, shake_at(lf, [hit], 12, 22), f)
        living(ctx, lights=True)
        # vase between them
        vase(ctx, 560, 1180, 0 if lf < hit else pop(lf, hit, hit + 22), lf)
        # kid juggling a ball, then it flies
        kp = P(eye='happy' if lf < hit else 'shock', mouth='grin' if lf < hit else 'scream', rsh=150 if lf < hit - 6 else 100, rel=-40,
               lsh=40, lel=-60, rhip=-30 * abs(math.sin(lf * 0.4)) if lf < hit - 6 else -6, rkn=40 * abs(math.sin(lf * 0.4)) if lf < hit - 6 else -4)
        draw_hip(ctx, 860, FLOOR - 160, 0.95, -1, BOY, kp)
        if lf < hit - 8:
            ball(ctx, 790, 1150 - 160 * abs(math.sin(lf * 0.4)), 40, lf * 0.3)
        elif lf < hit:
            u = pop(lf, hit - 8, hit)
            ball(ctx, 790 - 230 * u, 1150 - 120 * math.sin(u * math.pi), 40, lf * 0.5)
        else:
            u = pop(lf, hit, hit + 20)
            ball(ctx, 560 - 300 * u, 1000 + 440 * u, 40, lf * 0.5)
        # Mom on the phone, facing away, oblivious
        mp = P(eye='happy', mouth='grin', rsh=150, rel=-150, lsh=30, lel=-60, head=-6, sway=0.3 * math.sin(lf * 0.2))
        b = draw_hip(ctx, 250, FLOOR - 20, 1.25, 1, MOM, mp)
        hx_, hy_ = b['head']
        ctx.save(); ctx.translate(hx_ - 0.95 * b['R'], hy_ + 0.1 * b['R']); ctx.rotate(-0.25)
        rect_r(ctx, -22, -50, 44, 100, 10); fl(ctx, hx('24243a'), 5); ctx.restore()
        for k in range(3):
            heart(ctx, hx_ - 120 + k * 110, hy_ - 200 - 20 * math.sin(lf * 0.2 + k), 26, hx('ff8ac0'))
        ctx.restore()
        if lf < hit:
            label(ctx, "\"The kids are ANGELS!\"", 540, LY, 100, hx('ff5fa8'), -0.03, pop(lf, 2, 6))
        else:
            label(ctx, "*CRASH!*", 540, LY, 136, hx('fff27a'), 0.05, pop(lf, hit, hit + 4))
    elif lf < 92:
        il = lf - 56
        # dutch ECU: phone covered, head whips round
        ctx.save(); cam(ctx, 540, 1000, 1.12 + 0.05 * eout(pop(il, 0, 36)), -8, 3 + shake_at(il, [0], 12, 26), f)
        angry_bg(ctx, il)
        angry_face(ctx, 540, 1000, 320, il, 0.0, mouth='flat', phone=True, covered=True)
        ctx.restore()
        label(ctx, "\"I. SAW. THAT.\"", 540, LY, 124, (1, 1, 1), -0.03, pop(il, 4, 8))
    else:
        il = lf - 92
        ctx.save(); cam(ctx, 540, 1000, 1.02 + 0.04 * eout(pop(il, 0, 28)), 4, shake_at(il, [0], 6, 10), f)
        sweet_bg(ctx, il + 60)
        sweet_face(ctx, 540, 1000, 320, il, 0.06)
        ctx.restore()
        label(ctx, "\"Sorry! Bad signal!\"", 540, LY, 108, hx('ff5fa8'), -0.03, pop(il, 2, 6))
    card(ctx, 'p2', f, 114, 226)


def split_face(ctx, f, il, z, rot=0.0):
    """left half sweet (toward the phone), right half demon (toward the kid)"""
    cx, cy, Rt = 540, 1000, 330
    for side in (-1, 1):
        ctx.save()
        ctx.rectangle(0 if side < 0 else 540, 0, 540, H); ctx.clip()
        ctx.save(); cam(ctx, 540, 1000, z, rot, 2, f)
        if side < 0:
            sweet_bg(ctx, il)
            sweet_face(ctx, cx, cy, Rt, il, 0.0)
        else:
            angry_bg(ctx, il)
            angry_face(ctx, cx, cy, Rt, il, 0.0, mouth='scream')
        ctx.restore()
        ctx.restore()
    ctx.rectangle(532, 0, 16, H); setc(ctx, (1, 1, 1)); ctx.fill_preserve(); ink(ctx, 5); ctx.stroke()


def s3(ctx, f):
    lf = f - 230
    if lf < 66:
        split_face(ctx, f, lf, 1.0 + 0.08 * eout(pop(lf, 0, 66)))
        if lf < 32:
            label(ctx, "\"Yes, darling!\"", 280, LY, 64, hx('ff5fa8'), -0.04, pop(lf, 4, 8))
        else:
            label(ctx, "\"Yes, darling!\"", 280, LY, 64, hx('ff5fa8'), -0.04, 1)
            label(ctx, "\"PUT IT DOWN!\"", 730, LY - 120, 70, (1, 1, 1), 0.04, pop(lf, 32, 36))
    else:
        il = lf - 66
        # whip-switching, faster and faster
        flips = [0, 12, 22, 30, 36, 41, 45, 48, 51, 53, 55, 57]
        k = sum(1 for x in flips if il >= x)
        sweet = (k % 2 == 1) if il < 58 else True
        last = max([x for x in flips if il >= x] or [0])
        sh = shake_at(il, [last], 6, 18)
        ctx.save(); cam(ctx, 540, 1000, 1.05 + 0.1 * pop(il, 0, 74), (5 if sweet else -5), sh, f)
        if sweet:
            sweet_bg(ctx, il)
            sweet_face(ctx, 540, 1000, 320, il)
        else:
            angry_bg(ctx, il)
            angry_face(ctx, 540, 1000, 320, il, 0.0, phone=True)
        ctx.restore()
        if il - last < 3 and il < 60:   # whip-pan streaks
            for j in range(10):
                yy = 520 + j * 110
                ctx.rectangle(0, yy, W, 18); setc(ctx, (1, 1, 1, 0.55)); ctx.fill()
        if il < 58:
            label(ctx, ("\"Mm-hm, lovely!\"" if sweet else "\"STOP IT!\""), 540, LY, 104, hx('ff5fa8') if sweet else (1, 1, 1), -0.03, 1)
        elif il < 62:
            pass
        else:
            label(ctx, "\"LOVE YOU, BYE!\"  *CLICK*", 540, LY, 92, hx('ff5fa8'), -0.03, pop(il, 62, 66))
    card(ctx, 'p3', f, 234, 366)


def s4(ctx, f):
    lf = f - 370
    if lf < 76:
        # dark low angle: she slowly turns from the phone toward the camera (the kid)
        turn = eout(pop(lf, 10, 46))
        ctx.save(); cam(ctx, 540, 1080, 1.0 + 0.22 * ein(pop(lf, 0, 76)), 0, shake_at(lf, [46], 10, 16), f, sy=H / 2 + 60)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('1a1030')); ctx.fill()
        g = cairo.RadialGradient(540, 900, 50, 540, 900, 900)
        g.add_color_stop_rgba(0, 1, 0.15, 0.2, 0.75 * turn); g.add_color_stop_rgba(1, 0.4, 0, 0.1, 0)
        ctx.set_source(g); ctx.rectangle(-500, -500, 2200, 3000); ctx.fill()
        ctx.rectangle(-500, FLOOR, 2200, 800); setc(ctx, hx('2a1a40')); ctx.fill()
        mp = P(eye='glare' if turn > 0.5 else 'happy', mouth='flat' if turn > 0.5 else 'smile', rsh=20 + 40 * (1 - turn), rel=-30, lsh=20, lel=-30,
               head=0, rot=0)
        b = draw_hip(ctx, 540, FLOOR + 380, 2.9, -1 if turn < 0.5 else 1, MOM, mp)
        # dropped phone on the floor
        ctx.save(); ctx.translate(820, FLOOR + 40); ctx.rotate(0.2); rect_r(ctx, -60, -26, 120, 52, 10); fl(ctx, hx('24243a'), 6); ctx.restore()
        if turn > 0.5:
            hx_, hy_ = b['head']
            steam(ctx, hx_ - 270, hy_ - 160, lf, 1.0, -1); steam(ctx, hx_ + 270, hy_ - 160, lf + 9, 1.0, 1)
        ctx.restore()
        if lf >= 46:
            label(ctx, "\"NOW... WHERE WAS I?\"", 540, LY, 100, (1, 1, 1), -0.03, pop(lf, 46, 50))
        else:
            label(ctx, "*SLOW TURN*", 540, LY, 100, hx('c8b8ff'), 0.03, pop(lf, 10, 14))
    else:
        il = lf - 76
        # kid ECU, terrified, red glow from off-screen
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.1 * eout(pop(il, 0, 54)), 0, 3 + shake_at(il, [20], 8, 14), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('5a1030')); ctx.fill()
        rays(ctx, 540, 1000, 260, 1500, il * 0.02, col=(1, 0.3, 0.3), a=0.3, n=16)
        jx = 5 * math.sin(il * 3.3)
        face(ctx, BOY, P(eye='shock', mouth='wavy', head=0), 540 + jx, 1000, 330)
        sweat(ctx, 820, 760 + (il % 20) * 7, 2.2); sweat(ctx, 260, 820 + ((il + 9) % 20) * 7, 1.6)
        ctx.restore()
        label(ctx, "*GULP*", 540, LY, 130, hx('fff27a'), 0.04, pop(il, 20, 24))
    card(ctx, 'p4', f, 374, 496)


def s5(ctx, f):
    lf = f - 500
    if lf < 58:
        # kid lifts the tablet: grandma on video call
        lift = eout(pop(lf, 4, 18))
        ctx.save(); cam(ctx, 540, 1040, 1.0 + 0.08 * eout(pop(lf, 18, 58)), 0, shake_at(lf, [18], 10, 16), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('3ccfb0')); ctx.fill()
        rays(ctx, 540, 900, 200, 1500, lf * 0.03, col=(1, 1, 1), a=0.35 * lift, n=16)
        kp = P(eye='smug', mouth='grin', rsh=110, rel=-60, lsh=-110, lel=60, head=-4)
        draw_hip(ctx, 540, FLOOR + 260, 1.7, 1, BOY, kp)
        tablet(ctx, 540, 1400 - 480 * lift, 1.15, lf)
        for k in range(4):
            sparkle(ctx, 540 + 330 * math.cos(lf * 0.2 + k * 1.6), 920 + 230 * math.sin(lf * 0.2 + k * 1.6), 26 * lift + 1)
        ctx.restore()
        if lf >= 18:
            label(ctx, "\"GRANDMA'S ON VIDEO CALL!\"", 540, LY, 86, hx('fff27a'), -0.03, pop(lf, 18, 22))
        card(ctx, 'p5', f, 504, 616)
    elif lf < 120:
        il = lf - 58
        # Mom mid-scream -> instant angel
        flip = 10
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(il, flip, 62)), 0, 4 if il < flip else shake_at(il, [flip], 8, 14), f)
        if il < flip:
            angry_bg(ctx, il); angry_face(ctx, 540, 1000, 320, il)
        else:
            sweet_bg(ctx, il)
            face(ctx, MOM, P(eye='happy', mouth='grin', head=0), 540, 1000, 320, 0.06 * math.sin(il * 0.2))
            blush(ctx, 540, 1000, 320)
        ctx.restore()
        if il < flip:
            label(ctx, "\"YOUNG MAN—\"", 540, LY, 116, (1, 1, 1), -0.03, pop(il, 0, 4))
        else:
            label(ctx, "\"MOM! HIII! We're GREAT!\"", 540, LY, 92, hx('ff5fa8'), -0.03, pop(il, flip, flip + 4))
        # the kid's smug wink, bottom-left inset
        if il >= 28:
            u = eout(pop(il, 28, 36))
            ctx.save(); ctx.translate(240 - 340 * (1 - u), 1200); ctx.scale(1.2, 1.2)
            ellipse(ctx, 0, 0, 150, 150); fl(ctx, hx('fff27a'), 9)
            ctx.save(); ellipse(ctx, 0, 0, 142, 142); ctx.clip()
            face(ctx, BOY, P(eye='smug', mouth='grin', head=0), 0, 20, 110, -0.1)
            ctx.restore(); ctx.restore()
        card(ctx, 'p5', f, 504, 616)
    else:
        il = lf - 120
        opening_face(ctx, f, il, True)
        card(ctx, 'p1', f, 620)


SHOTS = [(0, s1), (110, s2), (230, s3), (370, s4), (500, s5)]
CUTS = (44, 62, 110, 166, 202, 230, 296, 370, 446, 500, 558, 620)


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
                              "-i", "out/phone_voice_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
