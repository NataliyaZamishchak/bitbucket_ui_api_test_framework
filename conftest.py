import os

import allure
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright
from utils.git_utils import delete_cloned_repo
from utils.api.api_requests import ApiRequests
from utils.api.token_manager import TokenManager
from utils.context_manager import load_or_login_context
from dotenv import load_dotenv

from utils.logger import get_logger

load_dotenv()
logger = get_logger("pytest-logger")


@pytest.fixture(autouse=True)
def log_test_flow(request):
    """Log the start and end of each test."""
    logger.info(f"START test: {request.node.name}")
    yield
    logger.info(f"END test:   {request.node.name}")


@pytest.fixture(scope="session")
def browser_context(admin_email, admin_password):
    """Provide a Playwright browser context for the session."""
    with sync_playwright() as playwright:
        logger.info("Initializing browser context with admin credentials.")
        context = load_or_login_context(playwright, admin_email, admin_password)
        yield context
        logger.info("Closing browser context.")
        context.close()


@pytest.fixture
def page(browser_context):
    """Provide a new page from the browser context."""
    logger.info("Creating a new page from the browser context.")
    page = browser_context.new_page()
    yield page
    logger.info("Closing the page.")
    page.close()


@pytest.fixture
def fresh_context():
    """Provide a fresh Playwright browser context."""
    with sync_playwright() as p:
        logger.info("Launching a fresh browser context.")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        yield context
        logger.info("Closing the fresh browser context.")
        context.close()
        browser.close()


@pytest.fixture
def fresh_page(fresh_context):
    """Provide a new page from a fresh browser context."""
    logger.info("Creating a new page from the fresh browser context.")
    page = fresh_context.new_page()
    yield page
    logger.info("Closing the fresh page.")
    page.close()


@pytest.fixture(scope="session")
def admin_email():
    """Provide the admin email from environment variables."""
    return os.getenv("ADMIN_EMAIL")


@pytest.fixture(scope="session")
def admin_password():
    """Provide the admin password from environment variables."""
    return os.getenv("ADMIN_PASSWORD")


@pytest.fixture(scope="session")
def read_email():
    """Provide the read-only email from environment variables."""
    return os.getenv("READ_EMAIL")


@pytest.fixture(scope="session")
def read_password():
    """Provide the read-only password from environment variables."""
    return os.getenv("READ_PASSWORD")


@pytest.fixture(scope="session")
def read_full_username():
    """Provide the full username for the read-only account."""
    return os.getenv("READ_FULL_USERNAME")


@pytest.fixture(scope="session")
def workspace():
    """Provide the workspace name from environment variables."""
    return os.getenv("WORKSPACE")


@pytest.fixture(scope="session")
def git_repo_name():
    """Provide the Git repository name from environment variables."""
    return os.getenv("GIT_REPO_NAME")


@pytest.fixture(scope="session", autouse=True)
def git_repo_url(workspace, git_repo_name):
    """Construct the Git repository URL using credentials and workspace."""
    username = os.getenv("GIT_USERNAME")
    password = os.getenv("GIT_APP_PASSWORD")
    repo_url = f"https://{username}:{password}@bitbucket.org/{workspace}/{git_repo_name}.git"
    logger.info(f"Constructed Git repository URL")
    return repo_url


@pytest.fixture(scope="session", autouse=True)
def cloned_repo_path(git_repo_name):
    """Provide the path to the cloned repository."""
    repo_name = f'cloned_repo/{git_repo_name}'
    repo_path = Path.cwd() / repo_name
    logger.info(f"Cloned repository path: {repo_path}")
    return repo_path


# @pytest.fixture(scope="session", autouse=True)
# def cleanup_repo(cloned_repo_path):
#     """Cleanup the cloned repository after the session."""
#     yield
#     if cloned_repo_path.exists():
#         logger.info(f"Cleaning up cloned repository at {cloned_repo_path}")
#         delete_cloned_repo(cloned_repo_path)


@pytest.fixture(scope="session")
def bitbucket_api(workspace):
    """Provide an API client for Bitbucket."""
    logger.info("Initializing Bitbucket API client.")
    token_manager = TokenManager(workspace)
    token = token_manager.get_or_refresh_token()
    return ApiRequests(token=token, workspace=workspace)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_call(item):
    doc = item.function.__doc__
    if doc:
        doc = doc.strip()
        allure.dynamic.title(doc)
    yield


