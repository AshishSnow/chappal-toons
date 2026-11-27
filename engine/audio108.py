"""Audio for scenes108 (Dad vs the frozen car)."""
import numpy as np, wave
import importlib.util, sys
spec = importlib.util.spec_from_file_location("a6", "/home/claude/audio6.py")
# reuse synth helpers without running audio6's main mix: copy minimal helpers here instead
SR = 44100
DUR = 22.0
n = int(SR * DUR)
L = np.zeros(n); R = np.zeros(n)
rng = np.random.default_rng(999)
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


def chomp(at, g=0.4):
    crunch(at, g * 0.6); place(tom(120, g * 0.5), at)


def growl(at, d=0.9, g=0.3):
    t = t_(d); fr = 55 + 20 * np.sin(2 * np.pi * 3 * t)
    place(np.tanh(np.sin(2 * np.pi * np.cumsum(fr) / SR) * 5) * np.sin(np.pi * t / d) * g + nz(d, 0.05)[:len(t)] * np.sin(np.pi * t / d) * g * 0.4, at)



def lullaby(t0, t1, g=0.05):
    notes = (659, 587, 523, 587, 659, 659, 659, 0, 587, 587, 587, 0, 659, 784, 784)
    k = 0
    while t0 + k * 0.32 < t1:
        fq = notes[k % len(notes)]
        if fq:
            place(mbox(fq, 0.9, g), t0 + k * 0.32, 1, 0.2)
        k += 1


def yawn_snd(at, d=1.6, g=0.22):
    t = t_(d); fr = 180 + 260 * np.sin(np.pi * t / d) - 120 * t / d
    w = np.tanh(np.sin(2 * np.pi * np.cumsum(fr) / SR) * 2) * np.sin(np.pi * t / d) ** 0.7
    place(w * g + nz(d, 0.2)[:len(t)] * np.sin(np.pi * t / d) * g * 0.4, at)




def sneak(t0, t1, g=0.12):
    notes = (147, 0, 175, 0, 196, 0, 175, 0, 147, 0, 220, 208, 196, 0, 175, 0)
    k = 0
    while t0 + k * 0.18 < t1:
        fq = notes[k % len(notes)]
        if fq:
            place(pizz(fq, g), t0 + k * 0.18, 1, -0.2 + 0.4 * (k % 2))
        k += 1


def spooky(at, g=0.1):
    place(sweep(220, 330, 0.6, g), at); place(sweep(233, 349, 0.6, g * 0.7), at, 1, 0.3)


def rattle(at, d=1.2, g=0.25):
    k = 0
    while k * 0.07 < d:
        place(tom(300 + 60 * (k % 3), g * 0.35), at + k * 0.07, 1, (-0.3 if k % 2 else 0.3)); rustle(at + k * 0.07, 0.04, g * 0.4); k += 1


def vroom(at, d=0.8, g=0.2):
    t = t_(d); fr = 70 + 90 * np.sin(np.pi * t / d) + 15 * np.sin(2 * np.pi * 18 * t)
    place(np.tanh(np.sin(2 * np.pi * np.cumsum(fr) / SR) * 4) * env(d, 0.03, d * 0.7) * g, at)


def robot_talk(at, n=6, g=0.07):
    for k in range(n):
        place(chip(rng.choice((660, 880, 990, 1320)), 0.06, g), at + k * 0.07)


def party_bgm(t0, t1, g=0.35):
    groove(t0, t1, 120, [131, 131, 165, 196], [(262, 330, 392), (220, 277, 330)], g=g)


def bark(at, g=0.3, hi=False):
    d = 0.14; t = t_(d); fr = (520 if hi else 380) * (1 - 0.35 * t / d)
    place(np.tanh(np.sin(2 * np.pi * np.cumsum(fr) / SR) * 3) * env(d, 0.005, 0.07) * g + nz(d, 0.4)[:len(t)] * env(d, 0.003, 0.03) * g * 0.4, at)


def splashsnd(at, g=0.5):
    s_ = nz(0.7, 0.4); tt = t_(0.7)[:len(s_)]; place(s_ * np.exp(-tt * 5) * g, at)
    for k in range(6):
        place(sweep(rng.uniform(600, 1200), rng.uniform(1500, 2500), 0.08, 0.12), at + 0.05 + k * 0.06)


def walk_bgm(t0, t1, g=0.3):
    groove(t0, t1, 128, [147, 147, 196, 220], [(294, 370, 440), (262, 330, 392)], g=g)



def sigh(at, g=0.25, d=0.9):
    s_ = nz(d, 0.25); tt = t_(d)[:len(s_)]
    place(s_ * np.sin(np.pi * tt / d) ** 2 * g, at); place(sweep(260, 150, d, 0.05), at)


def scrub(t0, t1, g=0.18):
    t = t0
    while t < t1:
        s_ = nz(0.07, 0.5); place(s_ * env(0.07, 0.003, 0.03)[:len(s_)] * g, t, 1, rng.uniform(-0.5, 0.5)); t += 0.075


def busy_bgm(t0, t1, g=0.25):
    groove(t0, t1, 170, [196, 196, 247, 294], [(392, 494, 587), (440, 554, 659)], g=g)



def cough(at, g=0.35):
    for k in range(2):
        s_ = nz(0.16, 0.3); tt = t_(0.16)[:len(s_)]
        place(s_ * np.exp(-tt * 18) * g + np.sin(2 * np.pi * 140 * tt) * np.exp(-tt * 25) * g * 0.5, at + k * 0.2, 1, 0.1)


def sick_bgm(t0, t1, g=0.05):
    notes = (392, 0, 370, 0, 349, 0, 330, 0)
    k = 0
    while t0 + k * 0.25 < t1:
        fq = notes[k % len(notes)]
        if fq:
            place(mbox(fq, 0.6, g), t0 + k * 0.25, 1, 0.2)
        k += 1


def tap_water(at, d, g=0.12):
    x = nz(d, 0.6); tt = t_(d)[:len(x)]
    place(x * np.minimum(1, tt / 0.08) * np.minimum(1, (d - tt) / 0.1) * g, at, 1, -0.2)


def breath(at, d=1.1, g=0.3):
    s_ = nz(d, 0.18); tt = t_(d)[:len(s_)]
    place(s_ * np.minimum(1, tt / 0.15) * np.exp(-np.maximum(0, tt - d * 0.6) * 6) * g, at)
    place(brass(55, d, 0.12), at + 0.1)


