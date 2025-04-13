import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
load_dotenv()

CONTEXT_FILE = "playwright_context.json"

def save_context(context):
    context.storage_state(path=CONTEXT_FILE)

def load_or_login_context(playwright):
    browser = playwright.chromium.launch(headless=False)
    if os.path.exists(CONTEXT_FILE):
        context = browser.new_context(storage_state=CONTEXT_FILE)
    else:
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://bitbucket.org/account/signin/")
        page.fill("#username", os.getenv("BITBUCKET_USERNAME"))
        page.click("#login-submit")
        page.fill("#password", os.getenv("BITBUCKET_PASSWORD"))
        page.click("#login-submit")
        page.wait_for_selector('[data-testid="profile-button"]', timeout=120_000)
        save_context(context)
    return context
