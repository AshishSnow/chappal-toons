"""'Mom's Bottomless Bag' - original, general-audience comedy short, 22s.
Hook: ECU kid mid-wail, tears flying: "MOM! I'M HUNGRY!!" -> Mom ECU, calm smug smile, hand already deep in a giant handbag: "Hold on, sweetie."
Beat 1: park wide: *rummage* -> a full sandwich *POP* -> "I'm COLD!" puffy coat -> "It's RAINING!" umbrella *FWOMP*.
Beat 2: low angle: kite stuck at the top of a tree "MY KITE!!" -> a ladder slides out of the bag, up and up (tilt-up) *CLANK CLANK*.
Beat 3: Dad ECU: "Honey... where are my CAR KEYS?" -> Mom dives head-first INTO the bag *SHLOOP* -> bag erupts: duck, sock, the lost remote, a lamp, a fish bowl.
Twist: POV from inside the bag looking up at Dad + kid with a flashlight "Mom...?" -> inside: a cozy little living room, Mom in an armchair with tea,
 twirling the keys: "Found your KEYS!" ... "But I'm on a BREAK." -> *ZZZIP* bag zips shut from inside -> Dad ECU sweating:
 kid off-screen "DAD... I'M HUNGRY!" -> opening face (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, eye_pos, zigs
from scenes48 import label1, label2
import scenes13
from scenes13 import card as _card13
import random

BOY = dict(doodle.BOY, hood=False, shirt=hx('22c3a6'), pants=hx('3d5aff'))
MOM = dict(doodle.MOM_G, shirt=hx('ff7a3d'), pants=hx('3d5a9e'))
DAD = dict(doodle.DAD, shirt=hx('8fd0ff'))
N = 660
FLOOR = 1460
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
BAGC = hx('d63c8f')
BAGD = hx('9a2066')
GOLD = hx('ffc93c')

CAPS = {
    'p1': [[("MOM'S BAG", OUT)], [("HAS EVERYTHING", PINK)]],
    'p2': [[("SNACKS?", OUT)], [("CHECK.", GREEN)]],
    'p3': [[("TOO HIGH?", OUT)], [("NO PROBLEM.", BLUE)]],
    'p4': [[("BUT DAD'S", OUT)], [("CAR KEYS...", ORANGE)]],
    'p5': [[("MEANWHILE,", OUT)], [("INSIDE THE BAG", PURPLE)]],
}
scenes13.CAPS = CAPS
card = _card13

_DUMMY = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4))


# ------------------------------------------------------------------ sets
def park(ctx, sky=hx('8fdcff'), horizon=1180):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, sky); ctx.fill()
    for cx_, cy_, s in ((200, 520, 1.0), (820, 430, 0.8), (560, 700, 0.6)):
        for dx, dy, r in ((-60, 0, 60), (0, -30, 75), (70, 0, 58), (10, 20, 60)):
            ellipse(ctx, cx_ + dx * s, cy_ + dy * s, r * s, r * s * 0.85); setc(ctx, (1, 1, 1)); ctx.fill()
    # far hills
    ctx.move_to(-500, horizon); ctx.curve_to(100, horizon - 200, 400, horizon - 120, 700, horizon - 40); ctx.curve_to(900, horizon - 160, 1300, horizon - 140, 1700, horizon)
    ctx.line_to(1700, 3000); ctx.line_to(-500, 3000); ctx.close_path(); fl(ctx, hx('7ed957'), 7)
    ctx.rectangle(-3000, horizon, 7000, 4000); setc(ctx, hx('5cc545')); ctx.fill()
    ctx.move_to(-3000, horizon); ctx.line_to(4000, horizon); ink(ctx, 7); ctx.stroke()
    rnd = random.Random(5)
    for k in range(40):
        x, y = rnd.uniform(-200, 1300), rnd.uniform(horizon + 30, 2000)
        ctx.move_to(x - 10, y); ctx.line_to(x - 4, y - 22); ctx.move_to(x + 2, y); ctx.line_to(x + 8, y - 18)
        setc(ctx, hx('3aa52e')); ctx.set_line_width(5); ctx.stroke()


def tree(ctx, x, ground, h=1500, top_r=330):
    poly(ctx, [(x - 60, ground), (x + 60, ground), (x + 40, ground - h + 200), (x - 40, ground - h + 200)]); fl(ctx, hx('a8642e'), 8)
    ctx.move_to(x, ground - h * 0.55); ctx.line_to(x - 220, ground - h * 0.75); setc(ctx, INK); ctx.set_line_width(48); ctx.stroke()
    ctx.move_to(x, ground - h * 0.55); ctx.line_to(x - 220, ground - h * 0.75); setc(ctx, hx('a8642e')); ctx.set_line_width(32); ctx.stroke()
    for dx, dy, r in ((-0.6, 0.1, 0.7), (0.6, 0.1, 0.7), (0, -0.3, 0.85), (-0.3, 0.35, 0.6), (0.35, 0.4, 0.6)):
        ellipse(ctx, x + dx * top_r, ground - h + dy * top_r, r * top_r, r * top_r * 0.85); fl(ctx, hx('2fb84a'), 8)
    for dx, dy in ((-0.4, -0.2), (0.3, -0.1), (0.0, 0.3)):
        ellipse(ctx, x + dx * top_r, ground - h + dy * top_r, 0.18 * top_r, 0.12 * top_r); setc(ctx, hx('5fd86f')); ctx.fill()


def kite(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(0, -140), (100, 0), (0, 170), (-100, 0)]); fl(ctx, hx('ff3b5c'), 7)
    poly(ctx, [(0, -140), (100, 0), (0, 0)]); fl(ctx, hx('ffd23f'), 5)
    poly(ctx, [(0, 170), (-100, 0), (0, 0)]); fl(ctx, hx('ffd23f'), 5)
    ctx.move_to(0, 170); ctx.curve_to(40, 260, -40, 320, 20, 420); ink(ctx, 5); ctx.stroke()
    for k, ty in enumerate((250, 330, 400)):
        ctx.save(); ctx.translate(10 + (14 if k % 2 else -14), ty); ctx.rotate(0.5 if k % 2 else -0.5)
        poly(ctx, [(-22, 0), (0, -14), (22, 0), (0, 14)]); fl(ctx, BLUE, 4); ctx.restore()
    ctx.restore()


# ------------------------------------------------------------------ props
def bag_back(ctx, x, y, s=1.0, glow=0.0):
    """inside of the bag mouth (draw BEFORE stuff going in); (x, y) = mouth centre"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    # handles behind
    for sx in (-1, 1):
        ctx.new_path(); ctx.arc(sx * 90, -10, 120, math.pi, 2 * math.pi)
        setc(ctx, INK); ctx.set_line_width(44); ctx.stroke()
        ctx.new_path(); ctx.arc(sx * 90, -10, 120, math.pi, 2 * math.pi); setc(ctx, BAGD); ctx.set_line_width(28); ctx.stroke()
    ellipse(ctx, 0, 0, 260, 62); fl(ctx, hx('3a0d2a'), 8)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 10, 0, 0, 260)
        g.add_color_stop_rgba(0, 1, 0.9, 0.5, 0.8 * glow); g.add_color_stop_rgba(1, 1, 0.9, 0.5, 0)
        ellipse(ctx, 0, 0, 250, 56); ctx.set_source(g); ctx.fill()
    ctx.restore()


