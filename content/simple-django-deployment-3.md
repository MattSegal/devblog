Title: Simple Django Deployments part three: deploy code
Description: How to get your Django code running on the server
Slug: simple-django-deployment-3
Date: 2020-04-19 15:00
Category: Django

# Deploy Django to server

- WINDOWS LINE ENDINGS dos2unix?

# Upload your Django app

Lots of ways to do this, scp, rsync, git. I'm going to stick to using scp to limit the number of new tools needed to do this.

This is a very manual process, we will automate this later.

- locally
- create a deploy folder, copy our project over
- remove everything that is not deployable
- mkdir deploy
- cp -r tute deploy
- cp requirements.txt deploy
- ls deploy
- tree deploy (?)
- find deploy -name \*.pyc (? or do on server)
- find deploy -name \*.pyc -delete
- find deploy -name **pycache**
- find deploy -name **pycache** -delete
- tree deploy (?)
- scp -r deploy root@64.225.23.131:/root/
- ssh root@64.225.23.131
- pwd
- ls
- mkdir /app/
- cp -r deploy/\* /app/
- ls /app/
- cd /app/
- install python packages
- same as locally we will set up a virtualenv
- virtualenv -p python3 /app/env
- . env/bin/activate
- which pip
- pip freeze
- pip install -r requirements.txt
- pip freeze

- we need to set DJANO_SETTINGS_MODULE and DJANGO_SECRET_KEY
- set them as system wide environment variables
- nano /etc/environment
  DJANGO_SETTINGS_MODULE="tute.settings.prod"
  DJANGO_SECRET_KEY="dqwdqwd22089ru230r0932ir0923iksd239f0u8fj2wq"
- printenv
- log out, log back in
- printenv | grep DJANGO
- cd /app/
- . env/bin/activate
- cd tute
- ./manage.py migrate
- ls /app/ - see database, that's our prod database
- ./manage.py collectstatic
- ls . - see statifciles
- run gunicorn same as locally
- gunicorn tute.wsgi:application
- curl from another ssh session
- curl localhost:8000
- check from web browser 64.225.23.131:8000
- gunicorn --bind 0.0.0.0:80 tute.wsgi:application
- curl localhost:80
- check from web browser 64.225.23.131
- you're in! static files are working all good
- we can also run ./manage.py shell

- one problem... what happens if we log out of our session?
- how do we fix this?

### Next steps

Get gunicorn to run even when we're not around.

[Run Django in the background]({filename}/simple-django-deployment-4.md)
