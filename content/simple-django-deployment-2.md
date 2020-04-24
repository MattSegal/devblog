Title: Simple django deployment part two: local setup
Description: How to make sure Django is working before you deploy it
Slug: simple-django-deployment-2
Date: 2020-04-19 14:00
Category: Django

We've got our server set up and ready to host our Django app, now let's focus on preparing our app for deployment.
The goal of this section is to set up and test as much of the stuff that we'll be using in production.
That way, we can debug issues on our computer, instead of on the server.

For this guide I'm going to be creating a Django app from scratch.
I recommend you follow along and set up your project like I do, rather than trying to deploy an existing Django project.
You can try deploy your existing app after you've finished the guide. Remember: new skills on easy terrain.

In this section we'll cover:

- Setting up our Python environment
- Creating a basic Django app
- SQLite limitations
- Preparing Django for production
- Serving static files in production
- Preparing our WSGI server
- Windows line endings

### Setting up our Python environment

I assume you've got Python 3 already installed on your computer. If you don't [install it now](https://realpython.com/installing-python/#windows).

We're going to be installing some Python packages for our app and we also will want to install the same packages on our server.
To keep things consistent, we're going to use a "virtual environment" (virtualenv) for this project.
In general it's good practice to always use a virtualenv, for these reasons:

- It helps maintain consistency between our local project and the deployed project
- It helps you keep track of what packages you need to run the project
- It helps minimise the number of packages that we need to install when we deploy
- It keeps other apps on the same computer from overwriting our packages with different versions

Here's how to start our project with a virtualenv.

VIRTUALENV VIDEO:

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

Now that we've got Django installed let's create our Django project. This guide covers some of the same ground as the [Django tutorial](https://docs.djangoproject.com/en/3.0/intro/tutorial01/), but we're going to skim through it, because the point isn't to teach you Django basics, it's to teach you how to deploy Django. If you're not familliar with Django then try out the tutorial first.

In addition some of my code (ie. the views) is going to be a little half-assed, since the purpose of the guide is not to show you how to write "good" Django views, it's just to get something basic working so we can deploy it.

I've put the [reference code for this guide onto GitHub](https://github.com/MattSegal/django-deploy), which you might want to look at while you're following along.

DJANGO APP VIDEO

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
- add Counter model
- add app to INSTALLED APPS as 'counter.apps.CounterConfig'
- create migrations, show migrations
- run migrations - view changes to SQLite database
- visit count page
- view SQLite database
- add model to admin, view admin
- try django shell ./manage.py shell
- from counter.models import Counter
- Counter.objects.all()

Now we've created our app and it's working locally. The next step is to get it ready for production. Here's a diagram of how we've been running our app and serving requests so far.

![runserver http]({attach}runserver-http.png)

### Is SQLite OK for production?

Before we move on, I want to talk about SQLite quickly. You can skip this bit if you don't care. We'll be using SQLite as our database in development and in production. It'll be two separate databases - we're not going to copy our local SQLite file to the server. The main reason that I'm using SQLite instead of a more advanced database like PostgreSQL or MySQL is because I want to keep this guide as simple as I can.

Is it bad practice to use SQLite in production? Are we taking some shitty shortcut that will bite us in the ass later? Mostly no. Here's what the creators of SQLite [have to say](https://www.sqlite.org/whentouse.html) about running it for webservers:

> SQLite works great as the database engine for most low to medium traffic websites (which is to say, most websites).

For our needs, the performance of SQLite is totally fine. There are some limitations to SQLite that are worth mentioning though ([discussed here](https://djangodeployment.com/2016/12/23/which-database-should-i-use-on-production)). One concern is that only one change to the database can [happen at a time](https://www.sqlite.org/faq.html#q5). Multiple concurrent reads, but only one write:

> Multiple processes can have the same database open at the same time. Multiple processes can be doing a SELECT at the same time. But only one process can be making changes to the database at any moment in time, however.

Most website traffic is reads, not writes, so it's not as bad as it sounds.
Still, what happens in Django when two users try to write to an SQLite database at the same time? I think this will happen:

- One user will get a lock on the database, and will write their changes, while the other user will be forced to wait
- If the first user finishes quickly enough, then the second user will get their turn - no problem here
- If the first user takes too long, then the second user gets an error "OperationalError: 'database is locked'"

You can [increase the wait time if you need to](https://docs.djangoproject.com/en/3.0/ref/databases/#database-is-locked-errors). I really don't think this is a big issue for low-volume learning projects, or small basic websites with medium traffic.

The other issue worth mentioning is switching from SQLite to another database like PostgreSQL. This probably will be annoying to do, where you need to dump your data to disk as a JSON or something then reload it into Postgres. If this seems like a huge issue for you, then I suggest you follow this guide, then learn how to switch SQLite for Postgres before you fill your database with valuable data. Take small steps.

One thing worth noting is that SQLite is _really easy_ to back up. You just make a copy of the file - done!

### Preparing Django for production

We need to make some changes to our Django settings to prepare our project for production, mostly for security reasons. The big 3 are:

- **DEBUG**: needs to be set to False to prevent Django from leaking information like error messages
- **SECRET_KEY**: needs to be set to something that's actually secret: you can't put it on GitHub
- **ALLOWED_HOSTS**: needs to be set to a whitelist of the IP addresses / domain names that your app can use, to prevent cross site request forgery attacks... or something like that

SETTING UP SETTINGS VIDEO:

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

  - note that DJANGO_SECRET_KEY is a SECRET

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

- add to allowed hosts and try again
- try localhost:8000
- where did my CSS go? --> we'll cover this later
- when DEBUG=False we need a new way to serve static files (CSS, JS, logos)

Our server seems to be _mostly_ working with our new production settings...
other than our static files mysteriously breaking. Let's fix that next.

### Serving static files in production

So your static files (CSS, JS, images, etc) work fine when DEBUG=True, but they're broken when DEBUG=False.
This doesn't seem like a "debug" thing... what the fuck? Right?
They were working before!?!? Whose ideas was this?

Aren't you glad you found out about this problem _before_ you tried to deploy your app?

Many Django developers have been slapped in the face by this surprise.
If you want to go outside and scream now's a good time.

> AIIIIIIIIIIIIIIEEEEAAAAAAAAAAAAHHHH!!!!

Computers can be frustrating! I like Django and the people who built it.
That said, this is one of the few times where I feel like the framework lets you down.
Django's docs on the [subject of deploying static files](https://docs.djangoproject.com/en/3.0/howto/static-files/deployment/) are somewhere between cryptic and infuriating.
They're usually good docs too!

The reason that the static files break when DEBUG=False is that there are lots of different ways to serve static content.
When you are in DEBUG=True mode, Django helpfully serves your static files for you.
When you set DEBUG=False, you're on your own - Django forces you to figure out how you're going to serve static files in production.

There are several options available: most of the choices that are made around hosting costs, the other tech tools you're using
bandwidth, performance - shit we don't care about right now.
We want the simplest solution for serving static files in production.

As far as I know [Whitenoise](http://whitenoise.evans.io/en/stable/) is the simplest way to serve static files in production:

> Radically simplified static file serving for Python web apps... None of this is rocket science, but it’s fiddly and annoying and WhiteNoise takes care of all it for you.

Sounds good right? It basically just does what runserver was doing before we set DEBUG=False, except maybe a bit better, or something. Their [documentation](http://whitenoise.evans.io/en/stable/index.html) and [FAQ](http://whitenoise.evans.io/en/stable/index.html#infrequently-asked-questions) goes over what it does for you. We're going to use the CloudFlare CDN in a later part of this guide to cache our static files, so that will solve most of our performance concerns.

Let's follow their [guide](http://whitenoise.evans.io/en/stable/django.html) and set up Django to use Whitenoise for static files. Before we get to the video let's go over the important bits.

First we have to install it

```bash
pip install whitenoise
```

We also have to set STATIC_ROOT in our Django settings. STATIC_ROOT is a folder where Django will dump all of your static files when you run the "collectstatic" management command. Whitenoise looks inside this folder when DEBUG=False, so it's important we set it, and run "collectstatic" when we deploy. We'll go over this more in the video.

Alright, let's set up Whitenoise and solve our static files problem.

- follow guide to setup whitenoise
- add whitenoise to requirements.txt
- pip install -r requirements.txt
- add middleware
- explain middleware
- we'll be using a CDN later (so we don't need compression)
- use whitenoise.runserver_nostatic in installed apps
- test static files again with prod
- export DJANGO_SETTINGS_MODULE="tute.settings.dev"
- run runserver
- hard refreesh
- export DJANGO_SETTINGS_MODULE="tute.settings.prod"
- run runserver
- should fail
- why fail?
- set static root
- STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
- run collectstatic
- inspect file
- ls staticfiles
- ls staticfiles/counter
- explain why staticfiles - unified interface?
- check

### Preparing our WSGI server

So far we've been using the "runserver" management command to run our Django code and serve HTTP requests.
It works pretty well for development - the way it auto restarts when files change is pretty handy.
There's some trouble with running runserver in production though -the Django docs [say it best](https://docs.djangoproject.com/en/2.2/ref/django-admin/#runserver):

> DO NOT USE THIS SERVER IN A PRODUCTION SETTING. It has not gone through security audits or performance tests. (And that’s how it’s gonna stay. We’re in the business of making Web frameworks, not Web servers, so improving this server to be able to handle a production environment is outside the scope of Django.)

Why _exactly_ is using runserver in prod a bad idea? Honestly I don't know, I've never tried. Something about security and performance... here's the thing: when the people writing the software tell you not to use it production (in all caps no less), it's best to just listen to them, unless you're confident that you understand the risks and benefits.

So... what do we use to run our Django app instead? We're going to use [Gunicorn](https://gunicorn.org/), basically because it's a popular WSGI server and I'm familliar with it and it seems OK. Another widely used contender is [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/).

You might be wondering what "[WSGI](https://wsgi.readthedocs.io/en/latest/what.html)" ("Web Server Gateway Interface") means. WSGI is a type of "interface". I think it's much easier to explain with examples than get too theoretical.

Here are some WSGI compatible web frameworks:

- Django
- Flask
- Pyramid
- web2py

Here are some WSGI compatible web servers:

- Gunicorn
- uWSGI
- CherryPy
- Apache's mod_wsgi module

Web frameworks (eg. Django) are just some Python code, you need a web server to actually run the code and translate incoming HTTP requests (which are just text) into Python objects. The WSGI specification makes it so that any WSGI compatible webserver can run any WSGI compatible web framework, which means:

- Gunicorn can run Django
- Gunicorn can run Flask
- CherryPy can run web2py
- mod_wsgi can run Django
- ... etc etc etc ...

This is a good thing because it means that if you are using a particular web framework (eg. Django), you have a lot of choices for which web server you run (eg. Gunicorn). It's also good for web server developers, because lots of people with different web frameworks can use their tools.

With that out of the way, let's get stuck into using Gunicorn instead of runserver to run our Django app.

VIDEO

- look at wsgi file, discuss purpose
- install gunicorn
- add gunicorn to requirements.txt
- pip install -r requirements.txt
- which gunicorn
- gunicorn --help
- ensure we have our envars set
  export DJANGO_SECRET_KEY="dqwdqwd22089ru230r0932ir0923iksd239f0u8fj2wq"
  export DJANGO_SETTINGS_MODULE="tute.settings.prod"
- we need to run gunicorn and show it our wsgi file, since that's the entrypoint
- gunicorn tute.wsgi:application from inside tute
- it's running on port 8000 - works!
- refresh static assets, check logs
- localhost:80 no works
- check help again
- gunicorn --bind 0.0.0.0:3000 tute.wsgi:application
- localhost:8000
- localhost:3000
- getting port 80 to work is too much of a pain on Windows
- we have tested our prod settings with runserver

So before we were doing this:

![runserver http]({attach}runserver-http.png)

Now we're doing this:

![gunicorn http]({attach}gunicorn-http.png)

Nothing too crazy.

### Next steps

Now that we've done our local setup, we're ready to [deploy Django to the server]({filename}/simple-django-deployment-3.md)
