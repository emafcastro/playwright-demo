from models.home_login import Home, Navbar
from helpers.article_helper import add_article, delete_article
from models.home_login import Login


def test_like_an_article(set_up_login):
    page, context = set_up_login
    article_url = add_article(context)
    id_article = article_url.split("/")[2]
    context.clear_cookies()
    page.reload()

    page.locator(Navbar.SIGN_IN_LNK).nth(0).click()
    login = Login(page)
    login.login_with_credentials("like@test.com", "Test1234")
    page.wait_for_selector("text=Sign Out")

    with page.expect_response("**/article/favorite/**", timeout=6000):
        page.locator(Home.FAVORITE_LIST).nth(0).click()

    assert page.locator(f"#favorite-{id_article}").inner_text().strip() == "1"


def test_user_can_see_their_feed(set_up_login):
    page, _ = set_up_login

    page.locator(Home.MY_FEED_LNK).click()
    author_list = page.locator(Home.AUTHOR_LNK)
    for index in range(0, author_list.count()):
        assert "automation" in author_list.nth(index).text_content()


def test_length_of_articles_when_one_is_deleted(set_up_login):
    page, context = set_up_login

    article_url = add_article(context)
    path_split = article_url.split("/")[3]
    article_title = path_split.replace("-", " ")
    page.goto("http://localhost:8000")

    old_length = page.locator(Home.ARTICLE_TITLES).count()
    url_first_article = page.locator(Home.ARTICLE_TITLES).first.get_attribute("href")
    id_article = url_first_article.split("/")[2]
    delete_article(context, id_article)
    page.goto("http://localhost:8000")
    new_length = page.locator(Home.ARTICLE_TITLES).count()

    assert new_length < old_length

    assert page.locator(f"text='{article_title}'").is_visible() is False


def test_filter_by_tag(set_up_login):
    page, context = set_up_login
    add_article(context=context, tags="newTag")
    page.goto("http://localhost:8000")

    with page.expect_response("**/?tag=newTag"):
        page.locator(Home.SIDEBAR_SECTION).locator("text='newTag'").click()

    article_list = page.locator(Home.ARTICLE_LIST)
    for index in range(0, article_list.count()):
        assert "newTag" in article_list.nth(index).locator("li").all_text_contents()
