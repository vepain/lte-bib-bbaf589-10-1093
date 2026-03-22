# On using clustering statistics for assessing plasmid binning tools accuracy

This repo allows to reproduce the experiments described in the letter to the editor submitted to Briefings in Bioinformatics about pitfalls of the accuracy measures used in he paper [Circling in on plasmids: benchmarking plasmid detection and reconstruction tools for short-read data from diverse species](https://doi.org/10.1093/bib/bbaf589):

* They do not take into account the length of the contigs.
* The measures take into account the bin containing the chromosomal contigs.
* When plasmid bins are sharing contigs, a perfect prediction does not have a perfect evaluation measure.

See also:

* [Notes on drawbacks of homogeneity and completeness](./docs/PlasEval_vs_V_measure.pdf) in `./docs/PlasEval_vs_V_measure.pdf`.
* [Article "Circling in on plasmids: benchmarking plasmid detection and reconstruction tools for short-read data from diverse species" supplementary data](https://github.com/broadinstitute/plasmid-detection-benchmark)

>[!WARNING]
> Homogeneity and completeness measures computing by `sklearn` are not correct.
> See [GitHub issue #13058](https://github.com/scikit-learn/scikit-learn/issues/13058)
> Our experiments rely on our own coding of the computation of completeness and homogeneity.

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
