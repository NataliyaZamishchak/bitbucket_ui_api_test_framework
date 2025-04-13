from playwright.sync_api import Page

class CommitChangesModal:
    def __init__(self, page: Page):
        self.page = page

    @property
    def commit_button(self):
        return self.page.locator('.dialog-button-panel .commit-button')

    def click_commit_button(self):
        self.commit_button.click()
        self.page.wait_for_selector('[aria-label="Global comments"]')