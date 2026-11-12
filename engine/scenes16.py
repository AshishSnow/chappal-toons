"""'Dad Fixes the Wi-Fi' - original, general-audience comedy short, ~35s.
The Wi-Fi dies. Dad says "I got this" and tries every wrong fix... Mom just turns it off and on again."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import cam, pop, sparkle, puff, label, shake_at
from scenes8 import walk, sit
from scenes13 import card as _card13
import scenes13

BOY, MOM, DAD = doodle.BOY, doodle.MOM_G, doodle.DAD
N = 1050
STAND = 1500
KB, KM, KD = 1.25, 1.5, 1.55
RX, RY = 900, 1300            # router centre x / base y (on the TV cabinet)

CAPS = {
    'p1': [[("WHEN THE ", OUT), ("WI-FI", hx('1f8bff')), (" DIES", OUT)], [("AND DAD SAYS...", OUT)]],
    'p2': [[("THE ", OUT), ("TECH EXPERT", hx('e07b12'))], [("HAS ARRIVED", OUT)]],
    'p3': [[("HIS ", OUT), ("PRO", hx('ff3b5c')), (" METHODS", OUT)]],
    'p4': [[("THEN HE FOUND", OUT)], [("THE ", OUT), ("MAGIC SPOT", hx('8a3cff'))]],
    'p5': [[("SO HE WENT", OUT)], [("BEHIND THE ", OUT), ("TV", hx('ff3b5c'))]],
    'p6': [[("THEN MOM DID", OUT)], [("THE ", OUT), ("SECRET MOVE", hx('1f8bff'))]],
    'p7': [[("DAD WANTED", OUT)], [("SOME ", OUT), ("CREDIT", hx('e07b12'))]],
}
scenes13.CAPS = CAPS
card = _card13
_tmp = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4))
CABLE_COLS = (hx('ff3b5c'), hx('2fbf5a'), hx('ffd23f'), hx('2f6bff'), hx('ff8a3d'), hx('8a3cff'), (1, 1, 1), hx('1c1a2e'))


# ------------------------------------------------------------------ props
def rect_r(ctx, x, y, w, h, r):
    ctx.new_path(); ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); ctx.close_path()


def wifi(ctx, x, y, s, bars, col=hx('2fbf5a'), dead=False):
    """generic signal icon: dot + 3 arcs; bars = 0..3"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for i in range(3):
        r = 30 + i * 26
        on = i < bars
        ctx.new_path(); ctx.arc(0, 0, r, -math.pi * 0.75, -math.pi * 0.25)
        setc(ctx, INK); ctx.set_line_width(19); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke_preserve()
        setc(ctx, col if on else hx('c9c9d6')); ctx.set_line_width(11); ctx.stroke()
    ellipse(ctx, 0, -2, 11, 11); fl(ctx, col if bars > 0 else hx('c9c9d6'), 4)
    if dead:
        for a, b in (((-50, -100), (50, 0)), ((50, -100), (-50, 0))):
            ctx.move_to(*a); ctx.line_to(*b); setc(ctx, INK); ctx.set_line_width(20); ctx.stroke()
            ctx.move_to(*a); ctx.line_to(*b); setc(ctx, hx('ff3b5c')); ctx.set_line_width(11); ctx.stroke()
    ctx.set_line_cap(cairo.LINE_CAP_BUTT)
    ctx.restore()


