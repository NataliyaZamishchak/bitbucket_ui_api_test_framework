from playwright.sync_api import Page

class RepoPrPage:
    def __init__(self, page: Page, workspace: str = None, repo: str = None, pr_number: int = None):
        self.page = page
        self.workspace = workspace
        self.repo = repo
        self.pr_number = pr_number

    @property
    def page_title(self):
        return self.page.locator("(//div[@data-read-view-fit-container-width]//span)[2]")

    @property
    def pr_status(self):
        return self.page.locator('(//div[@data-qa="pr-branches-and-state-styles"]//div[@role="presentation"])[3]//span[text()]')

    @property
    def code_diff_file_name(self):
        return self.page.locator('article h2 span')

    @property
    def code_diff_added_line(self):
        return self.page.locator('[data-line-type="+"]')

    @property
    def approve_button(self):
        return self.page.locator('[aria-label="Approve this pull request"]')

    @property
    def unapprove_button(self):
        return self.page.locator('[aria-label="Unapprove this pull request"]')

    @property
    def merge_button(self):
        return self.page.locator('[data-testid="mergeButton-primary"]')

    def select_pr_tab(self, tab_name):
        tab = self.page.locator(f'//a[@role="tab"][.//span[text()="{tab_name}"]]')
        tab.click()

    def goto(self):
        self.page.goto(f'https://bitbucket.org/{self.workspace}/{self.repo}/pull-requests/{self.pr_number}')

    def validate_if_added_line_contains_text(self, text: str) -> bool:
        added_line_text = self.code_diff_added_line.get_attribute('aria-label')
        return text in added_line_text

    def click_approve_button(self):
        self.approve_button.click()
        self.unapprove_button.wait_for()

    def click_merge_button(self):
        self.merge_button.click()