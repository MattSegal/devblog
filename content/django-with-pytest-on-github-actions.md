Title: How to setup Django with Pytest on GitHub Actions
Description: A minimal example of how you can quickly get Django and Pytest running on every commit to GitHub
Slug: django-with-pytest-on-github-actions
Date: 2022-1-02 12:00
Category: Django

As soon as you know it's going to be a "serious" project you should get it set up to run tests. So like, potentially before you write any code. That's my approach - get it working, write a dummy test. That means that as soon as you start writing features then you have everything you need to write a test. The other scenario is you start adding feature and get swept up in that, and at some point you're like "hmm maybe I should write a test for this..." but if you don't have CI set up already you're more likely to say "nah, fuck it I'll do it later" and not write the test. Getting pytest to work (without Django) on GitHub actions is pretty easy these days.

Anyway that's just my approach. An alternative checkpoint would be as soon as you write your first test, or at the very least around the time of your first deployment.
