"""'The Last Cookie' - original, general-audience comedy short, ~35s."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw
from scenes6 import cam, pop, sparkle, puff, label, shake_at, run_pose, crumbs
from scenes8 import walk
from scenes11 import half

BOY, MOM, DAD = doodle.BOY, doodle.MOM_G, doodle.DAD
N = 1050
STAND = 1500
KB, KD = 1.3, 1.45
ISL = (250, 830, 1250)          # kitchen island x0, x1, top y
JAR = (540, 1250)               # jar bottom-centre on island
BX, DX = 800, 285               # boy / dad standing x behind island

CAPS = {
    'p1': [[("WHEN THERE'S", OUT)], [("ONE ", OUT), ("COOKIE", hx('e07b12')), (" LEFT...", OUT)]],
    'p2': [[("MIDNIGHT. ", OUT), ("MISSION: COOKIE", hx('1f8bff'))]],
    'p3': [[("BUT I WASN'T ", OUT), ("ALONE", hx('ff3b5c'))]],
    'p4': [[("THE ", OUT), ("STANDOFF", hx('e07b12'))]],
    'p5': [[("CASE CLOSED...", OUT)], [("OR WAS IT?", hx('8a3cff'))]],
    'p6': [[("MOM WAS PLAYING", OUT)], [("THE ", OUT), ("LONG GAME", hx('ff3b5c'))]],
}


def card(ctx, key, f, appear, gone=10 ** 9):
    u = min(pop(f, appear, appear + 6), 1 - pop(f, gone - 5, gone))
    if u <= 0:
        return
    lines = CAPS[key]; size = 70
    ctx.save()
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    widths = [sum(ctx.text_extents(t).x_advance for t, _ in ln) for ln in lines]
    mw = max(widths)
    if mw > 820:
        size *= 820 / mw; ctx.set_font_size(size); widths = [sum(ctx.text_extents(t).x_advance for t, _ in ln) for ln in lines]; mw = max(widths)
    w = mw + 70; lh = size * 1.18; h = lh * len(lines) + 40
    s = 0.7 + 0.3 * eout(u)
    ctx.translate(W / 2, 300 + h / 2); ctx.scale(s, s)
    ctx.rectangle(-w / 2 + 8, -h / 2 + 10, w, h); setc(ctx, (0, 0, 0, 0.35 * u)); ctx.fill()
    ctx.rectangle(-w / 2, -h / 2, w, h); setc(ctx, (1, 1, 1, 0.97 * u)); ctx.fill_preserve(); setc(ctx, OUT + (u,)); ctx.set_line_width(5); ctx.stroke()
    y = -h / 2 + 20 + size * 0.92
    for ln, lw_ in zip(lines, widths):
        x = -lw_ / 2
        for t, col in ln:
            ctx.move_to(x, y); ctx.text_path(t); setc(ctx, col[:3] + (u,)); ctx.fill()
            x += ctx.text_extents(t).x_advance
        y += lh
    ctx.restore()


# ------------------------------------------------------------------ props
def cookie(ctx, x, y, r, bite=0.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ctx.new_path(); ctx.arc(0, 0, r, 0, 2 * math.pi)
    if bite > 0:
        for k in range(3):
            ctx.new_sub_path(); ctx.arc_negative(r * 0.95, -r * 0.35 + k * r * 0.35, r * 0.32 * bite, math.pi * 1.5, math.pi * 0.5)
        ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    fl(ctx, hx('e8a85a'), max(3, r * 0.08))
    for i, (cx, cy) in enumerate(((-0.4, -0.3), (0.2, -0.45), (0.35, 0.15), (-0.2, 0.35), (-0.5, 0.2), (0.05, 0.0))):
        if bite > 0 and cx > 0.3:
            continue
        ellipse(ctx, cx * r, cy * r, r * 0.12, r * 0.1, i); setc(ctx, hx('5a3218')); ctx.fill()
    ctx.restore()


def jar(ctx, x, yb, s=1.0, cookies=1, lid=0.0, glow=0.0, a=0.0):
    """glass cookie jar, bottom-centre at (x, yb). lid: 0 closed .. 1 off"""
    ctx.save(); ctx.translate(x, yb); ctx.rotate(a); ctx.scale(s, s)
    if glow > 0:
        g = cairo.RadialGradient(0, -110, 20, 0, -110, 300); g.add_color_stop_rgba(0, 1, 0.9, 0.5, 0.7 * glow); g.add_color_stop_rgba(1, 1, 0.9, 0.5, 0)
        ctx.set_source(g); ctx.arc(0, -110, 300, 0, 7); ctx.fill()
    if cookies:
        cookie(ctx, 0, -48, 46, a=0.3)
    ctx.new_path(); ctx.move_to(-95, -190); ctx.line_to(-95, -20); ctx.curve_to(-95, 0, -80, 0, -60, 0); ctx.line_to(60, 0); ctx.curve_to(80, 0, 95, 0, 95, -20); ctx.line_to(95, -190)
    setc(ctx, (0.75, 0.92, 1, 0.35)); ctx.fill_preserve(); ink(ctx, 7); ctx.stroke()
    ctx.rectangle(-70, -175, 14, 140); setc(ctx, (1, 1, 1, 0.7)); ctx.fill()
    ctx.rectangle(-105, -212, 210, 24); fl(ctx, hx('dff6ff'), 6)
    # lid
    ctx.save(); ctx.translate(lerp(0, -210, lid), lerp(-212, -12, lid) - math.sin(lid * math.pi) * 160); ctx.rotate(-math.sin(lid * math.pi) * 1.2)
    ctx.new_path(); ctx.move_to(-110, 0); ctx.curve_to(-100, -50, 100, -50, 110, 0); ctx.close_path(); fl(ctx, hx('ff3b5c'), 6)
    ellipse(ctx, 0, -40, 22, 16); fl(ctx, hx('ffd23f'), 5)
    ctx.restore()
    ctx.restore()


def flashlight(ctx, x, y, ang, on=True, length=700, spread=0.32, a=1.0):
    if on and a > 0:
        ctx.new_path(); ctx.move_to(x, y)
        ctx.line_to(x + math.cos(ang - spread) * length, y + math.sin(ang - spread) * length)
        ctx.line_to(x + math.cos(ang + spread) * length, y + math.sin(ang + spread) * length); ctx.close_path()
        g = cairo.LinearGradient(x, y, x + math.cos(ang) * length, y + math.sin(ang) * length)
        g.add_color_stop_rgba(0, 1, 0.97, 0.7, 0.55 * a); g.add_color_stop_rgba(1, 1, 0.97, 0.7, 0)
        ctx.set_source(g); ctx.fill()
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    ctx.rectangle(-70, -13, 62, 26); fl(ctx, hx('3a4258'), 4)
    ctx.rectangle(-12, -20, 18, 40); fl(ctx, hx('ffd23f') if on else hx('8a8a96'), 4)
    ctx.restore()


def dim(ctx, a=1.0):
    if a > 0:
        ctx.rectangle(-2000, -2000, 6000, 6000); setc(ctx, (0.04, 0.05, 0.18, 0.72 * a)); ctx.fill()


def kitchen_bg(ctx):
    ctx.rectangle(-900, -900, W + 1800, 2400); setc(ctx, hx('fff1dc')); ctx.fill()
    setc(ctx, hx('ffd9b0')); ctx.set_line_width(3)
    for j in range(8):
        ctx.move_to(-900, 760 + j * 70); ctx.line_to(W + 900, 760 + j * 70)
    ctx.stroke()
    # wall cabinets
    for x0 in (-260, 80, 700, 1040):
        ctx.rectangle(x0, 380, 300, 300); fl(ctx, hx('7fd1c3'), 7)
        ellipse(ctx, x0 + 150, 640, 12, 12); fl(ctx, hx('ffd23f'), 3)
    # window w/ moon
    ctx.rectangle(400, 380, 280, 300); fl(ctx, hx('1d2a66'), 7)
    ellipse(ctx, 600, 460, 40, 40); fl(ctx, hx('fff2b0'), 4)
    ctx.move_to(540, 380); ctx.line_to(540, 680); ink(ctx, 6); ctx.stroke()
    # doorway right
    ctx.rectangle(1080, 760, 300, 740); fl(ctx, hx('ffe9a8'), 8)
    ctx.rectangle(-900, 1500, W + 1800, 800); setc(ctx, hx('e3c9a8')); ctx.fill()
    ctx.move_to(-900, 1500); ctx.line_to(W + 900, 1500); ink(ctx, 8); ctx.stroke()


def island(ctx):
    x0, x1, y = ISL
    ctx.rectangle(x0, y + 30, x1 - x0, STAND - y - 30); fl(ctx, hx('3f7bff'), 8)
    for i in range(3):
        xx = lerp(x0, x1, (i + 0.5) / 3)
        ctx.rectangle(xx - 75, y + 80, 150, 140); fl(ctx, hx('5f95ff'), 5)
        ellipse(ctx, xx, y + 120, 10, 10); fl(ctx, hx('ffd23f'), 3)
    ctx.rectangle(x0 - 30, y, x1 - x0 + 60, 36); fl(ctx, hx('f2f2f8'), 7)


def scene(ctx, f, boy=None, dad=None, mom=None, jar_kw=None, dark_a=1.0, beams=(), z=1.0, cx=540, cy=1150, shake=0, after=None):
    """boy/dad/mom: (x, ground_y, facing, pose). beams: list of (who, ang) — flashlight from that char's front hand."""
    ctx.save(); cam(ctx, cx, cy, z, 0, shake, f)
    kitchen_bg(ctx)
    hs = {}
    for key, ch, k in (('mom', MOM, KD), ('dad', DAD, KD), ('boy', BOY, KB)):
        c = {'boy': boy, 'dad': dad, 'mom': mom}[key]
        if c:
            x, g, fc, p = c
            hs[key] = draw(ctx, x, g - 186 * k, k, fc, ch, p)
    island(ctx)
    if jar_kw is not None:
        jar(ctx, *JAR, **jar_kw)
    if after:
        after(ctx, hs)
    dim(ctx, dark_a)
    for who, ang in beams:
        if who in hs:
            fx, fy = hs[who]['front']
            flashlight(ctx, fx, fy, ang)
    ctx.restore()
    return hs


