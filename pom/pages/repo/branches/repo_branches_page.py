from playwright.sync_api import Page

class RepoBranchesPage:
    def __init__(self, page: Page, workspace: str = None, repo: str = None):
        self.page = page
        self.workspace = workspace
        self.repo = repo

    @property
    def page_title(self):
        return self.page.locator("main h1")

    @property
    def view_source_button(self):
        return self.page.locator('//a[.//*[contains(text(), "View source")]]')

    def click_view_source_button(self):
        self.view_source_button.click()
