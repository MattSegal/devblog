Title: A Django project blueprint to help you learn by doing
Description: I've found that a lot of people on reddit had the same complaint - they had been told to work on a project but didn't know what to build. I made a project template to help with this.
Slug: django-survey-project
Date: 2020-10-03 12:00
Category: Django

There's an awkward point when you're learning Django where you've done the [official tutorial](https://docs.djangoproject.com/en/3.1/intro/install/) and maybe built a simple project, like a to-do list, and now you want to try something a little more advanced. People say that you should "learn by building things", which is good advice, but it leaves you unsure about what to _actually build_. 

In this post I'll share two things:

- a description of a Django project for beginners, which you can build; and
- a short guide on how to design a new website from scratch

I won't introduce many new tools or technical concepts beyond what is already in the Django tutorial. The project can be built using just the basic Django features. There is no need to use REST Framework, JavaScript, React, Webpack, Babel, JSON or AJAX to get this done. Only Django, HTML and CSS are required.

Even though this project only uses simple tools, I think building it is worthwhile for a beginner, since it will introduce you to many of the common themes of backend web development.

# Project overview

In this project, you will build a Django app that runs a survey website. On this site, users can create surveys and send them out to other people to get answers. A user can sign up, create a survey and add multi-choice questions to it. They can then send a survey link to other people, who will answer all the questions. The user who created the survey can see how many people answered, and what percentage of people chose each multi-choice option.

That's the whole app.  I have created a [reference implementation on my GitHub](https://github.com/MattSegal/django-survey) which you can look at if you get stuck when building it yourself.

The project description sounds simple, doesn't it? I thought this would take me 8 hours to design and build, but I spent **20 hours** at the keyboard to get it done. Software projects are hard to estimate before they are built, since they have a [surprising amount of detail](http://johnsalvatier.org/blog/2017/reality-has-a-surprising-amount-of-detail) that you don't think about beforehand.



# Designing the app

So now you know what you're building, but you're not ready to write any code yet. We need to create a design first. As the saying goes: _weeks of coding can save hours of planning_. 

This design will have three parts:

- **User journeys**: where you decide who is using your app and how they will use it
- **Data models**: where you decide how you will structure the database
- **Webpage wireframes**: where you decide what your user interface (UI) will look like

# User journey

The most important thing to do when building a website is to consider the users and their goals. In this case, I think there are two sets of users:

- **Survey takers**: people who want to answer a survey's questions
- **Survey creators**: people who want to create a survey, send it out and view the answers

