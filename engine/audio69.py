"""Audio for scenes69 (Don't Touch the Buttons)."""
import numpy as np, wave
import importlib.util, sys
spec = importlib.util.spec_from_file_location("a6", "/home/claude/audio6.py")
# reuse synth helpers without running audio6's main mix: copy minimal helpers here instead
SR = 44100
DUR = 22.0
n = int(SR * DUR)
L = np.zeros(n); R = np.zeros(n)
rng = np.random.default_rng(869)
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
tension(F(0), F(60), 0.025)
sneak(F(60), F(100), 0.06)
busy_bgm(F(152), F(200), 0.024)
tension(F(200), F(234), 0.025)
busy_bgm(F(234), F(330), 0.022)
walk_bgm(F(330), F(400), 0.025)
innocent(F(500), F(530), 0.02)
tension(F(530), F(592), 0.03)
tension(F(628), F(660), 0.025)
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


# ------------------------------------------------------------------ cues
muzak(F(54), F(318), 0.05)
muzak(F(358), F(470), 0.045)
# 1. hook: DON'T. TOUCH. THE BUTTONS.
stab(F(0), 0.4); gasp(F(1), 0.8, 0.15)
for fr_ in (6, 18, 32):
    place(tom(110, 0.7), F(fr_)); place(clap(), F(fr_), 0.5)
# 2. interior: boop 7 (68), sparkle (86)
boop(F(68), 4)
harp_up(F(86), 0.08)
# panel macro (110): finger presses every button
whoosh(F(112), 0.25, 0.3)
for k in range(11):
    boop(F(110 + 8 + 4.5 * k), k, 0.22)
fanfare(F(167), 0.08)
# Dad NOOOO (170)
panic_hit(F(170)); scream(F(171), 0.6, 0.15, 320)
# 3. floor stops
STOPS = [(190, 42), (232, 32), (264, 24), (288, 16), (304, 14)]
for st, ln in STOPS:
    ding(F(st), 0.3); whoosh(F(st + 1), 0.2, 0.22); whoosh(F(st + ln - 5), 0.18, 0.18)
ask(F(201), 0.1, False)
cricket(F(241)); cricket(F(246))
ask(F(271), 0.1, True)
# split (318): twitch tension / kid yay
tension(F(318), F(358), 0.04)
boing(F(334), 0.15); harp_up(F(334), 0.06)
# 4. floor 7 (358): FINALLY, kid hops out, Phew, BOOP flurry, doors close, floors fly by
ding(F(358), 0.32); fanfare(F(364), 0.08)
whoosh(F(370), 0.3, 0.25); boing(F(371), 0.14)
sigh(F(404), 0.2, 0.9)
stab(F(418), 0.45)
for k in range(8):
    boop(F(418 + 2 * k), k, 0.18)
whoosh(F(434), 0.25, 0.25); thud(F(448), 0.3)
for k in range(6):
    ding(F(452 + 3.5 * k), 0.16)
scream(F(450), 1.4, 0.13, 480)
# 5. floor 12 (470): weary ding, kid from the stairs, walk in, sparkle
ding(F(470), 0.22); sad_trombone(F(474))
footsteps(F(490), 4, 0.12, 0.3); harp_up(F(496), 0.06)
footsteps(F(524), 4, 0.2, 0.3)
harp_up(F(546), 0.08)
# kid ECU (562): creeping finger
heartbeat(F(562), F(608), 0.4, 0.4)
boop(F(588), 4, 0.15)
# loop (610): hook again
stab(F(610), 0.4)
for fr_ in (614, 626, 640):
    place(tom(110, 0.7), F(fr_)); place(clap(), F(fr_), 0.5)

mix = np.stack([L, R], 1)
mix = np.tanh(mix / np.abs(mix).max() * 1.3) / np.tanh(1.3) * 0.92
mix[-int(0.1 * SR):] *= np.linspace(1, 0, int(0.1 * SR))[:, None]
with wave.open('out/dont_touch_the_buttons_audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('ok')
