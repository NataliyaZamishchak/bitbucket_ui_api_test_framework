from playwright.sync_api import Page

class CreateMenu:
    def __init__(self, page: Page):
        self.page = page

    @property
    def create_menu(self):
        return self.page.locator('[data-placement="bottom-start"]')

    @property
    def create_menu_options(self):
        return self.page.locator('a[data-testid*="-create-item"]')

    @property
    def create_menu_repo_options(self):
        return self.page.locator('[aria-label="This repository"] a [data-item-title]')

    def click_create_menu_option(self, option: str):
        elements = self.create_menu_options.element_handles()
        for element in elements:
            data_testid = element.get_attribute('data-testid')
            if option.lower() in data_testid:
                element.click()
                return

    def click_create_menu_repo_option(self, option: str):
        elements = self.create_menu_repo_options.element_handles()
        for element in elements:
            if option == element.text_content():
                element.click()
                return

    def validate_if_exists_create_menu_repo_option(self, option: str):
        elements = self.create_menu_repo_options.element_handles()
        for element in elements:
            if option == element.text_content():
                return True
        return False