Title: Is Django too slow?
Description: A discussion of Django's performance
Slug: is-django-too-slow
Date: 2020-7-17 12:00
Category: Django

Is the Django web framework slow? Does it have "bad performance"?
The framework is now is 15 years old, is it out of date?
I mean, [look at these benchmarks](https://medium.com/@mihaigeorge.c/web-rest-api-benchmark-on-a-real-life-application-ebb743a5d7a3): the NodeJS-based Express framework is consistently getting better numbers than Django. Does that mean that Django is obsolete? Web apps written in Go have way better performance than those written in Python, so why bother learning Python?

If you are learning Django in 2020 you might be worried that you're wasting time learning about an inferior technology.
In this post I'll explore web application performance and try to convince you that Django's performance is perfectly fine.

## Benchmarks

Let's start by digging into these ad-hoc web app performance benchmarks. To produce a graph like the one below, the author of [this article](https://medium.com/@mihaigeorge.c/web-rest-api-benchmark-on-a-real-life-application-ebb743a5d7a3) sets up a server for each of the frameworks tested and spams them with a bunch of HTTP requests. The benchmarking tool counts number of requests served per second by each framework.

![benchmark]({attach}img/benchmark.png)

These results are interesting in the same way that it's interesting that a man once ate [73 hotdogs in 10 minutes](https://nathansfamous.com/the-stand/hdec-fun-facts/). "Huh, cool... I guess" sums up my reaction. Why do I find these numbers so underwhelming? It's because they're irrelevant to practical web development. PHP Laravel, the worst performing framework on this chart still served **76 requests per second** on a \$5/month webserver. With baseline numbers like that, what does it matter if NodeJS served 3000 requests per second? It's like saying some guy ate 200 hotdogs in 10 minutes instead of 73. Yeah, I get it, it's a lot of hotdogs: _who cares_?

Let's say you have a website where your crappy API can only serve a pitiful 30 requests per second before it starts throwing errors. Let's assume each user sends a request every 5 seconds, on average, clicking on links and paginating and such. How many concurrent users can your web app support? I [calculate](https://stattrek.com/online-calculator/binomial.aspx) that in a 24h period, if you have 60 people using your app at the same time, for the whole 24 hours, there's an 8% chance of 1+ seconds of failure, and a 0.03% chance of 2+ seconds of failure. That's a ~99.9976% success rate, serving ~100k requests per day. I think this is pretty good for most human-facing web applications.

You probably don't need your web app to serve 3000 requests per second. If you do, then you work at a company with a name staring with "G" and ending with "oogle" and you don't care about web framework performance because you [program with butterflies](https://xkcd.com/378/). In summary, the "performance" that this benchmark is measuring is _probably_ not a performance problem that you actually have. So what is web app performance then? Let's get into that next.

## What is "performance", exactly?

When it comes to web app performance I think there are really only two things you care about, user experience and cost. How much money does running this website cost me, and do people enjoy using my website? For user experience I'm going to talk about two factors:

- Concurrency: how many people can use your website at the same time
- Response time: how long people need to wait before their request is fulfilled

Cost, on the other hand, is typically related to how many CPU cores and GB of RAM you will need.

## Concurrency in Django

Django web apps can handle multiple requests at the same time. This feature is handled by the WSGI server which runs the Django app in production. I'm going to use [Gunicorn](https://gunicorn.org/), a commonly used WGSI server, to explain how this works.

A Gunicorn server runs a master process with multiple child "worker" processes. Each child process has its own thread(s) of execution. So a Gunicorn WSGI app can run, for example, five workers, which can together process at least 5 requests using your Django code at the same time. Each worker will passively eat up some RAM and will require access to a CPU core when serving requests.

Each worker process can also have multiple threads, meaning one worker can handle multiple requests the same time. Eg. 5 workers with 2 threads each could process up to 10 requests at the same time.

But then what happens if a new request comes in and all the worker threads are busy? I'm a little fuzzy on this, but I believe these extra requests get put in a queue, which is managed by Gunicorn. It appears that the [default length](https://docs.gunicorn.org/en/stable/settings.html#backlog) of this queue is 2048 requests. So if the workers get overwhelmed, then the extra requests get put on the queue so that the workers can (hopefully) process them later. Typically NGINX will timeout any connections that have not received a response in 60s or less, so if a request gets put in the queue and does't get responded to in 60s, then the user will get a HTTP 504 "Gateway Timeout" error. If the queue gets full, then Gunicorn will start sending back errors for any overflowing requests.

So if your you've 5 Gunicorn workers with 2 threads each, then you can process 10 requests at once, with any extras getting put in a queue, which will be serviced as soon as new workers become available. You may be wondering: how do you know how many workers and threads to run? The answer to this will depend on:

- How much RAM your machine has
- How many CPU cores are available
- Are your requests CPU or IO bound?

First of all, each new worker process eats up some more RAM, so at some point your machine's RAM will limit the number of workers. You can save a little RAM using [preload](https://docs.gunicorn.org/en/latest/settings.html#preload-app). Next there's the number of CPUs. If you have 100 worker processes and only one CPU core, then they will spend all of their time fighting to execute code on the CPU, which is wasteful overhead. You need to scale the number of workers to the number of CPU cores to avoid this overhead. The [Gunicorn docs](https://docs.gunicorn.org/en/latest/design.html#how-many-workers) recommend using the rule of thumb `(2 x $num_cores) + 1`.

Next you'll need to decide how many threads per worker you're going to use. The key thing to know is that Gunicorn threads are "[green threads](https://en.wikipedia.org/wiki/Green_threads)", meaning that all the threads on a single worker have to share access to one CPU core. Because we're using "green threads", the number of threads you decide to use depends on what your web app is doing. If your app is primarly doing a lot of CPU-intensive work like manipulating strings and crunching numbers then your code will be "CPU bound", meaning more threads aren't going to improve performace. On the other hand, if your app is spending most of its time waiting for the results of database queries, API requests and reading files, then it is "I/O bound" and would benefit from more threads per worker. Generally I think most Django apps are I/O bound - they spend most of their time waiting for database queries, and a little bit of time building HTML templates and JSON strings. So why not have 10000 threads per worker? Well, running too many threads (or workers) can result in the "[thundering herd problem](https://docs.gunicorn.org/en/latest/faq.html#does-gunicorn-suffer-from-the-thundering-herd-problem)", which is described in great detail [here](https://rachelbythebay.com/w/2020/03/07/costly/).

You can read more on how to configure Gunicorn to use more workers/threads [here](https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7), and an interesting case study on optimising Gunicorn for [arxiv-vanity.com](https://www.arxiv-vanity.com/) [here](https://medium.com/@bfirsh/squeezing-every-drop-of-performance-out-of-a-django-app-on-heroku-4b5b1e5a3d44).

## Response time in Django

- latency in Django

  - push long running tasks offline

When you ask whether a framework or language is "slow", you have to ask "slow at what?" and "why do you care?".
You really need to apply a utlity function to all of these "performance" improvements.
A user getting a response in 5s compared to 25s transforms the app from "broken" to "barely useable"
1s compared to 5s is a huge improvement
200ms instead of 1s is good
50ms instead of 200ms is nice, I guess, but many people wouldn't notice
10ms instead of 50ms is just wank, no one can tell the difference
So if someone says "this framework is 5x faster than that framework blah blah blah" it really doesn't mean anything without more context.

The sub-10ms page load times is useful for throughput -- latency can improve concurrency

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

- how to test your Django app's performance

  - newrelic
  - Django debug Toolbar
  - database query logging
  - locust
  - https://developers.google.com/web/tools/lighthouse
  - just try it out

- the most common things that will make your Django app slow
  - N+1 queries - fix
  - too many database queries
  - 3rd party API calls in views
  - too many cache hits
  - CDN

=== REPLIES ===

From the article

> Having in mind that in a real world application almost all the requests interact with the database,
> none of the choices are bad and all of them could handle the requirements of most web applications.

If you really want to know how your current Django app + infrastructure stands up to high load,
then use Locust to load test it. It's pretty simple to do and will give you an empirical look at how your app performs,
rather than speculating on how simplistic benchmarks. Once you find some weak endpoints then you can look into performance tuning.
Often there are easy wins where you can find and fix slow queries using with Django Debug Toolbar or database query logging.
