Title: How to setup Django with Pytest on GitHub Actions
Description: A minimal example of how you can quickly get Django and Pytest running on every commit to GitHub
Slug: django-with-pytest-on-github-actions
Date: 2022-01-06 12:00
Category: Django

Someone recently asked me

> When is a good time to get automated testing setup on a new Django project?

The answer is "now". There are other good times, but now is best. In this post I'll briefly make my case for why, and show you an example of a minimal setup of Django running tests with [pytest](https://docs.pytest.org/en/6.2.x/index.html) with fully automated [continuous integration](https://www.atlassian.com/continuous-delivery/continuous-integration) (CI) using [GitHub Actions](https://github.com/features/actions).

As soon as you know a Django project is going to be "serious", then you should get it set up to run tests. So, potentially before you write any features. My approach is to get testing setup and to write a single dummy test and then get it running in CI. This means that as soon as you start writing features then you have everything you need to write a real test and have it run automatically on every commit.

The alternate scenario is you start adding features and get swept up in that process. At some point you'll think "hmm maybe I should write a test for this..." but if you don't have tests and CI set up already then you're more likely to say "nah, fuck it I'll do it later" and not write the test. Getting pytest to work with Django on GitHub actions is pretty easy these days. Bite the bullet, it tastes better than you may expect.

Or you could just not write any tests. This is fine for small personal projecs. Tests are a lot of things but they're not fun. For more serious endeavours though, not having tests will lead to riskier deployments, longer feedback loops on errors and less confidence in making big changes. Have you ever done a huge, wild refactor of a chunk of code, followed by a set of passing tests? It feels great man, that's when you're really living.

Let's go then: how do you set up Django + pytest + GitHub Actions? All the code discussed here can be found in this [example GitHub repository](https://github.com/MattSegal/django-pytest-github-actions).

## Installation

https://github.com/MattSegal/django-pytest-github-actions/blob/master/requirements.txt

```
django
pytest
pytest-django
```

https://docs.pytest.org/en/6.2.x/
https://pytest-django.readthedocs.io/en/latest/

## Config

https://github.com/MattSegal/django-pytest-github-actions/blob/master/app/pyproject.toml

```ini
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "demo.settings"
filterwarnings = [
    "ignore::UserWarning",
    "ignore::django.utils.deprecation.RemovedInDjango50Warning",
]
```

## Adding a dummy test

```python
def test_nothing():
    """A dummy test"""
    assert True
```

## Running the tests locally

```bash
pytest -vv
```

## Adding a basic view test

```python
def test_goodbye_view(client):
    """Test that goodbye view works"""
    url = reverse("goodbye")
    response = client.get(url)
    assert response.status_code == 200
    assert response.content == b"Goodbye world"
```

## Adding a view test with database interaction

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

https://github.com/MattSegal/django-pytest-github-actions/blob/master/.github/workflows/tests.yml

```yaml
name: Django Tests
on:
  push:
    branches:
      - master
  pull_request:
    branches:
      - master

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python 3.8
        uses: actions/setup-python@v2
        with:
          python-version: "3.8"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Test with pytest
        working-directory: ./app
        run: pytest -vv
```

## Conclusion

https://mattsegal.dev/alternate-test-styles.html
https://mattsegal.dev/pytest-on-github-actions.html
