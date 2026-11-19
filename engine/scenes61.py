"""'Can I Have ONE Bite?' - original, general-audience comedy short, 22s.
Hook: kid ECU, giant glossy puppy eyes, hands clasped: "Just ONE bite?"
Beat 1: park bench, Dad with a 3-scoop cone: "...FINE. ONE bite." -> kid's jaw unhinges, *CHOMP!* -> Dad holds an empty cone stub.
Beat 2: Dad buys another, sneaks off and locks himself in the car: "Ahh... PEACE." -> kid squished on the left window,
 the right window, then upside down through the sunroof: "ONE BITE?" -> Dad: "...HOW?!"
Twist: Dad gives up and buys the kid his OWN cone -> Dad's puppy eyes: "Can *I* have ONE bite?" -> kid: "NO. MINE."
 -> offers ONE sprinkle.
 Mom arrives with her cone -> split-screen double puppy eyes -> "...ONE." -> *CHOMP CHOMP* -> Mom holds a stub
 -> kid ECU puppy eyes again (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos
from scenes48 import label1, label2, heart
from scenes58 import arm_to, sweat, twitch
from scenes60 import finger_hand, car_side
import scenes13
from scenes13 import card as _card13
import random

MOM = dict(doodle.MOM_G, shirt=hx('8a3cff'), pants=hx('3d5a9e'))
DAD = dict(doodle.DAD, shirt=hx('ff8a1f'), pants=hx('3d5aff'))
BOY = dict(doodle.BOY, hood=False, shades=False, shirt=hx('22b4e0'), pants=hx('ff3b5c'))
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
MINT = hx('8ff0c8')
CHOC = hx('9a5a3a')
STRAW = hx('ffb3d9')
WHITE = (1, 1, 1)

CAPS = {
    'p1': [[("DAD BOUGHT", OUT)], [("ICE CREAM...", PINK)]],
    'p2': [[("ROUND 2:", OUT)], [("HIDE IT!", ORANGE)]],
    'p3': [[("FINE.", OUT)], [("YOUR OWN CONE.", GREEN)]],
    'p4': [[("THEN MOM", OUT)], [("SHOWED UP...", PURPLE)]],
}
scenes13.CAPS = CAPS
card = _card13
SIT = dict(lhip=-80, lkn=80, rhip=-80, rkn=80)


# ------------------------------------------------------------------ props
def cone(ctx, x, y, s=1.0, a=0.0, scoops=3, stub=False, drip=0.0):
    """ice cream cone, (x, y) = where the hand grips (upper cone)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if stub:
        poly(ctx, [(-50, -60), (-30, -78), (-12, -56), (8, -80), (28, -58), (50, -74), (0, 120)]); fl(ctx, hx('e9a85a'), 7)
    else:
        poly(ctx, [(-54, -70), (54, -70), (0, 120)]); fl(ctx, hx('e9a85a'), 7)
    for k in range(4):
        ctx.move_to(-46 + k * 26, -64); ctx.line_to(8 + k * 6, 80)
        ctx.move_to(46 - k * 26, -64); ctx.line_to(-8 - k * 6, 80)
    setc(ctx, hx('b8783a')); ctx.set_line_width(4); ctx.stroke()
    if not stub:
        cols = [STRAW, MINT, CHOC][:scoops]
        for k, col in enumerate(cols):
            cy = -110 - k * 78
            ellipse(ctx, 0, cy, 66 - k * 4, 54); fl(ctx, col, 7)
            ellipse(ctx, -22, cy - 18, 14, 9, -0.4); setc(ctx, (1, 1, 1, 0.6)); ctx.fill()
        # sprinkles on top scoop
        top = -110 - (len(cols) - 1) * 78
        rnd = random.Random(3)
        for k in range(9):
            sx = rnd.uniform(-40, 40); sy = top + rnd.uniform(-38, 10)
            ctx.save(); ctx.translate(sx, sy); ctx.rotate(rnd.uniform(0, 3))
            rect_r(ctx, -9, -3.5, 18, 7, 3.5); setc(ctx, [RED, YEL, BLUE, GREEN][k % 4]); ctx.fill(); ctx.restore()
        ellipse(ctx, 0, top - 62, 16, 16); fl(ctx, RED, 5)                                     # cherry
        if drip > 0:
            ellipse(ctx, 40, -70 + 60 * drip, 9, 14); fl(ctx, STRAW, 4)
    ctx.restore()


