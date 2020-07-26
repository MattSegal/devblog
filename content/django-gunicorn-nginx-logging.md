Title: How to manage logs with Django, Gunicorn and NGINX
Description: An overview of the logging options available when using Django, Gunicorn and NGINX
Slug: django-gunicorn-nginx-logging
Date: 2020-07-26 12:00
Category: Django

So you want to run a Django app using NGINX and Gunicorn.
Did you notice that _all three_ of these tools have logging options?
You can configure [Django logging](https://docs.djangoproject.com/en/3.0/topics/logging/), 
[Gunicorn logging](https://docs.gunicorn.org/en/latest/settings.html#errorlog), and [NGINX logging](https://docs.nginx.com/nginx/admin-guide/monitoring/logging/).

You just want to see what's happening in your Django app so that you can fix bugs. How are you supposed to set these logs up? What are they all for?
In this post I'll give you a brief overview of your logging options with Django, Gunicorn and NGINX, so that you don't feel so confused and overwhelmed.

I've previously written a short guide on [setting up file logging](https://mattsegal.dev/file-logging-django.html) with Django if you just want quick instructions on what to do. 

### NGINX logging

NGINX allows you to set up [two log files](https://docs.nginx.com/nginx/admin-guide/monitoring/logging/), access_log and error_log. I usually configure them like this in my `/etc/nginx/nginx.conf` file:

```text
access_log /var/log/nginx/access.log;
error_log /var/log/nginx/error.log;
```

### NGINX access logs

The NGINX access_log is a file which records of all the requests that are coming in to your server via NGINX. It looks like this:

``` text
123.45.67.89 - - [26/Jul/2020:04:55:28 +0000] "GET / HTTP/1.1" 200 906 "-" "Mozilla/5.0 ... Chrome/98 Safari/537.4"
123.45.67.89 - - [26/Jul/2020:05:06:29 +0000] "GET / HTTP/1.1" 200 904 "-" "Mozilla/5.0 ... Chrome/98 Safari/537.4"
123.45.67.89 - - [26/Jul/2020:05:10:33 +0000] "GET / HTTP/1.1" 200 904 "-" "Mozilla/5.0 ... Chrome/98 Safari/537.4"
123.45.67.89 - - [26/Jul/2020:05:21:33 +0000] "GET / HTTP/1.1" 200 910 "-" "Mozilla/5.0 ... Chrome/98 Safari/537.4"
123.45.67.89 - - [26/Jul/2020:05:25:37 +0000] "GET / HTTP/1.1" 200 907 "-" "Mozilla/5.0 ... Chrome/98 Safari/537.4"
```

There's a new line for each request that comes in. Breaking a single like down:

```text
123.45.67.89 - - [26/Jul/2020:04:55:28 +0000] "GET / HTTP/1.1" 200 906 "-" "Mozilla/5.0 ... Chrome/98 Safari/537.4"
```

From this line can see:

- the IP is 123.45.67.89
- the request arrived at 26/Jul/2020:04:55:28 +0000
- the HTTP request method was GET
- the path requested was /
- the version of HTTP used was HTTP/1.1
- the status code returned by the server was "200" (ie. [OK](https://http.cat/))
- the requester's [user agent](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent) was "Mozilla/5.0 ... Chrome/98 Safari/537.4"

This is _very_ useful information to have when debugging issues in production, and I recommend you enable these access logs in NGINX.
You can quickly view these logs using `tail`:

```bash
# View last 5 log lines
tail -n 5 /var/log/nginx/access.log
# View last 5 log lines and watch for new ones
tail -n 5 -f /var/log/nginx/access.log
```

In addition to legitimate requests to your web application, NGINX will also log all of the spam, crawlers, and hacking attempts that hit your webserver.
If you have your server accessible via the internet, then you will get garbage requests like this in your access log: 

```text
195.54.160.21 - - [26/Jul/2020:03:58:25 +0000] "POST /vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php HTTP/1.1" 404 564 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
```

I assume this is a bot trying to hack an old version of PHP (which I do not run on this server).

### NGINX error logs

NGINX also logs errors to error_log, which can occur when you've messed up your configuration somehow, or if your Gunicorn server is unresponsive. This file is also useful for debugging so I recommend you include it as well in your NGINX config. You get error messages like this:

```text
2020/07/25 08:14:57 [error] 32115#32115: *44242 connect() failed (111: Connection refused) while connecting to upstream, client: 11.22.33.44, server: www.example.com, request: "GET /admin/ HTTP/1.1", upstream: "http://127.0.0.1:8000/admin/", host: "clerk.anikalegal.com", referrer: "https://www.example.com/admin/"
```

### Gunicorn logging

Gunicorn has [two main logfiles](https://docs.gunicorn.org/en/latest/settings.html#errorlog) that it writes, the error log and the access log.
You can configure the log settings through the [command line](https://docs.gunicorn.org/en/latest/configure.html#command-line) or a [config file](https://docs.gunicorn.org/en/latest/configure.html#configuration-file). I recommend using the config file because it's easier to read.

### Gunicorn access logs

The Gunicorn access log is very similar to the NGINX access log, it records all the requests coming in to the Gunicorn server:

```text
10.255.0.2 - - [26/Jul/2020:05:10:33 +0000] "GET /foo/ HTTP/1.0" 200 1938 "-" "Mozilla/5.0 ... (StatusCake)"
10.255.0.2 - - [26/Jul/2020:05:25:37 +0000] "GET /foo/ HTTP/1.0" 200 1938 "-" "Mozilla/5.0 ... (StatusCake)"
10.255.0.2 - - [26/Jul/2020:05:40:42 +0000] "GET /foo/ HTTP/1.0" 200 1938 "-" "Mozilla/5.0 ... (StatusCake)"
```

I think you may as well enable this so that you can debug issues where you're not sure if NGINX is sending requests to Gunicorn properly.

### Gunicorn error logs

The Gunicorn error log is a little bit more complicated. By default it contains information about what the Gunicorn server is doing, like starting up and shutting down:

```text
[2020-04-06 06:17:23 +0000] [53] [INFO] Starting gunicorn 20.0.4
[2020-04-06 06:17:23 +0000] [53] [INFO] Listening at: http://0.0.0.0:8000 (53)
[2020-04-06 06:17:23 +0000] [53] [INFO] Using worker: sync
[2020-04-06 06:17:23 +0000] [56] [INFO] Booting worker with pid: 56
[2020-04-06 06:17:23 +0000] [58] [INFO] Booting worker with pid: 58
```

You can change how verbose these messages are using the "[loglevel](https://docs.gunicorn.org/en/latest/settings.html#loglevel)" setting, which can be set to log more info using the "debug" level, or only errors, using the "error" level, etc.

Finally, and importantly there is the "[capture_output](https://docs.gunicorn.org/en/latest/settings.html#capture-output)" logging setting, which is a boolean flag.
This setting will take any stdout/stderr, which is to say print statements, log messages, warnings and errors from your Django app, and log then to the Gunicorn error file. 
I like to keep this setting enabled so that I can catch any random output that is falling through from Django to Gunicorn.
Here is an example Gunicorn config file with logging set up:

```python
# gunicorn.conf.py
# Non logging stuff
bind = "0.0.0.0:80"
workers = 3
# Access log - records incoming HTTP requests
accesslog = "/var/log/gunicorn.access.log"
# Error log - records Gunicorn server goings-on
errorlog = "/var/log/gunicorn.error.log"
# Whether to send Django output to the error log 
capture_output = True
# How verbose the Gunicorn error logs should be 
loglevel = "info"
```

You can run Gunicorn using config like this as follows:

```bash
gunicorn myapp.wsgi:application -c /some/folder/gunicorn.conf.py
```

### Django logging

Django logging refers to the output of your Django application. The kind of messages you see printed by `runserver` in development. Stuff like this:

```text
Sending Thing<b5d1854b-7efc-4c67-9e9b-a956c10e5b86]> to Google API
Google API called failed: {'error_description': 'You failed hahaha'}
Traceback (most recent call last):
  File "/app/google/api/base.py", line 102, in _handle_json_response
    resp.raise_for_status()
  File "/usr/local/lib/python3.6/dist-packages/requests/models.py"
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 403 Client Error
Setting expired tokens to inactive: []
```

I discuss Django logging in more detail in [this guide](https://mattsegal.dev/file-logging-django.html), but I will give you a brief summary here.
Django uses the same conventions as Python's standard library [logging](https://docs.python.org/3/library/logging.html) module, which is kind of a pain to learn, but valuable to know.
The Django docs provide a nice overview of logging config [here](https://docs.djangoproject.com/en/3.0/topics/logging/).

I think you have two viable options for your Django logging:

- Set up Django to log everything to stdout/stderr using the `StreamHandler` and capture the output using Gunicorn via the capture_output option, so that your Django logs end up in the Gunicorn error logfile
- Set up Django to log to a file using `FileHandler` so you can keep your Django and Gunicorn logs separate

I personally prefer option #2, but you whatever makes you happy.


### Next steps

I encourage you to set up the logging described in this post, so that you don't waste hours trying to figure out what is causing bugs in production.
I also recommend that you configure error alerting with Django, with [Sentry](https://mattsegal.dev/sentry-for-django-error-monitoring.html) being a strong choice.

Finally, if you're having other difficulties getting your Django app onto the internet, then check out my guide on [Django deployment](https://mattsegal.dev/simple-django-deployment.html)