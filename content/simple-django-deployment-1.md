Title: Simple Django Deployments part one: infrastructure
Description: How to set up all the non-Django crap that you need to deploy
Slug: simple-django-deployment-1
Date: 2020-04-19 13:00
Category: Django

This part will be the most painful and frustrating, so we want to get this bit right first before we involve our Django app. Here we will learn how to:

- Buy a domain name
- Set up our cloud web server
- Set up a Cloudflare reverse-proxy
- Learn how to access our server, upload files
- Test our setup

This is, admittedly, a fuckton of stuff to do and many of these steps will be new to you, so let's proceed by taking many tiny steps.

### Buy a domain name

- buy a domain name
- create a DO droplet
- set up cloudflare (link to cloudflare)
- get droplet IP and put it into cloudflare
- ensure caching, compression
- set A record with proxing via Cloudflare (NGINX)
- test A record with dig or DNS checker
- wait a while...

- quick tools aside ConEmu for Windows
- also show how to access git bash via conemu

- Make sure you have bash or git-bash
- Fuck putty
- intro to git-bash, how to get it, where to run
- check for ssh, scp
- create an ssh key
- add it to the server
- ssh into the server
- copy a file onto the server

- create a HTML file locally
- run http.server using Python 3 locally
- check it in your browser

- copy HTML file onto server
- ssh in
- cat it to view
- run http.server on server
- check the IP address
- check the domain name

[Prepare and test Django locally]({filename}/simple-django-deployment-2.md)
