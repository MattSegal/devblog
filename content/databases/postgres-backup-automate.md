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

In my [previous post on database backups]({filename}/databases/postgres-backup-and-restore.md) I showed you a small script to automatically take a backup:

```bash
#!/bin/bash
# Backs up mydatabase to a file.
TIME=$(date "+%s")
BACKUP_FILE="postgres_${PGDATABASE}_${TIME}.pgdump"
echo "Backing up $PGDATABASE to $BACKUP_FILE"
pg_dump --format=custom > $BACKUP_FILE
echo "Backup completed for $PGDATABASE"
```

I'm going to assume you have set up the Postgres database environment variables (PGHOST, etc) either in the script, or elsewhere, as mentioned in the previous post.
Next we're going to get it to upload all backups to AWS S3.

### Uploading to AWS Simple Storage Service (S3)

We will be uploading our backups to S3 with the `aws` command line (CLI) tool. To get this tool to work, we need to set up our AWS credentials on the server by either using `aws configure` or by setting the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. Once that's done we can use `aws s3 cp` to upload our backup files. Let's say we're using a bucket called "mydatabase-backups":

```bash
#!/bin/bash
# Backs up mydatabase to a file and then uploads it to AWS S3.
TIME=$(date "+%s")
BACKUP_FILE="postgres_${PGDATABASE}_${TIME}.pgdump"
echo "Backing up $PGDATABASE to $BACKUP_FILE"
pg_dump --format=custom > $BACKUP_FILE

# Copy file to AWS S3
S3_BUCKET=s3://mydatabase-backups
S3_TARGET=$S3_BUCKET/$BACKUP_FILE
echo "Copying $BACKUP_FILE to $S3_TARGET"
aws s3 cp $BACKUP_FILE $S3_TARGET

echo "Backup completed for $PGDATABASE"
```

You should be able to run this multiple times and see a new backup appear in the S3 web UI every time you do it.
As a bonus, you can add a little one liner that checks for the last uploaded file to the S3 bucket:

```bash

BACKUP_RESULT=$(aws s3 ls $S3_BUCKET | sort | grep $PGDATABASE | tail -n 1)
echo "Latest S3 backup: $BACKUP_RESULT"
```

Once you're confident that your backup script works, let's move on to getting it to run every day.

### Running cron jobs

Next we need to get our server to run this script every day, even when we're not around. The simplest way to do this is on a Linux server is with [cron](https://en.wikipedia.org/wiki/Cron). Cron can automatically run scripts for us on a schedule. We'll be using the `crontab` tool to set up our backup job.

You can read more about how to use crontab [here](https://linuxize.com/post/scheduling-cron-jobs-with-crontab/). If you find that you're having issues setting up cron, you might also find this [StackOverflow post](https://serverfault.com/questions/449651/why-is-my-crontab-not-working-and-how-can-i-troubleshoot-it) useful.

Before we set up our daily database backup job, I suggest trying out a test script to make sure that your cron setup is working. For example, this script prints the current time when is run:

```bash
#!/bin/bash
echo $(date)
```

Write this script wih `nano`, save it, then make it executable as follows:

```bash
chmod +x ~/test.sh
```

Then you can test it out a little by running it a couple of times to check that it is printing the time:

```bash
~/test.sh
# Sat Jun  6 08:05:14 UTC 2020
~/test.sh
# Sat Jun  6 08:05:14 UTC 2020
~/test.sh
# Sat Jun  6 08:05:14 UTC 2020
```

Once you're confident that your test script works, you can create a cron job to run it every minute.
Cron uses a special syntax to specifiy how often a job runs. These "cron expressions" are a pain to write by hand, so I use
[this tool](https://crontab.cronhub.io/) to generate them.
The cron expression for "every minute" is the inscrutable string "`* * * * *`". This is the crontab entry that we're going to use:

```bash
# Test crontab entry
SHELL=/bin/bash
* * * * * ~/test.sh &>> ~/time.log
```

- The `SHELL` setting tells crontab to use bash to execute our command
- The "`* * * * *`" entry tells cron to execute our command every minute
- The command `~/test.sh &>> ~/time.log` runs our test script and appends all output to a log file

Enter the text above into your user's crontab file using the crontab editor:

```bash
crontab -e
```

Once you've saved your entry, you should then be able to view your crontab entry using the list command:

```bash
crontab -l
# SHELL=/bin/bash
# * * * * * ~/test.sh &>> ~/time.log
```

You can check that cron is actually trying to run your script by watching the system log:

```bash
tail -f /var/log/syslog | grep CRON
# Jun  6 11:17:01 swarm CRON[6908]: (root) CMD (~/test.sh &>> ~/time.log)
# Jun  6 11:17:01 swarm CRON[6908]: (root) CMD (~/test.sh &>> ~/time.log)
```

You can also watch your logfile to see that time is being written every minute:

```bash
tail -f time.log
# Sat Jun 6 11:34:01 UTC 2020
# Sat Jun 6 11:35:01 UTC 2020
# Sat Jun 6 11:36:01 UTC 2020
# Sat Jun 6 11:37:01 UTC 2020
```

Once you're happy that you can run a test script every minute with cron, we can move
on to running your database backup script daily.

### Running our backup script daily

Now we're nearly ready to run our backup script using a cron job. There are a few changes that we'll
need to make to our existing setup. First we need to write our database backup script to `~/backup.sh` and make sure it is executable:

```bash
chmod +x ~/backup.sh
```

Then we need to crontab entry to run every day, which will be "[`0 0 * * *`](https://crontab.cronhub.io/)",
and update our cron command to run our backup script. Our new crontab entry should be:

```bash
# Database backup crontab entry
SHELL=/bin/bash
0 0 * * * ~/backup.sh &>> ~/backup.log
```

Update your crontab with `crontab -e`. Now we wait! This script should run every night at midnight (server time) to
take your database backups and upload them to AWS S3. If this isn't working, then change your cron expression
so that it runs the script every minute, and use the steps I showed above to try and debug the problem.

Hopefully it all runs OK and you will have plenty of daily database backups to roll back to if anything ever goes wrong.
