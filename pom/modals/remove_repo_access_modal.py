from playwright.sync_api import Page

class RemoveRepoAccessModal:
    def __init__(self, page: Page):
        self.page = page

    @property
    def modal_title(self):
        return self.page.locator('//span[contains(@id, "modal-dialog-title")]')

    @property
    def remove_button(self):
        return self.page.locator('[data-testid="remove-access-modal--remove-btn"]')

    def click_remove_button(self):
        self.remove_button.click()
        self.page.wait_for_selector('[role="alert"] h2 span')