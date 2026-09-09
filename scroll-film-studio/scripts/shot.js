/* shot.js — deterministic headless screenshot + canvas probe.
 * Usage: node shot.js <url> <out.png> <width> <height> <scrollFraction>
 * Needs puppeteer-core (npm i puppeteer-core) and a local Chrome.
 * Prints the canvas centre pixel: three different colours across three scroll
 * positions proves the film is genuinely scrubbing. A black capture with a 0-size
 * viewport means the pane is hidden, not that the page is broken.
 */
const puppeteer = require('puppeteer-core');
const CHROME = process.env.CHROME_PATH ||
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
(async () => {
  const [url, out, w = 1440, h = 900, pct = 0] = process.argv.slice(2);
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox'] });
  const p = await b.newPage();
  await p.setViewport({ width: +w, height: +h, deviceScaleFactor: 1 });
  await p.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });
  await p.evaluate((f) => window.scrollTo(0, Math.round(document.body.scrollHeight * f)), +pct);
  await new Promise((r) => setTimeout(r, 3500));
  const px = await p.evaluate(() => {
    const c = document.querySelector('canvas');
    if (!c) return 'no canvas';
    if (!c.width) return 'ZERO-SIZE VIEWPORT — pane hidden, not a page bug';
    const d = c.getContext('2d').getImageData(c.width / 2, c.height / 2, 1, 1).data;
    return [d[0], d[1], d[2]].join(',');
  });
  await p.screenshot({ path: out });
  console.log(out, '| viewport', w + 'x' + h, '| scroll', pct, '| canvas centre rgb:', px);
  await b.close();
})();
