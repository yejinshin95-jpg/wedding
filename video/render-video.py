"""식장 스크린용 사진 슬라이드 영상 (1920×1080, 30fps, 무음).
구성: 표지 → 사진첩 16장(세로 사진은 두 장씩 나란히, 가로 사진은 한 장) → 표지.
처음과 끝이 표지라 반복 재생해도 자연스럽습니다. 사진은 움직이지 않고 크로스페이드로만 넘어갑니다.
사용: node video/render-cover.js && python3 video/render-video.py   (결과: video/wedding-slideshow.mp4)
"""
import subprocess, sys, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PH = os.path.join(HERE, '..', 'photos')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'wedding-slideshow.mp4')

W, H, FPS = 1920, 1080, 30
BG = (0xEF, 0xED, 0xE8)          # 청첩장 바탕색 --porcelain
COVER_SEC, PHOTO_SEC, END_SEC = 8, 8, 10   # 각 장면 길이(초, 전환 포함)
FADE_SEC = 1.5                   # 크로스페이드 길이
PHOTO_H = 960                    # 사진 높이 (위아래 60px 여백)
GAP = 40                         # 나란히 놓은 두 사진 사이 간격
LAND_MAX_W = 1600                # 가로 사진 최대 폭

# 청첩장 CONFIG.gallery 와 같은 순서. 세로 사진은 순서대로 두 장씩 묶고, 가로 사진은 한 장으로 둡니다.
GALLERY = ["g01-v2", "g02-v2", "g03-v2", "g04-v2", "g05-v2", "g06-v2", "g07-v4", "g08-v2",
           "g09-v2", "g10-v2", "g11-v2", "g12-v2", "g13-v2", "g14-v2", "g15-v2", "g16-v2"]

def load(name):
    return Image.open(os.path.join(PH, name + '.jpg')).convert('RGB')

def fit(im, h, max_w=None):
    s = h / im.height
    if max_w: s = min(s, max_w / im.width)
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)

def slide(names):
    canvas = Image.new('RGB', (W, H), BG)
    ims = [load(n) for n in names]
    if len(ims) == 1:
        im = fit(ims[0], PHOTO_H, LAND_MAX_W)
        canvas.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
    else:
        a, b = (fit(im, PHOTO_H) for im in ims)
        canvas.paste(a, (W // 2 - GAP // 2 - a.width, (H - a.height) // 2))   # 가운데 기준 왼쪽
        canvas.paste(b, (W // 2 + GAP // 2, (H - b.height) // 2))            # 가운데 기준 오른쪽
    return canvas

# 장면 묶기
groups, pending = [], []
for n in GALLERY:
    im = Image.open(os.path.join(PH, n + '.jpg'))
    if im.width > im.height:                  # 가로 사진: 한 장
        if pending: groups.append(pending); pending = []
        groups.append([n])
    else:
        pending.append(n)
        if len(pending) == 2: groups.append(pending); pending = []
if pending: groups.append(pending)            # 남은 세로 사진 한 장
print('장면:', groups)

cover = Image.open(os.path.join(HERE, 'cover.png')).convert('RGB')
scenes = [(cover, COVER_SEC)] + [(slide(g), PHOTO_SEC) for g in groups] + [(cover, END_SEC)]

starts, t = [], 0.0
for i, (_, dur) in enumerate(scenes):
    starts.append(t); t += dur - (FADE_SEC if i < len(scenes) - 1 else 0)
total = t

ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-tune', 'stillimage', '-movflags', '+faststart', OUT],
                      stdin=subprocess.PIPE)
raw = [s.tobytes() for s, _ in scenes]
for f in range(round(total * FPS)):
    sec = f / FPS
    cur = max(i for i in range(len(scenes)) if starts[i] <= sec)
    if cur > 0 and sec < starts[cur] + FADE_SEC:      # 앞 장면에서 서서히 넘어옴
        a = (sec - starts[cur]) / FADE_SEC
        a = a * a * (3 - 2 * a)
        ff.stdin.write(Image.blend(scenes[cur - 1][0], scenes[cur][0], a).tobytes())
    else:
        ff.stdin.write(raw[cur])
ff.stdin.close(); ff.wait()
print('done', OUT, f'{total:.1f}s')
