---
title: "Diff diffs (a.k.a. 4-way diffing)"
excerpt: "What changes have changed?"
---

GitHub provides in its web UI a view that shows "whats changed since you last reviewed". In some sense, this is a _diff_ of _diffs_. But how is it produced?

# The Background

GitHub provides a way for you to see the changes in a pull request branch, relative to some earlier change in the branch (i.e. "what's changed in this PR since...").

You end up with a URL like:

```
https://github.com/{owner}/{repo}/pull/{num}/files/{old-sha}..{new-sha}
```

This kind of "diff of diffs" is useful for several purposes:

- For humans to review only the changes since they last reviewed
- Automation based on "whats changed since it last ran"

An easy example is trying to re-implement `CODEOWNERS` logic. Knowing "what's changed since the last time we ran" tells you what paths to match in the `CODEOWNERS` file.

But how can we get this?

# The Struggle

It isn't easy. You'll learn quickly GitHub does not offer this in their REST API or their GraphQL API. The closest thing is the [compare two commits API](https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28#compare-two-commits), but that's not what we want.

Scouring the web will leave you thirsting for knowledge. As will sniffing the network while poking around GitHub's Web UI. Even asking Claude wasn't giving me the solution I wanted.

For a while I thought the path forward was to use `interdiff` from [`patchutils`](https://github.com/twaugh/patchutils). It does what it says on the tin: diff two diffs. Yet, the lack of support for things like renames left me unsatisfied.

I was convinced that diffs and snapshots were like points and vectors in linear space, and that there must be some way to easily "sum" all the little diffs together to produce the point(s) whose vector was itself the difference between the old tip and the new tip (after all GitHub is able to show me a single diff).

# The solution

The solution took an embarassing amount of time for me to
unravel, but once you understand it, it's exactly the `git`-fu equivalent to the "find the (linear space) point to use as our 'before'".

The "point" we want is "let's re-imagine the old tip as if it had our new tip's merge base". From there we just need to compare that to our new tip.

And how do we make that "new" old tip?

# Putting it together

You need a `git` repo, and all 3 points of reference from the PR interdiff perspective:

- The old SHA
- The new SHA
- The base branch

Then, you need some merge bases (specifically both SHA's merge base with respect to the base branch). You can use:

- [GitHub's API](https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28#compare-two-commits)
  - NOTE: Ask for `page=2` since you don't need the `files[]` object
- `git merge-base`

If you don't already have all 4 commits, you'll need to fetch them (but luckily you can do shallow fetches (e.g. `--depth 1`)).

Then, all you need to do is make a merge!

```bash
git merge-tree -X theirs --allow-unrelated-histories --merge-base <old-merge-base> <new-merge-base> <old-sha>
```

The result will be a Tree SHA which represents "the old tip as if it had our new tip's merge base". With that, we can finally

```bash
git diff <tree-sha> <new-sha>
```

And there you have it: a diff of diffs.

# Bonus: Crankin' it to 11

If your git server supports it (like GitHub does), fetch the SHAs using `git fetch --filter=blob:none <remote> <...>`.
This will fetch just the tree information, and not the binary contents of the files. Then when you do `git merge-tree` and
`git diff`, `git` will smartly choose whether (and which) blobs to fetch (if any).

This can mean the difference between minutes and sub-seconds for large enough repositories.
(On my M1 Macbook, performing this operation on [this merge conflict resolution in the `cpython` repo](https://github.com/python/cpython/pull/136307/commits/c5a1146887bc182a46d56bb08c6f6cc67507ef32),
took 2 minutes and downloaded 500MB without `--filter=blob:none` and 15s and 131MB with.
