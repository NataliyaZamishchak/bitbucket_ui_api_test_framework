from pom.modals.create_menu_component import CreateMenu
from pom.pages.atlassian_login_page import AtlassianLoginPage
from pom.pages.create_repo_page import CreateRepoPage
from pom.pages.overview_page import OverviewPage
from pom.pages.repo.branches.repo_create_branch_page import CreateBranchPage
from pom.pages.repo.source.repo_source_page import RepoSourcePage
import uuid

TEST_REPO_NAME = f"test_repo_{uuid.uuid4().hex[:8]}"
TEST_BRANCH_NAME = f"test_branch_{uuid.uuid4().hex[:8]}"

class TestsWebUi:
    def test_login_setup(self, page, bitbucket_username, bitbucket_password, bitbucket_organization):
        login_page = AtlassianLoginPage(page, page.context, bitbucket_organization)
        login_page.login(bitbucket_username, bitbucket_password)
        assert login_page.success_login_img.is_visible(), "Login failed or success image not visible."

    def test_create_repo(self, page, bitbucket_organization):
        overview_page = OverviewPage(page, bitbucket_organization)
        overview_page.goto()
        overview_page.header.click_create_button()
        create_menu = CreateMenu(page)
        create_menu.click_create_menu_option("Repository")
        create_repo_page = CreateRepoPage(page, bitbucket_organization)
        create_repo_page.select_first_project()
        create_repo_page.repo_name_input.fill(TEST_REPO_NAME)
        create_repo_page.click_create_button()
        repo_page = RepoSourcePage(page, bitbucket_organization, TEST_REPO_NAME)
        assert repo_page.page_title.text_content() == TEST_REPO_NAME

    def test_create_pr(self, page, bitbucket_organization):
        repo_page = RepoSourcePage(page, bitbucket_organization, 'test3')
        repo_page.goto()
        repo_page.header.click_create_button()
        create_menu = CreateMenu(page)
        create_menu.click_create_menu_repo_option("Branch")
        create_branch_page = CreateBranchPage(page, bitbucket_organization, 'test3')
        create_branch_page.select_branch_type('Feature')
        create_branch_page.branch_name_input.fill(TEST_BRANCH_NAME)
        create_branch_page.click_create_button()
