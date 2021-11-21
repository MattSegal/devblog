Title: DevOps in academic research
Description: Some things I learned supporting infectious disease epidemiologists
Slug: devops-academic-research
Date: 2021-11-21 12:00
Category: Programming

I'd like to share some things I've learned and done in the 18 months I worked as a "Research DevOps Specialist" for some infectious disease [epidemiologists](https://www.bmj.com/about-bmj/resources-readers/publications/epidemiology-uninitiated/1-what-epidemiology).
Prior to this job I'd worked as a web developer for four years and I'd found that the day-to-day had become quite routine. Web dev is a mature field where most of the hard problems have been solved. Looking for something new, I started a new job at a local university in early 2020. The job was created when my colleagues wrote ~20k lines of Python code and then found out what a pain in the ass it is to maintain a medium-sized codebase. It's the usual story: the code is fragile, it's slow, it's easy to break things, changes are hard to make. I don't think this situation is anyone's fault per-se: it arises naturally whenever you write a big pile of code.

In the remainder of this post I'll talk about the application we were working on and the awesome, transformative, <superlative\> power of:

- mapping your workflow
- an automated test suite
- performance improvements
- task automation
- visualisation tools; and
- data management

If you're a web developer, you might be interested to see how familar practices can be applied in different contexts. If you're an academic who uses computers in your work, then you might be interested to learn how some ideas from software development can help you be more effective.

## The application in question

We were working on a [compartmental](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology) infectious disease model to simulate the spread of tuberculosis. Around March 2020 the team quickly pivoted to modelling COVID-19 as well (surprise!). There's documentation [here](http://summerepi.com/) with [examples](http://summerepi.com/examples/index.html) if you want to poke around.

In brief, it works like this: you feed the model some data for a target region (population, demographics, disease attributes) and then you simulate what's going to happen in the future (infections, deaths, etc). This kind of modelling is useful for exploring different scenarios, such as "what would happen if we closed all the schools?" or "how should we roll out our vaccine?". These results are presented to stakeholders, usually from some national health department, via a PowerBI dashboard. Alternatively the results are included in a fancy academic paper as graphs and tables.

![notifications]({attach}/img/devops-academia/notifications.png)

(Note: "notifications" are the infected cases that we know about)

A big part of our workflow was model calibration. This is where we would build a disease model with variable input parameters, such as the "contact rate" (proportional to how infectious the disease is), and then try to learn the best value of those parameters given some historical data (such as a timeseries of the number of cases). We did this calibration using a technique called [Markov chain Monte Carlo](https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo) (MCMC). MCMC has many nice statistical properties, but requires running the model 1000 to 10,000 times - which is quite computationally expensive.

![calibration]({attach}/img/devops-academia/calibration.png)

This all sounds cool, right? It was! The problem is that when I started. the codebase just hadn't been getting the care it needed given its size and complexity. It was becoming unruly and unmanageable. Trying to read and understand the code was stressing me out.

Furthermore, running calibrations was _slow_. It could take days or weeks. There was a lot of manual toil where someone needed to upload the application to the university computer cluster, babysit the run and download the outputs, and then post-process the results on their laptop. The execution of the code itself took days or weeks. This time-sink is a problem when you're trying to submit an academic paper and a reviewer is like "hey can you just re-run everything with this one small change" and that means re-running days or weeks of computation.

So there were definitely some pain points and room for improvement when I started.

## Improving our workflow with DevOps

The team knew that there were problems and everybody wanted to improve the way we worked. If I could point to any key factor in our later succeses it would be their willingness to change and openness to new things.

I took a "DevOps" approach to my role (it was in the job title after all). What do I mean by DevOps? This [article](https://www.atlassian.com/devops/what-is-devops) sums it up well:

> a set of practices that works to automate and integrate the processes between [different teams], so they can build, test, and release software faster and more reliably

Traditionally this refers to work done by Software **Dev**elopers and IT **Op**eration**s**, but I think it can be applied more broadly. In this case we had a software developer, a mathematician, an epidemiologist and a data visualisation expert working on a common codebase.

A key technique of DevOps is to think about the entire system that produces finished work. You want to conceive of it as a kind of pipeline to be optimised end-to-end, rather than focusing on any efficiencies achieved by individuals in isolation. One is encouraged to explicitly map the flow of work through the system. Where does work come from? What stages does it need to flow through to be completed? Where are the bottlenecks? Importantly: what is the goal of the system?

In this case, I determined that our goal was to produce robust academic research, in the form of published papers or reports. My key metric was to minimise "time to produce a new piece of research", since I believed that our team's biggest constraint was time, rather than materials or money or ideas or something else. Another key metric was "number of errors", which should be zero: it's bad to publish incorrect research.

If you want to read more about DevOps I recommend checking out [The Phoenix Project](https://www.goodreads.com/book/show/17255186-the-phoenix-project) and/or [The Goal](https://www.amazon.com.au/Goal-Process-Ongoing-Improvement/dp/0884271951) (the audiobooks are decent).

## Mapping the workflow

As I mentioned, you want to conceive of your team's work as a kind of pipeline. So what was our pipeline? After chatting with my colleagues I came up with something like this:

![workflow]({attach}/img/devops-academia/autumn-workflow.png)

It took several discussions to nail this process down. People typically have decent models of how they work floating around in their heads, but it's not common to write it out explicitly like this. Getting this workflow on paper gave us some clear targets for improvement. For example:

- Updating a model required tedious manual testing to check for regressions
- The update/calibrate cycle was the key bottleneck, because calibration ran slowly and manual steps were required to run long jobs on the compute cluster
- Post processing was done manually and was typically only done by the one person who knew the correct scripts to run

## Testing the codebase

My first concern was testing. When I started there were no automated tests for the code. There were a few little scripts and "test functions" which you could run manually, but nothing that could be run as a part of [continuous integration](https://www.atlassian.com/continuous-delivery/continuous-integration).

This was a problem. Without tests, errors will inevitably creep into the code. As the complexity of the codebase increases, it becomes infeasible to manually check that everything is working since there are too many things to check. In general writing code that is correct the first time isn't too hard - it's not breaking it later that's difficult.

In the context of disease modelling, automated tests are even more important than usual because the correctness of the output cannot be easily verified. The whole point of the system is to calculate an output that would be infeasible for a human to produce. Compare this scenario to web development where the desired output is usually known and easily verified. You can usually load up a web page and click a few buttons to check that the app works.

## Smoke Tests

So where did I start? Trying to add tests to an untested codebase with thousands of lines of code is very intimidating. I couldn't simply sit down and write unit tests for every little bit of functionality because it would have taken weeks. So instead I wrote "smoke tests". A smoke test runs some code and checks that it doesn't crash. For example:

```python
def test_covid_malaysia():
    """Ensure the Malaysia region model can run without crashing"""
    # Load model configuration.
    region = get_region("malaysia")
    # Build the model with default parameters.
    model = region.build_model()
    # Run the model, don't check the outputs.
    model.run_model()
```

To some this may look crimininally stupid, but these tests give fantastic bang-for-buck. They don't tell you whether the model outputs are correct, but they only takes a few minutes to write. These tests catch all sorts of stupid bugs: like someone trying to add a number to a string, undefined variables, bad filepaths, etc. They doesn't help so much in reducing semantic errors, but they do help with development speed.

## Continuous Integration

A lack of testing is the kind of problem that people don't know they have. When you tell someone "hey we need to start writing tests!" the typical reaction is "hmm yeah sure I guess, sounds nice..." and internally they're thinking "... but I've got more important shit to do". You can try browbeating them by telling them how irresponsible they're being etc, but that's unlikely to actually get anyone to write and run tests on their own time.

So how to convince people that testing is valuable? You can _show_ them, with the magic of ✨continuous integration✨. Our code was hosted in GitHub so I set up GitHub Actions to automatically run the new smoke tests on every commit to master. I've written a short guide on how to do this [here](https://mattsegal.dev/pytest-on-github-actions.html).

This setup makes tests visible to everyone. There's a little tick or cross next to every commit and, importantly, next to the name of the person who broke the code.

![test-failures]({attach}/img/devops-academia/test-failures.png)

With this system in place we eventually developed new norms around keeping the tests passing. People would say "Oops! I broke the tests!" and it became normal to run the tests locally and fix them if they were broken. It was a little harder to encourage people to invest time in writing new tests.

Once I become more familiar with the codebase I eventually wrote integration and unit tests for the critical modules. I've written a bit more about some testing approaches I used [here](https://mattsegal.dev/alternate-test-styles.html).

Something that stood out to me in this process was that perhaps the most valuable thing I did in that job was one of the easiest things to do. Setting up continuous integration with GitHub took me an hour to two, but it's been paying dividends for ~2 years since. How hard something is to do and how valuable it is are different things.

{% from 'mail.html' import mailchimp %}
{{ mailchimp("Get alerted when I publish new blog posts", "Enter your email address", "Subscribe") }}

## Performance improvements

The code was too slow and the case for improving performance was clear. Slowness can be subjective, I've [written a little](https://mattsegal.dev/is-django-too-slow.html) about the different meanings of "slow" in backend web dev, but in this case having to wait 2+ days for a calibration result was obviously way too slow and was our biggest productivity bottleneck.

The core of the problem was that a MCMC calibration had to run the model over 1000 times. When I started, a single model run took about 2 minutes. Doing that 1000 times means ~33 hours of runtime per calibration. Our team's mathematician worked on trying to make our MCMC algorithm more sample-efficient, while I tried to push down the 2 minute inner loop.

It wasn't hard to do better, since performance optimisation hadn't been a priority so far. I used Python's cProfile module, plus a few visualisation tools to find the hot parts of the code and speed them up. [This article](https://julien.danjou.info/guide-to-python-profiling-cprofile-concrete-case-carbonara/) was a lifesaver. In broad strokes, these were the kinds of changes that improved performance:

- Avoid redundant re-calculation in for-loops
- Switching data structures for more efficient value look-ups (eg. converting a list to a dict)
- Converting for-loops to matrix operations ([vectorisation](https://en.wikipedia.org/wiki/Vectorization))
- Applying JIT optimisation to hot, pure, numerical functions ([Numba](https://numba.pydata.org/))
- Caching function return values ([memoization](https://en.wikipedia.org/wiki/Memoization))
- Caching data read from disk

This work was heaps of fun. It felt like I was playing a video game. Profile, change, profile, change, always trying to get a new high score. Initially there were lots of easy, huge wins, but it became harder to push the needle over time.

After several months the code was ~100x faster, running a model in 10s or less, meaning we could run 1000 iterations in a few hours, rather than over a day. This had a big impact on our ability to run calibrations for weekly reports, but the effects of this speedup were felt more broadly. To borrow a phrase: "more is different". Our tests ran faster. CI was more snappy and people were happier to run the tests locally, since they would take 10 seconds rather than 2 minutes to complete. Dev work was faster since you could tweak some code, run it, and view the outputs in seconds. In general, these performance improvements opened up other opportunities for working better that weren't obvious from the outset.

There were some performance regressions over time as the code evolved. To try and fight these slowdowns I added automatic [benchmarking](https://github.com/benchmark-action/github-action-benchmark) to our continuous integration pipeline.

## Task automation

Once our calibration process could run in hours instead of days we started to notice new bottlenecks in our workflow. Notably, running a calibration involved a lot of manual steps which were not documented, meaning that only one person knew how to do it.

Interacting with the university's [Slurm](https://slurm.schedmd.com/documentation.html) cluster was also a pain. The compute was free but we were at the mercy of the scheduler, which decided when our code would actually run, and the APIs for running and monitoring jobs were arcane and clunky.

Calibrations didn't always run well so this cycle could repeat several times before we got an acceptable result that we would want to use.

Finally, there wasn't a systematic method for recording input and output data for a given model run. It would be hard to reproduce a given model run 6 months later.

The process worked something like this when I started:

![old workflow]({attach}/img/devops-academia/old-workflow.png)

It was possible to automate most of these steps. After a lot of thrashing around on my part, we ended up with a workflow that looks like this.

![new workflow]({attach}/img/devops-academia/new-workflow.png)

In brief:

- A disease modeller would update the code and push it to GitHub
- Then they could load up a webpage and trigger a job by filling out a form
- The calibration and any other post processing would run "in the cloud"
- The final results would be available on a website
- The data vis guy could pull down the results and push them to PowerBI

There were many benefits to this new workflow. There were no more manual tasks. The process could be run by anyone on the team. We could easily run multiple calibrations in parallel (and often did). We also created standard diagnostic plots that would be automatically generated for each calibration run (similar to [Weights and Biases](https://wandb.ai/site) for machine learning). For example, these plots show how the model parameters change over the course of a MCMC calibration run.

![parameter traces]({attach}/img/devops-academia/param-traces.png)

I won't go into too much detail on the exact implementation of this cloud pipeline. Not my cleanest work, but it did work. It was a collection of Python scripts that hacked together several tools:

- [Buildkite](https://buildkite.com/home) for task automation (it's really great)
- AWS EC2 for compute
- AWS S3 for storing data
- [boto3](https://github.com/boto/boto3) for managing transient servers
- [NextJS](https://nextjs.org/) for building the static results website

If I could build it again I'd consider using something like [Azure ML pipelines](https://docs.microsoft.com/en-us/azure/machine-learning/concept-ml-pipelines). See below for an outline of the cloud architecture if you're curious.

![new workflow, detailed]({attach}/img/devops-academia/new-workflow-detailed.png)

## Visualization tools

Our models had a lot of stuff that needed to be visualised: inputs, outputs, and calibration targets. Our prior approach was to run a Python script which used [matplotlib](https://matplotlib.org/) to dump all the required plots to into a folder. So the development loop to visualise something was:

- Edit the model code, run the model
- Run a Python script on the model outputs
- Open up a folder and look at the plots inside

It's not terrible but there's some friction and toil in there.

[Jupyter notebooks](https://jupyter.org) were a contender in this space, but I chose to use [Streamlit](https://streamlit.io/), because many of our plots were routine and standardised. With Streamlit, you can use Python to build web dashboards that generate plots based on a user's input. This was useful for disease modellers to quickly check a bunch of different diagnostic plots when working on the model on their laptop. Given it's all Python (no JavaScript), my colleagues were able to independently add their own plots. This tool went from interesting idea to a key fixture of our workflow over a few months.

![streamlit dashboard]({attach}/img/devops-academia/streamlit.png)

A key feature of Streamlit is "hot reloading", which is where the code that generates the dashboard automatically re-runs when you change it. This means you can adjust a plot by editing the Python code, hit "save" and the changes will appear in your web browser. This quick feedback loop sped up plotting tasks considerably.

**Aside:** This isn't super relevant but while we're here I just want to show off this visualisation I made of an agent based model simulating the spread of a disease through a bunch of households.

![agent based model]({attach}/img/devops-academia/abm.gif)

## Data management

We had quite a variety of data flying around. Demographic inputs like population size, model parameters, calibration targets and the model outputs.

We had a lot of model input parameters stored as YAML files and it was hard to keep them all consistent. We had like, a hundred YAML files when I left.
To catch errors early I used [Cerberus](https://docs.python-cerberus.org/en/stable/) and later [Pydantic](https://pydantic-docs.helpmanual.io/) to validate parameters as they were loaded from disk.
I wrote smoke tests, which were run in CI, to check that none of these files were invalid. I wrote more about this approach [here](https://mattsegal.dev/cerberus-config-validation.html), although now I prefer Pydantic to Cerberus becuase it's a little less verbose.

We had a lot of 3rd party inputs for our modelling such as [Google mobility data](https://www.google.com/covid19/mobility/), [UN World Population](https://population.un.org/wpp/) info, [social mixing matrices](https://github.com/kieshaprem/synthetic-contact-matrices). Initially this data was kept in source control as a random scattering of undocumented .csv and .xls file. Pre-processing was done manually using some Python scripts. I pushed to get all of the source data properly documented and consolidated into a single folder and tried to encourage a standard framework for pre-processing all of our inputs with a single script. As our input data grew to 100s of megabytes I moved these CSV files to GitHub's [Git LFS](https://git-lfs.github.com/), since our repo was getting quite hefty and slow to download (>400MB).

In the end hand-rolled a lot of functionality that I probably shouldn't have. If you want to organise and standardise all your input data, I recommend checking out [Data Version Control](https://dvc.org/).

Finally I used AWS S3 to store all of the outputs, intermediate values, log files and plots produced by cloud jobs. Each job was stored using a key that included the model name, region name, timestamp and git commit. This was very helpful for debugging and convenient for everybody on the team to access via our results website. The main downside was that I had to occasionally manually prune ~100GB of results from S3 to keep our cloud bills low.

## Wrapping Up

Overall I look back on this job fondly. You might have noticed that I've written thousands of words about it. There were some downsides specific to the academic environment. There was an emphasis on producing novel results, especially in the context of COVID in 2020, and as a consequence there were a lot of "one off" tasks and analyses. The codebase was constantly evolving and it felt like I was always trying to catch-up. It was cool working on things that I'd never done before where I didn't know what the solution was. I drew a lot of inspiration from machine learning and data science.

Thanks for reading. If this sounds cool and you think you might like working as a software developer in academia, then go pester some academics.
