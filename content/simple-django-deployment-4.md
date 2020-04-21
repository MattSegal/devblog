Title: Simple Django Deployments part four: run a service
Description: How to get gunicorn to run in the background
Slug: simple-django-deployment-4
Date: 2020-04-19 16:00
Category: Django

# Make it a service, run as a service

- you might have noticed that running Django only works when you have a terminal session
- get it to run in the background
- set up supervisord
- run as service (as root)
- we don't want to run as root (why?)
- create gunicorn user
- give user file permissions over /app/ chown -R
- change supervisord to run as gunicorn or something?

[Script the deployment]({filename}/simple-django-deployment-5.md)
