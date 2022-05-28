# playwright-demo

This is a demo run using Playwright framework with Python.

This demo is using The RealWorld application, specifically an implementation done in Django. If you want to test locally, you can clone the repository following the instructions in the next link:

https://github.com/danjac/realworld

I have deployed the project on the next link, you can use it to test on "production"

https://realworld-djangoapp.herokuapp.com


## How this demo works
After you clone this repository, execute

    python -m venv venv

    venv\Scripts\activate.ps1

    pip install -r requirements.txt

    pytest --base-url http://localhost:8000