def innocent(t0, t1, g=0.08):
    notes = (784, 988, 1175, 988, 784, 988, 1319, 1175)
    k = 0
    while t0 + k * 0.2 < t1:
        place(mbox(notes[k % len(notes)], 0.5, g), t0 + k * 0.2, 1, 0.2 * (1 if k % 2 else -1)); k += 1



def doom(at, g=0.5):
    # heavy "count" hit: low brass + kick + low tom
    place(brass(55, 0.7, g) + brass(82.4, 0.7, g * 0.5), at); place(kick(1.2), at); place(tom(70, 0.6), at + 0.02)


def tension(t0, t1, g=0.05):
    b_ = 0.25; k = 0
    while t0 + k * b_ < t1:
        place(pluck(220 * (1 + 0.06 * (k % 4)), 0.2, g), t0 + k * b_, 1, 0.3 if k % 2 else -0.3); k += 1



def shutter(at, g=0.4):
    click(at, g); place(nz(0.05, 0.6) * np.exp(-t_(0.05)[:int(SR * 0.05)] * 60) * g * 0.6, at + 0.05); click(at + 0.09, g * 0.7)
    place(sweep(2500, 800, 0.25, 0.08), at + 0.02)


def sneeze(at, g=0.35):
    place(sweep(300, 900, 0.35, g * 0.4), at); s_ = nz(0.3, 0.6); tt = t_(0.3)[:len(s_)]
    place(s_ * np.exp(-tt * 10) * g, at + 0.35); place(kick(0.5), at + 0.35)


def fail_stamp(at):
    thud(at, 0.9); buzz(at + 0.02, 0.35, 0.14)


def chatter(t0, t1, g=0.12):
    t = t0
    while t < t1:
        click(t, g); t += 0.055


def wind(t0, t1, g=0.06):
    d = t1 - t0; x = nz(d, 0.02); tt = t_(d)[:len(x)]
    place(x * (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * tt)) * np.minimum(1, tt / 0.4) * np.minimum(1, (d - tt) / 0.4) * g, t0)


def sonar(at, g=0.18):
    tt = t_(0.7); place(np.sin(2 * np.pi * 1320 * tt) * np.exp(-tt * 6) * g, at)


def squawk(at, g=0.12):
    kazoo(at, [(880, 0.07), (740, 0.09)], g)


def why_pop(at, g=0.14, hi=0):
    # bright rising "why?" chirp + bubble pop
    place(sweep(500 + hi * 80, 1100 + hi * 120, 0.16, g), at); place(chip(880 + hi * 110, 0.06, g * 0.5), at + 0.12)
    place(sweep(900, 300, 0.05, g * 0.8), at)


def chalk_scratch(t0, t1, g=0.1):
    t = t0
    while t < t1:
        s_ = nz(0.06, 0.8); place(s_ * env(0.06, 0.004, 0.03)[:len(s_)] * g, t, 1, 0.3); t += 0.09


def moo(at, d=1.2, g=0.3):
    t = t_(d); fr = 150 - 30 * t / d + 8 * np.sin(2 * np.pi * 5 * t)
    w = sum(np.sin(2 * np.pi * np.cumsum(fr * h) / SR) / h for h in range(1, 6))
    place(np.tanh(w * 1.5) * env(d, 0.08, d * 0.7) * g, at)


def cluck(at, n=3, g=0.15):
    for k in range(n):
        place(sweep(900, 600, 0.07, g), at + k * 0.12); place(chip(700, 0.04, g * 0.5), at + k * 0.12)


def bumps(t0, t1, dt=0.19, g=0.5):
    t = t0
    while t < t1:
        place(kick(g), t); place(sweep(300, 120, 0.08, 0.15), t); t += dt


def splat(at, g=0.5):
    place(nz(0.25, 0.3) * env(0.25, 0.003, 0.06) * g, at); place(sweep(220, 70, 0.2, 0.3), at)


def lick(at, n=4, g=0.12):
    for k in range(n):
        place(sweep(400, 900, 0.09, g), at + k * 0.16, 1, 0.2)


def blackout(at):
    click(at, 0.5); place(sweep(400, 60, 0.4, 0.2), at)

def scream(at, d=1.3, g=0.2, f0=520):
    t = t_(d); fr = f0 + 140 * np.exp(-t * 3) - 80 * t / d + 22 * np.sin(2 * np.pi * 7 * t)
    ph = np.cumsum(fr) / SR
    w = sum(np.sin(2 * np.pi * ph * h) * (1.0 if h in (2, 3) else 0.5) / h for h in range(1, 9))
    place(np.tanh(w * 2.2) * env(d, 0.02, d * 0.7) * g + nz(d, 0.3)[:len(t)] * env(d, 0.01, d * 0.4) * g * 0.25, at)


def pain_hit(at):
    crunch(at, 0.6); stab(at, 0.5); place(sweep(2400, 900, 0.3, 0.12), at); scream(at + 0.05)


def tweets(at, d=1.0, g=0.06):
    k = 0
    while k * 0.12 < d:
        place(chip(1568 if k % 2 else 1976, 0.08, g), at + k * 0.12, 1, 0.4 if k % 2 else -0.4); k += 1


def heartbeat(t0, t1, dt=0.6, g=0.6):
    t = t0
    while t < t1:
        place(tom(60, g), t); place(tom(55, g * 0.7), t + 0.18); t += dt


def hee(at, g=0.1):
    # kid giggle: two quick high bouncy chirps
    for k in range(2):
        place(sweep(1100, 1500, 0.07, g), at + k * 0.13); place(chip(1318, 0.05, g * 0.4), at + k * 0.13 + 0.03)


def squish(at, g=0.5):
    place(sweep(500, 90, 0.35, 0.3), at); place(nz(0.3, 0.2) * env(0.3, 0.005, 0.1) * g * 0.6, at); place(kick(0.9), at)


def count_blip(at, k):
    place(chip(523 * (1.26 ** k), 0.12, 0.1), at)


def clang(at, g=0.35):
    tt = t_(1.2)
    x = sum(np.sin(2 * np.pi * fq * tt) for fq in (420, 1130, 1870, 2690)) * np.exp(-tt * 4)
    place(x * g * 0.3, at); place(nz(0.08, 0.9) * g, at)


def snap(at):
    stab(at, 0.5); place(kick(1.2), at); bloop(at, 0.3); scream(at + 0.05, 0.9, 0.15, 640)


def wood_bonk(at, g=0.6):
    place(tom(160, g), at); place(nz(0.05, 0.4) * env(0.05, 0.002, 0.02)[:int(SR * 0.05)] * g * 0.5, at)


