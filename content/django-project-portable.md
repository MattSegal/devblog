Title: How to make your Django project easy to move and share
Description: Some tips to help you ensure that your Django project can be shared between many people
Slug: django-portable-setup
Date: 2020-7-24 12:00
Category: Django

You need your Django project to be portable. It should be quick and easy to start it up on a new laptop. 
If it isn't portable, then your project is trapped on your machine. If it gets deleted or corrupted, then you've lost all your work!
This issue comes up in quite a few scenarios:

- you want to work on your code on multiple machines, like a laptop and a PC
- you want to get help from other people, and they want to try running your code
- you somehow screwed up your files very badly and you want to start from scratch 

In the worst case, moving your Django project from one machine to another is a frustrating and tedious experience that involves dead ends, mystery bugs and cryptic error messages. It's the kind of thing that makes you want to scream at your computer.

![frutsrated fox]({attach}/img/frustrated-fox.jpeg)

In the best case, this process can take minutes. To achieve this best case, there are some steps that you'll
need to take to make your development environment reproducable.

If you don't believe that this is achievable, then here's a quick example of me cloning and setting up an [example project](git@github.com:MattSegal/djdt-perf-demo.git) from scratch in under a minute:

<div class="loom-embed"><iframe src="https://www.loom.com/embed/01cbd6d2c2f04d0ab78e4d33d0174de5" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

In the rest of this post, I'll describe some practices that will help ensure that anyone with Python installed can quickly start working on your Django app.

## Hosting your code

