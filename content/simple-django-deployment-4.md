Title: Simple Django Deployments part four: run a service
Description: How to get gunicorn to run in the background
Slug: simple-django-deployment-4
Date: 2020-04-19 16:00
Category: Django

# Make it a service, run as a service

- you might have noticed that running Django only works when you have a terminal session
- get it to run in the background
- set up supervisord
- run as service (as root)
- we don't want to run as root (why?)
- create gunicorn user
- give user file permissions over /app/ chown -R
- change supervisord to run as gunicorn or something?

[Script the deployment]({filename}/simple-django-deployment-5.md)

# NOTES

will gunicorn run as non root? what do we need to do?

- chown /app/
- will it be able to write the database?

Supervisor:

does not work on Windows - cannot be tested locally

pip install supervisor (in virtualenv)

supervisord - the bit that

- runs the child programs
- respondin to commands from clients
- restarts crashed or exited subprocesseses
- logs its subprocess stdout and stderr output
- generates and handles “events” corresponding to points in subprocess lifetimes
- uses /etc/supervisord.conf

supervisorctl

- command line client for access to supervisord

config

echo_supervisord_conf > config/supervisord.conf
so we can run supervisord -c supervisord.conf

```
[program:gunicorn]
command=/app/scripts/run-gunicorn.sh
autostart=true
autorestart=true
user=root
```

- note supervisord.log
  running supervisord will detatch it an it'll run in the background

to change the programms we can `kill -HUP` the process
(or otherwise restart it?)

supervisord can run as --user=USER
--logfile=FILE

supervisorctl

- status all
- update all (Reload config and add/remove as necessary, and will restart affected programs)
- pid (get pid)
- restart <name>
- start stop

### Running as root

- do we trust supervisord as root?
- do we trust gunicorn as root?
- what could go wrong?

### Logging

- we need logging or we're fucked

### Security check?
