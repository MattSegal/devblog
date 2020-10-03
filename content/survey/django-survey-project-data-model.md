Title: Django project blueprint: data model
Description: TODO
Slug: django-survey-project-data-model
Date: 2020-10-03 12:00
Category: Appendix

This post is an appendix to my post on [designing a Django project]({filename}/survey/django-survey-project.md). In this page I explain why I chose to use this data model:

![app data model]({attach}/img/survey/data-model.png)

I created this data model by looking at the user journeys and thinking about what data I would need to make them work. Here's the thought process I used. For defining a new survey we need:

- a **Survey** model to represent each survey
- a link between **Survey** and **User**, because we need to restrict survey access to a particular user, so each survey needs to know which user owns it
- a **Question** model for each question on the survey. Each survey needs to have one or more questions, so we can't hardcode questions as fields, so we create a **Question** model which knows which **Survey** owns it
- each **Question** has one ore more multi-choice answer options,  so we create an **Option** model

Next, I thought about how we would record a survey taker answering the questions. We would need:

- a **Submission** model to represent each survey taker's submission
- a link between**Submission** and  **Survey**, because submissions needs to know which survey it belongs to
- the **Answers** to each question, where the answer is for a particular **Option**
