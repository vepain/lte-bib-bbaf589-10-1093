# Letter to the editor - paper <https://doi.org/10.1093/bib/bbaf589>

The letter to the editor aims to demonstrate the bias of the clustering completeness and homogeneity measures to evaluate plasmid binning results, and that are used in [Circling in on plasmids: benchmarking plasmid detection and reconstruction tools for short-read data from diverse species](https://doi.org/10.1093/bib/bbaf589):

* They do not take into account the length of the contigs.
* The measures take into account the bin containing the chromosomal contigs.
* When plasmid bins are sharing contigs, a perfect prediction does not have a perfect evaluation measure.

See also:

* [Details about the bias](./docs/PlasEval_vs_V_measure.pdf) in `./docs/PlasEval_vs_V_measure.pdf`.
* [Article supplementary data](https://github.com/broadinstitute/plasmid-detection-benchmark)

>[!WARNING]
> Homogeneity and completeness measures computing by `sklearn` are not correct. So we code ours to fix this.
> See [GitHub issue #13058](https://github.com/scikit-learn/scikit-learn/issues/13058)

**Python package:** `lteu` (for Letter To the Editor Utilities).

## Experiments

### Reading the documentation in a web viewer (recommended)

With [uv](https://docs.astral.sh/uv/):

>[!NOTE]
> It will install all the dependencies for the developers.

```sh
uv sync
uv run zensical serve
open http://localhost:8000
```

### Reading the documentation in raw Markdown

The experiments running tutorial is in [./docs/index.md](./docs/index.md).

## Contributing

Refer first to the [CONTRIBUTING.md](./CONTRIBUTING.md) file, giving conventions and tutorials.