def tiptoe(ph, **kw):
    s = math.sin(ph)
    p = P(torso=8, lhip=22 * s, lkn=-30 - 20 * max(0, s), rhip=-22 * s, rkn=-30 - 20 * max(0, -s), lsh=-30, lel=-90, rsh=80, rel=-10,
          eye='normal', mouth='flat')
    p.update(kw); return p


def hallway(ctx, f):
    ctx.rectangle(-900, -900, 4000, 2400); setc(ctx, hx('7fb0ff')); ctx.fill()
    setc(ctx, hx('6a9cf0')); ctx.set_line_width(14)
    for i in range(-10, 40):
        ctx.move_to(i * 110, 300); ctx.line_to(i * 110, 1500)
    ctx.stroke()
    # frames (abstract art)
    for x, c in ((150, hx('ff8a3d')), (1050, hx('5fd07a')), (1900, hx('ff3b8a'))):
        ctx.rectangle(x, 640, 220, 170); fl(ctx, hx('fff1c9'), 7)
        ellipse(ctx, x + 110, 725, 50, 50); fl(ctx, c, 5)
    # parents' door
    ctx.rectangle(560, 620, 300, 880); fl(ctx, hx('c98b55'), 8)
    ellipse(ctx, 610, 1080, 14, 14); fl(ctx, hx('ffd23f'), 4)
    # stairs down at far right
    for i in range(6):
        ctx.rectangle(2300 + i * 90, 1500 - (6 - i) * 0 + i * 60, 400, 60); fl(ctx, hx('d8b48a'), 5)
    ctx.rectangle(-900, 1500, 4000, 800); setc(ctx, hx('d8b48a')); ctx.fill()
    ctx.move_to(-900, 1500); ctx.line_to(3100, 1500); ink(ctx, 8); ctx.stroke()


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    # hook: the last cookie, spotlit like treasure
    z = kf(f, [(0, 1.0), (90, 1.35)], eout)
    ctx.save(); cam(ctx, 540, 1080, z, 0, 0, f)
    ctx.rectangle(-900, -900, 3000, 4000); setc(ctx, hx('241a4a')); ctx.fill()
    for i in range(16):
        a = i * math.pi / 8 + f * 0.01
        ctx.move_to(540, 1050); ctx.line_to(540 + math.cos(a) * 2000, 1050 + math.sin(a) * 2000); ctx.line_to(540 + math.cos(a + 0.18) * 2000, 1050 + math.sin(a + 0.18) * 2000); ctx.close_path()
    setc(ctx, hx('2f2460')); ctx.fill()
    ctx.new_path(); ctx.move_to(470, -200); ctx.line_to(610, -200); ctx.line_to(900, 1350); ctx.line_to(180, 1350); ctx.close_path()
    setc(ctx, (1, 0.95, 0.7, 0.22)); ctx.fill()
    ctx.rectangle(60, 1350, 960, 60); fl(ctx, hx('f2f2f8'), 7)
    ctx.rectangle(80, 1410, 920, 400); fl(ctx, hx('3f7bff'), 7)
    jar(ctx, 540, 1352, 2.0, glow=0.6 + 0.4 * math.sin(f * 0.2))
    for i in range(5):
        sparkle(ctx, 540 + math.cos(i * 1.3 + f * 0.08) * 300, 1100 + math.sin(i * 1.3 + f * 0.08) * 260, 40 * abs(math.sin(f * 0.25 + i)), (1, 1, 1))
    ctx.restore()
    label(ctx, "THE LAST ONE.", 540, 1440, 110, hx('ffcf3d'), -0.04, pop(f, 46, 52))
    card(ctx, 'p1', f, 2, 98)


