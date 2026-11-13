"""'Waiting For Food Delivery' - original, general-audience comedy short, ~22s.
Dad + kid faces pressed to the window: "2 MIN AWAY!". The driver's map: the scooter turns away and circles the block.
30 min later Dad finally goes to the bathroom -> DING DONG the very second the door shuts. He sprints out with
toilet paper on his shoe - nobody there, just a "SORRY WE MISSED YOU" note, and the neighbour across the street
is happily eating his fries. Dad re-orders and refuses to move -> "45 MIN". Loop back to the window faces."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import cam, pop, sparkle, puff, label, shake_at
import scenes13
from scenes13 import card as _card13

BOY, DAD, NEIGH = doodle.BOY, doodle.DAD, doodle.NEIGHBOR
N = 660
FLOOR = 1500
KB, KD = 1.5, 1.75
BHIP, DHIP = FLOOR - 92 * KB, FLOOR - 92 * KD
DOOR0, DOOR1, DOORT = 700, 960, 830          # front door (hallway)
BATH0, BATH1 = 60, 300                       # bathroom door (hallway)

CAPS = {
    'p1': [[("WAITING FOR", OUT)], [("FOOD ", hx('ff8a1f')), ("DELIVERY", OUT)]],
    'p2': [[("THE DRIVER'S ", OUT), ("MAP", hx('1f8bff')), (":", OUT)]],
    'p3': [[("30 MIN LATER: ", OUT)], [("\"BRB, ", OUT), ("BATHROOM", hx('8a3cff')), ("\"", OUT)]],
    'p4': [[("WHERE IS ", OUT), ("MY FOOD", hx('ff3b5c')), ("?!", OUT)]],
    'p5': [[("ORDER ", OUT), ("AGAIN", hx('2fbf5a')), (". DON'T MOVE.", OUT)]],
}
scenes13.CAPS = CAPS
card = _card13

WALL, WALL2 = hx('8fd3c8'), hx('7cc4b8')
DOORC = hx('e0623a')


def rect_r(ctx, x, y, w, h, r):
    ctx.new_path(); ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); ctx.close_path()


def rays(ctx, x, y, r0, r1, t, col=(1, 0.97, 0.6), a=0.8, n=12):
    for k in range(n):
        ang = k * 2 * math.pi / n + t
        ctx.move_to(x + math.cos(ang) * r0, y + math.sin(ang) * r0)
        ctx.line_to(x + math.cos(ang - 0.09) * r1, y + math.sin(ang - 0.09) * r1)
        ctx.line_to(x + math.cos(ang + 0.09) * r1, y + math.sin(ang + 0.09) * r1); ctx.close_path()
    setc(ctx, col + (a,)); ctx.fill()


# ------------------------------------------------------------------ props
def phone(ctx, x, y, a=0.0, s=1.0, txt="2 MIN", col=hx('2fbf5a')):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -40, -80, 80, 160, 16); fl(ctx, hx('2a2a3a'), 6)
    rect_r(ctx, -31, -68, 62, 136, 8); setc(ctx, hx('fff8e8')); ctx.fill()
    rect_r(ctx, -31, -68, 62, 40, 8); setc(ctx, col); ctx.fill()
    text(ctx, txt, 0, -48, 15, (1, 1, 1), outline=col, ow=1, shadow=False)
    ellipse(ctx, 0, 14, 12, 12); setc(ctx, hx('ff3b5c')); ctx.fill()
    ctx.restore()


def fork(ctx, x, y, a=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -9, -10, 18, 90, 8); fl(ctx, hx('d8dde8'), 5)
    rect_r(ctx, -22, -50, 44, 44, 10); fl(ctx, hx('d8dde8'), 5)
    for dx in (-15, -5, 5, 15):
        ctx.move_to(dx, -50); ctx.line_to(dx, -90)
    ink(ctx, 8); ctx.stroke()
    for dx in (-15, -5, 5, 15):
        ctx.move_to(dx, -50); ctx.line_to(dx, -88)
    setc(ctx, hx('d8dde8')); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()


def food_bag(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-80, -110), (80, -110), (92, 100), (-92, 100)]); fl(ctx, hx('c98f5a'), 6)
    poly(ctx, [(-80, -110), (80, -110), (70, -80), (-70, -80)]); setc(ctx, hx('a8703c')); ctx.fill()
    # burger doodle
    ctx.new_path(); ctx.arc(0, 0, 44, math.pi, 2 * math.pi); ctx.close_path(); fl(ctx, hx('f2b45a'), 5)
    rect_r(ctx, -48, 2, 96, 14, 6); fl(ctx, hx('6b3a1e'), 5)
    rect_r(ctx, -44, 18, 88, 16, 8); fl(ctx, hx('f2b45a'), 5)
    for k in range(4):
        rect_r(ctx, -60 + k * 34, -150 - 14 * (k % 2), 14, 50, 6); fl(ctx, hx('ffd23f'), 4)
    ctx.restore()


def fry(ctx, x, y, a=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -8, -40, 16, 80, 6); fl(ctx, hx('ffd23f'), 4)
    ctx.restore()


def note(ctx, x, y, s=1.0, a=0.0, full=True):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -150, -100, 300, 200, 8); fl(ctx, hx('fff27a'), 6)
    if full:
        text(ctx, "SORRY", 0, -48, 46, INK, outline=INK, ow=1, shadow=False)
        text(ctx, "WE MISSED", 0, 6, 46, INK, outline=INK, ow=1, shadow=False)
        text(ctx, "YOU!", 0, 60, 46, hx('ff3b5c'), outline=hx('ff3b5c'), ow=1, shadow=False)
    ctx.restore()


def toilet_paper(ctx, x0, y0, x1, y1, t):
    """streamer from shoe (x0,y0) trailing back to (x1,y1)"""
    ctx.new_path(); ctx.move_to(x0, y0)
    for k in range(1, 9):
        u = k / 8
        ctx.line_to(lerp(x0, x1, u), lerp(y0, y1, u) + 26 * math.sin(u * 8 + t * 0.9) * u)
    setc(ctx, INK); ctx.set_line_width(38); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke_preserve()
    setc(ctx, (1, 1, 1)); ctx.set_line_width(28); ctx.stroke()


def wall_clock(ctx, x, y, r, t):
    ellipse(ctx, x, y, r, r); fl(ctx, (1, 1, 1), 7)
    for k in range(12):
        a = k * math.pi / 6
        ctx.move_to(x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8); ctx.line_to(x + math.cos(a) * r * 0.9, y + math.sin(a) * r * 0.9)
    ink(ctx, 4); ctx.stroke()
    for ang, ln, w in ((t, 0.75, 6), (t / 12, 0.5, 9)):
        ctx.move_to(x, y); ctx.line_to(x + math.sin(ang) * r * ln, y - math.cos(ang) * r * ln); ink(ctx, w); ctx.stroke()
    ellipse(ctx, x, y, 7, 7); setc(ctx, hx('ff3b5c')); ctx.fill()


# ------------------------------------------------------------------ sets
def hallway(ctx, door_open=0.0, bath_open=0.0, bath_shake=0.0, door_shake=0.0, f=0, clock_t=None):
    ctx.rectangle(-1500, -1500, 4200, 4200); setc(ctx, WALL); ctx.fill()
    for i in range(-12, 22):
        ctx.rectangle(i * 110, -400, 50, FLOOR + 400); setc(ctx, WALL2); ctx.fill()
    # skirting
    ctx.rectangle(-1500, FLOOR - 40, 4200, 40); fl(ctx, (1, 1, 1), 6)
    # bathroom door (left)
    ctx.save()
    if bath_shake:
        ctx.translate(math.sin(f * 2.3) * 8 * bath_shake, 0)
    rect_r(ctx, BATH0 - 24, DOORT - 24, BATH1 - BATH0 + 48, FLOOR - DOORT + 24, 10); fl(ctx, (1, 1, 1), 7)
    ctx.rectangle(BATH0, DOORT, BATH1 - BATH0, FLOOR - DOORT); setc(ctx, hx('2a2340')); ctx.fill()
    if bath_open < 1:
        w = (BATH1 - BATH0) * (1 - bath_open)
        ctx.rectangle(BATH0, DOORT, w, FLOOR - DOORT); fl(ctx, hx('ffb6d0'), 7)
        if w > 80:
            ellipse(ctx, BATH0 + w - 40, 1180, 16, 16); fl(ctx, hx('ffd23f'), 5)
            # little sign
            rect_r(ctx, BATH0 + w / 2 - 50, 900, 100, 70, 10); fl(ctx, (1, 1, 1), 5)
            ellipse(ctx, BATH0 + w / 2 - 18, 922, 9, 9); setc(ctx, INK); ctx.fill()
            ellipse(ctx, BATH0 + w / 2 + 18, 922, 9, 9); setc(ctx, INK); ctx.fill()
            ctx.rectangle(BATH0 + w / 2 - 26, 936, 16, 24); ctx.rectangle(BATH0 + w / 2 + 10, 936, 16, 24); ctx.fill()
    ctx.restore()
    # clock between doors
    wall_clock(ctx, 500, 760, 80, clock_t if clock_t is not None else 1.0)
    # coat hooks
    ctx.rectangle(400, 960, 200, 20); fl(ctx, hx('8a5a34'), 5)
    for hx_ in (440, 560):
        ellipse(ctx, hx_, 990, 10, 10); setc(ctx, INK); ctx.fill()
    poly(ctx, [(425, 990), (455, 990), (480, 1150), (400, 1150)]); fl(ctx, hx('ffcc1f'), 6)
    # front door (right)
    ctx.save()
    if door_shake:
        ctx.translate(math.sin(f * 2.9) * 10 * door_shake, 0)
    rect_r(ctx, DOOR0 - 24, DOORT - 24, DOOR1 - DOOR0 + 48, FLOOR - DOORT + 24, 10); fl(ctx, (1, 1, 1), 7)
    ctx.rectangle(DOOR0, DOORT, DOOR1 - DOOR0, FLOOR - DOORT); setc(ctx, hx('fff2b0')); ctx.fill()
    if door_open < 1:
        w = (DOOR1 - DOOR0) * (1 - door_open)
        ctx.rectangle(DOOR1 - w, DOORT, w, FLOOR - DOORT); fl(ctx, DOORC, 7)
        if w > 100:
            rect_r(ctx, DOOR1 - w + 40, DOORT + 40, w - 80, 170, 10); fl(ctx, hx('bfeaff'), 5)
            rect_r(ctx, DOOR1 - w + 40, DOORT + 260, w - 80, 300, 10); fl(ctx, dark(DOORC, 0.85), 5)
            ellipse(ctx, DOOR1 - w + 34, 1190, 16, 16); fl(ctx, hx('ffd23f'), 5)
    ctx.restore()
    # floor
    ctx.rectangle(-1500, FLOOR, 4200, 900); setc(ctx, hx('c98f5a')); ctx.fill()
    for i in range(-14, 26):
        ctx.move_to(i * 140, FLOOR); ctx.line_to(i * 140 - 60, FLOOR + 900); setc(ctx, (0, 0, 0, 0.1)); ctx.set_line_width(5); ctx.stroke()
    rect_r(ctx, DOOR0 - 10, FLOOR + 14, DOOR1 - DOOR0 + 20, 50, 14); fl(ctx, hx('5a7bd6'), 6)
    ctx.move_to(-1500, FLOOR); ctx.line_to(2700, FLOOR); ink(ctx, 8); ctx.stroke()


def window_shot(ctx, f, lf, eta="2 MIN"):
    """opening / loop: seen from OUTSIDE - Dad + kid faces squashed against the window"""
    ctx.save(); cam(ctx, 540, 1060, 1.0 + 0.02 * math.sin(lf * 0.2), -2 + 1.5 * math.sin(lf * 0.25), shake_at(lf, [0], 10, 14), f)
    # dim interior
    ctx.rectangle(-500, -500, 2100, 2900); setc(ctx, hx('5aa89c')); ctx.fill()
    bounce = 8 * math.sin(lf * 0.9)
    h = draw_hip(ctx, 390, 1560 + bounce, 2.6, 1, DAD, P(rsh=20, rel=-20, lsh=20, lel=-40, eye='shock', mouth='open', head=-4, torso=3))
    b = draw_hip(ctx, 770, 1640 - bounce, 2.0, -1, BOY, P(rsh=20, rel=-20, lsh=150, lel=-40, eye='shock', mouth='grin', head=6, torso=-3))
    fx, fy = h['head'][0] - 150, h['head'][1] + 300
    phone(ctx, fx, fy, -0.15 + 0.05 * math.sin(lf * 0.8), 2.0, eta)
    fork(ctx, b['back'][0], b['back'][1] - 30, -0.3 + 0.1 * math.sin(lf * 1.1), 1.4)
    # breath fog
    for (cx, cy), r in ((h['head'], 1.0), (b['head'], 0.75)):
        ellipse(ctx, cx + 20, cy + 140 * r, 90 * r * (0.85 + 0.15 * math.sin(lf * 0.5)), 50 * r); setc(ctx, (1, 1, 1, 0.35)); ctx.fill()
    # glass + exterior wall with a window hole
    ctx.rectangle(110, 560, 860, 760); setc(ctx, (0.85, 0.97, 1, 0.12)); ctx.fill()
    for k in range(2):
        poly(ctx, [(200 + k * 120, 560), (260 + k * 120, 560), (140 + k * 120, 1320), (110 + k * 120 - 30 * k, 1320)])
        setc(ctx, (1, 1, 1, 0.22)); ctx.fill()
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    ctx.rectangle(-500, -500, 2100, 2900); ctx.rectangle(110, 560, 860, 760)
    setc(ctx, hx('ffd88a')); ctx.fill()
    ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    for i in range(-6, 30):
        y = i * 70
        if 560 < y < 1320:
            ctx.move_to(-500, y); ctx.line_to(110, y); ctx.move_to(970, y); ctx.line_to(1600, y)
        else:
            ctx.move_to(-500, y); ctx.line_to(1600, y)
    setc(ctx, (0.6, 0.4, 0.1, 0.25)); ctx.set_line_width(4); ctx.stroke()
    rect_r(ctx, 90, 540, 900, 800, 16); ink(ctx, 26); ctx.stroke()
    rect_r(ctx, 90, 540, 900, 800, 16); setc(ctx, (1, 1, 1)); ctx.set_line_width(16); ctx.stroke()
    ctx.move_to(540, 548); ctx.line_to(540, 1332); ink(ctx, 26); ctx.stroke()
    ctx.move_to(540, 548); ctx.line_to(540, 1332); setc(ctx, (1, 1, 1)); ctx.set_line_width(16); ctx.stroke()
    rect_r(ctx, 60, 1330, 960, 50, 12); fl(ctx, (1, 1, 1), 7)
    # flower box
    rect_r(ctx, 120, 1380, 840, 110, 14); fl(ctx, hx('c9782a'), 7)
    for k in range(7):
        x = 170 + k * 125
        ctx.move_to(x, 1390); ctx.line_to(x, 1340); setc(ctx, hx('2fbf5a')); ctx.set_line_width(8); ctx.stroke()
        for j in range(5):
            a = j * 2 * math.pi / 5 + k
            ellipse(ctx, x + math.cos(a) * 18, 1330 + math.sin(a) * 18, 14, 14); fl(ctx, (hx('ff6f9a'), hx('ffcc1f'), hx('8a3cff'))[k % 3], 3)
        ellipse(ctx, x, 1330, 10, 10); setc(ctx, hx('fff2de')); ctx.fill()
    ctx.restore()


def street(ctx, f, door_open=1.0):
    """exterior: our porch on the left, neighbour's porch across on the right (wide world)"""
    ctx.rectangle(-1500, -1500, 5000, 4200); setc(ctx, hx('8fdcff')); ctx.fill()
    for cx, cy in ((300, 520), (1500, 460), (2300, 560)):
        for dx, r in ((-60, 50), (0, 70), (60, 50)):
            ellipse(ctx, cx + dx, cy, r, r * 0.8); setc(ctx, (1, 1, 1)); ctx.fill()
    # our house
    ctx.rectangle(-600, 700, 1300, FLOOR - 700); fl(ctx, hx('ffd88a'), 8)
    poly(ctx, [(-700, 720), (50, 330), (800, 720)]); fl(ctx, hx('ff6f4a'), 8)
    ctx.rectangle(180, DOORT, 260, FLOOR - DOORT); setc(ctx, hx('5aa89c')); ctx.fill()
    if door_open < 1:
        ctx.rectangle(180, DOORT, 260 * (1 - door_open), FLOOR - DOORT); fl(ctx, DOORC, 7)
    else:
        poly(ctx, [(180, DOORT), (120, DOORT - 20), (120, FLOOR + 30), (180, FLOOR)]); fl(ctx, DOORC, 7)
    ctx.rectangle(180, DOORT, 260, FLOOR - DOORT); ink(ctx, 8); ctx.stroke()
    # street
    ctx.rectangle(-1500, FLOOR, 5000, 900); setc(ctx, hx('b8bcc8')); ctx.fill()
    ctx.rectangle(-1500, FLOOR + 140, 5000, 300); setc(ctx, hx('5a5d6a')); ctx.fill()
    for i in range(-10, 30):
        ctx.rectangle(i * 200, FLOOR + 280, 100, 20); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.move_to(-1500, FLOOR); ctx.line_to(3500, FLOOR); ink(ctx, 8); ctx.stroke()
    rect_r(ctx, 160, FLOOR - 4, 300, 36, 12); fl(ctx, hx('5a7bd6'), 6)
    # neighbour house (across, far right)
    ctx.rectangle(1500, 700, 1400, FLOOR - 700); fl(ctx, hx('c9b8ff'), 8)
    poly(ctx, [(1400, 720), (2200, 330), (3000, 720)]); fl(ctx, hx('4a74c9'), 8)
    ctx.rectangle(2060, DOORT, 260, FLOOR - DOORT); fl(ctx, hx('2fbf5a'), 7)
    rect_r(ctx, 1680, 900, 260, 240, 12); fl(ctx, hx('bfeaff'), 7)
    rect_r(ctx, 2040, FLOOR - 4, 300, 36, 12); fl(ctx, hx('ff6f9a'), 6)
    # bush between
    for k in range(4):
        ellipse(ctx, 900 + k * 140, FLOOR - 60, 100, 80); fl(ctx, hx('2fbf5a'), 6)


