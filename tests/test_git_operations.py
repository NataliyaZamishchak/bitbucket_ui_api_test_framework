from utils.git_utils import clone_repo, create_test_file, git_status, git_add_all, git_commit, git_push, \
    generate_random_string
import os
from utils.logger import get_logger

logger = get_logger(__name__)

class TestsGitOperations:
    """Test suite for Git operations."""

    def test_clone_repo(self, git_repo_url, cloned_repo_path):
        """Test cloning a Git repository."""
        clone_repo(git_repo_url, dest_folder=cloned_repo_path)
        assert os.path.exists(f"{cloned_repo_path}/.git")

    def test_create_and_commit_file(self, cloned_repo_path):
        """Test creating and committing a file."""
        text = generate_random_string()
        create_test_file(cloned_repo_path, filename="commit.txt", content=text)

        status_before = git_status(cloned_repo_path)
        assert "commit.txt" in status_before

        git_add_all(cloned_repo_path)
        git_commit(cloned_repo_path)

        status_after = git_status(cloned_repo_path)
        assert "nothing to commit" in status_after

    def test_add_commit_push(self, cloned_repo_path):
        """Test adding, committing, and pushing changes."""
        text = generate_random_string()
        create_test_file(cloned_repo_path, filename="pushed.txt", content=text)

        git_add_all(cloned_repo_path)
        git_commit(cloned_repo_path, message="Add pushed.py test file")
        result = git_push(cloned_repo_path)

        assert result.returncode == 0, f"Git push failed: {result.stderr.decode()}"