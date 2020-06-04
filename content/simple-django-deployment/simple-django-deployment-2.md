Title: Simple Django deployment part two: local setup
Description: How to make sure Django is working before you deploy it
Slug: simple-django-deployment-2
Date: 2020-04-26 14:00
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

<div class="yt-embed">
    <iframe 
        src="https://www.youtube.com/embed/8ja20EjR7zs" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen
    >
    </iframe>
</div>

### Creating a basic Django app

Now that we've got Django installed let's create our Django project. This guide covers some of the same ground as the [Django tutorial](https://docs.djangoproject.com/en/3.0/intro/tutorial01/), but we're going to skim through it, because the point isn't to teach you Django basics, it's to teach you how to deploy Django. If you're not familliar with Django then try out the tutorial first.

In addition some of my code (ie. the views) is going to be a little half-assed, since the purpose of the guide is not to show you how to write "good" Django views, it's just to get something basic working so we can deploy it.

I've put the [reference code for this guide onto GitHub](https://github.com/MattSegal/django-deploy), which you might want to look at while you're following along.

This video will show you how we're going to set up our Django project, and importantly, it will show you how to implement the key features that we want to test later, namely:

- A view which interacts with a database model
- Some static files (eg. CSS, JS)
- Our database setup
- The admin panel

<div class="yt-embed">
    <iframe 
        src="https://www.youtube.com/embed/fOvQfz8GZeM" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen
    >
    </iframe>
</div>

Now we've created our app and it's working locally. The next step is to get it ready for production. Here's a diagram of how we've been running our app and serving requests so far.

![runserver http]({attach}runserver-http.png)

<h3 id="sqlite">Is SQLite OK for production?</h3>

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

<div class="yt-embed">
    <iframe 
        src="https://www.youtube.com/embed/nL6yJOKTzO0" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen
    >
    </iframe>
</div>

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

<div class="yt-embed">
    <iframe 
        src="https://www.youtube.com/embed/97UQM-Cfhxs" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen
    >
    </iframe>
</div>

<h3 id="wsgi">Preparing our WSGI server</h3>

So far we've been using the "runserver" management command to run our Django code and serve HTTP requests.
It works pretty well for development - the way it auto restarts when files change is pretty handy.
There's some trouble with running runserver in production though -the Django docs [say it best](https://docs.djangoproject.com/en/2.2/ref/django-admin/#runserver):

> DO NOT USE THIS SERVER IN A PRODUCTION SETTING. It has not gone through security audits or performance tests. (And that’s how it’s gonna stay. We’re in the business of making Web frameworks, not Web servers, so improving this server to be able to handle a production environment is outside the scope of Django.)

Why _exactly_ is using runserver in prod a bad idea? Honestly I don't know, I've never tried. Something about security and performance... here's the thing: when the people writing the software tell you not to use it production (in all caps no less), it's best to just listen to them, unless you're confident that you understand the risks and benefits.

So... what do we use to run our Django app instead? We're going to use [Gunicorn](https://gunicorn.org/), basically because it's a popular WSGI server and I'm familliar with it and it seems OK. Another widely used contender is [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/). I've seen [Waitress](http://docs.pylonsproject.org/projects/waitress/en/stable/) recommended for running on Windows, but I've never tried it myself.

You might be wondering what "[WSGI](https://wsgi.readthedocs.io/en/latest/what.html)" ("Web Server Gateway Interface") means. WSGI is a type of "interface". I think it's much easier to explain with examples than to get too theoretical.

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

<div class="yt-embed">
    <iframe 
        src="https://www.youtube.com/embed/wHmpB2AEmZY" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen
    >
    </iframe>
</div>

So before we were doing this:

![runserver http]({attach}runserver-http.png)

Now we're doing this (hypothetically if Gunicorn actually worked on Windows):

![gunicorn http]({attach}gunicorn-http.png)

Nothing too crazy.

### Next steps

Now that we've done our local setup, we're ready to [deploy Django to the server]({filename}/simple-django-deployment/simple-django-deployment-3.md)
