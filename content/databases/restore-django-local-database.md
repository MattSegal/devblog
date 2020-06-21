Title: How to pull production data into your local Postgres database
Description: How to copy a Postgres database backup into your local database
Slug: restore-django-local-database
Date: 2020-6-21 12:00
Category: Django

Sometimes you want to write a feature for your Django app that requires a lot of structured data that already exists in production. This happened to me recently: I needed to create a reporting tool for internal business users. The problem was that I didn't have much data in my local database. How can I see what my reports will look like if I don't have any data?

It's possible to generate a bunch of fake data using a management command. I've written earlier about [how to do this with FactoryBoy](https://mattsegal.dev/django-factoryboy-dummy-data.html). This approach is great for filling web pages with dummy content, but it's tedious to do if your data is highly structured and follows a bunch of implcit rules. In the case of my reporting tool, the data I wanted involved hundreds of form submissions, and each submission has dozens of answers with many different data types. Writing a script to generate data like this would haven take ages! I've also seen situations like this when working with billing systems and online stores with many product categories.

Wouldn't it be nice if we could just get a copy of our production data and use that for local development? You could just pull the latest data from prod and work on your feature with the confidence that you have plenty of data that is structured correctly.

In this post I'll show you a script which you can use to fetch a Postgres database backup from cloud storage and use it to populate your local Postgres database with prod data. This post builds on three previous posts of mine, which you might want to read if you can't follow the scripting in this post:

- [How to automatically reset your local Django database](https://mattsegal.dev/reset-django-local-database.html)
- [How to backup and restore a Postgres database](https://mattsegal.dev/postgres-backup-and-restore.html)
- [How to automate your Postgres database backups](https://mattsegal.dev/postgres-backup-automate.html)

I'm going to do all of my scripting in bash, but it's also possible to write similar scripts in PowerShell, with only a few tweaks to the syntax.

### Starting script

Let's start with the "database reset" bash script from my [previous post](https://mattsegal.dev/reset-django-local-database.html). This script resets your local database, runs migrations and creates a local superuser for you to use. We're going to extend this script with an additional step to download and restore from our latest database backup.

```bash
#!/bin/bash
# Resets the local Django database, adding an admin login and migrations
set -e
echo -e "\n>>> Resetting the database"
./manage.py reset_db --close-sessions --noinput

# =========================================
# DOWNLOAD AND RESTORE DATABASE BACKUP HERE
# =========================================

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

echo -e "\n>>> Database restore finished."
```

### Fetching the latest database backup

Now that we have a base script to work with, we need to fetch the latest database backup. I'm going to assume that you've followed my guide on [automating your Postgres database backups](https://mattsegal.dev/postgres-backup-automate.html).

Let's say your database is saved in an AWS S3 bucket called `mydatabase-backups`, and you've saved your backups with a timestamp in the filename, like `postgres_mydatabase_1592731247.pgdump`. Using these two facts we can use a little bit of bash scripting to find the name of the latest backup from our S3 bucket:

```bash
# Find the latest backup file
S3_BUCKET=s3://mydatabase-backups
LATEST_FILE=$(aws s3 ls $S3_BUCKET | awk '{print $4}' | sort | tail -n 1)
echo -e "\nFound file $LATEST_FILE in bucket $S3_BUCKET"
```

Once you know the name of the latest backup file, you can download it to the current directory with the `aws` CLI tool:

```bash
# Download the latest backup file
aws s3 cp ${S3_BUCKET}/${LATEST_FILE} .
```

The `.` in this case refers to the current directory.

### Restoring from the latest backup

Now that you've downloaded the backup file, you can apply it to your local database with `pg_restore`. You may need to install a Postgres client on your local machine to get access to this tool. Assuming your local Postgres credentials aren't a secret, you can just hardcode them into the script:

```bash
pg_restore \
    --clean \
    --dbname postgres \
    --host localhost \
    --port 5432 \
    --username postgres \
    --no-owner \
    $LATEST_FILE
```

In this case we use `--clean` to remove any existing data and we use `--no-owner` to ignore any commands that set ownership of objects in the database.

### Look ma, no files!

You don't have to save your backup file to disk before you use it to restore your local database: you can stream the data directly from `aws s3 cp` to `pg_restore` using pipes.

```bash
aws s3 cp ${S3_BUCKET}/${LATEST_FILE} - | \
    pg_restore \
        --clean \
        --dbname postgres \
        --host localhost \
        --port 5432 \
        --username postgres \
        --no-owner
```

The `-` in this case means "stream to stdout", which we use so that we can pipe the data.

### Final script

Here's the whole thing:

```bash
#!/bin/bash
# Resets the local Django database,
# restores from latest prod backup,
# and adds an admin login and migrations
set -e
echo -e "\n>>> Resetting the database"
./manage.py reset_db --close-sessions --noinput

echo -e "\nRestoring database from S3 backups"
S3_BUCKET=s3://mydatabase-backups
LATEST_FILE=$(aws s3 ls $S3_BUCKET | awk '{print $4}' | sort | tail -n 1)
aws s3 cp ${S3_BUCKET}/${LATEST_FILE} - | \
    pg_restore \
        --clean \
        --dbname postgres \
        --host localhost \
        --port 5432 \
        --username postgres \
        --no-owner

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

echo -e "\n>>> Database restore finished."
```

You should be able to to run this over and over and over to get the latest database backup working on your local machine.

### Other considerations

When talking about using production backups locally, there are two points that I think are important.

First, production data can contain sensitive user information including names, addresses, emails and even credit card details. You need to ensure that this data is only be distributed to people who are authorised to access it, or alternatively the backups should be sanitized so the senitive data is overwritten or removed.

Secondly, It's possible to use database backups to debug issues in production. I think it's a great method for squashing hard-to-reproduce bugs, but it shouldn't be your only way to solve production errors. Before you move onto this technique, you should first ensure you have [application logging](https://mattsegal.dev/file-logging-django.html) and [error monitoring](https://mattsegal.dev/sentry-for-django-error-monitoring.html) set up for your Django app, so that you don't lean on your backups as a crutch.

### Next steps

If you don't already have automated prod backups, I encourage you to set that up if you have any valuable data in your Django app. Once that's done, you'll be able to use this script to pull down prod data into your local dev environment on demand.
