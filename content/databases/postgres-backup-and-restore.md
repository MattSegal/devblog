Title: How to backup and restore a Postgres database
Description: Losing your Django app's data is somewhere between annoying and catastropic. Here's how to take backups and restore from them in PostgreSQL.
Slug: postgres-backup-and-restore
Date: 2020-6-4 12:00
Category: Django

You've deployed your Django app to to the internet. Grats! Now you have a fun new problem: your app's database is full of precious "live" data, and if you lose that data, it's gone forever. If your database gets blown away or corrupted, then you will need backups to restore your data. This post will go over how to backup and restore PostgreSQL, which is the database most commonly deployed with Django.

Not everyone needs backups. If your Django app is just a hobby project then losing all your data might not be such a big deal. That said, if your app is a critical part of a business, then losing your app's data could literally mean the end of the business - people losing their jobs and going bankrupt. So, at least some of time, you don't want to lose all your data.

The good news is that backing up and restoring Postgres is pretty easy, you only need two commands: `pg_dump` and `pg_restore`. If you're using MySQL instead of Postgres, then you can do something very similar to the instructions in this post using [`mysqldump`](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html).

### Taking database backups

I'm going to assume that you've already got a Postgres database running somewhere. You'll need to run the following code from a `bash` shell on a Linux machine that can access the database. In this example, let's say you're logged into the database server with `ssh`.

