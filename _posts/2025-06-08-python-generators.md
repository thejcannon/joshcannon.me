---
title: "How Python Generators (for the Systems-flovered folks)"
excerpt: 'AKA Watching the "A-HA" in realtime'
---

One of my favorite little joys in life is explaining, very simply, how and why Python generators work - at a very basic level - to
a "systems-flavored" (thing C, C++, etc...) programmer.

# The Stack and the Heap

Most "systems-flavored" programmers understand "the stack" and "the heap" as well as what goes where.

Particularly, that each function call has a corresponding "frame" on the stack, and that, in good stack-fashion,
the stack frame is popped off the stack when the function has completed.

# Python's memory model

As an interpreted language, it is not surprising that pretty much every non-implementation-detail part of Python
and its execution is on the heap. That includes objects, classes (which are objects), functions (which are objects),
and yes, even Python stack frames (which are... (drumroll please)... objects!).

# Generators

So, what fun things could you do if when it was time to pop a stack frame off the stack (which by the way, "the stack"
is also on the heap) you popped it, but kept the object (i.e. the memory) around? It's on the heap after all.

You could make functions which "pause" and "resume" as you decided to push and pop the frame on to and off of the stack.

---

A-HA!
