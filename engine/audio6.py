import numpy as np, wave

SR = 44100
DUR = 34.0
n = int(SR * DUR)
L = np.zeros(n); R = np.zeros(n)
rng = np.random.default_rng(3)
F = lambda fr: fr / 30.0


def t_(d):
    return np.arange(int(SR * d)) / SR


def place(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= n or i < 0:
        return
    s = sig[: n - i] * gain
    L[i:i + len(s)] += s * (1 - max(0, pan)); R[i:i + len(s)] += s * (1 + min(0, pan))


def env(d, a=0.005, r=None):
    t = t_(d); e = np.minimum(1, t / a)
    return e * np.exp(-t / r) if r else e


def sweep(f0, f1, d, g=0.2, shape='sin'):
    t = t_(d); fr = np.linspace(f0, f1, len(t)); ph = 2 * np.pi * np.cumsum(fr) / SR
    w = np.sin(ph) if shape == 'sin' else np.sign(np.sin(ph)) * 0.6
    return w * g * env(d, 0.01, d * 0.5)


def noise_f(d, lo=0.02):
    x = rng.normal(0, 1, int(SR * d)); y = np.zeros_like(x); a = 0
    for i in range(len(x)):
        a += lo * (x[i] - a); y[i] = a
    return y / (np.abs(y).max() + 1e-9)


def kick(g=1):
    t = t_(0.35); fr = 48 + 120 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 9) * g


def snare():
    t = t_(0.22); return (rng.normal(0, 1, len(t)) * 0.55 + np.sin(2 * np.pi * 185 * t) * 0.45) * np.exp(-t * 18)


def clap():
    t = t_(0.2); x = rng.normal(0, 1, len(t)); e = np.exp(-t * 25) + 0.6 * np.exp(-np.maximum(0, t - 0.012) * 30) * (t > 0.012)
    return x * e * 0.5


def hat(o=False):
    t = t_(0.25 if o else 0.08); x = np.diff(rng.normal(0, 1, len(t)), prepend=0)
    return x * np.exp(-t * (14 if o else 70)) * 0.22


def bass(fq, d):
    t = t_(d); w = 2 * (t * fq % 1) - 1
    return np.tanh(w * 2.5 + np.sin(2 * np.pi * fq * t)) * env(d, 0.004, d * 0.6) * 0.33


def pluck(fq, d=0.3, g=0.2):
    t = t_(d); return (np.sin(2 * np.pi * fq * t) + 0.35 * np.sin(4 * np.pi * fq * t)) * np.exp(-t * 8) * g


def lead(fq, d, g=0.12):
    t = t_(d); w = 2 * (t * fq * (1 + 0.003 * np.sin(2 * np.pi * 6 * t)) % 1) - 1
    return w * env(d, 0.01, d * 0.8) * g


def brass(fq, d, g):
    t = t_(d); w = sum(np.sin(2 * np.pi * fq * h * t + 0.3 * h) / h for h in range(1, 9))
    return np.tanh(w * 1.4) * env(d, 0.02, d * 0.7) * g


def chip(fq, d, g=0.1):
    t = t_(d); return np.sign(np.sin(2 * np.pi * fq * t)) * env(d, 0.002, d * 0.5) * g


