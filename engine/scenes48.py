"""'I Was Watching That!' - original, general-audience comedy short, 22s.
Hook: ECU Dad, eyes snapping open mid-snore with a drool bubble popping: "I WAS WATCHING THAT!!"
Beat 1: wide - Dad asleep on the sofa with the remote, *SNOOORE*. The kid tiptoes in and slides the remote out of his hand.
 TV POV: boring grey channel -> *CLICK* -> bright cartoon colours. Dad wakes: "I WAS WATCHING THAT!"
 Split screen: kid "YOUR EYES WERE CLOSED!" / Dad smug: "I was RESTING my EYES."
Beat 2: 2 seconds later he snores again. The kid swaps the remote for a BANANA. Dad half-wakes, clicks the banana at the TV:
 "I'm... WATCHING..." then the kid pulls the plug: TV off. Dad, asleep: "Ooh... GREAT show..."
Beat 3: 11 PM - the kid gave up and is now snoring on Dad's shoulder, Zzz duet.
Twist: Mom tiptoes in, takes the remote, plugs the TV in: her show (hearts). Dad AND kid pop awake:
 "WE WERE WATCHING THAT!!" - Mom, eyes already closed: "Shh. I'm resting my eyes." -> cut back to the opening (loop)."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, living, sofa_back, sofa_front, SEAT, eye_pos, zzz
from scenes8 import sit
from scenes13 import tiptoe
from scenes23 import remote
from scenes28 import banana
import scenes13
from scenes13 import card as _card13
import random

BOY = dict(doodle.BOY, hood=False)
DAD = doodle.DAD
MOM = doodle.MOM_G
N = 660
FLOOR = 1460
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
LY = 1400

CAPS = {
    'p1': [[("WHEN DAD IS", OUT)], [("\"WATCHING\" TV", RED)]],
    'p2': [[("TEST #1:", OUT)], [("CHANGE THE CHANNEL", BLUE)]],
    'p3': [[("TEST #2:", OUT)], [("THE BANANA", ORANGE)]],
    'p4': [[("11 PM...", PURPLE)]],
    'p5': [[("PLOT TWIST:", OUT)], [("MOM FINDS THE REMOTE", PINK)]],
}
scenes13.CAPS = CAPS
card = _card13


def label2(ctx, a, b, col, t, size=104, col2=None, y=LY):
    label(ctx, a, 540, y - 60, size, col, -0.03, t)
    label(ctx, b, 540, y + 50, size, col2 or col, 0.02, t)


def label1(ctx, s, col, t, size=110, ang=-0.03, y=LY + 20):
    label(ctx, s, 540, y, size, col, ang, t)


# ------------------------------------------------------------------ props
def tv(ctx, cx, cy, w, h, mode, lf, off=0.0):
    """TV seen from the front. mode: 'boring' | 'cartoon' | 'love' | 'off'"""
    rect_r(ctx, cx - w / 2 - 30, cy - h / 2 - 30, w + 60, h + 60, 30); fl(ctx, hx('2a2a3a'), 9)
    ctx.save(); rect_r(ctx, cx - w / 2, cy - h / 2, w, h, 14); ctx.clip()
    x0, y0 = cx - w / 2, cy - h / 2
    if mode == 'boring':
        ctx.rectangle(x0, y0, w, h); setc(ctx, hx('8a8f99')); ctx.fill()
        # a slow bar chart + a ticker that nobody reads
        for k, v in enumerate((0.3, 0.45, 0.38, 0.5, 0.42)):
            ctx.rectangle(x0 + w * (0.12 + k * 0.16), y0 + h * (0.8 - v), w * 0.1, h * v); setc(ctx, hx('a9aeb8')); ctx.fill()
        ctx.rectangle(x0, y0 + h * 0.84, w, h * 0.16); setc(ctx, hx('6a6f7a')); ctx.fill()
        for k in range(6):
            ctx.rectangle(x0 + ((k * w * 0.22 - lf * 3) % (w * 1.2)) - w * 0.1, y0 + h * 0.895, w * 0.14, h * 0.05); setc(ctx, hx('9aa0aa')); ctx.fill()
    elif mode == 'cartoon':
        cols = (hx('ff3b5c'), hx('ffd23f'), hx('3ccf4e'), hx('1f8bff'), hx('8a3cff'))
        for k, c in enumerate(cols):
            ctx.rectangle(x0, y0 + k * h / 5, w, h / 5 + 1); setc(ctx, c); ctx.fill()
        for k in range(4):
            bx = x0 + w * (0.15 + 0.23 * k); by = y0 + h * 0.5 - abs(math.sin(lf * 0.3 + k)) * h * 0.3
            ellipse(ctx, bx, by, w * 0.07, w * 0.07); fl(ctx, (1, 1, 1), 6)
            ellipse(ctx, bx - w * 0.02, by - w * 0.01, w * 0.012, w * 0.018); setc(ctx, INK); ctx.fill()
            ellipse(ctx, bx + w * 0.02, by - w * 0.01, w * 0.012, w * 0.018); setc(ctx, INK); ctx.fill()
    elif mode == 'love':
        ctx.rectangle(x0, y0, w, h); setc(ctx, hx('ffb3d1')); ctx.fill()
        rnd = random.Random(4)
        for k in range(9):
            hx_ = x0 + rnd.uniform(0.05, 0.95) * w; hy_ = y0 + ((rnd.uniform(0, 1) * h - lf * 4) % (h * 1.2))
            heart(ctx, hx_, hy_, w * rnd.uniform(0.04, 0.08), hx('ff3b7a'))
        heart(ctx, cx, cy, w * 0.16 * (1 + 0.08 * math.sin(lf * 0.5)), hx('ff1f5a'))
    else:
        ctx.rectangle(x0, y0, w, h); setc(ctx, hx('0c0c14')); ctx.fill()
        if off < 1:
            u = eout(off)
            hh = h * (1 - u) ** 3 + 8; ww = w * (1 - u * 0.97)
            ctx.rectangle(cx - ww / 2, cy - hh / 2, ww, hh); setc(ctx, (1, 1, 1, 0.9)); ctx.fill()
        ctx.rectangle(x0 + w * 0.1, y0 + h * 0.1, w * 0.18, h * 0.06); setc(ctx, (1, 1, 1, 0.08)); ctx.fill()
    ctx.restore()
    rect_r(ctx, cx - w / 2, cy - h / 2, w, h, 14); ink(ctx, 7); ctx.stroke()
    # stand
    poly(ctx, [(cx - 60, cy + h / 2 + 30), (cx + 60, cy + h / 2 + 30), (cx + 110, cy + h / 2 + 110), (cx - 110, cy + h / 2 + 110)]); fl(ctx, hx('2a2a3a'), 7)


def heart(ctx, x, y, r, col):
    ctx.new_path(); ctx.move_to(x, y + r)
    ctx.curve_to(x - 1.6 * r, y - 0.2 * r, x - 0.8 * r, y - 1.4 * r, x, y - 0.5 * r)
    ctx.curve_to(x + 0.8 * r, y - 1.4 * r, x + 1.6 * r, y - 0.2 * r, x, y + r); ctx.close_path()
    fl(ctx, col, max(3, r * 0.12))


def plug(ctx, x, y, a, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ctx.move_to(0, 40); ctx.curve_to(0, 160, -80, 200, -60, 320); ink(ctx, 10); ctx.stroke()
    rect_r(ctx, -32, -40, 64, 84, 14); fl(ctx, (1, 1, 1), 6)
    for dx in (-14, 14):
        ctx.rectangle(dx - 5, -78, 10, 40); fl(ctx, hx('d8b84a'), 4)
    ctx.restore()


def drool_bubble(ctx, x, y, r, popped=0.0):
    if popped <= 0:
        ellipse(ctx, x, y, r, r); setc(ctx, (0.8, 0.95, 1, 0.55)); ctx.fill_preserve(); setc(ctx, (1, 1, 1)); ctx.set_line_width(5); ctx.stroke()
        ellipse(ctx, x - r * 0.35, y - r * 0.35, r * 0.18, r * 0.12); setc(ctx, (1, 1, 1)); ctx.fill()
    elif popped < 1:
        for k in range(8):
            a = k * math.pi / 4
            d = r * (0.6 + 1.2 * popped)
            ellipse(ctx, x + math.cos(a) * d, y + math.sin(a) * d, 9 * (1 - popped) + 2, 9 * (1 - popped) + 2); setc(ctx, (0.85, 0.97, 1)); ctx.fill()


def tv_glow(ctx, col, a=0.18):
    ctx.rectangle(-3000, -3000, 7000, 7000); setc(ctx, col + (a,)); ctx.fill()


def sleepy_dad(ctx, x, lf, eye='closed', mouth='open', hold=None, nod=0.0):
    """Dad slumped on the sofa, head lolling back. hold: None | 'remote' | 'banana'. returns body dict"""
    p = sit(torso=-14, head=-22 + 6 * math.sin(lf * 0.12) + nod, eye=eye, mouth=mouth,
            lsh=20, lel=-60, rsh=50, rel=-80)
    b = draw_hip(ctx, x, SEAT, 1.5, 1, DAD, p)
    hx_, hy_ = b['front']
    if hold == 'remote':
        remote(ctx, hx_ + 10, hy_ - 10, 1.3, 0.75)
    elif hold == 'banana':
        banana(ctx, hx_ + 20, hy_ - 10, 1.1, -0.4)
    return b


# ------------------------------------------------------------------ opening
def opening_face(ctx, f, lf, lab=True):
    """ECU: Dad's eyes snap open mid-snore"""
    snap = lf >= 6
    sh = shake_at(lf, [6], 12, 24)
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.06 * eout(pop(lf, 6, 30)), 0, sh, f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('2f3fa8') if not snap else hx('ff4f6a')); ctx.fill()
    rays(ctx, 540, 900, 240, 1700, lf * 0.05, col=(1, 0.95, 0.5) if snap else (0.6, 0.8, 1), a=0.35, n=18)
    cx, cy, R = 540, 900, 320
    if not snap:
        face(ctx, DAD, P(eye='closed', mouth='open', head=0), cx, cy, R, -0.12)
        drool_bubble(ctx, cx + 0.15 * R, cy + 0.72 * R, 40 + 30 * pop(lf, 0, 6))
        zzz(ctx, cx + 260, cy - 200, lf + 20, 1.2)
    else:
        face(ctx, DAD, P(eye='shock', mouth='scream', head=0), cx, cy, R, 0.03 * math.sin(lf * 1.3))
        drool_bubble(ctx, cx + 0.15 * R, cy + 0.72 * R, 70, pop(lf, 6, 14) + 0.001)
        sparkle(ctx, cx - 380, cy - 220, 50 * (1 - pop(lf, 6, 20)) + 1)
        sparkle(ctx, cx + 390, cy - 260, 60 * (1 - pop(lf, 6, 20)) + 1)
    ctx.restore()
    # TV glow in the corner
    tv_glow(ctx, (0.6, 0.85, 1.0), 0.08)
    if lab:
        if not snap:
            label1(ctx, "*SNNNORRK-*", (1, 1, 1), 1, 110)
        else:
            label2(ctx, "\"I WAS WATCHING", "THAT!!\"", (1, 1, 1), pop(lf, 6, 9), 116, col2=YEL)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 50:
        opening_face(ctx, f, f)
    else:
        lf = f - 50
        ctx.save(); cam(ctx, 520, 1120, 1.0 + 0.08 * eout(pop(lf, 0, 60)), 0, 0, f)
        living(ctx, lights=False)
        sofa_back(ctx)
        sleepy_dad(ctx, 360, lf, hold='remote')
        # kid tiptoes in from the doorway
        sofa_front(ctx)
        x = lerp(1050, 740, eout(pop(lf, 0, 50)))
        draw(ctx, x, FLOOR - 186 * 1.25, 1.25, -1, BOY, tiptoe(lf * 0.4, eye='smug', mouth='grin'))
        zzz(ctx, 520, 860, lf, 1.0)
        tv_glow(ctx, (0.6, 0.8, 1.0), 0.14 + 0.05 * math.sin(lf * 0.7))
        ctx.restore()
        label1(ctx, "*SNOOOORE*", (1, 1, 1), pop(lf, 0, 4), 120)
    card(ctx, 'p1', f, -6, 108)


