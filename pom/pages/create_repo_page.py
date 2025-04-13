from playwright.sync_api import Page

class CreateRepoPage:
    def __init__(self, page: Page, workspace: str):
        self.page = page
        self.workspace = workspace

    @property
    def page_title(self):
        return self.page.locator("header h1")

    @property
    def repo_name_input(self):
        return self.page.locator("input#id_name")

    @property
    def project_select(self):
        return self.page.locator("#s2id_id_project")

    @property
    def private_checkbox(self):
        return self.page.locator("input#id_is_private")

    @property
    def create_button(self):
        return self.page.locator("button[type='submit']")

    @property
    def project_select_dropdown(self):
        return self.page.locator('#select2-drop')

    @property
    def project_select_options(self):
        return self.page.locator('//li[.//*[@class="project-dropdown--label"]]')

    @property
    def project_select_create_new_option(self):
        return self.page.locator('//li[.//*[@class="select2-result-label"]]')

    @property
    def project_input(self):
        return self.page.locator('#id_project_name')

    def goto(self):
        self.page.goto(f"https://bitbucket.org/{self.workspace}/workspace/create/repository")

    def select_first_project(self):
        self.project_select.click()
        self.project_select_dropdown.wait_for()
        self.project_select_create_new_option.wait_for()
        elements = self.project_select_options.element_handles()
        if elements:
            elements[0].click()

    def select_create_new_project(self, name: str):
        self.project_select.click()
        self.project_select_dropdown.wait_for()
        self.project_select_create_new_option.click()
        self.project_input.fill(name)

    def click_create_button(self):
        self.create_button.click()
