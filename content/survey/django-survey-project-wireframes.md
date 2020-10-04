Title: Django project blueprint: wireframes
Description: Wireframe appendix for the Django project blueprint post
Slug: django-survey-project-wireframes
Date: 2020-10-03 12:00
Category: Appendix

This post is an appendix to my post on [designing a Django project]({filename}/survey/django-survey-project.md). This page shows all the wireframes for the app, with some additional notes for each page.

<h1>Page designs for the user who answers the survey</h1>

This section covers the pages required for the "survey taker" user journey:

![journey for survey taker]({attach}/img/survey/journey-taker.png)

Taken literally, this journey suggests that we should build ~3 pages. 

<h2 id="start">Starting the survey</h2>

The person taking the survey should start on a "landing" page, where we explain what's going on and invite them to take the survey.

![landing]({attach}/img/survey/wireframes/page-start.png)

The "start survey" button can just be a link to the next page.

<h2 id="answer">Answering the survey</h2>

Next, we need a page for the survey taker to actually answer the questions.

![survey answering page]({attach}/img/survey/wireframes/page-submit.png)

You will need to render all of the questions on the survey inside an HTML form. The "submit" button should trigger a POST request to the backend. 


If you want to answer multiple questions on one page, then you will need to use a more advanced feature of Django: a formset. I found [this blog post](https://whoisnicoleharris.com/2015/01/06/implementing-django-formsets.html) and [this other one](https://jacobian.org/2010/feb/28/dynamic-form-generation/) useful for creating my formsets, along with the [official Django docs on formsets](https://docs.djangoproject.com/en/3.1/topics/forms/formsets/).

Alternatively, you could have one page per question, which would mean splitting up this single page across multiple pages, but it would make your Django forms simpler.

<h2 id="submit">Survey submitted</h2>

Once the user submits their answers for the survey, they should then receive confirmation that everything worked so that they don't try to submit the survey again or get frustrated. When they click "submit", let's take them to a "thank you" page.

![thanks page]({attach}/img/survey/wireframes/page-thanks.png)

That's it for the survey taker. Next let's look at the survey creator pages.

<h1 >Page designs for the user who creates the survey</h1>

Here's the "survey creator" user journey again.

![creator journey]({attach}/img/survey/journey-creator.png)

The correspondence between this journey and the pages won't be exact, but it'll be pretty close. 

<h2 id="landing">Landing page</h2>

We should start the user's experience with a landing page, where we will explain the app to the user and invite them to log in with a [call to action](https://en.wikipedia.org/wiki/Call_to_action_(marketing)) button.

![landing page]({attach}/img/survey/wireframes/page-landing.png)

The button can just be a link to the login or signup page. If you're not sure what to write for the landing page, check out [this article](https://stackingthebricks.com/how-i-increased-conversion-2-4x-with-better-copywriting/).

<h2 id="signup">Signing up</h2>

We need a signup page for new users to create accounts.

![sign up]({attach}/img/survey/wireframes/page-signup.png)

There should also be a link to the log in page from the signup page, just in case a user who alread has an account gets lost. This [blog post](https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html) is a good guide for how to create a sign up view in Django.

<h2 id="login">Logging in</h2>

We also need a login page for returning users.

![login page]({attach}/img/survey/wireframes/page-login.png)

Use a [LoginView](https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.LoginView) for the log in view. More details on this view class at [CCBV](https://ccbv.co.uk/projects/Django/3.0/django.contrib.auth.views/LoginView/). There should be a link to the signup page from the login page.

<h2 id="list">Survey list</h2>

Where do users go after they log in? There are two viable options. You could send them straight to a "create survey" page, or you could send them to a "list" page, where they can see all their surveys. I chose the list page option, becuase I think it's less disorienting for the user and less complicated to implement.

![survey list]({attach}/img/survey/wireframes/page-list.png)

For this page to work you'll need to grab all of the Survey objects that the user has created and list them in the HTML template. 

In this wireframe, a survey can be either in an "active" or "editing" state, where if the survey is "active" then the user can view the results and if it is "editing" then they can add more questions.

This is the first page we've seen that is specific to one user. You need to implement [authorization](https://en.wikipedia.org/wiki/Authorization) so that one user cannot spy on another user's surveys.

<h2 id="create">Create survey</h2>

On this page a user types in the name of a new survey, and presses "create survey" to create a new survey with that name.

![create survey]({attach}/img/survey/wireframes/page-create.png)

This can be implented with a HTML form which sends a POST request to a Django view. You will need a Django Form to validate the data.

I have broken the "survey creation" pages (this page an the ones after it) up into many stages to try and make the Django views simple. This is not the only way to design pages for the "survey creation" feature, and you can do this differently, with fewer pages, if you like. 

You will need to think about authorization for this view, and all the other views where the user can change data. We don't want users to be able to change the data of other users. You will need to write some code in your views to check that the user who is changing some data is also the user who owns it.

<h2 id="edit">Edit survey</h2>

On this page a user can add questions to the survey they just created. 

![edit survey]({attach}/img/survey/wireframes/page-edit.png)

Clicking "add another question" takes the user to a seperate "add question" page.
The user can add as many questions as they like until they are ready to make the survey "active".

When they click "start survey", the button should use an HTML form to send a POST request to a Django view which moves the survey from "edit mode" to "active mode".

<h2 id="addquestion">Add a question to survey</h2>

On this page the user can create a new question for the survey. They type in the prompt for the question, like "what is your favourite colour?" and then click "add question" to create the new question.

![create questions]({attach}/img/survey/wireframes/page-question-create.png)

<h2 id="addoption">Add options to a new question</h2>

On this page the user can add multiple options to a question that they just created.

![add options]({attach}/img/survey/wireframes/page-option-create.png)

<h2 id="details">Survey details</h2>

This is the final page that a user who is running a survey wants to look at. They will view this dashboard to check the answers of a survey that they've created and sent out.

This page tells the user how many people have answered their survey and what percentage of people chose each answer.

![survey details]({attach}/img/survey/wireframes/page-details.png)

You will need to do a bit of maths in the view for this page. You can calculate the percentages using some fancy database queries using [aggregation](https://docs.djangoproject.com/en/3.1/topics/db/aggregation/). Otherwise you can query the Survey model, its Questions and all of its Submissions and their Answers. Once you have pulled all the data you need into memory, then you can write a for loop or something to do the percentage calculations. I recommend using `filter` and `count` in your queries.

When thinking about database queries for this view, you should imagine that you have thousands of surveys and each survey has dozens of questions and hundreds of answers.

You will need to implement authorization on in this page's view so that only the user who created the survey can view the results.
