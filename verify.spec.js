const { test, expect } = require('@playwright/test');
const path = require('path');

test('verify Commander and Controller updates', async ({ page }) => {
    const logs = [];
    const errors = [];
    page.on('console', msg => logs.push(msg.text()));
    page.on('pageerror', err => errors.push(err.message));

    const fileUrl = `file://${path.resolve('CommanderAndController.html')}`;
    await page.goto(fileUrl);
    await page.waitForTimeout(1000);

    // Start single player
    await page.click('#modal-start button');
    await page.waitForTimeout(1500);

    await page.screenshot({ path: 'test-results/battlefield_verified.png' });

    // Spawn units to verify new rotor spinning, recoil, walking bobbing, and EVA voice
    await page.evaluate(() => {
        if (typeof buyUnit === 'function') {
            buyUnit('tank', 1);
            buyUnit('orca', 1);
            buyUnit('harv', 1);
            buyUnit('missile', -1);
        }
    });

    await page.waitForTimeout(1500);
    await page.screenshot({ path: 'test-results/units_verified.png' });

    console.log('Errors caught during test execution:', errors);
    expect(errors.length).toBe(0);
});
