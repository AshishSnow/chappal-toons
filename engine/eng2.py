from eng import *
import eng

DEVA = "Noto Sans Devanagari"


def cat_eyes(ctx, R, iris, eye):
    for ex, s in ((R * 0.42, 1.0), (-R * 0.12, 0.85)):
        ctx.save(); ctx.translate(ex, -R * 0.02); ctx.scale(s, 1)
        if eye == 'happy':
            ctx.set_line_width(8); setc(ctx, OUT); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.arc(0, R * 0.05, R * 0.17, math.pi * 1.1, math.pi * 1.9); ctx.stroke()
        else:
            ew, eh = R * 0.22, R * 0.27
            ellipse(ctx, 0, 0, ew, eh); setc(ctx, light(iris, 0.15)); ctx.fill_preserve(); setc(ctx, OUT); ctx.set_line_width(4); ctx.stroke()
            ctx.save(); ellipse(ctx, 0, 0, ew, eh); ctx.clip()
            ctx.set_source(vgrad(ctx, 0, -eh, 0, eh, [(0, dark(iris, 0.5)), (1, light(iris, 0.5))])); ctx.paint()
            pw = {'focus': 0.025, 'shock': 0.03}.get(eye, 0.07)
            ph = 0.06 if eye == 'shock' else 0.22
            ellipse(ctx, R * 0.03, 0, R * pw, R * ph); setc(ctx, OUT); ctx.fill()
            ctx.restore()
            ellipse(ctx, -R * 0.06, -R * 0.1, R * 0.06, R * 0.07); setc(ctx, (1, 1, 1)); ctx.fill()
            ellipse(ctx, R * 0.08, R * 0.12, R * 0.03, R * 0.03); ctx.fill()
            if eye == 'smug':
                ctx.rectangle(-ew * 1.3, -eh * 1.3, ew * 2.6, eh * 1.05); setc(ctx, eng._cur_fur); ctx.fill()
                ctx.move_to(-ew * 1.15, -eh * 0.25); ctx.line_to(ew * 1.15, -eh * 0.3); setc(ctx, OUT); ctx.set_line_width(6); ctx.stroke()
        ctx.restore()


