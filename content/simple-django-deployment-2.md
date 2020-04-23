Title: Simple Django Deployments part two: local setup
Description: How to make sure Django is working before you deploy it
Slug: simple-django-deployment-2
Date: 2020-04-19 14:00
Category: Django

# Prepare and test Django locally

We've got our server set up and ready to host our Django app, now let's focus on preparing our app for deployment.
For this guide I'm going to be creating an app from scratch.
I recommend you follow along as well, rather than trying to deploy an existing Django project.
Deploy your existing app after you've finished the guide.

In this section we'll cover:

- Setting up our Python environment
- Creating a basic Django app
- Preparing Django for production
- Serving static files in production
- Preparing our WSGI server
- Windows line endings

### Setting up our Python environment

I assume you've got Python 3 already installed on your computer. If you don't [install it now](https://realpython.com/installing-python/#windows).

Whenever you're doing Python development, you should use a "virtual environment" for your project
only want the package we need
keep track of what packages we need
helps us install packages when we deploy
minimise what we need to install
keeps other apps on the same server from overwriting our packages with different versions

- create project in ~/code/django-deploy
- pip freeze to show Python packages
- pip3 install virtualenv
- which virtualenv
- which pip3 / python3
- virtualenv --python python3 env
- ls env
- ls env/bin
- ./env/bin/python -V
- cat ./env/bin/activate
- . env/bin/activate
- note (env)
- which pip3 / python3
- which pip / python
- deactivate
- which pip3 / python3
- pip freeze
- . env/bin/activate
- pip freeze

- powershell side show
- get-command pip3
- get-command python3
- create virtualenv (using python3)
- show how to activate virtualenv in powershell
- get-command python3
- get-command pip3

- make sure virtualenv is active
- which pip
- create requirements.txt with django
- pip install -r requirements.txt
- pip show django
- pip freeze
- we can use freeze
- discuss pros / cons of django==3.0 vs just django
- check that it works with django-admin
- which django-admin

### Creating a basic Django app

covers some material in the Django tutorial but the point isn't to teach you Django basics
If you're not familliar with Django then try out https://docs.djangoproject.com/en/3.0/intro/tutorial01/

this will be like a half-assed version of the Django tutorial.
The purpose is not to show you how to write "good" Django, it's just to get something basic working so we can deploy it.

- create a Django app locally - link to github
- activate virtualenv in git bash
- start a project
- django-admin startproject tute
- look at created assets
- delete asgi
- cd tute
- ./manage.py migrate
- change settings DATABASES NAME to parent dir
- PARENT_DIR = os.path.dirname(BASE_DIR)
- delete database
- ./manage.py migrate
- check database outside of Django app
- run migrations
- view database that's been added (SQLite) (tool optional)
- open in SQLite viewer
- get it working with runserver - view default page

- create superuser, login to admin

- go into tute
- ./manage.py startapp counter
- look at created assets
- add view returning HttpResponse ''
- add to root urls
- test
- add HTML to counter/templates/counter/index.html
- add render + context
- test
- add styles.css to counter/static/counter/styles.css
- test

* add Counter model
* add app to INSTALLED APPS as 'counter.apps.CounterConfig'
* create migrations, show migrations
* run migrations - view changes to SQLite database

- visit count page
- view SQLite database

* add model to admin, view admin

* try django shell ./manage.py shell
* from counter.models import Counter
* Counter.objects.all()

Now we've created out app locally, let's get it ready for production
show diagram of how runserver works

DISCUSS SQLITE HERE

- discuss SQLite limitations?

https://www.sqlite.org/whentouse.html

> SQLite works great as the database engine for most low to medium traffic websites (which is to say, most websites). The amount of web traffic that SQLite can handle depends on how heavily the website uses its database. Generally speaking, any site that gets fewer than 100K hits/day should work fine with SQLite. The 100K hits/day figure is a conservative estimate, not a hard upper bound. SQLite has been demonstrated to work with 10 times that amount of traffic.

https://djangodeployment.com/2016/12/23/which-database-should-i-use-on-production/
concurrency

> Multiple processes can have the same database open at the same time. Multiple processes can be doing a SELECT at the same time. But only one process can be making changes to the database at any moment in time, however.

> SQLite uses reader/writer locks to control access to the database. (Under Win95/98/ME which lacks support for reader/writer locks, a probabilistic simulation is used instead.) But use caution: this locking mechanism might not work correctly if the database file is kept on an NFS filesystem. This is because fcntl() file locking is broken on many NFS implementations. You should avoid putting SQLite database files on NFS if multiple processes might try to access the file at the same time. On Windows, Microsoft's documentation says that locking may not work under FAT filesystems if you are not running the Share.exe daemon. People who have a lot of experience with Windows tell me that file locking of network files is very buggy and is not dependable. If what they say is true, sharing an SQLite database between two or more Windows machines might cause unexpected problems.

> We are aware of no other embedded SQL database engine that supports as much concurrency as SQLite. SQLite allows multiple processes to have the database file open at once, and for multiple processes to read the database at once. When any process wants to write, it must lock the entire database file for the duration of its update. But that normally only takes a few milliseconds. Other processes just wait on the writer to finish then continue about their business. Other embedded SQL database engines typically only allow a single process to connect to the database at once.

> However, client/server database engines (such as PostgreSQL, MySQL, or Oracle) usually support a higher level of concurrency and allow multiple processes to be writing to the same database at the same time. This is possible in a client/server database because there is always a single well-controlled server process available to coordinate access. If your application has a need for a lot of concurrency, then you should consider using a client/server database. But experience suggests that most applications need much less concurrency than their designers imagine.

> When SQLite tries to access a file that is locked by another process, the default behavior is to return SQLITE_BUSY. You can adjust this behavior from C code using the sqlite3_busy_handler() or sqlite3_busy_timeout() API functions.

### Preparing Django for production

- add prod-specific settings file
- add settings folder
- move settings.py to settings/base.py
- add an extra layer of dirname BASE_DIR
- add dev.py (import \* from base)
- add **init**.py
- import \* from dev to **init**
- set DEBUG = TRUE and secret key in dev (remove from base)

- https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
- try ./manage.py check --deploy

  - some issues with secret key, allowed hosts, debug
  - other ones ??? not so sure

- add prod.py (import \* from base)

  - DEBUG = False
  - ALLOWED_HOSTS = ['localhost', '64.225.23.131']
  - SECRET_KEY = os.environ['SECRET_KEY']

- we need to tell Django to use our new prod settings
- export DJANGO_SECRET_KEY="dqwdqwd22089ru230r0932ir0923iksd239f0u8fj2wq"
- try ./manage.py check --deploy AGAIN (some issues gone, some remain)

TRY DEV SETTINGS

- export DJANGO_SETTINGS_MODULE="tute.settings.dev"
- runserver (note "using settings dev")
- try 127.0.0.1:8000
- try localhost:8000
- show soft reload with runserver logs (click or f5)
- explain 200 status vs 404 status (favicon.ico)
- show hard reload (ctrl or shift click, ctrl or shift f5)

TRY PROD settings

- export DJANGO_SETTINGS_MODULE="tute.settings.prod"
- runserver FAIIIIIL
- export DJANGO_SECRET_KEY="dqwdqwd22089ru230r0932ir0923iksd239f0u8fj2wq"
- runserver (note "using settings prod")
- try 127.0.0.1:8000 -> FAIL 400 bad request (not in allowed hosts)

* add to allowed hosts and try again
* try localhost:8000
* where did my CSS go? --> we'll cover this later
* when DEBUG=False we need a new way to serve static files (CSS, JS, logos)

other than our static files mysteriously breaking, our server
seems to be working which is good

### Serving static files in production

so your static files are broken when DEBUG=True - what the fuck? right?
they were working before!?!?!

If you want to go outside and scream now's the time.

> AIIIIIIIIIIIIIIEEEEAAAAAAAAAAAAHHHH!!!!

Computers can be frustrating!

Django's docs on the subject are somewhere between cryptic and infuriating.
They're usually good docs too!
https://docs.djangoproject.com/en/3.0/howto/static-files/deployment/

Basically there are lots of different ways to serve static content,
so Django forces you to figure out how you're going to serve
static files in production.
Most of the choices are made around hosting costs,
other tech tools you're using
bandwitdh, performance - shit we don't care about right now.
We want the simplest solution for serving static files in production

You'll notice DJango already sets
STATIC_URL = '/static/'
This just means that when Django needs to figure out what {% static 'counter/style.css' %} means in our templates, it makes the URL

"http://mysite.com/static/counter/style.css"

It's really just telling Django what string to put in the HTML templates.
That's it.

STATIC_ROOT is the setting we're interested in.
STATIC_ROOT is the folder that Django copies all your static files into
when you run `./manage.py collectstatic`

You will need to run collectstatic when you deploy

Let's try it now just to see what it does

Set STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') in prod.py
run ./manage.py collectstatic
ls staticfiles
ls staticfiles/counter

So Django has copied all our files into a folder.
Seems kind of useless - it does make sense \$EXPLANATION

static files diagram?

So we need a program that knows to look into this folder and serve our staticfiles. We're going to use whitenoise. The short version is
that Whitenoise does what you'd expect should happen - it just serves

> Radically simplified static file serving for Python web apps... None of this is rocket science, but it’s fiddly and annoying and WhiteNoise takes care of all it for you.

Sounds good right?

See http://whitenoise.evans.io/en/stable/index.html#infrequently-asked-questions

This is probably the simplest way to serve static files in production
http://whitenoise.evans.io/en/stable/django.html

so let's follow the whitenoise guide!

- follow guide to setup whitenoise
- add whitenoise to requirements.txt
- explain middleware
- we'll be using a CDN later (so we don't need compression)
- use whitenoise.runserver_nostatic in installed apps
- test static files again with prod
- export DJANGO_SETTINGS_MODULE="tute.settings.dev"
- run runserver
- hard refreesh
- export DJANGO_SETTINGS_MODULE="tute.settings.prod"
- run runserver

