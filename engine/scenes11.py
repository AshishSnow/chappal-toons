"""'The Perfect Kid Next Door' - original, general-audience comedy short, ~35s."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import cam, pop, sparkle, puff, label, shake_at, room, sofa_back, sofa_front, coffee_table, run_pose, book, phone
from scenes7 import bedroom, chair, desk
from scenes8 import head_of, sit, walk
from scenes9 import kitchen

BOY, MOM, KID, NMOM = doodle.BOY, doodle.MOM_G, doodle.NEIGHBOR, doodle.NMOM
N = 1050
STAND = 1500
SEAT = 1235
KB, KM = 1.5, 1.75

CAPS = {
    'p1': [[("WHEN I FINALLY", OUT)], [("GET A ", OUT), ("B+", hx('1fa84f')), ("...", OUT)]],
    'p2': [[("AND THEN THE", OUT)], [("COMPARISONS ", OUT), ("BEGIN", hx('e0123a'))]],
    'p3': [[("PLOT TWIST:", hx('7a3cff'))], [("HIS MOM COMPARES HIM TO ME", OUT)]],
    'p4': [[("EVERY KID IS SOMEONE'S", OUT)], [("\"PERFECT KID NEXT DOOR\"", hx('ff3b5c'))]],
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
def report(ctx, x, y, a, s, grade, col, glow=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 20, 0, 0, 300); g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.8 * glow); g.add_color_stop_rgba(1, 1, 0.9, 0.4, 0)
        ctx.set_source(g); ellipse(ctx, 0, 0, 300, 300); ctx.fill()
    ctx.rectangle(-110, -140, 220, 280); fl(ctx, (1, 1, 1), 6)
    text(ctx, "REPORT CARD", 0, -105, 22, hx('3f7bff'), outline=INK, ow=0.5, shadow=False)
    for i in range(4):
        ctx.rectangle(-85, -70 + i * 26, 100, 8); setc(ctx, hx('c7cede')); ctx.fill()
    ellipse(ctx, 30, 70, 74, 62); setc(ctx, col); ctx.set_line_width(9); ctx.stroke()
    text(ctx, grade, 30, 72, 60 if len(grade) <= 2 else 44, col, outline=INK, ow=4, shadow=False)
    ctx.restore()


def trophy(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-50, -110); ctx.line_to(50, -110); ctx.curve_to(50, -30, 20, -10, 0, -10); ctx.curve_to(-20, -10, -50, -30, -50, -110); ctx.close_path()
    fl(ctx, hx('ffd23f'), 6)
    for sx in (-1, 1):
        ctx.new_path(); ctx.arc(sx * 55, -80, 22, -1.5 if sx > 0 else 1.6, 1.5 if sx > 0 else 4.7); ink(ctx, 12); ctx.stroke_preserve(); setc(ctx, hx('ffd23f')); ctx.set_line_width(6); ctx.stroke()
    ctx.rectangle(-10, -12, 20, 30); fl(ctx, hx('ffd23f'), 4)
    ctx.rectangle(-40, 16, 80, 22); fl(ctx, hx('a86c3a'), 5)
    poly(ctx, [(-30, -95), (-16, -95), (-28, -45)]); setc(ctx, (1, 1, 1, 0.7)); ctx.fill()
    ctx.restore()


def halo(ctx, h, t=0):
    hx_, hy_ = h['head']; R = h['R']
    ellipse(ctx, hx_, hy_ - R * 1.3 + 6 * math.sin(t * 0.2), R * 0.6, R * 0.15); setc(ctx, hx('ffe14d')); ctx.set_line_width(14); ctx.stroke_preserve()
    setc(ctx, INK); ctx.set_line_width(3); ctx.stroke()


def rain_cloud(ctx, x, y, f):
    for i in range(12):
        t = ((f + i * 4) % 18) / 18
        ctx.move_to(x - 120 + i * 22, y + 50 + t * 300); ctx.line_to(x - 125 + i * 22, y + 80 + t * 300)
    setc(ctx, hx('6bb8ff')); ctx.set_line_width(6); ctx.stroke()
    for dx, dy, r in ((-90, 0, 60), (-20, -30, 80), (70, 0, 65), (0, 25, 70)):
        ellipse(ctx, x + dx, y + dy, r, r * 0.8)
    setc(ctx, INK); ctx.set_line_width(8); ctx.stroke_preserve(); setc(ctx, hx('8a93a8')); ctx.fill()


def spotlight(ctx, x, a=1.0):
    ctx.new_path(); ctx.move_to(x - 70, -100); ctx.line_to(x + 70, -100); ctx.line_to(x + 420, 1600); ctx.line_to(x - 420, 1600); ctx.close_path()
    setc(ctx, (1, 0.97, 0.75, 0.35 * a)); ctx.fill()


def half(ctx, top, cx, cy, z, drawfn):
    y0 = 0 if top else H / 2
    ctx.save(); ctx.rectangle(0, y0, W, H / 2); ctx.clip()
    ctx.translate(W / 2, y0 + H / 4); ctx.scale(z, z); ctx.translate(-cx, -cy)
    drawfn(ctx)
    ctx.restore()


def park(ctx, f):
    ctx.rectangle(-900, -900, W + 1800, 2200); ctx.set_source(vgrad(ctx, 0, 300, 0, 1250, [(0, hx('ff9a5a')), (1, hx('ffd9a0'))])); ctx.fill()
    ellipse(ctx, 800, 1000, 140, 140); setc(ctx, hx('fff27a')); ctx.fill()
    for tx in (150, 950):
        ctx.rectangle(tx - 20, 980, 40, 280); fl(ctx, hx('7a4a2c'), 6)
        ellipse(ctx, tx, 940, 150, 130); fl(ctx, hx('2fbf5a'), 8)
    ctx.rectangle(-900, 1250, W + 1800, 1600); setc(ctx, hx('5fd07a')); ctx.fill()
    ctx.move_to(-900, 1250); ctx.line_to(W + 900, 1250); ink(ctx, 8); ctx.stroke()


def houses_night(ctx, f):
    ctx.rectangle(-900, -900, W + 1800, 4000); ctx.set_source(vgrad(ctx, 0, 0, 0, 1900, [(0, hx('141a46')), (1, hx('3a3f8a'))])); ctx.fill()
    rnd = random.Random(2)
    for _ in range(40):
        ellipse(ctx, rnd.uniform(-200, 1300), rnd.uniform(0, 700), 3, 3); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()
    ellipse(ctx, 540, 260, 70, 70); setc(ctx, hx('fff6d0')); ctx.fill()
    # two houses with a gap
    for x0, col, rc in ((-300, hx('ffb38a'), hx('d9573b')), (600, hx('a8d8ff'), hx('3f7bff'))):
        ctx.rectangle(x0, 640, 780, 1400); fl(ctx, col, 9)
        poly(ctx, [(x0 - 50, 640), (x0 + 390, 380), (x0 + 830, 640)]); fl(ctx, rc, 9)
    ctx.rectangle(470, 1500, 140, 600); setc(ctx, hx('2a2f5a')); ctx.fill()


def window(ctx, x, y, w, h, inner=hx('ffe9a8')):
    ctx.rectangle(x, y, w, h); setc(ctx, inner); ctx.fill()


def window_frame(ctx, x, y, w, h):
    ctx.rectangle(x, y, w, h); ink(ctx, 12); ctx.stroke()
    ctx.rectangle(x - 20, y + h - 6, w + 40, 26); fl(ctx, (1, 1, 1), 6)
    for side in (0, 1):
        poly(ctx, [(x + (0 if side == 0 else w), y), (x + (-70 if side == 0 else w + 70), y + 10), (x + (-70 if side == 0 else w + 70), y + h - 10), (x + (0 if side == 0 else w), y + h)])
        fl(ctx, hx('ffffff'), 6)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 30:
        ctx.rectangle(0, 0, W, H); setc(ctx, hx('5fd07a')); ctx.fill()
        for i in range(18):
            a = i * math.pi / 9 + f * 0.02
            ctx.move_to(540, 1000); ctx.line_to(540 + math.cos(a) * 2000, 1000 + math.sin(a) * 2000); ctx.line_to(540 + math.cos(a + 0.17) * 2000, 1000 + math.sin(a + 0.17) * 2000); ctx.close_path()
        setc(ctx, hx('8ff09a')); ctx.fill()
        report(ctx, 540, 1000, -0.06 + 0.03 * math.sin(f * 0.4), 2.6 + 0.2 * eout(pop(f, 0, 8)), "B+", hx('1fa84f'), glow=1.0)
        for i in range(5):
            sparkle(ctx, 540 + math.cos(i * 1.3 + f * 0.1) * 380, 1000 + math.sin(i * 1.3 + f * 0.1) * 460, 50 * abs(math.sin(f * 0.3 + i)), (1, 1, 1))
    else:
        ctx.save(); cam(ctx, 540, 1080, kf(f, [(30, 1.5), (50, 1.1)], eout), 3 * math.sin(f * 0.25), 0, f)
        room(ctx, f); sofa_back(ctx); sofa_front(ctx); coffee_table(ctx)
        ph = f * 0.5
        pose = P(torso=6 * math.sin(ph), rot=6 * math.sin(ph), lsh=-160, lel=-10, rsh=-60 + 40 * math.sin(ph), rel=-80, lhip=-20 * math.sin(ph), lkn=-30,
                 rhip=20 * math.sin(ph), rkn=-30, eye='happy', mouth='grin', sway=0.7 * math.sin(ph), sq=0.1 * abs(math.sin(ph)))
        h = draw(ctx, 540, STAND - 186 * KB - abs(math.sin(ph)) * 60, KB, 1, BOY, pose)
        bx, by = h['back']
        report(ctx, bx, by - 120, 0.1 * math.sin(ph), 0.8, "B+", hx('1fa84f'))
        ctx.restore()
        rnd = random.Random(1)
        for i in range(24):
            t = pop(f, 30, 70)
            x = 540 + rnd.uniform(-500, 500) * eout(t); y = 700 + rnd.uniform(-300, 100) * eout(t) + 600 * t * t
            ctx.save(); ctx.translate(x, y); ctx.rotate(i + t * 8); ctx.rectangle(-10, -5, 20, 10)
            setc(ctx, [hx('ff3b8a'), hx('ffd23f'), hx('3fb6ff'), hx('5fd07a')][i % 4]); ctx.fill(); ctx.restore()
        label(ctx, "B+!! LET'S GOOO!", 540, 1520, 110, hx('ffe14d'), -0.04, pop(f, 32, 37))
    card(ctx, 'p1', f, 2, 198)


def s2(ctx, f):
    lf = f - 100
    smug = lf >= 40
    ctx.save(); cam(ctx, 560, 1080, kf(lf, [(0, 1.15), (40, 1.15), (52, 1.5)], eout), 0, 0, f)
    room(ctx, f); sofa_back(ctx); sofa_front(ctx); coffee_table(ctx)
    mp = P(lsh=40, lel=-110, rsh=80, rel=-60, eye='normal' if not smug else 'smug', mouth='smile', lhip=8, rhip=-8, head=-6 if not smug else 6)
    h = draw(ctx, 380, STAND - 186 * KM, KM, 1, MOM, mp)
    hx_, hy_ = h['front']
    report(ctx, hx_ + 30, hy_ - 60, 0.15, 0.7, "B+", hx('1fa84f'))
    draw(ctx, 820, STAND - 186 * KB, KB, -1, BOY, P(eye='happy' if not smug else 'shock', mouth='grin' if not smug else 'open', lsh=8, rsh=-8))
    ctx.restore()
    if not smug:
        label(ctx, "THAT'S NICE, HONEY...", 540, 1520, 86, (1, 1, 1), -0.03, pop(lf, 6, 11))
    else:
        label(ctx, "BUT THE KID NEXT DOOR", 540, 1430, 84, hx('ffe14d'), -0.03, pop(lf, 42, 46))
        label(ctx, "GOT AN A+++", 540, 1550, 120, hx('ff3b5c'), 0.03, pop(lf, 52, 56))
    card(ctx, 'p1', f, 2, 198)


def s3(ctx, f):
    lf = f - 200
    ctx.save(); cam(ctx, 620, 1080, 1.05, 0, shake_at(lf, [0, 60, 72, 84], 8, 16), f)
    room(ctx, f, door_open=1, hall_light=1); sofa_back(ctx); sofa_front(ctx); coffee_table(ctx)
    spotlight(ctx, 900, pop(lf, 0, 8))
    u = pop(lf, 4, 40)
    kx = lerp(1250, 880, ease(u)); ky = STAND - 186 * KB - 80 - 20 * math.sin(lf * 0.2)
    h = draw(ctx, kx, ky, KB, -1, KID, P(eye='happy', mouth='smile', lsh=-150, lel=-20, rsh=-160, rel=-20, sway=0))
    halo(ctx, h, lf)
    hx_, hy_ = h['front']
    report(ctx, hx_, hy_ - 100, -0.1, 0.8, "A+++", hx('e0123a'), glow=1.0)
    for i, t0 in enumerate((60, 72, 84, 96)):
        if lf >= t0:
            v = pop(lf, t0, t0 + 8)
            trophy(ctx, 560 + i * 120, lerp(800, 1460, ein(v)), 1.0)
    draw(ctx, 260, STAND - 186 * KB, KB, 1, BOY, P(eye='shock', mouth='scream', lsh=-150, rsh=-160, lel=-30, rel=-30, torso=-10))
    ctx.restore()
    for i in range(6):
        a = i * math.pi / 3 + lf * 0.06
        sparkle(ctx, 880 + math.cos(a) * 300, 1000 + math.sin(a) * 380, 44, (1, 1, 1))
    if lf < 60:
        label(ctx, "*ANGELS SINGING*", 540, 1560, 76, hx('ffe14d'), -0.03, pop(lf, 8, 14))
    else:
        label(ctx, "CLANK! CLANK!", 540, 1560, 100, hx('ffd23f'), 0.04, pop(lf, 60, 64))


PAIRS = [
    ("HE WAKES UP AT 5 AM", "ME:", 'jog', 'sleep'),
    ("HE CLEANS HIS ROOM", "ME:", 'tidy', 'mess'),
    ("HE NEVER TOUCHES HIS PHONE", "ME:", 'read', 'scroll'),
]


def mini(kind, f):
    def fn(ctx):
        if kind == 'jog':
            park(ctx, f)
            draw(ctx, 540, STAND - 186 * KB, KB, 1, KID, run_pose(f * 0.6, eye='happy', mouth='smile'))
        elif kind == 'sleep':
            bedroom(ctx, f, 0.0, False, 0, None, 0, 300)
            draw_hip(ctx, 1230, 1215, KB, 1, BOY, P(rot=-90, head=-6, lsh=-170, lel=-30, rsh=-60, rel=-80, lhip=4, lkn=-6, rhip=10, rkn=-12, eye='closed', mouth='open'))
            for i in range(3):
                t = ((f + i * 12) % 36) / 36
                text(ctx, "Z", 900 + i * 50, 1050 - t * 200, 60 + i * 14, (1, 1, 1), ow=8)
        elif kind == 'tidy':
            bedroom(ctx, f, 0.1, True, 0, None, 0, 300); chair(ctx); desk(ctx, 3)
            hh = draw(ctx, 600, STAND - 186 * KB, KB, -1, KID, P(eye='happy', mouth='smile', rsh=80 + 30 * math.sin(f * 0.8), rel=-40, lsh=10))
            for i in range(4):
                sparkle(ctx, 300 + i * 160, 1150 + 50 * math.sin(f * 0.3 + i), 40 * abs(math.sin(f * 0.25 + i)), (1, 1, 1))
        elif kind == 'mess':
            bedroom(ctx, f, 0.1, True, 0, None, 0, 300); chair(ctx); desk(ctx, 3)
            from scenes10 import messy_floor
            messy_floor(ctx, 1.0)
            for i, (x, y) in enumerate(((200, 1420), (700, 1450), (900, 1380))):
                ctx.save(); ctx.translate(x, y); ctx.rotate(i); ctx.rectangle(-60, -40, 120, 80); fl(ctx, [hx('ff8a3d'), hx('b06bff'), hx('5fd07a')][i], 5); ctx.restore()
            draw_hip(ctx, 420, SEAT, KB, 1, BOY, sit(eye='normal', mouth='grin', lsh=58, lel=-80, rsh=62, rel=-86))
        elif kind == 'read':
            bedroom(ctx, f, 0.1, True, 0, None, 0, 300); chair(ctx)
            hh = draw_hip(ctx, 420, SEAT, KB, 1, KID, sit(eye='happy', mouth='smile', lsh=70, lel=-90, rsh=72, rel=-94))
            desk(ctx, 3)
            bx, by = hh['front']; book(ctx, bx + 20, by - 40, -0.2, 1.4, hx('3f8bff'))
            halo(ctx, hh, f)
        elif kind == 'scroll':
            room(ctx, f); sofa_back(ctx)
            hh = draw_hip(ctx, 420, SEAT, KB, 1, BOY, sit(eye='happy', mouth='grin' if f % 20 < 10 else 'open', torso=-18, lsh=58, lel=-80, rsh=62, rel=-86, lhip=70, lkn=-20, rhip=74, rkn=-20))
            sofa_front(ctx)
            bx, by = hh['back']; phone(ctx, bx + 30, by - 10, -0.1, True)
    return fn


def s4(ctx, f):
    lf = f - 330
    i = min(2, lf // 90)
    ll = lf - i * 90
    top_t, bot_t, tk, bk = PAIRS[i]
    sl = eout(pop(ll, 0, 8))
    ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.save(); ctx.translate(-W * (1 - sl), 0)
    half(ctx, True, 560, 1230, 0.74, mini(tk, f))
    ctx.restore()
    ctx.save(); ctx.translate(W * (1 - eout(pop(ll, 6, 14))), 0)
    half(ctx, False, 560, 1230, 0.74, mini(bk, f))
    ctx.restore()
    ctx.rectangle(0, H / 2 - 8, W, 16); fl(ctx, (1, 1, 1), 5)
    ellipse(ctx, W / 2, H / 2, 70, 70); fl(ctx, hx('ff3b5c'), 7)
    text(ctx, "VS", W / 2, H / 2, 60, (1, 1, 1), ow=6, shadow=False)
    label(ctx, top_t, 540, 870, 64, hx('ffe14d'), -0.03, pop(ll, 8, 13))
    label(ctx, bot_t + (" ZZZ..." if bk == 'sleep' else (" OOPS." if bk == 'mess' else " LOL")), 540, 1440, 76, hx('8fe9ff'), 0.03, pop(ll, 20, 25))
    card(ctx, 'p2', f, 332, 366)
    if lf < 34:
        ctx.rectangle(0, 0, W, H); setc(ctx, (0, 0, 0, 0.0)); ctx.fill()


def s5(ctx, f):
    lf = f - 600
    ctx.save(); cam(ctx, 300, 1100, 1.3, 0, 0, f)
    room(ctx, f); sofa_back(ctx); sofa_front(ctx)
    ctx.rectangle(-900, -900, W + 1800, 4000); setc(ctx, (0.3, 0.35, 0.5, 0.35)); ctx.fill()
    hh = draw(ctx, 240, STAND - 186 * KB + 60, KB, 1, BOY, P(torso=20, head=24, lsh=60, lel=-120, rsh=64, rel=-124, lhip=80, lkn=-150, rhip=82, rkn=-150, eye='closed', mouth='wavy'))
    rain_cloud(ctx, hh['head'][0], hh['head'][1] - hh['R'] * 2.0, f)
    ctx.restore()
    label(ctx, "ME AFTER EVERY", 540, 1430, 90, (1, 1, 1), -0.03, pop(lf, 6, 11))
    label(ctx, "REPORT CARD", 540, 1540, 110, hx('8fe9ff'), 0.03, pop(lf, 12, 17))


WL = (110, 1000, 360, 420)   # boy's window (left house)
WR = (610, 1000, 360, 420)   # neighbor's window (right house)


def windows(ctx, f, lf, boy_pose, kid_pose, nmom=False, fist=0.0):
    houses_night(ctx, f)
    for (x, y, w, h), who, pose, fc in ((WL, BOY, boy_pose, 1), (WR, KID, kid_pose, -1)):
        window(ctx, x, y, w, h)
        ctx.save(); ctx.rectangle(x - (0 if fist <= 0 else 400), y - 400, w + (0 if fist <= 0 else 800), h + 400); ctx.clip()
        cxw = x + w / 2 + fc * 150 * fist
        if who is KID and nmom:
            u = pop(lf, 10, 22)
            draw(ctx, x + w / 2 - 90, y + h + 90 - 186 * 1.3 + 300 * (1 - eout(u)), 1.3, -1, NMOM, P(eye='glare', mouth='scream' if lf % 14 < 9 else 'frown', lsh=40, lel=-120, rsh=95, rel=-10))
        draw(ctx, cxw, y + h + 60 - 186 * 1.3, 1.3, fc, who, pose)
        ctx.restore()
        window_frame(ctx, x, y, w, h)


def s6(ctx, f):
    lf = f - 720
    ctx.save(); cam(ctx, 540, 1180, 1.0, 0, 0, f)
    bp = P(eye='closed' if lf < 60 else 'shock', mouth='wavy' if lf < 60 else 'open', lsh=40, lel=-120, rsh=35, rel=-120, head=10 if lf < 60 else -6)
    kp = P(eye='normal' if lf < 20 else 'closed', mouth='smile' if lf < 20 else 'wavy', lsh=10, rsh=-10, head=0 if lf < 20 else 12)
    windows(ctx, f, lf, bp, kp, nmom=True)
    ctx.restore()
    if lf >= 14:
        label(ctx, "WHY CAN'T YOU BE CHILL", 540, 1560, 74, hx('ffe14d'), -0.03, pop(lf, 14, 18))
        label(ctx, "LIKE THE KID NEXT DOOR?!", 540, 1660, 74, hx('ff3b5c'), 0.03, pop(lf, 24, 28))
    if lf >= 70:
        label(ctx, "WAIT... WHAT?!", 300, 900, 80, hx('8fe9ff'), -0.08, pop(lf, 70, 74))
    card(ctx, 'p3', f, 724, 900)


def s7(ctx, f):
    lf = f - 900
    lean = ease(pop(lf, 26, 46))
    ctx.save(); cam(ctx, 540, 1180, kf(lf, [(0, 1.0), (46, 1.3)], eout), 0, shake_at(lf, [46], 8, 14), f)
    bp = P(eye='happy' if lf > 46 else 'normal', mouth='grin' if lf > 46 else 'smile', lsh=40, lel=-120, rsh=lerp(35, 95, lean), rel=lerp(-120, 0, lean), torso=10 * lean)
    kp = P(eye='happy' if lf > 46 else 'normal', mouth='grin' if lf > 46 else 'smile', lsh=10, rsh=lerp(-10, 95, lean), rel=lerp(-10, 0, lean), torso=10 * lean)
    windows(ctx, f, lf, bp, kp, nmom=False, fist=lean * 0.55)
    ctx.restore()
    if lf < 26:
        label(ctx, "*NOD*", 540, 900, 90, (1, 1, 1), 0, pop(lf, 4, 8))
    if lf >= 46:
        burst(ctx, 540, 1250, 120 * eout(pop(lf, 46, 52)), 12, lf // 3)
        label(ctx, "BROTHERS IN PAIN", 540, 1600, 100, hx('ffe14d'), -0.03, pop(lf, 50, 55))
    card(ctx, 'p4', f, 1000)


SHOTS = [(0, s1), (100, s2), (200, s3), (330, s4), (600, s5), (720, s6), (900, s7)]


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.28)
    ctx.set_source(g); ctx.paint()
    for c in (30, 100, 200, 330, 600, 720, 900):
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.55 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/c{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/kid_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
