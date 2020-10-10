Title: How to save Django logs in production
Description: A guide for setting up file logging in production with Django
Slug: file-logging-django
Date: 2020-04-10 12:00
Category: Django

You've deployed Django to a webserver and something has broken. There's an error _somewhere_. What happened? When you're debugging Django on your local computer, you can just throw a print statement into your code and check the output in the runserver logs. What about in production? Where do the logs go there? How can I set up Django so it's easy to see what is happening?

## Write your logs to a file

You need to get your deployed Django app to write its logs to a file, so that you can look at them later. You can do this by configuring Django's settings. You will also need to use Python's logging library, rather than print statements. Why use logging over print? The logging library generally makes it easier to manage logs in production. Specifically, it makes it easier to:

- write logs to a file
- track extra data like the current time and function
- filter your logs

You might be thinking that using "print" works fine when you're using Django's dev web server. It's true! Using "print" works fine locally, but when you're in production with DEBUG=False, you won't be able to see your print statements anymore in Django's log output. Log messages will still show up when you're working locally so there's nothing to lose by ditching print for logging.

## How to use logging in Django

Before you set Django up to write logs to a file, you need to use Python's logging framework to write any log messages that you want to record. It's pretty easy, you just need to set it up in each module that needs it. For example, in one of your views:

```python
# views.py
# Import logging from Python's standard library
import logging

# Create a logger for this file
logger = logging.getLogger(__file__)

def some_view(request):
    """
    Example view showing all the ways you can log messages.
    """
    logger.debug("This logs a debug message.")
    logger.info("This logs an info message.")
    logger.warn("This logs a warning message.")
    logger.error("This logs an error message.")
    try:
        raise Exception("This is a handled exception")
    except Exception:
        logger.exception("This logs an exception.")

    raise Exception("This is an unhandled exception")
    return HttpResponse("this worked")

```

Most of the time I just use:

- logger.info for events I want to track, like a purchase being made
- logger.error for logical errors, like things that should never happen according to business rules
- logger.exception for when I catch an exception

Once you've configured your logging in your settings (shown further below), you'll see messages like this appear in your log file (thanks to the info, warn and error methods):

```text
2020-04-10 03:35:05 [INFO    ] (views.some_view) This logs an info message.
2020-04-10 03:35:05 [WARNING ] (views.some_view) This logs a warn message.
2020-04-10 03:35:05 [ERROR   ] (views.some_view) This logs an error message.
```

And you'll see your message plus a stack trace when you log using the exeption method:

```text
2020-04-10 03:35:05 [ERROR   ] (views.some_view) This logs an exception.
Traceback (most recent call last):
  File ".../myproj/views.py", line 14, in log_view
    raise Exception("This is a handled exception")
Exception: This is a handled exception
```

And you'll still get an error log and stack track for your unhandled exceptions:

```text
2020-04-10 03:35:05 [ERROR   ] (log.log_response) Internal Server Error:
Traceback (most recent call last):
  File ".../exception.py", line 34, in inner
    response = get_response(request)
  File ".../base.py", line 115, in _get_response
    response = self.process_exception_by_middleware(e, request)
  File ".../base.py", line 113, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File ".../myproj/views.py", line 18, in log_view
    raise Exception("This is an unhandled exception")
Exception: This is an unhandled exception
```

Importantly, you won't see any results from print statements, which is why you can't use them for production logging.

{% from 'mail.html' import mailchimp %}
{{ mailchimp("Get more Django tips by email", "Enter your email address", "Subscribe") }}

## How to set up file logging

Now that you're sold on logging and you know how to use it in your code, you can set it up in your Django settings.

I like to do this by splitting my settings module up into two files - one for dev and one for production. Usually your Django project's main app will have your settings set up something like this:

```text
myapp
├── settings.py
├── urls.py
└── wsgi.py
```

I recommend turning settings into a folder, and moving the original settings.py file into the folder's \_\_init\_\_.py file:

```text
myapp
├── settings
|   ├── __init__.py
|   └── prod.py
├── urls.py
└── wsgi.py
```

So that \_\_init\_\_.py has all your original settings

