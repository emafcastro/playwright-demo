from helpers.user_helper import create_user, login_user_via_api
from models.home_login import Navbar
from models.settings import Settings
import pytest
import time


@pytest.fixture()
def before_each_setting(generate_user_context):
    context = generate_user_context
    response = create_user(context)

    page = context.new_page()
    page.goto(f'{response["hx-redirect"]}')
    yield page


def test_change_profile_picture(before_each_setting):
    """ This test allows the user to change their profile """
    image_url = "https://www.goarabic.com/vm/wp-content/uploads/2019/05/dummy-profile-pic.jpg"

    page = before_each_setting
    page.locator(Navbar.SETTINGS_LNK).click()
    page.locator(Settings.IMAGE_INPUT).fill(image_url)
    page.locator(Settings.UPDATE_BUTTON).click()
    profile_image_url = page.locator("img").get_attribute("src")
    assert profile_image_url == image_url


def test_change_username(before_each_setting):
    """ This test allows the user to change their username """

    page = before_each_setting
    page.locator(Navbar.SETTINGS_LNK).click()
    page.locator(Settings.NAME_INPUT).fill("EditedName")
    with page.expect_navigation(url="**/profile/**/"):
        page.locator(Settings.UPDATE_BUTTON).click()
    assert page.locator("h4:has-text('EditedName')").is_visible()


def test_change_bio(before_each_setting):
    """ This test allows the user to change their bio """

    page = before_each_setting
    page.locator(Navbar.SETTINGS_LNK).click()
    page.locator(Settings.BIO_INPUT).fill("New Bio")
    with page.expect_navigation(url="**/profile/**/"):
        page.locator(Settings.UPDATE_BUTTON).click()
    assert page.locator("text=New Bio").is_visible()


def test_change_email(before_each_setting):
    """ This test allows the user to change their email """

    new_mail = f"edited{time.time()}@test.com"

    page = before_each_setting
    page.locator(Navbar.SETTINGS_LNK).click()
    page.locator(Settings.EMAIL_INPUT).fill(new_mail)
    with page.expect_navigation(url="**/profile/**/"):
        page.locator(Settings.UPDATE_BUTTON).click()

    page.context.clear_cookies()

    login_user_via_api(page.context, new_mail, "Test1234")
    page.goto("/")
    page.locator(Navbar.SETTINGS_LNK).click()
    assert page.locator(Settings.EMAIL_INPUT).get_attribute("value") == new_mail


def test_change_password(before_each_setting):
    """ This test allows the user to change their password """

    page = before_each_setting
    page.locator(Navbar.SETTINGS_LNK).click()

    email = page.locator(Settings.EMAIL_INPUT).get_attribute("value")
    page.locator(Settings.PASSWORD_INPUT).fill("Test5678")
    with page.expect_navigation(url="**/profile/**/"):
        page.locator(Settings.UPDATE_BUTTON).click()

    page.context.clear_cookies()

    login_user_via_api(page.context, email, "Test5678")
    page.goto("/")

    assert page.locator("text=Sign Out").is_visible()
