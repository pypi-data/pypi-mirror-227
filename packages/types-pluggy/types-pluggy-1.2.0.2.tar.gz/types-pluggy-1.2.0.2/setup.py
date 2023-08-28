from setuptools import setup

name = "types-pluggy"
description = "Typing stubs for pluggy"
long_description = '''
## Typing stubs for pluggy

This is a PEP 561 type stub package for the `pluggy` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`pluggy`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pluggy. All fixes for
types and metadata should be contributed there.

*Note:* The `pluggy` package includes type annotations or type stubs
since version 1.3.0. Please uninstall the `types-pluggy`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `94ddcf87dac61ff2626f995d8ee8c6f3402d5cb7` and was tested
with mypy 1.5.1, pyright 1.1.323, and
pytype 2023.8.14.
'''.lstrip()

setup(name=name,
      version="1.2.0.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pluggy.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pluggy-stubs'],
      package_data={'pluggy-stubs': ['__init__.pyi', '_hooks.pyi', '_manager.pyi', '_result.pyi', '_tracing.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
