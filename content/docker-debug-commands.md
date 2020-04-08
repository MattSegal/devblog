Title: 9 commands for debugging Django in Docker containers
Slug: docker-container-debugging
Date: 2020-04-8 12:00
Category: Docker

You want to get started "Dockerizing" your Django environment and you do a tutorial which shows you how to set it all up with docker-compose. You follow the listed commands and everything is working. Cool!

A few days later there's an error in your code and you want to debug the issue. What caused your dev environment to break? Is it your code? Is it a dependencies issue? Is it a Docker thing? How can you tell?

I've compiled a list of handy Docker commands that I whip out in these "what the fuck is happening!?!?" situations to help me get to the bottom of the issue:

- Rebuild from scratch
- Run a debugger
- Get a bash shell in a running container
- Get a bash shell in a brand new container
- Run a script
- Poke around inside of a PostgreSQL container
- Watch some logs
- View volumes
- Destroy absolutely everything

### Rebuild from scratch

Sometimes you want to rebuild you Docker image from scratch, just to make sure. Rebuilding with the --no-cache flag ensures that your Dockerfile is executed from start to finish, with no intermediate cached layers used.

For docker:

```bash
docker build --no-cache .
```

For docker-compose, assuming you have a "web" service:

```bash
docker-compose build --no-cache web
```

### Run a debugger

You might notice that using docker-compose, Django's runserver and the pdb debugger together doesn't really work.

If you've plopped your debugger into a Django view for example:

```python
def my_view(request):
    things = Thing.objects.all()
    result = do_stuff(things)
    # Launch Python command-line debugger
    import pdb;pdb.set_trace()
    return JsonResponse(result)
```

... and your `docker-compose.yml` file is something like this:

```yaml
services:
  web:
    command: ./manage.py runserver
    # ... more stuff ...
```

... and you start your services like this:

```bash
docker-compose up web
```

Then your Python debugger will never work! When the view hits the pdb.set_trace() function, you'll always see this horrible error:

```text
 # ... 10 million lines of stack trace ...
  File "/usr/lib/python3.6/bdb.py", line 51, in trace_dispatch
    return self.dispatch_line(frame)
  File "/usr/lib/python3.6/bdb.py", line 70, in dispatch_line
    if self.quitting: raise BdbQuit
bdb.BdbQuit
```

This is an easy fix. The debugger, which is inside the Docker container, is trying to communicate with your terminal, which is outside of the Docker container, via some port, which is closed - hence the error. So we need to tell Docker to keep the required port open with --service-ports. More info [here](https://stackoverflow.com/questions/33066528/should-i-use-docker-compose-up-or-run):

```bash
docker-compose run --rm --service-ports web
```

Now when you hit the debugger you will get a functional, interactive pdb interface in your terminal.

### Get a bash shell in a running container

Sometimes you want to poke around inside a container that is already running. You might want to `cat` a file, run `ls` or inspect the output of `ps auxww`. To get inside a running container you can use docker's `exec` command.

First, you need to get the running container's id:

```bash
docker ps
```

Which will get you and output like

```text
CONTAINER ID    ...    NAMES
0dd3d893u8d3    ...    web
518f741c4415    ...    worker
0ce1cfd9c99f    ...    database
```

Say I wanted to poke around in the "worker" container, then I need to note its id of "518f741c4415" and then run bash using `docker exec`:

```bash
docker exec -it 518f741c4415 bash
```

### Get a bash shell in a brand new container

Sometimes you want to poke around inside a container that is based on an image, to see what is baked into the image. You can do this using docker or docker-compose.

For a service set up like this:

```yaml
services:
  web:
    image: myimage:latest
    # ... more stuff ...
```

You can run the image `myimage` using docker:

```bash
docker run --rm -it myimage:latest bash
```

Or via docker-compose:

```bash
docker-compose run --rm web bash
```

Note the `--rm` flag, which will save you from having all these single use containers lying around, using up disk space.

### Run a script

If you just want to run a script in a single-use, throw away container, you can use the `run` command as well. This is particularly useful for running management commands or unit tests:

```bash
docker-compose run --rm web ./manage.py migrate
```

Note: this only works if your container's default working dir is contains `./manage.py`.

### Poke around inside of a PostgreSQL container

If you're using Django and docker-compose then you're likely running a PostgreSQL container, set up something like this:

```yaml
services:
  database:
    image: postgres
    # ... more stuff ...
    environment:
      POSTGRES_HOST_AUTH_METHOD: "trust"

  web:
    command: ./manage.py runserver
    # ... more stuff ...
    environment:
      PGDATABASE: postgres
      PGUSER: postgres
      PGPASSWORD: password
      PGHOST: database
      PGPORT: 5432
```

Then you can use the psql command line from the web container to check out your database tables:

```bash
docker-compose run --rm web psql
```

### Watch some logs

Sometimes you have a container, like a Celery worker or database, which is running in the background and you want to see its console output. Even better, you want to watch its console output in realtime. You can do this with `logs`. For example, if I want to follow the output of the "worker" container:

```bash
docker-compose logs --tail 100 -f worker
```

### View volumes

Sometimes when you're having issues with volume you want to double check what volumes you have and how they're set up. This is relatively straightforward.

To see all volumes:

```bash
docker volume ls
```

Which gets output like

```text
DRIVER              VOLUME NAME
local               docker_postgres-data
```

And then to drill down into one volume:

```text
docker volume inspect docker_postgres-data
```

Giving you something like

```json
[
  {
    "CreatedAt": "2020-04-08T12:44:34+10:00",
    "Driver": "local",
    "Labels": {
      "com.docker.compose.project": "docker",
      "com.docker.compose.version": "1.23.1",
      "com.docker.compose.volume": "postgres-data"
    },
    "Mountpoint": "/var/lib/docker/volumes/docker_postgres-data/_data",
    "Name": "docker_postgres-data",
    "Options": null,
    "Scope": "local"
  }
]
```

If that doesn't help you, there's always the next step.

### Destroy absolutely everything

There's a Docker command that removes all your "unused" data:

```bash
docker system prune
```

That's nice, it might free up some disk space, but what if you want to go full scorched-earth on your Docker envrionemnt? Like tear down Carthage and salt the fields so that nothing will ever grow again?

Here's a script I use occasionally when I just want to get rid of _everything_ and start afresh:

```bash
# Stop all containers
docker kill $(docker ps -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Remove all docker images
docker rmi $(docker images -q)

# Remove all volumes
docker volume rm $(docker volume ls -q)
```

Burn it all down I say! From the ashes, we will rebuild!

If this doesn't fix your issue, I recommend that you throw your laptop out a window, sell all your worldy possesions and [start a new life in the wilderness](https://www.outsideonline.com/2411125/lynx-vilden-stone-age-life).
