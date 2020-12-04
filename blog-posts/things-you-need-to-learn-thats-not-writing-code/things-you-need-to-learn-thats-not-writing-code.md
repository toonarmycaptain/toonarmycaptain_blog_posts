---
published: true
title: "What you need to learn that's not writing code."
cover_image: ""
description: "Things you should master when learning to code, besides a primary language and how to code in it."
tags: [learning, git, testing, documentation]
series: ""
canonical_url: ""
---


A mate told me they're trying to pick up coding. While I'm not yet employed with my skills, I thought I'd write down my thoughts about what they need to learn. 

[They're planning on learning HTML/CSS/JS and Python for front end development, and have started with Python.]

What do they need to learn?

- ###Version control - Git/GitHub
Use version control, preferably externally hosted. [Git](https://git-scm.com/) hosted on [Github](https://github.com/) is the ubiquitous place to start.  
It can be a bit of a head trip when you first try it, but at least get the basics of making a repo, cloning it to your machine, .gitignore, adding/tracking files, committing changes in sensible portions regularly, pushing, and the rest will come.  
The rest being branching, making/merging PRs (Pull Requests), `reset`, and the-rest-you-will-likely-google-when-you-need-them-the-first-few-times-and-even-then-still-google-to-be-sure.  
Seeing what files are tracked/ignored and what changes are committed is much easier when starting out with some sort of GUI, like an...

- ###IDE - Pycharm
Become proficient in at least one full-featured IDE, and it's features.  
[PyCharm](https://www.jetbrains.com/pycharm/) is a good one for python, and integrates with the rest of these well, and has useful features for HTML/CSS/JS.  
Some call this cheating, but I believe learning how to use an IDE well is worthwhile both for productivity and understanding what is going on in the code you're writing. 
The debugger in whatever language you're using is also a great skill, but when you're beginning, the GUI debugger in most IDEs is a good place to start. 

- ###Some testing skills  - pytest
Whether or not you decide to go hard into TDD (Test Driven Development), as long as you write tests around the time you write the code, or figure out what you need the code to be doing/not doing, you'll be doing yourself a favour.  
In tandem with git and automated testing, this will save you from your own assumptions, and force you to learn the basics of extremely useful tools (eg [TravisCI](https://travis-ci.com/), [Appveyor](https://ci.appveyor.com/)).    
[Pytest](https://docs.pytest.org/), compatible with python's builtin `unittest`, and has lots of plugins for testing most things you'd care to test. 
*While technically writing code, the concepts, practise, skill set of writing tests are separate from writing production code. 

- ###Documenting your code
When you go back in a few months and wonder what you were thinking...this is your chance to help yourself fix the mess you created when you had no idea what you were doing (for me this is generally yesterday). This includes comments as well as more formal documentation (ie package/module/class/function/method docstrings, README.md).
This also includes git commit messages that make enough sense for you (and preferably others) to follow what changes are being made.  
Python has the helpful [PEP 8](https://www.python.org/dev/peps/pep-0008/) and [PEP 257](https://www.python.org/dev/peps/pep-0257/) general guides. 

- ###Learning practices
Keeping a journal or record of the things you're learning, or even a blog, are great practices. Even if it's as simple as text document you can search in, recording the things you learn and figure out gives you a reference later ("how did I do that obscure weird thing that other time and why") is invaluable. This can also function as a record of what you've learned and grown, for yourself, and to potentially to draw on to give current or future employers specific evidence of growth and experience.  
Writing in public about what you're learning or doing also seems good advice; it's why I'm here; and the process of distilling knowledge for communicating or teaching others is a boon to your personal learning, if for no other reason than the gaps in your knowledge will be filled when you double-check your facts (I mean...research), or get corrected publicly. Which, if you've any humility, is more good than bad!

####Speaking of which, please let me know what I'm missing, or wrong about!


I'll note that these are habits that will grow into well-developed skills when they're practiced as part of a workflow, rather than as an afterthought.
Or at least, I hope they will...


There are a few of almost-without-saying skills that are independent of any technology, but worth mentioning:
- Problem solving, and a rough personal methodology, both when debugging code, and figuring out how you need to solve a problem (or, first, what the problem is). 
- ...and the tool to find the details: Google and/or [StackOverflow](https://stackoverflow.com/). 
- Learn to find, and how to navigate, the documentation for the technologies you're using. 
