# Lab 2: Git Practice

In this lab, you'll practice using git and GitHub.  Git is a
collaborative tool, so make sure you form a group of 2-3 people to do
this lab together.

You can do this lab on your virtual machine, which should already have
git installed (and even not, installing git on Ubuntu can be done with
a simple `apt` command, like this: `sudo apt install git`).

It's probably a good idea to install git on your own laptop at some
point.  Windows directions: https://git-scm.com/download/win.  Mac
directions:
https://www.ics.uci.edu/~pattis/common/handouts/macmingweclipse/allexperimental/macxcodecommandlinetools.html.
You're welcome to do this lab directly on your laptop (not through the
virtual machine), though if you run into any tricky issues installing
or using git directly on your laptop, we might ask you to switch to
using your virtual machine.

## Step 1: Practice Git Branching

Let's start by practicing in the Git simulator <a
href="https://tyler.caraza-harter.com/cs320/s20/learnGitBranching/index.html"
target="_blank">here</a>.  Try to run commands to get to the following state (if you get stuck, check the [solution here](solution.md)):

<img src="step1/1.png" width=500>

Useful commands for the above problem:
* `git commit`: make a new commit
* `git branch bname`: create a branch named `bname`
* `git checkout bname`: move `HEAD` to the commit referenced by the `bname`
* `git checkout c1`: move `HEAD` to the `c1` commit
* `git merge bname`: merge changes on the `bname` branch into the current branch
* `git branch -D bname`: delete the branch named `bname`

Ready for a real challenge?  Try to get to this state (no answer to
check for this one, so you'll need to work for it!):

<img src="step1/2.png" width=500>

**Hint:** start by creating commits on four branches, b1, b2, b3, and b4.
Merge b2 into b1 and b4 into b3.  Then merge the two merge commits
with a third merge commit.

## Step 2: Create GitHub Account



## Step 3: Create and Clone a Repo



## Step 4: Launching your Virtual Machine



