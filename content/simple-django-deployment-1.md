Title: Simple Django Deployments part one: infrastructure
Description: How to set up all the non-Django crap that you need to deploy
Slug: simple-django-deployment-1
Date: 2020-04-19 13:00
Category: Django

In order to deploy our Django app, we need a somewhere to run it: we need a server.
In this section we'll be setting up our server in "the cloud".
Doing this can be fiddly and annoying, especially if you're new, so we want to get it right first before we involve our Django app. By the end of this section we will learn how to:

- Install ssh and scp on Windows
- Create a SSH key
- Set up our cloud web server
- Learn how to access our server, upload files
- Test our setup

### Installing our tools

We'll need some tools to access the server:

- the "bash" [shell](https://en.wikipedia.org/wiki/Unix_shell) for scripting
- the "ssh" tool for logging into our web server
- the "scp" tool to transfer file to our server

We need to install these tools on Windows and the fastest and easiest way I know of is to just [install Git](https://git-scm.com/download/win).
We won't be using Git, just some of the tools that get installed with it. You can [learn Git](https://www.codecademy.com/learn/learn-git) some other time.
If you're using a Mac or Linux you can skip this step and open up a terminal window.

<div class="loom-embed"><iframe src="https://www.loom.com/embed/932bb0f277354db7aa9e2418b6969296" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

### Creating a SSH key

We'll be using an "SSH key" a way to authenticate ourselves when we log in to the server with ssh.
We need this key for when we create our server, so we're doing this bit first.
It's possible to just use a username / password when logging in via SSH, but creating a key is more convenient in the long run.
In particular, using a key means you don't have to type in a password every time you want to access the server.

In this video, we'll be creating an SSH key using the "ssh-keygen" command in bash:

```bash
ssh-keygen -C "mattdsegal@gmail.com"
```

<div class="loom-embed"><iframe src="https://www.loom.com/embed/d5a9137a974a4e5da6fe36ec04429ad7" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

Now that we've created our key, we're ready to use it to log into web servers. To recap:
the SSH key we just created has two parts, a public key (id_rsa.pub) and a private key (id_rsa).
Both keys will be stored in ~/.ssh by convention. You can read your public key like this:

```bash
cat ~/.ssh/id_rsa.pub
```

A public key is like your "username" when logging in - it's public information and it's OK to share it. It looks like this:

```text
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCVtWYN+uDbdG6RtmU8vcaj1cxYM0kK6565LFa
MMkolZZlSA6MhfWfGUmIGswIHJ/yjQCRQRihlEdm0VQJgsFBtK36J/U2/u+cMjGXwN/9swYBsnj
8bSMRzYc2s6PeshYmefpD80dWsvW550zqHmOwnKxeiwpz1q+rqUgT/xd0nOATw92nx5CS7ozhnL
t0FA0r0fk9LGih473Ho4/22fsAGXTcnMV5VoDgeBP4z8BLt16pKD8fgSGB8OG3/bN6udY54TcM2
rFjfN8yP+Vcbs5xBd3HaTu8Z42IPdC46Z25WMt285FLLZyUqWY36CrQZoTEf9F6aCkFgwtOCN81
u0Qr1 foo@bar.com
```

It's usually all just long one line of text.
The "ssh-rsa" part means it's a key for SSH and uses RSA encryption.
The "AAAAB3N...u0Qr1" part is your actual key, it uniquely identifies your keypair.
The "foo@bar.com" part is just a comment, it can be anything, but by convention it's your email.

A private key is like your password - do not share it with anyone. Private keys look like this:

```text
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAlbVmDfrg23RukbZlPL3Go9XMWDNJCuueuSxWjDJKJWWZUgOj
IX1nxlJiBrMCByf8o0AkUEYoZRHZtFUCYLBQbSt+if1Nv7vnDIxl8Df/bMGAbJ4/
G0jEc2HNrOj3rIWJnn6Q/NHVrL1uedM6h5jsJysXosKc9avq6lIE/8XdJzgE8Pdp
8eQku6M4Zy7dBQNK9H5PSxooeO9x6OP9tn7ABl03JzFeVaA4HgT+M/AS7deqSg/H
4EhgfDht/2zernWOeE3DNqxY3zfMj/lXG7OcQXdx2k7vGeNiD3QuOmduVjLdvORS
y2clKlmN+gq0GaExH/RemgpBYMLTgjfNbtEK9QIDAQABAoIBAQCAtWwAKOiYxAkr
jTyMdDwLLwx359+sW9YiLVRbRAErFaYzNJ1TdZV6k+ljCRN9Q4uYbtTJjwe7nRUm
TM+2gN8kfHhV+kiVxt5lk28wj3Qx9EqNF5/5vR3odPV26vPEhypB8V6FfYHO+S25
3zg6y+Z75jhz3g1DyYI14j4aB+qSg+5YSQ56vG+vhutYD41XVp3bkgD76kL8QFxd
q2cTpF5WSoZF49CaPhE2PnHoMZibLRQUOG+wJWkrQHcU+UnoWQvQUkqGNeRYpmI5
49Umk3b+/MQr0Dj6vuT2ZKqgFjr2FEu8AoA0tCZu8GUXWS1LshuZuqb1D0ZY+KOj
1SpEY48hAoGBAMXAbA8iNeON93yhOf7GqRCecL/wuyn6KqifCtEg8HbhbafcWBsd
/prEnEJHGRTU+omfLx7uVJmAgkVhj/uHl8K9L2qvlqkbBqF/rWPwWBi94G/cszn4
tYb91sTnnOk+QRjs/bGSCcv6kGlv2Bv0YYie0K6oQNPD9SqXCAit5hCDAoGBAMHO
Qv2+JcrrfLjoCbUaPaJ2sblO6Bq1RpUsltE1lL8nldTu/MgUIA3dEExg/hl7YLYW
vQVgNZkJQxHf1UJgZF/FTfw8yYaN4CKX4lOXDeKW8kN8xTtQQCPi77w/jxz5DUau
wmhqYOVwrCeqvLI4qUoEp6oOsQ83GxjHKXPfNK0nAoGAQD5aHLSFg068xz1tpOqP
RDnk8UZY17NRJoS8s+IanNRxlmYMLYsaCtey2AlXCaCDYDBZ05ej3laUe8vNRe7w
C7EAdY1jyb5g8hiTkPMk+6y7/Dtb8optFtTicAe6vz+dUGa1qHmEO0NEpSxTrgk/
om3N59/7Z5Cy1kpIruEn69cCgYBgRYCboVgOq9nB1Gn2D3nseT+hiKPdmIzeT07/
z7j7F8PjCXCCRxUBLf4Joui2acZJzZPJ1tfpFGO/vkumdFGIDW/Gy79j2pgrNv2T
fmbEVy0y/wjOhPfHm9Rw07XYs5K3uNoTmjxV3Rl3fuXLNkBJ53QOEsw7fak1LsHV
sFvvYwKBgDTRNKz3217jYjuAzeluHQHsfrUKn73DzckivDHr35m1JR37rlNXGWRE
JlN82KNevAqrDabwYPZnkDrPMGpLQi1A1icUtiBXRRskeR6ULxOASVyAJ3N1WV8T
1/g0+hahPeNFGQG649Z1d5WYSJeVbz7is3MiVGYaQu+iNz9VXNq5
-----END RSA PRIVATE KEY-----
```

... I'm not actually using this one so it's OK to share.

### Creating the server

You've probably heard the word "server" used to refer to a dozen different things, so let me be specific.
Our server will be a Linux virtual machine (VM), which we are going to rent from DigitalOcean, a cloud hosting company.
DigitalOcean will run our VM in one of their datacenters, which is a [big building](https://lh3.googleusercontent.com/7D8_SzSQQn-uDeKq4R7SSER5LO7fjsnkCLJ-uZG443cKHFS20nU-SyvlzXaGP97Fgt31MYJdgy94563uETi9jbosUMYQzO95-H0PRg=w2114-h1058-n) [full of computers](https://www.pon-cat.com/application/files/6215/3995/7501/Datacenter-Pon_Power.jpg). For our purposes, this VM is a stand-alone computer that is for our private usage, with a static IP address which we can use to find it online.

The first thing you need to do is create an account with [DigitalOcean](https://www.digitalocean.com/). The only reason I've chosen this company is because they have a nice web UI and I already use them. Other than that, there's no reason you couldn't also use Linode, AWS, Google Cloud or Azure to do the exact same thing. They all provide Linux web servers.

Once you've created your account, you can follow this video for the rest of the setup.
I'm not sure exactly when they're going to ask you to put your credit card details it, but have a credit card ready.

By the end of this video we'll have created our server and we'll have an IP address, which we can use to log into the server.

<div class="loom-embed"><iframe src="https://www.loom.com/embed/7c5f9599218a48f5873572084222ce50" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

### Setting up the server

The main tools that we'll need to run our Django app on this server are Python 3 and pip, the Python package manager.
You'll find that Python 3 is already installed on our Ubuntu server, but we need to install pip.
We'll be using the [apt package manager](https://devconnected.com/apt-package-manager-on-linux-explained/) to download and install pip.

<div class="loom-embed"><iframe src="https://www.loom.com/embed/16cfdb897c6a4e74ab0d16b777799ca3" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

By the way, it turns out that "LTS" stands for [Long Term Support](https://en.wikipedia.org/wiki/Long-term_support) and refers to Ubuntu's policy of how they plan to provide patches in the future (not super relevant to this guide).

### Uploading files and troubleshooting HTTP

So now we know how to create a server, log in with ssh and install the software we need to run Django.
Next I will show you how to upload files to the server with scp.
In addition, I'll show you how to run a quick and easy HTTP web server, which can be useful for debugging later.

<div class="loom-embed"><iframe src="https://www.loom.com/embed/3925e8a8ef45406eb5d25b623d4d5834" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

If you want to take a 40 minute side-quest I recommend checking out Brian Will's "The Internet" videos to learn more about what HTTP, TCP, and ports are: [part 1](https://www.youtube.com/watch?v=DTQV7_HwF58), [part 2](https://www.youtube.com/watch?v=3fvUc2Dzr04&t=167s), [part 3](https://www.youtube.com/watch?v=_55PyDw0lGU), [part 4](https://www.youtube.com/watch?v=yz3lkSqioyU).

I'll recap on the HTTP troubleshooting, so you understand why we just did that.
The main purpose was to get us ready to troubleshoot our Django app later.

We ran a program (http.server) on our Linux VM using Python.
That program was listening for HTTP requests on port 80, and when someone sends it a GET request, it responds with the contents of the index.html file that we wrote and uploaded.

If we use our web browser and visit our web server's IP address (64.225.23.131 in my case), our web browser will send an HTTP GET request to our server on port 80. Sometimes this works and gets the the HTML, but under some circumstances it will fail. The point of our troubleshooting is to figure out why it is failing. It could be that:

- Our computer is not connected to the internet
- Our web server is turned off
- We cannot access our web server over the internet
- A firewall on our web server is blocking port 80
- etc. etc. etc

One way we can figure out what's going on is to log into the VM using ssh and make a HTTP GET request using curl. If the curl request works, then we know that the our HTTP server program is working and serving requests _inside_ the VM, and the problem is something between our computer and the VM. Once we've narrowed down the exact problem, then we can figure out how to fix it.

![troubleshooting http]({attach}troubleshoot-http.png)

### Next steps

Now our server is ready to serve Django and we know how to troubleshoot HTTP connections.
Next we will [prepare and test Django locally]({filename}/simple-django-deployment-2.md).
