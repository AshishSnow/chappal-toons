import numpy as np, wave
import importlib.util, sys
spec = importlib.util.spec_from_file_location("a6", "/home/claude/audio6.py")
# reuse synth helpers without running audio6's main mix: copy minimal helpers here instead
SR = 44100
DUR = 35.0
n = int(SR * DUR)
L = np.zeros(n); R = np.zeros(n)
rng = np.random.default_rng(151)
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



def rustle(at, d=0.25, g=0.3):
    s_ = nz(d, 0.35); place(s_ * np.sin(np.pi * t_(d)[:len(s_)] / d) * g, at, 1, rng.uniform(-0.5, 0.5))


def thud(at, g=0.8):
    place(kick(g), at); place(nz(0.08, 0.2) * 0.25, at)



def choir(at, d=2.0, g=0.07, base=(523, 659, 784, 1047)):
    t = t_(d); place(sum(np.sin(2 * np.pi * fq * t * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * t))) for fq in base) * env(d, 0.3, d * 0.6) * g, at)


def clank(at):
    for fq in (1800, 2400, 3100):
        place(np.sin(2 * np.pi * fq * t_(0.4)) * np.exp(-t_(0.4) * 9) * 0.08, at)
    place(kick(0.6), at)


def raindrops(at, d):
    for k in range(int(d * 12)):
        place(np.sin(2 * np.pi * rng.uniform(1500, 3000) * t_(0.03)) * np.exp(-t_(0.03) * 120) * 0.06, at + rng.uniform(0, d), 1, rng.uniform(-0.7, 0.7))
    s_ = nz(d, 0.5); place(s_ * 0.04, at)



def ring(at, d=1.2, g=0.18):
    t = t_(d)
    w = (np.sin(2 * np.pi * 2300 * t) + 0.6 * np.sin(2 * np.pi * 3100 * t)) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 22 * t)))
    place(w * g * np.minimum(1, (d - t) / 0.05), at)


def snore(at, g=0.25):
    s_ = nz(1.2, 0.03); tt = t_(1.2)[:len(s_)]
    place(s_ * np.sin(np.pi * tt / 1.2) ** 2 * g + np.sin(2 * np.pi * 65 * tt) * np.sin(np.pi * tt / 1.2) ** 2 * g * 0.3, at)


def slap(at):
    place(rng.normal(0, 1, int(SR * 0.06)) * np.exp(-t_(0.06) * 60) * 0.7, at); place(kick(0.7), at)



def pizz(fq, g=0.22):
    t = t_(0.18); return (np.sin(2 * np.pi * fq * t) + 0.4 * np.sin(4 * np.pi * fq * t)) * np.exp(-t * 22) * g


def click(at, g=0.4):
    place(np.sin(2 * np.pi * 3200 * t_(0.02)) * np.exp(-t_(0.02) * 300) * g, at)
    place(nz(0.03, 0.5) * 0.15, at + 0.03)


def whistle(at, notes, g=0.13):
    tt = at
    for fq, d in notes:
        t = t_(d); fr = fq * (1 + 0.012 * np.sin(2 * np.pi * 5.5 * t))
        place(np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(d, 0.04, d * 0.8) * g, tt)
        tt += d


def crunch(at, g=0.5):
    for k in range(5):
        place(nz(0.06, 0.6) * np.exp(-t_(0.06)[:int(SR * 0.06)] * 40) * g, at + k * 0.07 + rng.uniform(0, 0.02))


def buzz(at, d=0.5, g=0.22):
    t = t_(d); w = np.sign(np.sin(2 * np.pi * 150 * t)) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 9 * t)))
    place(np.convolve(w, np.ones(12) / 12, 'same') * g * np.minimum(1, (d - t) / 0.03), at, 1, -0.3)


def game_blips(t0, t1, g=0.06, base=523):
    seq = [0, 4, 7, 12, 7, 4, 9, 5]
    for k in range(int((t1 - t0) / 0.11)):
        place(chip(base * 2 ** (seq[k % 8] / 12), 0.08, g), t0 + k * 0.11, 1, 0.2)


def fake_snore(at, g=0.35):
    # exaggerated cartoon snore: honk in, whistle out
    t = t_(0.6); place(np.tanh(np.sin(2 * np.pi * np.cumsum(70 + 25 * np.sin(2 * np.pi * 30 * t)) / SR) * 3) * env(0.6, 0.08, 0.4) * g * 0.6, at)
    place(nz(0.6, 0.05) * np.sin(np.pi * t / 0.6) * g * 0.5, at)
    place(sweep(900, 1500, 0.4, g * 0.35), at + 0.65)


