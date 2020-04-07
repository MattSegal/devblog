Title: Fix long running tasks in Django views
Slug: offline-tasks
Date: 2020-04-2 12:00
Category: Django

What do you do if you have a Django view that runs too slow? Slow views are a bad user experience. Users hate waiting. Even worse, if the view takes too long to return a response, they will receive a "408 Request Timeout" error, completely ruining the website experience.

Sometimes you can fine tune your code and improve the performance enough to fix the slow runtime, but sometimes there's nothing you can do to make it faster. What do you do when your code looks like this?

```python
# views.py

def my_slow_view(request):
    """
    Performs a long running task for the user (slow response time).
    """
    long_running_task(request.user) # Takes 30s
    return HttpResponse("Your task is finished!")

```

This kind of situation can happen when you have to:

- call out to an external API which is slow
- do some computationally expensive data crunching
- make some slow database queries
- any combination of the above

So how do you fix this problem? You can't make your `long_running_task` any faster - that's out of your control, so what can you do? The solution is to push the execution of your long running task _somewhere else_.

### Somewhere else?

In Django, when your view function runs, everything is happening on one thread. That is to say, each line of code has to run one after the other. We want to push our long running code into a different thread so that the view doesn't have to wait for our task to finish before it can return a response. We want to do something like this:

```python
# views.py

def my_fast_view(request):
    """
    Performs a long running task for the user (quick response time).
    """
    run_offline(long_running_task, request.user) # Takes 0.01s
    # ... runs for 30s somewhere else.
    return HttpResponse("Your will task be finished soon!")

```

This is a common problem and Django has a lot of tools that will provide this functionality. There's [Celery](http://www.celeryproject.org/), [Huey](https://huey.readthedocs.io/en/latest/django.html), [Django Redis Queue](https://github.com/rq/django-rq). For most projects I recommend using [Django Q](https://django-q.readthedocs.io/en/latest/), for the reasons outlined in [this post](https://mattsegal.dev/simple-scheduled-tasks.html).

### Setting up Django Q

To get started you need Django Q set up. You can skip past this section to the worked example below and do this later.

The first thing to do is install the Django Q package alongside Django:

```bash
pip install django-q
```

#### Configure settings

Then we need to adjust our Django settings so that Django knows that it should use the Django Q app. We also need to configure Django Q to use the database as the task broker.

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

#### Apply migrations

Once this is done, we need to run our database migrations to create the tables that Django Q needs:

```bash
./manage.py migrate
```

#### Run the task process

Finally, we need to run the Django Q process. This is the "somewhere else" where our long-running tasks will execute. If you don't run the qcluster management command, your offline tasks will never run. To get this process started, open a new terminal window start the Django Q cluster via the Django management script:

```bash
./manage.py qcluster
```

### Worked example

Imagine you run a stock-trading website. Your user owns a bunch of stocks - like 60 different stocks. Sometimes they want to click a button to refresh all their stocks so they can see the latest prices. The problem is that you need to hit a 3rd party API to get the new prices. Say each API call takes 500ms, that's 30s of waiting!

#### Slow version

Consider the following Stock model:

```python
# models.py

class Stock(models.Model):
    code = models.CharField(max_length=16)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

```

... and this slow view:

```python
# views.py

def refresh_stocks_view(request):
    """
    Refreshes a user's stocks (slow version)
    """
    stocks = Stocks.objects.filter(user=request.user)
    # Go through all stocks and update prices, takes at least 30s
    for stock in stocks:
        stock.price = some_api.fetch_price(stock.code)
        stock.save()

    return render(request, 'stocks.html', {'stocks': stocks})

```

#### Fast offline version

We can start by moving the slow code into a task function, which will run inside of Django Q. By convention, I like to put these into a `tasks.py` module:

```python
# task.py

def refresh_stocks_task(stock_ids):
    """
    Refreshes all stocks in `stock_ids`, a list of ids.
    """
    stocks = Stocks.objects.filter(id__in=stock_ids).all()
    # Go through all stocks and update prices, takes at least 30s
    for stock in stocks:
        stock.price = some_api.fetch_price(stock.code)
        stock.save()

```

Note that the task function takes a list of ids (`stock_ids`) - why not a list of Stock objects? The reason is that when Django Q stores the task in the database, waiting for execution, the task arguments are serialized as a string (or something like that). A Django model cannot be serialized into a string, so we need to use the ids instead.

Now that we've created the task function, we just need to call it from our view:

```python
# views.py
from django_q.tasks import async_task
from .tasks import refresh_stocks_task

def refresh_stocks_view(request):
    """
    Refreshes a user's stocks (fast version)
    """
    stocks = Stocks.objects.filter(user=request.user)
    stock_ids = stocks.values_list('id', flat=True)
    # Dispatch task to Django Q - runs in <1s
    async_task(refresh_stocks_task, stock_ids)
    return render(request, 'stocks.html', {'stocks': stocks})


```

That's basically it, but there's one level of complexity we can add for a better user experience.

#### Loading state

In the slow version, the user submits a request, waits 30s and eventually gets a response back with the new stock prices. In the fast version, the user gets a response back much faster, but their stock data isn't updated yet! They'll have to wait 30s and refresh the page to get the latest data, but there's no indication that anything happened. We can add a loading state the Stocks model to help the user understand what is going on:

```python
# models.py

class Stock(models.Model):
    code = models.CharField(max_length=16)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_loading = models.BooleanField(default=False)

```

Then in the view we can set all our pending Stocks to "loading":

```python
# views.py
from django_q.tasks import async_task
from .tasks import refresh_stocks_task

def refresh_stocks_view(request):
    """
    Refreshes a user's stocks (fast version)
    """
    stocks = Stocks.objects.filter(user=request.user)
    stock_ids = stocks.values_list('id', flat=True)
    stocks.update(is_loading=True)
    # Dispatch task to Django Q - runs in <1s
    async_task(refresh_stocks_task, stock_ids)
    return render(request, 'stocks.html', {'stocks': stocks})

```

Finally, we can set the Stock state back to "not loading" when the new price is fetched:

```python
# task.py

def refresh_stocks_task(stock_ids):
    """
    Refreshes all stocks in `stock_ids`, a list of ids.
    """
    stocks = Stocks.objects.filter(id__in=stock_ids).all()
    # Go through all stocks and update prices, takes at least 30s
    for stock in stocks:
        stock.price = some_api.fetch_price(stock.code)
        stock.is_loading = False
        stock.save()

```

Now the user will request a refresh, see that all of their stocks are loading, and when the new prices have been set the user will see them once they refresh the page again.

That's it, hopefully you can now get started doing offline processing in Django. Enjoy!
