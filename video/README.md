# 식장 스크린용 사진 슬라이드 영상

- 1920×1080 (16:9), 30fps, 무음 (라이브 연주)
- 구성: 표지 8초 → 사진첩 16장(세로 사진은 두 장씩 나란히, 가로 사진은 한 장 · 장면당 8초 · 1.5초 크로스페이드 · 확대 효과 없음) → 표지 10초 (총 75초)
- 처음과 끝이 같은 표지라 반복 재생해도 끊김 없이 이어집니다
- 표지: 모바일 청첩장 첫 화면(Wedding Invitation · 사진 · 날짜/시간)과 커버(WEDDING DAY. · 이름 · 일시/장소)를 나란히 배치. 스티커·레이스 액자는 쓰지 않음
- 사진 순서: 청첩장 `CONFIG.gallery` 와 같음 (g01-v2 … g16-v2, 7번은 g07-v4)

## 다시 만들기
```bash
node video/render-cover.js
python3 video/render-video.py
```
결과: `video/wedding-slideshow.mp4` (용량이 커서 저장소에는 올리지 않음)

길이·전환 속도는 `render-video.py` 맨 위 `COVER_SEC`, `PHOTO_SEC`, `END_SEC`, `FADE_SEC`, `GAP` 으로 바꿉니다.
