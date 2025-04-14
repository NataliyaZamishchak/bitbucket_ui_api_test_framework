from playwright.sync_api import Page

from pom.elements.bitbucket_header import BitbucketHeader
from pom.elements.repo_side_navigation_menu import RepoSideMenu
from pom.elements.user_permissions_table import UsersPermissionsTable


class RepoPermissionsPage:
    def __init__(self, page: Page, workspace: str = None, repo: str = None):
        self.page = page
        self.workspace = workspace
        self.repo = repo
        self.side_menu = RepoSideMenu(page.locator('[data-testid="side-navigation"]'))
        self.header = BitbucketHeader(page.locator('header'))
        self.users_permissions_table = UsersPermissionsTable(page.locator('//table[.//th[text()="Permission"]]'))

    @property
    def page_title(self):
        return self.page.locator("main h1")

    @property
    def add_user_or_group_button(self):
        return self.page.locator('[data-testid="addPrivilegeButton"]')

    @property
    def permission_table(self):
        return self.page.locator('//table[.//th[text()="Permission"]]')

    def goto(self):
        self.page.goto(f'https://bitbucket.org/{self.workspace}/{self.repo}/admin/permissions')

    def click_add_user_or_group_button(self):
        return self.add_user_or_group_button.click()
