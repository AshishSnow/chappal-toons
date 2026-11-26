"""'DAD vs THE NEIGHBOR'S LIGHTS'. Original, general-audience comedy short, 22s.
Hook:   snowy night front yard, medium shot: Dad on a ladder against his house, which is already blazing with
        holiday lights, frantically hanging ANOTHER string, sweating "MORE... LIGHTS!!" + caption; kid in shades.
Beat 1: Dad plugs in ONE neat string *click* "PERFECT." -> pan right: the neighbour's house *KA-CHUNK!* blazes,
        reindeer inflatable *FWOOMP* -> neighbour waves "Evening, NEIGHBOR!" -> whip back: Dad glares "...oh, it's ON."
Beat 2: split screen, Dad (top) vs neighbour (bottom): *KA-CHUNK!* MORE! / MORE!! / MORE!!! / ...EVEN MORE.
Beat 3: the one close-up: Dad lit by coloured bokeh, holding a GIANT plug "I... WILL..." "...WIN!!"
Twist:  *KA-CHUNK!!* Dad's house shines like the sun, neighbour puts on shades "...okay. You WIN." Dad "YESSS!!"
        PLOT TWIST: THE WHOLE STREET WENT DARK. *bzzzt... POP!* only eyes in the dark "...honey?" ->
        Mom in the window lights ONE candle "Who wants COCOA?" -> Dad's eyes "...I need MORE LIGHTS." -> hook loop."""
from eng3 import *
import doodle, sys, subprocess, random
from doodle import INK, fl, ink, draw
from scenes6 import pop, sparkle, shake_at
from scenes32 import label, cam, rect_r, face, rays
from scenes58 import sweat, twitch
from scenes84 import eio
import scenes13
from scenes13 import card as _card13

RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff'); MINT = hx('3fd6a0')
SNOW = hx('f2f6ff'); SNOWSH = hx('c9d6f2')
DAD = dict(doodle.DAD, shirt=hx('ff4d5e'), pants=hx('3a4a8a'), shoes=hx('6a3a24'))
KID = dict(doodle.BOY, hood=True, shades=True, shirt=hx('3fd6a0'), pants=hx('3d7bff'), shoes=hx('ffc93c'))
NB = dict(doodle.NEIGHBOR, tie=None, shirt=hx('22b45a'), sleeve=1.0, shades=True)
MOM = doodle.MOM_G
N = 660
GND = 1660      # where people stand
HB = 1520       # house base
DCX, NCX = 540, 1640   # house centres (Dad, neighbour)
SOCK = 930      # Dad's outdoor socket post
NSOCK = 1240
BCOL = (RED, GOLD, MINT, PINK, BLUE, ORANGE, WHITE)

CAPS = {'p1': [[("DAD vs THE", OUT)], [("NEIGHBOR'S ", RED), ("LIGHTS:", BLUE)]],
        'p2': [[("PLOT TWIST:", RED)], [("THE WHOLE STREET", OUT)], [("WENT ", OUT), ("DARK.", PURPLE)]]}
scenes13.CAPS = CAPS
card = _card13


def stand(ctx, ch, x, k, p, f_=1, feet=GND):
    return draw(ctx, x, feet - 186 * k, k, f_, ch, p)


# ------------------------------------------------------------------ lights
def resample(pts, step):
    out = []
    carry = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        d = carry
        while d < L:
            u = d / L; out.append((lerp(x0, x1, u), lerp(y0, y1, u))); d += step
        carry = d - L
    return out


