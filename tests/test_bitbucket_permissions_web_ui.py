from pom.modals.add_users_or_groups_modal import AddUserOrGroupsModal
from pom.modals.commit_changes_modal import CommitChangesModal
from pom.modals.create_menu_component import CreateMenu
from pom.modals.merge_pr_modal import MergePrModal
from pom.modals.remove_repo_access_modal import RemoveRepoAccessModal
from pom.pages.atlassian_login_page import AtlassianLoginPage
from pom.pages.create_repo_page import CreateRepoPage
from pom.pages.overview_page import OverviewPage
from pom.pages.repo.branches.repo_branches_page import RepoBranchesPage
from pom.pages.repo.branches.repo_create_branch_page import CreateBranchPage
from pom.pages.repo.commits.repo_commits_page import RepoCommitsPage
from pom.pages.repo.pr.repo_create_pr_page import RepoCreatePrPage
from pom.pages.repo.pr.repo_pr_page import RepoPrPage
from pom.pages.repo.repo_settings.repo_permissions_page import RepoPermissionsPage
from pom.pages.repo.source.repo_source_file_page import RepoSourceFilePage
from pom.pages.repo.source.repo_source_page import RepoSourcePage
import uuid
from utils.logger import get_logger

logger = get_logger(__name__)

TEST_REPO_NAME = f"test_repo_permissions_{uuid.uuid4().hex[:8]}"
TEST_BRANCH_NAME = f"test_branch_{uuid.uuid4().hex[:8]}"
TEST_BRANCH_NAME_2 = f"test_branch_{uuid.uuid4().hex[:8]}"
ADD_NEW_TEXT_CHANGES = "Add new text to README.md"
DEFAULT_COMMIT_MESSAGE = 'README.md edited online with Bitbucket'
ERROR_SOURCE_REPO_PAGE = 'Repository not found'

