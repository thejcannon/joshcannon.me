---
title: "What's in a name?"
excerpt: "Inspecting filenames of PyPI packages."
---

# Background

Naming is important (as well as hard). Good names are good. Bad names are... bad.
And we name a lot of things. In Python (a name) code is bundled and uploaded as a package 
(another name), usually to the Python Package Index (PyPI, a third name). Inside of these
packages is code. Most commonly, Python code (but they truly can contain anything
([like whole books](https://discuss.python.org/t/user-uploading-books-to-pypi-disguised-as-wheels/24096)).
The only relationship between the package name and the module name(s) is the same as the 
relationship between a cat's name and its demeanor. _Usually_ "fluffy" is a fluffy cat,
but it's a convention. "Cupcake" could be the name of a very very naughty kitten.

You install `requests` and import `requests`. You install `typing-extensions` and import
`typing_extensions`. You install `python-dateutil` you import `dateutil` (I guess it isn't
`python_dateutil` because that would imply you could import `go_dateutil` and that's a can
of worms the author(s) didn't want to open). But, again, this is merely a convention.

So let's say you wanted to map module names to package names? How well would you be doing
so only via conventions? How unique are modules? What are the conventions, and who isn't following them?

Well, that's exactly what I needed to find out for my hobby project, so hop in! Come along!

# The plan

## Step 1: We need data

Hugo van Kemenade has [this list](https://hugovk.github.io/top-pypi-packages/) 
of the top 8000 most downloaded packages on PyPI, updated monthly. That was easy (Thanks Hugo!).

PyPI has [a nice simple API](https://wiki.python.org/moin/PyPISimple) (quite literally) for
getting links to downloadables for a package.

`pip` wants to extract METADATA out of wheels (which are just zips) without downloading the 
entire thing, so it has some [clever code](https://github.com/pypa/pip/blob/main/src/pip/_internal/network/lazy_wheel.py)
for doing "range requests" to only fetch a fraction of the bytes. (For tarballs, we're out of luck).

Swirl all that in a big pot, and voila! You can quickly scrape PyPI to get each package's filenames.

## Step 2: That was too easy, let's add some complexity

Since getting data was kinda easy, the universe has evened things out by making analyzing that data
(in a useful way) kinda hard. That's for two reasons:

1. Source distributions (sdists, as opposed to binary ones, bdists) go through a build process.
   That means there is only a loose relationship between the files inside them and the files that
   would be inside a built distribution (part of that build process could be moving or creating files).
   There are 658 sdist-only packages on the list.
3. Namespace packages. Namespaces might've been "one honking great idea" but namespace _packages_
   are usually misunderstood, and a honking painful thing to have to remember.

The solution to 1. is easy, just build (most of) them myself (how I did this is worthy of a blog post to come).

The solution to 2. is annoyingly complex. Namespace packages come in two forms:

1. Implicit namespace packages. These are the reason you can `mkdir foo`, then `import foo` even though
   there's no `__init__.py` in it. Any directory can be imported without a `__init__.py` and is treated as
   an _implicit_ namespace packages. That's a daily annoyance for me, but in this case its actually easier to handle.
2. Explicit namespace packages. These have a `__init__.py` with one or two magic incantations that basically say
   "I'm a namespace". And they can't/shouldn't have much more.

Because of 2., if I was to try and find what common "prefixes" a package has by simply looking at filenames,
both `opencensus` and `opencensus-context` and `opencensus-ext-azure` would all claim `opencensus`.

So, for any `__init__.py` whose path shows up in more than one package, we need to see if it contains one of the
magic incantations.

## Step 3: Let's have fun with data

([Link to online `datasette`](lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite)
which all of the following links will use. I can't guarantee, however, the schema won't change.
)

So, of the 7,893 packages scraped:

- [7,337 wheels were found on PyPI](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29+FROM+packages%0AWHERE+url+LIKE+%22%25pythonhosted.org%25%22)
- [I built another 556](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29+FROM+packages%0AWHERE+url+LIKE+%22%25github.com%25%22)
- [But 217 packages didn't have an importable file](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29%0AFROM+packages+p%0ALEFT+JOIN+filepaths+f+ON+p.package_name+%3D+f.package_name%0AWHERE+f.package_name+IS+NULL%0AORDER+BY+p.package_name)
  - Most of these are `types-` or `-stubs`
  - Some were "meta" packages that just contained requirements on other packages

Which leaves us with 7676 packages to analyze.

### Fun with the `filepaths` table

This table is a simple "what Python files of valid importable names are in the zip?"

- [Sorting by filecount, descending](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+package_name%2C+COUNT%28filepath%29+AS+filepath_count%0AFROM+filepaths%0AGROUP+BY+package_name%0AORDER+BY+filepath_count+DESC)
  shows us: 
  - `ansible` tops the chart with 13,650 files,
  - followed by `plotly` at 13,443 files,
  - and `oci` with 12,778 files
- [There are 802 packages with only a single file](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29%0AFROM+%28%0A++++SELECT+package_name%0A++++FROM+filepaths%0A++++GROUP+BY+package_name%0A++++HAVING+COUNT%28filepath%29+%3D+1%0A%29)
- [There are 210 packages which include a top-level `test` or `tests` directory](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28DISTINCT+package_name%29+FROM+filepaths%0AWHERE+filepath+LIKE+%22test%2F%25%22+%0AOR+filepath+LIKE+%22tests%2F%25%22)
  - (This can get annoying if your Python set up finds these before finding your tests directory,
    as your tests won't be importable)

### Fun with the `namespace_packages` table

These filepaths are `__init__.py` filepaths found in >1 package.

Out of 8,829 candidate package/filepath combinations:

- [There are 3408 distinct filepaths](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=select+COUNT%28DISTINCT+filepath%29+from+namespace_packages)
- [Only 180 of the 8,829 are explicit namespace packages](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=select+COUNT%28filepath%29+from+namespace_packages+WHERE+is_namespace+%3D+1)
  representing only [91 distinct filepaths](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=select+COUNT%28DISTINCT+filepath%29+from+namespace_packages+WHERE+is_namespace+%3D+1)
- [63 filepaths are marked as a namespace package in one package, but not in another](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29%0AFROM+%28%0A++++SELECT+filepath%0A++++FROM+namespace_packages%0A++++GROUP+BY+filepath%0A++++HAVING+COUNT%28DISTINCT+is_namespace%29+%3D+2%0A%29)
  - Virtually all of these are from packages which have undergone some kind of migration,
    and therefore the colliding packages shouldn't be installed at the same time anyways.
- [3320 filepaths appeared in multiple packages and _weren't_ marked as namespace packages](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29+FROM+%28%0A++SELECT+DISTINCT+filepath%0A++FROM+namespace_packages%0A++WHERE+is_namespace+%3D+0%0A++GROUP+BY+filepath%0A++HAVING+COUNT%28DISTINCT+package_name%29+%3E+1%0A%29)
  - From [scrolling the data](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+filepath%2C+%0A+++++++GROUP_CONCAT%28DISTINCT+package_name%29+AS+package_names%0AFROM+namespace_packages%0AWHERE+is_namespace+%3D+0%0AGROUP+BY+filepath%0AHAVING+COUNT%28DISTINCT+package_name%29+%3E+1)
    it appears these are largely from packages which are alternates (or forks) of other packages.
 - [the deepest namespace packages are](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+DISTINCT+filepath%0AFROM+namespace_packages%0AWHERE+is_namespace+%3D+1%0AORDER+BY+LENGTH%28filepath%29+-+LENGTH%28REPLACE%28filepath%2C+%27%2F%27%2C+%27%27%29%29+DESC)
   - `aws_cdk/aws_cloudfront/experimental` and `azureml/train/automl` at 3 directories deep

### Fun with the `prefixes` table

These prefixes are calculated by:

- Take the filepaths for a package
- Remove any `__init__.py` files that are namespace packages
- Calculate the lowest common ancestor among the Python files

The intent is to try and find unambiguous prefixes for each package.

Of 16,681 total package/prefix combos (with 16,177 distinct prefixes):

- [7147 packages have one prefix](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29%0AFROM+%28%0A++++SELECT+package_name%0A++++FROM+package_prefixes%0A++++GROUP+BY+package_name%0A++++HAVING+COUNT%28prefix%29+%3D+1%0A%29)
- [On the other end, sorting packages by prefix count reveals](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+package_name%2C+COUNT%28prefix%29+AS+prefix_count%0AFROM+package_prefixes%0AGROUP+BY+package_name%0AORDER+BY+prefix_count+DESC)
  - `ansible` tops the charts with 5,915 prefixes
    - This is because there are _a lot_ of nested directories with only one Python file in them and no `__init__.py`,
      making that a "unique" prefix.
  - (In fact most of the high-prefixers are due to a lack of `__init__.py`)
  - [So if we filter out prefixes of multiple depths](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+package_name%2C+%0A+++++++COUNT%28prefix%29+as+prefix_count%2C%0A+++++++GROUP_CONCAT%28prefix%29+as+prefixes%0AFROM+package_prefixes%0AWHERE+prefix+NOT+LIKE+%22%25%2F%25%22%0AGROUP+BY+package_name%0AORDER+BY+prefix_count+DESC)
    - `timedelta` now tops the charts with __130 unique prefixes__
    - It (and its friends near the top of the chart) all appear to be a snafu
      and didn't intend to include several dozens of directories in the wheel.
- [360 prefixes are shared by more than one package](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+p1.prefix%2C+GROUP_CONCAT%28p1.package_name%29+AS+packages%0AFROM+package_prefixes+p1%0AJOIN+package_prefixes+p2+ON+p1.prefix+%3D+p2.prefix+AND+p1.package_name+%21%3D+p2.package_name%0AGROUP+BY+p1.prefix%0AORDER+BY+p1.prefix)
  - However, just like shared filepaths, it appears these are largely from packages
    which are alternates (or forks) of other packages.
  - Some are legitimate though, like `haystack` being a prefix of both `django-haystack` and `haystack-ai`

## Step 4: Funtime is over, let's find conventions

By far, the most common convention is (unsurprisingly) [normalizing](https://packaging.python.org/en/latest/specifications/name-normalization/#name-normalization)
the module name:

- [5,551 prefixes map to their package name after normalization](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29%0AFROM+package_prefixes+pp%0AWHERE+pp.package_name+%3D+REPLACE%28LOWER%28pp.prefix%29%2C+%22_%22%2C+%22-%22%29%0AORDER+BY+pp.package_name+DESC)
  - E.g. `requests` -> `requests` or `sqlalchemy_views` -> `sqlalchemy-views` or `ShazamAPI` -> `shazamapi`
  - [Of those, 5,303 prefixes _solely_ identify their package](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29%0AFROM+package_prefixes+pp%0AWHERE+pp.package_name+%3D+REPLACE%28LOWER%28pp.prefix%29%2C+%22_%22%2C+%22-%22%29%0A++AND+NOT+EXISTS+%28%0A++++SELECT+1%0A++++FROM+package_prefixes+pp2%0A++++WHERE+pp2.package_name+%3D+pp.package_name%0A++++++AND+pp2.prefix+%21%3D+pp.prefix%0A++%29%0AORDER+BY+pp.package_name+DESC)
    - E.g. `pytest` wouldn't count because `_pytest` and `py` are also prefixes.
    - __That's almost 70% of packages!__
- There are a few common prefixes/suffixes, too (numbers are packages with 1 prefix):
  - [`python-` prefix adds 84](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29%0AFROM+package_prefixes+pp%0AWHERE+pp.package_name+%3D+%27python-%27+%7C%7C+REPLACE%28LOWER%28pp.prefix%29%2C+%22_%22%2C+%22-%22%29%0A++AND+NOT+EXISTS+%28%0A++++SELECT+1%0A++++FROM+package_prefixes+pp2%0A++++WHERE+pp2.package_name+%3D+pp.package_name%0A++++++AND+pp2.prefix+%21%3D+pp.prefix%0A++%29%0AORDER+BY+pp.package_name+DESC),
  [`-python` suffix adds 22](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29%0AFROM+package_prefixes+pp%0AWHERE+pp.package_name+%3D+REPLACE%28LOWER%28pp.prefix%29%2C+%22_%22%2C+%22-%22%29+%7C%7C+%27-python%27%0A++AND+NOT+EXISTS+%28%0A++++SELECT+1%0A++++FROM+package_prefixes+pp2%0A++++WHERE+pp2.package_name+%3D+pp.package_name%0A++++++AND+pp2.prefix+%21%3D+pp.prefix%0A++%29%0AORDER+BY+pp.package_name+DESCZ)
  - [`py` prefix adds 62](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29%0AFROM+package_prefixes+pp%0AWHERE+pp.package_name+%3D+%27py%27+%7C%7C+REPLACE%28LOWER%28pp.prefix%29%2C+%22_%22%2C+%22-%22%29%0A++AND+NOT+EXISTS+%28%0A++++SELECT+1%0A++++FROM+package_prefixes+pp2%0A++++WHERE+pp2.package_name+%3D+pp.package_name%0A++++++AND+pp2.prefix+%21%3D+pp.prefix%0A++%29%0AORDER+BY+pp.package_name+DESC),
    [`-py` suffix adds 33](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29%0AFROM+package_prefixes+pp%0AWHERE+pp.package_name+%3D+REPLACE%28LOWER%28pp.prefix%29%2C+%22_%22%2C+%22-%22%29+%7C%7C+%27-py%27%0A++AND+NOT+EXISTS+%28%0A++++SELECT+1%0A++++FROM+package_prefixes+pp2%0A++++WHERE+pp2.package_name+%3D+pp.package_name%0A++++++AND+pp2.prefix+%21%3D+pp.prefix%0A++%29%0AORDER+BY+pp.package_name+DESC)
  - [`django-` prefix adds 115](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29%0AFROM+package_prefixes+pp%0AWHERE+pp.package_name+%3D+%27django-%27+%7C%7C+REPLACE%28LOWER%28pp.prefix%29%2C+%22_%22%2C+%22-%22%29%0A++AND+NOT+EXISTS+%28%0A++++SELECT+1%0A++++FROM+package_prefixes+pp2%0A++++WHERE+pp2.package_name+%3D+pp.package_name%0A++++++AND+pp2.prefix+%21%3D+pp.prefix%0A++%29%0AORDER+BY+pp.package_name+DESC)
  - [`pyobjc-framework-` prefix adds 135](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29%0AFROM+package_prefixes+pp%0AWHERE+pp.package_name+%3D+%27pyobjc-framework-%27+%7C%7C+REPLACE%28LOWER%28pp.prefix%29%2C+%22_%22%2C+%22-%22%29%0A++AND+NOT+EXISTS+%28%0A++++SELECT+1%0A++++FROM+package_prefixes+pp2%0A++++WHERE+pp2.package_name+%3D+pp.package_name%0A++++++AND+pp2.prefix+%21%3D+pp.prefix%0A++%29%0AORDER+BY+pp.package_name+DESC)
- Then for multi-level prefixes:
  - [441 more are found by replacing the `.` with `-`](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29%0AFROM+package_prefixes+pp%0AWHERE+pp.package_name+%3D+REPLACE%28REPLACE%28LOWER%28pp.prefix%29%2C+%22_%22%2C+%22-%22%29%2C+%27%2F%27%2C+%27-%27%29%0A++AND+NOT+EXISTS+%28%0A++++SELECT+1%0A++++FROM+package_prefixes+pp2%0A++++WHERE+pp2.package_name+%3D+pp.package_name%0A++++++AND+pp2.prefix+%21%3D+pp.prefix%0A++%29%0A++AND+prefix+LIKE+%22%25%2F%25%22%0AORDER+BY+pp.package_name+DESC)
    - E.g. `flufl.lock` -> `flufl-lock`
 - [Then 52 more with an `apache-` prefix](https://lite.datasette.io/?url=https%3A%2F%2Fthejcannon.github.io%2FPyPIPackageMapper%2Fpackage_database.sqlite#/package_database?sql=SELECT+COUNT%28*%29%0AFROM+package_prefixes+pp%0AWHERE+pp.package_name+%3D+%27apache-%27+%7C%7C+REPLACE%28REPLACE%28LOWER%28pp.prefix%29%2C+%22_%22%2C+%22-%22%29%2C+%27%2F%27%2C+%27-%27%29%0A++AND+NOT+EXISTS+%28%0A++++SELECT+1%0A++++FROM+package_prefixes+pp2%0A++++WHERE+pp2.package_name+%3D+pp.package_name%0A++++++AND+pp2.prefix+%21%3D+pp.prefix%0A++%29%0A++AND+prefix+LIKE+%22%25%2F%25%22%0AORDER+BY+pp.package_name+DESC)

So sticking solely to normalization, and applying some common prefixes/suffixes, you get...

__81% of packages__ have a single prefix, which when normalized directly correlates to the package name.

# Conclusion, and next steps

So here we are. Sitting on a pile of data, and a concrete understanding of 
package name -> module name conventions 
(which I'm sure most of y'all reading already had on your BINGO card). 
But we've turned hunch into proof, and more importantly we can also compile a little mapping
of the top packages' prefixes that _don't_ fit the mold.

If you're already publishing packages to PyPI, or planning to do so, be a peach::

- Stick to a convention for your module names
- Upload wheels
- Avoid implicit or explicit namespace packages if you can help it
  - Otherwise, if you have to choose... well, you know the saying ;)

I'll probably run this collection periodically, and maybe even evolve it some.
However, now I can get back to my hobby project (as well as this hobby project's
hobby project: building wheels where missing)..