def bulbs(ctx, pts, lf, on=1.0, step=46, seed=0, r=9, sag=10, chase=True):
    if len(pts) < 2:
        return
    # wire
    ctx.new_path(); ctx.move_to(*pts[0])
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        ctx.line_to(x1, y1)
    setc(ctx, hx('1d3a2a')); ctx.set_line_width(3); ctx.stroke()
    for i, (x, y) in enumerate(resample(pts, step)):
        c = BCOL[(i + seed) % len(BCOL)]
        lit = on
        if chase and on > 0.5:
            lit = 0.65 + 0.35 * (1 if (i + lf // 6) % 3 else 0)
        if lit > 0.05:
            ellipse(ctx, x, y + r, r * 3.2, r * 3.2); setc(ctx, c[:3] + (0.22 * lit,)); ctx.fill()
        ellipse(ctx, x, y + r, r * 0.8, r * 1.15)
        setc(ctx, tuple(lerp(dark(c, 0.45)[j], c[j], lit) for j in range(3))); ctx.fill()
        if lit > 0.3:
            ellipse(ctx, x - r * 0.25, y + r * 0.7, r * 0.25, r * 0.35); setc(ctx, (1, 1, 1, 0.8 * lit)); ctx.fill()


def roof_pts(cx):
    return [(cx - 400, 1080), (cx, 760), (cx + 400, 1080)]


# ------------------------------------------------------------------ set: snowy night street
def sky(ctx, lf, dark_=0.0):
    ctx.set_source(vgrad(ctx, 0, 0, 0, 1500, [(0, hx('1a1f5e')), (0.65, hx('3b3a9e')), (1, hx('6a5ac8'))]))
    ctx.rectangle(-3000, -3000, 9000, 9000); ctx.fill()
    rnd = random.Random(5)
    for k in range(90):
        sx, sy = rnd.uniform(-900, 3200), rnd.uniform(-500, 1000)
        tw = 0.5 + 0.5 * math.sin(lf * 0.15 + k)
        sparkle(ctx, sx, sy, 4 + 5 * tw, hx('fff6c0'))
    ellipse(ctx, 2050, 420, 90, 90); fl(ctx, hx('fff3c0'), 5)
    ellipse(ctx, 2025, 400, 16, 13); setc(ctx, hx('f0dea0')); ctx.fill()
    ellipse(ctx, 2080, 450, 11, 9); setc(ctx, hx('f0dea0')); ctx.fill()
    # far snowy hills + pines
    for (x, y, r) in ((-200, 1480, 900), (1100, 1500, 1000), (2500, 1480, 900)):
        ellipse(ctx, x, y, r, 260); fl(ctx, hx('aab4e8'), 4)


def ground(ctx):
    ctx.rectangle(-3000, HB - 40, 9000, 4000); setc(ctx, SNOW); ctx.fill()
    ctx.move_to(-3000, HB - 40); ctx.line_to(6000, HB - 40); ink(ctx, 4); ctx.stroke()
    rnd = random.Random(8)
    for k in range(30):
        x, y = rnd.uniform(-900, 3000), rnd.uniform(HB + 20, 1760)
        ellipse(ctx, x, y, 60, 10); setc(ctx, SNOWSH[:3] + (0.5,)); ctx.fill()
    # sidewalk + street
    ctx.rectangle(-3000, 1790, 9000, 70); setc(ctx, hx('d8dcec')); ctx.fill()
    for k in range(-30, 60):
        ctx.move_to(k * 140, 1790); ctx.line_to(k * 140 - 10, 1860); setc(ctx, (0.6, 0.62, 0.75, 0.6)); ctx.set_line_width(3); ctx.stroke()
    ctx.rectangle(-3000, 1860, 9000, 3000); setc(ctx, hx('4a4e6e')); ctx.fill()
    for k in range(-20, 40):
        rect_r(ctx, k * 260, 2000, 140, 18, 8); setc(ctx, hx('fff27a')); ctx.fill()


def fence(ctx, x0, x1):
    ctx.rectangle(x0, 1420, x1 - x0, 14); fl(ctx, WHITE, 3)
    ctx.rectangle(x0, 1470, x1 - x0, 14); fl(ctx, WHITE, 3)
    x = x0
    while x <= x1:
        poly(ctx, [(x, HB), (x, 1400), (x + 15, 1380), (x + 30, 1400), (x + 30, HB)]); fl(ctx, WHITE, 3)
        ellipse(ctx, x + 15, 1384, 18, 8); setc(ctx, SNOW); ctx.fill()
        x += 60


def lamp(ctx, x, on=1.0):
    ctx.rectangle(x - 10, 900, 20, GND - 900); fl(ctx, hx('3a3f5e'), 3)
    if on > 0:
        g = cairo.RadialGradient(x, 900, 10, x, 900, 260)
        g.add_color_stop_rgba(0, 1, 0.95, 0.7, 0.55 * on); g.add_color_stop_rgba(1, 1, 0.95, 0.7, 0)
        ctx.set_source(g); ctx.arc(x, 900, 260, 0, 7); ctx.fill()
    poly(ctx, [(x - 40, 900), (x - 26, 850), (x + 26, 850), (x + 40, 900)]); fl(ctx, hx('fff0a0') if on > 0.5 else hx('6a6a80'), 3)
    rect_r(ctx, x - 46, 836, 92, 18, 6); fl(ctx, hx('3a3f5e'), 3)
    # wreath on the lamp post
    ctx.new_path(); ctx.arc(x, 1060, 34, 0, 7); setc(ctx, INK); ctx.set_line_width(22); ctx.stroke()
    ctx.new_path(); ctx.arc(x, 1060, 34, 0, 7); setc(ctx, GREEN); ctx.set_line_width(14); ctx.stroke()
    poly(ctx, [(x, 1098), (x - 22, 1120), (x - 20, 1090)]); fl(ctx, RED, 2)
    poly(ctx, [(x, 1098), (x + 22, 1120), (x + 20, 1090)]); fl(ctx, RED, 2)


def socket_post(ctx, x):
    rect_r(ctx, x - 26, 1480, 52, GND - 1470, 6); fl(ctx, hx('7a8aa0'), 3)
    rect_r(ctx, x - 40, 1440, 80, 70, 10); fl(ctx, hx('ffc93c'), 4)
    for sx in (-12, 12):
        rect_r(ctx, x + sx - 4, 1462, 8, 22, 3); setc(ctx, INK); ctx.fill()


def plug(ctx, x, y, s=1.0, ang=0.0, cable_to=None):
    if cable_to:
        ctx.new_path(); ctx.move_to(x, y + 40 * s)
        ctx.curve_to(x, y + 200 * s, cable_to[0] - 200, cable_to[1], *cable_to)
        setc(ctx, INK); ctx.set_line_width(26 * s); ctx.stroke()
        ctx.new_path(); ctx.move_to(x, y + 40 * s)
        ctx.curve_to(x, y + 200 * s, cable_to[0] - 200, cable_to[1], *cable_to)
        setc(ctx, hx('2fbf5a')); ctx.set_line_width(16 * s); ctx.stroke()
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s)
    for sx in (-18, 18):
        rect_r(ctx, sx - 7, -96, 14, 52, 4); fl(ctx, hx('d8dce6'), 3)
    rect_r(ctx, -50, -52, 100, 96, 18); fl(ctx, ORANGE, 5)
    for k in range(3):
        rect_r(ctx, -36, -30 + k * 24, 72, 8, 4); setc(ctx, dark(ORANGE, 0.75)); ctx.fill()
    ctx.restore()


def window(ctx, x, y, w, h, lit=1.0, mom=None, candle=0.0):
    rect_r(ctx, x - w / 2 - 14, y - h / 2 - 14, w + 28, h + 28, 10); fl(ctx, WHITE, 4)
    ctx.save(); rect_r(ctx, x - w / 2, y - h / 2, w, h, 6); ctx.clip()
    ctx.set_source(vgrad(ctx, 0, y - h / 2, 0, y + h / 2, [(0, tuple(lerp(hx('2a2a50')[j], hx('ffd98a')[j], lit) for j in range(3))),
                                                          (1, tuple(lerp(hx('1a1a3a')[j], hx('ffb85a')[j], lit) for j in range(3)))]))
    ctx.paint()
    if mom is not None:
        stand(ctx, MOM, x - 10, 0.55, mom, 1, y + 175)
    if candle > 0:
        ctx.rectangle(x + 30, y + 30, 16, 42); fl(ctx, WHITE, 2)
        ellipse(ctx, x + 38, y + 20, 8 * candle, 14 * candle); setc(ctx, hx('ffc93c')); ctx.fill()
    ctx.restore()
    # curtains + cross
    for sx in (-1, 1):
        poly(ctx, [(x + sx * w / 2, y - h / 2), (x + sx * w * 0.3, y - h / 2), (x + sx * w * 0.42, y + h / 2), (x + sx * w / 2, y + h / 2)])
        fl(ctx, hx('ff8aa8'), 3)
    ctx.move_to(x, y - h / 2); ctx.line_to(x, y + h / 2); ctx.move_to(x - w / 2, y); ctx.line_to(x + w / 2, y)
    setc(ctx, WHITE); ctx.set_line_width(10); ctx.stroke()
    rect_r(ctx, x - w / 2 - 24, y + h / 2 + 8, w + 48, 20, 6); fl(ctx, WHITE, 3)
    ellipse(ctx, x, y + h / 2 + 10, w / 2 + 20, 10); setc(ctx, SNOW); ctx.fill()


def house(ctx, cx, lv, lf, owner='dad', on=1.0, mom=None, candle=0.0, win_lit=1.0):
    wall = hx('ffd8a8') if owner == 'dad' else hx('b8d8ff')
    roofc = hx('d0566a') if owner == 'dad' else hx('5a5ab8')
    door = hx('3fa0ff') if owner == 'dad' else hx('ffc93c')
    # chimney
    rect_r(ctx, cx + 170, 800, 80, 170, 4); fl(ctx, hx('c0604a'), 4)
    ellipse(ctx, cx + 210, 800, 52, 16); setc(ctx, SNOW); ctx.fill()
    # walls
    ctx.rectangle(cx - 330, 1040, 660, HB - 1040); fl(ctx, wall, 5)
    for k in range(1, 9):
        ctx.move_to(cx - 330, 1040 + k * 54); ctx.line_to(cx + 330, 1040 + k * 54)
    setc(ctx, dark(wall, 0.88)[:3] + (0.6,)); ctx.set_line_width(3); ctx.stroke()
    # wall curtain lights (behind windows)
    if lv >= 4:
        for k in range(12):
            x = cx - 310 + k * 56
            bulbs(ctx, [(x, 1070), (x, 1490)], lf, on, 48, k, 7)
    # roof
    poly(ctx, [(cx - 400, 1080), (cx, 760), (cx + 400, 1080)]); fl(ctx, roofc, 6)
    ctx.new_path(); ctx.move_to(cx - 400, 1080); ctx.line_to(cx, 760); ctx.line_to(cx + 400, 1080)
    ctx.curve_to(cx + 300, 1040, cx + 250, 1010, cx + 200, 1000); ctx.line_to(cx, 830); ctx.line_to(cx - 200, 1000)
    ctx.curve_to(cx - 250, 1010, cx - 300, 1040, cx - 400, 1080); ctx.close_path(); setc(ctx, SNOW); ctx.fill()
    # round attic window
    ellipse(ctx, cx, 950, 50, 50); fl(ctx, WHITE, 4)
    ellipse(ctx, cx, 950, 36, 36); setc(ctx, hx('ffd98a') if win_lit > 0.5 else hx('2a2a50')); ctx.fill()
    if lv >= 5:   # roof net
        for j in range(1, 6):
            y = 780 + j * 52; half = (y - 760) / 320 * 400
            bulbs(ctx, [(cx - half + 20, y), (cx + half - 20, y)], lf, on, 44, j * 2, 7)
    # windows + door
    window(ctx, cx - 190, 1220, 190, 170, win_lit, mom, candle)
    window(ctx, cx + 190, 1220, 190, 170, win_lit)
    rect_r(ctx, cx - 65, 1330, 130, HB - 1330 + 10, 14); fl(ctx, door, 5)
    ellipse(ctx, cx + 38, 1430, 8, 8); fl(ctx, GOLD, 2)
    ctx.new_path(); ctx.arc(cx, 1385, 32, 0, 7); setc(ctx, INK); ctx.set_line_width(20); ctx.stroke()
    ctx.new_path(); ctx.arc(cx, 1385, 32, 0, 7); setc(ctx, GREEN); ctx.set_line_width(13); ctx.stroke()
    ellipse(ctx, cx, 1420, 14, 9); fl(ctx, RED, 2)
    # steps + bushes
    rect_r(ctx, cx - 100, HB - 4, 200, 30, 6); fl(ctx, hx('d8dcec'), 3)
    for sx in (-1, 1):
        ellipse(ctx, cx + sx * 300, HB - 30, 110, 70); fl(ctx, hx('1f9a6a'), 4)
        ellipse(ctx, cx + sx * 300, HB - 82, 80, 20); setc(ctx, SNOW); ctx.fill()
    # lights by level
    if lv >= 1:
        bulbs(ctx, [(cx - 400, 1080), (cx, 760), (cx + 400, 1080)], lf, on, 46, 0, 10)
    if lv >= 2:
        for wx in (cx - 190, cx + 190):
            bulbs(ctx, [(wx - 110, 1120), (wx + 110, 1120), (wx + 110, 1320), (wx - 110, 1320), (wx - 110, 1120)], lf, on, 40, 3, 7)
        bulbs(ctx, [(cx - 80, HB), (cx - 80, 1320), (cx + 80, 1320), (cx + 80, HB)], lf, on, 40, 1, 7)
        for sx in (-1, 1):
            for j in range(3):
                bulbs(ctx, [(cx + sx * 300 - 90 + j * 10, HB - 60 + j * 30), (cx + sx * 300 + 90 - j * 10, HB - 60 + j * 30)], lf, on, 32, j, 6)
    if lv >= 3:
        # icicle lights under the eaves
        for k in range(15):
            x = cx - 340 + k * 48
            bulbs(ctx, [(x, 1050), (x, 1050 + 30 + 30 * (k % 3))], lf, on, 30, k, 6, chase=False)
        star(ctx, cx, 735, 60, lf, on)
    if lv >= 4:
        bulbs(ctx, [(cx + 170, 830), (cx + 250, 830), (cx + 250, 960), (cx + 170, 960)], lf, on, 36, 2, 7)
    if lv >= 6:
        g = cairo.RadialGradient(cx, 1100, 100, cx, 1100, 1100)
        g.add_color_stop_rgba(0, 1, 1, 0.85, 0.55 * on); g.add_color_stop_rgba(1, 1, 1, 0.85, 0)
        ctx.set_source(g); ctx.arc(cx, 1100, 1100, 0, 7); ctx.fill()


def star(ctx, x, y, r, lf, on=1.0):
    if on > 0.3:
        rays(ctx, x, y, r * 1.1, r * 2.6, lf * 0.02, (1, 0.95, 0.5), 0.5 * on, 10)
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    poly(ctx, pts); fl(ctx, GOLD if on > 0.3 else dark(GOLD, 0.5), 4)


def inflatable_snowman(ctx, x, s, on, lf, puff=1.0):
    if puff <= 0:
        return
    ctx.save(); ctx.translate(x, GND - 10); ctx.scale(s * (0.6 + 0.4 * puff), s * puff)
    if on > 0.3:
        g = cairo.RadialGradient(0, -250, 20, 0, -250, 330)
        g.add_color_stop_rgba(0, 1, 1, 1, 0.45 * on); g.add_color_stop_rgba(1, 1, 1, 1, 0)
        ctx.set_source(g); ctx.arc(0, -250, 330, 0, 7); ctx.fill()
    ellipse(ctx, 0, -110, 120, 110); fl(ctx, WHITE, 5)
    ellipse(ctx, 0, -300, 90, 90); fl(ctx, WHITE, 5)
    for sx in (-1, 1):
        ellipse(ctx, sx * 30, -320, 11, 14); setc(ctx, INK); ctx.fill()
        ellipse(ctx, sx * 27, -324, 4, 4); setc(ctx, WHITE); ctx.fill()
        ellipse(ctx, sx * 52, -290, 14, 8); setc(ctx, hx('ff9aa8')); ctx.fill()
    poly(ctx, [(-6, -300), (50, -290), (-4, -282)]); fl(ctx, ORANGE, 3)
    ctx.new_path(); ctx.arc(0, -282, 18, 0.4, math.pi - 0.4); ink(ctx, 4); ctx.stroke()
    rect_r(ctx, -80, -228, 160, 30, 12); fl(ctx, RED, 4)
    rect_r(ctx, -70, -440, 140, 60, 8); fl(ctx, hx('2a3a6a'), 4)
    rect_r(ctx, -100, -390, 200, 18, 8); fl(ctx, hx('2a3a6a'), 4)
    for k in range(3):
        ellipse(ctx, 0, -150 + k * 40, 9, 9); setc(ctx, INK); ctx.fill()
    ctx.restore()


def inflatable_deer(ctx, x, s, on, lf, puff=1.0):
    if puff <= 0:
        return
    ctx.save(); ctx.translate(x, GND - 10); ctx.scale(s * (0.6 + 0.4 * puff), s * puff)
    if on > 0.3:
        g = cairo.RadialGradient(0, -200, 20, 0, -200, 300)
        g.add_color_stop_rgba(0, 1, 0.8, 0.6, 0.4 * on); g.add_color_stop_rgba(1, 1, 0.8, 0.6, 0)
        ctx.set_source(g); ctx.arc(0, -200, 300, 0, 7); ctx.fill()
    brown = hx('c07a3a')
    for lx in (-80, -40, 50, 90):
        rect_r(ctx, lx - 14, -130, 28, 125, 12); fl(ctx, brown, 4)
    ellipse(ctx, 0, -170, 140, 70); fl(ctx, brown, 5)
    ellipse(ctx, 10, -150, 80, 36); setc(ctx, hx('f0c89a')); ctx.fill()
    rect_r(ctx, 70, -320, 50, 160, 22); fl(ctx, brown, 5)
    ellipse(ctx, 110, -330, 70, 56); fl(ctx, brown, 5)
    for sx in (-1, 1):   # antlers
        ctx.new_path(); ctx.move_to(100 + sx * 24, -380); ctx.line_to(100 + sx * 60, -460); ctx.move_to(100 + sx * 44, -428); ctx.line_to(100 + sx * 84, -440)
        setc(ctx, INK); ctx.set_line_width(18); ctx.stroke_preserve(); setc(ctx, hx('8a5a3a')); ctx.set_line_width(10); ctx.stroke()
    ellipse(ctx, 92, -342, 9, 12); setc(ctx, INK); ctx.fill()
    ellipse(ctx, 132, -342, 9, 12); setc(ctx, INK); ctx.fill()
    ellipse(ctx, 176, -316, 22, 20); fl(ctx, RED, 4)
    if on > 0.3:
        ellipse(ctx, 176, -316, 40, 40); setc(ctx, (1, 0.2, 0.3, 0.35 * on)); ctx.fill()
    ctx.new_path(); ctx.move_to(-130, -190); ctx.line_to(-170, -230); setc(ctx, INK); ctx.set_line_width(14); ctx.stroke()
    ctx.restore()


def candy_cane(ctx, x, s, on):
    ctx.save(); ctx.translate(x, GND); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(0, 0); ctx.line_to(0, -260); ctx.arc_negative(-40, -260, 40, 0, math.pi)
    setc(ctx, INK); ctx.set_line_width(36); ctx.stroke_preserve(); setc(ctx, WHITE); ctx.set_line_width(26); ctx.stroke_preserve()
    ctx.set_dash([26, 26]); setc(ctx, RED); ctx.stroke(); ctx.set_dash([])
    if on > 0.3:
        ellipse(ctx, -20, -200, 90, 180); setc(ctx, (1, 0.4, 0.5, 0.18 * on)); ctx.fill()
    ctx.restore()


def street(ctx, lf, dlv=1, nlv=0, don=1.0, non=1.0, lamp_on=1.0, deer=0.0, nsnow=0.0, dsnow=0.0, mom=None, candle=0.0, win=1.0):
    sky(ctx, lf)
    ground(ctx)
    lamp(ctx, 1100, lamp_on)
    fence(ctx, 1000, 1220)
    house(ctx, DCX, dlv, lf, 'dad', don, mom, candle, win)
    house(ctx, NCX, nlv, lf, 'nb', non, None, 0, win)
    socket_post(ctx, SOCK)
    socket_post(ctx, NSOCK)
    # neighbour's lawn toys
    inflatable_deer(ctx, NCX + 460, 0.8, non, lf, deer)
    if nlv >= 5:
        for k in range(4):
            candy_cane(ctx, NCX - 280 + k * 190, 0.55, non)
    inflatable_snowman(ctx, NCX - 470, 0.85, non, lf, nsnow)
    inflatable_snowman(ctx, DCX - 450, 0.7, don, lf, dsnow)
    snowfall(ctx, lf)


def snowfall(ctx, lf):
    rnd = random.Random(21)
    for k in range(120):
        x0, y0, sp, r = rnd.uniform(-900, 3200), rnd.uniform(0, 2400), rnd.uniform(1.2, 3), rnd.uniform(4, 9)
        y = -300 + (y0 + lf * sp) % 2400
        x = x0 + 25 * math.sin(lf * 0.05 + k)
        ellipse(ctx, x, y, r, r); setc(ctx, (1, 1, 1, 0.8)); ctx.fill()


def ladder(ctx, x):
    for sx in (-60, 60):
        ctx.new_path(); ctx.move_to(x + sx, GND); ctx.line_to(x + sx * 0.7 - 30, 1040)
        setc(ctx, INK); ctx.set_line_width(26); ctx.stroke_preserve(); setc(ctx, hx('c0c8d8')); ctx.set_line_width(16); ctx.stroke()
    for k in range(1, 8):
        u = k / 8; y = lerp(GND, 1040, u)
        ctx.new_path(); ctx.move_to(x - 60 + u * 18 - 30 * u, y); ctx.line_to(x + 60 - u * 18 - 30 * u, y)
        setc(ctx, INK); ctx.set_line_width(16); ctx.stroke_preserve(); setc(ctx, hx('c0c8d8')); ctx.set_line_width(8); ctx.stroke()


def string_in_hands(ctx, a, b, lf):
    pts = [a, ((a[0] + b[0]) / 2, max(a[1], b[1]) + 70 + 10 * math.sin(lf * 0.5)), b]
    pts2 = resample(pts, 12)
    bulbs(ctx, pts2 + [b], lf, 1.0, 40, 2, 8)


# ------------------------------------------------------------------ shot 1: hook
LADX = 800


def ladder_dad(ctx, lf, hand=True):
    w = math.sin(lf * 0.9)
    p = P(eye='shock', mouth='scream', lsh=-170 + 10 * w, lel=0, rsh=170 - 10 * w, rel=0, torso=-6, head=-6 + 4 * w,
          lhip=-6, rhip=20, rkn=-40)
    d = stand(ctx, DAD, LADX - 20, 1.0, p, -1, 1440)
    sweat(ctx, d['head'][0] + d['R'] * 0.95, d['head'][1] - d['R'] * 0.5, lf, 1.0)
    sweat(ctx, d['head'][0] - d['R'] * 0.95, d['head'][1] - d['R'] * 0.2, lf + 40, 0.8)
    if hand:
        hx_, hy_ = d['front']
        bulbs(ctx, resample([(DCX + 400, 1080), (hx_, hy_), (hx_ + 30, 1300 + 10 * w), (SOCK, 1450)], 12), lf, 1.0, 40, 2, 8)
    return d


def hook(ctx, f, lf):
    z = 1.12 + 0.04 * eio(pop(lf, 0, 40))
    ctx.save(); cam(ctx, 610, 1230, z, 0, 3 + shake_at(lf, [0], 6, 8), f)
    street(ctx, lf, 5, 5, deer=1, nsnow=1, dsnow=1)
    ladder(ctx, LADX)
    kp = P(eye='happy', mouth='open', shades=1, lsh=-30, lel=-100, rsh=40, rel=-110, head=4)
    stand(ctx, KID, 300, 0.78, kp, 1)
    ladder_dad(ctx, lf)
    ctx.restore()


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    hook(ctx, f, lf)
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label(ctx, "\"MORE...", 540, 1385, 110, YEL, -0.04, t)
    label(ctx, "LIGHTS!!\"", 540, 1490, 136, WHITE, 0.03, t)


# ------------------------------------------------------------------ shot 2: one string -> neighbour KA-CHUNK
def beat1(ctx, f, il):
    # 0-10 Dad at socket with plug ; 10 *click* lights on ; 14-40 "PERFECT." ; 40-62 pan right ;
    # 64 KA-CHUNK neighbour ; 70-104 neighbour "Evening, NEIGHBOR!" ; 106-112 whip back ; 112-140 Dad glare
    if il < 40:
        cx, z = 760, 1.15
    elif il < 106:
        u = eio(pop(il, 40, 62)); cx, z = lerp(760, 1560, u), lerp(1.15, 1.0, u)
    else:
        u = eio(pop(il, 106, 112)); cx, z = lerp(1560, 800, u), lerp(1.0, 1.25, u)
    cy = 1240 if il < 106 else lerp(1240, 1340, pop(il, 106, 112))
    ctx.save(); cam(ctx, cx, cy, z, 0, shake_at(il, [64], 14, 22), f)
    don = 0 if il < 10 else 1
    non = 0 if il < 64 else (1 if il > 66 else 0.5)
    street(ctx, il, 1, 0 if il < 64 else 3, don, non, deer=eout(pop(il, 66, 78)))
    # Dad
    if il < 12:
        p = P(eye='normal', mouth='smile', lsh=60, lel=-40, rsh=70, rel=-30, torso=8)
        d = stand(ctx, DAD, SOCK - 150, 1.0, p, 1)
        plug(ctx, SOCK - 30 + 20 * pop(il, 0, 10), 1478, 0.5, 0)
    elif il < 106:
        p = P(eye='happy', mouth='grin', lsh=-40, lel=-80, rsh=-40, rel=-80, torso=-4) if il < 64 else \
            P(eye='shock', mouth='open', lsh=-20, lel=-60, rsh=40, rel=-50, head=8)
        d = stand(ctx, DAD, SOCK - 150, 1.0, p, 1 if il >= 64 else -1)
    else:
        w = math.sin(il * 1.3)
        p = P(eye='glare', mouth='flat', lsh=-30, lel=-110, rsh=30, rel=110, head=2 * w)
        d = stand(ctx, DAD, SOCK - 150, 1.0, p, 1)
        twitch(ctx, d['head'][0] + d['R'] * 0.8, d['head'][1] - d['R'] * 1.1, il, 1.0)
    # neighbour
    if il < 64:
        np_ = P(eye='smug', mouth='smile', lsh=40, lel=-60, rsh=50, rel=-40, torso=6)
    else:
        wv = math.sin(il * 0.5)
        np_ = P(eye='smug', mouth='grin', lsh=-30, lel=-80, rsh=-160 + 20 * wv, rel=-20 * wv, head=-4)
    stand(ctx, NB, NSOCK + 170, 1.0, np_, -1)
    ctx.restore()
    if il < 40:
        label(ctx, "*click*", 540, 470, 90, YEL, 0.04, pop(il, 10, 13))
        if il >= 16:
            label(ctx, "\"PERFECT.\"", 540, 1430, 120, WHITE, -0.03, pop(il, 16, 20))
    elif il < 64:
        label(ctx, "*glance*", 540, 1430, 90, CYAN, 0.03, pop(il, 44, 48))
    elif il < 106:
        label(ctx, "*KA-CHUNK!*", 540, 470, 120, YEL, -0.05, pop(il, 64, 67))
        if il >= 76:
            label(ctx, "\"Evening,", 540, 1385, 100, MINT, -0.03, pop(il, 76, 80))
            label(ctx, "NEIGHBOR!\"", 540, 1480, 120, MINT, 0.03, pop(il, 84, 88))
    else:
        label(ctx, "\"...oh, it's", 540, 1385, 100, WHITE, -0.03, pop(il, 113, 117))
        if il >= 120:
            label(ctx, "ON.\"", 540, 1490, 150, RED, 0.04, pop(il, 120, 123))


def s2(ctx, f):
    beat1(ctx, f, f - 60)


# ------------------------------------------------------------------ shot 3: split-screen light war
def war(ctx, f, il):
    # Dad: lv1 -> 2 @4 -> 3 @68 ; neighbour: lv3 -> 4 @36 -> 5 @100
    dlv = 1 + (il >= 4) + (il >= 68)
    nlv = 3 + (il >= 36) + (il >= 100)
    hits = [4, 36, 68, 100]
    for half, sy in ((0, 480), (1, 1440)):
        ctx.save(); ctx.rectangle(0, half * 960, W, 960); ctx.clip()
        mine = (half == 0 and il < 36) or (half == 0 and 68 <= il < 100) or (half == 1 and 36 <= il < 68) or (half == 1 and il >= 100)
        zz = 0.8 + (0.04 * (1 - pop(il % 32, 0, 10)) if mine else 0)
        tilt = (-5 if half == 0 else 5)
        cxh = DCX + 60 if half == 0 else NCX - 40
        ctx.save(); cam(ctx, cxh, 1250, zz, tilt, shake_at(il, [h for h in hits if (h in (4, 68)) == (half == 0)], 10, 16), f, 540, sy)
        street(ctx, il, dlv, nlv, deer=1, nsnow=1 if nlv >= 4 else 0, dsnow=1 if dlv >= 3 else 0)
        if half == 0:
            w = math.sin(il * 1.4)
            p = P(eye='glare', mouth='scream', lsh=150 + 20 * w, lel=0, rsh=-150 + 20 * w, rel=0, head=4 * w, lhip=-10, rhip=10)
            d = stand(ctx, DAD, SOCK - 140, 1.0, p, 1)
            string_in_hands(ctx, d['back'], d['front'], il)
            sweat(ctx, d['head'][0] + d['R'] * 0.95, d['head'][1] - d['R'] * 0.5, il, 1.0)
        else:
            p = P(eye='smug', mouth='grin', lsh=-30, lel=-80, rsh=-30, rel=-80, torso=-4, head=-6 + 4 * math.sin(il * 0.3))
            stand(ctx, NB, NSOCK + 160, 1.0, p, -1)
        ctx.restore()
        ctx.restore()
    rect_r(ctx, -10, 950, W + 20, 20, 0); setc(ctx, WHITE); ctx.fill()
    ctx.rectangle(-10, 946, W + 20, 4); setc(ctx, INK); ctx.fill(); ctx.rectangle(-10, 970, W + 20, 4); ctx.fill()
    words = [("MORE!", YEL, 4), ("MORE!!", MINT, 36), ("MORE!!!", RED, 68), ("...EVEN MORE.", CYAN, 100)]
    cur = [w_ for w_ in words if w_[2] <= il]
    if cur:
        s, c, t0 = cur[-1]
        label(ctx, s, 540, 990, 120, c, -0.04 if len(cur) % 2 else 0.04, pop(il, t0, t0 + 3))
    for t0 in hits:
        if t0 <= il < t0 + 14:
            y = 300 if t0 in (4, 68) else 1300
            label(ctx, "*KA-CHUNK!*", 540, y, 90, WHITE, 0.04, pop(il, t0, t0 + 3))


def s3(ctx, f):
    war(ctx, f, f - 200)


# ------------------------------------------------------------------ shot 4: the one close-up
def bokeh(ctx, lf):
    ctx.set_source(vgrad(ctx, 0, 0, 0, H, [(0, hx('14184a')), (1, hx('3b2a7e'))])); ctx.paint()
    rnd = random.Random(4)
    for k in range(40):
        x, y, r = rnd.uniform(-100, 1180), rnd.uniform(200, 1900), rnd.uniform(40, 110)
        c = BCOL[k % len(BCOL)]
        y += 20 * math.sin(lf * 0.05 + k)
        ellipse(ctx, x, y, r, r); setc(ctx, c[:3] + (0.28,)); ctx.fill()
        ellipse(ctx, x, y, r * 0.7, r * 0.7); setc(ctx, c[:3] + (0.18,)); ctx.fill()


def closeup(ctx, f, il):
    z = 1 + 0.06 * eio(il / 90)
    ctx.save(); cam(ctx, 540, 960, z, 2 * math.sin(il * 0.2), shake_at(il, [36], 10, 18) + 2, f)
    bokeh(ctx, il)
    w = math.sin(il * 1.2)
    p = P(eye='glare', mouth='flat' if il < 36 else 'scream', lsh=-20, lel=-100, rsh=120, rel=40, head=3 * w)
    # draw the body at the face() scale, then the plug in his raised hand
    b = doodle.draw_hip(scenes32_SCR, 0, 0, 1, 1, DAD, p)
    s = 200 / b['R']
    ctx.save(); ctx.translate(430, 860); ctx.scale(s, s); ctx.translate(-b['head'][0], -b['head'][1])
    d = doodle.draw_hip(ctx, 0, 0, 1, 1, DAD, p)
    ctx.restore()
    hx_, hy_ = 430 + (d['front'][0] - b['head'][0]) * s, 860 + (d['front'][1] - b['head'][1]) * s
    plug(ctx, hx_ + 150, hy_ - 110, 1.3, 0.25, (1300, 2000))
    if il >= 36:
        for k in range(6):
            a = k * 1.05 + il * 0.3
            sparkle(ctx, hx_ + 150 + 150 * math.cos(a), hy_ - 140 + 150 * math.sin(a), 22, YEL)
    sweat(ctx, 430 - 230, 860 - 120, il, 1.4)
    if il >= 36:
        twitch(ctx, 430 - 170, 860 - 220, il, 1.5)
    ctx.restore()
    label(ctx, "\"I... WILL...", 540, 1400, 110, WHITE, -0.03, pop(il, 4, 8))
    if il >= 36:
        label(ctx, "...WIN!!\"", 540, 1510, 150, RED, 0.04, pop(il, 36, 39))


def s4(ctx, f):
    closeup(ctx, f, f - 330)


# ------------------------------------------------------------------ shot 5: mega plug -> blackout -> candle
def dark_layer(ctx, a, holes=()):
    ctx.push_group()
    ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, (0.02, 0.02, 0.08, a)); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_DEST_OUT)
    for (x, y, r, s) in holes:
        g = cairo.RadialGradient(x, y, 0, x, y, r)
        g.add_color_stop_rgba(0, 0, 0, 0, s); g.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.set_source(g); ctx.arc(x, y, r, 0, 7); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.pop_group_to_source(); ctx.paint()


