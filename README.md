# Letter to the editor - paper <https://doi.org/10.1093/bib/bbaf589>

The letter to the editor aims to demonstrate the bias of the evaluating measures used in [Circling in on plasmids: benchmarking plasmid detection and reconstruction tools for short-read data from diverse species](https://doi.org/10.1093/bib/bbaf589):

* The measures take into account the bin containing the chromosomal contigs.
* The way they manage the repeated contig does not ensure a perfect prediction has a perfect measure.
* They do not take into account the length of the contigs.

See also:

* [Details about the bias](./docs/PlasEval_vs_V_measure.pdf) in `./docs/PlasEval_vs_V_measure.pdf`.
* [Article supplementary data](https://github.com/broadinstitute/plasmid-detection-benchmark)

>[!WARNING]
> Homogeneity and completeness measures computing by `sklearn` are not correct. So we code ours.
> See [GitHub issue #13058](https://github.com/scikit-learn/scikit-learn/issues/13058)

**Python package:** `lteu` (for Letter To the Editor Utilities).

## Installation

With [uv](https://docs.astral.sh/uv/):

```sh
uv sync
```

## Usage

```sh
uv run lteu --help
```

### Format ground-truths

To get the ground truths in the PlasEval format:

```sh
GT_OUTDIR=ground_truth
uv run lteu fmt gt-to-plaseval predictions.xlsx "$GT_OUTDIR"

# Where all the chromosomal contigs belong to the same bin:
GT_CHR_OUTDIR=ground_truth_chromosome
uv run lteu fmt gt-to-plaseval predictions.xlsx "$GT_CHR_OUTDIR" --with-chromosome
```

### Extract samples IDs with complete hybrid assemblies

```sh
# One column "Sample ID", one sample ID per row
uv run lteu fmt complete-hybrid-asm predictions.xlsx complete_hybrid_asm.tsv
```

### Format the bins for PlasEval

To see all the binning method codes:

```sh
uv run lteu fmt bins-to-plaseval --help
```

```sh
BINS_OUTDIR=bins/pbf
uv run lteu fmt bins-to-plaseval predictions.xlsx pbf "$BINS_OUTDIR"

# Where all the chromosomal contigs belong to the same bin:
BINS_CHR_OUTDIR=bins_chromosome/pbf
uv run lteu fmt bins-to-plaseval predictions.xlsx pbf "$BINS_CHR_OUTDIR" --with-chromosome
```

## Experiments

The experiments running tutorial is in [./experiments/README.md](./experiments/README.md).

## To-do

Refer to the [TODO.md](./TODO.md) file.

## Contributing

Refer first to the [CONTRIBUTING.md](./CONTRIBUTING.md) file, giving conventions and tutorials.
