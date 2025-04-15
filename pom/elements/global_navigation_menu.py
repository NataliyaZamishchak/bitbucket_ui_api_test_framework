from playwright.sync_api import Locator
from utils.logger import get_logger

logger = get_logger(__name__)

class GlobalNavigation:
    """Represents the global navigation menu."""

    def __init__(self, base_locator: Locator):
        """Initialize the global navigation menu."""
        self.base_locator = base_locator

    def navigation_tab(self, tab_name: str):
        """Get the locator for a navigation tab."""
        return self.base_locator.locator(f'//div[@role="listitem"]//a[.//span[text()="{tab_name}"]]')

    def click_navigation_tab(self, tab_name: str):
        """Click a navigation tab by name."""
        logger.info(f"Clicking navigation tab: {tab_name}")
        self.navigation_tab(tab_name).click()
