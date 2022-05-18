from pages.home_login import Navbar
from pages.articles import Articles, ArticleDetail
from pages.home_login import Home, Login
import time
from datetime import date


def test_create_article(set_up_login):
    """ Test that creates an article and verifies if the title matches"""

    title = f"Test article {time.time()}"
    description = "This is another article"
    body = "# Hello world"
    tags = "test"

    page, _ = set_up_login

    page.click(Navbar.NEW_ARTICLE_LNK)
    article = Articles(page)
    with page.expect_navigation(url="**/article/**/**/"):
        article.create_article(title, description, body, tags)

    assert page.locator(f"text='{title}'").is_visible()


def test_logged_out_user_visibility_on_article(set_up_login):
    # Get all information from login
    page, context = set_up_login
    article_url = add_article(context)

    # Delete all cookies
    context.clear_cookies()

    page.goto(f"http://localhost:8000{article_url}")
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


def add_article(context):
    cookies = context.cookies()
    api_context = context.request  # Get api_context to execute api  methods

    article = {"title": f"test article {time.time()}", "summary": "this is another article by Playwright",
               "content": "# hello world from Playwright", "tags": "test",
               "csrfmiddlewaretoken": cookies[0]["value"]}

    # Execute POST method with article data
    create_article = api_context.post("http://localhost:8000/new/", form=article)
    assert create_article.ok
    return create_article.headers['hx-redirect']


def test_edit_article(set_up_login):
    edited_article = {"title": "Edited title via Cypress", "summary": "Edited description", "content": "Edited body",
                      "tags": "test"}

    # Get all information from login
    page, context = set_up_login

    # Create a new article
    add_article(context)

    page.goto("http://localhost:8000")
    url_first_article = page.locator(Home.ARTICLE_LIST).first.get_attribute("href")
    id_article = url_first_article.split("/")[2]

    url_edited_article = edit_article(context, id_article, edited_article)
    page.goto(f"http://localhost:8000{url_edited_article}")

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


def edit_article(context, id_article, article):
    cookies = context.cookies()

    token = {"csrfmiddlewaretoken": cookies[0]["value"]}
    article.update(token)
    api_context = context.request  # Get api_context to execute api  methods

    # Execute POST method with article data
    create_article = api_context.post(f"http://localhost:8000/article/edit/{id_article}/", form=article)
    assert create_article.ok
    return create_article.headers['hx-redirect']


def test_like_article_with_different_user(set_up_login):
    # TODO: Investigate a better way to expect for the event that add and removes the class

    # Get all information from login
    page, context = set_up_login
    article_url = add_article(context)

    # Delete all cookies
    context.clear_cookies()
    page.goto("http://localhost:8000/login/")
    login_page = Login(page)
    login_page.login_with_credentials("like@test.com", "Test1234")
    page.wait_for_selector("text=Sign Out")
    page.goto(f"http://localhost:8000{article_url}")
    like_article = page.locator(ArticleDetail.LIKE_ARTICLE_BUTTON).first
    like_article.click()

    page.locator(".btn-outline-secondary").first.wait_for()

    assert "1" in like_article.inner_text()
