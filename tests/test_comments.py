import time

from pages.articles import ArticleDetail
from pages.home_login import Home


def test_user_can_leave_a_comment(set_up_login):
    comment = "Amazing article " + str(time.time())

    page = set_up_login
    page.wait_for_load_state()

    page.locator(Home.ARTICLE_LIST).nth(0).click()
    page.wait_for_selector(ArticleDetail.COMMENT_TXT)
    page.fill(ArticleDetail.COMMENT_TXT, comment)
    page.click(ArticleDetail.POST_COMMENT_BTN)

    page.wait_for_load_state('networkidle')

    assert page.locator(f"text='{comment}'").is_visible()


def test_user_can_delete_a_comment(set_up_login):
    pass


def test_user_can_edit_a_comment(set_up_login):
    pass
