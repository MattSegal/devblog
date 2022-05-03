Title: How I hunt down (and fix) errors in production
Description: My approach to finding and fixing bugs with an example
Slug: prod-bug-hunt
Date: 2022-05-03 12:00
Category: Programming

Once you’ve deployed your web app to prod there is a moment of satisfaction: a brief respite where you can reflect on your hard work. You sit, adoringly refreshing the homepage of www.mysite.com to watch it load over and over. It’s beautiful, perfect, timeless. A glittering crystal palace of logic and reason. Then people start to actually use it in earnest and you begin to receive messages like this in Slack:

>  Hey Matt. I am not getting reply emails for case ABC123 Jane Doe

Ideally, with a [solid monitoring stack](https://mattsegal.dev/django-monitoring-stack.html), you will be alerted of bugs and crashes as they happen, but some may still slip through the cracks. In any case, you’ve got to find and fix these issues promptly or your users will learn to distrust you and your software, kicking off a feedback loop of negative perception. Best to nip this in the bud.

So a user has told you about a bug in production, and you’ve gotta fix it - how do you figure out what went wrong? Where do you start? In this post I’ll walk you through an illustrative example of hunting down a bug in our email system.

## The problem

So this was the message I got over Slack from a user of my website:

>  Hey Matt. I am not getting reply emails for case ABC123 Jane Doe

A user was not receiving an email, despite their client insisting that they had sent the email. That’s all I know so far...

## More detail

... and it’s not quite enough. I know the case number but that’s not enough to track any error messages efficiently. I followed up with my user to check:

- what address was used to send the email (eg. jane.doe@gmail.com)
- when they attempted to send the email (over the weekend apparently)

With this info in hand I can focus my search on a particular time range and sender address.

## Knowledge of the system

There’s one more piece of info you need to have before you start digging into log files and such: what are the components of the email-receiving system? I assembled this one myself, but under other circumstances, in a team setting, I might ask around to build a complete picture of the system. In this case it looks like this:

![email-system]({attach}/img/prod-bug-hunt/email-system.png)

In brief:

- The client sends an email from their email client
- The email travels through the mystical email realm
- SendGrid (SaaS product) receives the email via SMTP
- SendGrid sends the email content to a webhook URL on my webserver as an HTTP POST request
- My web application ingests the POST request and stores the relevant bits in a database table

Inside the web server there’s a pretty standard “3 tier” setup:

- NGINX receives all web traffic, sends requests onwards to the app server
- Gunicorn app server running the Django web application
- A database hosting all the Django tables (including email content)

![web server]({attach}/img/prod-bug-hunt/webserver.png)

## My approach

So, the hunt begins for evidence of this missing email, but where to start looking? One needs a search strategy.  In this case, my intuition is to check the “start” and “end” points of this system and work my way inwards. My reasoning is:

- if we definitely knew that SendGrid did not receive the email, then there’d be no point checking anywhere downstream (saving time)
- if we knew that the database contained the email (or it was showing up on the website itself!) then there’d be no point checking upstream services like SendGrid or NGINX (saving time)

So do you start upstream or downstream? I think you do whatever’s most convenient and practical. 

Of course you may have a special system-specific knowledge that leads you towards checking one particular component first (eg. “our code is garbage it’s probably our code, let’s check that first”), which is a cool and smart thing to do. Gotta exploit that domain knowledge.

## Did SendGrid get the email?

In this case it seemed easiest to check SendGrid’s fancy web UI for evidence of an email failing to be received or something. I had a click around and found their reporting on this matter to be... pretty fucking useless to be honest.

![Sendgrid chart]({attach}/img/prod-bug-hunt/sendgrid-chart.png)

This is all I could find - so I’ve learned that we usually get emails. Reassuring but not very helpful in this case. They have good reporting on email sending, but this dashboard was disappointingly vague.

## Is the email in the database?

After checking SendGrid (most upstream) I then checked to see if the the database (most downstream) had received the email content.

As an aside, I also checked if the email was showing up in the web UI, which it wasn’t (maybe my user got confused and looked at the wrong case?). It’s good to quickly check for stupid obvious things just in case.

Since we don’t have a high volume of emails I was able to check the db by just eyeballing the Django admin page. If we were getting many emails per day I would have instead run a query in the Django shell via the ORM (or run an SQL query directly on the db).

![Django admin page]({attach}/img/prod-bug-hunt/django-admin.png)

It wasn’t there >:(

## Did my code explode?

So far we know that *maybe* SendGrid got the email and it’s definitely not in the database. Since it was easy to do I quickly scanned my error monitoring logs (using [Sentry](https://sentry.io/for/python/)) for any relevant errors. Nothing. No relevant application errors during the expected time period found.

![Sentry error logs]({attach}/img/prod-bug-hunt/sentry-errors.png)

**Aside**: yes my Sentry issue inbox is a mess. I know, it's bad. Think of it like an email in box with 200 unread emails, most of them spam, but maybe a few important ones in the pile. For both emails and error reports, it's best to have a clean inbox.

**Aside**: ideally I would get Slack notifications for any production errors and investigate them as they happen but Sentry recently made Slack integration a paid feature and I haven’t decided whether to upgrade or move.

## Did NGINX receive the POST request?

Looking back upstream, I wanted to know if I could find anything interesting in the NGINX logs. If you’re not familiar with webserver logfiles I give a rundown in [this article](https://mattsegal.dev/django-gunicorn-nginx-logging.html) covering a typical Django stack.

All my server logs get sent to SumoLogic, a log aggregator (explained in the “log aggregation” section of [this article](https://mattsegal.dev/django-monitoring-stack.html), where I can search through them in a web UI.

I checked the NGINX access logs for all incoming requests to the email webhook path in the relevant timeframe and found nothing interesting. This shows NGINX is receiving email data in general, which is good.

![Sumologic search of access logs]({attach}/img/prod-bug-hunt/sumologic-access-search.png)

Next I checked the NGINX error logs... and found a clue!

![Sumologic search of error logs]({attach}/img/prod-bug-hunt/sumologic-error-search.png)

For those who don’t want to squint at the screenshot above this was the error log:

> 2022/04/30 02:38:40 [error] 30616#30616: *129401 client intended to send too large body: 21770024 bytes, client: 172.70.135.74, server: www.mysite.com, request: "POST /email/receive/ HTTP/1.1", host: "www.mysite.com”

This error, which occurs when in receiving a POST request to the webhook URL, lines up with the time that the client apparently sent the email. So it seems likely that this is related to the email problem.

## What is going wrong?

I googled the error message and found [this StackOverflow post](https://stackoverflow.com/questions/44741514/nginx-error-client-intended-to-send-too-large-body). It seems that NGINX limits the size of requests that it will receive (which is configurable via the nginx.conf file). I checked my NGINX config and I had a limit of 20MB set. Checking my email ingestion code, it seems like all the file attachments are included in the HTTP request body. So... my guess was that the client sending the email attached more than 20MB of attachments (an uncompressed phone camera image is ~5MB) and NGINX refused to receive that request. Most email providers (eg Gmail) offer ~25MB of attachments per email.

## Testing the hypothesis

I actually didn’t do this because I got a little over-exicted and immediately wrote and pushed a fix. 

What I should have done is verified that the problem I had in mind actually exists. I should have tried to send a 21MB email to our staging server to see if I could reproduce the error, plus asked my user to ask the client if she was sending large files in her email.

Oops. A small fuckup given I think the error message is pretty clear about what the problem is.

## The fix

The fix was pretty simple, as it often is in these cases, I bumped up the NGINX request size limit (`client_max_body_size`) to 60MB. That might be a little excessive, perhaps 30MB would have been fine, but whatever. I updated the config file in source control and deployed it to the staging and prod environments. I tested that I can send larger files by sending a 24MB email attachment to the staging server.

## Aftermath

We’ve asked the client to re-send her email. Hopefully it comes through and all is well.

I checked further back in the SumoLogic and this is not the first time this error has happened, meaning we’ve dropped a few emails. I’ll need to notify the team about this. 

If I had more time to spend on this project and I’d consider adding some kind of alert to NGINX error logs so that we’d see them pop up in Slack - maybe SumoLogic offers this, I haven’t checked. 

Another option would be going with an alternative to SendGrid that had more useful reporting on failed webhook delivery attempts.

## Overview

Although it can sometimes be stressful, finding and fixing these problems can also be a lot of fun. It’s like a detective game where you are searching for clues to crack the case.

In summary my advice for productively hunting down errors in production are:

- Gather info from the user who reported the error
- Mentally sketch a map of the system
- Check each system component for clues, using a search strategy
- Use these clues to develop a hypothesis about what went wrong
- Test the hypothesis if you can (before writing a fix)
- Build, test, ship a fix (then check it's fixed)
- Tell your users the good news

Importantly I was only able to solve this issue because I had access to my server log files. A good server monitoring setup makes these issues much quicker and less painful to crack. If you want to know what montioring tools I like to use in my projects, check out [my Django montioring stack](https://mattsegal.dev/django-monitoring-stack.html).