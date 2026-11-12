"""'Are You Asleep?' - original, general-audience comedy short, ~35s.
A kid fakes sleep when Mom checks on him... and the twist shows where he learned it."""
from eng3 import *
import doodle, sys, subprocess
from doodle import INK, fl, ink, draw, draw_hip
from scenes6 import cam, pop, sparkle, label, shake_at
from scenes8 import walk
from scenes11 import half
from scenes13 import card as _card13
import scenes13

BOY, MOM, DAD = doodle.BOY, doodle.MOM_G, doodle.DAD
N = 1050
STAND = 1500
KB, KM = 1.2, 1.55
HIP = (600, 1150)               # boy hip while lying in bed
DOOR = (1060, 640, 300, 860)    # x, y, w, h  (world coords, right side of kid's room)

CAPS = {
    'p1': [[("WHEN MOM CHECKS", OUT)], [("IF YOU'RE ", OUT), ("ASLEEP", hx('1f8bff'))]],
    'p2': [[("0.5 SECONDS", hx('ff3b5c')), (" TO", OUT)], [("LOOK ASLEEP", OUT)]],
    'p3': [[("THE ", OUT), ("FAKE SNORE", hx('8a3cff'))]],
    'p4': [[("THE ", OUT), ("INSPECTION", hx('e07b12'))]],
    'p5': [[("THEN THE PHONE", OUT)], [("BUZZED", hx('ff3b5c')), ("...", OUT)]],
    'p6': [[("SHE BOUGHT IT...", OUT)], [("RIGHT?", hx('8a3cff'))]],
    'p7': [[("GUESS WHERE HE", OUT)], [("LEARNED IT", hx('ff3b5c'))]],
}
scenes13.CAPS = CAPS
card = _card13


# ------------------------------------------------------------------ props
def phone(ctx, x, y, s=1.0, a=0.0, on=True, buzz=0):
    ctx.save(); ctx.translate(x + (math.sin(buzz * 3.1) * 6 if buzz else 0), y); ctx.rotate(a); ctx.scale(s, s)
    rect_r(ctx, -32, -56, 64, 112, 12); fl(ctx, hx('2a2f45'), 5)
    rect_r(ctx, -24, -46, 48, 88, 6); setc(ctx, hx('6be2ff') if on else hx('3a4258')); ctx.fill()
    if on:
        for i in range(3):
            ellipse(ctx, -10 + i * 10, -10 + (i % 2) * 18, 6, 6); setc(ctx, (hx('ffd23f'), hx('ff3b8a'), hx('5fd07a'))[i]); ctx.fill()
    ctx.restore()


def rect_r(ctx, x, y, w, h, r):
    ctx.new_path(); ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); ctx.close_path()


def glow(ctx, x, y, r, col=(0.42, 0.88, 1.0), a=0.55):
    g = cairo.RadialGradient(x, y, 10, x, y, r)
    g.add_color_stop_rgba(0, col[0], col[1], col[2], a); g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    ctx.set_source(g); ctx.arc(x, y, r, 0, 7); ctx.fill()


def lying(**kw):
    p = P(rot=-90, head=-4, lsh=-170, lel=-30, rsh=-60, rel=-80, lhip=4, lkn=-6, rhip=10, rkn=-12, eye='closed', mouth='smile')
    p.update(kw); return p


