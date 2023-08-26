# Python2Json

[![Python 3.10][python_badge]](https://www.python.org/downloads/release/python-3100/)
[![License: AGPL v3][agpl3_badge]](https://www.gnu.org/licenses/agpl-3.0)
[![Code Style: Black][black_badge]](https://github.com/ambv/black)

Deconstructs Python code into modular JSON format and back. The JSON consists
of the following modular components:

- Docstring of a .py file
- Classes
- Class documentation
- Methods
- Method documentation
- Raw code

Before it outputs a Python file to a `.json` file, it verifies that it is able
to reconstruct the `.json` file back to its original file. It runs `pip`
package `black` to wash out any formatting differences between the original and
reconstructed Python files. This however, does not fix new line spacing.

## Example

An example CLI command is:

```sh
jsonmodipy \
  --get src_code \
  --filepath \
  ../D*/testrepos/doctestbot/src/pythontemplate/adder.py \
  --function
```

Below is an example workflow:

### Input Python file

```py
"""
* Tests a Python file with:
*   - class + classmethods + methods
"""


class MyClass:
   def __init__(self, file_dir: str, raw_filename: str):
       """Some initialisation documentation."""
       self.file_dir: str = file_dir
       self.raw_filename: str = raw_filename

       self.actual_double_newline: str = "SPECIAL"

   def instance_method(self, some: int) -> int:
       """Returns input+1."""
       return some + 1


def instance_method(some: int) -> None:
   """Returns None."""

```

### Output JSON file

```json
{
  "code_elems": [
    {
      "class": {
        "arguments": [],
        "children": [
          {
            "method": {
              "arguments": [
                {
                  "name": "self"
                },
                {
                  "argType": "str",
                  "name": "file_dir"
                },
                {
                  "argType": "str",
                  "name": "raw_filename"
                }
              ],
              "children": [
                {
                  "documentation_content": "Some initialisation documentation.",
                  "indentation": 8
                },
                {
                  "code_content": "self.file_dir: str = file_dir",
                  "indentation": 8
                },
                {
                  "code_content": "self.raw_filename: str = raw_filename",
                  "indentation": 8
                },
                {
                  "code_content": "self.actual_double_newline: str = 'SPECIAL'",
                  "indentation": 8
                }
              ],
              "documentation": "Some initialisation documentation.",
              "name": "__init__",
              "returnType": ""
            }
          },
          {
            "method": {
              "arguments": [
                {
                  "name": "self"
                },
                {
                  "argType": "int",
                  "name": "some"
                }
              ],
              "children": [
                {
                  "documentation_content": "Returns input+1.",
                  "indentation": 8
                },
                {
                  "code_content": "return (some + 1)",
                  "indentation": 8
                }
              ],
              "documentation": "Returns input+1.",
              "name": "instance_method",
              "returnType": "int"
            }
          }
        ],
        "documentation": "",
        "name": "MyClass",
        "returnType": "None"
      }
    },
    {
      "method": {
        "arguments": [
          {
            "argType": "int",
            "name": "some"
          }
        ],
        "children": [
          {
            "documentation_content": "Returns None.",
            "indentation": 4
          }
        ],
        "documentation": "Returns None.",
        "name": "instance_method",
        "returnType": "None"
      }
    }
  ],
  "docstring": "\n* Tests a Python file with:\n *   - class + classmethods + methods\n"
}
```

### Buggy reconstructed Python file

The reconstructed Python file does not yet preserve the new line spacing.

```py
"""
* Tests a Python file with:
*   - class + classmethods + methods
"""


class MyClass:
   def __init__(
       self,
       file_dir: str,
       raw_filename: str,
   ):
       """Some initialisation documentation."""
       self.file_dir: str = file_dir
       self.raw_filename: str = raw_filename
       self.actual_double_newline: str = "SPECIAL"

   def instance_method(
       self,
       some: int,
   ) -> int:
       """Returns input+1."""
       return some + 1


def instance_method(
   some: int,
) -> None:
   """Returns None."""
```

This is because:  `source_code: str = astunparse.unparse(stmt)` puts 1 new line
at the start and end of each line of code, regardless of whether the line of
code directly follows its previous line or, whether a blank line is in between.

## Testing

To reproduce this bug, create, and activate the conda environment, and run:

```sh
clear && python -m pytest test/TestPythonGetter.py
```

If you know how to fix the line spacing, please let me know in an issue
and/or send a pull-request.

## Usage

First install this pip package with:

```bash
pip install python2json
```

Then run:

```py
python -m src.jsonmodipy
```

## Developer

```bash
pre-commit install
pre-commit autoupdate
pre-commit run --all
```

## Publish pip package

Build the pip package with:

```bash
pip install --upgrade pip setuptools wheel
pip install twine
```

Install the pip package locally with:

```bash
pip install -e .
```

Upload the pip package to the world with:

```bash
rm -r dist
rm -r build
python -m build
python3 -m twine upload dist/\*
```

## Sphinx Documentation

To auto-generate the Sphinx documentation for your Python project look into the
`/docs` folder.

- The `conf.py` is the configuration that is used to build your
  Sphinx documentation.
- The index.rst contains the main page and documentation file-structure.
- You can include other `.rst` files that automatically include the
  documentation of a Python file, for example in `docs/source/example.rst`. In
  this `.rst` file, you refer to a "module"=`.py` file in a path relative to the
  root of this project.

### Include .py file example

To add a file in `src/jsonmodipy/helper.py` you
create a `docs/source/some_name.rst` file with content:

```rst
.. _helper-module:

Helper Module
===============

.. automodule:: jsonmodipy.helper
  :members:
  :undoc-members:
  :show-inheritance:

And here you can just type additional text that will be displayed on the site.
```

and to the `index.rst` you add it like:

```rst
.. jsonmodipy documentation master file, created by

Welcome to jsonmodipy's documentation!
=========================================

.. toctree::
   :maxdepth: 2

   example
   some_name
```

### Generate Sphinx Documentation

Then to generate/update the Sphinx documentation you can run from the root dir:

```sh
cd docs
 [ -d "_build" ] && rm -r "_build" ; [ -d "html" ] && rm -r "html" ; \
  clear ; \
  python -m sphinx -T -E -b html -d _build/doctrees -D language=en . html
```

<!-- Un-wrapped URL's below (Mostly for Badges) -->

[agpl3_badge]: https://img.shields.io/badge/License-AGPL_v3-blue.svg
[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[python_badge]: https://img.shields.io/badge/python-3.6-blue.svg