def squeak(at, g=0.14):
    t = t_(0.14); fr = 1500 + 900 * np.sin(np.pi * t / 0.14)
    place(np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * t / 0.14) * g, at, 1, rng.uniform(-0.4, 0.4))


def grunt(at, d=1.0, g=0.18, f0=110):
    t = t_(d); fr = f0 + 15 * np.sin(2 * np.pi * 7 * t) + 30 * t / d
    w = sum(np.sin(2 * np.pi * np.cumsum(fr * h) / SR) / h for h in range(1, 8))
    place(np.tanh(w * 2) * env(d, 0.05) * np.minimum(1, (d - t) / 0.08) * g + nz(d, 0.3)[:len(t)] * 0.03, at)


def cork_pop(at, g=0.6):
    t = t_(0.12); place(np.sin(2 * np.pi * np.cumsum(900 - 600 * t / 0.12) / SR) * np.exp(-t * 40) * g, at)
    place(nz(0.06, 0.5) * 0.3, at)


def spin_whirr(t0, t1, g=0.12):
    d = t1 - t0; t = t_(d); fr = 4 + 18 * (t / d)
    s_ = nz(d, 0.2)[:len(t)] * (0.5 + 0.5 * np.sin(2 * np.pi * np.cumsum(fr) / SR))
    place(s_ * g * np.minimum(1, t / 0.2) * np.minimum(1, (d - t) / 0.2), t0)


def bubbles_snd(t0, t1, g=0.08):
    t = t0
    while t < t1:
        fq = rng.uniform(500, 1200); d = 0.07
        tt = t_(d); place(np.sin(2 * np.pi * np.cumsum(fq + 3000 * tt) / SR) * np.exp(-tt * 40) * g, t, pan=rng.uniform(-0.6, 0.6))
        t += rng.uniform(0.06, 0.18)


def drain(t0, t1, g=0.18):
    d = t1 - t0; t = t_(d)
    fr = 140 + 60 * np.sin(2 * np.pi * 7 * t)
    place(np.sin(2 * np.pi * np.cumsum(fr) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * 4 * t)) * g * np.minimum(1, (d - t) / 0.2), t0)
    k = t0
    while k < t1:
        plop(k, 0.25); k += 0.28


def rubber_squeak(at, g=0.12):
    t = t_(0.18); fr = 1300 + 500 * np.sin(2 * np.pi * 9 * t)
    place(np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(0.18, 0.01, 0.08) * g, at)


def tape_rip(at, g=0.3):
    d = 0.35; t = t_(d); x = nz(d, 0.6)[:len(t)] * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 38 * t)))
    place(x * env(d, 0.01, 0.2) * g, at, 1, rng.uniform(-0.4, 0.4))


def fizz(t0, t1, g=0.15):
    d = t1 - t0; t = t_(d)
    place(np.diff(rng.normal(0, 1, len(t)), prepend=0) * np.minimum(1, t / 0.15) * np.minimum(1, (d - t) / 0.4) * g, t0)


def glug(t0, n, g=0.25):
    for k in range(n):
        tt = t_(0.12); place(np.sin(2 * np.pi * np.cumsum(220 + 400 * tt) / SR) * np.exp(-tt * 25) * g, t0 + k * 0.14)


def bike_tick(t0, t1, g=0.05):
    k = t0
    while k < t1:
        click(k, g); k += 0.11


def bike_bell(at, g=0.18):
    for d in (0, 0.14):
        t = t_(0.5); place((np.sin(2 * np.pi * 2350 * t) + 0.5 * np.sin(2 * np.pi * 3610 * t)) * np.exp(-t * 9) * g, at + d)


def leaves_crash(at, g=0.6):
    thud(at, 0.9); crunch(at, g); rustle(at, 0.6, 0.5); rustle(at + 0.25, 0.4, 0.35)
    for k in range(5):
        place(nz(0.05, 0.6) * env(0.05, 0.002, 0.02)[:int(SR * 0.05)] * 0.3, at + 0.05 + k * 0.06, pan=rng.uniform(-0.6, 0.6))


def kettle(t0, d, g=0.12):
    t = t_(d); fr = 1900 + 500 * np.minimum(1, t / 0.4) + 40 * np.sin(2 * np.pi * 6 * t)
    s_ = np.sin(2 * np.pi * np.cumsum(fr) / SR) + 0.3 * nz(d, 0.9)[:len(t)]
    place(s_ * np.minimum(1, t / 0.15) * np.minimum(1, (d - t) / 0.1) * g, t0)


def groan(at, d=1.2, g=0.2):
    t = t_(d); fr = 150 - 50 * t / d + 8 * np.sin(2 * np.pi * 5 * t)
    place(np.tanh(2 * np.sin(2 * np.pi * np.cumsum(fr) / SR)) * env(d, 0.1, d * 0.6) * g, at)

def mbuzz(t0, d, g=0.06, f0=620, pan_sp=1.3):
    """mosquito whine: thin buzzy tone with wobble, panning around"""
    t = t_(d); fr = f0 * (1 + 0.05 * np.sin(2 * np.pi * 7 * t) + 0.03 * np.sin(2 * np.pi * 1.7 * t))
    ph = 2 * np.pi * np.cumsum(fr) / SR
    w = np.tanh(3 * np.sin(ph)) * 0.6 + 0.4 * np.sin(2 * ph)
    e = np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.05) * (0.75 + 0.25 * np.sin(2 * np.pi * 0.9 * t))
    s = w * e * g
    i = int(t0 * SR)
    if i >= n:
        return
    s = s[: n - i]; pn = np.sin(2 * np.pi * pan_sp * t[:len(s)] / 2)
    L[i:i + len(s)] += s * (1 - np.maximum(0, pn)); R[i:i + len(s)] += s * (1 + np.minimum(0, pn))


def siren(t0, d, g=0.12):
    t = t_(d); fr = 900 + 450 * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 2.2 * t)))
    w = np.tanh(2 * np.sin(2 * np.pi * np.cumsum(fr) / SR))
    place(w * g * np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.05), t0)


def fob_beep(at, g=0.2):
    beep(at, 2600, g); beep(at + 0.14, 2600, g)


def echo_beeps(at, g=0.1):
    for k in range(5):
        place(np.sin(2 * np.pi * 2600 * t_(0.08)) * env(0.08, 0.003, 0.04) * g * (0.8 ** k), at + k * 0.11, 1, (-1) ** k * 0.6)