The best way to make your code portable between multiple computers is to put it online in a place that is publicly accessible, like [GitHub](https://github.com/).
For example, this blog is [hosted on GitHub](https://github.com/MattSegal/devblog) so that I can access the latest copy of my writing from both my laptop and PC.
Git, the version control tool, is widely used by software developers and allows you to efficently and reliably sync your code between multiple machines.

If you don't know Git and you plan to work with software in any capacity, then I strongly recommend that you start learning how to use it as soon as possible.
There are plenty of [books](https://hellowebbooks.com/learn-git/), [online courses](https://www.udacity.com/course/version-control-with-git--ud123), [lectures](https://missing.csail.mit.edu/2020/version-control/) and [more](https://try.github.io/) to help you learn. It's a pain in the ass to start with, no doubt about that, but it is definitely worth your time.

## Tracking Python dependencies

Your project needs a bunch of 3rd party libraries to run. Obviously Django is required, plus maybe, Django Rest Framework, Boto3... Pillow, perhaps?
It's hard to remember all the thing that you've `pip install`'d, which is why it's really important to track all the libraries that your app needs, plus the versions, if those are important to you.

There is a Python convention of tracking all your libraries in a [requirements.txt](https://pip.pypa.io/en/latest/reference/pip_install/#example-requirements-file) file.
Experienced Python devs immediately know what to do if they see a project with one of these files, so it's good if you stick with this practice. Installing all
your requirements is as easy as:

```bash
pip install -r requirements.txt
```

You can also use `pip freeze` to get an exact snapshot of your current Python packages and write them to a file:

```bash
pip freeze > requirements.txt
```

Python's `pip` package manager tries to install all of your dependencies in your global system Python folder by default, which is a really dumb idea, 
and it can cause issues where multiple Python projects are all installing libraries in the same place. When this happens you can get the wrong
version installed, and you can no longer keep track of what dependencies you need to run your code, because they're are muddled
together with the ones from all your other projects.

The simplest way to fix this issue is to *always* use `virtualenv` to isolate your Python dependencies. You can read a guide on that [here](https://realpython.com/python-virtual-environments-a-primer/).  Using `virtualenv`, incidentally, also fixes the problem where you sometimes have to use `sudo` to pip install things on Linux.
There are also other tools like [pipenv](https://realpython.com/pipenv-guide/) or [poetry](https://python-poetry.org/) that solve this problem as well. Use whatever you want,
but it's a good idea to pick _something_, or you will shed many tears over Python dependency errors in the future.

## Repeatable setup instructions

Most simple Django projects have the exact same setup sequence. It's almost always roughly this:

```bash
# Create and activate virtual environment
virtualenv -p python3 env
. ./env/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create SQLite databse, run migrations
cd myapp
./manage.py migrate

# Run Django dev server
./manage.py runserver
```

But for anything but the simplest projects there's usually a few extra steps that you'll need to get up and running.
You need to **write this shit down**, preferably in your project's README, or **you will forget**.
Even if you remember all these steps, your friends or colleagues will get stuck if they're not available.

You want to document all the instructions that someone needs to do to start running your project, with as much of it being explicit
line of shell code as possible. Someone, who already has Python setup, should be able to clone your project onto their laptop with Git, follow
your instructions, and then be able to run your Django app. The kind of extra things that you should document are:

- any extra scripts or management commands that the user must run
- any environment variables or files that the user needs to configure
- setup of required data in the Django admin or shell 
- installing and running any 3rd party dependencies (eg. Docker, Postgres, Redis)
- building required front end web assets (eg. with Webpack)
- downloading essential data from the internet

Documenting the project setup isn't so important for small and simple projects, but it's also really easy to do (see script above). 
As your project becomes more complicated, the need to have replicable, explicit setup instructions becomes vital. 
If you do not maintain these instructions, then it will cost your hours of work when you forget to perform a vital step and your app doesn't work.

I've written before on [how to write a nice README](https://mattsegal.dev/github-resume-polish.html#readme), which you might find useful.
It's a little over the top for the purposes of just making your project portable and reproducible, but it should give you a general idea of what to cover.

## Exclude unnecessary files

Your project should only contain source code, plus the minimum files required to run it. It should not not contain:

- Editor config files (.idea, .vscode)
- Database files (eg. SQLite)
- Random documents (.pdf, .xls)
- Non-essential media files (images, videos, audio)
- Bytecode (eg. *.pyc files)
- Build artifacts (eg. JavaScript and CSS from Webpack)
- Virtual environments (eg env/venv folders)
- JavaScript packages (node_modules)
- Log files (eg. *.log)

Some of these files are just clutter, but the SQLite databases and bytecode are particularly important to exclude.

SQLite files are a binary format, which Git does not store easily. Every change to the database causes Git to store a whole new copy.
In addition, there's no way to "merge" databases with Git, meaning the data will get regularly overwritten by multiple users.

[Python bytecode](https://opensource.com/article/18/4/introduction-python-bytecode) files, with the `.pyc` extension, can cause issues
when shared between different machines, and are also just yucky to look at.

You can exlude all of the files (and folders) I described above using a `.gitignore` file, in the root of your repository, with contents something like this:

```text
# General
*.log
*.pdf
*.png

# IDE
.idea/ # PyCharm settings
.vscode/ # VSCode settings

# Python
*.pyc
env/
venv/

# Databases
*.sqlite3

# JavaScript
node_modules/
build/ # Webpack build output
```

If you've already added these kinds of files to your project's Git history, then you'll need to delete them before ignoring them.

In addition, a common mistake by beginners is to exclude migration files from theit Git history. Django migration files belong in source control,
so that you can ensure that everybody is running the same migrations on their data.

## Automate common tasks

Although it's not strictly necessary, it's really nice to automate your project setup, so that you can get started by just running a few scripts.
You can use bash scripts if you're a Linux or Mac user, PowerShell if you're using Windows, or even custom Django management commands. I also recommend checking out [Invoke](https://www.pyinvoke.org/), which is a nice, cross-platform Python tool for running tasks ([example Invoke script](https://github.com/MattSegal/link-sharing-site/blob/master/tasks.py)).

For example, in this [demo repo](https://github.com/MattSegal/djdt-perf-demo), I added a script which [fills the website with test data](https://mattsegal.dev/django-factoryboy-dummy-data.html), which a user can quickly run via a management command:

```bash
./manage.py setup_test_data
```

In other projects of mine, I also like to include a script that allows me to [pull production data into my local database](https://mattsegal.dev/restore-django-local-database.html), which is also just one quick copy-paste to run. 

```bash
./scripts/restore-prod.sh
```

## Next steps

If you're working on a Django project right now, I recommend that you make sure that it's portable. 
It doesn't take long to do and you will save yourself hours and hours of this:

![dog screaming internally]({attach}/img/screams.jpg)


If multiple people are working on your Django project and you want to become even more productive as a team, then I also recommend that you begin [writing tests](https://docs.djangoproject.com/en/3.0/topics/testing/) and [run them automatically with GitHub Actions](https://mattsegal.dev/pytest-on-github-actions.html).

If you've found moving your Django project around to be a frustrating experience, then you've probably also had trouble deploying it to the web as well. If that's the case, you might enjoy my guide on [Django deployment](https://mattsegal.dev/simple-django-deployment.html), where I show you how to deploy Django to a DigitalOcean virtual machine.