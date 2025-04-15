from playwright.sync_api import Page
from pom.elements.bitbucket_header import BitbucketHeader
from pom.elements.repo_side_navigation_menu import RepoSideMenu
from pom.elements.user_permissions_table import UsersPermissionsTable
from utils.logger import get_logger

logger = get_logger(__name__)

class RepoPermissionsPage:
    """Represents the repository permissions page."""

    def __init__(self, page: Page, workspace: str = None, repo: str = None):
        """Initialize the repository permissions page."""
        self.page = page
        self.workspace = workspace
        self.repo = repo
        self.side_menu = RepoSideMenu(page.locator('[data-testid="side-navigation"]'))
        self.header = BitbucketHeader(page.locator('header'))
        self.users_permissions_table = UsersPermissionsTable(page.locator('//table[.//th[text()="Permission"]]'))

    @property
    def page_title(self):
        """Locator for the page title."""
        return self.page.locator("main h1")

    @property
    def add_user_or_group_button(self):
        """Locator for the add user or group button."""
        return self.page.locator('[data-testid="addPrivilegeButton"]')

    @property
    def permission_table(self):
        """Locator for the permissions table."""
        return self.page.locator('//table[.//th[text()="Permission"]]')

    def goto(self):
        """Navigate to the repository permissions page."""
        logger.info(f"Navigating to the permissions page for repo: {self.repo}")
        self.page.goto(f'https://bitbucket.org/{self.workspace}/{self.repo}/admin/permissions')

    def click_add_user_or_group_button(self):
        """Click the add user or group button."""
        logger.info("Clicking the add user or group button.")
        self.add_user_or_group_button.click()
