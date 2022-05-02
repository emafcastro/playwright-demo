from playwright.sync_api import Page


class Articles:
    # Selectors
    TITLE_INPUT = "[name='title']"
    DESCRIPTION_INPUT = "[name='description']"
    BODY_INPUT = "textarea"
    TAGS_INPUT = "[placeholder='Enter tags']"
    PUBLISH_BTN = "text='Publish Article'"

    def __init__(self, page: Page):
        self.page = page

    async def create_article(self, title, description, body, tags):
        await self.page.fill(self.TITLE_INPUT, title)
        await self.page.fill(self.DESCRIPTION_INPUT, description)
        await self.page.fill(self.BODY_INPUT, body)
        await self.page.fill(self.TAGS_INPUT, tags)
        await self.page.click(self.PUBLISH_BTN)


class ArticleDetail:
    # Selectors
    TITLE_TXT = "h1"
    COMMENT_TXT = "textarea"
    POST_COMMENT_BTN = "text='Post Comment'"