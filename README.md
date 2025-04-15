# Bitbucket Test Automation Framework

This repository contains automated tests for verifying Bitbucket functionality via Web UI and API. The tests cover areas such as repository management, access permissions, pull request creation, commits, and other operations.

## Requirements

- Python 3.8+
- `requests` — For making HTTP requests to Bitbucket API.
- `pytest` — For running the test suite.
- `pytest-xdist` — For parallel test execution.
- `playwright` — For browser automation.
- `python-dotenv` — For managing environment variables.
- `allure-pytest` — For generating test reports.

## Setup

Before running the tests:

1. Create a `.env` file in the root directory of the repository based on the `.env.example` file. Populate it with the required variables.

   ### Environment Variables

   #### Bitbucket Workspace

   - `WORKSPACE` — Your Bitbucket Workspace name (with at least 1 project added).

   #### Admin User Credentials

   - `ADMIN_EMAIL` — Admin email address.
   - `ADMIN_PASSWORD` — Admin password.

   #### Read-Only User Credentials

   - `READ_EMAIL` — Email address of the read-only user.
   - `READ_PASSWORD` — Password of the read-only user.
   - `READ_FULL_USERNAME` — Full username of the read-only user.

   #### OAuth2 for Bitbucket API

   - `BITBUCKET_CLIENT_ID` — Your OAuth2 Client ID for Bitbucket workspace with `repository:admin` role.
   - `BITBUCKET_CLIENT_SECRET` — Your OAuth2 Client Secret for Bitbucket workspace.

   #### Git Configuration for repo

   - `GIT_USERNAME` — Git username (shortened from email).
   - `GIT_APP_PASSWORD` — Git App Password (set up for particular repo).
   - `GIT_REPO_NAME` — Name of the repository for testing Git operations.

2. Go through OAuth2 implementation steps (1-3) from [OAuth2 Documentation for Bitbucket](https://developer.atlassian.com/cloud/bitbucket/rest/intro/#oauth-2-0) using `BITBUCKET_CLIENT_ID` and `BITBUCKET_CLIENT_SECRET`. Write the result output to the `token.json` file in the root of this repository.

## Running Tests

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Install Playwright browsers:

   ```bash
   playwright install
   ```

3. Install Allure command-line tool:

   ```bash
   npm install -g allure-commandline --save-dev
   ```

4. Run the tests:

   ```bash
   pytest -n 4 --dist=loadscope --alluredir=allure-results
   ```

5. Generate Allure report and open locally:

   ```bash
   allure generate allure-results --clean -o allure-report
   allure open allure-report
   ```

## Test Description

### Web UI Tests

These tests are located in `tests/test_bitbucket_web_ui.py` and cover the following scenarios:

- **Admin login to Bitbucket**
- **Creating a new repository**
- **Creating a pull request**
- **Reviewing and merging a pull request**

### Web UI Permissions Tests

These tests are located in `tests/test_bitbucket_permissions_web_ui.py` and cover the following scenarios:

- **Granting Permissions to a repo for user**
- **Revoking Permissions to a repo for user**
- **User Permission Validation**

### API Tests

These tests are located in `tests/test_bitbucket_api.py` and cover the following scenarios:

- **Repository Creation**
- **Fetching Repository Details**
- **Repository Deletion**

### Git Operations Tests

These tests are located in `tests/test_git_operations.py` and cover the following scenarios:

- **Repository Cloning**
- **File Creation and Commit**
- **Pushing Changes**

## Project Structure

- `tests/` — Contains tests for Web UI, API, and Git.
- `pom/` — Page Object Model for interacting with UI elements.
- `utils/` — Utilities for working with API, Git, and other services.
- `.env.example` — Example file for environment variables.

## Additional Notes

- All actions are logged in console and added to file `logs/test.log`.
- All tests, classes, functions are pytest documented.
- Allure report generated under `allure-report`

### Useful Links

- [Playwright Documentation](https://playwright.dev/)
- [pytest Documentation](https://docs.pytest.org/)
- [Allure Documentation](https://docs.qameta.io/allure/)
- [Bitbucket API Documentation](https://developer.atlassian.com/cloud/bitbucket/rest/api-group-source/)
- [OAuth2 Documentation for Bitbucket](https://developer.atlassian.com/cloud/bitbucket/rest/intro/#oauth-2-0)

## Author

Code written by **@Nataliia Zamishchak**.