def air_brake(at, g=0.25):
    s_ = nz(0.6, 0.6); tt = t_(0.6)[:len(s_)]; place(s_ * np.exp(-tt * 5) * g, at)


def hic(at, g=0.35, f0=420):
    """hiccup: short glottal blip + rising chirp + tiny kick"""
    d = 0.11; t = t_(d); fr = f0 * (1 + 1.2 * t / d)
    w = np.tanh(np.sin(2 * np.pi * np.cumsum(fr) / SR) * 3) * env(d, 0.003, 0.04)
    place(w * g + nz(d, 0.5)[:len(t)] * env(d, 0.002, 0.02) * g * 0.5, at)
    place(kick(0.35), at); place(chip(1320, 0.05, g * 0.25), at + 0.06)


def gulp(at, g=0.3):
    place(sweep(380, 150, 0.12, g), at); place(tom(140, g * 0.5), at + 0.05)


def deflate(at, d=1.1, g=0.18):
    t = t_(d); fr = 900 - 500 * t / d + 120 * np.sin(2 * np.pi * 14 * t)
    w = np.sign(np.sin(2 * np.pi * np.cumsum(fr) / SR)) * 0.5
    place(w * g * env(d, 0.01, d) + nz(d, 0.3)[:len(t)] * g * 0.5 * env(d, 0.01, d), at)


def inflate(t0, d, g=0.06):
    place(sweep(120, 420, d, g), t0)



# low background music (kept quiet: silence is the joke)
# ------------------------------------------------------------------ sneeze sfx
def robo_voice(at, syl=11, d=1.7, g=0.16, f0=150):
    """monotone robot 'UN-EX-PEC-TED I-TEM IN BAG-GING A-RE-A' - buzzy vowel blips"""
    t = t_(d); ph = np.cumsum(f0 + 0 * t) / SR
    w = np.sign(np.sin(2 * np.pi * ph)) * 0.5 + np.sin(2 * np.pi * ph * 3) * 0.3 + np.sin(2 * np.pi * ph * 7.1) * 0.15
    seg = d / syl
    gate = np.zeros_like(t)
    for k in range(syl):
        a = k * seg; m = (t >= a) & (t < a + seg * 0.78)
        gate[m] = np.sin(np.pi * (t[m] - a) / (seg * 0.78)) ** 0.5 * (0.8 + 0.2 * ((k * 7) % 3) / 2)
    # vowel-ish formant wobble
    form = 0.6 + 0.4 * np.sin(2 * np.pi * (1 / seg) * t * 0.5)
    place(np.tanh(w * gate * form * 2) * g, at)


def alarm(f0, f1, origin, g=0.07):
    fr = f0
    while fr < f1:
        if (fr - origin) % 8 == 0:
            place(sweep(1400, 1900, 0.12, g * 5), F(fr), 1, 0.2)
        fr += 1


def scanner_beep(at, g=0.22):
    t = t_(0.14); place(np.sin(2 * np.pi * 2900 * t) * env(0.14, 0.003) * np.minimum(1, (0.14 - t) / 0.01) * g, at)


def chime_ok(at, g=0.14):
    for j, fq in enumerate((784, 988, 1175)):
        place(mbox(fq, 0.8, g), at + j * 0.09)


