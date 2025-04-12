from playwright.sync_api import Page

class CreateRepoPage:
    def __init__(self, page: Page):
        self.page = page
    
    @property
    def repo_name_input(self):
        return self.page.locator("input#repo-name")

    @property
    def description_input(self):
        return self.page.locator("textarea#repo-description")

    @property
    def private_checkbox(self):
        return self.page.locator("input#repo-private")

    @property
    def create_button(self):
        return self.page.get_by_role("button", name="Create repository")

    @property
    def success_message(self):
        return self.page.locator(".repo-created-message")

    def select_project_by_name(self, project_name: str):
        return self.page.locator(f"text={project_name}")

    def go_to_create_repo(self):
        self.page.goto(f"https://bitbucket.org/{os.getenv('BITBUCKET_ORGANIZATION_NAME')}/workspace/create/repository")
