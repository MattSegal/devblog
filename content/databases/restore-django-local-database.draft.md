Title: How to restore your local Django database from a prod backup
Description: How to copy a Postgres database backup into your local database
Slug: restore-django-local-database
Date: 2020-6-14 12:00
Category: Django

It's really nice being able to work on production data from your local Django app. There are a lot of cases where this is quite useful:

- Something weird happens in prod and you want to try reproduce the issue locally
- You want to test a scary custom migration on a copy of prod data before you deploy it
- You want to see how webpage styling changes will when you're using realistic data

In this post I'll show you a script which you can use to pull down the latest Postgres database backup from cloud storage and use it to populate your local database with prod data. This post builds on three previous posts on mine, which might be helpful if you can't follow the scripting in this post:

- [How to backup and restore a Postgres database](https://mattsegal.dev/postgres-backup-and-restore.html)
- [How to automate your Postgres database backups](https://mattsegal.dev/postgres-backup-automate.html)
- [How to automatically reset your local Django database](https://mattsegal.dev/reset-django-local-database.html)

### Other considerations

When talking about using production backups locally, there are two points that I think are important.

First, production data can contain sensitive user information including names, addresses, emails and even credit card details. You need to ensure that this data is only be distributed to people who are authorised to access it, or alternatively the backups should be sanitized so the senitive data is overwritten or removed.

Secondly, I mentioned using database backups to debug issues in production. I think it's a great method for squashing bugs, but it shouldn't be your only way to solve production errors. Before you move onto this technique, you should first ensure you have [application logging](https://mattsegal.dev/file-logging-django.html) and [error monitoring](https://mattsegal.dev/sentry-for-django-error-monitoring.html) set up for your Django app.
