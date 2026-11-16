"""'The Family Photo Timer' - original, general-audience comedy short, ~22s.
Hook: ECU of Mom in a matching holiday sweater, manic frozen grin, twitching, sweating: "EVERYBODY... SMILE!"
 -> wide: family on the sofa, Dad at the phone on a tripod: *beep* "10 SECONDS! EASY!"
Beat 1 (ATTEMPT #1): countdown 3-2-1 on the wall, Dad sprints, trips on the rug, flies - *CLICK* - freeze frame: FAIL.
Beat 2: freeze-frame montage slams in: #7 kid blinked, #15 Mom sneezed, #31 Dad still running - FAIL FAIL FAIL;
 split screen: Mom "My face is STUCK." / kid "My cheeks HURT!"
Beat 3 (ATTEMPT #47): low-angle Dad in a headband "ONE. MORE. TIME." - super-speed sprint, dive, perfect landing,
 sparkle smiles, *CLICK* "PERFECT!!" - everyone cheers "WE DID IT!!"
Twist: Dad checks the phone - gallery: 47 photos of DAD's face. "...it was on SELFIE mode." Mom + kid glare,
 Dad: "...one more?" -> loops to Mom's frozen grin."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import pop, sparkle, puff, shake_at
from scenes32 import label, cam, rect_r, rays, face, living, sofa_back, sofa_front, SEAT
from scenes8 import sit
from scenes14 import sweat
from scenes33 import vein
import scenes13
from scenes13 import card as _card13
import random

SW = hx('e0263a')
BOY = dict(doodle.BOY, shirt=SW)
MOM = dict(doodle.MOM_G, shirt=SW)
DAD = dict(doodle.DAD, shirt=SW)
N = 660
FLOOR = 1460
RED = hx('ff3b5c')
PINK = hx('ff5fa8')
ORANGE = hx('ff8a1f')
PURPLE = hx('8a3cff')
GREEN = hx('22b45a')
BLUE = hx('1f8bff')
YEL = hx('fff27a')
LY = 1450
SOFA_DX = -100            # sofa group shifted left to make room for the tripod
SEATS = (280, 480, 680)   # mom, kid, dad (pre-shift)
TRI_X = 960

CAPS = {
    'p1': [[("THE FAMILY PHOTO", OUT)], [("WITH A 10-SECOND TIMER", RED)]],
    'p2': [[("ATTEMPT #1:", OUT)], [("PRESS. RUN. PRAY.", ORANGE)]],
    'p3': [[("ATTEMPT #31:", OUT)], [("SMILES START CRACKING", PURPLE)]],
    'p4': [[("ATTEMPT #47:", OUT)], [("DAD GOES PRO", GREEN)]],
    'p5': [[("PLOT TWIST:", OUT)], [("WRONG CAMERA", PINK)]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def sweater_pattern(ctx, b, s=1.0):
    pass


def tripod(ctx, x, lf=0, rec=False):
    top = 1060
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for dx in (-90, 0, 90):
        ctx.move_to(x, top + 60); ctx.line_to(x + dx, FLOOR + 30 + (12 if dx == 0 else 0))
        setc(ctx, OUT); ctx.set_line_width(22); ctx.stroke_preserve(); setc(ctx, hx('5a5a6a')); ctx.set_line_width(10); ctx.stroke()
    rect_r(ctx, x - 26, top + 40, 52, 40, 8); fl(ctx, hx('3a3a4a'), 5)
    rect_r(ctx, x - 70, top - 110, 140, 160, 18); fl(ctx, hx('24243a'), 7)   # phone, sideways-ish
    ellipse(ctx, x - 30, top - 70, 18, 18); fl(ctx, hx('4a4a6a'), 4)
    if rec and (lf // 6) % 2 == 0:
        ellipse(ctx, x + 36, top - 74, 13, 13); fl(ctx, RED, 3)


def rug(ctx):
    ellipse(ctx, 640, FLOOR + 60, 330, 46); fl(ctx, hx('3d7bff'), 7)
    ellipse(ctx, 640, FLOOR + 60, 250, 30); ink(ctx, 4); ctx.stroke()


def countdown(ctx, s, t=1.0, col=(1, 1, 1)):
    if t <= 0:
        return
    sc = 0.6 + 0.4 * eout(min(1, t * 2))
    ctx.save(); ctx.translate(560, 770); ctx.scale(sc, sc)
    ctx.push_group()
    text(ctx, s, 0, 0, 300, col, ow=20, shadow=False)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(0.85)
    ctx.restore()


def flash(ctx, u):
    if 0 <= u < 1:
        ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.95 * (1 - u) ** 1.5)); ctx.fill()


def headband(ctx, b):
    hx_, hy_ = b['head']; R = b['R']
    rect_r(ctx, hx_ - 1.02 * R, hy_ - 0.62 * R, 2.04 * R, 0.24 * R, 0.1 * R); fl(ctx, hx('ffffff'), 5)
    poly(ctx, [(hx_ - 0.95 * R, hy_ - 0.5 * R), (hx_ - 1.5 * R, hy_ - 0.75 * R), (hx_ - 1.45 * R, hy_ - 0.3 * R)]); fl(ctx, hx('ffffff'), 5)


def stamp(ctx, s, x, y, t, ang=-0.25, col=RED):
    if t <= 0:
        return
    sc = 1.8 - 0.8 * eout(min(1, t))
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(sc, sc)
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(220)
    w = ctx.text_extents(s).x_advance
    rect_r(ctx, -w / 2 - 40, -195, w + 80, 260, 30); setc(ctx, col); ctx.set_line_width(22); ctx.stroke()
    ctx.move_to(-w / 2, 0); ctx.text_path(s); setc(ctx, col); ctx.fill()
    ctx.restore()


# ------------------------------------------------------------------ the family scene
def fam(ctx, f, lf, mom=('normal', 'smile'), kid=('normal', 'smile'), dad=None, z=0.95, cx=520, cy=1110, shake=0,
        cnt=None, cnt_t=1.0, rec=False, mom_p=None, kid_p=None, sparkles=False, ghosts=()):
    """dad: None | ('seat', eye, mouth, extra) | ('stand', x, hipy, pose, f)"""
    ctx.save(); cam(ctx, cx, cy, z, 0, shake, f)
    living(ctx)
    if cnt:
        countdown(ctx, cnt, cnt_t)
    rug(ctx)
    ctx.save(); ctx.translate(SOFA_DX, 0)
    sofa_back(ctx)
    bm = draw_hip(ctx, SEATS[0], SEAT, 1.12, 1, MOM, mom_p or sit(eye=mom[0], mouth=mom[1], head=4, rsh=40, rel=-90))
    bk = draw_hip(ctx, SEATS[1], SEAT + 10, 0.95, 1, BOY, kid_p or sit(eye=kid[0], mouth=kid[1], head=-4))
    bd = None
    if dad and dad[0] == 'seat':
        p = sit(eye=dad[1], mouth=dad[2], head=-4, lsh=-30, lel=-40, rsh=60, rel=-80)
        p.update(dad[3] if len(dad) > 3 else {})
        bd = draw_hip(ctx, SEATS[2], SEAT, 1.15, -1, DAD, p)
    sofa_front(ctx)
    ctx.restore()
    tripod(ctx, TRI_X, lf, rec)
    for gx, ghy, gp, ga in ghosts:
        ctx.push_group(); draw_hip(ctx, gx, ghy, 1.15, -1, DAD, gp); ctx.pop_group_to_source(); ctx.paint_with_alpha(ga)
    if dad and dad[0] == 'stand':
        bd = draw_hip(ctx, dad[1], dad[2], 1.15, dad[4], DAD, dad[3])
    if sparkles:
        for j in range(6):
            sparkle(ctx, 150 + j * 130, 820 + 50 * math.sin(lf * 0.3 + j * 1.7), 28 + 8 * math.sin(lf * 0.5 + j), YEL)
    ctx.restore()
    return bm, bk, bd


def freeze_card(ctx, f, draw_fn, u, ang, s1=0.64, cx=540, cy=930, note=None, fail_t=0.0):
    """draws a full-frame scene shrunk into a white-bordered snapshot card"""
    s = 1.0 + (s1 - 1.0) * eout(clamp(u))
    a = ang * eout(clamp(u))
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(a); ctx.scale(s, s); ctx.translate(-W / 2, -H / 2)
    ctx.rectangle(-44 + 18, -44 + 22, W + 88, H + 88); setc(ctx, (0, 0, 0, 0.35)); ctx.fill()
    ctx.rectangle(-44, -44, W + 88, H + 88); fl(ctx, (1, 1, 1), 10)
    ctx.save(); ctx.rectangle(0, 0, W, H); ctx.clip()
    draw_fn(ctx)
    ctx.rectangle(0, 0, W, H); setc(ctx, (1, 0.95, 0.85, 0.12)); ctx.fill()
    ctx.restore()
    if note:
        text(ctx, note, 230, 1560, 170, (1, 1, 1), ow=16, ang=-0.06)
    stamp(ctx, "FAIL", 560, 1150, fail_t, -0.22)
    ctx.restore()


def table_bg(ctx, lf, col=hx('2a2a5a')):
    ctx.rectangle(0, 0, W, H); setc(ctx, col); ctx.fill()
    rays(ctx, 540, 960, 200, 1700, lf * 0.015, col=(1, 1, 1), a=0.08, n=18)


# ------------------------------------------------------------------ opening
def opening_face(ctx, f, lf, lab=True):
    tw = 0.025 * math.sin(lf * 2.3) + (0.03 * math.sin(lf * 9.1) if (lf // 9) % 3 == 1 else 0)
    ctx.save(); cam(ctx, 540, 1000, 1.0 + 0.05 * eout(pop(lf, 0, 40)), 0, shake_at(lf, [0], 8, 10), f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8ac0')); ctx.fill()
    rays(ctx, 540, 960, 240, 1700, lf * 0.02, col=(1, 1, 1), a=0.3, n=16)
    face(ctx, MOM, P(eye='shock', mouth='grin', head=0), 540, 960, 310, tw)
    sweat(ctx, 250, 700, lf * 2, 1.2)
    vein(ctx, 760, 690, 1.2 + 0.15 * math.sin(lf * 0.9))
    # cheek strain lines
    for sx in (-1, 1):
        for k in range(3):
            ctx.move_to(540 + sx * (330 + k * 22), 1090 - k * 26); ctx.line_to(540 + sx * (380 + k * 22), 1070 - k * 26)
    ink(ctx, 7); ctx.stroke()
    ctx.restore()
    if lab:
        label(ctx, "\"EVERYBODY... SMILE!\"", 540, LY + 40, 104, YEL, -0.03, pop(lf, 0, 4) if lf > 0 else 1)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    if f < 50:
        opening_face(ctx, f, f)
    else:
        lf = f - 50
        pressed = lf >= 18
        fam(ctx, f, lf, mom=('shock', 'grin'), kid=('normal', 'grin'),
            dad=('stand', 860, FLOOR - 220, P(eye='happy' if pressed else 'normal', mouth='grin', rsh=-80 if not pressed else -150,
                                              rel=-10 if not pressed else -40, lsh=20, lel=-20, head=4), 1),
            cnt="10" if pressed else None, cnt_t=pop(lf, 18, 24), rec=pressed, shake=shake_at(lf, [0], 6, 8))
        if lf < 18:
            label(ctx, "*boop*", 540, LY + 40, 110, (1, 1, 1), 0.03, pop(lf, 4, 8))
        else:
            label(ctx, "\"10 SECONDS! EASY!\"", 540, LY + 40, 100, YEL, -0.03, pop(lf, 18, 22))
    card(ctx, 'p1', f, -6, 108)


def dad_flight(lf):
    """Dad's sprint + trip; returns (x, hipy, pose, rot)"""
    if lf < 18:
        x = 860 - 9 * lf
        return x, FLOOR - 220, run_pose(lf * 0.9, eye='shock', mouth='scream', torso=20)
    u = clamp((lf - 18) / 22)
    x = 860 - 9 * 18 - 330 * u
    hy = FLOOR - 220 - 170 * math.sin(math.pi * min(1, u * 1.1)) + 60 * u
    p = P(eye='shock', mouth='scream', rot=85 * eout(min(1, u * 2)), lsh=-160, lel=-10, rsh=-170, rel=-10,
          lhip=-20, lkn=-40, rhip=10, rkn=-60, torso=0)
    return x, hy, p


