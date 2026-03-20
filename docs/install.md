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
uv install .
```

The commands described in the [experiments](experiments/index.md) can be prepended by `uv run` e.g. `uv run lteu --help`.

### Without uv

Create a virtual environment, source it, and install `lteu`:

```sh
pip install .
```

>[!WARNING]
> If you use this method, make sure you have sourced your virtual environment before running the commands in the [experiments](experiments/index.md).

## Usage

Test the installation with:

```sh
lteu --help
```

To run the [experiments](experiments/index.md), we will use the command:

```sh
lteu exp --help
```
