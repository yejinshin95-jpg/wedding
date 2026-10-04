/**
 * 석종 · 예진 청첩장 — 참석 여부(RSVP) 받기
 *
 * 사용법
 * 1) 구글 시트를 새로 만들고, 메뉴 [확장 프로그램] → [Apps Script] 를 엽니다.
 * 2) 기본 코드를 모두 지우고 이 파일 내용을 붙여넣은 뒤 저장합니다.
 * 3) [배포] → [새 배포] → 유형 '웹 앱'
 *      - 다음 사용자 인증 정보로 실행: 나
 *      - 액세스 권한이 있는 사용자: 모든 사용자
 *    → [배포] 후 권한 승인, 나오는 '웹 앱 URL'(…/exec)을 복사합니다.
 * 4) 그 URL을 index.html 의 CONFIG.rsvpUrl 에 넣습니다.
 */
const SHEET_NAME = 'RSVP';
const HEADERS = ['제출 시각', '구분', '참석 여부', '성함', '인원'];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.tryLock(10000);
  try {
    const d = JSON.parse(e.postData.contents || '{}');
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
    if (sh.getLastRow() === 0) sh.appendRow(HEADERS);
    const clean = v => String(v == null ? '' : v).slice(0, 40).replace(/^[=+\-@]/, "'$&"); // 수식 주입 방지
    sh.appendRow([new Date(), clean(d.side), clean(d.attend), clean(d.name), Number(d.count) || 0]);
    return ContentService.createTextOutput('ok');
  } finally {
    lock.releaseLock();
  }
}

/* 브라우저에서 URL을 열었을 때 동작 확인용 */
function doGet() {
  return ContentService.createTextOutput('RSVP endpoint is running');
}
