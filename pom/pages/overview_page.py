from playwright.sync_api import Page

from pom.elements.bitbucket_header import BitbucketHeader


class OverviewPage:
    def __init__(self, page: Page, workspace: str):
        self.page = page
        self.workspace = workspace
        self.header = BitbucketHeader(page.locator('header'))

    def goto(self):
        self.page.goto(f'https://bitbucket.org/{self.workspace}/workspace/overview/')

