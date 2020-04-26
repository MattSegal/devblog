Title: Simple django deployment part five: deployment automation
Description: Script your Django deployment with bash
Slug: simple-django-deployment-5
Date: 2020-04-26 17:00
Category: Django

Deploying our Django app involved a lot of different commands, right? It would suck to have to do all that over again, wouldn't it?

Having to manually type all those commands again would be tedious, slow and easy to screw up.
Even worse, the harder it is to deploy, the less often you are going to do it.
If you deployments are infrequent, then they'll contain more features in one big batch and they'll be risker, because there's more things that could go wrong, and it's harder to tell what caused any issues that crop up.
Frequent, small deployments are key to pumping out lots of valuable code with lower risk.
The [Phoenix Project](https://www.amazon.com.au/Phoenix-Project-DevOps-Helping-Business/dp/0988262592)
is a great book that talks more about this idea (srsly give it a read).

So, if we want to deploy fast and often, we're going to need to automate the process. Hell, even if we want to do this again in a week we need to automate the process, because we're definitely going to forget what-the-fuck we just did.
No need to get fancy, we can do the whole thing with a bunch of bash scripts.
You can get fancy later.

Our goal is that you can run a single bash script and your whole deployment happens.

We'll write these scripts in stages:

- Uploading new code to the server
- Installing the new code
- Single deploy script
- Backing up the database
- Automating the server setup

### Uploading new code to the server

If you recall, we uploaded code to the server by creating a "deploy" directory locally,
then uploading that directory to our server. After that we did some clean up work on that directory
to deal with Python bytecode (pyc) files and Windows line endings.

Let's automate the upload first. The files that we need to copy over are:

- requirements.txt for our Python packages
- tute for our Django code
- scripts for our bash scripts
- config for our Gunicorn and Supervisor config

<div class="loom-embed"><iframe src="https://www.loom.com/embed/aaa3e2038ada46e98705d223a82fa371" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

### Installing the new code

Now we have automated the process of getting our code onto the server,
let's script the bit where we install it in the project dir and run Gunicorn

<div class="loom-embed"><iframe src="https://www.loom.com/embed/3fb4a3e1cdd54fa19ac72478904cc49d" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

So, you might have noticed that we stop Gunicorn at the start of the deployment and start it again it at the end. That means your site will be offline during the deployment and if something goes wrong, it'll stay down. You have to log in and manually fix the problem to get it running again.

This is fine for personal projects and low traffic websites - nobody will notice. If you're running some important, high traffic website, then there are techniques to make sure that your website is always running - but we won't go into that here. We're keeping it simple for now.

### Single deploy script

Alright we're basically done with this section, now all we need to do is combine our two scripts into a master deploy script.

<div class="loom-embed"><iframe src="https://www.loom.com/embed/c4a94c5a12a14084b6298d53a0cde9be" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

That's it, now we can deploy our code over and over in seconds.

### Backing up the database

This section is optional, it's nice to have, but not a core part of the guide. Skip it if you like.
Here I'll show you how to back up your database on the server.
It's very, very simple to do with SQLite because the database is just a single file.

<div class="loom-embed"><iframe src="https://www.loom.com/embed/a6f0a047674e46929a35cbdf27b6165e" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

### Automating the server setup

This section is also optional, it's nice to have, but not a core part of the guide. Skip it if you like.

You will get to a point where you want to move you app to a new server,
or maybe you've broken your server really badly, or maybe you want to set your server up again slightly differently.
When that time comes, you will not remember how you set this one up: that's why we want to automate our server setup.

Automating your server setup also allows you to do things that were inconceivable before:

- run hundreds of servers that are all configured the same way
- create a new server for every new deployment (allowing for "blue-green" deployments), allowing for zero downtime during deploys
- create servers for testing that are identical to your "live" production server

I talk more about this topic in my video on [configuration management](https://mattsegal.dev/intro-config-management.html).

So, we want to be able to blow away our server and make a new one with minimal work required. The good news is we're already most of the way there. Our Django app in prod is defined by 3 things at the moment:

- our code (we have our code already)
- our database (we have automatic backups already)
- the server (we know how to set it up, we just need to automate this)

Our goal in this section is to run a single script on a new DigitalOcean droplet and it all just works. In addition, we want this script to be "idempotent" - this means we want to be able to run it many times on the same server and get (mostly) the same result.

<div class="loom-embed"><iframe src="https://www.loom.com/embed/75a0e1b6e68e4feb957dffa3534122a5" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

This script can get kind of long and hairy, especially as your deployments get more complicated.
At some point, you're going to want to use something other than a bash script to automate this process.
When you're ready, I recommend you take a look at [Ansible](https://github.com/ansible/ansible),
which is a great tool for writing scripts to automatically setting up servers.
[Packer](https://www.packer.io/) is also a good tool for using scripts like the one we just wrote to
"bake" a single virtual machine image, which can then be used to instantly create multiple copies of the same virtual machine.

### Next steps

There's one last thing to do before our website is _really_ deployed - [give our app a domain name]({filename}/simple-django-deployment-6.md).