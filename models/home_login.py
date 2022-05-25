from playwright.sync_api import Page


class Home:
    # Selectors
    ARTICLE_LIST = ".article-preview"
    ARTICLE_TITLES = ".article-preview > a"
    FAVORITE_LIST = "[title='Add to Favorites']"
    MY_FEED_LNK = "text='Your Feed'"
    AUTHOR_LNK = ".author"
    SIDEBAR_SECTION = ".sidebar"


class Navbar:
    # Selectors
    SIGN_IN_LNK = "text=Sign in"
    NEW_ARTICLE_LNK = "text=New Article"
    SETTINGS_LNK = "//li/a[contains(text(), 'Settings')]"
    LOGOUT_LNK = "body > nav > div > ul > li:nth-child(4) > a"


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
