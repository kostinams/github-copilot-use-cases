const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto('https://finance.yahoo.com/quote/MSFT/', {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });

  // Handle consent/cookie page if redirected
  if (page.url().includes('consent') || page.url().includes('guce')) {
    const selectors = [
      'button:has-text("Accept all")',
      'button:has-text("Accept All")',
      'button:has-text("I agree")',
      'button:has-text("Agree")',
      'input[type="submit"][value="agree"]',
      'form[action*="consent"] button[type="submit"]',
    ];
    for (const sel of selectors) {
      const el = page.locator(sel).first();
      if (await el.count()) {
        await el.click({ timeout: 5000 }).catch(() => {});
        break;
      }
    }
    await page.waitForLoadState('domcontentloaded', { timeout: 20000 }).catch(() => {});
  }

  // Wait for the price streamer to appear
  await page.waitForSelector(
    'fin-streamer[data-field="regularMarketPrice"]',
    { timeout: 30000 }
  );

  const price = await page
    .locator('fin-streamer[data-field="regularMarketPrice"]')
    .first()
    .innerText();

  let change = 'N/A';
  let pct = 'N/A';
  try {
    change = await page
      .locator('fin-streamer[data-field="regularMarketChange"]')
      .first()
      .innerText();
  } catch {}
  try {
    pct = await page
      .locator('fin-streamer[data-field="regularMarketChangePercent"]')
      .first()
      .innerText();
  } catch {}

  console.log('=== MSFT Stock Quote (Yahoo Finance) ===');
  console.log('Price:  ', price);
  console.log('Change: ', change);
  console.log('Change%:', pct);

  await browser.close();
})().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
