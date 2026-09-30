import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 720})

        file_path = "file://" + os.path.abspath("CommanderAndController.html")
        await page.goto(file_path)

        # Start single player
        await page.click('button:has-text("Single Player")')
        await page.wait_for_timeout(1000)

        # Spawn tank
        await page.evaluate("() => buyUnit('tank', 1)")
        await page.wait_for_timeout(500)

        # Select tank
        await page.evaluate("() => { selectedUnit = units.find(u => u.owner === 1 && u.key === 'tank'); }")
        await page.wait_for_timeout(500)

        # Enter FPS mode
        await page.click('#fps-btn')
        await page.wait_for_timeout(500)

        # Record initial position & yaw
        pos_before = await page.evaluate("() => ({ x: fpsUnit.x, y: fpsUnit.y, yaw: fpsYaw, currX: touchControls.stickCurrX, currY: touchControls.stickCurrY })")
        print("Before movement:", pos_before)

        # Dispatch touchstart and touchmove to simulate dragging touch joystick up & sideways
        await page.evaluate("""() => {
            const touchStart = new Touch({ identifier: 1, target: document.body, clientX: 100, clientY: 500 });
            const eventStart = new TouchEvent('touchstart', { touches: [touchStart], targetTouches: [touchStart], changedTouches: [touchStart], cancelable: true });
            document.dispatchEvent(eventStart);

            const touchMove = new Touch({ identifier: 1, target: document.body, clientX: 180, clientY: 460 });
            const eventMove = new TouchEvent('touchmove', { touches: [touchMove], targetTouches: [touchMove], changedTouches: [touchMove], cancelable: true });
            document.dispatchEvent(eventMove);
        }""")

        await page.wait_for_timeout(500)

        pos_after = await page.evaluate("() => ({ x: fpsUnit.x, y: fpsUnit.y, yaw: fpsYaw, currX: touchControls.stickCurrX, currY: touchControls.stickCurrY, baseX: touchControls.stickBaseX })")
        print("After movement:", pos_after)

        await page.screenshot(path="joystick_fwd_back_only.png")
        print("Saved joystick_fwd_back_only.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
