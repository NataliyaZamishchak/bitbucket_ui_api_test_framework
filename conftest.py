import os
import pytest
from utils.api_requests.api_requests import ApiRequests
from utils.auth.token_manager import TokenManager
from playwright.sync_api import sync_playwright
from utils.context_manager import load_or_login_context

@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as playwright:
        context = load_or_login_context(playwright)
        yield context
        context.close()

@pytest.fixture
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="session")
def bitbucket_username():
    return os.getenv("BITBUCKET_USERNAME")

@pytest.fixture(scope="session")
def bitbucket_password():
    return os.getenv("BITBUCKET_PASSWORD")



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


