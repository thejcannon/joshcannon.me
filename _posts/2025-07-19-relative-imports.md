---
title: "Python: Relative vs Absolute Imports"
subtitle: "9 out of 10 Pythonistas agree..."
---

In the PyTexas Discord my fellow PyTexas organizer and friend, Mason Egger, asked:

> Do you prefer absolute or relative imports for inter-module imports within applications?

Go ahead and [call me a Sith](https://youtu.be/wgpytjlW5wU?si=qoLqiNyuv0EJPpqD) because I deal in absolutes.

And here's why.

# Ways of running Python files

Python has more than a few ways of running a "Python file":

- `python path/to/file.py`: Run the file at this path
- `python -m path.to.file`: Run the module found with this dotted name
- `python path/to`: Run the `__main__.py` file under this directory path
- `python -m path/to`: Run the module found with this dotted name, which this time would be the directory's `__init__.py`
- `python path/to/zipapp.zip`: Run this [zipapp](https://docs.python.org/3/library/zipapp.html)
- `pytest` or any other installed script name: Run the script found at `<Python environment directory>/bin/<name>`, e.g. `.venv/bin/pytest`

# Ways of importing your fellow module

- `from . import sibling`: Imports `sibling` from under the same/parent directory this module is in
  - This first would try to import attribute `sibling` from `__init__.py`
  - then try to import the module named `sibling` (either `sibling/__init__.py` or `sibling.py`)
- `from .sibling import boogers`: Same idea, but this time we need to load module `sibling` and attribute/submodule `boogers`
- `from .. import uncle`: Imports `uncle` from under the grandparent directory (using similar rules)
- `from ..uncle import tickles`: (you get the jist)
- `from ... import great_aunt`: ...

These are all examples of _relative_ imports. What they import is _relative_ to the module importing them.

(By the way, in case you needed one, here's an example of an _absolute_ import: `from pkgname.child import fun`)

# Ways of running Python files which import their fellow modules

Given this [flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) project:

```
.
├── macaroni/
│   ├── __init__.py
│   ├── salad.py
│   └── and_/
│       ├── __init__.py
│       └── cheese.py
```

| Contents / Invocation| `python -m macaroni.and_.cheese` | `python macaroni/and_/cheese.py` |
| ------------- | ------------- | ------------- |
| `from ..salad import dressing` | 🎉  | 💥 `ImportError: attempted relative import with no known parent package` |
| `from macaroni.salad import dressing` | 🎉  | 🎉 |

# Why is that?

Buried in the Python docs' tutorials, in Chapter 6 "Modules", Section 4 "Packages", Subsection 2 "Intra-package References" ([6.4.2. here](https://docs.python.org/3/tutorial/modules.html#intra-package-references)),
there is this paragraph [^1]:

> Note that relative imports are based on the name of the current module’s package. Since the main module does not have a package, modules intended for use as the main module of a Python application must always use absolute imports.

When Python encounters a relative import, [it is relative to the current package](https://docs.python.org/3/reference/import.html#package-relative-imports),
which for the "main module" (the module being invoked), doesn't exist.

**The bottom line**: Absolute imports work consistently irrespective of how your Python file is executed. Relative imports don't give you that luxury.

---

[^1]: The paragraph used to read
  > Note that relative imports are based on the name of the current module. Since the name of the main module is always `"__main__"`, modules intended for use as the main module of a Python application must always use absolute imports.
  However, this was slightly incorrect so I suggested a change in [PR 136846](https://github.com/python/cpython/pull/136846).
