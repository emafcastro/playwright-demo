import pytest
from pages.home_login import Login, Navbar
from playwright.sync_api import Playwright, sync_playwright, Page, BrowserContext

# URL = "https://realworld-djangoapp.herokuapp.com"
URL = "http://localhost:8000"
user = {"username": "automation", "email": "automation@test.com", "password": "Test1234"}

# TODO: Move user dictionary to a json file outside

# TODO: Investigate how to apply a base_url

# TODO: Investigate a best way to implement fixtures


""" End to End fixtures """


@pytest.fixture()
def set_up(context: BrowserContext):
    """ Fixture to access the website """
    # TODO: Check how can other browsers be implemented
    page = context.new_page()
    page.goto(URL)
    yield page, context


@pytest.fixture()
def set_up_login(set_up):
    """ Fixture to log in with credentials """
    page, context = set_up

    # page.on("request", lambda request: print(">>", request.method, request.url))
    # page.on("response", lambda response: print("<<", response.status, response.url))

    page.locator(Navbar.SIGN_IN_LNK).click()
    login_page = Login(page)
    login_page.login_with_credentials(user["email"], user["password"])
    page.wait_for_selector("text=Sign Out")
    yield page, context


@pytest.fixture()
def set_up_with_trace():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()
        page.goto(URL)

        page.click(Navbar.SIGN_IN_LNK)
        login_page = Login(page)
        login_page.login_with_credentials(user["email"], user["password"])
        page.wait_for_selector("text=Sign Out")

        yield page

        context.tracing.stop(path="trace.zip")


@pytest.fixture()
def get_api_call(page: Page):
    page.on("request", lambda request: print(">>", request.method, request.url))
    page.on("response", lambda response: print("<<", response.status, response.url))
    yield page

