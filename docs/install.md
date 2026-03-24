---
icon: lucide/package-open
---

# Installation

Clone the repository:

```sh
git clone git@github.com:vepain/lte-bib-bbaf589-10-1093.git
cd lte-bib-bbaf589-10-1093
```

<!-- markdownlint-disable MD046 -->
=== "With `uv` (recommended)"

    Install thanks to [uv](https://docs.astral.sh/uv/):

    ```sh
    uv sync --no-dev
    ```

    Source the environment:

    === "Bash"

        ```sh
        source .venv/bin/activate
        ```

    === "Fish"

        ```sh
        source .venv/bin/activate.fish
        ```

=== "Without `uv`"

    Create a virtual environment and source it

    === "Bash"

        ```sh
        python3.13 -m venv .venv
        source .venv/bin/activate
        ```

    === "Fish"

        ```sh
        python3.13 -m venv .venv
        source .venv/bin/activate.fish
        ```

    install `lteu`:

    ```sh
    pip install .
    ```

<!-- markdownlint-enable MD046 -->

Test the installation with:

```sh
lteu --help
```
