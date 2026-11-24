"""Dad vs parallel parking - original, general-audience comedy short, 22s.
Hook:   street medium shot: Dad's car jammed at an angle into a gap between two parked cars, Dad leaning out of the
        window looking back, sweating "I GOT THIS!!" + caption "DAD vs PARALLEL PARKING:"; Mom facepalms in her seat.
Beat 1: top-down cam over the parking gap: ATTEMPT #1 *BONK!* car alarm, #4 diagonal "...ALMOST.", #9 sideways across
        the gap, #15 up on the sidewalk; ghost outlines of every failed try pile up.
Beat 2: wide street: a CROWD gathers on the sidewalk with popcorn *munch munch*, the neighbour directs
        "LEFT! LEFT!" ... "...your OTHER left!" while Mom sinks down in her seat.
Turn:   Dad ECU at the wheel (the one close-up): "ONE. MORE." "TRY."
Twist:  the car glides in perfectly *DING!* crowd "YAAAY!!" Dad "...NAILED it." -> "PLOT TWIST:" Mom: "Honey...
        READ the SIGN." -> tilt up to a NO PARKING sign, crowd "OOOOH..." -> Dad ECU "...from the TOP." -> he pulls
        back out, kid with popcorn "AGAIN!!" -> loop to the hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import twitch, sweat
from scenes65 import dog
from scenes60 import car_top
import scenes91
from scenes91 import family_car, street, smoke, motion_lines, wheel, eio, ST0, GY
import scenes13
from scenes13 import card as _card13

RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
MYCOL = hx('2fc4b2'); BACKCOL = hx('ff6b5a'); FRONTCOL = hx('8a5ac8')
DAD = dict(doodle.DAD, shirt=hx('ff8a1f'), pants=hx('3d5a9e'))
MOM = dict(doodle.MOM_G, shirt=hx('ff5fa8'), pants=hx('2f4a8a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('7fd04a'), pants=hx('3d7bff'), shoes=hx('ff3b5c'))
NEI = dict(doodle.NEIGHBOR, shirt=hx('ffc93c'))
NM = dict(doodle.NMOM)
N = 660
CS = 0.8                     # car scale on the street
BACKX, FRONTX, SPOTX = 80, 1300, 650
SIDE = ST0 - 30              # crowd ground on the sidewalk
SIGNX = 1330

CAPS = {'p1': [[("DAD vs ", OUT), ("PARALLEL PARKING:", ORANGE)]],
        'p2': [[("PLOT TWIST:", RED)]]}
scenes13.CAPS = CAPS
card = _card13


def car(ctx, x, col, faces=None, tilt=0.0, spin=0.0, s=CS, lf=0, f_=1, bounce=0.0):
    old = scenes91.CARCOL
    scenes91.CARCOL = col
    family_car(ctx, x, GY, s, faces or {}, spin=spin, tilt=tilt, f_=f_, lf=lf, bounce=bounce)
    scenes91.CARCOL = old


def dad_out(ctx, x, tilt, p, lf, s=CS, arm=True):
    """Dad leaning out of the driver window, looking back over his shoulder"""
    ctx.save(); ctx.translate(x, GY); ctx.rotate(tilt); ctx.scale(s, s)
    if arm:
        rect_r(ctx, 60, -250, 140, 46, 22); fl(ctx, DAD['shirt'], 6)
        ellipse(ctx, 50, -228, 34, 30); fl(ctx, DAD['skin'], 5)
    ctx.save(); ctx.rectangle(-600, -900, 1200, 692); ctx.clip()
    face(ctx, DAD, p, 150, -300, 82, -0.12 + 0.04 * math.sin(lf * 0.5), -1)
    ctx.restore()
    ctx.restore()


def mom_faces(mood, lf=0):
    if mood == 'palm':
        return P(eye='closed', mouth='frown', head=-6)
    if mood == 'sink':
        return P(eye='glare', mouth='flat')
    if mood == 'cheer':
        return P(eye='happy', mouth='grin')
    if mood == 'point':
        return P(eye='smug', mouth='smile')
    return P(eye='normal', mouth='smile')


def mom_hand(ctx, x, tilt, mood, lf, s=CS):
    """hand over the face in the middle window (facepalm) or pointing up"""
    ctx.save(); ctx.translate(x, GY); ctx.rotate(tilt); ctx.scale(s, s)
    if mood == 'palm':
        ellipse(ctx, -36, -262, 30, 20, 0.4); fl(ctx, MOM['skin'], 4)
    elif mood == 'point':
        ctx.move_to(-40, -250); ctx.line_to(-30, -400 - 10 * math.sin(lf * 0.6)); setc(ctx, INK); ctx.set_line_width(30)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        ctx.move_to(-40, -250); ctx.line_to(-30, -400 - 10 * math.sin(lf * 0.6)); setc(ctx, MOM['skin']); ctx.set_line_width(20); ctx.stroke()
    ctx.restore()


def sign(ctx, x, lf=0):
    ctx.rectangle(x - 12, 600, 24, SIDE - 600); fl(ctx, hx('9aa4b8'), 5)
    rect_r(ctx, x - 150, 330, 300, 300, 22); fl(ctx, WHITE, 8)
    ctx.new_path(); ctx.arc(x, 450, 95, 0, 2 * math.pi); fl(ctx, WHITE, 0)
    ctx.new_path(); ctx.arc(x, 450, 95, 0, 2 * math.pi); setc(ctx, RED); ctx.set_line_width(22); ctx.stroke()
    text(ctx, "P", x, 492, 120, BLUE, ow=0, shadow=False)
    ctx.move_to(x - 66, 384); ctx.line_to(x + 66, 516); setc(ctx, RED); ctx.set_line_width(22); ctx.stroke()
    text(ctx, "NO PARKING", x, 604, 44, RED, ow=0, shadow=False)


def popcorn(ctx, x, y, s=1.0):
    poly(ctx, [(x - 34 * s, y - 70 * s), (x + 34 * s, y - 70 * s), (x + 24 * s, y), (x - 24 * s, y)]); fl(ctx, WHITE, 5)
    for k in range(3):
        ctx.rectangle(x - 26 * s + k * 20 * s, y - 68 * s, 9 * s, 66 * s); setc(ctx, RED); ctx.fill()
    for k in range(5):
        ellipse(ctx, x - 28 * s + k * 14 * s, y - 80 * s - 8 * (k % 2) * s, 13 * s, 12 * s); fl(ctx, hx('fff6c8'), 3)


def crowd(ctx, lf, mode='watch'):
    """mode: watch / direct / other / cheer / ooh / again"""
    ch = mode in ('cheer',)
    bob = 6 * math.sin(lf * 0.5)
    # neighbour directing
    if mode == 'direct':
        p = P(eye='happy', mouth='open', lsh=-150 + 20 * math.sin(lf * 0.7), lel=-20, rsh=40, rel=60)
    elif mode == 'other':
        p = P(eye='glare', mouth='open', lsh=120, lel=20, rsh=-150, rel=-20 + 20 * math.sin(lf * 0.7), head=8)
    elif ch:
        p = P(eye='happy', mouth='grin', lsh=-160, lel=-10, rsh=160, rel=10)
    elif mode == 'ooh':
        p = P(eye='shock', mouth='open', lsh=-40, lel=-120, rsh=40, rel=120)
    else:
        p = P(eye='normal', mouth='smile', lsh=20, lel=20, rsh=-20, rel=-20)
    draw(ctx, 300, SIDE - 186 * 1.0 - (bob if ch else 0), 1.0, 1, NEI, p)
    # neighbour mom with popcorn
    pm = P(eye='happy' if ch else ('shock' if mode == 'ooh' else 'normal'), mouth='grin' if ch else ('open' if mode == 'ooh' else 'smile'),
           lsh=-160 if ch else 30, lel=0 if ch else 100, rsh=160 if ch else -30, rel=0 if ch else -90, head=-6)
    d = draw(ctx, 540, SIDE - 186 * 0.95 - (bob if ch else 0), 0.95, 1, NM, pm)
    if not ch:
        popcorn(ctx, 540, d['head'][1] + 230, 1.1)
    # kid with popcorn (munching)
    pk = P(eye='happy' if ch or mode == 'again' else ('shock' if mode == 'ooh' else 'normal'),
           mouth='grin' if ch or mode == 'again' else ('open' if (lf // 4) % 2 or mode == 'ooh' else 'smile'),
           lsh=-160 if ch or mode == 'again' else 20, lel=0 if ch else 90, rsh=160 if ch else -20, rel=0 if ch else -90)
    d = draw(ctx, 790, SIDE - 186 * 0.75 - (bob if ch or mode == 'again' else 0), 0.75, -1, KID, pk)
    if not ch:
        popcorn(ctx, 790, d['head'][1] + 175, 0.9)
    dog(ctx, 1000, SIDE - 10, 0.5, -1, lf)
    if ch:
        rnd = random.Random(lf // 2)
        for k in range(18):
            ctx.rectangle(rnd.uniform(-200, 1400), (rnd.uniform(500, 1500) + lf * 18) % 1200 + 400, 18, 28)
            setc(ctx, (PINK, GOLD, CYAN, GREEN)[k % 4]); ctx.fill()


def scene_street(ctx, f, lf, camx, camy, zoom, my_x, my_tilt, dad_p, mom_mood, crowd_mode=None, rot=0.0, shk=0,
                 kid_p=None, dad_in=None):
    ctx.save(); cam(ctx, camx, camy, zoom, rot, shk, f)
    street(ctx, lf)
    sign(ctx, SIGNX, lf)
    if crowd_mode:
        crowd(ctx, lf, crowd_mode)
    car(ctx, BACKX, BACKCOL, lf=lf)
    car(ctx, FRONTX, FRONTCOL, lf=lf)
    faces = {'kid': kid_p or P(eye='happy', mouth='grin'), 'mom': mom_faces(mom_mood, lf)}
    if mom_mood == 'sink':
        faces['mom'] = None
    if dad_in is not None:
        faces['dad'] = dad_in
    car(ctx, my_x, MYCOL, faces, tilt=my_tilt, spin=my_x * 0.02, lf=lf)
    if mom_mood == 'sink':   # only Mom's eyes peeking over the door
        ctx.save(); ctx.translate(my_x, GY); ctx.rotate(my_tilt); ctx.scale(CS, CS)
        ctx.save(); poly(ctx, [(-110, -198), (-110, -306), (10, -306), (10, -198)]); ctx.clip()
        face(ctx, MOM, P(eye='glare', mouth='flat'), -50, -150, 46, 0, 1)
        ctx.restore(); ctx.restore()
    mom_hand(ctx, my_x, my_tilt, mom_mood, lf)
    if dad_p is not None:
        dad_out(ctx, my_x, my_tilt, dad_p, lf)
    ctx.restore()


# ------------------------------------------------------------------ shot 1: hook
HOOKX, HOOKT = 760, 0.13


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    wob = 6 * math.sin(lf * 0.9)
    scene_street(ctx, f, lf, 740, 1580, 1.5 + 0.04 * eio(pop(lf, 0, 40)), HOOKX + wob, HOOKT,
                 P(eye='shock', mouth='scream'), 'palm', shk=shake_at(lf, [0], 7, 8))
    # sweat drops flying off Dad
    ctx.save(); cam(ctx, 740, 1580, 1.5 + 0.04 * eio(pop(lf, 0, 40)), 0, 0, f)
    sweat(ctx, HOOKX + 40, GY - 330, lf, 1.0)
    ctx.restore()
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"I GOT THIS!!\"", 540, 1420, 140, WHITE, -0.04, t)


# ------------------------------------------------------------------ shot 2: top-down attempts
CURBX = 780
GAP0, GAP1 = 700, 1300
TRY = [  # (t0, t1, final x, y, angle, attempt label, sfx, sfx colour, quip)
    (0, 34, 640, 1250, 0.55, "ATTEMPT #1", "*BONK!*", RED, None),
    (34, 66, 520, 1000, 0.95, "ATTEMPT #4", "*SCREECH!*", ORANGE, "\"...ALMOST.\""),
    (66, 98, 640, 1000, math.pi / 2, "ATTEMPT #9", "*BUMP!*", RED, "\"...CLOSE?\""),
    (98, 130, 940, 1000, 0.0, "ATTEMPT #15", "*KA-THUNK!*", PURPLE, "\"...wrong SIDE.\""),
]


def top_bg(ctx, il):
    ctx.rectangle(-2000, -2000, 5000, 6000); setc(ctx, hx('6a6f80')); ctx.fill()
    for k in range(-4, 12):                         # lane dashes
        rect_r(ctx, 200, k * 260 + 40, 20, 150, 8); setc(ctx, hx('fff2a8')); ctx.fill()
    ctx.rectangle(CURBX, -2000, 3000, 6000); setc(ctx, hx('e4e0d8')); ctx.fill()
    ctx.move_to(CURBX, -2000); ctx.line_to(CURBX, 4000); ink(ctx, 7); ctx.stroke()
    for k in range(-8, 20):
        ctx.move_to(CURBX, k * 180); ctx.line_to(CURBX + 340, k * 180)
    setc(ctx, hx('c8c2b8')); ctx.set_line_width(4); ctx.stroke()
    ctx.rectangle(CURBX + 340, -2000, 3000, 6000); setc(ctx, hx('6fd06a')); ctx.fill()
    for y in (260, 980, 1700):                       # trees from above
        ctx.new_path(); ctx.arc(CURBX + 470, y, 110, 0, 2 * math.pi); fl(ctx, hx('3fbf4a'), 6)
        ctx.new_path(); ctx.arc(CURBX + 440, y - 30, 40, 0, 2 * math.pi); setc(ctx, hx('6fe06a')); ctx.fill()
    ctx.new_path(); ctx.arc(CURBX + 260, 760, 30, 0, 2 * math.pi); fl(ctx, RED, 5)   # hydrant
    # painted parking box
    ctx.rectangle(CURBX - 280, GAP0 - 40, 270, GAP1 - GAP0 + 80); setc(ctx, WHITE); ctx.set_line_width(8)
    ctx.set_dash([26, 18]); ctx.stroke(); ctx.set_dash([])


def try_pose(j, il):
    t0, t1, x1, y1, a1 = TRY[j][:5]
    u = eio(pop(il, t0, t0 + 18))
    x = lerp(290, x1, u); y = lerp(1950, y1, u); a = lerp(0.0, a1, eio(pop(il, t0 + 6, t0 + 18)))
    return x, y, a


def top_shot(ctx, f, il, labels=True):
    # il 0..140
    j = min(3, max(k for k in range(4) if TRY[k][0] <= il)) if il < 130 else 3
    ctx.save(); cam(ctx, 600, 1000, 1.0 + 0.05 * eio(il / 140), 0.0, shake_at(il, [t[0] + 18 for t in TRY], 7, 7), f)
    top_bg(ctx, il)
    car_top(ctx, CURBX - 140, GAP1 + 290, 1.35, BACKCOL, 0.0, blink=(0.5 + 0.5 * math.sin(il * 1.3)) if 18 <= il < 66 else 0.0)
    car_top(ctx, CURBX - 140, GAP0 - 290, 1.35, FRONTCOL, 0.0)
    for k in range(j):                                # ghosts of failed tries
        x, y, a = try_pose(k, TRY[k][1])
        ctx.save(); ctx.push_group(); car_top(ctx, x, y, 1.35, MYCOL, a); ctx.pop_group_to_source(); ctx.paint_with_alpha(0.3); ctx.restore()
    x, y, a = try_pose(j, il)
    car_top(ctx, x, y, 1.35, MYCOL, a)
    if il - TRY[j][0] < 18:
        smoke(ctx, x, y + 200, pop(il, TRY[j][0], TRY[j][0] + 18), 0.8)
    ctx.restore()
    if not labels:
        return
    t0, t1 = TRY[j][0], TRY[j][1]
    label(ctx, TRY[j][5], 540, 1380, 110, GOLD, (-0.04, 0.04, -0.03, 0.03)[j], pop(il, t0, t0 + 3))
    if il >= t0 + 18:
        label(ctx, TRY[j][6], 540, 680, 110, TRY[j][7], 0.05, pop(il, t0 + 18, t0 + 21))
        if j == 0:
            label(ctx, "*WEE-OO WEE-OO*", 540, 1530, 80, WHITE, -0.03, pop(il, t0 + 22, t0 + 25))
        elif TRY[j][8]:
            label(ctx, TRY[j][8], 540, 1530, 100, WHITE, -0.03, pop(il, t0 + 22, t0 + 25))


def s2(ctx, f):
    il = f - 60
    if il < 130:
        top_shot(ctx, f, il)
    else:
        top_shot(ctx, f, 129, False)
        label2(ctx, "20 MINUTES", "LATER...", WHITE, pop(il, 130, 133), 110, col2=GOLD, y=1000)


# ------------------------------------------------------------------ shot 3: the crowd
def s3(ctx, f):
    il = f - 200
    # Dad's car shuffles back and forth in the gap
    x = SPOTX + 120 + 90 * math.sin(il * 0.22)
    tl = 0.10 + 0.05 * math.sin(il * 0.22 + 1)
    mode = 'watch' if il < 45 else ('direct' if il < 90 else 'other')
    scene_street(ctx, f, il, 600, 1330, lerp(0.98, 1.06, eio(il / 130)), x, tl, P(eye='glare', mouth='wavy') if il < 90 else P(eye='shock', mouth='open'),
                 'sink' if il >= 45 else 'palm', mode)
    if il < 45:
        label2(ctx, "A CROWD", "GATHERS...", WHITE, pop(il, 2, 6), 110, col2=GOLD, y=1560)
        label(ctx, "*munch munch*", 540, 470, 80, ORANGE, -0.04, pop(il, 14, 17))
    elif il < 90:
        label(ctx, "\"LEFT! LEFT!\"", 540, 1580, 130, WHITE, 0.03, pop(il, 46, 49))
        label(ctx, "*BEEP BEEP BEEP*", 540, 470, 80, ORANGE, -0.04, pop(il, 50, 53))
    else:
        label2(ctx, "\"...your OTHER", "LEFT!\"", WHITE, pop(il, 91, 94), 110, col2=RED, y=1560)


# ------------------------------------------------------------------ shot 4: Dad ECU (the one close-up)
def car_interior(ctx, il):
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('8fd8ff')); ctx.fill()
    for k, (hx0, col) in enumerate(((-200, hx('ffe08a')), (500, hx('a8e0ff')), (1150, hx('ffc2d8')))):
        ctx.rectangle(hx0, 560, 520, 400); fl(ctx, col, 6)
        rect_r(ctx, hx0 + 80, 640, 130, 120, 10); fl(ctx, hx('bfe6ff'), 5)
    ctx.rectangle(-600, 900, 2400, 400); setc(ctx, hx('e4e0d8')); ctx.fill()
    ctx.rectangle(-600, -600, 2400, 760); setc(ctx, hx('3a3f55')); ctx.fill()
    rect_r(ctx, -40, 150, 1160, 900, 60); ink(ctx, 14); ctx.stroke()
    ctx.rectangle(-600, 1250, 2400, 1600); setc(ctx, hx('3a3f55')); ctx.fill()
    rect_r(ctx, 200, 700, 680, 900, 140); fl(ctx, hx('ff8a6a'), 8)
    ctx.move_to(260, 1000); ctx.line_to(820, 1000); setc(ctx, hx('e06a50')); ctx.set_line_width(8); ctx.stroke()
    # little air freshener tree hanging from the mirror
    ctx.move_to(880, 150); ctx.line_to(880, 300); ink(ctx, 4); ctx.stroke()
    poly(ctx, [(880, 290), (840, 380), (920, 380)]); fl(ctx, GREEN, 5)


def dad_ecu(ctx, f, il, lines, mood=0):
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.06 * eio(il / 70), 0, 2 + shake_at(il, [0, 30], 6, 8), f)
    car_interior(ctx, il)
    face(ctx, DAD, P(eye='glare', mouth='flat' if mood == 0 else 'wavy'), 540, 900, 200, 0.0)
    twitch(ctx, 540 + 200 * 0.95, 900 - 200 * 0.7, il, 1.6)
    sweat(ctx, 540 - 230, 760, il, 1.4)
    wheel(ctx, 540, 1460, 330, 0.5 * math.sin(il * 0.25) if mood == 0 else 0.08 * math.sin(il * 0.7))
    for sx in (-1, 1):
        ellipse(ctx, 540 + sx * 300, 1230, 56, 64); fl(ctx, DAD['skin'], 6)
    ctx.restore()
    if len(lines) == 1:
        label(ctx, lines[0], 540, 1430, 150, WHITE, -0.03, pop(il, 3, 7))
    else:
        if il < 32:
            label(ctx, lines[0], 540, 1430, 160, WHITE, -0.03, pop(il, 3, 7))
        else:
            label(ctx, lines[1], 540, 1430, 170, RED, 0.03, pop(il, 32, 35))


def s4(ctx, f):
    dad_ecu(ctx, f, f - 330, ["\"ONE. MORE.\"", "\"TRY.\""])


# ------------------------------------------------------------------ shot 5: perfect park -> twist -> loop
def perfect(ctx, f, il):
    # il 0..60: glides in 0-24 ; 25 *DING!* crowd YAAAY ; 42 "...NAILED it."
    u = eio(pop(il, 0, 24))
    x = lerp(1000, SPOTX, u); tl = lerp(0.16, 0.0, eio(pop(il, 6, 24)))
    done = il >= 25
    scene_street(ctx, f, il, 640, 1360, 1.02, x, tl, P(eye='smug', mouth='smile') if done else P(eye='glare', mouth='flat'),
                 'cheer' if done else 'sink', 'cheer' if done else 'watch', shk=shake_at(il, [25], 5, 6),
                 kid_p=P(eye='happy', mouth='grin'))
    if done:
        ctx.save(); cam(ctx, 640, 1360, 1.02, 0, 0, f)
        for j in range(5):
            sparkle(ctx, SPOTX + (-300, -120, 80, 260, 360)[j], GY - (330, 420, 380, 300, 420)[j], 24 + 8 * math.sin(il * 0.6 + j), GOLD)
        ctx.restore()
        label(ctx, "*DING!*", 540, 470, 120, GOLD, -0.05, pop(il, 25, 28))
    if il < 42:
        label(ctx, "*swoosh*" if not done else "\"YAAAY!!\"", 540, 1580, 130, WHITE if done else CYAN, 0.03, pop(il, 3, 6) if not done else pop(il, 25, 28))
    else:
        label(ctx, "\"...NAILED it.\"", 540, 1580, 130, WHITE, -0.03, pop(il, 42, 45))


def twist(ctx, f, il):
    # il 0..70: Mom points "Honey... READ the SIGN." -> tilt up to NO PARKING (30-46) -> crowd "OOOOH..."
    up = eio(pop(il, 28, 46))
    camy = lerp(1360, 820, up); zoom = lerp(1.02, 1.3, up); camx = lerp(640, SIGNX - 60, up)
    scene_street(ctx, f, il, camx, camy, zoom, SPOTX, 0.0, P(eye='smug', mouth='smile') if il < 46 else P(eye='shock', mouth='open'),
                 'point', 'ooh' if il >= 46 else 'watch')
    if il < 28:
        label2(ctx, "\"Honey...", "READ the SIGN.\"", WHITE, pop(il, 4, 8), 110, col2=CYAN, y=1560)
    elif il >= 48:
        label(ctx, "\"OOOOH...\"", 480, 1020, 140, GOLD, 0.04, pop(il, 48, 51))
    card(ctx, 'p2', il, 0, 28)


def pull_out(ctx, f, il):
    # il 0..50: car pulls back out to the hook pose *VROOM*, kid "AGAIN!!"
    u = eio(pop(il, 4, 30))
    x = lerp(SPOTX, HOOKX, u); tl = lerp(0.0, HOOKT, u)
    scene_street(ctx, f, il, lerp(640, 700, u), lerp(1360, 1500, u), lerp(1.02, 1.2, u), x, tl, P(eye='glare', mouth='flat'), 'palm', 'again')
    label(ctx, "*VROOM!*", 540, 470, 110, ORANGE, -0.05, pop(il, 4, 7))
    label(ctx, "\"AGAIN!! AGAIN!!\"", 540, 1580, 130, WHITE, 0.03, pop(il, 18, 21))


def s5(ctx, f):
    lf = f - 400
    if lf < 60:
        perfect(ctx, f, lf)
    elif lf < 130:
        twist(ctx, f, lf - 60)
    elif lf < 180:
        dad_ecu(ctx, f, lf - 130, ["\"...from the TOP.\""], mood=1)
    elif lf < 230:
        pull_out(ctx, f, lf - 180)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (60, s2), (200, s3), (330, s4), (400, s5)]
CUTS = (60, 200, 330, 400, 460, 530, 580, 630)


def render(f):
    import sketch
    sketch.BOIL[0] = f // 4
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.0, 0.05, 0.15, 0.2)
    ctx.set_source(g); ctx.paint()
    for c in CUTS:
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.5 * (1 - (f - c) / 3))); ctx.fill()
    sketch.paper(s)
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/v{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/dad_vs_parallel_parking_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
