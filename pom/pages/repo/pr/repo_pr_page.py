from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)

class RepoPrPage:
    """Represents the pull request page of a repository."""

    def __init__(self, page: Page, workspace: str = None, repo: str = None, pr_number: int = None):
        """Initialize the pull request page."""
        self.page = page
        self.workspace = workspace
        self.repo = repo
        self.pr_number = pr_number

    @property
    def page_title(self):
        """Locator for the pull request page title."""
        return self.page.locator("(//div[@data-read-view-fit-container-width]//span)[2]")

    @property
    def pr_status(self):
        """Locator for the pull request status."""
        return self.page.locator('(//div[@data-qa="pr-branches-and-state-styles"]//div[@role="presentation"])[3]//span[text()]')

    @property
    def code_diff_file_name(self):
        """Locator for the file name in the code diff."""
        return self.page.locator('article h2 span')

    @property
    def code_diff_added_line(self):
        """Locator for the added line in the code diff."""
        return self.page.locator('[data-line-type="+"]')

    @property
    def approve_button(self):
        """Locator for the approve button."""
        return self.page.locator('[aria-label="Approve this pull request"]')

    @property
    def unapprove_button(self):
        """Locator for the unapprove button."""
        return self.page.locator('[aria-label="Unapprove this pull request"]')

    @property
    def merge_button(self):
        """Locator for the merge button."""
        return self.page.locator('[data-testid="mergeButton-primary"]')

    def select_pr_tab(self, tab_name):
        """Select a pull request tab by name."""
        logger.info(f"Selecting pull request tab: {tab_name}")
        tab = self.page.locator(f'//a[@role="tab"][.//span[text()="{tab_name}"]]')
        tab.click()

    def goto(self):
        """Navigate to the pull request page."""
        if self.pr_number:
            url = f'https://bitbucket.org/{self.workspace}/{self.repo}/pull-requests/{self.pr_number}'
        else:
            url = f'https://bitbucket.org/{self.workspace}/{self.repo}/pull-requests'
        logger.info(f"Navigating to the pull request page: {url}")
        self.page.goto(url)

    def validate_if_added_line_contains_text(self, text: str) -> bool:
        """Validate if the added line contains the specified text."""
        logger.info(f"Validating if the added line contains text: {text}")
        added_line_text = self.code_diff_added_line.get_attribute('aria-label')
        return text in added_line_text

    def click_approve_button(self):
        """Click the approve button."""
        logger.info("Clicking the approve button.")
        self.approve_button.click()
        self.unapprove_button.wait_for()

    def click_merge_button(self):
        """Click the merge button."""
        logger.info("Clicking the merge button.")
        self.merge_button.click()