"""Clean flat doodle-style characters: bold outline, flat colour, round chubby shapes (original designs)."""
import cairo, math
from eng import hx, dark, light, lerp, clamp, ellipse, poly, setc, vgrad, P

INK = (0.07, 0.06, 0.08)
_SWAY = [0.0]
_SIND = [True]


def ink(ctx, w):
    setc(ctx, INK); ctx.set_line_width(w); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.set_line_cap(cairo.LINE_CAP_ROUND)


def fl(ctx, col, w):
    ctx.save(); setc(ctx, col); ctx.fill_preserve(); ink(ctx, w); ctx.stroke(); ctx.restore()


# ------------------------------------------------------------------ face parts
def eyes(ctx, R, kind, turn, lw):
    pos = ((-R * 0.3 + turn, R * 0.06, 0.88), (R * 0.32 + turn, R * 0.06, 1.0))
    if kind == 'glare':
        for x, y, s in pos:
            r = R * 0.3 * s
            ellipse(ctx, x, y + R * 0.06, r * 0.95, r); fl(ctx, (1, 1, 1), lw)
            setc(ctx, hx('e0263a')); ctx.set_line_width(lw * 0.35)
            for i in range(6):
                a = i * math.pi / 3 + 0.3
                ctx.move_to(x + math.cos(a) * r * 0.92, y + R * 0.06 + math.sin(a) * r * 0.92)
                ctx.line_to(x + math.cos(a + 0.2) * r * 0.6, y + R * 0.06 + math.sin(a + 0.2) * r * 0.6)
                ctx.line_to(x + math.cos(a - 0.1) * r * 0.45, y + R * 0.06 + math.sin(a - 0.1) * r * 0.45)
                ctx.stroke()
            px = x + (R * 0.08 if x < turn else -R * 0.08)
            ellipse(ctx, px, y + R * 0.12, R * 0.045, R * 0.05); setc(ctx, INK); ctx.fill()
        # angry V brows
        ink(ctx, lw * 1.7)
        ctx.new_path(); ctx.move_to(-R * 0.62 + turn, -R * 0.38); ctx.curve_to(-R * 0.4 + turn, -R * 0.36, -R * 0.15 + turn, -R * 0.22, -R * 0.02 + turn, -R * 0.1); ctx.stroke()
        ctx.new_path(); ctx.move_to(R * 0.66 + turn, -R * 0.4); ctx.curve_to(R * 0.45 + turn, -R * 0.36, R * 0.2 + turn, -R * 0.22, R * 0.06 + turn, -R * 0.1); ctx.stroke()
        return
    for x, y, s in pos:
        if kind == 'normal' or kind == 'smug':
            ellipse(ctx, x, y, R * 0.085 * s, R * 0.125); setc(ctx, INK); ctx.fill()
            ellipse(ctx, x - R * 0.025, y - R * 0.05, R * 0.03, R * 0.035); setc(ctx, (1, 1, 1)); ctx.fill()
            if kind == 'smug':
                ink(ctx, lw); ctx.new_path(); ctx.move_to(x - R * 0.12, y - R * 0.04); ctx.line_to(x + R * 0.12, y - R * 0.06); ctx.stroke()
        elif kind == 'shock':
            ellipse(ctx, x, y, R * 0.17 * s, R * 0.19); fl(ctx, (1, 1, 1), lw)
            ellipse(ctx, x, y + R * 0.02, R * 0.04, R * 0.045); setc(ctx, INK); ctx.fill()
        elif kind == 'happy':
            ink(ctx, lw * 1.2); ctx.new_path(); ctx.arc(x, y + R * 0.06, R * 0.11, math.pi * 1.1, math.pi * 1.9); ctx.stroke()
        elif kind == 'closed':
            ink(ctx, lw * 1.2); ctx.new_path(); ctx.arc(x, y - R * 0.04, R * 0.11, math.pi * 0.1, math.pi * 0.9); ctx.stroke()
    if kind in ('normal', 'smug', 'happy', 'shock'):
        ink(ctx, lw * 1.1)
        by = -R * 0.2 if kind != 'shock' else -R * 0.32
        for x, y, s in pos:
            ctx.new_path(); ctx.move_to(x - R * 0.09, by + R * 0.01); ctx.curve_to(x - R * 0.03, by - R * 0.04, x + R * 0.04, by - R * 0.04, x + R * 0.1, by); ctx.stroke()


