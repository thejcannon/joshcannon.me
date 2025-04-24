---
title: "Remote Single-file Python scripts with uv"
excerpt: "How supercharge your script running with uv tricks"
---

Let's make a checklist:

- `uv` installing/managing Python for you
- `uv` supporting remote files (e.g. `https://`)
  - `uv` also supporting reading `~/.netrc`
- `uv` supporting [PEP 723: Inline Script Metadata](https://peps.python.org/pep-0723/)

I think we're set!

# Purpose

Python scripts are useful for great fun and profit, but they can be a bit of a hassle to develop/publish/run.

It turns out, combining a bunch of the features already baked into `uv`, we can pretty easily make
remote single-file scripts that are a single command to run!

# Plan

## 1. `uv` installs/runs `python` for you

(From [the docs](https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies))

> `uv run` will search for and use the required Python version. The Python version will download if it is not installed

That means you don't need to worry about installing (the right version of) Python!

## 2. `uv` supports remote files

(From [the docs](https://docs.astral.sh/uv/reference/cli/#uv-run))

> When used with [...] an HTTP(S) URL, the file will be treated as a script and run with a Python interpreter, [...]. For URLs, the script is temporarily downloaded before execution.

That means you can just `uv run https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}` and it will work!

NOTE: `uv` caches based on the URL, so if you want "evergreen" URLs (e.g. `refs/heads/main`) you'll need to use `--refresh` to force a re-download.

### Supporting "private" repos too!

`uv run` _also_ supports reading `~/.netrc`, meaning [you can do the same thing for private repos too](https://joshcannon.me/2025/04/23/private-raw-github-url.html)!

## 3. `uv` supports inline script metadata

(From [the docs](https://docs.astral.sh/uv/reference/cli/#uv-run))

> If the script contains inline dependency metadata, it will be installed into an isolated, ephemeral environment.

(This is referencing [PEP 723](https://peps.python.org/pep-0723/)) "inline script metadata", which allows you to specify metdata like dependencies and python version in the file itself.

# Putting it all together

In this repo, is `scripts/claudesay.py`, therefore you should be able to run it like:

```bash
uv run -q --refresh https://raw.githubusercontent.com/thejcannon/joshcannon.me/refs/heads/main/scripts/claudesay.py 'Certainly!'
```

And it just works!

# Conclusion

This is a super easy/simple way to share scripts with others (or with yourself, no judgement),
including scripts in private repos (like in an enterprise/work environment), without having to configure
the right version of Python or the right dependencies to use.

## Disclaimer

Of course, please include the normal caveats about trusting remote code.
