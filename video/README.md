# 식장 스크린용 사진 슬라이드 영상

- 1920×1080 (16:9), 30fps, 무음 (라이브 연주), 약 1분 22초
- 배경색 `#F5F5F5`(모든 장면 공통), 화면 가장자리에 붙지 않은 사진에는 인화지 같은 테두리(`#E6E7E2`, 사진 폭의 2.8%) — `slides.html` 의 `--bg`, `--frame`, `img.frame`
- 첫 화면 레이스는 바탕을 투명하게 바꾼 `derived/main-lace.png` 사용 (새 배경색 위에 네모 자국이 남지 않도록)
- 글꼴: 모바일 청첩장과 같음 — Pinyon Script(필기체) · Montserrat(영문 대문자) · Noto Sans KR(본문)
- 장면당 6초, 장면 사이 1.5초 크로스페이드 (확대 효과 없음). 스티커는 쓰지 않음
- 장면 안의 사진·글은 하나씩 나타남: 페이드 인(글은 살짝 떠오름), 필기체는 왼쪽부터 써지듯
- 첫 화면은 모바일 청첩장 첫 화면 그대로(레이스 액자 사진 `main.jpg`), 레이스 위에 은은한 반짝임 효과
- 완성된 첫 화면으로 시작해 같은 첫 화면으로 끝남(반짝임 타이밍까지 이어짐) → 반복 재생해도 끊김 없음
- 사진: 사진첩 11장(g01·g02·g06·g08·g15 제외) + 추가 사진 5장. 신랑 소개 g11·g14, 신부 소개 g04·g09, 가로 사진 g05는 화면 꽉 채움
- **추가 사진 5장(`video/local-photos/set03-a.jpg`, `set05-a.jpg`, `set05-b.jpg`, `set06-a.jpg`, `set09-a.jpg`)은 이 저장소가 공개라서 올리지 않았습니다.** 다시 렌더링하려면 이 파일들을 그 위치에 넣어 주세요

| # | 장면 | 사진 | 문구 |
|---|---|---|---|
| 1 | 첫 화면 (레이스 + 반짝임, 처음부터 완성된 화면) | main.jpg | Wedding Invitation · Yejin · Seokjong |
| 2 | 신랑 소개 (사진 · 이름 · 사진) | g11, g14 | Groom · 이석종 · LEE SEOKJONG |
| 3 | 신부 소개 | set06-a*, g09 | Bride · 신예진 · SHIN YEJIN |
| 4 | 엇갈린 높이의 두 장 | set03-a*, g03 | (없음) |
| 5 | 인화 사진 세 장 나란히 | A-1*, A-2*, A-3* | (없음) |
| 6 | 흑백 가로 사진 꽉 채우기 (천천히 위로) | g05 | (없음) |
| 7 | 두 장 세트 | set05-a*, set05-b* | (없음) |
| 8 | 위 제목 + 아래 사진 두 장 | set06-b*, g07 | Just as we are |
| 9 | 디테일 4컷 (흑백·컬러 번갈아) | D-1* ~ D-4* | Little moments |
| 10 | 오른쪽 한 장 | g10 | Always on your side · 평생 서로의 편이 되어 |
| 11 | 컬러 가로 사진 꽉 채우기 (천천히 위로) | C-1* | (없음) |
| 12 | 흩어진 인화 사진 | B-3* (나머지 두 장은 대체 사진 대기) | Our days |
| 13 | 큰 사진 + 작은 사진 | g13, g12 | Through five seasons · 다섯 해의 계절을 지나 · with you |
| 14 | 반반 꽉 채우기 (천천히 위로) | E-1b*, E-2* | (없음) |
| 15 | 가운데 큰 사진 | F-1* | Forever |
| 16 | 두 장 + 아래 문구 | set09-a*, g16 | 저희의 새로운 시작을 함께 축복해 주세요 · A new beginning |
| 17 | 감사 인사 | — | Thank you · 함께해 주셔서 감사합니다 |
| — | 첫 화면 (영상 첫 프레임과 같은 화면으로 끝남 → 반복 재생 시 끊김 없음) | | |

`*` 표시 사진은 `video/local-photos/` 에만 있고 저장소에는 올리지 않았습니다 (이 저장소가 공개라서). 다시 렌더링하려면 같은 이름으로 그 폴더에 넣어 주세요.

## 다시 만들기
```bash
node video/render-slides.js
python3 video/render-video.py
```
결과: `video/wedding-slideshow.mp4` (용량 때문에 저장소에는 올리지 않음)
렌더링은 약 5분 걸립니다.

- 문구·배치·사진: `slides.html` 에서 고칩니다. 장면 길이는 각 `<section data-sec="초">`, 나타나는 순서는 `data-step`, 써지는 효과는 `data-fx="write"`.
- 꽉 찬 사진이 올라가는 거리: `render-video.py` 의 `PAN_PX` (지금 50px), 적용할 사진은 `slides.html` 에서 `data-fx="pan"`
- 나타나는 속도: `render-video.py` 의 `START_DELAY`, `STEP_GAP`, `FADE_IN`, `RISE`, `WRITE_BASE`, `WRITE_PX_PER_SEC`.
- 전환 속도·마지막 첫 화면 길이: `render-video.py` 의 `FADE_SEC`, `END_SEC`.
- 반짝임 양·크기·속도·색: `render-video.py` 의 `SPARKLE_ON_SCREEN`, `SPARKLE_SIZE`, `SPARKLE_LIFE`, `SPARKLE_COLOR`, `GLOW_COLOR`.
- 한 장면 미리보기: `python3 video/render-video.py --still 장면번호 초 미리보기.png` (예: `--still 1 1.9 out.png`)
