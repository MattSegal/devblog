Title: Cloudflare makes DNS slightly less painful  
Slug: cloudflare-review
Date: 2020-04-18 12:00
Category: DevOps

When you're setting up a new website, there's a bunch of little tasks that you have to do that _suck_.
They're important, but they don't give you the joy of creating something new, they're just... plumbing.

In particular I'm thinking of:

- setting up your domain name with DNS records
- encrypting your traffic with SSL
- compressing and caching your static assets (CSS, JS) using a CDN

No one decided to learn web development because they were super stoked on DNS.
The good news is that you can use [Cloudflare](https://www.cloudflare.com/) (for free)
to make all these plumbing tasks a little less painful.

In the rest of this post I'll go over the pros and cons of using Cloudflare,
plus a short video guide on how to start using it.

### What is Cloudflare

Cloudflare is a [reverse proxy](https://en.wikipedia.org/wiki/Reverse_proxy) service that you put in-between you website visitors and your website's server. All requests that hit your website are routed through Cloudflare's servers first. This means that they can provide:

- **DNS record configuration**: allowing you to set up A records, CNAMEs etc for your domain.
- **HTTP traffic encryption using SSL**: All HTTP traffic between the end-user and Cloudflare's servers are encrypted with SSL (making it HTTPS)
- **Caching of static assets**: Cloudflare will cache static assets like CSS and JS [depending on the "Cache-Control" headers](https://support.cloudflare.com/hc/en-us/articles/200172516-Understanding-Cloudflare-s-CDN) set by your origin server.
- **Compression of static assets**: Cloudflare will compress [static assets](https://support.cloudflare.com/hc/en-us/articles/200168396-What-will-Cloudflare-compress-) like CSS and JS so that your pages load and render faster.

This is a _whooole_ lot of bullshit that I don't want to set up myself, if I can avoid it, so it's nice when Cloudflare handles it for me.

### Cloudflare pros

In addition to the features I listed above, there are a few nice I've found when using Cloudflare:

- **Free**: It has a free plan which is sufficient for all the projects I've worked on so far
- **Easy to use**: I think it's uncommonly easy to set up and use for tools in its field
- **CNAME flattening**: They provide a handy DNS feature called "CNAME flattening", which means you can point your root domain name (eg. "mattsegal.dev") to other domain names (eg. an AWS S3 bucket website "mattsegal.dev.s3-blah.aws.com"). As far as I know only Cloudflare provides this feature.
- **Flexible SSL**: Their "flexible SSL" feature is both a pro and a con. It works like this: traffic between you users and Cloudflare are encrypted, but traffic between Cloudflare are your servers are not encrypted. As long as you trust Cloudflare or intermediate routers not to snoop on your packets, this is a nice setup. In this case setting up flexible SSL is as simple as toggling a button on the website. You _can_ set up end-to-end encryption but that's a little more work. [Let's Encrypt](https://letsencrypt.org/) has made setting up SSL _much_ easier and cheaper for developers, but it's still relatively complex compared to Cloudflare's "flexible" implementation.
- **Faster DNS updates?**: I might be imagining things, but I find that updates to DNS records in Cloudflare _seem_ to propagate faster than other services.
- **Analytics**: They provide some basic analytics like unique visitors and download bandwidth, which is nice, I guess

### Cloudflare cons

The biggest main con I see for using Cloudflare is that you're not learning to use open source alternatives like self-hosted NGINX to do the same job.
If you are an NGINX expert already then you're a big boy/girl and you can make your own decisions about what tools to use.
If you're a newer developer and you've never set up a webserver like NGINX and Apache, then you're robbing yourself of useful infrastructure experience if you _only_ ever use Cloudflare for _everything_.

That said, I think that newer developers should start deploying websites using services like Cloudflare, and then learn how to use tools like NGINX.

Another, more abstract downside, is that some double-digit percentage of the internet's websites use Cloudflare. If you're worried about centralization of control of the internet, then Cloudflare's growing consolidation of internet traffic is a concern. Personally I don't really care about that right now.

### How to get started

This video shows you how to get set up with Cloudflare.

<div class="loom-embed"><iframe src="https://www.loom.com/embed/fffc03f4a3f24285be017b7759461755" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

### What now?

Once you've set up Cloudflare, you'll need to start creating some DNS records. I've written a [guide on exactly this topic](https://mattsegal.dev/dns-for-noobs.html) to help you get set up.
I suggest you check it out so you can give your website a domain name.
