import os
import pytest
from utils.api_requests.api_requests import ApiRequests
from utils.auth.token_manager import TokenManager

# @pytest.fixture(scope="session")
# def bitbucket_auth():
#     username = os.getenv("BITBUCKET_USERNAME")
#     app_password = os.getenv("BITBUCKET_APP_PASSWORD")
#     return HTTPBasicAuth(username, app_password)

# @pytest.fixture(scope="session")
# def base_url():
#     return "https://api.bitbucket.org/2.0/repositories"

# @pytest.fixture(scope="module")
# def repo_slug():
#     import uuid
#     return f"test-repo-{uuid.uuid4().hex[:6]}"
# conftest.py


@pytest.fixture(scope="session")
def bitbucket_api():
    token_manager = TokenManager()
    token = token_manager.get_or_refresh_token()
    return ApiRequests(token=token, workspace=os.getenv("BITBUCKET_ORGANIZATION_NAME"))


