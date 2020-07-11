Title: How to polish your GitHub projects when you're looking for a job
Description: How to make a GitHub project look good to impress potential employers
Slug: github-resume-polish
Date: 2020-6-17 12:00
Category: Programming

When you're going for your first programming job, you don't have any work experience or references to show that you can write code. You might not even have a relevant degree (I didn't). What you _can_ do is write some code and throw it up on GitHub to demonstrate to employers that you can build a complete app all by yourself.

A lot of junior devs don't know how to show off their projects on GitHub. They spend _hours and hours_ writing code and then forget to do some basic things to make their project seem interesting. In this post I want to share some tips that you can apply in a few hours to make an existing project much more effective at getting you an interview.

### Remove all the clutter

Your project should only contain source code, plus the minimum files required to run it. It should not not contain:

- Editor config files (.idea, .vscode)
- Database files (eg. SQLite)
- Random documents (.pdf, .xls)
- Media files (images, videos, audio)
- Build outputs and artifacts (\*.dll files, \*.exe, etc)
- Bytecode (eg. \*.pyc files for Python)
- Log files (eg. \*.log)

Having these files in your repo make you look sloppy. Professional developers don't like finding random crap cluttering up their codebase.
You can keep these files out of your git repo using a [.gitignore](https://www.atlassian.com/git/tutorials/saving-changes/gitignore) file. If you already have these files inside your repo, make sure to delete them. If you're using `bash` you can use `find` to delete all files that match a pattern, like Python bytecode files ending in `.pyc`.

```bash
find -name *.pyc -delete
```

You can achieve a similar result in Windows PowerShell, but it'll be a little more verbose.

Sometimes you do need to keep some media files, documents or even small databases in your source control. This is okay to do as long as it's an essential part of running, testing or documenting the code, as opposed to random clutter that you forgot to remove or gitignore. A good example of non-code files that you should keep in source control is website static files, like favicons and fonts.

### Write a README

Your project _must_ have a README file. This is a file in the root of your project's repository called `README.md`. It's a text file written in [Markdown](https://github.com/adam-p/markdown-here/wiki/markdown-cheatsheet) that gives a quick overview of what your project is and what it does. Not having a README makes your project seem crappy, and many people, including me, may close the browser window without checking any code if there isn't one present.

Here's [one I prepared earlier](https://github.com/anikalegal/clerk), and [here's another](https://github.com/AnikaLegal/intake). They're not
perfect, but I hope they give you a general idea of what to do.

One hour of paying attention to your project's README is worth 20 extra hours of coding, when it comes to impressing hiring managers. You know when people mindlessly write that they have "excellent communication skills" on their resume? No one believe that - it's far too easy to just say that. Don't _tell them_ that you have excellent commuication skills, _show them_ when you write an excellent README.

Enough of me waffling about why you should right a README, what do you put in it?

First, you should describe what your project does at a high level: what problem it solves. It is a command line tool that plays music? Is it a website that finds you low prices on Amazon? Is it a Reddit bot that reminds people? A reader should be able to read the first few sentences and decide if it's something they might want to use. You should summarize the main features of your project in this section.

A key point to remember is that the employer or recruiter reading your GitHub is both lazy and time-poor. They might not read past the first few sentences... they might not even read the code! They may well assume that your project works without checking anything. Before you rush to pack your README with features that don't exist, you scallywag, note that they may ask you more about your project in a job interview. So, uh... don't lie about anything.

Beyond a basic overview of your project, it's also good to outline the high-level architecture of your code - how it's structured. For example, in a Django web app, you could explain the different apps that you've implemented and their responsibilities.

If your project is a website, then you can also talk about the production infrastructure that your website runs on. For example:

> This website is deployed to a DigitalOcean virtual machine. The Django app runs inside a Gunicorn WSGI app server and depends on a Postgres database. A seperate Celery worker process runs offline tasks. Redis is responsible for both caching and serving as a task broker.

Or for something a little more simple:

> This project is a static webpage that is hosted on Netlify

Simply indicating that you know how to deploy your application makes you look good. "Isn't that obvious though?" - you may ask. No, it's not obvious and you need to be explicit.

A little warning on READMEs: they're for other people to read, not you. Do not include personal to-dos or notes to yourself in your README. Put those somewhere else, like Trello or Workflowy.

### Add a screenshot

Add a screenshot of your website or tool and embed it in the README, it'll take you 10 minutes and it makes it look way better. Store the screenshot in a "docs" folder and embed it in your README using Markdown. If it's a command line app your can use [asciinema](https://asciinema.org/) to record the tool in action, if your project has a GUI then you can quickly record yourself using the website with [Loom](https://www.loom.com/my-videos). This will make your project seem much more impressive for only a small amount of effort.

### Give instructions for other developers

You should include instructions on how other devs can get started using your project. This is important because it demonstrates that you can document project setup instructions, and also because someone may actually try to run your code. These instructions should state what tools are required to run your project. For example:

- You will need Python 3 and pip installed
- You will need yarn and node v11+
- You will need docker and docker-compose

Next your should explain the steps, with explicit command line examples if possible, that are required to get the app built or running. If your project has external libraries that need to be installed, then you should have a file that specifies these dependencies, like a `requirements.txt` (Python) or `package.json` (Node) or `Dockerfile` / `docker-compose.yaml` (Docker).

You should also include instructions on how to run your automated tests.
You have some tests, right? More on that later.

If you've scripted your project's deployment, you can mention how to do it here, if you like.

### Have a nice, readable commit history

If possible, your git commit history should tell a story about what you've been working on.
Each commit should represent a distinct unit of work, and the commit message should explain what work was done.
For example your commit messages could look like this:

- Added smoke tests for payment API
- Refactored image compression
- Added Windows compatibility

There are differing opions amongst devs on what exactly makes a "good" commit message, but it's very, very clear what bad commit messages look like:

- zzzz
- add code
- more code
- fuck
- remove shitty code
- fuckfuckfuckfuck
- still broken
- fuck Windows
- zzz
- adsafsf
- broken

I for one have written my fair share of "zzz"s. This tip is hard to implement if you've already written all your commits. If you're feeling brave, or if you need to remove a few "fucks", you can re-write your commit history with `git rebase`. Be warned though, you can lose your code if you screw this up.

### Fix your formatting

If I see inconsistent indentation or other poor formatting in someone's code, my opinion of their programming ability drops dramatically.
Is this fair? Maybe, maybe not, but that's how it is. Make sure all your code sticks to your language's standard styling conventions.
If you don't know what those are, find out, you'll need to learn them eventually.
Fixing bad coding style is much easier to do if you use a linter or auto-formatter.

### Add linting or formatting

This one is a bonus, but it's reasonably quick to do. Grab your language community's favorite linter and run it over your code.
Something like `eslint` for JavaScript or `flake8` for Python.
For those not in the know, a linter is a program that identifies style issues in your code.
You run it over your codebase and it yells at you if you do anything wrong. You think your impostor syndrome is bad?
Try using a tool that screams at your about all your shitty style choices.
These tools are quite common in-industry and using one will help you stand out from other junior devs.

Even better than a linter, try using an auto-formatter. I prefer these personally.
These tools automatically re-write your code so they conform with a standard style.
Examples include [gofmt](https://golang.org/cmd/gofmt/) for Go, [Black](https://github.com/psf/black) for Python and
[Prettier](https://prettier.io/) for JavaScript. I've written more about getting started with Black [here](https://mattsegal.dev/python-formatting-with-black.html).

Whatever you choose, make sure you document how to run the linter or formatting tool in your README.

### Write some tests

Automated code testing is an important part of writing reliable professional-grade software.
If you want someone to pay you money to be a professional software developer, then you should demonstrate
that you know what a unit test is and how to write one. You don't need to write 100s of tests or get a high test coverage,
but write a _few_ at least.

Needless to say, explain how to run your tests in your README.

### Add automated tests

If you want to look super fancy then you can run your automated tests in GitHub Actions.
This isn't a must-have but it looks nice.
It'll take you 30 minutes if you've already written some tests and you can put a cool "tests passing" badge in your README that looks really good.
I've written more on how to do this [here](https://mattsegal.dev/pytest-on-github-actions.html)

### Deploy your project

If your project is a website then make sure it's deployed and available online.
If you have deployed it, make sure there's a link to the live site in the README.
This could be a large undertaking, taking hours or days, especially if you haven't done this before, so
I'll leave it to you do decide if it's worthwhile.

If your project is a Django app and you want to get it online, then you might like my guide on [simple Django deployments](https://mattsegal.dev/simple-django-deployment.html).

### Add documentation

This is a high effort endeavour so I don't really recommend it if you're just trying to quickly improve the appeal of your project.
That said, building HTML documentation with something like [Sphinx](https://www.sphinx-doc.org/en/master/) and hosting it on [GitHub Pages](https://pages.github.com/) looks pretty pro. This only really makes sense if your app is reasonably complicated and requires documentation.

### Next steps

I mention GitHub a lot in this post, but the same tips apply for projects hosted on Bitbucket and GitLab. All these tips also apply to employer-supplied coding tests that are hosted on GitHub, although I'd caution you not to spend too much time jazzing up coding tests: too many beautiful submissions end up in the garbage.

Now you should have a few things you can do to spiff up your projects before you show them to prospective employers. I think it's important to make sure that the code that you've spent hours on isn't overlooked or dismissed because you didn't write a README.

Good luck, and please don't hesitate to mail me money if this post helps you get a job.
