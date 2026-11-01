# 식장 스크린용 사진 슬라이드 영상

- 1920×1080 (16:9), 30fps, 무음 (라이브 연주), 약 1분
- 글꼴: 모바일 청첩장과 같음 — Pinyon Script(필기체) · Montserrat(영문 대문자) · Noto Sans KR(본문)
- 장면당 6초, 1.5초 크로스페이드 (확대 효과 없음). 스티커는 쓰지 않음
- 첫 화면은 모바일 청첩장 첫 화면 그대로(레이스 액자 사진 `main.jpg`), 레이스 위에 은은한 반짝임 효과
- 처음과 끝이 같은 첫 화면이라 반복 재생해도 끊김 없이 이어집니다
- 사진첩 16장을 한 번씩 모두 사용 (신랑 소개 g11·g14, 신부 소개 g04·g09, 가로 사진 g05는 화면 꽉 채움)

| # | 장면 | 사진 | 문구 |
|---|---|---|---|
| 00 | 첫 화면 (레이스 + 반짝임) | main.jpg | Wedding Invitation · 2026.11.14 · 12:00 PM |
| 01 | 커버 | — | WEDDING DAY. · 이름 · 일시·장소 |
| 02 | 신랑 소개 (사진 · 이름 · 사진) | g11, g14 | Groom · 이석종 · LEE SEOKJONG |
| 03 | 신부 소개 | g04, g09 | Bride · 신예진 · SHIN YEJIN |
| 04 | 인사말 | g01 | 청첩장 인사말 (2021년 4월, …) |
| 05 | 가로 사진 꽉 채우기 | g05 | Our Moments · 우리의 순간들 |
| 06 | 세 장 나란히 | g02, g06, g08 | (없음) |
| 07 | 엇갈린 두 장 | g03, g07 | Just as we are · 있는 그대로를 사랑하며 |
| 08 | 오른쪽 한 장 | g10 | Always on your side · 평생 서로의 편이 되어 |
| 09 | 큰 사진 + 작은 사진 | g13, g12 | Through five seasons · 다섯 해의 계절을 지나 · with you |
| 10 | 두 장 + 아래 문구 | g15, g16 | 저희의 새로운 시작을 함께 축복해 주세요 · A new beginning |
| 11 | 감사 인사 | — | Thank you · 함께해 주셔서 감사합니다 |
| — | 첫 화면 (반복 연결) | | |

## 다시 만들기
```bash
node video/render-slides.js
python3 video/render-video.py
```
결과: `video/wedding-slideshow.mp4` (용량 때문에 저장소에는 올리지 않음)

- 문구·배치·사진: `slides.html` 에서 고칩니다. 장면 길이는 각 `<section data-sec="초">`.
- 전환 속도·마지막 첫 화면 길이: `render-video.py` 의 `FADE_SEC`, `END_SEC`.
- 반짝임 양·크기·속도·색: `render-video.py` 의 `SPARKLE_ON_SCREEN`, `SPARKLE_SIZE`, `SPARKLE_LIFE`, `SPARKLE_COLOR`, `GLOW_COLOR`.
- 반짝임 미리보기 한 장: `python3 video/render-video.py --still 2.3 미리보기.png`
