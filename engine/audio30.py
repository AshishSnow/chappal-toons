"""Audio for scenes30 (Dad's Home Haircut)."""
import numpy as np, wave
import importlib.util, sys
spec = importlib.util.spec_from_file_location("a6", "/home/claude/audio6.py")
# reuse synth helpers without running audio6's main mix: copy minimal helpers here instead
SR = 44100
DUR = 22.0
n = int(SR * DUR)
L = np.zeros(n); R = np.zeros(n)
rng = np.random.default_rng(301)
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


def sniff(at, g=0.25):
    for k in range(2):
        s_ = nz(0.09, 0.4); place(s_ * np.sin(np.pi * t_(0.09)[:len(s_)] / 0.09) * g, at + k * 0.13, 1, 0.3)


def slurp(at, g=0.2):
    place(sweep(300, 900, 0.18, g), at); rustle(at, 0.15, 0.15)


def panic_hit(at):
    stab(at, 0.7); alarm_beep(at + 0.05, 3, 0.12); whoosh(at, 0.25, 0.4)



def doorbell(at, g=0.3):
    for fq, dt in ((784, 0), (622, 0.42)):
        t = t_(1.0)
        place((np.sin(2 * np.pi * fq * t) + 0.4 * np.sin(2 * np.pi * fq * 2.0 * t)) * np.exp(-t * 3) * g, at + dt)


def door_slam(at):
    place(kick(1.1), at); place(nz(0.12, 0.3) * np.exp(-t_(0.12)[:int(SR * 0.12)] * 30) * 0.5, at)


def scooter_buzz(t0, d, g=0.12):
    t = t_(d); fr = 110 + 60 * t / d
    w = np.tanh(np.sin(2 * np.pi * np.cumsum(fr) / SR) * 4) * np.minimum(1, t / 0.05) * np.maximum(0, 1 - t / d)
    place(w * g, t0, 1, 0.5)


def tictoc(t0, t1, dt=0.1, g=0.25):
    k = 0
    while t0 + k * dt < t1:
        place(tick(g) if k % 2 else np.sin(2 * np.pi * 1500 * t_(0.04)) * np.exp(-t_(0.04) * 120) * g, t0 + k * dt); k += 1



def stretch(at, g=0.12):
    place(sweep(180, 420, 0.25, g), at, 1, rng.uniform(-0.4, 0.4))


def mine(at, hi=False):
    # cartoon "MINE!" squawk
    kazoo(at, [(523 if hi else 392, 0.12), (659 if hi else 494, 0.22)], 0.13); stab(at, 0.4)


def flip(at, k):
    click(at, 0.35)
    notes = (523, 659, 784, 440, 587, 880, 698)
    place(chip(notes[k % len(notes)], 0.12, 0.07), at + 0.02); place(pluck(notes[k % len(notes)], 0.2, 0.12), at + 0.02)

def ding(at, g=0.3):
    for fq in (1568, 2093, 2637):
        place(np.sin(2 * np.pi * fq * t_(1.2)) * np.exp(-t_(1.2) * 3) * g / 3, at)


def scribble(t0, t1, g=0.18):
    k = 0
    while t0 + k * 0.07 < t1:
        rustle(t0 + k * 0.07, 0.06, g); k += 1



def munch(t0, t1, g=0.3):
    k = 0
    while t0 + k * 0.16 < t1:
        crunch(t0 + k * 0.16, g * 0.5); place(tom(140, g * 0.4), t0 + k * 0.16); k += 1


def ringtone(at, k=2, g=0.12):
    for j in range(k):
        for i, fq in enumerate((784, 988, 1175, 988)):
            place(chip(fq, 0.1, g), at + j * 0.5 + i * 0.1)


def bloop(at, g=0.25):
    place(sweep(300, 900, 0.15, g), at)




def jingle(at, d=1.6, g=0.06):
    k = 0
    while k * 0.09 < d:
        for fq in (3200, 4100):
            place(np.sin(2 * np.pi * (fq + rng.uniform(-200, 200)) * t_(0.05)) * np.exp(-t_(0.05) * 80) * g, at + k * 0.09 + rng.uniform(0, 0.02), 1, 0.4)
        k += 1


def fan_whirr(t0, d, g=0.05):
    t = t_(d); place(nz(d, 0.05)[:len(t)] * (0.6 + 0.4 * np.sin(2 * np.pi * 4 * t)) * g, t0)


def clipper_buzz(at, d, g=0.12):
    t = t_(d); w = np.sign(np.sin(2 * np.pi * 120 * t)) * 0.6 + np.sin(2 * np.pi * 240 * t) * 0.4
    w *= (0.85 + 0.15 * np.sin(2 * np.pi * 23 * t))
    place(np.convolve(w, np.ones(6) / 6, 'same') * g * np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.05), at)


