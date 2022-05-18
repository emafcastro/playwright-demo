from playwright.sync_api import Page


class Home:
    # Selectors
    ARTICLE_LIST = ".article-preview > a"
    FAVORITE_LIST = "[name=favorite]"
    FIRST_FAVORITE = ""

    def __init__(self, page: Page):
        self.page = page


class Navbar:
    # Selectors
    SIGN_IN_LNK = "text=Sign in"
    NEW_ARTICLE_LNK = "text=New Article"
    SETTINGS_LNK = "text=Settings"
    LOGOUT_LNK = "body > nav > div > ul > li:nth-child(4) > a"

    def __init__(self, page: Page):
        self.page = page


class Login:
    # Selectors
    EMAIL_INPUT = "#id_username"
    PASSWORD_INPUT = "#id_password"
    SIGN_IN_BTN = "button:has-text('Sign in')"
    ERROR_MESSAGE_DIV = ".error-messages"

    def __init__(self, page: Page):
        self.page = page

    def login_with_credentials(self, email, password):
        """ Manual login on the website """
        self.page.locator(self.EMAIL_INPUT).fill(email)
        self.page.focus(self.PASSWORD_INPUT)
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        self.page.locator(self.SIGN_IN_BTN).click()
