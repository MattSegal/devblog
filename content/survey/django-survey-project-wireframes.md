Title: Django project blueprint: wireframes
Description: TODO
Slug: django-survey-project-wireframes
Date: 2020-10-03 12:00
Category: Appendix

This post is an appendix to my post on [designing a Django project]({filename}/survey/django-survey-project.md). In this page I show all the wireframes for the app.

### Page designs: survey taker

Let's look at the survey taker user journey first:


![zzzzzzzzzzzzzzzzzzzzzzzz]({attach}/img/survey/journey-taker.png)

Taken literally, this journey suggests that we should build ~3 pages. 

### Starting the survey

Our first page should be a "landing" page for the survey taker, where we explain what's going on and invite them to take the survey.

![zzzzzzzzzzzzzzzzzzzzzzzz.png]({attach}/img/survey/wireframes/page-start.png)

### Answering the survey

Next, there's the page where they actually answer the questions.

![zzzzzzzzzzzzzzzzzzzzzzzz.png]({attach}/img/survey/wireframes/page-submit.png)

[https://whoisnicoleharris.com/2015/01/06/implementing-django-formsets.html](https://whoisnicoleharris.com/2015/01/06/implementing-django-formsets.html)

[https://jacobian.org/2010/feb/28/dynamic-form-generation/](https://jacobian.org/2010/feb/28/dynamic-form-generation/)

### Survey submitted

Once the survey is submitted, the user should receive confirmation that everything worked so that they don't try to submit the survey again or get frustrated. When they click "submit", let's take them to a "thank you" page.

![zzzzzzzzzzzzzzzzzzzzzzzz-page.png]({attach}/img/survey/wireframes/page-thanks.png)

That's it for the survey taker. Next let's look at the survey creator pages.

**TODO: Overiew diagram**

### Page designs: survey creator

Here's the survey creator user user journey again.

![zzzzzzzzzzzzzzzzzzzzzzzz-journey.png]({attach}/img/survey/journey-creator.png)

The correspondence between this journey and the pages won't be exact, but it'll be pretty close. 

### Landing page

Let's start with the app landing page, where we will explain the app to the user and invite them to log in with a "call to action" ([https://en.wikipedia.org/wiki/Call_to_action_(marketing)](https://en.wikipedia.org/wiki/Call_to_action_(marketing))) button.

![zzzzzzzzzzzzzzzzzzzzzzzz.png]({attach}/img/survey/wireframes/page-landing.png)

### Signing up

We need a signup page for new users to create accounts.

![zzzzzzzzzzzzzzzzzzzzzzzz.png]({attach}/img/survey/wireframes/page-signup.png)

[https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html](https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html)

### Logging in

And a login page for returning users.

![zzzzzzzzzzzzzzzzzzzzzzzz.png]({attach}/img/survey/wireframes/page-login.png)

login view (CCBV)

### Survey list

Where do users go after they log in? There are two viable options. You could send them straight to a "create survey" page, or you could send them to a "list" page, where they can see all their surveys. I chose the list page option, becuase I think it's less disorienting for the user and less complicated to implement.

![zzzzzzzzzzzzzzzzzzzzzzzz.png]({attach}/img/survey/wireframes/page-list.png)

authentication - how can you make sure only users who are allowed to change data can do it?

### Create survey

![zzzzzzzzzzzzzzzzzzzzzzzz.png]({attach}/img/survey/wireframes/page-create.png)

### Edit survey

![zzzzzzzzzzzzzzzzzzzzzzzz.png]({attach}/img/survey/wireframes/page-edit.png)

### Add questions to survey

![zzzzzzzzzzzzzzzzzzzzzzzz-create.png]({attach}/img/survey/wireframes/page-question-create.png)

### Add options to a survey question

![zzzzzzzzzzzzzzzzzzzzzzzz-create.png]({attach}/img/survey/wireframes/page-option-create.png)

### Survey detials

![zzzzzzzzzzzzzzzzzzzzzzzz.png]({attach}/img/survey/wireframes/page-details.png)