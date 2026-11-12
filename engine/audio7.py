import numpy as np, wave
import importlib.util, sys
spec = importlib.util.spec_from_file_location("a6", "/home/claude/audio6.py")
# reuse synth helpers without running audio6's main mix: copy minimal helpers here instead
SR = 44100
DUR = 35.0
n = int(SR * DUR)
L = np.zeros(n); R = np.zeros(n)
rng = np.random.default_rng(11)
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


def sweep(f0, f1, d, g=0.2):
    t = t_(d); fr = np.linspace(f0, f1, len(t))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * g * env(d, 0.01, d * 0.5)


def nz(d, k=0.05):
    x = rng.normal(0, 1, int(SR * d)); y = np.convolve(x, np.ones(max(1, int(1 / k))) / max(1, int(1 / k)), 'same')
    return y / (np.abs(y).max() + 1e-9)


def kick(g=1):
    t = t_(0.35); fr = 48 + 120 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 9) * g


def snare():
    t = t_(0.22); return (rng.normal(0, 1, len(t)) * 0.55 + np.sin(2 * np.pi * 185 * t) * 0.45) * np.exp(-t * 18)


def clap():
    t = t_(0.2); return rng.normal(0, 1, len(t)) * (np.exp(-t * 25) + 0.6 * np.exp(-np.maximum(0, t - 0.012) * 30) * (t > 0.012)) * 0.5


def hat(o=False):
    t = t_(0.25 if o else 0.08); x = np.diff(rng.normal(0, 1, len(t)), prepend=0)
    return x * np.exp(-t * (14 if o else 70)) * 0.2


def bass(fq, d):
    t = t_(d); w = 2 * (t * fq % 1) - 1
    return np.tanh(w * 2.5 + np.sin(2 * np.pi * fq * t)) * env(d, 0.004, d * 0.6) * 0.3


def pluck(fq, d=0.3, g=0.2):
    t = t_(d); return (np.sin(2 * np.pi * fq * t) + 0.35 * np.sin(4 * np.pi * fq * t)) * np.exp(-t * 8) * g


def brass(fq, d, g):
    t = t_(d); w = sum(np.sin(2 * np.pi * fq * h * t + 0.3 * h) / h for h in range(1, 9))
    return np.tanh(w * 1.4) * env(d, 0.02, d * 0.7) * g


def chip(fq, d, g=0.08):
    t = t_(d); return np.sign(np.sin(2 * np.pi * fq * t)) * env(d, 0.002, d * 0.5) * g


def mbox(fq, d=0.9, g=0.12):
    t = t_(d); return (np.sin(2 * np.pi * fq * t) + 0.3 * np.sin(2 * np.pi * fq * 3.01 * t)) * np.exp(-t * 4) * g


def tick(g=0.35):
    t = t_(0.04); return np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 120) * g


def groove(t0, t1, bpm, bass_line, chords, hype=False, g=1.0):
    b_ = 60 / bpm
    for b in range(int((t1 - t0) / b_)):
        tb = t0 + b * b_
        place(kick(0.85 * g), tb)
        if b % 2 == 1:
            place(snare(), tb, 0.45 * g); place(clap(), tb, 0.35 * g)
        place(hat(), tb + b_ / 2, g, 0.3); place(hat(b % 4 == 3), tb, 0.6 * g, -0.3)
        place(bass(bass_line[b % len(bass_line)], b_ * 0.9), tb, g)
        if b % 2 == 0:
            for fq in chords[(b // 4) % len(chords)]:
                place(pluck(fq * 2, 0.35, 0.14 * g), tb + b_ / 2, 1, 0.2)


BL = [55, 55, 65.4, 73.4, 55, 55, 82.4, 73.4]
CH = [(220, 277, 330), (196, 247, 294), (174.6, 220, 262), (196, 247, 294)]
# --- hook
place(sweep(300, 2200, 0.5, 0.14), 0.05)
for j, fq in enumerate((2093, 2637, 3136)):
    place(np.sin(2 * np.pi * fq * t_(0.5)) * np.exp(-t_(0.5) * 8) * 0.1, 0.25 + j * 0.06, 1, 0.3 - j * 0.3)
groove(0.7, 6.0, 110, BL, CH)
for fr in (64, 72, 80):
    place(kick(1.2), F(fr)); place(nz(0.12, 0.2) * np.exp(-t_(0.12)[:len(nz(0.12, 0.2))] * 25) * 0.4, F(fr))
for i in range(6):
    place(rng.normal(0, 1, int(SR * 0.03)) * np.exp(-t_(0.03) * 150) * 0.6, F(93 + i * 3.2))
place(brass(196, 0.5, 0.25) + brass(294, 0.5, 0.15), F(112))
place(sweep(320, 420, 0.2, 0.1), 4.1); place(sweep(420, 320, 0.25, 0.1), 4.4)
# clock tick tock (music stops)
for i in range(6):
    place(tick(0.5 if i % 2 == 0 else 0.35) * (1 if i % 2 == 0 else 0.7), F(184) + i * 0.33)
# --- goal montage 7-13: bouncy
groove(7.0, 13.0, 128, [65.4, 65.4, 82.4, 98, 87.3, 87.3, 110, 98], [(262, 330, 392), (349, 440, 523), (294, 370, 440), (392, 494, 587)], g=0.9)
for i in range(14):
    place(nz(0.12, 0.3) * np.sin(np.pi * t_(0.12)[:len(nz(0.12, 0.3))] / 0.12) * 0.12, F(220 + i * 6), 1, 0.4)
for fr in (300, 312, 324, 336):
    place(sweep(500, 1600, 0.1, 0.25), F(fr)); place(rng.normal(0, 1, int(SR * 0.05)) * np.exp(-t_(0.05) * 70) * 0.3, F(fr))
t = t_(2.2)
choir = sum(np.sin(2 * np.pi * fq * t * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * t))) for fq in (523, 659, 784, 1047)) * env(2.2, 0.3, 1.3) * 0.05
place(choir, F(330))
for j, fq in enumerate((523, 587, 659, 784, 880, 1047, 1175, 1319)):
    place(pluck(fq, 0.5, 0.1), F(330) + j * 0.04, 1, -0.6 + j * 0.15)
