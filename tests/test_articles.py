from pages.home_login import Navbar, Home
from pages.articles import Articles, ArticleDetail
import time
import pytest


@pytest.mark.asyncio
async def test_create_article(set_up_login):
    """ Test that creates an article and verifies if the title matches"""

    title = f"Test article {time.time()}"
    description = "This is another article"
    body = "# Hello world"
    tags = "test"

    page = set_up_login

    await page.click(Navbar.NEW_POST_LNK)
    article = Articles(page)
    await article.create_article(title, description, body, tags)

    await page.wait_for_selector(f"text='{title}'")
    assert await page.locator(f"text='{title}'").is_visible()


@pytest.mark.asyncio
async def test_like_an_article(set_up_login):
    page = set_up_login
    await page.wait_for_load_state()

    await page.locator(Home.FAVORITE_LIST).nth(0).click()

    await page.wait_for_load_state(state='networkidle')
    actual_likes_first_article = int(await page.locator(Home.FAVORITE_LIST).nth(0).inner_text())

    applied_classes = await page.locator("[name=favorite]").nth(0).get_attribute('class')
    is_button_active = "btn-primary" in applied_classes

    assert actual_likes_first_article == 1 if is_button_active else actual_likes_first_article == 0


@pytest.mark.asyncio
async def test_user_can_leave_a_comment(set_up):
    comment = "Amazing article "+str(time.time())

    page = set_up
    await page.wait_for_load_state()

    await page.locator(Home.TITLE_LIST).nth(0).click()
    await page.fill(ArticleDetail.COMMENT_TXT, comment)
    await page.click(ArticleDetail.POST_COMMENT_BTN)

    await page.wait_for_load_state('networkidle')

    assert await page.locator(f"text='{comment}'").is_visible()