# ------------------------------------------------------------------ extra
def muzak(t0, t1, g=0.05):
    """soft original elevator bossa: plucked 7th chords + music-box melody"""
    b_ = 60 / 104
    chords = [(262, 330, 392, 494), (220, 262, 330, 392), (294, 349, 440, 523), (196, 247, 294, 349)]
    mel = [659, 587, 523, 587, 659, 784, 659, 587, 523, 494, 523, 587, 440, 494, 523, 392]
    k = 0
    while t0 + k * b_ / 2 < t1:
        tb = t0 + k * b_ / 2
        ch = chords[(k // 8) % 4]
        if k % 8 in (0, 3, 6):
            for fq in ch:
                place(pluck(fq, 0.5, g * 0.6), tb, 1, 0.2)
        if k % 2 == 0:
            place(bass(ch[0] / 2, b_ * 0.8), tb, g * 1.2)
        if k % 2 == 0:
            place(mbox(mel[(k // 2) % len(mel)] * 2, 0.6, g * 0.7), tb + 0.01, 1, -0.2)
        place(hat(), tb, g * 1.5, 0.3)
        k += 1


def boop(at, k=0, g=0.2):
    fq = 520 + 45 * k
    place(sweep(fq, fq * 1.6, 0.12, g), at); beep(at, 1800 + 80 * k, g * 0.25)


# ------------------------------------------------------------------ new for 70
def freeze_snd(at, d=0.7, g=0.16):
    """crystalline ice-over: falling sparkle pings + icy downward sweep"""
    for k in range(14):
        fq = 4200 - k * 220 + rng.uniform(-80, 80)
        place(np.sin(2 * np.pi * fq * t_(0.25)) * np.exp(-t_(0.25) * 18) * g * 0.6, at + k * d / 14, 1, rng.uniform(-0.6, 0.6))
    place(sweep(2400, 500, d, g * 0.8), at)
    x = nz(d, 0.6); place(x * np.linspace(1, 0, len(x)) * g * 0.35, at)


def long_slurp(at, d=0.8, g=0.22):
    t = t_(d); x = nz(d, 0.25)[:len(t)]
    am = 0.55 + 0.45 * np.sin(2 * np.pi * 11 * t + 3 * np.sin(2 * np.pi * 2 * t))
    tone = np.sin(2 * np.pi * np.cumsum(420 + 260 * np.sin(2 * np.pi * 3 * t)) / SR) * 0.35
    e = np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.08)
    place((x * 0.8 + tone) * am * e * g, at)


def clink(at, g=0.25):
    for fq in (2637, 3520, 4186):
        place(np.sin(2 * np.pi * fq * t_(0.4)) * np.exp(-t_(0.4) * 12) * g / 3, at)


def dryer(t0, d, g=0.07):
    t = t_(d); hum = np.sin(2 * np.pi * 180 * t) * 0.3 + np.sin(2 * np.pi * 360 * t) * 0.15
    x = nz(d, 0.12)[:len(t)]
    e = np.minimum(1, t / 0.1) * np.minimum(1, (d - t) / 0.1)
    place((x + hum) * e * g, t0)



# ------------------------------------------------------------------ cues (don't wake the baby)
def wah(at, d=1.0, g=0.16):
    t = t_(d); fr = 520 + 220 * np.sin(np.pi * np.minimum(1, t / (d * 0.5))) * np.exp(-t * 0.4) + 25 * np.sin(2 * np.pi * 6 * t)
    ph = np.cumsum(fr) / SR
    w = sum(np.sin(2 * np.pi * ph * h) * (1.0 if h in (2, 3, 4) else 0.4) / h for h in range(1, 9))
    e = np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.12)
    place(np.tanh(w * 2.0) * e * g, at)


def big_snore(at, d=0.6, g=0.35):
    t = t_(d); saw = 2 * (t * 55 % 1) - 1
    am = 0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 28 * t))
    e = np.sin(np.pi * t / d) ** 0.7
    x = nz(d, 0.05)[:len(t)]
    place((np.tanh(saw * 3) * 0.7 + x * 0.5) * am * e * g, at)
    place(sweep(1800, 2600, 0.35, g * 0.25), at + d)   # whistle "shooo"


def mw_hum(t0, d, g=0.05):
    t = t_(d); w = np.sin(2 * np.pi * 120 * t) * 0.5 + np.sin(2 * np.pi * 240 * t) * 0.2
    e = np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.05)
    place(w * e * g, t0)


def shh(at, d=0.7, g=0.25):
    x = np.diff(nz(d, 0.9), prepend=0); t = t_(d)[:len(x)]
    place(x / (np.abs(x).max() + 1e-9) * np.sin(np.pi * t / d) ** 0.5 * g, at)


def hop(at, g=0.25):
    place(sweep(300, 700, 0.12, g), at); place(tom(140, g), at + 0.1)

# ------------------------------------------------------------------ new for 75
def jingle(t0, t1, g=0.05):
    """sleigh-bell shakes, quiet holiday bed"""
    t = t0
    while t < t1:
        for k in range(3):
            d = 0.12; tt = t_(d)
            place(sum(np.sin(2 * np.pi * fq * tt) for fq in (2900, 4100, 5300)) * np.exp(-tt * 40) * g * rng.uniform(0.6, 1), t + k * 0.05, 1, rng.uniform(-0.4, 0.4))
        t += 0.47


def glockenspiel(t0, t1, g=0.05):
    notes = [659, 659, 659, 0, 659, 659, 659, 0, 659, 784, 523, 587, 659, 0, 0, 0]   # original simple bell riff
    b = 0.235; i = 0; t = t0
    while t < t1:
        fq = notes[i % len(notes)]
        if fq:
            tt = t_(0.6); place((np.sin(2 * np.pi * fq * tt) + 0.4 * np.sin(2 * np.pi * fq * 2.76 * tt)) * np.exp(-tt * 6) * g, t, 1, 0.2)
        t += b; i += 1


def twinkle(at, g=0.08):
    for j, fq in enumerate((1568, 2093, 2637, 3136)):
        tt = t_(0.3); place(np.sin(2 * np.pi * fq * tt) * np.exp(-tt * 12) * g, at + j * 0.05, 1, -0.5 + j * 0.3)


# ------------------------------------------------------------------ 79: Dad vs ONE tiny spider
def clink(at, g=0.25):
    t = t_(0.5)
    place((np.sin(2 * np.pi * 2350 * t) + 0.6 * np.sin(2 * np.pi * 3720 * t) + 0.3 * np.sin(2 * np.pi * 5110 * t)) * np.exp(-t * 9) * g, at)
    place(tom(140, 0.4), at)


def knock_snd(at, g=0.55):
    for k in range(2):
        place(tom(180, g), at + k * 0.16); place(nz(0.04, 0.5) * g * 0.3, at + k * 0.16)


def tiptoe_pizz(t0, t1, g=0.2):
    notes = (196, 247, 196, 247, 220, 262, 220, 262)
    k = 0
    while t0 + k * 0.2 < t1:
        place(pizz(notes[k % len(notes)], g), t0 + k * 0.2, 1, (-1) ** k * 0.3); k += 1


def rattle(t0, t1, g=0.12):
    t = t0
    while t < t1:
        place(tom(320, g), t); t += 0.09


def big_rise(at, d=0.9, g=0.18):
    place(sweep(60, 140, d, g), at); place(sweep(90, 210, d, g * 0.6), at)


def hook_snd(t0):
    stab(t0, 0.4); scream(t0, 1.3, 0.22, 560); rattle(t0, t0 + 1.6, 0.08)


# ------------------------------------------------------------------ 81: Dad vs the fitted sheet
def strain(t0, d=1.6, g=0.16):
    groan(t0, d, g); stretch(t0 + 0.2, 0.1); stretch(t0 + 0.8, 0.1)


def ping(at, g=0.3):
    place(sweep(900, 1900, 0.12, g), at); boing(at + 0.02, g * 0.5)


def hook81(t0):
    strain(t0, 1.7, 0.18); stab(t0, 0.28)


# ------------------------------------------------------------------ 82: Dad vs wrapping paper
def sneeze(at, g=0.25):
    place(sweep(500, 900, 0.35, g * 0.4), at)
    x = nz(0.3, 0.6); place(x * np.exp(-t_(0.3)[:len(x)] * 9) * g, at + 0.4)


def hook82(t0):
    stab(t0, 0.3); scream(t0, 1.3, 0.18, 560); tape_rip(t0 + 0.2, 0.22); tape_rip(t0 + 1.0, 0.18)


# ------------------------------------------------------------------ 83: Dad vs the air mattress
def huff(at, g=0.3):
    """one big lung-full blown into the valve"""
    x = nz(0.5, 0.5); t = t_(0.5)[:len(x)]
    place(x * np.sin(np.pi * t / 0.5) ** 0.8 * g, at)
    inflate(at + 0.05, 0.4, g * 0.25)


def motor(t0, d, g=0.1):
    t = t_(d); saw = 2 * (t * (95 + 30 * t / d) % 1) - 1
    e = np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.05)
    place((np.tanh(saw * 2) * 0.6 + nz(d, 0.2)[:len(t)] * 0.4) * e * g, t0)


def hook83(t0):
    stab(t0, 0.28)
    for k in range(3):
        huff(t0 + 0.05 + k * 0.55, 0.22)
    groan(t0 + 0.2, 1.4, 0.1)

# ------------------------------------------------------------------ 84: Dad vs the ketchup bottle
def shake_snd(t0, t1, g=0.18, dt=0.1):
    t = t0
    while t < t1:
        x = nz(0.06, 0.4); place(x * np.exp(-t_(0.06)[:len(x)] * 40) * g, t, 1, rng.uniform(-0.4, 0.4)); t += dt


def tap(at, g=0.4):
    place(tom(170, g), at); place(tick(0.15), at)


