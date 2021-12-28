Title: My (free) Django monitoring stack for 2021
Description: The free tools I use to keep an eye on my Django apps
Slug: django-monitoring-stack
Date: 2021-12-28 12:00
Category: Django

You've built and deployed a website with Django. Congrats!
After that initial high of successfully launching your site comes the grubby work of fixing bugs. There are so many things that can go wrong.
Pages crash with 500 errors in prod but not locally. Pages load too slowly. Some offline tasks never finish. The site becomes [mysteriously unresponsive](https://twitter.com/mattdsegal/status/1473462877772136448). This one pain-in-the-ass user keeps complaining that file uploads "don't work"
but refuses to elaborate further: "they just don't work okay!?!". If enough issues crop up and you aren't able to solve them quickly and decisively, then you will lose the precious trust of your coworkers or clients.

Imagine that you find out about bugs or outages _as they happen_. You proactively tell your users that the site is down, not the other way around. You can quickly reproduce problems locally and have a fix up in prod in a matter of hours. Sounds good right? You're going to need a good monitoring stack to achieve this dream state of omniscient hyper-competence.

You'll need a few different (free) tools to get a holistic picture of what your app is doing:

- **Uptime monitoring**: tells you when the site is down ([StatusCake](https://www.statuscake.com/))
- **Error alerting**: tells you when an application error occurs, collects details ([Sentry](https://sentry.io/welcome/))
- **Log aggregation**: allows you to read about what happened on your servers ([Sumologic](https://www.sumologic.com/))
- **Performance**: tells you how long requests took, what's fast, what's slow ([Sentry](tps://sentry.io/welcome/), [New Relic](https://newrelic.com/products/application-monitoring))

In the rest of this post I'll talk about these SaaS tools in more detail, why I like to use the ones linked above, and finish with a few examples of how you can use them together to solve problems.

## Uptime monitoring

tells you when the site is down ([StatusCake](https://www.statuscake.com/))

## Error alerting

tells you when an application error occurs, collects details ([Sentry](https://sentry.io/welcome/))
https://mattsegal.dev/sentry-for-django-error-monitoring.html

## Log aggregation

allows you to read about what happened on your servers ([Sumologic](https://www.sumologic.com/))

https://mattsegal.dev/django-logging-papertrail.html
https://mattsegal.dev/django-gunicorn-nginx-logging.html
https://mattsegal.dev/file-logging-django.html

## Performance montioring

tells you how long requests took, what's fast, what's slow ([Sentry](tps://sentry.io/welcome/), [New Relic](https://newrelic.com/products/application-monitoring))
https://newrelic.com/products/application-monitoring

new relic apm great for complicated cases

## Examples

- was it an error?
- did the request hit nginx?
- did the task start or finish?

## Conclusion

words
