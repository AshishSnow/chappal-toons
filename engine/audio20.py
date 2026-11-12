"""Audio for scenes20 (We Have Food At Home)."""
import numpy as np, wave
import importlib.util, sys
spec = importlib.util.spec_from_file_location("a6", "/home/claude/audio6.py")
# reuse synth helpers without running audio6's main mix: copy minimal helpers here instead
SR = 44100
DUR = 22.0
n = int(SR * DUR)
L = np.zeros(n); R = np.zeros(n)
rng = np.random.default_rng(201)
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



def crack(at):
    for k in range(3):
        place(np.sin(2 * np.pi * rng.uniform(2500, 3500) * t_(0.015)) * np.exp(-t_(0.015) * 300) * 0.3 + nz(0.015, 0.8)[:int(SR*0.015)] * 0.2, at + k * 0.03)


def fanfare(at, g=0.14):
    for fq, dt, d in ((392, 0, 0.15), (523, 0.15, 0.15), (659, 0.3, 0.15), (784, 0.45, 0.6)):
        place(brass(fq / 2, d, g), at + dt)


def power_down(at):
    place(sweep(900, 60, 0.9, 0.25), at)


def power_up(at):
    place(sweep(120, 1400, 0.6, 0.18), at)

def burp(at, g=0.4):
    t = t_(0.5); fr = 90 + 30 * np.sin(2 * np.pi * 7 * t)
    place(np.tanh(np.sin(2 * np.pi * np.cumsum(fr) / SR) * 4) * env(0.5, 0.02, 0.3) * g, at)


def plop(at, g=0.4):
    place(sweep(700, 200, 0.12, g), at); place(kick(0.4), at)



def engine_hum(t0, t1, g=0.06, f0=46):
    d = t1 - t0; t = t_(d)
    fr = f0 * (1 + 0.04 * np.sin(2 * np.pi * 0.7 * t))
    w = 2 * (np.cumsum(fr) / SR % 1) - 1
    w = np.convolve(w, np.ones(30) / 30, 'same')
    e = np.minimum(1, t / 0.4) * np.minimum(1, (d - t) / 0.4)
    place(w * e * g, t0); place(nz(d, 0.02) * e * g * 0.3, t0)


def ask(at, g=0.12, up=True):
    # rising three-note "are-we-there-yet?" chirp
    for k, fq in enumerate((523, 587, 784) if up else (784, 659, 523)):
        place(chip(fq, 0.11, g), at + k * 0.12); place(pluck(fq, 0.2, g), at + k * 0.12)
    place(sweep(784, 1050, 0.18, g * 1.3), at + 0.36)


def honk(at, d=0.9, g=0.25):
    t = t_(d); w = np.sign(np.sin(2 * np.pi * 392 * t)) + np.sign(np.sin(2 * np.pi * 494 * t))
    w = np.convolve(w, np.ones(8) / 8, 'same')
    place(w * g * np.minimum(1, t / 0.01) * np.minimum(1, (d - t) / 0.05), at)


def screech(at, d=0.9, g=0.12):
    t = t_(d); fr = 2600 - 900 * t / d
    place((np.sin(2 * np.pi * np.cumsum(fr) / SR) * 0.6 + nz(d, 0.7)[:len(t)] * 0.4) * env(d, 0.02, d * 0.6) * g, at)


def zipper(at, g=0.3):
    for k in range(14):
        place(np.sin(2 * np.pi * (1500 + k * 120) * t_(0.012)) * np.exp(-t_(0.012) * 300) * g, at + k * 0.022)


def kazoo(at, notes, g=0.12):
    tt = at
    for fq, d in notes:
        t = t_(d); w = np.sign(np.sin(2 * np.pi * fq * t * (1 + 0.01 * np.sin(2 * np.pi * 6 * t))))
        w = np.convolve(w, np.ones(6) / 6, 'same')
        place(w * env(d, 0.02, d * 0.8) * g, tt); tt += d