def s2(ctx, f):
    lf = f - 100
    creak = 58 <= lf < 92
    # boy tiptoes past the parents' door; camera tracks
    if lf < 58:
        bx = lerp(150, 560, lf / 58)
    elif creak:
        bx = 560
    else:
        bx = lerp(560, 1300, ein(pop(lf, 92, 150)))
    ccx = clamp(bx + 60, 540, 1200)
    ctx.save(); cam(ctx, ccx, 1100, 1.1, 0, shake_at(lf, [58], 8, 14), f)
    hallway(ctx, f)
    if creak:
        p = P(torso=4, lhip=-14, lkn=-40, rhip=6, rkn=-10, lsh=-40, lel=-90, rsh=80, rel=-10, eye='shock', mouth='scream')
        p['head'] = 6
    elif lf >= 92:
        p = run_pose(lf * 1.2, eye='shock', mouth='flat', rsh=80, rel=-10)
    else:
        p = tiptoe(lf * 0.35)
    gy = STAND - 186 * KB - (abs(math.sin(lf * 0.35)) * 18 if lf < 58 else 0)
    h = draw(ctx, bx, gy, KB, 1, BOY, p)
    dim(ctx, 0.9)
    fx, fy = h['front']
    flashlight(ctx, fx, fy, 0.35)
    # snores from the parents' room
    for i in range(3):
        t = ((lf + i * 14) % 42) / 42
        label(ctx, "z", 830 + i * 40, 760 - t * 160, 50 + i * 12, (1, 1, 1), 0.2, 1 - t)
    ctx.restore()
    if lf < 58:
        label(ctx, "*TIPTOE* *TIPTOE*", 540, 1440, 76, (1, 1, 1), 0.03, pop(lf, 8, 12))
    elif creak:
        label(ctx, "CREEEAK!", 540, 1300, 130, hx('ff3b5c'), -0.05, pop(lf, 58, 62))
        label(ctx, "*FREEZES*", 540, 1440, 76, (1, 1, 1), 0.03, pop(lf, 66, 70))
    else:
        hlines(ctx, lf, 0.35, col=(1, 1, 1), y0=900, y1=1450)
    card(ctx, 'p2', f, 104, 246)