def s2(ctx, f):
    lf = f - 110
    CLICK = 32
    def scene_at(c, l):
        x, hy, p = dad_flight(l)
        cnt = "3" if l < 10 else ("2" if l < 20 else "1")
        st = 0 if l < 10 else (10 if l < 20 else 20)
        fam(c, f, l, mom=('shock', 'open') if l >= 20 else ('shock', 'grin'), kid=('shock', 'scream') if l >= 20 else ('normal', 'grin'),
            dad=('stand', x, hy, p, -1), cnt=cnt, cnt_t=pop(l, st, st + 5), rec=True, shake=shake_at(l, [18], 8, 14))
    if lf < CLICK:
        scene_at(ctx, lf)
        if lf < 18:
            label(ctx, "*RUN RUN RUN*", 540, LY + 40, 110, (1, 1, 1), 0.03 * math.sin(lf), pop(lf, 0, 4))
        else:
            label(ctx, "*TRIP!*", 540, LY + 40, 140, ORANGE, -0.05, pop(lf, 18, 22))
    else:
        il = lf - CLICK
        table_bg(ctx, il)
        freeze_card(ctx, f, lambda c: scene_at(c, CLICK), pop(il, 4, 16), -0.07, fail_t=pop(il, 24, 30))
        flash(ctx, il / 8)
        if il < 24:
            label(ctx, "*CLICK!*", 540, LY + 40, 140, (1, 1, 1), -0.03, pop(il, 0, 4))
        else:
            label(ctx, "ATTEMPT #1", 540, LY + 40, 110, RED, 0.03, pop(il, 24, 28))
    card(ctx, 'p2', f, 112, 228)


