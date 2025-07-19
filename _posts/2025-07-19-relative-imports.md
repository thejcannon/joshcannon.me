---
title: "Python: Relative vs Absolute Imports"
subtitle: "9 out of 10 Pythonistas agree..."
---

In the PyTexas Discord my fellow PyTexas Organizer and friend, Mason Egger, asked:

> Do you prefer absolute or relative imports for inter-module imports within applications?

Go ahead and [call me a sith](https://youtu.be/wgpytjlW5wU?si=qoLqiNyuv0EJPpqD) because I deal in absolutes.

And here's why.

# Ways of running Python files

Python has more than a few ways of running a "Python file":

- `python path/to/file.py`: Run the file at this path
- `python -m path.to.file`: Run the module found with this dotted name
- `python path/to`: Run the `__main__.py` file under this directory path
- `python -m path/to`: Run the module found with this dotted name, which this time would be the directory's `__init__.py`
- `python path/to/zipapp.zip`: Run this [zipapp](https://docs.python.org/3/library/zipapp.html)
- `pytest` or any other installed script name: Run the script found at `<Python environment directory>/bin/<name>`, e.g. `.venv/bin/pytest`

# Ways of laying out Python code

There are a techincally infinite number of ways of "laying out" Python code, however the [Python Packaging User Guide](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
suggests two main ones: **src lyout** and **flat layout**.

## src layout

This layout has your source code underneath the directory named `src`. It looks something like:

```
.
├── README.md
├── pyproject.toml
├── src/
│   ├── macaroni/
│   │   ├── salad.py
│   │   └── and/
│   │       └── cheese.py
│   └── spaghetti/
│       ├── squash.py
│       └── and/
│           └── meatballs.py
└── scripts/
    └── release.py
```

## flat layout

The flat layout looks very similar...

```
.
├── README.md
├── pyproject.toml
├── macaroni/
│   ├── salad.py
│   └── and/
│       └── cheese.py
├── spaghetti/
│   ├── squash.py
│   └── and/
│       └── meatballs.py
└── scripts/
    └── release.py
```

## What's the difference?

The Python Packaging User Guide (linked above) does a pretty good job of breaking this down, so I won't.

# Ways of importing your fellow module

- `from . import sibling`: Imports `sibling` from the same directory this module is in
  - This first would try to import attribute `subling` from `__init__.py`, or
  - then try to import the module named `subling` (either `sibling/__init__.py` or `sibling.py`)
- `from .sibling import boogers`: Same idea