def router(ctx, x, yb, f, state='red', s=1.0, a=0.0, bars=None):
    """box with two antennas and 4 LEDs. state: red (blinking) | green | off"""
    ctx.save(); ctx.translate(x, yb); ctx.rotate(a); ctx.scale(s, s)
    for ax, ang in ((-50, -0.25), (50, 0.25)):
        ctx.save(); ctx.translate(ax, -50); ctx.rotate(ang)
        rect_r(ctx, -9, -110, 18, 112, 8); fl(ctx, hx('3a3f55'), 5)
        ctx.restore()
    rect_r(ctx, -90, -56, 180, 56, 14); fl(ctx, hx('f4f4fa'), 6)
    ctx.rectangle(-90, -14, 180, 14); setc(ctx, hx('c9cbe0')); ctx.fill()
    rect_r(ctx, -90, -56, 180, 56, 14); ink(ctx, 6); ctx.stroke()
    for i in range(4):
        lx = -54 + i * 36
        if state == 'green':
            c = hx('3dff6a')
        elif state == 'red':
            c = hx('ff2a3d') if ((f // 6) + i) % 2 == 0 else hx('5a1a22')
        else:
            c = hx('55576a')
        ellipse(ctx, lx, -34, 9, 9); fl(ctx, c, 3)
        if state == 'green':
            ellipse(ctx, lx, -34, 18, 18); setc(ctx, (0.3, 1, 0.45, 0.25)); ctx.fill()
    ctx.restore()
    if bars is not None:
        wifi(ctx, x, yb - 210 * s, 0.9 * s, bars, dead=(bars == 0))


def tablet(ctx, x, y, s, f, mode='spin', prog=0.0, a=0.0):
    """mode: spin (buffering) | bar (progress) | play (video playing)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -110, -76, 220, 152, 18); fl(ctx, hx('2a2f45'), 6)
    ctx.rectangle(-94, -62, 188, 124)
    if mode == 'play':
        ctx.set_source(vgrad(ctx, 0, -62, 0, 62, [(0, hx('5fc8ff')), (1, hx('b8ffb0'))])); ctx.fill()
        # bouncing cartoon blob on screen
        by = -10 - abs(math.sin(f * 0.25)) * 30
        ellipse(ctx, 0, by, 26, 26); fl(ctx, hx('ffd23f'), 4)
        ellipse(ctx, -8, by - 4, 4, 5); setc(ctx, INK); ctx.fill(); ellipse(ctx, 8, by - 4, 4, 5); ctx.fill()
        ctx.rectangle(-94, 34, 188, 28); setc(ctx, hx('2fbf5a')); ctx.fill()
    else:
        setc(ctx, hx('11131c')); ctx.fill()
        if mode == 'spin':
            for i in range(8):
                aa = i * math.pi / 4 + f * 0.25
                ellipse(ctx, math.cos(aa) * 34, math.sin(aa) * 34, 8, 8); setc(ctx, (1, 1, 1, (i + 1) / 8)); ctx.fill()
        else:
            ctx.rectangle(-70, -8, 140, 18); setc(ctx, hx('3a3f55')); ctx.fill()
            ctx.rectangle(-70, -8, 140 * prog, 18); setc(ctx, hx('3dff6a')); ctx.fill()
            ctx.rectangle(-70, -8, 140, 18); setc(ctx, (1, 1, 1)); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()


def headlamp(ctx, h, fac, on=1.0, beam=True):
    hx_, hy = h['head']; R = h['R']
    lx, ly = hx_ + fac * R * 0.55, hy - R * 0.62
    if beam and on > 0:
        ctx.new_path(); ctx.move_to(lx, ly)
        ctx.line_to(lx + fac * 900, ly - 260); ctx.line_to(lx + fac * 900, ly + 420); ctx.close_path()
        g = cairo.LinearGradient(lx, ly, lx + fac * 900, ly)
        g.add_color_stop_rgba(0, 1, 0.97, 0.6, 0.55 * on); g.add_color_stop_rgba(1, 1, 0.97, 0.6, 0)
        ctx.set_source(g); ctx.fill()
    ctx.new_path(); ctx.arc(hx_, hy - R * 0.2, R * 0.98, math.pi * 1.05, math.pi * 1.95)
    setc(ctx, INK); ctx.set_line_width(R * 0.24); ctx.stroke()
    ctx.new_path(); ctx.arc(hx_, hy - R * 0.2, R * 0.98, math.pi * 1.05, math.pi * 1.95)
    setc(ctx, hx('ff3b5c')); ctx.set_line_width(R * 0.14); ctx.stroke()
    ellipse(ctx, lx, ly, R * 0.24, R * 0.24); fl(ctx, hx('fff27a') if on > 0 else hx('9a9aa8'), 5)


def frizz(ctx, h, amt):
    if amt <= 0:
        return
    hx_, hy = h['head']; R = h['R']
    for i in range(11):
        a = math.pi * (1.05 + i * 0.09)
        r0, r1 = R * 0.95, R * (0.95 + 0.6 * amt * (0.8 + 0.4 * ((i * 7) % 3) / 2))
        ctx.move_to(hx_ + math.cos(a) * r0, hy - R * 0.1 + math.sin(a) * r0)
        ctx.line_to(hx_ + math.cos(a + 0.05) * r1, hy - R * 0.1 + math.sin(a + 0.05) * r1)
    setc(ctx, INK); ctx.set_line_width(R * 0.14); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke(); ctx.set_line_cap(cairo.LINE_CAP_BUTT)


def tangle(ctx, cx, cy, rw, rh, amt, seed=3):
    """loops of cables wrapped around a body"""
    rnd = random.Random(seed)
    n = int(9 * amt)
    for j in range(n):
        y = cy - rh + (j + 0.5) * 2 * rh / 9 + rnd.uniform(-20, 20)
        c = CABLE_COLS[j % len(CABLE_COLS)]
        ctx.new_path(); ctx.move_to(cx - rw - 40, y + rnd.uniform(-40, 40))
        ctx.curve_to(cx - rw * 0.3, y - 60, cx + rw * 0.3, y + 70, cx + rw + 40, y + rnd.uniform(-40, 40))
        setc(ctx, INK); ctx.set_line_width(22); ctx.stroke_preserve(); setc(ctx, c); ctx.set_line_width(13); ctx.stroke()


def plug(ctx, x, y, a, col, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.rectangle(-8, -66, 6, 22); ctx.rectangle(4, -66, 6, 22); setc(ctx, hx('d8d8e0')); ctx.fill_preserve(); ink(ctx, 3); ctx.stroke()
    rect_r(ctx, -24, -46, 48, 56, 10); fl(ctx, col, 5)
    ctx.restore()


# ------------------------------------------------------------------ set
def living(ctx, f, wall=hx('9be3c9'), tv='static'):
    ctx.rectangle(-1200, -1500, 3600, 3200); setc(ctx, wall); ctx.fill()
    for i in range(-12, 30):
        ctx.rectangle(i * 90, -1500, 30, 3000); setc(ctx, light(wall, 0.25)); ctx.fill()
    ctx.rectangle(-1200, -1500, 3600, 1300); setc(ctx, light(wall, 0.5)); ctx.fill()
    ctx.move_to(-1200, -200); ctx.line_to(2400, -200); ink(ctx, 8); ctx.stroke()
    # window
    ctx.rectangle(110, 560, 300, 330); fl(ctx, hx('8fe0ff'), 8)
    ellipse(ctx, 330, 640, 34, 34); setc(ctx, hx('fff27a')); ctx.fill()
    ellipse(ctx, 210, 780, 70, 28); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.move_to(260, 560); ctx.line_to(260, 890); ctx.move_to(110, 725); ctx.line_to(410, 725); ink(ctx, 6); ctx.stroke()
    # picture frame (abstract hills)
    ctx.rectangle(560, 560, 260, 190); fl(ctx, hx('fff6e0'), 7)
    poly(ctx, [(575, 735), (650, 640), (720, 700), (770, 650), (805, 735)]); fl(ctx, hx('2fbf5a'), 4)
    ellipse(ctx, 760, 600, 18, 18); setc(ctx, hx('ff8a3d')); ctx.fill()
    # floor
    ctx.rectangle(-1200, STAND - 60, 3600, 1400); setc(ctx, hx('b77a4b')); ctx.fill()
    for i in range(-10, 30):
        ctx.move_to(i * 140, STAND - 60); ctx.line_to(i * 140 - 60, STAND + 1300); setc(ctx, dark(hx('b77a4b'), 0.85)); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-1200, STAND - 60); ctx.line_to(2400, STAND - 60); ink(ctx, 8); ctx.stroke()
    ellipse(ctx, 480, 1600, 440, 80); setc(ctx, hx('ffd23f')); ctx.fill_preserve(); ink(ctx, 6); ctx.stroke()
    # TV cabinet + TV
    ctx.rectangle(560, 1300, 460, 150); fl(ctx, hx('c98b55'), 7)
    for xx in (580, 800):
        ctx.rectangle(xx, 1320, 200, 110); fl(ctx, light(hx('c98b55'), 0.2), 4)
        ellipse(ctx, xx + 100, 1375, 9, 9); fl(ctx, hx('ffd23f'), 3)
    ctx.rectangle(650, 1260, 30, 40); fl(ctx, hx('3a3f55'), 5)
    rect_r(ctx, 540, 1000, 250, 262, 12); fl(ctx, hx('2a2f45'), 7)
    ctx.rectangle(556, 1016, 218, 230)
    if tv == 'static':
        setc(ctx, hx('11131c')); ctx.fill()
        rnd = random.Random(f // 2)
        for _ in range(40):
            ctx.rectangle(556 + rnd.uniform(0, 210), 1016 + rnd.uniform(0, 225), rnd.uniform(6, 30), 4)
        setc(ctx, (1, 1, 1, 0.5)); ctx.fill()
    elif tv == 'on':
        ctx.set_source(vgrad(ctx, 0, 1016, 0, 1246, [(0, hx('5fc8ff')), (1, hx('ffe68a'))])); ctx.fill()
        sparkle(ctx, 665, 1120, 40 + 8 * math.sin(f * 0.3), hx('ff8a3d'))
    else:
        setc(ctx, hx('11131c')); ctx.fill()
    # plant
    ctx.rectangle(-20, 1370, 70, 80); fl(ctx, hx('ff8a3d'), 5)
    for a in (-0.6, -0.2, 0.25, 0.6):
        ellipse(ctx, 15 + math.sin(a) * 60, 1300 - math.cos(a) * 40, 22, 52, a); fl(ctx, hx('2fbf5a'), 4)


def sofa(ctx, x=40, w=470):
    rect_r(ctx, x, 1100, w, 220, 30); fl(ctx, hx('ff6b8a'), 7)
    rect_r(ctx, x + 20, 1270, w - 40, 110, 20); fl(ctx, light(hx('ff6b8a'), 0.25), 6)
    for ax in (x - 30, x + w - 40):
        rect_r(ctx, ax, 1220, 70, 170, 26); fl(ctx, hx('e04f74'), 7)
    for lx in (x + 20, x + w - 50):
        ctx.rectangle(lx, 1390, 30, 50); fl(ctx, hx('7a4a2c'), 5)


def chair(ctx, x, seat_y, wob=0.0):
    ctx.save(); ctx.translate(x, STAND - 60); ctx.rotate(wob); ctx.translate(-x, -(STAND - 60))
    for lx in (x - 90, x + 70):
        ctx.rectangle(lx, seat_y, 20, STAND - 60 - seat_y); fl(ctx, hx('7a4a2c'), 5)
    ctx.rectangle(x - 110, seat_y - 24, 220, 30); fl(ctx, hx('c98b55'), 6)
    ctx.rectangle(x + 70, seat_y - 230, 24, 210); fl(ctx, hx('c98b55'), 6)
    ctx.restore()


def dark_eyes(ctx, x, y, s, f, kind='normal', fac=1, seed=0):
    bl = (f + seed * 17) % 70 < 4
    for dx in (-26, 26):
        ex, ey = x + dx * s, y
        if bl:
            ctx.move_to(ex - 18 * s, ey); ctx.line_to(ex + 18 * s, ey); setc(ctx, (1, 1, 1)); ctx.set_line_width(5 * s); ctx.stroke()
            continue
        if kind == 'glare':
            poly(ctx, [(ex - 20 * s, ey - 6 * s - (dx * 0.25 * s)), (ex + 20 * s, ey - 6 * s + (dx * 0.25 * s)), (ex + 18 * s, ey + 12 * s), (ex - 18 * s, ey + 12 * s)])
            setc(ctx, (1, 1, 1)); ctx.fill()
            ellipse(ctx, ex + fac * 4 * s, ey + 4 * s, 7 * s, 7 * s); setc(ctx, INK); ctx.fill()
        else:
            ellipse(ctx, ex, ey, 20 * s, 24 * s); setc(ctx, (1, 1, 1)); ctx.fill()
            ellipse(ctx, ex + fac * 5 * s, ey + 2 * s, 9 * s, 10 * s); setc(ctx, INK); ctx.fill()


# ------------------------------------------------------------------ shots
BOYX, BOYHIP = 290, 1290


def boy_sofa(ctx, f, mode='spin', prog=0.0, eye='normal', mouth='smile', arms_up=False, tab=True):
    if arms_up:
        bp = sit(eye=eye, mouth=mouth, lsh=-160, lel=-30, rsh=160, rel=30)
    else:
        bp = sit(eye=eye, mouth=mouth, lsh=60, lel=-80, rsh=70, rel=-90)
    h = draw_hip(ctx, BOYX, BOYHIP, KB, 1, BOY, bp)
    if tab:
        fx, fy = h['front']
        if arms_up:
            tablet(ctx, fx + 10, fy - 60, 0.75, f, mode, prog, -0.3)
        else:
            tablet(ctx, fx + 40, fy - 30, 0.75, f, mode, prog, -0.15)
    return h


def s1(ctx, f):
    # ECU on the buffering tablet, pull back as Dad bursts in
    pull = eout(pop(f, 44, 58))
    z = lerp(2.0, 1.0, pull)
    cx = lerp(BOYX + 90, 560, pull); cy = lerp(BOYHIP - 230, 1150, pull)
    ctx.save(); cam(ctx, cx, cy, z, 0, shake_at(f, [52], 12, 22), f)
    living(ctx, f)
    sofa(ctx)
    groan = f < 48
    boy_sofa(ctx, f, 'spin', eye='glare' if groan else 'shock', mouth='frown' if groan else 'open')
    router(ctx, RX, RY, f, 'red')
    if f >= 44:
        dx = lerp(1300, 800, eout(pop(f, 44, 54)))
        dp = P(eye='smug', mouth='grin', torso=-6, lsh=10, lel=-10, rsh=150, rel=-20)    # finger up "I got this"
        draw(ctx, dx, STAND - 186 * KD, KD, -1, DAD, dp)
    ctx.restore()
    if f < 44:
        wifi(ctx, 860, 1020, 1.0, 0, dead=True)
        label(ctx, "BUFFERING...", 540, 1440, 96, (1, 1, 1), -0.03, pop(f, 6, 10))
    else:
        label(ctx, "I GOT THIS!", 540, 1440, 130, hx('ffe14d'), 0.04, pop(f, 52, 56))
    card(ctx, 'p1', f, 2, 98)


def s2(ctx, f):
    lf = f - 100
    # low-angle hero shot: knuckle crack, headlamp on, slow push-in
    crack = 14 <= lf < 48
    lamp = lf >= 56
    if crack:
        k2 = (lf // 4) % 2
        dp = P(eye='closed' if k2 else 'smug', mouth='grin', torso=-4, lsh=80, lel=-60 - 20 * k2, rsh=85, rel=-70 + 20 * k2)
    elif lf < 56:
        dp = P(eye='smug', mouth='grin', torso=-4, lsh=10, lel=-10, rsh=160, rel=-110, head=-6)    # hand to forehead
    else:
        dp = P(eye='glare', mouth='grin', torso=-8, lsh=-40, lel=-80, rsh=-40, rel=-80, head=6)   # hands on hips
    z = kf(lf, [(0, 1.45), (120, 1.75)], eout)
    ctx.save(); cam(ctx, 560, kf(lf, [(0, 1170), (120, 1120)], eout), z, -6, shake_at(lf, [56], 8, 12), f)
    living(ctx, f)
    router(ctx, RX, RY, f, 'red')
    h = draw(ctx, 520, STAND - 186 * KD, KD, 1, DAD, dp)
    headlamp(ctx, h, 1, on=1.0 if lamp else 0.0)
    if lamp:
        for i in range(5):
            a = lf * 0.06 + i * 1.256
            sparkle(ctx, 520 + math.cos(a) * 250, 1150 + math.sin(a) * 300, 26 * pop(lf, 56, 64), hx('fff27a'))
    if crack:
        for i in range(3):
            sparkle(ctx, h['front'][0] + 20 + i * 30, h['front'][1] - 40 - i * 20, 22 * ((lf + i * 3) % 8 < 4), (1, 1, 1))
    ctx.restore()
    if lf < 14:
        pass
    elif lf < 56:
        label(ctx, "*CRACK* *CRACK*", 540, 1440, 86, (1, 1, 1), 0.03, pop(lf, 14, 18))
    elif lf < 84:
        label(ctx, "*CLICK*", 540, 1440, 110, hx('fff27a'), -0.04, pop(lf, 56, 60))
    else:
        label(ctx, "STAND BACK, KID.", 540, 1440, 90, hx('ffe14d'), 0.02, pop(lf, 84, 88))
    card(ctx, 'p2', f, 102, 216)


def s3(ctx, f):
    lf = f - 220
    step = 0 if lf < 60 else (1 if lf < 118 else 2)
    sl = lf - (0, 60, 118)[step]
    ra, rlift, rshake = 0.0, 0.0, 0
    dx = 620
    if step == 0:          # blow on it
        dp = P(eye='closed', mouth='open', torso=24, head=10, lsh=40, lel=-30, rsh=60, rel=-40)
    elif step == 1:        # smack it
        hit = 26
        if sl < hit:
            arm = lerp(60, 175, eout(pop(sl, 0, 16)))
        else:
            arm = 70
        dp = P(eye='glare', mouth='grin' if sl < hit else 'scream', torso=10, lsh=20, lel=-20, rsh=arm, rel=-10)
        if sl >= hit:
            rlift = 30 * abs(math.sin((sl - hit) * 0.5)) * (1 - pop(sl, hit, hit + 20))
    else:                  # wave it around
        sw = math.sin(sl * 0.45)
        dp = P(eye='shock', mouth='open', torso=-4 + 6 * sw, lsh=165 + 10 * sw, lel=-10, rsh=165 - 10 * sw, rel=-10)
    z = kf(lf, [(0, 1.15), (58, 1.25), (60, 1.1), (116, 1.2), (118, 1.0), (180, 1.08)], eout)
    cy = 1150 if step < 2 else 1060
    ctx.save(); cam(ctx, 760 if step < 2 else 720, cy, z, (0, 4, -4)[step], shake_at(lf, [60 + 26], 12, 26), f)
    living(ctx, f)
    h = draw(_tmp, dx, STAND - 186 * KD, KD, 1, DAD, dp)
    if step < 2:
        router(ctx, RX, RY - rlift, f, 'red', a=0.1 * math.sin(sl) * (rlift > 1), bars=0)
    h = draw(ctx, dx, STAND - 186 * KD, KD, 1, DAD, dp)
    headlamp(ctx, h, 1, beam=False)
    if step == 0:
        mx, my = h['head'][0] + h['R'] * 1.1, h['head'][1] + h['R'] * 0.35
        for i in range(3):
            t = ((sl * 0.04) + i / 3) % 1
            ellipse(ctx, lerp(mx, RX - 20, t), lerp(my, RY - 50, t), 16 + 20 * t, 12 + 14 * t); setc(ctx, (1, 1, 1, 0.8 * (1 - t))); ctx.fill()
    if step == 2:
        fx, fy = h['front']
        router(ctx, fx, fy - 10, f, 'red', s=0.9, a=0.3 * math.sin(sl * 0.45), bars=0)
        for i in range(4):
            ctx.move_to(fx - 160 - i * 30, fy - 60 + i * 30); ctx.line_to(fx - 110 - i * 30, fy - 40 + i * 30); ink(ctx, 6); ctx.stroke()
    if step == 1 and 26 <= sl < 36:
        burst(ctx, RX, RY - 70, 130 * (1 - pop(sl, 26, 36)) + 20, seed=sl)
    ctx.restore()
    texts = ["STEP 1: BLOW ON IT", "STEP 2: SMACK IT", "STEP 3: WAVE IT AROUND"]
    label(ctx, texts[step], 540, 1360, 74, hx('ffe14d'), -0.02, pop(sl, 2, 6))
    sub = ["*FOOOOO*", "*BONK!*", "COME ON...!"][step]
    if step != 1 or sl >= 26:
        label(ctx, sub, 540, 1460, 84, (1, 1, 1), 0.03, pop(sl, 10 if step != 1 else 26, 14 if step != 1 else 30))
    card(ctx, 'p3', f, 224, 396)


def panel(ctx, x0, x1, cx, cy, z, rot=0, shake=0, f=0):
    ctx.save(); ctx.rectangle(x0, 0, x1 - x0, H); ctx.clip()
    rnd = random.Random(f * 13 + x0)
    sx, sy = (rnd.uniform(-1, 1) * shake, rnd.uniform(-1, 1) * shake) if shake else (0, 0)
    ctx.translate((x0 + x1) / 2 + sx, H / 2 + sy); ctx.rotate(math.radians(rot)); ctx.scale(z, z); ctx.translate(-cx, -cy)


def s4(ctx, f):
    lf = f - 400
    sneeze = 96
    climb = eout(pop(lf, 0, 14))
    bars = 0 if lf < 30 else (1 if lf < sneeze else 0)
    prog = clamp((lf - 34) / 70) * 0.85 if lf < sneeze else max(0.0, 0.85 - pop(lf, sneeze, sneeze + 10) * 0.85)
    wob = 0.03 * math.sin(lf * 0.4) if lf < sneeze else 0.10 * math.sin(lf * 0.9) * (1 - pop(lf, sneeze, sneeze + 40))
    seat = 1240
    # ---- top panel: Dad on the chair, router held up high
    panel(ctx, 0, 532, 560, 950, 0.8, 0, shake_at(lf, [sneeze], 12, 22), f)
    living(ctx, f)
    chair(ctx, 560, seat, wob)
    if lf < 30:
        dp = P(eye='glare', mouth='flat', torso=0, lsh=170, lel=-10, rsh=170, rel=-10, lhip=0, lkn=0, rhip=0, rkn=0)
    elif lf < sneeze - 12:
        dp = P(eye='closed', mouth='wavy', torso=-6, lsh=175, lel=-5, rsh=165, rel=-10, lhip=70, lkn=-100, rhip=-4, rkn=0, head=-10)
    elif lf < sneeze:
        dp = P(eye='closed', mouth='open', torso=-14, head=-22, lsh=175, lel=-5, rsh=165, rel=-10, lhip=70, lkn=-100, rhip=-4, rkn=0)
    else:
        dp = P(eye='shock', mouth='scream', torso=18, head=20, lsh=175, lel=-5, rsh=140, rel=-10, lhip=70, lkn=-100, rhip=-4, rkn=0)
    ctx.save(); ctx.translate(560, STAND - 60); ctx.rotate(wob); ctx.translate(-560, -(STAND - 60))
    dy = lerp(STAND - 186 * KD, seat - 24 - 186 * KD, climb)
    h = draw(ctx, 560, dy, KD, 1, DAD, dp)
    headlamp(ctx, h, 1, beam=False)
    fx, fy = h['front']
    router(ctx, fx, fy - 10, f, 'red' if bars == 0 else 'green', s=0.8, bars=bars)
    if 40 <= lf < sneeze - 12:
        doodle_sweat(ctx, h['head'][0] - 90, h['head'][1] - 40, lf)
    ctx.restore()
    ctx.restore()
    # ---- bottom panel: Boy watching the progress bar
    panel(ctx, 548, W, BOYX + 70, BOYHIP - 110, 1.45, 0, shake_at(lf, [sneeze + 4], 10, 18), f)
    living(ctx, f)
    sofa(ctx)
    happy = 40 <= lf < sneeze
    boy_sofa(ctx, f, 'bar', prog, eye='happy' if happy else ('normal' if lf < sneeze else 'shock'),
             mouth='grin' if happy else ('flat' if lf < sneeze else 'scream'))
    ctx.restore()
    # divider
    ctx.rectangle(532, 0, 16, H); setc(ctx, OUT); ctx.fill()
    if 34 <= lf < 70:
        label(ctx, "ONE BAR!!", 540, 1440, 100, hx('5fd07a'), -0.03, pop(lf, 34, 38))
    elif 70 <= lf < sneeze:
        label(ctx, "DON'T. MOVE.", 540, 1440, 100, hx('ffe14d'), 0.03, pop(lf, 70, 74))
    elif lf >= sneeze:
        label(ctx, "ACHOO!!", 540, 1440, 130, hx('ff3b5c'), -0.05, pop(lf, sneeze, sneeze + 4))
    card(ctx, 'p4', f, 404, 536)


def doodle_sweat(ctx, x, y, t, s=1.0):
    for i in range(2):
        tt = (t * 0.05 + i * 0.5) % 1
        ctx.save(); ctx.translate(x + i * 40 * s, y + tt * 80 * s); ctx.scale(s, s)
        ctx.new_path(); ctx.move_to(0, -26); ctx.curve_to(16, 0, 16, 18, 0, 18); ctx.curve_to(-16, 18, -16, 0, 0, -26); ctx.close_path()
        fl(ctx, hx('8fe9ff'), 4); ctx.restore()


def behind_tv(ctx, f, lf, wrap, zap):
    ctx.rectangle(-1200, -1500, 3600, 4000); setc(ctx, hx('3b3f5c')); ctx.fill()
    for i in range(-12, 30):
        ctx.rectangle(i * 90, -1500, 30, 4000); setc(ctx, hx('42476a')); ctx.fill()
    # back of the TV
    rect_r(ctx, 120, 420, 840, 420, 20); fl(ctx, hx('2a2f45'), 8)
    for i in range(8):
        ctx.rectangle(220 + i * 80, 470, 40, 120); setc(ctx, hx('1c2030')); ctx.fill()
    # floor + power strip
    ctx.rectangle(-1200, 1500, 3600, 1400); setc(ctx, hx('6b4a33')); ctx.fill()
    ctx.move_to(-1200, 1500); ctx.line_to(2400, 1500); ink(ctx, 8); ctx.stroke()
    rect_r(ctx, 260, 1420, 560, 70, 18); fl(ctx, (1, 1, 1), 6)
    # spaghetti cables
    rnd = random.Random(42)
    for j in range(14):
        x0 = 180 + j * 52; x1 = 290 + (j % 8) * 66
        c = CABLE_COLS[j % len(CABLE_COLS)]
        w1 = math.sin(lf * 0.1 + j) * 20
        ctx.new_path(); ctx.move_to(x0, 820)
        ctx.curve_to(x0 + rnd.uniform(-400, 400) + w1, rnd.uniform(900, 1300), x1 + rnd.uniform(-400, 400), rnd.uniform(1000, 1400), x1, 1390)
        setc(ctx, INK); ctx.set_line_width(24); ctx.stroke_preserve(); setc(ctx, c); ctx.set_line_width(14); ctx.stroke()
    for j in range(8):
        plug(ctx, 290 + j * 66, 1440, 0, CABLE_COLS[j])


def s5(ctx, f):
    lf = f - 540
    zap = 118
    wrap = clamp((lf - 20) / 90)
    tug = math.sin(lf * 0.5)
    if lf < zap:
        dp = P(eye='shock' if (lf // 20) % 2 else 'glare', mouth='wavy', torso=0, lsh=110 + 20 * tug, lel=-40, rsh=120 - 20 * tug, rel=-40)
    else:
        dp = P(eye='shock', mouth='scream', torso=0, lsh=160, lel=-30, rsh=160, rel=-30)
    z = kf(lf, [(0, 0.95), (zap, 1.15), (zap + 1, 1.3), (180, 1.4)], eout)
    ctx.save(); cam(ctx, 540, kf(lf, [(0, 1080), (zap, 1050)], eout), z, kf(lf, [(0, -3), (zap, 4)]), shake_at(lf, [zap], 16, 34), f)
    behind_tv(ctx, f, lf, wrap, lf >= zap)
    h = draw(ctx, 540, 1500 - 186 * KD, KD, 1, DAD, dp)
    frizz(ctx, h, pop(lf, zap, zap + 6))
    headlamp(ctx, h, 1, on=1.0, beam=False)
    tangle(ctx, 540, 1250, 150, 230, wrap)
    if lf < zap:
        bx, by = h['back']; fx, fy = h['front']
        plug(ctx, bx, by, -0.4, hx('ff3b5c'), 1.1); plug(ctx, fx, fy, 0.4, hx('2fbf5a'), 1.1)
    if zap <= lf < zap + 14:
        burst(ctx, 540, 1100, 260 * (1 - pop(lf, zap, zap + 14)) + 60, seed=lf, col=hx('fff27a'), col2=hx('5fc8ff'))
    if lf >= zap + 14:
        puff(ctx, h['head'][0], h['head'][1] - 120, pop(lf, zap + 14, zap + 50), 1.4)
    ctx.restore()
    if lf < 20:
        pass
    elif lf < 60:
        label(ctx, "WHICH ONE IS IT?!", 540, 1440, 84, hx('ffe14d'), 0.03, pop(lf, 20, 24))
    elif lf < zap:
        label(ctx, "MAYBE... THIS ONE?", 540, 1440, 84, (1, 1, 1), -0.03, pop(lf, 64, 68))
    else:
        label(ctx, "*ZAP!*", 540, 1440, 140, hx('5fc8ff'), -0.05, pop(lf, zap, zap + 4))
    card(ctx, 'p5', f, 544, 716)


def s6(ctx, f):
    lf = f - 720
    walk_in = eout(pop(lf, 0, 34))
    unplug, replug = 46, 86
    fixed = lf >= replug + 6
    mx = lerp(-150, 760, walk_in)
    if lf < 34:
        mp = walk(lf * 0.5, eye='normal', mouth='flat')
    elif lf < unplug:
        mp = P(eye='normal', mouth='flat', torso=8, lsh=10, lel=-10, rsh=80, rel=-10)
    elif lf < replug:
        mp = P(eye='closed', mouth='flat', torso=4, lsh=10, lel=-10, rsh=40, rel=-60)     # waits, holding the plug
    else:
        mp = P(eye='smug' if fixed else 'normal', mouth='smile', torso=0, lsh=-40, lel=-80, rsh=-40, rel=-80)
    z = kf(lf, [(0, 1.0), (40, 1.05), (replug, 1.25), (replug + 10, 1.0), (160, 1.05)], eout)
    cx = kf(lf, [(0, 560), (40, 700), (replug, 760), (replug + 10, 560)], eout)
    ctx.save(); cam(ctx, cx, kf(lf, [(0, 1150), (replug, 1200), (replug + 10, 1120)], eout), z, 0, shake_at(lf, [replug + 6], 10, 18), f)
    living(ctx, f, tv='on' if fixed else 'static')
    sofa(ctx)
    boy_sofa(ctx, f, 'play' if fixed else 'spin', eye='happy' if fixed else 'normal', mouth='grin' if fixed else 'flat', arms_up=fixed)
    rs = 'off' if unplug <= lf < replug else ('green' if fixed else 'red')
    router(ctx, RX, RY, f, rs, bars=(3 if fixed else None))
    # router power cable to the wall socket
    ctx.rectangle(1000, 1330, 50, 70); fl(ctx, (1, 1, 1), 5)
    pl_out = unplug <= lf < replug
    ctx.new_path(); ctx.move_to(RX + 80, RY - 20); ctx.curve_to(RX + 140, RY, 980, 1370, 1010 if not pl_out else 960, 1370 if not pl_out else 1290)
    setc(ctx, INK); ctx.set_line_width(14); ctx.stroke()
    # Dad's legs sticking out from behind the cabinet, tangled
    for lx in (585, 640):
        ctx.rectangle(lx, 1440, 40, 70); fl(ctx, DAD['pants'], 5)
        ellipse(ctx, lx + 20, 1515, 34, 18); fl(ctx, DAD['shoes'], 5)
    tangle(ctx, 610, 1470, 60, 40, 0.5, seed=8)
    stand_m = draw(ctx, mx, STAND - 186 * KM, KM, 1, MOM, mp)
    if fixed:
        wifi(ctx, RX - 40, RY - 380, 1.3 * eout(pop(lf, replug + 6, replug + 14)) + 0.01, 3)
        for i in range(6):
            a = lf * 0.08 + i * 1.05
            sparkle(ctx, RX + math.cos(a) * 170, RY - 150 + math.sin(a) * 120, 30 * (0.6 + 0.4 * math.sin(lf * 0.3 + i)), hx('fff27a'))
    ctx.restore()
    if lf < 40:
        label(ctx, "*SIGH*", 540, 1440, 100, (1, 1, 1), 0.03, pop(lf, 10, 14))
    elif lf < replug:
        label(ctx, "OFF..." if lf < 66 else "...AND ON.", 540, 1440, 110, hx('ffe14d'), -0.03, pop(lf, unplug if lf < 66 else 66, (unplug if lf < 66 else 66) + 4))
    else:
        label(ctx, "FIXED.", 540, 1440, 140, hx('5fd07a'), 0.04, pop(lf, replug + 6, replug + 10))
    card(ctx, 'p6', f, 724, 876)


def s7(ctx, f):
    lf = f - 880
    yank = 96
    dark_ = lf >= yank
    rise = eout(pop(lf, 6, 30))
    z = kf(lf, [(0, 1.0), (yank - 1, 1.18), (yank, 1.1), (170, 1.18)], eout)
    ctx.save(); cam(ctx, kf(lf, [(0, 600), (yank, 620)], eout), 1160, z, 0, shake_at(lf, [yank], 12, 24), f)
    living(ctx, f, tv='on' if not dark_ else 'off')
    sofa(ctx)
    bh = boy_sofa(ctx, f, 'play' if not dark_ else 'spin', eye='happy', mouth='grin', tab=not dark_)
    router(ctx, RX, RY, f, 'green' if not dark_ else 'off')
    # Dad rises from behind the cabinet, wrapped in cables, proud
    proud = lf >= 30
    step_ = eout(pop(lf, 78, yank))
    dp = P(eye='smug' if proud else 'normal', mouth='grin', torso=-6 if proud else 0, lsh=-40, lel=-80, rsh=170 if proud else 30, rel=-20)
    dx = lerp(620, 470, step_)
    behind = lf < 30
    if behind:
        dx = 700
    dyy = lerp(STAND - 186 * KD + 420, STAND - 186 * KD - 120, rise) if behind else STAND - 186 * KD
    if behind:
        ctx.save(); ctx.rectangle(-500, -1500, 2500, 2800); ctx.clip()
    dh = draw(ctx, dx, dyy, KD, 1, DAD, dp)
    frizz(ctx, dh, 1.0)
    headlamp(ctx, dh, 1, beam=False)
    tangle(ctx, dx, dyy + 186 * KD * 0.55, 110, 160, 1.0, seed=5)
    if behind:
        ctx.restore()
        ctx.rectangle(560, 1300, 460, 150); fl(ctx, hx('c98b55'), 7)
        for xx in (580, 800):
            ctx.rectangle(xx, 1320, 200, 110); fl(ctx, light(hx('c98b55'), 0.2), 4)
    if 30 <= lf < 44:
        puff(ctx, dx, 1300, pop(lf, 30, 44), 1.6)
    mh = draw(ctx, 910, STAND - 186 * KM, KM, -1, MOM, P(eye='smug', mouth='smile', lsh=-40, lel=-80, rsh=-40, rel=-80))
    # the cable that drags behind him to the wall
    ctx.new_path(); ctx.move_to(dx + 60, STAND - 200); ctx.curve_to(dx + 250, STAND - 60, 900, 1440, 1020 if not dark_ else 860, 1370 if not dark_ else 1460)
    setc(ctx, INK); ctx.set_line_width(22); ctx.stroke_preserve(); setc(ctx, hx('ff8a3d')); ctx.set_line_width(13); ctx.stroke()
    ctx.rectangle(1000, 1330, 50, 70); fl(ctx, (1, 1, 1), 5)
    if dark_:
        plug(ctx, 860, 1460, 1.4, hx('ff8a3d'), 1.0)
        ctx.rectangle(-1200, -1500, 3600, 4000); setc(ctx, (0.02, 0.02, 0.06, 0.94)); ctx.fill()
        if lf >= yank + 18:
            dark_eyes(ctx, dh['head'][0] + 6, dh['head'][1] + 6, 1.1, lf, 'normal', 1, 1)
            dark_eyes(ctx, bh['head'][0] + 6, bh['head'][1] + 6, 0.9, lf, 'normal', 1, 2)
        if lf >= yank + 34:
            dark_eyes(ctx, mh['head'][0] - 6, mh['head'][1] + 6, 1.0, lf, 'glare', -1, 3)
    ctx.restore()
    if lf < 30:
        pass
    elif lf < 78:
        label(ctx, "WE DID IT!", 540, 1360, 100, hx('ffe14d'), -0.03, pop(lf, 32, 36))
        label(ctx, "TEAMWORK!", 540, 1470, 84, hx('5fd07a'), 0.03, pop(lf, 44, 48))
    elif lf < yank:
        pass
    elif lf < yank + 50:
        label(ctx, "*YANK* *CLICK*", 540, 1440, 96, (1, 1, 1), 0.03, pop(lf, yank, yank + 4))
    elif lf < 140:
        label(ctx, "...OOPS.", 540, 1440, 110, hx('ffe14d'), -0.03, pop(lf, yank + 52, yank + 56))
    else:
        label(ctx, "I GOT THIS!", 540, 1440, 120, hx('ffe14d'), 0.04, pop(lf, 142, 146))
    card(ctx, 'p7', f, 884)


SHOTS = [(0, s1), (100, s2), (220, s3), (400, s4), (540, s5), (720, s6), (880, s7)]


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.25)
    ctx.set_source(g); ctx.paint()
    for c in (100, 156, 220, 280, 338, 400, 496, 540, 658, 720, 812, 880, 976):
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.5 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/w{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/wifi_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
