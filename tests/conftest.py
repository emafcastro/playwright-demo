import pytest
from playwright.async_api import async_playwright
from playwright.sync_api import Page
from pages.home_login import Login, Navbar

# URL = 'http://127.0.0.1:8080'
URL = "https://mits-gossau.github.io/event-driven-web-components-realworld-example-app"

user = {"username": "automation", "email": "automation@test.com", "password": "Test1234"}


@pytest.fixture()
@pytest.mark.asyncio
async def set_up():
    """ Fixture to access the website """
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()
        await page.goto(URL)
        yield page


@pytest.fixture()
@pytest.mark.asyncio
async def set_up_login(set_up):
    """ Fixture to log in with credentials """
    page = set_up
    await page.click(Navbar.SIGN_IN_LNK)
    login_page = Login(page)
    await login_page.login_with_credentials(user["email"], user["password"])
    yield page


@pytest.fixture()
@pytest.mark.asyncio
async def set_up_with_trace():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = await context.new_page()
        await page.goto(URL)

        await page.click(Navbar.SIGN_IN_LNK)
        login_page = Login(page)
        await login_page.login_with_credentials(user["email"], user["password"])

        yield page

        await context.tracing.stop(path="trace.zip")
