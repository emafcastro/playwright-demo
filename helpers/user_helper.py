import string
import random
import time
from playwright.sync_api import BrowserContext


def create_user(context: BrowserContext, email=None, name=None, password="Test1234") -> dict[str, str]:
    if email is None:
        email = f"automated{time.time()}@test.com"
    if name is None:
        name = f"automated{time.time()}"
    cookies = context.cookies()
    api_context = context.request

    headers = {'X-CSRFToken': cookies[0]["value"]}
    user = {"email": email, "name": name, "password": password}
    print(f"Creating user: {user['name']}")
    response = api_context.post("/register/", headers=headers, form=user)
    return response.headers


def login_user_via_api(context, email, password):
    csrftoken = maketoken(64)
    token = {"name": "csrftoken", "value": csrftoken, 'path': '/',
             'domain': 'localhost'}
    context.add_cookies([token])
    api_context = context.request

    user = {"username": email, "password": password, "csrfmiddlewaretoken": csrftoken}
    response = api_context.post("/login/", form=user)
    return response


def maketoken(length):
    characters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(characters) for i in range(length))
    return result_str
