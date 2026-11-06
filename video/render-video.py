"""식장 스크린용 사진 슬라이드 영상 (1920×1080, 30fps, 무음).
- 장면 안의 사진·글은 data-step 순서대로 하나씩 나타납니다: 페이드 인(글은 살짝 떠오름), 필기체는 왼쪽부터 써지듯.
- 장면 사이는 크로스페이드. 끝에는 첫 화면이 다시 나왔다가 요소가 사라져 배경만 남음 → 처음(배경에서 시작)과 이어져 반복 재생이 자연스러움.
- 첫 화면의 레이스 액자 위에는 살짝 반짝이는 빛(별 모양 글린트).
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
OUTRO_SEC = 1.2     # 마지막에 요소가 사라지는 시간

# ── 등장 효과 ─────────────────────────────────────────
START_DELAY = 0.35  # 장면 시작 후 첫 요소가 나오기까지
STEP_GAP = 0.5      # 다음 요소가 나오기까지 (페이드 인 요소)
FADE_IN = 0.9       # 페이드 인 길이
RISE = 18           # 글이 떠오르는 거리(px)
WRITE_BASE, WRITE_PX_PER_SEC = 0.6, 900   # 필기체 써지는 시간 = 기본 + 폭/속도
WRITE_SOFT = 70     # 써지는 경계의 부드러운 폭(px)
PAN_PX = 50         # 꽉 찬 사진이 장면 동안 위로 올라가는 거리(px)

# ── 반짝임 설정 ─────────────────────────────────────────
SPARKLE_ON_SCREEN = 14          # 동시에 보이는 반짝임 수(평균)
SPARKLE_LIFE = (1.2, 2.2)       # 반짝임 하나가 켜졌다 꺼지는 시간(초)
SPARKLE_SIZE = (22, 46)         # 빛줄기 반지름(px)
SPARKLE_COLOR = np.array([1.0, 0.99, 0.96])   # 빛 중심·빛줄기 (흰빛)
GLOW_COLOR = np.array([1.0, 0.90, 0.68])      # 둘레 번짐 (샴페인빛)
# main.jpg(720px) 안에서 레이스가 있는 범위와 가운데 사진 범위
LACE_OUTER = (45, 62, 680, 648)
LACE_INNER = (150, 185, 570, 530)

def lace_points():
    g = np.asarray(Image.open(os.path.join(HERE, '..', 'photos', 'main.jpg')).convert('L')).astype(int)
    ys, xs = np.mgrid[0:g.shape[0], 0:g.shape[1]]
    ox0, oy0, ox1, oy1 = LACE_OUTER; ix0, iy0, ix1, iy1 = LACE_INNER
    m = (xs >= ox0) & (xs <= ox1) & (ys >= oy0) & (ys <= oy1) & ~((xs >= ix0) & (xs <= ix1) & (ys >= iy0) & (ys <= iy1)) & (g >= 120) & (g <= 200)   # 흰 실 사이 회색 망사 위 → 흰 빛이 잘 보임
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
    return np.clip(s, 0, 1), np.exp(-(r / (0.38 * R)) ** 2)     # (빛, 번짐)

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

def add_sparkles(img, sched, lt, gain=1.0):
    a = np.asarray(img).astype(np.float32) / 255
    for s in sched:
        u = (lt - s['t0']) / s['life']
        if not 0 < u < 1: continue
        env = math.sin(math.pi * u) ** 2 * s['peak'] * gain
        R = s['R']; sp, glow = SPRITES[R]
        x0, y0 = int(round(s['x'])) - R, int(round(s['y'])) - R
        xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + 2 * R + 1), min(H, y0 + 2 * R + 1)
        if xa >= xb or ya >= yb: continue
        cy, cx = slice(ya - y0, yb - y0), slice(xa - x0, xb - x0)
        k = env * (sp[cy, cx, None] * SPARKLE_COLOR + 0.55 * glow[cy, cx, None] * GLOW_COLOR)
        k = np.clip(k, 0, 1)
        reg = a[ya:yb, xa:xb]
        a[ya:yb, xa:xb] = 1 - (1 - reg) * (1 - k)              # 스크린 합성 (밝게만)
    return Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8))


ease = lambda u: u * u * (3 - 2 * u)

class Layer:
    def __init__(self, path, meta):
        a = np.asarray(Image.open(path).convert('RGBA')).astype(np.float32) / 255
        ys, xs = np.where(a[..., 3] > 0.002)
        self.x0, self.y0, self.x1, self.y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
        c = a[self.y0:self.y1, self.x0:self.x1]
        self.rgb, self.alpha = c[..., :3], c[..., 3]
        self.w = self.x1 - self.x0
        self.fx, self.step, self.lace = meta['fx'], meta['step'], meta['lace']
        self.rise = RISE if meta['kind'] == 'text' else 0
        self.dur = WRITE_BASE + self.w / WRITE_PX_PER_SEC if self.fx == 'write' else FADE_IN
        self.cols = np.arange(self.w, dtype=np.float32)

    def draw(self, a, u, lt=0, sec=1):
        """u: 0~1 등장 진행도. a: 프레임(float, H×W×3)에 그림."""
        if u <= 0: return
        if self.fx == 'write':
            e = u * (self.w + WRITE_SOFT)                               # 펜 위치
            m = np.clip((e - self.cols) / WRITE_SOFT, 0, 1)[None, :]
            al = self.alpha * m * min(1, u * 6); dy = 0
        else:
            k = ease(min(1, u)); al = self.alpha * k; dy = int(round((1 - k) * self.rise))
        y0, y1 = self.y0 + dy, self.y1 + dy
        cy0, cy1 = max(0, -y0) , (self.y1 - self.y0) - max(0, y1 - H)
        y0, y1 = max(0, y0), min(H, y1)
        reg = a[y0:y1, self.x0:self.x1]; al = al[cy0:cy1, :, None]
        reg[:] = reg * (1 - al) + self.rgb[cy0:cy1] * al

class PanLayer:
    """꽉 채운 사진(화면 전체 또는 반쪽 등 data-fx="pan" 요소의 칸): 페이드 인 + 장면 내내 PAN_PX 만큼 아주 천천히 위로 (소수점 위치까지 부드럽게)."""
    def __init__(self, meta):
        r = meta.get('rect') or {'x': 0, 'y': 0, 'w': W, 'h': H}
        self.x, self.y, self.w, self.h = r['x'], r['y'], r['w'], r['h']
        im = Image.open(os.path.join(HERE, meta['src'])).convert('RGB')
        sc = max(self.w / im.width, (self.h + PAN_PX + 2) / im.height)
        im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
        x0 = (im.width - self.w) // 2
        self.img = np.asarray(im).astype(np.float32)[:, x0:x0 + self.w] / 255
        room = self.img.shape[0] - self.h - 1
        c = room * meta.get('pos', 0.5)
        self.y_from = min(max(c - PAN_PX / 2, 0), room - PAN_PX)    # 처음 보이는 위치
        self.fx, self.step, self.lace, self.dur = 'pan', meta['step'], False, FADE_IN

    def draw(self, a, u, lt=0, sec=1):
        if u <= 0: return
        y = self.y_from + PAN_PX * min(1, max(0, lt / sec))         # 보는 창이 내려감 = 사진이 위로 올라감
        yi, f = int(y), y - int(y)
        crop = self.img[yi:yi + self.h] * (1 - f) + self.img[yi + 1:yi + 1 + self.h] * f
        k = ease(min(1, u))
        reg = a[self.y:self.y + self.h, self.x:self.x + self.w]
        reg[:] = reg * (1 - k) + crop * k

class Scene:
    def __init__(self, meta, idx, settled=False, outro=False, sec=None):
        self.sec = sec or meta['sec']
        self.bg = np.asarray(Image.open(os.path.join(SL, meta['bg'])).convert('RGB')).astype(np.float32) / 255
        self.layers = [PanLayer(l) if l['fx'] == 'pan' else Layer(os.path.join(SL, l['file']), l) for l in meta['layers']]
        self.moving = any(isinstance(l, PanLayer) for l in self.layers)   # 계속 움직이는 장면은 완성 화면을 저장해 두지 않음
        # 등장 시각: step 순서대로
        t = START_DELAY; self.start = {}
        for st in sorted({l.step for l in self.layers}):
            self.start[st] = t
            ws = [l.dur for l in self.layers if l.step == st and l.fx == 'write']
            t += max(STEP_GAP, max(ws) * 0.85) if ws else STEP_GAP
        self.settled, self.outro = settled, outro
        self.sched = sparkle_schedule(self.sec, meta['lace'], seed=idx) if meta.get('lace') else None
        self.lace_layer = next((l for l in self.layers if l.lace), None)
        self.done_at = max(self.start[l.step] + l.dur for l in self.layers) if self.layers else 0
        self._full = None

    def progress(self, l, lt):
        return 1.0 if self.settled else (lt - self.start[l.step]) / l.dur

    def frame(self, lt):
        k_out = 1.0
        if self.outro and lt > self.sec - OUTRO_SEC: k_out = 1 - ease(min(1, (lt - (self.sec - OUTRO_SEC)) / OUTRO_SEC))
        if (self.settled or lt >= self.done_at) and k_out == 1.0 and self._full is not None and not self.moving:
            a = self._full.copy()
        else:
            a = self.bg.copy()
            for l in self.layers: l.draw(a, min(1.0, self.progress(l, lt)), lt, self.sec)
            if (self.settled or lt >= self.done_at) and k_out == 1.0: self._full = a.copy()
            if k_out < 1.0: a = self.bg + (a - self.bg) * k_out
        img = Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8))
        if self.sched:
            lace_k = min(1.0, max(0.0, self.progress(self.lace_layer, lt))) if self.lace_layer else 1.0
            lace_k *= k_out
            if lace_k > 0: img = add_sparkles(img, self.sched, lt, lace_k)
        return img

lst = json.load(open(os.path.join(SL, 'list.json')))

# 미리보기: python3 render-video.py --still 장면번호 초 out.png
if len(sys.argv) > 1 and sys.argv[1] == '--still':
    i = int(sys.argv[2]); Scene(lst[i], i).frame(float(sys.argv[3])).save(sys.argv[4]); sys.exit()

scenes = [Scene(m, i) for i, m in enumerate(lst)] + [Scene(lst[0], 99, settled=True, outro=True, sec=END_SEC)]
starts, t = [], 0.0
for i, sc in enumerate(scenes):
    starts.append(t); t += sc.sec - (FADE_SEC if i < len(scenes) - 1 else 0)
total = t

ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-tune', 'stillimage', '-movflags', '+faststart', OUT],
                      stdin=subprocess.PIPE)
for f in range(round(total * FPS)):
    sec = f / FPS
    cur = max(i for i in range(len(scenes)) if starts[i] <= sec)
    img = scenes[cur].frame(sec - starts[cur])
    if cur > 0 and sec < starts[cur] + FADE_SEC:
        a = ease((sec - starts[cur]) / FADE_SEC)
        img = Image.blend(scenes[cur - 1].frame(sec - starts[cur - 1]), img, a)
    ff.stdin.write(img.tobytes())
    if f % (FPS * 10) == 0: print(f'{sec:5.1f}s / {total:.1f}s', flush=True)
ff.stdin.close(); ff.wait()
print('done', OUT, f'{total:.1f}s')
