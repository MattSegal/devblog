Title: A Django project blueprint to help you learn by doing
Description: TODO
Slug: django-survey-project
Date: 2020-10-03 12:00
Category: Django

There's this awkward point when you're learning Django where you've done the [official tutorial](https://docs.djangoproject.com/en/3.1/intro/install/) and maybe built a simple project, like a to-do list, and now you want to try something a *little* more advanced. People say that you should "learn by building things yourself". This is good advice, but it leaves you unsure about what to actually build. 

In this post I'll share two things:

- the blueprints of a "simple" project for beginners, which you can use to build a Django app
- a guide on how to design a new website from scratch

This project will be challenging for a beginner, but I won't introduce many new technical concepts or tools beyond what is already in the Django tutorial. The project can be built using just the basic Django features. There is no need to use Rest Framework, JavaScript, React, Webpack, Babel, JSON or AJAX to get this done. Only Django, HTML and CSS are required.

# Project overview

In this project, you will build a Django app that runs a survey website. On this site, users can create surveys and get answers to their questions. Think of it as an extension of the "polls" app from the official Django tutorial. A user can sign up, create a survey and add multi-choice questions to it. The user can then send a survey link to other people, who will answer all the questions. Once some submissions have been made, the user can see what percentage of people chose each multi-choice option.

That's the whole app. It sounds simple, doesn't it? I thought it would take me 8 hours to design and build, but I spent **~20 hours** at the keyboard to get it done. Software projects are hard to estimate before they are built, since they have a [surprising amount of detail](http://johnsalvatier.org/blog/2017/reality-has-a-surprising-amount-of-detail) that you don't think about beforehand.

Despite being both simple-seeming and suprisingly time-consuming, I think building this project is worthwhile, since it will introduce you to many of the common themes of backend web development. I have created a [reference implementation on my GitHub](https://github.com/MattSegal/django-survey) which you can look at if you get stuck when building it yourself.

# Designing the app

So now we know what we're building, but we're not ready to write any code yet. We need to create a design first. As the saying goes: _weeks of coding can save hours of planning_. 

This design will have three parts:

- **User journeys**: decide who is using our app and how they will use it
- **Data models**: decide how we will structure our database
- **Webpage wireframes**: decide what our UI will look like

# User journey

The most important thing to do when building a user-facing web app is to consider the users and their goals. In this case, I think there are two sets of users:

- **Survey creators**: people who want to create a survey, send it out and view the answers
- **Survey takers**: people who want to answer a survey's questions

Once you know who our users are and what they want, you should construct a "[user journey](https://en.wikipedia.org/wiki/User_journey)" for each of them: a high-level description of the steps that they will need to take to get what they want. This is easily represented as a diagram, created with a free wireframing tool like [Exalidraw](https://excalidraw.com/) or [Wireflow](https://wireflow.co/).

Let's start with the survey taker, who has a simple user journey:

![user journey for survey taker]({attach}/img/survey/journey-taker.png)

Next, let's look at the survey creator's journey when using the app:

![user journey for survey creator]({attach}/img/survey/journey-creator.png)

Creating these diagrams will force you to think about what you will need to build and why. For example, a survey creator will probably need a login, since they want to be the only people updating and viewing their survey.

# Data models

Once you know what our users want to do, you should focus on what data you need to represent the state of your app. So far we've got vague ideas of "surveys", "questions", "answers" and "results", but we need a more specific description of these things, so that we can write our Model classes later.

I suggest you create a quick-and-dirty diagram to display your models and how they relate to each other. Each connection between a model is a kind of foreign key relation.

![app data model]({attach}/img/survey/data-model.png)

I explain why I chose this particular data model in detail in this [appendix page]({filename}/survey/django-survey-project-data-model.md).

You don't need to get too formal or technical with these diagrams. They're just a starting point, not a perfect technical description of how your app will work. Also this isn't the only possible or correct data model for this app - feel free to change this.

# Webpage wireframes

Now that we have an idea of how our user will use the app and the data that we will need, we can create rough wireframes that describe the user interface of each page. Creating these wireframes is a good idea for two reasons:

- Wireframing allows you **quickly** explore different page designs and forces you to think about how you would build your app
- It is **much** easier to write HTML/CSS for pages where you already have a simple design to work from

Since we're not using any JavaScript, we want to keep our user interface simple and only use HTML forms for updating data in the backend. I recommend you use a free wireframing tool like [Exalidraw](https://excalidraw.com/) or [Wireflow](https://wireflow.co/) for these diagrams.

**TODO: Add in wireframes**
The  in this [appendix page]({filename}/survey/django-survey-project-wireframes.md).

# Keep it simple

This project blueprint will help you get started, but there is still a lot of work for you to do if you want to build this app. You still need to:

- decide on a URL schema
- design models to represent the data
- create forms to validate the user-submitted data
- write HTML templates to build each page
- add views to bind everything together

There's at approx 12 views, 12 templates, 5 forms and 5 models to write. Given all this work, it's really important that you **focus** and keep the scope of the project narrow. Keep everything **simple**. Don't use any JavaScript and write as little CSS as possible. Use a CSS framework like Boostrap or Semantic UI.  Get something simple working **first**, and then you can make it fancy later. If you don't focus, you could spend weeks, or months on this project before it's "done".

As a specific example, consider authentication. In this app, your users can log in or sign up. To really make the auth system "complete", you could add a log out button, a password reset page, and an email validation feature. I think you should skip these features for now though, and get the core functionality working first.

Software projects are never finished, and you can improve this app again and again even after you are "done". Don't try to make it perfect, just finish it.

# Next steps

I hope you find this blueprint project and design guide helpful. If you actually end up building this, send me an email! If you like this post and you want to read some more stuff I've written about Django, check out:

- [A beginner's guide to Django deployment](https://mattsegal.dev/simple-django-deployment.html)
- [How to read the Django documentation](https://mattsegal.dev/how-to-read-django-docs.html)
- [How to polish your GitHub projects when you're looking for a job](https://mattsegal.dev/github-resume-polish.html)
- [Tips for debugging with Django](https://mattsegal.dev/django-debug-tips.html)

You can also subscribe to my mailing list below for emails when I post new articles.