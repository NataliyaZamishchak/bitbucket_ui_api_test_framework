from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)

class CreateRepoPage:
    """Represents the page for creating a new repository."""

    def __init__(self, page: Page, workspace: str):
        """Initialize the create repository page."""
        self.page = page
        self.workspace = workspace

    @property
    def page_title(self):
        """Locator for the page title."""
        return self.page.locator("header h1")

    @property
    def repo_name_input(self):
        """Locator for the repository name input field."""
        return self.page.locator("input#id_name")

    @property
    def project_select(self):
        """Locator for the project select dropdown."""
        return self.page.locator("#s2id_id_project")

    @property
    def private_checkbox(self):
        """Locator for the private repository checkbox."""
        return self.page.locator("input#id_is_private")

    @property
    def create_button(self):
        """Locator for the create button."""
        return self.page.locator("button[type='submit']")

    @property
    def project_select_dropdown(self):
        """Locator for the project select dropdown menu."""
        return self.page.locator('#select2-drop')

    @property
    def project_select_options(self):
        """Locator for the project select options."""
        return self.page.locator('//li[.//*[@class="project-dropdown--label"]]')

    @property
    def project_select_create_new_option(self):
        """Locator for the create new project option."""
        return self.page.locator('//li[.//*[@class="select2-result-label"]]')

    @property
    def project_input(self):
        """Locator for the project name input field."""
        return self.page.locator('#id_project_name')

    def goto(self):
        """Navigate to the create repository page."""
        logger.info(f"Navigating to the create repository page for workspace: {self.workspace}")
        self.page.goto(f"https://bitbucket.org/{self.workspace}/workspace/create/repository")

    def select_first_project(self):
        """Select the first project from the dropdown."""
        logger.info("Selecting the first project from the dropdown.")
        self.project_select.click()
        self.project_select_dropdown.wait_for()
        self.project_select_create_new_option.wait_for()
        elements = self.project_select_options.element_handles()
        if elements:
            elements[0].click()
            logger.info("First project selected.")
        else:
            logger.warning("No projects available to select.")

    def select_create_new_project(self, name: str):
        """Select the create new project option and fill in the name."""
        logger.info(f"Creating a new project with name: {name}")
        self.project_select.click()
        self.project_select_dropdown.wait_for()
        self.project_select_create_new_option.click()
        self.project_input.fill(name)
        logger.info(f"New project name '{name}' filled in.")

    def click_create_button(self):
        """Click the create button."""
        logger.info("Clicking the create button.")
        self.create_button.click()
