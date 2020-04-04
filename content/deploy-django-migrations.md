Title: How to deploy Django migrations
Slug: deploy-django-migrations
Date: 2020-04-4 12:00
Category: Django

You've started learning Django, you've created a new Django app and you've deployed it to a Linux webserver in the cloud somewhere. It's all set up and running nicely. Now you want to make some more changes and you need to update your models.

How do you deploy those model changes? How do you get those change sinto your production database?

First I'll show you a simple way to run your migrations on a deloyed Django app with a worked example, then I'll discuss some more advanced considerations.

### Simple method

This simple method is how I like to run migrations. It's for when your web app:

- is a personal project
- has low traffic
- is only used by internal staff members

Basically any situation where a few seconds of downtime isn't that important.

#### Update your model

First you need to make the changes you want to your model class.

```python

class Person(models.Model):
    """A human person"""
    name = models.CharField(max_length=128)
    height = models.FloatField()
    # Add new attribute "weight"
    weight = models.FloatField()

```

#### Create the migration script locally

Once that is done, you want to use Django's command-line managment script `makemigrations` to auto-generate the migrations script.

```bash
./manage.py makemigrations
```

You should see a new file in your app's migrations folder. It'll have some whacky name like `0002_auto_20170219_2310.py`. If you're using Git, don't forget to commit this file.

#### Run the migration script locally

The `makemigrations` command only generates a script which applies your models changes to the database. To actually run that code and apply the changes, you need to run the `migrate` script:

```bash
./manage.py migrate
```

#### Check nothing broke

After you've done that, you should do some testing to make sure that the migrations actually worked. Check the admin panel to see that the model has changed in your local database, test out your app to see that you haven't broken any existing functionality. If you've got automated tests, run them. Once you're happy that it's all good, move on.

#### Deploy the migrations

Now that you've generated your migration script it's time to apply it to the production database:

- Copy all your new code onto the server. Ideally instead of just picking single files, just copy all the .py files in your project to make sure you didn't miss anything
- Stop your WSGI server
- Delete all of the old code on the server, including any .pyc files
- Move the new code to where the old code was
- Apply your migrations with `./manage.py migrate`
- Start your WSGI server again

#### Why delete all the old code?

It might seem scary deleting all your deployed code and replacing it, but the alternative of just uploading a few files is even more risky. You could miss:

- The auto-generated migration file
- The model file that you changed
- Any other code that you've updated which depends on the updated model

It's best to just nuke everything and start from scratch. This will ensure that your production code stays the same as your development code.

#### Is this the best way to do it?

The good thing about this method is that you don't have to worry about keeping your migrations backwards compatible. Sometimes your model changes will break your old code, but not your new code, like when you remove a field from a Django model. This method will keep you from running into that issue.

BUT, following these steps will take your site down for a few seconds, which is fine for a lot of cases, but is bad if any downtime is unnacceptable.

Websites that need to always stay up usually use a method called ["blue-green" deployments](https://rollout.io/blog/blue-green-deployment/), where there are many severs running at once.

If you are doing blue-green deployments, this method will not work, and you will need to construct and deploy [backwards-compatible migrations](https://gist.github.com/majackson/493c3d6d4476914ca9da63f84247407b).

Don't invent problems for yourself though, keep your process simple if you can.
