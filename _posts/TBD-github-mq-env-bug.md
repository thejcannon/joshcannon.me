---
title: GitHub doesn't let you secure Merge Queue Environments
subtitle: (Add it to the pile of minor GitHub Security holes I suppose)
---

I think this is a pretty niche bug (although it can probably be searched for),
however I found it at `$dayjob` while trying to use `environments` as a way
to secure GitHub Actions workflows. After reporting it to GitHub my ticket was
archived as an "internal issue" with no promises of resolution.

# Background

Let's (briefly) go over the two features at play here,
[Environments](https://docs.github.com/en/actions/how-tos/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment) 
and [GitHub's Merge Queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue).

## Environments

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

## Merge Queue