- discuss limitations?

### Preparing our WSGI server

so far we've been using runserver
it works pretty well for development
the auto restart on file change is pretty handy
there's some trouble with runserver

The Django docs say it best
https://docs.djangoproject.com/en/2.2/ref/django-admin/#runserver

> NOT USE THIS SERVER IN A PRODUCTION SETTING. It has not gone through security audits or performance tests. (And that’s how it’s gonna stay. We’re in the business of making Web frameworks, not Web servers, so improving this server to be able to handle a production environment is outside the scope of Django.)

Why _exactly_ is it a bad idea? Honestly I don't know, I've never tried. _Something something security + performance something something_. When the people writing the software tell you not to use it production, it's best to just listen to them, unless you're confident you understand the risks.

So... what do we use to run our Django app? We're going to use [gunicorn](https://gunicorn.org/), basically because it's popular and I'm familliar with it. Another popular contenders is [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/).

TODO: What does it do? What is WSGI? Why do we need this?

- look at wsgi file
-
- install gunicorn
- add gunicorn to requirements.txt
- pip install -r requirements.txt
- which gunicorn
- gunicorn --help
- ensure we have our envars set
  export DJANGO_SECRET_KEY="dqwdqwd22089ru230r0932ir0923iksd239f0u8fj2wq"
  export DJANGO_SETTINGS_MODULE="tute.settings.prod"
- we need to run gunicorn and show it our wsgi file, since that's the entrypoint

* add bash script to run gunicorn (in scripts, chmod +x)
  - DJANGO_SETTINGS_MODULE
  - DJANGO_SECRET_KEY

- gunicorn tute.wsgi:application from inside tute
- it's running on port 8000 - works!
- localhost:80 no works
- check help again
- gunicorn --bind 0.0.0.0:3000 tute.wsgi:application
- localhost:8000
- localhost:3000
- getting port 80 to work is too much of a pain on windows
- this is enought for now

- we have tested our prod settings with runserver

wsgi server diagram? local and post deploy?

### Windows line endings

TODO

- warn about line endings
- show how to change line endings in VScode

[Deploy Django to the server]({filename}/simple-django-deployment-3.md)
