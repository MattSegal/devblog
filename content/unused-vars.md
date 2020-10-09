Title: How to highlight unused Python variables in VS Code 
Description: A quick intro to Pylance + VS Code
Slug: pylance-vscode
Date: 2020-10-9 12:00
Category: Programming

I make a lot of stupid mistakes when I'm working on Python code. I tend to:

- make typos in variable names
- accidently delete a variable that's used somewhere else
- leave unused variables lying around when they should be deleted

It's easy to accidentally create code like the image below, where you have unused variables (`y`, `z`, `q`) and references to variables that aren't defined yet (`z`). 

![foo-before]({attach}/img/pylance/foo-before.png)

You'll catch these issues when you eventually try to run this function, but it's best
to be able to spot them instantly. I want my editor to show me something that looks like this:

![foo-after]({attach}/img/pylance/foo-after.png)

Here you can see that the vars `y`, `z` and `q` are greyed out, to show that they're not used. The undefined reference to `z` is highlighted with a yellow squiggle. This kind of instant visual feedback means you can write better code, faster and with less mental overhead.

Having your editor highlight unused variables can also help you remove clutter.
For example, it's common to have old imports that aren't used anymore, like `copy` and `requests` in this script:

![imports-before]({attach}/img/pylance/imports-before.png)

It's often hard to see what imports are being used just by looking, which is why it's nice to
have your editor tell you:

![imports-after]({attach}/img/pylance/imports-after.png)

You'll also note that there is an error in my import statement. `import copy from copy` isn't valid Python. This was an _unintentional mistake_ in my example code that VS Code caught for me.

## Setting this up with VS Code

You can get these variable highlights in VS Code very easily by installing [PyLance](https://devblogs.microsoft.com/python/announcing-pylance-fast-feature-rich-language-support-for-python-in-visual-studio-code/
), and alternative "language server" for VS Code. A language server is a tool, which runs alongside VSCode, that does [static analysis](https://en.wikipedia.org/wiki/Static_program_analysis) of your code.

To get this language server, go into your extensions tab in VS Code, search for "pylance", install it, and then you'll see this popup:

![server-prompt]({attach}/img/pylance/server-prompt.png)

Click "Yes, and reload".

## Alternatives

PyCharm does this kind of [static analysis](https://en.wikipedia.org/wiki/Static_program_analysis) out of the box. I don't like PyCharm quite so much as VS Code, but it's a decent editor and many people swear by it. You can also get this feature by enabling a Python linter in VS Code like flake8, pylint or autopep8. I don't like twiddling with linters, but again other people enjoy using them.

## Next steps

If you're looking for more Python productivity helpers, then check out my blog post on the [Black](https://mattsegal.dev/python-formatting-with-black.html) auto-formatter.



