Title: An introduction to cloud file storage
Description: A gentle introduction using AWS S3 to host all your files
Slug: aws-s3-intro
Date: 2020-6-5 11:00
Category: DevOps

Sometimes when you're running a web app you will find that you have a lot of files on your server. All these files will start to feel like a burden. You might worry about losing them all if the server fails, or you might be concerned about running out of disk space. You might even have multiple servers that all need to access these files.

Wouldn't it be nice if solving all these issues were someone else's problem? You would pay a few cents a month so that you never need to think about this again, right? I like using cloud object storage for hosting most of my web app's files and backups. If you haven't heard of "object storage" before: it's just a kind of cloud service where you can store a bunch of files. All major cloud providers offer this service:

- Amazon's AWS has the [Simple Storage Service (S3)](https://aws.amazon.com/s3/)
- Microsoft's Azure has [Storage](https://azure.microsoft.com/en-us/services/storage/)
- Google Cloud also has [Storage](https://cloud.google.com/storage)
- DigitalOcean has [Spaces](https://www.digitalocean.com/products/spaces/)

These object storage services are _very_ cheap at around 2c/GB/month, you'll never run out of disk space, they're easy to access from command line tools and they have very fast upload/download speeds, especially to/from other services hosted with the same cloud provider. I use these services a lot: this blog is being served from AWS S3.

I like using S3 simply because I'm quite familiar with it, so that's what we're going to use for the rest of this post. The other services are probably great as well. This video will take you through how to get started with AWS S3.

<div class="yt-embed">
    <iframe 
        src="https://www.youtube.com/embed/b-icwbsGZkc" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen
    >
    </iframe>
</div>

One great use for object storage like AWS S3 is hosting your [database backups]({filename}/databases/postgres-backup-automate.md).
