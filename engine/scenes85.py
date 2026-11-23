"""'Dad vs the snow plow' - original, general-audience comedy short, 22s.
Hook:   snowy front-yard medium shot: red-faced Dad shovelling the last bit of the driveway
        "ALMOST... DONE...!!" + caption "DAD vs THE SNOW PLOW:"
Beat 1: "DONE! PERFECT." *DING* -> *VRRRMMM* a snow plow roars past on the street *FWOOOSH!!*
        -> a giant snow wall blocks the driveway, only Dad's eyes peek over "...WHAT?!"
Beat 2: Dutch-tilt speed shovelling *SCRAPE!* x3 "DONE...!" -> the plow comes back the other way -> bigger wall "...AGAIN?!"
Beat 3: Dad stands in the street with a STOP sign "NOT. THIS. TIME." -> plow *SCREEECH* stops -> "HA! VICTORY!"
        -> the pine branch above him *creeeak* *FWUMP!* -> Dad is a snowman "...REALLY?"
        ECU: Dad's face poking out of the snow, teeth chattering "...I LOVE... WINTER."
Twist:  "PLOT TWIST: THE NEIGHBOUR GOT A SNOWBLOWER." neighbour clears his drive in seconds - the whole arc lands on Dad.
        "Morning, neighbour!" -> Dad buried to the neck "...morning." -> bursts out, grabs the shovel -> loop to the hook."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, rays, face
from scenes48 import label2
from scenes58 import sweat, twitch
import scenes13
from scenes13 import card as _card13


def eio(t):
    return 0.5 - 0.5 * math.cos(math.pi * clamp(t))


RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
SNOW = hx('f7fbff'); SNOW_S = hx('cfe3f7'); ICE = hx('a8d8ff')
DAD = dict(doodle.DAD, shirt=hx('3ccfb0'), pants=hx('34477e'), shoes=hx('7a4a2c'))
DAD_R = dict(DAD, skin=hx('f07a6a'))
DAD_B = dict(DAD, skin=hx('b8d4f0'))                     # frozen blue
NB = dict(doodle.NEIGHBOR, shirt=hx('9b4dff'), pants=hx('2a3a6a'))
KID = dict(doodle.BOY, hood=False, shades=False, shirt=hx('ff5fa8'))
DRV = dict(doodle.UNCLE, shirt=hx('ff8a1f'))
N = 660
HZ = 1190             # house bottom / lawn line
GND = 1560            # Dad's feet on the driveway
ST0, ST1 = 1660, 1990  # street band
SGND = 1820           # feet in the street
KD = 1.15
DX = 820              # Dad on the driveway

CAPS = {'p1': [[("DAD vs ", OUT), ("THE SNOW PLOW:", BLUE)]],
        'p2': [[("PLOT TWIST:", RED)], [("THE NEIGHBOUR GOT A ", OUT), ("SNOWBLOWER.", PURPLE)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ small helpers
def blob(ctx, x0, x1, gy, h, seed=1, col=SNOW, lw=6):
    """lumpy snow mound from x0..x1 resting on gy, height h"""
    if h <= 2:
        return
    rnd = random.Random(seed)
    n = max(3, int((x1 - x0) / 110))
    ctx.new_path(); ctx.move_to(x0, gy)
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        env = math.sin(math.pi * (0.15 + 0.7 * i / n)) ** 0.6
        y = gy - h * env * rnd.uniform(0.85, 1.05)
        if i == 0:
            ctx.line_to(x, gy - h * 0.35)
        ctx.curve_to(x - (x1 - x0) / n * 0.6, y - 30, x - (x1 - x0) / n * 0.2, y - 30, x, y)
    ctx.line_to(x1, gy); ctx.close_path()
    path = ctx.copy_path()
    fl(ctx, col, lw)
    ctx.save(); ctx.new_path(); ctx.append_path(path); ctx.clip()
    ctx.rectangle(x0 - 50, gy - h * 0.28, x1 - x0 + 100, h); setc(ctx, (0.75, 0.86, 0.97, 0.55)); ctx.fill()
    for k in range(4):
        sparkle(ctx, lerp(x0, x1, rnd.uniform(0.15, 0.85)), gy - h * rnd.uniform(0.45, 0.8), 10, WHITE)
    ctx.restore()


def chunks(ctx, x0, y0, x1, y1, u, n=7, seed=2, r=22, arc=260):
    """snow clumps flying from (x0,y0) to (x1,y1), progress u 0..1"""
    if u <= 0 or u >= 1:
        return
    rnd = random.Random(seed)
    for k in range(n):
        v = clamp(u * rnd.uniform(0.85, 1.2) - k * 0.03)
        if v <= 0 or v >= 1:
            continue
        x = lerp(x0, x1, v) + rnd.uniform(-40, 40); y = lerp(y0, y1, v) - arc * 4 * v * (1 - v) + rnd.uniform(-30, 30)
        rr = r * rnd.uniform(0.6, 1.2)
        ellipse(ctx, x, y, rr, rr * 0.85, k); fl(ctx, SNOW, 4)


def hat(ctx, d, col=RED, snowy=False):
    hx_, hy_ = d['head']; R = d['R']
    ctx.new_path(); ctx.arc(hx_ - R * 0.04, hy_ - R * 0.3, R * 0.95, math.pi * 1.02, math.pi * 1.98); ctx.close_path(); fl(ctx, col, 5)
    for k in range(5):                                                # knit ribs
        x = hx_ - R * 0.6 + k * R * 0.28
        ctx.move_to(x, hy_ - R * 0.45); ctx.line_to(x + R * 0.04, hy_ - R * 0.9)
    setc(ctx, dark(col, 0.82)); ctx.set_line_width(4); ctx.stroke()
    rect_r(ctx, hx_ - R * 1.02, hy_ - R * 0.48, R * 1.96, R * 0.3, R * 0.12); fl(ctx, WHITE, 5)
    ellipse(ctx, hx_ - R * 0.04, hy_ - R * 1.3, R * 0.24, R * 0.22); fl(ctx, WHITE, 5)
    if snowy:
        blob(ctx, hx_ - R * 0.9, hx_ + R * 0.8, hy_ - R * 1.05, R * 0.45, 9, lw=4)


def shovel(ctx, back, front, L=260, load=0.0, col=hx('ff8a1f')):
    """shovel through both hands; the blade sits past the front hand."""
    dx, dy = front[0] - back[0], front[1] - back[1]
    d = math.hypot(dx, dy) or 1; ux, uy = dx / d, dy / d
    s0 = (back[0] - ux * 40, back[1] - uy * 40); s1 = (front[0] + ux * L, front[1] + uy * L)
    ctx.move_to(*s0); ctx.line_to(*s1)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); setc(ctx, INK); ctx.set_line_width(26); ctx.stroke_preserve()
    setc(ctx, hx('c98a4a')); ctx.set_line_width(16); ctx.stroke()
    rect_r(ctx, s0[0] - 26, s0[1] - 14, 52, 28, 12); fl(ctx, hx('2a2840'), 4)     # grip
    a = math.atan2(uy, ux)
    ctx.save(); ctx.translate(*s1); ctx.rotate(a)
    if load > 0:
        ellipse(ctx, 70, -40 * load, 80 * load + 20, 50 * load + 10); fl(ctx, SNOW, 4)
    poly(ctx, [(-10, -70), (130, -86), (150, 86), (-10, 70)]); fl(ctx, col, 6)
    ctx.move_to(10, -50); ctx.line_to(120, -60); setc(ctx, (1, 1, 1, 0.5)); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()
    return s1


def stop_sign(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.rectangle(-9, 0, 18, 330); fl(ctx, hx('b8c0d4'), 4)
    pts = [(math.cos(math.pi / 8 + k * math.pi / 4) * 110, math.sin(math.pi / 8 + k * math.pi / 4) * 110) for k in range(8)]
    poly(ctx, pts); fl(ctx, hx('e8232f'), 6)
    pts2 = [(x_ * 0.86, y_ * 0.86) for x_, y_ in pts]
    poly(ctx, pts2); setc(ctx, WHITE); ctx.set_line_width(6); ctx.stroke()
    text(ctx, "STOP", 0, 14, 64, WHITE, ow=0, shadow=False)
    ctx.restore()


def snow_fall(ctx, lf, n=34, a=0.85, seed=5):
    """screen-space falling snow"""
    rnd = random.Random(seed)
    for k in range(n):
        x = rnd.uniform(-40, 1120); sp = rnd.uniform(3, 7); r = rnd.uniform(5, 12)
        y = (rnd.uniform(0, 2000) + lf * sp) % 2000 - 40
        x += 26 * math.sin(lf * 0.05 + k)
        ellipse(ctx, x, y, r, r); setc(ctx, (1, 1, 1, a)); ctx.fill()


# ------------------------------------------------------------------ the snow plow
def plow(ctx, x, gy, s=1.0, f_=1, lf=0, drv_eye='happy', drv_mouth='grin', spray=0.0, wave=0.0):
    """snow plow truck side view, facing f_ (1 = right). (x, gy) = bottom centre."""
    ctx.save(); ctx.translate(x, gy); ctx.scale(s * f_, s)
    # spray in front of the blade
    if spray > 0:
        rnd = random.Random(lf)
        for k in range(14):
            u = rnd.uniform(0, 1)
            ellipse(ctx, 430 + 260 * u, -120 - 300 * u * (1 - u) * 2 - rnd.uniform(0, 80), 26 + 20 * u, 22 + 16 * u, k)
            setc(ctx, (1, 1, 1, 0.95 * spray)); ctx.fill_preserve(); setc(ctx, INK + (0.6 * spray,)); ctx.set_line_width(4); ctx.stroke()
    # body
    rect_r(ctx, -360, -250, 470, 170, 26); fl(ctx, hx('ffb020'), 8)              # dump bed
    for k in range(4):
        ctx.move_to(-330 + k * 110, -230); ctx.line_to(-330 + k * 110, -100)
    setc(ctx, dark(hx('ffb020'), 0.82)); ctx.set_line_width(6); ctx.stroke()
    blob(ctx, -350, 100, -248, 50, 4, lw=5)                                       # snow on the bed
    rect_r(ctx, 90, -420, 200, 340, 30); fl(ctx, hx('ff8a1f'), 8)                # cab
    rect_r(ctx, 120, -390, 140, 120, 20); fl(ctx, hx('dff4ff'), 6)               # window
    rect_r(ctx, 270, -260, 120, 180, 26); fl(ctx, hx('ff8a1f'), 8)               # hood
    rect_r(ctx, 360, -230, 30, 40, 10); fl(ctx, YEL, 4)                          # headlight
    # roof light (blinks)
    on = (lf // 4) % 2 == 0
    if on:
        ellipse(ctx, 190, -450, 70, 46); setc(ctx, (1, 0.8, 0.2, 0.35)); ctx.fill()
    rect_r(ctx, 160, -456, 60, 36, 14); fl(ctx, hx('ffd23f') if on else hx('d08a1a'), 5)
    # blade
    ctx.new_path(); ctx.move_to(400, -40); ctx.curve_to(520, -60, 540, -260, 470, -330)
    ctx.line_to(440, -320); ctx.curve_to(490, -240, 470, -90, 390, -70); ctx.close_path(); fl(ctx, hx('ffd23f'), 8)
    for k in range(4):
        ctx.move_to(415 + k * 12, -300 + k * 70); ctx.line_to(470 + k * 8, -290 + k * 66)
    setc(ctx, (0, 0, 0, 0.25)); ctx.set_line_width(10); ctx.stroke()
    rect_r(ctx, 360, -170, 60, 26, 8); fl(ctx, hx('6a6e80'), 4)
    # wheels
    for wx in (-240, -60, 230):
        ellipse(ctx, wx, -70, 74, 74); fl(ctx, hx('2a2840'), 8)
        ellipse(ctx, wx, -70, 30, 30); fl(ctx, hx('c8ccd8'), 5)
        ctx.save(); ctx.translate(wx, -70); ctx.rotate(lf * 0.6 * f_)
        for k in range(4):
            ctx.move_to(0, 0); ctx.line_to(28 * math.cos(k * 1.57), 28 * math.sin(k * 1.57))
        ink(ctx, 4); ctx.stroke(); ctx.restore()
    wc = ctx.user_to_device(190, -330)
    ctx.restore()
    wcx, wcy = ctx.device_to_user(*wc)
    # driver in the cab window (unflipped so his face reads normally)
    ctx.save(); rect_r(ctx, wcx - 70 * s, wcy - 60 * s, 140 * s, 120 * s, 20 * s); ctx.clip()
    face(ctx, DRV, P(eye=drv_eye, mouth=drv_mouth), wcx + 6 * s * f_, wcy + 20 * s, 52 * s, 0.0, f_)
    ctx.restore()
    if wave > 0:
        ctx.save(); ctx.translate(wcx + 80 * s * f_, wcy - 10 * s); ctx.rotate(0.4 * math.sin(lf * 0.6))
        ellipse(ctx, 0, 0, 22 * s, 26 * s); fl(ctx, DRV['skin'], 4); ctx.restore()


def snowblower(ctx, x, gy, s=1.0, f_=-1, lf=0, on=True):
    ctx.save(); ctx.translate(x, gy); ctx.scale(s * f_, s)
    rect_r(ctx, -40, -150, 190, 120, 26); fl(ctx, hx('e8232f'), 7)
    rect_r(ctx, 120, -120, 60, 110, 16); fl(ctx, hx('ffd23f'), 6)               # auger housing
    poly(ctx, [(30, -150), (70, -150), (110, -320), (60, -330)]); fl(ctx, hx('e8232f'), 6)  # chute
    for wx in (-10, 100):
        ellipse(ctx, wx, -26, 34, 34); fl(ctx, hx('2a2840'), 6)
    ctx.move_to(-30, -140); ctx.line_to(-160, -300); ink(ctx, 10); ctx.stroke()  # handles
    ctx.move_to(-30, -140); ctx.line_to(-160, -300); setc(ctx, hx('6a6e80')); ctx.set_line_width(5); ctx.stroke()
    tip = ctx.user_to_device(85, -330)
    if on:
        for k in range(3):
            ctx.move_to(-60 - k * 20, -60 + 10 * math.sin(lf + k)); ctx.line_to(-110 - k * 24, -70 + 10 * math.sin(lf + k))
        setc(ctx, (0.3, 0.3, 0.4, 0.5)); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()
    return ctx.device_to_user(*tip)


def arc_spray(ctx, x0, y0, x1, y1, lf, h=700, a=1.0, n=26):
    for k in range(n):
        u = ((lf * 0.05 + k / n) % 1)
        x = lerp(x0, x1, u); y = lerp(y0, y1, u) - h * 4 * u * (1 - u)
        rr = 18 + 26 * u
        ellipse(ctx, x + 20 * math.sin(k * 7), y + 16 * math.cos(k * 5), rr, rr * 0.85, k)
        setc(ctx, (1, 1, 1, a)); ctx.fill_preserve(); setc(ctx, INK + (0.55 * a,)); ctx.set_line_width(4); ctx.stroke()


# ------------------------------------------------------------------ set
def sky(ctx, lf=0):
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, hx('cfe6ff')); ctx.fill()
    ctx.rectangle(-3000, -3000, 9000, 3500); setc(ctx, hx('bcdcff')); ctx.fill()
    for cx_, cy_ in ((260 + 0.3 * lf, 360), (1300 + 0.2 * lf, 300), (2300, 380), (-500, 330)):
        for dx, r in ((-60, 50), (0, 70), (64, 50)):
            ellipse(ctx, cx_ + dx, cy_, r, r * 0.8); fl(ctx, WHITE, 5)


def house(ctx, cx, col, roof, mine=True, lf=0, kid=True):
    rect_r(ctx, cx - 440, 640, 880, HZ - 640 + 10, 8); fl(ctx, col, 8)
    for k in range(6):
        ctx.move_to(cx - 430, 720 + k * 80); ctx.line_to(cx + 430, 720 + k * 80)
    setc(ctx, dark(col, 0.9)); ctx.set_line_width(5); ctx.stroke()
    # chimney + smoke
    rect_r(ctx, cx + 220, 400, 90, 200, 6); fl(ctx, hx('c96a5a'), 7)
    for k in range(3):
        u = ((lf * 0.02 + k / 3) % 1)
        ellipse(ctx, cx + 265 + 40 * math.sin(u * 5), 370 - 260 * u, 30 + 30 * u, 26 + 24 * u); setc(ctx, (1, 1, 1, 0.8 * (1 - u))); ctx.fill()
    poly(ctx, [(cx - 500, 660), (cx, 380), (cx + 500, 660)]); fl(ctx, roof, 9)
    # thick snow on the roof + icicles
    ctx.new_path(); ctx.move_to(cx - 520, 676); ctx.line_to(cx, 360); ctx.line_to(cx + 520, 676)
    for i in range(9):
        x = cx + 520 - 1040 * (i + 1) / 9; xm = x + 1040 / 18
        ctx.curve_to(xm + 20, 720, xm - 20, 720, x, 676)
    ctx.close_path(); fl(ctx, SNOW, 7)
    rnd = random.Random(cx)
    for k in range(9):
        x = cx - 460 + k * 115; L = rnd.uniform(40, 90)
        poly(ctx, [(x - 14, 690), (x + 14, 690), (x + 2, 690 + L)]); fl(ctx, ICE, 3)
    # window (warm light), kid inside with cocoa
    wx = cx - 250
    rect_r(ctx, wx - 120, 780, 240, 200, 12); fl(ctx, hx('ffe9a8'), 8)
    if kid:
        ctx.save(); rect_r(ctx, wx - 120, 780, 240, 200, 12); ctx.clip()
        face(ctx, KID, P(eye='happy', mouth='smile'), wx - 10, 900, 62, 0.05 * math.sin(lf * 0.1))
        rect_r(ctx, wx + 40, 900, 46, 56, 10); fl(ctx, hx('ff8ab8'), 4)
        for k in range(2):
            ctx.move_to(wx + 52 + 16 * k, 890); ctx.curve_to(wx + 40 + 16 * k, 870 - 8 * math.sin(lf * 0.2), wx + 64 + 16 * k, 860, wx + 52 + 16 * k, 840)
        setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(4); ctx.stroke()
        ctx.restore()
    ctx.move_to(wx, 780); ctx.line_to(wx, 980); ctx.move_to(wx - 120, 880); ctx.line_to(wx + 120, 880); ink(ctx, 6); ctx.stroke()
    blob(ctx, wx - 140, wx + 140, 984, 34, 3, lw=4)
    # door + wreath
    dx0 = cx + 150
    rect_r(ctx, dx0, 880, 170, HZ - 880, 10); fl(ctx, hx('ff6b5a') if mine else hx('3ccfb0'), 7)
    ellipse(ctx, dx0 + 140, 1040, 10, 10); fl(ctx, GOLD, 3)
    ctx.new_path(); ctx.arc(dx0 + 85, 960, 46, 0, 6.29); setc(ctx, INK); ctx.set_line_width(28); ctx.stroke_preserve()
    setc(ctx, GREEN); ctx.set_line_width(20); ctx.stroke()
    for k in range(5):
        ellipse(ctx, dx0 + 85 + 46 * math.cos(k * 1.26), 960 + 46 * math.sin(k * 1.26), 8, 8); fl(ctx, RED, 2)
    # number plate
    rect_r(ctx, cx - 30, 700, 70, 60, 8); fl(ctx, WHITE, 5)
    text(ctx, "12" if mine else "14", cx + 5, 732, 40, OUT, ow=0, shadow=False)


def pine(ctx, x, gy, s=1.0, dump=0.0, branch=False):
    ctx.save(); ctx.translate(x, gy); ctx.scale(s, s)
    ctx.rectangle(-26, -120, 52, 130); fl(ctx, hx('8a5a3a'), 6)
    for i, (w, y) in enumerate(((260, -120), (210, -330), (160, -520), (110, -690))):
        poly(ctx, [(-w, y), (w, y), (0, y - 300)]); fl(ctx, hx('2f9a5a'), 7)
        blob(ctx, -w * 0.8, w * 0.8, y - 70, 50, 11 + i, lw=4)
    if branch:                                                        # long branch over the street
        ctx.move_to(60, -560); ctx.curve_to(260, -600, 420, -560, 560, -520); ink(ctx, 28); ctx.stroke()
        ctx.move_to(60, -560); ctx.curve_to(260, -600, 420, -560, 560, -520); setc(ctx, hx('8a5a3a')); ctx.set_line_width(18); ctx.stroke()
        for k in range(4):
            ellipse(ctx, 200 + k * 110, -575 + 10 * k, 90, 36, -0.1); fl(ctx, hx('2f9a5a'), 5)
        if dump < 1:
            blob(ctx, 150, 640, -585 + 40 * dump, 90 * (1 - dump), 17, lw=5)
    ctx.restore()


def yard(ctx, lf, drive=0.0, nb_drive=1.0):
    """drive: snow cover on Dad's driveway (0 clean, 1 covered). nb_drive: neighbour's."""
    ctx.rectangle(-3000, HZ, 9000, 4000); setc(ctx, SNOW); ctx.fill()
    ctx.move_to(-3000, HZ); ctx.line_to(6000, HZ); ink(ctx, 6); ctx.stroke()
    for k in range(-10, 40):
        x = k * 137 % 3600 - 800; y = HZ + 40 + (k * 61) % 380
        ellipse(ctx, x, y, 60, 10); setc(ctx, SNOW_S); ctx.fill()
    # driveways (in front of each house)
    for cx, cov in ((DX + 40, drive), (2060, nb_drive)):
        poly(ctx, [(cx - 300, HZ), (cx + 300, HZ), (cx + 380, ST0), (cx - 380, ST0)]); fl(ctx, hx('aab3c4'), 6)
        for k in range(3):
            ctx.move_to(cx - 310 - 25 * k, HZ + 110 + 120 * k); ctx.line_to(cx + 310 + 25 * k, HZ + 110 + 120 * k)
        setc(ctx, hx('97a0b2')); ctx.set_line_width(5); ctx.stroke()
        if cov > 0:
            poly(ctx, [(cx - 300, HZ), (cx + 300, HZ), (cx + 380, ST0), (cx - 380, ST0)]); setc(ctx, SNOW[:3] + (cov,)); ctx.fill()
    # snow banks along Dad's driveway
    blob(ctx, DX - 760, DX - 330, ST0 - 10, 220, 21)
    blob(ctx, DX + 410, DX + 760, ST0 - 10, 200, 22)
    # fence between the yards
    for k in range(7):
        x = 1330 + k * 58
        poly(ctx, [(x, HZ + 210), (x, HZ + 50), (x + 22, HZ + 26), (x + 44, HZ + 50), (x + 44, HZ + 210)]); fl(ctx, WHITE, 5)
        ellipse(ctx, x + 22, HZ + 26, 26, 12); fl(ctx, SNOW, 3)
    ctx.rectangle(1320, HZ + 90, 420, 22); fl(ctx, WHITE, 4)
    # mailbox with a snow cap
    ctx.rectangle(DX - 330, ST0 - 220, 16, 220); fl(ctx, hx('8a5a3a'), 4)
    rect_r(ctx, DX - 380, ST0 - 280, 120, 70, 30); fl(ctx, hx('3d8bff'), 5)
    ellipse(ctx, DX - 320, ST0 - 284, 66, 18); fl(ctx, SNOW, 4)
    # snowman in the neighbour's yard
    sx, sy = 2470, 1520
    for r, cy in ((90, -90), (66, -230), (48, -330)):
        ellipse(ctx, sx, sy + cy, r, r * 0.95); fl(ctx, WHITE, 6)
    for ex in (-16, 16):
        ellipse(ctx, sx + ex, sy - 342, 7, 7); setc(ctx, INK); ctx.fill()
    poly(ctx, [(sx, sy - 330), (sx, sy - 316), (sx + 50, sy - 326)]); fl(ctx, ORANGE, 3)
    ctx.move_to(sx - 42, sy - 285); ctx.curve_to(sx - 14, sy - 270, sx + 14, sy - 270, sx + 42, sy - 285); setc(ctx, INK); ctx.set_line_width(22); ctx.stroke_preserve()
    setc(ctx, RED); ctx.set_line_width(14); ctx.stroke()


def street(ctx, lf):
    ctx.rectangle(-3000, ST0, 9000, ST1 - ST0); setc(ctx, hx('8a92a8')); ctx.fill()
    ctx.move_to(-3000, ST0); ctx.line_to(6000, ST0); ctx.move_to(-3000, ST1); ctx.line_to(6000, ST1); ink(ctx, 6); ctx.stroke()
    for k in range(-20, 40):
        rect_r(ctx, k * 260, (ST0 + ST1) / 2 - 8, 140, 16, 8); setc(ctx, hx('ffd23f')); ctx.fill()
    ctx.rectangle(-3000, ST1, 9000, 3000); setc(ctx, SNOW); ctx.fill()
    blob(ctx, -900, 3200, ST1 + 40, 70, 31, lw=5)


def world(ctx, lf, drive=0.0, nb_drive=1.0, nb_house=True, kid=True):
    sky(ctx, lf)
    house(ctx, DX - 60, hx('ffe08a'), hx('ff6b5a'), True, lf, kid)
    if nb_house:
        house(ctx, 2160, hx('c8b8ff'), hx('3d8bff'), False, lf, False)
    yard(ctx, lf, drive, nb_drive)
    pine(ctx, 160, ST0 - 40, 0.9)


# ------------------------------------------------------------------ people
def stand(ctx, ch, x, k, p, f_=1, g=GND):
    return draw(ctx, x, g - 186 * k, k, f_, ch, p)


def dad_shovel(ctx, lf, ch=DAD_R, x=DX, amp=1.0, eye='glare', mouth='scream', load=None, g=GND, snowy=False):
    """Dad mid-shovel: a 'push + flick' cycle; returns body + blade"""
    ph = (lf % 16) / 16
    sw = math.sin(ph * 2 * math.pi) * amp
    d = stand(ctx, ch, x, KD, P(eye=eye, mouth=mouth, torso=18 + 8 * sw, head=-10, lsh=110 + 20 * sw, lel=-20, rsh=140 + 20 * sw, rel=-10,
                                lhip=-10, rkn=-20, rhip=20), g=g)
    hat(ctx, d, snowy=snowy)
    ld = (0.5 + 0.5 * math.cos(ph * 2 * math.pi)) if load is None else load
    tip = shovel(ctx, d['back'], d['front'], 200, ld)
    return d, tip, ph


def dad_eyes_over(ctx, x, g, lf, eye='shock', ch=DAD):
    d = stand(ctx, ch, x, KD, P(eye=eye, mouth='flat', lsh=160, lel=-20, rsh=160, rel=-20), g=g)
    hat(ctx, d)
    return d


# ------------------------------------------------------------------ shot 1: hook
def hook(ctx, f, lf):
    ctx.save(); cam(ctx, 860, 1300, 1.1 + 0.03 * eio(pop(lf, 0, 40)), 0, 2 + shake_at(lf, [0], 6, 8), f)
    world(ctx, lf, drive=0.25)
    blob(ctx, DX + 150, DX + 380, GND + 40, 110, 41)                     # the last little bit
    d, tip, ph = dad_shovel(ctx, lf * 1.4)
    chunks(ctx, tip[0], tip[1] - 40, DX + 700, ST0 - 260, ((lf * 1.4) % 16) / 16, 6, int(lf * 1.4 // 16))
    sweat(ctx, d['head'][0] - d['R'] * 1.0, d['head'][1] - d['R'] * 0.3, lf, 1.0)
    ctx.restore()
    snow_fall(ctx, lf)


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"ALMOST...", "...DONE...!!\"", WHITE, t, 120, col2=BLUE, y=1460)


# ------------------------------------------------------------------ shot 2: done -> plow -> speed -> plow again
def done(ctx, f, il):
    # il 0..42: Dad leans on the shovel, clean driveway sparkles "DONE! PERFECT." *DING*
    ctx.save(); cam(ctx, 880, 1300, 1.0, 0, 0, f)
    world(ctx, il, drive=0.0)
    d = stand(ctx, DAD, DX, KD, P(eye='smug', mouth='grin', torso=-4, lsh=30, lel=-40, rsh=150, rel=-30, lhip=-10, rhip=14))
    hat(ctx, d)
    fx, fy = d['front']
    shovel(ctx, (fx - 10, fy - 60), (fx, fy), 300, 0, ORANGE)
    for k, (sx, sy) in enumerate(((DX - 180, GND - 60), (DX + 240, GND - 20), (DX + 60, HZ + 160))):
        sparkle(ctx, sx, sy, 26 + 10 * math.sin(il * 0.4 + k), WHITE)
    ctx.restore()
    snow_fall(ctx, il)
    label2(ctx, "\"DONE!", "PERFECT.\"", WHITE, pop(il, 3, 7), 124, col2=GOLD, y=1460)


def plow_pass(ctx, f, il, dirn=1, wall0=0.0, wall1=1.0, big=1.0):
    # il 0..64 (dirn=1, left->right) or 0..40 (dirn=-1)
    if dirn == 1:
        px = lerp(-900, 2700, clamp((il - 8) / 30))
        rumble = il < 40
    else:
        px = lerp(2700, -900, clamp((il - 2) / 22))
        rumble = il < 26
    wall = lerp(wall0, wall1, clamp((px - 450) / 800) if dirn == 1 else clamp((1300 - px) / 800))
    ctx.save(); cam(ctx, 880, 1320, 1.04, 0, (5 if rumble else 0) + shake_at(il, [20 if dirn == 1 else 12], 10, 10), f)
    world(ctx, il, drive=0.0)
    after = wall > 0.6
    if after:
        d = dad_eyes_over(ctx, DX, GND, il)
        if il > (44 if dirn == 1 else 28):
            twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 1.0, il, 1.1)
    else:
        d = stand(ctx, DAD, DX, KD, P(eye='shock' if il > 4 else 'smug', mouth='open' if il > 4 else 'grin', torso=-4,
                                      lsh=30, lel=-40, rsh=150, rel=-30, head=-12 * dirn))
        hat(ctx, d)
        fx, fy = d['front']
        shovel(ctx, (fx - 10, fy - 60), (fx, fy), 300, 0, ORANGE)
    street(ctx, il)
    blob(ctx, DX - 380, DX + 460, ST0 + 40, 470 * big * wall, 51 + (dirn < 0))
    plow(ctx, px, ST1 + 20, 1.35, dirn, il, spray=1.0 if -400 < px < 2200 else 0.0)
    ctx.restore()
    snow_fall(ctx, il)
    if dirn == 1:
        if il < 18:
            label(ctx, "*VRRRMMM...*", 540, 450, 104, ORANGE, -0.04, pop(il, 1, 4))
        elif il < 40:
            label(ctx, "*FWOOOSH!!*", 540, 450, 128, CYAN, 0.04, pop(il, 18, 21))
        else:
            label(ctx, "\"...WHAT?!\"", 540, 1470, 140, RED, -0.04, pop(il, 42, 45))
    else:
        if il < 24:
            label(ctx, "*FWOOOSH!!*", 540, 450, 128, CYAN, -0.04, pop(il, 8, 11))
        else:
            label(ctx, "\"...AGAIN?!\"", 540, 1470, 140, RED, 0.04, pop(il, 26, 29))


def speed_dig(ctx, f, il):
    # il 0..40: Dutch tilt; ghost-Dad digs through the wall *SCRAPE!* x3 ; 32 "DONE...!"
    wall = 1 - eio(pop(il, 2, 30))
    ctx.save(); cam(ctx, 880, 1340, 1.14, -7, shake_at(il, [4, 14, 24], 5, 6), f)
    world(ctx, il, drive=0.0)
    for g in (2, 1):
        ctx.push_group()
        dad_shovel(ctx, (il - g) * 3.0, x=DX + 60 * math.sin((il - g) * 0.9))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(0.25)
    d, tip, ph = dad_shovel(ctx, il * 3.0, x=DX + 60 * math.sin(il * 0.9))
    street(ctx, il)
    blob(ctx, DX - 380, DX + 460, ST0 + 40, 470 * wall, 51)
    for k in range(3):
        chunks(ctx, DX + 100, ST0 - 120, DX - 900 + 600 * k, HZ - 200, ((il * 0.15 + k * 0.33) % 1), 5, k + il // 7, 26, 420)
    sweat(ctx, d['head'][0] - d['R'] * 1.0, d['head'][1] - d['R'] * 0.3, il, 1.0)
    ctx.restore()
    snow_fall(ctx, il)
    if il < 32:
        for j, (a, y) in enumerate(((4, 330), (14, 430), (24, 1480))):
            label(ctx, "*SCRAPE!*", 540 + (-130, 130, 0)[j], y, 108, PURPLE, (-0.08, 0.07, -0.04)[j], pop(il, a, a + 3))
    else:
        label(ctx, "\"DONE...!\"", 540, 1470, 130, WHITE, -0.03, pop(il, 32, 35))


def s2(ctx, f):
    lf = f - 54
    if lf < 42:
        done(ctx, f, lf)
    elif lf < 106:
        plow_pass(ctx, f, lf - 42, 1)
    elif lf < 146:
        speed_dig(ctx, f, lf - 106)
    else:
        plow_pass(ctx, f, lf - 146, -1, 0.0, 1.0, 1.04)


# ------------------------------------------------------------------ shot 3: STOP sign standoff -> branch dump
SX = 760


def standoff(ctx, f, il):
    # il 0..100: 0-30 plow approaches from the right; 26 *SCREEECH*; 34 "HA! VICTORY!" ; 62 creak ; 70 FWUMP ; 82 "...REALLY?"
    px = lerp(2600, SX + 760, eout(pop(il, 0, 28)))
    dump = eio(pop(il, 66, 74))
    z = 1.12 if il < 60 else lerp(1.12, 1.0, eio(pop(il, 60, 66)))
    cy = 1440 if il < 60 else lerp(1440, 1330, eio(pop(il, 60, 66)))
    ctx.save(); cam(ctx, SX + 240, cy, z, 0, shake_at(il, [26, 70], 10, 12), f)
    world(ctx, il, drive=0.0, kid=True)
    pine(ctx, SX - 380, ST0 - 30, 1.15, dump, branch=True)
    street(ctx, il)
    if il < 74:
        win = il >= 34
        d = stand(ctx, DAD, SX, KD, P(eye='glare' if not win else 'happy', mouth='flat' if not win else 'grin',
                                     lsh=160 if win else 20, lel=-20, rsh=170 if win else 150, rel=-10 if win else -40,
                                     torso=-4, head=4), g=SGND)
        hat(ctx, d)
        fx, fy = d['front']
        stop_sign(ctx, fx + 10, fy - 230 if not win else fy - 300, 0.8, 0.1 * math.sin(il * 0.3) if win else 0.0)
        if win:
            sparkle(ctx, d['head'][0] - 220, d['head'][1] - 120, 30, GOLD); sparkle(ctx, d['head'][0] + 200, d['head'][1] - 160, 24, GOLD)
    else:
        # Dad is now a snow lump with eyes, the stop sign poking out
        stop_sign(ctx, SX + 160, SGND - 760, 0.8, 0.25)
        blob(ctx, SX - 220, SX + 220, SGND + 10, 520, 61)
        for ex in (-40, 40):
            ellipse(ctx, SX + ex, SGND - 380, 22, 26); fl(ctx, WHITE, 4)
            ellipse(ctx, SX + ex + 4, SGND - 376, 11, 13); setc(ctx, INK); ctx.fill()
        ctx.move_to(SX - 70, SGND - 420); ctx.line_to(SX - 20, SGND - 410); ctx.move_to(SX + 70, SGND - 420); ctx.line_to(SX + 20, SGND - 410)
        ink(ctx, 6); ctx.stroke()
    if 66 <= il < 76:                                                # falling snow load
        u = pop(il, 66, 74)
        blob(ctx, SX - 260, SX + 260, lerp(SGND - 900, SGND - 300, u * u), 200, 71)
    plow(ctx, px, ST1 + 60, 1.2, -1, il if il < 28 else 28, drv_eye='shock' if il < 34 else 'happy', drv_mouth='open' if il < 34 else 'grin',
         spray=1.0 if il < 26 else 0.0, wave=1.0 if il > 76 else 0.0)
    ctx.restore()
    snow_fall(ctx, il)
    if il < 26:
        label2(ctx, "\"NOT. THIS.", "TIME.\"", WHITE, pop(il, 2, 6), 120, col2=RED, y=1500)
    elif il < 34:
        label(ctx, "*SCREEECH!*", 540, 450, 120, ORANGE, -0.04, pop(il, 26, 29))
    elif il < 60:
        label2(ctx, "\"HA!", "VICTORY!\"", WHITE, pop(il, 34, 38), 124, col2=GOLD, y=1500)
    elif il < 70:
        label(ctx, "*creeeak...*", 540, 450, 100, hx('c98a4a'), 0.04, pop(il, 60, 63))
    elif il < 82:
        label(ctx, "*FWUMP!*", 540, 450, 136, CYAN, -0.04, pop(il, 70, 73))
    else:
        label(ctx, "\"...REALLY?\"", 540, 1500, 130, WHITE, -0.03, pop(il, 82, 85))


def s3(ctx, f):
    standoff(ctx, f, f - 240)


# ------------------------------------------------------------------ shot 4: the one big close-up
def frozen(ctx, f, il):
    # il 0..80: Dad's blue face poking out of the snow, teeth chattering "...I LOVE... WINTER."
    ctx.save(); cam(ctx, 540, 960, 1.0 + 0.07 * eio(il / 80), 0, 2 + shake_at(il, [0], 6, 8), f)
    ctx.rectangle(-600, -600, 2400, 3200); setc(ctx, hx('9fd0ff')); ctx.fill()
    rays(ctx, 540, 900, 240, 1500, il * 0.02, col=(1, 1, 1), a=0.3, n=16)
    jit = 4 * math.sin(il * 2.6)
    face(ctx, DAD_B, P(eye='glare', mouth='grin'), 540 + jit, 930, 205, 0.0)
    # snow cap on the head + icicle on the nose
    for cx_, cy_, rx, ry in ((540, 735, 230, 70), (430, 715, 90, 60), (600, 700, 110, 70), (700, 745, 70, 40)):
        ellipse(ctx, cx_, cy_, rx, ry); fl(ctx, SNOW, 6)
    poly(ctx, [(560, 1010), (590, 1010), (575, 1080)]); fl(ctx, ICE, 4)
    blob(ctx, -200, 1280, 1500, 420, 82, lw=7)
    blob(ctx, 120, 960, 1320, 200, 83, lw=6)
    twitch(ctx, 760, 760, il, 1.4)
    ctx.restore()
    snow_fall(ctx, il, 24)
    label(ctx, "*chatter chatter*", 540, 450, 92, CYAN, 0.04, pop(il, 0, 3))
    label2(ctx, "\"...I LOVE...", "...WINTER.\"", WHITE, pop(il, 14, 18), 120, col2=BLUE, y=1500)


def s4(ctx, f):
    frozen(ctx, f, f - 340)


# ------------------------------------------------------------------ shot 5: twist
NBX = 2000


def blower(ctx, f, il):
    # il 0..120: wide; Dad shovels (left), the neighbour's snowblower arcs ALL the snow onto him; 66 "Morning, neighbour!"
    pile = eio(pop(il, 24, 104))
    ctx.save(); cam(ctx, 1380, 1290, 0.8, 0, 2 if il > 20 else 0, f)
    world(ctx, il, drive=0.0, nb_drive=1 - eio(pop(il, 14, 90)))
    # Dad (shovelling, then buried by the growing pile)
    d, tip, ph = dad_shovel(ctx, il * 1.2, ch=DAD if il < 50 else DAD_R, eye='glare' if il < 50 else 'shock', mouth='flat' if il < 50 else 'scream')
    blob(ctx, DX - 360, DX + 360, GND + 40, 640 * pile, 91)
    # neighbour + snowblower, waving
    n = stand(ctx, NB, NBX, KD, P(eye='happy', mouth='grin', lsh=150, lel=-30, rsh=40 if il < 60 else 160, rel=-20 if il < 60 else -40 + 30 * math.sin(il * 0.6)), f_=-1)
    hat(ctx, n, GOLD)
    tip2 = snowblower(ctx, NBX - 250, GND + 10, 1.0, -1, il)
    if il > 10:
        arc_spray(ctx, tip2[0], tip2[1], DX + 40, GND - 420 * max(pile, 0.25), il, 640, min(1, pop(il, 10, 16)))
    for k in range(3):
        sparkle(ctx, 1860 + k * 160, 1300 + (k % 2) * 140, 24 * pop(il, 60, 70), WHITE)
    ctx.restore()
    snow_fall(ctx, il)
    card(ctx, 'p2', il, 0)
    if il < 60:
        label(ctx, "*VRRRRRRR!*", 540, 1480, 112, PURPLE, 0.04, pop(il, 8, 11))
    else:
        label2(ctx, "\"Morning,", "neighbour!\"", WHITE, pop(il, 62, 66), 112, col2=PURPLE, y=1500)


def buried(ctx, f, il):
    # il 0..90: Dad buried to the neck "...morning." twitch ; 56 bursts out *POOF!* grabs the shovel "HNNNGH!"
    ctx.save(); cam(ctx, 900, 1310, 1.08, 0, shake_at(il, [56], 10, 10), f)
    world(ctx, il, drive=0.0, nb_drive=0.0)
    if il < 56:
        blob(ctx, DX - 420, DX + 420, GND + 40, 380, 91)
        ctx.save(); ctx.rectangle(-3000, -3000, 9000, GND - 300 + 3000); ctx.clip()
        d = stand(ctx, DAD_R, DX, KD, P(eye='glare', mouth='flat', lsh=20, lel=-10, rsh=20, rel=-10), g=GND)
        ctx.restore()
        hat(ctx, d, snowy=True)
        blob(ctx, DX - 420, DX + 420, GND + 40, 300, 92)
        shovel(ctx, (DX + 330, GND - 330), (DX + 350, GND - 420), 70, 0, ORANGE)
        if il > 22:
            twitch(ctx, d['head'][0] + d['R'] * 0.9, d['head'][1] - d['R'] * 1.1, il, 1.2)
    else:
        u = pop(il, 56, 64)
        for k in range(10):                                           # POOF burst
            a = k * 0.63
            ellipse(ctx, DX + math.cos(a) * 500 * u, GND - 260 + math.sin(a) * 360 * u, 60 * (1 - u) + 20, 50 * (1 - u) + 16); fl(ctx, SNOW, 4)
        blob(ctx, DX - 420, DX + 420, GND + 40, 120, 93)
        d, tip, ph = dad_shovel(ctx, il * 1.4, snowy=True)
        sweat(ctx, d['head'][0] - d['R'] * 1.0, d['head'][1] - d['R'] * 0.3, il, 1.0)
    ctx.restore()
    snow_fall(ctx, il)
    if il < 56:
        label2(ctx, "\"...good", "morning.\"", WHITE, pop(il, 6, 10), 120, col2=RED, y=1480)
    else:
        label(ctx, "*POOF!*", 540, 450, 124, CYAN, 0.04, pop(il, 56, 59))
        label(ctx, "\"HNNNNGH!!\"", 540, 1480, 128, RED, -0.03, pop(il, 64, 67))


def s5(ctx, f):
    lf = f - 420
    if lf < 120:
        blower(ctx, f, lf)
    elif lf < 210:
        buried(ctx, f, lf - 120)
    else:
        s1(ctx, f, f - 630)


SHOTS = [(0, s1), (54, s2), (240, s3), (340, s4), (420, s5)]
CUTS = (54, 96, 160, 200, 240, 340, 420, 540, 630)


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
                              "-i", "out/snowplow_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