def draw_cat(ctx, x, y, k, f, c, p):
    """x,y = ground point under body centre. p keys: crouch, stretch, ph(walk), rear, eye, mouse, tail, head(deg), mouth"""
    fur, fur2, iris = c['fur'], c.get('fur2', dark(c['fur'], 0.75)), c.get('iris', hx('ffd23f'))
    eng._cur_fur = fur
    cr, st, ph = p.get('crouch', 0), p.get('stretch', 0), p.get('ph', None)
    ctx.save(); ctx.translate(x, y); ctx.scale(f, 1)
    rear = p.get('rear', 0)
    if rear:
        ctx.translate(-100 * k, 0); ctx.rotate(-math.radians(rear)); ctx.translate(100 * k, 0)
    h = (120 - 55 * cr + 25 * st) * k
    L = (105 + 70 * st) * k
    sh, hp = (L * 0.72, -h), (-L * 0.72, -h + 8 * k)
    leg_len = h
    # tail
    ta = math.radians(p.get('tail', 40))
    tb = (hp[0] - 20 * k, hp[1] - 10 * k)
    t1 = (tb[0] - 90 * k * math.cos(ta), tb[1] - 90 * k * math.sin(ta))
    t2 = (t1[0] - 20 * k, t1[1] - 100 * k * math.sin(ta) - 20 * k)
    ctx.move_to(*tb); ctx.curve_to(tb[0] - 70 * k, tb[1] + 10 * k, t1[0], t1[1], *t2)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    setc(ctx, OUT); ctx.set_line_width(30 * k); ctx.stroke_preserve(); setc(ctx, fur); ctx.set_line_width(19 * k); ctx.stroke()

    def leg(base, sw, back):
        a = math.radians(sw)
        foot = (base[0] + math.sin(a) * leg_len, -abs(math.cos(a)) * 0 + 0)
        knee = ((base[0] + foot[0]) / 2 - (12 * k if back else -8 * k), (base[1] + foot[1]) / 2 + 4 * k)
        chain(ctx, [base, knee, foot], 24 * k, dark(fur, 0.8) if back else fur, fur2, 1)
        ellipse(ctx, foot[0] + 8 * k, foot[1] - 4 * k, 20 * k, 12 * k); fill_out(ctx, dark(fur, 0.8) if back else fur, 5)
    s1 = 0 if ph is None else 22 * math.sin(ph)
    pounce = st
    leg(sh, s1 + 35 * pounce, True); leg(hp, -s1 - 30 * pounce, True)
    # body
    ellipse(ctx, 0, -h - 8 * k, L, 52 * k + 6 * k * cr); fill_out(ctx, fur, 7)
    ctx.save(); ellipse(ctx, 0, -h - 8 * k, L, 52 * k + 6 * k * cr); ctx.clip()
    ellipse(ctx, 0, -h + 30 * k, L * 1.1, 34 * k); setc(ctx, fur2); ctx.fill()
    ellipse(ctx, -L * 0.2, -h - 45 * k, L * 0.6, 12 * k); setc(ctx, light(fur, 0.25)); ctx.fill()
    if c.get('stripes'):
        setc(ctx, c['stripes']); ctx.set_line_width(10 * k)
        for i in range(5):
            xx = -L * 0.6 + i * L * 0.3
            ctx.move_to(xx, -h - 70 * k); ctx.curve_to(xx + 18 * k, -h - 20 * k, xx - 10 * k, -h, xx + 6 * k, -h + 20 * k)
        ctx.stroke()
    ctx.restore()
    leg((sh[0] - 10 * k, sh[1]), -s1 + 25 * pounce, False); leg((hp[0] + 10 * k, hp[1]), s1 - 20 * pounce, False)
    # head
    R = 66 * k
    hc = (sh[0] + 42 * k + 30 * k * st, sh[1] - 52 * k + 30 * k * cr)
    ctx.save(); ctx.translate(*hc); ctx.rotate(math.radians(p.get('head', 0)))
    for ex, s in ((-R * 0.55, 0.85), (R * 0.45, 1)):
        poly(ctx, [(ex - R * 0.4 * s, -R * 0.5), (ex - R * 0.05, -R * 1.35 * s), (ex + R * 0.38 * s, -R * 0.55)]); fill_out(ctx, fur, 6)
        poly(ctx, [(ex - R * 0.22 * s, -R * 0.6), (ex - R * 0.04, -R * 1.1 * s), (ex + R * 0.2 * s, -R * 0.62)]); setc(ctx, hx('ff9fb8')); ctx.fill()
    ellipse(ctx, 0, 0, R * 1.05, R * 0.92); fill_out(ctx, fur, 7)
    if c.get('stripes'):
        ctx.save(); ellipse(ctx, 0, 0, R * 1.05, R * 0.92); ctx.clip(); setc(ctx, c['stripes']); ctx.set_line_width(8 * k)
        for dx in (-0.25, 0.05, 0.35):
            ctx.move_to(R * dx, -R * 0.95); ctx.line_to(R * (dx + 0.04), -R * 0.55)
        ctx.stroke(); ctx.restore()
    ellipse(ctx, R * 0.3, R * 0.42, R * 0.5, R * 0.32); setc(ctx, c.get('muzzle', light(fur, 0.35))); ctx.fill()
    cat_eyes(ctx, R, iris, p.get('eye', 'normal'))
    poly(ctx, [(R * 0.48, R * 0.25), (R * 0.66, R * 0.25), (R * 0.57, R * 0.36)]); fill_out(ctx, hx('ff7aa2'), 3)
    m = p.get('mouth', 'w')
    ctx.set_line_width(5); setc(ctx, OUT); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    if m == 'w':
        ctx.arc(R * 0.5, R * 0.42, R * 0.08, 0.2, math.pi - 0.2); ctx.stroke(); ctx.arc(R * 0.66, R * 0.42, R * 0.08, 0.2, math.pi - 0.2); ctx.stroke()
    elif m == 'open':
        ellipse(ctx, R * 0.57, R * 0.52, R * 0.13, R * 0.14); fill_out(ctx, hx('7a1228'), 4)
    setc(ctx, (1, 1, 1, 0.9)); ctx.set_line_width(3)
    for dy in (-0.05, 0.08):
        ctx.move_to(R * 0.8, R * (0.35 + dy)); ctx.line_to(R * 1.35, R * (0.3 + dy * 2.5))
        ctx.move_to(R * 0.2, R * (0.35 + dy)); ctx.line_to(-R * 0.25, R * (0.3 + dy * 2.5))
    ctx.stroke()
    if p.get('mouse'):
        ctx.save(); ctx.translate(R * 0.7, R * 0.75); ctx.rotate(0.5)
        draw_mouse(ctx, 0, 0, 1.0, 1, dict(eye='shock', dangle=True))
        ctx.restore()
    ctx.restore()
    ctx.restore()


