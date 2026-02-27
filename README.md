# Letter to the editor - paper <https://doi.org/10.1093/bib/bbaf589>

The letter to the editor aims to demonstrate the bias of the evaluating measures used in [Circling in on plasmids: benchmarking plasmid detection and reconstruction tools for short-read data from diverse species](https://doi.org/10.1093/bib/bbaf589):

* The measures take into account the bin containing the chromosomal contigs.
* The way they manage the repeated contig does not ensure a perfect prediction has a perfect measure.
* They do not take into account the length of the contigs.

See also:

* [Details about the bias](./docs/PlasEval_vs_V_measure.pdf) in `./docs/PlasEval_vs_V_measure.pdf`.
* [Article supplementary data](https://github.com/broadinstitute/plasmid-detection-benchmark)

## Python package

`lteu` (for Letter To the Editor Utilities).

### Installation

With [uv](https://docs.astral.sh/uv/):

```sh
uv sync
```

### Usage

```sh
uv run lteu --help
```

## To-do

Refer to the [TODO.md](./TODO.md) file.

## Contributing

Refer first to the [CONTRIBUTING.md](./CONTRIBUTING.md) file, giving conventions and tutorials.
