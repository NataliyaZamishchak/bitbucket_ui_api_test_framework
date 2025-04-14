import requests

class ApiRequests:
    def __init__(self, token: str, workspace: str):
        self.token = token
        self.workspace = workspace
        self.base_url = f"https://api.bitbucket.org/2.0/repositories/{self.workspace}"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }

    def create_repo(self, repo_slug: str, is_private: bool = True):
        url = f"{self.base_url}/{repo_slug}"
        print(f"\nCreating repository at {url} with slug {repo_slug} and privacy {is_private}...")
        headers = {
            "Content-Type": "application/json"
        }
        headers.update(self.headers)
        payload = {
            "scm": "git",
            "is_private": is_private
        }
        response = requests.post(url=url, headers=headers, json=payload)
        print(f'POST request finished with status code: {response.status_code}')
        return response

    def delete_repo(self, repo_slug: str):
        url = f"{self.base_url}/{repo_slug}"
        print(f"\nDeleting repository at {url} with slug {repo_slug}...")
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.delete(url=url, headers=headers)
        print(f'DELETE request finished with status code: {response.status_code}')
        return response

    def get_repo_info(self, repo_slug: str):
        url = f"{self.base_url}/{repo_slug}"
        print(f"\nGetting repository info at {url} with slug {repo_slug}...")
        response = requests.get(url=url, headers=self.headers)
        print(f'GET request finished with status code: {response.status_code}')
        return response

    def get_branching_model(self, repo_slug: str):
        url = f"{self.base_url}/{repo_slug}/branching-model"
        print(f"\nGetting branching model at {url} for repo {repo_slug}...")
        response = requests.get(url=url, headers=self.headers)
        print(f'GET request finished with status code: {response.status_code}')
        return response

    def get_list_commits(self, repo_slug: str):
        url = f"{self.base_url}/{repo_slug}/commits"
        print(f"\nGetting list of commits at {url} for repo {repo_slug}...")
        response = requests.get(url=url, headers=self.headers)
        print(f'GET request finished with status code: {response.status_code}')
        return response