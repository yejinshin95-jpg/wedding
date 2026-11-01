"""식장 스크린용 사진 슬라이드 영상 (1920×1080, 30fps, 무음).
slides/ 의 장면을 순서대로 크로스페이드로 잇고, 마지막에 첫 화면(00)으로 돌아갑니다 → 반복 재생해도 자연스러움.
첫 화면의 레이스 액자 위에는 살짝 반짝이는 빛(별 모양 글린트)을 그립니다.
사용: node video/render-slides.js && python3 video/render-video.py   (결과: video/wedding-slideshow.mp4)
"""
import subprocess, sys, os, json, math, random
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SL = os.path.join(HERE, 'slides')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'wedding-slideshow.mp4')
W, H, FPS = 1920, 1080, 30
FADE_SEC = 1.5      # 크로스페이드 길이
END_SEC = 6         # 마지막 첫 화면 길이

# ── 반짝임 설정 ─────────────────────────────────────────
SPARKLE_ON_SCREEN = 16          # 동시에 보이는 반짝임 수(평균)
SPARKLE_LIFE = (1.2, 2.2)       # 반짝임 하나가 켜졌다 꺼지는 시간(초)
SPARKLE_SIZE = (14, 34)         # 빛줄기 반지름(px)
SPARKLE_COLOR = np.array([1.0, 0.99, 0.95])   # 살짝 따뜻한 흰빛
# main.jpg(720px) 안에서 레이스가 있는 범위와 가운데 사진 범위
LACE_OUTER = (45, 62, 680, 648)
LACE_INNER = (150, 185, 570, 530)

def lace_points():
    g = np.asarray(Image.open(os.path.join(HERE, '..', 'photos', 'main.jpg')).convert('L')).astype(int)
    ys, xs = np.mgrid[0:g.shape[0], 0:g.shape[1]]
    ox0, oy0, ox1, oy1 = LACE_OUTER; ix0, iy0, ix1, iy1 = LACE_INNER
    m = (xs >= ox0) & (xs <= ox1) & (ys >= oy0) & (ys <= oy1) & ~((xs >= ix0) & (xs <= ix1) & (ys >= iy0) & (ys <= iy1)) & (g >= 224)
    return np.stack([xs[m], ys[m]], 1) / g.shape[1]    # 0~1 비율 좌표

def make_sprite(R):
    y, x = np.mgrid[-R:R + 1, -R:R + 1].astype(float)
    r = np.hypot(x, y)
    core = np.exp(-(r / (0.13 * R)) ** 2)
    ray = lambda a, b, L, w: np.exp(-(np.abs(b) / w) ** 2) * np.clip(1 - np.abs(a) / L, 0, 1) ** 2.2
    w = 0.6 + 0.03 * R
    s = core + ray(x, y, R, w) + ray(y, x, R, w)               # 가로·세로 빛줄기
    u, v = (x + y) / math.sqrt(2), (x - y) / math.sqrt(2)
    s += 0.45 * (ray(u, v, 0.5 * R, w) + ray(v, u, 0.5 * R, w))  # 짧은 대각선
    s += 0.25 * np.exp(-(r / (0.45 * R)) ** 2)                  # 은은한 번짐
    return np.clip(s, 0, 1)

SPRITES = {R: make_sprite(R) for R in range(SPARKLE_SIZE[0], SPARKLE_SIZE[1] + 1, 2)}

def sparkle_schedule(dur, box, seed):
    pts = lace_points(); rnd = random.Random(seed)
    avg_life = sum(SPARKLE_LIFE) / 2; rate = SPARKLE_ON_SCREEN / avg_life
    out, t = [], -avg_life
    while t < dur:
        px, py = pts[rnd.randrange(len(pts))]
        out.append(dict(t0=t, life=rnd.uniform(*SPARKLE_LIFE), x=box['x'] + px * box['w'], y=box['y'] + py * box['h'],
                        R=rnd.choice(list(SPRITES)), peak=rnd.uniform(0.55, 1.0)))
        t += rnd.expovariate(rate)
    return out

def add_sparkles(img, sched, lt):
    a = np.asarray(img).astype(np.float32) / 255
    for s in sched:
        u = (lt - s['t0']) / s['life']
        if not 0 < u < 1: continue
        env = math.sin(math.pi * u) ** 2 * s['peak']
        R = s['R']; sp = SPRITES[R] * env
        x0, y0 = int(round(s['x'])) - R, int(round(s['y'])) - R
        xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + 2 * R + 1), min(H, y0 + 2 * R + 1)
        if xa >= xb or ya >= yb: continue
        k = sp[ya - y0:yb - y0, xa - x0:xb - x0, None] * SPARKLE_COLOR
        reg = a[ya:yb, xa:xb]
        a[ya:yb, xa:xb] = 1 - (1 - reg) * (1 - k)              # 스크린 합성 (밝게만)
    return Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8))

# ── 장면 ──────────────────────────────────────────────
lst = json.load(open(os.path.join(SL, 'list.json')))
lst.append(dict(lst[0], sec=END_SEC))
scenes = []
for i, s in enumerate(lst):
    im = Image.open(os.path.join(SL, s['file'])).convert('RGB')
    sched = sparkle_schedule(s['sec'], s['lace'], seed=i) if s.get('lace') else None
    scenes.append((im, s['sec'], sched))

starts, t = [], 0.0
for i, (_, dur, _) in enumerate(scenes):
    starts.append(t); t += dur - (FADE_SEC if i < len(scenes) - 1 else 0)
total = t

def frame(i, sec):
    im, _, sched = scenes[i]
    return add_sparkles(im, sched, sec - starts[i]) if sched else im

ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-tune', 'stillimage', '-movflags', '+faststart', OUT],
                      stdin=subprocess.PIPE)
for f in range(round(total * FPS)):
    sec = f / FPS
    cur = max(i for i in range(len(scenes)) if starts[i] <= sec)
    img = frame(cur, sec)
    if cur > 0 and sec < starts[cur] + FADE_SEC:
        a = (sec - starts[cur]) / FADE_SEC
        a = a * a * (3 - 2 * a)
        img = Image.blend(frame(cur - 1, sec), img, a)
    ff.stdin.write(img.tobytes())
ff.stdin.close(); ff.wait()
print('done', OUT, f'{total:.1f}s')
