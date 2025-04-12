import requests

class ApiRequests:
    def __init__(self, token: str, workspace: str):
        self.token = token
        self.workspace = workspace
        self.base_url = f"https://api.bitbucket.org/2.0/repositories/{self.workspace}"

    def create_repo(self, repo_slug: str, is_private: bool = True):
        url = f"{self.base_url}/{repo_slug}"
        print(f"Creating repository at {url} with slug {repo_slug} and privacy {is_private}...")
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = {
            "scm": "git",
            "is_private": is_private
        }
        response = requests.post(url, headers=headers, json=payload)
        return response
