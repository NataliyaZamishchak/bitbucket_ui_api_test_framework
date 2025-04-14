from playwright.sync_api import Locator


class RepoSideMenu:
    def __init__(self, base_locator: Locator):
        self.base_locator = base_locator

    def side_menu_option(self, name: str):
        return self.base_locator.locator(f'//a[.//*[text()="{name}"]] | //button[.//*[text()="{name}"]]')

    def click_side_menu_option(self, name: str):
        self.side_menu_option(name).click()
