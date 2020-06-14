Title: How to generate lots of dummy data for your Django app
Description: How to quickly and repeatedly populate your Django app
Slug: django-factoryboy-dummy-data
Date: 2020-6-14 12:00
Category: Django

It sucks when you're working on a Django app and all your pages are empty.
For example, if you're working on a forum webapp, then all your discussion boards will be empty by default:

![dummy-threads-empty]({attach}dummy-threads-empty.png)

Manually creating enough data for your pages to look realistic is a lot of work.
Wouldn't it be nice if there was an automatic way to populate your local database with dummy data
that looks real? Eg. your forum app has many threads:

![dummy-threads]({attach}dummy-threads-full.png)

Even better, wouldn't it be cool if there was an easy way to populate each thread with as many comments
as you like?

![dummy-comments]({attach}dummy-comments.png)

In this post I'll show you how to use [Factory Boy](https://factoryboy.readthedocs.io/en/latest/) and a few other tricks to quickly and repeatably generate an endless amount of dummy data for your Django app. By the end of the post you'll be able to generate all your test data using a management command:

```bash
./manage.py setup_test_data
```

There is example code for this blog post hosted in [this GitHub repo](https://github.com/MattSegal/djdt-perf-demo).

### Example application

In this post we'll be working with an example app that is an online forum. There are four models that we'll be working with:

```python
# models.py

class User(models.Model):
    """A person who uses the website"""
    name = models.CharField(max_length=128)


class Thread(models.Model):
    """A forum comment thread"""
    title = models.CharField(max_length=128)
    creator = models.ForeignKey(User)


class Comment(models.Model):
    """A comment by a user on a thread"""
    body = models.CharField(max_length=128)
    poster = models.ForeignKey(User)
    thread = models.ForeignKey(Thread)


class Club(models.Model):
    """A group of users interested in the same thing"""
    name = models.CharField(max_length=128)
    member = models.ManyToManyField(User)
```

### Building data with Factory Boy

We'll be using [Factory Boy](https://factoryboy.readthedocs.io/en/latest/) to generate all our dummy data. It's a library that's built for automated testing, but it also works well for this use-case. Factory Boy can easily be configured to generate random but realistic data like names, emails and paragraphs by internally using the [Faker](https://faker.readthedocs.io/en/master/) library.

When using Factory Boy you create classes called "factories", which each represent a Django model. For example, for a user, you would create a factory class as follows:

```python
# factories.py
import factory
from factory.django import DjangoModelFactory

from .models import User

# Defining a factory
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    name = factory.Faker("first_name")

# Using a factory with auto-generated data
u = UserFactory()
u.name # Kimberly
u.id # 51

# You can optionally pass in your own data
u = UserFactory(name="Alice")
u.name # Alice
u.id # 52
```

You can find the data types that Faker can produce by looking at the "[providers](https://faker.readthedocs.io/en/master/providers.html)" that the library offers. Eg. I found "first_name" by reviewing the options inside the [person provider](https://faker.readthedocs.io/en/master/providers/faker.providers.person.html).

Another benefit of Factory boy is that it can be set up to generate related data using [SubFactory](https://factoryboy.readthedocs.io/en/latest/recipes.html#dependent-objects-foreignkey), saving you a lot of boilerplate and time. For example we can set up the `ThreadFactory` so that it generates a `User` as its creator automatically:

```python
# factories.py
class ThreadFactory(DjangoModelFactory):
    class Meta:
        model = Thread

    creator = factory.SubFactory(UserFactory)
    title = factory.Faker(
        "sentence",
        nb_words=5,
        variable_nb_words=True
    )

# Create a new thread
t = ThreadFactory()
t.title  # Room marriage study
t.creator  # <User: Michelle>
t.creator.name  # Michelle
```

The ability to automatically generate related models and fake data makes Factory Boy quite powerful. It's worth taking a quick look at the [other suggested patterns](https://factoryboy.readthedocs.io/en/latest/recipes.html) if you decide to try it out.

### Adding a management command

Once you've defined all the models that you want to generate with Factory Boy, you can write a [management command](https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html) to automatically populate your database. This is a pretty crude script that doesn't take advantage of all of Factory Boy's features, like sub-factories, but I didn't want to spend too much time getting fancy:

```python
# setup_test_data.py
import random

from django.db import transaction
from django.core.management.base import BaseCommand

from forum.models import User, Thread, Club, Comment
from forum.factories import (
    UserFactory,
    ThreadFactory,
    ClubFactory,
    CommentFactory
)

NUM_USERS = 50
NUM_CLUBS = 10
NUM_THREADS = 12
COMMENTS_PER_THREAD = 25
USERS_PER_CLUB = 8

class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [User, Thread, Comment, Club]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")
        # Create all the users
        people = []
        for _ in range(NUM_USERS):
            person = UserFactory()
            people.append(person)

        # Add some users to clubs
        for _ in range(NUM_CLUBS):
            club = ClubFactory()
            members = random.choices(
                people,
                k=USERS_PER_CLUB
            )
            club.user.add(*members)

        # Create all the threads
        for _ in range(NUM_THREADS):
            creator = random.choice(people)
            thread = ThreadFactory(creator=creator)
            # Create comments for each thread
            for _ in range(COMMENTS_PER_THREAD):
                commentor = random.choice(people)
                CommentFactory(
                    user=commentor,
                    thread=thread
                )
```

Using the `transaction.atomic` decorator makes a big difference in the runtime of this script, since it bundles up 100s of queries and submits them in one go.

### Images

If you need dummy images for your website as well then there are a lot of great free tools online to help. I use [adorable.io](https://api.adorable.io) for dummy profile pics and [Picsum](https://picsum.photos/) or [Unsplash](https://unsplash.com/developers) for larger pictures like this one: [https://picsum.photos/700/500](https://picsum.photos/700/500).

![picsum-example](https://picsum.photos/700/500)

### Next steps

Hopefully this post helps you spin up a lot of fake data for your Django app very quickly.
If you enjoy using Factory Boy to generate your dummy data, then you also might like incorporating it into your unit tests.
