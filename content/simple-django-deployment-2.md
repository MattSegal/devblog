Title: Simple Django Deployments part two: local setup
Description: How to make sure Django is working before you deploy it
Slug: simple-django-deployment-2
Date: 2020-04-19 14:00
Category: Django

# Prepare and test Django locally

So we've set up our server, now let's get out Django app working

- warn about line endings
- show how to change line endings in VScode

- create a Django app locally - link to github
- add model, view
- create migrations, save
- point out sqlite database (we will use in prod)
- SQLite limitations?
- get it working with runserver
- ensure you have requirements.txt
- set up in virtualenv
- install whitenoise
- add prod-specific settings

  - debug = False
  - allowed hosts = localhost, IP address
  - secret key = os.environ
  - ??? what else ??? check Django deploy guide

- install gunicorn
- add bash script to run gunicorn
- creat envar file
- set secret key envar
- set django settings envar
- test prod settings using gunicorn locally

[Deploy Django to the server]({filename}/simple-django-deployment-3.md)
