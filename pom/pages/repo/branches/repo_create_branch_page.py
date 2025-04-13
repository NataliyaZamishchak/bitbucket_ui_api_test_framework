from playwright.sync_api import Page

class CreateBranchPage:
    def __init__(self, page: Page, workspace: str, repo: str):
        self.page = page
        self.workspace = workspace
        self.repo = repo

    @property
    def page_title(self):
        return self.page.locator("main h1")

    @property
    def branch_type_input(self):
        return self.page.locator('[aria-labelledby="branch-type-label"]')

    @property
    def branch_name_input(self):
        return self.page.locator('[name="branchName"]')

    @property
    def create_button(self):
        return self.page.locator('#create-branch-button')

    def goto(self):
        self.page.goto(f"https://bitbucket.org/{self.workspace}/{self.repo}/branch")

    def select_branch_type(self, branch_type: str):
        self.branch_type_input.fill(branch_type)
        self.branch_type_input.press("Enter")

    def click_create_button(self):
        self.create_button.click()
        self.page.wait_for_selector('[data-qa="commit-list-styles"]')
