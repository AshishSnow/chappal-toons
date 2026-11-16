"""'Counting to Three' - original, general-audience comedy short, ~22s.
Hook: ECU of Mom, glaring, one finger up, a giant 1 behind her: "ONE..."
 -> wide: the kid sprawled on a beanbag with a tablet, in socks: *tap tap tap*  "Yeah, yeah..."
Beat 1: "TWO..." (redder, closer) - kid ECU, smug, dangling ONE sock: "She never gets to THREE."
Beat 2: Mom stalls: "TWO AND A HALF..." "TWO AND THREE QUARTERS..." sweating; split screen:
 kid: "What happens at THREE?" / Mom freezes, glitch, "...uh."
Beat 3: Mom secretly phones Grandma: "Mom... what happens at three?" - Grandma ECU: "ONE..."
 -> Mom AND the kid super-speed into coats + shoes, POOF: both saluting at the open door: "READY!"
Twist: Dad on the sofa with popcorn: "Pfft, nobody knows what happens at thr-" - Mom turns the phone:
 Grandma: "TWO..." - WHOOSH: a Dad-shaped hole in the wall, popcorn raining on the empty sofa,
 *HONK HONK* "...Dad's in the car."
Loop: Mom ECU "ONE..." -> loops to the opening."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos, living, sofa_back, sofa_front, popcorn, SEAT
from scenes8 import sit
from scenes14 import sweat
from scenes33 import phone_at_ear
import scenes13
from scenes13 import card as _card13
import random

BOY = doodle.BOY
MOM = doodle.MOM_G
DAD = doodle.DAD
GRAN = dict(doodle.NMOM, hair=hx('dfe2ec'), shirt=hx('ff6fae'), glasses=hx('8a3cff'))
KID_SOCKS = dict(BOY, shoes=hx('ffffff'))
MOM_SLIP = dict(MOM, shoes=hx('ff9fd0'))
KID_COAT = dict(BOY, shirt=hx('ff3b5c'))
MOM_COAT = dict(MOM, shirt=hx('1fa36a'))
N = 660
FLOOR = 1460
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
LY = 1450

CAPS = {
    'p1': [[("WHEN MOM STARTS", OUT)], [("COUNTING TO 3", RED)]],
    'p2': [[("BUT THIS KID", OUT)], [("KNOWS THE TRICK", ORANGE)]],
    'p3': [[("NOBODY HAS EVER", OUT)], [("REACHED THREE", PURPLE)]],
    'p4': [[("SO MOM CALLED", OUT)], [("HER OWN MOM", GREEN)]],
    'p5': [[("DAD THOUGHT", OUT)], [("HE WAS IMMUNE", PINK)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def finger_up(ctx, x, y, s, skin, wag=0.0):
    """raised hand with the index finger up, wrist at (x, y)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(wag); ctx.scale(s, s)
    rect_r(ctx, -26, -150, 52, 130, 26); fl(ctx, skin, 6)          # index finger
    ellipse(ctx, 0, 0, 70, 60); fl(ctx, skin, 6)                    # fist
    for k in range(3):
        ctx.move_to(-40 + k * 28, -30); ctx.line_to(-40 + k * 28, 6)
    ink(ctx, 4); ctx.stroke()
    ellipse(ctx, 50, -10, 22, 34, 0.4); fl(ctx, skin, 5)           # thumb
    ctx.rectangle(-50, 50, 100, 140); fl(ctx, skin, 6)              # wrist
    ctx.rectangle(-58, 120, 116, 120); fl(ctx, MOM['shirt'], 6)     # sleeve
    ctx.restore()


def big_num(ctx, s, x, y, size, col, a=0.35, ang=0.0):
    ctx.push_group()
    text(ctx, s, x, y, size, col, ow=24, ang=ang, shadow=False)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a)


