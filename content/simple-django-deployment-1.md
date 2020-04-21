Title: Simple Django Deployments part one: infrastructure
Description: How to set up all the non-Django crap that you need to deploy
Slug: simple-django-deployment-1
Date: 2020-04-19 13:00
Category: Django

In order to deploy our Django app, we need a somewhere to run it: we need a server.
In this section we'll be setting up our server in "the cloud".
Doing this can be fiddly and annoying, especially if you're new, so we want to get it right first before we involve our Django app. By the end of this section we will learn how to:

- Create a SSH key
- Set up our cloud web server
- Learn how to access our server, upload files
- Test our setup

### Creating a SSH key

- Make sure you have bash or git-bash
- search for bash in windows sidebar - if you see git bash
- we need git for it's bash shell but we won't need git

- bing git
- got to download page
- download for windows
- default install options

- open git bash
- check for ssh, scp

- do you already have an ssh key?
- ls ~/.ssh id_rsa id_rsa.pub
- if not

ssh-keygen -t rsa -C "mattdsegal@gmail.com"

- you can password protect, I cbf
- default options
- ls ~/.ssh
- cat ~/.ssh/id_rsa private key
- cat ~/.ssh/id_rsa.pub
- create an ssh key

### Creating the server

You've probably heard the word "server" used to refer to a dozen different things, so let me be specific.
Our server will be a Linux virtual machine (VM), which we are going to rent from DigitalOcean, a cloud hosting company.
DigitalOcean will run our VM in one of their datacenters. For all intents and purposes, this VM is a stand-alone computer that is for our private usage, with a static IP address which we can use to find it online.

The first thing you need to do is create an account with [DigitalOcean](https://www.digitalocean.com/). The only reason I've chosen this company is because they have a nice web UI and I already use them. Other than that, there's no reason you couldn't also use Linode, AWS, Google Cloud or Azure to do the exact same thing. They all provide Linux web servers.

Once you've created your account, you can follow this video for the rest of the setup.

- create new project
- explain what a droplet is
- choose Ubuntu (eg. Python, apt package manager)
- choose \$5/month
- explain that main constraint will be memory
  - database will not use much disk space
  - most web apps don't use that much CPU
- datacenter region doesn't matter, just choose whatever is closest to your users (speed of light)
- SSH key auth
- backups - naaaah
- CREATE DROPLET
- wait
- get IP address

### Setting up the server

- go into git bash
- check for ssh
- man ssh
- ssh in
- explain ssh semantics
- accept host authenticity
- get in
- pwd
- ls
- expain /root/ ~
- we need Python to run Django
- python3 -V
- we need pip to install Python packages
- pip ==> FAIL
- pip3 ==> FAIL
- apt ==> help
- apt install python3-pip FAIL
- apt update -- update package list
- apt upgrade -- best to do it now, but could skip... security?
- apt install python3-pip
- pip3 -V Good! (note python3)
- pip -V BAD! (we don't care)
- pip3 freeze # see what is installed currently
- done for now

### Uploading files

- create a small HTML file index.html
- run http.server locally
- check in browser
- run http.server locally on port 80
- explain port 80
- explain port 22
- check in browser
- check for scp
- man scp
- add it to the server
- copy a file onto the server
- ssh into the server
- ls for the file
- cat the file
- run http.server
- explain port 80
- open another tab ssh
- use curl to check localhost
- use curl to check 0.0.0.0
- check the IP address in browser

show schematic of our http debugging

### Next steps

That's it our server is ready to serve Django
importantly we know how to debug http connections

[Prepare and test Django locally]({filename}/simple-django-deployment-2.md)
