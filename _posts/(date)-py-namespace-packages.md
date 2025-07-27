---
title: Python Namespace Packages are a pain
subtitle: Where something can be explicitly implicit
---

# Namespace Packages

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

---


## To-write

- Background
- Import Mechanics? (__file__, __path__, file loader)
- Implicit Namespace Packages
- Explicit Namespace Packages
