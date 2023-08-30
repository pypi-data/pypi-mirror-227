from setuptools import setup

name = "types-singledispatch"
description = "Typing stubs for singledispatch"
long_description = '''
## Typing stubs for singledispatch

This is a PEP 561 type stub package for the `singledispatch` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`singledispatch`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/singledispatch. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `28d3ce2951008dfdb199ec0d728eab5d164ea96b` and was tested
with mypy 1.5.1, pyright 1.1.323, and
pytype 2023.8.14.
'''.lstrip()

setup(name=name,
      version="4.1.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/singledispatch.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['singledispatch-stubs'],
      package_data={'singledispatch-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