def bag_front(ctx, x, y, s=1.0, wob=0.0, zip_t=0.0):
    """bag body in front of the mouth; (x, y) = mouth centre"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.translate(0, 0); ctx.rotate(wob)
    ctx.move_to(-262, 0); ctx.curve_to(-262, 40, 262, 40, 262, 0)
    ctx.line_to(320, 330); ctx.curve_to(320, 380, 280, 400, 230, 400)
    ctx.line_to(-230, 400); ctx.curve_to(-280, 400, -320, 380, -320, 330); ctx.close_path(); fl(ctx, BAGC, 9)
    # stitched flap band + clasp
    ctx.move_to(-290, 120); ctx.line_to(290, 120); setc(ctx, light(BAGC, 0.3)); ctx.set_line_width(10); ctx.set_dash([18, 14]); ctx.stroke(); ctx.set_dash([])
    rect_r(ctx, -55, 70, 110, 90, 22); fl(ctx, GOLD, 7)
    ellipse(ctx, 0, 115, 18, 18); fl(ctx, hx('fff2b0'), 4)
    ctx.move_to(-230, 330); ctx.curve_to(-150, 360, 150, 360, 230, 330); setc(ctx, (1, 1, 1, 0.25)); ctx.set_line_width(14); ctx.stroke()
    if zip_t > 0:
        # zipper closing across the mouth from left to right
        zx = -250 + 500 * zip_t
        ctx.move_to(-250, 4); ctx.line_to(zx, 4); setc(ctx, INK); ctx.set_line_width(40); ctx.stroke()
        ctx.move_to(-250, 4); ctx.line_to(zx, 4); setc(ctx, GOLD); ctx.set_line_width(24); ctx.stroke()
        for k in range(int((zx + 250) / 22)):
            ctx.move_to(-246 + k * 22, -8); ctx.line_to(-246 + k * 22, 16); ink(ctx, 4); ctx.stroke()
        rect_r(ctx, zx - 22, -26, 44, 60, 10); fl(ctx, hx('c0c6d6'), 6)
        rect_r(ctx, zx - 12, 30, 24, 50, 8); fl(ctx, hx('c0c6d6'), 5)
    ctx.restore()


def bag(ctx, x, y, s=1.0, wob=0.0, glow=0.0, zip_t=0.0):
    bag_back(ctx, x, y, s, glow); bag_front(ctx, x, y, s, wob, zip_t)


def sandwich(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    poly(ctx, [(-130, 50), (130, 50), (130, 80), (-130, 80)]); fl(ctx, hx('f2c27a'), 6)
    ctx.move_to(-140, 40)
    for i in range(8):
        ctx.line_to(-140 + i * 40 + 20, 60 if i % 2 else 25)
    ctx.line_to(150, 40); ctx.close_path(); fl(ctx, hx('6fd84a'), 5)
    rect_r(ctx, -135, 0, 270, 34, 10); fl(ctx, hx('ff5a5a'), 5)
    rect_r(ctx, -128, -16, 256, 22, 8); fl(ctx, hx('ffd23f'), 5)
    ctx.move_to(-140, -10); ctx.curve_to(-140, -110, 140, -110, 140, -10); ctx.close_path(); fl(ctx, hx('f2c27a'), 6)
    for sx, sy in ((-60, -60), (0, -75), (60, -58), (-20, -40), (40, -38)):
        ellipse(ctx, sx, sy, 7, 4); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.restore()


def coat(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    col = hx('1f8bff')
    for sx in (-1, 1):
        poly(ctx, [(sx * 110, -150), (sx * 230, -40), (sx * 250, 160), (sx * 170, 170), (sx * 150, -20)]); fl(ctx, col, 7)
        rect_r(ctx, sx * 250 - (60 if sx > 0 else 20), 150, 80, 40, 14); fl(ctx, hx('ffffff'), 5)
    rect_r(ctx, -160, -160, 320, 380, 60); fl(ctx, col, 7)
    for k in range(4):
        ctx.move_to(-160, -80 + k * 80); ctx.curve_to(-60, -60 + k * 80, 60, -60 + k * 80, 160, -80 + k * 80); ink(ctx, 5); ctx.stroke()
    ctx.move_to(0, -160); ctx.line_to(0, 220); ink(ctx, 5); ctx.stroke()
    ellipse(ctx, 0, -175, 140, 50); fl(ctx, hx('ffffff'), 6)
    ctx.restore()


def umbrella(ctx, x, y, s=1.0, a=0.0, open_=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(0, 0); ctx.line_to(0, 330); setc(ctx, INK); ctx.set_line_width(20); ctx.stroke()
    ctx.move_to(0, 0); ctx.line_to(0, 330); setc(ctx, hx('dfe3ee')); ctx.set_line_width(10); ctx.stroke()
    ctx.new_path(); ctx.arc(-30, 330, 30, 0, math.pi); setc(ctx, INK); ctx.set_line_width(22); ctx.stroke()
    ctx.new_path(); ctx.arc(-30, 330, 30, 0, math.pi); setc(ctx, hx('a8642e')); ctx.set_line_width(12); ctx.stroke()
    w = 60 + 280 * open_
    h = 220 - 60 * open_
    cols = (hx('ffd23f'), hx('ff3b5c'), hx('ffd23f'), hx('ff3b5c'))
    for k in range(4):
        x0 = -w + k * w / 2; x1 = x0 + w / 2
        ctx.move_to(0, -h); ctx.curve_to(x0, -h + 20, x0, -20, x0, 0)
        ctx.curve_to(x0 + w / 8, -30, x1 - w / 8, -30, x1, 0); ctx.curve_to(x1, -20, x1, -h + 20, 0, -h); ctx.close_path(); fl(ctx, cols[k], 6)
    ctx.move_to(0, -h); ctx.line_to(0, -h - 40); ink(ctx, 10); ctx.stroke()
    ctx.restore()


def ladder(ctx, x, y_bot, h, w=170):
    """ladder rising from y_bot up by h"""
    for sx in (-1, 1):
        ctx.move_to(x + sx * w / 2, y_bot); ctx.line_to(x + sx * w / 2, y_bot - h); setc(ctx, INK); ctx.set_line_width(36); ctx.stroke()
        ctx.move_to(x + sx * w / 2, y_bot); ctx.line_to(x + sx * w / 2, y_bot - h); setc(ctx, hx('c0c6d6')); ctx.set_line_width(20); ctx.stroke()
    k = 1
    while k * 120 < h:
        yy = y_bot - k * 120
        ctx.move_to(x - w / 2, yy); ctx.line_to(x + w / 2, yy); setc(ctx, INK); ctx.set_line_width(26); ctx.stroke()
        ctx.move_to(x - w / 2, yy); ctx.line_to(x + w / 2, yy); setc(ctx, hx('ff8a1f')); ctx.set_line_width(12); ctx.stroke()
        k += 1


def keys(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 34, 0, 2 * math.pi); setc(ctx, INK); ctx.set_line_width(16); ctx.stroke()
    ctx.new_path(); ctx.arc(0, 0, 34, 0, 2 * math.pi); setc(ctx, hx('dfe3ee')); ctx.set_line_width(7); ctx.stroke()
    for ang, col in ((1.2, GOLD), (2.0, hx('c0c6d6'))):
        ctx.save(); ctx.rotate(ang); ctx.translate(34, 0)
        ellipse(ctx, 30, 0, 30, 26); fl(ctx, col, 5)
        poly(ctx, [(55, -10), (140, -10), (140, 0), (128, 0), (128, 14), (114, 14), (114, 0), (100, 0), (100, 10), (55, 10)]); fl(ctx, col, 5)
        ctx.restore()
    ctx.restore()


def duck(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ellipse(ctx, 0, 20, 90, 60); fl(ctx, hx('ffd23f'), 6)
    ellipse(ctx, 50, -40, 48, 46); fl(ctx, hx('ffd23f'), 6)
    poly(ctx, [(90, -44), (130, -36), (92, -24)]); fl(ctx, ORANGE, 5)
    ellipse(ctx, 62, -50, 8, 9); setc(ctx, INK); ctx.fill()
    ctx.restore()


def sock(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(-30, -110); ctx.line_to(30, -110); ctx.line_to(30, 30); ctx.curve_to(30, 60, 90, 50, 100, 70); ctx.curve_to(110, 110, 40, 120, -10, 100)
    ctx.curve_to(-40, 90, -30, 60, -30, 30); ctx.close_path(); fl(ctx, hx('ffffff'), 6)
    ctx.rectangle(-30, -80, 60, 22); setc(ctx, RED); ctx.fill(); ctx.rectangle(-30, -50, 60, 16); setc(ctx, BLUE); ctx.fill()
    ctx.restore()


def remote(ctx, x, y, s=1.0, a=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -40, -120, 80, 240, 22); fl(ctx, hx('2a2a3a'), 6)
    ellipse(ctx, 0, -85, 16, 16); fl(ctx, RED, 3)
    for r in range(3):
        for c in range(2):
            ellipse(ctx, -14 + c * 28, -30 + r * 40, 9, 9); setc(ctx, hx('9aa0b4')); ctx.fill()
    ctx.restore()


def lamp(ctx, x, y, s=1.0, a=0.0, on=True):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    if on:
        g = cairo.RadialGradient(0, -40, 10, 0, -40, 320)
        g.add_color_stop_rgba(0, 1, 0.95, 0.6, 0.55); g.add_color_stop_rgba(1, 1, 0.95, 0.6, 0)
        ellipse(ctx, 0, -40, 320, 320); ctx.set_source(g); ctx.fill()
    ctx.move_to(0, -40); ctx.line_to(0, 160); setc(ctx, INK); ctx.set_line_width(20); ctx.stroke()
    ctx.move_to(0, -40); ctx.line_to(0, 160); setc(ctx, GOLD); ctx.set_line_width(10); ctx.stroke()
    ellipse(ctx, 0, 165, 70, 20); fl(ctx, GOLD, 6)
    poly(ctx, [(-60, -140), (60, -140), (100, -30), (-100, -30)]); fl(ctx, hx('fff2b0'), 7)
    ctx.restore()


def fishbowl(ctx, x, y, s=1.0, a=0.0, lf=0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 110, 100); setc(ctx, (0.7, 0.9, 1, 0.8)); ctx.fill_preserve(); ink(ctx, 6); ctx.stroke()
    ellipse(ctx, 0, -86, 70, 16); fl(ctx, hx('dff4ff'), 5)
    fx = 20 * math.sin(lf * 0.4)
    ellipse(ctx, fx, 10, 34, 22); fl(ctx, ORANGE, 5)
    poly(ctx, [(fx - 30, 10), (fx - 60, -10), (fx - 60, 30)]); fl(ctx, ORANGE, 4)
    ellipse(ctx, fx + 16, 4, 5, 5); setc(ctx, INK); ctx.fill()
    ctx.restore()


def mug(ctx, x, y, s=1.0, steam=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(58, 0, 30, -math.pi / 2, math.pi / 2); setc(ctx, INK); ctx.set_line_width(22); ctx.stroke()
    ctx.new_path(); ctx.arc(58, 0, 30, -math.pi / 2, math.pi / 2); setc(ctx, PINK); ctx.set_line_width(10); ctx.stroke()
    rect_r(ctx, -55, -60, 115, 130, 18); fl(ctx, PINK, 6)
    ellipse(ctx, 2, -60, 56, 14); fl(ctx, hx('8a4a2a'), 5)
    for k in range(3):
        ph = steam * 0.15 + k * 2
        ctx.move_to(-30 + k * 30, -80); ctx.curve_to(-50 + k * 30 + 20 * math.sin(ph), -120, -10 + k * 30, -150, -30 + k * 30 + 20 * math.sin(ph + 1), -190)
        setc(ctx, (1, 1, 1, 0.75)); ctx.set_line_width(9); ctx.stroke()
    ctx.restore()


def tears(ctx, cx, cy, R, lf):
    for sx in (-1, 1):
        for k in range(3):
            t = ((lf * 0.07 + k / 3.0) % 1.0)
            x = cx + sx * (0.45 * R + 520 * t) + (0.1 * R if sx > 0 else 0)
            y = cy + 0.05 * R - 260 * t + 500 * t * t
            ctx.move_to(x, y - 60); ctx.curve_to(x + 38, y, x + 32, y + 42, x, y + 42); ctx.curve_to(x - 32, y + 42, x - 38, y, x, y - 60)
            fl(ctx, hx('5ac8ff'), 5)


def rummage_lines(ctx, x, y, lf, r=300):
    for k in range(5):
        a = -math.pi * 0.85 + k * math.pi * 0.17 + 0.05 * math.sin(lf * 0.9 + k)
        ctx.move_to(x + math.cos(a) * r, y + math.sin(a) * r * 0.6); ctx.line_to(x + math.cos(a) * (r + 60), y + math.sin(a) * (r + 60) * 0.6)
        ink(ctx, 9); ctx.stroke()


def sweat(ctx, x, y, lf, s=1.0):
    y_ = y + ((lf * 3) % 120)
    ctx.move_to(x, y_ - 40 * s); ctx.curve_to(x + 26 * s, y_, x + 20 * s, y_ + 26 * s, x, y_ + 26 * s)
    ctx.curve_to(x - 20 * s, y_ + 26 * s, x - 26 * s, y_, x, y_ - 40 * s); fl(ctx, hx('5ac8ff'), 5)


# ------------------------------------------------------------------ opening face
def opening_face(ctx, f, lf, lab=True):
    bob = 14 * abs(math.sin(lf * 0.6))
    ctx.save(); cam(ctx, 540, 960, 1.02 + 0.04 * eout(pop(lf, 0, 40)), 2.0 * math.sin(lf * 0.7), 7, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffd23f')); ctx.fill()
    rays(ctx, 540, 960, 260, 1700, lf * 0.06, col=(1, 1, 1), a=0.5, n=18)
    cx, cy, R = 540, 1000 - bob, 290
    rot = 0.06 * math.sin(lf * 0.8)
    face(ctx, BOY, P(eye='closed', mouth='scream', head=0), cx, cy, R, rot)
    tears(ctx, cx, cy, R, lf)
    ctx.restore()
    if lab:
        label2(ctx, "\"MOM!", "I'M HUNGRY!!\"", (1, 1, 1), 1.0, 120, col2=YEL)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 45:
        opening_face(ctx, f, f)
    else:
        lf = f - 45
        # Mom ECU: calm smug smile, arm already deep in the giant bag
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.08 * eout(pop(lf, 0, 40)), 0, shake_at(lf, [0], 8, 10), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb3d9')); ctx.fill()
        rays(ctx, 540, 900, 260, 1700, lf * 0.03, col=(1, 1, 1), a=0.35, n=14)
        cx, cy, R = 460, 800, 250
        face(ctx, MOM, P(eye='smug', mouth='smile', head=0), cx, cy, R, -0.05)
        # her arm reaching down into the bag (bag mouth bottom-right)
        bx, by = 720, 1120
        bag_back(ctx, bx, by, 0.95)
        wig = 14 * math.sin(lf * 1.4)
        ctx.move_to(cx + 120, cy + 300); ctx.curve_to(cx + 220, cy + 380, bx - 40 + wig, by - 120, bx + wig, by + 10)
        setc(ctx, INK); ctx.set_line_width(96); ctx.stroke()
        ctx.move_to(cx + 120, cy + 300); ctx.curve_to(cx + 220, cy + 380, bx - 40 + wig, by - 120, bx + wig, by + 10)
        setc(ctx, MOM['shirt']); ctx.set_line_width(78); ctx.stroke()
        bag_front(ctx, bx, by, 0.95, 0.03 * math.sin(lf * 1.4))
        rummage_lines(ctx, bx, by, lf, 280)
        ctx.restore()
        label2(ctx, "\"Hold on,", "sweetie...\"", (1, 1, 1), pop(lf, 2, 6), 104, col2=PINK, y=1400)
    card(ctx, 'p1', f, -6, 86)


def mom_with_bag(ctx, mx, mbag_x, by, arm_up=0.0, eye='smug', mouth='smile', bs=0.75, wob=0.0, glow=0.0):
    """Mom standing (facing right) beside the giant bag on the ground"""
    bag_back(ctx, mbag_x, by, bs, glow)
    b = draw(ctx, mx, FLOOR - 186 * 1.3, 1.3, 1, MOM, P(lsh=20, rsh=60 + 100 * arm_up, rel=-20 - 30 * arm_up, eye=eye, mouth=mouth))
    bag_front(ctx, mbag_x, by, bs, wob)
    return b


def kid_wide(ctx, x, p, k=1.0):
    return draw(ctx, x, FLOOR - 186 * k, k, -1, BOY, p)


def s2(ctx, f):
    lf = f - 90
    BX, BY = 540, 1200
    if lf < 45:
        # wide park: rummage... sandwich POPS out
        ctx.save(); cam(ctx, 540, 1060, 1.0 + 0.05 * eout(pop(lf, 20, 30)), 0, shake_at(lf, [20], 10, 18), f)
        park(ctx)
        up = eout(pop(lf, 20, 28))
        mom_with_bag(ctx, 160, BX, BY, up, wob=0.05 * math.sin(lf * 1.5) * (1 - up))
        if lf < 20:
            rummage_lines(ctx, BX, BY, lf, 290)
        else:
            sandwich(ctx, BX, BY - 60 - 330 * up + 60 * ein(pop(lf, 28, 45)), 1.0 + 0.2 * up, 0.3 * (1 - up))
            sparkle(ctx, BX - 220, BY - 470, 30 * up); sparkle(ctx, BX + 220, BY - 520, 40 * up)
        kid_wide(ctx, 900, P(eye='shock' if lf >= 20 else 'closed', mouth='open' if lf >= 20 else 'frown', lsh=-30, rsh=30))
        ctx.restore()
        if lf < 20:
            label1(ctx, "*rummage rummage*", (1, 1, 1), pop(lf, 1, 4), 96, y=1450)
        else:
            label1(ctx, "*POP!*", YEL, pop(lf, 20, 23), 150, -0.05, y=1450)
        card(ctx, 'p2', f, 92, 132)
    elif lf < 75:
        il = lf - 45
        # snap push-in: "I'm COLD!" -> puffy coat flies out
        ctx.save(); cam(ctx, 620, 1000, 1.25, -3, shake_at(il, [10], 8, 16), f)
        park(ctx, sky=hx('b8e4ff'))
        for k in range(14):  # wind streaks
            y = 500 + k * 70; x0 = (il * 60 + k * 170) % 1500 - 300
            ctx.move_to(x0, y); ctx.line_to(x0 + 160, y); setc(ctx, (1, 1, 1, 0.8)); ctx.set_line_width(8); ctx.stroke()
        up = eout(pop(il, 10, 18))
        mom_with_bag(ctx, 160, BX, BY, up)
        if il >= 10:
            coat(ctx, BX + 300 * up, BY - 100 - 260 * up, 0.4 + 0.35 * up, -0.8 * (1 - up))
        kid_wide(ctx, 900, P(eye='closed', mouth='wavy', lsh=-150, lel=-110, rsh=-150, rel=-110, torso=-4 + 4 * math.sin(il * 3)))
        ctx.restore()
        label1(ctx, "\"I'm COLD!\"" if il < 10 else "*FLUMP!*", (1, 1, 1) if il < 10 else YEL, pop(il, 1, 4) if il < 10 else pop(il, 10, 13), 120, y=1440)
    else:
        il = lf - 75
        # dutch tilt other way: "It's RAINING!" -> umbrella FWOMP
        ctx.save(); cam(ctx, 520, 1000, 1.2, 4, shake_at(il, [12], 8, 18), f)
        park(ctx, sky=hx('7f93b0'))
        up = eout(pop(il, 12, 18))
        mom_with_bag(ctx, 160, BX, BY, up)
        if il >= 12:
            umbrella(ctx, BX + 330 * up, BY - 120 - 330 * up, 0.5 + 0.3 * up, -0.4 * (1 - up), up)
        kid_wide(ctx, 900, P(eye='shock', mouth='scream' if il < 12 else 'grin', lsh=-160, lel=-20, rsh=-160, rel=-20))
        rnd = random.Random(il // 2)
        for k in range(40):
            x = rnd.uniform(-100, 1200); y = rnd.uniform(200, 1800)
            if il >= 18 and 690 < x < 1060 and y > 640:
                continue
            ctx.move_to(x, y); ctx.line_to(x - 14, y + 60); setc(ctx, (0.8, 0.9, 1, 0.9)); ctx.set_line_width(7); ctx.stroke()
        ctx.restore()
        label1(ctx, "\"It's RAINING!\"" if il < 12 else "*FWOMP!*", (1, 1, 1) if il < 12 else YEL, pop(il, 1, 4) if il < 12 else pop(il, 12, 15), 120, y=1440)


def s3(ctx, f):
    lf = f - 200
    if lf < 40:
        # low angle up the tree: kite stuck at the top, kid pointing
        ctx.save(); cam(ctx, 540, 900, 1.0 + 0.06 * eout(pop(lf, 0, 40)), -2, 0, f)
        park(ctx, horizon=1500)
        tree(ctx, 600, 1600, 980, 330)
        kite(ctx, 650, 640, 0.9, 0.4 + 0.08 * math.sin(lf * 0.5))
        face(ctx, BOY, P(eye='shock', mouth='scream', head=0), 290, 1020, 220, -0.15)
        tears(ctx, 290, 1020, 220, lf)
        ctx.restore()
        label1(ctx, "\"MY KITE!!\"", (1, 1, 1), pop(lf, 2, 6), 130, y=1440)
        card(ctx, 'p3', f, 202, 236)
    elif lf < 100:
        il = lf - 40
        # the ladder slides up out of the bag; camera tilts up with it
        h = 1500 * eout(pop(il, 4, 44))
        cyc = 1150 - 700 * eout(pop(il, 8, 50))
        ctx.save(); cam(ctx, 540, cyc, 0.85, 0, 6 if 4 < il < 44 else 0, f)
        park(ctx, horizon=1260)
        tree(ctx, 760, 1360, 1400, 360)
        kite(ctx, 760, 30, 0.9, 0.4)
        BX, BY = 470, 1200
        bag_back(ctx, BX, BY, 1.0, 0.5)
        ladder(ctx, BX + 30, BY + 30, h)
        bag_front(ctx, BX, BY, 1.0, 0.04 * math.sin(il * 2))
        draw(ctx, 180, 1360 - 186 * 1.3, 1.3, 1, MOM, P(lsh=20, rsh=-150, rel=-20, eye='smug', mouth='smile'))
        ctx.restore()
        label1(ctx, "*CLANK! CLANK! CLANK!*", YEL, pop(il, 5, 9), 96, 0.03 * math.sin(il), y=1450)
    else:
        il = lf - 100
        # kid at the top of the ladder hugging the kite
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eout(pop(il, 0, 30)), 0, shake_at(il, [0], 8, 12), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('8fdcff')); ctx.fill()
        rays(ctx, 540, 900, 200, 1700, il * 0.05, col=(1, 1, 1), a=0.45, n=16)
        ladder(ctx, 540, 2300, 1400, 260)
        kite(ctx, 790, 740, 0.9, 0.5)
        face(ctx, BOY, P(eye='happy', mouth='grin', head=0), 520, 880, 240, 0.05)
        for k in range(4):
            sparkle(ctx, 200 + k * 230, 1220 + 30 * math.sin(il * 0.4 + k), 30)
        ctx.restore()
        label2(ctx, "\"BEST.", "MOM. EVER.\"", (1, 1, 1), pop(il, 2, 6), 110, col2=YEL, y=1330)


def s4(ctx, f):
    lf = f - 330
    if lf < 40:
        # Dad ECU, patting his pockets
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.1 * eout(pop(lf, 0, 40)), 0, shake_at(lf, [0], 8, 10), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffcf7a')); ctx.fill()
        rays(ctx, 540, 900, 260, 1700, lf * 0.03, col=(1, 1, 1), a=0.35, n=14)
        cx, cy, R = 540, 900, 280
        face(ctx, DAD, P(eye='shock', mouth='open', head=0), cx, cy, R, 0.04 * math.sin(lf * 0.6))
        sweat(ctx, cx + 0.95 * R, cy - 0.6 * R, lf)
        ctx.restore()
        label2(ctx, "\"Honey... where are", "my CAR KEYS?\"", (1, 1, 1), pop(lf, 2, 6), 92, col2=ORANGE, y=1360)
        card(ctx, 'p4', f, 332, 366)
    elif lf < 90:
        il = lf - 40
        # wide: Mom dives head-first INTO the bag
        BX, BY = 540, 1250
        ctx.save(); cam(ctx, 540, 1000, 1.0, 0, shake_at(il, [8, 40], 10, 18), f)
        park(ctx)
        draw(ctx, 140, FLOOR - 186 * 1.2, 1.2, 1, DAD, P(eye='shock', mouth='open', lsh=-40, rsh=40))
        kid_wide(ctx, 950, P(eye='shock', mouth='open', lsh=-160, rsh=-160, lel=-20, rel=-20))
        bag_back(ctx, BX, BY, 1.0)
        if il < 8:
            # crouch & leap
            draw(ctx, 540, 1250 - 186 * 1.2 - 200 * eout(pop(il, 2, 8)), 1.2, 1, MOM, P(eye='glare', mouth='grin', lsh=-170, rsh=-170, lel=0, rel=0, torso=20, lhip=-30, lkn=40))
        else:
            u = ein(pop(il, 8, 40))
            piv = 640 + 900 * u
            k = 1.2
            ytop = piv - 94.2 * k
            ctx.save(); ctx.rectangle(-500, -500, 2200, BY + 10 + 500); ctx.rectangle(-500, -500, 2200, 1); ctx.restore()
            ctx.save(); ctx.rectangle(-500, -2000, 2200, 2000 + BY); ctx.clip()
            kick_ = 30 * math.sin(il * 1.6)
            draw(ctx, 540, ytop, k, 1, MOM, P(rot=180, eye='glare', mouth='grin', lsh=-10, rsh=10, lhip=-20 + kick_, lkn=30, rhip=20 - kick_, rkn=-30))
            ctx.restore()
        bag_front(ctx, BX, BY, 1.0, 0.06 * math.sin(il * 2.2) if il > 8 else 0)
        ctx.restore()
        if il < 30:
            label1(ctx, "\"Hold on.\"" if il < 8 else "*SHLOOOOP!*", (1, 1, 1) if il < 8 else YEL, pop(il, 1, 4) if il < 8 else pop(il, 8, 11), 120, y=600)
        else:
            label1(ctx, "...", (1, 1, 1), pop(il, 40, 43), 130, y=600)
    else:
        il = lf - 90
        # bag ERUPTS: stuff flies everywhere, Dad + kid duck
        BX, BY = 540, 1250
        ctx.save(); cam(ctx, 540, 1000, 1.06, 2 * math.sin(il * 1.3), 10, f)
        park(ctx)
        draw(ctx, 140, FLOOR - 186 * 1.2 + 30, 1.2, 1, DAD, P(eye='shock', mouth='scream', lsh=-170, rsh=-170, lel=-60, rel=-60, torso=30))
        kid_wide(ctx, 950, P(eye='shock', mouth='scream', lsh=-170, rsh=-170, lel=-60, rel=-60, torso=30))
        bag_back(ctx, BX, BY, 1.0)
        bag_front(ctx, BX, BY, 1.0, 0.12 * math.sin(il * 2.6))
        items = (duck, sock, remote, lamp, fishbowl, sandwich, sock, duck, coat)
        for j, fn in enumerate(items):
            t = (il - j * 3.5) / 22.0
            if not 0 < t < 1.6:
                continue
            ang = -math.pi / 2 + (j - 4) * 0.28
            d = 1100 * t
            x = BX + math.cos(ang) * d; y = BY - 60 + math.sin(ang) * d + 900 * t * t
            sc = 0.45 if fn is coat else (0.7 if fn in (lamp, fishbowl, sandwich) else 0.9)
            if fn is fishbowl:
                fn(ctx, x, y, sc, t * 4, il)
            elif fn is lamp:
                fn(ctx, x, y, sc, t * 5, on=False)
            else:
                fn(ctx, x, y, sc, t * 6 + j)
        ctx.restore()
        label1(ctx, "*CLATTER! BONK! CRASH!*", YEL, pop(il, 2, 5), 92, 0.04 * math.sin(il), y=600)


def s5(ctx, f):
    lf = f - 460
    if lf < 40:
        # POV from INSIDE the bag looking up: Dad + kid peer down with a flashlight
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.04 * eout(pop(lf, 0, 40)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('2a0a20')); ctx.fill()
        # lining pattern
        for i in range(-6, 14):
            ctx.move_to(i * 120, -200); ctx.line_to(i * 120 + 400, 2200); setc(ctx, (0.45, 0.12, 0.33, 0.6)); ctx.set_line_width(20); ctx.stroke()
        ctx.save(); ellipse(ctx, 540, 980, 470, 640); ctx.clip()
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('8fdcff')); ctx.fill()
        face(ctx, DAD, P(eye='shock', mouth='flat', head=0), 360, 960, 220, math.pi + 0.15)
        face(ctx, BOY, P(eye='shock', mouth='flat', head=0), 730, 1010, 190, math.pi - 0.15)
        ctx.restore()
        ellipse(ctx, 540, 980, 470, 640); ink(ctx, 14); ctx.stroke()
        # flashlight beam
        fb = 0.5 + 0.1 * math.sin(lf * 0.7)
        poly(ctx, [(560, 480), (620, 480), (900, 1900), (100, 1900)]); setc(ctx, (1, 1, 0.75, 0.22 * fb + 0.08)); ctx.fill()
        ctx.restore()
        label1(ctx, "\"Mom...?\"", (1, 1, 1), pop(lf, 4, 8), 120, y=1450)
        card(ctx, 'p5', f, 462, 500)
    elif lf < 125:
        il = lf - 40
        # inside the bag: a cozy little living room
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.07 * eout(pop(il, 0, 85)), 0, shake_at(il, [42], 6, 8), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb3d9')); ctx.fill()
        for i in range(-6, 16):
            ctx.rectangle(i * 110, -500, 44, 3000); setc(ctx, hx('ffc8e4')); ctx.fill()
        # bag lining ceiling with the zip mouth far above
        ctx.move_to(-500, 330); ctx.curve_to(200, 470, 880, 470, 1600, 330); ctx.line_to(1600, -500); ctx.line_to(-500, -500); ctx.close_path(); fl(ctx, hx('5a1a40'), 8)
        # rug + floor
        ctx.rectangle(-500, 1420, 2200, 900); setc(ctx, hx('c46a2e')); ctx.fill()
        ellipse(ctx, 540, 1500, 520, 90); fl(ctx, hx('8a3cff'), 7)
        # picture frame
        rect_r(ctx, 700, 560, 220, 170, 10); fl(ctx, GOLD, 8)
        ctx.rectangle(722, 582, 176, 126); setc(ctx, hx('8fdcff')); ctx.fill()
        ctx.move_to(722, 708); ctx.line_to(780, 640); ctx.line_to(830, 690); ctx.line_to(860, 660); ctx.line_to(898, 708); ctx.close_path(); setc(ctx, GREEN); ctx.fill()
        lamp(ctx, 900, 1250, 1.0, 0, True)
        # armchair
        rect_r(ctx, 120, 820, 560, 560, 90); fl(ctx, hx('1f8bff'), 9)
        rect_r(ctx, 60, 1080, 160, 340, 60); fl(ctx, hx('1f6be0'), 9)
        rect_r(ctx, 580, 1080, 160, 340, 60); fl(ctx, hx('1f6be0'), 9)
        rect_r(ctx, 200, 1180, 400, 200, 40); fl(ctx, hx('3aa0ff'), 8)
        # Mom: torso + head, mug + keys
        rect_r(ctx, 270, 1010, 260, 260, 70); fl(ctx, MOM['shirt'], 8)
        face(ctx, MOM, P(eye='closed' if il < 42 else 'smug', mouth='smile', head=0), 400, 860, 170, -0.06)
        mug(ctx, 300, 1130, 0.9, il)
        ellipse(ctx, 290, 1150, 44, 40); fl(ctx, MOM['skin'], 6)
        # other arm up, keys twirling on a finger
        ctx.move_to(500, 1060); ctx.curve_to(600, 1040, 640, 960, 650, 880); setc(ctx, INK); ctx.set_line_width(70); ctx.stroke()
        ctx.move_to(500, 1060); ctx.curve_to(600, 1040, 640, 960, 650, 880); setc(ctx, MOM['shirt']); ctx.set_line_width(54); ctx.stroke()
        ellipse(ctx, 650, 860, 40, 40); fl(ctx, MOM['skin'], 6)
        if il >= 42:
            keys(ctx, 650, 800, 0.9, il * 0.6)
        # feet up on a pouf
        ellipse(ctx, 560, 1440, 120, 60); fl(ctx, hx('ffd23f'), 7)
        ellipse(ctx, 540, 1370, 50, 30); fl(ctx, MOM['shoes'], 6); ellipse(ctx, 610, 1375, 50, 30); fl(ctx, MOM['shoes'], 6)
        ctx.restore()
        if il < 42:
            label1(ctx, "\"Ahhh...\"", (1, 1, 1), pop(il, 3, 7), 110, y=1450)
        elif il < 70:
            label1(ctx, "\"Found your KEYS!\"", YEL, pop(il, 42, 46), 110, y=1450)
        else:
            label2(ctx, "\"...but I'm", "on a BREAK.\"", (1, 1, 1), pop(il, 70, 74), 110, col2=PINK, y=1380)
    elif lf < 160:
        il = lf - 125
        # outside, low wide: the bag ZIPS itself shut in Dad's + kid's faces
        BX, BY = 540, 1250
        ctx.save(); cam(ctx, 540, 1080, 1.12, 0, shake_at(il, [26], 8, 14), f)
        park(ctx)
        face(ctx, DAD, P(eye='shock', mouth='open', head=0), 300, 1010, 200, 0.3)
        face(ctx, BOY, P(eye='shock', mouth='open', head=0), 790, 1040, 170, -0.3)
        bag(ctx, BX, BY, 1.0, 0.0, 0.0, eout(pop(il, 4, 26)))
        ctx.restore()
        label1(ctx, "*ZZZZZIP!*", YEL, pop(il, 4, 8), 140, -0.04, y=600)
    elif lf < 186:
        il = lf - 160
        # Dad ECU, sweating: kid off-screen "DAD... I'M HUNGRY!"
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.12 * eout(pop(il, 0, 26)), 0, shake_at(il, [8], 8, 14), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8a8a')); ctx.fill()
        rays(ctx, 540, 900, 260, 1700, il * 0.08, col=(1, 1, 1), a=0.45, n=18)
        cx, cy, R = 540, 940, 290
        face(ctx, DAD, P(eye='shock', mouth='wavy', head=0), cx, cy, R, 0.03 * math.sin(il * 2))
        sweat(ctx, cx + 0.95 * R, cy - 0.6 * R, il); sweat(ctx, cx - 1.0 * R, cy - 0.5 * R, il + 20)
        ctx.restore()
        label2(ctx, "\"DAD...", "I'M HUNGRY!\"", (1, 1, 1), pop(il, 0, 4), 120, col2=YEL, y=1360)
    else:
        il = lf - 186
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 646)


SHOTS = [(0, s1), (90, s2), (200, s3), (330, s4), (460, s5)]
CUTS = (45, 90, 135, 165, 200, 240, 300, 330, 370, 420, 460, 500, 585, 620, 646)


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
            render(f).write_to_png(f'out/v{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/bag_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