def scooter(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for wx in (-90, 90):
        ellipse(ctx, wx, 0, 44, 44); fl(ctx, INK, 6); ellipse(ctx, wx, 0, 16, 16); setc(ctx, hx('b8bcc8')); ctx.fill()
    poly(ctx, [(-130, -30), (60, -30), (110, -150), (140, -150), (110, -10), (-120, 10)]); fl(ctx, hx('ff8a1f'), 6)
    rect_r(ctx, -140, -150, 110, 100, 12); fl(ctx, hx('2fbf5a'), 6)
    ctx.restore()


def map_screen(ctx, t, eta, eta_col):
    """big phone with a street map; t = 0..1 progress of the scooter route"""
    rect_r(ctx, 150, 470, 780, 900, 60); fl(ctx, hx('2a2a3a'), 9)
    ctx.save(); rect_r(ctx, 190, 510, 700, 820, 34); ctx.clip()
    ctx.rectangle(190, 510, 700, 820); setc(ctx, hx('e8f5d8')); ctx.fill()
    # blocks
    for bx in range(3):
        for by in range(3):
            rect_r(ctx, 230 + bx * 220, 680 + by * 210, 150, 140, 14); setc(ctx, hx('cfe8b0')); ctx.fill()
    ellipse(ctx, 735, 1105, 60, 50); setc(ctx, hx('8fdcff')); ctx.fill()
    ctx.restore()
    # route (dashed)
    ctx.save(); rect_r(ctx, 190, 510, 700, 820, 34); ctx.clip()
    route = route_pts()
    ctx.move_to(*route[0])
    for p_ in route[1:]:
        ctx.line_to(*p_)
    ctx.set_dash([18, 14]); setc(ctx, hx('1f8bff', )); ctx.set_line_width(10); ctx.stroke(); ctx.set_dash([])
    # home pin
    hxp, hyp = 420, 1210
    ellipse(ctx, hxp, hyp + 10, 30, 10); setc(ctx, (0, 0, 0, 0.2)); ctx.fill()
    poly(ctx, [(hxp - 40, hyp - 40), (hxp, hyp - 80), (hxp + 40, hyp - 40), (hxp + 40, hyp), (hxp - 40, hyp)]); fl(ctx, hx('ff3b5c'), 6)
    ctx.rectangle(hxp - 12, hyp - 30, 24, 30); setc(ctx, (1, 1, 1)); ctx.fill()
    # scooter dot
    sx, sy = along(route, t)
    ellipse(ctx, sx, sy, 34, 34); fl(ctx, hx('ff8a1f'), 6)
    scooter(ctx, sx, sy + 10, 0.18)
    ctx.restore()
    # eta banner
    rect_r(ctx, 190, 510, 700, 130, 34); setc(ctx, eta_col); ctx.fill()
    ctx.rectangle(190, 600, 700, 40); setc(ctx, eta_col); ctx.fill()
    text(ctx, "ARRIVING IN", 540, 548, 34, (1, 1, 1), outline=eta_col, ow=1, shadow=False)
    text(ctx, eta, 540, 602, 54, (1, 1, 1), outline=INK, ow=6, shadow=False)


def route_pts():
    # starts top right, comes close to home, then turns away and loops round a far block
    return [(860, 640), (640, 640), (640, 1080), (500, 1080), (500, 860), (860, 860), (860, 1290), (200, 1290), (200, 640), (640, 640)]


def along(pts, t):
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    d = t * sum(seg)
    for i, s_ in enumerate(seg):
        if d <= s_:
            u = d / s_ if s_ else 0
            return (lerp(pts[i][0], pts[i + 1][0], u), lerp(pts[i][1], pts[i + 1][1], u))
        d -= s_
    return pts[-1]


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 44:
        window_shot(ctx, f, f)
        label(ctx, "\"2 MIN AWAY!\"", 540, 1440, 110, hx('ffe14d'), -0.04, 1)
    else:
        lf = f - 44
        u = eout(pop(lf, 0, 14))
        ctx.save(); cam(ctx, lerp(820, 640, u), lerp(1040, 1060, u), lerp(1.7, 1.15, u), 0, shake_at(lf, [0], 8, 10), f)
        hallway(ctx, f=f)
        hop = abs(math.sin(lf * 0.45)) * 30
        d = draw_hip(ctx, 740, DHIP - hop, KD, 1, DAD, P(rsh=150, rel=10, lsh=40, lel=-60, eye='happy', mouth='grin', torso=6, lhip=8, rhip=-8))
        b = draw_hip(ctx, 420, BHIP - abs(math.sin(lf * 0.45 + 1.4)) * 30, KB, 1, BOY, P(rsh=150, rel=10, lsh=40, lel=-60, eye='happy', mouth='grin', torso=6))
        fork(ctx, d['front'][0], d['front'][1] - 20, 0.1, 1.2)
        fork(ctx, b['front'][0], b['front'][1] - 20, 0.1, 1.0)
        ctx.restore()
        label(ctx, "READY.", 540, 1440, 140, (1, 1, 1), 0.04, pop(lf, 4, 8))
    card(ctx, 'p1', f, -6, 110)


def s2(ctx, f):
    lf = f - 110
    if lf < 66:
        # map insert: scooter turns away from home and loops the far block
        ctx.save(); cam(ctx, 540, 920, 1.0 + 0.003 * lf, 0, 0, f)
        ctx.rectangle(-1000, -1000, 3000, 4000); setc(ctx, hx('ffd88a')); ctx.fill()
        rays(ctx, 540, 920, 150, 1100, lf * 0.02, col=(1, 1, 1), a=0.3, n=16)
        t = kf(lf, [(0, 0.0), (14, 0.17), (66, 0.78)], lambda x: x)
        etas = [(0, "2 MIN", hx('2fbf5a')), (22, "5 MIN", hx('ff8a1f')), (38, "9 MIN", hx('ff8a1f')), (52, "14 MIN", hx('ff3b5c'))]
        e = [x for x in etas if x[0] <= lf][-1]
        map_screen(ctx, t, e[1], e[2])
        ctx.restore()
        if lf < 18:
            label(ctx, "ALMOST...", 540, 1440, 120, (1, 1, 1), 0.03, pop(lf, 2, 6))
        else:
            label(ctx, "WRONG WAY!", 540, 1440, 130, hx('ff3b5c'), -0.04, pop(lf, 18, 22))
    elif lf < 96:
        # ECU Dad glaring at the phone
        il = lf - 66
        ctx.save(); cam(ctx, 600, 940, 2.1, 5, shake_at(il, [0, 14], 8, 14), f)
        hallway(ctx, f=f)
        d = draw_hip(ctx, 600, DHIP, KD, 1, DAD, P(rsh=120, rel=40, lsh=10, lel=-20, eye='glare', mouth='scream', torso=-4, head=-4))
        phone(ctx, d['front'][0] + 20, d['front'][1] - 40, 0.2, 1.4, "14 MIN", hx('ff3b5c'))
        ctx.restore()
        label(ctx, "WHY IS HE", 540, 1320, 100, (1, 1, 1), 0.03, pop(il, 2, 6))
        label(ctx, "GOING LEFT?!", 540, 1440, 110, hx('ff3b5c'), -0.03, pop(il, 4, 8))
    else:
        # time-lapse: flopped on the floor, clock spinning
        il = lf - 96
        sink = eout(pop(il, 0, 30))
        ctx.save(); cam(ctx, 560, 1140, 1.1, 0, 0, f)
        hallway(ctx, f=f, clock_t=il * 0.9)
        draw_hip(ctx, 620, DHIP + 70 * sink, KD, 1, DAD, P(rsh=-20, rel=-10, lsh=-30, lel=-10, eye='closed' if il > 30 else 'normal', mouth='flat',
                                                         torso=lerp(0, -40, sink), head=-10 * sink, lhip=lerp(6, 80, sink), rhip=lerp(-6, 85, sink),
                                                         lkn=lerp(-4, -80, sink), rkn=lerp(-4, -80, sink), rot=-15 * sink))
        draw_hip(ctx, 410, BHIP + 60 * sink, KB, 1, BOY, P(rsh=20, rel=-10, lsh=-20, lel=-10, eye='closed' if il > 20 else 'normal', mouth='open' if il > 20 else 'flat',
                                                         torso=lerp(0, 30, sink), head=12 * sink, lhip=lerp(6, 80, sink), rhip=lerp(-6, 85, sink),
                                                         lkn=lerp(-4, -80, sink), rkn=lerp(-4, -80, sink), rot=20 * sink))
        for k in range(3):
            tt = ((il * 0.04) + k / 3) % 1
            text(ctx, "Z", 350 + 40 * tt + k * 10, 1150 - 160 * tt, 40 + 20 * tt, (1, 1, 1), ow=6, shadow=False)
        ctx.restore()
        label(ctx, "STILL WAITING...", 540, 1440, 100, (1, 1, 1), 0.03, pop(il, 2, 6))
    card(ctx, 'p2', f, 114, 206)


def s3(ctx, f):
    lf = f - 260
    if lf < 40:
        # Dad gets up and goes to the bathroom
        ctx.save(); cam(ctx, 420, 1130, 1.15, 0, shake_at(lf, [30], 10, 16), f)
        ph = lf * 0.5
        s_ = math.sin(ph)
        shut = lf >= 30
        hallway(ctx, f=f, bath_open=0 if shut else (eout(pop(lf, 0, 8)) * 0.85), bath_shake=(1 - pop(lf, 30, 40)) if shut else 0)
        if not shut:
            dx = lerp(640, 180, ease(pop(lf, 0, 28)))
            draw_hip(ctx, dx, DHIP - 6 * abs(s_), KD, -1, DAD, P(rsh=20 * s_, rel=-20, lsh=-20 * s_, lel=-20, eye='normal', mouth='smile', torso=4,
                                                               lhip=24 * s_, rhip=-24 * s_, lkn=-25 * max(0, s_), rkn=-25 * max(0, -s_)))
        draw_hip(ctx, 700, BHIP, KB, -1, BOY, P(rsh=20, rel=-10, lsh=-20, lel=-10, eye='normal', mouth='smile'))
        ctx.restore()
        if lf < 30:
            label(ctx, "\"ONE SECOND...\"", 540, 1440, 100, (1, 1, 1), 0.03, pop(lf, 2, 6))
        else:
            label(ctx, "*CLICK*", 540, 1440, 120, hx('ffe14d'), -0.04, pop(lf, 30, 34))
    elif lf < 84:
        # split: front door rings (top) / Dad frozen in the bathroom (bottom)
        il = lf - 40
        ring_ = il >= 4
        ctx.save(); ctx.rectangle(0, 0, W, H / 2); ctx.clip()
        ctx.save(); cam(ctx, 830, 1080, 1.45, 0, shake_at(il, [4, 16], 10, 18), f)
        hallway(ctx, f=f, door_shake=1 if ring_ and il % 12 < 8 else 0)
        if ring_:
            for k in range(3):
                r = 60 + ((il * 6 + k * 40) % 120)
                ctx.new_path(); ctx.arc(830, 1080, r * 1.6, -0.5, 0.5); setc(ctx, hx('ffe14d') + (1 - r / 180,)); ctx.set_line_width(12); ctx.stroke()
                ctx.new_path(); ctx.arc(830, 1080, r * 1.6, math.pi - 0.5, math.pi + 0.5); ctx.stroke()
        ctx.restore(); ctx.restore()
        ctx.save(); ctx.rectangle(0, H / 2, W, H / 2); ctx.clip()
        ctx.save(); cam(ctx, 540, 1060, 2.0, 0, shake_at(il, [4], 10, 12), f)
        ctx.translate(0, 195)
        ctx.rectangle(-1000, -1000, 3000, 4000); setc(ctx, hx('ffd1e3')); ctx.fill()
        for i in range(-6, 16):
            ctx.move_to(i * 90, -500); ctx.line_to(i * 90, 2500); ctx.move_to(-500, i * 90 + 400); ctx.line_to(2000, i * 90 + 400)
        setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(6); ctx.stroke()
        draw_hip(ctx, 540, DHIP, KD, 1, DAD, P(rsh=150, rel=-30, lsh=-150, lel=30, eye='shock' if ring_ else 'normal', mouth='scream' if ring_ else 'smile', torso=-4))
        ctx.restore(); ctx.restore()
        ctx.rectangle(0, H / 2 - 9, W, 18); setc(ctx, INK); ctx.fill()
        if ring_:
            label(ctx, "DING DONG!", 540, 760, 140, hx('ffe14d'), -0.05, pop(il, 4, 8))
            label(ctx, "NOW?!", 540, 1440, 150, hx('ff3b5c'), 0.04, pop(il, 14, 18))
    else:
        # bathroom door BLASTS open, Dad sprints with toilet paper on his shoe
        il = lf - 84
        ctx.save(); cam(ctx, lerp(300, 760, eout(pop(il, 0, 50))), 1150, 1.2, 0, shake_at(il, [0], 12, 24), f)
        hallway(ctx, f=f, bath_open=eout(pop(il, 0, 3)))
        ph = il * 1.1
        s_ = math.sin(ph)
        dx = lerp(180, 900, eout(pop(il, 2, 40)))
        hd = draw_hip(ctx, dx, DHIP - 30 * abs(s_), KD, 1, DAD, P(rsh=70 * s_, rel=-80, lsh=-70 * s_, lel=-80, eye='shock', mouth='scream', torso=18,
                                                              lhip=50 * s_, rhip=-50 * s_, lkn=-60 * max(0, s_), rkn=-60 * max(0, -s_)))
        toilet_paper(ctx, dx - 40, FLOOR - 20, max(BATH1 - 40, dx - 600), FLOOR - 10, il)
        for k in range(5):
            y = 900 + k * 110
            ctx.move_to(dx - 260 - k * 30, y); ctx.line_to(dx - 520 - k * 30, y); ink(ctx, 8); ctx.stroke()
        ctx.restore()
        label(ctx, "COMING!!!", 540, 1440, 140, (1, 1, 1), -0.04, pop(il, 2, 6))
    card(ctx, 'p3', f, 264, 300)


def s4(ctx, f):
    lf = f - 400
    if lf < 46:
        # outside: porch empty, scooter zooming off
        ctx.save(); cam(ctx, 520, 1180, 1.05, 0, shake_at(lf, [0], 10, 16), f)
        street(ctx, f, door_open=1)
        note(ctx, 300, FLOOR - 10, 0.45, -0.1, full=False)
        h = draw_hip(ctx, 330, DHIP, KD, 1, DAD, P(rsh=150, rel=20, lsh=-150, lel=-20, eye='shock', mouth='scream', torso=-4, head=6))
        toilet_paper(ctx, 290, FLOOR - 20, 150, FLOOR - 5, lf)
        sx = lerp(900, 1700, ein(pop(lf, 0, 26)))
        if lf < 26:
            scooter(ctx, sx, FLOOR + 220, 1.1)
            for k in range(3):
                puff(ctx, sx - 200 - k * 60, FLOOR + 220, ((lf * 0.08) + k / 3) % 1, 0.8)
        ctx.restore()
        label(ctx, "NOBODY?!", 540, 1440, 150, hx('ff3b5c'), -0.04, pop(lf, 2, 6))
    elif lf < 72:
        # insert: the note
        il = lf - 46
        ctx.save(); cam(ctx, 540, 940, 1.0, 0, shake_at(il, [0], 6, 8), f)
        ctx.rectangle(-1000, -1000, 3000, 4000); setc(ctx, hx('5a7bd6')); ctx.fill()
        rays(ctx, 540, 940, 150, 1100, il * 0.02, col=(1, 1, 1), a=0.2, n=16)
        note(ctx, 540, 940, 2.4 + 0.1 * eout(pop(il, 0, 6)), -0.06)
        ctx.restore()
        label(ctx, "...REALLY?", 540, 1440, 120, (1, 1, 1), 0.03, pop(il, 6, 10))
    else:
        # whip pan across the street: neighbour eating Dad's fries, waving
        il = lf - 72
        u = eout(pop(il, 0, 8))
        ctx.save(); cam(ctx, lerp(520, 2180, u), 1150, lerp(1.05, 1.5, eout(pop(il, 4, 40))), 0, 0, f)
        street(ctx, f, door_open=1)
        n = draw_hip(ctx, 2140, DHIP, KD, 1, NEIGH, P(rsh=150 + 15 * math.sin(il * 0.8), rel=-40 + 25 * math.sin(il * 0.8), lsh=40, lel=-90,
                                                      eye='happy', mouth='grin' if il % 12 < 6 else 'open', torso=-4))
        bx, by = n['back']
        food_bag(ctx, bx - 10, by + 40, 0.75, 0.1)
        fx_, fy_ = n['front']
        fry(ctx, fx_, fy_ - 30, 0.4, 1.2)
        if il < 10:
            for k in range(6):
                y = 900 + k * 110
                ctx.move_to(1700, y); ctx.line_to(2600, y); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(14); ctx.stroke()
        ctx.restore()
        label(ctx, "\"THANKS!\"", 540, 1440, 140, hx('2fbf5a'), 0.04, pop(il, 10, 14))
    card(ctx, 'p4', f, 404, 530)


def s5(ctx, f):
    lf = f - 530
    if lf < 50:
        # Dad parked on a chair right in front of the door, legs crossed, refusing to move
        ctx.save(); cam(ctx, 760, 1020, lerp(1.2, 1.5, eout(pop(lf, 0, 50))), 0, shake_at(lf, [26], 8, 12), f)
        hallway(ctx, f=f)
        # chair
        rect_r(ctx, 700, 1200, 220, 40, 10); fl(ctx, hx('ff8a1f'), 6)
        rect_r(ctx, 880, 900, 40, 320, 12); fl(ctx, hx('ff8a1f'), 6)
        for lx in (710, 880):
            ctx.rectangle(lx, 1240, 26, FLOOR - 1240); fl(ctx, hx('c96a1a'), 5)
        jit = 4 * math.sin(lf * 2.1)
        d = draw_hip(ctx, 790 + jit, 1215, KD, -1, DAD, P(rsh=40, rel=80, lsh=-30, lel=-30, eye='glare', mouth='flat' if lf < 26 else 'wavy',
                                                          torso=-6, lhip=-80, lkn=80, rhip=-95, rkn=95, head=4))
        phone(ctx, d['front'][0] - 10, d['front'][1] - 10, -0.2, 1.4, "2 MIN" if lf < 26 else "45 MIN", hx('2fbf5a') if lf < 26 else hx('ff3b5c'))
        hx_, hy_ = d['head']
        if lf >= 26:
            for k in range(2):
                dy = (lf * 4 + k * 40) % 80
                ellipse(ctx, hx_ - 150 + k * 300, hy_ - 60 + dy, 14, 22); fl(ctx, hx('8fdcff'), 4)
        ctx.restore()
        if lf < 26:
            label(ctx, "NOT. MOVING.", 540, 1440, 130, (1, 1, 1), -0.03, pop(lf, 2, 6))
        else:
            label(ctx, "...45 MIN?!", 540, 1440, 140, hx('ff3b5c'), 0.04, pop(lf, 26, 30))
        card(ctx, 'p5', f, 534, 580)
    elif lf < 96:
        # ECU Dad sweating, wavy mouth, legs crossed tighter
        il = lf - 50
        ctx.save(); cam(ctx, 790, 900, 2.3, -4 + 3 * math.sin(il * 0.6), shake_at(il, [0, 20], 6, 10), f)
        hallway(ctx, f=f)
        d = draw_hip(ctx, 790 + 6 * math.sin(il * 2.5), 1215, KD, -1, DAD, P(rsh=120, rel=40, lsh=-30, lel=-30, eye='shock', mouth='wavy',
                                                                            torso=-6, lhip=-80, lkn=80, rhip=-95, rkn=95, head=-6))
        hx_, hy_ = d['head']
        for k in range(3):
            dy = (il * 5 + k * 30) % 90
            ellipse(ctx, hx_ - 170 + k * 170, hy_ - 90 + dy, 12, 20); fl(ctx, hx('8fdcff'), 4)
        ctx.restore()
        label(ctx, "BUT...", 540, 1320, 100, (1, 1, 1), 0.03, pop(il, 2, 6))
        label(ctx, "I NEED THE BATHROOM", 540, 1440, 84, hx('8a3cff'), -0.03, pop(il, 12, 16))
    else:
        il = lf - 96
        window_shot(ctx, f, il)
        label(ctx, "\"2 MIN AWAY!\"", 540, 1440, 110, hx('ffe14d'), -0.04, pop(il, 0, 4))
        card(ctx, 'p1', f, 626)


SHOTS = [(0, s1), (110, s2), (260, s3), (400, s4), (530, s5)]
CUTS = (44, 110, 176, 206, 260, 300, 344, 400, 446, 472, 530, 580, 626)


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
            render(f).write_to_png(f'out/w{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/delivery_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
