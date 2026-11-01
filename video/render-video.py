"""식장 스크린용 사진 슬라이드 영상 (1920×1080, 30fps, 무음).
구성: 표지 → 사진첩 16장(한 장씩, 천천히 확대 + 크로스페이드) → 표지. 처음과 끝이 표지라 반복 재생해도 자연스럽습니다.
사용: node video/render-cover.js && python3 video/render-video.py   (결과: video/wedding-slideshow.mp4)
"""
import subprocess, sys, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PH = os.path.join(HERE, '..', 'photos')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'wedding-slideshow.mp4')

W, H, FPS = 1920, 1080, 30
BG = (0xEF, 0xED, 0xE8)          # 청첩장 바탕색 --porcelain
COVER_SEC, PHOTO_SEC, END_SEC = 8, 7, 10   # 각 장면 길이(초, 전환 포함)
FADE_SEC = 1.5                   # 크로스페이드 길이
ZOOM = 0.04                      # 한 장면 동안 4% 천천히 확대
PHOTO_H = 960                    # 사진 높이 (위아래 60px 여백)
PHOTO_MAX_W = 1600               # 가로 사진 최대 폭

# 청첩장 CONFIG.gallery 와 같은 순서
GALLERY = ["g01-v2", "g02-v2", "g03-v2", "g04-v2", "g05-v2", "g06-v2", "g07-v4", "g08-v2",
           "g09-v2", "g10-v2", "g11-v2", "g12-v2", "g13-v2", "g14-v2", "g15-v2", "g16-v2"]

def prep_photo(path):
    im = Image.open(path).convert('RGB')
    s = min(PHOTO_H / im.height, PHOTO_MAX_W / im.width)
    # 확대 끝 크기까지 미리 줄여 두면 매 프레임 변환이 깨끗합니다
    s *= 1 + ZOOM
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)

def frame_photo(im, t):
    """t: 0~1 장면 진행도. 사진을 화면 가운데에 (1→1+ZOOM) 배율로."""
    scale = (1 + ZOOM * t) / (1 + ZOOM)
    w, h = im.width * scale, im.height * scale
    x0, y0 = (W - w) / 2, (H - h) / 2
    # 출력 좌표 → 원본 좌표 (역변환), 소수점 위치까지 부드럽게
    return im.transform((W, H), Image.AFFINE, (1 / scale, 0, -x0 / scale, 0, 1 / scale, -y0 / scale),
                        resample=Image.BICUBIC, fillcolor=BG)

cover = Image.open(os.path.join(HERE, 'cover.png')).convert('RGB')
scenes = [('cover', COVER_SEC, None)] + [('photo', PHOTO_SEC, prep_photo(os.path.join(PH, g + '.jpg'))) for g in GALLERY] + [('cover', END_SEC, None)]

# 장면 시작 시각 (전환 구간만큼 겹침)
starts, t = [], 0.0
for i, (_, dur, _) in enumerate(scenes):
    starts.append(t); t += dur - (FADE_SEC if i < len(scenes) - 1 else 0)
total = t
nframes = round(total * FPS)

def render(i, sec):
    kind, dur, im = scenes[i]
    if kind == 'cover': return cover
    return frame_photo(im, min(1, max(0, (sec - starts[i]) / dur)))

ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-tune', 'film', '-movflags', '+faststart', OUT],
                      stdin=subprocess.PIPE)
for f in range(nframes):
    sec = f / FPS
    cur = max(i for i in range(len(scenes)) if starts[i] <= sec)
    img = render(cur, sec)
    # 앞 장면과 겹치는 처음 FADE_SEC 동안은 앞 장면에서 서서히 넘어옴
    if cur > 0 and sec < starts[cur] + FADE_SEC:
        a = (sec - starts[cur]) / FADE_SEC
        a = a * a * (3 - 2 * a)  # 부드러운 가감속
        img = Image.blend(render(cur - 1, sec), img, a)
    ff.stdin.write(img.tobytes())
    if f % (FPS * 10) == 0: print(f'{sec:5.1f}s / {total:.1f}s', flush=True)
ff.stdin.close(); ff.wait()
print('done', OUT, f'{total:.1f}s')