def splort(at, d=1.0, g=0.45):
    x = nz(d, 0.08); tt = t_(d)[:len(x)]
    place(x * (0.6 + 0.4 * np.sin(2 * np.pi * 14 * tt)) * np.exp(-tt * 1.8) * g, at)
    place(sweep(160, 60, d * 0.8, g * 0.8), at); place(kick(1.0), at)


def hook84(t0):
    stab(t0, 0.26); shake_snd(t0, t0 + 1.7, 0.16, 0.12); groan(t0 + 0.1, 1.5, 0.1)


# ------------------------------------------------------------------ 85: Dad vs the snow plow
def scrape(at, d=0.22, g=0.3):
    x = nz(d, 0.35); tt = t_(d)[:len(x)]
    place(x * np.sin(np.pi * tt / d) * g, at, 1, rng.uniform(-0.3, 0.3)); place(sweep(300, 180, d, g * 0.25), at)


def shovel_cycle(t0, t1, dt=0.38, g=0.22):
    t = t0
    while t < t1:
        scrape(t, 0.2, g); place(nz(0.1, 0.3) * np.exp(-t_(0.1)[:int(SR * 0.1)] * 30) * g * 0.6, t + 0.24); t += dt


def plow_roar(t0, d, g=0.14, pan0=-0.8, pan1=0.8):
    t = t_(d); fq = 52 + 8 * np.sin(2 * np.pi * 3 * t)
    saw = 2 * ((np.cumsum(fq) / SR) % 1) - 1
    e = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.7
    sig = (np.tanh(saw * 3) * 0.6 + nz(d, 0.15)[:len(t)] * 0.4) * e * g
    pan = np.linspace(pan0, pan1, len(t))
    i = int(t0 * SR); m = min(len(sig), n - i)
    L[i:i + m] += sig[:m] * (1 - np.maximum(0, pan[:m])); R[i:i + m] += sig[:m] * (1 + np.minimum(0, pan[:m]))


def fwoosh(at, g=0.5):
    x = nz(0.9, 0.12); tt = t_(0.9)[:len(x)]
    place(x * np.exp(-tt * 3) * g, at); place(sweep(400, 90, 0.8, g * 0.4), at); place(kick(0.8), at + 0.05)


def saw_zz(at, d=0.5, g=0.22):
    tt = t_(d); x = nz(d, 0.6)[:len(tt)] * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 9 * tt[:len(nz(d, 0.6))])))
    place(x * env(d, 0.01, d * 0.6)[:len(x)] * g, at); place(sweep(900, 600, d, g * 0.15), at)


def rustle_pull(t0, t1, g=0.18):
    t = t0
    while t < t1:
        rustle(t, 0.22, g); t += 0.3


def hook86(t0):
    stab(t0, 0.26); strain(t0 + 0.05, 1.6, 0.14); rustle_pull(t0, t0 + 1.75, 0.16)




def hook87(t0):
    stab(t0, 0.26); munch(t0 + 0.1, t0 + 1.5, 0.16); twinkle(t0 + 0.3, 0.06)

def squirt(at, g=0.3):
    place(sweep(700, 250, 0.22, g), at); x = nz(0.25, 0.3); place(x * np.exp(-t_(0.25)[:len(x)] * 14) * g * 0.6, at)


def hook88(t0):
    stab(t0, 0.26); strain(t0 + 0.05, 1.6, 0.14); creak(t0 + 0.3, 0.1); creak(t0 + 1.0, 0.1)


def hook89(t0):
    stab(t0, 0.26); scream(t0 + 0.05, 1.2, 0.12, 560); boing(t0 + 0.1, 0.12)




def rain_bed(t0, t1, g=0.05):
    d = t1 - t0; x = nz(d, 0.6); tt = t_(d)[:len(x)]
    place(x * np.minimum(1, tt / 0.2) * np.minimum(1, (d - tt) / 0.2) * g, t0)
    raindrops(t0, d)


def ribbit(at, g=0.18):
    for k in range(2):
        t = t_(0.12); fr = 180 + 60 * np.sin(2 * np.pi * 30 * t)
        place(np.tanh(np.sin(2 * np.pi * np.cumsum(fr) / SR) * 3) * np.exp(-t * 14) * g, at + k * 0.14)


def umb_open(at, g=0.4):
    click(at, 0.35); place(nz(0.25, 0.3) * np.exp(-t_(0.25)[:int(SR * 0.25)] * 14) * g * 0.6, at + 0.05); place(kick(0.5), at + 0.06)




def car_alarm(t0, t1, g=0.07):
    d = t1 - t0; t = t_(d); fr = np.where((t * 2.5 % 1) < 0.5, 900 + 500 * (t * 5 % 1), 1400 - 500 * (t * 5 % 1))
    place(np.sign(np.sin(2 * np.pi * np.cumsum(fr) / SR)) * 0.5 * np.minimum(1, (d - t) / 0.1) * g, t0)


def rev_beeps(t0, t1, g=0.1):
    t = t0
    while t < t1:
        beep(t, 1050, g); t += 0.42


def crowd_murmur(t0, t1, g=0.05):
    d = t1 - t0; x = nz(d, 0.08); tt = t_(d)[:len(x)]
    place(x * (0.7 + 0.3 * np.sin(2 * np.pi * 1.3 * tt)) * np.minimum(1, tt / 0.3) * np.minimum(1, (d - tt) / 0.3) * g, t0)


def cheer(at, d=1.4, g=0.25):
    x = nz(d, 0.35); tt = t_(d)[:len(x)]
    place(x * np.minimum(1, tt / 0.05) * np.exp(-tt * 1.6) * g, at)
    for k in range(12):
        place(clap(), at + 0.05 + k * 0.1 + rng.uniform(0, 0.04), 0.35, rng.uniform(-0.6, 0.6))


def clatter(at, d=0.8, k=10, g=0.12):
    """plastic containers bouncing: short hollow knocks"""
    for j in range(k):
        tt = at + rng.uniform(0, d); fq = rng.uniform(500, 1100); t = t_(0.07)
        place(np.sin(2 * np.pi * fq * t) * np.exp(-t * 60) * g + nz(0.07, 0.4)[:len(t)] * np.exp(-t * 80) * g * 0.6, tt, 1, rng.uniform(-0.6, 0.6))


def snap_click(at, g=0.5):
    t = t_(0.05); place(nz(0.05, 0.6)[:len(t)] * np.exp(-t * 120) * g, at); place(np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90) * g * 0.5, at + 0.012)


