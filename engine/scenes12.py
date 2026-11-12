"""'Me vs My Alarm' - original, general-audience comedy short, ~35s."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import cam, pop, sparkle, puff, label, shake_at, run_pose, book
from scenes7 import bedroom, night
from scenes8 import head_of, walk
from scenes9 import kitchen

BOY, MOM = doodle.BOY, doodle.MOM_G
N = 1050
STAND = 1500
KB, KM = 1.5, 1.75
BED_HIP = (1230, 1215)
ALARM = (690, 1100)

CAPS = {
    'p1': [[("ME VS MY ALARM", OUT)], [("EVERY ", OUT), ("SCHOOL", hx('e0123a')), (" MORNING", OUT)]],
    'p2': [[("JUST ", OUT), ("5 MORE MINUTES", hx('1f8bff')), ("...", OUT)]],
    'p3': [[("10 SECONDS", hx('ff3b5c')), (" TO GET READY", OUT)]],
    'p4': [[("BUT ON WEEKENDS:", OUT)], [("WIDE AWAKE AT ", OUT), ("6 AM", hx('ff8a3d'))]],
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
def alarm_clock(ctx, x, y, s, ringing, f, time_txt="6:00", body=hx('ff3b5c')):
    j = math.sin(f * 2.3) * (8 if ringing else 0)
    ctx.save(); ctx.translate(x + j, y); ctx.rotate(0.08 * math.sin(f * 2.3) if ringing else 0); ctx.scale(s, s)
    for sx in (-1, 1):
        ctx.move_to(sx * 40, 60); ctx.line_to(sx * 55, 95); ink(ctx, 12); ctx.stroke()
        ellipse(ctx, sx * 52, -70, 34, 30, sx * 0.5); fl(ctx, hx('ffd23f'), 6)
    ctx.move_to(-20, -100); ctx.line_to(20, -100); ink(ctx, 12); ctx.stroke()
    ellipse(ctx, 0, 0, 90, 90); fl(ctx, body, 7)
    ellipse(ctx, 0, 0, 72, 72); fl(ctx, (1, 1, 1), 5)
    ctx.rectangle(-58, -22, 116, 50); fl(ctx, hx('1e2a3a'), 4)
    text(ctx, time_txt, 0, 4, 38, hx('6be2ff') if time_txt != "7:45" else hx('ff3b5c'), outline=hx('1e2a3a'), ow=1, shadow=False)
    ctx.restore()
    if ringing:
        for i in range(3):
            r = 120 + i * 30 + 10 * math.sin(f * 1.5)
            for a0 in (-0.6, math.pi - 0.6):
                ctx.new_path(); ctx.arc(x, y, r * s, a0, a0 + 1.2); setc(ctx, (1, 1, 1, 0.9)); ctx.set_line_width(9 * s); ctx.stroke()


def nightstand(ctx):
    ctx.rectangle(560, 1180, 260, 320); fl(ctx, hx('c98b55'), 7)
    ctx.rectangle(585, 1240, 210, 90); fl(ctx, hx('a86c3a'), 5)
    ellipse(ctx, 690, 1285, 12, 8); fl(ctx, hx('ffd23f'), 3)


def blanket(ctx, x0, x1, y, b=0, col=hx('ff8a3d')):
    ctx.new_path(); ctx.move_to(x0, y + 60); ctx.curve_to(x0, y - 90 - b, x1, y - 110 - b, x1, y + 60); ctx.close_path()
    fl(ctx, col, 7)
    for i in range(1, 6):
        xx = lerp(x0, x1, i / 6)
        ellipse(ctx, xx, y - 10 - b * 0.5, 14, 14); setc(ctx, light(col, 0.5)); ctx.fill()


def bed_shot(ctx, f, pose, alarm_ring, time_txt, cover=True, tod=0.15, z=1.05, cx=980, cy=1150, shake=0, b=0, alarm_pos=None, alarm_s=1.0):
    ctx.save(); cam(ctx, cx, cy, z, 0, shake, f)
    bedroom(ctx, f, tod, False, 0, None, 0, 360)
    nightstand(ctx)
    h = draw_hip(ctx, BED_HIP[0], BED_HIP[1] - b, KB, 1, BOY, pose)
    if cover:
        blanket(ctx, 1150, 1560, 1215 - b, b)
    ax, ay = alarm_pos or ALARM
    alarm_clock(ctx, ax, ay, alarm_s, alarm_ring, f, time_txt)
    ctx.restore()
    return h


def lying(**kw):
    p = P(rot=-90, head=-6, lsh=-170, lel=-30, rsh=-60, rel=-80, lhip=4, lkn=-6, rhip=10, rkn=-12, eye='closed', mouth='open')
    p.update(kw); return p


def bathroom(ctx):
    ctx.rectangle(-900, -900, W + 1800, 2200); setc(ctx, hx('dff6ff')); ctx.fill()
    setc(ctx, hx('bfe4f5')); ctx.set_line_width(3)
    for i in range(-10, 20):
        ctx.move_to(i * 90, 0); ctx.line_to(i * 90, 1250)
    for j in range(15):
        ctx.move_to(-900, j * 90); ctx.line_to(W + 900, j * 90)
    ctx.stroke()
    ctx.rectangle(330, 560, 420, 380); fl(ctx, hx('eaf8ff'), 8)
    poly(ctx, [(360, 600), (430, 600), (360, 700)]); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()
    ctx.rectangle(300, 1080, 480, 70); fl(ctx, (1, 1, 1), 7)
    ctx.rectangle(470, 1150, 140, 350); fl(ctx, (1, 1, 1), 7)
    ctx.rectangle(-900, 1250, W + 1800, 1600); setc(ctx, hx('9fd8f0')); ctx.fill()
    ctx.move_to(-900, 1250); ctx.line_to(W + 900, 1250); ink(ctx, 8); ctx.stroke()


def hallway(ctx):
    ctx.rectangle(-900, -900, W + 1800, 2200); setc(ctx, hx('fff1c9')); ctx.fill()
    ctx.rectangle(720, 520, 300, 730); fl(ctx, hx('3f7bff'), 8)
    ellipse(ctx, 760, 900, 14, 14); fl(ctx, hx('ffd23f'), 4)
    ctx.rectangle(120, 700, 220, 160); fl(ctx, hx('9fe0ff'), 7)
    # calendar
    ctx.rectangle(440, 600, 200, 220); fl(ctx, (1, 1, 1), 6)
    ctx.rectangle(440, 600, 200, 60); fl(ctx, hx('ff3b5c'), 6)
    text(ctx, "SAT", 540, 740, 64, INK, outline=INK, ow=1, shadow=False)
    ctx.rectangle(-900, 1250, W + 1800, 1600); setc(ctx, hx('d8b48a')); ctx.fill()
    ctx.move_to(-900, 1250); ctx.line_to(W + 900, 1250); ink(ctx, 8); ctx.stroke()


def toothbrush(ctx, x, y, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ctx.rectangle(-8, -110, 16, 120); fl(ctx, hx('3fb6ff'), 4)
    ctx.rectangle(-12, -140, 24, 34); fl(ctx, (1, 1, 1), 4)
    ctx.restore()


def toast(ctx, x, y, a=0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-45, 40); ctx.line_to(-45, -20); ctx.curve_to(-60, -60, -20, -70, 0, -55); ctx.curve_to(20, -70, 60, -60, 45, -20); ctx.line_to(45, 40); ctx.close_path()
    fl(ctx, hx('d99a5b'), 6)
    ctx.rectangle(-32, -28, 64, 58); setc(ctx, hx('ffe2a8')); ctx.fill()
    ctx.restore()


def backpack(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-60, 80); ctx.line_to(-55, -60); ctx.curve_to(-40, -100, 40, -100, 55, -60); ctx.line_to(60, 80); ctx.close_path(); fl(ctx, hx('5fd07a'), 6)
    ctx.rectangle(-40, 10, 80, 50); fl(ctx, hx('ffd23f'), 4)
    ctx.restore()


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    # ECU on ringing alarm, then the slap
    if f < 40:
        ctx.rectangle(0, 0, W, H); setc(ctx, hx('ffcf3d')); ctx.fill()
        for i in range(18):
            a = i * math.pi / 9 + f * 0.03
            ctx.move_to(540, 1000); ctx.line_to(540 + math.cos(a) * 2000, 1000 + math.sin(a) * 2000); ctx.line_to(540 + math.cos(a + 0.17) * 2000, 1000 + math.sin(a + 0.17) * 2000); ctx.close_path()
        setc(ctx, hx('ffe38a')); ctx.fill()
        ctx.save(); ctx.translate(math.sin(f * 3.1) * 14, math.cos(f * 2.7) * 10)
        alarm_clock(ctx, 540, 1010, 3.2, True, f, "6:00")
        ctx.restore()
        label(ctx, "BRRRRING!!!", 540, 1540, 130, hx('ff3b5c'), -0.06, pop(f, 2, 6))
    else:
        slap = f >= 64
        rp = lying(eye='closed', mouth='wavy' if not slap else 'open', rsh=lerp(-60, -150, pop(f, 52, 64)), rel=lerp(-80, -30, pop(f, 52, 64)))
        bed_shot(ctx, f, rp, not slap, "6:00", z=1.15, cx=960, cy=1150, shake=shake_at(f, [64], 8, 18))
        if slap:
            burst(ctx, 690, 1000, 130 * eout(pop(f, 64, 70)), 12, f // 3)
            label(ctx, "SNOOZE.", 540, 1520, 120, hx('8fe9ff'), 0.04, pop(f, 64, 68))
        else:
            label(ctx, "*STILL ASLEEP*", 540, 1520, 80, (1, 1, 1), 0.03, 1)
    card(ctx, 'p1', f, 2, 90)


ROUNDS = [(90, "6:05", "pillow", "5 MORE MINUTES..."), (160, "6:10", "drawer", "JUST 5 MORE..."), (230, "6:15", "talk", "LAST 5. PROMISE.")]


def s2(ctx, f):
    lf = f - 90
    r = min(2, lf // 70)
    t0, tm, act, txt = ROUNDS[r]
    ll = f - t0
    ring = ll < 30
    if act == 'pillow':
        thr = pop(ll, 26, 34)
        rp = lying(eye='closed', mouth='wavy', rsh=lerp(-60, 60, thr), rel=-40)
        bed_shot(ctx, f, rp, ring, tm, z=1.12, cx=980, cy=1150, shake=shake_at(ll, [34], 8, 14))
        if 26 <= ll < 34:
            ctx.save(); ctx.translate(lerp(1000, 690, thr) * 1.0 - 120, 1180 - math.sin(thr * math.pi) * 250 - 120); ctx.rotate(thr * 4)
            ctx.rectangle(-90, -50, 180, 100); fl(ctx, hx('ff8ab0'), 6); ctx.restore()
        if ll >= 34:
            label(ctx, "BONK!", 400, 1000, 110, hx('ffe14d'), -0.1, pop(ll, 34, 38))
    elif act == 'drawer':
        hide = ll >= 34
        rp = lying(eye='closed', mouth='wavy', rsh=-150 if 26 <= ll < 40 else -60, rel=-30)
        bed_shot(ctx, f, rp, ring and not hide, tm, z=1.12, cx=980, cy=1150, alarm_pos=(690, 1285) if hide else None, alarm_s=0.5 if hide else 1.0)
        if hide:
            label(ctx, "*MUFFLED BRRRING*", 540, 1520, 76, (1, 1, 1), 0.03, 1)
    else:
        rp = lying(eye='closed', mouth='open' if ll % 10 < 5 else 'smile', rsh=-120, rel=-60)
        bed_shot(ctx, f, rp, ring, tm, z=1.3, cx=980, cy=1120)
        if ll >= 30:
            label(ctx, "*NEGOTIATING WITH ALARM*", 540, 1520, 66, (1, 1, 1), 0.03, 1)
    if ring and ll < 22:
        label(ctx, "BRRRING!", 540, 760, 100, hx('ff3b5c'), 0.06, 1)
    if 10 <= ll < 60:
        label(ctx, txt, 540, 1400 if act == 'talk' else 1400, 92, hx('8fe9ff'), -0.03, pop(ll, 10, 14))
    card(ctx, 'p2', f, 94, 298)


def s3(ctx, f):
    lf = f - 300
    rp = lying(eye='closed', mouth='smile')
    bed_shot(ctx, f, rp, False, "6:20", z=1.1, cx=1000, cy=1160)
    for i in range(3):
        t = ((lf + i * 14) % 42) / 42
        label(ctx, "Z", 560 + i * 60, 1000 - t * 260, 60 + i * 16, (1, 1, 1), 0.2, 1)
    u = pop(lf, 6, 18)
    ctx.save(); ctx.translate(540, 820); ctx.scale(max(0.01, eout(u)), max(0.01, eout(u)))
    for bx, by, r in ((250, 360, 28), (200, 290, 42)):
        ellipse(ctx, bx, by, r, r); fl(ctx, (1, 1, 1), 6)
    for dx, dy, r in ((-200, 0, 170), (0, -70, 200), (200, 0, 170), (0, 80, 180)):
        ellipse(ctx, dx, dy, r, r * 0.8)
    setc(ctx, INK); ctx.set_line_width(14); ctx.stroke_preserve(); setc(ctx, hx('eaf4ff')); ctx.fill()
    ph = lf * 0.3
    draw(ctx, -40, 30 - 186 * 0.75, 0.75, 1, BOY, P(eye='happy', mouth='grin', rsh=-150 + 20 * math.sin(ph), rel=-20, lsh=30))
    backpack(ctx, 110, -10, 0.6)
    ctx.restore()
    label(ctx, "DREAM ME: ALREADY READY!", 540, 1500, 72, hx('ffe14d'), -0.03, pop(lf, 20, 26))


def s4(ctx, f):
    lf = f - 420
    if lf < 34:
        ctx.rectangle(0, 0, W, H); setc(ctx, hx('ff3b5c')); ctx.fill()
        for i in range(18):
            a = i * math.pi / 9 + f * 0.05
            ctx.move_to(540, 1000); ctx.line_to(540 + math.cos(a) * 2000, 1000 + math.sin(a) * 2000); ctx.line_to(540 + math.cos(a + 0.17) * 2000, 1000 + math.sin(a + 0.17) * 2000); ctx.close_path()
        setc(ctx, hx('ff6b7d')); ctx.fill()
        z = 3.0 + 0.5 * eout(pop(lf, 0, 10))
        alarm_clock(ctx, 540, 1010, z, False, f, "7:45", body=hx('ffd23f'))
        label(ctx, "7:45?!", 540, 1560, 150, (1, 1, 1), -0.05, pop(lf, 4, 8))
    else:
        up = eout(pop(lf, 34, 44))
        ctx.save(); cam(ctx, 1000, 1100, 1.1, 0, shake_at(lf, [34], 12, 30), f)
        bedroom(ctx, f, 0.1, False, 0, None, 0, 465); nightstand(ctx)
        draw(ctx, 1200, 1215 - 186 * KB * 0.3 - 500 * math.sin(pop(lf, 34, 54) * math.pi), KB, -1, BOY,
             P(rot=-90 * (1 - up), eye='shock', mouth='scream', lsh=-160, rsh=-170, lel=-20, rel=-20, lhip=10, rhip=-10))
        blanket(ctx, 1150, 1560, 1215 + 200 * up, 0)
        alarm_clock(ctx, 690, 1100, 1.0, False, f, "7:45", body=hx('ffd23f'))
        ctx.restore()
        hlines(ctx, lf, 0.4, col=INK, vertical=True)
        label(ctx, "I'M LATE!!!", 540, 1520, 130, hx('ff3b5c'), 0.05, pop(lf, 36, 40))


def s5(ctx, f):
    lf = f - 540
    seg = lf // 60
    ll = lf % 60
    if seg == 0:       # brushing teeth at hyper speed
        ctx.save(); cam(ctx, 540, 1000, 1.3, 0, 3, f)
        bathroom(ctx)
        sc = math.sin(lf * 3)
        h = draw(ctx, 540, STAND - 186 * KB, KB, 1, BOY, P(eye='shock', mouth='open', rsh=-140 + 20 * sc, rel=-100, lsh=20))
        hx_, hy_ = h['front']; toothbrush(ctx, hx_ + 10 * sc, hy_ - 20, -0.6 + 0.3 * sc)
        for i in range(8):
            t = ((lf + i * 3) % 12) / 12
            ellipse(ctx, 560 + i * 18 - 70, 860 - t * 120, 10 + 6 * t, 10 + 6 * t); fl(ctx, (1, 1, 1), 2)
        ctx.restore()
        label(ctx, "BRUSH: 1 SECOND", 540, 1520, 90, hx('8fe9ff'), -0.03, pop(ll, 2, 6))
    elif seg == 1:     # dressing: shirt on backwards, one shoe
        ctx.save(); cam(ctx, 600, 1050, 1.2, 0, 3, f)
        bedroom(ctx, f, 0.3, False, 0, None, 0, 470); nightstand(ctx)
        spin = (ll * 40) % 360 if ll < 30 else 0
        h = draw(ctx, 560, STAND - 186 * KB, KB, 1 if (ll // 4) % 2 == 0 else -1, BOY, P(rot=0, eye='shock', mouth='scream', lsh=-150, rsh=-150, lel=-30, rel=-30, lhip=-10, rhip=40, rkn=-60))
        if ll < 30:
            puff(ctx, 560, 1200, (ll % 10) / 10, 2.0)
        ctx.restore()
        if ll >= 30:
            label(ctx, "SHIRT: BACKWARDS", 540, 1430, 80, hx('ffe14d'), -0.03, pop(ll, 30, 34))
            label(ctx, "SHOES: ONE", 540, 1540, 80, hx('ffe14d'), 0.03, pop(ll, 38, 42))
    elif seg == 2:     # toast + mom
        ctx.save(); cam(ctx, 560, 1080, 1.15, 0, 0, f)
        kitchen(ctx)
        h = draw(ctx, 300, STAND - 186 * KM, KM, 1, MOM, P(eye='happy', mouth='smile', rsh=95, rel=-5, lsh=30, lel=-110))
        hx_, hy_ = h['front']
        grab = ll >= 24
        if not grab:
            toast(ctx, hx_ + 40, hy_ - 20, 0.2, 0.9)
        u = pop(ll, 10, 40)
        bx = lerp(1300, -300, u)
        for j in range(3, 0, -1):
            ctx.push_group(); draw(ctx, bx + j * 60, STAND - 186 * KB, KB, -1, BOY, run_pose(lf * 1.6, eye='shock', mouth='open')); ctx.pop_group_to_source(); ctx.paint_with_alpha(0.12 * (4 - j) / 3)
        hb = draw(ctx, bx, STAND - 186 * KB, KB, -1, BOY, run_pose(lf * 1.6, eye='shock', mouth='open'))
        if grab:
            toast(ctx, hb['head'][0] - 60, hb['head'][1] + 60, -0.3, 0.7)
        ctx.restore()
        hlines(ctx, lf, 0.35, col=INK, y0=900, y1=1500)
        label(ctx, "BREAKFAST: TO GO", 540, 1560, 84, hx('ffe14d'), -0.03, pop(ll, 24, 28))
    else:              # backpack, out the door
        ctx.save(); cam(ctx, 600, 1080, 1.1, 0, 0, f)
        hallway(ctx)
        u = pop(ll, 0, 40)
        bx = lerp(-200, 860, ease(u))
        hb = draw(ctx, bx, STAND - 186 * KB - abs(math.sin(lf * 0.8)) * 30, KB, 1, BOY, run_pose(lf * 1.3, eye='shock', mouth='open'))
        backpack(ctx, bx - 90, hb['head'][1] + 230, 0.9)
        ctx.restore()
        label(ctx, "OUT THE DOOR!", 540, 1540, 100, hx('5fd07a'), 0.03, pop(ll, 6, 10))
    card(ctx, 'p3', f, 544, 778)


def s6(ctx, f):
    lf = f - 780
    ctx.save(); cam(ctx, kf(lf, [(0, 600), (60, 600), (70, 540)], eout), 1080, kf(lf, [(0, 1.1), (60, 1.1), (72, 1.6)], eout), 0, shake_at(lf, [44], 10, 20), f)
    hallway(ctx)
    stop = lf >= 44
    bp = run_pose(lf * 1.3, eye='shock', mouth='open') if not stop else P(eye='shock', mouth='open', lsh=8, rsh=-8, torso=-6)
    bx = lerp(200, 520, ease(pop(lf, 0, 44)))
    hb = draw(ctx, bx, STAND - 186 * KB, KB, 1, BOY, bp)
    backpack(ctx, bx - 90, hb['head'][1] + 230, 0.9)
    mp = P(eye='normal', mouth='open' if lf % 12 < 7 else 'smile', lsh=40, lel=-110, rsh=-150, rel=-30, lhip=8, rhip=-8)
    mx = lerp(1300, 900, ease(pop(lf, 10, 30)))
    draw(ctx, mx, STAND - 186 * KM, KM, -1, MOM, mp)
    ctx.restore()
    if lf >= 30:
        label(ctx, "HONEY...", 540, 1440, 90, (1, 1, 1), -0.03, pop(lf, 30, 34))
        label(ctx, "IT'S SATURDAY.", 540, 1560, 120, hx('ff3b5c'), 0.03, pop(lf, 44, 48))
    if lf >= 90:
        label(ctx, "......", 540, 700, 130, (1, 1, 1), 0, pop(lf, 90, 94))


def s7(ctx, f):
    lf = f - 930
    rp = lying(eye='shock', mouth='flat', head=-14, rsh=-60, rel=-80)
    blink_ = (lf % 30) < 3
    if blink_:
        rp['eye'] = 'closed'
    bed_shot(ctx, f, rp, False, "6:00", tod=2.6, z=kf(lf, [(0, 1.0), (120, 1.35)]), cx=1000, cy=1120)
    night(ctx, 0.5)
    if lf >= 20:
        label(ctx, "*NO ALARM*", 540, 1340, 80, hx('8fe9ff'), 0.03, pop(lf, 20, 24))
    if lf >= 50:
        label(ctx, "WHY AM I AWAKE?!", 540, 1480, 104, hx('ffe14d'), -0.03, pop(lf, 50, 54))
    card(ctx, 'p4', f, 934)


SHOTS = [(0, s1), (90, s2), (300, s3), (420, s4), (540, s5), (780, s6), (930, s7)]


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.28)
    ctx.set_source(g); ctx.paint()
    for c in (40, 90, 160, 230, 300, 420, 454, 540, 600, 660, 720, 780, 930):
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.55 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/d{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/alarm_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
