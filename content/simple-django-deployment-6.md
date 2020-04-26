Title: Simple Django deployment part six: domain setup
Description: Setup your Django app's domain name
Slug: simple-django-deployment-6
Date: 2020-04-26 18:00
Category: Django

We're very nearly done deploying our Django app. There's just one more thing we should take care of.
Having a raw IP as our website address is kind of yucky, isn't it?
You're not going to ask your friend, boss, or mum to visit 23.231.147.88 to check out your cool new Django app.
You want a domain name like mycoolwebsite.xyz! Let's finish up our deployment by setting up a domain for our web app.

Here we will learn how to:

- Buy a domain name
- Set up a Cloudflare reverse-proxy
- Adding our domain name to Django prod settings
- Test our setup

A quick note before we start - usually you would do this at the start of the process, right after you create your server,
because setting domain name records can take a long time. The reason we're doing it last in this guide is to make sure that you're confident that your app is working before we start fiddling with DNS. If you've never heard of DNS before, I did a short [blog post](https://mattsegal.dev/dns-for-noobs.html) that explains the basics.

### Buy a domain name

If you already own a domain name for your app your can skip this step.
To get a domain name we need to give someone some money.
We're going to go to [Namecheap](https://www.namecheap.com/) and buy a domain name. Why Namecheap?
Domain name registrars exist to sell domains and occasionally fuck you over by raising prices and trying to sell you crap that you don't need. They're generally a pain, so I did a Google search for "site:reddit.com best domain seller", and the good people of Reddit seemed to hate Namecheap the least.

<div class="loom-embed"><iframe src="https://www.loom.com/embed/ac966d91b0c543cebf076dc0bd6f53cb" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

### Set up Cloudflare

We're going to use Cloudflare to set up our DNS records. I've written elsewhere on [why I like Cloudflare](https://mattsegal.dev/cloudflare-review.html). TLDR it's pretty easy to use and provides some nice bonus features like caching your static files, SSL encryption and analytics.

All requests to our domain (mycoolwebsite.xyz) are going to pass through Cloudflare's servers, which are running NGINX under the hood. This kind of set up is called a "[reverse proxy](https://en.wikipedia.org/wiki/Reverse_proxy)", because we have a "proxy" (Cloudflare), routing all incoming traffic to our server. This is in contrast to a "forward proxy", which deals will outbound traffic.

<div class="loom-embed"><iframe src="https://www.loom.com/embed/c4d7ae886c8944299ac19a7fd286ee96" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

... 30 minutes later ...

<div class="loom-embed"><iframe src="https://www.loom.com/embed/c19353063130409799a53a008fb1efee" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

### Next steps

Alright! We're done! Congratulations, you've deployed a Django app. Just as a quick recap, you've learned how to:

- Use ssh, scp and create SSH keys
- Create a cloud virtual machine
- Set up your cloud VM
- Configure your Django project for deployment
- Deploy your Django project to the server
- Run your web app using Gunicorn and Supervisor
- Set up server logging
- Automate the deployment, server setup and database backups
- Set up your web app's domain name plus SSL and caching using Cloudflare

Now I encourage you to take the things you've learned and write your own Django app and try deploying that.
It will probably break at some point, it always does, but I hope you're able to use the skills that you've
picked up in this guide to debug the problem and fix it.

You've got the basics down, but there is a lot of stuff you can learn about deploying Django and web apps in general.
Some things you might want to look into at some point:

- [Setting up Django logging in production](https://mattsegal.dev/file-logging-django.html)
- [Adding error monitoring](https://mattsegal.dev/sentry-for-django-error-monitoring.html)
- [Adding offline tasks](https://mattsegal.dev/offline-tasks.html)
- [Adding offline scheduled tasks](https://mattsegal.dev/simple-scheduled-tasks.html)
- Start using Git for deployments
- Try using Fabric for deployment scripting
- Implement "continuous delivery" using GitHub actions
- Try using PostgreSQL instead of SQLite
- Try using NGINX instead of (or in addition to) Cloudflare
- Try put your gunicorn server / Django app inside of Docker with Docker Swarm
- Try out media hosting in AWS S3
- Add automated unit tests to your deployment pipeline
- Secure your server fail2ban and a firewall
- Improve your server setup automation with Ansible
- Try a different cloud hosting provider, like AWS or Google Cloud

There's an endless list of stuff you can learn, and there's no need to do it all right now,
but it's there if you're interested.

If you have any feedback on this guide, or questions about the steps, you can email me at mattdsegal@gmail.com.
