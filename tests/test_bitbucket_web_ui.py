import pytest
from playwright.sync_api import Page
from pom.pages.atlassian_login_page import AtlassianLoginPage


def test_login_setup(page, bitbucket_username, bitbucket_password):
    login_page = AtlassianLoginPage(page, page.context)
    login_page.login(bitbucket_username, bitbucket_password)
    assert login_page.success_login_img.is_visible(), "Login failed or success image not visible."