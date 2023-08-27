# Shepherd - Core

[![PyPiVersion](https://img.shields.io/pypi/v/shepherd_core.svg)](https://pypi.org/project/shepherd_core)
[![Pytest](https://github.com/orgua/shepherd-datalib/actions/workflows/python-app.yml/badge.svg)](https://github.com/orgua/shepherd-datalib/actions/workflows/python-app.yml)
[![CodeStyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This Python Module bundles data-models and file-access-routines for the shepherd-testbed, that are used by several codebases.

Users probably want to use the [datalib](https://pypi.org/project/shepherd_data).

---

**Main Project**: [https://github.com/orgua/shepherd](https://github.com/orgua/shepherd)

**Source Code**: [https://github.com/orgua/shepherd-datalib](https://github.com/orgua/shepherd-datalib)

---

This library allows to

- read and write shepherds h5-files
- create, read, write and convert experiments for the testbed (all data-models included)
- simulate the virtual source, including virtual harvesters
- connect and query the testbed via a webclient (TestbedClient)
- work with target-firmwares
  - embed, modify, verify, convert
  - **Note**: working with ELF-files requires external dependencies, see ``Installation``-Chapter
- decode waveforms -> uart

see [examples](./examples) for more details.

# Installation

The Library is available via PyPI and can be installed with

```shell
  pip install shepherd-core

  # or for the full experience
  pip install shepherd-data
```

for bleeding-edge-features or dev-work it is possible to install directly from GitHub-Sources (here `dev`-branch):

```Shell
pip install git+https://github.com/orgua/shepherd-datalib.git@dev#subdirectory=shepherd_core -U
```


If you are working with ``.elf``-files (embedding into experiments) you make "objcopy" accessible to python. In Ubuntu, you can either install ``build-essential`` or ``binutils-$ARCH`` with arch being ``msp430`` or ``arm-none-eabi`` for the nRF52.

```shell
  sudo apt install build-essential
```

For more advanced work with ``.elf``-files (modify value of symbols / target-ID) you should install

```shell
  pip install shepherd-core[elf]
```

and also make sure the prereqs for the [pwntools](https://docs.pwntools.com/en/stable/install.html) are met.

For creating an inventory of the host-system you should install

```shell
  pip install shepherd-core[inventory]
```
