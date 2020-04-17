Title: DNS for beginners: how to give your site a domain name
Slug: dns-for-noobs
Date: 2020-4-13 12:00
Category: DevOps

You are learning how to build a website and you want to give it a domain name like mycoolwebsite.com.
It doesn't seem like a _real_ website without a domain name, does it?
How is anybody going to find your website without one?
Setting up your domain is an important step for launcing your website, but it's also a real pain if you're new to web development.
I want to help make this job a little easier for you.

Typically you go to [namecheap](https://www.namecheap.com/) or GoDaddy or some other domain name vendor and you buy mycoolwebsite.com for 12 bucks a year - now you need to set it up.
When you try to get started you are confronted by all these bizzare terms: "A record", "CNAME", "nameserver". It can be quite intimidating.
The rest of this blog will show you the basics of how to set up your domain, with a few explanations sprinkled throughout.

Contents:

- What the fuck is DNS?
- I want my domain name to go to an IP address
- I want my domain name to go to a different domain name
- I want to give control of my domain name to another service

### What the fuck is DNS?

I'll keep this short. I think [CloudFlare explains it best](https://www.cloudflare.com/learning/dns/what-is-dns/):

> The Domain Name System (DNS) is the phonebook of the Internet. Humans access information online through domain names, like nytimes.com or espn.com. Web browsers interact through Internet Protocol (IP) addresses. DNS translates domain names to IP addresses so browsers can load Internet resources.

DNS is a worldwide, online "phonebook" that translates human-friendly website names like "mattsegal.dev" into computer-friendly numbers like 192.168.1.1. You use the domain name system every day:

- You type "mattsegal.dev" into your web browser and press "Enter"
- Your computer will reach out into the domain name system and ask other computers to find out which IP address "mattsegal.dev" points to
- Your computer eventually finds the correct IP address
- Your web browser fetches a web page from that IP address

So, how do we get our website into this "phonebook"?

### I want my domain name to go to an IP address

Sometimes you have an IP address like 11.22.33.44 and you want your domain name to send users to that IP. You want a mapping like this:

```text

mycoolwebsite.com --> 11.22.33.44

```

You will need this when you are running software like WordPress, or your own custom web app. Your website is running on a server and that server has an IP address.
For example, I have a website [mattslinks.xyz](https://mattslinks.xyz) which runs on a webserver which has a public IP of 167.99.78.141.
My users (me, my girlfriend) don't want to type in 167.99.78.141 into our browsers to visit my site. We'd prefer to type in mattslinks.xyz, which is way easier to remember. So I need to set up a mapping using DNS:

```text

mattslinks.xyz --> 167.99.78.141

```

So how do we set this up? We need an **A record** ("address record") to do this. An A record maps a domain name to an IP address.
To set up an A record you need to go onto your domain name provider's website and enter the **subdomain** name you want plus the IP address that you wanto to point to.

![Photo]({attach}a-record.png)

What I've set up here is:

```text
mattslinks.xyz --> 167.99.78.141
www.mattslinks.xyz --> 167.99.78.141
```

At this point you may yell _"What the fuck is a subdomain!?"_ at your monitor. Please do, it's cathartic. The idea is that when you own mattslinks.xyz, you also own a near-infinite number of "child domains" which end in mattslinks.xyz. For example you can set up A records (and other DNS records) for all these domain names:

- mattslinks.xyz ("root domain", sometimes written as "@")
- www.mattslinks.xyz (a subdomain)
- blog.mattslinks.xyz (a different subdomain)
- cult.mattslinks.xyz
- super.secret.clubhouse.mattslinks.xyz

Apparently you can do this to up to 255 characters (including the dots) so this.is.a.very.long.domain.name.but.i.advise.against.doing.this.mattslinks.xyz is _technically_ possible, but a stupid idea.

If you're serving a normal website, then it's pretty standard to add A records for both your root domain (mattslinks.xyz) and the "www" subdomain (www.mattslinks.xyz), because some people might put "www" in front of the domain name and we don't want them to miss our website.

Just in case this all seems a little too abstract and theoretical for you, here's a video of me setting some A records:

<div class="loom-embed"><iframe src="https://www.loom.com/embed/2398e6757135445989f83757befd6c11" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

And then, 30 minutes later, checking if I've gone mad or not...

<div class="loom-embed"><iframe src="https://www.loom.com/embed/c591b12ac5ae400b82e497011a96d901" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

Finally, the record updates and I add a www subdomain

<div class="loom-embed"><iframe src="https://www.loom.com/embed/4a2fed1898b0491fabab1ef8f063b987" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

You might also be wondering about the **TTL** value. It's not that important, just set it to 3600. If you care to know, TTL stands for "time to live" and it represents how long your DNS records is going to hang around in the system before anybody checks the records you set. So if it's 3600 (seconds), it means it takes at least an hour for changes that you make to your DNS records to update on other people's computers.

So you have an A record set up, how do you check that it's working? The easiest way is to wait an hour or so and then use a 3rd party website like [DNS checker](https://dnschecker.org/#A/mattslinks.xyz). If you're a little more technical and have a bash shell handy you can also try using [dig](https://www.linux.com/training-tutorials/check-your-dns-records-dig/) from your local machine.

### I want my domain name to go to a different domain name

Sometimes your DNS needs are a little more complicated than just mapping a domain name to an IP address. Sometimes you want to do this instead:

```text
prettyname.com --> ugly-name-for-pretty-site.ap-southeast2.amazon.aws.com
```

That is to say, you want users to type in www.prettyname.com, but you want them to see the website which is hosted on ugly-name-for-pretty-site.ap-southeast2.amazon.aws.com, but you never want them to know about the hideous name that lies beneath.

For this problem you need a **CNAME record** ("canonical name"). A CNAME record is used to map from one domain name to another.

Here's an example of me setting up a CNAME record in CloudFlare:

<div class="loom-embed"><iframe src="https://www.loom.com/embed/1445cce96ac3449183acf40719c02b4d" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

### I want to give control of my domain name to another service

Sometimes you you want to give control of a domain to another service. This can happen when you're using a service like Squarespace or Webflow and you want them to set up all your DNS records for you, or if you want to use a different service (like CloudFlare) to manage your DNS.

The way to set this up is to use set the **name servers** of your domain. Changing the name servers, as far as I can tell, gives the target servers full control of your domain. In this video, I'll show you some examples.

<div class="loom-embed"><iframe src="https://www.loom.com/embed/269e0eba94dc40d3880ef04aa261f41f" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

### Conclusion

So there you go, some basic DNS-how-tos. With A records, CNAMES and name servers under your belt, you should be able to do ~70% of DNS tasks that you need in web development. Get a handle on TXT and MX records, and you're up to ~95%. DNS is horrible to work with, but it doesn't need to be confusing.

This certainly isn't the definitive guide on DNS, and I expect I made some technical errors in my explanations, but I hope you now have the tools to go out an setup some websites.
