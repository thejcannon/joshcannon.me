---
title: GitHub Environments are a (sometimes) useful security feature
excerpt: "(much like GitHub Secrets)"
---

# Environments

GitHub's Environments are closely tied to "Deployments". So much so I thought "huh this seems useless (for me)" and moved on.
Perhaps I held this belief after seeing the 58 instances of "deployment" on the page describing Environments (which has 118 hits).

But, as I learned later Environments are actually quite useful outside of the world of Deployments, and inside the world of Security. That's because:

> You can configure environments with protection rules and secrets. When a workflow job references an environment, the job won't start until all of the environment's protection rules pass. A job also cannot access secrets that are defined in an environment until all the deployment protection rules pass.

It may not be well-known that GitHub Secrets are _barely_ secure. Of course the pages on ["About Secrets"](https://docs.github.com/en/actions/concepts/security/about-secrets) and ["Using Secrets in GitHub Actions"](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/using-secrets-in-github-actions) don't mention it, but ["Security hardening for GitHub Actions"](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/security-hardening-for-github-actions#using-secrets) (what, you don't cross-search all your favorite technologies with "-hardening") does:

> Any user with write access to your repository has read access to all secrets configured in your repository. Therefore, you should ensure that the credentials being used within workflows have the least privileges required.

**... has read access to all secrets**?! (way to bury the lede there!)

## For Security

Environments can be used to _securely_ store secrets knowing that even users with write access can't
(easily - depending on the overall security enforced by the repo's branch/tag protections) access them. For security-purposes, they work like this:

- You make a GitHub Environment, let's call it `main`
- You configure the "deployment" protection rules to restrict the "deployment" to just the `main` branch
  - "deployment" is a (repeated) red herring 
- You store your precious secrets as Environment Secrets

Then, in your workflow you just need to use `environment: main`.
If the ref that the workflow is triggered from is `main` the workflow proceeds and can access the secrets.
Otherwise, it gets rejected with a _mostly_ helpful message.

When configured this way, along with common branch rulesets like requiring a PR and requiring code review, we know:

- The workflow definition came from the default branch, which should be trustable
- The workflow run is running against the default branch, which should be trustable

Trust is Security's best frienemy.

## Why "Sometimes"?

This is useful for situations where the triggering ref is `main` - events like `status`, or `issues`, or `workflow_dispatch` (when the `ref` is `main`)
(See `GITHUB_REF` in the [docs](https://docs.github.com/en/actions/reference/events-that-trigger-workflows))

However that means that triggers like `pull_request` will almost never match (unless you're opening PRs where `main` is the head branch - dude WTF?).

However however a clever GitHub aficionado would point out the existence of [`pull_request_target`](https://docs.github.com/en/actions/reference/events-that-trigger-workflows#pull_request_target).
An event whose sole purpose is to _trigger_ on Pull Request events, but with the `github.ref` of the base branch!
So using `pull_request_target` means we CAN combine Environments with Pull Request events!

However however however the _triggering_ branch is still the pull request base, so the environment is rejected.
([You get NOTHING! You LOSE! GOOD DAY SIR!](https://youtu.be/M5QGkOGZubQ?si=CyZk7xO5X1X3JALJ))

(I have an open ticket about this but I wouldn't hold my breath)

While I'm piling on GitHub, even if this "bug" was fixed, the lack of event symmetry means that
`pull_request_review` and `pull_request_review_comment` events would still be left out by the roadside,
(forever) [waiting](https://github.com/orgs/community/discussions/155603) for a `_target` equivalent.

### Workaround(s)

If your workflow is inherently safe for anyone to be able to trigger arbitrarily, one workaround is to use `workflow_dispatch`.

you can combine `pull_request` and `workflow_dispatch` triggers, like so:

{% raw %}
```yaml
on:
  pull_request: ...
  workflow_dispatch:
    inputs:
      pull-number:
        type: number
        required: true

jobs:
  trigger-job:
    if: github.event_name == 'pull_request'
    name: Trigger the workflow
    runs-on: ubuntu-latest
    permissions:
      actions: write
    steps:
      - run: gh workflow run <filename> --ref main -F pull-number=${{ github.event.pull_request.number }}
        env:
          GH_TOKEN: ${{ github.token }}
          GH_REPO: ${{ github.repository }}

  the-job:
    if: github.event_name == 'workflow_dispatch'
    name: Name
    runs-on: ubuntu-latest
    environment: main
    steps: ...

```
{% endraw %}

It's a hack, and not a very pretty or nice one. But it works in a pinch

There are undoubtedly other workarounds, but that's all the simple ones I'm aware of.
