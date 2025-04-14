import os
import pytest
import allure
from pathlib import Path
import subprocess
# from utils.api_requests.api_requests import ApiRequests
# from utils.auth.token_manager import TokenManager
from playwright.sync_api import sync_playwright
from utils.context_manager import load_or_login_context
from dotenv import load_dotenv

from utils.git_utils import delete_cloned_repo

load_dotenv()

SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)

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

@pytest.fixture
def fresh_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

@pytest.fixture
def fresh_page(fresh_context):
    page = fresh_context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="session")
def username_1():
    return os.getenv("BITBUCKET_USERNAME")

@pytest.fixture(scope="session")
def password_1():
    return os.getenv("BITBUCKET_PASSWORD")

@pytest.fixture(scope="session")
def username_2():
    return os.getenv("BITBUCKET_USERNAME_1")

@pytest.fixture(scope="session")
def password_2():
    return os.getenv("BITBUCKET_PASSWORD_1")

@pytest.fixture(scope="session")
def workspace():
    return os.getenv("BITBUCKET_ORGANIZATION_NAME")

@pytest.fixture(scope="session")
def git_repo_name():
    return os.getenv("GIT_REPO_NAME")

@pytest.fixture(scope="session", autouse=True)
def git_repo_url(workspace, git_repo_name):
    username = os.getenv("GIT_USERNAME")
    password = os.getenv("GIT_APP_PASSWORD")
    return f"https://{username}:{password}@bitbucket.org/{workspace}/{git_repo_name}.git"

@pytest.fixture(scope="session", autouse=True)
def cloned_repo_path(git_repo_name):
    repo_name = f'cloned_repo/{git_repo_name}'
    repo_path = Path.cwd() / repo_name
    print(f"Cloned repo path: {repo_path}")
    return repo_path

@pytest.fixture(scope="session", autouse=True)
def cleanup_repo(cloned_repo_path):
    yield
    if cloned_repo_path.exists():
        delete_cloned_repo(cloned_repo_path)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot_path = SCREENSHOT_DIR / f"{item.name}.png"
            page.screenshot(path=str(screenshot_path))
            allure.attach.file(
                str(screenshot_path),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
# @pytest.fixture(scope="session", autouse=True)
# def run_tests_and_generate_report():
#     subprocess.run(["pytest", "--alluredir=allure-results"])
#     subprocess.run(["allure", "generate", "allure-results", "--clean", "-o", "allure-report"])
#     subprocess.run(["allure", "open", "allure-report"])

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


