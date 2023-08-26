# docassemble-stubs

Docassemble has a lot of python functions, but no in-source types.
This package lets you install and use types for docassemble functions.

Includes docassemble.base and docassembe.webapp, but I wouldn't rely on
docassemble.webapp's types to be perfectly accurate. Types are fairly close
to what's generated with `stubgen`, and are still "in progress".

## Installation

You can install from pypi with `pip install docassemble-types`

You can also download this git repo and run `pip install .` while inside of
the repo. `mypy` should be able to find types installed in your python
environment.

## Updating the stubs

Install both these stubs and the corresponding version of docassemble, and run:

```bash
stubtest --allowlist base_allowlist.txt docassemble.base
```

For the webapp version, `DA_CONFIG_FILE` needs to be defined as an env var.

```bash
export DA_CONFIG_FILE=/home/myuser/path/to/config/myconfig.yml
stubtest --allowlist web_allowlist.txt docassemble.webapp
```

All of the errors will be things that are missing in the stubs, and you will
have to fix them manually.

TODO(brycew): find a way to automatically update the stubs without overwriting the manually
changed types?
