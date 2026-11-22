"""'Saturday 6 AM' - can't wake up for school, wide awake on Saturday. Original, general-audience comedy short, 22s.
Hook: Mom's mid-yell ECU + ringing alarm, caption "SCHOOL DAY:" / "7:00 AM" + "WAKE UP!! SCHOOL!!"
Beat 1: blanket burrito -> *YANK!* blanket flies, kid still asleep "Zzz" -> Mom lifts him up, he MELTS back down *FLOOOP* "...5 more minutes..."
        breakfast: kid's face slowly sinks into the cereal bowl *SPLOOSH!* "...zzz..."
Beat 2: "SATURDAY:" / "6:00 AM" dark ECU -> eyes SNAP open *PING!* -> tornado-dress *ZOOM!* -> checklist DRESSED/TEETH/BED MADE/BREAKFAST ding-ding-ding
Twist:  parents asleep, kid BOINGs on their bed "WAKE UP! WAKE UP!" -> Dad's one bloodshot eye "It's 6 AM... on a SATURDAY." -> pulls blanket over "...5 more minutes."
End:    kid yanks THEIR blanket, ECU mid-yell mirroring Mom "WAKE UP!! IT'S SATURDAY!!" -> groggy Mom "Where was this energy on MONDAY?!" -> loop to hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face, zzz
from scenes48 import label2
from scenes58 import sweat, twitch, arm_to
from scenes12 import alarm_clock
from scenes8 import sit
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'), pants=hx('3d5a9e'))
DAD = dict(doodle.DAD, shirt=hx('7fb8ff'), pants=hx('2a3a6a'))
PJ = dict(doodle.BOY, hood=False, shades=False, shirt=hx('7fe3ff'), pants=hx('7fe3ff'), shoes=hx('7fe3ff'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff8a1f'), pants=hx('2a3a6a'))
N = 660
RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
FLOOR = 1460
KK = 1.15
MK = 1.45

CAPS = {'p1': [[("SCHOOL DAY:", OUT)], [("7:00 AM", RED)]],
        'p2': [[("SATURDAY:", OUT)], [("6:00 AM", GREEN)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ sets / props
def wall(ctx, col, stripes=True):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, col); ctx.fill()
    if stripes:
        for i in range(-30, 40):
            ctx.rectangle(i * 130, -3000, 50, 6000); setc(ctx, dark(col, 0.95)); ctx.fill()


def floor(ctx, col=hx('b86a3c')):
    ctx.rectangle(-3000, FLOOR, 7000, 3000); setc(ctx, col); ctx.fill()
    ctx.move_to(-3000, FLOOR); ctx.line_to(4000, FLOOR); ink(ctx, 7); ctx.stroke()


def bed_head(ctx, cx, top, w, col=hx('5a8ae8')):
    """front-view bed: headboard + pillows; head sits around (cx, top+60)"""
    rect_r(ctx, cx - w / 2 - 30, top - 230, w + 60, 420, 40); fl(ctx, col, 9)
    rect_r(ctx, cx - w / 2, top - 30, w, 1000, 30); fl(ctx, WHITE, 8)


def pillow(ctx, x, y, w=300, h=130):
    rect_r(ctx, x - w / 2, y - h / 2, w, h, 55); fl(ctx, hx('eef6ff'), 7)


def blanket(ctx, x0, x1, y, col=hx('ffc93c'), bump=0.0, stripe=hx('ff8a1f'), yb=2400):
    ctx.move_to(x0, yb); ctx.line_to(x0, y + 40)
    ctx.curve_to(x0 + 40, y - 20 - bump, x1 - 40, y - 20 - bump, x1, y + 40)
    ctx.line_to(x1, yb); ctx.close_path(); fl(ctx, col, 9)
    for k in range(1, 4):
        yy = y + 120 + k * 110
        if yy > yb - 20:
            break
        ctx.move_to(x0 + 10, yy); ctx.line_to(x1 - 10, yy); setc(ctx, stripe); ctx.set_line_width(22); ctx.stroke()


def morning_room(ctx, dark_=False):
    wall(ctx, hx('27306e') if dark_ else hx('8fd8ff'))
    rect_r(ctx, 90, 520, 300, 340, 18); fl(ctx, hx('122050') if dark_ else hx('fff2b0'), 9)
    if dark_:
        ellipse(ctx, 260, 640, 55, 55); setc(ctx, hx('fff2b0')); ctx.fill(); ellipse(ctx, 285, 625, 48, 48); setc(ctx, hx('122050')); ctx.fill()
    else:
        ellipse(ctx, 240, 690, 70, 70); setc(ctx, hx('ffc93c')); ctx.fill()
    ctx.move_to(240, 520); ctx.line_to(240, 860); ctx.move_to(90, 690); ctx.line_to(390, 690); ink(ctx, 8); ctx.stroke()


def bowl(ctx, x, y, s=1.0, front=True):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if not front:
        ellipse(ctx, 0, 0, 220, 55); fl(ctx, hx('fff8ec'), 8)
        for k in range(14):
            ellipse(ctx, -170 + (k * 53) % 340, -10 + (k * 37) % 30 - 15, 22, 15); fl(ctx, GOLD, 4)
    else:
        ctx.move_to(-230, 0); ctx.curve_to(-220, 200, 220, 200, 230, 0); ctx.close_path(); fl(ctx, hx('ff5fa8'), 9)
        ctx.move_to(-200, 60); ctx.curve_to(-60, 80, 60, 80, 200, 60); setc(ctx, WHITE); ctx.set_line_width(14); ctx.stroke()
    ctx.restore()


def big_z(ctx, x, y, lf, s=1.0):
    zzz(ctx, x, y, lf, s)


def splash(ctx, x, y, t, n=12, col=WHITE):
    if t <= 0 or t >= 1:
        return
    rnd = random.Random(3)
    for i in range(n):
        a = rnd.uniform(-math.pi * 0.95, -math.pi * 0.05); v = rnd.uniform(300, 700)
        px = x + math.cos(a) * v * t; py = y + math.sin(a) * v * t + 900 * t * t
        r = rnd.uniform(16, 34) * (1 - t * 0.5)
        ellipse(ctx, px, py, r, r * 1.2); fl(ctx, col, 4)


def speed_lines(ctx, lf, col=(1, 1, 1, 0.8), n=14):
    rnd = random.Random(int(lf) // 2)
    for i in range(n):
        y = rnd.uniform(500, 1500); x = rnd.uniform(-100, 1100); l = rnd.uniform(200, 500)
        ctx.move_to(x, y); ctx.line_to(x + l, y); setc(ctx, col); ctx.set_line_width(rnd.uniform(6, 14)); ctx.stroke()


def bloodshot_eye(ctx, x, y, r, lf):
    ellipse(ctx, x, y, r, r * 1.05); fl(ctx, WHITE, 6)
    setc(ctx, hx('e0263a')); ctx.set_line_width(4)
    for i in range(7):
        a = i * 2 * math.pi / 7 + 0.2
        ctx.move_to(x + math.cos(a) * r * 0.95, y + math.sin(a) * r * 0.95)
        ctx.line_to(x + math.cos(a + 0.25) * r * 0.6, y + math.sin(a + 0.25) * r * 0.6); ctx.stroke()
    j = 3 * math.sin(lf * 1.7)
    ellipse(ctx, x + j, y + r * 0.1, r * 0.28, r * 0.3); setc(ctx, INK); ctx.fill()


def tick(ctx, x, y, s, t):
    if t <= 0:
        return
    sc = s * (0.5 + 0.5 * eout(min(1, t * 2)))
    ctx.save(); ctx.translate(x, y); ctx.scale(sc, sc)
    ellipse(ctx, 0, 0, 44, 44); fl(ctx, GREEN, 6)
    ctx.move_to(-20, 2); ctx.line_to(-6, 18); ctx.line_to(22, -16); setc(ctx, WHITE); ctx.set_line_width(11); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.restore()


# ------------------------------------------------------------------ hook (Mom ECU mid-yell)
def hook_face(ctx, f, lf):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eio(pop(lf, 0, 54)), 0, 6, f)
    wall(ctx, hx('ffb03a'), False)
    rays(ctx, 540, 900, 260, 1500, lf * 0.04, col=(1, 0.95, 0.6), a=0.35, n=18)
    cx, cy, R = 540, 880, 270
    jit = 4 * math.sin(lf * 2.7)
    face(ctx, MOM, P(eye='glare', mouth='scream'), cx + jit, cy, R, 0.04 * math.sin(lf * 0.9))
    twitch(ctx, cx + 0.66 * R, cy - 0.8 * R, lf, 1.3)
    alarm_clock(ctx, 880, 1110, 1.0, True, lf, "7:00")
    # shout lines
    for k in range(5):
        a = -0.5 + k * 0.25
        r0 = 150 + 30 * math.sin(lf * 1.3 + k)
        ctx.move_to(cx + math.cos(a + 1.57) * 0 + math.sin(a) * r0, cy + R * 0.55 + math.cos(a) * r0)
    ctx.new_path()
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook_face(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"WAKE UP!!", "SCHOOL!!\"", WHITE, t, 130, col2=YEL, y=1420)


# ------------------------------------------------------------------ beat 1: burrito -> yank -> melt
def burrito(ctx, f, il):
    # il 0..34: front view bed, lump, YANK at 14
    yanked = il >= 14
    ctx.save(); cam(ctx, 540, 1060, 0.95, 0, shake_at(il, [14], 8, 14), f)
    morning_room(ctx)
    floor(ctx)
    bed_head(ctx, 540, 1000, 780)
    ctx.rectangle(150, FLOOR - 40, 780, 300); fl(ctx, hx('5a8ae8'), 8)
    pillow(ctx, 540, 1010)
    face(ctx, PJ, P(eye='closed', mouth='open'), 540, 1010, 120, 0.25)
    if not yanked:
        blanket(ctx, 150, 930, 900, bump=60 + 8 * math.sin(il * 0.3), yb=FLOOR - 40)
    else:
        t = eout(pop(il, 14, 24))
        ctx.save(); ctx.translate(540 + 900 * t, 1300 - 500 * t); ctx.rotate(0.9 * t)
        blanket(ctx, -390, 390, -300 * (1 - t) - 120, yb=-300 * (1 - t) + 300)
        ctx.restore()
        big_z(ctx, 680, 820, il, 1.2)
    # Mom's hand reaching in from the right
    arm_to(ctx, 1300, 700, lerp(940, 1150, eout(pop(il, 14, 22))), lerp(900, 760, eout(pop(il, 14, 22))), MOM['shirt'], MOM['skin'], bend=-60, w=100)
    ctx.restore()
    if not yanked:
        label(ctx, "\"UP! NOW!\"", 540, 1450, 130, WHITE, -0.03, pop(il, 2, 5))
    else:
        label(ctx, "*YANK!*", 540, 440, 120, YEL, 0.04, pop(il, 14, 17))
        label(ctx, "\"...zzz...\"", 540, 1450, 120, CYAN, -0.03, pop(il, 20, 23))


def lift_melt(ctx, f, il):
    # il 0..70: Mom holds him up (0..30), he melts down (30..52), puddle
    ctx.save(); cam(ctx, 540, 1080, 1.15, 0, shake_at(il, [50], 6, 10), f)
    morning_room(ctx)
    floor(ctx)
    mx = 300
    draw(ctx, mx, FLOOR - 186 * MK, MK, 1, MOM, P(eye='glare', mouth='open', lsh=95, lel=-10, rsh=80, rel=-10, torso=-4))
    kx = 640
    m = eio(pop(il, 30, 52))
    ctx.save(); ctx.translate(kx, FLOOR)
    ctx.scale(1 + 0.7 * m, 1 - 0.78 * m)
    lift = 120 * (1 - m)
    draw(ctx, 0, -186 * KK - lift, KK, -1, PJ, P(eye='closed', mouth='open', lsh=150, lel=0, rsh=-150, rel=0, rot=6 * math.sin(il * 0.2), head=20))
    ctx.restore()
    if m > 0.2:
        ellipse(ctx, kx, FLOOR - 10, 170 * m, 34 * m); setc(ctx, CYAN); ctx.fill()
    if m < 0.5:
        # Mom's hands under his arms
        for dy in (0, 40):
            ellipse(ctx, kx - 70, FLOOR - 186 * KK - lift + 120 + dy, 34, 34); fl(ctx, MOM['skin'], 6)
    big_z(ctx, kx + 150, FLOOR - 470 + 200 * m, il, 1.0)
    ctx.restore()
    if il < 30:
        label(ctx, "\"STAND. UP.\"", 540, 1450, 130, WHITE, -0.03, pop(il, 2, 5))
    else:
        label(ctx, "*FLOOOOP*", 540, 440, 120, CYAN, 0.04, pop(il, 34, 37))
        label(ctx, "\"...5 more minutes...\"", 540, 1450, 110, WHITE, 0.03, pop(il, 44, 47))


def cereal(ctx, f, il):
    # il 0..42: face slowly sinks into cereal bowl, SPLOOSH at 24
    sp = il >= 24
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.08 * eio(pop(il, 0, 24)), 0, shake_at(il, [24], 10, 14), f)
    wall(ctx, hx('ffd9a8'))
    ctx.rectangle(-500, 1300, 2200, 900); fl(ctx, hx('c96a2a'), 8)
    bowl(ctx, 540, 1280, 1.4, front=False)
    ctx.save(); ctx.rectangle(-500, -500, 2200, 1800); ctx.clip()
    d = eio(pop(il, 0, 24))
    face(ctx, PJ, P(eye='closed', mouth='open'), 540, lerp(820, 1150, d), 230, lerp(0.05, 0.25, d) + 0.04 * math.sin(il * 0.4))
    ctx.restore()
    bowl(ctx, 540, 1280, 1.4, front=True)
    splash(ctx, 540, 1250, pop(il, 24, 40), 14, hx('fff8ec'))
    if sp:
        for k in range(5):
            ellipse(ctx, 340 + k * 100, 1230 - 30 * math.sin(il * 0.5 + k), 24, 16); fl(ctx, GOLD, 4)
        zz_t = il - 28
        if zz_t > 0:
            for k in range(3):
                yy = 1150 - ((zz_t * 6 + k * 60) % 200)
                ellipse(ctx, 620 + 30 * k, yy, 18 + 6 * k, 18 + 6 * k); setc(ctx, (1, 1, 1, 0.9)); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()
    if not sp:
        label(ctx, "*nod... nod...*", 540, 1450, 100, WHITE, -0.03, pop(il, 4, 7))
    else:
        label(ctx, "*SPLOOSH!*", 540, 440, 130, YEL, 0.04, pop(il, 24, 27))
        label(ctx, "\"...blub... zzz...\"", 540, 1450, 110, CYAN, -0.03, pop(il, 30, 33))


def s2(ctx, f):
    lf = f - 54
    if lf < 34:
        burrito(ctx, f, lf)
    elif lf < 104:
        lift_melt(ctx, f, lf - 34)
    else:
        cereal(ctx, f, lf - 104)


# ------------------------------------------------------------------ beat 2: Saturday
def sat_wake(ctx, f, il):
    # il 0..40: dark ECU on pillow, eyes snap open at 18
    on = il >= 18
    ctx.save(); cam(ctx, 540, 960, 1.0 + (0.15 * eout(pop(il, 18, 24)) if on else 0.02 * il / 18), 0, shake_at(il, [18], 10, 10), f)
    wall(ctx, hx('1a1f4a') if not on else hx('ffd23f'), False)
    if on:
        rays(ctx, 540, 960, 200, 1500, il * 0.05, col=(1, 1, 1), a=0.45, n=16)
    pillow(ctx, 540, 900, 900, 520)
    face(ctx, PJ, P(eye='shock' if on else 'closed', mouth='grin' if on else 'smile'), 540, 930, 270, 0.0 if on else 0.2)
    blanket(ctx, 0, 1080, 1290, col=hx('3ccfb0') if on else hx('2a7a70'), stripe=hx('2aa890'))
    alarm_clock(ctx, 900, 1120, 0.8, False, il, "6:00")
    if not on:
        big_z(ctx, 820, 640, il, 1.2)
    ctx.restore()
    if on:
        label(ctx, "*PING!*", 540, 1450, 140, RED, -0.04, pop(il, 18, 21))


def tornado(ctx, f, il):
    # il 0..36: spinning blur, clothes fly on; ends dressed, ZOOM out the door
    ctx.save(); cam(ctx, 540, 1100, 1.1, 0, 5, f)
    morning_room(ctx, True)
    floor(ctx, hx('3a2f5a'))
    rnd = random.Random(9)
    d = 1 if (il // 2) % 2 == 0 else -1
    dressed = il >= 18
    ch = KID if dressed else PJ
    x = 540 if il < 26 else lerp(540, 1500, eio(pop(il, 26, 36)))
    if il < 26:
        for k in range(4):
            ctx.new_path(); ctx.arc(540, 1150, 230 + k * 50, il * 0.7 + k, il * 0.7 + k + 2.4); setc(ctx, (1, 1, 1, 0.85)); ctx.set_line_width(12); ctx.stroke()
        draw(ctx, x, FLOOR - 186 * KK, KK, d, ch, P(eye='happy', mouth='grin', lsh=140, rsh=-140))
        # clothes flying in
        for k, col in enumerate((ORANGE, BLUE, RED, GOLD)):
            t = clamp((il - k * 4) / 10)
            if 0 < t < 1:
                a = k * 1.6 + il * 0.3
                rr = 500 * (1 - t)
                rect_r(ctx, 540 + math.cos(a) * rr - 50, 1100 + math.sin(a) * rr - 40, 100, 80, 14); fl(ctx, col, 6)
    else:
        speed_lines(ctx, il)
        draw(ctx, x, FLOOR - 186 * KK, KK, 1, KID, run_pose(il * 0.9, eye='happy', mouth='grin', torso=18))
    ctx.restore()
    label(ctx, "*ZOOOM!*", 540, 440, 130, YEL, 0.04, pop(il, 2, 5))
    if il >= 14:
        label(ctx, "\"IT'S SATURDAY!!!\"", 540, 1450, 130, WHITE, -0.03, pop(il, 14, 17))


def checklist(ctx, f, il):
    # il 0..64: kid proud next to a checklist; four ticks DING DING DING DING
    ctx.save(); cam(ctx, 540, 1000, 1.0, 0, 0, f)
    wall(ctx, hx('8a3cff'), False)
    rays(ctx, 540, 960, 200, 1500, il * 0.03, col=(1, 0.8, 1), a=0.25, n=16)
    rect_r(ctx, 120, 540, 840, 560, 30); fl(ctx, WHITE, 9)
    items = ["DRESSED", "TEETH BRUSHED", "BED MADE", "BREAKFAST"]
    for k, s in enumerate(items):
        y = 640 + k * 125
        text(ctx, s, 470, y, 70, OUT, ow=0, shadow=False)
        tick(ctx, 860, y - 6, 1.0, pop(il, 6 + k * 9, 9 + k * 9))
    alarm_clock(ctx, 300, 1300, 0.8, False, il, "6:03")
    draw(ctx, 830, 1480 - 186 * 0.85, 0.85, -1, KID, P(eye='happy', mouth='grin', lsh=150, lel=20, rsh=30, rel=-60))
    for k in range(4):
        if il >= 6 + k * 9:
            sparkle(ctx, 200 + k * 220, 520 + (k % 2) * 40, 22 + 6 * math.sin(il * 0.5 + k), YEL)
    ctx.restore()
    if il >= 44:
        label(ctx, "*in 3 minutes*", 540, 440, 110, YEL, -0.03, pop(il, 44, 47))


def s3(ctx, f):
    lf = f - 200
    if lf < 40:
        sat_wake(ctx, f, lf)
        card(ctx, 'p2', lf, 0)
    elif lf < 76:
        tornado(ctx, f, lf - 40)
    else:
        checklist(ctx, f, lf - 76)


# ------------------------------------------------------------------ twist: parents
def parents_bed(ctx, f, il):
    # il 0..54: dark, parents asleep; kid BOINGs between them
    ctx.save(); cam(ctx, 540, 1020, 1.05, 0, shake_at(il, [10, 24, 38], 9, 8), f)
    morning_room(ctx, True)
    bed_head(ctx, 540, 1000, 900, hx('8a5ac8'))
    jb = [10, 24, 38]
    bounce = max([math.sin(math.pi * clamp((il - b) / 8)) if 0 <= il - b < 8 else 0 for b in jb] + [0])
    for x0, ch in ((330, DAD), (750, MOM)):
        pillow(ctx, x0, 1000)
        face(ctx, ch, P(eye='closed', mouth='open' if il < 10 else 'frown'), x0, 1000 - 50 * bounce, 115, 0.15 if x0 < 540 else -0.15)
    blanket(ctx, 70, 1010, 1080 - 30 * bounce, col=hx('5ac8ff'), stripe=hx('3a8bd8'))
    # kid bouncing on the bed
    ph = il % 14
    hy = 1050 - 360 * math.sin(math.pi * ph / 14) if il >= 4 else lerp(-600, 1050, il / 4)
    draw(ctx, 540, hy - 186 * 0.9, 0.9, 1, KID, P(eye='happy', mouth='scream', lsh=160, rsh=-160, lhip=20, rhip=-20, lkn=-40, rkn=-40))
    if il < 10:
        zzz(ctx, 330, 820, il, 0.9); zzz(ctx, 760, 820, il + 9, 0.9)
    ctx.restore()
    label(ctx, "*BOING! BOING!*", 540, 440, 110, YEL, 0.04, pop(il, 10, 13))
    label2(ctx, "\"WAKE UP!", "WAKE UP!!\"", WHITE, pop(il, 12, 16), 120, col2=YEL, y=1420)


def dad_eye(ctx, f, il):
    # il 0..46: Dad ECU, one bloodshot eye opens; at 26 pulls blanket over his face
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.1 * eio(pop(il, 0, 26)), 0, 2, f)
    wall(ctx, hx('27306e'), False)
    pillow(ctx, 540, 880, 980, 560)
    cx, cy, R = 540, 900, 290
    face(ctx, DAD, P(eye='closed', mouth='flat'), cx, cy, R, 0.0)
    if il >= 4:
        # one eye open (viewer's right eye)
        ex, ey, er = cx + 0.42 * R, cy + 0.04 * R, 0.17 * R * 1.2
        ellipse(ctx, ex, ey, er * 1.25, er * 1.2); setc(ctx, DAD['skin']); ctx.fill()
        o = eout(pop(il, 4, 10))
        ctx.save(); ctx.translate(ex, ey); ctx.scale(1, max(0.05, o)); ctx.translate(-ex, -ey)
        bloodshot_eye(ctx, ex, ey, er, il)
        ctx.restore()
        ctx.move_to(ex - er * 1.2, ey - er * 1.0); ctx.line_to(ex + er * 1.1, ey - er * 1.35); ink(ctx, 12); ctx.stroke()
    up = eio(pop(il, 26, 36))
    blanket(ctx, -100, 1180, lerp(1340, 560, up), col=hx('5ac8ff'), stripe=hx('3a8bd8'))
    ctx.restore()
    if il < 26:
        label2(ctx, "\"It's 6 AM...", "on a SATURDAY.\"", WHITE, pop(il, 8, 12), 100, col2=YEL, y=1420)
    else:
        label(ctx, "*FWUMP*", 540, 440, 110, WHITE, 0.04, pop(il, 28, 31))
        label(ctx, "\"...5 more minutes.\"", 540, 1450, 115, CYAN, -0.03, pop(il, 32, 35))


def s4(ctx, f):
    lf = f - 340
    if lf < 54:
        parents_bed(ctx, f, lf)
    else:
        dad_eye(ctx, f, lf - 54)


# ------------------------------------------------------------------ end
def kid_yell(ctx, f, il):
    # il 0..60: kid ECU mid-yell, blanket flying away behind; mirrors Mom's hook
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eio(pop(il, 0, 60)), 0, 6 if il > 4 else 14, f)
    wall(ctx, hx('ffb03a'), False)
    rays(ctx, 540, 900, 260, 1500, il * 0.04, col=(1, 0.95, 0.6), a=0.35, n=18)
    t = eout(pop(il, 0, 12))
    ctx.save(); ctx.translate(lerp(540, 1400, t), lerp(1300, 300, t)); ctx.rotate(1.2 * t)
    blanket(ctx, -400, 400, -200, col=hx('5ac8ff'), stripe=hx('3a8bd8'))
    ctx.restore()
    cx, cy, R = 540, 880, 270
    jit = 4 * math.sin(il * 2.7)
    face(ctx, KID, P(eye='glare', mouth='scream'), cx + jit, cy, R, -0.04 * math.sin(il * 0.9))
    twitch(ctx, cx - 0.62 * R, cy - 0.8 * R, il, 1.3)
    alarm_clock(ctx, 200, 1110, 1.0, True, il, "6:05")
    ctx.restore()
    label(ctx, "*YANK!*", 540, 440, 120, YEL, 0.04, pop(il, 0, 3))
    label2(ctx, "\"WAKE UP!!", "IT'S SATURDAY!!\"", WHITE, pop(il, 6, 10), 112, col2=YEL, y=1420)


def mom_groggy(ctx, f, il):
    # il 0..72: Mom ECU, messy hair, droopy, deadpan line
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.08 * eio(pop(il, 0, 72)), 0, 0, f)
    wall(ctx, hx('5a3aa8'), False)
    rays(ctx, 540, 900, 260, 1500, il * 0.01, col=(0.8, 0.6, 1), a=0.2, n=16)
    cx, cy, R = 540, 880, 280
    face(ctx, MOM, P(eye='closed', mouth='flat'), cx, cy, R, 0.06)
    # bags under the eyes
    for ex in (cx - 0.2 * R, cx + 0.42 * R):
        ctx.new_path(); ctx.arc(ex, cy + 0.2 * R, 0.13 * R, 0.3, math.pi - 0.3); setc(ctx, hx('7a4a8a')); ctx.set_line_width(7); ctx.stroke()
    # messy hair strands
    for k in range(5):
        a = -2.4 + k * 0.4
        ctx.move_to(cx + math.cos(a) * R * 0.95, cy - 0.1 * R + math.sin(a) * R * 0.95)
        ctx.curve_to(cx + math.cos(a) * R * 1.3, cy + math.sin(a) * R * 1.3 - 60, cx + math.cos(a + 0.3) * R * 1.4, cy + math.sin(a + 0.3) * R * 1.2, cx + math.cos(a + 0.2) * R * 1.45, cy + math.sin(a + 0.2) * R * 1.35)
        ink(ctx, 12); ctx.stroke()
    ctx.restore()
    label2(ctx, "\"Where was this energy", "on MONDAY?!\"", WHITE, pop(il, 4, 8), 98, col2=YEL, y=1420)


def s5(ctx, f):
    lf = f - 480
    if lf < 60:
        kid_yell(ctx, f, lf)
    elif lf < 132:
        mom_groggy(ctx, f, lf - 60)
    else:
        s1(ctx, f, f - 612)


SHOTS = [(0, s1), (54, s2), (200, s3), (340, s4), (480, s5)]
CUTS = (54, 88, 158, 200, 240, 276, 340, 394, 480, 540, 612)


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
                              "-i", "out/saturday_6am_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
