from playwright.sync_api import Page
from pom.elements.bitbucket_header import BitbucketHeader
from utils.logger import get_logger

logger = get_logger(__name__)

class RepoCommitsPage:
    """Represents the commits page of a repository."""

    def __init__(self, page: Page, workspace: str = None, repo: str = None):
        """Initialize the commits page."""
        self.page = page
        self.workspace = workspace
        self.repo = repo
        self.header = BitbucketHeader(page.locator('header'))

    @property
    def page_title(self):
        """Locator for the page title."""
        return self.page.locator("main h1")

    @property
    def commit_message_label(self):
        """Locator for the commit message label."""
        return self.page.locator("//main//h1/following::p[1]")

    def goto(self):
        """Navigate to the commits page."""
        logger.info(f"Navigating to the commits page for repo: {self.repo}")
        url = f'https://bitbucket.org/{self.workspace}/{self.repo}/commits/'
        self.page.goto(url)
