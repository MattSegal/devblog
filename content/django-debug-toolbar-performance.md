Title: How to diagnose and fix slow queries with Django Debug Toolbar
Description: A guide on how to find and squash slow database queries with Django Debug Toolbar
Slug: django-debug-toolbar-performance
Date: 2020-05-09 12:00
Category: Django

Your Django views are running slowly and you want to make them faster,
but you can't figure out what the issue is just by reading the code.
Just as bad is when you're not sure if you're using the Django ORM correctly - how can you know if the
code you write will be slow?

This is where a profiling tool comes in handy.
[Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io) is great
for figuring out why your Django views are going slow. This guide will show you how to use DJDT to find and fix slow database queries in your views.

The demo app shown in the video is [available on GitHub](https://github.com/MattSegal/djdt-perf-demo).

<div class="yt-embed">
    <iframe 
        src="https://www.youtube.com/embed/9uoI6pvuvYs" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen
    >
    </iframe>
</div>

The DJDT docs explain [how to install](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html) the toolbar.
