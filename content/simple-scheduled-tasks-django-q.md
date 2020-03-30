Title: Simple Scheduled Tasks with Django-Q
Slug: simple-scheduled-tasks
Date: 2020-03-30 12:00
Category: Django

How do you run some code once a day in Django, or every hour?
There are a lot of reasons you'd want to do this. Anybody running a backend web service will run into this problem eventually.
Maybe you want to delete some expired data, update the status of some of your models, or poll a 3rd-party API.

So you ask around online for help. If you're using Django, people will often point you to [Celery](http://www.celeryproject.org/). If you look at their website:

> Celery is an asynchronous task queue/job queue based on distributed message passing. It is focused on real-time operation, but supports scheduling as well.

Asynchronous what? It sounds scary and it's a pain in the ass to set up. If you need Celery, then it's well worth the effort, but I believe that for
most people setting up their first scheduled task in Django it's overkill.

I think the best solution for beginners is [Django-Q](https://django-q.readthedocs.io/en/latest/). It's much simpler to set up and run in production that Celery and is perfectly fine for most simple scheduling tasks.

### Getting started

Let's say I have a simple Django app that just has a list of models
