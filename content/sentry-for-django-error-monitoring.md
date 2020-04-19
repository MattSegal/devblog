Title: Sentry is great for tracking Django errors
Description: An introduction to the Sentry error monitoring service
Slug: sentry-for-django-error-monitoring
Date: 2020-04-8 12:00
Category: Django

You've deployed a Django app to a webserver and now it's not working. Your app is throwing 500 Internal Server Errors - what's wrong? Why is this happening? It worked on my laptop!?

Even worse is when a _customer_ experienced an error 12 hours ago and _you_ need to figure out what went wrong.

### Error reporting

You need something to alert you when errors happen in production, otherwise you're flying blind. How can you fix a bug if you don't know what happened? Error reporting is important if you're a new developer, because you're going to write a lot of bugs, or if you're experienced, since other people are likely relying on your code to work.

Django allows you to set up [email reports](https://docs.djangoproject.com/en/3.0/howto/error-reporting/), which requires some fiddling with mail servers, but it's a totally OK way to track errors.

My favourite way to monitor errors is using [Sentry](https://sentry.io/welcome/). It's a SaaS product that's been used at every Django job I've worked at and I use it for my personal projects. Here's why I like it so much.

### Easy to set up

Sentry used to be a little harder to install, but now there are only 3 things you need to do in order to get started.

Install the Python package

```bash
pip install sentry-sdk
```

Set an envrionment variable

```bash
export SENTRY_DSN="https://xxx@sentry.io/yyy"
```

And run a line of Python in your _production_ settings.py

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    environment="prod"
)
```

### Rich reporting

You want as much information as possible on the incident:

- when did it happen?
- how many times did it happen?
- what URL was requested?
- what cookies were set?
- was it for a particular user?
- was it in a particular browser?
- what line of code triggered the error?
- what's the stack trace?

Sentry captures an incredible amount of info when it logs an error, sometimes including the values of variables in scope and the database queries that were run.

### Free for multiple apps

I host all my personal projects in Sentry for free. I think as long as you stick to one user you don't have to pay for it.

### Handles frontend errors

You can use Sentry in your frontend JavaScript as well, which gives you a much more complete picture of what went wrong.

### Slack integration

Some people might not like this, but if you pefer Slack to email, you can set up Sentry to post to a Slack channel when an error crops up.

### Deployment tracking

If you're willing to do a little more legwork, you can configure Sentry to track your deployments. You give it a Git commit hash and it is able to correlate errors with particular deployments, making it easier to track down the offending code. This is particularly useful if you/your team are shippng multiple deployments per day.

### Wrapping up

As you might have noticed, I'm pretty happy with Sentry, even after a few years of using it. There are a few little issues with it, like the overly-complex settings panel in the web UI, but overall it offers a low-friction user experience. Hopefully you'll get some use out of it.

Now, just because you have error monitoring set up, that doesn't mean you've done everything you need to in order to monitor your production environment. Application logging is essential as well! If you haven't already set up your Django app to write logs in production [you can find out how here](https://mattsegal.dev/file-logging-django.html).
