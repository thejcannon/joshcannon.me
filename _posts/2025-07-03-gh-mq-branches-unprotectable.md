---
title: GitHub doesn't let you secure Merge Queue branches
subtitle: (Add it to the pile, I suppose)
---

# TL;DR

- GitHub's merge queue uses branches of the form (`gh-readonly-queue/<branch>/pr-<num>-<parent-sha>`)
- GitHub does not prevent users with write access from making branches with this pattern
- It is impossible to configure GitHub to restrict or prevent users from making these branches

# Merge Queues

GitHub has a [merge queue offering](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)
(I won't go into detail about the "what" or "why", we'll save that for another day).
It works like this, for each PR in the queue it makes an "entry". An entry is basically the code of the target branch
(almost always the default branch) along with the N PRs enqueued, stacked one on top of the other.
Each entry, then is represented by a commit (automatically created by the surreptitious GitHub Merge Queue App.

In order to ensure this system is compatible with 3rd party CI providers, GitHub creates (and destroys) branches
that point to the commits for each entry (they take the form `github-readonly-queue/<target branch name>/pr-<num>-<parent-sha>`).
Presumably you then configure your CI provider to build when these branches are pushed to.

## Security Bug

GitHub doesn't restrict users with write access from making branches of this pattern.

### Pull Request CI hole

That means if you have the code in your CI/testing infrastructure specific to merge queues
(usually this takes the shape of, say, bypassing some PR checks, or assuming the code has already been reviewed),
a clever coder can:

1. Make a commit, push a branch, and a PR
2. CI (presumably) fails
3. Push a branch whose name looks like a Merge Queue branch, pointing to the commit
4. CI (presumably) succeeds (on the same commit!)
5. Enqueue PR

(This relies on the fact that in GitHub-land a "passing" commit status is associated with the _commit_,
and not on anything related to any refs pointing to the commit, or PRs open where the commit is the `HEAD`)

## Environments hole

You may declare an [Environment](https://joshcannon.me/2025/06/29/github-environments-for-security.html)
with a branch config like `gh-readonly-queue/<branch>/*` thinking
"this code was good enough to enqueue, which without a merge queue represents merging into the default branch -
that means its as trustable as the default branch".

You wouldn't know it, but you'd be wrong (like wearing two different shades of dark navy).
And, worse, (much like finding out you're wearing two different shades of dark navy) you'd be _insecure_.

## OK, if GitHub won't lock them, I will!...

...try and fail to lock them because GitHub makes this impossible.

### Attempt 1: Disallow Creation via Branch Ruleset

This seems like a no-brainer.
Use a [ruleset](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) to restrict the creation/modification/deletion of branches matching `gh-readonly-queue/main/**/*`.

<img width="834" alt="Screenshot 2025-07-02 at 8 24 42 PM" src="https://github.com/user-attachments/assets/e157ba62-4182-4756-9804-bad96fb300ea" />

...I suppose that is to be expected.

### Attempt 1.5: Includelist the GitHub Merge Queue App as a bypasser

Rulesets have a nice UI box that you can:

> Exempt roles, teams, and apps from this ruleset by adding them to the bypass list.

That just means we need to select the GitHub Merge Queue App! Which is easier said than done,
since the app does not appear in the dropdown.

### Attempt 1.75: again but using JSON

Luckily the UI isn't all there is. Rulesets can be exported and imported as JSON.
The relevant section in the JSON looks something like:

```json
{
  "bypass_actors": [
    {
      "actor_id": <number>,
      "actor_type": "Integration",
      "bypass_mode": "always"
    }
}
```

so presumably, if we could figure out what the magic number is for the GitHub Merge Queue App, we could
create a ruleset via import of a well-crafted JSON and our precious branches would be protected.

After cross-checking with existing app bypasses and settings,
it's clear that the number is the GitHub App's "App ID". 

The GitHub Merge Queue App itself isn't well-documented. Webhook payloads show the following `sender` in events related to
the merge queue branches:

```json
{
  "sender": {
    "login": "github-merge-queue[bot]",
    "id": 118344674,
    "node_id": "BOT_kgDOBw3L4g",
    "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
    "url": "https://api.github.com/users/github-merge-queue%5Bbot%5D",
    "html_url": "https://github.com/apps/github-merge-queue",
    ...
  }
}
```

Of course, the login tells us the app slug, so we can also poke at the REST API:

```
% gh api /apps/github-merge-queue
{
  "message": "Not Found",
  "documentation_url": "https://docs.github.com/rest/apps/apps#get-an-app",
  "status": "404"
}
```

(for comparsion `gh api /apps/github-actions` does return a result,
and again cross-checking an existing app shows that the App ID is also the payload's `.id`)

Unfortunately, the sender `id` and `node_id` are for the "Bot" user associated with the app,
and [GitHub's GraphQL API](https://docs.github.com/en/graphql/reference/objects#bot) bears no fruit
as doesn't the [REST API for Apps](https://docs.github.com/en/rest/apps/apps?apiVersion=2022-11-28).

So, short of guessing the app slug, we're out of luck.

(and besides, even if we did guess the app ID, there's a chance GitHub rejects the ruleset JSON.
Like it does if you try to put the GitHub Actions App ID)

<img width="557" alt="Screenshot 2025-07-02 at 9 25 42 PM" src="https://github.com/user-attachments/assets/1dc4f8e8-0936-4aee-b5db-846cf97a6db0" />

Better luck next time!
