Title: Studying programming: tools or theory?
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
are going to be complete jibberish. Functional programming is infamous for this kind of techno-babble:

> [A monad is just a monoid in the category of endofunctors, what's the problem?](https://stackoverflow.com/questions/3870088/a-monad-is-just-a-monoid-in-the-category-of-endofunctors-whats-the-problem)

The authors of the Redux docs have the [curse of knowledge](https://en.wikipedia.org/wiki/Curse_of_knowledge). They either don't know that they need to explain these terms, or they don't care to.
You might not have bothered to learn about functional programming, but the authors of Redux did.

Similarly, you don't need to understand hash functions to use Git, but the string of crazy numbers and letters
in your history is going to be quite disorienting: what the fuck is e2cbf1addc70652c4d63fdb5a81720024c9f2677 supposed to mean?

Even simple ideas like the idea of a "tree" data structure helps you work with the computer filesystem more easily.
You might know that recursion is a good method for "walking" trees. Pattern-matching a programming problem
to a data structure will help you come up with solutions much faster.

You can't know beforehand which computer science concepts will be useful.
As far as I can tell, functional programming got "cool" and baked into some frontend tools in the last five years or so. I don't know what's next. You need to get a broad base of knowledge to navigate and demystify the programming landscape.

Ok, so you should:

- isolate yourself in a log cabin for four years
- study computer science
- return to civilisation
- learn Git
- get money

...right?

### What to learn first?

You can't sit down and just learn all of computer science, downloading it all into your brain
like Neo hooked into the Matrix.
You'll also struggle to learn new tools and frameworks without some computer science fundamentals.
So, what to do?

I think you should try a [spiral approach](https://en.wikipedia.org/wiki/Spiral_approach) to learning.
You should learn a some theory, then explore some new tools, then try to build something practical.
Repeat over and over.
You won't necessarily learn everything in the "right order", but new ideas from one area will influence another.
You might:

- run into performance bottlenecks in your code and get interested in computational complexity
- read about "pure functions" in the Redux docs and explore functional programming
- complete a course on [compilers](https://mattsegal.dev/nand-to-tetris.html) and finally understand what all those pesky .class, .pyc and .dll files are doing on your computer

This might seem like a random and haphazard approach, and it kind of is, but I don't think learning
programming should be viewed as a big list of "things you must do". I've written more about that [in this post](https://mattsegal.dev/self-study-mindset-enthusiasm.html).

If you are learning programming and you have only focused on learning frameworks and tools, then I encourage you to mix in some theoretical online courses as well. If you're immersed in a univeristy-style curriculum and haven't tried any modern programming tools - start using them now!
