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

## Environment


