Title: Is Django too slow?
Description: A discussion of Django's performance
Slug: is-django-too-slow
Date: 2020-7-17 12:00
Category: Django

Does Django have "bad performance"?
The framework is now is 15 years old, is it out of date?
I mean, [look at these benchmarks](https://medium.com/@mihaigeorge.c/web-rest-api-benchmark-on-a-real-life-application-ebb743a5d7a3): the NodeJS-based Express framework is consistently getting better numbers than Django.

If you are learning Django in 2020 you might be worried that you're wasting time with an inferior technology.
In this post I'll explore web application performance and try to convince you that Django's performance is perfectly fine for most use-cases.

## Benchmarks

Let's start by digging into the ad-hoc web app performance benchmarks that you'll see pop up on Medium from time to time. To produce a graph like the one below, the author of [this article](https://medium.com/@mihaigeorge.c/web-rest-api-benchmark-on-a-real-life-application-ebb743a5d7a3) sets up a server for each of the frameworks tested and spams them with a bunch of HTTP requests. The benchmarking tool counts number of requests served per second by each framework.

![benchmark]({attach}img/benchmark.png)

These results are interesting in the same way that it's interesting that a man once ate [73 hotdogs in 10 minutes](https://nathansfamous.com/the-stand/hdec-fun-facts/). "Huh, cool... I guess" sums up my reaction. Why do I find these numbers so underwhelming? It's because they're irrelevant to practical web development. PHP Laravel, the worst performing framework on this chart still served **76 requests per second** on a $5/month webserver. With baseline numbers like that, what does it matter if NodeJS served 3000 requests per second? It's like saying some guy ate 200 hotdogs in 10 minutes instead of 73. Yeah, I get it, it's a lot of hotdogs: _who cares_?

So what kind of performance metrics should you pay attention to when working on your Django app?

## What do you mean by "performance"?

When you ask whether a framework or language is "slow", you have to also ask "slow at what?" and "why do you care?".
Fundamentally I think there are really only two performance goals you care about: a good user experience and low hosting cost. How much money does running this website cost me, and do people enjoy using my website? For user experience I'm going to talk about two factors:

- Response time: how long people need to wait before their requests are fulfilled
- Concurrency: how many people can use your website at the same time

Cost, on the other hand, is typically proportional to compute resources: how many CPU cores and GB of RAM you will need to run your webapp.

## Response time in Django

Users don't like waiting for their page to load, so the less time they have to wait, the better. There are a few different
metrics that you could use to measure page load speed, such as [time to first byte](https://web.dev/time-to-first-byte/) or [first contentful paint](https://web.dev/first-contentful-paint/), both of which you can check with [PageSpeed Insights](https://developers.google.com/speed/pagespeed/insights/). Faster responses don't benefit your user linearly though, not every 5x improvement in response is equally beneficial. A user getting a response in:

- 5s compared to 25s transforms the app from "broken" to "barely useable"
- 1s compared to 5s is a huge improvement
- 200ms instead of 1s is good
- 50ms instead of 200ms is nice, I guess, but many people wouldn't notice
- 10ms instead of 50ms is imperceptible, no one can tell the difference

So if someone says "this framework is 5x faster than that framework blah blah blah" it really doesn't mean anything without more context.
The important question is: will your users notice? Will they care?

So, what makes a page load slowly in Django? The most common beginner mistakes are using too many database queries or making slow API calls to external services.
I've written previously on how to [find and slow database queries with Django Debug Toolbar](https://mattsegal.dev/django-debug-toolbar-performance.html) and how to [push slow API calls into offline tasks](https://mattsegal.dev/offline-tasks.html). There are **many** other ways to make your Django web pages or API endpoints load slowly, but if you avoid these two major pitfalls then you should be able to serve users with a time to first byte (TTFB) of 1000ms or less and provide a reasonable user experience.

## When is Django's response time not fast enough?

Django isn't perfect for every use case, and sometimes it can't respond to queries fast enough.
There are some aspects of Django that are hard to optimise without giving up much of the convenience that makes the framework attractive in the first place.
You will always have to wait for Django when it is:

- running requests through middleware (on the way in and out) 
- serializing and deserializing JSON strings
- building HTML strings from templates
- converting database queries into Python objects
- running garbage collection

All this stuff run really fast on modern computers, but it is still overhead.
Most humans don't mind waiting roughly a second for their web page to load, but machines can be more impatient.
If you are using Django to run an API, where it is primarily computer programs talking to other computer programs, then it _may_ not be fast enough.
Some applications where you would consider ditching Django to shave off some latency are:

- a stock trading marketplace
- an global online advertisement serving network
- a low level infrastructure control API

If you find yourself sweating about an extra 100ms here or there, then maybe it's time to look at alternative web frameworks or languages. If the difference between a 600ms and 500ms TTFB doesn't mean much to you, then Django is totally fine.

## Concurrency in Django

As we saw in the benchmark above, Django web apps can handle multiple requests at the same time. This is important if your application has many users on your website at the same time. If too many people try to use your site at the same time, then it will eventually become overwhelmed, and they will receive errors or timeouts. In Australia, our government's household census website was [famously overwhelmed](https://www.abc.net.au/news/2016-08-09/abs-website-inaccessible-on-census-night/7711652) when the entire country tried to access an online form in 2016. This effect is often called the "[hug of death](https://en.wikipedia.org/wiki/Slashdot_effect)" and associated with small sites becoming popular on Reddit or Hacker News.

A Django app's [WSGI server](https://mattsegal.dev/simple-django-deployment-2.html#wsgi) is the thing that handles multiple concurrent requests. I'm going to use [Gunicorn](https://gunicorn.org/), the WGSI server I know best, as a reference. Gunicorn can provide two kinds of concurrency: multiple child worker processes and multiple threads per worker. If you don't know what a "process" or a "thread" is, then whatever, suffice to say you can set Gunicorn up to handle multiple requests at the same time. 

But then what happens if a new request comes in and all the workers/threads are busy? I'm a little fuzzy on this, but I believe these extra requests get put in a queue, which is managed by Gunicorn. It appears that the [default length](https://docs.gunicorn.org/en/stable/settings.html#backlog) of this queue is 2048 requests. So if the workers get overwhelmed, then the extra requests get put on the queue so that the workers can (hopefully) process them later. Typically NGINX will timeout any connections that have not received a response in 60s or less, so if a request gets put in the queue and does't get responded to in 60s, then the user will get a HTTP 504 "Gateway Timeout" error. If the queue gets full, then Gunicorn will start sending back errors for any overflowing requests.

There are some limitations to this setup, of course:

- Each additional worker eats up extra RAM (which can be reduced if you use [preload](https://docs.gunicorn.org/en/latest/settings.html#preload-app))
- Each additional worker/threads will eat some CPU when processing requests
- Each additional worker/thread will eat some extra CPU when listening to new requests, ie. the "[thundering herd problem](https://docs.gunicorn.org/en/latest/faq.html#does-gunicorn-suffer-from-the-thundering-herd-problem)", which is described in great detail [here](https://rachelbythebay.com/w/2020/03/07/costly/)

So, really, the question of "how much concurrency can Django handle" is really a question of "how much RAM can you afford"? 

Due to fixed RAM to CPU ratio of cloud virtual machines and 


Of course at some point


- TODO: AUTOSCALING


You may be wondering: how do you know how many workers and threads to run? The answer to this will depend on:

- How much RAM your machine has
- How many CPU cores are available
- Are your requests CPU or IO bound?

First of all, each new worker process eats up some more RAM, so at some point your machine's RAM will limit the number of workers. You can save a little RAM using [preload](https://docs.gunicorn.org/en/latest/settings.html#preload-app). Next there's the number of CPUs. If you have 100 worker processes and only one CPU core, then they will spend all of their time fighting to execute code on the CPU, which is wasteful overhead. You need to scale the number of workers to the number of CPU cores to avoid this overhead. The [Gunicorn docs](https://docs.gunicorn.org/en/latest/design.html#how-many-workers) recommend using the rule of thumb `(2 x $num_cores) + 1`.

Next you'll need to decide how many threads per worker you're going to use. Because we're using "green threads", the number of threads you decide to use depends on what your web app is doing. If your app is primarly doing a lot of CPU-intensive work like manipulating strings and crunching numbers then your code will be "CPU bound", meaning more threads aren't going to improve performace. On the other hand, if your app is spending most of its time waiting for the results of database queries, API requests and reading files, then it is "I/O bound" and would benefit from more threads per worker. Generally I think most Django apps are I/O bound - they spend most of their time waiting for database queries, and a little bit of time building HTML templates and JSON strings. So why not have 10000 threads per worker? Well, running too many threads (or workers) can result in the .

Finally, you should test out your app with locust.

You can read more on how to configure Gunicorn to use more workers/threads [here](https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7), and an interesting case study on optimising Gunicorn for [arxiv-vanity.com](https://www.arxiv-vanity.com/) [here](https://medium.com/@bfirsh/squeezing-every-drop-of-performance-out-of-a-django-app-on-heroku-4b5b1e5a3d44).


- the cost is just too high??? that's when Django doesn't have enough concurrency
- maybe you hit some other limitations like database conntections (pooling)

# FIXME throughput and response time.



## The other kind of "performance"

- the other kind of performance
- web dev performance
- cost of infra vs cost of extra developers
- const of maintainability of code (raw assembly?)
- do we optimise the shit out of this or change languages?

## Next steps

You're worried