def mouth(ctx, kind, R, turn, lw):
    mx, my = R * 0.04 + turn, R * 0.5
    ink(ctx, lw)
    if kind == 'smile':
        ctx.new_path(); ctx.arc(mx, my - R * 0.08, R * 0.1, 0.4, math.pi - 0.4); ctx.stroke()
    elif kind == 'frown':
        ctx.new_path(); ctx.arc(mx, my + R * 0.1, R * 0.1, math.pi + 0.5, 2 * math.pi - 0.5); ctx.stroke()
    elif kind == 'grin':
        ctx.new_path(); ctx.move_to(mx - R * 0.2, my - R * 0.08); ctx.curve_to(mx - R * 0.05, my - R * 0.02, mx + R * 0.1, my - R * 0.04, mx + R * 0.22, my - R * 0.12)
        ctx.curve_to(mx + R * 0.18, my + R * 0.14, mx - R * 0.16, my + R * 0.14, mx - R * 0.2, my - R * 0.08); ctx.close_path()
        fl(ctx, (1, 1, 1), lw)
        ctx.new_path(); ctx.move_to(mx - R * 0.17, my - R * 0.01); ctx.curve_to(mx, my + R * 0.03, mx + R * 0.1, my + R * 0.01, mx + R * 0.19, my - R * 0.05); ink(ctx, lw * 0.6); ctx.stroke()
    elif kind in ('open', 'scream'):
        s = 1 if kind == 'open' else 1.8
        ellipse(ctx, mx, my, R * 0.07 * s, R * 0.09 * s); fl(ctx, hx('8a1c2c'), lw)
        ellipse(ctx, mx, my + R * 0.05 * s, R * 0.045 * s, R * 0.03 * s); setc(ctx, hx('ff6f86')); ctx.fill()
    elif kind == 'flat':
        ctx.new_path(); ctx.move_to(mx - R * 0.08, my); ctx.line_to(mx + R * 0.08, my); ctx.stroke()
    elif kind == 'wavy':
        ctx.new_path(); ctx.move_to(mx - R * 0.14, my)
        for i in range(4):
            d = -1 if i % 2 == 0 else 1
            ctx.rel_curve_to(R * 0.025, R * 0.05 * d, R * 0.045, R * 0.05 * d, R * 0.07, 0)
        ctx.stroke()


# ------------------------------------------------------------------ hair
def hair_boy(ctx, R, col, front, lw):
    if not front:
        ctx.new_path(); ctx.arc(0, -R * 0.08, R * 1.06, math.pi * 0.9, math.pi * 2.1); ctx.close_path(); fl(ctx, col, lw)
        return
    ctx.new_path()
    ctx.move_to(-R * 1.02, R * 0.05)
    ctx.curve_to(-R * 1.1, -R * 0.75, -R * 0.55, -R * 1.18, R * 0.05, -R * 1.15)
    ctx.curve_to(R * 0.7, -R * 1.12, R * 1.12, -R * 0.75, R * 1.02, R * 0.05)
    # fringe with soft points
    ctx.curve_to(R * 0.95, -R * 0.2, R * 0.85, -R * 0.3, R * 0.72, -R * 0.38)
    ctx.curve_to(R * 0.62, -R * 0.2, R * 0.5, -R * 0.15, R * 0.42, -R * 0.12)
    ctx.curve_to(R * 0.38, -R * 0.28, R * 0.25, -R * 0.4, R * 0.12, -R * 0.42)
    ctx.curve_to(R * 0.05, -R * 0.25, -R * 0.08, -R * 0.15, -R * 0.2, -R * 0.12)
    ctx.curve_to(-R * 0.25, -R * 0.28, -R * 0.4, -R * 0.38, -R * 0.55, -R * 0.4)
    ctx.curve_to(-R * 0.65, -R * 0.2, -R * 0.78, -R * 0.12, -R * 0.88, -R * 0.1)
    ctx.curve_to(-R * 0.95, -R * 0.05, -R * 1.0, 0, -R * 1.02, R * 0.05)
    ctx.close_path(); fl(ctx, col, lw)
    # one clean highlight
    ctx.new_path(); ctx.move_to(-R * 0.55, -R * 0.82); ctx.curve_to(-R * 0.3, -R * 0.95, R * 0.0, -R * 0.98, R * 0.25, -R * 0.94)
    setc(ctx, light(col, 0.35)); ctx.set_line_width(R * 0.07); ctx.stroke()
    # ahoge
    sw_ = _SWAY[0] * R
    ctx.new_path(); ctx.move_to(-R * 0.05, -R * 1.12); ctx.curve_to(-R * 0.05 + sw_ * 0.5, -R * 1.45, R * 0.35 + sw_, -R * 1.45, R * 0.3 + sw_, -R * 1.25); ink(ctx, lw); ctx.stroke()