def kid_room(ctx, f, door=0.0, theme=0):
    """door: 0 closed .. 1 fully open. theme 0 = kid room, 1 = parents' room"""
    wall = hx('5a6fd8') if theme == 0 else hx('b0577f')
    ctx.rectangle(-900, -900, 3200, 2400); setc(ctx, wall); ctx.fill()
    # wallpaper pattern
    rnd = random.Random(4 + theme)
    for _ in range(40):
        x, y = rnd.uniform(-600, 1900), rnd.uniform(200, 1450)
        if theme == 0:
            sparkle(ctx, x, y, 14, light(wall, 0.25))
        else:
            ellipse(ctx, x, y, 10, 10); setc(ctx, light(wall, 0.2)); ctx.fill()
    # window with moon + stars
    ctx.rectangle(-420, 520, 360, 420); fl(ctx, hx('16204f'), 8)
    ellipse(ctx, -150, 620, 46, 46); setc(ctx, hx('fff2b0')); ctx.fill()
    ellipse(ctx, -132, 606, 40, 40); setc(ctx, hx('16204f')); ctx.fill()
    for sx, sy in ((-360, 600), (-300, 820), (-200, 880), (-110, 760)):
        sparkle(ctx, sx, sy, 12, (1, 1, 1))
    ctx.move_to(-240, 520); ctx.line_to(-240, 940); ink(ctx, 6); ctx.stroke()
    if theme == 0:
        # abstract posters (rocket + planet)
        ctx.rectangle(330, 520, 220, 280); fl(ctx, hx('ffd23f'), 7)
        poly(ctx, [(440, 560), (480, 680), (400, 680)]); fl(ctx, hx('ff3b5c'), 5)
        ctx.rectangle(415, 680, 50, 60); fl(ctx, (1, 1, 1), 5)
        ctx.rectangle(640, 560, 220, 200); fl(ctx, hx('5fd07a'), 7)
        ellipse(ctx, 750, 660, 60, 60); fl(ctx, hx('ff8a3d'), 5)
        ellipse(ctx, 750, 660, 100, 22, -0.3); ink(ctx, 6); ctx.stroke()
    else:
        ctx.rectangle(400, 520, 420, 260); fl(ctx, hx('fff1c9'), 8)
        ctx.new_path(); ctx.move_to(420, 760); ctx.line_to(540, 620); ctx.line_to(640, 720); ctx.line_to(700, 660); ctx.line_to(800, 760); ctx.close_path(); fl(ctx, hx('5fd07a'), 5)
        ellipse(ctx, 740, 590, 30, 30); fl(ctx, hx('ffd23f'), 4)
    # door frame + hallway light behind
    x, y, w, h = DOOR
    ctx.rectangle(x - 18, y - 18, w + 36, h + 18); fl(ctx, hx('f2e6d0'), 8)
    ctx.rectangle(x, y, w, h); setc(ctx, hx('ffe9a8')); ctx.fill()
    # door panel swings open (narrows toward the hinge on the right)
    pw = w * (1 - door * 0.82)
    ctx.rectangle(x + w - pw, y, pw, h); fl(ctx, hx('c98b55') if theme == 0 else hx('8a5a34'), 7)
    if door < 0.5:
        ellipse(ctx, x + w - pw + 40, y + h * 0.55, 13, 13); fl(ctx, hx('ffd23f'), 4)
    # floor
    ctx.rectangle(-900, STAND, 3200, 900); setc(ctx, hx('7a5236') if theme == 0 else hx('6a4630')); ctx.fill()
    ctx.move_to(-900, STAND); ctx.line_to(2300, STAND); ink(ctx, 8); ctx.stroke()


def bed_back(ctx, theme=0):
    # headboard + frame (drawn behind the sleeper)
    ctx.rectangle(60, 960, 70, 560); fl(ctx, hx('ff8a3d') if theme == 0 else hx('3fb5a5'), 8)
    ellipse(ctx, 95, 960, 50, 30); fl(ctx, hx('ff8a3d') if theme == 0 else hx('3fb5a5'), 8)
    ctx.rectangle(110, 1250, 820, 120); fl(ctx, (1, 1, 1), 7)   # mattress
    ctx.rectangle(110, 1370, 820, 80); fl(ctx, hx('c98b55'), 7)
    ctx.rectangle(110, 1450, 820, 50); fl(ctx, hx('8a5a34'), 6)


def pillow(ctx, puff_=0.0, glow_a=0.0):
    ctx.save(); ctx.translate(250, 1215); ctx.scale(1 + puff_ * 0.05, 1 + puff_ * 0.12)
    ctx.new_path(); ctx.move_to(-130, 20); ctx.curve_to(-150, -60, 140, -70, 130, 20); ctx.curve_to(140, 60, -140, 60, -130, 20); ctx.close_path()
    fl(ctx, hx('fff6e0'), 7)
    ctx.restore()