# ---------------- 0-15s swag groove 120 bpm
BEAT = 0.5
BL = [55, 55, 65.4, 73.4, 55, 55, 82.4, 73.4]
CH = [(220, 277, 330), (196, 247, 294), (174.6, 220, 262), (196, 247, 294)]
for b in range(int((15.0 - 0.6) / BEAT)):
    tb = 0.6 + b * BEAT
    hype = tb >= 11.0
    place(kick(1.0 if hype else 0.85), tb)
    if b % 2 == 1:
        place(snare(), tb, 0.5); place(clap(), tb, 0.6 if hype else 0.3)
    place(hat(), tb + 0.25, 1.0, 0.3); place(hat(b % 4 == 3), tb, 0.6, -0.3)
    if hype:
        place(hat(), tb + 0.125, 0.7, 0.4); place(hat(), tb + 0.375, 0.7, -0.4)
    place(bass(BL[b % 8], 0.45), tb)
    if b % 2 == 0:
        for fq in CH[(b // 4) % 4]:
            place(pluck(fq * 2, 0.35, 0.16), tb + 0.25, 1, 0.2)
    if hype:
        mel = [880, 988, 1175, 988, 880, 784, 880, 659]
        place(lead(mel[b % 8], 0.4), tb, 1.0, -0.2)
# hook: shades shing + glint
place(sweep(400, 2400, 0.45, 0.15), 0.0)
for j, fq in enumerate((2093, 2637, 3136)):
    place(np.sin(2 * np.pi * fq * t_(0.5)) * np.exp(-t_(0.5) * 8) * 0.1, 0.5 + j * 0.05, 1, 0.3 - j * 0.3)
# snap
place(rng.normal(0, 1, int(SR * 0.05)) * np.exp(-t_(0.05) * 90) * 0.9, F(72))
# homework: hmm? blip, toss whoosh, thud
place(sweep(300, 450, 0.25, 0.15), F(110)); place(sweep(450, 300, 0.25, 0.15), F(118))
place(noise_f(0.45, 0.08) * np.sin(np.pi * t_(0.45) / 0.45) * 0.7, F(146))
place(kick(1.3), F(176)); place(noise_f(0.2, 0.05) * np.exp(-t_(0.2) * 15) * 0.6, F(176))
# gaming bleeps + victory
for i in range(16):
    place(chip([523, 659, 784, 1047][i % 4] * (1 + (i % 3) * 0.5), 0.07, 0.08), F(205 + i * 6), 1, 0.3)
for j, fq in enumerate((523, 659, 784, 1047)):
    place(brass(fq, 0.18 if j < 3 else 0.6, 0.14), F(300) + j * 0.12)
# ---------------- 15.0 scratch / stop, creak
t = t_(0.4); sc = rng.normal(0, 1, len(t)) * np.sin(2 * np.pi * (1000 - 2400 * t) * t)
place(np.tanh(sc) * np.exp(-t * 4) * 0.5, 15.0)
t = t_(1.6)
creak = np.sin(2 * np.pi * np.cumsum(180 + 70 * np.sin(2 * np.pi * 1.3 * t) + 40 * rng.normal(0, 1, len(t)) * 0.05) / SR)
creak = np.tanh(creak * 3) * (0.5 + 0.5 * np.sin(2 * np.pi * 23 * t) ** 2) * env(1.6, 0.1, 0.9) * 0.18
place(creak, 15.35, 1, -0.5)
# drone + heartbeat 15.3-23
t = t_(7.7)
drone = (np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 58.3 * t)) * (0.6 + 0.4 * np.sin(2 * np.pi * 4 * t)) * 0.16
drone *= np.minimum(1, t / 0.8) * np.minimum(1, (7.7 - t) / 0.6)
place(drone, 15.3)
for i in range(12):
    at = 17.0 + i * (0.55 - i * 0.015)
    for dt, g in ((0, 0.75), (0.14, 0.5)):
        tt = t_(0.18); place(np.sin(2 * np.pi * 48 * tt) * np.exp(-tt * 22) * g, at + dt)
# silhouette sting + light zap + DUN DUN DUN
t = t_(2.0); place(np.sin(2 * np.pi * np.cumsum(38 + 50 * np.exp(-t * 5)) / SR) * np.exp(-t * 1.5) * 0.9, F(510))
place(chip(120, 0.15, 0.25) + rng.normal(0, 1, int(SR * 0.15)) * 0.2 * np.exp(-t_(0.15) * 20), F(544))
for at, fq, d, g in ((F(545), 98, 0.35, 0.4), (F(558), 92.5, 0.35, 0.4), (F(572), 73.4, 1.4, 0.55)):
    place(brass(fq, d, g) + brass(fq * 1.5, d, g * 0.5), at)
place(sweep(200, 1400, 1.1, 0.08), F(560))
for j, fq in enumerate((2637, 3520)):
    place(np.sin(2 * np.pi * fq * t_(0.8)) * np.exp(-t_(0.8) * 5) * 0.14, F(590) + j * 0.03)
# crack, shades clatter, gulp
place(rng.normal(0, 1, int(SR * 0.12)) * np.exp(-t_(0.12) * 35) * 0.7, F(620)); place(chip(2400, 0.08, 0.1), F(620))
for j in range(3):
    place(np.sin(2 * np.pi * (1800 + j * 400) * t_(0.1)) * np.exp(-t_(0.1) * 40) * 0.2, F(668) + j * 0.09)
place(sweep(500, 140, 0.25, 0.3), F(658))
# ---------------- 23-30 fast-forward montage (160 bpm chiptune)
place(noise_f(0.4, 0.1) * np.sin(np.pi * t_(0.4) / 0.4) * 0.8, F(688))
B2 = 60 / 160 / 2
mel2 = [659, 784, 880, 1047, 880, 784, 659, 587]
for b in range(int((29.9 - 23.0) / B2)):
    tb = 23.0 + b * B2
    if b % 2 == 0:
        place(kick(0.6), tb)
    if b % 4 == 2:
        place(snare(), tb, 0.35)
    place(hat(), tb, 0.5)
    place(chip(mel2[b % 8], B2 * 0.9, 0.06), tb, 1, 0.2)
    place(chip(mel2[b % 8] / 4, B2 * 0.9, 0.05), tb, 1, -0.2)
for fr in (712, 728, 744, 760, 776, 792):
    place(sweep(600, 1800, 0.12, 0.25), F(fr)); place(rng.normal(0, 1, int(SR * 0.06)) * np.exp(-t_(0.06) * 60) * 0.4, F(fr))
for i in range(8):
    place(noise_f(0.18, 0.15) * np.sin(np.pi * t_(0.18) / 0.18) * 0.5, F(700 + i * 12), 1, (-1) ** i * 0.6)
scrib = rng.normal(0, 1, int(SR * 1.8)) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 14 * t_(1.8)))) * 0.08
place(np.convolve(scrib, np.ones(8) / 8, 'same'), F(804))
# angelic choir + harp
t = t_(2.0)
choir = sum(np.sin(2 * np.pi * fq * t * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * t))) for fq in (523, 659, 784, 1047)) * env(2.0, 0.3, 1.2) * 0.06
place(choir, F(852))
for j, fq in enumerate((523, 587, 659, 784, 880, 1047, 1175, 1319)):
    place(pluck(fq, 0.5, 0.12), F(850) + j * 0.04, 1, -0.6 + j * 0.15)
