Title: How to find what you want in the Django documentation
Description: How to find what you're looking for in the Django documentation.
Slug: how-to-read-django-docs
Date: 2020-6-26 12:00
Category: Django

Many beginner programmers find the [Django documentation](https://docs.djangoproject.com/en/3.0/) overwhelming.

Let's say you want to learn how to perform a login for a user. Seems like it would be pretty simple: logins are a core feature of Django. If you [google for "django login"](https://www.google.com/search?q=django+login) or [search the docs](https://docs.djangoproject.com/en/3.0/search/?q=login) you see a few options, with "Using the Django authentication system" as the most promising result. You click the link, happily anticipating that your login problems will soon be over, and you get smacked in the face with [thirty nine full browser pages of text](https://docs.djangoproject.com/en/3.0/topics/auth/default/). This is way too much information!

Alternatively, you find your way to the reference page on [django.contrib.auth](https://docs.djangoproject.com/en/3.0/ref/contrib/auth/), because that's where all the auth stuff is, right? If you browse this page you will see an endless enumeration of all the different authentication models and fields and functions, but no explanation of how they're supposed to fit together.

At this stage you may want to close your browser tab in despair and reconsider your decision to learn Django. It turns out the info that you wanted was somewhere in that really long page [here](https://docs.djangoproject.com/en/3.0/topics/auth/default/#how-to-log-a-user-in) and [here](https://docs.djangoproject.com/en/3.0/topics/auth/default/#django.contrib.auth.authenticate). Why was it so hard to find? Why is this documentation so fragmented?

God forbid that you should complain to anyone about this struggle. Experienced devs will say things like "you are looking in the wrong place" and "you need more experience before you try Django". This response begs the question though: how does anyone know where the "right place" is? The table of contents in the Django documentation [is unreadably long](https://docs.djangoproject.com/en/3.0/contents/). Meanwhile, you read other people raving about how great Django docs are: what are they talking about? You may wonder: am I missing something?

Wouldn't it be great if you could go from having a question to finding the answer in a few minutes or less? A quick Google and a scan, and boom: you know how to solve your Django problem. This is possible. As a professional Django dev I do this daily. I rarely remember how to do anything from heart and I am constantly scanning the docs to figure out how to solve problems, and you can too.

In this post I will outline how to find what you want in the Django documentation, so that you spend less time frustrated and stuck, and more time writing your web app. I also include a list of key references that I find useful.

Experienced devs can be dismissive when you complain about documentation, but they're right about one thing: knowing how to read docs is a really important skill for a programmer, and being good at this will save you lots of time.

## Find the right section

Library documentation is almost always written with distinct sections. If you do not understand what these sections are for, then you will be totally lost.
If you have time, watch [Daniele Procida's excellent talk](https://www.youtube.com/watch?v=t4vKPhjcMZg) how documentation should be structured. In the talk he describes four different sections of documentation:

- **Tutorials**: lessons that show you how to complete a small project ([example](https://docs.djangoproject.com/en/3.0/intro/install/))
- **How-to guides**: guide with steps on how to solve a common problem ([example](https://docs.djangoproject.com/en/3.0/howto/custom-management-commands/))
- **API References**: detailed technical descriptions of all the bits of code ([example](https://docs.djangoproject.com/en/3.0/ref/models/querysets/))
- **Explanations**: high level discussion of design decisions ([example](https://docs.djangoproject.com/en/3.0/topics/templates/#module-django.template))

In addition to these, there's also commonly a **Quickstart** ([example](http://whitenoise.evans.io/en/stable/#quickstart-for-django-apps)), which is the absolute minimum steps you need to to do get started with the library.

The Django Rest Framework docs use a structure similar to this

![django rest framework sections]({attach}/img/drf-sections.png)

The ReactJS docs use a structure similar to this

![react sections]({attach}/img/react-sections.png)

The Django docs use a [structure similar to this](https://docs.djangoproject.com/en/3.0/#how-the-documentation-is-organized)

![django sections]({attach}/img/django-sections.png)

Hopefully you see the pattern here: all these docs have been split up into distinct sections. Learn this structure once and you can quickly navigate most documentation.
Now that you understand that library documentation is usually structured in a particular way, I will explain how to navigate that structure.

## Do the tutorial first

This might seem obvious, but I have to say it. If there is a tutorial in the docs and you are feeling lost, then do the tutorial. It is a place where the authors may have decided to introduce concepts that are key to understanding everything else. If you're feeling like a badass, then don't "do" the tutorial, but at the very least skim read it.

## Find an example, guide or overview

Avoid the [API reference](https://docs.djangoproject.com/en/3.0/ref/) section, unless you already know _exactly_ what you're looking for. You will recognise that you are in an API reference section because the title will have "reference" in it, and the content will be very detailed with few high-level explanations. For example, [django.contrib.auth](https://docs.djangoproject.com/en/3.0/ref/contrib/auth/) is a reference section - it is not a good place to learn how "Django login" works.

You need to understand how the bits of code fit together before looking at an API reference. This can be hard since most documentation, even the really good stuff, is incomplete. Still, the best thing to try is to look for overviews and explanations of framework features.

Find and scan the list of [how-to guides](https://docs.djangoproject.com/en/3.0/howto/), to see if they solve your exact problem. This will save you a lot of time if the guide directly solves your problem. Using our login example, there is no "how to log a user in" guide, which is bad luck.

If there is no guide, then quickly scan the [topic list](https://docs.djangoproject.com/en/3.0/topics/) and try and find the topic that you need. If you do not already understand the topic well, then read the overview. **Google terms that you do not understand**, like "authentication" and "authorization" (they're different, specific things). In our login case, "[User authentication in Django](https://docs.djangoproject.com/en/3.0/topics/auth/)" is the topic that we want from the list.

Once you think you sort-of understand how everything should fit together, then you can move to the detailed API reference, so that you can ensure that you're using the code correctly.

## Find and remember key references

Once you understand what you want to do, you will need to use the API reference pages to figure out exactly what code you should write. It's good to remember key pages that contain the most useful references. Here's my personal favourites that I use all the time:

- [**Settings reference**](https://docs.djangoproject.com/en/3.0/ref/settings/): A list of all the settings and what they do
- [**Built-in template tags**](https://docs.djangoproject.com/en/3.0/ref/templates/builtins/): All the template tags with examples
- [**Queryset API reference**](https://docs.djangoproject.com/en/3.0/ref/models/querysets/): All the different tools for using the ORM to access the database
- [**Model field reference**](https://docs.djangoproject.com/en/3.0/ref/models/fields/): All the different model fields
- [**Classy Class Based Views**](https://ccbv.co.uk/): Detailed descriptions for each of Django's class-based views

I don't have any of these pages bookmarked, I just google for them and then search using `ctrl-f` to find what I need in seconds.

When using Django REST Framework I often find myself referring to:

- [**Classy DRF**](http://www.cdrf.co/): Like Classy Class Based Views but for DRF
- [**Serializer reference**](https://www.django-rest-framework.org/api-guide/serializers/): To make serializers work
- [**Serializer field reference**](https://www.django-rest-framework.org/api-guide/fields/): All the different serializer fields
- [**Nested relationships**](https://www.django-rest-framework.org/api-guide/relations/#nested-relationships): How to put serializers [inside of other serializers]({attach}/img/xzibit.png)

## Search insead of reading

Most documentation is not meant to be read linearly, from start to end, like a novel: most pages are too long to read. Instead, you should strategically search for what you want. Most documentation involves big lists of things, because they're so much stuff that the authors need to explain in a lot of detail. You cannot rely on brute-force reading all the content to find the info you need.

You can use your browser's build in text search feature (`ctrl-f`) to quickly find the text that you need. This will save you a lot of scrolling and squinting at your screen. I use this technique all the time when browsing the Django docs. Here's a video of me finding out how to log in with Django using `ctrl-f`:

<div class="loom-embed"><iframe src="https://www.loom.com/embed/cc4b030513b0406c91a1eadcd08514a2" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

Here's me struggling to get past the first list by trying to read all the words with my pathetic human eyes. I genuinely did miss the "auth" section several times when trying to read that list manually while writing this post:

<div class="loom-embed"><iframe src="https://www.loom.com/embed/1be42c1709334817ab3cb055ad8acf69" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

Using search is how you navigate the enormous [table of contents](https://docs.djangoproject.com/en/3.0/contents/) or the [39 browser pages of authentication overview](https://docs.djangoproject.com/en/3.0/topics/auth/default/). You're not supposed to read all that stuff, you're supposed to strategically search it. In our login example, good search terms would be "auth", "login", "log in" and "user".

In addition, most really long pages will have a sidebar summarising all the content. If you're going to read something, read that.

![django sections]({attach}/img/docs-sidebar.png)

## Read the source code

This is kind of the documentation equivalent of "go fuck yourself", but when you need an answer and the documentation doesn't have it, then the code is the authoratative source on how the library works. There are many library details that would be too laborious to document in full, and at some point the expectation is that if you _really need to know_ how something works, then you should try reading the code. The [Django source code](https://github.com/django/django) is pretty well written, and the more time you spend immersed in it, the easier it will be to navigate. This isn't really advice for beginners, but if you're feeling brave, then give it a try.

## Summary

The Django docs, in my opionion, really are quite good, but like most code docs, they're hard for beginners to navigate. I hope that these tips will make learning Django a more enjoyable experience for you. To summarise my tips:

- Identify the different sections of the documentation
- Do the tutorial first if you're not feeling confident, or at least skim read it
- Avoid the API reference early on
- Try find a how to guide for your problem
- Try find a topic overview and explanation for your topic
- Remember key references for quick lookup later
- Search the docs, don't read them like a book
- Read the source code if you're desperate

As good as it is, the Django docs do not, and should not, tell you everything there is to know about how to use Django. At some point, you will need to turn to Django community blogs like [Simple is Better than Complex](https://simpleisbetterthancomplex.com/), YouTube videos, courses and books. When you need to deploy your Django app, you might enjoy my guide on [Django deployment]({filename}/simple-django-deployment/simple-django-deployment.md) and my overview of [Django server setups]({filename}/infra/django-prod-architecture.md).
