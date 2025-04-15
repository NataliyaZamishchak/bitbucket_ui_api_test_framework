from playwright.sync_api import Page
from pom.elements.bitbucket_header import BitbucketHeader
from pom.elements.repo_side_navigation_menu import RepoSideMenu
from utils.logger import get_logger

logger = get_logger(__name__)

class RepoSourcePage:
    """Represents the repository source page."""

    def __init__(self, page: Page, workspace: str, repo: str):
        """Initialize the repository source page."""
        self.page = page
        self.workspace = workspace
        self.repo = repo
        self.side_menu = RepoSideMenu(page.locator('[data-testid="side-navigation"]'))
        self.header = BitbucketHeader(page.locator('header'))

    @property
    def page_title(self):
        """Locator for the page title."""
        return self.page.locator("header h1")

    @property
    def page_error(self):
        """Locator for the error message on the page."""
        return self.page.locator("#error h1")

    def goto(self):
        """Navigate to the repository source page."""
        logger.info(f"Navigating to the repository source page for repo: {self.repo}")
        url = f'https://bitbucket.org/{self.workspace}/{self.repo}/src/main/'
        self.page.goto(url)

    def click_target_file(self, file_name: str):
        """Click on a target file in the repository."""
        logger.info(f"Clicking on the target file: {file_name}")
        self.page.locator(f'//table[@data-qa="repository-directory"]//a[contains(@href, "{file_name}")]').click()