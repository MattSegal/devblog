Title: 3 ways to deploy a Django backend with a React frontend
Slug: django-spa-infrastructure
Date: 2020-04-7 12:00
Category: Django

You're developing a web app with a Django REST backend and some sort of single page app frontend using React or Vue or something like that. There are many ways for you to run this app in production. There are a lot of choices that you need to make:

- Do you serve your frontend as a stand-alone static site or via Django views?
- Do you put the backend and frontend on different subdomains?
- Do you deploy the backend and frontend separately, or together?

How do you choose? What is "the right way"?

Well, the bad news is that there is no "right way" to do this and there are a lot of different trade-offs to consider. The good news is that I've compiled three different options with their pros and cons.

### Option 1 - Cram it all into Django

This is the "default" approach, where you have a Django site and you just add React to it. All your HTML is served via Django views, and all your JavaScript and CSS is bundled by Django and served as static files. All your code, frontend and backend, is in one Git repository. You serve the app from a single domain like www.myapp.com.

When you deploy your code using this setup, you will need to:

- Use [webpack](https://webpack.js.org), or something [similar](https://www.google.com/search?q=webpack+alternatives), to build your JavaScript and CSS assets and put them into a Django static files directory
- Deploy Django like you usually would

You will need to use something like [django-webpack-loader](https://github.com/owais/django-webpack-loader) to integrate Webpack's build assets with Django's staticfiles system and templates. Other than that, it's a vanilla Django deployment.

The pros are:

- **Simplest infrastructure.** Other than setting up django-webpack-loader and adding a Webpack build to the start of your deployment process, there's nothing else you need to do to your production infrustructure. Nothing extra to set up, pay for, configure, debug or tear your hair out over.
- **Cross-cutting changes.** If you need to make a change that affects both your frontend and backend, then you can do it all in one Git commit and get your changes into production using a single deployment.
- **Tighter integration.** With this setup you can use Django's views to pass context data from the backend to the frontend via templates. In addition, you can do server side rendering (with additional messing around with NodeJS).

The cons are:

- **Single deployment for frontend and backend.** Often you want to just deploy a small CSS or content change to the frontend, or a backend-only change. With this setup, you are forced to always deploy the backend and the frontend together. This means that you need to wait for the frontend to build, even if you didn't make any frontend changes! Even worse, a broken test, or linter error in the _other codebase_ can fail a deployment, if you're using continuous integration practices. You don't want your database migration deployment to fail just because someone forgot to use semicolons in their JavaScript.
- **Tangled tech stack.** Backend devs will need to know a little React, and frontend devs will need to know a little Django for this system to work.
- **Tricksy django-webpack-loader.** Setting up the integration between Webpack and Django has been a painful process for me in the past. I don't remember why, I just remember pain. Truthfully, every option on this list will involve you wanting to throw your computer out of a window at some point, and this one is no exception.

Choose this when:

- You want to keep your infrastructure simple
- You don't care about deployment times
- You typically deploy the frontend and backend together
- You need a tight integration between the frontend and backend (eg. data passing, server-side rendering)

### Option 2 - Completely separate infrastructure

This is an approach that has become more popular over the last several years. In this setup you have two separate codebases, one for the frontend and one for the backend, each with their own Git repository.

The frontend is deployed as a "static site" of just HTML CSS and JavaScript assets. It is hosted separately to Django, in an [AWS S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html), [Netlify](https://www.netlify.com/), or something similar. The frontend is built, tested and deployed independently of the backend. The frontend gets data from the backend soley through REST API calls.

The backend is a Django REST API with no HTML views (other than the admin pages), and hosts no static content (other than what's needed for the admin). It is built, tested and deployed independently of the backend.

Importantly, since the frontend and backend are on different servers, they will also have different domain names. The backend might live on something like api.myapp.com and the frontend on www.myapp.com.

The pros are:

- **Independent deployments.** No waiting on the backend to deploy the frontend and vice versa.
- **Separation of concerns.** Backend developers only need to think about the API, not views or CSS. Frontend developers only need to think in terms of the API presented by the backend, not the internal workings of Django. You _can_ achieve this using option 1, but this method enforces it more strictly.
- **If the backend goes down, the frontend still works.** Your users will still experience errors, but the site won't appear as broken.
- **Security permissions can be split up.** You can split up who is allowed to deploy the frontend vs the backend, typically meaning more people will have the power to deploy, making your team more productive.

The cons are:

- **More infrastructure.** You will need to set up and maintain the static site plus an extra deployment process, which is more work, more complexity.
- **Cross-domain fuckery.** You run into several problems because your frontend is on a different subdomain to your backend. You need to do some extra configuration of your Django settings to allow the frontend to talk to the backend properly. It's a security thing apparently. If you don't fix this you can have issues with making API requests to the backend, receiving cookies, and stuff like that. I don't understand it super well. I don't _want_ to understand it super well. I have better shit to do than figure out the correct value of SESSION_COOKIE_DOMAIN, CORS_ORIGIN_REGEX_WHITELIST and friends. Even worse, cross-domain issues do not crop up on your local machine, because everything is served from localhost, so you need to deploy your configuration before you know if you got it right.

Here are some cross domain Django settings that I hope you never need to think about:

- SESSION_COOKIE_DOMAIN
- CSRF_COOKIE_DOMAIN
- CSRF_TRUSTED_ORIGINS
- CORS_ORIGIN_ALLOW_ALL
- CORS_ALLOW_CREDENTIALS
- CORS_ORIGIN_REGEX_WHITELIST

Choose this when:

- You have separate dedicated frontend and backend developers
- You want to deploy the backend and frontend separately
- You want to _completely_ decouple your backend and frontend infrastructure
- You don't mind a little more operational complexity and configuration

### Option 3 - One server, separate deployments

This approach is an attempted fusion of options 1 and 2. The idea is to still deploy the frontend as a separate static site, but you deploy everything to one server, under a single domain name:

- You have two separate codebases for the backend and frontend respectively
- Both codebases are deployed indepdently, but to the same server
- Both codebases are hosted on a single domain, like wwww.myapp.com

You manage this by using a webserver, like NGINX, which handles all incoming requests. Requests to the URL path /api/ get sent to the WSGI server which runs your Django app (traditional reverse-proxy setup), while all other requests are sent to the frontend, which is set up as a static site and served from the filesystem (eg. /var/www/).

The pros are:

- **Most of the benefits of Option 2.** Separation of concerns and independent deployments are still possible.
- **No "cross-domain fuckery".** Since all requests are served from one domain, you shouldn't need to mess around with all those horrible cross-domain settings in Django.

The cons are:

- **More infrastructure.** This setup is still more complex than the "Cram it all into Django" option.
- **Requires control over host webserver.** You need to be able to install and configure NGINX, deploy files to the filesystem etc. to get this done. This is straightforward if you're using a typical cloud virtual machine, but might be more tricky if you're using something like Heroku (not sure).

Choose this when:

- You want to split up frontend and backend, but you don't need completely separate infrastructure
- You have sufficient control over your host webserver

I'll be honest here. I actually have never tried option 3 (I've used 1 + 2 before). I thought it up when replying to a Reddit post. I think it'll work though. Good luck!
