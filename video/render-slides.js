// slides.html 의 장면(.s)마다 배경과 등장 요소(data-step)를 따로 PNG로 저장합니다.
//   slides/NN_bg.png      : 요소를 모두 숨긴 배경
//   slides/NN_LL.png      : 요소 하나만 보이는 투명 레이어 (1920×1080)
//   slides/list.json      : 장면 길이, 레이어 순서(step)·효과(fx)·종류, 레이스 위치
// 사용: node video/render-slides.js
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const out = path.join(__dirname, 'slides'); fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + path.join(__dirname, 'slides.html'), { waitUntil: 'networkidle' });
  await p.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
  const secs = await p.$$('section.s'); const list = [];
  for (const [i, el] of secs.entries()) {
    const nn = String(i).padStart(2, '0');
    // 배경: 등장 요소 숨김
    await el.evaluate(s => s.querySelectorAll('[data-step]').forEach(e => e.style.visibility = 'hidden'));
    await el.screenshot({ path: path.join(out, nn + '_bg.png') });
    const n = await el.evaluate(s => s.querySelectorAll('[data-step]').length);
    const layers = [];
    for (let k = 0; k < n; k++) {
      const info = await el.evaluate((s, k) => {
        document.documentElement.style.background = document.body.style.background = 'transparent';
        if (!('bg' in s.dataset)) s.dataset.bg = s.style.background; s.style.background = 'transparent';
        s.querySelectorAll('*').forEach(e => e.style.visibility = 'hidden');
        const t = s.querySelectorAll('[data-step]')[k];
        t.style.visibility = 'visible'; t.querySelectorAll('*').forEach(e => e.style.visibility = 'visible');
        return { step: +t.dataset.step, fx: t.dataset.fx || 'fade', kind: t.tagName === 'IMG' ? 'img' : 'text', lace: t.classList.contains('lace'), src: t.getAttribute('src'), pos: Number(t.dataset.pos || 0.5),
          rect: (r => ({ x: Math.round(r.left - s.getBoundingClientRect().left), y: Math.round(r.top - s.getBoundingClientRect().top), w: Math.round(r.width), h: Math.round(r.height) }))(t.getBoundingClientRect()) };
      }, k);
      const file = `${nn}_${String(k).padStart(2, '0')}.png`;
      await el.screenshot({ path: path.join(out, file), omitBackground: true });
      layers.push({ file, ...info });
    }
    // 원래대로
    await el.evaluate(s => { s.style.background = s.dataset.bg; document.documentElement.style.background = document.body.style.background = '';
      s.querySelectorAll('*').forEach(e => e.style.visibility = ''); });
    const lace = await el.evaluate(sec => { const i = sec.querySelector('img.lace'); if (!i) return null;
      const a = sec.getBoundingClientRect(), r = i.getBoundingClientRect(); return { x: r.left - a.left, y: r.top - a.top, w: r.width, h: r.height }; });
    await el.screenshot({ path: path.join(out, nn + '_full.png') });   // 확인용 완성 화면
    list.push({ bg: nn + '_bg.png', full: nn + '_full.png', sec: Number(await el.getAttribute('data-sec')), lace, layers });
  }
  fs.writeFileSync(path.join(out, 'list.json'), JSON.stringify(list, null, 1));
  console.log(list.length + ' scenes, ' + list.reduce((a, s) => a + s.layers.length, 0) + ' layers'); await b.close();
})();
