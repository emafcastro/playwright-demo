from models.home_login import Navbar
from models.articles import Articles, ArticleDetail
from models.home_login import Home, Login
import time
from datetime import date
from helpers.article_helper import add_article, edit_article, delete_article
from helpers.user_helper import login_user_via_api
import pytest


@pytest.fixture()
def after_each_article(set_up_login):
    """ This fixture deletes the created article, to clean up the article list """
    page = set_up_login
    yield page

    context = page.context

    page.goto("/")
    url_first_article = page.locator(Home.ARTICLE_TITLES).first.get_attribute("href")
    id_article = url_first_article.split("/")[2]
    print(f"Removing article with id: {id_article}")
    delete_article(context, id_article)


def test_create_article(after_each_article):
    """ Test that creates an article and verifies if the title matches"""

    title = f"Test article {time.time()}"
    description = "This is another article"
    body = "# Hello world"
    tags = "test"

    page = after_each_article

    page.click(Navbar.NEW_ARTICLE_LNK)
    article = Articles(page)
    with page.expect_navigation(url="**/article/**/**/"):
        article.create_article(title, description, body, tags)

    assert page.locator(f"text='{title}'").is_visible()


def test_logged_out_user_visibility_on_article(after_each_article):
    """ This test allows an external user to see the content of an article """

    # Get all information from login
    page = after_each_article
    context = page.context

    article_url = add_article(context)

    # Delete all cookies
    context.clear_cookies()

    page.goto(f"{article_url}")
    assert page.locator(ArticleDetail.TITLE_TXT).is_visible()
    author_list = page.locator(ArticleDetail.AUTHOR_LNK)
    for index in range(0, author_list.count()):
        assert author_list.nth(index).inner_text() == "automation"

    # Verification that checks that date is today's date
    today_date = date.today().strftime("%B %d, %Y")
    date_list = page.locator(ArticleDetail.DATE_TXT)
    for index in range(0, date_list.count()):
        assert date_list.nth(index).inner_text() == today_date

    assert page.locator(ArticleDetail.ARTICLE_CONTENT_TXT).is_visible()

    assert page.locator(ArticleDetail.COMMENT_TXT).is_visible() is False


def test_edit_article(after_each_article):
    """ This test allows to edit an article and check if the changes are done """

    edited_article = {"title": "Edited title via Cypress", "summary": "Edited description", "content": "Edited body",
                      "tags": "test"}

    # Get all information from login
    page = after_each_article
    context = page.context

    # Create a new article
    add_article(context)

    page.goto("/")
    url_first_article = page.locator(Home.ARTICLE_TITLES).first.get_attribute("href")
    id_article = url_first_article.split("/")[2]

    url_edited_article = edit_article(context, id_article, edited_article)
    page.goto(f"{url_edited_article}")

    # Verifications

    assert page.locator(ArticleDetail.TITLE_TXT).inner_text() == edited_article["title"]
    author_list = page.locator(ArticleDetail.AUTHOR_LNK)
    for index in range(0, author_list.count()):
        assert author_list.nth(index).inner_text() == "automation"

    # Verification that checks that date is today's date
    today_date = date.today().strftime("%B %d, %Y")
    date_list = page.locator(ArticleDetail.DATE_TXT)
    for index in range(0, date_list.count()):
        assert date_list.nth(index).inner_text() == today_date

    assert edited_article["summary"] in page.locator(ArticleDetail.ARTICLE_CONTENT_TXT).inner_text()

    assert edited_article["content"] in page.locator(ArticleDetail.ARTICLE_CONTENT_TXT).inner_text()


def test_like_article_with_different_user(after_each_article):

    # Get all information from login
    page = after_each_article
    context = page.context
    article_url = add_article(context)

    # Delete all cookies
    context.clear_cookies()

    login_user_via_api(context, "like@test.com", "Test1234")
    page.goto(f"{article_url}")

    like_article = page.locator(ArticleDetail.LIKE_ARTICLE_BUTTON).first
    like_article.click()

    page.locator(".btn-outline-secondary").first.wait_for()

    assert "1" in like_article.inner_text()