def blanket(ctx, x0=470, x1=950, y=1250, b=0.0, col=hx('ff3b8a')):
    ctx.new_path(); ctx.move_to(x0 - 30, y + 30); ctx.curve_to(x0 - 40, y - 150 - b, x1, y - 140 - b, x1 + 10, y + 30)
    ctx.line_to(x1 + 10, y + 120); ctx.line_to(x0 - 30, y + 120); ctx.close_path()
    fl(ctx, col, 7)
    for i in range(1, 6):
        xx = lerp(x0, x1, i / 6)
        ellipse(ctx, xx, y - 40 - b * 0.4, 16, 16); setc(ctx, light(col, 0.45)); ctx.fill()


def dark_with_wedge(ctx, wedge=None, a=0.78):
    """darken everything except an optional light wedge polygon"""
    ctx.new_path(); ctx.rectangle(-3000, -3000, 9000, 9000)
    if wedge:
        ctx.move_to(*wedge[0])
        for p_ in wedge[1:]:
            ctx.line_to(*p_)
        ctx.close_path()
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    setc(ctx, (0.03, 0.04, 0.16, a)); ctx.fill()
    ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    if wedge:
        poly(ctx, wedge); setc(ctx, (1, 0.9, 0.55, 0.16)); ctx.fill()


def wedge_pts(door):
    x, y, w, h = DOOR
    if door <= 0.01:
        return None
    ox = x + w * 0.18 * 0 + w * door * 0.82  # opening width
    left = x; right = x + w * door * 0.82
    spread = door
    return [(left, y), (right, y), (right, STAND), (right - 150 * spread, STAND + 600), (left - 1300 * spread, STAND + 600), (left, STAND)]


def sweat(ctx, x, y, t, s=1.0):
    for i in range(2):
        tt = (t * 0.05 + i * 0.5) % 1
        ctx.save(); ctx.translate(x + i * 40 * s, y + tt * 80 * s); ctx.scale(s, s)
        ctx.new_path(); ctx.move_to(0, -26); ctx.curve_to(16, 0, 16, 18, 0, 18); ctx.curve_to(-16, 18, -16, 0, 0, -26); ctx.close_path()
        fl(ctx, hx('8fe9ff'), 4); ctx.restore()


def room_shot(ctx, f, boy_p, door=0.0, mom=None, z=1.0, cx=540, cy=1150, shake=0, cover_b=0.0, phone_at=None, phone_glow=0.0,
              dark=0.55, after=None, theme=0, sleeper=BOY, extra=None, under=None):
    """mom: (x, facing, pose) standing in doorway / room."""
    ctx.save(); cam(ctx, cx, cy, z, 0, shake, f)
    kid_room(ctx, f, door, theme)
    if mom:
        mx, mf, mp, mch, mk = mom
        hs_m = draw(ctx, mx, STAND - 186 * mk, mk, mf, mch, mp)
    else:
        hs_m = None
    bed_back(ctx, theme)
    if under:
        under(ctx)
    pillow(ctx)
    h = draw_hip(ctx, HIP[0], HIP[1], KB, 1, sleeper, boy_p)
    blanket(ctx, b=cover_b, col=hx('ff3b8a') if theme == 0 else hx('ffcf3d'))
    if extra:
        extra(ctx, h, hs_m)
    if phone_at:
        phone(ctx, *phone_at)
    dark_with_wedge(ctx, wedge_pts(door), dark)
    if phone_glow > 0 and phone_at:
        glow(ctx, phone_at[0], phone_at[1], 300, a=0.3 * phone_glow)
        glow(ctx, h['head'][0], h['head'][1], 200, a=0.18 * phone_glow)
    if after:
        after(ctx, h, hs_m)
    ctx.restore()
    return h, hs_m


GAME_P = dict(lsh=-150, lel=-60, rsh=-150, rel=-50)   # arms up holding phone above face
ANGEL_P = dict(lsh=-30, lel=-150, rsh=-30, rel=-150)   # hands folded on chest


def phone_pos(h):
    hx_, hy = h['front']
    return (hx_ + 10, hy - 40, 1.0, -0.3)


