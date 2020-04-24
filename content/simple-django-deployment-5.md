Title: Simple Django Deployments part five: deployment automation
Description: Script your Django deployment with bash
Slug: simple-django-deployment-5
Date: 2020-04-19 17:00
Category: Django

# Script the deployment

That was, um, a lot, right? It would suck to have to do all that over again, wouldn't it?

Goal is to run a single script and it all just happens.

./scripts/deploy.sh
./scripts/upload-to-server.sh
./scripts/congfigure-server.sh

```bash
SERVER=64.225.23.131
set -e
# Prepare deploy directory
rm -rf deploy
cp -r tute deploy
cp requirements.txt deploy
find deploy -name \*.pyc -delete
find deploy -name **pycache** -delete

# Copy files to server
ssh root@$SERVER "rm -rf /root/deploy/"
scp -r deploy root@$SERVER:/root/

ssh root@$SERVER
# Then... on the server
set -e
supervisorctl stop gunicorn
rm /app/requirements.txt
rm -rf /app/tute/
cp -r /root/deploy/tute /app/tute
cp /root/deply/requirements.txt /app/requirements.txt
cd /app/
. env/bin/activate
pip install -r requirements.txt
cd tute
./manage.py migrate
./manage.py collectstatic
supervisorctl start gunicorn
```

- automate the process with bash

- note that this process has limitations (stopping gunicorn)
- note that you could run tests and checks here
- ssh into server, stop gunicorn
- nuke old code (immutable)
- copy code from local to server with scp
- activate virtualenv
- install new requirements
- run migrations
- collect static
- chown again?
- start gunicorn
- now that this script is written, you can easily move it into a CI server

- show pushing code changes to prod

# Discussion - starting and stopping gunicorn

# Discussion - what if this goes wrong?

# Optional - Script the setup

link to config management

# Optional - idempotent scripting

# Optional - back up database

- stateful vs stateless

### Next steps

[Set up your domain]({filename}/simple-django-deployment-6.md)
