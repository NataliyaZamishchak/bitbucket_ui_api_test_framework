from playwright.sync_api import Locator

from pom.elements.global_navigation_menu import GlobalNavigation


class BitbucketHeader:
    def __init__(self, base_locator: Locator):
        self.base_locator = base_locator
        self.global_nav_menu = GlobalNavigation(base_locator.locator('//nav[@aria-label="Global navigation"]'))

    @property
    def create_button(self):
        return self.base_locator.locator('#createGlobalItem')

    @property
    def profile_button(self):
        return self.base_locator.locator('[data-testid="profile-button"]')

    def click_create_button(self):
        self.create_button.click()

    def click_header_tab(self, tab_name):
        self.global_nav_menu.click_navigation_tab(tab_name)
