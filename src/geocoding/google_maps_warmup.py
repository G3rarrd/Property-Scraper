class GoogleMapsWarmup:
    def __init__(self, browser_manager):
        self.browser = browser_manager

    async def run(self):
        context = await self.browser.new_context()
        page = await context.new_page()
        
        url : str = "https://www.google.com/maps"

        await page.goto(url, wait_until="domcontentloaded")

        if "consent" in page.url:
            try:
                await page.click("button:has-text('Accept all')")
            except:
                pass

        await self.browser.save_session(context)
        await context.close()