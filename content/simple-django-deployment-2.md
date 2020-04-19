Title: Simple Django Deployments part two: local setup
Description: How to make sure Django is working before you deploy it
Slug: simple-django-deployment-2
Date: 2020-04-19 14:00
Category: Django

# Prepare and test Django locally

- create a Django app locally
- add model, view
- create migrations, save
- get it working with runserver
- ensure you have requirements.txt
- set up in virtualenv
- install whitenoise
- add prod-specific settings
  - debug = False
  - allowed hosts
  - secret key
  - ??? what else ??? check Django deploy guide
- test prod settings using gunicorn locally