MONTAGE = [  # (note, mom, kid, dad, angle)
    ("#7", ('shock', 'grin'), ('closed', 'grin'), ('seat', 'happy', 'grin'), 0.08),
    ("#15", ('closed', 'scream'), ('shock', 'open'), ('seat', 'shock', 'open'), -0.1),
    ("#31", ('glare', 'flat'), ('normal', 'flat'), None, 0.05),
]


def montage_scene(c, f, k):
    note, mom, kid, dad, ang = MONTAGE[k]
    if dad is None:   # Dad still running, half out of frame
        dad = ('stand', 940, FLOOR - 220, run_pose(1.3, eye='shock', mouth='scream', torso=20), -1)
    fam(c, f, 0, mom=mom, kid=kid, dad=dad, rec=True)
    if k == 1:   # sneeze spray
        c.save(); cam(c, 520, 1110, 0.95, 0, 0, f)
        for j in range(9):
            ellipse(c, 260 + 40 * j, 880 + 30 * math.sin(j * 1.7), 14, 14); fl(c, hx('bff3ff'), 3)
        text(c, "ACHOO!", 300, 760, 110, YEL, ow=12, ang=-0.15)
        c.restore()


def s3(ctx, f):
    lf = f - 230
    if lf < 78:
        table_bg(ctx, lf, hx('3a2a6a'))
        k_now = min(2, lf // 26)
        for k in range(k_now + 1):
            il = lf - 26 * k
            u = pop(il, 0, 7)
            s1_ = 0.6 - 0.02 * (k_now - k)
            ctx.save()
            s = 1.0 + 0.5 * (1 - eout(u))
            ctx.translate(540, 930); ctx.scale(s, s); ctx.translate(-540, -930)
            freeze_card(ctx, f, lambda c, k=k: montage_scene(c, f, k), 1.0, MONTAGE[k][4], s1=s1_, cx=540 + (k - 1) * 30,
                        cy=930 + (k - 1) * 20, note=MONTAGE[k][0], fail_t=pop(il, 9, 14))
            ctx.restore()
        il = lf - 26 * k_now
        flash(ctx, il / 6)
        names = ("\"Who BLINKED?!\"", "\"Bless you...\"", "\"DAD!!!\"")
        label(ctx, names[k_now], 540, LY + 40, 110, YEL, -0.03, pop(il, 4, 8))
    else:
        il = lf - 78
        tw = 0.04 * math.sin(il * 7.3) * (1 if il > 10 else 0.3)
        # split screen: Mom (top) / kid (bottom), smiles cracking
        ctx.save(); ctx.rectangle(0, 0, W, 960); ctx.clip()
        cam(ctx, 540, 600, 1.0 + 0.05 * eout(pop(il, 0, 60)), 0, shake_at(il, [0], 6, 8), f, sy=520)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff8ac0')); ctx.fill()
        rays(ctx, 540, 600, 200, 1200, il * 0.02, col=(1, 1, 1), a=0.3, n=16)
        face(ctx, MOM, P(eye='shock', mouth='grin', head=0), 540, 690, 180, tw)
        sweat(ctx, 360, 560, il * 3, 0.8); vein(ctx, 690, 560, 0.8)
        ctx.restore()
        ctx.save(); ctx.rectangle(0, 960, W, 960); ctx.clip()
        cam(ctx, 540, 1230, 1.0 + 0.05 * eout(pop(il, 0, 60)), 0, shake_at(il, [20], 6, 10), f, sy=1220)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('6fd6ff')); ctx.fill()
        rays(ctx, 540, 1230, 200, 1200, -il * 0.02, col=(1, 1, 1), a=0.3, n=16)
        face(ctx, BOY, P(eye='closed', mouth='grin', head=0), 540, 1230, 220, -tw)
        sweat(ctx, 740, 1080, il * 3 + 20, 0.9)
        # cheek cracks
        if il > 20:
            for sx in (-1, 1):
                ctx.move_to(540 + sx * 170, 1290); ctx.line_to(540 + sx * 200, 1320); ctx.line_to(540 + sx * 185, 1345); ctx.line_to(540 + sx * 215, 1370)
            ink(ctx, 6); ctx.stroke()
        ctx.restore()
        ctx.rectangle(0, 952, W, 16); setc(ctx, OUT); ctx.fill()
        label(ctx, "\"My face is STUCK.\"", 540, 912, 76, YEL, -0.02, pop(il, 2, 6))
        if il >= 20:
            label(ctx, "\"My cheeks HURT!\"", 540, LY + 40, 100, (1, 1, 1), 0.03, pop(il, 20, 24))
    card(ctx, 'p3', f, 232, 368)