def s3(ctx, f):
    lf = f - 250
    caught = lf >= 82
    bx = lerp(1250, BX, eout(pop(lf, 0, 40)))
    reach = pop(lf, 44, 64)
    if lf < 40:
        bp = walk(lf * 0.5, eye='normal', mouth='flat', rsh=80, rel=-10)
    elif not caught:
        bp = P(torso=-8, eye='happy', mouth='grin', rsh=lerp(80, 95, reach), rel=-5, lsh=lerp(10, 80, reach), lel=-10)
    else:
        bp = P(torso=4, eye='shock', mouth='scream', rsh=80, rel=-10, lsh=60, lel=-30, head=-6)
    rise = eout(pop(lf, 82, 92))
    dg = STAND + lerp(330, 0, rise)
    dp = P(eye='shock' if lf < 100 else 'glare', mouth='scream' if lf < 100 else 'frown', rsh=80, rel=-10, lsh=70, lel=-20)
    beams = [('boy', math.pi + (0.35 if not caught else 0.05))]
    if caught:
        beams.append(('dad', 0.0))
    hs = scene(ctx, f, boy=(bx, STAND, -1, bp), dad=(DX, dg, 1, dp), jar_kw=dict(lid=0, glow=0.3 * reach), dark_a=1.0, beams=beams,
               z=kf(lf, [(0, 1.0), (60, 1.15), (82, 1.15), (88, 1.0)], eout), cx=560, cy=1130, shake=shake_at(lf, [82], 10, 22))
    if lf < 82 and lf >= 44:
        label(ctx, "ALMOST...", 540, 1440, 90, hx('ffe14d'), -0.03, pop(lf, 46, 50))
    if caught:
        label(ctx, "DAD?!", 250, 690, 110, hx('ffe14d'), -0.08, pop(lf, 88, 92))
        label(ctx, "SON?!", 830, 690, 110, hx('8fe9ff'), 0.08, pop(lf, 104, 108))
        label(ctx, "*CLICK*", 540, 1440, 76, (1, 1, 1), 0.03, pop(lf, 82, 86) * (1 if lf < 104 else 0))
    card(ctx, 'p3', f, 340, 398)