```python
# __init__.py
# Base settings for myapp
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "xxx"
DEBUG = True
ALLOWED_HOSTS = []
# ... all the regular Django settings ...
```

and prod.py has your production-only settings:

```python
# prod.py
# Production settings for myapp
from . import *  # Import base settings from settings/__init__.py

ALLOWED_HOSTS = ["www.myapp.com"]
DEBUG = False
# ... whatever else you need ...
```

In this prod.py settings file, I recommend adding the following logging config:

```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["file"]},
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "/var/log/django.log",
            "formatter": "app",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True
        },
    },
    "formatters": {
        "app": {
            "format": (
                u"%(asctime)s [%(levelname)-8s] "
                "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}
```

This is, admittedly, a horrific clusterfuck of configuration. It burns my eyes and I imagine it makes you want to slam your laptop shut and run away screaming. If you want to know how it all works, I recommend watching [this presentation](https://www.youtube.com/watch?v=DxZ5WEo4hvU). If not, feel free to blindly copy now and figure it out later.

The relevant area for you is in `LOGGING["handlers"]["file"]`. This dict defines the bit that acutally writes our logs to the file. The important key is "filename", which defines the filepath where your logs will be written. You might want to change this depending on your preferences.

## Use prod settings in production

The last little trick you need is to tell Django to use your prod settings in production. You can do this a few ways, I like to do it by setting the DJANGO_SETTINGS_MODULE environment variable.

When I launch gunicorn, I do this:

```bash
# Set Django settings to use prod.py
export DJANGO_SETTINGS_MODULE=myproj.settings.prod

# Launch gunicorn as-per-normal
gunicorn myproj.wsgi:application
```

## Bonus round: gunicorn logs

If you're using gunicorn as your WSGI app server in production, you might also want to track your gunicorn logs. This will give you information about incoming web requests, and the app starting and stopping, which can be useful when debugging. To do this, you just need to set some command-line flags:

```bash
# Set Django settings to use prod.py
export DJANGO_SETTINGS_MODULE=myproj.settings.prod

# Create logging folder for gunicorn.
mkdir -p /var/log/gunicorn

# Launch gunicorn with access and error logging.
gunicorn myproj.wsgi:application \
    --error-logfile /var/log/gunicorn/error.log \
    --access-logfile /var/log/gunicorn/access.log
```

Gunicorn's access logs look something like this, telling you about incoming web requests:

```text
127.0.0.1 - - [10/Apr/2020:02:46:09 +0000] "GET /logs/ HTTP/1.1" 400 143 ...
127.0.0.1 - - [10/Apr/2020:02:46:43 +0000] "GET /logs/ HTTP/1.1" 500 145 ...
```

And the error logs are mostly information about the app booting up and stopping:

```text
[2020-04-10 12:45:57 +1000] [14814] [INFO] Starting gunicorn 20.0.4
[2020-04-10 12:45:57 +1000] [14814] [INFO] Listening at: http://127.0.0.1:8000
[2020-04-10 12:45:57 +1000] [14814] [INFO] Using worker: sync
[2020-04-10 12:45:57 +1000] [14817] [INFO] Booting worker with pid: 14817
[2020-04-10 12:46:38 +1000] [14814] [INFO] Handling signal: int
[2020-04-10 02:46:38 +0000] [14817] [INFO] Worker exiting (pid: 14817)
[2020-04-10 12:46:38 +1000] [14814] [INFO] Shutting down: Master
```

Both of these can be pretty useful when debugging issues in production.

## Next steps

Once you've conifgured all of this, you'll be able to log into your webserver and see all your info events, error messages, access logs and gunicorn events. Finding and fixing an error in prod will be much easier with these logs.

Wouldn't it be nice if you didn't have to log into production to see these messages though? Even better, wouldn't it be great to search through your logs? That's when log aggregation tools like Papertrail or SumoLogic come in handy. I've written a guide on how to set up Papertrail [here](https://mattsegal.dev/django-logging-papertrail.html).

In addition, if you're running a professional operation, wouldn't it be good to get alerts when you have errors? That's when you need to [set up error reporting](https://mattsegal.dev/sentry-for-django-error-monitoring.html) as well as logging.
