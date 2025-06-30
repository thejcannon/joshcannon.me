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

## The Security Bug

GitHub doesn't restrict users with write access from makes branches of this pattern.

That means if you have code in your CI/testing infrastructure specific to merge queues
(usually this takes the shape of, say, bypassing some PR checks, or assuming the code has already been reviewed),
a clever coder can:

- Make a commit, push a branch, and a PR
- CI (presumably) fails
- Push a branch that looks like a Merge Queue branch, pointing to the commit
- CI (presumably) succeeds 

Ruh Roh Raggie





# Bonus: Environments

GitHub's Environments are closely tied to "Deployments". So much so I thought "huh this seems useless (for me)" and moved on.
Perhaps I held this belief after seeing the 58 instances of "deployement" on the page describing Environments (which has 118 hits).

But, as I learned later Environments are actually quite useful outside of the world of Deployments, and inside the world of Security. That's because:

> You can configure environments with protection rules and secrets. When a workflow job references an environment, the job won't start until all of the environment's protection rules pass. A job also cannot access secrets that are defined in an environment until all the deployment protection rules pass.

It is hopefully well-known that GitHub Secrets are _barely_ secure. Of course the pages on ["About Secrets"](https://docs.github.com/en/actions/concepts/security/about-secrets) and ["Using Secrets in GitHub Actions"](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/using-secrets-in-github-actions) don't mention it, but ["Security hardening for GitHub Actions"](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/security-hardening-for-github-actions#using-secrets) (what, you don't cross-search all your favorite technologies with "-hardening") does:

> Any user with write access to your repository has read access to all secrets configured in your repository. Therefore, you should ensure that the credentials being used within workflows have the least privileges required.

(way to bury the lede there!)

### for Security

Environments CAN be used to _securely_ store secrets knowing that even users with write access can't (easily - depending on the overall security of your repo) access them. For security-purposes, they work like this:

- You make a GitHub Environment, let's call it `main`
- You configure the "deployment" protection rules to restrict the "deployment" to just the `main` branch
  - "deployment" is a (repeated) red herring 
- You store your precious secrets as Environment Secrets

Then, in your workflow you just need to use `environment: main`. If the ref that the workflow is triggered from is `main` the workflow proceeds and can access the secrets. Otherwise, it gets rejected with a _mostly_ helpful message.

(Pssst. This means you can't use certain workflow triggers whose ref isn't the default branch, like `pull_request`)

(Pssssssssssst you also can't use `pull_request_target` because although it runs using a `github.ref` of the default branch, the triggering ref is the PR head branch. I have an open ticket but I wouldn't hold my breath)

When configured this way, along with common branch rulesets like requiring a PR and requiring code review, we know:

- The workflow definition came from the default branch, which should be trustable
- The workflow run is running against the default branch, which should be trustable

Trust is Security's best frienemy.
