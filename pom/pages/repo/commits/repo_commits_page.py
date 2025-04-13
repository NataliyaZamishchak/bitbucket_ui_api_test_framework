from playwright.sync_api import Page

from pom.elements.bitbucket_header import BitbucketHeader


class RepoCommitsPage:
    def __init__(self, page: Page, workspace: str = None, repo: str = None):
        self.page = page
        self.workspace = workspace
        self.repo = repo
        self.header = BitbucketHeader(page.locator('header'))

    @property
    def page_title(self):
        return self.page.locator("main h1")

    @property
    def commit_message_label(self):
        return self.page.locator("//main//h1/following::p[1]")
