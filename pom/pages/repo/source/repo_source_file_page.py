from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)

class RepoSourceFilePage:
    """Represents the repository source file page."""

    def __init__(self, page: Page, workspace: str = None, repo: str = None):
        """Initialize the repository source file page."""
        self.page = page
        self.workspace = workspace
        self.repo = repo

    @property
    def page_title(self):
        """Locator for the page title."""
        return self.page.locator("main h1")

    @property
    def edit_file_button(self):
        """Locator for the edit file button."""
        return self.page.locator('//div[@data-testid="file-actions"]//button[.//span[contains(text(), "Edit")]]')

    @property
    def editing_page_title(self):
        """Locator for the editing page title."""
        return self.page.locator('.bb-content-container-heading')

    @property
    def editing_file_form_title(self):
        """Locator for the editing file form title."""
        return self.page.locator('.bb-content-container-heading')

    @property
    def editing_file_textarea(self):
        """Locator for the editing file textarea."""
        return self.page.locator('#id_source')

    @property
    def editing_file_commit_button(self):
        """Locator for the commit button on the editing file page."""
        return self.page.locator('//div[@class="bb-content-container-footer"]//button[text()="Commit"]')

    def click_edit_file_button(self):
        """Click the edit file button."""
        logger.info("Clicking the edit file button.")
        self.edit_file_button.click()

    def click_editing_file_commit_button(self):
        """Click the commit button on the editing file page."""
        logger.info("Clicking the commit button on the editing file page.")
        self.editing_file_commit_button.click()

