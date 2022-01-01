Title: My (free) Django monitoring stack for 2021
Description: The free tools I use to keep an eye on my Django apps
Slug: django-monitoring-stack
Date: 2022-01-01 12:00
Category: Django

You've built and deployed a website using Django. Congrats!
After that initial high of successfully launching your site comes the grubby work of fixing bugs. There are so many things that <s>can</s> will go wrong.
Pages may crash with 500 errors in prod, but not locally. Some offline tasks never finish. The site becomes [mysteriously unresponsive](https://twitter.com/mattdsegal/status/1473462877772136448). This one pain-in-the-ass user keeps complaining that file uploads "don't work"
but refuses to elaborate further: "they just don't work okay!?!".

If enough issues crop up and you aren't able to solve them quickly and decisively, then you will lose the precious trust of your coworkers or clients. Often reputational damage isn't caused by the bug itself, but by the perception that you have no idea what's going on.

Imagine that you are able to find out about bugs or outages _as they happen_. You proactively warn your users that the site is down, not the other way around. You can quickly reproduce problems locally and push a fix to prod in a matter of hours. Sounds good right? You're going to need a good "monitoring stack" to achieve this dream state of omniscient hyper-competence.

You'll need a few different (free) tools to get a holistic picture of what your Django app is doing:

- **Uptime monitoring**: tells you when the site is down ([StatusCake](https://www.statuscake.com/))
- **Error reporting**: tells you when an application error occurs, collects details ([Sentry](https://sentry.io/welcome/))
- **Log aggregation**: allows you to read about what happened on your servers ([Sumologic](https://www.sumologic.com/))
- **Performance**: tells you how long requests took, what's fast, what's slow ([Sentry](tps://sentry.io/welcome/), [New Relic](https://newrelic.com/products/application-monitoring))

In the rest of this post I'll talk about these SaaS tools in more detail, why I like to use the ones linked above, and finish with a few examples of how you can use them together to solve problems.

## Uptime monitoring

It's quite embarrasing when your site goes down, but what's more embarrasing is when you learn about it from _someone else_. An uptime monitoring service can help: it sends a request to your site every few minutes and pings you (Slack, email) when it's unresponsive. This allows you to quickly get your site back online, hopefully before anyone notices. If you want to get fancy you can build a health check route (eg. `/health-check/`) into your Django app which, for example, checks that the database, or cache, or whatever are still online as well.

Another benefit of uptime monitoring is that you'll get a clear picture of when the outage started. For example, in the picture below you can see that a website of mine stopped responding to requests between ~21:00 and ~23:30 UTC. You can use this knowledge of exactly _when_ the site become unresponsive to check other sources of information, such as server logs or error reports for clues.

![downtime]({attach}/img/downtime.png)

I like to use [StatusCake](https://www.statuscake.com/) for this function because it's free, simple and easy to set up.

## Error reporting

There are lots of ways for your site to break that don't render it completely unresponsive. A user might click a button to submit a form and receive a 500 error page because you made some trivial coding mistake that wasn't caught by your [automated testing pipeline](https://mattsegal.dev/pytest-on-github-actions.html). This user comes to you and complains that "the site is broken". Sometimes they will provide you with a very detailed explanation of what they did to produce the error, which you can use to replicate the issue, but as often as not they may, infuriated by your shitty website and seemingly antagonistic line of questioning, follow up with "iTs JuST brOken OKAY!?". Wouldn't it be nice to get the detailed information that you need to fix the bug without having to talk to a human?

This is where error reporting comes in. When your Django web app catches some kind of exception, then an error reporting library can inspect the error and send the details to a SaaS service which records it for you. These error reporting tools capture heaps of useful information, such as:

- When the error happened first and most recently
- The exception type and message
- Which line of code triggered the error
- The stack trace of the error
- The value of local variables in each frame of the stack trace
- The Python version, package versions, user browser, IP, etc etc etc.

This rich source of information makes error reporting a vital tool. It really shines when you encounter errors that _only_ happen in production, where you have no idea how to replicate them locally. [Sentry](https://sentry.io/welcome/) is great for this task because it's free, easy to set up and has a great web UI. You can set up Sentry to send you error alerts via Slack and/or email.

## Log aggregation

Production errors can be more complicated than a simple Python exception crashing a page. Sometimes, much more complicated. If you want to get a feel for the twisted shit computers will get up to then give [Rachel by the Bay](https://rachelbythebay.com/w/) a read. To solve the trickier issues in production you're going to need to reconstruct what actually happened at the time of the error. You'll need to draw upon multiple sources of information, such as:

- application logs (eg. [Django logs](https://mattsegal.dev/file-logging-django.html))
- webserver logs (eg. [NGINX, Gunicorn logs](https://mattsegal.dev/django-gunicorn-nginx-logging.html))
- logs from other services (eg. Postgres, syslog, etc)

You can `ssh` into your server and read these logs from the command line using `less` or `grep` or `awk` or something. Even so, it's much more convenient to access these logs via a log aggregation service's web UI, where you can run search queries to quickly find the log lines of interest. These tools work by running a "logging agent" on your server, which watches files of interest and sends them to a centralised server.

![logging]({attach}/img/logging.png)

This model is paritcularly valuable if you have transient infrastructure (servers that don't last forever) or if you have many different servers, or if you want to limit `ssh` access for security reasons.

[Sumologic](https://www.sumologic.com/) if my favourite free SaaS for this task because it's easy to install the logging agent and add new files to be watched. The search is pretty good as well. The main downside is that web UI can be a little complicated and overwhelming at times. The search DSL is very powerful but I always need to look up the syntax. Log retention times seem reasonable, 30 days by default. The Sumologic agent seems to consume several hundred MB of RAM (~300MB?).

[Papertrail](https://www.papertrail.com/) is, in my opinion, worse than Sumologic in every way I can think of. However, it is also free and presents a simple web UI for viewing and searching your logs. If you're interested I wrote about setting up Papertrail [here](https://mattsegal.dev/django-logging-papertrail.html). [New Relic](https://docs.newrelic.com/docs/logs/get-started/get-started-log-management/) offer a logging service as well - never tried it though. There are open source logging solutions like [Elasticsearch](https://www.elastic.co/) + Kibana and other alternatives, but they come with the downside of having to run them yourself: "now you have two problems".

## Performance montioring

Sometimes your website isn't broken per-se, but it's too slow. People hate slow websites. You can often diagnose and fix these issues locally using tools like [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) (I made a video on how to do this [here](https://mattsegal.dev/django-debug-toolbar-performance.html)), but sometimes the slowness only happens in production. Furthermore, riffing on the general theme of this article, you want to know about (and fix) slow pages before your boss walks over to your desk and complains about it.

Performance monitoring tools instrument your Django web app and record information about how long various requests take. What's fast? What's slow? Which pages have problems? I recommend that you start out by using [Sentry](https://sentry.io/welcome/) for this task because their performance monitoring service comes bundled with their error reporting by default. It's kind of basic, but maybe that's all you need.

The best appilcation performance monitoring for Django that I know of is [New Relic's offering](https://newrelic.com/products/application-monitoring), which seems to have a free tier. The request traces that they track include a very detailed breakdown of _where_ the time was spent in serving a request. For example, it will tell you how much time was spent querying the database, or a cache, or building HTML templates. Sometimes you need that level of detail to solve tricky performance issues. The downside of using New Relic is that you have to reconfigure your app server to boot using their [agent](https://docs.newrelic.com/docs/apm/agents/python-agent/) as a wrapper.

Although it's not strictly on-topic, [PageSpeed Insights](https://pagespeed.web.dev/) is pretty useful for checking page load performance from a front-end perspective. If you're interested in more on Django web app performance then you might like this post I wrote, where I ponder: [is Django too slow?](https://mattsegal.dev/is-django-too-slow.html)

## Conclusion

This list is not exhaustive or definitive, it's just the free-tier tools that I like to use for my freelance and personal projects.
Nevertheless I hope you find them useful.
It can be a pain to integrate them all into your app, but over the long run they'll save you a lot of time and energy.

Be prepared!
