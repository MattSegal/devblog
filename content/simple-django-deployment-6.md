Title: Simple Django Deployments part five: domain setup
Description: Setup your Django app's domain name
Slug: simple-django-deployment-6
Date: 2020-04-19 18:00
Category: Django

Here we will learn how to:

- Buy a domain name
- Set up a Cloudflare reverse-proxy
- Add our domain name to Django prod settings
- Test our setup

We'd usually do this early \$EXPLAIN_WHY

### Buy a domain name

- motivate why we want one
- link to DNS guide
- present interface with diagram
- suggest search "site:reddit.com best domain seller"
- suggest namecheap
- suggest .xyz for cheapskates
- ???
- take stock

### Set up Cloudflare

- motivate why we need cloudflare
- link to Cloudflare review
- explain why you want to do DNS stuff early
- get droplet IP and put it into cloudflare
- ensure caching, compression
- set A record with proxing via Cloudflare (NGINX)
- test A record with dig or DNS checker
- take stock
- wait a while...

### Testing our setup

- run http.server on server
- check locally
- check the IP address
- check the domain name
- start Django

# Next steps

- Add logging
- start using git for deployments
- Try out Celery or Django-Q for offline tasks
- Try using Postgres
- Try out using NGINX
- Try out media hosting in S3
- Try out ???
- Automate deployment with GitHub actions
- Add automated unit tests

[xxxx]({filename}/file-logging-django.md)
[xxxx]({filename}/intro-config-management.md)
[xxxx]({filename}/simple-offline-tasks-django-q.md)
[xxxx]({filename}/sentry-for-django-error-monitoring.md)
