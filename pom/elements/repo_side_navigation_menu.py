from playwright.sync_api import Locator
from utils.logger import get_logger

logger = get_logger(__name__)

class RepoSideMenu:
    """Represents the repository side navigation menu."""

    def __init__(self, base_locator: Locator):
        """Initialize the repository side menu."""
        self.base_locator = base_locator

    def side_menu_option(self, name: str):
        """Get the locator for a side menu option."""
        return self.base_locator.locator(f'//a[.//*[text()="{name}"]] | //button[.//*[text()="{name}"]]')

    def click_side_menu_option(self, name: str):
        """Click a side menu option by name."""
        logger.info(f"Clicking side menu option: {name}")
        self.side_menu_option(name).click()
