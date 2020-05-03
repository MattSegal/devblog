Title: Keeping your config files valid with Python
Description: Using Ceberus in Python to keep data structured the way you want
Slug: cerberus-config-validation
Date: 2020-05-03 12:00
Category: Django

It's common to use a config file for your Python projects:
some sort of JSON or YAML document that defines how you program behaves. Something like this:

```yaml
# my-config.yaml
num_iters: 30
population_size: 20000
cycle_type: "long"
use_gpu: true
plots: [population, infections, cost]
```

Storing config in a file is nice because it lets you separate your input data from the code itself,
but it sucks when a bad config file crashes your program. What _really_ sucks is when:

- You don't know exactly which bad value is caused the crash, or how to fix it
- The bad config crashes your program minutes or hours after you first ran it
- Other users write invalid config, then tell you your code is broken

A related issue is when you have complex data structures flying around inside your code: lists of dicts, dicts of lists, dicts of dicts of dicts.
You just have to pray that all the data is structured the way you want it. Sometimes you forget how it's supposed to look in the first place.

You might have tried validating this data yourself using "assert" statments, "if"s and "ValueError"s, but it quickly get tedious and ugly.

### Cerberus

When I run into these kinds of problems, I tend to pull out [Cerberus](https://docs.python-cerberus.org/en/stable/)
to stop the bleeding. It's a small Python library that can validate data according to some schema at runtime.
It's pretty simple to use (as per their docs):

```python
from cerberus import Validator

schema = {'name': {'type': 'string'}}
v = Validator(schema)
v.validate({'name': 'john doe'}) # True
v.validate({'name': 'aaaa'}) # True
v.validate({'name': 1}) # False
v.errors # {'name': ['must be of string type']}
```

You can use this tool to validate all of your loaded config at the _start_ of your program: giving early feedback to the user
and printing a sensible error message that tells them how to solve the problem ("Look at 'name', make it a string!").
This is much better than some obscure ValueError that bubbles up from 6 function calls deep.
It's still not a great experience for non-programmers, but coders will appreciate the clarity.

The Cerberus schema is just a Python dictionary that you define.
Even so, it's quite a powerful system for how basic it is. You can use Ceberus schemas to validate complicated nested data structres if you want to,
even adding custom validation functions and type definitions.
It's particularly nice because it allows you to declare how your data should look, rather than writing a hundred "if" statements.

Here's an example: a YAML config file for training a neural network might look like [this](https://gist.github.com/MattSegal/d813f8d7848b5459f95f5eeacf581d2a) and
you could build a validator for that config like [this](https://gist.github.com/MattSegal/fea30d10d26ef666f3a572e97f03c339). Since everything is just dicts, there's no reason you can't also write your schema as a YAML or JSON ([example](https://gist.github.com/MattSegal/b855659ff40533a9d13935a3ca632f63)).
Luckily Cerberus will validate your schema before applying it, so there is no endless recursion of "who validates the validators?".

### Schema as documenation

I think that defining data schemas using Cerberus gets really useful when lots of different people need to use your config files.
The schema that you've defined also serve as documentation on how to write a correct config file: add a few explanatory comments and you've got some quick-n-dirty docs.
It's not a perfect strategy for writing docs but it has one fantasic property: the documentation cannot lie, because it _actually runs as code_.

I was recently working on an in-house CLI tool for builds and deployment that was written in Python.
I had devs from other teams using the file and I couldn't always show them how to use it in-person.
Even worse I was constantly updating the tool based on feature requests and the config was evolving over time.
Once I had written a Cerberus schema for the tool's config files, I was able to link to the
schema from our documentation. In addition, I was able to run regression tests on "wild" config files
by pulling them down from our source control and checking that they were still valid.

### Limitations

There's no denying that these schemas are very, very verbose: you need to write a lot of text to define even simple data structures.
I think this verbosity caused by the fact that the tool uses built-in Python data structures, rather than an object-oriented DSL.
It's quick and easy to get started, but that comes at a cost.

Another issue is that you can abuse this tool by using it as half-assed type system.
It gives you no type hints or static compilation errors in your IDE: everything happens when the code runs.
Some code quality problems are better solved by investing in static analysis and using tools like [mypy](http://mypy-lang.org/).

Finally, using Cerberus to validate config files and big data structures can hide underlying issues.
I think of it like slapping a bandaid on a problem. It stops the bleeding, but you should also clean up all the broken glass on the floor.
Why do you have all these config files in the first place? Why are you shipping around these big crazy data structures in your code?
It's good to ask these questions and consider alternative solutions.

### Next steps

Give Cerberus a try in your next CLI tool or data science project, you're a quick pip install and a schema definition
from validating your config files.
