import cairo, math, random

W, H = 1080, 1920
OUT = (0.07, 0.04, 0.10)
FONT = "Noto Sans CJK JP Black"


def hx(s, a=None):
    s = s.lstrip('#')
    c = tuple(int(s[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return c if a is None else c + (a,)


def dark(c, f=0.72):
    return tuple(x * f for x in c[:3])


def light(c, f=0.35):
    return tuple(x + (1 - x) * f for x in c[:3])


def lerp(a, b, t):
    return a + (b - a) * t


def clamp(x, a=0, b=1):
    return max(a, min(b, x))


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def eout(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ein(t):
    t = clamp(t)
    return t ** 3


def kf(t, keys, fn=ease):
    """keys: list of (time, value) value float or dict"""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            u = fn((t - t0) / (t1 - t0)) if t1 > t0 else 1
            if isinstance(v0, dict):
                return {k: (lerp(v0[k], v1.get(k, v0[k]), u) if isinstance(v0[k], (int, float)) else (v1.get(k, v0[k]) if u > 0.5 else v0[k])) for k in v0}
            return lerp(v0, v1, u)
    return keys[-1][1]


def setc(ctx, c):
    if len(c) == 4:
        ctx.set_source_rgba(*c)
    else:
        ctx.set_source_rgb(*c)


def ellipse(ctx, x, y, rx, ry, ang=0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()


def poly(ctx, pts):
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path()


def fill_out(ctx, c, ow=6):
    ctx.save(); setc(ctx, c); ctx.fill_preserve(); setc(ctx, OUT); ctx.set_line_width(ow)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke(); ctx.restore()


def vgrad(ctx, x0, y0, x1, y1, stops):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    for o, c in stops:
        g.add_color_stop_rgb(o, *c[:3]) if len(c) == 3 else g.add_color_stop_rgba(o, *c)
    return g


# ---------------------------------------------------------------- characters
DEF_POSE = dict(torso=0, head=0, lsh=12, lel=-15, rsh=-12, rel=-15, lhip=6, lkn=-4, rhip=-6, rkn=-4,
                rot=0, eye='normal', mouth='smile', jig=0)


def P(**kw):
    d = dict(DEF_POSE); d.update(kw); return d


def down(a, f):
    a = math.radians(a)
    return (f * math.sin(a), math.cos(a))


def up(a, f):
    a = math.radians(a)
    return (f * math.sin(a), -math.cos(a))


def add(p, v, s):
    return (p[0] + v[0] * s, p[1] + v[1] * s)


def chain(ctx, pts, w, col, sh_col=None, f=1):
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    setc(ctx, OUT); ctx.set_line_width(w + 11); ctx.stroke_preserve()
    setc(ctx, col); ctx.set_line_width(w); ctx.stroke()
    if sh_col:
        # cel shadow strip on the back edge
        ctx.save()
        for a, b in zip(pts, pts[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1
            nx, ny = -dy / L * w * 0.27 * -f, dx / L * w * 0.27 * -f
            ctx.move_to(a[0] + nx, a[1] + ny); ctx.line_to(b[0] + nx, b[1] + ny)
        setc(ctx, sh_col); ctx.set_line_width(w * 0.42); ctx.stroke()
        ctx.restore()


def draw_head(ctx, c, R, f, tilt, ch, pose):
    ctx.save(); ctx.translate(*c); ctx.rotate(math.radians(tilt) * f); ctx.scale(f, 1)
    kind = ch.get('kind', 'normal')
    skin = ch['skin']
    if kind == 'hero':
        mask = ch['mask']
        ellipse(ctx, 0, 0, R * 1.02, R * 1.1); fill_out(ctx, mask, 7)
        ellipse(ctx, -R * 0.25, R * 0.25, R * 0.75, R * 0.7); setc(ctx, dark(mask, 0.85)); ctx.fill()
        ellipse(ctx, 0, 0, R * 1.02, R * 1.1); setc(ctx, OUT); ctx.set_line_width(7); ctx.stroke()
        # stitched seam lines
        ctx.save(); ellipse(ctx, 0, 0, R * 1.0, R * 1.08); ctx.clip()
        ctx.set_line_width(2.5); setc(ctx, dark(mask, 0.55))
        for i in range(-2, 3):
            ctx.move_to(R * 0.15 + i * R * 0.28, -R * 1.05); ctx.curve_to(R * 0.3 + i * R * 0.3, -R * 0.2, R * 0.2 + i * R * 0.3, R * 0.5, R * 0.1 + i * R * 0.3, R * 1.05)
        ctx.stroke(); ctx.restore()
        for ex, s in ((R * 0.42, 1), (-R * 0.25, 0.8)):
            ctx.save(); ctx.translate(ex, -R * 0.05); ctx.scale(s * 1.45, 1.45)
            ctx.move_to(-R * 0.28, -R * 0.05); ctx.curve_to(-R * 0.2, -R * 0.4, R * 0.25, -R * 0.45, R * 0.3, -R * 0.2)
            ctx.curve_to(R * 0.35, R * 0.15, R * 0.05, R * 0.3, -R * 0.15, R * 0.22); ctx.close_path()
            fill_out(ctx, (1, 1, 1), 9)
            ellipse(ctx, R * 0.12, -R * 0.15, R * 0.1, R * 0.05, -0.4); setc(ctx, hx('cfe9ff')); ctx.fill()
            ctx.restore()
        ctx.restore(); return
    if kind == 'dog':
        fur, fur2 = ch['fur'], ch['fur2']
        for ex, s_ in ((-R * 0.7, 0.9), (R * 0.45, 1)):
            ctx.save(); ctx.translate(ex, -R * 0.45); ctx.rotate(0.25 if ex > 0 else -0.25)
            ellipse(ctx, 0, R * 0.45, R * 0.3 * s_, R * 0.62 * s_); fill_out(ctx, fur2, 6); ctx.restore()
        ellipse(ctx, 0, 0, R * 0.95, R * 0.92); fill_out(ctx, fur, 7)
        ellipse(ctx, -R * 0.45, -R * 0.2, R * 0.38, R * 0.45); setc(ctx, light(fur2, 0.25)); ctx.fill()
        ellipse(ctx, R * 0.62, R * 0.42, R * 0.48, R * 0.34); fill_out(ctx, light(fur, 0.4), 6)
        ellipse(ctx, R * 0.98, R * 0.3, R * 0.15, R * 0.11); setc(ctx, OUT); ctx.fill()
        ellipse(ctx, R * 0.94, R * 0.26, R * 0.05, R * 0.03); setc(ctx, (1, 1, 1)); ctx.fill()
        pose = dict(pose)
        # cap
        cap = ch.get('cap')
        if cap:
            ctx.new_path(); ctx.arc(-R * 0.05, -R * 0.15, R * 0.92, math.pi * 1.05, math.pi * 1.95); ctx.close_path(); fill_out(ctx, cap, 7)
            ctx.rectangle(-R * 0.95, -R * 0.3, R * 1.8, R * 0.16); fill_out(ctx, dark(cap, 0.8), 5)
        skin = fur
    # back hair
    if kind not in ('rider', 'dog'):
        hair = ch['hair']
        ellipse(ctx, -R * 0.18, -R * 0.12, R * 1.08, R * 1.06); fill_out(ctx, dark(hair, 0.8), 7)
    if kind != 'dog':
        # face
        ctx.new_path()
        ellipse(ctx, 0, 0, R * 0.95, R * 1.0)
        setc(ctx, OUT); ctx.set_line_width(14); ctx.stroke()
        poly(ctx, [(-R * 0.7, R * 0.35), (R * 0.25, R * 1.12), (R * 0.9, R * 0.3)])
        setc(ctx, OUT); ctx.set_line_width(14); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
        ellipse(ctx, 0, 0, R * 0.95, R * 1.0); setc(ctx, skin); ctx.fill()
        poly(ctx, [(-R * 0.7, R * 0.35), (R * 0.25, R * 1.12), (R * 0.9, R * 0.3)]); ctx.fill()
        # face shade on the back side
        ellipse(ctx, -R * 0.62, R * 0.15, R * 0.4, R * 0.75); setc(ctx, dark(skin, 0.86)); ctx.fill()
        # ear
        ellipse(ctx, -R * 0.55, R * 0.1, R * 0.17, R * 0.24); fill_out(ctx, skin, 5)
        # blush
        for bx in (R * 0.52, -R * 0.12):
            ellipse(ctx, bx, R * 0.5, R * 0.16, R * 0.07); setc(ctx, (1, 0.45, 0.5, 0.45)); ctx.fill()
    eye = pose.get('eye', 'normal')
    iris = ch.get('iris', hx('3a6df0'))
    for ex, s in ((R * 0.45, 1.0), (-R * 0.05, 0.82)):
        ctx.save(); ctx.translate(ex, R * 0.1); ctx.scale(s, 1)
        if eye == 'ko':
            ctx.set_line_width(7); setc(ctx, OUT); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            r = R * 0.17
            ctx.move_to(-r, -r); ctx.line_to(r, r); ctx.move_to(r, -r); ctx.line_to(-r, r); ctx.stroke()
        elif eye == 'happy':
            ctx.set_line_width(8); setc(ctx, OUT); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.arc(0, R * 0.05, R * 0.17, math.pi * 1.1, math.pi * 1.9); ctx.stroke()
        elif eye == 'closed':
            ctx.set_line_width(7); setc(ctx, OUT); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.arc(0, -R * 0.08, R * 0.17, math.pi * 0.15, math.pi * 0.85); ctx.stroke()
        elif eye == 'glare':
            ew, eh = R * 0.22, R * 0.2
            ctx.move_to(-ew, -eh * 0.2); ctx.line_to(ew, -eh * 0.9); ctx.curve_to(ew * 1.1, eh * 0.6, -ew * 0.8, eh * 1.1, -ew, -eh * 0.2); ctx.close_path()
            setc(ctx, (1, 1, 1)); ctx.fill_preserve(); setc(ctx, OUT); ctx.set_line_width(5); ctx.stroke()
            g = cairo.RadialGradient(R * 0.02, R * 0.02, 0, R * 0.02, R * 0.02, R * 0.16)
            g.add_color_stop_rgb(0, 1, 0.95, 0.5); g.add_color_stop_rgb(0.45, 1, 0.2, 0.15); g.add_color_stop_rgb(1, 0.5, 0, 0.05)
            ellipse(ctx, R * 0.02, R * 0.02, R * 0.12, R * 0.12); ctx.set_source(g); ctx.fill()
            ellipse(ctx, R * 0.02, R * 0.02, R * 0.03, R * 0.06); setc(ctx, OUT); ctx.fill()
            ctx.move_to(-ew * 1.2, -eh * 0.3); ctx.line_to(ew * 1.15, -eh * 1.15); setc(ctx, OUT); ctx.set_line_width(10); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        else:
            ew, eh = R * 0.2, R * 0.28
            ellipse(ctx, 0, 0, ew, eh); setc(ctx, (1, 1, 1)); ctx.fill_preserve(); setc(ctx, OUT); ctx.set_line_width(3); ctx.stroke()
            if eye == 'shock':
                ellipse(ctx, R * 0.02, 0, R * 0.055, R * 0.07); setc(ctx, OUT); ctx.fill()
            else:
                ctx.save(); ellipse(ctx, 0, 0, ew, eh); ctx.clip()
                g = vgrad(ctx, 0, -eh, 0, eh, [(0, dark(iris, 0.45)), (0.6, iris), (1, light(iris, 0.5))])
                ellipse(ctx, R * 0.05, R * 0.04, R * 0.16, R * 0.24); ctx.set_source(g); ctx.fill()
                ellipse(ctx, R * 0.05, R * 0.04, R * 0.07, R * 0.11); setc(ctx, OUT); ctx.fill()
                ctx.restore()
                ellipse(ctx, -R * 0.03, -R * 0.1, R * 0.07, R * 0.08); setc(ctx, (1, 1, 1)); ctx.fill()
                ellipse(ctx, R * 0.09, R * 0.12, R * 0.035, R * 0.035); ctx.fill()
            # lash
            ctx.set_line_width(9); setc(ctx, OUT); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.arc(0, R * 0.04, R * 0.24, math.pi * 1.15, math.pi * 1.92); ctx.stroke()
            if eye == 'smug':
                ellipse(ctx, 0, -eh * 0.55, ew * 1.3, eh * 0.6); setc(ctx, skin); ctx.fill()
                ctx.move_to(-ew * 1.1, -eh * 0.05); ctx.line_to(ew * 1.1, -eh * 0.15); setc(ctx, OUT); ctx.set_line_width(7); ctx.stroke()
        ctx.restore()
    # brows
    ctx.set_line_width(6); setc(ctx, dark(ch.get('hair', OUT), 0.6)); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    by = -R * 0.3 if eye != 'shock' else -R * 0.42
    if eye == 'glare':
        ctx.set_line_width(11); ctx.move_to(R * 0.22, by + R * 0.02); ctx.line_to(R * 0.66, by - R * 0.14); ctx.move_to(-R * 0.22, by - R * 0.08); ctx.line_to(R * 0.08, by + R * 0.04); ctx.stroke()
    else:
        ctx.move_to(R * 0.3, by); ctx.line_to(R * 0.62, by - R * 0.05); ctx.move_to(-R * 0.15, by); ctx.line_to(R * 0.08, by - R * 0.03); ctx.stroke()
    # mouth
    m = pose.get('mouth', 'smile')
    mx, my = R * 0.3, R * 0.62
    if m == 'smile':
        ctx.set_line_width(6); setc(ctx, OUT); ctx.arc(mx, my - R * 0.1, R * 0.14, 0.3, math.pi - 0.3); ctx.stroke()
    elif m == 'grin':
        ctx.move_to(mx - R * 0.2, my - R * 0.06); ctx.line_to(mx + R * 0.2, my - R * 0.08)
        ctx.curve_to(mx + R * 0.15, my + R * 0.2, mx - R * 0.15, my + R * 0.2, mx - R * 0.2, my - R * 0.06)
        fill_out(ctx, hx('8a1530'), 4)
        poly(ctx, [(mx - R * 0.17, my - R * 0.05), (mx + R * 0.18, my - R * 0.07), (mx + R * 0.15, my), (mx - R * 0.15, my + R * 0.01)]); setc(ctx, (1, 1, 1)); ctx.fill()
    elif m in ('open', 'scream'):
        s = 1.0 if m == 'open' else 1.6
        ellipse(ctx, mx, my, R * 0.12 * s, R * 0.15 * s); fill_out(ctx, hx('7a1228'), 4)
        ellipse(ctx, mx, my + R * 0.08 * s, R * 0.08 * s, R * 0.05 * s); setc(ctx, hx('ff6b7d')); ctx.fill()
    elif m == 'flat':
        ctx.set_line_width(6); setc(ctx, OUT); ctx.move_to(mx - R * 0.12, my); ctx.line_to(mx + R * 0.12, my); ctx.stroke()
    elif m == 'wavy':
        ctx.set_line_width(6); setc(ctx, OUT); ctx.move_to(mx - R * 0.18, my)
        for i in range(4):
            ctx.rel_line_to(R * 0.09, -R * 0.06 if i % 2 == 0 else R * 0.06)
        ctx.stroke()
    # hair / helmet
    if kind == 'rider':
        hc = ch['helmet']
        ctx.new_path(); ctx.arc(-R * 0.05, -R * 0.05, R * 1.2, math.pi * 0.9, math.pi * 2.08); ctx.close_path()
        fill_out(ctx, hc, 8)
        ctx.save(); ctx.arc(-R * 0.05, -R * 0.05, R * 1.2, math.pi * 0.9, math.pi * 2.08); ctx.close_path(); ctx.clip()
        ctx.rectangle(-R * 1.4, -R * 0.62, R * 2.8, R * 0.2); setc(ctx, ch.get('stripe', (1, 1, 1))); ctx.fill()
        ctx.restore()
        ellipse(ctx, -R * 0.4, -R * 0.85, R * 0.32, R * 0.12, -0.4); setc(ctx, light(hc, 0.65)); ctx.fill()
        poly(ctx, [(R * 0.6, -R * 0.55), (R * 1.45, -R * 0.45), (R * 1.35, -R * 0.25), (R * 0.75, -R * 0.3)]); fill_out(ctx, dark(hc, 0.75), 5)
        ctx.new_path(); ctx.arc(-R * 0.95, R * 0.05, R * 0.22, 0, 2 * math.pi); fill_out(ctx, dark(hc, 0.8), 5)
    elif kind == 'dog':
        pass
    else:
        hair = ch['hair']
        style = ch.get('style', 'spiky')
        pts = []
        if style == 'wrap':
            import eng2; eng2.wrap_hair(ctx, R); ctx.restore(); return
        if style == 'spiky':
            spikes = [(-1.15, -0.1), (-1.3, -0.6), (-0.9, -0.75), (-1.0, -1.25), (-0.4, -1.05), (-0.2, -1.45), (0.25, -1.08), (0.75, -1.3), (0.8, -0.85), (1.25, -0.55),
                      (0.95, -0.35), (1.05, 0.05), (0.7, -0.2), (0.55, 0.15), (0.35, -0.3), (0.1, 0.05), (-0.05, -0.32), (-0.35, 0.0), (-0.55, -0.25), (-0.85, 0.3)]
        elif style == 'short':
            spikes = [(-1.05, 0.1), (-1.1, -0.6), (-0.7, -1.05), (0.0, -1.18), (0.7, -1.0), (1.05, -0.5), (1.0, -0.15), (0.8, -0.3), (0.65, -0.05), (0.4, -0.35),
                      (0.15, -0.15), (-0.1, -0.38), (-0.4, -0.12), (-0.6, -0.35), (-0.85, 0.2)]
        else:  # messy
            spikes = [(-1.1, 0.2), (-1.35, -0.3), (-1.05, -0.5), (-1.2, -1.0), (-0.6, -0.95), (-0.45, -1.4), (0.0, -1.0), (0.5, -1.35), (0.6, -0.9), (1.2, -0.95),
                      (0.95, -0.55), (1.3, -0.25), (0.85, -0.2), (0.75, 0.1), (0.45, -0.3), (0.2, 0.0), (0.0, -0.35), (-0.3, 0.05), (-0.5, -0.3), (-0.8, 0.35)]
        pts = [(x * R, y * R) for x, y in spikes]
        poly(ctx, pts); fill_out(ctx, hair, 7)
        ctx.save(); poly(ctx, pts); ctx.clip()
        ellipse(ctx, R * 0.1, -R * 0.75, R * 0.65, R * 0.14, -0.15); setc(ctx, light(hair, 0.45)); ctx.fill()
        ellipse(ctx, -R * 0.8, -R * 0.2, R * 0.4, R * 0.9); setc(ctx, dark(hair, 0.75)); ctx.fill()
        ctx.restore()
        poly(ctx, pts); setc(ctx, OUT); ctx.set_line_width(7); ctx.stroke()
    if ch.get('acc'):
        ch['acc'](ctx, R, pose)
    ctx.restore()


def draw_char(ctx, x, y, k, f, ch, p):
    """x,y = hip centre; k scale; f facing (+1 right, -1 left)"""
    Lt, Lu, Lf, Lth, Ls, R = 130 * k, 70 * k, 66 * k, 88 * k, 88 * k, 72 * k
    aw, lw = 25 * k, 36 * k
    ctx.save(); ctx.translate(x, y); ctx.rotate(math.radians(p['rot']) * f)
    hip = (0, 0)
    tor = p['torso']
    neck = add(hip, up(tor, f), Lt)
    sh = add(neck, up(tor, f), -14 * k)
    shirt, pants, skin = ch['shirt'], ch['pants'], ch['skin']
    shoes = ch.get('shoes', hx('f4f4f4'))
    sleeve = ch.get('sleeve', 0.55)
    bare = ch.get('bare', False)
    belly = ch.get('belly', 0)

    def arm(a1, a2, back):
        e = add(sh, down(a1, f), Lu); hnd = add(e, down(a1 + a2, f), Lf)
        sc = dark(skin, 0.82) if back else skin
        chain(ctx, [sh, e, hnd], aw, sc, dark(skin, 0.8), f)
        if not bare and sleeve > 0:
            se = (lerp(sh[0], e[0], sleeve * 1.4) if sleeve > 0.7 else lerp(sh[0], e[0], sleeve * 1.8), 0)
            u = min(1, sleeve * 1.8)
            if sleeve > 0.7:
                s_pts = [sh, e, (lerp(e[0], hnd[0], (sleeve - 0.7) * 2.5), lerp(e[1], hnd[1], (sleeve - 0.7) * 2.5))]
            else:
                s_pts = [sh, (lerp(sh[0], e[0], u), lerp(sh[1], e[1], u))]
            col = dark(shirt, 0.82) if back else shirt
            chain(ctx, s_pts, aw + 8 * k, col, dark(shirt, 0.72), f)
        ellipse(ctx, hnd[0], hnd[1], 17 * k, 17 * k); fill_out(ctx, sc, 5)
        return hnd

    def leg(a1, a2, back):
        kn = add(hip, down(a1, f), Lth); ft = add(kn, down(a1 + a2, f), Ls)
        col = dark(pants, 0.8) if back else pants
        chain(ctx, [hip, kn, ft], lw, col, dark(pants, 0.68), f)
        ang = math.radians(a1 + a2)
        ctx.save(); ctx.translate(*ft); ctx.rotate(-ang * f)
        ellipse(ctx, f * 16 * k, 6 * k, 30 * k, 15 * k); fill_out(ctx, dark(shoes, 0.85) if back else shoes, 6)
        ctx.restore()
        return ft

    arm(p['lsh'], p['lel'], True)
    leg(p['lhip'], p['lkn'], True)
    # torso
    hw, sw = 40 * k, 54 * k
    nrm = (math.cos(math.radians(tor)), math.sin(math.radians(tor) * f) * 0)  # perpendicular approx
    u_ = up(tor, f); pn = (-u_[1], u_[0])
    tpts = [add(hip, pn, hw), add(hip, pn, -hw), add(sh, pn, -sw), add(sh, pn, sw)]
    tcol = skin if bare else shirt
    # neck
    chain(ctx, [sh, add(sh, u_, 34 * k)], 26 * k, skin)
    poly(ctx, tpts); fill_out(ctx, tcol, 7)
    if belly > 0:
        bc = add(hip, u_, Lt * 0.38)
        j = p.get('jig', 0)
        bx, by = bc[0] + f * (18 * k + belly * 30 * k) + j * 10 * k, bc[1]
        ellipse(ctx, bx, by, (40 + belly * 48) * k, (54 + belly * 30) * k); fill_out(ctx, tcol if not ch.get('belly_col') else ch['belly_col'], 7)
        ellipse(ctx, bx + f * 22 * k, by - 20 * k, 18 * k, 26 * k); setc(ctx, light(ch.get('belly_col', tcol), 0.4)); ctx.fill()
        ellipse(ctx, bx - f * 30 * k, by + 25 * k, 38 * k, 30 * k); setc(ctx, dark(ch.get('belly_col', tcol), 0.82)); ctx.fill()
    # torso shade
    ctx.save(); poly(ctx, tpts); ctx.clip()
    poly(ctx, [add(hip, pn, -hw), add(hip, pn, -hw * 0.25 * f), add(sh, pn, -sw * 0.2 * f), add(sh, pn, -sw)])
    setc(ctx, dark(tcol, 0.8)); ctx.fill()
    if bare:
        setc(ctx, dark(skin, 0.75)); ctx.set_line_width(3)
        for i in range(3):
            c0 = add(hip, u_, Lt * (0.2 + i * 0.17))
            ctx.move_to(*add(c0, pn, -12 * k)); ctx.line_to(*add(c0, pn, 12 * k))
        ctx.stroke()
        c0 = add(hip, u_, Lt * 0.78)
        ctx.arc(*add(c0, pn, 14 * k), 14 * k, 0.2, 2.8); ctx.stroke()
    if ch.get('emblem'):
        c0 = add(hip, u_, Lt * 0.72); c0 = (c0[0] + f * 8 * k, c0[1])
        st = []
        for i in range(10):
            r = (22 if i % 2 == 0 else 9) * k
            a = -math.pi / 2 + i * math.pi / 5
            st.append((c0[0] + r * math.cos(a), c0[1] + r * math.sin(a)))
        poly(ctx, st); fill_out(ctx, ch['emblem'], 3)
    if ch.get('stripe2'):
        poly(ctx, [add(hip, pn, hw), add(hip, pn, hw * 0.4), add(sh, pn, sw * 0.4), add(sh, pn, sw)]); setc(ctx, ch['stripe2']); ctx.fill()
    ctx.restore()
    # belt
    ctx.set_line_width(14 * k); setc(ctx, dark(pants, 0.6)); ctx.move_to(*add(add(hip, u_, 6 * k), pn, hw)); ctx.line_to(*add(add(hip, u_, 6 * k), pn, -hw)); ctx.stroke()
    if ch.get('robe'):
        leg(p['rhip'], p['rkn'], False)
        kl = add(hip, down(p['lhip'], f), Lth); kr = add(hip, down(p['rhip'], f), Lth)
        xs = sorted([kl, kr], key=lambda q: q[0])
        lo = max(kl[1], kr[1], hip[1] + Lth * 0.8)
        rb = ch['robe']
        sk = [add(hip, pn, hw * 1.05), add(hip, pn, -hw * 1.05), (min(xs[0][0], -hw) - 34 * k, lo + 30 * k), (max(xs[1][0], hw) + 34 * k, lo + 30 * k)]
        sk = [add(sh, pn, sw), add(sh, pn, -sw)] + [sk[1], (min(xs[0][0], -hw) - 34 * k, lo + 30 * k), (max(xs[1][0], hw) + 34 * k, lo + 30 * k), sk[0]]
        poly(ctx, sk); fill_out(ctx, rb, 7)
        ctx.save(); poly(ctx, sk); ctx.clip()
        setc(ctx, dark(rb, 0.8)); ctx.set_line_width(7 * k)
        for i in range(4):
            xx = lerp(sk[3][0], sk[4][0], (i + 0.5) / 4)
            ctx.move_to(lerp(xx, 0, 0.7), hip[1] - 10 * k); ctx.line_to(xx, lo + 40 * k)
        ctx.stroke()
        ctx.move_to(*add(sh, pn, -sw * 0.6)); ctx.line_to(*add(hip, pn, sw * 0.3)); setc(ctx, light(rb, 0.3)); ctx.set_line_width(12 * k); ctx.stroke()
        ctx.restore()
    else:
        leg(p['rhip'], p['rkn'], False)
    head_c = add(neck, up(tor + p['head'] * 0.5, f), R * 0.95)
    draw_head(ctx, head_c, R, f, tor + p['head'], ch, p)
    arm(p['rsh'], p['rel'], False)
    ctx.restore()


# ---------------------------------------------------------------- FX
def speed_lines(ctx, cx, cy, seed, alpha=0.8, n=70, inner=300, col=(1, 1, 1)):
    rnd = random.Random(seed)
    for _ in range(n):
        a = rnd.uniform(0, 2 * math.pi)
        r0 = inner + rnd.uniform(0, 260)
        w = rnd.uniform(4, 16)
        ctx.move_to(cx + math.cos(a + 0.012 * w / 4) * 1800, cy + math.sin(a + 0.012 * w / 4) * 1800)
        ctx.line_to(cx + math.cos(a) * r0, cy + math.sin(a) * r0)
        ctx.line_to(cx + math.cos(a - 0.012 * w / 4) * 1800, cy + math.sin(a - 0.012 * w / 4) * 1800)
        ctx.close_path()
    setc(ctx, col + (alpha,)); ctx.fill()


def hlines(ctx, seed, alpha=0.6, col=(1, 1, 1), y0=0, y1=H, vertical=False):
    rnd = random.Random(seed)
    for _ in range(26):
        if vertical:
            x = rnd.uniform(0, W); L = rnd.uniform(200, 700); y = rnd.uniform(y0, y1)
            ctx.rectangle(x, y, rnd.uniform(3, 9), L)
        else:
            y = rnd.uniform(y0, y1); L = rnd.uniform(200, 700); x = rnd.uniform(-200, W)
            ctx.rectangle(x, y, L, rnd.uniform(3, 10))
    setc(ctx, col + (alpha,)); ctx.fill()


def burst(ctx, x, y, r, n=14, seed=1, col=hx('ffe14d'), col2=hx('ff5a36')):
    rnd = random.Random(seed)
    for rr, c in ((r, col2), (r * 0.72, col), (r * 0.4, (1, 1, 1))):
        pts = []
        for i in range(n * 2):
            a = i * math.pi / n
            q = rr * (1 if i % 2 == 0 else 0.55) * rnd.uniform(0.85, 1.15)
            pts.append((x + q * math.cos(a), y + q * math.sin(a)))
        poly(ctx, pts); fill_out(ctx, c, 6)


def text(ctx, s, x, y, size, fill, outline=OUT, ow=14, ang=0, anchor='c', font=FONT, shadow=True, maxw=None):
    ctx.save()
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)
    ex = ctx.text_extents(s)
    if maxw and ex.width > maxw:
        size = size * maxw / ex.width; ctx.set_font_size(size); ex = ctx.text_extents(s); ow = ow * maxw / ex.width if False else ow
    ctx.translate(x, y); ctx.rotate(ang)
    tx = -ex.x_bearing - ex.width / 2 if anchor == 'c' else (-ex.x_bearing if anchor == 'l' else -ex.x_bearing - ex.width)
    ty = -ex.y_bearing - ex.height / 2
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    if shadow:
        ctx.move_to(tx + 7, ty + 9); ctx.text_path(s); setc(ctx, OUT); ctx.set_line_width(ow); ctx.stroke_preserve(); ctx.fill()
    ctx.move_to(tx, ty); ctx.text_path(s)
    setc(ctx, outline); ctx.set_line_width(ow); ctx.stroke_preserve()
    if isinstance(fill, cairo.Pattern):
        ctx.set_source(fill)
    else:
        setc(ctx, fill)
    ctx.fill()
    ctx.restore()
    return ex.width


def dust(ctx, x, y, t, seed=3, n=9, spread=220, col=hx('e9dcc8')):
    if t <= 0 or t >= 1:
        return
    rnd = random.Random(seed)
    for i in range(n):
        a = rnd.uniform(math.pi * 1.0, math.pi * 2.0)
        d = spread * eout(t) * rnd.uniform(0.4, 1.1)
        r = (40 + 50 * rnd.random()) * (0.5 + t) * (1 - t * 0.6)
        ellipse(ctx, x + math.cos(a) * d, y + math.sin(a) * d * 0.45, r, r * 0.8)
        setc(ctx, col + (0.95 * (1 - t),)); ctx.fill_preserve()
        setc(ctx, OUT + ((1 - t) * 0.8,)); ctx.set_line_width(4); ctx.stroke()


def sweat(ctx, x, y, s=1):
    ctx.move_to(x, y - 30 * s); ctx.curve_to(x + 22 * s, y, x + 16 * s, y + 22 * s, x, y + 22 * s)
    ctx.curve_to(x - 16 * s, y + 22 * s, x - 22 * s, y, x, y - 30 * s)
    fill_out(ctx, hx('8fd8ff'), 4)
    ellipse(ctx, x - 5 * s, y + 6 * s, 4 * s, 7 * s); setc(ctx, (1, 1, 1)); ctx.fill()


def stars_ko(ctx, x, y, t, n=4, r=90):
    for i in range(n):
        a = t * 5 + i * 2 * math.pi / n
        sx, sy = x + math.cos(a) * r, y + math.sin(a) * r * 0.35
        pts = []
        for j in range(10):
            q = (20 if j % 2 == 0 else 8)
            b = -math.pi / 2 + j * math.pi / 5
            pts.append((sx + q * math.cos(b), sy + q * math.sin(b)))
        poly(ctx, pts); fill_out(ctx, hx('ffe14d'), 4)


def cloud(ctx, x, y, s, col=(1, 1, 1), sh=hx('bfd8ff')):
    for dx, dy, r in ((0, 0, 60), (70, -25, 75), (150, 0, 60), (75, 20, 60)):
        ellipse(ctx, x + dx * s, y + dy * s, r * s, r * s * 0.85)
    setc(ctx, OUT); ctx.set_line_width(8); ctx.stroke_preserve(); setc(ctx, col); ctx.fill()
    for dx, dy, r in ((10, 20, 45), (90, 30, 50), (150, 18, 40)):
        ellipse(ctx, x + dx * s, y + dy * s, r * s, r * s * 0.5)
    setc(ctx, sh); ctx.fill()
