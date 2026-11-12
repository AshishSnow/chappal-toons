import numpy as np, wave
import importlib.util, sys
spec = importlib.util.spec_from_file_location("a6", "/home/claude/audio6.py")
# reuse synth helpers without running audio6's main mix: copy minimal helpers here instead
SR = 44100
DUR = 35.0
n = int(SR * DUR)
L = np.zeros(n); R = np.zeros(n)
rng = np.random.default_rng(21)
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


# 0-1.6 angry
stab(0.0); stab(F(22), 0.4)
place(np.convolve(rng.normal(0, 1, int(SR * 1.2)), np.ones(30) / 30, 'same') * np.exp(-t_(1.2) * 2) * 2.0, 0.0)
bell(F(36))
# 1.6 switch to sweet
harp_up(F(48), 0.12)
t = t_(1.5); place(sum(np.sin(2 * np.pi * fq * t) for fq in (523, 659, 784)) * env(1.5, 0.1, 0.9) * 0.06, F(48))
for j, fq in enumerate((2093, 2637, 3136)):
    place(np.sin(2 * np.pi * fq * t_(0.5)) * np.exp(-t_(0.5) * 8) * 0.09, F(50) + j * 0.06, 1, 0.3 - j * 0.3)
# 3-8 war mode drums
b_ = 60 / 140
tb = 3.0
i = 0
while tb < 8.3:
    place(tom(70 if i % 2 == 0 else 95, 0.7), tb, 1, -0.2 if i % 2 else 0.2)
    if i % 4 == 2:
        place(snare(), tb, 0.45)
    place(hat(), tb + b_ / 2, 0.6)
    if i % 2 == 0:
        place(bass([55, 55, 58.3, 49][(i // 2) % 4], b_ * 1.6), tb, 0.9)
    tb += b_; i += 1
stab(3.0, 0.45); stab(4.0, 0.55)
whoosh(4.0, 0.5, 0.5)
for k in range(8):
    whoosh(F(160 + k * 12), 0.25, 0.45); place(kick(0.9), F(160 + k * 12 + 9)); place(nz(0.1, 0.2) * 0.3, F(160 + k * 12 + 9))
for k in range(12):
    place(tick(0.35), 8.7 + k * 0.12)
place(sweep(220, 160, 0.5, 0.15), 9.2)
for j, fq in enumerate((784, 988, 1175)):
    place(pluck(fq, 0.4, 0.12), F(300) + j * 0.08)
# 11-15 special cups
place(rng.normal(0, 1, int(SR * 0.03)) * 0.7 * np.exp(-t_(0.03) * 150), F(350))
t = t_(2.0)
choir = sum(np.sin(2 * np.pi * fq * t * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * t))) for fq in (523, 659, 784, 1047)) * env(2.0, 0.3, 1.2) * 0.07
place(choir, F(352)); harp_up(F(352), 0.1)
boing(F(404))
# 15 doorbell + switch
bell(F(450)); whoosh(F(470), 0.5, 0.4); harp_up(F(472), 0.1)
for k in range(4):
    place(pluck([659, 784, 659, 523][k], 0.3, 0.12), F(490) + k * 0.25)
# 17.3-25.3 sweet guest music (pentatonic plucks + soft bass)
scale = [523, 587, 659, 784, 880, 1047]
mel = [0, 2, 3, 4, 3, 2, 1, 2, 3, 5, 4, 3, 2, 1, 0, 1]
for k in range(int((25.3 - 17.3) / 0.25)):
    at = 17.3 + k * 0.25
    if F(640) <= at < F(690):
        place(pluck(scale[mel[k % 16]] * 0.97, 0.3, 0.08), at)
        continue
    place(pluck(scale[mel[k % 16]], 0.32, 0.11), at, 1, 0.2)
    if k % 4 == 0:
        place(bass([65.4, 87.3, 98, 65.4][(k // 4) % 4], 0.9), at, 0.6)
    if k % 2 == 1:
        place(hat(), at, 0.4)
place(np.convolve(rng.normal(0, 1, int(SR * 0.8)), np.ones(40) / 40, 'same') * 0.4 * env(0.8, 0.05, 0.4), F(520))
bell(F(530), 0.12)
place(sweep(700, 400, 0.3, 0.12), F(600))
boing(F(620)); place(kick(1.2), F(624)); whoosh(F(624), 0.4, 0.6)
t = t_(1.7); place((np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 58 * t)) * env(1.7, 0.2, 1.0) * 0.18, F(640))
s_ = nz(0.8, 0.06); tt = t_(0.8)[:len(s_)]
place(s_ * np.sin(np.pi * tt / 0.8) * 0.25 + np.sin(2 * np.pi * np.cumsum(np.linspace(600, 1200, len(tt))) / SR) * 0.04, F(735))
# 25.3 bye bye, slam, chase
for k in range(4):
    place(pluck([784, 659, 784, 1047][k], 0.3, 0.12), F(762) + k * 0.2)
place(kick(1.5), F(800)); place(nz(0.25, 0.1) * np.exp(-t_(0.25)[:len(nz(0.25, 0.1))] * 12) * 0.8, F(800))
stab(F(806), 0.5)
b2 = 60 / 170
tb = F(820); i = 0
while tb < 30.0:
    place(kick(0.6), tb) if i % 2 == 0 else place(snare(), tb, 0.35)
    place(chip([196, 233, 262, 233][i % 4], b2 * 0.8, 0.07), tb, 1, 0.2)
    place(nz(0.04, 0.3) * 0.25, tb + b2 / 2)
    tb += b2 / 2 * 2; i += 1
for k in range(2):
    whoosh(F(820 + k * 40), 0.4, 0.6)
# 30-34 calm then doorbell + sad trombone
for k in range(10):
    place(pluck([392, 494, 587, 494, 440, 523, 659, 523, 494, 392][k], 0.45, 0.1), 30.0 + k * 0.27)
for k in range(8):
    place(sweep(900 + k * 80, 1400 + k * 80, 0.06, 0.05), 30.1 + k * 0.3, 1, 0.4)
bell(F(980)); harp_up(F(990), 0.08)
sad_trombone(F(1000))

mix = np.stack([L, R], 1)
mix = np.tanh(mix / np.abs(mix).max() * 1.3) / np.tanh(1.3) * 0.92
mix[-int(0.15 * SR):] *= np.linspace(1, 0, int(0.15 * SR))[:, None]
with wave.open('out/guests_audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('ok')
