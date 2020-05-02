Title: 8 helpful tools for programming on Windows
Description: Some helpful tools for setting up a Windows laptop for programming
Slug: windows-setup-programming
Date: 2020-05-02 12:00
Category: Programming

Software development on Windows can be a pain. Not because of any issues with C#, .NET
or the operating system, but simply because the tools surrounding your work can be quite clunky by default.
I'm talking about the lack of a package manager, PowerShell's ugly blue terminal with no tabs and a bunch of "missing" tools (git, ssh).
It's like a living room where all the furniture is perfectly positioned to stub your toe.

That said, you can get have a pretty nice developer experience if you install a few tools.
This post goes over my preferred setup on a new Windows laptop. It's not a definitive guide, just some tips and
tricks that I've picked up from other devs that I've worked with. Hopefully you find some of them useful.

The post below summarises everything in this video.

<div class="yt-embed">
    <iframe 
        src="https://www.youtube.com/embed/wMJJp1PbQQA" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen
    >
    </iframe>
</div>

### ConEmu console emulator

[ConEmu](https://conemu.github.io/) my #1 favourite tool for Windows. It allows you to:

- Open many PowerShell tabs in one window
- Show and hide the terminal with a hotkey (ctrl-`)
- Split your windows into sub-windows using hotkeys (ctrl-shift-(o|e))
- Open different shells in one window (PowerShell, Git Bash, cmd)
- Customise your terminal (different colors etc)
- Open PowerShell as Admin automatically

It's like removing a rock from your shoe: an ugly blue rock.
Some people also like to use [Cmder](https://cmder.net/) for the same use-case.

### Everything search

Windows Explorer search is so horribly broken in 2020 that you _hope_ Microsoft is trolling you,
because the alternative is just sad. In any case [Everything](https://www.voidtools.com/support/everything/)
gives you very fast search of all your files and folders, including that pesky InternalToolChain.dll
which has gone missing.

I believe it runs in the background all the time, quietly indexing your files.
I do not how this affects your workstation's performance.

### Chocolatey package manager

[Chocolatey](https://chocolatey.org/) is the (unofficial) package manager for Windows.
[NuGet](https://www.nuget.org/) is good for installing your .NET libraries, while `choco` is good for everything else.
It's great for quickly installing tools and automating the process. It's quite easy to [install](https://chocolatey.org/install).

To install a tool like Everything, you can just [search for it](https://chocolatey.org/search?q=everything) then run the install from the CLI:

```powershell
choco install everything
```

In fact, once you've got choco installed, you can install all of the other tools on this list with:

```powershell
choco install git -y
choco install conemu -y
choco install everything -y
choco install poshgit -y
choco install vscode -y
choco install ag -y
```

Try not to install anything with Chocolatey if it already exists: things can get weird. You can always run `Get-Command` in PowerShell to check for existing executables:

```powershell
Get-Command python
```

### Visual Studio Code

[Visual Studio Code](https://code.visualstudio.com/) is a text editor that strikes a great balance between being full-featured and overly bloated.
This is an obvious proposition to more experienced developers, but there are a lot of beginners out there editing their files in `notepad.exe`.
I personally prefer it to slimmer alternatives like Sublime Text 3 and hulking behemoths like PyCharm or Visual Studio.

A really cool feature of VSCode on Windows is that it's quite command-line friendly. You can open the current folder in VSCode from the CLI with:

```powershell
code .
```

or you can open a single file like this:

```powershell
code my-file.txt
```

I'm quite a fan of the [Monokai ST3 theme](https://marketplace.visualstudio.com/items?itemName=AndreyVolosovich.monokai-st3) and the [Materoal Icon Theme](https://github.com/PKief/vscode-material-icon-theme), plus a bajillion other language-specific extensions.

[Sublime Text 3](https://www.sublimetext.com/3) is a popular alternative with a rich plugin ecosystem but less features out-of-the box.
Some people also like [Notepad++](https://notepad-plus-plus.org/downloads/), a decision I don't really understand, but as the name suggests,
it beats the shit out of just using Notepad.

### PowerShell setup

There's a few tricks to getting PowerShell into a usable state on a new Windows machine.
The first thing is to always open as Administrator, if you can.
Once PowerShell is open, I like set the "execution policy", which allows you to run scripts:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass
```

Now you can put some PowerShell in a script, like myscript.ps1:

```powershell
# myscript.ps1
Write-Host "Hello World!"
```

and then run it from your PowerShell terminal

```powershell
./myscript.ps1
# Hello World!
```

Finally, I like to configure my profile, which is a script that runs before every PowerShell session starts.
This is where you can add things like welcome messages, function definitions and module imports.
To set up your profile, just open `$profile`, add some stuff and then save the file. For example:

```powershell
code $profile
```

One other handy PowerShell tip while I'm here: you can open folders in explorer with `explorer`, and, if you're not using VSCode,
you can still edit files using `notepad`:

```powershell
explorer .
explorer "C:\Users\mattd"
notepad "secret-plot.txt"
```

### Git for Windows

This one also seems kind of obvious if you're already using [Git](https://git-scm.com/download/win),
and if you're not using Git then why would you bother?
Wait! There's more than just `git` in Git for Windows. The install also gives you:

- Git Bash, which is a bash shell that can run scripts
- `ssh` for logging into Linux servers
- `scp` for transfering files to Linux servers

* `ssh-keygen` for generating SSH keys

- A bunch of nice Unix tools like `find`

You'll never need ot use [PuTTY](https://www.putty.org/) again! You might scoff at my promotion of Git Bash:

> Fool! Doesn't he know about [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10)?

WSL seems nice, but a lot of workplaces won't let you install it, but they will allow Git.

### Posh-Git: a PowerShell environment for Git

[Posh-Git](https://github.com/dahlbyk/posh-git) gives you a nice little Git status message in your command prompt.
It tells you the current branch that you're on and the number un-comitted changes. It's quite convenient. To install it:

```powershell
Install-Module posh-git -Scope CurrentUser -Force
```

And then to activate it:

```powershell
Import-Module posh-git
```

Note that it will only display your Git status when the current directory is a Git repo.
Consider placing the import statement into your PowerShell profile so that it loads automatically for you.

### The Silver Searcher

The [Silver Searcher](https://github.com/ggreer/the_silver_searcher) is a nice little CLI tool for quickly finding all
instances of a string in a folder. For example if I want to find all instances of "probably" in my "contents" folder:

```powershell
ag -i probably content
```

Its main appeal is speed: it's really fucking fast. Git grep is also a contender if you're working in a Git repository:

```powershell
git grep probably
```

### Next steps

Despite Steve Ballmer's [pro-dev yelling](https://www.youtube.com/watch?v=Vhh_GeBPOhs) in the 2000s, Microsoft
dropped the ball on making Windows nice for developers. Nevertheless you can use these tools, and others, to cobble together an environment where
building software isn't like stubbing your toe on every piece of furniture. If you haven't tried these tools already, then I encourage you to install them and have a play around. You might find your coding experience a little less painful.
