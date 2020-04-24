Title: Never think about Python formatting again
Description: Why you should give the black auto formatter a try
Slug: python-formatting-with-black
Date: 2020-04-24 12:00
Category: Programming

At some point you realise that formatting your Python code is important.
You want your code to be readable, but what's the _right_ way to format it?
You recognise that it's much harder to read this:

```python
some_things = {"carrots": [1,2 ],
"apples":[
3,3, 3
], "pears": [] }
```

than it is to read this:

```python
some_things = {
    "carrots": [1, 2],
    "apples": [3, 3, 3],
    "pears": [],
}
```

or... wait should it be like this instead? Hmm...

```python
some_things = {
    "carrots": [1, 2],
    "apples":  [3, 3, 3],
    "pears":   [],
}
```

nah, nah, wait a sec maybe would be better if we kept in on one line to save space...

```python
some_things = {"carrots": [1, 2], "apples":  [3, 3, 3], "pears": []}
```

Umm, is that line too long though? We could do this for hours.

Formatting your code _is_ important, but it's easy to get lost in the details.
You want your code to look professional, but it can be a time-sink. It's easy to:

- spend time experimenting with different formatting styles
- spend ages twiddling with linter (eg. PyLint) rules, and then spend cumulative hours tweaking your code to make the linter stop yelling at you
- fight a co-worker to the death on top of a castle tower in a thunderstorm over the proper way to lay out brackets

This is all just incidental bullshit though. It's a distraction from your real work: laying out brackets one way or another isn't going to make your software run any better (but if the closing bracket isn't on its own new line then I'll gut you like the dog you are!).

Is there a way to avoid this mess? How can we get rid of all this incidental work?

### Give black a try

[Black](https://github.com/psf/black/) is a tool that auto-formats your Python code. You jut run black over all your .py files and the correct formatting is applied for you. It's like [prettier](https://prettier.io/), but for Python instead of JavaScript.

Importantly, Black has minimal configuration. You basically only get to choose the maximum line length that you want, and everything else is decided by the formatter. It's the "uncompromising Python code formatter". This means you don't get to choose what formatting style you use, but it also means you don't need to decide either: once you've adopted Black, you _never need to think about Python formatting again_. No more config files, no more arguing with your coworkers. Spend your time on more valuable things, like what your code is doing.

Is it safe to just run your whole codebase through this tool? I think so. Black compares the Python [abstract syntax tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree) of the code before and after the changes, just to make sure it didn't change or break anything. In the last few jobs I've worked, I've walked in, made the case for Black (politely), and run it over the whole codebase. It's never caused any issues.

Here's some of the other benefits of Black:

- **Less work when coding**: all the time you spend manually formatting your code can now be spent writing more code, or thinking, or something.
- **More productive pull requests**: the person reviewing your code can't [bikeshed](https://en.wiktionary.org/wiki/bikeshedding) your formatting, because it's out of your hands - instead they'll need to actually look at what your code is doing.
- **Smaller diffs in source control**: there will be no formatting changes applied between commits, so the only changes left are meaningful ones. In addition, their formatting style is optimised around minimising diffs.
- **Keep the linter off your back**: if you are also using a linter like flake8, then black will help you avoid basic [PEP 8](https://www.python.org/dev/peps/pep-0008/) errors.
- **Auto format on save in your IDE**: This one is huuuuge. You can set up black to reformat your code _as you write it_. I've found this helps me write code much faster.

### Running black

You have to install it.

```bash
pip install black
```

Then you run it with a path as an argument

```bash
black .
```

Then it mangles all of your code!

```text
reformatted /home/matt/code/redbubble/colors.py
reformatted /home/matt/code/redbubble/fuzzer.py
reformatted /home/matt/code/redbubble/image.py
reformatted /home/matt/code/redbubble/sierpinski.py
All done! ✨ 🍰 ✨
4 files reformatted, 2 files left unchanged.
```

You can mess around a little bit with the line length config, or using pyproject.toml, but that's basically it.

If you're running CI and you want to check for correct formatting, you can use

```bash
black --check .
```

It returns exit code 0 if the formatting is correct, and exit code 1 if it's not.

### Format on save

Format on save is incredible, it's been a big productivity boost for me. In VSCode you can add the following settings to format on save with black:

```json
{
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

I don't know about other editors, but I've set this up in PyCharm as well. Once that's done then any save will format the document. Here's an example:

<div class="loom-embed"><iframe src="https://www.loom.com/embed/a5914312a4ff44d188f019bb63e19bf7" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

### Limitations

Black is a just formatter, not a linter, so it does not do some linting functions. It will not complain about unused variables, imports and other linty stuff.

It will also not do import sorting like [isort](https://github.com/timothycrosley/isort). In fact, Black and isort can fight over how imports should be formatted, if you're running both of them. You can resolve it by running isort then black, or vice versa, but it can make CI tests a little awkward.

Finally, it's "in beta", which as far as I can tell just means "you should expect some formatting to change in the future".

### Summary

Black is awesome, it'll save you time and brain cycles, go forth and use it on all your Python code.
