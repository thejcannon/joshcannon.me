---
title: Python Namespace Packages are a pain
subtitle: there's no Zen here
---

TL;DR: Just use `__init__.py` in every directory. Please.

# Background

This blog post is about Python "namespace packages". Unfortunately because the Zen of Python didn't include "There should be one-- and preferably only one --defintion for a term", I have to disambiguate.

I assume when you read "Python package" your first thought is of packages as found on the Python Package Index
(PyPI for short, pronunciation: "🥧 P 👁️"). That is mine as well. However, in the statement `import x.y`, Python calls `x` a 
["module"](https://docs.python.org/3/tutorial/modules.html#modules) as well as a 
["package"](https://docs.python.org/3/tutorial/modules.html#packages), and `y` a "submodule" and a "subpackage".

And now a tongue twister: "[Petr](https://github.com/encukou) promptly packaged Python package [`pello`](https://github.com/fedora-python/Pello/tree/master/pello) producing Python package `pello`, then published Python package `pello` containing Python package `pello` to the [Python Package Index](https://pypi.org/project/Pello/) promptly.

...whew!

In order to disambiguate, we can use the term
["distribution packages"](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package)
to refer to the PyPI-flavored ones 
and ["import packages"](https://packaging.python.org/en/latest/glossary/#term-Import-Package)  
for the module-flavored ones.

## Definition(s) and Terminology

[PEP 420](https://peps.python.org/pep-0420/) starts with

> Namespace packages are a mechanism for splitting a single Python package across multiple directories on disk.

A better definition might be

> Namespace packages are a mechanism for splitting a single Import Package across one or more directories on disk.
> They can either be "explicit" or "implicit", depending on the mechanism.

[The Python docs](https://docs.python.org/3/glossary.html#term-namespace-package) define namespace packages as:

> A package which serves only as a container for subpackages. \[...]

This is the most correct, in my opinion, because Python import packages don't have to come from directories on disk.
They may also come from other exotic places like [zip archives](https://docs.python.org/3/library/zipimport.html).

## Rationale

Let's say you're a megacorp named Gooble and you want all of your code to be known to be Gooble code so you'd prefer
all of your modules to start with `gooble.`. You now have a choice. Put everything inside of one distribution package named
`gooble` (combining code for your Earth Engine with Big Lake code along with your Cloud APIs - 
much to the confusion of Hydrologists everywhere). Or split things into logical sections, each _sharing_ a piece of 
the `gooble.` pie, making `gooble` a namespace package.

You may be thinking "ok, so what's the big deal?" - and in most "vanilla" cases there'd be no big deal. Most of the time you
install a Python package, it goes into some `site-packages` directory along with all its installed brothers and sisters
and cousins. Install `gooble-storage` and `site-packages/gooble/storage/...` exists.
Likewise install `gooble-functions` and `site-packages/gooble/functions/...` will join in.

There are other ways of loading modules from disk, however. And therein lies the challenge.

## The challenge

The reason the code in your `site-packages` is found when you `import` is due to Python's default [path based finder](https://docs.python.org/3/glossary.html#term-path-based-finder).
It works kinda like this:

- Given a module (like `gooble`), iterate through the paths in `sys.path` trying to find a valid `gooble` module underneath.
  This may look like `gooble/__init__.py` or `gooble.py` or any of the other valid ways of defining a Python module on disk.
- Given a submodule (like `gooble.firewall`), first load module `gooble`, take the path we found it at (`__path__`) and look
  underneath for submodule `firewall`.

Undoubtedly, your `sys.path` has your `site-packages` directory in it, and this is how most "third-party" code is
loaded most of the time.

But imagine with me, instead of a single `sys.path` entry containing every installed distribution package we instead
used one `sys.path` entry for _each_ distribution package. This is certainly an attractive idea if you were designing
a Python environment manager with an emphasis on speed. Each package could be installed, in parallel, into a cache directory
and then in order to construct a Python environment you'd simply need to populate `sys.path` with the correct cache directories.

Re-enter `gooble`. How should the default path finder find `gooble.firestore`, given it already loaded `gooble` and `gooble.firebase` from `/cached/gooble-firebase/gooble/firebase.py`?

Namespace packages is the how. They are mechanism for splitting a single Import Package across one or more directories on disk.

# Namespace Packages

So now we know what namespace packages aim to solve. Its a way to tell the import machinery that an import package belongs
to many (or none, depending on how you want to look at it) distribution packages, and all that entails.

Historically, there were only _explicit_ namespace packages (I suspect at the time they were just called "namespace packages",
and then PEP 420 came along and gave us _implicit_ namespace packages). Of course, the Zen of Python does say
"There should be one-- and preferably only one --obvious way to do it" but I'm not sure it applies here, given it isn't called
"the Zen of Python Packaging". I suspect that rule was skipped over and the rule which reads 
"Namespaces are one honking great idea -- let's do more of those!" was instead double-clicked on.

## Explicit Namespace Packages

These come in two flavors, but they both accomplish roughly the same thing:
declaring a Python import package as a namespace package. In your namespace package (`gooble/__init__.py` in our case), use

```py
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
# or...
import pkg_resources
pkg_resources.declare_namespace(__name__)
```

These use `__path__` shenanigans to trick the Python import machinery into searching additional directories when
searching for submodules.

It is important to note that one quirk of this solution is that _every_ `gooble/__init__py` in _every_ distribution package
MUST agree on doing this. Otherwise, if `gooble-cloud-walk` accidentally shipped an empty `gooble/__init__.py` _AND_ it had
an "early" `sys.path` entry, then it claims the import package `gooble` all to itself.

Remember these are the "old" way.

## Implicit Namespace Packages

PEP 420 gave us a (better) alternative, implicit namespace packages. These are easy to make and easy to explain.
Just don't make `gooble/__init__.py`. Easy peasy lemon squeezy. The import machinery was changed to allow this
new way of saying "hey keep looking for `gooble.cloud_build`.

We still have to make sure every `gooble` distribution package agrees _NOT_ to contain the file, but now we don't have
to worry about multiple distribution packages containing the same path.

(If you've ever forgotten to make a `__init__.py` file and importing still worked - this is why)

# The Pain of Python (Namespace Packages)

Unfortunately, both _explicit_ and _implicit_ namespace packages still exist today - meaning we have two ways of accomplishing
the same thing (two strikes against "the Zen"  - one for having "one obvious way" and one for "explicit is better than implicit").

Secondly, newcomers (or forgetful old-timers) might omit the `__init__.py` and now implicitly have an implicit namespace package.
(as opposed to someone adhering to PEP 420 and explicitly having an implicit namespace package).
There's also a slight import performance hit when doing this (but likely not enough to matter).

Third, for hard-workin' folks like myself who would like to [associate module (and submodule) names to packages](https://joshcannon.me/2024/07/05/package-names.html),
this is nigh impossible. It's impossible to correctly determine if the omission of a `__init__.py` was implicit or explicit.
Educated guesses can be made, but as we can see from that blog post they are just guesses.

Fourth, implicit namespace packages are still brittle. Developer X knows that `gooble/` is a namespace package and omits `__init__.py`.
But it can very easily be added. Consider how many Pull Requests you've reviewed where you've scrutinized the addition of a `__init__.py` file (hint: it's likely an integer less than one). This is because explicit really is better than implicit.

Last, because most installations involve overlapping unpacking in a shared directory (`site-packages`), there are several
distribution packages which have namespace import packages, but lack the mechanism. It's all too easy to have `gooble-deploy` 
and `gooble-console` contain `gooble/__init__.py`, and everything "just work" _most of the time_. This is a large reason
environment-management tools _don't_ use the `sys.path` trick. It exposes annoying and hard-to-diagnose bugs.

# Conclusion

Namespace packages are a useful mechanism which solves a real problem. However, the precise semantics come at the cost of 
cognitive complexity, especially for developer tool authors/maintainers. Here are my suggestions:

- Avoid accidental namespace packages - always include `__init__.py` files in directories
- Avoid purposeful namespace packages - they're a pain in the ass

# References

- [PEP 420](https://peps.python.org/pep-0420/)
- [Packaging Namespace Packages](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/)
- [Python Glossary - "Namespace Package"](https://docs.python.org/3/glossary.html#term-namespace-package)
- [Python Language Reference - "Namespace Packages"](https://docs.python.org/3/reference/import.html#reference-namespace-package)
