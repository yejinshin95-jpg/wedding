# 이석종 · 신예진 모바일 청첩장

정적 HTML 한 장(`index.html`)으로 동작합니다. 빌드 도구·의존성 없음 →
Vercel / GitHub Pages / Netlify 어디에나 그대로 올라갑니다.

**예식** 2026년 11월 14일 토요일 낮 12시 · 소피텔 앰배서더 서울 4층 그랜드 볼룸 방돔

## 구성

| # | 섹션 | 내용 |
|---|---|---|
| ① | 커버 | 액자 매트에 담은 메인 사진 + 인사말·일시·장소 / 신랑·신부 이름 2단 |
| ② | 결혼식에 초대합니다 | 신랑·신부 세로 사진, 혼주·생년월일·소개 3줄, 인사말 |
| ③ | 예식 안내 | 일시·장소 + 달력(예식일 강조) + D-day |
| ④ | 우리의 순간들 | 인생네컷 프리뷰(4장씩, 3초마다 크로스페이드·스와이프) → 탭하면 라이트박스 |
| ⑤ | 오시는 길 | 지도 + 주소 복사 + 2×2 교통 안내 + 네이버지도 / 티맵 |
| ⑥ | 예식 순서 | 식순 타임라인 |
| ⑦ | 안내사항 | 좌우 화살표로 한 장씩 넘겨 보는 캐러셀 (라인 드로잉 삽화 5종) |
| ⑧ | 마음 전하실 곳 | 신랑측·신부측 아코디언, 계좌 복사 |
| ⑨ | 연락하기 | 신랑·신부 각 3명(본인·아버지·어머니) 전화/문자 |

## 1. 정보 수정

`index.html` 스크립트 최상단 `CONFIG` **한 블록만** 고치면 됩니다.

| 항목 | 키 | 비고 |
|---|---|---|
| 신랑·신부 | `groom`, `bride` | `rel`을 장남/차녀 등으로 수정, `late:true` → 이름 앞 `故` |
| 연락처 | `.tel`, `.father.tel`, `.mother.tel` | **`0000`이 남아 있으면 버튼이 자동으로 비활성** 표시됩니다 |
| 예식 일시 | `wedding` | ISO 형식. 요일·표기·공유 문구가 자동 계산됩니다 |
| 예식장 | `venue` | `mapImage` 교체 시 지도 이미지 변경 (현재 소피텔 공식 약도) |
| 교통 | `venue.ways` | `**추천**` → 진사색 강조, `verify:true` → 「확인」 표시 |
| 식순 | `timeline` | 3개 초과 시 아이콘이 순환 재사용됩니다 |
| 안내사항 | `guide` | 카드 1장 = `{title, art, photo, desc}`. `photo`가 있으면 사진이, 없으면 `art` 삽화가 표시됩니다 |
| 사진첩 장수 | `galleryCount` | `gallery`가 비었을 때 표시할 자리표시자 수 (현재 33) |
| 계좌 | `accounts` | |
| 사진 | `cover`, `groom.photo`, `bride.photo`, `gallery` | |
| 배경음악 | `bgm` | 비우면 음악 버튼이 숨겨집니다 |

인사말 문구는 `<div class="greet">` 안의 텍스트를 직접 수정합니다.

## 2. 반드시 확인 후 교체할 항목

현재 값은 **자리표시자이거나 미확인 정보**입니다.