def gasp(at, d=1.4, g=0.3):
    t = t_(d); s_ = nz(d, 0.25)[:len(t)]
    place(s_ * (t / d) ** 1.5 * g + sweep(200, 700, d, 0.08), at)


def alarm_beep(at, k=3, g=0.16):
    for j in range(k):
        beep(at + j * 0.18, 1800, g); beep(at + j * 0.18 + 0.08, 1400, g * 0.8)


# 1. hook (0-100): begging -> "we have food at home"
groove(F(0), F(46), 120, [131, 131, 147, 165], [(523, 659, 784), (587, 740, 880)], g=0.3)
for at in (0, 14, 28):
    place(sweep(500, 1100, 0.25, 0.12), F(at))          # puppy whine
whoosh(F(46), 0.3, 0.6); stab(F(54), 0.7); thud(F(54), 0.6)
place(sweep(400, 150, 0.5, 0.12), F(62)); stab(F(60), 0.4)
# 2. fridge (100-250)
creak(F(110), 0.2); fanfare(F(114), 0.12); harp_up(F(114), 0.1); choir(F(114), 1.4, 0.06)
whoosh(F(150), 0.3, 0.5)
for at, fq in ((156, 523), (176, 494), (198, 466)):
    place(pizz(fq, 0.3), F(at)); tick()
sad_trombone(F(198))
for k in range(5):
    cricket(F(222) + k * 0.2, 0.06)
whistle(F(226), [(330, 0.5), (294, 0.5), (262, 0.8)], 0.07)
# 3. cooking (250-400)
groove(F(250), F(294), 140, [110, 147, 110, 165], [(440, 554, 659)], g=0.3)
for at in (254, 264, 274, 284):
    whoosh(F(at), 0.18, 0.35); plop(F(at + 12), 0.35)
sizzle(F(270), 1.2, 0.1)
place(nz(0.6, 0.08) * np.exp(-t_(0.6)[:int(SR * 0.6)] * 5) * 0.8, F(294)); thud(F(294), 0.8)  # POOF
click(F(328), 0.4)
burp(F(346), 0.5); boing(F(346), 0.2)
place(sweep(500, 120, 0.6, 0.1), F(356))
place(chip(1200, 0.06, 0.08), F(374)); place(chip(1200, 0.06, 0.08), F(380))  # blink blink
# 4. dad + pizza (400-530)
bell(F(400), 0.35)
creak(F(406), 0.2); choir(F(410), 1.5, 0.08); harp_up(F(410), 0.1)
footsteps(F(410), 4, 0.15, 0.3)
fanfare(F(420), 0.1)
whoosh(F(446), 0.35, 0.7); stab(F(456), 0.6); crunch(F(462), 0.4)
whoosh(F(484), 0.25, 0.5); stab(F(484), 0.5)
kazoo(F(494), [(392, 0.25), (440, 0.25), (523, 0.5)], 0.1)
# 5. twist + loop (530-660)
whoosh(F(530), 0.3, 0.4)
crunch(F(536), 0.35)
place(sweep(300, 220, 0.5, 0.15), F(544)); stab(F(544), 0.4)
place(mbox(523, 0.8, 0.12), F(548)); place(mbox(659, 0.8, 0.12), F(554)); place(mbox(784, 1.2, 0.12), F(560))
sad_trombone(F(598))
burp(F(610), 0.5)
groove(F(630), F(660), 120, [131, 131, 147, 165], [(523, 659, 784)], g=0.3)
place(sweep(500, 1100, 0.25, 0.12), F(630))

mix = np.stack([L, R], 1)
mix = np.tanh(mix / np.abs(mix).max() * 1.3) / np.tanh(1.3) * 0.92
mix[-int(0.1 * SR):] *= np.linspace(1, 0, int(0.1 * SR))[:, None]
with wave.open('out/food_audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('ok')