The first thing to do is set some [Postgres-specifc environment variables](https://www.postgresql.org/docs/current/libpq-envars.html) to specify your target database and login credentials. This is mostly for our convenience later on.

```bash
# The server Postgres is running on
export PGHOST=localhost
# The port Postgres is listening on
export PGPORT=5432
# The database you want to back up
export PGDATABASE=mydatabase
# The database user you are logging in as
export PGUSER=myusername
# The database user's password
export PGPASSWORD=mypassw0rd
```

You can test these environment variables by running a [`psql`](https://www.postgresql.org/docs/current/app-psql.html) command to list all the tables in your app's database.

```bash
psql -c "\dt"

# Output:
# List of relations
# Schema | Name          | Type  | Owner
#--------+---------------+-------+--------
# public | auth_group    | table | myusername
# public | auth_group... | table | myusername
# public | auth_permi... | table | myusername
# public | django_adm... | table | myusername
# .. etc ..
```

If `psql` is missing you can install it on Ubuntu or Debian using `apt`:

```bash
sudo apt install postgresql-client
```

Now we're ready to create a database dump with [`pg_dump`](https://www.postgresql.org/docs/12/app-pgdump.html). It's pretty simple to use because we set up those environment variables earlier. When you run `pg_dump`, it just spits out a bunch of SQL statements as hundreds, or even thousands of lines of text. You can take a look at the output using `head` to view the first 10 lines of text:

```bash
pg_dump | head

# Output:
# --
# -- PostgreSQL database dump
# --
# -- Dumped from database version 9.5.19
# -- Dumped by pg_dump version 9.5.19
# SET statement_timeout = 0;
# SET lock_timeout = 0;
# SET client_encoding = 'UTF8';
```

The SQL statements produced by `pg_dump` are instructions on how to re-create your database.
You can turn this output into a backup by writing all this SQL text into a file:

```bash
pg_dump > mybackup.sql
```

That's it! You now have a database backup. You might have noticed that storing all your data as SQL statements is rather inefficient. You can compress this data by using the "custom" dump format:

```bash
pg_dump --format=custom > mybackup.pgdump
```

This "custom" format is ~3x smaller in terms of file size, but it's not as pretty for humans to read because it's now in some funky non-text binary format:

```bash
pg_dump --format=custom | head

# Output:
# xtshirt9.5.199.5.19k0ENCODINENCODING
# SET client_encoding = 'UTF8';
# false00
# ... etc ...
```

Finally, `mybackup.pgdump` is a crappy file name. It's not clear what is inside the file. Are we going to remember which database this is for? How do we know that this is the freshest copy? Let's add a [timestamp](https://en.wikipedia.org/wiki/Unix_time) plus a descriptive name to help us remember:

```bash
# Get Unix epoch timestamp
# Eg. 1591255548
TIME=$(date "+%s")
# Descriptive file name
# Eg. postgres_mydatabase_1591255548.pgdump
BACKUP_FILE="postgres_${PGDATABASE}_${TIME}.pgdump"
pg_dump --format=custom > $BACKUP_FILE
```

Now you can run these commands every month, week, or day to get a snapshot of your data.
If you wanted, you could write this whole thing into a `bash` script called `backup.sh`:

```bash
#!/bin/bash
# Backs up mydatabase to a file.
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=mydatabase
export PGUSER=myusername
export PGPASSWORD=mypassw0rd
TIME=$(date "+%s")
BACKUP_FILE="postgres_${PGDATABASE}_${TIME}.pgdump"
echo "Backing up $PGDATABASE to $BACKUP_FILE"
pg_dump --format=custom > $BACKUP_FILE
echo "Backup completed"
```

You should avoid hardcoding passwords like I just did above, it's better to pass credentials in as a script argument or environment variable. The file `/etc/environment` is a nice place to store these kinds of credentials on a secure server.

### Restoring your database from backups

It's pointless creating backups if you don't know how to use them to restore your data.
There are three scenarios that I can think of where you want to run a restore:

- You need to set up your database from scratch
- You want to rollback your exiting database to a previous time
- You want to restore data in your dev environment

I'll go over these scenarios one at a time.

### Restoring from scratch

Sometimes you can lose the database server and there is nothing left. Maybe you deleted it by accident, thinking it was a different server. Luckily you have your database backup file, and hopefully some [automated configuration management](https://mattsegal.dev/intro-config-management.html) to help you quickly set the server up again.

Once you've got the new server provisioned and PostgreSQL installed, you'll need to recreate the database and the user who owns it:

```bash
sudo -u postgres psql <<-EOF
    CREATE USER $PGUSER WITH PASSWORD '$PGPASSWORD';
    CREATE DATABASE $PGDATABASE WITH OWNER $PGUSER;
EOF
```

Then you can set up the same environment variables that we did earlier (PGHOST, etc.) and then use [`pg_restore`](https://www.postgresql.org/docs/12/app-pgrestore.html) to restore your data.
You'll probably see some warning errors, which is normal.

```bash
BACKUP_FILE=postgres_mydatabase_1591255548.pgdump
pg_restore --dbname $PGDATABASE $BACKUP_FILE

# Output:
# ... lots of errors ...
# pg_restore: WARNING:  no privileges were granted for "public"
# WARNING: errors ignored on restore: 1
```

I'm not 100% on what all these errors mean, but I believe they're mostly related to the restore script trying to modify Postgres objects that your user does not have permission to modify. If you're using a standard Django app this shouldn't be an issue. You can check that the restore actually worked by checking your tables with `psql`:

```bash
# Check the tables
psql -c "\dt"

# Output:
# List of relations
# Schema | Name          | Type  | Owner
#--------+---------------+-------+--------
# public | auth_group    | table | myusername
# public | auth_group... | table | myusername
# public | auth_permi... | table | myusername
# public | django_adm... | table | myusername
# .. etc ..

# Check the last migration
psql -c "SELECT * FROM django_migrations ORDER BY id DESC LIMIT 1"

# Output:
#  id |  app   | name      | applied
# ----+--------+-----------+---------------
#  20 | tshirt | 0003_a... | 2019-08-26...

```

There you go! Your database has been restored. Crisis averted.

### Rolling back an existing database

If you want to roll your existing database back to an previous point in time, deleting all new data, then you will need to use the `--clean` flag, which drops your restored database tables before re-creating them ([docs here](https://www.postgresql.org/docs/12/app-pgrestore.html)):

```bash
BACKUP_FILE=postgres_mydatabase_1591255548.pgdump
pg_restore --clean --dbname $PGDATABASE $BACKUP_FILE
```

### Restoring a dev environment

It's often beneficial to restore a testing or development database from a known backup.
When you do this, you're not so worried about setting up the right user permissions.
In this case you want to completely destroy and re-create the database to get a completely fresh start, and you want to use the `--no-owner` flag to ignore any database-user related stuff in the restore script:

```bash
sudo -u postgres psql -c "DROP DATABASE $PGDATABASE"
sudo -u postgres psql -c "CREATE DATABASE $PGDATABASE"
BACKUP_FILE=postgres_mydatabase_1591255548.pgdump
pg_restore --no-owner --dbname $PGDATABASE $BACKUP_FILE
```

I use this method quite often to pull non-sensitive data down from production environments to try and reproduce bugs that have occured in prod. It's much easier to fix mysterious bugs when you have regular database backups, [error reporting](https://mattsegal.dev/sentry-for-django-error-monitoring.html) and [centralized logging](https://mattsegal.dev/django-logging-papertrail.html).

### Next steps

I hope you now have the tools you need to backups and restore your Django app's Postgres database. If you want to read more the [Postgres docs](https://www.postgresql.org/docs/12/index.html) have a good section on [database backups](https://www.postgresql.org/docs/12/backup-dump.html).

Once you've got your head around database backups, you should automate the process to make it more reliable. I will write more on this soon.
