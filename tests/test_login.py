import os
import pytest

from models.home_login import Login, Navbar
from playwright.sync_api import Page
from dotenv import load_dotenv

load_dotenv()


@pytest.mark.login
def test_login_with_valid_credentials(page: Page):
    """ Test with valid credentials """
    page.goto("/")
    page.locator(Navbar.SIGN_IN_LNK).click()
    login_page = Login(page)
    login_page.login_with_credentials(os.environ["TEST_EMAIL"], os.environ["TEST_PASSWORD"])
    page.wait_for_selector("text=Sign Out")
    assert page.locator("text=Sign Out").is_visible()


@pytest.mark.login
def test_login_with_empty_field(page: Page):
    """ Test that performs an invalid login """

    page.goto("/login/")
    page.click(Navbar.SIGN_IN_LNK)
    Login(page).login_with_credentials(" ", "Test1234")
    assert page.locator(Login.ERROR_MESSAGE_DIV).inner_text() == "* This field is required."


@pytest.mark.login
def test_login_with_incorrect_email_and_password(page: Page):
    """ Test that performs an invalid login by missmatch email and password """

    error_message = "* Please enter a correct Email Address and password. Note that both fields may be case-sensitive."

    page.goto("/login/")
    page.click(Navbar.SIGN_IN_LNK)
    Login(page).login_with_credentials("automation@test.com", " ")
    assert page.locator(Login.ERROR_MESSAGE_DIV).inner_text() == error_message

    page.reload()
    Login(page).login_with_credentials("automation", "Test1234")
    assert page.locator(Login.ERROR_MESSAGE_DIV).inner_text() == error_message


@pytest.mark.login
def test_check_email_and_password_are_required(page: Page):
    """ Test that performs an invalid login """

    page.goto("/login/")
    page.click(Navbar.SIGN_IN_LNK)

    assert "required" in page.locator(Login.EMAIL_INPUT).evaluate("email => email.getAttributeNames()")
    assert "required" in page.locator(Login.PASSWORD_INPUT).evaluate("password => password.getAttributeNames()")
