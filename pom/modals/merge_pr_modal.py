from playwright.sync_api import Page

class MergePrModal:
    def __init__(self, page: Page):
        self.page = page

    @property
    def merge_button(self):
        return self.page.locator('//button[.//*[@data-qa="merge-dialog-merge-button"]]')

    def click_merge_button(self):
        self.merge_button.click()
        self.page.wait_for_selector('//h2[text()="Merged pull request"]')