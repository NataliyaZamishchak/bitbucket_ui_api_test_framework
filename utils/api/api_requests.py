import requests
from utils.logger import get_logger

logger = get_logger(__name__)

class ApiRequests:
    """Bitbucket API wrapper using OAuth2 token for repository and branch operations."""

    def __init__(self, token: str, workspace: str):
        """Init with token and workspace."""
        self.token = token
        self.workspace = workspace
        self.base_url = f"https://api.bitbucket.org/2.0/repositories/{self.workspace}"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }

    def create_repo(self, repo_slug: str, is_private: bool = True):
        """Create a new repository."""
        url = f"{self.base_url}/{repo_slug}"
        logger.info(f"Creating repo '{repo_slug}' (private={is_private})")
        headers = {"Content-Type": "application/json", **self.headers}
        payload = {
            "scm": "git",
            "is_private": is_private
        }
        response = requests.post(url=url, headers=headers, json=payload)
        logger.info(f'POST request finished with status code: {response.status_code}')
        return response

    def delete_repo(self, repo_slug: str):
        """Delete an existing repository."""
        url = f"{self.base_url}/{repo_slug}"
        logger.info(f"Deleting repo '{repo_slug}'")
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.delete(url=url, headers=headers)
        logger.info(f'DELETE request finished with status code: {response.status_code}')
        return response

    def get_repo_info(self, repo_slug: str):
        """Get repository info."""
        url = f"{self.base_url}/{repo_slug}"
        logger.info(f"Getting info for repo '{repo_slug}'")
        response = requests.get(url=url, headers=self.headers)
        logger.info(f'GET request finished with status code: {response.status_code}')
        return response

    def get_branching_model(self, repo_slug: str):
        """Get branching model config."""
        url = f"{self.base_url}/{repo_slug}/branching-model"
        logger.info(f"Getting branching model for '{repo_slug}'")
        response = requests.get(url=url, headers=self.headers)
        logger.info(f'GET request finished with status code: {response.status_code}')
        return response

    def get_list_commits(self, repo_slug: str):
        """List commits in a repository."""
        url = f"{self.base_url}/{repo_slug}/commits"
        logger.info(f"Getting commits for repo '{repo_slug}'")
        response = requests.get(url=url, headers=self.headers)
        logger.info(f'GET request finished with status code: {response.status_code}')
        return response