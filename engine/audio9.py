import numpy as np, wave
import importlib.util, sys
spec = importlib.util.spec_from_file_location("a6", "/home/claude/audio6.py")
# reuse synth helpers without running audio6's main mix: copy minimal helpers here instead
SR = 44100
DUR = 35.0
n = int(SR * DUR)
L = np.zeros(n); R = np.zeros(n)
rng = np.random.default_rng(31)
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



def bell(at, g=0.35):
    for fq, dt in ((659, 0), (523, 0.38)):
        t = t_(1.2)
        place((np.sin(2 * np.pi * fq * t) + 0.5 * np.sin(2 * np.pi * fq * 2.76 * t) + 0.25 * np.sin(2 * np.pi * fq * 5.4 * t)) * np.exp(-t * 2.5) * g, at + dt)


def harp_up(at, g=0.1):
    for j, fq in enumerate((523, 587, 659, 784, 880, 1047, 1175, 1319)):
        place(pluck(fq, 0.5, g), at + j * 0.04, 1, -0.6 + j * 0.15)


def stab(at, g=0.5):
    place(brass(73.4, 0.4, g) + brass(110, 0.4, g * 0.5), at); place(kick(1.2), at)


def tom(fq=90, g=0.8):
    t = t_(0.3); return np.sin(2 * np.pi * np.cumsum(fq + 60 * np.exp(-t * 20)) / SR) * np.exp(-t * 10) * g


def whoosh(at, d=0.35, g=0.5):
    s_ = nz(d, 0.12); tt = t_(d)[:len(s_)]; place(s_ * np.sin(np.pi * tt / d) * g, at)


def boing(at, g=0.25):
    t = t_(0.5); place(np.sin(2 * np.pi * np.cumsum(220 + 160 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 5)) / SR) * np.exp(-t * 4) * g, at)


def sad_trombone(at):
    for j, fq in enumerate((233, 220, 207, 196)):
        d = 0.35 if j < 3 else 0.9
        t = t_(d); fr = fq * (1 + (0.01 * np.sin(2 * np.pi * 6 * t) if j == 3 else 0))
        w = sum(np.sin(2 * np.pi * np.cumsum(fr * h * np.ones_like(t)) / SR) / h for h in range(1, 7))
        place(np.tanh(w) * env(d, 0.03, d * 0.8) * 0.18, at + j * 0.36)



def sizzle(at, d, g=0.12):
    x = rng.normal(0, 1, int(SR * d)); x = np.diff(x, prepend=0)
    place(x * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * t_(d))) * g * np.minimum(1, t_(d) / 0.3) * np.minimum(1, (d - t_(d)) / 0.3), at)


def creak(at, g=0.12):
    t = t_(0.45); place(np.tanh(np.sin(2 * np.pi * np.cumsum(260 + 90 * np.sin(2 * np.pi * 2 * t)) / SR) * 3) * env(0.45, 0.05, 0.25) * g, at, 1, 0.3)


def beep(at, fq=2000, g=0.18):
    place(np.sin(2 * np.pi * fq * t_(0.09)) * env(0.09, 0.003, 0.05) * g, at)


def cricket(at, g=0.05):
    for k in range(3):
        t = t_(0.04); place(np.sin(2 * np.pi * 4200 * t) * np.sin(np.pi * t / 0.04) * g, at + k * 0.06, 1, 0.5)


def snore(at, g=0.3):
    s_ = nz(1.3, 0.03); tt = t_(1.3)[:len(s_)]
    place(s_ * np.sin(np.pi * tt / 1.3) ** 2 * g + np.sin(2 * np.pi * 65 * tt) * np.sin(np.pi * tt / 1.3) ** 2 * g * 0.3, at)


# 0-3.3 heat
sizzle(0.0, 3.3, 0.1)
for k in range(4):
    creak(1.3 + k * 0.8)
for k in range(6):
    place(bass([55, 52, 49, 46.2, 49, 52][k], 0.5), 0.2 + k * 0.5, 0.6)
for j, fq in enumerate((2093, 2637, 3136)):
    place(np.sin(2 * np.pi * fq * t_(0.5)) * np.exp(-t_(0.5) * 8) * 0.1, F(80) + j * 0.05)
# slow-mo reach
place(sweep(80, 40, 1.0, 0.4), F(100))
t = t_(1.1); place(sum(np.sin(2 * np.pi * fq * t * (1 + 0.004 * np.sin(2 * np.pi * 5 * t))) for fq in (440, 554, 659)) * env(1.1, 0.4, 0.8) * 0.07, F(100))
# beeps down to 16
for k in range(9):
    beep(F(132) + k * 5 / 30, 2000)
