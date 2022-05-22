import pytest

from models.home_login import Login, Navbar

user = {"username": "automation", "email": "automation@test.com", "password": "Test1234"}


@pytest.mark.login
def test_login_with_valid_credentials(set_up_login):
    """ Test with valid credentials """

    page, _ = set_up_login
    assert page.locator("text=Sign Out").is_visible()


@pytest.mark.login
def test_login_with_empty_field(set_up):
    """ Test that performs an invalid login """

    page = set_up
    page.click(Navbar.SIGN_IN_LNK)
    login_page = Login(page)
    login_page.login_with_credentials(" ", "Test1234")
    assert page.locator(Login.ERROR_MESSAGE_DIV).inner_text() == "* This field is required."


@pytest.mark.login
def test_login_with_incorrect_email_and_password(set_up):
    """ Test that performs an invalid login by missmatch email and password """

    error_message = "* Please enter a correct Email Address and password. Note that both fields may be case-sensitive."

    page = set_up
    page.click(Navbar.SIGN_IN_LNK)
    login_page = Login(page)
    login_page.login_with_credentials("automation@test.com", " ")
    assert page.locator(Login.ERROR_MESSAGE_DIV).inner_text() == error_message

    login_page.login_with_credentials("automation", "Test1234")
    assert page.locator(Login.ERROR_MESSAGE_DIV).inner_text() == error_message


@pytest.mark.login
def test_check_email_and_password_are_required(set_up):
    """ Test that performs an invalid login """

    page = set_up
    page.click(Navbar.SIGN_IN_LNK)

    assert "required" in page.locator(Login.EMAIL_INPUT).evaluate("email => email.getAttributeNames()")
    assert "required" in page.locator(Login.PASSWORD_INPUT).evaluate("password => password.getAttributeNames()")
