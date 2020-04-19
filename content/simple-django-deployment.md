Title: UNTUITLDE
Slug: simplest-django-deploument
Date: 2020-04-19 12:00
Category: Django

PAIN

- you are a beginner coder
- you have a Django project working on your computer
- you want to put it on the internet
- your main focus is learning, but you want to see results... sometime this week
- if you don't care about learning to _how_ deploy, just use Heroku or PythonAnywhere, this guide is going to assume that you do

- I've noticed most Django deployment guides can be pretty rough on beginners
- there are a lot of moving pieces in a Django deployment

  - guides show you gunicorn + postgres + nginx + .... Docker?
  - it's hard doing something new, it's really hard to learn 10 new things at once
  - you know you're not supposed to just use runserver - why?
  - you want to learn to _do it right_
  - what does _right_ mean anyway?
  - one step at a time
  - my goal is to show you how to deploy something _reasonable_ with as few new technologies as possible

Call out DigitalOcean and reddit

- Do you _need_ to set up a reverse proxy like NGINX? No!
- Do you _need_ to set up a database like Postgres / MySQL? No!
- Do you _need_ Docker? No!

* sometimes you want to just get started and have something working, not fiddle around with 10 different new technologies
* what's the simplest Django deployment that we can get away with?

I imagine you already have set up a local Django website with SQLite as the database, following the Django tutorial or something similar and run it using `./manage.py runserver`.
I'm going to assume that you're using Windows, because most people do.

Here are the new technologies that I propose we use:

- A Linux virtual machine in the cloud for hosting (DigitalOcean)
- SSH and SCP for accesing the server
- Gunicorn and XXXXXXX for running your app
- Whitenoise to server static files
- Cloudflare for DNS, static file caching, SSL

We will not be using

- NGINX
- Postgres or MySQL
- Docker

I've tried to keep this guide as simple as possible while also keeping it mostly production ready.
I also aim to make it easy to debug production problems locally.

Once you've got this deployment done you can mix it up later, you can add NGINX, Postgres and Docker if you like,
you can experiment with different technologies.

=== INTRO VIDEO ===

UPSIDES

- mostly testable locally
- minimal new technologies, harder to fuck up
- can always extend later

DOWNSIDES

- sqlite has limitations
- not using NGINX has limitations

Steps in guide

- Non-Django infrastructure

### Non Django Infrastructure

This stuff is the most painful and we want to get this right first
before we involve

- create a DO droplet
- buy a domain name
- set up cloudflare (link to cloudflare)
- get droplet IP and put it into cloudflare
- ensure caching, compression
- set A record with proxing via Cloudflare (NGINX)
- test A record with dig or DNS checker
- wait a while...

- quick tools aside ConEmu for Windows
- also show how to access git bash via conemu

- Make sure you have bash or git-bash
- Fuck putty
- intro to git-bash, how to get it, where to run
- check for ssh, scp
- create an ssh key
- add it to the server
- ssh into the server
- copy a file onto the server

- create a HTML file locally
- run http.server using Python 3 locally
- check it in your browser

- copy HTML file onto server
- ssh in
- cat it to view
- run http.server on server
- check the IP address
- check the domain name

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

# Deploy Django to server

- WINDOWS LINE ENDINGS
- copy source code to server
- set up virtualenv
- collectstatic, run migrations
- run prod settings on server
- test locally with curl
- test IP address
- test DNS
- you're in!

# Make it a service, run as a service

- you might have noticed that running Django only works when you have a terminal session
- get it to run in the background
- set up supervisord
- run as service

# Script the deployment

- automate the process
- push it into github actions
- show pushing code changes to prod

# Next steps

- Start using Postgres
- Try out using NGINX
- Try out Celery or Django-Q
- Try out media hosting in S3
- Try out ???
- Automate deployment with GitHub actions
- Add automated unit tests
