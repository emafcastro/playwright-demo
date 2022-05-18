from pages.home_login import Home


def test_like_an_article(set_up_login):
    page = set_up_login

    page.locator(Home.FAVORITE_LIST).nth(0).click()

    page.wait_for_load_state(state='networkidle')
    actual_likes_first_article = int(page.locator(Home.FAVORITE_LIST).nth(0).inner_text())

    applied_classes = page.locator("[name=favorite]").nth(0).get_attribute('class')
    is_button_active = "btn-primary" in applied_classes

    assert actual_likes_first_article == 1 if is_button_active else actual_likes_first_article == 0


def test_user_can_see_their_feed(set_up_login):
    pass


def test_length_of_articles_when_one_is_deleted(set_up_login):
    pass


def test_filter_by_tag(set_up_login):
    pass
