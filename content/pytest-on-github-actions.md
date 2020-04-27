Title: Run your Python unit tests via GitHub actions.
Description: How to run your Python unit tests via GitHub actions.
Slug: pytest-on-github-actions
Date: 2020-04-27 12:00
Category: Programming

You've written some unit tests for your Python app. Good for you! There are dozens of us, dozens!
You don't always remember to run your tests, or worse, your colleagues don't always remember to run them.

Wouldn't it be nice to run unit tests on every commit to GitHub? What about on every pull request?
You'd be able to hunt down commits that broke the build, and if you're feeling blamey, _who_ broke the build.
Sounds complicated, but it's not. Let me show you.

There is example code for this blog post [here](https://github.com/MattSegal/actions-python-tests).

### Setting up your project

I'm going to assume that:

- You have some Python code
- You use Git, and your code is already in a GitHub repository

If you're already running unit tests locally you can skip this section.
Otherwise, your Python project's folder looks something like this:

```text
.
├── env                     Python virtualenv
├── requirements.txt        Python requirements
├── README.md               Project description
└── stuff.py                Your code
```

If you don't have tests already, I recommend trying pytest (and adding it to your requirements.txt).

```bash
pip install pytest
```

You'll need at least one test

```python
# test_stuff.py
from stuff import run_stuff

def test_run_stuff():
    result = run_stuff()
    assert result == 1
```

You'll want to make sure your tests run and pass locally

```bash
pytest
```

### Set up your Action

You'll need to create new a file in a new folder: `.github/ci.yml`.
You can learn more about these config files [here](https://help.github.com/en/actions).
Here's an example file:

```yaml
name: Project Tests
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
      - name: Set up Python 3.6
        uses: actions/setup-python@v1
        with:
          python-version: 3.6
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Test with pytest
        run: pytest -vv
```

Now your project looks like this:

```text
.
├── .github                 GitHub hidden folder
|   └── workflows           Some other folder
|       └── ci.yml          GitHub Actions config
├── env                     Python virtualenv
├── requirements.txt        Python requirements
├── README.md               Project description
├── test_stuff.py           pytest unit tests
└── stuff.py                Your code
```

Commit your changes, push it up to GitHub and watch your tests run!

Sometimes they fail:

<div class="loom-embed"><iframe src="https://www.loom.com/embed/c46a3b978fa441b2a50abbe9d7d2a1ef" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

Sometimes they pass:

<div class="loom-embed"><iframe src="https://www.loom.com/embed/f06b6150b74445159e665f0b3ba92c2a" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

### Add a badge to your README

You can add a "badge" to your project's README.md.
Assuming your project was hosted at https://github.com/MyName/my-project/, you can add this
to your README.md file:

```text
![](https://github.com/MyName/my-project/workflows/Project%20Tests/badge.svg)
```

### Next steps

Write some tests, run them locally, and then let GitHub run them for you on every commit from now on.
