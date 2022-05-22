import string
import random
from playwright.sync_api import BrowserContext
import time


def create_user(context: BrowserContext, email=f"automated{time.time()}@test.com", name=f"automated{time.time()}",
                password="Test1234"):
    cookies = context.cookies()
    api_context = context.request

    headers = {'X-CSRFToken': cookies[0]["value"]}
    user = {"email": email, "name": name, "password": password}
    response = api_context.post("http://localhost:8000/register/", headers=headers, form=user)
    return response


def login_user_via_api(context: BrowserContext, email, password):
    csrftoken = maketoken(64)
    token = {"name": "csrftoken", "value": csrftoken, 'path': '/',
             'domain': 'localhost'}
    context.add_cookies([token])
    api_context = context.request

    user = {"username": email, "password": password, "csrfmiddlewaretoken": csrftoken}
    response = api_context.post("http://localhost:8000/login/", form=user)
    return response

def maketoken(length):
    characters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(characters) for i in range(length))
    return result_str
