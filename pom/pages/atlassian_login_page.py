from playwright.sync_api import Page, BrowserContext

class AtlassianLoginPage:
    def __init__(self, page: Page, context: BrowserContext):
        self.page = page
        self.context = context

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
        return self.page.locator('[data-testid="nav-profile-button--trigger"]')
    
    def goto(self):
        self.page.goto('https://atlassian.com/')
        self.login_state.wait_for()

    def login(self, username: str, password: str):
        self.goto()
        self.login_state.wait_for()
        self.signin_button.click()
        self.success_login_img.wait_for(timeout=5000)

        if self.success_login_img.is_visible():
            return
        
        self.email_input.fill(username)
        self.continue_button.click()
        self.password_input.fill(password)
        self.login_button.click()

        self.success_login_img.wait_for()
        self.context.storage_state(path="browser-context.json")
