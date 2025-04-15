from playwright.sync_api import Page
from pom.elements.bitbucket_header import BitbucketHeader
from utils.logger import get_logger

logger = get_logger(__name__)

class OverviewPage:
    """Represents the Bitbucket workspace overview page."""

    def __init__(self, page: Page, workspace: str):
        """Initialize the overview page with the Playwright page and workspace."""
        self.page = page
        self.workspace = workspace
        self.header = BitbucketHeader(page.locator('header'))

    def goto(self):
        """Navigate to the workspace overview page."""
        logger.info(f"Navigating to the overview page for workspace: {self.workspace}")
        self.page.goto(f'https://bitbucket.org/{self.workspace}/workspace/overview/')