def hair_mom(ctx, R, col, front, lw):
    if not front:
        ellipse(ctx, -R * 0.62, -R * 0.62, R * 0.42, R * 0.4); fl(ctx, col, lw)   # side bun
        ctx.new_path(); ctx.arc(0, -R * 0.05, R * 1.06, math.pi * 0.85, math.pi * 2.15); ctx.close_path(); fl(ctx, col, lw)
        for i in range(3):
            ellipse(ctx, -R * 0.85 + i * R * 0.2, -R * 0.95 + i * R * 0.04, R * 0.05, R * 0.05); fl(ctx, hx('ffd23f'), lw * 0.4)
        return
    ctx.new_path()
    ctx.move_to(-R * 1.03, R * 0.25)
    ctx.curve_to(-R * 1.12, -R * 0.65, -R * 0.6, -R * 1.12, R * 0.02, -R * 1.12)
    ctx.curve_to(R * 0.65, -R * 1.12, R * 1.12, -R * 0.65, R * 1.03, R * 0.25)
    ctx.curve_to(R * 0.92, -R * 0.15, R * 0.6, -R * 0.62, R * 0.05, -R * 0.66)
    ctx.curve_to(-R * 0.55, -R * 0.62, -R * 0.92, -R * 0.15, -R * 1.03, R * 0.25)
    ctx.close_path(); fl(ctx, col, lw)
    if _SIND[0]:
        ctx.new_path(); ctx.move_to(R * 0.04, -R * 0.68); ctx.line_to(R * 0.03, -R * 1.08); setc(ctx, hx('e0123a')); ctx.set_line_width(lw * 1.2); ctx.stroke()
    ctx.new_path(); ctx.move_to(-R * 0.6, -R * 0.88); ctx.curve_to(-R * 0.4, -R * 0.98, -R * 0.2, -R * 1.0, -R * 0.08, -R * 1.0)
    setc(ctx, light(col, 0.3)); ctx.set_line_width(R * 0.06); ctx.stroke()


def hair_aunty(ctx, R, col, front, lw):
    if not front:
        for dx, dy, r in ((-0.85, -0.2, 0.42), (0.85, -0.2, 0.42), (-0.6, -0.75, 0.45), (0.6, -0.75, 0.45), (0, -1.0, 0.5), (-0.95, 0.25, 0.32), (0.95, 0.25, 0.32)):
            ellipse(ctx, dx * R, dy * R, r * R, r * R); fl(ctx, col, lw)
        return
    for dx, dy, r in ((-0.55, -0.62, 0.3), (-0.15, -0.78, 0.32), (0.3, -0.75, 0.3), (0.68, -0.55, 0.28)):
        ellipse(ctx, dx * R, dy * R, r * R, r * R); fl(ctx, col, lw)
    for dx, dy in ((-0.5, -0.7), (0.0, -0.85), (0.4, -0.82)):
        ctx.new_path(); ctx.arc(dx * R, dy * R, R * 0.1, math.pi, math.pi * 1.7); setc(ctx, light(col, 0.4)); ctx.set_line_width(lw); ctx.stroke()


