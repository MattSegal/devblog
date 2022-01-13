Title: How to setup Django with Pytest on GitHub Actions
Description: A minimal example of how you can quickly get Django and Pytest running on every commit to GitHub
Slug: django-with-pytest-on-github-actions
Date: 2022-01-13 12:00
Category: Django

Someone recently asked me

> When is a good time to get automated testing setup on a new Django project?

The answer is "now". There are other good times, but now is best. In this post I'll briefly make my case for why, and show you an example of a minimal setup of Django running tests with [pytest](https://docs.pytest.org/en/6.2.x/index.html) with fully automated [continuous integration](https://www.atlassian.com/continuous-delivery/continuous-integration) (CI) using [GitHub Actions](https://github.com/features/actions).

As soon as you know a Django project is going to be "serious", then you should get it set up to run tests. So, potentially before you write any features. My approach is to get testing setup and to write a dummy test or two and then get it running in CI. This means that as soon as you start writing features then you will have everything you need to write a real test and have it run automatically on every commit.

The alternate scenario is you start adding features and get swept up in that process. At some point you'll think "hmm maybe I should write a test for this...", but if you don't have tests and CI set up already then you're more likely to say "nah, fuck it I'll do it later" and not write the test. Getting pytest to work with Django on GitHub actions is pretty easy these days. Bite the bullet, it tastes better than you may expect.

Or you could just not write any tests. This is fine for small personal projecs. Tests are a lot of things but they're not fun. For more serious endeavours though, not having tests will lead to riskier deployments, longer feedback loops on errors and less confidence in making big changes. Have you ever done a huge, wild refactor of a chunk of code, followed by a set of passing tests? It feels great man, that's when you're really living.

The other question is: when should I run my tests? Sometimes you forget or you can't be bothered. This is where GitHub Actions (or any other CI) is very useful. You can set this service up to automatically run your tests _every time_ you push a commit up to GitHub.

Let's go then: how do you set up Django + pytest + GitHub Actions? All the code discussed here can be found in this [example GitHub repository](https://github.com/MattSegal/django-pytest-github-actions).

## Installation

Alongside Django you will need to install [`pytest`](https://docs.pytest.org/en/6.2.x/) and [`pytest-django`](https://pytest-django.readthedocs.io/en/latest/). These libraries are not required to run tests with Django: the [official docs](https://docs.djangoproject.com/en/4.0/topics/testing/overview/) show you how to use Python's unittest library instead. I like pytest better though, and I think you will too. My [requirements.txt](https://github.com/MattSegal/django-pytest-github-actions/blob/master/requirements.txt) file looks like this:

```
django
pytest
pytest-django
```

I don't pin my dependencies because I'm lazy: what can I say? I recommend you setup a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/) and then install as follows:

```bash
pip install -r requirements.txt
```

## Configuraton