To better understand who your users are and what they want, you should construct a [user journey](https://en.wikipedia.org/wiki/User_journey) for each of them: a high-level description of the steps that they will need to take to get what they want. This is easily represented as a diagram, created with a free wireframing tool like [Exalidraw](https://excalidraw.com/) or [Wireflow](https://wireflow.co/).

Let's start with the person who is answering the survey, the "survey taker", who has a simple user journey:

![user journey for survey taker]({attach}/img/survey/journey-taker.png)

Next, let's look at the person who created the survey, the "survey creator":

![user journey for survey creator]({attach}/img/survey/journey-creator.png)

Creating these diagrams will force you to think about what you will need to build and why. For example, a survey creator will probably need a user account and the ability to "log in", since they will want private access to their surveys. Lots of thoughts about how to build your app will cross your mind when you are mapping these user journeys.

# Data models

Once you know what your users want to do, you should focus on what data you will need to describe all of the things in your app. So far we have vague ideas of "surveys", "questions", "answers" and "results", but we need a more specific description of these things so that we can write our Model classes in Django.

To better understand your data, I recommend that you create a simple diagram that displays your models and how they relate to each other. Each connection between a model is some kind of foreign key relation. Something like this:

![app data model]({attach}/img/survey/data-model.png)

I explain how I came up with this particular data model in this [appendix page]({filename}/survey/django-survey-project-data-model.md).

You don't need to get too formal or technical with these diagrams. They're just a starting point, not a perfect, final description of how your app will work. Also, the data model which I made isn't the only possible one for this app. Feel free to make your own and do it differently.

# Webpage wireframes

Now we have an idea of how our users will interact with the app and we know how we will structure our data. Next, we design our user interfaces. I suggest you create a rough [wireframe](https://www.usability.gov/how-to-and-tools/methods/wireframing.html) that describes the user interface for each webpage. Creating wireframes for webpages is a good idea for two reasons:

- Wireframing allows you to **quickly** explore different page designs and it forces you to think about how your app needs to work
- It's **much** easier to write HTML and CSS for pages where you already have a simple design to work from

You can use a free wireframing tool like [Exalidraw](https://excalidraw.com/) or [Wireflow](https://wireflow.co/) for these diagrams. Keep in mind that this project doesn't use JavaScript, so you can't get too fancy with custom interactions. You will need to use  [HTML forms](https://developer.mozilla.org/en-US/docs/Learn/Forms) to POST data to the backend.

You can create your own wireframes or you can use the ones that I've already created, which are all listed in this [appendix page]({filename}/survey/django-survey-project-wireframes.md) with some additional notes for each page:

- [Starting the survey]({filename}/survey/django-survey-project-wireframes.md#start)
- [Answering the survey]({filename}/survey/django-survey-project-wireframes.md#answer)
- [Survey submitted]({filename}/survey/django-survey-project-wireframes.md#submit)
- [Landing page]({filename}/survey/django-survey-project-wireframes.md#landing)
- [Signing up]({filename}/survey/django-survey-project-wireframes.md#signup)
- [Logging in]({filename}/survey/django-survey-project-wireframes.md#login)
- [Survey list]({filename}/survey/django-survey-project-wireframes.md#list)
- [Create a survey]({filename}/survey/django-survey-project-wireframes.md#create)
- [Edit a survey]({filename}/survey/django-survey-project-wireframes.md#edit)
- [Add questions to a survey]({filename}/survey/django-survey-project-wireframes.md#addquestion)
- [Add options to a survey question]({filename}/survey/django-survey-project-wireframes.md#addoption)
- [Survey details]({filename}/survey/django-survey-project-wireframes.md#details)

# General advice

Now with some user journeys, a data model and a set of wireframes, you should be ready to start building your Django app. This project blueprint will help you get started, but there is still a lot of work for you to do if you want to build this app. You still need to:

- decide on a URL schema
- create models to represent the data
- create forms to validate the user-submitted data
- write HTML templates to build each page
- add views to bind everything together

There's about 12 views, 12 templates, 5 forms and 5 models to write. Given all this work, it's really important that you **focus** and keep the scope of this project narrow. Keep everything **simple**. Don't use any JavaScript and write as little CSS as possible. Use a CSS framework like [Boostrap](https://getbootstrap.com/docs/4.0/getting-started/introduction/) or [Semantic UI](https://semantic-ui.com/) if you want it to look nice.  Get something simple working **first**, and then you can make it fancy later. If you don't focus, you could spend weeks or months on this project before it's done.

As a specific example, consider the user authentication feature. In this app, your users can log in or sign up. To really make the auth system "complete", you could also add a log out button, a password reset page, and an email validation feature. I think you should skip these features for now though, and get the core functionality working first.

Software projects are never finished, and you can improve this app again and again even after you are "done". Don't try to make it perfect, just finish it.

# Next steps

I hope you find this blueprint project and design guide helpful. If you actually end up building this, send me an email! I'd love to see it. If you like this post and you want to read some more stuff I've written about Django, check out:

- [A beginner's guide to Django deployment](https://mattsegal.dev/simple-django-deployment.html)
- [How to read the Django documentation](https://mattsegal.dev/how-to-read-django-docs.html)
- [How to make your Django project easy to move and share ](https://mattsegal.dev/django-portable-setup.html)
- [How to polish your GitHub projects when you're looking for a job](https://mattsegal.dev/github-resume-polish.html)
- [Tips for debugging with Django](https://mattsegal.dev/django-debug-tips.html)

You can also subscribe to my mailing list below for emails when I post new articles.