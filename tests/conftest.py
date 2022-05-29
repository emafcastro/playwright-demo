import os

import pytest
from models.home_login import Login, Navbar
from helpers.user_helper import maketoken, login_user_via_api
from playwright.sync_api import sync_playwright, BrowserContext, Page

from dotenv import load_dotenv

load_dotenv()

# TODO Implement Report Portal

""" End to End fixtures """


@pytest.fixture()
def set_up_login(page: Page):
    """ Fixture to log in with credentials """
    login_user_via_api(page.context, os.environ["TEST_EMAIL"], os.environ["TEST_PASSWORD"])
    page.goto("/")

    yield page


@pytest.fixture()
def set_up_with_trace():
    """ Fixture to use for debugging """

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()
        page.goto("http://localhost:8000/")

        page.click(Navbar.SIGN_IN_LNK)
        login_page = Login(page)
        login_page.login_with_credentials(os.environ["TEST_EMAIL"], os.environ["TEST_PASSWORD"])
        page.wait_for_selector("text=Sign Out")

        yield page

        context.tracing.stop(path="trace.zip")


""" API Fixtures """


@pytest.fixture()
def generate_user_context(context: BrowserContext):
    csrftoken = maketoken(64)
    token = {"name": "csrftoken", "value": csrftoken, 'path': '/',
             'domain': f'{os.environ["DOMAIN"]}'}
    context.add_cookies([token])
    yield context
    context.close()
