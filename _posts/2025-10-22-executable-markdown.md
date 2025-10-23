---
title: Making executable markdown files
subtitle: Because its useful (kinda)
---

In the pursuit of something itself worthy of a (future) blog post,
I foud myself wanting to have "exeuctable" markdown files.

TL;DR `[ \]; exec <COMMAND> $0 "$@"; ]:#`

Try it! `curl https://raw.githubusercontent.com/thejcannon/joshcannon.me/refs/heads/main/scripts/magic-word.md | sh`

(or save it to a file, `chmod +x` it, then run it)

# What the hell?

Figuring out the puzzle is left as an exercise for the reader, but I'll present two key pieces of information:

1. `[ <anything> ]:#` is a valid Markdown comment
  - You cannot put a space between the `]` and the `:`
2. `[` is not Bash syntax, it is a program. (`man [` if you don't believe me)

Enjoy!
