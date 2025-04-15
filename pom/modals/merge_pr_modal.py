from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)

class MergePrModal:
    """Represents the modal for merging a pull request."""

    def __init__(self, page: Page):
        """Initialize the merge pull request modal."""
        self.page = page

    @property
    def merge_button(self):
        """Locator for the merge button."""
        return self.page.locator('//button[.//*[@data-qa="merge-dialog-merge-button"]]')

    def click_merge_button(self):
        """Click the merge button."""
        logger.info("Clicking the merge button in the merge pull request modal.")
        self.merge_button.click()
        self.page.wait_for_selector('//h2[text()="Merged pull request"]')