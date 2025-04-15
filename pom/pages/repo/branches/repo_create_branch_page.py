from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)

class CreateBranchPage:
    """Represents the create branch page of a repository."""

    def __init__(self, page: Page, workspace: str, repo: str):
        """Initialize the create branch page."""
        self.page = page
        self.workspace = workspace
        self.repo = repo

    @property
    def page_title(self):
        """Locator for the page title."""
        return self.page.locator("main h1")

    @property
    def branch_type_input(self):
        """Locator for the branch type input field."""
        return self.page.locator('[aria-labelledby="branch-type-label"]')

    @property
    def branch_name_input(self):
        """Locator for the branch name input field."""
        return self.page.locator('[name="branchName"]')

    @property
    def create_button(self):
        """Locator for the create branch button."""
        return self.page.locator('#create-branch-button')

    def goto(self):
        """Navigate to the create branch page."""
        logger.info(f"Navigating to the create branch page for repo: {self.repo}")
        self.page.goto(f"https://bitbucket.org/{self.workspace}/{self.repo}/branch")

    def select_branch_type(self, branch_type: str):
        """Select a branch type."""
        logger.info(f"Selecting branch type: {branch_type}")
        self.branch_type_input.fill(branch_type)
        self.branch_type_input.press("Enter")

    def click_create_button(self):
        """Click the create branch button."""
        logger.info("Clicking the create branch button.")
        self.create_button.click()
        self.page.wait_for_selector('[data-qa="commit-list-styles"]')
