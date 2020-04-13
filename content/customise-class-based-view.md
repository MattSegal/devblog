Title: How to customise a class based view in Django
Slug: customise-class-based-view-django
Date: 2020-4-9 12:00
Category: Django

You've spend a little bit of time working on your Django app and you want to dip your toes into class-based views. The basic examples are simple enough, but once you want to do something more complicated, something more custom, you get stuck. How do you customise a class-based view?

You've written some function-based views before, and they seem pretty straightforward, it's just a function! If you want to change how it works, you just change the code inside the function. Simple - no magic, no mystery, it's just code. Customising class based views seems much less user-friendly.

In this post I'll take you through a worked example, showing you how to customise class-based views.

### Example problem

Let's start with an example problem. Say we've got a model called Article, used for publishing news online:

```python
# models.py

class Article(models.Model):

    created_at = models.DateTimeField(default=timezone.now)
    published_at = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=512)
    body_html = models.TextField()

```

We have a function-based view that lists all the articles:

```python
# views.py

def article_list_view(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'news/article_list.html', context)

```

As I mentioned earlier, this function-based code is pretty easy to customise - you just change the code! Let's say we only want to list all the _published_ articles and list them from newest to oldest:

```python
# views.py

def article_list_view(request):
    articles = (
        Article.objects
        .filter(published_at__isnull=False)
        .order_by('-published_at')
    )
    context = {'object_list': articles}
    return render(request, "news/article_list.html", context)

```

Now let's try doing the same thing with a class-based view. Listing all Articles is _super_ simple. It's like 3 lines of code:

```python
# views

class ArticleListView(ListView):
    model = Article
    template_name = "news/article_list.html"

```

Cool, cool, and now we need to do the next bit: list all the _published_ articles and list them from newest to oldest. How the fuck do we do that? Where do you even start? Are you stressed? I'm stressed.

### The fix

The fix is to read some documentation. Not the [Django docs](https://docs.djangoproject.com/en/3.0/ref/class-based-views/), which are great for a lot of topics. No, you are going to need to refer to [Classy Class-Based Views](https://ccbv.co.uk/) to keep your sanity. Let's take a peek at the documentation for [ListView](https://ccbv.co.uk/projects/Django/3.0/django.views.generic.list/ListView/).

I'm going to cut to video to show you the rest of the fix.

<div class="loom-embed"><iframe src="https://www.loom.com/embed/914ef155a98f49faba6c3c8af3d686a4" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

You can use the techniques of overriding on any of the class-based view methods, depending on what you need to do.

A common method to override is get_context_data:

```python

class ArticleListView(ListView):
    model = Article
    template_name = "news/article_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {
            **context,
            'now': timezone.now()
        }

```

In summary, when you're stuck on a class-based view:

- Go to [Classy Class-Based Views](https://ccbv.co.uk/)
- Take a peek at the attributes of the class
- Scan over the methods of the class
- Dig into the methods to figure out what you need to change
- Set any attributes that are necessary
- Override any methods that you need to change
