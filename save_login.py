"""Save authenticated session state for the crawler."""
# pyrefly: ignore[missing-import]
from playwright.sync_api import sync_playwright

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

def save_login(login_url="https://ojtrack.bscs4b.com/login", auth_file="auth.json"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=USER_AGENT)
        page = context.new_page()
        page.goto(login_url)
        input("Log in in the browser window, then press Enter here...")
        context.storage_state(path=auth_file)
        browser.close()
        print(f"Session saved to {auth_file}")

if __name__ == "__main__":
    save_login()