def tablet(ctx, x, y, a=0.0, s=1.0, lf=0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -110, -80, 220, 160, 18); fl(ctx, hx('24243a'), 6)
    rect_r(ctx, -96, -66, 192, 132, 10); setc(ctx, hx('6be2ff')); ctx.fill()
    for k in range(3):   # bouncing game blocks
        yy = 20 - 30 * abs(math.sin(lf * 0.4 + k))
        ctx.rectangle(-70 + k * 50, yy, 34, 34); fl(ctx, (hx('ffd23f'), hx('ff5fa8'), hx('22b45a'))[k], 3)
    ctx.restore()


def beanbag(ctx, x, y):
    ctx.new_path(); ctx.move_to(x - 250, y + 60)
    ctx.curve_to(x - 280, y - 90, x - 120, y - 150, x - 10, y - 120)
    ctx.curve_to(x + 120, y - 160, x + 280, y - 90, x + 250, y + 60)
    ctx.close_path(); fl(ctx, hx('ff8a1f'), 8)
    ctx.move_to(x - 120, y - 60); ctx.curve_to(x - 60, y - 20, x + 40, y - 20, x + 110, y - 70); ink(ctx, 5); ctx.stroke()


def sock(ctx, x, y, a=0.0, s=1.0, swing=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a + swing); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-28, 0); ctx.line_to(28, 0); ctx.line_to(28, 150)
    ctx.curve_to(28, 200, 110, 190, 110, 230); ctx.curve_to(110, 270, 20, 270, -10, 240); ctx.curve_to(-30, 220, -28, 190, -28, 150)
    ctx.close_path(); fl(ctx, (1, 1, 1), 6)
    for k in range(2):
        ctx.rectangle(-28, 20 + k * 30, 56, 14); setc(ctx, RED); ctx.fill()
    ctx.restore()


def beanie(ctx, b, col=hx('ffd23f')):
    hx_, hy_ = b['head']; R = b['R']
    ctx.new_path(); ctx.arc(hx_, hy_ - 0.25 * R, 1.05 * R, math.pi, 2 * math.pi); ctx.close_path(); fl(ctx, col, 5)
    rect_r(ctx, hx_ - 1.1 * R, hy_ - 0.38 * R, 2.2 * R, 0.32 * R, 0.12 * R); fl(ctx, dark(col, 0.85), 5)
    ellipse(ctx, hx_, hy_ - 1.32 * R, 0.22 * R, 0.22 * R); fl(ctx, (1, 1, 1), 5)


