from playwright.sync_api import Page


class Home:
    # Selectors
    TITLE_LIST = "a > h1"
    FAVORITE_LIST = "[name=favorite]"
    FIRST_FAVORITE = ""

    def __init__(self, page: Page):
        self.page = page


class Navbar:
    # Selectors
    SIGN_IN_LNK = "text=Sign in"
    PROFILE_LNK = "li >> nth=3 >> a"
    NEW_POST_LNK = "text=New Post"

    def __init__(self, page: Page):
        self.page = page


class Login:
    # Selectors
    EMAIL_INPUT = "[placeholder='Email']"
    PASSWORD_INPUT = "[type=password]"
    SIGN_IN_BTN = "button:has-text('Sign in')"

    def __init__(self, page: Page):
        self.page = page

    async def login_with_credentials(self, email, password):
        await self.page.fill(self.EMAIL_INPUT, email)
        await self.page.fill(self.PASSWORD_INPUT, password)
        await self.page.click(self.SIGN_IN_BTN)
