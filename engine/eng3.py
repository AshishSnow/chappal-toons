from eng2 import *


def shades_acc(ctx, R, pose):
    a = pose.get('shades', 1)
    if a <= 0:
        return
    dy = pose.get('shades_dy', 0) * R
    ctx.save(); ctx.translate(0, R * 0.08 + dy)
    for ex, s in ((R * 0.45, 1.0), (-R * 0.08, 0.8)):
        ctx.save(); ctx.translate(ex, 0); ctx.scale(s, 1)
        poly(ctx, [(-R * 0.3, -R * 0.18), (R * 0.3, -R * 0.2), (R * 0.26, R * 0.12), (R * 0.05, R * 0.22), (-R * 0.24, R * 0.14)])
        ctx.set_source(vgrad(ctx, 0, -R * 0.2, 0, R * 0.22, [(0, hx('3a3a52')), (1, hx('07070c'))])); ctx.fill_preserve()
        setc(ctx, OUT); ctx.set_line_width(6); ctx.stroke()
        poly(ctx, [(-R * 0.2, -R * 0.12), (-R * 0.05, -R * 0.13), (-R * 0.16, R * 0.06)]); setc(ctx, (1, 1, 1, 0.55)); ctx.fill()
        ctx.restore()
    ctx.move_to(R * 0.13, -R * 0.12); ctx.line_to(R * 0.18, -R * 0.12); setc(ctx, OUT); ctx.set_line_width(8); ctx.stroke()
    ctx.move_to(-R * 0.32, -R * 0.14); ctx.line_to(-R * 0.75, -R * 0.2); ctx.stroke()
    ctx.restore()


def mom_acc(ctx, R, pose):
    # bun
    ellipse(ctx, -R * 0.35, -R * 1.05, R * 0.42, R * 0.36); fill_out(ctx, hx('1d1626'), 7)
    ellipse(ctx, -R * 0.42, -R * 1.15, R * 0.18, R * 0.08, -0.3); setc(ctx, hx('5a4a70')); ctx.fill()
    ctx.move_to(-R * 0.72, -R * 0.95); ctx.line_to(R * 0.05, -R * 1.2); setc(ctx, hx('ffcc1f')); ctx.set_line_width(7); ctx.stroke()
    # bindi
    ellipse(ctx, R * 0.25, -R * 0.42, R * 0.07, R * 0.07); fill_out(ctx, hx('e0123a'), 3)
    # earring
    ellipse(ctx, -R * 0.55, R * 0.42, R * 0.1, R * 0.1); fill_out(ctx, hx('ffcc1f'), 4)


def dupatta(ctx, x, y, k, f, sway=0):
    """sash over the shoulder, drawn after the body in world coords around hip x,y"""
    ctx.save(); ctx.translate(x, y); ctx.scale(f, 1)
    pts = [(-30 * k, -128 * k), (8 * k, -132 * k), (38 * k, 5 * k), (60 * k + sway * 12 * k, 95 * k), (30 * k + sway * 12 * k, 100 * k), (10 * k, 12 * k)]
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path(); fill_out(ctx, hx('ffcc1f'), 6)
    ctx.move_to(-12 * k, -120 * k); ctx.line_to(25 * k + sway * 8 * k, 40 * k); setc(ctx, hx('e0a400')); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()


BOY = dict(skin=hx('e8b48a'), hair=hx('1b1530'), style='spiky', shirt=hx('ffcc1f'), pants=hx('2f6bff'), sleeve=1.0, shoes=hx('ff3b5c'),
           iris=hx('5a3a20'), acc=shades_acc)
MOM = dict(skin=hx('d9a07a'), hair=hx('1d1626'), style='short', shirt=hx('8a3cff'), robe=hx('8a3cff'), pants=hx('ff9fd0'), sleeve=0.6,
           shoes=hx('ffcc1f'), iris=hx('3b2412'), acc=mom_acc)


def keychain(ctx, x, y, a):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a)
    ctx.arc(0, 0, 22, 0, 2 * math.pi); setc(ctx, OUT); ctx.set_line_width(9); ctx.stroke_preserve(); setc(ctx, hx('ffd23f')); ctx.set_line_width(5); ctx.stroke()
    ctx.move_to(0, 22); ctx.line_to(0, 70); setc(ctx, OUT); ctx.set_line_width(14); ctx.stroke_preserve(); setc(ctx, hx('d0d6e6')); ctx.set_line_width(7); ctx.stroke()
    ctx.rectangle(0, 52, 16, 6); ctx.rectangle(0, 62, 12, 6); setc(ctx, hx('d0d6e6')); ctx.fill()
    ctx.restore()


def slipper(ctx, x, y, a, s=1):
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 30, 75); fill_out(ctx, hx('2fbf5a'), 6)
    ellipse(ctx, 0, -10, 22, 62); setc(ctx, hx('7cf08a')); ctx.fill()
    ctx.move_to(-22, -20); ctx.curve_to(-10, -50, 10, -50, 22, -20); setc(ctx, OUT); ctx.set_line_width(12); ctx.stroke_preserve(); setc(ctx, hx('ff3b5c')); ctx.set_line_width(7); ctx.stroke()
    ctx.restore()


def run_pose(ph, **kw):
    s = math.sin(ph)
    d = P(torso=14, lhip=38 * s, lkn=-20 - 45 * max(0, s), rhip=-38 * s, rkn=-20 - 45 * max(0, -s),
          lsh=-45 * s, lel=70, rsh=45 * s, rel=70)
    d.update(kw); return d