# ------------------------------------------------------------------ shots
def s1(ctx, f):
    steps = f >= 56
    p = lying(eye='shock' if f >= 74 else 'normal', mouth='grin' if f < 56 else ('flat' if f < 74 else 'scream'), head=-20, **GAME_P)
    z = kf(f, [(0, 0.95), (56, 1.25), (74, 1.25), (80, 1.5)], eout)
    tap = (f // 3) % 2

    def extra(c, h, hm):
        pass

    def after(c, h, hm):
        # glowing strip under the door = someone in the hallway
        if steps:
            x, y, w, hh = DOOR
            a = pop(f, 56, 66)
            c.rectangle(x - 200, STAND - 4, w + 400, 26); setc(c, (1, 0.9, 0.5, 0.55 * a)); c.fill()
    h0 = draw_hip(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)), HIP[0], HIP[1], KB, 1, BOY, p)
    px, py, ps, pa = phone_pos(h0)
    room_shot(ctx, f, p, z=z, cx=lerp(620, 420, pop(f, 0, 80)), cy=1120, phone_at=(px, py + (4 if tap else 0), ps, pa), phone_glow=1.0,
              after=after, shake=shake_at(f, [74], 8, 14))
    if f < 56:
        label(ctx, "*TAP TAP TAP*", 540, 1430, 76, hx('8fe9ff'), 0.03, pop(f, 8, 12))
    elif f < 74:
        label(ctx, "*FOOTSTEPS*", 540, 1430, 80, (1, 1, 1), -0.03, pop(f, 56, 60))
    else:
        label(ctx, "MOM!", 540, 1430, 130, hx('ff3b5c'), -0.05, pop(f, 74, 78))
    card(ctx, 'p1', f, 2, 98)


def s2(ctx, f):
    lf = f - 100
    # 0.5-second transformation: phone hidden, blanket up, eyes shut, angel hands
    throw = pop(lf, 4, 18)
    cover = eout(pop(lf, 24, 34))
    angel = lf >= 44
    if lf < 20:
        arms = GAME_P
    elif not angel:
        arms = dict(lsh=-60, lel=-80, rsh=-100, rel=-40)
    else:
        arms = ANGEL_P
    p = lying(eye='shock' if lf < 44 else 'closed', mouth='scream' if lf < 44 else 'smile', head=-6, **arms)
    rot = -6 * math.sin(lf * 0.9) if lf < 44 else 0
    ctx.save(); ctx.translate(540, 960); ctx.rotate(math.radians(rot)); ctx.translate(-540, -960)
    h0 = draw_hip(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)), HIP[0], HIP[1], KB, 1, BOY, P(**{**lying(), **GAME_P}))
    sx, sy, _, _ = phone_pos(h0)
    if lf < 4:
        ph = (sx, sy, 1.0, -0.3)
    elif lf < 18:
        ph = (lerp(sx, 250, eout(throw)), lerp(sy, 1215, eout(throw)) - math.sin(throw * math.pi) * 200, 1.0, throw * 9)
    else:
        ph = None

    def after(c, h, hm):
        if angel:
            # tiny halo
            hx_, hy = h['head']
            a = max(0.05, pop(lf, 44, 52))
            ellipse(c, hx_ - 150, hy - 10, 30 * a, 80 * a); setc(c, hx('ffe14d')); c.set_line_width(9); c.stroke()
            for i in range(3):
                sparkle(c, hx_ + math.cos(lf * 0.2 + i * 2) * 170, hy - 120 + math.sin(lf * 0.2 + i * 2) * 60, 26 * a, hx('fff27a'))
    room_shot(ctx, f, p, z=kf(lf, [(0, 1.35), (44, 1.2), (60, 1.1)], eout), cx=480, cy=1140, cover_b=lerp(-30, 60, cover),
              phone_at=ph, phone_glow=1.0 if ph else 0, after=after, shake=shake_at(lf, [18, 34], 8, 14))
    ctx.restore()
    if lf < 44:
        hlines(ctx, lf, 0.25, col=(1, 1, 1), y0=700, y1=1450)
    # checklist pops
    for i, (t_, s_) in enumerate(((18, "PHONE: HIDDEN"), (34, "BLANKET: UP"), (44, "EYES: SHUT"))):
        if lf >= t_:
            label(ctx, s_ + "  ✓", 540, 1260 + i * 85, 64, hx('5fd07a'), 0.0, pop(lf, t_, t_ + 4))
    card(ctx, 'p2', f, 102, 236)


