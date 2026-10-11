// Planner-owned acceptance. The builder receives this file read-only.
// Runs actual candidate sources. Mock tag transport proves bootstrap, not GA delivery.
import assert from 'node:assert/strict';
import { test, after } from 'node:test';
import { execFileSync, spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(process.env.HANDBOOK_CANDIDATE_ROOT || process.cwd());
const FIXTURE_ROOT = path.join(ROOT, '.scratch');
fs.mkdirSync(FIXTURE_ROOT, { recursive: true });
const SCRATCH = fs.mkdtempSync(path.join(FIXTURE_ROOT, 'handbook-consent-'));
after(() => fs.rmSync(SCRATCH, { recursive: true, force: true }));
const HOST = 'agent-engineering-handbook.dev';
const ORIGIN = `https://${HOST}`;
const GTM = 'GTM-TEST123';
const TOKEN = 'planner-public-verification-token';
const KEY = 'handbook.analytics.v1';
const DAY = 86400000;
const allow = '[data-analytics-choice="allow"]';
const decline = '[data-analytics-choice="decline"]';
const preferences = '[data-analytics-preferences]';
const CONFIG = { productionHostname: HOST, gtmId: GTM, verificationToken: TOKEN };

function fixture(config = CONFIG) {
  const root = fs.mkdtempSync(path.join(SCRATCH, 'discovery-consent-'));
  const excluded = ['.git', '.scratch', 'node_modules', '__pycache__', 'public'];
  for (const entry of fs.readdirSync(ROOT)) {
    if (excluded.includes(entry)) continue;
    fs.cpSync(path.join(ROOT, entry), path.join(root, entry), {
      recursive: true,
      filter(source) {
        return !path.relative(ROOT, source).split(path.sep).some(part => excluded.includes(part));
      },
    });
  }
  const configFile = path.join(root, 'build', 'analytics.json');
  if (config === null) fs.rmSync(configFile, { force: true });
  else fs.writeFileSync(configFile, JSON.stringify(config));
  const rendered = spawnSync('python3', ['build/render.py'], { cwd: root, encoding: 'utf8' });
  assert.equal(rendered.status, 0, `Candidate renderer failed: ${rendered.stdout}\n${rendered.stderr}`);
  return root;
}

const configured = fixture();
const unconfigured = fixture(null);
const publicRoot = path.join(configured, 'public');

function featurePresent(root = configured) {
  const html = fs.readFileSync(path.join(root, 'public', 'index.html'), 'utf8');
  assert.ok(html.includes('data-analytics-choice="allow"'), 'Generated page has no allow-analytics control');
  assert.ok(html.includes('data-analytics-choice="decline"'), 'Generated page has no decline-analytics control');
  assert.ok(html.includes('data-analytics-preferences'), 'Generated page has no footer preference control');
  assert.ok(fs.existsSync(path.join(root, 'public', 'privacy.html')), 'Generated privacy reader is missing');
}

// Python uses the project's parser family and stdlib XML, not HTML regexes.
test('crawler files contain exactly canonical indexable HTML routes', () => {
  assert.ok(fs.existsSync(path.join(publicRoot, 'sitemap.xml')), 'No generated sitemap.xml');
  assert.ok(fs.existsSync(path.join(publicRoot, 'robots.txt')), 'No generated robots.txt');
  execFileSync('python3', ['-I', '-c', `
import sys, pathlib, urllib.parse, xml.etree.ElementTree as ET
from html.parser import HTMLParser
root = pathlib.Path(sys.argv[1]); origin = sys.argv[2]
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.canonicals = []; self.noindex = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'link' and a.get('rel') == 'canonical': self.canonicals.append(a.get('href'))
        if tag == 'meta' and a.get('name', '').lower() == 'robots': self.noindex |= 'noindex' in a.get('content', '').lower()
expected = set()
pages = list(root.rglob('*.html'))
assert len(pages) == 34, f'Expected 34 physical HTML pages after privacy; got {len(pages)}'
for page in pages:
    parsed = Page(); parsed.feed(page.read_text())
    relative = page.relative_to(root).as_posix()
    if relative == '404.html':
        assert not parsed.canonicals, '404 must not advertise a canonical URL'
        continue
    assert len(parsed.canonicals) == 1, str(page)
    wanted = origin + ('/' if relative == 'index.html' else '/' + relative)
    assert parsed.canonicals[0] == wanted, (relative, parsed.canonicals)
    if not parsed.noindex: expected.add(wanted)
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
doc = ET.parse(root / 'sitemap.xml')
assert doc.getroot().tag == '{http://www.sitemaps.org/schemas/sitemap/0.9}urlset'
urls = [node.text for node in doc.findall('s:url/s:loc', ns)]
assert len(urls) == len(set(urls)), 'Duplicate sitemap URLs'
assert set(urls) == expected, (set(urls) - expected, expected - set(urls))
for url in urls:
    parsed = urllib.parse.urlsplit(url)
    assert parsed.scheme == 'https' and parsed.netloc == urllib.parse.urlsplit(origin).netloc
    assert not parsed.query and not parsed.fragment
    assert not parsed.path.endswith('.md') and 'vercel.app' not in url
robots = (root / 'robots.txt').read_text().lower()
assert 'user-agent: *' in robots
assert 'sitemap: ' + origin.lower() + '/sitemap.xml' in robots
assert not any(line.strip() == 'disallow: /' for line in robots.splitlines())
`, publicRoot, ORIGIN], { encoding: 'utf8' });
});

test('shared markup has verification, private preference controls and no remote embeds', () => {
  featurePresent();
  execFileSync('python3', ['-I', '-c', `
import sys, pathlib, urllib.parse
from html.parser import HTMLParser
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.tokens = []; self.privacy = []; self.network = []; self.allow = []; self.decline = []; self.prefs = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta' and a.get('name') == 'google-site-verification': self.tokens.append(a.get('content'))
        if tag == 'a' and urllib.parse.urlsplit(a.get('href', '')).path.endswith('privacy.html'): self.privacy.append(a['href'])
        if a.get('data-analytics-choice') == 'allow': self.allow.append(tag)
        if a.get('data-analytics-choice') == 'decline': self.decline.append(tag)
        if 'data-analytics-preferences' in a: self.prefs.append(tag)
        if tag in ('script', 'iframe', 'img', 'audio', 'video', 'source', 'link'):
            target = a.get('href') if tag == 'link' else a.get('src')
            if a.get('rel') != 'canonical' and target and (target.startswith(('http:', 'https:', '//'))): self.network.append(target)
for page in pathlib.Path(sys.argv[1]).rglob('*.html'):
    p = Page(); p.feed(page.read_text())
    assert p.tokens == [sys.argv[2]], (page, p.tokens)
    assert p.privacy, (page, 'privacy link missing')
    assert p.allow == ['button'] and p.decline == ['button'] and p.prefs == ['button'], (page, 'duplicate or wrong-role controls')
    assert not p.network, (page, p.network)
`, publicRoot, TOKEN], { encoding: 'utf8' });
});

test('malformed public configuration fails before replacing output', () => {
  for (const value of [
    { ...CONFIG, gtmId: 'GTM-TEST123&evil=1' },
    { ...CONFIG, gtmId: 'G-TEST123' },
    { ...CONFIG, productionHostname: `${HOST}.evil.example` },
    { ...CONFIG, productionHostname: `https://${HOST}` },
    { ...CONFIG, verificationToken: '"><script>alert(1)</script>' },
  ]) {
    const root = fixture();
    const marker = path.join(root, 'public', 'planner-preservation-marker.txt');
    fs.writeFileSync(marker, 'retain candidate output on invalid input');
    fs.writeFileSync(path.join(root, 'build', 'analytics.json'), JSON.stringify(value));
    const run = spawnSync('python3', ['build/render.py'], { cwd: root, encoding: 'utf8' });
    assert.notEqual(run.status, 0, `Malformed config was accepted: ${JSON.stringify(value)}`);
    assert.ok(fs.existsSync(marker), 'Invalid config replaced public output');
    assert.equal(fs.readFileSync(marker, 'utf8'), 'retain candidate output on invalid input');
  }
});

test('existing checker accepts candidate and still rejects unrelated remote scripts', () => {
  featurePresent();
  const run = () => spawnSync('python3', ['build/check.py'], { cwd: configured, encoding: 'utf8' });
  const before = run();
  assert.equal(before.status, 0, `Normal candidate check failed: ${before.stdout}\n${before.stderr}`);
  const file = path.join(publicRoot, 'index.html');
  const original = fs.readFileSync(file, 'utf8');
  try {
    fs.writeFileSync(file, original.replace('</head>', '<script src="https://unrelated.example/tracker.js"></script></head>'));
    const rejected = run();
    assert.notEqual(rejected.status, 0, 'Checker accepted an unrelated external script');
    assert.match(rejected.stdout + rejected.stderr, /network|unrelated\.example/i);
  } finally {
    fs.writeFileSync(file, original);
  }
});

async function browserCase(options, callback) {
  const root = options.root || configured;
  featurePresent(root); // Absent behavior is an assertion failure, not a browser-load error.
  const puppeteer = createRequire(path.join(process.env.HANDBOOK_PUPPETEER_ROOT || path.join(ROOT, 'build'), 'package.json'))('puppeteer');
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  const google = [];
  const remote = [];
  const errors = [];
  try {
    await page.setViewport(options.viewport || { width: 390, height: 844 });
    if (options.noJS) await page.setJavaScriptEnabled(false);
    page.on('pageerror', error => errors.push(error.message));
    await page.evaluateOnNewDocument((key, opts) => {
      if (opts.gpc) Object.defineProperty(Navigator.prototype, 'globalPrivacyControl', { configurable: true, get: () => true });
      if (opts.preference !== undefined) localStorage.setItem(key, opts.preference);
      if (opts.storageDenied) {
        Storage.prototype.getItem = function () { throw new DOMException('Storage denied', 'SecurityError'); };
        Storage.prototype.setItem = function () { throw new DOMException('Storage denied', 'SecurityError'); };
      }
    }, KEY, options);
    await page.setRequestInterception(true);
    page.on('request', request => {
      const url = new URL(request.url());
      if (!['http:', 'https:'].includes(url.protocol)) return void request.continue();
      if (url.hostname !== (options.hostname || HOST)) remote.push(request.url());
      if (/(^|\.)(googletagmanager|google-analytics|analytics\.google|doubleclick)\.(com|net)$/.test(url.hostname)) {
        google.push(request.url());
        if (!options.googleUnavailable && url.hostname === 'www.googletagmanager.com' && url.pathname === '/gtm.js' && url.searchParams.get('id') === GTM) {
          return void request.respond({ status: 200, contentType: 'application/javascript', body: 'window.__plannerContainerLoads = (window.__plannerContainerLoads || 0) + 1;' });
        }
        return void request.abort();
      }
      if (url.hostname !== (options.hostname || HOST)) return void request.abort();
      const relative = decodeURIComponent(url.pathname).replace(/^\/+/, '') || 'index.html';
      const file = path.resolve(root, 'public', relative);
      const base = path.join(root, 'public') + path.sep;
      if (!file.startsWith(base) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
        return void request.respond({ status: 404, contentType: 'text/plain', body: 'not found' });
      }
      const ext = path.extname(file);
      return void request.respond({ status: 200, contentType: ({ '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.json': 'application/json' })[ext] || 'application/octet-stream', body: fs.readFileSync(file) });
    });
    const hostname = options.hostname || HOST;
    await page.goto(`${hostname === 'localhost' ? 'http' : 'https'}://${hostname}/index.html?private=value#secret`, {
      waitUntil: 'load', referer: 'https://referrer.example/source?private=value#secret',
    });
    const settle = async () => new Promise(resolve => setTimeout(resolve, 250));
    await settle();
    await callback({ page, google, settle });
    assert.deepEqual(remote, google, 'Unexpected non-Google remote transmission');
    assert.deepEqual(errors, [], 'Reading/consent script raised a page error');
  } finally {
    await browser.close();
  }
}

const saved = (choice, decidedAt = Date.now()) => JSON.stringify({ choice, decidedAt });
const expectReading = async page => assert.ok(await page.$('main, #main'), 'Main reader is missing');

test('production starts without Google requests and equal keyboard-accessible choices', async () => {
  await browserCase({}, async ({ page, google }) => {
    await expectReading(page);
    assert.deepEqual(google, []);
    const styles = await page.evaluate((a, d) => [a, d].map(selector => {
      const b = document.querySelector(selector), s = getComputedStyle(b);
      return { tag: b.tagName, disabled: b.disabled, tabIndex: b.tabIndex, name: b.textContent.trim(), background: s.backgroundColor, color: s.color, font: s.fontSize, padding: s.padding };
    }), allow, decline);
    assert.equal(styles[0].tag, 'BUTTON');
    assert.equal(styles[1].tag, 'BUTTON');
    assert.ok(styles.every(s => !s.disabled && s.tabIndex >= 0 && s.name));
    for (const key of ['background', 'color', 'font', 'padding']) assert.equal(styles[0][key], styles[1][key], `Unequal choice emphasis: ${key}`);
  });
});

test('decline persists locally and sends nothing on reload', async () => {
  await browserCase({}, async ({ page, google, settle }) => {
    await page.focus(decline); await page.keyboard.press('Enter'); await settle();
    const value = await page.evaluate(key => JSON.parse(localStorage.getItem(key)), KEY);
    assert.equal(value.choice, 'decline'); assert.ok(Number.isFinite(value.decidedAt));
    await page.reload({ waitUntil: 'load' }); await settle();
    assert.deepEqual(google, []); await expectReading(page);
  });
});

test('allow bootstraps only GTM once and seeds sanitized data before it loads', async () => {
  await browserCase({}, async ({ page, google, settle }) => {
    await page.focus(allow); await page.keyboard.press('Enter'); await settle();
    assert.equal(google.length, 1);
    assert.equal(new URL(google[0]).searchParams.get('id'), GTM);
    const layer = await page.evaluate(() => (window.dataLayer || []).filter(value => value && typeof value === 'object' && !Array.isArray(value)));
    const sanitized = layer.find(value => value.page_location === `${ORIGIN}/index.html` && value.page_referrer === 'https://referrer.example');
    assert.ok(sanitized, 'Sanitized origin/path and referrer origin not seeded into dataLayer');
    assert.ok(JSON.stringify(layer).indexOf('private=value') === -1 && JSON.stringify(layer).indexOf('#secret') === -1);
    await page.addScriptTag({ content: fs.readFileSync(path.join(configured, 'public', 'assets', 'handbook.js'), 'utf8') });
    await settle(); assert.equal(google.length, 1, 'Duplicate initialization bootstrapped another container');
  });
});

test('valid saved allowance permits one container load per ordinary page load', async () => {
  await browserCase({ preference: saved('allow') }, async ({ page, google, settle }) => {
    assert.equal(google.length, 1);
    await page.reload({ waitUntil: 'load' }); await settle();
    assert.equal(google.length, 2);
  });
});

test('unavailable Google transport does not break reading or preference controls', async () => {
  await browserCase({ googleUnavailable: true }, async ({ page, google, settle }) => {
    await page.click(allow); await settle();
    assert.equal(google.length, 1); await expectReading(page);
    await page.click(preferences);
    assert.ok(await page.$(decline));
  });
});

for (const hostname of ['handbook-preview.vercel.app', 'localhost', `${HOST}.evil.example`]) {
  test(`saved allowance cannot collect on ${hostname}`, async () => {
    await browserCase({ hostname, preference: saved('allow') }, async ({ page, google }) => {
      await expectReading(page); assert.deepEqual(google, []);
    });
  });
}

test('Global Privacy Control overrides a saved allowance', async () => {
  await browserCase({ gpc: true, preference: saved('allow') }, async ({ page, google }) => {
    await expectReading(page); assert.deepEqual(google, []);
  });
});

for (const preference of ['not-json', saved('allow', Date.now() - 181 * DAY), saved('allow', Date.now() + DAY)]) {
  test('invalid, expired or future-dated allowance never implicitly persists', async () => {
    await browserCase({ preference }, async ({ page, google, settle }) => {
      assert.deepEqual(google, []);
      await page.click(allow); await settle();
      assert.equal(google.length, 1, 'Fresh explicit consent must still work');
      assert.equal(await page.evaluate(key => JSON.parse(localStorage.getItem(key)).choice, KEY), 'allow');
    });
  });
}

test('storage denial keeps reading and requires fresh explicit consent on reload', async () => {
  await browserCase({ storageDenied: true }, async ({ page, google, settle }) => {
    await expectReading(page); assert.deepEqual(google, []);
    await page.click(allow); await settle(); assert.equal(google.length, 1);
    await page.reload({ waitUntil: 'load' }); await settle(); assert.equal(google.length, 1);
  });
});

test('withdrawal denies future loads and removes accessible analytics cookies', async () => {
  await browserCase({}, async ({ page, google, settle }) => {
    await page.click(allow); await settle(); assert.equal(google.length, 1);
    await page.evaluate(() => { document.cookie = '_ga=planner-test; path=/'; document.cookie = '_ga_TEST123=planner-test; path=/'; });
    await page.click(preferences);
    await Promise.all([page.waitForNavigation({ waitUntil: 'load' }), page.click(decline)]);
    await settle(); assert.equal(google.length, 1, 'Withdrawal caused another Google request');
    const cookies = await page.evaluate(() => document.cookie);
    assert.ok(!/(?:^|;\s*)_ga(?:_|=)/.test(cookies), `Accessible analytics cookie remains: ${cookies}`);
    assert.equal(await page.evaluate(key => JSON.parse(localStorage.getItem(key)).choice, KEY), 'decline');
    await expectReading(page);
  });
});

test('unconfigured analytics stays disabled without breaking reading', async () => {
  await browserCase({ root: unconfigured }, async ({ page, google, settle }) => {
    await expectReading(page);
    const visible = await page.$eval(allow, b => !b.hidden && !b.disabled && b.getBoundingClientRect().width > 0);
    if (visible) await page.click(allow);
    await settle(); assert.deepEqual(google, []);
  });
});

test('privacy and reading remain reachable with JavaScript disabled', async () => {
  await browserCase({ noJS: true }, async ({ page, google }) => {
    await expectReading(page);
    const href = await page.$eval('a[href$="privacy.html"]', a => a.href);
    const response = await page.goto(href, { waitUntil: 'load' });
    assert.equal(response.status(), 200); await expectReading(page); assert.deepEqual(google, []);
    assert.ok(await page.$('h1'));
  });
});

test('maintainer links preserve source credits and use the confirmed contextual targets', () => {
  const source = fs.readFileSync(path.join(configured, 'ATTRIBUTION.md'), 'utf8');
  assert.ok(source.includes('https://grovestreetpainting.com/about'), 'Confirmed maintainer link to Grove Street Painting is missing');
  assert.ok(source.includes('https://constance.digital/'), 'Confirmed related-work link to Constance is missing');
  execFileSync('python3', ['-I', '-c', `
import sys, pathlib, hashlib
from html.parser import HTMLParser
root = pathlib.Path(sys.argv[1])
source = (root / 'ATTRIBUTION.md').read_text()
intro, separator, tail = source.partition('## Screenshots\\n')
assert separator, 'Existing attribution sections were removed'
credit_end = intro.find('the \\x60sandbox-runtime\\x60 fork.')
assert credit_end >= 0, 'Original cited-engineer list was changed'
credit_end += len('the \\x60sandbox-runtime\\x60 fork.')
assert hashlib.sha256(intro[:credit_end].rstrip().encode()).hexdigest() == '0fd978d20a32bdb3d8fa592ba7ed9910ab399fef49a752335733bc73f04002f4', 'Original credit prefix changed'
assert hashlib.sha256((separator + tail).encode()).hexdigest() == '0db2b4a829cb50c63368a28e4088bb099ee97a809ee5d14f269207ee36789941', 'Unrelated attribution sections changed'
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.paragraph = None; self.anchor = None; self.paragraphs = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'p': self.paragraph = {'text': '', 'links': []}
        if tag == 'a' and self.paragraph is not None: self.anchor = {'href': a.get('href', ''), 'text': ''}
    def handle_data(self, data):
        if self.paragraph is not None: self.paragraph['text'] += data
        if self.anchor is not None: self.anchor['text'] += data
    def handle_endtag(self, tag):
        if tag == 'a' and self.anchor is not None:
            self.paragraph['links'].append(self.anchor); self.anchor = None
        if tag == 'p' and self.paragraph is not None:
            self.paragraphs.append(self.paragraph); self.paragraph = None
page = Page(); page.feed((root / 'public/ATTRIBUTION.html').read_text())
wanted = [('https://grovestreetpainting.com/about', 'Grove Street Painting'), ('https://constance.digital/', 'Constance')]
related = [p for p in page.paragraphs if any(a['href'] == wanted[0][0] for a in p['links'])]
assert len(related) == 1, 'One contextual maintainer paragraph is required'
paragraph = related[0]
actual = [(a['href'], a['text'].strip()) for a in paragraph['links']]
assert actual == wanted, ('Wrong related-work links or duplicate anchors', actual)
assert any(word in paragraph['text'].lower() for word in ['owner', 'maintainer', 'maintained']), 'Maintainer relationship must be explicit'
assert any(word in paragraph['text'].lower() for word in ['independent', 'separate', 'related']), 'Related work must not be presented as a cited source'
`, configured], { encoding: 'utf8' });
});

// No test here claims actual pageviews, Google verification or live publication.
// Those remain separately authorized account/production integration readbacks.