def eyes_half(ctx, top, ch, k, f, lf, fc, lines_col):
    def dfn(c):
        c.rectangle(-900, -900, 3000, 4000); setc(c, hx('1d1640') if top else hx('2a1838')); c.fill()
        for i in range(14):
            a = i * math.pi / 7 + lf * 0.01 * (1 if top else -1)
            c.move_to(540, 1100); c.line_to(540 + math.cos(a) * 2000, 1100 + math.sin(a) * 2000); c.line_to(540 + math.cos(a + 0.2) * 2000, 1100 + math.sin(a + 0.2) * 2000); c.close_path()
        setc(c, lines_col); c.fill()
        p = P(eye='glare', mouth='frown', head=4 * math.sin(lf * 0.2) * (1 if top else -1))
        h = draw(c, 540, 1500 - 186 * k, k, fc, ch, p)
        # under-chin flashlight glow
        g = cairo.RadialGradient(540, h['head'][1] + 200, 20, 540, h['head'][1] + 200, 420)
        g.add_color_stop_rgba(0, 1, 0.95, 0.6, 0.35); g.add_color_stop_rgba(1, 1, 0.95, 0.6, 0)
        c.set_source(g); c.paint()
    return dfn


def s4(ctx, f):
    lf = f - 400
    zt = kf(lf, [(0, 1.0), (100, 1.0), (110, 1.9), (160, 2.1)], eout)
    zb = kf(lf, [(0, 1.0), (100, 1.0), (114, 1.9), (160, 2.1)], eout)
    sh = shake_at(lf, [100, 104], 6, 10)
    ctx.save(); ctx.translate(random.Random(f).uniform(-sh, sh), 0)
    half(ctx, True, 540, 857, zt, eyes_half(ctx, True, DAD, 1.6, f, lf, 1, hx('2c2260')))
    half(ctx, False, 540, 1167, zb, eyes_half(ctx, False, BOY, 1.6, f, lf, -1, hx('3c2250')))
    ctx.restore()
    # divider bolt
    poly(ctx, [(0, 940), (420, 940), (470, 905), (520, 975), (570, 935), (1080, 935), (1080, 985), (575, 985), (520, 1025), (470, 955), (420, 990), (0, 990)])
    fl(ctx, hx('ffd23f'), 6)
    jar(ctx, 540, 1035, 0.5, glow=0.8)
    if lf < 100:
        label(ctx, "IT'S MINE.", 540, 860, 100, hx('ffe14d'), -0.04, pop(lf, 14, 18))
        if lf >= 50:
            label(ctx, "I SAW IT FIRST.", 540, 1430, 96, hx('8fe9ff'), 0.04, pop(lf, 50, 54))


