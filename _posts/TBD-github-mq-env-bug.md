---
title: GitHub doesn't let you secure Merge Queue branches
subtitle: (Add it to the pile of minor GitHub Security holes I suppose)
---

# TL;DR

- GitHub's merge queue uses branches of the form (`gh-readonly-queue/<branch>/pr-<num>-<parent-sha>`)
- GitHub does not prevent users with write access from making branches with this pattern
- It is impossible to configure GitHub to restrict or prevent users from making these branches

# Merge Queues

GitHub has a [merge queue offering](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)
(I won't go into detail about the "what" or "why", we'll save that for another day).
It works like this, for each PR in the queue it makes an "entry". An entry is basically the code of the target branch
(almost always the defualt branch) along with the N PRs enqueued, stacked one on top of the other.
Each entry, then, is represented by a commit (automatically created by the surreptitious GitHub Merge Queue App.

In order to ensure this system is compatible with 3rd party CI providers, GitHub creates branches (and destroys)
that point to the commits for each entry (they take the form `github-readonly-queue/<target branch name>/pr-<num>-<parent-sha>`).
Presumably you then configure your CI provider to build when these branches are pushed to.

## The Security Bug 1

GitHub doesn't restrict users with write access from makes branches of this pattern.

### Pull Request CI hole

That means if you have code in your CI/testing infrastructure specific to merge queues
(usually this takes the shape of, say, bypassing some PR checks, or assuming the code has already been reviewed),
a clever coder can:

- Make a commit, push a branch, and a PR
- CI (presumably) fails
- Push a branch whose name looks like a Merge Queue branch, pointing to the commit
- CI (presumably) succeeds (on the same commit!)
- Enqueue PR

(This relies on the fact that in GitHub-land a "passing" commit status is associated with the _commit_,
and not on anything related to any refs pointing to the commit, or PRs open where the commit is the `HEAD`)

### Environments hole

You may declare an Environment with a branch config like `gh-readonly-queue/<branch>/*` thinking
"this code was good enough to enqueue, which without a merge queue represents merging into the defualt branch -
that means its as trustable as the default branch".

You wouldn't know it, but you'd be wrong (like wearing two different shades of dark navy).
And, worse, (much like finding out you're wearing two different shades of dark navy_ you'd be insecure.

## If GitHub won't lock them, I will!...

...try and fail to lock them because GitHub makes this impossible.

