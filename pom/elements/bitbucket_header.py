from playwright.sync_api import Locator
from pom.elements.global_navigation_menu import GlobalNavigation
from utils.logger import get_logger

logger = get_logger(__name__)

class BitbucketHeader:
    """Represents the Bitbucket header with navigation and actions."""

    def __init__(self, base_locator: Locator):
        """Initialize the Bitbucket header."""
        self.base_locator = base_locator
        self.global_nav_menu = GlobalNavigation(base_locator.locator('//nav[@aria-label="Global navigation"]'))

    @property
    def create_button(self):
        """Locator for the create button."""
        return self.base_locator.locator('#createGlobalItem')

    @property
    def profile_button(self):
        """Locator for the profile button."""
        return self.base_locator.locator('[data-testid="profile-button"]')

    def click_create_button(self):
        """Click the create button."""
        logger.info("Clicking the create button in the header.")
        self.create_button.click()

    def click_header_tab(self, tab_name):
        """Click a header tab by name."""
        logger.info(f"Clicking the header tab: {tab_name}")
        self.global_nav_menu.click_navigation_tab(tab_name)