- [x] 혼주 성함 — 이범령 · 정미자 / 신호철 · 임선형
- [x] 계좌 6개 — 기존 청첩장과 동일하게 입력 완료
- [x] 교통편 — 지하철 · 버스 · 주차 · 홀 도착방법 입력 완료
- [x] 연락처 6개 — 신랑·신부 및 양가 부모님
- [x] 약도 — 소피텔 공식 약도(`photos/map.jpg`)
- [x] 식순 — 11:00 식장 오픈 / 12:00 1부 / 12:45 2부 · 식사
- [x] 식사(웨스턴 코스 요약), ATM 위치(지하 1층)
- [x] 커버 · 사진첩 28장
- [x] 신랑·신부 독사진
- [ ] (선택) 안내사항 실제 현장 사진 5장 — 없으면 삽화가 표시됩니다
- [ ] **셔틀버스** — 운행 여부·시간. 화면에 붉은 「확인」 표시 중
- [ ] (선택) 삽화를 기성 일러스트로 교체 — Freepik·Pngtree 등에서 받아 `guide[].photo` 에 연결
- [ ] 예식장 주소 `서울특별시 송파구 잠실로 209` — 예식장 안내문과 한 번 대조
- [ ] `<meta property="og:*">` 3줄
- [ ] 상단 미리보기 배너 `<div class="notice">` 블록 삭제

## 3. 사진 넣기

사진을 `photos/` 에 넣고 `CONFIG` 를 수정합니다.

```js
cover: "photos/main.jpg",
groom: { ..., photo: "photos/groom.jpg" },
bride: { ..., photo: "photos/bride.jpg" },
gallery: ["photos/01.jpg", "photos/02.jpg", /* … 30장 */]
```

### 안내사항 삽화

사진이 없을 때는 코드로 그린 라인 드로잉이 표시됩니다.
`art` 값으로 5종 중 선택합니다 — `elevator` · `car` · `dining` · `atm` · `wreath`.
선에 미세한 흔들림(`wob`)과 해칭 음영(`hatch`)을 넣어 손그림 느낌을 냈습니다.
실제 현장 사진(가로 16:11 권장)을 `guide[].photo` 에 넣으면 사진이 우선합니다.

### 사진 추가·교체

현재 `photos/01.jpg` ~ `33.jpg` 가 들어가 있습니다 (`20.jpg`, `26.jpg` 는 삭제).
`01.jpg` 는 **커버 전용**이라 사진첩(`gallery`)에서는 제외했고, 사진첩은 28장(7페이지 × 4컷)입니다.
신랑·신부 독사진은 `photos/groom.jpg`, `photos/bride.jpg`,
푸터 배경은 `photos/foot.jpg` 입니다.
사진을 더 넣으려면 같은 규칙으로 파일을 두고 `CONFIG.gallery` 배열에 경로를 추가합니다.
저장소 용량을 위해 가로 860px(커버 1000px), JPEG 품질 76~84로 리사이즈해 두었습니다.
가로 사진은 사진첩에서 잘려 보이지만, 탭해서 크게 보면 전체가 표시됩니다.

신랑·신부 독사진은 `groom.photo` / `bride.photo` 에 경로를 넣으면 소개 섹션에 반영됩니다.

권장 규격

| 위치 | 비율 | 크기 |
|---|---|---|
| 메인(커버) | 3:4 세로 | 가로 1000px 내외 · 하단이 배경으로 페이드되므로 인물은 상단~중앙에 |
| 신랑·신부 | 3:4 세로 | 가로 800px 내외 |
| 사진첩 | 3:4 세로 | 가로 1200px 이하, 장당 300KB 이하 |

`gallery`가 비어 있으면 `galleryCount`(기본 30) 만큼 자리표시자가 표시됩니다.

## 로딩 속도에 관하여

저장소의 `index.html` 은 사진을 `photos/` 의 **개별 파일로 참조**합니다.
Vercel·GitHub Pages에 올리면 브라우저가 첫 화면에 필요한 사진만 먼저 받고
나머지는 `loading="lazy"` 로 스크롤할 때 받으므로 첫 화면이 빠르게 뜹니다.

반면 미리보기용 Artifact는 **HTML 한 장**이라 사진을 base64로 본문에 심어야 하고,
그만큼 첫 로딩이 느립니다. 실제 배포본에서는 발생하지 않는 제약입니다.

## 4. 배포

### Vercel (`*.vercel.app` 주소)