def puppy(ctx, cx, cy, Rt, lf=0, f_=1, wet=1.0):
    """giant glossy puppy pupils drawn over face(..., eye='shock')"""
    for k, (ex, ey, rx) in enumerate(eye_pos(cx, cy, Rt, f_)):
        ry = 0.19 * Rt
        ellipse(ctx, ex, ey, rx * 1.06, ry * 1.04); fl(ctx, WHITE, max(4, Rt * 0.03))
        ellipse(ctx, ex, ey + ry * 0.06, rx * 0.8, ry * 0.82); setc(ctx, hx('2a1a40')); ctx.fill()
        ellipse(ctx, ex, ey + ry * 0.35, rx * 0.6, ry * 0.35); setc(ctx, hx('4a3a8a')); ctx.fill()
        ellipse(ctx, ex - rx * 0.3, ey - ry * 0.3, rx * 0.3, ry * 0.28); setc(ctx, WHITE); ctx.fill()
        ellipse(ctx, ex + rx * 0.28, ey + ry * 0.28, rx * 0.13, ry * 0.12); setc(ctx, WHITE); ctx.fill()
        if wet > 0:   # wobbling tear line at the bottom
            ctx.new_path(); ctx.arc(ex, ey + ry * 0.1, rx * 0.95, 0.35, math.pi - 0.35)
            setc(ctx, (0.6, 0.88, 1.0, 0.85 * wet)); ctx.set_line_width(Rt * 0.035); ctx.stroke()
            ty = ey + ry * 0.95 + (Rt * 0.02) * math.sin(lf * 0.6 + k)
            ellipse(ctx, ex + rx * 0.5, ty, Rt * 0.025, Rt * 0.035); setc(ctx, (0.6, 0.88, 1.0, 0.9 * wet)); ctx.fill()
    # sad pleading brows
    for sx, (ex, ey, rx) in zip((-1, 1), eye_pos(cx, cy, Rt, f_)):
        by = ey - 0.36 * Rt
        ctx.new_path(); ctx.move_to(ex - sx * rx * 0.9, by + 0.04 * Rt); ctx.line_to(ex + sx * rx * 0.8, by - 0.06 * Rt)
        ink(ctx, Rt * 0.045); ctx.stroke()


def cheeks(ctx, cx, cy, R, col, puff_=1.0):
    for sx in (-1, 1):
        ellipse(ctx, cx + sx * 0.78 * R, cy + 0.42 * R, 0.36 * R * puff_, 0.32 * R * puff_); fl(ctx, col, max(4, R * 0.03))
        ellipse(ctx, cx + sx * 0.78 * R, cy + 0.4 * R, 0.14 * R, 0.08 * R); setc(ctx, (1, 0.5, 0.6, 0.5)); ctx.fill()
    ellipse(ctx, cx + 0.04 * R, cy + 0.5 * R, 0.07 * R, 0.05 * R); setc(ctx, CHOC); ctx.fill()
    ellipse(ctx, cx + 0.3 * R, cy + 0.55 * R, 0.08 * R, 0.05 * R); setc(ctx, MINT); ctx.fill()


def chomp_mouth(ctx, cx, cy, R, g):
    """jaw unhinging: g 0..1"""
    if g <= 0:
        return
    w = R * (0.2 + 0.75 * g); h = R * (0.15 + 1.2 * g)
    my = cy + 0.6 * R + h * 0.42
    ellipse(ctx, cx, my + h * 0.1, w * 1.15, h * 0.7); fl(ctx, BOY['skin'], R * 0.03)      # stretched chin
    ellipse(ctx, cx, my, w, h * 0.62); fl(ctx, hx('6a1020'), R * 0.035)
    ellipse(ctx, cx, my + h * 0.36, w * 0.6, h * 0.18); setc(ctx, hx('ff6f86')); ctx.fill()
    for k in range(5):
        tx = cx - w * 0.6 + k * w * 0.3
        poly(ctx, [(tx - w * 0.1, my - h * 0.5), (tx + w * 0.1, my - h * 0.5), (tx, my - h * 0.32)]); fl(ctx, WHITE, R * 0.012)