def hair_uncle(ctx, R, col, front, lw):
    if not front:
        for sx in (-1, 1):
            ellipse(ctx, sx * R * 0.92, -R * 0.15, R * 0.22, R * 0.38); fl(ctx, col, lw)
        return
    ink(ctx, lw * 0.8)
    for i in range(3):
        ctx.new_path(); ctx.arc(-R * 0.1 + i * R * 0.12, -R * 0.95, R * 0.12, math.pi * 1.1, math.pi * 1.6); ctx.stroke()
    ellipse(ctx, -R * 0.35, -R * 0.65, R * 0.18, R * 0.08, -0.4); setc(ctx, (1, 1, 1, 0.5)); ctx.fill()


def hair_dad(ctx, R, col, front, lw):
    if not front:
        ctx.new_path(); ctx.arc(0, -R * 0.1, R * 1.04, math.pi * 0.95, math.pi * 2.05); ctx.close_path(); fl(ctx, col, lw)
        for sx in (-1, 1):
            ellipse(ctx, sx * R * 0.93, -R * 0.12, R * 0.12, R * 0.22); fl(ctx, hx('a8a8b4'), lw * 0.7)
        return
    ctx.new_path()
    ctx.move_to(-R * 1.0, -R * 0.05)
    ctx.curve_to(-R * 1.05, -R * 0.8, -R * 0.4, -R * 1.15, R * 0.15, -R * 1.12)
    ctx.curve_to(R * 0.75, -R * 1.08, R * 1.08, -R * 0.7, R * 1.0, -R * 0.1)
    ctx.curve_to(R * 0.8, -R * 0.45, R * 0.3, -R * 0.62, -R * 0.25, -R * 0.55)   # swoop to the side part
    ctx.curve_to(-R * 0.6, -R * 0.5, -R * 0.85, -R * 0.35, -R * 1.0, -R * 0.05)
    ctx.close_path(); fl(ctx, col, lw)
    ink(ctx, lw * 0.8); ctx.new_path(); ctx.move_to(-R * 0.35, -R * 1.05); ctx.curve_to(-R * 0.3, -R * 0.85, -R * 0.28, -R * 0.7, -R * 0.25, -R * 0.56); ctx.stroke()
    ctx.new_path(); ctx.move_to(R * 0.0, -R * 0.98); ctx.curve_to(R * 0.4, -R * 0.95, R * 0.7, -R * 0.8, R * 0.8, -R * 0.55); setc(ctx, light(col, 0.35)); ctx.set_line_width(R * 0.06); ctx.stroke()