def s5(ctx, f):
    lf = f - 560
    lights = lf >= 96
    if lf < 96:
        # lunge + tug of war over the jar
        lunge = eout(pop(lf, 0, 14))
        tug = math.sin(lf * 0.55) * (1 if lf >= 18 else 0)
        jx = 540 + tug * 35
        bx = lerp(BX, 750, lunge) + tug * 35
        dx = lerp(DX, 330, lunge) + tug * 35
        bp = P(torso=-10 + tug * 6, eye='glare', mouth='scream', rsh=90, rel=0, lsh=85, lel=0)
        dp = P(torso=10 + tug * 6, eye='glare', mouth='scream', rsh=90, rel=0, lsh=85, lel=0)

        def after(c, hs):
            jar(c, jx, JAR[1] - 40, 0.8, a=tug * 0.15)
        scene(ctx, f, boy=(bx, STAND, -1, bp), dad=(dx, STAND, 1, dp), dark_a=1.0, beams=[], z=1.12, cx=540, cy=1120,
              shake=4 if lf >= 18 else 0, after=after)
        if lf < 18:
            hlines(ctx, lf, 0.5, col=(1, 1, 1), y0=800, y1=1400)
        if lf >= 18:
            word = ["MINE!", "NO, MINE!"][(lf // 20) % 2]
            label(ctx, word, 300 if word == "MINE!" else 780, 690, 96, hx('ffe14d') if word == "MINE!" else hx('8fe9ff'), 0.05 * (1 if word == "MINE!" else -1), 1)
            label(ctx, "*TUG OF WAR*", 540, 1440, 76, (1, 1, 1), 0.03, pop(lf, 22, 26))
    elif lf < 140:
        # lights on: low-angle mom in doorway
        ll = lf - 96
        ctx.save(); cam(ctx, 540, 1080, kf(ll, [(0, 1.25), (20, 1.1)], eout), -4, shake_at(ll, [0], 10, 20), f)
        ctx.rectangle(-900, -900, 3000, 4000); setc(ctx, hx('ffe9a8')); ctx.fill()
        ctx.rectangle(-900, -900, 330, 4000); fl(ctx, hx('fff1dc'), 8); ctx.rectangle(820, -900, 900, 4000); fl(ctx, hx('fff1dc'), 8)
        ctx.rectangle(-60, 820, 110, 160); fl(ctx, (1, 1, 1), 6); ctx.rectangle(-20, 850, 30, 60); fl(ctx, hx('ffd23f'), 4)
        ctx.rectangle(-900, 1500, 3000, 800); setc(ctx, hx('e3c9a8')); ctx.fill()
        draw(ctx, 560, STAND - 186 * 1.75, 1.75, -1, MOM, P(eye='glare', mouth='open' if ll % 10 < 6 else 'frown', lsh=-30, lel=-120, rsh=-30, rel=-120))
        ctx.restore()
        label(ctx, "WHAT IS GOING ON", 540, 1330, 92, hx('ff3b5c'), -0.03, pop(ll, 4, 8))
        label(ctx, "IN HERE?!", 540, 1440, 92, hx('ff3b5c'), 0.03, pop(ll, 10, 14))
    else:
        # caught: both innocent, hands behind backs
        ll = lf - 140
        bp = P(eye='happy', mouth='smile', rsh=-20, rel=0, lsh=-20, lel=0, head=6 * math.sin(ll * 0.2))
        dp = P(eye='happy', mouth='wavy', rsh=-20, rel=0, lsh=-20, lel=0, head=-6 * math.sin(ll * 0.2))
        scene(ctx, f, boy=(BX - 30, STAND, -1, bp), dad=(DX + 30, STAND, 1, dp), jar_kw=dict(), dark_a=0, z=1.05, cx=540, cy=1120)
        for i, x in enumerate((DX + 130, BX - 170)):
            t = ((ll + i * 8) % 20) / 20
            label(ctx, "~", x + 40 * t, 830 - 70 * t, 60, (1, 1, 1), 0, 1 - t)
        label(ctx, "*INNOCENT WHISTLING*", 540, 1440, 72, (1, 1, 1), 0.03, pop(ll, 2, 6))


def s6(ctx, f):
    lf = f - 720
    take = pop(lf, 26, 36)
    leave = ein(pop(lf, 80, 140))
    mx = lerp(1250, 540, eout(pop(lf, 0, 26)))
    mp = walk(lf * 0.5, eye='glare', mouth='frown') if lf < 26 else P(eye='glare', mouth='frown', rsh=lerp(60, 90, take), rel=lerp(-20, 0, take), lsh=-30, lel=-120)
    sad = lf >= 40
    bp = P(eye='closed' if sad else 'shock', mouth='frown', torso=8 if sad else 0, head=12 if sad else 0, lsh=5, rsh=-5)
    dp = P(eye='closed' if sad else 'shock', mouth='frown', torso=8 if sad else 0, head=12 if sad else 0, lsh=5, rsh=-5)
    if leave > 0:
        bp = walk(lf * 0.4, eye='closed', mouth='frown', head=12)
        dp = walk(lf * 0.4, eye='closed', mouth='frown', head=12)

    def after(c, hs):
        if lf < 30:
            jar(c, *JAR)
        else:
            fx, fy = hs['mom']['front']
            jar(c, fx - 20, fy + 70, 0.8)
    scene(ctx, f, boy=(BX + 520 * leave, STAND, 1 if leave > 0 else -1, bp), dad=(DX - 520 * leave, STAND, -1 if leave > 0 else 1, dp),
          mom=(mx, STAND, -1, mp), dark_a=0, z=1.0, cx=540, cy=1120, after=after)
    if 30 <= lf < 80:
        label(ctx, "NOBODY GETS IT.", 540, 1440, 96, hx('ff3b5c'), -0.03, pop(lf, 30, 34))
    elif lf >= 80:
        label(ctx, "GO TO BED.", 540, 1440, 96, hx('ff3b5c'), 0.03, pop(lf, 80, 84))
    card(ctx, 'p5', f, 812, 878)


def s7(ctx, f):
    lf = f - 880
    bite = lf >= 60
    zz = kf(lf, [(0, 1.05), (55, 1.35), (62, 1.5), (110, 1.15), (124, 1.0)], eout)
    peek = eout(pop(lf, 118, 128))
    mp = P(eye='smug', mouth='grin', lsh=20, lel=-40, rsh=lerp(60, -150, pop(lf, 36, 50)), rel=lerp(-20, 0, pop(lf, 36, 50)))
    if bite:
        mp.update(eye='happy', mouth='open' if (lf // 5) % 2 == 0 and lf < 100 else 'grin')
    if lf >= 128:
        mp.update(eye='shock', mouth='flat', rsh=-150, rel=0)
    pp = P(eye='glare', mouth='frown')

    def after(c, hs):
        fx, fy = hs['mom']['front']
        if lf < 36:
            jar(c, 330, JAR[1], 0.7, lid=pop(lf, 20, 30))
        else:
            jar(c, 330, JAR[1], 0.7, cookies=0, lid=1)
            fx -= 70 * pop(lf, 40, 50)
            cookie(c, fx, fy, 46, bite=1.0 if bite else 0)
        if bite and lf < 90:
            burst(c, fx - 110, fy - 30, 70 * eout(pop(lf, 60, 66)), 12, lf // 3)
            crumbs(c, lf, 10, fx - 120, fx + 40, fy, fy + 200)
        if peek > 0:
            # boy + dad pop up behind the island edges
            draw(c, 215, STAND + lerp(380, 60, peek) - 186 * KD, KD, 1, DAD, pp)
            draw(c, 830, STAND + lerp(380, 60, peek) - 186 * KB, KB, -1, BOY, pp)
            island(c); jar(c, 330, JAR[1], 0.7, cookies=0, lid=1)
    scene(ctx, f, mom=(540, STAND, -1, mp), dark_a=0.45, z=zz, cx=kf(lf, [(0, 540), (55, 560), (110, 560), (124, 540)]), cy=1080, shake=shake_at(lf, [60, 128], 10, 18), after=after)
    if lf < 36:
        label(ctx, "*LOOKS AROUND*", 540, 1440, 76, (1, 1, 1), 0.03, pop(lf, 4, 8))
    elif lf < 60:
        pass
    elif lf < 118:
        label(ctx, "CHOMP!", 540, 1440, 120, hx('ffcf3d'), -0.05, pop(lf, 60, 64))
    else:
        label(ctx, "MOM?!", 540, 1440, 130, hx('ff3b5c'), 0.05, pop(lf, 128, 132))
    card(ctx, 'p6', f, 948)


SHOTS = [(0, s1), (100, s2), (250, s3), (400, s4), (560, s5), (720, s6), (880, s7)]


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.28)
    ctx.set_source(g); ctx.paint()
    for c in (100, 250, 332, 400, 500, 560, 656, 700, 720, 880, 1008):
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.55 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/c{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/cookie_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
