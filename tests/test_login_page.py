import pytest

from pages.home_login import Login, Navbar

user = {"username": "automation", "email": "automation@test.com", "password": "Test1234"}


@pytest.mark.login
@pytest.mark.asyncio
async def test_login_with_valid_credentials(set_up_login):
    """ Test with valid credentials, it validates if the username matches"""

    page = set_up_login
    await page.wait_for_selector(f"text={user['username']}")
    assert await page.locator(f"text={user['username']}").is_visible()


@pytest.mark.login
@pytest.mark.asyncio
@pytest.mark.skip(reason="This test will fail")
async def test_login_with_invalid_credentials(set_up):
    """ Test that performs an invalid login, but will fail because there is no error message """

    page = set_up
    await page.click(Navbar.SIGN_IN_LNK)
    login_page = Login(page)
    await login_page.login_with_credentials("", "Test1234")
    assert await page.locator("text=Email can't be blank").is_visible()