def s4(ctx, f):
    lf = f - 370
    if lf < 36:
        # low-angle hero shot: Dad in a headband
        ctx.save(); cam(ctx, 540, 1150, 1.25 + 0.08 * eout(pop(lf, 0, 36)), -6, shake_at(lf, [0], 10, 14), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('ff5a3c')); ctx.fill()
        rays(ctx, 540, 900, 200, 1700, lf * 0.03, col=(1, 0.85, 0.4), a=0.4, n=18)
        b = draw_hip(ctx, 540, 1500, 1.7, 1, DAD, P(eye='glare', mouth='flat', rsh=-160, rel=-20, lsh=40, lel=-110, head=0,
                                                   lhip=-14, rhip=14))
        headband(ctx, b)
        ctx.restore()
        label(ctx, "\"ONE. MORE. TIME.\"", 540, LY + 40, 108, YEL, -0.03, pop(lf, 4, 8))
    elif lf < 130:
        il = lf - 36
        CL = 46
        if il < 8:
            dad = ('stand', 860, FLOOR - 220, P(eye='glare', mouth='flat', rsh=-150, rel=-40, head=4), 1)
            ghosts = ()
        elif il < 20:
            u = (il - 8) / 12
            x = 860 - 200 * u
            dad = ('stand', x, FLOOR - 220 - 60 * math.sin(math.pi * u), run_pose(il * 1.4, eye='glare', mouth='flat', torso=30,
                                                                                  rot=40 * u), -1)
            ghosts = [(x + 70 * g, FLOOR - 220, run_pose((il - g) * 1.4, torso=30), 0.25 - 0.06 * g) for g in range(1, 4)]
        else:
            dad = ('seat', 'happy' if il < CL + 4 else 'happy', 'grin', dict(rsh=-150, rel=-30) if il >= CL + 8 else {})
            ghosts = ()
        seated = il >= 20
        cnt = "3" if il < 16 else ("2" if il < 30 else "1")
        st = 0 if il < 16 else (16 if il < 30 else 30)
        cheer = il >= CL + 8
        fam(ctx, f, il, mom=('happy', 'grin') if seated else ('shock', 'grin'), kid=('happy', 'grin') if seated else ('shock', 'grin'),
            dad=dad, cnt=cnt if il < CL else None, cnt_t=pop(il, st, st + 5), rec=il < CL, shake=shake_at(il, [8, 20], 8, 14),
            sparkles=seated, ghosts=ghosts, z=0.95 + (0.06 * eout(pop(il, CL, CL + 12)) if il >= CL else 0),
            mom_p=sit(eye='happy', mouth='scream', rsh=-150, rel=-30, lsh=-150, lel=-30) if cheer else None,
            kid_p=sit(eye='happy', mouth='scream', rsh=-150, rel=-30, lsh=-150, lel=-30, head=-4) if cheer else None)
        if il < 20:
            ctx.save()
            for k in range(12):
                rnd = random.Random(il // 2 * 13 + k)
                y = rnd.uniform(1050, 1450); x = rnd.uniform(300, 900); L = rnd.uniform(140, 320)
                ctx.move_to(x, y); ctx.line_to(x + L, y)
            setc(ctx, (1, 1, 1, 0.75)); ctx.set_line_width(9); ctx.stroke(); ctx.restore()
        if il >= 20 and il < 24:
            for j in range(4):
                puff(ctx, 330 + j * 90, 1130, (il - 20) / 4, 1.6)
        if il >= CL:
            flash(ctx, (il - CL) / 9)
        if il < 20:
            label(ctx, "*ZOOOOOM!*", 540, LY + 40, 130, YEL, 0.03 * math.sin(il * 0.8), pop(il, 0, 4))
        elif il < CL:
            label(ctx, "*perfect landing*", 540, LY + 40, 100, (1, 1, 1), -0.03, pop(il, 20, 24))
        elif il < CL + 8:
            label(ctx, "*CLICK!*", 540, LY + 40, 140, (1, 1, 1), -0.03, pop(il, CL, CL + 3))
        else:
            label(ctx, "\"WE DID IT!!\"", 540, LY + 40, 130, YEL, -0.03, pop(il, CL + 8, CL + 12))
            for j in range(14):   # confetti
                rnd = random.Random(j)
                x = rnd.uniform(80, 1000); y = 500 + (il - CL - 8) * rnd.uniform(14, 24) + rnd.uniform(-200, 0)
                ctx.save(); ctx.translate(x, y); ctx.rotate(il * 0.3 + j)
                ctx.rectangle(-14, -8, 28, 16); fl(ctx, (YEL, PINK, BLUE, GREEN)[j % 4], 3); ctx.restore()
    card(ctx, 'p4', f, 372, 498)


THUMBS = [('shock', 'scream'), ('glare', 'flat'), ('happy', 'grin'), ('shock', 'open'), ('normal', 'wavy'), ('closed', 'grin'),
          ('smug', 'smile'), ('shock', 'scream'), ('happy', 'open')]
TCOL = [hx('ffd23f'), hx('6fd6ff'), hx('ff8ac0'), hx('b98aff'), hx('8fe39a'), hx('ffb85a'), hx('6fd6ff'), hx('ff8ac0'), hx('ffd23f')]


def gallery(ctx, il, f):
    ctx.save(); cam(ctx, 540, 1010 if il < 30 else 1010 - 60 * eout(pop(il, 30, 40)), 1.0 + 0.25 * eout(pop(il, 30, 40)),
                    2, shake_at(il, [0, 30], 10, 16), f)
    ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('1f8bff')); ctx.fill()
    rays(ctx, 540, 960, 200, 1600, il * 0.04, col=(1, 1, 1), a=0.18, n=18)
    rect_r(ctx, 170, 540, 740, 1060, 70); fl(ctx, hx('24243a'), 10)
    rect_r(ctx, 205, 590, 670, 960, 40); setc(ctx, (1, 1, 1)); ctx.fill()
    ctx.save(); rect_r(ctx, 205, 590, 670, 960, 40); ctx.clip()
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(58)
    s = "Photos (47)"; w = ctx.text_extents(s).x_advance
    ctx.move_to(540 - w / 2, 690); ctx.text_path(s); setc(ctx, OUT); ctx.fill()
    for k in range(9):
        r, c = divmod(k, 3)
        x0 = 230 + c * 210; y0 = 740 + r * 210
        ctx.save(); rect_r(ctx, x0, y0, 200, 200, 16); ctx.clip()
        ctx.rectangle(x0, y0, 200, 200); setc(ctx, TCOL[k]); ctx.fill()
        e, m = THUMBS[k]
        face(ctx, DAD, P(eye=e, mouth=m, head=0), x0 + 100, y0 + 120, 120, 0.15 * math.sin(k * 2.1))
        ctx.restore()
        rect_r(ctx, x0, y0, 200, 200, 16); ink(ctx, 5); ctx.stroke()
    ctx.restore()
    ellipse(ctx, 540, 1585, 34, 12); setc(ctx, (1, 1, 1, 0.4)); ctx.fill()
    ctx.restore()


