# Namespace Packages

This blog post is about Python "Packaging namespace packages", commonly referred to as "namespace packages".
It is, of course, delightfully ambiguous when you throw the fact that in the statement `import x.y`, Python calls
`x` a ["module"](https://docs.python.org/3/tutorial/modules.html#modules) as well as a ["package"](https://docs.python.org/3/tutorial/modules.html#packages),
and `y` a "submodule" and a "subpackage", thus making `x` a ["namespace package"](https://docs.python.org/3/glossary.html#term-namespace-package).

## To-write

- Background
- Import Mechanics? (__file__, __path__, file loader)
- Implicit Namespace Packages
- Explicit Namespace Packages
