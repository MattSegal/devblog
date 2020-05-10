Title: Studying programming: tools or concepts?
Description: Mindsets and strategies for choosing what to learn
Slug: self-study-tools-vs-concepts
Date: 2020-05-10 12:00
Category: Programming

When you're studying web development you have a lot to learn and limited time.
One of the hard choices that you'll need to make is whether you learn tools or concepts.
Should you study data structures and algorithms to be a web developer?
It seems kind of esoteric.
Do you just need to learn a bunch of the latest tools and frameworks to be productive?
I'm going to argue that you need both: learning concepts makes you better at using tools, and using tools motivates you to learn concepts.

### The case for learning tools

The case for learning tools and frameworks is the strongest so let's get it out of the way: they make you more productive.
I can use [Django](https://www.djangoproject.com/) to build a website with
authentication, permissions, HTML templating, database models, form validation, etc. in half a day.
Writing any one of these features from scratch would take me days at the very least.
You do not want to invent the 2020 programmer's toolchain from scratch, not if you want to get anything done.

In addition, employers want you to know how to use tools.
Programmers get paid to ship valuable code, not to know a bunch of stuff.
Job advertisments are primarily a list of [React](https://reactjs.org/), [Spring](https://spring.io/), [Webpack](https://webpack.js.org/), [NuxtJS](https://nuxtjs.org/), Django, [Rails](https://rubyonrails.org/), etc.
Contrary to how it might seem, you can get these jobs without knowing every technology on the list,
but you do need to know at least some of them.
Good luck getting a coding job if you don't know Git.

Ok, so we're done right? Tools win, fuck ideas. Learn Git, get money.

### The case for learning ideas

You can't just learn tools and frameworks. If you do not know [how the internet works](https://www.youtube.com/watch?v=DTQV7_HwF58),
then you're going to spend your time as a web developer swimming in a meaningless word-soup of "DNS", "TCP" and "Headers".
Django's database model structure is going to be very confusing if you don't know what "database normalisation" is.
How will you debug issues that don't already have a StackOverflow post written for then?

Ok cool, so you need to learn some basic internet stuff, but do you really need to learn about computational complexity?
Do you have to be able to [invert a binary tree](https://twitter.com/mxcl/status/608682016205344768?lang=en)?

Well, no: you don't _have_ to learn these theoretical computer-sciency concepts to get a job as a programmer.
That said, I think it's in your interest to learn theoretical stuff.
Learning computer-sciency concepts help you learn new tools faster and use them better.
If you've learned a little bit of [functional programming](https://en.wikipedia.org/wiki/Functional_programming) then you'll find a lot of familliar concepts when reading the [Redux documentation](https://redux.js.org/basics/reducers):

> The reducer is a pure function that takes the previous state and an action, and returns the next state.

If you haven't been exposed to functional programming concepts, then words like "state", "pure function" and "immutability"
are going to be complete jibberish. The authors of the docs have the [curse of knowledge](https://en.wikipedia.org/wiki/Curse_of_knowledge). They either don't know that they need to explain these terms, or they don't care to.
You might not have bothered to learn about functional programming, but the authors of Redux did.

Similarly, you don't need to understand hash functions to use Git, but the string of crazy numbers and letters
in your history is going to be quite disorienting: what the fuck is e2cbf1addc70652c4d63fdb5a81720024c9f2677 supposed to mean?

Even simple ideas like the idea of a "tree" data structure helps you work with the computer filesystem more easily.
You might know that recursion is a good method for "walking" trees. Pattern-matching a programming problem
to a data structure will help you come up with solutions much faster.

You can't know beforehand which computer science concepts will be useful for your tools.
As far as I can tell, functional programming got "cool" and baked into tools in the last five years or so when the JavaScript ecosystem
started flourishing. I don't know what's next. You need to get a broad base of knowledge to navigate
and demystify the programming landscape.

Ok, so you should:

- isolate yourself in a log cabin for four years
- study computer science
- return to civilisation
- learn React
- get money

Right?

### What to learn first?

- you cannot and will not learn all the concepts or all the tools up front, sample and cycle

you want to learn functional programming because you read the redux docs

- guitar teacher taught me upward spiral
- rhythm, then melody, then harmony,
- no guitar player goes into a cave for a month and practices nothing but rhythm

* you will never understand security, but every time you will know a little more