def park(ctx, ground=FLOOR, sky=hx('8fd8ff')):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, sky); ctx.fill()
    ellipse(ctx, 880, 470, 90, 90); setc(ctx, YEL); ctx.fill()
    for cx_, cy_ in ((180, 520), (640, 430)):
        for dx, r in ((-50, 45), (0, 62), (55, 45)):
            ellipse(ctx, cx_ + dx, cy_, r, r * 0.8); setc(ctx, WHITE); ctx.fill()
    for tx, s in ((-60, 1.1), (1130, 1.0), (300, 0.7)):
        ctx.rectangle(tx - 30 * s, ground - 520 * s, 60 * s, 520 * s); fl(ctx, hx('8a5a3a'), 6)
        for dx, dy, r in ((-90, -560, 130), (80, -580, 140), (0, -700, 150)):
            ellipse(ctx, tx + dx * s, ground + dy * s, r * s, r * s * 0.9); fl(ctx, hx('3fbf5a'), 6)
    ctx.rectangle(-3000, ground - 120, 7000, 3000); setc(ctx, hx('6fd86a')); ctx.fill()
    ctx.move_to(-3000, ground - 120); ctx.line_to(4000, ground - 120); ink(ctx, 6); ctx.stroke()
    rnd = random.Random(7)
    for k in range(40):
        x = rnd.uniform(-200, 1300); y = rnd.uniform(ground - 100, ground + 500)
        ctx.move_to(x, y); ctx.line_to(x + 8, y - 22); ctx.move_to(x + 14, y); ctx.line_to(x + 18, y - 18)
    setc(ctx, hx('3fae4a')); ctx.set_line_width(5); ctx.stroke()


def bench(ctx, x0=60, x1=1020, seat=1330):
    for k in range(3):
        rect_r(ctx, x0, seat - 300 + k * 70, x1 - x0, 46, 12); fl(ctx, hx('c8743a'), 7)
    for lx in (x0 + 80, x1 - 80):
        ctx.rectangle(lx - 14, seat - 320, 28, 330); fl(ctx, hx('4a4e60'), 6)


def bench_front(ctx, x0=60, x1=1020, seat=1330):
    rect_r(ctx, x0 - 20, seat, x1 - x0 + 40, 54, 14); fl(ctx, hx('d8843a'), 7)
    for lx in (x0 + 80, x1 - 80):
        ctx.rectangle(lx - 16, seat + 54, 32, 200); fl(ctx, hx('4a4e60'), 6)


def cart(ctx, x, g, s=1.0):
    """plain ice cream cart with striped umbrella (no branding)"""
    ctx.save(); ctx.translate(x, g); ctx.scale(s, s)
    ctx.rectangle(-8, -760, 16, 420); fl(ctx, hx('c8ccd8'), 5)
    for k in range(6):
        a0 = math.pi + k * math.pi / 6; a1 = a0 + math.pi / 6
        ctx.move_to(0, -760); ctx.arc(0, -760, 300, a0, a1); ctx.close_path()
        fl(ctx, RED if k % 2 == 0 else WHITE, 6)
    rect_r(ctx, -260, -360, 520, 280, 30); fl(ctx, hx('fff3c8'), 8)
    for k, col in enumerate((STRAW, MINT, CHOC)):
        ellipse(ctx, -140 + k * 140, -250, 50, 44); fl(ctx, col, 6)
    for wx in (-170, 170):
        ellipse(ctx, wx, -60, 60, 60); fl(ctx, hx('2a2840'), 7)
        ellipse(ctx, wx, -60, 24, 24); fl(ctx, hx('c8ccd8'), 4)
    ctx.restore()


def pink_bg(ctx, lf, col=hx('ff8fc4')):
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, col); ctx.fill()
    rays(ctx, 540, 1000, 260, 1700, lf * 0.03, col=(1, 1, 1), a=0.28, n=16)
    for k, (hx_, hy_) in enumerate(((170, 700), (900, 760), (130, 1350), (950, 1300))):
        heart(ctx, hx_, hy_ + 10 * math.sin(lf * 0.2 + k), 42 + 6 * math.sin(lf * 0.3 + k), hx('ff3b8a'))


# ------------------------------------------------------------------ opening face
def opening_face(ctx, f, lf, lab=True):
    ctx.save(); cam(ctx, 540, 960, 1.02 + 0.05 * eout(pop(lf, 0, 45)), 0, 2 + shake_at(lf, [0], 8, 10), f)
    pink_bg(ctx, lf)
    cx, cy, R = 540, 960, 330
    wob = 0.03 * math.sin(lf * 0.35)
    face(ctx, BOY, P(eye='shock', mouth='frown', head=0), cx, cy, R, wob)
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(wob); ctx.translate(-cx, -cy)
    puppy(ctx, cx, cy, R, lf)
    ctx.restore()
    # clasped hands under the chin
    for sx in (-1, 1):
        ellipse(ctx, cx + sx * 75, cy + 1.02 * R, 95, 80); fl(ctx, BOY['skin'], 9)
    for k in range(3):
        ctx.move_to(cx - 20 + k * 20, cy + R + 20); ctx.line_to(cx - 20 + k * 20, cy + R + 70)
    ink(ctx, 5); ctx.stroke()
    sparkle(ctx, 270, 700, 30 + 8 * math.sin(lf * 0.5)); sparkle(ctx, 820, 640, 24)
    ctx.restore()
    if lab:
        label1(ctx, "\"Just ONE bite?\"", WHITE, pop(lf, 0, 4) if lf > 0 else 1, 120, -0.04, y=1480)