def speed_lines(ctx, lf, col=(1, 1, 1), a=0.8, n=14):
    rnd = random.Random(lf // 2)
    for k in range(n):
        y = rnd.uniform(500, 1450); x = rnd.uniform(-100, 900); L = rnd.uniform(160, 420)
        ctx.move_to(x, y); ctx.line_to(x + L, y)
    setc(ctx, col + (a,)); ctx.set_line_width(10); ctx.stroke()


def glitch(ctx, lf, y0, y1, amt=1.0):
    rnd = random.Random(lf)
    for k in range(int(6 * amt)):
        y = rnd.uniform(y0, y1); h = rnd.uniform(6, 30)
        ctx.rectangle(0, y, W, h); setc(ctx, rnd.choice([(1, 0.2, 0.4), (0.2, 0.9, 1), (1, 1, 1)]) + (0.45,)); ctx.fill()


def person_hole(ctx, x, y, s, sky=hx('8fd8ff')):
    """jagged Dad-shaped hole in the wall, centre (x, y), arms up like a rocket"""
    shapes = [('e', 0, -230, 95, 100), ('r', -95, -150, 190, 260), ('l', -60, -110, -200, -330), ('l', 60, -110, 200, -330),
              ('l', -50, 100, -110, 330), ('l', 50, 100, 110, 330)]
    for pass_ in (0, 1):
        for sh in shapes:
            ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
            if sh[0] == 'e':
                ellipse(ctx, sh[1], sh[2], sh[3], sh[4])
            elif sh[0] == 'r':
                rect_r(ctx, sh[1], sh[2], sh[3], sh[4], 40)
            else:
                ctx.move_to(sh[1], sh[2]); ctx.line_to(sh[3], sh[4])
            ctx.restore()
            if sh[0] == 'l':
                ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                setc(ctx, OUT if pass_ == 0 else sky); ctx.set_line_width((90 + 16) * s if pass_ == 0 else 90 * s); ctx.stroke()
            else:
                if pass_ == 0:
                    setc(ctx, OUT); ctx.set_line_width(16 * s); ctx.stroke_preserve(); ctx.fill()
                else:
                    setc(ctx, sky); ctx.fill()
    # a little cloud seen through the hole
    ellipse(ctx, x - 20 * s, y - 40 * s, 60 * s, 30 * s); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()
    ellipse(ctx, x + 30 * s, y - 55 * s, 45 * s, 30 * s); ctx.fill()
    # cracks around it
    rnd = random.Random(5)
    for k in range(10):
        a = k * 2 * math.pi / 10 + rnd.uniform(-0.2, 0.2); r0 = 300 * s; r1 = r0 + rnd.uniform(40, 110) * s
        ctx.move_to(x + math.cos(a) * r0 * 0.75, y + math.sin(a) * r0)
        ctx.line_to(x + math.cos(a + 0.1) * r1 * 0.75, y + math.sin(a + 0.1) * r1)
    ink(ctx, 5); ctx.stroke()


# ------------------------------------------------------------------ shared shots
def mom_count(ctx, f, lf, num, word, bg, zoom0=1.0, rays_col=(1, 1, 1), lab=True, eye='glare', mouth='flat', sweat_=False, big=True,
              lab_col=(1, 1, 1), lab_size=130):
    ctx.save(); cam(ctx, 540, 1000, zoom0 + 0.06 * eout(pop(lf, 0, 40)), -3, shake_at(lf, [0], 10, 14), f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, bg); ctx.fill()
    rays(ctx, 540, 940, 240, 1700, lf * 0.02, col=rays_col, a=0.35, n=16)
    if big:
        big_num(ctx, num, 300, 820, 760, (1, 1, 1), 0.55, -0.12)
    face(ctx, MOM, P(eye=eye, mouth=mouth, head=0), 560, 950, 300, 0.04)
    finger_up(ctx, 860, 1330, 1.2, MOM['skin'], 0.08 * math.sin(lf * 0.5))
    if sweat_:
        sweat(ctx, 330, 700, lf, 1.0)
    ctx.restore()
    if lab:
        label(ctx, word, 540, LY + 40, lab_size, lab_col, -0.03, pop(lf, 0, 4) if lf > 0 else 1)


def opening_face(ctx, f, lf):
    mom_count(ctx, f, lf, "1", "\"ONE...\"", hx('ffb85a'))


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 50:
        opening_face(ctx, f, f)
    else:
        lf = f - 50
        ctx.save(); cam(ctx, 560, 1080, 1.22 - 0.2 * eout(pop(lf, 0, 14)), 0, shake_at(lf, [0], 8, 10), f)
        living(ctx)
        beanbag(ctx, 380, FLOOR - 70)
        kick = 25 * math.sin(lf * 0.35)
        b = draw_hip(ctx, 360, FLOOR - 160, 0.98, 1, KID_SOCKS,
                     sit(eye='happy', mouth='smile' if lf < 30 else 'flat', torso=-14, head=10, rsh=-40, rel=-60, lsh=-30, lel=-70,
                         lhip=80, lkn=-40 + kick, rhip=84, rkn=-60 - kick))
        tablet(ctx, b['head'][0] + 110, b['head'][1] + 190, -0.35, 0.8, lf)
        draw_hip(ctx, 860, FLOOR - 220, 1.15, -1, MOM_SLIP, P(eye='glare', mouth='flat', rsh=-130, rel=-110, lsh=130, lel=-110, head=-6))
        ctx.restore()
        if lf < 28:
            label(ctx, "*tap tap tap*", 540, LY + 40, 104, (1, 1, 1), 0.03, pop(lf, 2, 6))
        else:
            label(ctx, "\"Yeah, yeah...\"", 540, LY + 40, 110, YEL, -0.03, pop(lf, 28, 32))
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 38:
        mom_count(ctx, f, lf, "2", "\"TWO...\"", hx('ff5a3c'), zoom0=1.12, rays_col=(1, 0.85, 0.4), lab_col=YEL, lab_size=140)
    else:
        il = lf - 38
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(il, 0, 80)), 2, shake_at(il, [0], 6, 8), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('6fd6ff')); ctx.fill()
        rays(ctx, 540, 900, 240, 1600, il * 0.02, col=(1, 1, 1), a=0.3, n=16)
        face(ctx, BOY, P(eye='smug', mouth='smile', head=0), 500, 900, 290, -0.08)
        # lazy dangling sock
        sock(ctx, 800, 1170, 0.0, 1.0, 0.25 * math.sin(il * 0.25))
        ellipse(ctx, 800, 1160, 58, 50); fl(ctx, BOY['skin'], 6)
        ctx.restore()
        if il < 36:
            label(ctx, "*puts on ONE sock*", 540, LY + 40, 96, (1, 1, 1), 0.03, pop(il, 0, 4))
        else:
            label(ctx, "\"She never gets to THREE.\"", 540, LY + 40, 84, YEL, -0.03, pop(il, 36, 40))
    card(ctx, 'p2', f, 112, 228)