def s5(ctx, f):
    lf = f - 500
    if lf < 36:
        # Dad ECU looking at the phone
        shock = lf >= 18
        ctx.save(); cam(ctx, 540, 1000, 1.0 + (0.12 * eout(pop(lf, 18, 24)) if shock else 0), 0, shake_at(lf, [18], 12, 18), f)
        ctx.rectangle(-500, -500, 2200, 3000); setc(ctx, hx('8fe39a') if not shock else hx('2a2a5a')); ctx.fill()
        rays(ctx, 540, 900, 200, 1600, lf * 0.03, col=(1, 1, 1), a=0.25, n=16)
        face(ctx, DAD, P(eye='happy' if not shock else 'shock', mouth='grin' if not shock else 'scream', head=0), 540, 880, 270, 0.03)
        if shock:
            sweat(ctx, 300, 660, lf * 3, 1.1)
        # phone back + hands
        rect_r(ctx, 400, 1180, 280, 380, 40); fl(ctx, hx('24243a'), 9)
        ellipse(ctx, 450, 1240, 22, 22); fl(ctx, hx('4a4a6a'), 4)
        ellipse(ctx, 390, 1420, 60, 90); fl(ctx, DAD['skin'], 7)
        ellipse(ctx, 690, 1420, 60, 90); fl(ctx, DAD['skin'], 7)
        ctx.restore()
        if not shock:
            label(ctx, "\"Let's see it!\"", 540, LY + 40, 110, (1, 1, 1), -0.03, pop(lf, 2, 6))
        else:
            label(ctx, "\"...uh oh.\"", 540, LY + 40, 130, YEL, 0.03, pop(lf, 18, 22))
    elif lf < 96:
        il = lf - 36
        gallery(ctx, il, f)
        if il < 30:
            label(ctx, "*47 photos of... DAD*", 540, LY + 40, 92, YEL, -0.03, pop(il, 2, 6))
        else:
            label(ctx, "\"...it was on SELFIE mode.\"", 540, LY + 40, 84, (1, 1, 1), -0.02, pop(il, 30, 34))
    elif lf < 124:
        il = lf - 96
        fam(ctx, f, il, mom=('glare', 'flat'), kid=('glare', 'flat'),
            dad=('seat', 'normal', 'wavy', dict(rsh=-120, rel=-60)), z=0.95 + 0.05 * eout(pop(il, 0, 28)), cx=420, cy=1080,
            shake=shake_at(il, [0], 6, 8),
            mom_p=sit(eye='glare', mouth='flat', head=14, rsh=40, rel=-110, lsh=30, lel=-110),
            kid_p=sit(eye='glare', mouth='flat', head=14, rsh=40, rel=-110, lsh=30, lel=-110))
        label(ctx, "\"...one more?\"", 540, LY + 40, 120, YEL, -0.03, pop(il, 4, 8))
    else:
        il = lf - 124
        opening_face(ctx, f, il)
    if lf < 124:
        card(ctx, 'p5', f, 502, 622)
    else:
        card(ctx, 'p1', f, 626)


SHOTS = [(0, s1), (110, s2), (230, s3), (370, s4), (500, s5)]
CUTS = (50, 110, 230, 308, 370, 406, 500, 536, 596, 624)


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
                              "-i", "out/family_photo_timer_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
