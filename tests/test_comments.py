import time

from models.articles import ArticleDetail, Comment
from helpers.article_helper import add_article, add_comment, delete_article
import pytest


@pytest.fixture()
def before_after_each_comment(set_up_login):
    # The user will be logged in, an article will be created and will redirect to that article
    # Before
    page = set_up_login
    context = page.context
    article_url = add_article(context)
    page.goto(f"{article_url}")

    yield page

    # After
    id_article = article_url.split("/")[2]
    print(f"Removing article with id: {id_article}")
    delete_article(context, id_article)


def test_user_can_leave_a_comment(before_after_each_comment):
    """ This test allows the user to leave a comment """
    comment = "Amazing article " + str(time.time())

    page = before_after_each_comment
    page.fill(ArticleDetail.COMMENT_TXT, comment)
    page.click(ArticleDetail.POST_COMMENT_BTN)

    page.wait_for_load_state('networkidle')

    assert page.locator(f"text='{comment}'").is_visible()


def test_user_can_delete_a_comment(before_after_each_comment):
    """ This test allows the user to delete a comment """

    page = before_after_each_comment
    context = page.context

    article_id = page.url.split("/")[4]
    comment = add_comment(context, article_id)
    page.reload()
    page.on("dialog", lambda dialog: dialog.accept())
    page.locator(Comment.DELETE_COMMENT_BTN).click()

    page.wait_for_load_state('networkidle')
    assert page.locator(f"text={comment}").is_visible() is False


def test_user_can_edit_a_comment(before_after_each_comment):
    """ This test allows the user to edit a comment """

    page = before_after_each_comment
    context = page.context

    article_id = page.url.split("/")[4]
    add_comment(context, article_id)
    page.reload()

    page.locator(Comment.EDIT_COMMENT_BTN).click()
    page.locator(Comment.COMMENT_LIST).nth(1).fill("Edited comment")
    page.locator(Comment.SAVE_COMMENT_BTN).click()
    page.wait_for_load_state('networkidle')

    assert page.locator("text='Edited comment'").is_visible()