def s2(ctx, f):
    lf = f - 110
    if lf < 40:
        # insert: the remote slides out of Dad's sleeping hand
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.04 * eout(pop(lf, 0, 40)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff7f9a')); ctx.fill()
        for i in range(-6, 16):
            ctx.rectangle(i * 140, -500, 60, 3000); setc(ctx, hx('ff8faa')); ctx.fill()
        # Dad's big hand (palm up, relaxed)
        ellipse(ctx, 330, 1080, 210, 150); fl(ctx, DAD['skin'], 9)
        for k in range(4):
            ctx.save(); ctx.translate(430 + k * 10, 970 + k * 55); ctx.rotate(-0.15 + 0.05 * k)
            rect_r(ctx, 0, -32, 190 - k * 15, 64, 32); fl(ctx, DAD['skin'], 8); ctx.restore()
        ctx.rectangle(-500, 1000, 200, 200); fl(ctx, DAD['shirt'], 9)
        rx = lerp(560, 860, ein(pop(lf, 8, 34)))
        remote(ctx, rx, 1020, 1.45, 1.6)
        # kid's small fingers pulling it
        kx = rx + 170
        for k in range(3):
            ctx.save(); ctx.translate(kx - 20, 980 + k * 42); ctx.rotate(0.1)
            rect_r(ctx, -90, -18, 110, 36, 18); fl(ctx, BOY['skin'], 6); ctx.restore()
        ellipse(ctx, kx + 50, 1020, 70, 80); fl(ctx, BOY['skin'], 7)
        ctx.rectangle(kx + 90, 950, 400, 150); fl(ctx, BOY['shirt'], 7)
        ctx.restore()
        label1(ctx, "*slooowly...*", (1, 1, 1), pop(lf, 2, 6), 110)
    elif lf < 80:
        il = lf - 40
        clicked = il >= 14
        ctx.save(); cam(ctx, 540, 960, 1.0 + 0.05 * eout(pop(il, 14, 30)), 0, shake_at(il, [14], 8, 12), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('1d2c50')); ctx.fill()
        tv(ctx, 540, 900, 820, 560, 'cartoon' if clicked else 'boring', il)
        remote(ctx, 820, 1380, -0.5, 1.3 + 0.1 * (1 if 12 <= il < 16 else 0))
        ctx.restore()
        if clicked:
            label1(ctx, "*CLICK!*", YEL, pop(il, 14, 17), 150, 0.04)
        else:
            label1(ctx, "\"Boring... boring...\"", (1, 1, 1), pop(il, 0, 4), 96)
    elif lf < 102:
        opening_face(ctx, f, lf - 80 + 6)
    else:
        il = lf - 102
        # split screen: kid (top) vs Dad (bottom)
        ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
        ctx.rectangle(0, 0, W, 960); setc(ctx, hx('ffcf3d')); ctx.fill()
        rays(ctx, 540, 640, 200, 1200, il * 0.05, col=(1, 1, 1), a=0.3, n=16)
        face(ctx, BOY, P(eye='shock', mouth='open', head=0), 540, 640, 200, -0.05)
        ctx.restore()
        label(ctx, "\"YOUR EYES WERE CLOSED!\"", 540, 880, 84, (1, 1, 1), -0.02, pop(il, 0, 4))
        ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
        ctx.rectangle(0, 960, W, 960); setc(ctx, hx('6fd6c8')); ctx.fill()
        face(ctx, DAD, P(eye='smug', mouth='smile', head=0), 540, 1170, 190, 0.08)
        ctx.restore()
        ctx.rectangle(0, 952, W, 16); setc(ctx, (1, 1, 1)); ctx.fill()
        if il >= 14:
            label2(ctx, "\"I was RESTING", "my EYES.\"", (1, 1, 1), pop(il, 14, 18), 96, col2=YEL, y=1450)
    card(ctx, 'p2', f, 150, 212)


def s3(ctx, f):
    lf = f - 250
    if lf < 50:
        # 2 seconds later: asleep again, kid swaps remote for a banana
        swapped = lf >= 28
        ctx.save(); cam(ctx, 470, 1100, 1.22, 0, 0, f)
        living(ctx, lights=False)
        sofa_back(ctx)
        sleepy_dad(ctx, 360, lf, hold='banana' if swapped else 'remote')
        sofa_front(ctx)
        bx = lerp(760, 610, eout(pop(lf, 6, 26))) if not swapped else lerp(610, 760, eout(pop(lf, 28, 44)))
        b = draw(ctx, bx, FLOOR - 186 * 1.25, 1.25, -1, BOY,
                 P(torso=-10, lhip=-6, lkn=0, rhip=6, rkn=0, lsh=-80, lel=-10, rsh=20, rel=-60, eye='smug', mouth='grin', head=-6))
        hx_, hy_ = b['front']
        if not swapped:
            banana(ctx, hx_, hy_, 0.9, 0.3)
        else:
            remote(ctx, hx_, hy_, -0.4, 0.6)
        zzz(ctx, 500, 880, lf, 0.9)
        tv_glow(ctx, (0.6, 0.8, 1.0), 0.14)
        ctx.restore()
        label1(ctx, "2 SECONDS LATER...", (1, 1, 1), pop(lf, 0, 4), 92, 0.0, y=560)
        if swapped:
            label1(ctx, "*SWAP*", YEL, pop(lf, 28, 31), 140, 0.04)
        else:
            label1(ctx, "*SNOOORE*", (1, 1, 1), pop(lf, 2, 6), 110)
    elif lf < 100:
        il = lf - 50
        # Dad half-wakes and clicks the banana at the TV
        ctx.save(); cam(ctx, 400, 1050, 1.3 + 0.05 * eout(pop(il, 0, 50)), -3, 0, f)
        living(ctx, lights=False)
        sofa_back(ctx)
        p = sit(torso=-6, head=-6, eye='smug', mouth='wavy', lsh=20, lel=-60, rsh=95, rel=-5)
        b = draw_hip(ctx, 360, SEAT, 1.5, 1, DAD, p)
        hx_, hy_ = b['front']
        jab = 10 * (1 if (il // 5) % 2 == 0 else 0)
        banana(ctx, hx_ + 40 + jab, hy_ - 10, 1.2, -0.2)
        for k in range(3):
            if (il // 5) % 2 == 0:
                ctx.move_to(hx_ + 150, hy_ - 40 + k * 30); ctx.rel_line_to(70, -20 + k * 20)
        setc(ctx, YEL); ctx.set_line_width(9); ctx.stroke()
        sofa_front(ctx)
        tv_glow(ctx, (0.6, 0.8, 1.0), 0.14)
        ctx.restore()
        label1(ctx, "*click click*", YEL, pop(il, 0, 3), 96, 0.04, y=600)
        label2(ctx, "\"I'm... still...", "WATCHING...\"", (1, 1, 1), pop(il, 8, 12), 104, col2=YEL)
    else:
        il = lf - 100
        # kid pulls the plug - TV dies - Dad sleep-talks
        if il < 22:
            ctx.save(); cam(ctx, 540, 960, 1.0, 0, shake_at(il, [8], 10, 14), f)
            ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('1d2c50')); ctx.fill()
            tv(ctx, 540, 860, 820, 560, 'off' if il >= 8 else 'boring', il, off=pop(il, 8, 16))
            plug(ctx, 820 + 40 * eout(pop(il, 2, 8)), 1340 - 60 * eout(pop(il, 2, 8)), 0.2, 1.3)
            ctx.restore()
            label1(ctx, "*YANK!*", YEL, pop(il, 4, 7), 150, -0.04)
        else:
            jl = il - 22
            ctx.save(); cam(ctx, 520, 1100, 1.25, 0, 0, f)
            living(ctx, lights=False)
            sofa_back(ctx)
            sleepy_dad(ctx, 360, jl, mouth='smile', hold='banana')
            sofa_front(ctx)
            b = draw(ctx, 700, FLOOR - 186 * 1.25, 1.25, -1, BOY,
                     P(torso=0, lhip=-6, lkn=0, rhip=6, rkn=0, lsh=150, lel=-40, rsh=-150, rel=40, eye='shock', mouth='open', head=0))
            hx_, hy_ = b['back']
            plug(ctx, hx_, hy_ - 20, 0.0, 0.7)
            ctx.restore()
            label2(ctx, "\"Mmm... GREAT", "show...\"", (1, 1, 1), pop(jl, 2, 6), 110, col2=YEL)
    card(ctx, 'p3', f, 252, 396)


def s4(ctx, f):
    lf = f - 400
    # 11 PM: both asleep on the sofa, zzz duet, push-in
    ctx.save(); cam(ctx, 470, 1060, 1.05 + 0.25 * eout(pop(lf, 0, 100)), 2 * math.sin(lf * 0.05), 0, f)
    living(ctx, lights=False)
    from scenes32 import clock
    clock(ctx, 500, 760, 90, 11, 0)
    sofa_back(ctx)
    sleepy_dad(ctx, 330, lf, hold='banana')
    b = draw_hip(ctx, 560, SEAT + 20, 1.2, -1, BOY, sit(torso=-18, head=-24 + 5 * math.sin(lf * 0.14 + 1), eye='closed', mouth='open',
                                                     lsh=10, lel=-40, rsh=30, rel=-60))
    hx_, hy_ = b['front']
    plug(ctx, hx_, hy_ - 10, 0.6, 0.55)
    sofa_front(ctx)
    zzz(ctx, 430, 780, lf, 1.1)
    zzz(ctx, 640, 860, lf + 21, 0.8, hx('ffd0e6'))
    ctx.restore()
    label2(ctx, "*SNOORE*", "*snore*", (1, 1, 1), pop(lf, 6, 10), 110, col2=hx('ffd0e6'))
    card(ctx, 'p4', f, 402, 496)


def s5(ctx, f):
    lf = f - 500
    if lf < 56:
        # Mom tiptoes in, grabs the remote, plugs in, HER show
        ctx.save(); cam(ctx, 520, 1100, 1.05, 0, 0, f)
        living(ctx, lights=False, door=1.0)
        sofa_back(ctx)
        sleepy_dad(ctx, 330, lf, hold='banana')
        draw_hip(ctx, 560, SEAT + 20, 1.2, -1, BOY, sit(torso=-18, head=-24, eye='closed', mouth='open', lsh=10, lel=-40, rsh=30, rel=-60))
        sofa_front(ctx)
        x = lerp(1000, 880, eout(pop(lf, 0, 24)))
        b = draw(ctx, x, FLOOR - 186 * 1.6, 1.6, -1, MOM,
                 tiptoe(lf * 0.4, eye='smug', mouth='grin') if lf < 24 else
                 P(torso=0, lhip=-8, lkn=0, rhip=8, rkn=0, lsh=-100, lel=-20, rsh=20, rel=-90, eye='smug', mouth='grin', head=-4))
        if lf >= 24:
            hx_, hy_ = b['front']
            remote(ctx, hx_ - 10, hy_ - 10, -1.2, 0.8)
        zzz(ctx, 430, 780, lf, 1.0)
        tv_glow(ctx, hx('ff8fc0'), 0.22 if lf >= 34 else 0.0)
        ctx.restore()
        if lf < 34:
            label2(ctx, "\"Finally...", "MY show.\"", (1, 1, 1), pop(lf, 6, 10), 110, col2=PINK)
        else:
            label1(ctx, "*CLICK!*", PINK, pop(lf, 34, 37), 150, 0.04)
        card(ctx, 'p5', f, 502, 590)
    elif lf < 96:
        il = lf - 56
        # double pop-awake split screen
        sh = shake_at(il, [0], 12, 22)
        for k, (ch, top) in enumerate(((DAD, True), (BOY, False))):
            y0 = 0 if top else 960
            ctx.save(); ctx.rectangle(0, y0, W, 960); ctx.clip()
            ctx.save(); cam(ctx, 540, y0 + 480, 1.0, 0, sh, f + k, sy=y0 + 480)
            ctx.rectangle(-500, y0 - 200, 2200, 1400); setc(ctx, hx('ff4f6a') if top else hx('8a3cff')); ctx.fill()
            rays(ctx, 540, y0 + 520, 180, 1100, il * 0.06, col=(1, 0.95, 0.5), a=0.35, n=16)
            face(ctx, ch, P(eye='shock', mouth='scream', head=0), 540, y0 + (560 if top else 400), 230, 0.04 * math.sin(il * 1.2 + k))
            ctx.restore(); ctx.restore()
        ctx.rectangle(0, 952, W, 16); setc(ctx, (1, 1, 1)); ctx.fill()
        label(ctx, "\"WE WERE WATCHING", 540, 880, 92, (1, 1, 1), -0.03, pop(il, 0, 3))
        label(ctx, "THAT!!\"", 540, 1040, 120, YEL, 0.03, pop(il, 0, 3))
    elif lf < 125:
        il = lf - 96
        # Mom ECU: eyes closed, already dozing
        ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(il, 0, 29)), 0, 0, f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ffb3d1')); ctx.fill()
        rnd = random.Random(2)
        for k in range(10):
            heart(ctx, rnd.uniform(0, W), (rnd.uniform(400, 1500) - il * 6) % 1300 + 300, rnd.uniform(25, 45), hx('ff6fa0'))
        face(ctx, MOM, P(eye='closed', mouth='smile', head=0), 540, 900, 290, -0.1)
        zzz(ctx, 830, 700, il, 1.1, hx('ffffff'))
        ctx.restore()
        label2(ctx, "\"Shh. I'm resting", "my EYES.\"", (1, 1, 1), pop(il, 2, 6), 100, col2=PINK)
    else:
        il = lf - 125
        opening_face(ctx, f, il)
        card(ctx, 'p1', f, 625)


SHOTS = [(0, s1), (110, s2), (250, s3), (400, s4), (500, s5)]
CUTS = (50, 110, 150, 190, 212, 250, 300, 350, 372, 400, 500, 556, 596, 625)


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
                              "-i", "out/watching_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