def nope(at):
    buzz(at, 0.25, 0.12); thud(at, 0.3)


def hook93(t0):
    stab(t0, 0.24); clatter(t0, 1.9, 22, 0.1); gasp(t0 + 0.05, 0.8, 0.1)


def smk(t0, t1, period=0.42, g=0.09):
    t = t0
    while t < t1:
        beep(t, 3150, g); beep(t + 0.09, 3150, g * 0.9); beep(t + 0.18, 3150, g * 0.8)
        t += period + 0.18


def fwap(t0, t1, dt=0.3, g=0.14):
    t = t0
    while t < t1:
        whoosh(t, 0.18, g); t += dt


def howl(at, d=1.0, g=0.08):
    t = t_(d); fr = 520 + 180 * np.sin(np.pi * t / d) + 12 * np.sin(2 * np.pi * 6 * t)
    place(np.sin(2 * np.pi * np.cumsum(fr) / SR) * g * env(d, 0.08, d * 0.7), at, 1, -0.4)


def kapow(at):
    stab(at, 0.35); thud(at, 0.9); place(nz(0.6, 0.15) * np.exp(-t_(0.6) * 6) * 0.5, at); whoosh(at + 0.05, 0.4, 0.25)


def clink(at, g=0.22):
    bell(at, g * 0.6); ding(at + 0.02, g * 0.5)


def boop(at, g=0.12):
    chip(880, 0.08, g); place(chip(880, 0.08, g), at); place(chip(1320, 0.08, g), at + 0.09)


def whirr(t0, d, g=0.08):
    fan_whirr(t0, d, g)
    t = t_(d); place(np.sin(2 * np.pi * (180 + 20 * np.sin(2 * np.pi * 3 * t)) * t) * g * 0.6 * env(d, 0.05, d), t0)


def rattle(t0, d, g=0.25):
    t = t0
    while t < t0 + d:
        thud(t, g * 0.5); clank(t + 0.05) if int(t * 10) % 3 == 0 else None; t += 0.13


def hook95(t0):
    stab(t0, 0.22); rattle(t0, 1.9, 0.35); creak(t0 + 0.6, 0.1)


def tink(at, g=0.18):
    t = t_(0.5); place((np.sin(2 * np.pi * 2637 * t) + 0.5 * np.sin(2 * np.pi * 3951 * t)) * np.exp(-t * 12) * g, at, 1.0, 0.3)


def skree(t0, d=1.0, g=0.12):
    """saw/knife on a frozen turkey: scrapy squeal + grit"""
    t = t_(d); fr = 1400 + 300 * np.sin(2 * np.pi * 4.5 * t)
    sig = np.sin(2 * np.pi * np.cumsum(fr) / SR) * 0.5 + nz(d, 0.6) * 0.5
    place(sig * env(d, 0.01) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 3.3 * t))) * g, t0)


def hook96(t0):
    stab(t0, 0.22); skree(t0, 1.9, 0.1); sizzle(t0 + 0.1, 1.6, 0.06)


def wriggle(t0, d, g=0.2):
    t = t0
    while t < t0 + d:
        rustle(t, 0.18, g); t += 0.21


def hook97(t0):
    stab(t0, 0.2); wriggle(t0, 1.9, 0.22); grunt(t0 + 0.3, 0.8, 0.12, 180); grunt(t0 + 1.2, 0.6, 0.1, 200)




def lava_bed(t0, t1, g=0.05):
    bubbles_snd(t0, t1, g); sizzle(t0, t1 - t0, g * 0.5)


def hook98(t0):
    stab(t0, 0.22); scream(t0 + 0.05, 1.1, 0.12, 620); lava_bed(t0, t0 + 2.0, 0.06)


def fwump(at, g=0.5):
    thud(at, g); place(nz(0.4, 0.2) * np.exp(-t_(0.4)[:int(SR * 0.4)] * 9) * g * 0.5, at)


def hook99(t0):
    stab(t0, 0.22); scream(t0 + 0.05, 1.0, 0.1, 760); twinkle_bed(t0, t0 + 2.0)


def twinkle_bed(t0, t1, g=0.03):
    notes = (1047, 1319, 1568, 1319, 1175, 1568)
    t = t0; i = 0
    while t < t1:
        place(mbox(notes[i % 6], 0.6, g), t, 1, 0.3 * ((-1) ** i)); t += 0.33; i += 1




def pucker(at, g=0.25):
    # squeaky rubbery squeeze: fast downward wobble
    t = t_(0.6); fr = 900 * np.exp(-t * 3) + 300 + 60 * np.sin(2 * np.pi * 22 * t)
    place(np.sign(np.sin(2 * np.pi * np.cumsum(fr) / SR)) * 0.3 * env(0.6, 0.01, 0.3) * g, at)


def sugar_buzz(at, d=0.6, g=0.12):
    t = t_(d); fr = 180 + 40 * np.sin(2 * np.pi * 30 * t)
    place(np.sign(np.sin(2 * np.pi * np.cumsum(fr) / SR)) * env(d, 0.01, d * 0.6) * g, at)


def zoom_by(at, g=0.3):
    place(sweep(1400, 300, 0.4, g), at + 0.25, 1, 0.5)
    place(sweep(300, 1400, 0.25, g), at, 1, -0.5)


def unroll(t0, d, g=0.15):
    for k in range(int(d / 0.06)):
        place(nz(0.05, 0.5) * np.exp(-t_(0.05)[:int(SR * 0.05)] * 60) * g, t0 + k * 0.06, 1, 0.3 * math.sin(k))




def glide(at, d=0.6, g=0.12, pan=0.0):
    # skate blade hiss: bright noise swell
    x = np.diff(nz(d, 0.6), prepend=0); x /= (np.abs(x).max() + 1e-9)
    tt = t_(d)[:len(x)]
    place(x * np.sin(np.pi * tt / d) ** 2 * g, at, 1, pan)


import math


def kachunk(at, g=0.6, big=False):
    click(at, 0.5)
    place(kick(1.0) * g, at + 0.01)
    t = t_(0.7 if big else 0.4)
    hum = (np.sin(2 * np.pi * 60 * t) + 0.5 * np.sin(2 * np.pi * 120 * t) + 0.3 * np.sin(2 * np.pi * 180 * t)) * np.exp(-t * (3 if big else 7))
    place(hum * g * 0.35, at + 0.02)
    if big:
        place(sweep(200, 1600, 0.8, 0.12), at); choir(at + 0.05, 1.6, 0.06)