1. [vercel.com](https://vercel.com) 가입 → **Continue with GitHub**
2. [vercel.com/new](https://vercel.com/new) → `mobile-letter` 저장소 **Import**
3. Framework Preset **Other**, Build Command·Output Directory 모두 비움 → **Deploy**
4. Settings → Git → **Production Branch** 를 `claude/mobile-invitation-claude-code-ttc4ph` 로 지정
   (기본값 `main` 브랜치가 아직 없기 때문입니다)
5. Settings → Domains → 주소를 원하는 이름으로 변경
6. `index.html` 의 `og:url`, `og:image` 두 줄을 확정된 주소로 교체 → push

`vercel.json` 이 사진에 1년 캐시를 걸어두어 재방문 시 즉시 뜹니다.

### GitHub Pages
Settings → Pages → Source `Deploy from a branch` → 브랜치 선택, 폴더 `/ (root)`

## 5. 선택 기능 연결

### 카카오맵 실제 지도
[카카오 개발자센터](https://developers.kakao.com)에서 JavaScript 키 발급 + 사이트 도메인 등록 후 `</body>` 앞에 추가합니다.

```html
<script src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=발급받은키"></script>
<script>
  const c = new kakao.maps.LatLng(CONFIG.venue.lat, CONFIG.venue.lng);
  const map = new kakao.maps.Map(document.getElementById("map"), { center: c, level: 3 });
  new kakao.maps.Marker({ map, position: c });
</script>
```

### 카카오톡 공유 (썸네일 카드)
현재 `공유하기` 버튼은 브라우저 기본 공유(Web Share API)를 쓰고, 미지원 시 문구를 복사합니다.
카카오톡 전용 카드가 필요하면:

```html
<script src="https://t1.kakaocdn.net/kakao_js_sdk/2.7.2/kakao.min.js"></script>
<script>
  Kakao.init("발급받은키");
  document.getElementById("shareKakao").onclick = () => Kakao.Share.sendDefault({
    objectType: "feed",
    content: {
      title: "이석종 · 신예진 결혼합니다",
      description: "2026년 11월 14일 토요일 낮 12시 · 소피텔 앰배서더 서울",
      imageUrl: location.origin + "/photos/main.jpg",
      link: { mobileWebUrl: location.href, webUrl: location.href }
    },
    buttons: [{ title: "청첩장 보기", link: { mobileWebUrl: location.href, webUrl: location.href } }]
  });
</script>
```

## 6. 디자인 토큰

청화백자(靑華白磁) 계열. 색을 바꾸려면 `:root` 변수만 수정하면 전체에 반영됩니다.

| 토큰 | 값 | 역할 |
|---|---|---|
| `--porcelain` | `#F1F1EC` | 한지 바탕 |
| `--ink` | `#1A2530` | 먹 (본문) |
| `--indigo` | `#2C4A6B` | 청화 (제목 강조·문양) |
| `--celadon` | `#8CA89A` | 청자 (영문 라벨·대나무) |
| `--jinsa` | `#A5564A` | 진사 (손글씨·시각 표시) |

서체 — 고운바탕(제목) / IBM Plex Sans KR(본문) / Cormorant Garamond(영문·숫자)

## 카카오톡 공유 (피드 카드)

`공유하기` 버튼은 카카오 JavaScript 키가 있으면 **사진 + 제목 + 일시·장소 + [청첩장 보기][위치 보기]** 카드로 보냅니다.
키가 비어 있으면 기존처럼 기기 기본 공유창을 씁니다.

1. [developers.kakao.com](https://developers.kakao.com) → 내 애플리케이션 → 앱 추가 (앱 이름·아이콘이 카드 하단에 표시됨)
2. 플랫폼 → Web → 사이트 도메인에 `https://seokjong-yejin.vercel.app` 등록
3. 앱 키 → **JavaScript 키**를 `CONFIG.kakao.key`에 입력
4. 카드 사진은 `CONFIG.kakao.image` (절대 URL), 문구는 `#shareKakao` 핸들러에서 수정
