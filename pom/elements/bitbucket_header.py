from playwright.sync_api import Locator


class BitbucketHeader:
    def __init__(self, base_locator: Locator):
        self.baseLocator = base_locator

    @property
    def create_button(self):
        return self.baseLocator.locator('#createGlobalItem')

    @property
    def profile_button(self):
        return self.baseLocator.locator('[data-testid="profile-button"]')

    def click_create_button(self):
        self.create_button.click()