def head(ctx, R, ch, p, f, lw):
    ctx.scale(f, 1)
    hp_ = p.get('headphones', 0)
    turn = R * 0.1
    hf = {'boy': hair_boy, 'mom': hair_mom, 'aunty': hair_aunty, 'uncle': hair_uncle, 'dad': hair_dad}[ch['hairstyle']]
    hf(ctx, R, ch['hair'], False, lw)
    skin = ch['skin']
    for ex in (-R * 0.97, R * 0.97):
        ellipse(ctx, ex, R * 0.1, R * 0.13, R * 0.16); fl(ctx, skin, lw)
        if ch.get('earring'):
            ellipse(ctx, ex, R * 0.34, R * 0.07, R * 0.07); fl(ctx, hx('ffd23f'), lw * 0.6)
    # chubby face
    ctx.new_path()
    ctx.move_to(-R, -R * 0.1)
    ctx.curve_to(-R, -R * 1.05, R, -R * 1.05, R, -R * 0.1)
    ctx.curve_to(R * 1.04, R * 0.5, R * 0.62, R * 0.86, 0, R * 0.86)
    ctx.curve_to(-R * 0.62, R * 0.86, -R * 1.04, R * 0.5, -R, -R * 0.1)
    ctx.close_path(); fl(ctx, skin, lw)
    # soft flat blush
    if p.get('eye') != 'glare':
        for bx in (-R * 0.5 + turn, R * 0.58 + turn):
            ellipse(ctx, bx, R * 0.36, R * 0.15, R * 0.08); setc(ctx, (1, 0.55, 0.6, 0.55)); ctx.fill()
    ek = p.get('eye', 'normal')
    if p.get('blink', 0) > 0.5 and ek in ('normal', 'smug', 'shock'):
        ek = 'closed'
    eyes(ctx, R, ek, turn, lw)
    # nose
    ink(ctx, lw * 0.8); ctx.new_path(); ctx.arc(R * 0.05 + turn, R * 0.3, R * 0.04, -0.3, 1.6); ctx.stroke()
    mouth(ctx, p.get('mouth', 'smile'), R, turn, lw)
    if ch.get('bindi'):
        ellipse(ctx, R * 0.04 + turn * 0.5, -R * 0.42 if ek != 'glare' else -R * 0.5, R * 0.05, R * 0.055); fl(ctx, hx('e0123a'), lw * 0.4)
    if ch.get('moustache'):
        mx = R * 0.05 + turn
        ctx.new_path(); ctx.move_to(mx, R * 0.36)
        ctx.curve_to(mx - R * 0.15, R * 0.3, mx - R * 0.3, R * 0.36, mx - R * 0.34, R * 0.5)
        ctx.curve_to(mx - R * 0.2, R * 0.44, mx - R * 0.08, R * 0.46, mx, R * 0.42)
        ctx.curve_to(mx + R * 0.08, R * 0.46, mx + R * 0.2, R * 0.44, mx + R * 0.34, R * 0.5)
        ctx.curve_to(mx + R * 0.3, R * 0.36, mx + R * 0.15, R * 0.3, mx, R * 0.36); ctx.close_path()
        fl(ctx, ch['moustache'], lw * 0.8)
    hf(ctx, R, ch['hair'], True, lw)
    if ch.get('glasses'):
        for x, y, s_ in ((-R * 0.3 + turn, R * 0.06, 0.88), (R * 0.32 + turn, R * 0.06, 1.0)):
            ellipse(ctx, x, y, R * 0.22 * s_, R * 0.2); setc(ctx, (0.8, 0.95, 1, 0.25)); ctx.fill_preserve()
            setc(ctx, ch['glasses']); ctx.set_line_width(lw * 1.4); ctx.stroke()
        ctx.new_path(); ctx.move_to(-R * 0.08 + turn, R * 0.04); ctx.line_to(R * 0.1 + turn, R * 0.04); setc(ctx, ch['glasses']); ctx.set_line_width(lw * 1.2); ctx.stroke()
    if hp_:
        ctx.new_path(); ctx.arc(0, -R * 0.05, R * 1.12, math.pi * 1.08, math.pi * 1.92); setc(ctx, INK); ctx.set_line_width(R * 0.16); ctx.stroke()
        ctx.new_path(); ctx.arc(0, -R * 0.05, R * 1.12, math.pi * 1.08, math.pi * 1.92); setc(ctx, hx('ff3b8a')); ctx.set_line_width(R * 0.1); ctx.stroke()
        for ex in (-R * 1.02, R * 1.02):
            ellipse(ctx, ex, R * 0.08, R * 0.2, R * 0.27); fl(ctx, hx('ff3b8a'), lw)
            ellipse(ctx, ex, R * 0.08, R * 0.1, R * 0.15); fl(ctx, hx('2a2a3a'), lw * 0.6)
    if ch.get('shades') and p.get('shades', 0) > 0:
        dy = p.get('shades_dy', 0) * R
        ctx.save(); ctx.translate(turn, R * 0.06 + dy)
        for ex, s in ((-R * 0.3, 0.9), (R * 0.32, 1.0)):
            ctx.new_path(); ctx.move_to(ex - R * 0.24 * s, -R * 0.12); ctx.line_to(ex + R * 0.24 * s, -R * 0.12)
            ctx.curve_to(ex + R * 0.24 * s, R * 0.12, ex + R * 0.08 * s, R * 0.17, ex, R * 0.17)
            ctx.curve_to(ex - R * 0.14 * s, R * 0.17, ex - R * 0.24 * s, R * 0.1, ex - R * 0.24 * s, -R * 0.12); ctx.close_path()
            fl(ctx, INK, lw)
            setc(ctx, (1, 1, 1)); ctx.set_line_width(lw * 0.9)
            ctx.new_path(); ctx.move_to(ex - R * 0.1 * s, -R * 0.06); ctx.line_to(ex - R * 0.17 * s, R * 0.08); ctx.stroke()
            ctx.new_path(); ctx.move_to(ex - R * 0.0, -R * 0.06); ctx.line_to(ex - R * 0.05, R * 0.04); ctx.stroke()
        ink(ctx, lw * 1.2); ctx.new_path(); ctx.move_to(-R * 0.08, -R * 0.08); ctx.line_to(R * 0.1, -R * 0.08); ctx.stroke()
        ctx.new_path(); ctx.move_to(-R * 0.54, -R * 0.1); ctx.line_to(-R * 0.95, -R * 0.12); ctx.stroke()
        if p.get('crack'):
            setc(ctx, (1, 1, 1)); ctx.set_line_width(lw * 0.7)
            ctx.new_path(); ctx.move_to(R * 0.2, -R * 0.1); ctx.line_to(R * 0.3, 0); ctx.line_to(R * 0.24, R * 0.06); ctx.line_to(R * 0.38, R * 0.14)
            ctx.move_to(R * 0.3, 0); ctx.line_to(R * 0.45, -R * 0.06); ctx.stroke()
        ctx.restore()


