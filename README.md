# Website Error Crawler (React / JS)

A spider that opens every page of your website in a **real browser**, so it sees what your users see, and reports everything that is broken. A normal HTML crawler fails on React sites because the page is empty until JavaScript runs. This one uses **Playwright** to run your JavaScript first.

---

## What it checks

| Issue type | What it means |
|---|---|
| `HTTP 404`, `HTTP 500`, etc. | A page, API call, image, script, or CSS file returned an error |
| `REQUEST FAILED` | A request never finished (network error, blocked, CORS) |
| `JS CONSOLE ERROR` | Something logged `console.error` in the browser |
| `JS EXCEPTION` | Uncaught JavaScript error (the red errors in DevTools) |
| `BLANK PAGE` | The page loaded but shows almost nothing (typical React crash) |
| `SOFT 404` | The URL returns 200 but the page says "page not found" |
| `BROKEN IMAGE` | An image tag failed to load |
| `IMG MISSING ALT` | Image has no alt text (accessibility) |
| `MISSING TITLE` | The page has no `<title>` |
| `SLOW PAGE` | Page took longer than your limit to load |
| `TIMEOUT` | Page did not load in time |
| `BROKEN EXTERNAL LINK` | A link to another website is dead |
| `UNREACHABLE LINK` | An external link could not be reached at all |

---

## Requirements

- Python 3.9 or newer
- Playwright (installs its own Chromium browser)

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

---

## Files

- [crawler.py](file:///crawler.py): The main crawler script.
- [save_login.py](file:///save_login.py): Utility to capture authenticated sessions for pages behind login.
- [requirements.txt](file:///requirements.txt): Python dependencies.

---

## How to run

1. Make sure your site is running. For local testing, start your dev server first (for example `npm start`) and use `http://localhost:3000` as `START_URL`.
2. Edit `START_URL` and settings in [crawler.py](file:///crawler.py):
   - `HEADLESS = False`: Shows the real Chromium browser window on your screen.
   - `VIEW_DELAY = 5`: Keeps each page visible for 5 seconds so you can watch what it crawls.
   - `KEEP_BROWSER_OPEN = True`: Keeps the browser open at the end until you press Enter.
3. Run:
   ```bash
   python crawler.py
   ```
4. Open `crawl_report.csv` in Excel or Google Sheets.
5. Use the `found_on` column to see which page contains the problem, then fix it there.

---

## Reading the report

Each row has four columns:

- **type**: what kind of problem it is
- **url**: the broken thing (a page, image, API endpoint, or link)
- **detail**: extra info such as the status code or error message
- **found_on**: the page where the crawler noticed it

Tip: sort by `type` first, then fix the most serious ones (`JS EXCEPTION`, `BLANK PAGE`, `HTTP 500`) before the small ones (`IMG MISSING ALT`).

---

## Important limitations

- **Only follows real links.** React pages reached only by clicking a button (not an `<a>` tag) will not be found. Add those URLs to `EXTRA_PAGES`.
- **No login by default.** Pages behind a login are skipped unless you add a saved session (`auth.json`).
- **Soft 404 detection is a guess.** It looks for phrases in `NOT_FOUND_PHRASES`. Change them to match your own "not found" page.
- **External sites may block bots.** Status codes 401, 403, 429, and 999 are ignored on purpose because they usually mean "blocked", not "broken".
- **Hash routing** (`/#/about`) is not followed because the fragment is removed. Add those routes to `EXTRA_PAGES` with the `#` removed, or switch your router to normal paths.

---

## Optional upgrades

### Crawl pages behind a login

Log in once and save the session using [save_login.py](file:///save_login.py):

```bash
python save_login.py
```

Then in [crawler.py](file:///crawler.py), change context initialization:

```python
context = browser.new_context(storage_state="auth.json")
```

> **Warning:** Do not commit or share `auth.json`; it contains your login session cookies and tokens.

### Seed pages from your sitemap

If your site has `/sitemap.xml`, paste its URLs into `EXTRA_PAGES` so the crawler also tests pages that nothing links to.

### Test on a phone-sized screen

Replace the context line with:

```python
context = browser.new_context(**p.devices["iPhone 13"])
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `playwright: command not found` | Run `python -m playwright install chromium` |
| Every page shows `BLANK PAGE` | Your dev server may not be running, or the app crashes on load. Open the URL in your browser and check DevTools. |
| Too many `TIMEOUT` rows | Increase `NAV_TIMEOUT_MS` or lower `MAX_PAGES` |
| Crawler never ends | Lower `MAX_PAGES`. Sites with endless filters or calendars generate unlimited URLs. |
| Same error repeated on every page | That is likely a shared component (header, footer, analytics script). Fix it once. |

---

## Good habits

- Only crawl websites you own or have permission to test.
- Keep `DELAY` above zero so you do not overload the server.
- Test against a staging or local copy first, not a live site under heavy traffic.
- Re-run the crawler after every deployment to catch new breakage.
