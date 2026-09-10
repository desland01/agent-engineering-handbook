/*
 * Rendered check (T4): scrollbars and horizontal overflow.
 * Pure Node + puppeteer; serves public/ itself on an ephemeral port.
 * Optional: run via build/check.sh after `cd build && npm install`.
 */
'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const ROOT = path.resolve(__dirname, '..', 'public');
const PORT = 0; // ephemeral

const PAGES = [
  'index.html',
  'ideas.html',
  'guides.html',
  'skills.html',
  'investigations.html',
  'evidence.html',
  'guides/01-recurring-failures.html',
  'skills/agent-feedback-engineering/index.html',
  'ideas/01-ci-feedback-loop.html',
];

const VIEWPORTS = [{ width: 390, height: 844 }, { width: 1440, height: 900 }];

const HUBS = ['ideas.html', 'guides.html', 'skills.html', 'investigations.html', 'evidence.html'];

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.json': 'application/json',
  '.md': 'text/plain; charset=utf-8',
  '.yml': 'text/plain; charset=utf-8',
};

function serve(root) {
  return new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      const urlPath = decodeURIComponent(new URL(req.url, 'http://x').pathname);
      let filePath = path.normalize(path.join(root, urlPath));
      if (!filePath.startsWith(root)) {
        res.writeHead(403);
        return res.end('forbidden');
      }
      fs.stat(filePath, (err, st) => {
        if (!err && st.isDirectory()) filePath = path.join(filePath, 'index.html');
        fs.readFile(filePath, (err2, data) => {
          if (err2) {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            return res.end('not found: ' + urlPath);
          }
          const ext = path.extname(filePath).toLowerCase();
          res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
          res.end(data);
        });
      });
    });
    server.on('error', reject);
    server.listen(PORT, '127.0.0.1', () => resolve(server));
  });
}

// Runs in the page: returns overflow/scrollbar findings for one document.
function inspectPage() {
  const problems = [];
  const doc = document.documentElement;
  if (doc.scrollWidth > window.innerWidth) {
    problems.push(
      'horizontal overflow — documentElement.scrollWidth ' +
        doc.scrollWidth + ' > innerWidth ' + window.innerWidth
    );
  }
  const all = document.querySelectorAll('*');
  for (const el of all) {
    const cs = getComputedStyle(el);
    const ox = cs.overflowX;
    const oy = cs.overflowY;
    const scrollsX = (ox === 'auto' || ox === 'scroll') && el.scrollWidth > el.clientWidth;
    const scrollsY = (oy === 'auto' || oy === 'scroll') && el.scrollHeight > el.clientHeight;
    if (!scrollsX && !scrollsY) continue;
    if (cs.scrollbarWidth && cs.scrollbarWidth !== 'none') {
      problems.push(
        'scrollbar chrome — <' + el.tagName.toLowerCase() +
          (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).join('.') : '') +
          '> computed scrollbar-width: ' + cs.scrollbarWidth
      );
    }
    const bs = cs.borderLeftWidth || '0';
    const be = cs.borderRightWidth || '0';
    const bt = cs.borderTopWidth || '0';
    const bb = cs.borderBottomWidth || '0';
    const borderX = (parseFloat(bs) || 0) + (parseFloat(be) || 0);
    const borderY = (parseFloat(bt) || 0) + (parseFloat(bb) || 0);
    if (scrollsX && el.offsetWidth - el.clientWidth - borderX !== 0) {
      problems.push(
        'scrollbar chrome — <' + el.tagName.toLowerCase() + '> takes ' +
          (el.offsetWidth - el.clientWidth - borderX) + 'px horizontal gutter'
      );
    }
    if (scrollsY && el.offsetHeight - el.clientHeight - borderY !== 0) {
      problems.push(
        'scrollbar chrome — <' + el.tagName.toLowerCase() + '> takes ' +
          (el.offsetHeight - el.clientHeight - borderY) + 'px vertical gutter'
      );
    }
  }
  return problems;
}

// Runs in the page: counts links inside .hub-next.
function countHubNext() {
  const el = document.querySelector('.hub-next');
  if (!el) return { present: false, links: 0 };
  return { present: true, links: el.querySelectorAll('a[href]').length };
}

