Title: Simple Django Deployments part three: deploy code
Description: How to get your Django code running on the server
Slug: simple-django-deployment-3
Date: 2020-04-19 15:00
Category: Django

# Deploy Django to server

/srv/app
/srv/env
/srv/static?

- create app folder /srv/app/
- copy source code to server
- WINDOWS LINE ENDINGS dos2unix?
- find pyc and delete
- only copy source code! not SQLite database (how?)
- find py files (print dir tree?)
- try run migrations to create database - see failure
- set up virtualenv
- install requirements
- activate env
- try run migrations - see failure
- change secret key envar in /etc/environment
- collectstatic, run migrations
- look for SQLite database
- look for staticfiles?????
- run gunicorn from same bash script
- run prod settings on server
- test locally with curl
- test IP address
- test DNS
- you're in!

[Run Django in the background]({filename}/simple-django-deployment-4.md)
