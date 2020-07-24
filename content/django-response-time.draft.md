### Too many database queries
https://www.reddit.com/r/django/comments/hv5yrj/how_well_can_django_scale/


- N+1 queries - fix
- too many database queries
- write regression tests to count number of database calls
- cache expensive queries
- bulk write

see https://docs.djangoproject.com/en/3.0/topics/db/optimization/

### External API calls

- 3rd party API calls in views
- cache results
- push long running tasks offline

### Search

- can get slow
- use Postgres search
- use Elasticsearch

### Too much data

- query from DB
- push over wire
- fetching too much data (pagination)

### Web assets

- assets minified
- gzipped
- images too large
- images + static slow to load (CDN)

### What else?

- too many cache hits (they add up!)
- slow processing in memory (It's usually never python... but)

### How to test your Django app's performance

- newrelic, datadog
- Django Debug Toolbar
- database query logging
- https://developers.google.com/web/tools/lighthouse
- just try it out