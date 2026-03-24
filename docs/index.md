---
icon: lucide/home
---

# On using clustering statistics for assessing plasmid binning tools accuracy

This documentation describes how to reproduce the experiments present in the letter of the editor for the paper [Circling in on plasmids: benchmarking plasmid detection and reconstruction tools for short-read data from diverse species](https://doi.org/10.1093/bib/bbaf589)

1. [Installing the Python utilities](/install.md)
2. [Configurating the working space](/inputs.md)
3. [Reproducing the experiments](/experiments/index.md)

>[!WARNING]
> Homogeneity and completeness measures computing by `sklearn` are not correct.
> See [GitHub issue #13058](https://github.com/scikit-learn/scikit-learn/issues/13058).
> Our experiments rely on our own coding of the computation of completeness and homogeneity.

## See also

* [Additional notes: On using homogeneity and completeness for evaluating plasmid binning](/PlasEval_vs_V_measure.pdf){ target="_blank" }
* [Supplementary data for the article "Circling in on plasmids: benchmarking plasmid detection and reconstruction tools for short-read data from diverse species"](https://github.com/broadinstitute/plasmid-detection-benchmark){ target="_blank" }