# ------------------------------------------------------------------ shots
def bench_scene(ctx, f, lf, dad_p, boy_p, dad_cone=None, boy_cone=None, z=1.6, cx=555, cy=1090, boy_puppy=False,
                dad_puppy=False, dad_cheeks=False, boy_cheeks=False, mom=None, shake=0, _=None):
    ctx.save(); cam(ctx, cx, cy, z, 0, shake, f)
    park(ctx)
    cart(ctx, 1200, FLOOR - 60, 0.7)
    bench(ctx)
    g = 1330 + 70
    bd = draw(ctx, 370, g - 186 * 1.0 - 70 + 70, 1.0, 1, DAD, dict(dad_p, **SIT))
    bb = draw(ctx, 740, g - 186 * 0.7 - 70 + 70, 0.7, -1, BOY, dict(boy_p, **SIT))
    if dad_puppy:
        puppy(ctx, bd['head'][0], bd['head'][1], bd['R'], lf, 1)
    if boy_puppy:
        puppy(ctx, bb['head'][0], bb['head'][1], bb['R'], lf, -1)
    if dad_cheeks:
        cheeks(ctx, bd['head'][0], bd['head'][1], bd['R'], DAD['skin'])
    if boy_cheeks:
        cheeks(ctx, bb['head'][0], bb['head'][1], bb['R'], BOY['skin'])
    if dad_cone:
        cone(ctx, bd['front'][0], bd['front'][1], **dad_cone)
    if boy_cone:
        cone(ctx, bb['front'][0], bb['front'][1], **boy_cone)
    if mom:
        mom(ctx)
    bench_front(ctx)
    ctx.restore()
    return bd, bb


def s1(ctx, f):
    if f < 45:
        opening_face(ctx, f, f)
    else:
        lf = f - 45
        give = eout(pop(lf, 24, 34))
        bench_scene(ctx, f, lf,
                    P(eye='glare' if lf < 22 else 'closed', mouth='flat' if lf < 22 else 'wavy', rsh=40 + 50 * give, rel=-60 + 50 * give, lsh=10, head=-6),
                    P(eye='shock', mouth='frown', rsh=30, lsh=-30, rel=-80, lel=-80, head=8),
                    dad_cone=dict(s=0.8, a=0.1 * give), boy_puppy=True, z=1.55 + 0.08 * eout(pop(lf, 0, 45)), shake=shake_at(lf, [0], 6, 8))
        if lf < 22:
            label1(ctx, "\"...no.\"", WHITE, pop(lf, 2, 6), 120, -0.04, y=1480)
        else:
            label2(ctx, "\"...FINE.", "ONE bite.\"", WHITE, pop(lf, 22, 26), 116, col2=YEL, y=1440)
    card(ctx, 'p1', f, -6, 86)


