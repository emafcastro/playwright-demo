import time
from playwright.sync_api import BrowserContext


def add_article(page_context: BrowserContext, title=f"test article {time.time()}",
                summary="this is another article by Playwright",
                content="# hello world from Playwright", tags="test"):
    cookies = page_context.cookies()
    api_context = page_context.request  # Get api_context to execute api  methods

    article = {"title": title, "summary": summary,
               "content": content, "tags": tags,
               "csrfmiddlewaretoken": cookies[0]["value"]}

    # Execute POST method with article data
    create_article_response = api_context.post("/new/", form=article)
    if create_article_response.ok:
        return create_article_response.headers['hx-redirect']
    else:
        raise Exception(f"The add article method could not be executed correctly. Info: {create_article_response}")


def edit_article(page_context: BrowserContext, id_article, article):
    cookies = page_context.cookies()

    token = {"csrfmiddlewaretoken": cookies[0]["value"]}
    article.update(token)
    api_context = page_context.request  # Get api_context to execute api  methods

    # Execute POST method with article data
    edit_article_response = api_context.post(f"/article/edit/{id_article}/", form=article)
    if edit_article_response.ok:
        return edit_article_response.headers['hx-redirect']
    else:
        raise Exception(f"The edit article method could not be executed correctly. Info: {edit_article_response}")


def add_comment(page_context: BrowserContext, id_article):
    cookies = page_context.cookies()

    body = {"content": "comment created via API"}
    header = {"X-CSRFToken": cookies[0]["value"]}

    api_context = page_context.request
    api_context.post(f"/comments/add/{id_article}/", form=body, headers=header)
    return body["content"]


def delete_article(page_context: BrowserContext, id_article):
    cookies = page_context.cookies()
    header = {"X-CSRFToken": cookies[0]["value"]}

    api_context = page_context.request
    response = api_context.delete(f"/article/delete/{id_article}/", headers=header)
    return response