for j, fq in enumerate((1047, 1319, 1568, 2093)):
    place(pluck(fq, 0.5, 0.12), F(172) + j * 0.05)
# cold bliss
whoosh(F(176), 1.2, 0.5)
for k in range(6):
    place(np.sin(2 * np.pi * [1568, 1760, 2093, 1760, 1568, 1319][k] * t_(0.6)) * np.exp(-t_(0.6) * 5) * 0.07, F(180) + k * 0.33, 1, (-1) ** k * 0.4)
groove(F(180), F(250), 90, [65.4, 65.4, 82.4, 73.4], [(262, 330, 392), (220, 262, 330)], g=0.55)
# meanwhile: dad
for k in range(3):
    place(nz(0.15, 0.3) * np.exp(-t_(0.15)[:len(nz(0.15, 0.3))] * 15) * 0.25, F(255) + k * 0.4)
stab(F(280), 0.55)
for k in range(10):
    beep(F(282) + k * 0.2, 1400, 0.16)
whoosh(F(330), 0.4, 0.6); place(kick(1.0), F(336))
stab(F(336), 0.45)
# lecture
stab(F(360), 0.45); stab(F(400), 0.5)
s_ = nz(1.3, 0.25); place(s_ * 0.15 * np.minimum(1, t_(1.3)[:len(s_)] / 0.1), F(386))
for k in range(11):
    beep(F(450) + k * 3.5 / 30, 1600 + k * 40)
# fan + heat back
t = t_(2.6); place((np.sin(2 * np.pi * 90 * t) * 0.5 + nz(2.6, 0.05)[:len(t)] * 0.5) * (0.6 + 0.4 * np.sin(2 * np.pi * 6 * t)) * 0.12 * np.minimum(1, t / 0.4), F(492))
sizzle(F(500), 2.0, 0.08)
place(kick(0.8), F(525)); place(nz(0.08, 0.3) * 0.3, F(525))
# night: crickets + tick
for k in range(14):
    cricket(F(560) + k * 0.42)
for k in range(10):
    place(tick(0.25), F(560) + k * 0.5)
# spy sneak
spy = [220, 0, 262, 0, 247, 0, 220, 208]
for k in range(16):
    if spy[k % 8]:
        place(pluck(spy[k % 8], 0.18, 0.18), F(610) + k * 0.1, 1, -0.2)
    if k % 4 == 0:
        place(bass(55, 0.2), F(610) + k * 0.1, 0.6)
# reveal cold room
creak(F(660), 0.2); whoosh(F(664), 1.0, 0.5)
t = t_(1.5); place(np.sin(2 * np.pi * np.cumsum(40 + 50 * np.exp(-t * 5)) / SR) * np.exp(-t * 2) * 0.7, F(668))
for k in range(3):
    snore(F(676) + k * 1.4, 0.25)
boing(F(716), 0.3)
# dad wakes
snore(F(760), 0.25)
stab(F(778), 0.4)
stab(F(794), 0.35)
s_ = nz(0.5, 0.1); place(s_ * np.sin(np.pi * t_(0.5)[:len(s_)] / 0.5) * 0.3, F(850))
for j, fq in enumerate((392, 349, 311)):
    place(pluck(fq, 0.3, 0.12), F(866) + j * 0.22)
# fridge ending
t = t_(1.7); place(np.sin(2 * np.pi * 60 * t) * 0.06 + nz(1.7, 0.02)[:len(t)] * 0.03, 30.0)
harp_up(30.05, 0.08)
stab(F(950), 0.45)
whoosh(F(986), 0.45, 0.6)
place(kick(1.6), F(1000)); place(rng.normal(0, 1, int(SR * 0.08)) * np.exp(-t_(0.08) * 40) * 0.9, F(1000)); boing(F(1002), 0.3)
for j in range(5):
    place(np.sin(2 * np.pi * (2200 + j * 300) * t_(0.3)) * np.exp(-t_(0.3) * 10) * 0.06, F(1006) + j * 0.08, 1, (-1) ** j * 0.5)

mix = np.stack([L, R], 1)
mix = np.tanh(mix / np.abs(mix).max() * 1.3) / np.tanh(1.3) * 0.92
mix[-int(0.15 * SR):] *= np.linspace(1, 0, int(0.15 * SR))[:, None]
with wave.open('out/ac_audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('ok')