# ------------------------------------------------------------------ body
def draw(ctx, x, y, k, f, ch, p):
    ground = y + 186 * k
    S = k * 1.35
    lw = max(3.0, 3.7 * S)
    ctx.save()
    ctx.translate(x, ground - 68 * S)
    ctx.rotate(math.radians(p['rot']) * f)

    def dn(a):
        a = math.radians(a); return (f * math.sin(a), math.cos(a))

    def upv(a):
        a = math.radians(a); return (f * math.sin(a), -math.cos(a))

    tor = p['torso']
    u = upv(tor); pn = (-u[1], u[0])
    TL = 104 * S

    def tp(a, b):
        return (u[0] * a + pn[0] * b, u[1] * a + pn[1] * b)

    skin, shirt, pants, shoes = ch['skin'], ch['shirt'], ch['pants'], ch['shoes']
    hands = {}

    def limb(pts, w, col):
        ctx.new_path(); ctx.move_to(*pts[0])
        for q in pts[1:]:
            ctx.line_to(*q)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        setc(ctx, INK); ctx.set_line_width(w + lw * 2); ctx.stroke_preserve(); setc(ctx, col); ctx.set_line_width(w); ctx.stroke()

    def arm(side, a1, a2, back):
        sp = tp(TL - 20 * S, side * 44 * S)
        e = (sp[0] + dn(a1)[0] * 40 * S, sp[1] + dn(a1)[1] * 40 * S)
        h = (e[0] + dn(a1 + a2)[0] * 36 * S, e[1] + dn(a1 + a2)[1] * 36 * S)
        sl = ch.get('sleeve', 1.0)
        sc = dark(skin, 0.9) if back else skin
        limb([sp, e, h], 30 * S, sc)
        shc = dark(shirt, 0.88) if back else shirt
        if sl >= 1:
            limb([sp, e, (lerp(e[0], h[0], 0.6), lerp(e[1], h[1], 0.6))], 32 * S, shc)
        else:
            limb([sp, (lerp(sp[0], e[0], sl * 1.6), lerp(sp[1], e[1], sl * 1.6))], 34 * S, shc)
        if ch.get('bangles'):
            bx, by = lerp(e[0], h[0], 0.72), lerp(e[1], h[1], 0.72)
            for i, c in enumerate((hx('ffd23f'), hx('e0123a'))):
                ellipse(ctx, bx + i * 4 * S * f, by + i * 5 * S, 16 * S, 7 * S, math.atan2(h[1] - e[1], h[0] - e[0]) + math.pi / 2)
                fl(ctx, c, lw * 0.5)
        ellipse(ctx, h[0], h[1], 17 * S, 17 * S); fl(ctx, sc, lw)
        hands['back' if back else 'front'] = ctx.user_to_device(*h)

    def leg(side, a1, a2, back):
        hp = (side * 24 * S, -6 * S)
        kn = (hp[0] + dn(a1)[0] * 34 * S, hp[1] + dn(a1)[1] * 34 * S)
        ft = (kn[0] + dn(a1 + a2)[0] * 34 * S, kn[1] + dn(a1 + a2)[1] * 34 * S)
        limb([hp, kn, ft], 36 * S, dark(pants, 0.88) if back else pants)
        ellipse(ctx, ft[0] + f * 12 * S, ft[1] + 4 * S, 32 * S, 16 * S); fl(ctx, dark(shoes, 0.88) if back else shoes, lw)
        ellipse(ctx, ft[0] + f * 20 * S, ft[1] - 2 * S, 9 * S, 4 * S); setc(ctx, (1, 1, 1, 0.6)); ctx.fill()

    if ch.get('hood'):
        ellipse(ctx, *tp(TL + 4 * S, 0), 62 * S, 26 * S); fl(ctx, dark(shirt, 0.85), lw)
    arm(-1, p['lsh'], p['lel'], True)
    leg(-1, p['lhip'], p['lkn'], True)
    leg(1, p['rhip'], p['rkn'], False)
    robe = ch.get('robe')
    hw, sw = 58 * S, 46 * S
    ctx.new_path()
    if robe:
        bot = -40 * S
        ctx.move_to(*tp(TL - 6 * S, -sw)); ctx.curve_to(*tp(TL * 0.55, -hw * 1.12), *tp(TL * 0.15, -hw * 1.2), *tp(bot, -hw * 1.3))
        ctx.curve_to(*tp(bot - 6 * S, -hw * 0.4), *tp(bot - 6 * S, hw * 0.4), *tp(bot, hw * 1.3))
        ctx.curve_to(*tp(TL * 0.15, hw * 1.2), *tp(TL * 0.55, hw * 1.12), *tp(TL - 6 * S, sw))
    else:
        ctx.move_to(*tp(TL - 6 * S, -sw)); ctx.curve_to(*tp(TL * 0.6, -hw * 1.15), *tp(TL * 0.05, -hw * 1.12), *tp(-4 * S, -hw * 0.8))
        ctx.curve_to(*tp(-14 * S, -hw * 0.3), *tp(-14 * S, hw * 0.3), *tp(-4 * S, hw * 0.8))
        ctx.curve_to(*tp(TL * 0.05, hw * 1.12), *tp(TL * 0.6, hw * 1.15), *tp(TL - 6 * S, sw))
    ctx.curve_to(*tp(TL + 10 * S, sw * 0.5), *tp(TL + 10 * S, -sw * 0.5), *tp(TL - 6 * S, -sw))
    ctx.close_path()
    body = ctx.copy_path()
    fl(ctx, robe or shirt, lw)
    ctx.save(); ctx.new_path(); ctx.append_path(body); ctx.clip()
    ink(ctx, lw * 0.7)
    if ch.get('hood'):
        ctx.new_path(); ctx.move_to(*tp(TL * 0.4, -hw * 0.55)); ctx.line_to(*tp(TL * 0.4, hw * 0.55)); ctx.line_to(*tp(TL * 0.08, hw * 0.72))
        ctx.move_to(*tp(TL * 0.4, -hw * 0.55)); ctx.line_to(*tp(TL * 0.08, -hw * 0.72)); ctx.stroke()
        for b in (-11 * S, 11 * S):
            ctx.new_path(); ctx.move_to(*tp(TL - 6 * S, b)); ctx.line_to(*tp(TL * 0.6, b * 1.15)); ink(ctx, lw * 0.6); ctx.stroke()
    if robe:
        ctx.new_path(); ctx.move_to(*tp(TL, -16 * S)); ctx.line_to(*tp(TL - 30 * S, 0)); ctx.line_to(*tp(TL, 16 * S))
        setc(ctx, hx('ffd23f')); ctx.set_line_width(7 * S); ctx.stroke()
        ctx.new_path(); ctx.move_to(*tp(-30 * S, -hw * 1.5)); ctx.line_to(*tp(-30 * S, hw * 1.5)); setc(ctx, hx('ffd23f')); ctx.set_line_width(9 * S); ctx.stroke()
    ctx.restore()
    if ch.get('dupatta'):
        ctx.new_path(); ctx.move_to(*tp(TL - 4 * S, sw * 0.9)); ctx.curve_to(*tp(TL * 0.6, sw * 0.2), *tp(TL * 0.3, -hw * 0.6), *tp(TL * 0.05, -hw * 1.08))
        ctx.line_to(*tp(-20 * S, -hw * 1.15)); ctx.line_to(*tp(-20 * S, -hw * 0.55)); ctx.curve_to(*tp(TL * 0.3, -hw * 0.05), *tp(TL * 0.5, sw * 0.75), *tp(TL - 26 * S, sw * 1.25)); ctx.close_path()
        fl(ctx, ch['dupatta'], lw)
    arm(1, p['rsh'], p['rel'], False)
    R = 86 * S
    ht = tor + p.get('head', 0)
    nk = tp(TL, 0)
    hc = (nk[0] + upv(ht)[0] * R * 0.82, nk[1] + upv(ht)[1] * R * 0.82)
    ctx.save(); ctx.translate(*hc); ctx.rotate(math.radians(ht) * f)
    _SWAY[0] = p.get('sway', 0)
    _SIND[0] = ch.get('sindoor', True)
    hands['head'] = ctx.user_to_device(0, 0)
    hands['eyeL'] = ctx.user_to_device(f * (-R * 0.3 + R * 0.1), R * 0.12)
    hands['eyeR'] = ctx.user_to_device(f * (R * 0.32 + R * 0.1), R * 0.12)
    head(ctx, R, ch, p, f, lw)
    ctx.restore()
    ctx.restore()
    out = {k_: ctx.device_to_user(*v) for k_, v in hands.items()}
    out['R'] = R
    return out