def snip_flurry(t0, t1, g=0.12):
    k = 0
    while t0 + k * 0.11 < t1:
        rustle(t0 + k * 0.11, 0.05, g); k += 1


def shatter(at, g=0.4):
    for k in range(10):
        fq = rng.uniform(2500, 6000)
        place(np.sin(2 * np.pi * fq * t_(0.3)) * np.exp(-t_(0.3) * rng.uniform(10, 25)) * g / 4, at + rng.uniform(0, 0.15), 1, rng.uniform(-0.5, 0.5))
    place(nz(0.3, 0.5) * np.exp(-t_(0.3)[:len(nz(0.3, 0.5))] * 12) * g * 0.6, at)


# 1. hook: mirror ECU scream + 5 minutes earlier (0-110)
stab(F(0), 0.7); gasp(F(0), 0.6, 0.25)
for k in range(3):
    place(sweep(500 - 40 * k, 300, 0.22, 0.12), F(2) + k * 0.3)    # "what did you do"
whoosh(F(54), 0.3, 0.45); place(sweep(1200, 300, 0.5, 0.08), F(56))   # rewind
groove(F(60), F(230), 120, [131, 165, 147, 110], [(523, 659, 784)], g=0.12)
clipper_buzz(F(66), 0.5, 0.08); fanfare(F(70), 0.08)
# 2. first trim (110-230)
whoosh(F(110), 0.25, 0.4)
clipper_buzz(F(118), 1.6, 0.16); snip_flurry(F(124), F(165), 0.12)
stab(F(124), 0.5)
whoosh(F(172), 0.25, 0.4); stab(F(174), 0.6); place(sweep(600, 200, 0.6, 0.1), F(176))   # oops slide
cricket(F(190), 0.06)
ding(F(202), 0.15); clipper_buzz(F(206), 0.4, 0.1)
# 3. even it out montage (230-370)
whoosh(F(230), 0.3, 0.45)
groove(F(230), F(322), 150, [196, 220, 247, 262], [(784, 988, 1175)], hype=True, g=0.13)
clipper_buzz(F(232), 3.0, 0.15); snip_flurry(F(232), F(322), 0.14)
for k in range(6):
    whoosh(F(236 + k * 14), 0.15, 0.22)
stab(F(260), 0.5); boing(F(260), 0.15); stab(F(292), 0.5); boing(F(292), 0.15)
whoosh(F(322), 0.3, 0.4)
cricket(F(326), 0.06); place(sweep(900, 700, 1.2, 0.04), F(334))   # lone hair drifting
ding(F(346), 0.25); fanfare(F(348), 0.08)
# 4. Mom + he moved (370-500)
whoosh(F(370), 0.25, 0.45); gasp(F(372), 0.6, 0.3); stab(F(374), 0.7)
whoosh(F(392), 0.2, 0.25); shatter(F(406), 0.5); thud(F(406), 0.4)
whoosh(F(432), 0.3, 0.45); stab(F(438), 0.5)
kazoo(F(440), [(330, 0.15), (262, 0.35)], 0.1)
place(sweep(300, 220, 0.4, 0.05), F(472)); cricket(F(478), 0.05)
# 5. payback + loop (500-660)
whoosh(F(500), 0.3, 0.4)
for k in range(5):
    place(pizz([392, 330, 392, 330, 294][k], 0.18), F(504) + k * 0.24)
snore(F(506), 0.2); snore(F(530), 0.2)
clipper_buzz(F(546), 0.8, 0.16); stab(F(552), 0.6)
whoosh(F(570), 0.3, 0.45); stab(F(570), 0.8); gasp(F(570), 0.6, 0.3)
for k in range(3):
    place(sweep(420 - 30 * k, 250, 0.22, 0.12), F(572) + k * 0.3)
whistle(F(594), [(988, 0.15), (1319, 0.3)], 0.08)
whoosh(F(618), 0.2, 0.4)
stab(F(620), 0.7); gasp(F(620), 0.6, 0.25)
for k in range(3):
    place(sweep(500 - 40 * k, 300, 0.22, 0.12), F(622) + k * 0.3)

mix = np.stack([L, R], 1)
mix = np.tanh(mix / np.abs(mix).max() * 1.3) / np.tanh(1.3) * 0.92
mix[-int(0.1 * SR):] *= np.linspace(1, 0, int(0.1 * SR))[:, None]
with wave.open('out/haircut_audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('ok')