def glow_eyes(ctx, d, blink=False, s=1.0):
    for k in ('eyeL', 'eyeR'):
        x, y = d[k]
        if blink:
            ctx.new_path(); ctx.move_to(x - 14 * s, y); ctx.line_to(x + 14 * s, y); setc(ctx, WHITE); ctx.set_line_width(5 * s); ctx.stroke()
        else:
            ellipse(ctx, x, y, 15 * s, 19 * s); setc(ctx, WHITE); ctx.fill()
            ellipse(ctx, x + 2 * s, y + 3 * s, 7 * s, 9 * s); setc(ctx, INK); ctx.fill()


def finale(ctx, f, il):
    # 0-14 Dad with giant plug ; 14 KA-CHUNK!! mega ; 30-60 pull wide ; 40-70 neighbour shades "okay. You WIN." ;
    # 60-75 "YESSS!!" ; 75-105 card ; 80 bzzzt flicker ; 96 POP dark ; 100-130 eyes "...honey?" ;
    # 130 candle ; 140-175 Mom "Who wants COCOA?" ; 175-210 push in on Dad's eyes "...I need MORE LIGHTS."
    if il < 30:
        cx, cy, z = 820, 1260, 1.05
    elif il < 100:
        u = eio(pop(il, 30, 52)); cx, cy, z = lerp(820, 1120, u), lerp(1260, 1260, u), lerp(1.05, 0.62, u)
    elif il < 175:
        u = eio(pop(il, 112, 136)); cx, cy, z = lerp(1120, 470, u), lerp(1260, 1330, u), lerp(0.62, 1.3, u)
    else:
        u = eio(pop(il, 175, 186)); cx, cy, z = lerp(470, SOCK - 120, u), lerp(1330, 1160, u), lerp(1.3, 1.7, u)
    ctx.save(); cam(ctx, cx, cy, z, 0, shake_at(il, [14, 96], 14, 26), f)
    blackout = il >= 96
    fl_ = 1.0
    if 80 <= il < 96:
        fl_ = 1.0 if (il // 2) % 2 == 0 else 0.25
    don = 0 if blackout else fl_
    non = 0 if blackout else fl_
    dlv = 3 if il < 14 else 6
    street(ctx, il, dlv, 5, don, non, lamp_on=0 if blackout else fl_, deer=1, nsnow=1, dsnow=1,
           mom=P(eye='happy', mouth='smile', lsh=-20, lel=-120, rsh=40, rel=-110) if il >= 128 else None,
           candle=eout(pop(il, 130, 136)), win=0 if blackout else 1)
    if 14 <= il < 96:
        rays(ctx, DCX, 1100, 200, 1600, il * 0.01, (1, 1, 0.8), 0.45 * fl_, 16)
    # Dad
    if il < 14:
        p = P(eye='glare', mouth='flat', lsh=-20, lel=-60, rsh=60, rel=-30, torso=10)
        dd = stand(ctx, DAD, SOCK - 160, 1.0, p, 1)
        plug(ctx, SOCK - 10, 1440 - 40 * (1 - pop(il, 6, 14)), 0.7, 0, (SOCK - 400, GND - 20))
    elif il < 96:
        jump = abs(math.sin((il - 60) * 0.35)) * 60 if il >= 60 else 0
        p = P(eye='happy', mouth='scream', lsh=-160, lel=-10, rsh=160, rel=10, head=-6) if il >= 60 else \
            P(eye='shock', mouth='grin', lsh=-40, lel=-80, rsh=-40, rel=-80)
        dd = stand(ctx, DAD, SOCK - 160, 1.0, p, 1, GND - jump)
    else:
        p = P(eye='shock', mouth='flat', lsh=10, lel=-10, rsh=-10, rel=-10)
        dd = stand(ctx, DAD, SOCK - 160, 1.0, p, 1)
    # kid
    kp = P(eye='happy', mouth='open', shades=1, lsh=-150, lel=0, rsh=150, rel=0) if 14 <= il < 96 else \
        P(eye='shock', mouth='open', lsh=10, lel=-20, rsh=-10, rel=-20)
    kd = stand(ctx, KID, 590, 0.74, kp, 1)
    # neighbour
    if il < 40:
        np_ = P(eye='smug', mouth='grin', lsh=-30, lel=-80, rsh=-30, rel=-80)
    elif il < 96:
        np_ = P(eye='closed' if il < 50 else 'normal', mouth='wavy', shades=1 if il >= 50 else 0,
                lsh=-150 if il < 50 else 20, lel=-30 if il < 50 else -20, rsh=-150 if il < 50 else 50, rel=-30 if il < 50 else -40)
    else:
        np_ = P(eye='shock', mouth='flat', lsh=10, lel=-10, rsh=-10, rel=-10)
    nd = stand(ctx, NB, NSOCK + 200, 1.0, np_, -1)
    if 14 <= il < 22:
        ctx.rectangle(-3000, -3000, 9000, 9000); setc(ctx, (1, 1, 0.9, 0.7 * (1 - (il - 14) / 8))); ctx.fill()
    if blackout:
        a = 0.9 * eout(pop(il, 96, 100))
        holes = []
        if il >= 130:
            holes.append((DCX - 165, 1240, 260 * eout(pop(il, 130, 138)), 0.95))
        dark_layer(ctx, a, holes)
        for d_, sd, sc in ((dd, 0, 1.0), (kd, 2, 0.8), (nd, 4, 1.0)):
            glow_eyes(ctx, d_, (il + sd * 13) % 60 < 4, sc)
    ctx.restore()
    if 75 <= il < 105:
        card(ctx, 'p2', il, 75, 105)
    if 14 <= il < 40:
        label(ctx, "*KA-CHUNK!!*", 540, 470, 130, YEL, -0.05, pop(il, 14, 17))
    elif 40 <= il < 60:
        label(ctx, "\"...okay.", 540, 1385, 100, MINT, -0.03, pop(il, 42, 46))
        label(ctx, "You WIN.\"", 540, 1480, 120, MINT, 0.03, pop(il, 50, 54))
    elif 60 <= il < 80:
        label(ctx, "\"YESSS!!\"", 540, 1430, 150, YEL, 0.04, pop(il, 61, 64))
    elif 80 <= il < 96:
        label(ctx, "*bzzzt...*", 540, 1430, 110, CYAN, 0.04, pop(il, 80, 83))
    elif 96 <= il < 128:
        label(ctx, "*POP!*", 540, 1380, 140, WHITE, -0.05, pop(il, 96, 99))
        if il >= 108:
            label(ctx, "\"...honey?\"", 540, 1500, 100, WHITE, 0.03, pop(il, 108, 112))
    elif 128 <= il < 175:
        label(ctx, "*fwip*", 540, 470, 80, GOLD, 0.04, pop(il, 130, 133))
        if il >= 142:
            label(ctx, "\"Who wants", 540, 1385, 100, PINK, -0.03, pop(il, 142, 146))
            label(ctx, "COCOA?\"", 540, 1480, 130, PINK, 0.03, pop(il, 148, 152))
    elif il >= 175:
        label(ctx, "\"...I need", 540, 1385, 100, WHITE, -0.03, pop(il, 182, 186))
        if il >= 190:
            label(ctx, "MORE LIGHTS.\"", 540, 1490, 120, YEL, 0.03, pop(il, 190, 194))


def s5(ctx, f):
    lf = f - 420
    if lf < 210:
        finale(ctx, f, lf)
    else:
        s1(ctx, f, f - 630)


import scenes32 as _s32
scenes32_SCR = _s32._SCR
SHOTS = [(0, s1), (60, s2), (200, s3), (330, s4), (420, s5)]
CUTS = (60, 200, 330, 420, 630)


def render(f):
    import sketch
    sketch.BOIL[0] = f // 4
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.1, 0.05, 0.15, 0.16)
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
                              "-i", "out/lights_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
