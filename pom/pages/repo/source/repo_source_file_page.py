from playwright.sync_api import Page

class RepoSourceFilePage:
    def __init__(self, page: Page, workspace: str = None, repo: str = None):
        self.page = page
        self.workspace = workspace
        self.repo = repo

    @property
    def page_title(self):
        return self.page.locator("main h1")

    @property
    def edit_file_button(self):
        return self.page.locator('//div[@data-testid="file-actions"]//button[.//span[contains(text(), "Edit")]]')

    @property
    def editing_page_title(self):
        return self.page.locator('.bb-content-container-heading')

    @property
    def editing_file_form_title(self):
        return self.page.locator('.bb-content-container-heading')

    @property
    def editing_file_textarea(self):
        return self.page.locator('#id_source')

    @property
    def editing_file_commit_button(self):
        return self.page.locator('//div[@class="bb-content-container-footer"]//button[text()="Commit"]')

    def click_edit_file_button(self):
        self.edit_file_button.click()

    def click_editing_file_commit_button(self):
        self.editing_file_commit_button.click()