def s2(ctx, f):
    lf = f - 90
    if lf < 30:
        # ECU kid, low angle: jaw unhinges, cone comes in from the right
        g = eout(pop(lf, 2, 22))
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.12 * eout(pop(lf, 0, 26)), -4, shake_at(lf, [24], 14, 34), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb02e')); ctx.fill()
        rays(ctx, 540, 960, 200, 1700, lf * 0.06, col=(1, 1, 0.8), a=0.45, n=20)
        cx, cy, R = 520, 820, 290
        face(ctx, BOY, P(eye='shock' if lf < 12 else 'glare', mouth='scream', head=0), cx, cy, R, 0)
        chomp_mouth(ctx, cx, cy, R, g)
        if lf < 24:
            cone(ctx, 1150 - 380 * eout(pop(lf, 4, 22)), 1250, 1.5, -0.9)
        ctx.restore()
        if lf < 24:
            label(ctx, "*STRETCH...*", 540, 400, 80, WHITE, -0.06, pop(lf, 4, 8))
        if lf >= 24:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.6 * (1 - (lf - 24) / 6))); ctx.fill()
            label(ctx, "*CHOMP!!*", 540, 1450, 170, RED, -0.08, pop(lf, 24, 27))
    elif lf < 78:
        il = lf - 30
        bench_scene(ctx, f, il,
                    P(eye='shock', mouth='scream' if il < 26 else 'wavy', rsh=90, rel=-10, lsh=-20, head=-4),
                    P(eye='happy', mouth='flat', rsh=20, lsh=-20, head=8),
                    dad_cone=dict(s=0.8, stub=True), boy_cheeks=True, z=1.8, cx=555, cy=1080, shake=shake_at(il, [0], 12, 26))
        if il < 26:
            label2(ctx, "\"THAT WAS", "THE WHOLE THING!\"", WHITE, pop(il, 2, 6), 104, col2=RED, y=1440)
        else:
            label1(ctx, "\"Mmmf! ONE bite!\"", WHITE, pop(il, 26, 30), 110, -0.04, y=1480)
    else:
        il = lf - 78
        # Dad tiptoes off with a NEW cone, wide, looking around
        ctx.save(); cam(ctx, 560, 1150, 1.3, 0, 0, f)
        park(ctx)
        cart(ctx, 160, FLOOR - 60, 0.8)
        x = 420 + 9 * il
        step = math.sin(il * 0.6)
        look = 1 if (il // 10) % 2 == 0 else -1
        b = draw(ctx, x, FLOOR - 186 * 1.0 + 40 - 20 * abs(step), 1.0, look, DAD,
                 P(eye='normal', mouth='flat', rsh=60, rel=-80, lsh=-40, lel=-30, lhip=-25 * step, rhip=25 * step, lkn=20, rkn=20, torso=-8 * look, head=-10))
        cone(ctx, b['front'][0], b['front'][1], 0.75)
        ctx.restore()
        label2(ctx, "\"Somewhere...", "...SAFE.\"", WHITE, pop(il, 3, 7), 104, col2=ORANGE, y=1440)
        card(ctx, 'p2', f, 170, 198)


def car_interior(ctx, lf, wins=(False, False, False), shake=0, f=0, dad_eye='closed', dad_mouth='smile', z=1.0):
    ctx.save(); cam(ctx, 540, 960, z, 0, shake, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('3a3e5e')); ctx.fill()
    # sunroof + two side windows (park outside)
    for (x, y, w, h) in ((290, 280, 500, 230), (40, 560, 440, 470), (600, 560, 440, 470)):
        rect_r(ctx, x - 14, y - 14, w + 28, h + 28, 50); setc(ctx, hx('22243a')); ctx.fill()
        ctx.save(); rect_r(ctx, x, y, w, h, 40); ctx.clip()
        ctx.rectangle(x, y, w, h); setc(ctx, hx('8fd8ff')); ctx.fill()
        if h > 300:
            ctx.rectangle(x, y + h * 0.7, w, h); setc(ctx, hx('6fd86a')); ctx.fill()
            ellipse(ctx, x + w * 0.3, y + h * 0.45, 70, 60); setc(ctx, hx('3fbf5a')); ctx.fill()
        ctx.restore()
        rect_r(ctx, x, y, w, h, 40); ink(ctx, 8); ctx.stroke()
    # squished kid faces on the glass
    spots = [(260, 800, 0.0, 1), (820, 800, 0.0, -1), (540, 395, math.pi, 1)]
    for k, on in enumerate(wins):
        if not on:
            continue
        x, y, rot, f_ = spots[k]
        clip = [(40, 560, 440, 470), (600, 560, 440, 470), (290, 280, 500, 230)][k]
        ctx.save(); rect_r(ctx, *clip, 40); ctx.clip()
        R = 170 if k < 2 else 105
        face(ctx, BOY, P(eye='shock', mouth='open', head=0), x, y, R, rot, f_)
        if k < 2:
            puppy(ctx, x, y, R, lf, f_)
            ellipse(ctx, x + f_ * 0.12 * R, y + 0.28 * R, 0.2 * R, 0.13 * R); setc(ctx, hx('ffb3a0')); ctx.fill()     # nose smoosh
            for sx in (-1, 1):
                ellipse(ctx, x + sx * 1.15 * R, y + 0.6 * R, 0.32 * R, 0.4 * R); fl(ctx, BOY['skin'], 6)
        ctx.rectangle(clip[0], clip[1], clip[2], clip[3]); setc(ctx, (1, 1, 1, 0.16)); ctx.fill()
        ctx.move_to(clip[0] + 40, clip[1] + 30); ctx.line_to(clip[0] + 120, clip[1] + 30 + 100)
        setc(ctx, (1, 1, 1, 0.5)); ctx.set_line_width(16); ctx.stroke()
        ctx.restore()
    # seat + Dad, eating
    rect_r(ctx, 250, 1000, 580, 900, 120); fl(ctx, hx('5a3a2a'), 8)
    cx, cy, R = 540, 1230, 250
    face(ctx, DAD, P(eye=dad_eye, mouth=dad_mouth, head=0), cx, cy, R, 0)
    ctx.arc(540, 1760, 380, math.pi * 1.15, math.pi * 1.85); ink(ctx, 46); ctx.stroke()            # steering wheel
    ctx.arc(540, 1760, 380, math.pi * 1.15, math.pi * 1.85); setc(ctx, hx('2a2840')); ctx.set_line_width(34); ctx.stroke()
    cone(ctx, 780, 1300, 0.8, -0.25)
    ellipse(ctx, 780, 1330, 62, 56); fl(ctx, DAD['skin'], 7)
    ctx.restore()


def s3(ctx, f):
    lf = f - 200
    if lf < 40:
        car_interior(ctx, lf, shake=shake_at(lf, [4], 6, 8), f=f, dad_eye='closed' if lf > 12 else 'smug', dad_mouth='smile' if lf > 12 else 'grin', z=1.0 + 0.03 * eout(pop(lf, 0, 40)))
        if lf < 12:
            label(ctx, "*CLICK!* LOCKED.", 540, 1500, 84, YEL, -0.05, pop(lf, 4, 7))
        else:
            label1(ctx, "\"Ahh... PEACE.\"", WHITE, pop(lf, 12, 16), 110, -0.04, y=1500)
    elif lf < 106:
        il = lf - 40
        wins = (il >= 0, il >= 22, il >= 44)
        k = 0 if il < 22 else (1 if il < 44 else 2)
        car_interior(ctx, il, wins, shake=shake_at(il, [0, 22, 44], 10, 18), f=f, dad_eye='shock', dad_mouth='wavy' if k < 2 else 'scream', z=1.0)
        txt = ["\"One bite?\"", "\"ONE bite?\"", "\"ONE BITE?!\""][k]
        pos = [(260, 990), (820, 990), (540, 570)][k]
        sq = pop(il - 22 * k, 0, 3) * (1 - pop(il - 22 * k, 12, 15))
        if k < 2:
            label(ctx, "*SQUEAK!*", pos[0], 640, 64, WHITE, 0.08, sq)
        label(ctx, txt, pos[0], pos[1], 76 if k < 2 else 88, YEL, -0.06, pop(il - 22 * k, 2, 6))
    else:
        il = lf - 106
        # Dad ECU: ...HOW?!
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.2 * eout(pop(il, 0, 8)), 0, shake_at(il, [0], 12, 28), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd23f')); ctx.fill()
        rays(ctx, 540, 960, 260, 1700, il * 0.02, col=(1, 1, 1), a=0.5, n=20)
        face(ctx, DAD, P(eye='shock', mouth='scream', head=0), 540, 960, 290, 0)
        twitch(ctx, 540 + 0.5 * 290, 960 - 0.55 * 290, il, 1.2)
        sweat(ctx, 540 - 0.95 * 290, 960 - 0.6 * 290, il, 1.4)
        ctx.restore()
        label1(ctx, "\"...HOW?!\"", WHITE, pop(il, 2, 6), 140, -0.04, y=1480)


def s4(ctx, f):
    lf = f - 330
    if lf < 42:
        bench_scene(ctx, f, lf,
                    P(eye='closed', mouth='wavy', rsh=90, rel=-10, lsh=10, head=-4),
                    P(eye='happy', mouth='grin', rsh=40, lsh=-30, rel=-60, head=6),
                    boy_cone=dict(s=0.62, a=-0.1), z=1.6, cy=1090)
        sparkle(ctx, 760, 760, 40 + 8 * math.sin(lf * 0.6)); sparkle(ctx, 900, 880, 28)
        label2(ctx, "\"Here. YOUR OWN.", "Happy now?\"", WHITE, pop(lf, 2, 6), 100, col2=GREEN, y=1440)
        card(ctx, 'p3', f, 332, 370)
    elif lf < 80:
        il = lf - 42
        # Dad's turn: puppy eyes
        ctx.save(); cam(ctx, 540, 960, 1.02 + 0.06 * eout(pop(il, 0, 38)), 0, shake_at(il, [0], 6, 8), f)
        pink_bg(ctx, il, col=hx('ffb3d9'))
        cx, cy, R = 540, 960, 310
        face(ctx, DAD, P(eye='shock', mouth='frown', head=0), cx, cy, R, 0)
        puppy(ctx, cx, cy, R, il)
        for sx in (-1, 1):
            ellipse(ctx, cx + sx * 80, cy + 1.02 * R, 100, 84); fl(ctx, DAD['skin'], 9)
        ctx.restore()
        label2(ctx, "\"Can *I* have", "ONE bite?\"", WHITE, pop(il, 2, 6), 112, col2=YEL, y=1440)
    elif lf < 106:
        il = lf - 80
        # kid hugs the cone like a baby, glare
        ctx.save(); cam(ctx, 540, 960, 1.05, 3, shake_at(il, [0], 10, 20), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff5f5f')); ctx.fill()
        rays(ctx, 540, 960, 260, 1700, -il * 0.03, col=(1, 0.8, 0.6), a=0.35, n=16)
        cx, cy, R = 560, 880, 290
        face(ctx, BOY, P(eye='glare', mouth='flat', head=0), cx, cy, R, -0.05)
        cone(ctx, 300, 1380, 0.85, 0.3)
        for sx, (ax, ay) in ((-1, (280, 1420)), (1, (420, 1450))):
            ellipse(ctx, ax, ay, 80, 66); fl(ctx, BOY['skin'], 8)
        ctx.restore()
        label1(ctx, "\"NO. MINE.\"", WHITE, pop(il, 2, 5), 140, -0.04, y=1480)
    else:
        il = lf - 106
        # ECU: ONE sprinkle on a fingertip
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.1 * eout(pop(il, 0, 24)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('7fd0ff')); ctx.fill()
        rays(ctx, 540, 820, 160, 1700, il * 0.02, col=(1, 1, 1), a=0.35, n=18)
        arm_to(ctx, 1200, 1800, 640, 1080, BOY['shirt'], BOY['skin'], bend=-60, w=130)
        sk = BOY['skin']
        for k, (fx, fh) in enumerate(((-150, 150), (-60, 190), (30, 200), (120, 170))):
            rect_r(ctx, 540 + fx, 900 - fh, 70, fh + 60, 35); fl(ctx, sk, 8)
        ctx.save(); ctx.translate(380, 1000); ctx.rotate(-0.7); rect_r(ctx, -40, -100, 70, 170, 35); fl(ctx, sk, 8); ctx.restore()
        ellipse(ctx, 540, 1000, 220, 170); fl(ctx, sk, 9)
        ctx.new_path(); ctx.arc(540, 960, 110, 0.3, math.pi - 0.3); setc(ctx, dark(sk, 0.8)); ctx.set_line_width(6); ctx.stroke()
        tip = (540, 1000)
        ctx.save(); ctx.translate(540, 990); ctx.rotate(0.4)
        rect_r(ctx, -30, -11, 60, 22, 11); fl(ctx, PINK, 5); ctx.restore()
        sparkle(ctx, tip[0] + 70, tip[1] - 70, 22 + 6 * math.sin(il * 0.8))
        ctx.restore()
        label2(ctx, "\"Here.", "ONE sprinkle.\"", WHITE, pop(il, 2, 6), 110, col2=PINK, y=1440)


def mom_walk(lf, x, holding='full', eye='happy', mouth='grin', hair_blown=False):
    def fn(ctx):
        step = math.sin(lf * 0.6) if holding == 'full' and lf < 30 else 0
        b = draw(ctx, x, FLOOR - 186 * 1.05 + 60 - 16 * abs(step), 1.05, -1, MOM,
                 P(eye=eye, mouth=mouth, rsh=25, rel=-5, lsh=20, lhip=-20 * step, rhip=20 * step, head=4))
        cone(ctx, b['head'][0] - 175, b['head'][1] + 130 + (60 if holding == 'full' else 0), 0.62 if holding == 'full' else 0.85, -0.2, stub=(holding == 'stub'))
        if hair_blown:
            for k in range(3):
                ctx.move_to(b['head'][0] - 140, b['head'][1] - 120 + k * 60); ctx.line_to(b['head'][0] - 260, b['head'][1] - 140 + k * 60)
            setc(ctx, WHITE); ctx.set_line_width(10); ctx.stroke()
    return fn


def s5(ctx, f):
    lf = f - 460
    if lf < 44:
        x = 1300 - 440 * eout(pop(lf, 0, 26))
        bench_scene(ctx, f, lf,
                    P(eye='normal', mouth='frown', rsh=20, lsh=10, head=4),
                    P(eye='closed', mouth='smile', rsh=40, lsh=-30, rel=-60, head=6),
                    boy_cone=dict(s=0.62, a=-0.1), z=1.3, cx=600, cy=1090, mom=mom_walk(lf, x))
        label1(ctx, "\"Hi guys! Ice cream!\"", WHITE, pop(lf, 8, 12), 104, -0.04, y=1480)
        card(ctx, 'p4', f, 462, 500)
    elif lf < 84:
        il = lf - 44
        # split screen: both turn with puppy eyes
        for side in (0, 1):
            ctx.save(); ctx.rectangle(side * 540, 0, 540, H); ctx.clip()
            zz = 1.0 + 0.05 * eout(pop(il, 0, 40)); ctx.translate(270 + side * 540, 960); ctx.scale(zz, zz); ctx.translate(-270 - side * 540, -960)
            ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8fc4') if side == 0 else hx('ffb3d9')); ctx.fill()
            rays(ctx, 270 + side * 540, 960, 120, 1400, il * 0.03 * (1 if side else -1), col=(1, 1, 1), a=0.3, n=12)
            ch = DAD if side == 0 else BOY
            cx = 270 + side * 540
            face(ctx, ch, P(eye='shock', mouth='frown', head=0), cx, 960, 230, 0.04 * math.sin(il * 0.4 + side))
            puppy(ctx, cx, 960, 230, il)
            ctx.restore()
        ctx.rectangle(530, 0, 20, H); setc(ctx, WHITE); ctx.fill()
        ctx.rectangle(527, 0, 4, H); setc(ctx, OUT); ctx.fill(); ctx.rectangle(549, 0, 4, H); setc(ctx, OUT); ctx.fill()
        label2(ctx, "\"Can WE have", "ONE bite?\"", WHITE, pop(il, 3, 7), 112, col2=YEL, y=1440)
    elif lf < 110:
        il = lf - 84
        ctx.save(); cam(ctx, 540, 960, 1.04, 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('c8b8ff')); ctx.fill()
        for k in range(6):
            ellipse(ctx, 540, 960, 280 + k * 170, 280 + k * 170); setc(ctx, (1, 1, 1, 0.3)); ctx.set_line_width(30); ctx.stroke()
        face(ctx, MOM, P(eye='closed', mouth='wavy', head=0), 540, 960, 300, 0.04)
        cone(ctx, 870, 1250, 1.1, 0.15)
        ctx.restore()
        label1(ctx, "\"...ONE.\"", WHITE, pop(il, 3, 7), 150, -0.04, y=1480)
    elif lf < 122:
        il = lf - 110
        ctx.save(); cam(ctx, 540, 960, 1.0, 0, shake_at(il, [0, 6], 10, 40), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd23f') if il < 6 else hx('ff8a1f')); ctx.fill()
        rays(ctx, 540, 960, 100, 1700, il * 0.3, col=(1, 1, 1), a=0.6, n=24)
        ctx.restore()
        label(ctx, "*CHOMP!*", 540, 760, 170, RED, -0.12, pop(il, 0, 3))
        if il >= 6:
            label(ctx, "*CHOMP!*", 540, 1160, 170, PURPLE, 0.1, pop(il, 6, 9))
    elif lf < 166:
        il = lf - 122
        bench_scene(ctx, f, il,
                    P(eye='happy', mouth='flat', rsh=20, lsh=10, head=4),
                    P(eye='happy', mouth='flat', rsh=40, lsh=-30, rel=-60, head=6),
                    boy_cone=dict(s=0.62, a=-0.1), dad_cheeks=True, boy_cheeks=True, z=1.3, cx=600, cy=1090,
                    mom=mom_walk(40, 860, holding='stub', eye='shock', mouth='flat', hair_blown=True), shake=shake_at(il, [0], 10, 20))
        label2(ctx, "\"...that was", "MY cone.\"", WHITE, pop(il, 6, 10), 112, col2=PURPLE, y=1440)
    else:
        il = lf - 166
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 628)


SHOTS = [(0, s1), (90, s2), (200, s3), (330, s4), (460, s5)]
CUTS = (45, 90, 120, 168, 200, 240, 306, 330, 372, 410, 436, 460, 504, 544, 570, 582, 626)


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
                              "-i", "out/bite_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
