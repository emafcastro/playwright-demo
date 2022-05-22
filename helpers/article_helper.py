import time
from playwright.sync_api import BrowserContext


def add_article(context, title=f"test article {time.time()}", summary="this is another article by Playwright",
                content="# hello world from Playwright", tags="test"):
    cookies = context.cookies()
    print(f"cookies: {cookies}")
    api_context = context.request  # Get api_context to execute api  methods

    article = {"title": title, "summary": summary,
               "content": content, "tags": tags,
               "csrfmiddlewaretoken": cookies[0]["value"]}

    # Execute POST method with article data
    create_article = api_context.post("http://localhost:8000/new/", form=article)
    assert create_article.ok
    return create_article.headers['hx-redirect']


def edit_article(context, id_article, article):
    cookies = context.cookies()

    token = {"csrfmiddlewaretoken": cookies[0]["value"]}
    article.update(token)
    api_context = context.request  # Get api_context to execute api  methods

    # Execute POST method with article data
    create_article = api_context.post(f"http://localhost:8000/article/edit/{id_article}/", form=article)
    assert create_article.ok
    return create_article.headers['hx-redirect']


def add_comment(context, id_article):
    cookies = context.cookies()

    body = {"content": "comment created via API"}
    header = {"X-CSRFToken": cookies[0]["value"]}

    api_context = context.request
    api_context.post(f"http://localhost:8000/comments/add/{id_article}/", form=body, headers=header)
    return body["content"]


def delete_article(context, id_article):
    cookies = context.cookies()
    header = {"X-CSRFToken": cookies[0]["value"]}

    api_context = context.request
    response = api_context.delete(f"http://localhost:8000/article/delete/{id_article}/", headers=header)
    print(response)
