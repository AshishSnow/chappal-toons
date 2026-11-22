"""Hand-drawn 'cute sketch' look: wobbly double pencil outlines with gentle line-boil, slightly
off-register flat fills, and a warm paper-grain finish. Used by doodle.fl / eng.fill_out."""
import cairo, math
import numpy as np

ON = [True]       # sketch outlines on/off
BOIL = [0]        # set to frame // 4 by render() -> outlines redraw ~7.5x per second (classic line boil)
AMP = 1.7         # wobble amplitude in device px
STEP = 13.0       # resample spacing in device px


def _polys(path):
    out, cur = [], []
    for kind, pts in path:
        if kind == cairo.PATH_MOVE_TO:
            if len(cur) > 1:
                out.append((cur, False))
            cur = [pts]
        elif kind == cairo.PATH_LINE_TO:
            cur.append(pts)
        elif kind == cairo.PATH_CLOSE_PATH:
            if cur:
                cur.append(cur[0]); out.append((cur, True)); cur = [cur[0]]
    if len(cur) > 1:
        out.append((cur, False))
    return out


def _resample(pts, step):
    a = np.asarray(pts, float)
    seg = np.hypot(*np.diff(a, axis=0).T)
    L = seg.sum()
    if L < 1e-6:
        return a
    n = max(3, int(L / step) + 1)
    s = np.concatenate([[0], np.cumsum(seg)])
    t = np.linspace(0, L, n)
    return np.stack([np.interp(t, s, a[:, 0]), np.interp(t, s, a[:, 1])], 1)


def _wobble(a, seed, amp, closed):
    n = len(a)
    if n < 3:
        return a
    d = np.gradient(a, axis=0)
    ln = np.hypot(d[:, 0], d[:, 1]) + 1e-9
    nrm = np.stack([-d[:, 1] / ln, d[:, 0] / ln], 1)
    rnd = np.random.default_rng(seed)
    k = np.arange(n) / n * 2 * math.pi
    off = np.zeros(n)
    for fq in (1, 2, 3, 5):
        off += rnd.uniform(-1, 1) / fq ** 0.6 * np.sin(fq * k * (1 if closed else 0.7) + rnd.uniform(0, 6.28))
    off += rnd.normal(0, 0.18, n)
    if not closed:
        off *= np.minimum(1, np.minimum(np.arange(n), np.arange(n)[::-1]) / 3 + 0.4)
    return a + nrm * (off * amp)[:, None]


def stroke(ctx, col, w):
    """sketchy replacement for stroke() of the current path (path is consumed)."""
    if not ON[0] or w <= 0:
        ctx.set_source_rgba(*col) if len(col) == 4 else ctx.set_source_rgb(*col)
        ctx.set_line_width(w); ctx.stroke(); return
    path = ctx.copy_path_flat()
    ctx.new_path()
    sx, sy = ctx.user_to_device_distance(1, 0)
    sc = max(1e-6, math.hypot(sx, sy))
    step, amp = STEP / sc, AMP / sc * min(1.6, max(0.6, w * sc / 6))
    ctx.save()
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i, (pts, closed) in enumerate(_polys(path)):
        a = _resample(pts, step)
        h = int(abs(a[0, 0] * 7.3 + a[0, 1] * 3.1 + len(a) * 13)) % 100000
        for pas, (wf, alpha, af) in enumerate(((0.82, 1.0, 1.0), (0.38, 0.55, 1.6))):
            b = _wobble(a, h * 31 + BOIL[0] * 977 + pas * 7, amp * af, closed)
            if pas == 1 and len(b) > 4:      # second, lighter pencil pass with a little overshoot
                ext = (b[1] - b[0]) * -1.2
                b = np.vstack([b[:1] + ext, b])
            ctx.move_to(*b[0])
            for q in b[1:]:
                ctx.line_to(*q)
            if len(col) == 4:
                ctx.set_source_rgba(col[0], col[1], col[2], col[3] * alpha)
            else:
                ctx.set_source_rgba(col[0], col[1], col[2], alpha)
            ctx.set_line_width(w * wf * (1.12 if pas == 0 else 1)); ctx.stroke()
    ctx.restore()


_PAPER = {}


def _paper(h, w):
    if (h, w) not in _PAPER:
        rng = np.random.default_rng(11)
        g = rng.normal(0, 1, (h // 2, w // 2)).astype(np.float32)
        import cv2
        g = cv2.GaussianBlur(g, (0, 0), 1.2)
        g = cv2.resize(g, (w, h))
        fib = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), sigmaX=6, sigmaY=0.8)
        tex = 1 - 0.035 * np.abs(g) / (np.abs(g).max() + 1e-6) * 3 - 0.02 * np.clip(fib / (np.abs(fib).max() + 1e-6) * 4, -1, 1)
        yy, xx = np.mgrid[0:h, 0:w]
        warm = np.ones((h, w, 3), np.float32)
        warm[..., 0] *= 0.975   # B
        warm[..., 1] *= 0.993   # G  -> slightly warm/cream paper
        _PAPER[(h, w)] = (np.clip(tex, 0.86, 1.02)[..., None] * warm).astype(np.float32)
    return _PAPER[(h, w)]


def paper(surface):
    """in-place paper-grain finish on an RGB24 cairo surface"""
    surface.flush()
    w, h = surface.get_width(), surface.get_height()
    buf = np.ndarray((h, surface.get_stride() // 4, 4), np.uint8, surface.get_data())[:, :w]
    t = _paper(h, w)
    buf[..., :3] = np.clip(buf[..., :3].astype(np.float32) * t, 0, 255).astype(np.uint8)
    surface.mark_dirty()
