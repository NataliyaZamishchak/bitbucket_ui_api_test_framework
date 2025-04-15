from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)

class CreateMenu:
    """Represents the create menu component."""

    def __init__(self, page: Page):
        """Initialize the create menu with the Playwright page."""
        self.page = page

    @property
    def create_menu(self):
        """Locator for the create menu."""
        return self.page.locator('[data-placement="bottom-start"]')

    @property
    def create_menu_options(self):
        """Locator for the create menu options."""
        return self.page.locator('a[data-testid*="-create-item"]')

    @property
    def create_menu_repo_options(self):
        """Locator for the repository-specific create menu options."""
        return self.page.locator('[aria-label="This repository"] a [data-item-title]')

    def click_create_menu_option(self, option: str):
        """Click a create menu option by name."""
        logger.info(f"Clicking create menu option: {option}")
        elements = self.create_menu_options.element_handles()
        for element in elements:
            data_testid = element.get_attribute('data-testid')
            if option.lower() in data_testid:
                element.click()
                logger.info(f"Clicked create menu option: {option}")
                return
        logger.warning(f"Create menu option '{option}' not found.")

    def click_create_menu_repo_option(self, option: str):
        """Click a repository-specific create menu option by name."""
        logger.info(f"Clicking repository-specific create menu option: {option}")
        elements = self.create_menu_repo_options.element_handles()
        for element in elements:
            if option == element.text_content():
                element.click()
                logger.info(f"Clicked repository-specific create menu option: {option}")
                return
        logger.warning(f"Repository-specific create menu option '{option}' not found.")

    def validate_if_exists_create_menu_repo_option(self, option: str):
        """Validate if a repository-specific create menu option exists."""
        logger.info(f"Validating existence of repository-specific create menu option: {option}")
        elements = self.create_menu_repo_options.element_handles()
        for element in elements:
            if option == element.text_content():
                logger.info(f"Repository-specific create menu option '{option}' exists.")
                return True
        logger.info(f"Repository-specific create menu option '{option}' does not exist.")
        return False