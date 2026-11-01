"""식장 스크린용 사진 슬라이드 영상 (1920×1080, 30fps, 무음).
slides/ 의 장면을 순서대로 크로스페이드로 잇고, 마지막에 표지(00)로 돌아갑니다 → 반복 재생해도 자연스러움.
사용: node video/render-slides.js && python3 video/render-video.py   (결과: video/wedding-slideshow.mp4)
"""
import subprocess, sys, os, json
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SL = os.path.join(HERE, 'slides')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'wedding-slideshow.mp4')
W, H, FPS = 1920, 1080, 30
FADE_SEC = 1.5      # 크로스페이드 길이
END_SEC = 10        # 마지막 표지 길이

lst = json.load(open(os.path.join(SL, 'list.json')))
scenes = [(Image.open(os.path.join(SL, s['file'])).convert('RGB'), s['sec']) for s in lst]
scenes.append((scenes[0][0], END_SEC))

starts, t = [], 0.0
for i, (_, dur) in enumerate(scenes):
    starts.append(t); t += dur - (FADE_SEC if i < len(scenes) - 1 else 0)
total = t

ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-tune', 'stillimage', '-movflags', '+faststart', OUT],
                      stdin=subprocess.PIPE)
raw = [im.tobytes() for im, _ in scenes]
for f in range(round(total * FPS)):
    sec = f / FPS
    cur = max(i for i in range(len(scenes)) if starts[i] <= sec)
    if cur > 0 and sec < starts[cur] + FADE_SEC:
        a = (sec - starts[cur]) / FADE_SEC
        a = a * a * (3 - 2 * a)
        ff.stdin.write(Image.blend(scenes[cur - 1][0], scenes[cur][0], a).tobytes())
    else:
        ff.stdin.write(raw[cur])
ff.stdin.close(); ff.wait()
print('done', OUT, f'{total:.1f}s')
