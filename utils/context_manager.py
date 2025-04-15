import os
from dotenv import load_dotenv
from utils.logger import get_logger

logger = get_logger(__name__)
load_dotenv()

CONTEXT_FILE = "playwright_context.json"

def save_context(context):
    """Save browser context to file."""
    context.storage_state(path=CONTEXT_FILE)
    logger.info("Browser context saved to file.")

def load_or_login_context(playwright, username_1, password_1):
    """Load saved context if available, otherwise perform login and save it."""
    browser = playwright.chromium.launch(headless=False)
    if os.path.exists(CONTEXT_FILE):
        logger.info("Loading existing browser context.")
        context = browser.new_context(storage_state=CONTEXT_FILE)
    else:
        logger.info("Logging in and creating new browser context.")
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://bitbucket.org/account/signin/")
        page.fill("#username", username_1)
        page.click("#login-submit")
        page.fill("#password", password_1)
        page.click("#login-submit")
        page.wait_for_selector('[data-testid="profile-button"]', timeout=120_000)
        save_context(context)
    return context
