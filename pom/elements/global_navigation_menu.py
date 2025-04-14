from playwright.sync_api import Locator


class GlobalNavigation:
    def __init__(self, base_locator: Locator):
        self.base_locator = base_locator

    def navigation_tab(self, tab_name:str):
        return self.base_locator.locator(f'//div[@role="listitem"]//a[.//span[text()="{tab_name}"]]')

    def click_navigation_tab(self, tab_name:str):
        self.navigation_tab(tab_name).click()
