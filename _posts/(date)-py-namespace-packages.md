---
title: Python Namespace Packages are a pain
subtitle: the Zen of Python has no power here
---

# Background

This blog post is about Python "namespace packages". Unfortunately because the Zen of Python didn't include "There should be one-- and preferably only one --defintion for a term", I have to disambiguate.

I assume when you read "Python package" your first thought relates to packages as found on the Python Package Index
(PyPI for short, pronounciation: "🥧 P 👁️"). That is mine as well. However, in the statement `import x.y`, Python calls `x` a 
["module"](https://docs.python.org/3/tutorial/modules.html#modules) as well as a 
["package"](https://docs.python.org/3/tutorial/modules.html#packages), and `y` a "submodule" and a "subpackage".

And now a toungue twister: "[Petr](https://github.com/encukou) promptly packaged Python package [`pello`](https://github.com/fedora-python/Pello/tree/master/pello) producing Python package `pello`, then published Python package `pello` containing Python package `pello` to the [Python Package Index](https://pypi.org/project/Pello/) promptly.

...whew!

In order to disambiguate, we can use the term
["distribution packages"](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package)
to refer to the PyPI-flavored ones and ["import packages"](https://packaging.python.org/en/latest/glossary/#term-Import-Package)  
for the module-flavored ones.

## Definition and Terminology

[PEP 420](https://peps.python.org/pep-0420/) starts with

> Namespace packages are a mechanism for splitting a single Python package across multiple directories on disk.

A better definition might be

> Namespace packages are a mechanism for splitting a single Import Package across one or more directories on disk.
> They can either be "explicit" or "implicit", depending on the mechanism.

(if you're reading this from the future, then ideally the Python Packaging Index Glossary now contains a definition
for "namespace package" along the lines of the above. [PR 1882](https://github.com/pypa/packaging.python.org/pull/1882))

Historically, there were only _explicit_ namespace packages (I suspect at the time they were just called "namespace packages",
and then PEP 420 came along and gave us _implicit_ namespace packages. Of course, the Zen of Python does say
"There should be one-- and preferably only one --obvious way to do it" but I'm not sure it applies here, given it isn't called
"the Zen of Python Packaging". It could be of course that that rule was skipped over and "Namespaces are one honking great idea -- let's do more of those!" was instead double-clicked on. We may never know.

# Rationale

Let's say you're a megacorp named Gooble and you want all of your code to be known to be Gooble code so you'd prefer
all of your modules to start with `gooble.`. You now have a choice. Put everything inside of one distribution package named
`gooble` (combining code for your Earth Engine with Big Lake code along with your Cloud APIs - 
much to the confusion of Hydrologists everywhere). Or split things into logical sections, each _sharing_ a piece of 
the `gooble.` pie, making `gooble` is a namespace package.

# A Detour through Python Import Machinery

Let's focus a moment on Python's [path based finder](https://docs.python.org/3/glossary.html#term-path-based-finder).
It works kinda like this:

- Given a module (like `gooble`), iterate through the paths in `sys.path` trying to find a valid `gooble` module underneath.
  This may look like `gooble.py` or `gooble/__init__.py` or any of the other valid ways of defining a Python module on disk.
- Given a submodule (like `gooble.firewall`), first load module `gooble`, take the path we found it at (`__path__`) and look
  underneath for submodule `firewall`.

This is a useful optimization, ensuring we only ever really iterate through at most a list-of-directories,
instead of hiking up and down file heirarchies.

TODO: (mention different names in sys.path)


## To-write

- Import Mechanics? (__file__, __path__, file loader)
- Implicit Namespace Packages
- Explicit Namespace Packages
