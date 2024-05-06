from playwright.sync_api import sync_playwright

def InitSession():
    with sync_playwright() as play:
        browser = play.chromium.connect_over_cdp("http://localhost:9222")
        default_context = browser.contexts[0]
        page = default_context.pages[0]
        storage = page.context.storage_state(path="state.json")
        return storage


if __name__ == "__main__":
    InitSession()