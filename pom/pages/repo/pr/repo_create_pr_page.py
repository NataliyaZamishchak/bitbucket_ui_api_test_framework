from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)

class RepoCreatePrPage:
    """Represents the create pull request page of a repository."""

    def __init__(self, page: Page, workspace: str = None, repo: str = None):
        """Initialize the create pull request page."""
        self.page = page
        self.workspace = workspace
        self.repo = repo

    @property
    def page_title(self):
        """Locator for the page title."""
        return self.page.locator("main h1")

    @property
    def create_pr_button(self):
        """Locator for the create pull request button."""
        return self.page.locator('[data-testid="create-PR-button"]')

    def click_create_pr_button(self):
        """Click the create pull request button."""
        logger.info("Clicking the create pull request button.")
        self.create_pr_button.click()
