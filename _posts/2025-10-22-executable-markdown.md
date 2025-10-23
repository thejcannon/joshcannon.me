[ \]; exec /usr/bin/env open 'https://www.youtube.com/watch?v=RfiQYRn7fBg'; ]:#
---
title: Making executable markdown files
subtitle: This blog post is executable
---

In the pursuit of something itself worthy of a (future0 blog post,
I foud myself wanting to have "exeuctable" markdown files.

TL;DR `[ \]; exec <COMMAND> $0 "$@"; ]:#`

Try it! `curl https://raw.githubusercontent.com/thejcannon/joshcannon.me/refs/heads/main/_posts/2025-10-22-executable-markdown.md.md | sh`

(or save it to a file, `chmod +x` it, then run it)

# What the hell?

Figuring out the puzzle is left as an exercise for the reader, but I'll present two key pieces of information:

1. `[ <anything> ]:#` is a valid Markdown comment
  - You cannot put a space between the `]` and the `:`
2. `[` is not Bash syntax, it is a program. (`man [` if you don't believe me)

Enjoy!