You can configure pytest with a standard [pyproject.toml](https://snarky.ca/what-the-heck-is-pyproject-toml/) file. [Here's mine](https://github.com/MattSegal/django-pytest-github-actions/blob/master/app/pyproject.toml). The most important thing is to set [`DJANGO_SETTINGS_MODULE`](https://docs.djangoproject.com/en/4.0/topics/settings/#envvar-DJANGO_SETTINGS_MODULE) so pytest knows which settings to use. It's good to have a separate set of test settings for your project so that you can avoid, for example, accidently changing your production environment with credentials stored in settings when you run a test.

```ini
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "demo.settings"
filterwarnings = [
    "ignore::UserWarning",
]
```

This file should live in whichever folder you will be running `pytest` from. For the reference project, that means in the `./app` folder alongside `manage.py`.

## Adding a dummy test

That's a good start. Now we can test the setup so far with a dummy test. This test does nothing: it always passes, but it verifies that all the plumbing is working. In pytest, tests are just functions that use assert statements to check things:

```python
def test_nothing():
    """A dummy test"""
    assert True
```

Pytest looks for a `tests` folder in your Django apps. For example, here is the [tests folder](https://github.com/MattSegal/django-pytest-github-actions/tree/master/app/web/tests) in the reference project. So this dummy test function could live in a file named `app/web/tests/test_dummy.py`. You can add as many tests to a file as you like, or have as many test files as you like. Avoid duplicate names though!

## Running the tests locally

At this stage it's good to check that the dummy test works by running pytest from the command line:

```bash
pytest -vv
```

Read `-vv` as "very verbose". Here are [specific instructions](https://github.com/MattSegal/django-pytest-github-actions#running-tests) for anyone trying out the reference project. Hopefully that worked. You may see a folder called `.pytest_cache` appear in your project. I recommend you [gitignore](https://www.atlassian.com/git/tutorials/saving-changes/gitignore) this.

Now let's add some more meaningful example tests before we move on to setting up GitHub Actions.

## Adding a basic view test

My reference project has a very basic view named "goodbye" which just returns the text "Goodbye world". Here it is:

```python
def goodbye_view(request):
    return HttpResponse(f"Goodbye world")
```

You can test that this view returns the expected response using the [Django test client](https://docs.djangoproject.com/en/4.0/topics/testing/tools/#the-test-client). Pytest has a handy feature called [fixtures](https://docs.pytest.org/en/6.2.x/fixture.html), which is a little piece of magic where you ask for an speficic object via the test function arguments and pytest automagically provides it. In this case we add "client" to the function arguments to get a test client. It's a little out of scope for this post, but you can write your own fixtures too!

```python
def test_goodbye_view(client):
    """Test that goodbye view works"""
    # Build the URL from the url's name
    url = reverse("goodbye")
    # Make a GET request to the view using the test client
    response = client.get(url)
    # Verify that the response is correct
    assert response.status_code == 200
    assert response.content == b"Goodbye world"
```

Very nice, but you will find that you need to do a little more work to test views that include database queries.

## Adding a view test with database interaction

With pytest-django you need to _explicitly_ request access to the database using the [pytest.mark.django_db](https://pytest-django.readthedocs.io/en/latest/helpers.html#pytest-mark-django-db-request-database-access) decorator. Below is an example of a test that hits the database. In this example there is a page view counter that increments +1 every time someone views the page:

```python
def hello_view(request):
    counter, _ = PageViewCount.objects.get_or_create(title="hello")
    counter.count += 1
    counter.save()
    return HttpResponse(f"Hello world. The counter is: {counter.count}")
```

So if you load the page over and over again it should say:

```text
Hello world. The counter is: 1
Hello world. The counter is: 2
Hello world. The counter is: 3
Hello world. The counter is: 4
... etc
```

Here is a test for this view:

```python
import pytest
from django.urls import reverse

from web.models import PageViewCount


@pytest.mark.django_db
def test_hello_view(client):
    url = reverse("hello")
    assert PageViewCount.objects.count() == 0

    response = client.get(url)
    assert response.status_code == 200
    assert PageViewCount.objects.count() == 1
    counter = PageViewCount.objects.last()
    assert counter.count == 1
    assert b"Hello world" in response.content
    assert b"The counter is: 1" in response.content

    response = client.get(url)
    assert response.status_code == 200
    counter.refresh_from_db()
    assert counter.count == 2
    assert b"The counter is: 2" in response.content
```

## Setting up GitHub Actions

Ok so all our tests are running locally, how do we get them to run automatically in GitHub Actions? You can configure an action by adding a config file to your GitHub project at the location `.github/workflows/whatever.yml`. I named mine [tests.yml](https://github.com/MattSegal/django-pytest-github-actions/blob/master/.github/workflows/tests.yml).

Let's walk through the contents of this file (docs [here](https://docs.github.com/en/actions)):

```yaml
# The name of the action
name: Django Tests
# When the action is triggered
on:
  push:
    branches:
      - master
  pull_request:
    branches:
      - master

# What to do when the action is triggered
jobs:
  # A job called 'build' - arbitrary
  build:
    # Run on a Ubuntu VM
    runs-on: ubuntu-latest
    steps:
      # Checkout the GitHub repo
      - uses: actions/checkout@v2

      # Install Python 3.8
      - name: Set up Python 3.8
        uses: actions/setup-python@v2
        with:
          python-version: "3.8"

      # Pip install project dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # Move into the Django project folder (./app) and run pytest
      - name: Test with pytest
        working-directory: ./app
        run: pytest -vv
```

That's it, now pytest will run on every commit to master, and every pull request to master. You can see the actions for the reference project [here](https://github.com/MattSegal/django-pytest-github-actions/actions). Every test run will put a little tick or cross in your GitHub commit history.

![test ticks]({attach}/img/django-test-tick.png)

You can also embed a nice little badge in your README:

[![Django Tests](https://github.com/MattSegal/django-pytest-github-actions/actions/workflows/tests.yml/badge.svg)](https://github.com/MattSegal/django-pytest-github-actions/actions/workflows/tests.yml)

## Conclusion

I hope this post helps you get started with writing and running automated tests for your Django project. They're a real lifesaver. If you liked this post about testing, you might also like this post about different testing styles ([There's no one right way to test your code](https://mattsegal.dev/alternate-test-styles.html)) and this post about setting up pytest on GitHub actions, without Django ([Run your Python unit tests via GitHub actions](https://mattsegal.dev/pytest-on-github-actions.html)).
