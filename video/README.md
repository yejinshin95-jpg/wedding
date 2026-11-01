# 식장 스크린용 사진 슬라이드 영상

- 1920×1080 (16:9), 30fps, 무음 (라이브 연주), 약 1분 22초
- 글꼴: 모바일 청첩장과 같음 — Pinyon Script(필기체) · Montserrat(영문 대문자) · Noto Sans KR(본문)
- 장면마다 배치와 문구가 다르고, 1.5초 크로스페이드로 넘어갑니다 (확대 효과 없음). 스티커·레이스 액자는 쓰지 않음
- 처음과 끝이 같은 표지라 반복 재생해도 끊김 없이 이어집니다
- 사진첩 16장을 한 번씩 모두 사용 (신랑 소개 g11·g14, 신부 소개 g04·g09, 가로 사진 g05는 화면 꽉 채움)

| # | 장면 | 사진 | 문구 |
|---|---|---|---|
| 00 | 표지 (청첩장 첫 화면 + 커버) | 01 | Wedding Invitation · 이름 · 일시·장소 |
| 01 | 인사말 | g01 | 청첩장 인사말 |
| 02 | 신랑 소개 (사진 · 이름 · 사진) | g11, g14 | Groom · 이석종 · LEE SEOKJONG |
| 03 | 신부 소개 | g04, g09 | Bride · 신예진 · SHIN YEJIN |
| 04 | 가로 사진 꽉 채우기 | g05 | Our Moments · 우리의 순간들 |
| 05 | 세 장 나란히 | g02, g06, g08 | (없음) |
| 06 | 엇갈린 두 장 | g03, g07 | Just as we are · 있는 그대로를 사랑하며 |
| 07 | 오른쪽 한 장 | g10 | Always on your side · 평생 서로의 편이 되어 |
| 08 | 큰 사진 + 작은 사진 | g13, g12 | Through five seasons · 다섯 해의 계절을 지나 · with you |
| 09 | 두 장 + 아래 문구 | g15, g16 | 저희의 새로운 시작을 함께 축복해 주세요 · A new beginning |
| 10 | 감사 인사 | — | Thank you · 함께해 주셔서 감사합니다 |
| — | 표지 (10초) | | |

## 다시 만들기
```bash
node video/render-slides.js
python3 video/render-video.py
```
결과: `video/wedding-slideshow.mp4` (용량 때문에 저장소에는 올리지 않음)

- 문구·배치·사진: `slides.html` 에서 고칩니다. 장면 길이는 각 `<section data-sec="초">`.
- 전환 속도·마지막 표지 길이: `render-video.py` 의 `FADE_SEC`, `END_SEC`.
