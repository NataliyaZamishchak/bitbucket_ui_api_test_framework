from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)

class AddUserOrGroupsModal:
    """Represents the modal for adding users or groups."""

    def __init__(self, page: Page):
        """Initialize the modal with the Playwright page."""
        self.page = page

    @property
    def add_group_or_user_input(self):
        """Locator for the input to add a user or group."""
        return self.page.locator('[class="add-access-select__input"]')

    @property
    def user_select_menu_first_option(self):
        """Locator for the first option in the user select menu."""
        return self.page.locator('.add-access-select__option')

    @property
    def permission_dropdown(self):
        """Locator for the permission dropdown."""
        return self.page.locator('section[role="dialog"] [data-testid="privilegesDropdown--trigger"]')

    @property
    def confirm_button(self):
        """Locator for the confirm button."""
        return self.page.locator('//button[.//span[text()="Confirm"]]')

    def select_user_to_add(self, user_name: str):
        """Select a user to add by typing their name."""
        logger.info(f"Typing username '{user_name}' to add.")
        self.add_group_or_user_input.type(user_name, delay=300)
        self.user_select_menu_first_option.wait_for()
        logger.info(f"Selecting the first option for user '{user_name}'.")
        self.user_select_menu_first_option.click()

    def select_privilege(self, privilege: str):
        """Select a privilege from the dropdown."""
        logger.info(f"Selecting privilege '{privilege}' from the dropdown.")
        self.permission_dropdown.click()
        self.page.locator(f'//button[@role="menuitem"][.//span[text()="{privilege}"]]').click()

    def click_confirm_button(self):
        """Click the confirm button."""
        logger.info("Clicking the confirm button.")
        self.confirm_button.click()
        self.page.wait_for_selector('[role="alert"] h2 span')
        logger.info("Confirm button clicked and action completed.")

