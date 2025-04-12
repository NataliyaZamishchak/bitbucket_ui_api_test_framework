import json
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

BITBUCKET_USERNAME = os.getenv("BITBUCKET_USERNAME")
BITBUCKET_PASSWORD = os.getenv("BITBUCKET_PASSWORD")
BITBUCKET_ORGANIZATION_NAME = os.getenv("BITBUCKET_ORGANIZATION_NAME")
BITBUCKET_LOGIN_URL = "https://bitbucket.org/test1_nz/workspace/repositories/"


class TokenRetriever:
    def __init__(self):
        self.token = None

    def _navigate_to_bitbucket_login(self, page):
        print("Navigating to Bitbucket login page...")
        page.goto("https://bitbucket.org/account/signin/")
        page.locator("#username").fill("")
        page.locator("#username").fill(BITBUCKET_USERNAME)
        page.locator("#login-submit").click()
        page.locator("#password").fill(BITBUCKET_PASSWORD)
        page.locator("#login-submit").click()
    
    def _wait_for_login(self, page):
        try:
            page.wait_for_selector('[data-testid="profile-button"]', timeout=180_000)
            print("Successfully logged into Bitbucket.")
        except Exception as e:
            print(f"Login failed or timeout occurred: {str(e)}")
            raise Exception("Login failed or timeout occurred")
    
    def _extract_token_from_cookies(self, context):
        print("Extracting cookies...")
        cookies = context.cookies()
        for cookie in cookies:
            if cookie["name"] == "cloud.session.token":
                print("Token found in cookies.")
                return cookie["value"]
        print("Token not found in cookies.")
        return None

    def get_bearer_token(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            self._navigate_to_bitbucket_login(page)
            self._wait_for_login(page)
            
            page.wait_for_timeout(3000)
            print("Navigating to workspace overview page...")
            page.goto(f"https://bitbucket.org/{BITBUCKET_ORGANIZATION_NAME}/workspace/overview/")
            page.wait_for_timeout(3000)

            self.token = self._extract_token_from_cookies(context)

            browser.close()
            return self.token
        
# if __name__ == "__main__":
#     retriever = TokenRetriever()
#     token = retriever.get_bearer_token()
#     print("Bearer token:", token)