def draw_mouse(ctx, x, y, k, f, p):
    ctx.save(); ctx.translate(x, y); ctx.scale(f * k, k)
    fur = hx('9a8f99')
    ctx.move_to(-50, 0); ctx.curve_to(-110, 10, -120, -50, -170, -30)
    setc(ctx, OUT); ctx.set_line_width(10); ctx.stroke_preserve(); setc(ctx, hx('ffb3c4')); ctx.set_line_width(5); ctx.stroke()
    ellipse(ctx, 0, -35, 62, 42); fill_out(ctx, fur, 6)
    ellipse(ctx, 10, -18, 40, 18); setc(ctx, light(fur, 0.35)); ctx.fill()
    for ex, s in ((20, 0.85), (60, 1)):
        ellipse(ctx, ex, -100, 28 * s, 30 * s); fill_out(ctx, fur, 5)
        ellipse(ctx, ex, -100, 16 * s, 18 * s); setc(ctx, hx('ffb3c4')); ctx.fill()
    ellipse(ctx, 50, -60, 45, 38); fill_out(ctx, fur, 6)
    ellipse(ctx, 92, -55, 8, 7); setc(ctx, hx('ff6b8a')); ctx.fill()
    eye = p.get('eye', 'normal')
    for ex, s in ((60, 1), (38, 0.8)):
        ellipse(ctx, ex, -68, 9 * s, 12 * s); setc(ctx, (1, 1, 1) if eye == 'shock' else OUT); ctx.fill_preserve(); setc(ctx, OUT); ctx.set_line_width(2); ctx.stroke()
        ellipse(ctx, ex + 1, -68, 3 if eye == 'shock' else 3.5, 3 if eye == 'shock' else 4); setc(ctx, OUT if eye == 'shock' else (1, 1, 1)); ctx.fill()
    setc(ctx, OUT); ctx.set_line_width(2)
    for dy in (-4, 4):
        ctx.move_to(92, -55 + dy); ctx.line_to(125, -58 + dy * 2.5)
    ctx.stroke()
    ctx.restore()


def draw_bucket(ctx, x, y, k, tilt, milk=1.0):
    ctx.save(); ctx.translate(x, y); ctx.translate(90 * k, 0); ctx.rotate(math.radians(tilt)); ctx.translate(-90 * k, 0)
    pts = [(-100 * k, -260 * k), (100 * k, -260 * k), (80 * k, 0), (-80 * k, 0)]
    poly(ctx, pts); fill_out(ctx, hx('f4f7ff'), 7)
    ctx.save(); poly(ctx, pts); ctx.clip()
    ctx.rectangle(-120 * k, -150 * k, 240 * k, 80 * k); setc(ctx, hx('2f6bff')); ctx.fill()
    ctx.rectangle(40 * k, -260 * k, 60 * k, 260 * k); setc(ctx, hx('d5ddef')); ctx.fill()
    ctx.restore()
    if milk > 0:
        ellipse(ctx, 0, -258 * k, 98 * k, 24 * k); fill_out(ctx, (1, 1, 1), 5)
    ctx.restore()


def char_head_bust(ctx, x, y, k, ch, p, f=1):
    draw_char(ctx, x, y, k, f, ch, p)


def wrap_hair(ctx, R):
    pts = [(-1.05, 0.05), (-1.12, -0.55), (-0.7, -1.12), (0.1, -1.25), (0.85, -0.95), (1.1, -0.4), (0.95, -0.2), (-0.2, -0.45), (-0.8, -0.1)]
    poly(ctx, [(a * R, b * R) for a, b in pts]); fill_out(ctx, hx('fbfbf3'), 7)
    setc(ctx, hx('cfd3c8')); ctx.set_line_width(5)
    for i in range(4):
        ctx.move_to(-R * 0.95 + i * R * 0.1, -R * (0.3 + i * 0.2)); ctx.curve_to(-R * 0.3, -R * (0.75 + i * 0.12), R * 0.4, -R * (0.75 + i * 0.1), R * 0.95, -R * (0.4 + i * 0.13))
    ctx.stroke()


def text_mixed(ctx, parts, cx, y, ow=12):
    """parts: list of (text, font, size, fill). centred at cx"""
    ctx.save()
    widths = []
    for t, fnt, sz, _ in parts:
        ctx.select_font_face(fnt, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(sz)
        widths.append(ctx.text_extents(t).x_advance)
    tot = sum(widths); x = cx - tot / 2
    ctx.restore()
    for (t, fnt, sz, col), w in zip(parts, widths):
        text(ctx, t, x, y, sz, col, ow=ow, anchor='l', font=fnt)
        x += w


def sunburst(ctx, cx, cy, c1, c2, rot=0, n=18):
    ctx.rectangle(0, 0, W, H); setc(ctx, c1); ctx.fill()
    for i in range(n):
        a0 = rot + i * 2 * math.pi / n
        ctx.move_to(cx, cy); ctx.line_to(cx + math.cos(a0) * 3000, cy + math.sin(a0) * 3000)
        ctx.line_to(cx + math.cos(a0 + math.pi / n) * 3000, cy + math.sin(a0 + math.pi / n) * 3000); ctx.close_path()
    setc(ctx, c2); ctx.fill()
