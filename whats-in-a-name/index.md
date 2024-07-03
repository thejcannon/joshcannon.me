---
title: "What's in a name?"
excerpt: "Inspecting filenames of PyPI packages."
---

# Background

Naming is important (as well as hard). Good names are good. Bad names are... bad.
And we name a lot of things. In Python (a name) code is budled and uploaded as a package 
(another name), usually to the Python Package Index (PyPI, a third name). Inside of these
packages is code. Most commonly, Python code (but they truly can contain anything).
The only relationship between the package name and the module name(s) is the same as the 
relationship as between a cat's name and its demeanor. _Usually_ "fluffy" is a fluffy cat,
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

Hugo van Kemenade, has [this list](https://hugovk.github.io/top-pypi-packages/) 
of the top 8000 most downloaded packages on PyPI, updated monthly. That was easy (Thanks Hugo!).

PyPI has [a nice simple API](https://wiki.python.org/moin/PyPISimple) (no quite literally) for
gettings links to downloadables for a package.

`pip` wants to extract METADATA out of wheels (which are just zips) without downloading the 
entire thing, so it has some [clever code](https://github.com/pypa/pip/blob/main/src/pip/_internal/network/lazy_wheel.py)
for doing "range requests" to only fetch a fraction of the bytes. (For tarballs, we're out of luck).

Swirl all that in a big pot, and voila! You can quickly scrape PyPI to get each package's filenames.

## Step 2: That was too easy, let's add some complexity

Since getting data was kinda easy, the universe has evened things out by making analyzing that data
in a useful way kinda hard. That's because of two reasons:

1. Source distributions (sdists, as opposed to binary ones, bdists) go through a build process. That means there is
   only a loose relationship between the files inside them and the files that would be inside a built
   distribution (part of that that build process could be moving, moving, or creating files).
   There are 658 sdist-only packages on the list.
3. Namespace packages. Namespaces might've been "one honking great idea" but namespace _packages_
   are usually misunderstood and a honking painful thing to have to remember.

The solution to 1. is easy, let's ignore them.

The solution to 2. is annoyingly complex. Namespace packages come in two forms:

1. Implicit namespace packages. These are the reason you can `mkdir foo`, then `import foo` even though
   there's no `__init__.py` in it. Any directory can be imported without a `__init__.py` and is treated as
   an _implicit_ namespace packages. That's a daily annoyance for me, but in this case its actually preferable.
2. Explicit namespace packages. These have a `__init__.py` with one or two magic incantations that basically say
   "I'm a namespace". And they can't/shouldn't have much more.

Because of 2., if I was to try and find what common "prefixes" a package has by simplying looking at filenames,
both `opencensus` and `opencensus-context` and `opencensus-ext-azure` would all claim `opencensus`.

So, for any `__init__.py` whose path shows up in more than one package, we need to see if it contains one of the
magic incantations.

## Step 3: Let's have fun

So, of the 7258 packages (663 sdists, and 3 bdists of weird extensions, and 79 packages with no valid Python files) scraped...

### Oops

The most common prefixes[^1] are:

```
tests|111
test|34
nvidia|22
examples|10
docs/conf|9
benchmarks|5
docs|5
__init__|4
cv2|4
docs/source/conf|4
```

Which is slightly annoying that installation of over 100 packages might take "place" of the top-level `tests` module name,
depending on how I structure my project.

For the rest of the statstics, we'll pretend the following prefixes don't exist: `setup`, `test`, `tests`, `doc`, `docs`, `examples`, `benchmarks`, `scripts`, etc...

### Conventions

TODO: Lowercase the prefix for these

- 3330 packages are identified by a prefix which is the normalized package name. E.g. (`requests` -> `requests`)
   - 3089 of those packages are _uniquely_ identified by that single prefix. (Meaning they have no other prefix).
     - E.g. `pytest`-the-package is identified by `pytest`-the-module, so it meets criteria one. But `pytest`-the-package
       also has the prefix of `_pytest` (anf `py`), so it doesn't meet criteria two.
- Similarly, if we replaced hypens with underscores we'd add another 2166. Hyphens to path separators adds 381
   (if you were wondering which was more popular).
   - E.g. `typing-extensions` -> `typing_extensions` and `zope-browser` -> `zope/browser`, respectively
   - 2089 and 326 for _uniquely_ prerfixed, respectively.

(TODO: Also do replacing `'-'` with `''` (just smush it together)

So that leaves us with 2119 packages (7994 - 3330 - 2166 - 381) that don't follow the simple convention.

Perhaps there's just more conventions we should uncover?

### More Conventions - Prefixes and suffixes

- Of 134 packages which start with `types-`, 119 of them have a `-stubs` suffixed prefix.
  - These really shouldn't be imported, so we can just ignore all `types-` packages
- 68 packages/prefix combinations have `py` prefixing the package name (e.g. `pyusb` -> `usb`)
- 88 have a `python-` prefix
- 121 have a `django-` prefix
- 141 have a `pyobjc-framework` prefix
- 52 look like `apache-airflow-providers-*` -> `airflow/providers/*`
- 54 look like `aws-cdk-aws-*` -> `aws_cdk/aws_*/_jsii` [^9]
- TODO: `scikit` -> `sk*`
- TODO: `robotframework`

# Working our way back

So, you may remember I wanted to map module names to package names.
Let's see how successful applying these handful of conventions would net me.

Of 9940 prefixes,

- `package_name = module.lower().replace("_", "-")` -> handles 5590 prefixes (56%) [^10]
- otherwise, try `f"python-{package_name}"` -> 89 more
- otherwise, try `f"py{package_name}"` -> 72 more
- otherwise, try `f"django-{package_name}"` -> 121 more
- otherwise, try `f"django-{package_name}"` -> 141 more

Brings us to 60.5%.

---

[^1]: Query
      ```sql
      SELECT prefix, COUNT(*) as count
      FROM package_prefixes
      GROUP BY prefix
      ORDER BY count DESC
      LIMIT 10;
      ```

[^3]: Query
      ```sql
      SELECT COUNT(*) as matching_packages
      FROM packages p
      JOIN package_prefixes pp ON p.package_name = pp.package_name
      WHERE pp.prefix = p.package_name;
      ```

[^4]: Query
      ```sql
      WITH matching_packages AS (
          SELECT p.package_name
          FROM packages p
          JOIN package_prefixes pp ON p.package_name = pp.package_name
          WHERE pp.prefix = p.package_name
      ),
      prefix_counts AS (
          SELECT package_name, COUNT(*) as prefix_count
          FROM package_prefixes
          GROUP BY package_name
      )
      SELECT COUNT(*) as single_prefix_packages
      FROM matching_packages mp
      JOIN prefix_counts pc ON mp.package_name = pc.package_name
      WHERE pc.prefix_count = 1;
      ```

[^6]: Query
      ```sql
      SELECT p.package_name,
             GROUP_CONCAT(pp.prefix) AS prefixes
      FROM packages p
      LEFT JOIN package_prefixes pp ON p.package_name = pp.package_name
      WHERE NOT EXISTS (
          SELECT 1
          FROM package_prefixes pp2
          WHERE pp2.package_name = p.package_name
          AND (
              pp2.prefix = REPLACE(p.package_name, '-', '_')
              OR
              pp2.prefix = REPLACE(p.package_name, '-', '/')
          )
      )
      GROUP BY p.package_name
      HAVING prefixes IS NOT NULL;
      ```

[^7]: Query
      ```sql
      SELECT COUNT(DISTINCT package_name)
      FROM package_prefixes
      WHERE package_name LIKE "types-%"
        AND prefix LIKE "%-stubs"
        AND substr(package_name, 7) = substr(prefix, 1, length(prefix) - 6)
      ```

[^8]: Query
      ```sql
      SELECT p.package_name, pp.prefix
      FROM packages p
      JOIN package_prefixes pp ON p.package_name = pp.package_name
      WHERE p.package_name LIKE 'py%'
        AND (pp.prefix = SUBSTR(p.package_name, 3)
             OR pp.prefix = REPLACE(SUBSTR(p.package_name, 3), '-', '_')
             OR pp.prefix = REPLACE(SUBSTR(p.package_name, 3), '-', '/'));
      ```

[^9]: Query
      ```sql
      SELECT COUNT(*)
      FROM packages p
      JOIN package_prefixes pp ON p.package_name = pp.package_name
      WHERE p.package_name LIKE 'aws-cdk-aws-%'
        AND pp.prefix = 'aws_cdk/' || REPLACE(SUBSTR(p.package_name, 9), '-', '_') || '/_jsii';
      ```

[^10]: Query
      ```sql
      SELECT COUNT(*) as matching_packages
      FROM packages p
      JOIN package_prefixes pp ON p.package_name = pp.package_name
      WHERE LOWER(pp.prefix) = p.package_name
      OR LOWER(REPLACE(pp.prefix, "_", "-")) = p.package_name
      ```

```
SELECT COUNT(DISTINCT package_name)
FROM package_prefixes
WHERE 'django-' || LOWER(prefix) = package_name
   OR 'django-' || LOWER(REPLACE(prefix, '_', '-')) = package_name;
```

```
SELECT COUNT(*)
FROM package_prefixes pp
WHERE pp.package_name = 'apache-' || REPLACE(REPLACE(LOWER(pp.prefix), "_", "-"), '/', '-')
  AND NOT EXISTS (
    SELECT 1
    FROM package_prefixes pp2
    WHERE pp2.package_name = pp.package_name
      AND pp2.prefix != pp.prefix
  )
```

```
SELECT COUNT(*)
FROM package_prefixes pp
WHERE pp.package_name = REPLACE(REPLACE(LOWER(pp.prefix), "_", "-"), '/', '-')
  AND pp.prefix LIKE "%/%"
  AND NOT EXISTS (
    SELECT 1
    FROM package_prefixes pp2
    WHERE pp2.package_name = pp.package_name
      AND pp2.prefix != pp.prefix
  )
```