class TestsPermissionsWebUi:
    """Test suite for testing repository permissions via the Bitbucket Web UI."""

    def test_create_repo_for_permissions_tests(self, fresh_page, workspace, admin_email, admin_password):
        """Test creating a repository for permissions testing."""
        login_page = AtlassianLoginPage(fresh_page, fresh_page.context, workspace)
        login_page.login(admin_email, admin_password, save_state=False)
        assert login_page.success_login_img.is_visible(), "Login failed or success image not visible."
        overview_page = OverviewPage(fresh_page, workspace)
        overview_page.goto()
        overview_page.header.click_create_button()
        create_menu = CreateMenu(fresh_page)
        create_menu.click_create_menu_option("Repository")
        create_repo_page = CreateRepoPage(fresh_page, workspace)
        create_repo_page.select_first_project()
        create_repo_page.repo_name_input.fill(TEST_REPO_NAME)
        create_repo_page.click_create_button()
        repo_page = RepoSourcePage(fresh_page, workspace, TEST_REPO_NAME)
        assert repo_page.page_title.text_content() == TEST_REPO_NAME

    def test_create_pr_for_permissions_tests(self, fresh_page, workspace, admin_email, admin_password):
        """Test creating a pull request for permissions testing."""
        login_page = AtlassianLoginPage(fresh_page, fresh_page.context, workspace)
        login_page.login(admin_email, admin_password, save_state=False)
        assert login_page.success_login_img.is_visible(), "Login failed or success image not visible."
        repo_page = RepoSourcePage(fresh_page, workspace, TEST_REPO_NAME)
        repo_page.goto()
        repo_page.header.click_create_button()
        create_menu = CreateMenu(fresh_page)
        create_menu.click_create_menu_repo_option("Branch")
        create_branch_page = CreateBranchPage(fresh_page, workspace, TEST_REPO_NAME)
        create_branch_page.select_branch_type('Feature')
        create_branch_page.branch_name_input.fill(TEST_BRANCH_NAME)
        create_branch_page.click_create_button()
        branch_page = RepoBranchesPage(fresh_page)
        assert branch_page.page_title.text_content() == "feature/" + TEST_BRANCH_NAME
        branch_page.click_view_source_button()
        repo_page.click_target_file('README.md')
        file_page = RepoSourceFilePage(fresh_page)
        assert file_page.page_title.text_content() == 'README.md'
        file_page.click_edit_file_button()
        assert 'Editing' in file_page.editing_file_form_title.text_content()
        file_page.editing_file_textarea.type(ADD_NEW_TEXT_CHANGES)
        file_page.click_editing_file_commit_button()
        commit_changes_modal = CommitChangesModal(fresh_page)
        commit_changes_modal.click_commit_button()
        commits_page = RepoCommitsPage(fresh_page)
        assert commits_page.commit_message_label.text_content() == DEFAULT_COMMIT_MESSAGE
        commits_page.header.click_create_button()
        create_menu = CreateMenu(fresh_page)
        create_menu.click_create_menu_repo_option("Pull request")
        create_pr_page = RepoCreatePrPage(fresh_page)
        create_pr_page.click_create_pr_button()
        pr_page = RepoPrPage(fresh_page)
        assert pr_page.page_title.text_content() == DEFAULT_COMMIT_MESSAGE
        expected_pr_url = f'https://bitbucket.org/{workspace}/{TEST_REPO_NAME}/pull-requests/1'
        assert pr_page.page.url == expected_pr_url
        assert pr_page.pr_status.text_content() == "Open"

    def test_give_user2_read_permissions_to_repo(self, fresh_page, workspace, admin_email, admin_password,
                                                 read_full_username):
        """Test giving a user read permissions to the repository."""
        login_page = AtlassianLoginPage(fresh_page, fresh_page.context, workspace)
        login_page.login(admin_email, admin_password, save_state=False)
        assert login_page.success_login_img.is_visible(), "Login failed or success image not visible."
        repo_page = RepoSourcePage(fresh_page, workspace, TEST_REPO_NAME)
        repo_page.goto()
        assert repo_page.page_title.text_content() == TEST_REPO_NAME
        repo_page.side_menu.click_side_menu_option('Repository settings')
        repo_page.side_menu.click_side_menu_option('Repository permissions')
        repo_permissions_page = RepoPermissionsPage(fresh_page)
        repo_permissions_page.click_add_user_or_group_button()
        add_users_modal = AddUserOrGroupsModal(fresh_page)
        add_users_modal.select_user_to_add(read_full_username)
        add_users_modal.click_confirm_button()
        repo_permissions_page.page_title.wait_for(state="visible")
        repo_permissions_page.permission_table.wait_for(state="visible")
        assert repo_permissions_page.page_title.is_visible()
        assert repo_permissions_page.permission_table.is_visible()
        user_data = repo_permissions_page.users_permissions_table.get_user_row_data(read_full_username)
        assert user_data.get("Permission", '') == "Read"
        assert user_data.get("Access level", '') == "Repository"

    def test_user2_login_with_read_permissions_to_repo(self, fresh_page, workspace, read_email, read_password):
        """Test user login with read permissions to the repository."""
        login_page = AtlassianLoginPage(fresh_page, fresh_page.context, workspace)
        login_page.login(read_email, read_password, save_state=False)
        assert login_page.success_login_img.is_visible(), "Login failed or success image not visible."
        repo_page = RepoSourcePage(fresh_page, workspace, TEST_REPO_NAME)
        repo_page.goto()
        assert repo_page.page_title.text_content() == TEST_REPO_NAME
        repo_page.header.click_create_button()
        create_menu = CreateMenu(fresh_page)
        assert not create_menu.validate_if_exists_create_menu_repo_option("Branch")
        assert not create_menu.validate_if_exists_create_menu_repo_option("Pull request")
        repo_page.click_target_file('README.md')
        file_page = RepoSourceFilePage(fresh_page)
        assert file_page.page_title.text_content() == 'README.md'
        assert file_page.edit_file_button.is_disabled()
        pr_page = RepoPrPage(fresh_page, workspace, TEST_REPO_NAME, 1)
        pr_page.goto()
        assert pr_page.page_title.text_content() == DEFAULT_COMMIT_MESSAGE
        assert pr_page.pr_status.text_content() == "Open"
        assert pr_page.approve_button.is_visible()
        assert pr_page.approve_button.is_enabled()
        assert pr_page.merge_button.count() == 0

    def test_give_user2_write_permissions_to_repo(self, fresh_page, workspace, admin_email, admin_password,
                                                  read_full_username):
        """Test user login with read permissions to the repository."""
        login_page = AtlassianLoginPage(fresh_page, fresh_page.context, workspace)
        login_page.login(admin_email, admin_password, save_state=False)
        assert login_page.success_login_img.is_visible(), "Login failed or success image not visible."
        repo_page = RepoSourcePage(fresh_page, workspace, TEST_REPO_NAME)
        repo_page.goto()
        assert repo_page.page_title.text_content() == TEST_REPO_NAME
        repo_page.side_menu.click_side_menu_option('Repository settings')
        repo_page.side_menu.click_side_menu_option('Repository permissions')
        repo_permissions_page = RepoPermissionsPage(fresh_page)
        repo_permissions_page.page_title.wait_for(state="visible")
        repo_permissions_page.permission_table.wait_for(state="visible")
        assert repo_permissions_page.page_title.is_visible()
        assert repo_permissions_page.permission_table.is_visible()
        repo_permissions_page.users_permissions_table.set_user_permission(read_full_username, 'Write')
        user_data = repo_permissions_page.users_permissions_table.get_user_row_data(read_full_username)
        assert user_data.get("Permission", '') == "Write"
        assert user_data.get("Access level", '') == "Repository"

    def test_user2_login_with_write_permissions_to_repo(self, fresh_page, workspace, read_email, read_password):
        """Test user login with write permissions."""
        login_page = AtlassianLoginPage(fresh_page, fresh_page.context, workspace)
        login_page.login(read_email, read_password, save_state=False)
        assert login_page.success_login_img.is_visible(), "Login failed or success image not visible."
        repo_page = RepoSourcePage(fresh_page, workspace, TEST_REPO_NAME)
        repo_page.goto()
        assert repo_page.page_title.text_content() == TEST_REPO_NAME
        repo_page.header.click_create_button()
        create_menu = CreateMenu(fresh_page)
        create_menu.click_create_menu_repo_option("Branch")
        create_branch_page = CreateBranchPage(fresh_page, workspace, TEST_REPO_NAME)
        create_branch_page.select_branch_type('Feature')
        create_branch_page.branch_name_input.fill(TEST_BRANCH_NAME_2)
        create_branch_page.click_create_button()
        branch_page = RepoBranchesPage(fresh_page)
        assert branch_page.page_title.text_content() == "feature/" + TEST_BRANCH_NAME_2
        branch_page.click_view_source_button()
        repo_page.click_target_file('README.md')
        file_page = RepoSourceFilePage(fresh_page)
        assert file_page.page_title.text_content() == 'README.md'
        file_page.click_edit_file_button()
        assert 'Editing' in file_page.editing_file_form_title.text_content()
        file_page.editing_file_textarea.type(ADD_NEW_TEXT_CHANGES)
        file_page.click_editing_file_commit_button()
        commit_changes_modal = CommitChangesModal(fresh_page)
        commit_changes_modal.click_commit_button()
        commits_page = RepoCommitsPage(fresh_page)
        assert commits_page.commit_message_label.text_content() == DEFAULT_COMMIT_MESSAGE
        commits_page.header.click_create_button()
        create_menu = CreateMenu(fresh_page)
        create_menu.click_create_menu_repo_option("Pull request")
        create_pr_page = RepoCreatePrPage(fresh_page)
        create_pr_page.click_create_pr_button()
        pr_page = RepoPrPage(fresh_page)
        assert pr_page.page_title.text_content() == DEFAULT_COMMIT_MESSAGE
        expected_pr_url = f'https://bitbucket.org/{workspace}/{TEST_REPO_NAME}/pull-requests/2'
        assert pr_page.page.url == expected_pr_url
        assert pr_page.pr_status.text_content() == "Open"
        pr_page.select_pr_tab('Files changed')
        assert pr_page.code_diff_file_name.text_content() == 'README.md'
        assert pr_page.validate_if_added_line_contains_text(ADD_NEW_TEXT_CHANGES)
        pr_page.select_pr_tab('Overview')
        pr_page.click_approve_button()
        assert pr_page.unapprove_button.is_visible()
        pr_page.click_merge_button()
        merge_pr_modal = MergePrModal(fresh_page)
        merge_pr_modal.click_merge_button()
        assert pr_page.pr_status.text_content() == "Merged"

    def test_user2_delete_permissions_to_repo(self, fresh_page, workspace, admin_email, admin_password,
                                              read_full_username):
        """Test removing user permissions from the repository."""
        login_page = AtlassianLoginPage(fresh_page, fresh_page.context, workspace)
        login_page.login(admin_email, admin_password, save_state=False)
        assert login_page.success_login_img.is_visible(), "Login failed or success image not visible."
        repo_page = RepoSourcePage(fresh_page, workspace, TEST_REPO_NAME)
        repo_page.goto()
        assert repo_page.page_title.text_content() == TEST_REPO_NAME
        repo_page.side_menu.click_side_menu_option('Repository settings')
        repo_page.side_menu.click_side_menu_option('Repository permissions')
        repo_permissions_page = RepoPermissionsPage(fresh_page)
        repo_permissions_page.page_title.wait_for(state="visible")
        repo_permissions_page.permission_table.wait_for(state="visible")
        assert repo_permissions_page.page_title.is_visible()
        assert repo_permissions_page.permission_table.is_visible()
        repo_permissions_page.users_permissions_table.click_remove_button(read_full_username)
        remove_access_modal = RemoveRepoAccessModal(fresh_page)
        assert remove_access_modal.modal_title.inner_text() == 'Remove access'
        remove_access_modal.click_remove_button()
        assert repo_permissions_page.users_permissions_table.get_row_by_username(read_full_username) is None

    def test_user2_login_with_no_permissions_to_repo(self, fresh_page, workspace, read_email, read_password):
        """Test user login with no permissions to the repository."""
        login_page = AtlassianLoginPage(fresh_page, fresh_page.context, workspace)
        login_page.login(read_email, read_password, save_state=False)
        assert login_page.success_login_img.is_visible(), "Login failed or success image not visible."
        repo_page = RepoSourcePage(fresh_page, workspace, TEST_REPO_NAME)
        repo_page.goto()
        assert repo_page.page_error.inner_text() == ERROR_SOURCE_REPO_PAGE
