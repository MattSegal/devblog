Title: Simple Django Deployments part five: deployment automation
Description: Script your Django deployment with bash
Slug: simple-django-deployment-5
Date: 2020-04-19 17:00
Category: Django

# Script the deployment

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

### Next steps

[Set up your domain]({filename}/simple-django-deployment-6.md)
