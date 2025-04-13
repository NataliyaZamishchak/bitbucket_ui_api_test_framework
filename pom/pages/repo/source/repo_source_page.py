from playwright.sync_api import Page

from pom.elements.bitbucket_header import BitbucketHeader
from pom.elements.repo_side_navigation_menu import RepoSideMenu


class RepoSourcePage:
    def __init__(self, page: Page, workspace: str, repo: str):
        self.page = page
        self.workspace = workspace
        self.repo = repo
        self.side_menu = RepoSideMenu(page.locator('[data-testid="side-navigation"]'))
        self.header = BitbucketHeader(page.locator('header'))

    @property
    def page_title(self):
        return self.page.locator("header h1")

    def goto(self):
        self.page.goto(f'https://bitbucket.org/{self.workspace}/{self.repo}/src/main/')

    def click_target_file(self, file_name: str):
        self.page.locator(f'//table[@data-qa="repository-directory"]//a[contains(@href, "{file_name}")]').click()