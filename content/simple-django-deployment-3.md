Title: Simple django deployment part three: deploy code
Description: How to get your Django code running on the server
Slug: simple-django-deployment-3
Date: 2020-04-19 15:00
Category: Django

We've got our server set up, and our Django code is ready.
Now we can actually deploy Django to our server.
The goal of this section is to get a basic deployment done.
We'll do some automation and introduce some extra tools later.

In this section we'll cover:

- Windows line endings
- Uploading and running your Django app

### Windows line endings

A quick aside before we start deploying: Windows line endings. These are the curse of every Django developer running Windows.
This is one of those technical details that you never want to know about, but they'll bite you in the ass if you ignore them.

The TLDR is that in Linux and MacOS, lines end with the "\n" character.
On Windows lines end with "\r\n", because fuck-you-that's-why.
The problem is that your Windows Python files will fail on Linux because they have the wrong line endings.

There are several ways to fix this, including writing our own custom bash or Python scripts to convert these line endings, but for simplicity we'll just use an off-the-shelf tool called [dos2unix](https://linux.die.net/man/1/dos2unix), which I'll show you later.

You can help avoid this problem in VSCode by selecting the "LF" option for the "End of Line Sequence" setting, which is visible in the toolbar on the bottom right hand corner of your screen.

# Uploading and running your Django app

Let's upload our code to the server and set up our app so we can run it. There are lots of ways to do get your code onto the server: scp, rsync, git. I'm going to stick to using scp to limit the number of new tools needed to do this.

When we upload our code, we're going to put it in the root user's home directory - /root/. It'll look like this:

````text
/root
└── deploy                  All uploaded code
    ├── requirements.txt    Python requirements
    └── tute                Django project code
        ├── tute            Django app code
        ├── counter         Django app code
        ├── staticfiles     Collected static files
        └── manage.py       Django management script

Then we'll be creating a directory called /app/, which will be the final resting place of our code,
 and we will set up our project like this:

```text
/app
├── env                     Python 3 virtualenv
├── requirements.txt        Python requirements
├── db.sqlite3              Production SQLite database
└── tute                    Django project code
    ├── tute                Django app code
    ├── counter             Django app code
    ├── staticfiles         Collected static files
    └── manage.py           Django management script
````

A key idea is that every time we re-deploy our code in the future, we want to delete and re-create the folder /app/tute,
but we want to keep the database (db.sqlite3), or else we lose all our production data.

What I'm going to show you now is a very manual process, we will automate this later.

- export SERVER=64.225.23.131
- locally

- create a deploy folder, copy our project over
- mkdir deploy
- cp -r tute deploy
- cp requirements.txt deploy
- copy project to root

- upload deploy to the server
- scp -r deploy root@\$SERVER:/root/
- ssh root@\$SERVER "rm -rf /root/deploy/"

- go into server, look at and clean up our deploy directory
- ssh root@\$SERVER
- this isn't the final destination for our code
- pwd
- ls
- ls deploy
- tree deploy (?)
- look at code
- find deploy -name \*.pyc
- find deploy -name \*.pyc -delete
- find deploy -name **pycache**
- find deploy -name **pycache** -delete
- tree deploy (?)
- apt install dos2unix
- dos2unix? where do we do this?

- create project directory
- mkdir /app/
- ls /app/
- cp -r /root/deploy/\* /app/
- ls /app/
- cd /app/
- install python packages
- same as locally we will set up a virtualenv
- which pip3
- which pip
- which python3
- which python
- pip3 install virtualenv (this is global)
- virtualenv -p python3 /app/env
- pip freeze
- . env/bin/activate
- which pip
- which python
- python -V
- pip freeze
- pip install -r requirements.txt
- pip freeze

- now we need to set our environment variables
- we need to set DJANO_SETTINGS_MODULE and DJANGO_SECRET_KEY
- set them as system wide environment variables
- printenv
- nano /etc/environment
  DJANGO_SETTINGS_MODULE="tute.settings.prod"
  DJANGO_SECRET_KEY="dqwdqwd22089ru230r0932ir0923iksd239f0u8fj2wq"
- printenv
- log out, log back in (idk a better way)
- printenv
- printenv | grep DJANGO

- we have uploaded code, cleaned code, created project dir, setup virtualenv, set envars
- now lets set up our database and staticfiles
- cd /app/
- . env/bin/activate
- cd tute
- ./manage.py migrate
- ls /app/ - see database, that's our prod database

- now for our static files
- ./manage.py collectstatic
- ls . - see statifciles

- now we're ready to run our WSGI server - gunicorn
- run gunicorn same as locally
- gunicorn tute.wsgi:application

- is it working?
- curl from another ssh session
- curl localhost:8000
- check from web browser 64.225.23.131:8000

- can we run it on port 80 (only as root)
- gunicorn --bind 0.0.0.0:80 tute.wsgi:application
- curl localhost:80
- check from web browser 64.225.23.131
- you're in! static files are working all good

- ./manage.py createsuperuser
- go to 64.225.23.131/admin

- finally, we can look at our models via the shell
- we can also run ./manage.py shell

- one problem... what happens if we log out of our session?
- how do we fix this?

So to recap, the testing we just did looks like this:

![gunicorn http]({attach}gunicorn-server-http.png)

We're most of the way there! We've got our Django app running our server.
There's just a bit more to go before it's fully deployed.

### Next steps

To really say that our app is "deployed", we need it to run even when we're not around.
In the next section, we'll learn how to [run Django in the background]({filename}/simple-django-deployment-4.md)