def s3(ctx, f):
    lf = f - 230
    if lf < 80:
        k = 0 if lf < 40 else 1
        il = lf - 40 * k
        num = ("2½", "2¾")[k]
        word = ("\"TWO AND A HALF...\"", "\"TWO AND THREE QUARTERS...\"")[k]
        mom_count(ctx, f, il, num, word, (hx('ff8ac0'), hx('b98aff'))[k], zoom0=1.0 + 0.1 * k, rays_col=(1, 1, 1),
                  eye='shock', mouth='wavy', sweat_=True, lab_col=(1, 1, 1), lab_size=88)
    else:
        il = lf - 80
        # split screen: kid (top) asks, Mom (bottom) freezes
        ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
        cam(ctx, 540, 600, 1.0 + 0.04 * eout(pop(il, 0, 60)), 0, shake_at(il, [0], 6, 8), f, sy=520)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('6fd6ff')); ctx.fill()
        rays(ctx, 540, 600, 200, 1200, il * 0.02, col=(1, 1, 1), a=0.3, n=16)
        face(ctx, BOY, P(eye='smug', mouth='grin', head=0), 540, 660, 220, -0.06)
        ctx.restore()
        ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
        jit = 10 * math.sin(il * 3.1) if il >= 26 else 0
        cam(ctx, 540 + jit, 1230, 1.0 + 0.1 * eout(pop(il, 26, 34)), 0, shake_at(il, [26], 10, 14), f, sy=1220)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('2a2a5a') if il >= 26 else hx('b98aff')); ctx.fill()
        if il >= 26:
            big_num(ctx, "3", 540, 1200, 700, (1, 0.3, 0.4), 0.35)
        face(ctx, MOM, P(eye='shock', mouth='flat' if il < 26 else 'wavy', head=0), 540, 1230, 220, 0.0)
        if il >= 26:
            sweat(ctx, 330, 1050, il * 3, 0.9); sweat(ctx, 700, 1060, il * 3 + 20, 0.8)
            for j in range(3):
                text(ctx, "?", 300 + j * 240, 1100 - 40 * (j % 2) - 6 * math.sin(il * 0.4 + j), 110, YEL, ow=10, ang=0.2 * (j - 1))
        ctx.restore()
        if il >= 26:
            glitch(ctx, il, 960, 1500, 1.0 if il < 40 else 0.4)
        ctx.rectangle(0, 952, W, 16); setc(ctx, OUT); ctx.fill()
        label(ctx, "\"What happens at THREE?\"", 540, 890, 84, YEL, -0.02, pop(il, 2, 6))
        if il >= 30:
            label(ctx, "\"...uh.\"", 540, LY + 40, 120, (1, 1, 1), 0.03, pop(il, 30, 34))
    card(ctx, 'p3', f, 232, 310)