def s3(ctx, f):
    lf = f - 240
    door = eout(pop(lf, 6, 40))
    mx = 1185
    mp = P(eye='normal', mouth='flat', rsh=-20, rel=-60, lsh=10, lel=-20, head=8)
    snore = lf >= 54
    p = lying(eye='closed', mouth='open' if snore and (lf // 10) % 2 == 0 else 'flat', **ANGEL_P)
    z = kf(lf, [(0, 0.85), (60, 0.85), (160, 0.95)], ein)
    room_shot(ctx, f, p, door=door, mom=(mx, -1, mp, MOM, KM) if lf > 20 else None, z=z, cx=kf(lf, [(0, 700), (160, 740)]), cy=1100)
    if lf < 50:
        label(ctx, "CREEEAK...", 540, 1430, 100, hx('ffe14d'), -0.04, pop(lf, 8, 12))
    if snore:
        for i in range(3):
            t = ((lf - 54 + i * 10) % 30) / 30
            label(ctx, "Z", 330 + i * 60 + t * 60, 900 - t * 160 - i * 30, 60 + 50 * i + 30 * (lf > 110), hx('8fe9ff'), 0.15, 1 - t * 0.6)
        label(ctx, "*SUPER LOUD SNORING*", 540, 1430, 66, (1, 1, 1), 0.03, pop(lf, 60, 64))
    card(ctx, 'p3', f, 296, 398)


def s4(ctx, f):
    lf = f - 400
    peek = 30 <= lf < 40 or 66 <= lf < 70
    caught = lf >= 40

    def top(c):
        # mom in the doorway, low-ish angle, squinting
        c.rectangle(-900, -900, 3000, 4000); setc(c, hx('2a2f6a')); c.fill()
        c.rectangle(300, 300, 480, 1300); setc(c, hx('ffe9a8')); c.fill()
        c.rectangle(280, 280, 520, 20); fl(c, hx('f2e6d0'), 6)
        lean = math.sin(min(lf, 60) * 0.05) * 6
        mp = P(eye='glare', mouth='flat' if lf < 70 or lf >= 100 else ('open' if (lf // 5) % 2 == 0 else 'flat'), torso=lean, head=6, lsh=-30, lel=-120, rsh=60, rel=-90)
        draw(c, 540, 1500 - 186 * 1.75, 1.75, -1, MOM, mp)

    def bot(c):
        c.rectangle(-900, -900, 3000, 4000); setc(c, hx('1d1640')); c.fill()
        ellipse(c, 380, 1200, 500, 200); fl(c, hx('fff6e0'), 9)
        bp = lying(eye='normal' if peek else 'closed', mouth='smile' if lf < 100 or lf >= 132 else ('open' if (lf // 5) % 2 == 0 else 'flat'), head=-8)
        h = draw_hip(c, 980, 1080, 1.9, 1, BOY, bp)
        if lf >= 40:
            sweat(c, h['head'][0] + 40, h['head'][1] - 230, lf, 1.3)
    zt = kf(lf, [(0, 1.0), (40, 1.0), (46, 1.25), (160, 1.35)], eout)
    zb = kf(lf, [(0, 1.0), (160, 1.15)], eout)
    sh = shake_at(lf, [40], 8, 10)
    ctx.save(); ctx.translate(random.Random(f).uniform(-sh, sh), 0)
    half(ctx, True, 540, 760, zt, top)
    half(ctx, False, 540, 1130, zb, bot)
    ctx.restore()
    ctx.rectangle(0, H / 2 - 10, W, 20); fl(ctx, hx('ffd23f'), 5)
    if lf < 70:
        if lf >= 30 and lf < 40:
            label(ctx, "*PEEK*", 540, 1240, 80, hx('ffe14d'), 0.05, 1)
        if lf >= 40:
            label(ctx, "HMMM...", 540, 860, 110, hx('ffe14d'), -0.04, pop(lf, 40, 44))
    elif lf < 100:
        label(ctx, "ARE YOU ASLEEP?", 540, 860, 92, hx('ffe14d'), -0.03, pop(lf, 70, 74))
    else:
        label(ctx, "...YES.", 540, 1070, 120, hx('8fe9ff'), 0.04, pop(lf, 104, 108))
    card(ctx, 'p4', f, 404, 470)


def s5(ctx, f):
    lf = f - 560
    walk_in = eout(pop(lf, 0, 34))
    lean = eout(pop(lf, 34, 50))
    buzz = 64 <= lf < 110
    kiss = lf >= 122
    mx = lerp(1210, 800, walk_in)
    if lf < 34:
        mp = walk(lf * 0.5, eye='normal', mouth='flat')
    else:
        hide = pop(lf, 100, 112)
        mp = P(torso=lerp(0, 22, lean), head=lerp(0, 14, lean), eye='happy' if kiss else ('glare' if buzz else 'normal'),
               mouth='smile' if not kiss else 'open', rsh=lerp(10, 80, lean), rel=-30,
               lsh=lerp(-10, -50, hide), lel=lerp(-20, -60, hide))
    bp = lying(eye='closed', mouth='wavy' if buzz else 'smile', **ANGEL_P)

    def under(c):
        # phone hidden under the pillow; mom's hand quietly slides it out after the buzz
        if lf < 104:
            phone(c, 130 + (math.sin(lf * 2.6) * 8 if buzz else 0), 1225, 0.8, 1.57, buzz, lf if buzz else 0)

    def extra(c, h, hm):
        if lf >= 106 and hm:
            fx, fy = hm['back']
            glow(c, fx, fy - 10, 120, a=0.5)
            phone(c, fx, fy - 10, 0.75, 0.3, True)

    def after(c, h, hm):
        if buzz:
            glow(c, 160, 1225, 240, a=0.5 * (0.6 + 0.4 * abs(math.sin(lf * 1.3))))
            for a0 in (math.pi - 0.4, -0.4):
                c.new_path(); c.arc(160, 1225, 110 + 15 * math.sin(lf), a0, a0 + 0.8)
                setc(c, (1, 1, 1, 0.8)); c.set_line_width(8); c.stroke()
            sweat(c, h['head'][0] + 20, h['head'][1] - 200, lf, 1.0)
        if kiss:
            hx_, hy = h['head']
            a = max(0.05, pop(lf, 122, 130))
            for i in range(3):
                t = ((lf - 122 + i * 7) % 24) / 24
                ellipse(c, hx_ + 40 + i * 40, hy - 160 - t * 140, 22 * a, 20 * a); setc(c, hx('ff3b8a', ) + (1 - t,)); c.fill()
    room_shot(ctx, f, bp, door=1.0, mom=(mx, -1, mp, MOM, 1.75), z=kf(lf, [(0, 0.85), (40, 1.05), (64, 1.12)], eout),
              cx=kf(lf, [(0, 640), (40, 540)], eout), cy=1080, dark=0.45, extra=extra, under=under, after=after, shake=4 if buzz else 0)
    if buzz:
        label(ctx, "BZZZT! BZZZT!", 540, 1430, 100, hx('ff3b5c'), -0.04, 1)
    elif kiss:
        label(ctx, "GOODNIGHT, SWEETIE.", 540, 1430, 80, hx('ffb3d0'), 0.02, pop(lf, 124, 128))
    card(ctx, 'p5', f, 600, 716)


def s6(ctx, f):
    lf = f - 720
    door = 1 - eout(pop(lf, 0, 26))
    smug = 30 <= lf < 82
    reach = pop(lf, 82, 98)
    shock = lf >= 104
    if lf < 30:
        bp = lying(eye='closed', mouth='smile', **ANGEL_P)
    elif smug:
        bp = lying(eye='smug', mouth='grin', head=-14, lsh=-160, lel=-40, rsh=-30, rel=-150)
    else:
        bp = lying(eye='shock' if shock else 'normal', mouth='scream' if shock else 'flat', head=-20 if shock else -12,
                   lsh=-120, lel=-20, rsh=lerp(-30, -175, reach), rel=lerp(-150, -10, reach))
    z = kf(lf, [(0, 0.9), (30, 1.15), (100, 1.15), (106, 1.7), (160, 1.8)], eout)

    room_shot(ctx, f, bp, door=door, z=z, cx=kf(lf, [(0, 620), (30, 470), (100, 470), (106, 330)], eout), cy=1120, dark=0.5,
              shake=shake_at(lf, [104], 10, 20))
    if lf < 30:
        label(ctx, "*CLICK*", 540, 1430, 76, (1, 1, 1), 0.03, pop(lf, 22, 26))
    elif smug:
        label(ctx, "TOO EASY.", 540, 1430, 100, hx('8fe9ff'), -0.03, pop(lf, 34, 38))
    elif not shock:
        label(ctx, "*RUMMAGE*", 540, 1430, 76, (1, 1, 1), 0.03, pop(lf, 84, 88))
    else:
        label(ctx, "MY PHONE?!", 540, 1430, 130, hx('ff3b5c'), -0.05, pop(lf, 104, 108))
    card(ctx, 'p6', f, 744, 818)


def s7(ctx, f):
    lf = f - 880
    door = eout(pop(lf, 58, 80))
    fake = lf >= 66
    if not fake:
        mp = lying(eye='happy', mouth='grin', head=-20, **GAME_P)
    else:
        mp = lying(eye='closed', mouth='open' if (lf // 10) % 2 == 0 else 'flat', **ANGEL_P)
    dp = P(eye='glare', mouth='flat', head=10, torso=6, lsh=-20, lel=-80, rsh=10, rel=-20)
    h0 = draw_hip(cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 4, 4)), HIP[0], HIP[1], KB, 1, MOM, P(**{**lying(), **GAME_P}))
    px, py, ps, pa = phone_pos(h0)
    ph = (px, py, ps, pa) if not fake else None
    z = kf(lf, [(0, 1.3), (58, 1.15), (70, 0.82)], eout)

    def after(c, h, hm):
        if not fake:
            for i in range(3):
                t = ((lf + i * 9) % 27) / 27
                label(c, "HA", h['head'][0] + 120 + i * 50, h['head'][1] - 150 - t * 100, 56, hx('ffe14d'), 0.1, 1 - t)
    room_shot(ctx, f, mp, door=door, mom=(1170, -1, dp, DAD, KM) if lf >= 64 else None, z=z, cx=kf(lf, [(0, 420), (58, 520), (70, 700)], eout),
              cy=1100, phone_at=ph, phone_glow=1.0 if ph else 0, theme=1, sleeper=MOM, after=after, dark=0.55, shake=shake_at(lf, [66], 8, 14))
    if fake:
        for i in range(3):
            t = ((lf - 66 + i * 10) % 30) / 30
            label(ctx, "Z", 300 + i * 60 + t * 40, 860 - t * 120 - i * 30, 60 + 40 * i, hx('8fe9ff'), 0.15, 1 - t * 0.6)
    if lf < 58:
        label(ctx, "MEANWHILE...", 540, 1430, 90, (1, 1, 1), 0.03, pop(lf, 2, 6))
    elif lf < 100:
        label(ctx, "CREEEAK...", 540, 1430, 96, hx('ffe14d'), -0.04, pop(lf, 60, 64))
    else:
        label(ctx, "LIKE MOTHER, LIKE SON.", 540, 1430, 76, hx('ffe14d'), -0.02, pop(lf, 100, 106))
    card(ctx, 'p7', f, 960)


SHOTS = [(0, s1), (100, s2), (240, s3), (400, s4), (560, s5), (720, s6), (880, s7)]


def render(f):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(s)
    fn = [fn for st, fn in SHOTS if st <= f][-1]
    fn(ctx, f)
    g = cairo.RadialGradient(W / 2, H / 2, 600, W / 2, H / 2, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.05, 0, 0.1, 0.28)
    ctx.set_source(g); ctx.paint()
    for c in (100, 240, 400, 440, 560, 624, 720, 824, 880, 946):
        if c <= f < c + 3:
            ctx.rectangle(0, 0, W, H); setc(ctx, (1, 1, 1, 0.5 * (1 - (f - c) / 3))); ctx.fill()
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        for f in map(int, sys.argv[2:]):
            render(f).write_to_png(f'out/c{f:04d}.png')
    else:
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-i", "out/asleep_audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
                              "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                              "-shortest", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
        for f in range(N):
            p.stdin.write(bytes(render(f).get_data()))
        p.stdin.close(); p.wait()
