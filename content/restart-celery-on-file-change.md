Title: How to restart Celery on file change
Description: Quick guide on how to use Watchdog
Slug: restart-celery-on-file-change
Date: 2020-04-7 12:00
Category: Django

I use Celery and Django together a lot. My biggest pain when doing local development with Celery is that the worker process won't restart when I change my code. Django's `runserver` restarts on code change, why can't Celery? How can you set up your dev envrionent to force Celery to restart on file change?

[Watchdog](https://github.com/gorakhargosh/watchdog) is a nifty little (cross-platform?) Python library that watches for filesystem changes. We can use Watchdog to restart _anything_ on file change.

First, you need to install it in your local Python environment:

```bash
pip install watchdog[watchmedo]
```

Let's say you normally start Celery like this:

```bash
celery worker --broker redis://localhost:6379 --app myapp
```

Now you can start it like this:

```bash
watchmedo \
	auto-restart \
	--directory ./my-code/ \
	--recursive \
	--pattern '*.py' \
	-- \
    celery worker --broker redis://localhost:6379 --app myapp
```

That's it! Watchdog will restart the process on file change. If you like, you can specify:

- multiple code directories using --directory
- different file patterns using --pattern
