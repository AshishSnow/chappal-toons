"""'My Mom When Guests Arrive' - original characters, doodle style, ~35s loopable."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import (cam, pop, sparkle, puff, label, book, phone, chips, bag, shake_at, room, sofa_back, sofa_front, coffee_table, crumbs, run_pose)

BOY, MOM, AUNTY, UNCLE = doodle.BOY, doodle.MOM, doodle.AUNTY, doodle.UNCLE
N = 1050
STAND = 1500
SEAT = 1235
KB, KM, KG = 1.45, 1.75, 1.6

CAPS = {
    'p1': [[("MY MOM WHEN", OUT)], [("GUESTS ARRIVE", hx('ff3b5c'))]],
    'p2': [[("1 HOUR BEFORE GUESTS:", OUT)], [("WAR MODE", hx('e0123a'))]],
    'p3': [[("THE SPECIAL CUPS", OUT)], [("COME OUT", hx('d99a00'))]],
    'p4': [[("WITH GUESTS:", OUT)], [("SWEETEST MOM EVER", hx('ff3b8a'))]],
    'p5': [[("AFTER GUESTS LEAVE:", OUT)]],
    'p6': [[("DING DONG...", OUT)], [("NOT AGAIN!", hx('ff3b5c'))]],
}


def card(ctx, key, f, appear, gone=10 ** 9):
    u = min(pop(f, appear, appear + 6), 1 - pop(f, gone - 5, gone))
    if u <= 0:
        return
    lines = CAPS[key]; size = 74
    ctx.save()
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    widths = [sum(ctx.text_extents(t).x_advance for t, _ in ln) for ln in lines]
    w = max(widths) + 70; lh = size * 1.18; h = lh * len(lines) + 40
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


_tmp = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4))


def head_of(x, y, k, f, ch, pose):
    h = draw(_tmp, x, y, k, f, ch, pose); return h['head'], h['R']


def sit(**kw):
    p = P(torso=2, lsh=30, lel=-100, rsh=34, rel=-104, lhip=86, lkn=-86, rhip=88, rkn=-88, eye='normal', mouth='smile'); p.update(kw); return p


def walk(ph, **kw):
    p = run_pose(ph, torso=2); p['lhip'] *= 0.6; p['rhip'] *= 0.6; p['lsh'] *= 0.5; p['rsh'] *= 0.5; p.update(kw); return p


# ------------------------------------------------------------------ props
def sock(ctx, x, y, a, col=hx('ff3b8a')):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ctx.new_path(); ctx.move_to(-18, -60); ctx.line_to(18, -60); ctx.line_to(18, 10); ctx.curve_to(18, 30, 60, 26, 60, 44); ctx.curve_to(60, 62, 0, 62, -18, 40); ctx.close_path()
    fl(ctx, col, 5); ctx.rectangle(-18, -60, 36, 14); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.restore()


def cabinet(ctx, open_=0.0, glow=0.0, cups=True):
    ctx.rectangle(40, 520, 300, 730); fl(ctx, hx('8a5a34'), 8)
    ctx.rectangle(64, 545, 252, 560); setc(ctx, hx('5a3a20')); ctx.fill()
    if glow > 0:
        g = cairo.RadialGradient(190, 760, 10, 190, 760, 420); g.add_color_stop_rgba(0, 1, 0.95, 0.6, 0.9 * glow); g.add_color_stop_rgba(1, 1, 0.9, 0.5, 0)
        ctx.rectangle(64, 545, 252, 560); ctx.set_source(g); ctx.fill()
    for yy in (720, 900):
        ctx.rectangle(64, yy, 252, 14); fl(ctx, hx('c98b55'), 3)
    if cups:
        for i in range(3):
            teacup(ctx, 110 + i * 80, 700, 0.6)
        for i in range(3):
            ellipse(ctx, 110 + i * 80, 860, 32, 32); fl(ctx, (1, 1, 1), 4); ellipse(ctx, 110 + i * 80, 860, 18, 18); setc(ctx, hx('3fb6ff')); ctx.fill()
    # glass doors
    for side in (0, 1):
        w_ = 126 * (1 - open_ * 0.8)
        x_ = 64 if side == 0 else 316 - w_
        ctx.rectangle(x_, 545, w_, 560); setc(ctx, (0.8, 0.95, 1, 0.25)); ctx.fill_preserve(); ink(ctx, 6); ctx.stroke()
        if w_ > 30:
            poly(ctx, [(x_ + 12, 560), (x_ + 40, 560), (x_ + 14, 640)]); setc(ctx, (1, 1, 1, 0.6)); ctx.fill()
    ctx.rectangle(64, 1120, 252, 110); fl(ctx, hx('a86c3a'), 6)
    ellipse(ctx, 190, 1175, 12, 12); fl(ctx, hx('ffd23f'), 3)


def teacup(ctx, x, y, s=1.0, steam=False, t=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(32, -10, 16, -1.6, 1.6); ink(ctx, 12); ctx.stroke_preserve(); setc(ctx, hx('ffd23f')); ctx.set_line_width(6); ctx.stroke()
    ctx.new_path(); ctx.move_to(-38, -36); ctx.line_to(38, -36); ctx.curve_to(36, 10, 20, 22, 0, 22); ctx.curve_to(-20, 22, -36, 10, -38, -36); ctx.close_path()
    fl(ctx, (1, 1, 1), 5)
    ctx.rectangle(-36, -24, 72, 9); setc(ctx, hx('ffd23f')); ctx.fill()
    ellipse(ctx, 0, 26, 52, 10); fl(ctx, (1, 1, 1), 4)
    if steam:
        for i in range(3):
            ctx.new_path(); ctx.move_to(-16 + i * 16, -44)
            ctx.curve_to(-26 + i * 16, -70 - 6 * math.sin(t * 0.3 + i), -6 + i * 16, -90, -16 + i * 16, -116)
            setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def tray(ctx, x, y, s=1.0, shine=0.0, t=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 170, 34); fl(ctx, hx('ffcf3d'), 6)
    # teapot
    ctx.new_path(); ctx.move_to(-110, -40); ctx.curve_to(-130, -60, -150, -70, -160, -95); ink(ctx, 16); ctx.stroke_preserve(); setc(ctx, (1, 1, 1)); ctx.set_line_width(9); ctx.stroke()
    ellipse(ctx, -70, -55, 60, 50); fl(ctx, (1, 1, 1), 6)
    ctx.rectangle(-122, -64, 104, 12); setc(ctx, hx('ff3b8a')); ctx.fill()
    ellipse(ctx, -70, -108, 14, 10); fl(ctx, hx('ffd23f'), 4)
    teacup(ctx, 30, -30, 0.7, True, t); teacup(ctx, 110, -30, 0.7, True, t)
    ctx.restore()
    if shine > 0:
        for i, (dx, dy) in enumerate(((-90, -140), (60, -110), (140, -60))):
            sparkle(ctx, x + dx * s, y + dy * s, 40 * s * abs(math.sin(t * 0.25 + i)) * shine, (1, 1, 1))


def doorbell_fx(ctx, f, at, x=760, y=820):
    u = pop(f, at, at + 26)
    if 0 < u < 1:
        ctx.save(); ctx.translate(x, y); ctx.rotate(0.35 * math.sin(f * 1.4) * (1 - u))
        ctx.new_path(); ctx.move_to(-60, 40); ctx.curve_to(-60, -70, 60, -70, 60, 40); ctx.line_to(75, 60); ctx.line_to(-75, 60); ctx.close_path(); fl(ctx, hx('ffd23f'), 7)
        ellipse(ctx, 0, 72, 18, 18); fl(ctx, hx('ffd23f'), 5)
        ctx.restore()
        for i in range(3):
            ctx.new_path(); ctx.arc(x, y, 110 + i * 34 + 30 * u, -0.7, 0.7); setc(ctx, (1, 1, 1, 1 - u)); ctx.set_line_width(9); ctx.stroke()
            ctx.new_path(); ctx.arc(x, y, 110 + i * 34 + 30 * u, math.pi - 0.7, math.pi + 0.7); ctx.stroke()
        label(ctx, "DING DONG!", x - 220, y + 210, 96, hx('ffe14d'), -0.08, pop(f, at, at + 5))


def mess(ctx, items_gone_f, f):
    items = [('chips', 330, 1470, 0.5, 170), ('sock', 600, 1560, -0.4, 182), ('book', 170, 1620, 0.9, 194), ('bag', 900, 1580, 0.2, 206),
             ('sock2', 760, 1450, 0.6, 218), ('crumbs', 0, 0, 0, 230)]
    for kind, x, y, a, gf in items:
        if f < gf:
            if kind == 'chips':
                chips(ctx, x, y, a, 0.8)
            elif kind.startswith('sock'):
                sock(ctx, x, y, a, hx('ff3b8a') if kind == 'sock' else hx('3fb6ff'))
            elif kind == 'book':
                book(ctx, x, y, a)
            elif kind == 'bag':
                bag(ctx, x, y)
            elif kind == 'crumbs':
                crumbs(ctx, 5, 30, 120, 1050, 1420, 1700)


def sofa_bulge(ctx, amt):
    """mess sticking out from under the sofa"""
    if amt <= 0:
        return
    sock(ctx, 200, 1380, 1.2 * amt, hx('ff3b8a')); chips(ctx, 520, 1380, -0.8 * amt, 0.6); sock(ctx, 640, 1385, -1.3 * amt, hx('3fb6ff'))


def glare_aura(ctx, x, y, f, a=1.0):
    rnd = random.Random(f // 2)
    for col, rr in ((hx('ff2d55'), 1.0), (hx('ff9a1f'), 0.8)):
        pts = []
        for i in range(44):
            ang = i * math.pi / 22
            r = 420 * rr * (1.2 if i % 2 == 0 else 0.95) * rnd.uniform(0.9, 1.1)
            pts.append((x + math.cos(ang) * r, y + math.sin(ang) * r * 1.2))
        poly(ctx, pts); setc(ctx, col + (0.55 * a,)); ctx.fill()


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    sweet = f >= 48
    pose = P(lsh=40, lel=-130, rsh=95 if not sweet else 30, rel=-10 if not sweet else -110, lhip=8, rhip=-8,
             eye='glare' if not sweet else 'happy', mouth='scream' if not sweet else 'grin')
    (hxp, hyp), R = head_of(540, STAND - 186 * KM, KM, 1, MOM, pose)
    z = kf(f, [(0, 2.3), (40, 2.45), (48, 2.2), (90, 2.3)])
    ctx.save(); cam(ctx, hxp + 20, hyp + 120, z, -3 if not sweet else 2, shake_at(f, [0, 22], 10, 22) if not sweet else 0, f)
    if not sweet:
        ctx.rectangle(-2000, -2000, 6000, 6000); setc(ctx, hx('d9262f')); ctx.fill()
        glare_aura(ctx, hxp, hyp, f, 0.8)
    else:
        ctx.rectangle(-2000, -2000, 6000, 6000); setc(ctx, hx('ffb3d6')); ctx.fill()
        for i in range(16):
            a = i * math.pi / 8 + f * 0.02
            ctx.move_to(hxp, hyp); ctx.line_to(hxp + math.cos(a) * 3000, hyp + math.sin(a) * 3000); ctx.line_to(hxp + math.cos(a + 0.2) * 3000, hyp + math.sin(a + 0.2) * 3000); ctx.close_path()
        setc(ctx, hx('ffd3e8')); ctx.fill()
    draw(ctx, 540, STAND - 186 * KM, KM, 1, MOM, pose)
    ctx.restore()
    if not sweet:
        if f < 40:
            label(ctx, "CLEAN YOUR ROOM!!", 540, 1480, 92, hx('ffe14d'), -0.05, pop(f, 2, 7))
        doorbell_fx(ctx, f, 36, 800, 1100)
    else:
        rnd = random.Random(4)
        for i in range(7):
            t = ((f + i * 6) % 24) / 24
            sparkle(ctx, rnd.uniform(140, 940), rnd.uniform(600, 1350), 50 * math.sin(t * math.pi), (1, 1, 1))
        label(ctx, "AAIYE AAIYE!", 540, 1480, 110, hx('ff3b8a'), -0.04, pop(f, 50, 55))
    if 46 <= f < 50:
        ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()
    card(ctx, 'p1', f, 2, 90)


def s2(ctx, f):
    lf = f - 90
    stuff = lf >= 70
    z = kf(lf, [(0, 1.0), (60, 1.05), (70, 1.15), (175, 1.15), (190, 1.3)])
    ctx.save(); cam(ctx, 540, kf(lf, [(0, 1150), (70, 1180)]), z, 0, shake_at(lf, [0, 30], 10, 20), f)
    room(ctx, f); sofa_back(ctx)
    # mom (left), pointing / arms crossed
    tap = math.sin(lf * 0.9)
    if lf < 70:
        mp = P(lsh=40, lel=-130, rsh=95, rel=-5 + 6 * tap, lhip=8, rhip=-8, eye='glare', mouth='scream' if lf % 16 < 10 else 'frown', torso=6)
    elif lf < 170:
        mp = P(lsh=40, lel=-135, rsh=35, rel=-138, lhip=8, rhip=-8 + 8 * max(0, tap), rkn=-10 * max(0, tap), eye='glare', mouth='frown')
    else:
        u = pop(lf, 170, 200)
        mp = P(torso=20 * math.sin(u * math.pi), lsh=40, lel=-130, rsh=60, rel=-40, eye='smug' if u < 0.8 else 'normal', mouth='flat' if u < 0.8 else 'smile', lhip=8, rhip=-8)
    sofa_front(ctx, 1.0 if f < 230 else 0)
    coffee_table(ctx)
    mess(ctx, None, f)
    draw(ctx, 170, STAND + 60 - 186 * KM, KM, 1, MOM, mp)
    # boy
    if lf < 30:
        bp = sit(eye='normal', mouth='grin', lsh=58, lel=-80, rsh=62, rel=-86)
        h = draw_hip(ctx, 560, SEAT, KB, 1, BOY, bp)
        hb = h['back']; phone(ctx, hb[0] + 30, hb[1] - 10, -0.1, True)
    elif lf < 70:
        u = pop(lf, 30, 40)
        bp = P(eye='shock', mouth='open', lsh=-160, lel=-20, rsh=-150, rel=-20, sq=-0.1)
        draw(ctx, 600, STAND - 186 * KB - 140 * math.sin(u * math.pi), KB, 1, BOY, bp)
        ph = pop(lf, 30, 50)
        phone(ctx, 640 + 300 * ph, 900 - 400 * math.sin(ph * math.pi) + 500 * ph * ph, ph * 12, False)
    elif lf < 160:
        # stuffing items under the sofa, one every 12 frames
        cyc = (lf - 70) % 12
        x = [330, 600, 170, 900, 760, 500][min(5, (lf - 70) // 12)]
        bx = lerp(x, 420, pop(cyc, 4, 10))
        for j in range(3, 0, -1):
            ctx.push_group(); draw(ctx, bx + j * 40, STAND - 186 * KB, KB, -1, BOY, run_pose(lf * 1.6, eye='shock', mouth='open')); ctx.pop_group_to_source(); ctx.paint_with_alpha(0.12 * (4 - j) / 3)
        draw(ctx, bx, STAND - 186 * KB, KB, -1, BOY, run_pose(lf * 1.6, eye='shock', mouth='open'))
        if cyc >= 9:
            puff(ctx, 420, 1380, pop(cyc, 9, 12), 0.8)
    else:
        jit = math.sin(lf * 3) * 4
        draw(ctx, 680 + jit, STAND - 186 * KB, KB, -1, BOY, P(rsh=-150, rel=-115, lsh=6, lel=-5, eye='shock', mouth='wavy'))
    sofa_bulge(ctx, 0.25 if lf >= 80 else 0)
    ctx.restore()
    if lf < 30:
        label(ctx, "CLEAN THE ROOM!", 540, 1500, 96, hx('ffe14d'), -0.04, pop(lf, 0, 5))
    elif lf < 70:
        label(ctx, "NOW!!!", 540, 1500, 140, hx('ff3b5c'), 0.05, pop(lf, 30, 34))
    elif lf < 160:
        if (lf - 70) % 12 >= 8:
            label(ctx, "STUFF!", 420, 1240, 80, (1, 1, 1), -0.1, 1)
        label(ctx, "SPEED CLEANING...", 540, 1640, 66, hx('8fe9ff'), 0.02, 1)
        hlines(ctx, lf, 0.25, col=INK, y0=1100, y1=1600)
    elif lf < 200:
        label(ctx, "INSPECTION...", 540, 1500, 96, (1, 1, 1), 0.03, pop(lf, 170, 175))
    else:
        label(ctx, "HMM. OKAY.", 540, 1500, 100, hx('5fd07a'), -0.03, pop(lf, 200, 205))
    card(ctx, 'p2', f, 92, 332)


def s3(ctx, f):
    lf = f - 330
    open_ = ease(pop(lf, 20, 34)); glow = pop(lf, 20, 30)
    z = kf(lf, [(0, 1.35), (34, 1.55), (70, 1.55), (78, 1.25)])
    cx = kf(lf, [(0, 300), (70, 300), (78, 480)])
    ctx.save(); cam(ctx, cx, 1000, z, 0, 0, f)
    room(ctx, f); cabinet(ctx, open_, glow, cups=lf < 50)
    sofa_back(ctx); sofa_front(ctx, 0); coffee_table(ctx)
    if lf < 50:
        mp = P(lsh=40, lel=-110, rsh=-80 + 30 * pop(lf, 10, 20), rel=-40, eye='happy' if lf > 20 else 'normal', mouth='grin' if lf > 20 else 'smile', lhip=8, rhip=-8, head=-6)
        h = draw(ctx, 420, STAND - 186 * KM, KM, -1, MOM, mp)
        if lf < 20:
            hx_, hy_ = h['front']
            ctx.new_path(); ctx.arc(hx_ - 10, hy_ - 10, 12, 0, 6.3); ink(ctx, 5); ctx.stroke(); ctx.move_to(hx_ - 22, hy_ - 10); ctx.line_to(hx_ - 50, hy_ - 10); ctx.stroke()
    else:
        u = pop(lf, 50, 80)
        mx = lerp(420, 700, ease(u))
        mp = walk(lf * 0.5, eye='happy', mouth='grin', rsh=95, rel=-90, lsh=95, lel=-90) if u < 1 else P(lsh=95, lel=-90, rsh=95, rel=-90, eye='happy', mouth='grin')
        h = draw(ctx, mx, STAND - 186 * KM, KM, 1, MOM, mp)
        hx_, hy_ = h['front']
        tray(ctx, hx_ + 20, hy_ - 10, 0.9, 1, lf)
    # boy peeking
    if lf >= 60:
        draw(ctx, 900, STAND - 186 * KB, KB, -1, BOY, P(eye='shock', mouth='open', lsh=10, rsh=-10, torso=-6))
    ctx.restore()
    if 20 <= lf < 30:
        label(ctx, "CLICK", 400, 1000, 80, (1, 1, 1), 0.05, 1)
    if 30 <= lf < 70:
        for i in range(6):
            a = i * math.pi / 3 + lf * 0.05
            sparkle(ctx, 300 + math.cos(a) * 260, 950 + math.sin(a) * 300, 40, (1, 1, 1))
        label(ctx, "*ANGELIC MUSIC*", 540, 1480, 80, hx('ffe14d'), -0.03, pop(lf, 30, 36))
    if lf >= 74:
        label(ctx, "WE HAD THESE?!", 540, 1500, 100, hx('8fe9ff'), 0.04, pop(lf, 74, 79))
    card(ctx, 'p3', f, 334, 448)


def s4(ctx, f):
    lf = f - 450
    ctx.save(); cam(ctx, 600, 1050, 1.25, 0, 0, f)
    room(ctx, f); sofa_back(ctx); sofa_front(ctx, 0); coffee_table(ctx)
    tray(ctx, 930, 1360, 0.75, 0.6, f)
    spin = ease(pop(lf, 20, 38))
    mp = P(rot=-360 * spin, lsh=-150 if lf < 20 else 30, lel=-60 if lf < 20 else -110, rsh=-150 if lf < 20 else 120, rel=-60 if lf < 20 else -30,
           eye='shock' if lf < 20 else 'happy', mouth='open' if lf < 20 else 'grin', lhip=8, rhip=-8)
    h = draw(ctx, 520, STAND - 186 * KM, KM, 1, MOM, mp)
    bp = P(eye='shock', mouth='flat', lsh=6, rsh=-6, sq=0.15 * abs(math.sin(lf * 0.5)) if lf >= 40 else 0)
    draw(ctx, 820, STAND - 186 * KB, KB, -1, BOY, bp)
    ctx.restore()
    doorbell_fx(ctx, f, 450, 840, 760)
    if 20 <= lf < 40:
        for i in range(8):
            a = i * math.pi / 4 + lf * 0.3
            sparkle(ctx, 500 + math.cos(a) * 300, 1000 + math.sin(a) * 380, 46, hx('ffd3e8'))
        label(ctx, "MODE SWITCH!", 540, 1500, 100, hx('ff3b8a'), -0.04, pop(lf, 20, 25))
    if lf >= 40 and (lf - 40) % 12 < 7:
        label(ctx, "FIX HAIR, SMILE!", 540, 1520, 80, (1, 1, 1), 0.03, 1)


def s5(ctx, f):
    lf = f - 520
    if lf < 70:      # guests enter
        ctx.save(); cam(ctx, 620, 1100, 1.05, 0, 0, f)
        room(ctx, f, door_open=ease(pop(lf, 0, 12)), hall_light=1)
        sofa_back(ctx); sofa_front(ctx, 0); coffee_table(ctx); tray(ctx, 930, 1360, 0.75, 0.6, f)
        sofa_bulge(ctx, 0.25)
        u = pop(lf, 8, 60)
        draw(ctx, lerp(1250, 820, ease(u)), STAND - 186 * KG, KG, -1, UNCLE, walk(lf * 0.5, eye='normal', mouth='smile') if u < 1 else P(eye='normal', mouth='smile'))
        draw(ctx, lerp(1150, 700, ease(u)), STAND - 186 * KG, KG, -1, AUNTY, walk(lf * 0.5 + 1, eye='happy', mouth='grin') if u < 1 else P(eye='happy', mouth='grin', rsh=120, rel=-30))
        draw(ctx, 330, STAND - 186 * KM, KM, 1, MOM, P(lsh=-140, lel=-30, rsh=120 + 15 * math.sin(lf * 0.6), rel=-20, eye='happy', mouth='grin', lhip=8, rhip=-8))
        draw(ctx, 140, STAND - 186 * KB, KB, 1, BOY, P(eye='normal', mouth='smile', rsh=-140, rel=-60))
        ctx.restore()
        if lf >= 10:
            label(ctx, "NAMASTE JI!", 540, 1500, 100, hx('ff3b8a'), -0.03, pop(lf, 10, 16))
    elif lf < 140:   # sit on sofa -> mess bursts out
        burst = lf >= 104
        ctx.save(); cam(ctx, 470, 1150, 1.2, 0, shake_at(lf, [104], 10, 22), f)
        room(ctx, f); sofa_back(ctx)
        sq = 0.3 * math.exp(-max(0, lf - 100) / 6) if lf >= 100 else 0
        draw_hip(ctx, 280, SEAT - (0 if lf >= 100 else 120 * (1 - pop(lf, 80, 100))), KG, 1, AUNTY, sit(eye='happy', mouth='grin', sq=sq))
        draw_hip(ctx, 600, SEAT, KG, 1, UNCLE, sit(eye='normal', mouth='smile'))
        sofa_front(ctx, 0)
        coffee_table(ctx); tray(ctx, 930, 1360, 0.75, 0, f)
        if not burst:
            sofa_bulge(ctx, 0.25)
        else:
            u = pop(lf, 104, 124)
            items = [('sock', 200, -1.2), ('chips', 360, 0.4), ('book', 480, -0.7), ('sock2', 620, 1.4), ('bag', 760, 0.2)]
            for i, (k_, x, a) in enumerate(items):
                xx = lerp(x, x + (i - 2) * 140, eout(u)); yy = 1380 - math.sin(u * math.pi) * (260 + i * 40) + 180 * u
                if k_.startswith('sock'):
                    sock(ctx, xx, yy, a * (1 + u * 4), hx('ff3b8a') if k_ == 'sock' else hx('3fb6ff'))
                elif k_ == 'chips':
                    chips(ctx, xx, yy, a + u * 6, 0.7)
                elif k_ == 'book':
                    book(ctx, xx, yy, a + u * 5)
                else:
                    bag(ctx, xx, yy + 60)
            puff(ctx, 420, 1390, u, 1.4)
        ctx.restore()
        if burst:
            label(ctx, "POOF!!", 540, 1580, 130, hx('ffe14d'), -0.06, pop(lf, 104, 108))
    elif lf < 190:   # close-up: smile + side-eye glare
        ctx.save()
        pose = P(lsh=40, lel=-130, rsh=35, rel=-136, eye='glare', mouth='grin', lhip=8, rhip=-8, head=-8)
        (hxp, hyp), R = head_of(540, STAND - 186 * KM, KM, 1, MOM, pose)
        cam(ctx, hxp - 40, hyp + 150, kf(lf, [(140, 2.1), (190, 2.35)]), 0, 2, f)
        ctx.rectangle(-2000, -2000, 6000, 6000); setc(ctx, hx('ffb3d6')); ctx.fill()
        ctx.rectangle(hxp - 2000, -2000, 2000 - 20, 6000); setc(ctx, hx('ff8ab5')); ctx.fill()
        draw(ctx, 540, STAND - 186 * KM, KM, 1, MOM, pose)
        ctx.restore()
        label(ctx, "SMILING OUTSIDE...", 540, 1380, 76, hx('ff3b8a'), -0.03, pop(lf, 142, 147))
        label(ctx, "ANGRY INSIDE", 540, 1480, 96, hx('e0123a'), 0.03, pop(lf, 156, 161))
    else:            # aunty asks, boy nervous, uncle slurps
        ctx.save(); cam(ctx, 480, 1120, 1.12, 0, 0, f)
        room(ctx, f); sofa_back(ctx)
        h = draw_hip(ctx, 280, SEAT, KG, 1, AUNTY, sit(eye='normal', mouth='open' if lf % 10 < 5 and lf < 215 else 'smile', rsh=95, rel=-40))
        hu = draw_hip(ctx, 600, SEAT, KG, 1, UNCLE, sit(eye='closed', mouth='open', rsh=60, rel=-120))
        sofa_front(ctx, 0); coffee_table(ctx)
        ux, uy = hu['front']; teacup(ctx, ux + 10, uy - 20, 0.7, True, lf)
        jit = math.sin(lf * 3) * 4
        draw(ctx, 900 + jit, STAND - 186 * KB, KB, -1, BOY, P(eye='shock', mouth='wavy', rsh=-150, rel=-115, lsh=6, lel=-5))
        ctx.restore()
        for i in range(2):
            t = ((lf + i * 8) % 16) / 16
            sweat(ctx, 760 + i * 120, 900 + t * 200, 1.4)
        if lf < 215:
            label(ctx, "BETA, WHICH CLASS?", 540, 1500, 90, hx('8fe9ff'), -0.03, pop(lf, 190, 195))
        else:
            label(ctx, "SLURRRP...", 540, 1500, 100, hx('ffcf6b'), 0.04, pop(lf, 215, 220))
    card(ctx, 'p4', f, 524, 758)


def s6(ctx, f):
    lf = f - 760
    if lf < 60:
        door = 1 - ease(pop(lf, 34, 40))
        ctx.save(); cam(ctx, 620, 1100, 1.05, 0, shake_at(lf, [40], 12, 26), f)
        room(ctx, f, door_open=door, hall_light=door)
        sofa_back(ctx); sofa_front(ctx, 0); coffee_table(ctx)
        u = pop(lf, 0, 34)
        if u < 1:
            draw(ctx, lerp(820, 1300, ease(u)), STAND - 186 * KG, KG, 1, UNCLE, walk(lf * 0.5))
            draw(ctx, lerp(700, 1200, ease(u)), STAND - 186 * KG, KG, 1, AUNTY, walk(lf * 0.5 + 1, eye='happy', mouth='grin'))
        sweet = lf < 44
        mp = P(lsh=40, lel=-130, rsh=-150 + 20 * math.sin(lf * 0.8), rel=-20, eye='happy' if sweet else 'glare', mouth='grin' if sweet else 'frown', lhip=8, rhip=-8)
        if lf >= 44:
            mp = P(lsh=40, lel=-135, rsh=35, rel=-138, eye='glare', mouth='frown', lhip=8, rhip=-8)
        h = draw(ctx, 500, STAND - 186 * KM, KM, 1 if sweet else -1, MOM, mp)
        draw(ctx, 180, STAND - 186 * KB, KB, 1, BOY, P(eye='normal' if sweet else 'shock', mouth='smile' if sweet else 'open', rsh=-150 if sweet else 6, rel=-20, lsh=6))
        ctx.restore()
        if sweet:
            label(ctx, "BYE BYE! COME AGAIN!", 540, 1500, 80, hx('ff3b8a'), -0.03, pop(lf, 2, 7))
        else:
            if lf < 48:
                label(ctx, "SLAM!", 760, 900, 120, (1, 1, 1), 0.1, pop(lf, 40, 43))
            label(ctx, "NOW... YOU.", 540, 1500, 120, hx('ff3b5c'), 0.03, pop(lf, 46, 50))
    else:
        # chase loop across the screen
        u = (lf - 60) / 40.0
        ctx.save(); cam(ctx, 540, 1100, 1.0, 0, 0, f)
        room(ctx, f); sofa_back(ctx); sofa_front(ctx, 0); coffee_table(ctx)
        pass_ = int(u) % 2
        t = u % 1
        dirn = -1 if pass_ == 0 else 1
        bx = lerp(1350, -300, t) if dirn < 0 else lerp(-300, 1350, t)
        draw(ctx, bx, STAND - 186 * KB - abs(math.sin(lf * 0.8)) * 30, KB, dirn, BOY, run_pose(lf * 1.2, eye='shock', mouth='scream'))
        mx = bx - dirn * 360
        hm = draw(ctx, mx, STAND - 186 * KM - abs(math.sin(lf * 0.8 + 1)) * 20, KM, dirn, MOM, run_pose(lf * 1.2, eye='glare', mouth='scream', rsh=-150, rel=-30))
        hx_, hy_ = hm['front']
        slipper(ctx, hx_, hy_ - 90, 0.6 * dirn + 0.4 * math.sin(lf * 0.9), 1.3)
        dust(ctx, bx + dirn * 120, STAND, (lf % 12) / 12, seed=lf // 12, n=4, spread=120, col=hx('f0d6a8'))
        ctx.restore()
        hlines(ctx, lf, 0.3, col=INK, y0=900, y1=1500)
        label(ctx, "RUN!!!", 540, 1600, 130, hx('ffe14d'), -0.05, 1)
    card(ctx, 'p5', f, 762, 898)


def s7(ctx, f):
    lf = f - 900
    ring = lf >= 80
    ctx.save(); cam(ctx, 520, 1120, 1.12 if not ring else kf(lf, [(80, 1.12), (92, 1.4)], eout), 0, 0, f)
    room(ctx, f); sofa_back(ctx)
    if not ring:
        mp = sit(eye='happy', mouth='smile', rsh=60, rel=-120, head=-6)
    else:
        mp = sit(eye='happy', mouth='grin', rsh=120, rel=-30, lsh=-140, lel=-40)
    hm = draw_hip(ctx, 300, SEAT, KM, 1, MOM, mp)
    sofa_front(ctx, 0); coffee_table(ctx)
    if not ring:
        ux, uy = hm['front']; teacup(ctx, ux + 10, uy - 20, 0.7, True, lf)
    # boy washing cups on the floor
    scrub = math.sin(lf * 1.6)
    bp = P(torso=20, head=10, lsh=60 + 10 * scrub, lel=-60, rsh=70 - 10 * scrub, rel=-60, lhip=80, lkn=-150, rhip=82, rkn=-150, eye='closed' if not ring else 'shock',
           mouth='wavy' if not ring else 'scream', sq=0.05)
    draw(ctx, 820, STAND - 186 * KB + 60, KB, -1, BOY, bp)
    ctx.new_path(); ctx.move_to(560, 1480); ctx.line_to(700, 1480); ctx.line_to(680, 1600); ctx.line_to(580, 1600); ctx.close_path(); fl(ctx, hx('3fb6ff'), 6)
    for i in range(6):
        t = ((lf + i * 5) % 30) / 30
        ellipse(ctx, 600 + i * 18, 1470 - t * 120, 12 + 6 * t, 12 + 6 * t); setc(ctx, (1, 1, 1, 0.9 * (1 - t))); ctx.fill_preserve(); setc(ctx, (0.3, 0.6, 1, 1 - t)); ctx.set_line_width(2); ctx.stroke()
    for i in range(4):
        teacup(ctx, 480 - i * 70, 1560 + (i % 2) * 20, 0.55)
    ctx.restore()
    if not ring:
        label(ctx, "PEACE RESTORED", 540, 1640, 80, hx('8fe9ff'), 0.02, pop(lf, 6, 12))
    else:
        doorbell_fx(ctx, f, 980, 820, 760)
        rnd = random.Random(5)
        for i in range(5):
            t = ((lf + i * 6) % 24) / 24
            sparkle(ctx, rnd.uniform(140, 600), rnd.uniform(800, 1200), 46 * math.sin(t * math.pi), (1, 1, 1))
        card(ctx, 'p6', f, 984)


SHOTS = [(0, s1), (90, s2), (330, s3), (450, s4), (520, s5), (760, s6), (900, s7)]


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.28)
    ctx.set_source(g); ctx.paint()
    for c in (90, 330, 450, 520, 590, 660, 710, 760, 820, 900):
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.55 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/z{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/guests_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