def footsteps(t0, n, dt=0.32, g=0.4):
    for k in range(n):
        place(tom(85, g), t0 + k * dt, 1, (-1) ** k * 0.2)


def mwah(at):
    place(sweep(500, 1100, 0.18, 0.2), at); place(nz(0.04, 0.6) * 0.2, at + 0.17)


# 1. hook (0-100): mom yells, 5 MINUTES sting
whistle(0.1, [(784, 0.15), (659, 0.15), (523, 0.3)], 0.08)
for k in range(5):
    place(sweep(420, 300, 0.12, 0.12), F(6) + k * 0.16, 1, -0.4)   # mom yapping
stab(F(50), 0.65); place(sweep(500, 1500, 0.3, 0.15), F(52))
for k in range(6):
    place(tick(0.2), F(56) + k * 0.25)
# 2. idea (100-220): ding, whip pan, angelic closet
place(sweep(300, 500, 0.6, 0.06), F(104))
bell(F(126), 0.3)
whoosh(F(154), 0.35, 0.7)
choir(F(164), 1.8, 0.07); harp_up(F(164), 0.08)
# 3. speed cleaning (220-400): fast groove + whoosh per item
groove(F(220), F(390), 160, [110, 110, 131, 147], [(440, 554, 659), (392, 494, 587)], g=0.5)
for i in range(16):
    whoosh(F(236 + i * 8), 0.2, 0.45)
    place(pizz(880 * 2 ** ((i % 8) / 12), 0.12), F(236 + i * 8 + 14))
harp_up(F(370), 0.1); bell(F(370), 0.2)
# 4. closet won't close (400-540)
for k in range(5):
    creak(F(404) + k * 0.42, 0.2); place(sweep(200, 140, 0.25, 0.12), F(410) + k * 0.42)  # grunts
whoosh(F(470), 0.6, 0.6); place(sweep(400, 1200, 0.5, 0.14), F(472))
slap(F(492)); thud(F(492), 1.0); click(F(494), 0.6)
boing(F(500), 0.2)
whistle(F(506), [(784, 0.18), (988, 0.18), (1175, 0.4)], 0.1)
# 5. mom inspection (540-720)
footsteps(F(542), 4, 0.25, 0.35)
harp_up(F(572), 0.08)
for j, fq in enumerate((784, 659, 523, 659, 587, 523)):
    place(mbox(fq, 0.9, 0.1), F(574) + j * 0.3)
place(sweep(900, 300, 0.4, 0.12), F(640))   # gulp
footsteps(F(636), 5, 0.3, 0.3)
stab(F(672), 0.6); place(sweep(1400, 400, 0.5, 0.14), F(674))
# 6. avalanche (720-880)
creak(F(726), 0.28); creak(F(736), 0.2)
stab(F(744), 0.9)
for k in range(30):
    place(tom(rng.uniform(70, 160), 0.5), F(744) + k * 0.05 + rng.uniform(0, 0.03), 1, rng.uniform(-0.7, 0.7))
    rustle(F(744) + k * 0.05, 0.15, 0.3)
crunch(F(760), 0.4); thud(F(780), 0.8)
boing(F(800), 0.2); boing(F(820), 0.18)
place(brass(98, 0.9, 0.18), F(834))
sad_trombone(F(840))
# 7. plan B (880-1050)
for k in range(18):
    whoosh(F(884) + k * 0.12, 0.1, 0.25); place(pizz(660 + 40 * (k % 5), 0.1), F(886) + k * 0.12)
for k in range(12):
    place(sweep(200 + k * 60, 260 + k * 60, 0.15, 0.1), F(950) + k * 0.15)   # rising
stab(F(1010), 0.8); thud(F(1010), 1.0); clank(F(1011))
for k in range(4):
    place(chip(1568 - k * 120, 0.12, 0.05), F(1016) + k * 0.13)   # dizzy tweets
groove(F(1020), 35.0, 120, [73.4, 73.4, 98, 87.3], [(294, 370, 440), (392, 494, 587)], g=0.45)

mix = np.stack([L, R], 1)
mix = np.tanh(mix / np.abs(mix).max() * 1.3) / np.tanh(1.3) * 0.92
mix[-int(0.15 * SR):] *= np.linspace(1, 0, int(0.15 * SR))[:, None]
with wave.open('out/closet_audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('ok')
