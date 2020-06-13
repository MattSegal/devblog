Title: How to automatically reset your local Django database
Description: How
Slug: reset-django-local-database
Date: 2020-6-13 12:00
Category: Django

Sometimes when you're working on a Django app you want a fresh start. You want to nuke all of the data in your local database and start again from scratch. Maybe you ran some migrations that you don't want to keep, or perhaps there's some test data that you want to get rid of. This doesn't happen very often, but when it does it's _super_ annoying to do it manually over and over.

In this post I'll show you small script that you can use to reset your local Django database. It completely automates deleting the old data, running migrations and setting up new users. I've written the script in `bash` but most of it will also work in `powershell` or `cmd` with only minor changes.

### Resetting the database

We're going to reset our local database with the [django-extensions](https://django-extensions.readthedocs.io/en/latest/installation_instructions.html) package, which provides a nifty little helper command called `reset_db`. This command destroys and recreates your Django app's database.

```bash
./manage.py reset_db
```

I like to add the `--noinput` flag so the script does not ask me for confirmation, and the `--close-sessions` flag if I'm using PostgreSQL locally so that the command does not fail if my Django app is connected the database at the same time.

```bash
./manage.py reset_db --noinput --close-sessions
```

This is is a good start, but now we have no migrations, users or any other data in our database. We need to add some data back in there before we can start using the app again.

### Running migrations

Before you do anything else it's important to run migrations so that all your database tables are set up correctly:

```bash
./manage.py migrate
```

### Creating an admin user

You want to have a superuser set up so you can log into the Django admin. It's nice when a script guarantees that your superuser always has the same username and password. The first part of creating a superuser is pretty standard:

```bash
./manage.py createsuperuser \
   --username admin \
   --email admin@example.com \
   --noinput
```

Now we want to set the admin user's password to something easy to remember, like "12345". This isn't a security risk because it's just for local development. This step involves a little more scripting trickery. Here we can use `shell_plus`, which is an enhanced Django shell provided by django-extensions. The `shell_plus` command will automatically import all of our models, which means we can write short one liners like this one, which prints the number of Users in the database:

```bash
./manage.py shell_plus --quiet-load -c "print(User.objects.count())"
# 13
```

Using this method we can grab our admin user and set their password:

```bash
./manage.py shell_plus --quiet-load -c "
u = User.objects.get(username='admin')
u.set_password('12345')
u.save()
"
```

### Setting up new data

There might be a little bit of data that you want to set up every time you reset your database. For example, in one app I run, I want to ensure that there is always a `SlackMessage` model that has a `SlackChannel`. We can set up this data in the same way we set up the admin user's password:

```bash
./manage.py shell_plus --quiet-load -c "
c = SlackChannel.objects.create(name='Test Alerts')
SlackMessage.objects.create(channel=c)
"
```

If you need to set up a _lot_ of data then there are options like [fixtures](https://docs.djangoproject.com/en/3.0/howto/initial-data/) or tools like [Factory Boy](https://factoryboy.readthedocs.io/en/latest/) (which I heartily recommend). If you only need to do a few lines of scripting to create your data, then you can include them in this script. If your development data setup is very complicated, then I recommend putting all the setup code into a custom management command.

### The final script

This is the script that you can use to reset your local Django database:

```bash
#!/bin/bash
# Resets the local Django database, adding an admin login and migrations
set -e
echo -e "\n>>> Resetting the database"
./manage.py reset_db --close-sessions --noinput

echo -e "\n>>> Running migrations"
./manage.py migrate

echo -e "\n>>> Creating new superuser 'admin'"
./manage.py createsuperuser \
   --username admin \
   --email admin@example.com \
   --noinput

echo -e "\n>>> Setting superuser 'admin' password to 12345"
./manage.py shell_plus --quiet-load -c "
u=User.objects.get(username='admin')
u.set_password('12345')
u.save()
"

# Any extra data setup goes here.

echo -e "\n>>> Database restore finished."
```

### Docker environments

If you're running your local Django app in a Docker container via `docker-compose`, then this process is a little bit more tricky, but it's not too much more complicated. You just need to add two commands to your script.

First you want a command to kill all running containers, which I do because I'm superstitious and don't trust that `reset_db` will actually close all database connections:

```bash
function stop_docker {
    echo -e "\nStopping all running Docker containers"
    # Ensure that no containers automatically restart
    docker update --restart=no `docker ps -q`
    # Kill everything
    docker kill `docker ps -q`
}
```

We also want a shorthand way to run commands inside your docker environment. Let's say you are working with a compose file located at `docker/docker-compose.local.yml` and your Django app's container is called `web`. Then you can run your commands inside the container as follows:

```bash
function run_docker {
    docker-compose -f docker/docker-compose.local.yml run --rm web $@
}
```

Now we can just prefix `run_docker` to all the management commands we run. For example:

```bash
# Without Docker
./manage.py reset_db --close-sessions --noinput
# With Docker
run_docker ./manage.py reset_db --close-sessions --noinput
```

I will note that this `run_docker` shortcut can act a little weird when you're passing strings to `shell_plus`. You might need to experiment with different methods of escaping whitespace etc.

### Conclusion

Hopefully this script will save you some time when you're working on your Django app. If you're interested in more Django-related database stuff then you might enjoy reading about how to [back up and restore a Postgres database](https://mattsegal.dev/postgres-backup-and-restore.html) and then how to [fully automate your prod backup process](https://mattsegal.dev/postgres-backup-automate.html).
