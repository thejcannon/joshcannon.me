---
title: The Programmer's Dilemma
subtitle: A different take on "locality"
---

Imagine for a moment you had to get a group of 100 random adult human beings
to perform a task that involves groups of them working together 
(and if you really want to succeed, groups would also need to work with other groups).

Let's assume these humans are rational (most are!), have a good memory (present company only maybe included),
and understand how other humans generally work (as most do).

Now all you can control is one thing: do you let them hunker down in separate rooms, or bring them all into one?

...this isn't about "Return to Office." It's about monorepos!

And TL;DR: The more you co-locate, the more you co-operate and co-llaborate.

---

# (aside) A Pedant's "Repo" Rant

A "repository" is defined as "a place, building, or receptacle where things are or may be stored."

As there's no comment on size or shape, this implies that my belly button is a lint repository just as much
as Earth is a humans repository.

Or, put another way, not only is the `CPython` GitHub [repo](https://github.com/python/cpython) a repository,
the [Python GitHub org](https://github.com/python) is a repository, as is GitHub (.com) itself.

This is important because when people talk about a "monorepo," sometimes we aren't all talking about the
exact same thing. Google's "monorepo" is not like Meta's is not like (org I've worked at using a GitHub git monorepo).

# What's that human doing in my machine?

I often approach solving common organizational problems in a way that is likely uncomfortable to some:
ignore the technology and focus on the humans. They are the ones writing the code, they are the ones working together,
they are the ones that define success or failure.

This is because I strongly believe that "software engineering" is not just engineering, but is also an artistic exercise
and a social experience (I also believe that driving is a form of dancing, just to go ahead and put that out there).
Perhaps put another way, it's a [game](https://en.wikipedia.org/wiki/Game_theory).

I recently watched a video talking about the ["Iterated Prisoner's Dilemma"](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma#The_iterated_prisoner's_dilemma).
In the version I watched, centered around Axelrod's Tournament, people submitted BASIC programs to compete in a game where
both programs "cooperating" earned them each 5 points, only one cooperating earned that one 3 (and the other 0), and neither 
cooperating earned them both 1. Breaking this down a bit:

- If you only ever focus on yourself (don't choose to cooperate) you'll earn at most 3 points or as little as 1 point
- The fact that the game is played continuously with the same agents is important. The agents have _memory_ and there's no end in sight
- Cooperation takes _continued trust_, but yields the highest outcome for everyone

This kind of experimental study is used to help us understand otherwise confounding behaviors in evolved creatures.
We're quite literally evolved to work together. Which is a good thing, since "working together" is usually a requirement
for a successful organization.

# A simple thought experiment

Let's take away everything that goes into software development that _isn't_ interacting with source code control.
After you stop salivating about no longer worrying about CI, JIRA, or Agile, you then take the code from every repo
in your org (within reason) and shove them each in a subdirectory in a new single organization.

...what do you think would happen over time? What kind of culture would emerge?

# Conclusion

Coding is a social activity. As evolved, social beings we work best when we're "all in the same room"
so to speak. That includes our code - one of (but not our only) means of communication.

(And once we decide to cooperate and collaborate, I'm sure we'll find solutions to the technical problems a monorepo
usually entails. I'm not sure it won't be Bazel (sorry))
