Title: There's no one right way to test your code
Description: Don't let other people lecture you on how to test your code, except for me. Listen to me.
Slug: no-right-way-to-write-tests
Date: 2020-07-10 12:00
Category: Programming

Today I read a Reddit thread that burned my eyes and hurt my head. A beginner was stumbling over themself, apologizing for writing tests the "wrong way":

> I'm now writing some unit tests ... I know that the correct way would be to write tests first and then the code, but unfortunately it had to be done this way.

This is depressing... what causes newbies to feel the need to _ask for forgiveness_ when writing tests? You can tell the poster has either previously copped some snark or has seen someone else lectured online for not doing things the "correct way".

Of all things in software development, the idea that there is a "correct way" to write tests is particularly puzzling to me. There are so many different use-cases for automated tests that there cannot be one right way to do it.

In this post I want to review some misleading pieces of testing advice that I've seen floating around the internet and provide some general guidelines on what I think makes a suite of tests useful.

## You should write "unit tests"

People often say that you should write **unit tests** for your code. In brief, these tests check that some chunk of code returns a an specific output for a given input. For example:

```python

# The function to be tested
def add(a: int, b: int):
    """Returns a added with b"""
    return a + b


# Some tests for `add`
def test_add__with_positive_numbers():
    assert add(1, 2) == 3


def test_add__with_zero():
    assert add(1, 0) == 1

# etc. etc. etc

```

This style of testing is great under the right circumstances, but these are not the only kind of test that you can, or should, write. Unfortunately the name "unit test" is used informally to refer to all automated testing of code. This misnomer leads beginners to believe that unit tests are the best, and maybe only, way to test.

Let's start with what unit tests are good for. They favour a "bottom-up" style of coding. They're the most effective when you have a lots of little chunks of code that you want to write, test independently, and then assemble into a bigger program.

