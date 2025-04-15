from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)

class RemoveRepoAccessModal:
    """Represents the modal for removing repository access."""

    def __init__(self, page: Page):
        """Initialize the remove repository access modal."""
        self.page = page

    @property
    def modal_title(self):
        """Locator for the modal title."""
        return self.page.locator('//span[contains(@id, "modal-dialog-title")]')

    @property
    def remove_button(self):
        """Locator for the remove button."""
        return self.page.locator('[data-testid="remove-access-modal--remove-btn"]')

    def click_remove_button(self):
        """Click the remove button."""
        logger.info("Clicking the remove button in the remove repository access modal.")
        self.remove_button.click()
        self.page.wait_for_selector('[role="alert"] h2 span')