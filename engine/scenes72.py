"""'The Robot Vacuum' - Dad's new robot vacuum. Original, general-audience comedy short, 22s.
Hook: Dad ECU mid-scream, caption "Dad's NEW ROBOT VACUUM:" + "IT ATE MY SOCK!!", smug vacuum burping below.
Beat 1: low angle Dad holds it up "It cleans... BY ITSELF!" *beep boop* -> overhead top-down room cam: BONK sofa,
        BONK wall, BONK table leg, stuck spinning in the corner -> "...it's LEARNING."
Beat 2: floor-level: vacuum eats Dad's sock off his foot *SHLUUURP!* "MY SOCK!!" -> eats the kid's homework off the table
        "The VACUUM ate my HOMEWORK!" (true for once) -> split: eats the car keys / Dad twitch "...my KEYS."
Twist:  Dad flips it over "GIVE. IT. BACK." *CLICK* -> *PFOOOMP!!* dust explosion of socks, keys, remote, duck ->
        dusty Dad buried in a mountain of single socks, Mom + kid: "So THAT'S where the socks GO!"
End:    "...GOOD vacuum." *pat pat* -> floor-level: Dad's OTHER sock, vacuum eyes turn red -> "...don't you DARE."
        -> *SHLUUURP!* -> loop to the hook."""
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


DAD = dict(doodle.DAD, shirt=hx('ff8a1f'), pants=hx('3d5a9e'))
DUSTY = dict(DAD, shirt=hx('a9a4b0'), pants=hx('8e8a96'), skin=hx('c9c4cc'), hair=hx('9a96a0'))
BOY = dict(doodle.BOY, hood=False, shades=False, shirt=hx('22b45a'), pants=hx('2a3a6a'))
MOM = dict(doodle.MOM_G, shirt=hx('9b4dff'), pants=hx('3d5a9e'))
N = 660
RED = hx('ff3b5c'); PINK = hx('ff5fa8'); ORANGE = hx('ff8a1f'); PURPLE = hx('8a3cff'); GREEN = hx('22b45a')
BLUE = hx('1f8bff'); YEL = hx('fff27a'); GOLD = hx('ffc93c'); WHITE = (1, 1, 1); CYAN = hx('7fe3ff')
SOCKC = [(hx('ff3b5c'), hx('ffffff')), (hx('1f8bff'), hx('fff27a')), (hx('22b45a'), hx('ffffff')), (hx('ff5fa8'), hx('8a3cff')),
         (hx('ffc93c'), hx('ff3b5c')), (hx('8a3cff'), hx('7fe3ff')), (hx('ffffff'), hx('ff8a1f'))]
FLOOR = 1500
KK, DK, MK = 0.95, 1.4, 1.35
SKIN = doodle.DAD['skin']

CAPS = {'p1': [[("Dad's NEW ", OUT), ("ROBOT VACUUM:", BLUE)]]}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def vac_eyes(ctx, x, y, r, mood, lf):
    """two LED eyes centred at (x, y), r = eye radius"""
    col = RED if mood == 'angry' else CYAN
    for dx in (-1, 1):
        ex = x + dx * r * 1.6
        if mood == 'happy':
            ctx.new_path(); ctx.arc(ex, y + r * 0.3, r, math.pi * 1.1, math.pi * 1.9)
            setc(ctx, col); ctx.set_line_width(r * 0.55); ctx.stroke()
        elif mood == 'angry':
            poly(ctx, [(ex - r, y - r * 0.5 - dx * r * 0.4 * -1), (ex + r, y - r * 0.5 + dx * r * 0.4 * -1), (ex + r, y + r * 0.6), (ex - r, y + r * 0.6)])
            setc(ctx, col); ctx.fill()
            ctx.new_path(); ctx.arc(ex, y, r * 1.8, 0, 2 * math.pi); setc(ctx, (1, 0.2, 0.3, 0.25)); ctx.fill()
        else:
            bl = (lf % 50) < 3
            ellipse(ctx, ex, y, r, r * (0.15 if bl else 1)); setc(ctx, col); ctx.fill()
            ellipse(ctx, ex + r * 0.3, y - r * 0.35, r * 0.3, r * 0.3); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()