def s4(ctx, f):
    lf = f - 370
    if lf < 58:
        # split screen: Mom whispering into the phone / Grandma
        ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
        cam(ctx, 540, 520, 1.0, 0, 0, f, sy=520)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('b98aff')); ctx.fill()
        rays(ctx, 540, 600, 200, 1200, lf * 0.02, col=(1, 1, 1), a=0.25, n=16)
        face(ctx, MOM, P(eye='shock' if lf >= 28 else 'normal', mouth='open' if lf < 28 else 'scream', head=0), 560, 560, 210, 0.05)
        phone_at_ear(ctx, 560, 560, 210, -1)
        ellipse(ctx, 560 + 0.04 * 210 + 120, 560 + 0.5 * 210, 50, 44); fl(ctx, MOM['skin'], 5)   # hand cupping the whisper
        ctx.restore()
        ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
        cam(ctx, 540, 1240, 1.0 + 0.12 * eout(pop(lf, 28, 34)), 0, shake_at(lf, [28], 12, 20), f, sy=1220)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb85a') if lf < 28 else hx('e0263a')); ctx.fill()
        rays(ctx, 540, 1260, 200, 1200, -lf * 0.04, col=(1, 0.9, 0.5), a=0.4, n=16)
        if lf >= 28:
            big_num(ctx, "1", 300, 1180, 600, (1, 1, 1), 0.3, -0.12)
        face(ctx, GRAN, P(eye='normal' if lf < 28 else 'glare', mouth='smile' if lf < 28 else 'flat', head=0), 540, 1240, 220, -0.04)
        if lf >= 28:
            finger_up(ctx, 820, 1460, 0.9, GRAN['skin'], 0.1 * math.sin(lf * 0.5))
        ctx.restore()
        ctx.rectangle(0, 952, W, 16); setc(ctx, OUT); ctx.fill()
        label(ctx, "\"Mom... what happens at 3?\"", 540, 890, 76, (1, 1, 1), -0.02, pop(lf, 2, 6))
        if lf >= 28:
            label(ctx, "\"ONE...\"", 540, LY + 40, 140, YEL, -0.03, pop(lf, 28, 32))
    else:
        il = lf - 58
        ready = il >= 40
        ctx.save(); cam(ctx, 560, 1080, 1.0 + (0.08 * eout(pop(il, 40, 70)) if ready else 0), 0,
                        shake_at(il, [0, 40], 10, 14) + (5 if not ready else 0), f)
        living(ctx, door=1.0)
        if not ready:
            # super-speed blur: ghost copies zipping all over the room, clothes flying
            rnd = random.Random(il // 2)
            for g in range(5):
                ctx.push_group()
                draw_hip(ctx, rnd.uniform(150, 900), FLOOR - 165, 0.98, rnd.choice([1, -1]), BOY if g % 2 else KID_COAT,
                         P(eye='shock', mouth='scream', rsh=rnd.uniform(-160, 160), rel=-30, lsh=rnd.uniform(-160, 160), lel=-30,
                           lhip=40, lkn=-60, rhip=-40, rkn=-20, torso=rnd.uniform(-20, 20)))
                draw_hip(ctx, rnd.uniform(150, 900), FLOOR - 220, 1.15, rnd.choice([1, -1]), MOM_SLIP if g % 2 else MOM_COAT,
                         P(eye='shock', mouth='scream', rsh=rnd.uniform(-160, 160), rel=-30, lsh=rnd.uniform(-160, 160), lel=-30,
                           lhip=40, lkn=-60, rhip=-40, rkn=-20, torso=rnd.uniform(-20, 20)))
                ctx.pop_group_to_source(); ctx.paint_with_alpha(0.35 + 0.1 * g)
            for j in range(4):   # flying shoes / sock
                ang = il * 0.6 + j
                x = (j * 280 + il * 40) % 1200 - 60; y = 700 + 200 * math.sin(il * 0.3 + j)
                if j % 2:
                    sock(ctx, x, y, ang, 0.6)
                else:
                    ellipse(ctx, x, y, 60, 28, ang); fl(ctx, RED, 5)
            speed_lines(ctx, il)
            for j in range(3):
                puff(ctx, 250 + j * 280, FLOOR - 60, ((il + j * 5) % 15) / 15, 1.5)
        else:
            u = il - 40
            bm = draw_hip(ctx, 700, FLOOR - 220, 1.15, -1, MOM_COAT,
                          P(eye='happy', mouth='grin', rsh=-150, rel=-60, lsh=20, lel=-20, head=-4))
            bk = draw_hip(ctx, 440, FLOOR - 165, 0.98, 1, KID_COAT,
                          P(eye='happy', mouth='grin', rsh=-150, rel=-60, lsh=20, lel=-20, head=4))
            beanie(ctx, bk)
            for b in (bm, bk):
                puff(ctx, b['head'][0], b['head'][1] + 200, pop(u, 0, 14), 2.0)
            for j in range(4):
                sparkle(ctx, 300 + j * 180, 640 + 40 * math.sin(u * 0.3 + j), 26 + 6 * math.sin(u * 0.5 + j), YEL)
        ctx.restore()
        if not ready:
            label(ctx, "*ZOOOOOM!*", 540, LY + 40, 132, YEL, 0.03 * math.sin(il * 0.8), pop(il, 0, 4))
        else:
            label(ctx, "\"READY!\"", 540, LY + 40, 140, (1, 1, 1), -0.03, pop(il, 40, 44))
    if lf >= 58:
        card(ctx, 'p4', f, 428, 498)


def s5(ctx, f):
    lf = f - 500
    if lf < 44:
        # Dad sprawled on the sofa, Mom + kid ready in the doorway
        ctx.save(); cam(ctx, 560, 1080, 0.9 + 0.04 * eout(pop(lf, 0, 44)), 0, shake_at(lf, [0], 6, 8), f)
        living(ctx, door=1.0)
        sofa_back(ctx)
        bd = draw_hip(ctx, 360, SEAT, 1.15, 1, DAD, sit(eye='smug', mouth='grin', rsh=150, rel=-30, lsh=40, lel=-90, head=-6, torso=-10))
        sofa_front(ctx)
        popcorn(ctx, bd['back'][0] + 30, bd['back'][1] - 10, 0.8)
        draw_hip(ctx, 905, FLOOR - 220, 1.15, -1, MOM_COAT, P(eye='smug', mouth='smile', rsh=-60, rel=-80, lsh=130, lel=-110, head=-4))
        bk = draw_hip(ctx, 765, FLOOR - 165, 0.98, -1, KID_COAT, P(eye='smug', mouth='smile', rsh=-130, rel=-110, lsh=130, lel=-110))
        beanie(ctx, bk)
        ctx.restore()
        label(ctx, "\"Pfft. Nobody knows", 540, LY - 50, 82, (1, 1, 1), -0.02, pop(lf, 2, 6))
        label(ctx, "what happens at thr-\"", 540, LY + 50, 82, (1, 1, 1), -0.02, pop(lf, 4, 8))
    elif lf < 64:
        il = lf - 44
        # insert: Mom's phone screen pushed into camera - Grandma: TWO
        ctx.save(); cam(ctx, 540, 1000, 1.1 - 0.1 * eout(pop(il, 0, 6)), 4, shake_at(il, [0], 10, 18), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('e0263a')); ctx.fill()
        rays(ctx, 540, 960, 200, 1600, il * 0.06, col=(1, 0.8, 0.3), a=0.5, n=18)
        rect_r(ctx, 160, 560, 760, 1000, 70); fl(ctx, hx('24243a'), 10)
        rect_r(ctx, 200, 610, 680, 900, 40); setc(ctx, hx('ffd1ea')); ctx.fill()
        ctx.save(); rect_r(ctx, 200, 610, 680, 900, 40); ctx.clip()
        big_num(ctx, "2", 380, 900, 500, (1, 0.2, 0.3), 0.3, -0.12)
        face(ctx, GRAN, P(eye='glare', mouth='flat', head=0), 540, 1020, 250, 0.03)
        ctx.restore()
        ellipse(ctx, 180, 1300, 70, 110); fl(ctx, MOM['skin'], 6)
        ellipse(ctx, 900, 1300, 70, 110); fl(ctx, MOM['skin'], 6)
        ctx.restore()
        label(ctx, "\"TWO...\"", 540, LY + 40, 150, YEL, -0.03, pop(il, 0, 3))
    elif lf < 120:
        il = lf - 64
        # WHOOSH: Dad-shaped hole in the wall, popcorn rain on the empty sofa
        ctx.save(); cam(ctx, 560, 1080, 0.9 + 0.03 * eout(pop(il, 0, 56)), 0, shake_at(il, [0], 14, 22), f)
        living(ctx, door=1.0)
        person_hole(ctx, 380, 830, 0.62 * (1 + 0.3 * (1 - eout(pop(il, 0, 6)))))
        sofa_back(ctx)
        sofa_front(ctx)
        rnd = random.Random(2)
        for k in range(16):   # popcorn rain
            t0 = rnd.uniform(0, 20); x = rnd.uniform(200, 760)
            y = 500 + 26 * max(0, il - t0) ** 1.25
            if y < SEAT - 20:
                ellipse(ctx, x, y, 22, 18, k); fl(ctx, hx('fff6d8'), 4)
            else:
                ellipse(ctx, x, SEAT - 20, 22, 18, k); fl(ctx, hx('fff6d8'), 4)
        popcorn(ctx, 520, SEAT - 40, 0.7, 1.0, il)
        if il < 10:
            for j in range(5):   # dust burst
                puff(ctx, 380 + (j - 2) * 90, 760 + 60 * math.sin(j), il / 10, 2.2)
        draw_hip(ctx, 905, FLOOR - 220, 1.15, -1, MOM_COAT, P(eye='shock' if il < 20 else 'smug', mouth='open' if il < 20 else 'smile',
                                                              rsh=-60, rel=-80, lsh=130, lel=-110, head=-4))
        bk = draw_hip(ctx, 765, FLOOR - 165, 0.98, -1, KID_COAT, P(eye='shock' if il < 20 else 'happy', mouth='open' if il < 20 else 'grin',
                                                                   rsh=-130, rel=-110, lsh=130, lel=-110))
        beanie(ctx, bk)
        ctx.restore()
        if il < 22:
            label(ctx, "*WHOOSH!!*", 540, LY + 40, 140, YEL, -0.04, pop(il, 0, 3))
        elif il < 36:
            label(ctx, "*HONK HONK!*", 540, LY + 40, 120, ORANGE, 0.04, pop(il, 22, 26))
        else:
            label(ctx, "\"...Dad's in the car.\"", 540, LY + 40, 92, (1, 1, 1), -0.02, pop(il, 36, 40))
    else:
        il = lf - 120
        opening_face(ctx, f, il)
    if lf < 120:
        card(ctx, 'p5', f, 502, 618)
    else:
        card(ctx, 'p1', f, 620)


SHOTS = [(0, s1), (110, s2), (230, s3), (370, s4), (500, s5)]
CUTS = (50, 110, 148, 230, 270, 310, 370, 428, 468, 500, 544, 564, 620)


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
                              "-i", "out/counting_to_three_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
