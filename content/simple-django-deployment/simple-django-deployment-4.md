Title: Simple Django deployment part four: run a service
Description: How to get gunicorn to run in the background
Slug: simple-django-deployment-4
Date: 2020-04-26 16:00
Category: Django

So we've got a problem. Our Django app only runs when we're logged into the server via SSH and running Gunicorn.
That's not going to work long term. We need to get Gunicorn running even when we're not around.
In addition, if our Gunicorn server crashes because of some bug, we want it to automatically restart.

In this section we're going to cover:

- Setting up Supervisor
- Adding Gunicorn config
- Setting up basic logging
- Running as root

### Setting up Supervisor

We're going to solve our process supervison problem with [Supervisor](http://supervisord.org/). It's a program
that we can use to run Gunicorn in the background. I chose this tool because a lot of other Django devs use it,
plus it's pretty easy to install, configure and run.

We can install it into our virtualenv with pip, which is handy:

```bash
pip install supervisor
```

Supervisor has several parts that we should know about:

- **supervisord**: the "[daemonized](<https://en.wikipedia.org/wiki/Daemon_(computing)>)" program that will run Gunicorn as a "child process"
- **supervisorctl**: the tool that we will use to send commands to supervisord

We'll also be writing some config files to help automate how Supervisor and Gunicorn run

- **supervisord.conf**: a file that we'll need write to configure how supervisord works
- **gunicorn.conf.py**: a file we'll need to write to configure how Gunicorn works

Finally, we need to start configuring basic logging. We didn't really need logging before because when we ran "runserver" or "gunicorn",
we could just read the console output on our terminal. We can't do that anymore because we cannot see the terminal. So we need to ask
gunicorn and supervisord to write their logs to a file somewhere, so we can read them later if we need to. Once we're done, our Django project will look like this when we deploy it:

```text
/app
├── env                     Python 3 virtualenv
├── requirements.txt        Python requirements
├── db.sqlite3              Production SQLite database
├── scripts                 Bash scripts
|   └── run-gunicorn.sh     Script to run Gunicorn
├── config                  Config files
|   ├── supervisord.conf    Supervisor config
|   └── gunicorn.conf.py    Gunicorn config
├── logs                    Log files
|   ├── supervisord.log     Supervisor logs
|   └── gunicorn.access.log Gunicorn access logs
|   └── gunicorn.app.log    Gunicorn application logs
└── tute                    Django project code
    ├── tute                Django app code
    ├── counter             Django app code
    ├── staticfiles         Collected static files
    └── manage.py           Django management script
```

It's coming to be a lot of stuff isn't it? When I said this would be a "simple" deployment guide, I meant that in a relative sense. ¯\\\_(ツ)\_/¯

Let's get started by setting up Supervisor to run our Django app using Gunicorn. Unfortunately we can't test this new setup completely on our Windows machine, so we're going to have to upload our files to the server to try this out.

