from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)

class CommitChangesModal:
    """Represents the modal for committing changes."""

    def __init__(self, page: Page):
        """Initialize the modal with the Playwright page."""
        self.page = page

    @property
    def commit_button(self):
        """Locator for the commit button."""
        return self.page.locator('.dialog-button-panel .commit-button')

    def click_commit_button(self):
        """Click the commit button."""
        logger.info("Clicking the commit button.")
        self.commit_button.click()
        self.page.wait_for_selector('[aria-label="Global comments"]')
        logger.info("Commit button clicked and changes committed.")