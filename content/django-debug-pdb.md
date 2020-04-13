Title: Quickly fix bugs in Django with Python's debugger
Slug: django-debug-pdb
Date: 2020-04-11 12:00
Category: Django

There's a bug in your Django code. You've tried to track down the problem with "print" statements, but it's such a slow, tedious process:

- Add a "print" statement to your code
- Refresh the page in your browser to re-run your code
- Look at the `runserver` console output for the "print" results

Repeat this 100 times, maybe you find the issue. Is there a faster way to find and fix bugs in Django?

### Python's built-in debugger

Python's standard library comes with a debugging tool and it is easily the most efficient tool for diving into your code and figuring out what's happening. Using the debugger is as simple as taking a Django view like this:

```python
# views.py

def some_view(request):
    """Shows user some stuff"""
    things = Thing.objects.all()
    stuff = get_stuff(things)
    return HttpResponse(f"The stuff is {stuff}")

```

... and then whacking a single line of code into the view:

```python
# views.py

def my_view(request):
    """Shows user some stuff"""
    things = Thing.objects.all()

    # Start debugging here
    import pdb;pdb.set_trace()

    stuff = get_stuff(things)
    return HttpResponse(f"The stuff is {stuff}")

```

That's it, you're now using Python's debugger.

### Yeah, but, what's it do?

Here's a short video I made showing you an example of using pdb in a Django view:

<div class="loom-embed"><iframe src="https://www.loom.com/embed/7de384817fbc45f0918995646b199055" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

### Quick reference

The [Python pdb docs](https://docs.python.org/3/library/pdb.html) tell you all the commands, but for completeness, here are the commands I used:

- `__dict__` - print Python object attributes as a dictionary
- `type()` - print object type
- `l / ll` - show the current line of code
- `n` - execute next line
- `s` - step inside function
- `c` - exit debugger, continue running code
- `q` - quit debugger, throw an exception

Some extra commands worth trying, which I didn't show you:

- `help` - print debugger help
- `dir()` - print Python object functions available
- `locals()` - print local variables
- `globals()` - print global variables

### Why the command line?

You might be wondering why I insist on using pdb from the command line rather than using some fancy integrated IDE like PyCharm or Visual Studio. Basically I think these tools take too long to set up. Using pdb requires no set up time with nothing to install. If you use an IDE-based debugger, then anytime you switch editors you'll need to set up your debugging tools. You don't want to waste time debugging your debugger. No thanks!

### Bonus tip: run debugger on any exception

You can also set up pdb to start running anytime there is an exception:

```bash
python -m pdb -c continue myscript.py
```

This doesn't work for Django, because of the way `runserver` handles exceptions, but you can use it for your other Python scripting.

If you're testing Django with pytest you can force the testing tool to drop into the pdb debugger when it hits an error:

```bash
pytest --pdb
```

### Next steps

Go out there and use pdb - it's one line of code! If you really want to step up your debugging, then I recommend learning how to write tests that reproduce your issue, and then use pdb in concert with your tests to find a fix, and make sure it stays fixed.
