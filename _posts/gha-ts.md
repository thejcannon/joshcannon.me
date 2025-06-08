---
title: Conjuring Powerful GitHub Actions
subtitle: Wield the power of Typescript, `bun`, and GitHub's toolkit(s)
---

I love automation. The good kind of automation. The kind that takes [a release process with a mind-numbing amount of manual work](https://www.pantsbuild.org/2.15/docs/contributions/releases/release-process)
and turns it into [a few simple blissful button-clicks](https://www.pantsbuild.org/2.20/docs/contributions/releases/release-process).

Ahhhhhhh

...anyways, that's why I'm a GitHub-Actions stan (despite how often and how hard GitHub tries at making me dislike it).

Let's take a look at how to conjure up powerful GitHub Actions.

# Anatomy of an action

- `action.yml`
- the "three types" of actions
- Why they are so damn hard to test

# Javascript Actions

- what they are
- why they exist
- why they are superior
  - `INPUTS_`
  - Actions Toolkit
  - `pre`/`post` hooks
  - `github/local-action`
  - No deps setup needed

# My current setup

- `bun`
 - Plus plugin (TBD)
- `ci` / `cd`
- Testing
