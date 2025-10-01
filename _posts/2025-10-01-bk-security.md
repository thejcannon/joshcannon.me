---
title: Overwriting GitHub Required Checks with Buildkite
subtitle: Green CI is easier than ever
---
 
 (for some pre-reading you may want to read [my brief post](https://joshcannon.me/2025/08/24/github-commit-status.html)
 on how GitHub commit statuses and PR required checks work)

## Buildkite step-level `notify`

Buildkite pipelines offer a [nice feature](https://buildkite.com/docs/pipelines/configure/notifications)
where the pipeline YAML can have a `notify` key which can be configured
to list different services to receive "notifications" about the pipeline's status
(e.g. "in progress" or "failed" or "succeeded").

These services include Slack (to send messages/updates) and PagerDuty (presumably to alert on failure) and also GitHub,
although not documented on the linked page - for that you'd need to go [here](https://buildkite.com/docs/pipelines/source-control/github#customizing-commit-statuses-build-level).

This feature is also extended to individual pipeline steps, as well as group steps, with a subset of the configurable services.

As an example:

```yaml
steps:
  - label: "Example Script"
    command: "script.sh"
    notify:
      - ...
 ```

### `github_commit_status`

One of the configurable services services is `github_commit_status`,
which takes an arbitrary string _context_, and tells Buildkite to send commit statuses
(e.g. "pending", "failure") representing the pipeline step status ("running", "failed") using the provided context.

It hopefully isn't hard to imagine how this can be a useful feature!
Unfortunately it also isn't hard to imagine how this can be abused.

## Setting up the board

1. Configure your repository to require Pull Requests, and require that PRs MUST pass a required status check
   (which for this purpose, let's assume does some security checks) which MUST come from the Buildkite GitHub App
   using the context `buildkite/security-pipeline` (the one sent by the "Security Pipeline" pipeline).
2. In the same repository, have a pipeline (could be any) which allows developers to change/upload pipeline steps
   (e.g. edit the steps or run `buildkite-agent pipeline upload`).
   (Due to the nature of Buildkite and their "dynamic pipelines" feature, this is usually a possibility).

## The "Play"

1. Make a malicious commit which would fail the security check
2. Wait for the security pipeline to fail
3. Upload some pipeline YAML containing
```yaml
steps:
  - command: echo "gotcha"
    notify:
      - github_commit_status:
          context: "buildkite/security-pipeline"
```
4. Trigger that pipeline on the malicious commit
5. Your PR is now mergeable

For step 3, it helps if you find a way to upload pipeline YAML outside of the code changes itself
(otherwise you'll need to get creative in crafting your malicious commit - although most folks
aren't scrutinizing Buildkite pipeline steps for security flaws).

## BONUS: Every security bug is a security feature

Once I discovered this bug, I immediately reported it to Buildkite.

Then, of course, I set out to use this to my advantage.

At the time, I was helping support our usage of GitHub's Merge Queue.
One displeasure was when parts of CI (say a set of tests) were still running for a particular entry,
where they'd passed on a "downstream" entry. In this scenario we knew it was 99% safe to merge, but
had no way of kicking Buildkite/GitHub into action.

So, easiest way to move forward is... make a pipeline which does the above!
Trigger the pipeline on the SHA of the merge queue entry and ✨ merged ✨
