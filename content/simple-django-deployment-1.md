Title: Simple Django Deployments part one: infrastructure
Description: How to set up all the non-Django crap that you need to deploy
Slug: simple-django-deployment-1
Date: 2020-04-19 13:00
Category: Django

### Non Django Infrastructure

This part involves the most painful tooling, so we want to get this bit right first before we involve our Django app.

- create a DO droplet
- buy a domain name
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
