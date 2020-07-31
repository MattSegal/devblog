Title: A breakdown of how NGINX is typically configured with Django 
Description: xxxxxxxxxxxxxxxxxxxxxxxx
Slug: nginx-django-reverse-proxy-config
Date: 2020-07-31 12:00
Category: DevOps

You are trying to deploy your Django web app to the internet.
You have never done this before:, so you follow a guide like [this one](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04).
The guide gives you many instructions, which includes installing and configuring an "NGINX reverse proxy".
At some point you mutter to yourself:

> What the fuck is an NGINX? Eh, whatever, let's keep reading.

You will have to copy-paste some weird gobbledygook into a file, which looks like this:

```nginx
# NGINX site config file at /etc/nginx/sites-available/myproject
server {
    listen 80;
    server_name www.example.com;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect http://127.0.0.1:8000 http://www.example.com;
    }
    location /static/ {
        root /home/myuser/myproject;
    }
}
```

What is all this stuff? What is it supposed to do?
How do you know if it will work?

Most people do their first Django deployment as a learning exercise.
You want to understand what you are doing, so that you can fix problems if you get stuck
and so you don't need to rely on guides in the future.
In this post I'll break down the elements of this config and how it ties in with Django,
so that you can confidently debug, update and extend it in the future.

If you have specific questions that aren't covered by this post, I recommend looking at the official NGINX documentation [here](https://docs.nginx.com/nginx/admin-guide/web-server/web-server/).

## What is this file supposed to achieve?

This scary-looking config file sets up NGINX so that it acts as the entrypoint to your Django application.
Explaining why you might choose to use NGINX is a topic too expansive for this post, so I'm going to stick to just explaining
what it is doing.

First, I'd like to establish that NGINX is completely separate program to your Django app.
NGINX is running inside its own process, while Django is running inside a WSGI server process, such as Gunicorn.

![nginx as a separate process]({attach}/img/nginx-separate-process.png)

All requests that hit your Django app have to go through NGINX first.


![nginx proxy]({attach}/img/nginx-proxy.png)

NGINX listens for incoming HTTP requests on port 80 and HTTPS requests on port 443. 
When a new request comes in:

- NGINX looks at the request, checks some rules, and sends it on to your WSGI server, which is usually listening on localhost, port 8000
- Your Django app will process the request and eventually produce a response
- Your WSGI server will send the response to NGINX; and then
-  NGINX will send the response back out to the original requesting user

You can also configure it to serve static files, like images, directly from the filesystem, so requests for these assets don't need to go through Django

![nginx proxy with static files]({attach}/img/nginx-static-proxy.png)

You can adjust the rules in NGINX so that it selectively routes requests to multiple app servers. You could, for example, run a Wordpress site and a Django app from the same server:

![nginx multi proxy]({attach}/img/nginx-multi-proxy.png)

Now that you have a general idea of what NGINX is supposed to do, let's go over the config file that makes this happen.

## Server block

