Title: How to view Django logs with Papertrail
Slug: django-logging-papertrail
Date: 2020-04-10 12:00
Category: Django

You have a Django app running on a webserver and hopefully you're [writing your logs to a file](https://mattsegal.dev/file-logging-django.html). If anything goes wrong you can search back through the logs and figure out what happened.

The problem is that to get to your logs, you have to log into your server, find the right file and search through the text on the command line. It's possible to do but it's kind of a pain. Isn't there an easier way to view your Django app's logs? Wouldn't it be nice to search through them on a website?

This post will show you how to push your Django logs into [Papertrail](https://www.papertrail.com/). Papertrail is a free web-based log aggregator that is reasonably simple to set up. It stores ~6 days of searchable logs. It's best for small, simple projects where you don't want to do anything complicated.

<div class="loom-embed"><iframe src="https://www.loom.com/embed/5ede7f70b62645ca82c1ffbf4c0e64eb" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

### Create an account

You can start by going to the [Papertrail website](https://www.papertrail.com/) and creating an account. Once that's done, you can visit [this page](https://papertrailapp.com/systems/setup?type=app&platform=unix), where you'll see a message like this:

> Your logs will go to logs2.papertrailapp.com:41234 and appear in Events.

You need to note down two things from this page:

- The hostname: logs2.papertrailapp.com
- The port: 41234

These two peices of information will determine where Papertrail stores your logs, and they're essentially secrets that should be kept out of public view. Keep the page open, because it'll be useful later.

### Install Papertrail's remote_syslog2

Papertrail uses some tool they've built called `remote_syslog2` to ship logs from your server into their storage. Assuming you're running Ubuntu or Debian, you can download the .deb installation file for remote_syslog2 from GitHub. As of the writing of this post, [this is the latest release deb file](https://github.com/papertrail/remote_syslog2/releases/download/v0.20/remote-syslog2_0.20_amd64.deb).

```bash
# Download installation file to /tmp/
DEB_URL=" https://github.com/papertrail/...deb"
curl --location --silent $DEB_URL -o /tmp/remote_syslog.deb

# Install remote_syslog2 from the file
sudo dpkg -i /tmp/remote_syslog.deb
```

You can read more about remote_syslog [here](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-text-log-files-in-unix/).

### Create logging config

You can configure what logs get sent to Papertrail using a config file. This uses the YAML format and should live at `/etc/log_files.yml`

```yaml
# /etc/log_files.yml
files:
  - /tmp/papertrail-test.log
destination:
  host: logs2.papertrailapp.com
  port: 41234
  protocol: tls
```

### Run Papertrail with a test log file

Start by testing out whether remote_syslog is setup correctly by running it in non-daemonized mode:

```bash
remote_syslog -D --hostname myapp
```

Note that "hostname" can be whatever name you want. You should see some console output like this:

```text
... Connecting to logs2.papertrailapp.com:41234 over tls
... Cannot forward /tmp/papertrail-test.log, it may not exist
```

Make sure you have [this page](https://papertrailapp.com/systems/setup?type=app&platform=unix) open in your web browser (or open it now). In another bash terminal, write some text to papertrail-test.log:

```bash
echo "[$(date)] Test logline" >> /tmp/papertrail-test.log
```

Now you should see, in your remote_syslog terminal, a new message:

```text
... Forwarding file: /tmp/papertrail-test.log
```

When you look at the page you have open, you should see something like:

> Logs received from myapp

If you head to your [dashboard](https://papertrailapp.com/dashboard) you should now see a new system added called "myapp". You should be also able to see your test log messages in the [search panel for myapp](https://my.papertrailapp.com/systems/myapp/events).

### Run Papertrail with real log files

Now that you're happy that Papertrail is able to upload log messages, you can set it up to ship your log files. In this example, I'm going to upload data from the Django and gunicorn log files I created in [this post](https://mattsegal.dev/file-logging-django.html):

```yaml
# /etc/log_files.yml
files:
  - /var/log/django.log
  - /var/log/gunicorn/access.log
  - /var/log/gunicorn/error.log
destination:
  host: logs2.papertrailapp.com
  port: 41234
  protocol: tls
```

When you are not testing with remote_syslog, you want to run it in daemonized mode:

```bash
sudo remote_syslog --hostname myapp
```

You can check that it's still running by looking up its process:

```bash
ps aux | grep remote_syslog
```

If you need to stop it:

```bash
pkill remote_syslog
```

That's it! Now you have remote_syslog running on your server, shipping log data off to Papertrail.
