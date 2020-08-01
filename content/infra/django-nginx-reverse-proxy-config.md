Title: A breakdown of how NGINX is typically configured with Django 
Description: A detailed review of all the NGINX configurations that are typically used with Django
Slug: nginx-django-reverse-proxy-config
Date: 2020-07-31 12:00
Category: DevOps

You are trying to deploy your Django web app to the internet.
You have never done this before, so you follow a guide like [this one](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04).
The guide gives you many instructions, which includes installing and configuring an "NGINX reverse proxy".
At some point you mutter to yourself:

> What-the-hell is an NGINX? Eh, whatever, let's keep reading.

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

Most people do their first Django deployment as a learning exercise.
You want to understand what you are doing, so that you can fix problems if you get stuck
and so you don't need to rely on guides in the future.
In this post I'll break down the elements of this NGINX config and how it ties in with Django,
so that you can confidently debug, update and extend it in the future.

If you have specific questions that aren't covered by this post, I recommend looking at the official NGINX documentation [here](https://docs.nginx.com/nginx/admin-guide/web-server/web-server/).

## What is this file supposed to achieve?

This scary-looking config file sets up NGINX so that it acts as the entrypoint to your Django application.
Explaining _why_ you might choose to use NGINX is a topic too expansive for this post, so I'm just going to stick to explaining
how it works.

First, I'd like to establish that NGINX is completely separate program to your Django app.
NGINX is running inside its own process, while Django is running inside a WSGI server process, such as Gunicorn.
In this post I will sometimes refer to Gunicorn and Django interchangeably.

![nginx as a separate process]({attach}/img/nginx-separate-process.png)

All requests that hit your Django app have to go through NGINX first.


![nginx proxy]({attach}/img/nginx-proxy.png)

NGINX listens for incoming HTTP requests on port 80 and HTTPS requests on port 443. 
When a new request comes in:

- NGINX looks at the request, checks some rules, and sends it on to your WSGI server, which is usually listening on localhost, port 8000
- Your Django app will process the request and eventually produce a response
- Your WSGI server will send the response back to NGINX; and then
-  NGINX will send the response back out to the original requesting client

You can also configure NGINX to serve static files, like images, directly from the filesystem, so that requests for these assets don't need to go through Django

![nginx proxy with static files]({attach}/img/nginx-static-proxy.png)

You can adjust the rules in NGINX so that it selectively routes requests to multiple app servers. You could, for example, run a Wordpress site and a Django app from the same server:

![nginx multi proxy]({attach}/img/nginx-multi-proxy.png)

Now that you have a general idea of what NGINX is supposed to do, let's go over the config file that makes this happen.

## Server block

