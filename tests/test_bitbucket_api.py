import requests
import uuid
import pytest

@pytest.fixture(scope="module")
def repo_slug():
    return f"test-repo-{uuid.uuid4().hex[:6]}"

def test_create_repository(bitbucket_api, repo_slug):
    response = bitbucket_api.create_repo(repo_slug)

    assert response.status_code in [201, 200], f"Unexpected status: {response.status_code}"
    assert response.json()["slug"] == repo_slug

# def test_list_and_validate_repository(base_url, bitbucket_auth, repo_slug):
#     username = bitbucket_auth.username
#     url = f"{base_url}/{username}/{repo_slug}"

#     response = requests.get(url, auth=bitbucket_auth)
#     assert response.status_code == 200
#     repo_data = response.json()
#     assert repo_data["slug"] == repo_slug
#     assert repo_data["is_private"] is True

# def test_branch_and_commit_operations(base_url, bitbucket_auth, repo_slug):
#     # Бітбакет API не дозволяє комітити напряму через REST
#     # Але можна отримати список бранчів
#     username = bitbucket_auth.username
#     branches_url = f"{base_url}/{username}/{repo_slug}/refs/branches"

#     response = requests.get(branches_url, auth=bitbucket_auth)
#     assert response.status_code == 200
#     data = response.json()
#     assert "values" in data
#     assert any(branch["name"] == "main" or branch["name"] == "master" for branch in data["values"])

# def test_delete_repository(base_url, bitbucket_auth, repo_slug):
#     username = bitbucket_auth.username
#     url = f"{base_url}/{username}/{repo_slug}"

#     response = requests.delete(url, auth=bitbucket_auth)
#     assert response.status_code == 204