async function main() {
  const failures = [];
  let checks = 0;
  const server = await serve(ROOT);
  const port = server.address().port;
  let browser;
  try {
    browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
    for (const pagePath of PAGES) {
      for (const vp of VIEWPORTS) {
        const page = await browser.newPage();
        const consoleErrors = [];
        const badResponses = [];
        page.on('console', (msg) => {
          if (msg.type() === 'error') consoleErrors.push(msg.text());
        });
        page.on('response', (res) => {
          if (res.status() >= 400) badResponses.push(res.status() + ' ' + res.url());
        });
        try {
          await page.setViewport({ width: vp.width, height: vp.height });
          await page.goto('http://127.0.0.1:' + port + '/' + pagePath, {
            waitUntil: 'networkidle0',
            timeout: 15000,
          });
          await page.evaluate(() => document.fonts ? document.fonts.ready : null);
        } catch (err) {
          failures.push(pagePath + ' @' + vp.width + ': navigation — ' + err.message);
          await page.close();
          continue;
        }

        checks++;
        const problems = await page.evaluate(inspectPage);
        for (const p of problems) failures.push(pagePath + ' @' + vp.width + ': ' + p);

        checks++;
        if (HUBS.includes(pagePath)) {
          const hub = await page.evaluate(countHubNext);
          if (!hub.present) {
            failures.push(pagePath + ' @' + vp.width + ': hub-next — no .hub-next element found');
          } else if (hub.links < 2) {
            failures.push(pagePath + ' @' + vp.width + ': hub-next — only ' + hub.links + ' link(s)');
          }
        }

        checks++;
        // Scroll capture: a vertical wheel over a horizontal region must still
        // move the page. Measured 0px on four regions before the per-axis fix.
        for (const sel of ['.ideas-row', '.track-row', '.table-scroll', '.reader pre']) {
          const box = await page.evaluate((s) => {
            const el = document.querySelector(s); if (!el) return null;
            document.documentElement.style.scrollBehavior = 'auto';
            const r = el.getBoundingClientRect(); window.scrollTo(0, Math.max(0, r.top + window.scrollY - 200));
            const q = el.getBoundingClientRect(); return {x: q.left + q.width / 2, y: q.top + q.height / 2, before: window.scrollY};
          }, sel);
          if (!box) continue;
          await page.mouse.move(box.x, box.y); await page.mouse.wheel({deltaY: 300});
          await new Promise((r) => setTimeout(r, 200));
          const after = await page.evaluate(() => window.scrollY);
          if (after - box.before < 50) failures.push(pagePath + ' @' + vp.width + ': scroll capture — ' + sel + ' swallows the vertical wheel (page moved ' + (after - box.before) + 'px)');
        }
        // Reveal: after scrolling the whole page, nothing may remain hidden.
        const stuck = await page.evaluate(async () => {
          // The site scrolls smoothly; a harness must not depend on where an
          // animation happens to be when it retargets. Scroll instantly, in
          // half-viewport steps so every element is fully inside the observer's
          // root at some stop, and give the observer a frame at each.
          document.documentElement.style.scrollBehavior = 'auto';
          const step = Math.max(1, Math.floor(window.innerHeight / 2));
          const max = document.documentElement.scrollHeight;
          for (let y = 0; y <= max; y += step) {
            window.scrollTo(0, y);
            await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
          }
          await new Promise((r) => setTimeout(r, 700));
          const left = Array.from(document.querySelectorAll('.reveal-pending'));
          return left.slice(0, 3).map((el) => el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).trim().split(/\s+/).join('.') : ''))
            .concat(left.length > 3 ? ['+' + (left.length - 3) + ' more'] : []);
        });
        if (stuck.length) {
          failures.push(pagePath + ' @' + vp.width + ': reveal — ' + stuck.length + ' element(s) never revealed: ' + stuck.join(', '));
        }
        if (consoleErrors.length) {
          failures.push(pagePath + ' @' + vp.width + ': console — ' + consoleErrors.join(' | '));
        }

        checks++;
        if (badResponses.length) {
          failures.push(pagePath + ' @' + vp.width + ': failed request — ' + badResponses.join(' | '));
        }

        await page.close();
      }
    }
  } finally {
    if (browser) await browser.close().catch(() => {});
    server.close();
  }

  if (failures.length) {
    for (const f of failures) console.log('FAIL ' + f);
  }
  const status = failures.length === 0 ? 'PASS' : 'FAIL';
  console.log(
    status + ': ' + PAGES.length + ' pages x ' + VIEWPORTS.length + ' viewports, ' +
      checks + ' rendered checks, ' + failures.length + ' failure(s)'
  );
  process.exit(failures.length ? 1 : 0);
}

main().catch((err) => {
  console.error('rendered check crashed: ' + (err && err.stack || err));
  process.exit(1);
});
