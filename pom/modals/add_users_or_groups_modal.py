from playwright.sync_api import Page

class AddUserOrGroupsModal:
    def __init__(self, page: Page):
        self.page = page

    @property
    def add_group_or_user_input(self):
        return self.page.locator('[class="add-access-select__input"]')

    @property
    def user_select_menu_first_option(self):
        return self.page.locator('.add-access-select__option')

    @property
    def permission_dropdown(self):
        return self.page.locator('section[role="dialog"] [data-testid="privilegesDropdown--trigger"]')

    @property
    def confirm_button(self):
        return self.page.locator('//button[.//span[text()="Confirm"]]')

    def select_user_to_add(self, user_name: str):
        self.add_group_or_user_input.type(user_name, delay=300)
        self.user_select_menu_first_option.wait_for()
        self.user_select_menu_first_option.click()

    def select_privilege(self, privilege: str):
        self.permission_dropdown.click()
        self.page.locator(f'//button[@role="menuitem"][.//span[text()="{privilege}"]]').click()

    def click_confirm_button(self):
        self.confirm_button.click()
        self.page.wait_for_selector('[role="alert"] h2 span')

