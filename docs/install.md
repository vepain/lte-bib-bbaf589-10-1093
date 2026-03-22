---
icon: lucide/package-open
---

# Installation

## Install `lteu`

Clone the repository:

```sh
git clone git@github.com:vepain/lte-bib-bbaf589-10-1093.git
cd lte-bib-bbaf589-10-1093
```

<!-- markdownlint-disable MD046 -->
=== "With `uv` (recommended)"

    Install thanks to [uv](https://docs.astral.sh/uv/):

    ```sh
    uv install .
    ```

    The commands described in the [experiments](experiments/index.md) are prepended by `uv run` e.g. `uv run lteu --help`.

=== "Without `uv`"

    Create a virtual environment, source it, and install `lteu`:

    ```sh
    pip install .
    ```

    >[!WARNING]
    > If you use this method, make sure you have sourced your virtual environment before running the commands in the [experiments](experiments/index.md).
    > Also, all the commands in the scripts use `uv run lteu`. So you may have to remove the `uv run` prefix if you cannot use `uv`.

<!-- markdownlint-enable MD046 -->

## Usage

Test the installation with:

<!-- markdownlint-disable MD046 -->
=== "With `uv` (recommended)"

    ```sh
    uv run lteu --help
    ```

=== "Without `uv`"

    ```sh
    lteu --help
    ```
<!-- markdownlint-enable MD046 -->