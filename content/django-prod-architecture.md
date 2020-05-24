Title: A tour of Django server setups
Description: A review of many different ways to deploy Django
Slug: django-prod-architectures
Date: 2020-05-20 12:00
Category: Django

If you haven't worked as a web developer yet, you might be wondering:
_how do professionals deploy Django to the internet? What does it look like when it's running in production?_
You might even be thinking _what the hell is [production](https://www.techopedia.com/definition/8989/production-environment)?_

Before I started working a developer there was just a fuzzy cloud in my head where the knowledge of production infrastructure should be.
There are a bunch of natural questions like _how many servers do people use?_, _where does the database go?_ and _why does everyone tell me to use NGINX_?
If there's a fuzzy cloud in your head, let's fix it. This post will take you on a tour of some common Django server setups,
from the most simple and basic to the more complex.

In this post I'll cover your local machine, some single webserver setups and then
get into external services, multiple services, autoscaling and containers.

I'm not going to spend a lot of time talking about services like [Heroku](https://www.heroku.com/)
or [pythonanywhere](https://www.pythonanywhere.com/) or do-it-yourself platforms like [Dokku](http://dokku.viewdocs.io/dokku/).
The focus of this post will be on building up your mental model of how Django is hosted in production,
rather than the details on any particular service.

### Your local machine

Let's start with the simplest infrastructure - your local machine.
This will be a useful reference for later sections.
When you run Django locally, you have:

- Your web browser (Chrome, Safari, Firefox, etc)
- Django running with the runserver management command
- A SQLite database sitting in your project folder

![local server setup]({attach}django-prod-architecture/local-server.png)

Pretty simple right? Next let's look at the closest analogue in production.

### Simplest possible webserver

The simplest Django web server you can setup is very similar to your local dev environment. Now your setup looks like this:

![simple server setup]({attach}django-prod-architecture/simple-server.png)

Typically people run Django on a Linux virtual machine, often using the Ubuntu distribution.
The virtual machine is hosted by a cloud provider like [Amazon](https://aws.amazon.com/), [Google](https://cloud.google.com/gcp/), [Azure](https://azure.microsoft.com/en-au/), [DigitalOcean](https://www.digitalocean.com/) or [Linode](https://www.linode.com/).

Instead of using runserver, you would use a WSGI server like [Gunicorn](https://gunicorn.org/) to run your Django app.
I go into more detail on why you shouldn't use runserver in production, and explain WSGI [here](https://mattsegal.dev/simple-django-deployment-2.html#wsgi).
Gunicorn is not the only possible WSGI option, there's also uWSGI, Waitress and others, I'm just using it for these examples.
Otherwise, not that much is different from your local machine: you can still use SQLite as the database ([more here](https://mattsegal.dev/simple-django-deployment-2.html#sqlite)).

There are a few other details that I didn't mention here like [setting up DNS](https://mattsegal.dev/dns-for-noobs.html), virtual environments, babysitting Gunicorn with a supervisord like [Supervisord](https://mattsegal.dev/simple-django-deployment-4.html) or how to serve static files with [Whitenoise](http://whitenoise.evans.io/en/stable/), but this is bones of the basic setup. If you're interested in a more complete guide on how to set up a simple server like this, I wrote [a guide](https://mattsegal.dev/simple-django-deployment.html) that explains how to do that.

Most professional Django devs don't use a basic setup like this for their production environments - let's move on towards something more typical.

### Typical standalone webserver

Let's go over a simple environment that a professional Django dev might set up in production when using a single server.
It's not the exact setup that everyone will always use, but the structure is very common.

![typical server setup]({attach}django-prod-architecture/typical-server.png)

Some things same as the simple setup above: it's still a Linux virtual machine with Django being run by Gunicorn.
There are three main differences:

- SQLite has been replaced by a different database, [PostgreSQL](https://www.postgresql.org/)
- A [NGINX](https://www.nginx.com/) web server is now sitting in-front of Gunicorn in a [reverse-proxy](https://www.nginx.com/resources/glossary/reverse-proxy-server/) setup
- Static files are now being served from outside of Django

Why did we swap SQLite for PostgreSQL? In general Postgres is a litte more advanced and full featured. For example, Postgres can handle multiple writes at the same
time, while SQLite can't.

Why did we add NGINX to our setup? NGINX is a dedicated webserver which provides extra features and performance improvements
over just using Gunicorn to serve web requests. For example we can use NGINX to directly serve our app's static and media files from the file system, rather than routing our requests through Python first, which is slower. NGINX can also be configured to use HTTPS, serve redirects, log access requests and route requests to different apps on the server.
You can use Gunicorn/Django to do a lot of this stuff, but NGINX is a tool that is specifically built for these tasks. There are alternatives to NGINX like the [Apache HTTP server](https://httpd.apache.org/), but NGINX is the most widely used with Django.

It's important to note that everything here lives on a single server, which means that if the server goes away, so does all your data, unless you have backups.
This data includes your Django tables, which are stored in Postgres, and files uploaded by users, which will be stored in the MEDIA_ROOT folder, somewhere on your filesystem. Having only one server also means that if you server restarts or shuts off, so does your website. This is OK for smaller projects, but it's not acceptable for big sites like StackOverflow or Instagram.

### Single webserver with multiple apps

Once you start using NGINX and PostgreSQL, there's no reason you can't run multiple Django apps on the same machine.
NGINX is able to route incomping HTTP requests to different apps based on the domain name, and Postgres can host multiple databases on a single machine.
For example, I use a single server to host some of my personal Django projects: [Matt's Links](http://mattslinks.xyz/), [Memories Ninja](http://memories.ninja/) and [Blog Reader](https://www.blogreader.com.au/)

![multi-app server setup]({attach}django-prod-architecture/multi-app-server.png)

I've omitted the static files for simplicity. Note that having multiple apps on one server saves you hosting costs, but there are downsides: restarting the server restarts all of your apps.

### Single webserver with a worker

Some web apps need to do things other than just [CRUD](https://www.codecademy.com/articles/what-is-crud). For example, my website [Blog Reader](https://www.blogreader.com.au/) needs to scrape [text](https://slatestarcodex.com/2020/04/24/employer-provided-health-insurance-delenda-est/) from a website and then send it to an Amazon API to be translated into [audio files](https://media.blogreader.com.au/media/043dcf9fe4c1df539468000cb97af1d7.mp3). Another common example is "thumbnailing", where you upload a huge 5MB image file to Facebook and they downsize it into a crappy 120kB JPEG. These kinds of tasks do not happen inside a Django view, because they take too long to run. Instead they have to happen "offline", in a separate worker process, using tools like [Celery](http://www.celeryproject.org/), [Huey](https://huey.readthedocs.io/en/latest/django.html), [Django-RQ](https://github.com/rq/django-rq) or [Django-Q](https://django-q.readthedocs.io/en/latest/). All these tools provide you with a way to run tasks outside of Django views and do more complicated things, like co-ordinate multiple tasks and run them on schedules.

All of these tools follow a similar pattern: tasks are dispatched by Django and put in a queue where they wait to be executed. This queue is managed by a service called a "broker", which keeps track of all the tasks that need to be done. Common brokers for Django tasks are Redis and RabbitMQ. A worker process, which typically shares you Django app's code, pulls tasks out the broker and runs them.

![worker server setup]({attach}django-prod-architecture/worker-server.png)

If you haven't worked with task queues before then it's not immediately obvious how this all works, so let me give an example. You want to upload a 2MB [photo of your breakfast](https://memories-ninja-prod.s3-ap-southeast-2.amazonaws.com/original/7e26334177b6ee7d5ab4c21f7149190e.jpeg) from your phone to a Django site. To optimise image loading performance, the Django site will turn that 2MB photo upload into a 70kB [display image](https://memories-ninja-prod.s3.amazonaws.com/display/7e26334177b6ee7d5ab4c21f7149190e.jpeg) and a smaller [thumbnail image](https://memories-ninja-prod.s3.amazonaws.com/thumbnail/7e26334177b6ee7d5ab4c21f7149190e.jpeg). So this is what happenes:

- A user uploads a photo to the Django site, which sends the image data to NGINX and through to Django, which runs some view code
- The Django view saves the original photo to the filesystem and records the upload in the database
- The Django view also pushes a thumbnailing task to the task broker
- The broker receives the task and puts it in a queue, where it waits to be executed
- The worker asks the broker for the next task and the broker sends the thumbnailing tasks
- The worker reads the task description and runs some Python function, which reads the original image from the filesystem, creates the smaller thumbnail images, saves them and then updates the database record to show that the thumbnailing is complete.

If you want to learn more about this stuff, I've written guides for getting started with [offline tasks](https://mattsegal.dev/offline-tasks.html) and [scheduled tasks](https://mattsegal.dev/simple-scheduled-tasks.html) with Django Q.

### Single webserver with a cache

Sometimes you'll want to [use a cache](https://docs.djangoproject.com/en/3.0/topics/cache/) to store data for a short time. For example, caches are commonly used when you have some data that was expensive to pull from the database or an API and you want to re-use it for a little while. [Redis](https://redis.io/) and [Memcached](https://en.wikipedia.org/wiki/Memcached) are both popular cache services that are used in production with Django. It's not a very complicated setup.

![cache on server setup]({attach}django-prod-architecture/cache-on-server.png)

### Single webserver with Docker

where would you use docker?
docker really just wraps around these services
you could dockerise each app and the services they depend upon
you could dockerise just the app, or the services as well
it's possible to put the database in docker but it's really the last thing you'd dockerise

### External services

There are a few reasons why you don't want to cram all these services onto one webserver

- you don't need to do this! this is an extreme example
- show incrementally

- database on own server
- redis on own server
- broker on own server
- django app own server
- nginx often still deployed on same server as django app
- object storage can be farmed out - often for media files

why?

- you want to be able to make the web server transient
- provision different sized services for different workloads
- forces you to untangle your infrastructure
- allows you to use external services to do tasks that you don't want to
  - AWS S3
  - external database
  - container runtimes
  - load balancers
  - externally hosted redis, queue broker
  - app server to Heroku, Dokku, AWS ECS, AWS fargate etc
- allows for autoscaling later

link to configuration management talk

### Scaling groups

- you can have multiple servers doing the same job
- why not just make one server bigger?
- some redundancy if something goes wrong like a botched deployment
- scaling dynamically to save money
- blue/green deployments

### Container clusterfuck

- you can decouple your virtual machines from your applications
- use kubernets to define pods
- good for big companies that want to provide an infrastructure platform
- not good for a single developer

krazam microservices

### Next steps

pass

If you liked the box diagrams in this post check out [Exalidraw](https://excalidraw.com/).
