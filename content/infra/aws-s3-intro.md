Title: An intro to cloud file storage
Description: A gentle introduction use AWS S3 to host all your files
Slug: aws-s3-intro
Date: 2020-6-5 11:00
Category: DevOps

Sometimes when you're running a web app you will find that you have a lot of files on your server. All these files will start to feel like a burden. You might worry about losing them all if the server fails, or you might be concerned about running out of disk space. You might even have multiple servers that all need to access these files.

Wouldn't it be nice if solving all these issues were someone else's problem? You'd pay a couple cents a month so that you never need to think about this again, right? I like using cloud object storage for hosting most of my web app's files and backups. If you haven't heard of "object storage" before: it's just a kind of cloud service where you can store a bunch of files. All major cloud providers offer this service:

- Amazon's AWS has the [Simple Storage Service (S3)](https://aws.amazon.com/s3/)
- Microsoft's Azure has [Storage](https://azure.microsoft.com/en-us/services/storage/)
- Google Cloud also has [Storage](https://cloud.google.com/storage)
- DigitalOcean has [Spaces](https://www.digitalocean.com/products/spaces/)

These object storage services are _very_ cheap at around 2c/GB/month, you'll never run out of disk space, they're easy to access from command line tools and they have very fast upload/download speeds, especially to/from other services hosted with the same cloud provider. I use these services a lot: this blog is being served from AWS S3.

I like using S3 simply because I'm quite familiar with it, so that's what we're going to use for the rest of this post. The other services are probably great as well. This video will take you through how to get started with AWS S3.

<div class="yt-embed">
    <iframe 
        src="https://www.youtube.com/embed/OOYG4ZGOv80" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen
    >
    </iframe>
</div>

- create an AWS account (credit card required?)
- view S3 via web UI
- create a bucket
  - private by default
  - global namespace
- upload a file
  - mention 2c/gigabyte/month
- download a file
- i'll be using bash but all of this works from a windows shell as well
- install awscli
  - virtualenv
  - pip install awscli
- create credentials
- set up credentials locally
- aws help
- aws s3 help
- aws s3 ls
- aws s3 ls s3://mybucket
- aws s3 cp myfile s3://mybucket
- rm myfile
- aws s3 cp s3://mybucket/myfile .
- aws s3 cp myfile s3://mybucket/foo/myfile
- aws s3 cp --recursive myfolder s3://mybucket
- rm all locally
- aws s3 sync s3://mybucket .
