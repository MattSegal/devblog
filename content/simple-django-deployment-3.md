Title: Simple django deployment part three: deploy code
Description: How to get your Django code running on the server
Slug: simple-django-deployment-3
Date: 2020-04-26 15:00
Category: Django

We've got our server set up, and our Django code is ready.
Now we can actually deploy Django to our server.
The goal of this section is to get a basic deployment done.
We'll do some automation and introduce some extra tools later.

In this section we'll cover:

- Windows line endings
- Uploading and running your Django app

### Windows line endings

A quick aside before we start deploying: Windows line endings. These are the curse of every Django developer running Windows.
This is one of those technical details that you never want to know about, but they'll bite you in the ass if you ignore them.

The TLDR is that in Linux and MacOS, lines end with the "\n" character.
On Windows lines end with "\r\n", because fuck-you-that's-why.
The problem is that your Windows Python files will fail on Linux because they have the wrong line endings.

There are several ways to fix this, including writing our own custom bash or Python scripts to convert these line endings, but for simplicity we'll just use an off-the-shelf tool called [dos2unix](https://linux.die.net/man/1/dos2unix), which I'll show you later.

You can help avoid this problem in VSCode by selecting the "LF" option instead of "CRLF" for the "End of Line Sequence" setting, which is visible in the toolbar on the bottom right hand corner of your screen.

# Uploading and running your Django app

Let's upload our code to the server and set up our app so we can run it. There are lots of ways to do get your code onto the server: scp, rsync, git. I'm going to stick to using scp to limit the number of new tools needed to do this.

Currently our Django project, on our local machine, looks like this:

```text
/django-deploy
├── env                     Python 3 virtualenv
├── requirements.txt        Python requirements
├── db.sqlite3              Local SQLite database
└── tute                    Django project code
    ├── tute                Django app code
    ├── counter             Django app code
    └── manage.py           Django management script
```

When we upload our code, we're going to put it in the root user's home directory - /root/. It'll look like this:

```text
/root
└── deploy                  All uploaded code
    ├── requirements.txt    Python requirements
    └── tute                Django project code
        ├── tute            Django app code
        ├── counter         Django app code
        └── manage.py       Django management script
```

Then we'll be creating a directory called /app/, which will be the final resting place of our code,
and we will set up our project like this:

```text
/app
├── env                     Python 3 virtualenv
├── requirements.txt        Python requirements
├── db.sqlite3              Production SQLite database
└── tute                    Django project code
    ├── tute                Django app code
    ├── counter             Django app code
    ├── staticfiles         Collected static files
    └── manage.py           Django management script
```

A key idea is that every time we re-deploy our code in the future, we want to delete and re-create the folder /app/tute,
but we want to keep the database (db.sqlite3), or else we lose all our production data.

What I'm going to show you now is a very manual process, we will automate this later.

<div class="loom-embed"><iframe src="https://www.loom.com/embed/de3cbdca8ec146dd80f3e5136636b3ea" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

So to recap, the testing we just did looks like this:

![gunicorn http]({attach}gunicorn-server-http.png)

We're most of the way there! We've got our Django app running our server.
There's just a bit more to go before it's fully deployed.

### Next steps

To really say that our app is "deployed", we need it to run even when we're not around.
In the next section, we'll learn how to [run Django in the background]({filename}/simple-django-deployment-4.md)
