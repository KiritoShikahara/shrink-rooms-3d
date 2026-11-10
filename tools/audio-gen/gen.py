"""効果音とBGMを標準ライブラリだけで合成して WAV に書き出す。使い方: python gen.py <出力フォルダ>"""
import math, random, struct, sys, wave, os
SR = 22050
random.seed(7)

def write(path, samples):
    peak = max(1e-9, max(abs(s) for s in samples))
    data = b"".join(struct.pack("<h", int(max(-1, min(1, s / peak * 0.9)) * 32767)) for s in samples)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data)

def env(n, a=0.005, r=0.05):
    out = []
    for i in range(n):
        t = i / SR; dur = n / SR
        out.append(min(1, t / a) * min(1, max(0, (dur - t) / r)))
    return out

def tone(freq, dur, vol=1.0, a=0.005, r=0.08, decay=0.0):
    n = int(SR * dur); e = env(n, a, r)
    return [vol * e[i] * math.exp(-decay * i / SR) * math.sin(2 * math.pi * freq * i / SR) for i in range(n)]

def noise(dur, vol=1.0, a=0.002, r=0.05, lp=0.2):
    n = int(SR * dur); e = env(n, a, r); y = 0; out = []
    for i in range(n):
        y += lp * (random.uniform(-1, 1) - y); out.append(vol * e[i] * y)
    return out

def mix(*ls):
    n = max(len(l) for l in ls); out = [0.0] * n
    for l in ls:
        for i, v in enumerate(l): out[i] += v
    return out

def sweep(f0, f1, dur, vol=1.0, r=0.05):
    n = int(SR * dur); e = env(n, 0.005, r); ph = 0; out = []
    for i in range(n):
        f = f0 + (f1 - f0) * i / n; ph += 2 * math.pi * f / SR; out.append(vol * e[i] * math.sin(ph))
    return out

def seq(*parts):
    out = []
    for p in parts: out += p
    return out

def make(d):
    os.makedirs(d, exist_ok=True)
    for k, f in enumerate((300, 340, 380), 1):
        write(f"{d}/sfx_move{k}.wav", mix(tone(f, 0.07, 0.8, decay=40), noise(0.05, 0.25)))
    write(f"{d}/sfx_push.wav", mix(tone(90, 0.16, 1.0, decay=18), noise(0.12, 0.5, lp=0.08)))
    write(f"{d}/sfx_bump.wav", mix(tone(140, 0.08, 0.8, decay=35), noise(0.04, 0.2)))
    write(f"{d}/sfx_shrink.wav", mix(tone(48, 0.8, 0.9, a=0.1, r=0.3), noise(0.8, 0.6, a=0.1, r=0.3, lp=0.04)))
    write(f"{d}/sfx_crush.wav", mix(noise(0.2, 1.0, lp=0.5, r=0.12), tone(70, 0.25, 0.8, decay=14), tone(900, 0.05, 0.3, decay=60)))
    write(f"{d}/sfx_key.wav", seq(tone(880, 0.09, 0.8, decay=10), tone(1320, 0.22, 0.8, decay=8)))
    write(f"{d}/sfx_door.wav", mix(sweep(180, 520, 0.35, 0.7), noise(0.35, 0.25, lp=0.1)))
    write(f"{d}/sfx_plate.wav", mix(tone(200, 0.1, 0.9, decay=25), noise(0.05, 0.3)))
    write(f"{d}/sfx_pit.wav", sweep(520, 90, 0.45, 0.9, r=0.1))
    write(f"{d}/sfx_clear.wav", seq(*[tone(f, 0.16, 0.8, decay=5) for f in (523, 659, 784, 1047)]))
    write(f"{d}/sfx_fail.wav", mix(sweep(300, 70, 0.6, 0.9, r=0.2), noise(0.6, 0.2, lp=0.05, r=0.2)))
    write(f"{d}/sfx_ui.wav", tone(660, 0.06, 0.7, decay=30))
    # BGM: 16 小節のゆるいループ(パッド + 低音パルス)
    bpm = 96; beat = 60 / bpm; chords = [(110, 164.8, 220), (87.3, 130.8, 174.6), (98, 146.8, 196), (82.4, 123.5, 164.8)]
    out = []
    for bar in range(16):
        c = chords[bar % 4]; n = int(SR * beat * 4)
        pad = [0.0] * n
        for f in c:
            for i in range(n):
                t = i / SR; v = 0.18 * math.sin(2 * math.pi * f * t) + 0.08 * math.sin(2 * math.pi * f * 2.003 * t)
                pad[i] += v * min(1, t / 0.4) * min(1, (n / SR - t) / 0.4)
        for b in range(4):
            s0 = int(SR * beat * b)
            p = tone(c[0] / 2, beat * 0.45, 0.5, a=0.01, r=0.15, decay=5)
            for i, v in enumerate(p):
                if s0 + i < n: pad[s0 + i] += v
        out += pad
    write(f"{d}/bgm_main.wav", out)

if __name__ == "__main__":
    make(sys.argv[1] if len(sys.argv) > 1 else "out")
