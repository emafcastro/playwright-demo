from playwright.sync_api import Page


class Articles:
    # Selectors
    TITLE_INPUT = "#id_title"
    DESCRIPTION_INPUT = "#id_summary"
    BODY_INPUT = "#id_content"
    TAGS_INPUT = "[name=tags]"
    PUBLISH_BTN = "text='Publish Article'"

    def __init__(self, page: Page):
        self.page = page

    def create_article(self, title, description, body, tags):
        self.page.fill(self.TITLE_INPUT, title)
        self.page.fill(self.DESCRIPTION_INPUT, description)
        self.page.fill(self.BODY_INPUT, body)
        self.page.fill(self.TAGS_INPUT, tags)
        self.page.click(self.PUBLISH_BTN)


class ArticleDetail:
    # Selectors
    TITLE_TXT = ".container > h1"
    COMMENT_TXT = "textarea"
    POST_COMMENT_BTN = "text='Post Comment'"
    AUTHOR_LNK = ".author"
    DATE_TXT = ".date"
    ARTICLE_CONTENT_TXT = ".article-content"
    LIKE_ARTICLE_BUTTON = "text='Favorite Post'"
