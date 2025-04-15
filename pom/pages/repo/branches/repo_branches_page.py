from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)

class RepoBranchesPage:
    """Represents the branches page of a repository."""

    def __init__(self, page: Page, workspace: str = None, repo: str = None):
        """Initialize the branches page."""
        self.page = page
        self.workspace = workspace
        self.repo = repo

    @property
    def page_title(self):
        """Locator for the page title."""
        return self.page.locator("main h1")

    @property
    def view_source_button(self):
        """Locator for the view source button."""
        return self.page.locator('//a[.//*[contains(text(), "View source")]]')

    def click_view_source_button(self):
        """Click the view source button."""
        logger.info("Clicking the view source button.")
        self.view_source_button.click()
