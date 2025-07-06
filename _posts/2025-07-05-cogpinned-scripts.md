---
title: 'Using `cog` for pinned Single-File Python scripts'
subtitle: 'Or as I call it: cogpinning'
---

# Background

## Cog

I've been dying to have some fun with [`cog`](https://cog.readthedocs.io/en/latest/) ever since I
overheard Ned Batchelder ([`@nedbat`](https://github.com/nedbat)) talking about it with someone else.

Here's its own description:

> Cog is a content generation tool.
> It lets you use small bits of Python code in otherwise static files to generate whatever text you need.

I think the best and most fun example of how cog works is a hidden gem in the cog docs.
Cog embeds the the [CLI `--help` in the docs](https://cog.readthedocs.io/en/latest/running.html) by [using cog](https://github.com/nedbat/cog/blob/0ff1d7c1ce8331a6ebcd733523e7587df858aebd/docs/running.rst?plain=1#L6)
to run `cog -h` and dump the output (into the file).

This is poetry (no, not the Python tool). This is beautiful (not the soup).

## Single-file scripts

Also, if you haven't heard of or tried them yet, the Python packaging ecosystem has a neat way of taking
a Python script's dependency specifier and "inlining" it at the top of a file in a comment TOML ([not a TOML comment](https://toml.io/en/v1.0.0#comment)),
making a ["single-file script"](https://packaging.python.org/en/latest/specifications/inline-script-metadata/).

The result is something that can be `uv run` or `pipx run` and is spiritually a Python "single-file executable".

This is also beautiful and amazing.

# Problem

Single-file scripts lack a way to pin transitive dependencies.

While `uv` supports this with `uv lock --script`, it creates a separate lock file, defeating the whole _"single-file"_ concept.

(Really I want to fully embed the lockfile, but pinned transitive deps are "good enough" for now).

# Solution

Use `cog` to generate to pin the dependencies!

```python
# /// script
# dependencies = [
# # [[[cog
# # DEPENDENCIES = [
# #     "cyclopts",
# #     "httpx",
# # ]
# # cog.outl("\n".join(f'#   "{line}",' for line in __import__("subprocess").check_output("uv pip compile --no-annotate --no-header -", shell=True, text=True, input="\n".join(DEPENDENCIES)).splitlines()))
# # ]]]
#   "anyio==4.9.0",
#     "<the others omitted for brevity>",
# # [[[end]]]
# ]
# ///

import cyclopts
import httpx

# Script code here...
```

And now you can update (and pin) dependencies anytime with:

```bash
uvx --from cogapp cog -r <path>
```

Caveat: (when compared with a full lockfile) is the lack of hash support (if you're into supply-chain security).
However, incremental improvement is still improvement.

# Bonus: Self-relocking

This also means your single-file script (usually a CLI app) can now have a `self relock` command!

```python
# <same preamble>

import cyclopts
import rich
import subprocess

app = cyclopts.App()
self_app = cyclopts.App(name="self")
app.command(self_app)

@self_app.command()
def relock():
    subprocess.check_call(f"uvx --from cogapp cog -r {__file__}", shell=True)
    rich.print("[green]Relocked successfully[/green]")

...
```
