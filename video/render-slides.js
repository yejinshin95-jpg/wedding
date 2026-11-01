// slides.html 의 장면(.s)을 하나씩 1920×1080 PNG로 저장 → slides/NN.png, slides/list.json(장면 길이)
// 사용: node video/render-slides.js
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const out = path.join(__dirname, 'slides'); fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + path.join(__dirname, 'slides.html'), { waitUntil: 'networkidle' });
  await p.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
  const list = [];
  for (const [i, el] of (await p.$$('section.s')).entries()) {
    const file = String(i).padStart(2, '0') + '.png';
    await el.screenshot({ path: path.join(out, file) });
    // 레이스 사진이 있는 장면은 반짝임 위치 계산용으로 화면 속 위치를 같이 기록
    const lace = await el.evaluate(sec => { const i = sec.querySelector('img.lace'); if (!i) return null;
      const a = sec.getBoundingClientRect(), b = i.getBoundingClientRect(); return { x: b.left - a.left, y: b.top - a.top, w: b.width, h: b.height }; });
    list.push({ file, sec: Number(await el.getAttribute('data-sec')), lace });
  }
  fs.writeFileSync(path.join(out, 'list.json'), JSON.stringify(list, null, 1));
  console.log(list.length + ' slides'); await b.close();
})();
