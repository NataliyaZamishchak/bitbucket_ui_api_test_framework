from pom.modals.commit_changes_modal import CommitChangesModal
from pom.modals.create_menu_component import CreateMenu
from pom.modals.merge_pr_modal import MergePrModal
from pom.pages.atlassian_login_page import AtlassianLoginPage
from pom.pages.create_repo_page import CreateRepoPage
from pom.pages.overview_page import OverviewPage
from pom.pages.repo.branches.repo_branches_page import RepoBranchesPage
from pom.pages.repo.branches.repo_create_branch_page import CreateBranchPage
from pom.pages.repo.commits.repo_commits_page import RepoCommitsPage
from pom.pages.repo.pr.repo_create_pr_page import RepoCreatePrPage
from pom.pages.repo.pr.repo_pr_page import RepoPrPage
from pom.pages.repo.source.repo_source_file_page import RepoSourceFilePage
from pom.pages.repo.source.repo_source_page import RepoSourcePage
import uuid
from utils.logger import get_logger

logger = get_logger(__name__)

TEST_REPO_NAME = f"test_repo_{uuid.uuid4().hex[:8]}"
TEST_BRANCH_NAME = f"test_branch_{uuid.uuid4().hex[:8]}"
ADD_NEW_TEXT_CHANGES = "Add new text to README.md"
DEFAULT_COMMIT_MESSAGE = 'README.md edited online with Bitbucket'

class TestsWebUi:
    """Test suite for Bitbucket Web UI functionality."""

    def test_login_setup(self, page, admin_email, admin_password, workspace):
        """Test admin login to Bitbucket."""
        login_page = AtlassianLoginPage(page, page.context, workspace)
        login_page.login(admin_email, admin_password)
        assert login_page.success_login_img.is_visible(), "Login failed or success image not visible."

    def test_create_repo(self, page, workspace):
        """Test creating a new repository."""
        overview_page = OverviewPage(page, workspace)
        overview_page.goto()
        overview_page.header.click_create_button()
        create_menu = CreateMenu(page)
        create_menu.click_create_menu_option("Repository")
        create_repo_page = CreateRepoPage(page, workspace)
        create_repo_page.select_first_project()
        create_repo_page.repo_name_input.fill(TEST_REPO_NAME)
        create_repo_page.click_create_button()
        repo_page = RepoSourcePage(page, workspace, TEST_REPO_NAME)
        assert repo_page.page_title.text_content() == TEST_REPO_NAME

    def test_create_pr(self, page, workspace):
        """Test creating a pull request."""
        repo_page = RepoSourcePage(page, workspace, TEST_REPO_NAME)
        repo_page.goto()
        repo_page.header.click_create_button()
        create_menu = CreateMenu(page)
        create_menu.click_create_menu_repo_option("Branch")
        create_branch_page = CreateBranchPage(page, workspace, TEST_REPO_NAME)
        create_branch_page.select_branch_type('Feature')
        create_branch_page.branch_name_input.fill(TEST_BRANCH_NAME)
        create_branch_page.click_create_button()
        branch_page = RepoBranchesPage(page)
        assert branch_page.page_title.text_content() == "feature/" + TEST_BRANCH_NAME
        branch_page.click_view_source_button()
        repo_page.click_target_file('README.md')
        file_page = RepoSourceFilePage(page)
        assert file_page.page_title.text_content() == 'README.md'
        file_page.click_edit_file_button()
        assert 'Editing' in file_page.editing_file_form_title.text_content()
        file_page.editing_file_textarea.type(ADD_NEW_TEXT_CHANGES)
        file_page.click_editing_file_commit_button()
        commit_changes_modal = CommitChangesModal(page)
        commit_changes_modal.click_commit_button()
        commits_page = RepoCommitsPage(page)
        assert commits_page.commit_message_label.text_content() == DEFAULT_COMMIT_MESSAGE
        commits_page.header.click_create_button()
        create_menu = CreateMenu(page)
        create_menu.click_create_menu_repo_option("Pull request")
        create_pr_page = RepoCreatePrPage(page)
        create_pr_page.click_create_pr_button()
        pr_page = RepoPrPage(page)
        assert pr_page.page_title.text_content() == DEFAULT_COMMIT_MESSAGE
        expected_pr_url = f'https://bitbucket.org/{workspace}/{TEST_REPO_NAME}/pull-requests/1'
        assert pr_page.page.url == expected_pr_url
        assert pr_page.pr_status.text_content() == "Open"

    def test_review_pr_and_merge(self, page, workspace):
        """Test reviewing and merging a pull request."""
        pr_page = RepoPrPage(page, workspace, TEST_REPO_NAME, 1)
        pr_page.goto()
        assert pr_page.page_title.text_content() == DEFAULT_COMMIT_MESSAGE
        assert pr_page.pr_status.text_content() == "Open"
        pr_page.select_pr_tab('Files changed')
        assert pr_page.code_diff_file_name.text_content() == 'README.md'
        assert pr_page.validate_if_added_line_contains_text(ADD_NEW_TEXT_CHANGES)
        pr_page.select_pr_tab('Overview')
        pr_page.click_approve_button()
        assert pr_page.unapprove_button.is_visible()
        pr_page.click_merge_button()
        merge_pr_modal = MergePrModal(page)
        merge_pr_modal.click_merge_button()
        assert pr_page.pr_status.text_content() == "Merged"