def vac_side(ctx, x, ground, s, d, lf, mood='normal', spin=True):
    """side view robot vacuum; d=+1 faces right"""
    ctx.save(); ctx.translate(x, ground); ctx.scale(s * d, s)
    w, h = 200, 58
    ellipse(ctx, 0, 4, w * 0.55, 10); setc(ctx, (0, 0, 0, 0.18)); ctx.fill()
    rect_r(ctx, -w / 2, -h - 8, w, h, 26); fl(ctx, hx('3a3f52'), 6)
    rect_r(ctx, -w / 2 + 10, -h - 8, w - 20, 16, 8); fl(ctx, hx('5c6480'), 4)
    # bumper
    ctx.new_path(); ctx.arc(w / 2 - 24, -h / 2 - 8, h / 2, -math.pi / 2, math.pi / 2); fl(ctx, hx('ffc93c'), 5)
    # wheel
    ctx.new_path(); ctx.arc(-30, -6, 16, 0, 2 * math.pi); fl(ctx, hx('22222a'), 4)
    a = lf * 0.8 if spin else 0
    ctx.move_to(-30 + 12 * math.cos(a), -6 + 12 * math.sin(a)); ctx.line_to(-30 - 12 * math.cos(a), -6 - 12 * math.sin(a)); ink(ctx, 3); ctx.stroke()
    # brush
    for k in range(5):
        aa = a * 1.5 + k * 1.256
        ctx.move_to(w / 2 - 10, -4); ctx.line_to(w / 2 - 10 + 22 * math.cos(aa), -4 + 8 * math.sin(aa))
    ink(ctx, 3); ctx.stroke()
    # eyes (on the front half, readable from the side)
    ctx.save(); ctx.translate(w * 0.16, -h / 2 - 10); ctx.scale(d, 1)
    vac_eyes(ctx, 0, 0, 10, mood, lf)
    ctx.restore()
    # antenna light
    ctx.move_to(-40, -h - 8); ctx.line_to(-48, -h - 30); ink(ctx, 4); ctx.stroke()
    ctx.new_path(); ctx.arc(-48, -h - 34, 7, 0, 2 * math.pi)
    fl(ctx, RED if (mood == 'angry' or (lf // 8) % 2) else GREEN, 3)
    ctx.restore()


def vac_top(ctx, x, y, s, ang, lf, mood='normal'):
    """top-down robot vacuum, front points along ang"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(6, 8, 96, 0, 2 * math.pi); setc(ctx, (0, 0, 0, 0.2)); ctx.fill()
    ctx.new_path(); ctx.arc(0, 0, 92, 0, 2 * math.pi); fl(ctx, hx('3a3f52'), 7)
    ctx.new_path(); ctx.arc(0, 0, 92, -1.1, 1.1); setc(ctx, hx('ffc93c')); ctx.set_line_width(14); ctx.stroke()
    ctx.new_path(); ctx.arc(0, 0, 50, 0, 2 * math.pi); fl(ctx, hx('5c6480'), 5)
    ctx.save(); ctx.rotate(math.pi / 2)
    vac_eyes(ctx, 0, -62, 11, mood, lf)
    ctx.restore()
    for k in range(5):
        aa = lf * 1.2 + k * 1.256
        ctx.move_to(60, 60); ctx.line_to(60 + 30 * math.cos(aa), 60 + 30 * math.sin(aa))
        ctx.move_to(60, -60); ctx.line_to(60 + 30 * math.cos(-aa), -60 + 30 * math.sin(-aa))
    ink(ctx, 4); ctx.stroke()
    ctx.restore()


def sock(ctx, x, y, s, a, col=0, stretch=1.0):
    c1, c2 = SOCKC[col % len(SOCKC)]
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    pts = [(0, -60 * stretch), (0, 20), (10, 40), (48, 46)]

    def path():
        ctx.new_path(); ctx.move_to(*pts[0]); ctx.line_to(*pts[1]); ctx.curve_to(0, 36, 10, 46, *pts[3])
    path(); setc(ctx, INK); ctx.set_line_width(40); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    path(); setc(ctx, c1); ctx.set_line_width(28); ctx.stroke()
    for k in range(3):
        yy = -50 * stretch + k * 18 * stretch
        ctx.move_to(-13, yy); ctx.line_to(13, yy)
    setc(ctx, c2); ctx.set_line_width(7); ctx.stroke()
    ctx.set_line_cap(cairo.LINE_CAP_BUTT)
    ctx.restore()


def keys(ctx, x, y, s, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 22, 0, 2 * math.pi); ink(ctx, 6); ctx.stroke()
    for k, (ang, c) in enumerate(((0.5, GOLD), (1.4, hx('c9ced8')))):
        ctx.save(); ctx.rotate(ang)
        rect_r(ctx, 20, -16, 34, 32, 10); fl(ctx, c, 4)
        poly(ctx, [(52, -6), (110, -6), (110, 2), (100, 2), (100, 10), (90, 10), (90, 2), (52, 6)]); fl(ctx, c, 4)
        ctx.restore()
    ctx.restore()


def paper(ctx, x, y, s, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-50, -64), (50, -64), (50, 64), (-50, 64)]); fl(ctx, WHITE, 4)
    for k in range(5):
        ctx.move_to(-36, -40 + k * 20); ctx.line_to(36 - (k % 2) * 20, -40 + k * 20)
    setc(ctx, hx('7fa8ff')); ctx.set_line_width(4); ctx.stroke()
    text(ctx, "A+", 18, 52, 30, RED, ow=0, shadow=False)
    ctx.restore()


def remote(ctx, x, y, s, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -24, -70, 48, 140, 14); fl(ctx, hx('2a2a36'), 4)
    ctx.new_path(); ctx.arc(0, -46, 9, 0, 2 * math.pi); setc(ctx, RED); ctx.fill()
    for k in range(6):
        ellipse(ctx, -10 + 20 * (k % 2), -14 + 20 * (k // 2), 6, 6); setc(ctx, hx('c9ced8')); ctx.fill()
    ctx.restore()


def duck(ctx, x, y, s, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ellipse(ctx, 0, 10, 46, 32); fl(ctx, hx('ffd23f'), 4)
    ctx.new_path(); ctx.arc(26, -26, 24, 0, 2 * math.pi); fl(ctx, hx('ffd23f'), 4)
    poly(ctx, [(46, -28), (70, -22), (46, -16)]); fl(ctx, ORANGE, 3)
    ellipse(ctx, 32, -32, 4, 5); setc(ctx, INK); ctx.fill()
    ctx.restore()


def puff(ctx, x, y, r, a=1.0, col=(0.78, 0.76, 0.8)):
    for dx, dy, k in ((0, 0, 1), (-0.6, 0.2, 0.75), (0.6, 0.15, 0.8), (-0.25, -0.45, 0.7), (0.3, -0.4, 0.65)):
        ctx.new_path(); ctx.arc(x + dx * r, y + dy * r, r * k, 0, 2 * math.pi)
        setc(ctx, (col[0], col[1], col[2], a)); ctx.fill()


def room(ctx, lf, wall=hx('ffe3a3'), floor=hx('d9a066')):
    ctx.rectangle(-2000, -2000, 5000, 5000); setc(ctx, wall); ctx.fill()
    for k in range(-8, 20):
        ctx.rectangle(k * 140, -2000, 60, 3500); setc(ctx, dark(wall, 0.96)); ctx.fill()
    # window
    rect_r(ctx, 640, 520, 330, 380, 16); fl(ctx, hx('8fd8ff'), 9)
    ctx.move_to(805, 520); ctx.line_to(805, 900); ctx.move_to(640, 710); ctx.line_to(970, 710); ink(ctx, 8); ctx.stroke()
    # frame
    ctx.save(); ctx.translate(250, 640); ctx.rotate(-0.04)
    rect_r(ctx, -110, -90, 220, 180, 10); fl(ctx, hx('ff5fa8'), 8)
    ctx.new_path(); ctx.arc(-20, 10, 40, 0, 2 * math.pi); fl(ctx, YEL, 5)
    ctx.restore()
    ctx.rectangle(-2000, FLOOR - 50, 5000, 50); fl(ctx, WHITE, 6)
    ctx.rectangle(-2000, FLOOR, 5000, 2000); setc(ctx, floor); ctx.fill()
    for k in range(6):
        ctx.move_to(-2000, FLOOR + 40 + k * 70 + k * k * 8); ctx.line_to(3000, FLOOR + 40 + k * 70 + k * k * 8)
    setc(ctx, dark(floor, 0.85)); ctx.set_line_width(5); ctx.stroke()
    ctx.move_to(-2000, FLOOR); ctx.line_to(3000, FLOOR); ink(ctx, 7); ctx.stroke()


def floor_level(ctx, lf, horizon=1120):
    """low floor-level camera background"""
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffe3a3')); ctx.fill()
    ctx.rectangle(-500, horizon - 70, 2200, 70); fl(ctx, WHITE, 6)
    ctx.rectangle(-500, horizon, 2200, 1500); setc(ctx, hx('d9a066')); ctx.fill()
    for k in range(8):
        yy = horizon + 30 + k * 40 + k * k * 14
        ctx.move_to(-500, yy); ctx.line_to(1700, yy)
    setc(ctx, hx('c48a52')); ctx.set_line_width(5); ctx.stroke()
    for k in range(-6, 12):
        ctx.move_to(540 + k * 30, horizon); ctx.line_to(540 + k * 420, 2200)
    setc(ctx, (0.75, 0.5, 0.3, 0.35)); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-500, horizon); ctx.line_to(1700, horizon); ink(ctx, 6); ctx.stroke()


def leg_foot(ctx, lf, sock_col=0, sock_on=1.0, toes=False, pants=None):
    """Dad's leg from the top-left to a foot on the floor; sock_on 1 = full sock, 0 = bare"""
    pants = pants or DAD['pants']
    ctx.move_to(-120, 560); ctx.curve_to(120, 760, 230, 980, 300, 1170)
    setc(ctx, INK); ctx.set_line_width(170); ctx.stroke()
    ctx.move_to(-120, 560); ctx.curve_to(120, 760, 230, 980, 300, 1170)
    setc(ctx, pants); ctx.set_line_width(152); ctx.stroke()
    # foot
    wig = 0.08 * math.sin(lf * 1.3) if toes else 0
    ctx.save(); ctx.translate(320, 1250); ctx.rotate(wig)
    ctx.new_path(); ctx.move_to(-70, -110); ctx.line_to(60, -110); ctx.curve_to(70, -40, 150, -50, 230, -30)
    ctx.curve_to(290, -10, 290, 60, 220, 66); ctx.line_to(-60, 66); ctx.curve_to(-110, 60, -100, -40, -70, -110); ctx.close_path()
    if sock_on > 0.5:
        c1, c2 = SOCKC[sock_col]
        fl(ctx, c1, 8)
        for k in range(3):
            ctx.move_to(-78, -90 + k * 34); ctx.line_to(62, -90 + k * 34)
        setc(ctx, c2); ctx.set_line_width(14); ctx.stroke()
    else:
        fl(ctx, SKIN, 8)
        for k in range(5):
            tx = 215 - k * 16 + 30; ty = 20 - k * 12
            ctx.new_path(); ctx.arc(tx + 10 * math.sin(lf * 1.7 + k) * (1 if toes else 0), ty - 30, 22 - k * 2, 0, 2 * math.pi); fl(ctx, SKIN, 5)
    ctx.restore()
    # cuff
    rect_r(ctx, 200, 1090, 210, 70, 20); fl(ctx, dark(pants, 0.85), 7)


# ------------------------------------------------------------------ hook
def dad_scream(ctx, f, lf, z0=1.0):
    ctx.save(); cam(ctx, 540, 960, z0, 0, 7 if lf < 12 else 3, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff5f7a')); ctx.fill()
    rays(ctx, 540, 900, 260, 1420, lf * 0.03, col=(1, 1, 1), a=0.25, n=18)
    face(ctx, DAD, P(eye='shock', mouth='open'), 540, 860, 290, 0.03 * math.sin(lf * 1.9))
    twitch(ctx, 540 + 0.6 * 290, 860 - 0.75 * 290, lf, 1.4)
    sweat(ctx, 540 - 0.95 * 290, 820, lf, 1.3)
    ctx.restore()
    # smug vacuum bottom-right, burping
    vac_side(ctx, 830 + 8 * math.sin(lf * 0.5), 1250, 1.4, -1, lf, 'happy')
    if lf % 40 < 14:
        label(ctx, "*burp*", 840, 1110, 50, WHITE, 0.1, 1)


def s1(ctx, f, lf=None):
    lf = f if lf is None else lf
    dad_scream(ctx, f, lf, 1.02 + 0.06 * eio(pop(lf, 0, 54)))
    card(ctx, 'p1', f, -6 if lf == f else f - lf - 6)
    t = 1 if lf == f else pop(lf, 0, 3)
    label2(ctx, "\"IT ATE", "MY SOCK!!\"", WHITE, t, 124, col2=YEL, y=1400)


# ------------------------------------------------------------------ beat 1
WAY = [(0, 540, 1380, -1.57), (12, 540, 760, -1.57), (18, 540, 860, -1.57), (22, 540, 860, 0), (32, 930, 860, 0), (36, 860, 860, 2.3),
       (48, 720, 1080, 2.3), (52, 760, 1040, 2.6), (64, 170, 1350, 2.6)]
BONKS = [12, 32, 48]


def path_at(il):
    for a, b in zip(WAY, WAY[1:]):
        if il <= b[0]:
            t = (il - a[0]) / max(1, b[0] - a[0])
            return lerp(a[1], b[1], t), lerp(a[2], b[2], t), lerp(a[3], b[3], t)
    l = WAY[-1]
    return l[1], l[2], l[3] + (il - l[0]) * 0.7


def overhead(ctx, f, il):
    ctx.save(); cam(ctx, 540, 1000, 1.0, 0, shake_at(il, BONKS, 10, 6), f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('5a4a6a')); ctx.fill()
    ctx.rectangle(40, 380, 1000, 1150); setc(ctx, hx('d9a066')); ctx.fill()
    for k in range(9):
        ctx.move_to(40 + k * 125, 380); ctx.line_to(40 + k * 125, 1530)
    setc(ctx, hx('c48a52')); ctx.set_line_width(5); ctx.stroke()
    ctx.rectangle(40, 380, 1000, 1150); ink(ctx, 14); ctx.stroke()
    # rug
    ellipse(ctx, 560, 1000, 300, 200); fl(ctx, hx('7fe3ff'), 7)
    ellipse(ctx, 560, 1000, 200, 120); fl(ctx, hx('b6f0ff'), 5)
    # sofa (top)
    rect_r(ctx, 260, 400, 560, 240, 40); fl(ctx, hx('9b4dff'), 8)
    rect_r(ctx, 300, 470, 480, 150, 26); fl(ctx, hx('b47bff'), 6)
    # table + legs (right)
    rect_r(ctx, 640, 1110, 280, 180, 14); setc(ctx, (0.45, 0.28, 0.15, 0.35)); ctx.fill()
    for lx, ly in ((660, 1130), (900, 1130), (660, 1270), (900, 1270)):
        ctx.new_path(); ctx.arc(lx, ly, 18, 0, 2 * math.pi); fl(ctx, hx('8a5a3a'), 5)
    # plant
    ctx.new_path(); ctx.arc(960, 470, 70, 0, 2 * math.pi); fl(ctx, GREEN, 7)
    ctx.new_path(); ctx.arc(960, 470, 30, 0, 2 * math.pi); fl(ctx, hx('5fd86f'), 4)
    # trail
    ctx.new_path()
    for k in range(0, min(il, 64) + 1, 2):
        x, y, _ = path_at(k)
        (ctx.move_to if k == 0 else ctx.line_to)(x, y)
    setc(ctx, (1, 1, 1, 0.35)); ctx.set_line_width(30); ctx.stroke()
    x, y, a = path_at(il)
    mood = 'angry' if any(b <= il < b + 6 for b in BONKS) else 'normal'
    vac_top(ctx, x, y, 1.2, a, il, mood)
    for b in BONKS:
        if b <= il < b + 10:
            bx, by, ba = path_at(b)
            sparkle(ctx, bx + 95 * math.cos(ba), by + 95 * math.sin(ba), 60 * (1 - (il - b) / 10) + 20, YEL)
    if il >= 64:
        for k in range(3):
            aa = il * 0.5 + k * 2.1
            ctx.new_path(); ctx.arc(170, 1350, 130 + k * 12, aa, aa + 0.8); setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()


def s2(ctx, f):
    lf = f - 54
    if lf < 50:
        ctx.save(); cam(ctx, 540, 1120, 1.12 + 0.05 * eio(pop(lf, 0, 50)), -4, 0, f)
        room(ctx, lf)
        rays(ctx, 540, 520, 160, 1200, lf * 0.04, col=(1, 1, 1), a=0.3, n=16)
        b = draw(ctx, 540, FLOOR - 186 * 1.8, 1.8, 1, DAD, P(eye='smug', mouth='grin', lsh=165, rsh=-165, lel=-15, rel=15))
        hy = (b['front'][1] + b['back'][1]) / 2
        vac_side(ctx, 540, hy - 175 + 6 * math.sin(lf * 0.3), 1.6, 1, lf, 'happy')
        ctx.restore()
        for k, (sx, sy) in enumerate(((200, 520), (880, 480), (300, 860), (820, 900))):
            sparkle(ctx, sx, sy, 30 + 12 * math.sin(lf * 0.4 + k), YEL)
        label(ctx, "*beep boop!*", 540, 330, 96, CYAN, -0.04, pop(lf, 2, 5))
        label2(ctx, "\"It cleans...", "BY ITSELF!\"", WHITE, pop(lf, 6, 10), 116, col2=YEL, y=1400)
    else:
        il = lf - 50   # 0..96
        overhead(ctx, f, il)
        words = ["*BONK!*", "*BONK!!*", "*BONK!!!*"]
        for k, b in enumerate(BONKS):
            if b <= il < (BONKS[k + 1] if k + 1 < len(BONKS) else 64):
                label(ctx, words[k], 540, 300, 110 + 10 * k, YEL, -0.05 + 0.05 * k, pop(il, b, b + 3))
        if il >= 66:
            label(ctx, "*whirr whirr whirr*", 540, 300, 80, WHITE, 0.03, pop(il, 64, 67))
            label(ctx, "\"...it's LEARNING.\"", 540, 1440, 110, YEL, -0.04, pop(il, 70, 74))


# ------------------------------------------------------------------ beat 2
def sock_steal(ctx, f, il, col, pull_at, label_top=True, mood0='normal', mood_eat='happy', start_x=1300):
    """floor-level: vacuum drives in and slurps the sock off the foot. returns nothing"""
    ctx.save(); cam(ctx, 540, 960, 1.0, 0, shake_at(il, [pull_at + 8], 10, 10), f)
    floor_level(ctx, il)
    off = il >= pull_at + 8
    leg_foot(ctx, il, col, 0 if off else 1, toes=off)
    vx = lerp(start_x, 760, eout(pop(il, 0, pull_at)))
    if pull_at <= il < pull_at + 8:
        t = (il - pull_at) / 8
        # stretched sock between toe and vacuum mouth
        x0, x1 = 520, vx - 150
        ctx.move_to(x0, 1260); ctx.curve_to(lerp(x0, x1, 0.3), 1240 - 30 * t, lerp(x0, x1, 0.7), 1290, x1, 1300)
        c1, c2 = SOCKC[col]
        setc(ctx, INK); ctx.set_line_width(70 - 30 * t); ctx.stroke()
        ctx.move_to(x0, 1260); ctx.curve_to(lerp(x0, x1, 0.3), 1240 - 30 * t, lerp(x0, x1, 0.7), 1290, x1, 1300)
        setc(ctx, c1); ctx.set_line_width(54 - 30 * t); ctx.stroke()
    elif pull_at + 8 <= il < pull_at + 14:
        t = (il - pull_at - 8) / 6
        sock(ctx, lerp(vx - 200, vx - 120, t), 1290, 2.0 * (1 - t) + 0.2, 1.4 + t * 3, col)
    mood = mood0 if il < pull_at else mood_eat
    vac_side(ctx, vx, 1330, 2.6, -1, il, mood)
    if pull_at <= il < pull_at + 14:
        for k in range(5):
            yy = 1200 + k * 30
            ctx.move_to(vx - 200 - ((il * 40 + k * 60) % 300), yy); ctx.line_to(vx - 150, 1290)
        setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()


def homework(ctx, f, il):
    ctx.save(); cam(ctx, 560, 1240, 1.12, 0, shake_at(il, [16], 6, 8), f)
    room(ctx, il, wall=hx('c9f0d0'))
    # table
    rect_r(ctx, 120, 1120, 520, 40, 12); fl(ctx, hx('c98a4a'), 7)
    for lx in (160, 580):
        ctx.rectangle(lx, 1160, 30, FLOOR - 1160); fl(ctx, hx('a86e3a'), 6)
    shock = il >= 10
    draw(ctx, 790, FLOOR - 186 * KK, KK, -1, BOY, P(eye='shock' if shock and il < 26 else ('smug' if shock else 'normal'),
                                                   mouth='open' if shock and il < 26 else ('grin' if shock else 'smile'),
                                                   lsh=40 if il < 26 else 150, rsh=-40 if il < 26 else -150, lel=-20, rel=20))
    vx = lerp(-200, 380, eout(pop(il, 0, 10)))
    vac_side(ctx, vx, FLOOR, 1.5, 1, il, 'happy' if il >= 18 else 'normal')
    t = clamp((il - 8) / 10)
    if t < 1:
        px = lerp(480, vx + 150, t * t); py = lerp(1100, FLOOR - 50, t * t) + 0 * t
        paper(ctx, px, py, 1.3 * (1 - 0.7 * t), -0.3 + t * 5)
    if 8 <= il < 20:
        for k in range(4):
            ctx.move_to(vx + 160, FLOOR - 40); ctx.line_to(vx + 260 + k * 40, FLOOR - 200 - k * 40)
        setc(ctx, (1, 1, 1, 0.7)); ctx.set_line_width(6); ctx.stroke()
    ctx.restore()
    label(ctx, "*SHLURP!*", 540, 330, 110, CYAN, -0.05, pop(il, 14, 17))
    if il >= 22:
        label2(ctx, "\"The VACUUM ate", "my HOMEWORK!\"", WHITE, pop(il, 22, 26), 96, col2=GREEN, y=1400)


def keys_split(ctx, f, il):
    ctx.save(); ctx.rectangle(0, 0, W, H / 2); ctx.clip()
    ctx.save(); cam(ctx, 600, 1200, 1.15, 0, 0, f, sy=620)
    floor_level(ctx, il, 1050)
    vx = lerp(1300, 620, eout(pop(il, 0, 12)))
    if il < 16:
        t = clamp((il - 8) / 8)
        keys(ctx, lerp(380, vx - 180, t * t), 1240 - 30 * math.sin(math.pi * t), 1.6 * (1 - 0.6 * t), il * 0.4 * t)
    vac_side(ctx, vx, 1300, 2.2, -1, il, 'happy' if il >= 16 else 'normal')
    ctx.restore()
    ctx.restore()
    ctx.save(); ctx.rectangle(0, H / 2, W, H / 2); ctx.clip()
    ctx.translate(0, 360)
    ctx.save(); cam(ctx, 540, 960, 0.8, 0, 2, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb347')); ctx.fill()
    rays(ctx, 540, 900, 260, 1420, il * 0.03, col=(1, 1, 1), a=0.2, n=18)
    face(ctx, DAD, P(eye='glare', mouth='wavy'), 540, 880, 300, 0.02 * math.sin(il * 0.5))
    twitch(ctx, 540 + 0.6 * 300, 880 - 0.75 * 300, il, 1.3)
    ctx.restore()
    ctx.restore()
    ctx.rectangle(0, H / 2 - 8, W, 16); setc(ctx, OUT); ctx.fill()
    label(ctx, "*jingle-SHLURP!*", 540, 330, 90, GOLD, -0.04, pop(il, 12, 15))
    label(ctx, "\"...my... KEYS.\"", 540, 1450, 116, ORANGE, 0.03, pop(il, 18, 22))


def s3(ctx, f):
    lf = f - 200
    if lf < 50:
        sock_steal(ctx, f, lf, 0, 14)
        if lf >= 20:
            label(ctx, "*SHLUUURP!*", 540, 330, 120, CYAN, -0.05, pop(lf, 20, 23))
        if lf >= 26:
            label(ctx, "\"MY SOCK!!\"", 540, 1500, 130, RED, 0.03, pop(lf, 26, 29))
    elif lf < 96:
        homework(ctx, f, lf - 50)
    else:
        keys_split(ctx, f, lf - 96)


# ------------------------------------------------------------------ twist
ITEMS = ['sock'] * 9 + ['keys', 'paper', 'remote', 'duck', 'sock', 'sock', 'sock', 'sock']


def explode(ctx, cx, cy, t, n=40, seed=5):
    if t < 0:
        return
    rnd = random.Random(seed)
    for k in range(n):
        ang = rnd.uniform(-math.pi, math.pi)
        v = rnd.uniform(600, 1700)
        d = v * (1 - math.exp(-3.0 * t)) / 3.0
        x = cx + math.cos(ang) * d; y = cy + math.sin(ang) * d + 500 * t * t
        a = rnd.uniform(0, 6.3) + t * rnd.uniform(-7, 7)
        it = ITEMS[k % len(ITEMS)]
        if it == 'sock':
            sock(ctx, x, y, 1.5, a, k)
        elif it == 'keys':
            keys(ctx, x, y, 1.4, a)
        elif it == 'paper':
            paper(ctx, x, y, 1.2, a)
        elif it == 'remote':
            remote(ctx, x, y, 1.2, a)
        else:
            duck(ctx, x, y, 1.3, a)


def sock_mound(ctx, cx, ground, w, h, seed=3):
    ctx.new_path(); ctx.move_to(cx - w / 2, ground + 6)
    ctx.curve_to(cx - w * 0.42, ground - h * 1.25, cx + w * 0.42, ground - h * 1.25, cx + w / 2, ground + 6); ctx.close_path()
    fl(ctx, hx('b6b0c0'), 8)
    rnd = random.Random(seed)
    for k in range(110):
        u = rnd.uniform(-0.5, 0.5); v = rnd.uniform(0, 1) ** 0.7
        hm = h * (1 - (2 * u) ** 2) * 0.95
        sock(ctx, cx + u * w * 0.92, ground - v * hm + 10, rnd.uniform(1.0, 1.4), rnd.uniform(0, 6.3), rnd.randrange(7))


def s4(ctx, f):
    lf = f - 340
    if lf < 46:
        ctx.save(); cam(ctx, 540, 1000, 1.05 + 0.08 * eio(pop(lf, 0, 46)), 5, shake_at(lf, [34], 6, 8), f, sy=1050)
        room(ctx, lf, wall=hx('ffd0d8'))
        b = draw(ctx, 540, FLOOR - 186 * 1.8, 1.8, 1, DAD, P(eye='glare', mouth='frown', lsh=165, rsh=-165, lel=-15, rel=15))
        hy = (b['front'][1] + b['back'][1]) / 2
        ctx.save(); ctx.translate(540, hy - 230); ctx.rotate(math.pi + 0.1 * math.sin(lf * 0.8) * (lf < 34))
        vac_side(ctx, 0, 0, 1.6, 1, lf, 'angry' if lf < 34 else 'normal')
        ctx.restore()
        ctx.restore()
        label2(ctx, "\"GIVE. IT.", "BACK.\"", WHITE, pop(lf, 2, 6), 130, col2=RED, y=1400)
        if lf >= 34:
            label(ctx, "*CLICK*", 540, 330, 110, WHITE, -0.05, pop(lf, 34, 37))
    elif lf < 84:
        il = lf - 46
        ctx.save(); cam(ctx, 540, 960, 1.0, 0, shake_at(il, [0], 26, 26), f)
        room(ctx, il, wall=hx('ffd0d8'))
        g = eout(pop(il, 0, 16))
        for k in range(7):
            ang = k * 0.9 + 0.3
            puff(ctx, 540 + math.cos(ang) * 380 * g, 900 + math.sin(ang) * 420 * g, 260 * g + 40, 0.92)
        explode(ctx, 540, 900, il / 30, 44, 5)
        if il < 4:
            ctx.rectangle(-500, -500, 2500, 3000); setc(ctx, (1, 1, 1, 0.8 * (1 - il / 4))); ctx.fill()
        ctx.restore()
        label(ctx, "*PFOOOMP!!*", 540, 330, 130, WHITE, -0.05, pop(il, 0, 3))
    else:
        il = lf - 84   # 0..56
        ctx.save(); cam(ctx, 590, 1150, 1.08, 0, 0, f)
        room(ctx, il, wall=hx('ffd0d8'))
        draw(ctx, 960, FLOOR - 186 * MK, MK, -1, MOM, P(eye='shock', mouth='open', lsh=40, rsh=-130, rel=-40))
        draw(ctx, 790, FLOOR - 186 * KK, KK, -1, BOY, P(eye='happy', mouth='grin', lsh=150, rsh=-150, lel=20, rel=-20))
        sock_mound(ctx, 400, FLOOR + 10, 720, 400, 4)
        face(ctx, DUSTY, P(eye='closed' if (il % 30) < 3 else 'shock', mouth='flat'), 400, 1000, 120, 0.05)
        sock(ctx, 420, 870, 1.3, 1.2, 2)
        for sx in (250, 560):
            sock(ctx, sx, 1110, 1.3, 0.6 if sx < 400 else -0.6, 3)
        for k in range(3):
            puff(ctx, 200 + k * 200 + 20 * math.sin(il * 0.1 + k), 980 - il * 2 - k * 40, 50, 0.5)
        ctx.restore()
        label(ctx, "*cough cough*", 540, 330, 96, WHITE, 0.04, pop(il, 0, 3))
        if il >= 12:
            label2(ctx, "\"So THAT'S where", "the socks GO!\"", WHITE, pop(il, 12, 16), 100, col2=PINK, y=1400)


# ------------------------------------------------------------------ end
def s5(ctx, f):
    lf = f - 480
    if lf < 60:
        ctx.save(); cam(ctx, 560, 1180, 1.15, 0, 0, f)
        room(ctx, lf)
        pat = math.sin(lf * 0.6) if lf >= 14 else 0
        b = draw(ctx, 380, FLOOR - 186 * DK, DK, 1, DAD, P(eye='happy', mouth='smile', torso=30, head=-10, rsh=-30 - 15 * pat, rel=-40, lsh=20))
        vac_side(ctx, 640, FLOOR, 1.5, -1, lf, 'happy' if lf >= 14 else 'normal', spin=False)
        if lf >= 16:
            for k in range(2):
                y = 1240 - ((lf * 4 + k * 60) % 140)
                ctx.save(); ctx.translate(680 + k * 60, y); ctx.scale(0.9, 0.9)
                ctx.new_path(); ctx.move_to(0, 20); ctx.curve_to(-40, -10, -20, -40, 0, -18); ctx.curve_to(20, -40, 40, -10, 0, 20)
                fl(ctx, PINK, 4); ctx.restore()
        ctx.restore()
        label(ctx, "*pat pat*", 540, 330, 96, WHITE, 0.04, pop(lf, 14, 17))
        label(ctx, "\"...GOOD vacuum.\"", 540, 1440, 116, YEL, -0.04, pop(lf, 4, 8))
    elif lf < 132:
        il = lf - 60   # 0..72
        sock_steal(ctx, f, il, 1, 50, mood0='angry', mood_eat='happy', start_x=1500)
        if il >= 50:
            label(ctx, "*SHLUUURP!*", 540, 330, 120, CYAN, -0.05, pop(il, 50, 53))
        elif il >= 6:
            label(ctx, "*beep... beep...*", 540, 330, 86, RED, 0.03, pop(il, 6, 9))
        if 14 <= il < 50:
            label(ctx, "\"...don't you DARE.\"", 540, 1500, 106, WHITE, -0.04, pop(il, 14, 18))
    else:
        s1(ctx, f, f - 612)


SHOTS = [(0, s1), (54, s2), (200, s3), (340, s4), (480, s5)]
CUTS = (54, 104, 200, 250, 296, 340, 386, 424, 480, 540, 612)


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.22)
    ctx.set_source(g); ctx.paint()
    for c in CUTS:
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.5 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/v{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/robot_vacuum_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