You can find the scripts and config referenced in the video [here](https://github.com/MattSegal/django-deploy).

<div class="yt-embed">
    <iframe 
        src="https://www.youtube.com/embed/ny2L15dOf4Q" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen
    >
    </iframe>
</div>

### Adding Gunicorn config

Next we want to tweak how Gunicorn runs a little bit. In particular, we want to set the number of "workers". The Gunicorn process runs as a sort of "master", which then co-ordinates a bunch of child "worker" processes. The [Gunicorn docs](https://docs.gunicorn.org/en/stable/settings.html#workers) suggest using 2-4 workers per CPU core (we have 1 on our DigitalOcean VM), but the default is 1.

If we only have 1 worker, and two people send our site a HTTP request, then one of them will need to wait for the other to finish. If we set more workers, it means we can handle more HTTP requests at the same time. Too many workers are kind of pointless because they'll just end up fighting for access to the CPU. So let's pick 3 workers, because we have 1 CPU core, nothing else happening on this machine, and 3 is half way between the recommended 2-4 (which is a very arbitrary way of deciding).

We _could_ apply this config change by just adding it as a command line parameter when we run Gunicorn:

```bash
gunicorn tute.wsgi:application --workers 3
```

But this will become unweildy when we configure more and more settings. It's kind of just an aesthetic thing, but I'd rather write this config to a file than as command line parameters. So instead, we can write a [configuration file](https://docs.gunicorn.org/en/stable/configure.html#configuration-file) called "gunicorn.conf.py" and put all our config in there:

```python
# gunicorn.conf.py

bind = "0.0.0.0:80"
workers = 3
# Add more config here
```

and then when we run gunicorn we can just do this:

```bash
gunicorn tute.wsgi:application -c config/gunicorn.conf.py
```

Let's set up our Gunicorn config.

<div class="yt-embed">
    <iframe 
        src="https://www.youtube.com/embed/KsCJw3skJdQ" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen
    >
    </iframe>
</div>

Now that our Gunicorn config has been created, we can set up logging.

### Setting up basic logging

As I mentioned earlier, we need logging because Gunicorn is now running in the background and we can't see its terminal output.
This is important when something goes wrong on in our code and we need to figure out what happened. In this section we'll set up logging so we can see:

- what supervisord is doing
- what requests Gunicorn is receiving
- what Gunicorn is doing, plus Django logs

This isn't the _perfect_ logging setup, I go into more detail on how we can improve Django logging in production [in this blog post](https://mattsegal.dev/file-logging-django.html), but it's good enough for now.

When we're done, our logs on the server will look like this:

```text
/app
...
└── logs                    Log files
    ├── supervisord.log     Supervisor logs
    └── gunicorn.access.log Gunicorn access logs
    └── gunicorn.app.log    Gunicorn application logs
```

<div class="yt-embed">
    <iframe 
        src="https://www.youtube.com/embed/ubR--JB5iQM" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen
    >
    </iframe>
</div>

Ok we've got logging all set up, looking good! Later on, you might want to also add [error monitoring](https://mattsegal.dev/sentry-for-django-error-monitoring.html) to your app, which alerts you when errors happen.

### Running as root

Before we move on to automating our deployments, there's an elephant in the room that I'd like to address.
This whole time we've been running Gunicorn as the Linux root user.
In Windows terminology we'd call this an "admin" account.

This setup is a potential security risk. Here's the problem: we've given Gunicorn permission
to do _anything_ to our VM. It can delete all the files, install any programs they want, terminate other processes, whatever.
This will be a problem if a hacker figures out how to execute arbitrary code on our Django app, or manipulate our Django app in some other way (like writing to any part of the filesystem).
Any vulnerability that we accidentally write in our Django app can do maximum damage to our server,
because we've allowed Gunicorn to do everything. The two biggest risks that I see are:

- a hacker could trash our server and delete all our shit
- a hacker could gain control of our server and use it to mine Bitcoin, [DDoS](https://www.cloudflare.com/en-au/learning/ddos/what-is-a-ddos-attack/) another server, etc.

This is why people say "don't run Gunicorn as root", because if you fuck up your code somewhere, or if Gunicorn itself
is vulnerable somehow, then control of your server and data could be compromised.

So why does this guide have you run Gunicorn as root?

- It makes it easier for us to access port 80
- It removes some extra work around managing file permissions
- It avoids some extra config work around creating new users and assigning user roles
- Our server, app and data are all pretty trivial and if they're compromised it's not a big deal

As you learn more about deploying web apps and managing infrastructure, you'll need to learn to make your own decisions about
the security risks you're willing to take vs. the extra work you'll need to do. For now I think running as root is OK.
In the future, especially if you think your app is important, you may want to run Gunicorn as a non-root user and research
other security measures.

### Next steps

Now that we've got our Django app up-and-running, all on its own, we can look forward to [automating the deployment]({filename}/simple-django-deployment/simple-django-deployment-5.md), so we can deploy our code again and again, quickly and easily.
