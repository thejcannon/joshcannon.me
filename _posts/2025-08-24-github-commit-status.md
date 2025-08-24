---
title: "The Problem with GitHub Commit Statuses"
excerpt: "(Just one?)"
---

GitHub has a feature where you can gate merging Pull Requests behind passing commit statuses.

This is largely used for checks such as "has CI run?", but can be used for many many more things since this is automatable.

There are all kinds of GitHub Automations leveraging these. Ones for:

- Code Coverage gates
- "DO NOT MERGE" checks
- Code Review requirements (because CODEOWNERS isn't great)
- Pull Request title/description checks
- Merge Queue semantics
- ...and of course every AI code reviewer ever

# How it works

Just use the API (REST or GraphQL) to send a commit status (passing, failing, or pending) along with a "context" (e.g. a slug)
some optional description (e.g. "you didn't say the magic word") and an optional URL.
If configured, the Pull Request MUST have a passing status sent from the exact configured GitHub App 
before it is able to merge.

# The Problem(s)

## Arbitrary, arbitrary. Everything is arbitrary.

The APIs for commit statuses aren't limited to apps and contexts aren't limited and whose URLs aren't limited and which are only
limited to those with write access to the repository.

Feeling bored and want to mess with your peers? Pick a PR, grab the SHA and...

```
gh api \
  /repos/{owner}/{repo}/statuses/{SHA} \
   -f 'state=failure' \
   -f 'target_url=https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDkwajRocjlpazJ6NXIzbXRlbWg1ZThneml5NzQ4a29sajZkcmZ6MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/owRSsSHHoVYFa/giphy.gif' \
   -f 'description=YOU DIDNT SAY THE MAGIC WORD' \
   -f 'context=i-hate-this-hacker-crap'
```

From a security standpoint, required checks are configured along with the GitHub App they are expected to come from.
Meaning if you're expecting the required "passes security checks" commit status to come from the GitHub App "Scruff McGruff",
a passing status from another GitHub App, or from a user, will not be honored.

The status will of course still exist and be displayed, which is some sucky UI/UX. Speaking of...

## The UI/UX sucks

In addition to aribitrary statuses or descriptions or senders, there's also the juggling of required status checks with all
the other (not-aribitrary-but-not-required) ones. Not only can it get overwhelming, but it can get downright misleading!

GitHub's UX changes if you have failing NOT required status checks. The nice green merge button (the one that feels SO GOOD to click)
turns into a clickable-but-greytone one. I can't count the number of times I've had to help people in realizing the button is clickable,
it just isn't _green_. I'm also pretty sure as every company matures they make a set of userscripts of a Chrome Extension just for GitHub,
and _this_ is the first piece of functionality.

## Context is Key

Lastly, everything is keyed off of the (aribtrary) `context` in the payload.

A new status with the same context (but different state or description) just overwrites the previous one.

If you're adding a new required status - hope your opened (and currently mergeable) PRs have a passing 
status already.

Or if you want to rename/change the context, good luck!

## One Commit SHA: 0 to inifinite PRs

Since commit statuses are sent to commit SHAs that means the relationship between the Pull Request and the "required" statuses
is the same relationship between a branch and a commit.

In the case of Pull Requests, let's say we have a check that the PR description includes a reference to HeadOn ("Apply directly to the forehead").
And I open a PR against the default branch omitting the reference. I presumably get a failing commit status check and can't merge my PR.
Then, because our development cycle is weird I also have to open the same change against the `superbowl` feature branch, so I do, remembering
the required reference. I get a passing commit status check (apply directly to the commit SHA).

One SHA. One branch (but could be two). Two PRs. Both (now) mergeable.

(The pain of which is felt beyond just the forehead)
