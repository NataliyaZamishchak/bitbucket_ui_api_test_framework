from playwright.sync_api import Page

class RepoCreatePrPage:
    def __init__(self, page: Page, workspace: str = None, repo: str = None):
        self.page = page
        self.workspace = workspace
        self.repo = repo

    @property
    def page_title(self):
        return self.page.locator("main h1")

    @property
    def create_pr_button(self):
        return self.page.locator('[data-testid="create-PR-button"]')

    def click_create_pr_button(self):
        return self.create_pr_button.click()