This is a perfect fit when you're writing code to deterministically transform data from one form into another, like parts of an [ETL pipeline](https://en.wikipedia.org/wiki/Extract,_transform,_load) or a compiler. These tests work best when you're writing [pure functions](https://en.wikipedia.org/wiki/Pure_function), or code with limited [side effects](<https://en.wikipedia.org/wiki/Side_effect_(computer_science)>).

## When unit tests don't make sense

The main problem with unit tests is that you can't always break your code up into pretty little pure functions.

When you start working on an existing legacy codebase there's no guarantee that the code is well-structured enough to allow for unit tests. I've encountered a fair few 2000+ line classes where reasoning about the effect of any one function is basically impossible because of all the shared state. You can't test a function if you don't know what it's supposed to do. These codebases cannot be rigourly unit tested straight away and need to be [gently massaged into a better shape over time](https://understandlegacycode.com/), which is a whole other can of worms.

Another, very common, case where unit tests don't make much sense is when a lot of the heavy lifting is being done by a framework. This happens to me all the time when I'm writing web apps with the [Django](https://www.djangoproject.com/) framework. In Django's REST Framework, we use a "serializer" class to validate data and translate Python objects into a JSON string and vice versa. For example:

```python
from django.db import models
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

# Create a data model that represents a person
class Person(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField()

# Create a serializer that can map a Person to a JSON string
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["name", "email"]

# Example usage.
p = Person(name="Matt", email="mattdsegal@gmail.com")
ps = PersonSerializer(p)
ps.is_valid() # True
JSONRenderer().render(ps.data)
# '{"name":"Matt","email":"mattdsegal@gmail.com"}'
```

In this case, there's barely anything for you to actually test.
Don't get me wrong, you _could_ write unit tests for this code, but anything you write is just a re-hash of the definitions of the `Person` and `PersonSerializer`. All the interesting stuff is handled by the framework. Any "unit test" of this code is really just a test of the 3rd party code, which [already has heaps of tests](https://github.com/encode/django-rest-framework/tree/master/tests). In this case, writing unit tests is just adding extra boilerplate to your codebase, when the whole point of using a framework was to save you time.

So if "unit tests" don't always make sense, what else can you do? There are other styles of testing that you can use. I'll highlight my two favourites: **smoke tests** and **integration tests**.

## Quick 'n dirty smoke tests

Some of the value of an automated test is checking that the code runs at all. A smoke test runs some code and checks that it doesn't crash. Smoke tests are really, really easy to write and maintain and they catch 50% of bugs (made up number). These kinds of tests are great for when:

- your app has many potential code-paths
- you are using interpreted languages like JavaScript or Python which often crash at runtime
- you don't know or can't predict what the output of your code will be

Here's a smoke test for a neural network. All it does is construct the network and feed it some random garbage data, making sure that it doesn't crash and that the outputs are the correct shape:

```python
def test_processes_noise():
    input_shape = (1, 1, 80, 256)
    inputs = get_random_input(input_shape)
    outputs = MyNeuralNet(inputs)
    assert outputs.shape == (1, 1, 80, 256)
```

Typically when training a neural net it might take minutes of runtime before your code crashes because of all the data loading and processing that needs to happen. With smoke tests like this, you can check for stupid errors in seconds instead of minutes.

In a more web-development focused example, here's a Django smoke test that loops over a bunch of urls and checks that they all respond to GET requests with happy "200" HTTP status codes, without validating any of the data that is returned:

```python
@pytest.mark.django_db
def test_urls_work(client):
    """Ensure all urls return 200"""
    for url in SMOKE_TEST_URLS:
        response = client.get(url)
        assert response.status_code == 200
```

Maybe you don't have time to write detailed tests for all your web app's endpoints, but a smoke test like this will at least exercise your code and check for stupid errors.

This crude style of testing is both fine and good. Don't let people shame you for writing smoke tests. If you do nothing but write smoke tests for your app, you'll still be getting a sizeable benefit from your test suite.

## High level integration tests

To me, integration tests are when you test a whole feature, end-to-end. You are testing a system of components (functions, classes, modules, libraries) and the _integrations_ between them. I think this style of testing can provide more bang-for-buck than a set of unit tests, because the integration tests cover a lot of different components with less code, and they check for behaviours that you actually care about. This is more "top down" approach to testing, compared to the "bottom up" style of unit tests.

Calling back to my earlier Django example, an integration test wouldn't test any independent behaviour of the the `Person` or `PersonSerializer` classes. Instead, we would test them by exercising a code path where they are used in combination. For example, we would want to make sure that a GET request asking for a specific Person by their id returns the correct data. Here's the API code to be tested:

```python
# Data model
class Person(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField()

# Maps data model to JSON string
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["name", "email"]

# API endpoint for Person
class PersonViewSet(viewsets.RetrieveAPIView):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

# Attach API endpoint to a URL path
router = routers.SimpleRouter()
router.register("person", PersonViewSet)
urlpatterns = [path("api", include(router.urls))]
```

And here's a short integration test for the code above. It used Django's [test client](https://docs.djangoproject.com/en/3.0/topics/testing/tools/#the-test-client) to simulate a HTTP GET request to our view and validate the data that is returned:

```python
@pytest.mark.django_db
def test_person_get(client):
    """Ensure a user can retrieve a person's data by id"""
    p = Person.objects.create(name="Matt", email="mattdsegal@gmail.com")
    url = reverse("person-detail", args=[p.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.data == {
        "name": "Matt",
        "email": "mattdsegal@gmail.com",
    }
```

This integration test is exercising the code of the `Person` data model, the `PersonSerializer` data mapping and the `PersonViewSet` API endpoint all in one go.

A valid criticism of this style of testing is that if the integration test fails, it's not always clear _why_ it failed. This is typically a non-issue, since you can get to the bottom of a failure by reading the error message and spending a few minutes poking the code with a debugger.

## That's not an X test it's a Y test

The level of pedantry displayed over how to name different kinds of tests irks me. Stuff like:

> Those are integration tests not unit tests

It's nice to have different names for different things, but I generally find that people focus too much whether they're doing this kind of that kind of testing, rather than focusing on _why_ they're testing their code.

There are a variety of reasons people test their code:

- for developers to get quick feedback whether the logic of their new code works
- to catch regressions in the logic of working code during development
- to catch stupid mistakes and runtime errors
- minimise the risk of shipping bugs to production

aaaaaabbb
aaaaaabbb
aaaaaabbb
aaaaaabbb

## Write tests before you code

drf example

we love tests
they are so helpful and make you so productive

but they can also be a burden
useless tests are horrible

TDD is a cult
a cargo cult
tests are

tests must be done the right way

## Some guidelines

unit tests are great, but you don't _have_ to write them to get the benefits of testing
integration tests and smoke tests are valuable
tests should reduce risk, whatever that means to you
you don't need to do TDD

Run your Python unit tests via GitHub actions
https://mattsegal.dev/pytest-on-github-actions.html
