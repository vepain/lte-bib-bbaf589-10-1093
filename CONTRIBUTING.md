# Contributing

<!--
module name: lteu
-->
**Table of content:**

* [Conventions](#conventions)
  * [Git](#git)
  * [Tags comments](#tags-comments)
* [Developing](#developing)
  * [Initializing the development environment](#initializing-the-development-environment)
  * [Use an already initialized environment](#use-an-already-initialized-environment)
  * [Git](#git-1)
    * [Developing a feature](#developing-a-feature)
  * [Linting and format](#linting-and-format)
* [Documentations](#documentations)
  * [Installation](#installation)
  * [Preview in live server](#preview-in-live-server)

## Conventions

### Git

* Branching conventions: [git-flow conventions](https://danielkummer.github.io/git-flow-cheatsheet/)
* Commit message conventions:
  * See [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
  * And [Conventional Commits VSCode extension](https://marketplace.visualstudio.com/items?itemName=vivaxy.vscode-conventional-commits)

### Tags comments

>[!NOTE]
> Sources:
>
> * [Conventional comments](https://conventionalcomments.org/)
> * [Medium @scottgrivner | Effectively Managing Technical Debt with TODO, FIXME, and Other Code Reminders](https://medium.com/@scottgrivner/effectively-managing-technical-debt-with-todo-fixme-and-other-code-reminders-e0b770f6180a)
> * [VSCode extension todo-tree](https://github.com/Gruntfuggly/todo-tree)

```python
# TAG The message
# TAG (context) The message
```

| Tag        | Purpose                         | Next tag(s)                                    |
| ---------- | ------------------------------- | ---------------------------------------------- |
| `TODO`     | Task to do in priority          |                                                |
| `FIXME`    | Bug to fix in priority          |                                                |
| `FEATURE`  | Future feature idea             | `TODO`                                         |
| `BUG`      | Not urgent bug to fix           | `FIXME`                                        |
| `REFACTOR` | Refactoring task                | `TODO (refactor)`                              |
| `HACK`     | Temporary trick                 | `TODO (hack)` `FIXME (hack)` `REFACTOR (hack)` |
| `XXX`      | Require caution, important area | `TODO` `FIXME` `REFACTOR`                      |
| `TOTEST`   | Require testing                 | `TODO (test)`                                  |
| `OPTIMIZE` | Can do for better performance   | `TODO (optimize)` `REFACTOR (optimize)`        |
| `DOCU`     | Add documentation               | `TODO (docu)`                                  |
| `REVIEW`   | Review code                     | `TODO` `FIXME` `REFACTOR`                      |

## Developing

* [VScode](https://code.visualstudio.com/)
  * Settings in `.vscode/settings.json`
  * Required extensions in `.vscode/extensions.json`
* [git-flow](https://danielkummer.github.io/git-flow-cheatsheet/) for git branching template
* [uv](https://docs.astral.sh/uv/) to manage Python environment
* [ruff](https://docs.astral.sh/ruff/) for linting
* [ty](https://docs.astral.sh/ty/) for type checking

### Initializing the development environment

>[!NOTE]
> **👤 @vepain:** I already initialized `git-flow` and `uv`, this section helps you to know how. Otherwise, you can go directly to the [next section](#use-an-already-initialized-environment).

```sh
git flow init
# Branch name for production releases: main
# Default for the other options.
```

```sh
uv init --package --name lteu # Letter To the Editor Utilities
```

You can see [./pyproject.toml](./pyproject.toml) file is also initialized, I changed the `projet.scripts.lteu` key:

```toml
[project.scripts]
  # From...
  # lteu = "lteu:main"
  # ...to
  lteu = "lteu.__main__:main"
```

Install the linters:

```sh
uv add --group lint ruff
uv add --group lint ty
```

You then have to say that the `lint` dependency group is part of the `dev` group (`uv` default dependency group for developers): <https://docs.astral.sh/uv/concepts/projects/dependencies/#nesting-groups>

```toml
[dependency-groups]
  dev = [ { include-group = "lint" } ]
```

Install [deptry](https://github.com/fpgmaas/deptry) to check correct dependencies:

```sh
uv add --group dev deptry
```

Install a first dependency ([Typer](https://typer.tiangolo.com/) to build great CLI):

```sh
uv add typer
```

Sync the environment:

```sh
uv sync
```

### Use an already initialized environment

By default, `uv` create a local `virtualenv` Python virtual environment in the directory `.venv`.

```sh
uv sync
```

>[!NOTE]
> The recommendation is to use `uv` to run the tools.
> If you do not want to use `uv` to run the tools, you have to activate the virtual environment `uv` created:
>
> ```sh
> source .venv/bin/activate
> # For Fish shell
> source .venv/bin/activate.fish
> ```
>
> Any command `uv run tool ...` can be run as `tool ...` with the virtual environment activated.

Check the command is installed:

```sh
uv run lteu --help
```

### Git

See [git-flow cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/).

>[!WARNING]
> Developing on the `develop` branch.
> The `main` branch is for releases.

Commits must respect the [conventional commits convention](#git).

#### Developing a feature

```sh
# Start a new feature
git flow feature start <feature-name>
# Do not forget to publish the feature!
git glow feature publish <feature-name>
# Finish
git flow feature finish <feature-name>
```

### Linting and format

Lint and format the code with [ruff](https://docs.astral.sh/ruff/):

```sh
uv run ruff check src/lteu
uv run ruff format src/lteu  # With VSCode you can autoformat on save
```

With [ty](https://docs.astral.sh/ty/):

```sh
uv run ty check src/lteu
```

## Documentations

We use [zensical](https://zensical.org) static website generator based on Markdown.

### Installation

Add dependencies via `uv`:

```sh
uv add --group docs zensical
```

Add group `docs` to group `dev`:

```toml
[dependency-groups]
  dev = [
    # ...
    { include-group = "docs" }
  ]
```

Other dependencies: are listed in the group `docs`.

### Preview in live server

```sh
uv run zensical serve
open http://localhost:8000 # May be different, use the adress given by the command in stdout
```
