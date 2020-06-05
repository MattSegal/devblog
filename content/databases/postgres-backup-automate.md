Title: How to automate your Postgres database backups
Description: Taking manual PostgreSQL backups is nice, but let's make the computer to do it for us.
Slug: postgres-backup-automate
Date: 2020-6-5 12:00
Category: DevOps

If you've got a web app running in production, then you'll want to take [regular database backups]({filename}/databases/postgres-backup-and-restore.md), or else you risk losing all your data. Taking these backups manually is fine, but it's easy to forget to do it. It's better to remove the chance of human error and automate the whole process.
To automate your backup and restore you will need three things:

- A safe place to store your backup files
- A script that creates the backups and uploads them to the safe place
- A method to automatically run the backup script every day

As a bonus, I'll also include a script to automatically restore your database from the latest backup.

### A safe place for your database backup files

You don't want to store your backup files on the same server as your database. If your database server gets deleted, then you'll lose your backups as well. Instead, you should store your backups somewhere else, like a hard drive, your PC, or in the cloud.

I like using cloud object storage for this kind of use-case. If you haven't heard of "object storage" before: it's just a kind of cloud service where you can store a bunch of files. All major cloud providers offer this service:

- Amazon's AWS has the [Simple Storage Service (S3)](https://aws.amazon.com/s3/)
- Microsoft's Azure has [Storage](https://azure.microsoft.com/en-us/services/storage/)
- Google Cloud also has [Storage](https://cloud.google.com/storage)
- DigitalOcean has [Spaces](https://www.digitalocean.com/products/spaces/)

These object storage services are _very_ cheap at around 2c/GB/month, you'll never run out of disk space, they're easy to access from command line tools and they have very fast upload/download speeds, especially to/from other services hosted with the same cloud provider. I use these services a lot: this blog is being served from AWS S3.

I like using S3 simply because I'm quite familiar with it, so that's what we're going to use for the rest of this post. If you're not already familiar with using the AWS command-line, then check out this post I wrote about [getting started with AWS S3]({filename}/infra/aws-s3-intro.md) before you continue.

### Creating a database backup script

[previous post]({filename}/databases/postgres-backup-and-restore.md)

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

/etc/environment

### Running the backup script daily

words

cron
pycrontab
