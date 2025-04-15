import random
import string
import subprocess
import os
import shutil
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)


def clone_repo(repo_url: str, dest_folder: str = "cloned_repo") -> None:
    """Clone a Git repository to the specified destination folder."""
    try:
        logger.info(f"Cloning repository from {repo_url} to {dest_folder}")
        subprocess.run(["git", "clone", repo_url, dest_folder], check=True)
        logger.info(f"Repository cloned successfully to {dest_folder}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to clone repository: {e}")
        raise


def create_test_file(repo_path: str, filename: str = "hello.py", content: str = 'print("Hello")') -> None:
    """Create a test file with the specified content in the repository."""
    try:
        file_path = Path(repo_path) / filename
        logger.info(f"Creating test file at {file_path}")
        with open(file_path, "w") as f:
            f.write(content)
        logger.info(f"Test file {filename} created successfully")
    except Exception as e:
        logger.error(f"Failed to create test file: {e}")
        raise


def git_status(repo_path: str) -> str:
    """Get the Git status of the repository."""
    try:
        logger.info(f"Getting Git status for repository at {repo_path}")
        result = subprocess.run(["git", "status"], cwd=repo_path, capture_output=True, text=True)
        logger.info("Git status retrieved successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to get Git status: {e}")
        raise


def git_add_all(repo_path: str) -> None:
    """Stage all changes in the repository."""
    try:
        logger.info(f"Staging all changes in repository at {repo_path}")
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        logger.info("All changes staged successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to stage changes: {e}")
        raise


def git_commit(repo_path: str, message: str = "Add test file") -> None:
    """Commit staged changes with the specified message."""
    try:
        logger.info(f"Committing changes in repository at {repo_path} with message: {message}")
        subprocess.run(["git", "commit", "-m", message], cwd=repo_path, check=True)
        logger.info("Changes committed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to commit changes: {e}")
        raise


def git_push(repo_path: str, branch: str = "main") -> subprocess.CompletedProcess[str]:
    """Push committed changes to the remote repository."""
    try:
        logger.info(f"Pushing changes to branch {branch} in repository at {repo_path}")
        result = subprocess.run(
            ["git", "push"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        logger.info("Changes pushed successfully")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to push changes: {e}")
        raise


def generate_random_string(length=10):
    """Generate a random alphanumeric string of the specified length."""
    logger.info(f"Generating random string of length {length}")
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def delete_cloned_repo(repo_path: Path):
    """Delete the cloned repository at the specified path."""
    try:
        logger.info(f"Deleting repository at {repo_path}")
        os.chmod(repo_path, 0o777)
        shutil.rmtree(repo_path)
        logger.info(f"Repository at {repo_path} deleted successfully")
    except Exception as e:
        logger.error(f"Error while deleting the repository: {e}")
        raise