# ---------------- 30-34 ending
for b in range(8):
    tb = 30.0 + b * 0.4
    place(pluck([392, 494, 587, 494, 440, 523, 659, 523][b], 0.45, 0.14), tb)
    if b % 2 == 0:
        place(bass([98, 110, 130.8, 110][b // 2], 0.4), tb, 0.6)
for i in range(4):
    place(noise_f(0.06, 0.2) * np.exp(-t_(0.06)[:len(noise_f(0.06, 0.2))] * 40) * 0.6, F(936) + i * 0.47)
place(noise_f(0.6, 0.05) * np.sin(np.pi * t_(0.6) / 0.6) * 0.4, F(976))
place(brass(73.4, 0.6, 0.5) + brass(110, 0.6, 0.25), F(996))
for j, fq in enumerate((2637, 3520)):
    place(np.sin(2 * np.pi * fq * t_(0.6)) * np.exp(-t_(0.6) * 6) * 0.12, F(997) + j * 0.03)

mix = np.stack([L, R], 1)
mix = np.tanh(mix / np.abs(mix).max() * 1.3) / np.tanh(1.3) * 0.92
mix[-int(0.2 * SR):] *= np.linspace(1, 0, int(0.2 * SR))[:, None]
with wave.open('out/mom_audio34.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('ok')
