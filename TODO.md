# To-dos

## Preamble

* Visualize the data
  * [ ] Ground truth
  * [ ] Predictions

## Formatting task

* [ ] Format their ground truth to Plaseval [in `format.py` file](./src/lteu/format.py)

## Chromosomal bin

**Bias:** The measures take into account the bin containing the chromosomal contigs.

## Repeated contigs

**Bias:** The way they manage the repeated contig does not ensure a perfect prediction has a perfect measure.

* [ ] Identify a subset of the ground truth for which there are repeated contigs
* [ ] Find a measure of repetitiveness to illustrate the bias according to

## Contig lengths

**Bias:** They do not take into account the length of the contigs.

* [ ] Adapt the `sklearn` homogeneity and completness measures to take into account the length of the contigs
