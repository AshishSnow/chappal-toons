"""'Phone at 1%' - original, general-audience comedy short, ~22s.
Kid's phone hits 1%: full panic. Tears the room apart for a charger, finds one... the cable is tiny, so he lives
on the floor now. Meanwhile Mom's phone has been at 1% for three days and she does not care at all.
The shock knocks his plug out -> back to 1% -> loop."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import cam, pop, sparkle, puff, label, shake_at
from scenes8 import sit, sock
from scenes13 import card as _card13
import scenes13

BOY, MOM = doodle.BOY, doodle.MOM_G
N = 660
FLOOR = 1500
OUTX, OUTY = 930, 1400

CAPS = {
    'p1': [[("MY PHONE AT ", OUT), ("1%", hx('ff3b5c')), (":", OUT)]],
    'p2': [[("THE ", OUT), ("SEARCH", hx('1f8bff'))]],
    'p3': [[("THE CABLE WAS ", OUT), ("TINY", hx('8a3cff'))]],
    'p4': [[("MEANWHILE, ", OUT), ("MOM'S", hx('ff3b8a'))], [("PHONE:", OUT)]],
    'p5': [[("3 DAYS ", OUT), ("LATER", hx('1f8bff'))]],
}
scenes13.CAPS = CAPS
card = _card13


def rect_r(ctx, x, y, w, h, r):
    ctx.new_path(); ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); ctx.close_path()


def wtext(ctx, s, x, y, size, col):
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s)
    ctx.move_to(x - e.x_advance / 2, y + e.height / 2); ctx.text_path(s); setc(ctx, col); ctx.fill()


# ------------------------------------------------------------------ props
def phone(ctx, x, y, s, pct, a=0.0, f=0, charging=False, case=hx('1f8bff')):
    """phone centred at x,y; s = scale (1 -> 120x220)"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -60, -110, 120, 220, 22); fl(ctx, case, 6)
    rect_r(ctx, -48, -96, 96, 192, 12); fl(ctx, hx('15152a'), 3)
    low = pct <= 2
    col = hx('ff3b5c') if low else hx('2fe07a')
    on = (not low) or charging or (f // 8) % 2 == 0
    # battery icon
    rect_r(ctx, -30, -60, 60, 100, 8); setc(ctx, (1, 1, 1)); ctx.set_line_width(5); ctx.stroke()
    ctx.rectangle(-12, -70, 24, 10); setc(ctx, (1, 1, 1)); ctx.fill()
    lvl = max(0.08, pct / 100)
    if on:
        ctx.rectangle(-23, 33 - 86 * lvl, 46, 86 * lvl); setc(ctx, col); ctx.fill()
    if charging:
        poly(ctx, [(4, -48), (-16, -6), (0, -6), (-6, 28), (16, -16), (0, -16)]); fl(ctx, hx('ffe14d'), 3)
    wtext(ctx, f"{pct}%", 0, 72, 34, col if on else (1, 1, 1))
    ctx.restore()


def charger(ctx, x, y, a=0.0, s=1.0, glow=0.0, cable=(0, 70)):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if glow > 0:
        for k in range(10):
            ang = k * math.pi / 5 + glow * 2
            ctx.move_to(math.cos(ang) * 60, math.sin(ang) * 60); ctx.line_to(math.cos(ang) * 120, math.sin(ang) * 120)
        setc(ctx, (1, 0.95, 0.4, 0.9 * min(1, glow))); ctx.set_line_width(10); ctx.stroke()
    ctx.move_to(0, 20); ctx.line_to(*cable); setc(ctx, INK); ctx.set_line_width(16); ctx.stroke_preserve()
    setc(ctx, (1, 1, 1)); ctx.set_line_width(9); ctx.stroke()
    rect_r(ctx, -32, -38, 64, 62, 10); fl(ctx, (1, 1, 1), 5)
    for px in (-12, 12):
        ctx.rectangle(px - 4, -60, 8, 22); fl(ctx, hx('c8c8d8'), 3)
    ctx.restore()


def pillow(ctx, x, y, a, col=hx('ff8fb8')):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    rect_r(ctx, -80, -46, 160, 92, 36); fl(ctx, col, 6)
    ctx.restore()


def mug(ctx, x, y, s=1.0, steam=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(46, 0, 22, -1.4, 1.4); ink(ctx, 16); ctx.stroke()
    ctx.new_path(); ctx.arc(46, 0, 22, -1.4, 1.4); setc(ctx, hx('ffe14d')); ctx.set_line_width(8); ctx.stroke()
    rect_r(ctx, -44, -50, 88, 100, 14); fl(ctx, hx('ffe14d'), 6)
    ellipse(ctx, 0, -6, 14, 12); setc(ctx, hx('ff3b5c')); ctx.fill()
    for k in range(3):
        sx = -20 + k * 20; o = math.sin(steam * 0.2 + k) * 8
        ctx.move_to(sx, -64); ctx.curve_to(sx + o, -90, sx - o, -110, sx + o, -135); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(7); ctx.stroke()
    ctx.restore()


def bedroom(ctx, mess=0.0):
    ctx.rectangle(-1500, -1500, 4200, 4200); setc(ctx, hx('7fd4ff')); ctx.fill()
    for i in range(-6, 12):
        ctx.rectangle(i * 160, -200, 70, FLOOR + 200); setc(ctx, (1, 1, 1, 0.14)); ctx.fill()
    # window
    rect_r(ctx, 560, 640, 360, 330, 18); fl(ctx, hx('ffe9a8'), 8)
    ctx.move_to(740, 640); ctx.line_to(740, 970); ctx.move_to(560, 805); ctx.line_to(920, 805); ink(ctx, 6); ctx.stroke()
    ellipse(ctx, 830, 720, 44, 44); setc(ctx, hx('ffb000')); ctx.fill()
    # poster (original: a rocket)
    rect_r(ctx, 120, 600, 260, 330, 10); fl(ctx, hx('ff8a3d'), 7)
    poly(ctx, [(250, 650), (300, 760), (300, 840), (200, 840), (200, 760)]); fl(ctx, (1, 1, 1), 5)
    ellipse(ctx, 250, 760, 22, 22); fl(ctx, hx('1f8bff'), 4)
    poly(ctx, [(220, 840), (250, 900), (280, 840)]); fl(ctx, hx('ffe14d'), 4)
    # bed
    rect_r(ctx, -300, 1180, 620, 120, 30); fl(ctx, hx('ffffff'), 7)
    rect_r(ctx, -300, 1270, 620, 230, 20); fl(ctx, hx('ff3b8a'), 7)
    rect_r(ctx, 290, 1060, 40, 440, 14); fl(ctx, hx('8a5a34'), 6)
    # floor
    ctx.rectangle(-1500, FLOOR, 4200, 900); setc(ctx, hx('d9a46a')); ctx.fill()
    for i in range(-6, 14):
        ctx.move_to(i * 200 + 40, FLOOR); ctx.line_to(i * 200 - 80, FLOOR + 600); setc(ctx, (0, 0, 0, 0.12)); ctx.set_line_width(5); ctx.stroke()
    ctx.move_to(-1500, FLOOR); ctx.line_to(2700, FLOOR); ink(ctx, 8); ctx.stroke()
    # outlet
    rect_r(ctx, OUTX - 40, OUTY - 55, 80, 110, 12); fl(ctx, (1, 1, 1), 6)
    for dy in (-22, 22):
        ctx.rectangle(OUTX - 14, OUTY + dy - 6, 6, 14); ctx.rectangle(OUTX + 8, OUTY + dy - 6, 6, 14); setc(ctx, INK); ctx.fill()
    # mess on the floor
    if mess > 0:
        a = clamp(mess)
        for i, (mx, my, r, c) in enumerate(((120, 1560, 0.4, hx('ff3b8a')), (480, 1600, -0.8, hx('2fbf5a')), (760, 1570, 1.2, hx('8a3cff')),
                                             (-80, 1620, 2.0, hx('1f8bff')))):
            if i < a * 4 + 0.01:
                sock(ctx, mx, my, r, c)
        if a > 0.5:
            pillow(ctx, 620, 1540, 0.2)


def kitchen(ctx):
    ctx.rectangle(-1500, -1500, 4200, 4200); setc(ctx, hx('ffd9a8')); ctx.fill()
    for i in range(-8, 16):
        for j in range(-4, 10):
            if (i + j) % 2 == 0:
                ctx.rectangle(i * 120, 980 + j * 120, 120, 120); setc(ctx, (1, 1, 1, 0.25)); ctx.fill()
    # plant on shelf
    ctx.rectangle(560, 760, 380, 30); fl(ctx, hx('8a5a34'), 6)
    poly(ctx, [(640, 760), (700, 760), (690, 680), (650, 680)]); fl(ctx, hx('ff8a3d'), 5)
    for a in (-0.8, -0.3, 0.2, 0.7):
        ellipse(ctx, 670 + math.sin(a) * 50, 640 - math.cos(a) * 30, 22, 46, a); fl(ctx, hx('2fbf5a'), 4)
    # clock
    ellipse(ctx, 260, 700, 90, 90); fl(ctx, (1, 1, 1), 8)
    ctx.move_to(260, 700); ctx.line_to(260, 640); ctx.move_to(260, 700); ctx.line_to(300, 720); ink(ctx, 7); ctx.stroke()
    ctx.rectangle(-1500, FLOOR, 4200, 900); setc(ctx, hx('9b6a4a')); ctx.fill()
    ctx.move_to(-1500, FLOOR); ctx.line_to(2700, FLOOR); ink(ctx, 8); ctx.stroke()


def table(ctx):
    rect_r(ctx, 380, 1250, 680, 50, 12); fl(ctx, hx('ffffff'), 7)
    for lx in (420, 1000):
        ctx.rectangle(lx, 1300, 30, 200); fl(ctx, hx('8a5a34'), 6)


def cobweb(ctx, x, y, s, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    setc(ctx, (1, 1, 1, 0.85 * a)); ctx.set_line_width(4)
    for k in range(6):
        ang = k * math.pi / 10
        ctx.move_to(0, 0); ctx.line_to(math.cos(ang) * 150, math.sin(ang) * 150)
    ctx.stroke()
    for r in (50, 95, 140):
        ctx.new_path()
        for k in range(6):
            ang = k * math.pi / 10
            pt = (math.cos(ang) * r, math.sin(ang) * r)
            ctx.line_to(*pt) if k else ctx.move_to(*pt)
        ctx.stroke()
    ctx.restore()


def twitch(ctx, x, y, a):
    for k in range(3):
        ang = -0.9 + k * 0.6
        ctx.move_to(x + math.cos(ang) * 50, y + math.sin(ang) * 50)
        ctx.line_to(x + math.cos(ang) * (85 + 10 * a), y + math.sin(ang) * (85 + 10 * a))
    ink(ctx, 8); ctx.stroke()


# ------------------------------------------------------------------ characters
KB = 1.5
BHIP = FLOOR - 92 * KB


def panic_kid(ctx, f, x=540, pct=1, charging=False, mouth='scream', eye='shock'):
    """kid holding phone up next to his face, used in the opening and the loop ending"""
    p = P(lsh=-150, lel=-20, rsh=140, rel=-50, eye=eye, mouth=mouth, torso=-4, head=4 * math.sin(f * 1.3))
    h = draw_hip(ctx, x, BHIP, KB, 1, BOY, p)
    hx_, hy = h['front']
    phone(ctx, hx_ + 30, hy - 60, 1.15, pct, 0.15, f, charging)
    return h


def s1(ctx, f):
    # ECU from frame 0: kid screaming at his phone; pull back on the NOOO
    pull = eout(pop(f, 40, 70))
    z = lerp(2.3, 1.15, pull)
    ctx.save(); cam(ctx, lerp(640, 560, pull), lerp(1000, 1060, pull), z, lerp(-4, 0, pull), shake_at(f, [0, 40], 12, 18) + 3, f)
    bedroom(ctx)
    panic_kid(ctx, f)
    ctx.restore()
    label(ctx, "NOOOOO!", 540, 1450, 140, hx('ff3b5c'), -0.04, pop(f, 2, 8) if f < 40 else 1)
    if f >= 52:
        label(ctx, "NOT LIKE THIS!", 540, 1300, 72, (1, 1, 1), 0.03, pop(f, 52, 56))
    card(ctx, 'p1', f, -6, 96)


def s2(ctx, f):
    lf = f - 96
    if lf < 90:
        # frantic search: kid zips left/right, stuff flies, whip-pan camera follows
        ph = lf * 0.7
        x = 540 + 300 * math.sin(lf * 0.12)
        fac = 1 if math.cos(lf * 0.12) >= 0 else -1
        ctx.save(); cam(ctx, lerp(540, x, 0.5), 1150, 1.05, 3 * math.sin(lf * 0.1), shake_at(lf % 18, [0], 6, 8), f)
        bedroom(ctx, mess=lf / 70)
        p = run_pose(ph, eye='shock', mouth='open', lsh=-150 + 40 * math.sin(ph), rsh=150 - 40 * math.sin(ph), lel=-30, rel=-30)
        draw_hip(ctx, x, BHIP - 10 * abs(math.sin(ph)), KB, fac, BOY, p)
        # flying stuff
        for k in range(4):
            t = ((lf + k * 22) % 40) / 40
            ox = x + fac * (-80 - 500 * t) * (1 if k % 2 else -0.7)
            oy = 1150 - 700 * t + 900 * t * t
            if k == 1:
                pillow(ctx, ox, oy, t * 8, hx('ffe14d'))
            else:
                sock(ctx, ox, oy, t * 10, (hx('ff3b8a'), hx('2fbf5a'), hx('8a3cff'), hx('1f8bff'))[k])
        ctx.restore()
        txt = ["NOT HERE!", "NOT HERE!!", "WHERE IS IT?!"][min(2, lf // 30)]
        label(ctx, txt, 540, 1420, 96, hx('ffe14d'), 0.04 * (-1) ** (lf // 30), pop(lf % 30, 0, 4))
    else:
        # found it: holy glow, push in
        fl_ = lf - 90
        z = kf(fl_, [(0, 1.1), (60, 1.5)], eout)
        ctx.save(); cam(ctx, 560, 1000, z, -3, shake_at(fl_, [0], 8, 14), f)
        bedroom(ctx, mess=1)
        h = draw_hip(ctx, 540, BHIP, KB, 1, BOY, P(rsh=175, rel=-5, lsh=-40, lel=-30, eye='happy', mouth='grin', torso=-3))
        x, y = h['front']
        charger(ctx, x + 10, y - 70, 0.1, 1.2, glow=pop(fl_, 2, 10) + fl_ * 0.02, cable=(-20, 50))
        for i in range(5):
            a = fl_ * 0.07 + i * 1.256
            sparkle(ctx, x + math.cos(a) * 200, y - 70 + math.sin(a) * 160, 24, hx('fff27a'))
        ctx.restore()
        label(ctx, "FOUND IT!", 540, 1420, 130, hx('2fe07a'), -0.03, pop(fl_, 4, 10))
    card(ctx, 'p2', f, 100, 250)


def s3(ctx, f):
    lf = f - 250
    # kid lying on the floor stretched to the outlet, phone dangling on a tiny cable
    lie = P(rot=88, torso=0, lsh=170, lel=-10, rsh=176, rel=-4, lhip=4, lkn=-6, rhip=-4, rkn=-4, eye='closed' if lf > 80 else 'happy',
            mouth='grin' if lf < 80 else 'smile', head=-6)
    # rot -88: character lies along the floor, head towards the outlet (x+)
    def body(ctx):
        h = draw(ctx, 330, 1323, KB * 0.9, 1, BOY, lie)
        return h
    if lf < 70:
        # low-angle wide shot
        z = kf(lf, [(0, 0.95), (70, 1.05)], eout)
        ctx.save(); cam(ctx, 600, 1240, z, 0, shake_at(lf, [10], 10, 16), f)
        bedroom(ctx, mess=1)
        h = body(ctx)
        charger(ctx, OUTX, OUTY + 52, math.pi, 0.8, cable=(0, 0))
        hx_, hy = h['front']
        # cable from outlet to phone
        ctx.move_to(OUTX, OUTY + 10); ctx.line_to(hx_ + 40, hy + 10); setc(ctx, INK); ctx.set_line_width(13); ctx.stroke_preserve()
        setc(ctx, (1, 1, 1)); ctx.set_line_width(7); ctx.stroke()
        phone(ctx, hx_ + 20, hy, 0.75, 2, -1.2, f, charging=True)
        ctx.restore()
        if lf >= 8:
            label(ctx, "CABLE LENGTH:", 540, 760, 72, (1, 1, 1), 0.02, pop(lf, 8, 12))
            label(ctx, "4 INCHES", 540, 870, 110, hx('ffe14d'), -0.03, pop(lf, 16, 20))
        if lf >= 36:
            label(ctx, "WORTH IT.", 540, 1430, 100, hx('2fe07a'), 0.03, pop(lf, 36, 40))
    else:
        # ECU blissful face smushed on the floor next to the charging phone
        il = lf - 70
        z = kf(il, [(0, 1.6), (80, 1.9)], eout)
        ctx.save(); cam(ctx, 640, 1250, z, -6, 0, f)
        bedroom(ctx, mess=1)
        h = body(ctx)
        charger(ctx, OUTX, OUTY + 52, math.pi, 0.8, cable=(0, 0))
        hx_, hy = h['front']
        ctx.move_to(OUTX, OUTY + 10); ctx.line_to(hx_ + 40, hy + 10); setc(ctx, INK); ctx.set_line_width(13); ctx.stroke_preserve()
        setc(ctx, (1, 1, 1)); ctx.set_line_width(7); ctx.stroke()
        phone(ctx, hx_ + 20, hy, 0.75, 2 + il // 40, -1.2, f, charging=True)
        for k in range(3):
            t = ((il * 0.02 + k / 3) % 1)
            sparkle(ctx, 700 + k * 60, 1250 - t * 150, 14 * (1 - t), (1, 1, 1))
        ctx.restore()
        label(ctx, "I LIVE HERE NOW.", 540, 760, 90, (1, 1, 1), -0.02, pop(il, 4, 8))
    card(ctx, 'p3', f, 254, 396)


def mom_scene(ctx, f, lf, z, cx, cy, pct=1, extra=None, web=0.0, mood='happy'):
    kitchen(ctx)
    p = sit(lsh=40, lel=-120, rsh=60, rel=-130, eye=mood, mouth='grin' if mood == 'happy' else 'smile', head=3 * math.sin(lf * 0.12))
    h = draw_hip(ctx, 300, FLOOR - 160, 1.45, 1, MOM, p)
    # chair
    rect_r(ctx, 150, 1350, 260, 34, 10); fl(ctx, hx('8a5a34'), 6)
    ctx.rectangle(170, 1384, 24, 120); fl(ctx, hx('8a5a34'), 5); ctx.rectangle(370, 1384, 24, 120); fl(ctx, hx('8a5a34'), 5)
    table(ctx)
    x, y = h['front']
    mug(ctx, x + 20, y - 30, 0.9, lf)
    phone(ctx, 760, 1180, 0.8, pct, 0.0, f, case=hx('ff8a3d'))
    if web > 0:
        cobweb(ctx, 838, 1088, 0.7 * web, web)
    if extra:
        extra(ctx, h)
    return h


def s4(ctx, f):
    lf = f - 400
    if lf < 70:
        # push on Mom's phone: 1% ... and she is sipping tea, totally calm
        z = kf(lf, [(0, 2.4), (24, 2.4), (50, 1.1)], eout)
        cx = kf(lf, [(0, 760), (24, 760), (50, 600)], eout); cy = kf(lf, [(0, 1170), (24, 1170), (50, 1150)], eout)
        ctx.save(); cam(ctx, cx, cy, z, 0, shake_at(lf, [0], 6, 10), f)
        mom_scene(ctx, f, lf, z, cx, cy)
        ctx.restore()
        if lf < 26:
            label(ctx, "1%", 540, 1430, 150, hx('ff3b5c'), -0.04, pop(lf, 2, 6))
        else:
            label(ctx, "*SIP*", 540, 1430, 110, hx('ffe14d'), 0.04, pop(lf, 40, 44))
    else:
        # split screen: kid (top) horrified, mom (bottom) shrugging
        sl = lf - 70
        ctx.save(); ctx.rectangle(0, 0, W, H / 2); ctx.clip()
        ctx.save(); cam(ctx, 560, 1230, 1.3, 0, shake_at(sl, [0], 8, 12), f)
        bedroom(ctx, mess=1)
        draw_hip(ctx, 540, BHIP, KB, 1, BOY, P(lsh=-40, lel=-20, rsh=40, rel=-20, eye='shock', mouth='scream', head=-6))
        ctx.restore(); ctx.restore()
        ctx.save(); ctx.rectangle(0, H / 2, W, H / 2); ctx.clip()
        ctx.translate(0, H / 2 - 960 / 2 + 60)
        ctx.save(); cam(ctx, 520, 1200, 1.05, 0, 0, f)
        mom_scene(ctx, f, lf, 1, 520, 1100)
        ctx.restore(); ctx.restore()
        ctx.move_to(0, H / 2); ctx.line_to(W, H / 2); ink(ctx, 14); ctx.stroke()
        label(ctx, "MOM, YOUR PHONE!!", 540, 905, 70, hx('ff3b5c'), -0.03, pop(sl, 2, 6))
        if sl >= 18:
            label(ctx, "IT'S FINE.", 600, 1080, 100, hx('ffe14d'), 0.03, pop(sl, 18, 22))
    card(ctx, 'p4', f, 404, 520)


def s5(ctx, f):
    lf = f - 520
    if lf < 72:
        # 3 days later: same calm mom, same 1%, now with a cobweb on the phone
        z = kf(lf, [(0, 1.05), (72, 1.35)], ease)
        ctx.save(); cam(ctx, 640, 1140, z, 0, 0, f)
        def ext(ctx, h):
            if lf > 30:
                x, y = h['head']
                for k in range(3):
                    t = ((lf * 0.02 + k / 3) % 1)
                    ctx.save(); ctx.translate(x + 120 + t * 160, y - 140 - t * 160); ctx.scale(1.0, 1.0)
                    ellipse(ctx, 0, 0, 16, 12, -0.4); fl(ctx, hx('ff3b8a'), 4)
                    ctx.rectangle(12, -60, 6, 60); setc(ctx, INK); ctx.fill(); ctx.restore()
        mom_scene(ctx, f, lf, z, 640, 1140, web=pop(lf, 4, 24), extra=ext)
        ctx.restore()
        label(ctx, "STILL 1%.", 540, 1430, 120, hx('ff3b5c'), -0.03, pop(lf, 6, 10))
    elif lf < 108:
        # kid ECU, twitching eye, jumps up -> his plug pops out
        il = lf - 72
        ctx.save(); cam(ctx, 560, 1014, 2.2, 5, shake_at(il, [24], 12, 22), f)
        bedroom(ctx, mess=1)
        h = draw_hip(ctx, 540, BHIP, KB, 1, BOY, P(lsh=-40, lel=-20, rsh=40, rel=-20, eye='glare' if il < 24 else 'shock', mouth='wavy' if il < 24 else 'scream', head=6))
        x, y = h['head']
        twitch(ctx, x + 150, y - 60, math.sin(il * 1.7))
        ctx.restore()
        label(ctx, "HOW?!", 540, 1450, 150, hx('ffe14d'), 0.04, pop(il, 2, 6))
        if il >= 24:
            label(ctx, "*PLINK*", 540, 1180, 90, (1, 1, 1), -0.05, pop(il, 24, 28))
    else:
        # loop: back to the opening ECU - his own phone is at 1% again
        il = lf - 108
        ctx.save(); cam(ctx, 640, 1000, 2.3, -4, shake_at(il, [0], 12, 18) + 3, f)
        bedroom(ctx)
        panic_kid(ctx, f)
        ctx.restore()
        label(ctx, "NOOOOO!", 540, 1450, 140, hx('ff3b5c'), -0.04, pop(il, 2, 8))
        card(ctx, 'p1', f, 520 + 106)
    if lf < 108:
        card(ctx, 'p5', f, 524, 520 + 106)


def run_pose(ph, **kw):
    s = math.sin(ph)
    d = P(torso=14, lhip=38 * s, lkn=-20 - 45 * max(0, s), rhip=-38 * s, rkn=-20 - 45 * max(0, -s), lsh=-45 * s, lel=70, rsh=45 * s, rel=70)
    d.update(kw); return d


SHOTS = [(0, s1), (96, s2), (250, s3), (400, s4), (520, s5)]


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.25)
    ctx.set_source(g); ctx.paint()
    for c in (96, 186, 250, 320, 400, 470, 520, 592, 628):
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.5 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/v{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/battery_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
