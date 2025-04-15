import os
from playwright.sync_api import Page, BrowserContext
from utils.logger import get_logger

logger = get_logger(__name__)

class AtlassianLoginPage:
    """Represents the Atlassian login page."""

    def __init__(self, page: Page, context: BrowserContext, workspace: str):
        """Initialize the login page with the Playwright page, context, and workspace."""
        self.page = page
        self.context = context
        self.workspace = workspace

    @property
    def login_state(self):
        """Locator for the login state element."""
        return self.page.locator('//nav/following-sibling::div//button[@name="sign-in"] | //nav/following-sibling::div//div[@data-testid="main-container"]')

    @property
    def signin_button(self):
        """Locator for the sign-in button."""
        return self.page.locator('//nav/following-sibling::div//button[@name="sign-in"]')

    @property
    def email_input(self):
        """Locator for the email input field."""
        return self.page.locator('#username')

    @property
    def password_input(self):
        """Locator for the password input field."""
        return self.page.locator('#password')

    @property
    def continue_button(self):
        """Locator for the continue button."""
        return self.page.locator('#login-submit')

    @property
    def login_button(self):
        """Locator for the login button."""
        return self.page.locator('#login-submit')

    @property
    def user_logo(self):
        """Locator for the user logo."""
        return self.page.locator('//img[@alt="Account"]')

    @property
    def success_login_img(self):
        """Locator for the success login image."""
        return self.page.locator('[data-testid="profile-button"]')

    def is_success_login_img_visible(self):
        """Check if the success login image is visible."""
        logger.info("Waiting for the success login image to become visible.")
        self.success_login_img.wait_for(timeout=10000, state="visible")
        visible = self.success_login_img.is_visible()
        logger.info(f"Success login image visibility: {visible}")
        return visible

    def goto(self):
        """Navigate to the workspace overview page."""
        logger.info(f"Navigating to the workspace overview page for workspace: {self.workspace}")
        self.page.goto(f'https://bitbucket.org/{self.workspace}/workspace/overview/')
        logger.info("Navigation to the workspace overview page completed.")

    def login(self, username: str, password: str, save_state: bool = True):
        """Perform login with the provided username and password."""
        logger.info("Starting login process.")
        self.goto()

        if save_state:
            logger.info("Checking if the user is already logged in.")
            if self.is_success_login_img_visible():
                logger.info("User is already logged in.")
                return

            logger.info("Waiting for the login state and clicking the sign-in button.")
            self.login_state.wait_for()
            self.signin_button.click()

            if self.is_success_login_img_visible():
                logger.info("User logged in successfully after clicking sign-in.")
                return

        logger.info("Filling in the email and password fields.")
        self.email_input.fill(username)
        self.continue_button.click()
        self.password_input.fill(password)
        self.login_button.click()

        logger.info("Waiting for the success login image after login.")
        self.success_login_img.wait_for()

        if save_state:
            logger.info("Saving the browser context state.")
            self.context.storage_state(path="browser-context.json")
        logger.info("Login process completed.")
