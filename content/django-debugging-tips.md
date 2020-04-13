Title: 4 tips for debugging in Django
Slug: django-debug-tips
Date: 2020-04-12 12:00
Category: Django

You've got a bug in your Django code and you can't quite figure out what's wrong. You know there's a problem, but you can't quite pin down where it's coming from. This post will share 4 tips which will help you speed up your bug catching.

### Dig deeper in your print statements

Using `print` to view data is the most basic debugging method. You're probably already doing this, so I'm going to show you how to squeeze more info out of your objects when you print them.

Basic print usage for debugging looks like this:

```python
# views.py

def my_view(request):
    thing = Things.objects.last()
    print("Check thing:", thing)
    return HttpResponse(f"The thing is called {thing.name}")

```

The problem is that when you're looking at Python objects, you might only see a string representing the object, rather than the data you want. For example the above code will print this:

```text
Check thing: <Thing: 1>
```

This is not helpful for our debugging, but there's a better way. We can use `pprint`, which "pretty prints" dictionaries, and the `__dict__` attribute, which is present on every Python object, to dig into the data in more detail:

```python
# views.py

def my_view(request):
    thing = Things.objects.last()
    from pprint import pprint
    pprint(thing.__dict__)
    return HttpResponse(f"The thing is called {thing.name}")

```

With this method we will see a nicely formatted dict, showing all the data attached to the `thing` object:

```text
{
    "_state": <django.db.models. ...>,
    "id": 1,
    "name": "the thing",
    "weight": 12,
}
```

Now you can dig deeper into your objects when printing.

Leaving a bunch of print statements in your code can pollute your app's console output. You can keep the printing but reduce the noise by [setting up logging](https://mattsegal.dev/file-logging-django.html), which then enables you to toggle how noisy your logs are using [log levels](https://docs.python.org/3/howto/logging.html).

### Python's built-in debugger

Finding bugs via print works, but it can be a slow and tedious process. You might have to run the same code dozens of times to find the problem. Wouldn't it be nice to just stop the code on a particular line and then check a bunch of variables? You can do this with Python's built-in debugger. You can get started with it by following [this guide on using pdb](https://mattsegal.dev/django-debug-pdb.html).

### Check your insanity with assertions

At some point during debugging you start to question your sanity - you don't know what to believe anymore. You start to question everything you've ever known about programming.

> When debugging, you must first accept that something you believe is true is not true. If everything you believed about this system were true, it would work. It doesn't, so you're wrong about something. ([source](https://twitter.com/cocoaphony/status/1224364439429881856))

Using Python's `assert` statement is a quick and easy way to check if something that you believe is true, is _acutally true_. `assert` is pretty simple:

- You whack `assert` in your code with an expression
- If the expression is truthy then nothing happens
- If the expression is falsy then `assert` throws an `AssertionError`

Simple, but quite useful. Here are some quick examples:

```python
# All OK, nothing happens
assert True
assert 1 == 1
assert [1, 2, 3]
a = 1
b = 1
assert a == b

# All throw AssertionError
assert False
assert 1 == 2
assert []
a = 1
b = 2
assert a == b

# You can include messages
assert False, 'This is forbidden'
# Throws AssertionError: This is forbidden

```

So how do you use this practically? Well, in a Django view, you can check all sorts of things that you believe are true. Check the assertions that you believe _maybe_ aren't true, even though they _should_ be.

```python
# views.py

def my_view(request):
    assert Thing.objects.exists(), 'there is at least 1 thing in db'
    thing = Things.objects.last()
    assert thing, 'thing exists'
    assert thing.name, 'thing has name'
    assert type(thing.name) is str, 'thing name is a str'
    return HttpResponse(f"The thing is called {thing.name}")

```

Deciding when to use print vs. assert vs. pdb comes with experience, so I recommend you give them all a try so that you can get a feel for them. These three methods are quick and simple to implement, wheras this final tip is the most useful, but also requires the most labour.

### Reproduce the bug with tests

Some bugs can be quite tricky to reproduce. To trigger the line of code that causes the bug you might need to create a new user, log in as that user, verify their email, sign in, sign out, sign in again, buy their first product... etc. etc. etc. you get the idea.

Even worse, you might have to do this series of steps dozens of times before you've fixed the bug. To avoid all of this hard work... you're going to have to do a little bit of hard work and write a test.

The bad thing about tests is that they take some time to write. The good thing about tests is that you set up the data required to run the test once, and then you've automated the process forever. Tests become more valuable the more you run them, and you can run them _a lot_:

- You can quickly re-run them to reproduce the issue
- You can run them to check that the issue is solved
- You can run them in the future to make sure that the issue never comes back

I'll give you a quick example. Say your issue is that when you call the view `my_view`, you get an error:

```python
# views.py

def my_view(request):
    thing = Things.objects.last()
    return HttpResponse(f"The thing is called {thing.name}")

```

The error is

```text
AttributeError: 'NoneType' object has no attribute 'name'
```

A quick test to run this view (using [pytest](https://docs.pytest.org/en/latest/)) is:

```python
# tests.py

@pytest.mark.django_db
def test_my_view__with_thing(client):
    """
    Check that my_view returns thing name when there is a Thing
    """
    Thing.objects.create(name="a thing")
    url = reverse("my-view")
    response = client.get(url)
    assert response.status_code == 200
    assert response.data == "The thing is called a thing"


@pytest.mark.django_db
def test_my_view__with_no_thing(client):
    """
    Check that my_view returns no thing name when there is no Thing
    """
    url = reverse("my-view")
    response = client.get(url)
    assert response.status_code == 200
    assert response.data == "The thing is called "

```

Note that even just writing these tests will show you where the code is broken, but this is just an example, so let's ignore that.

When you run these tests, you'll notice that:

- `test_my_view__with_thing` passes
- `test_my_view__with_no_thing` fails, with an `AttributeError`

Now that we've nailed down the issue with a test, we can fix the bug, update the test and re-run it to make sure the bug is fixed. Now we've automated the process of reproducing the bug and checking that it's fixed.

### Conclusion

So there you go, four tips for debugging Django:

- better print statements with `__dict__`
- Python's pdb debugger
- assert statements
- reproducing the issue with tests

Of all these four, I recommend you invest time into learning how to write tests. Effective testing has huge bang-for-buck, not just for debugging, but also for preventing bugs in the first place.