The top level block in the NGINX config file is the [virtual server](https://docs.nginx.com/nginx/admin-guide/web-server/web-server/#setting-up-virtual-servers).
The main utility of virtual servers is that they allow you to sort incoming requests based on the port and hostname. 
Let's start by looking at the most basic server block possible:

```nginx
server {
    # Listen on port 80 for incoming requests.
    listen 80;
    # Return status code 200 with text "Hello World".
    return 200 'Hello World';
}
```

Let me show you some example requests. Say we're on the same server as NGINX and we send some requests using `curl`.

```bash
curl localhost
# Hello World
``` 

This command sends the following [HTTP request](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages) to localhost, port 80:

```http
GET / HTTP/1.1
Host: localhost
User-Agent: curl/7.58.0
Accept: */*
```

We get the following response back from NGINX, with a 200 OK status code and "Hello World" in the body:

```http
HTTP/1.1 200 OK
Date: Fri, 31 Jul 2020 07:15:49 GMT
Content-Type: application/octet-stream
Content-Length: 11
Connection: keep-alive

Hello World
```

We can also request some random path inside this virtual server... same result:

```bash
curl localhost/some/path/on/website
# Hello World
``` 

With `curl` sending this HTTP request: 

```http
GET /some/path/on/website HTTP/1.1
Host: localhost
User-Agent: curl/7.58.0
Accept: */*
```

and we get back the same response as before:

```http
HTTP/1.1 200 OK
Date: Fri, 31 Jul 2020 07:34:47 GMT
Content-Type: application/octet-stream
Content-Length: 11
Connection: keep-alive

Hello World
```

Simple so far, but not very interesting, let's start to mix it up with multiple server blocks.

## Multiple virtual servers

You can add more than one virtual server in NGINX:

```nginx
# All requests to foo.com return a 200 OK status code
server {
    listen 80;
    server_name foo.com;
    return 200 'Welcome to foo.com!';
}

# Any other requests get a 404 Not Found page
server {
    listen 80 default_server;
    return 404;
}
```

NGINX uses the `server_name` directive to check the `Host` header of incoming requests and match the request to a virtual server. Your web browser will usually set this header automatically for you.
You can set up a particular virtual server to be the default choice if no other virtual servers match. You can use this feature to host multiple
Django apps on a single server. All you need to do is [set up your DNS](https://mattsegal.dev/dns-for-noobs.html) to get multiple domain names to point to a single server, and then add a virtual server for each Django app.

Let's test out the config above. If send a request to `localhost`, we'll get a 404 status code from the default server:

```bash
curl localhost
# <html>
#   <head><title>404 Not Found</title></head>
#   ...
# </html>
```

We got the default server because the `Host` header we sent didn't match `foo.com`:

```http
GET / HTTP/1.1
Host: localhost
User-Agent: curl/7.58.0
Accept: */*
```

Let's try setting the `Host` header to `foo.com`:

```bash
curl localhost --header "Host: foo.com"
# Welcome to foo.com!
```

We got directed to the foo.com virtual server because we sent the correct `Host` header in our request:

```http
GET / HTTP/1.1
Host: foo.com
User-Agent: curl/7.58.0
Accept: */*
```

Finally, we can see that setting a random `Host` header sends us to the default server:

```bash
curl localhost --header "Host: fasfsadfs.com"
# <html>
#   <head><title>404 Not Found</title></head>
#   ...
# </html>
```

There's [more](https://docs.nginx.com/nginx/admin-guide/web-server/web-server/#setting-up-virtual-servers) that you can do with virtual servers in NGINX,
but what we've covered so far should be enough for you to understand their typical usage with Django. 

## Location blocks

Within a virtual server you can route the request based on the requested path.

```nginx
server {
    listen 80;
    # Requests to the root path get a 200 OK response
    location / {
        return 200 'Cool!';
    }
    # Requests to /forbidden get 403 Forbidden response
    location /forbidden {
        return 403;
    }
}
```

Under this configuration, any request that doesn't match `/forbidden` will return a 403 Forbidden status code, and everything else will return _Cool!_ Let's try it out:

```bash
curl localhost
# Cool!
curl localhost/blah/blah/blah
# Cool!
curl localhost/forbidden
# <html>
# <head><title>403 Forbidden</title></head>
# ...
# </html>

curl localhost/forbidden/blah/blah/blah
# <html>
# <head><title>403 Forbidden</title></head>
# ...
# </html>
```

Now that we've covered `server` and `location` blocks it should be easier to make sense of some of the config that I showed you at the start of this post:

```nginx
server {
    listen 80;
    server_name www.example.com;
    location / {
        # Do something...
    }
    location /static/ {
        # Do something...
    }
}
```

Next we'll dig into the connection between NGINX and our WSGI server.

## Reverse proxy location

As mentioned earlier, NGINX acts as a [reverse proxy](https://en.wikipedia.org/wiki/Reverse_proxy#:~:text=In%20computer%20networks%2C%20a%20reverse,from%20the%20proxy%20server%20itself.) for Django:

![nginx proxy]({attach}/img/nginx-proxy.png)


This reverse proxy setup is configured within this location block:

```nginx
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_redirect http://127.0.0.1:8000 http://www.example.com;
}
```

In the next few sections I will break down the directives in this block so that you understand what is going on. 
You might also find the NGINX documentation on [reverse proxies](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) helpful for understanding this config.

## Proxy pass

The `proxy_pass` directive tells NGINX to send all requests for that location to the specified address.
For example, if your WSGI server was running on 127.0.0.1 / localhost, port 8000, then you would use this config:

```nginx
server {
    listen 80;
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

You can also point proxy pass at a [Unix domain socket](https://en.wikipedia.org/wiki/Unix_domain_socket#:~:text=A%20Unix%20domain%20socket%20or,the%20same%20host%20operating%20system.), with Gunicorn listening on that socket, which is very similar to using localhost except it doesn't use up a port number and it's a bit faster:

```nginx
server {
    listen 80;
    location / {
        proxy_pass http://unix:/home/user/my-socket-file.sock;
    }
}
```

Seems simple enough - you just point NGINX at your WSGI server, so... what was all that other crap? Why do you set `proxy_set_header` and `proxy_redirect`? That's what we'll discuss next.

## Setting the Host header

Django would like to know the value of the Host header so that various bits of the framework, like [ALLOWED_HOSTS](https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts) or [HttpRequest.get_host](https://docs.djangoproject.com/en/3.0/ref/request-response/#django.http.HttpRequest.get_host) can function. The problem is that NGINX does not pass the Host header to proxied servers by default.

For example, when I'm using `proxy_pass` like I did in the previous section, and I send a request with the `Host` header like this:

```bash
curl localhost --header "Host: foo.com"
```

Then NGINX receives the request, which looks like this:

```http
GET / HTTP/1.1
Host: foo.com
User-Agent: curl/7.58.0
Accept: */*
```

and then NGINX sends a request to your WSGI server, like this:

```http
GET / HTTP/1.0
Host: 127.0.0.1:8000
Connection: close
User-Agent: curl/7.58.0
Accept: */*
```

Notice something? That rat-fuck-excuse-for-a-webserver sent different headers to our WSGI server! What the fuck? Right?
I'm sure there is a good reason for this behaviour, but it's not what we want because it breaks some Django functionality.
We can fix this by using the `proxy_set_header` as follows:


```nginx
server {
    listen 80;
    location / {
        proxy_pass http://127.0.0.1:8000;
        # Ensure original Host header is forwarded to our Django app.
        proxy_set_header Host $host;
    }
}
```

Now NGINX will send the desired headers to Django:

```http
GET / HTTP/1.0
Host: foo.com
Connection: close
User-Agent: curl/7.58.0
Accept: */*
```

## Setting the X-Forwarded-For header

```nginx
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```
## Setting the X-Forwarded-Proto header

```nginx
proxy_set_header X-Forwarded-Proto $scheme;
```
## Proxy redirect

```nginx
proxy_redirect http://127.0.0.1:8000 http://www.example.com;
```

## Static block

```nginx
location /static/ {
    root /home/myuser/myproject;
}
```
## Next steps

weirdly hard to navigate and google search
https://docs.nginx.com/nginx/admin-guide/web-server/web-server/

simple django deployment
nginx logs article
