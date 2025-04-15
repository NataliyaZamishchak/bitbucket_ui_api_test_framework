import uuid
import pytest

from utils.logger import get_logger

logger = get_logger(__name__)

class TestsApi:
    """Test suite for Bitbucket API functionality."""

    @pytest.fixture(scope="module")
    def repo_slug(self):
        """Generate a unique repository slug for testing."""
        return f"test-repo-{uuid.uuid4().hex[:6]}"

    def test_create_repository(self, bitbucket_api, repo_slug):
        """Test the creation of a new repository."""
        response = bitbucket_api.create_repo(repo_slug)
        assert response.status_code in [201, 200], f"Unexpected status: {response.status_code}"
        assert response.json().get("slug", "") == repo_slug

    def test_list_and_validate_repository(self, bitbucket_api, repo_slug):
        """Test listing and validating repository details."""
        response = bitbucket_api.get_repo_info(repo_slug)
        assert response.status_code == 200, f"Unexpected status: {response.status_code}"
        repo_data = response.json()
        assert repo_data.get("slug", "") == repo_slug
        assert repo_data.get("is_private", False) is True

    def test_branching_model(self, bitbucket_api, repo_slug):
        """Test retrieving the branching model of a repository."""
        response = bitbucket_api.get_branching_model(repo_slug)
        assert response.status_code == 200, f"Unexpected status: {response.status_code}"
        assert response.json().get("development", {}).get("use_mainbranch")

    def test_list_commits(self, bitbucket_api, repo_slug, git_repo_name):
        """Test listing commits for a repository."""
        response = bitbucket_api.get_list_commits(repo_slug)
        assert response.status_code == 200, f"Unexpected status: {response.status_code}"
        assert response.json().get("size", 0) == 0

        response = bitbucket_api.get_list_commits(git_repo_name)
        assert response.status_code == 200, f"Unexpected status: {response.status_code}"
        assert response.json().get("pagelen", 0) > 0

    def test_delete_repository(self, bitbucket_api, repo_slug):
        """Test deleting a repository."""
        response = bitbucket_api.delete_repo(repo_slug)
        assert response.status_code == 204
