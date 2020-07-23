Title: Is Django too slow?
Description: A discussion of Django's performance
Slug: is-django-too-slow
Date: 2020-7-24 12:00
Category: Django

Does Django have "bad performance"?
The framework is now is 15 years old. Is it out of date?
I mean, [look at these benchmarks](https://medium.com/@mihaigeorge.c/web-rest-api-benchmark-on-a-real-life-application-ebb743a5d7a3): NodeJS/Express is consistently getting better numbers than Django.

If you are learning Django in 2020 then you might be worried that you're wasting time with an inferior technology.
In this post I'll explore web application performance and try to convince you that Django's performance is perfectly fine for most use-cases.

## Benchmarks

Let's start by digging into the ad-hoc web app performance benchmarks that you'll see pop up on Medium from time to time. To produce a graph like the one below, the author of [this article](https://medium.com/@mihaigeorge.c/web-rest-api-benchmark-on-a-real-life-application-ebb743a5d7a3) sets up a server for each of the frameworks tested and sends them a bunch of HTTP requests. The benchmarking tool counts number of requests served per second by each framework.

![benchmark]({attach}img/benchmark.png)

These results are interesting in the same way that it's interesting that a man once ate [73 hotdogs in 10 minutes](https://nathansfamous.com/the-stand/hdec-fun-facts/). "Huh, cool... I guess" sums up my reaction. Why do I find these numbers so underwhelming? It's because they're irrelevant to practical web development. PHP Laravel, the worst performing framework on this chart still served **76 requests per second** on a $5/month webserver. With baseline numbers like that, what does it matter if NodeJS served 3000 requests per second? It's like saying some guy ate 200 hotdogs in 10 minutes instead of 73. Yeah, I get it, it's a lot of hotdogs: _who cares_? Given that this kind of test is a little silly, what kind of performance metrics should you pay attention to when working on your Django app?

## What do you mean by "performance"?

When you ask whether a framework or language is "slow", you should also ask "slow at what?" and "why do you care?".
Fundamentally I think there are really only two performance goals: a good user experience and low hosting cost. How much money does running this website cost me, and do people enjoy using my website? For user experience I'm going to talk about two factors:

- Response time: how long people need to wait before their requests are fulfilled
- Concurrency: how many people can use your website at the same time

Cost, on the other hand, is typically proportional to compute resources: how many CPU cores and GB of RAM you will need to run your web app.

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
I've written previously on how to [find and fix slow database queries with Django Debug Toolbar](https://mattsegal.dev/django-debug-toolbar-performance.html) and how to [push slow API calls into offline tasks](https://mattsegal.dev/offline-tasks.html). There are **many** other ways to make your Django web pages or API endpoints load slowly, but if you avoid these two major pitfalls then you should be able to serve users with a time to first byte (TTFB) of 1000ms or less and provide a reasonable user experience.

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
If you are using Django to serve an API, where it is primarily computer programs talking to other computer programs, then it _may_ not be fast enough.
Some applications where you would consider ditching Django to shave off some latency are:

- a stock trading marketplace
- an global online advertisement serving network
- a low level infrastructure control API

If you find yourself sweating about an extra 100ms here or there, then maybe it's time to look at alternative web frameworks or languages. If the difference between a 600ms and 500ms TTFB doesn't mean much to you, then Django is totally fine.

## Concurrency in Django

As we saw in the benchmark above, Django web apps can handle multiple requests at the same time. This is important if your application has multiple users. If too many people try to use your site at the same time, then it will eventually become overwhelmed, and they will be served errors or timeouts. In Australia, our government's household census website was [famously overwhelmed](https://www.abc.net.au/news/2016-08-09/abs-website-inaccessible-on-census-night/7711652) when the entire country tried to access an online form in 2016. This effect is often called the "[hug of death](https://en.wikipedia.org/wiki/Slashdot_effect)" and associated with small sites becoming popular on Reddit or Hacker News.

A Django app's [WSGI server](https://mattsegal.dev/simple-django-deployment-2.html#wsgi) is the thing that handles multiple concurrent requests. I'm going to use [Gunicorn](https://gunicorn.org/), the WGSI server I know best, as a reference. Gunicorn can provide two kinds of concurrency: multiple child worker processes and multiple green threads per worker. If you don't know what a "process" or a "green thread" is then, whatever, suffice to say that you can set Gunicorn up to handle multiple requests at the same time. 

What happens if a new request comes in and all the workers/threads are busy? I'm a little fuzzy on this, but I believe these extra requests get put in a queue, which is managed by Gunicorn. It appears that the [default length](https://docs.gunicorn.org/en/stable/settings.html#backlog) of this queue is 2048 requests. So if the workers get overwhelmed, then the extra requests get put on the queue so that the workers can (hopefully) process them later. Typically NGINX will timeout any connections that have not received a response in 60s or less, so if a request gets put in the queue and does't get responded to in 60s, then the user will get a HTTP 504 "Gateway Timeout" error. If the queue gets full, then Gunicorn will start sending back errors for any overflowing requests.

It's interesting to note the relationship between request throughput and response time. If your WSGI server has 10 workers
and each request takes 1000ms to complete, then you can only serve ~10 requests per second. If you optimise your Django code so that each request only takes
100ms to complete, then you can serve ~100 requests per second. Given this relationship, it's sometimes good to improve your app's response time even if users won't notice, because it will also improve the number of requests/second that you can serve.

There are some limitations to adding more Gunicorn workers, of course:

- Each additional worker eats up some RAM (which can be reduced if you use [preload](https://docs.gunicorn.org/en/latest/settings.html#preload-app))
- Each additional worker/thread will eat some CPU when processing requests
- Each additional worker/thread will eat some extra CPU when listening to new requests, ie. the "[thundering herd problem](https://docs.gunicorn.org/en/latest/faq.html#does-gunicorn-suffer-from-the-thundering-herd-problem)", which is described in great detail [here](https://rachelbythebay.com/w/2020/03/07/costly/)

So, really, the question of "how much concurrency can Django handle" is actually a question of "how much cloud compute can you afford":

- if you need to handle more requests, add more workers
- if you need more RAM, rent a virtual machine with more RAM
- if you have too many workers one server and are seeing "thundering herd" problems, then [scale out your web servers](https://mattsegal.dev/django-prod-architecture/nginx-2-external.png) ([more here](https://mattsegal.dev/django-prod-architectures.html))

This situation is, admittedly, not ideal, and it would be better if Gunicorn were more resource efficient. To be fair, though, this problem of scaling
Django's concurrency doesn't really come up for most developers. If you're working at [Instagram](https://instagram-engineering.com/) or [Eventbrite](https://www.eventbrite.com/engineering/our-strategy-to-migrate-to-django/), then sure, this is costing your company some serious money, but most developers don't run apps that operate at a scale where this is an issue.

How do you know if you can support enough concurrency with your current infrastructure? I recommend using [Locust](https://locust.io/) to load test your app
with dozens, hundreds, or thousands of simultaneous users - whatever you think a realistic "bad case" scenario would look like. Ideally you would do this on a staging server that has a similar architecture and compute resources to your production enviroment. If your server becomes overwhelmed with requests and starts returning
errors or timeouts, then you know you have concurrency issues. If all requests are gracefully served, then you're OK!

What if the traffic to your site is very "bursty" though, with large transient peaks, or you're afraid that you'll get the dreaded "hug of death"? 
In that case I recommend looking into "[autoscaling](https://en.wikipedia.org/wiki/Autoscaling)" your servers, based on a metric like CPU usage.


If you're interested, you can read more on Gunicorn [worker selection](https://docs.gunicorn.org/en/latest/design.html#how-many-workers) and how to configure Gunicorn to [use more workers/threads](https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7). There's also [this interesting case study](https://medium.com/@bfirsh/squeezing-every-drop-of-performance-out-of-a-django-app-on-heroku-4b5b1e5a3d44) on optimising Gunicorn for [arxiv-vanity.com](https://www.arxiv-vanity.com/).

## When is Django's concurrency not enough?

You will have hit the wall when you run out of money, or you can't move your app to a bigger server, or distribute it across more servers.
If you've twiddled all the available setings and still can't get your app to handle all the incoming requests without sending back errors or 
burning through giant piles of cash, then maybe Django isn't the right backend framework for your applciation.

## The other kind of "performance"

There's one more aspect of performance to consider: your performance as a developer. Call it your [takt time](https://en.wikipedia.org/wiki/Takt_time), if you like metrics. Your ability to quickly and easily fix bugs and ship new features is valuable to both you and your users.
Improvements to the speed or thoroughput of your web app that also makes your code harder to work with may not be worth it.
Cost savings on infrastructure might be a waste if the change makes you less productive and costs you your time.

Choosing languages, frameworks and optimisations is an engineering decision, and in all engineering decisions there are competing tradeoffs to be considered, at least at the [Pareto frontier](https://en.wikipedia.org/wiki/Pareto_efficiency).

If raw performance was all we cared about, we'd just write all our web apps in raw assembly.

![web development in assembly]({attach}/img/assembly.webp)


## Next steps

If you liked reading about running Django in production, then you might also enjoy another post I wrote, which gives you a tour of some common [Django production architectures](https://mattsegal.dev/django-prod-architectures.html). If you've written a Django app and you're looking to deploy it to production, then
you might enjoy my guide on [Django deployment](https://mattsegal.dev/simple-django-deployment.html).

