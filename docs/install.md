---
icon: lucide/package-open
---

# Installation

## Install `lteu`

Clone the repository:

```sh
git clone -b develop git@github.com:vepain/lte-bib-bbaf589-10-1093.git
cd lte-bib-bbaf589-10-1093
```

### With uv (recommended)

Install thanks to [uv](https://docs.astral.sh/uv/):

```sh
uv sync
```

### Without uv

Create a virtual environment, source it, and install `lteu`:

```sh
pip install .
```

## Prepare working space

Create a directory in which who will do the experiments, create the figures etc.

We recommend creating the `data` directory in it:

```sh
mkdir data
```

The commands described in the [experiments](experiments/index.md) section will be executed in this directory.
