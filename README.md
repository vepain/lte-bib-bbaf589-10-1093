# On using clustering statistics for assessing plasmid binning tools accuracy

This repo allows to reproduce the experiments described in the letter to the editor submitted to Briefings in Bioinformatics about pitfalls of the accuracy measures used in he paper [Circling in on plasmids: benchmarking plasmid detection and reconstruction tools for short-read data from diverse species](https://doi.org/10.1093/bib/bbaf589):

* They do not take into account the length of the contigs.
* The measures take into account the bin containing the chromosomal contigs.
* When plasmid bins are sharing contigs, a perfect prediction does not have a perfect evaluation measure.

## Experiments

Please refer to the [documentation](vepain.github.io/lte-bib-BBAF589-10-1093) to reproduce the experiments described in the letter to the editor.

>[!TIP]
> If you cannot access to the web documentation, you can read it in raw Markdown format via the `./docs/index.md` file.
> Otherwise, you can follow the instructions in the [CONTRIBUTING.md](./CONTRIBUTING.md) file.

## Contributing

Refer first to the [CONTRIBUTING.md](./CONTRIBUTING.md) file, giving conventions and tutorials.
