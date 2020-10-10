Title: Simple scheduled tasks with Django Q
Description: This post will explain how to set up scheduled code execution in Django using Django-Q.
Slug: simple-scheduled-tasks
Date: 2020-03-30 12:00
Category: Django

How do you run some code once a day in Django, or every hour? This post will explain how to set up scheduled code execution in Django using Django-Q.

There are a lot of reasons you might want to run code on a schedule. You may want to:

- Process a batch of data every night
- Send out a bunch of emails once a week
- Regularly scrape a website and store the results in the database

If you're running a backend web service, you will need to do something like this eventually.

When you ask around online for help with setting up a scheduler in Django, people will often point you to [Celery](http://www.celeryproject.org/). If you look at Celery's website:

> Celery is an asynchronous task queue/job queue based on distributed message passing. It is focused on real-time operation, but supports scheduling as well.

Asynchronous what? Distributed? Sounds complicated. Do I need that? Celery is intimidating for beginners, and it happens to be pain in the ass to set up. If you happen to need Celery, then it's well worth the effort, but I believe that it's overkill for most people.

The biggest stumbling block is that Celery requires that you set up some kind of "[broker](http://docs.celeryproject.org/en/latest/getting-started/brokers/)", which is a program which keeps track of all the tasks that need to be done. You will need to install and run a program like [Redis](https://redis.io/) or [RabbitMQ](https://www.rabbitmq.com/) to run Celery, which makes getting started more complciated, and gives you more infrastructure to worry about.

I think the best solution for beginners is [Django-Q](https://django-q.readthedocs.io/en/latest/). It's simpler to set up and run in production than Celery, and it is perfectly fine for basic scheduling tasks. Django-Q can use just your existing database as a broker, which means you don't have to set up any new infrastructure. If you find that you need to use a different broker later on, then you can swap out the database for something else.

## Example project

The [Django-Q installation docs](https://django-q.readthedocs.io/en/latest/install.html) are reasonably good, but if you're new to programming you might struggle to put all the pieces together. I've created a worked example to try to give you the full picture. You can check out the full code on [GitHub](https://github.com/MattSegal/devblog-examples/tree/master/django-q-scheduling-example).

Let's say I have a Django app that is and online store which has a Discount model. This model keeps track of:

- when it was created (`created_at`)
- the amount that should be discounted (`amount`)

```python
#  discounts/models.py

class Discount(model.Model):
    created_at = models.DateTimeField(default=timezone.now)
    amount = models.IntegerField()

```

And let's say that every minute I want to delete every discount that is older than a minute. It's a silly thing to do, but this is just an learning example. So how do we set up Django-Q to do this?

{% from 'mail.html' import mailchimp %}
{{ mailchimp("Get more Django tips by email", "Enter your email address", "Subscribe") }}


## Install the package

First thing to do is install the Django-Q package:

```bash
pip install django-q
```

## Configure settings

Then we need to adjust our Django settings so that Django knows that it should use the Django-Q app. We also need to configure Django-Q to use the database as the task broker.

```python
# shop/settings.py

# Add Django-Q to your installed apps.
INSTALLED_APPS = [
    # ...
    'django_q'
]

# Configure your Q cluster
# More details https://django-q.readthedocs.io/en/latest/configure.html
Q_CLUSTER = {
    "name": "shop",
    "orm": "default",  # Use Django's ORM + database for broker
}

```

## Apply migrations

Once this is done, we need to run our database migrations to create the tables that Django-Q needs:

```bash
./manage.py migrate
```

## Create a task

Next we need to create the task function that will be called every minute. I've decided to put mine in a `tasks.py` module. You can see below that there's nothing special about this - just a plain old Python function.

```python
# discounts/tasks.py

def delete_expired_discounts():
    """
    Deletes all Discounts that are more than a minute old
    """
    one_minute_ago = timezone.now() - timezone.timedelta(minutes=1)
    expired_discounts = Discount.objects.filter(
        created_at__lte=one_minute_ago
    )
    expired_discounts.delete()

```

## Create a schedule

Now that we have a task ready to run, we need to add a scheduled task to the database. We can do this on the admin site at `/admin/django_q/schedule/add/`, or we can create and save a Schedule instance ([docs here](https://django-q.readthedocs.io/en/latest/schedules.html)) using the Django shell:

```bash
./manage.py shell
from django_q.models import Schedule
Schedule.objects.create(
    func='discounts.tasks.delete_expired_discounts',
    minutes=1,
    repeats=-1
)
```

## Run the scheduler

Finally, we need to run the Django-Q process. When using Django, you will usually have one process that is responsible for serving web requests and a separate one that takes care of processing tasks. During local development, these two processes are:

- web requests: `./manage.py runserver`
- async tasks: `./manage.py qcluster`

So if you don't run the qcluster management command, the scheduled task will never run. To get this process started, open a new terminal window start the Django-Q cluster via the Django management script:

```bash
./manage.py qcluster
```

Now you should see your scheduled task processing in the console output:

```text
12:54:18 [Q] INFO Process-1 created a task from schedule [2]
```

You can also see what's going on in the Django admin site at `/admin/django_q/`.

...and that's it! You can now run scheduled tasks in Django.