def inflate(at, g=0.3):
    d = 0.5; tt = t_(d); x = nz(d, 0.3)[:len(tt)]
    place(x * np.minimum(1, tt / 0.4) * np.exp(-np.maximum(0, tt - 0.4) * 30) * g, at)
    place(sweep(150, 600, 0.5, 0.12), at)


def match(at, g=0.3):
    d = 0.3; tt = t_(d); x = np.diff(nz(d, 0.7), prepend=0)[:len(tt)]
    place(x / (np.abs(x).max() + 1e-9) * np.exp(-tt * 12) * g, at)


def meow(at, g=0.25):
    d = 0.55; tt = t_(d)
    f = 520 + 420 * np.sin(np.pi * np.minimum(1, tt / d)) ** 1.5 + 12 * np.sin(2 * np.pi * 7 * tt)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)) * np.minimum(1, tt / 0.04) * np.exp(-np.maximum(0, tt - 0.35) * 12)
    place(x * g, at)


def hiss(at, d=0.7, g=0.3):
    tt = t_(d); x = np.diff(nz(d, 1.0), prepend=0)[:len(tt)]
    x = np.diff(x, prepend=0)
    x = x / (np.abs(x).max() + 1e-9)
    place(x * np.minimum(1, tt / 0.05) * np.exp(-tt * 3) * g, at)


def clatter(t0, t1, g=0.12):
    t = t0
    while t < t1:
        place(np.sin(2 * np.pi * rng.uniform(1800, 4200) * t_(0.03)) * np.exp(-t_(0.03) * 120) * g * rng.uniform(0.4, 1),
              t, 1, rng.uniform(-0.7, 0.7))
        t += rng.uniform(0.015, 0.06)


def hook103(t0):
    stab(t0, 0.22); scream(t0 + 0.05, 1.0, 0.08, 600)
    shake_snd(t0 + 0.1, t0 + 1.6, 0.12, 0.12)


def hook104(t0):
    stab(t0, 0.22); munch(t0 + 0.02, t0 + 0.7, 0.2)
    shake_snd(t0 + 0.1, t0 + 1.2, 0.1, 0.1)




def rumble(t0, d, g=0.12):
    x = nz(d, 0.01); tt = t_(d)[:len(x)]
    place(x * (0.7 + 0.3 * np.sin(2 * np.pi * 7 * tt)) * g * np.minimum(1, tt / 0.2) * np.minimum(1, (d - tt) / 0.2), t0)
    place(np.sin(2 * np.pi * 42 * tt) * g * 0.6 * np.minimum(1, tt / 0.2) * np.minimum(1, (d - tt) / 0.2), t0)


def snow_crunch(at, g=0.3):
    x = nz(0.12, 0.6); place(x * np.exp(-t_(0.12)[:len(x)] * 25) * g, at, 1, rng.uniform(-0.3, 0.3))


def roll_crunch(t0, t1, dt=0.2, g=0.18):
    t = t0
    while t < t1:
        snow_crunch(t, g); t += dt


def hook106(t0):
    stab(t0, 0.22); roll_crunch(t0, t0 + 2.0, 0.22, 0.2)
    grunt(t0 + 0.3, 0.5, 0.12, 130); grunt(t0 + 1.1, 0.5, 0.12, 150)


def hook107(t0):
    stab(t0, 0.22); scream(t0 + 0.04, 0.9, 0.08, 560)
    ask(t0 + 0.6, 0.09, True)


def bleh(at, g=0.25):
    tt = t_(0.6); fr = 180 - 80 * tt
    x = np.sign(np.sin(2 * np.pi * np.cumsum(fr) / SR)) * 0.5 + nz(0.6, 0.3)[:len(tt)] * 0.3
    place(x * np.minimum(1, tt / 0.02) * np.exp(-tt * 4) * g, at)



def hook108(t0):
    stab(t0, 0.22); scream(t0 + 0.04, 0.9, 0.08, 600)
    shovel_cycle(t0, t0 + 1.9, 0.2, 0.2)
    ask(t0 + 0.7, 0.09, True)


def laugh(at, g=0.1):
    for k in range(4):
        hee(at + k * 0.13, g)


hook108(0)
jingle(0.0, DUR, 0.025)
walk_bgm(0.0, DUR, 0.08)
# macro peephole
whoosh(F(60), 0.25, 0.3); stab(F(60), 0.15)
shovel_cycle(F(62), F(90), 0.18, 0.25)
ding(F(90), 0.22); ask(F(91), 0.1, True)
# roof avalanche
creak(F(122), 0.16); creak(F(130), 0.14)
whoosh(F(136), 0.4, 0.4); fwump(F(144), 0.9)
ask(F(159), 0.08, False)
# tool montage
for t0 in (200, 245, 290):
    whoosh(F(t0), 0.22, 0.3); stab(F(t0), 0.15)
for k in range(4):
    tink(F(204 + 6 * k), 0.2)
nope(F(226))
dryer(F(249), 0.75, 0.09)
cork_pop(F(271), 0.5); ask(F(274), 0.1, True)
breath(F(294), 0.75, 0.28)
freeze_snd(F(312), 0.6, 0.16); ask(F(321), 0.08, False)
# close-up
chatter(F(342), F(367), 0.1)
stab(F(368), 0.3); scream(F(368), 0.6, 0.07, 640)
# mega scrape
skree(F(396), 0.73, 0.12); shovel_cycle(F(396), F(418), 0.1, 0.22)
ding(F(418), 0.3); harp_up(F(419), 0.1); twinkle(F(420), 0.08)
ask(F(421), 0.1, True)
# the neighbour
for k in range(4):
    snow_crunch(F(440 + 4 * k), 0.18)
fob_beep(F(456), 0.2); fob_beep(F(461), 0.2)
ask(F(470), 0.09, True); ask(F(476), 0.1, True)
# reveal
whoosh(F(510), 0.35, 0.45); stab(F(512), 0.3); doom(F(513), 0.2)
vroom(F(530), 1.0, 0.16)
laugh(F(526), 0.09)
# own car, twitch, scrape again
ask(F(566), 0.08, False); ask(F(586), 0.08, False); stab(F(586), 0.18)
shovel_cycle(F(610), F(630), 0.2, 0.2)
hook108(F(630))

mix = np.stack([L, R], 1)
mix = np.tanh(mix / np.abs(mix).max() * 1.3) / np.tanh(1.3) * 0.92
mix[-int(0.1 * SR):] *= np.linspace(1, 0, int(0.1 * SR))[:, None]
with wave.open('out/frozen_car_audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('ok')