The top level block in the NGINX config file is the [virtual server](https://docs.nginx.com/nginx/admin-guide/web-server/web-server/#setting-up-virtual-servers).
The main utility of virtual servers is that they allow you to sort incoming requests based on the port and hostname. 
Let's start by looking at a basic server block:

```nginx
server {
    # Listen on port 80 for incoming requests.
    listen 80;
    # Return status code 200 with text "Hello World".
    return 200 'Hello World';
}
```

Let me show you some example requests. Say we're on the same server as NGINX and we send a GET request using the command line tool `curl`.

```bash
curl localhost
# Hello World
``` 

This `curl` command sends the following [HTTP request](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages) to localhost, port 80:

```http
GET / HTTP/1.1
Host: localhost
User-Agent: curl/7.58.0
```

We will get the following HTTP response back from NGINX, with a 200 OK status code and "Hello World" in the body:

```http
HTTP/1.1 200 OK
Content-Type: application/octet-stream
Content-Length: 11

Hello World
```

We can also request some random path inside this virtual server and we get the same result:

```bash
curl localhost/some/path/on/website
# Hello World
``` 

With `curl` sending this HTTP request: 

```http
GET /some/path/on/website HTTP/1.1
Host: localhost
User-Agent: curl/7.58.0
```

and we get back the same response as before:

```http
HTTP/1.1 200 OK
Content-Type: application/octet-stream
Content-Length: 11

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
You can set up a particular virtual server to be the default choice (`default_server`) if no other ones match the incoming request. You can use this feature to host multiple
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
```

Let's try setting the `Host` header to `foo.com`:

```bash
curl localhost --header "Host: foo.com"
# Welcome to foo.com!
```

We were directed to the `foo.com` virtual server because we sent the correct `Host` header in our request:

```http
GET / HTTP/1.1
Host: foo.com
User-Agent: curl/7.58.0
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
For example, if your WSGI server was running on localhost (which has IP 127.0.0.1), port 8000, then you would use this config:

```nginx
server {
    listen 80;
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

You can also point `proxy_pass` at a [Unix domain socket](https://en.wikipedia.org/wiki/Unix_domain_socket#:~:text=A%20Unix%20domain%20socket%20or,the%20same%20host%20operating%20system.), with Gunicorn listening on that socket, which is very similar to using localhost except it doesn't use up a port number and it's a bit faster:

```nginx
server {
    listen 80;
    location / {
        proxy_pass http://unix:/home/user/my-socket-file.sock;
    }
}
```

Seems simple enough - you just point NGINX at your WSGI server, so... what was all that other crap? Why do you set `proxy_set_header` and `proxy_redirect`? That's what we'll discuss next.

## NGINX is lying to you

As a reverse proxy, NGINX will receive HTTP requests from clients and then send those requests to our Gunicorn WSGI server.
The problem is that NGINX hides information from our WSGI server. The HTTP request that Gunicorn receives is not the same as the one that NGINX received from the client.

![nginx hiding info]({attach}/img/nginx-hide-info.png)

Let me give you an example, which is illustrated above. You, the client, have an IP of `12.34.56.78` and you go to `https://foo.com` in your web browser and try to load the page. The request hits the server on port 443 and is read by NGINX. At this stage, NGINX knows that:

- the protocol is [HTTPS](https://www.cloudflare.com/learning/ssl/what-is-https/)
- the client has an IP address of `12.34.56.78`
- the request is for the host `foo.com`

NGINX then sends the request onwards to Gunicorn. When Gunicorn receives this request, it thinks:

- the protocol is HTTP, not HTTPS, because the connection between NGINX and Gunicorn is not encrypted
- the client has the IP address `127.0.0.1`, because that's the address NGINX is using
- the host is `127.0.0.1:8000` because NGINX said so

Some of this lost information is useful, and we want to force NGINX to send it to our WSGI server. That's what these lines are for:

```nginx
proxy_set_header Host $host;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

Next, I will explain each line in more detail.

## Setting the Host header

Django would like to know the value of the `Host` header so that various bits of the framework, like [ALLOWED_HOSTS](https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts) or [HttpRequest.get_host](https://docs.djangoproject.com/en/3.0/ref/request-response/#django.http.HttpRequest.get_host) can work. The problem is that NGINX does not pass the `Host` header to proxied servers by default.

For example, when I'm using `proxy_pass` like I did in the previous section, and I send a request with the `Host` header to NGINX like this:

```bash
curl localhost --header "Host: foo.com"
```

Then NGINX receives the HTTP request, which looks like this:

```http
GET / HTTP/1.1
Host: foo.com
User-Agent: curl/7.58.0
```

and then NGINX sends a HTTP request to your WSGI server, like this:

```http
GET / HTTP/1.0
Host: 127.0.0.1:8000
User-Agent: curl/7.58.0
```

Notice something? That rat-fuck-excuse-for-a-webserver sent different headers to our WSGI server!
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
User-Agent: curl/7.58.0
```

Gunicorn will read this `Host` header and provide it to you in your Django views via the `request.META` object:

```python
# views.py
def my_view(request):
    host = request.META['HTTP_HOST']
    print(host)  # Eg. "foo.com"
    return HttpResponse(f"Got host {host}")

```

## Setting the X-Forwarded-Whatever headers

The `Host` header isn't the only useful information that NGINX does not pass to Gunicorn. We would also like the protocol and source IP address of the client request
to be passed to our WSGI server. We achieve this with these two lines:

```nginx
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

I just want to point out that these header names are completely arbitrary. You can send any header you want with the format `X-Insert-Words-Here` to Gunicorn and it will parse it and send it onwards to Django. For example, you could set the header to be `X-Matt-Is-Cool` as follows:

```nginx
proxy_set_header X-Matt-Is-Cool 'it is true';
```

Now NGINX will include this header with every request it sends to Gunicorn. When Gunicorn parses the HTTP request it reads **any** header with the format `X-Insert-Words-Here` into a Python dictionary, which ends up in the `HttpRequest` object that Django passes to your view. So in this case, `X-Matt-Is-Cool` gets turned into the key `HTTP_X_MATT_IS_COOL` in your request object. For example:

```python
# views.py
def my_view(request):
    # Prints value of X-Matt-Is-Cool header included by NGINX
    print(request.META["HTTP_X_MATT_IS_COOL"])  # it is true
    return HttpResponse("Hello World")
```

This means you can add in whatever custom headers you like to your NGINX config, but for now let's focus on getting the protocol and client IP address to your Django app.

## Setting the X-Forwarded-Proto header

Django sometimes needs to know whether the incoming request is secure (HTTPS) or not (HTTP). For example, some features of the [SecurityMiddleware](https://docs.djangoproject.com/en/3.0/ref/middleware/#http-strict-transport-security) class checks for HTTPS. The problem is, of course, that NGINX is _always_ telling Django that the client's request to the sever is not secure, even when it is.  This problem always crops up for me when I'm implementing pagination, and the "next" URL has `http://` instead of `https://` like it should.  

Our fix for this is to put the client request protocol into a header called `X-Forwarded-Proto`:

```nginx
proxy_set_header X-Forwarded-Proto $scheme;
```

Then you need to set up the [SECURE_PROXY_SSL_HEADER](https://docs.djangoproject.com/en/3.0/ref/settings/#secure-proxy-ssl-header) setting to read this header in your `settings.py` file:

```python
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

Now Django can tell the difference between incoming HTTP requests and HTTPS requests. 


## Setting the X-Forwarded-For header

Now let's talk about determining the client's IP address. As mentioned before, NGINX will always lie to you and say that the client IP address is `127.0.0.1`.
If you don't care about client IP addresses, then you don't care about this header. You don't need to set it if you don't want to. Knowing the client IP might be useful sometimes. For example, if you want to guess at where they are located, or if you are building one of those [_What's My IP?_](https://www.expressvpn.com/what-is-my-ip) websites:

![some website knows my ip address]({attach}/img/my-ip.png)


You can set the [X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For) header to tell Gunicorn the original IP address of the client: 

```nginx
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

As described earlier, the header `X-Forwarded-For` gets turned into the key `HTTP_X_FORWARDED_FOR` in your request object. For example:

```python
# views.py
def my_view(request):
    # Prints client IP address: "12.34.56.78"
    print(request.META["HTTP_X_FORWARDED_FOR"])
    # Prints NGINX IP address: "127.0.0.1", ie. localhost
    print(request.META["REMOTE_ADDR"])
    return HttpResponse("Hello World")
```

Does this seem kind of underwhelming? Maybe a little pointless? As I said before, if you don't care about client IP addresses, then this header isn't for you.


## Proxy redirect

Let's cover the final line of the Django reverse proxy config: `proxy_redirect`.
The NGINX docs for this directive are [here](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_redirect).

```nginx
proxy_redirect http://127.0.0.1:8000 http://foo.com;
```

This directive is used when handling redirects that are issued by Django.
For example, you might have a webpage that used to live at path `old/page/`, but you moved it to `new/page/`.
You want to send any user that asked for `old/page/` to `new/page/`. 
To achieve this you could write a Django view like this:

```python
# view.py
def redirect_view(request):
    return HttpResponseRedirect("new/page/")

```

When a user asks for `old/page/`, this view will send them a HTTP response with a 302 redirect status code:

```http
HTTP/1.1 302 Found
Location: new/page/
```

Your web browser will follow the `Location` response header to the new page.
A problem occurs when your Django app includes the WSGI server's address and port in the `Location` header:

```http
HTTP/1.1 302 Found
Location: http://127.0.0.1:8000/new/page/
```

This is a problem because the client's browser will try to go to that address, and it will fail because the WSGI server is not
on the same server as the client.

Here's the thing: I have never actually seen this happen, and I'm having trouble thinking of a common scenario where this would happen.
Send me an email if you know where this issue crops up. Anyway, using `proxy_redirect` helps in the hypothetical case where Django does include the WSGI address
in a redirect's `Location` header.

The directive rewrites the header using the syntax:

```nginx
proxy_redirect redirect replacement
```

So, for example, if there was a redirect response like this:

```http
HTTP/1.1 302 Found
Location: http://127.0.0.1:8000/new/page/
```

and you set up your `proxy_redirect` like this 

```nginx
proxy_redirect http://127.0.0.1:8000 https://foo.com/blog/;
```

then the outgoing response would be re-written to this:

```http
HTTP/1.1 302 Found
Location: https://foo.com/blog/new/page/
```

I guess this directive might be useful in some situations? I'm not really sure.

## Static block

Earlier I mentioned that NGINX can serve static files directly from the filesystem.

![nginx proxy with static files]({attach}/img/nginx-static-proxy.png)

This is a good idea because NGINX is much more efficient at doing this than your WSGI server will be.
It means that your server will be able to respond faster to static file request and handle more load.
You can use [this technique](https://docs.djangoproject.com/en/3.0/howto/static-files/deployment/#serving-static-files-in-production) to put all of your
Django app's static files into a folder like this:

```text
/home/myuser/myproject 
└─ static               Your static files
    ├─ styles.css       CSS file
    ├─ main.js          JavaScript file
    └─ cat.png          A picture of a cat
```

Then you can set the `/static/` location to serve files from this folder: 

```nginx
location /static/ {
    root /home/myuser/myproject;
}
```

Now a request to `http://localhost/static/cat.png` will cause NGINX to read directly from `/home/myuser/myproject/static/cat.png`, without sending a request to the WSGI server.

## Next steps

weirdly hard to navigate and google search
https://docs.nginx.com/nginx/admin-guide/web-server/web-server/

simple django deployment
nginx logs article


If you want to take a 40 minute side-quest I recommend checking out Brian Will's "The Internet" videos to learn more about what HTTP, TCP, and ports are: [part 1](https://www.youtube.com/watch?v=DTQV7_HwF58), [part 2](https://www.youtube.com/watch?v=3fvUc2Dzr04&t=167s), [part 3](https://www.youtube.com/watch?v=_55PyDw0lGU), [part 4](https://www.youtube.com/watch?v=yz3lkSqioyU).