# --- break 13-20
place(sweep(500, 260, 0.6, 0.12), 13.05)
for j, fq in enumerate((1047, 1319, 1568)):
    place(mbox(fq, 0.4, 0.1), F(420) + j * 0.07)
B2 = 60 / 150 / 2
mel = [659, 784, 988, 784, 659, 523, 587, 659]
tb = 14.4; b = 0
while tb < 20.0:
    speed = 1.0 if tb < 17.0 else 1.0 + (tb - 17.0) * 0.6
    if b % 2 == 0:
        place(kick(0.55), tb)
    place(hat(), tb, 0.5)
    place(chip(mel[b % 8] * (1 if tb < 17 else 1.06), B2 * 0.9, 0.06), tb, 1, 0.2)
    place(chip(mel[b % 8] / 4, B2 * 0.9, 0.05), tb, 1, -0.2)
    tb += B2 / speed; b += 1
for j, fq in enumerate((523, 659, 784, 1047, 1319)):
    place(chip(fq, 0.1, 0.09), F(470) + j * 0.07)
for i in range(30):
    place(tick(0.2), 17.0 + i * 0.1)
place(nz(1.0, 0.08) * np.sin(np.pi * t_(1.0)[:len(nz(1.0, 0.08))] / 1.0) * 0.25, 17.0)
for i, st in enumerate((118, 150, 182)):
    place(sweep(300, 900, 0.25, 0.12), F(390 + st))
# --- 11:58
for i in range(3):
    place(tick(0.6), 20.0 + i * 0.5)
t = t_(1.6); place(np.sin(2 * np.pi * np.cumsum(40 + 50 * np.exp(-t * 5)) / SR) * np.exp(-t * 2) * 0.8, F(640))
place(brass(98, 0.35, 0.35) + brass(147, 0.35, 0.2), F(641))
t = t_(1.0)
yawn = np.sin(2 * np.pi * np.cumsum(np.linspace(380, 150, len(t)) * (1 + 0.02 * np.sin(2 * np.pi * 6 * t))) / SR) * np.sin(np.pi * t) * 0.22
place(yawn + nz(1.0, 0.1)[:len(t)] * np.sin(np.pi * t) * 0.06, F(662))
scrib = rng.normal(0, 1, int(SR * 1.5)) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 12 * t_(1.5)))) * 0.06
place(np.convolve(scrib, np.ones(8) / 8, 'same'), F(696))
place(rng.normal(0, 1, int(SR * 0.08)) * np.exp(-t_(0.08) * 50) * 0.8, F(740)); place(kick(0.8), F(740))
for j, fq in enumerate((784, 988, 1175)):
    place(pluck(fq, 0.4, 0.12), F(758) + j * 0.08)
# --- sleep
place(rng.normal(0, 1, int(SR * 0.02)) * 0.8 * np.exp(-t_(0.02) * 200), F(789))
place(nz(0.9, 0.08) * np.sin(np.pi * t_(0.9)[:len(nz(0.9, 0.08))] / 0.9) * 0.4, F(792))
t = t_(0.5); place(np.sin(2 * np.pi * np.cumsum(220 + 160 * np.sin(2 * np.pi * 7 * t) * np.exp(-t * 4)) / SR) * np.exp(-t * 5) * 0.3, F(822))
lull = [784, 659, 523, 659, 784, 880, 784, 659, 587, 523, 587, 659]
for i, fq in enumerate(lull * 2):
    at = 27.6 + i * 0.45
    if at < 32.9:
        place(mbox(fq, 1.0, 0.1), at, 1, (-1) ** i * 0.3)
for i in range(3):
    at = F(822 + 40) + i * (80 / 30)
    s_ = nz(1.2, 0.03); tt = t_(1.2)[:len(s_)]
    place(s_ * np.sin(np.pi * tt / 1.2) ** 2 * 0.3 + np.sin(2 * np.pi * 70 * tt) * np.sin(np.pi * tt / 1.2) ** 2 * 0.08, at)
# --- next day loop
for i in range(5):
    place(sweep(2800, 3600 + i * 200, 0.08, 0.08) + 0, 33.0 + i * 0.14, 1, 0.5)
groove(33.3, 35.0, 110, BL, CH)
place(brass(196, 0.5, 0.25) + brass(294, 0.5, 0.15), F(1020))

mix = np.stack([L, R], 1)
mix = np.tanh(mix / np.abs(mix).max() * 1.3) / np.tanh(1.3) * 0.92
mix[-int(0.15 * SR):] *= np.linspace(1, 0, int(0.15 * SR))[:, None]
with wave.open('out/study_audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('ok')
