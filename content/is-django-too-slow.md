Title: Is Django too slow?
Description: A discussion of Django's performance
Slug: is-django-too-slow
Date: 2020-7-17 12:00
Category: Django

Does Django have "bad performance"?
The framework is now is 15 years old, is it out of date?
I mean, [look at these benchmarks](https://medium.com/@mihaigeorge.c/web-rest-api-benchmark-on-a-real-life-application-ebb743a5d7a3): the NodeJS-based Express framework is consistently getting better numbers than Django. It's not just NodeJS. Web apps written in Go have way better performance than those written in Python, so why bother learning Python?

If you are learning Django in 2020 you might be worried that you're wasting time learning about an inferior technology.
In this post I'll explore web application performance and try to convince you that Django's performance is perfectly fine.

## Benchmarks

Let's start by digging into the ad-hoc web app performance benchmarks that you'll see pop up on Medium from time to time. To produce a graph like the one below, the author of [this article](https://medium.com/@mihaigeorge.c/web-rest-api-benchmark-on-a-real-life-application-ebb743a5d7a3) sets up a server for each of the frameworks tested and spams them with a bunch of HTTP requests. The benchmarking tool counts number of requests served per second by each framework.

![benchmark]({attach}img/benchmark.png)

These results are interesting in the same way that it's interesting that a man once ate [73 hotdogs in 10 minutes](https://nathansfamous.com/the-stand/hdec-fun-facts/). "Huh, cool... I guess" sums up my reaction. Why do I find these numbers so underwhelming? It's because they're irrelevant to practical web development. PHP Laravel, the worst performing framework on this chart still served **76 requests per second** on a $5/month webserver. With baseline numbers like that, what does it matter if NodeJS served 3000 requests per second? It's like saying some guy ate 200 hotdogs in 10 minutes instead of 73. Yeah, I get it, it's a lot of hotdogs: _who cares_?

So what kind of performance metrics should you pay attention to when working on your Django app? Let's get into that next. 

## So, what is "performance" exactly?

When you ask whether a framework or language is "slow", you have to ask "slow at what?" and "why do you care?".
Fundamentally I think there are really only two performance goals you care about: a good user experience and low hosting cost. How much money does running this website cost me, and do people enjoy using my website? For user experience I'm going to talk about two factors:

- Concurrency: how many people can use your website at the same time
- Response time: how long people need to wait before their request is fulfilled

Cost, on the other hand, is typically proportional to compute resources: how many CPU cores and GB of RAM you will need to run your webapp.

## Response time in Django

Users don't like waiting for their page to load, so the less time they have to wait, the better. There are a few different
metrics that you could use to measure page load speed, such as [time to first byte](https://web.dev/time-to-first-byte/) or [first contentful paint](https://web.dev/first-contentful-paint/), both of which you can check with [PageSpeed Insights](https://developers.google.com/speed/pagespeed/insights/).

Faster responses don't benefit your user linearly though, not every 5x speedup is equally beneficial:

- A user getting a response in 5s compared to 25s transforms the app from "broken" to "barely useable"
- 1s compared to 5s is a huge improvement
- 200ms instead of 1s is great
- 50ms instead of 200ms is nice, I guess, but many people wouldn't notice
- 10ms instead of 50ms is imperceptible, no one can tell the difference

So if someone says "this framework is 5x faster than that framework blah blah blah" it really doesn't mean anything without more context.

# FIXME
The sub-10ms page load times is useful for throughput -- latency can improve concurrency.


So, what makes a page load slowly in Django?

### Too many database queries

  - N+1 queries - fix
  - too many database queries
  - write regression tests to count number of database calls
  - cache expensive queries

### External API calls

- 3rd party API calls in views
- cache results
- push long running tasks offline

### What else?

  - fetching too much data (pagination)
  - images + static slow to load (CDN)
  - too many cache hits (they add up!)
  - slow processing in memory (It's usually never python... but)


### How to test your Django app's performance

  - newrelic, datadog
  - Django Debug Toolbar
  - database query logging
  - https://developers.google.com/web/tools/lighthouse
  - just try it out

## Concurrency in Django

As we saw in the benchmark above, Django web apps can handle multiple requests at the same time. This is important if your application has many users on your website at the same time. Multiple concurrent requests are handled by the WSGI server which runs the Django app in production. If too many users try to use your site at the same time, then it will eventually become overwhelmed, and users will receiving errors or timeouts. I'm going to use [Gunicorn](https://gunicorn.org/), a commonly used WGSI server, as a reference. Gunicorn can provide two kinds of concurrency: multiple workers or multiple threads.


A Gunicorn server runs a master process with multiple child "worker" processes. Each child process has its own thread(s) of execution. So a Gunicorn WSGI app can run, for example, five workers, which can together process at least 5 requests using your Django code at the same time. Each worker will passively eat up some RAM and will require access to a CPU core when serving requests.

Each worker process can also have multiple threads, meaning one worker can handle multiple requests the same time. Eg. 5 workers with 2 threads each could process up to 10 requests at the same time. The key thing to know is that Gunicorn threads are "[green threads](https://en.wikipedia.org/wiki/Green_threads)", meaning that all the threads on a single worker have to share access to one CPU core. This means 

But then what happens if a new request comes in and all the worker threads are busy? I'm a little fuzzy on this, but I believe these extra requests get put in a queue, which is managed by Gunicorn. It appears that the [default length](https://docs.gunicorn.org/en/stable/settings.html#backlog) of this queue is 2048 requests. So if the workers get overwhelmed, then the extra requests get put on the queue so that the workers can (hopefully) process them later. Typically NGINX will timeout any connections that have not received a response in 60s or less, so if a request gets put in the queue and does't get responded to in 60s, then the user will get a HTTP 504 "Gateway Timeout" error. If the queue gets full, then Gunicorn will start sending back errors for any overflowing requests.

 You may be wondering: how do you know how many workers and threads to run? The answer to this will depend on:

- How much RAM your machine has
- How many CPU cores are available
- Are your requests CPU or IO bound?

First of all, each new worker process eats up some more RAM, so at some point your machine's RAM will limit the number of workers. You can save a little RAM using [preload](https://docs.gunicorn.org/en/latest/settings.html#preload-app). Next there's the number of CPUs. If you have 100 worker processes and only one CPU core, then they will spend all of their time fighting to execute code on the CPU, which is wasteful overhead. You need to scale the number of workers to the number of CPU cores to avoid this overhead. The [Gunicorn docs](https://docs.gunicorn.org/en/latest/design.html#how-many-workers) recommend using the rule of thumb `(2 x $num_cores) + 1`.

Next you'll need to decide how many threads per worker you're going to use. Because we're using "green threads", the number of threads you decide to use depends on what your web app is doing. If your app is primarly doing a lot of CPU-intensive work like manipulating strings and crunching numbers then your code will be "CPU bound", meaning more threads aren't going to improve performace. On the other hand, if your app is spending most of its time waiting for the results of database queries, API requests and reading files, then it is "I/O bound" and would benefit from more threads per worker. Generally I think most Django apps are I/O bound - they spend most of their time waiting for database queries, and a little bit of time building HTML templates and JSON strings. So why not have 10000 threads per worker? Well, running too many threads (or workers) can result in the "[thundering herd problem](https://docs.gunicorn.org/en/latest/faq.html#does-gunicorn-suffer-from-the-thundering-herd-problem)", which is described in great detail [here](https://rachelbythebay.com/w/2020/03/07/costly/).

Finally, you should test out your app with locust.

You can read more on how to configure Gunicorn to use more workers/threads [here](https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7), and an interesting case study on optimising Gunicorn for [arxiv-vanity.com](https://www.arxiv-vanity.com/) [here](https://medium.com/@bfirsh/squeezing-every-drop-of-performance-out-of-a-django-app-on-heroku-4b5b1e5a3d44).


## Resource usage in Django

- aaa

## When is Django's performance not good enough?

- sub ms response times
- the cost is just too hight

https://rachelbythebay.com/w/2020/03/07/costly/

- when not to use Django

## The other kind of "performance"

- the other kind of performance

## Next steps

You're worried

