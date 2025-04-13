import os

from playwright.sync_api import Page, BrowserContext

class AtlassianLoginPage:
    def __init__(self, page: Page, context: BrowserContext, workspace: str):
        self.page = page
        self.context = context
        self.workspace = workspace

    @property
    def login_state(self):
        return self.page.locator('//nav/following-sibling::div//button[@name="sign-in"] | //nav/following-sibling::div//div[@data-testid="main-container"]')
    
    @property
    def signin_button(self):
        return self.page.locator('//nav/following-sibling::div//button[@name="sign-in"]')

    @property
    def email_input(self):
        return self.page.locator('#username')

    @property
    def password_input(self):
        return self.page.locator('#password')

    @property
    def continue_button(self):
        return self.page.locator('#login-submit')
    
    @property
    def login_button(self):
        return self.page.locator('#login-submit')
    
    @property
    def user_logo(self):
        return self.page.locator('//img[@alt="Account"]')

    @property
    def success_login_img(self):
        return self.page.locator('[data-testid="profile-button"]')

    def is_success_login_img_visible(self):
        self.success_login_img.wait_for(timeout=10000, state="visible")
        return self.success_login_img.is_visible()
    
    def goto(self):
        self.page.goto(f'https://bitbucket.org/{self.workspace}/workspace/overview/')


    def login(self, username: str, password: str):
        self.goto()

        if self.is_success_login_img_visible():
            return

        self.login_state.wait_for()
        self.signin_button.click()

        if self.is_success_login_img_visible():
            return
        
        self.email_input.fill(username)
        self.continue_button.click()
        self.password_input.fill(password)
        self.login_button.click()

        self.success_login_img.wait_for()
        self.context.storage_state(path="browser-context.json")
