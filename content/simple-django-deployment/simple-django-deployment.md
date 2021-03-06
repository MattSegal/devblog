Title: Simple Django deployment: a guide
Description: How to deploy Django in many small steps
Slug: simple-django-deployment
Date: 2020-04-26 12:00
Category: Django

You're learning web development with Django. You've followed the [official introductory tutorial](https://docs.djangoproject.com/en/3.0/intro/tutorial01/) and you can get a Django app working on your local computer. Now you want to put your web app onto the internet. Maybe it's to show your friends, or you actually want to use it for something, or maybe you just want to learn how to deploy Django apps. This guide has five parts:

1. [Server setup]({filename}/simple-django-deployment/simple-django-deployment-1.md)
2. [Prepare and test Django locally]({filename}/simple-django-deployment/simple-django-deployment-2.md)
3. [Deploy Django to the server]({filename}/simple-django-deployment/simple-django-deployment-3.md)
4. [Run Django in the background]({filename}/simple-django-deployment/simple-django-deployment-4.md)
5. [Automate the re-deployment]({filename}/simple-django-deployment/simple-django-deployment-5.md)
6. [Domain setup]({filename}/simple-django-deployment/simple-django-deployment-6.md)

You can start the guide with part 1 now. If you're interested, read on to learn more about what motivated me to write this.

### Stuck, frustrated, confused

You've probably tried [tutorials like this](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04) which give you a bunch of steps to follow, commands to type, files to configure. This is how I learned to deploy Python web apps: with online tutorials and a lot of Googling. When you follow these guides, you have no fucking idea what you're actually doing. Why do you use that tool? Why do you type that command? You may as well be [learning magic at Hogwarts](https://youtu.be/nAQBzjE-kvI?t=33). You could easily swap:

> What is apt? Why am I using it to install postgresql-contrib and libpq-dev?

with

> Why do I have to say Wingardium Levios*aaa* not Leviosa*rrr* to get my spell to work?

It's not your fault. These kinds of guide throw a lot of unfamilliar tools and concepts at you without taking the time to teach you about them. The DigitalOcean guide above smacks you with:

- apt package manager
- PostgreSQL installation
- PostgreSQL database admin
- Python virtual environments
- Prod Django settings
- Running a gunicorn WSGI server
- Firewall configurations
- Systemd configuration
- Socket file setup
- NGINX reverse proxy setup

It also requires that you know:

- How to spin up a new a web server
- How to login via SSH
- How to set DNS records
- How to get your Django code onto the server

Some of these tools and skills are necessary, some of them are not. If you don't follow their instructions perfectly then you can get stuck and have no idea how to get unstuck. Then you get frustrated, discouraged and embarrassed that you suck so much at deployment. It's pretty common for new developers to struggle for days, even weeks to get their first web app deployed.

Hitting a wall when trying to deploy your Django app isn't inevitable. I used to work as a ski instructor (software pays better) and I was taught a saying:

> Teach new skills on easy terrain. On hard terrain, stick to the old skills.

This means that you shouldn't try teaching a fancy new technique on the steepest, hardest runs.
Deploying web applications is _hard_. It gets easier with time, but it's got a nasty learning curve. It's easier to learn if we minimise the number of new skills and try to keep you in a familiar environment.

### Minimal new tools, small steps

That's the focus of this guide. I want to help you achieve lots of small, incremental wins where you gain one small skill, then another, until you have all the skills you need to deploy your Django app. I want to you to understand what the fuck is going on so you don't get stuck. I want to introduce as few new tools as possible.

Here are the new technologies that I propose we learn to use:

- A Linux virtual machine in the cloud for hosting (DigitalOcean)
- SSH and SCP for accesing the server
- git-bash shell scripting
- Python virtual environments
- Gunicorn WSGI server for running your app
- Supervisor for keeping Gunicorn running
- Whitenoise Python library to serve static files
- Cloudflare SaaS tool for DNS, static file caching, SSL

That's still a lot of tools, despite trying to keep it small an simple. Here are some things we will not be using:

- PostgreSQL database
- NGINX reverse proxy
- Containers (eg. Docker, Kubernetes)
- Config management tools (eg. Ansible, Fabric)
- Git version control

You should give them a try sometime... just not yet.

> But don't professional web developers use NGINX/Docker/Postgres/etc? That's what people on Reddit say! I don't want to learn bad practices :(

It's true that these are all great tools. I use them often, but I think they will make learning to deploy Django unnecessarily complicated.
The good news is that you can always add them to your infrastructure later on.
Once you've got this simple deployment down then you can mix it up: you can add NGINX, Postgres and Docker if you like.

### The guide

I am going to assume that you are using Windows for the guide, partly because it's what most new developers use, and partly because it's the worst-case scenario.
That's right: doing this stuff on Windows is hard-mode.
If you have a Mac or Linux desktop, then you can still follow along - there will just be slightly fewer things for you to do.

Also, just so you know, this guide will involve buying a domain name ($2 - $10 USD / year) and using a paid cloud service (5 bucks / month).
If you're not willing (or unable) to get your credit card out and pay for some stuff, then you will not be able to complete every step.

I said this was a "simple" guide, but I didn't say it's short: it's surprisingly long in fact. This guide has five steps, which I suggest you do in order:

1. [Server setup]({filename}/simple-django-deployment/simple-django-deployment-1.md)
2. [Prepare and test Django locally]({filename}/simple-django-deployment/simple-django-deployment-2.md)
3. [Deploy Django to the server]({filename}/simple-django-deployment/simple-django-deployment-3.md)
4. [Run Django in the background]({filename}/simple-django-deployment/simple-django-deployment-4.md)
5. [Automate the re-deployment]({filename}/simple-django-deployment/simple-django-deployment-5.md)
6. [Domain setup]({filename}/simple-django-deployment/simple-django-deployment-6.md)