def draw_hip(ctx, x, hipy, k, f, ch, p):
    return draw(ctx, x, hipy - (186 - 68 * 1.35) * k, k, f, ch, p)


BOY = dict(skin=hx('f3c29a'), hair=hx('1c1a2e'), hairstyle='boy', shirt=hx('ffc93c'), pants=hx('3d7bff'), shoes=hx('ff4d5e'), hood=True, shades=True)
MOM = dict(skin=hx('e9b08c'), hair=hx('1f1416'), hairstyle='mom', shirt=hx('9b4dff'), robe=hx('9b4dff'), pants=hx('ffa6d5'), shoes=hx('ffd23f'),
           earring=True, bindi=True, dupatta=hx('ffcf3d'), bangles=True, sleeve=0.45)


AUNTY = dict(skin=hx('f0c09c'), hair=hx('3a2420'), hairstyle='aunty', shirt=hx('19b5a5'), robe=hx('19b5a5'), pants=hx('ffffff'), shoes=hx('ff6b8a'),
             earring=True, dupatta=hx('ff8a3d'), bangles=True, sleeve=0.45, glasses=hx('d0263a'))
UNCLE = dict(skin=hx('d8a07a'), hair=hx('8a8a96'), hairstyle='uncle', shirt=hx('a8642e'), pants=hx('3a4258'), shoes=hx('3a2a20'),
             moustache=hx('2a2026'), sleeve=1.0, glasses=hx('2a2026'))

DAD = dict(skin=hx('d9a079'), hair=hx('1d1820'), hairstyle='dad', shirt=hx('fbfbf6'), pants=hx('4a74c9'), shoes=hx('7a4a2c'),
           moustache=hx('1d1820'), sleeve=0.0)

NEIGHBOR = dict(skin=hx('f6d2b0'), hair=hx('3a2a20'), hairstyle='dad', shirt=hx('ffffff'), pants=hx('2a3a6a'), shoes=hx('1d1820'),
                glasses=hx('1d1820'), tie=hx('e0263a'), sleeve=0.45)

MOM_G = dict(skin=hx('e9b08c'), hair=hx('3a2420'), hairstyle='mom', shirt=hx('9b4dff'), pants=hx('3d5a9e'), shoes=hx('ffffff'),
             earring=True, sindoor=False, sleeve=1.0)
NMOM = dict(skin=hx('f0c09c'), hair=hx('b8482e'), hairstyle='aunty', shirt=hx('19b5a5'), pants=hx('2a3a6a'), shoes=hx('ff6b8a'),
            earring=True, sleeve=1.0, glasses=hx('d0263a'))
